#!/usr/bin/env python3
"""Release-level approval-artifact validator (Phase 60sq2.3.2, RD-1).

The EXTERNAL approval artifact — library/releases/matterlib-<version>.approval.json — is the sole
release-promotion flip (RD-1/RD-2): it records that a release is immutable + eligible for PRODUCTION
ACTIVATION and REFERENCES the complete frozen-payload hashes (RD-4). It is a control-boundary file:
the runtime never reads it (runtime stays status-blind), and it does NOT mutate the manifest.

This is a VALIDATOR — it only CHECKS an approval artifact's shape + internal consistency. The
artifact is CREATED by the terminal promotion command promote_release.py (60sq2.12), which
references the frozen hashes from freeze_release.py (60sq2.3.3). Kept SEPARATE from the per-material
validate_manifest.py (§11 fix 4).

    validate_approval.py <approval.json> [--releases-dir <dir>]

Checks (mirrors validate_manifest's (name, ok, detail) result shape):
  json                     parses as a JSON object
  required-keys            release / approved_at / approver / payload_sha256 present
  release                  non-empty string
  release-matches-filename release == the filename's <version> (matterlib-<version>.approval.json)
  approved_at              non-empty ISO-8601 timestamp
  approver                 non-empty
  payload_sha256           a NON-EMPTY map of <payload-key> -> 64-hex sha256 (references the frozen
                           payload; a shallow/empty hash set == a promotion that never actually froze)
  release-record           (with --releases-dir) a matterlib-<release>.lock.yaml exists

Exit 0 iff every check passes.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
# Lenient ISO-8601: YYYY-MM-DD, optionally with THH:MM(:SS)(.frac)(Z|+hh:mm).
_ISO_RE = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2})?(\.\d+)?(Z|[+-]\d{2}:?\d{2})?)?$")
_APPROVAL_SUFFIX = ".approval.json"


def _release_from_filename(path: Path) -> str:
    """matterlib-0.1.0.approval.json -> '0.1.0' (bare, matching the lock.yaml `release` field)."""
    name = path.name
    if name.endswith(_APPROVAL_SUFFIX):
        stem = name[: -len(_APPROVAL_SUFFIX)]  # matterlib-0.1.0
        if stem.startswith("matterlib-"):
            return stem[len("matterlib-"):]  # 0.1.0
    return ""


def validate_approval(path: Path, releases_dir: Path | None = None) -> list:
    """Return a list of (check_name, ok, detail) tuples (always >= 1)."""
    results: list = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [("json", False, f"cannot read/parse: {exc}")]
    if not isinstance(data, dict):
        return [("json", False, "approval artifact is not a JSON object")]
    results.append(("json", True, "ok"))

    required = ("release", "approved_at", "approver", "payload_sha256")
    missing = [k for k in required if k not in data]
    results.append(("required-keys", not missing,
                    "ok" if not missing else f"missing: {', '.join(missing)}"))

    release = data.get("release", "")
    release_ok = isinstance(release, str) and bool(release)
    results.append(("release", release_ok, "ok" if release_ok else "empty/non-string release"))

    expected = _release_from_filename(path)
    if expected:
        match = (release == expected)
        results.append(("release-matches-filename", match,
                        "ok" if match else f"release {release!r} != filename version {expected!r}"))

    approved_at = data.get("approved_at", "")
    at_ok = isinstance(approved_at, str) and bool(_ISO_RE.match(approved_at or ""))
    results.append(("approved_at", at_ok, "ok" if at_ok else f"not ISO-8601: {approved_at!r}"))

    approver = data.get("approver", "")
    approver_ok = isinstance(approver, str) and bool(approver)
    results.append(("approver", approver_ok, "ok" if approver_ok else "empty/non-string approver"))

    ps = data.get("payload_sha256", None)
    if not isinstance(ps, dict) or not ps:
        results.append(("payload_sha256", False,
                        "must be a NON-EMPTY map payload-key -> sha256 (shallow/unfrozen approval)"))
    else:
        bad = [f"{k}={v!r}" for k, v in ps.items()
               if not (isinstance(v, str) and _SHA256_RE.match(v))]
        results.append(("payload_sha256", not bad,
                        "ok" if not bad else "non-sha256 entries: " + "; ".join(bad)))

    if releases_dir is not None and release:
        lock = releases_dir / f"matterlib-{release}.lock.yaml"
        results.append(("release-record", lock.exists(),
                        "ok" if lock.exists() else f"no release record: {lock.name}"))
    return results


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Validate a release-level approval artifact (RD-1).")
    ap.add_argument("approval", type=Path, help="the matterlib-<version>.approval.json to check")
    ap.add_argument("--releases-dir", type=Path, default=None,
                    help="library/releases/ — enables the release-record existence check")
    args = ap.parse_args(argv)
    results = validate_approval(args.approval, args.releases_dir)
    ok = all(good for _, good, _ in results)
    for name, good, detail in results:
        print(f"  [{'PASS' if good else 'FAIL'}] {name}: {detail}")
    print("APPROVAL:", "VALID" if ok else "INVALID")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
