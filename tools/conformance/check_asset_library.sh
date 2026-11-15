#!/usr/bin/env bash
# Creator Asset-Browser library — GENERATE + STRUCTURE gate (Phase 60sq1 E8 §5).
#
#   check_asset_library.sh [OUT_DIR]
#
# Proves the generator produces an installed Blender Asset-Browser library the Creator can
# browse/assign: gen_asset_library.py (on the scaffold) -> verify_asset_library.py (structure).
# The browse/assign UX itself is the §6 human sitting; this gate proves the STRUCTURE is right.
set -uo pipefail
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
GEN="$REPO/tools/generators/gen_asset_library.py"
VERIFY="$REPO/tools/conformance/verify_asset_library.py"
OUT="${1:-$(mktemp -d)/asset_library}"
mkdir -p "$OUT"
rc=0

# Blender uses its OWN bundled USD — run with a clean env (see check_exporter.sh).
CLEAN="env -u LD_LIBRARY_PATH -u PYTHONPATH -u PXR_MTLX_STDLIB_SEARCH_PATHS -u PXR_AR_DEFAULT_SEARCH_PATH"
# The Blender to run: $MATTER_BLENDER (the rig's and the thumbnails' variable), else `blender` on PATH.
BLENDER="${MATTER_BLENDER:-blender}"

echo "### 1. Generate the Asset-Browser library (blender --background --factory-startup -> gen_asset_library.py, every Creator-selectable article in the working tree)"
if $CLEAN "$BLENDER" --background --factory-startup --python "$GEN" -- "$OUT" > "$OUT/gen.log" 2>&1 \
        && grep -q ASSET_LIB_OK "$OUT/gen.log"; then
  echo "  generate: OK"; grep ASSET_LIB_OK "$OUT/gen.log"
else
  echo "  generate: FAIL"; tail -20 "$OUT/gen.log"; exit 1
fi

echo ""
echo "### 2. Structure verify (asset-marked + catalog + identity carrier + proxy)"
$CLEAN "$BLENDER" --background "$OUT/MatterLibrary.blend" --python "$VERIFY" > "$OUT/verify.log" 2>&1
grep -E '^\s*\[(PASS|FAIL)\]|=> asset-library' "$OUT/verify.log" || { cat "$OUT/verify.log"; rc=1; }
grep -q 'CONFORMS' "$OUT/verify.log" || rc=1

echo ""
echo "### 3. Blender version: the committed asset file vs this build (a warning, never a FAIL)"
# Copying this build over blender/asset_library/MatterLibrary.blend re-saves it in the running
# Blender; say so in the commit when that moves the version (Velvet's landing moved 5.2 -> 5.3
# inside a commit about velvet, 2026-11-15).
COMMITTED="$REPO/blender/asset_library/MatterLibrary.blend"
NOW="$(grep -o 'running [0-9][0-9.]*' "$OUT/verify.log" | head -1 | cut -d' ' -f2)"
if [ -f "$COMMITTED" ]; then
  WAS="$($CLEAN "$BLENDER" --background --factory-startup "$COMMITTED" \
        --python-expr 'import bpy; print("SAVED_BY %d.%d" % bpy.data.version[:2])' 2>/dev/null \
        | grep '^SAVED_BY' | cut -d' ' -f2)"
  echo "  committed file saved by Blender ${WAS:-?}; this build by ${NOW:-?}"
  if [ -n "$WAS" ] && [ -n "$NOW" ] && [ "$WAS" != "$(echo "$NOW" | cut -d. -f1-2)" ]; then
    echo "  WARN: copying this build in moves the committed file from Blender $WAS to ${NOW} — say so in the commit"
  fi
else
  echo "  no committed asset file to compare; this build by ${NOW:-?}"
fi

echo ""
echo "### ASSET-LIBRARY GATE $([ $rc -eq 0 ] && echo PASS || echo FAIL) (rc=$rc)"
exit $rc
