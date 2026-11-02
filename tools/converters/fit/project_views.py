#!/usr/bin/env python3
"""Project an image model's pictures of hm08's head onto a skin subject's atlas (Phase25, RD-P25-1 … 8).

    uv run tools/converters/fit/project_views.py render <dir> <view>[,<view>…] [--albedo <tag>]
    uv run tools/converters/fit/project_views.py bake   <dir> <tag> <view>[,<view>…] [--picture]

The head is rendered from fixed cameras (``VIEWS``) with the subject's colour (``Tone34`` as served,
or an albedo baked so far), an image model repaints each render as a photographed person
(``gen_views_model.py``, through ComfyUI), and ``bake`` projects those pictures back onto the
subject's atlas at its own size (8192 for ``Tone34``):

* each texel of the head is looked up in every picture that sees it squarely (a z-buffer test, kept
  away from the silhouette and the eye openings), weighted by cos⁴ of its angle to the camera and by
  the picture's pixels per millimetre (a close camera outweighs a far one where both see);
* the picture's albedo is its colour over the render's own light;
* **masks** keep the model's brows, lid lines and lips out (F-AIS-13, RD-P25-2): there, and below the
  neck, the subject's own colour stays (RD-P25-1);
* the baked head is held to the subject's face-core average (MPFB's face mask over 0.9, as
  ``gen_skin_maps.subject`` holds it), so D sits at the subject's tone like C;
* it is feathered into the subject's colour over the neck.

Everything is written under ``<dir>`` (git-ignored ``library/parity/P25_*`` by convention): the
renders ``in_<view>_<tag>.png`` (the model's pictures come back as ``view_<view>_<tag>.png``), the geometry ``geom_<view>.npz``, the albedo ``albedo_<tag>.npy``
and, with ``--picture``, ``D_<tag>.png`` (linear albedo, sRGB-encoded, drawn with constant 1:
``look.py --candidate``). NumPy only; the model runs elsewhere (RD-P25-7).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

SUBJECT = "Tone34"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))
import gen_synth_skin as _gss0  # noqa: E402  (only for SUBJECTS; the size is set below)

if os.environ.get("MATTER_SKIN_N") is None and __name__ == "__main__":   # the subject's own size, before the maker reads it
    os.environ["MATTER_SKIN_N"] = str(_gss0.SUBJECTS[SUBJECT]["size"])
    os.execvpe(sys.executable, [sys.executable, str(Path(__file__).resolve()), *sys.argv[1:]], os.environ)

import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402

import gen_skin_maps as gsm  # noqa: E402
import gen_synth_skin as gss  # noqa: E402
import make_kits  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
W = 2048                          # FLUX.2 [klein]'s largest square (4 MP), RD-P25-4
FOV = 24.0
TARGET = np.array([0.0, 0.715, 0.03])
HEAD_Y = 0.50                     # the head region: every texel and triangle above this height (m)
NECK = (0.50, 0.56)               # the model's colour fades in over this height (m): the neck join
EYE_MM = 4.0                      # kept clear around each eye opening (the model paints eyes larger)
EDGE_MM = 2.0                     # kept clear inside the silhouette
POW = 4.0
IOU_MIN = 0.95                    # the overlay gate: painted head over the render's silhouette
NECK_R = 60                       # the neck match's breadth (pixels at 2048)
NECK_MATCH = (0.53, 0.60)         # D's broad level eases onto C's below the top of this band (m)
FILL_R = 20                       # the masked brows' and lids' fill reaches this far (pixels at 2048)

# The cameras (RD-P25-4): the spike's five at 0.78 m, then three close ones on the face at 0.45 m.
# ``words`` is what the prompt says of the angle. Order is the progressive order (F-AIS-12).
VIEWS = {
    "f000": {"yaw": 0, "pitch": 5, "dist": 0.78, "words": "seen straight from the front"},
    "f-40": {"yaw": -40, "pitch": 5, "dist": 0.78, "words": "seen in three-quarter view, turned to the right"},
    "f+40": {"yaw": 40, "pitch": 5, "dist": 0.78, "words": "seen in three-quarter view, turned to the left"},
    "f-80": {"yaw": -80, "pitch": 5, "dist": 0.78, "words": "seen in right profile"},
    "f+80": {"yaw": 80, "pitch": 5, "dist": 0.78, "words": "seen in left profile"},
    "c000": {"yaw": 0, "pitch": 3, "dist": 0.45, "words": "a close-up of the face seen straight from the front"},
    "c-35": {"yaw": -35, "pitch": 3, "dist": 0.45, "words": "a close-up of the face in three-quarter view, turned to the right"},
    "c+35": {"yaw": 35, "pitch": 3, "dist": 0.45, "words": "a close-up of the face in three-quarter view, turned to the left"},
}


def mm_per_px(v: dict) -> float:
    return 2 * v["dist"] * np.tan(np.radians(FOV) / 2) / W * 1000


def srgb_to_lin(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def lin_to_srgb(x):
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


C_DIR = gsm.REPO / "library" / "parity" / "P25_C"


def subject_map() -> Path:
    """C's map: the maker's own, with no outside field. Since Phase25 25.3 the served map is D (the image
    model's face as a structure), so C is remade beside it, never read from the library (git-ignored)."""
    p = C_DIR / f"Skin{SUBJECT}_basecolor_{gsm.TAG}.png"
    if not p.is_file():
        raise SystemExit(f"{p} missing: make C with `uv run tools/converters/fit/gen_skin_maps.py "
                         f"--subject {SUBJECT} --out {C_DIR.relative_to(gsm.REPO)}`")
    return p


def subject_albedo() -> np.ndarray:
    """C's rendered albedo (linear): the maker's own map decoded times its ``base_color_const``."""
    c = np.array(json.loads((C_DIR / f"Skin{SUBJECT}_basecolor_stats.json").read_text())["base_color_const"], np.float32)
    m = np.asarray(Image.open(subject_map()).convert("RGB"))
    lut = srgb_to_lin(np.arange(256) / 255.0).astype(np.float32)
    return lut[m] * c


# ------------------------------------------------------------------ the camera and the renderer --
def camera(v: dict) -> dict:
    y, p = np.radians(v["yaw"]), np.radians(v["pitch"])
    C = TARGET + v["dist"] * np.array([np.sin(y) * np.cos(p), np.sin(p), np.cos(y) * np.cos(p)])
    f = TARGET - C
    f /= np.linalg.norm(f)
    r = np.cross(f, [0, 1, 0]); r /= np.linalg.norm(r)
    u = np.cross(r, f)
    return {"C": C, "R": np.stack([r, u, f]), "fpx": (W / 2) / np.tan(np.radians(FOV) / 2)}


def project(cam, X):
    Xc = (X - cam["C"]) @ cam["R"].T
    z = Xc[..., 2]
    return W / 2 + cam["fpx"] * Xc[..., 0] / z, W / 2 - cam["fpx"] * Xc[..., 1] / z, z


def head_mesh():
    m = make_kits.load_mesh(gss.MESH)
    P = np.array(m["points"], np.float64)
    vt = np.array(m["vt"], np.float64)
    tris = []
    for f in m["faces"]:
        for t in ((0, 1, 2), (0, 2, 3)) if len(f) == 4 else ((0, 1, 2),):
            tris.append([(f[i][0], f[i][1]) for i in t])
    T = np.array(tris)
    vn = np.zeros_like(P)
    for tri in T:
        vi = tri[:, 0]
        vn[vi] += np.cross(P[vi[1]] - P[vi[0]], P[vi[2]] - P[vi[0]])
    vn /= np.maximum(np.linalg.norm(vn, axis=1, keepdims=True), 1e-12)
    return P, vt, T[(P[T[:, :, 0], 1] > HEAD_Y).all(1)], vn


def render(cam, P, vt, T, vn) -> dict:
    """z-buffer: per pixel the atlas position (0..1, rows down), the depth and the normal."""
    px, py, z = project(cam, P)
    zb = np.full((W, W), np.inf)
    uvb = np.zeros((W, W, 2))
    nb = np.zeros((W, W, 3))
    for tri in T:
        vi, ti = tri[:, 0], tri[:, 1]
        ax, bx, cx = px[vi]; ay, by, cy = py[vi]
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if den >= -1e-9:
            continue
        x0, x1 = int(max(np.floor(min(ax, bx, cx)), 0)), int(min(np.ceil(max(ax, bx, cx)), W - 1))
        y0, y1 = int(max(np.floor(min(ay, by, cy)), 0)), int(min(np.ceil(max(ay, by, cy)), W - 1))
        if x1 < x0 or y1 < y0:
            continue
        ys, xs = np.mgrid[y0:y1 + 1, x0:x1 + 1]
        qx, qy = xs + 0.5, ys + 0.5
        w0 = ((by - cy) * (qx - cx) + (cx - bx) * (qy - cy)) / den
        w1 = ((cy - ay) * (qx - cx) + (ax - cx) * (qy - cy)) / den
        w2 = 1 - w0 - w1
        ins = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        if not ins.any():
            continue
        Wb = np.stack([w0[ins], w1[ins], w2[ins]], -1)
        zz = Wb @ z[vi]
        yy, xx = ys[ins], xs[ins]
        closer = zz < zb[yy, xx]
        if not closer.any():
            continue
        yy, xx, Wb, zz = yy[closer], xx[closer], Wb[closer], zz[closer]
        zb[yy, xx] = zz
        uv = Wb @ vt[ti]
        uvb[yy, xx, 0], uvb[yy, xx, 1] = uv[:, 0], 1 - uv[:, 1]
        n = Wb @ vn[vi]
        nb[yy, xx] = n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    return {"z": zb.astype(np.float32), "uv": uvb.astype(np.float32), "n": nb.astype(np.float32),
            "mask": np.isfinite(zb)}


def sample(img, uv):
    """Bilinear lookup of an (H, W, C) picture at uv in 0..1 (x right, y down)."""
    H, Wd = img.shape[:2]
    x = np.clip(uv[..., 0] * Wd - 0.5, 0, Wd - 1.001)
    y = np.clip(uv[..., 1] * H - 0.5, 0, H - 1.001)
    x0, y0 = np.floor(x).astype(np.int64), np.floor(y).astype(np.int64)
    fx, fy = (x - x0)[..., None], (y - y0)[..., None]
    return ((img[y0, x0] * (1 - fx) + img[y0, x0 + 1] * fx) * (1 - fy)
            + (img[y0 + 1, x0] * (1 - fx) + img[y0 + 1, x0 + 1] * fx) * fy)


def shading(cam, g, key=(0.35, 0.45, 1.0), amb=0.45):
    """The render's light: a soft key from the upper front left, in camera space, plus ambient."""
    l = np.array(key) / np.linalg.norm(key)
    nc = g["n"] @ cam["R"].T
    nc[..., 2] *= -1
    return amb + (1 - amb) * np.clip(nc @ l, 0, 1)


def _box(m, r: int):
    """How many of the (2r+1)² pixels around each pixel are set (a square window, cumulative sums)."""
    a = m.astype(np.int32)
    for ax in (0, 1):
        c = np.cumsum(np.pad(a, [(r + 1, r) if i == ax else (0, 0) for i in (0, 1)]), axis=ax)
        a = np.take(c, range(2 * r + 1, c.shape[ax]), axis=ax) - np.take(c, range(0, c.shape[ax] - 2 * r - 1), axis=ax)
    return a


def dilate(m, r: int):
    return _box(m, r) > 0


def erode(m, r: int):
    return _box(m, r) == (2 * r + 1) ** 2


def enclosed(m):
    """Background pixels with the silhouette on all four sides (the eye openings, the mouth's gap)."""
    l, r = np.maximum.accumulate(m, 1), np.maximum.accumulate(m[:, ::-1], 1)[:, ::-1]
    u, d = np.maximum.accumulate(m, 0), np.maximum.accumulate(m[::-1], 0)[::-1]
    return l & r & u & d & ~m


def save_srgb(path: Path, lin):
    Image.fromarray((lin_to_srgb(lin) * 255 + 0.5).astype(np.uint8)).save(path)


# ------------------------------------------------------------------ the head's texels -----------
def head_fields(d: Path) -> dict:
    """The head region's texels at the subject's size: positions, normals, and the masks the bake
    uses, cached in ``<dir>`` (the whole atlas's fields are made once, then only the head is kept)."""
    cache = d / f"head_fields_{gsm.N}.npz"
    if cache.is_file():
        z = np.load(cache)
        if "ears" in z.files:
            return {k: z[k] for k in z.files}
    t = time.time()
    F = gss.fields(parts=False)
    P, cover, masks = F["P"], F["cover"], F["masks"]
    idx = np.flatnonzero((cover & (P[..., 1] > HEAD_Y)).ravel())
    flat = lambda a: a.reshape(-1, *a.shape[2:])[idx]                       # noqa: E731
    Pf = flat(P)
    L = gss.face_landmarks(Pf, {k: flat(masks[k]) for k in ("face", "eyelids", "lips")}, np.ones(len(idx), bool))
    brow = np.zeros(len(idx))
    for e in L["eyes"]:
        m, y, zz = gss._eye_frame(Pf, e, L["fx"])
        brow = np.maximum(brow, np.exp(-(((m + 0.004) / 0.026) ** 2 + ((y - 0.021) / 0.009) ** 2 + (zz / 0.025) ** 2)))
    out = {"idx": idx, "P": Pf.astype(np.float32), "N": flat(F["N"]).astype(np.float32),
           "face": flat(masks["face"]), "lips": flat(gsm.blur(masks["lips"], 4)),
           "lids": flat(gsm.blur(masks["eyelids"], 4)), "brow": brow.astype(np.float32),
           "ears": flat(gsm.blur(masks["ears"], 6))}
    np.savez(cache, **out)
    print(f"head fields at {gsm.N}: {len(idx)} texels, {time.time() - t:.0f}s")
    return out


# ------------------------------------------------------------------ the commands ----------------
def cmd_render(d: Path, keys: list, tag: str) -> None:
    P, vt, T, vn = head_mesh()
    alb = subject_albedo() if tag == "base" else np.load(d / f"albedo_{tag}.npy").astype(np.float32)
    for k in keys:
        t = time.time()
        cam = camera(VIEWS[k])
        g = d / f"geom_{k}.npz"
        if g.is_file():
            geo = dict(np.load(g))
        else:
            geo = render(cam, P, vt, T, vn)
            np.savez(g, **geo)
        col = sample(alb, geo["uv"]) * shading(cam, geo)[..., None]
        save_srgb(d / f"in_{k}_{tag}.png", np.where(geo["mask"][..., None], col, 0.18 ** 2.2))
        print(f"{k}: {VIEWS[k]['words']}, {mm_per_px(VIEWS[k]):.3f} mm/px, {time.time() - t:.0f}s")


def cmd_bake(d: Path, tag: str, keys: list, picture: bool) -> None:
    H = head_fields(d)
    P, Nr = H["P"].astype(np.float64), H["N"].astype(np.float64)
    n = len(P)
    # the masks (F-AIS-13); the ears too: the profile pictures do not sit on hm08's ear (click 1)
    # The lids are the model's: the lash line sits at the opening, inside the band kept clear around it
    # (EYE_MM); masking the whole lid left C's smoother lid as a ring (click 1, second showing).
    keep = (H["brow"] < 0.25) & (H["lips"] < 0.15) & (H["ears"] < 0.2)
    acc, wsum = np.zeros((n, 3)), np.zeros(n)
    skipped, overlaps = [], {}
    for k in keys:
        v, cam = VIEWS[k], camera(VIEWS[k])
        geo = dict(np.load(d / f"geom_{k}.npz"))
        gen = srgb_to_lin(np.asarray(Image.open(d / f"view_{k}_{tag}.png").convert("RGB"), np.float64) / 255)
        if gen.shape[:2] != (W, W):
            raise SystemExit(f"view_{k}_{tag}.png is {gen.shape[1]} x {gen.shape[0]}, not {W}²")
        mpp = mm_per_px(v)
        mask = geo["mask"]
        # The overlay gate (F-AIS-11, RD-P25-5): the painted head must sit on the render's silhouette.
        g8 = np.asarray(Image.open(d / f"view_{k}_{tag}.png").convert("RGB"), np.int16)
        bgpix = g8[~dilate(mask | enclosed(mask), 12)]          # where the render shows no head
        fg = np.abs(g8 - np.median(bgpix, 0)).max(-1) > 24
        iou = float((fg & mask).sum() / max((fg | mask).sum(), 1))
        if iou < IOU_MIN:
            print(f"{k}: SKIPPED, the painted head is off the render's silhouette (overlap {iou:.3f} < {IOU_MIN})")
            skipped.append(k)
            continue
        overlaps[k] = round(iou, 4)
        inside = erode(mask, max(1, round(EDGE_MM / mpp)))
        inside &= ~dilate(enclosed(mask), max(1, round(EYE_MM / mpp)))
        px, py, z = project(cam, P)
        xi, yi = np.clip(px.astype(int), 0, W - 1), np.clip(py.astype(int), 0, W - 1)
        vis = keep & (np.abs(geo["z"][yi, xi] - z) < 0.004) & inside[yi, xi]
        to_cam = cam["C"] - P
        to_cam /= np.linalg.norm(to_cam, axis=-1, keepdims=True)
        w = np.where(vis, np.clip(np.einsum("ij,ij->i", Nr, to_cam), 0, 1) ** POW, 0) / mpp ** 2
        uv = np.stack([px / W, py / W], -1)
        est = sample(gen, uv) / np.maximum(sample(shading(cam, geo)[..., None], uv), 0.05)
        acc += w[:, None] * est
        wsum += w
        print(f"{k}: {int((w > 0).sum())} texels seen")
    have = wsum > 0
    new = acc[have] / wsum[have, None]

    base = subject_albedo()
    flat = base.reshape(-1, 3)
    core = have & (H["face"] > 0.9)
    k_hold = flat[H["idx"][core]].mean(0, dtype=np.float64) / new[core[have]].mean(0, dtype=np.float64)
    new *= k_hold
    N = gsm.N
    C = flat[H["idx"]].astype(np.float64)
    newfull = np.zeros((n, 3))
    newfull[have] = new
    # The masked brows and lids take the subject's colour at D's level there: C times D's ratio to C
    # over the skin around them (a normalised blur in the atlas), so no patch of C shows. The lips
    # stay the subject's as they are (RD-P25-2).
    # Every head texel no picture drew (the masks, the band kept clear around the eye openings: the
    # ring at click 1) takes C at D's level; the lips stay C's.
    fill = (~have) & (H["lips"] < 0.15)
    logq = np.log(np.maximum(newfull[have], 1e-4) / np.maximum(C[have], 1e-4))
    den = np.zeros(N * N, np.float32)
    den[H["idx"][have]] = 1
    den = gsm.blur(den.reshape(N, N), FILL_R).ravel()[H["idx"]]
    lq = np.zeros((n, 3))
    for ch in range(3):
        num = np.zeros(N * N, np.float32)
        num[H["idx"][have]] = logq[:, ch]
        lq[:, ch] = gsm.blur(num.reshape(N, N), FILL_R).ravel()[H["idx"]] / np.maximum(den, 1e-6)
    newfull[fill] = C[fill] * np.exp(lq[fill])
    # The neck (click 1: "a neck line skin color change"): toward the bottom of the head region D's broad
    # level is eased onto C's (D's ratio to C, blurred wide, divided out), so the join changes gradually.
    den_w = np.zeros(N * N, np.float32)
    den_w[H["idx"][have]] = 1
    den_w = gsm.blur(den_w.reshape(N, N), NECK_R).ravel()[H["idx"]]
    lw = np.zeros((n, 3))
    for ch in range(3):
        num = np.zeros(N * N, np.float32)
        num[H["idx"][have]] = logq[:, ch]
        lw[:, ch] = gsm.blur(num.reshape(N, N), NECK_R).ravel()[H["idx"]] / np.maximum(den_w, 1e-6)
    s = np.clip((H["P"][:, 1] - NECK_MATCH[0]) / (NECK_MATCH[1] - NECK_MATCH[0]), 0, 1)[:, None]
    newfull *= np.exp(-(1 - s) * lw)
    drawn = have | fill
    # The blend: where the pictures saw (their weight, feathered in the atlas), faded in over the neck.
    wfull = np.zeros(N * N, np.float32)
    wfull[H["idx"][have]] = np.clip(wsum[have] / np.percentile(wsum[have], 50), 0, 1)
    wfull[H["idx"][fill]] = 1.0
    wt = gsm.blur(wfull.reshape(N, N), 6).ravel()[H["idx"]]
    wt *= np.clip((H["P"][:, 1] - NECK[0]) / (NECK[1] - NECK[0]), 0, 1)
    wt = np.where(drawn, np.clip(wt, 0, 1), 0)[:, None]
    out = flat.copy()
    out[H["idx"]] = flat[H["idx"]] * (1 - wt) + newfull * wt
    out = out.reshape(N, N, 3)
    np.save(d / f"albedo_{tag}.npy", out.astype(np.float16))
    clipped = float((out[out.max(-1) > 1.0].shape[0]) / max(int(have.sum()), 1))
    rec = {"tag": tag, "views": keys, "skipped": skipped, "overlap": overlaps, "size": N, "hold_scale": np.round(k_hold, 4).tolist(),
           "texels_seen": int(have.sum()), "masked_out": int((~keep).sum()), "clipped_share": round(clipped, 5),
           "mm_per_px": {k: round(mm_per_px(VIEWS[k]), 4) for k in keys},
           "face_core_mean": np.round(out.reshape(-1, 3)[H["idx"][core]].mean(0, dtype=np.float64), 4).tolist()}
    (d / f"bake_{tag}.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(rec))
    if picture:
        save_srgb(d / f"D_{tag}.png", out)
        print(f"picture {d / f'D_{tag}.png'}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("render")
    r.add_argument("dir", type=Path)
    r.add_argument("views")
    r.add_argument("--albedo", default="base", help="'base' (the subject as served) or a baked tag")
    b = sub.add_parser("bake")
    b.add_argument("dir", type=Path)
    b.add_argument("tag")
    b.add_argument("views")
    b.add_argument("--picture", action="store_true")
    a = ap.parse_args(argv)
    a.dir.mkdir(parents=True, exist_ok=True)
    keys = a.views.split(",")
    for k in keys:
        if k not in VIEWS:
            raise SystemExit(f"unknown view {k!r} (have {list(VIEWS)})")
    if a.cmd == "render":
        cmd_render(a.dir, keys, a.albedo)
    else:
        cmd_bake(a.dir, a.tag, keys, a.picture)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
