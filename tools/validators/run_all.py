#!/usr/bin/env python3
"""Validator orchestrator (Phase 53) — runs the full §6 automated gate set.

    run_all.py [--repo-root <dir>]

Runs, skipping with a note any surface not yet present:
  1. grammar fixtures        — fixtures/grammar_cases.json (must-pass / must-fail)
  2. per-material            — validate_material.py over MatterLibrary/materials/**.mtlx
  3. manifest                — validate_manifest.py over the newest library/releases/*.lock.yaml
  4. determinism             — recipe .mtlx assembly byte-stability
  5. catalog freshness/valid — projected runtime catalog is byte-current + rejects dangling ids
  6. provenance / projection — promotion-metadata gates + no-runtime-projection guard
  7. fixture sync            — Stage fixture catalog + payloads byte-current (cross-repo)
  8. compression negative    — the compressed-output validator REJECTS corrupt/mismatched .dds
  9. compression             — source textures compress to deterministic, valid BCn .dds
                               (encoder-gated: skips if compressonatorcli is absent)
 10. approval gate           — the external release-level approval artifact is well-formed +
                               references the frozen-payload hashes (positive + shallow-negative)
 11. freeze lock             — the complete-payload hash-lock is deterministic + tamper-detecting
                               (RD-4: catalog/manifest/.mtlx/textures[/.dds])

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
sys.path.insert(0, str(HERE.parent / "compressors"))
sys.path.insert(0, str(HERE.parent / "releases"))

import validate_material as vm        # noqa: E402
import validate_manifest as vman      # noqa: E402
from assemble_mtlx import assemble, MaterialSpec  # noqa: E402
import project_runtime_catalog as prc  # noqa: E402
import check_fixture_sync as cfs       # noqa: E402
import compress_textures as ct        # noqa: E402
import validate_approval as va        # noqa: E402
import freeze_release as fr           # noqa: E402


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
        ("approved_rank_shallow_evidence.lock.yaml",
         "approved ambientCG texture with shallow (doc-path) evidence, not {url, sha256}"),
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


def run_compression_negative(root: Path) -> bool:
    """Phase 60sq2.4: the compressed-output validator REJECTS corrupt/mismatched .dds.

    Drives the deliberately-corrupt negative fixtures through
    compress_textures.read_dds_header / validate_output and asserts each is
    rejected for its intended reason — the RED half of the compression validation
    gate (§14a). Needs NO encoder, so it always runs."""
    fxdir = Path(ct.__file__).resolve().parent / "fixtures"
    structural = ["bad_magic.dds", "truncated_header.dds", "truncated_dx10.dds"]
    present = [f for f in structural if (fxdir / f).exists()]
    mismatch = fxdir / "format_mismatch.dds"
    if not present and not mismatch.exists():
        print("== compression negative == (skip: no negative .dds fixtures)")
        return True
    print("== compression negative ==")
    ok = True
    for name in present:
        try:
            ct.read_dds_header(fxdir / name)
            print(f"  [FAIL] {name}: WRONGLY PARSED a corrupt .dds")
            ok = False
        except ValueError:
            print(f"  [PASS] {name}: rejected (corrupt structure)")
    if mismatch.exists():
        # A structurally-valid BC4 (ATI1) .dds fails when the record expected BC7.
        rec = {"dst": str(mismatch), "w": 4, "h": 4, "mips": 1, "bc": "BC7"}
        good, detail = ct.validate_output(rec)
        rejected = not good
        print(f"  [{'PASS' if rejected else 'FAIL'}] format_mismatch.dds: "
              f"{'rejected (' + detail + ')' if rejected else 'WRONGLY ACCEPTED a role<->format mismatch'}")
        ok = ok and rejected
    return ok


def run_compression(root: Path) -> bool:
    """Phase 60sq2.4: the source texture tree compresses to deterministic, structurally
    valid, mip-complete BCn .dds. Compresses the tree TWICE, validates every output, and
    sha256-compares the two runs (byte-identical determinism gate).

    Encoder-gated: skips with a note when compressonatorcli is absent (CI without the
    pinned encoder) — mirrors run_all's skip-if-surface-absent policy. On the dev box the
    encoder is present so the full sweep (~12 s over 30 textures) runs."""
    src_root = root / "MatterLibrary" / "textures"
    if not src_root.exists():
        print("== compression == (skip: no MatterLibrary/textures)")
        return True
    if not Path(ct.COMPRESSONATOR).exists() or not ct._check_encoder():
        print(f"== compression == (skip: pinned encoder {ct.PINNED_VERSION} absent — "
              f"run tools/compressors/compress_textures.py --determinism for the full sweep)")
        return True
    print("== compression ==")
    import tempfile as _tf
    a = Path(_tf.mkdtemp(prefix="mtc_run_a_"))
    b = Path(_tf.mkdtemp(prefix="mtc_run_b_"))
    try:
        ok_a, recs = ct.compress_tree(src_root, a)
        ok_b, _ = ct.compress_tree(src_root, b)
        if not (ok_a and ok_b):
            print("  [FAIL] compression errored (see above)")
            return False
        ok = True
        for rec in recs:
            good, detail = ct.validate_output(rec)
            rel = Path(rec["dst"]).relative_to(a)
            same = ct.sha256(a / rel) == ct.sha256(b / rel)
            good_all = good and same
            reason = detail if not good else ("byte-identical" if same else "NON-DETERMINISTIC")
            print(f"  [{'PASS' if good_all else 'FAIL'}] {rel}: {reason}")
            ok = ok and good_all
        return ok
    finally:
        import shutil as _sh
        _sh.rmtree(a, ignore_errors=True)
        _sh.rmtree(b, ignore_errors=True)


def run_approval_gate(root: Path) -> bool:
    """Phase 60sq2.3.2 (RD-1): the external release-level approval artifact is well-formed and
    references the frozen-payload hashes.

    A validator only CHECKS; the artifact is CREATED by the terminal promotion (promote_release.py,
    60sq2.12), so no real approval exists pre-promotion and the real-surface check skips-if-absent.
    A POSITIVE fixture proves the validator ACCEPTS a well-formed approval; the SHALLOW negative
    fixture (empty payload_sha256 — a promotion that never actually froze) proves it REJECTS, the
    RED half that keeps the gate non-tautological (§14a)."""
    fxdir = HERE.parent / "releases" / "fixtures"
    releases = root / "library" / "releases"
    real = sorted(releases.glob("*.approval.json")) if releases.exists() else []
    valid_fx = fxdir / "approval_valid.approval.json"
    shallow_fx = fxdir / "approval_shallow.approval.json"
    if not real and not valid_fx.exists() and not shallow_fx.exists():
        print("== approval gate == (skip: no approval artifacts or fixtures)")
        return True
    print("== approval gate ==")
    ok = True
    for ap in real:  # any real approval MUST validate clean
        errs = [d for _, good, d in va.validate_approval(ap, releases) if not good]
        print(f"  [{'PASS' if not errs else 'FAIL'}] {ap.name}: {'valid' if not errs else '; '.join(errs)}")
        ok = ok and not errs
    if valid_fx.exists():  # the positive fixture MUST validate clean
        errs = [d for _, good, d in va.validate_approval(valid_fx, None) if not good]
        print(f"  [{'PASS' if not errs else 'FAIL'}] {valid_fx.name}: {'valid' if not errs else '; '.join(errs)}")
        ok = ok and not errs
    if shallow_fx.exists():  # the negative fixture MUST be rejected (else the gate is tautological)
        rejected = any(not good for _, good, _ in va.validate_approval(shallow_fx, None))
        print(f"  [{'PASS' if rejected else 'FAIL'}] {shallow_fx.name}: "
              f"{'rejected (shallow approval)' if rejected else 'WRONGLY ACCEPTED — gate is tautological'}")
        ok = ok and rejected
    return ok


def run_freeze_lock(root: Path) -> bool:
    """Phase 60sq2.3.3 (RD-4): the complete-payload hash-lock is deterministic, self-consistent,
    and verify() catches tampering.

    Freezes the newest release, re-freezes (byte-identical payload_digest), self-verifies against
    the on-disk payload, and flips one recorded hash to prove verify() REJECTS — the RED half that
    keeps the hash-lock non-tautological (§14a). Skips if no release catalog is present."""
    releases = root / "library" / "releases"
    catalogs = sorted(releases.glob("matterlib-*.catalog.json"), key=lambda p: p.name)
    if not catalogs:
        print("== freeze lock == (skip: no release catalog)")
        return True
    version = catalogs[-1].name[len("matterlib-"):-len(".catalog.json")]  # newest, e.g. 0.1.0
    print("== freeze lock ==")
    try:
        rec = fr.compute_freeze(root, version)
        rec2 = fr.compute_freeze(root, version)
    except Exception as exc:  # noqa: BLE001
        print(f"  [FAIL] {version}: compute error: {exc}")
        return False
    ok = True
    det = rec["payload_digest"] == rec2["payload_digest"]
    print(f"  [{'PASS' if det else 'FAIL'}] {version} determinism: "
          f"{'byte-identical payload_digest' if det else 'NON-DETERMINISTIC'}")
    ok = ok and det
    clean = fr.verify_freeze(root, rec)
    print(f"  [{'PASS' if not clean else 'FAIL'}] {version} self-verify: "
          f"{'matches on-disk payload' if not clean else '; '.join(clean)}")
    ok = ok and not clean
    import copy
    tampered = copy.deepcopy(rec)
    tampered["payload_sha256"]["catalog"] = "f" * 64  # not the real catalog hash
    rejected = bool(fr.verify_freeze(root, tampered))
    print(f"  [{'PASS' if rejected else 'FAIL'}] {version} tamper-detection: "
          f"{'a mutated payload hash is rejected' if rejected else 'WRONGLY ACCEPTED — hash-lock is tautological'}")
    ok = ok and rejected
    return ok


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
        "compression_negative": run_compression_negative(root),
        "compression": run_compression(root),
        "approval_gate": run_approval_gate(root),
        "freeze_lock": run_freeze_lock(root),
    }
    print("\n=== SUMMARY ===")
    for k, v in results.items():
        print(f"  {k}: {'PASS' if v else 'FAIL'}")
    all_ok = all(results.values())
    print("OVERALL:", "ALL PASS" if all_ok else "FAILURES")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
