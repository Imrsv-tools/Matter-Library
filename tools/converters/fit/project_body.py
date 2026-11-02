#!/usr/bin/env python3
"""An image model's picture of a person becomes the body island's skin, through four cameras (Phase27).

    uv run --with scipy tools/converters/fit/project_body.py prep  <dir>
    python3 -I tools/converters/fit/project_body.py paint <dir> [--seeds 7] [--strength 0.5]
    uv run --with scipy tools/converters/fit/project_body.py fit   <dir> <picture>
    uv run --with scipy tools/converters/fit/project_body.py put   <dir> <picture> <tag> [--head <atlas.png>] [--no-fit]

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
field, F-P25-16). ``put`` then gives each body texel the colour of the view that faces it most squarely
and shows the body there (a hard cut), through the fit; holes by pull-push; the body held to C's mean;
the groin the maker's colour at the surrounding level (RD-P27-2, RD-SKM-4). The result is written on
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
LEVEL_CAP = 0.5              # the most a seam levelling moves a view, in log colour (x1.65)
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
INNER_PAD = 10               # pixels kept clear of it (~1.7 cm): where the model's limb edge sits, unfitted


def inner_edges(g):
    """Pixels near a depth jump INSIDE hm08's silhouette in one view (an arm across the trunk, a leg behind
    the other). The fit moves only the outline, so the model's own limb edge there can sit a centimetre
    or two off hm08's and would paint a line onto the surface behind."""
    np = _np()
    from scipy.ndimage import binary_dilation  # noqa: PLC0415
    z, m = g["z"], g["mask"]
    e = np.zeros_like(m)
    for ax in (0, 1):
        z2 = np.roll(z, 1, ax); m2 = np.roll(m, 1, ax)
        jump = m & m2 & (np.abs(np.where(m & m2, z - z2, 0)) > INNER_JUMP)
        e |= jump | np.roll(jump, -1, ax)
    return binary_dilation(e, iterations=INNER_PAD)


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


def cmd_put(d: Path, pic_path: Path, tag: str, head: Path | None, use_fit: bool, delight: bool = False,
            levelled: bool = False) -> None:
    np = _np()
    from PIL import Image  # noqa: PLC0415
    import project_views as pv  # noqa: PLC0415
    from scipy.ndimage import binary_dilation  # noqa: PLC0415
    Image.MAX_IMAGE_PIXELS = None
    t = time.time()
    A = np.load(d / "atlas.npz")
    C, Pa, Na, body, groin = A["C"].astype(np.float64), A["P"], A["N"], A["body"], A["groin"]
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
        vis &= ~inner_edges(g)[yi, xi]          # one limb in front of another: the fit has no outline there
        if F is not None:
            Dv = F[f"D_{yaw}"]
            ix, iy = ix + sample(Dv[..., 0], ix, iy), iy + sample(Dv[..., 1], ix, iy)
        vis &= sample(fg[:, x0:x0 + w].astype(float), ix, iy) > 0.5
        col = np.zeros((len(rr), 3))
        col[vis] = sample(pic[:, x0:x0 + w], ix[vis], iy[vis])
        if delight:
            # the light the model painted into THIS view, as a smooth function of the surface's direction:
            # the picture over C, fitted with the nine second-order terms of the normal, then divided out
            fitk = vis & (nz > 0.25)
            B = sh9(Nu)
            coef = np.linalg.lstsq(B[fitk], col[fitk] / np.maximum(C[rr[fitk], cc[fitk]], 1e-4), rcond=None)[0]
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
    # a hole (no view faces it squarely enough: between the legs, under the arms) is the maker's skin at
    # D's level round it: C's own detail times D / C carried smoothly in by pull-push (as the groin is)
    from scipy.ndimage import gaussian_filter  # noqa: PLC0415
    ratio = pushpull(np.where(kn[..., None], sh / np.maximum(C, 1e-4), 0.0), kn)
    ratio = np.stack([gaussian_filter(ratio[..., c], 6.0) for c in range(3)], -1)   # pull-push is blocky; ~5 mm
    D[body] = np.where(kn[body][:, None], sh[body], C[body] * ratio[body])
    gain = C[body].mean(0) / D[body].mean(0)                          # the body held to C's mean
    D[body] *= gain
    ring = binary_dilation(groin, iterations=6) & ~groin & body
    level = D[ring].mean(0) / C[ring].mean(0)
    D[groin] = C[groin] * level                                       # RD-P27-2: the maker's, at the level round it
    full = pushpull(np.where(body[..., None], D, 0.0), body)          # the island carried past its edge for 8K
    bid, ids8 = body_island(8192)
    base = (lin(np.asarray(Image.open(head).convert("RGB"), np.float64) / 255) if head else pv.subject_albedo())
    if base.shape[0] != 8192:
        raise SystemExit(f"the base atlas is {base.shape[0]}, not 8192")
    up = np.stack([np.asarray(Image.fromarray(full[..., c].astype(np.float32), "F").resize((8192, 8192), Image.BILINEAR))
                   for c in range(3)], -1)
    sel = ids8 == bid
    out = base.astype(np.float32)
    out[sel] = up[sel]
    del up, base
    Image.fromarray((srgb(out) * 255 + 0.5).astype(np.uint8)).save(d / f"D_{tag}.png")
    save(d / f"D_{tag}_2048.png", D)
    rec = {"picture": pic_path.name, "fit": use_fit, "delight": delight, "light": light, "levelled": levelled,
           "level_log_max": None if lev_max is None else round(lev_max, 3),
           "cut_step_pct_median": step_before_gain["median"], "cut_step_pct_p90": step_before_gain["p90"],
           "head": head.name if head else None,
           "seen_pct": round(float(have.mean() * 100), 1),
           "grazing_under_0.3_pct": round(float((have & (face < 0.3)).mean() * 100), 1),
           "gain": [round(float(v), 3) for v in gain], "groin_level": [round(float(v), 3) for v in level],
           "seconds": round(time.time() - t)}
    (d / f"D_{tag}.json").write_text(json.dumps(rec, indent=1) + "\n")
    print(f"D_{tag}.png: {json.dumps(rec)}")


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
    a = ap.parse_args(argv)
    if a.cmd == "prep":
        cmd_prep(a.dir)
    elif a.cmd == "paint":
        cmd_paint(a.dir, [int(x) for x in a.seeds.split(",")], a.strength, a.server)
    elif a.cmd == "fit":
        cmd_fit(a.dir, a.dir / a.picture)
    elif a.cmd == "put":
        cmd_put(a.dir, a.dir / a.picture, a.tag, a.head, not a.no_fit, a.delight, a.level)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
