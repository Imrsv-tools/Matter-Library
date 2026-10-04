#!/usr/bin/env python3
"""Generate the base texture set `Concrete_Polished` (lane L2).

Polished concrete: a cast slab ground flat, densified and polished, the clean floor of a
gallery or a showroom. The cement paste shows the soft clouding a power trowel and the
grinder leave, the fine aggregate shows as a faint salt-and-pepper speckle, and the face is
flat and glossy with a sheen that wanders a little from pass to pass.

The colour is GROUNDED, not invented: the texture's mean linear albedo is anchored to
Physically Based `Concrete`, (0.51, 0.51, 0.51). Its roughness (0.5, a cast face) is not
taken: the polish is a judgement, a mean of about 0.22.

Generated, not scanned: ambientCG has no concrete tagged polished (its clean, smooth ones
measure a mean roughness of 0.49 to 0.78), and none states a floor's physical size.

BUILT FOR LARGE FLOORS. The tile is 3 m, the largest the 1024 px map carries while a texel
stays about 3 mm, and nothing in it is a landmark: no stain, no crack, no single scratch.
The slowest feature is a fifth of the tile and the noise grids are mutually prime, so no
feature repeats inside the tile and the eye has nothing to count the repeats by.

Writes MatterLibrary/textures/base/engineered/cementitious/Concrete_Polished_<channel>_s1.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Seamless
(tileable.py), fixed seed, no network.

    gen_concrete_polished.py [--out DIR]

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
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "engineered" / "cementitious"
SET = "Concrete_Polished"
SCALE = "s1"
SEED = 4104
PB_CONCRETE = np.array([0.51, 0.51, 0.51])   # Physically Based `Concrete`, linear sRGB
ROUGH_MEAN = 0.22                            # judgement: a polished, densified floor


def maps() -> dict:
    # On a 3 m tile one pixel is about 3 mm.
    # Trowel and grinder clouding, 60 cm down to 10 cm. The slowest octave is the weakest,
    # so the tile's own period carries the least contrast.
    cloud = (0.20 * tl.noise(5, SEED) + 0.30 * tl.noise(9, SEED + 1)
             + 0.30 * tl.noise(17, SEED + 2) + 0.20 * tl.noise(31, SEED + 3))
    patch = tl.fbm((61, 127), SEED + 10)             # paste mottling: 5, 2.4 cm
    fine = tl.fbm((211, 421), SEED + 20)             # sand texture: 14, 7 mm
    grain = tl.noise(tl.SIZE, SEED + 30)             # salt and pepper, one pixel (3 mm)
    stones = tl.noise(347, SEED + 40)                # the odd larger grain, about 9 mm
    light = np.clip((stones - 0.86) * 9, 0, 1)
    dark = np.clip((0.12 - stones) * 9, 0, 1)
    pinholes = np.clip((0.02 - tl.noise(509, SEED + 50)) * 50, 0, 1)   # sparse, about 6 mm
    tone = tl.fbm((6, 11), SEED + 60)                # a faint warm-to-cool drift in the paste
    sheen = tl.fbm((7, 13, 29), SEED + 70)           # where the polish took more, or less

    shade = (1.0 + 0.22 * (cloud - 0.5) + 0.07 * (patch - 0.5) + 0.06 * (fine - 0.5)
             + 0.09 * (grain - 0.5) + 0.10 * light - 0.16 * dark - 0.12 * pinholes)
    drift = 1.0 + 0.02 * (tone - 0.5)[..., None] * np.array([1.0, 0.2, -1.0])
    albedo = PB_CONCRETE[None, None, :] * shade[..., None] * drift
    albedo *= PB_CONCRETE / albedo.reshape(-1, 3).mean(0)       # re-anchor the MEAN to PB exactly

    rough = 0.16 * (sheen - 0.5) + 0.06 * (patch - 0.5) + 0.02 * (grain - 0.5) + 0.35 * pinholes
    rough = np.clip(rough - rough.mean() + ROUGH_MEAN, 0.08, 0.7)

    # Near flat: a slab's slow waviness, a trace of sand texture, the pinholes as small pits.
    height = 0.6 * cloud + 0.05 * fine - 0.5 * pinholes
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=2.0)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Concrete_Polished base texture set.")
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
