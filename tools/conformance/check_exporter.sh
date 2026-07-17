#!/usr/bin/env bash
# Creator Asset Profile — REAL-EXPORTER conformance gate (Phase 60sq1, Step 1).
#
#   check_exporter.sh [OUT_DIR]
#
# Proves the SHIPPING Blender add-on (not the hand-authored golden) emits a conforming
# lightweight Open Matter Creator asset, through its new selected-only / geometry+bindings-only
# output boundary:
#   1. blender --background -> export_copper_slice.py -> the real export_lcd_usd
#   2. assert_profile.py lightweight — profile SHAPE + spec-derived NEGATIVE guards
#   3. usdchecker Success + usdcat --flatten composes the material network (library-resolved)
#
# Exit 0 iff every check passes. Companion to check_conformance.sh (which validates the golden).
set -uo pipefail
INST=/home/peter/usd-tools/inst/usd-26.03
ENVP=/home/peter/.conda/envs/imrsv-usd-tools
REPO=/home/peter/Documents/IMRSV_GITrepos/IMRSV_Platform/Matter-Library
CONF="$REPO/tools/conformance"
BLEND="$REPO/blender/MatterMaterials.blend"
MATROOT="$REPO/MatterLibrary/materials"
PY="$ENVP/bin/python"
OUT="${1:-$(mktemp -d)}"
USDA="$OUT/creator_copper_slice.usda"
mkdir -p "$OUT"
rc=0

echo "### 1. Real add-on export (blender --background -> export_lcd_usd)"
if blender --background "$BLEND" --python "$CONF/export_copper_slice.py" -- "$USDA" \
        > "$OUT/export.log" 2>&1 && grep -q SLICE_EXPORT_OK "$OUT/export.log"; then
  echo "  export: OK -> $USDA"
else
  echo "  export: FAIL"; tail -15 "$OUT/export.log"; exit 1
fi

export PYTHONPATH="$INST/lib/python"
export LD_LIBRARY_PATH="$INST/lib:$ENVP/lib"
export PXR_MTLX_STDLIB_SEARCH_PATHS="$INST/libraries"
export PATH="$INST/bin:$PATH"
ROOTS=$(find "$MATROOT" -name '*.mtlx' -printf '%h\n' | sort -u | paste -sd: -)
export PXR_AR_DEFAULT_SEARCH_PATH="$ROOTS"

echo ""
echo "### 2. Profile asserts (shape + spec-derived negative guards)"
"$PY" "$CONF/assert_profile.py" lightweight "$USDA" || rc=1

echo ""
echo "### 3. usdchecker + usdcat --flatten (composition proof, library-resolved)"
usdchecker "$USDA" && echo "  usdchecker: Success" || { echo "  usdchecker: FAIL"; rc=1; }
if usdcat --flatten "$USDA" -o "$OUT/slice_flat.usda" 2>"$OUT/slice.err"; then
  echo "  usdcat --flatten: OK  shaders=$(grep -c 'def Shader' "$OUT/slice_flat.usda")"
else
  echo "  usdcat --flatten: FAIL"; cat "$OUT/slice.err"; rc=1
fi

echo ""
echo "### 4. Binding resolution + material-instance uniqueness (pxr)"
# Catches the duplicate-prim / dangling-binding class the text asserts CANNOT see: every mesh
# binding must resolve to a VALID material prim, each mesh must bind a DISTINCT prim (profile
# rule 6 independent instances), and each bound material must expose an mtlx surface source.
"$PY" - "$USDA" <<'PYEOF' || rc=1
import sys
from pxr import Usd, UsdShade
st = Usd.Stage.Open(sys.argv[1])
bound, unresolved, nosurf = [], [], []
for p in st.Traverse():
    if p.GetTypeName() != "Mesh":
        continue
    m = UsdShade.MaterialBindingAPI(p).GetDirectBinding().GetMaterial()
    if not (m and m.GetPrim().IsValid()):
        unresolved.append(p.GetName()); continue
    bound.append(m.GetPath())
    if not m.ComputeSurfaceSource("mtlx")[0]:
        nosurf.append(p.GetName())
uniq = (len(set(bound)) == len(bound))
ok = not unresolved and not nosurf and uniq and len(bound) >= 2
print("  [%s] every mesh binding resolves to a valid material prim%s"
      % ("PASS" if not unresolved else "FAIL", "" if not unresolved else " — dangling: %s" % unresolved))
print("  [%s] each mesh binds a DISTINCT material instance prim (rule 6)%s"
      % ("PASS" if uniq else "FAIL", "" if uniq else " — bound paths %s" % [str(b) for b in bound]))
print("  [%s] each bound material exposes an mtlx surface source%s"
      % ("PASS" if not nosurf else "FAIL", "" if not nosurf else " — no surface: %s" % nosurf))
print("  => bindings: %s (%d meshes)" % ("OK" if ok else "VIOLATION", len(bound)))
sys.exit(0 if ok else 1)
PYEOF

echo ""
echo "### REAL-EXPORTER GATE $([ $rc -eq 0 ] && echo PASS || echo FAIL) (rc=$rc)"
exit $rc
