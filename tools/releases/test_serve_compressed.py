#!/usr/bin/env python3
"""Units for serve_to_stage.py --compressed: the dev .dds are built aside and served beside their
PNGs through a folder of links, the checkout is never written, and the plain link comes back.

    uv run tools/releases/test_serve_compressed.py        exit 0 = PASS

The compressor is replaced by a stand-in that writes a marker file, so no encoder is needed.
"""
import os
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import serve_to_stage as S  # noqa: E402

fails = []


def check(cond, what):
    print(("  [PASS] " if cond else "  [FAIL] ") + what)
    if not cond:
        fails.append(what)


calls = []


def fake_compress(src, dst, src_root):
    calls.append(src.name)
    if "unnamed" in src.name:
        return "no role token"
    dst.write_text(f"dds of {src.name}")
    return None


def tree(root, files):
    for rel, text in files.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)


def listing(root):
    return sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if not p.is_dir())


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    src, staging, dev = tmp / "src", tmp / "staging", tmp / "dev"
    tree(src, {"base/Wood/Oak_basecolor.png": "png", "base/Wood/Oak_normal.png": "png",
               "base/Wood/notes.txt": "txt", "shared/unnamed.png": "png"})
    dev.mkdir()
    before = listing(src)

    print("== first compressed serve ==")
    line = S.serve_textures(dev, True, src, staging, fake_compress, encoder_ok=True)
    out = dev / "textures"
    check(out.is_dir() and not out.is_symlink(), "textures is a real folder")
    check(S.is_link_farm(out), "it holds only links")
    check(listing(out) == ["base/Wood/Oak_basecolor.dds", "base/Wood/Oak_basecolor.png",
                           "base/Wood/Oak_normal.dds", "base/Wood/Oak_normal.png",
                           "base/Wood/notes.txt", "shared/unnamed.png"],
          "every source file plus a .dds beside each compressible PNG")
    check((out / "base/Wood/Oak_basecolor.png").resolve() == (src / "base/Wood/Oak_basecolor.png").resolve(),
          "a PNG links to the checkout's file")
    check((out / "base/Wood/Oak_normal.dds").resolve() == (staging / "base/Wood/Oak_normal.dds").resolve(),
          "a .dds links to the staging tree")
    check(not (out / "shared/unnamed.dds").exists(), "a PNG the compressor refuses is served without one")
    check(listing(src) == before, "the checkout is not written")
    check("2 .dds served" in line and "1 without" in line, f"the serve says what it did: {line!r}")

    print("== second serve: only stale .dds are remade ==")
    calls.clear()
    time.sleep(0.02)
    os.utime(src / "base/Wood/Oak_normal.png")              # a regenerated picture
    (src / "base/Wood/Oak_basecolor.png").unlink()           # a dropped picture
    S.serve_textures(dev, True, src, staging, fake_compress, encoder_ok=True)
    check(sorted(calls) == ["Oak_normal.png", "unnamed.png"], f"only the newer PNG (and the refused one) recompress: {calls}")
    check(not (staging / "base/Wood/Oak_basecolor.dds").exists(), "a .dds whose PNG is gone is removed from staging")
    check(not (out / "base/Wood/Oak_basecolor.dds").exists() and not (out / "base/Wood/Oak_basecolor.png").exists(),
          "and from the served folder")
    check(not (dev / "textures.old").exists() and not (dev / "textures.building").exists(), "no swap leftovers")

    print("== no encoder: warn, serve the plain link ==")
    S.serve_textures(dev, True, src, staging, fake_compress, encoder_ok=False)
    check(out.is_symlink() and out.resolve() == src.resolve(), "the farm is replaced by the plain link")
    check(listing(src) == ["base/Wood/Oak_normal.png", "base/Wood/notes.txt", "shared/unnamed.png"],
          "the checkout survives the farm's removal")

    print("== back to compressed, then plain again ==")
    S.serve_textures(dev, True, src, staging, fake_compress, encoder_ok=True)
    check(S.is_link_farm(out), "a link is replaced by a farm")
    S.serve_textures(dev, False, src, staging, fake_compress)
    check(out.is_symlink(), "without --compressed the plain link comes back")

    print("== a real folder is never removed ==")
    out.unlink()
    tree(out, {"real.png": "authored"})
    try:
        S.serve_textures(dev, True, src, staging, fake_compress, encoder_ok=True)
        refused = False
    except SystemExit:
        refused = True
    check(refused and (out / "real.png").read_text() == "authored", "a folder holding a real file is refused, kept")

print("== a failed texture leaves no .dds, even when another one raises ==")


def failing_compress(src, dst, src_root):
    dst.write_text(f"half-made dds of {src.name}")     # the encoder wrote something...
    if "raises" in src.name.lower():
        raise ValueError(f"{src.name} is not a PNG")     # ...then a malformed PNG raised
    if "badcheck" in src.name.lower():
        return "format BC4 != role format BC5"          # ...or the release's check refused it
    return None


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    src, staging, dev = tmp / "src", tmp / "staging", tmp / "dev"
    tree(src, {"a/Good_basecolor.png": "png", "a/Badcheck_normal.png": "png", "a/Raises_roughness.png": "png"})
    dev.mkdir()
    line = S.serve_textures(dev, True, src, staging, failing_compress, encoder_ok=True)
    check(listing(staging) == ["a/Good_basecolor.dds"], f"only the good .dds is staged: {listing(staging)}")
    check(not (dev / "textures/a/Badcheck_normal.dds").exists() and not (dev / "textures/a/Raises_roughness.dds").exists(),
          "neither failed texture is served a .dds")
    check("1 .dds served" in line and "2 without" in line, f"the serve counts both misses: {line!r}")
    calls.clear()
    S.serve_textures(dev, True, src, staging, lambda s, d, r: (calls.append(s.name), failing_compress(s, d, r))[1],
                     encoder_ok=True)
    check(sorted(calls) == ["Badcheck_normal.png", "Raises_roughness.png"],
          f"the next serve retries both failures instead of keeping them: {calls}")

print("RESULT:", "PASS" if not fails else f"FAIL ({len(fails)})")
sys.exit(1 if fails else 0)
