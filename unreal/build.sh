#!/usr/bin/env bash
# Build the Matter Unreal runtime from this repo's sources (Phase06). Needs Unreal Engine 5.8.
#
#   UE=/path/to/Unreal_5.8 unreal/build.sh [editor|masters|all]
#
#   editor   the C++ editor target (capped jobs, nice)       — CPU
#   masters  the masters, by commandlet with no GPU (-nullrhi) — CPU
#   all      both (default)
#
# Every Unreal asset is generated here; none is committed (UR-F5). The package (cook, stripped
# Shipping build, archive) is added at Phase06 step 6.2.
set -euo pipefail

: "${UE:?set UE to an Unreal Engine 5.8 install}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="$HERE/MatterRuntime/MatterRuntime.uproject"
JOBS="${MATTER_UE_JOBS:-8}"     # this machine also builds other Unreal projects: never uncapped
STEP="${1:-all}"

editor() {
  nice -n 19 "$UE/Engine/Build/BatchFiles/Linux/Build.sh" MatterRuntimeEditor Linux Development \
    -Project="$PROJECT" -MaxParallelActions="$JOBS" -WaitMutex
}

masters() {
  nice -n 19 "$UE/Engine/Binaries/Linux/UnrealEditor-Cmd" "$PROJECT" -run=pythonscript \
    -script="$HERE/MatterRuntime/Scripts/build_masters.py" \
    -EnablePlugins=PythonScriptPlugin,EditorScriptingUtilities -unattended -nullrhi -stdout
}

case "$STEP" in
  editor) editor ;;
  masters) masters ;;
  all) editor; masters ;;
  *) echo "usage: $0 [editor|masters|all]" >&2; exit 2 ;;
esac
