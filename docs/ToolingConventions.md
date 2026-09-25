# Matter Library — Tooling Conventions

**Status: ACTIVE (arrived 2026-09-23, Phase01 step 1.5).** Its trigger, "the first real build", was met before adoption: the authoring harness, validators, release tooling and Blender add-on already exist. This doc takes over the artifact-taxonomy role of the retired `FolderStructure.txt` (archived verbatim at `docs/Planning/Phases/Complete/PreStandalone/FolderStructure.txt`). What each tool *does* is specified in [`docs/specs/Tooling/AuthoringHarness.md`](specs/Tooling/AuthoringHarness.md); this doc says **where things live and how they are named**.

## The artifact taxonomy

*Measured against the tree on 2026-09-23.*

| Root | What lives there | Licence |
|---|---|---|
| `MatterLibrary/materials/<domain>/<class>/` | the articles (`.mtlx`), **generated** from recipes, never hand-edited | CC0 |
| `MatterLibrary/textures/base/<domain>/<class>/` (flat: `<Set>_<channel>_<sNN>.png`) · `textures/shared/{overlays,masks}/` | textures (Git LFS; `.gitattributes`). *(Corrected 2026-09-25, Phase03: this row said a `<Set>/` subfolder; every shipped set sits flat in its class folder.)* | CC0 |
| `library/releases/` | per-release records: `matterlib-X.Y.Z.lock.yaml` (authored) · `.catalog.json` (projected) · `.freeze.json` · `.approval.json` | CC0 |
| `library/provenance/` | per-release texture provenance records · `sources/<texture-id>.yaml`: a texture set's provenance before any release pins it (Phase03, lead ruling Q2) | CC0 |
| `library/staging/` | the staged release tree (PNG + compressed DDS). **Gitignored, rebuildable** | — |
| `tools/converters/` | authoring: `assemble_mtlx.py` (the assembler), `build_proof_subset.py` (recipes → articles), `project_runtime_catalog.py` (lock → catalog), `gen_*.py` (procedural textures), `tileable.py` (seamless noise/normal/packing helpers), `layers/gen_<layer>.py` (one generator per shared wear layer), `base/gen_<set>.py` (one generator per generated base set), `import_ambientcg.py` (the ambientCG importer), `lookup_physically_based.py` (Physically Based grounding), `recipe.schema.json` (the recipe contract) | Apache-2.0 |
| `tools/converters/recipes/` | one JSON recipe per article, `<Stem>_vNN.json` | CC0 |
| `tools/validators/` | the structural gate `run_all.py` and its checks (`validate_material.py`, `validate_manifest.py`, `check_determinism.py`, `check_fixture_sync.py`, `source_provenance.py`, `validate_recipe.py`) + `fixtures/` (incl. `fixtures/recipes/`, the RED recipes) | Apache-2.0 |
| `tools/releases/` | the release lifecycle: `stage_release.py` → `freeze_release.py` → `promote_release.py` (+ `validate_approval.py`) → `activate_release.py` | Apache-2.0 |
| `tools/compressors/` | BCn compression (`compress_textures.py`) + negative fixtures | Apache-2.0 |
| `tools/conformance/` | Creator-asset and parity checks: `assert_profile.py`, `check_lcd_carrier.py` (+ `test_check_lcd_carrier.py`), the `check_*.sh` wrappers, `codec_ab.py`, `build_ocio_parity_config.py`, the Blender slice exporters, `golden/`, `fixtures/` | Apache-2.0 |
| `tools/generators/` | the Blender Asset-Browser library generator (`gen_asset_library.py`, `matter_proxy.py`) | Apache-2.0 |
| `tools/preview_generators/` | the preview scene for one article, rendered headless with `usdrecord` (`--render`); `--set` previews a moved Creator slider | Apache-2.0 |
| `tools/usd-toolchain/` | the pinned OpenUSD + MaterialX build recipe (`environment.yml`, `build-usd-tools.sh`, `run-all.sh`) | Apache-2.0 |
| `blender/addons/imrsv_lcd_export/` | the Matter exporter add-on + its `test_lcd_*.py` | Apache-2.0 |
| `blender/asset_library/` | the **generated** Asset-Browser library (`MatterLibrary.blend`, `blender_assets.cats.txt`) | CC0 |
| `blender/MatterMaterials.blend` | the scaffold scene the conformance slices export from | Apache-2.0 |
| `docs/` · `Methodology/` · `.ai/` · `.claude/` | specs, planning, method, agent surface | Apache-2.0 |
| `.claude/skills/matter-generate/` | the `/matter-generate` skill: a draft material from a brief (Phase03). A product surface, not methodology | Apache-2.0 |

## Naming

- **Python tools:** `snake_case.py`, verb-first where it is an action (`build_…`, `check_…`, `validate_…`, `gen_…`, `project_…`).
- **Shell wrappers:** `check_*.sh`, `*-usd-tools.sh`.
- **Fixtures:** under a sibling `fixtures/` folder; deliberately bad inputs are named for what they break.
- **Tests:** `test_*.py` beside the code they test (`blender/addons/imrsv_lcd_export/`, `tools/conformance/`). Test documentation lives in the docstrings; there is no separate test-docs tree. That is the observed practice as of 2026-09-23, not yet a ruling: the first phase that ships a real test suite decides it here.

## Entry points

| To… | Run |
|---|---|
| validate everything structural — **the one command** | `uv run tools/validators/run_all.py` (17 lanes, listed in [AuthoringHarness](specs/Tooling/AuthoringHarness.md)). From a fresh clone, uv builds `.venv/` from `pyproject.toml` + `uv.lock` (Python 3.12, MaterialX 1.39.5) first. Add `--strict` to fail on any skipped lane. Without uv: `python3.12 -m venv .venv && .venv/bin/pip install .`, then run the script with `.venv/bin/python`. |
| (re)generate articles from recipes | `python tools/converters/build_proof_subset.py [<recipe.json> …]` |
| re-project a catalog from its lockfile | `python tools/converters/project_runtime_catalog.py` |
| stage / freeze / promote / activate a release | the scripts in `tools/releases/` ([ReleaseModel](specs/Distribution/ReleaseModel.md)) |
| **serve the working tree to Stage and test it in USDLiveView** (pre-release; no versioning) | `uv run tools/releases/serve_to_stage.py [--view <composition>]` (`--off` to undo). Needs `IMRSV_STAGE_RUNTIME`. |
| build the USD validation toolchain | `tools/usd-toolchain/run-all.sh` ([USDValidationToolchain](specs/Tooling/USDValidationToolchain.md)) |

**Tool locations (environment variables, all optional):**
- `COMPRESSONATORCLI` — the pinned texture encoder, AMD `compressonatorcli` **V4.5.52** (default `~/.local/bin/compressonatorcli`). Without it the `compression` and `staging` lanes **SKIP** and say so, and `release_verify` checks everything except the `.dds` set.
- `USD_TOOLS_ROOT` — the USD toolchain root (default `~/usd-tools`; the install is `$USD_TOOLS_ROOT/inst/usd-26.03`).
- `USD_TOOLS_ENV` — the toolchain's conda env (default `~/.conda/envs/imrsv-usd-tools`).
- `MATTER_PREVIEW_DIR` — where `make_preview.py` writes preview scenes and renders (default `<tmp>/matter-preview/`; never the repo).

Every script finds the repo from its own location; none assumes a checkout path. *(Phase02, 2026-09-23. Before it, `run_all.py` failed at import for want of MaterialX, several tools hardcoded a retired checkout path, and there was no pinned environment and no CI.)*

## Gates and CI

- **The gate of record** is `tools/validators/run_all.py`. Each lane reports **PASS**, **FAIL** or **SKIP** with the reason, and the summary counts all three. A SKIP is never reported as a pass. Exit 0 means no FAIL; with `--strict`, it also means no SKIP.
- **`fixture_sync` is no longer a lane** (Phase02, 2026-09-23). It read a consumer's checkout, which a producer gate must not do (R1). `tools/validators/check_fixture_sync.py` stays as a standalone tool, moving to the consumer side (`docs/Planning/PlatformDependencies.md` P8).
- **CI: parked (lead, 2026-09-23: "that is really advanced and I don't want it").** Today the gate is run by hand, and a maintainer runs it strict, with the encoder, before merging. `.github/workflows/gate.yml` is written and kept, but dormant: it would run the one command strict on every pull request, with read-only permissions, no secrets and actions pinned by SHA. It has never run, because the Imrsv-tools organisation's Actions policy disables all repositories. The Contribution Path phase decides whether to turn it on.
- **No gate-id registry** exists; gates are named by file.

## Planned roots *(carried from `FolderStructure.txt`; not built)*

- `tools/matter_manager/`: file management, import, promotion, subset/export, path remap *(planned)*.
- `bridges/unreal/`, `bridges/blender/`, `bridges/usd/`: transformers and cook targets. **Reevaluate (2026-09-23):** the Blender bridge was built at `blender/`. The Unreal side is, per R14, a release bundle + master contract now, with an optional reference UE masters package later.
- `MatterLibrary/materials/environmental/` and the unpopulated classes (wood, soil, composite, polymer, coating, sand, vegetation, liquid, atmospheric, energy): *(planned)* taxonomy coverage.
- Extra shared textures: overlays `{fingerprints, smudges, watermarks}`, masks `{wear, paint, rust, dirt, edge}` *(planned)*.
- `_SupportingDocs/`: supplemental design material. **Reevaluate (2026-09-23):** superseded by `docs/`.

## What does NOT land here

- **What the system is** → `docs/specs/`.
- **How code is written** → `CodingStandards.md` (still a stub).
- **Naming rules for Matter assets and id series** → `NamingConventions.md`.
