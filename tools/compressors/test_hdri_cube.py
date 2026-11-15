#!/usr/bin/env python3
"""Units for an HDRI's BC6H cube sibling (#424): the cube faces point where Unreal's do, and the
built ``.dds`` is the cube Unreal would build from the ``.hdr``. Every red case says what is wrong.

    uv run tools/compressors/test_hdri_cube.py        exit 0 = PASS (the .dds half needs the encoder)

The .dds half builds from a 1024 x 512 copy of a library sky (512 faces, 10 mips): the same code as
a 2048 cube in under a minute, where the full size takes the emulated encoder about twelve. A real
build checks its own size and mips (``validate_cube_dds``).
"""
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compress_textures as CT  # noqa: E402
import hdri_cube as HC  # noqa: E402

fails = []


def check(cond, what):
    print(f"  [{'PASS' if cond else 'FAIL'}] {what}")
    if not cond:
        fails.append(what)


def direction_sky(width: int) -> np.ndarray:
    """An equirect whose every pixel holds its own direction, in Unreal's world (Z up): the top row
    is straight up, and a column's direction turns with u = 0.75 + atan2(y, x) / 2pi, so +X sits
    at u = 0.75, -X at 0.25, +Y at 0 and -Y at 0.5 (what the runtime loader samples for each face's
    centre)."""
    height = width // 2
    v = (np.arange(height) + 0.5) / height
    u = (np.arange(width) + 0.5) / width
    elevation = (np.pi / 2 - v * np.pi)[:, None]
    theta = (2 * np.pi * (u - 0.75))[None, :]
    return np.stack([np.cos(elevation) * np.cos(theta), np.cos(elevation) * np.sin(theta),
                     np.sin(elevation) * np.ones_like(theta)], -1).astype(np.float32)


def d3d_directions(size: int) -> np.ndarray:
    """Each texel's direction on each face, in the D3D cube convention Unreal samples with
    (slices +X, -X, +Y, -Y, +Z, -Z; a texel's column is s, its row t, both -1 .. 1)."""
    t, s = np.meshgrid((2 * np.arange(size) + 1) / size - 1, (2 * np.arange(size) + 1) / size - 1,
                       indexing="ij")
    one = np.ones_like(s)
    faces = [(one, -t, -s), (-one, -t, s), (s, one, t), (s, -one, -t), (s, -t, one), (-s, -t, -one)]
    d = np.stack([np.stack(f, -1) for f in faces])
    return d / np.linalg.norm(d, axis=-1, keepdims=True)


print("== the cube's faces point where Unreal's do ==")
cube = HC.equirect_to_cube(direction_sky(64)).astype(np.float32)
check(cube.shape == (6, 32, 32, 3), f"six 32 x 32 faces from a 64 x 32 sky (got {cube.shape})")
want = d3d_directions(32)
got = cube / np.linalg.norm(cube, axis=-1, keepdims=True)
for i, name in enumerate(("+X", "-X", "+Y", "-Y", "+Z (up)", "-Z (down)")):
    agree = np.einsum("ijk,ijk->ij", got[i], want[i])
    check(agree.min() > 0.99, f"slice {i} ({name}) shows its own directions, turned as Unreal's "
                              f"(worst agreement {agree.min():.3f})")
check(HC.equirect_to_cube(direction_sky(256)).shape[1] == 128,
      "a face below the cap is the sky's height")
bright = HC.equirect_to_cube(np.abs(direction_sky(64)) * 1e6)     # light is never negative
check(np.isfinite(bright).all() and bright.max() == np.finfo(np.float16).max,
      "a sun beyond half float's range is clamped to its largest value, not made Inf or NaN")

print("== a broken .hdr is refused, not read as a wrong picture ==")


def tiny_hdr(packets: bytes) -> Path:
    """A one-row, 8-wide Radiance file whose scanline holds ``packets``."""
    path = Path(tempfile.mkdtemp()) / "tiny.hdr"
    path.write_bytes(b"#?RADIANCE\nFORMAT=32-bit_rle_rgbe\n\n-Y 1 +X 8\n\x02\x02\x00\x08" + packets)
    return path


grey = bytes([128 + 8, 128]) * 3 + bytes([128 + 8, 129])   # each channel one run of 8: 128 x 2^(129-136)
check(np.allclose(HC.read_hdr(tiny_hdr(grey)), 1.0), "a well-formed run-length row reads as its pixels")
for what, packets in (("a run past the row's end", bytes([128 + 9, 128]) * 4),
                      ("a packet of no pixels", bytes([0]) + grey),
                      ("a literal cut short by the file's end", bytes([8, 1, 2]))):
    try:
        HC.read_hdr(tiny_hdr(packets))
        refused = False
    except ValueError:
        refused = True
    check(refused, f"{what} is refused")

REPO = HERE.parent.parent
NOON = REPO / "MatterLibrary" / "hdris" / "QwantaniNoon_PureSky_v01.hdr"   # a bright noon sun


def decode_cube(dds: Path, tmp: Path) -> tuple[np.ndarray, int]:
    """The six top mips of a cube .dds, as the pinned encoder decodes them (to RGBA16F, its faces
    one after another, each with its mip chain), and the mip count it read."""
    out = tmp / "decoded.dds"
    subprocess.run(CT._encoder_prefix() + ["-fd", "ARGB_16F", "-noprogress", str(dds), str(out)],
                   check=True, capture_output=True)
    data = out.read_bytes()
    size, mips = struct.unpack("<I", data[12:16])[0], struct.unpack("<I", data[28:32])[0]
    texels = np.frombuffer(data[128:], "<f2").astype(np.float32).reshape(-1, 4)
    stride = sum(max(size >> m, 1) ** 2 for m in range(mips))
    return np.stack([texels[f * stride:f * stride + size * size, :3].reshape(size, size, 3)
                     for f in range(6)]), mips


def psnr_tonemapped(a: np.ndarray, b: np.ndarray) -> float:
    """PSNR (peak 1) of two HDR pictures after the same Reinhard tonemap, x / (1 + x)."""
    mse = np.mean((a / (1 + a) - b / (1 + b)) ** 2)
    return float("inf") if mse == 0 else 10 * np.log10(1 / mse)


print("== the built .dds is the cube Unreal builds from the .hdr ==")
if not shutil.which("magick"):
    print("  [SKIP] no ImageMagick: the .hdr cross-check and the .dds half are not run")
elif not CT._check_encoder():
    print("  [SKIP] no pinned compressor: the .dds half is not run")
else:
    with tempfile.TemporaryDirectory() as tmp:
        noon = HC.read_hdr(NOON)
        check(noon.shape == (2048, 4096, 3), f"the noon sky reads as 4096 x 2048 RGB (got {noon.shape})")
        raw = Path(tmp) / "magick.raw"
        subprocess.run(["magick", str(NOON), "-define", "quantum:format=floating-point", "-depth", "32",
                        f"RGB:{raw}"], check=True)
        theirs = np.fromfile(raw, "<f4").reshape(noon.shape)
        lit = theirs > 1e-3
        err = np.abs(noon[lit] - theirs[lit]) / theirs[lit]
        check(np.median(err) < 0.01, f"its pixels are ImageMagick's, within 1 % (median {np.median(err):.4f})")

        small = Path(tmp) / "QwantaniNoon_PureSky_v01.hdr"
        subprocess.run(["magick", str(NOON), "-resize", "1024x512!", str(small)], check=True)
        sky = HC.read_hdr(small)

        dds = Path(tmp) / "QwantaniNoon_v01.dds"
        HC.build_cube_dds(small, dds)
        problems = HC.validate_cube_dds(dds, 512)
        check(problems == [], f"the sibling is a 512 BC6H_UF16 cube with every mip ({problems})")
        faces, mips = decode_cube(dds, Path(tmp))
        check(faces.shape == (6, 512, 512, 3) and mips == 10,
              f"it decodes to six 512 faces and 10 mips (got {faces.shape}, {mips})")
        want = HC.equirect_to_cube(sky).astype(np.float32)
        for i, name in enumerate(("+X", "-X", "+Y", "-Y", "+Z", "-Z")):
            db = psnr_tonemapped(faces[i], want[i])
            check(db >= 40, f"face {name} is the runtime's, tonemapped PSNR {db:.1f} dB >= 40")

print("RESULT:", "ALL PASS" if not fails else f"{len(fails)} FAILED")
sys.exit(1 if fails else 0)
