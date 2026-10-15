#!/usr/bin/env python3
"""Deterministically generate the scale grids' base-colour textures (Phase19 19.1).

One grid per scale tag (RD-SP-1), plus the ``sUKN`` hatch. The rules are the lead's (RD-SP-4):

* **a line's colour is its LENGTH**, the same in every grid (blue is 1 m, the lead's example);
* **a grid's background is a dark shade of its own tile length's colour**, so from across the
  room each grid still reads as its own colour;
* **four line levels**: the tile's edge, then each tenth below it, three times. Weight and
  brightness step down with the level, so a colour-blind eye still reads which level a line is.
  The finest level is drawn DIM (D-3): drawn at full strength it takes the grid's colour over
  once the tile is a few hundred pixels across (F-P15-8).

Lines sit at exact metric positions (``k / 10**level`` of the tile), anti-aliased by pixel
coverage, and wrap at the tile's edge, so the edge line is split across the seam and a tiled
surface shows it at full width. The texture is the tile: its real size is the article's
``meters_per_tile``, never its resolution (RD-P19-1).

No network, no RNG: byte-stable for a given tag and size. LFS-tracked (``textures/**``).

    gen_scalegrid.py            # all seven
    gen_scalegrid.py s1 sUKN    # some
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
OUT_DIR = ROOT / "MatterLibrary" / "textures" / "base" / "utility" / "virtual"
SIZE = 4096                     # D-1: flat colours compress to almost nothing

# The tags and their tile lengths in metres (Identity.md §Scale tags; assemble_mtlx.SCALE_TAG_METRES).
TILE_M = {"s0001": 0.001, "s001": 0.01, "s01": 0.1, "s1": 1.0, "s10": 10.0, "s100": 100.0}

# One colour per length, nine lengths: the s0001 grid's finest line (1 µm) to the s100 tile
# (D-2). sRGB. The six tile lengths take the most distinct hues, since they are also backgrounds.
COLOUR = {
    1e-6: (200, 200, 200),      # 1 µm   light grey
    1e-5: (160, 120, 255),      # 10 µm  violet
    1e-4: (0, 215, 215),        # 100 µm cyan
    1e-3: (255, 215, 0),        # 1 mm   yellow
    1e-2: (255, 70, 205),       # 1 cm   magenta
    1e-1: (45, 200, 70),        # 10 cm  green
    1.0: (45, 115, 255),        # 1 m    blue (the lead's example)
    10.0: (255, 140, 0),        # 10 m   orange
    100.0: (230, 35, 35),       # 100 m  red
}
BACKGROUND = 0.35               # a grid's background: its tile colour at this fraction

# Per level (0 = the tile's edge): the line's full width in pixels at SIZE, and its strength.
# Tuned so each grid's AVERAGE colour (what it reads as from across the room, F-P15-8) stays
# within 11 degrees of hue of its own tile colour (Phase19 19.1, measured at 4096 px): the
# finest level's 1 px lines fall every 4.1 px and cover about half the tile, so at the first
# setting (background 0.22, strengths 1/0.9/0.7/0.3) the grids drifted up to 36 degrees.
WIDTH_PX = (12.0, 5.0, 2.0, 1.0)
STRENGTH = (1.0, 0.85, 0.5, 0.18)  # the finest drawn dim (D-3)

# The sUKN hatch: two neutral greys in 45-degree bands, a period that divides SIZE (seamless).
HATCH = ((38, 38, 38), (92, 92, 92))
HATCH_PERIOD = 256


def length_key(metres: float) -> float:
    """The palette's length nearest ``metres`` (they are exact powers of ten)."""
    return min(COLOUR, key=lambda k: abs(np.log10(k) - np.log10(metres)))


def line_coverage(size: int, divisions: int, width_px: float) -> np.ndarray:
    """Per-pixel coverage (0..1) of lines at every 1/``divisions`` of the tile, one axis,
    wrapping at the edge. Pixel centres sit at (i + 0.5) / size."""
    u = (np.arange(size) + 0.5) / size * divisions
    dist_px = np.abs(u - np.round(u)) * (size / divisions)
    return np.clip(width_px / 2 + 0.5 - dist_px, 0.0, 1.0)


def grid(tag: str, size: int = SIZE) -> Image.Image:
    tile = TILE_M[tag]
    img = np.empty((size, size, 3), dtype=np.float64)
    img[:] = np.array(COLOUR[length_key(tile)], dtype=np.float64) * BACKGROUND
    for level in (3, 2, 1, 0):                  # finest first; coarser lines drawn over it
        cov1 = line_coverage(size, 10 ** level, WIDTH_PX[level])
        cov = np.maximum(cov1[None, :], cov1[:, None])[..., None] * STRENGTH[level]
        colour = np.array(COLOUR[length_key(tile / 10 ** level)], dtype=np.float64)
        img = img * (1.0 - cov) + colour * cov
    return Image.fromarray(np.round(img).astype(np.uint8), "RGB")


def hatch(size: int = SIZE) -> Image.Image:
    y, x = np.mgrid[0:size, 0:size] + 0.5
    # half the period light, half dark: a square wave with about 1 px of anti-aliasing (sin's
    # slope at a band edge is 2*pi*sqrt(2)/period per pixel across the band)
    sharp = HATCH_PERIOD / (2 * np.pi * np.sqrt(2))
    t = np.clip(np.sin(2 * np.pi * (x + y) / HATCH_PERIOD) * sharp + 0.5, 0.0, 1.0)[..., None]
    dark, light = (np.array(c, dtype=np.float64) for c in HATCH)
    return Image.fromarray(np.round(dark * (1 - t) + light * t).astype(np.uint8), "RGB")


def out_path(tag: str) -> Path:
    return OUT_DIR / f"ScaleGrid_basecolor_{tag}.png"


def main(argv: list[str]) -> int:
    tags = argv or [*TILE_M, "sUKN"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for tag in tags:
        if tag != "sUKN" and tag not in TILE_M:
            print(f"unknown tag {tag!r} (have {[*TILE_M, 'sUKN']})", file=sys.stderr)
            return 2
        (hatch() if tag == "sUKN" else grid(tag)).save(out_path(tag), "PNG", optimize=True)
        print(f"wrote {out_path(tag)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
