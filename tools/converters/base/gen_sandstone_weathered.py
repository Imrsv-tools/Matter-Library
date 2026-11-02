#!/usr/bin/env python3
"""Generate the base texture set `Sandstone_Weathered` (Phase11 batch 261101-1; lane L2).

Weathered sandstone: sand grains cemented into rock, laid down in beds, cut and left to the
weather, as in cliffs, quarried building stone and old walls. It reads as SANDSTONE, not as
concrete or render, because of three things this draws: the BEDDING (laminae a few mm to a few
cm thick, each a little paler or darker, gently undulating, the harder ones standing slightly
proud where the softer have weathered back), faint wavy IRON-STAIN lines across the beds, and
a fine sandy GRAIN with small rounded weathering pits.

No scan fits: ambientCG's sandstone assets are bricks, tiles and walls (assemblies, not matter),
so the set is generated. The colour is a JUDGEMENT: the texture's mean linear albedo is (0.43, 0.31, 0.19), sRGB
about 174, 151, 121, a warm buff sandstone, re-normalised so the mean is exact. Physically Based
has no sandstone entry; its `Sand`, (0.44, 0.386, 0.231), was tried and read khaki-olive on a
stone face, so it supplies only the roughness ceiling: the mean roughness is 0.9, under that
entry's 1.0 (a weathered face keeps a trace of sheen on its quartz grains).

Writes MatterLibrary/textures/base/natural/stone/Sandstone_Weathered_<channel>_s1.png: basecolor
(sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s1`: a 1 m tile at 1024 px
(about 1 mm a texel): laminae 3 to 40 mm in beds of a few cm to a decimetre, stain lines a few cm apart, pits 3 to 8 mm, the sand
grain single texels. The laminae's thicknesses sum to exactly the tile and every noise
wraps, so the tile is seamless. Fixed seed, no network.

    gen_sandstone_weathered.py [--out DIR]

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
SET = "Sandstone_Weathered"
SCALE = "s1"
SEED = 5303
STONE = np.array([0.43, 0.31, 0.19])            # judgement: a warm buff sandstone, linear sRGB
ROUGH_MEAN = 0.90                               # under the entry's 1.0: see the docstring
N = tl.SIZE


def spots(n: int, seed: int, radius: float, share: float) -> np.ndarray:
    """Soft, irregular spots on a random `share` of an n x n cell grid (radius in cell units)."""
    warp = (0.25 * (tl.noise(min(4 * n, N), seed + 2) - 0.5), 0.25 * (tl.noise(min(4 * n, N), seed + 3) - 0.5))
    d1, _, cid = tl.cells(n, seed, warp=warp)
    rng = np.random.RandomState(seed + 1)
    keep, size = rng.rand(n * n)[cid] < share, (0.4 + 0.6 * rng.rand(n * n))[cid]
    r = radius * size
    return np.clip((r - d1) / (0.3 * r), 0, 1) * keep


def beds() -> tuple:
    """The bedding: laminae of random thickness (3 to 40 mm), grouped into beds, stacked down the
    tile so their thicknesses sum to exactly 1 m (it wraps), gently undulating; each lamina fades
    in and out along its length. Returns each texel's tone and hardness, both about [0, 1]."""
    rng = np.random.RandomState(SEED + 2)
    th = []
    while sum(th) < 1.0:
        th.append(float(np.clip(rng.lognormal(np.log(0.010), 0.7), 0.003, 0.04)))
    th = np.array(th) / sum(th)                                   # exactly the tile, so it wraps
    cum = np.concatenate([[0.0], np.cumsum(th)])
    n = len(th)
    bed = np.cumsum(rng.rand(n) < 0.18)                           # a new bed every few laminae
    bed_tone = rng.rand(bed.max() + 1)[bed]
    lam_tone = np.clip(0.55 * bed_tone + 0.45 * rng.rand(n), 0, 1)
    lam_hard = np.clip(0.5 * rng.rand(bed.max() + 1)[bed] + 0.5 * rng.rand(n), 0, 1)
    v = (np.arange(N)[:, None] + 0.5) / N * np.ones((1, N))
    u = (np.arange(N)[None, :] + 0.5) / N * np.ones((N, 1))
    dip = 0.012 * np.sin(2 * np.pi * u)                           # a gentle dip that wraps
    sway = dip + 0.035 * (tl.fbm((2, 3, 5), SEED) - 0.5) + 0.006 * (tl.fbm((9, 17), SEED + 1) - 0.5)
    idx = np.clip(np.searchsorted(cum, (v + sway) % 1.0, side="right") - 1, 0, n - 1)
    fade = tl.fbm((3, 6, 12), SEED + 8)                           # a lamina fades along its length
    tone = 0.5 + (lam_tone[idx] - 0.5) * (0.15 + 1.7 * fade)
    hard = lam_hard[idx]
    return soften(tone, 0.8), soften(hard, 1.5)


def soften(a: np.ndarray, sigma: float) -> np.ndarray:
    """A wrap-around Gaussian blur (sigma in texels), done in the frequency domain so it tiles."""
    f = np.fft.fftfreq(a.shape[0])
    g = np.exp(-2 * (np.pi * sigma) ** 2 * (f[:, None] ** 2 + f[None, :] ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(a) * g))


def maps() -> dict:
    tone, hard = beds()
    cloud = tl.fbm((3, 6, 12), SEED + 3)                          # broad weathering and tone
    fine = tl.fbm((256, 512), SEED + 4)                           # the cemented grain's texture
    rng = np.random.RandomState(SEED + 5)
    grain = rng.rand(N, N)                                        # one value per texel: sand
    pits = soften(spots(170, SEED + 6, 0.45, 0.05), 1.0)          # weathering pits, 3 to 8 mm
    # iron staining: broad soft mottling, and a few continuous curving bands across the beds
    field = soften(tl.fbm((2, 3, 4), SEED + 7), 6.0)
    bands = np.clip(1 - np.abs(np.sin(2 * np.pi * 5 * field)) / 0.07, 0, 1)
    mottle = np.clip((tl.fbm((4, 8, 16), SEED + 9) - 0.55) * 4, 0, 1)
    stain = np.clip(0.7 * bands + 0.8 * mottle, 0, 1)
    grit = tl.fbm((128, 256, 512), SEED + 10)                      # mm-scale grit

    # the sand leads and the bedding follows: strong bedding alone reads as wood grain
    dark = (rng.rand(N, N) > 0.93).astype(float)                   # dark lithic grains
    pale = (rng.rand(N, N) > 0.92).astype(float)                   # pale quartz grains
    shade = (1.0 + 0.16 * (tone - 0.5) + 0.14 * (cloud - 0.5) + 0.05 * (fine - 0.5)
             + 0.14 * (grain - 0.5) + 0.18 * (grit - 0.5) - 0.18 * pits - 0.22 * dark + 0.18 * pale)
    albedo = STONE[None, None, :] * shade[..., None]
    iron = np.array([1.12, 0.88, 0.68])                           # rust: redder, less blue
    albedo = albedo * (1 + (iron - 1) * (0.9 * stain + 0.35 * (1 - tone))[..., None])
    albedo *= STONE / albedo.reshape(-1, 3).mean(0)               # re-anchor the MEAN exactly
    albedo = np.clip(albedo, 0, 1)

    rough = 0.04 * (fine - 0.5) + 0.03 * (grain - 0.5) - 0.03 * hard + 0.03 * pits
    rough = np.clip(rough - rough.mean() + ROUGH_MEAN, 0, 1)
    height = 1.2 * hard + 0.5 * fine + 0.5 * grain + 1.2 * grit - 1.2 * pits + 1.5 * cloud
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=1.2)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Sandstone_Weathered base texture set.")
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
