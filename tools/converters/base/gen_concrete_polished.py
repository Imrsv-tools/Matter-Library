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

BUILT FOR LARGE FLOORS. The tile is exactly 1 m, the s1 scale option (Phase19 D-9; it was
3 m until 2026-10-31, off its tag), at 1024 px, so a texel is about 1 mm. Nothing in it is
a landmark: no stain, no crack, no single scratch. The slowest feature is half the tile and
the weakest, and the noise grids are mutually prime, so no feature repeats inside the tile
and the eye has little to count the repeats by on a floor many tiles wide.

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


def spots(n: int, seed: int, radius: float, share: float) -> np.ndarray:
    """Soft, irregular spots on a random `share` of an n x n cell grid: each spot's radius is
    `radius` (in cell units) times 0.4 to 1, and its outline is bent by a periodic warp."""
    warp = (0.25 * (tl.noise(4 * n, seed + 2) - 0.5), 0.25 * (tl.noise(4 * n, seed + 3) - 0.5))
    d1, _, cid = tl.cells(n, seed, warp=warp)
    rng = np.random.RandomState(seed + 1)
    keep, size = rng.rand(n * n)[cid] < share, (0.4 + 0.6 * rng.rand(n * n))[cid]
    r = radius * size
    return np.clip((r - d1) / (0.3 * r), 0, 1) * keep


def maps() -> dict:
    # On a 1 m tile one pixel is about 1 mm.
    # Trowel and grinder clouding, 50 cm down to 9 cm. The slowest octave is the weakest,
    # so the tile's own period carries the least contrast.
    cloud = (0.10 * tl.noise(2, SEED) + 0.25 * tl.noise(3, SEED + 1)
             + 0.35 * tl.noise(7, SEED + 2) + 0.30 * tl.noise(11, SEED + 3))
    patch = tl.fbm((19, 41), SEED + 10)              # paste mottling: 5, 2.4 cm
    fine = tl.fbm((71, 143), SEED + 20)              # sand texture: 14, 7 mm
    grain = tl.noise(341, SEED + 30)                 # salt and pepper, about 3 mm
    # The odd larger grain (about 8 mm) and the sparse pinholes (about 3 mm) are round spots
    # around cell points, not thresholded value noise, whose grid shows as square marks at 1 mm
    # a pixel.
    light, dark = spots(60, SEED + 40, 0.24, 0.14), spots(60, SEED + 41, 0.24, 0.12)
    pinholes = spots(90, SEED + 50, 0.13, 0.06)
    tone = tl.fbm((2, 5), SEED + 60)                 # a faint warm-to-cool drift in the paste
    sheen = tl.fbm((2, 5, 11), SEED + 70)            # where the polish took more, or less

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
