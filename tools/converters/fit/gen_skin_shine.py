#!/usr/bin/env python3
"""Make the skin's SHINE MAPS for MakeHuman_Body_v01 (hm08): one shared set for all six tones.

    uv run tools/converters/fit/gen_skin_shine.py                 # every map, into the library
    uv run tools/converters/fit/gen_skin_shine.py --out /tmp/x    # a trial: nothing in the library

Phase22 *Skin Maps Beyond Colour* (RD-P22-1 … 10). Phase21's colour maps did not take away skin's
plastic look: the cause measured was the EVEN SHEEN (F-P21-1). These maps describe the surface, not
the tone, so one set serves every Fitzpatrick article (RD-P22-2). Each is LINEAR DATA on hm08's
atlas, read on the mesh's own UVs, and its neutral value draws today's skin (RD-P22-3):

* ``Skin_roughness_sUKN.png`` (22.1): an OFFSET around 0.5, added to the pores' roughness before
  the Creator's bias and the clamp, ``clamp(pores + (map - 0.5) + bias)`` (RD-P22-4). Oilier, so
  glossier, on the forehead, nose and chin; drier on the cheeks; a few-millimetre grain so the
  highlight breaks up; neutral on the lips (they keep their own finish, RD-P22-8). **Its average
  over the skin is held at 0.5**, so each article's measured roughness stays its average.
* ``Skin_normal_sUKN.png`` (22.2): the skin's RELIEF at the scale the atlas carries (hm08 gives the
  face ~0.47 mm a texel, the back of the hand ~0.75 mm, the body ~0.7-1.1 mm), a tangent-space
  normal (+Y up; the tangent is the mesh's dP/du from texcoord 0, as a bake's is) whose XY is added
  to the pores' (RD-P22-5). It carries what the tiling 1 cm ``Skin_Pores`` cannot: the furrow
  network between the skin's plateaus (larger cells on the hands and body than the face), the
  face's visible pores (densest on the nose and cheeks), and the lines placed on anatomy: the
  forehead's, the frown lines, crow's feet, the lines under the eyes, the fold from nose to mouth,
  the lip lines, the neck's, and the creases over every finger joint. Neutral (flat) at the groin
  (RD-SKM-4).
* ``Skin_cavity_sUKN.png`` (22.2): multiplies ``specular_weight`` (RD-P22-6): 1 on open skin, lower
  in the same furrows, pores and lines, and in the mesh's own creases.

**Made in 3D, not on the atlas** (the 2026-10-26 rule, ``SkinMaps.md``): every texel's position and
normal are rasterised from the mesh (``gen_synth_skin.rasterise``), and the relief is a HEIGHT FIELD
evaluated at each texel's 3D position (supersampled 3 x 3 through the face's own UV mapping), so
nothing seams across a UV edge. The lines are placed from hm08's own joint helpers (the eyes, the
neck, every finger joint) and the mouth from its lip region. The normal is the height's slope along
each face's dP/du and dP/dv, as a baker computes it. CC0 parts only, no photograph and no AI
(RD-SKM-2). Every amount below is judgement, chosen to be seen in the look view; the anatomy
(where lines run, how far apart, how wide) follows the dermatology of skin's surface. Provenance:
``library/provenance/sources/fit/makehuman/skin.yaml``.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gen_skin_maps as gsm  # noqa: E402
import gen_synth_skin as gss  # noqa: E402
import make_kits  # noqa: E402

OUT = gsm.OUT
TAG = gsm.TAG
PROVENANCE = gsm.PROVENANCE
SEED = 20261027
MAPS = ("roughness", "normal", "cavity")

# Roughness offsets (roughness units). The Physically Based skin value is 0.5 and the pores spread
# it 0.46 - 0.56; these move whole zones. First made at half these (T-zone -0.13, cheeks +0.07):
# the look view moved by a third of an 8-bit level on average, so the map was too timid.
T_ZONE = -0.25         # forehead, nose, chin: the sebaceous zones, oilier
CHEEKS = +0.12         # drier
FACE_GRAIN = 0.06      # a 1.5 - 3 cm grain over the face
FINE_GRAIN = 0.08      # 22.2: a 3 - 8 mm grain everywhere, so a highlight is broken, never even
FURROW_ROUGH = 0.08    # 22.2: the furrows and lines hold less oil than the plateaus: rougher
BODY_GRAIN = 0.025     # a 8 - 16 cm drift over the body
CHEST_BACK = -0.03     # the upper trunk's sebaceous zone

# The relief (22.2): depths in metres of the HEIGHT field (negative = into the skin). The slope a
# depth makes depends on its width, and the atlas's texel (~0.5 mm on the face) is the narrowest
# width any of these can have, so the widths below are never under ~1.3 texels where they act.
FURROW = {"face": (1.3e-3, 160e-6), "hand": (1.5e-3, 210e-6), "body": (1.9e-3, 160e-6)}  # cell, depth
FURROW_WIDTH = 0.11    # of a cell: the furrow's half-width; narrow, so the plateaus stay flat (not domes)
PORE = {"cell": 0.95e-3, "radius": 0.30, "depth": 250e-6}   # the face's pores (radius in cells)
LINE_DEPTH = {"forehead": 500e-6, "glabella": 500e-6, "crows": 420e-6, "undereye": 320e-6,
              "nasolabial": 400e-6, "lips": 260e-6, "neck": 500e-6, "knuckle": 520e-6}
LINE_WIDTH = {"forehead": 0.65e-3, "glabella": 0.6e-3, "crows": 0.55e-3, "undereye": 0.5e-3,
              "nasolabial": 2.4e-3, "lips": 0.35e-3, "neck": 0.9e-3, "knuckle": 0.6e-3}
CAVITY_DEPTH = 450e-6  # a groove this deep dims the specular to CAVITY_FLOOR
CAVITY_FLOOR = 0.5
CREASE_CAVITY = 0.25   # the mesh's own creases (its concavity) dim it this much more at the deepest


def name(kind: str) -> str:
    return f"Skin_{kind}_{TAG}.png"


def ellipse(P, cx: float, cy: float, rx: float, ry: float):
    """A soft zone on the face, seen from the front (x across, y up)."""
    return np.exp(-(((P[..., 0] - cx) / rx) ** 2 + ((P[..., 1] - cy) / ry) ** 2))


def smooth(x, a: float, b: float):
    """0 below a, 1 above b, smooth between (b < a runs the other way)."""
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ roughness (22.1) -----------
def roughness_offset(F: dict, R: dict | None = None) -> tuple[np.ndarray, dict]:
    """The roughness offset over the atlas, before the average is held at 0."""
    P, Nr, J, masks, parts = F["P"], F["N"], F["J"], F["masks"], F["parts"]
    ye = float(J["l-eye"][1])                       # eye height (m); the eyes are 6.2 cm apart
    ex = float(J["l-eye"][0])
    chin_y = float(J["jaw"][1])
    front = np.clip((Nr[..., 2] - 0.1) / 0.4, 0.0, 1.0)      # facing forward
    face = np.clip(masks["face"] * 1.5, 0.0, 1.0) * front * (P[..., 1] > float(J["neck"][1]))
    forehead = ellipse(P, 0.0, ye + 0.050, 0.055, 0.028)
    nose = ellipse(P, 0.0, ye - 0.025, 0.014, 0.032)
    chin = ellipse(P, 0.0, chin_y - 0.004, 0.022, 0.016)
    tzone = np.maximum(np.maximum(forehead, nose), chin) * face
    cheeks = (ellipse(P, 1.55 * ex, ye - 0.032, 0.022, 0.022)
              + ellipse(P, -1.55 * ex, ye - 0.032, 0.022, 0.022)) * face
    grain = gss.fbm(P, (0.015, 0.03), (0.6, 0.4), SEED) * face
    fine = gss.fbm(P, (0.003, 0.008), (0.5, 0.5), SEED + 3)
    drift = gss.fbm(P, (0.08, 0.16), (0.6, 0.4), SEED + 7)
    upper = np.clip((P[..., 1] - float(J["spine-2"][1])) / 0.15, 0.0, 1.0) * parts["trunk"]
    f = (T_ZONE * tzone + CHEEKS * cheeks + FACE_GRAIN * grain + FINE_GRAIN * fine
         + BODY_GRAIN * drift + CHEST_BACK * upper)
    if R is not None:                               # the relief's grooves: drier, so rougher
        f = f + FURROW_ROUGH * R["G"]
    f = np.where(F["reg"]["Lips"], 0.0, f)          # the lips keep their own finish (RD-P22-8)
    zones = {"tzone": tzone > 0.5, "cheeks": cheeks > 0.5}
    return f, zones


def store(f: np.ndarray, F: dict) -> tuple[np.ndarray, dict]:
    """The offset -> an 8-bit linear map around 128, its average over the skin held at 0.5."""
    S, cover = F["reg"]["Body"], F["cover"]
    f = gsm.bleed(np.where(cover, f, 0.0)[..., None], cover, gsm.BLEED)[..., 0]
    grown = _grown(cover)
    shift = -float(f[S].mean())
    for _ in range(4):                    # the clip and the 8 bits move the mean: settle it
        q = np.round(np.clip(0.5 + f + shift, 0.0, 1.0) * 255.0)
        q[~grown] = 128.0                  # beyond every island: neutral, so a mip blends nothing
        shift += 0.5 - float((q / 255.0)[S].mean())
    m = q.astype(np.uint8)
    dec = m / 255.0
    stats = {"skin_average": round(float(dec[S].mean()), 4),
             "skin_range": [round(float(np.percentile(dec[S], 1)), 3), round(float(np.percentile(dec[S], 99)), 3)],
             "uncovered_islands": int((F["reg"]["islands"] & ~grown).sum())}
    return m, stats


def _grown(cover):
    grown = cover.copy()
    for _ in range(gsm.BLEED):
        grown = grown | np.roll(grown, 1, 0) | np.roll(grown, -1, 0) | np.roll(grown, 1, 1) | np.roll(grown, -1, 1)
    return grown


# ------------------------------------------------------------------ the mesh's UV mapping -------
def jacobian(m: dict, N: int):
    """Each texel's dP per texel step along the atlas's +x (u) and +y (down, -v), from its face."""
    P = np.array(m["points"], dtype=np.float64)
    vt = np.array(m["vt"], dtype=np.float64)
    Tx = np.zeros((N, N, 3))
    Ty = np.zeros((N, N, 3))
    for f in m["faces"]:
        for tri in ((0, 1, 2), (0, 2, 3)) if len(f) == 4 else ((0, 1, 2),):
            vi = [f[t][0] for t in tri]
            uv = np.array([[vt[f[t][1]][0] * N, (1 - vt[f[t][1]][1]) * N] for t in tri])
            d_uv = np.array([uv[1] - uv[0], uv[2] - uv[0]])           # 2 x 2 (texels)
            det = np.linalg.det(d_uv)
            if abs(det) < 1e-9:
                continue
            d_p = np.array([P[vi[1]] - P[vi[0]], P[vi[2]] - P[vi[0]]])  # 2 x 3 (m)
            Jm = np.linalg.solve(d_uv, d_p)                            # rows: dP/dx, dP/dy
            x0, y0 = np.floor(uv.min(0)).astype(int)
            x1, y1 = np.ceil(uv.max(0)).astype(int)
            x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, N - 1), min(y1, N - 1)
            if x1 < x0 or y1 < y0:
                continue
            ys, xs = np.mgrid[y0:y1 + 1, x0:x1 + 1]
            px, py = xs + 0.5, ys + 0.5
            (ax, ay), (bx, by), (cx, cy) = uv
            den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
            w0 = ((by - cy) * (px - cx) + (cx - bx) * (py - cy)) / den
            w1 = ((cy - ay) * (px - cx) + (ax - cx) * (py - cy)) / den
            ins = (w0 >= -1e-4) & (w1 >= -1e-4) & (1 - w0 - w1 >= -1e-4)
            Tx[ys[ins], xs[ins]] = Jm[0]
            Ty[ys[ins], xs[ins]] = Jm[1]
    return Tx, Ty


# ------------------------------------------------------------------ the relief (22.2) ----------
def _hash3(c, seed: int):
    """Three uniform 0..1 values per integer cell (a 64-bit integer mix)."""
    x = (c[:, 0] * 73856093) ^ (c[:, 1] * 19349663) ^ (c[:, 2] * 83492791) ^ seed
    x = x.astype(np.uint64)
    out = []
    for k in (0x9E3779B97F4A7C15, 0xC2B2AE3D27D4EB4F, 0x165667B19E3779F9):
        y = x * np.uint64(k)
        y ^= y >> np.uint64(29)
        y *= np.uint64(0xBF58476D1CE4E5B9)
        y ^= y >> np.uint64(32)
        out.append((y & np.uint64(0xFFFFFF)).astype(np.float64) / float(0x1000000))
    return np.stack(out, -1)


def worley(P, cell: float, seed: int, chunk: int = 300_000):
    """3D cellular noise over points P (n x 3): the nearest and second-nearest feature distances,
    in cells. F2 - F1 is 0 on a cell's border (a furrow); F1 is 0 at its feature point (a pore)."""
    n = len(P)
    F1, F2 = np.empty(n), np.empty(n)
    offs = [(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1)]
    for s in range(0, n, chunk):
        q = P[s:s + chunk] / cell
        base = np.floor(q).astype(np.int64)
        f1 = np.full(len(q), 9.0)
        f2 = np.full(len(q), 9.0)
        for o in offs:
            c = base + np.array(o)
            d = np.sqrt(((c + _hash3(c, seed) - q) ** 2).sum(-1))
            f2 = np.where(d < f1, f1, np.minimum(f2, d))
            f1 = np.minimum(f1, d)
        F1[s:s + chunk], F2[s:s + chunk] = f1, f2
    return F1, F2


def _lines(t, starts, spacing, width, depths):
    """Grooves across a coordinate t (m): line k at starts + k * spacing, each its own depth."""
    g = np.zeros_like(t)
    for k, d in enumerate(depths):
        g = g + d * np.exp(-((t - (starts + k * spacing)) / width) ** 2)
    return g


class Anatomy:
    """Where the lines go, from hm08's joints and its lip region (metres; x to the body's left)."""

    def __init__(self, F: dict):
        J = F["J"]
        self.J = J
        self.ye = float(J["l-eye"][1])
        self.ex = float(J["l-eye"][0])
        self.eye_z = float(J["l-eye"][2])
        lips = F["reg"]["Lips"] & F["cover"]
        L = F["P"][lips]
        self.mouth_y = float(np.median(L[:, 1]))
        self.mouth_w = float(np.percentile(np.abs(L[:, 0]), 99))     # half the mouth's width
        self.neck_y = float(J["neck"][1])


def height(Q, Nq, sel: dict, A: Anatomy, rng_seed: int = SEED) -> tuple[np.ndarray, np.ndarray]:
    """The relief's height (m, <= 0) and its groove amount (0..1) at points Q (n x 3), normals Nq.
    ``sel`` holds each point's soft region weights (face, hand, body, lips, groin)."""
    x, y, z = Q[:, 0], Q[:, 1], Q[:, 2]
    face, hand, lips = sel["face"], sel["hand"], sel["lips"]
    body = np.clip(1.0 - face - hand, 0.0, 1.0)
    H = np.zeros(len(Q))
    G = np.zeros(len(Q))
    breakup = np.clip(0.55 + 0.9 * gsm.vnoise(Q, 0.012, rng_seed + 1), 0.0, 1.0)   # lines fade in and out

    # 1. The furrow network: the skin's plateaus and the furrows between them, everywhere
    for region, w, k in (("face", face, 0), ("hand", hand, 1), ("body", body, 2)):
        cell, depth = FURROW[region]
        idx = w > 0.01
        if not idx.any():
            continue
        f1, f2 = worley(Q[idx], cell, rng_seed + 11 + k)
        fur = np.exp(-((f2 - f1) / FURROW_WIDTH) ** 2)
        vary = np.clip(0.7 + 0.6 * gsm.vnoise(Q[idx], 0.02, rng_seed + 21 + k), 0.3, 1.3)
        H[idx] -= w[idx] * depth * fur * vary
        G[idx] += w[idx] * fur * 0.5

    # 2. The face's pores: densest and largest on the nose and the cheeks, few at the eyes and lips
    idx = face > 0.01
    if idx.any():
        f1, _ = worley(Q[idx], PORE["cell"], rng_seed + 31)
        pit = np.exp(-(f1 / PORE["radius"]) ** 2)
        q = Q[idx]
        nose = ellipse(q, 0.0, A.ye - 0.03, 0.018, 0.03)
        cheek = ellipse(q, 1.4 * A.ex, A.ye - 0.035, 0.03, 0.03) + ellipse(q, -1.4 * A.ex, A.ye - 0.035, 0.03, 0.03)
        chin = ellipse(q, 0.0, A.mouth_y - 0.035, 0.02, 0.015)
        dens = np.clip(0.35 + 0.9 * nose + 0.7 * cheek + 0.4 * chin, 0.0, 1.4)
        near_eye = ellipse(q, A.ex, A.ye, 0.016, 0.009) + ellipse(q, -A.ex, A.ye, 0.016, 0.009)
        dens = dens * (1.0 - np.clip(near_eye, 0.0, 1.0)) * (1.0 - lips[idx])
        H[idx] -= face[idx] * PORE["depth"] * pit * dens
        G[idx] += face[idx] * pit * dens * 0.6

    front = smooth(Nq[:, 2], 0.15, 0.55)
    fw = face * front
    s = np.sign(x)
    ax = np.abs(x)

    # 3. The lines placed on anatomy (each a groove profile; t is the distance across the lines)
    def add(kind: str, groove: np.ndarray):
        nonlocal H, G
        H = H - LINE_DEPTH[kind] * groove
        G = G + np.clip(groove, 0.0, 1.0)

    wig = 0.0012 * gsm.vnoise(Q, 0.018, rng_seed + 41)
    # forehead: four or five horizontal lines above the brows, curving down at the temples
    t = y - (A.ye + 0.024) + 2.5 * x ** 2 + wig
    fore = fw * smooth(ax, 0.052, 0.035) * smooth(y, A.ye + 0.016, A.ye + 0.024) * smooth(y, A.ye + 0.072, A.ye + 0.06)
    add("forehead", fore * breakup * _lines(t, 0.0, 0.0095, LINE_WIDTH["forehead"], (0.8, 1.0, 0.9, 0.7, 0.45)))
    # the frown lines: two short verticals between the brows
    tg = ax - 0.0055 + 0.3 * wig
    gl = fw * smooth(y, A.ye - 0.002, A.ye + 0.006) * smooth(y, A.ye + 0.026, A.ye + 0.016)
    add("glabella", gl * _lines(tg, 0.0, 1.0, LINE_WIDTH["glabella"], (1.0,)))
    # crow's feet: a fan from each eye's outer corner, outward
    cx = A.ex + 0.0165
    dx, dy = ax - cx, y - (A.ye - 0.002)
    r = np.hypot(dx, dy)
    th = np.arctan2(dy, np.maximum(dx, 1e-6))
    side = smooth(np.abs(Nq[:, 0]) + Nq[:, 2], 0.3, 0.6)
    crow_m = sel["face"] * side * (dx > -0.001) * smooth(r, 0.003, 0.006) * smooth(r, 0.024, 0.016)
    crow = np.zeros(len(Q))
    ci = crow_m > 0
    jit = 0.06 * gsm.vnoise(Q[ci], 0.01, rng_seed + 51)
    for k, a in enumerate((-0.62, -0.36, -0.14, 0.06, 0.27, 0.5)):
        a = a + jit * (1 if k % 2 else -1)
        crow[ci] += (0.7 + 0.3 * (k % 2)) * np.exp(-((th[ci] - a) * r[ci] / LINE_WIDTH["crows"]) ** 2)
    add("crows", crow_m * breakup * crow)
    # under the eyes: two or three fine arcs below the lower lid
    tu = (A.ye - 0.0115) - y + 9.0 * (ax - A.ex) ** 2 + 0.5 * wig
    ue = fw * smooth(np.abs(ax - A.ex), 0.016, 0.010)
    add("undereye", ue * breakup * _lines(-tu, 0.0, 0.0024, LINE_WIDTH["undereye"], (1.0, 0.75, 0.45)))
    # the fold from the nose's wing to past the mouth's corner
    a2 = np.stack([0.017 * np.ones_like(x), np.full_like(x, A.ye - 0.047)], -1)
    b2 = np.stack([(A.mouth_w + 0.006) * np.ones_like(x), np.full_like(x, A.mouth_y - 0.014)], -1)
    p2 = np.stack([ax, y], -1)
    ab = b2 - a2
    tt = np.clip(((p2 - a2) * ab).sum(-1) / (ab * ab).sum(-1), 0, 1)
    dn = np.linalg.norm(p2 - (a2 + tt[:, None] * ab), axis=-1)
    nl = fw * smooth(tt, 0.0, 0.15) * smooth(tt, 1.0, 0.8)
    add("nasolabial", nl * np.exp(-(dn / LINE_WIDTH["nasolabial"]) ** 2))
    # the lips' vertical lines, fanning a little toward the corners
    if lips.any():
        phase = 2 * np.pi * (x * (1.0 + 2.0 * ax / max(A.mouth_w, 1e-3))) / 0.0012 \
            + 2.5 * gsm.vnoise(Q, 0.004, rng_seed + 61)
        lp = (0.5 + 0.5 * np.cos(phase)) ** 6
        add("lips", lips * front * smooth(ax, A.mouth_w, A.mouth_w * 0.8) * lp
            * np.clip(0.5 + 0.8 * gsm.vnoise(Q, 0.006, rng_seed + 62), 0.0, 1.0))
    # the neck: two soft rings at the front
    tn = y - (A.neck_y + 0.038) + 1.2 * x ** 2 + wig
    nk = sel["neck"] * front * smooth(ax, 0.06, 0.04)
    add("neck", nk * breakup * _lines(tn, 0.0, 0.021, LINE_WIDTH["neck"], (1.0, 0.7)))
    # every finger joint: rings of creases across the finger (both sides; the palm's deepest)
    kn = np.zeros(len(Q))
    hi = hand > 0.01
    Qh = Q[hi]
    kwig = 0.0004 * gsm.vnoise(Qh, 0.004, rng_seed + 71)
    for sd in ("l", "r"):
        for fi in range(1, 6):
            for j, n_lines in ((1, 2), (2, 3), (3, 2)):
                c = A.J[f"{sd}-finger-{fi}-{j}"]
                nxt = A.J[f"{sd}-finger-{fi}-{j + 1}"]
                prv = A.J[f"{sd}-finger-{fi}-{j - 1}"] if j > 1 else A.J[f"{sd}-hand"]
                axis = (nxt - prv) / np.linalg.norm(nxt - prv)
                rel = Qh - c
                ta = rel @ axis
                rad = np.linalg.norm(rel - ta[:, None] * axis, axis=-1)
                m = smooth(rad, 0.016, 0.011) * smooth(np.abs(ta), 0.006, 0.004)
                if not (m > 0).any():
                    continue
                kn[hi] += m * _lines(ta + kwig, -0.002 * (n_lines - 1) / 2,
                                     0.002, LINE_WIDTH["knuckle"], (1.0,) * n_lines)
    add("knuckle", hand * kn)

    keep = 1.0 - sel["groin"]                     # RD-SKM-4: no relief at the genitals or groin
    return H * keep, np.clip(G * keep, 0.0, 1.0)


def regions3d(F: dict, A: Anatomy):
    """Each texel's soft region weights for the relief."""
    P, parts, masks = F["P"], F["parts"], F["masks"]
    head = np.clip(parts["head"], 0, 1)
    face = np.clip(masks["face"] * 1.5, 0.0, 1.0) * head
    face = np.maximum(face, np.clip(masks["eyelids"] * 1.5, 0, 1))
    hand = np.clip(parts["hand"], 0, 1)
    lips = F["reg"]["Lips"].astype(float)
    pel = A.J["pelvis"]
    groin = smooth(np.linalg.norm(P - (pel + np.array([0.0, -0.07, 0.06])), axis=-1), 0.13, 0.09)
    return {"face": face, "hand": hand, "lips": lips, "neck": np.clip(parts["neck"], 0, 1), "groin": groin}


def relief(F: dict, Tx, Ty, supersample: int = 2) -> dict:
    """The height (m) on the atlas, its groove amount, and the tangent-space normal."""
    cover = F["cover"] & (np.linalg.norm(Tx, axis=-1) > 0)
    A = Anatomy(F)
    R3 = regions3d(F, A)
    P, Nr = F["P"][cover], F["N"][cover]
    sel = {k: v[cover] for k, v in R3.items()}
    tx, ty = Tx[cover], Ty[cover]
    offs = [((i + 0.5) / supersample - 0.5) for i in range(supersample)]
    h = np.zeros(len(P))
    g = np.zeros(len(P))
    for ox in offs:
        for oy in offs:
            hh, gg = height(P + ox * tx + oy * ty, Nr, sel, A)
            h += hh
            g += gg
    h /= supersample ** 2
    g /= supersample ** 2
    Hm = np.zeros(cover.shape)
    Gm = np.zeros(cover.shape)
    Hm[cover], Gm[cover] = h, g
    # the slope along +x and +y, from the neighbours on the SAME face side of a seam: a neighbour
    # whose 3D position is not where this texel's own mapping puts it is across a UV seam
    Pm = F["P"]
    lx = np.linalg.norm(Tx, axis=-1)
    ly = np.linalg.norm(Ty, axis=-1)

    def slope(axis: int, T, L):
        ok_p = np.roll(cover, -1, axis) & (np.linalg.norm(np.roll(Pm, -1, axis) - Pm - T, axis=-1) < 0.6 * L)
        ok_m = np.roll(cover, 1, axis) & (np.linalg.norm(Pm - np.roll(Pm, 1, axis) - T, axis=-1) < 0.6 * L)
        hp, hm = np.roll(Hm, -1, axis), np.roll(Hm, 1, axis)
        d = np.where(ok_p & ok_m, (hp - hm) / 2, np.where(ok_p, hp - Hm, np.where(ok_m, Hm - hm, 0.0)))
        return np.where(cover, d / np.maximum(L, 1e-9), 0.0)

    dTx = slope(1, Tx, lx)            # dH / d(metres along the tangent, +u)
    dTy = slope(0, Ty, ly)            # dH / d(metres along +y = -v)
    n = np.stack([-dTx, dTy, np.ones_like(dTx)], -1)   # +Y up: the bitangent is +v, so -dH/dv = +dH/dy
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    return {"H": Hm, "G": Gm, "normal": n, "cover": cover}


def store_normal(n: np.ndarray, F: dict, cover) -> tuple[np.ndarray, dict]:
    """The unit normal -> 8-bit RGB (n/2 + 1/2), flat beyond the islands."""
    full = F["cover"]
    n = np.where(cover[..., None], n, np.array([0.0, 0.0, 1.0]))
    n = gsm.bleed(n, cover, gsm.BLEED)
    n /= np.maximum(np.linalg.norm(n, axis=-1, keepdims=True), 1e-9)
    m = np.round((n * 0.5 + 0.5) * 255.0)
    grown = _grown(full)
    m[~grown] = (128, 128, 255)
    m = np.clip(m, 0, 255).astype(np.uint8)
    S = F["reg"]["Body"]
    dec = m.astype(np.float64) / 255.0 * 2 - 1
    xy = np.linalg.norm(dec[..., :2], axis=-1)
    face = (F["masks"]["face"] > 0.5) & S
    stats = {"xy_rms_skin": round(float(np.sqrt((xy[S] ** 2).mean())), 4),
             "xy_rms_face": round(float(np.sqrt((xy[face] ** 2).mean())), 4),
             "xy_p99_skin": round(float(np.percentile(xy[S], 99)), 3),
             "unit_error_max": round(float(np.abs(np.linalg.norm(dec[S], axis=-1) - 1).max()), 3)}
    return m, stats


def cavity(F: dict, R: dict) -> np.ndarray:
    """1 on open skin; dimmed in the grooves the height carries and in the mesh's own creases."""
    depth = np.clip(-R["H"] / CAVITY_DEPTH, 0.0, 1.0)
    crease = np.clip(F["cv"], 0.0, 1.0)
    c = 1.0 - (1.0 - CAVITY_FLOOR) * depth - CREASE_CAVITY * crease
    return np.clip(np.where(R["cover"], c, 1.0), CAVITY_FLOOR * 0.8, 1.0)


def store_cavity(c: np.ndarray, F: dict, cover) -> tuple[np.ndarray, dict]:
    c = gsm.bleed(np.where(cover, c, 1.0)[..., None], cover, gsm.BLEED)[..., 0]
    m = np.round(np.clip(c, 0, 1) * 255.0)
    m[~_grown(F["cover"])] = 255
    m = m.astype(np.uint8)
    S = F["reg"]["Body"]
    dec = m / 255.0
    return m, {"skin_average": round(float(dec[S].mean()), 4),
               "skin_p1": round(float(np.percentile(dec[S], 1)), 3)}


# ------------------------------------------------------------------ provenance and main ---------
def write_provenance(rows: dict) -> None:
    """Add this maker's files and member rows to ``skin.yaml``, keeping every other row."""
    text = PROVENANCE.read_text(encoding="utf-8")
    lines = text.splitlines()
    files = [f"  - MatterLibrary/textures/fit/makehuman/skin/{name(k)}" for k in rows]
    members = [f"  Skin_{k}: {json.dumps(r, separators=(', ', ': '))}" for k, r in rows.items()]
    lines = [ln for ln in lines if ln not in files and not any(ln.startswith(f"  Skin_{k}:") for k in rows)]
    i = lines.index("provenance:")
    lines[i:i] = files
    lines += members
    out = "\n".join(lines) + "\n"
    out = re.sub(r"(  evidence: tools/converters/fit/gen_skin_maps\.py)(?:, tools/converters/fit/gen_skin_shine\.py)?",
                 r"\1, tools/converters/fit/gen_skin_shine.py", out)
    PROVENANCE.write_text(out, encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=Path, help="write the maps here instead (a trial: no provenance)")
    ap.add_argument("--supersample", type=int, default=3, help="height samples per texel, per axis")
    a = ap.parse_args(argv)
    F = gss.fields()
    m = make_kits.load_mesh(gsm.MESH)
    Tx, Ty = jacobian(m, gsm.N)
    R = relief(F, Tx, Ty, a.supersample)
    rows = {}
    out = a.out or OUT
    out.mkdir(parents=True, exist_ok=True)

    f, zones = roughness_offset(F, R)
    mr, st = store(f, F)
    dec = mr / 255.0
    st |= {f"{z}_average": round(float(dec[sel & F['reg']['Body']].mean()), 4) for z, sel in zones.items()}
    if st["uncovered_islands"]:
        raise SystemExit(f"roughness: {st['uncovered_islands']} island texels left unpainted")
    if abs(st["skin_average"] - 0.5) > 0.005:
        raise SystemExit(f"roughness: the skin's average is {st['skin_average']}, not 0.5")
    Image.fromarray(mr, "L").save(out / name("roughness"), optimize=True)
    rows["roughness"] = {"made": "procedural", "space": "linear", "neutral": 0.5,
                         "rule": "roughness = clamp(pores + (map - 0.5) + roughness_bias)", **st}

    mn, sn = store_normal(R["normal"], F, R["cover"])
    Image.fromarray(mn, "RGB").save(out / name("normal"), optimize=True)
    rows["normal"] = {"made": "procedural", "space": "linear", "neutral": [0.5, 0.5, 1.0],
                      "rule": "tangent space, +Y up (dP/du, dP/dv of texcoord 0); XY added to the article's normal",
                      **sn}

    mc, sc = store_cavity(cavity(F, R), F, R["cover"])
    Image.fromarray(mc, "L").save(out / name("cavity"), optimize=True)
    rows["cavity"] = {"made": "procedural", "space": "linear", "neutral": 1.0,
                      "rule": "specular_weight x map", **sc}
    for k, r in rows.items():
        print(f"{k}: {out / name(k)}\n  " + json.dumps({x: v for x, v in r.items() if x not in ('made', 'rule')}))
    if not a.out:
        write_provenance(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
