#!/usr/bin/env python3
"""Regenerate the deterministic negative .dds fixtures for the compressor gate (Phase 60sq2.4).

These are DELIBERATELY-CORRUPT .dds artifacts. They exist so the compressor's
structural+semantic validator (`compress_textures.validate_output` /
`read_dds_header`) has something it MUST reject — the RED half of the validation
gate (§14a: a gate that cannot fail is not a gate). No encoder is required to
check them, so the negative gate runs even on a box without compressonatorcli.

Each fixture pins ONE failure mode:
  bad_magic.dds        — first 4 bytes are not b"DDS "        -> read_dds_header raises
  truncated_header.dds — b"DDS " then a <124-byte header       -> read_dds_header raises
  truncated_dx10.dds   — valid 124-byte header flags DX10, but the 20-byte
                         DDS_HEADER_DXT10 is truncated         -> read_dds_header raises
  format_mismatch.dds  — a STRUCTURALLY-VALID legacy-FourCC BC4 (ATI1) header;
                         validate_output rejects it when the source record
                         expected BC7 (role<->format disagreement)

Run:  python3 make_negative_fixtures.py     # rewrites the four .dds in this dir
"""
from __future__ import annotations

import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent

_DDS_MAGIC = b"DDS "
_DDPF_FOURCC = 0x4


def _dds_header(width: int, height: int, mipcount: int, fourcc: bytes) -> bytes:
    """A minimal, structurally-valid 124-byte DDS_HEADER with a legacy FourCC pixelformat."""
    hdr = bytearray(124)
    # size flags height width pitch depth mipcount  (first 7 uint32)
    struct.pack_into("<7I", hdr, 0, 124, 0x21007, height, width, 0, 0, mipcount)
    # DDS_PIXELFORMAT at offset 72: size(32) flags(FOURCC) fourcc(4) ...
    struct.pack_into("<II4s", hdr, 72, 32, _DDPF_FOURCC, fourcc)
    return bytes(hdr)


def main() -> None:
    (HERE / "bad_magic.dds").write_bytes(b"XXXX" + b"\x00" * 200)

    (HERE / "truncated_header.dds").write_bytes(_DDS_MAGIC + b"\x00" * 50)

    # Valid 124-byte header that DECLARES a DX10 extension, then only 4 of the
    # required 20 DDS_HEADER_DXT10 bytes.
    (HERE / "truncated_dx10.dds").write_bytes(
        _DDS_MAGIC + _dds_header(4, 4, 1, b"DX10") + b"\x00" * 4
    )

    # Structurally valid legacy BC4 (ATI1). Semantically wrong only relative to a
    # record that expected BC7 — the semantic (role<->format) rejection path.
    (HERE / "format_mismatch.dds").write_bytes(
        _DDS_MAGIC + _dds_header(4, 4, 1, b"ATI1")
    )

    for f in sorted(HERE.glob("*.dds")):
        print(f"  wrote {f.name} ({f.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
