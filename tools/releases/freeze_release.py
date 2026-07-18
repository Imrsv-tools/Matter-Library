#!/usr/bin/env python3
"""Complete-payload hash-lock for a Matter release (Phase 60sq2.3.3, RD-4).

RD-4: per-entry statuses are settled BEFORE the freeze; the freeze then hash-locks the COMPLETE
final payload — catalog + manifest + every referenced .mtlx + the shipped source textures + the
compressed .dds outputs (when present, post-60sq2.5). The external approval artifact (RD-1,
validate_approval.py) REFERENCES these hashes; it does not rewrite the payload, so the tested
candidate stays byte-identical to the approved release. CI re-runs this and asserts a match on
later builds.

Extends the check_determinism.py byte-identical-regen idea from a single .mtlx to the whole
payload. Reuses source_provenance.py's file_sha256 / canonical_listing / set_digest / is_lfs_pointer.
(.dds are excluded from source_provenance by construction — covered HERE.)

    freeze_release.py compute <version> [--repo-root <dir>] [--staging <dir>] [--out <file>]
    freeze_release.py verify  <record.json> [--repo-root <dir>] [--staging <dir>]

The record (deterministic — NO wall-clock field is hashed):
    { "release": "<version>",
      "payload_sha256": { "catalog", "manifest", "mtlx_set", "source_textures_set"[, "dds_set"] },
      "payload_digest": <sha256 over the canonical payload_sha256 listing>,
      "files": { <category>: [ {path, sha256, lfs_pointer?}, ... ] } }

`payload_sha256` is exactly what an approval artifact carries; `payload_digest` is the single
number that binds the release to its complete frozen payload.

Exit 0 iff compute succeeds / verify matches.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "validators"))
import source_provenance as sp  # noqa: E402

_MATTERLIB = Path("MatterLibrary")


def _rel(repo_root: Path, p: Path) -> str:
    return p.resolve().relative_to(repo_root.resolve()).as_posix()


def _file_entry(repo_root: Path, p: Path) -> dict:
    e = {"path": _rel(repo_root, p), "sha256": sp.file_sha256(p)}
    if sp.is_lfs_pointer(p):
        e["lfs_pointer"] = True  # a freeze over an un-materialized LFS stub is NOT a real freeze
    return e


def _payload_files(repo_root: Path, version: str, staging: Path | None) -> dict:
    """category -> sorted list[{path, sha256[, lfs_pointer]}] for the complete release payload."""
    releases = repo_root / "library" / "releases"
    catalog = releases / f"matterlib-{version}.catalog.json"
    manifest = releases / f"matterlib-{version}.lock.yaml"
    if not catalog.exists():
        raise FileNotFoundError(f"no catalog for release {version}: {catalog}")
    if not manifest.exists():
        raise FileNotFoundError(f"no manifest for release {version}: {manifest}")

    # .mtlx: exactly the payloads the catalog names (catalog-relative == MatterLibrary-relative).
    entries = json.loads(catalog.read_text(encoding="utf-8")).get("materials", [])
    mtlx = []
    for m in entries:
        rel = m.get("payload_path", "")
        if not rel:
            continue
        p = repo_root / _MATTERLIB / rel
        if not p.exists():
            raise FileNotFoundError(f"missing .mtlx payload for {m.get('id', '?')}: {p}")
        mtlx.append(p)

    # source textures: the whole shipped source texture set (PNG-only by construction).
    textures = sorted((repo_root / _MATTERLIB / "textures").rglob("*.png"))

    # .dds compressed outputs: only exist post-60sq2.5, in the staging tree — include IF present.
    dds: list[Path] = []
    if staging is not None and staging.exists():
        dds = sorted(staging.rglob("*.dds"))

    files = {
        "catalog": [_file_entry(repo_root, catalog)],
        "manifest": [_file_entry(repo_root, manifest)],
        "mtlx": [_file_entry(repo_root, p) for p in sorted(set(mtlx))],
        "source_textures": [_file_entry(repo_root, p) for p in textures],
    }
    if dds:
        files["dds"] = [_file_entry(repo_root, p) for p in dds]
    return files


def compute_freeze(repo_root: Path, version: str, staging: Path | None = None) -> dict:
    files = _payload_files(repo_root, version, staging)
    payload_sha256 = {
        "catalog": files["catalog"][0]["sha256"],
        "manifest": files["manifest"][0]["sha256"],
        "mtlx_set": sp.set_digest(files["mtlx"]),
        "source_textures_set": sp.set_digest(files["source_textures"]),
    }
    if "dds" in files:
        payload_sha256["dds_set"] = sp.set_digest(files["dds"])
    # payload_digest: one number over the canonical (sorted-key) payload_sha256 listing.
    listing = "".join(f"{k}  {payload_sha256[k]}\n" for k in sorted(payload_sha256))
    payload_digest = hashlib.sha256(listing.encode("utf-8")).hexdigest()
    return {
        "release": version,
        "payload_sha256": payload_sha256,
        "payload_digest": payload_digest,
        "files": files,
    }


def verify_freeze(repo_root: Path, record: dict, staging: Path | None = None) -> list[str]:
    """Recompute from disk and compare to a prior record. [] == matches."""
    version = record.get("release", "")
    if not version:
        return ["record has no `release`"]
    try:
        fresh = compute_freeze(repo_root, version, staging)
    except FileNotFoundError as exc:
        return [f"cannot recompute: {exc}"]
    errs: list[str] = []
    if fresh["payload_digest"] != record.get("payload_digest"):
        errs.append(f"payload_digest mismatch: recorded {record.get('payload_digest')!r} "
                    f"!= on-disk {fresh['payload_digest']!r}")
    rec_ps, fresh_ps = record.get("payload_sha256", {}), fresh["payload_sha256"]
    for k in sorted(set(rec_ps) | set(fresh_ps)):
        if rec_ps.get(k) != fresh_ps.get(k):
            errs.append(f"payload_sha256[{k}] mismatch: {rec_ps.get(k)!r} != {fresh_ps.get(k)!r}")
    return errs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Complete-payload hash-lock for a Matter release (RD-4).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("compute", help="compute + print (or write) the freeze record")
    c.add_argument("version")
    c.add_argument("--repo-root", type=Path, default=_HERE.parent.parent)
    c.add_argument("--staging", type=Path, default=None)
    c.add_argument("--out", type=Path, default=None)
    v = sub.add_parser("verify", help="recompute + assert a prior record matches")
    v.add_argument("record", type=Path)
    v.add_argument("--repo-root", type=Path, default=_HERE.parent.parent)
    v.add_argument("--staging", type=Path, default=None)
    args = ap.parse_args(argv)

    if args.cmd == "compute":
        rec = compute_freeze(args.repo_root.resolve(), args.version, args.staging)
        text = json.dumps(rec, indent=2, sort_keys=True) + "\n"
        if args.out:
            args.out.write_text(text, encoding="utf-8")
            print(f"froze release {args.version}: payload_digest {rec['payload_digest']} -> {args.out}")
        else:
            print(text, end="")
        lfs = [e["path"] for cat in rec["files"].values() for e in cat if e.get("lfs_pointer")]
        if lfs:
            print(f"WARNING: {len(lfs)} payload file(s) are un-materialized LFS pointers — "
                  f"freeze covers the pointer, not the pixels: {lfs[:3]}{' …' if len(lfs) > 3 else ''}",
                  file=sys.stderr)
        return 0

    record = json.loads(args.record.read_text(encoding="utf-8"))
    errs = verify_freeze(args.repo_root.resolve(), record, args.staging)
    for e in errs:
        print(f"  [FAIL] {e}")
    print("FREEZE:", "MATCH" if not errs else "MISMATCH")
    return 0 if not errs else 1


if __name__ == "__main__":
    raise SystemExit(main())
