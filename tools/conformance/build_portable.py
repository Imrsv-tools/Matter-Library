#!/usr/bin/env python3
"""Materialize the COMPLETE-PORTABLE golden from the lightweight golden + the Matter Library.

Phase 60sq1, Step 1 (Creator Asset Profile). The complete-portable form (RD-4 / Goal
§6) is the explicit, self-contained option: the required Matter .mtlx files and their texture
sets are materialized ONCE into the package, and every reference is rewritten portable-relative,
so the package opens and renders in a reference app with NO PXR_AR_DEFAULT_SEARCH_PATH and
no access to the installed Matter Library.

pxr-free by design (file copy + MaterialX-text rewrite only) — mirrors the frozen v1
producer mechanism (Step 7). Deterministic: same inputs -> byte-identical package.

Layout produced (under golden/creator_table_portable/):
    creator_table_portable.usda                 # references ./<article>.mtlx (relative)
    <article>.mtlx                              # one per article; texture refs -> ./textures/<name>
    textures/<name>.png                         # every required texture file, flattened

The articles (Phase19 19.4): Copper on the table, and the 1 m scale grid on the reference cube.
"""
import re
import shutil
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]  # this repo, from the script's own location
MATLIB = REPO / "MatterLibrary"
CONF = REPO / "tools" / "conformance"
GOLDEN = CONF / "golden"

ARTICLES = {
    "Copper_Verdigris_Aged_Base_s01_v01": MATLIB / "materials" / "engineered" / "metal",
    "Diagnostic_ScaleGrid_Clean_Base_s1_v01": MATLIB / "materials" / "utility" / "virtual",
}
LIGHTWEIGHT = GOLDEN / "creator_table_lightweight.usda"

PKG = GOLDEN / "creator_table_portable"
PKG_TEX = PKG / "textures"


def materialize(stem: str, folder: Path, copied: dict[str, Path]) -> None:
    """Copy one article into the package, its texture references flattened to ./textures/."""
    src_mtlx = folder / f"{stem}.mtlx"
    mtlx_text = src_mtlx.read_text()
    # Collect + flatten every texture filename referenced by the .mtlx, copy it in,
    # and rewrite the reference to the portable ./textures/<basename> form.
    for m in re.finditer(r'name="file" type="filename" value="([^"]+)"', mtlx_text):
        ref = m.group(1)
        base = Path(ref).name
        src = (src_mtlx.parent / ref).resolve()
        if not src.is_file():
            raise SystemExit(f"MISSING texture referenced by .mtlx: {src}")
        if copied.setdefault(base, src) != src:
            raise SystemExit(f"two different textures flatten to textures/{base}")
        if not (PKG_TEX / base).exists():
            shutil.copy2(src, PKG_TEX / base)
        mtlx_text = mtlx_text.replace(f'value="{ref}"', f'value="textures/{base}"')
    (PKG / f"{stem}.mtlx").write_text(mtlx_text)


def main() -> None:
    # Clean rebuild for determinism.
    if PKG.exists():
        shutil.rmtree(PKG)
    PKG_TEX.mkdir(parents=True)

    copied: dict[str, Path] = {}
    for stem, folder in ARTICLES.items():
        materialize(stem, folder, copied)

    # Portable .usda = the lightweight golden with each BARE library ref rewritten to the
    # LOCAL relative .mtlx. Everything else (geometry, UVs, identity, release key) identical.
    usda = LIGHTWEIGHT.read_text()
    usda = usda.replace(
        "# The minimal, independently-intelligible exemplar of an Open Matter Creator\n"
        "    # asset in its lightweight (library-linked) form.",
        "# The minimal, independently-intelligible exemplar of an Open Matter Creator\n"
        "    # asset in its COMPLETE-PORTABLE (self-contained) form.",
    )
    for stem in ARTICLES:
        usda = usda.replace(f"@{stem}.mtlx@", f"@./{stem}.mtlx@")
    (PKG / "creator_table_portable.usda").write_text(usda)

    print(f"portable package: {PKG}")
    for stem in ARTICLES:
        print(f"  materialized .mtlx: {stem}.mtlx")
    print(f"  {len(copied)} textures flattened")
    for base in sorted(copied):
        print(f"    textures/{base}")


if __name__ == "__main__":
    main()
