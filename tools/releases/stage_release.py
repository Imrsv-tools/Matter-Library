#!/usr/bin/env python3
"""Release-staging tree producer for a Matter release (Phase 60sq2.5).

Assembles a self-contained, deterministic per-release snapshot of its textures and (#426) HDRIs:

    library/staging/matterlib-<version>/textures/<subtree>/<name>.png
    library/staging/matterlib-<version>/textures/<subtree>/<name>.dds   <- BCn sibling
    library/staging/matterlib-<version>/hdris/<published>_<vNN>.hdr     <- stamped (hdris.stamp)
    library/staging/matterlib-<version>/hdris/<published>_<vNN>.dds     <- its BC6H cube (#424)
    library/staging/matterlib-<version>/thumbnails/hdris/<published>_<vNN>.jpg

Each HDRI the lock lists is staged under its published name (RD-LBL-5), at the release catalog's
own payload and thumbnail paths, so the folder installs as the release root.

The ``.dds`` are offline-compressed release DERIVATIVES (compress_textures.py, 60sq2.4),
NEVER written back into the authored ``MatterLibrary/textures`` source tree (Phase 60sq2
invariant #3: the uncompressed source stays the open material source of truth AND the
deployed-path RED fixture, by construction). The PNG is copied alongside so the staging
tree is a self-contained release payload snapshot (freeze / qualification consume it).

Downstream:
  * deploy-to-studio.sh overlays this staging tree's ``.dds`` into the deployed install
    root (``releases/matterlib-<version>/textures/``) so the Plugin by-path load (60sq2.6)
    finds a ``.dds`` sibling next to each resolved ``.png``, and installs its ``hdris/`` and
    ``thumbnails/hdris/``.
  * freeze_release.py ``--staging <this tree>`` hash-locks the ``.dds`` and the staged ``.hdr``
    into the complete frozen payload (RD-4); the approval artifact references those hashes.

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
shipped source texture, and a stamped .hdr, valid cube and thumbnail for every listed HDRI.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent / "compressors"))
sys.path.insert(0, str(_HERE.parent / "validators"))
sys.path.insert(0, str(_HERE))
import compress_textures as ct  # noqa: E402
import hdri_cube as hc  # noqa: E402
import source_provenance as sp  # noqa: E402
import validate_manifest as vm  # noqa: E402
import hdris as H  # noqa: E402
import serve_to_stage as sts  # noqa: E402  (stage_dev and the dev cubes: one cube builder for both)
import yaml  # noqa: E402

_MATTERLIB = "MatterLibrary"


def default_staging_root(repo_root: Path) -> Path:
    return repo_root / "library" / "staging"


def release_root(staging_root: Path, version: str) -> Path:
    return staging_root / f"matterlib-{version}"


def release_hdris(repo_root: Path, version: str, only: str | None = None) -> list[dict]:
    """The HDRIs the release's lock lists, as ``hdris.on_disk`` rows (published id, source file,
    record). A listed HDRI with no file on disk is an error, as a missing texture is."""
    lock = repo_root / "library" / "releases" / f"matterlib-{version}.lock.yaml"
    listed = {(h["id"], h["version"]) for h in (yaml.safe_load(lock.read_text(encoding="utf-8")) or {})
              .get("hdris") or []}
    rows = [r for r in H.on_disk(repo_root) if (r["source_id"], r["version"]) in listed]
    missing = listed - {(r["source_id"], r["version"]) for r in rows}
    if missing:
        raise FileNotFoundError(f"release {version} lists HDRIs not on disk: {sorted(missing)}")
    return [r for r in rows if not only or only.lower() in str(r["path"]).lower()]


def _hdri_paths(out: Path, row: dict) -> tuple[Path, Path, Path]:
    """A staged HDRI's .hdr, cube .dds and thumbnail: the release catalog's paths (#426)."""
    hdr = out / "hdris" / f"{row['identity']}{vm.HDRI_EXT}"
    return hdr, hdr.with_suffix(ct.OUT_EXT), out / "thumbnails" / "hdris" / f"{row['identity']}.jpg"


def _cube(src: Path, dst: Path) -> None:
    """An HDRI's cube: the dev staging tree's copy when it is up to date with src (the same
    builder made it), else built (minutes a sky)."""
    dev = sts.DEV_HDRI_STAGING / dst.name
    if sts.up_to_date(src, dev):
        shutil.copy2(dev, dst)
    else:
        hc.build_cube_dds(src, dst)


def stage_hdris(repo_root: Path, version: str, out: Path, only: str | None = None) -> list[str]:
    """Stage each HDRI the lock lists into the release folder ``out``: its stamped copy (as the dev
    serve stamps it), its BC6H cube (``stage_dev``, as the dev serve's: CUBE_WORKERS at once) and
    its thumbnail. Returns the HDRIs whose cube could not be made, each with why."""
    rows = release_hdris(repo_root, version, only)
    for row in rows:
        hdr, _, jpg = _hdri_paths(out, row)
        H.stamp(row["path"], hdr, H.facts(row))
        H.thumbnail(row["path"], jpg)
    return sts.stage_dev(sts.cube_jobs(rows), out / "hdris", _cube, sts.CUBE_WORKERS)["missed"]


def verify_hdris(repo_root: Path, version: str, out: Path, only: str | None = None) -> list[str]:
    """What is wrong with the release folder ``out``'s HDRIs ([] when nothing): each listed HDRI's
    stamped .hdr says its facts, its cube is valid, its thumbnail is there."""
    errs = []
    for row in release_hdris(repo_root, version, only):
        hdr, dds, jpg = _hdri_paths(out, row)
        if not hdr.is_file():
            errs.append(f"missing staged HDRI: {hdr.name}")
        elif not H.stamp_says(hdr, H.facts(row)):
            errs.append(f"staged HDRI {hdr.name}: its stamp does not say {row['source_id']}'s facts")
        _, _, height = vm.read_hdr_header(row["path"])
        problems = hc.validate_cube_dds(dds, min(height, hc.MAX_FACE)) if dds.is_file() else ["missing"]
        if problems:
            errs.append(f"staged cube {dds.name}: {'; '.join(problems)}")
        if not jpg.is_file():
            errs.append(f"missing staged thumbnail: {jpg.name}")
    return errs


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
    out = release_root(staging_root, version)
    dst = out / "textures"
    # Clean rebuild of THIS release's subtree only (siblings — other releases — untouched).
    if out.exists():
        shutil.rmtree(out)
    dst.mkdir(parents=True, exist_ok=True)

    # .dds derivatives (mirrors src subtree, .png -> .dds).
    # Exactly the textures this release's lock names (Phase03), never every PNG on disk.
    ok, records = ct.compress_tree(src_root, dst, only=only,
                                   sources=sp.release_textures(repo_root, version))

    # PNG siblings — self-contained snapshot (copied verbatim from the shipped source).
    for rec in records:
        src = Path(rec["src"])
        rel = src.relative_to(src_root)
        png_dst = dst / rel
        png_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, png_dst)

    # HDRIs (#426): stamped, each with its cube and thumbnail.
    missed = stage_hdris(repo_root, version, out, only)
    for m in missed:
        print(f"  [FAIL] no cube for {m}")
    return ok and not missed, records


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
    out = release_root(staging_root, version)
    dst = out / "textures"
    if not dst.exists():
        return [f"staging tree absent for release {version}: {dst} (run `stage_release.py build {version}`)"]

    errs: list[str] = []
    sources = [p for p in sp.release_textures(repo_root, version)
               if not only or only.lower() in str(p).lower()]
    if not sources:
        return [f"no source textures discovered under {src_root}"]
    errs.extend(verify_hdris(repo_root, version, out, only))
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
        print(f"staged release {args.version} -> {release_root(staging, args.version)}")
        print("RESULT:", "ALL PASS" if ok else "FAILURES")
        return 0 if ok else 1

    errs = verify(args.repo_root, args.version, args.staging_root, args.only)
    for e in errs:
        print(f"  [FAIL] {e}")
    print("RESULT:", "COMPLETE" if not errs else "INCOMPLETE")
    return 0 if not errs else 1


if __name__ == "__main__":
    raise SystemExit(main())
