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
| `recipes/*.json` | the **reproducible per-article inputs** (one recipe per article; 12 files) |
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
| `check_fixture_sync.py` | cross-repo check that a consumer's fixture copy of the runtime catalog + payloads is byte-current (see Drift below) |
| `source_provenance.py` | computes the shipped-source-set sha256 used as `evidence.sha256` for third-party (ambientCG) textures |
| `run_all.py` | orchestrator — the **[structural gate](../../Glossary.md)**; lanes listed below |
| `fixtures/grammar_cases.json` | identity-grammar regression fixture (must-pass / must-fail) |
| `fixtures/*.lock.yaml` | RED manifest fixtures (dangling id, missing provenance, under-promoted coverage, shallow evidence) |

**`run_all.py` lanes** (in run order; each skips with a note when its surface is absent):

| Lane | Checks |
|---|---|
| `grammar` | identity-grammar fixtures (must-pass / must-fail) |
| `materials` | `validate_material.py` over every `MatterLibrary/materials/**.mtlx` |
| `manifest` | `validate_manifest.py` over the newest `library/releases/*.lock.yaml` |
| `determinism` | every recipe assembles byte-identically twice |
| `catalog_freshness` | each committed `*.catalog.json` is byte-current with, and deterministic from, its lockfile |
| `catalog_validation` | the projector rejects a manifest with dangling ids |
| `provenance_gate` | promotion-metadata RED fixtures are rejected (missing provenance, under-promoted coverage, shallow evidence) |
| `no_projection_guard` | provenance / evidence / licence data never leaks into the runtime catalog |
| `fixture_sync` | a consumer's fixture catalog + payloads are byte-current (cross-repo) |
| `compression_negative` | the compressed-output validator rejects corrupt / mismatched `.dds` fixtures |
| `compression` | source textures compress to deterministic, valid BCn `.dds` (encoder-gated) |
| `staging` | the release-staging producer assembles a complete `{png, dds}` snapshot (encoder-gated) |
| `approval_gate` | approval artifacts are well-formed (positive + shallow-negative fixtures) |
| `freeze_lock` | the complete-payload hash-lock is deterministic + tamper-detecting |
| `approval_binds_freeze` | a promoted approval references the release's actual frozen hashes |
| `activation` | `activate_release.py` verifies install-readiness and switches the selector atomically |

> **Drift (2026-09-23):** the `fixture_sync` lane (and promotion, via it) reads a consumer's (IMRSV Stage's) fixture mirror, so this repo's gate depends on a consumer checkout — owned by the release-bundle / consumer-contract phase (R1).

> **Todo (2026-09-23):** `run_all.py` fails at import on the lead's box as of 2026-09-23 — `validate_material.py` does `import MaterialX` and no MaterialX Python module is installed, so no lane runs — owned by the one-command-check phase. *(Measured: `python3 tools/validators/run_all.py` → `ModuleNotFoundError: No module named 'MaterialX'`.)*

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
| `make_preview.py` | emits a standalone preview `.usda` (sphere + dome light, article bound) and optionally opens usdview |
| `preview_wrapper.usda` | the preview template |
| `README.md` | usage + the `parity-not-evaluated` fallback |

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

## Status

**Authoring harness + QC gate set stood up** and proven by authoring the range-covering
proof subset through it. The **production tool-stack** (Matter Manager, a generator for stages A→B whose output satisfies the shipped-pixel rule, automated de-light/tileability/parity as CI gates) remains *(planned)*
(`tools/` continues to grow). No wire/ABI contract frozen here.

## History

- 2026-06: the harness (assembler, per-material and manifest validators, determinism check, `run_all.py`) was stood up inside the IMRSV platform and used to author the proof subset.
- 2026-07: the gate grew lanes for the runtime catalog, provenance, compression, staging, freeze, approval and activation, plus the conformance and Blender-generator tools.
- 2026-09-23: brought home; tool list refreshed against the live tree.
