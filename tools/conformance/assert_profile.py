#!/usr/bin/env python3
"""Assert a USD asset conforms to the Creator Asset Profile (Phase 60sq1, Step 1).

    assert_profile.py <lightweight|portable> <asset.usda>

Text-based + directory-level (pxr-free) so it runs against ANY authored asset — including
the CURRENT whole-scene Blender export (which carries UsdPreviewSurface + a DomeLight +
absolute author paths) for a two-way RED demo. Composition/validity is proven separately by
usdchecker + usdcat --flatten (check_conformance.sh); this asserts the SHAPE the profile
pins, and — critically — a NEGATIVE assert derived from the spec's forbidden list (no
texture/.mtlx files of ANY kind beside a lightweight asset), not a Matter-basename allowlist.

Exit 0 = all checks PASS; exit 1 = any FAIL (each printed with a [PASS]/[FAIL] line).
Spec: IMRSV_Platform_Documentation/MatterLibrary/Contract/CreatorAssetProfile.md
"""
import re
import sys
from pathlib import Path

RELEASE = "matterlib-0.1.0"
NAME_RE = re.compile(r"^[A-Za-z0-9_]{1,63}$")
FORBIDDEN_TOKENS = [
    "UsdPreviewSurface",
    "PreviewSurface",
    "DomeLight",
    "def Camera",
    "def SphereLight",
    "def RectLight",
    "def DistantLight",
    "inputs:diffuseColor",  # UsdPreviewSurface tell
]
MATERIAL_TEX_EXTS = {".png", ".jpg", ".jpeg", ".exr", ".tga", ".tif", ".tiff", ".hdr", ".mtlx"}


def main() -> int:
    if len(sys.argv) != 3 or sys.argv[1] not in ("lightweight", "portable"):
        print(__doc__)
        return 2
    mode = sys.argv[1]
    usda = Path(sys.argv[2]).resolve()
    text = usda.read_text()
    # Comment-stripped copy for the token/path scans, so the asset's OWN documentation
    # comment (which names the forbidden tokens) can't self-trigger a false positive.
    nocomment = re.sub(r"(?m)^\s*#.*$", "", text)
    fails = 0

    def check(ok: bool, label: str, detail: str = "") -> None:
        nonlocal fails
        tag = "PASS" if ok else "FAIL"
        if not ok:
            fails += 1
        print(f"  [{tag}] {label}" + (f" — {detail}" if detail and not ok else ""))

    # 1. required Matter release recorded in customLayerData.
    m = re.search(r'string\s+"imrsv:matterlibRelease"\s*=\s*"([^"]+)"', text)
    check(bool(m) and m.group(1) == RELEASE, f"customLayerData imrsv:matterlibRelease == {RELEASE!r}",
          f"got {m.group(1) if m else 'ABSENT'}")

    # 2. every material-addressable region is a separate Mesh, each with exactly one binding.
    n_mesh = len(re.findall(r'\bdef Mesh\b', text))
    n_bind = len(re.findall(r'\brel material:binding\b', text))
    check(n_mesh >= 2 and n_mesh == n_bind, "each Mesh has one material:binding (>=2 regions)",
          f"{n_mesh} meshes vs {n_bind} bindings")

    # 3. every mesh carries geometry-authored UVs.
    n_st = len(re.findall(r'texCoord2f\[\]\s+primvars:st', text))
    check(n_st == n_mesh and n_st >= 2, "each Mesh has texCoord2f[] primvars:st",
          f"{n_st} st-primvars vs {n_mesh} meshes")

    # 3b. every mesh declares subdivisionScheme="none" (polygon, not a catmullClark cage).
    n_subdiv = len(re.findall(r'uniform token subdivisionScheme = "none"', text))
    check(n_subdiv == n_mesh, 'each Mesh declares subdivisionScheme = "none"',
          f"{n_subdiv} of {n_mesh} meshes")

    # 4. exact Matter identity carried on assetInfo:identifier (not the prim name).
    ids = re.findall(r'string\s+identifier\s*=\s*"([^"]+)"', text)
    id_ok = len(ids) == n_bind and all(NAME_RE.match(i) for i in ids)
    check(id_ok, "assetInfo:identifier on every material prim, <=63-char [A-Za-z0-9_]",
          f"{len(ids)} identifiers {ids}")

    # 5. material reference form (bare library ref vs local relative ref).
    refs = re.findall(r'references\s*=\s*@([^@]+)@', text)
    if mode == "lightweight":
        ok = bool(refs) and all(re.fullmatch(r'[A-Za-z0-9_]+\.mtlx', r) for r in refs)
        check(ok, "lightweight: bare @Name.mtlx@ library references only", f"refs={refs}")
    else:
        ok = bool(refs) and all(r.startswith("./") and r.endswith(".mtlx") for r in refs)
        check(ok, "portable: local @./Name.mtlx@ relative references only", f"refs={refs}")

    # 6. forbidden tokens absent (no preview-surface / lights / camera in the asset).
    present = [t for t in FORBIDDEN_TOKENS if t in nocomment]
    check(not present, "no UsdPreviewSurface / Light / Camera in the asset", f"found {present}")

    # 6b. no absolute author-machine paths anywhere.
    abs_paths = re.findall(r'(?:@|value=")(/[^@"\s]+)', nocomment)
    check(not abs_paths, "no absolute author-machine paths", f"found {abs_paths[:3]}")

    # 7. directory-level material-payload asserts (the NEGATIVE spec-derived guard).
    if mode == "lightweight":
        # The lightweight asset carries NO material payload of ANY kind beside it.
        # Scan its own dir tree, excluding any sibling complete-portable package.
        d = usda.parent
        stray = [p for p in d.rglob("*")
                 if p.is_file() and p.suffix.lower() in MATERIAL_TEX_EXTS
                 and "creator_table_portable" not in p.parts]
        check(not stray, "lightweight asset dir holds ZERO texture/.mtlx files of any kind",
              f"found {[p.name for p in stray[:5]]}")
    else:
        pkg = usda.parent
        stem = ids[0] if ids else ""
        has_mtlx = (pkg / f"{stem}.mtlx").is_file()
        tex = list((pkg / "textures").glob("*")) if (pkg / "textures").is_dir() else []
        check(has_mtlx and len(tex) >= 1,
              "portable package is self-contained (.mtlx + textures/ materialized)",
              f"mtlx={has_mtlx} textures={len(tex)}")

    print(f"  => {mode}: {'CONFORMS' if fails == 0 else f'{fails} VIOLATION(S)'}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
