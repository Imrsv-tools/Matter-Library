# Matter Library — Architecture

> **Seed (Phase01 step 1.1, 2026-09-23).** This is the landing spot for the design principles previously held in `.ai/conventions.md` and `.ai/context.md` §Architecture (decided). They are carried here verbatim in substance, so no intent is lost when those files became the agent orientation and working agreement. **Step 1.3 merges this with the Matter Library architecture spec brought home from the platform docs** (the component map, the spec tree and the identity spine), then annotates it against the lead's rulings of 2026-09-23 (`docs/Planning/Research/260923_R_StandaloneSetup.md` §Resolved).

## Decided architecture (carried from `.ai/context.md`, 2026-07-14 refresh)

- **MaterialX = single source of truth.** ASWF MaterialX 1.39+.
- **Two-tier library:** a volatile **source collection** (community-contributable, under the matter taxonomy) → a curated **versioned library**.
- **A release is a manifest, not a copy.** `library/releases/matterlib-X.Y.Z.lock.yaml` pins the exact `vNN` of each included material and texture set; each release is a git tag. *(Drift, 2026-09-23: no git tags exist yet. Tags are created as needed per R8.)*
- **Two version axes:** per-material/texture `vNN` (contributor-driven) vs library release semver (maintainer-driven).
- **Promotion model A:** manifest + tags in one repo. The CODEOWNERS-gated manifest is the control point, upgradeable to a separate library repo later without re-architecting. *(Drift, 2026-09-23: no CODEOWNERS file exists yet.)*
- **Textures via Git LFS** (large, lower-churn; many materials share one texture set).
- **LCD parity** across MaterialX / Unreal / Blender; master materials bridge the gap.
- **UE cook project in-repo at `bridges/unreal/`.** *(Reevaluate, 2026-09-23: per R14 this repo ships the release bundle + master contract as data. A reference UE masters package is the "B later" option; no `bridges/` folder exists.)*
- **Target versions:** Unreal **5.8+ with Substrate** (R15); Blender **5.1+** (R6). *(Was "Blender 4.x" before 2026-09-23.)*

## Design principles (carried from `.ai/conventions.md`)

### MaterialX-first
- `.mtlx` is the single source of truth. Blender/Unreal targets are **derived**, never hand-authored as the master.
- Conform to ASWF MaterialX 1.39+. IMRSV metadata is carried via the `imrsv_metadata` nodedef (master material, scale tag, meters-per-tile, domain, class).

### Least Common Denominator (LCD)
- Expose only parameters that every target (MaterialX / Unreal Substrate / Blender Principled BSDF) can honour. If one target can do something the others can't, don't rely on it.
- Master materials are where per-target gaps are bridged so the visible result stays close (target ΔE < 2 under standardised lighting).

### Two-tier library (source vs versioned)
- The **source collection** is volatile and community-contributable under the matter taxonomy.
- The **versioned library** is curated. A release = `library/releases/matterlib-X.Y.Z.lock.yaml` (a manifest pinning the exact `vNN` of each material and texture set) plus a git tag.
- **Promotion** edits the manifest; it does not copy files. Carry-forward = the next manifest keeps the same pins for unchanged materials.

### Versioning
- **Two axes:** per-material/texture `vNN` (contributor) vs library release semver (maintainer). Don't conflate them.
- **Library semver:** MAJOR = breaking (an LCD/master-material parameter change, a change in what a scale tag means, a material retired); MINOR = additive; PATCH = drop-in visual fix.
- **Status lifecycle:** draft → candidate → approved → deprecated → retired.

### Immutability after promotion
- Once `material@vNN` (or `texture@vNN`) ships in any released manifest, that file is frozen.
- A change is **always** a new `vNN+1`, never an in-place edit. This keeps old releases reproducible and back-compat real.

### Textures
- Tracked with **Git LFS**. Stored once under `textures/base` (matter hierarchy) + `textures/shared` (overlays, masks), and referenced by many materials.

### Governance
- Source PRs are open but **CI-gated**: schema valid, naming/taxonomy valid, scale tag present, referenced textures exist, eventually an automated parity render.
- The release manifests under `library/releases/` are **CODEOWNERS-gated**; only maintainers promote.

*Naming rules (filename grammar, scale tags, Domain/Class in the folder path) moved to `docs/NamingConventions.md`. The "Don't Delete Spec Functionality" rule moved to `.ai/AI_WorkingAgreement.md` §Project practices. The decision record is `docs/Planning/Research/260530_R_LibraryArchitecture.md`.*
