#!/usr/bin/env bash
# build-usd-tools.sh — the Matter Library's USD validation/authoring toolchain.
#
# Builds OpenUSD v26.03 — the library's USD baseline — with the dev/tool capabilities a lean
# runtime strips out flipped ON:
#   --python --usd-imaging --usdview --tools --materialx
# MaterialX rides USD's own 1.39.5 (the library's MaterialX baseline; OpenPBR-1.39 nodedefs).
# For BYTE-exact MaterialX against a particular consumer's vendored build, see NOTE below.
#
# Why these pins: usdview must render .mtlx the way a consumer READS it, so parity proofs need
# the same USD version and MaterialX minor. They were chosen (2026-06) to match the IMRSV Stage
# consumer's build. Whether the library's baseline leads and consumers declare a match, or the
# reverse, is open: docs/specs/Tooling/USDValidationToolchain.md (Drift, 2026-09-23).
#
# Run from INSIDE the host env (run-all.sh makes it: the conda env from environment.yml,
# or a uv venv where there is no conda):
#   conda activate imrsv-usd-tools && bash build-usd-tools.sh   (or: bash run-all.sh)
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
# Grep-guarded => idempotent. (-i.bak, then remove it: the one in-place form GNU and
# BSD/macOS sed both accept.)
if grep -q 'MaterialX/archive/v1\.39\.3\.zip' "${SRC}/build_scripts/build_usd.py"; then
  sed -i.bak 's#MaterialX/archive/v1\.39\.3\.zip#MaterialX/archive/v1.39.5.zip#' \
    "${SRC}/build_scripts/build_usd.py"
  rm -f "${SRC}/build_scripts/build_usd.py.bak"
fi
echo "[usd-tools] MaterialX pin: $(grep -o 'MaterialX/archive/v[0-9.]*\.zip' "${SRC}/build_scripts/build_usd.py")"

# --- 1c. Metal render fix: glslfx primvar type names (source patch) ------------------
# On macOS v26.03 writes a <texcoord>'s `st` primvar into the generated glslfx as MSL's
# `float2`, which the glslfx parser rejects, so Storm draws every such article as its
# fallback. patches/hdSt-glslfx-primvar-type.patch backports OpenUSD dev's fix (the type
# comes from the MaterialX type name); drop it when the baseline moves past v26.03.
# docs/specs/Tooling/USDValidationToolchain.md, fix 3. Idempotent: skipped once applied.
PATCH="$(cd "$(dirname "$0")" && pwd)/patches/hdSt-glslfx-primvar-type.patch"
if ! git -C "${SRC}" apply --reverse --check "${PATCH}" 2>/dev/null; then
  echo "[usd-tools] applying ${PATCH##*/}"
  git -C "${SRC}" apply "${PATCH}"
fi

# --- 2. Build USD + deps + tools via USD's own orchestrator ------------------------
# build_usd.py fetches+builds boost/tbb/opensubdiv/etc, then USD itself. --usdview
# implies --python --imaging. PySide6 + PyOpenGL come from the host env.
# The host python (conda's, or uv's) ships only the SHARED libpython, but build_usd.py introspects
# sysconfig and forces Python3_LIBRARY=libpython3.12.a (static, absent) -> FindPython3
# fails. Override with the real shared lib, derived from the active env (reproducible;
# .dylib on macOS).
PYLIB="$(python -c 'import sysconfig,glob,os; d=sysconfig.get_config_var("LIBDIR"); print(sorted(glob.glob(os.path.join(d,"libpython3.*.so"))+glob.glob(os.path.join(d,"libpython3.*.dylib")))[0])')"
echo "[usd-tools] forcing shared Python lib: ${PYLIB}"
# Linking the modules against that lib is right on Linux. On macOS it is not: uv's python
# has libpython built into the executable, so a module that also loads the .dylib puts two
# Pythons in one process and `import pxr` segfaults. There the modules leave the Python
# symbols to the running interpreter (dynamic lookup, USD's own macOS default).
PYLOOKUP=OFF
if [ "$(uname -s)" = "Darwin" ]; then PYLOOKUP=ON; fi

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
  --build-args "USD,-DPython3_LIBRARY=${PYLIB} -DPXR_PY_UNDEFINED_DYNAMIC_LOOKUP=${PYLOOKUP}" \
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
# consumer's vendored MaterialX tree (MATERIALX_BUILD_PYTHON=ON) and pass
# --build-args USD,"-DMaterialX_DIR=<prefix>/lib/cmake/MaterialX -DPXR_ENABLE_MATERIALX_SUPPORT=TRUE".
# Same-minor (1.39.x) is parity-faithful for OpenPBR rendering, so default uses USD's.
