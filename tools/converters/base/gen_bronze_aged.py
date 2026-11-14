#!/usr/bin/env python3
"""Generate the base texture set `Bronze_Aged` (Phase11 batch 261114-1; lane L2).

Aged architectural and statuary bronze: cast bronze whose surface has darkened to a deep brown
patina with years of air and handling, waxed now and then: doors, grilles, urns, statues. It
reads as AGED BRONZE, not as brown paint, because it is still metal: a dark, warm reflection
with a satin sheen, slightly uneven. This draws the patina's soft mottle (a few mm to 2 cm,
a little darker and cooler in places, a little warmer and brighter where it is thin), a fine
cast-and-chased skin, and a roughness that wanders with the mottle.

Generated, not scanned: ambientCG's bronzes are tagged eroded, rusted and scratched, and this
is a kept, waxed patina (the scans were not tried; a redo may). The colour is a JUDGEMENT: the mean
linear base colour is (0.20, 0.125, 0.062), sRGB about 124, 99, 71 as a metal's reflectance,
which is a bright bronze (about 0.71, 0.43, 0.18) darkened to a little under a third by its
patina; re-normalised so the mean is exact. Physically Based has no bronze entry. The mean
roughness is 0.38 (satin). Metalness is a constant 1 in the recipe.

Writes MatterLibrary/textures/base/engineered/metal/Bronze_Aged_<channel>_s01.png: basecolor
(sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s01`: a 0.1 m tile at
1024 px (about 0.1 mm a texel); nothing in it is larger than 2 cm and its contrast is low, so
the repeat shows no grid. Seamless (tileable.py), fixed seed, no network.

    gen_bronze_aged.py [--out DIR]

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
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "engineered" / "metal"
SET = "Bronze_Aged"
SCALE = "s01"
SEED = 6401
BRONZE = np.array([0.20, 0.125, 0.062])         # judgement: a patina-darkened bronze, linear sRGB
ROUGH_MEAN = 0.38
N = tl.SIZE


def maps() -> dict:
    mottle = tl.fbm((7, 13, 29, 61), SEED)                        # the patina's mottle, 3 mm to 1.5 cm
    thin = np.clip((tl.fbm((11, 23, 47), SEED + 1) - 0.5) * 2.2, 0, 1)   # where the patina is thin
    skin = tl.fbm((90, 180, 360), SEED + 2)                       # the cast and chased skin
    micro = tl.fbm((400, 512), SEED + 3)

    shade = 1.0 + 0.30 * (mottle - 0.5) + 0.35 * thin + 0.06 * (skin - 0.5)
    albedo = BRONZE[None, None, :] * shade[..., None]
    cool = np.array([0.92, 1.0, 1.10])                            # thick patina: darker, a little cooler
    warm = np.array([1.08, 1.0, 0.86])                            # thin patina: the metal's gold shows
    albedo = albedo * (1 + (cool - 1) * np.clip(1 - 2 * mottle, 0, 1)[..., None])
    albedo = albedo * (1 + (warm - 1) * thin[..., None])
    albedo *= BRONZE / albedo.reshape(-1, 3).mean(0)              # re-anchor the MEAN exactly
    albedo = np.clip(albedo, 0, 1)

    rough = -0.10 * thin - 0.10 * (mottle - 0.5) + 0.06 * (skin - 0.5) + 0.04 * (micro - 0.5)
    rough = np.clip(rough - rough.mean() + ROUGH_MEAN, 0.05, 1)
    height = 0.6 * skin + 0.15 * micro + 0.8 * mottle
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=2.0)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Bronze_Aged base texture set.")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args(argv)
    out = Path(args.out)
    targets = {ch: out / f"{SET}_{ch}_{SCALE}.png" for ch in ("basecolor", "roughness", "normal")}
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
