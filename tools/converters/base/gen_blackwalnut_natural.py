#!/usr/bin/env python3
"""Generate the base texture set `BlackWalnut_Natural` (Phase11 batch 261002-2; lane L2).

Unfinished (sanded, no oil or lacquer) black walnut, flat-sawn: a chocolate-brown heartwood
with darker latewood bands every few millimetres, fine open pores that read as short dark
streaks along the grain, and broad, slow colour drift. No scan fits: ambientCG has no asset
that says walnut (its dark woods are tagged only "dark"/"espresso"), and the library names only
what a source states, so the set is generated. The colour is a JUDGEMENT, not invented per
pixel: the texture's mean linear albedo is anchored to (0.16, 0.085, 0.05) (sRGB about
112, 82, 63, unfinished black walnut heartwood); Physically Based has no wood entry.
Everything here only varies around it.

Writes MatterLibrary/textures/base/natural/wood/BlackWalnut_Natural_<channel>_s01.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s01`: a 0.1 m
tile, so the grain runs along U, about 22 growth rings cross the tile (~4.5 mm apart) and the
pores are ~0.1-0.3 mm wide. Seamless (periodic noise, integer ring count), fixed seed, no
network.

    gen_blackwalnut_natural.py [--out DIR]

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
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "natural" / "wood"
SET = "BlackWalnut_Natural"
SCALE = "s01"
SEED = 511
WALNUT = np.array([0.16, 0.085, 0.05])   # judgement: unfinished black walnut heartwood, linear sRGB
RINGS = 22                                # growth rings across the tile (integer: seamless in V)
SIZE = tl.SIZE


def noise2(sx: int, sy: int, seed: int, size: int = SIZE) -> np.ndarray:
    """Periodic value noise in [0, 1] on an sx (along U) x sy (along V) grid: tileable.noise
    with a different cell count per axis, so features stretch along the grain."""
    rng = np.random.RandomState(seed)
    grid = rng.rand(sy, sx)

    def axis(n):
        t = np.arange(size) * n / size
        i0 = np.floor(t).astype(int) % n
        f = t - np.floor(t)
        return i0, (i0 + 1) % n, f * f * (3 - 2 * f)

    y0, y1, fy = axis(sy)
    x0, x1, fx = axis(sx)
    rows = grid[y0] * (1 - fy)[:, None] + grid[y1] * fy[:, None]       # (size, sx)
    return rows[:, x0] * (1 - fx)[None, :] + rows[:, x1] * fx[None, :]


def maps() -> dict:
    v = np.arange(SIZE)[:, None] / SIZE                               # across the grain
    # Ring figure: bands across V, wandered by slow noise that is long along U.
    warp = (0.45 * (noise2(1, 3, SEED) - 0.5) + 0.25 * (noise2(2, 5, SEED + 1) - 0.5)
            + 0.10 * (noise2(3, 11, SEED + 6) - 0.5))
    uneven = 0.9 * (noise2(1, 9, SEED + 7) - 0.5)                    # irregular ring spacing
    phase = (RINGS * v + RINGS * 0.22 * warp + uneven) % 1.0
    # Latewood: a soft dark band (rises over ~40 % of the ring, falls over ~15 %).
    late = np.where(phase < 0.85, np.clip((phase - 0.45) / 0.40, 0, 1),
                    np.clip((1.0 - phase) / 0.15, 0, 1)) ** 1.5
    # Fibres: fine long streaks; pores: sparse thin dark dashes along U.
    fibre = 0.6 * noise2(6, 500, SEED + 2) + 0.4 * noise2(20, 900, SEED + 8)
    pores = np.clip((0.16 - noise2(36, 560, SEED + 3)) * 9, 0, 1) * (0.4 + 0.9 * late)
    streak = noise2(2, 26, SEED + 9)                                  # darker chocolate streaks
    drift = tl.fbm((2, 4), SEED + 4)                                  # broad colour drift
    tone = noise2(3, 6, SEED + 5)                                     # grey-violet vs warm cast

    shade = (1.0 - 0.28 * late + 0.22 * (fibre - 0.5) - 0.45 * pores
             - 0.30 * np.clip(streak - 0.55, 0, 1) * 2 + 0.25 * (drift - 0.5))
    albedo = WALNUT[None, None, :] * shade[..., None]
    cast = np.stack([1 + 0.06 * (tone - 0.5), np.ones_like(tone), 1 - 0.10 * (tone - 0.5)], -1)
    albedo = albedo * cast
    albedo *= WALNUT / albedo.reshape(-1, 3).mean(0)                  # re-anchor the MEAN exactly

    rough = np.clip(0.66 + 0.10 * pores + 0.04 * (fibre - 0.5) + 0.03 * late, 0, 1)
    height = 0.45 * fibre - 1.2 * pores + 0.10 * late
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=3.0)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the BlackWalnut_Natural base texture set.")
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
