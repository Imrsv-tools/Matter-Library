#!/usr/bin/env python3
"""Generate the base texture set `Aluminium_Brushed` (Phase11 batch 261002-4; lane L2).

Brushed aluminium: rolled sheet finished with an abrasive belt or pad, so the face is a dense
field of fine parallel grooves (appliance fronts, laptop lids, trim, nameplates). The colour
is GROUNDED, not invented: the texture's mean linear albedo is anchored to Physically Based
`Aluminum` (0.916, 0.923, 0.924); the brushing varies only around it.

**The grooves run along V** (down the tile). The article's anisotropy
(`specular_roughness_anisotropy`, OpenPBR) stretches the highlight along the UV tangent U,
ACROSS the grooves, which is what a brushed face does: its micro-normals tilt across the
grooves, never along them. The groove direction here and the highlight's stretch must agree
(the Satin article follows the same rule; Learnings B9).

Writes MatterLibrary/textures/base/engineered/metal/Aluminium_Brushed_<channel>_s001.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s001`: a 1 cm
tile, 10 µm per pixel, so the grooves are 10-80 µm wide and run the tile's length (they wrap,
so the tile is seamless along V too). Fixed seed, no network.

    gen_aluminium_brushed.py [--out DIR]

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
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "engineered" / "metal"
SET = "Aluminium_Brushed"
SCALE = "s001"
SEED = 1307
PB_ALUMINUM = np.array([0.916, 0.923, 0.924])   # Physically Based `Aluminum`, linear sRGB
SIZE = tl.SIZE


def noise2(sx: int, sy: int, seed: int, size: int = SIZE) -> np.ndarray:
    """Periodic value noise in [0, 1] on an sx (along U) x sy (along V) grid. Few cells
    along V and many along U draw streaks running down the tile (along V)."""
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


def maps() -> dict:
    # The groove field: octaves of streak noise, long along V, from 80 µm down to one pixel.
    grooves = (0.40 * noise2(128, 3, SEED) + 0.30 * noise2(256, 4, SEED + 1)
               + 0.20 * noise2(512, 6, SEED + 2) + 0.10 * noise2(1024, 8, SEED + 3))
    # A few deeper scores from a coarser grit, sparse.
    scores = np.clip((noise2(341, 2, SEED + 4) - 0.80) * 5, 0, 1)
    # The pad's pressure wanders slowly over the sheet: a faint banding across the grooves.
    pressure = noise2(6, 2, SEED + 5)

    shade = 1.0 + 0.035 * (grooves - 0.5) - 0.05 * scores + 0.02 * (pressure - 0.5)
    albedo = PB_ALUMINUM[None, None, :] * shade[..., None]
    albedo *= PB_ALUMINUM / albedo.reshape(-1, 3).mean(0)        # re-anchor the MEAN to PB exactly

    rough = np.clip(0.34 + 0.06 * (grooves - 0.5) + 0.05 * scores + 0.03 * (pressure - 0.5), 0, 1)
    height = 1.0 * grooves - 1.2 * scores
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=3.0)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Aluminium_Brushed base texture set.")
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
