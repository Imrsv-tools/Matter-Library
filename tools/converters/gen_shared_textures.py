#!/usr/bin/env python3
"""Deterministically generate the shared overlay/maskset textures (Phase 53; rewritten 71.11).

⭐ Phase 71 — THESE ARE DATA TEXTURES, NOT ALBEDO.

Until this rewrite they were painted as *colour* bitmaps (the `_basecolor_` in their old
filenames was the tell) and the assembler duly mixed them over base colour. MasterSet.md is
now normative — an overlay and a maskset are both MODULATORS, and neither may ever contribute
colour. So they are generated packed, per the frozen channel contracts:

    Overlay (RGBA)    R/G = normal XY (0.5 = flat)  ·  B = roughness bias  ·  A = mask density
    MaskSet (RGBA)    R   = layer-2 coverage        ·  G = overlay-1 gate
                      B   = overlay-2 gate          ·  A = reserved (v1)

Both load `lin_rec709`. Loading packed data through an sRGB transfer curve corrupts every
channel it carries, which is exactly what shipped.

⚠ B is a roughness bias in [0,1], so an overlay can only ever ROUGHEN. MasterSet.md writes the
`*2-1` remap for the normal XY and DELIBERATELY not for B. Generated to match: a dust or
scratch layer roughens, and a smoothing overlay would be a spec change, not a texture tweak.

Fixed-seed value noise -> no network, byte-stable for a given seed/size. LFS-tracked
(textures/shared/**).

    gen_shared_textures.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
SHARED = ROOT / "MatterLibrary" / "textures" / "shared"

SIZE = 1024


def _value_noise(size: int, scale: int, seed: int) -> np.ndarray:
    """Smooth value noise in [0,1] from a fixed seed (deterministic)."""
    rng = np.random.RandomState(seed)
    low = rng.rand(scale, scale).astype(np.float64)
    img = Image.fromarray((low * 255).astype(np.uint8)).resize((size, size), Image.BICUBIC)
    return np.asarray(img, dtype=np.float64) / 255.0


def _gradients(height: np.ndarray, strength: float) -> tuple:
    """Tangent-space normal XY from a height field, encoded to [0,1] (0.5 = flat).

    A packed overlay carries the PERTURBATION, so the encoding matches the master's decode:
    `normal_xy = tex.RG * 2 - 1`. Wrapped gradients keep the tile seamless.
    """
    dy, dx = np.gradient(height)
    return (np.clip(-dx * strength * 0.5 + 0.5, 0, 1),
            np.clip(-dy * strength * 0.5 + 0.5, 0, 1))


def _pack(nx, ny, rough_bias, density) -> Image.Image:
    rgba = np.stack([nx, ny, np.clip(rough_bias, 0, 1), np.clip(density, 0, 1)], axis=-1)
    return Image.fromarray((rgba * 255).astype(np.uint8), "RGBA")


def main() -> int:
    (SHARED / "overlays").mkdir(parents=True, exist_ok=True)
    (SHARED / "masks").mkdir(parents=True, exist_ok=True)

    # ── Overlay 1 — DUST. Fine, soft, low-relief grit that settles patchily and roughens.
    # Seeds preserved from the pre-71 generator so the *structure* is recognisably the same
    # layer; only the CHANNEL MEANING changed.
    dust_h = _value_noise(SIZE, 256, seed=11)
    dnx, dny = _gradients(dust_h, strength=6.0)
    dust = _pack(
        nx=dnx, ny=dny,
        rough_bias=0.25 + 0.45 * dust_h,                     # dust is matte: it always roughens
        density=np.clip((dust_h - 0.35) * 2.2, 0, 1),        # patchy coverage, not a full film
    )
    dust.save(SHARED / "overlays" / "Dust01_overlay_s001.png", "PNG", optimize=True)

    # ── Overlay 2 — SCRATCHES. High-frequency directional streaks: sharp normal relief, a
    # narrow roughened line, and a SPARSE mask (a scratch is a thin mark, not a wash).
    scr_h = _value_noise(SIZE, 512, seed=17)
    streak = _value_noise(SIZE, 24, seed=23)                 # low-freq anisotropy -> streaking
    scr_h = np.clip(scr_h * 0.35 + streak * 0.65, 0, 1)
    snx, sny = _gradients(scr_h, strength=14.0)              # scratches bite deeper than dust
    scr = _pack(
        nx=snx, ny=sny,
        rough_bias=0.55 * np.clip((scr_h - 0.55) * 3.0, 0, 1),
        density=np.clip((scr_h - 0.62) * 4.0, 0, 1),         # sparse
    )
    scr.save(SHARED / "overlays" / "Scratches01_overlay_s001.png", "PNG", optimize=True)

    # ── MaskSet — VERDIGRIS. Blotchy patina coverage. R is the layer-2 coverage (what a
    # TwoLayer article blends by); G/B gate where each overlay is ALLOWED to appear. Giving
    # the three channels genuinely different noise is the point: a maskset whose channels are
    # identical is indistinguishable from a single-channel mask and hides a wiring mistake.
    patina = _value_noise(SIZE, 64, seed=29)
    verd = _pack(
        nx=np.clip((patina - 0.30) * 1.8, 0, 1),             # R: layer-2 coverage
        ny=_value_noise(SIZE, 48, seed=31),                  # G: overlay-1 (dust) gate
        rough_bias=_value_noise(SIZE, 96, seed=37),          # B: overlay-2 (scratches) gate
        density=np.ones((SIZE, SIZE)),                       # A: reserved (v1)
    )
    MASKS_DIR = SHARED / "masks"
    verd.save(MASKS_DIR / "Verdigris01_s01.png", "PNG", optimize=True)

    # ── MaskSet — GRIME. A general "where is this surface dirty" coverage set, for articles
    # that carry overlays but have no second layer (Glass). R is still layer-2 coverage and is
    # simply unused by such an article; G/B are what it is for — gating WHERE the dust and the
    # scratches are allowed to sit on the pane. This is what lets a maskset be live and
    # semantically correct on a NON-TwoLayer article (MasterSet.md: `maskset_blend` gives the
    # maskset a real job on every master, not only TwoLayer).
    grime = _pack(
        nx=_value_noise(SIZE, 56, seed=41),                  # R: layer-2 coverage (unused here)
        ny=np.clip(_value_noise(SIZE, 28, seed=43) * 1.4, 0, 1),   # G: overlay-1 (dust) gate
        rough_bias=np.clip((_value_noise(SIZE, 60, seed=47) - 0.25) * 1.9, 0, 1),  # B: ov-2 gate
        density=np.ones((SIZE, SIZE)),                       # A: reserved (v1)
    )
    grime.save(MASKS_DIR / "Grime01_s01.png", "PNG", optimize=True)

    for p in ("overlays/Dust01_overlay_s001.png",
              "overlays/Scratches01_overlay_s001.png",
              "masks/Verdigris01_s01.png",
              "masks/Grime01_s01.png"):
        print("wrote", SHARED / p)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
