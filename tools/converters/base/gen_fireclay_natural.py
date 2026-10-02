#!/usr/bin/env python3
"""Generate the base texture set `Fireclay_Natural` (Phase11 batch 261002-2; lane L2).

Unglazed fireclay: a refractory clay fired hot, so it is denser and paler than earthenware: a
buff-cream body, coarse grog (crushed fired clay) that shows as lighter and darker grains, and
the small dark iron specks fireclay is known for. Matte and porous. The colour is a JUDGEMENT:
Physically Based has `Clay` (modelling clay) and `Brick` (red), neither a buff fireclay, so the
texture's mean linear albedo is anchored to (0.60, 0.48, 0.31) (sRGB about 205, 185, 150).
Everything here only varies around it.

Writes MatterLibrary/textures/base/engineered/ceramic/Fireclay_Natural_<channel>_s01.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s01`: a 0.1 m
tile, so grog grains are ~0.5-1.5 mm and iron specks ~0.3-1 mm. Seamless (tileable.py), fixed
seed, no network.

    gen_fireclay_natural.py [--out DIR]

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
SET = "Fireclay_Natural"
SCALE = "s01"
SEED = 613
FIRECLAY = np.array([0.60, 0.48, 0.31])   # judgement: buff unglazed fireclay, linear sRGB
IRON = np.array([0.30, 0.17, 0.08])       # relative tint of an iron speck (dark rust-brown)


def specks(count: int, rmin: float, rmax: float, seed: int, size: int = tl.SIZE) -> np.ndarray:
    """Round, soft-edged grains at random points, in [0, 1]. Each disc is drawn with wrap-around
    (toroidal), so the tile stays seamless. Thresholded value noise would make square,
    axis-aligned grains (its extremes sit on the grid), which is why grains are drawn here."""
    rng = np.random.RandomState(seed)
    out = np.zeros((size, size))
    for cx, cy, r in zip(rng.rand(count) * size, rng.rand(count) * size,
                         rmin + (rmax - rmin) * rng.rand(count) ** 2):
        k = int(np.ceil(r + 1.5))
        xs, ys = np.arange(int(cx) - k, int(cx) + k + 1), np.arange(int(cy) - k, int(cy) + k + 1)
        d = np.hypot(xs[None, :] + 0.5 - cx, ys[:, None] + 0.5 - cy)
        disc = np.clip(r + 0.5 - d, 0, 1)                     # ~1 px soft edge
        win = np.ix_(ys % size, xs % size)
        out[win] = np.maximum(out[win], disc)
    return out


def maps() -> dict:
    mottle = tl.fbm((5, 10, 20), SEED)                          # uneven firing / body colour
    fine = tl.fbm((128, 256), SEED + 10)                        # clay grain
    grog_light = specks(2600, 1.5, 6.0, SEED + 20)              # coarse grog grains, 0.3-1.2 mm
    grog_dark = specks(1800, 1.5, 5.0, SEED + 21)
    iron = specks(420, 1.2, 4.5, SEED + 40)                     # dark iron specks, 0.2-0.9 mm
    pits = specks(1500, 0.8, 2.5, SEED + 30)                    # small open pores

    shade = 1.0 + 0.16 * (mottle - 0.5) + 0.06 * (fine - 0.5) + 0.16 * grog_light - 0.18 * grog_dark - 0.08 * pits
    albedo = FIRECLAY[None, None, :] * shade[..., None]
    albedo = albedo * (1 - iron[..., None]) + (FIRECLAY * IRON)[None, None, :] * iron[..., None]
    albedo *= FIRECLAY / albedo.reshape(-1, 3).mean(0)          # re-anchor the MEAN exactly

    rough = np.clip(0.88 + 0.06 * (fine - 0.5) - 0.04 * (mottle - 0.5) + 0.06 * pits, 0, 1.0)
    height = 0.5 * fine + 0.2 * mottle - 0.6 * pits + 0.35 * grog_light + 0.2 * grog_dark
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=6.0)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Fireclay_Natural base texture set.")
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
