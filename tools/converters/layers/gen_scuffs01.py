#!/usr/bin/env python3
"""Generate the shared overlay `Scuffs01` (Phase03 step 3.4): broad rubbed scuff marks.

One script per wear layer (see gen_fingerprints01.py for the pattern); provenance names this
file. The frozen overlay channel contract:

    R/G = normal XY (0.5 = flat)  ·  B = roughness bias  ·  A = mask density

A scuff is a rub: something dragged across the surface. It dulls a band (B, roughness up),
leaves fine parallel drag lines inside it (a shallow directional normal), and has ragged
ends. It is the DAMAGE overlay (slot 1) for wood, stone, leather, plastics.

Scale `s01`: a 0.1 m tile, so a 3-8 cm scuff is 300-800 px long. Strokes wrap toroidally,
so the tile is seamless. Fixed seed, no network: byte-stable.

    gen_scuffs01.py [--out DIR]      # default: MatterLibrary/textures/shared/overlays/

It refuses to overwrite an existing file (AI_WorkingAgreement §Build Safety).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from gen_shared_textures import SIZE, SHARED, _gradients, _pack, _value_noise  # noqa: E402

NAME = "Scuffs01_overlay_s01.png"
SEED = 211
STROKES = 8


def scuffs() -> tuple:
    rng = np.random.RandomState(SEED)
    y, x = np.mgrid[0:SIZE, 0:SIZE].astype(np.float64)
    band = np.zeros((SIZE, SIZE))
    lines = np.zeros((SIZE, SIZE))
    ragged = _value_noise(SIZE, 110, seed=SEED + 1)             # fine break-up, not blobs
    for _ in range(STROKES):
        cx, cy = rng.rand(2) * SIZE
        length = 300 + rng.rand() * 500                          # px along the drag
        width = 14 + rng.rand() * 26                             # px across it
        th = rng.rand() * np.pi
        dx = (x - cx + SIZE / 2) % SIZE - SIZE / 2               # toroidal: seamless
        dy = (y - cy + SIZE / 2) % SIZE - SIZE / 2
        along = dx * np.cos(th) + dy * np.sin(th)
        across = -dx * np.sin(th) + dy * np.cos(th)
        t = np.exp(-(along / (length * 0.33)) ** 2)              # soft taper at both ends
        w = np.exp(-(across / (width * 0.45)) ** 2)              # soft edges, no hard sides
        stroke = t * w * np.clip(0.35 + (ragged - 0.5) * 1.3, 0, 1)
        # fine drag lines: high frequency ACROSS the stroke, constant along it
        drag = 0.5 + 0.5 * np.sin(across * (0.9 + rng.rand() * 0.6) + rng.rand() * 6.28)
        band = np.maximum(band, stroke)
        lines = np.where(stroke >= band, drag, lines)
    return band, lines


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Scuffs01 shared overlay.")
    ap.add_argument("--out", default=str(SHARED / "overlays"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety); use --out <dir> to reproduce elsewhere",
              file=sys.stderr)
        return 1
    band, lines = scuffs()
    height = band * (0.7 + 0.3 * lines)
    nx, ny = _gradients(height, strength=4.0)                    # shallow: a rub, not a gouge
    img = _pack(nx=nx, ny=ny,
                rough_bias=band * (0.35 + 0.25 * lines),         # the rubbed band goes dull
                density=np.clip(band * 1.2, 0, 1))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
