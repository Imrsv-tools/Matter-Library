# Library Architecture — Decision Record

Captures the source→approved→release model and the decisions made 2026-05-30. This is the
"why" behind `.ai/conventions.md` and Phase 01.

## Problem

A **rolling** material library that mostly grows: some materials stay `v01` forever but must
carry forward to every future release; new materials/textures get added; existing ones get new
versions; older versions are sometimes kept for backwards compatibility. A **community** can
contribute to a volatile base library, but **we** must keep control of what enters our
**versioned** library.

## Core insight — two version axes

| Axis | Versions what | Example | Driven by |
|---|---|---|---|
| Material version | one asset | `Limestone_Veined_Clean_Base_s01_v02` | contributor |
| Library release version | the curated set | Matter Library 1.3 | maintainer |

Confirmed by user: each material has its own version; we pick which version of each material
goes into the versioned library.

## Decision — a release is a manifest, not a copy

`library/releases/matterlib-X.Y.lock.yaml` pins the exact `vNN` of each included material and
texture set. Consequences (all desired):
- **Carry-forward** is automatic: next manifest = prior + new lines; unchanged pins stay.
- **Back-compat**: list `approved` (new) and `deprecated` (old) side by side; old release tags
  stay consumable.
- **Growth**: manifest is append-mostly; rarely remove, mark `deprecated`/`retired`.

## Decision — promotion model A (one repo, manifest + tags)

Considered: (A) manifest + tags in one repo; (B) `/source` + `/library` folder copies;
(C) two repos; (D) volatile/protected branches.

**Chosen: A.** No file duplication; back-compat trivial; one history. Upgrades cleanly to (C)
later (a separate library repo consuming source by pinned SHA) if access-control volume
demands — without re-architecting. (B) duplicates huge textures; (D) can't cleanly express
"v1 and v2 both live."

## Decision — textures via Git LFS, in-repo

User: textures are **less volatile** than materials (many materials share one texture set),
so LFS in-repo is acceptable. Manifest pins texture-set versions too, so a release is fully
reproducible. The manifest can later point at content-addressed / DAM-hosted textures without
schema change (parking-lot item).

## Decision — governance

- Source PRs open but CI-gated (schema/naming/scale/reference/parity) → `candidate`.
- `library/releases/*.lock` CODEOWNERS-gated → only maintainers promote to `approved`.
- Single control point = the manifest file set.

## Rules that fall out

- **Immutability after promotion**: a promoted `vNN` file is frozen; changes are new `vNN+1`.
- **Library semver**: MAJOR breaking / MINOR additive / PATCH drop-in fix.
- **Status lifecycle**: draft → candidate → approved → deprecated → retired (never deleted
  from history).

## Other decisions (2026-05-30)

- **UE cook project** lives **in-repo** at `bridges/unreal/` (`MatterLibraryUE.uproject`).
- **Target versions**: Unreal **5.7+** forward target; Linux dev pinned to UE **5.6.1**
  (platform CLAUDE.md). Blender **4.x** (latest stable). Corrects the README's prior
  "Blender 5.1" (nonexistent) and mixed 5.6/5.7 statements.
- **Doc posture**: research/define — ADD/REFINE, never DELETE intended design to match disk.

## Resolved

- **Metadata location (2026-05-30): keep the `.mtlx` portable.** Material identity + scale live
  in the `.mtlx` (`imrsv_metadata`); **version pins + promotion status live in the manifest
  only**, never in the `.mtlx`. So adding versioning later requires no edits to material files.
- **Working order (2026-05-30):** version management (manifest/releases/promotion) lands
  **last**, not in Phase 01. Phase 01 narrows to folder structure + taxonomy + naming + the
  portable metadata contract. Manifest design preserved at
  `.ai/phases/future/PhaseTBD_VersionManagement.md`.

## Open questions

- Final taxonomy Class list — is 19 sufficient near-term, or are Classes missing?
  (Gut-checked by `PhaseTBD_MaterialCatalog`.)
- Texture-set naming/versioning grammar (`PhaseTBD_FiveMaterialsTextured`).
- LCD parameter set — proven by `PhaseTBD_FiveMaterialsNoTextures`.
