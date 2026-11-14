#!/usr/bin/env python3
"""Generate the shared mask `Drip01` (Phase11 batch 261114-1): stains that ran down a wall.

A mask only GATES layers (never colour). Frozen mask contract (MasterSet.md):

    R = layer-2 coverage (TwoLayer only)  ·  G/B/A = where overlays 1/2/3 may appear

Drip01 is for upright surfaces that water runs down: plaster, render, stucco, painted walls,
concrete. Each channel is its own field, so the layers it gathers do not sit in the same places:

- R: large soft patches, ~45 % cover (a TwoLayer's second layer: damp, a stain);
- G: overlay 1 (damage: cracks, crazing) in medium patches, ~40 %;
- B: overlay 2 (a DEPOSIT: a water stain, dirt, soot, by its colour) as DRIP RUNS: streaks
  1 to 4 cm wide and 15 to 70 cm long that start dense at a head and thin and fade as they
  run, each wandering a little, a few of them joining; ~15 % cover, truly 0 between runs;
- A: overlay 3 in smaller scattered patches, ~30 %.

The runs go DOWN the picture (toward larger V rows): lay the article's UVs upright on a wall
(or turn them with `uv_rotation`) and the stains run down it. Scale `s1` (1 m tile, about
1 mm per pixel). Every field wraps, and a run that leaves the bottom re-enters at the top, so
the tile is seamless. Fixed seed, no network: byte-stable.

    gen_drip01.py [--out DIR]          # default: MatterLibrary/textures/shared/masks/

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
NAME = "Drip01_s1.png"
SEED = 6301
N = tl.SIZE
RUNS = 42


def patches(scales: tuple, seed: int, cover: float, edge: float) -> np.ndarray:
    """Soft patches covering `cover` of the tile (the field's own quantile), truly 0 elsewhere."""
    f = tl.fbm(scales, seed)
    t = np.quantile(f, 1 - cover)
    return np.clip((f - t) / edge, 0, 1)


def runs() -> np.ndarray:
    """The drip runs: each starts at a head and runs down, narrowing and fading; all wrap."""
    rng = np.random.RandomState(SEED + 10)
    out = np.zeros((N, N))
    cols = np.arange(N)
    wander = tl.fbm((6, 12, 24), SEED + 11)                       # sideways drift along a run
    for k in range(RUNS):
        x0, y0 = rng.rand() * N, int(rng.rand() * N)
        length = int((0.15 + 0.55 * rng.rand() ** 1.5) * N)
        width = (5 + 15 * rng.rand()) * (0.6 + 0.4 * length / (0.7 * N))   # half-width, texels
        strength = 0.55 + 0.45 * rng.rand()
        col = int(x0) % N
        for i in range(length):
            row = (y0 + i) % N
            t = i / length
            x = x0 + 28 * (wander[row, col] - wander[y0, col])
            w = width * (1 - 0.65 * t) * (0.75 + 0.25 * min(1.0, i / 12))  # a rounded head
            d = np.abs((cols - x + N / 2) % N - N / 2)
            prof = np.clip(1 - d / w, 0, 1) ** 1.5
            out[row] = np.maximum(out[row], strength * (1 - t) ** 0.8 * prof)
    ragged = 0.75 + 0.5 * (tl.fbm((64, 128), SEED + 12) - 0.5)   # a stain is never even
    return np.clip(out * ragged * 1.25, 0, 1)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Drip01 shared mask.")
    ap.add_argument("--out", default=str(ROOT / "MatterLibrary" / "textures" / "shared" / "masks"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety)", file=sys.stderr)
        return 1
    img = tl.pack_mask(
        r=patches((3, 5, 9), SEED + 1, 0.45, 0.10),               # layer-2 coverage
        g=patches((5, 9, 17), SEED + 2, 0.40, 0.08),              # overlay 1: damage patches
        b=runs(),                                                 # overlay 2: the drip runs
        a=patches((7, 13, 27), SEED + 3, 0.30, 0.07),             # overlay 3: scattered patches
    )
    a = np.asarray(img).astype(float) / 255
    print("cover R/G/B/A (share over 0.05):", [round(float((a[..., c] > 0.05).mean()), 3) for c in range(4)])
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
