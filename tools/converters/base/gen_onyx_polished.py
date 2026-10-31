#!/usr/bin/env python3
"""Generate the base texture set `Onyx_Polished` (Phase11 batch 261031-1; lane L2).

Polished honey onyx: banded calcite (the stone sold as onyx marble), cut across its layers and
polished. Its look is wavy bands a few millimetres wide, each its own tone of amber, orange,
honey-brown or cream, with thin pale and faintly pink seams between some of them; the band
edges are crinkled, not ruled; a faint cloudy mottle sits inside the wider bands.

Generated, not scanned: it was ambientCG Onyx007, judged 0.3 m across (the source states no
size), off its s01 tag (Phase19 D-9, RD-P19-2). That scan is one large wave structure, about
two waves a tile, which no 0.1 m quilt can carry, so the set is generated at the tag's size.
The colour and roughness are ANCHORED to that scan, not invented: the texture's mean linear
albedo is (0.573, 0.319, 0.147), the scan's own mean and the recipe's subsurface_color, and
its mean roughness 0.04, the scan's; Physically Based has no onyx or calcite entry.
Everything here only varies around them.

Writes MatterLibrary/textures/base/natural/stone/Onyx_Polished_<channel>_s01.png: basecolor
(sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s01`: an exact 0.1 m tile
at 1024 px (about 0.1 mm a texel), about 30 bands across it (~3 mm each, as on the scan at its
judged size) undulating gently across it. The polish leaves the normal almost
flat. Seamless (periodic noise, integer band count), fixed seed, no network.

    gen_onyx_polished.py [--out DIR]

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
SET = "Onyx_Polished"
SCALE = "s01"
SEED = 7007
ONYX = np.array([0.573, 0.319, 0.147])    # the Onyx007 scan's mean linear albedo
ROUGH_MEAN = 0.04                          # the Onyx007 scan's mean roughness: polished
BANDS = 30                                 # bands across the tile (integer: seamless in V)
SIZE = tl.SIZE
# The bands' tones, as multiples of the anchor (linear): cream, honey, amber, orange, brown.
PALETTE = np.array([[1.40, 1.65, 1.85], [1.15, 1.15, 1.05], [1.00, 0.92, 0.75],
                    [1.05, 0.70, 0.42], [0.78, 0.66, 0.55]])


def noise2(sx: int, sy: int, seed: int, size: int = SIZE) -> np.ndarray:
    """Periodic value noise in [0, 1] on an sx (along U) x sy (along V) grid, so features
    stretch along U (the bands' run)."""
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
    rng = np.random.RandomState(SEED)
    v = np.arange(SIZE)[:, None] / SIZE
    # The swell: the scan's waves are longer than this tile (about 15 cm), so here the bands
    # undulate, up to about a centimetre and irregularly, the same for every band nearby so they
    # run parallel. A regular wave would repeat as a zigzag across a wall of tiles.
    swell = (0.12 * (noise2(2, 2, SEED) - 0.5) + 0.06 * (noise2(3, 3, SEED + 1) - 0.5)
             + 0.015 * (noise2(7, 4, SEED + 2) - 0.5))
    crinkle = 0.004 * (noise2(40, 20, SEED + 3) - 0.5) + 0.002 * (noise2(120, 60, SEED + 4) - 0.5)
    uneven = 0.6 * (noise2(1, 11, SEED + 5) - 0.5) / BANDS            # uneven band widths
    pos = BANDS * (v + swell + crinkle + uneven)
    k = np.floor(pos).astype(int) % BANDS
    f = pos - np.floor(pos)

    tone = rng.randint(0, len(PALETTE), BANDS)
    lift = rng.uniform(0.85, 1.15, BANDS)
    col = PALETTE[tone][k] * lift[k][..., None]
    nxt = PALETTE[tone][(k + 1) % BANDS] * lift[(k + 1) % BANDS][..., None]
    blend = np.clip((f - 0.70) / 0.30, 0, 1)[..., None] ** 1.5         # soft step into the next band
    col = col * (1 - blend) + nxt * blend
    # Seams: thin pale (and on a few, faintly pink) lines at some band edges.
    seam_on = rng.rand(BANDS) < 0.4
    pink = rng.rand(BANDS) < 0.3
    seam = np.clip(1 - np.abs(f - 0.92) / 0.035, 0, 1) * seam_on[k]
    seam_col = np.where(pink[k][..., None], np.array([1.60, 1.25, 1.35]), np.array([1.65, 1.85, 2.10]))
    col = col * (1 - 0.7 * seam[..., None]) + seam_col * 0.7 * seam[..., None]

    # Laminae: each band is itself many fine layers, a few tenths of a millimetre to a millimetre.
    lam = (rng.uniform(-1, 1, BANDS * 7)[np.floor(pos * 7).astype(int) % (BANDS * 7)]
           + 0.6 * rng.uniform(-1, 1, BANDS * 23)[np.floor(pos * 23).astype(int) % (BANDS * 23)])
    mottle = tl.fbm((6, 13, 29, 61), SEED + 6)                          # cloudy, inside the bands
    albedo = ONYX[None, None, :] * col * (1 + 0.07 * lam + 0.30 * (mottle - 0.5))[..., None]
    albedo *= ONYX / albedo.reshape(-1, 3).mean(0)                    # re-anchor the MEAN exactly
    albedo = np.clip(albedo, 0, 1)

    rough = 0.02 * (mottle - 0.5) + 0.02 * seam
    rough = np.clip(rough - rough.mean() + ROUGH_MEAN, 0, 1)
    height = 0.2 * seam + 0.1 * mottle
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=0.5)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Onyx_Polished base texture set.")
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
