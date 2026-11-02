#!/usr/bin/env python3
"""Generate the base texture set `Oak_Natural` (Phase11 batch 261031-1; lane L2).

Natural oak, flat-sawn and unfinished: plain, smooth boards of a mid, warm brown, the growth
rings drawn as long bands along the grain that bend into the flat-sawn "cathedral" figure
where the cut runs through them; oak is ring-porous, so each ring's earlywood carries a band
of open pores that read as fine dark streaks; the rays show as short flecks along the grain.

Generated, not scanned: it was ambientCG Wood049, an 80 cm sample, off its s1 tag (Phase19 D-9,
RD-P19-2), and quilting it into an exact 1 m tile breaks its long grain into a visible
patchwork, so the set is generated at the tag's size. The colour and roughness are ANCHORED to
that scan, not invented: the texture's mean linear albedo is (0.202, 0.127, 0.077) and its mean
roughness 0.50, the scan's own means; Physically Based has no wood entry. Everything here only
varies around them.

Writes MatterLibrary/textures/base/natural/wood/Oak_Natural_<channel>_s1.png: basecolor
(sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s1`: an exact 1 m tile at
1024 px (about 1 mm a texel), the grain along U, about 90 growth rings across the tile (~11 mm
apart, as on the scan). Seamless (periodic noise, integer ring count), fixed seed, no network.

    gen_oak_natural.py [--out DIR]

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
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "natural" / "wood"
SET = "Oak_Natural"
SCALE = "s1"
SEED = 8049
OAK = np.array([0.202, 0.127, 0.077])    # the Wood049 scan's mean linear albedo
ROUGH_MEAN = 0.50                         # the Wood049 scan's mean roughness
RINGS = 90                                # growth rings across the tile (integer: seamless in V)
SIZE = tl.SIZE


def noise2(sx: int, sy: int, seed: int, size: int = SIZE) -> np.ndarray:
    """Periodic value noise in [0, 1] on an sx (along U) x sy (along V) grid: tileable.noise
    with a different cell count per axis, so features stretch along the grain."""
    rng = np.random.RandomState(seed)
    grid = rng.rand(sy, sx)

    def axis(n):
        t = np.arange(size) * n / size
        i0 = np.floor(t).astype(int) % n
        f = t - np.floor(t)
        return i0, (i0 + 1) % n, f * f * (3 - 2 * f)

    y0, y1, fy = axis(sy)
    x0, x1, fx = axis(sx)
    rows = grid[y0] * (1 - fy)[:, None] + grid[y1] * fy[:, None]       # (size, sx)
    return rows[:, x0] * (1 - fx)[None, :] + rows[:, x1] * fx[None, :]


def maps() -> dict:
    v = np.arange(SIZE)[:, None] / SIZE                               # across the grain
    # Ring figure: bands across V, bent by slow noise long along U. Where the warp's slope across
    # V outruns the ring rate, the cut runs through the rings and they close into the long loops
    # of the flat-sawn (cathedral) figure; elsewhere they run nearly straight.
    warp = (25.0 * (noise2(1, 3, SEED) - 0.5) + 8.0 * (noise2(2, 5, SEED + 1) - 0.5)
            + 2.0 * (noise2(5, 14, SEED + 6) - 0.5))
    uneven = 3.0 * (noise2(1, 37, SEED + 7) - 0.5)                   # irregular ring spacing
    ring = RINGS * v + warp + uneven
    phase = ring % 1.0
    k = np.floor(ring).astype(int) % RINGS                            # each ring's own strength
    strength = 0.4 + 1.2 * np.random.RandomState(SEED + 11).rand(RINGS)[k]
    # Earlywood: the first quarter of each ring, open pores; latewood: a denser, darker band.
    early = np.clip(1.0 - np.abs(phase - 0.12) / 0.12, 0, 1)
    late = np.clip((phase - 0.55) / 0.35, 0, 1) * np.clip((1.0 - phase) / 0.10, 0, 1) * strength
    fibre = 0.6 * noise2(5, 400, SEED + 2) + 0.4 * noise2(16, 800, SEED + 8)
    pores = np.clip((0.35 - noise2(48, 700, SEED + 3)) * 5, 0, 1) * early
    rays = np.clip((noise2(90, 330, SEED + 10) - 0.80) * 6, 0, 1)    # short flecks, 5 to 15 mm
    streak = noise2(2, 14, SEED + 9)                                  # darker and lighter boards' streaks
    drift = tl.fbm((2, 4), SEED + 4)                                  # broad colour drift
    tone = noise2(3, 5, SEED + 5)                                     # yellower vs greyer cast

    shade = (1.0 + 0.16 * (fibre - 0.5) - 0.35 * late - 0.35 * pores + 0.10 * rays
             + 0.30 * (streak - 0.5) + 0.20 * (drift - 0.5))
    albedo = OAK[None, None, :] * shade[..., None]
    cast = np.stack([1 + 0.05 * (tone - 0.5), np.ones_like(tone), 1 - 0.10 * (tone - 0.5)], -1)
    albedo = albedo * cast
    albedo *= OAK / albedo.reshape(-1, 3).mean(0)                     # re-anchor the MEAN exactly

    rough = 0.08 * pores + 0.04 * (fibre - 0.5) - 0.03 * late + 0.03 * (drift - 0.5)
    rough = np.clip(rough - rough.mean() + ROUGH_MEAN, 0, 1)
    height = 0.40 * fibre - 0.9 * pores + 0.25 * late + 0.15 * rays
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=2.0)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Oak_Natural base texture set.")
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
