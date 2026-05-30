# PhaseTBD — Version Management (Manifest / Releases / Promotion)

**Status:** FUTURE — not sequenced. The last chunk in the rough working order. Detail captured
now so the design (drafted 2026-05-30) isn't lost; refine when it becomes active.

## Goal

Build the source→approved→release machinery that turns the volatile source collection into a
controlled, versioned, consumable library. By this point the taxonomy, naming, portable `.mtlx`
metadata, ~10 materials (with textures + overlays), the cook project, and Studio consumption
all exist — this phase makes the library **curatable and versioned**.

## Scope (draft)

### Manifest / release schema (`library/releases/matterlib-X.Y.lock.yaml`)
- Fields: `release` (semver), `materials[]` (`id`, `version`, `status`), `textures[]`
  (`id`, `version`), optional `notes`.
- `id` form: taxonomy-relative path (Domain/Class from the folder, not the filename).
- A release is a **manifest + git tag**, not a file copy.
- Example must express **carry-forward** (unchanged pins persist) and a **deprecated**
  back-compat entry alongside an `approved` newer one.

### Versioning rules
- **Two axes:** per-material/texture `vNN` (contributor) vs library release semver (maintainer).
- **Library semver:** MAJOR = breaking (LCD/master-material param change, scale-meaning change,
  a material retired); MINOR = additive; PATCH = drop-in visual fix.
- **Immutability after promotion:** a promoted `vNN` file is frozen; changes are new `vNN+1`.

### Status lifecycle
- `draft → candidate → approved → deprecated → retired` (never deleted from history).
- Which statuses are valid inside a release manifest.

### Governance
- Source PRs open but **CI-gated** (schema / naming / scale / reference / parity render) →
  `candidate`.
- `library/releases/*.lock` **CODEOWNERS-gated** → only maintainers promote to `approved`.
- The manifest file set is the single control point.

### First curated release
- Author the first real manifest, tag `matterlib-1.0`, validate end-to-end consumption by the
  platform.

## Dependencies / related

- Validators / CI and Matter Manager tooling (parking lot) implement the gates referenced here.
- Decision record: `.ai/research/Library_Architecture_Research.md`.
- Originally drafted as Steps 1.4–1.5 of Phase 01; moved here so version management lands last
  (per working-order decision 2026-05-30), kept intact per Don't Delete Spec Functionality.
