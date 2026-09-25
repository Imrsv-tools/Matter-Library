# PhaseTBD — Version Management (the next release carries the last one forward)

**Status:** TBD — not numbered. Trimmed 2026-09-23 (Phase01 step 1.5) to what is still open. The original draft (2026-05-30) is kept below, with each part marked as delivered, moved or open. Nothing is deleted.

## Outcome

**A maintainer can cut the next library release from the previous one — keeping unchanged articles pinned, adding new ones, deprecating and retiring old ones — and every earlier release stays reproducible exactly as it was.**

## Why this is still a phase

The release machinery exists and has cut one pilot (`matterlib-0.1.0`). What has **never happened** is a **second** release built from a first. That is the moment every versioning rule is actually exercised: carry-forward, `deprecated`/`retired`, immutability after promotion, and semver bumps. It is one thing a person can do, and it is demonstrable.

## Scope (to settle at discovery)

- A second release manifest derived from `matterlib-0.1.0`, exercising carry-forward and at least one `deprecated` or `retired` entry.
- Immutability after promotion enforced by a gate (a changed file under a shipped `vNN` is rejected), not just stated.
- The semver bump rule applied and checked.
- **Open question:** does immutability bind in `0.x`, or only from `1.0`, given that `0.1.0` is a pilot (lead R7/R8)? *(Also a `Reevaluate` in `docs/specs/Contract/Manifest.md`.)*
  - **Precedent (2026-09-24, Matter-Library#1):** asked whether a roughness clamp should ship as new `_v02` articles in a new release or as an in-place edit of the approved `v01`, the lead answered *"Fix forward only... we have no legacy projects yet"*. The 10 affected `v01` articles were regenerated in place and `matterlib-0.1.0` was re-frozen and re-approved (`4ed38dc`, `4172c74`). That is a ruling for this case while no consumer holds a release, not yet the general rule this question asks for; this phase states the general rule.

## The original draft (2026-05-30), marked

### Manifest / release schema
- Fields: `release` (semver), `materials[]` (`id`, `version`, `status`), `textures[]` (`id`, `version`), optional `notes`. — **Delivered** (pre-standalone, 2026-06/07): `library/releases/*.lock.yaml`, spec [`Manifest`](../../../specs/Contract/Manifest.md). Provenance and `creator_selectable` were added since.
- `id` form: taxonomy-relative path (Domain/Class from the folder, not the filename). — **Delivered.**
- A release is a **manifest + git tag**, not a file copy. — Manifest **delivered**; **git tags: open**, moved to the release-bundle phase (publishing).
- The example must express **carry-forward** (unchanged pins persist) and a **deprecated** back-compat entry alongside an `approved` newer one. — **Open: this is this phase's Outcome.**

### Versioning rules
- **Two axes:** per-material/texture `vNN` vs library release semver. — **Delivered** (in use in both pilot manifests).
- **Library semver** (MAJOR breaking / MINOR additive / PATCH visual fix). — Specified; **first exercised by this phase.**
- **Immutability after promotion.** — The freeze hash-locks a release (**delivered**). **A gate rejecting in-place edits: open (this phase).**

### Status lifecycle
- `draft → candidate → approved → deprecated → retired` (never deleted from history). — `draft` and `approved` are exercised (`0.0.1`, `0.1.0`). **`candidate`, `deprecated`, `retired`: open (this phase).**
- Which statuses are valid inside a release manifest. — **Delivered** (the manifest validator).

### Governance
- Source PRs open but **CI-gated** → `candidate`. — **Moved** to the contribution-path phase (since Phase02, 2026-09-23, the structural gate is one command, run by hand; automatic PR CI is parked by the lead, and a dormant workflow is kept for the contribution path to decide on).
- `library/releases/` **CODEOWNERS-gated**, so only maintainers promote. — **Moved** to the contribution-path phase. The approval artifact (`promote_release.py --approver`) exists today (**delivered**).
- The manifest file set is the single control point. — **Delivered.**

### First curated release
- ~~Author the first real manifest, tag `matterlib-1.0`, validate end-to-end consumption by the platform.~~ — **Partly delivered, re-shaped:** the first real manifest and approval exist as the **pilot** `matterlib-0.1.0`, and consumption by IMRSV ran on it. **The first release for users**, and its version number, is a lead decision owned by the release-bundle phase (lead, 2026-09-23: "Create whatever version we need; we are unreleased").

## Dependencies / related

- The release lifecycle as built: [`docs/specs/Distribution/ReleaseModel.md`](../../../specs/Distribution/ReleaseModel.md).
- Decision record: [`docs/Planning/Research/260530_R_LibraryArchitecture.md`](../../Research/260530_R_LibraryArchitecture.md).
- Originally drafted as Steps 1.4–1.5 of the pre-standalone Phase 01; moved here 2026-05-30 so version management landed last. Kept intact per Don't Delete Spec Functionality.
