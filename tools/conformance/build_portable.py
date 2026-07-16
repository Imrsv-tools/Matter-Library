#!/usr/bin/env python3
"""Materialize the COMPLETE-PORTABLE golden from the lightweight golden + the Matter Library.

Phase 60sq1, Step 1 (Creator Asset Profile). The complete-portable form (RD-4 / Goal
§6) is the explicit, self-contained option: the required Matter .mtlx and its texture set
are materialized ONCE into the package, and every reference is rewritten portable-relative,
so the package opens and renders in a reference app with NO PXR_AR_DEFAULT_SEARCH_PATH and
no access to the installed Matter Library.

pxr-free by design (file copy + MaterialX-text rewrite only) — mirrors the frozen v1
producer mechanism (Step 7). Deterministic: same inputs -> byte-identical package.

Layout produced (under golden/creator_table_portable/):
    creator_table_portable.usda                 # references ./Copper_...mtlx (relative)
    Copper_Verdigris_Aged_Base_s01_v01.mtlx     # texture refs rewritten -> ./textures/<name>
    textures/<name>.png                         # the 7 required texture files, flattened
"""
import re
import shutil
from pathlib import Path

REPO = Path("/home/peter/Documents/IMRSV_GITrepos/IMRSV_Platform")
MATLIB = REPO / "Matter-Library" / "MatterLibrary"
CONF = REPO / "Matter-Library" / "tools" / "conformance"
GOLDEN = CONF / "golden"

MATERIAL_STEM = "Copper_Verdigris_Aged_Base_s01_v01"
SRC_MTLX = MATLIB / "materials" / "engineered" / "metal" / f"{MATERIAL_STEM}.mtlx"
LIGHTWEIGHT = GOLDEN / "creator_table_lightweight.usda"

PKG = GOLDEN / "creator_table_portable"
PKG_TEX = PKG / "textures"


def main() -> None:
    # Clean rebuild for determinism.
    if PKG.exists():
        shutil.rmtree(PKG)
    PKG_TEX.mkdir(parents=True)

    mtlx_text = SRC_MTLX.read_text()

    # Collect + flatten every texture filename referenced by the .mtlx, copy it in,
    # and rewrite the reference to the portable ./textures/<basename> form.
    copied: dict[str, str] = {}
    for m in re.finditer(r'name="file" type="filename" value="([^"]+)"', mtlx_text):
        ref = m.group(1)
        base = Path(ref).name
        src = (SRC_MTLX.parent / ref).resolve()
        if not src.is_file():
            raise SystemExit(f"MISSING texture referenced by .mtlx: {src}")
        if base not in copied:
            shutil.copy2(src, PKG_TEX / base)
            copied[base] = ref
        mtlx_text = mtlx_text.replace(f'value="{ref}"', f'value="textures/{base}"')

    (PKG / f"{MATERIAL_STEM}.mtlx").write_text(mtlx_text)

    # Portable .usda = the lightweight golden with the BARE library ref rewritten to the
    # LOCAL relative .mtlx. Everything else (geometry, UVs, identity, release key) identical.
    usda = LIGHTWEIGHT.read_text()
    usda = usda.replace(
        "# The minimal, independently-intelligible exemplar of an Open Matter Creator\n"
        "    # asset in its lightweight (library-linked) form.",
        "# The minimal, independently-intelligible exemplar of an Open Matter Creator\n"
        "    # asset in its COMPLETE-PORTABLE (self-contained) form.",
    )
    usda = usda.replace(
        f"@{MATERIAL_STEM}.mtlx@",
        f"@./{MATERIAL_STEM}.mtlx@",
    )
    (PKG / "creator_table_portable.usda").write_text(usda)

    print(f"portable package: {PKG}")
    print(f"  materialized .mtlx: {MATERIAL_STEM}.mtlx  ({len(copied)} textures flattened)")
    for base in sorted(copied):
        print(f"    textures/{base}")


if __name__ == "__main__":
    main()
