# Phase 01 — Foundations: Folder Structure, Taxonomy & Naming

**Status:** PLANNING — contract-layer only. No master materials, textures, transformers, or
manifest tooling this phase.

## Goal

Lay out the full folder structure and taxonomy and lock the durable, hard-to-change-later
contracts everything downstream depends on:

1. The **folder structure** (full target tree, exists vs planned).
2. The **taxonomy** (Domain / Class; a future Realm noted but deferred).
3. The **filename grammar** and its default tokens.
4. The **portable `.mtlx` metadata contract** — identity + scale in the file; version + status
   deferred to the manifest (Version Management phase).

These are contracts. Locking them now avoids mass renames / re-tagging later (immutability
after promotion makes churn expensive once content accumulates). Crucially, the
**portable-`.mtlx` decision means adding versioning/manifests later won't require editing any
material file.**

## Why first

Master materials, transformers, the cook project, and Studio consumption all reference the
taxonomy, the filename grammar, and the metadata block. Lock the contract before building on it.

## Scope — Steps

### Step 1.1 — Lay out folder structure + taxonomy
- Finalize the full target tree (`FolderStructure.txt`) with **(exists)/(planned)** tags.
- Ratify the 5 Domains and the seeded Classes (19 today). Add any Class missing for near-term
  content; don't prune (open taxonomy).
- Note the **Realm** super-level as explicitly deferred (only if a non-matter compound library
  lands). No folders/code for it yet.
- **Done when:** the Domain/Class list in `Readme.md`, `FolderStructure.txt`, and the seeded
  folders agree.

### Step 1.2 — Lock the filename grammar
- Ratify `Material_Variant_Condition_Detail_sNN_vNN.mtlx`; confirm `Clean`/`Base` defaults.
- Confirm the 4 seeded samples conform (`Glass_Clear_Clean_Base_s01_v01`, etc.).
- Write a short grammar reference (allowed characters, token order, scale tags, version
  padding). Domain/Class are folder-only (not in the filename).
- **Done when:** grammar is documented and all on-disk samples validate against it by hand.

### Step 1.3 — Lock the portable `.mtlx` metadata contract
- Confirm the `imrsv_metadata` nodedef fields against the seeded samples:
  `master_material`, `scale_tag`, `meters_per_tile`, `domain`, `class`.
- **Decision (2026-05-30): keep the `.mtlx` portable.** Material identity + scale live in the
  `.mtlx`. **Version pins and promotion status do NOT live in the `.mtlx`** — they live in the
  manifest (Version Management phase). The on-disk `vNN` in the *filename* is the material's own
  version; the manifest decides which `vNN` a release includes.
- Document the metadata schema; note any sample migration needed.
- **Done when:** the metadata schema is documented and the samples conform (or have a noted
  migration), with the portable-`.mtlx` rule recorded.

## Out of scope (moved to later phases)

- Material catalog / gut-check chart → `PhaseTBD_MaterialCatalog`.
- LCD parameter set + master materials → `PhaseTBD_FiveMaterialsNoTextures`.
- Textures / LFS → `PhaseTBD_FiveMaterialsTextured`.
- Overlays/masksets → `PhaseTBD_Overlays`.
- UE cook project → `PhaseTBD_CookUnrealLibrary`.
- **Manifest / release schema, semver, governance, validators/CI** →
  `.ai/phases/future/PhaseTBD_VersionManagement.md`.

## Acceptance

- `Readme.md`, `FolderStructure.txt`, and seeded content agree on folder structure, taxonomy,
  and filename grammar.
- The portable `.mtlx` metadata schema is documented with the seeded samples conforming.
- Aspirational items remain, tagged `(planned)` (Don't Delete Spec Functionality).

## Notes

- Doc/spec-heavy by design — the contract layer for a research-phase repo.
- Decision record: `.ai/research/Library_Architecture_Research.md`.
