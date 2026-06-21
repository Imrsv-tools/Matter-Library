# activate-usd-tools.sh — put the IMRSV USD toolchain on PATH for a shell.
#   conda activate imrsv-usd-tools && source activate-usd-tools.sh
# Must be sourced from inside the conda env that built it.
#
# Override the install location with USD_TOOLS_ROOT (default ~/usd-tools).
INST="${USD_TOOLS_ROOT:-${HOME}/usd-tools}/inst/usd-26.03"
export PATH="${INST}/bin:${PATH}"
export PYTHONPATH="${INST}/lib/python:${PYTHONPATH:-}"
# Only the install's own lib — NOT the conda env lib. (Garch links libGL via the conda
# python's RPATH already; adding conda lib here is unnecessary and was implicated in
# earlier GL confusion. The proven render path uses INST/lib alone.)
export LD_LIBRARY_PATH="${INST}/lib"
# Storm/usdview need the MaterialX stdlib nodedefs (open_pbr_surface) to resolve; USD
# installs them under libraries/.
export PXR_MTLX_STDLIB_SEARCH_PATHS="${INST}/libraries:${PXR_MTLX_STDLIB_SEARCH_PATHS:-}"

# --- GL fix (Linux/Wayland) -------------------------------------------------------
# On a Wayland session (e.g. KDE Plasma 6) Qt/PySide6 — which BOTH usdview and usdrecord
# use to create their GL context — defaults to the wayland platform + nvidia Wayland-EGL,
# which does not hand Storm a valid GL 4.5 *core* context ("HgiGL minimum OpenGL
# requirements not met" -> "No renderer plugins"). This build's Garch is GLX-only, so
# force Qt onto Xwayland + GLX, where a core 4.5 nvidia context works. Harmless on X11.
# (macOS: Storm uses Metal, not GL/X — these are no-ops there, hence the Linux guard.)
if [ "$(uname -s)" = "Linux" ]; then
  export QT_QPA_PLATFORM="${QT_QPA_PLATFORM:-xcb}"
  export QT_XCB_GL_INTEGRATION="${QT_XCB_GL_INTEGRATION:-glx}"
  export DISPLAY="${DISPLAY:-:0}"
fi

echo "[usd-tools] active: $(command -v usdview || echo 'usdview NOT FOUND — build incomplete?')"
