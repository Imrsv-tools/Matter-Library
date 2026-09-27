#!/usr/bin/env python3
"""Generate the base texture set `Skin_Pores` (Phase07 step 7.1; lane L2).

The micro-surface every skin article shares: pores on a fine furrow network, at real size.
It carries no colour: a skin's tone is its own constant (Physically Based Skin I-VI), so
one normal and one roughness map serve all six.

- **Pores:** 0.06-0.2 mm across, about 0.4 mm apart (a jittered grid, 24 per centimetre),
  each a soft round dip.
- **Furrows:** the shallow criss-cross lines that divide skin into small plateaus, roughly
  0.5-1 mm across (ridged noise).
- **Roughness:** anchored to Physically Based Skin's 0.5 (the MEAN is re-normalised to it),
  slightly rougher in the pores and furrows, where oil does not sit.

Writes MatterLibrary/textures/base/biological/tissue/Skin_Pores_<channel>_s001.png:
roughness and normal (linear data, NormalGL). Scale `s001`: a 0.01 m tile at 1024 px,
about 10 um per pixel. Seamless (tileable.py; pores wrap toroidally), fixed seed, no network.

    gen_skin_pores.py [--out DIR]

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
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "biological" / "tissue"
SET = "Skin_Pores"
SCALE = "s001"
SEED = 707
PB_SKIN_ROUGHNESS = 0.5          # Physically Based `Skin I`-`Skin VI` (all 0.5)
PORES_PER_TILE = 24              # per axis, on a 1 cm tile: ~0.42 mm apart
PORE_RADIUS_PX = (3.0, 10.0)     # 0.03-0.1 mm radius at ~9.8 um per pixel


def pores(size: int = tl.SIZE) -> np.ndarray:
    """Pore depth in [0, 1]: soft round dips on a jittered grid, wrapped so the tile is seamless."""
    rng = np.random.RandomState(SEED)
    depth = np.zeros((size, size))
    cell = size / PORES_PER_TILE
    win = int(np.ceil(PORE_RADIUS_PX[1] * 2.5))
    offs = np.arange(-win, win + 1)
    for gy in range(PORES_PER_TILE):
        for gx in range(PORES_PER_TILE):
            cx = (gx + 0.15 + 0.7 * rng.rand()) * cell
            cy = (gy + 0.15 + 0.7 * rng.rand()) * cell
            r = rng.uniform(*PORE_RADIUS_PX)
            d = rng.uniform(0.5, 1.0)
            ys = (np.floor(cy).astype(int) + offs) % size
            xs = (np.floor(cx).astype(int) + offs) % size
            dy = (np.floor(cy) + offs - cy)[:, None]
            dx = (np.floor(cx) + offs - cx)[None, :]
            dip = d * np.exp(-(dx * dx + dy * dy) / (2 * (r * 0.5) ** 2))
            block = depth[np.ix_(ys, xs)]
            depth[np.ix_(ys, xs)] = np.maximum(block, dip)
    return depth


def maps() -> dict:
    pore = pores()
    ridge_a = 1.0 - np.abs(tl.fbm((14, 28), SEED + 10) - 0.5) * 2.0   # 1 on a furrow line
    ridge_b = 1.0 - np.abs(tl.fbm((20, 40), SEED + 20) - 0.5) * 2.0
    furrow = np.clip((np.maximum(ridge_a, ridge_b) - 0.86) * 7.0, 0, 1)
    micro = tl.fbm((160, 320), SEED + 30)                              # the finest grain
    swell = tl.fbm((3, 6), SEED + 40)                                  # gentle unevenness

    height = 0.35 * swell + 0.08 * micro - 0.55 * furrow - 0.9 * pore
    rough = 0.5 + 0.06 * (micro - 0.5) + 0.10 * furrow + 0.12 * pore - 0.04 * (swell - 0.5)
    rough *= PB_SKIN_ROUGHNESS / rough.mean()                          # re-anchor the MEAN to PB
    return {"roughness": tl.gray(np.clip(rough, 0, 1)),
            "normal": tl.normal_map(height, strength=3.0)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Skin_Pores base texture set.")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args(argv)
    out = Path(args.out)
    targets = {ch: out / f"{SET}_{ch}_{SCALE}.png" for ch in ("roughness", "normal")}
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
