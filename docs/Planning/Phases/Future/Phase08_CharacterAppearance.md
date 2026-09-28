# Phase08 — Character Appearance for Studio

**Status:** IN EXECUTION (2026-09-28, `/execute P8`). Discovery complete the same day (Pass 1; the Brief is complete). Lane: `build` (verified, §Risk lane).
- **Seeded** 2026-09-28 from `docs/Planning/Research/260928_R_PlatformAppearanceAsks.md` (the platform's asks, Passes 1–4; the library's review, Passes 5–6).
- **Numbered by the lead, 2026-09-28**: first as Phase09 (*"seed Phase09 with items 1–3.. I would like to address this issue now"*), then as **Phase08** the same day (*"make this Phase 8, mark the current Phase8 as TBD - we have many other little things to get in here befoer we build out the full library"*). Library Coverage, which held Phase08, is now unnumbered (`PhaseTBD_LibraryCoverage.md`). *(Anything written before 2026-09-28 that says "Phase08" means Library Coverage, not this phase.)*
- **Why now:** the IMRSV platform's Appearance phase (Phase 66) is under way and focused on Studio. Its skin and hair sittings wait on this phase (`PlatformDependencies.md` **M3**, **M4**); the lead: *"We need to update things in the matter library to address the needs of Studio."*

## Outcome

**In Studio, a Creator can give a character any hair colour from one good hair material, pick any of six skin tones and have the lips and nails match, and dress it in clothes whose fabrics, soles included, come from the library in any colour.**

Concretely, at close:
- a `Hair` master token and **one light hair article** that `base_color_tint` takes to any hair colour;
- **lips and nails for each of the six skin tones**, paired to each skin by name;
- **the first wardrobe fabrics**: rubber, a light leather and a lighter denim, then as many of canvas, felt, satin, a stretch knit and a wool suiting as the phase holds;
- every new article a `candidate`, seen side by side in the rig (on the MakeHuman body where it has a part there), in Blender's Asset Browser, and served to Studio through the dev install (Phase07 L4).

---

## The Brief

### First human test

No running service. The lead judges the rig's picture sheets, Blender's Asset Browser, and (the platform's check) Studio through the dev install. The agent runs every command.

1. **The hair article's slider sweep** (rig sheet, test scene). **Expect:** one light hair article whose Base Color Tint moves it through browns to near-black, and to red and auburn, the same in both columns. *(8.1)*
2. **Blender 5.2** → Asset Browser → Matter library → `biological / keratin` → the new hair article on a cube → Base Color Tint. **Expect:** the same colour range as the sweep. The asset is tagged `candidate` and its master is `Hair`. *(8.1)*
3. **The character sheet with the new hair** on the bob, brows and lashes. **Expect:** strands cut out, not solid cards; light hair; nothing magenta. *(8.1)*
4. **The character sheets for skins I, IV and VI**, each with its own lips and nails. **Expect:** the lips and nails sit with each tone: no pink lips on type VI, no dark lips on type I. *(8.2)*
5. **The character's feet and waist views.** **Expect:** rubber soles distinct from the leather uppers; the uppers in the light leather; the jeans in the lighter denim. *(8.3)*
6. **One sheet per further fabric** (canvas, felt, satin, stretch knit, wool suiting, as many as land). **Expect:** each reads as its fabric, and its tint sweep recolours it. *(8.4)*
7. **Studio** (the platform's check; `PlatformDependencies.md` P19). **Expect:** picking a skin tone offers that tone's lips and nails by name; the fabrics recolour. **The hair shows only once Studio has its own Hair master:** until then, the platform fails loud on the new token (research Pass 4). *(The close's hand-off.)*

**Reconciled with the steps:** clicks 1–3 are 8.1's. Click 4 is 8.2's (it needs the rig to pick lips and nails by the skin's tone; built in 8.2). Click 5 is 8.3's (it needs the shoe split in the rig; built in 8.3). Click 6 is 8.4's. Click 7 is the close's hand-off; the dev install serves every new article from the moment it lands, so nothing extra is built for it.

### In now

1. **The `Hair` master, settings-only** (RD-P08-1): the token (the 8th), its row in `MasterSet.md`'s master table and its settings row (masked coverage, a **hair** shading model, two-sided, no refraction), and every tool that knows the tokens (F-P08-2). In Blender and USD viewers it is the Masked graph; the article stays `open_pbr_surface`.
2. **`Hair_Natural_Clean_Base_s001_v01`** on `Hair` (RD-P08-2): a light, low-melanin fibre whose untinted look is the lightest natural hair, with the same cut-out input, cutoff and anisotropy as `Hair_DarkBrown`. `Hair_DarkBrown` stays as it is, on Masked.
3. **Lips and nails per tone** (RD-P08-3): `Lips_FitzpatrickI…VI` and `Nail_FitzpatrickI…VI` (twelve articles), each derived from its skin's albedo by one written rule (F-P08-1). `Lips_Natural` and `Nail_Natural` stay.
4. **Wardrobe fabrics, first tranche:** `Rubber_Natural` (`synthetic/polymer`, RD-P08-6), a light `Leather_Natural` and a lighter denim wash, each authored light so the tint reaches its colours (RD-P08-5).
5. **Wardrobe fabrics, second tranche**, in this order until the phase is done: canvas, satin, felt, a synthetic stretch knit, a wool suiting (F-P08-6). Judged on the article sheet, not on outfits (RD-P08-4).
6. **The rig**: the cast takes the new hair; `--character <skin>` binds that tone's lips and nails; `shoes01` is split into upper and sole, as the jeans are split from the shirt.
7. **The hand-offs**: `PlatformDependencies.md` M3 and M4 closed on the library side; Phase06's coupling note (a Hair master in the Unreal runtime, F-P08-3); `Glossary.md`; `Experience_MatterLibrary.md` §Shipped; the Library Coverage doc's rows that were pulled forward.

### Not now

- **Who splits Studio's garments into their fabrics** (research A6). The platform's garment meshes are platform-side (Phase07 §Not now: *"The platform's hair and garment meshes and their atlases (mesh assets…)"*), so the split is `PlatformDependencies.md` P15's garment half. The rig splits **its own** copy of a shoe only to judge rubber on a sole.
- **Colour on layers** (CM-Q5): garment prints, trims and fades, and makeup (research A7). A contract change; it stays with Library Coverage (L3).
- **A real skin-tone control** (research A4): a change to the frozen Creator vocabulary.
- **`chiang_hair_bsdf`** (AP-Q1). It would be the first article whose shader is not `open_pbr_surface`, which Decision of record 1 rules out. It returns only if the lead reopens that decision.
- **Dressing the rig in more outfits** for the second tranche (each outfit needs its own split).
- **A release** (Phase07 L4). The review's cleanups (the Glossary's retired-proxy row; `check_lcd_carrier.py` not seeing `cutout_map`): `/retro` or `/quick-fix`.

### Reuse check: what the stack already gives us

| Need | What exists | Evidence (2026-09-28) |
|---|---|---|
| A tintable colour | `base_color_tint`, a frozen Creator port: **multiply, 0–1** | `LCDSchema.md` §Creator subset |
| A card cut-out, supplied at binding | `cutout_map` + `opacity_cutoff` on Masked (Phase07 7.6); the assembler, the Blender masters and the rig all handle it | `LCDSchema.md` §Cut-out map; `assemble_mtlx.py`; `job.py` |
| The fibre highlight | specular anisotropy (carrier C3) | `LCDSchema.md` §Author tier |
| A master that differs only in its settings | the settings table already maps a shading model per master (Subsurface → *subsurface*) | `MasterSet.md` §Material-settings intent |
| Making articles | `/matter-generate` (Phase03): recipe → assemble → gate → preview | `.claude/skills/matter-generate/` |
| Fabric textures | `tools/converters/base/gen_fabrics.py` (the 1 cm jersey, twill and leather sets) with provenance | read |
| Tint judged across its range | `rig.py --sweep` sweeps every declared port on the test scene | `rig.py` |
| Everything reaching people | `working_tree.py` → `serve_to_stage.py` (USDLiveView; Studio via P19) and `gen_asset_library.py` (Blender) read every `.mtlx` on disk, with status and master | read |
| A garment split in the rig | `build_character.py` `MESHES` split rules (the jeans from the shirt by UV rectangles) | read |

**No custom layer is proposed.** The Hair token is the master mechanism the spec already has; every article is a recipe.

### Decisions that bind

- **Standing:** CM1 (`biological`) · CM2 / D1 (substance only; mesh-bound pictures are never in an article) · L1 (one part per substance) · L2 (the mesh supplies the cut-out; *"a `Hair` master is probed only if Masked hair looks wrong"*) · L4 (no release; Studio takes the dev install) · C1 (wear layers ship at 0) · C4 / C5 (six parseable tokens; Variant = the look, tint included; `Natural` = untinted) · D-S (status in the recipe) · "no versioning" before the first release (lead, 2026-09-25).
- **RD-P08-1 — The `Hair` master is settings-only; its articles stay `open_pbr_surface`.** Answered by `_Architecture.md` Decision of record 1: *"The article shader is `open_pbr_surface`."* That decides the graph, so the Chiang option is out unless the lead reopens it. A master is *"a graph plus a settings block"* (`MasterSet.md`), and the settings table already gives Subsurface its own shading model, so a master that differs only in settings is the spec's own pattern. **L2's condition is met:** the platform reports the Masked cards read as plastic in Unreal (research Pass 3). **Not D-E:** the Eye master was refused for inputs the other targets lack; this master adds no input. It changes how Unreal shades the same article.
- **RD-P08-2 — A new light hair article, named `Hair_Natural`; `Hair_DarkBrown` is kept on Masked.** Under C5, `Natural` is the untinted look, and the untinted look of a tintable hair is its light base. Keeping `Hair_DarkBrown` on Masked means nothing Studio uses today changes (research Pass 4). Re-authoring it in place would make its name false.
- **RD-P08-3 — Lips and nails pair with a skin by the Variant token** (`Skin_FitzpatrickIV` ↔ `Lips_FitzpatrickIV` ↔ `Nail_FitzpatrickIV`). Answered by `Identity.md`: *"Exactly six tokens … so a name always parses back into its axes"* (C4). Under C5 the Variant is the look, and the skins already carry the tone there. So the pairing is spec-native and needs no contract change. A served-catalog field would change the runtime catalog, which is the release-bundle phase's, and Stage drops keys it does not know (Phase07 F9). The platform left the choice to the library (research A2).
- **RD-P08-4 — Brows and lashes keep one article with the hair.** Phase07 7.6 bound one hair article to all three. Each card mesh already gets its own Material instance for its cut-out (P17), so Studio can tint brows apart from the hair. Which article Studio binds to brows is its binding.
- **RD-P08-5 — Anything Studio recolours is authored at its lightest plausible colour.** `base_color_tint` only darkens (F-P08-1). This applies to the hair, the leather and the denim. The rubber is the one exception: it may be dark, since a Creator rarely lightens a sole.
- **RD-P08-6 — Rubber is `synthetic/polymer`.** Taxonomy has no `rubber` class (it is a validator RED fixture's example of a missing class), and the Library Coverage list places `Rubber_Natural` in polymer (*"elastic, foamed, cast or waxy → polymer"*).
- **Bars** (as Phase07): Masked and Hair are judged like Lace (the whole set advisory, the close-up graded); fabrics are Opaque, ΔE < 2; lips are Subsurface, "recognisable".

### Risk lane: `build` (verified)

The controls, read 2026-09-28:
- The **release lifecycle** (`library/releases/`, `freeze` / `promote`) is untouched: no release is cut (L4).
- **`run_all.py`:** `catalog_freshness` re-projects release lockfiles only; `provenance_gate` drives fixtures only; `determinism` re-assembles every recipe (new ones included) and proves existing articles byte-stable; `materials` validates every `.mtlx` by its master. The `materials` lane must learn `Hair` or a Hair article passes unchecked; that is the lane doing its documented job for a token the lead put in scope, not a new gate.
- **`tools/conformance/codec_ab.py`** lists graded classes (`TIGHT_CLASSES`). Editing it puts the change under `tools/conformance/`, so **`check_exporter.sh` is baselined before the edit** (LOCAL_DELTAS, the RUN row). `check_asset_library.sh` runs after the Blender library is regenerated.
- The contract edits (`MasterSet.md`, `LCDSchema.md`, `recipe.schema.json`) are additive: adding a token is semver-minor (`MasterSet.md` §Master tokens).
- No authorization, secrets, destructive migration or public edge is involved. **The push is the lead's, and it is irreversible (a public repo).**

### Step list

- **8.1 — Any hair colour from one hair material.** The `Hair` token through `MasterSet.md`, `LCDSchema.md` (the cut-out input is now Masked's and Hair's) and every tool (F-P08-2), including `ML_Hair` in the Blender masters (a version bump). Then `Hair_Natural` on it via `/matter-generate`; the rig's hair cast moves to it. *(Clicks 1–3.)* **Push after it:** the platform's Hair master and Phase06's runtime build against the token.
- **8.2 — Lips and nails that match each skin tone.** One written derivation rule; the twelve articles; `rig.py --character <skin>` binds that tone's lips and nails by the shared Variant. *(Click 4.)*
- **8.3 — Soles, shoes and jeans from the library.** `Rubber_Natural`, `Leather_Natural` and the lighter denim (textures via `gen_fabrics.py`, with provenance). The rig's `shoes01` is split into `Shoes` and `Soles`, and the cast gains the new fabrics. *(Click 5.)*
- **8.4 — More fabrics for the wardrobe.** Canvas, satin, felt, stretch knit and wool suiting, in that order, each a recipe and an article sheet with its sweep. Stop where the phase is done; the rest stays on Library Coverage's list. *(Click 6.)*
- **Close.** `PlatformDependencies.md`: M3 and M4's library side done. Phase06's coupling note. `Glossary.md` (the `Hair` master). `Experience_MatterLibrary.md` §Shipped. `PhaseTBD_LibraryCoverage.md`: the rows built here, and its stale C2/C3 blockers (F-P08-6). Studio's check (click 7) handed to the platform.

**Why this order:** 8.1 carries the only contract change, and two other parties (the platform's Studio and Phase06's runtime) build against it, so it goes first and is pushed. 8.2 unblocks Studio's skin-tone control with no contract change. 8.3 dresses the character. 8.4 is open-ended, so it goes last.

**Split signal (raised, not cut):** these are three independently demonstrable journeys (hair, tones, fabrics), which is a split trigger. They stay one phase: the lead seeded them together (*"seed Phase09 with items 1–3"*), they share one entry path (the dev install and the rig's character), and none is expected to exceed an hour to its first click. Cut only if 8.1 grows past one step.

### Compact build map

- **The token** (8.1): `docs/specs/Ontology/MasterSet.md` (v1 table → 8 masters, the settings row, §Master tokens, the Masked row's *"planned probe"* resolved, the coverage line, History) · `docs/specs/Contract/LCDSchema.md` (§Author tier row; §Cut-out map: Masked **or Hair**) · `tools/converters/assemble_mtlx.py` (`KNOWN_MASTERS`; the `cutout_map` guard at `spec.master != "Masked"`) · `tools/converters/recipe.schema.json` (the `master` enum) · `tools/validators/validate_material.py` (the Masked branch serves Hair too) · `blender/masters/build_masters.py` (`MASTER_PARTS["Hair"] = {"opacity"}`, `VERSION` bump) · `tools/parity/rig.py` (`GRADED`, `ADVISORY_VIEWS`) · `tools/conformance/codec_ab.py` (`TIGHT_CLASSES`; baseline `check_exporter.sh` first) · `tools/parity/JOB_FORMAT.md` (the master list) · `blender/asset_library/MatterLibrary.blend` regenerated.
- **Articles:** recipes in `tools/converters/recipes/`; `.mtlx` in `MatterLibrary/materials/biological/{keratin,tissue}/`, `synthetic/{textile,polymer}/`; fabric textures in `MatterLibrary/textures/base/synthetic/…` with provenance YAML under `library/provenance/sources/base/…`.
- **Rig:** `tools/parity/rig.py` (`CHARACTER_CAST`; lips and nails by the skin's Variant) · `tools/parity/scene/build_character.py` (`MESHES`: the shoe's sole split; rebuild the scene) · `job.py` (the new part's mask colour).
- **Hand-offs:** `docs/Planning/PlatformDependencies.md` · `docs/Planning/Phases/Future/Phase06_UnrealTestRuntime.md` · `docs/Glossary.md` · `docs/specs/Experience/Experience_MatterLibrary.md` · `docs/Planning/Phases/Future/PhaseTBD_LibraryCoverage.md`.
- **Tests:** existing only (`run_all.py`, `check_asset_library.sh`, `check_exporter.sh`) plus the rig sheets. No new gate.

---

## Discovery Log

### Pass 1 (2026-09-28): the product docs, top-down, read against the Outcome

**Examined:** `_Architecture.md` (the LCD principle, Decisions of record 1 and 9) · `Identity.md` (C4, C5) · `Taxonomy.md` · `MasterSet.md` · `LCDSchema.md` · `Consumers.md` · the research thread (`260928_R_PlatformAppearanceAsks.md`, `260927_R_CharacterMaterials_MPFB2.md`) · `Phase07_CharacterMaterials.md` (L1–L4, D-E, the close) · the Library Coverage list (`260925_R_LibraryCoverage_FirstRelease.md`: textile and polymer rows, E6, N1–N8 superseded by C5) · D2 (`260923_R_AgenticMaterialGeneration.md`) · `Phase06_UnrealTestRuntime.md`. **Tree:** every reader of the master token, every Masked special case, `working_tree.py`, `serve_to_stage.py`, the rig's character job, `run_all.py`'s enumerating lanes, and the hair, lips, nail, skin I–VI, leather and denim recipes. **Learnings:** Blender (B3 per-article interface defaults, B5, B9 anisotropy), MaterialX (M4), Storm (S5 cut-out edges, S8, S9) apply. **Tree grep for the phase's own names** (`Rubber`, `Leather_Natural`, `Lips_Fitz`, `Nail_Fitz`, `Hair_Natural`, `"Hair"`, `ML_Hair`, the second-tranche fabrics): **nothing built**. `rubber` appears only as a RED fixture's missing class.

**Findings:**
- **F-P08-1 — A tint only darkens, and one shipped article assumes otherwise.** `base_color_tint` is a 0–1 multiply. `Hair_DarkBrown` is `(0.090, 0.052, 0.030)`, and `Leather_Brown` is `(0.16, 0.07, 0.03)`. `Lips_Natural` is `(0.52, 0.26, 0.24)`, and its recipe says *"a Creator tints it to sit with a darker **or lighter** skin"*. It cannot go lighter, and Skin I is `(0.847, 0.638, 0.552)`. So the per-tone lips and nails are articles, not tints (8.2). **The derivation rule is judgement** (no measured lip or nail albedo exists; research Pass 4); it is written once, in the recipes, and judged on the character sheet.
- **F-P08-2 — The token lives in eight sites across seven tool files, plus three docs, not six places.** Tool files: `assemble_mtlx.py` (`KNOWN_MASTERS`, the `cutout_map` guard), `recipe.schema.json`, `validate_material.py`, `build_masters.py`, `rig.py` (`GRADED`, `ADVISORY_VIEWS`), `codec_ab.py`, and `JOB_FORMAT.md`. Docs: `MasterSet.md`, `LCDSchema.md`, `Glossary.md`. The master token reaches the Blender loader (`load_article.py`), the rig (`job.py`) and the dev install (`working_tree.py`) by reading the article, so those need no list. *(Corrects research AP-F4, which counted `build_scene.py`, where the word is only a comment, and missed `rig.py` and `codec_ab.py`.)*
- **F-P08-3 — Phase06 is built against "no Hair master".** Its seed reads *"No new master … no Hair master (L2: Masked served)"*. It is built on the UE machine (Roadmap; whether it is running today is not visible from here), so the library's own Unreal column needs a Hair master too. That is a coupling note at this phase's close, pushed after 8.1, as Phase07 did for its inputs.
- **F-P08-4 — The character job takes defaults only** (`JOB_FORMAT.md`: *"Sliders are swept on the test scene"*). So the tint range is judged on the sweep and in Blender (clicks 1–2), and the character sheet shows the untinted hair (click 3). No rig change is needed for that.
- **F-P08-5 — Studio sees each article the moment it lands.** `working_tree.py` reads every `.mtlx` on disk, and the platform fails loud on an unknown token (research Pass 4). So `Hair_Natural` renders as the missing material in Studio if picked before Studio's Hair master exists. The platform planned for this; `Hair_DarkBrown` keeps working meanwhile.
- **F-P08-6 — Library Coverage's textile blockers are stale.** Suede, Velvet and Satin are marked `C2` / `C2 + C3`, but Phase07 built coat, fuzz and specular anisotropy. The second tranche's order (canvas, satin, felt, stretch knit, wool suiting) puts first what the rig can judge best on the article sheet. Stretch knit and wool suiting are not on that list. Their names are fixed at 8.4 under C5.

**Forks tested and closed** (none reached the lead):
- *Chiang or OpenPBR* → DoR1 (RD-P08-1).
- *Re-route `Hair_DarkBrown` or add an article* → C5, "no versioning", and research Pass 4 (RD-P08-2).
- *Names or a catalog field for the pairing* → C4 / C5; the platform deferred to the library (RD-P08-3).
- *Brows and lashes* → Phase07 7.6 and P17 (RD-P08-4).
- *Who owns the garment split* → Phase07 §Not now (§Not now above).

## Discovery Status

- **Passes captured:** 1. **The Brief is complete.** Lane `build`.
- **Current working direction:** the Brief above.
- **Open decisions:** none for the lead. The phase's judgement calls are eyes-on at each sitting: the lip and nail derivation rule, and how far 8.4 goes.
- **Checks to carry forward:** baseline `check_exporter.sh` before touching `codec_ab.py` (8.1) · regenerate the Blender library and run `check_asset_library.sh` (8.1) · rebuild the character scene after the shoe split (8.3) · Phase06's coupling note (close) · push after 8.1 (the lead's).

## Execution Log

*Ledger: step · result · next. Findings live in the commit messages.*

### Resume block (written at the 2026-09-28 hand-off; the lead: *"yes to 1 and 2, then hand off"*)

- **Superseded by the 8.1 rework row in the ledger below** (items 1–3 of "Next" landed; item 4's sitting is owed).
- **Where:** 8.1 is **reworking**. The `Hair` token, `Hair_Natural` (candidate) and the Blender library landed. The lead judged the hair unusable (see the verdicts below), so the Hair master's graph is being redone. **Not pushed** since `de08ccc`: 8.1's commits, the research, and this hand-off. **Push after the rework lands** (the platform builds against the Hair master).
- **Ruled by the lead, 2026-09-28** (*"yes to 1 and 2"*):
  - **(1)** the mesh-UV rule and the `uv_scale` formula are now in the contract (`LCDSchema.md` §Notes, `PlatformDependencies.md` P18). Done at this hand-off.
  - **(2)** the hair ships as an **interim**: light through the strands, soft edges and much less gloss, **marked interim**. **The lead picked probe C**, verbatim: *"I do think c soft edges is the way"*. So soft coverage (H2) is in, not optional. If Storm's alpha-blend sorting fails HR-Q2, the fallback is a lower cutoff in Storm only, with full softness in Blender and Unreal. The real fix is its own research thread: card maps (root-to-tip, strand variation, depth), strands, and better card assets than MakeHuman's bob (`260928_R_HairAndNailRendering.md` H4/H5; Roadmap *Hair That Reads as Hair*).
- **Next, 8.1 rework, in this order:**
  1. **Storm probe first** (HR-Q1, HR-Q2): the character's hair with a hand-edited `Hair_Natural` (`geometry_thin_walled = true`, `subsurface_weight` ≈ 0.6, `subsurface_color` = the fibre colour, forward `subsurface_scatter_anisotropy`; then a continuous `geometry_opacity` with no threshold), rendered through the rig. Blender's equivalent is probe B/C (`260928_R_HairAndNailRendering_probe.py`).
  2. **The Hair graph:**
     - the assembler authors `geometry_thin_walled` and the subsurface set on Hair;
     - `validate_material.py`'s Hair branch requires them;
     - `build_masters.py` gives `ML_Hair` a translucency part (OpenPBR's thin-walled split: reflection × (1 − a), a Translucent BSDF × (1 + a); HR-Q6 whether Principled's `Thin Wall` does it natively);
     - soft coverage, if HR-Q2 passes;
     - `MasterSet.md` (the Hair row and settings row: *"masked, dithered"*; RD-P08-1 superseded) and `LCDSchema.md`.
  3. **Less gloss** (the lead: *"too glossy"*): roughness up from 0.4, specular weight down. Re-author `Hair_Natural` in place (`v01`, unreleased, "no versioning") with an **interim** note in its recipe.
  4. Rig sweep and character sheet; Blender library rebuilt; `check_asset_library.sh`; then the lead's sitting on the **character's hair cards**, never on cubes.
- **Then 8.2 with nails (N1):** `Nail_FitzpatrickI…VI` on **Subsurface + a glossy coat**, `subsurface_color` from the tone (the lead: *"Agreed nails are bad we need to fix them"*). This replaces the Brief's Opaque nail.
- **Gate state at hand-off:** `run_all.py` 14 / 2 / 1 (`approval_binds_freeze` alone, inherited). `check_exporter.sh` red for its environment (no MaterialX in its Python), identical before and after 8.1.
- **Offered, not ruled (a later step, not this phase's scope):** a Blender-side helper that sets `uv_scale` from the mesh's measured UV density when a Matter material is dropped on it, so a Blender user does not meet F-P08-8's furrows. The contract rule it would apply is in `LCDSchema.md` §Notes.
- **Left open on the desktop (disposable, unsaved):** a Blender session holding the scenes *P08 hair probe* and the four-cube demo. Close it without saving.

**Tree at start (2026-09-28):** `main` @ `de08ccc`, level with origin; 49 tracked textures modified in the working tree by no session of this phase. **Gate at start:** `run_all.py` 10 PASS / 2 SKIP / **5 FAIL** (Phase07 closed on 14 / 2 / 1, `approval_binds_freeze` alone). `check_exporter.sh` red at start: its Python cannot import MaterialX (environment, not code).

**F-P08-7 — Every texture in the working tree was an 8×8 placeholder PNG.** The 49 tracked PNGs under `MatterLibrary/textures/` were 67–74 bytes (mtimes 2026-09-23 15:02 and 2026-09-27 20:52), while their real objects sat intact in the local LFS store. That caused the four extra release-hash reds, and it would have put stub textures in every rig sheet, every Blender preview and the dev install Studio links to. The cause is not traced. **Restored by the lead's ruling**, verbatim: *"yes restore the textures"* (`git checkout -- MatterLibrary/textures`). The gate is back to 14 / 2 / 1, `approval_binds_freeze` alone (inherited).

**F-P08-8 — The skin's "strange pattern" is a UV-scale mismatch, not a material, texture or naming defect** (2026-09-28, seen by the lead in the live hair probe: *"The face and arms have a strange pattern on them... P65 thought this was a scale issue. can you see the issue?"*). The articles are authored at real size: one UV unit = one tile = the article's `meters_per_tile` (skin: 1 cm). A mesh whose UVs are in another unit draws the detail at the wrong size. On MakeHuman's own atlas, 1 UV unit ≈ 1.69 m of body (Phase07 F13), so a 1 cm pore map is drawn ~170× too large, as big worm-like furrows. **Reproduced and fixed, live:** the probe loaded the rig's character scene (UVs in metres) without the rig's ÷ `meters_per_tile` wrapper (`job.py`), and the furrows appeared. Setting the skin's `uv_scale` to 0.01 removed them (`/tmp` renders, before and after). **The consumer-side lever is per-binding `uv_scale = meters_per_tile ÷ (metres per UV unit)`**, and it **divides** (MaterialX `place2d`, `LCDSchema.md`): ≈ 0.006 on the raw hm08 atlas, not 170. That is P18's stopgap; the platform's own fix was reported as *"P65 fixed this in studio by scaling it (I think)"*. **The library's gap:** the rule lives only in Phase07 F13 and P18, and nothing in the library applies it, so a Blender user dropping skin on MakeHuman's body gets the pattern too. A second possible cause for what Studio saw: the dev install served F-P08-7's 8×8 stub textures from 2026-09-27 20:52 until the restore.

**Lead's verdicts on the hair probe (2026-09-28), verbatim:** hair: *"I will follow your lead - they all look bad to me... too glossy, no "life" looks clearly extermly fake and really really bad... if that is the best we can do then it is what it is.. but eventuall this needs to be reseerached and fixed.. this is not usable..."*; nails: *"Agreed nails are bad we need to fix them."*

| Step | Result | Next |
|---|---|---|
| **8.1 rework** (`/execute P8`, 2026-09-28, second run) | Landed at `a9e1eae` + `3d29e78`: Hair's own graph (soft coverage, thin-walled translucency with `subsurface_color` following the tinted base); `ML_Hair` v7; `Hair_Natural` re-authored as the **interim** (roughness 0.65, subsurface 0.6 at anisotropy 0.5); specs updated; Blender library rebuilt (36, CONFORMS). Gate 14 / 2 / 1 (inherited). **HR-Q1:** Storm renders it, but **Storm vs Blender 2.84 / 2.77** on the test scene (was 0.71 / 0.80), character hair 4.01 / 3.81: it is the translucency (off: 0.81 / 0.47), both lobes, cause not isolated (commit `3d29e78`). **HR-Q2:** no sorting artefacts in Storm; soft coverage barely moves the bob (95 % of its map is 0 or 1) and matters for brows and lashes. **Sitting owed:** Blender, the character's cards backlit at four tints (clicks 2–3). | The lead's sitting; the parity bar for Hair (YOUR CALL). |
| **8.1** | **Click 1 ✅ (sitting 2026-09-28).** Lead, on the sweep sheet, verbatim: *"sheet looks plausable"*. Storm vs Blender, `Hair_Natural`: ΔE 0.81 whole set / 0.54 close-up; the tint moves both alike (14.8 / 14.6). Landed at `8.1` (WIP): the `Hair` token through the specs and the seven tool files, and `Hair_Natural`. **Deviation (small):** the rig's sweep has one tint setting ("tint blue"), so click 1 shows the tint behaving alike in both tools, not a walk through hair colours. The colour range is judged in Blender (click 2). **Then:** `Hair_Natural` marked `candidate`; the Blender library rebuilt (36 articles, `check_asset_library.sh` CONFORMS); the character sheet rendered with it on the bob, brows and lashes. Storm vs Blender: hair 0.71 / 0.80 (whole / face), was 1.34 / 1.71 on `Hair_DarkBrown`; brows 2.18, lashes 4.95 (thin cards, advisory as Lace). Nothing magenta. **Click 2 ✗ (sitting 2026-09-28)**, shown on four tinted cubes in Blender. Lead, verbatim: *"Hair still looks plastic, no transparency, no SSS... hair is not a thick solid"*, then *"YOu need to research how to render hair"* and *"Will be similar issue with nails"*. **RD-P08-1 (settings-only) is reopened:** it changes how Unreal shades the article, but in Blender and USD viewers the article stays an opaque surface. (The cubes were also the wrong fixture: hair is thin fibres on cards.) **8.1 SUSPENDED, not pushed**, pending `260928_R_HairAndNailRendering.md` (lead-directed `/research`). | Research, then rework 8.1 (and review `Nail_Natural`). |
