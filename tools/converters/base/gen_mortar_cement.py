#!/usr/bin/env python3
"""Generate the base texture set `Mortar_Cement` (Phase11 batch 261114-1; lane L2).

A cement-lime bedding mortar, as it sits in a struck joint between bricks, stones or tiles:
a grey-brown binder paste holding SAND. It reads as mortar, not as concrete, because the
sand is everything: grains 0.3 to 2 mm, most of them tan quartz, a few dark, a few white,
each standing slightly proud of the paste, with small round air voids between them and no
coarse aggregate at all.

No scan fits: ambientCG's mortar assets are brick walls (assemblies, not matter), so the set
is generated. The colour is a JUDGEMENT: the mean linear albedo is (0.33, 0.30, 0.25), sRGB
about 155, 148, 136, a grey-brown sandy mortar, re-normalised so the mean is exact. It is
darker than Physically Based `Concrete` (0.51) on purpose: a joint sits in shadow, and the
article is tinted DOWN for a dark or sooted joint. The mean roughness is 0.93.

Writes MatterLibrary/textures/base/engineered/cementitious/Mortar_Cement_<channel>_s01.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s01`: a 0.1 m
tile at 1024 px (about 0.1 mm a texel). Nothing in it is larger than a few mm, so a 10 cm
repeat has no feature to show as a grid. Every noise and cell field wraps: seamless. Fixed
seed, no network.

    gen_mortar_cement.py [--out DIR]

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
SET = "Mortar_Cement"
SCALE = "s01"
SEED = 6101
MORTAR = np.array([0.33, 0.30, 0.25])           # judgement: a grey-brown sandy mortar, linear sRGB
ROUGH_MEAN = 0.93
N = tl.SIZE


def soften(a: np.ndarray, sigma: float) -> np.ndarray:
    """A wrap-around Gaussian blur (sigma in texels), done in the frequency domain so it tiles."""
    f = np.fft.fftfreq(a.shape[0])
    g = np.exp(-2 * (np.pi * sigma) ** 2 * (f[:, None] ** 2 + f[None, :] ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(a) * g))


def sand(n: int, seed: int, share: float) -> tuple:
    """Sand grains: a `share` of the cells of an n x n warped cell grid, each a rounded grain of
    its own size. Returns the grain cover (0 paste .. 1 grain), a dome height and a value per grain."""
    w = min(4 * n, N)
    warp = (0.35 * (tl.noise(w, seed + 2) - 0.5), 0.35 * (tl.noise(w, seed + 3) - 0.5))
    d1, _, cid = tl.cells(n, seed, warp=warp)
    rng = np.random.RandomState(seed + 1)
    keep = rng.rand(n * n)[cid] < share
    r = (0.22 + 0.30 * rng.rand(n * n))[cid]                       # grain radius, in cell units
    cover = np.clip((r - d1) / (0.25 * r), 0, 1) * keep
    dome = np.sqrt(np.clip(1 - (d1 / r) ** 2, 0, 1)) * keep
    return cover, dome, rng.rand(n * n)[cid]


def maps() -> dict:
    coarse, dome_c, val_c = sand(70, SEED, 0.50)                   # grains about 0.6 to 1.5 mm
    fine, dome_f, val_f = sand(190, SEED + 10, 0.60)               # grains about 0.25 to 0.55 mm
    fine, dome_f = fine * (1 - coarse), dome_f * (1 - coarse)      # a coarse grain sits on top
    paste = tl.fbm((40, 80, 160), SEED + 20)                       # the binder: mm-scale unevenness
    dustn = tl.fbm((300, 512), SEED + 21)                          # its finest tooth
    rng = np.random.RandomState(SEED + 22)
    speck = rng.rand(N, N)
    vn = 46                                                        # air voids, 0.3 to 1 mm, sparse
    vw = (0.3 * (tl.noise(4 * vn, SEED + 32) - 0.5), 0.3 * (tl.noise(4 * vn, SEED + 33) - 0.5))
    vd, _, vid = tl.cells(vn, SEED + 30, warp=vw)
    vr = np.random.RandomState(SEED + 31)
    vrad = (0.10 + 0.14 * vr.rand(vn * vn))[vid]
    void = np.clip((vrad - vd) / (0.35 * vrad), 0, 1) * (vr.rand(vn * vn)[vid] < 0.22)
    void = soften(void, 0.8)

    def grain_tone(val):
        """Most grains tan quartz, a few dark lithic, a few white."""
        return np.where(val < 0.13, -0.42, np.where(val > 0.88, 0.42, 0.14 + 0.34 * (val - 0.5)))

    shade = (1.0 + 0.10 * (paste - 0.5) + 0.06 * (dustn - 0.5) + 0.05 * (speck - 0.5)
             + coarse * grain_tone(val_c) + 0.8 * fine * grain_tone(val_f) - 0.45 * void)
    albedo = MORTAR[None, None, :] * shade[..., None]
    warm = np.array([1.06, 1.0, 0.90])                             # quartz sand is warmer than paste
    albedo = albedo * (1 + (warm - 1) * np.clip(coarse + fine, 0, 1)[..., None])
    albedo *= MORTAR / albedo.reshape(-1, 3).mean(0)               # re-anchor the MEAN exactly
    albedo = np.clip(albedo, 0, 1)

    rough = 0.04 * (dustn - 0.5) - 0.06 * coarse - 0.03 * fine + 0.04 * void
    rough = np.clip(rough - rough.mean() + ROUGH_MEAN, 0, 1)
    height = (1.0 * dome_c + 0.45 * dome_f + 0.35 * paste + 0.15 * dustn - 1.3 * void)
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(soften(height, 1.0), strength=3.5)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Mortar_Cement base texture set.")
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
