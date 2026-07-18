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

Exit 0 iff every discovered source texture compressed to a byte-valid, correctly
formatted, mip-complete ``.dds``.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
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
    ("opacity", "BC4"),
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
    encoder through bash; exec a real ELF directly.
    """
    try:
        head = Path(COMPRESSONATOR).read_bytes()[:4]
    except OSError:
        return [COMPRESSONATOR]
    return [COMPRESSONATOR] if head[:4] == b"\x7fELF" else ["/bin/bash", COMPRESSONATOR]


def compress_one(src: Path, dst: Path, bc: str, miplevels: int, dry_run: bool = False) -> bool:
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = _encoder_prefix() + ["-fd", bc, "-miplevels", str(miplevels), str(src), str(dst)]
    if dry_run:
        print("  [DRY] " + " ".join(cmd))
        return True
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or not dst.exists():
        sys.stderr.write(res.stdout + res.stderr + "\n")
        print(f"  [FAIL] {src.name} -> {bc}: compressonatorcli rc={res.returncode}")
        return False
    return True


def compress_tree(src_root: Path, out_root: Path, only: str | None = None,
                  dry_run: bool = False) -> tuple[bool, list[dict]]:
    """Compress every source texture; return (ok, [record...])."""
    records: list[dict] = []
    ok = True
    for src in discover(src_root, only):
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
        good = compress_one(src, dst, bc, mips, dry_run)
        if good and not dry_run:
            print(f"  [OK]   {src.relative_to(src_root)}  role={role} fmt={bc} {w}x{h} mips={mips}")
        records.append({"src": str(src), "dst": str(dst), "role": role, "bc": bc,
                        "w": w, "h": h, "mips": mips, "ok": good})
        ok = ok and good
    return ok, records


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
        dxgi = None
        if pf_flags & _DDPF_FOURCC and fourcc == _FOURCC_DX10:
            dx10 = f.read(20)  # DDS_HEADER_DXT10
            if len(dx10) < 20:
                raise ValueError(f"{dst} truncated DX10 header")
            dxgi = struct.unpack("<I", dx10[:4])[0]
    return {"width": width, "height": height, "mipcount": mipcount,
            "fourcc": fourcc, "dxgi": dxgi}


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
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


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
    """Byte-identical re-run gate: compress the tree twice, sha256-compare every .dds."""
    if not _check_encoder():
        return 1
    src_root = Path(args.src_root)
    a = Path(tempfile.mkdtemp(prefix="mtc_det_a_"))
    b = Path(tempfile.mkdtemp(prefix="mtc_det_b_"))
    try:
        ok_a, recs = compress_tree(src_root, a, only=args.only)
        ok_b, _ = compress_tree(src_root, b, only=args.only)
        if not (ok_a and ok_b):
            print("RESULT: FAILURES (compression)")
            return 1
        all_ok = True
        for rec in recs:
            rel = Path(rec["dst"]).relative_to(a)
            ha, hb = sha256(a / rel), sha256(b / rel)
            same = ha == hb
            print(f"  [{'PASS' if same else 'FAIL'}] {rel}: {'byte-identical' if same else 'NON-DETERMINISTIC'}")
            all_ok = all_ok and same
        print("RESULT:", "ALL PASS" if all_ok else "FAILURES")
        return 0 if all_ok else 1
    finally:
        shutil.rmtree(a, ignore_errors=True)
        shutil.rmtree(b, ignore_errors=True)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="BCn texture compressor for Matter release staging.")
    ap.add_argument("--determinism", action="store_true",
                    help="byte-identical re-run gate (compress twice, sha256-compare)")
    ap.add_argument("--validate", action="store_true",
                    help="compress then structurally+semantically validate every .dds")
    ap.add_argument("--only", default=None, help="restrict to sources whose path contains this substring")
    ap.add_argument("--dry-run", action="store_true", help="print compressonatorcli commands, do not run")
    ap.add_argument("src_root", help="source texture tree root (e.g. MatterLibrary/textures)")
    ap.add_argument("out_root", nargs="?", default=None, help="output .dds root (omit for --determinism)")
    args = ap.parse_args(argv)

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
