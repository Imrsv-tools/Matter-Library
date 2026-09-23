# Phase01 — Standalone Bootstrap

**Status:** ACTIVE — IN EXECUTION (started 2026-09-23). Lane: `build`. All lead calls are ruled (§Lead rulings). Numbered `Phase01` by the lead on 2026-09-23 — the first phase on this repo's own line.

## Outcome

**Anyone, whether a contributor, a consumer or a fresh agent session, can understand, navigate and work on the Matter Library from this repository alone.** That covers what it is, its vocabulary, its contract, its licence terms and its plan, with no need for the private IMRSV platform docs.

Concretely, at close this repo has:
- the Agentic Engineering method vendored in;
- the old `.ai/` scaffold folded into the standard shape;
- the Matter-owned specs brought home under `docs/`, rewritten for a public repo, with every conflict against the lead's rulings *annotated in place*;
- a Glossary;
- Apache-2.0 (code) and CC0-1.0 (content) licence files plus CONTRIBUTING and CREDITS;
- an identity-only README;
- a Roadmap seeded for what comes next;
- a list of the asks this repo has of its consumers.

## Why this is a phase

It is one user-facing result, *the repo stands on its own*, demonstrated by one path: open the repo, orient, look up a term, read the contract, see the terms and the plan. Nothing in it changes the library's tools, payload or contract.

The expensive-to-unwind choices are:
- where the specs live (every consumer's pointers will target it);
- glossary terms (names propagate into the system);
- what goes public (a public push cannot be taken back).

---

## The Brief

### Outcome
See above.

### First human test
Run it at the repo root after execute; the clicks follow the step order.

1. **(Step 1)** `cd /home/peter/Documents/_GIT_IMRSV/Matter-Library && claude` → type `/howdy`. It answers with what the Matter Library is, that it stands alone, that the Active phase is *Standalone Bootstrap*, and what's next. `/research`, `/discovery`, `/execute`, `/quick-fix` and `/retro` all exist as commands.
1.2. **(Step 2)** Open `docs/Glossary.md` and find **article**, **master**, **LCD schema**, **Creator tier**, **author tier**, **release bundle**, **scale tag** and **shipped-pixel rule**. Each is a one-line definition plus a pointer, and none of them links outside this repo.
1.3. **(Step 3)** Open `docs/specs/_Architecture.md`, follow every link into Ontology → Contract → Distribution, and every link resolves inside this repo. Then run the publication check (build map §Gates); it prints **0 hits**.
1.4. **(Step 4)** Open `LICENSE` (Apache-2.0), `LICENSE-CONTENT.md` (CC0-1.0 for `MatterLibrary/` materials and textures), `CONTRIBUTING.md` (the CC0 dedication affirmation plus the "credit is asked, not required" norm) and `CREDITS.md`. After the lead pushes, the GitHub repo page shows the Apache-2.0 badge.
1.5. **(Step 5)** Open `Readme.md`: it says what the project *is*, with no status banner. Open `docs/Planning/Roadmap.md`: Active is this phase, and Future lists the next phases, each with a one-line Outcome. Open `docs/Planning/PlatformDependencies.md`: it lists each ask of Stage, Plugin, Studio, USDLiveView and the platform docs.

*Reconciled:* each click lands in the step that produces it. Click 1 needs a Roadmap to exist, so step 1 carries the *structural* move of `build_plan.md` → `Roadmap.md`. The Roadmap *re-think* is step 5.

### In now / not now

**In now:**
- **Vendor the method** from upstream `PeteSmalls/agentic-engineering` @ **`9f52c7f`** (pushed `origin/main`, measured 2026-09-23 17:00; re-check at execution start), including the provenance stamp, `LOCAL_DELTAS.md` and `.claude/settings.json`.
- **Fold in the existing scaffold with `git mv`**, dropping no intent.
- **Bring home 18 platform `MatterLibrary/` docs** (~1,580 lines) into `docs/specs/`. Rewrite each for a public repo, and **annotate each conflict with R1–R16 in place** (`Drift (2026-09-23): … → see <phase>`), never silently rewriting the contract.
- **Glossary and NamingConventions** (R16).
- **Licence and contribution files:** LICENSE, LICENSE-CONTENT, CONTRIBUTING, CREDITS.
- **README and roadmap:** an identity-only README, the re-thought Roadmap, and `PlatformDependencies.md`.
- **Hygiene:** remove the tracked `stage.log`; gitignore `.claude/scheduled_tasks.lock`; absorb `FolderStructure.txt`.
- **Fix the public reference `.mtlx`.** It teaches a defect the contract has since forbidden. Replace it with a live assembled article.

**Not now:**
- **Any contract change.** The master token in the catalog (`schema_version` 3), the release-bundle spec, and re-expressing the master settings for Substrate belong to the release-bundle / consumer-contract phase. This phase only *marks* them.
- **Tool code:** hardcoded paths, the pinned environment and CI belong to the one-command-check phase.
- **Tags and re-versioning** (research Q5).
- **Any edit in another repo.** The platform side is *listed* in `PlatformDependencies.md`, not done.
- **Renaming IMRSV-branded identifiers** (`imrsv_metadata`, `imrsv:matterlibRelease`, `IMRSV_MissingMaterial`, `imrsv_lcd_export`). R16 keeps carried words; they are glossed as historical names, and the one principle tension is noted for the contract phase.
- **Scrubbing already-committed artifacts.** The approval JSON's approver field is a frozen, hash-locked record, so it is left as is (research Pass 6).

### Reuse check
*What does the chosen stack already provide, and which standards are touched?*

- **The method's `templates/` + `commands/` + `Methodology/`** provide the whole agent surface. Nothing is invented. The only local layer is `LOCAL_DELTAS.md`, which is the method's own override point.
- **The platform `MatterLibrary/` specs** are the contract text. They are *moved and scrubbed*, not rewritten from scratch, and the subfolder names are kept (R16 / Conway).
- **The platform glossary §MATTER LIBRARY** provides 22 terms that are carried with the same words. About 60 further terms used in the specs are missing from it; the set is inventoried in Pass 1.
- **`git mv`** keeps history across the folding-in, which satisfies the don't-delete rule without any extra machinery.
- **Standards actually touched:**
  - the method's §Setup Checklist;
  - `AI_WorkingAgreement` §Documentation Shapes Architecture;
  - this repo's §Don't Delete Spec Functionality: mark `Drift`/`Reevaluate` with a date, never delete.

### Decisions that bind
- **R1–R16** in `docs/Planning/Research/260923_R_StandaloneSetup.md` §Resolved. That is the one authoritative copy; this doc does not restate it.
- **From the method:**
  - vendor, don't submodule;
  - the stack-tier stubs ship empty *unless triggered*. NamingConventions is triggered (the filename grammar and scale tags exist). ToolingConventions is triggered (the `tools/` taxonomy exists). `docs/architecture/` is answered by `docs/specs/_Architecture.md`. CodingStandards stays a stub.
  - no AI co-author trailer (the template HARD RULE, and R8).
- **From this repo:** ADD/REFINE, don't delete. It is carried as a project HARD RULE in `.claude/CLAUDE.md` and as a practice in `AI_WorkingAgreement`.

### Risk lane — `build`
- **Checked against the high-rigor triggers** (`plan.md`: authorization · secrets · destructive migrations · data loss · the public edge).
  - No auth or secrets are touched.
  - Nothing is destroyed: moves are `git mv`, and the only removal is the tracked `stage.log`, which is noise.
- **The one irreversible act is publication.** The repo is public (verified with `gh repo view`), so a push exposes whatever it carries. That control is **the lead-gated push**; execute never pushes. It is backed by a **publication check that is demonstrated both ways**: run against the raw platform text it must hit, and against the scrubbed tree it must print 0.
- That is a gate on content, not an amendment to an edge control, so it does not need the `/plan` lane.

### Step list
Steps are numbered `1.1`–`1.5` (Phase01).

1.1. **Orient from the repo.**
   - Vendor the method.
   - `git mv` the old `.ai/` files to their new homes (build map).
   - Write `AGENTS.md`, `.claude/CLAUDE.md`, `AI_Orientation`, `AI_WorkingAgreement` and `LOCAL_DELTAS`.
   - Add `.claude/commands/*`, `.claude/settings.json` and `.gitignore`.
   - Move `build_plan.md` → `Roadmap.md` structurally, with this phase ACTIVE.
   - → *`/howdy` works* (test click 1).
2. **Look up any term.** `docs/Glossary.md` (the platform §MATTER LIBRARY terms re-glossed, the missing Matter terms, method terms, Retired identifiers) + `docs/NamingConventions.md` (filename grammar pointer, MaterialX casing, scale tags). → click 2.
3. **Read the contract at home.**
   - The 18 docs are moved to `docs/specs/`, keeping the platform subfolder names (ruling 1), scrubbed, and conflicts annotated.
   - Add `docs/specs/Consumers.md` (the boundary: which consumer docs stay in the platform).
   - Fix the reference `.mtlx`.
   - Record the platform research's settled decisions (S1–S9, with S6 superseded by R15) as a dated "Decisions of record" section in `docs/specs/_Architecture.md` — distilled, not migrated (ruling 2).
   - → click 3, with the publication check at 0.
4. **Know the terms.** LICENSE, LICENSE-CONTENT, CONTRIBUTING, CREDITS. → click 4.
5. **See what's next.**
   - The README becomes identity-only; its `(planned)` intent moves into the Roadmap and phase docs first.
   - The Roadmap is re-thought from research Pass 8 per R11: bootstrap → one-command check → release bundle + consumer contract → IMRSV consumes the bundle → the rest as TBD.
   - The old phase docs go to `Phases/Complete/` (delivered by platform phases, marked as such) or to `Phases/Future/`, trimmed to what is really open.
   - `docs/Planning/PlatformDependencies.md`, `FolderStructure.txt` → `docs/ToolingConventions.md`, `stage.log` removed.
   - → click 5.

**Split signal:** step 3 is the heavy one (about 1,580 lines rewritten with care), but it serves the same single journey. Time to the first click (step 1) is well under 60–90 minutes. No split.

### Compact build map

**Upstream copy** (@ `9f52c7f`, per `ADOPTING.md` §2):

| From | To |
|---|---|
| `commands/*.md` (14) | `.ai/commands/` |
| `templates/.ai/*` | `.ai/` |
| `templates/.claude/*` | `.claude/` |
| `templates/AGENTS.md` | `AGENTS.md` |
| `templates/docs/*` | `docs/` |
| `Methodology/AgenticEngineering_{Workflow,DocumentationMap,ProjectFolders}.md` | `Methodology/` |

**Folding in (all `git mv`, then edit):**

| Existing | → |
|---|---|
| `.ai/context.md` | `.ai/AI_Orientation.md`. Fix the local root and Blender 5.1+. "Architecture (decided)" → `docs/specs/_Architecture.md`. ⛔ **Do not transcribe its "What exists vs planned" or "Active Phase" blocks** into the orientation, AGENTS or CLAUDE.md. Those docs *point* at `Roadmap.md` and leave one line saying the summary is deliberately absent (upstream DocumentationMap §No-Duplication, added at `b1f36c2`, present at `9f52c7f`). The exists/planned content moves to the Roadmap and phase docs in step 5. |
| `.ai/conventions.md` | `.ai/AI_WorkingAgreement.md` §Project practices. Naming → `docs/NamingConventions.md`. |
| `.ai/commands/howdy.md` | Replaced by upstream. |
| `.ai/commands/housekeeping.md` | A `LOCAL_DELTAS` row plus a `ToolingConventions` check. |
| `.ai/plan/build_plan.md` | `docs/Planning/Roadmap.md` |
| `.ai/plan/Phase01_Foundations.md` | `docs/Planning/Phases/Complete/PreStandalone/Phase01_Foundations.md` (marked "delivered by platform Phase 52"). The subfolder keeps it from colliding with the new Phase01 (Workflow §Archive: an older scheme's docs go in a clearly-named `Complete/` subfolder rather than being renumbered). |
| `.ai/phases/future/PhaseTBD_VersionManagement.md` | `docs/Planning/Phases/Future/` (trimmed to the open remainder) |
| `.ai/phases/ignore/` | `docs/Planning/Phases/Complete/ignore/` |
| `.ai/research/Library_Architecture_Research.md` | `docs/Planning/Research/260530_R_LibraryArchitecture.md` |
| `FolderStructure.txt` | `docs/ToolingConventions.md` |

**Specs:** platform `MatterLibrary/<X>` → `docs/specs/<X>` (Q1).
- **SPLIT docs** (MasterSet, LCDSchema, Manifest, ReleaseModel, Experience, CompressedDistribution, `_Architecture`): only the Matter-owned sections come home. The consumer-side sections (UE pins, MID naming, wire and role numbers, deploy script, install discovery, Studio/Theater journey steps) become one-line pointers in `docs/specs/Consumers.md` and entries in `PlatformDependencies.md`.
- **Rename** `Experience_Matter Library.md` → `Experience_MatterLibrary.md` (no space).
- **Merge** `Catalog/Catalog.md`'s fictional chart into a real 0.1.0 article table.

**`LOCAL_DELTAS` rows this project needs:**
- **Separation model (R1):** this repo is a producer. There is no SHA bump here; the platform still pinning this repo is the platform's business during the transition.
- **Tracker:** `issue-create` → `Imrsv-tools/Matter-Library`. The existing platform-tracker Matter issues stay there (R4).
- **Where discovery Pass 1 reads:** it becomes `docs/specs/`.
- **How the project is run:** `python tools/validators/run_all.py`. Write the state in dated form: *"fails at import (no MaterialX Python) — measured 2026-09-23; owned by the one-command-check phase"*, never as a settled property (upstream §A claim carries its measurement).
- **"The artifact a person can reach":** the installed Blender add-on and Asset Browser, a release bundle, a usdview preview.
- **Namespaces:** release ids `matterlib-X.Y.Z`, material `vNN`, scale tags.
- **Weighting:** still building (R7), so bias toward the smallest unit that fits.

**Gates:**
- **Placeholder sweep:** `grep -rnE '<(PROJECT|DATE|SHA|owner>/<repo|one-line|ProductDefinition|absolute path|private\|public|Domain|Name)' --exclude-dir=.git .` → 0. The Workflow/illustrative `<n>`, `<sha>` and similar in the commands are excluded.
- **Publication check (both ways):**
  ```
  grep -rnE 'IMRSV_Platform_Documentation|\.\./(\.\./)?(Stage|Plugin|Studio|Planning|Learnings|Tests|3rdPartyGuides)/|/home/peter|~/\.config/imrsv|IoxMaterialInfo|MaterialXOps\.cpp|ExternalUSD\.cmake|GH ?#[0-9]+|#(35|47|64|78|79|80|81|82|350)\b|Tobias|project_no_legacy' docs/specs docs/Glossary.md docs/NamingConventions.md Readme.md CONTRIBUTING.md
  ```
  It must **hit** on the raw platform text and print **0** on the scrubbed tree. Allowlisted hits (with a reason) are recorded in the Execution Log.
- **Link check:** every relative link under `docs/` resolves to a file in this repo.

---

## Discovery Log

### Pass 1 — the platform-docs review (2026-09-23)

**Examined:**
- all 18 platform `MatterLibrary/` docs (~1,580 lines);
- the platform glossary §MATTER LIBRARY + NamingConventions §MaterialX;
- this repo's tree;
- the method templates @ `a6e7e81` (re-baselined to `b1f36c2` in Pass 2, then `9f52c7f` in Pass 3);
- the USDLiveView adoption (the closest precedent: an IMRSV standalone that absorbed an old flat scaffold);
- the research doc R1–R16.

The platform-docs survey was done by an agent reading the docs through `gh api` and is summarised here. The two load-bearing claims were re-verified by hand: the reference `.mtlx` defect and the absence of a catalog master field.

**Findings (distilled):**
1. **The specs are solid and mostly Matter-owned.**
   - **MOVE:** Taxonomy, Identity, MaterialXTemplate, RuntimeCatalog, CreatorAssetProfile, AuthoringGoldenPath, AuthoringHarness, USDValidationToolchain, `_Docs_Index`.
   - **SPLIT** (the consumer-side sections stay in the platform): `_Architecture`, Experience, MasterSet, Manifest, LCDSchema, ReleaseModel, CompressedDistribution.
   - **MERGE:** Catalog.
2. **Scrub load, per the build-map check:**
   - about 25 links into Stage/Studio/Planning/Tests;
   - about 180 platform phase ids;
   - GitHub ids #35≡#47, #81, #350;
   - private code cites (`MaterialXOps.cpp`, `ExternalUSD.cmake`, `IoxMaterialInfo`, protocol versions);
   - local paths (`~/usd-tools`, `~/.config/imrsv`);
   - a person's name;
   - a private memory name.

   Only a few phase-history facts are load-bearing: TwoLayer retained, the Phase-71 overlay/colour-space correction, the 60sq1 Blender ship, and the 60sq2 release model. They condense into one dated history note per doc.
3. **Conflicts with the rulings.** These are annotated in place, not resolved here:
   - **R14:** there is no master token in the catalog or manifest ✔. MaterialXTemplate even calls the manifest "authoritative for master mapping". The token lives only in the `imrsv_metadata` hint, and the `system` token (MissingMaterial ✔) is undefined.
   - **R15:** MasterSet says "legacy model, not Substrate, for v1", and its settings table is written in legacy shading-model terms.
   - **R1:** ReleaseModel's deploy step and its promote gate depend on Stage's fixture mirror. USDValidationToolchain slaves the toolchain pins to Stage's. No spec names a "release bundle".
   - **R9/R13:** AuthoringGoldenPath frames provenance around "sells the pixels" and favours indemnified licensed-data vendors. The live policy (ambientCG CC0 + procedural, no generative vendor) is not written into the spec.
4. **The reference `.mtlx` teaches a forbidden defect ✔.** It uses `overlay1_dust_tex`, loaded as `srgb_texture`, and mixes the overlay over base colour. The live articles use `overlay1_tex` in `lin_rec709`, applied as a modulator. Publishing it as-is would ship the bug as the reference. (In scope: replace it.)
5. **The authority is inverted in the text.** Four specs call this repo "stale … the source, not the authority". Moving home flips that.
6. **Stale against the live repo:**
   - Catalog's chart names articles that don't exist, and puts Diamond under utility.
   - `_Docs_Index` omits CreatorAssetProfile.
   - The Manifest YAML example is invalid.
   - CODEOWNERS and tags are claimed but absent.
   - AuthoringHarness's tool list is incomplete.
7. **Glossary.**
   - 22 platform terms: about 15 are Matter-owned; the rest are consumer-side (`M_MasterMaterial_<Token>`, rewrite-on-import, `category`, ReleaseConflict, the MID) and are kept only as boundary notes.
   - **"Name-keyed master resolution" conflicts with R14.** It is re-glossed as token-from-data plus the consumer's own token→asset map.
   - About 60 further terms are used but not glossed: article, source collection, author/Creator tier, render-role texture, freeze, staging, selector, recipe, shipped-pixel rule, lightweight/complete-portable, release bundle, and others.
8. **IMRSV-branded identifiers in a community contract** (`imrsv_metadata`, `imrsv:matterlibRelease`, `IMRSV_MissingMaterial`, `imrsv_lcd_export`). Fork test 1 answers this: **R16 + "never rename a carried term"** means they are kept and glossed as historical names. It is not a lead fork. The one real tension, `imrsv:matterlibRelease` against the specs' own "no `imrsv:` attributes" principle, is recorded for the contract phase.
9. **Learnings:** this repo has no `docs/Learnings/`. The platform learnings that mention Matter (build-deploy B23/B26, headless-Blender exit-0, the UE sampler/sRGB fallback) concern tool and deploy behaviour this phase does not touch. **This is a discharged read.** They are candidates for the toolchain and release-bundle phases.
10. **The phase name in the tree** exists only in the research doc and this seed; no prior phase built or deferred it.

### Pass 2 — upstream re-baseline (2026-09-23)

**Examined:** `PeteSmalls/agentic-engineering`, after the lead found the local copy was out of date.
- The local copy had **already been pulled** to `b1f36c2` (2026-09-23), which equals `origin/main` (fetched 2026-09-23).
- It carries two commits after the `a6e7e81` that Pass 1 read: `252cbae` (`plan.md` streamlining + the template's §Git rules for a shared index) and `b1f36c2` (eight portable lessons).
- The local AE working tree also holds **uncommitted edits by someone else**: `README.md`, `execute_close.md`, `execute_repair.md` and `execute_test.md` drop the dead `_ProvenanceAppendix` / `(WS-nn)` references. These were not touched here.

**What changes for this phase (folded into the Brief above):**
- ~~Vendor from `b1f36c2`.~~ Superseded by Pass 3: vendor from `9f52c7f`.
- `plan.md`'s `<ENGINE_SOURCE_ROOT>` placeholder **no longer exists**, so there is one placeholder fewer (grep, 2026-09-23).
- **New DocumentationMap rule:** briefing docs point at the registry and never restate it. This shapes how `context.md` is folded in (build map).
- **New Workflow tenets:**
  - *A claim carries its measurement:* state claims in `LOCAL_DELTAS` and orientation are written in dated form.
  - *Reading a green result:* the publication and link checks also get the set-level question *"what do all these checks never touch?"*. The known answer: neither reads **file contents outside `docs/` and the README**, e.g. comments in `tools/` or the `.mtlx` files. Those stay out of scope here and are named in the Execution Log rather than implied clean.
  - *The human's waiting time is a budget:* this confirms small vertical steps.
- **Template `.claude/CLAUDE.md` §Git** gains the shared-index rules and "multi-line commit messages go through `-F`". These arrive with the template, and nothing needs adapting.
- ~~Still unfixed upstream: the `docs/Methodology/**` references.~~ **Fixed upstream at `9f52c7f`** (Pass 3).

### Pass 3 — upstream finished its cleanup (2026-09-23)

**Examined:** `PeteSmalls/agentic-engineering` after the other session finished (fetched 2026-09-23 ~17:00). `HEAD` = `origin/main` = **`9f52c7f`**, with a clean working tree. Two commits after `b1f36c2`:
- `0c1929a`: the `execute_*` siblings drop the old sixteen-stage § numbering (~60 pointers), and the dead `_ProvenanceAppendix` / `(WS-nn)` links go.
- `9f52c7f`: the `docs/Methodology/` references become `Methodology/` (in six places, including the template `CLAUDE.md` §Lanes), and `execute_test`'s pointer to another project's learnings file is made stack-blind.

**Re-measured at `9f52c7f` (grep over `commands/`, `templates/`, `Methodology/`, `README.md`, `ADOPTING.md`):**
- **0** hits for `docs/Methodology`, `_ProvenanceAppendix`, `WS-nn` and `containers-and-deployment`;
- **0** hits for `ENGINE_SOURCE_ROOT`.

**Effect:** all three known upstream defects are fixed, so none needs a local adaptation and no `/retro` item is owed for them. **Pin `9f52c7f`.**

**Decision:** Brief written (above). Scope line: **bring home + scrub + annotate; no contract change.** Every contract change the rulings imply goes to the release-bundle / consumer-contract phase.

## Lead rulings (2026-09-23)

The lead, verbatim: *"go with your recommendations... review again as the other agent finished up"*.

1. **Spec layout:** `docs/specs/`, keeping the platform subfolder names (`Ontology/`, `Contract/`, `Catalog/`, `Authoring/`, `Distribution/`, `Tooling/`, `Experience/`).
2. **Platform research docs:** **distil, don't migrate.** Their settled decisions (S1–S9, S6 marked superseded by R15) go into a dated "Decisions of record" section in `docs/specs/_Architecture.md`; the originals are cited as platform history.
3. **Numbering:** **`Phase01`**, the first phase on this repo's own line. This doc moved from `Phases/Future/` to `Phases/` (numbering is the commitment). The old `Phase01_Foundations` goes to `Complete/PreStandalone/`.
4. **Upstream SHA:** vendor what is pushed when execute starts. The other session's cleanup has landed, so this resolves to **`9f52c7f`** (Pass 3). Re-check at execution start.

## Discovery Status

- **Passes captured:** 3.
- **Current working direction:** bring home + scrub + annotate, in five vertical steps; lane `build`.
- **Open decisions:** none. The Brief is complete; the lane is `build`, so next is `/execute`.
- **Checks to carry forward:**
  - re-verify the upstream SHA before vendoring (`9f52c7f` measured 2026-09-23 ~17:00; upstream may move again);
  - run the publication check both ways;
  - the push stays with the lead.

## Execution Log

*Ledger: step · result · next.*

- **Start (2026-09-23).** Tree: `main`, clean, 4 ahead of `origin/main`; no other session live. Upstream re-checked: `9f52c7f` = `origin/main`, clean.
- **1.1 — Orient from the repo.** Vendored `9f52c7f` (14 commands, 3 Methodology docs, `.claude/commands/` ×10, `settings.json`, `docs/` stubs and templates). Folded in with `git mv`: `context.md` → `AI_Orientation.md`, `conventions.md` → `AI_WorkingAgreement.md`, research → `260530_R_LibraryArchitecture.md`, VersionManagement → `Phases/Future/`, `ignore/` → `Complete/ignore/`. `housekeeping.md` retired into a `LOCAL_DELTAS` section. Carried content: the decided architecture and conventions principles → a seed `docs/specs/_Architecture.md` (merged in 1.3); naming → `NamingConventions.md`; the don't-delete rule → a `.claude/CLAUDE.md` HARD RULE + `AI_WorkingAgreement` §Settled practices. Roadmap in template form with Phase01 ACTIVE.
  - **Divergence from the build map (small, noted):** `build_plan.md` was **archived verbatim** to `Complete/PreStandalone/build_plan.md` and a fresh `Roadmap.md` was written. It was *not* `git mv`'d into `Roadmap.md`, because the Roadmap format forbids its technical content; archiving keeps every word, and 1.5 re-homes the intent. `context.md`'s "exists vs planned" block is likewise not carried into the orientation (upstream no-transcription rule); it survives in `git show 957069e:.ai/context.md` and in the archived `build_plan.md` §Delivered, for 1.5.
  - **Test-click refinement:** upstream `/howdy` prints a ≤2-line orientation (branch · clean · last closed · active), not an identity paragraph. Click 1 therefore checks that `/howdy` runs and names **Phase01** as active. Identity is in `.ai/AI_Orientation.md`.
  - **Lead verdict (click 1, 2026-09-23):** *"howdy works, continue with 1.2"*. ✅ **1.1 done** (landed at `0faabed`).
- **1.2 — Look up any term.**
  - `docs/Glossary.md` covers:
    - the 22 platform §MATTER LIBRARY terms, same words and re-glossed standalone; 6 of them are marked consumer-side;
    - about 60 Matter terms that were used but never glossed, grouped as library · identity · masters/LCD · releases · authoring/provenance · Creator/Blender · validation/compression;
    - the method terms, plus the project markers (`Drift`/`Reevaluate`…, Pre-standalone);
    - Retired identifiers.
  - `docs/NamingConventions.md` owns the casing matrix, the MaterialX alias, the id series with who assigns them, and the historical IMRSV-branded names kept on purpose. It points at `docs/specs/Ontology/Identity.md` for the grammar.
  - **Corrections made while glossing, each re-measured against the live tree (2026-09-23):**
    - the render-role textures are **linear** (`lin_rec709`, 3/3/3 articles), not "overlay = sRGB" as the platform glossary said;
    - master tokens in use: 7 masters + `system` (12 articles);
    - the ≤63 / `[A-Za-z0-9_]` rule is in `validate_material.py`;
    - carriage lanes and the opacity floor were re-read from LCDSchema and MasterSet.
  - **Pointer check:** there are 0 external or private links. The 16 `docs/specs/…` owners are **pending 1.3**, and `CONTRIBUTING.md` / `LICENSE-CONTENT.md` are **pending 1.4**. That list is 1.3's link check.
  - **Lead verdict (click 2, 2026-09-23):** *"glossary looks right, continue with 1.3"*. ✅ **1.2 done** (landed at `9b38adb`).
- **1.3 — Read the contract at home.** `docs/specs/` holds 20 files, 2,199 lines, measured 2026-09-23.
  - **Who wrote what:** three parallel writers took Ontology · Contract · Authoring/Distribution/Tooling under one shared rulebook. The coordinator wrote `_Architecture` (merged with the 1.1 seed and adding a §Decisions of record: S1–S9 distilled, with S6 marked superseded by R15), `_Docs_Index`, `Catalog` (the real `matterlib-0.1.0` table generated from the catalog and the articles), `Experience_MatterLibrary` (re-framed per R1/R9) and a new `Consumers.md` (the boundary: 14 IMRSV-owned topics moved out, with no private symbols).
  - **Annotations:** 24 `Drift`, 18 `Reevaluate` and 1 `Todo`, each dated. No contract text was changed silently.
  - **Reference `.mtlx`:** the platform template taught the overlay defect. It is replaced by a verbatim copy of the live Copper article (`diff`-identical body, `xmllint` ok).
  - **Consistency pass:**
    - MasterSet's two token rules, written while bringing it home, are marked "proposed, not yet ruled".
    - The historical keep-set examples are labelled as not in this library.
    - A cross-note on the `_vNN`-in-identity ambiguity was added to Identity.
  - **Gates (2026-09-23):**
    - **Link check:** 470 references across 21 files; 0 broken relative links. The path misses are all intentional: `PlatformDependencies.md` lands in 1.5, `matterlib-X.Y.Z` is a pattern, `library/staging/` is gitignored, and one old path is quoted inside a correction note.
    - **Publication check, both ways:** 22 hits over 6 raw platform sources, and 0 on the scrubbed tree.
    - **Wider sweep** (platform phase ids, private symbols, the deploy script, email): 0.
  - **What these checks never touch:** file *contents* outside `docs/`, meaning comments in `tools/` and the `.mtlx` files under `MatterLibrary/`. Those still carry old-layout paths (research Pass 6) and belong to the one-command-check phase.
  - **Unverified:** the public Blender issue link (`projects.blender.org/…/124263`) returns 403 to `curl`, which is evidence about `curl`. The lead opens it at click 3. The OpenUSD issue links were checked with `gh`.
  - **Next:** the lead runs click 3 → then 1.4.
