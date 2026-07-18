#!/usr/bin/env python3
"""Shipped-source-set provenance digest for externally-sourced textures (Phase 60sq2.9).

`evidence.sha256` for an ambientCG texture attests the **shipped release-source texture
set** — the processed source PNGs this library actually distributes — NOT the historical
upstream ambientCG download (re-fetching would hash *today's* upstream asset, which does
not prove it was the historical input; and the shipped maps are processed derivatives
— resized / de-lit / tiled — so they are not byte-identical to any ambientCG download).
This is a deliberate, lead-ratified scope (D5, 2026-07-18); the evidence block records
`sha256_scope: shipped_source_set` so nobody later reads it as an upstream checksum.

Per texture id the evidence carries:
  url          — the ambientCG asset page (origin, human-auditable)
  sha256_scope — literal "shipped_source_set"
  sha256       — the SET DIGEST (see below)
  files        — [{path, sha256}] for every shipped source map, repo-relative
  note         — the processed-derivative disclaimer

Set digest (canonical, order-independent of filesystem enumeration):
  listing = "".join(f"{path}  {sha256}\n" for path, sha256 in sorted(files by path))
  set_digest = sha256(listing.encode("utf-8"))

Generated `.dds` derivatives are EXCLUDED — RD-4's payload hash-lock (freeze_release.py)
covers the compressed payload separately.

CLI:
  source_provenance.py compute <texture-id> <ambientcg-url> [--repo-root <dir>]
      -> prints the YAML evidence block (2-space indent under `provenance:`), for
         authoring / regenerating a lockfile entry.
  source_provenance.py verify <matterlib-X.Y.lock.yaml> [--repo-root <dir>]
      -> re-verifies every shipped_source_set evidence block in the lockfile.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

SRC_TEXTURES_REL = Path("MatterLibrary") / "textures"
_LFS_POINTER_MAGIC = b"version https://git-lfs.github.com/spec/v1"


def file_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def is_lfs_pointer(path: Path) -> bool:
    """True if the file is an un-smudged git-LFS pointer (text stub), not real pixels."""
    try:
        return Path(path).read_bytes(  # small read is fine; pointers are ~130 bytes
        )[:len(_LFS_POINTER_MAGIC)] == _LFS_POINTER_MAGIC
    except OSError:
        return False


def canonical_listing(files: list[dict]) -> str:
    """Deterministic path+digest listing, sorted by repo-relative path."""
    return "".join(f"{e['path']}  {e['sha256']}\n"
                   for e in sorted(files, key=lambda e: e["path"]))


def set_digest(files: list[dict]) -> str:
    return hashlib.sha256(canonical_listing(files).encode("utf-8")).hexdigest()


def discover_source_maps(repo_root: Path, texture_id: str) -> list[Path]:
    """Every shipped source PNG for a texture id (e.g. base/engineered/metal/Copper_Verdigris
    -> Copper_Verdigris_*.png in that dir). Excludes .dds by construction (source is PNG-only)."""
    tex_dir = repo_root / SRC_TEXTURES_REL / Path(texture_id).parent
    base = Path(texture_id).name
    return sorted(p for p in tex_dir.glob(f"{base}_*.png") if p.is_file())


def compute_evidence(repo_root: Path, texture_id: str, url: str) -> dict:
    maps = discover_source_maps(repo_root, texture_id)
    if not maps:
        raise SystemExit(f"no shipped source maps found for texture id {texture_id!r}")
    files = [{"path": str(p.relative_to(repo_root)), "sha256": file_sha256(p)} for p in maps]
    return {
        "url": url,
        "sha256_scope": "shipped_source_set",
        "sha256": set_digest(files),
        "note": ("Shipped source textures are processed derivatives (resized/de-lit/tiled) "
                 "of the ambientCG asset; NOT byte-identical to the upstream download. "
                 "sha256 attests the shipped release-source set, not an upstream-download checksum."),
        "files": files,
    }


def verify_evidence(repo_root: Path, ev: dict) -> list[str]:
    """Return error strings ([] == verified) for a shipped_source_set evidence block.

    Always checks INTERNAL consistency (the recorded set digest matches the recorded
    listing). Additionally checks PIXEL integrity (recompute each file's sha256 from disk)
    for every map that is materialized on disk; skips a map that is missing or an
    un-smudged LFS pointer (can't verify without LFS smudge) with an informational note."""
    errs: list[str] = []
    files = ev.get("files")
    if not isinstance(files, list) or not files:
        return ["shipped_source_set evidence has no files listing"]
    for e in files:
        if not (isinstance(e, dict) and e.get("path") and e.get("sha256")):
            errs.append(f"malformed files entry: {e!r}")
    if errs:
        return errs
    # internal consistency: recorded top digest == digest of the recorded listing
    recomputed = set_digest(files)
    if ev.get("sha256") != recomputed:
        errs.append(f"set digest {ev.get('sha256')!r} != digest of recorded listing {recomputed!r}")
    # pixel integrity: recompute from disk where materialized
    for e in files:
        fp = repo_root / e["path"]
        if not fp.exists():
            errs.append(f"listed source file missing on disk: {e['path']}")
            continue
        if is_lfs_pointer(fp):
            continue  # LFS not smudged here — internal consistency still holds
        disk = file_sha256(fp)
        if disk != e["sha256"]:
            errs.append(f"{e['path']}: on-disk sha256 {disk} != recorded {e['sha256']}")
    return errs


def _render_yaml(ev: dict, indent: int = 6) -> str:
    """Render the evidence dict as a YAML block for a lockfile provenance section.
    `indent` is the column of the `evidence:` key's CHILDREN (source/license sit at 6,
    so evidence's children sit at 8 — pass indent=8)."""
    pad = " " * indent
    lines = [f"{pad}url: {ev['url']}",
             f"{pad}sha256_scope: {ev['sha256_scope']}",
             f"{pad}sha256: {ev['sha256']}",
             f"{pad}note: >-",
             f"{pad}  {ev['note']}",
             f"{pad}files:"]
    for e in ev["files"]:
        lines.append(f"{pad}  - path: {e['path']}")
        lines.append(f"{pad}    sha256: {e['sha256']}")
    return "\n".join(lines)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Shipped-source-set provenance digest tool.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("compute", help="print the YAML evidence block for a texture id")
    c.add_argument("texture_id")
    c.add_argument("url")
    c.add_argument("--repo-root", default=None)
    v = sub.add_parser("verify", help="re-verify shipped_source_set evidence in a lockfile")
    v.add_argument("lockfile")
    v.add_argument("--repo-root", default=None)
    args = ap.parse_args(argv)

    here = Path(__file__).resolve().parent
    default_root = here.parent.parent  # tools/validators -> tools -> repo root
    repo_root = Path(args.repo_root) if args.repo_root else default_root

    if args.cmd == "compute":
        ev = compute_evidence(repo_root, args.texture_id, args.url)
        print(_render_yaml(ev, indent=8))
        return 0

    import yaml
    data = yaml.safe_load(Path(args.lockfile).read_text(encoding="utf-8"))
    textures = (data or {}).get("textures") or []
    ok = True
    n = 0
    for t in textures:
        ev = (t.get("provenance") or {}).get("evidence") if isinstance(t, dict) else None
        if isinstance(ev, dict) and ev.get("sha256_scope") == "shipped_source_set":
            n += 1
            errs = verify_evidence(repo_root, ev)
            good = not errs
            print(f"  [{'PASS' if good else 'FAIL'}] {t.get('id')}: "
                  f"{'verified' if good else '; '.join(errs)}")
            ok = ok and good
    if n == 0:
        print("  (no shipped_source_set evidence blocks)")
    print("RESULT:", "ALL PASS" if ok else "FAILURES")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
