#!/usr/bin/env bash
# Creator Asset Profile — REAL-EXPORTER conformance gate (Phase 60sq1, Steps 1 + E8 §1/§2).
#
#   check_exporter.sh [OUT_DIR]
#
# Proves the SHIPPING Blender add-on (not the hand-authored golden) emits a conforming
# lightweight Open Matter Creator asset, through its selected-only / geometry+bindings-only
# output boundary, across THREE Creator scenarios:
#   distinct — two separate datablocks, sparse per-instance tint (different-settings path)
#   shared   — two meshes share ONE datablock -> exporter SPLITS to per-mesh instance prims (§2)
#   renamed  — datablock renamed off its identity, durable property carries identity (§1)
# Each scenario runs: real export -> assert_profile lightweight -> usdchecker + usdcat --flatten
# -> pxr binding-resolution + instance-uniqueness + identity check.
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
EXPECT_ID="Copper_Verdigris_Aged_Base_s01_v01"   # every scenario resolves to the ONE Copper identity
mkdir -p "$OUT"
rc=0

export PYTHONPATH="$INST/lib/python"
export LD_LIBRARY_PATH="$INST/lib:$ENVP/lib"
export PXR_MTLX_STDLIB_SEARCH_PATHS="$INST/libraries"
export PATH="$INST/bin:$PATH"
ROOTS=$(find "$MATROOT" -name '*.mtlx' -printf '%h\n' | sort -u | paste -sd: -)
export PXR_AR_DEFAULT_SEARCH_PATH="$ROOTS"

run_scenario() {
  MODE="$1"
  USDA="$OUT/creator_copper_${MODE}.usda"
  echo ""
  echo "======== SCENARIO: $MODE ========"
  echo "### 1. Real add-on export (blender --background -> export_lcd_usd, mode=$MODE)"
  # Blender uses its OWN bundled USD/MaterialX — strip the from-source USD-tools env (which the
  # pxr checks below need) or Blender's libusd_ms.so crashes on a MaterialX symbol mismatch.
  if env -u LD_LIBRARY_PATH -u PYTHONPATH -u PXR_MTLX_STDLIB_SEARCH_PATHS -u PXR_AR_DEFAULT_SEARCH_PATH \
          blender --background "$BLEND" --python "$CONF/export_copper_slice.py" -- "$USDA" --mode "$MODE" \
          > "$OUT/export_${MODE}.log" 2>&1 && grep -q SLICE_EXPORT_OK "$OUT/export_${MODE}.log"; then
    echo "  export: OK -> $USDA"
  else
    echo "  export: FAIL"; tail -15 "$OUT/export_${MODE}.log"; rc=1; return
  fi

  echo "### 2. Profile asserts (shape + spec-derived negative guards)"
  "$PY" "$CONF/assert_profile.py" lightweight "$USDA" || rc=1

  echo "### 3. usdchecker + usdcat --flatten (composition proof, library-resolved)"
  usdchecker "$USDA" && echo "  usdchecker: Success" || { echo "  usdchecker: FAIL"; rc=1; }
  if usdcat --flatten "$USDA" -o "$OUT/flat_${MODE}.usda" 2>"$OUT/${MODE}.err"; then
    echo "  usdcat --flatten: OK  shaders=$(grep -c 'def Shader' "$OUT/flat_${MODE}.usda")"
  else
    echo "  usdcat --flatten: FAIL"; cat "$OUT/${MODE}.err"; rc=1
  fi

  echo "### 4. Binding resolution + instance-uniqueness + identity (pxr)"
  EXPECT_ID="$EXPECT_ID" "$PY" - "$USDA" <<'PYEOF' || rc=1
import os, sys
from pxr import Usd, UsdShade
st = Usd.Stage.Open(sys.argv[1])
want = os.environ["EXPECT_ID"]
bound, unresolved, nosurf, badid = [], [], [], []
for p in st.Traverse():
    if p.GetTypeName() != "Mesh":
        continue
    m = UsdShade.MaterialBindingAPI(p).GetDirectBinding().GetMaterial()
    if not (m and m.GetPrim().IsValid()):
        unresolved.append(p.GetName()); continue
    bound.append(m.GetPath())
    if not m.ComputeSurfaceSource("mtlx")[0]:
        nosurf.append(p.GetName())
    ident = m.GetPrim().GetAssetInfoByKey("identifier")
    if ident != want:
        badid.append("%s->%r" % (p.GetName(), ident))
uniq = (len(set(bound)) == len(bound))
ok = not unresolved and not nosurf and not badid and uniq and len(bound) >= 2
print("  [%s] every mesh binding resolves to a valid material prim%s"
      % ("PASS" if not unresolved else "FAIL", "" if not unresolved else " — dangling: %s" % unresolved))
print("  [%s] each mesh binds a DISTINCT material instance prim (rule 6 / §2 split)%s"
      % ("PASS" if uniq else "FAIL", "" if uniq else " — bound paths %s" % [str(b) for b in bound]))
print("  [%s] each bound material exposes an mtlx surface source%s"
      % ("PASS" if not nosurf else "FAIL", "" if not nosurf else " — no surface: %s" % nosurf))
print("  [%s] every instance carries assetInfo:identifier == %r (§1 durable carrier)%s"
      % ("PASS" if not badid else "FAIL", want, "" if not badid else " — mismatched: %s" % badid))
print("  => bindings: %s (%d meshes)" % ("OK" if ok else "VIOLATION", len(bound)))
sys.exit(0 if ok else 1)
PYEOF
}

run_scenario distinct
run_scenario shared
run_scenario renamed

echo ""
echo "======== SELECTION-CONTEXT REGRESSION (E9 §15d) ========"
echo "### §2 split must fire even when context.selected_objects is incomplete (File-browser bug)"
if env -u LD_LIBRARY_PATH -u PYTHONPATH -u PXR_MTLX_STDLIB_SEARCH_PATHS -u PXR_AR_DEFAULT_SEARCH_PATH \
        blender --background --factory-startup --python "$CONF/test_export_selection.py" \
        -- "$OUT/creator_selection_regression.usda" > "$OUT/selection_reg.log" 2>&1; then
  grep -E "^REG:" "$OUT/selection_reg.log"
else
  echo "  selection regression FAIL"; grep -E "^REG:" "$OUT/selection_reg.log" || tail -10 "$OUT/selection_reg.log"; rc=1
fi

echo ""
echo "### REAL-EXPORTER GATE $([ $rc -eq 0 ] && echo PASS || echo FAIL) (rc=$rc)"
exit $rc
