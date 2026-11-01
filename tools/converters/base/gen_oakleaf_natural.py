#!/usr/bin/env python3
"""Generate the base texture set `OakLeaf_Natural` (Phase11 batch 261002-7; re-made 261031-1, 261101-1; lane L2).

Fresh, green oak leaves' upper surfaces, on a card: the Masked master cuts them out by the
`opacity` map. The OUTLINE is a pedunculate-oak leaf drawn by JUDGEMENT: obovate (widest past
the middle), five rounded lobes a side with rounded sinuses about halfway to the midrib, lobes
alternating a little left to right, a rounded terminal lobe, small ear-like auricles at the
base and a short stalk. Pinnate veins: a pale midrib and one secondary vein to each lobe, with
a fine net between. No scan fits: ambientCG's single-leaf sets (Leaf001-003) are tagged only
"green, leaf, single, tree", and the library names only what a source states, so the set is
generated.

MANY LEAVES a tile, scattered (the maintainer's redo, 261101-1: "we should redo the oak leaf";
laid as a surface, the 261031-1 tile's two leaves repeated in a grid every 10 cm). About 180
leaves on a 1 m tile, each with its own place, tilt, size, mirroring, lobing, midrib bow and
tone, overlapping where they fall, so no leaf or layout repeats inside a metre. A leaf may cross
the tile's border: every leaf is drawn on wrapped coordinates, in a window round itself.

The colour is a JUDGEMENT (the same redo: "a livelier leaf green"): the MEAN linear albedo over
the leaves is (0.075, 0.185, 0.028), sRGB about 77, 119, 47, a fresh mid green. It was anchored
to Physically Based `Grass` (0.105, 0.133, 0.041), whose olive read dull on a leaf; Physically
Based has no leaf entry. The roughness keeps that entry's 0.5 (a waxy cuticle).

Writes MatterLibrary/textures/base/environmental/vegetation/OakLeaf_Natural_<channel>_s1.png:
basecolor (sRGB-encoded), roughness, normal (linear data, NormalGL) and opacity (linear, the
cut-out). Scale `s1`: an exact 1 m tile at 2048 px (about 0.5 mm a texel), blades 4.5 to 7.5 cm
long. *(Was `s01`, two leaves in 0.1 m.)* Outside the leaves
the colour and roughness are padded with the leaves' own mean, so filtering at the cut edge
draws no fringe. Every noise wraps and every leaf is drawn wrapped, so the tile is seamless.
Fixed seed, no network.

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
SCALE = "s1"
SIZE = 2048
SEED = 707
LEAF = np.array([0.075, 0.185, 0.028])    # judgement: a fresh mid green, linear sRGB: the leaves' mean
VEIN = np.array([1.55, 1.40, 1.60])       # relative tint of a vein (paler, a little yellower)
STALK = np.array([1.5, 1.0, 2.2])         # relative tint of the stalk
ROUGH = 0.5                               # Physically Based `Grass` roughness: a waxy cuticle

# A leaf is drawn in its own frame: the blade from row BASE to row TIP of a unit square.
BASE, TIP = 0.90, 0.08
LENGTH = BASE - TIP
STALK_END = 0.975
HALF_W = 0.235                            # the envelope's peak half-width, leaf units
LOBES = 5
SINUS = 0.50                              # how far a sinus cuts toward the midrib (fraction of width)
SUPER = 4                                 # supersampling for the anti-aliased outline
LEAN = 0.45                               # a lobe's crest moves this far tipward per unit of width

GRID = 14                                 # leaves are scattered one to a cell of a GRID x GRID jitter
KEEP = 0.92                               # the share of cells that hold a leaf: a few gaps


def leaves() -> list:
    """The leaves on the tile: centre (x, y), tilt in degrees, size (a leaf unit in tiles: a blade
    is LENGTH of it), mirrored, lobe phases (right, left), midrib bow, tone (relative to LEAF,
    before re-anchoring). One per jittered cell, in a random order, so overlaps fall anyhow."""
    rng = np.random.RandomState(SEED + 50)
    out = []
    for gy in range(GRID):
        for gx in range(GRID):
            if rng.rand() > KEEP:
                continue
            out.append(dict(c=((gx + rng.rand()) / GRID, (gy + rng.rand()) / GRID),
                            tilt=rng.uniform(0, 360), size=rng.uniform(0.045, 0.075) / LENGTH,
                            mirror=bool(rng.rand() < 0.5),
                            phases=(rng.uniform(0, 0.6), rng.uniform(0, 0.6)),
                            bow=rng.uniform(-0.02, 0.02),
                            tone=tuple(1 + rng.uniform(-0.12, 0.12, 3))))
    return [out[i] for i in rng.permutation(len(out))]


def frame(X, Y, leaf):
    """Tile coordinates to the leaf's own frame (its blade upright in the unit square), wrapped."""
    dx = (X - leaf["c"][0] + 0.5) % 1.0 - 0.5
    dy = (Y - leaf["c"][1] + 0.5) % 1.0 - 0.5
    a = np.radians(leaf["tilt"])
    u = (np.cos(a) * dx + np.sin(a) * dy) / leaf["size"]
    v = (-np.sin(a) * dx + np.cos(a) * dy) / leaf["size"]
    if leaf["mirror"]:
        u = -u
    return 0.5 + u, 0.53 + v                                          # the blade's middle at the centre


def midrib_x(t, bow):
    return 0.5 + bow * np.sin(np.pi * t)


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


def lobe_crests(phase):
    """t of each lobe crest on one side (where lobing() == 1)."""
    crest_s = 0.5 ** (1 / 1.35)
    ts = []
    for k in range(-1, LOBES + 2):
        t = 0.06 + (k + crest_s - phase) * 0.80 / LOBES
        if 0.12 < t < 0.88:
            ts.append(t)
    return ts


def outline(X, Y, leaf) -> np.ndarray:
    """Coverage of one leaf's blade plus stalk (1 inside), at tile coordinates X, Y."""
    X, Y = frame(X, Y, leaf)
    t = (BASE - Y) / LENGTH
    dx = X - midrib_x(t, leaf["bow"])
    env = envelope(t)
    ts = t - LEAN * np.abs(dx) / LENGTH                                # lobes lean toward the tip
    ph = leaf["phases"]
    half = np.where(dx >= 0, env * lobing(ts, ph[0]), env * lobing(ts, ph[1]))
    blade = (t >= 0) & (t <= 1) & (np.abs(dx) < half)
    stalk = (Y > BASE - 0.01) & (Y < STALK_END) & (np.abs(X - midrib_x(0.0, leaf["bow"]) + 0.02 * (Y - BASE)) < 0.0055)
    return (blade | stalk).astype(float)


def seg_dist(X, Y, a, b):
    ab = np.subtract(b, a)
    t = np.clip(((X - a[0]) * ab[0] + (Y - a[1]) * ab[1]) / (ab @ ab), 0, 1)
    return np.hypot(X - (a[0] + t * ab[0]), Y - (a[1] + t * ab[1])), t


def veins(X, Y, leaf):
    """One leaf's (midrib, secondary, stalk) strengths in [0, 1] at tile coordinates X, Y."""
    X, Y = frame(X, Y, leaf)
    bow = leaf["bow"]
    t = (BASE - Y) / LENGTH
    w_mid = np.interp(t, [-0.1, 0.0, 1.0], [0.0050, 0.0050, 0.0012])
    d_mid = np.abs(X - midrib_x(np.clip(t, 0, 1), bow))
    midrib = np.clip(1 - d_mid / w_mid, 0, 1) * ((t > -0.10) & (t < 0.99))
    sec = np.zeros_like(X)
    for side, phase in zip((1, -1), leaf["phases"]):
        for tc in lobe_crests(phase):
            half = float(envelope(np.array([tc]))[0])
            tip_t = tc + LEAN * 0.93 * half / LENGTH                  # the leaning crest
            half = float(envelope(np.array([tip_t]))[0])
            tip = (midrib_x(tip_t, bow) + side * 0.90 * half, BASE - tip_t * LENGTH)
            t0 = tc - 0.07
            root = (midrib_x(t0, bow), BASE - t0 * LENGTH)
            mid = (root[0] + side * 0.5 * half, BASE - (0.5 * (t0 + tip_t) - 0.02) * LENGTH)  # a gentle bow
            for a, b, w0, w1 in ((root, mid, 0.0026, 0.0018), (mid, tip, 0.0018, 0.0007)):
                d, f = seg_dist(X, Y, np.array(a), np.array(b))
                w = w0 + (w1 - w0) * f
                sec = np.maximum(sec, np.clip(1 - d / w, 0, 1))
    stalk = (Y > BASE + 0.004).astype(float)
    return midrib, sec, stalk


def window(leaf, n):
    """The pixel rows and columns (wrapped) round one leaf, and their tile coordinates, plus the
    same at SUPER x SUPER sub-pixels for the outline."""
    h = int(np.ceil(0.62 * leaf["size"] * n)) + 2                      # the leaf frame's reach, rotated
    cx, cy = int(leaf["c"][0] * n), int(leaf["c"][1] * n)
    k = np.arange(-h, h)
    cols, rows = (cx + k) % n, (cy + k) % n
    x = (cx + k + 0.5) / n
    y = (cy + k + 0.5) / n
    X, Y = np.meshgrid(x, y)
    kb = (np.arange(2 * h * SUPER) + 0.5) / SUPER
    XB, YB = np.meshgrid((cx - h + kb) / n, (cy - h + kb) / n)
    return np.ix_(rows, cols), X, Y, XB, YB, 2 * h


def maps() -> dict:
    n = SIZE
    netw = 1 - np.abs(2 * tl.fbm((640, 1280), SEED + 5, n) - 1)       # ridged: a reticulate net
    net = np.clip((netw - 0.82) / 0.18, 0, 1)
    mottle = tl.fbm((60, 120, 240), SEED, n)                           # 4 to 16 mm: within a leaf
    fine = tl.fbm((512, 1024), SEED + 10, n)
    shade = 1.0 + 0.18 * (mottle - 0.5) + 0.05 * (fine - 0.5) + 0.05 * net

    cover = np.zeros((n, n))
    albedo = np.zeros((n, n, 3))
    vein_all = np.zeros((n, n))
    mid_all = np.zeros((n, n))
    sec_all = np.zeros((n, n))
    for leaf in leaves():                                             # later leaves lie on top
        ix, X, Y, XB, YB, m = window(leaf, n)
        cov = outline(XB, YB, leaf).reshape(m, SUPER, m, SUPER).mean(axis=(1, 3))
        midrib, sec, stalk = veins(X, Y, leaf)
        vein = np.maximum(midrib, 0.8 * sec)
        tint = 1 + vein[..., None] * (VEIN - 1)[None, None, :]
        tint = tint * (1 - stalk[..., None]) + STALK[None, None, :] * stalk[..., None]
        col = LEAF[None, None, :] * np.array(leaf["tone"])[None, None, :] * shade[ix][..., None] * tint
        albedo[ix] = albedo[ix] * (1 - cov[..., None]) + col * cov[..., None]
        vein_all[ix] = vein_all[ix] * (1 - cov) + vein * cov
        mid_all[ix] = mid_all[ix] * (1 - cov) + midrib * cov
        sec_all[ix] = sec_all[ix] * (1 - cov) + sec * cov
        cover[ix] = np.maximum(cover[ix], cov)
    inside = cover > 0.5
    albedo *= LEAF / albedo[inside].mean(0)                            # re-anchor the leaves' MEAN
    albedo[~inside] = LEAF                                              # pad: no fringe at the cut

    rough = np.clip(ROUGH + 0.05 * (fine - 0.5) + 0.04 * (mottle - 0.5) + 0.10 * vein_all, 0, 1)
    rough += ROUGH - rough[inside].mean()
    rough[~inside] = ROUGH

    # upper surface: the veins sit in shallow channels, the tissue between them bulges a little
    height = -1.0 * mid_all - 0.6 * sec_all - 0.15 * net + 0.35 * mottle + 0.15 * fine
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=1.0),
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
