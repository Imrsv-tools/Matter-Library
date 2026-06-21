#!/usr/bin/env bash
# build-usd-tools.sh — IMRSV canonical USD validation/authoring toolchain.
#
# Builds OpenUSD v26.03 (Stage's exact pin, IMRSV_Stage/cmake/ExternalUSD.cmake GIT_TAG)
# with the dev/tool capabilities Stage deliberately strips out flipped ON:
#   --python --usd-imaging --usdview --tools --materialx
# MaterialX rides USD's own 1.39.5 (same minor as Stage's vendored third_party/MaterialX
# 1.39.5 — OpenPBR-1.39 nodedefs identical). For BYTE-exact MaterialX, see NOTE below.
#
# Faithful-to-Stage rationale: usdview must render .mtlx the way Stage READS it. Same USD
# version + same MaterialX minor => trustworthy parity proof.
#
# Run from INSIDE the host conda env (see environment.yml):
#   conda activate imrsv-usd-tools && bash build-usd-tools.sh
#
# Idempotent: re-running resumes (clone + build_usd.py both skip done work; the GLSL fix
# below is grep-guarded). Reversible: rm -rf "$USD_TOOLS_ROOT".
#
# Override the install location with USD_TOOLS_ROOT (default ~/usd-tools).
set -euo pipefail

ROOT="${USD_TOOLS_ROOT:-${HOME}/usd-tools}"
SRC="${ROOT}/src/OpenUSD"
INST="${ROOT}/inst/usd-26.03"
USD_TAG="v26.03"
JOBS="${USD_BUILD_JOBS:-8}"

mkdir -p "${ROOT}/src" "${ROOT}/inst"

# --- 1. OpenUSD v26.03 source (shallow, the exact tag Stage pins) -----------------
if [ ! -d "${SRC}/.git" ]; then
  echo "[usd-tools] cloning OpenUSD ${USD_TAG} ..."
  git clone --branch "${USD_TAG}" --depth 1 \
    https://github.com/PixarAnimationStudios/OpenUSD.git "${SRC}"
else
  echo "[usd-tools] OpenUSD source present at ${SRC}"
fi

# --- 1b. Pin MaterialX to 1.39.5 (faithful + gcc-16-safe) -------------------------
# Stage vendors MaterialX 1.39.5; build_usd.py defaults to 1.39.3, whose
# MaterialXGenShader/HwShaderGenerator.cpp fails under gcc 16 ('Classification::BSDF
# is not a member' — that file was refactored into MaterialXGenHw in 1.39.4+).
# Idempotent: no-ops once already 1.39.5.
sed -i 's#MaterialX/archive/v1\.39\.3\.zip#MaterialX/archive/v1.39.5.zip#' \
  "${SRC}/build_scripts/build_usd.py"
echo "[usd-tools] MaterialX pin: $(grep -o 'MaterialX/archive/v[0-9.]*\.zip' "${SRC}/build_scripts/build_usd.py")"

# --- 2. Build USD + deps + tools via USD's own orchestrator ------------------------
# build_usd.py fetches+builds boost/tbb/opensubdiv/etc, then USD itself. --usdview
# implies --python --imaging. PySide6 + PyOpenGL come from the conda env.
# Conda's python ships only the SHARED libpython (.so), but build_usd.py introspects
# sysconfig and forces Python3_LIBRARY=libpython3.12.a (static, absent) -> FindPython3
# fails. Override with the real shared lib, derived from the active env (reproducible).
PYLIB="$(python -c 'import sysconfig,glob,os; d=sysconfig.get_config_var("LIBDIR"); print(sorted(glob.glob(os.path.join(d,"libpython3.*.so")))[0])')"
echo "[usd-tools] forcing shared Python lib: ${PYLIB}"

echo "[usd-tools] building into ${INST} (jobs=${JOBS}) ..."
python "${SRC}/build_scripts/build_usd.py" \
  --materialx \
  --usd-imaging \
  --usdview \
  --tools \
  --python \
  --no-examples \
  --no-tutorials \
  --no-tests \
  --no-docs \
  --build-args "USD,-DPython3_LIBRARY=${PYLIB} -DPXR_PY_UNDEFINED_DYNAMIC_LOOKUP=OFF" \
  -j "${JOBS}" \
  "${INST}"

# --- 3. Render fix: define AIRY_FRESNEL_ITERATIONS in the MaterialX GLSL lib -------
# USD v26.03's HdStMaterialXShaderGen::emitPixelStage() (pxr/imaging/hdSt/materialXShaderGen.cpp)
# is hand-copied from an OLDER MaterialX and omits the `#define AIRY_FRESNEL_ITERATIONS`
# that MaterialX 1.39.5's own GlslShaderGenerator emits. The thin-film Airy loops in
# pbrlib/genglsl/lib/mx_microfacet_specular.glsl then reference an undefined macro, the
# OpenPBR fragment shader fails to compile, and Storm draws EVERY material unshaded/white.
# Inject the macro (MaterialX default hwAiryFresnelIterations = 2) behind an #ifndef guard.
# Grep-guarded => idempotent. (Render-only; does NOT touch data parity. macOS/Metal uses the
# MSL generator instead — if Storm-on-Metal shows the same symptom, apply the analogous
# define in the genmsl lib. The clean upstream fix is in USD C++ emitPixelStage.)
GLSL="${INST}/libraries/pbrlib/genglsl/lib/mx_microfacet_specular.glsl"
if [ -f "${GLSL}" ] && ! grep -q 'AIRY_FRESNEL_ITERATIONS 2' "${GLSL}"; then
  echo "[usd-tools] applying AIRY_FRESNEL_ITERATIONS GLSL fix -> ${GLSL}"
  cp "${GLSL}" "${GLSL}.orig"
  printf '#ifndef AIRY_FRESNEL_ITERATIONS\n#define AIRY_FRESNEL_ITERATIONS 2\n#endif\n' > "${GLSL}.tmp"
  cat "${GLSL}" >> "${GLSL}.tmp"
  mv "${GLSL}.tmp" "${GLSL}"
fi

echo "[usd-tools] BUILD COMPLETE -> ${INST}"
echo "[usd-tools] activate with: source $(dirname "$0")/activate-usd-tools.sh"
echo "[usd-tools] verify: usdview --help ; usdrecord --help ; python -c 'import MaterialX,pxr.UsdMtlx;print(MaterialX.__version__)'"

# NOTE (byte-exact MaterialX, if ever needed): instead of --materialx, pre-build the
# vendored tree (IMRSV_Stage/third_party/MaterialX, MATERIALX_BUILD_PYTHON=ON) and pass
# --build-args USD,"-DMaterialX_DIR=<prefix>/lib/cmake/MaterialX -DPXR_ENABLE_MATERIALX_SUPPORT=TRUE".
# Same-minor (1.39.x) is parity-faithful for OpenPBR rendering, so default uses USD's.
