#!/usr/bin/env python3
"""An HDRI's cube sibling for Unreal (#424, RD-SKY-4): a BC6H_UF16 cubemap ``.dds`` beside its ``.hdr``.

The cube is the one the IMRSV platform's runtime loader builds from the ``.hdr`` today
(``IMRSVRuntimeMedia``'s ``RuntimeMedia::BuildCubePlatformData``, ``SphericalToCubemap.cpp``), so a
Sky looks the same whichever file Studio loads: same faces, same turns, same sampling, quirks and
all, but one: a sun brighter than half float's range is clamped, where the runtime makes Inf and
NaN. ``equirect_to_cube`` is a port of it; keep the two in step (the platform's mapping-parity
test compares them).
"""

from __future__ import annotations

import os
import struct
import tempfile
from pathlib import Path

import numpy as np

import compress_textures as CT

# The runtime's face cap (FRuntimeHDRILoader::MaxSkyFaceSize).
MAX_FACE = 2048
_BC6H_UF16 = 95
_CUBE = 0x4                 # DDS_RESOURCE_MISC_TEXTURECUBE
_ARRAY_SIZE_AT = 4 + 124 + 12   # the DX10 header's arraySize: the number of CUBES, so 1


def read_hdr(path: Path) -> np.ndarray:
    """A Radiance ``.hdr`` (run-length RGBE, top row first, as the library's HDRIs are: the HDRI
    check) as float32 [row, column, rgb], decoded as the runtime does: mantissa x 2^(exponent - 136),
    no half-step added."""
    data = Path(path).read_bytes()
    end = data.find(b"\n\n")
    line_end = data.find(b"\n", end + 2)
    if not data.startswith(b"#?") or end < 0 or line_end < 0:
        raise ValueError(f"{path}: not a Radiance file")
    axes = data[end + 2:line_end].split()
    if len(axes) != 4 or axes[0] != b"-Y" or axes[2] != b"+X":
        raise ValueError(f"{path}: rows must run -Y +X (got {data[end + 2:line_end]!r})")
    height, width = int(axes[1]), int(axes[3])
    buf, pos = memoryview(data), line_end + 1
    rgbe = np.empty((height, 4, width), np.uint8)
    for row in range(height):
        if bytes(buf[pos:pos + 4]) != b"\x02\x02" + width.to_bytes(2, "big"):
            raise ValueError(f"{path}: row {row} is not a run-length scanline of width {width}")
        pos += 4
        for channel in range(4):
            out, x = rgbe[row, channel], 0
            while x < width:
                count = buf[pos]
                run = count > 128                     # a run: one byte, count - 128 times
                count -= 128 if run else 0            # else count bytes as they are
                size = 1 if run else count
                if not 0 < count <= width - x or pos + 1 + size > len(buf):
                    raise ValueError(f"{path}: row {row} has a broken run-length packet")
                out[x:x + count] = buf[pos + 1] if run else buf[pos + 1:pos + 1 + count]
                pos += 1 + size
                x += count
    rgbe = rgbe.transpose(0, 2, 1)
    exponent = rgbe[..., 3].astype(np.float32)
    scale = np.where(rgbe[..., 3] > 0, np.exp2(exponent - 136), 0).astype(np.float32)
    return rgbe[..., :3].astype(np.float32) * scale[..., None]


def _mip_bytes(size: int) -> int:
    """One face's BC6H bytes, every mip: 16 bytes a 4 x 4 block, at least one block a mip."""
    return sum(16 * max(1, (max(size >> m, 1) + 3) // 4) ** 2 for m in range(CT.full_miplevels(size, size)))


def _float_cube_dds(cube: np.ndarray) -> bytes:
    """The float16 cube as an uncompressed R16G16B16A16_FLOAT cube .dds (one mip): the encoder's input."""
    size = cube.shape[1]
    head = bytearray(124)
    struct.pack_into("<7I", head, 0, 124, 0x100F, size, size, size * 8, 0, 1)
    struct.pack_into("<II4s", head, 72, 32, 0x4, b"DX10")
    struct.pack_into("<II", head, 104, 0x1008, 0xFE00)          # complex | texture; every face
    dx10 = struct.pack("<5I", 10, 3, _CUBE, 1, 0)               # R16G16B16A16_FLOAT, 2D, cube
    rgba = np.ones(cube.shape[:3] + (4,), "<f2")
    rgba[..., :3] = cube
    return b"DDS " + bytes(head) + dx10 + rgba.tobytes()


def build_cube_dds(hdr: Path, dst: Path) -> None:
    """Write ``dst``: the runtime's cube of ``hdr`` as a BC6H_UF16 cube .dds with every mip, made
    by the pinned encoder (it keeps a cube's faces, one after another, each with its mips), checked,
    and swapped in whole. Raises when it cannot."""
    cube = equirect_to_cube(read_hdr(hdr))
    dst.parent.mkdir(parents=True, exist_ok=True)
    # Beside dst, not in the system temp: the encoder may run in a container that sees only some paths
    with tempfile.TemporaryDirectory(dir=dst.parent, prefix=".cube-") as tmp:
        src, out = Path(tmp) / "float.dds", Path(tmp) / "bc6h.dds"
        src.write_bytes(_float_cube_dds(cube))
        size = cube.shape[1]
        if not CT.compress_one(src, out, "BC6H", CT.full_miplevels(size, size)):
            raise RuntimeError(f"the compressor failed on {hdr.name}")
        with out.open("r+b") as f:         # the encoder writes arraySize 6 (the faces), not 1 cube
            f.seek(_ARRAY_SIZE_AT)
            f.write(struct.pack("<I", 1))
        problems = validate_cube_dds(out, size)
        if problems:
            raise RuntimeError(f"{hdr.name}'s cube failed its check: {'; '.join(problems)}")
        os.replace(out, dst)


def validate_cube_dds(dds: Path, size: int) -> list[str]:
    """What is wrong with an HDRI's cube sibling ([] when nothing): a BC6H_UF16 cube of
    ``size`` faces with every mip, its six faces' bytes all there."""
    try:
        h = CT.read_dds_header(dds)
    except (OSError, ValueError) as e:
        return [f"unreadable: {e}"]
    problems = []
    if h["dxgi"] != _BC6H_UF16:
        problems.append(f"format {h['dxgi'] or h['fourcc']} is not BC6H_UF16")
    if not h["misc"] or not h["misc"] & _CUBE or h["array_size"] != 1:
        problems.append(f"not one cube (miscFlag {h['misc']}, arraySize {h['array_size']})")
    if (h["width"], h["height"]) != (size, size):
        problems.append(f"faces {h['width']} x {h['height']}, not {size} x {size}")
    if h["mipcount"] != CT.full_miplevels(size, size):
        problems.append(f"{h['mipcount']} mips, not {CT.full_miplevels(size, size)}")
    if not problems and dds.stat().st_size != 148 + 6 * _mip_bytes(size):
        problems.append(f"{dds.stat().st_size} bytes, not six faces' {148 + 6 * _mip_bytes(size)}")
    return problems

# The runtime's faces: where each one starts, which way its columns and rows run, the UE slice
# (+X, -X, +Y, -Y, +Z, -Z) it lands in, and how it is turned there (np.rot90 turns: WalkFor's
# TurnXP is one, TurnXN minus one, Flip two). The image's Y faces go to UE's Z slices and back.
_FACES = (
    ((1, -1, -1), (0, 0, 1), (0, 1, 0), 0, 1),
    ((-1, -1, 1), (0, 0, -1), (0, 1, 0), 1, -1),
    ((-1, -1, 1), (1, 0, 0), (0, 0, -1), 4, 0),
    ((-1, 1, -1), (1, 0, 0), (0, 0, 1), 5, 2),
    ((-1, -1, -1), (1, 0, 0), (0, 1, 0), 3, 0),
    ((1, -1, 1), (-1, 0, 0), (0, 1, 0), 2, 2),
)


def _sample_face(img: np.ndarray, size: int, start, right, up) -> np.ndarray:
    """One face, sampled from the equirect by direction (SampleFace), rows by PixelY."""
    height, width = img.shape[:2]
    # The runtime's (2i + 0.5) / R, not the texel centre's (2i + 1) / R: kept, so the cubes match.
    steps = (np.arange(size, dtype=np.float32) * 2 + np.float32(0.5)) / np.float32(size)
    v, u = np.meshgrid(steps, steps, indexing="ij")
    p = [np.float32(start[k]) + u * np.float32(right[k]) + v * np.float32(up[k]) for k in range(3)]
    azimuth = np.arctan2(p[0], -p[2]) + np.float32(np.pi)
    elevation = np.arctan(p[1] / np.sqrt(p[0] * p[0] + p[2] * p[2])) + np.float32(np.pi / 2)
    sx = (azimuth / np.float32(np.pi) / 2) * width - np.float32(0.5)
    sy = (elevation / np.float32(np.pi)) * height - np.float32(0.5)
    x0, y0 = np.floor(sx).astype(np.int64), np.floor(sy).astype(np.int64)
    fx, fy = (sx - x0)[..., None], (sy - y0)[..., None]
    x2, x3 = x0 % width, (x0 + 1) % width                  # the sky wraps sideways
    y2, y3 = np.clip(y0, 0, height - 1), np.clip(y0 + 1, 0, height - 1)   # the poles don't
    c00, c10, c01, c11 = img[y2, x2], img[y2, x3], img[y3, x2], img[y3, x3]
    top = c00 + (c10 - c00) * fx                           # FMath::BiLerp
    bottom = c01 + (c11 - c01) * fx
    return top + (bottom - top) * fy


def equirect_to_cube(img: np.ndarray) -> np.ndarray:
    """The six faces (UE slice order, each [row, column, rgb], float16 as the runtime stores them)
    of the cube the runtime builds from a 2:1 equirect, faces capped at ``MAX_FACE``."""
    height, width = img.shape[:2]
    if width != 2 * height:
        raise ValueError(f"an equirect is 2:1; this one is {width} x {height}")
    size = min(height, MAX_FACE)
    # The runtime samples FFloat16 pixels. Its FFloat16(float) stores a sun brighter than half's
    # largest value as +Inf, and the blend then makes NaN; BC6H holds neither, so clamp (SetClamped).
    src = np.minimum(img[..., :3], np.finfo(np.float16).max).astype(np.float16).astype(np.float32)
    cube = np.empty((6, size, size, 3), np.float16)       # assigning rounds, as the runtime does
    for start, right, up, slice_, turns in _FACES:
        cube[slice_] = np.rot90(_sample_face(src, size, start, right, up), turns)
    return cube
