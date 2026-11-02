#!/usr/bin/env python3
"""Generate the base texture set `Concrete_BoardFormed` (lane L2).

Board-formed concrete: concrete cast against rough-sawn timber boards, so its face keeps
each board's imprint. Vertical strips about 10 cm wide (8 to 12 cm here), each a slightly
different plane and tone where the board sat a little proud or soaked up more water; the
sawn grain printed into each strip; thin fins of paste where it leaked into the joints;
the odd knot; bug holes (small air voids) and the form-tie holes.

The colour is GROUNDED, not invented: the texture's mean linear albedo is anchored to
Physically Based `Concrete`, (0.51, 0.51, 0.51), and its mean roughness to the same entry's
0.5 (a cast face). Vary only around them.

Generated, not scanned: ambientCG's one board-formed scan (Concrete045) is 2 m, not a scale
option, and is itself a 0.67 m sample repeated three times down the tile, so no exact 1 m
tile can be cut or quilted from it without breaking its boards (Phase19 D-9, RD-P19-2).

The tile is exactly 1 m, the s1 scale option, at 1024 px (about 1 mm a texel). The boards'
widths sum to the tile, so the tile wraps on a joint. A board is far longer than the tile,
so the boards run through it top to bottom with no butt joint.

Writes MatterLibrary/textures/base/engineered/cementitious/Concrete_BoardFormed_<channel>_s1.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Seamless
(tileable.py), fixed seed, no network.

    gen_concrete_boardformed.py [--out DIR]

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
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "engineered" / "cementitious"
SET = "Concrete_BoardFormed"
SCALE = "s1"
SEED = 4510
N = tl.SIZE                                  # 1024 px over 1 m: about 1 mm a pixel
PB_CONCRETE = np.array([0.51, 0.51, 0.51])   # Physically Based `Concrete`, linear sRGB
ROUGH_MEAN = 0.5                             # Physically Based `Concrete`, a cast face
BOARDS = 10                                  # 8 to 12 cm each, summing to exactly 1 m
TIES = ((0.30, 0.22), (0.80, 0.72))          # form-tie holes (x, y) in the tile, about 25 mm


def board_edges(rng) -> np.ndarray:
    """The joints' x positions in pixels: BOARDS widths of 0.8 to 1.2 of the mean, summing to N."""
    w = rng.uniform(0.8, 1.2, BOARDS)
    edges = np.round(np.cumsum(w) / w.sum() * N).astype(int)
    return np.r_[0, edges]                   # 0 .. N; N is the same joint as 0 (the wrap)


def spots(n: int, seed: int, radius: float, share: float) -> np.ndarray:
    """Soft, irregular spots on a random `share` of an n x n cell grid (radius in cell units)."""
    warp = (0.25 * (tl.noise(4 * n, seed + 2) - 0.5), 0.25 * (tl.noise(4 * n, seed + 3) - 0.5))
    d1, _, cid = tl.cells(n, seed, warp=warp)
    rng = np.random.RandomState(seed + 1)
    keep, size = rng.rand(n * n)[cid] < share, (0.4 + 0.6 * rng.rand(n * n))[cid]
    r = radius * size
    return np.clip((r - d1) / (0.3 * r), 0, 1) * keep


def grain(seed: int) -> np.ndarray:
    """The sawn grain's imprint: fine streaks along y, wandering a few pixels, in [0, 1]."""
    rng = np.random.RandomState(seed)
    line = rng.rand(N)
    line = 0.5 * line + 0.25 * (np.roll(line, 1) + np.roll(line, -1))   # streaks 1 to 2 mm wide
    line = (line - line.min()) / (line.max() - line.min())
    wobble = (6.0 * (tl.noise(5, seed + 1) - 0.5) + 3.0 * (tl.noise(23, seed + 2) - 0.5)
              + 1.5 * (tl.noise(97, seed + 4) - 0.5))
    x = (np.arange(N)[None, :] + wobble) % N
    i0 = np.floor(x).astype(int)
    f = x - i0
    streak = line[i0] * (1 - f) + line[(i0 + 1) % N] * f
    saw = tl.noise(41, seed + 3)             # the saw's chatter: the grain comes and goes along y
    s = streak * (0.6 + 0.4 * saw)
    return np.clip((s - s.mean()) / (3 * s.std()) + 0.5, 0, 1)    # full contrast, about +-3 sigma


def maps() -> dict:
    rng = np.random.RandomState(SEED)
    edges = board_edges(rng)
    xs = np.arange(N)
    board = np.searchsorted(edges, xs, side="right") - 1          # each column's board, 0..BOARDS-1
    k = BOARDS
    tone = rng.uniform(-1, 1, k)[board][None, :]                   # one board soaked more water
    plane = rng.uniform(-1, 1, k)[board][None, :]                  # one board sat a little proud
    warmth = rng.uniform(-1, 1, k)[board][None, :]

    # Distance to the nearest joint, in pixels, wobbling along y as the boards' edges do.
    lo, hi = edges[board], edges[board + 1]
    edge_wob = 1.5 * (tl.noise(37, SEED + 5) - 0.5)
    d_joint = np.minimum(xs[None, :] - lo[None, :], hi[None, :] - xs[None, :]) + edge_wob
    fin = np.clip(1.0 - np.abs(d_joint) / 2.5, 0, 1)               # a paste fin about 4 mm wide
    gap = np.clip(1.0 - np.abs(d_joint - 3.5) / 2.0, 0, 1)         # the shadow beside it

    # Each board's grain is its own: shift one grain field per board.
    g = grain(SEED + 10)
    shift = rng.randint(0, N, k)
    gb = np.empty_like(g)
    for b in range(k):
        cols = board == b
        gb[:, cols] = np.roll(g, shift[b], axis=1)[:, cols]

    # Knots: a few dark eyes with a ring of swirled grain, on some boards.
    yy, xx = np.mgrid[0:N, 0:N].astype(float)
    knot = np.zeros((N, N))
    for _ in range(3):
        b = rng.randint(k)
        cx = (edges[b] + edges[b + 1]) / 2 + rng.uniform(-15, 15)
        cy = rng.uniform(0, N)
        dx = (xx - cx + N / 2) % N - N / 2
        dy = ((yy - cy + N / 2) % N - N / 2) / 2.2                # knots are longer along the grain
        r = np.hypot(dx, dy)
        knot = np.maximum(knot, np.clip(1 - r / 9, 0, 1) + 0.35 * np.clip(1 - np.abs(r - 16) / 3, 0, 1))

    cloud = (0.15 * tl.noise(2, SEED + 20) + 0.35 * tl.noise(5, SEED + 21)
             + 0.30 * tl.noise(11, SEED + 22) + 0.20 * tl.noise(29, SEED + 23))
    fine = tl.fbm((71, 143), SEED + 24)                            # sand texture: 14, 7 mm
    bugs = spots(70, SEED + 30, 0.16, 0.07)                       # bug holes, 1 to 2.5 mm, sparse
    ties = np.zeros((N, N))
    for tx, ty in TIES:
        dx = (xx - tx * N + N / 2) % N - N / 2
        dy = (yy - ty * N + N / 2) % N - N / 2
        r = np.hypot(dx, dy)
        ties = np.maximum(ties, np.clip((12 - r) / 5, 0, 1))   # a cone, filled grout grey

    shade = (1.0 + 0.12 * (cloud - 0.5) + 0.09 * tone + 0.16 * (gb - 0.5) + 0.04 * (fine - 0.5)
             - 0.18 * knot + 0.06 * fin - 0.12 * gap - 0.30 * bugs - 0.22 * ties)
    drift = 1.0 + 0.02 * warmth[..., None] * np.array([1.0, 0.3, -1.0])
    albedo = PB_CONCRETE[None, None, :] * shade[..., None] * drift
    albedo *= PB_CONCRETE / albedo.reshape(-1, 3).mean(0)          # re-anchor the MEAN to PB exactly

    rough = (0.08 * (gb - 0.5) + 0.05 * (cloud - 0.5) + 0.04 * (fine - 0.5)
             + 0.25 * bugs + 0.25 * ties + 0.05 * gap)
    rough = np.clip(rough - rough.mean() + ROUGH_MEAN, 0.3, 0.85)

    height = (0.8 * plane + 1.5 * gb + 0.8 * knot + 1.2 * fin - 0.8 * gap
              + 0.4 * cloud + 0.2 * fine - 2.0 * bugs - 4.0 * ties)
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=1.5)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Concrete_BoardFormed base texture set.")
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
