#!/usr/bin/env python3
"""Generate the shared overlay `Pitting01` (Phase11 step 11.3): small pits and pores.

A DAMAGE overlay (slot 1, or 2-3 as a second damage layer) for corroded and cast metal,
porous stone, travertine, sandstone, weathered concrete, sand-blasted surfaces and leaves:
scattered round depressions, mostly tiny with a few larger ones, gathered in patches rather
than spread evenly. Each pit is a spherical dish, the larger ones with a slight raised lip,
and its inside is rough. Frozen overlay contract (MasterSet.md):

    R/G = normal XY (0.5 = flat)  ·  B = roughness bias (only roughens)  ·  A = density

B is filled everywhere (a renderer filters A and B separately, so a B masked to the pits
would multiply down to almost nothing at a distance; Phase11 F-P11-7). Outside a pit A = 0,
so the B there never applies.

Scale `s001` (1 cm tile, 0.01 mm per pixel): pits 0.07-0.6 mm across. Pits wrap toroidally,
so the tile is seamless. Fixed seed, no network: byte-stable.

    gen_pitting01.py [--out DIR]       # default: MatterLibrary/textures/shared/overlays/

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
NAME = "Pitting01_overlay_s001.png"
SEED = 621
SIZE = tl.SIZE
PITS = 900             # per 1 cm tile


def _window(cx: float, cy: float, rad: float):
    """Wrapped row/column indices and offsets of a square window around (cx, cy)."""
    ys = np.arange(int(np.floor(cy - rad)), int(np.ceil(cy + rad)) + 1)
    xs = np.arange(int(np.floor(cx - rad)), int(np.ceil(cx + rad)) + 1)
    return ys % SIZE, xs % SIZE, (ys - cy)[:, None], (xs - cx)[None, :]


def pits() -> tuple:
    rng = np.random.RandomState(SEED)
    cluster = tl.fbm((3, 6, 12), SEED + 1)                       # where pitting gathers
    lo, hi = np.quantile(cluster, [0.15, 0.85])
    accept = np.clip((cluster - lo) / (hi - lo), 0.08, 1.0)
    rough_rim = tl.noise(160, SEED + 2) - 0.5                    # not quite round
    dish = np.zeros((SIZE, SIZE))
    lip = np.zeros((SIZE, SIZE))
    cover = np.zeros((SIZE, SIZE))
    placed = 0
    while placed < PITS:
        cx, cy = rng.rand(2) * SIZE
        if rng.rand() > accept[int(cy), int(cx)]:
            continue
        placed += 1
        r = 3.5 * (30.0 / 3.5) ** (rng.rand() ** 2.6)            # radius px; most pits tiny
        depth = 0.6 + 0.4 * rng.rand()
        rows, cols, oy, ox = _window(cx, cy, r * 1.4 + 3)
        rho = np.sqrt(ox * ox + oy * oy) / r + 0.12 * rough_rim[np.ix_(rows, cols)]
        d = np.sqrt(np.clip(1.0 - rho * rho, 0, 1)) * depth      # a spherical dish
        lp = np.exp(-((rho - 1.08) / 0.12) ** 2) * (0.3 if r > 12 else 0.0)
        c = np.clip((1.2 - rho) / 0.2, 0, 1)                      # the dish and its rim
        sub = np.ix_(rows, cols)
        dish[sub] = np.maximum(dish[sub], d)
        lip[sub] = np.maximum(lip[sub], lp)
        cover[sub] = np.maximum(cover[sub], c)
    return lip * (dish < 0.01) - dish, cover


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Pitting01 shared overlay.")
    ap.add_argument("--out", default=str(ROOT / "MatterLibrary" / "textures" / "shared" / "overlays"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety)", file=sys.stderr)
        return 1
    height, cover = pits()
    img = tl.pack_overlay(height, strength=9.0,                  # a dish: clearly bent
                          rough_bias=0.50 + 0.20 * tl.noise(24, SEED + 3),
                          density=cover)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
