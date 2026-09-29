# Phase06 — Unreal Test Runtime

**Status:** ACTIVE: discovery complete, the Brief is ready (2026-09-29, Pass 1). Lane: `build` (verified, §Risk lane). No `YOUR CALL` item is open (§Discovery Status). Pass 2 (the same day) folded in the MAP research and Phase09's seed, which decide the hair and eye questions.
- **Seeded** 2026-09-26 from `docs/Planning/Research/260926_R_BigPicture_NimbleSetup.md` (Passes 7, 8). Numbered by the lead the same day.
- **Opened** 2026-09-29 (lead: *"push it and start /discovery Phase06"*), after `260929_R_UnrealTestRuntimeHere.md` (the plan, UR-D1–D3) and `260929_R_Spike_UnrealRuntime.md` (probes 1–3 passed).
- **Runs on this machine, the UE machine** (UR-D1, lead: *"yes run it here"*). The other machine, where Phases 05, 07 and 08 were built, has no Unreal. It pulls the package and tests it (UR-D3).

## Outcome

**The test rig's picture sheet gains an Unreal column, rendered by a small Unreal app of our own that runs on any Linux machine with a GPU.**

Concretely, at close:
- `rig.py <article>` fills the sheet's Unreal column for the 11-article test set and for the character job, and its scorecard reads how each slider moved Unreal.
- The pictures come from a packaged Unreal 5.8 app (Substrate on) that lives **in this repo**, so the other machine pulls it and renders the column with no Unreal installed.
- Its 8 masters are the ones Studio will adopt (`PlatformDependencies.md` P20).

## The Brief

### First human test

**Click 1 — the grey card, on this machine** (step 6.1).
- **What the lead opens:** the sheet `library/parity/GreyCard_Neutral18_Clean_Base_s01_v01/sheet.png`, which the agent renders.
- **What the lead judges:** the third column is Unreal's picture of the same scene: sphere, rounded cube, floor with the 10 cm ruler, and the UV-grid wall. The grey reads as the same grey as Storm and Blender, lit from the same side, with the dome behind.
- **The numbers under it:** the agent reports Unreal's linear radiance against the other two, with the calibration factor it measured.

**Click 2 — the same sheet, made on the other machine** (step 6.2).
- The lead pulls this repo on the other machine, and its agent runs the rig on the grey card.
- **What the lead judges:** the sheet made there has the Unreal column, although that machine has no Unreal installed.

**Click 3 — the sliders** (step 6.3).
- **What the lead opens:** the `Copper_Verdigris_Aged` sweep sheet.
- **What the lead judges:** each slider (tint, UV scale, rotation, offset, the wear layers, the mask blend, the roughness bias) moves the Unreal picture the same way it moves the other two. The dust sits at the same size against the ruler.

**Click 4 — the rest of the masters** (step 6.4).
- **What the lead opens:** the sheets for `Rust_OnSteel_Flaking`, `Lace_Floral`, `Neon_Signage` (with the dim view), `Glass_Clear`, `Glass_Green`, `Diamond_Brilliant` and `Marble_Veined_Polished`.
- **What the lead judges:** each master's matter reads right in Unreal: the rust sits in the mask, the lace has holes, the neon glows, the glass shows the wall through it, and the marble lets light in.

**Click 5 — the character** (step 6.5).
- **What the lead opens:** `rig.py --character` sheets for two skin tones.
- **What the lead judges:** skin, eyes, mouth, nails, clothes and hair in Unreal's column, with no default grey and no magenta. The hair is matte and the eyes are today's articles on the rig's eye, which still has its cornea shell (MAP-F12). Both improve in Phase09.

**Click 6 — the close.** The other machine pulls the final package and renders the Unreal column for one sweep sheet and one character sheet.

### In now

- **The Unreal project, in this repo at `unreal/`,** as the peer of `blender/`. It is built from scripts: the C++ runtime, config, and the Python that builds the masters, the scene and the dome. No hand-made `.uasset` is committed; the probe proved every asset regenerates (UR-F5).
- **One command builds the package from scratch:** the editor target, the masters, the scene, the cook, and a stripped Shipping build. It runs on any machine with Unreal 5.8, with capped jobs and `nice`.
- **The package, in this repo through Git LFS** (UR-D3). It is the Shipping build, with no debug symbols, no Vulkan debug layers and unused plugins off.
- **The 8 masters** (MasterSet): Opaque, TwoLayer, Masked, Hair, Emissive, TranslucentThin, TranslucentThick and Subsurface. Each wraps Epic's `MF_Substrate_OpenPBR_{Opaque,Translucent}` and is built out with our own network around it (§Decisions that bind, D6).
- **The Unreal driver,** `tools/parity/drivers/unreal.py`, which implements `JOB_FORMAT.md` for both job shapes (the test scene and the character).
- **The rig gains its third column:** `rig.py` runs the Unreal driver when a runtime is present. The sheet shows Unreal's pictures, and the scorecard reports how each slider moved Unreal, beside Storm and Blender.
- **The rig's verdict becomes the "Moved" agreement,** with picture ΔE demoted to a diagnostic. `_Architecture.md` §LCD owns this ruling and lists it as a Todo; a third column is when it bites (D9).
- **Docs at close:**
  - `ToolingConventions.md` gains an `unreal/` row;
  - `JOB_FORMAT.md` gains the Unreal driver's notes;
  - MasterSet and Consumers now say where the Unreal masters are built: here (P20);
  - a new `docs/Learnings/Unreal/` domain, from UR-F4–F10;
  - `PlatformDependencies.md` P20 gets where Studio takes the masters from.

### Not now

- **Studio adopting the masters (P20).** That is the platform's work. This phase builds the masters Studio will take; *Unreal Reference Masters* publishes them.
- **Unreal's path tracer as a second Unreal column** (UR-Q4). The real-time column is what Studio users see.
- **The `Eye` master, and the hair's and eyes' picture input:** Phase09's (D13). Phase09 builds their Unreal side in this phase's project, and judges them on this phase's column.
- **Strand hair (grooms):** MAP-RD4, a phase of its own. Candidates 2 and 3 (Unreal's skin and cloth) are judged on the column, not built up front (D7).
- **Re-judging the character articles** that Phase07 and Phase08 left as candidates. The column makes that possible; it is the next unit, not this one.
- **New or changed articles.** No contract change is needed: the Hair master is built on today's `Hair` row, read through MAP-RD3 (D12).

### Reuse check: what the stack already gives us

| Need | Native | What we add, and why |
|---|---|---|
| The OpenPBR BSDF | **`MF_Substrate_OpenPBR_{Opaque,Translucent}`** (core engine; OpenPBR's names; Substrate front material) | Nothing to the BSDF. The masters wrap it. |
| MaterialX UV placement | `MX_Place2D` (Interchange assets) | Use it, **after checking its maths** against LCDSchema's `place2d` (divide by scale, rotate, subtract offset). If it differs, we write the same few nodes the Blender master has. The platform hit the look-alike trap with `UsdTransform2d`. |
| The wear layers, mask set, two-layer blend, cut-out, opacity floor | none (it is our contract: MasterSet §Overlay/MaskSet, §TwoLayer blend, §Scale, §Opacity floor) | Our network around Epic's function, a port of `blender/masters/build_masters.py`'s `_build`. |
| Building assets by script | `PythonScriptPlugin` + `MaterialEditingLibrary`, as a `-nullrhi` commandlet (UR-F5) | The build scripts. |
| The scene | USD importer (`USDStageImporter`, a commandlet) | The import is scripted. It must honour the root layer's `metersPerUnit` (`JOB_FORMAT.md`; learning B7). |
| Loading textures at run time | `FImageUtils` / `ImageWrapper` → `UTexture2D` | Setting the colour flag and the compression to match each sampler's type. A mismatch renders Unreal's default material with every check green (platform learning). |
| Capture | `USceneCaptureComponent2D` to a float target, `SCS_SceneColorHDR` (UR-F8) | A per-view camera, supersampling, and writing the file. The encode stays in Python, like the other drivers. |
| Reading the article | `blender/masters/load_article.py` `read()` (plain XML) | **Move it into a Blender-free module that both drivers import.** There is one reader, not two. |
| Job, scene, comparison, sheet | `tools/parity/` (Phase05) | The third column and the "Moved" verdict. |
| Headless, standalone run | `-RenderOffscreen` on SDL `dummy`; a package that needs glibc 2.28 (UR-F8) | None. |

### Decisions that bind

| # | Decision | Source |
|---|---|---|
| D1 | Runs on this machine, the UE machine. **Ask the lead before each GPU launch.** Before any launch, check for a running Unreal and name its owner; never touch the IMRSV project. | UR-D1, UR-D2; research Pass 4 |
| D2 | **Everything lives in this repo, the executable included:** the package goes through Git LFS, so the other machine pulls and tests it. | UR-D3 |
| D3 | **A standalone packaged runtime is the deliverable.** Running the same project in the editor is the development loop. | BP7; UR Pass 5 |
| D4 | **These are Studio's masters.** Build them as the shared masters: Unreal's best feature per master, never a test-only stand-in. | P20, lead 2026-09-28: *"yes, Studio adopts the library masters, record it"* |
| D5 | **Parameter names are the article's names**: OpenPBR's for lane A, the frozen Creator ports, and the author-tier names (`opacity_cutoff`, `layer2_*`, `layer_blend_*`, `cutout_map`). Studio aligns to them (P20). *(The platform's snake/Pascal split was consumer-side and does not bind the library's masters.)* | LCDSchema: *"Names use OpenPBR-aligned terms so the same word means the same thing in MaterialX, the Unreal instance param, and the Blender node-group input"* |
| D6 | **Each master is Epic's Substrate OpenPBR function plus our network:** `place2d`, the per-article textures, the tint, `roughness_bias` clamped to 0..1, up to three overlays gated by the mask set, the TwoLayer blend, each layer at its own scale, normals combined in tangent space and converted once, and the cut-out. The settings come from MasterSet §Material-settings intent, and the translucent masters keep the 0.05 opacity floor. The formulas are MaterialX's, copied; `build_masters.py` is the worked reference. | MasterSet; LCDSchema; learning M1; UR-F4 |
| D7 | **Unreal's best features, per the LCD ruling, are measured on the column, not assumed.** Epic's Substrate OpenPBR already renders fuzz, coat and subsurface natively (candidates 2 and 3). A dedicated skin profile or Cloth model is added only if the column shows a gap. Hair's coverage is dithered, per its MasterSet row; Masked stays alpha-tested at the cutoff, per its row. | `_Architecture.md` §LCD, lead 2026-09-28: *"we use the master materails to lean in on the egines BEST qaulities"*; MasterSet settings table |
| D8 | **Real time, captured linear, encoded in Python.** The app writes linear scene colour (before the tonemapper) with exposure fixed at 1. The driver applies the view's `exposure`, box-filters the supersampling and does the plain sRGB encode. Lighting is matched: no shadows, no GI, no screen-space or Lumen reflections, a constant dome and a sun, calibrated on the grey card as Blender's `DOME_K` / `SUN_K` were. | UR Pass 5; UR-Q4; `JOB_FORMAT.md` |
| D9 | **The rig's verdict is the "Moved" agreement:** each slider moves every tool the same way. Picture ΔE is a diagnostic that flags real bugs; it is not a bar. | `_Architecture.md` §LCD, *"Todo, make the 'Moved' agreement the criterion and demote picture ΔE to a diagnostic"* |
| D10 | **The dome is not a hand-written flat `.hdr`.** Storm misread one (learning S2), and the probe's own 2.5× over-brightness (UR-F10) may be the same trap. Generate the cubemap from a format read exactly (EXR), and verify its value in Unreal before calibrating. | Storm S2; UR-F10 |
| D12 | **The Hair master is matte on cards.** It is default lit with no specular sheen, not Unreal's hair shading model, which reads a flat card as one glossy sheet. Its coverage is soft and dithered, per the MasterSet row. The hairstyle's picture shading the article's light colour (modulate) is Phase09's input; the master takes it when Phase09 lands. | MAP-RD3, lead: *"yes on hair"*; *"The matte look the lead approved at the platform's sitting is where card quality stops"* |
| D13 | **The eye and the hair picture belong to Phase09, including their Unreal side, built in this phase's `unreal/` project.** Phase06 builds the 8 masters and the column that Phase09 then judges on. | Phase09 seed §Scope In: *"The `Eye` token and its settings row; its Unreal side where the library's Unreal masters are built"*; MAP-RD6 |
| D14 | **A package version goes through LFS twice: at 6.2 and at the close.** A master change in between does not push a package; the other machine renders from the newest pushed one. | Lead, 2026-09-29: *"yes and 6.2 and close (not every master change)"* |
| D11 | **A capture waits for the material to be ready,** by a signal that works. The probe caught Unreal's default material once, and `IsGameThreadShaderMapComplete` did not work as a signal (UR-F7). The package precompiles its shaders, so the risk is mostly in editor mode. | UR-F7 |

### Risk lane: `build` (verified)

- **Controls read.** `tools/validators/run_all.py` and `tools/releases/*` enumerate only their own roots: `MatterLibrary/materials/**/*.mtlx`, `library/releases/*`, `tools/converters/recipes/*.json` and the staged `*.dds`. A new `unreal/` root, and LFS files under it, are in none of them.
- **Nothing touches authorization, secrets, data or the public web.** The phase adds tooling and one binary, both under Apache-2.0.
- **The one account-side entry path is GitHub LFS on the organisation's Team plan,** measured with `gh api orgs/Imrsv-tools/settings/billing/usage` (2026-09-29):
  - about 43 GB stored (29–32k GB-hours a month) and 14–15 GB of downloads a month, across the organisation;
  - August went over the included allowance (net $4.29); July and September were $0;
  - one ~620 MB package version adds about $0.04 a month of storage, and each pull about $0.05.
  - Pushing it is public and irreversible, so how often a package is pushed is the lead's call: D14.
- **The test surface:** the existing gate (`run_all.py`), the rig's own runs (the smoke is the sheet), and one check: the shared article reader gives Blender the same values after the move. No new gate.

### Step list

- **6.1 — The grey card in the Unreal column (this machine, editor mode).**
  - `unreal/` holds the project from the probe.
  - The Opaque master's first form: constants and tint, no textures yet.
  - The rig's scene is imported, with its cameras.
  - The dome and sun are calibrated (D10); anti-aliasing is by supersampling.
  - `drivers/unreal.py` and the rig's third column.
  - **First clickable result:** click 1.
- **6.2 — The package, pulled on the other machine.**
  - The one-command build; a stripped Shipping package in `unreal/package/` through LFS.
  - The driver uses the package by default, and editor mode on request.
  - **First clickable result:** click 2. *(Early by design: it proves the lead's portability ask before the masters grow. The next pushed version is the close's (D14).)*
- **6.3 — The Opaque master in full, with textures and sliders.**
  - Textures load at run time with the right colour settings; `place2d`; the normal; the three overlays and the mask set, each at its own scale; the roughness bias.
  - Coat, fuzz and specular anisotropy.
  - Articles: `ABS_Glossy`, `Oak_Natural` and the `Copper_Verdigris_Aged` sweep.
  - **First clickable result:** click 3.
- **6.4 — The other masters on the test set:** TwoLayer, Masked, Emissive, TranslucentThin, TranslucentThick and Subsurface. That completes the 11 articles. **First clickable result:** click 4.
- **6.5 — The character job and the Hair master.**
  - `bindings`, `cutout_map`, the per-view `hide`, and the setting scene's `st`.
  - The Hair master, matte on cards (D12).
  - **First clickable result:** click 5.
- **Close.** The final package through LFS (click 6), then the docs listed in §In now.

**Reconciled against the test:**
- Click 1 needs only 6.1: a flat grey card uses no textures and no sliders.
- Click 2 needs 6.1 and 6.2.
- Click 3's sliders all live on the Opaque master: `maskset_blend` and the overlays are Opaque's network (MasterSet); Copper is Opaque.
- Click 4's Rust needs TwoLayer (6.4). Glass needs the UV-grid wall, which is in 6.1's scene.
- Click 5 needs the Subsurface master (6.4) for skin and the Hair master (6.5).

**Time to first click:** 6.1 reuses the probe's app, but adds the scene import and the calibration. It may run past 90 minutes; if so, the calibration is where it goes.

### Compact build map

- **`unreal/MatterRuntime/`:**
  - `MatterRuntime.uproject`; `Config/` (Substrate on with Adaptive GBuffer, Vulkan SM6, GI and reflections off, `r.PSOPrecache.ProxyCreationStrategy=0`, shader threads capped);
  - `Source/MatterRuntime/`: the probe's GameMode, grown to read an "Unreal job" JSON (per setting and view: camera, subjects, materials with their master token, parameters and textures, the colour space of each, and `hide`), and to write one float image per setting and view;
  - `Scripts/`: `build_masters.py` (one builder shared by the 8 masters), `build_scene.py` (commandlet USD import of `test_scene.usda` and `character_scene.usda`), `build_env.py` (the dome).
- **`unreal/build.sh`:** editor target → masters → scene → `BuildCookRun` (Shipping, `-MaxParallelActions=8`, `nice`) → strip → `unreal/package/Linux/`.
- **`.gitattributes`:** `unreal/package/** filter=lfs`. **`.gitignore`:** the project's `Binaries/`, `Intermediate/`, `Saved/`, `DerivedDataCache/` and its generated `Content/`.
- **`tools/parity/drivers/unreal.py`:**
  - turns the job into the Unreal job, using the shared reader;
  - finds the runtime from `$MATTER_UNREAL_RUNTIME`, then the repo's `unreal/package/Linux/MatterRuntime.sh`, or editor mode from `$MATTER_UNREAL_EDITOR`;
  - runs it with `env -u DISPLAY -u WAYLAND_DISPLAY`, then turns each float image into an 8-bit sRGB PNG (exposure applied, box-filtered).
- **The shared reader:** `read()` / `ArticleData` move out of `blender/masters/load_article.py` into a module that does not import `bpy`. `load_article.py` imports it back. `tools/conformance/check_exporter.sh` is baselined before the edit (the LOCAL_DELTAS "RUN" row) if the move touches `blender/`.
- **`tools/parity/rig.py`:**
  - `run_unreal()` beside `run_blender()`, skipped with a notice when no runtime is found;
  - the sheet's Unreal column;
  - "Moved" for all three tools, and the verdict per D9.
- **Where to start reading:** the probe sources (`docs/Planning/Research/260929_R_Spike_UnrealRuntime/`); `blender/masters/build_masters.py` (the network to port); `JOB_FORMAT.md`; `drivers/blender_render.py` (the lighting constants, the views, the `hide` handling).

## Discovery Log

### Pass 1 (2026-09-29): the product docs, top-down, read against the Outcome

**Examined:**
- `_Architecture.md` §LCD (the 2026-09-28 ruling);
- MasterSet: the overlay and mask set, the TwoLayer blend, §Scale, colour space, the settings table, the opacity floor;
- LCDSchema: the author tier, the Creator subset, the cut-out map, the render-role nodes;
- Consumers (IMRSV) and `PlatformDependencies.md` (P16, P18, P20, M1, M3);
- `JOB_FORMAT.md`, `rig.py`, `job.py`, `drivers/blender_render.py`, `blender/masters/build_masters.py` and `load_article.py`;
- the Phase05, 07 and 08 hand-offs;
- the research threads UR, BigPicture and HS;
- the learnings: MaterialX M1–M4, Blender B6/B7, Storm S1/S2/S4/S5;
- `ToolingConventions.md` roots;
- the gates' globs;
- the organisation's LFS billing.

**Findings:**
- **F-P06-1 — The seed's scope is carried, and three facts sharpen it.**
  - Epic ships the OpenPBR BSDF on Substrate, so a master is Epic's function plus our network, and the network is exactly what `build_masters.py`'s `_build` already implements for Blender (D6).
  - Epic's Substrate OpenPBR renders fuzz and coat natively. The seed's candidate 3 (Unreal's Cloth model for fuzz fabrics) is therefore likely delivered by D6, and is measured rather than built (D7).
  - The master count is 8 since Phase08.
- **F-P06-2 — The rig already reserves the Unreal column** (`rig.py` prints *"Unreal: no pictures yet"*). It compares only Storm with Blender, and its bar is still picture ΔE < 2. The LCD ruling's Todo moves the verdict to "Moved", and a third tool is when a pairwise ΔE bar stops being meaningful (D9).
- **F-P06-3 — The reader exists; only its home is wrong.** `load_article.read()` is plain XML and already yields everything the Unreal job needs: ports, lane-A values, textures with colour spaces, layer scales and constants. It sits in a module that imports `bpy`.
- **F-P06-4 — The Hair master had an open contract question upstream** (HS-Q3: restate Hair's Unreal realisation as matte, coloured by the mesh's picture). *Answered in Pass 2 by MAP-RD3 (D12).*
- **F-P06-5 — The seed's open questions are closed.**
  - "Is 5.8 available?" Yes (UR-F1).
  - "Real time or the path tracer?" Real time, captured linear (D8).
  - "Where does the package live?" In this repo (UR-D3).
- **F-P06-6 — The dome may be the over-brightness.** The probe wrote a flat Radiance `.hdr`, the same shape Storm misread (S2). That may be UR-F10's 2.5×; D10 makes 6.1 verify it first.

**The seed's coupling notes, compressed.** Phase07 and Phase08 landed:
- the carriers coat, fuzz, subsurface scatter anisotropy and specular anisotropy;
- the Masked `cutout_map`;
- the `Hair` master;
- Subsurface nails with a coat;
- the character job, with its `Soles` part.

All of it is in the contract docs and `JOB_FORMAT.md`, which this Brief binds to. The LCD candidates 1–5 are dispositioned in D7 and §Not now.

### Pass 2 (2026-09-29): the MAP research and Phase09's seed, pulled from the other machine

**Examined:** `260929_R_CharacterMaps.md` (its rulings MAP-RD1–RD6, Passes 7–8, the open questions and Status, all read); `Phase09_HairAndEyeMasters.md` (the seed); and the engine's Substrate eye BSDF (`MaterialExpressionSubstrate.h`, Unreal 5.8.0).

**Findings:**
- **F-P06-7 — Hair is decided: matte on cards, with the picture as Phase09's.** MAP-RD3 as amended answers the HS asks the library's way: the hairstyle's picture **shades** a light article (modulate), and *"the matte look … is where card quality stops"*. So Phase06's Hair master is matte, without Unreal's hair model (D12). The picture input and the `Hair` graph change are Phase09's contract work (D13). This retired Pass 1's YOUR CALL 1.
- **F-P06-8 — The `Eye` master is Phase09's, built in this phase's project.** MAP-RD6 adds a 9th token, and Phase09's seed scopes its Unreal side. MAP-Q13 read "Phase06 / Unreal Reference Masters build it"; the two agree once Phase06 is the project and the column, and Phase09 the eye (D13). Phase06 builds no Eye master.
- **F-P06-9 — Evidence for MAP-Q12 (for Phase09's discovery).** Unreal 5.8's **Substrate Eye BSDF** takes one surface's `DiffuseColor`, `Roughness`, `CorneaNormal`, `IrisNormal`, `IrisPlaneNormal`, **`IrisMask`**, **`IrisDistance`**, `EmissiveColor` and a Subsurface Profile. The iris is a **masked region of one eyeball material**, not a material of its own. That supports **one `Eye` article bound on all three parts**, with the mask and distance computed from the eye's shared UV layout (the parts share it, MAP-F11). No refraction function ships in engine content; the eye's refraction offset is built in the graph. *(Read from the header, not rendered.)*
- **F-P06-10 — Click 5 judges today's eye.** The rig's eye still has the cornea shell Studio dropped (MAP-F12). Phase06 renders it as it is; the eye's real judgement is Phase09's.

## Discovery Status

- **Passes captured:** 2 (2026-09-29).
- **Current working direction:** the Brief above. The project is in `unreal/`, the masters are Epic's OpenPBR plus our network, the package goes through LFS, and the rig gets its third column and the "Moved" verdict. The Hair master is matte on cards (D12); the Eye master and the hair and eye pictures are Phase09's, built in this project (D13).
- **Open decisions:** none.
  - ~~The package's LFS commits~~ **Ruled (lead, 2026-09-29): *"yes and 6.2 and close (not every master change)"*** (D14).
- **Checks to carry forward:** D1's look-before-launching before every GPU run · D10 before calibrating · D11 in editor mode · `check_exporter.sh` baselined before the reader move touches `blender/`.

## Execution Log

_(populated during execution)_
