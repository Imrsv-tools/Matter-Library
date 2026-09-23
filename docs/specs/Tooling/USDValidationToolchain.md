# USD Validation/Authoring Toolchain — faithful usdview/usdrecord/PyMaterialX

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

A **local, faithful, reproducible** OpenUSD validation + render toolchain built at the Matter Library's
**declared validation baseline**, so it reads and renders `.mtlx` the way a USD consumer at that baseline reads them. It is the
surface behind the authoring harness's **usdview parity QC gate**
([AuthoringHarness](AuthoringHarness.md) §Manual QC gates) and the `usdrecord` ΔE
baselines ([CompressedDistribution](CompressedDistribution.md) §Parity), and its PyMaterialX feeds the harness's `import MaterialX` assembler. Glossary term: [USD validation toolchain](../../Glossary.md).

> This is a **tooling-recipe** spec — it names *why the toolchain exists*, the *version-pin
> contract* it must hold, and *where the runnable recipe lives*; it does **not** restate the
> authoring pipeline (see [AuthoringHarness](AuthoringHarness.md) / the
> [Authoring Golden Path](../Authoring/AuthoringGoldenPath.md)).

## Why it exists

A lean USD runtime build (the kind a consuming application ships) typically strips dev capability —
Python support, GL, imaging and the USD tools are all turned off — so it has **no usdview/usdrecord**.
This toolchain is a *separate* build of the **same two sources** (OpenUSD + MaterialX) with those dev
capabilities turned back **on**, so the tools render `.mtlx` exactly as a consumer at the same versions
reads them. A separate install prefix perturbs no one's product build.

## The version-pin contract (the whole point)

Parity is only trustworthy if the toolchain is built at a known baseline. **The Matter Library declares its validation baseline:**

| Source | Pin |
|---|---|
| OpenUSD | **v26.03** |
| MaterialX | **1.39.5** (OpenPBR 1.39 nodedefs) |

*(Updated 2026-09-23, measured: `USD_TAG="v26.03"` and the MaterialX 1.39.3 → 1.39.5 archive pin in `tools/usd-toolchain/build-usd-tools.sh`; `MaterialX==1.39.5` in `tools/usd-toolchain/environment.yml`.)*

**Consumers state whether they match** the baseline (same USD version + same MaterialX minor ⇒ usdview/usdrecord are a faithful proof of how that consumer will read the material); a consumer that differs owns the gap. A baseline change is a deliberate Matter Library decision recorded here (re-point `environment.yml` + `build-usd-tools.sh`, rebuild). Build dev flags: `--python --usd-imaging --usdview --tools --materialx`.

Original text (kept, annotated):

> Parity is only trustworthy if the toolchain tracks Stage's sources. **These pins are the contract** (OpenUSD tracks the consumer's USD build tag; MaterialX tracks the consumer's vendored MaterialX). **When Stage bumps either pin, bump this toolchain in lockstep.**

> **Drift (2026-09-23):** "track Stage's pins in lockstep" makes a consumer the authority over the producer's baseline; under R1 the Matter Library declares its baseline and each consumer states whether it matches — owned by the release-bundle / consumer-contract phase (R1).

> **Done (Phase02, 2026-09-23):** the recipe's comments (`build-usd-tools.sh`, `environment.yml`, `README.md`) now state the pins as the library's baseline, chosen to match the IMRSV Stage consumer's build, and point at the Drift above for who follows whom. The README's link now resolves in this repo. The conformance scripts read the install location from `USD_TOOLS_ROOT` (the recipe's own variable) and the conda env from `USD_TOOLS_ENV`.

## Home — this repo's `tools/usd-toolchain/`

The recipe is **payload-adjacent** (it backs the harness QC gate and consumes nothing from
any consumer), so it lives beside the harness:

| Path (in `tools/usd-toolchain/`) | Role |
|---|---|
| `environment.yml` | conda host env (python 3.12, cmake 3.28, pyside6/pyopengl/numpy, **PyMaterialX 1.39.5** via pip) — isolates the host's system python/cmake/gcc |
| `build-usd-tools.sh` | clone v26.03 · pin MaterialX 1.39.5 · `build_usd.py` · apply the GLSL render fix |
| `run-all.sh` | create env from `environment.yml` → build (idempotent, backgroundable) |
| `activate-usd-tools.sh` | PATH/PYTHONPATH/LD_LIBRARY_PATH/`PXR_MTLX_STDLIB_SEARCH_PATHS` + the Linux render fix |
| `README.md` | recipe usage |

*(Updated 2026-09-23, measured: `ls tools/usd-toolchain/`; python/cmake pins in `environment.yml`.)*

The **built install** (`inst/usd-26.03/` under `$USD_TOOLS_ROOT`, which has a per-user default in the scripts) is a multi-GB artifact and is **never committed** (generated output). Reversible:
`rm -rf "$USD_TOOLS_ROOT"` and remove the conda env named in `environment.yml` (`imrsv-usd-tools`, a historical name kept).

## Five build fixes (captured in the recipe, reproducible)

`--imaging`→`--usd-imaging`; MaterialX `1.39.3`→`1.39.5` (the 1.39.3 default fails to compile
under gcc 16, and 1.39.5 is the baseline pin anyway); conda static→shared libpython override
(`-DPython3_LIBRARY=…so`, since conda ships only the shared lib but `build_usd.py` asks for the
static); `-DPXR_PY_UNDEFINED_DYNAMIC_LOOKUP=OFF` (link libpython into the C++ tools). PyMaterialX
is a pip wheel — `--materialx` builds only USD's MaterialX C++ libs, not the importable module.

## The live render path (two gotchas — durable)

The headless **data** path (`usdcat --flatten`, `usdchecker`, PyMaterialX, UsdMtlx) worked
immediately. The **live Storm GL render** took two fixes; both are baked into the recipe so a
fresh build renders correctly. (The full diagnostic trail is in `tools/usd-toolchain/README.md`.)

1. **Qt picks the wrong GL platform.** Both `usdview` *and* `usdrecord` build their GL context
   through **Qt (PySide6 `QOpenGLContext`)**. On a **Wayland** session (e.g. KDE Plasma 6) Qt
   defaults to the wayland platform + nvidia **Wayland-EGL**, which never gives Storm a valid GL
   **4.5 core** context → `HgiGL minimum OpenGL requirements not met` → cascading `No renderer
   plugins found`. This build's Garch is **GLX-only**. **Fix:** force Qt onto **Xwayland + GLX**
   (`QT_QPA_PLATFORM=xcb`, `QT_XCB_GL_INTEGRATION=glx`, `DISPLAY=:0`) — set in
   `activate-usd-tools.sh`, Linux-guarded. *(This was NOT conda GLVND shadowing system nvidia —
   a direct GLX 4.5 context from the conda python returns `4.5.0 NVIDIA` fine; the hypothesis was
   disproven.)*
2. **MaterialX OpenPBR shaders fail to compile** (kept it white even once the context worked).
   `pbrlib/genglsl/lib/mx_microfacet_specular.glsl` references `AIRY_FRESNEL_ITERATIONS`, but USD
   v26.03's `HdStMaterialXShaderGen::emitPixelStage()` is hand-copied from an older MaterialX and
   omits the `#define` that MaterialX 1.39.5's own `GlslShaderGenerator` emits → every OpenPBR
   material draws fallback white. **Fix (no rebuild needed):** `build-usd-tools.sh` injects a
   guarded `#define AIRY_FRESNEL_ITERATIONS 2` (MaterialX default) into that GLSL lib. Render-only
   — it does **not** touch data parity (a consumer reading `.mtlx` with GL off never runs this GLSL).
   The clean fix belongs upstream in OpenUSD's hdSt MaterialX shader generator.

**Cross-platform note (macOS / CI).** Fix 1 is Linux/Wayland-specific (macOS uses cocoa;
Storm-on-Metal needs neither var — the guard skips it). Fix 2 is a USD↔MaterialX integration gap,
not OS-specific, but macOS Storm uses the **MSL** generator, so if a Metal build shows the same
white-material symptom, apply the analogous define in the `genmsl` lib (the MaterialX MSL
generator emits it; USD's MSL `emitPixelStage` may omit it the same way).

> **Reevaluate (2026-09-23):** the macOS path has not been built or measured.

## Status

**Live Storm render working** (2026-06-21): `usdview` renders bound MaterialX
materials shaded in the viewport (eyeball-confirmed), and `usdrecord` produces real PNGs (copper
→ green verdigris metal, ABS → matte grey plastic). This unblocked the usdview parity gate and
seeds the `usdrecord` ΔE baselines. No wire/ABI contract frozen here.

## History

- 2026-06-21: the toolchain was built from source and the live Storm render was made to work (the two GL fixes above), inside the IMRSV platform, with its pins set to track one consumer's USD build.
- 2026-09-23: brought home; the pins reframed as the Matter Library's declared validation baseline that consumers match against.
