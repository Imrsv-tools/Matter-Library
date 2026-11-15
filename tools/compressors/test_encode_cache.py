#!/usr/bin/env python3
"""Units for compress_textures.py's encode cache and its determinism gate (prove_one): a texture
encoded before is copied, not encoded again; a changed picture, another encoder version or a
damaged entry is encoded anew; two encodes that differ FAIL and leave nothing behind as proof;
--fresh encodes everything and compares it with the cache; a texture edited while it is encoded
is never kept; a copy from the cache is of the bytes it checked.

    uv run tools/compressors/test_encode_cache.py        exit 0 = PASS

Runs with a stand-in encoder (a shell script that copies its input and logs each run) and a cache
in a temp folder, so neither the pinned encoder nor library/dds_cache/ is touched.
"""
import json
import struct
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compress_textures as CT  # noqa: E402

fails = []


def check(cond, what):
    print(("  [PASS] " if cond else "  [FAIL] ") + what)
    if not cond:
        fails.append(what)


def png(path: Path, payload: bytes) -> Path:
    """Enough of a PNG for png_dims (a 4x4 IHDR), then payload so two pictures can differ."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + struct.pack(">I", 13) + b"IHDR"
                     + struct.pack(">II", 4, 4) + bytes(5) + payload)
    return path


with tempfile.TemporaryDirectory(prefix="encode_cache_test_") as tmp:
    tmp = Path(tmp)
    runs = tmp / "runs.log"
    steady = tmp / "steady.sh"  # called as: -fd <bc> -miplevels <n> <src> <dst>
    steady.write_text(f'echo run >> "{runs}"\ncp "$5" "$6"\n')
    wobbly = tmp / "wobbly.sh"  # a different .dds every run
    wobbly.write_text(f'echo run >> "{runs}"\ncp "$5" "$6"\necho $RANDOM$RANDOM >> "$6"\n')
    CT.COMPRESSONATOR = str(steady)
    CT.CACHE_DIR = tmp / "cache"
    src_root, out = tmp / "textures", tmp / "out"
    mips = CT.full_miplevels(4, 4)
    tex = png(src_root / "a" / "a_basecolor.png", b"one")

    def encodes(fn):
        """fn()'s result, and how many times the stand-in encoder ran during it."""
        before = len(runs.read_text().splitlines()) if runs.exists() else 0
        result = fn()
        return result, len(runs.read_text().splitlines()) - before

    def prove(only=None, fresh=False):
        return CT.compress_tree(src_root, out, only=only, prove=True, fresh=fresh)

    (ok, _), n = encodes(prove)
    check(ok and n == 2, f"a new texture is encoded twice and proven (encodes: {n})")
    metas = list(CT.CACHE_DIR.glob("*.json"))
    check(len(metas) == 1 and json.loads(metas[0].read_text())["proven"], "its proven encode is kept")

    (ok, recs), n = encodes(prove)
    check(ok and n == 0 and recs[0]["cached"], f"proven before: copied from the cache, not encoded (encodes: {n})")
    check((out / "a" / "a_basecolor.dds").read_bytes() == tex.read_bytes(), "the copy is the encoder's output")

    plain = tmp / "plain" / "a.dds"
    ok, n = encodes(lambda: CT.compress_one(tex, plain, "BC7", mips))
    check(ok and n == 0 and plain.read_bytes() == tex.read_bytes(),
          "compress_one (staging, the dev server) copies it too")

    png(tex, b"two")
    (ok, _), n = encodes(prove)
    check(ok and n == 2, f"a changed picture is encoded anew, twice (encodes: {n})")

    CT.PINNED_VERSION, pinned = "V0.0.0-test", CT.PINNED_VERSION
    (ok, _), n = encodes(prove)
    CT.PINNED_VERSION = pinned
    check(ok and n == 2, f"another encoder version is encoded anew (encodes: {n})")

    for dds in CT.CACHE_DIR.glob("*.dds"):
        dds.write_bytes(b"damaged")
    (ok, _), n = encodes(prove)
    check(ok and n == 2, f"a damaged entry is dropped and encoded anew (encodes: {n})")
    (ok, _), n = encodes(prove)
    check(ok and n == 0, f"... and the entry is whole again (encodes: {n})")

    cube = png(tmp / "cube" / "float.png", b"a sky")
    before = set(CT.CACHE_DIR.iterdir())
    ok, n = encodes(lambda: CT.compress_one(cube, tmp / "cube" / "bc6h.dds", "BC6H", mips, cache=False))
    check(ok and n == 1 and set(CT.CACHE_DIR.iterdir()) == before,
          f"cache=False (an HDRI's cube) encodes and keeps nothing (encodes: {n})")

    rough = png(src_root / "b" / "b_roughness.png", b"three")
    ok, n = encodes(lambda: CT.compress_one(rough, tmp / "plain" / "b.dds", "BC4", mips))
    check(ok and n == 1, f"compress_one encodes a new texture once, unproven (encodes: {n})")
    (ok, _), n = encodes(prove)
    check(ok and n == 1, f"the gate then encodes it once: the earlier encode is the other run (encodes: {n})")

    CT.COMPRESSONATOR = str(wobbly)
    normal = png(src_root / "c" / "c_normal.png", b"four")
    (ok, recs), _ = encodes(prove)
    bad = [r for r in recs if not r["ok"]]
    check(not ok and len(bad) == 1 and "NON-DETERMINISTIC" in bad[0]["how"],
          "an encoder whose two runs differ FAILs the gate")
    check(CT._cache_read(CT._cache_key(CT.sha256(normal), "BC5", mips)) is None, "... and nothing of it is kept")

    (ok, recs), n = encodes(lambda: prove(only="a_basecolor", fresh=True))
    check(not ok and "earlier run" in recs[0]["how"],
          "--fresh re-encodes a proven texture and FAILs when the encoder now gives other bytes")
    CT.COMPRESSONATOR = str(steady)
    (ok, _), n = encodes(lambda: prove(only="a_basecolor", fresh=True))
    check(ok and n == 2, f"--fresh with a steady encoder: encoded twice, proven again (encodes: {n})")
    ok, n = encodes(lambda: CT.compress_one(tex, plain, "BC7", mips))
    check(ok and n == 0, f"then staging copies that re-proven encode, no third encode (encodes: {n})")

    # Another session edits a texture while it is encoded: the output is not the old bytes' encode
    editor = tmp / "editor.sh"  # encodes what it reads, then the picture changes
    editor.write_text(f'echo run >> "{runs}"\ncp "$5" "$6"\necho edited >> "$5"\n')
    CT.COMPRESSONATOR = str(editor)
    edited = png(src_root / "d" / "d_roughness.png", b"five")
    before = set(CT.CACHE_DIR.iterdir())
    ok, n = encodes(lambda: CT.compress_one(edited, tmp / "plain" / "d.dds", "BC4", mips))
    check(ok and n == 1 and set(CT.CACHE_DIR.iterdir()) == before,
          f"a texture edited while it is encoded is not kept by compress_one (encodes: {n})")
    (ok, recs), _ = encodes(lambda: prove(only="d_roughness"))
    check(not ok and "changed while it was encoded" in recs[0]["how"] and set(CT.CACHE_DIR.iterdir()) == before,
          "... and the gate FAILs it (not as NON-DETERMINISTIC), keeping nothing")
    CT.COMPRESSONATOR = str(steady)

    # Another session replaces an entry between the cache's check and the copy
    real_read = CT._cache_read

    def read_then_replaced(key):
        hit = real_read(key)
        if hit:
            (CT.CACHE_DIR / f"{key}.dds").write_bytes(b"another session's bytes")
        return hit

    CT._cache_read = read_then_replaced
    swapped = tmp / "plain" / "swapped.dds"
    ok, n = encodes(lambda: CT.compress_one(tex, swapped, "BC7", mips))
    CT._cache_read = real_read
    check(ok and n == 0 and swapped.read_bytes() == tex.read_bytes(),
          "a copy from the cache is of the bytes it checked, whatever replaced the entry since")

    check(not list(CT.CACHE_DIR.glob(".*")), "no half-written file is left in the cache")
    check(not [p for p in out.rglob(".again-*")], "no second-encode folder is left beside the outputs")

print("RESULT:", "ALL PASS" if not fails else f"{len(fails)} FAILED")
sys.exit(1 if fails else 0)
