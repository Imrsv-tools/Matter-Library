#!/usr/bin/env bash
# Creator Asset Profile conformance gate (Phase 60sq1, Step 1).
#
#   check_conformance.sh [OUT_DIR]
#
# Proves the hand-authored golden conforms to the Creator Asset Profile in BOTH forms:
#   1. rebuild the complete-portable package (deterministic, from the lightweight golden)
#   2. usdchecker Success + usdcat --flatten composes  — lightweight (WITH library search
#      path) AND portable (with NO search path -> proves independent open)
#   3. assert_profile.py — profile SHAPE + the spec-derived NEGATIVE guards, both forms
#   4. usdrecord eyes-on render of BOTH forms (DomeLight harness kept OUT of the golden)
#
# Exit 0 iff every check passes. See Contract/CreatorAssetProfile.md.
set -uo pipefail
INST=/home/peter/usd-tools/inst/usd-26.03
ENVP=/home/peter/.conda/envs/imrsv-usd-tools
CONF=/home/peter/Documents/IMRSV_GITrepos/IMRSV_Platform/Matter-Library/tools/conformance
GOLDEN="$CONF/golden"
MATROOT=/home/peter/Documents/IMRSV_GITrepos/IMRSV_Platform/Matter-Library/MatterLibrary/materials
OUT="${1:-/home/peter/.claude/jobs/71b4820d/tmp/p60_conformance}"
PY="$ENVP/bin/python"
mkdir -p "$OUT"
rc=0

export PYTHONPATH="$INST/lib/python"
export LD_LIBRARY_PATH="$INST/lib:$ENVP/lib"
export PXR_MTLX_STDLIB_SEARCH_PATHS="$INST/libraries"
export PATH="$INST/bin:$PATH"
ROOTS=$(find "$MATROOT" -name '*.mtlx' -printf '%h\n' | sort -u | paste -sd: -)

echo "### 1. Rebuild complete-portable package"
"$PY" "$CONF/build_portable.py" || rc=1

echo ""
echo "### 2. usdchecker + usdcat --flatten (composition proof)"
echo "-- lightweight (library-resolved; $(echo "$ROOTS" | tr ':' '\n' | wc -l) leaf-dir search roots) --"
export PXR_AR_DEFAULT_SEARCH_PATH="$ROOTS"
usdchecker "$GOLDEN/creator_table_lightweight.usda" && echo "  usdchecker: Success" || { echo "  usdchecker: FAIL"; rc=1; }
if usdcat --flatten "$GOLDEN/creator_table_lightweight.usda" -o "$OUT/lightweight_flat.usda" 2>"$OUT/lightweight.err"; then
  echo "  usdcat --flatten: OK  shaders=$(grep -c 'def Shader' "$OUT/lightweight_flat.usda")"
else
  echo "  usdcat --flatten: FAIL"; cat "$OUT/lightweight.err"; rc=1
fi
echo "-- portable (NO search path -> independent open) --"
unset PXR_AR_DEFAULT_SEARCH_PATH
( cd "$GOLDEN/creator_table_portable" && usdchecker creator_table_portable.usda ) && echo "  usdchecker: Success" || { echo "  usdchecker: FAIL"; rc=1; }
if ( cd "$GOLDEN/creator_table_portable" && usdcat --flatten creator_table_portable.usda -o "$OUT/portable_flat.usda" 2>"$OUT/portable.err" ); then
  echo "  usdcat --flatten: OK  shaders=$(grep -c 'def Shader' "$OUT/portable_flat.usda")"
else
  echo "  usdcat --flatten: FAIL"; cat "$OUT/portable.err"; rc=1
fi

echo ""
echo "### 3. Profile asserts (shape + spec-derived negative guards)"
export PXR_AR_DEFAULT_SEARCH_PATH="$ROOTS"
echo "-- lightweight --"
"$PY" "$CONF/assert_profile.py" lightweight "$GOLDEN/creator_table_lightweight.usda" || rc=1
echo "-- portable --"
"$PY" "$CONF/assert_profile.py" portable "$GOLDEN/creator_table_portable/creator_table_portable.usda" || rc=1

echo ""
echo "### 4. usdrecord eyes-on render (both forms)"
# usdrecord builds its GL context through Qt (needs xcb/GLX + a live display). Inherit an
# interactive session's env; else attach to the running Xwayland :0 with its discovered
# xauth cookie (so the gate renders from a headless background job too).
export QT_QPA_PLATFORM="xcb"
export QT_XCB_GL_INTEGRATION="glx"
export DISPLAY="${DISPLAY:-:0}"
if [ -z "${XAUTHORITY:-}" ]; then
  _xa=$(ls -t /run/user/$(id -u)/xauth_* 2>/dev/null | head -1)
  [ -n "$_xa" ] && export XAUTHORITY="$_xa"
fi
# lightweight harness: subLayer the golden + add a DomeLight (light kept OUT of the golden).
cat > "$OUT/harness_lightweight.usda" <<H
#usda 1.0
(
    subLayers = [@$GOLDEN/creator_table_lightweight.usda@]
)
def DomeLight "Key"
{
    float inputs:intensity = 1500
}
H
cat > "$GOLDEN/creator_table_portable/harness_portable.usda" <<H
#usda 1.0
(
    subLayers = [@creator_table_portable.usda@]
)
def DomeLight "Key"
{
    float inputs:intensity = 1500
}
H
export PXR_AR_DEFAULT_SEARCH_PATH="$ROOTS"
if "$PY" "$INST/bin/usdrecord" --complexity high --renderer GL "$OUT/harness_lightweight.usda" "$OUT/render_lightweight.png" 2>"$OUT/render_lightweight.log"; then
  echo "  lightweight render: $OUT/render_lightweight.png ($(stat -c%s "$OUT/render_lightweight.png" 2>/dev/null) bytes)"
else
  echo "  lightweight render: FAIL (see render_lightweight.log)"; tail -5 "$OUT/render_lightweight.log"; rc=1
fi
unset PXR_AR_DEFAULT_SEARCH_PATH
if ( cd "$GOLDEN/creator_table_portable" && "$PY" "$INST/bin/usdrecord" --complexity high --renderer GL harness_portable.usda "$OUT/render_portable.png" 2>"$OUT/render_portable.log" ); then
  echo "  portable render:    $OUT/render_portable.png ($(stat -c%s "$OUT/render_portable.png" 2>/dev/null) bytes)"
else
  echo "  portable render: FAIL (see render_portable.log)"; tail -5 "$OUT/render_portable.log"; rc=1
fi
rm -f "$GOLDEN/creator_table_portable/harness_portable.usda"

echo ""
echo "### CONFORMANCE GATE $([ $rc -eq 0 ] && echo PASS || echo FAIL) (rc=$rc)"
exit $rc
