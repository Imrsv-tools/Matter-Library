#!/usr/bin/env python3
"""Generate the shared mask `RustFlake01` (batch 261016-2): flaking rust over bare steel.

A mask only GATES layers (never colour). Frozen mask contract (MasterSet.md):

    R = layer-2 coverage (TwoLayer only)  ·  G/B/A = where overlays 1/2/3 may appear

RustFlake01 is the TwoLayer mask for rust on iron or steel: layer 1 is the metal, layer 2
the rust, and R says where the rust has grown. It replaces RustBloom01 on Rust_OnSteel,
whose R is a 10 cm tile of 5 mm blobs and so reads as a speckle, not as rust:

- R: rust, ~55 % cover, in blooms a few cm to a few dm across that merge into fields, with
  bare steel between. R is GRADED, not a step: 0.5 is the bloom's edge and it rises to 1
  in a bloom's heart (falling to 0 on the bare steel) over several EDGE spans of the field,
  so `layer_blend_balance` grows or shrinks the rust visibly. Near the edge
  each flake (a cell of ~4-12 mm) tips in or out on its own, so the edge is ragged and
  broken into flakes, never a smooth contour; `layer_blend_contrast` crisps it;
- G: overlay 1 (damage: pitting) in and round the rust, where the steel has corroded;
- B: overlay 2 (a deposit: dust, dirt) caught in the rough rust, plus soft patches;
- A: overlay 3 (a stain: water spots) on the bare steel, in broad soft areas.

Scale `s1` (1 m tile, 2048 px, about 0.5 mm per pixel): it is sampled at its own size, so
the blooms are sized in metres whatever the article's tile. The noise is periodic and every
blur wraps, so the tile is seamless. Fixed seed, no network: byte-stable.

    gen_rustflake01.py [--out DIR]     # default: MatterLibrary/textures/shared/masks/

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
NAME = "RustFlake01_s1.png"
SEED = 1607
SIZE = 2048
COVER = 0.55           # share of the tile under rust (R > 0.5)
EDGE = 0.06            # the field's span from bare to full rust, as a share of its range
FLAKES = 128           # flake cells across the tile: about 8 mm each
GRADE = 0.18           # R's rise per EDGE of the field: wide enough for layer_blend_balance to move the edge


def blur(f: np.ndarray, sigma: float) -> np.ndarray:
    """A Gaussian blur that wraps (done in the frequency domain), so the tile stays seamless."""
    k = np.fft.fftfreq(SIZE)
    g = np.exp(-2 * (np.pi * sigma) ** 2 * (k[:, None] ** 2 + k[None, :] ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(f) * g))


def norm(f: np.ndarray) -> np.ndarray:
    lo, hi = np.quantile(f, [0.01, 0.99])
    return np.clip((f - lo) / (hi - lo), 0, 1)


def rust() -> np.ndarray:
    # Where the rust grows: a broad field (blooms of cm to dm), cut at the cover.
    field = norm(tl.fbm((6, 12, 24, 48, 96), SEED, SIZE))
    edge = np.quantile(field, 1 - COVER)
    d = (field - edge) / EDGE                                   # 0 at the bloom's edge
    # Each flake tips in or out on its own near the edge: a value per cell, two sizes.
    _, _, big = tl.cells(FLAKES, SEED + 1, SIZE)
    _, _, small = tl.cells(FLAKES * 3, SEED + 2, SIZE)
    rng = np.random.RandomState(SEED + 3)
    tip = 1.2 * (rng.rand(FLAKES ** 2)[big] - 0.5) + 0.5 * (rng.rand((FLAKES * 3) ** 2)[small] - 0.5)
    r = np.clip(0.5 + GRADE * (d + tip), 0, 1)
    return r


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the RustFlake01 shared mask.")
    ap.add_argument("--out", default=str(ROOT / "MatterLibrary" / "textures" / "shared" / "masks"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety)", file=sys.stderr)
        return 1
    r = rust()
    solid = (r > 0.5).astype(float)
    near = np.clip(blur(solid, 24.0) * 2.2, 0, 1)               # ~1 cm round the rust
    patches = norm(tl.fbm((6, 12, 24), SEED + 4, SIZE))
    soft = np.clip((patches - 0.6) * 3, 0, 1)
    stain = norm(tl.fbm((3, 6, 12), SEED + 5, SIZE))
    img = tl.pack_mask(
        r=r,
        g=np.maximum(solid, near),
        b=np.maximum(0.9 * solid, soft),
        a=np.clip((stain - 0.55) * 3, 0, 1) * (1 - solid),
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}  (rust cover {solid.mean():.2f}, mean R {r.mean():.2f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
