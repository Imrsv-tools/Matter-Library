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
| C2 | **Raise the overlay cap from 2 to 3** (lead, 2026-09-25; answers L6). *Blast radius: a contract change to `MasterSet.md` §Overlay/MaskSet model and `LCDSchema.md` (a new Creator port, presumably `overlay3_density`, 0–1 / `0`; a third gate, presumably the maskset's reserved A channel). It also touches the assembler, the validators, the Blender add-on and every consumer master. The spec is not edited from research; see Pass 5.* |
| C3 | **One matter may have several articles with different overlay sets** (lead, 2026-09-25): e.g. an `Oak` article per Condition/Detail, each carrying the layers that fit it. That is how a fourth or fifth relevant layer is covered, not by a larger cap. |
| C4 | **The filename has exactly six tokens — five underscores — so it can be parsed** (lead, 2026-09-25, restating the original grammar). Layer information goes *inside* `Condition` / `Detail` (e.g. `Distressed_Dusty`), never in added tokens. See Pass 6. |
| C5 | **Each name token is a fixed axis** (lead, 2026-09-25; "apply"). **Material** = the matter, down to species or alloy (`WhiteOak`, `MildSteel`; optionally a base-set id, as in `Limestone26b`). **Variant** = the *look*: base-texture choice plus tint and the other Creator settings (`Natural`, `Polished`, `Weathered`, `Blue`), so a white oak tinted blue is `WhiteOak_Blue`. **Condition** = the **damage** axis, driven by overlay 1 (+ mask): `Clean` (0) → `Worn` → `Distressed`, with an optional save counter (`VeryDistressed12`). **Detail** = everything else, driven by overlays 2–3 (usually deposits, but a second damage layer too; E1 (a), lead 2026-09-25): `Base` (0) → `Dusty` → `ScratchedButNotVeryDusty`. Names can be user-made from slider states; the exact values live in the file. **Overlay slot 1 is the damage layer.** See Pass 7. |
| C6 | **Composed materials are not matter; a single leaf is** (lead, 2026-09-25): "leaf textures as materials would be good, just not a full ground of leaves." The test: pick up one piece; is it the same substance as the whole? `LeafLitter_Autumn` and `Grass_Lawn` moved to a **Composed (planned)** section, kept, not deleted. `OakLeaf` stays, and `MapleLeaf` and `IvyLeaf` were added. `Topsoil_Forest` is flagged `Composed?`. |

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
| every article is `v01` | first version | every row is `_v01`, shown in full in the tables |

**Depth per matter, not volume** (Pass 11 of the prior thread): Condition/Detail variants are kept rare, because the Creator-tier tint, UV and roughness controls plus overlays and masksets already span most conditions. A Condition appears only where the condition changes the *matter's* look beyond what an overlay does (wet, weathered, peeling).

**Matter only (D1):** no walls, floors, tiles, paving, corrugated sheet or diamond plate — their substance is listed instead.

## Pass 2 — The list

**Columns:** `Path` = `MatterLibrary/materials/<domain>/<class>/` + the full filename. **Master** = the article's declared master (D2: the material decides, the class is only a default). **Lane:** L1 param-only grounded in Physically Based · L2 agent-written procedural texture · L3 ambientCG CC0 scan. **Status:**

- ✅ **shipped** (in `matterlib-0.1.0`)
- **Now** — buildable with no contract change
- **Now·C1** — buildable, but a measured metal wants the F82 `specular_color` carrier to be accurate (open O5)
- **C2** — blocked on the coat/sheen carrier (the look *is* the coat or the sheen)
- **C3** — blocked on the anisotropy carrier
- **O11** — class boundary undecided; the row's home is provisional
- **D1?** — may be an assembly rather than matter; lead's call

**Wear layers (Pass 4, ruling C1; third overlay added in Pass 5, ruling C2):** `Overlays 1 · 2 · 3 · Mask` = the shared layers the article carries, all at default strength 0. The mask gates *where* each overlay may appear (G/B, and presumably A for overlay 3) and, on TwoLayer, where layer 2 sits (R). **Also wanted:**
- **`+X`** is a fourth relevant overlay. Per C3 it is covered by a sibling article, not a bigger cap.
- **`~X`** is a colour or gloss change. **Uniformly across the article it is already available** through the Creator ports `base_color_tint` (colour multiply) and `roughness_bias` (−0.5…+0.5). What no layer can do today is apply it *locally*, e.g. moss only in crevices or wet only in patches (Pass 5, L7).

*Physically Based record names are unverified per row; Pass 9 of the prior thread confirmed the category counts (Metal 32, Crystal 10, Liquid 19, Manmade 22, Plastic 7), not each entry. ambientCG availability per row is by category (Pass 9), not by named set.*

### 🪨 natural

**natural/stone** — 15

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Limestone_Veined_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | ✅ | EdgeWear01 · Dust01 · — · Crevice01 | ~Wet · ~Moss |
| 2 | `Marble_Veined_Polished_Base_s01_v01.mtlx` | Subsurface | L3 | s01 | ✅ | Scratches01 · Dust01 · WaterSpots01 · Crevice01 | ~Wet |
| 3 | `CarraraMarble_Honed_Clean_Base_s1_v01.mtlx` | Subsurface | L3 | s1 | Now | Scratches01 · Dust01 · WaterSpots01 · Crevice01 | ~Wet |
| 4 | `Granite_Polished_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Scratches01 · Dust01 · WaterSpots01 · Crevice01 | ~Wet |
| 5 | `Granite_Weathered_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | EdgeWear01 · Dust01 · — · Crevice01 | ~Wet · ~Moss |
| 6 | `Sandstone_Weathered_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | EdgeWear01 · Dust01 · — · Crevice01 | ~Wet · ~Moss |
| 7 | `Slate_Cleft_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | EdgeWear01 · Dust01 · — · Crevice01 | ~Wet · ~Moss |
| 8 | `Basalt_Natural_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | EdgeWear01 · Dust01 · — · Crevice01 | ~Wet · ~Moss |
| 9 | `Travertine_Honed_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Scratches01 · Dust01 · WaterSpots01 · Crevice01 | ~Wet |
| 10 | `Quartzite_Natural_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | EdgeWear01 · Dust01 · — · Crevice01 | ~Wet · ~Moss |
| 11 | `LavaRock_Natural_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | EdgeWear01 · Dust01 · — · Crevice01 | ~Wet · ~Moss |
| 12 | `Limestone_CliffWeathered_Clean_Base_s10_v01.mtlx` | Opaque | L3 | s10 | Now | EdgeWear01 · Dust01 · — · Crevice01 | ~Wet · ~Moss |
| 13 | `Onyx_Polished_Clean_Base_s01_v01.mtlx` | Subsurface | L3 | s01 | Now | Scratches01 · Dust01 · WaterSpots01 · Crevice01 | ~Wet |
| 14 | `NephriteJade_Polished_Clean_Base_s01_v01.mtlx` | Subsurface | L2 | s01 | Now | Scratches01 · Dust01 · WaterSpots01 · Crevice01 | ~Wet |
| 15 | `Obsidian_Polished_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now | Scratches01 · Dust01 · WaterSpots01 · Crevice01 | ~Wet |

**natural/wood** — 15

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `WhiteOak_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Dust01 · Grime01 | ~Wet · ~WaterStain |
| 2 | `WhiteOak_Weathered_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Cracks01 · Dust01 · — · Crevice01 | ~Wet · ~Moss |
| 3 | `WhiteOak_Varnished_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | C2 | Scuffs01 · Scratches01 · Dust01 · Grime01 | ~Wet · ~WaterStain |
| 4 | `BlackWalnut_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Dust01 · Grime01 | ~Wet · ~WaterStain |
| 5 | `HardMaple_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Dust01 · Grime01 | ~Wet · ~WaterStain |
| 6 | `Pine_Knotty_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Dust01 · Grime01 | ~Wet · ~WaterStain |
| 7 | `Birch_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Dust01 · Grime01 | ~Wet · ~WaterStain |
| 8 | `BlackCherry_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Dust01 · Grime01 | ~Wet · ~WaterStain |
| 9 | `Teak_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Dust01 · Grime01 | ~Wet · ~WaterStain |
| 10 | `WhiteAsh_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Dust01 · Grime01 | ~Wet · ~WaterStain |
| 11 | `RedCedar_Weathered_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Cracks01 · Dust01 · — · Crevice01 | ~Wet · ~Moss |
| 12 | `Driftwood_Bleached_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Cracks01 · Dust01 · — · Crevice01 | ~Wet · ~Moss |
| 13 | `Bamboo_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scuffs01 · Scratches01 · Dust01 · Grime01 | ~Wet · ~WaterStain |
| 14 | `PineBark_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Cracks01 · Dust01 · — · Crevice01 | ~Wet · ~Moss |
| 15 | `Cork_Natural_Clean_Base_s001_v01.mtlx` | Opaque | L3 | s001 | Now | Scuffs01 · Scratches01 · Dust01 · Grime01 | ~Wet · ~WaterStain |

**natural/soil** — 10

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Loam_Natural_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · — · Patches01 | ~Wet (the wet rows are authored wet) |
| 2 | `Loam_Wet_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · — · Patches01 | ~Wet (the wet rows are authored wet) |
| 3 | `Topsoil_Forest_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now · Composed? | Cracks01 · Pitting01 · — · Patches01 | ~Wet (the wet rows are authored wet) |
| 4 | `RedClay_DryCracked_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · — · Patches01 | ~Wet (the wet rows are authored wet) |
| 5 | `GreyClay_Wet_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · — · Patches01 | ~Wet (the wet rows are authored wet) |
| 6 | `Mud_Natural_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · — · Patches01 | ~Wet (the wet rows are authored wet) |
| 7 | `Peat_Natural_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · — · Patches01 | ~Wet (the wet rows are authored wet) |
| 8 | `Laterite_Natural_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · — · Patches01 | ~Wet (the wet rows are authored wet) |
| 9 | `Silt_Wet_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · — · Patches01 | ~Wet (the wet rows are authored wet) |
| 10 | `Loess_Dry_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Cracks01 · Pitting01 · — · Patches01 | ~Wet (the wet rows are authored wet) |

**natural/mineral** — 8

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Diamond_Brilliant_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | ✅ | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 |  |
| 2 | `Sapphire_Natural_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 |  |
| 3 | `Ruby_Natural_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 |  |
| 4 | `Emerald_Natural_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 |  |
| 5 | `Amethyst_Natural_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 |  |
| 6 | `Quartz_Clear_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 |  |
| 7 | `Nacre_Polished_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now † | Scratches01 · Fingerprints01 · — · Grime01 | ~Yellowing |
| 8 | `Ivory_Aged_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now · O11 | Scratches01 · Fingerprints01 · — · Grime01 | ~Yellowing |

† Iridescence needs a thin-film carrier, which is **not** one of C1–C3. Without it, nacre renders as pearl-white and the critique must say so. *(New finding: a fourth carrier candidate, thin film; Physically Based carries `thinFilmIor`/`thinFilmThickness`.)*

### ⚙️ engineered

**engineered/metal** — 20

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Copper_Verdigris_Aged_Base_s01_v01.mtlx` | Opaque | L3 | s01 | ✅ | Scratches01 · Dust01 · — · Verdigris01 | (shipped) |
| 2 | `Rust_OnSteel_Flaking_Base_s01_v01.mtlx` | TwoLayer | L3 | s01 | ✅ | Pitting01 · Dust01 · — · RustBloom01 | — (layer 2 is the rust) |
| 3 | `Gold_Polished_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 | ~Tarnish colour |
| 4 | `SterlingSilver_Polished_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 | ~Tarnish colour |
| 5 | `Copper_Polished_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 | ~Tarnish colour |
| 6 | `Brass_Polished_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 | ~Tarnish colour |
| 7 | `Bronze_Aged_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scratches01 · Pitting01 · Dust01 · Grime01 | ~Oxide colour |
| 8 | `Aluminium_Raw_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 | ~Tarnish colour |
| 9 | `Aluminium_Brushed_Clean_Base_s001_v01.mtlx` | Opaque | L2 | s001 | C3 | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 | ~Tarnish colour |
| 10 | `StainlessSteel_Polished_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 | ~Tarnish colour |
| 11 | `StainlessSteel_Brushed_Clean_Base_s001_v01.mtlx` | Opaque | L2 | s001 | C3 | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 | ~Tarnish colour |
| 12 | `Chrome_Mirror_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 | ~Tarnish colour |
| 13 | `Titanium_Raw_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now·C1 | HairlineScratches01 · Fingerprints01 · Dust01 · Edges01 | ~Tarnish colour |
| 14 | `MildSteel_Raw_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scratches01 · Pitting01 · Dust01 · Grime01 | ~Oxide colour |
| 15 | `Steel_Galvanised_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scratches01 · Pitting01 · Dust01 · Grime01 | ~Oxide colour |
| 16 | `CortenSteel_Weathered_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Pitting01 · Dust01 · — · RustBloom01 | ~Streaking colour |
| 17 | `Steel_Perforated_Clean_Base_s01_v01.mtlx` | Masked | L3 | s01 | Now · D1? | Scratches01 · Dust01 · — · Edges01 |  |
| 18 | `CastIron_Raw_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scratches01 · Pitting01 · Dust01 · Grime01 | ~Oxide colour |
| 19 | `WroughtIron_Aged_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scratches01 · Pitting01 · Dust01 · Grime01 | ~Oxide colour |
| 20 | `Lead_Aged_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scratches01 · Pitting01 · Dust01 · Grime01 | ~Oxide colour |

**engineered/glass** — 6

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Glass_Clear_Clean_Base_s01_v01.mtlx` | TranslucentThin | L1 | s01 | ✅ | Scratches01 · Dust01 · Fingerprints01 · Grime01 | +WaterSpots01 |
| 2 | `Glass_Frosted_Clean_Base_s01_v01.mtlx` | TranslucentThin | L1 | s01 | Now | Scratches01 · Dust01 · Fingerprints01 · Grime01 | +WaterSpots01 |
| 3 | `Glass_Green_Clean_Base_s01_v01.mtlx` | TranslucentThin | L1 | s01 | Now | Scratches01 · Dust01 · Fingerprints01 · Grime01 | +WaterSpots01 |
| 4 | `Glass_Amber_Clean_Base_s01_v01.mtlx` | TranslucentThin | L1 | s01 | Now | Scratches01 · Dust01 · Fingerprints01 · Grime01 | +WaterSpots01 |
| 5 | `Glass_Reeded_Clean_Base_s001_v01.mtlx` | TranslucentThin | L2 | s001 | Now | Scratches01 · Dust01 · Fingerprints01 · Grime01 | +WaterSpots01 |
| 6 | `LeadCrystal_Clear_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | Now | Scratches01 · Dust01 · Fingerprints01 · Grime01 | +WaterSpots01 |

**engineered/cementitious** — 10

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Concrete_Smooth_Worn_Dusty_s1_v01.mtlx` | Opaque | L3 | s1 | ✅ | Scratches01 · Cracks01 · Dust01 · Grime01 | (shipped) |
| 2 | `Concrete_BoardFormed_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Cracks01 · Scratches01 · Dust01 · Grime01 | ~Wet · ~Efflorescence colour |
| 3 | `Concrete_Polished_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Scratches01 · Scuffs01 · Dust01 · Grime01 |  |
| 4 | `Concrete_ExposedAggregate_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Cracks01 · Scratches01 · Dust01 · Grime01 | ~Wet · ~Efflorescence colour |
| 5 | `Concrete_Stained_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Cracks01 · Scratches01 · Dust01 · Grime01 | ~Wet · ~Efflorescence colour |
| 6 | `Plaster_Smooth_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Cracks01 · Dust01 · — · Drip01 | ~Water stain colour |
| 7 | `Stucco_Rough_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Cracks01 · Dust01 · — · Drip01 | ~Water stain colour |
| 8 | `Terrazzo_Polished_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scratches01 · Scuffs01 · Dust01 · Grime01 |  |
| 9 | `Asphalt_Fresh_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now · O11 | Cracks01 · Scuffs01 · — · Patches01 | ~Wet · ~Oil stain colour |
| 10 | `Asphalt_Aged_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now · O11 | Cracks01 · Scuffs01 · — · Patches01 | ~Wet · ~Oil stain colour |

**engineered/ceramic** — 8

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Terracotta_Unglazed_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now | EdgeWear01 · Dust01 · — · Crevice01 | ~Efflorescence colour |
| 2 | `Terracotta_Glazed_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | C2 | Crazing01 · Scratches01 · Fingerprints01 · Grime01 |  |
| 3 | `BrickClay_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now | EdgeWear01 · Dust01 · — · Crevice01 | ~Efflorescence colour |
| 4 | `Fireclay_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L2 | s01 | Now | EdgeWear01 · Dust01 · — · Crevice01 | ~Efflorescence colour |
| 5 | `Earthenware_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L2 | s01 | Now | EdgeWear01 · Dust01 · — · Crevice01 | ~Efflorescence colour |
| 6 | `Stoneware_SpeckledGlaze_Clean_Base_s01_v01.mtlx` | Opaque | L2 | s01 | C2 | Crazing01 · Scratches01 · Fingerprints01 · Grime01 |  |
| 7 | `Porcelain_Bisque_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now | EdgeWear01 · Dust01 · — · Crevice01 | ~Efflorescence colour |
| 8 | `Porcelain_Glazed_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | C2 | Crazing01 · Scratches01 · Fingerprints01 · Grime01 |  |

**engineered/composite** — 8 *(the whole class is O11: its boundary is not written)*

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `BirchPlywood_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now · O11 | Scuffs01 · EdgeWear01 · Dust01 · Edges01 |  |
| 2 | `MDF_Raw_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now · O11 | Scuffs01 · EdgeWear01 · Dust01 · Edges01 |  |
| 3 | `Chipboard_Raw_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now · O11 | Scuffs01 · EdgeWear01 · Dust01 · Edges01 |  |
| 4 | `Cardboard_Kraft_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now · O11 | Creases01 · Dust01 · — · Patches01 | ~Water stain colour |
| 5 | `Paper_Natural_Clean_Base_s001_v01.mtlx` | Opaque | L3 | s001 | Now · O11 | Creases01 · Dust01 · — · Patches01 | ~Water stain colour |
| 6 | `CarbonFibre_Twill_Clean_Base_s001_v01.mtlx` | Opaque | L2 | s001 | Now · O11 | Scratches01 · Fingerprints01 · Dust01 · Edges01 |  |
| 7 | `Fibreglass_Chopped_Clean_Base_s01_v01.mtlx` | Opaque | L2 | s01 | Now · O11 | Scratches01 · Fingerprints01 · Dust01 · Edges01 |  |
| 8 | `Laminate_Matte_Clean_Base_s01_v01.mtlx` | Opaque | L2 | s01 | Now · O11 | Scratches01 · Fingerprints01 · Dust01 · Edges01 |  |

### 🧪 synthetic

**synthetic/plastic** — 10

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `ABS_Matte_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | ✅ | Scratches01 · Fingerprints01 · Dust01 · Grime01 | ~UV fading |
| 2 | `ABS_Glossy_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now | Scratches01 · Fingerprints01 · Dust01 · Grime01 | ~UV fading |
| 3 | `Polypropylene_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now | Scratches01 · Fingerprints01 · Dust01 · Grime01 | ~UV fading |
| 4 | `PVC_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now | Scratches01 · Fingerprints01 · Dust01 · Grime01 | ~UV fading |
| 5 | `HDPE_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now | Scratches01 · Fingerprints01 · Dust01 · Grime01 | ~UV fading |
| 6 | `HIPS_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now · O11 | Scratches01 · Fingerprints01 · Dust01 · Grime01 | ~UV fading |
| 7 | `Bakelite_Polished_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now · O11 | Scratches01 · Fingerprints01 · Dust01 · Grime01 | ~UV fading |
| 8 | `Acrylic_Clear_Clean_Base_s01_v01.mtlx` | TranslucentThin | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Dust01 · Grime01 | ~Yellowing |
| 9 | `Polycarbonate_Clear_Clean_Base_s01_v01.mtlx` | TranslucentThin | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Dust01 · Grime01 | ~Yellowing |
| 10 | `PET_Clear_Clean_Base_s01_v01.mtlx` | TranslucentThin | L1 | s01 | Now | HairlineScratches01 · Fingerprints01 · Dust01 · Grime01 | ~Yellowing |

**synthetic/polymer** — 7 *(plastic vs polymer is O11; the working split used here is "rigid → plastic; elastic, foamed, cast or waxy → polymer")*

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Rubber_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Scuffs01 · Cracks01 · Dust01 · Grime01 |  |
| 2 | `Neoprene_Natural_Clean_Base_s001_v01.mtlx` | Opaque | L3 | s001 | Now | Scuffs01 · Cracks01 · Dust01 · Grime01 |  |
| 3 | `Silicone_Translucent_Clean_Base_s01_v01.mtlx` | Subsurface | L1 | s01 | Now | Scratches01 · Fingerprints01 · Dust01 · Grime01 |  |
| 4 | `Polyurethane_Foam_Clean_Base_s001_v01.mtlx` | Opaque | L3 | s001 | Now | Pitting01 · Dust01 · — · Grime01 | ~Yellowing |
| 5 | `Polystyrene_Expanded_Clean_Base_s001_v01.mtlx` | Opaque | L3 | s001 | Now · O11 | Pitting01 · Dust01 · — · Grime01 | ~Yellowing |
| 6 | `Epoxy_Clear_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | Now | Scratches01 · Fingerprints01 · Dust01 · Grime01 |  |
| 7 | `ParaffinWax_Natural_Clean_Base_s01_v01.mtlx` | Subsurface | L1 | s01 | Now · O11 | Scratches01 · Fingerprints01 · Dust01 · Grime01 |  |

**synthetic/textile** — 12 *(cloth without sheen reads acceptably; velvet, satin and suede do not)*

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Lace_Floral_Clean_Base_s01_v01.mtlx` | Masked | L3 | s01 | ✅ | Pilling01 · Dust01 · — · Grime01 |  |
| 2 | `Canvas_Natural_Clean_Base_s001_v01.mtlx` | Opaque | L3 | s001 | Now | Pilling01 · Creases01 · Dust01 · Grime01 | ~Fading · ~Stain colour |
| 3 | `Denim_Indigo_Clean_Base_s001_v01.mtlx` | Opaque | L3 | s001 | Now | Pilling01 · Creases01 · Dust01 · Grime01 | ~Fading · ~Stain colour |
| 4 | `Linen_Natural_Clean_Base_s001_v01.mtlx` | Opaque | L3 | s001 | Now | Pilling01 · Creases01 · Dust01 · Grime01 | ~Fading · ~Stain colour |
| 5 | `Tweed_Natural_Clean_Base_s001_v01.mtlx` | Opaque | L3 | s001 | Now | Pilling01 · Creases01 · Dust01 · Grime01 | ~Fading · ~Stain colour |
| 6 | `Burlap_Natural_Clean_Base_s001_v01.mtlx` | Opaque | L3 | s001 | Now | Pilling01 · Creases01 · Dust01 · Grime01 | ~Fading · ~Stain colour |
| 7 | `Felt_Natural_Clean_Base_s001_v01.mtlx` | Opaque | L3 | s001 | Now | Pilling01 · Creases01 · Dust01 · Grime01 | ~Fading · ~Stain colour |
| 8 | `Nylon_Ripstop_Clean_Base_s001_v01.mtlx` | Opaque | L3 | s001 | Now | Pilling01 · Creases01 · Dust01 · Grime01 | ~Fading · ~Stain colour |
| 9 | `Leather_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now · O9? | Scuffs01 · Creases01 · — · Edges01 | ~Darkening at wear |
| 10 | `Suede_Natural_Clean_Base_s001_v01.mtlx` | Opaque | L3 | s001 | C2 | Scuffs01 · Creases01 · — · Edges01 | ~Darkening at wear |
| 11 | `Velvet_Natural_Clean_Base_s001_v01.mtlx` | Opaque | L3 | s001 | C2 | Pilling01 · Creases01 · Dust01 · Grime01 | ~Fading · ~Stain colour |
| 12 | `Satin_Natural_Clean_Base_s001_v01.mtlx` | Opaque | L2 | s001 | C2 + C3 | Pilling01 · Creases01 · Dust01 · Grime01 | ~Fading · ~Stain colour |

**synthetic/coating** — 8

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Paint_Matte_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now | Scratches01 · Dust01 · Fingerprints01 · Edges01 | ~Chalking colour |
| 2 | `Paint_Satin_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now | Scratches01 · Dust01 · Fingerprints01 · Edges01 | ~Chalking colour |
| 3 | `Paint_Gloss_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | C2 | Scratches01 · Dust01 · Fingerprints01 · Edges01 | ~Chalking colour |
| 4 | `Paint_OnWood_Peeling_Base_s01_v01.mtlx` | TwoLayer | L3 | s01 | Now | Cracks01 · Dust01 · — · PaintPeel01 | — (layer 2 is the substrate) |
| 5 | `Paint_OnMetal_Chipped_Base_s01_v01.mtlx` | TwoLayer | L3 | s01 | Now | Scratches01 · Dust01 · — · PaintChip01 | — (layer 2 is the substrate) |
| 6 | `PowderCoat_Textured_Clean_Base_s001_v01.mtlx` | Opaque | L2 | s001 | Now | Scratches01 · Dust01 · Fingerprints01 · Edges01 | ~Chalking colour |
| 7 | `Enamel_Gloss_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | C2 | Scratches01 · Dust01 · Fingerprints01 · Edges01 | ~Chalking colour |
| 8 | `CarPaint_Metallic_Clean_Base_s001_v01.mtlx` | Opaque | L2 | s001 | C1 + C2 | HairlineScratches01 · WaterSpots01 · Dust01 · Grime01 |  |

### 🌫️ environmental

**environmental/sand** — 6

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `BeachSand_Dry_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Pitting01 · Dust01 · — · Patches01 | ~Wet |
| 2 | `BeachSand_Wet_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Pitting01 · Dust01 · — · Patches01 | ~Wet |
| 3 | `DesertSand_Rippled_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Pitting01 · Dust01 · — · Patches01 | ~Wet |
| 4 | `VolcanicSand_Natural_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now | Pitting01 · Dust01 · — · Patches01 | ~Wet |
| 5 | `PeaGravel_Natural_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now · O11 | Pitting01 · Dust01 · — · Patches01 | ~Wet |
| 6 | `CrushedGravel_Natural_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Now · O11 | Pitting01 · Dust01 · — · Patches01 | ~Wet |

**environmental/vegetation** — 6 *(leaves are matter: a single leaf's tissue on a card. A ground covered in leaves is not; see Composed below)*

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Moss_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Creases01 · Dust01 · — · Patches01 | ~Wet · ~Dry-out colour |
| 2 | `Lichen_Crustose_Clean_Base_s01_v01.mtlx` | Opaque | L2 | s01 | Now | Creases01 · Dust01 · — · Patches01 | ~Wet · ~Dry-out colour |
| 3 | `Straw_Natural_Clean_Base_s01_v01.mtlx` | Opaque | L3 | s01 | Now | Creases01 · Dust01 · — · Patches01 | ~Wet · ~Dry-out colour |
| 4 | `OakLeaf_Natural_Clean_Base_s01_v01.mtlx` | Masked | L3 | s01 | Now ‡ | Pitting01 · Dust01 · — · Patches01 | ~Wet · ~Autumn colour |
| 5 | `MapleLeaf_Natural_Clean_Base_s01_v01.mtlx` | Masked | L3 | s01 | Now ‡ | Pitting01 · Dust01 · — · Patches01 | ~Wet · ~Autumn colour |
| 6 | `IvyLeaf_Natural_Clean_Base_s01_v01.mtlx` | Masked | L3 | s01 | Now ‡ | Pitting01 · Dust01 · — · Patches01 | ~Wet · ~Autumn colour |

‡ A leaf card is Masked today; the two-sided thin-transmission *foliage variant* is `(planned)` in `MasterSet.md`.

**Composed (planned) — not matter, kept so the intent survives** *(ruling C6)*. Each of these is an **arrangement** of several matters (loose leaves, twigs and soil; living grass over soil). By D1 that is not a substance, so they sit outside the matter list, waiting for the `(planned)` Realm above Domain (`Taxonomy.md` §Growth model). Later they could be **composed from library matter** (e.g. `Loam_Natural` + a scattered-`OakLeaf` layer) rather than shipped as one flat scan. Not counted in any class.

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Grass_Lawn_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Composed | Creases01 · Dust01 · — · Patches01 | ~Wet · ~Dry-out colour |
| 2 | `LeafLitter_Autumn_Clean_Base_s1_v01.mtlx` | Opaque | L3 | s1 | Composed | Creases01 · Dust01 · — · Patches01 | ~Wet · ~Dry-out colour |

**environmental/liquid** — 8

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Water_Clear_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | Now | Ripples01 · Dust01 · — · Patches01 |  |
| 2 | `Seawater_Natural_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | Now | Ripples01 · Dust01 · — · Patches01 |  |
| 3 | `Water_Murky_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | Now | Ripples01 · Dust01 · — · Patches01 |  |
| 4 | `Honey_Natural_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | Now | Ripples01 · Dust01 · — · Patches01 | ~Skin/film colour |
| 5 | `RedWine_Natural_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | Now | Ripples01 · Dust01 · — · Patches01 | ~Skin/film colour |
| 6 | `MotorOil_Natural_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | Now | Ripples01 · Dust01 · — · Patches01 | ~Skin/film colour |
| 7 | `WholeMilk_Natural_Clean_Base_s01_v01.mtlx` | Subsurface | L1 | s01 | Now | Ripples01 · Dust01 · — · Patches01 | ~Skin/film colour |
| 8 | `Coffee_Natural_Clean_Base_s01_v01.mtlx` | TranslucentThick | L1 | s01 | Now | Ripples01 · Dust01 · — · Patches01 | ~Skin/film colour |

**Frozen water — home undecided (O11), 2 articles not counted in any class above:**

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Snow_Fresh_Clean_Base_s1_v01.mtlx` | Subsurface | L3 | s1 | O11 | Pitting01 · Dust01 · — · Patches01 | ~Dirty-snow colour |
| 2 | `Ice_Clear_Clean_Base_s01_v01.mtlx` | TranslucentThick | L3 | s01 | O11 | Scratches01 · Cracks01 · — · Patches01 | ~Frost colour |

### 💡 utility

**utility/emissive** — 6

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Neon_Signage_Clean_Base_s01_v01.mtlx` | Emissive | L1 | s01 | ✅ | Scratches01 · Dust01 · Fingerprints01 · Grime01 |  |
| 2 | `LED_WarmWhite_Clean_Base_s01_v01.mtlx` | Emissive | L1 | s01 | Now | Scratches01 · Dust01 · Fingerprints01 · Grime01 |  |
| 3 | `LED_CoolWhite_Clean_Base_s01_v01.mtlx` | Emissive | L1 | s01 | Now | Scratches01 · Dust01 · Fingerprints01 · Grime01 |  |
| 4 | `Tungsten_Filament_Clean_Base_s01_v01.mtlx` | Emissive | L1 | s01 | Now | Scratches01 · Dust01 · Fingerprints01 · Grime01 |  |
| 5 | `Phosphor_Green_Clean_Base_s01_v01.mtlx` | Emissive | L1 | s01 | Now | Scratches01 · Dust01 · Fingerprints01 · Grime01 |  |
| 6 | `Lava_Molten_Clean_Base_s1_v01.mtlx` | Emissive | L2 | s1 | Now · O11 | Cracks01 · Pitting01 · — · Patches01 | ~Crust colour |

**utility/virtual** — 5 *(plus the system article `IMRSV_MissingMaterial`, which is outside the grammar and not counted)*

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Diagnostic_UVGrid_Clean_Base_s1_v01.mtlx` | Opaque | L2 | s1 | ✅ | — · — · — · — | none by design: reference articles stay pure |
| 2 | `Diagnostic_Checker_Clean_Base_s1_v01.mtlx` | Opaque | L2 | s1 | Now | — · — · — · — | none by design: reference articles stay pure |
| 3 | `GreyCard_Neutral18_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now | — · — · — · — | none by design: reference articles stay pure |
| 4 | `Spectralon_White_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now | — · — · — · — | none by design: reference articles stay pure |
| 5 | `MusouBlack_Matte_Clean_Base_s01_v01.mtlx` | Opaque | L1 | s01 | Now | — · — · — · — | none by design: reference articles stay pure |

*Rows 3–5 are the Physically Based calibration references (Pass 9 of the prior thread) — the natural anchors for the **Parity Baselines** Roadmap entry.*

**utility/energy** — 3 *(animated plasma is out of scope; these are static, pre-authored looks)*

| # | Filename | Master | Lane | Scale | Status | Overlays 1 · 2 · 3 · Mask | Also wanted |
|---|---|---|---|---|---|---|---|
| 1 | `Plasma_Blue_Clean_Base_s01_v01.mtlx` | Emissive | L2 | s01 | Now | Ripples01 · Scratches01 · — · Patches01 | (treated as a surface; S6 may remove) |
| 2 | `Hologram_Cyan_Clean_Base_s01_v01.mtlx` | Emissive | L2 | s01 | Now | Ripples01 · Scratches01 · — · Patches01 | (treated as a surface; S6 may remove) |
| 3 | `Forcefield_Hex_Clean_Base_s01_v01.mtlx` | Emissive | L2 | s01 | Now | Ripples01 · Scratches01 · — · Patches01 | (treated as a surface; S6 may remove) |

### Not in the list: biological matter (O9)

Skin (Physically Based carries 6 Fitzpatrick types with subsurface data), hair, bone and nails have **no class**, and hair is not a surface material in this model. They are the platform's one live pull (`PlatformDependencies.md` M1). Leather (textile #9) and ivory (mineral #8) sit on the same boundary.

### Shared wear-layer library (superseded the Pass 2 sketch in Pass 4)

Names follow the shipped forms `<Name><NN>_overlay_sNN.png` (overlays) and `<Name><NN>_sNN.png` (masks). Scale tags are set at authoring. Usage = how many articles in the list carry it.

**Overlays** (`MatterLibrary/textures/shared/overlays/`): 13, of which 2 shipped. Each one only bends the normal and/or roughens.

| Overlay | What it does | Used by (after C2) | |
|---|---|---|---|
| `Dust01` | fine roughening film | 144 | ✅ |
| `Scratches01` | directional scratches (normal + roughness) | 71 | ✅ |
| `Fingerprints01` | oily smudge prints (roughness) | 53 | new |
| `Cracks01` | hairline cracks (normal) | 27 | new |
| `Pitting01` | pits and pores (normal) | 29 | new |
| `Scuffs01` | broad rubbed scuff marks | 22 | new |
| `HairlineScratches01` | micro-scratches for polished and clear surfaces | 20 | new |
| `EdgeWear01` | chipped, rounded wear (normal) | 16 | new |
| `Ripples01` | surface ripples (normal only) | 11 | new |
| `Pilling01` | fibre pilling and fuzz (normal + roughness) | 10 | new |
| `Creases01` | folds and creases (normal) | 18 | new |
| `Crazing01` | glaze craze network (normal) | 3 | new |
| `WaterSpots01` | dried mineral spots (roughness) | 8 | new |

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
- **Names:** every stem, version included, is within 63 chars (the longest, `StainlessSteel_Brushed_Clean_Base_s001_v01`, is 42). Nothing here tests the budget.
- **Version:** every new article starts at `v01` (`NamingConventions.md`: the next free integer for that asset). `Identity.md` carries a `Reevaluate` on whether an article's *identity* includes `_vNN`: the filename and nodegraph names carry it, while the manifest and catalog `id` stop at `sNN` and hold the version as a separate field. That is owned by the release-bundle / consumer-contract phase and does not change these filenames.

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
- **The cap collides with the ruling.** **96 of 173 rows** have a third relevant overlay that doesn't fit (most often `Dust01` on scratched surfaces, `Fingerprints01` and `WaterSpots01` on glass). The ruling says all relevant layers; the contract says two. *(Open question L6. **Resolved by C2: cap raised to 3.** See Pass 5.)*
- ~~**The modulator rule collides with "smart" more deeply.** 121 rows want an effect that overlays cannot express at all (wet; moss, stains, tarnish, fading, yellowing, efflorescence).~~ **Overstated. Corrected in Pass 5:** it missed the Creator's `base_color_tint` and `roughness_bias`, which already give uniform colour and gloss changes. The real gap is *localised* colour or gloss only. *(Open question L7, narrowed.)*
- **7 shipped articles carry no overlays:** Limestone, Marble, Rust (mask only), Diamond, ABS, Lace, Neon. Under C1 each needs a new version. **Immutability** says that is `v02`, but the repo also has a recorded in-place `v01` precedent (the Version Management seed, from Issue #1). That call belongs to Version Management, not here. *(Open question L8.)*
- **Cost:** `MasterSet.md` notes that always-carried layers cost shader time even at strength 0. The VR-budget measurement that picks the strategy is marked `Reevaluate` (never recorded here). C1 makes that measurement load-bearing: every article now pays the cost.
- **Phase03 impact:** the `/matter-generate` skill, the recipe schema (G2) and the plausibility guard must author and check the layer assignment per article, and 17 new layer textures need producing. The Phase03 Brief doesn't include either yet. *(Recorded for `/discovery Phase03`; research does not edit the phase doc.)*

## Pass 5 — Correction after reading `LCDSchema.md` in full; the third overlay (C2, C3)

**Examined (2026-09-25):** `docs/specs/Contract/LCDSchema.md` in full (Pass 4 had grepped it for "overlay" only; that was the miss). The lead asked directly: "did you read the docs, or are we missing core functionality?"

**Answer: the docs are not missing core functionality. Pass 4 was.** The Creator subset is 8 frozen ports:
- `base_color_tint` (color3, multiply, 0–1 per channel);
- `roughness_bias` (float, add, −0.5…+0.5, total clamped to [0, 1]);
- `uv_scale` / `uv_offset` / `uv_rotation`;
- `overlay1_density` / `overlay2_density` / `maskset_blend`.

On top of those, the author tier carries every OpenPBR input per master (Lane A) and the TwoLayer set (Lane B). So:
- **Uniform wet** (darker and glossier) = `base_color_tint` down + `roughness_bias` negative. **Available today.** The same goes for uniform fading, yellowing and tarnish (tint) and for gloss changes (bias).
- **What is genuinely absent** is only the *localised* form: a colour or gloss change gated by a mask (moss in crevices, wet patches, rust streaks). Overlays roughen and bend normals only (the modulator rule; the assembler's B channel is [0, 1]), and a mask gates only overlays and the TwoLayer layer. The only localised colour today is **TwoLayer**. That is a refinement for later, not a hole in the contract. *(L7, narrowed.)*
- `LCDSchema.md` itself expects evolution: "frozen" means version-stable, and "new dimensions may be added over time as we see opportunity". **C2 is exactly such an addition.**

**Applied C2 to the list** (a script over the tables): each row's first `+X` became **overlay 3**. **96 rows now carry 3 overlays and 72 carry 2** (no third was relevant). The 5 virtual references carry none. **7 rows still want a fourth** (mostly glass wanting `WaterSpots01`); per **C3**, a sibling article covers that (e.g. `Glass_Clear_Weathered_Base` with water spots), not the cap.

**What C2 needs, for whichever unit lands it** (it is a contract change, and research does not edit specs):
- `MasterSet.md`: the cap `≤2` becomes `≤3`, and the channel contract gives **A = overlay-3 gate** (A is "reserved (unused in v1)").
- `LCDSchema.md`: a 9th Creator port, `overlay3_density`, and a third render-role node `overlay3_tex`. *(Names are proposed by pattern; not yet ruled.)*
- The assembler (`LCD_PORTS`), the validators, the Blender add-on and every consumer master (the IMRSV/Unreal side goes in `PlatformDependencies.md`).
- The **shader-cost measurement** (`MasterSet.md`, `Reevaluate`) becomes more pressing: every article now carries up to 3 layers at strength 0.
- Probably a library **semver-minor**: an additive port.

## Pass 6 — Does the filename capture the layers? (worked examples)

*Names in this pass predate C5 (Pass 7), which moved species into Material and gave each token a fixed axis.*

**Examined (2026-09-25):** `tools/converters/recipes/Concrete_Smooth_Worn_Dusty_s1_v01.json`; `library/releases/matterlib-0.1.0.lock.yaml` (article and texture entries); `matterlib-0.1.0.catalog.json` (the Concrete entry). The lead asked: "do we have a way to capture everything in the filename layout?"

**No, and by design it shouldn't.** Each fact has its own home:

| What | Where it lives | Example (Concrete, shipped) |
|---|---|---|
| **Which look** this article is | the **filename** | `Concrete_Smooth_Worn_Dusty_s1_v01.mtlx` |
| **Which base pixels** | the **base texture set**, named independently and shared across articles (the original design: "Steel clean, Steel dusty, Steel brushed could all use base set `CleanSteel01`"; the shipped sets happen to reuse the first three tokens; texture-set naming was deferred and is unsettled) | `textures/base/engineered/cementitious/Concrete_Smooth_Worn_{basecolor,normal,roughness}_s1.png` |
| **Which layers**, and their default strengths | the **recipe** (`overlays[]`, `maskset_tex`, `lcd_defaults`), assembled into the `.mtlx` (`overlay1_tex`, `overlay2_tex`, `maskset_tex`) | Dust01 → `overlay1_density`, Scratches01 → `overlay2_density`, both at the default 0 |
| **That the layer textures are pinned** | the release **lock**: one texture entry per shared layer | `shared/overlays/Dust01`, `shared/overlays/Scratches01` |
| **What an app's picker sees** | the release **catalog** | `id`, `domain`, `material_class`, `scale`, `version`, `payload_path`: **no layers, no master** |

**The grammar has a fixed six-token shape, so a name can be parsed back into its parts** (lead, 2026-09-25; ruling C4): `Material _ Variant _ Condition _ Detail _ sNN _ vNN`, exactly five underscores. **Layer information goes *inside* the fixed slots, never in extra ones.** `Condition` carries the state of the base matter (`Distressed`, `Weathered`, `Worn`), and `Detail` carries the dialled-in layers as **one PascalCase token** (`Dusty`, `Scratched`, `ScuffedDusty`).

The original library README's own examples show exactly this. They were deliberately over the top, to show how much a single token can hold (`Identity.md`, kept as grammar fixtures):
- `Limestone_Veined_Distressed_Dusty_s01_v01`: the canonical example. Distressed = the base state, Dusty = the dust layer dialled in.
- `Limestone26b_Veinish_VeryDistressed12_ScratchedButNotVeryDusty_s01_v32`: 70 chars, the **must-fail** case (over budget, but still six tokens). Its `Detail` packs two layers and their strengths into one token.
- `Limestone26b_Veinish_VeryDistressed_Scratched_s01_v32`: 53 chars, the **must-pass** worst case.

So a layered sibling is named inside the six slots:
- `Oak_White_Worn_ScuffedDusty_s01_v01`: 35 chars
- `Glass_Clear_Clean_Fingerprinted_s01_v01`: 39
- `StainlessSteel_Brushed_Clean_ScratchedSmudged_s001_v01`: 54

**What the name does NOT carry** is the *inventory* of layers an article holds at 0 (C1). That lives in the recipe and the `.mtlx`; the name says only what is dialled in.

⚠ *An earlier draft of this pass (never committed) illustrated "layers in the name" by appending one extra token per layer (nine tokens in all). That broke the fixed shape, and was withdrawn at the lead's correction.*

**Worked examples: how C1 (all layers, at 0) and C3 (sibling articles) read in names:**

| Article | Base set it uses | Layers (defaults) | Reads as |
|---|---|---|---|
| `Oak_White_Clean_Base_s01_v01` | `Oak_White_Clean` | Scuffs01 · Scratches01 · Dust01 · Grime01 (all 0) | new oak; the app dials wear up |
| `Oak_White_Clean_Scuffed_s01_v01` *(C3 sibling)* | `Oak_White_Clean` (the **same pixels**) | same layers; Scuffs01 at e.g. 0.6 | a *preset*: same material, wear pre-dialled |
| `Oak_White_Weathered_Base_s01_v01` | `Oak_White_Weathered` (**different pixels**: a weathered scan) | Dust01 · Cracks01 · — · Crevice01 (0) | a different matter state, so a different base set |
| `Concrete_Smooth_Worn_Dusty_s1_v01` ✅ | `Concrete_Smooth_Worn` | Dust01 · Scratches01 (0) · no mask | *shipped:* named Dusty, but dust defaults to 0 |
| `Glass_Clear_Clean_Base_s01_v01` ✅ | *(param-only)* | Dust01 · Scratches01 · Grime01 (**0.25 / 0.35 / 0.6**) | *shipped:* named Clean, but wear is pre-dialled |
| `Rust_OnSteel_Flaking_Base_s01_v01` ✅ | `Rust_OnSteel_Flaking` + layer 2 | mask RustBloom01 at **0.85**, no overlays | TwoLayer: the mask *is* the material, so it can't default to 0 |

**Findings:**
- **The grammar holds, with six fixed tokens.** The name carries the *look* (`Condition` = the base state, `Detail` = the dialled-in layers as one PascalCase token), the base set carries the *pixels*, and the recipe/`.mtlx` carries the *layer inventory*. C3 siblings fall out naturally: **same base set, different `Detail`** (`Clean_Base` → `Clean_Dusty`). A different `Condition` usually means different pixels.
- **The validator does not enforce six tokens.** `check_grammar` in `tools/validators/validate_material.py` requires only **≥ 4** tokens, plus a valid scale tag and version in the last two. So a nine-token name within 63 chars passes today. Enforcing exactly six (with the one system exemption) is a small guard for Phase03's harness, where an agent authors names. *(New question L10.)*
- **The two shipped precedents contradict each other on what `Clean`/`Detail` mean.** `Glass_Clear_Clean_Base` ships with wear pre-dialled; `Concrete_…_Dusty` ships with dust at 0. Under C1 the consistent rule would be: **`Clean_Base` ⇒ all layer defaults 0; a `Detail` word ⇒ that layer's default is dialled up.** Both shipped articles break it, in opposite directions. *(New question N8; fixing either one means a new version, which ties to L8.)*
- **Apps can't see an article's layers without opening the `.mtlx`.** The catalog carries no layer list (nor the master). A picker that wants to show "this oak has scuffs, scratches and dust" can't. A `layers` field is a catalog `schema_version` change, and belongs to *Release Bundle and Consumer Contract* / *See the Library*. *(New question L9.)*

## Pass 7 — The axis structure applied to the whole list (ruling C5)

**What changed (one scripted pass, 2026-09-25):**
- **89 rows renamed.** Species and alloys moved into `Material` (`Oak_White` → `WhiteOak_Natural`, `Steel_Mild` → `MildSteel_Raw`). The look moved into `Variant`: finish (`Polished`), weathered or wet scans (`Weathered`, `Wet`), or `Natural`. Every new row is `…_Clean_Base`, meaning all layer sliders at 0.
- **Overlay slots reordered:** damage layers first, then deposits (`Dust01`, `Fingerprints01`, `WaterSpots01`). No layer was added or dropped.
- **The 11 shipped articles keep their names** (immutability).
- **Checked:** all 173 names are six tokens, no duplicates, longest 43 chars.

**Demo — the axes in use (3 of the list's articles, each with user-style siblings):**

| Name | Look (Variant) | Damage (Condition → overlay 1) | Deposits (Detail → overlays 2–3) |
|---|---|---|---|
| `WhiteOak_Natural_Clean_Base_s01_v01` | untinted | Scuffs01 at 0 | Scratches01, Dust01 at 0 |
| `WhiteOak_Blue_Worn_Base_s01_v01` | tinted blue | scuffs up | 0 |
| `WhiteOak_Blue_VeryDistressed12_Dusty_s01_v01` | tinted blue | scuffs high, 12th save | dust up |
| `StainlessSteel_Brushed_Clean_Base_s001_v01` | brushed | HairlineScratches01 at 0 | Fingerprints01, Dust01 at 0 |
| `StainlessSteel_Brushed_Scratched_Smudged_s001_v01` | brushed | scratches up | fingerprints up |
| `Concrete_Stained_Worn_Dusty_s1_v01` | stained | Cracks01 up | Dust01 up |

**Edge cases the pass turned up (for the lead's hunt):**

| # | Edge case | Rows | Options |
|---|---|---|---|
| E1 | **Resolved (lead, 2026-09-25): option (a).** **Two damage layers, so slot 2 holds damage, not a deposit.** E.g. wood carries Scuffs01 + Scratches01 + Dust01; soil carries Cracks01 + Pitting01. The rule "overlays 2–3 = deposits" breaks. | 59 | (a) **Condition = overlay 1 only; Detail = everything else.** The original example `ScratchedButNotVeryDusty` already puts a damage word in Detail, so there is precedent. (b) Move the second damage layer to a C3 sibling. **Recommend (a).** |
| E2 | **The tint doesn't reach see-through colour.** `base_color_tint` multiplies `base_color` only (`assemble_mtlx.py`). `transmission_color`, the colour of glass, gems and liquids, is fixed by the author. So `Glass_Blue` can't be made by tinting `Glass_Clear`; it has to be its own article. | glass, gems, liquids, clear plastics (~30) | Accept: for these, Variant colour means an authored article, not a Creator tint. Or add a Creator transmission tint (an LCD change). |
| E3 | **Shipped names break C5.** `Marble_Veined_Polished_Base` and `Copper_Verdigris_Aged_Base` put a look word (`Polished`, `Aged`) in the damage slot. `Glass_Clear_Clean_Base` is named Clean but ships with wear pre-dialled. `Concrete_Smooth_Worn_Dusty` fits C5 but ships its sliders at 0. | 4 | Fix at their next version (ties to L8), or accept them as legacy. |
| E4 | **TwoLayer damage can't be 0.** `Rust_OnSteel_Flaking`, `Paint_OnWood_Peeling`, `Paint_OnMetal_Chipped`: the mask-driven layer 2 *is* the material, so Condition is non-`Clean` at the library default. | 3 | Accept: on TwoLayer, Condition names the layer-2 state. |
| E5 | **The default Variant word.** `Identity.md` says "use `Base` if none"; this list uses `Natural` (untinted). | ~70 | Adopt `Natural` in `Identity.md`, or revert to `Base` (`WhiteOak_Base_Clean_Base`). |
| E6 | **Species vs type.** Species went into Material (`WhiteOak`, `BeachSand`, `RedWine`), but type words stayed as the look (`Topsoil_Forest`, `Grass_Lawn`, `Cardboard_Kraft`, `Nylon_Ripstop`). The line between "a kind of matter" and "a look" is a judgement call. | ~10 | A rule of thumb: if you'd tint it into existence, it's Variant; if not, it's Material. |
| E7 | **`Ripples01` counted as damage** (it changes the surface shape) on liquids and energy. | 11 | Accept, or treat liquid ripples as their own axis. |
| E8 | **Colour-as-identity in emissive and utility:** `LED_WarmWhite`, `Phosphor_Green`, `Plasma_Blue`, `Spectralon_White`. The colour is the emission colour or a reference value, not a tint. | ~8 | Accept as the look (same as E2). |

## Gut-check questions — for the lead

Naming (each has a recommendation; this draft already follows it). *N1, N2, N4, N5 and N8 are superseded by C5 (Pass 7).*

| # | Question | Draft follows | Alternative |
|---|---|---|---|
| N1 | `Material` = the most specific substance (`Oak`, `Denim`, `ABS`)? | yes (precedent: `Limestone`, `Lace`, `ABS`) | class-word first: `Wood_Oak`, `Fabric_Denim` |
| N2 | A two-word substance is one token (`StainlessSteel`, `CarbonFibre`, `BrickClay`)? | yes | `Steel_Stainless…`, which uses up the Variant slot |
| N3 | British spelling (`Aluminium`, `Fibre`, `Grey`, `Galvanised`)? | yes (the docs write "colour") | US spelling. **Either way, write it into `NamingConventions.md`**, since names are permanent after release |
| N4 | A finish (Polished, Honed, Weathered, Wet) goes in `Condition`; a structure (Brushed, Veined, Reeded) goes in `Variant`? | yes (precedent: `Marble_Veined_Polished`) | — |
| N5 | A colour word in `Variant` only when the colour *is* the matter (`Sapphire_Blue`, `Glass_Green`), never for paint or plastic, where colour is the Creator tint? | yes | — |
| N6 | Param-only (L1) articles carry `s01`, as the shipped ones do? | yes | `sUKN` (more honest: there is no texture to scale) |
| N7 | Layered articles use `<Top>_On<Substrate>` (`Paint_OnWood`, after `Rust_OnSteel`)? | yes | — |
| N8 | `Clean_Base` ⇒ every layer default is 0; a `Detail` word (`Dusty`, `Scuffed`) ⇒ that layer is pre-dialled, and the sibling shares the base set (Pass 6)? | yes | keep the shipped mix (Glass is `Clean` but pre-dialled; Concrete is `Dusty` at 0) |

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
| L1 | Naming rulings N1–N8 | Names are permanent once released (immutability). |
| L2 | Structure rulings S1–S6 (the rest of O11) | 22 rows have a provisional class. |
| L3 | Is **thin film** a fourth carrier (C4)? | Nacre, and later soap bubble and oil sheen. |
| L4 | Ship the 8 C1 metals approximated in the first release, or hold them for F82? | Metals are the class users reach for first. |
| L5 | Is this the **first release**, or the eventual coverage target? At 5–10 min review each (unmeasured), 162 new articles is roughly 15–25 hours. | Decides whether to cut a smaller first tranche. |
| ~~L6~~ | ~~Raise the overlay cap?~~ **Resolved by C2: raise to 3.** Landing the contract change is open (which unit: a `/quick-fix` on the specs plus the assembler, or a step in Phase03). | — |
| L7 | *Narrowed in Pass 5.* **Localised colour or gloss** (moss only in crevices, wet only in patches): is it wanted, and when? Uniform colour and gloss already exist (`base_color_tint`, `roughness_bias`). | A refinement, not a gap. It does not block the list. |
| L8 | Do the 7 shipped articles without overlays get `v02`, or the in-place `v01` precedent? | Version Management owns it. |
| L9 | Should the release catalog list each article's layers (and master), so an app can show them without opening the `.mtlx`? | A catalog `schema_version` bump, owned by *Release Bundle and Consumer Contract*. |
| L10 | Enforce **exactly six tokens** in `check_grammar` (today ≥ 4)? | An agent authoring names needs the guard. A small harness fix (Phase03 G-series or a `/quick-fix`). |

## Status

**Passes captured:** 7 (2026-09-25).

- **E1 resolved (lead): (a).** Condition = overlay 1 (the primary damage) only; Detail = overlays 2–3, whatever their kind (`ScratchedButNotVeryDusty` is the precedent). The 59 two-damage rows stand as they are.

- **C6 (lead):** composed materials are out of the matter list. `LeafLitter_Autumn` and `Grass_Lawn` moved to *Composed (planned)*; `MapleLeaf` and `IvyLeaf` added, so vegetation stays at 6; `Topsoil_Forest` flagged `Composed?`.

- **Pass 7: C5 applied.** Each name token is a fixed axis: Material = matter/species · Variant = the look (texture + tint + settings) · Condition = damage (overlay 1) · Detail = deposits (overlays 2–3). 89 rows renamed, overlay slots reordered, all 173 names checked (six tokens, unique, ≤ 43 chars). **Eight edge cases (E1–E8)** are listed for the lead's hunt; E1 (59 rows with two damage layers) is the big one.

- **Pass 6: the filename grammar holds with layers, in six fixed tokens (C4).** The name = the look (`Condition` = base state, `Detail` = dialled-in layers as one token, e.g. `Distressed_Dusty`); the base set = the pixels; the recipe/`.mtlx` = the layer inventory. The validator checks only ≥ 4 tokens (L10). Two new items: **N8** (make `Clean_Base` mean all layers at 0, and `Detail` mean a pre-dialled preset; the two shipped precedents disagree) and **L9** (the catalog doesn't list layers).

- **Lead rulings:** C1 *smart, not lean* (all relevant layers, at strength 0, names unchanged) · C2 *overlay cap raised to 3* · C3 *several articles per matter may carry different overlay sets*.
- **Draft v1 of the list is complete:** 173 named articles (11 shipped, 162 new) across all 20 classes, including 2 unplaced (snow, ice). Every row has a full stem, a folder, a declared master, a lane, a scale tag, a status and **its wear layers**: 96 carry 3 overlays + mask, 72 carry 2 + mask, and the 5 virtual references carry none. The shared layer library grows from 5 to 22.
- **Pass 4 overstated a gap and Pass 5 corrects it:** uniform colour and gloss (wet, fading, tarnish) are already Creator controls (`base_color_tint`, `roughness_bias`). Only *localised* colour or gloss is absent (L7, a refinement).
- **C2 is a contract change still to land** (`MasterSet.md`, `LCDSchema.md`, assembler, validators, Blender, consumers). Pass 5 lists what it touches.
- **140 new articles are buildable with the Phase03 tools alone** (20 of them in a provisional class). The rest wait on carriers C2 (10), C3 (3), optionally C1 (8), or a class ruling (snow, ice).
- **Direction:** nothing is committed. This is input for the lead's gut check, and later for the *Library Coverage* phase.
- **Open:** L1–L10. None blocks Phase03's first step, but C1 widens Phase03's scope: the skill must author the layers, and 17 layer textures must be produced. `/discovery Phase03` should pick that up.
- **Next step:** the lead marks up the list (rename, cut, add, move), and rules N1–N7 and S1–S6 where they have a view. The naming rulings then land in `NamingConventions.md` / `Identity.md` through a `/quick-fix`, and the class rulings in `Taxonomy.md`. A later pass here re-issues the list as v2.
