#!/usr/bin/env bash
# Build the Matter Unreal runtime from this repo's sources (Phase06). Needs Unreal Engine 5.8.
#
#   UE=/path/to/Unreal_5.8 unreal/build.sh [editor|masters|package|all]
#
#   editor   the C++ editor target (capped jobs, nice)                    — CPU
#   masters  the masters, by commandlet with no GPU (-nullrhi)             — CPU
#   package  cook + a Shipping build, stripped, archived to
#            unreal/dist/MatterRuntime-Linux.tar.gz                        — CPU
#   all      editor, masters, package (default)
#
# Every Unreal asset is generated here; none is committed (UR-F5). Publishing the archive is
# its own command, unreal/publish.sh (Phase06 D2, D14).
set -euo pipefail

: "${UE:?set UE to an Unreal Engine 5.8 install}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="$HERE/MatterRuntime/MatterRuntime.uproject"
JOBS="${MATTER_UE_JOBS:-8}"     # this machine also builds other Unreal projects: never uncapped
STEP="${1:-all}"
STAGED="$HERE/MatterRuntime/Packaged"
DIST="$HERE/dist"

editor() {
  nice -n 19 "$UE/Engine/Build/BatchFiles/Linux/Build.sh" MatterRuntimeEditor Linux Development \
    -Project="$PROJECT" -MaxParallelActions="$JOBS" -WaitMutex
}

masters() {
  nice -n 19 "$UE/Engine/Binaries/Linux/UnrealEditor-Cmd" "$PROJECT" -run=pythonscript \
    -script="$HERE/MatterRuntime/Scripts/build_masters.py" \
    -EnablePlugins=PythonScriptPlugin,EditorScriptingUtilities -unattended -nullrhi -stdout
}

package() {
  rm -rf "$STAGED"
  nice -n 19 "$UE/Engine/Build/BatchFiles/RunUAT.sh" BuildCookRun -project="$PROJECT" -noP4 \
    -platform=Linux -clientconfig=Shipping -build -cook -stage -pak -iostore -archive \
    -archivedirectory="$STAGED" -nodebuginfo -unattended -nocompileeditor \
    -ubtargs="-MaxParallelActions=$JOBS"
  # What a run does not need (UR-F8): debug symbols and the Vulkan debugging layers
  find "$STAGED/Linux" \( -name '*.debug' -o -name '*.sym' -o -name 'libVkLayer_*' -o -name 'VkLayer_*.json' \) -delete
  mkdir -p "$DIST"
  tar -C "$STAGED" -czf "$DIST/MatterRuntime-Linux.tar.gz" Linux
  du -sh "$STAGED/Linux" "$DIST/MatterRuntime-Linux.tar.gz"
}

case "$STEP" in
  editor) editor ;;
  masters) masters ;;
  package) package ;;
  all) editor; masters; package ;;
  *) echo "usage: $0 [editor|masters|package|all]" >&2; exit 2 ;;
esac
