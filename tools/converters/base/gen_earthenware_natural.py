#!/usr/bin/env python3
"""Generate the base texture set `Earthenware_Natural` (Phase03 step 3.5; lane L2).

Unglazed earthenware: low-fired clay, porous and matte, with a mottled body and small grog
(crushed fired-clay) specks. The colour is GROUNDED, not invented: the texture's mean linear
albedo is anchored to Physically Based `Terracotta` (terracotta is unglazed earthenware),
(0.555, 0.212, 0.11), with its roughness 1.0 as the ceiling. Everything here only varies
around those values.

Writes MatterLibrary/textures/base/engineered/ceramic/Earthenware_Natural_<channel>_s01.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s01`: a 0.1 m
tile, so grog specks are ~0.3-1 mm. Seamless (tileable.py), fixed seed, no network.

    gen_earthenware_natural.py [--out DIR]

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
SET = "Earthenware_Natural"
SCALE = "s01"
SEED = 307
PB_TERRACOTTA = np.array([0.555, 0.212, 0.11])   # Physically Based `Terracotta`, linear sRGB


def maps() -> dict:
    mottle = tl.fbm((6, 12, 24), SEED)                          # uneven firing / body colour
    fine = tl.fbm((96, 192), SEED + 10)                         # clay grain
    specks = tl.noise(340, SEED + 20)                           # grog, sparse
    grog_light = np.clip((specks - 0.86) * 9, 0, 1)
    grog_dark = np.clip((0.12 - specks) * 9, 0, 1)
    pits = np.clip((0.18 - tl.noise(260, SEED + 30)) * 6, 0, 1) # small open pores

    shade = 1.0 + 0.22 * (mottle - 0.5) + 0.06 * (fine - 0.5) + 0.18 * grog_light - 0.25 * grog_dark
    albedo = PB_TERRACOTTA[None, None, :] * shade[..., None]
    albedo *= PB_TERRACOTTA / albedo.reshape(-1, 3).mean(0)     # re-anchor the MEAN to PB exactly

    rough = np.clip(0.92 + 0.06 * (fine - 0.5) - 0.05 * (mottle - 0.5) + 0.04 * pits, 0, 1.0)
    height = 0.5 * fine + 0.25 * mottle - 0.6 * pits + 0.2 * grog_light
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=6.0)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Earthenware_Natural base texture set.")
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
