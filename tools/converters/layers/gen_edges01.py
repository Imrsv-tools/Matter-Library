#!/usr/bin/env python3
"""Generate the shared mask `Edges01` (Phase11 step 11.3): wear gathered along borders.

A mask only GATES layers (never colour). Frozen mask contract (MasterSet.md):

    R = layer-2 coverage (TwoLayer only)  ·  G/B/A = where overlays 1/2/3 may appear

Edges01 is for matter whose wear follows edges and seams (metal panels and plates, gem
facets, tiles of a glaze, enamel, painted trim): the tile is divided into irregular facets
(a toroidal Voronoi diagram, straight-sided like panels or facets), and each channel follows
their borders differently:

- R: the top layer worn through along some borders (a TwoLayer's second layer showing at
  the edges), in broken stretches up to 2.5 mm deep, crisp-edged;
- G: overlay 1 (damage: chips, edge wear, scratches) in a narrow, ragged band along every
  border, 2-8 mm deep;
- B: overlay 2 (a deposit: dust, grime) in a broad soft band, heaviest in the corners where
  two borders meet;
- A: overlay 3 (handling: fingerprints, hairline scratches, water spots) on the open faces,
  away from the borders.

⚠ A tiling mask cannot know the mesh's real edges: these are the edges of facets drawn in
the tile, not of the model (the library has no curvature or occlusion input yet).

Scale `s01` (0.1 m tile, 0.1 mm per pixel): facets of ~2-4 cm. Seamless, fixed seed.

    gen_edges01.py [--out DIR]         # default: MatterLibrary/textures/shared/masks/

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
NAME = "Edges01_s01.png"
SEED = 641
SIZE = tl.SIZE
FACETS = 14


def _wrap(d: np.ndarray) -> np.ndarray:
    return (d + SIZE / 2) % SIZE - SIZE / 2


def blur(f: np.ndarray, sigma: float) -> np.ndarray:
    """A Gaussian blur that wraps (done in the frequency domain), so the tile stays seamless."""
    k = np.fft.fftfreq(SIZE)
    g = np.exp(-2 * (np.pi * sigma) ** 2 * (k[:, None] ** 2 + k[None, :] ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(f) * g))


def edges() -> tuple:
    """Distance (px) to the nearest facet border, and to the second-nearest border."""
    rng = np.random.RandomState(SEED)
    pts = rng.rand(FACETS, 2) * SIZE
    y, x = np.mgrid[0:SIZE, 0:SIZE].astype(np.float64)
    d = np.stack([np.hypot(_wrap(x - px), _wrap(y - py)) for px, py in pts])
    order = np.argsort(d, axis=0)
    i1 = order[0]
    d1 = np.take_along_axis(d, order[:1], 0)[0]
    best = np.full(x.shape, np.inf)
    second = np.full(x.shape, np.inf)
    for k in range(1, 4):                                        # borders with the next 3 cells
        ik = order[k]
        dk = np.take_along_axis(d, order[k:k + 1], 0)[0]
        sep = np.hypot(_wrap(pts[i1, 0] - pts[ik, 0]), _wrap(pts[i1, 1] - pts[ik, 1]))
        e = (dk ** 2 - d1 ** 2) / (2 * np.maximum(sep, 1e-6))
        second = np.where(e < best, best, np.minimum(second, e))
        best = np.minimum(best, e)
    return best, second


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Edges01 shared mask.")
    ap.add_argument("--out", default=str(ROOT / "MatterLibrary" / "textures" / "shared" / "masks"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety)", file=sys.stderr)
        return 1
    e, e2 = edges()
    rag = tl.fbm((24, 48, 96, 192), SEED + 1)                    # ragged, chippy band edge
    along = tl.fbm((6, 12, 24), SEED + 2)                        # varies along a border
    # R: worn through in broken stretches, 0-2.5 mm deep, crisp (a 1.5 px edge)
    wr = 25 * np.clip((along - 0.47) * 4.0, 0, 1) * (0.6 + 0.8 * rag)
    r = np.clip((wr - e) / 1.5 + 0.5, 0, 1) * (wr > 1)
    # G: a narrow ragged damage band along every border, 2-8 mm
    wg = 20 + 60 * along
    g = np.clip(1.0 - e / wg + (rag - 0.5) * 0.9, 0, 1) ** 1.3
    # B: a broad soft band, heaviest where two borders meet (a corner)
    band = np.clip(1.0 - e / 110.0, 0, 1) ** 2
    corner = np.clip(1.0 - e2 / 150.0, 0, 1) ** 2
    b = np.clip(blur(band + corner, 14) * (0.4 + 0.9 * tl.fbm((12, 24), SEED + 3)), 0, 1)
    # A: the open faces, away from the borders
    t = np.clip((e - 25.0) / 75.0, 0, 1)
    a = np.clip(blur(t * t * (3 - 2 * t), 14), 0, 1) * (0.6 + 0.4 * tl.fbm((8, 16), SEED + 4))
    img = tl.pack_mask(r=r, g=g, b=b, a=a)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
