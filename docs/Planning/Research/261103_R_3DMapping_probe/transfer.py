"""Carry Pixal3D's vertex colours onto hm08's layout: align, then nearest surface point per texel.

Usage: uv run --with scipy --with trimesh python transfer.py <painted.glb> <out dir> <tag>
Reads Phase27's atlas (library/parity/P27_Body/atlas.npz: each 2K texel's position, normal, cover).
Writes <out>/E_<tag>_all.png (every skin texel from Pixal3D) and E_<tag>_body.png (the head kept as served),
both 8K on Tone34's served atlas, and <out>/E_<tag>.json (alignment and distance numbers).
"""
import json
import sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[4]   # docs/Planning/Research/<probe>/ -> the repo
import numpy as np
import trimesh
from PIL import Image
from scipy.spatial import cKDTree

sys.path.insert(0, str(REPO / "tools/converters/fit"))
import project_body as pb      # noqa: E402
import project_views as pv     # noqa: E402

Image.MAX_IMAGE_PIXELS = None
glb, out, tag = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
out.mkdir(parents=True, exist_ok=True)
A = np.load(REPO / "library/parity/P27_Body/atlas.npz")
P, cover, body = A["P"].astype(np.float64), A["cover"], A["body"]

def glb_attr(path, name):
    """One vertex attribute of the first primitive, read straight from the GLB (as float)."""
    import struct
    b = path.read_bytes()
    n = struct.unpack("<I", b[12:16])[0]
    j = json.loads(b[20:20 + n])
    bin0 = 20 + n + 8
    acc = j["accessors"][j["meshes"][0]["primitives"][0]["attributes"][name]]
    bv = j["bufferViews"][acc["bufferView"]]
    comps = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}[acc["type"]]
    dt = {5126: np.float32, 5121: np.uint8, 5123: np.uint16}[acc["componentType"]]
    off = bin0 + bv.get("byteOffset", 0) + acc.get("byteOffset", 0)
    a = np.frombuffer(b, dt, acc["count"] * comps, off).reshape(acc["count"], comps).astype(np.float64)
    if dt != np.float32:
        a /= np.iinfo(dt).max
    return a, acc["componentType"]


V, _ = glb_attr(glb, "POSITION")
col, ctype = glb_attr(glb, "COLOR_0")
col = col[:, :3]
print(f"pixal3d mesh: {len(V)} vertices; COLOR_0 type {ctype}, mean {col.mean(0).round(3)}, max {col.max(0).round(3)}")

rng = np.random.default_rng(0)
Q = P[cover]
Qs = Q[rng.choice(len(Q), 60000, replace=False)]


def norm(X):
    lo, hi = X.min(0), X.max(0)
    return (lo + hi) / 2, hi[1] - lo[1]


def roty(a):
    a = np.radians(a)
    return np.array([[np.cos(a), 0, np.sin(a)], [0, 1, 0], [-np.sin(a), 0, np.cos(a)]])


cq, hq = norm(Qs)
tq = cKDTree(Qs)
best = None
for name, R0 in [(f"y{a}", roty(a)) for a in (0, 90, 180, 270)] + \
        [(f"zup_y{a}", roty(a) @ np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]])) for a in (0, 90, 180, 270)]:
    X = V @ R0.T
    cx, hx = norm(X)
    X = (X - cx) * (hq / hx) + cq
    d = tq.query(X[::20])[0].mean() + cKDTree(X[::20]).query(Qs)[0].mean()
    print(f"  orientation {name}: chamfer {d * 1000:.1f} mm")
    if best is None or d < best[0]:
        best = (d, name, R0, cx, hq / hx)
_, oname, R0, cx, s0 = best
X = (V @ R0.T - cx) * s0 + cq

# ICP with uniform scale, hm08 samples -> pixal surface (vertex cloud)
for it in range(40):
    sub = X[::4]
    dist, idx = cKDTree(sub).query(Qs)
    keep = dist < np.percentile(dist, 90)
    a, b = sub[idx[keep]], Qs[keep]          # move pixal points a onto hm08 points b
    ma, mb = a.mean(0), b.mean(0)
    A0, B0 = a - ma, b - mb
    U, S, Vt = np.linalg.svd(A0.T @ B0)
    D = np.diag([1, 1, np.sign(np.linalg.det(U @ Vt))])
    R = (U @ D @ Vt).T
    sc = (S * np.diag(D)).sum() / (A0 ** 2).sum()
    X = (X - ma) @ R.T * sc + mb
d_fwd = cKDTree(X).query(Qs)[0]
print(f"aligned ({oname}): hm08 -> pixal3d median {np.median(d_fwd) * 1000:.1f} mm, p90 {np.percentile(d_fwd, 90) * 1000:.1f}, p99 {np.percentile(d_fwd, 99) * 1000:.1f}")

# colour per texel: inverse-distance over the 4 nearest vertices
tx = cKDTree(X)
dist, idx = tx.query(Q, k=4)
wgt = 1 / np.maximum(dist, 1e-5)
c = (col[idx] * wgt[..., None]).sum(1) / wgt.sum(1, keepdims=True)
# COLOR_0 is linear (glTF): used as is
N = cover.shape[0]
E = np.zeros((N, N, 3))
E[cover] = c
dmap = np.zeros((N, N))
dmap[cover] = dist[:, 0]

SERVED = REPO / "MatterLibrary/textures/fit/makehuman/skin/SkinTone34_basecolor_sUKN.png"
CONST = np.array([0.8951, 0.5383, 0.4296], np.float32)   # the article's base_color_const (its .mtlx)
lut = pb.lin(np.arange(256) / 255.0).astype(np.float32)
base = lut[np.asarray(Image.open(SERVED).convert("RGB"))] * CONST   # Tone34 as served: rendered albedo, 8K linear
S8 = base.shape[0]
k8 = S8 // N
Cb = base.reshape(N, k8, N, k8, 3).mean((1, 3))
gain = Cb[body].mean(0) / E[body].mean(0)       # the library's calibration: hold the body's mean per channel
E *= gain
ids8, _, head_isl = pb.skin_islands(S8)
full = pb.pushpull(np.where(cover[..., None], E, 0.0), cover)
up = np.stack([np.asarray(Image.fromarray(full[..., k].astype(np.float32), "F").resize((S8, S8), Image.BILINEAR))
               for k in range(3)], -1)
from scipy.ndimage import binary_dilation as dil  # noqa: E402
skin8 = ids8 > 0
sel_all = skin8 | (dil(skin8, iterations=pb.GUTTER) & (ids8 == 0))
sel_body = (ids8 > 0) & (ids8 != head_isl)
sel_body |= dil(sel_body, iterations=pb.GUTTER) & (ids8 == 0)
for name, sel in (("all", sel_all), ("body", sel_body)):
    o = base.astype(np.float32).copy()
    o[sel] = up[sel]
    Image.fromarray((pb.srgb(np.clip(o, 0, 1)) * 255 + 0.5).astype(np.uint8)).save(out / f"E_{tag}_{name}.png")
pb.save(out / f"E_{tag}_2048.png", np.clip(E, 0, 1))
Image.fromarray((np.clip(dmap / 0.02, 0, 1) * 255).astype(np.uint8)).save(out / f"E_{tag}_dist.png")
rec = {"glb": str(glb), "orientation": oname, "vertices": int(len(V)),
       "dist_mm": {"median": round(float(np.median(dist[:, 0]) * 1000), 2),
                   "p90": round(float(np.percentile(dist[:, 0], 90) * 1000), 2),
                   "p99": round(float(np.percentile(dist[:, 0], 99) * 1000), 2)},
       "over_1cm_pct": round(float((dist[:, 0] > 0.01).mean() * 100), 2),
       "gain": [round(float(v), 3) for v in gain], "head_island": head_isl}
(out / f"E_{tag}.json").write_text(json.dumps(rec, indent=1) + "\n")
print(json.dumps(rec))
