#!/usr/bin/env python3
"""Terminal promotion — CREATE the external release-level approval artifact (Phase 60sq2.12, RD-1/RD-2).

Promotion is the SOLE release-promotion flip (RD-1): it produces the control-boundary approval
artifact library/releases/matterlib-<version>.approval.json that records the release is immutable +
eligible for PRODUCTION ACTIVATION, REFERENCING the complete frozen-payload hashes (RD-4) — it never
mutates the manifest (statuses are settled to `approved` BEFORE the freeze, so the approved release is
byte-identical to the qualified candidate). The runtime never reads this artifact (status-blind, RD-1).

  §11 fix 4 division of labour: a VALIDATOR only checks (validate_approval.py); the PROMOTER creates.
  RD-2: approval != activation — this step keys on approval; activation/rollback key on the selector
  (activate_release.py, 60sq2.13). Approval is never revoked or rewritten by a rollback.

Before writing the artifact, promotion re-asserts atomic version-surface agreement across the release
surfaces it owns (invariant #9), refusing to promote if any fails:

  release-record       library/releases/matterlib-<version>.lock.yaml exists
  all-approved         every manifest entry (materials + textures) is status `approved`
                       (RD-4 settle-before-freeze; promotion first EXPOSES `approved`, never invents it)
  freeze-present       library/releases/matterlib-<version>.freeze.json exists (freeze BEFORE promote)
  catalog-current      the committed .catalog.json re-projects byte-identically from the lockfile
  fixture-sync         the cross-repo Stage fixture mirror is byte-current with the projected catalog
  freeze-matches       the freeze record STILL verifies against the on-disk complete payload
                       (catalog/manifest/.mtlx/source-textures/.dds) — the approved release IS the
                       frozen candidate, byte-for-byte (RD-4)

The wire ABI axes (IOX_PROTOCOL_VERSION / SKELETAL_MESH_HEADER_VERSION / the sizeof static_asserts /
Studio ProjectVersion) concern the compressed_roles_mask PROTOCOL, not the release semver; they are
pinned in committed C++/ini and gated by the Stage/Plugin suites (60sq2.6), not re-checked from here.

    promote_release.py <version> --approver <name> [--repo-root <dir>] [--staging <dir>]
                       [--freeze <record.json>] [--out <approval.json>] [--approved-at <iso8601>]
                       [--force]

--approved-at defaults to the current UTC time (a real wall-clock promotion timestamp). --force
overwrites an existing approval artifact (promotion is normally once-per-release + immutable).

Exit 0 iff every agreement check passes and a valid approval artifact was written.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "validators"))
sys.path.insert(0, str(_HERE.parent / "converters"))

import freeze_release as fr          # noqa: E402
import validate_approval as va       # noqa: E402
import project_runtime_catalog as prc  # noqa: E402
import check_fixture_sync as cfs      # noqa: E402

try:
    import yaml  # noqa: E402
except ImportError:  # pragma: no cover
    yaml = None


def _releases_dir(repo_root: Path) -> Path:
    return repo_root / "library" / "releases"


def _all_entries_approved(manifest: Path) -> tuple[bool, str]:
    """Every material + texture entry in the lockfile is status `approved` (RD-4)."""
    if yaml is None:
        return False, "PyYAML unavailable — cannot read the manifest"
    data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
    not_approved: list[str] = []
    for section in ("materials", "textures"):
        for entry in data.get(section, []) or []:
            ident = entry.get("id") or entry.get("name") or "?"
            if entry.get("status") != "approved":
                not_approved.append(f"{section}:{ident}={entry.get('status')!r}")
    if not_approved:
        return False, "not-approved entries: " + ", ".join(not_approved[:6]) + (
            " …" if len(not_approved) > 6 else "")
    return True, "all entries approved"


def _catalog_current(repo_root: Path, version: str) -> tuple[bool, str]:
    releases = _releases_dir(repo_root)
    lock = releases / f"matterlib-{version}.lock.yaml"
    catalog = releases / f"matterlib-{version}.catalog.json"
    if not catalog.exists():
        return False, f"committed {catalog.name} missing"
    materials_root = repo_root / "MatterLibrary" / "materials"
    try:
        projected = prc.project_to_string(lock, materials_root)
    except Exception as exc:  # noqa: BLE001
        return False, f"projection error: {exc}"
    return (catalog.read_text(encoding="utf-8") == projected,
            "byte-current with the lockfile" if catalog.read_text(encoding="utf-8") == projected
            else "DRIFTED from lockfile (run project_runtime_catalog.py)")


def check_agreement(repo_root: Path, version: str, staging: Path | None) -> list[tuple[str, bool, str]]:
    """Atomic version-surface agreement across the release surfaces promotion owns (invariant #9)."""
    releases = _releases_dir(repo_root)
    lock = releases / f"matterlib-{version}.lock.yaml"
    freeze = releases / f"matterlib-{version}.freeze.json"
    results: list[tuple[str, bool, str]] = []

    results.append(("release-record", lock.exists(),
                    "ok" if lock.exists() else f"no release record: {lock.name}"))
    if lock.exists():
        ok, detail = _all_entries_approved(lock)
        results.append(("all-approved", ok, detail))

    results.append(("freeze-present", freeze.exists(),
                    "ok" if freeze.exists() else f"no freeze record: {freeze.name} "
                    "(run freeze_release.py compute)"))

    ok, detail = _catalog_current(repo_root, version)
    results.append(("catalog-current", ok, detail))

    try:
        sync_ok = cfs.check_fixture_sync(repo_root, cfs.default_fixture_root(repo_root))
    except Exception as exc:  # noqa: BLE001
        sync_ok, detail = False, f"fixture-sync error: {exc}"
    else:
        detail = "Stage fixture mirror byte-current" if sync_ok else "Stage fixture DRIFTED"
    results.append(("fixture-sync", sync_ok, detail))

    if freeze.exists():
        record = json.loads(freeze.read_text(encoding="utf-8"))
        errs = fr.verify_freeze(repo_root, record, staging)
        results.append(("freeze-matches", not errs,
                        "on-disk payload IS the frozen candidate" if not errs
                        else "; ".join(errs[:3])))
    return results


def build_approval(version: str, freeze_record: dict, approver: str, approved_at: str,
                   freeze_name: str) -> dict:
    """The external approval artifact — references the frozen hashes, never rewrites the payload."""
    return {
        "release": version,
        "approved_at": approved_at,
        "approver": approver,
        "payload_sha256": dict(freeze_record["payload_sha256"]),
        "payload_digest": freeze_record["payload_digest"],
        "freeze_record": freeze_name,
    }


def _atomic_write_json(path: Path, data: dict) -> None:
    text = json.dumps(data, indent=2, sort_keys=True) + "\n"
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=path.name + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)  # atomic within the same filesystem
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def promote(repo_root: Path, version: str, approver: str, approved_at: str,
            staging: Path | None, out: Path | None, force: bool) -> int:
    repo_root = repo_root.resolve()
    releases = _releases_dir(repo_root)
    freeze = releases / f"matterlib-{version}.freeze.json"
    out = out or releases / f"matterlib-{version}.approval.json"

    print(f"== promote {version} — version-surface agreement ==")
    agreement = check_agreement(repo_root, version, staging)
    ok = True
    for name, good, detail in agreement:
        print(f"  [{'PASS' if good else 'FAIL'}] {name}: {detail}")
        ok = ok and good
    if not ok:
        print("PROMOTE: BLOCKED (version-surface disagreement — release NOT promoted)")
        return 1

    if out.exists() and not force:
        print(f"PROMOTE: BLOCKED — {out.name} already exists (approval is immutable; --force to re-issue)")
        return 1

    freeze_record = json.loads(freeze.read_text(encoding="utf-8"))
    approval = build_approval(version, freeze_record, approver, approved_at, freeze.name)
    _atomic_write_json(out, approval)

    # Validate the durable artifact on disk (the exact check run_all's approval_gate re-runs).
    post = va.validate_approval(out, releases)
    post_ok = all(good for _, good, _ in post)
    for name, good, detail in post:
        print(f"  [{'PASS' if good else 'FAIL'}] approval:{name}: {detail}")
    if not post_ok:
        out.unlink(missing_ok=True)
        print("PROMOTE: BLOCKED (written approval failed validation — removed)")
        return 1

    print(f"PROMOTE: APPROVED — {out.name} references payload_digest "
          f"{approval['payload_digest']} (approver={approver}, at={approved_at})")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Terminal promotion — create the approval artifact (RD-1).")
    ap.add_argument("version")
    ap.add_argument("--approver", required=True, help="who approves (recorded in the artifact)")
    ap.add_argument("--repo-root", type=Path, default=_HERE.parent.parent)
    ap.add_argument("--staging", type=Path, default=None,
                    help="the staging tree (enables the .dds half of the freeze re-verify)")
    ap.add_argument("--freeze", type=Path, default=None, help="(unused override) freeze record path")
    ap.add_argument("--out", type=Path, default=None, help="approval artifact output path")
    ap.add_argument("--approved-at", default=None, help="ISO-8601 timestamp (default: now, UTC)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing approval artifact")
    args = ap.parse_args(argv)

    approved_at = args.approved_at or _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return promote(args.repo_root, args.version, args.approver, approved_at,
                   args.staging, args.out, args.force)


if __name__ == "__main__":
    raise SystemExit(main())
