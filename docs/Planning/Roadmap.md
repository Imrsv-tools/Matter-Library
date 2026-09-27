# Matter Library — Roadmap

Lightweight phase guide. Three sections: **`## Active`** (live work) → **`## Future`** (sequenced seeds + the backlog) → **`## Complete`** (closed phases, newest at the bottom).

> **Entry format — keep it scannable.** Each entry is just: the **heading** (name + status), a one-line **`Outcome`**, and **doc pointer(s)**. The **`Outcome` is what the USER can DO when the phase is done** — the *point* of the work, in plain non-technical language (no code symbols, no implementation detail, never tech-for-tech's-sake). **Always challenge it — "is there a user-facing result?"**: default to the user-facing outcome; a pure-infra / refactor phase MAY instead state a system-capability outcome, but the challenge is never skipped. If an `Outcome` already exists, don't rewrite it unless asked. The doc pointer is the phase doc if it exists, else the known relevant docs. **ALL technical content — scope, rename maps, root-cause, hazards — lives in the phase doc, never here.** This index exists so anyone can skim the phases in seconds.
>
> **Status vocabulary:** `RESEARCH` (no phase doc yet — the pointers are the raw material) → `SEEDED` (phase doc written) → `ACTIVE` (being worked) → `COMPLETE`. A `TBD` entry is simply one the lead has not numbered — it may hold a perfectly settled position, since **order is position in the list, never an ordinal**. Numbering is the lead's call: sometimes one as work starts, sometimes a whole span when committing to a Wave (Workflow §Phase Numbering).

> **Re-thought 2026-09-23 (Phase01 step 1.5)** around the library and the tools that make it usable, grow it and generate it (lead rulings R5/R11, `docs/Planning/Research/260923_R_StandaloneSetup.md`). The first phases make the library stand alone, be versioned and published, and be consumed by IMRSV. The pre-standalone plan is archived at `docs/Planning/Phases/Complete/PreStandalone/build_plan.md`; every planned idea in it is carried below or in the Parking lot.

==================================================================================
## Active

### Phase07 — Character Materials — ACTIVE *(discovery complete 2026-09-27, next `/execute`; runs here while Phase06 runs on the UE machine)*
**Outcome:** a character wears real materials from the library (skin, eyes, mouth, lips, nails, hair and basic clothing fabrics) in Blender and a USD viewer, and in Unreal once it is calibrated. None shows the missing-material magenta, on any character.
- `docs/Planning/Phases/Future/Phase07_CharacterMaterials.md`

==================================================================================
## Future

> **Re-sequenced 2026-09-26 (lead):** the test rig comes before building materials at volume. Phase05 runs on this machine and is pushed; Phase06 runs on the UE machine; work returns here for Phase07 on. Why: `docs/Planning/Research/260926_R_BigPicture_NimbleSetup.md`.
>
> **Re-sequenced 2026-09-27 (lead):** Character Materials becomes **Phase07** and runs here straight after Phase05, **at the same time as Phase06** on the UE machine. Its materials ship as candidates (uncalibrated) until the Unreal column exists: *"I would rather have everything in and 'uncalibrated' yet then a bunch of magenta."* Library Coverage becomes Phase08. Why: `docs/Planning/Research/260927_R_CharacterMaterials_MPFB2.md` (CM4).

### Phase06 — Unreal Test Runtime — SEEDED *(runs on the UE machine, alongside Phase07)*
**Outcome:** the test rig's picture sheet gains an Unreal column, rendered by a small Unreal app of our own that runs on any Linux machine with a GPU.
- `docs/Planning/Phases/Future/Phase06_UnrealTestRuntime.md`

### Phase08 — Library Coverage — SEEDED *(renumbered from Phase07, 2026-09-27; its character classes moved to Phase07)*
**Outcome:** Creators find materials for every class of matter in the taxonomy, including the classes IMRSV's character work needs (skin, cloth, hair).
- `docs/Planning/Phases/Future/Phase08_LibraryCoverage.md`

### Release Bundle and Consumer Contract — SEEDED *(un-numbered 2026-09-25: the lead re-sequenced the material work ahead of it; discovery Pass 1 kept)*
**Outcome:** a consumer can download one versioned, verifiable release of the library and use it without ever touching this repository.
- `docs/Planning/Phases/Future/PhaseTBD_ReleaseBundleConsumerContract.md`

### IMRSV Consumes Releases — RESEARCH *(integration; numbered on the IMRSV platform's line)*
**Outcome:** IMRSV Studio users get Matter materials from an installed release, including in packaged builds, with no copy of this repository involved.
- `docs/Planning/PlatformDependencies.md` (P1–P4, P10)

### Blender from a Release — RESEARCH
**Outcome:** a Blender user installs the Matter add-on and library from a release and uses Matter materials without cloning this repository.
- `docs/Planning/Research/260923_R_StandaloneSetup.md` (seed 4) · `docs/specs/Experience/Experience_MatterLibrary.md` §Shipped

### See the Library — RESEARCH
**Outcome:** anyone can browse what is in a release, with a preview image of every material.
- `docs/Planning/Research/260923_R_StandaloneSetup.md` (seed 5) · `docs/specs/Catalog/Catalog.md` §Thumbnails

### Version Management — SEEDED
**Outcome:** a maintainer can cut the next release from the last one — keeping, adding, deprecating and retiring materials — and every earlier release stays exactly reproducible.
- `docs/Planning/Phases/Future/PhaseTBD_VersionManagement.md`

### Author a Material End to End — RESEARCH
**Outcome:** a contributor can go from an idea to a validated material in the library in minutes, using one tool (the first cut of the Matter Manager).
- `docs/Planning/Research/260923_R_StandaloneSetup.md` (seed 7)

### Contribution Path — RESEARCH
**Outcome:** an outside contributor can submit a material and get an automatic verdict, with only maintainers able to put it in a release.
- `docs/Planning/Research/260923_R_StandaloneSetup.md` (seed 8) · `CONTRIBUTING.md`

### Parity Baselines — RESEARCH *(its build is Phase05 + Phase06, 2026-09-26; publishing the results for anyone to see stays here)*
**Outcome:** anyone can see, for each kind of material, how closely its MaterialX, Blender and Unreal renders match.
- `docs/Planning/Research/260923_R_StandaloneSetup.md` (seed 10) · `docs/specs/Tooling/CompressedDistribution.md` · `docs/Planning/Phases/Complete/Phase05_TestRig.md`

### Unreal Reference Masters — RESEARCH *(its masters are first built by Phase06, 2026-09-26)*
**Outcome:** an Unreal user outside IMRSV can drop in a package of the Matter masters and render library materials from a release.
- `docs/Planning/Research/260923_R_StandaloneSetup.md` (Pass 9, option B; R14 "B later") · `docs/Planning/Phases/Future/Phase06_UnrealTestRuntime.md`

### Parking lot — TBD
**Outcome:** unsequenced ideas, kept so their intent survives (Don't Delete Spec Functionality).
- Automated transformers (MaterialX → Blender / Unreal), after manual parity is proven. Parity-gate automation in CI. A Realm level above Domain. Texture storage beyond Git LFS (asset management, content-addressed pointers). Further engine targets. Personal saved variants, community scoring and contributor reputation (`docs/specs/Experience/Experience_MatterLibrary.md` §Future Layers). The planned roots in `docs/ToolingConventions.md` §Planned roots.

==================================================================================
## Complete

### Pre-standalone — built by IMRSV platform phases (2026-06 → 2026-07) — COMPLETE
**Outcome:** the foundations, the authoring harness, the first 12 materials, the release machinery and the Blender library, all built into this repo by the IMRSV platform's Materials wave.
- `docs/Planning/Phases/Complete/PreStandalone/` (`build_plan.md` §Delivered · `Phase01_Foundations.md` · `Readme_2026-07.md` · `FolderStructure.txt`)

### Phase01 — Standalone Bootstrap — COMPLETE
**Outcome:** anyone can understand, navigate and work on the Matter Library from this repository alone.
- `docs/Planning/Phases/Complete/Phase01_StandaloneBootstrap.md`
*Closed 2026-09-23.*

### Phase02 — One-Command Check — COMPLETE
**Outcome:** anyone can clone the library on a fresh machine, run one command, and see every material and release validate, with the result also checked automatically on every pull request.
- `docs/Planning/Phases/Complete/Phase02_OneCommandCheck.md`
*Closed 2026-09-23; automatic pull-request checks parked by the lead (→ Contribution Path).*

### Phase03 — Agentic Material Generation — COMPLETE
**Outcome:** a maintainer can ask an agent for new materials and receive validated candidates, with recorded provenance, ready for human judgement.
- `docs/Planning/Phases/Complete/Phase03_AgenticMaterialGeneration.md`
*Closed 2026-09-25.*

### Phase04 — Wear Layers at Their Own Scale — COMPLETE
**Outcome:** a wear layer (dust, scratches, scuffs) looks the right size on every material, whatever that material's tile size.
- `docs/Planning/Phases/Complete/Phase04_WearLayersAtTheirOwnScale.md`
*Closed 2026-09-26; the pilot's re-approval is owed by the maintainer.*

### Phase05 — Test Rig: Blender and USDLiveView Side by Side — COMPLETE
**Outcome:** the maintainer can put any material side by side in Blender and USDLiveView, with every slider moved through its range, and see where the two agree and where they drift.
- `docs/Planning/Phases/Complete/Phase05_TestRig.md`
*Closed 2026-09-27; one maintainer re-approval of the pilot covers Phase04 and Phase05.*
