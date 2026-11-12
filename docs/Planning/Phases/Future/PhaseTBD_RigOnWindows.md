# Phase TBD — The Rig on Windows

**Status:** SEEDED 2026-11-12 (phase doc exists; discovery has not opened). Not numbered: numbering is the lead's.

**Why it exists:** the lead has only a Windows machine now (*"i only have this windows machine, not linux"*, 2026-11-12). Asked how Phase30 should be judged, the lead chose *"2"*: get the rig running on Windows first, with Phase30 waiting behind it ([Phase30](../Phase30_OneCoatOpaqueMaster.md) RD-P30-2).

## Outcome

**On a Windows machine with Unreal, the maintainer runs the rig and sees a material in Storm, Blender and Unreal side by side, as the Linux machines did. The Unreal masters and the test runtime build there too.**

Concretely, at close:
- `uv run tools/parity/rig.py <article>` draws all three columns on Windows;
- the library's Unreal app (`unreal/MatterRuntime`) and its masters build there;
- the test runtime can be built and published from there, or the lead has ruled what replaces it.

## Why this is a phase

Every Unreal phase from Phase30 on needs it. It touches three toolchains (OpenUSD's Storm, Blender, Unreal and its C++ build) and the scripts that assume a POSIX machine. One outcome: the rig's sheet, on this machine.

## What was measured at seeding (2026-11-12, on the Windows machine)

- **Unreal:**
  - Unreal 5.8 is installed, and Studio's project builds the masters with it: the platform ran `build_masters.py` as a commandlet into Studio's plugin from a PowerShell stand-in for the Linux/Mac build script.
  - The library's own app has **never been built here**: `unreal/MatterRuntime` has no `Binaries/`.
  - **A C++ toolchain is installed:** Visual Studio 2026 (v18) Community, on a second drive. It built OpenUSD the same day. The Visual Studio 2022 folder under Program Files is empty, and 2019 is there. *(Corrected the same day: the seed first read the empty 2022 folder as "no toolchain".)* Whether Unreal 5.8 builds a C++ project with 2026 is to be checked.
- **The rig's Unreal driver** (`tools/parity/drivers/unreal.py` `find_runtime`) knows three launchers: `$MATTER_UNREAL_RUNTIME`, editor mode by `$MATTER_UNREAL_EDITOR` (or the Mac default), and the pinned runtime, which is **Linux-only** (`Linux/MatterRuntime.sh`). `unreal/build.sh` and `publish.sh` are bash for Linux/Mac.
- **Storm: built and working, by hand.** *(Corrected the same day: the seed first said there was no `usdrecord`, having looked only on `PATH`.)*
  - The platform's session built OpenUSD 26.03 with MaterialX 1.39.5 (Storm, `usdrecord`, `usdview`) from the library's own recipe, `tools/usd-toolchain/build-usd-tools.sh`, by hand, because the recipe is bash-only. It lives in a local tools folder with its own Python 3.12 venv and a `build.cmd` (vcvars64, Ninja, `build_usd.py` with `MATERIALX_URL` set to v1.39.5; about 15 min).
  - Its environment: `PATH` += `inst/bin;inst/lib` · `PYTHONPATH=inst/lib/python` · `PXR_MTLX_STDLIB_SEARCH_PATHS=inst/libraries`.
  - Run as `python inst/bin/usdrecord ...`: there are no `.exe` wrappers, and the `#!` lines do not work on Windows.
  - **Two gotchas, as relayed.** After any rebuild, re-prepend the `AIRY_FRESNEL_ITERATIONS` define to `libraries/pbrlib/genglsl/lib/mx_microfacet_specular.glsl`, or Storm renders white. The define is present today. And Storm drops textures on `UsdGeom.Sphere`, which has no UVs: use mesh spheres with `primvars:st`.
  - Checked by that session: on Paint Gloss, Porcelain and Leather, Storm matched MaterialX's GLSL reference within 2 %.
  - **What is left is the driver.** `tools/parity/drivers/storm.py` finds `usdrecord` under `$USD_TOOLS_ROOT/bin`, then reads its `#!` line and sets `LD_LIBRARY_PATH`. Both are POSIX, so it needs a Windows branch. The recipe itself has no Windows form.
- **Blender:** only 4.0 is installed. The library needs 5.1+, and the rig is measured on an official 5.2 build (`LOCAL_DELTAS.md`; Learnings B22).
- **Earlier Windows work:** branch `win-build-attempt-1` (2026-10-22, not on main) holds one fix: `serve_to_stage.py` finds the Stage binary on Windows.

## Scope

**In:**
- the rig's three columns on Windows;
- building the library's Unreal app and masters on Windows;
- a Windows path for the runtime build and publish, or a lead ruling on what the pinned runtime becomes with no Linux machine.

**Out:**
- the platform's own Windows tooling;
- Phase30's master change itself.

## Open questions (seed — test against the docs in Pass 1)

1. What is still to install on the lead's machine? Blender 5.x. OpenUSD/Storm is built, and Visual Studio 2026 is present, though whether Unreal 5.8 accepts it is still open. Each install is the lead's call. Also: should the hand-built USD recipe become a `.cmd`/PowerShell twin of `build-usd-tools.sh` in the tree, so a rebuild (and the GLSL define) is repeatable?
2. Editor mode or a packaged Win64 runtime for the rig's Unreal column? Editor mode skips a package, but `RUNTIME.json` and `publish.sh` assume one.
3. With no Linux machine, what does `unreal/RUNTIME.json` pin? A Win64 package, both, or nothing until a Linux machine returns?
4. Which lanes of `run_all.py` and `check_exporter.sh` run on Windows today? Baseline them first: a lane that cannot start is absent coverage.
5. Is `win-build-attempt-1` worth merging, or superseded?
6. `LOCAL_DELTAS.md` §Two machines no longer describes the machines in use. That is a `/retro` item for the Refiner, not this phase's edit.

## Rides on

_(discovery pass 1)_

| Row | What in this phase rides it | The peer we follow (file:line, opened) |
|---|---|---|

## Discovery Log

_(numbered passes accrue here)_

## Discovery Status

- **Passes captured:** —
- **Current working direction:** —
- **Open decisions:** —
- **Checks to carry forward:** —

## Execution Log

_(populated during execution)_
