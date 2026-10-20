#!/usr/bin/env python3
"""Generate the shared overlay `HairlineScratches01` (Phase11 step 11.3): fine micro-scratches.

A DAMAGE overlay (slot 1) for polished and brushed metal, gems, clear and glossy plastics,
lacquer and glass: hundreds of hairline scratches, finer and far denser than Scratches01,
mostly running one way (the wipe or polish direction) with a few strays across them, each
a shallow groove tapering out at both ends. They cover the tile evenly, and any unevenness
is left to a mask: worn patches inside a tile repeat with it and read as a grid on highlights
(Phase11 F-P11-14). Frozen overlay contract (MasterSet.md):

    R/G = normal XY (0.5 = flat)  ·  B = roughness bias (only roughens)  ·  A = density

B is filled everywhere (a renderer filters A and B separately, so a B masked to a 1-pixel
line would multiply down to almost nothing at a distance; Phase11 F-P11-7, which is why
Scratches01 is too faint to see). Outside a scratch A = 0, so the B there never applies.

Scale `s01` (10 cm tile, 2048 px, 0.05 mm per pixel; the lead, 2026-10-20): scratches 1-10 mm
long, 6-25 µm wide, so each is narrower than a pixel and is drawn as a faint anti-aliased
line whose strength stands for its width. The texture holds sharp to about 14 cm from an HD
camera. A 1 cm tile (`s001`, the first version) repeated every 14 px of the parity rig's
close-up and read as a fine grain, worst in Blender (F-P11-14). Segments wrap toroidally, so
the tile is seamless. Fixed seed, no network: byte-stable.

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
NAME = "HairlineScratches01_overlay_s01.png"
SEED = 631
SIZE = 2048           # over 10 cm: 0.049 mm per pixel
PX_MM = 100 / SIZE
SCRATCHES = 43000      # per 10 cm tile: 430 per square centimetre
DIRECTION = 0.12       # rad: the main wipe direction, a little off the U axis
STRAY = 0.10           # share of scratches at any angle (and shorter)
# Matched to the 1 cm version, filtered to 0.1 and 0.5 mm per pixel: mean density 0.21, mean
# density x roughness bias 0.13, mean normal tilt 0.02 (0.1 mm), as before (2026-10-20).
LINE_GAIN = 1.0        # groove depth per pixel of width (sub-pixel lines)
COVER_GAIN = 1.8       # density per pixel of width
STRENGTH = 2.5         # normal strength


def scratches() -> tuple:
    rng = np.random.RandomState(SEED)
    rows = rng.permutation(SCRATCHES)                            # one band each, in random order:
    groove = np.zeros((SIZE, SIZE))
    cover = np.zeros((SIZE, SIZE))
    placed = 0
    while placed < SCRATCHES:
        cx = rng.rand() * SIZE                                   # evenly: no patches (F-P11-14), and
        cy = (rows[placed] + rng.rand()) / SCRATCHES * SIZE      # no bunching across the wipe direction
        placed += 1
        stray = rng.rand() < STRAY
        if stray:
            th = rng.rand() * np.pi
        else:
            th = DIRECTION + rng.randn() * 0.06                  # ~3.5 degrees of spread
        length = (1 + 9 * rng.rand() ** 1.6) * (0.45 if stray else 1.0) / PX_MM   # 1-10 mm, in px
        hw = (0.3 + 0.9 * rng.rand() ** 2) * 0.01 / PX_MM       # half-width 3-12 µm, in px (< 0.25)
        depth = 0.35 + 0.65 * rng.rand()
        ux, uy = np.cos(th), np.sin(th)
        ax, ay = cx - ux * length / 2, cy - uy * length / 2
        pad = 3
        x0, x1 = min(ax, ax + ux * length) - pad, max(ax, ax + ux * length) + pad
        y0, y1 = min(ay, ay + uy * length) - pad, max(ay, ay + uy * length) + pad
        xs = np.arange(int(np.floor(x0)), int(np.ceil(x1)) + 1)
        ys = np.arange(int(np.floor(y0)), int(np.ceil(y1)) + 1)
        px, py = xs[None, :] - ax, ys[:, None] - ay
        t = np.clip((px * ux + py * uy) / length, 0, 1)
        dist = np.hypot(px - t * length * ux, py - t * length * uy)
        taper = np.sin(np.pi * t) ** 0.4
        tent = np.clip(1 - dist, 0, 1)                           # a sub-pixel line, anti-aliased:
        line = tent * LINE_GAIN * hw * taper * depth             # its strength is its width
        wide = tent * min(1.0, COVER_GAIN * (hw + 0.01 / PX_MM)) * taper * (0.4 + 0.6 * depth)   # groove + walls
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
    img = tl.pack_overlay(-groove, strength=STRENGTH,            # shallow, but a sharp edge
                          rough_bias=0.55 + 0.15 * tl.noise(240, SEED + 2, SIZE),
                          density=cover)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
