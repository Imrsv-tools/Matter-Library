#!/usr/bin/env python3
"""Validator orchestrator (Phase 53) — runs the full §6 automated gate set.

    run_all.py [--repo-root <dir>]

Runs, skipping with a note any surface not yet present:
  1. grammar fixtures   — fixtures/grammar_cases.json (must-pass / must-fail)
  2. per-material        — validate_material.py over MatterLibrary/materials/**.mtlx
  3. manifest            — validate_manifest.py over the newest library/releases/*.lock.yaml
  4. determinism         — check_determinism.py over tools/converters/recipes/*.json

Exit 0 iff every present surface passes.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "converters"))

import validate_material as vm        # noqa: E402
import validate_manifest as vman      # noqa: E402
from assemble_mtlx import assemble, MaterialSpec  # noqa: E402
import project_runtime_catalog as prc  # noqa: E402
import check_fixture_sync as cfs       # noqa: E402


def run_grammar_fixtures() -> bool:
    cases = json.loads((HERE / "fixtures" / "grammar_cases.json").read_text(encoding="utf-8"))
    ok = True
    print("== grammar fixtures ==")
    for name in cases["must_pass"]:
        errs = vm.check_grammar(name)
        good = not errs
        print(f"  [{'PASS' if good else 'FAIL'}] must-pass {name}: {'ok' if good else errs}")
        ok = ok and good
    for name in cases["must_fail"]:
        errs = vm.check_grammar(name)
        good = bool(errs)
        print(f"  [{'PASS' if good else 'FAIL'}] must-fail {name}: {'rejected' if good else 'WRONGLY ACCEPTED'}")
        ok = ok and good
    return ok


def run_materials(root: Path) -> bool:
    materials = sorted((root / "MatterLibrary" / "materials").rglob("*.mtlx"))
    if not materials:
        print("== per-material == (skip: no .mtlx under MatterLibrary/materials)")
        return True
    print("== per-material ==")
    rc = vm.main([str(p) for p in materials])
    return rc == 0


def run_manifest(root: Path) -> bool:
    releases = sorted((root / "library" / "releases").glob("*.lock.yaml")) \
        if (root / "library" / "releases").exists() else []
    if not releases:
        print("== manifest == (skip: no library/releases/*.lock.yaml)")
        return True
    print("== manifest ==")
    rc = vman.main([str(releases[-1])])
    return rc == 0


def run_determinism(root: Path) -> bool:
    recipes = sorted((root / "tools" / "converters" / "recipes").glob("*.json")) \
        if (root / "tools" / "converters" / "recipes").exists() else []
    if not recipes:
        print("== determinism == (skip: no tools/converters/recipes/*.json)")
        return True
    print("== determinism ==")
    ok = True
    for r in recipes:
        spec = MaterialSpec.from_dict(json.loads(r.read_text(encoding="utf-8")))
        stable = assemble(spec) == assemble(spec)
        print(f"  [{'PASS' if stable else 'FAIL'}] {spec.name}: {'byte-stable' if stable else 'NON-DETERMINISTIC'}")
        ok = ok and stable
    return ok


def run_catalog_freshness(root: Path) -> bool:
    """Phase 56: the committed runtime catalog is byte-current with — and deterministic
    from — the authored lockfile. Re-project and diff: a drift between the YAML lockfile
    and the committed .catalog.json (or a non-deterministic projector) fails here, so the
    two can't independently 'validate' while out of sync."""
    releases = root / "library" / "releases"
    locks = sorted(releases.glob("*.lock.yaml")) if releases.exists() else []
    if not locks:
        print("== catalog freshness == (skip: no library/releases/*.lock.yaml)")
        return True
    print("== catalog freshness ==")
    ok = True
    materials_root = root / "MatterLibrary" / "materials"
    for lock in locks:
        catalog = lock.with_name(lock.name.replace(".lock.yaml", ".catalog.json"))
        try:
            projected = prc.project_to_string(lock, materials_root)
        except Exception as exc:  # noqa: BLE001
            print(f"  [FAIL] {lock.name}: projection error: {exc}")
            ok = False
            continue
        if not catalog.exists():
            print(f"  [FAIL] {lock.name}: committed {catalog.name} missing (run project_runtime_catalog.py)")
            ok = False
            continue
        committed = catalog.read_text(encoding="utf-8")
        # determinism: a second projection is byte-identical to the first
        deterministic = (projected == prc.project_to_string(lock, materials_root))
        fresh = (committed == projected)
        good = deterministic and fresh
        detail = "byte-current + deterministic" if good else (
            ("NON-DETERMINISTIC; " if not deterministic else "") +
            ("DRIFTED from lockfile" if not fresh else ""))
        print(f"  [{'PASS' if good else 'FAIL'}] {catalog.name}: {detail}")
        ok = ok and good
    return ok


def run_catalog_validation(root: Path) -> bool:
    """Phase 56: the projector REJECTS a malformed / dangling-id manifest (validation, not a
    silent empty projection). Drives the negative fixture through project_to_string and asserts
    it raises."""
    fixture = HERE / "fixtures" / "dangling_manifest.lock.yaml"
    if not fixture.exists():
        print("== catalog validation == (skip: no dangling_manifest fixture)")
        return True
    print("== catalog validation ==")
    materials_root = root / "MatterLibrary" / "materials"
    try:
        prc.project_to_string(fixture, materials_root)
        print(f"  [FAIL] {fixture.name}: WRONGLY ACCEPTED a dangling id")
        return False
    except Exception:  # noqa: BLE001
        print(f"  [PASS] {fixture.name}: rejected (dangling id)")
        return True


def run_provenance_gate(root: Path) -> bool:
    """Phase 60: the shipped-pixel no-ship gate REJECTS a promoted texture without provenance
    and a promoted material binding an under-promoted texture (validation, not silent pass).
    Drives the RED fixtures through validate_manifest and asserts each FAILS for its reason."""
    fixtures = [
        ("provenance_missing.lock.yaml", "promoted texture missing provenance"),
        ("coverage_underpromoted.lock.yaml", "promoted material binds under-promoted texture"),
    ]
    materials_root = root / "MatterLibrary" / "materials"
    present = [(HERE / "fixtures" / f, why) for f, why in fixtures if (HERE / "fixtures" / f).exists()]
    if not present:
        print("== provenance gate == (skip: no provenance RED fixtures)")
        return True
    print("== provenance gate ==")
    ok = True
    for fixture, why in present:
        results = vman.validate_manifest(fixture, materials_root)
        rejected = any(not good for _, good, _ in results)
        print(f"  [{'PASS' if rejected else 'FAIL'}] {fixture.name}: "
              f"{'rejected (' + why + ')' if rejected else 'WRONGLY ACCEPTED — gate is tautological'}")
        ok = ok and rejected
    return ok


def run_no_projection_guard(root: Path) -> bool:
    """Phase 60: provenance/license/evidence and per-texture status are authoring/promotion
    metadata and must NEVER reach the runtime catalog (RuntimeCatalog 'not v1'; no runtime
    consumer). Projects every lockfile and asserts none of those tokens appear in the JSON.
    A regression that starts projecting provenance fails here."""
    releases = root / "library" / "releases"
    locks = sorted(releases.glob("*.lock.yaml")) if releases.exists() else []
    if not locks:
        print("== no-projection guard == (skip: no lockfiles)")
        return True
    print("== no-projection guard ==")
    materials_root = root / "MatterLibrary" / "materials"
    banned = ("provenance", "evidence", "license")
    ok = True
    for lock in locks:
        try:
            projected = prc.project_to_string(lock, materials_root)
        except Exception as exc:  # noqa: BLE001
            print(f"  [FAIL] {lock.name}: projection error: {exc}")
            ok = False
            continue
        leaked = [tok for tok in banned if tok in projected]
        good = not leaked
        print(f"  [{'PASS' if good else 'FAIL'}] {lock.name}: "
              f"{'no promotion metadata projected' if good else 'LEAKED ' + ', '.join(leaked)}")
        ok = ok and good
    return ok


def run_fixture_sync(root: Path) -> bool:
    """Phase 58.5: the Stage fixture copy of the runtime catalog (+ payloads) is byte-current
    with the Matter-Library projected catalog — the cross-repo half Phase 56 left open
    (`run_catalog_freshness` covers only lockfile -> projected, within this repo)."""
    return cfs.check_fixture_sync(root, cfs.default_fixture_root(root))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Run the full Phase-53 validator gate set.")
    ap.add_argument("--repo-root", default=str(HERE.parent.parent))
    args = ap.parse_args(argv)
    root = Path(args.repo_root)

    results = {
        "grammar": run_grammar_fixtures(),
        "materials": run_materials(root),
        "manifest": run_manifest(root),
        "determinism": run_determinism(root),
        "catalog_freshness": run_catalog_freshness(root),
        "catalog_validation": run_catalog_validation(root),
        "provenance_gate": run_provenance_gate(root),
        "no_projection_guard": run_no_projection_guard(root),
        "fixture_sync": run_fixture_sync(root),
    }
    print("\n=== SUMMARY ===")
    for k, v in results.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    all_ok = all(results.values())
    print("OVERALL:", "ALL PASS" if all_ok else "FAILURES")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
