# `usd-toolchain/` — reproducible OpenUSD validation/authoring toolchain

The **recipe** that builds a faithful, from-source OpenUSD **v26.03** + MaterialX **1.39.5**
install with `usdview` / `usdrecord` / `usdcat` / `usdchecker` / PyMaterialX — the dev tools
Stage strips out of its lean runtime. It reads/renders `.mtlx` the same way Stage does, so it
backs the Phase-53 authoring harness's QC parity gate and Phase-60 `usdrecord` ΔE baselines.

**The "why", the version-pin contract, and the full GL-render gotcha are the durable doc:**
[`IMRSV_Platform_Documentation/MatterLibrary/Tooling/USDValidationToolchain.md`](../../../IMRSV_Platform_Documentation/MatterLibrary/Tooling/USDValidationToolchain.md).
This folder is just the runnable recipe.

## Build
```bash
# 1. system prereqs (see environment.yml header) — Fedora example:
sudo dnf install gcc-c++ libXt-devel libXrandr-devel libXinerama-devel libXcursor-devel libXi-devel mesa-libGL-devel
# 2. one shot (creates the conda env + builds; ~30-50 min, idempotent, logs to build.log):
bash run-all.sh
```
The install lands in `${USD_TOOLS_ROOT:-~/usd-tools}/inst/usd-26.03` and is **never committed**
(multi-GB). Override the location with `USD_TOOLS_ROOT`.

## Use
```bash
conda activate imrsv-usd-tools && source activate-usd-tools.sh   # PATH + GL env
usdchecker  <file.usda|file.mtlx>          # validate
usdcat --flatten <file>                    # inspect composed network
usdview     <stage.usda>                   # live Storm GUI (eyeball parity)
usdrecord --complexity high <stage.usda> out.png   # headless PNG
```

## Files
| File | Role |
|---|---|
| `environment.yml` | the conda host env (python 3.12, cmake 3.28, pyside6/pyopengl/numpy, PyMaterialX 1.39.5) |
| `build-usd-tools.sh` | clone v26.03, pin MaterialX 1.39.5, run `build_usd.py`, apply the GLSL render fix |
| `run-all.sh` | create env from `environment.yml` → build; backgroundable |
| `activate-usd-tools.sh` | PATH/PYTHONPATH/LD_LIBRARY_PATH/MTLX + the Linux Wayland→xcb/GLX render fix |

> The five grounded build fixes and the two render-path fixes (Qt Wayland-EGL → Xwayland+GLX,
> and the missing `AIRY_FRESNEL_ITERATIONS` GLSL define) are captured in the scripts and
> explained in the durable doc. Reversible: `rm -rf "$USD_TOOLS_ROOT" && conda env remove -n imrsv-usd-tools`.
