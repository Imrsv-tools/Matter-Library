#!/usr/bin/env python3
"""Generate the shared overlay `Cracks01` (Phase11 step 11.3): fine cracks and checking.

The DAMAGE overlay (slot 1) for weathered wood, concrete, render, plaster, dried soil crust
and old paint: a network of thin cracks around irregular cells, some edges open and some
still closed, with finer secondary cracks branching off the open ones. Each crack is a
V-shaped groove, so its two walls tilt opposite ways and the line reads dark under any
light, and its inside is rough. Frozen overlay contract (MasterSet.md):

    R/G = normal XY (0.5 = flat)  ·  B = roughness bias (only roughens)  ·  A = density

B is filled everywhere (a renderer filters A and B separately, so a B masked to the thin
crack would multiply down to almost nothing at a distance; Phase11 F-P11-7). Outside a crack
A = 0, so the B there never applies.

Scale `s01` (0.1 m tile, 0.1 mm per pixel): cells of ~1-3 cm, cracks 0.2-0.9 mm wide, the
secondary ones finer. The cell network is a Voronoi diagram on a warped, wrapped plane, so
the tile is seamless. Fixed seed, no network: byte-stable.

    gen_cracks01.py [--out DIR]        # default: MatterLibrary/textures/shared/overlays/

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
NAME = "Cracks01_overlay_s01.png"
SEED = 611
SIZE = tl.SIZE


def _wrap(d: np.ndarray) -> np.ndarray:
    return (d + SIZE / 2) % SIZE - SIZE / 2


def edge_distance(points: np.ndarray, X: np.ndarray, Y: np.ndarray) -> np.ndarray:
    """Distance (px) to the nearest Voronoi edge, on a torus: the exact distance to the
    bisector of the two nearest points."""
    d1 = np.full(X.shape, np.inf); d2 = np.full(X.shape, np.inf)
    i1 = np.zeros(X.shape, int); i2 = np.zeros(X.shape, int)
    for k, (px, py) in enumerate(points):
        d = np.hypot(_wrap(X - px), _wrap(Y - py))
        closer = d < d1
        second = ~closer & (d < d2)
        d2 = np.where(closer, d1, np.where(second, d, d2))
        i2 = np.where(closer, i1, np.where(second, k, i2))
        d1 = np.where(closer, d, d1)
        i1 = np.where(closer, k, i1)
    sep = np.hypot(_wrap(points[i1, 0] - points[i2, 0]), _wrap(points[i1, 1] - points[i2, 1]))
    return (d2 ** 2 - d1 ** 2) / (2 * np.maximum(sep, 1e-6))


def cracks() -> tuple:
    rng = np.random.RandomState(SEED)
    y, x = np.mgrid[0:SIZE, 0:SIZE].astype(np.float64)
    # warp the plane so the cell edges wander instead of running dead straight
    wx = (tl.fbm((6, 12, 24, 48), SEED + 1) - 0.5) * 70
    wy = (tl.fbm((6, 12, 24, 48), SEED + 2) - 0.5) * 70
    jx = (tl.noise(96, SEED + 3) - 0.5) * 6                      # a little jag at fine scale
    jy = (tl.noise(96, SEED + 4) - 0.5) * 6
    X, Y = (x + wx + jx) % SIZE, (y + wy + jy) % SIZE
    e1 = edge_distance(rng.rand(30, 2) * SIZE, X, Y)             # primary cells, ~2 cm
    e2 = edge_distance(rng.rand(110, 2) * SIZE, X, Y)            # secondary cells, ~1 cm

    # which edges have opened, and how far: most primary edges, a few secondary ones,
    # and those only near an open primary crack (so they read as branches off it)
    o1 = np.clip((tl.fbm((5, 10, 20), SEED + 5) - 0.36) * 4.0, 0, 1)
    o2 = np.clip((tl.fbm((8, 16, 32), SEED + 6) - 0.50) * 4.0, 0, 1)
    o2 *= np.clip(1.0 - e1 / 160.0, 0, 1) * np.clip(o1 * 2, 0, 1)
    w1 = 0.8 + 3.8 * o1                                          # half-width px: 0.1-0.46 mm
    w2 = 0.5 + 1.6 * o2
    g1 = np.clip(1.0 - e1 / w1, 0, 1) ** 0.8 * np.clip(o1 * 3, 0, 1)
    g2 = np.clip(1.0 - e2 / w2, 0, 1) ** 0.8 * np.clip(o2 * 3, 0, 1) * 0.75
    groove = np.maximum(g1, g2)
    # the density covers the groove and its walls (the bent normal), a little wider
    a1 = np.clip(1.0 - e1 / (w1 + 2.5), 0, 1) * np.clip(o1 * 3, 0, 1)
    a2 = np.clip(1.0 - e2 / (w2 + 2.0), 0, 1) * np.clip(o2 * 3, 0, 1)
    density = np.clip(np.maximum(a1, a2) * 1.4, 0, 1)
    return groove, density


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Cracks01 shared overlay.")
    ap.add_argument("--out", default=str(ROOT / "MatterLibrary" / "textures" / "shared" / "overlays"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety)", file=sys.stderr)
        return 1
    groove, density = cracks()
    img = tl.pack_overlay(-groove, strength=5.0,                 # a groove: steep walls
                          rough_bias=0.55 + 0.15 * tl.noise(40, SEED + 7),
                          density=density)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
