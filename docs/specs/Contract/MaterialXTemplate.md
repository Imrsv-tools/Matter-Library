# MaterialX Template — `open_pbr_surface` 1.39, single-file

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

The contract for **what a Matter material `.mtlx` looks like**. Every Matter material (an [article](../../Glossary.md)) is a **single-file MaterialX 1.39 document** built around one **`open_pbr_surface`** shader, exposing the [LCD inputs](LCDSchema.md) as material **interface inputs**. The reference example is [`examples/Reference_Copper_Verdigris_Aged_Base_s01_v01.mtlx`](examples/Reference_Copper_Verdigris_Aged_Base_s01_v01.mtlx), a verbatim copy of a live assembled article. *(Updated 2026-09-23, measured: the former hand-authored platform template was retired because it mixed an overlay over base colour and loaded it as `srgb_texture`, which the [modulator rule](../Ontology/MasterSet.md) forbids; see [`examples/README.md`](examples/README.md).)*

> **Why OpenPBR:** `open_pbr_surface` is the ASWF ecosystem's uber-shader — bundled in MaterialX 1.39+ and USD 25.05+, native in Omniverse, the Maya/3ds Max default, and **Blender's Principled BSDF is officially "based on the OpenPBR Surface shading model."** Bidirectional `standard_surface`↔OpenPBR translation graphs exist (MaterialX 1.39.1+), so the existing keep-set converts. One canonical model is what keeps cross-renderer [parity](../../Glossary.md) honest (every renderer-side master is a *window onto* this model — [MasterSet](../Ontology/MasterSet.md)).

## Hard rules

1. **Single-file, self-contained.** No multi-file `.mtlx` include chains — Storm has known `NodeDef-not-found` failures with includes ([OpenUSD #1636](https://github.com/PixarAnimationStudios/OpenUSD/issues/1636) / [#1586](https://github.com/PixarAnimationStudios/OpenUSD/issues/1586)); self-contained single-file documents render reliably. Everything a material needs is in its one `.mtlx`.
2. **MaterialX 1.39, `open_pbr_surface`.** Document `version="1.39"`; the surface shader is `<open_pbr_surface>`. No `standard_surface` in new authoring (the keep-set converts via the translation graph).
3. **LCD as interface inputs.** Creator-adjustable values (tint, UV transform, overlay intensity, roughness bias) are exposed as **`<input>` interface ports on the nodegraph `NG_<material>`**. A Creator tweak is a value on the bound Material's `inputs:<port>` that `NG_<material>.inputs:<port>` **connects to**; without the connection the value is inert in stock USD tools, because usdMtlx exposes only the surface shader's inputs on the Material ([LCDSchema §Carrier rule](LCDSchema.md#carrier-rule-no-imrsv-attrs), corrected 2026-09-24). UV placement lands on a **`place2d`** node inside the nodegraph with MaterialX `place2d` semantics, never on custom prim attrs. The biased roughness is clamped to [0, 1] inside the article ([LCDSchema](LCDSchema.md) §Creator-adjustable subset).
4. **No `imrsv:` USD attributes for materials.** Identity and adjustments ride **standard carriers** (the material name, `material:binding`, shader `inputs:`). The composition stays as standard-USD as possible (the chain's cleanliness constraint).

> **Reevaluate (2026-09-23):** the [release pin](Manifest.md#composition-release-pin--imrsvmatterlibrelease) `imrsv:matterlibRelease` is an `imrsv:`-prefixed key in root-layer `customLayerData` — it is layer metadata, not a material attribute, but it sits in tension with this principle; the historical name is kept (R16) and the tension is owned by the contract phase.

## The `imrsv_metadata` nodedef — internal hint, NOT a USD `imrsv:` attr

A material **may** carry an internal **`imrsv_metadata` nodedef** inside the `.mtlx` — an optional portability hint holding `master_material`, `scale_tag`, `meters_per_tile`, `domain`, `class` (deliberately **no `version`** — the manifest is the version source of truth). The historical name is kept.

*(Updated 2026-09-23, measured: all 12 live articles under `MatterLibrary/materials/` carry `ND_imrsv_metadata` with exactly those five inputs; `master_material` values are Opaque ×5, Masked, TranslucentThin, TranslucentThick, Subsurface, TwoLayer, Emissive, `system` ×1 each.)*

> ⚠ **This is NOT a no-`imrsv:` violation.** `imrsv_metadata` is an **internal MaterialX nodedef inside the `.mtlx` document** — it is *not* a USD `imrsv:` composition attribute on a prim. The no-`imrsv:`-attrs rule is about keeping the **USD composition** clean; a nodedef inside a self-contained material document is invisible to the composition. State this explicitly so a later pass doesn't "fix" it.

Its **role is downgraded** to an optional hint: the [manifest](Manifest.md) is the authoritative source for master mapping, scale, and taxonomy. The nodedef is a convenience for tools reading a loose `.mtlx`; the CI-agreement policy (does the nodedef have to match the manifest?) is an open later-phase question.

> **Drift (2026-09-23):** the manifest and runtime catalog carry **no master field** today (measured: no `master` key in any `library/releases/*.lock.yaml` or `*.catalog.json`), so the nodedef's `master_material` is currently the only place a master token is written down; R14 moves the per-article master token into release data (manifest → catalog), at which point this sentence becomes true — owned by the release-bundle / consumer-contract phase (R14).

## Anatomy of a Matter `.mtlx` (target shape)

```
<materialx version="1.39">
  <nodegraph name="NG_<material>">           ← base PBR + place2d UV + ≤3 overlays + ≤1 mask
    <input> ports …                            ← the LCD interface inputs (Creator-adjustable subset)
    <place2d> … </place2d>                     ← UV scale/offset/rotation (NOT a prim attr)
    <image>/<tiledimage> … texture reads       ← base color, roughness, normal, …
    <output> surface-graph outputs
  </nodegraph>
  <open_pbr_surface name="SR_<material>"> … </open_pbr_surface>   ← the OpenPBR shader
  <surfacematerial name="<QualifiedMatterName>"> … </surfacematerial>   ← name = identity
  <nodedef name="ND_imrsv_metadata"> … </nodedef>                ← optional internal hint
</materialx>
```

The `<surfacematerial>` **name is the qualified Matter identity** ([Identity](../Ontology/Identity.md)) — that is what a consumer resolves.

> **Reevaluate (2026-09-23):** measured on the live articles, the `<surfacematerial>`, `NG_` and `SR_` names are the full filename stem **including** `_vNN` (e.g. `Copper_Verdigris_Aged_Base_s01_v01`), whereas the manifest/catalog `id` ends at the `sNN` scale tag — whether the resolved identity includes the material version needs one stated rule in [Identity](../Ontology/Identity.md).

The overlay and maskset textures inside the nodegraph use the fixed [render-role texture](LCDSchema.md#render-role-texture-nodes--assembler-owned-node-name-contract) node names (`overlay1_tex` / `overlay2_tex` / `maskset_tex`), load `lin_rec709`, and **modulate** normal and roughness — they are never mixed over base colour ([MasterSet](../Ontology/MasterSet.md) §Overlay/MaskSet model). The [reference example](examples/Reference_Copper_Verdigris_Aged_Base_s01_v01.mtlx) shows the full shape.

## Validation

Articles are validated **offline** with the **MaterialX Python SDK** — load the document and assert `doc.validate()` returns true with the MaterialX stdlib loaded — not with any consumer's own `.mtlx` parser. *(Updated 2026-09-23, measured: this is the `sdk-validate` check in `tools/validators/validate_material.py`, run over every article by `tools/validators/run_all.py`.)*

> **Deployment gotcha:** USD builds burn in the MaterialX stdlib path — a shipped USD consumer must set `PXR_MTLX_STDLIB_SEARCH_PATHS` (distinct from asset-path resolution). Recorded for [Distribution](../Distribution/ReleaseModel.md) and the [USD validation toolchain](../Tooling/USDValidationToolchain.md).

## Status

**Template discipline specced; articles are generated.** The target shape is specced here and every live article is produced by the [assembler](../Tooling/AuthoringHarness.md) (`tools/converters/assemble_mtlx.py`) from its recipe, then SDK-validated. *(Updated 2026-09-23, measured: 12 recipes in `tools/converters/recipes/` for the 12 articles.)* No wire/ABI contract is frozen here.

## History

- Pre-standalone (2026-06 → 2026-07): the library standardised on OpenPBR (`open_pbr_surface`, MaterialX 1.39) as its one shading model, and on single-file documents after include chains were found to fail in Storm.
- Pre-standalone: the template shape and one hand-authored reference `.mtlx` were specced before the assembler existed; the generator came afterwards.
- Pre-standalone: the `imrsv_metadata` nodedef was downgraded from authority to optional hint in favour of the manifest.
- 2026-09-23: the hand-authored reference was retired for a verbatim copy of a live article, because it taught the overlay-over-base-colour defect.
- 2026-09-24: rule 3 now names the connection a Creator override needs (Matter-Library#1), and every article that declares `roughness_bias` clamps the biased roughness to [0, 1]. The 10 affected articles were regenerated in place at `v01` (lead: "fix forward only... we have no legacy projects yet"), and the reference copy was refreshed with them.
