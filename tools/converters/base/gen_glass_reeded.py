#!/usr/bin/env python3
"""Generate the base texture set `Glass_Reeded` (Phase11 batch 261002-5; lane L2).

Reeded (fluted) glass: rolled clear glass whose face is pressed into parallel, rounded ridges
(shower screens, cabinet doors, partitions). The glass itself is constant (its colour, IOR and
gloss are the recipe's, from Physically Based `Glass (Soda-lime)`), so this set is ONE map: the
**normal** (NormalGL, linear data). There is no basecolor or roughness map: a clear glass has
no albedo texture, and its fire-polished face is uniformly smooth.

**The reeds run along V** (down the tile): each is a circular-arc ridge, convex, about 10 mm
wide, whose flanks tilt to 30 degrees at the crease between two reeds. Scale `s001`: one reed
per 1 cm tile, so the tile repeats exactly as the reeds do. The crease sits mid-tile and the
reed's crown on the tile's edge, so the wrap is smooth. A faint low-frequency waviness along
each reed (the roller's own unevenness) keeps it from reading as machined.

Writes MatterLibrary/textures/base/engineered/glass/Glass_Reeded_normal_s001.png. Fixed seed,
no network.

    gen_glass_reeded.py [--out DIR]

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
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "engineered" / "glass"
SET = "Glass_Reeded"
SCALE = "s001"
SEED = 2011
SIZE = tl.SIZE
FLANK_DEG = 30.0          # the reed's slope at the crease


def maps() -> dict:
    half = SIZE / 2
    x = np.arange(SIZE) + 0.5
    u = np.where(x > half, x - SIZE, x)                       # distance from the reed's crown (px)
    radius = half / np.sin(np.radians(FLANK_DEG))             # arc whose flank reaches FLANK_DEG
    profile = np.sqrt(radius * radius - u * u)                # height in pixel units: slope is real
    height = np.tile(profile[None, :], (SIZE, 1))
    # The roller's unevenness: a slow swell along and across the reeds, tilting the face about 2 degrees.
    height = height + 20.0 * tl.fbm((2, 4), SEED)
    return {"normal": tl.normal_map(height, strength=1.0)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Glass_Reeded base texture set.")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args(argv)
    out = Path(args.out)
    targets = {ch: out / f"{SET}_{ch}_{SCALE}.png" for ch in ("normal",)}
    if any(p.exists() for p in targets.values()):
        print(f"refusing to overwrite {SET} in {out} (Build Safety); use --out <dir>", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)
    for ch, img in maps().items():
        img.save(targets[ch], "PNG", optimize=True)
        print(f"wrote {targets[ch]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
