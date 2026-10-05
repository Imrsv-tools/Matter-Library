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
# The masters step reads the MATTER_MASTERS_* switches (the head of Scripts/build_masters.py
# lists them). They are for a SECOND project building the masters for its own meshes. The
# runtime packaged and published from here is built with none of them set.
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
  # A good build is BOTH an exit code of 0 and the builder's own last line. Neither alone is
  # enough, and which one catches a refused switch depends on the project:
  #   - In a second project on Unreal 5.8 the commandlet exited 0 and printed "Python script
  #     executed successfully" after the script raised (2026-10-05). Only the result line saw it.
  #   - In this project on Unreal 5.8.0 the same refusal made the commandlet exit 255
  #     (2026-10-05). Only the exit code saw it.
  # The builder's lines ("told …", "built …", "RESULT ok") reach the output only with
  # -FullStdOutLogOutput (seen in both). The exit code is taken here, not left to `set -e`, so
  # that both routes end in one message and the log is removed.
  local log status=0 result="did not report"
  log="$(mktemp)"
  nice -n 19 "$UE/Engine/Binaries/Linux/UnrealEditor-Cmd" "$PROJECT" -run=pythonscript \
    -script="$HERE/MatterRuntime/Scripts/build_masters.py" \
    -EnablePlugins=PythonScriptPlugin,EditorScriptingUtilities -unattended -nullrhi -stdout \
    -FullStdOutLogOutput | tee "$log" || status=$?
  if grep -q "MATTER RESULT ok" "$log"; then result="reported"; fi
  if [ "$status" -ne 0 ] || [ "$result" != "reported" ]; then
    echo "masters: FAILED. The commandlet exited $status and the builder $result 'MATTER RESULT ok' (its output is above)." >&2
    rm -f "$log"
    exit 1
  fi
  echo "masters: ok. $(grep -o 'MATTER told .*' "$log" | tail -1)"
  rm -f "$log"
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
