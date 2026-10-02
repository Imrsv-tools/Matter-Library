#!/usr/bin/env python3
"""Generate the shared overlay `HairlineScratches01` (Phase11 step 11.3): fine micro-scratches.

A DAMAGE overlay (slot 1) for polished and brushed metal, gems, clear and glossy plastics,
lacquer and glass: hundreds of hairline scratches, finer and far denser than Scratches01,
mostly running one way (the wipe or polish direction) with a few strays across them, each
a shallow groove tapering out at both ends. They gather in worn patches rather than covering
the tile evenly, so the surface hazes unevenly instead of going uniformly matte. Frozen
overlay contract (MasterSet.md):

    R/G = normal XY (0.5 = flat)  ·  B = roughness bias (only roughens)  ·  A = density

B is filled everywhere (a renderer filters A and B separately, so a B masked to a 1-pixel
line would multiply down to almost nothing at a distance; Phase11 F-P11-7, which is why
Scratches01 is too faint to see). Outside a scratch A = 0, so the B there never applies.

Scale `s001` (1 cm tile, 0.01 mm per pixel): scratches 6-25 µm wide and 1-10 mm long.
`s0001` (a 1 mm tile) would make each scratch shorter than a millimetre. Segments wrap
toroidally, so the tile is seamless. Fixed seed, no network: byte-stable.

    gen_hairlinescratches01.py [--out DIR]   # default: MatterLibrary/textures/shared/overlays/

It refuses to overwrite an existing file (AI_WorkingAgreement §Build Safety).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import tileable as tl  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent.parent
NAME = "HairlineScratches01_overlay_s001.png"
SEED = 631
SIZE = tl.SIZE
SCRATCHES = 430        # per 1 cm tile
DIRECTION = 0.12       # rad: the main wipe direction, a little off the U axis
STRAY = 0.10           # share of scratches at any angle (and shorter)


def scratches() -> tuple:
    rng = np.random.RandomState(SEED)
    wear = tl.fbm((3, 6, 12), SEED + 1)                          # worn patches
    lo, hi = np.quantile(wear, [0.30, 0.85])
    accept = np.clip((wear - lo) / (hi - lo), 0.06, 1.0)
    groove = np.zeros((SIZE, SIZE))
    cover = np.zeros((SIZE, SIZE))
    placed = 0
    while placed < SCRATCHES:
        cx, cy = rng.rand(2) * SIZE
        if rng.rand() > accept[int(cy), int(cx)]:
            continue
        placed += 1
        stray = rng.rand() < STRAY
        if stray:
            th = rng.rand() * np.pi
        else:
            th = DIRECTION + rng.randn() * 0.06                  # ~3.5 degrees of spread
        length = (100 + 900 * rng.rand() ** 1.6) * (0.45 if stray else 1.0)   # px
        hw = 0.3 + 0.9 * rng.rand() ** 2                         # half-width px
        depth = 0.35 + 0.65 * rng.rand()
        ux, uy = np.cos(th), np.sin(th)
        ax, ay = cx - ux * length / 2, cy - uy * length / 2
        pad = hw + 3
        x0, x1 = min(ax, ax + ux * length) - pad, max(ax, ax + ux * length) + pad
        y0, y1 = min(ay, ay + uy * length) - pad, max(ay, ay + uy * length) + pad
        xs = np.arange(int(np.floor(x0)), int(np.ceil(x1)) + 1)
        ys = np.arange(int(np.floor(y0)), int(np.ceil(y1)) + 1)
        px, py = xs[None, :] - ax, ys[:, None] - ay
        t = np.clip((px * ux + py * uy) / length, 0, 1)
        dist = np.hypot(px - t * length * ux, py - t * length * uy)
        taper = np.sin(np.pi * t) ** 0.4
        line = np.clip(hw + 0.5 - dist, 0, 1) * taper * depth    # anti-aliased groove
        wide = np.clip(hw + 1.0 - dist, 0, 1) * taper * (0.4 + 0.6 * depth)   # groove + walls
        sub = np.ix_(ys % SIZE, xs % SIZE)
        groove[sub] = np.maximum(groove[sub], line)
        cover[sub] = np.maximum(cover[sub], wide)
    return groove, cover


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the HairlineScratches01 shared overlay.")
    ap.add_argument("--out", default=str(ROOT / "MatterLibrary" / "textures" / "shared" / "overlays"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety)", file=sys.stderr)
        return 1
    groove, cover = scratches()
    img = tl.pack_overlay(-groove, strength=2.5,                 # shallow, but a sharp edge
                          rough_bias=0.55 + 0.15 * tl.noise(24, SEED + 2),
                          density=cover)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
