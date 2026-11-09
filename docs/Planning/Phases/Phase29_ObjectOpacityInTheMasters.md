# Phase29 — Object Opacity in the Masters

**Status:** IN EXECUTION (2026-11-09), step **29.3, the fade as fine grain**. Reopened the same day — the lead: *"stay in this phase and update the doc - it is OK that it is closed... we will just close it again"*. ▶ `/execute P29` (29.3 only). First closed 2026-11-09 (`1560610`; runtime `unreal-runtime-v8`) after 29.1 and 29.2. BRIEF READY the same day (discovery in session `ML_R_VariousQuestions`). Seeded the same day on the lead's *"do both — quick-fix the ledger row, then seed the phase... We are paused on all the skin work right now... this will be the next phase we do"* (RD-POA-1). Discovery was opened with *"go ahead with discovery"*. **Runs next**, ahead of the paused skin work (Phase28 included). Lane: **build**. ▶ `/execute P29`.

## Outcome

**A Character, Prop or Set drawn with the library's materials fades in and out in Unreal: part-faded, it dissolves into what is behind it and never turns to glass, so two versions of one character cross-fade cleanly. While it is fully there, it draws and costs exactly what it does today.**

*Who it is for:* the platform's Creators, who key an object's Opacity on the timeline (`PlatformDependencies.md` M15). Other USD apps see a clean swap. No article reads the value, so Blender and Storm are untouched.

**Source:** [`../Research/261105_R_PlatformObjectOpacityAsks.md`](../Research/261105_R_PlatformObjectOpacityAsks.md) — the platform's asks (Pass 1) and the library's reading (Pass 2, F-POA-1 … 8). This Brief is the one authoritative copy of what the phase builds. The research keeps the evidence.

## First human test

**Where:** the lead's desktop on the machine with Unreal. The pictures are opened with `xdg-open`, and the handback carries their paths.

**⛔ Native resolution, not the rig's supersampled picture.** The rig and the look view render 4× (look: 2×) and average each block (`drivers/unreal.py` `SUPERSAMPLE`; the capture has anti-aliasing off). That average turns a 4 × 4 dissolve into a smooth see-through fade, which is the look the platform ruled out and the headset never shows. **So every click's picture is rendered at one sample per pixel** (F-P29-1). At the click camera the dissolve's cell is 1 pixel and its tile is 4 × 4 pixels, read at 100 %.

1. **Click 1 — every master at half (29.1).**
   - **Picture:** the rig's 11-article sheet rendered at presence 0.5, one sample per pixel, beside the same sheet at presence 1.
   - **Fixtures:** the 11 articles span Opaque (the grey card, ABS, Copper, Oak), TwoLayer (Rust), Masked (Lace), Emissive (Neon), TranslucentThin (Glass_Clear, Glass_Green), TranslucentThick (Diamond) and Subsurface (Marble). Near-white, near-black, metal, glass and a light are all in the set. Hair is in click 2.
   - **What the lead judges:** each article is an even scatter of whole pixels, half the article and half the backdrop. None reads as tinted glass. Lace keeps its holes. The diamond's dropped pixels show the backdrop unbent.
   - **The sentence afterwards:** *"every master dissolves at half, and none turns to glass."*
2. **Click 2 — two versions of the character cross-fading (29.2).**
   - **Picture:** the look view's `face` and `face34`, at one sample per pixel.
   - **Fixture:** the rig's character, cast twice in the same place, wearing two skins far apart in tone (`Skin_Fitzpatrick` I and VI). One copy fades out and the other fades in, at 50/50 and 25/75. Beside it, the character alone at 50 %, in front of the look view's backdrop.
   - **What the lead judges:**
     - in the cross-fade, every pixel of the character is one skin or the other: no backdrop shows through the character, and the two skins' share follows the split;
     - the character alone shows no teeth, eye interior or hair-under-skin through the face;
     - the hair and eyes dissolve with the head;
     - the shadow thins with the character.
   - **The sentence afterwards:** *"two versions of one character cross-fade with no holes and no insides."*

The headset's FXAA and its frame cost are judged in the platform's app, not here (§Not now).

## In now / not now

- **In:**
  - the eight masters' dissolve (29.1);
  - the four masked instances (29.1);
  - the value's spec in `MasterSet.md` (29.1);
  - the runtime and driver writing the value and swapping to the instance (29.1);
  - the rig's half-presence sheet (29.1) and the look view's cross-fade (29.2);
  - the ledger's handover to the platform (at the close).
- **Not now:**
  - **the platform's side:** writing the value, its own swap, the start-up precache, the bake to a clean swap, the effect overlay, and the FXAA headset look (its own gate);
  - any article, Creator port, Blender master or Storm change (F-POA-8);
  - **publishing a new runtime** (RD-P29-5).

## Decisions that bind

*The lead ruled the phase (RD-POA-1) but not its design. These are the agent's calls from Pass 2, settled **unless the lead says otherwise**.*

- **RD-P29-1 — One rule for every master.** A pixel is kept when its 4 × 4 threshold (`bayer4()`, Hair's own) is below *(how present the object is) × (the master's own coverage)*:
  - **Hair:** its soft coverage × presence.
  - **Masked:** a second test beside its alpha test; the pixel must pass both.
  - **Opaque, TwoLayer, Emissive, Subsurface:** the same test on the opacity mask, which an opaque master ignores.
  - **TranslucentThin, TranslucentThick:** the same dither; a dropped pixel draws no glass **and bends nothing**. The bend is zeroed at dropped pixels always, rather than only if a probe shows it (this closes Q-P29-1).
- **RD-P29-2 — One masked instance per solid master,** for Opaque, TwoLayer, Emissive and Subsurface:
  - blend mode overridden to masked, clip overridden to 0.5 (Unreal's default is 0.3333);
  - no graph and no parameter of its own;
  - built by the same builder under `MATTER_MASTERS_ROOT`;
  - named for the master it overrides (`M_Matter_<Token>` → `MI_Matter_<Token>_Fading`).
  
  A consumer re-parents a part's material to it while the object is part-present. Unreal 5.8 compiles an instance asset's overrides into its own shaders (F-POA-2), so the instances, like the masters, need their shaders ready before first use (U7).
- **RD-P29-3 — The value.** One Custom Primitive Data float, `object_fade`, in **slot 0**:
  - **`object_fade` = how far the object has faded out.** 0 = fully there, which is also what an unset slot reads (F-POA-3). 1 = gone. **Negative = the copy fading in.**
  - **The tests:** the copy fading out keeps a pixel where `t ≤ 1 − |f|`. The copy fading in uses the mirrored threshold `1 − t`, which is the same 16 levels.
  - **A tie shows both copies, never neither** (Unreal keeps a pixel at or above the clip). This closes Q-P29-6.
  - The value is written into `MasterSet.md` beside the master table, as part of the producer↔consumer contract.
  - **Slot 0 is confirmed free by the platform** (2026-11-09, by message, after searching its code). Nothing reads or writes per-component data on the components that draw a library material: scene meshes, a Character, or a scatter's instanced component. Its planned effect overlay takes its values from its own material and will not write slot 0. Q-P29-5 is closed.
- **RD-P29-4 — A part-present object's shadow thins with it.** A masked shadow takes the same test in the shadow map's pixels. That is consistent with a dissolve, and at 0 the platform hides the object anyway (closes Q-P29-2).
- **RD-P29-5 — The runtime is built locally, not published.** This follows Phase26's precedent (M14: its makeup runtime was built locally).
  - The masters draw today's pixels at the default (the lead, 2026-10-05: *a builder change that alters nothing at its defaults needs no new runtime*).
  - The platform runs the library's builder itself, so it does not need our runtime.
  - The close offers the publish as the lead's word (closes Q-P29-4).
- **RD-P29-6 — The cost while fading is measured in the platform's headset, not here.** A headless capture's timing says nothing about the headset's frame. Here the mechanism is stated: a masked part writes its mask in the depth pass and loses early depth rejection, only while it is part-present (closes Q-P29-3).

## Rides on

`docs/CoreMechanisms.md` rows 1–4 are skin-map mechanisms. **This phase meets none of them.** The peers it follows:

| What in this phase | The peer we follow (opened this pass) |
|---|---|
| the dissolve's threshold | Hair's soft coverage: `build_masters.py` `bayer4()` and the Hair branch's `clip` (grep `bayer4(g, 10)`) |
| a master's mask and clip | Masked: `MP_OPACITY_MASK` + `opacity_mask_clip_value` 0.5 (grep `cannot connect the opacity mask`) |
| a second project builds the same assets | the M7 switches: `MATTER_MASTERS_ROOT` (grep `_told("MATTER_MASTERS_ROOT"`) |
| an older runtime refuses a job it cannot draw | Phase26's makeup: `drivers/unreal.py` `MAKEUP_JOB_FORMAT`; runtime `JobFormat` / `OldestJobFormat` in `MatterRuntimeGameMode.h` |
| a master's first use draws the engine default (U7) | `drivers/unreal.py` `warmup` |
| a master loaded by token | `MatterRuntimeGameMode::LoadMaster` (`/Game/Masters/M_Matter_<Token>`) |
| **NEW** — a value per object, and swapping a part to an instance | no peer. RD-P29-2 and RD-P29-3 (the agent's calls, above) |

## Reuse check

- **What the stack already gives:**
  - Unreal's material-instance property overrides (no second graph);
  - Custom Primitive Data (one value on a component reaches every section's material, with no per-material write);
  - Hair's `bayer4()` (a frame-stable screen threshold, already in the masters).
- **Custom layers proposed:** none. No custom dither, no per-material parameter write, no extra masters.
- **The contracts touched:** `MasterSet.md`, which gains the value and the instances and is the producer↔consumer contract (`Consumers.md` §IMRSV). The job format gains one field per mesh.
- **Not touched:** the frozen Creator-port vocabulary (`LCDSchema.md`).

## Risk lane — build

- **Controls read:**
  - `run_all.py` runs no Unreal lane. No validator, snapshot or test globs or hashes `unreal/` or the drivers (grep for `build_masters`, `MatterRuntime` and `drivers/unreal` in `tools/`: only the rig, look view, job and character builders, which this phase edits on purpose).
  - The one fingerprint is a doc tell: `JOB_FORMAT.md` §Which masters a runtime carries (`git log <pin source>..HEAD -- build_masters.py`). It will list this phase's commits. RD-P29-5 and the 2026-10-05 ruling answer it.
- **No high-rigor trigger:** no authorization, secret, migration, data loss or public edge. Publishing a runtime is out of scope (RD-P29-5).

## Step list

- **29.1 — Every master dissolves (click 1).**
  - The builder: the threshold test on all eight masters; the four masked instances; the glass bend zeroed at dropped pixels.
  - The runtime: per mesh, reads `object_fade` from the job, writes it to slot 0 and swaps a solid master's part to its instance when it is non-zero. Job format 6; formats 3–5 still read.
  - The driver and rig: `rig.py --fade <f>` with one sample per pixel.
  - `MasterSet.md`: the value, the instances, and the two-sided `Drift` note resolved.
  - **First clickable result:** click 1.
  - Before the first edit, baseline the rig's sheet at presence 1 and keep it. After the change it must match pixel for pixel (the default draws as today).
- **29.2 — Two versions of the character cross-fade (click 2).**
  - The look view casts the character twice in one place, each copy with its own skin and `object_fade` (`look.py --crossfade <skin> --fade <f>`), at one sample per pixel. The character alone at 50 %.
  - **First clickable result:** click 2.
- **29.3 — The fade is fine grain, not a grid** *(added 2026-11-09 at the reopen; the platform's ask [`261109_R_PlatformObjectFadeLookAsks.md`](../Research/261109_R_PlatformObjectFadeLookAsks.md), `OFL`, and the lead's rulings below)*.
  - **Why.** Seen in the platform's app, the 4 × 4 pattern is not good enough for a high-fidelity platform: under the Desktop's TSR it reads as a moiré that grows while the view is still (R-OFL-1); in the headset a slow fade steps through its 16 levels, each a visibly different regular pattern (R-OFL-2); and at 25 / 75 the cross-fade reads as a grid (click 2). Step 29.2's *"keep it"* on that grid is **replaced** by these rulings.
  - **The lead's rulings (2026-11-09):** a **blue-noise threshold** (Q-OFL-1); **an even fade on a view that averages over time**, the threshold varied per frame there and fixed on a one-sample view (Q-OFL-2); and **no technique that renders the scene twice** (an exact layer composite was offered and ruled out: the platform is VR-first and real-time, one render per eye — the lead: *"I think 1 is what we need to do"*, option 1 being this step).
  - **Build:** `fade_terms`' threshold becomes a tiled blue-noise texture on the screen pixel, many more than 16 levels (the ask suggests 64 × 64, up to 256); varied per frame where the view averages (TSR), fixed where it does not. **How a master tells the two views apart is the executor's call** (the ask's (a), the engine's own per-view data, is preferred to (b), one global value). Whether **Hair** takes the new threshold too is the executor's call; show Hair either way.
  - **Must still hold:** a copy fading in takes `1 − t` of the SAME (per-frame) threshold, so the cross-fade stays complementary with no holes (R-OFL-3); a tie keeps the pixel; every layer of one object keeps or drops the same pixels (no insides); the value contract (`object_fade`, slot 0) unchanged, so the platform only rebuilds its masters; fully there draws exactly as before (re-run the presence-1 baseline, `fade.py --fade 0 --supersample 4`, against `~/.cache/matter-parity/P29_baseline_presence1/captures.json`).
  - **⛔ Before building, say in one sentence what the worst step looks like in the headset, moving** (project memory, the fidelity bar).
  - **Click 3:** at one sample per pixel (the headset's look), the 11-article sheet at 50 % and a slow fade on one article in small steps, and the 25 / 75 cross-fade, beside 29.1's grid; and the per-frame average over enough frames to stand in for TSR (the library's runtime has no temporal AA: the capture turns anti-aliasing off), which should read as an even fade. The Desktop under real TSR is judged in the platform's app.
  - **At its close:** `MasterSet.md` §Object fade (the threshold; its *"averaging turns it see-through"* sentence changes under Q-OFL-2), the `OFL` research doc's library pass and footer, a ledger row, and a runtime `unreal-runtime-v9` offered on the lead's word.
- **At the close:**
  - M15's status: what the platform's next act is (re-run its masters build; write slot 0; swap to `MI_Matter_<Token>_Fading`; precache it);
  - the Glossary's new words (*masked instance*, `object_fade`);
  - the publish offered (RD-P29-5).

*Reconciled click by click:* click 1 needs only 29.1's builder, runtime and rig. Click 2 needs 29.1 plus the look view's two-character cast in 29.2. Every In-now bullet names its step or the close.

## Compact build map

| Seam | Likely files | Note |
|---|---|---|
| the masters | `unreal/MatterRuntime/Scripts/build_masters.py` | `bayer4()` shared. The mask on the solid masters is ignored while opaque. The instances: `unreal.MaterialInstanceConstant` with `base_property_overrides` (blend mode, clip) after the master is saved. Check that the connect call accepts the mask on an opaque master. |
| the runtime | `MatterRuntimeGameMode.{h,cpp}` | `JobFormat` 6. Per mesh, `SetCustomPrimitiveDataFloat(0, f)`; a `LoadMaster`-style cache for the instances. Built through `unreal/build.sh editor` + `masters`; the editor-hosted driver path (`MATTER_UNREAL_EDITOR`) avoids a package for the clicks. |
| the job | `tools/parity/drivers/unreal.py`, `job.py`, `JOB_FORMAT.md` | `fade` per mesh; `FADE_JOB_FORMAT = 6`; a one-sample mode beside `SUPERSAMPLE`. |
| the clicks | `tools/parity/rig.py`, `tools/parity/look.py`, `scene/build_character.py` | `--fade`; `--crossfade`, two casts of one character. |
| the contract | `docs/specs/Ontology/MasterSet.md`, `tools/parity/JOB_FORMAT.md`, `docs/Glossary.md` | the value, the slot, the instances' names, the tests. |

**Test surface (build ceiling):**
- `run_all.py` (no lane should move; the WorkingDrive must be mounted, or `tool_tests` fails on `library/parity`);
- the presence-1 sheet against its baseline (one real-path smoke);
- the two clicks.
- No new gate.

**Cost to announce at execute:** the C++ editor build, capped at 8 jobs (CPU, minutes) and the masters commandlet (CPU, `-nullrhi`). The renders use the GPU. Check `ps -ef | grep "[U]nrealEditor"` first and ask once for the batch if an editor or Studio is up.

## Discovery Log

### Pass 1 — the product docs, the tree, the engine (2026-11-09)

- **Read:**
  - the phase seed; `_Architecture.md` (headings), `Consumers.md` §IMRSV, `MasterSet.md` §Material-settings intent, `CoreMechanisms.md` (whole);
  - `Learnings/Unreal/Unreal.md` (U7, U8, U18 apply; the rest are shading facts this phase does not move);
  - `JOB_FORMAT.md` (§The test set, §Which masters a runtime carries, the look view);
  - `look.py`'s head; `drivers/unreal.py` (`SUPERSAMPLE`, the job formats); `MatterRuntimeGameMode` (`LoadMaster`, the capture's show flags, `JobFormat`);
  - `unreal/build.sh`; the research doc (the source).
- **The platform's side:** its object-fade phase is in discovery (2026-11-09). Its session was told this split by message: the library owns the masters, the instances, the value's spec and its own runtime's swap; the platform owns writing the value, its swap, the precache, the bake and the overlay. Asked whether slot 0 is free (Q-P29-5). It replied that it is, and that the split matches its own record.
- **Grep for this phase's own names** (`object_fade`, Custom Primitive Data, dissolve, *object opacity*) across `tools/`, `unreal/`, `blender/` and `docs/specs/`: nothing built. The only hit is `MasterSet.md`'s 2026-11-09 history line.
- **F-P29-1 — The rig's and the look view's averaging hides a dissolve.** `drivers/unreal.py` renders at `SUPERSAMPLE` 4 (look: 2) and averages each block, and the runtime's capture has `SetAntiAliasing(false)` (*"the driver supersamples instead"*). `bayer4()`'s docstring relies on exactly this to make Hair's coverage soft in the rig. A dissolve rendered that way reads as a smooth fade, the ruled-out look. The clicks render one sample per pixel (§First human test).
- **F-P29-2 — The rig's test set covers seven of the eight masters.** Hair is not among the 11 articles, but the character wears it, so click 2 covers it.
- **F-P29-3 — The runtime loads a master by token, from a fixed path.** A swap to an instance is a second, parallel lookup. It is the reference the platform's own swap can follow.

## Open questions

| # | Question | State |
|---|---|---|
| Q-P29-1 | does a dropped glass pixel still bend the view? | closed by RD-P29-1: the bend is zeroed there always |
| Q-P29-2 | the shadow while fading | closed by RD-P29-4 |
| Q-P29-3 | the cost while fading | closed by RD-P29-6: the platform measures it in the headset |
| Q-P29-4 | publish the runtime? | closed by RD-P29-5: local; offered at the close |
| Q-P29-5 | is slot 0 free on the platform's components? | closed: the platform confirmed it free, 2026-11-09 (RD-P29-3) |
| Q-P29-6 | which copy owns a tie | closed by RD-P29-3: both |

## Execution

| Step | Result | Next |
|---|---|---|
| 29.1 | ✅ **Click 1, the lead (2026-11-09), on `fade_sheet.png`:** *"looks right, every master dissolves — go on to 29.2"*.  Masters, four `MI_Matter_<Token>_Fading`, runtime job format 6, `fade.py`, `MasterSet.md` §Object fade, `JOB_FORMAT.md`. Presence 1 against the pre-change baseline (4×, the rig's sampling): 10 of 11 articles bit for bit in linear float; Marble differs by the same amount between two launches of one build (mean 1.2 levels on the same 39k pixels, no bias): its subsurface pass's launch noise. At 0.5, one sample per pixel: on Grey, ABS, Copper, Oak, Rust, Lace, Neon and Glass_Green every subject pixel is exactly the article or exactly the backdrop, 50/50, and a copy at −0.5 keeps exactly the other half. **Every dropped pixel on all 11 is exactly the backdrop.** Kept pixels differ from fully there on Glass_Clear (7 %), Diamond (15 %) and Marble (42 %, median 2 levels): the glass shows the object's own half-gone parts through its blur or bend, and Marble's scatter has half its neighbours. | click 1, then 29.2 |
| 29.2 | ✅ **Click 2, the lead (2026-11-09), on `crossfade_sheet.png`:** column 4 (A alone at 50 %) *"looks right to me"*; column 3 (25/75) *"There is a ton of dithering on column 3 (lots of squares) could be a render issue... no idea.."*. Measured: the 4 × 4 pattern as built, 25 % light skin on a regular two-pixel grid (at 50/50 a one-pixel checkerboard). Asked to keep the grid and judge the look in the headset, or change to an irregular grain now: *"keep it"*. **The cross-fade's look at 25/75 is judged in the platform's headset sitting (FXAA, motion), not here.**  `look.py --crossfade <skin>`: the character twice in one place (copy B's meshes and slots `__b`), face and three quarters, one sample per pixel; columns A fully there · 50/50 · 25/75 · A alone at 50 %. **First render: copy B never showed**, every pixel was A's skin with no holes. Cause, from the engine source: Unreal 5.8 defaults `r.EarlyZPassOnlyMaterialMasking` to 1, the mask tested only in the depth pre-pass and colour drawn where depth is equal, and two coplanar copies have equal depth everywhere. Fixed in the runtime's `DefaultEngine.ini` (=0) and written into `MasterSet.md` §Object fade as a consumer requirement. After: B's pixels differ from A by a median 88–111 levels, A's kept pixels match A fully there (median 2), backdrop inside the outline 0.01 % (edge pixels), the dark share rises from 50/50 to 25/75. Presence 1 re-checked under the new setting against the pre-change baseline (4×): the same 10 of 11 bit for bit, Lace among them; Marble its launch noise, as before. | the close |
| REOPEN | 2026-11-09, for 29.3 (above): the platform's sitting and the lead found the 4 × 4 grid not good enough; blue-noise grain ruled. The first close's work stands. | 29.3 |
| 29.3 (start) | **The worst step in the headset, moving (said before building):** halfway through a slow fade the object is a fine, even, pixel-sized speckle with no grid; the speckle is fixed to the screen, not the object, so as the head turns the grain holds still while the surface slides under it (a faint screen-door shimmer). One level step flips 1 pixel in 4096, so a slow fade shows no steps. **Executor's calls:** a 64 × 64 blue-noise threshold, 4096 levels, made by the builder (no binary in git); the per-frame shift read from the view's own data (its jitter sequence is longer than 1 only under TAA/TSR — engine `SceneRendering.cpp`, `TemporalAAParams`), so the headset's FXAA view stays fixed (the ask's (a)); **Hair** keeps its own 4 × 4 coverage and takes the shared fade as a second test, so fully there is unchanged and hair drops with the head under it; the TSR stand-in renders N real per-frame frames through the production masters (TSR on in the capture, raw scene colour, averaged). | build |
| 29.3 | ▶ **SCAFFOLD COMPLETE — click 3 owed.** Built at `11c8eec` (what and the numbers: its message). Fully there unchanged (presence 1, 4×: 10 of 11 bit for bit, Marble its launch noise). One sample: no grid (pattern score 88 vs 973), every 0.01 step flips 1 % of the article (the grid: 16 steps of 6.3 %), the cross-fade has no holes and keeps 29.2's split. Under TSR every article fades near its presence with no grid. **Hair:** its own 4 × 4 coverage kept, the fade a second test. **Q-OFL-3:** the solid masters fully there cost nothing new; Masked, Hair and the glass masters, which always test, now fetch one 64 × 64 texel per pixel where the 4 × 4 was arithmetic. **Deviation:** the TSR picture is TSR's own output after 64 frames of a still view, not a mean of raw frames: Unreal turns post-processing, and so every AA method, off for a raw scene-colour capture (`SceneCaptureRendering.cpp`), so a raw capture is never a TSR view — the first try was exactly that and its spread stayed that of a fixed dissolve. Its colour is post-processed (tone curve, vignette), so it compares only with its own fully-there column. **For the platform to watch:** a part-present object's shadow takes the per-frame test too; a cached shadow (virtual shadow maps) may hold one frame's pattern. | click 3 |
| CLOSE (first) | ✅ **DONE 2026-11-09.** M15 → the platform's next acts (incl. `r.EarlyZPassOnlyMaterialMasking=0`); Glossary *`object_fade`*, *Masked instance*; CoreMechanisms row 5; Learnings Unreal U19, U20; runtime published as `unreal-runtime-v8` and pinned (the lead's word, overriding RD-P29-5's local-only default). `run_all.py` at the close, the WorkingDrive mounted: 18 lanes, 18 PASS. No open DEFER. | — |

- **Deviation (29.1):** click 1's sheet is drawn by a new `tools/parity/fade.py`, one launch for all 11 articles, not by `rig.py --fade`: the rig is one article per run and compares tools, and Storm and Blender cannot fade. `look.py` is the precedent for a caller of its own.
- **Deviation (29.1):** the fade is per mesh **per setting** (`settings[].fade`), not a field on `meshes[]`: one launch then draws fully there and part-faded side by side, and the runtime swaps a part to its instance and back as a timeline would.
- **Note:** the WorkingDrive was not mounted this run, so the pictures are under `~/.cache/matter-parity/` (`--out`), not `library/parity/`; mounting it asked for a password on the desk, and was cancelled.

## Status footer

- **Passes:** Pass 1 (2026-11-09). The Brief is complete; the lane is build.
- **Decided:** RD-P29-1 … 6, the agent's calls from Pass 2, unless the lead says otherwise.
- **Open:** none. Slot 0 was confirmed by the platform the same day (Q-P29-5).
- **Reopened 2026-11-09** for 29.3 (first closed the same day).
- **▶ Next:** `/execute P29` — 29.3 only.
