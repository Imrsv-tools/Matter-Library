#!/usr/bin/env python3
"""Build the v2.4-native OCIO parity config bundle (Phase 60sq2.8).

The material-authoring / eyes-on color pipeline must be a DEFINED, parity-grade
color transform (Blender authoring <-> Storm reference <-> UE deployed capture all
resolving to the same view transform). Until now the box carried a *header-hacked*
config at ``~/.config/imrsv/ocio/`` — Blender's shipped ``config.ocio`` copied with
its ``ocio_profile_version`` line changed 2.5 -> 2.4 so the system OpenColorIO 2.4.2
would load it. That was explicitly a TEMPORARY qualitative-smoke config, NEVER
parity-grade: it still carried OCIO-2.5-only keys (``interop_id`` and the per-
ColorSpace ``interchange``) that 2.4.2 *silently ignores* (emitting a warning per
key). The color MATH is unaffected by those keys — AgX / Filmic are LUT-based
(version-independent), and every view-transform processor builds correctly under
2.4.2 — but a config that loads with 22 "unknown key" warnings is not something you
can call a parity reference in good conscience.

This tool produces a genuinely 2.4-NATIVE config: it loads Blender's shipped config
under OpenColorIO 2.4.2 (which drops the 2.5-only keys), stamps the version to 2.4,
and re-serializes OCIO's own canonical 2.4 form — so the output has ZERO ignored
constructs and loads warning-free. The interchange ROLES (``aces_interchange`` /
``cie_xyz_d65_interchange``) — the standard 2.x cross-config mechanism — are
preserved; only the 2.5 per-space metadata keys are gone.

Reproducibility: the bundle is a machine-local BUILD ARTIFACT (like the gitignored
release staging tree), derived from whatever Blender is installed. THIS SCRIPT is
the repo-tracked, portable source of truth — run it on any box (pass ``--source``
for a non-Fedora Blender) to regenerate an identical parity config. Nothing 20 MB
lands in git.

Usage:
  build_ocio_parity_config.py [--source <blender colormanagement dir>]
                              [--out <dir>] [--validate-only]

Exit 0 iff the built config loads warning-free under OCIO 2.4.2 and every graded
view transform (AgX / Filmic / Standard) builds a processor.
"""
from __future__ import annotations

import argparse
import io
import shutil
import sys
import tempfile
from contextlib import redirect_stderr
from pathlib import Path

# Candidate Blender color-management dirs (the reproducible SOURCE). First existing wins.
DEFAULT_SOURCES = [
    "/usr/share/blender/5.1/datafiles/colormanagement",
    "/usr/share/blender/5.2/datafiles/colormanagement",
    "/Applications/Blender.app/Contents/Resources/5.1/datafiles/colormanagement",
]
DEFAULT_OUT = Path.home() / ".config/imrsv/ocio-parity"

# The view transforms IMRSV grades for parity (Experience_Materials — AgX is the
# Blender authoring default; the others are the reference alternatives).
GRADED_VIEWS = ["AgX", "Filmic", "Standard"]


def _ocio():
    try:
        import PyOpenColorIO as ocio
        return ocio
    except ImportError:
        print("RESULT: FAIL — PyOpenColorIO not importable in this interpreter")
        raise SystemExit(2)


def find_source(explicit: str | None) -> Path:
    if explicit:
        p = Path(explicit)
        if not (p / "config.ocio").exists():
            print(f"RESULT: FAIL — no config.ocio under --source {p}")
            raise SystemExit(2)
        return p
    for cand in DEFAULT_SOURCES:
        if (Path(cand) / "config.ocio").exists():
            return Path(cand)
    print("RESULT: FAIL — no Blender colormanagement dir found; pass --source")
    raise SystemExit(2)


def to_native_2_4(src_config: Path) -> str:
    """Load the source config under OCIO 2.4.2 (dropping 2.5-only keys) and return a
    canonical, warning-free 2.4-native serialization."""
    ocio = _ocio()
    txt = src_config.read_text()
    # OCIO 2.4.2 refuses a 2.5 header outright; hack the header in a temp copy so it
    # will load — loading is where the 2.5-only KEYS are dropped.
    for v in ("2.5", "2.6", "2.7"):
        txt = txt.replace(f"ocio_profile_version: {v}", "ocio_profile_version: 2.4")
    # OCIO load/serialize is lazy — it does NOT resolve the LUT search_path until a
    # processor is built — so the temp can live anywhere writable (the source dir is
    # read-only system Blender). The output bundle carries the LUTs for validate().
    with tempfile.NamedTemporaryFile("w", suffix=".ocio", delete=False) as tf:
        tf.write(txt)
        tmp = Path(tf.name)
    try:
        c = ocio.Config.CreateFromFile(str(tmp))   # warns per dropped 2.5 key
        c.setMajorVersion(2)
        c.setMinorVersion(4)
        c.validate()
        return c.serialize()
    finally:
        tmp.unlink(missing_ok=True)


def copy_luts(src: Path, out: Path, config_text: str) -> list[str]:
    """Copy every search_path dir referenced by the config from src to out."""
    dirs = []
    for line in config_text.splitlines():
        s = line.strip()
        if s.startswith("search_path:"):
            raw = s.split(":", 1)[1].strip().strip('"')
            dirs = [d for d in raw.replace(":", "\n").split("\n") if d]
            break
    if not dirs:
        dirs = ["luts", "filmic", "icc"]   # Blender's standard bundle dirs
    copied = []
    for d in dirs:
        s, o = src / d, out / d
        if s.is_dir():
            if o.exists():
                shutil.rmtree(o)
            shutil.copytree(s, o)
            copied.append(d)
    return copied


def validate(out: Path) -> bool:
    """Reload the built config; assert warning-free load + graded processors build."""
    ocio = _ocio()
    buf = io.StringIO()
    with redirect_stderr(buf):
        c = ocio.Config.CreateFromFile(str(out / "config.ocio"))
        c.validate()
        for v in GRADED_VIEWS:
            p = c.getProcessor(ocio.ROLE_SCENE_LINEAR, "sRGB", v,
                               ocio.TRANSFORM_DIR_FORWARD)
            p.getDefaultCPUProcessor()
    warns = [ln for ln in buf.getvalue().splitlines() if "Warning" in ln]
    print(f"  version: {c.getMajorVersion()}.{c.getMinorVersion()}   "
          f"colorspaces: {len(list(c.getColorSpaces()))}   "
          f"view_transforms: {len(list(c.getViewTransforms()))}")
    print(f"  graded view processors built: {', '.join(GRADED_VIEWS)}")
    if warns:
        print(f"  ✗ {len(warns)} load warning(s) — NOT 2.4-native clean:")
        for w in warns[:6]:
            print(f"      {w}")
        return False
    print("  ✓ loads warning-free (genuinely 2.4-native — no ignored 2.5 constructs)")
    return True


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Build the v2.4-native OCIO parity config (Phase 60sq2.8).")
    ap.add_argument("--source", default=None, help="Blender colormanagement dir (default: auto-detect)")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help=f"output bundle dir (default: {DEFAULT_OUT})")
    ap.add_argument("--validate-only", action="store_true", help="validate an existing --out bundle")
    args = ap.parse_args(argv)
    out = Path(args.out)

    if args.validate_only:
        if not (out / "config.ocio").exists():
            print(f"RESULT: FAIL — no config.ocio under {out}"); return 2
        ok = validate(out)
        print("RESULT:", "PASS" if ok else "FAIL")
        return 0 if ok else 1

    src = find_source(args.source)
    print(f"source: {src}")
    native = to_native_2_4(src / "config.ocio")
    out.mkdir(parents=True, exist_ok=True)
    (out / "config.ocio").write_text(native)
    copied = copy_luts(src, out, native)
    print(f"built:  {out}/config.ocio  ({native.count(chr(10))} lines)")
    print(f"        LUT dirs copied: {', '.join(copied) or '(none)'}")
    ok = validate(out)
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
