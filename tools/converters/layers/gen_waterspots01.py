#!/usr/bin/env python3
"""Generate the shared overlay `WaterSpots01` (Phase11 step 11.3): dried water spots.

A GLOSS overlay (slot 2 or 3) for polished stone, glass, glazed ceramic, gloss paint and
metal: where a drop dried it left a thin mineral film, heaviest at its rim (the coffee-ring
effect), so each spot reads as a matte ring with a hazier inside. Small drops dry to solid
dots; some large ones show a second, inner tide line. Spots gather where a splash landed,
with a few strays between. Frozen overlay contract (MasterSet.md):

    R/G = normal XY (0.5 = flat)  ·  B = roughness bias (only roughens)  ·  A = density

The film is thin, so the normal is shallow; B carries the effect, as with Fingerprints01.
B is filled everywhere (not only inside a spot), because a renderer filters A and B
separately: a B masked to the spot would multiply down to almost nothing at a distance
(Phase11 F-P11-7, Scratches01 and Fingerprints01 too faint to see). Outside a spot A = 0,
so the B there never applies.

Scale `s01` (0.1 m tile, 0.1 mm per pixel): spots of 1-14 mm across. Picked by the feature's
real size (SKILL §3a step 3): at `s001` a 1 cm tile holds one or two of them. Spots wrap
toroidally, so the tile is seamless. Fixed seed, no network: byte-stable.

    gen_waterspots01.py [--out DIR]    # default: MatterLibrary/textures/shared/overlays/

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
NAME = "WaterSpots01_overlay_s01.png"
SEED = 601
SIZE = tl.SIZE
CLUSTERS = 8           # splashes per 0.1 m tile
STRAYS = 45            # lone drops between them


def _window(cx: float, cy: float, rad: float):
    """Wrapped row/column indices and offsets of a square window around (cx, cy)."""
    ys = np.arange(int(np.floor(cy - rad)), int(np.ceil(cy + rad)) + 1)
    xs = np.arange(int(np.floor(cx - rad)), int(np.ceil(cx + rad)) + 1)
    return ys % SIZE, xs % SIZE, (ys - cy)[:, None], (xs - cx)[None, :]


def spots() -> tuple:
    rng = np.random.RandomState(SEED)
    wobble = tl.fbm((24, 48, 96), SEED + 1) - 0.5               # irregular, not compass-drawn rims
    deposit = np.zeros((SIZE, SIZE))
    rims = np.zeros((SIZE, SIZE))
    centres = []
    for _ in range(CLUSTERS):
        cx, cy = rng.rand(2) * SIZE
        spread = 50 + rng.rand() * 130
        for _ in range(rng.randint(10, 28)):
            centres.append((cx + rng.randn() * spread, cy + rng.randn() * spread))
    for _ in range(STRAYS):
        centres.append(tuple(rng.rand(2) * SIZE))
    for cx, cy in centres:
        cx, cy = cx % SIZE, cy % SIZE
        r = 5.0 * (70.0 / 5.0) ** (rng.rand() ** 1.7)           # radius px; most drops small
        rows, cols, oy, ox = _window(cx, cy, r * 1.5 + 4)
        rho = np.sqrt(ox * ox + oy * oy) / r + 0.35 * wobble[np.ix_(rows, cols)]
        rw = 0.06 + 1.6 / r                                      # thin rims on big drops
        ring = np.exp(-((rho - 1.0) / rw) ** 2)
        if r < 12:                                               # a small drop dries to a dot
            film = np.clip(1.0 - rho, 0, 1) ** 0.35 * (0.7 + 0.3 * rng.rand())
        else:
            film = np.clip(1.0 - rho, 0, 1) ** 0.5 * (0.18 + 0.27 * rng.rand())
        if r > 25 and rng.rand() < 0.35:                         # an inner tide line
            ring = np.maximum(ring, 0.5 * np.exp(-((rho - 0.55 - 0.15 * rng.rand()) / rw) ** 2))
        strength = 0.65 + 0.35 * rng.rand()
        dep = np.maximum(ring, film) * strength
        sub = np.ix_(rows, cols)
        deposit[sub] = np.maximum(deposit[sub], dep)
        rims[sub] = np.maximum(rims[sub], ring * strength)
    return deposit, rims


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the WaterSpots01 shared overlay.")
    ap.add_argument("--out", default=str(ROOT / "MatterLibrary" / "textures" / "shared" / "overlays"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety)", file=sys.stderr)
        return 1
    deposit, rims = spots()
    img = tl.pack_overlay(deposit, strength=3.0,                 # a raised film, barely there
                          rough_bias=0.40 + 0.35 * rims,         # the rim is the mattest part
                          density=np.clip(deposit * 1.3, 0, 1))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
