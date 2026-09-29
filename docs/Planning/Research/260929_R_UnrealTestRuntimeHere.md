# Research — The Unreal test runtime, built on this machine, run on any Linux machine

**Opened:** 2026-09-29 · **Mode:** research. It gathers and commits to nothing. **Mnemonic:** `UR` (ids `UR-Qn`, `UR-Fn`).

**Question (lead, 2026-09-29, condensed):** "Phase 6… what do we need to make an agent-controlled setup that can test materials in our UE setup with the needed master materials. This system has UE 5.8. Another agent is using it for the IMRSV project at the moment, so we need to be careful with opening things. Ideally this would be a standalone project we build and bring back to any other Linux system to test the materials agentically. Possible? Let's find out."

**Extends, does not replace:** `Phase06_UnrealTestRuntime.md` (SEEDED; its Outcome and scope stand), `260926_R_BigPicture_NimbleSetup.md` Passes 7–8 (what the runtime is and where it hurts), and `tools/parity/JOB_FORMAT.md` (the render job an Unreal driver implements).

**How this was done:** everything below was read from disk. **No Unreal process was launched**, no project was opened, and nothing under the engine or another project was written to.

---

## Resolved — lead decisions (2026-09-29)

| # | Decision |
|---|---|
| UR-D1 | **Phase06 runs on this machine** (lead: *"yes run it here"*). This is the UE machine; the other machine built everything else (UR-F1, corrected). Answers UR-Q1. |
| UR-D2 | **Ask before each GPU launch;** the first one was approved at once (*"ask me before GPU launches but now is OK"*). Answers UR-Q5. |
| UR-D3 | **Everything lives in this repo, the built executable included,** so the other machine pulls and tests it (*"if you keep everything in this repo including the executable, I can pull on the other machine and test"*). This answers UR-Q3 and UR-Q6: git is the delivery, and the other machine is the portability test. |

---

## The short answer

**Yes, it is possible, and most of what it needs is already on this machine.** The engine installed here can build a small Unreal app of our own and package it for Linux. The package runs on any 64-bit Linux machine with a Vulkan GPU driver and no Unreal install. The agent drives it from the rig with one command and gets pictures back, with no window and no editor.

**One find changes how the masters get built.** Unreal 5.8 ships **Epic's own OpenPBR material functions**, whose inputs carry OpenPBR's own parameter names: the names our articles already use. The Unreal masters can be thin wrappers around Epic's function, not hand translations (Pass 3).

**The one real risk is sharing the machine,** and it is manageable with a few rules (Pass 4). Nothing needs launching until the lead picks a moment.

---

## Pass 1 — What changed since Phase06 was seeded

**Examined:** the Phase06 stub, BigPicture BP1/BP6/BP7, the engine registry and the engine install on this machine (2026-09-29).

**Finding UR-F1: Unreal 5.8.0 is on this machine.** It is Epic's installed Linux build, version 5.8.0 (changelist 55116800), registered as `UE_5.8`.

**Corrected 2026-09-29 (lead):** this machine **is** the "UE machine" the Phase06 stub means. The *other* machine, where Phases 05, 07 and 08 were built, has no Unreal. *(This pass first read BP1 as "no Unreal here", which had the two machines the wrong way round.)* So BP1, BP6 and BP7 stand as written: Phase06 runs here, and the package goes back to the other machine. See UR-D1–D3.

## Pass 2 — What this engine install can do (read from disk, nothing launched)

**Examined:** the install's build marker, its binaries, its bundled toolchain, and the plugin descriptors for Python, capture and USD.

| Need | On disk | What it means |
|---|---|---|
| Package a Linux app | `UnrealGame-Linux-Shipping` and `-DebugGame` binaries are present | An installed build can package for Linux. |
| Compile our own C++ | A bundled clang 20.1.8, built against a Rocky Linux 8 system root (glibc 2.28) | There is no system compiler to set up. The package should run on any distribution with glibc 2.28 or newer, which covers roughly every distribution since 2018. *(Inferred from the system root, not yet run elsewhere.)* |
| Build masters by script | `PythonScriptPlugin` | The masters can be built by an editor script run as a commandlet, which needs no window and no GPU. The IMRSV platform has used this recipe on 5.8 to build its 7 masters in under a second. |
| Capture without the editor | `MovieRenderPipeline` has runtime modules allowed on Linux | A packaged app can capture. A simpler scene-capture readback is probably enough (Pass 5). |
| Read the USD test scene | `USDStage` and `USDCore` have runtime modules allowed on Linux | The scene could even load at run time. Importing it once at build time is simpler. |
| OpenPBR | See Pass 3 | — |

**Unverified until run:** whether a packaged Linux (Vulkan) build with Substrate on renders **headless** (`-RenderOffscreen`), and whether it needs a display server at all. Neither this repo nor the IMRSV platform has ever packaged a full Linux build on this machine; the platform deliberately kept a full package out of its gates because it is heavy here.

## Pass 3 — Unreal 5.8 speaks OpenPBR

> **Corrected by probe 1 (2026-09-29, spike UR-F4):** the function to wrap is the **core engine's** `/Engine/Functions/Substrate/MF_Substrate_OpenPBR_Opaque` (and `_Translucent`), which outputs a Substrate front material. The Interchange plugin's `MX_OpenPBR_*` named below outputs Unreal's classic pins instead. The rest of this pass stands.

**Examined:** the engine's Interchange plugin (its MaterialX translator source and its content), and the `BaseMaterial` plugin. Input names were read as strings out of the asset files; **the assets were not opened in Unreal.**

**UR-F2: Epic ships OpenPBR as material functions.**
- `/Interchange/Functions/MX_OpenPBR_Opaque` and `MX_OpenPBR_Translucent` (Substrate). Their inputs carry the OpenPBR names: `base_weight`, `base_color`, `base_metalness`, `base_diffuse_roughness`, `specular_weight`, `specular_roughness`, `specular_roughness_anisotropy`, `specular_ior`, `coat_*`, `fuzz_*`, `subsurface_weight`, `subsurface_color`, `subsurface_radius`, `subsurface_scatter_anisotropy`, `thin_film_*`, `emission_luminance`, `emission_color`, `geometry_opacity`, `geometry_thin_walled`, `geometry_normal`, `geometry_tangent`.
- **`MX_Place2D`**, MaterialX's own UV placement. It matters because the platform found that Unreal's USD transform function does the *opposite* of MaterialX's `place2d` (it multiplies by the scale where `place2d` divides), and it hand-wrote a fix. Epic's `place2d` should make that fix unnecessary.
- 71 `MX_*` functions in all, including hair BSDFs, sheen and subsurface.
- A `BaseMaterial` plugin (Epic's, **flagged beta**, on by default) with `M_OpenPBR_Opaque_Parent` and a parallax variant.

**UR-F3: Epic's own importer partitions OpenPBR as our master set does.** Interchange's MaterialX translator picks the Unreal blend mode from which OpenPBR inputs an article sets: transmission → translucent (coloured transmittance); opacity → masked; subsurface → Substrate subsurface. It warns that OpenPBR *"might be wrong"* unless the project uses Substrate's **Adaptive GBuffer** format. That is the MasterSet's governing insight (*"only a renderer that partitions shader space forces the split"*), arrived at independently by Epic.

**Nobody here knew this:** neither this repo nor the IMRSV platform docs mention `MX_OpenPBR`, `MX_Place2D` or the `BaseMaterial` plugin (grep, 2026-09-29).

**What it means, two ways:**
1. **The masters can wrap Epic's function.** An article's values go in by the same names they have in the `.mtlx`, so the loader has no translation table to drift. The work that remains per master is the part the LCD ruling asks for: Unreal's settings (blend mode, two-sided, dithered coverage), our overlay and mask network, and Unreal's better model where it has one (the skin profile, the Cloth model, hair). This also makes Studio's adoption easier (`PlatformDependencies.md` P20): the parameter names Studio must bind become OpenPBR's own.
2. **A cheap reference column exists before any master is built.** Interchange can import an article's `.mtlx` directly into an Unreal material in the editor. That is not the product: Studio renders through masters (P20), and a packaged app cannot compile a new shader per article. But it is Epic's own reading of our article, useful as a quick first Unreal picture and, later, as a check on our masters. *(Unverified: how much of our nodegraph it imports, especially the overlay and mask network and the shared layer textures.)*

**Risks:** the functions' real inputs and behaviour are read from strings, not tested. `BaseMaterial` is beta, so its layout can change in a later Unreal. The function lives in plugin content, and whether it survives packaging is **unverified** (probe 1 below settles all three).

## Pass 4 — Sharing the machine with the IMRSV agent

**Examined:** the running processes and the GPU (2026-09-29: **no Unreal process running**; GPU 1.3 of 24 GB in use), the engine's per-user state, disk space, and the IMRSV platform's own lessons about Unreal on this machine (private; summarised here without detail).

**What is shared, and what is not:**
- **Separate by construction:** our own project folder, with its own `Saved/`, `Intermediate/` and project config. We **never open, build or touch** the platform's Studio project.
- **Shared whether we like it or not:** the engine install (read-only in use), the per-user Unreal folder (the shared derived-data cache and its cache server, build-tool state, per-user editor settings), the CPU, the GPU and the disk.

**The hazards, measured or recorded:**
1. **This machine can freeze under a CPU storm.** An uncapped parallel build hard-reset it once (2026-09). The platform also recorded that a brand-new 5.8 level with default settings (Lumen on) set off a shader-compile storm that locked the desktop, twice.
2. **The GPU has a hang history.** Crash capture is armed on this machine for that reason.
3. **Another agent's run can be killed by ours, and ours by theirs.** The platform's rule: find out who owns a running Unreal process before acting, and never kill one you did not start.
4. **Disk is tight:** 77 GB free (92 % used), and the video work keeps a 50 GB floor on the same filesystem. That leaves **about 27 GB** for our project, its cache and a package. An estimated 5–15 GB is enough, but that estimate is unverified.

**The rules that make it safe (proposals for discovery):**
- **Look before launching.** Check for any running Unreal process first (`ps -ef | grep "[U]nreal"`). If one is running, name its owner (another Claude session, or the lead), and **ask the lead** before any GPU work.
- **Most of the work needs no GPU.** Building the masters and importing the scene run as commandlets with `-nullrhi` (no GPU at all). Only the render step touches the GPU, in short batches at 512 px.
- **Cap everything:** the C++ build with a fixed job count (for example `-MaxParallelActions=8`), shader compiling through **our project's** config, and every launch under `nice -n 19`.
- **Never a default new level.** Our project turns off GI, Lumen and screen-space reflections in its own config, so nothing opts into them.
- **Change nothing shared.** No edits under the per-user Unreal folder: its build configuration file is global and would change the other agent's builds. Use command-line flags only. Whether our project can use its **own** cache instead of the shared one is worth probing. *(Unverified in 5.8's installed build.)*
- **Tell the lead before the first launch.** The first launch compiles shaders. The platform's own rule on this machine is to announce a shader-heavy first launch before running it.

## Pass 5 — The shape: one project in this repo, two ways to run it

**What goes in git (this repo, its own folder):**
- A **small C++ Unreal 5.8 project** (Substrate on, Adaptive GBuffer, GI and reflections off), plus the **Python scripts that build everything else**: the masters, the imported scene and the level. Ideally no hand-made binary assets live in git at all. Any Linux machine with Unreal 5.8 rebuilds them from the scripts.
- A **rig driver**, `tools/parity/drivers/unreal.py`, beside `storm.py` and `blender_render.py`, implementing `JOB_FORMAT.md`.

**The built package goes in git too (UR-D3),** so the other machine pulls and runs it. It is too large for plain git, so it goes through Git LFS, as the textures already do. Its size, and whether it fits the repo's LFS quota, are measured by probe 3.

**Two ways to run the same project**, one flag in the driver:
- **Editor-hosted** on any machine with Unreal 5.8 (`UnrealEditor <project> -game -RenderOffscreen`). This is the development loop, with no packaging step.
- **Packaged** on any Linux GPU machine with no Unreal install. This is the portable deliverable the lead asked for.

**How a render works, and where each job lives:**
1. **The rig (Python) does the thinking.** It turns `job.json` and the article's `.mtlx` into a flat per-setting list: the master token, each parameter value, and each texture's file and colour space. It reads the `.mtlx` the way the Blender loader already does (`blender/masters/load_article.py` `read()`, plain XML), so **Unreal never parses MaterialX**. That is one reader, shared by two tools.
2. **The Unreal app (C++, small) does the rendering.** For each setting it makes an instance of the named master and sets its values. It loads each PNG at run time, colour textures as sRGB and data textures as linear. **Each texture's colour flag must match its sampler type.** The platform learned that a mismatch makes a material silently render as Unreal's default grey, with every check green. The app assigns the instance to the subjects, captures, and writes the file.
3. **Capture in linear light, and encode in Python.** The app writes the scene's **linear, pre-tonemapper** colour as a float image (EXR). The driver then does the plain sRGB encode that Storm and Blender do, and applies the `dim` view's exposure itself. **Unreal's tonemapper and auto-exposure are then out of the path entirely,** which removes two of BigPicture's named risks by design, not by settings. For anti-aliasing, render large and shrink, as Storm does (`storm_supersample`). *(Unverified: that Substrate's translucency and refraction appear in the captured linear colour.)*
4. **Match the lighting:** no shadows, no GI bounce, and reflections of the dome only; a sky light from the constant 0.503 dome and a sun at 1.5. Calibrate on the grey card before judging any material (`JOB_FORMAT.md`).

**One detail for discovery:** each setting's scene divides the subjects' UVs by the article's `meters_per_tile`. Doing that inside the master would not equal doing it on the mesh once `uv_offset` and rotation are involved, and the masters are Studio's too (P20), so they should not carry a rig-only input. The app should rewrite the mesh's UVs at run time. The character job's rule is the same: import the setting scene's `st`, never the mesh's own.

## Pass 6 — The probes, in order (a hypothesis for `/discovery`, not a plan)

Each probe is small, and each settles one unknown before anything is built on it. Probes 0–1 need **no GPU** and are safe while the other agent works. Probes 2 and later need a moment the lead picks (UR-Q5).

| # | Probe | GPU? | Settles |
|---|---|---|---|
| 0 | Scaffold the project and the driver's Python half. Check that the flat per-setting list matches the Blender loader's values for the 11 test articles. | no | the seam |
| 1 | A commandlet (`-nullrhi`) that lists `MX_OpenPBR_Opaque`'s real inputs and builds the **Opaque** master on it | no | UR-F2 for real; whether a master can wrap Epic's function |
| 2 | **Grey sphere**, editor-hosted, `-game -RenderOffscreen`, captured twice | yes (first launch; announce it) | headless capture works, and the output is identical from run to run |
| 3 | **Package it** (Shipping), then run the grey sphere from the package in a clean folder with no display variables set | yes | the package is standalone and headless; its size on disk |
| 4 | `GreyCard_Neutral18` through the rig: the first real Unreal cell | yes | lighting and colour calibration against Storm and Blender |
| 5 | The other masters, then the 11-article test set and the character job | yes | the Unreal column |
| 6 | Run the package on another Linux machine, or in a GPU container on this one | yes | "bring it to any Linux machine" |
| opt | Interchange-import the 11 test articles in the editor | yes | Epic's own reading as a reference column (Pass 3) |

**Probes 0–3 are the risky part.** Once they pass, the rest is the master work Phase06 already scopes.

## Pass 7 — Probes 1–3 run (2026-09-29)

**All three held.** The results are in `260929_R_Spike_UnrealRuntime.md`, and the probe sources are committed beside it.
- **Probe 1:** a script builds a master on Epic's Substrate OpenPBR function in about 6 s, with no GPU. It registers 21 parameters by their OpenPBR names (UR-F4, UR-F5).
- **Probe 2:** editor mode renders headless. A settled capture is byte-identical from run to run, but a capture taken too early gets Unreal's default material, so readiness must be checked explicitly (UR-F7). The first launch compiled shaders for about 12 minutes; later runs take seconds (UR-F6).
- **Probe 3:** the package builds with 0 errors. It runs with no display (SDL `dummy`) and gives byte-identical output, in 4 s once warm. It needs about **620 MB** and glibc 2.28 (UR-F8), and agrees with editor mode to 0.9 % (UR-F9).
- **Not yet calibrated:** the grey sphere reads about 2.5× brighter than a hand estimate. That is probe 4 (UR-F10).
- **For UR-D3:** about 620 MB per package goes through Git LFS, and every rebuild adds to the history.

---

## Open questions

| # | Question | Recommendation |
|---|---|---|
| ~~UR-Q1~~ | ~~Does Phase06 run on this machine?~~ **Yes (UR-D1).** | — |
| UR-Q2 | Build the Unreal masters by wrapping Epic's `MX_OpenPBR_*` functions? | **Yes: probe 1 held** (Pass 7), for Opaque, TwoLayer, Masked, Emissive and both Translucent masters. Subsurface and Hair take Unreal's better model where the LCD ruling's candidates call for it. |
| ~~UR-Q3~~ | ~~Where does the package live between machines?~~ **In this repo (UR-D3).** Git LFS quota and size are measured by probe 3. | — |
| UR-Q4 | Real time or Unreal's path tracer for the column? *(Phase06's own)* | **Real time, captured linear** (Pass 5): it is what Studio users see. The path tracer is an optional later check; it is unverified on Linux. |
| ~~UR-Q5~~ | ~~When may GPU probes run?~~ **Ask before each launch (UR-D2).** | — |
| ~~UR-Q6~~ | ~~A second Linux machine?~~ **Yes: the machine that built Phases 05–08 (UR-D3).** | — |
| UR-Q7 | Keep the Unreal project's binary assets out of git by rebuilding them from scripts? | **Yes, as the aim.** Probe 1 shows whether the masters regenerate cleanly. The level may need to be committed if scripting it proves fragile. |

**Settled by probes 1–3 (Pass 7):** a headless packaged Linux build with Substrate · the real inputs of Epic's OpenPBR functions, and whether they survive packaging · the package's size (about 620 MB needed). **Still unverified:** linear capture including translucency and refraction (5) · the package on another machine (6) · a project-local cache in the installed build · how much of our nodegraph Interchange imports (opt) · the organisation's Git LFS quota.

## Status

- **Passes captured:** 7 (2026-09-29). Passes 1–6 were read from disk; Pass 7 ran probes 1–3, which all held (`260929_R_Spike_UnrealRuntime.md`).
- **The answer:** yes. Build a small C++ Unreal 5.8 project in this repo, with its masters built by script, and package it for Linux. The rig drives it through a fourth driver and gets pictures back. It runs editor-hosted on any machine with Unreal, and as a package on any Linux GPU machine without one.
- **Key finds:** Unreal 5.8 is on this machine (UR-F1). **Epic ships OpenPBR, with our parameter names, and MaterialX's `place2d`** (UR-F2). Epic's own importer splits OpenPBR as our master set does (UR-F3).
- **The risk:** sharing the machine with the IMRSV agent. It is handled by looking before launching, doing most of the work with no GPU, capping builds and shaders, changing nothing shared, and telling the lead before the first launch (Pass 4). Disk headroom is about 27 GB.
- **Decided (UR-D1–D3):** Phase06 runs here, the lead approves each GPU launch, and everything, the executable included, lives in this repo for the other machine to pull.
- **Open:** UR-Q2, UR-Q4 and UR-Q7, each with a recommendation.
- **Next step:** `/discovery Phase06` on this machine, starting from Pass 7 and the spike. The spike lists what is left: calibration, the rest of the masters, the driver and scene, a readiness signal, a Shipping build small enough for the repo, and the run on the other machine.
