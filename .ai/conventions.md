# Matter Library — Conventions

Rules and boundaries for this repo. Keep lean; deep detail lives in `Readme.md` and the
platform docs.

## MaterialX-First

- `.mtlx` is the single source of truth. Blender/Unreal targets are **derived**, never
  hand-authored as the master.
- Conform to ASWF MaterialX 1.39+. Carry IMRSV metadata via the `imrsv_metadata` nodedef
  (master material, scale tag, meters-per-tile, domain, class).

## Least Common Denominator (LCD)

- Only expose parameters all targets (MaterialX / Unreal Substrate / Blender Principled BSDF)
  can honor. If a target can do something the others can't, don't rely on it.
- Master materials are where per-target gaps get bridged so the visible result stays close
  (target ΔE < 2 under standardized lighting).

## Two-Tier Library (Source vs Versioned)

- **Source collection** is volatile and community-contributable under the matter taxonomy.
- **Versioned library** is curated. A release = `library/releases/matterlib-X.Y.lock.yaml`
  (a manifest pinning exact `vNN` of each material + texture set) plus a git tag.
- **Promotion** edits the manifest; it does not copy files. Carry-forward = the next
  manifest keeps the same pins for unchanged materials.

## Versioning

- **Two axes**: per-material/texture `vNN` (contributor) vs library release semver
  (maintainer). Don't conflate them.
- **Library semver**: MAJOR = breaking (LCD/master-material param change, scale-meaning
  change, a material retired); MINOR = additive; PATCH = drop-in visual fix.
- **Status lifecycle**: draft → candidate → approved → deprecated → retired.

## Immutability After Promotion

- Once `material@vNN` (or `texture@vNN`) ships in any released manifest, that file is frozen.
- A change is **always** a new `vNN+1`, never an in-place edit. Keeps old releases
  reproducible and back-compat real.

## Naming

- **Domain / Class** live in the **folder path only** (so materials can be recategorized
  without renaming).
- **Filename**: `Material_Variant_Condition_Detail_sNN_vNN.mtlx`. `Condition` defaults to
  `Clean`, `Detail` defaults to `Base` when nothing special applies.
- **Scale tags**: `s0001 … s100`, plus `sUKN` (see `Readme.md` scale table).

## Textures

- Tracked with **Git LFS**. Stored once under `textures/base` (matter hierarchy) +
  `textures/shared` (overlays, masks); referenced by many materials.

## Governance

- Source PRs are open but **CI-gated** (schema valid, naming/taxonomy valid, scale tag
  present, referenced textures exist, eventual automated parity render).
- The release manifests under `library/releases/` are **CODEOWNERS-gated** — only maintainers
  promote.

## Don't Delete Spec Functionality

- This repo is in research/define phase: design intentionally runs ahead of disk.
- When aligning docs, **never delete a previously-specified capability**. Mark it
  `(planned)`, `Todo`, `Drift`, or `Reevaluate` with a date instead. Preserve intent;
  annotate reality.

## Planning & Workflow

- Follow `…/AgenticEngineering_PlanningProcess.md`: research → phase plan → harden →
  implement → close.
- Phase numbering here is **independent** of the platform's Studio/Plugin/Stage line.
- Commit planning + docs before implementation (rollback baseline).
- This is a submodule: code/doc commits land here; the platform bumps this submodule's SHA at
  phase closure.
