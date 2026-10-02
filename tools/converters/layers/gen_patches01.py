#!/usr/bin/env python3
"""Generate the shared mask `Patches01` (Phase11 step 11.3): large soft irregular patches.

A mask only GATES layers (never colour). Frozen mask contract (MasterSet.md):

    R = layer-2 coverage (TwoLayer only)  ·  G/B/A = where overlays 1/2/3 may appear

Patches01 is the general "wear gathers here, not there" mask for broad surfaces: ground,
paving, sand, soil, leaves, liquids, walls and floors. Each channel is its own patch field,
so the layers gathered by it do not all sit in the same places (a mask whose channels match
hides a wiring mistake, gen_shared_textures.py):

- R: large patches, ~45 % cover (a TwoLayer's second layer: moss, wet, a stain);
- G: overlay 1 (damage: cracks, pitting) in medium patches, ~40 %;
- B: overlay 2 (a deposit: dust, dirt) in broad soft drifts, ~55 %;
- A: overlay 3 (water spots, a second damage layer) in smaller scattered patches, ~30 %.

Each cover fraction is set by the field's own quantile (not by trial), and away from the
patches each gate is truly 0, so a dialled-up layer reads as patches, not as a wash.

Scale `s1` (1 m tile, 1 mm per pixel): patches of ~3-30 cm, soft edges of 1-5 cm. On an
article at a 10 cm tile, one patch edge crosses it. Seamless, fixed seed.

    gen_patches01.py [--out DIR]       # default: MatterLibrary/textures/shared/masks/

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
NAME = "Patches01_s1.png"
SEED = 651


def blur(f: np.ndarray, sigma: float) -> np.ndarray:
    """A Gaussian blur that wraps (done in the frequency domain), so the tile stays seamless."""
    k = np.fft.fftfreq(f.shape[0])
    g = np.exp(-2 * (np.pi * sigma) ** 2 * (k[:, None] ** 2 + k[None, :] ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(f) * g))


def patches(scales: tuple, seed: int, cover: float, soft: float) -> np.ndarray:
    """Soft patches covering about `cover` of the tile; `soft` is the edge ramp in the
    field's standard deviations (smaller = crisper), then a 1 cm blur softens the edge."""
    f = tl.fbm(scales, seed)
    q = np.quantile(f, 1.0 - cover)
    t = np.clip((f - q) / (soft * f.std()) + 0.5, 0, 1)
    return np.clip(blur(t * t * (3 - 2 * t), 10.0), 0, 1)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Patches01 shared mask.")
    ap.add_argument("--out", default=str(ROOT / "MatterLibrary" / "textures" / "shared" / "masks"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety)", file=sys.stderr)
        return 1
    img = tl.pack_mask(
        r=patches((5, 10, 20, 40, 80), SEED, cover=0.45, soft=0.6),
        g=patches((7, 14, 28, 56, 112), SEED + 10, cover=0.40, soft=0.6),
        b=patches((4, 8, 16, 32), SEED + 20, cover=0.55, soft=1.0),
        a=patches((11, 22, 44, 88, 176), SEED + 30, cover=0.30, soft=0.6),
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
