#!/usr/bin/env python3
"""Generate the shared overlay `Creases01` (Phase11 wish list): fold lines pressed into cloth.

One script per wear layer (see gen_fingerprints01.py for the pattern); provenance names this
file. The frozen overlay channel contract:

    R/G = normal XY (0.5 = flat)  ·  B = roughness bias  ·  A = mask density

A crease is where cloth was folded and pressed: a sharp, narrow valley (1.5-3 mm) along a
near-straight line 5-30 cm long, with a soft shoulder either side (the fold's memory, ~1-2
cm), tapering out at both ends. On a pile or a nap the fold crushes the fibres, so the line
also changes the surface's roughness (B). It is a second overlay (slot 2) for textiles and
leather; overlay 1 stays the damage layer.

Creases come in loose families (cloth folds roughly one way, then another), so each crease
takes one of three dominant directions, jittered. B is filled over each crease's shoulder, not
only its valley (Phase11, F-P11-8): a renderer filters A and B separately and multiplies them.

Scale `s1`: creases are garment-sized, so a 1 m tile at ~1 mm per pixel; on a 10 cm tile they
were too short, and the tile's repeat showed as a grid. Creases wrap toroidally, so the tile
is seamless. Fixed seed, no network: byte-stable.

    gen_creases01.py [--out DIR]      # default: MatterLibrary/textures/shared/overlays/

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

NAME = "Creases01_overlay_s1.png"
SEED = 1102
CREASES = 45


def creases() -> tuple:
    rng = np.random.RandomState(SEED)
    y, x = np.mgrid[0:SIZE, 0:SIZE].astype(np.float64)
    families = rng.rand(3) * np.pi                               # the folds' dominant directions
    wobble = tl.fbm((6, 12), SEED + 1) - 0.5                     # bends each line gently
    valley = np.zeros((SIZE, SIZE))
    shoulder = np.zeros((SIZE, SIZE))
    for _ in range(CREASES):
        cx, cy = rng.rand(2) * SIZE
        th = families[rng.randint(3)] + (rng.rand() - 0.5) * 0.8
        length = 50 + rng.rand() * 250                           # px: 5-30 cm
        sharp = 1.2 + rng.rand() * 1.3                           # valley half-width, px: 1-2.5 mm
        soft = 6 + rng.rand() * 8                                # shoulder, px: ~1-2 cm across
        bend = (rng.rand() - 0.5) * 0.5 / length                 # a gentle arc: creases run near straight
        dx = (x - cx + SIZE / 2) % SIZE - SIZE / 2               # toroidal: seamless
        dy = (y - cy + SIZE / 2) % SIZE - SIZE / 2
        along = dx * np.cos(th) + dy * np.sin(th)
        across = -dx * np.sin(th) + dy * np.cos(th) - bend * along ** 2 - 6 * wobble
        taper = np.exp(-(along / (length * 0.45)) ** 4)          # long, then fading at the ends
        valley = np.maximum(valley, taper * np.exp(-np.abs(across) / sharp))
        shoulder = np.maximum(shoulder, taper * np.exp(-(across / soft) ** 2))
    return valley, shoulder


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Creases01 shared overlay.")
    ap.add_argument("--out", default=str(SHARED / "overlays"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety); use --out <dir> to reproduce elsewhere",
              file=sys.stderr)
        return 1
    valley, shoulder = creases()
    height = 0.35 * shoulder - valley                            # a pressed valley in a raised fold
    img = tl.pack_overlay(height, strength=3.0,
                          rough_bias=np.clip(0.25 * shoulder + 0.35 * valley, 0, 1),  # crushed fibre
                          density=np.clip(np.maximum(valley, 0.8 * shoulder) * 1.2, 0, 1))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
