# Matter Library — Glossary

**Status:** Active. Created at bootstrap, not "when it settles" — the moment a second doc reuses a term, that term is load-bearing (`.ai/AI_WorkingAgreement.md` §Documentation Shapes Architecture). **Use the established term, or fix it here first.**

> **Shape.** Term + **one-line** definition + pointer — never the spec (`Methodology/AgenticEngineering_DocumentationMap.md` §Glossary entry shape). Detail lives with its owner; the moment an entry needs a paragraph, it is mis-homed.
>
> **Source of truth.** Where this file and an authoritative spec disagree, **the spec wins and this file is the bug.**
>
> **Heritage.** Most Matter terms were first defined in the IMRSV platform's glossary. They are carried here with **the same words** (a carried term is never renamed) and re-glossed to stand alone. Terms marked **(consumer-side)** belong to a consuming application such as IMRSV; they appear only where this repo's contract touches them. *Pointers into `docs/specs/…` resolve once Phase01 step 1.3 brings the specs home (2026-09-23).*

---

## The library

| Term | Definition |
|---|---|
| **Matter Library** | A community, CC0 MaterialX material library of elemental "matter" materials (stone, metal, glass, …) plus the tooling to author, curate, version and publish it. Consumers such as Blender, IMRSV and USD viewers use its published releases. → `docs/specs/_Architecture.md` |
| **Matter** | Real-world physical material as the organising idea: the library catalogues *what things are made of*, not objects. → `docs/specs/Ontology/Taxonomy.md` |
| **Article** | One material in the library: a single `.mtlx` file plus the textures it references. → `docs/specs/Contract/MaterialXTemplate.md` |
| **Source collection** | The volatile, community-contributable tier: every article in `MatterLibrary/`, whatever its status. → `docs/specs/_Architecture.md` |
| **Versioned library** (curated library) | The controlled tier: the articles a library release pins, curated by maintainers. → `docs/specs/_Architecture.md` |
| **Contributor** | Anyone who submits a material or texture, dedicated under CC0. Credited, but retains no rights (lead, 2026-09-23). → `CONTRIBUTING.md` |
| **Maintainer** (curator) | Someone who promotes articles into a library release. → `docs/specs/Contract/Manifest.md` §Governance |
| **Pilot release** | A release that was built and approved to prove the machinery, not to ship to users. `matterlib-0.1.0` is one (lead, 2026-09-23: "not in production"). → `docs/specs/Distribution/ReleaseModel.md` |
| **Realm** *(planned)* | A possible level above Domain, e.g. Matter vs Buildings, for use if a non-matter compound library ever lands. → `docs/specs/Ontology/Taxonomy.md` |

## Identity and naming

| Term | Definition |
|---|---|
| **Domain** | The top taxonomy level (natural · engineered · synthetic · environmental · utility). Carried in the folder path only, never in a filename. → `docs/specs/Ontology/Taxonomy.md` |
| **Class** | The second taxonomy level inside a Domain (stone, metal, glass, …; 19 defined). Folder-only. → `docs/specs/Ontology/Taxonomy.md` |
| **Matter filename grammar** (Material · Variant · Condition · Detail) | `Material_Variant_Condition_Detail_sNN_vNN.mtlx`; `Condition` defaults to `Clean`, `Detail` to `Base`. → `docs/specs/Ontology/Identity.md` |
| **Qualified Matter name** (Matter identity) | An article's filename stem. It *is* the material's identity: compositions carry the name and consumers resolve it. → `docs/specs/Ontology/Identity.md` |
| **Name budget** | A filename stem is ≤63 characters of `[A-Za-z0-9_]`, so the name survives Blender's USD export unchanged. → `docs/specs/Ontology/Identity.md` |
| **Scale tag** | The `s###` token for real-world scale in meters per UV tile (`s0001`…`s100`, `sUKN` for unknown). → `docs/specs/Ontology/Identity.md` |
| **Material version** (`vNN`) | One article's (or texture set's) own version, driven by the contributor. Never conflated with the library release version. → `docs/specs/Ontology/Identity.md` |
| **Two version axes** | Material `vNN` (per asset) vs library release semver (the whole set). They are separate, and a manifest pins which `vNN` each release includes. → `docs/specs/Ontology/Identity.md` |
| **Off-grammar article** | An article allowed outside the filename grammar because it is a system material (`IMRSV_MissingMaterial`). → `docs/specs/Contract/Manifest.md` |
| **MaterialX** / `mtlx` | The open ASWF shading standard and file format the library is authored in. Written `MaterialX` for people and `mtlx` in machine names; `Mtlx`/`Materialx` are banned. → `docs/NamingConventions.md` |

## Masters and the LCD contract

| Term | Definition |
|---|---|
| **Matter master** | The rendering class every article declares (Opaque, Masked, TranslucentThin, TranslucentThick, Subsurface, TwoLayer, Emissive). A renderer that partitions shader space (e.g. Unreal) implements one template per master. → `docs/specs/Ontology/MasterSet.md` |
| **Master set** | The versioned collection of masters. It defines what an article can *be*: a template instance, not arbitrary node soup. → `docs/specs/Ontology/MasterSet.md` |
| **Master token** | The master's name as data (`Opaque`, …, plus `system` for the missing-material fallback). The library pins the token; each consumer maps it to its own asset. → `docs/specs/Ontology/MasterSet.md` |
| **Class routing** | The rule assigning each Class a default master, with named exceptions (e.g. marble → Subsurface). *Drift (2026-09-23): consumers hold this in code today; R14 moves it into release data.* → `docs/specs/Ontology/MasterSet.md` |
| **`IMRSV_MissingMaterial`** | The library's system fallback material: the deliberate "broken material" look rendered when an identity cannot resolve. Its token is `system`. The historical name is kept. → `docs/specs/Ontology/MasterSet.md` |
| **LCD** (Least Common Denominator) | The discipline of exposing only parameters that every target renderer can honour, so an article looks close to the same everywhere. → `docs/specs/Contract/LCDSchema.md` |
| **LCD schema** | The two-tier parameter set, OpenPBR-named: the **author tier** plus the **Creator tier**. → `docs/specs/Contract/LCDSchema.md` |
| **Creator tier** | The 8 frozen end-user-adjustable ports: `base_color_tint`, `uv_scale`, `uv_offset`, `uv_rotation`, `overlay1_density`, `overlay2_density`, `maskset_blend`, `roughness_bias`. → `docs/specs/Contract/LCDSchema.md` |
| **Author tier** | The parameters an author sets and a Creator does not, including each master's defining property (cutoff · IOR · absorption · subsurface · layer blend · emission). → `docs/specs/Contract/LCDSchema.md` |
| **Carriage lane** (A / B) | Where an author-tier value lives in the `.mtlx`: **A** on the shader node under its OpenPBR name (OpenPBR has an input for it); **B** as a named author-tier interface input on the nodegraph (OpenPBR has none — the Masked cutoff and the TwoLayer layer-2 set). → `docs/specs/Contract/LCDSchema.md` |
| **Render-role texture** | A fixed per-article texture node, `overlay1_tex` / `overlay2_tex` / `maskset_tex`, loaded **linear** (`lin_rec709`). It is not Creator-adjustable. → `docs/specs/Contract/LCDSchema.md` |
| **Overlay** | A tiling surface effect (dust, scratches) packed as a *data* texture (normal XY · roughness bias · mask density), never an albedo bitmap. → `docs/specs/Ontology/MasterSet.md` |
| **Maskset** | A packed multi-mask data texture (up to 4 masks) driving blends such as paint or rust. → `docs/specs/Ontology/MasterSet.md` |
| **Modulator rule** | Overlays and masksets *modulate* the base material; they are never mixed over base colour. → `docs/specs/Ontology/MasterSet.md` |
| **TwoLayer blend** | The master whose single OpenPBR surface blends two layers per channel by the maskset (e.g. rust on steel). → `docs/specs/Ontology/MasterSet.md` |
| **Opacity floor** | `MIN_TRANSMISSIVE_OPACITY = 0.05`: the translucent masters never drop below it, so an article can state honest physics (`transmission = 1.0`) and still present a surface. The fix lives in the master, never in the article. → `docs/specs/Ontology/MasterSet.md` |
| **`imrsv_metadata`** | The optional nodedef in each `.mtlx` carrying hints (master, scale tag, meters-per-tile, domain, class). The historical name is kept. → `docs/specs/Contract/MaterialXTemplate.md` |
| **Parity** | How closely renders of one article match across MaterialX/USD, Blender and Unreal: calibrated, not pixel-identical (target ΔE < 2 where the master allows). → `docs/specs/Tooling/CompressedDistribution.md` |

## Releases and distribution

| Term | Definition |
|---|---|
| **Manifest** (library lockfile) | The authored YAML (`matterlib-X.Y.Z.lock.yaml`) pinning each article's and texture's version and status. It is the authored source of truth for a release. → `docs/specs/Contract/Manifest.md` |
| **Status lifecycle** | draft → candidate → approved → deprecated → retired, per material/texture version. → `docs/specs/Contract/Manifest.md` |
| **Immutability after promotion** | Once `material@vNN` ships in a release, that file is frozen; a change is always a new `vNN+1`. → `docs/specs/Contract/Manifest.md` |
| **Carry-forward** | The next release's manifest keeps the same pins for unchanged articles: no copying, no churn. → `docs/specs/Contract/Manifest.md` |
| **Library release** | A curated, semver-versioned set of articles pinned by a manifest (`matterlib-X.Y.Z`). → `docs/specs/Distribution/ReleaseModel.md` |
| **Runtime catalog** | The machine-readable JSON (`matterlib-X.Y.Z.catalog.json`) projected from the manifest and shipped with every release. It is versioned by its own `schema_version`. → `docs/specs/Contract/RuntimeCatalog.md` |
| **Projector** / projection | The tool (`tools/converters/project_runtime_catalog.py`) that validates the manifest and deterministically projects it to the runtime catalog. → `docs/specs/Contract/RuntimeCatalog.md` |
| **`creator_selectable`** | A catalog flag: whether an article is offered to end users in pickers (the missing-material fallback is not). → `docs/specs/Contract/RuntimeCatalog.md` |
| **Staging** (staging tree) | The built release payload, with PNG + compressed textures, under `library/staging/`. It is rebuildable and never committed. → `docs/specs/Distribution/ReleaseModel.md` |
| **Freeze** (freeze record, hash-lock) | `*.freeze.json`: the hashes of the manifest, catalog, `.mtlx` files and textures, combined into one `payload_digest`. → `docs/specs/Distribution/ReleaseModel.md` |
| **Release approval** | `*.approval.json`: the external record that promotes a frozen release to activation-eligible. It never edits the manifest. → `docs/specs/Distribution/ReleaseModel.md` |
| **Release activation** | Choosing which approved release an install serves, by writing the **active-release selector** (`active-release.json`); distinct from approval. → `docs/specs/Distribution/ReleaseModel.md` |
| **Install root** | The versioned folder layout a consumer installs a release into (`releases/matterlib-X.Y.Z/` + the selector). → `docs/specs/Distribution/ReleaseModel.md` |
| **Rollback / pilot recovery** | Re-pointing the selector at a prior approved release (**rollback**), or, audited break-glass only, at an installed but unapproved pilot (**pilot recovery**). → `docs/specs/Distribution/ReleaseModel.md` |
| **Release bundle** *(planned)* | The one self-contained, hash-locked, published artifact per release that every consumer installs instead of reading this repo (lead ruling R14, 2026-09-23). → `docs/Planning/Research/260923_R_StandaloneSetup.md` Pass 9 |
| **Master contract** *(planned)* | The master set, parameter names, texture roles and per-article master token, published **as data** in the release (R14). → `docs/Planning/Research/260923_R_StandaloneSetup.md` Pass 9 |
| **Release pin** (`imrsv:matterlibRelease`) | The key a USD composition uses to record which library release it was built against. The historical IMRSV-branded name is kept. → `docs/specs/Contract/CreatorAssetProfile.md` |

## Authoring and provenance

| Term | Definition |
|---|---|
| **Recipe** | The per-article JSON (`tools/converters/recipes/`) an article is generated from. Articles are generated, not hand-edited. → `docs/specs/Tooling/AuthoringHarness.md` |
| **Assembler** | The deterministic MaterialX-SDK script (`tools/converters/assemble_mtlx.py`) that writes an article from its recipe and textures. → `docs/specs/Tooling/AuthoringHarness.md` |
| **Authoring Golden Path** | The reference pipeline for *making* materials: generate a tileable albedo → decompose to PBR maps → assemble the `.mtlx` (+ QC). Distinct from the Creator Golden Path. → `docs/specs/Authoring/AuthoringGoldenPath.md` |
| **De-light / tileability** | The two QC checks on generated textures: baked-in lighting removed, and seamless at 2×2 / 3×3 tiling. → `docs/specs/Authoring/AuthoringGoldenPath.md` |
| **Provenance** | The recorded origin and licence of every shipped texture, with `evidence: {url, sha256}` for third-party sources. → `docs/specs/Contract/Manifest.md` |
| **Shipped-pixel rule** | No pixel ships in a release unless its provenance is recorded and it is CC0-dedicable (lead ruling R13). → `docs/specs/Authoring/AuthoringGoldenPath.md` |
| **CC0-dedicable** | An input that can be released under CC0-1.0 with no rights retained, e.g. ambientCG or in-house procedural textures. → `LICENSE-CONTENT.md` |

## Creator assets and Blender

| Term | Definition |
|---|---|
| **Creator** | An end user who applies Matter materials to their own work, in Blender, IMRSV Studio or elsewhere. |
| **Creator Golden Path** | The end-user *consumption* flow: assign in Blender → export → use downstream. Here, the Blender leg belongs to this repo and downstream steps belong to each consumer. → `docs/specs/Experience/Experience_MatterLibrary.md` |
| **Open Matter Creator asset** | A USD asset, exported from Blender, that binds Matter materials by name in one of two forms: **lightweight** (references a library `.mtlx`) or **complete-portable** (carries its own copy). → `docs/specs/Contract/CreatorAssetProfile.md` |
| **Blender Asset-Browser library** | The generated `blender/asset_library/MatterLibrary.blend`, which offers each `creator_selectable` article as a proxy. → `docs/specs/Experience/Experience_MatterLibrary.md` |
| **`MatterLCD_<id>` proxy** | The Principled-BSDF node group standing in for an article inside Blender, generated from its recipe. → `docs/specs/Experience/Experience_MatterLibrary.md` |
| **IMRSV LCD USD exporter** | The Blender add-on (`blender/addons/imrsv_lcd_export/`) that writes Open Matter Creator assets. The historical name is kept. → `docs/specs/Contract/CreatorAssetProfile.md` |
| **Golden** | A committed reference output a conformance check compares against (`tools/conformance/golden/`). → `docs/specs/Contract/CreatorAssetProfile.md` |

## Validation and compression

| Term | Definition |
|---|---|
| **Structural gate** | `tools/validators/run_all.py`: the lanes every article, manifest and release must pass. → `docs/specs/Tooling/AuthoringHarness.md` |
| **Determinism gate** | The check that the same inputs always produce byte-identical outputs (articles, catalogs, compressed textures). → `docs/specs/Tooling/AuthoringHarness.md` |
| **BCn** / compressed role | GPU block-compressed textures (BC7 / BC5 / BC4) chosen by a texture's role (colour, normal, single-channel). → `docs/specs/Tooling/CompressedDistribution.md` |
| **Codec A/B** | The ΔE2000 comparison of each PNG against its compressed twin, gating that compression stays visually faithful. → `docs/specs/Tooling/CompressedDistribution.md` |
| **OCIO parity config** | The colour-management config used so every parity render is judged under the same view transform. → `docs/specs/Tooling/CompressedDistribution.md` |
| **USD validation toolchain** | The pinned OpenUSD + MaterialX build (`tools/usd-toolchain/`) used to preview and check articles the way a USD consumer sees them. → `docs/specs/Tooling/USDValidationToolchain.md` |

## Consumer-side terms (IMRSV)

*Kept only because this repo's contract touches them; each consumer owns the definition in its own docs.*

| Term | Definition |
|---|---|
| **`M_MasterMaterial_<Token>`** (consumer-side) | IMRSV's cooked Unreal asset implementing a master token (e.g. `Opaque` → `M_MasterMaterial_Opaque`). Token ≠ asset: the library pins the token, the consumer owns the asset. |
| **Name-keyed master resolution** (consumer-side) | How a consumer maps an article to its master at render time. *Drift (2026-09-23): IMRSV does this with a compiled table today; under R14 it reads the master token from release data instead.* |
| **MID** (consumer-side) | Unreal's runtime material instance, created per use from a master and set from the article's values. |
| **Material `category`** (consumer-side) | IMRSV's picker filter key; it is the article's Class. |
| **ReleaseConflict** (consumer-side) | IMRSV's fail-loud state when a composition's release pin doesn't match the active release. |
| **Rewrite-on-import** / **Matter search path** (consumer-side) | How IMRSV's Stage recognises a Matter name in an imported asset and resolves the bare `@Name.mtlx@` reference through a search path over a release's `materials/<domain>/<class>/` folders. |

## Method terms

*⚠ **These are OWNED by `Methodology/AgenticEngineering_Workflow.md` — the rows below are a one-line gloss plus a pointer, never a second copy of the definition.** They are seeded on day one because, unlike anything stack-shaped, **this vocabulary is fully understood at adoption** and you are about to meet it in every command doc. **Where a row and the owning section disagree, the owning section wins and this row is the bug.***

| Term | Definition |
|---|---|
| **Phase** | Complex interconnected functionality; the top-level unit of work. → `Workflow.md` §Phase / Step / Task Terminology |
| **Step** | A **vertical**, testable chunk inside a phase — something a person can USE, never a layer with no user path. Numbered `Phase.Step` (`12.3`). → *same* |
| **Task** | An atomic, validatable check inside a step (`12.3.5`). **Available when a step needs decomposing; not a level every step populates.** → *same* |
| **Side Quest** | Unplanned work surfaced mid-phase and needed *now*; completed inline, inherits the phase's anchor. → *same* |
| **Quick Fix** | Shallow, self-contained, finishable in one context; the commit is the record. → `Workflow.md` §Units of work |
| **Issue** | Deferred standalone work, tracked; promotes to a Phase when it needs an anchor of its own. → *same* |
| **Brief** | Discovery's deliverable — Outcome · first human test · in/not-now · reuse check · lane · step list · build map. → `.ai/commands/discovery.md` |
| **First human test** | The exact click path, written before any code, that `/execute` hands the lead. → *same* |

## Project-local method terms

*Only project-specific usages appear here — a status word this project adds, a tier it names differently.*

| Term | Definition |
|---|---|
| **RESEARCH** | Roadmap status: the thinking lives in a research doc — no phase doc yet; the entry's pointers are the raw material. |
| **SEEDED** | Roadmap status: a phase doc exists. That doc is what discovery → plan → execute run against. |
| **ACTIVE** | Roadmap status: being worked. The phase doc moves from `Phases/Future/` up to `Phases/`. |
| **COMPLETE** | Roadmap status: closed; the phase doc moves to `Phases/Complete/`. |
| **TBD** | Roadmap status: a phase the lead has not numbered. It may hold a perfectly settled position — order is position in the list, never an ordinal. |
| **Probe** *(a.k.a. spike)* | A local, disposable feasibility test answering what documentation cannot settle. → `.ai/commands/research.md` §Disposable probes. |
| **Candidate** vs **selection** | A candidate has been assessed or probe-verified; a selection has been decided by the lead. A passed probe yields a candidate, never a selection. *(Not the same as the manifest status `candidate`, which is a material passing CI.)* |
| **`(planned)` · `Todo` · `Drift` · `Reevaluate`** | The dated markers this project uses instead of deleting a specified capability that isn't built or has diverged. → `.ai/AI_WorkingAgreement.md` §Project practices |
| **Pre-standalone** | Work done in this repo by IMRSV platform phases (2026-06 → 2026-07), before it had its own phase line. Archived in `docs/Planning/Phases/Complete/PreStandalone/`. |

---

## Retired identifiers

*When a term is replaced, record it here rather than deleting it — two names for one thing at the same layer is a bug, and a reader hitting the old word needs to land somewhere.*

| Retired name | Use instead | Why |
|---|---|---|
| `standard_surface` (as the article shader) | `open_pbr_surface` (OpenPBR, MaterialX 1.39) | The library moved OpenPBR-only before adoption. |
| "5 masters" | the 7-master set | TranslucentThick and Subsurface were added and TwoLayer kept, before adoption. |
| `.ai/context.md` · `.ai/conventions.md` · `.ai/plan/build_plan.md` | `.ai/AI_Orientation.md` · `.ai/AI_WorkingAgreement.md` · `docs/Planning/Roadmap.md` | Method adoption, 2026-09-23. |
| `bridges/unreal/`, `bridges/blender/` | `blender/` (built); the Unreal side per R14 | The Blender bridge was built at `blender/`; no `bridges/` folder exists. |
| "official library … for IMRSV" | "a community resource that IMRSV consumes" | Lead rulings R1/R9, 2026-09-23. |
