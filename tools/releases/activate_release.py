#!/usr/bin/env python3
"""Offline release activation + rollback — the active-release selector writer (Phase 60sq2.13, RD-3/RD-5).

Activation is OFFLINE (Studio stopped, B27) and separate from approval (RD-2): approval records a
release is eligible; ACTIVATION picks which approved release the runtime serves, by writing the
active-release selector. There is NO in-session notification path — the next fresh Studio process
reads the new selector (fresh LoadRuntimeCatalog + empty texture cache), so the process restart IS
the RD-5 texture-cache invalidation.

The selector the Stage resolver reads (MaterialXOps.cpp ReadActiveRelease / ResolveCatalogUnderRootImpl):

    <runtime-dir>/active-release.json      {"active_release": "matterlib-<version>"}   ->
    <runtime-dir>/releases/matterlib-<version>/matterlib-<version>.catalog.json

Atomic activation (RD-5): the selector is switched ONLY once the complete install is verified ready,
via a temp-file + POSIX rename() (os.replace) — so a failure at any earlier check leaves the PRIOR
release active (the file is never touched). Rollback is the same command aimed at a prior approved
release: the prior immutable install root stays present (versioned installs coexist), so restore =
re-point the selector, no rebuild (RD-3/RD-5). A composition pinned past a rollback surfaces
ReleaseConflict by design (accepted boundary, project_no_legacy_compositions) — not this tool's concern.

Install-readiness re-check (RD-4 "re-check the frozen-payload hashes against the installed root"):
  approval-valid   the release's approval artifact validates clean (validate_approval)
  install-present  <runtime-dir>/releases/matterlib-<version>/ + its catalog exist
  catalog-frozen   the installed catalog's sha256 == the approval's frozen `catalog` hash
  dds-frozen       every installed .dds byte-matches the freeze record's hash for that basename,
                   and every frozen .dds is present (the complete compressed payload IS installed)
The frozen `dds_set` DIGEST folds in the staging paths, so it can't be recomputed over the differently
-pathed install tree; the per-file sha256 (path-independent) IS re-checked against the freeze record.

    activate_release.py activate <version> --runtime-dir <MatterLibrary-root> [--repo-root <dir>]
                        [--approval <file>] [--no-dds-check]
    activate_release.py resolve-check --runtime-dir <MatterLibrary-root>   # post-activation verify

Exit 0 iff activation switched the selector (or resolve-check resolved the active release).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent / "validators"))

import validate_approval as va       # noqa: E402
import source_provenance as sp       # noqa: E402

_SELECTOR = "active-release.json"


def _install_dir(runtime_dir: Path, version: str) -> Path:
    return runtime_dir / "releases" / f"matterlib-{version}"


def check_install_ready(repo_root: Path, runtime_dir: Path, version: str,
                        approval_path: Path, check_dds: bool = True) -> list[tuple[str, bool, str]]:
    """The complete-install-ready gate: approval valid + the installed catalog/.dds ARE the frozen
    approved payload (path-independent per-file sha256). Any FAIL means DO NOT switch the selector."""
    releases_dir = repo_root / "library" / "releases"
    results: list[tuple[str, bool, str]] = []

    if not approval_path.exists():
        return [("approval-present", False, f"no approval artifact: {approval_path.name} "
                                            "(promote the release first)")]
    approval_errs = [d for _, good, d in va.validate_approval(approval_path, releases_dir) if not good]
    results.append(("approval-valid", not approval_errs,
                    "ok" if not approval_errs else "; ".join(approval_errs)))
    approval = json.loads(approval_path.read_text(encoding="utf-8"))
    frozen = approval.get("payload_sha256", {}) or {}

    inst = _install_dir(runtime_dir, version)
    catalog = inst / f"matterlib-{version}.catalog.json"
    present = inst.is_dir() and catalog.exists()
    results.append(("install-present", present,
                    f"ok ({inst})" if present else f"installed release/catalog missing under {inst}"))
    if not present:
        return results

    cat_ok = sp.file_sha256(catalog) == frozen.get("catalog")
    results.append(("catalog-frozen", cat_ok,
                    "installed catalog == frozen approved catalog"
                    if cat_ok else "installed catalog sha256 != approval's frozen `catalog` hash"))

    if check_dds and "dds_set" in frozen:
        freeze_name = approval.get("freeze_record", f"matterlib-{version}.freeze.json")
        freeze_path = releases_dir / freeze_name
        if not freeze_path.exists():
            results.append(("dds-frozen", False,
                            f"approval references {freeze_name} but it is missing (cannot re-check .dds)"))
            return results
        freeze = json.loads(freeze_path.read_text(encoding="utf-8"))
        frozen_dds = {Path(e["path"]).name: e["sha256"] for e in freeze.get("files", {}).get("dds", [])}
        installed_dds = {p.name: sp.file_sha256(p) for p in sorted(inst.rglob("*.dds"))}
        missing = [n for n in frozen_dds if n not in installed_dds]
        mismatched = [n for n, h in frozen_dds.items() if n in installed_dds and installed_dds[n] != h]
        dds_ok = bool(frozen_dds) and not missing and not mismatched
        if not frozen_dds:
            detail = "freeze record carries no .dds entries (nothing to re-check)"
        elif dds_ok:
            detail = f"all {len(frozen_dds)} installed .dds byte-match the frozen payload"
        else:
            detail = (f"{len(missing)} missing, {len(mismatched)} byte-mismatched vs the frozen payload"
                      + (f" (e.g. {(missing + mismatched)[0]})" if (missing or mismatched) else ""))
        results.append(("dds-frozen", dds_ok, detail))
    return results


def _atomic_write_selector(runtime_dir: Path, active_id: str) -> None:
    path = runtime_dir / _SELECTOR
    text = json.dumps({"active_release": active_id}, indent=2) + "\n"
    fd, tmp = tempfile.mkstemp(dir=str(runtime_dir), prefix=_SELECTOR + ".", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        os.replace(tmp, path)  # atomic within the runtime filesystem — the ONLY mutation
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def _read_active(runtime_dir: Path) -> str:
    sel = runtime_dir / _SELECTOR
    if not sel.exists():
        return ""
    try:
        return json.loads(sel.read_text(encoding="utf-8")).get("active_release", "")
    except (OSError, json.JSONDecodeError):
        return ""


def activate(repo_root: Path, runtime_dir: Path, version: str,
             approval_path: Path | None, check_dds: bool) -> int:
    repo_root, runtime_dir = repo_root.resolve(), runtime_dir.resolve()
    if not runtime_dir.is_dir():
        print(f"  [FAIL] runtime-dir does not exist: {runtime_dir}")
        print("ACTIVATE: BLOCKED (no runtime install root)")
        return 1
    approval_path = approval_path or repo_root / "library" / "releases" / f"matterlib-{version}.approval.json"
    active_id = f"matterlib-{version}"
    prior = _read_active(runtime_dir)

    print(f"== activate {active_id} — install-readiness (prior active: {prior or '<none>'}) ==")
    checks = check_install_ready(repo_root, runtime_dir, version, approval_path, check_dds)
    ok = True
    for name, good, detail in checks:
        print(f"  [{'PASS' if good else 'FAIL'}] {name}: {detail}")
        ok = ok and good
    if not ok:
        print(f"ACTIVATE: BLOCKED — install not ready; selector UNCHANGED (prior '{prior}' stays active)")
        return 1

    _atomic_write_selector(runtime_dir, active_id)
    print(f"ACTIVATE: SWITCHED — active-release.json: '{prior or '<none>'}' -> '{active_id}' "
          f"(offline; the next fresh Studio process serves it with an empty texture cache)")
    return 0


def resolve_check(runtime_dir: Path) -> int:
    """Post-activation verify (headless): mirror the Stage resolver — the selector's active release
    resolves to a present catalog under releases/<active>/. The ⚠human eyes-on smoke is separate."""
    runtime_dir = runtime_dir.resolve()
    active = _read_active(runtime_dir)
    print(f"== resolve-check — active-release.json under {runtime_dir} ==")
    if not active:
        print("  [FAIL] no/empty selector (active-release.json absent or malformed)")
        print("RESOLVE-CHECK: NO ACTIVE RELEASE")
        return 1
    catalog = runtime_dir / "releases" / active / f"{active}.catalog.json"
    payload = runtime_dir / "releases" / active / "materials"
    cat_ok, pay_ok = catalog.exists(), payload.is_dir()
    print(f"  [{'PASS' if cat_ok else 'FAIL'}] catalog: "
          f"{catalog if cat_ok else str(catalog) + ' MISSING (selector names an unstaged release)'}")
    print(f"  [{'PASS' if pay_ok else 'FAIL'}] payload: "
          f"{'materials/ present' if pay_ok else str(payload) + ' MISSING'}")
    good = cat_ok and pay_ok
    print(f"RESOLVE-CHECK: {'ACTIVE ' + active + ' RESOLVES' if good else 'ACTIVE RELEASE DOES NOT RESOLVE'}")
    return 0 if good else 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Offline release activation + rollback (RD-3/RD-5).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("activate", help="verify install-ready + atomically switch the selector")
    a.add_argument("version")
    a.add_argument("--runtime-dir", type=Path, required=True,
                   help="the deployed MatterLibrary root (contains releases/ + active-release.json)")
    a.add_argument("--repo-root", type=Path, default=_HERE.parent.parent)
    a.add_argument("--approval", type=Path, default=None, help="approval artifact (default: repo library/releases/)")
    a.add_argument("--no-dds-check", action="store_true",
                   help="skip the per-file .dds re-check (catalog re-check still runs)")
    r = sub.add_parser("resolve-check", help="post-activation: the active release resolves headless")
    r.add_argument("--runtime-dir", type=Path, required=True)
    args = ap.parse_args(argv)

    if args.cmd == "activate":
        return activate(args.repo_root, args.runtime_dir, args.version,
                        args.approval, not args.no_dds_check)
    return resolve_check(args.runtime_dir)


if __name__ == "__main__":
    raise SystemExit(main())
