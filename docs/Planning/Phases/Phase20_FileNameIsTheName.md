# Phase20 — The File Name Is the Name

**Status:** ACTIVE — IN EXECUTION (2026-10-16, the lead's *"/execute P20"*). Q-P20-1 and Q-P20-2 were taken at their recommendations on that go-ahead (§Execution ledger). Numbered **Phase20** by the lead's *"/discovery P20 The File Name Is the Name"*, which also opened discovery. Seeded the same day by `/research` on the lead's word: *"Seed a phase for what needs doing here and make it next"* (RD-LBL-8). *(In 2026-10-14 commits, Phase20 means Scale Grids, RD-DS-7; it closed as Phase19.)*
**Lane:** `build` (§Risk lane). **Next:** `/execute` once the lead answers Q-P20-1 and Q-P20-2.
**Measured at:** `b400a16`, on the library machine (no engine at `unreal/build.sh`'s `UE`).

## Outcome

**Wherever a person meets a Matter material or HDRI (the website, Studio, USDLiveView), it is called by its file name's own words, the same in every app. HDRIs are named without *PureSky*, and every scene keeps its sky.**

*(Verbatim from the seed. The last clause depends on Q-P20-2: under its option (a) it narrows to the scenes the platform renames.)*

---

## The Brief

### What is left, in one paragraph

The library stopped publishing a second name on 2026-10-16 (RD-LBL-1, `matterlib-0.2.0-dev.9`). Two library jobs remain, plus work on the platform's side:
- **The switch.** Published HDRI names drop *PureSky*. It is built and off: one line in `library/hdris.yaml`, then a re-serve and a snapshot (RD-LBL-5, RD-LBL-7).
- **The gate gap.** The one command does not run the tools' own tests (F-P20-7).
- **The platform's half.** The website must stop making its own material name (P30), and every repo that names an HDRI takes the new name (P31). That work is the platform's, recorded in the ledger (`LOCAL_DELTAS.md` §Separation), and this phase does not wait on it to close.

### First human test

**Where:** the lead's desktop on the library machine: USDLiveView on the re-served dev install. Clicks 4 and 5 are elsewhere, as marked.
**Prep (the agent, before the switch):** create a new scene through Stage. It names the library's default sky. Save it, then read its sky from the file: it should say `IndustrialSunset02_PureSky_v01.hdr`. **The fixture's state is read from its data, never assumed.**

1. **USDLiveView, the materials list:** `ABS_Glossy_Clean_Base` reads *"ABS Glossy Clean Base"*, with every word in the file's order. It does today (F-P20-4); this click shows that nothing regressed.
2. **Open the scene saved before the switch.** It is lit by its sky, as it was. *(Only under Q-P20-2 (b). Under (a) this click is dropped: that scene opens unlit until its sky is picked again.)*
3. **Create a new scene.** It is lit by the default sky. The agent reads the file: `IndustrialSunset02_v01.hdr`.
4. **Studio, the sky picker** (where the lead runs Studio, expected to be the machine with Unreal; it needs this repo pushed and that machine's dev install re-served): the skies read `IndustrialSunset02` and so on, with no *PureSky*, and the materials read their file names' words. Studio shows the catalog's `display_name`, so no Studio change is needed (F-P20-4).
5. **The website**, after the dev snapshot is published (the lead's word) and the platform's mirror has run: an HDRI page reads `IndustrialSunset02`. A material page reads the file name's words **only once the platform's P30 has landed**, which is the platform's work, judged in its own sitting. This phase's TRY covers the library's half of this click: the published site file carries only the published names.

**Surface check:**
- USDLiveView shows material names and draws the sky, but shows no sky names. So *"named without PureSky"* is judged in Studio (click 4), and the file's sky name is the agent's read (clicks 2 and 3).
- Every click runs on a machine where its tools have run.
- No click needs anything under Not now except click 5's P30 half, which is marked.

### In now

| Item | Step |
|---|---|
| The gate runs the tools' own `test_*.py` (if Q-P20-1 is yes), and `ToolingConventions.md` records the first ruling on tests | 20.1 |
| `published_drop_variant: PureSky` set; the dev install re-served under the published names; the old HDRI thumbnails removed | 20.2 |
| Scenes saved before the switch keep their sky (Q-P20-2 (b)) | 20.2 |
| The specs say what is now in force: [Identity](../../specs/Ontology/Identity.md) §HDRI names (dated) and its "a rename is a new article" Reevaluate line (this is the rename in place it anticipates, RD-LBL-5); the published-name examples in [RuntimeCatalog](../../specs/Contract/RuntimeCatalog.md), [SiteFile](../../specs/Contract/SiteFile.md) and [Manifest](../../specs/Contract/Manifest.md) (F-P20-8) | 20.2 |
| Ledger P31 and M10 updated: the day, and what a late rename now costs | 20.2 |
| A dev snapshot published with the published HDRI names, at the lead's word | 20.3 |
| P30 for Studio and USDLiveView marked as verified conforming in the ledger, while the website's half stays open | *at the close* |

### Not now

- **The platform's work (P30, P31):** the website stops making its own material name, and the platform renames its HDRI references. Theirs, through the ledger. No platform phase holds either yet (F-P20-5).
- **A release that lists HDRIs**, and the manifest check taking published names (F-P20-9): *Release Bundle*. See §Deferred.
- **Blender's asset library:** no change (F-P20-6, decided below).
- **Renaming the HDRI source files:** ruled out (RD-LBL-5).

### Reuse check

*What does the stack already provide, and which contracts are touched?*
- **The switch is built** (`dc9bde6`): `hdris.py` `published()` and `on_disk()`, the stamped served copies, the collision refusal and the published default. It was verified with the setting on in scratch folders (research Pass 5). 20.2 sets the line and re-serves; it writes no new mechanism for the rename.
- **Keeping old scenes lit (Q-P20-2 (b)) uses fields the catalog already has.** An old name becomes an `hdris[]` row with `status: deprecated` and `creator_selectable: false` ([RuntimeCatalog](../../specs/Contract/RuntimeCatalog.md) §HDRIs; both fields exist). This is [Identity](../../specs/Ontology/Identity.md)'s own lifecycle for a renamed entry: *"the old one is marked `deprecated` ('kept for old scenes; prefer a newer material'), so scenes naming it still resolve."* The platform's lookup already honours it (F-P20-3). There is no schema bump and no platform change. **The gap that justifies it:** without it, any scene saved outside the platform's repos loses its sky (F-P20-2).
- **The gate lane (Q-P20-1)** runs scripts that already exist and already report exit 0 for a pass. It needs no test framework: the project has no `pytest`, and every script is a standalone `uv run` (F-P20-7).
- **Contracts touched:** Identity §HDRI names and the runtime catalog's `hdris[]`, both additive under (b); the site file's HDRI ids (the ruled rename); the gate's lane set (`ToolingConventions.md` §Gates and CI).

### Decisions that bind

*One authoritative copy. The research rows are quoted where they are the authority.*
- **RD-LBL-1:** the file name is the name. A consumer shows `display_name`, with its underscores as spaces or as breaks between sections, and never drops or reorders a token.
- **RD-LBL-2 and RD-LBL-5:** HDRIs follow that rule. Every published name drops *PureSky*; the source files, their records and `library/hdris.yaml`'s `default` keep theirs.
- **RD-LBL-7:** the library's half is built now and the switch is the lead's day. Under Q-P20-2 (b) the day no longer has to wait for the platform's rename. The lead still names it.
- **RD-LBL-3:** summaries and search words stay.
- **RD-P20-1 — Blender's asset library needs no change** *(the agent's decision, closing the seed's question, unless the lead says otherwise)*. Each asset is named by its article identity, the file stem verbatim, and nothing is derived (F-P20-6).
- **RD-P20-2 — The phase closes on the library's half** *(answered by `LOCAL_DELTAS.md` §Separation: "Work this repo needs a consumer to do goes in `docs/Planning/PlatformDependencies.md`")*. P30's website half and P31 stay ledger rows. The close says which clicks of the Outcome they still owe.
- **Pre-release, no release ceremony** (`AI_WorkingAgreement.md` §Settled practices). The snapshot in 20.3 is a dev pre-release, published at the lead's word as dev.1 to dev.9 were.

### Risk lane — `build`

The controls this phase touches, each one read:
- **The gate (`run_all.py`):** no lane reads HDRIs. Its manifest lane checks the newest lockfile, which lists none, and the freeze refuses a lockfile that does. So setting the switch moves no gate result. The baseline is **17 lanes: 15 PASS, 2 SKIP (compression, staging), 0 FAIL** (2026-10-16). Adding a lane (20.1) is a lead ruling (Q-P20-1), not a lane escalation.
- **The dev install (`serve_to_stage.py`):** local, git-ignored, rebuilt on every run. The prune step removes served copies that are no longer listed. Under (b) it must keep the old-name links, which is the main build seam.
- **Publication:** a dev snapshot on GitHub, already practised nine times and gated on the lead's word. No new URL or edge is involved.
- **Data:** nothing is deleted. The source HDRIs stay, and the old thumbnails are derived files in the dev install.
- **Not touched:** `unreal/` (no runtime owed: no master's defaults change), `blender/addons/` and `tools/conformance/`. The 20.1 lane *reads* tests there and edits nothing, so no `check_exporter.sh` baseline is owed.

### Step list

- **20.1 — The one command runs the tools' own tests** *(only if Q-P20-1 is yes)*. First result: `run_all.py`'s summary carries the new lane. The six scripts that run under the project's Python pass. The four that need `pxr` or `bpy` run under the USD-tools Python when it is present, and SKIP with the reason when it is not. `test_export_selection.py` stays in `check_exporter.sh`, which runs it inside Blender. Independent of the switch, so it can land first.
- **20.2 — HDRIs are published without *PureSky*, and old scenes keep their sky.** Set the line, re-serve, remove the old thumbnails, add the deprecated old-name rows and links under (b), update the specs and the ledger. **First human test, clicks 1–4.** Under (a), 20.2 waits for the platform to say its rename is ready (P31).
- **20.3 — The website can show it:** the dev snapshot is published with the published names, at the lead's word, and its site file is fetched back. **Click 5, the library's half.**

**Reconciled click by click:**
- Click 1 needs nothing new.
- Clicks 2 and 3 need 20.2's re-serve.
- Click 4 needs 20.2 plus the push and the re-serve on the machine where Studio runs. That needs the push asked for once, at the hand-off (`LOCAL_DELTAS.md`).
- Click 5 needs 20.3, plus the platform's mirror run and P30.
- **The doer of the prep** is the agent, through Stage's scene creation on the library machine. Stage runs there: its runtime is the dev install's root, `IMRSV_STAGE_RUNTIME`.

### Compact build map

- **20.1:**
  - `tools/validators/run_all.py`: a lane over `tools/**/test_*.py` and `blender/**/test_*.py`, found by glob, so a new test joins by itself.
  - The interpreter rule: the project's Python, or the USD-tools env (`USD_TOOLS_ENV`, as `check_exporter.sh` finds it) for a script that imports `pxr` or `bpy`. A missing interpreter is a SKIP with the reason, never a PASS.
  - `docs/ToolingConventions.md`: §Gates and CI (the lane, and the new count), and its §Tests line, *"not yet a ruling: the first phase that ships a real test suite decides it here"*, which this ruling decides.
- **20.2:**
  - `library/hdris.yaml`: uncomment `published_drop_variant: PureSky`.
  - `tools/releases/hdris.py` (`on_disk()` carries each HDRI's former published name).
  - `tools/releases/serve_to_stage.py`: under (b), the deprecated hidden rows in the dev catalog, an old-name link in `hdris/` to the new stamped copy, and a prune step that keeps them. Under either option, the old `thumbnails/hdris/` files are removed.
  - Tests: units in `tools/validators/test_hdri.py` and `tools/releases/test_build_snapshot.py`.
  - Specs: per §In now.
  - `docs/Planning/PlatformDependencies.md`: P31 and M10.
  - Under (b), the site file carries no hidden rows: the website shows skies to choose, not scenes.
- **20.3:** `uv run tools/releases/build_snapshot.py --publish` (`docs/Learnings/GitHub/` G1: it resumes an interrupted draft).
- **The one real-path smoke:** clicks 2 and 3, on the real dev install. **Test ceiling:** existing tests, the new units and that smoke. No RED demo.

### Open for the lead

- **Q-P20-1 — Should the one command run the tools' own tests?** *(A new lane is a lead ruling.)*
  - **Recommendation: yes,** as in 20.1. Today nothing runs 8 of the 11 test scripts. A broken `test_hdri.py` stayed green on 2026-10-16, and the switch this phase throws is guarded only by two of those unrun scripts (F-P20-7). The cost is a few seconds per run.
  - **Or no:** whoever edits a tool runs its test, as today.
- **Q-P20-2 — A scene saved before the switch names `…_PureSky_v01.hdr`. What happens to it?** P31 renames the scenes in the platform's repos; a scene saved anywhere else is not covered (F-P20-2).
  - **(a) Accept it.** Such a scene opens unlit until its sky is picked again. Nothing is built. The switch still waits for the platform's rename day (RD-LBL-7), and the Outcome's *"every scene keeps its sky"* narrows to the scenes the platform renames.
  - **(b) Keep the old names resolving, hidden.** *(Recommended.)* The dev catalog keeps each old name as a `deprecated` row that no picker shows, and serves it as a link to the new file. The platform's lookup already draws a hidden row's sky without any change on its side (F-P20-3). This is Identity's own lifecycle for a renamed entry. **It also frees the switch from the platform's day:** a late rename on their side no longer loses a sky, though they still rename (P31). Cost: 59 hidden rows in the dev install, dropped when the first release ships, since a release carries only the published names. It **refines RD-LBL-5** (*"rename the others that are published"*) for the dev install only: the old names stay there, hidden, and appear nowhere a person reads a name.
  - **(c) The platform maps an old name to the new one** when it opens a scene. That is the platform's work, added to P31, and a lasting shim on their side.

---

## Discovery findings

- **F-P20-1 — The switch is off on disk** (measured 2026-10-16). The dev catalog lists 59 HDRIs, all selectable, every id `…_PureSky`, with the default `IndustrialSunset02_PureSky`. There are 59 thumbnails.
- **F-P20-2 — A saved scene stores its sky as a bare file name** (`IndustrialSunset02_PureSky_v01.hdr`, the platform's scene schema), so the switch changes what a scene must name. P31 covers the platform's repos. A scene saved anywhere else names a file the re-served dev install no longer lists → Q-P20-2.
- **F-P20-3 — The platform's sky lookup** (read at its origin, 2026-10-16, contract level):
  - drawing a scene's sky searches **every** HDRI in the catalog, selectable or not;
  - choosing a sky accepts only a `creator_selectable` one;
  - so a hidden `deprecated` row keeps an old scene lit, and no one can pick it anew;
  - **to confirm on the real scene at execute** (click 2).
- **F-P20-4 — The consumers today** (read at origin, 2026-10-16):
  - **USDLiveView** shows a material's `display_name` with underscores as spaces, so it conforms to RD-LBL-1. It shows no sky names.
  - **Studio** shows the catalog's `display_name` for materials and skies, so the switch reaches it with no Studio change.
  - **The website** makes its own material name when the site file carries no `label`, which is every material since dev.9. That is what P30 asks it to stop.
  - **The website also builds an HDRI page's address from its id,** so the switch changes those addresses. P31 lists the website.
- **F-P20-5 — No platform phase holds P30 or P31 yet.** The platform's active materials phase reads this ledger up to P29, and P30 and P31 came later the same day. Routing them is the platform's business; the lead may want them pulled in.
- **F-P20-6 — Blender's asset library** names each asset by its article identity, the file stem verbatim (`ABS_Glossy_Clean_Base_s01_v01`, `tools/generators/gen_asset_library.py`), and derives nothing. It holds no HDRIs. → RD-P20-1.
- **F-P20-7 — The gate gap, measured.** There are 11 `test_*.py` scripts:
  - **`run_all.py` runs none of them.** `check_exporter.sh` runs three: `test_lcd_portable`, `test_check_lcd_carrier` and `test_export_selection`.
  - **Run once each under the project's Python (2026-10-16):**
    - six exit 0: `test_lcd_portable`, `test_scale_view_rules`, `test_wishlist`, `test_build_snapshot`, `test_thumbnails`, `test_hdri`;
    - four exit 1 only for want of `pxr` or `bpy`: `test_lcd_sparse` and `test_lcd_transform` (every pure check passes) and `test_check_facing` and `test_check_lcd_carrier` (import errors);
    - `test_export_selection` runs only inside Blender.
  - **No lane reads HDRIs at all.** Their only checks are `test_hdri.py` and `test_build_snapshot.py`, both unrun.
- **F-P20-8 — This repo's *PureSky* references, sorted:**
  - **Published names that change on the day:** the examples in RuntimeCatalog, SiteFile and Manifest.
  - **Source names that stay:** `library/hdris.yaml` `default`, `CREDITS.md`, the provenance records, `import_polyhaven_hdri.py`, `tools/thumbnails/showcase.py` (it reads a source file) and the tests' source fixtures.
  - **Research and closed-phase docs are history** and are not edited.
- **F-P20-9 — A release that lists HDRIs would take the published name** (Identity §HDRI names). `validate_manifest.py`'s HDRI grammar is `<Name>_<Variant>_vNN`, resolved to the source path, so it would refuse `IndustrialSunset02_v01`. That is moot until a release holds an HDRI. → §Deferred.
- **F-P20-10 — The gate baseline on the library machine:** 17 lanes, 15 PASS, 2 SKIP, 0 FAIL (2026-10-16).

## Deferred

| What | To | What it consumes from this phase |
|---|---|---|
| A release lockfile listing HDRIs, and `validate_manifest.py` taking the published name (mapped back to the source file) | *Release Bundle* (`Phases/Future/PhaseTBD_ReleaseBundleConsumerContract.md`) | `hdris.py`'s published id beside its `source_id`; `published_drop_variant`; under Q-P20-2 (b), the rule that a release carries no deprecated old-name rows |
| The website showing the file name's words, and its HDRI addresses | the platform, ledger P30 and P31 | the site file's `display_name` and published HDRI ids from 20.3's snapshot |

## Depends on

- **Nothing, for 20.1.**
- **For 20.2:** under Q-P20-2 (a), the platform's word that its rename is ready (P31). Under (b), only the lead naming the day.
- **For click 5's material half:** the platform's P30.

## Execution ledger

- **The two questions** (the lead's go-ahead, *"/execute P20"*, passed over both; both are reversible, so the agent took its recommendations and said so; **not rulings the lead spoke**):
  - **Q-P20-1 → RD-P20-3 (taken):** the one command runs the tools' own test scripts (20.1).
  - **Q-P20-2 → RD-P20-4 (taken): (b).** The old names stay resolvable, hidden and `deprecated`. This refines RD-LBL-5 for the dev install only. **Consequences stated to the lead:**
    - old scenes keep their sky;
    - the switch no longer waits for the platform's day, though the platform still renames (P31);
    - 59 hidden rows stay in the dev install until the first release.
- **Deviation, a Brief fact that was false:** the Stage on the library machine is a 2026-09-27 build. It cannot seed a scene with the library's default sky, which the platform added on 2026-10-14/15. So the prep is not *"create a scene through Stage"*. **The fixture is the platform's own Studio-saved composition** naming the default sky (`CubeAndCone_04/Composition_09`, at the platform's origin), in scratch copies outside that repo:
  - **A** is as saved (`…_PureSky_v01.hdr`);
  - **B** is renamed as the platform's P31 will write it (`IndustrialSunset02_v01.hdr`);
  - **C** is a control naming a sky that does not exist.
- **Deviation, found building:** `serve_to_stage.py --view` pointed USDLiveView at the checkout, which holds only the source names, so a scene naming a published sky would not resolve there. It now points at the dev install.
- **Surface check:** USDLiveView draws the sky as the backdrop. Measured on the scratch copies: A shows the sunset; C shows a flat grey backdrop. A headless `usdrecord` render cannot show it (no image lighting, no backdrop) and was dropped as the instrument.
- **20.2 · `676a2d8` · clicks 2 and 3, the lead in USDLiveView (2026-10-16, library machine):**
  - **The lead, verbatim:** *"Ok... they look the same to me... is that what you want me to see?"*
  - **The agent's reading:** a pass. The scene saved with the old sky name (`SavedBefore_OldSkyName`) and the same scene with the published name (`Renamed_NewSkyName`) show the same sunset sky; the agent's screenshots of both show it behind the objects, where the C control shows flat grey.
  - **Click 1 is agent-checked, not the lead's.** The materials list needs Stage editing that scene, and Stage had another session's scene open ("editing off"). What it shows is unchanged by this phase: the served catalog's `display_name`, which USDLiveView shows with underscores as spaces (F-P20-4).
  - **Owed:** click 4 (Studio, on the machine with Unreal; needs a push) and click 5 (the website; needs 20.3).
- **20.1 · `89ba1a6` · done** (no click: the gate's own output).
- **Gate, 20.1 and 20.2 in the tree:** 18 lanes: 16 PASS, 2 SKIP (compression, staging), 0 FAIL. That is the baseline set plus `tool_tests` (11 of 11 scripts PASS on the library machine).

## Discovery Log

- **2026-10-16 — Pass 1 and the Brief.**
  - Numbered by the lead (`b400a16`).
  - Read: the specs, top down to Identity §HDRI names and the runtime catalog's `hdris[]`; the labels research (RD-LBL-1 to RD-LBL-8); the ledger (P30, P31, M9, M10); the consumers at their origin, read-only, for what concerns the library; the Blender generator; the gate and the 11 test scripts; the GitHub learnings, which bear on 20.3. No other learnings domain is touched.
  - Found F-P20-1 to F-P20-10. Closed the seed's Blender question (RD-P20-1).
  - **The seed's draft test assumed a saved scene keeps its sky. Nothing on the library's side made that true.** That gap became Q-P20-2.
