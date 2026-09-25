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
- **Layer information goes *inside* `Condition` / `Detail`, never in extra tokens.** Which layers an article *carries* (its overlay and maskset textures) is recorded in its recipe and `.mtlx`, not the name. The name says only what is dialled up.
- **A see-through colour is its own authored article** (`Glass_Green`, not a tinted `Glass_Clear`): `base_color_tint` multiplies the surface colour only and does not reach `transmission_color`.
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

Changing what a scale tag *means* is a library semver-**major** change (see [_Architecture](../_Architecture.md) §Versioning).

## Two version axes (don't conflate)

| Axis | Versions what | Example | Driven by |
|------|---------------|---------|-----------|
| **Material version** (`vNN` in the name) | one individual asset | `Limestone_Veined_Clean_Base_s01_`**`v02`** | contributor |
| **Library release version** (semver) | the curated *set* as a whole | **Matter Library 1.3** | maintainer |

> **Reevaluate (2026-09-23):** the resolved identity is ambiguous about `vNN`. In the live articles the filename and the `<surfacematerial>` / nodegraph names carry `_vNN`, while the manifest and catalog `id` end at `sNN`, with the version as a separate field. This spec should state one rule for whether a composition's Matter identity includes the version. Owned by the release-bundle / consumer-contract phase (it touches what consumers resolve). See [MaterialXTemplate](../Contract/MaterialXTemplate.md).

The `vNN` in the filename pins the material; the **library release** (a [manifest](../Contract/Manifest.md) semver) pins the whole set for reproducibility. These are **separate axes** — a release manifest pins which `vNN` of each material it includes. See [Manifest](../Contract/Manifest.md) and [Catalog](../Catalog/Catalog.md).

## Status

**Solid grammar, corrected for the name budget.** The grammar, defaults, and scale tags are carried unchanged from the library's original design; the ≤63-char / identifier-charset budget is the one hard correction (the original's own 70-char example is over).

**Data-versioning schemes (material `vNN`, release semver) are draft here** — frozen as contract when the manifest/catalog contract is frozen.

> **Reevaluate (2026-09-23):** both axes are already in use — `library/releases/` holds `matterlib-0.0.1` and `matterlib-0.1.0` manifests that pin a `vNN` per article (every article is `v01` today). Whether that pilot use freezes the schemes, or the freeze waits for the release-bundle contract (R14), is for the release-bundle / consumer-contract phase to decide.

## History

- The filename grammar, the `Clean` / `Base` defaults and the scale-tag table come from the library's original README, carried unchanged.
- 2026-06 — the name budget was added after measuring two Blender USD-export facts: material names truncate at 63 bytes, and spaces / dots / hyphens sanitize to `_`, so distinct names can collide. The original README's own 70-character example name was over budget; it is kept as the must-fail regression case.
- 2026-09-25 — each token became a fixed axis (Material = matter/species · Variant = the look · Condition = damage · Detail = the other layers), the default Variant became `Natural`, and exactly six tokens became a validator rule (it previously accepted ≥ 4). All shipped names already had six. (Lead rulings, `260925_R_LibraryCoverage_FirstRelease.md`.)
