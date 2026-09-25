# Research — Library Coverage: the first-release material list (draft v1)

**Opened:** 2026-09-25 · **Mode:** research — gathers, commits to nothing · **Next:** the lead gut-checks names and structure (§Gut-check questions)

**Question:** what, concretely, are the ~170 articles of an excellent first library — each with its full name and place in the tree — so the names, the class boundaries and the blockers can be checked before anything is built?

**Extends, does not replace:** `260923_R_AgenticMaterialGeneration.md` Pass 11 (the per-class *targets*) and D1–D7; `260923_R_StandaloneSetup.md` seed 9. The Roadmap entry is **Library Coverage — RESEARCH**. Phase03 deliberately leaves filling the library out of scope and hands this entry its tools.

**Sources examined (2026-09-25):** `docs/specs/Ontology/{Identity,Taxonomy,MasterSet}.md`, `docs/NamingConventions.md`, `docs/Glossary.md` (Article, Overlay, Maskset), `260923_R_AgenticMaterialGeneration.md` (Resolved, Passes 8–12, Open questions, Status), the tracked tree `MatterLibrary/materials/**` and `MatterLibrary/textures/shared/**`.

---

## Resolved — lead decisions

| # | Decision |
|---|---|
| C1 | **Every article carries all of its relevant overlays and masks: "smart, not lean"** (lead, 2026-09-25). "We are building and testing complex materials, not just a bunch of wood textures." The layers ship in every article with their sliders defaulted to **0**, so the article reads as its name says (`Clean`) and the app dials the wear up. **Names do not change.** Leaving out a relevant layer is not an option. An article carries no layer only where none is relevant (the `utility/virtual` references). *Blast radius: Phase03's skill and recipe schema must author these layers, and every shipped article without them needs a new version. See Pass 4.* |

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

**Wear layers (added in Pass 4, ruling C1):** `Overlay 1 · Overlay 2 · Mask` = the shared layers the article carries, all at default strength 0. The mask gates *where* each overlay may appear (G/B channels) and, on TwoLayer, where layer 2 sits (R). **Also wanted** = relevant layers the article cannot carry today: **`+X`** is a third overlay the 2-overlay cap leaves out; **`~X`** is an effect overlays cannot express, because an overlay may only bend the normal and *roughen* (never smooth, never colour).

*Physically Based record names are unverified per row; Pass 9 of the prior thread confirmed the category counts (Metal 32, Crystal 10, Liquid 19, Manmade 22, Plastic 7), not each entry. ambientCG availability per row is by category (Pass 9), not by named set.*

### 🪨 natural

**natural/stone** — 15

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Limestone_Veined_Clean_Base_s01` | Opaque | L3 | s01 | ✅ | Dust01 · EdgeWear01 · Crevice01 | ~Wet · ~Moss |
| 2 | `Marble_Veined_Polished_Base_s01` | Subsurface | L3 | s01 | ✅ | Scratches01 · Dust01 · Crevice01 | ~Wet · +WaterSpots01 |
| 3 | `Marble_Carrara_Honed_Base_s1` | Subsurface | L3 | s1 | Now | Scratches01 · Dust01 · Crevice01 | ~Wet · +WaterSpots01 |
| 4 | `Granite_Speckled_Polished_Base_s1` | Opaque | L3 | s1 | Now | Scratches01 · Dust01 · Crevice01 | ~Wet · +WaterSpots01 |
| 5 | `Granite_Grey_Weathered_Base_s1` | Opaque | L3 | s1 | Now | Dust01 · EdgeWear01 · Crevice01 | ~Wet · ~Moss |
| 6 | `Sandstone_Layered_Weathered_Base_s1` | Opaque | L3 | s1 | Now | Dust01 · EdgeWear01 · Crevice01 | ~Wet · ~Moss |
| 7 | `Slate_Cleft_Clean_Base_s1` | Opaque | L3 | s1 | Now | Dust01 · EdgeWear01 · Crevice01 | ~Wet · ~Moss |
| 8 | `Basalt_Dark_Clean_Base_s1` | Opaque | L3 | s1 | Now | Dust01 · EdgeWear01 · Crevice01 | ~Wet · ~Moss |
| 9 | `Travertine_Pitted_Honed_Base_s1` | Opaque | L3 | s1 | Now | Scratches01 · Dust01 · Crevice01 | ~Wet · +WaterSpots01 |
| 10 | `Quartzite_White_Clean_Base_s1` | Opaque | L3 | s1 | Now | Dust01 · EdgeWear01 · Crevice01 | ~Wet · ~Moss |
| 11 | `Lava_Porous_Clean_Base_s1` | Opaque | L3 | s1 | Now | Dust01 · EdgeWear01 · Crevice01 | ~Wet · ~Moss |
| 12 | `Limestone_Cliff_Weathered_Base_s10` | Opaque | L3 | s10 | Now | Dust01 · EdgeWear01 · Crevice01 | ~Wet · ~Moss |
| 13 | `Onyx_Banded_Polished_Base_s01` | Subsurface | L3 | s01 | Now | Scratches01 · Dust01 · Crevice01 | ~Wet · +WaterSpots01 |
| 14 | `Jade_Nephrite_Polished_Base_s01` | Subsurface | L2 | s01 | Now | Scratches01 · Dust01 · Crevice01 | ~Wet · +WaterSpots01 |
| 15 | `Obsidian_Black_Polished_Base_s01` | Opaque | L1 | s01 | Now | Scratches01 · Dust01 · Crevice01 | ~Wet · +WaterSpots01 |

**natural/wood** — 15

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Oak_White_Clean_Base_s01` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Grime01 | +Dust01 · ~Wet · ~WaterStain |
| 2 | `Oak_White_Weathered_Base_s01` | Opaque | L3 | s01 | Now | Dust01 · Cracks01 · Crevice01 | ~Wet · ~Moss |
| 3 | `Oak_White_Varnished_Base_s01` | Opaque | L3 | s01 | C2 | Scuffs01 · Scratches01 · Grime01 | +Dust01 · ~Wet · ~WaterStain |
| 4 | `Walnut_Black_Clean_Base_s01` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Grime01 | +Dust01 · ~Wet · ~WaterStain |
| 5 | `Maple_Hard_Clean_Base_s01` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Grime01 | +Dust01 · ~Wet · ~WaterStain |
| 6 | `Pine_Knotty_Clean_Base_s01` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Grime01 | +Dust01 · ~Wet · ~WaterStain |
| 7 | `Birch_Plain_Clean_Base_s01` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Grime01 | +Dust01 · ~Wet · ~WaterStain |
| 8 | `Cherry_Black_Clean_Base_s01` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Grime01 | +Dust01 · ~Wet · ~WaterStain |
| 9 | `Teak_Plain_Clean_Base_s01` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Grime01 | +Dust01 · ~Wet · ~WaterStain |
| 10 | `Ash_White_Clean_Base_s01` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Grime01 | +Dust01 · ~Wet · ~WaterStain |
| 11 | `Cedar_Red_Weathered_Base_s01` | Opaque | L3 | s01 | Now | Dust01 · Cracks01 · Crevice01 | ~Wet · ~Moss |
| 12 | `Driftwood_Bleached_Weathered_Base_s01` | Opaque | L3 | s01 | Now | Dust01 · Cracks01 · Crevice01 | ~Wet · ~Moss |
| 13 | `Bamboo_Natural_Clean_Base_s01` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Grime01 | +Dust01 · ~Wet · ~WaterStain |
| 14 | `Bark_Pine_Clean_Base_s01` | Opaque | L3 | s01 | Now | Dust01 · Cracks01 · Crevice01 | ~Wet · ~Moss |
| 15 | `Cork_Natural_Clean_Base_s001` | Opaque | L3 | s001 | Now | Scuffs01 · Scratches01 · Grime01 | +Dust01 · ~Wet · ~WaterStain |

**natural/soil** — 10

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Loam_Dark_Clean_Base_s1` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · Patches01 | ~Wet (the wet rows are authored wet) |
| 2 | `Loam_Dark_Wet_Base_s1` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · Patches01 | ~Wet (the wet rows are authored wet) |
| 3 | `Topsoil_Forest_Clean_Base_s1` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · Patches01 | ~Wet (the wet rows are authored wet) |
| 4 | `Clay_Red_Dry_Cracked_s1` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · Patches01 | ~Wet (the wet rows are authored wet) |
| 5 | `Clay_Grey_Wet_Base_s1` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · Patches01 | ~Wet (the wet rows are authored wet) |
| 6 | `Mud_Brown_Wet_Base_s1` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · Patches01 | ~Wet (the wet rows are authored wet) |
| 7 | `Peat_Fibrous_Clean_Base_s1` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · Patches01 | ~Wet (the wet rows are authored wet) |
| 8 | `Laterite_Red_Clean_Base_s1` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · Patches01 | ~Wet (the wet rows are authored wet) |
| 9 | `Silt_River_Wet_Base_s1` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · Patches01 | ~Wet (the wet rows are authored wet) |
| 10 | `Loess_Pale_Dry_Base_s1` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · Patches01 | ~Wet (the wet rows are authored wet) |

**natural/mineral** — 8

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Diamond_Brilliant_Clean_Base_s01` | TranslucentThick | L1 | s01 | ✅ | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 |
| 2 | `Sapphire_Blue_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 |
| 3 | `Ruby_Deep_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 |
| 4 | `Emerald_Green_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 |
| 5 | `Amethyst_Purple_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 |
| 6 | `Quartz_Clear_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 |
| 7 | `Nacre_Iridescent_Polished_Base_s01` | Opaque | L3 | s01 | Now † | Scratches01 · Fingerprints01 · Grime01 | ~Yellowing |
| 8 | `Ivory_Aged_Clean_Base_s01` | Opaque | L3 | s01 | Now · O11 | Scratches01 · Fingerprints01 · Grime01 | ~Yellowing |

† Iridescence needs a thin-film carrier, which is **not** one of C1–C3. Without it, nacre renders as pearl-white and the critique must say so. *(New finding: a fourth carrier candidate, thin film; Physically Based carries `thinFilmIor`/`thinFilmThickness`.)*

### ⚙️ engineered

**engineered/metal** — 20

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Copper_Verdigris_Aged_Base_s01` | Opaque | L3 | s01 | ✅ | Dust01 · Scratches01 · Verdigris01 | (shipped) |
| 2 | `Rust_OnSteel_Flaking_Base_s01` | TwoLayer | L3 | s01 | ✅ | Dust01 · Pitting01 · RustBloom01 | — (layer 2 is the rust) |
| 3 | `Gold_Pure_Polished_Base_s01` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 · ~Tarnish colour |
| 4 | `Silver_Sterling_Polished_Base_s01` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 · ~Tarnish colour |
| 5 | `Copper_Pure_Polished_Base_s01` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 · ~Tarnish colour |
| 6 | `Brass_Yellow_Polished_Base_s01` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 · ~Tarnish colour |
| 7 | `Bronze_Cast_Aged_Base_s01` | Opaque | L3 | s01 | Now | Scratches01 · Dust01 · Grime01 | +Pitting01 · ~Oxide colour |
| 8 | `Aluminium_Raw_Clean_Base_s01` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 · ~Tarnish colour |
| 9 | `Aluminium_Brushed_Clean_Base_s001` | Opaque | L2 | s001 | C3 | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 · ~Tarnish colour |
| 10 | `StainlessSteel_Polished_Clean_Base_s01` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 · ~Tarnish colour |
| 11 | `StainlessSteel_Brushed_Clean_Base_s001` | Opaque | L2 | s001 | C3 | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 · ~Tarnish colour |
| 12 | `Chrome_Mirror_Polished_Base_s01` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 · ~Tarnish colour |
| 13 | `Titanium_Raw_Clean_Base_s01` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Edges01 | +Dust01 · ~Tarnish colour |
| 14 | `Steel_Mild_Clean_Base_s01` | Opaque | L3 | s01 | Now | Scratches01 · Dust01 · Grime01 | +Pitting01 · ~Oxide colour |
| 15 | `Steel_Galvanised_Clean_Base_s01` | Opaque | L3 | s01 | Now | Scratches01 · Dust01 · Grime01 | +Pitting01 · ~Oxide colour |
| 16 | `Steel_Corten_Weathered_Base_s01` | Opaque | L3 | s01 | Now | Dust01 · Pitting01 · RustBloom01 | ~Streaking colour |
| 17 | `Steel_Perforated_Clean_Base_s01` | Masked | L3 | s01 | Now · D1? | Scratches01 · Dust01 · Edges01 |  |
| 18 | `Iron_Cast_Clean_Base_s01` | Opaque | L3 | s01 | Now | Scratches01 · Dust01 · Grime01 | +Pitting01 · ~Oxide colour |
| 19 | `Iron_Wrought_Aged_Base_s01` | Opaque | L3 | s01 | Now | Scratches01 · Dust01 · Grime01 | +Pitting01 · ~Oxide colour |
| 20 | `Lead_Grey_Aged_Base_s01` | Opaque | L3 | s01 | Now | Scratches01 · Dust01 · Grime01 | +Pitting01 · ~Oxide colour |

**engineered/glass** — 6

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Glass_Clear_Clean_Base_s01` | TranslucentThin | L1 | s01 | ✅ | Dust01 · Scratches01 · Grime01 | +Fingerprints01 · +WaterSpots01 |
| 2 | `Glass_Frosted_Clean_Base_s01` | TranslucentThin | L1 | s01 | Now | Dust01 · Scratches01 · Grime01 | +Fingerprints01 · +WaterSpots01 |
| 3 | `Glass_Green_Clean_Base_s01` | TranslucentThin | L1 | s01 | Now | Dust01 · Scratches01 · Grime01 | +Fingerprints01 · +WaterSpots01 |
| 4 | `Glass_Amber_Clean_Base_s01` | TranslucentThin | L1 | s01 | Now | Dust01 · Scratches01 · Grime01 | +Fingerprints01 · +WaterSpots01 |
| 5 | `Glass_Reeded_Clean_Base_s001` | TranslucentThin | L2 | s001 | Now | Dust01 · Scratches01 · Grime01 | +Fingerprints01 · +WaterSpots01 |
| 6 | `Glass_LeadCrystal_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now | Dust01 · Scratches01 · Grime01 | +Fingerprints01 · +WaterSpots01 |

**engineered/cementitious** — 10

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Concrete_Smooth_Worn_Dusty_s1` | Opaque | L3 | s1 | ✅ | Dust01 · Scratches01 · Grime01 | (shipped) · +Cracks01 |
| 2 | `Concrete_BoardFormed_Clean_Base_s1` | Opaque | L3 | s1 | Now | Dust01 · Cracks01 · Grime01 | +Scratches01 · ~Wet · ~Efflorescence colour |
| 3 | `Concrete_Grey_Polished_Base_s1` | Opaque | L3 | s1 | Now | Scratches01 · Scuffs01 · Grime01 | +Dust01 |
| 4 | `Concrete_Aggregate_Weathered_Base_s1` | Opaque | L3 | s1 | Now | Dust01 · Cracks01 · Grime01 | +Scratches01 · ~Wet · ~Efflorescence colour |
| 5 | `Concrete_Smooth_Weathered_Stained_s1` | Opaque | L3 | s1 | Now | Dust01 · Cracks01 · Grime01 | +Scratches01 · ~Wet · ~Efflorescence colour |
| 6 | `Plaster_Smooth_Clean_Base_s1` | Opaque | L3 | s1 | Now | Cracks01 · Dust01 · Drip01 | ~Water stain colour |
| 7 | `Stucco_Rough_Clean_Base_s01` | Opaque | L3 | s01 | Now | Cracks01 · Dust01 · Drip01 | ~Water stain colour |
| 8 | `Terrazzo_Chipped_Polished_Base_s01` | Opaque | L3 | s01 | Now | Scratches01 · Scuffs01 · Grime01 | +Dust01 |
| 9 | `Asphalt_Fresh_Clean_Base_s1` | Opaque | L3 | s1 | Now · O11 | Cracks01 · Scuffs01 · Patches01 | ~Wet · ~Oil stain colour |
| 10 | `Asphalt_Aged_Worn_Cracked_s1` | Opaque | L3 | s1 | Now · O11 | Cracks01 · Scuffs01 · Patches01 | ~Wet · ~Oil stain colour |

**engineered/ceramic** — 8

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Terracotta_Unglazed_Clean_Base_s01` | Opaque | L1 | s01 | Now | EdgeWear01 · Dust01 · Crevice01 | ~Efflorescence colour |
| 2 | `Terracotta_Glazed_Clean_Base_s01` | Opaque | L3 | s01 | C2 | Crazing01 · Scratches01 · Grime01 | +Fingerprints01 |
| 3 | `BrickClay_Red_Clean_Base_s01` | Opaque | L1 | s01 | Now | EdgeWear01 · Dust01 · Crevice01 | ~Efflorescence colour |
| 4 | `Fireclay_Buff_Clean_Base_s01` | Opaque | L2 | s01 | Now | EdgeWear01 · Dust01 · Crevice01 | ~Efflorescence colour |
| 5 | `Earthenware_Red_Clean_Base_s01` | Opaque | L2 | s01 | Now | EdgeWear01 · Dust01 · Crevice01 | ~Efflorescence colour |
| 6 | `Stoneware_SpeckledGlaze_Clean_Base_s01` | Opaque | L2 | s01 | C2 | Crazing01 · Scratches01 · Grime01 | +Fingerprints01 |
| 7 | `Porcelain_Bisque_Clean_Base_s01` | Opaque | L1 | s01 | Now | EdgeWear01 · Dust01 · Crevice01 | ~Efflorescence colour |
| 8 | `Porcelain_Glazed_Clean_Base_s01` | Opaque | L1 | s01 | C2 | Crazing01 · Scratches01 · Grime01 | +Fingerprints01 |

**engineered/composite** — 8 *(the whole class is O11: its boundary is not written)*

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Plywood_Birch_Clean_Base_s01` | Opaque | L3 | s01 | Now · O11 | Scuffs01 · EdgeWear01 · Edges01 | +Dust01 |
| 2 | `MDF_Raw_Clean_Base_s01` | Opaque | L3 | s01 | Now · O11 | Scuffs01 · EdgeWear01 · Edges01 | +Dust01 |
| 3 | `Chipboard_Raw_Clean_Base_s01` | Opaque | L3 | s01 | Now · O11 | Scuffs01 · EdgeWear01 · Edges01 | +Dust01 |
| 4 | `Cardboard_Kraft_Clean_Base_s01` | Opaque | L3 | s01 | Now · O11 | Creases01 · Dust01 · Patches01 | ~Water stain colour |
| 5 | `Paper_White_Clean_Base_s001` | Opaque | L3 | s001 | Now · O11 | Creases01 · Dust01 · Patches01 | ~Water stain colour |
| 6 | `CarbonFibre_Twill_Clean_Base_s001` | Opaque | L2 | s001 | Now · O11 | Scratches01 · Fingerprints01 · Edges01 | +Dust01 |
| 7 | `Fibreglass_Chopped_Clean_Base_s01` | Opaque | L2 | s01 | Now · O11 | Scratches01 · Fingerprints01 · Edges01 | +Dust01 |
| 8 | `Laminate_Matte_Clean_Base_s01` | Opaque | L2 | s01 | Now · O11 | Scratches01 · Fingerprints01 · Edges01 | +Dust01 |

### 🧪 synthetic

**synthetic/plastic** — 10

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `ABS_Matte_Clean_Base_s01` | Opaque | L1 | s01 | ✅ | Scratches01 · Fingerprints01 · Grime01 | +Dust01 · ~UV fading |
| 2 | `ABS_Glossy_Clean_Base_s01` | Opaque | L1 | s01 | Now | Scratches01 · Fingerprints01 · Grime01 | +Dust01 · ~UV fading |
| 3 | `Polypropylene_White_Clean_Base_s01` | Opaque | L1 | s01 | Now | Scratches01 · Fingerprints01 · Grime01 | +Dust01 · ~UV fading |
| 4 | `PVC_Grey_Clean_Base_s01` | Opaque | L1 | s01 | Now | Scratches01 · Fingerprints01 · Grime01 | +Dust01 · ~UV fading |
| 5 | `HDPE_Natural_Clean_Base_s01` | Opaque | L1 | s01 | Now | Scratches01 · Fingerprints01 · Grime01 | +Dust01 · ~UV fading |
| 6 | `Polystyrene_HighImpact_Clean_Base_s01` | Opaque | L1 | s01 | Now · O11 | Scratches01 · Fingerprints01 · Grime01 | +Dust01 · ~UV fading |
| 7 | `Bakelite_Brown_Polished_Base_s01` | Opaque | L1 | s01 | Now · O11 | Scratches01 · Fingerprints01 · Grime01 | +Dust01 · ~UV fading |
| 8 | `Acrylic_Clear_Clean_Base_s01` | TranslucentThin | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Grime01 | +Dust01 · ~Yellowing |
| 9 | `Polycarbonate_Clear_Clean_Base_s01` | TranslucentThin | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Grime01 | +Dust01 · ~Yellowing |
| 10 | `PET_Clear_Clean_Base_s01` | TranslucentThin | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Grime01 | +Dust01 · ~Yellowing |

**synthetic/polymer** — 7 *(plastic vs polymer is O11; the working split used here is "rigid → plastic; elastic, foamed, cast or waxy → polymer")*

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Rubber_Black_Clean_Base_s01` | Opaque | L3 | s01 | Now | Scuffs01 · Dust01 · Grime01 | +Cracks01 |
| 2 | `Neoprene_Black_Clean_Base_s001` | Opaque | L3 | s001 | Now | Scuffs01 · Dust01 · Grime01 | +Cracks01 |
| 3 | `Silicone_Translucent_Clean_Base_s01` | Subsurface | L1 | s01 | Now | Fingerprints01 · Dust01 · Grime01 | +Scratches01 |
| 4 | `Polyurethane_Foam_Clean_Base_s001` | Opaque | L3 | s001 | Now | Dust01 · Pitting01 · Grime01 | ~Yellowing |
| 5 | `Polystyrene_Expanded_Clean_Base_s001` | Opaque | L3 | s001 | Now · O11 | Dust01 · Pitting01 · Grime01 | ~Yellowing |
| 6 | `Epoxy_Clear_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now | Fingerprints01 · Dust01 · Grime01 | +Scratches01 |
| 7 | `Wax_Paraffin_Clean_Base_s01` | Subsurface | L1 | s01 | Now · O11 | Fingerprints01 · Dust01 · Grime01 | +Scratches01 |

**synthetic/textile** — 12 *(cloth without sheen reads acceptably; velvet, satin and suede do not)*

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Lace_Floral_Clean_Base_s01` | Masked | L3 | s01 | ✅ | Dust01 · Pilling01 · Grime01 |  |
| 2 | `Canvas_Natural_Clean_Base_s001` | Opaque | L3 | s001 | Now | Pilling01 · Dust01 · Grime01 | +Creases01 · ~Fading · ~Stain colour |
| 3 | `Denim_Indigo_Clean_Base_s001` | Opaque | L3 | s001 | Now | Pilling01 · Dust01 · Grime01 | +Creases01 · ~Fading · ~Stain colour |
| 4 | `Linen_Natural_Clean_Base_s001` | Opaque | L3 | s001 | Now | Pilling01 · Dust01 · Grime01 | +Creases01 · ~Fading · ~Stain colour |
| 5 | `Tweed_Grey_Clean_Base_s001` | Opaque | L3 | s001 | Now | Pilling01 · Dust01 · Grime01 | +Creases01 · ~Fading · ~Stain colour |
| 6 | `Burlap_Jute_Clean_Base_s001` | Opaque | L3 | s001 | Now | Pilling01 · Dust01 · Grime01 | +Creases01 · ~Fading · ~Stain colour |
| 7 | `Felt_Grey_Clean_Base_s001` | Opaque | L3 | s001 | Now | Pilling01 · Dust01 · Grime01 | +Creases01 · ~Fading · ~Stain colour |
| 8 | `Nylon_Ripstop_Clean_Base_s001` | Opaque | L3 | s001 | Now | Pilling01 · Dust01 · Grime01 | +Creases01 · ~Fading · ~Stain colour |
| 9 | `Leather_Brown_Clean_Base_s01` | Opaque | L3 | s01 | Now · O9? | Scuffs01 · Creases01 · Edges01 | ~Darkening at wear |
| 10 | `Suede_Tan_Clean_Base_s001` | Opaque | L3 | s001 | C2 | Scuffs01 · Creases01 · Edges01 | ~Darkening at wear |
| 11 | `Velvet_Crimson_Clean_Base_s001` | Opaque | L3 | s001 | C2 | Pilling01 · Dust01 · Grime01 | +Creases01 · ~Fading · ~Stain colour |
| 12 | `Satin_Ivory_Clean_Base_s001` | Opaque | L2 | s001 | C2 + C3 | Pilling01 · Dust01 · Grime01 | +Creases01 · ~Fading · ~Stain colour |

**synthetic/coating** — 8

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Paint_Matte_Clean_Base_s01` | Opaque | L1 | s01 | Now | Scratches01 · Dust01 · Edges01 | +Fingerprints01 · ~Chalking colour |
| 2 | `Paint_Satin_Clean_Base_s01` | Opaque | L1 | s01 | Now | Scratches01 · Dust01 · Edges01 | +Fingerprints01 · ~Chalking colour |
| 3 | `Paint_Gloss_Clean_Base_s01` | Opaque | L1 | s01 | C2 | Scratches01 · Dust01 · Edges01 | +Fingerprints01 · ~Chalking colour |
| 4 | `Paint_OnWood_Peeling_Base_s01` | TwoLayer | L3 | s01 | Now | Dust01 · Cracks01 · PaintPeel01 | — (layer 2 is the substrate) |
| 5 | `Paint_OnMetal_Chipped_Base_s01` | TwoLayer | L3 | s01 | Now | Dust01 · Scratches01 · PaintChip01 | — (layer 2 is the substrate) |
| 6 | `PowderCoat_Textured_Clean_Base_s001` | Opaque | L2 | s001 | Now | Scratches01 · Dust01 · Edges01 | +Fingerprints01 · ~Chalking colour |
| 7 | `Enamel_Gloss_Clean_Base_s01` | Opaque | L1 | s01 | C2 | Scratches01 · Dust01 · Edges01 | +Fingerprints01 · ~Chalking colour |
| 8 | `CarPaint_Metallic_Clean_Base_s001` | Opaque | L2 | s001 | C1 + C2 | HairlineScratches01 · WaterSpots01 · Grime01 | +Dust01 |

### 🌫️ environmental

**environmental/sand** — 6

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Sand_Beach_Dry_Base_s1` | Opaque | L3 | s1 | Now | Pitting01 · Dust01 · Patches01 | ~Wet |
| 2 | `Sand_Beach_Wet_Base_s1` | Opaque | L3 | s1 | Now | Pitting01 · Dust01 · Patches01 | ~Wet |
| 3 | `Sand_Desert_Rippled_Base_s1` | Opaque | L3 | s1 | Now | Pitting01 · Dust01 · Patches01 | ~Wet |
| 4 | `Sand_Volcanic_Clean_Base_s1` | Opaque | L3 | s1 | Now | Pitting01 · Dust01 · Patches01 | ~Wet |
| 5 | `Gravel_Pea_Clean_Base_s1` | Opaque | L3 | s1 | Now · O11 | Pitting01 · Dust01 · Patches01 | ~Wet |
| 6 | `Gravel_Crushed_Clean_Base_s1` | Opaque | L3 | s1 | Now · O11 | Pitting01 · Dust01 · Patches01 | ~Wet |

**environmental/vegetation** — 6

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Grass_Lawn_Clean_Base_s1` | Opaque | L3 | s1 | Now | Dust01 · Creases01 · Patches01 | ~Wet · ~Dry-out colour |
| 2 | `Moss_Green_Clean_Base_s01` | Opaque | L3 | s01 | Now | Dust01 · Creases01 · Patches01 | ~Wet · ~Dry-out colour |
| 3 | `Lichen_Crustose_Clean_Base_s01` | Opaque | L2 | s01 | Now | Dust01 · Creases01 · Patches01 | ~Wet · ~Dry-out colour |
| 4 | `LeafLitter_Autumn_Clean_Base_s1` | Opaque | L3 | s1 | Now | Dust01 · Creases01 · Patches01 | ~Wet · ~Dry-out colour |
| 5 | `Straw_Dry_Clean_Base_s01` | Opaque | L3 | s01 | Now | Dust01 · Creases01 · Patches01 | ~Wet · ~Dry-out colour |
| 6 | `Leaf_Oak_Clean_Base_s01` | Masked | L3 | s01 | Now ‡ | Dust01 · Pitting01 · Patches01 | ~Wet · ~Autumn colour |

‡ A leaf card is Masked today; the two-sided thin-transmission *foliage variant* is `(planned)` in `MasterSet.md`.

**environmental/liquid** — 8

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Water_Clear_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now | Ripples01 · Dust01 · Patches01 |  |
| 2 | `Water_Sea_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now | Ripples01 · Dust01 · Patches01 |  |
| 3 | `Water_Murky_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now | Ripples01 · Dust01 · Patches01 |  |
| 4 | `Honey_Amber_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now | Ripples01 · Dust01 · Patches01 | ~Skin/film colour |
| 5 | `Wine_Red_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now | Ripples01 · Dust01 · Patches01 | ~Skin/film colour |
| 6 | `Oil_Motor_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now | Ripples01 · Dust01 · Patches01 | ~Skin/film colour |
| 7 | `Milk_Whole_Clean_Base_s01` | Subsurface | L1 | s01 | Now | Ripples01 · Dust01 · Patches01 | ~Skin/film colour |
| 8 | `Coffee_Black_Clean_Base_s01` | TranslucentThick | L1 | s01 | Now | Ripples01 · Dust01 · Patches01 | ~Skin/film colour |

**Frozen water — home undecided (O11), 2 articles not counted in any class above:**

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Snow_Fresh_Clean_Base_s1` | Subsurface | L3 | s1 | O11 | Pitting01 · Dust01 · Patches01 | ~Dirty-snow colour |
| 2 | `Ice_Clear_Clean_Base_s01` | TranslucentThick | L3 | s01 | O11 | Scratches01 · Cracks01 · Patches01 | ~Frost colour |

### 💡 utility

**utility/emissive** — 6

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Neon_Signage_Clean_Base_s01` | Emissive | L1 | s01 | ✅ | Dust01 · Fingerprints01 · Grime01 | +Scratches01 |
| 2 | `LED_WarmWhite_Clean_Base_s01` | Emissive | L1 | s01 | Now | Dust01 · Fingerprints01 · Grime01 | +Scratches01 |
| 3 | `LED_CoolWhite_Clean_Base_s01` | Emissive | L1 | s01 | Now | Dust01 · Fingerprints01 · Grime01 | +Scratches01 |
| 4 | `Tungsten_Filament_Clean_Base_s01` | Emissive | L1 | s01 | Now | Dust01 · Fingerprints01 · Grime01 | +Scratches01 |
| 5 | `Phosphor_Green_Clean_Base_s01` | Emissive | L1 | s01 | Now | Dust01 · Fingerprints01 · Grime01 | +Scratches01 |
| 6 | `Lava_Molten_Clean_Base_s1` | Emissive | L2 | s1 | Now · O11 | Cracks01 · Pitting01 · Patches01 | ~Crust colour |

**utility/virtual** — 5 *(plus the system article `IMRSV_MissingMaterial`, which is outside the grammar and not counted)*

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Diagnostic_UVGrid_Clean_Base_s1` | Opaque | L2 | s1 | ✅ | — · — · — | none by design: reference articles stay pure |
| 2 | `Diagnostic_Checker_Clean_Base_s1` | Opaque | L2 | s1 | Now | — · — · — | none by design: reference articles stay pure |
| 3 | `GreyCard_Neutral18_Clean_Base_s01` | Opaque | L1 | s01 | Now | — · — · — | none by design: reference articles stay pure |
| 4 | `Spectralon_White_Clean_Base_s01` | Opaque | L1 | s01 | Now | — · — · — | none by design: reference articles stay pure |
| 5 | `MusouBlack_Matte_Clean_Base_s01` | Opaque | L1 | s01 | Now | — · — · — | none by design: reference articles stay pure |

*Rows 3–5 are the Physically Based calibration references (Pass 9 of the prior thread) — the natural anchors for the **Parity Baselines** Roadmap entry.*

**utility/energy** — 3 *(animated plasma is out of scope; these are static, pre-authored looks)*

| # | Stem | Master | Lane | Scale | Status | Overlay 1 · Overlay 2 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Plasma_Blue_Clean_Base_s01` | Emissive | L2 | s01 | Now | Ripples01 · Scratches01 · Patches01 | (treated as a surface; S6 may remove) |
| 2 | `Hologram_Cyan_Clean_Base_s01` | Emissive | L2 | s01 | Now | Ripples01 · Scratches01 · Patches01 | (treated as a surface; S6 may remove) |
| 3 | `Forcefield_Hex_Clean_Base_s01` | Emissive | L2 | s01 | Now | Ripples01 · Scratches01 · Patches01 | (treated as a surface; S6 may remove) |

### Not in the list: biological matter (O9)

Skin (Physically Based carries 6 Fitzpatrick types with subsurface data), hair, bone and nails have **no class**, and hair is not a surface material in this model. They are the platform's one live pull (`PlatformDependencies.md` M1). Leather (textile #9) and ivory (mineral #8) sit on the same boundary.

### Shared wear-layer library (superseded the Pass 2 sketch in Pass 4)

Names follow the shipped forms `<Name><NN>_overlay_sNN.png` (overlays) and `<Name><NN>_sNN.png` (masks). Scale tags are set at authoring. Usage = how many articles in the list carry it.

**Overlays** (`MatterLibrary/textures/shared/overlays/`): 13, of which 2 shipped. Each one only bends the normal and/or roughens.

| Overlay | What it does | Used by | |
|---|---|---|---|
| `Dust01` | fine roughening film | 98 | ✅ |
| `Scratches01` | directional scratches (normal + roughness) | 60 | ✅ |
| `Fingerprints01` | oily smudge prints (roughness) | 39 | new |
| `Cracks01` | hairline cracks (normal) | 24 | new |
| `Pitting01` | pits and pores (normal) | 23 | new |
| `Scuffs01` | broad rubbed scuff marks | 22 | new |
| `HairlineScratches01` | micro-scratches for polished and clear surfaces | 20 | new |
| `EdgeWear01` | chipped, rounded wear (normal) | 16 | new |
| `Ripples01` | surface ripples (normal only) | 11 | new |
| `Pilling01` | fibre pilling and fuzz (normal + roughness) | 10 | new |
| `Creases01` | folds and creases (normal) | 9 | new |
| `Crazing01` | glaze craze network (normal) | 3 | new |
| `WaterSpots01` | dried mineral spots (roughness) | 1 | new |

**Masks** (`MatterLibrary/textures/shared/masks/`): 9, of which 3 shipped. Each one only gates layers.

| Mask | Where it puts wear | Used by | |
|---|---|---|---|
| `Grime01` | low, protected areas | 67 | ✅ |
| `Patches01` | broken-up organic patches | 40 | new |
| `Edges01` | exposed edges and high points | 30 | new |
| `Crevice01` | cracks and recesses | 24 | new |
| `RustBloom01` | rust blooms (TwoLayer R) | 2 | ✅ |
| `Drip01` | vertical run-off streaks | 2 | new |
| `Verdigris01` | patina areas | 1 | ✅ |
| `PaintPeel01` | peeling-paint coverage (TwoLayer R) | 1 | new |
| `PaintChip01` | chipped-paint coverage (TwoLayer R) | 1 | new |

⚠ A mask's G/B gates apply only where the article carries overlays, and the channel contract gives one gate per overlay. The pairing is therefore authored per article. *(A mask on an article with no overlays and no layer 2 is a dead control: the shipped Copper recipe's own rationale.)*

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
| **Total** | **173** (11 shipped + 162 new) **+ 22 wear layers** (13 overlays, 9 masks; 5 shipped; Pass 4) | Pass 11's target was ~170 |

*(C2 and C3 overlap on satin, so the rows sum to 173, not 174.)*

**Findings:**
- **140 new articles need nothing but the Phase03 tools.** The prior thread estimated ~110; the difference is D2 (the material chooses its master), which turned every "routing" blocker into a buildable row.
- **C2 (coat/sheen) is the most valuable carrier.** It unblocks 10 articles across ceramic, wood, textile and coating. C3 unblocks 3. C1 turns 8 approximations into measured metals.
- **A fourth carrier appears: thin film** (nacre, and later soap film and oil sheen). It is not in C1–C3. *(New open question L3.)*
- **The class-boundary rulings (O11) matter more than they looked:** 22 rows (20 tagged + snow and ice) carry a provisional home. `Polystyrene` appears in both plastic and polymer, which is the plainest example.
- **Names:** every stem is within 63 chars (the longest, `StainlessSteel_Brushed_Clean_Base_s001`, is 38). Nothing here tests the budget.

## Pass 4 — Wear layers on every article (ruling C1)

**Examined (2026-09-25):** `MasterSet.md` §Overlay/MaskSet model (cap, channel contract, overlay formula, cost note); `LCDSchema.md` (render-role textures fixed per article; only the densities are Creator ports); `tools/converters/assemble_mtlx.py` (overlay roughness handling); the 4 shipped recipes that use layers (Concrete, Glass, Copper, Rust).

**How the layers work, as the contract stands:**
- An article carries **≤ 2 overlays and ≤ 1 mask** (`MasterSet.md`). The textures are fixed when the article is authored. The Creator gets only the strengths: `overlay1_density`, `overlay2_density`, `maskset_blend`.
- An overlay changes **normal and roughness only**, never colour (the modulator rule, normative).
- **An overlay can only roughen.** `assemble_mtlx.py` reads the B channel as a bias in [0, 1] ("an overlay can only ever ROUGHEN"), verified 2026-09-25.

**What was done:** the list gained a wear-layer column. Each row got the two most relevant overlays and a gating mask for its class and finish (a script over the tables; the rule is readable in the column). Everything else relevant went into **Also wanted**. Defaults are **0** everywhere, except `maskset_blend` on TwoLayer articles, where layer 2 *is* the material (`Rust_OnSteel`, `Paint_On…`), so the recipe must keep it non-zero (the shipped Rust recipe's own rule).

**Findings:**
- **168 of 173 articles carry 2 overlays and 1 mask.** The 5 `utility/virtual` references carry none by design, because a calibration target must stay pure.
- **The layer library grows from 5 to 22:** 11 new overlays and 6 new masks. These are packed data textures, produced by L2 (procedural, deterministic) or converted from ambientCG's 52 imperfection sets (prior thread, Pass 9). **They are a deliverable in their own right**, and every article depends on them.
- **The cap collides with the ruling.** **96 of 173 rows** have a third relevant overlay that doesn't fit (most often `Dust01` on scratched surfaces, `Fingerprints01` and `WaterSpots01` on glass). The ruling says all relevant layers; the contract says two. *(Open question L6.)*
- **The modulator rule collides with "smart" more deeply.** **121 rows** want an effect that overlays cannot express at all:
  - **wet** (57 rows) needs smoothing and darkening;
  - **moss, stains, tarnish, fading, yellowing and efflorescence** need colour.

  Today the only way to put colour on an article is **TwoLayer** (a whole second material under a mask), and each article has one master. *(Open question L7.)*
- **7 shipped articles carry no overlays:** Limestone, Marble, Rust (mask only), Diamond, ABS, Lace, Neon. Under C1 each needs a new version. **Immutability** says that is `v02`, but the repo also has a recorded in-place `v01` precedent (the Version Management seed, from Issue #1). That call belongs to Version Management, not here. *(Open question L8.)*
- **Cost:** `MasterSet.md` notes that always-carried layers cost shader time even at strength 0. The VR-budget measurement that picks the strategy is marked `Reevaluate` (never recorded here). C1 makes that measurement load-bearing: every article now pays the cost.
- **Phase03 impact:** the `/matter-generate` skill, the recipe schema (G2) and the plausibility guard must author and check the layer assignment per article, and 17 new layer textures need producing. The Phase03 Brief doesn't include either yet. *(Recorded for `/discovery Phase03`; research does not edit the phase doc.)*

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
| L6 | **Raise the cap of 2 overlays per article (e.g. to 3 or 4), or accept picking the top 2?** This is a `MasterSet.md` / `LCDSchema.md` contract change: new Creator ports, and a new gate channel (the mask's A channel is reserved and free). | 96 rows want a third overlay. Ruling C1 says all relevant layers. |
| L7 | **How does a "smart" article get colour and wet?** Options: (a) signed roughness bias in overlays (enables wet sheen, but not darkening); (b) a colour-carrying layer kind, which reverses the normative modulator rule; (c) TwoLayer for colour wear, which spends the article's one master on it. | 121 rows want wet, moss, stains, tarnish or fading. |
| L8 | Do the 7 shipped articles without overlays get `v02`, or the in-place `v01` precedent? | Version Management owns it. |

## Status

**Passes captured:** 4 (2026-09-25).

- **Ruling C1 (lead): smart, not lean.** Every article carries all its relevant overlays and masks at strength 0. Names are unchanged.
- **Draft v1 of the list is complete:** 173 named articles (11 shipped, 162 new) across all 20 classes, including 2 unplaced (snow, ice). Every row has a full stem, a folder, a declared master, a lane, a scale tag, a status and **its wear layers** (168 carry 2 overlays + 1 mask; the 5 virtual references carry none). The shared layer library grows from 5 to 22.
- **C1 collides with two contract limits:** the 2-overlay cap (96 rows want more; L6) and the modulator rule (121 rows want wet or colour wear; L7). Both are lead calls on `MasterSet.md`, and neither is decided here.
- **140 new articles are buildable with the Phase03 tools alone** (20 of them in a provisional class). The rest wait on carriers C2 (10), C3 (3), optionally C1 (8), or a class ruling (snow, ice).
- **Direction:** nothing is committed. This is input for the lead's gut check, and later for the *Library Coverage* phase.
- **Open:** L1–L8. None blocks Phase03's first step, but C1 widens Phase03's scope: the skill must author the layers, and 17 layer textures must be produced. `/discovery Phase03` should pick that up.
- **Next step:** the lead marks up the list (rename, cut, add, move), and rules N1–N7 and S1–S6 where they have a view. The naming rulings then land in `NamingConventions.md` / `Identity.md` through a `/quick-fix`, and the class rulings in `Taxonomy.md`. A later pass here re-issues the list as v2.
