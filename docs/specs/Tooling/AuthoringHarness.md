# Authoring Harness — stage-C assembler + QC validators

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

The **deterministic authoring harness** that turns a material spec (a [recipe](../../Glossary.md)) into a contract-valid Matter
`.mtlx`, plus the **QC / validation gate set** that proves conformance. It implements **stage C
(+ QC)** of the [Authoring Golden Path](../Authoring/AuthoringGoldenPath.md) — generator stages
A→B (generation + decomposition) remain *(planned)* as in-repo tooling; this spec covers what is built.

> This is a **harness-contract** spec — it names the harness shape and the contract it upholds,
> and **points at the implementation**; it does **not** restate the A→B→C pipeline (see Authoring
> Golden Path) or copy the assembler/validator logic (that lives in `tools/`, below).

## Home — this repo's `tools/`

The harness is **payload-adjacent**, not consumer application code (matches the "no shader-graph
authoring in the consumer application" [Experience](../Experience/Experience_MatterLibrary.md) boundary). It lives in this repo's `tools/`.

## Tools

*(Updated 2026-09-23, measured: `ls tools/*/` on the live tree and each script's module docstring; the `run_all.py` lanes are the `results` keys of its `main()`.)*

### `tools/converters/` — stage C (assembly) and procedural textures

| Path | Role |
|---|---|
| `assemble_mtlx.py` | the **[Assembler](../../Glossary.md)** — a `MaterialSpec` → OpenPBR 1.39 single-file `.mtlx` (MaterialX Python SDK), deterministic |
| `build_proof_subset.py` | driver: assembles every recipe in `recipes/` to its `.mtlx` under `MatterLibrary/materials/` |
| `recipes/*.json` | the **reproducible per-article inputs** (one recipe per article), authored against `recipe.schema.json` |
| `recipe.schema.json` | the recipe contract (JSON Schema): every allowed key, its type and enums (Phase03) |
| `lookup_physically_based.py` | grounds recipe constants in the CC0 Physically Based database and prints the recipe's `sources` record (Phase03) |
| `import_ambientcg.py` | imports one ambientCG (CC0) material as a base texture set, with its provenance record and CREDITS row (Phase03) |
| `tileable.py` | seamless noise, wrap-around normals and overlay/mask packing for procedural textures (Phase03) |
| `layers/gen_<layer>.py` | one generator per shared wear layer (`Fingerprints01`, `Scuffs01`, `EdgeWear01`, `Crevice01`) (Phase03) |
| `base/gen_<set>.py` | one generator per generated base texture set (`Earthenware_Natural`) (Phase03) |
| `gen_uvgrid.py` | deterministic procedural UV/grid diagnostic base-colour texture |
| `gen_article_textures.py` | deterministic procedural base textures for the example articles of the masters that had none (Lace, Marble, Rust …) |
| `gen_shared_textures.py` | deterministic procedural shared overlay / maskset **data** textures (not albedo) |
| `project_runtime_catalog.py` | the **[Projector](../Contract/RuntimeCatalog.md)** — validates a manifest and projects it to the runtime catalog JSON |

### `tools/validators/` — the structural gate

| Path | Role |
|---|---|
| `validate_material.py` | the **per-`.mtlx`** conformance checks (below) |
| `validate_manifest.py` | the **library-level** lockfile check, incl. the provenance gate |
| `check_determinism.py` | byte-stable re-assembly check (and optional regen-matches-committed) |
| `check_fixture_sync.py` | cross-repo check that a consumer's fixture copy of the runtime catalog + payloads is byte-current. **Not a `run_all.py` lane since 2026-09-23** (see below); a standalone tool, run with `--fixture-root` |
| `source_provenance.py` | computes the shipped-source-set sha256 used as `evidence.sha256` for third-party (ambientCG) textures; `release_textures()` names the texture files a release's lock covers |
| `validate_recipe.py` | the **recipe** guards: G1 unknown keys, G2 schema, G3 taxonomy, G5 path agreement, G6 physical plausibility, G7 layer assignment (Phase03) |
| `run_all.py` | orchestrator — the **[structural gate](../../Glossary.md)**; lanes listed below |
| `fixtures/grammar_cases.json` | identity-grammar regression fixture (must-pass / must-fail) |
| `fixtures/*.lock.yaml` | RED manifest fixtures (dangling id, missing provenance, under-promoted coverage, shallow evidence) |
| `fixtures/recipes/*.json` | RED recipe fixtures, each rejected by one named guard |

**`run_all.py` lanes** (in run order). Each reports **PASS**, **FAIL** or **SKIP** with the reason when its surface or tool is absent. A SKIP is never counted as a pass, and `--strict` (the full check a maintainer runs before merging) fails on any SKIP. Run it as `uv run tools/validators/run_all.py` ([ToolingConventions §Entry points](../../ToolingConventions.md)).

| Lane | Checks |
|---|---|
| `grammar` | identity-grammar fixtures (must-pass / must-fail) |
| `materials` | `validate_material.py` over every `MatterLibrary/materials/**.mtlx` |
| `manifest` | `validate_manifest.py` over the newest `library/releases/*.lock.yaml` |
| `determinism` | every recipe assembles byte-identically twice |
| `recipe` | `validate_recipe.py` over every recipe (G1–G3, G5–G7), and every RED recipe fixture rejected by its own guard (Phase03) |
| `catalog_freshness` | each committed `*.catalog.json` is byte-current with, and deterministic from, its lockfile |
| `catalog_validation` | the projector rejects a manifest with dangling ids |
| `provenance_gate` | promotion-metadata RED fixtures are rejected (missing provenance, under-promoted coverage, shallow evidence) |
| `no_projection_guard` | provenance / evidence / licence data never leaks into the runtime catalog |
| ~~`fixture_sync`~~ | *Removed from the gate 2026-09-23 (Phase02).* A consumer's fixture catalog + payloads are byte-current (cross-repo). The intent is kept: the check moves to the consumer side (`PlatformDependencies.md` P8), and `check_fixture_sync.py` remains as its tool. |
| `compression_negative` | the compressed-output validator rejects corrupt / mismatched `.dds` fixtures |
| `compression` | source textures compress to deterministic, valid BCn `.dds` (encoder-gated) |
| `staging` | the release-staging producer assembles a complete `{png, dds}` snapshot (encoder-gated) |
| `approval_gate` | approval artifacts are well-formed (positive + shallow-negative fixtures) |
| `freeze_lock` | the complete-payload hash-lock is deterministic + tamper-detecting |
| `approval_binds_freeze` | a promoted approval references the release's actual frozen hashes |
| `release_verify` | *(Since Phase03, a release's source textures are the ones its lock names, not every PNG on disk.)* Every **committed** freeze record (`library/releases/*.freeze.json`) still reproduces from the tree, naming any changed, missing or added file. A shipped file edited in place, or LFS pointer files in place of textures, fail here. The `.dds` set is included when the encoder or a staging tree is present. This is the hash mechanism only; the `vNN` immutability rule belongs to Version Management. |
| `activation` | `activate_release.py` verifies install-readiness and switches the selector atomically |

> **Drift (2026-09-23), narrowed by Phase02:** the **gate** no longer reads a consumer's checkout (`fixture_sync` left `run_all.py`). **Promotion still does:** `promote_release.py` runs `check_fixture_sync` against IMRSV Stage's fixture mirror as one of its preconditions — owned by the release-bundle / consumer-contract phase (R1; `PlatformDependencies.md` P8).

> **Done (Phase02, 2026-09-23):** `run_all.py` used to fail at import (no MaterialX Python module on the lead's box). It now runs from a fresh clone with `uv run tools/validators/run_all.py`, which builds the pinned environment from `pyproject.toml` + `uv.lock`. *(Measured: fresh clone → 16 lanes, 14 PASS / 2 SKIP without the encoder; `--strict` with the pinned encoder → 16 PASS.)*

### `tools/releases/` — the release lifecycle ([ReleaseModel](../Distribution/ReleaseModel.md))

| Path | Role |
|---|---|
| `stage_release.py` | `build` / `verify` the per-release `{png, .dds}` staging tree under `library/staging/` |
| `freeze_release.py` | `compute` / `verify` the complete-payload hash-lock (`*.freeze.json`) |
| `promote_release.py` | the sole promotion flip — creates `*.approval.json` referencing the frozen hashes |
| `validate_approval.py` | checks an approval artifact's shape (never creates one) |
| `activate_release.py` | offline `activate` / `resolve-check` / `recover-unapproved` — writes the active-release selector atomically |
| `fixtures/approval_{valid,shallow}.approval.json` | positive / shallow-negative approval fixtures |

### `tools/compressors/` — BCn ([CompressedDistribution](CompressedDistribution.md))

| Path | Role |
|---|---|
| `compress_textures.py` | source PNG tree → deterministic, mip-complete BCn `.dds` by texture role, with output validation |
| `fixtures/make_negative_fixtures.py` (+ `*.dds`) | regenerates the deliberately corrupt `.dds` fixtures the `compression_negative` lane must reject |

### `tools/conformance/` — Creator-asset profile, Blender exporter, parity

| Path | Role |
|---|---|
| `assert_profile.py` | asserts a USD asset conforms to the [Creator Asset Profile](../Contract/CreatorAssetProfile.md) (lightweight / portable), pxr-free |
| `build_portable.py` | materialises the complete-portable golden from the lightweight golden + the library |
| `export_copper_slice.py` | drives the real `imrsv_lcd_export` add-on on a two-mesh Copper scene (Blender half of the producer harness) |
| `export_library_slice.py` | exports a slice built from the generated Asset-Browser library material |
| `test_export_selection.py` | regression: per-mesh material-instance split survives the File-browser selection collapse |
| `verify_asset_library.py` | headless structure verifier for the generated Blender Asset-Browser library |
| `render_leg_probe.py` | probe: does an article sample each carried LCD appearance scalar in Storm |
| `codec_ab.py` | [Codec A/B](CompressedDistribution.md) — ΔE2000 / SSIM of source PNG vs release BCn through one pinned Storm pipeline |
| `build_ocio_parity_config.py` | builds and validates the OCIO 2.4-native [parity config](CompressedDistribution.md) |
| `check_conformance.sh` | Creator Asset Profile conformance gate |
| `check_exporter.sh` | real-exporter conformance gate |
| `check_asset_library.sh` | Asset-Browser library generate + structure gate |
| `golden/creator_table_lightweight.usda` · `fixtures/foreign_material_prop.usda` | the committed [golden](../../Glossary.md) + a negative fixture |

### `tools/generators/` — Blender Asset-Browser library

| Path | Role |
|---|---|
| `gen_asset_library.py` | generates `blender/asset_library/MatterLibrary.blend` for every `creator_selectable` article |
| `matter_proxy.py` | the one generic recipe → Principled-BSDF `MatterLCD_<id>` proxy mapper |

### `tools/preview_generators/` — usdview parity preview

| Path | Role |
|---|---|
| `make_preview.py` | writes a standalone preview scene (UV sphere, dome + key light, camera, article bound); `--render` renders it headless with `usdrecord`; `--set` moves a Creator slider through the carrier rule (Phase03) |
| `preview_wrapper.usda` | the preview template |
| `README.md` | usage, the three render fixes, and the toolchain it needs |

### `tools/usd-toolchain/` — [USD Validation Toolchain](USDValidationToolchain.md)

| Path | Role |
|---|---|
| `environment.yml` | conda host env for building + hosting OpenUSD 26.03 / MaterialX 1.39.5 |
| `build-usd-tools.sh` | clones and builds OpenUSD with dev tools on, pins MaterialX, applies the GLSL render fix |
| `run-all.sh` | one-shot: create the env, then build |
| `activate-usd-tools.sh` | puts the built tools on PATH / PYTHONPATH (+ the Linux GL platform fix) |
| `README.md` | recipe usage |

## The contract the harness upholds

- **Deterministic + reproducible** — identical inputs produce a **byte-identical** `.mtlx`
  (fixed element order, no `datetime`/RNG); **no network at assembly time**
  (MaterialX-first, [_Architecture](../_Architecture.md)).
- **Conformance is asserted, not assumed** — a document can pass `doc.validate()` while burying
  the LCD as constants or being multi-file, so the **`validate_material` checks are the
  conformance gate**, not `doc.validate()` alone:
  SDK-validate (stdlib loaded) · single-file (no includes / external `.mtlx`) · OpenPBR-only
  (exactly one `open_pbr_surface`, zero `standard_surface`) · **LCD-as-interface-inputs** (each
  exposed Creator control is a wired nodegraph interface input from the
  [frozen LCD vocabulary](../Contract/LCDSchema.md), not a buried constant) · identity grammar
  (name == file stem, ≤63 / `[A-Za-z0-9_]` / token shape, [Identity](../Ontology/Identity.md)) ·
  texture-path locality (every `<image>` path relative + resolves on disk).
- **Output conforms to the contract specs** — [MaterialXTemplate](../Contract/MaterialXTemplate.md)
  (single-file `open_pbr_surface` 1.39 anatomy) · [LCDSchema](../Contract/LCDSchema.md) (the
  Creator-adjustable subset as interface inputs) · [MasterSet](../Ontology/MasterSet.md) (the
  master token rides the optional `imrsv_metadata` nodedef, never a USD `imrsv:` attr).
- **Manifest well-formed** — `validate_manifest` checks a release lockfile parses, uses release
  **semver** + per-material **`vNN`** (the two version axes never conflated), a lifecycle `status`, and
  each `id` resolves to an on-disk `.mtlx` ([Manifest](../Contract/Manifest.md)).

## Manual QC gates (mandatory-human)

Automated conformance proves the material *matches the contract*; the **author's visual QC**
proves the *pixels are right* — de-light (albedo carries no baked lighting), tileability
(2×2 / 3×3, no seam), and **informal usdview parity** (render vs intent — *not* the formal ΔE
bar, which is [CompressedDistribution](CompressedDistribution.md) §Parity). The faithful usdview/usdrecord that backs this gate is the
[USD Validation Toolchain](USDValidationToolchain.md) (from-source OpenUSD 26.03 + MaterialX 1.39.5).
Where usdview / the `pxr` Python module is unavailable, the parity gate
**degrades** to SDK-validate + structural review with an explicit **`parity-not-evaluated`** note
(an honest non-claim that keeps the manifest `draft` status honest) — see
`tools/preview_generators/README.md`.

*Shipped (Phase03, 2026-09-25):* the preview renders real articles headless (`usdrecord`), and a maintainer reviews drafts in USDLiveView. **Limits recorded, not fixed:** the preview renderer (Storm) shows no transmission colour and renders `transmission = 1.0` black, and light intensity barely changes its output (owned by *Parity Baselines*).

## Status

**Authoring harness + QC gate set stood up** and proven by authoring the range-covering
proof subset through it. The **production tool-stack** (Matter Manager, a generator for stages A→B whose output satisfies the shipped-pixel rule, automated de-light/tileability/parity as CI gates) remains *(planned)*
(`tools/` continues to grow). No wire/ABI contract frozen here.

*Shipped (Phase03, 2026-09-25):* a first cut of stages A→B inside this repo, driven by the `/matter-generate` skill: constants from Physically Based (L1), ambientCG scans (L3), generated base textures and wear layers (L2), each with provenance. The Matter Manager and CI gates are still *(planned)*.

## History

- 2026-06: the harness (assembler, per-material and manifest validators, determinism check, `run_all.py`) was stood up inside the IMRSV platform and used to author the proof subset.
- 2026-07: the gate grew lanes for the runtime catalog, provenance, compression, staging, freeze, approval and activation, plus the conformance and Blender-generator tools.
- 2026-09-23: brought home; tool list refreshed against the live tree.
- 2026-09-25 (Phase03): the recipe lane (17 lanes), the recipe schema, the Physically Based lookup, the ambientCG importer, layer and base-set generators, the working headless preview; freeze and staging scoped to each release's lock.
