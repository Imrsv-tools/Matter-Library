#!/usr/bin/env python3
"""Generate the shared mask `PaintChip01` (Phase11 step 11.3): chipped paint over a substrate.

A mask only GATES layers (never colour). Frozen mask contract (MasterSet.md):

    R = layer-2 coverage (TwoLayer only)  ·  G/B/A = where overlays 1/2/3 may appear

PaintChip01 is the TwoLayer mask for a coat that flakes off (paint on metal or wood, enamel,
powder coat, glaze on a body): layer 1 is the coat, layer 2 the substrate, and R says where
the coat has chipped off to show it. RustBloom01 (gen_article_textures.py) is the same kind
of mask for rust; its R is a blotchy soft field, this one is sharp-edged flakes:

- R: chips, ~15 % cover, crisp-edged (a 1-pixel anti-aliased edge), angular like a flake
  of paint (unions of small Voronoi cells, in two sizes), gathered in clusters where the
  coat has failed, with lone flakes between;
- G: overlay 1 (damage: edge wear, scratches, scuffs) in a halo 1-3 mm around each chip,
  where the coat is cracked and lifting, and in the chip itself;
- B: overlay 2 (a deposit: dust, dirt) settled in the chips, plus soft patches;
- A: overlay 3 (a stain: water spots, rust run) in a broad soft area round each cluster.

The chips are sharp at the defaults (balance 0.5, contrast 0); `layer_blend_contrast` only
crisps them further. Like RustBloom01 on Rust_OnSteel, `maskset_blend` must be non-zero on a
TwoLayer article, or the substrate never shows.

Scale `s01` (0.1 m tile, 0.1 mm per pixel): flakes of ~1-12 mm. The cells are a Voronoi
diagram on a warped, wrapped plane, and every blur wraps, so the tile is seamless. Fixed
seed, no network: byte-stable.

    gen_paintchip01.py [--out DIR]     # default: MatterLibrary/textures/shared/masks/

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
NAME = "PaintChip01_s01.png"
SEED = 661
SIZE = tl.SIZE
COVER = 0.15           # share of the tile chipped bare


def _wrap(d: np.ndarray) -> np.ndarray:
    return (d + SIZE / 2) % SIZE - SIZE / 2


def blur(f: np.ndarray, sigma: float) -> np.ndarray:
    """A Gaussian blur that wraps (done in the frequency domain), so the tile stays seamless."""
    k = np.fft.fftfreq(SIZE)
    g = np.exp(-2 * (np.pi * sigma) ** 2 * (k[:, None] ** 2 + k[None, :] ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(f) * g))


def cells(points: np.ndarray, X: np.ndarray, Y: np.ndarray) -> tuple:
    """Per pixel: the nearest and second-nearest cell, and the distance (px) to their border."""
    d1 = np.full(X.shape, np.inf); d2 = np.full(X.shape, np.inf)
    i1 = np.zeros(X.shape, int); i2 = np.zeros(X.shape, int)
    for k, (px, py) in enumerate(points):
        d = np.hypot(_wrap(X - px), _wrap(Y - py))
        closer = d < d1
        second = ~closer & (d < d2)
        d2 = np.where(closer, d1, np.where(second, d, d2))
        i2 = np.where(closer, i1, np.where(second, k, i2))
        d1 = np.where(closer, d, d1)
        i1 = np.where(closer, k, i1)
    sep = np.hypot(_wrap(points[i1, 0] - points[i2, 0]), _wrap(points[i1, 1] - points[i2, 1]))
    return i1, i2, (d2 ** 2 - d1 ** 2) / (2 * np.maximum(sep, 1e-6))


def chips() -> np.ndarray:
    rng = np.random.RandomState(SEED)
    y, x = np.mgrid[0:SIZE, 0:SIZE].astype(np.float64)
    wx = (tl.fbm((12, 24, 48), SEED + 1) - 0.5) * 30             # irregular cells
    wy = (tl.fbm((12, 24, 48), SEED + 2) - 0.5) * 30
    jx = (tl.fbm((128, 256), SEED + 5) - 0.5) * 9                # a ragged, torn flake edge
    jy = (tl.fbm((128, 256), SEED + 6) - 0.5) * 9
    X, Y = (x + wx + jx) % SIZE, (y + wy + jy) % SIZE
    failed = tl.fbm((3, 6, 12), SEED + 3)                        # where the coat has failed
    lo_f, hi_f = np.quantile(failed, [0.05, 0.95])
    failed = np.clip((failed - lo_f) / (hi_f - lo_f), 0, 1)
    sel_all = []
    edge_all = []
    for n, bias in ((300, 1.0), (900, 1.15)):                    # large flakes, small flakes
        pts = rng.rand(n, 2) * SIZE
        i1, i2, e = cells(pts, X, Y)
        # a cell chips with odds in proportion to its weight (weight / uniform > threshold):
        # 8x likelier where the coat failed, so clusters, but lone flakes can land anywhere
        weight = (0.15 + failed[pts[:, 1].astype(int), pts[:, 0].astype(int)]) * bias
        score = weight / np.maximum(rng.rand(n), 1e-9)
        sel_all.append((score, i1, i2, e))
    # one threshold for both sizes, set so the union covers COVER of the tile
    def union(th: float) -> np.ndarray:
        r = np.zeros((SIZE, SIZE))
        for score, i1, i2, e in sel_all:
            s = score > th
            a, b = s[i1].astype(float), s[i2].astype(float)
            # crisp: 1 inside a chosen cell, 0 outside, a 1 px ramp across a chip border
            v = np.where(a == b, a, 0.5 + (a - 0.5) * np.clip(e, 0, 1))
            r = np.maximum(r, v)
        return r
    lo, hi = 0.0, 50.0
    for _ in range(30):                                          # bisection on the cover
        mid = (lo + hi) / 2
        if union(mid).mean() > COVER:
            lo = mid
        else:
            hi = mid
    return union(hi)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the PaintChip01 shared mask.")
    ap.add_argument("--out", default=str(ROOT / "MatterLibrary" / "textures" / "shared" / "masks"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety)", file=sys.stderr)
        return 1
    r = chips()
    halo = np.clip(blur(r, 12.0) * 2.8, 0, 1)                    # 1-3 mm round each chip
    drift = tl.fbm((6, 12, 24), SEED + 4)
    soft = np.clip((drift - np.quantile(drift, 0.75)) / (0.5 * drift.std()) + 0.5, 0, 1)
    cluster = blur(r, 60.0)
    img = tl.pack_mask(
        r=r,
        g=np.maximum(r, halo),
        b=np.maximum(0.9 * r, soft),
        a=np.clip(cluster / np.quantile(cluster, 0.9), 0, 1) ** 1.5,
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
