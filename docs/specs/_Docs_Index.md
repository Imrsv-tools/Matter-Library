# Matter Library specs — index

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for these specs; consumers point here.

Navigation for `docs/specs/`. **Start at [`_Architecture.md`](_Architecture.md)**: the component map, how the pieces fit, and the decisions of record. Vocabulary is in [`../Glossary.md`](../Glossary.md); naming rules are in [`../NamingConventions.md`](../NamingConventions.md).

## By question

| If you want to know… | Read |
|---|---|
| what the Matter Library is, and how its parts fit | [`_Architecture.md`](_Architecture.md) |
| what a Creator experiences, and what shipped for Blender | [`Experience/Experience_MatterLibrary.md`](Experience/Experience_MatterLibrary.md) |
| where a material goes in the taxonomy (Domain / Class) | [`Ontology/Taxonomy.md`](Ontology/Taxonomy.md) |
| how to name a material; scale tags; the version axes | [`Ontology/Identity.md`](Ontology/Identity.md) |
| which masters exist and what an article can *be* | [`Ontology/MasterSet.md`](Ontology/MasterSet.md) |
| the rules a `.mtlx` must follow | [`Contract/MaterialXTemplate.md`](Contract/MaterialXTemplate.md) · the reference article in [`Contract/examples/`](Contract/examples/) |
| what a release manifest contains; the status lifecycle; governance | [`Contract/Manifest.md`](Contract/Manifest.md) |
| the machine-readable catalog every release ships | [`Contract/RuntimeCatalog.md`](Contract/RuntimeCatalog.md) |
| which parameters are adjustable, by whom | [`Contract/LCDSchema.md`](Contract/LCDSchema.md) |
| what a Blender-exported Matter asset must look like | [`Contract/CreatorAssetProfile.md`](Contract/CreatorAssetProfile.md) |
| what is in the current release | [`Catalog/Catalog.md`](Catalog/Catalog.md) |
| how materials get made, and the provenance rule | [`Authoring/AuthoringGoldenPath.md`](Authoring/AuthoringGoldenPath.md) |
| how a release is staged, frozen, approved, activated and rolled back | [`Distribution/ReleaseModel.md`](Distribution/ReleaseModel.md) |
| what the tools in `tools/` do and which gates run | [`Tooling/AuthoringHarness.md`](Tooling/AuthoringHarness.md) |
| the pinned USD + MaterialX build used for validation | [`Tooling/USDValidationToolchain.md`](Tooling/USDValidationToolchain.md) |
| texture compression and visual parity | [`Tooling/CompressedDistribution.md`](Tooling/CompressedDistribution.md) |
| what a consumer (IMRSV, Blender, USD viewers) specifies on its own side | [`Consumers.md`](Consumers.md) |

## Reading order for a new contributor

1. [`_Architecture.md`](_Architecture.md)
2. [`Ontology/Identity.md`](Ontology/Identity.md)
3. [`Ontology/MasterSet.md`](Ontology/MasterSet.md)
4. [`Contract/MaterialXTemplate.md`](Contract/MaterialXTemplate.md)
5. [`Contract/LCDSchema.md`](Contract/LCDSchema.md)
6. [`Authoring/AuthoringGoldenPath.md`](Authoring/AuthoringGoldenPath.md)

That is enough to author a conforming article. Releases come after: [`Contract/Manifest.md`](Contract/Manifest.md) → [`Distribution/ReleaseModel.md`](Distribution/ReleaseModel.md).

## Markers used in these specs

`(planned)` · `Drift (date)` · `Reevaluate (date)` · `Updated (date, measured: …)` — the project's rule is to annotate reality, never delete intended design (`.ai/AI_WorkingAgreement.md` §Project practices).
