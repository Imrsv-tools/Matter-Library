# Phase31 — The Rig on Windows

**Status:** WITHDRAWN AS A PHASE 2026-11-12, after its Brief. The lead: *"i feel a phase for this is overkill, also it only concerns this machine"*. *My reading:* the Windows rig work goes as a `/quick-fix` (or a few), with this doc as its input. The findings, the probe, the gate baseline and the two rulings (RD-P31-1, RD-P31-2) stay in force. The work's machine-specific settings (install paths, environment variables) stay on the machine and out of tracked files. Only the portable changes are committed: the platform branches in the drivers, the `Owner` rename, and the build twin. Kept, not deleted, so its intent survives. *(Historical: BRIEF READY the same day, both blockers ruled.)* Opened and numbered by the lead's `/discovery 31` the same day; seeded earlier that day by Phase30's discovery. Runs ahead of Phase30, which is parked on it (RD-P30-2). Lane: **build**.

**Why it exists:** the lead has only a Windows machine now (*"i only have this windows machine, not linux"*, 2026-11-12). Asked how Phase30 should be judged, the lead chose *"2"*: get the rig running on Windows first ([Phase30](Complete/Phase30_OneCoatOpaqueMaster.md) RD-P30-2).

## Outcome

**On the lead's Windows machine, the maintainer runs the rig and sees a material in Storm, Blender and Unreal side by side, as the Linux machines did, and builds the Unreal masters there.**

*Who it is for:* the maintainer, and every Unreal phase after this one, starting with Phase30. Nothing a consumer reads changes.

## First human test

**Where:** the lead's desktop on the Windows machine. The agent opens the sheet with Windows' own opener (`os.startfile`); the handback carries its path.

1. **Click 1 — the rig's sheet, three columns, on Windows (31.2).**
   - **Picture:** the rig's 11-article sheet (Phase29 click 1's set), Storm · Blender · Unreal, rendered on Windows.
   - **Fixtures:**
     - the grey card, ABS, Copper, Oak (Opaque); Rust (TwoLayer); Lace (Masked, a cut-out); Neon (a light); Glass_Clear, Glass_Green (thin see-through); Diamond (solid see-through); Marble (subsurface).
     - Together they span near-white, near-black, a mirror-like metal, clear surfaces and a light.
   - **What the lead judges:**
     - every article draws in all three columns: no magenta, no world-grid checker (`Unreal.md` U7), no white Storm frame (`Storm.md` S3);
     - beside each article, its ΔE per pair of tools, with the grey card held against Phase06's own 0.70 / 1.28 (Storm–Unreal; 6.3);
     - a difference between Windows and the last Linux sheet shows as a number, and the agent says which tool moved.
   - **The sentence afterwards:** *"the rig draws all three tools on my Windows machine, and they agree as they did on Linux."*

**The agent's, not a click:**
- 31.1's two-column sheet (Storm · Blender) before Unreal is wired: plumbing, its evidence the ΔE table.
- The gate's baseline on Windows, before any edit (§Risk lane).

## In now / not now

- **In:**
  - **31.1 — Storm and Blender columns on Windows.**
    - `tools/parity/drivers/storm.py` and `tools/preview_generators/make_preview.py` `usd_env`: a Windows branch. The interpreter comes from the toolchain's venv, since a `#!` line does not run on Windows. Also `inst/lib` on `PATH` for the DLLs, and no `LD_LIBRARY_PATH` / GLX settings.
    - A Windows twin of the USD recipe, `tools/usd-toolchain/build-usd-tools.cmd` (or `.ps1`), carrying what the hand build did: vcvars64 + Ninja, `build_usd.py`, MaterialX pinned to 1.39.5, and the `AIRY_FRESNEL_ITERATIONS` define re-applied after every build (the bash recipe's step 3).
    - Blender 5.3.0, already installed on the lead's machine (official build, 2026-11-10), as `$MATTER_BLENDER` (RD-P31-2).
  - **31.2 — Unreal column on Windows.**
    - `MatterRuntimeGameMode.cpp`: the local `Owner` renamed. MSVC refuses it as C4458 (it hides `AActor::Owner`); clang on Linux never said.
    - `unreal/build.ps1 [editor|masters]`, the twin of `build.sh`'s two CPU steps. It keeps the masters step's double check: the exit code AND *"MATTER RESULT ok"*.
    - `tools/parity/drivers/unreal.py`: editor mode is the Windows default, through `$UE_ROOT` (default `C:/Program Files/Epic Games/UE_5.8`) → `Engine/Binaries/Win64/UnrealEditor.exe`, as the Mac default does. `nice -n 19` becomes a below-normal priority class on Windows.
    - The renderer check (D-P31-2).
  - **At the close:**
    - `docs/ToolingConventions.md` §Entry points: the Windows forms;
    - `docs/specs/Tooling/USDValidationToolchain.md`: a Windows section;
    - Learnings: Unreal (C4458; the RHI result), Storm (the Windows run form, `UsdGeom.Sphere` has no UVs).
- **Not now:**
  - a packaged Win64 runtime and its publish (RD-P31-1);
  - `blender/addons/` and `tools/conformance/check_exporter.sh` (bash; untouched by this phase, so not baselined);
  - the platform's own Windows scripts.
  - `LOCAL_DELTAS.md` §Two machines no longer describing the machines in use: a `/retro` item for the Refiner.

## Rides on

No `docs/CoreMechanisms.md` row is met: its five rows are skin and makeup authoring and the object fade. **The peers are the rig's own drivers**, and each Windows branch copies the shape already there for the Mac:

| Where | The peer we follow (opened this pass) |
|---|---|
| the Unreal launcher | `tools/parity/drivers/unreal.py:617–643` `find_runtime`: `$MATTER_UNREAL_EDITOR`, else a per-platform default under `$UE_ROOT` (Mac today) |
| the Unreal launch | `unreal.py:693–710` `run_runtime` (`nice`, the display variables, the double failure check) |
| Storm's environment | `make_preview.py:101–118` `usd_install` / `usd_env` (`sys.platform` branch for Linux's GLX) |
| Storm's interpreter | `storm.py:46–60` (the `#!` read) |
| the masters build | `unreal/build.sh:33–57` (exit code + result line) |

## The reuse check

- **What the stack already provides:** Unreal's own `Build.bat` / `RunUAT.bat`; OpenUSD's `build_usd.py`, which supports Windows natively; Blender's official Windows build; Python's `os.startfile` and `subprocess` priority classes.
- **No custom layer is proposed.** Every change is a platform branch beside an existing one.
- **Standards touched:** none. No article, contract or format changes, and the job format is unchanged.

## Decisions that bind

- **D-P31-1 — Unreal on Windows runs in editor mode** (`UnrealEditor.exe <project> -game`, the driver's existing editor path), not as a package. The machine has Unreal. The package exists for machines that do not (Phase06 D2). *(The published runtime: RD-P31-1.)*
- **D-P31-2 — The renderer: measured at 31.2, not assumed.** The Linux history is Vulkan SM6. Windows defaults to D3D12. The grey card and Copper are rendered on both (`-d3d12` / `-vulkan`). **The one nearer Phase06's grey card (0.70 / 1.28) is kept, D3D12 on a tie** (the consumer's default on Windows). Both numbers are recorded.
- **D-P31-3 — Blender is the official 5.3.0 build the lead has installed** (RD-P31-2), not the 4.0 also there. The rig was last measured on 5.2.2 (`Blender.md` B22); 31.1's sheet is the first reading on 5.3, so a Storm–Blender ΔE that moves from the Linux sheets is checked against the version before it is blamed on Windows.
- **D-P31-4 — The hand-built USD toolchain is kept and given a recipe in the tree** rather than rebuilt. It is already OpenUSD 26.03 + MaterialX 1.39.5, the library's pins, and it matched MaterialX's GLSL reference within 2 % on three coated articles (the platform's check). The recipe makes a rebuild repeatable.

## Blockers — the lead's

1. **RULED 2026-11-12 → (a), RD-P31-1.** The lead: *"d1 a"*. *My reading:* no package is built or published from Windows for now; `RUNTIME.json` keeps `unreal-runtime-v9` as the last Linux runtime; a master change that owes a runtime (Phase30's) writes a dated *runtime owed* line instead. *The fork as it was put:* **The published Unreal test runtime, with no Linux machine.** Today `unreal/RUNTIME.json` pins `unreal-runtime-v9`, a Linux package. The rule that a master change *"owes a new runtime"* assumes a Linux machine can build one. Phase30 will owe one.
   - **(a) Recommended — no new package for now.** The rig on Windows runs editor mode (D-P31-1). The v9 pin stays as the last Linux runtime. A runtime a change owes is written as a dated *runtime owed* line, as `LOCAL_DELTAS.md` already says for a machine that cannot build it. Smallest; nothing is published.
   - **(b)** Package and publish a **Win64** runtime from here (`RunUAT BuildCookRun -platform=Win64`, a `MatterRuntime-Win64-…` asset, `RUNTIME.json` naming it). The rig then also runs on a Windows machine without Unreal. It adds a package step, a publish twin of `publish.sh`, and a public asset per change.
2. **RULED 2026-11-12, RD-P31-2.** The lead: *"d2 blender 5.3 is installed"*. Read on the machine: the official Blender 5.3.0 (build date 2026-11-10). Nothing is installed by this phase. *The fork as it was put:* **Install Blender 5.2 on your machine** — the official portable zip, unpacked to a folder of your choosing; no installer, and Blender 4.0 is left alone. Without it the Blender column cannot run (D-P31-3).
   - **Recommended:** yes, at 31.1.
   - **Otherwise:** the rig runs with Storm and Unreal only, and the sheet says Blender is missing.

## Step list

- **31.1 — Storm and Blender draw on Windows.**
  - The Storm driver's and `usd_env`'s Windows branch, the recipe twin, and Blender 5.3 as `$MATTER_BLENDER`.
  - Its evidence is the agent's: the 11-article sheet in two columns, ΔE Storm–Blender per article.
- **31.2 — Unreal draws on Windows.**
  - The `Owner` rename, `unreal/build.ps1`, the driver's Windows editor default and priority, the masters built into the library's project, and the renderer measured (D-P31-2).
  - First clickable result: **click 1**.
- **At the close:** the doc sweep and the learnings; no runtime published (RD-P31-1).

Click 1 needs both steps: it is the first point where all three columns exist. Every §In now bullet names its step or *at the close*.

## Compact build map

- **Probed this pass** (a scratch copy outside the repo, 2026-11-12):
  - `Build.bat MatterRuntimeEditor Win64 Development -Project=<copy>/MatterRuntime.uproject -MaxParallelActions=8 -WaitMutex` on Unreal 5.8.4 (an installed build).
  - UBT picked **Visual Studio 2026's MSVC 14.44** and the Windows 10.0.22621 SDK.
  - The first run failed on one error only, C4458 at `MatterRuntimeGameMode.cpp:443`. With the local renamed (4 occurrences), it **succeeded in 13 s**.
  - The source has no platform code (`PLATFORM_*`, SDL, POSIX headers: none).
- **`Config/DefaultEngine.ini`:** `[/Script/LinuxTargetPlatform.LinuxTargetSettings]` names Vulkan only. A Windows section is added only if D-P31-2 keeps Vulkan.
- **Files:**
  - `tools/parity/drivers/{storm,unreal}.py`
  - `tools/preview_generators/make_preview.py`
  - `tools/usd-toolchain/` (+ the twin)
  - `unreal/build.ps1`
  - `unreal/MatterRuntime/Source/MatterRuntime/MatterRuntimeGameMode.cpp`
- **Tests:** the existing lanes and one real-path smoke, the sheet. No new gate.

## Risk lane — `build`

- **What it touches:** no authorisation, secrets, data or public edge. Nothing is published (RD-P31-1).
- **Controls read:**
  - nothing hashes the drivers (`rig.py`, `look.py`: only LFS objects are hashed);
  - `run_all.py` is the gate: its Windows baseline is below;
  - `check_exporter.sh` is bash and guards `blender/addons/` and `tools/conformance/`, which this phase does not touch.
- **The gate's baseline on Windows, before any edit** (`uv run tools/validators/run_all.py`, 2026-11-12, at `d33cbdd`): **18 lanes, 15 PASS, 0 SKIP, 3 FAIL** — `release_verify`, `activation`, `tool_tests`.
  - `release_verify`: `matterlib-0.1.0`'s recorded `payload_sha256` (catalog, manifest, mtlx_set) do not match the files on disk. Most likely the Windows checkout's line endings (Git warns *"LF will be replaced by CRLF"* on this clone); not verified.
  - `activation`: the installed catalog's hash is not the approval's frozen one, which follows from the same mismatch.
  - `tool_tests`: `tools/releases/test_build_snapshot.py` fails with `UnicodeDecodeError: 'charmap'`, a file read without an explicit encoding (Windows' default code page).
  - None comes from this work; each is a Windows-machine defect of its own, for its own fix.

## Discovery Log

- **Pass 1 (2026-11-12):**
  - **Read:**
    - the rig's drivers (`storm.py`, `unreal.py` `find_runtime` / `run_runtime`, `rig.py`'s tool lookup) and `make_preview.py` `usd_env`;
    - `unreal/build.sh`, `publish.sh` and the USD recipe's README and build script;
    - `CoreMechanisms.md` and the learnings for Storm, Unreal, Blender and ClaudeCode;
    - the C++ source for platform code, and the old `win-build-attempt-1` branch (one fix to `serve_to_stage.py`, outside the rig; left as is).
  - **Probe:** the Win64 editor build (§Compact build map).
  - **Corrected the seed:** Storm *is* built here, and Visual Studio 2026 *is* installed (`f7224fc`).

## Discovery Status

- **Passes captured:** 1.
- **Current working direction:** 31.1 Storm + Blender, 31.2 Unreal in editor mode.
- **Open decisions:** none (RD-P31-1, RD-P31-2). Withdrawn as a phase; the work goes as a `/quick-fix`.
- **Checks to carry forward:**
  - the gate baseline;
  - D-P31-2's renderer measurement;
  - the grey card against 0.70 / 1.28.

## Execution Log

- **2026-11-12 — the rig runs on Windows, as a `/quick-fix`** (`git log --grep "✅ Quick Fix — the parity rig on Windows"`). The Storm environment's Windows branch, the Unreal driver's Windows editor default and priority, the `Owner` rename, `unreal/build.ps1` (editor + masters), and a Windows section in `DefaultEngine.ini`.
  - **D-P31-2 measured** on the grey card. D3D12 with no Windows section ran at **SM5: 6.72 / 14.36** ΔE2000 Unreal–Blender. `-vulkan` was refused by the project's data and fell back to SM5 with the same numbers. **D3D12 at SM6: 0.85 / 1.43** (close-up 0.77 / 1.28), with Storm–Blender at 0.31 / 0.98. **Kept: D3D12 SM6** (`Unreal.md` U23).
  - Blender 5.3.0 and Storm agree on the grey card (0.31), so the version change shows no drift there.
  - **Not done:** the USD recipe's Windows twin (the hand build stands; D-P31-4); the 11-article click-1 sheet; `USDValidationToolchain.md`'s Windows section.
