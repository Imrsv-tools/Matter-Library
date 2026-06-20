#!/usr/bin/env python3
"""Library-level manifest (lockfile) validator (Phase 53).

Scope is the *library*, not a single material (R3 — distinct from validate_material.py).
Checks the release lockfile against Contract/Manifest.md:

    validate_manifest.py <matterlib-X.Y.lock.yaml> [--materials-root <dir>]

  * parses as YAML
  * release semver (MAJOR.MINOR.PATCH) — the library release axis
  * each material entry has id + version (vNN) + status (lifecycle)
  * the two version axes are well-formed and never conflated (release semver vs vNN)
  * each id resolves to an on-disk .mtlx: <materials-root>/<id>_<version>.mtlx

Exit 0 iff well-formed and every id resolves.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
VERSION_RE = re.compile(r"^v\d+$")
LIFECYCLE = {"draft", "candidate", "approved", "deprecated", "retired"}


def validate_manifest(path: Path, materials_root: Path) -> list:
    results = []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))

    release = data.get("release") if isinstance(data, dict) else None
    rel_ok = isinstance(release, str) and bool(SEMVER_RE.match(release))
    results.append(("release-semver", rel_ok,
                    f"release={release!r}" if rel_ok else f"release {release!r} not MAJOR.MINOR.PATCH"))

    materials = (data or {}).get("materials") or []
    results.append(("materials-present", bool(materials),
                    f"{len(materials)} material(s)" if materials else "no materials list"))

    for i, m in enumerate(materials):
        tag = f"material[{i}]"
        if not isinstance(m, dict):
            results.append((tag, False, f"not a mapping: {m!r}"))
            continue
        mid = m.get("id")
        ver = m.get("version")
        status = m.get("status")
        errs = []
        if not mid:
            errs.append("missing id")
        if not (isinstance(ver, str) and VERSION_RE.match(ver)):
            errs.append(f"version {ver!r} not 'vNN'")
        if status not in LIFECYCLE:
            errs.append(f"status {status!r} not in {sorted(LIFECYCLE)}")
        if mid and isinstance(ver, str):
            mtlx = materials_root / f"{mid}_{ver}.mtlx"
            if not mtlx.exists():
                errs.append(f"does not resolve: {mtlx}")
        results.append((f"{tag} {mid}", not errs, "ok" if not errs else "; ".join(errs)))

    return results


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate a Matter Library release manifest.")
    ap.add_argument("manifest")
    ap.add_argument("--materials-root", default=None,
                    help="default: <manifest>/../../MatterLibrary/materials")
    args = ap.parse_args(argv)

    path = Path(args.manifest)
    if args.materials_root:
        root = Path(args.materials_root)
    else:
        # library/releases/<file> -> repo root -> MatterLibrary/materials
        root = path.parent.parent.parent / "MatterLibrary" / "materials"

    print(f"== {path.name} (materials-root={root}) ==")
    try:
        results = validate_manifest(path, root)
    except Exception as exc:  # noqa: BLE001
        print(f"  ERROR: {exc}")
        return 1
    all_ok = True
    for check, ok, detail in results:
        print(f"  [{'PASS' if ok else 'FAIL'}] {check}: {detail}")
        all_ok = all_ok and ok
    print("RESULT:", "ALL PASS" if all_ok else "FAILURES")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
