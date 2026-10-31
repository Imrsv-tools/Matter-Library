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

Writes MatterLibrary/textures/base/engineered/ceramic/Terracotta_Unglazed_<channel>_s01.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s01`: a 0.1 m
tile at 1024 px (about 0.1 mm a texel): flash clouds 2 to 5 cm, sand and grog 0.3 to 1.5 mm,
pin pores 0.2 to 0.6 mm. Seamless (tileable.py), fixed seed, no network.

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
SCALE = "s01"
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


def maps() -> dict:
    flash = tl.fbm((2, 4, 8), SEED)                              # kiln flashing, 2 to 5 cm clouds
    body = tl.fbm((16, 32), SEED + 1)                            # the body's own unevenness
    fine = tl.fbm((128, 256), SEED + 2)                          # the clay's grain
    sand_pale = spots(110, SEED + 10, 0.26, 0.07)                # quartz sand, pale
    grog_dark = spots(70, SEED + 20, 0.26, 0.05)                 # grog, darker red-brown
    pores = spots(160, SEED + 30, 0.22, 0.12)                    # open pin pores

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
    height = (0.6 * fine + 0.25 * body + 0.5 * sand_pale + 0.3 * grog_dark - 1.2 * pores)
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=5.0)}


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
