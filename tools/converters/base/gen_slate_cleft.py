#!/usr/bin/env python3
"""Generate the base texture set `Slate_Cleft` (Phase11 batch 261002-3; lane L2).

Cleft (riven) slate: a fine-grained, dark blue-grey metamorphic stone split along its
cleavage, so the face is a set of shallow, irregular terraces with soft step edges, a faint
ripple along the cleavage, slightly different tones layer to layer, and the odd rusty
iron stain. No scan fits: ambientCG has no asset that names slate as a stone surface (only
slate roofing tiles, an assembly, and a gravel), and the library names only what a source
states, so the set is generated. The colour is a JUDGEMENT, not invented per pixel: the
texture's mean linear albedo is anchored to (0.065, 0.072, 0.085) (sRGB about 72, 76, 82,
a dark blue-grey roofing slate); Physically Based has no slate entry. Everything here only
varies around it.

Writes MatterLibrary/textures/base/natural/stone/Slate_Cleft_<channel>_s1.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s1`: a 0.5 m
tile, so about 9 ragged terraces cross the tile (steps a few cm apart, running along U) and
the cleavage ripple is about a centimetre. Seamless (periodic noise; the terraces are a floor() of periodic noise),
fixed seed, no network.

    gen_slate_cleft.py [--out DIR]

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
SET = "Slate_Cleft"
SCALE = "s1"
SEED = 733
SLATE = np.array([0.065, 0.072, 0.085])  # judgement: dark blue-grey slate, linear sRGB
STEPS = 9                                 # terraces across the tile
SIZE = tl.SIZE


def noise2(sx: int, sy: int, seed: int, size: int = SIZE) -> np.ndarray:
    """Periodic value noise in [0, 1] on an sx (along U) x sy (along V) grid, so features
    stretch along U (the cleavage direction)."""
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


def hash01(k: np.ndarray, salt: float) -> np.ndarray:
    """A fixed pseudo-random value in [0, 1) per integer k (one tone per terrace)."""
    return np.modf(np.abs(np.sin(k * 12.9898 + salt) * 43758.5453))[0]


def maps() -> dict:
    # Terraces: the floor of a periodic field, so step edges wander and the tile wraps.
    # Long along U (the cleavage's strike), wandering along V; a ragged high-frequency term
    # breaks the step edges into flaky, broken lines rather than smooth contours.
    field = (0.60 * noise2(1, 4, SEED) + 0.25 * noise2(2, 9, SEED + 1)
             + 0.10 * noise2(6, 20, SEED + 2) + 0.05 * noise2(48, 64, SEED + 8))
    s = field * STEPS
    level = np.floor(s)
    frac = s - level
    edge = np.clip((frac - 0.80) / 0.20, 0, 1)            # the soft riser of each step
    edge = edge * edge * (3 - 2 * edge)
    terrace = level + edge
    ripple = noise2(5, 48, SEED + 3)                      # cleavage ripple, long along U
    swell = tl.fbm((2, 3), SEED + 9)                      # broad undulation of the split face
    grain = tl.fbm((64, 128), SEED + 4)                   # fine mineral grain
    stain = np.clip((noise2(5, 5, SEED + 5) - 0.78) * 4.5, 0, 1) * noise2(23, 23, SEED + 6)
    drift = tl.fbm((2, 4), SEED + 7)
    mottle = tl.fbm((8, 16, 32), SEED + 10)

    tone = hash01(level, 1.7) - 0.5                       # each layer a shade apart
    fresh = edge * (1 - edge) * 4                         # step risers: freshly broken
    shade = (1.0 + 0.10 * tone + 0.06 * (ripple - 0.5) + 0.14 * (grain - 0.5)
             + 0.08 * fresh + 0.20 * (drift - 0.5) + 0.16 * (mottle - 0.5))
    albedo = SLATE[None, None, :] * shade[..., None]
    rust = np.array([1.6, 1.1, 0.75])                    # iron staining: warm, a little lighter
    albedo = albedo * (1 + stain[..., None] * (rust - 1)[None, None, :])
    albedo *= SLATE / albedo.reshape(-1, 3).mean(0)       # re-anchor the MEAN exactly

    rough = np.clip(0.62 + 0.12 * fresh + 0.05 * (grain - 0.5) + 0.06 * stain
                    - 0.04 * (ripple - 0.5), 0, 1)
    height = -0.9 * terrace + 0.45 * ripple + 14.0 * swell + 0.10 * grain
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=4.0)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Slate_Cleft base texture set.")
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
