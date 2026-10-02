# Phase11 — Library Coverage

**Status:** IN EXECUTION (2026-10-02; lane `build`). Brief written at Pass 2; Q-P11-1 and Q-P11-2 ruled at the hand-off (RD-P11-1, RD-P11-2), and the per-row review moved to one review at the end (RD-P11-3). **Numbered Phase11 by the lead, 2026-10-02** (`/discovery P11`, the head of the Roadmap's `## Future` once Phase10 closed). Discovery was paused after Pass 1 (2026-10-01): **un-numbered again the same day it was numbered Phase10**, because its Pass 1 proposed colour on wear layers as a phase of its own (F-LC-7), and the lead ruled, verbatim: *"If 2 then we need to do that phase now instead."* **Coloured Wear Layers took Phase10** (`../Complete/Phase10_ColouredWearLayers.md`, closed 2026-10-01). **Id scope:** the ids minted while unnumbered keep `LC` (`F-LC-n`; minted as `F-P10-n` and renamed 2026-10-01); **new ids take `P11`** (`NamingConventions.md` §Planning ids).
- **Its numbers, oldest first** (anything older that names one of them about this work means this phase): seeded as **Phase05** on 2026-09-25 (*"i and then seed phase 5 and that will be building materials"*); **Phase07** from 2026-09-26 (the test rig and the Unreal runtime first, so every material is checked in all three tools); **Phase08** from 2026-09-27 (research `260927_R_CharacterMaterials_MPFB2.md` CM4: Character Materials first); **un-numbered** on 2026-09-28 (*"make this Phase 8, mark the current Phase8 as TBD - we have many other little things to get in here befoer we build out the full library."*); **Phase10** for part of 2026-10-01 (*"/discovery … as Phase10"*), then **un-numbered** again the same day; **Phase11** from 2026-10-02.
- **Why it exists:** *"we have 200 materials to build and test before we have our first versionable library"* (lead, 2026-09-25, `260925_R_DraftsInUSDLiveView.md` Pass 5).
- **Re-cut at Pass 1 (2026-10-01)** from "build ~162 articles" to "build the loop that builds them, and prove it", as the seed's own `Reevaluate (2026-09-26)` anticipated (F-LC-1). The seed's scope is kept below, marked with where it now lives.

## Outcome

**The maintainer runs a batch and gets new materials, each already built and checked side by side in USDLiveView's renderer, Blender and Unreal, and keeps or sends back each one from its picture sheet. The library fills toward its full list this way, without a phase per batch.** *(RD-P11-1, 2026-10-02.)*

**The loop's long-run aim (the Roadmap's Outcome until 2026-10-02):** *Creators find materials for every class of matter in the taxonomy, including the classes IMRSV's character work needs (skin, cloth, hair).*
- **Reevaluate (2026-09-27):** skin, hair and the character side of cloth went to Phase07 Character Materials (CM4) and Phase08.

---

## The Brief

### What this phase delivers, in one paragraph

A **wish list** in the repo (every material the library wants, each with its state) and a **batch command** the maintainer runs in a session. For each of the next few rows the batch builds the material the `/matter-generate` way, puts it through the rig in all three tools, reads its own sheet, fixes and re-runs (up to 3 tries), and marks the row. Each batch writes a short **summary** in the repo. The lead opens it with the agent, looks at each sheet, and says **keep** or **redo, with a note**. The phase proves this on **about 30 rows** (§The proving set) and closes; after that the loop keeps running and the rest of the list fills without a phase per batch.

### First human test

Reached in the batch summary (a tracked file, `.claude/CLAUDE.md` §The deliverable surface) and in each row's rig sheet, which the agent opens. **The lead looks and judges, and says keep or redo in chat; the agent records it. The lead types no command.**

**Cadence changed by RD-P11-3 (2026-10-02):** the clicks below are not driven one by one as each step lands. The loop builds the whole proving set first, and the lead judges every row **in one review at the end**: clicks 1–4 become one sitting over all the summaries and sheets. Redo notes from that review go back on the list for the loop's next batches.

| # | Step | What the lead looks at | Passes when |
|---|---|---|---|
| 1 | 11.1 | The first batch's summary (one row, `Polypropylene_Natural`), then its sheet: every slider through its range, Storm · Blender · Unreal | the summary says what was built, how, from what source, and what the critique found; the sheet reads as polypropylene and every row moves alike in all three. The lead says keep or redo |
| 2 | 11.1 | The list after the verdict | the row reads **kept** (or **redo**, with the lead's note). On a keep, the article carries its status (`approved` when all three tools moved alike, F-P11-1), visible as its Blender asset tag after the close's rebuild |
| 3 | 11.2 | A batch of 5 (§The proving set, batch 2): its summary and five sheets, one of them a rig-only re-judge | the lead can judge each from its summary line and sheet alone, and keeps or redoes each. **A redo is rebuilt by the next batch with the note in hand,** and the summary says what changed |
| 4 | 11.3 | The rest of the proving set, over several sessions, including the rows that needed a new wear layer: each new layer shown dialled up on its sheet | every row ends kept, redo or stuck-with-why; **the review time per article is measured** (seed question 2; the coverage research's 5–10 minutes is unmeasured) |

**Reconciled click by click:** click 1 needs the list file, the batch skill and one row built and rigged (11.1). Click 2 needs the keep/redo recording, also 11.1. Click 3 needs a batch of more than one and a redo carried forward (11.2); if click 1 is a keep, 11.2 plants its redo on one of its own five. Click 4 needs the new wear-layer path inside the batch (11.3). No click reaches past its step. **The fixture is real:** `Polypropylene_Natural` is an L1 Opaque whose four layers all exist (`Scratches01 · Fingerprints01 · Dust01 · Grime01`), so 11.1 needs no new layer and no download.

### In now / not now

**In now:**
- **The wish list**, one plain file in the repo, seeded from the 173 rows of `260925_R_LibraryCoverage_FirstRelease.md` Pass 2 **and** every article on disk as a rig-only re-judge row (F-LC-9: 45 `candidate`, 13 with no status, the system article excepted). Each row: the name, its slot, master, way of making it, scale, layers, a free note, and its state (`queued` · `built` · `stuck` with why · `kept` · `redo` with the note). The proving rows are marked.
- **The batch command** (a skill), its summary, and the keep/redo recording (F-P11-1's status mapping).
- **`/matter-generate` brought up to Phase10:** `Dust01` is a deposit with its `color_port` (F-P11-2). The batch reuses its steps 1–5 and replaces its hand-off (§6a, USDLiveView by hand) with the rig.
- **The proving set** (about 30 rows) and **the 7 new wear layers** it needs, made by the skill's §3a path.
- **No schedule.** A batch runs in a session (F-LC-8, BigPicture BP10).

**After the proof (the loop's work, not a step of this phase; kept from the seed):**
- The rest of the list (its remaining build rows, and the re-judges of the articles on disk) and the rest of the 22 wear layers.
- Articles on disk updated to carry their relevant layers (ruling C1); they keep their `v01` in place (the lead's "no versioning" ruling, 2026-09-25).
- `Scuffs01` and `Fingerprints01` regenerated with real coverage (seed question 10; measured at 3 % and 4 % coverage, Phase10 F-P10-5).

**Not now:**
- **The F82 (`specular_color`) and thin-film inputs** (seed question 3). The loop builds a row that wants one as an approximation and says so in its critique (F-LC-6). *Suggested at Phase10's close (agent, not ruled):* hold them until the proving sheets show metals reading wrong; if they do, that is a contract phase in Phase10's shape.
- **Further deposits** (dirt, soot, pollen): they take Phase10's `overlayN_color` shape when a row needs one; no new input.
- Localised colour or gloss through a mask (L7).
- **Hair rows:** *Hair That Reads as Hair* owns them (F-LC-10).
- Cutting, versioning or publishing a release: *Release Bundle and Consumer Contract* and *Version Management*. The pilot `matterlib-0.1.0` is untouched: no new article is in its lock.
- The catalog listing each article's layers and master (L9), which belongs to the release bundle's catalog.
- **A new gate or `run_all.py` lane** over the list or the batch: a lead ruling, and nothing asks for one.

### Reuse check

*What does the stack already provide, and which standards does this touch?*

**Provided, reused as is:**
- **The building agent:** a Claude Code skill runs in the session, and `/matter-generate` (Phase03) already does plan → Physically Based values or an ambientCG scan or generated textures → recipe → assemble → gate, and makes a missing wear layer (§3a).
- **The judge:** `tools/parity/rig.py <article> --sweep` renders all three tools on this machine and writes `sheet.png`, `scorecard.md` and `scorecard.json` (per-setting Moved values per tool, the seam and ruler checks). **The verdict word is computed by `rig.moved_verdict`**, which the batch imports rather than re-implements (`scorecard.json` holds the numbers, not the word).
- **The lifecycle:** the recipe's `status` (`draft → candidate → approved`, schema enum since Phase07), resolved by `tools/converters/working_tree.py` and shown as a Blender asset tag by `gen_asset_library.py`. Nothing new.
- **The gate:** `run_all.py` globs `MatterLibrary/materials/**/*.mtlx` and `recipes/*.json`, so each new article brings its own material, recipe and determinism checks.

**Custom, each with its gap:**
- **The wish-list file.** Gap: the queue exists only as a research markdown table, dated 2026-09-25, not editable by a tool, with stale status words (its C2/C3 blockers are built: F-P08-6) and no state column.
- **A small helper for the list** (next N rows · mark · keep · redo · write the summary). Gap: over 200 rows' state changes made by hand-editing a file is where a loop goes wrong. *The executor may fold it into the skill if the file stays simple enough to edit safely.*
- **The batch skill.** Gap: `/matter-generate` builds one brief and hands off to USDLiveView by hand; it never reads the rig. **It does not replace a native behaviour.** It sequences two existing ones.

**Not built:** a scheduler (BP10) · a tracked per-material scorecard (BigPicture Q-F's *"a small scorecard kept beside each material"* is met by reuse: each summary carries its rows' verdict lines) · a new gate.

**Standards touched:** the recipe schema's `status` enum (consumed as written) · the Glossary's *Status lifecycle* (consumed as written, F-P11-1) · `MasterSet.md`'s deposit rule (consumed; F-P11-2 makes the skill follow it) · `Identity.md` naming (each row) · `ToolingConventions.md` (new rows at the close).

### Decisions that bind

*One authoritative copy. Each cites where it was decided.*

| # | Decision | From |
|---|---|---|
| 1 | **The phase builds the loop and proves it on about 30 rows,** not the whole list by hand | F-LC-1 (BigPicture Pass 2, Pass 12; BP5) |
| 2 | **The judge is the rig's three-tool sheet and its Moved verdict**, not the skill's Storm preview. All three tools from the start | F-LC-2, F-LC-3 (Phase06 D9) |
| 3 | **No schedule;** a batch runs in a session | F-LC-8, BP10 (lead, 2026-10-01) |
| 4 | **Statuses:** the list says `kept`, never "approved". **A keep sets the recipe's `status` to `approved` when all three tools moved alike, and `candidate` when only Storm and Blender did** (the Glossary's definitions). A redo leaves it `draft` | F-P11-1 (corrects F-LC-11) |
| 5 | **Tries:** a row is fixed and re-run at most **3** times, then marked `stuck`, with why | `/matter-generate` §5 (its gate limit), reused |
| 6 | **Every article carries all its relevant layers at 0** (C1), and **`Dust01` is always a deposit with its `color_port`** | C1 (lead, 2026-09-25) · Phase10 10.3 · F-P11-2 |
| 7 | **Build by whatever works:** measured values, free scans, code-generated textures, image models. Licensing and provenance do not block; the tools keep recording provenance | BP8 (lead, 2026-09-26) |
| 8 | **F82 and thin film:** built as approximations, named in the critique | F-LC-6 (the CM4 precedent: *"I would rather have everything in and 'uncalibrated' yet then a bunch of magenta"*) |
| 9 | **No versioning:** every row is `v01`, and a redo is rebuilt in place | the lead, 2026-09-25 (*"Make a material, serve it to stage. no versioning"*) |
| 10 | **The review surface is the tracked summary and the sheets the agent opens.** USDLiveView stays available for a closer look at any one row | `.claude/CLAUDE.md` §The deliverable surface · BigPicture Pass 9 |
| 11 | **The push is the lead's** (a public repo) | `LOCAL_DELTAS.md` §Weighting |
| 12 | **A built row is committed as `draft`, locally, with its batch** | RD-P11-2 |
| 13 | **The lead reviews once, at the end of the proving set**, not row by row | RD-P11-3 |

**Rulings at the hand-off (lead, 2026-10-02), verbatim:** *"yes to 1 and 2... I do not need to review each one so if you just want to start building and cranking through them... we can review at the end.... go ahead with /execute P11"*
- **RD-P11-1 — answers Q-P11-1:** the Outcome is restated as proposed (§Outcome; the Roadmap's sentence kept as the loop's long-run aim).
- **RD-P11-2 — answers Q-P11-2:** commit each built row as `draft`, locally, with the batch.
- **RD-P11-3 — the review moves to the end:** build and run through the proving set without a per-row sitting; one review of every row at the end.

### Risk lane — `build` (verified against the tree, 2026-10-02)

- **What enumerates the trees this phase adds to:** `run_all.py` globs `MatterLibrary/materials/**/*.mtlx`, `recipes/*.json` and, under `library/`, **only `library/releases/`** (its lock, catalog, freeze and approval records). `source_provenance.py` reads a texture's own provenance. `freeze_release.py` hashes the staged tree, scoped to the lock since Phase03. **Nothing enumerates `library/` outside `releases/`, or `.claude/skills/`.** A new list file and batch summaries trip no control; each new article adds its own checks, as Phase07–10's 41 did.
- **The status field:** `approved` in a recipe changes a Blender asset tag (*"checked in USDLiveView, Blender and Unreal"*) and what `serve_to_stage.py` lists. It is not the release approval: `promote_release.py` is untouched and stays the maintainer's act.
- **A batch** touches no sign-in, secret or public edge. It writes only to this machine's tree, and the push stays the lead's.

### Step list

| Step | Intent | First clickable result |
|---|---|---|
| **11.1** | The list file (seeded in full, the proving rows marked) · the helper · the batch skill · the skill's deposit line (F-P11-2) · **one row built, rigged, summarised, and the keep or redo recorded** | clicks 1–2 |
| **11.2** | A batch of 5 (§The proving set, batch 2), including a rig-only re-judge and a redo carried forward with its note | click 3 |
| **11.3** | The rest of the proving set, batch by batch over several sessions, **including the 7 new wear layers**; the review time per article measured | click 4 |
| **Close** | The Blender library rebuilt once with every kept article · docs conformed (§Build map) · the next batches left queued on the list | — |

### The proving set (the default; the lead may edit the list)

*Chosen to cover every master but Hair (F-LC-10), every way of making a material (L1 values, L2 generated textures, L3 a scan), the old C1/C2/C3 blockers, and every new layer the first rows need. Names are the coverage research's; the skill re-plans each row and says where it differs (its §1).*

| Batch | Rows | Why |
|---|---|---|
| **1 (11.1)** | `Polypropylene_Natural_Clean_Base_s01_v01` (Opaque, L1) | every layer exists; Dust01 as a deposit |
| **2 (11.2)** | `BlackWalnut_Natural_Clean_Base_s01_v01` (Opaque, L3) · `Fireclay_Natural_Clean_Base_s01_v01` (Opaque, L2) · `LED_WarmWhite_Clean_Base_s01_v01` (Emissive, L1) · `Glass_Frosted_Clean_Base_s01_v01` (TranslucentThin, L1) · **re-judge** `Rust_OnSteel_Flaking_Base_s01_v01` (TwoLayer) | a scan, generated textures, an emitter, see-through matter and a rig-only row, all on existing layers |
| **3+ (11.3)** | **Existing layers:** `Slate_Cleft` (Opaque, L3) · `Terracotta_Unglazed` (Opaque, L1) · `Glass_Reeded` (TranslucentThin, L2) · `LeadCrystal_Clear` (TranslucentThick, L1) · `Silicone_Translucent` (Subsurface, L1) · `Paint_Gloss` (Opaque + coat, L1, was C2) · `Aluminium_Brushed` (Opaque + anisotropy, L2, was C3) | the rest of the masters and the old blockers |
| | **New layers:** `Granite_Polished` · `Onyx_Polished` (Subsurface, L3) · `NephriteJade_Polished` (Subsurface, L2) → **WaterSpots01** · `WhiteOak_Weathered` · `Concrete_BoardFormed` → **Cracks01** · `Loam_Natural` · `BeachSand_Dry` · `OakLeaf_Natural` (Masked) → **Pitting01**, **Patches01** · `MildSteel_Raw` → Pitting01 · `Acrylic_Clear` → **HairlineScratches01** · `Sapphire_Natural` (TranslucentThick) · `Gold_Polished` · `StainlessSteel_Polished` (F82 approximated, was C1) → HairlineScratches01, **Edges01** · `Paint_OnMetal_Chipped` (TwoLayer) → **PaintChip01** | 7 new layers (4 overlays, 3 masks) and the layer path proven |
| | **Re-judges:** `Lace_Floral` (Masked: the soft-coverage question, seed question 11) · `Diamond_Brilliant` (TranslucentThick) · `Neon_Signage` (Emissive) | the rig-only row on three more masters |

26 build rows and 4 re-judges. **Measured cost:** a three-tool `--sweep` took 6.4 min (Oak) and 7.2 min (Glass_Clear) after Phase10, so a row takes 7–22 min of rig time across up to 3 tries, plus the build, and a batch of 5 runs about an hour (F-P11-4).

### Compact build map

- **The list:** one tracked file, likely `library/wishlist.yaml` (YAML, beside the lockfiles and provenance records, CC0), one entry per row, short enough for a person to add a line by hand. **Seeded by a one-off script** parsing the research's Pass 2 tables (the script need not be kept), plus one re-judge row per article on disk. The research table stays as written; the list supersedes it as the working queue (annotate the research's Status with a date).
- **The helper:** likely `tools/converters/wishlist.py` (authoring), with units beside it for the state changes. **`keep`** writes the recipe's `status` (Decision 4), reading the verdict through `rig.moved_verdict` over the row's `scorecard.json`.
- **The summaries:** likely `library/batches/<date>-<n>.md`, one per batch: per row, the state, how it was built and from what, the critique's 4–8 lines, the Moved verdict per slider, the sheet's path (git-ignored, on this machine), and the keep or redo once given.
- **The skill:** `.claude/skills/matter-batch/SKILL.md` (a product surface, as `matter-generate` is): take N rows → for each, `/matter-generate` §1–5 with the row as the brief → `rig.py <stem> --sweep` → Read the sheet and the scorecard → fix the recipe (or the layer) and re-run, up to 3 → mark → write the summary. **A rig-only row skips the build.** It reads `/matter-generate` for the build steps rather than copying them.
- **`/matter-generate` §3 (F-P11-2):** a `Dust01` overlay entry carries `"color_port": "overlayN_color"`, and that port goes into `lcd_ports`.
- **Drafts in the shared tree:** Q-P11-2 decides whether a built row is committed as `draft` or left uncommitted until the keep.
- **Test surface (the `build` ceiling):** the existing `run_all.py` lanes (every new article's checks) · units for the helper · **one real-path smoke: the first human test's batches.** No new gate.
- **Execute's first acts:** baseline `run_all.py` (Phase10 closed at the inherited `approval_binds_freeze` red alone) and `check_exporter.sh` if anything under `blender/addons/` moves (nothing is planned to).
- **The close's doc conform:** `ToolingConventions.md` (the list, the helper, the summaries, the skill) · `Glossary.md` (*wish list*, *batch*) · `Experience_MatterLibrary.md` §Shipped · `260925_R_LibraryCoverage_FirstRelease.md` and `260926_R_BigPicture_NimbleSetup.md` Status (Q-D, Q-F settled here) · **`_Architecture.md` §Governance:** *"Running it automatically (nightly or per PR) is still (planned), owned by Library Coverage"*. The nightly half is struck (BP10) and the per-PR half belongs to Contribution Path: annotate with a date, do not delete · the Roadmap entry.

---

## Why this is a phase

Filling a library is a loop, not a sequence of phases: build, check in every tool, fix, keep (`260926_R_BigPicture_NimbleSetup.md` Pass 2, accepted as the working plan by the lead in BP5). **This phase builds that loop once and proves it on about 30 rows** (that research's Pass 12). After the close the loop keeps running, and the rest of the list fills without a phase per batch.

## What it consumes (re-measured 2026-10-02)

- **The library:** 58 articles. 30 are `biological` (Phase07–09); 28 are the rest, the system article included, across 12 classes. **45 recipes carry `status: candidate`**, 13 carry none (`working_tree.py` resolves them to their release status when the pilot holds them, else `draft`), **none is `approved`**.
- **Wear layers:** 9 of the 22 the list wants. Overlays: `Dust01` (the one deposit, Phase10), `EdgeWear01`, `Fingerprints01`, `Scratches01`, `Scuffs01`. Masks: `Crevice01`, `Grime01`, `RustBloom01`, `Verdigris01`.
- **The building half:** `/matter-generate` (Phase03), one article per brief. It never commits, and **its §3 predates Phase10** (F-P11-2).
- **The checking half:** `tools/parity/rig.py <article> --sweep`, all three columns on this machine: Storm, Blender (`~/.local/bin/blender`) and the Unreal runtime pinned in `unreal/RUNTIME.json` (`unreal-runtime-v3` since Phase10), downloaded under `unreal/package/`.
- **The list:** 173 rows in `260925_R_LibraryCoverage_FirstRelease.md` Pass 2, each with a name, folder, master, way of making it, scale and layers. Its status column is dated 2026-09-25.

## Seed questions — where each stands

| # | The seed's question | Where it stands |
|---|---|---|
| 1 | Skin, cloth and hair in the Outcome | **Answered.** CM4 moved the character classes to Phase07; nothing character-specific remains here. The Outcome's wording is Q-P11-1. |
| 2 | The whole ~173, or a first tranche? | **Answered by precedent:** prove on about 30 (BigPicture Pass 12); §The proving set. Click 4 measures the review time. |
| 3 | Carriers C1–C3 in or out? | **C2 and C3 are built** (Phase07: coat, fuzz, anisotropy; F-P08-6); one row each is in the proving set. **F82 and thin film are not;** out (F-LC-6). |
| 4 | The naming and structure gut-check (N1–N8, S1–S6) | **Answered by precedent:** resolved on contact, when the loop reaches a row it affects (BigPicture Pass 3, item 5, under BP5). N1, N2, N4, N5 and N8 were superseded by C5. **N3 (British spelling) is still unwritten** in `NamingConventions.md`. |
| 5 | The layer library: generated or converted from ambientCG? | **No policy needed:** the skill decides per layer (§3a), and the rig judges the result. |
| 6 | The risk lane | **`build`, verified** (§Risk lane). |
| 7 | A seam-check lane over the shared layers? | **Reuse, not a new gate:** the rig runs the seam check on every texture of every article it renders. |
| 8 | Do the pre-Phase03 base textures tile? | **Measured by the loop:** the re-judge rows run the rig's seam check. |
| 9 | Layers at their own size | **Built in** (Phase04): the skill's §6 critique and the rig's ruler check. |
| 10 | Wear layers too faint; dust can't show colour | **The colour half is done** (Phase10). **The faint half** (`Scuffs01`, `Fingerprints01`, F-P10-5) is the loop's work after the proof. |
| 11 | The LCD ruling, at volume | **The rig's bar is done** (Phase06's Moved verdict). Still binding on the loop: each article states the real substance, and masked articles take soft coverage (`Lace_Floral` is a proving re-judge). |

## Open questions

- **Q-P11-1 [lead] — The Outcome, restated.** → RD-P11-1 The Roadmap's *"Creators find materials for every class of matter in the taxonomy"* is where the loop ends up, not what this phase closes on. The close reads the Outcome verbatim, and a proving set of 30 cannot claim *"every class"*. **Recommended:** the wording proposed under §Outcome, with the Roadmap's sentence kept as the loop's long-run aim. *(Four tests: no ruling answers it, since the Roadmap rule makes the wording the lead's; necessary, as above; deliverable either way; both admissible.)*
- **Q-P11-2 [lead] — A built row in the shared tree: committed as `draft`, or left uncommitted until the keep?** → RD-P11-2 `/matter-generate` never commits (Phase03, a design choice, not a quoted ruling). At batch scale, in a tree other sessions share by design (`.claude/CLAUDE.md` §Git), uncommitted drafts sit in every sibling's `git status`, and a wildcard stage by any session would sweep them up. **Recommended: commit each built row as `draft`, locally, with the batch** (the push stays the lead's). A keep is then a one-line status commit, and a redo is rebuilt in place. *(Four tests: unanswered; necessary from batch 2; both deliverable; both admissible.)* (F-LC-4)

## Discovery Log

### Pass 1 — 2026-10-01 — the product docs read against the Outcome; the re-cut

*Distilled. Examined: the specs top-down (`_Architecture.md`, `Taxonomy.md`, `Experience_MatterLibrary.md`, `MasterSet.md`, `LCDSchema.md`, `NamingConventions.md`, `ToolingConventions.md`) · the coverage, BigPicture and hair research · Phases 05–09 for what they routed here · the tree (articles, recipes, layers, the skill, the rig, the Unreal pin, `run_all.py`'s globs) · grep for the phase's own names (nothing built) · learnings, all five domains (Storm S3, S5; Blender B1–B9; Unreal U7, U11; MaterialX M4; Claude Code CC1, no bearing) · sequencing (no newer ruling).*

- **F-LC-1 — The phase builds the loop, not 162 articles by hand** (BigPicture Pass 2, 5, 12; BP5). → Decision 1. The Outcome's wording → Q-P11-1.
- **F-LC-2 — All three tools are on this machine,** so "two tools = candidate, three = approved" (BigPicture Q-H) is no momentum rule here: the loop requires all three. → Decision 2. *(Q-H's status words stand, as the Glossary's definitions: F-P11-1.)*
- **F-LC-3 — The judge is the rig, not the skill's preview** (BigPicture Pass 9). → Decision 2.
- **F-LC-4 — Where the drafts are kept is open.** → Q-P11-2.
- **F-LC-5 — Only 9 of the 22 wear layers exist,** and `Scuffs01` is nearly empty. → the proving set's 7 new layers; the faint layers after the proof.
- **F-LC-6 — F82 and thin film are not built;** approximated and named. → Decision 8.
- **F-LC-7 — Colour on wear layers ran first, as Phase10** (lead, 2026-10-01: *"If 2 then we need to do that phase now instead."*). Closed 2026-10-01.
- **F-LC-8 — No schedule** (lead, 2026-10-01: *"The fixed times was ONE session... remove taht thought."*; BP10). → Decision 3.
- **F-LC-9 — Phase06's re-judging of the candidates is unclaimed;** the list carries every article on disk as a rig-only row. → §In now.
- **F-LC-10 — Nothing here overlaps *Hair That Reads as Hair*.** → §Not now.
- **F-LC-11 — Two things share "approved".** *Superseded 2026-10-02 by F-P11-1:* its conclusion ("keep sets `candidate`; `approved` waits for the first release") contradicted the Glossary. Its point stands: the list never says "approved", and the release approval is untouched.
- **F-LC-12 — Risk lane `build` (hypothesis).** Verified at Pass 2 (§Risk lane).

### Pass 2 — 2026-10-02 — after Phase10; the Brief

**Examined:** Phase10's close and its routing (F-P10-5, the deposit contract), commits since Pass 1 (Phase10, the F-P10-17 quick fix, the sweep-time measure, a retro: no sequencing ruling) · `.claude/skills/matter-generate/SKILL.md` (whole) · `tools/parity/rig.py` (the verdict, the scorecard, the CLI) · `recipe.schema.json` (`status`) · `validate_recipe.py` G7 and `assemble_mtlx.py` (the deposit) · `MasterSet.md` §Overlay (Phase10's refinement) · `working_tree.py`, `gen_asset_library.py`, `serve_to_stage.py` (who reads `status`) · `Glossary.md` *Status lifecycle* · `Phase07` D-S · `Phase03` (where "never commits" came from) · every tree enumeration in `tools/validators`, `tools/releases`, `tools/generators` · `ToolingConventions.md` (the roots, entry points, gates) · the coverage list's buildable rows, against the 58 articles and 9 layers on disk · `NamingConventions.md` §Planning ids · learnings since Pass 1 (none added; Pass 1's read stands).

**Findings:**
- **F-P11-1 — The status words are already defined, and Pass 1 had them wrong.** `Glossary.md` *Status lifecycle* (since Phase07): *"**candidate** = passed USDLiveView's renderer and Blender in the parity rig; **approved** = Unreal agrees too."* The schema's `status` description says the same, and `gen_asset_library.py` tags `approved` as *"checked in USDLiveView, Blender and Unreal"*. BigPicture Pass 9: *"**Keep** marks it approved (subject to the UE column)"*. So a keep on a three-tool sheet is `approved`, by the durable spec; F-LC-11's "approved waits for the first release" mixed this field with the release approval (`promote_release.py`), which nothing here touches. → Decision 4. No recipe is `approved` yet, so the proving set is the first.
- **F-P11-2 — `/matter-generate` §3 predates Phase10.** Its recipe snippet has no `color_port`, and the recipe gate (G7) does not require one, since a deposit is declared and not inferred. A loop-built article with `Dust01` would therefore carry colourless dust, unlike all 13 dusty articles Phase10 converted. → §In now; Decision 6.
- **F-P11-3 — The verdict word is not in `scorecard.json`.** It holds each tool's Moved numbers; `rig.moved_verdict` turns them into *moved alike* / ONE-SIDED / UNEVEN. The batch imports it. → §Build map.
- **F-P11-4 — A batch's cost, sized.** A three-tool `--sweep` took 6.4 min (Oak: Storm 201 s · Blender 81 s · Unreal 100 s) and 7.2 min (Glass_Clear: 204 · 84 · 147 s) after Phase10's close, on the test scene. With up to 3 tries a row is 7–22 min of rig time plus the build, and a batch of 5 is about an hour. A hypothesis for sizing, not a constant. Storm is the slowest column on both.
- **F-P11-5 — The list is the queue's only source, and it is stale in three ways:** its status words (C2/C3 are built), its rows already on disk (`Limestone_Veined`, `Marble_Veined`, `ABS_Glossy`, `Glass_Green`, `Earthenware_Natural`, `Rubber_Natural`, `Canvas_Natural`, `Denim_Indigo`, `Felt_Natural`, `Satin_Natural` and others), and 13 of the 22 layers it names do not exist. Seeding the list file reconciles all three once.
- **F-P11-6 — The lane holds** (§Risk lane): nothing enumerates `library/` outside `releases/`, or `.claude/skills/`.

## Discovery Status

- **Passes captured:** 2 (2026-10-01, 2026-10-02). **The Brief is complete.**
- **Working direction:** the build loop, proven on about 30 rows; the rest of the list fills after the close (F-LC-1).
- **Open decisions:** none. Q-P11-1 and Q-P11-2 were ruled at the hand-off (RD-P11-1, RD-P11-2).
- **Checks to carry forward:** the review time per article (click 4) · whether metals read wrong without F82 (the proving set's three metals; the suggestion under §Not now) · the `_Architecture.md` §Governance annotation at the close.

## Execution Log

**Run 1 (2026-10-02, the library machine).** Tree at start: `main`, `ed9242a`, clean. Gate baseline: `run_all.py` 15 PASS / 2 SKIP (compression, staging: no encoder) / 0 FAIL; the inherited `approval_binds_freeze` red is gone (the pilot was re-approved after Phase10).

**Findings in execution:**
- **F-P11-7 — The faint scratch layer trips the Moved floor in Blender alone.** On Polypropylene, *wear 1 at 1* (Scratches01) moved Blender 0.52 against the floor of 0.5, Storm and Unreal 0.03: **ONE-SIDED**, on a layer nobody can see in any tool. Expect it on every article carrying Scratches01 (and possibly Fingerprints01) until those layers are strengthened, which is the loop's work after the proof (§After the proof). The rig's rule is not loosened; such a row keeps as `candidate`, and the summary says why.
- **F-P11-8 — Why the old layers vanish: `B` filled only inside the feature.** A renderer filters `A` and `B` separately and multiplies them, so at a distance a layer whose `B` is 0 outside the feature delivers about mean(A) × mean(B): Scratches01 0.022, Fingerprints01 0.011. The 7 new overlays fill `B` everywhere (A×B 0.05–0.17). Now a rule in `/matter-generate` §3a. Regenerating Scratches01 and Fingerprints01 that way is the faint-layer work after the proof.
- **F-P11-9 — Two library limits a batch cannot fix.** (1) **Overlays can only roughen,** so damage layers (scuffs, scratches, edge wear) show nothing on already-rough matter: walnut (0.67), fireclay. (2) **The Emissive master's emission is a constant** the wear layers do not reach, so nothing dims an LED, dust included. Both are contract work (MasterSet), not loop work; recorded for a later phase.
- **F-P11-10 — See-through matter, three renderers, three looks.** Glass_Frosted: Storm clear, Unreal frosted, Cycles milky. The roughness, dust and soot rows read UNEVEN or ONE-SIDED from the renderers, not the recipe (the Phase05 limit, widened by rough transmission). Not tuned toward agreement; a keep sets `candidate`.
- **F-P11-11 — Re-judges measure the old articles (seed question 8).** Rust_OnSteel (pre-Phase03): **7 of 9 textures seam**, and the ruler finds no scale in any tool (it matches layer 1's texture; the floor mostly shows the rust blend, a rig limit on TwoLayer). It reads as a blocky grey-and-orange speckle, not flaking rust. All three tools agree, so a keep would set `approved`: `verdict` now prints seams, ruler and every slider that moved nothing, and the skill puts them on the summary's Verdict line, so a keep over them is the maintainer's eyes-open call (the status word stays the Glossary's).
- **F-P11-12 — Cracks01 is crazing, not wood checking.** On its first render (WhiteOak_Weathered) it reads as a faint polygonal network: right for a glaze, plaster or dried earth, wrong for wood, whose checks run along the grain. A grain-aligned layer (a `Checks01`) is the loop's to make when the wood rows come up; Cracks01 stays on the rows it fits.
- **F-P11-13 — The list's L3 often cannot be honoured.** Three of seven scan rows so far had no ambientCG asset that names the matter (walnut, slate, white oak), and the skill's rule is to name only what the source states, so they were built as L2 and recorded (`mark --lane`). Scanned stone often has no physical size (granite, onyx: 0 × 0 cm), set by judgement.
- **F-P11-14 — Two of this phase's new layers do not read as designed** (batch 4, their first renders):
  - **HairlineScratches01** (s001): its worn-patch variation repeats on a visible 1 cm grid, clearest where a polished metal's highlight breaks into a row of equal blobs. The cause is variation inside a 1 cm tile; the fix is a uniform hairline field, with the variation left to a mask (F-P11-8's note on fine layers).
  - **Edges01** (mask): it gates correctly, but reads as a lace of 2–4 cm cells, not wear at the object's edges. A tiling mask cannot know a mesh's edges; the library has no curvature or occlusion input. That input is contract work.
  - **Not regenerated on the run's own call:** the skills forbid overwriting an existing texture, and five articles already carry these files. **For the end review.**
- **F-P11-15 — The rig cannot judge a mirror or a gem.** Its surround is plain grey, so a polished metal has little to reflect, and its 36 cm sphere is about 18 absorption depths of sapphire (Blender draws navy-black). The rig judges agreement between tools, not whether a mirror metal or a gem looks right at its real size. A test-scene question, recorded for a later rig phase.
- **F-P11-16 — No master shows textured see-through glass.** Glass_Reeded's reeds are a normal map on a thin-walled pane, which cannot refract, so nothing seen through it breaks into strips; they show only as faint ribbing at grazing angles, in all three tools. Reeded, fluted or hammered glass needs refraction through a pane (a thick master on a thin mesh, or a new input): contract work, recorded.
- **F-P11-17 — Three Creator controls that cannot reach what they should** (batch 6; each is the assembler's graph, so contract work, recorded):
  - **A coat is out of reach of wear and roughness.** `coat_roughness` is a constant; overlays and `roughness_bias` roughen only the body under it. A scratched or smudged gloss paint cannot be shown (every coated row: Enamel_Gloss, car paint).
  - **The tint is dead on a fully subsurface article.** `subsurface_color` takes the tinted base colour only for Hair and `base_color_map` articles; at subsurface weight 1 (Silicone) the base colour is hidden.
  - **On TwoLayer the tint colours both layers** (it follows the blend), so a red paint turns its bare steel red.
  - *Also:* Paint_OnMetal_Chipped reuses MildSteel_Raw's Metal002 textures, so a redo of MildSteel_Raw with another scan changes it too.

| Step | Commits | Result | Next |
|---|---|---|---|
| 11.1 | `c7be9d4` (list, helper, units 11/11, skills) · the batch commit | ▶ **SCAFFOLD COMPLETE, review owed (RD-P11-3: at the end).** Batch `261002-1`: Polypropylene built, all three tools alike but F-P11-7's flag; 5.8 min of rig | 11.2 |
| 11.2 | `f9da94c`…`f879809` (batch `261002-2`, run by a fresh agent from the skill alone) · the strengthen commit | ▶ **SCAFFOLD COMPLETE, review owed (RD-P11-3).** 4 built (BlackWalnut as L2: no scan names walnut; Glass_Frosted; Fireclay; LED_WarmWhite), Rust_OnSteel re-judged, none stuck, 1 try each, 34.5 min of rig; gate 15/2/0. **No redo carried forward:** the review is at the end (RD-P11-3), so click 3's redo half moves to the next batch after the review. **Strengthen, from the agent's feedback:** `mark --lane`; `verdict` prints seams, ruler and sliders that moved nothing; `tools/parity/crop_sheet.py` (a sheet's rows, readable); the skill's wait, re-judge marking, review-line and §3a rules (F-P11-8) | 11.3 |
| 11.3 (batch 3) | `50ad1fb`…`e9582ca` (batch `261002-3`) · the skill fix | ▶ **Review owed (RD-P11-3).** 5 built: Granite_Polished (ambientCG Granite001A), Onyx_Polished (Onyx007), Slate_Cleft and WhiteOak_Weathered **as L2** (no source names them), NephriteJade (L2); 6 rig runs, 37.8 min; gate 15/2/0. Granite and Slate would keep `approved`, the rest `candidate` (UNEVEN rows at the floor). **First renders:** WaterSpots01 reads as dried rings at the right size, alike in all three, on polished faces (it can only roughen); **Cracks01 reads as crazing or dried mud, wrong for wood** (F-P11-12). Skill: a scan with no size, `git add` first, one row through its commit, an unconfirmed seam flag | next batch |
| 11.3 (batch 4) | `475b9c0`…`4555420` (batch `261002-4`) · the skill fix | ▶ **Review owed (RD-P11-3).** 5 built, 1 try each, 34.2 min; gate 15/2/0. Loam_Natural (ambientCG Ground048, "soil": a rename to `Soil_Natural` is flagged), Sapphire_Natural (three renderers, three looks: F-P11-10), Gold_Polished and StainlessSteel_Polished (no F82: F-LC-6), Aluminium_Brushed (L2, anisotropy 0.8: **the brushed highlight reads alike in all three**). Loam would keep `approved`, the rest `candidate`. **First renders:** HairlineScratches01 and Edges01 fail as designed (F-P11-14); Pitting01 and Patches01 gate correctly but cannot be judged on soil. Skill: the mask's channel design wins over slot order; judging a near-invisible layer | next batch |
| 11.3 (batch 5) | `447e601`…`fa88ca6` (batch `261002-5`) · the skill fix | ▶ **Review owed (RD-P11-3).** 5 built, 1 try each, 37.6 min; gate 15/2/0. MildSteel_Raw (ambientCG Metal002, "steel": name flagged), Glass_Reeded (L2, a normal alone: **the reeds cannot show**, F-P11-16), LeadCrystal_Clear (only Cycles refracts, F-P11-10), Concrete_BoardFormed (Concrete045, 2 m), Terracotta_Unglazed (Physically Based). Concrete and Terracotta would keep `approved`, the rest `candidate`. Pitting01 shows the same 1 cm grid on a highlight as HairlineScratches01 (F-P11-14). Seam flags on smooth maps are rounding (the check compares against a near-zero interior) | next batch |
| 11.3 (batch 6) | `bd6fe1b`…`7996fb4` (batch `261002-6`) · `crop_sheet.py --full` | ▶ **Review owed (RD-P11-3).** 5 built, 6 rig runs, 36.8 min; gate 15/2/0. Acrylic_Clear (Physically Based), Silicone_Translucent (judgement; no entry), Paint_Gloss (**the coat reads**, 2 tries), Paint_OnMetal_Chipped (TwoLayer: param-only enamel over the Metal002 steel MildSteel_Raw already carries, by **PaintChip01: reads as chipped paint up close, a speckle from afar**), BeachSand_Dry (ambientCG Ground055S). Paint_OnMetal_Chipped would keep `approved`, the rest `candidate`. Three library limits (F-P11-17) | the last proving rows |
| 11.3 (layers) | `98f2ae9` `9e1e780` `d1d31f2` `f4cb2f2` `5bc067e` `7202c48` `18a40a6` | **The 7 new layers**, by a parallel agent (CPU only): WaterSpots01 (s01), Cracks01 (s01), Pitting01 (s001), HairlineScratches01 (s001), Edges01 (mask, s01), Patches01 (mask, s1), PaintChip01 (TwoLayer mask, s01); seamless, byte-reproducible, provenance, LFS. Not yet rendered: the proving rows show them dialled up | the proving rows |
