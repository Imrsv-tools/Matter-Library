#!/usr/bin/env bash
# run-all.sh — one-shot: ensure the host env, then build.
# Backgroundable; logs to "$USD_TOOLS_ROOT/build.log". Reversible (see build-usd-tools.sh).
#
# The host env only pins Python 3.12 + cmake 3.28 (a box's own may be too new for the
# OpenUSD deps) and the Python packages usdview/usdrecord need; the build uses the SYSTEM
# compiler + system GL/X dev libs. With conda on PATH it is the conda env from
# environment.yml; without it, a uv venv at "$USD_TOOLS_ROOT/venv" with the same pins.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="${USD_TOOLS_ROOT:-${HOME}/usd-tools}"
ENVNAME="imrsv-usd-tools"
mkdir -p "${ROOT}"
LOG="${ROOT}/build.log"
exec > >(tee -a "${LOG}") 2>&1
echo "[run-all] $(date -u) starting (USD_TOOLS_ROOT=${ROOT})"

if command -v conda >/dev/null; then
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
else
  # The same pins as environment.yml (keep the two in step); git comes from the system.
  VENV="${ROOT}/venv"
  if [ ! -x "${VENV}/bin/python" ]; then
    echo "[run-all] no conda: creating uv venv ${VENV}"
    uv venv --python 3.12 "${VENV}"
  fi
  uv pip install --python "${VENV}/bin/python" "cmake==3.28.*" ninja pyside6 pyopengl \
    numpy pyyaml jinja2 "MaterialX==1.39.5"
  source "${VENV}/bin/activate"
fi
echo "[run-all] launching build (system compiler: $(c++ --version 2>/dev/null | head -1))"
USD_TOOLS_ROOT="${ROOT}" bash "${HERE}/build-usd-tools.sh"
echo "[run-all] $(date -u) DONE — activate with: source ${HERE}/activate-usd-tools.sh"
