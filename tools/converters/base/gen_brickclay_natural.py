#!/usr/bin/env python3
"""Generate the base texture set `BrickClay_Natural` (Phase11 batch 261114-1; lane L2).

The fired clay of a common building brick: a coarse, sandy, open body, less refined than
terracotta. It reads as BRICK because of four things this draws: the FIRING MOTTLE (broad soft
clouds, paler orange where the kiln ran cooler, deeper and browner where the flame reached),
dark IRON SPOTS a few mm across, the SAND on its face (pale and dark grains), and open VOIDS
and pits 2 to 5 mm where grit pulled out or gas escaped. It is the clay only: no brick shape,
no joint, no bond (a wall is an assembly; the brick's size and its mortar are the builder's).

The colour is a JUDGEMENT, set against Physically Based `Brick`, (0.262, 0.095, 0.061): the
texture's mean linear albedo is (0.40, 0.17, 0.10), a light orange-red, re-normalised so the
mean is exact. It is LIGHTER than that entry on purpose, so one article tints DOWN to a dark
or burnt firing (a tint of about 0.66, 0.56, 0.61 gives the entry's own colour) and a tint can
never go up. The mean roughness is 0.94, under the entry's 1.0.

Writes MatterLibrary/textures/base/engineered/ceramic/BrickClay_Natural_<channel>_s1.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s1`: a 1 m tile
at 1024 px (about 1 mm a texel), so the firing clouds (15 to 50 cm) do not repeat within several
bricks, and a builder offsets the UVs per brick for variety. Seamless (tileable.py), fixed
seed, no network.

    gen_brickclay_natural.py [--out DIR]

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
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "engineered" / "ceramic"
SET = "BrickClay_Natural"
SCALE = "s1"
SEED = 6203
CLAY = np.array([0.40, 0.17, 0.10])             # judgement: lighter than Physically Based `Brick`
ROUGH_MEAN = 0.94
N = tl.SIZE


def spots(n: int, seed: int, radius: float, share: float) -> np.ndarray:
    """Soft, irregular spots on a random `share` of an n x n cell grid (radius in cell units)."""
    w = min(4 * n, N)
    warp = (0.25 * (tl.noise(w, seed + 2) - 0.5), 0.25 * (tl.noise(w, seed + 3) - 0.5))
    d1, _, cid = tl.cells(n, seed, warp=warp)
    rng = np.random.RandomState(seed + 1)
    keep, size = rng.rand(n * n)[cid] < share, (0.4 + 0.6 * rng.rand(n * n))[cid]
    r = radius * size
    return np.clip((r - d1) / (0.3 * r), 0, 1) * keep


def soften(a: np.ndarray, sigma: float) -> np.ndarray:
    """A wrap-around Gaussian blur (sigma in texels), done in the frequency domain so it tiles."""
    f = np.fft.fftfreq(a.shape[0])
    g = np.exp(-2 * (np.pi * sigma) ** 2 * (f[:, None] ** 2 + f[None, :] ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(a) * g))


def maps() -> dict:
    # Firing mottle, 15 to 50 cm: warped cell blobs over odd-scaled noise (no octave grid shows).
    warp = (0.6 * (tl.fbm((3, 7), SEED + 40) - 0.5), 0.6 * (tl.fbm((3, 7), SEED + 41) - 0.5))
    d1, _, cid = tl.cells(5, SEED + 42, warp=warp)
    lift = np.random.RandomState(SEED + 43).rand(25)[cid]
    blobs = soften(np.clip(1 - d1 / 0.75, 0, 1) ** 1.5 * (0.3 + 0.7 * lift), 30)
    flash = 0.5 * blobs + 0.5 * tl.fbm((3, 5, 7, 13), SEED)
    flash = (flash - flash.min()) / (flash.max() - flash.min())
    body = tl.fbm((11, 23, 47), SEED + 1)                         # the body's unevenness, 2 to 9 cm
    fine = tl.fbm((256, 512), SEED + 2)                           # the clay's grain
    grit = tl.fbm((128, 256, 512), SEED + 3)                      # the sanded face, mm scale
    rng = np.random.RandomState(SEED + 5)
    sand_pale = (rng.rand(N, N) > 0.955).astype(float)            # quartz sand, pale, ~1 mm
    sand_dark = (rng.rand(N, N) > 0.965).astype(float)            # dark grains, ~1 mm
    iron = soften(spots(190, SEED + 20, 0.42, 0.035), 0.7)        # iron spots, 1 to 4 mm
    voids = soften(spots(130, SEED + 30, 0.40, 0.06), 0.8)        # open voids and pits, 2 to 6 mm

    # Cooler-fired areas go paler and more orange; flame-touched ones deeper and browner.
    f = flash - 0.5
    tint = np.stack([1 + 0.20 * f, 1 + 0.60 * f, 1 + 0.75 * f], -1)
    shade = (1.0 + 0.30 * f + 0.16 * (body - 0.5) + 0.08 * (fine - 0.5) + 0.14 * (grit - 0.5)
             + 0.22 * sand_pale - 0.25 * sand_dark - 0.45 * iron - 0.28 * voids)
    albedo = CLAY[None, None, :] * shade[..., None] * tint
    sand_col = np.array([1.3, 1.8, 2.0])                          # sand grains: pale, toward buff
    albedo = albedo * (1 + (sand_col - 1) * 0.3 * sand_pale[..., None])
    grey = albedo.mean(-1, keepdims=True)                         # iron spots: near-black, purple-brown
    albedo = albedo + (0.8 * grey - albedo) * (0.7 * iron)[..., None]
    albedo *= CLAY / albedo.reshape(-1, 3).mean(0)                # re-anchor the MEAN exactly
    albedo = np.clip(albedo, 0, 1)

    rough = 0.05 * (fine - 0.5) + 0.03 * voids - 0.06 * sand_pale - 0.08 * iron
    rough = np.clip(rough - rough.mean() + ROUGH_MEAN, 0, 1)
    # At 1 mm a texel a single-texel grain is already steep: a light hand, or it reads as stucco.
    height = (0.5 * fine + 1.0 * grit + 3.5 * body + 0.25 * sand_pale + 0.2 * sand_dark
              + 0.3 * iron - 2.2 * voids)
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=1.6)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the BrickClay_Natural base texture set.")
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
