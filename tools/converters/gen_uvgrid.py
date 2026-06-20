#!/usr/bin/env python3
"""Deterministically generate the UV-grid diagnostic base-color texture (Phase 53).

A procedural diagnostic grid (per-cell RG gradient + white grid lines) so the UV/grid
proof article exercises uv_scale/offset/rotation against a real texture. No network, no RNG
-- byte-stable for a given (size, cells). LFS-tracked (textures/**).

    gen_uvgrid.py
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent.parent
OUT = (ROOT / "MatterLibrary" / "textures" / "base" / "utility" / "virtual"
       / "UVGrid_basecolor_s1.png")


def generate(size: int = 1024, cells: int = 8) -> Image.Image:
    img = Image.new("RGB", (size, size), (32, 32, 32))
    d = ImageDraw.Draw(img)
    step = size // cells
    for cy in range(cells):
        for cx in range(cells):
            r = round(255 * cx / (cells - 1))
            g = round(255 * cy / (cells - 1))
            d.rectangle([cx * step, cy * step, (cx + 1) * step - 1, (cy + 1) * step - 1],
                        fill=(r, g, 128))
    for i in range(cells + 1):
        x = min(i * step, size - 1)
        d.line([(x, 0), (x, size)], fill=(255, 255, 255), width=2)
        d.line([(0, x), (size, x)], fill=(255, 255, 255), width=2)
    return img


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    generate().save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
