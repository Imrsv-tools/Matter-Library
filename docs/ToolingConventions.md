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
| `tools/generators/` | the Blender Asset-Browser library generator (`gen_asset_library.py`, which builds on `blender/masters/` since 2026-09-27; `matter_proxy.py`, the look-alike it used before, retired and kept) | Apache-2.0 |
| `tools/preview_generators/` | the preview scene for one article, rendered headless with `usdrecord` (`--render`); `--set` previews a moved Creator slider | Apache-2.0 |
| `tools/parity/` *(Phase05, 2026-09-27; Unreal column Phase06, 2026-09-30)* | the parity rig: `rig.py <article> [--sweep]` (or `--character [<skin>]`) renders one material side by side in USDLiveView's renderer (Storm), Blender (Cycles) and Unreal, and writes `library/parity/<article>/sheet.png` + `scorecard.md` (git-ignored). **The verdict is the Moved agreement** (each slider moves every tool alike); picture ΔE2000 between tools is a diagnostic (Phase06 D9). `--no-blender` compares Storm with Unreal on a machine whose Blender cannot render parity. `job.py` (the render job), `drivers/storm.py`, `drivers/blender_render.py`, `drivers/unreal.py` (Phase06), `compare.py` (ΔE2000, SSIM, the ruler and seam checks), `pair_sheet.py` (Phase12, 2026-10-05: one article with a slider set, beside another as authored, per tool, built from the pictures the rig stored; it renders nothing), `scene/build_scene.py` → `scene/test_scene.usda`, `scene/build_character.py` → `scene/character_scene.usda`. `JOB_FORMAT.md` is the contract a renderer's driver implements | Apache-2.0 |
| `unreal/` *(Phase06, 2026-09-29)* | the Matter Unreal runtime, the peer of `blender/`: `MatterRuntime/` (a small Unreal 5.8 app, Substrate on: `Source/` its C++, `Config/`, `Scripts/build_masters.py` the **8 Unreal masters**, which Studio adopts, `PlatformDependencies.md` P20). **Every asset is generated; no `.uasset` is committed** (`Content/`, `Binaries/`, `Intermediate/`, `Saved/`, `DerivedDataCache/`, `Packaged/` are git-ignored). `build.sh [editor\|masters\|package\|all]` builds it from scratch (capped jobs, `nice`); `publish.sh N` publishes `dist/`'s archive as the GitHub pre-release `unreal-runtime-vN` and writes the pin **`RUNTIME.json`** (tracked), which the rig's driver downloads into the git-ignored `package/` | Apache-2.0 |
| `blender/masters/` *(Phase05, 2026-09-27)* | the Blender versions of the masters (eight since Phase08's `Hair`), built by code (`build_masters.py`: `ML_Place2D` + one `ML_<Master>` group each), and `load_article.py`, which builds a `MatterLCD_<id>` material from an article's `.mtlx`; used by the rig and by the Asset-Browser library generator. **`article.py`** *(Phase06)* is the one article reader, plain XML with no `bpy`: `load_article.py` and the Unreal driver both import it | Apache-2.0 |
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
| **see a material in Storm, Blender and Unreal** | `uv run tools/parity/rig.py <article> [--sweep]` · `--character [<skin>]` for the MakeHuman body. The Unreal column comes from the pinned runtime, downloaded once (no Unreal install needed) |
| build the Unreal runtime · publish it *(needs Unreal 5.8)* | `UE=<Unreal 5.8 root> unreal/build.sh` · then, with the sources pushed, `unreal/publish.sh <N>` and commit + push `unreal/RUNTIME.json`. Publishing is public: the lead decides when (Phase06 D14) |

**Tool locations (environment variables, all optional):**
- `COMPRESSONATORCLI` — the pinned texture encoder, AMD `compressonatorcli` **V4.5.52** (default `~/.local/bin/compressonatorcli`). Without it the `compression` and `staging` lanes **SKIP** and say so, and `release_verify` checks everything except the `.dds` set.
- `USD_TOOLS_ROOT` — the USD toolchain root (default `~/usd-tools`; the install is `$USD_TOOLS_ROOT/inst/usd-26.03`).
- `USD_TOOLS_ENV` — the toolchain's conda env (default `~/.conda/envs/imrsv-usd-tools`).
- `MATTER_PREVIEW_DIR` — where `make_preview.py` writes preview scenes and renders (default `<tmp>/matter-preview/`; never the repo).
- `MATTER_UNREAL_RUNTIME` — a packaged Unreal runtime's `MatterRuntime.sh`, used instead of the pinned download; `MATTER_UNREAL_EDITOR` — an Unreal 5.8 `UnrealEditor`, to run `unreal/MatterRuntime` in editor mode (the development loop). Neither set: the build `unreal/RUNTIME.json` pins. `MATTER_BLENDER` — the Blender the rig runs. `MATTER_BLENDER_DEVICE` — `cpu` or `gpu`, to force what the rig's Blender driver renders on; unset, it takes the first device that can actually render (OptiX, CUDA, then the CPU) and names it in the job's `blender.log` *(2026-10-05)*.

**What a second project tells the Unreal master builder (environment variables, all optional; 2026-10-05, `PlatformDependencies.md` M7):** `unreal/MatterRuntime/Scripts/build_masters.py` reads them, and its head is the owner of what each does. Unset, the build is the library's own runtime's, and the runtime published from here is built with none set. A value the builder does not know stops the build.
- `MATTER_MASTERS_ROOT` — where the masters and their default textures are written: a package path, `/Game/<path>` or a plugin's content mount point (default `/Game/Masters`).
- `MATTER_MASTERS_SKINNED=1` — the masters also draw on a skinned mesh with morph targets.
- `MATTER_MASTERS_MESH_V=unreal` — the meshes' UVs are Unreal's (`v = 1 − t`), not USD's `st`.
- `MATTER_MASTERS_MESH_BINORMAL=unreal` — the meshes' binormal runs along `+v`, so the normal map's green is turned.
- `MATTER_MASTERS_SKY=0` — leave out the rig's Sky.
- **Candidates, each for an open question:** `MATTER_MASTERS_COLOUR_SAMPLER=srgb` (the colour slots sample an sRGB texture) and `MATTER_MASTERS_REFRACTION=index` (the Refraction input takes the article's index on the solid see-through master and 1.0 on the thin one; M6).
- **Run in Unreal by the platform, in its own project (2026-10-05; `261005_R_PlatformMasterAdoptionAsks.md` Passes 5 and 6):** the five above, all eight masters compiling and drawing with them, a character included, and a bump reading as a bump. `MATTER_MASTERS_REFRACTION=index` compiles and leaves the thin master right; the solid master's bend under it is not settled. `MATTER_MASTERS_COLOUR_SAMPLER=srgb` has never been built. **The unset build is run in Unreal and is unchanged (2026-10-05, the same doc's Pass 9; the library's own project, Unreal 5.8.0):** its nine *"built …"* lines and its result line are those of the build of 1 October, byte for byte, and its assets the same sizes. That is the engine's account of what was built, not a picture. *(Was, earlier the same day: "The unset build has not been run in Unreal since the switches were added", and before that "None of these has been run in Unreal".)*
- **`unreal/build.sh masters` calls a build good only on BOTH an exit code of 0 and the builder's own line** (`MATTER RESULT ok`). Neither alone is enough: in the platform's project the commandlet exited 0 after the script raised, and in the library's own project the same refusal made it exit 255 (both on Unreal 5.8, 2026-10-05). The builder's lines reach the output only with `-FullStdOutLogOutput` (seen in both). A caller of its own should check both too, and compare the builder's `told …` line with what it set. *(Was, earlier the same day: "reads the result from the builder's own line, not from the exit code". Changed after the run in the library's own project, the same doc's Passes 9 and 10.)*
- **A builder change that alters nothing at its defaults needs no new runtime published** (the lead, 2026-10-05; the same doc's §Resolved, MA-RD1). The test is what the default build makes: `unreal/build.sh masters` with nothing set, its *"built …"* lines compared with those of the build the pinned runtime came from.
- **The shell scripts under `unreal/` are not executable in the repo** (seen 2026-10-05): run them as `bash unreal/build.sh …`.

Every script finds the repo from its own location; none assumes a checkout path. *(Phase02, 2026-09-23. Before it, `run_all.py` failed at import for want of MaterialX, several tools hardcoded a retired checkout path, and there was no pinned environment and no CI.)*

## Gates and CI

- **The gate of record** is `tools/validators/run_all.py`. Each lane reports **PASS**, **FAIL** or **SKIP** with the reason, and the summary counts all three. A SKIP is never reported as a pass. Exit 0 means no FAIL; with `--strict`, it also means no SKIP.
- **`fixture_sync` is no longer a lane** (Phase02, 2026-09-23). It read a consumer's checkout, which a producer gate must not do (R1). `tools/validators/check_fixture_sync.py` stays as a standalone tool, moving to the consumer side (`docs/Planning/PlatformDependencies.md` P8).
- **CI: parked (lead, 2026-09-23: "that is really advanced and I don't want it").** Today the gate is run by hand, and a maintainer runs it strict, with the encoder, before merging. `.github/workflows/gate.yml` is written and kept, but dormant: it would run the one command strict on every pull request, with read-only permissions, no secrets and actions pinned by SHA. It has never run, because the Imrsv-tools organisation's Actions policy disables all repositories. The Contribution Path phase decides whether to turn it on.
- **No gate-id registry** exists; gates are named by file.

## Planned roots *(carried from `FolderStructure.txt`; not built)*

- `tools/matter_manager/`: file management, import, promotion, subset/export, path remap *(planned)*.
- `bridges/unreal/`, `bridges/blender/`, `bridges/usd/`: transformers and cook targets. **Reevaluate (2026-09-23):** the Blender bridge was built at `blender/`. The Unreal side is, per R14, a release bundle + master contract now, with an optional reference UE masters package later. **Update (2026-09-30, Phase06):** the Unreal project was built at `unreal/` (the runtime and its 8 masters, which Studio adopts, P20); the reference masters package (*Unreal Reference Masters*) is still *planned*.
- `MatterLibrary/materials/environmental/` and the unpopulated classes (wood, soil, composite, polymer, coating, sand, vegetation, liquid, atmospheric, energy): *(planned)* taxonomy coverage.
- Extra shared textures: overlays `{fingerprints, smudges, watermarks}`, masks `{wear, paint, rust, dirt, edge}` *(planned)*.
- `_SupportingDocs/`: supplemental design material. **Reevaluate (2026-09-23):** superseded by `docs/`.

## What does NOT land here

- **What the system is** → `docs/specs/`.
- **How code is written** → `CodingStandards.md` (still a stub).
- **Naming rules for Matter assets and id series** → `NamingConventions.md`.
