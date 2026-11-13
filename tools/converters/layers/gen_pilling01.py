#!/usr/bin/env python3
"""Generate the shared overlay `Pilling01` (Phase11 wish list): bobbles of tangled fibre on cloth.

One script per wear layer (see gen_fingerprints01.py for the pattern); provenance names this
file. The frozen overlay channel contract:

    R/G = normal XY (0.5 = flat)  ·  B = roughness bias  ·  A = mask density

A pill is a ball of loose fibre ends rubbed into a knot, 1-3 mm across, standing proud of the
cloth. It is the DAMAGE overlay (slot 1) for textiles: knits, fleece, nylon, velvet. Pills
thicken where cloth rubs: a gentle low-frequency field thins and thickens them, never to bare
cloth (distinct clusters would show the 10 cm tile's repeat as a grid). Each pill is a rounded bump (the normal), matte and fuzzy
(B up), and a faint halo of loosened fibre surrounds it.

B is filled through the whole rubbed field, not only on the pills (Phase11, F-P11-8): a
renderer filters A and B separately and multiplies them, and a B that is 0 between the pills
would collapse to almost nothing at a distance. A is 0 away from a pill's halo, so the cloth
there stays untouched.

Scale `s01`: a 0.1 m tile at ~0.1 mm per pixel, so a pill is 10-30 px across and a tile holds
~1000 of them. Pills wrap toroidally, so the tile is seamless. Fixed seed, no network.

    gen_pilling01.py [--out DIR]      # default: MatterLibrary/textures/shared/overlays/

It refuses to overwrite an existing file (AI_WorkingAgreement §Build Safety).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import tileable as tl  # noqa: E402
from gen_shared_textures import SIZE, SHARED  # noqa: E402

NAME = "Pilling01_overlay_s01.png"
SEED = 1101
CANDIDATES = 1600      # pill sites tried; the rub field keeps about two thirds


def splat(acc: np.ndarray, cx: float, cy: float, radius: float, fn) -> None:
    """Add fn(r / radius) around (cx, cy) into acc, wrapping at the tile edge."""
    k = int(np.ceil(radius * 2.2))
    ys = np.arange(int(cy) - k, int(cy) + k + 1)
    xs = np.arange(int(cx) - k, int(cx) + k + 1)
    yy, xx = np.meshgrid(ys, xs, indexing="ij")
    r = np.hypot(xx - cx, yy - cy) / radius
    np.add.at(acc, (yy % SIZE, xx % SIZE), fn(r))


def pilling() -> tuple:
    rng = np.random.RandomState(SEED)
    # where the cloth rubs: a gentle thinning and thickening, never bare islands. Distinct
    # clusters line up into a visible grid when a 10 cm tile repeats; the variation you see
    # from afar is the article's mask's job.
    zones = tl.fbm((8, 16, 32), SEED + 1)
    zones = 0.45 + 0.55 * np.clip((zones - 0.35) / 0.3, 0, 1)
    fuzz = tl.fbm((96, 192), SEED + 2)                          # loose fibre texture
    dome = np.zeros((SIZE, SIZE))
    halo = np.zeros((SIZE, SIZE))
    for _ in range(CANDIDATES):
        cx, cy = rng.rand(2) * SIZE
        if rng.rand() > zones[int(cy), int(cx)]:
            continue
        radius = 5 + rng.rand() * 10                            # 10-30 px across: 1-3 mm
        splat(dome, cx, cy, radius, lambda r: np.clip(1 - r * r, 0, 1) ** 0.6)
        splat(halo, cx, cy, radius * 2.0, lambda r: np.exp(-r * r * 2.0))
    dome = np.clip(dome, 0, 1)
    halo = np.clip(halo, 0, 1)
    return zones, dome, halo, fuzz


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Pilling01 shared overlay.")
    ap.add_argument("--out", default=str(SHARED / "overlays"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety); use --out <dir> to reproduce elsewhere",
              file=sys.stderr)
        return 1
    zones, dome, halo, fuzz = pilling()
    height = dome * (0.85 + 0.3 * fuzz) + 0.15 * halo * fuzz
    rough = np.clip(0.30 * zones + 0.25 * halo + 0.35 * dome, 0, 1)   # the rubbed patch goes matte
    density = np.clip(np.maximum(dome, 0.6 * halo) * 1.2, 0, 1)
    img = tl.pack_overlay(height, strength=10.0, rough_bias=rough, density=density)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
