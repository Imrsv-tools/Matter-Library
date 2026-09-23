# Experience — Matter Library

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

**Status:** partial product direction. Much of the release and experience mechanics is still being built (the lead, 2026-09-23: "not in production… still building"). The Blender half of the Creator Golden Path is real (see §Shipped).

## Intent

The Matter Library is a **community-driven, versioned material library**. Its job is to give Creators high-quality, industry-standard materials that travel across Blender, Unreal-based apps, and USD/MaterialX-aware tools, without forcing every composition or model asset to carry heavy repeated texture payloads.

Its content is CC0: contributions are freely and fully distributable, contributors are credited, and consumers are asked to credit the Matter Library. The dependable experience starts with a **curated, versioned release**. Community submissions feed future releases through review and curation.

> **Drift (2026-09-23):** the platform version of this doc framed the library as "the official, versioned material library for IMRSV" and "a fixed official library… distributed by IMRSV". Rulings R1/R9 re-frame it as a community resource that IMRSV (and others) consume. The ideas below are carried in full; only the framing moved.

## Core Product Promise

A Creator can author a model with Matter materials, bring it into a consuming application, refine the look there, and share or play the result, without manually managing large texture folders.

The material identity stays stable across the chain. The heavy material data lives in an installed Matter Library release. Compositions and model assets carry material intent and small refinements, not duplicated texture libraries.

## Why It Exists

Materials are both an appearance system and a distribution strategy.

- Compositions stay lightweight because common textures are not repackaged into every composition.
- Consuming apps can update more often without forcing users to re-download the whole material library.
- The Matter Library can update on a slower cadence, because it is large, curated and shared by many consumers.
- Models authored in Blender use the same material identities that downstream apps understand.
- External MaterialX/USD workflows remain part of the pipeline instead of a separate import/export dead end.

## Creator Golden Path

> The **Creator Golden Path** is the end-user *consumption* flow below. It is distinct from the **Authoring Golden Path** ([`../Authoring/AuthoringGoldenPath.md`](../Authoring/AuthoringGoldenPath.md)), the pipeline for *making* Matter materials. Don't blur the two.

**The Blender leg — owned by this repo:**

1. A Creator makes a model in Blender.
2. The Creator assigns materials from the Blender-friendly Matter Library (the Asset-Browser library).
3. The Creator makes simple predefined refinements where supported: tint, dust, scratches, patina, wear.
4. The Creator exports the model with the Matter exporter, producing an [Open Matter Creator asset](../Contract/CreatorAssetProfile.md).

**Downstream — owned by each consumer:**

5. A consuming app (for example IMRSV Studio) adds the model.
6. It recognises the Matter identity and resolves it against an installed release.
7. It renders the material with its own runtime representation, not with texture payloads exported beside the model.
8. The Creator can refine the material there with the same bounded controls (the [Creator tier](../Contract/LCDSchema.md)).
9. The composition saves those choices and refinements.
10. Other instances resolve the same identity from their installed release.

*Consumer-side (IMRSV): the Studio/Theater steps, panels and recovery flows — see [Consumers](../Consumers.md).*

The point of the golden path is not universal ingest. It is a controlled, high-quality chain for content made the Matter way.

## Library Shape

The Matter Library should be understandable as a product, not only as a folder of files.

- **Curated release:** the versioned material set a manifest pins ([ReleaseModel](../Distribution/ReleaseModel.md)).
- **Material identity:** the stable name/version a composition or model uses to refer to a material ([Identity](../Ontology/Identity.md)).
- **Material payload:** the MaterialX definition, textures, previews and prepared runtime data installed with a release.
- **Blender-friendly library:** the authoring-side representation Creators use while modelling (shipped: the Asset-Browser library).
- **Consumer runtime representation:** the form each consuming app uses to render efficiently. Consumer-owned; for IMRSV see [Consumers](../Consumers.md).
- **Source MaterialX representation:** the portable material definition used by compatible tools.

A curated release is the dependable baseline. Other layers can exist, but they should not weaken the promise that a composition built against a release can be resolved later.

## Creator Roles

### Creator consuming materials

The main experience is simple: install a Matter Library release, use its materials while modelling or composing, and trust the consuming app to resolve them. This Creator should not need to understand MaterialX graphs, texture packaging, masters or file repointing. They should see material names, previews, scale and version information, and useful refinement controls.

### Creator contributing materials

A Creator may submit new materials or source textures. Submissions dedicate them under CC0 (see `CONTRIBUTING.md`) and do not immediately become part of a release: they move through review, cleanup, compatibility checks and release curation first.

### Maintainer (founding author)

Before community contribution is flowing, maintainers build the first curated library by running the [Authoring Golden Path](../Authoring/AuthoringGoldenPath.md) under the shipped-pixel rule. This is production infrastructure, not an end-user experience; it is named here so the chain is complete.

### Library curator

Curators decide which submitted materials enter a release, prepare the required representations, and protect compatibility across releases. This matters, but it should not distract the first usable chain: import, resolution, refinement and playback against a release.

## Versioning And Updates

The library will be large, so updates should usually be additive and diff-friendly.

> **Two version axes (don't conflate):** a **material** carries its own version (`vNN`, in its name); the **library release** is versioned separately as a semver set, and a release pins which `vNN` of each material it includes ([Identity](../Ontology/Identity.md)). **The manifest is the authoritative catalog:** a release is a lockfile, not a copy of files ([Manifest](../Contract/Manifest.md)).

- Releases are versioned.
- Existing compositions keep resolving against the materials they were authored with.
- Texture removal should be rare or avoided, because old compositions may depend on those assets.
- Quality upgrades need compatibility care: changing a base texture can alter the look of existing compositions.
- A consuming app should be able to tell the Creator when a required release or material is missing (consumer-owned behaviour).

The exact mechanics belong in the release specs. The experience requirement is that library updates never make older compositions silently wrong.

## Share And Export

Sharing and exporting are different experiences.

- **Share** with someone who has, or can install, the required release: the composition stays lightweight.
- **Export** for use outside that ecosystem: package the material payloads the composition needs. The exporter's **complete-portable** form does exactly this.

The Creator should not have to guess which mode they are in.

## Shipped

The Blender half of the Creator Golden Path is real (2026-07-17):

- **Installed Blender Asset-Browser library.** It offers all **11 Creator-selectable articles** of `matterlib-0.1.0`. It excludes the system material `IMRSV_MissingMaterial` via the `creator_selectable` catalog field (default `true`; `false` only on the system material — see [RuntimeCatalog](../Contract/RuntimeCatalog.md)).
- **v1 Blender representation = a catalog-driven Principled-BSDF proxy.** Each article is a `MatterLCD_<id>` node group generated by **one generic recipe→proxy mapper** (no per-article branches). Overlay/maskset sockets are **exposed but unwired in v1**, a documented limitation. *Not yet shipped:* MaterialX-native Blender import (the proxy stands in for the real `.mtlx` look).
- **The Matter exporter** (**File → Export → IMRSV LCD USD**, `blender/addons/imrsv_lcd_export/`; historical name kept) emits two forms:
  - **lightweight** (default): bare `@Name.mtlx@` references, library-resolved, with no `.mtlx` or textures beside the asset;
  - **complete-portable** (explicit checkbox): each required `.mtlx` and texture materialised **once**, with portable relative references, so the package opens without the library installed.

  Both conform to [CreatorAssetProfile](../Contract/CreatorAssetProfile.md).
- **The exact Matter identity travels on `assetInfo:identifier`**, independent of Blender's display name, which removes the old `_001` suffix heuristic.

> **Resolved (Phase02, 2026-09-23):** targets are **Blender 5.1+** (R6). The add-on declared 5.1.1; it enables and registers its exporter on the lead's Blender 5.1.0 (measured headless), so it now declares `(5, 1, 0)`.

## Future Layers *(planned)*

Part of the larger direction, but they should not drive the first usable chain:

- personal saved material variants
- community scoring or popularity signals
- contributor reputation and credits surfacing
- material submission tools
- curator/admin conversion tools
- promotion of community materials into releases
- **agentic material generation**: an agent-run generate → decompose → assemble → QC loop that proposes *candidate* articles for human judgement (lead, 2026-09-23; `docs/Planning/Research/260923_R_StandaloneSetup.md` Pass 8)
- optional Blender add-ons or assisted export tools

## Open Experience Questions

- What is the first curated release that goes to users (after the `0.1.0` pilot)?
- How visible should library versioning be to Creators?
- How should a consuming app explain that a material is missing, unsupported or from a newer release?
- When a shared composition needs a release the user does not have, what is the recovery path?
- Which contribution workflow is worth designing first, once the core chain works?

## Related Docs

- [`../_Architecture.md`](../_Architecture.md) — the system architecture and component map.
- [`../Ontology/Identity.md`](../Ontology/Identity.md) · [`../Contract/Manifest.md`](../Contract/Manifest.md) · [`../Authoring/AuthoringGoldenPath.md`](../Authoring/AuthoringGoldenPath.md).
- [`../Consumers.md`](../Consumers.md) — where each consumer's side of this experience is specified.

## History

- 2026-06 — the experience was first written inside the IMRSV platform, as IMRSV's official material library.
- 2026-07-17 — the Blender leg shipped: the Asset-Browser library, the proxy mapper, and both exporter forms.
- 2026-09-23 — brought home and re-framed as a community resource consumed by IMRSV and others (R1/R9).
