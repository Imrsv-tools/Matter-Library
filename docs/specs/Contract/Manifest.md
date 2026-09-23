# Manifest — the library lockfile

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

A **library release is a manifest (lockfile), not a copy.** The manifest pins the exact version of each included material and texture set; the files are payload behind it. The manifest is the **authored source of truth** for the runtime catalog: the [projector](../../Glossary.md) validates it and projects it to the [runtime catalog](RuntimeCatalog.md) JSON that consumers read (names, versions, taxonomy, scale, status) — no consumer scans the filesystem.

> **Contract.** The authored YAML below is projected to the [RuntimeCatalog.md](RuntimeCatalog.md) JSON that consumers read. Ownership: the Matter Library authors YAML, the projector validates + projects, consumers read JSON only.

## Lockfile schema

```yaml
# library/releases/matterlib-1.3.0.lock.yaml   (illustrative release)
release: 1.3.0

materials:
  - id: engineered/glass/Glass_Clear_Clean_Base_s01
    version: v01
    status: approved
  - id: natural/stone/Limestone_Veined_Clean_Base_s01
    version: v02
    status: approved
  - id: natural/stone/Limestone_Veined_Clean_Base_s01
    version: v01
    status: deprecated              # kept for back-compat
  - id: utility/virtual/IMRSV_MissingMaterial   # system material, off-grammar (bare-id resolve)
    version: v01
    status: approved
    creator_selectable: false       # excluded from Creator browse/assign; still resolvable by identity

textures:
  - id: base/natural/stone/Limestone_Veined
    version: v01
    status: approved
    provenance:
      source: ambientCG
      license: CC0-1.0
      evidence:
        url: https://ambientcg.com/view?id=Travertine009
        sha256_scope: shipped_source_set
        sha256: <64-hex digest of the shipped source set>
        files:
          - path: MatterLibrary/textures/base/natural/stone/Limestone_Veined_basecolor_s01.png
            sha256: <64-hex>
  - id: shared/overlays/Dust01
    version: v01
    status: approved
    provenance:
      source: procedural
      license: CC0-1.0
      evidence: tools/converters/gen_shared_textures.py
```

*(Updated 2026-09-23, measured: the former example was a one-line-per-entry block that was not valid YAML; the block above follows the live `library/releases/matterlib-0.1.0.lock.yaml` shape — top-level `release` / `materials[]` / `textures[]`, multi-line entries, optional `creator_selectable` on a material, and `provenance` on each texture with a dict `evidence` for ambientCG sources and a generator-script path for procedural ones.)*

The `id` is the Domain/Class folder path + the [qualified Matter name](../Ontology/Identity.md) **including the `sNN` scale tag** (Domain/Class are folder-only, so they appear in the path, not the name). Carrying `sNN` in `id` is what makes `id` + `version` resolve to a file — `<id>_<version>.mtlx`. `version` pins the material's own `vNN` axis; `release` is the library semver axis — the **[two version axes](../../Glossary.md)** never conflate ([Identity](../Ontology/Identity.md)).

### Off-grammar exception — `IMRSV_MissingMaterial`

The system material `utility/virtual/IMRSV_MissingMaterial` is **off-grammar**: it has no `sNN` scale tag and its filename has no `_vNN` axis, so it resolves by **bare `<id>.mtlx`** (not `<id>_<version>.mtlx`). It still carries a nominal `version: v01` in the lockfile for schema uniformity. The projector emits an empty `scale` and a `payload_path` without the `_<version>` suffix for it ([RuntimeCatalog.md](RuntimeCatalog.md)). It is also the one material carrying `creator_selectable: false`. The historical name is kept.

### `provenance` — an authoring + VALIDATOR artifact

A `provenance` field (authoring lineage) records each texture's origin. **It is an authoring + validator artifact — NOT runtime-projected.** `tools/validators/validate_manifest.py` is a provenance consumer: its `_validate_provenance` gate requires an `approved`-rank ambientCG texture to carry `evidence:{url, sha256}` (the shipped-source-set digest, `tools/validators/source_provenance.py`, `sha256_scope: shipped_source_set`), and a shallow (doc-path-only) evidence block on a promoted texture is REJECTED (RED fixture `tools/validators/fixtures/approved_rank_shallow_evidence.lock.yaml`). Provenance/license/evidence remain **absent from the runtime catalog** — the `no_projection_guard` lane of `tools/validators/run_all.py` asserts none of those tokens ever reach the projected JSON (they are control-boundary/authoring metadata, resolution-blind). *(Updated 2026-09-23, measured: `_validate_provenance`, `source_provenance.py`, the RED fixture and `run_no_projection_guard` all exist at those paths.)*

Every recorded `license` must be CC0-dedicable, because the shipped content is CC0-1.0 ([shipped-pixel rule](../Authoring/AuthoringGoldenPath.md), R13). *(Updated 2026-09-23, measured: every texture in `matterlib-0.1.0.lock.yaml` records `license: CC0-1.0`, source `ambientCG` or `procedural`.)*

**What the manifest gives for free:**
- **Carry-forward** — release 1.4's manifest = 1.3's + new lines; unchanged materials keep their same `vNN` pin (no copying, no churn).
- **Back-compat** — list both an `approved` newer version and a `deprecated` older one; old release **tags** stay consumable forever.
- **Growth** — append-mostly; rarely remove, mark `deprecated`/`retired`.

> **Drift (2026-09-23):** no git tags exist in this repo yet (measured: `git tag` is empty); tags are created as needed while everything is unreleased — owned by the release-bundle / consumer-contract phase (R8).

## Status lifecycle (per material/texture version)

```
draft        in source, not validated
  → candidate    passed CI (schema / naming / scale / parity checks)
  → approved     named in a release manifest
  → deprecated   superseded but kept for back-compat
  → retired      dropped from new manifests — never deleted from history
```

## Two safety rules

1. **Immutability after promotion.** Once `material@vNN` ships in any released manifest, that file is **frozen** — a change is *always* a new `vNN+1`, never an in-place edit. This is what makes old releases reproducible.
2. **Library release semver.** **MAJOR**: breaking (LCD/master-material param change, scale-meaning change, a material retired). **MINOR**: additive (new materials/textures). **PATCH**: drop-in visual fix.

> **Reevaluate (2026-09-23):** the repo is not in production (R7) and `matterlib-0.1.0` is a [pilot release](../../Glossary.md); whether immutability-after-promotion binds from 0.x or only from 1.0 is an open versioning question owned by the release-model work.

> **Release qualification, approval, activation & rollback:** the manifest is the *authoring* record; a release is **qualified → frozen (complete-payload hash-lock) → promoted (an external `*.approval.json` control-boundary artifact, the sole promotion flip) → activated (a deployed `active-release.json` selector) → rolled back / recovered (a selector re-point, no rebuild)**. Promotion to `approved` is enforced at the control boundary, NOT by mutating this manifest after the freeze — the approved release stays byte-identical to the qualified candidate. Full model: [Distribution/ReleaseModel.md](../Distribution/ReleaseModel.md).

## Composition release pin — `imrsv:matterlibRelease`

A composition records the **one exact library release** its recognized Matter materials resolve from, in the root-layer `customLayerData` key `imrsv:matterlibRelease` (e.g. `matterlib-0.1.0`). This is **package-dependency information** — the release axis carried alongside the composition so a cross-release resolve can be detected — **not an alternate material identity.** The **exact qualified material name stays the identity** ([Identity](../Ontology/Identity.md)); the pin never substitutes for or re-keys it. The key is written by conforming producers ([CreatorAssetProfile](CreatorAssetProfile.md) rule 7). The historical IMRSV-branded name is kept (R16).

> **Reevaluate (2026-09-23):** an `imrsv:`-prefixed key sits in tension with the spec's own "no `imrsv:` USD attributes" principle ([MaterialXTemplate](MaterialXTemplate.md) hard rule 4) — owned by the contract phase.

*Consumer-side (IMRSV): how the release pin is established and enforced in a composition (first-Add establishment, per-Add re-compare, `ReleaseConflict` on mismatch) — see [Consumers](../Consumers.md).*

## Governance — volatile community, controlled library

- **Contribution is open but CI-gated.** Community PRs add materials to the source taxonomy; automated checks (MaterialX schema valid, naming/taxonomy valid, scale tag present, referenced textures exist, conforms-to-a-Matter-template, eventual parity render) move a material to `candidate`.
- **Promotion is controlled via CODEOWNERS.** Only [maintainers](../../Glossary.md) edit `library/releases/*.lock.yaml`. That single file set is the control point — anyone can flood the source; only maintainers define a release.

> **Drift (2026-09-23):** no `CODEOWNERS` file exists yet (measured: none at the repo root or under `.github/`), so the promotion gate is currently convention, not enforcement — owned by the release-bundle / consumer-contract phase (R8).

## Status

**Schema + lifecycle — contract.** The manifest *shape* is the authored source of truth; the [runtime catalog](RuntimeCatalog.md) it projects to is the catalog consumers read, kept byte-current by the catalog-freshness lane of `tools/validators/run_all.py`. **No wire/ABI contract is frozen by this** — the data-versioning schemes here (material `vNN`, release semver, status lifecycle) and the runtime-catalog JSON (its own `schema_version`) are additive JSON.

## History

- Pre-standalone (2026-06 → 2026-07): the two-tier library and "a release is a manifest, not a copy" were first written in this repo's own Readme, then specced on the platform side.
- Pre-standalone: consumers switched from scanning the materials directory to reading the projected runtime catalog in one hard cutover, which is why the manifest → projector → catalog chain is the only read path.
- Pre-standalone: `provenance` was first judged "no consumer, out for v1", then reversed when the manifest validator started gating approved textures on their evidence digest.
- 2026-07-17: the composition release pin and the `creator_selectable` flag shipped together.
