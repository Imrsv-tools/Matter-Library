# Research — Library Coverage: the first-release material list (draft v1)

**Opened:** 2026-09-25 · **Mode:** research — gathers, commits to nothing · **Next:** the lead gut-checks names and structure (§Gut-check questions)

**Question:** what, concretely, are the ~170 articles of an excellent first library — each with its full name and place in the tree — so the names, the class boundaries and the blockers can be checked before anything is built?

**Extends, does not replace:** `260923_R_AgenticMaterialGeneration.md` Pass 11 (the per-class *targets*) and D1–D7; `260923_R_StandaloneSetup.md` seed 9. The Roadmap entry is **Library Coverage — RESEARCH**. Phase03 deliberately leaves filling the library out of scope and hands this entry its tools.

**Sources examined (2026-09-25):** `docs/specs/Ontology/{Identity,Taxonomy,MasterSet}.md`, `docs/NamingConventions.md`, `docs/Glossary.md` (Article, Overlay, Maskset), `260923_R_AgenticMaterialGeneration.md` (Resolved, Passes 8–12, Open questions, Status), the tracked tree `MatterLibrary/materials/**` and `MatterLibrary/textures/shared/**`.

---

## Pass 1 — The rules each name was written against

**Grammar** (`Identity.md`): `Material_Variant_Condition_Detail_sNN_vNN.mtlx`, ≤63 chars of `[A-Za-z0-9_]`, PascalCase tokens. `Condition` defaults to `Clean`, `Detail` to `Base`. Domain/Class live in the folder only.

**Precedent read from the 11 shipped articles** (the conventions this draft follows; each is a gut-check item in §Gut-check questions if it looks wrong):

| Precedent | Reading | Applied here as |
|---|---|---|
| `Limestone_…`, `ABS_…`, `Lace_…`, `Copper_…` | `Material` = the **most specific** substance name (species, alloy, polymer, fabric), not the class | `Oak_…`, not `Wood_Oak_…` |
| `Marble_Veined_Polished_Base` | a surface **finish** sits in `Condition` | `Granite_Speckled_Polished_Base` |
| Identity.md example "Brushed" as a Variant | a **structural** variation sits in `Variant` | `Aluminium_Brushed_Clean_Base` |
| `Rust_OnSteel_Flaking_Base` (TwoLayer) | a layer-on-substrate article names the top layer and `On<Substrate>` | `Paint_OnWood_Peeling_Base` |
| `Glass_Clear_…_s01`, `Diamond_…_s01`, `Neon_…_s01` | param-only (L1) articles still carry `s01` | L1 rows below use `s01` |
| every article is `v01` | first version | every row is `_v01` (omitted from the tables for width; **append `_v01.mtlx`**) |

**Depth per matter, not volume** (Pass 11 of the prior thread): Condition/Detail variants are kept rare, because the Creator-tier tint, UV and roughness controls plus overlays and masksets already span most conditions. A Condition appears only where the condition changes the *matter's* look beyond what an overlay does (wet, weathered, peeling).

**Matter only (D1):** no walls, floors, tiles, paving, corrugated sheet or diamond plate — their substance is listed instead.

## Pass 2 — The list

**Columns:** `Path` = `MatterLibrary/materials/<domain>/<class>/` + the stem (append `_v01.mtlx`). **Master** = the article's declared master (D2: the material decides, the class is only a default). **Lane:** L1 param-only grounded in Physically Based · L2 agent-written procedural texture · L3 ambientCG CC0 scan. **Status:**

- ✅ **shipped** (in `matterlib-0.1.0`)
- **Now** — buildable with no contract change
- **Now·C1** — buildable, but a measured metal wants the F82 `specular_color` carrier to be accurate (open O5)
- **C2** — blocked on the coat/sheen carrier (the look *is* the coat or the sheen)
- **C3** — blocked on the anisotropy carrier
- **O11** — class boundary undecided; the row's home is provisional
- **D1?** — may be an assembly rather than matter; lead's call

*Physically Based record names are unverified per row; Pass 9 of the prior thread confirmed the category counts (Metal 32, Crystal 10, Liquid 19, Manmade 22, Plastic 7), not each entry. ambientCG availability per row is by category (Pass 9), not by named set.*

### 🪨 natural

**natural/stone** — 15

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Limestone_Veined_Clean_Base_s01` | Opaque | L3 | s01 | ✅ |
| 2 | `Marble_Veined_Polished_Base_s01` | Subsurface | L3 | s01 | ✅ |
| 3 | `Marble_Carrara_Honed_Base_s1` | Subsurface | L3 | s1 | Now |
| 4 | `Granite_Speckled_Polished_Base_s1` | Opaque | L3 | s1 | Now |
| 5 | `Granite_Grey_Weathered_Base_s1` | Opaque | L3 | s1 | Now |
| 6 | `Sandstone_Layered_Weathered_Base_s1` | Opaque | L3 | s1 | Now |
| 7 | `Slate_Cleft_Clean_Base_s1` | Opaque | L3 | s1 | Now |
| 8 | `Basalt_Dark_Clean_Base_s1` | Opaque | L3 | s1 | Now |
| 9 | `Travertine_Pitted_Honed_Base_s1` | Opaque | L3 | s1 | Now |
| 10 | `Quartzite_White_Clean_Base_s1` | Opaque | L3 | s1 | Now |
| 11 | `Lava_Porous_Clean_Base_s1` | Opaque | L3 | s1 | Now |
| 12 | `Limestone_Cliff_Weathered_Base_s10` | Opaque | L3 | s10 | Now |
| 13 | `Onyx_Banded_Polished_Base_s01` | Subsurface | L3 | s01 | Now |
| 14 | `Jade_Nephrite_Polished_Base_s01` | Subsurface | L2 | s01 | Now |
| 15 | `Obsidian_Black_Polished_Base_s01` | Opaque | L1 | s01 | Now |

**natural/wood** — 15

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Oak_White_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 2 | `Oak_White_Weathered_Base_s01` | Opaque | L3 | s01 | Now |
| 3 | `Oak_White_Varnished_Base_s01` | Opaque | L3 | s01 | C2 |
| 4 | `Walnut_Black_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 5 | `Maple_Hard_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 6 | `Pine_Knotty_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 7 | `Birch_Plain_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 8 | `Cherry_Black_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 9 | `Teak_Plain_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 10 | `Ash_White_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 11 | `Cedar_Red_Weathered_Base_s01` | Opaque | L3 | s01 | Now |
| 12 | `Driftwood_Bleached_Weathered_Base_s01` | Opaque | L3 | s01 | Now |
| 13 | `Bamboo_Natural_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 14 | `Bark_Pine_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 15 | `Cork_Natural_Clean_Base_s001` | Opaque | L3 | s001 | Now |

**natural/soil** — 10

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Loam_Dark_Clean_Base_s1` | Opaque | L3 | s1 | Now |
| 2 | `Loam_Dark_Wet_Base_s1` | Opaque | L3 | s1 | Now |
| 3 | `Topsoil_Forest_Clean_Base_s1` | Opaque | L3 | s1 | Now |
| 4 | `Clay_Red_Dry_Cracked_s1` | Opaque | L3 | s1 | Now |
| 5 | `Clay_Grey_Wet_Base_s1` | Opaque | L3 | s1 | Now |
| 6 | `Mud_Brown_Wet_Base_s1` | Opaque | L3 | s1 | Now |
| 7 | `Peat_Fibrous_Clean_Base_s1` | Opaque | L3 | s1 | Now |
| 8 | `Laterite_Red_Clean_Base_s1` | Opaque | L3 | s1 | Now |
| 9 | `Silt_River_Wet_Base_s1` | Opaque | L3 | s1 | Now |
| 10 | `Loess_Pale_Dry_Base_s1` | Opaque | L3 | s1 | Now |

**natural/mineral** — 8

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Diamond_Brilliant_Clean_Base_s01` | TranslucentThick | L1 | s01 | ✅ |
| 2 | `Sapphire_Blue_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now |
| 3 | `Ruby_Deep_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now |
| 4 | `Emerald_Green_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now |
| 5 | `Amethyst_Purple_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now |
| 6 | `Quartz_Clear_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now |
| 7 | `Nacre_Iridescent_Polished_Base_s01` | Opaque | L3 | s01 | Now † |
| 8 | `Ivory_Aged_Clean_Base_s01` | Opaque | L3 | s01 | Now · O11 |

† Iridescence needs a thin-film carrier, which is **not** one of C1–C3. Without it, nacre renders as pearl-white and the critique must say so. *(New finding: a fourth carrier candidate, thin film; Physically Based carries `thinFilmIor`/`thinFilmThickness`.)*

### ⚙️ engineered

**engineered/metal** — 20

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Copper_Verdigris_Aged_Base_s01` | Opaque | L3 | s01 | ✅ |
| 2 | `Rust_OnSteel_Flaking_Base_s01` | TwoLayer | L3 | s01 | ✅ |
| 3 | `Gold_Pure_Polished_Base_s01` | Opaque | L1 | s01 | Now·C1 |
| 4 | `Silver_Sterling_Polished_Base_s01` | Opaque | L1 | s01 | Now·C1 |
| 5 | `Copper_Pure_Polished_Base_s01` | Opaque | L1 | s01 | Now·C1 |
| 6 | `Brass_Yellow_Polished_Base_s01` | Opaque | L1 | s01 | Now·C1 |
| 7 | `Bronze_Cast_Aged_Base_s01` | Opaque | L3 | s01 | Now |
| 8 | `Aluminium_Raw_Clean_Base_s01` | Opaque | L1 | s01 | Now·C1 |
| 9 | `Aluminium_Brushed_Clean_Base_s001` | Opaque | L2 | s001 | C3 |
| 10 | `StainlessSteel_Polished_Clean_Base_s01` | Opaque | L1 | s01 | Now·C1 |
| 11 | `StainlessSteel_Brushed_Clean_Base_s001` | Opaque | L2 | s001 | C3 |
| 12 | `Chrome_Mirror_Polished_Base_s01` | Opaque | L1 | s01 | Now·C1 |
| 13 | `Titanium_Raw_Clean_Base_s01` | Opaque | L1 | s01 | Now·C1 |
| 14 | `Steel_Mild_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 15 | `Steel_Galvanised_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 16 | `Steel_Corten_Weathered_Base_s01` | Opaque | L3 | s01 | Now |
| 17 | `Steel_Perforated_Clean_Base_s01` | Masked | L3 | s01 | Now · D1? |
| 18 | `Iron_Cast_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 19 | `Iron_Wrought_Aged_Base_s01` | Opaque | L3 | s01 | Now |
| 20 | `Lead_Grey_Aged_Base_s01` | Opaque | L3 | s01 | Now |

**engineered/glass** — 6

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Glass_Clear_Clean_Base_s01` | TranslucentThin | L1 | s01 | ✅ |
| 2 | `Glass_Frosted_Clean_Base_s01` | TranslucentThin | L1 | s01 | Now |
| 3 | `Glass_Green_Clean_Base_s01` | TranslucentThin | L1 | s01 | Now |
| 4 | `Glass_Amber_Clean_Base_s01` | TranslucentThin | L1 | s01 | Now |
| 5 | `Glass_Reeded_Clean_Base_s001` | TranslucentThin | L2 | s001 | Now |
| 6 | `Glass_LeadCrystal_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now |

**engineered/cementitious** — 10

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Concrete_Smooth_Worn_Dusty_s1` | Opaque | L3 | s1 | ✅ |
| 2 | `Concrete_BoardFormed_Clean_Base_s1` | Opaque | L3 | s1 | Now |
| 3 | `Concrete_Grey_Polished_Base_s1` | Opaque | L3 | s1 | Now |
| 4 | `Concrete_Aggregate_Weathered_Base_s1` | Opaque | L3 | s1 | Now |
| 5 | `Concrete_Smooth_Weathered_Stained_s1` | Opaque | L3 | s1 | Now |
| 6 | `Plaster_Smooth_Clean_Base_s1` | Opaque | L3 | s1 | Now |
| 7 | `Stucco_Rough_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 8 | `Terrazzo_Chipped_Polished_Base_s01` | Opaque | L3 | s01 | Now |
| 9 | `Asphalt_Fresh_Clean_Base_s1` | Opaque | L3 | s1 | Now · O11 |
| 10 | `Asphalt_Aged_Worn_Cracked_s1` | Opaque | L3 | s1 | Now · O11 |

**engineered/ceramic** — 8

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Terracotta_Unglazed_Clean_Base_s01` | Opaque | L1 | s01 | Now |
| 2 | `Terracotta_Glazed_Clean_Base_s01` | Opaque | L3 | s01 | C2 |
| 3 | `BrickClay_Red_Clean_Base_s01` | Opaque | L1 | s01 | Now |
| 4 | `Fireclay_Buff_Clean_Base_s01` | Opaque | L2 | s01 | Now |
| 5 | `Earthenware_Red_Clean_Base_s01` | Opaque | L2 | s01 | Now |
| 6 | `Stoneware_SpeckledGlaze_Clean_Base_s01` | Opaque | L2 | s01 | C2 |
| 7 | `Porcelain_Bisque_Clean_Base_s01` | Opaque | L1 | s01 | Now |
| 8 | `Porcelain_Glazed_Clean_Base_s01` | Opaque | L1 | s01 | C2 |

**engineered/composite** — 8 *(the whole class is O11: its boundary is not written)*

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Plywood_Birch_Clean_Base_s01` | Opaque | L3 | s01 | Now · O11 |
| 2 | `MDF_Raw_Clean_Base_s01` | Opaque | L3 | s01 | Now · O11 |
| 3 | `Chipboard_Raw_Clean_Base_s01` | Opaque | L3 | s01 | Now · O11 |
| 4 | `Cardboard_Kraft_Clean_Base_s01` | Opaque | L3 | s01 | Now · O11 |
| 5 | `Paper_White_Clean_Base_s001` | Opaque | L3 | s001 | Now · O11 |
| 6 | `CarbonFibre_Twill_Clean_Base_s001` | Opaque | L2 | s001 | Now · O11 |
| 7 | `Fibreglass_Chopped_Clean_Base_s01` | Opaque | L2 | s01 | Now · O11 |
| 8 | `Laminate_Matte_Clean_Base_s01` | Opaque | L2 | s01 | Now · O11 |

### 🧪 synthetic

**synthetic/plastic** — 10

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `ABS_Matte_Clean_Base_s01` | Opaque | L1 | s01 | ✅ |
| 2 | `ABS_Glossy_Clean_Base_s01` | Opaque | L1 | s01 | Now |
| 3 | `Polypropylene_White_Clean_Base_s01` | Opaque | L1 | s01 | Now |
| 4 | `PVC_Grey_Clean_Base_s01` | Opaque | L1 | s01 | Now |
| 5 | `HDPE_Natural_Clean_Base_s01` | Opaque | L1 | s01 | Now |
| 6 | `Polystyrene_HighImpact_Clean_Base_s01` | Opaque | L1 | s01 | Now · O11 |
| 7 | `Bakelite_Brown_Polished_Base_s01` | Opaque | L1 | s01 | Now · O11 |
| 8 | `Acrylic_Clear_Clean_Base_s01` | TranslucentThin | L1 | s01 | Now |
| 9 | `Polycarbonate_Clear_Clean_Base_s01` | TranslucentThin | L1 | s01 | Now |
| 10 | `PET_Clear_Clean_Base_s01` | TranslucentThin | L1 | s01 | Now |

**synthetic/polymer** — 7 *(plastic vs polymer is O11; the working split used here is "rigid → plastic; elastic, foamed, cast or waxy → polymer")*

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Rubber_Black_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 2 | `Neoprene_Black_Clean_Base_s001` | Opaque | L3 | s001 | Now |
| 3 | `Silicone_Translucent_Clean_Base_s01` | Subsurface | L1 | s01 | Now |
| 4 | `Polyurethane_Foam_Clean_Base_s001` | Opaque | L3 | s001 | Now |
| 5 | `Polystyrene_Expanded_Clean_Base_s001` | Opaque | L3 | s001 | Now · O11 |
| 6 | `Epoxy_Clear_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now |
| 7 | `Wax_Paraffin_Clean_Base_s01` | Subsurface | L1 | s01 | Now · O11 |

**synthetic/textile** — 12 *(cloth without sheen reads acceptably; velvet, satin and suede do not)*

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Lace_Floral_Clean_Base_s01` | Masked | L3 | s01 | ✅ |
| 2 | `Canvas_Natural_Clean_Base_s001` | Opaque | L3 | s001 | Now |
| 3 | `Denim_Indigo_Clean_Base_s001` | Opaque | L3 | s001 | Now |
| 4 | `Linen_Natural_Clean_Base_s001` | Opaque | L3 | s001 | Now |
| 5 | `Tweed_Grey_Clean_Base_s001` | Opaque | L3 | s001 | Now |
| 6 | `Burlap_Jute_Clean_Base_s001` | Opaque | L3 | s001 | Now |
| 7 | `Felt_Grey_Clean_Base_s001` | Opaque | L3 | s001 | Now |
| 8 | `Nylon_Ripstop_Clean_Base_s001` | Opaque | L3 | s001 | Now |
| 9 | `Leather_Brown_Clean_Base_s01` | Opaque | L3 | s01 | Now · O9? |
| 10 | `Suede_Tan_Clean_Base_s001` | Opaque | L3 | s001 | C2 |
| 11 | `Velvet_Crimson_Clean_Base_s001` | Opaque | L3 | s001 | C2 |
| 12 | `Satin_Ivory_Clean_Base_s001` | Opaque | L2 | s001 | C2 + C3 |

**synthetic/coating** — 8

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Paint_Matte_Clean_Base_s01` | Opaque | L1 | s01 | Now |
| 2 | `Paint_Satin_Clean_Base_s01` | Opaque | L1 | s01 | Now |
| 3 | `Paint_Gloss_Clean_Base_s01` | Opaque | L1 | s01 | C2 |
| 4 | `Paint_OnWood_Peeling_Base_s01` | TwoLayer | L3 | s01 | Now |
| 5 | `Paint_OnMetal_Chipped_Base_s01` | TwoLayer | L3 | s01 | Now |
| 6 | `PowderCoat_Textured_Clean_Base_s001` | Opaque | L2 | s001 | Now |
| 7 | `Enamel_Gloss_Clean_Base_s01` | Opaque | L1 | s01 | C2 |
| 8 | `CarPaint_Metallic_Clean_Base_s001` | Opaque | L2 | s001 | C1 + C2 |

### 🌫️ environmental

**environmental/sand** — 6

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Sand_Beach_Dry_Base_s1` | Opaque | L3 | s1 | Now |
| 2 | `Sand_Beach_Wet_Base_s1` | Opaque | L3 | s1 | Now |
| 3 | `Sand_Desert_Rippled_Base_s1` | Opaque | L3 | s1 | Now |
| 4 | `Sand_Volcanic_Clean_Base_s1` | Opaque | L3 | s1 | Now |
| 5 | `Gravel_Pea_Clean_Base_s1` | Opaque | L3 | s1 | Now · O11 |
| 6 | `Gravel_Crushed_Clean_Base_s1` | Opaque | L3 | s1 | Now · O11 |

**environmental/vegetation** — 6

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Grass_Lawn_Clean_Base_s1` | Opaque | L3 | s1 | Now |
| 2 | `Moss_Green_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 3 | `Lichen_Crustose_Clean_Base_s01` | Opaque | L2 | s01 | Now |
| 4 | `LeafLitter_Autumn_Clean_Base_s1` | Opaque | L3 | s1 | Now |
| 5 | `Straw_Dry_Clean_Base_s01` | Opaque | L3 | s01 | Now |
| 6 | `Leaf_Oak_Clean_Base_s01` | Masked | L3 | s01 | Now ‡ |

‡ A leaf card is Masked today; the two-sided thin-transmission *foliage variant* is `(planned)` in `MasterSet.md`.

**environmental/liquid** — 8

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Water_Clear_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now |
| 2 | `Water_Sea_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now |
| 3 | `Water_Murky_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now |
| 4 | `Honey_Amber_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now |
| 5 | `Wine_Red_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now |
| 6 | `Oil_Motor_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now |
| 7 | `Milk_Whole_Clean_Base_s01` | Subsurface | L1 | s01 | Now |
| 8 | `Coffee_Black_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now |

**Frozen water — home undecided (O11), 2 articles not counted in any class above:**

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Snow_Fresh_Clean_Base_s1` | Subsurface | L3 | s1 | O11 |
| 2 | `Ice_Clear_Clean_Base_s01` | TranslucentThick | L3 | s01 | O11 |

### 💡 utility

**utility/emissive** — 6

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Neon_Signage_Clean_Base_s01` | Emissive | L1 | s01 | ✅ |
| 2 | `LED_WarmWhite_Clean_Base_s01` | Emissive | L1 | s01 | Now |
| 3 | `LED_CoolWhite_Clean_Base_s01` | Emissive | L1 | s01 | Now |
| 4 | `Tungsten_Filament_Clean_Base_s01` | Emissive | L1 | s01 | Now |
| 5 | `Phosphor_Green_Clean_Base_s01` | Emissive | L1 | s01 | Now |
| 6 | `Lava_Molten_Clean_Base_s1` | Emissive | L2 | s1 | Now · O11 |

**utility/virtual** — 5 *(plus the system article `IMRSV_MissingMaterial`, which is outside the grammar and not counted)*

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Diagnostic_UVGrid_Clean_Base_s1` | Opaque | L2 | s1 | ✅ |
| 2 | `Diagnostic_Checker_Clean_Base_s1` | Opaque | L2 | s1 | Now |
| 3 | `GreyCard_Neutral18_Clean_Base_s01` | Opaque | L1 | s01 | Now |
| 4 | `Spectralon_White_Clean_Base_s01` | Opaque | L1 | s01 | Now |
| 5 | `MusouBlack_Matte_Clean_Base_s01` | Opaque | L1 | s01 | Now |

*Rows 3–5 are the Physically Based calibration references (Pass 9 of the prior thread) — the natural anchors for the **Parity Baselines** Roadmap entry.*

**utility/energy** — 3 *(animated plasma is out of scope; these are static, pre-authored looks)*

| # | Stem | Master | Lane | Scale | Status |
|---|---|---|---|---|---|
| 1 | `Plasma_Blue_Clean_Base_s01` | Emissive | L2 | s01 | Now |
| 2 | `Hologram_Cyan_Clean_Base_s01` | Emissive | L2 | s01 | Now |
| 3 | `Forcefield_Hex_Clean_Base_s01` | Emissive | L2 | s01 | Now |

### Not in the list: biological matter (O9)

Skin (Physically Based carries 6 Fitzpatrick types with subsurface data), hair, bone and nails have **no class**, and hair is not a surface material in this model. They are the platform's one live pull (`PlatformDependencies.md` M1). Leather (textile #9) and ivory (mineral #8) sit on the same boundary.

### Shared overlays and masksets (~8 each), names following the shipped `<Name><NN>_overlay_sNN` / `<Name><NN>_sNN` form

- **Overlays** (`textures/shared/overlays/`): `Dust01` ✅ · `Scratches01` ✅ · `Fingerprints01` · `Smudge01` · `WaterSpots01` · `EdgeWear01` · `Pitting01` · `HairlineScratches01`
- **Masksets** (`textures/shared/masks/`): `Grime01` ✅ · `RustBloom01` ✅ · `Verdigris01` ✅ · `PaintPeel01` · `PaintChip01` · `Moss01` · `WaterStain01` · `Efflorescence01`

## Pass 3 — What the list shows

**Tally (counted from the tables, 2026-09-25):**

| Status | Count | Notes |
|---|---|---|
| ✅ shipped | 11 | + `IMRSV_MissingMaterial` (not counted) |
| Now | 140 | 20 of these carry an O11 / O9 / D1 tag: their *class folder* may change, not whether they can be built |
| Now·C1 | 8 | clean L1 metals; ship approximated, or wait for F82 |
| C2 | 10 | incl. satin (C2 + C3) and car paint (C1 + C2) |
| C3 | 3 | brushed aluminium, brushed stainless, satin |
| O11 (unplaced) | 2 | snow, ice |
| **Total** | **173** (11 shipped + 162 new) **+ 16 overlays/masksets** (5 shipped) | Pass 11's target was ~170 |

*(C2 and C3 overlap on satin, so the rows sum to 173, not 174.)*

**Findings:**
- **140 new articles need nothing but the Phase03 tools.** The prior thread estimated ~110; the difference is D2 (the material chooses its master), which turned every "routing" blocker into a buildable row.
- **C2 (coat/sheen) is the most valuable carrier.** It unblocks 10 articles across ceramic, wood, textile and coating. C3 unblocks 3. C1 turns 8 approximations into measured metals.
- **A fourth carrier appears: thin film** (nacre, and later soap film and oil sheen). It is not in C1–C3. *(New open question L3.)*
- **The class-boundary rulings (O11) matter more than they looked:** 22 rows (20 tagged + snow and ice) carry a provisional home. `Polystyrene` appears in both plastic and polymer, which is the plainest example.
- **Names:** every stem is within 63 chars (the longest, `StainlessSteel_Brushed_Clean_Base_s001`, is 38). Nothing here tests the budget.

## Gut-check questions — for the lead

Naming (each has a recommendation; this draft already follows it):

| # | Question | Draft follows | Alternative |
|---|---|---|---|
| N1 | `Material` = the most specific substance (`Oak`, `Denim`, `ABS`)? | yes (precedent: `Limestone`, `Lace`, `ABS`) | class-word first: `Wood_Oak`, `Fabric_Denim` |
| N2 | A two-word substance is one token (`StainlessSteel`, `CarbonFibre`, `BrickClay`)? | yes | `Steel_Stainless…`, which uses up the Variant slot |
| N3 | British spelling (`Aluminium`, `Fibre`, `Grey`, `Galvanised`)? | yes (the docs write "colour") | US spelling. **Either way, write it into `NamingConventions.md`**, since names are permanent after release |
| N4 | A finish (Polished, Honed, Weathered, Wet) goes in `Condition`; a structure (Brushed, Veined, Reeded) goes in `Variant`? | yes (precedent: `Marble_Veined_Polished`) | — |
| N5 | A colour word in `Variant` only when the colour *is* the matter (`Sapphire_Blue`, `Glass_Green`), never for paint or plastic, where colour is the Creator tint? | yes | — |
| N6 | Param-only (L1) articles carry `s01`, as the shipped ones do? | yes | `sUKN` (more honest: there is no texture to scale) |
| N7 | Layered articles use `<Top>_On<Substrate>` (`Paint_OnWood`, after `Rust_OnSteel`)? | yes | — |

Structure (O11 rulings this list needs; no recommendation forced):

| # | Question | Rows affected |
|---|---|---|
| S1 | Where do **snow and ice** live? (a new `environmental/frozen`? `liquid` renamed `water`?) | 2 |
| S2 | **Plastic vs polymer**: is "rigid → plastic; elastic, foamed, cast, waxy → polymer" the rule? | ~5 |
| S3 | **Composite**: engineered boards, paper and fibre-reinforced materials? Or do plywood and MDF go under wood? | 8 |
| S4 | **Asphalt** in cementitious (bitumen binds it, not cement)? **Gravel** in sand? **Molten lava** in emissive? | 5 |
| S5 | Is **perforated steel** matter or an assembly (D1)? MasterSet names it as the Masked metal. | 1 |
| S6 | Do the **energy** looks belong in the library at all, or in a future effects domain like `atmospheric`? | 3 |

## Open questions

| # | Question | Why it matters |
|---|---|---|
| L1 | Naming rulings N1–N7 | Names are permanent once released (immutability). |
| L2 | Structure rulings S1–S6 (the rest of O11) | 22 rows have a provisional class. |
| L3 | Is **thin film** a fourth carrier (C4)? | Nacre, and later soap bubble and oil sheen. |
| L4 | Ship the 8 C1 metals approximated in the first release, or hold them for F82? | Metals are the class users reach for first. |
| L5 | Is this the **first release**, or the eventual coverage target? At 5–10 min review each (unmeasured), 162 new articles is roughly 15–25 hours. | Decides whether to cut a smaller first tranche. |

## Status

**Passes captured:** 3 (2026-09-25).

- **Draft v1 of the list is complete:** 173 named articles (11 shipped, 162 new) across all 20 classes, including 2 unplaced (snow, ice), plus 16 overlays/masksets. Every row has a full stem, a folder, a declared master, a lane, a scale tag and a status.
- **140 new articles are buildable with the Phase03 tools alone** (20 of them in a provisional class). The rest wait on carriers C2 (10), C3 (3), optionally C1 (8), or a class ruling (snow, ice).
- **Direction:** nothing is committed. This is input for the lead's gut check, and later for the *Library Coverage* phase.
- **Open:** L1–L5. None blocks Phase03.
- **Next step:** the lead marks up the list (rename, cut, add, move), and rules N1–N7 and S1–S6 where they have a view. The naming rulings then land in `NamingConventions.md` / `Identity.md` through a `/quick-fix`, and the class rulings in `Taxonomy.md`. A later pass here re-issues the list as v2.
