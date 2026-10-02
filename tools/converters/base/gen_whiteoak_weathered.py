#!/usr/bin/env python3
"""Generate the base texture set `WhiteOak_Weathered` (Phase11 batch 261002-3; lane L2).

Weathered white oak, flat-sawn: years outdoors have bleached the wood to a silver-grey, washed
the soft earlywood out so the harder latewood bands stand proud (a raised, ribbed grain), left
the pores as dark open streaks, scattered the oak's medullary rays as short pale dashes along
the grain, and laid darker grey-brown streaks of weathering where water runs. No scan fits:
ambientCG has no asset that says white oak or weathered oak (its weathered woods are siding
shingles, an assembly), and the library names only what a source states, so the set is
generated. The colour is a JUDGEMENT, not invented per pixel: the texture's mean linear albedo
is anchored to (0.23, 0.215, 0.19) (sRGB about 132, 128, 121, silver-grey weathered oak);
Physically Based has no wood entry. Everything here only varies around it. The checks (drying
splits) are NOT drawn here: they are the article's Cracks01 wear layer, dialled up by the app.

Writes MatterLibrary/textures/base/natural/wood/WhiteOak_Weathered_<channel>_s01.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s01`: a 0.1 m
tile, so the grain runs along U, about 30 growth rings cross the tile (~3.3 mm apart, white
oak's usual spacing) and the pores are ~0.1-0.3 mm wide. Seamless (periodic noise, integer
ring count), fixed seed, no network.

    gen_whiteoak_weathered.py [--out DIR]

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
SET = "WhiteOak_Weathered"
SCALE = "s01"
SEED = 907
OAK = np.array([0.23, 0.215, 0.19])      # judgement: silver-grey weathered oak, linear sRGB
RINGS = 30                                # growth rings across the tile (integer: seamless in V)
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
    warp = (0.45 * (noise2(1, 3, SEED) - 0.5) + 0.25 * (noise2(2, 5, SEED + 1) - 0.5)
            + 0.10 * (noise2(3, 11, SEED + 6) - 0.5))
    uneven = 0.9 * (noise2(1, 9, SEED + 7) - 0.5)                    # irregular ring spacing
    phase = (RINGS * v + RINGS * 0.22 * warp + uneven) % 1.0
    # Latewood: a band over ~45 % of the ring; weathering leaves it standing proud, and it
    # holds grime, so it reads a darker grey-brown than the bleached, eroded earlywood.
    late = np.where(phase < 0.85, np.clip((phase - 0.40) / 0.45, 0, 1),
                    np.clip((1.0 - phase) / 0.15, 0, 1)) ** 1.2
    fibre = 0.6 * noise2(6, 500, SEED + 2) + 0.4 * noise2(20, 900, SEED + 8)
    # Oak's large earlywood pores: dark open dashes, densest in the earlywood.
    pores = np.clip((0.16 - noise2(40, 600, SEED + 3)) * 8, 0, 1) * (1.2 - 0.8 * late)
    # Medullary rays: sparse short pale flecks along the grain.
    rays = np.clip((noise2(70, 260, SEED + 10) - 0.86) * 9, 0, 1)
    streak = noise2(3, 18, SEED + 9)                                  # water-run weathering
    drift = tl.fbm((2, 4), SEED + 4)
    tone = noise2(3, 6, SEED + 5)                                     # grey vs faint brown cast

    shade = (1.0 - 0.24 * (late - 0.5) + 0.20 * (fibre - 0.5) - 0.35 * pores + 0.25 * rays
             - 0.35 * np.clip(streak - 0.6, 0, 1) * 2.5 + 0.22 * (drift - 0.5))
    albedo = OAK[None, None, :] * shade[..., None]
    cast = np.stack([1 + 0.05 * (tone - 0.5), np.ones_like(tone), 1 - 0.08 * (tone - 0.5)], -1)
    albedo = albedo * cast
    albedo *= OAK / albedo.reshape(-1, 3).mean(0)                     # re-anchor the MEAN exactly

    rough = np.clip(0.80 + 0.08 * pores + 0.05 * (fibre - 0.5) - 0.04 * late, 0, 1)
    height = 0.45 * fibre - 1.4 * pores + 0.9 * late                  # raised latewood ribs
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=3.0)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the WhiteOak_Weathered base texture set.")
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
