#!/usr/bin/env python3
"""Library-level manifest (lockfile) validator (Phase 53; provenance gate Phase 60).

Scope is the *library*, not a single material (R3 — distinct from validate_material.py).
Checks the release lockfile against Contract/Manifest.md:

    validate_manifest.py <matterlib-X.Y.lock.yaml> [--materials-root <dir>]

  * parses as YAML
  * release semver (MAJOR.MINOR.PATCH) — the library release axis
  * each material entry has id + version (vNN) + status (lifecycle)
  * each texture entry has id + version (vNN) + status (lifecycle) [Phase 60]
  * the two version axes are well-formed and never conflated (release semver vs vNN)
  * each id resolves to an on-disk .mtlx: <materials-root>/<id>_<version>.mtlx

Phase 60 — auditable-provenance no-ship gate (shipped-pixel rule, RD-Provenance):
  * every TEXTURE whose status is promoted (candidate/approved) carries a well-formed
    provenance {source, license, evidence}; evidence is a repo-relative path that resolves
    OR a {url, sha256} pair — provenance is NOT projected into the runtime catalog.
  * Phase 60sq2.9 — release-grade DEPTH: at `approved` rank an ambientCG texture must carry
    the {url, sha256} form (a doc-path string is insufficient once the release is approved).
  * material -> texture coverage: a promoted (candidate/approved) MATERIAL may not bind a
    texture of *lower* status, nor an uncovered/clouded texture — a material's bound textures
    must all be at least as promoted as the material. Binding is read from the material .mtlx.

Exit 0 iff well-formed and every id resolves.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import source_provenance as sp  # noqa: E402  (shipped-source-set digest verification)

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
VERSION_RE = re.compile(r"^v\d+$")
LIFECYCLE = {"draft", "candidate", "approved", "deprecated", "retired"}
# Promotion rank — a bound texture must be at least as promoted as the material binding it.
STATUS_RANK = {"draft": 0, "candidate": 1, "approved": 2, "deprecated": 3, "retired": 4}
# Statuses that require recorded provenance and full texture-coverage (the shipped-pixel gate).
PROMOTED = {"candidate", "approved"}
# Texture-file references inside a material .mtlx: the part after 'textures/'.
_TEX_REF_RE = re.compile(r"textures/([^\"']+?\.(?:png|exr|jpg|jpeg|tga|hdr|bmp))")


def _repo_root(manifest: Path) -> Path:
    # Walk up to the Matter-Library repo root (has tools/validators + library), so a
    # provenance evidence path resolves regardless of whether the caller is a real lockfile
    # (library/releases/) or a test fixture (tools/validators/fixtures/).
    p = manifest.resolve()
    for anc in p.parents:
        if (anc / "tools" / "validators").is_dir() and (anc / "library").is_dir():
            return anc
    # fallback: library/releases/<file> -> library -> repo root
    return manifest.parent.parent.parent


def _texture_id_for_ref(ref_after_textures: str, texture_ids: list) -> str | None:
    """Map a texture-file path (relative to textures/) to its lockfile texture id by
    longest-prefix match: id == stem, or stem startswith id + '_' (the <map>_sNN suffix)."""
    stem = re.sub(r"\.(?:png|exr|jpg|jpeg|tga|hdr|bmp)$", "", ref_after_textures)
    best = None
    for tid in texture_ids:
        if stem == tid or stem.startswith(tid + "_"):
            if best is None or len(tid) > len(best):
                best = tid
    return best


def _bound_texture_refs(mtlx_path: Path) -> list:
    """The distinct 'after-textures/' file references a material .mtlx binds (order-stable)."""
    if not mtlx_path.exists():
        return []
    text = mtlx_path.read_text(encoding="utf-8", errors="replace")
    seen, out = set(), []
    for ref in _TEX_REF_RE.findall(text):
        if ref not in seen:
            seen.add(ref)
            out.append(ref)
    return out


def _validate_provenance(prov, repo_root: Path, status: str = "candidate") -> list:
    """Return a list of error strings ([] == well-formed) for a texture's provenance record.

    Phase 60sq2.9 — release-grade evidence DEPTH: at `approved` rank an externally-sourced
    (ambientCG) texture must carry the {url, sha256} form, not merely a resolving doc-path
    string. Candidate rank still accepts either form (the doc-path pointer is adequate
    pre-promotion; the depth is required only when the release is actually approved)."""
    if not isinstance(prov, dict):
        return ["provenance missing or not a mapping"]
    errs = []
    for key in ("source", "license", "evidence"):
        if key not in prov or prov.get(key) in (None, ""):
            errs.append(f"provenance.{key} missing/empty")
    ev = prov.get("evidence")
    if isinstance(ev, dict):
        if not ev.get("url"):
            errs.append("evidence.url missing")
        if not ev.get("sha256"):
            errs.append("evidence.sha256 missing (required with a url)")
    elif isinstance(ev, str) and ev:
        if not (repo_root / ev).exists():
            errs.append(f"evidence path does not resolve: {ev}")
    elif ev not in (None, ""):
        errs.append("evidence must be a repo-relative path (str) or {url, sha256}")
    if status == "approved" and prov.get("source") == "ambientCG" and not isinstance(ev, dict):
        errs.append("approved ambientCG texture requires evidence:{url, sha256} "
                    "(a doc-path string is insufficient at approved rank)")
    return errs


def _mtlx_path(materials_root: Path, mid: str, ver: str) -> Path:
    cand = materials_root / f"{mid}_{ver}.mtlx"
    return cand if cand.exists() else (materials_root / f"{mid}.mtlx")


def validate_manifest(path: Path, materials_root: Path) -> list:
    results = []
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    repo_root = _repo_root(path)

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
            # Standard: <id>_<version>.mtlx. Fallback: bare <id>.mtlx for off-grammar
            # system materials (e.g. IMRSV_MissingMaterial) whose filename has no _vNN axis.
            cand = materials_root / f"{mid}_{ver}.mtlx"
            if not cand.exists() and not (materials_root / f"{mid}.mtlx").exists():
                errs.append(f"does not resolve: {cand} (nor bare {mid}.mtlx)")
        results.append((f"{tag} {mid}", not errs, "ok" if not errs else "; ".join(errs)))

    # ---- textures: id + version + status + provenance gate (Phase 60) ----
    textures = (data or {}).get("textures") or []
    tex_status = {}
    tex_ids = []
    for i, t in enumerate(textures):
        tag = f"texture[{i}]"
        if not isinstance(t, dict):
            results.append((tag, False, f"not a mapping: {t!r}"))
            continue
        tid = t.get("id")
        ver = t.get("version")
        status = t.get("status", "draft")  # legacy pilot records omit status -> draft
        errs = []
        if not tid:
            errs.append("missing id")
        else:
            tex_ids.append(tid)
            tex_status[tid] = status
        if not (isinstance(ver, str) and VERSION_RE.match(ver)):
            errs.append(f"version {ver!r} not 'vNN'")
        if status not in LIFECYCLE:
            errs.append(f"status {status!r} not in {sorted(LIFECYCLE)}")
        # Shipped-pixel rule: a promoted texture must carry auditable provenance.
        if status in PROMOTED:
            perrs = _validate_provenance(t.get("provenance"), repo_root, status)
            errs.extend(perrs)
        # Phase 60sq2.9 — verify the shipped-source-set digest (a real hash-lock on the
        # shipped source textures, not a decorative field): internal consistency always,
        # plus pixel integrity for any map materialized on disk.
        prov = t.get("provenance") if isinstance(t.get("provenance"), dict) else {}
        ev = prov.get("evidence")
        if isinstance(ev, dict) and ev.get("sha256_scope") == "shipped_source_set":
            errs.extend(sp.verify_evidence(repo_root, ev))
        results.append((f"{tag} {tid}", not errs, "ok" if not errs else "; ".join(errs)))

    # ---- material -> texture coverage (Phase 60): a promoted material may not bind a
    #      texture of lower status, an uncovered texture, or a texture missing provenance ----
    if tex_ids:
        for m in materials:
            if not isinstance(m, dict):
                continue
            mstatus = m.get("status")
            if mstatus not in PROMOTED:
                continue  # coverage gate only fires for promoted materials
            mid, ver = m.get("id"), m.get("version")
            if not (mid and isinstance(ver, str)):
                continue
            mtlx = _mtlx_path(materials_root, mid, ver)
            # Distinct bound texture ids (many map files -> one texture id): dedupe, keep order.
            bound_ids, uncovered, seen = [], [], set()
            for ref in _bound_texture_refs(mtlx):
                bound = _texture_id_for_ref(ref, tex_ids)
                if bound is None:
                    if ref not in seen:
                        seen.add(ref)
                        uncovered.append(ref)
                elif bound not in seen:
                    seen.add(bound)
                    bound_ids.append(bound)
            cerrs = [f"binds uncovered texture (not in lockfile): textures/{r}" for r in uncovered]
            for bound in bound_ids:
                bstatus = tex_status.get(bound, "draft")
                if STATUS_RANK.get(bstatus, 0) < STATUS_RANK.get(mstatus, 0):
                    cerrs.append(f"binds under-promoted texture {bound!r} (status {bstatus!r} < material {mstatus!r})")
            results.append((f"coverage {mid}", not cerrs,
                            "all bound textures >= material status" if not cerrs else "; ".join(cerrs)))

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
