#!/usr/bin/env python3
"""Deterministically generate the shared overlay/mask textures (Phase 53).

The layered-materials marquee needs a shared dust overlay (Concrete article) and a verdigris
patina mask (Copper article). Both are generated procedurally (fixed-seed value noise -> no
network, byte-stable for a given seed/size) so the proof subset exercises the overlay/mask
plumbing without provenance-clouded pixels. LFS-tracked (textures/shared/**).

    gen_shared_textures.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
SHARED = ROOT / "MatterLibrary" / "textures" / "shared"


def _value_noise(size: int, scale: int, seed: int) -> np.ndarray:
    """Smooth value noise in [0,1] from a fixed seed (deterministic)."""
    rng = np.random.RandomState(seed)
    low = rng.rand(scale, scale).astype(np.float64)
    img = Image.fromarray((low * 255).astype(np.uint8)).resize((size, size), Image.BICUBIC)
    arr = np.asarray(img, dtype=np.float64) / 255.0
    return arr


def _tint(noise: np.ndarray, base, contrast=0.4) -> Image.Image:
    n = (noise - 0.5) * contrast + 1.0
    rgb = np.stack([np.clip(base[i] * n, 0, 1) for i in range(3)], axis=-1)
    return Image.fromarray((rgb * 255).astype(np.uint8), "RGB")


def main() -> int:
    (SHARED / "overlays").mkdir(parents=True, exist_ok=True)
    (SHARED / "masks").mkdir(parents=True, exist_ok=True)

    # Dust overlay — pale warm grey, fine-grain noise (s001 = micro scale).
    dust = _tint(_value_noise(1024, 256, seed=11), base=(0.82, 0.80, 0.76), contrast=0.5)
    dust.save(SHARED / "overlays" / "Dust01_basecolor_s001.png", "PNG", optimize=True)

    # Scratches overlay — dark high-contrast streaks (the 2nd overlay layer).
    scr = _tint(_value_noise(1024, 512, seed=17), base=(0.15, 0.15, 0.15), contrast=1.2)
    scr.save(SHARED / "overlays" / "Scratches01_basecolor_s001.png", "PNG", optimize=True)

    # Verdigris mask — green/teal copper patina, blotchy mid-scale noise.
    verd = _tint(_value_noise(1024, 64, seed=29), base=(0.28, 0.56, 0.46), contrast=0.7)
    verd.save(SHARED / "masks" / "Verdigris01_s01.png", "PNG", optimize=True)

    print("wrote", SHARED / "overlays" / "Dust01_basecolor_s001.png")
    print("wrote", SHARED / "overlays" / "Scratches01_basecolor_s001.png")
    print("wrote", SHARED / "masks" / "Verdigris01_s01.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
