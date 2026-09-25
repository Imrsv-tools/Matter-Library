# Matter Library — Naming Conventions

**Status: ACTIVE (arrived 2026-09-23, Phase01).** Its trigger was met long before adoption: the Matter filename grammar, the scale tags and the release ids were id series in live use. See `Methodology/AgenticEngineering_Workflow.md` §Where stack knowledge lives.

## Relationship to the Glossary and the identity spec

**`docs/Glossary.md` says what a term MEANS. This doc says what a name may LOOK LIKE.** A term that needs a definition goes there; a rule about form goes here.

**The Matter filename grammar is owned by `docs/specs/Ontology/Identity.md`** (brought home in Phase01 step 1.3) — the tokens, defaults, the ≤63-character `[A-Za-z0-9_]` budget and the scale-tag table. This doc carries only the summary below and points there; **where they disagree, Identity.md wins.**

## Matter asset names (summary; owner: Identity.md)

- **Filename:** `Material_Variant_Condition_Detail_sNN_vNN.mtlx`, **exactly six tokens**. Each token is a fixed axis: Material = the matter/species · Variant = the look (texture + tint + settings; default `Natural`) · Condition = damage (overlay 1; default `Clean`) · Detail = the other layers (overlays 2–3; default `Base`). *(Axes and the six-token rule: 2026-09-25.)*
- **Domain / Class live in the folder path only** (`MatterLibrary/materials/<domain>/<class>/`), so an article can be recategorised without a rename.
- **Name budget:** the stem is **≤63 characters** of **`[A-Za-z0-9_]`** only. It must survive Blender's USD export unchanged. `tools/validators/validate_material.py` enforces it (the `materials` lane of `run_all.py`, exercised against fixtures by the `grammar` lane).
- **Scale tags:** `s0001` · `s001` · `s01` · `s1` · `s10` · `s100` · `sUKN` (a closed set).
- **System materials** are the one sanctioned exception to the grammar (`IMRSV_MissingMaterial`).

## The casing matrix

| Surface | Form | Example |
|---|---|---|
| Matter asset filename stem | the grammar above: PascalCase tokens joined by `_` | `Copper_Verdigris_Aged_Base_s01_v01` |
| Domain / Class folders | lower-case, single word | `engineered/metal/` |
| LCD / author-tier ports on the MaterialX interface | `snake_case` (OpenPBR style) | `base_color_tint`, `roughness_bias` |
| Render-role texture nodes | `snake_case` with a `_tex` suffix | `overlay1_tex`, `maskset_tex` |
| Master tokens | PascalCase | `Opaque`, `TranslucentThin`, `TwoLayer`; plus the lower-case `system` for the fallback |
| Python tools | `snake_case.py` | `project_runtime_catalog.py` |
| Planning docs | `YYMMDD_R_ConceptName.md` (research) · `Phase<NN>_<Name>.md` / `PhaseTBD_<Name>.md` (phases) | `260923_R_StandaloneSetup.md` |

## Technology / product-name casing

- **Preserve official mixed-case names** on human and code surfaces: **`MaterialX`**, **`OpenPBR`**, **`OpenUSD`**, **`Blender`**, **`Unreal`**.
- Where mixed case isn't allowed (file extensions, JSON keys, CLI flags), use the documented alias **`mtlx`**. **Banned:** `Mtlx`, `Materialx`.

## Identifier vocabularies (who assigns what, and when)

| Series | Form | Assigned by · when | Authoritative artifact |
|---|---|---|---|
| **Library release** | `matterlib-X.Y.Z` (semver: MAJOR breaking · MINOR additive · PATCH visual fix) | the maintainer, at promotion | the release's `library/releases/matterlib-X.Y.Z.lock.yaml` |
| **Material / texture version** | `vNN`, two digits, starting at `v01` | the contributor, at authoring; the next free integer for that asset | the filename (material) · the manifest entry (texture set) |
| **Catalog schema** | `schema_version: <int>` | a contract phase only | `docs/specs/Contract/RuntimeCatalog.md` |
| **Phases** | `Phase<NN>` once the lead numbers it; `PhaseTBD_<Name>` until then; steps `<NN>.<n>`, tasks `<NN>.<n>.<m>`, **numeric at every level, never a letter suffix** | the lead | `docs/Planning/Roadmap.md` |
| **Research docs** | `YYMMDD_R_<Concept>.md` (probe results: `YYMMDD_R_Spike_<Subject>.md`) | whoever opens the research | the file name |
| **Lead rulings in a research thread** | `R<n>` within that doc | the doc's author, at recording | that doc's `## Resolved` table |

*No gate-id or check-id series exists yet (2026-09-23).*

## Historical names kept on purpose

These names carry the **IMRSV** brand because the library was built inside that platform. **They are kept, not renamed** (a carried term is never renamed; consumers depend on them): `imrsv_metadata` (the MaterialX nodedef) · `imrsv:matterlibRelease` (the USD release pin) · `IMRSV_MissingMaterial` (the fallback article) · `imrsv_lcd_export` (the Blender add-on). Any future rename is a contract change, and a release bump, owned by a contract phase.

## Retired names

Recorded in `docs/Glossary.md` §Retired identifiers.

## What does NOT land here

- **How code is written** → `CodingStandards.md`.
- **Where artifacts live** → `ToolingConventions.md`.
