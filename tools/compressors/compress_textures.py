#!/usr/bin/env python3
"""BCn texture compressor for Matter release staging (Phase 60sq2.4).

Compresses the authored source PNG texture tree into deterministic, mip-complete
BCn ``.dds`` artifacts, keyed by texture role. The ``.dds`` outputs are release
*derivatives* staged separately from the authored source tree — they are NEVER
written back into ``MatterLibrary/materials`` / ``MatterLibrary/textures`` (the
uncompressed source stays the open material source of truth and the deployed-path
RED fixture, by construction — Phase 60sq2 invariant #3).

Role is derived from the source filename suffix + directory
(basecolor / normal / metalness / roughness / opacity / ambient-occlusion /
emissive / overlay / mask). This drives ONLY the destination BC format. It is NOT
the runtime material-role binding: the runtime role comes from the ``.mtlx``
``<image>`` node name (e.g. ``metalness_tex``), and the source filename is opaque
to it. (Corrects the plan's "role detection keys on the filename suffix" framing:
no code parses the suffix to bind a runtime role — the recipe JSON key and the
``.mtlx`` node name own that. The suffix drives compression-format selection only.)

Role -> BC format (frozen, Phase 60sq2 §5 / plan 60sq2.4):

  base color / diffuse / emissive  -> BC7  (color; sRGB is a sampler decision at upload)
  overlay / mask (packed data)     -> BC7  (linear at upload)
  normal                           -> BC5  (16-bit source -> 8-bit BC5 precision drop,
                                            parity-gated by the codec A/B, 60sq2.8)
  metalness / roughness / opacity  -> BC4  (single channel)
  ambient occlusion                -> BC4  (single channel; latent — no AO map ships today)

All outputs carry the full mip chain (``-miplevels <full>``).

Usage:
  compress_textures.py <src-textures-root> <out-root> [--only <substr>] [--dry-run]
  compress_textures.py --determinism <src-textures-root>   # byte-identical re-run gate
  compress_textures.py --validate <src-textures-root> <out-root>  # structural+semantic
  compress_textures.py --determinism --fresh <src-textures-root>  # trust no earlier proof

The encode cache (2026-11-15): every encode is kept in ``library/dds_cache/`` (git-ignored) under
its source's bytes, the encoder version and the flags, and an unchanged texture is copied from
there instead of encoded again. The determinism gate proves each cache entry once (two encodes,
the same bytes) and trusts that proof afterwards; ``--fresh`` re-proves every texture with two new
encodes and also compares them with the cached one. Deleting the cache is always safe.

Exit 0 iff every discovered source texture compressed to a byte-valid, correctly
formatted, mip-complete ``.dds``.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

# Pinned encoder — Phase 60sq2 Discovery 4 (compressonatorcli V4.5.52, AMD 2024, MIT core).
COMPRESSONATOR = os.environ.get(
    "COMPRESSONATORCLI",
    str(Path.home() / ".local" / "bin" / "compressonatorcli"),
)
PINNED_VERSION = "V4.5.52"

CACHE_DIR = Path(__file__).resolve().parents[2] / "library" / "dds_cache"  # the encode cache, see above
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "releases"))
import atomic_write as AW  # noqa: E402  (a cache entry written whole)

SRC_EXT = ".png"
OUT_EXT = ".dds"

# Role token (in filename) -> (BC format, note). Order matters: longest / most
# specific tokens first so "ambient_occlusion" wins over a bare "occlusion", etc.
# Directory-based roles (masks/, overlays/) are handled separately below.
ROLE_TOKENS = [
    ("ambient_occlusion", "BC4"),
    ("basecolor", "BC7"),
    ("diffuse", "BC7"),
    ("emissive", "BC7"),
    ("metalness", "BC4"),
    ("metallic", "BC4"),   # legacy alias (Copper source PNG); canonicalized to metalness at freeze
    ("roughness", "BC4"),
    ("cavity", "BC4"),     # Phase22 22.2: the skin's cavity map (one channel, x specular_weight)
    ("scatter", "BC4"),    # Phase22 22.3: the skin's scatter map (one channel, x subsurface_radius)
    ("opacity", "BC4"),
    # Phase26 (RD-P26-5): a makeup piece's pictures. A fitted piece's coverage is one channel on the
    # atlas; a placed piece's stamp is RGBA (a colour multiplier and its coverage), so BC7
    ("coverage", "BC4"),
    ("stamp", "BC7"),
    ("normal", "BC5"),
    ("overlay", "BC7"),
    ("ao", "BC4"),
]

# Directory segment -> (BC format) when the filename carries no role token.
ROLE_DIRS = [
    ("masks", "BC7"),
    ("overlays", "BC7"),
]

# DXGI format code -> canonical BC name (DDS DX10 extended header, dxgiFormat).
# compressonatorcli emits a DX10-extended header for BC7, but LEGACY FourCC headers
# for BC4 (ATI1) / BC5 (ATI2) — both are valid; UE's FDDSFile parses both.
DXGI_TO_BC = {
    80: "BC4", 81: "BC4",   # BC4_UNORM / BC4_SNORM
    83: "BC5", 84: "BC5",   # BC5_UNORM / BC5_SNORM
    98: "BC7", 99: "BC7",   # BC7_UNORM / BC7_UNORM_SRGB
}
FOURCC_TO_BC = {
    b"ATI1": "BC4", b"BC4U": "BC4", b"BC4S": "BC4",
    b"ATI2": "BC5", b"BC5U": "BC5", b"BC5S": "BC5",
    b"DXT1": "BC1", b"DXT5": "BC3",
}


class ClassifyError(ValueError):
    pass


def classify(src: Path, src_root: Path) -> tuple[str, str]:
    """Return (role_token, bc_format) for a source texture, from suffix then dir."""
    stem = src.stem.lower()
    for token, bc in ROLE_TOKENS:
        # match the token as a whole underscore-delimited segment
        if token in stem.split("_") or ("_" + token + "_") in ("_" + stem + "_"):
            role = "metalness" if token in ("metalness", "metallic") else token
            return role, bc
    rel_parts = {p.lower() for p in src.relative_to(src_root).parts}
    for seg, bc in ROLE_DIRS:
        if seg in rel_parts:
            return seg.rstrip("s"), bc  # "masks" -> "mask", "overlays" -> "overlay"
    raise ClassifyError(f"cannot classify role for {src.relative_to(src_root)}")


def png_dims(src: Path) -> tuple[int, int]:
    with src.open("rb") as f:
        sig = f.read(8)
        if sig[:4] != b"\x89PNG":
            raise ValueError(f"{src} is not a PNG")
        f.read(4)  # IHDR length
        if f.read(4) != b"IHDR":
            raise ValueError(f"{src} missing IHDR")
        w, h = struct.unpack(">II", f.read(8))
    return w, h


def full_miplevels(w: int, h: int) -> int:
    """Full mip chain down to 1x1, capped at compressonator's 20-level ceiling."""
    n = max(w, h)
    levels = 1
    while n > 1:
        n >>= 1
        levels += 1
    return min(levels, 20)


def discover(src_root: Path, only: str | None = None) -> list[Path]:
    out = []
    for p in sorted(src_root.rglob("*" + SRC_EXT)):
        if only and only.lower() not in str(p).lower():
            continue
        out.append(p)
    return out


def _encoder_prefix() -> list[str]:
    """argv prefix to invoke the pinned encoder.

    compressonatorcli ships as a bash wrapper (sets LD_LIBRARY_PATH, exec's
    ``compressonatorcli-bin``) whose ``#!/bin/bash`` shebang is NOT on line 1
    (a leading blank line precedes it), so ``execve``/``posix_spawn`` fails
    ENOEXEC even though an interactive shell runs it. Route a text/script
    encoder through bash; exec a binary directly. Every binary format (ELF, a
    Windows PE, the native macOS Mach-O) has a non-text byte in its first four.
    """
    try:
        with open(COMPRESSONATOR, "rb") as f:
            head = f.read(4)
    except OSError:
        return [COMPRESSONATOR]
    script = all(32 <= b < 127 or b in b"\t\n\r" for b in head)
    return ["/bin/bash", COMPRESSONATOR] if script else [COMPRESSONATOR]


def _flags(bc: str, miplevels: int) -> list[str]:
    return ["-fd", bc, "-miplevels", str(miplevels)]


def _cmd(src: Path, dst: Path, bc: str, miplevels: int) -> list[str]:
    return _encoder_prefix() + _flags(bc, miplevels) + [str(src), str(dst)]


def _encode(src: Path, dst: Path, bc: str, miplevels: int) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    res = subprocess.run(_cmd(src, dst, bc, miplevels), capture_output=True, text=True)
    if res.returncode != 0 or not dst.exists():
        sys.stderr.write(res.stdout + res.stderr + "\n")
        print(f"  [FAIL] {src.name} -> {bc}: compressonatorcli rc={res.returncode}")
        return False
    return True


def _cache_key(src_sha: str, bc: str, miplevels: int) -> str:
    """The source's bytes (their sha256), the encoder version and the flags: a change to any is
    another key."""
    return hashlib.sha256("\0".join([src_sha, PINNED_VERSION] + _flags(bc, miplevels)).encode()).hexdigest()


def _cache_read(key: str) -> tuple[dict, bytes] | None:
    """key's cache entry and its .dds bytes, or None. The bytes are read once and checked against
    the entry's hash, so what a caller writes out is what was checked, even if another session
    replaces the entry meanwhile. An entry whose .dds does not have its recorded hash (damaged, or
    overwritten mid-read) is removed and reads as absent."""
    meta, dds = CACHE_DIR / f"{key}.json", CACHE_DIR / f"{key}.dds"
    if not meta.exists():
        return None
    try:
        entry = json.loads(meta.read_text(encoding="utf-8"))
        data = dds.read_bytes()
        if hashlib.sha256(data).hexdigest() == entry["dds_sha256"]:
            return entry, data
    except (OSError, ValueError, KeyError):
        pass
    meta.unlink(missing_ok=True)
    dds.unlink(missing_ok=True)
    return None


def _put(dst: Path, data: bytes) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(data)


def _cache_write(key: str, dds: Path, digest: str, proven: bool) -> None:
    """Keep dds (whose sha256 is digest) as key's entry, each file written whole; the .json goes
    last, so it names a whole .dds."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    AW.write_bytes(CACHE_DIR / f"{key}.dds", dds.read_bytes())
    AW.write_bytes(CACHE_DIR / f"{key}.json", json.dumps({"dds_sha256": digest, "proven": proven}).encode())


def compress_one(src: Path, dst: Path, bc: str, miplevels: int, dry_run: bool = False,
                 cache: bool = True) -> bool:
    """Encode src into dst, or copy an earlier encode of the same bytes, encoder version and flags
    from the encode cache; a new encode is kept there, unproven, unless src changed while it was
    encoded (another session editing it): that output is not the key's. cache=False encodes and
    keeps nothing."""
    if dry_run:
        print("  [DRY] " + " ".join(_cmd(src, dst, bc, miplevels)))
        return True
    if not cache:
        return _encode(src, dst, bc, miplevels)
    src_sha = sha256(src)
    key = _cache_key(src_sha, bc, miplevels)
    hit = _cache_read(key)
    if hit:
        _put(dst, hit[1])
        return True
    if not _encode(src, dst, bc, miplevels):
        return False
    if sha256(src) == src_sha:
        _cache_write(key, dst, sha256(dst), proven=False)
    return True


def prove_one(src: Path, dst: Path, bc: str, miplevels: int, fresh: bool = False) -> tuple[bool, str, bool]:
    """The determinism gate for one texture: encode src into dst and show that another encode of
    the same bytes gives the same bytes. Returns (ok, how, from the cache). A passed proof is kept
    in the encode cache and trusted later; an earlier unproven encode counts as the other run.
    fresh trusts no earlier proof: two new encodes, both also compared with the cached one. A
    source that changed while it was encoded FAILs, and nothing is kept: run again."""
    src_sha = sha256(src)
    key = _cache_key(src_sha, bc, miplevels)
    hit = _cache_read(key)
    entry = hit[0] if hit else None
    if entry and entry["proven"] and not fresh:
        _put(dst, hit[1])
        return True, "byte-identical (proven by an earlier run; from the encode cache)", True
    if not _encode(src, dst, bc, miplevels):
        return False, "the encoder failed", False
    got, again_sha = sha256(dst), None
    if not entry or fresh:  # else the earlier, unproven encode is the other run
        with tempfile.TemporaryDirectory(dir=dst.parent, prefix=".again-") as t:
            again = Path(t) / dst.name
            if not _encode(src, again, bc, miplevels):
                return False, "the encoder failed (second encode)", False
            again_sha = sha256(again)
    if sha256(src) != src_sha:
        return False, "the source changed while it was encoded (another session editing it?): run again", False
    if entry and entry["dds_sha256"] != got:
        return False, ("NON-DETERMINISTIC: differs from an earlier run's encode "
                       f"(if the encoder was reinstalled, delete {CACHE_DIR})"), False
    if again_sha is not None and again_sha != got:
        return False, "NON-DETERMINISTIC: two encodes differ", False
    _cache_write(key, dst, got, proven=True)
    return True, ("byte-identical (encoded twice)" if again_sha is not None
                  else "byte-identical with an earlier run's encode"), False


def compress_tree(src_root: Path, out_root: Path, only: str | None = None, dry_run: bool = False,
                  sources: list[Path] | None = None, prove: bool = False,
                  fresh: bool = False) -> tuple[bool, list[dict]]:
    """Compress every source texture (or exactly `sources`, e.g. one release's); return (ok, [record...]).
    prove: each texture passes the determinism gate too (prove_one, with fresh)."""
    records: list[dict] = []
    ok = True
    picked = discover(src_root, only) if sources is None else \
        [p for p in sources if not only or only.lower() in str(p).lower()]
    for src in picked:
        try:
            role, bc = classify(src, src_root)
        except ClassifyError as e:
            print(f"  [SKIP] {e}")
            ok = False
            continue
        w, h = png_dims(src)
        mips = full_miplevels(w, h)
        rel = src.relative_to(src_root).with_suffix(OUT_EXT)
        dst = out_root / rel
        good, how, cached = prove_one(src, dst, bc, mips, fresh) if prove else \
            (compress_one(src, dst, bc, mips, dry_run), "", False)
        if good and not dry_run:
            print(f"  [OK]   {src.relative_to(src_root)}  role={role} fmt={bc} {w}x{h} mips={mips}")
        records.append({"src": str(src), "dst": str(dst), "role": role, "bc": bc,
                        "w": w, "h": h, "mips": mips, "ok": good, "how": how, "cached": cached})
        ok = ok and good
    return ok, records


def prove_tree(src_root: Path, only: str | None = None, fresh: bool = False) -> bool:
    """The determinism gate over the tree (or its --only part), every output also validated, into
    a temp folder it removes; prints a line per texture and how many the encode cache held. Run by
    run_all.py's compression lane and by --determinism."""
    with tempfile.TemporaryDirectory(prefix="mtc_det_", ignore_cleanup_errors=True) as t:
        out = Path(t)
        ok, recs = compress_tree(src_root, out, only=only, prove=True, fresh=fresh)
        if not ok and all(rec["ok"] for rec in recs):
            print("  [FAIL] a texture could not be compressed (see above)")
        for rec in recs:
            good, detail = validate_output(rec) if rec["ok"] else (False, rec["how"])
            print(f"  [{'PASS' if good else 'FAIL'}] {Path(rec['dst']).relative_to(out)}: "
                  f"{rec['how'] if good else detail}")
            ok = ok and good
        cached = sum(rec["cached"] for rec in recs)
        print(f"  {len(recs)} textures: {cached} proven by an earlier run (the encode cache), "
              f"{len(recs) - cached} encoded now")
        return ok


# ---------------------------------------------------------------------------
# DDS header validation (structural + semantic)
# ---------------------------------------------------------------------------
_DDS_MAGIC = b"DDS "
_DDPF_FOURCC = 0x4
_FOURCC_DX10 = b"DX10"


def read_dds_header(dst: Path) -> dict:
    """Parse a DDS (optionally DX10-extended) header. Returns dims/mips/format."""
    with dst.open("rb") as f:
        if f.read(4) != _DDS_MAGIC:
            raise ValueError(f"{dst} not a DDS (bad magic)")
        hdr = f.read(124)
        if len(hdr) != 124:
            raise ValueError(f"{dst} truncated DDS header")
        # DDS_HEADER: size(0) flags(4) height(8) width(12) pitch(16) depth(20) mipcount(24)
        size, flags, height, width, pitch, depth, mipcount = struct.unpack("<7I", hdr[:28])
        # DDS_PIXELFORMAT begins at offset 72 within the 124-byte header
        pf = hdr[72:72 + 32]
        pf_size, pf_flags, fourcc = struct.unpack("<II4s", pf[:12])
        dxgi = misc = array_size = None
        if pf_flags & _DDPF_FOURCC and fourcc == _FOURCC_DX10:
            dx10 = f.read(20)  # DDS_HEADER_DXT10: dxgiFormat, dimension, miscFlag, arraySize, misc2
            if len(dx10) < 20:
                raise ValueError(f"{dst} truncated DX10 header")
            dxgi, _, misc, array_size = struct.unpack("<4I", dx10[:16])
    return {"width": width, "height": height, "mipcount": mipcount,
            "fourcc": fourcc, "dxgi": dxgi, "misc": misc, "array_size": array_size}


def validate_output(rec: dict) -> tuple[bool, str]:
    """Structural+semantic check of one compressed artifact against its source record."""
    dst = Path(rec["dst"])
    if not dst.exists():
        return False, "missing .dds"
    try:
        h = read_dds_header(dst)
    except ValueError as e:
        return False, f"corrupt: {e}"
    problems = []
    if h["width"] != rec["w"] or h["height"] != rec["h"]:
        problems.append(f"dims {h['width']}x{h['height']} != src {rec['w']}x{rec['h']}")
    if h["mipcount"] != rec["mips"]:
        problems.append(f"mipcount {h['mipcount']} != expected {rec['mips']}")
    if h["dxgi"] is not None:
        got_bc = DXGI_TO_BC.get(h["dxgi"])
    else:
        got_bc = FOURCC_TO_BC.get(h["fourcc"])
    if got_bc != rec["bc"]:
        problems.append(f"format {got_bc or h['fourcc']} != role format {rec['bc']}")
    return (not problems), ("ok" if not problems else "; ".join(problems))


def sha256(p: Path) -> str:
    with open(p, "rb") as f:  # in chunks, never the whole file in memory
        return hashlib.file_digest(f, "sha256").hexdigest()


# ---------------------------------------------------------------------------
# CLI + gates
# ---------------------------------------------------------------------------
def _check_encoder() -> bool:
    if not Path(COMPRESSONATOR).exists():
        print(f"RESULT: FAIL — compressonatorcli not found at {COMPRESSONATOR}")
        return False
    res = subprocess.run(_encoder_prefix(), capture_output=True, text=True)
    if PINNED_VERSION not in (res.stdout + res.stderr):
        print(f"RESULT: FAIL — compressonatorcli is not the pinned {PINNED_VERSION}")
        return False
    return True


def cmd_compress(args) -> int:
    if not args.dry_run and not _check_encoder():
        return 1
    ok, records = compress_tree(Path(args.src_root), Path(args.out_root),
                                only=args.only, dry_run=args.dry_run)
    print("RESULT:", "ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


def cmd_validate(args) -> int:
    ok, records = compress_tree(Path(args.src_root), Path(args.out_root), only=args.only)
    if not ok:
        print("RESULT: FAILURES (compression)")
        return 1
    all_ok = True
    for rec in records:
        good, detail = validate_output(rec)
        print(f"  [{'PASS' if good else 'FAIL'}] {Path(rec['dst']).name}: {detail}")
        all_ok = all_ok and good
    print("RESULT:", "ALL PASS" if all_ok else "FAILURES")
    return 0 if all_ok else 1


def cmd_determinism(args) -> int:
    if not _check_encoder():
        return 1
    ok = prove_tree(Path(args.src_root), only=args.only, fresh=args.fresh)
    print("RESULT:", "ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="BCn texture compressor for Matter release staging.")
    ap.add_argument("--determinism", action="store_true",
                    help="determinism gate: two encodes of each texture give the same bytes (a texture "
                         "proven before is copied from the encode cache)")
    ap.add_argument("--validate", action="store_true",
                    help="compress then structurally+semantically validate every .dds")
    ap.add_argument("--only", default=None, help="restrict to sources whose path contains this substring")
    ap.add_argument("--dry-run", action="store_true", help="print compressonatorcli commands, do not run")
    ap.add_argument("src_root", help="source texture tree root (e.g. MatterLibrary/textures)")
    ap.add_argument("out_root", nargs="?", default=None, help="output .dds root (omit for --determinism)")
    ap.add_argument("--fresh", action="store_true",
                    help="with --determinism: trust no earlier proof (two new encodes of every texture, "
                         "also compared with the encode cache)")
    args = ap.parse_args(argv)
    if args.fresh and not args.determinism:
        ap.error("--fresh goes with --determinism")
    # A SIGTERM (a stopped background run) unwinds as SystemExit, so the temp folders go too.
    signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(128 + signum))

    if args.determinism:
        return cmd_determinism(args)
    if args.validate:
        if not args.out_root:
            ap.error("--validate requires out_root")
        return cmd_validate(args)
    if not args.out_root:
        ap.error("out_root is required (or use --determinism)")
    return cmd_compress(args)


if __name__ == "__main__":
    raise SystemExit(main())
