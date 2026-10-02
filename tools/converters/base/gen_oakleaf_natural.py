#!/usr/bin/env python3
"""Generate the base texture set `OakLeaf_Natural` (Phase11 batch 261002-7; lane L2).

One fresh, green oak leaf's upper surface, on a card: the Masked master cuts it out by the
`opacity` map. The OUTLINE is a pedunculate-oak leaf drawn by JUDGEMENT: obovate (widest past
the middle), five rounded lobes a side with rounded sinuses about halfway to the midrib, lobes
alternating a little left to right, a rounded terminal lobe, small ear-like auricles at the
base and a short stalk. Pinnate veins: a pale midrib and one secondary vein to each lobe, with
a fine net between. No scan fits: ambientCG's single-leaf sets (Leaf001-003) are tagged only
"green, leaf, single, tree", and the library names only what a source states, so the set is
generated. The colour is anchored, not invented per pixel: the MEAN linear albedo over the
leaf is Physically Based `Grass` (0.105, 0.133, 0.041), the nearest measured green foliage
(it has no leaf entry). Everything here only varies around it.

Writes MatterLibrary/textures/base/environmental/vegetation/OakLeaf_Natural_<channel>_s01.png:
basecolor (sRGB-encoded), roughness, normal (linear data, NormalGL) and opacity (linear, the
cut-out). Scale `s01`: one leaf per tile, about 0.12 m tile, so the blade is ~10 cm long and
~5 cm wide. Outside the leaf the colour and roughness are padded with the leaf's own mean, so
filtering at the cut edge draws no fringe. The leaf never touches the tile's border and every
noise wraps, so the tile is seamless. Fixed seed, no network.

    gen_oakleaf_natural.py [--out DIR]

It refuses to overwrite an existing file (AI_WorkingAgreement §Build Safety).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import tileable as tl  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent.parent
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "environmental" / "vegetation"
SET = "OakLeaf_Natural"
SCALE = "s01"
SEED = 707
GRASS = np.array([0.105, 0.133, 0.041])   # Physically Based `Grass`, linear sRGB: the leaf's mean
VEIN = np.array([1.55, 1.45, 1.35])       # relative tint of a vein (paler, a little yellower)
STALK = np.array([1.5, 1.2, 1.6])         # relative tint of the stalk
ROUGH = 0.5                               # Physically Based `Grass` roughness: a waxy cuticle

BASE, TIP = 0.90, 0.08                    # blade from base to tip, image rows as tile fractions
LENGTH = BASE - TIP
STALK_END = 0.975
HALF_W = 0.235                            # the envelope's peak half-width, tile units
LOBES = 5
SINUS = 0.50                              # how far a sinus cuts toward the midrib (fraction of width)
SUPER = 4                                 # supersampling for the anti-aliased outline


def midrib_x(t):
    return 0.5 + 0.018 * np.sin(np.pi * t)


def envelope(t):
    """Obovate outline, widest at t ~ 0.6, rounded tip and base, small auricles at the base."""
    t = np.clip(t, 0, 1)
    env = np.sin(np.pi * t ** 1.36) ** 0.6                            # peaks at t ~ 0.6
    return HALF_W * env + 0.045 * np.exp(-((t - 0.05) / 0.035) ** 2)


def lobing(t, phase):
    """1 at a lobe's crest, SINUS-deep at a sinus. Lobes lean toward the tip (skewed crest); the
    lobing fades out on the terminal lobe and at the base."""
    s = np.mod(LOBES * (t - 0.06) / 0.80 + phase, 1.0)
    crest = np.sin(np.pi * s ** 1.35) ** 0.5
    m = (1 - SINUS) + SINUS * crest
    fade = np.clip((t - 0.10) / 0.06, 0, 1) * np.clip((0.86 - t) / 0.06, 0, 1)
    return 1 - fade * (1 - m)


PHASES = (0.0, 0.32)                      # right, left: lobes alternate a little
LEAN = 0.45                               # a lobe's crest moves this far tipward per unit of width


def lobe_crests(phase):
    """t of each lobe crest on one side (where lobing() == 1)."""
    crest_s = 0.5 ** (1 / 1.35)
    ts = []
    for k in range(-1, LOBES + 2):
        t = 0.06 + (k + crest_s - phase) * 0.80 / LOBES
        if 0.12 < t < 0.88:
            ts.append(t)
    return ts


def outline(n: int) -> np.ndarray:
    """Coverage of the blade plus stalk on an n x n grid (1 inside), not yet filtered."""
    y = (np.arange(n) + 0.5) / n
    x = (np.arange(n) + 0.5) / n
    X, Y = np.meshgrid(x, y)
    t = (BASE - Y) / LENGTH
    dx = X - midrib_x(t)
    env = envelope(t)
    ts = t - LEAN * np.abs(dx) / LENGTH                                # lobes lean toward the tip
    half = np.where(dx >= 0, env * lobing(ts, PHASES[0]), env * lobing(ts, PHASES[1]))
    blade = (t >= 0) & (t <= 1) & (np.abs(dx) < half)
    stalk = (Y > BASE - 0.01) & (Y < STALK_END) & (np.abs(X - midrib_x(0.0) + 0.02 * (Y - BASE)) < 0.0055)
    return (blade | stalk).astype(float)


def seg_dist(X, Y, a, b):
    ab = np.subtract(b, a)
    t = np.clip(((X - a[0]) * ab[0] + (Y - a[1]) * ab[1]) / (ab @ ab), 0, 1)
    return np.hypot(X - (a[0] + t * ab[0]), Y - (a[1] + t * ab[1])), t


def veins(size: int):
    """(midrib, secondary) vein strengths in [0, 1], each a soft line."""
    c = (np.arange(size) + 0.5) / size
    X, Y = np.meshgrid(c, c)
    # midrib + stalk: a line down the curved midrib, tapering toward the tip
    t = (BASE - Y) / LENGTH
    w_mid = np.interp(t, [-0.1, 0.0, 1.0], [0.0050, 0.0050, 0.0012])
    d_mid = np.abs(X - midrib_x(np.clip(t, 0, 1)))
    midrib = np.clip(1 - d_mid / w_mid, 0, 1) * ((t > -0.10) & (t < 0.99))
    # secondary veins: from the midrib, a little below each lobe's crest, out to the crest
    sec = np.zeros((size, size))
    for side, phase in zip((1, -1), PHASES):
        for tc in lobe_crests(phase):
            half = float(envelope(np.array([tc]))[0])
            tip_t = tc + LEAN * 0.93 * half / LENGTH                  # the leaning crest
            half = float(envelope(np.array([tip_t]))[0])
            tip = (midrib_x(tip_t) + side * 0.90 * half, BASE - tip_t * LENGTH)
            t0 = tc - 0.07
            root = (midrib_x(t0), BASE - t0 * LENGTH)
            mid = (root[0] + side * 0.5 * half, BASE - (0.5 * (t0 + tip_t) - 0.02) * LENGTH)  # a gentle bow
            for a, b, w0, w1 in ((root, mid, 0.0026, 0.0018), (mid, tip, 0.0018, 0.0007)):
                d, f = seg_dist(X, Y, np.array(a), np.array(b))
                w = w0 + (w1 - w0) * f
                sec = np.maximum(sec, np.clip(1 - d / w, 0, 1))
    return midrib, sec


def maps() -> dict:
    n = tl.SIZE
    big = outline(n * SUPER)
    cover = big.reshape(n, SUPER, n, SUPER).mean(axis=(1, 3))         # anti-aliased opacity
    inside = cover > 0.5
    midrib, sec = veins(n)
    netw = 1 - np.abs(2 * tl.fbm((96, 192), SEED + 5) - 1)              # ridged: a reticulate net
    net = np.clip((netw - 0.82) / 0.18, 0, 1)
    mottle = tl.fbm((6, 12, 24), SEED)
    fine = tl.fbm((128, 256), SEED + 10)
    c = (np.arange(n) + 0.5) / n
    X, Y = np.meshgrid(c, c)
    stalk = ((Y > BASE + 0.004) & inside).astype(float)

    vein = np.maximum(midrib, 0.8 * sec)
    shade = 1.0 + 0.14 * (mottle - 0.5) + 0.05 * (fine - 0.5) + 0.05 * net
    tint = 1 + vein[..., None] * (VEIN - 1)[None, None, :]
    tint = tint * (1 - stalk[..., None]) + STALK[None, None, :] * stalk[..., None]
    albedo = GRASS[None, None, :] * shade[..., None] * tint
    albedo *= GRASS / albedo[inside].mean(0)                            # re-anchor the leaf's MEAN
    albedo[~inside] = GRASS                                             # pad: no fringe at the cut

    rough = np.clip(ROUGH + 0.05 * (fine - 0.5) + 0.04 * (mottle - 0.5) + 0.10 * vein, 0, 1)
    rough += ROUGH - rough[inside].mean()
    rough[~inside] = ROUGH

    # upper surface: the veins sit in shallow channels, the tissue between them bulges a little
    height = -1.0 * midrib - 0.6 * sec - 0.15 * net + 0.35 * mottle + 0.15 * fine
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=3.0),
            "opacity": Image.fromarray((cover * 255).round().astype(np.uint8), "L")}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the OakLeaf_Natural base texture set.")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args(argv)
    out = Path(args.out)
    targets = {ch: out / f"{SET}_{ch}_{SCALE}.png" for ch in ("basecolor", "roughness", "normal", "opacity")}
    if any(p.exists() for p in targets.values()):
        print(f"refusing to overwrite {SET} in {out} (Build Safety); use --out <dir>", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)
    for ch, img in maps().items():
        img.save(targets[ch], "PNG", optimize=True)
        print(f"wrote {targets[ch]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
