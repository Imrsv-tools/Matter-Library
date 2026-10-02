#!/usr/bin/env python3
"""Generate the base texture set `NephriteJade_Polished` (Phase11 batch 261002-3; lane L2).

Polished nephrite jade: a tough, felted mass of fine amphibole fibres, cut and polished to a
soft, waxy lustre. Its look is a deep leaf-green, cloudy rather than banded: paler and darker
green clouds drift through it, a faint fibrous streak runs one way, and the odd small black
speck (a chromite or magnetite grain, as in "spinach" nephrite) sits in it. No scan fits: the
wish list plans it generated (L2), and ambientCG has no jade asset. The colour is a JUDGEMENT,
not invented per pixel: the texture's mean linear albedo is anchored to (0.055, 0.14, 0.065)
(sRGB about 66, 105, 72, a medium-green nephrite); Physically Based has no jade entry.
Everything here only varies around it.

Writes MatterLibrary/textures/base/natural/stone/NephriteJade_Polished_<channel>_s01.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s01`: a 0.1 m
tile, so the clouds are 1-3 cm across and the specks under a millimetre. The polish leaves
the normal almost flat. Seamless (periodic noise), fixed seed, no network.

    gen_nephritejade_polished.py [--out DIR]

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
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "natural" / "stone"
SET = "NephriteJade_Polished"
SCALE = "s01"
SEED = 1217
JADE = np.array([0.055, 0.14, 0.065])     # judgement: medium-green nephrite, linear sRGB
SIZE = tl.SIZE


def noise2(sx: int, sy: int, seed: int, size: int = SIZE) -> np.ndarray:
    """Periodic value noise in [0, 1] on an sx (along U) x sy (along V) grid, so features
    stretch along U (the fibres' drift)."""
    rng = np.random.RandomState(seed)
    grid = rng.rand(sy, sx)

    def axis(n):
        t = np.arange(size) * n / size
        i0 = np.floor(t).astype(int) % n
        f = t - np.floor(t)
        return i0, (i0 + 1) % n, f * f * (3 - 2 * f)

    y0, y1, fy = axis(sy)
    x0, x1, fx = axis(sx)
    rows = grid[y0] * (1 - fy)[:, None] + grid[y1] * fy[:, None]
    return rows[:, x0] * (1 - fx)[None, :] + rows[:, x1] * fx[None, :]


def specks(n: int, seed: int) -> np.ndarray:
    """n small round dark specks (0.2-0.8 mm), drawn with wrap-around so the tile stays seamless."""
    rng = np.random.RandomState(seed)
    yy, xx = np.mgrid[0:SIZE, 0:SIZE]
    out = np.zeros((SIZE, SIZE))
    for _ in range(n):
        cx, cy = rng.rand(2) * SIZE
        r = 1.5 + rng.rand() * 3.5
        dx = (xx - cx + SIZE / 2) % SIZE - SIZE / 2
        dy = (yy - cy + SIZE / 2) % SIZE - SIZE / 2
        out = np.maximum(out, np.clip(1.5 - np.sqrt(dx * dx + dy * dy) / r, 0, 1))
    return np.clip(out, 0, 1)


def maps() -> dict:
    clouds = tl.fbm((3, 6, 12), SEED)                     # paler and darker green clouds
    wisps = 0.6 * noise2(4, 24, SEED + 1) + 0.4 * noise2(9, 60, SEED + 2)   # fibrous streak
    felt = tl.fbm((96, 192), SEED + 3)                    # the fine felted texture
    pale = np.clip((tl.fbm((4, 8), SEED + 4) - 0.62) * 4, 0, 1)   # milky, paler patches
    inky = np.clip((tl.fbm((6, 12, 24), SEED + 6) - 0.52) * 3.5, 0, 1)   # deeper green mottles
    dark = specks(12, SEED + 5) * tl.fbm((64, 128), SEED + 7)

    shade = (1.0 + 0.70 * (clouds - 0.5) + 0.18 * (wisps - 0.5) + 0.08 * (felt - 0.5)
             - 0.45 * inky)
    albedo = JADE[None, None, :] * shade[..., None]
    milky = np.array([0.20, 0.27, 0.19])                  # a paler, greyer green
    albedo = albedo * (1 - 0.6 * pale[..., None]) + milky[None, None, :] * 0.6 * pale[..., None]
    albedo = albedo * (1 - 0.85 * dark[..., None])        # near-black specks
    albedo *= JADE / albedo.reshape(-1, 3).mean(0)        # re-anchor the MEAN exactly

    rough = np.clip(0.14 + 0.03 * (felt - 0.5) + 0.03 * (wisps - 0.5) + 0.04 * dark, 0, 1)
    height = 0.15 * felt + 0.10 * wisps                   # polished: almost flat
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=1.0)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the NephriteJade_Polished base texture set.")
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
