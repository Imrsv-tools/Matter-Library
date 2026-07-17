#!/usr/bin/env bash
# Creator Asset-Browser library — GENERATE + STRUCTURE gate (Phase 60sq1 E8 §5).
#
#   check_asset_library.sh [OUT_DIR]
#
# Proves the generator produces an installed Blender Asset-Browser library the Creator can
# browse/assign: gen_asset_library.py (on the scaffold) -> verify_asset_library.py (structure).
# The browse/assign UX itself is the §6 human sitting; this gate proves the STRUCTURE is right.
set -uo pipefail
REPO=/home/peter/Documents/IMRSV_GITrepos/IMRSV_Platform/Matter-Library
GEN="$REPO/tools/generators/gen_asset_library.py"
VERIFY="$REPO/tools/conformance/verify_asset_library.py"
OUT="${1:-$(mktemp -d)/asset_library}"
mkdir -p "$OUT"
rc=0

# Blender uses its OWN bundled USD — run with a clean env (see check_exporter.sh).
CLEAN="env -u LD_LIBRARY_PATH -u PYTHONPATH -u PXR_MTLX_STDLIB_SEARCH_PATHS -u PXR_AR_DEFAULT_SEARCH_PATH"

echo "### 1. Generate the Asset-Browser library (blender --background --factory-startup -> gen_asset_library.py, all 11 articles)"
if $CLEAN blender --background --factory-startup --python "$GEN" -- "$OUT" > "$OUT/gen.log" 2>&1 \
        && grep -q ASSET_LIB_OK "$OUT/gen.log"; then
  echo "  generate: OK"; grep ASSET_LIB_OK "$OUT/gen.log"
else
  echo "  generate: FAIL"; tail -20 "$OUT/gen.log"; exit 1
fi

echo ""
echo "### 2. Structure verify (asset-marked + catalog + identity carrier + proxy)"
$CLEAN blender --background "$OUT/MatterLibrary.blend" --python "$VERIFY" > "$OUT/verify.log" 2>&1
grep -E '^\s*\[(PASS|FAIL)\]|=> asset-library' "$OUT/verify.log" || { cat "$OUT/verify.log"; rc=1; }
grep -q 'CONFORMS' "$OUT/verify.log" || rc=1

echo ""
echo "### ASSET-LIBRARY GATE $([ $rc -eq 0 ] && echo PASS || echo FAIL) (rc=$rc)"
exit $rc
