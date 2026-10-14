# Catalog — the curated set, human-readable

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

The **human-readable view** of what a Matter Library release contains: which articles, where they sit in the taxonomy, which [master](../Ontology/MasterSet.md) each declares, their [scale](../Ontology/Identity.md) and their overlay/maskset payload. **The authoritative form is the release's [manifest](../Contract/Manifest.md)**, projected to the [runtime catalog](../Contract/RuntimeCatalog.md); this page is a view of them, never a second source. How a release is built, frozen, approved and activated is in [ReleaseModel](../Distribution/ReleaseModel.md).

## `matterlib-0.1.0` — the pilot release

*(Updated 2026-09-23, measured: generated from `library/releases/matterlib-0.1.0.catalog.json` (release `0.1.0`, `schema_version` 2, 12 entries) plus each article's `.mtlx` for its master token and render-role textures.)* This replaces the platform-era illustrative chart, which named articles that were never built.

`matterlib-0.1.0` is a **pilot**: approved and frozen to prove the release machinery, not shipped to users (lead, 2026-09-23). Every article is at `v01`. In the manifest an article's id is `domain/class/<stem>` and its `vNN` is a separate `version` field.

| Domain / Class | Article (stem) | Master | Scale | Status | Creator-selectable | Overlays / masks |
|---|---|---|---|---|---|---|
| engineered / cementitious | `Concrete_Smooth_Worn_Dusty_s1` | Opaque | s1 | approved | yes | overlay1, overlay2 |
| engineered / glass | `Glass_Clear_Clean_Base_s01` | TranslucentThin | s01 | approved | yes | overlay1, overlay2, maskset |
| engineered / metal | `Copper_Verdigris_Aged_Base_s01` | Opaque | s01 | approved | yes | overlay1, overlay2, maskset |
| engineered / metal | `Rust_OnSteel_Flaking_Base_s01` | TwoLayer | s01 | approved | yes | maskset |
| natural / mineral | `Diamond_Brilliant_Clean_Base_s01` | TranslucentThick | s01 | approved | yes | — |
| natural / stone | `Limestone_Veined_Clean_Base_s01` | Opaque | s01 | approved | yes | — |
| natural / stone | `Marble_Veined_Polished_Base_s01` | Subsurface | s01 | approved | yes | — |
| synthetic / plastic | `ABS_Matte_Clean_Base_s01` | Opaque | s01 | approved | yes | — |
| synthetic / textile | `Lace_Floral_Clean_Base_s01` | Masked | s01 | approved | yes | — |
| utility / emissive | `Neon_Signage_Clean_Base_s01` | Emissive | s01 | approved | yes | — |
| utility / virtual | `Diagnostic_UVGrid_Clean_Base_s1` | Opaque | s1 | approved | yes | — |
| utility / virtual | `IMRSV_MissingMaterial` | `system` | — | approved | **no** | — |

- **Coverage:** every one of the 7 masters has at least one example article, and 9 of the 19 taxonomy classes are populated. The environmental domain has none yet.
- `matterlib-0.0.1` (the earlier draft manifest, never approved) is kept in `library/releases/` as history.

> **Reevaluate (2026-09-23):** this table was generated once by hand. Generating it from the catalog at release time, so it can't drift, belongs with the release-bundle / consumer-contract phase.

## Thumbnails *(shipped in the dev snapshots and the dev install, Phase17, 2026-10-14; at a release: planned)*

**Shipped (Phase17, 2026-10-14):** `tools/thumbnails/make_thumbnails.py` renders each kept article **in Cycles**, at its best, on a subject that suits it: Matter by its master and class (a sphere and cube, a slab, a wall, a pane, a gem, a draped cloth, a neon ring, a card, leaves), and Character on the clothed character, from six views only. The 1024 px PNG masters and a record of what each was made from sit in the git-ignored `library/thumbnails/<identity>/`, and only stale pictures are re-made. They are published as baseline JPEG in the dev snapshots ([SiteFile](../Contract/SiteFile.md) `pictures[]`, `role: thumbnail`) and served at 512 px in the dev install ([RuntimeCatalog](../Contract/RuntimeCatalog.md) §A material's thumbnail). As release assets they are *planned* (the release-bundle phase). *Superseded, kept for history:* "At release preparation, `usdrecord` renders each article against a standardised sphere/dome scene. The same renders double as the per-class [parity](../Tooling/CompressedDistribution.md) baselines." Thumbnails are Cycles showcase renders (RD-MP-2), and the rig's pictures are not thumbnails (F-MP-6). The preview tooling exists in `tools/preview_generators/`; a committed thumbnail set does not yet (2026-09-23).

*(2026-10-14, [`261014_R_TheLibrarysSite.md`](../../Planning/Research/261014_R_TheLibrarysSite.md) RD-WS-4: the library's website is this set's first consumer. A standard preview set (the *thumbnails*, RD-MP-5) is published beside each release. The parity rig already renders every article in Storm, Blender and Unreal, at its defaults and with each Creator port moved; those renders are working files, not this set. Phase13's dev snapshots publish the Matter materials' default rig renders as release assets, labelled `role: rig` in the [site file](../Contract/SiteFile.md); they are still not this set.)*

## History

- 2026-06 — the catalog began as an illustrative chart before any release existed. It is replaced here by the real pilot contents.
- 2026-07 — the runtime catalog became a projection of the authored manifest (consumers stopped scanning folders). `matterlib-0.1.0` was approved as a pilot, with 12 articles covering all 7 masters.
