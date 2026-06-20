#!/usr/bin/env python3
"""Runtime-catalog projector (Phase 56).

Validates the authored release lockfile (YAML) and projects it to the JSON
**runtime catalog** that Stage's `list_mtlx_library` reads — the prepared runtime
contract (Decision D). Stage never sees YAML; it consumes this JSON via nlohmann::json.

    project_runtime_catalog.py [<matterlib-X.Y.lock.yaml>] [--materials-root <dir>] [--out <file>]

Schema (Contract/RuntimeCatalog.md):
    {schema_version, release, materials[{id, display_name, domain, material_class,
                                         scale, version, status, payload_path}]}

Each material field is derived from the qualified `id` + `version`:
  * id              — the qualified Matter identity (Domain/Class path + name incl. sNN); the resolution key
  * display_name    — the qualified leaf name with the sNN scale tag dropped
  * domain/class    — the first two path segments of id
  * scale           — the sNN tag off the leaf (empty for an off-grammar system material)
  * payload_path    — `materials/<id>_<version>.mtlx` (bare `materials/<id>.mtlx` off-grammar), relative to the catalog file

Validation reuses validate_manifest.py (well-formedness + every id resolves on disk).
Deterministic: materials sorted by id, JSON keys sorted, trailing newline — a re-run is byte-identical.

Exit 0 iff the lockfile validates and projects.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "validators"))
import validate_manifest as vman  # noqa: E402

import yaml  # noqa: E402

SCHEMA_VERSION = 1
SCALE_RE = re.compile(r"_(s\d+)$")


def _default_materials_root(lockfile: Path) -> Path:
    # library/releases/<file> -> repo root -> MatterLibrary/materials
    return lockfile.parent.parent.parent / "MatterLibrary" / "materials"


def derive_entry(material: dict) -> dict:
    """Project one lockfile material entry to a runtime-catalog entry."""
    mid = material["id"]
    version = material["version"]
    status = material["status"]

    parts = mid.split("/")
    if len(parts) < 3:
        raise ValueError(f"id {mid!r} is not Domain/Class/Name (needs >=3 path segments)")
    domain = parts[0]
    material_class = parts[1]
    leaf = "/".join(parts[2:])

    m = SCALE_RE.search(leaf)
    if m:
        scale = m.group(1)
        display_name = leaf[: m.start()]
        filename = f"{mid}_{version}.mtlx"
    else:
        # Off-grammar system material (e.g. IMRSV_MissingMaterial): no sNN, bare-id resolve.
        scale = ""
        display_name = leaf
        filename = f"{mid}.mtlx"

    return {
        "id": mid,
        "display_name": display_name,
        "domain": domain,
        "material_class": material_class,
        "scale": scale,
        "version": version,
        "status": status,
        "payload_path": f"materials/{filename}",
    }


def build_catalog(lockfile: Path, materials_root: Path) -> dict:
    """Validate the lockfile and build the runtime-catalog dict. Raises ValueError on invalid input."""
    results = vman.validate_manifest(lockfile, materials_root)
    failures = [f"{check}: {detail}" for check, ok, detail in results if not ok]
    if failures:
        raise ValueError("manifest validation failed:\n  " + "\n  ".join(failures))

    data = yaml.safe_load(lockfile.read_text(encoding="utf-8")) or {}
    release = data.get("release")
    materials = data.get("materials") or []

    entries = [derive_entry(m) for m in materials]
    entries.sort(key=lambda e: e["id"])
    return {"schema_version": SCHEMA_VERSION, "release": release, "materials": entries}


def project_to_string(lockfile: Path, materials_root: Path) -> str:
    """Deterministic JSON projection (sorted keys, trailing newline)."""
    catalog = build_catalog(lockfile, materials_root)
    return json.dumps(catalog, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def _newest_lockfile() -> Path | None:
    releases = HERE.parent.parent / "library" / "releases"
    locks = sorted(releases.glob("*.lock.yaml")) if releases.exists() else []
    return locks[-1] if locks else None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Project a Matter Library lockfile to its JSON runtime catalog.")
    ap.add_argument("lockfile", nargs="?", default=None,
                    help="default: newest library/releases/*.lock.yaml")
    ap.add_argument("--materials-root", default=None,
                    help="default: <lockfile>/../../MatterLibrary/materials")
    ap.add_argument("--out", default=None,
                    help="default: <lockfile> with .lock.yaml -> .catalog.json")
    args = ap.parse_args(argv)

    lockfile = Path(args.lockfile) if args.lockfile else _newest_lockfile()
    if not lockfile or not lockfile.exists():
        print("ERROR: no lockfile (give a path or add library/releases/*.lock.yaml)", file=sys.stderr)
        return 1
    materials_root = Path(args.materials_root) if args.materials_root else _default_materials_root(lockfile)
    out = Path(args.out) if args.out else lockfile.with_name(lockfile.name.replace(".lock.yaml", ".catalog.json"))

    try:
        catalog_json = project_to_string(lockfile, materials_root)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    out.write_text(catalog_json, encoding="utf-8")
    print(f"projected {lockfile.name} -> {out.name} ({len(json.loads(catalog_json)['materials'])} materials)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
