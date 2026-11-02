#!/usr/bin/env python3
"""An image model's picture of a person becomes the body island's skin, through four cameras (Phase27).

    uv run --with scipy tools/converters/fit/project_body.py prep  <dir>
    python3 -I tools/converters/fit/project_body.py paint <dir> [--seeds 7] [--strength 0.5]
    uv run --with scipy tools/converters/fit/project_body.py fit   <dir> <picture>
    uv run --with scipy tools/converters/fit/project_body.py put   <dir> <picture> <tag> [--head <atlas.png>] [--no-fit]
    uv run --with scipy tools/converters/fit/project_body.py seams <atlas.png>
    uv run --with scipy tools/converters/fit/project_body.py close prep|paint|put <dir> [--atlas D.png] [--tag t]

hm08's body island is a person seen from the front with the back split down the spine (F-P27-3), so no
one camera sees it. ``prep`` renders hm08 four times in ONE picture, front, profile, back, profile
(orthographic, 600 px a metre, Tone34's colour under a soft key: ``in_f4.png``), and keeps each view's
depth, normals and silhouette. ``paint`` has Krea repaint it at 0.5 through the lead's ComfyUI (one
record per picture; RD-P25-7): the model keeps hm08's pose and build and draws one person four times
(F-P27-11). Its outline still differs from hm08's in each view (F-P27-12), so ``fit`` fits each view to
hm08's render before anything is projected: every pixel of hm08's outline is matched to the model's
outline along hm08's normal (the nearest crossing from inside to outside within ``DMAX`` pixels,
outliers against the contour's own median dropped), and that displacement, held on the outline, is
relaxed harmonically over hm08's silhouette: one coordinate field per view, nothing blended (the face's
field, F-P25-16). ``put`` then gives each texel of the body, the feet and (with ``--head``) the back of the
neck the colour of the view that faces it most squarely and shows the body there (a hard cut), through
the fit; holes take the maker's skin at the level of their neighbours on the body; the body held to C's
mean; the groin the maker's colour at the surrounding level (RD-P27-2, RD-SKM-4). The hands are the
maker's until they have their own cameras (``HANDS_FROM_PICTURE``). Where the picture's skin meets
another source (Phase25's head, the maker's hands) the step is split between the two sides as a smooth
tone ramp (``neck_join``). ``seams`` measures the level step across each of hm08's seams on an atlas,
beside the skin's own variation (27.2). The result is written on
Tone34's 8K atlas (C elsewhere, or ``--head``'s atlas, Phase25's D) as linear albedo, sRGB-encoded, for
``look.py --candidate``. Everything is written under ``<dir>`` (git-ignored ``library/parity/P27_*``:
no picture of an unclothed person is committed, RD-P27-3). SciPy rides ``--with``; the project gains no
dependency.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("MATTER_SKIN_N", "2048")       # the body's work is at 2K (RD-P25-20, F-P27-4)
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

S = 600.0                    # pixels per metre in the four views (1.67 mm a pixel)
VH = 1152                    # the picture's height
VIEWS = ((0, 624), (90, 360), (180, 624), (270, 360))   # (yaw, width): front, profile, back, profile
CY = 0.015                   # the body's middle height in the mesh's frame (m)
DMAX = 24                    # the furthest the model's outline is looked for, in pixels (4 cm)
GROIN_R = (0.075, 0.075, 0.09)   # the groin's soft ellipsoid round the crotch (m): x, y, z radii
MIN_FACE = 0.3               # a texel no view faces better than this is a hole, not a grazing sample: the model
                             # paints a surface turning away darker, and dividing its light out there brightens it 2-3x
LIGHT_FLOOR = 0.3            # the least light divided out (``--delight``)
LIGHT_TERMS = {0: 1, 1: 4, 2: 9}   # the normal's terms up to each order (``--light-order``): order 2 also takes
                             # out shading that follows the spine's and the blades' curvature (27.2.5)
LUM = (0.2126, 0.7152, 0.0722)
LEVEL_CAP = 0.5              # the most a seam levelling moves a view, in log colour (x1.65)
NECK_R = 0.06                # the neck join's ramp on each side of the seam (m)
NAPE_R = 0.05                # how far up the head island the four views paint the back of the neck (m)
RIM = 2                      # texels of the maker's 2K rim taken from the island's inside
HANDS_FROM_PICTURE = False   # the four views' fingers do not land at 1.7 mm a pixel (27.2): the maker's hands,
                             # toned to the forearm, until the hands have their own cameras (the Brief's route)
MIN_CHROMA = 0.15            # the least (max - min) / max a sample of skin has; the background is ~0
GUTTER = 6                   # texels of the 8K atlas's gutter the painted colour fills
NAPE_X = 0.055               # ... and how far to each side of the middle (m): the ears start beyond it
PROMPT = ("A full-length photograph of the same real young woman about twenty shown four times side by side: seen "
          "from the front, in profile from her side, from the back, and in profile from her other side. She stands "
          "in an A-pose with her arms held out from her sides, nude, with a completely hairless body and a shaved "
          "bald head, light warm skin between Fitzpatrick III and IV. Real unretouched skin: visible pores, fine "
          "vellus hair, small blemishes, tiny moles, faint freckles, uneven tone, slight redness on the knees, elbows "
          "and knuckles. Even, soft, shadowless studio light on a plain grey background. Not a 3D render, not CGI, "
          "not painted.")


def _np():
    import numpy as np  # noqa: PLC0415
    return np


def lin(s):
    np = _np()
    return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)


def srgb(x):
    np = _np()
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


def save(path: Path, linimg) -> None:
    from PIL import Image  # noqa: PLC0415
    Image.fromarray((srgb(linimg) * 255 + 0.5).astype(_np().uint8)).save(path)


# ------------------------------------------------------------------ the renderer -----------------
def mesh():
    """hm08's points, texture coordinates, triangles (vertex, uv index pairs) and vertex normals."""
    np = _np()
    import gen_synth_skin as gss  # noqa: PLC0415
    import make_kits  # noqa: PLC0415
    m = make_kits.load_mesh(gss.MESH)
    P = np.array(m["points"], np.float64)
    vt = np.array(m["vt"], np.float64)
    T = np.array([[(f[i][0], f[i][1]) for i in t] for f in m["faces"]
                  for t in (((0, 1, 2), (0, 2, 3)) if len(f) == 4 else ((0, 1, 2),))])
    vn = np.zeros_like(P)
    a, b, c = (T[:, k, 0] for k in range(3))
    fn = np.cross(P[b] - P[a], P[c] - P[a])
    for k in (a, b, c):
        np.add.at(vn, k, fn)
    vn /= np.maximum(np.linalg.norm(vn, axis=1, keepdims=True), 1e-12)
    return P, vt, T, vn


def rot(yaw):
    """World → view: the body turned by ``yaw``; the camera looks down the view's -z."""
    np = _np()
    a = np.radians(yaw)
    return np.array([[np.cos(a), 0, -np.sin(a)], [0, 1, 0], [np.sin(a), 0, np.cos(a)]])


def proj(X, yaw, w, h=VH, s=S, cy=CY):
    """Orthographic: x right, y down in pixels (a pixel's centre at i + 0.5); depth, smaller is closer."""
    V = X @ rot(yaw).T
    return w / 2 + s * V[..., 0], h / 2 - s * (V[..., 1] - cy), -V[..., 2]


def raster(P, vt, T, vn, yaw, w, h=VH):
    """Depth, texture coordinate, normal and silhouette of hm08 through one view."""
    np = _np()
    px, py, z = proj(P, yaw, w, h)
    nv = vn @ rot(yaw).T
    zb = np.full((h, w), np.inf); uvb = np.zeros((h, w, 2)); nb = np.zeros((h, w, 3))
    for tri in T:
        vi, ti = tri[:, 0], tri[:, 1]
        ax, bx, cx = px[vi]; ay, by, cyy = py[vi]
        den = (by - cyy) * (ax - cx) + (cx - bx) * (ay - cyy)
        if abs(den) < 1e-9:
            continue
        x0, x1 = int(max(np.floor(min(ax, bx, cx)), 0)), int(min(np.ceil(max(ax, bx, cx)), w - 1))
        y0, y1 = int(max(np.floor(min(ay, by, cyy)), 0)), int(min(np.ceil(max(ay, by, cyy)), h - 1))
        if x1 < x0 or y1 < y0:
            continue
        ys, xs = np.mgrid[y0:y1 + 1, x0:x1 + 1]
        qx, qy = xs + 0.5, ys + 0.5
        w0 = ((by - cyy) * (qx - cx) + (cx - bx) * (qy - cyy)) / den
        w1 = ((cyy - ay) * (qx - cx) + (ax - cx) * (qy - cyy)) / den
        w2 = 1 - w0 - w1
        ins = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        if not ins.any():
            continue
        Wb = np.stack([w0[ins], w1[ins], w2[ins]], -1)
        zz = Wb @ z[vi]
        yy, xx = ys[ins], xs[ins]
        c = zz < zb[yy, xx]
        yy, xx, Wb, zz = yy[c], xx[c], Wb[c], zz[c]
        zb[yy, xx] = zz
        uv = Wb @ vt[ti]
        uvb[yy, xx, 0], uvb[yy, xx, 1] = uv[:, 0], 1 - uv[:, 1]
        n = Wb @ nv[vi]
        nb[yy, xx] = n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    return {"z": zb, "uv": uvb, "n": nb, "mask": np.isfinite(zb)}


def shade(n, amb=0.5):
    np = _np()
    lt = np.array([-0.35, 0.45, 1.0])
    return amb + (1 - amb) * np.clip(n @ (lt / np.linalg.norm(lt)), 0, 1)


def sample(img, x, y):
    """``img`` at index coordinates (``x``, ``y``), bilinear, clamped at the edge."""
    from scipy.ndimage import map_coordinates  # noqa: PLC0415
    np = _np()
    if img.ndim == 2:
        return map_coordinates(img, [y, x], order=1, mode="nearest")
    return np.stack([map_coordinates(img[..., c], [y, x], order=1, mode="nearest") for c in range(img.shape[2])], -1)


def pushpull(img, known):
    np = _np()
    if known.all() or min(img.shape[:2]) < 2:
        return img
    h, w, c = img.shape
    H2, W2 = (h + 1) // 2, (w + 1) // 2
    pi = np.zeros((H2 * 2, W2 * 2, c)); pk = np.zeros((H2 * 2, W2 * 2))
    pi[:h, :w] = img * known[..., None]; pk[:h, :w] = known
    si = pi.reshape(H2, 2, W2, 2, c).sum((1, 3)); sk = pk.reshape(H2, 2, W2, 2).sum((1, 3))
    low = pushpull(np.where(sk[..., None] > 0, si / np.maximum(sk, 1e-9)[..., None], 0), sk > 0)
    up = np.repeat(np.repeat(low, 2, 0), 2, 1)[:h, :w]
    return np.where(known[..., None], img, up)


def frames():
    """Each view's (yaw, x offset in the picture, width)."""
    out, x = [], 0
    for yaw, w in VIEWS:
        out.append((yaw, x, w))
        x += w
    return out


# ------------------------------------------------------------------ prep ---------------------------
def body_island(size: int):
    """The body island's id and the atlas of island ids at ``size`` (hm08's own faces, F-P27-1)."""
    np = _np()
    import gen_synth_skin as gss  # noqa: PLC0415
    import make_kits  # noqa: PLC0415
    m = make_kits.load_mesh(gss.MESH)
    ids = np.asarray(make_kits.island_ids_png(m, size), np.int32)
    counts = np.bincount(ids.ravel())
    counts[0] = 0
    return int(np.argmax(counts)), ids


def cmd_prep(d: Path) -> None:
    np = _np()
    from PIL import Image  # noqa: PLC0415
    import gen_synth_skin as gss  # noqa: PLC0415
    import make_kits  # noqa: PLC0415
    import project_views as pv  # noqa: PLC0415
    Image.MAX_IMAGE_PIXELS = None
    if gss.N != 2048:
        raise SystemExit(f"prep works at 2048 (MATTER_SKIN_N is {gss.N})")
    d.mkdir(parents=True, exist_ok=True)
    t = time.time()
    m = make_kits.load_mesh(gss.MESH)
    Pf, Nf, _, cover = gss.rasterise(m)
    bid, ids = body_island(2048)
    body = (ids == bid) & cover
    a8 = pv.subject_albedo()
    k = a8.shape[0] // 2048
    C = a8.reshape(2048, k, 2048, k, 3).mean((1, 3))
    J = gss.joints()
    crotch = (J["l-upper-leg"] + J["r-upper-leg"]) / 2 - np.array([0.0, 0.06, 0.0])
    groin = body & (gss.ellipse3(Pf, crotch, GROIN_R) > 0.5)
    np.savez(d / "atlas.npz", C=C.astype(np.float32), P=Pf.astype(np.float32), N=Nf.astype(np.float32),
             cover=cover, body=body, groin=groin, body_id=bid)
    print(f"atlas at 2048: {time.time() - t:.0f} s; body texels {int(body.sum())}, groin {int(groin.sum())}")
    P, vt, T, vn = mesh()
    W = sum(w for _, w in VIEWS)
    pic = np.full((VH, W, 3), 0.18)
    for yaw, x0, w in frames():
        g = raster(P, vt, T, vn, yaw, w)
        np.savez(d / f"geom_{yaw}.npz", **g)
        col = sample(C, g["uv"][..., 0] * 2048 - 0.5, g["uv"][..., 1] * 2048 - 0.5) * shade(g["n"])[..., None]
        part = pic[:, x0:x0 + w]
        part[g["mask"]] = col[g["mask"]]
    save(d / "in_f4.png", pic)
    print(f"in_f4.png {W} x {VH}; prep {time.time() - t:.0f} s")


# ------------------------------------------------------------------ paint --------------------------
def cmd_paint(d: Path, seeds: list, strength: float, server: str) -> None:
    import gen_views_model as g  # noqa: PLC0415
    graph = json.loads(g.WORKFLOWS["krea"].read_text(encoding="utf-8"))
    version = json.loads(g._call(server, "/system_stats"))["system"]["comfyui_version"]
    models = {n["class_type"]: n["inputs"].get("unet_name") or n["inputs"].get("clip_name") or n["inputs"].get("vae_name")
              for n in graph.values() if n["class_type"] in ("UNETLoader", "CLIPLoader", "VAELoader")}
    src = d / "in_f4.png"
    up = g.upload(server, src)
    for sd in seeds:
        t = time.time()
        vals = {"IMAGE": up, "PROMPT": PROMPT, "SEED": sd, "STEPS": 8, "STRENGTH": strength, "PREFIX": "matter_p27body"}
        png, pid = g.run(server, g.fill(graph, vals))
        name = f"f4_s{round(strength * 100):02d}_seed{sd}"
        (d / f"{name}.png").write_bytes(png)
        rec = {"model": "krea", "workflow": g.WORKFLOWS["krea"].name, "files": models, "comfyui": version, "seed": sd,
               "steps": 8, "strength": strength, "source": src.name,
               "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest(), "prompt": PROMPT, "prompt_id": pid,
               "seconds": round(time.time() - t, 1)}
        (d / f"{name}.json").write_text(json.dumps(rec, indent=1) + "\n")
        print(f"{name}: {rec['seconds']} s", flush=True)


# ------------------------------------------------------------------ fit ----------------------------
def picture(path: Path):
    """The model's picture at the render's size (linear) and its body: what differs from its background."""
    np = _np()
    from PIL import Image  # noqa: PLC0415
    from scipy import ndimage  # noqa: PLC0415
    W = sum(w for _, w in VIEWS)
    raw = np.asarray(Image.open(path).convert("RGB").resize((W, VH), Image.LANCZOS), np.float64)
    bg = np.median(np.concatenate([raw[:40].reshape(-1, 3), raw[:, :20].reshape(-1, 3)]), 0)
    fg = np.abs(raw - bg).max(-1) > 18
    fg = ndimage.binary_opening(fg, iterations=1)
    lab, n = ndimage.label(fg)
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    fg = np.isin(lab, 1 + np.nonzero(sizes > 2000)[0])
    return lin(raw / 255), ndimage.binary_fill_holes(fg)


def outline_moves(m, f):
    """For each pixel on hm08's outline ``m``: where the model's outline ``f`` is, along hm08's normal."""
    np = _np()
    from scipy.ndimage import binary_erosion, distance_transform_edt, gaussian_filter, map_coordinates  # noqa: PLC0415
    from scipy.spatial import cKDTree  # noqa: PLC0415
    sdf = distance_transform_edt(~f) - distance_transform_edt(f)        # > 0 outside the model's body
    ys, xs = np.nonzero(m & ~binary_erosion(m))
    g = gaussian_filter(m.astype(float), 2.0)
    gy, gx = np.gradient(g)
    n = -np.stack([gx[ys, xs], gy[ys, xs]], 1)
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)
    step = 0.5
    T = np.arange(-DMAX, DMAX + step, step)
    Sx = xs[:, None] + T[None] * n[:, :1]
    Sy = ys[:, None] + T[None] * n[:, 1:]
    s = map_coordinates(sdf, [Sy.ravel(), Sx.ravel()], order=1, mode="nearest").reshape(Sx.shape)
    cross = (s[:, :-1] <= 0) & (s[:, 1:] > 0)                            # inside → outside, going outward
    tc = T[:-1] + step * (-s[:, :-1]) / np.maximum(s[:, 1:] - s[:, :-1], 1e-9)
    tc = np.where(cross, tc, np.inf)
    t = tc[np.arange(len(tc)), np.argmin(np.abs(tc), 1)]
    ok = np.isfinite(t)
    mv = np.where(ok[:, None], t[:, None] * n, 0.0)
    # the contour's own median over 8 px: a match far from its neighbours' is another limb's outline
    tree = cKDTree(np.stack([xs, ys], 1))
    med = np.zeros_like(mv)
    for i, nb in enumerate(tree.query_ball_point(np.stack([xs, ys], 1), 8.0)):
        nb = [j for j in nb if ok[j]]
        med[i] = np.median(mv[nb], 0) if nb else 0
    ok &= np.linalg.norm(mv - med, axis=1) < 4.0
    return ys[ok], xs[ok], mv[ok], len(ys)


def relax(m, ys, xs, mv, eps=1e-4):
    """The displacement held on (``ys``, ``xs``), harmonic over the silhouette ``m`` (free at its other
    edges): one sparse solve per component."""
    np = _np()
    from scipy.sparse import coo_matrix  # noqa: PLC0415
    from scipy.sparse.linalg import splu  # noqa: PLC0415
    h, w = m.shape
    idx = -np.ones((h, w), np.int64)
    idx[m] = np.arange(m.sum())
    M = int(m.sum())
    fixed = np.zeros(M, bool)
    fixed[idx[ys, xs]] = True
    rows, cols, vals = [], [], []
    diag = np.full(M, eps)
    my, mx = np.nonzero(m)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        ny, nx = my + dy, mx + dx
        inb = (ny >= 0) & (ny < h) & (nx >= 0) & (nx < w)
        j = np.full(M, -1)
        j[inb] = idx[ny[inb], nx[inb]]
        has = j >= 0
        diag[has] += 1
        rows.append(np.nonzero(has)[0]); cols.append(j[has]); vals.append(-np.ones(has.sum()))
    r = np.concatenate(rows + [np.arange(M)]); c = np.concatenate(cols + [np.arange(M)])
    v = np.concatenate(vals + [diag])
    keep = ~fixed[r] | (r == c)
    v = np.where(fixed[r] & (r == c), 1.0, v)
    A = coo_matrix((v[keep], (r[keep], c[keep])), shape=(M, M)).tocsc()
    lu = splu(A)
    out = np.zeros((h, w, 2))
    for k in range(2):
        b = np.zeros(M)
        b[idx[ys, xs]] = mv[:, k]
        out[..., k][m] = lu.solve(b)
    return out


def cmd_fit(d: Path, pic_path: Path) -> None:
    np = _np()
    pic, fg = picture(pic_path)
    stem = pic_path.stem
    rec, warped = {"picture": pic_path.name, "dmax_px": DMAX, "views": {}}, np.full_like(pic, 0.18)
    fields = {}
    for yaw, x0, w in frames():
        g = np.load(d / f"geom_{yaw}.npz")
        m = g["mask"]
        f = fg[:, x0:x0 + w]
        ys, xs, mv, n_out = outline_moves(m, f)
        D = relax(m, ys, xs, mv)
        D = pushpull(D, m)                                            # carried past the outline for sampling
        fields[f"D_{yaw}"] = D.astype(np.float32)
        gy, gx = np.mgrid[0:VH, 0:w].astype(np.float64)
        sx, sy = gx + D[..., 0], gy + D[..., 1]
        fw = sample(f.astype(float), sx, sy) > 0.5
        part = sample(pic[:, x0:x0 + w], sx, sy)
        warped[:, x0:x0 + w][m] = part[m]
        det = (np.gradient(sx, axis=1) * np.gradient(sy, axis=0) - np.gradient(sx, axis=0) * np.gradient(sy, axis=1))[m]
        mm = 1000 / S
        rec["views"][str(yaw)] = {
            "outline_matched_pct": round(len(ys) / n_out * 100, 1),
            "bg_under_hm08_before_pct": round(float((m & ~f).sum() / m.sum() * 100), 2),
            "bg_under_hm08_after_pct": round(float((m & ~fw).sum() / m.sum() * 100), 2),
            "move_mm_median": round(float(np.median(np.hypot(*D[m].T)) * mm), 1),
            "move_mm_p99": round(float(np.percentile(np.hypot(*D[m].T), 99) * mm), 1),
            "folded_pct": round(float((det <= 0).mean() * 100), 3)}
        print(f"view {yaw:3d}: {json.dumps(rec['views'][str(yaw)])}", flush=True)
    np.savez(d / f"fit_{stem}.npz", **fields)
    save(d / f"fit_{stem}.png", warped)
    (d / f"fit_{stem}.json").write_text(json.dumps(rec, indent=1) + "\n")


# ------------------------------------------------------------------ put ----------------------------
INNER_JUMP = 0.03            # a depth step (m) between neighbouring pixels inside the silhouette: an occluding edge
INNER_PAD = 20               # pixels kept clear of it (~3.3 cm): where the model's limb edge sits, unfitted
                             # (10 left the profile's elbow edge as a crease on each side of the waist: 27.1 click 1)
CHIN_PAD = 6                 # ... and where the head is in front (the chin over the throat, the skull over the nape):
                             # the model's head is fitted by its outline and the head is Phase25's anyway; 20 px
                             # handed the throat to the profiles at a grazing angle (grey edge leaks: 27.2)


def inner_edges(g, head=None):
    """Pixels near a depth jump INSIDE hm08's silhouette in one view (an arm across the trunk, a leg behind
    the other). The fit moves only the outline, so the model's own limb edge there can sit a centimetre
    or two off hm08's and would paint a line onto the surface behind. ``head`` (the pixels showing the head
    island): a jump with the head in front keeps only ``CHIN_PAD`` clear."""
    np = _np()
    from scipy.ndimage import binary_dilation  # noqa: PLC0415
    z, m = g["z"], g["mask"]
    e, eh = np.zeros_like(m), np.zeros_like(m)
    zz = np.where(m, z, np.inf)
    for ax in (0, 1):
        z2 = np.roll(zz, 1, ax); m2 = np.roll(m, 1, ax)
        with np.errstate(invalid="ignore"):
            jump = m & m2 & (np.abs(np.where(m & m2, zz - z2, 0)) > INNER_JUMP)
        both = jump | np.roll(jump, -1, ax)
        if head is not None:                                      # the nearer of the two pixels is the head's
            near_is_head = np.where(zz <= z2, head, np.roll(head, 1, ax))
            hj = jump & near_is_head
            eh |= hj | np.roll(hj, -1, ax)
            both &= ~(hj | np.roll(hj, -1, ax))
        e |= both
    return binary_dilation(e, iterations=INNER_PAD) | (binary_dilation(eh, iterations=CHIN_PAD) if eh.any() else eh)


def sh9(n):
    """The nine second-order terms of a unit normal (a smooth light over directions)."""
    np = _np()
    x, y, z = n[:, 0], n[:, 1], n[:, 2]
    return np.stack([np.ones_like(x), x, y, z, x * y, y * z, x * z, x * x - y * y, 3 * z * z - 1], 1)


def cut_step(img, vmap, r: int = 6):
    """The level step where the source view changes: at each texel next to a texel from another view,
    the luminance of its own view's texels round it (``r`` px, ~5 mm at 2K) against the other view's,
    as |ratio - 1| in per cent (median, 90th percentile). Per-texel grain cancels in the local means."""
    np = _np()
    from scipy.ndimage import uniform_filter  # noqa: PLC0415
    lum = img @ np.array([0.2126, 0.7152, 0.0722])
    means = {}
    for v in range(len(VIEWS)):
        m = (vmap == v).astype(float)
        s = uniform_filter(lum * m, 2 * r + 1); c = uniform_filter(m, 2 * r + 1)
        means[v] = (s / np.maximum(c, 1e-9), c)
    ratios = []
    for a in range(len(VIEWS)):
        for b in range(len(VIEWS)):
            if a >= b:
                continue
            edge = (vmap == a) & (means[b][1] > 0.2) & (means[a][1] > 0.2)
            if edge.any():
                ratios.append(np.abs(means[a][0][edge] / np.maximum(means[b][0][edge], 1e-6) - 1))
    q = np.concatenate(ratios) if ratios else np.zeros(1)
    return {"median": round(float(np.median(q) * 100), 1), "p90": round(float(np.percentile(q, 90) * 100), 1)}


def seam_level(img, vmap, P, cell: int = 8, reach: float = 0.012, seam_w: float = 10.0, anchor: float = 1e-3):
    """Seam levelling (Lempitsky & Ivanov's seamless mosaicing): one smooth correction per view, in log
    colour, solved on ``cell``-pixel cells, so that where two views meet their levels agree, and the
    correction changes as little as possible elsewhere. Cells are neighbours by their distance ON THE
    BODY (``reach``, metres), not in the atlas: the body island's own cuts (down the spine, along the
    limbs) join pieces the atlas holds apart, and a field smooth only in the atlas steps across them.
    No pixel is mixed with another view's: each texel keeps its own view's detail; only a slow tone
    field moves it."""
    np = _np()
    from scipy.sparse import coo_matrix  # noqa: PLC0415
    from scipy.sparse.linalg import spsolve  # noqa: PLC0415
    from scipy.spatial import cKDTree  # noqa: PLC0415
    n = img.shape[0]
    hc = n // cell
    lg = np.log(np.maximum(img, 1e-4))
    keys, mean, cen, view = [], [], [], []
    for v in range(len(VIEWS)):
        m = (vmap == v)
        cnt = m.reshape(hc, cell, hc, cell).sum((1, 3))
        s = (lg * m[..., None]).reshape(hc, cell, hc, cell, 3).sum((1, 3))
        p = (P * m[..., None]).reshape(hc, cell, hc, cell, 3).sum((1, 3))
        for (i, j) in zip(*np.nonzero(cnt >= cell)):        # a cell with at least an eighth of its texels
            keys.append((v, i, j)); mean.append(s[i, j] / cnt[i, j]); cen.append(p[i, j] / cnt[i, j]); view.append(v)
    mean, cen, view = np.array(mean), np.array(cen), np.array(view)
    pairs = cKDTree(cen).query_pairs(reach, output_type="ndarray")
    a, b = pairs[:, 0], pairs[:, 1]
    same = view[a] == view[b]
    K = len(mean)
    E = len(a)
    w = np.where(same, 1.0, seam_w)
    rows = np.concatenate([np.arange(E), np.arange(E), E + np.arange(K)])
    cols = np.concatenate([a, b, np.arange(K)])
    vals = np.concatenate([w, -w, np.full(K, anchor)])
    A = coo_matrix((vals, (rows, cols)), shape=(E + K, K)).tocsr()
    rhs_seam = np.where(same[:, None], 0.0, mean[b] - mean[a]) * w[:, None]   # a seam pair: the levels agree
    bvec = np.concatenate([rhs_seam, np.zeros((K, 3))])
    nodes = {k: i for i, k in enumerate(keys)}
    AtA = (A.T @ A).tocsc()
    g = np.stack([spsolve(AtA, A.T @ bvec[:, c]) for c in range(3)], 1)
    raw_max = float(np.abs(g).max())
    g = np.clip(g, -LEVEL_CAP, LEVEL_CAP)
    from PIL import Image  # noqa: PLC0415
    out = img.copy()
    for v in range(len(VIEWS)):
        G = np.zeros((hc, hc, 3)); kn = np.zeros((hc, hc), bool)
        for (vv, i, j), k in nodes.items():
            if vv == v:
                G[i, j] = g[k]; kn[i, j] = True
        if not kn.any():
            continue
        G = pushpull(G, kn)
        up = np.stack([np.asarray(Image.fromarray(G[..., c].astype(np.float32), "F").resize((n, n), Image.BILINEAR))
                       for c in range(3)], -1)
        m = vmap == v
        out[m] = img[m] * np.exp(up[m])
    return out, raw_max



def hand_ids():
    """The two hands' island ids."""
    import gen_synth_skin as gss  # noqa: PLC0415
    import make_kits  # noqa: PLC0415
    _, names = named_islands(make_kits.load_mesh(gss.MESH))
    return [k for k, v in names.items() if v.startswith("hand_")]


def skin_islands(size: int):
    """The atlas of island ids at ``size``, the ids the four views paint (the body, both hands, both feet:
    the same picture on both sides of every wrist and ankle, so those seams cannot show, F-P27-2) and the
    head's id (Phase25's)."""
    np = _np()
    import gen_synth_skin as gss  # noqa: PLC0415
    import make_kits  # noqa: PLC0415
    m = make_kits.load_mesh(gss.MESH)
    ids = np.asarray(make_kits.island_ids_png(m, size), np.int32)
    _, names = named_islands(m)
    paint = [k for k, v in names.items() if v != "head"]
    return ids, paint, next(k for k, v in names.items() if v == "head")


def level_holes(C, sh, kn, skin, P, cell: int = 8, k: int = 8, sigma: float = 0.01):
    """A hole's level (D / C, in log colour) from its neighbours ON THE BODY: cell means of the known
    texels' log ratio, interpolated to each hole texel from its ``k`` nearest cells in 3D (a Gaussian of
    ``sigma`` metres past the nearest). An atlas-space fill steps wherever a hole runs along an island cut
    (the inner leg: both sides holes, far apart in the atlas; 27.2's seam instrument read 11 %)."""
    np = _np()
    from scipy.spatial import cKDTree  # noqa: PLC0415
    n = C.shape[0]
    hc = n // cell
    cl, cp = [], []
    for img, m in ((sh, skin & kn),):
        lr = np.log(np.maximum(img, 1e-4) / np.maximum(C, 1e-4))
        cnt = m.reshape(hc, cell, hc, cell).sum((1, 3))
        sl = (lr * m[..., None]).reshape(hc, cell, hc, cell, 3).sum((1, 3))
        sp = (P * m[..., None]).reshape(hc, cell, hc, cell, 3).sum((1, 3))
        ok = cnt >= cell
        cl.append(sl[ok] / cnt[ok][:, None]); cp.append(sp[ok] / cnt[ok][:, None])
    cl, cp = np.concatenate(cl), np.concatenate(cp)
    hole = skin & ~kn
    hr, hcc = np.nonzero(hole)
    dist, idx = cKDTree(cp).query(P[hr, hcc].astype(np.float64), k=k)
    w = np.exp(-(dist ** 2 - dist[:, :1] ** 2) / (2 * sigma ** 2))
    val = (cl[idx] * w[..., None]).sum(1) / w.sum(1, keepdims=True)
    out = np.zeros_like(C)
    out[hr, hcc] = np.exp(val)
    return out


def neck_join(D, body, H, hm, P, near: float = 0.004, r: float = 0.008, along: float = 0.04, label: str = "neck"):
    """The step where the picture's skin (``body``: the body and the nape it took) meets Phase25's head
    (``hm``), split between the two sides. The boundary is found ON THE BODY, not from UV seams: the head's
    texels within ``near`` metres of a painted texel. At each (every third), the head's mean log colour
    within ``r`` against the painted side's gives the step, smoothed along the boundary (the median within
    ``along``). Each side then takes half of it as a smooth tone ramp, full at the boundary and nothing
    ``NECK_R`` away (by the distance on the body). No pixel is mixed with another; the face is untouched.
    Returns the two log corrections (painted side, head) at the atlas's size, and a record."""
    np = _np()
    from scipy.spatial import cKDTree  # noqa: PLC0415
    br, bc = np.nonzero(body); hr, hc = np.nonzero(hm)
    Pb, Ph = P[br, bc], P[hr, hc]
    lb, lh = np.log(np.maximum(D[br, bc], 1e-4)), np.log(np.maximum(H[hr, hc], 1e-4))
    tb, th = cKDTree(Pb), cKDTree(Ph)
    dh = tb.query(Ph, distance_upper_bound=near)[0]
    pts = Ph[np.isfinite(dh)][::3]
    if not len(pts):
        raise SystemExit("the head and the painted skin do not meet")
    nb_b, nb_h = tb.query_ball_point(pts, r), th.query_ball_point(pts, r)
    delta = np.array([lh[h].mean(0) - lb[b].mean(0) for b, h in zip(nb_b, nb_h)])
    tree = cKDTree(pts)
    sm = np.array([np.median(delta[nb], 0) for nb in tree.query_ball_point(pts, along)])
    out = []
    for (rr, cc, Q), sign in (((br, bc, Pb), 0.5), ((hr, hc, Ph), -0.5)):
        g = np.zeros_like(D)
        dist, i = tree.query(Q)
        f = np.where(dist < NECK_R, 0.5 * (1 + np.cos(np.pi * np.minimum(dist / NECK_R, 1))), 0.0)
        g[rr, cc] = sign * sm[i] * f[:, None]
        out.append(g)
    rec = {"points": len(pts), "step_log_median": [round(float(v), 3) for v in np.median(sm, 0)],
           "step_log_p10": [round(float(v), 3) for v in np.percentile(sm, 10, 0)],
           "step_log_p90": [round(float(v), 3) for v in np.percentile(sm, 90, 0)], "ramp_m": NECK_R}
    print(f"{label} join: {json.dumps(rec)}", flush=True)
    return out, rec


def cmd_put(d: Path, pic_path: Path, tag: str, head: Path | None, use_fit: bool, delight: bool = False,
            levelled: bool = False, keep_colour: bool = False, light_order: int = 2) -> None:
    np = _np()
    from PIL import Image  # noqa: PLC0415
    import project_views as pv  # noqa: PLC0415
    from scipy.ndimage import binary_dilation  # noqa: PLC0415
    Image.MAX_IMAGE_PIXELS = None
    t = time.time()
    A = np.load(d / "atlas.npz")
    C, Pa, Na, groin = A["C"].astype(np.float64), A["P"], A["N"], A["groin"]
    ids2, paint_ids, head_id = skin_islands(2048)
    body = np.isin(ids2, paint_ids) & A["cover"]                     # the body, the hands and the feet
    hands = np.isin(ids2, hand_ids()) & A["cover"]
    if not HANDS_FROM_PICTURE:
        body &= ~hands
    base = (lin(np.asarray(Image.open(head).convert("RGB"), np.float64) / 255) if head else pv.subject_albedo())
    if base.shape[0] != 8192:
        raise SystemExit(f"the base atlas is {base.shape[0]}, not 8192")
    hm = (ids2 == head_id) & A["cover"]
    h8 = skin_islands(8192)[0] == head_id                         # the head's own texels only: the 8K
    cnt = h8.reshape(2048, 4, 2048, 4).sum((1, 3))                      # atlas beyond its edge is not the head
    H = (base * h8[..., None]).reshape(2048, 4, 2048, 4, 3).sum((1, 3)) / np.maximum(cnt, 1)[..., None]
    del h8
    hm &= cnt >= 8
    # the nape: the back half of the head island's neck ring is painted by the four views too. Phase25's field
    # stretches its picture there (a pale, streaked band below the skull, 27.2); RD-P25-16 left the neck to
    # the body. The join moves up onto the back of the skull, where Phase25's scalp is plain.
    from scipy.spatial import cKDTree  # noqa: PLC0415
    tb = cKDTree(Pa[body & (Pa[..., 1] > 0.5)][::4].astype(np.float64))
    dist = np.full(hm.shape, np.inf); dist[hm] = tb.query(Pa[hm].astype(np.float64), distance_upper_bound=NAPE_R)[0]
    zc = float(np.median(Pa[body & (Pa[..., 1] > 0.6)][:, 2]))        # the neck's middle, front to back
    nape = (hm & (dist < NAPE_R) & (Pa[..., 2] < zc + 0.01) & (np.abs(Pa[..., 0]) < NAPE_X) if head
            else np.zeros_like(hm))                                 # within the neck's width: never the ears
    body |= nape; hm &= ~nape
    pic, fg = picture(pic_path)
    F = np.load(d / f"fit_{pic_path.stem}.npz") if use_fit else None
    rr, cc = np.nonzero(body)
    X, Nn = Pa[rr, cc].astype(np.float64), Na[rr, cc].astype(np.float64)
    Nu = Nn / np.maximum(np.linalg.norm(Nn, axis=1, keepdims=True), 1e-9)
    got = np.zeros((len(rr), 3)); face = np.zeros(len(rr)); have = np.zeros(len(rr), bool)
    src = np.full(len(rr), -1)
    light = {}
    for k, (yaw, x0, w) in enumerate(frames()):
        g = np.load(d / f"geom_{yaw}.npz")
        px, py, z = proj(X, yaw, w)
        nz = (Nn @ rot(yaw).T)[:, 2]
        ix, iy = px - 0.5, py - 0.5                                   # index coordinates
        xi, yi = np.clip(np.round(ix).astype(int), 0, w - 1), np.clip(np.round(iy).astype(int), 0, VH - 1)
        vis = (z <= g["z"][yi, xi] + 0.004) & (nz > 0)
        uv = g["uv"]
        hpix = g["mask"] & (ids2[np.clip((uv[..., 1] * 2048).astype(int), 0, 2047),
                                 np.clip((uv[..., 0] * 2048).astype(int), 0, 2047)] == head_id)
        vis &= ~inner_edges(g, hpix)[yi, xi]    # one limb in front of another: the fit has no outline there
        if F is not None:
            Dv = F[f"D_{yaw}"]
            ix, iy = ix + sample(Dv[..., 0], ix, iy), iy + sample(Dv[..., 1], ix, iy)
        vis &= sample(fg[:, x0:x0 + w].astype(float), ix, iy) > 0.5
        col = np.zeros((len(rr), 3))
        col[vis] = sample(pic[:, x0:x0 + w], ix[vis], iy[vis])
        # the model's grey background, or an outline pixel half of it, is never skin (grey dots along the
        # shoulder in the judge, 27.2): a sample whose colour is nearly neutral is not seen
        chroma = (col.max(1) - col.min(1)) / np.maximum(col.max(1), 1e-6)
        vis &= chroma > MIN_CHROMA
        if delight:
            # the light the model painted into THIS view, as a smooth function of the surface's direction:
            # the picture over C, fitted with the terms of the normal up to ``light_order``, then divided out
            fitk = vis & (nz > 0.25)
            B = sh9(Nu)[:, :LIGHT_TERMS[light_order]]
            ratio_k = col[fitk] / np.maximum(C[rr[fitk], cc[fitk]], 1e-4)
            if keep_colour:
                # a grey light, from luminance alone: a light fitted per channel also divides out the picture's
                # own colour against C's (Tone34's orange, R/G 1.87 where the picture is 1.70; 27.2.5)
                Lk = col[fitk] @ np.asarray(LUM) / np.maximum(C[rr[fitk], cc[fitk]] @ np.asarray(LUM), 1e-4)
                coef = np.repeat(np.linalg.lstsq(B[fitk], Lk, rcond=None)[0][:, None], 3, 1)
            else:
                coef = np.linalg.lstsq(B[fitk], ratio_k, rcond=None)[0]
            L = np.maximum(B @ coef, LIGHT_FLOOR)   # at grazing normals the fit falls toward 0; never divide by it
            col[vis] = col[vis] / L[vis]
            light[str(yaw)] = {"min": [round(float(v), 3) for v in L[fitk].min(0)],
                               "max": [round(float(v), 3) for v in L[fitk].max(0)]}
        take = vis & (nz > face) & (nz > MIN_FACE)
        got[take] = col[take]; face[take] = nz[take]; have |= take; src[take] = k
    sh = np.zeros_like(C); kn = np.zeros(C.shape[:2], bool)
    sh[rr[have], cc[have]] = got[have]; kn[rr[have], cc[have]] = True
    vmap = np.full(C.shape[:2], -1); vmap[rr, cc] = src
    fmap = np.zeros(C.shape[:2], np.float32); fmap[rr, cc] = face
    np.savez_compressed(d / f"D_{tag}_source.npz", view=vmap.astype(np.int8), face=fmap)   # which view, how squarely
    step_before_gain = cut_step(sh, vmap)
    lev_max = None
    if levelled:
        sh, lev_max = seam_level(sh, vmap, Pa.astype(np.float64))
        step_before_gain = cut_step(sh, vmap)
    D = C.copy()
    # a hole (no view faces it squarely enough: between the legs, under the arms, the soles) is the maker's
    # skin at D's level round it ON THE BODY: C's own detail times D / C from the nearest known cells in 3D
    # C at 2K is the 8K map averaged without its island mask, so its outermost texels mix in the gutter (a thin
    # pale line along every cut where a hole sits on the rim, 27.2): its rim is taken from the island's inside
    from scipy.ndimage import binary_erosion  # noqa: PLC0415
    inner = binary_erosion(A["cover"], iterations=RIM)
    C = np.where((A["cover"] & ~inner)[..., None], pushpull(np.where(inner[..., None], C, 0.0), inner), C)
    ratio = level_holes(C, sh, kn, body, Pa.astype(np.float64))
    D[body] = np.where(kn[body][:, None], sh[body], C[body] * ratio[body])
    gain = C[body].mean(0) / D[body].mean(0)                          # the body held to C's mean
    if keep_colour:                                                   # ... in brightness only: the hue the picture's
        gain = np.full(3, (C[body].mean(0) @ np.asarray(LUM)) / (D[body].mean(0) @ np.asarray(LUM)))
    D[body] *= gain
    ring = binary_dilation(groin, iterations=6) & ~groin & body
    level = D[ring].mean(0) / C[ring].mean(0)
    D[groin] = C[groin] * level                                       # RD-P27-2: the maker's, at the level round it
    neck, neck_rec = None, None
    if head:                                                          # RD-P25-16: the neck was left to the body
        neck, neck_rec = neck_join(D, body, H, hm, Pa.astype(np.float64))
        D[body] *= np.exp(neck[0][body])
    hand_rec = None
    if not HANDS_FROM_PICTURE:                                        # the maker's hands, toned to the forearm
        g, hand_rec = neck_join(D, body, C, hands, Pa.astype(np.float64), label="wrist")
        D[body] *= np.exp(g[0][body])
        D[hands] = C[hands] * np.exp(g[1][hands])
        body = body | hands
    full = pushpull(np.where(body[..., None], D, 0.0), body)          # the island carried past its edge for 8K
    ids8, _, _ = skin_islands(8192)
    up = np.stack([np.asarray(Image.fromarray(full[..., c].astype(np.float32), "F").resize((8192, 8192), Image.BILINEAR))
                   for c in range(3)], -1)
    from scipy.ndimage import binary_dilation as dil  # noqa: PLC0415
    sel = np.isin(ids8, paint_ids)
    if nape.any():
        n8 = np.asarray(Image.fromarray(nape.astype(np.uint8) * 255).resize((8192, 8192), Image.NEAREST)) > 0
        n8 = dil(n8, iterations=GUTTER) & (ids8 == head_id)          # to the island's own edge (the 2K mask stops short)
        sel |= n8
        del n8
    out = base.astype(np.float32)
    # the painted colour also fills the atlas's gutter round it (texels in no island): a renderer filtering
    # across an island's edge otherwise reads the old colour there, a thin line on every seam (27.2)
    sel |= dil(sel, iterations=GUTTER) & (ids8 == 0)
    out[sel] = up[sel]
    if neck is not None:                                              # the head's share of the neck's step
        hsel = (ids8 == head_id) & ~sel                                # Phase25's own texels, not the nape painted here
        gh = pushpull(np.where(hm[..., None], neck[1], 0.0), hm)
        gh = np.stack([np.asarray(Image.fromarray(gh[..., c].astype(np.float32), "F").resize((8192, 8192),
                       Image.BILINEAR))[hsel] for c in range(3)], -1)
        out[hsel] *= np.exp(gh)
    del up, base
    Image.fromarray((srgb(out) * 255 + 0.5).astype(np.uint8)).save(d / f"D_{tag}.png")
    save(d / f"D_{tag}_2048.png", D)
    rec = {"picture": pic_path.name, "fit": use_fit, "delight": delight, "light": light, "levelled": levelled,
           "keep_colour": keep_colour, "light_order": light_order,
           "level_log_max": None if lev_max is None else round(lev_max, 3),
           "cut_step_pct_median": step_before_gain["median"], "cut_step_pct_p90": step_before_gain["p90"],
           "head": head.name if head else None, "neck_join": neck_rec, "wrist_join": hand_rec, "nape_texels": int(nape.sum()),
           "seen_pct": round(float(have.mean() * 100), 1),
           "grazing_under_0.3_pct": round(float((have & (face < 0.3)).mean() * 100), 1),
           "gain": [round(float(v), 3) for v in gain], "groin_level": [round(float(v), 3) for v in level],
           "seconds": round(time.time() - t)}
    (d / f"D_{tag}.json").write_text(json.dumps(rec, indent=1) + "\n")
    print(f"D_{tag}.png: {json.dumps(rec)}")


# ------------------------------------------------------------------ the fine skin ------------------
# RD-P27-6 (the lead, Pass 3: "3 looks more real, marks are right"): the four views are 1.67 mm a pixel, too
# coarse for the skin itself, and a close camera repainting a region redraws the body's marks (F-P27-18). So
# the skin is split by size: coarser than CLOSE_SPLIT_M it is D's (the four views), finer it comes from one
# close camera per region, as a ratio on D. Every region's level is D's, so regions cannot step.
CLOSE_SIZE = 1536             # each close picture's side, in pixels
CLOSE_M = 0.6                 # ... and in metres (0.39 mm a pixel)
CLOSE_STEP = 0.5              # tile spacing (m): 0.1 m of overlap
CLOSE_MIN_SHARE = 0.08        # a tile showing less of the body than this is dropped
CLOSE_STRENGTH = 0.65         # RD-P27-6: the lead's "3"
CLOSE_SPLIT_M = 0.002         # the split (F-P27-18: at 5 mm the marks begin to move; 3 mm still printed a
                             # breast fold the model drew lower, 27.2.3)
CLOSE_ERODE = 6               # pixels kept clear of a close picture's outline
CLOSE_SOFT = 0.08             # the fine skin's log ratio, soft-capped (tanh): the grain varies by a few per cent;
                             # an edge of a feature the model drew elsewhere (a breast fold, a nipple, a blade's
                             # crease) is a 20-50 % jump, and uncapped it printed as a second contour (27.2.3)
CLOSE_PROMPT = ("A close-up photograph of the bare {part} of a real young woman about twenty, seen {side}, with a "
                "completely hairless body, light warm skin between Fitzpatrick III and IV. Real unretouched skin "
                "filling the frame: visible pores, fine vellus hair, small blemishes, tiny moles, faint freckles, "
                "uneven tone. Even, soft, shadowless studio light on a plain grey background. Not a 3D render, not "
                "CGI, not painted.")


def close_part(yaw: int, cx: float, cy: float) -> tuple[str, str]:
    side = {0: "from the front", 180: "from directly behind"}.get(yaw, "from her side")
    if abs(cx) > 0.3 and cy > -0.1:
        part = "arm"
    elif cy > 0.3:
        part = "shoulders and upper torso"
    elif cy > 0.0:
        part = "waist and lower torso"
    elif cy > -0.4:
        part = "hips and thighs"
    else:
        part = "lower legs and feet"
    return part, side


def close_raster(P, vt, T, vn, c: dict):
    """hm08 through one close camera ``c`` (yaw, cx: across the view, cy: height, both metres)."""
    np = _np()
    s = CLOSE_SIZE / CLOSE_M
    R = rot(c["yaw"])
    keep = proj.__defaults__
    proj.__defaults__ = (CLOSE_SIZE, s, c["cy"])
    try:
        return raster(P - c["cx"] * R[0], vt, T, vn, c["yaw"], CLOSE_SIZE, CLOSE_SIZE)
    finally:
        proj.__defaults__ = keep


def close_render(g, A):
    """An 8K atlas (linear) worn through camera geometry ``g``, under the soft key, the raster's one-pixel
    cracks filled (Krea keeps them as a thin line, F-P27-17)."""
    np = _np()
    from scipy.ndimage import binary_closing  # noqa: PLC0415
    m = g["mask"]; n = A.shape[0]
    col = sample(A, g["uv"][..., 0] * n - 0.5, g["uv"][..., 1] * n - 0.5) * shade(g["n"])[..., None]
    col = pushpull(np.where(m[..., None], col, 0.0), m)
    return np.where(binary_closing(m, iterations=2)[..., None], col, 0.18)


def cmd_close_prep(d: Path, atlas: Path) -> None:
    """Lay the close cameras over the body and the feet, and render each wearing ``atlas`` (D)."""
    np = _np()
    from PIL import Image  # noqa: PLC0415
    Image.MAX_IMAGE_PIXELS = None
    t = time.time()
    out = d / "close"; out.mkdir(parents=True, exist_ok=True)
    A = lin(np.asarray(Image.open(atlas).convert("RGB"), np.float32) / 255)
    P, vt, T, vn = mesh()
    ids, paint_ids, _ = skin_islands(2048)
    hand = set(hand_ids())
    want = [k for k in paint_ids if HANDS_FROM_PICTURE or k not in hand]
    tri_uv = vt[T[:, :, 1]].mean(1)
    tid = ids[np.clip(((1 - tri_uv[:, 1]) * 2048).astype(int), 0, 2047), np.clip((tri_uv[:, 0] * 2048).astype(int), 0, 2047)]
    Tb = T[np.isin(tid, want)]
    cams = []
    for yaw in (0, 90, 180, 270):
        V = P[np.unique(Tb[:, :, 0])] @ rot(yaw).T
        x0, x1, y0, y1 = V[:, 0].min(), V[:, 0].max(), V[:, 1].min(), V[:, 1].max()
        nx = max(1, int(np.ceil((x1 - x0 - CLOSE_M) / CLOSE_STEP)) + 1)
        ny = max(1, int(np.ceil((y1 - y0 - CLOSE_M) / CLOSE_STEP)) + 1)
        for i in range(nx):
            for j in range(ny):
                cx = (x0 + x1) / 2 + (i - (nx - 1) / 2) * CLOSE_STEP
                cy = (y0 + y1) / 2 + (j - (ny - 1) / 2) * CLOSE_STEP
                c = {"yaw": yaw, "cx": round(float(cx), 3), "cy": round(float(cy), 3)}
                g = close_raster(P, vt, T, vn, c)                  # the whole mesh: what is in front, occludes
                uv = g["uv"]
                pid = ids[np.clip((uv[..., 1] * 2048).astype(int), 0, 2047), np.clip((uv[..., 0] * 2048).astype(int), 0, 2047)]
                share = float((g["mask"] & np.isin(pid, want)).mean())
                if share < CLOSE_MIN_SHARE:
                    continue
                c["name"] = f"c{yaw:03d}_{len([k for k in cams if k['yaw'] == yaw]):02d}"
                c["part"], c["side"] = close_part(yaw, c["cx"], c["cy"])
                c["share"] = round(share, 3)
                np.savez(out / f"geom_{c['name']}.npz", **g)
                save(out / f"in_{c['name']}.png", close_render(g, A))
                cams.append(c)
                print(f"{c['name']}: {c['part']}, {c['side']}, body {share * 100:.0f} %", flush=True)
    (out / "cams.json").write_text(json.dumps({"atlas": atlas.name, "metres": CLOSE_M, "size": CLOSE_SIZE,
                                               "cams": cams}, indent=1) + "\n")
    print(f"{len(cams)} close cameras; {time.time() - t:.0f} s")


def cmd_close_paint(d: Path, seed: int, strength: float, server: str) -> None:
    import gen_views_model as g  # noqa: PLC0415
    out = d / "close"
    cams = json.loads((out / "cams.json").read_text())["cams"]
    graph = json.loads(g.WORKFLOWS["krea"].read_text(encoding="utf-8"))
    version = json.loads(g._call(server, "/system_stats"))["system"]["comfyui_version"]
    for c in cams:
        name = f"{c['name']}_s{round(strength * 100):02d}_seed{seed}"
        if (out / f"{name}.png").exists():
            continue
        t = time.time()
        src = out / f"in_{c['name']}.png"
        prompt = CLOSE_PROMPT.format(part=c["part"], side=c["side"])
        vals = {"IMAGE": g.upload(server, src), "PROMPT": prompt, "SEED": seed, "STEPS": 8, "STRENGTH": strength,
                "PREFIX": "matter_p27close"}
        png, pid = g.run(server, g.fill(graph, vals))
        (out / f"{name}.png").write_bytes(png)
        rec = {"model": "krea", "workflow": g.WORKFLOWS["krea"].name, "comfyui": version, "seed": seed, "steps": 8,
               "strength": strength, "source": src.name, "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
               "prompt": prompt, "prompt_id": pid, "seconds": round(time.time() - t, 1)}
        (out / f"{name}.json").write_text(json.dumps(rec, indent=1) + "\n")
        print(f"{name}: {rec['seconds']} s", flush=True)


def _gblur(img, m, sig):
    np = _np()
    from scipy.ndimage import gaussian_filter  # noqa: PLC0415
    w = gaussian_filter(m.astype(np.float64), sig)
    return np.stack([gaussian_filter(img[..., k] * m, sig) for k in range(3)], -1) / np.maximum(w, 1e-6)[..., None]


def cmd_close_put(d: Path, atlas: Path, tag: str, seed: int, strength: float) -> None:
    """The fine skin onto ``atlas`` (D at 8K): each body and foot texel takes the ratio of the close picture
    facing it most squarely to its own blur at ``CLOSE_SPLIT_M`` (above it the colour stays D's), at 2K,
    carried to the 8K atlas's texels and gutter. The groin keeps the maker's skin (RD-P27-2)."""
    np = _np()
    from PIL import Image  # noqa: PLC0415
    from scipy.ndimage import binary_erosion, binary_dilation, gaussian_filter  # noqa: PLC0415
    Image.MAX_IMAGE_PIXELS = None
    t = time.time()
    out = d / "close"
    cams = json.loads((out / "cams.json").read_text())["cams"]
    A = np.load(d / "atlas.npz")
    Pa, Na, groin = A["P"].astype(np.float64), A["N"].astype(np.float64), A["groin"]
    ids2, paint_ids, head_id = skin_islands(2048)
    hand = set(hand_ids())
    want = [k for k in paint_ids if HANDS_FROM_PICTURE or k not in hand]
    skin = np.isin(ids2, want) & A["cover"] & ~binary_dilation(groin, iterations=4)
    rr, cc = np.nonzero(skin)
    X, Nn = Pa[rr, cc], Na[rr, cc]
    best = np.zeros(len(rr)); lr = np.zeros((len(rr), 3)); src = np.full(len(rr), -1)
    s = CLOSE_SIZE / CLOSE_M
    for k, c in enumerate(cams):
        g = dict(np.load(out / f"geom_{c['name']}.npz"))
        pic = picture_close(out / f"{c['name']}_s{round(strength * 100):02d}_seed{seed}.png")
        uv = g["uv"]
        hpix = g["mask"] & (ids2[np.clip((uv[..., 1] * 2048).astype(int), 0, 2047),
                                 np.clip((uv[..., 0] * 2048).astype(int), 0, 2047)] == head_id)
        m = binary_erosion(g["mask"], iterations=CLOSE_ERODE) & ~inner_edges(g, hpix)
        e = 4 * CLOSE_ERODE                                              # the frame's edge too
        m[:e] = m[-e:] = False; m[:, :e] = m[:, -e:] = False
        chroma = (pic.max(-1) - pic.min(-1)) / np.maximum(pic.max(-1), 1e-6)
        m &= chroma > MIN_CHROMA                                         # never the model's grey background
        raw = srgb(pic) * 255                                            # nor near the model's own outline, where
        bg = np.median(np.concatenate([raw[:40].reshape(-1, 3), raw[-40:].reshape(-1, 3)]), 0)   # it moved a limb:
        fg = np.abs(raw - bg).max(-1) > 18                               # its edge is a fine line (27.2)
        m &= binary_erosion(fg, iterations=2 * CLOSE_ERODE)
        lrat = np.log(np.maximum(pic, 1e-4)) - np.log(np.maximum(_gblur(pic, m, CLOSE_SPLIT_M * s), 1e-4))
        lrat = CLOSE_SOFT * np.tanh(lrat / CLOSE_SOFT)
        lrat = np.stack([gaussian_filter(lrat[..., j] * m, 0.8) for j in range(3)], -1) / np.maximum(
            gaussian_filter(m.astype(float), 0.8), 1e-6)[..., None]          # to the 2K texel, not aliased
        keep = proj.__defaults__
        proj.__defaults__ = (CLOSE_SIZE, s, c["cy"])
        try:
            px, py, z = proj(X - c["cx"] * rot(c["yaw"])[0], c["yaw"], CLOSE_SIZE, CLOSE_SIZE)
        finally:
            proj.__defaults__ = keep
        nz = (Nn @ rot(c["yaw"]).T)[:, 2] / np.maximum(np.linalg.norm(Nn, axis=1), 1e-9)
        xi, yi = np.floor(px).astype(int), np.floor(py).astype(int)
        inb = (xi >= 0) & (yi >= 0) & (xi < CLOSE_SIZE) & (yi < CLOSE_SIZE)
        ok = np.zeros(len(rr), bool)
        ok[inb] = m[yi[inb], xi[inb]] & (np.abs(z[inb] - g["z"][yi[inb], xi[inb]]) < 0.004)
        take = ok & (nz > MIN_FACE) & (nz > best)
        lr[take] = sample(lrat, px[take] - 0.5, py[take] - 0.5)
        best[take] = nz[take]; src[take] = k
    got = src >= 0
    L = np.zeros((2048, 2048, 3)); known = A["cover"].copy()
    L[rr[got], cc[got]] = lr[got]                                    # 0 (D's own) on every other texel
    L = pushpull(np.where(known[..., None], L, 0.0), known)         # into the gutter
    base = lin(np.asarray(Image.open(atlas).convert("RGB"), np.float32) / 255).astype(np.float32)
    ids8, _, _ = skin_islands(8192)
    sel = np.isin(ids8, want)
    sel |= binary_dilation(sel, iterations=GUTTER) & (ids8 == 0)
    up = np.stack([np.asarray(Image.fromarray(L[..., j].astype(np.float32), "F").resize((8192, 8192), Image.BILINEAR))
                   for j in range(3)], -1)
    base[sel] *= np.exp(up[sel])
    del up
    Image.fromarray((srgb(base) * 255 + 0.5).astype(np.uint8)).save(d / f"D_{tag}.png")
    srcmap = np.full((2048, 2048), -1, np.int16); srcmap[rr, cc] = src
    np.savez_compressed(d / f"D_{tag}_close.npz", cam=srcmap)
    rec = {"atlas": atlas.name, "cams": len(cams), "strength": strength, "seed": seed, "split_m": CLOSE_SPLIT_M,
           "skin_texels": int(len(rr)), "fine_pct": round(float(got.mean() * 100), 1),
           "ratio_std": [round(float(v), 4) for v in lr[got].std(0)], "seconds": round(time.time() - t)}
    (d / f"D_{tag}.json").write_text(json.dumps(rec, indent=1) + "\n")
    print(f"D_{tag}.png: {json.dumps(rec)}")


def picture_close(path: Path):
    """A close picture at the camera's size, linear."""
    np = _np()
    from PIL import Image  # noqa: PLC0415
    raw = np.asarray(Image.open(path).convert("RGB").resize((CLOSE_SIZE, CLOSE_SIZE), Image.LANCZOS), np.float64)
    return lin(raw / 255)


# ------------------------------------------------------------------ seams --------------------------
def named_islands(m):
    """Each face's island and the names of the islands a body seam joins: body, head, hand_l/r, foot_l/r
    (hm08's own faces, F-P27-1; left is +x)."""
    np = _np()
    import make_kits  # noqa: PLC0415
    isl = np.array(make_kits.islands(m))
    pts = np.asarray(m["points"], float)
    cen = {}
    for k in np.unique(isl):
        fi = np.nonzero(isl == k)[0]
        v = np.array([pts[a] for f in fi for a, _ in m["faces"][f]])
        cen[int(k)] = (len(fi), v.mean(0))
    body = max(cen, key=lambda k: cen[k][0])
    big = sorted((k for k in cen if k != body), key=lambda k: -cen[k][0])[:5]
    names = {body: "body"}
    head = max(big, key=lambda k: cen[k][1][1])
    names[head] = "head"
    rest = [k for k in big if k != head]
    feet = sorted(rest, key=lambda k: cen[k][1][1])[:2]
    for k in rest:
        side = "l" if cen[k][1][0] > 0 else "r"
        names[k] = ("foot_" if k in feet else "hand_") + side
    return isl, names


def seam_edges(m, isl):
    """Every mesh edge whose two faces carry different UVs: (island a, island b, face a, face b, the
    edge's uv indices on each side, its length in metres, its midpoint)."""
    np = _np()
    from collections import defaultdict  # noqa: PLC0415
    pts = np.asarray(m["points"], float)
    edge = defaultdict(list)
    for fi, f in enumerate(m["faces"]):
        n = len(f)
        for k in range(n):
            (a, ua), (b, ub) = f[k], f[(k + 1) % n]
            key, uvs = ((a, b), (ua, ub)) if a < b else ((b, a), (ub, ua))
            edge[key].append((fi, uvs))
    out = []
    for (a, b), lst in edge.items():
        if len(lst) == 2 and lst[0][1] != lst[1][1]:
            (f0, u0), (f1, u1) = lst
            out.append((int(isl[f0]), int(isl[f1]), f0, f1, u0, u1, float(np.linalg.norm(pts[a] - pts[b])),
                        (pts[a] + pts[b]) / 2))
    return out


def body_part(p) -> str:
    """Where on the body a point of the body island's own cut lies (the probe's ``seams.py`` buckets)."""
    x, y, z = p
    if y > 0.35 and abs(x) > 0.17:
        return "arm"
    if y < -0.05 and abs(x) > 0.02:
        return "leg"
    return "back" if z < 0 else "front"


def cmd_seams(atlas: Path, off_mm: float = 3.0, r_mm: float = 2.0) -> dict:
    """The level step across each of hm08's seams on an atlas: at three points along every seam edge, the
    mean luminance ``off_mm`` inside each side (a disc of ``r_mm``, that side's island only), as
    |ratio - 1| in per cent, length-weighted, per seam, beside its control: the same spacing on ONE side
    (``same_side``), the skin's own variation. A seam shows where the step beats its control. ``cut:*`` is the body island's own cut (down
    the spine and the back of the neck, along the arms and legs, on the front of the trunk). A step
    the eye finds is a level step; a seam with the same picture on both sides reads ~0 (F-P27-2)."""
    np = _np()
    from PIL import Image  # noqa: PLC0415
    from scipy.ndimage import map_coordinates, uniform_filter  # noqa: PLC0415
    import gen_synth_skin as gss  # noqa: PLC0415
    import make_kits  # noqa: PLC0415
    Image.MAX_IMAGE_PIXELS = None
    m = make_kits.load_mesh(gss.MESH)
    isl, names = named_islands(m)
    img = lin(np.asarray(Image.open(atlas).convert("RGB"), np.float32) / 255)
    n = img.shape[0]
    lum = (img @ np.array([0.2126, 0.7152, 0.0722], np.float32)).astype(np.float32)
    del img
    ids = np.asarray(make_kits.island_ids_png(m, n), np.int32)
    tpm = n / 1.69                     # texels a metre at the atlas's median (F-P27-4)
    off, r = off_mm / 1000 * tpm, max(1, int(r_mm / 1000 * tpm))
    means = {}
    for k in names:
        msk = (ids == k).astype(np.float32)
        means[k] = (uniform_filter(lum * msk, 2 * r + 1), uniform_filter(msk, 2 * r + 1))
    vt = np.asarray(m["vt"], float)
    cent = {}
    rows = {}
    for ia, ib, fa, fb, ua, ub, L, mid in seam_edges(m, isl):
        if ia not in names or ib not in names or "body" not in (names[ia], names[ib]):
            continue
        key = ("cut:" + body_part(mid)) if ia == ib else "-".join(sorted((names[ia], names[ib])))
        vals, ctrl = [], []
        for t in (0.25, 0.5, 0.75):
            side, far = [], []
            for k, f, (u0, u1) in ((ia, fa, ua), (ib, fb, ub)):
                if f not in cent:
                    cent[f] = vt[[t_ for _, t_ in m["faces"][f]]].mean(0)
                p = vt[u0] + t * (vt[u1] - vt[u0])
                e = vt[u1] - vt[u0]
                d = cent[f] - p
                d -= e * (d @ e) / max(e @ e, 1e-12)
                for o, dst in ((off, side), (3 * off, far)):   # far: the control, 2 x off from ``side``
                    q = p + d / max(np.linalg.norm(d), 1e-12) * o / n
                    y, x = (1 - q[1]) * n - 0.5, q[0] * n - 0.5
                    s, c = (map_coordinates(a, [[y], [x]], order=1)[0] for a in means[k])
                    dst.append(s / c if c > 0.3 else np.nan)
            vals.append(abs(side[0] / side[1] - 1) if np.all(np.isfinite(side)) else np.nan)
            cc = [abs(a / b - 1) for a, b in zip(side, far) if np.isfinite(a) and np.isfinite(b)]
            ctrl.append(np.mean(cc) if cc else np.nan)
        v, cv = np.array(vals), np.array(ctrl)
        v, cv = v[np.isfinite(v)], cv[np.isfinite(cv)]
        if len(v) and len(cv):
            rows.setdefault(key, []).append((float(v.mean()), L, float(cv.mean())))
    out = {}
    for key, lst in sorted(rows.items()):
        w = np.array([b for _, b, _ in lst])

        def wq(q, f):
            o = np.argsort(q); cw = np.cumsum(w[o]) / w.sum()
            return round(float(q[o][min(np.searchsorted(cw, f), len(q) - 1)] * 100), 1)
        q, qc = np.array([a for a, _, _ in lst]), np.array([c for _, _, c in lst])
        out[key] = {"m": round(float(w.sum()), 2), "median_pct": wq(q, 0.5), "p90_pct": wq(q, 0.9),
                    "same_side_median_pct": wq(qc, 0.5), "same_side_p90_pct": wq(qc, 0.9)}
        print(f"{key:14s} {json.dumps(out[key])}", flush=True)
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("prep"); s.add_argument("dir", type=Path)
    s = sub.add_parser("paint"); s.add_argument("dir", type=Path); s.add_argument("--seeds", default="7")
    s.add_argument("--strength", type=float, default=0.5); s.add_argument("--server", default="http://127.0.0.1:8188")
    s = sub.add_parser("fit"); s.add_argument("dir", type=Path); s.add_argument("picture")
    s = sub.add_parser("put"); s.add_argument("dir", type=Path); s.add_argument("picture"); s.add_argument("tag")
    s.add_argument("--head", type=Path, help="an 8K atlas (Phase25's D) the body is written onto; default C")
    s.add_argument("--no-fit", action="store_true", help="project the picture as painted (Pass 2's f4_50)")
    s.add_argument("--delight", action="store_true",
                   help="divide out the light the model painted into each view (a smooth function of the normal)")
    s.add_argument("--level", action="store_true",
                   help="seam levelling: a smooth tone correction per view so the views agree where they meet")
    s.add_argument("--keep-colour", action="store_true",
                   help="keep the picture's own colour: a grey light (from luminance) and the body held to C's "
                        "brightness only, not its hue (27.2.5)")
    s.add_argument("--light-order", type=int, choices=(0, 1, 2), default=2,
                   help="the light's terms of the normal (``--delight``): 2 also takes out curvature shading")
    s = sub.add_parser("seams", help="the level step across each seam of an atlas (neck, wrists, ankles, spine)")
    s.add_argument("atlas", type=Path)
    s = sub.add_parser("close", help="the fine skin from one close camera per region (RD-P27-6): prep, paint, put")
    s.add_argument("stage", choices=("prep", "paint", "put")); s.add_argument("dir", type=Path)
    s.add_argument("--atlas", type=Path, help="D at 8K (prep: what the cameras render; put: what the skin goes on)")
    s.add_argument("--tag", default="close"); s.add_argument("--seed", type=int, default=7)
    s.add_argument("--strength", type=float, default=CLOSE_STRENGTH); s.add_argument("--server", default="http://127.0.0.1:8188")
    a = ap.parse_args(argv)
    if a.cmd == "close":
        if a.stage == "prep":
            cmd_close_prep(a.dir, a.atlas)
        elif a.stage == "paint":
            cmd_close_paint(a.dir, a.seed, a.strength, a.server)
        else:
            cmd_close_put(a.dir, a.atlas, a.tag, a.seed, a.strength)
    elif a.cmd == "seams":
        cmd_seams(a.atlas)
    elif a.cmd == "prep":
        cmd_prep(a.dir)
    elif a.cmd == "paint":
        cmd_paint(a.dir, [int(x) for x in a.seeds.split(",")], a.strength, a.server)
    elif a.cmd == "fit":
        cmd_fit(a.dir, a.dir / a.picture)
    elif a.cmd == "put":
        cmd_put(a.dir, a.dir / a.picture, a.tag, a.head, not a.no_fit, a.delight, a.level, a.keep_colour, a.light_order)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
