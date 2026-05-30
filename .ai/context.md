# Matter Library — Agent Context

Navigation hub for the Matter Library. Keep lean; details live in the docs this points to.

## Identity

- **Project**: Matter Library — MaterialX single-source material library + toolset.
- **Role**: author materials once in MaterialX; transform to Unreal (Substrate) + Blender
  (Principled BSDF) targets with LCD visual parity; ship a stand-alone, cooked, versioned
  library the IMRSV Platform consumes.
- **Repo**: `Imrsv-tools/Matter-Library` (standalone project; submodule of `IMRSV_Platform`).
- **Local root**: `/home/peter/Documents/IMRSV_GITrepos/Matter-Library`.
- **Phase posture**: research / aggregate / learn / define. Design docs run ahead of disk —
  that's intentional. ADD/REFINE, don't DELETE (see `conventions.md`).

## Architecture (decided)

- **MaterialX = single source of truth.** ASWF MaterialX 1.39+.
- **Two-tier library**: volatile **source collection** (community-contributable, matter
  taxonomy) → curated **versioned library**.
- **A release is a manifest, not a copy** — `library/releases/matterlib-X.Y.lock.yaml` pins
  the exact `vNN` of each included material and texture set; each release is a git tag.
- **Two version axes**: per-material/texture `vNN` (contributor-driven) vs library release
  semver (maintainer-driven).
- **Promotion model A**: manifest + tags in one repo; CODEOWNERS-gated manifest is the
  control point; upgradeable to a separate library repo later without re-architecting.
- **Textures via Git LFS** (large, lower-churn; many materials share one texture set).
- **LCD parity** across MaterialX / Unreal / Blender; master materials bridge the gap.
- **UE cook project** lives in-repo at `bridges/unreal/`.
- **Target versions**: Unreal **5.7+** (Linux dev currently pinned to UE **5.6.1** per
  platform CLAUDE.md); Blender **4.x** (latest stable).

See `Readme.md` for the full model and `.ai/research/Library_Architecture_Research.md` for
the decision record.

## What exists vs planned

- **Exists**: `Readme.md`, `FolderStructure.txt`, 4 seeded `.mtlx` samples under
  `MatterLibrary/materials/{engineered/glass, engineered/metal, natural/stone,
  synthetic/plastic}`, this `.ai/` surface.
- **Planned**: `library/` manifests, `bridges/` (UE cook project, Blender), `tools/`
  (matter_manager, validators/CI, converters, preview_generators), `textures/` (LFS),
  master materials, transformers, parity gate.

## Active Phase

See `.ai/plan/build_plan.md` (**## Active**). The Matter Library phase line is **independent**
of the platform's Studio/Plugin/Stage numbering; it's referenced from the platform plan as an
external track.

## Working Conventions

See `.ai/conventions.md`. Highlights: MaterialX-first, LCD parity, source-volatile /
library-controlled, immutability-after-promotion, Don't Delete Spec Functionality.

## Key Docs

- This repo: `Readme.md`, `FolderStructure.txt`.
- Platform overview: `../IMRSV_Platform/IMRSV_Platform_Documentation/IMRSV_PlatformOverview.md`
- Planning process: `…/AgenticEngineering_PlanningProcess.md`
- Folder conventions: `…/AgenticEngineering_StandaloneProjectFolders.md`
- Studio-side material consumers (downstream): `…/Studio/Services/Service_MaterialX.md`,
  `Service_MaterialManager.md`.
