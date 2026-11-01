#!/usr/bin/env python3
"""Units for G8's picture size (Phase24 RD-P24-2): a part mesh's picture is square, at its
``map_size`` or a power-of-two multiple of it (the same layout, finer), and its island check reads
the islands at the picture's scale. Every red case asserts its REASON.

    uv run tools/validators/test_g8_size.py        exit 0 = PASS
"""
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import validate_recipe as vr  # noqa: E402

MESH = "MakeHuman_Body_v01"
MAP = HERE.parents[1] / "MatterLibrary" / "textures" / "fit" / "makehuman" / "skin" / "FitzpatrickIII_basecolor_sUKN.png"
fails = []


def check(cond, what):
    print(f"  [{'PASS' if cond else 'FAIL'}] {what}")
    if not cond:
        fails.append(what)


n = vr.G.PART_MESHES[MESH]["map_size"]
check(vr.size_ok((n, n), n), "the mesh's own size passes")
check(vr.size_ok((4 * n, 4 * n), n), "four times the size (8K on a 2048 layout) passes")
check(not vr.size_ok((n // 2, n // 2), n), "half the size is refused")
check(not vr.size_ok((3 * n, 3 * n), n), "three times the size (not a power of two) is refused")
check(not vr.size_ok((2 * n, n), n), "a picture that is not square is refused")

with tempfile.TemporaryDirectory() as tmp:
    px = np.asarray(Image.open(MAP).convert("RGB"))
    big = Path(tmp) / "big.png"
    Image.fromarray(np.repeat(np.repeat(px, 2, 0), 2, 1), "RGB").save(big)
    check(vr.picture_errors(big, MESH) == [], "a shipped map at twice its size covers every island")
    bare = np.repeat(np.repeat(px, 2, 0), 2, 1).copy()
    bare[: n, :] = bare[-1, -1]                     # the top half at the background colour
    hole = Path(tmp) / "hole.png"
    Image.fromarray(bare, "RGB").save(hole)
    check(any("unpainted" in e for e in vr.picture_errors(hole, MESH)),
          "a doubled map with bare islands is refused for its islands, at the islands' scale")
    small = Path(tmp) / "small.png"
    Image.fromarray(px[::2, ::2].copy(), "RGB").save(small)
    check(any("power-of-two multiple" in e for e in vr.picture_errors(small, MESH)),
          "a half-size map is refused for its size")

print("FAIL" if fails else "PASS")
sys.exit(1 if fails else 0)
