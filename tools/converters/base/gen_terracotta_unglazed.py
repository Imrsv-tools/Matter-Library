#!/usr/bin/env python3
"""Generate the base texture set `Terracotta_Unglazed` (Phase11 batch 261031-1; lane L2).

Unglazed architectural terracotta: the red-orange body of roof and floor tiles, pressed or
extruded, fired and left bare. It reads as FIRED CLAY, not painted clay, because the body is
not one flat colour: the kiln flashes it in soft clouds (paler and buff where it ran cooler,
deeper red-brown where the flame touched), the clay carries sand and grog (crushed fired clay)
that show as pale and dark grains, and the face is porous, open pin pores and a dry, sanded
tooth. It is the coarser, architectural sibling of Earthenware_Natural (the finer pottery body).

The colour is GROUNDED, not invented: the texture's mean linear albedo is anchored to Physically
Based `Terracotta`, (0.555, 0.212, 0.11), and its mean roughness to 0.95 under that entry's 1.0
(the entry's 1.0 is a ceiling; a sanded face keeps a trace of sheen on its grains). Everything
here only varies around them.

Writes MatterLibrary/textures/base/engineered/ceramic/Terracotta_Unglazed_<channel>_s1.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s1`: a 1 m tile
at 1024 px (about 1 mm a texel): flash clouds 20 to 50 cm, the body's own unevenness 5 to 10 cm,
grog 2 to 3 mm, sand and pin pores single texels. Seamless (tileable.py), fixed seed, no network.
*(Was `s01`, flash clouds 2 to 5 cm in a 0.1 m tile: three or four per tile, so the tile showed
as a grid on a floor; the maintainer's redo, batch 261101-1, "the pattern is too repetitive".)*

    gen_terracotta_unglazed.py [--out DIR]

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
SET = "Terracotta_Unglazed"
SCALE = "s1"
SEED = 4207
PB_TERRACOTTA = np.array([0.555, 0.212, 0.11])   # Physically Based `Terracotta`, linear sRGB
ROUGH_MEAN = 0.95                                # under the entry's 1.0: see the docstring


def spots(n: int, seed: int, radius: float, share: float) -> np.ndarray:
    """Soft, irregular spots on a random `share` of an n x n cell grid (radius in cell units)."""
    warp = (0.25 * (tl.noise(4 * n, seed + 2) - 0.5), 0.25 * (tl.noise(4 * n, seed + 3) - 0.5))
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
    # Kiln flashing, 20 to 50 cm clouds: warped cell blobs over odd-scaled noise, so no octave's
    # square grid shows (low-scale value noise alone reads as soft horizontal and vertical bands).
    warp = (0.6 * (tl.fbm((3, 7), SEED + 40) - 0.5), 0.6 * (tl.fbm((3, 7), SEED + 41) - 0.5))
    d1, _, cid = tl.cells(4, SEED + 42, warp=warp)
    lift = np.random.RandomState(SEED + 43).rand(16)[cid]
    blobs = soften(np.clip(1 - d1 / 0.75, 0, 1) ** 1.5 * (0.4 + 0.6 * lift), 40)
    flash = 0.55 * blobs + 0.45 * tl.fbm((3, 5, 7, 11), SEED)
    flash = (flash - flash.min()) / (flash.max() - flash.min())
    body = tl.fbm((10, 20, 40), SEED + 1)                        # the body's own unevenness, 2.5 to 10 cm
    fine = tl.fbm((256, 512), SEED + 2)                          # the clay's grain
    rng = np.random.RandomState(SEED + 5)                        # one value per texel tiles by itself
    sand_pale = (rng.rand(tl.SIZE, tl.SIZE) > 0.97).astype(float)  # quartz sand, pale, ~1 mm
    pores = (rng.rand(tl.SIZE, tl.SIZE) > 0.975).astype(float)     # open pin pores, ~1 mm
    grog_dark = spots(400, SEED + 20, 0.4, 0.10)                 # grog, darker red-brown, 2 to 3 mm

    # Flash: cooler-fired areas go paler and buff (less red), flame-touched ones deeper and browner.
    f = flash - 0.5
    tint = np.stack([1 + 0.18 * f, 1 + 0.55 * f, 1 + 0.80 * f], -1)
    shade = (1.0 + 0.18 * f + 0.14 * (body - 0.5) + 0.08 * (fine - 0.5) + 0.15 * sand_pale
             - 0.15 * grog_dark - 0.30 * pores)
    albedo = PB_TERRACOTTA[None, None, :] * shade[..., None] * tint
    sand_col = np.array([1.35, 1.75, 1.9])                        # sand grains: pale, toward buff
    albedo = albedo * (1 + (sand_col - 1) * 0.25 * sand_pale[..., None])
    albedo *= PB_TERRACOTTA / albedo.reshape(-1, 3).mean(0)      # re-anchor the MEAN to PB exactly
    albedo = np.clip(albedo, 0, 1)

    rough = 0.05 * (fine - 0.5) + 0.03 * pores - 0.06 * sand_pale
    rough = np.clip(rough - rough.mean() + ROUGH_MEAN, 0, 1)
    # At 1 mm a texel a single-texel grain is already steep: a light hand, or it reads as stucco.
    height = (0.6 * fine + 4.0 * body + 0.25 * sand_pale + 0.3 * grog_dark - 0.5 * pores)
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=1.5)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Terracotta_Unglazed base texture set.")
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
