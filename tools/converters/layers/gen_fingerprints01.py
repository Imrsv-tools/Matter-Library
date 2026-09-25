#!/usr/bin/env python3
"""Generate the shared overlay `Fingerprints01` (Phase03 step 3.3): oily fingerprint smudges.

One script per wear layer, so a layer's provenance evidence names exactly one file
(library/provenance/sources/shared/overlays/Fingerprints01.yaml). The packing helpers are
reused from gen_shared_textures.py, and the channel contract is the same frozen one:

    R/G = normal XY (0.5 = flat)  ·  B = roughness bias  ·  A = mask density

A fingerprint is an oil film: it barely bends the normal, and it HAZES a smooth surface, so B
(roughness bias) carries most of the effect. An overlay can only roughen (MasterSet.md), which
is exactly what a greasy print does to glass or polished metal.

Scale `s01`: one tile is 0.1 m, so a ~18 mm print is ~180 px across at 1024 px. Prints are
placed with toroidal wrap, so the tile is seamless. Fixed seed, no network: byte-stable.

    gen_fingerprints01.py [--out DIR]      # default: MatterLibrary/textures/shared/overlays/

It refuses to overwrite an existing file (AI_WorkingAgreement §Build Safety). To check it
reproduces the shipped bytes, write to another folder and compare.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from gen_shared_textures import SIZE, SHARED, _gradients, _pack, _value_noise  # noqa: E402

NAME = "Fingerprints01_overlay_s01.png"
SEED = 101
PRINTS = 7             # prints per 0.1 m tile
RIDGE_PERIOD_PX = 5.0  # ~0.5 mm ridge spacing at 0.1 mm per pixel


def fingerprints() -> np.ndarray:
    rng = np.random.RandomState(SEED)
    y, x = np.mgrid[0:SIZE, 0:SIZE].astype(np.float64)
    film = np.zeros((SIZE, SIZE))
    ridges_all = np.zeros((SIZE, SIZE))
    warp = _value_noise(SIZE, 32, seed=SEED + 1) - 0.5          # bends ridges into whorls
    for _ in range(PRINTS):
        cx, cy = rng.rand(2) * SIZE
        a = 70 + rng.rand() * 30                                 # semi-major radius, px
        b = a * (0.62 + rng.rand() * 0.12)
        th = rng.rand() * np.pi
        dx = (x - cx + SIZE / 2) % SIZE - SIZE / 2               # toroidal wrap: seamless
        dy = (y - cy + SIZE / 2) % SIZE - SIZE / 2
        u = dx * np.cos(th) + dy * np.sin(th)
        v = -dx * np.sin(th) + dy * np.cos(th)
        r = np.sqrt((u / a) ** 2 + (v / b) ** 2)
        envelope = np.clip(1.0 - r ** 2, 0, 1) ** 0.7
        # a partial, pressed print: some of each ellipse never touched the surface
        envelope *= np.clip((_value_noise(SIZE, 24, seed=int(rng.randint(1, 10**6))) - 0.25) * 2.5, 0, 1)
        ridges = 0.5 + 0.5 * np.cos(2 * np.pi * (r * a + warp * 18) / RIDGE_PERIOD_PX)
        film = np.maximum(film, envelope)
        ridges_all = np.where(envelope >= film, ridges, ridges_all)
    return film, ridges_all


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Fingerprints01 shared overlay.")
    ap.add_argument("--out", default=str(SHARED / "overlays"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety); use --out <dir> to reproduce elsewhere",
              file=sys.stderr)
        return 1
    film, ridges = fingerprints()
    height = film * (0.6 + 0.4 * ridges)
    nx, ny = _gradients(height, strength=2.0)                   # an oil film barely bends light
    img = _pack(nx=nx, ny=ny,
                rough_bias=film * (0.30 + 0.40 * ridges),        # the smudge hazes the surface
                density=np.clip(film * (0.55 + 0.45 * ridges) * 1.3, 0, 1))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
