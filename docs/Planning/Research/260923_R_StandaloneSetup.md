# Research — Matter Library as a standalone project (setup scope)

**Opened:** 2026-09-23 · **Mode:** research — gathers, commits to nothing · **Next:** lead review → `/discovery` for the bootstrap

**Question:** what does it take to set Matter-Library up as a self-contained, independently-run project on the Agentic Engineering method? Where does its knowledge live today, what are its components, and what should its roadmap be about?

**Sources examined:**
- this repo's tree and git history (83 commits, 2025-11-11 → 2026-07-19);
- the platform documentation repo (`IMRSV_Platform_Documentation/`, private: `MatterLibrary/`, `Planning/`, `Methodology/`, the glossary and conventions);
- the platform umbrella repo's `.ai/`;
- the upstream method `PeteSmalls/agentic-engineering` @ `a6e7e81` (re-baselined on 2026-09-23 to `b1f36c2`, then `9f52c7f`; see `docs/Planning/Phases/Complete/Phase01_StandaloneBootstrap.md` Passes 2–3);
- the prior adopters BipZip, PitchBoard, 925Platform and USDLiveView.

**The source of this file's first contents:** a 2026-09-23 research session, read-only against every repo. No code, spec or config was changed.

---

## Resolved — lead decisions (2026-09-23)

| # | Decision |
|---|---|
| R1 | **Matter Library exists fully separate from the platform.** It is a *producer*. IMRSV (Stage/Plugin/Studio), Blender and USDLiveView are *consumers* of its **results**, not of its checkout. (This is the "sibling/producer" model of Pass 4, not a decoupled submodule.) |
| R2 | **The durable spec moves back into this repo** and becomes self-contained. The platform's `MatterLibrary/` tree becomes pointers plus consumer-side boundary docs. |
| R3 | **Separate licence for code** vs content. (Which licences: open question Q3.) |
| R4 | **Platform-tracker Matter issues stay where they are for now.** They may reach into Plugin/Studio directly. |
| R5 | **The roadmap is rethought from scratch.** It focuses on the library itself, the tools that make it usable, the features needed to grow it, and possibly *agentic generation* of new materials. The platform-wave history is history, not the plan. |
| R6 | **Targets: Blender 5.1+,** plus whatever the UE/Studio solution turns out to be. Blender 4.x is retired as a target. |
| R7 | **Not in production; still building.** The research/define posture ("ADD or REFINE, don't DELETE intended design") still holds. The approved `matterlib-0.1.0` is a pilot artifact, not a shipped product. |
| R8 | **No AI attribution in commits.** The person committing is the author and the responsible party (this matches the upstream template's HARD RULE). **Versions and tags are created as needed; everything is unreleased.** |
| R9 | **A community resource, not a sole product.** This settles Q2: the library is open content, and the platform-era "the library sells the pixels" framing is retired for this repo. |
| R10 | **Code licence: Apache-2.0.** This settles half of Q3; the content licence is still to pick (see Q3). |
| R11 | **The first roadmap phases are about standing alone, being versioned, and having IMRSV (Stage/Plugin) consume its results.** This matches what the docs already say the project is meant to be. |
| R13 | **Content licence: CC0-1.0** for materials (`.mtlx`) and textures. Contributions must be freely and fully distributable, with no rights retained by the project or the contributor. **Credit is a norm, not a licence term:** the project credits contributors, and consumers are *asked* to credit the Matter Library. CC0 cannot legally *require* attribution, so this has to be written as a request. Consequences:<br>• CONTRIBUTING needs a CC0 dedication affirmation ("I have the right to dedicate this, and I do");<br>• a credits record, either per-material contributor fields in the manifest/provenance or a CREDITS file;<br>• every third-party input must itself be CC0. ambientCG qualifies; CC-BY and "royalty-free" sources do not. |
| R14 | **Q4 approach accepted:** A now, B later (Pass 9). This repo ships a versioned release bundle plus the master contract as data. IMRSV instantiates at runtime. An optional reference UE masters package follows later. |
| R15 | **Unreal target: UE 5.8+ with Substrate** (resolves Q11). The platform's S6 "legacy model for v1" is retired for this repo. The master contract targets Substrate. *To verify:* the lead believes 5.8 requires Substrate; local sources neither confirm nor refute that. It doesn't change the ruling, because Studio already runs with Substrate on. |
| R16 | **Glossary on day one, reusing IMRSV's wording and concepts where they apply.** Source: the platform glossary's §MATTER LIBRARY (22 terms) plus the MaterialX casing rule, and the method's own seeded vocabulary. Terms are carried with the *same word* (Conway's Variant: never rename a carried term). Each is re-glossed so it stands alone in this public repo, without pointing into private platform docs. IMRSV-only terms (wire/ABI names, Studio UI names) are included only where this repo's contract touches them, and marked as consumer-side. |
| R12 | **Hard requirement:** the project manages **many materials, and many versions of each, with textures**. It can **select a subset, version it, and make it available to IMRSV**. **Q4 (who builds the UE side) must be defined in the docs.** The lead asked for a recommendation grounded in how the Plugin and Studio work today (Pass 9). |

---

## Pass 1 — Where the project actually is (verified on disk)

**Finding:** the repo's self-description is about three platform phases behind reality.

- `.ai/context.md` and `.ai/plan/build_plan.md` were refreshed on 2026-07-14. They still say "all articles `status: draft`", "promotion/BCn/parity owned by platform Phase 60", and "Active: platform Phase 60".
- Since then the platform ran Phase 60 → 60sq1 (Open Matter Creator Pipeline, done 2026-07-17) → 60sq2 (Matter Production Distribution, **complete 2026-07-19**). Both landed here: 16 and 15 commits respectively.
- `matterlib-0.1.0` exists: 12 materials and 12 textures, all `approved`, frozen (hash-locked) and with an approval artifact. Per R7 it is a pilot, not a release.
- **No platform phase owns Matter Library work now.** The platform roadmap's Active work is the humanoid-character wave. Its Appearance phase lists a *dependency* on Matter masters for skin, cloth and hair, with "integrate or side-line" left open. That is the one live external pull.
- Nothing has been committed here since 2026-07-19. Local `main` = `origin/main` = the SHA the platform pins (`957069e`). No git tags exist.

## Pass 2 — Component map (what the project IS)

The platform's `MatterLibrary/_Architecture.md` decomposes the system by concern: Ontology · Contract · Catalog · Authoring · Distribution · Tooling (+ Experience). The on-disk components map onto it:

| Component | On disk | State |
|---|---|---|
| **Materials (articles)** | `MatterLibrary/materials/{engineered,natural,synthetic,utility}/` | 12 single-file OpenPBR `.mtlx` (MaterialX 1.39): every master has an example, plus `IMRSV_MissingMaterial` and a UV-grid diagnostic. Generated from recipes, not hand-edited. Taxonomy coverage: 9 of 19 classes; no `environmental` domain. |
| **Textures** | `MatterLibrary/textures/{base,shared}` (Git LFS) | 30 PNGs: 3 ambientCG CC0 sets + 9 procedural sets; shared overlays and masks are packed *data* textures. |
| **Authoring harness** | `tools/converters/` (+ `recipes/`) | Deterministic MaterialX-SDK assembler, recipe → `.mtlx`, procedural texture generators, the lock → catalog projector. |
| **Validators** | `tools/validators/run_all.py` | 16 lanes: grammar, materials, manifest, determinism, catalog freshness/validation, provenance gate, no-projection guard, fixture sync, compression (±), staging, approval, freeze, approval-binds-freeze, activation. |
| **Release machinery** | `tools/releases/`, `library/releases/`, `library/provenance/` | lock.yaml → catalog.json → staging → freeze → approval → `active-release.json` selector, plus rollback and break-glass recovery. |
| **Compression** | `tools/compressors/` | BCn via `compressonatorcli` (BC7 / BC5 / BC4 by role). |
| **Blender bridge** | `blender/addons/imrsv_lcd_export/`, `blender/asset_library/`, `tools/generators/` | USD exporter add-on (lightweight + complete-portable) and the Asset-Browser library of 11 `MatterLCD_<id>` Principled proxies. |
| **Conformance and parity** | `tools/conformance/` | Creator-asset profile checks, golden USD, codec A/B (ΔE2000/SSIM), OCIO 2.4 parity config builder, render-leg probe. |
| **USD toolchain and previews** | `tools/usd-toolchain/`, `tools/preview_generators/` | Recipe for building OpenUSD 26.03 + MaterialX 1.39.5; sphere/dome preview wrapper. |
| **UE masters** | *not here*: in the platform's Plugin repo | 7 cooked `M_MasterMaterial_<Token>` masters + bake scripts. **ML owns the tokens and parameter names; the Plugin owns the assets.** |
| **Still-intended, not built** (kept per the don't-delete rule) | — | Matter Manager (import · promotion · subset/export · path remap); automated MaterialX → UE/Blender transformers; a standalone UE cook project; a parity gate in CI; CI at all; CODEOWNERS governance; texture storage beyond LFS (DAM/content-addressed); Realm level above Domain; further engine targets. |

## Pass 3 — Where the knowledge lives, and what comes home (R2)

**Finding:** most of the *durable truth* about this project sits in the private platform docs, not here. This repo's `Readme.md` says so in a banner.

**Candidates to bring home** (platform `IMRSV_Platform_Documentation/`, about 1,500 lines in total):

| Platform doc | Proposed home here | Note |
|---|---|---|
| `MatterLibrary/_Architecture.md`, `_Docs_Index.md` | `docs/architecture/` | Flip its "the standalone repo is the source, not the authority" line. |
| `Ontology/{Taxonomy, Identity, MasterSet}.md` | `docs/specs/Ontology/` (or similar) | MasterSet is mixed: tokens are ML's, the UE asset names are the consumer's. |
| `Contract/{MaterialXTemplate, Manifest, RuntimeCatalog, LCDSchema, CreatorAssetProfile}.md` + `examples/*.mtlx` | `docs/specs/Contract/` | RuntimeCatalog and LCDSchema are **boundary contracts**: ML becomes owner, and consumers reference them. CreatorAssetProfile already says it "graduates to a Matter-Library contract". |
| `Catalog/Catalog.md` | `docs/specs/` | Stale ("skeleton"). |
| `Authoring/AuthoringGoldenPath.md` | `docs/specs/Authoring/` | This is where the agentic-generation work (Pass 8) starts. |
| `Distribution/ReleaseModel.md` | `docs/specs/Distribution/` | Its deploy and install-discovery steps are consumer-side and must be split out. |
| `Tooling/{AuthoringHarness, USDValidationToolchain, CompressedDistribution}.md` | `docs/specs/Tooling/` or `docs/ToolingConventions.md` | The CompressedDistribution role→bit table mirrors a Stage wire enum: ML owns the roles, Stage owns the ABI. |
| `Experience/Experience_Matter Library.md` | split | Product intent comes here; the Studio/Theater journey steps stay on the platform. |
| Glossary §MATTER LIBRARY (22 terms) + the MaterialX casing rule | `docs/Glossary.md` | Seeded on day one, per the method. |
| Research `260611_R_MaterialChain`, `260618_R_MaterialsBuildGrounding`, `260716_R_OpenMatterCreatorPipeline` | `docs/Planning/Research/` (migrated) or cited | These hold the decision history, including S1–S9: OpenPBR, the 63-char name budget, offline BCn, **Substrate deferred / legacy UE material model for v1**, single-file `.mtlx`, and "Storm transmission/SSS is recognisable, not ΔE<2". |
| Learnings entries (build-deploy B23/B26; Stage L12; headless-Blender exit-0; UE sampler/sRGB fallback) | `docs/Learnings/<Domain>/` | Carry only the ones that bite in this repo. |

**Stay on the platform and are referenced from here:** Stage representation, textures, composition-pin and wire-versioning specs; Plugin material translation; Studio material UI and modals; the Blender export-preset guide; smoke tests.

**Precedent:** Open Morphology Foundation migrated its research byte-for-byte into its own repo and reduced the platform folder to a pointer README ("IMRSV is a downstream consumer"). Same move here.

⚠ **Public-repo filter.** This repo is **public**; the platform docs are **private**. Migrated text must be scrubbed of:
- private issue numbers, internal SHAs and snapshot names;
- collaborator names;
- local absolute paths;
- business/pricing notes;
- ABI internals such as struct sizes and `file:line` cites into private repos;
- links that resolve only inside the private repos.

This is an editorial pass, not a copy.

## Pass 4 — Independence model (R1 made concrete)

**The two options the lead asked to be distinguished:**
- **Decoupled submodule** (USDLiveView's model): the platform still *embeds* this repo as a git submodule pointer, but nobody is obliged to bump it. The platform still builds against a *checkout* of this repo.
- **Separate sibling / producer** (Open Morphology's model, and what R1 describes): the platform has **no git link** to this repo. Consumers take **published release artifacts** (a versioned bundle) and never read the working tree.

**What currently couples consumers to the checkout.** This is the work R1 implies. It is mostly consumer-side, so much of it is *platform* work to list, not do:
1. **Stage keeps a byte-identical fixture mirror** of the catalog and `.mtlx` files. `check_fixture_sync.py` enforces it, and "a catalog promotion forces a Stage commit".
2. **The Stage deploy script** overlays this repo's textures and staged `.dds` into the app.
3. **The Blender add-on finds the repo root by `parents[3]`** and hardcodes `MATTERLIB_RELEASE = "matterlib-0.1.0"`.
4. **USDLiveView / `imrsv-view`** default their search root to the live `Matter-Library/MatterLibrary/materials`.
5. **The USD toolchain pins "must track Stage's"** OpenUSD/MaterialX versions. Under R1 this inverts: ML declares its supported MaterialX/USD versions, and consumers state compatibility.
6. The platform umbrella repo still lists this repo in `.gitmodules`. Removing that is a platform action.

**Hypothesis:** the missing piece is a **release bundle + consumer contract**. A packaged `matterlib-X.Y.Z` (catalog + `.mtlx` + textures PNG/DDS + freeze + approval + a small manifest of supported versions) is published, for example as a GitHub Release. Each consumer (Stage, Blender add-on, USDLiveView) installs a bundle. The existing `ReleaseModel.md` + `active-release.json` selector is 80% of that design already.

**Platform dependencies to record, not do:** a `docs/Planning/PlatformDependencies.md`, following PitchBoard's practice, collects asks of consumers:
- Stage switches from mirror to bundle;
- the deploy script consumes a bundle;
- the Plugin master-bake inputs;
- the platform drops the submodule and repoints its docs.

## Pass 5 — Method adoption (upstream `a6e7e81`)

**What the method prescribes:** vendor, don't submodule.
- `templates/` → `AGENTS.md`, `.claude/{CLAUDE.md, settings.json, commands/*}`, `.ai/{AI_Orientation, AI_WorkingAgreement, README}.md`, `.ai/commands/LOCAL_DELTAS.md`, `docs/{Glossary, NamingConventions, ToolingConventions, CodingStandards}.md`, `docs/architecture/`, `docs/Learnings/`, `docs/Planning/{Roadmap.md, Phases/{Future,Complete}, Research, Support/{Troubleshooting,WorkflowFeedback}}`.
- `commands/*.md` → `.ai/commands/`.
- `Methodology/*.md` → `Methodology/`.
- Stamp the provenance line in `AGENTS.md` and `LOCAL_DELTAS.md`.
- Set `.claude/settings.json` `worktree.bgIsolation: none`.
- LICENSE and CONTRIBUTING at bootstrap (a public repo).

**The existing scaffold is folded in, not duplicated** (checklist §9). Moves use `git mv` so history and intent survive (don't-delete):

| Existing | Lands in |
|---|---|
| `AGENTS.md`, `.claude/CLAUDE.md` | Regenerated from the templates. The ADD/REFINE rule carries as a project HARD RULE. |
| `.ai/context.md` | `.ai/AI_Orientation.md`. "Architecture (decided)" goes to `docs/architecture/`; the exists/planned status goes to the Roadmap. Fix the local root: it is now `/home/peter/Documents/_GIT_IMRSV/Matter-Library`. |
| `.ai/conventions.md` | Principles (MaterialX-first, LCD, two-tier, immutability, don't-delete) go to `AI_WorkingAgreement` §Project practices. Naming goes to `docs/NamingConventions.md`. Versioning and governance go to the specs. |
| `.ai/commands/howdy.md` | Replaced by the upstream `howdy`. |
| `.ai/commands/housekeeping.md` | No upstream twin. Its checks become a `LOCAL_DELTAS` row or a `ToolingConventions` gate. |
| `.ai/plan/build_plan.md` | Audited, then → `docs/Planning/Roadmap.md` (see below). |
| `.ai/plan/Phase01_Foundations.md` | `Phases/Complete/` (delivered by platform Phase 52; marked as such). |
| `.ai/phases/future/PhaseTBD_VersionManagement.md` | `Phases/Future/`, trimmed to its genuinely open remainder: CODEOWNERS, tags, the deprecate/retire carry-forward. |
| `.ai/research/Library_Architecture_Research.md` | `docs/Planning/Research/260530_R_LibraryArchitecture.md`. Asserted-but-untaken "decisions" are demoted to open questions. |
| `Readme.md` | Describes what the project *is*. Status and `(planned)` tags move into the Roadmap/phases **first**, then get trimmed. |
| `FolderStructure.txt` | → `docs/ToolingConventions.md` / `docs/architecture/`. It is badly stale: it marks existing folders "(planned)" and omits `blender/`, `tools/{compressors,releases,conformance,generators}`. |

**Roadmap audit:**
- The current `build_plan.md` "Delivered" table is *platform-phase history*. It is recorded as history, not as local phases.
- "Version Management" is theme-shaped, a bundle the method rejects as one phase.
- The Parking Lot is seeds.
- Per R5 the Roadmap is rethought anyway (Pass 8). The method's convention is that only lead-numbered phases get numbers; everything else is `PhaseTBD_*`.

**Multi-repo / separation deltas for `LOCAL_DELTAS.md`.** Matter-Library is the first adopter since upstream dropped the multi-repo apparatus that still has real neighbours, so these are new ground:
- Template lines assume one repo and no SHA cascade. Under R1 that becomes **true again for this repo**: once consumers take bundles, there is no SHA bump to do. During the transition, until the platform drops the submodule, record that the platform may still pin this repo and that is the platform's business, not a step here.
- The platform's integration phases are numbered on the platform line; this repo keeps its own line.
- The tracker is `Imrsv-tools/Matter-Library` for new ML-only work. The existing platform-tracker issues stay put (R4).
- Where portable-method friction goes: upstream `agentic-engineering`.

**Known upstream defects to carry and report, not fix locally:**
- The `docs/Methodology/**` vs `Methodology/**` path mismatch (PitchBoard already flagged it).
- Dead `_ProvenanceAppendix` / `(WS-nn)` citations in `execute_test`, `execute_repair` and `execute_close`.
- "C++ style" and "platform" wording in DocumentationMap/ProjectFolders.
- ~~`plan.md`'s `<ENGINE_SOURCE_ROOT>` placeholder.~~ *Gone upstream at `252cbae` (plan.md streamlining); re-baselined 2026-09-23, see the phase doc's Pass 2.*

**Commands:** all upstream verbs fit. `execute_test`'s examples lean toward web/containers, so `LOCAL_DELTAS` must name this project's "artifact a person can reach":
- the installed Blender add-on and Asset Browser;
- a release bundle;
- a usdview preview;
- *not* the source tree.

`issue-create` targets `Imrsv-tools/Matter-Library`.

## Pass 6 — Public repo, licensing, hygiene

- **No LICENSE, CONTRIBUTING or CODEOWNERS; no `.github/`.** The Readme footer is only "© 2025 The Matter Library". The provenance doc declares the procedural textures "IMRSV-owned, released CC0-1.0" with no licence file behind it.
- **Tension to settle (Q2):** the platform's authoring doc frames the library as a product that "distributes textures as the product" and grades provenance for *sold* pixels. The provenance record releases this repo's pixels CC0. Open library, commercial content, or open core?
- **Personal and old-layout paths in committed files.** Ten scripts under `tools/conformance/` and `tools/generators/` hardcode a retired checkout path (`…/IMRSV_GITrepos/IMRSV_Platform/Matter-Library`), a home-directory USD install, and a scratch job directory. `.ai/context.md` carries the old root. The tracked `stage.log` carries an old platform path and is unrelated noise.
- **Binary churn:** the `.blend` files are not in LFS. The generated `blender/asset_library/MatterLibrary.blend` is committed and re-saved (HEAD is a pure re-save).
- **Stale in-file claims:** the 0.0.1 lock header says "7 proof articles"; the 0.1.0 lock header still describes the draft→candidate flip. Under R7/R8 (unreleased), editing these is allowed.
- **Tags:** none exist, although the docs say "each release is a git tag". Per R8, tags are created as needed; see Q5 for the scheme.
- **Attribution (R8):** the template's HARD RULE already forbids AI co-author trailers, and the repo history has none. Carry it as-is.

## Pass 7 — Toolchain (what "can run the gates" requires)

Derived from the imports and external binaries across `tools/` and `blender/`, and checked against this machine on 2026-09-23:

| Tier | Needed for | Requirement | This machine |
|---|---|---|---|
| **Core** | converters, validators, manifest/catalog, releases (most `run_all` lanes; CI-able) | Python 3.12 · **MaterialX 1.39.5 (PyPI `MaterialX`)** · pyyaml · numpy · Pillow · git-lfs | ⚠ **MaterialX Python missing everywhere.** System Python is 3.14; conda env `imrsv-usd-tools` (3.12) exists but lacks MaterialX. So **`run_all.py` fails at import**. git-lfs ✓ |
| **Compression** | `compression*` and `staging` lanes, freeze of `dds_set` | **compressonatorcli V4.5.52** (AMD, MIT core) via `$COMPRESSONATORCLI` | ✗ missing. The 0.1.0 freeze cannot be fully re-verified; those lanes skip. |
| **Colour and parity** | codec A/B, OCIO parity config | OpenImageIO (Python) · PyOpenColorIO 2.4 | ✓ in system Python 3.14; not in the conda env |
| **USD** | conformance, previews, render probe, `usdchecker` | OpenUSD **26.03** built with MaterialX (usdview, usdrecord, usdcat, usdchecker, `pxr`) via `tools/usd-toolchain/` (~30–50 min build) | ✓ built at `~/usd-tools/inst/usd-26.03` |
| **Blender** | add-on, asset library generator, export conformance | **Blender 5.1+** (R6) | ✓ 5.1.0. Note the add-on declares `(5, 1, 1)`. |
| **Unreal** | UE masters / cook (consumer side today) | UE 5.8 + the Plugin repo | outside this repo; see Q4 |
| **Agentic generation** (future) | Pass 8 | a generator (clean-provenance: Scenario/Bria-backed or Firefly; open bootstrap: ComfyUI + SDXL circular-pad; zero-risk: Material Maker) · decomposer (PBRify_Remix, CC0-trained; Substance Sampler Image-to-Material) · the existing SDK assembler · an LLM for scripting and metadata | none installed |

**Findings:**
- There is **no single pinned environment**: no `requirements.txt` or `pyproject`. The only pin is the conda `environment.yml` for the USD build. The core tier is small enough to pin and run in CI with no encoder or GPU.
- **The `fixture_sync` lane silently passes when Stage isn't at the superrepo path.** It is a gate that cannot fail in this layout. Under R1 it is replaced by a consumer-side check against a bundle, or removed with its intent recorded.
- **Several lanes "skip" when a tool is missing and still report green.** A green `run_all` doesn't say which lanes ran. The method's "a gate you cannot demonstrate both ways is not a gate" applies.

## Pass 8 — Re-thinking the roadmap (R5) — candidate seeds, NOT a plan

The goal as stated: **the Matter Library, and the tools that make it usable, grow it, and possibly generate it.** These are *candidate* phase seeds, each shaped as one thing a person can DO (§What counts as ONE phase). Order and numbering are the lead's call. They are listed so `/discovery` has a menu, not a sequence.

**Foundation (make it stand alone):**
1. **Standalone bootstrap:** method adopted, old scaffold folded in, specs repatriated (Pass 3), glossary seeded, LICENSE/CONTRIBUTING. *Outcome:* a fresh agent or contributor can orient from this repo alone.
2. **One-command check on a fresh box:** a pinned core environment, hardcoded paths gone, lane reporting that says ran/skipped, CI on GitHub for the core lanes. *Outcome:* anyone can clone and see the library validate.

**Usable (consumers get results, not the checkout):**
3. **Release bundle:** a packaged, versioned, verifiable `matterlib-X.Y.Z` artifact plus a consumer contract. *Outcome:* a consumer installs a release without the repo.
4. **Blender consumer from a bundle:** an installable add-on plus Asset-Browser library built from a release; Blender 5.1+. *Outcome:* a Blender user installs Matter materials and exports.
5. **See the library:** thumbnails and a browsable catalog or contact sheet (usdrecord previews, which double as parity baselines). *Outcome:* a person can browse what's in a release.
6. **UE solution:** decide and deliver what ML ships for Unreal (Q4). *Outcome:* Studio consumes Matter masters and materials from a release.

**Grow the library:**
7. **Author a new material end-to-end ("Matter Manager" v1):** scaffold → recipe → assemble → validate → add to the manifest, in one tool. *Outcome:* adding a material takes minutes, not a phase.
8. **Contribution path:** CONTRIBUTING, PR CI, a source→candidate gate, CODEOWNERS on `library/releases/`. *Outcome:* an outside contributor can submit a material and get a verdict.
9. **Coverage:** fill the taxonomy (9/19 classes today; no environmental domain); overlay/maskset variety.
10. **Visual-match baselines:** per-class ΔE across MaterialX/USD, Blender and UE under a standard light and view transform.

**Generate:**
11. **Agentic material generation:** an agent-run *generate → decompose → assemble → QC → propose* loop that yields **candidate** materials, never approved ones, with provenance tagged per pixel source and a human judgement gate.
    - **Prior art:** platform Pass 14 (2026-06-19) and `AuthoringGoldenPath.md`:
      - no tool emits valid MaterialX from a prompt, so a deterministic SDK assembler is required (and it already exists here);
      - AI accelerates texture generation and scripting;
      - the long pole stays human (metallic correctness, roughness consistency, parity judgement);
      - the **shipped-pixel rule**: provenance-clouded pixels never reach `approved`.
    - **Open:** the tool stack (paid clean-provenance vs open) and how much "agentic" means: an agent that drives the pipeline, or an agent that also judges.

## Pass 9 — Q4: who builds the Unreal side? (grounded in the live Stage / Plugin / Studio code)

**Examined:**
- Stage `MaterialXOps.cpp`, `MaterialExtractor.cpp`, `IoxMaterialTypes.h`, `ReferenceOps.cpp`, `scripts/build/deploy-to-studio.sh`;
- Plugin (`IMRSV_USDPlugin`) `USDMaterial.cpp`, `RuntimeTextureFactory.cpp`, `IMRSVStageRuntime.Build.cs`, `scripts/bake_master_{lcd,authortier}.py`;
- Studio `SModal_MaterialSelection.cpp`, `Config/DefaultEngine.ini`;
- this repo's `tools/releases/`;
- platform research `260611_R_MaterialChain` (F-B, S5, S6) and `260618_R_MaterialsBuildGrounding` Pass 6.

[V] = verified in code or data; [D] = only a doc says so. The lead spot-check re-verified four items marked ✔.

### How it works today

- **Nothing per-material is cooked in UE [V].** The only Matter UE assets are the **7 `M_MasterMaterial_<Token>` masters + `M_System_IMRSV_MissingMaterial`**, and they live in the Plugin.
  - Stage parses the `.mtlx` through USD/MaterialX and sends the values, LCD fields, author-tier fields and absolute texture paths over the wire.
  - The Plugin creates a runtime material instance (MID) of the right master per prim. It uploads textures straight from loose `.dds` on disk, falling back to PNG pixels over IPC.
  - **Adding a material or a version needs no UE rebuild**, as long as its class already routes to a master and it uses the existing texture roles and parameters.
- **This was a decision, not an accident [D].**
  - MaterialChain F-B chose "runtime-instanced masters + texture-only package; textures are NEVER cooked into the Plugin; baked per-material assets rejected as the drift-prone half of the old two-libraries mistake".
  - S5: "offline-precompressed BCn, NOT UE-cooked paks… zero UE cooking, zero engine-version lock".
  - S6: legacy UE material model for v1; "the master contract (names/params/LCD mapping) is the stable artifact; the implementation swaps."
- **Which master a material uses is hard-coded in Plugin C++ ✔.** Two tables map class → master (plus name exceptions: marble → Subsurface, diamond → TranslucentThick, rust → TwoLayer).
  - The `master_material` that every `.mtlx` already carries (in its `imrsv_metadata`) **is read by nobody ✔**.
  - The docs *intend* routing to be data: MasterSet says "master ID … from the manifest"; F-B says "master mapping rides in the manifest".
  - Today a new class, or an off-default routing such as "perforated metal → Masked", is a C++ change in the Plugin.
- **The master bakes read nothing from this repo [V].** The LCD and author-tier parameter names are hand-transcribed constants that mirror `LCDSchema.md` and `assemble_mtlx.py`. The masters are locked to the engine version (the 5.8 masters were unloadable on 5.6.1).
- **Material model tension ✔.** The masters are baked as the legacy model, but Studio runs with `r.Substrate=True`. So the legacy masters are presumably auto-converted, which is not verified and is in tension with S6.
- **Select a subset → version it: works here [V].**
  - lock.yaml (the subset: id + `vNN` + status + creator_selectable) → catalog → freeze → approval → staging.
  - At runtime: one active release per Stage process, chosen by `active-release.json`.
  - A composition's `imrsv:matterlibRelease` pin **detects** a mismatch (ReleaseConflict); it does not *select* a release.
- **Make it available to IMRSV: this is where it breaks [V].**
  - The Stage deploy script assembles each installed release from **three sources**:
    - the catalog and `.mtlx` from Stage's hand-synced fixture mirror (the **same `.mtlx` set copied into every release directory**);
    - the PNGs from this repo's *current* tree, not pinned to the release;
    - the `.dds` from the gitignored staging folder.
  - `activate_release.py` re-verifies the catalog and `.dds` hashes, but **not the `.mtlx` or PNG**.
  - **Packaged Studio builds do not include the library at all ✔.** `Build.cs` stages Stage but not `MatterLibrary/`, so a shipped build finds no catalog.
  - USDLiveView ignores the release selector and scans every release.

### Options

| | What this repo ships | What IMRSV does | Verdict |
|---|---|---|---|
| **A — Definition + payload bundle** | One self-contained, hash-locked **release bundle** per version: the catalog (with the master token as data), the lock, `.mtlx`, PNG, pre-compressed DDS, freeze and approval, laid out as `releases/matterlib-<ver>/`. Plus the **master contract** (master set + parameter names + texture roles) as a versioned spec. | Installs the bundle and activates it. The Plugin owns the UE masters and builds instances at runtime (**no per-material cooking — there is nothing to cook**). | **What the code already does**, minus the gaps above. Engine-neutral: Blender and USDLiveView consume the same bundle. |
| **B — A + a reference UE package** | Additionally an **optional "Matter for Unreal" output**: the master set as a versioned UE content plugin, the bake scripts, per-material "instance recipes" (master token + parameter values + texture role → `.dds`), and a minimal DDS/MID loader. | Depends on that package for its masters instead of owning them. | The community "ready to use in UE" answer, **without** per-material cooking. Costs: a UE-version-locked binary artifact and a UE 5.8 build/test lane in this repo, a Substrate-on/off decision, and a licence check on engine-derived nodes. |
| **C — Cooked per-material UE assets / paks** | Pre-cooked assets per material, per release. | Mounts paks. | **Rejected before** (F-B, S5). Engine-locked per release, no mount code exists, and it duplicates what runtime instancing already does. |

### Recommendation (for lead ruling)

**Adopt A now, with B as a planned later output. Write the boundary into the docs as a producer/consumer contract.**

1. **This repo owns the *definition* and the *payload*.** A release bundle is the only thing any consumer takes. It is engine-neutral, self-contained and hash-locked, and it retires the fixture-mirror coupling and the three-source deploy assembly.
2. **This repo owns the *master contract* as data.** The master set, parameter names, texture roles and the **per-material master token** go into the catalog (a catalog schema bump). Routing then stops being C++ in the Plugin, and adding a class or an exception is a library change, not a Plugin change.
3. **IMRSV builds the UE side at runtime, as it does today.** There is no per-material cooking. The Plugin keeps the 7 masters *for now* and conforms to the master contract.
4. **"A pre-cooked UE solution people can use" = option B, later.** The masters move here as an optional reference UE package once the community-UE goal is real. Because nothing per-material is cooked, "pre-cooked" means *the master set*, not the library. Record this as a Future seed; don't block the first phases on it.

**Platform dependencies this creates** (asks of Stage/Plugin/Studio; recorded, not done here):
- Stage installs and consumes a bundle instead of its fixture mirror.
- The deploy script and packaged builds install a bundle. Distribution to end-user machines is not implemented at all today.
- Stage/Plugin route by the master token from data. That needs a way to carry it (a wire field or a `shader_type` convention), which is an ABI decision on the Stage side.
- Studio's category list follows the taxonomy, not a hard-coded list.
- USDLiveView honours the active release.
- Decide the target material model (legacy vs Substrate) for the masters.

## Proposed bootstrap sequence (hypothesis for `/discovery`, not a commitment)

1. **Commit 1: adopt and absorb.** Vendor the method; `git mv` the old `.ai/` into place; fill placeholders; `LOCAL_DELTAS` with the separation deltas; settings; attribution rule.
2. **Commit 2: specs home.** Repatriate and scrub the platform `MatterLibrary/` tree, the glossary terms and the key research. Record the platform-side pointer work in `PlatformDependencies.md`.
3. **Commit 3: README, Roadmap and licence.** README becomes identity-only; the Roadmap is seeded from Pass 8 as the lead rules; LICENSE (code) + content licence + CONTRIBUTING.
4. **Commit 4: hygiene.** Paths, `stage.log`, `.gitignore`, LFS for `.blend`, stale headers, tags.

The toolchain pin and CI (seed 2) are best as the first *real* phase after the bootstrap.

---

## Open questions

| # | Question | Why it matters |
|---|---|---|
| ~~Q1~~ | ~~Spec layout?~~ **Resolved 2026-09-23 (Phase01 ruling 1): `docs/specs/`, keeping the platform subfolder names.** | — |
| ~~Q2~~ | ~~Open vs commercial?~~ **Resolved by R9: a community resource.** | — |
| ~~Q3~~ | ~~Content licence?~~ **Resolved by R13: CC0-1.0, with attribution requested.** | — |
| ~~Q4~~ | ~~UE solution?~~ **Resolved by R14: A now + B later.** | — |
| ~~Q11~~ | ~~Master material model?~~ **Resolved by R15: Substrate.** Follow-on work: the 7 masters are legacy-authored and run today only through UE's automatic legacy→Substrate conversion (Studio `r.Substrate=True`; platform Phase 70 D11 confirmed that Substrate blend modes are live). Re-authoring them natively on Substrate is a **platform dependency** (the Plugin owns them) until B moves them here. The parity baselines must measure the Substrate result. | — |
| Q12 | **Credits mechanics:** a per-material `contributors` field in the lock/provenance (and projected into the catalog?) vs a repo-level CREDITS file. Is contributor identity in a CC0 dedication just a name, or a name plus a link? | Part of the contribution-path seed; it shapes the manifest schema. |
| Q5 | **Versioning while unreleased:** keep `0.1.0` as the pilot tag and continue 0.x? Does immutability-after-promotion apply only from 1.0? Tag scheme `matterlib-X.Y.Z`? | R8 allows it; the rules need writing down. |
| ~~Q6~~ | ~~Phase line?~~ **Resolved 2026-09-23 (Phase01 ruling 3): the standalone bootstrap is `Phase01`; the old `Phase01_Foundations` goes to `Phases/Complete/PreStandalone/`.** | — |
| Q7 | **Toolchain form:** extend the conda env (it already hosts the USD build) vs a separate `pyproject` + venv for the core tier (lighter, CI-friendly) — or both? | This is seed 2's main fork. |
| Q8 | **Committed generated artifacts:** keep committing `MatterLibrary.blend` and `*.catalog.json`, or build them into the bundle only? | Churn vs "a clone just works". |
| Q9 | **The platform's Appearance dependency** (skin/cloth/hair masters): do we plan for it here, or leave it to the platform to ask through `PlatformDependencies.md`? | It is the only live external pull. |
| Q10 | **Agentic generation scope:** a pipeline agent vs a judging agent; paid clean-provenance vs open stack; is it a near-term seed or parked? *Narrowed 2026-09-23 in `260923_R_AgenticMaterialGeneration.md`: the agent authors recipes and drives the pipeline, and a maintainer still judges; the paid-vs-open fork is only the parked generative-imagery lane. Still open there as O1–O7.* | It shapes seed 11. |

---

## Status

**Passes captured:** 9.

**Update, 2026-09-23 (third round):**
- R13–R15 are recorded: CC0 content with attribution requested; Q4 approach A+B accepted; UE 5.8+ Substrate as the target.
- Q2, Q3, Q4 and Q11 are closed.
- **Still open:** Q1 (spec layout), Q5 (versioning while unreleased), Q6 (phase numbering), Q7 (toolchain form), Q8 (committed generated artifacts), Q9 (Appearance dependency), Q10 (agentic scope), Q12 (credits mechanics). None of them blocks `/discovery` on the standalone bootstrap; they can be answered inside it.

**Update, 2026-09-23 (second round):**
- R9–R12 are recorded: community resource, Apache-2.0 for code, the first phases are standalone + versioned + consumed by IMRSV, and the subset/version/make-available requirement.
- Pass 9 answers Q4 against the live code. **Recommendation: A now** (release bundle + master contract as data; IMRSV instantiates at runtime; nothing per-material is cooked) **+ B later** (an optional reference UE masters package). Awaiting the lead's ruling.
- **The first roadmap phases therefore line up as:**
  1. standalone bootstrap (seed 1);
  2. one-command check (seed 2);
  3. release bundle + consumer contract, including the master token as data (seeds 3 and 6, re-shaped by Pass 9);
  4. IMRSV consumes the bundle. That step is mostly platform-side work, listed in `PlatformDependencies.md`.

**Earlier summary (first round):**

**Current direction:** the lead has ruled on independence (sibling/producer), spec repatriation, split licensing, trackers, the roadmap rethink, targets, the not-in-production posture and attribution (R1–R8).

**The picture:**
- The components are mapped (Pass 2).
- The knowledge to bring home is inventoried and needs a public-repo scrub (Pass 3).
- Consumer coupling to the checkout is the core technical debt of independence; its fix is a release bundle (Pass 4).
- The method adoption and scaffold absorption are fully mapped (Pass 5).
- The core toolchain cannot run the gates on this machine today: MaterialX Python and `compressonatorcli` are missing (Pass 7).

**Open:** Q1–Q10.

**Next step:** the lead reviews this doc and answers the Q-table. Then `/discovery` runs for the **standalone bootstrap** (seed 1), and the Roadmap is seeded from Pass 8 as ruled. Nothing has been built; this file and its folder are the only change to the repo.
