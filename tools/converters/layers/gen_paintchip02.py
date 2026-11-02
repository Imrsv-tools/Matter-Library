#!/usr/bin/env python3
"""Generate the shared mask `PaintChip02` (batch 261101-1): chipped paint over a substrate, at 1 m.

A mask only GATES layers (never colour). Frozen mask contract (MasterSet.md):

    R = layer-2 coverage (TwoLayer only)  ·  G/B/A = where overlays 1/2/3 may appear

PaintChip02 is PaintChip01's design over a 1 m tile instead of a 10 cm one. PaintChip01 holds
one fixed layout of chips in 10 cm, so on any face larger than a hand it repeats as a grid
(the maintainer's redo of Paint_OnMetal_Chipped, 2026-11-01: "this pattern is also super
repetitive"). Here the chips keep their real size but are spread over a metre, and they
gather: the coat fails in patches a few cm to a couple of dm across, chipped thickly there,
with long intact stretches between and only a few lone flakes:

- R: chips, ~12 % cover, crisp-edged (about a 1-pixel anti-aliased edge), angular like a flake
  of paint (warped Voronoi cells, in two sizes, ~2-12 mm), in clusters where the coat failed;
- G: overlay 1 (damage: edge wear, scratches, scuffs) in a halo 1-3 mm around each chip,
  where the coat is cracked and lifting, and in the chip itself;
- B: overlay 2 (a deposit: dust, dirt) settled in the chips, plus soft patches 5 to 15 cm
  across, many to a tile (PaintChip01's were a few large blobs per tile, which dust at 1
  showed as a grid);
- A: overlay 3 (a stain: water spots, rust run) in a broad soft area round each cluster.

Like PaintChip01, `maskset_blend` must be non-zero on a TwoLayer article, or the substrate
never shows.

Scale `s1` (1 m tile, 2048 px, about 0.5 mm per pixel): it is sampled at its own size, so the
chips are sized in millimetres whatever the article's tile. The noise is periodic and every
blur wraps, so the tile is seamless. Fixed seed, no network: byte-stable.

    gen_paintchip02.py [--out DIR]     # default: MatterLibrary/textures/shared/masks/

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
NAME = "PaintChip02_s1.png"
SEED = 662
SIZE = 2048
COVER = 0.12           # share of the tile chipped bare
SIZES = (160, 420)     # chip cells across the tile: about 6 mm and 2.4 mm


def blur(f: np.ndarray, sigma: float) -> np.ndarray:
    """A Gaussian blur that wraps (done in the frequency domain), so the tile stays seamless."""
    k = np.fft.fftfreq(SIZE)
    g = np.exp(-2 * (np.pi * sigma) ** 2 * (k[:, None] ** 2 + k[None, :] ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(f) * g))


def norm(f: np.ndarray) -> np.ndarray:
    lo, hi = np.quantile(f, [0.01, 0.99])
    return np.clip((f - lo) / (hi - lo), 0, 1)


def chips() -> np.ndarray:
    # Where the coat has failed: patches of cm to dm, most of the tile intact.
    failed = norm(tl.fbm((5, 10, 20, 40), SEED, SIZE))
    rng = np.random.RandomState(SEED + 1)
    layers = []
    for k, n in enumerate(SIZES):
        warp = (0.35 * (tl.fbm((n // 4, n // 2), SEED + 10 + k, SIZE) - 0.5),
                0.35 * (tl.fbm((n // 4, n // 2), SEED + 20 + k, SIZE) - 0.5))
        _, _, cid = tl.cells(n, SEED + 30 + k, SIZE, warp=warp)
        # each cell draws one number; it chips where that number is under the local odds
        layers.append(rng.rand(n * n)[cid])

    def union(th: float) -> np.ndarray:
        # capped below 1, so islands of paint survive inside a cluster; lone flakes anywhere, rarely
        odds = 0.55 * np.clip((failed - th) * 6, 0, 1) ** 2 + 0.005
        r = np.zeros((SIZE, SIZE))
        for draw in layers:
            r = np.maximum(r, (draw < odds).astype(float))
        return r

    lo, hi = 0.0, 1.0
    for _ in range(25):                                          # bisection on the cover
        mid = (lo + hi) / 2
        if union(mid).mean() > COVER:
            lo = mid
        else:
            hi = mid
    return np.clip(blur(union(hi), 0.6), 0, 1)                    # about a 1 px anti-aliased edge


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the PaintChip02 shared mask.")
    ap.add_argument("--out", default=str(ROOT / "MatterLibrary" / "textures" / "shared" / "masks"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety)", file=sys.stderr)
        return 1
    r = chips()
    halo = np.clip(blur(r, 4.0) * 2.8, 0, 1)                     # 1-3 mm round each chip
    drift = norm(tl.fbm((8, 16, 32), SEED + 4, SIZE))
    soft = np.clip((drift - 0.65) * 3, 0, 1)                     # soft patches, 5-15 cm
    cluster = blur(r, 60.0)                                      # ~3 cm round each cluster
    img = tl.pack_mask(
        r=r,
        g=np.maximum(r, halo),
        b=np.maximum(0.9 * r, soft),
        a=np.clip(cluster / np.quantile(cluster, 0.9), 0, 1) ** 1.5,
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}  (chip cover {r.mean():.3f}, B mean {np.maximum(0.9 * r, soft).mean():.3f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
