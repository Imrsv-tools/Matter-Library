#!/usr/bin/env python3
"""Cross-repo catalog-equality gate (Phase 58.5 — closes the Phase-56 gap).

The Stage runtime reads a *copy* of the projected runtime catalog (+ its material
payloads) from its fixture tree:

  IMRSV_Stage/_testing/test_assets/shared/MatterLibrary/

That copy is maintained by hand (Phase 56 left the fixture transitional), so it can
drift from the Matter-Library projected catalog. Phase 56's `run_catalog_freshness`
proves the *projected* catalog is byte-current with the authored lockfile; this gate
proves the *Stage fixture copy* is byte-current with the projected catalog — the
cross-repo half Phase 56 left open.

    check_fixture_sync.py [--projected <catalog.json> ...] [--fixture-root <dir>]

Asserts, per release catalog:
  1. fixture catalog JSON == projected catalog JSON (byte-equal)
  2. every catalog entry's payload_path resolves to a real file under the fixture root
  3. every payload's CONTENT is byte-equal to the authored .mtlx in Matter-Library  <-- 71.12 (F6)

⭐ WHY (3) EXISTS — it was missing, and it bit, live, at the 71.12 smoke.

This gate used to check only that a payload FILE EXISTED, never what was IN it. Its name
promised more than it checked. That matters more than it sounds, because of how the runtime
actually resolves materials:

    deploy-to-studio.sh rsyncs THE FIXTURE MIRROR's materials/ into _build/runtime/, and
    overlays ONLY the TEXTURES from the Matter-Library repo.

So the deployed daemon reads the FIXTURE's .mtlx, not Matter-Library's. A fix authored in
Matter-Library that is not mirrored NEVER REACHES THE APP.

At the 71.12 sitting, Diamond was fixed in Matter-Library (transmission 1.0 -> 0.95). The
mirror still held 1.0. The deployed runtime therefore still served 1.0 -- AND THIS GATE PASSED,
because the catalog had not changed and the payload file still existed. Had that not been caught
by hand, the app would have rendered Diamond identically broken, the lead would have read it as
"the fix didn't work", and a human-driven eyes-on cycle would have been burned chasing a fix
that was never actually shipped.

A stale payload is now a FAIL.

Exit 0 iff every present surface passes. Skips with a note if the fixture root is
absent (e.g. Matter-Library checked out standalone, without the platform monorepo).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Matter-Library repo root: tools/validators/ -> tools/ -> repo root.
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
# Stage fixture tree, relative to the platform superrepo layout (Matter-Library is a
# sibling of IMRSV_Studio under IMRSV_Platform). Overridable with --fixture-root.
STAGE_FIXTURE_REL = Path(
    "IMRSV_Studio/Plugins/IMRSVStagePlugin/Services/IMRSV_Stage"
    "/_testing/test_assets/shared/MatterLibrary"
)


def default_fixture_root(repo_root: Path = REPO_ROOT) -> Path:
    return (repo_root.parent / STAGE_FIXTURE_REL).resolve()


def _projected_catalogs(repo_root: Path) -> list[Path]:
    releases = repo_root / "library" / "releases"
    return sorted(releases.glob("*.catalog.json")) if releases.exists() else []


def check_release(projected: Path, fixture_root: Path, source_root: Path) -> list[str]:
    """Return a list of error strings ([] == in sync) for one release catalog."""
    errs: list[str] = []
    fixture_catalog = fixture_root / projected.name
    if not fixture_catalog.exists():
        return [f"fixture copy missing: {fixture_catalog}"]

    projected_text = projected.read_text(encoding="utf-8")
    fixture_text = fixture_catalog.read_text(encoding="utf-8")
    if fixture_text != projected_text:
        errs.append(
            f"{projected.name}: fixture copy DRIFTED from projected catalog "
            f"(re-copy {projected} -> {fixture_catalog})"
        )

    # Payload presence: every entry's payload_path resolves under the fixture root.
    # (payload_path is catalog-relative — same as Stage's runtime read.)
    try:
        entries = json.loads(fixture_text).get("materials", [])
    except json.JSONDecodeError as exc:
        return errs + [f"{fixture_catalog.name}: invalid JSON: {exc}"]
    for entry in entries:
        rel = entry.get("payload_path", "")
        if not rel:
            errs.append(f"{projected.name}: entry {entry.get('id', '?')} has empty payload_path")
            continue
        fixture_payload = fixture_root / rel
        if not fixture_payload.exists():
            errs.append(
                f"{projected.name}: payload missing in fixture tree for "
                f"{entry.get('id', '?')}: {rel}"
            )
            continue

        # (3) 71.12 F6 — the payload's CONTENT must match the authored .mtlx, not merely exist.
        # The deployed daemon reads the FIXTURE's copy, so a stale payload here is a fix that
        # silently never reaches the app. See the module docstring: this exact drift shipped a
        # "fixed" Diamond that was still broken, through a PASSING gate.
        source_payload = source_root / rel
        if not source_payload.exists():
            errs.append(
                f"{projected.name}: payload missing in Matter-Library for "
                f"{entry.get('id', '?')}: {rel}"
            )
            continue
        if fixture_payload.read_bytes() != source_payload.read_bytes():
            errs.append(
                f"{projected.name}: payload STALE in fixture tree for {entry.get('id', '?')}: "
                f"{rel} — the deployed daemon reads THIS copy, so the authored change is not "
                f"reaching the app (re-sync {source_payload} -> {fixture_payload})"
            )
    return errs


def check_fixture_sync(repo_root: Path, fixture_root: Path) -> bool:
    """Run the cross-repo equality gate. Returns True iff in sync (or cleanly skipped)."""
    if not fixture_root.exists():
        print(f"== fixture sync == (skip: Stage fixture tree absent at {fixture_root})")
        return True
    catalogs = _projected_catalogs(repo_root)
    if not catalogs:
        print("== fixture sync == (skip: no library/releases/*.catalog.json)")
        return True
    # Payloads are catalog-relative, and the authored tree they must match is MatterLibrary/.
    source_root = repo_root / "MatterLibrary"
    print("== fixture sync ==")
    ok = True
    for projected in catalogs:
        errs = check_release(projected, fixture_root, source_root)
        if errs:
            ok = False
            for e in errs:
                print(f"  [FAIL] {e}")
        else:
            print(f"  [PASS] {projected.name}: fixture copy byte-current + payloads "
                  f"present AND byte-equal to the authored .mtlx")
    return ok


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Cross-repo Stage-fixture / projected-catalog equality gate.")
    ap.add_argument("--repo-root", default=str(REPO_ROOT),
                    help="Matter-Library repo root (default: derived from this script)")
    ap.add_argument("--fixture-root", default=None,
                    help="Stage fixture MatterLibrary tree (default: platform-relative)")
    args = ap.parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    fixture_root = Path(args.fixture_root).resolve() if args.fixture_root \
        else default_fixture_root(repo_root)
    return 0 if check_fixture_sync(repo_root, fixture_root) else 1


if __name__ == "__main__":
    raise SystemExit(main())
