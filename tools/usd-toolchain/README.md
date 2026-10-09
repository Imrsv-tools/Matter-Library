# `usd-toolchain/` — reproducible OpenUSD validation/authoring toolchain

The **recipe** that builds a faithful, from-source OpenUSD **v26.03** + MaterialX **1.39.5**
install with `usdview` / `usdrecord` / `usdcat` / `usdchecker` / PyMaterialX — the dev tools
a lean runtime strips out. These pins are the library's USD baseline, chosen to match the IMRSV
Stage consumer's build, so it reads/renders `.mtlx` the way that consumer does. It backs the
authoring harness's QC parity gate and the `usdrecord` ΔE baselines.

**The "why", the version-pin contract, and the full GL-render gotcha are the durable doc:**
[`docs/specs/Tooling/USDValidationToolchain.md`](../../docs/specs/Tooling/USDValidationToolchain.md).
This folder is just the runnable recipe.

## Build
```bash
# 1. system prereqs (see environment.yml header) — Fedora example:
sudo dnf install gcc-c++ libXt-devel libXrandr-devel libXinerama-devel libXcursor-devel libXi-devel mesa-libGL-devel
#    macOS: Xcode command-line tools only (Storm renders through Metal).
# 2. one shot (creates the host env + builds; ~30-50 min, idempotent, logs to build.log):
bash run-all.sh
```
The host env only pins Python 3.12 + cmake 3.28 and the Python packages the tools need. With
conda on PATH it is the conda env from `environment.yml`; without it, `run-all.sh` makes a uv
venv at `$USD_TOOLS_ROOT/venv` with the same pins.
The install lands in `${USD_TOOLS_ROOT:-~/usd-tools}/inst/usd-26.03` and is **never committed**
(multi-GB). Override the location with `USD_TOOLS_ROOT`.

## Use
```bash
source activate-usd-tools.sh   # PATH + GL env (after `conda activate imrsv-usd-tools`; the uv venv activates itself)
usdchecker  <file.usda|file.mtlx>          # validate
usdcat --flatten <file>                    # inspect composed network
usdview     <stage.usda>                   # live Storm GUI (eyeball parity)
usdrecord --complexity high <stage.usda> out.png   # headless PNG
```

## Files
| File | Role |
|---|---|
| `environment.yml` | the conda host env (python 3.12, cmake 3.28, pyside6/pyopengl/numpy, PyMaterialX 1.39.5); `run-all.sh`'s uv venv carries the same pins |
| `build-usd-tools.sh` | clone v26.03, pin MaterialX 1.39.5, apply `patches/`, run `build_usd.py`, apply the GLSL render fix |
| `run-all.sh` | create the host env (conda from `environment.yml`, else a uv venv) → build; backgroundable |
| `patches/` | source patches applied before the build (the Metal render fix) |
| `activate-usd-tools.sh` | PATH/PYTHONPATH/LD_LIBRARY_PATH/MTLX + the Linux Wayland→xcb/GLX render fix |

> The five grounded build fixes and the three render-path fixes (two on Linux GL, one on
> macOS Metal, the last a source patch in `patches/`) are captured in the scripts and
> explained in the durable doc. Reversible: `rm -rf "$USD_TOOLS_ROOT"` (the uv venv lives inside it), plus `conda env remove -n imrsv-usd-tools` where conda made the env.
