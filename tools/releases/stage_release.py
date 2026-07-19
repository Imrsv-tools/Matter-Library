#!/usr/bin/env python3
"""Release-staging tree producer for a Matter release (Phase 60sq2.5).

Assembles a self-contained, deterministic per-release texture snapshot:

    library/staging/matterlib-<version>/textures/<subtree>/<name>.png
    library/staging/matterlib-<version>/textures/<subtree>/<name>.dds   <- BCn sibling

The ``.dds`` are offline-compressed release DERIVATIVES (compress_textures.py, 60sq2.4),
NEVER written back into the authored ``MatterLibrary/textures`` source tree (Phase 60sq2
invariant #3: the uncompressed source stays the open material source of truth AND the
deployed-path RED fixture, by construction). The PNG is copied alongside so the staging
tree is a self-contained release payload snapshot (freeze / qualification consume it).

Downstream:
  * deploy-to-studio.sh overlays this staging tree's ``.dds`` into the deployed install
    root (``releases/matterlib-<version>/textures/``) so the Plugin by-path load (60sq2.6)
    finds a ``.dds`` sibling next to each resolved ``.png``.
  * freeze_release.py ``--staging <this tree>`` hash-locks the ``.dds`` into the complete
    frozen payload (RD-4); the approval artifact references those hashes.

The staging tree is a REPRODUCIBLE build artifact and is GITIGNORED (``library/staging/``):
compress_textures is deterministic at the pinned encoder + flags, so it regenerates
byte-identically, and the freeze hash-lock + the determinism gate provide the integrity
guarantee — there is no need to commit the (large) binary derivatives. This mirrors the
build_portable.py gitignored-output precedent.

Sequencing (plan 60sq2.5): the compressor runs after ``gen_*_textures.py`` (it reads their
output — the shipped source PNG tree) and independently of ``project_runtime_catalog.py``
(the catalog projects the lockfile, never touches textures — Discovery D2). There is no
pipeline driver; this is a standalone CLI invoked in the staging flow.

    stage_release.py build  <version> [--repo-root <dir>] [--staging-root <dir>]
    stage_release.py verify <version> [--repo-root <dir>] [--staging-root <dir>]

Exit 0 iff build produced / verify found a complete, valid {png, dds} snapshot for every
shipped source texture.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "compressors"))
import compress_textures as ct  # noqa: E402

_MATTERLIB = "MatterLibrary"


def default_staging_root(repo_root: Path) -> Path:
    return repo_root / "library" / "staging"


def release_dir(staging_root: Path, version: str) -> Path:
    return staging_root / f"matterlib-{version}" / "textures"


def _source_root(repo_root: Path) -> Path:
    return repo_root / _MATTERLIB / "textures"


def build(repo_root: Path, version: str, staging_root: Path | None = None,
          only: str | None = None) -> tuple[bool, list[dict]]:
    """(Re)build the staging tree for ``version``. Returns (ok, [compress record...]).

    Clean rebuild: the release's staging subtree is removed first so a dropped source
    texture cannot leave a stale ``.dds`` behind (determinism / completeness)."""
    repo_root = repo_root.resolve()
    src_root = _source_root(repo_root)
    if not src_root.exists():
        print(f"  [FAIL] no source texture tree at {src_root}")
        return False, []
    staging_root = (staging_root or default_staging_root(repo_root)).resolve()
    dst = release_dir(staging_root, version)
    # Clean rebuild of THIS release's subtree only (siblings — other releases — untouched).
    if dst.parent.exists():
        shutil.rmtree(dst.parent)
    dst.mkdir(parents=True, exist_ok=True)

    # .dds derivatives (mirrors src subtree, .png -> .dds).
    ok, records = ct.compress_tree(src_root, dst, only=only)

    # PNG siblings — self-contained snapshot (copied verbatim from the shipped source).
    for rec in records:
        src = Path(rec["src"])
        rel = src.relative_to(src_root)
        png_dst = dst / rel
        png_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, png_dst)
    return ok, records


def verify(repo_root: Path, version: str, staging_root: Path | None = None,
           only: str | None = None) -> list[str]:
    """Encoder-INDEPENDENT completeness check of an already-built staging tree.

    Every shipped source texture must have (1) its PNG present in staging and (2) a valid,
    role-correct, mip-complete ``.dds`` sibling. Returns [] iff complete. Needs no encoder,
    so it runs in CI without the pinned compressor."""
    repo_root = repo_root.resolve()
    src_root = _source_root(repo_root)
    if not src_root.exists():
        return [f"no source texture tree at {src_root}"]
    staging_root = (staging_root or default_staging_root(repo_root)).resolve()
    dst = release_dir(staging_root, version)
    if not dst.exists():
        return [f"staging tree absent for release {version}: {dst} (run `stage_release.py build {version}`)"]

    errs: list[str] = []
    sources = ct.discover(src_root, only)
    if not sources:
        return [f"no source textures discovered under {src_root}"]
    for src in sources:
        rel = src.relative_to(src_root)
        png_dst = dst / rel
        dds_dst = (dst / rel).with_suffix(ct.OUT_EXT)
        if not png_dst.exists():
            errs.append(f"missing staged PNG: {rel}")
        if not dds_dst.exists():
            errs.append(f"missing staged .dds: {rel.with_suffix(ct.OUT_EXT)}")
            continue
        try:
            role, bc = ct.classify(src, src_root)
        except ct.ClassifyError as e:
            errs.append(f"cannot classify {rel}: {e}")
            continue
        w, h = ct.png_dims(src)
        rec = {"dst": str(dds_dst), "w": w, "h": h, "mips": ct.full_miplevels(w, h), "bc": bc}
        good, detail = ct.validate_output(rec)
        if not good:
            errs.append(f"invalid staged .dds {rel.with_suffix(ct.OUT_EXT)}: {detail}")
    return errs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Release-staging tree producer for a Matter release (60sq2.5).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, helptext in (("build", "compress + assemble the {png,dds} staging tree"),
                           ("verify", "check an already-built staging tree is complete + valid")):
        p = sub.add_parser(name, help=helptext)
        p.add_argument("version")
        p.add_argument("--repo-root", type=Path, default=_HERE.parent.parent)
        p.add_argument("--staging-root", type=Path, default=None)
        p.add_argument("--only", default=None, help="restrict to sources whose path contains this substring")
    args = ap.parse_args(argv)

    if args.cmd == "build":
        if not ct._check_encoder():
            return 1
        ok, records = build(args.repo_root, args.version, args.staging_root, args.only)
        for rec in records:
            good, detail = ct.validate_output(rec)
            print(f"  [{'PASS' if good else 'FAIL'}] {Path(rec['dst']).name}: {detail}")
            ok = ok and good
        staging = (args.staging_root or default_staging_root(args.repo_root.resolve())).resolve()
        print(f"staged release {args.version} -> {release_dir(staging, args.version)}")
        print("RESULT:", "ALL PASS" if ok else "FAILURES")
        return 0 if ok else 1

    errs = verify(args.repo_root, args.version, args.staging_root, args.only)
    for e in errs:
        print(f"  [FAIL] {e}")
    print("RESULT:", "COMPLETE" if not errs else "INCOMPLETE")
    return 0 if not errs else 1


if __name__ == "__main__":
    raise SystemExit(main())
