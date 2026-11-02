#!/usr/bin/env python3
"""An image model paints the head's whole skin map in hm08's own layout (Phase25, RD-P25-9 … 13).

    uv run tools/converters/fit/paint_uv.py cut   <dir> [--width 2048]
    python3 -I tools/converters/fit/paint_uv.py paint <dir> <tag> --model krea|flux [--strength 0.9] [--seeds 7,11]
    uv run tools/converters/fit/paint_uv.py gate  <dir> <picture>[,<picture>…]
    uv run tools/converters/fit/paint_uv.py warp  <dir> <picture> <tag>
    uv run --with scipy tools/converters/fit/paint_uv.py put <dir> <picture> <tag> [--no-ear]

hm08's head is one island of the atlas: the face unwrapped, the scalp rolled out to each side, the ears
as pads. ``cut`` takes that island from the subject's colour (``Tone34`` as served, held at its face-core
tone), stands it upright at the model's size and records hm08's features in the same frame (the lips and
the lid openings from the maker's masks). ``paint`` has the model repaint it as one picture through the
lead's ComfyUI (standard library only: RD-P25-7). ``gate`` finds the painted features over the whole face
and reports how far, in millimetres on the face, each sits from hm08's (RD-P25-10). ``warp`` moves a
picture's features onto hm08's with one smooth thin-plate warp of the whole picture, nothing blended
(candidate (d)). ``put`` returns a picture to the island on the subject's 8K atlas (C elsewhere, as
served) for ``look.py --candidate``. Everything is written under ``<dir>`` (git-ignored
``library/parity/P25_*``); the model's own size is the working size until the fit is solved (RD-P25-13).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

SUBJECT = "Tone34"
N = 8192                       # the subject's atlas (``SUBJECTS["Tone34"]["size"]``)
GRID = 512                     # the island is found on this grid, then taken at full size
ROT = "ROTATE_270"             # the atlas has the top of the head at its left; this stands it up
# hm08's head island as a picture of a scan, the words that made the model draw it (F-P25-7).
PERSON = ("a real young woman about twenty, light warm skin between Fitzpatrick III and IV, shaved bald head, "
          "no eyebrow hair, no makeup, eyes closed")
SKIN = ("Real unretouched skin: visible pores, fine vellus hair, small blemishes, tiny moles, faint freckles, "
        "uneven tone, slight redness around the nose and on the cheeks")
FLAT = "Albedo only: even, shadowless, delit, no lighting, no highlights. Not a 3D render, not CGI, not painted"
PROMPTS = {
    "krea": ("A flat unwrapped UV texture map of a real human head's skin, from a photogrammetry scan of "
             f"{PERSON}. The face is laid out flat in the centre with the closed eyes, nose and lips, the scalp and "
             f"the back of the head unrolled to each side, the ears as flat patches. {FLAT}. {SKIN}."),
    "flux": ("Turn this flat, unwrapped UV skin texture into the photographed skin texture of a real human head, as "
             f"from a photogrammetry scan: {PERSON}. {SKIN}. {FLAT}. Keep exactly the same layout: every feature "
             "(the closed eyes, nose, lips and ears) stays exactly where it is in the image, same size and shape, "
             "same unwrapped flat projection, same outline."),
}
STEPS = {"krea": 8, "flux": 4}


# ------------------------------------------------------------------ helpers (NumPy) -------------
def _np():
    import numpy as np  # noqa: PLC0415  (``paint`` runs on the standard library alone)
    return np


def lin(s):
    np = _np()
    return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)


def srgb(x):
    np = _np()
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


def _img():
    from PIL import Image  # noqa: PLC0415
    Image.MAX_IMAGE_PIXELS = None
    return Image


def head():
    """The head island's texels: hm08's head region (``project_views.head_fields``), kept to the one
    connected island that holds the face (the region's neck also reaches into the body's island)."""
    np = _np()
    import project_views as pv  # noqa: PLC0415
    H = pv.head_fields(Path(os.environ.get("P25_FIELDS", pv_default_dir())))
    idx = H["idx"]
    r, c = np.divmod(idx, N)
    s = N // GRID
    cell = np.zeros((GRID, GRID), bool)
    cell[r // s, c // s] = True
    seed = np.argwhere(np.zeros((GRID, GRID), bool) | _cells(r, c, H["face"] > 0.9, s))
    keep = np.zeros((GRID, GRID), bool)
    q = deque(map(tuple, seed[:1]))
    keep[q[0]] = True
    while q:                                              # the island: 4-connected cells from the face
        y, x = q.popleft()
        for yy, xx in ((y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)):
            if 0 <= yy < GRID and 0 <= xx < GRID and cell[yy, xx] and not keep[yy, xx]:
                keep[yy, xx] = True
                q.append((yy, xx))
    k = keep[r // s, c // s]
    if not k[H["face"] > 0.9].all():
        raise SystemExit("the face is not one island at this grid")
    return {key: v[k] for key, v in H.items()}


def _cells(r, c, sel, s):
    np = _np()
    m = np.zeros((GRID, GRID), bool)
    m[r[sel] // s, c[sel] // s] = True
    return m


def pv_default_dir() -> str:
    return str(HERE.parents[2] / "library" / "parity" / "P25_Views")


def frame_of(d: Path) -> dict:
    return json.loads((d / "uv_frame.json").read_text())


def to_frame(F: dict, rows, cols):
    """Atlas (row, col) → the upright picture's (x, y), in the picture's pixels."""
    np = _np()
    y0, y1, x0, x1 = F["bbox"]
    W, Hh = F["size"]
    sx, sy = W / (y1 - y0), Hh / (x1 - x0)
    # ROTATE_270 turns the island clockwise: the atlas's last row is the picture's left edge, its first
    # column the picture's top (the top of the head)
    return (y1 - np.asarray(rows) - 0.5) * sx - 0.5, (np.asarray(cols) - x0 + 0.5) * sy - 0.5


# ------------------------------------------------------------------ cut ------------------------
def cmd_cut(d: Path, width: int) -> None:
    np, Image = _np(), _img()
    import project_views as pv  # noqa: PLC0415
    d.mkdir(parents=True, exist_ok=True)
    Hd = head()
    idx, face = Hd["idx"], Hd["face"]
    r, c = np.divmod(idx, N)
    alb = pv.subject_albedo().reshape(-1, 3)                 # C as rendered (linear, its constant applied)
    held = np.array(__import__("gen_synth_skin").SUBJECTS[SUBJECT]["held"])
    Cl = alb[idx].astype(np.float64)
    k = held / Cl[face > 0.9].mean(0)
    y0, y1, x0, x1 = int(r.min()), int(r.max()) + 1, int(c.min()), int(c.max()) + 1
    img = np.empty((y1 - y0, x1 - x0, 3))
    img[:] = (Cl * k).mean(0)
    img[r - y0, c - x0] = Cl * k
    m = np.zeros(img.shape[:2], np.uint8)
    m[r - y0, c - x0] = 255
    img = _pushpull(img, m > 0)        # outside the island: its own skin pushed outward, never a flat edge
    rot = getattr(Image.Transpose, ROT)
    hgt = int(round((x1 - x0) * width / (y1 - y0) / 16)) * 16
    Image.fromarray((srgb(img) * 255 + 0.5).astype(np.uint8)).transpose(rot).resize((width, hgt), Image.LANCZOS).save(d / "uv_C.png")
    Image.fromarray(m).transpose(rot).resize((width, hgt), Image.NEAREST).save(d / "uv_mask.png")
    F = {"subject": SUBJECT, "bbox": [y0, y1, x0, x1], "rotate": ROT, "size": [width, hgt], "held": held.tolist()}
    # millimetres on the face per picture pixel: neighbouring face texels' distance on the body
    core = np.flatnonzero(face > 0.9)
    pos = {int(t): i for i, t in enumerate(idx)}
    dd = [np.linalg.norm(Hd["P"][pos[int(idx[i]) + 1]] - Hd["P"][i]) for i in core[::997] if int(idx[i]) + 1 in pos]
    F["mm_per_px"] = float(np.median(dd) * 1000 * (y1 - y0) / width)
    # hm08's features in the frame: the lips and each lid opening (the maker's masks)
    X, Y = to_frame(F, r, c)
    feats = {}
    lips = Hd["lips"] > 0.5
    feats["lips"] = _feat(X[lips], Y[lips])
    lids = Hd["lids"] > 0.5
    mid = float(np.median(X[face > 0.9]))
    for side, sel in (("eye_r", lids & (X < mid)), ("eye_l", lids & (X >= mid))):
        feats[side] = _feat(X[sel], Y[sel])
    ears = Hd["ears"] > 0.5
    for side, sel in (("ear_r", ears & (X < mid)), ("ear_l", ears & (X >= mid))):
        feats[side] = _feat(X[sel], Y[sel])
    F["features"] = feats
    F["face_box"] = [float(np.percentile(X[face > 0.9], 1)), float(np.percentile(Y[face > 0.9], 1)),
                     float(np.percentile(X[face > 0.9], 99)), float(np.percentile(Y[face > 0.9], 99))]
    (d / "uv_frame.json").write_text(json.dumps(F, indent=1) + "\n")
    print(f"island {y1 - y0} x {x1 - x0} texels → {width} x {hgt}; {F['mm_per_px']:.3f} mm a pixel on the face")
    for n, f in feats.items():
        print(f"  hm08 {n}: centre ({f['cx']:.0f}, {f['cy']:.0f}), {f['w'] * F['mm_per_px']:.1f} mm wide")


def _pushpull(img, known):
    """Fill the unknown pixels from the known ones by a pull-push pyramid (each level the masked mean
    of the one below, then filled back down), so the island's skin continues past its outline: a flat
    surround reads to the model as an edge, and it paints a jaw crease and streaks along it (25.1.11)."""
    np = _np()
    if known.all() or img.shape[0] < 2 or img.shape[1] < 2:
        return img
    h, w = img.shape[:2]
    H2, W2 = (h + 1) // 2, (w + 1) // 2
    pi = np.zeros((H2 * 2, W2 * 2, 3)); pk = np.zeros((H2 * 2, W2 * 2))
    pi[:h, :w] = img * known[..., None]; pk[:h, :w] = known
    si = pi.reshape(H2, 2, W2, 2, 3).sum((1, 3)); sk = pk.reshape(H2, 2, W2, 2).sum((1, 3))
    low = _pushpull(np.where(sk[..., None] > 0, si / np.maximum(sk, 1e-9)[..., None], 0), sk > 0)
    up = np.repeat(np.repeat(low, 2, 0), 2, 1)[:h, :w]
    return np.where(known[..., None], img, up)


def _feat(x, y) -> dict:
    np = _np()
    return {"cx": float(np.mean(x)), "cy": float(np.mean(y)), "x0": float(np.percentile(x, 1)),
            "x1": float(np.percentile(x, 99)), "w": float(np.percentile(x, 99) - np.percentile(x, 1)),
            "y0": float(np.percentile(y, 1)), "y1": float(np.percentile(y, 99))}


# ------------------------------------------------------------------ paint (standard library) ---
def cmd_paint(d: Path, tag: str, model: str, strength: float, seeds: list, server: str) -> None:
    import gen_views_model as g  # noqa: PLC0415
    graph = json.loads(g.WORKFLOWS[model].read_text(encoding="utf-8"))
    version = json.loads(g._call(server, "/system_stats"))["system"]["comfyui_version"]
    import hashlib  # noqa: PLC0415
    # uploaded under a name carrying its hash, so each source is its own file on the server. (This was once
    # read as ComfyUI caching by name; the identical pictures were Krea at 0.9 ignoring its input, 25.1.10.)
    raw = (d / "uv_C.png").read_bytes()
    named = d / f"uv_C_{hashlib.sha256(raw).hexdigest()[:12]}.png"
    named.write_bytes(raw)
    src = g.upload(server, named)
    for sd in seeds:
        t = time.time()
        vals = {"IMAGE": src, "PROMPT": PROMPTS[model], "SEED": sd, "STEPS": STEPS[model], "STRENGTH": strength,
                "PREFIX": f"matter_p25uv_{tag}"}
        png, pid = g.run(server, g.fill(graph, vals))
        name = f"uv_{tag}_seed{sd}"
        (d / f"{name}.png").write_bytes(png)
        models = {n["class_type"]: n["inputs"].get("unet_name") or n["inputs"].get("clip_name") or n["inputs"].get("vae_name")
                  for n in graph.values() if n["class_type"] in ("UNETLoader", "CLIPLoader", "VAELoader")}
        rec = {"model": model, "workflow": g.WORKFLOWS[model].name, "files": models, "comfyui": version, "seed": sd,
               "steps": STEPS[model], "strength": strength if model == "krea" else None, "source": "uv_C.png",
               "prompt": PROMPTS[model], "prompt_id": pid, "seconds": round(time.time() - t, 1)}
        (d / f"{name}.json").write_text(json.dumps(rec, indent=1) + "\n")
        print(f"{name}: {rec['seconds']}s", flush=True)


# ------------------------------------------------------------------ find the painted features --
def _blur(a, r: int):
    """A 2-D box mean of radius ``r`` (edges repeated), by cumulative sums."""
    np = _np()
    out = a.astype(np.float64)
    for ax in (0, 1):
        pad = [(0, 0), (0, 0)]
        pad[ax] = (r + 1, r)
        c = np.cumsum(np.pad(out, pad, mode="edge"), axis=ax)
        hi = c[2 * r + 1:] if ax == 0 else c[:, 2 * r + 1:]
        lo = c[:-(2 * r + 1)] if ax == 0 else c[:, :-(2 * r + 1)]
        out = (hi - lo) / (2 * r + 1)
    return out


def _components(m):
    """4-connected components of a small boolean mask (the windows are small): a list of (ys, xs)."""
    np = _np()
    lab = np.zeros(m.shape, np.int32)
    comps = []
    for y, x in np.argwhere(m):
        if lab[y, x]:
            continue
        comps.append(([], []))
        lab[y, x] = len(comps)
        q = deque([(y, x)])
        while q:
            a, b = q.popleft()
            comps[-1][0].append(a)
            comps[-1][1].append(b)
            for yy, xx in ((a - 1, b), (a + 1, b), (a, b - 1), (a, b + 1)):
                if 0 <= yy < m.shape[0] and 0 <= xx < m.shape[1] and m[yy, xx] and not lab[yy, xx]:
                    lab[yy, xx] = len(comps)
                    q.append((yy, xx))
    return [(np.array(a), np.array(b)) for a, b in comps]


def find(d: Path, picture: Path) -> dict:
    """The painted lips and the two lash lines, searched over the whole face (never only where hm08's
    are: a window around the expected place reads a moved feature as close). Lips: the largest
    component of the most lip-coloured pixels, red over its surroundings, below the eyes and within
    the face's middle; lash lines: per side, the largest dark, wide component in the upper face."""
    np, Image = _np(), _img()
    F = frame_of(d)
    W, Hh = F["size"]
    a = np.asarray(Image.open(picture).convert("RGB").resize((W, Hh), Image.LANCZOS), np.float64) / 255
    fb = F["face_box"]
    hm = F["features"]
    eye_y = (hm["eye_r"]["cy"] + hm["eye_l"]["cy"]) / 2
    span = hm["eye_l"]["cx"] - hm["eye_r"]["cx"]                # between hm08's eyes: the face's scale
    xc = (hm["eye_r"]["cx"] + hm["eye_l"]["cx"]) / 2
    ds = 2                                                       # search at half size (components in Python)
    small = a[::ds, ::ds]
    lum = small.mean(-1)
    red = small[..., 0] - 0.5 * (small[..., 1] + small[..., 2])
    ys, xs = np.mgrid[0:small.shape[0], 0:small.shape[1]] * ds
    out = {}
    # lips: red over a broad surround, below the eye line by at least a third of the eye span
    lipw = (ys > eye_y + 0.35 * span) & (ys < fb[3] + 0.3 * span) & (np.abs(xs - xc) < 0.75 * span)
    rr = red - _blur(red, max(3, int(span / ds)))          # red over the whole cheek's surround
    t = 0.5 * rr[lipw].max()                               # half the reddest: the lip's body, not its rim
    out["lips"] = _largest(np, (rr > t) & lipw, ds, wide=True)
    # lash lines: dark over the surround, per side, above the lips window
    dark = _blur(lum, max(3, int(0.2 * span / ds))) - lum
    for side, sel in (("eye_r", xs < xc), ("eye_l", xs >= xc)):
        w = sel & (ys > fb[1] - 0.2 * span) & (ys < eye_y + 0.35 * span) & (np.abs(xs - xc) < 1.1 * span)
        t = np.percentile(dark[w], 99)
        out[side] = _largest(np, (dark > t) & w, ds, wide=True)
    # ears: the pinkest blob on each side of the head, outside the face (the model draws whole ears)
    rr2 = red - _blur(red, max(3, int(1.5 * span / ds)))
    for side, sgn in (("ear_r", -1), ("ear_l", 1)):
        w = (sgn * (xs - xc) > 1.4 * span) & (sgn * (xs - xc) < 4.0 * span) & (np.abs(ys - eye_y) < 1.6 * span)
        t = 0.45 * rr2[w].max()
        out[side] = _largest(np, (rr2 > t) & w, ds, wide=False)
    return out


def _largest(np, m, ds: int, wide: bool) -> dict | None:
    comps = [c for c in _components(m) if len(c[0]) >= 6]
    if not comps:
        return None
    if wide:   # a lip or a lash line is wider than tall: weight size by flatness
        comps.sort(key=lambda c: len(c[0]) * min(3.0, (np.ptp(c[1]) + 1) / (np.ptp(c[0]) + 1)), reverse=True)
    ys, xs = comps[0]
    x, y = xs * ds + ds / 2, ys * ds + ds / 2
    return {"cx": float(x.mean()), "cy": float(y.mean()), "x0": float(np.percentile(x, 1)), "x1": float(np.percentile(x, 99)),
            "w": float(np.percentile(x, 99) - np.percentile(x, 1)), "y0": float(np.percentile(y, 1)), "y1": float(np.percentile(y, 99))}


def cmd_gate(d: Path, pictures: list) -> int:
    F = frame_of(d)
    mm = F["mm_per_px"]
    rows = {}
    for p in pictures:
        got = find(d, p)
        row = {}
        for n, hf in F["features"].items():
            g = got.get(n)
            if g is None:
                row[n] = None
                continue
            row[n] = {"dx_mm": round((g["cx"] - hf["cx"]) * mm, 1), "dy_mm": round((g["cy"] - hf["cy"]) * mm, 1),
                      "width_ratio": round(g["w"] / hf["w"], 2), "at": [round(g["cx"]), round(g["cy"])]}
        rows[p.name] = row
        ruled = [v for n, v in row.items() if not n.startswith("ear")]   # RD-P25-10 rules the lips and lids; ears are reported
        worst = 99.0 if None in ruled else max(max(abs(v["dx_mm"]), abs(v["dy_mm"])) for v in ruled)
        verdict = "PASS" if worst <= 1.0 else "FAIL"
        print(f"{p.name}: {verdict} (worst {worst:.1f} mm) " +
              " · ".join(f"{n} {v['dx_mm']:+.1f},{v['dy_mm']:+.1f} mm ×{v['width_ratio']}" if v else f"{n} not found" for n, v in row.items()))
    (d / "gate.json").write_text(json.dumps(rows, indent=1) + "\n")
    return 0


# ------------------------------------------------------------------ warp (candidate d) ---------
def _tps_fit(src, dst):
    """A thin-plate spline taking ``dst`` points to ``src`` (a backward map: for each output pixel,
    where to read the picture)."""
    np = _np()
    n = len(dst)
    r2 = ((dst[:, None, :] - dst[None, :, :]) ** 2).sum(-1)
    K = np.where(r2 > 0, r2 * np.log(r2 + 1e-12), 0.0)
    P = np.hstack([np.ones((n, 1)), dst])
    A = np.zeros((n + 3, n + 3))
    A[:n, :n], A[:n, n:], A[n:, :n] = K, P, P.T
    B = np.zeros((n + 3, 2))
    B[:n] = src
    return np.linalg.solve(A, B), dst


def _tps_eval(coef, ctrl, pts):
    np = _np()
    out = np.empty((len(pts), 2))
    for i in range(0, len(pts), 200_000):
        p = pts[i:i + 200_000]
        r2 = ((p[:, None, :] - ctrl[None, :, :]) ** 2).sum(-1)
        U = np.where(r2 > 0, r2 * np.log(r2 + 1e-12), 0.0)
        out[i:i + 200_000] = U @ coef[:len(ctrl)] + coef[len(ctrl)] + p @ coef[len(ctrl) + 1:]
    return out


def _bilinear(img, x, y):
    np = _np()
    h, w = img.shape[:2]
    x = np.clip(x, 0, w - 1.001)
    y = np.clip(y, 0, h - 1.001)
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    fx, fy = (x - x0)[:, None], (y - y0)[:, None]
    return (img[y0, x0] * (1 - fx) * (1 - fy) + img[y0, x0 + 1] * fx * (1 - fy)
            + img[y0 + 1, x0] * (1 - fx) * fy + img[y0 + 1, x0 + 1] * fx * fy)


def cmd_warp(d: Path, picture: Path, tag: str, passes: int = 2) -> None:
    """``passes`` warps, each measured afresh on the last one's picture: the features are found again
    after a warp (a lash line reads a little differently once moved), so a second pass converges them."""
    src = picture
    for k in range(passes):
        _warp_once(d, src, tag if k == passes - 1 else f"{tag}_pass{k + 1}")
        src = d / f"{tag}_pass{k + 1}.png" if k < passes - 1 else src


def _warp_once(d: Path, picture: Path, tag: str) -> None:
    """One smooth warp of the whole picture: each painted feature's two ends and centre onto hm08's,
    a ring of fixed points around the face, so the scalp and the ears stay where the model drew them."""
    np, Image = _np(), _img()
    F = frame_of(d)
    W, Hh = F["size"]
    got = find(d, picture)
    if None in got.values():
        raise SystemExit(f"{picture.name}: a feature was not found ({[n for n, v in got.items() if v is None]}); no warp")
    src, dst = [], []
    for n, hf in F["features"].items():
        g = got[n]
        for gx, hx in ((g["x0"], hf["x0"]), (g["cx"], hf["cx"]), (g["x1"], hf["x1"])):
            src.append((gx, g["cy"]))
            dst.append((hx, hf["cy"]))
        if n.startswith("ear"):                                  # an ear's height too
            for gy, hy in ((g["y0"], hf["y0"]), (g["y1"], hf["y1"])):
                src.append((g["cx"], gy))
                dst.append((hf["cx"], hy))
    fb = F["face_box"]
    span = F["features"]["eye_l"]["cx"] - F["features"]["eye_r"]["cx"]
    cx, cy = (fb[0] + fb[2]) / 2, (fb[1] + fb[3]) / 2
    ears = [F["features"][e] for e in ("ear_r", "ear_l")]
    rx = max(abs(e["cx"] - cx) + e["w"] for e in ears) + 0.6 * span
    ry = max((fb[3] - fb[1]) / 2, max(abs(e["cy"] - cy) + (e["y1"] - e["y0"]) for e in ears)) + 0.6 * span
    for k in (1.0, 1.5):                                         # held: two rings beyond the face and ears
        for t in np.linspace(0, 2 * np.pi, 32, endpoint=False):
            p = (cx + k * rx * np.cos(t), cy + k * ry * np.sin(t))
            src.append(p)
            dst.append(p)
    src, dst = np.array(src), np.array(dst)
    coef, ctrl = _tps_fit(src, dst)
    a = np.asarray(Image.open(picture).convert("RGB").resize((W, Hh), Image.LANCZOS), np.float64)
    yy, xx = np.mgrid[0:Hh, 0:W]
    pts = np.stack([xx.ravel(), yy.ravel()], -1).astype(np.float64)
    mp = _tps_eval(coef, ctrl, pts)                              # the whole picture: no edge to the warp
    out = _bilinear(a, mp[:, 0], mp[:, 1]).reshape(Hh, W, 3)
    # the warp's largest local stretch, as a check that no feature is visibly pulled (RD-P25-10 (d))
    J = mp.reshape(Hh, W, 2)
    sx = np.abs(np.diff(J[..., 0], axis=1))[2:-2, 2:-2].max()
    sy = np.abs(np.diff(J[..., 1], axis=0))[2:-2, 2:-2].max()
    Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(d / f"{tag}.png")
    rec = {"picture": picture.name, "moves_mm": {n: [round((F['features'][n]['cx'] - got[n]['cx']) * F['mm_per_px'], 1),
                                                     round((F['features'][n]['cy'] - got[n]['cy']) * F['mm_per_px'], 1)]
                                                 for n in got},
           "largest_local_scale": round(float(max(sx, sy)), 2)}
    (d / f"{tag}.json").write_text(json.dumps(rec, indent=1) + "\n")
    print(f"{tag}.png: moved {rec['moves_mm']} (mm); largest local scale {rec['largest_local_scale']}")


# ------------------------------------------------------------------ put ------------------------
def cmd_put(d: Path, picture: Path, tag: str, ear: bool = True) -> None:
    """The picture back on the island of the subject's 8K atlas, held to the face core; C elsewhere,
    exactly as served. Written as ``D_<tag>.png`` (linear albedo, sRGB-encoded, for ``look.py --candidate``
    at constant 1) and ``albedo_<tag>.npy`` (for ``project_views.py render``).

    For a subject with ear regions (``gen_synth_skin.SUBJECTS[s]["ear"]``) the ear and its join come from
    the maker, never the picture (RD-P25-18, -19): ``gen_synth_skin.ear_paint``, which needs SciPy
    (``uv run --with scipy``). ``ear=False`` (``--no-ear``) keeps the picture's ear, as before 25.1."""
    np, Image = _np(), _img()
    import project_views as pv  # noqa: PLC0415
    F = frame_of(d)
    y0, y1, x0, x1 = F["bbox"]
    Hd = head()
    idx, face = Hd["idx"], Hd["face"]
    r, c = np.divmod(idx, N)
    pic = Image.open(picture).convert("RGB").transpose(Image.Transpose.ROTATE_90).resize((x1 - x0, y1 - y0), Image.LANCZOS)
    p = lin(np.asarray(pic, np.float64) / 255)[r - y0, c - x0]
    p *= np.array(F["held"]) / p[face > 0.9].mean(0)
    alb = pv.subject_albedo()
    flat = alb.reshape(-1, 3)
    flat[idx] = p.astype(flat.dtype)
    import gen_synth_skin as gss  # noqa: PLC0415
    if ear and gss.SUBJECTS[SUBJECT].get("ear"):
        rep = gss.ear_paint(flat, SUBJECT, pv.head_fields(Path(os.environ.get("P25_FIELDS", pv_default_dir()))))
        for side, r_ in rep.items():
            print(f"  ear {side}: {r_['texels']} texels from the maker, level {r_['base']}, x {r_['ratio_full_ear']} on the ear; "
                  f"{r_['kept_as_picture']} kept as the picture in front; join {r_['join']} texels, face weight at most {r_['join_face_max']}")
    np.save(d / f"albedo_{tag}.npy", alb)
    Image.fromarray((srgb(alb) * 255 + 0.5).astype(np.uint8)).save(d / f"D_{tag}.png")
    print(f"D_{tag}.png: face core {p[face > 0.9].mean(0).round(4).tolist()}; clipped {(p > 1).any(-1).mean() * 100:.3f} % of the island")


def main(argv=None) -> int:
    if os.environ.get("MATTER_SKIN_N") != str(N):   # the maker reads its size at import: the subject's, first
        os.environ["MATTER_SKIN_N"] = str(N)
        os.execvpe(sys.executable, [sys.executable, str(Path(__file__).resolve()), *(sys.argv[1:] if argv is None else argv)], os.environ)
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("cut"); s.add_argument("dir", type=Path); s.add_argument("--width", type=int, default=2048)
    s = sub.add_parser("paint"); s.add_argument("dir", type=Path); s.add_argument("tag")
    s.add_argument("--model", choices=PROMPTS, required=True); s.add_argument("--strength", type=float, default=0.9)
    s.add_argument("--seeds", default="7"); s.add_argument("--server", default="http://127.0.0.1:8188")
    s = sub.add_parser("gate"); s.add_argument("dir", type=Path); s.add_argument("pictures")
    s = sub.add_parser("warp"); s.add_argument("dir", type=Path); s.add_argument("picture"); s.add_argument("tag")
    s.add_argument("--passes", type=int, default=2)
    s = sub.add_parser("put"); s.add_argument("dir", type=Path); s.add_argument("picture"); s.add_argument("tag")
    s.add_argument("--no-ear", action="store_true", help="keep the picture's ear (before RD-P25-18)")
    a = ap.parse_args(argv)
    if a.cmd == "cut":
        cmd_cut(a.dir, a.width)
    elif a.cmd == "paint":
        cmd_paint(a.dir, a.tag, a.model, a.strength, [int(x) for x in a.seeds.split(",")], a.server)
    elif a.cmd == "gate":
        return cmd_gate(a.dir, [a.dir / p for p in a.pictures.split(",")])
    elif a.cmd == "warp":
        cmd_warp(a.dir, a.dir / a.picture, a.tag, a.passes)
    else:
        cmd_put(a.dir, a.dir / a.picture, a.tag, ear=not a.no_ear)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
