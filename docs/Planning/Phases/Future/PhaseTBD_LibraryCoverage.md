# PhaseTBD — Library Coverage

**Status:** SEEDED, discovery paused after Pass 1 (2026-10-01). **Un-numbered again the same day it was numbered Phase10**: its Pass 1 proposed colour on wear layers as a phase of its own (F-LC-7), and the lead ruled, verbatim: *"If 2 then we need to do that phase now instead."* **Coloured Wear Layers took Phase10** (`Phase10_ColouredWearLayers.md`) and runs first. Discovery resumes here at Pass 2 after it closes. **Id scope: `LC`** (`NamingConventions.md` §Planning ids); the ids were minted as `F-P10-n` and renamed `F-LC-n` on 2026-10-01.
- **Its numbers, oldest first** (anything older that names one of them about this work means this phase): seeded as **Phase05** on 2026-09-25 (*"i and then seed phase 5 and that will be building materials"*); **Phase07** from 2026-09-26 (the test rig and the Unreal runtime first, so every material is checked in all three tools); **Phase08** from 2026-09-27 (research `260927_R_CharacterMaterials_MPFB2.md` CM4: Character Materials first); **un-numbered** on 2026-09-28 (*"make this Phase 8, mark the current Phase8 as TBD - we have many other little things to get in here befoer we build out the full library."*); **Phase10** for part of 2026-10-01 (*"/discovery … as Phase10"*), then **un-numbered** again the same day.
- **Why it exists:** *"we have 200 materials to build and test before we have our first versionable library"* (lead, 2026-09-25, `260925_R_DraftsInUSDLiveView.md` Pass 5).
- **Re-cut at Pass 1 (2026-10-01)** from "build ~162 articles" to "build the loop that builds them, and prove it", as the seed's own `Reevaluate (2026-09-26)` anticipated (F-LC-1). This doc was rewritten rather than patched; the seed's scope is kept below, marked with where it now lives.

## Outcome

**The Roadmap's, kept until the lead restates it:** *Creators find materials for every class of matter in the taxonomy, including the classes IMRSV's character work needs (skin, cloth, hair).*
- **Reevaluate (2026-09-27):** skin, hair and the character side of cloth went to Phase07 Character Materials (CM4) and Phase08.

**Under test (Pass 1, F-LC-1), proposed for the Roadmap:** **the maintainer runs a batch and gets new materials, each already built and checked side by side in USDLiveView's renderer, Blender and Unreal, and keeps or sends back each one from its picture sheet. The library fills toward its full list this way, without a phase per batch.** Restating it is the lead's call. **Asked at the Pass 1 handback (2026-10-01) and not answered** (the reply re-sequenced the phase instead); re-raise when discovery resumes here.

## Why this is a phase

Filling a library is a loop, not a sequence of phases: build, check in every tool, fix, keep (`260926_R_BigPicture_NimbleSetup.md` Pass 2, accepted as the working plan by the lead in BP5). **This phase builds that loop once and proves it on about 30 materials** (that research's Pass 12). After the close the loop keeps running, and the rest of the list fills without a phase per batch.

## What it consumes (measured 2026-10-01)

- **The library:** 58 articles. 30 are `biological` (Phase07–09); 28 are the rest, the system article included, across 12 classes. **45 recipes carry `status: candidate`**; the 13 recipes from before Phase07 carry no status.
- **Wear layers:** 9 shared layers. Overlays: `Dust01`, `EdgeWear01`, `Fingerprints01`, `Scratches01`, `Scuffs01`. Masks: `Crevice01`, `Grime01`, `RustBloom01`, `Verdigris01`. The list wants 22.
- **The building half:** `/matter-generate` (Phase03), one article per brief: plan → Physically Based values → recipe → assemble → gate → a Storm preview → a written critique. It can make a missing wear layer (§3a). It never commits.
- **The checking half:** `tools/parity/rig.py <article> --sweep`, with **all three columns on this machine**: Storm, Blender (`~/.local/bin/blender`) and the Unreal runtime `unreal-runtime-v2`, pinned and downloaded under `unreal/package/`. **Its verdict is the "Moved" agreement** (each slider moves every tool alike), with ΔE as a diagnostic (Phase06 D9, shipped).
- **The list:** 173 rows in `260925_R_LibraryCoverage_FirstRelease.md` Pass 2, each with a name, folder, master, way of making it (L1 values only · L2 generated textures · L3 an ambientCG scan), scale and wear layers. Its status column is dated 2026-09-25 (see §Seed questions, 3).

## Scope

**In — the re-cut (Pass 1 hypothesis; the Brief fixes it):**
- **The wish list**, one plain file in the repo (BigPicture Q-D, recommended *"decided at Phase07"*, so here), seeded from the 173-row list. Each row carries its state: queued · built · ready for review · stuck (with why) · kept · redo (with the note).
- **One batch command** that takes the next few rows and, for each, builds it the `/matter-generate` way, runs the rig, reads its own sheet, fixes and re-runs up to a set number of tries, and marks the row.
- **A short summary per batch** (what was built, each sheet, what got stuck), and the lead's **keep / redo**.
- **Proving it on about 30 rows** (BigPicture Pass 12), chosen to cover every master, every way of making a material, and rows that need a new wear layer.
- **The new wear layers those rows need**, made by the skill's §3a path.
- **No schedule.** A batch runs in a session; nothing runs at fixed times (the lead, 2026-10-01, F-LC-8).

**Kept from the seed; after the proof it is the loop's work, not a step of this phase:**
- The rest of the list (about 130 rows) and the rest of the 22 wear layers.
- Articles on disk updated to carry their relevant layers (ruling C1); they keep their `v01` in place (the lead's "no versioning" ruling, 2026-09-25).
- `Scuffs01` regenerated with real coverage (seed question 10; measured nearly empty, 2026-09-27).

**Not now:**
- **The F82 (`specular_color`) and thin-film inputs** (seed question 3). The loop builds a row that wants one as an approximation and says so in its critique (F-LC-6).
- **Colour on wear layers** (dust and grime that show their colour; makeup). Routed here by Phase07's L3; **now Phase10 Coloured Wear Layers, which runs first** (F-LC-7).
- Localised colour or gloss through a mask (L7).
- Cutting, versioning or publishing a release: *Release Bundle and Consumer Contract* and *Version Management*.
- The catalog listing each article's layers and master (L9), which belongs to the release bundle's catalog.

## Seed questions — where each stands (Pass 1)

| # | The seed's question | Where it stands |
|---|---|---|
| 1 | Skin, cloth and hair in the Outcome | **Answered.** CM4 moved the character classes to Phase07; nothing character-specific remains here. |
| 2 | The whole ~173, or a first tranche? | **Answered by precedent:** prove on about 30 first (BigPicture Pass 12). The proving batch measures review time (L5's 5–10 minutes per article is unmeasured). |
| 3 | Carriers C1–C3 in or out? | **C2 and C3 are built** (Phase07: coat, fuzz, anisotropy; F-P08-6). **F82 and thin film are not** (no trace in `LCDSchema.md`, `MasterSet.md`, the assembler or the recipe schema, 2026-10-01). Out (F-LC-6). |
| 4 | The naming and structure gut-check (N1–N8, S1–S6) | **Answered by precedent:** resolved on contact, when the loop reaches a row it affects (BigPicture Pass 3, item 5, under BP5). N1, N2, N4, N5 and N8 were superseded by C5. **N3 (British spelling) is still unwritten** in `NamingConventions.md`. |
| 5 | The layer library: generated or converted from ambientCG? | **No policy needed:** the skill decides per layer (§3a), and the rig judges the result. |
| 6 | The risk lane | **`build`** (hypothesis, F-LC-12); confirmed at the Brief. |
| 7 | A seam-check lane over the shared layers? | **Reuse, not a new gate:** the rig's `compare.py` already runs the seam check on every article it renders (Phase04's measure). A new `run_all.py` lane stays a lead ruling, and nothing asks for one. |
| 8 | Do the pre-Phase03 base textures tile? | **Measured by the loop:** the rig's seam check runs on each article it re-judges. |
| 9 | Layers at their own size | **Built in** (Phase04): the skill's §6 critique checks it. |
| 10 | Wear layers too faint; dust can't show colour | **Split:** regenerating `Scuffs01` is the loop's work (§Scope). **The colour half came back here** from Phase07 (L3's default, its close) and is now **Phase10 Coloured Wear Layers**, which runs first (F-LC-7). Whether `Scuffs01` goes with it is that phase's question. |
| 11 | The LCD ruling, at volume | **The rig's bar is done** (Phase06 shipped the Moved verdict). Still binding on the loop: each article states the real substance, and masked articles take soft coverage (`Lace_Floral`'s hard cut-out first). |

## Discovery Log

### Pass 1 — 2026-10-01 — the product docs read against the Outcome; the re-cut

**Examined:**
- **Specs, top-down:** `_Architecture.md` · `Taxonomy.md` · `Experience_MatterLibrary.md` · `MasterSet.md` (the overlay rule, the Hair note) · `LCDSchema.md` and `MasterSet.md` searched for F82 and thin film · `NamingConventions.md` · `ToolingConventions.md`.
- **Research:** `260925_R_LibraryCoverage_FirstRelease.md` (whole) · `260926_R_BigPicture_NimbleSetup.md` (whole) · `260928_R_HairAndNailRendering.md` (to rule out an overlap with *Hair That Reads as Hair*).
- **Closed phases, for what they routed here:** Phase05 (5.2, F11) · Phase06 (§Not now) · Phase07 (L3, the close) · Phase08 (F-P08-6, 8.4) · Phase09 (the close).
- **Tree:** the articles and recipes (counts and status), the shared layers, `.claude/skills/matter-generate/SKILL.md`, `tools/parity/rig.py` (the sweep, the verdict), `drivers/unreal.py` (where the runtime comes from), `unreal/RUNTIME.json` and `unreal/package/`, `run_all.py` (what it globs), the Unreal masters' scatter floor. **Grep for the phase's own names** (wish list, build loop, nightly) outside research and closed phases: **nothing built.**
- **Learnings, all five domains:** Storm (S3: render twice and accept on agreement; S5) · Blender (B1–B9: built into the masters) · Unreal (U7: the warm-up render; U11: a scatter colour of 0 hung the GPU, and the masters' `SUBSURFACE_FLOOR = 1e-4` guards it) · MaterialX (M4) · Claude Code (CC1: no bearing).
- **Sequencing:** no ruling newer than the Roadmap undercuts this phase. The 2026-09-28 *"many other little things"* were Phase08 and Phase09, both closed. `git log` since 2026-09-28 holds no other sequencing ruling.

**Findings:**
- **F-LC-1 — This phase builds the loop, not 162 articles by hand.** BigPicture Pass 2: *"Filling a library is a loop: generate, test, fix, keep. The loop should run without opening a phase per batch."* Its Pass 5 table re-cuts this entry as *"The generation loop: the library fills itself in scheduled batches; the lead reviews sheets, not scenes"* (the "scheduled" is struck: F-LC-8), and the lead accepted that sequence as the working plan (BP5, 2026-09-26). Pass 12: *"prove the build loop on about 30 materials before the full list."* **Precedent answers it, so it is taken and recorded here, not asked.** The Outcome's wording is the lead's to restate (the Roadmap rule); asked 2026-10-01, unanswered (§Outcome).
- **F-LC-2 — All three tools are on this machine,** so the momentum rule "two tools = candidate, three = approved" (BigPicture Q-H) is moot. The loop requires all three from the start, as that research's own Pass 11 said it would once the runtime existed.
- **F-LC-3 — The judge is the rig, not the skill's preview.** The skill renders a Storm preview and hands off to USDLiveView by hand (§6–6a). The loop judges on the rig's three-tool sheet and its Moved verdict, which is BigPicture Pass 9's design: *"runs it through the rig, reads its own contact sheet, fixes what's off, and runs it again"*.
- **F-LC-4 — Where the loop's drafts are kept is open.** The skill leaves an uncommitted draft and never commits. At volume, in a tree that other sessions share by design (`.claude/CLAUDE.md` §Git), a batch's uncommitted files show up in every other session's `git status` until the lead reviews them. **For the Brief:** commit each built row as `status: draft` (a local commit; the push stays the lead's), or keep the drafts uncommitted until the lead keeps them. Recommendation: commit as `draft`. Keep sets `candidate`, and redo marks the row with the lead's note.
- **F-LC-5 — Only 9 of the 22 wear layers exist,** and `Scuffs01` is nearly empty (seed question 10). The proving rows should include ones that need a new layer, so the layer path is proven too.
- **F-LC-6 — F82 and thin film are not built.** 8 metals want F82 to be accurate (status `Now·C1`), car paint wants it with coat, and nacre wants thin film. **The precedent for building them anyway:** the lead's ruling for Phase07 (CM4, 2026-09-27) that materials ship as uncalibrated candidates rather than not at all (*"I would rather have everything in and 'uncalibrated' yet then a bunch of magenta"*). The loop builds them as approximations, and each critique names what is missing (the skill's §6 already requires that). This answers the coverage research's L4 for the build. Whether F82 ever becomes an input is a later phase.
- **F-LC-7 — Colour on wear layers is a phase of its own, and it runs first.** Phase07 left it here (L3: build it only if skin needed it; it did not). It is a contract change, not material work: `MasterSet.md` says *"an overlay never tints"*, and lifting that touches `LCDSchema.md`, the Blender and Unreal masters, and Studio. **Ruled (lead, 2026-10-01), verbatim:** *"If 2 then we need to do that phase now instead."* It is **Phase10 Coloured Wear Layers**; this phase waits for it, unnumbered.
- **F-LC-8 — No schedule. Struck by the lead, 2026-10-01**, verbatim: *"The fixed times was ONE session... remove taht thought."* "At fixed times" came from one research session (BigPicture, the lead's sequence item 2); it is not a standing want. Recorded upstream as BigPicture BP10.
- **F-LC-9 — The Phase06 re-judging is unclaimed.** Phase06's §Not now: *"Re-judging the character articles that Phase07 and Phase08 left as candidates. The column makes that possible; it is the next unit."* No later phase took it. **The loop's list can carry the 45 existing candidates as rig-only rows** (no build, just the three-tool sheet and a keep/redo), which also re-measures the pre-Phase03 base textures' seams (seed question 8). Proposed for the Brief.
- **F-LC-10 — Nothing in the tree overlaps *Hair That Reads as Hair*.** Its remaining parts are strands and card maps (`260928_R_HairAndNailRendering.md` H4, H5), which are not on this list.
- **F-LC-11 — Status words: two things share "approved".** The article's lifecycle field (`draft → candidate → approved`, `_Architecture.md` §Versioning) is not the release approval (`promote_release.py`, the maintainer's act, which the pre-release ruling keeps out of content work). The loop sets the lifecycle field only. **The lead's keep sets `candidate`**, as every Phase07–09 article is; `approved` waits for the first release. *(Carried to the Brief: the wording on the list must not say "approved".)*
- **F-LC-12 — Risk lane: `build` (hypothesis, controls read).**
  - **Adding articles:** `run_all.py` globs the articles and recipes (`rglob("*.mtlx")`, `recipes/*.json`), so each article adds its own checks. The release lanes glob only `library/releases/` records. Phase07–09 added 41 articles, and Phase08 and Phase09 each closed with the gate at 14 PASS / 2 SKIP / 1 FAIL (the inherited `approval_binds_freeze`).
  - **A batch** touches no sign-in, secret or public edge. It writes only to this machine's tree, and the push stays the lead's.

**Hypothesis for Pass 2 (the Brief):**
- **Steps:** (1) the list file, and one row built and judged end to end by the batch command; (2) a batch of about 5, with the summary, and the lead's keep/redo; (3) the proving 30.
- **First human test:** the lead opens one batch's summary, looks at each row's three-tool sheet, and keeps or redoes it with a note.
- **Still to settle at Pass 2:** the list's file format and home, the proving 30, the try limit, how the summary reaches the lead (a tracked file, per `.claude/CLAUDE.md` §The deliverable surface), and the seconds-per-article of a three-tool `--sweep` (unmeasured; it sizes a batch).

## Discovery Status

- **Passes captured:** 1 (2026-10-01).
- **Current working direction:** the build loop, proven on about 30 rows; the rest of the list fills after the close (F-LC-1).
- **Paused (2026-10-01)** for Phase10 Coloured Wear Layers (F-LC-7). Resume at Pass 2 after Phase10 closes, and re-read what Phase10 changed in the overlay contract first: every article this loop builds carries those layers.
- **Open decisions:** the Outcome, restated (asked 2026-10-01, unanswered; re-raise on resuming).
- **Measured after Phase10's close (2026-10-01, the library machine, Unreal from the downloaded `unreal-runtime-v3`):** a three-tool `--sweep` took **Oak 6.4 min** (Storm 201 s · Blender 81 s · Unreal 100 s) and **Glass_Clear 7.2 min** (204 · 84 · 147 s), so a batch of 5 is about half an hour. Two articles, both on the test scene: a hypothesis for sizing a batch, not a constant.
- **Suggested at Phase10's close (agent, not ruled):** hold F82 / thin film (F-LC-6) until the proving batch's sheets show metals reading wrong; if they do, that is a contract phase in Phase10's shape. More deposits (dirt, soot, pollen) take Phase10's `overlayN_color` shape and need no new LCD input.
- **Checks to carry forward:** the three-tool `--sweep` time per article (first measured above) · **a doc correction for this phase's close:** `_Architecture.md` §Governance says the parity render *"Running it automatically (nightly or per PR) is still (planned), owned by Library Coverage"*. The nightly half is struck (F-LC-8, BP10); the per-PR half belongs to Contribution Path. Annotate with a date; do not delete.

## Execution Log

_(populated during execution)_
