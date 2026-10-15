# Matter Identity — filename grammar, charset budget, scale tags, versions

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

This spec owns the **Matter material asset-file grammar** — how a material is named so it stays readable, sortable, and **survives any USD exporter unchanged**. The [qualified Matter name](../../Glossary.md) *is* the material's identity (the spine of the chain — a composition carries the name, consumers resolve it). [NamingConventions](../../NamingConventions.md) (code / wire / doc naming) carries a summary and points here; **where they disagree, this spec wins.**

## Filename grammar

```
Material _ Variant _ Condition _ Detail _ sNN _ vNN . mtlx
Limestone_Veined_Distressed_Dusty_s01_v01.mtlx
Glass_Clear_Clean_Base_s01_v01.mtlx
```

**Exactly six tokens, five underscores, so a name always parses back into its axes.** Each token is a **fixed axis**, the same across the whole library. The words inside a token are free (PascalCase, digits allowed), so a name can be made by a Creator from where they left the sliders (e.g. a save counter, `VeryDistressed12`). The exact values always live in the file; the name is the readable, parseable handle.

| Token | Axis | Examples | Default |
|-------|------|----------|---------|
| **Material** | **the matter**, down to species or alloy (optionally with a base-set id, as in `Limestone26b`) | `Limestone`, `WhiteOak`, `MildSteel`, `StainlessSteel` | required |
| **Variant** | **the look**: the base-texture choice plus tint and the other [LCD](../Contract/LCDSchema.md) settings | `Natural`, `Veined`, `Polished`, `Brushed`, `Weathered`, `Blue` | **`Natural`** (untinted) |
| **Condition** | **damage**, driven by overlay 1 (+ the maskset) | `Clean` → `Worn` → `Distressed` → `VeryDistressed12` | **`Clean`** (slider at 0) |
| **Detail** | **everything else**, driven by overlays 2–3: usually deposits, sometimes a second damage layer | `Base` → `Dusty` → `Smudged` → `ScratchedButNotVeryDusty` | **`Base`** (sliders at 0) |
| **sNN** | [scale tag](#scale-tags) — meters per UV tile | `s01`, `s1` | required (`sUKN` if unknown) |
| **vNN** | [material version](#two-version-axes-dont-conflate) (this asset's own version axis) | `v01` | `v01` |

- **Domain and Class are NOT in the filename** — they live in the folder structure only ([Taxonomy](Taxonomy.md)), so a material can be recategorized without a rename.
- **A Character material uses the same name grammar, in its own folder** *(2026-10-14, Phase15, RD-P15-2, RD-P15-8)*: `materials/character/<species>/<part>/<name>.mtlx`, with species and part declared in the file too ([Taxonomy](Taxonomy.md) §Character). Moving the 30 there renamed nothing, so a scene that names one bare still resolves wherever the search path covers its folder. **The catalog `id` embeds the folder**, so theirs changed (`character/humanoid/skin/Skin_FitzpatrickIV_Clean_Base_s001`, was `biological/tissue/…`). Whether a contributor's name enters a Character material's name is Phase18's. **Answered 2026-10-15 (Phase18, RD-P18-3): it does not.** The name is the stable key (GPA-Q2), and a handle in it would change the key when the handle changes; the contributor is in the file (`contributor`) and shown wherever the entry is. A contributor names their look in the Variant token. **A fitted article's scale tag is `sUKN` when it tiles nothing** (RD-P18-8): its picture is drawn on a mesh's layout and has no real-world size. One that also tiles a detail (pores, say) keeps that tile's tag. *(The first two, 2026-10-15: `Teeth_Natural_Clean_Base_sUKN_v01`, `Eye_Green_Clean_Base_sUKN_v01`. A reader that parses the tag as `s` and digits must take `sUKN` too; the library's own did not until 18.4.)*
- **The bare name is the stable key; the catalog `id` is not** *(2026-10-14, the platform's ask GPA-Q2 in `docs/Planning/Research/261014_R_GroupsPlatformAsks.md`, written into the contract at the lead's word)*. A consumer that stores or recognises a library material (a bound instance in a saved scene, a wardrobe, a cache) keys it by its **bare file name** (`Skin_FitzpatrickIV_Clean_Base_s001_v01`). **The `id` embeds the folder, which says where the material is browsed, and the library may move it** (regrouping, recategorising: the 30 Character materials' `id`s changed in Phase15 while their names did not). The name survives such a move.
  - **A new `vNN` is a new name**, by design (§Two version axes): a scene naming `…_v01` keeps naming `v01`.
  - **A rename is a new article, not a move** *(the agent's reading of the existing lifecycle, 2026-10-14)*: the library does not rename a published material in place. A replacement gets its own name, and the old one is marked `deprecated` (*"kept for old scenes; prefer a newer material"*), so scenes naming it still resolve. **Reevaluate** if a rename in place is ever needed: it would break every scene that names the old one, and is a contract change, announced to consumers first.
- **Layer information goes *inside* `Condition` / `Detail`, never in extra tokens.** Which layers an article *carries* (its overlay and maskset textures) is recorded in its recipe and `.mtlx`, not the name. The name says only what is dialled up.
- **A see-through colour is a Creator setting** *(2026-10-05, Phase12; the lead's ruling, `docs/Planning/Phases/Complete/Phase12_GlassAndLightColour.md` RD-GLC-2)*: the port `transmission_color` ([LCDSchema](../Contract/LCDSchema.md)) sets the colour seen through glass, gems and liquids, so a green glass is a clear glass with that colour set. `base_color_tint` still does not reach it. **Judged 2026-10-05 (Phase12 click 5, the lead's pass):** `Glass_Clear` with the colour set stands in for `Glass_Green`, and `LED_CoolWhite` with its light's colour set is the same picture as `LED_WarmWhite`. The two colour-only articles are kept as authored and marked `Reevaluate (2026-10-05)` in their recipes and on the wish list; nothing is retired, renamed or deleted. *(Was: "`Glass_Green` stays as authored until that phase judges it.")* *(Superseded, kept for history: "**A see-through colour is its own authored article** (`Glass_Green`, not a tinted `Glass_Clear`): `base_color_tint` multiplies the surface colour only and does not reach `transmission_color`.")*
- **On TwoLayer articles** the maskset-driven second layer *is* the material, so `Condition` names the layer-2 state even at the library default (`Rust_OnSteel_Flaking_Base`).
- There is room for free variation while staying roughly readable — but always inside the charset/length budget below.

*(Updated 2026-09-25, lead rulings C4/C5/E1/E2/E5 in `docs/Planning/Research/260925_R_LibraryCoverage_FirstRelease.md`. Superseded, kept for history: Variant "a named variation (Veined, Clear, Brushed) — use `Base` if none"; Condition "surface condition (Distressed, Weathered)"; Detail "extra qualifier (Dusty, Scratched)". Shipped names predating the axes keep their names; `Marble_Veined_Polished_Base` and `Copper_Verdigris_Aged_Base` put a look word in the Condition slot.)*
- **Off-grammar articles.** A system material is exempt from the token grammar (but not from the length/charset budget). Today there is exactly one: **`IMRSV_MissingMaterial`** (master token `system`, see [MasterSet](MasterSet.md)); its historical name is kept. *(Updated 2026-09-23, measured: `tools/validators/validate_material.py` exempts `IMRSV_MissingMaterial` from the token-shape check and still applies length + charset to it.)* The manifest side of the exemption is owned by [Manifest](../Contract/Manifest.md).

## Name budget — ≤63 chars, `[A-Za-z0-9_]` (HARD CONSTRAINT, CI-checkable)

The whole name-keyed identity scheme rides on the material name **surviving Blender's USD export unchanged**. Two facts force a budget:

1. **Length:** Blender's `MAX_NAME` truncates material names at **63 bytes** (through Blender 5.1; the raise-to-258 proposal has not shipped). A truncated name fails to resolve.
2. **Charset:** spaces, dots, and hyphens **sanitize to `_` on USD export**, and two names that sanitize identically **silently collide** ([Blender #124263](https://projects.blender.org/blender/blender/issues/124263)). So the grammar must use only **`[A-Za-z0-9_]`**.

> **Reevaluate (2026-09-23):** the library now targets Blender 5.1+ (R6). If a later Blender raises `MAX_NAME`, the 63-byte budget still stands for as long as any supported Blender version truncates at 63 — re-check the limit when the minimum supported Blender version moves.

→ **Rule:** a Matter material filename stem is **≤63 characters** and uses only **`[A-Za-z0-9_]`**. CI-checkable; the per-work-item structural guard.

*(Updated 2026-09-23, measured: enforced today by the identity-grammar lane of `tools/validators/validate_material.py` (length > 63 and non-`[A-Za-z0-9_]` are errors), with the must-pass / must-fail cases below held in `tools/validators/fixtures/grammar_cases.json`.)*

**Documented must-fail** (the original library README's own example, **70 chars — over budget**, kept as a regression case):

```
Limestone26b_Veinish_VeryDistressed12_ScratchedButNotVeryDusty_s01_v32   ← 70 chars: REJECT
```

A conforming worst-case (≤63, identifier charset) is the must-pass:

```
Limestone26b_Veinish_VeryDistressed_Scratched_s01_v32                    ← 53 chars: PASS
```

## Scale tags

Every base texture uses a **real-world physical scale** — meters per UV tile — keeping detail consistent across renderers and giving artists a sane starting point. The scale tag (`s###`) appears in the base-texture-set folder name; the material filename carries the tag it was authored against.

| Scale Tag | Meters per Tile | Relative Detail | Typical Use |
|:---------:|:---------------:|:----------------|:------------|
| `s0001` | 0.001 m | Ultra-micro | Dust, pores, micro-scratches |
| `s001`  | 0.01 m  | Very fine | Fabric weave, paint texture, sand grains |
| `s01`   | 0.1 m   | Fine | Wood grain, brick clay, small tiles |
| `s1`    | 1 m     | Medium | Concrete, flooring, wall panels |
| `s10`   | 10 m    | Large | Terrain detail, large stone faces |
| `s100`  | 100 m   | Macro | Geological scale, landscapes, cliffs |
| `sUKN`  | Unknown | Unknown | Not defined / not relevant |

**An article's size is exactly its tag's length** *(2026-10-15, Phase19 D-9; the lead, RD-P19-2: "we should STRONGLY avoid fractions")*. Its `meters_per_tile` is 0.001, 0.01, 0.1, 1, 10 or 100, as its tag names, and an `sUKN` article authors `0.0`. A resolution option of an article keeps its size (RD-P19-1). **A source is never stretched to fit:** a scan whose real size is not a scale option is re-made at an option's size, or not used, and a generated texture is made at the option's size from the start. The `recipe` lane refuses a recipe off its tag; the 15 articles already off theirs are named there as known, each a redo row in `library/wishlist.yaml`.

**Shared layers (overlays and masksets) are sampled at the size their tag names** (Phase04, 2026-09-26; [MasterSet §Scale](MasterSet.md)). So a shared layer's tag is not a label but its rendered size: it is authored at exactly that size, and `sUKN` is not allowed on one. The assembler refuses an untagged or `sUKN` layer.

Changing what a scale tag *means* is a library semver-**major** change (see [_Architecture](../_Architecture.md) §Versioning).

## Two version axes (don't conflate)

| Axis | Versions what | Example | Driven by |
|------|---------------|---------|-----------|
| **Material version** (`vNN` in the name) | one individual asset | `Limestone_Veined_Clean_Base_s01_`**`v02`** | contributor |
| **Library release version** (semver) | the curated *set* as a whole | **Matter Library 1.3** | maintainer |

> **Reevaluate (2026-09-23):** the resolved identity is ambiguous about `vNN`. In the live articles the filename and the `<surfacematerial>` / nodegraph names carry `_vNN`, while the manifest and catalog `id` end at `sNN`, with the version as a separate field. This spec should state one rule for whether a composition's Matter identity includes the version. Owned by the release-bundle / consumer-contract phase (it touches what consumers resolve). See [MaterialXTemplate](../Contract/MaterialXTemplate.md).

The `vNN` in the filename pins the material; the **library release** (a [manifest](../Contract/Manifest.md) semver) pins the whole set for reproducibility. These are **separate axes** — a release manifest pins which `vNN` of each material it includes. See [Manifest](../Contract/Manifest.md) and [Catalog](../Catalog/Catalog.md).

## HDRI names

*(2026-10-14, Phase14; ruled in `docs/Planning/Research/261013_R_PlatformSkyAsks.md` RD-SKY-1 to RD-SKY-3.)* An [HDRI](../../Glossary.md) is a kind beside the taxonomy ([Taxonomy](Taxonomy.md)), so the material grammar does not fit it: it has no tile and so no scale tag.

- **Filename:** `<Name>_<Variant>_vNN.hdr`, in `MatterLibrary/hdris/` (one flat folder). PascalCase tokens, e.g. `IndustrialSunset02_PureSky_v01.hdr`.
- **Id and version:** the id is `<Name>_<Variant>`; `vNN` is the HDRI's own version, following §Two version axes (a changed picture is a new `vNN`). `id` + `version` resolve to the file, as a material's do.
- **Budget:** the same ≤63 characters of `[A-Za-z0-9_]`, unique within `hdris/`. A material's file cannot clash: the extension and the folder differ.
- **The file:** Radiance `.hdr` (RGBE), 4096 × 2048, 2:1 latitude-longitude. Any other format or size is refused (`tools/validators/validate_manifest.py` `check_hdri`). The format is part of the name a scene stores, so it is fixed.
- **A source's own id is not in the name.** It is in the HDRI's provenance record (`library/provenance/sources/hdris/<id>.yaml`).
- **What it says it is, in its own header** *(2026-10-14, Phase16, RD-P16-2, RD-P16-12)*. **A served copy** (the dev install's `releases/matterlib-dev/hdris/`; a release's, when one holds HDRIs) carries its facts as Radiance header lines after the source's own, before the blank line that ends the header. **The checkout keeps the source's bytes** (its `sha256` matches its record), so only a served copy is stamped; its pixels are the checkout's bytes. One line per fact, `MATTER_<FIELD>=<value>`, field names mirroring the [runtime catalog](../Contract/RuntimeCatalog.md)'s, in this order:
  - `MATTER_ID`, `MATTER_VERSION`, `MATTER_NAME` (the source's name), `MATTER_LICENCE`, `MATTER_CONTRIBUTOR`, `MATTER_GROUP` (`hdris`), `MATTER_WHEN`, `MATTER_SKY`;
  - `MATTER_CREDIT_SOURCE`, `MATTER_CREDIT_SOURCE_URL`, `MATTER_CREDIT_ASSET_URL`, `MATTER_CREDIT_EDITED_FROM_NAME`, `MATTER_CREDIT_EDITED_FROM_URL`;
  - `MATTER_CREDIT_AUTHOR` and `MATTER_CREDIT_SPONSOR`, **repeated once per author or sponsor**, each value one JSON object (`{"name": …, "role": …}`; `{"id": …, "name": …, "url": …}`).
  
  A fact the record does not hold has no line. Values are UTF-8 and never hold a line break. Left out: the source's description, its raw tags and the Markdown `edited_from` line (they are in the record and the site file). Readers skip header lines they do not know: Storm and Blender read a stamped copy pixel for pixel (Phase16 F-P16-1, and the 16.2 check on the default sky); Unreal's importer is checked on the machine with Unreal. Written by `tools/releases/hdris.py` (`stamp`, read back by `read_stamp`; `hdris.py stamp <id> <out>` writes one).

## Status

**Solid grammar, corrected for the name budget.** The grammar, defaults, and scale tags are carried unchanged from the library's original design; the ≤63-char / identifier-charset budget is the one hard correction (the original's own 70-char example is over).

**Data-versioning schemes (material `vNN`, release semver) are draft here** — frozen as contract when the manifest/catalog contract is frozen.

> **Reevaluate (2026-09-23):** both axes are already in use — `library/releases/` holds `matterlib-0.0.1` and `matterlib-0.1.0` manifests that pin a `vNN` per article (every article is `v01` today). Whether that pilot use freezes the schemes, or the freeze waits for the release-bundle contract (R14), is for the release-bundle / consumer-contract phase to decide.

## History

- The filename grammar, the `Clean` / `Base` defaults and the scale-tag table come from the library's original README, carried unchanged.
- 2026-06 — the name budget was added after measuring two Blender USD-export facts: material names truncate at 63 bytes, and spaces / dots / hyphens sanitize to `_`, so distinct names can collide. The original README's own 70-character example name was over budget; it is kept as the must-fail regression case.
- 2026-09-25 — each token became a fixed axis (Material = matter/species · Variant = the look · Condition = damage · Detail = the other layers), the default Variant became `Natural`, and exactly six tokens became a validator rule (it previously accepted ≥ 4). All shipped names already had six. (Lead rulings, `260925_R_LibraryCoverage_FirstRelease.md`.)
