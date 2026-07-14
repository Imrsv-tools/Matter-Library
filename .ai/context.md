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
- **Target versions**: Unreal **5.8+** (the platform forward line since 2026-07-06; the old
  Linux 5.6.1 pin is retired); Blender **4.x** (latest stable).

See `Readme.md` for the full model and `.ai/research/Library_Architecture_Research.md` for
the decision record.

## What exists vs planned

*(Refreshed 2026-07-14 — the platform Materials wave (Phases 52–71) built most of what this
section used to list as "planned". Verified against the live tree, not asserted.)*

- **Exists — the authoring + curation spine is BUILT and in production use:**
  - **12 articles** under `MatterLibrary/materials/{engineered, natural, synthetic, utility}/`
    — single-file OpenPBR (`open_pbr_surface`, MaterialX 1.39). **Every one of the 7 masters
    has a real, Creator-selectable example article** (Phase 71); the set covers
    Opaque · Masked · TranslucentThin · TranslucentThick · Subsurface · TwoLayer · Emissive,
    plus the `IMRSV_MissingMaterial` system material and the UV-grid diagnostic.
  - **`tools/converters/`** — `assemble_mtlx.py` (the deterministic MaterialX-SDK assembler),
    `build_proof_subset.py`, `project_runtime_catalog.py`, the procedural texture generators
    (`gen_article_textures.py` / `gen_shared_textures.py` / `gen_uvgrid.py`), and one
    **recipe per article** under `recipes/`.
  - **`tools/validators/`** — `run_all.py` over `validate_material.py`, `validate_manifest.py`,
    `check_determinism.py`, `check_fixture_sync.py`. This is the producer-side structural gate.
  - **`tools/preview_generators/`**, **`tools/usd-toolchain/`**.
  - **`library/releases/`** — `matterlib-0.0.1.lock.yaml` (the authored manifest) **and**
    `matterlib-0.0.1.catalog.json` (the projected runtime catalog Stage reads).
  - **`MatterLibrary/textures/{base,shared}`** under Git LFS.
  - **The two-tier LCD contract is frozen and live**: the **Creator tier** (8 adjustable ports)
    and the **author tier** (each master's defining property — cutoff · IOR · absorption ·
    SSS · two-layer blend · emission). Both are authored here, enforced by the validators, and
    consumed end-to-end by the platform. See `Docs/MatterLibrary/Contract/LCDSchema.md`.
  - **Master materials exist as 7 cooked UE masters** — but they live in the **Plugin** repo
    (`IMRSVStagePlugin`), baked by its `bake_master_authortier.py`, **not** in this repo's
    `bridges/unreal/`. That is the shipped arrangement, not a gap.
- **Still planned** *(unchanged intent — see `.ai/conventions.md` §Don't Delete Spec
  Functionality)*: **`bridges/`** — the standalone UE cook project and the Blender material
  library + export-preset extension; **`tools/matter_manager`** (import · promotion ·
  subset/export · path remap); **automated transformers** (MaterialX → UE / Blender);
  the **parity gate** (standardized ΔE comparison as a promotion CI check); CI wiring.
  The **production texture delivery (BCn)** and **`usdrecord` parity baselines** are owned by
  platform **Phase 60**.
- **Article status**: all articles are still `status: draft` in the lockfile. Promotion
  (`draft → approved`) + the clean-provenance production tool-stack decision are **Phase 60**.

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
- Planning process: `…/AgenticEngineering_Workflow.md`
- Folder conventions: `…/AgenticEngineering_StandaloneProjectFolders.md`
- Studio-side material consumers (downstream): `…/Studio/Services/Service_MaterialX.md`,
  `Service_MaterialManager.md`.
