# Matter Library — Tooling Conventions

**Status: ACTIVE (arrived 2026-09-23, Phase01 step 1.5).** Its trigger, "the first real build", was met before adoption: the authoring harness, validators, release tooling and Blender add-on already exist. This doc takes over the artifact-taxonomy role of the retired `FolderStructure.txt` (archived verbatim at `docs/Planning/Phases/Complete/PreStandalone/FolderStructure.txt`). What each tool *does* is specified in [`docs/specs/Tooling/AuthoringHarness.md`](specs/Tooling/AuthoringHarness.md); this doc says **where things live and how they are named**.

## The artifact taxonomy

*Measured against the tree on 2026-09-23.*

| Root | What lives there | Licence |
|---|---|---|
| `MatterLibrary/materials/<domain>/<class>/` | the articles (`.mtlx`), **generated** from recipes, never hand-edited | CC0 |
| `MatterLibrary/textures/base/<domain>/<class>/<Set>/` · `textures/shared/{overlays,masks}/` | textures (Git LFS; `.gitattributes`) | CC0 |
| `library/releases/` | per-release records: `matterlib-X.Y.Z.lock.yaml` (authored) · `.catalog.json` (projected) · `.freeze.json` · `.approval.json` | CC0 |
| `library/provenance/` | per-release texture provenance records | CC0 |
| `library/staging/` | the staged release tree (PNG + compressed DDS). **Gitignored, rebuildable** | — |
| `tools/converters/` | authoring: `assemble_mtlx.py` (the assembler), `build_proof_subset.py` (recipes → articles), `project_runtime_catalog.py` (lock → catalog), `gen_*.py` (procedural textures) | Apache-2.0 |
| `tools/converters/recipes/` | one JSON recipe per article, `<Stem>_vNN.json` | CC0 |
| `tools/validators/` | the structural gate `run_all.py` and its checks (`validate_material.py`, `validate_manifest.py`, `check_determinism.py`, `check_fixture_sync.py`, `source_provenance.py`) + `fixtures/` | Apache-2.0 |
| `tools/releases/` | the release lifecycle: `stage_release.py` → `freeze_release.py` → `promote_release.py` (+ `validate_approval.py`) → `activate_release.py` | Apache-2.0 |
| `tools/compressors/` | BCn compression (`compress_textures.py`) + negative fixtures | Apache-2.0 |
| `tools/conformance/` | Creator-asset and parity checks: `assert_profile.py`, the `check_*.sh` wrappers, `codec_ab.py`, `build_ocio_parity_config.py`, the Blender slice exporters, `golden/`, `fixtures/` | Apache-2.0 |
| `tools/generators/` | the Blender Asset-Browser library generator (`gen_asset_library.py`, `matter_proxy.py`) | Apache-2.0 |
| `tools/preview_generators/` | usdview/usdrecord preview wrapper | Apache-2.0 |
| `tools/usd-toolchain/` | the pinned OpenUSD + MaterialX build recipe (`environment.yml`, `build-usd-tools.sh`, `run-all.sh`) | Apache-2.0 |
| `blender/addons/imrsv_lcd_export/` | the Matter exporter add-on + its `test_lcd_*.py` | Apache-2.0 |
| `blender/asset_library/` | the **generated** Asset-Browser library (`MatterLibrary.blend`, `blender_assets.cats.txt`) | CC0 |
| `blender/MatterMaterials.blend` | the scaffold scene the conformance slices export from | Apache-2.0 |
| `docs/` · `Methodology/` · `.ai/` · `.claude/` | specs, planning, method, agent surface | Apache-2.0 |

## Naming

- **Python tools:** `snake_case.py`, verb-first where it is an action (`build_…`, `check_…`, `validate_…`, `gen_…`, `project_…`).
- **Shell wrappers:** `check_*.sh`, `*-usd-tools.sh`.
- **Fixtures:** under a sibling `fixtures/` folder; deliberately bad inputs are named for what they break.
- **Tests:** `test_*.py` beside the code they test (`blender/addons/imrsv_lcd_export/`, `tools/conformance/`). Test documentation lives in the docstrings; there is no separate test-docs tree. That is the observed practice as of 2026-09-23, not yet a ruling: the first phase that ships a real test suite decides it here.

## Entry points

| To… | Run |
|---|---|
| validate everything structural | `python tools/validators/run_all.py` (16 lanes, listed in [AuthoringHarness](specs/Tooling/AuthoringHarness.md)) |
| (re)generate articles from recipes | `python tools/converters/build_proof_subset.py [<recipe.json> …]` |
| re-project a catalog from its lockfile | `python tools/converters/project_runtime_catalog.py` |
| stage / freeze / promote / activate a release | the scripts in `tools/releases/` ([ReleaseModel](specs/Distribution/ReleaseModel.md)) |
| build the USD validation toolchain | `tools/usd-toolchain/run-all.sh` ([USDValidationToolchain](specs/Tooling/USDValidationToolchain.md)) |

**Measured 2026-09-23:**
- `run_all.py` fails at import on the lead's box (no MaterialX Python module).
- Several tools still hardcode a retired absolute checkout path (`tools/conformance/*`, `tools/generators/gen_asset_library.py`).
- There is **no pinned Python environment** (no `requirements.txt` / `pyproject`) and **no CI**.

Fixing these belongs to the one-command-check phase on the Roadmap.

## Gates and CI

- **The gate of record** is `tools/validators/run_all.py`. Lanes whose tool is missing (e.g. `compressonatorcli`) **skip and report green**. A green run does not say which lanes actually ran. *(Drift, 2026-09-23: owned by the one-command-check phase.)*
- **The `fixture_sync` lane** compares against a *consumer's* mirror and passes silently when that consumer's tree isn't found. Under R1 it belongs on the consumer side. *(Drift, 2026-09-23: see `docs/Planning/PlatformDependencies.md`.)*
- **CI: none yet** (2026-09-23).
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
