#!/usr/bin/env bash
# run-all.sh — one-shot: ensure the conda host env (from environment.yml), then build.
# Backgroundable; logs to "$USD_TOOLS_ROOT/build.log". Reversible (see build-usd-tools.sh).
#
# The host env isolates system Python/cmake/gcc mismatches while using the SYSTEM compiler
# + system GL/X dev libs (so OpenGL/X headers resolve without a conda sysroot).
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="${USD_TOOLS_ROOT:-${HOME}/usd-tools}"
ENVNAME="imrsv-usd-tools"
mkdir -p "${ROOT}"
LOG="${ROOT}/build.log"
exec > >(tee -a "${LOG}") 2>&1
echo "[run-all] $(date -u) starting (USD_TOOLS_ROOT=${ROOT})"

# Activate conda in this non-interactive shell (avoids the `conda run` __conda_exe quirk
# seen on some boxes — we activate the env and run in-process instead).
source "$(conda info --base)/etc/profile.d/conda.sh"

if ! conda env list | grep -qE "^${ENVNAME}\s"; then
  echo "[run-all] creating conda env ${ENVNAME} from environment.yml"
  conda env create -f "${HERE}/environment.yml"
else
  echo "[run-all] conda env ${ENVNAME} already present"
fi

conda activate "${ENVNAME}"
echo "[run-all] launching build (system gcc=$(gcc -dumpversion 2>/dev/null))"
USD_TOOLS_ROOT="${ROOT}" bash "${HERE}/build-usd-tools.sh"
echo "[run-all] $(date -u) DONE — activate with: source ${HERE}/activate-usd-tools.sh"
