# Phase26 — Makeup on the Skin

**Status:** 🎉 COMPLETE (closed 2026-11-02). *Before:* IN EXECUTION (2026-11-02, `/execute Phase26`). *Before:* BRIEF READY (2026-11-02, the close of Pass 1, `ML_P26_D1`). *Before:* SEEDED (2026-11-02), the first part of *Skin Layers*, numbered on the lead's *"b"* (RD-PSM-2). It runs **alongside Phase25** and **ahead of *Eyes in the Shader***. The rest of *Skin Layers* keeps its place after Eyes.
**Lane:** `build` (§Risk lane).
**Measured at:** `5c4bfde`, on **the machine with Unreal**. Unreal 5.8 is at the path `unreal/build.sh` takes as `UE`, `MATTER_BLENDER` is the official 5.2.2, and `unreal-runtime-v7` is pinned.
**Seeded from:** [`../Research/261101_R_PlatformSkinAndMakeupAsks.md`](../../Research/261101_R_PlatformSkinAndMakeupAsks.md) (Q-PSM-2, Q-PSM-7; F-PSM-1, F-PSM-4; RD-PSM-2) · [`../Research/261027_R_CharacterMaterials.md`](../../Research/261027_R_CharacterMaterials.md) (Pass 4, Makeup and marks; RD-CMT-1, RD-CMT-2, RD-CMT-4) · the platform's ask row `PlatformDependencies.md` **M14** (1) and (2).

## Outcome

**A character wears the library's first makeup: face makeup picked by area and a mark placed on the body, merged into one layer on its skin, and it looks the same in Storm, Blender and Unreal.**

*(Drafted at seeding; confirmed unchanged at Pass 1.)*

## Why this is a phase

- **The platform's skin phase is held on it.** Its merge step waits on the slots (Q-PSM-7) and on a format and a first few pieces (Q-PSM-2), together (F-PSM-1).
- **The slots are a contract change in three tools** (F-PSM-4): the contract, the MaterialX graph, the Blender masters, the Unreal builder, the rig and the recipe check. Add a new kind of library entry (the piece), and this is a phase by `LOCAL_DELTAS.md` §Weighting.

---

## The Brief

### First human test

**Where:** the lead's desktop on the machine with Unreal.
- **The look:** the library's Unreal look view (`tools/parity/look.py`, with a new makeup option, run on a local package that has the slots; RD-CMT-4).
- **Agreement across the three tools:** the rig's character sheet.
- The agent runs both and opens each picture at full resolution, one labelled picture at a time. The paths go in the handback.

**The fixtures:**
- `Skin_FitzpatrickII` and `Skin_FitzpatrickVI`: the lightest and the darkest finished skins, each with its shine maps.
- **The lips are cast as the skin**, as on the platform's new base character (R-PSM-3). This is the rig option F-PSM-5 named, added in 26.1.
- One look on both skins: **red lip colour** (a fitted piece) and **a black-ink tattoo on the back of the left hand** (a placed piece).
- The tattoo is an asymmetric arrow about 4 cm long, so its position, size and turn can all be read.
- These span the cases that matter for paint: saturated colour on the lightest and the darkest skin, and near-black ink.

**Can the surfaces show it?** Worked from `look.py`'s cameras (`look_views`, the `at(target, frame_m, …)` framing):
- The **hand** view frames 0.20 m across the image width: about 5 px/mm at `--width 1024`, 7.7 px/mm at 1536. The 4 cm tattoo spans about 200–300 px.
- The **face** view frames 0.28 m: about 3.7 px/mm at 1024. The lips (~50 mm wide) span ~180 px.
- The rig's Storm column on the character is capped at 512 px on this machine (Learnings Storm S11). So agreement across the tools is the agent's number, read at the pieces' pixels. The lead only looks at the sheet.

**The clicks (26.1):**
1. Face, front, on Fitzpatrick II, then on VI: the lips are red and the skin around them is untouched. On VI, the red reads as lipstick, not as a tint of the skin.
2. The back of the left hand, on both skins: the arrow sits where it was placed, points the way its turn says, and is about 4 cm long.
3. The rig sheet: the same lips and the same arrow in Storm, Blender and Unreal.

**What the lead can say afterwards:** *"Red lipstick and a hand tattoo sit on the light and the dark skin, merged into the skin, and the three tools agree."* (Or the gap, e.g. *"the red is too orange on VI"*.)

**No earlier reference has been judged:** this is the first makeup the library has drawn.

**The second sitting (26.2):** the full first handful on the same fixtures:
- **a clear lip gloss**: finish only. The lips' highlight is sharper, and their colour does not move.
- **an eyeshadow** on the lids.
- The gloss is judged in the face view in the look view's sun. A finish needs a lit highlight, which the rig's sheet is too small to show.

### In now / not now

**In now:**
- **The slots** on the Subsurface master, in all three tools, with their order against the skin's maps written down (RD-P26-2) → **26.1**.
- **The reference merge:** a library tool that turns a piece list into the slot pictures (RD-P26-4) → **26.1** (fitted and placed).
- **The piece format** as the library's contract, fitted and placed (RD-P26-5, RD-P26-6) → **26.1** (both kinds' pictures and placement); **at the close** (the contract text).
- **The first four pieces:** `LipColour` and `Tattoo` → **26.1**; `LipGloss` and `Eyeshadow` → **26.2** (RD-P26-7).
- **The pieces in the dev catalog**, a group of their own, served to Stage (RD-P26-8) → **26.2**.
- **The rig and look view showing makeup**, with the lips cast as the skin → **26.1**.
- **The ledger and the platform told** (M14 (1)–(2)) → **at the close**.

**Not now** (the rest of *Skin Layers*, after Eyes, unless marked):
- **Relief in a piece** (a raised scar) and the third slot that would carry it: kept in the format as a channel marked *(planned)* (RD-P26-1).
- **Pigment pieces** (a bruise, a flush, a vein, freckles added by the Creator) and the shipped pigment fields (Q-PSM-3, F-PSM-6).
- A wide piece set · the Blender kit for contributors (RD-CMT-2) · stubble and body hair.
- **Makeup on the `Lips_*` and `Nail_*` articles.** The platform's new base has its lips in the body. Older characters with a lips part keep their `Lips_*` articles without makeup. Polish is a nail article (Q-PSM-4).
- **8K slots**, only after the 2K → 4K → 8K steps (RD-P25-20).
- **Multi-colour stamps:** the stamp picture's colour is a multiplier that a later piece may use; the first pieces are single-colour.

### The reuse check

**What the stack already provides, and which contracts are touched:**
- **A picture a binding supplies, on the mesh's own layout:** `base_color_map` (LCDSchema §Base colour map; `assemble_mtlx.py`'s `spec.base_color_map` branch, the `base = const × map × tint` block; JOB_FORMAT `bindings[].base_color_map`).
  - The slots are the same shape: empty in the article, read on texcoord 0 directly, supplied by the binding through the Carrier rule.
  - A colour picture's asset value carries `colorSpace = "srgb_texture"` (Storm S10).
  - **No new mechanism.**
- **The shine maps' formulas** (LCDSchema §Shine maps) set where the makeup sits in the roughness chain: after the map, the bias and the clamp.
- **Each texel's 3D position, normal and regions on the body:**
  - `gen_skin_shine.py` already uses them (`F["P"]`, `F["reg"]["Lips"]`, `regions3d`, `ellipse`).
  - The fitted pieces are made in 3D the same way (SkinMaps §Authored on the body, baked per layout).
  - The reference merge reads the same positions to place a stamp.
- **A non-material entry with its own group and list:** the HDRIs (`groups.py` `GROUPS`, `hdris[]` in the dev catalog; RuntimeCatalog §Groups). The pieces follow that shape.
- **A locally built runtime for the library's own look:** `$MATTER_UNREAL_RUNTIME` (the Unreal driver's lookup order). No publish is needed to judge.
- **Contracts touched:** LCDSchema (three new author-tier inputs) · JOB_FORMAT (a job format bump, so an older runtime refuses a makeup job rather than drawing it bare) · RuntimeCatalog §Groups (additive) · Identity (piece names). **Each is additive. Every article that does not declare makeup assembles byte-identically.**
- **The one custom layer is the reference merge.** It replaces nothing native. The gap: no tool in any of the three targets merges a piece list placed on a body, and the platform's merge needs a known answer (RD-P26-4).

### Rides on

| `CoreMechanisms.md` row | What in this phase rides it | The peer we follow |
|---|---|---|
| 1 — a body map larger than 2048 | **Not met:** the slots and pieces are 2048² (RD-P26-9). An 8K step would ride it. | `gen_synth_skin.compose_banded` (opened in Phase24/25's reading, not re-opened: not met) |
| NEW — ruled by RD-PSM-2 (the format is this phase's) | the piece format and the reference merge | the mesh-supplied picture shape (`assemble_mtlx.py` `spec.base_color_map`, opened this pass); 3D-on-the-body fields (`gen_skin_shine.py` `regions3d`, `F["reg"]["Lips"]`, opened this pass); the catalog's non-material list (`groups.py` `GROUPS`, opened this pass) |

### Decisions that bind

- **RD-P26-1 — Relief stays out of Phase26** (F-PSM-4, settled with the platform 2026-11-02).
  - No relief slot, and no relief in the first pieces.
  - The format keeps relief as a per-piece channel marked *(planned)*, so no piece is remade when it arrives.
  - The slot arrives with the first piece that needs it (a raised scar, *Skin Layers*), the same road the shine maps took: one input, neutral by construction.
  - **The platform's answer** (its skin phase's session, 2026-11-02): road (b) *"suits us"*. Its merge asked for exactly colour + coverage, finish and an amount, and its makeup sitting clicks no relief. A fifth picture slot later is *"one row on each side, a wire bump and a rebuild. That is no reason to design the merge for three pictures now."*
  - Matches SkinMaps §Shine maps: *"a mark's own relief (Skin Layers)"* is *(planned)*.
- **RD-P26-2 — The slots, their neutral and their order.** Names are final at execute; these are the shape.
  - **`makeup_color_map`** (`filename`, a `color4` image). RGB is the makeup's colour, read as `srgb_texture`. A is the colour's coverage: straight, not premultiplied, read linear.
  - **`makeup_finish_map`** (`filename`, linear data). R is the target roughness, G the finish coverage.
  - **`makeup_amount`** (`float`, default 1). It multiplies both coverages, so a mark can fade the whole layer without a new merge.
  - All three are author-tier, lane B, read on texcoord 0 directly, supplied by the binding (the Carrier rule), and empty in the article.
  - **Neutral = no picture = coverage 0**, so every skin draws as today.
  - **Order:**
    - `base = mix(base_color_const × base_color_map × base_color_tint, makeup colour, colour coverage × amount)`. The tint stays the skin's, and the scatter colour follows this mixed base (`subsurface_follows_base`).
    - `roughness = mix(clamp(pores + (roughness_map − 0.5) + roughness_bias, 0, 1), target roughness, finish coverage × amount)`. Matte powder over a wet skin reads matte.
    - The normal, the cavity's shine and the scatter radius are untouched.
  - **Why finish has its own coverage:** a clear gloss changes finish with no colour.
  - **Agreed by the platform 2026-11-02:** colour coverage in straight alpha, finish as a target roughness that coverage mixes toward, the makeup colour over the colour map with the scatter following, and 2048² first. The separate finish coverage and this order were sent the same day as a refinement and agreed too: *"its merge writes those two pictures, and neutral = coverage 0 = today's skin is what we need"*.
- **RD-P26-3 — The finished skins declare the slots** (a recipe flag, like `base_color_map: true`): the 18 `Skin_Fitzpatrick*` and `Skin_Tone34`.
  - In Blender and Unreal the Subsurface master carries the slots for every Subsurface article, at neutral.
  - In MaterialX only a declaring article has the nodes, so the rest assemble byte-identically.
- **RD-P26-4 — The library ships a reference merge, and it is the known answer.**
  - It is a tool under `tools/converters/fit/` that takes a piece list and writes the two slot pictures at 2048².
  - The rig, the look view and the platform's own merge test all read its output.
  - The platform's live merge must produce the same pictures for the same list (the platform: *"welcome"*).
- **RD-P26-5 — The piece format** (written into a new spec at the close, beside `SkinMaps.md`).
  - **A fitted piece** is a coverage shape on the body's atlas (a greyscale PNG, 2048², made in 3D and baked per layout), plus its controls.
  - **A placed piece** is a square stamp (RGBA: RGB a colour multiplier, white for a one-colour piece; A coverage), plus `size` in metres, plus its controls.
  - **Controls:** colour · strength (scales coverage) · finish (a target roughness, matte to wet) · whether the piece carries colour, finish or both (a clear gloss: finish only).
  - **Planned channels, kept in the format:** relief (RD-P26-1), and pigment in place of colour (*Skin Layers*).
  - **What a composition stores:** the piece's name, its point on the rest-pose surface, size, turn, strength and control values, never pixels (R-PSM-5). The merge makes the pixels.
- **RD-P26-6 — Where a stamp lands** (agreed by the platform 2026-11-02: its merge *"will follow it, with your reference merge as the known answer"*; its own sketch, a plain 3D distance from the point, ignored a piece's size and turn).
  - The stamp is centred on its rest-pose surface point.
  - Turn 0 points the stamp's up along the body's rest-pose +Y, projected onto the tangent plane there. The turn is clockwise about the outward normal.
  - A texel takes the stamp only where its rest-pose normal faces the point's normal (dot > 0), so a stamp never prints through a limb.
  - A texel's stamp coordinate is its rest-pose position projected into that tangent frame.
- **RD-P26-7 — The first four pieces:** `LipColour` (fitted; colour + finish) · `Tattoo` (placed; colour) · `LipGloss` (fitted; finish only) · `Eyeshadow` (fitted; colour + finish).
  - **The seed's bruise is not among them:** Q-PSM-2 itself calls a bruise a pigment piece, and pigment pieces wait for the pigment fields.
  - A tattoo is paint, and being asymmetric it shows a stamp's turn; a round bruise cannot.
  - The platform agreed the same day (*"the better test of position, size and turn"*). Its own makeup sitting's *"place a bruise"* row is its lead's to change.
  - **Unless you say otherwise.**
- **RD-P26-8 — The pieces have a group of their own in the dev catalog:** id `makeup`, list `pieces`, shown on the character. It is additive, as the HDRIs' group was, and `schema_version` is unchanged.
  - **Names:** `Makeup_<Kind>_<Variant>_v01` (for example `Makeup_LipColour_Full_v01`, `Makeup_Tattoo_Arrow_v01`), inside Identity's 63-character `[A-Za-z0-9_]` budget, written into Identity at the close. **Unless you say otherwise.**
- **RD-P26-9 — 2048² slots and pieces first** (RD-P25-20's 2K → 4K → 8K; the platform agreed).
- **Carried:**
  - RD-PSM-1 · RD-PSM-2;
  - RD-CMT-1 (the library makes the pieces; how a character wears them is the platform's) · RD-CMT-2 (a piece works on every character: authored in 3D on the approved mesh) · RD-CMT-4 (the look in the Unreal look view until Studio can draw it);
  - RD-P22-17 (the skin has no coat: gloss is roughness, never a coat);
  - RD-RO-2: CC0. **The pieces are procedural or hand-made, with no photograph or scan** (RD-SKM-2). AI may make a tattoo design only as tone-free content (RD-SYN-1); the first arrow is drawn by code.

### Risk lane

**`build`.** It touches no authorisation, secret, destructive migration, data loss or public edge. The format is consumer-facing but additive.

The controls, each read:
- **The thumbnail fingerprint** (`tools/thumbnails/showcase.py` `masters_hash` hashes `blender/masters/*.py`; `build_snapshot.py` refuses a thumbnail whose `masters_sha256` differs).
  - **Any edit to the Blender masters stales all ~140 thumbnails.** That is about 40 minutes of GPU (~17 s an article) at the next snapshot, and the pictures come out unchanged at neutral.
  - The 19 declaring skins also change their `article_sha256`.
  - ~~Owed at the next snapshot, not at the gate.~~ *(Superseded 2026-11-02.)*
  - **RD-P26-10 — No thumbnail re-render in this phase.** The lead, at the Brief's handback, verbatim: *"Do NOT redo thumbnails until we get everything resolves, things in place, reduce the skin sets etc... total waiste of time"*. Read as: the stale thumbnails stay stale, through this phase and its close. A snapshot that refuses a stale thumbnail is not built for this phase's sake. The re-render waits until the skin work settles and the skin sets are reduced, on the lead's word.
- **`run_all.py`** (18 lanes): the recipe and material lanes see the new recipe flag, and `validate_recipe.py` learns it.
  - The piece pictures land under `MatterLibrary/textures/fit/makehuman/makeup/`. No gate walks that tree except the release-time compressor (`compress_textures.py`) and the freeze, and neither runs pre-release (§Settled practices).
- **`check_exporter.sh`:** only if the add-on is touched. The masters are not the add-on. If 26.1 finds it must touch `blender/addons/`, baseline it first.
- **The Unreal runtime:** the slots draw nothing at their defaults, so no new runtime is owed (the lead, 2026-10-05). The library's own look uses a local package through `$MATTER_UNREAL_RUNTIME`. Publishing one is the lead's word, offered at the close.
- **The job format:** a makeup job bumps it, so `unreal-runtime-v7` refuses the job rather than drawing a skin with no makeup as matched.

### Step list

- **26.1 — Red lips and a hand tattoo, merged, in three tools** *(the first human test)*.
  - The slots in the MaterialX graph, the Blender masters and the Unreal builder (+ a local masters build and package).
  - The recipe flag on the 19 skins.
  - The job format and the rig's bindings, and the rig option that casts the skin on the lips.
  - The reference merge (fitted and placed).
  - The pieces `LipColour` and `Tattoo`.
  - `look.py`'s makeup option.
  - **First clickable result:** clicks 1–3 above.
  - One vertical path; the click needs every part. A first click past 90 minutes is likely; there is no smaller unit a person can use.
- **26.2 — The first handful, listed** *(the second sitting)*.
  - `LipGloss` and `Eyeshadow`.
  - The piece records, and the `makeup` group in the dev catalog, served to Stage (`serve_to_stage.py --no-restart` when Stage is up).
  - **First clickable result:** the gloss and the lids in the face view on both skins; the pieces listed in the served catalog (the agent reads it).
- **At the close:**
  - The contract text: LCDSchema §Makeup layer, the piece spec beside `SkinMaps.md`, JOB_FORMAT, RuntimeCatalog §Groups, Identity's piece names, and the Glossary's *piece*, *fitted piece*, *placed piece* and *makeup layer*.
  - The ledger: M14 (1)–(2) answered.
  - The platform told of the commit that holds the builder change, so it can rebuild its masters.
  - A runtime publish offered. **No thumbnail re-render** (RD-P26-10).

### Compact build map

- **Contract:** `docs/specs/Contract/LCDSchema.md` (a §Makeup layer beside §Shine maps) · a new `docs/specs/Authoring/MakeupPieces.md` · `tools/parity/JOB_FORMAT.md` · `RuntimeCatalog.md` / `SiteFile.md` §Groups · `Identity.md` · `docs/Glossary.md`.
- **Graph:** `tools/converters/assemble_mtlx.py`:
  - a `makeup` spec flag next to `base_color_map`, Subsurface only;
  - the mix inserted before `base` feeds both `base_color` and the scatter colour;
  - the roughness mix after the clamp.
- **Blender:** `blender/masters/article.py`, `load_article.py` (the shine maps' peers).
- **Unreal:** `unreal/MatterRuntime/Scripts/build_masters.py` (the Subsurface master's picture slots); `UE=~/Documents/Unreal/Linux_Unreal_Engine_5.8.0 bash unreal/build.sh masters` then `package`. Diff the builder's `MATTER built …` lines against a copy taken first, to confirm the defaults draw unchanged.
- **Rig:**
  - `tools/parity/job.py` and `drivers/{unreal.py,blender_render.py}`: `bindings[].makeup_*` (the `base_color_map` peer), with the colour picture's `colorSpace` (S10);
  - `rig.py` `cast_for`: the skin on the lips;
  - `look.py`: a makeup option, after Phase25's edit is committed.
- **Merge and pieces:**
  - new `tools/converters/fit/merge_makeup.py` (the reference merge; reads the body's texel positions, normals and regions the way `gen_skin_shine.py` does);
  - new `tools/converters/fit/gen_makeup_pieces.py` (the four pieces, made in 3D);
  - piece records and pictures under `MatterLibrary/` (exact folder at 26.1, beside the skin's fit set).
- **Catalog:** `tools/converters/groups.py` (the `makeup` group) · `tools/releases/serve_to_stage.py` (the `pieces` list).
- **Check:** `tools/validators/validate_recipe.py` (the flag) · G8 for a piece picture (a fitted shape at the mesh's map size; a stamp, square).
- **Tests:** the existing gate + units for the merge (coverage > 0 at a placed point, 0 on the far side of the limb, a fitted piece's coverage equals its picture's) + **one** real-path smoke (the first human test). No new gate or lane.
- **A premise probe, early in 26.1 (minutes):** a `color4` image read as `srgb_texture` keeps its alpha linear in Storm, Blender and Unreal.
  - **If not:** the colour's coverage moves to the finish picture's B channel, and the colour picture becomes `color3`. Tell the platform.

### Shared surfaces — Phase25 runs alongside

| Surface | Owner | Phase26's part |
|---|---|---|
| `tools/parity/look.py` | Phase25 (its 25.1 option, committed `9c11f4b` 2026-11-02) | adds its own off-by-default option at 26.1; re-read the file first, and check `git status` for a newer Phase25 edit |
| `tools/converters/fit/` | Phase25 (`gen_synth_skin.py`, `paint_uv.py`, `project_face.py`) | new files only; reads `gen_skin_shine.py`, edits none of Phase25's |
| the GPU | one heavy job at a time | a look-view launch, and a local Unreal build and package (no thumbnail re-render, RD-P26-10): before each, `ps -ef \| grep "[U]nrealEditor"`, and the lead asked once if Phase25's generation is running |

*Told to Phase25's session by message, 2026-11-02.*

---

## Pass 1 — Discovery (2026-11-02, `ML_P26_D1`)

- **Examined:**
  - the seed; the PSM research whole; CMT Pass 4–5;
  - LCDSchema §Cut-out map → §Render-role texture nodes; SkinMaps §Shine maps; `CoreMechanisms.md`; `_Architecture.md`'s principles; RuntimeCatalog §Groups; Identity's outline;
  - the M14 row; the Roadmap's Phase26 and *Skin Layers* entries;
  - `assemble_mtlx.py`'s `base_color_map` and shine-map branches; `rig.py` `cast_for`; JOB_FORMAT's bindings;
  - `look.py`'s cameras; `groups.py`; `showcase.py`'s hashes; `build_snapshot.py`'s checks; `gen_skin_shine.py`'s regions; the Unreal driver's runtime lookup;
  - Learnings MaterialX M4, M5 and Storm S10, S11; Phase25's status and shared files;
  - the platform's skin phase doc, read in place at its newest commit, never pulled.
- **Learnings:** MaterialX, Storm, Unreal and Blender are touched. The entries that bind are M4/M5 (the scatter follows the base; a value that must be settable is an interface input), S10 (a colour picture's carrier needs `colorSpace`) and S11 (Storm's character column caps at 512 px here). The others were listed and not needed.
- **The tree grep for "makeup":** no code builds or defers it. The hits are planning docs and Phase25's image-model prompts, which tell the model *not* to draw makeup.
- **The relief question went to the platform first**, as the invocation asked, before any format was written. Its answer is RD-P26-1.
- **Findings that changed the seed:**
  - **F-P26-1:** the slots are binding-supplied like `base_color_map`, not article-carried like the shine maps.
  - **F-P26-2:** finish needs its own coverage (RD-P26-2).
  - **F-P26-3:** a bruise is a pigment piece by the platform's own ask (RD-P26-7).
  - **F-P26-4:** editing the Blender masters stales every thumbnail (§Risk lane). The stale thumbnails stay stale (RD-P26-10).
  - **F-P26-5:** a tattoo on the back of the hand is judgeable in the existing hand view; no new camera is needed.

---

## Execution ledger (`/execute Phase26`, 2026-11-02)

| Step | Result | Next |
|---|---|---|
| 26.2 | **✅** (clicks 4–5 sat 2026-11-02, below; served to Stage). The pieces `Makeup_LipGloss_Clear_v01` (fitted, finish only, roughness 0.08) and `Makeup_Eyeshadow_Lids_v01` (fitted, plum, satin; both upper lids, placed in 3D from each eye) in `gen_makeup_pieces.py`; the look `tools/parity/makeup/first_handful.json` (the 26.1 look plus both). The dev catalog's `pieces` list and `makeup` group (`serve_to_stage.py`, `groups.DEV_GROUPS`), read from a projection: four pieces, `schema_version` unchanged. Measured in the face view (look view, 1024 px), the gloss against the same lips without it: the lips' median colour moves ≤ 2/255; the highlight's peak 170 → 255 (II) and 131 → 255 (VI). Served on the lead's word (the platform's sessions were open on this machine, `LOCAL_DELTAS.md` §Two machines). | the close |
| 26.1 | **✅** (clicks 1–3 sat 2026-11-02, below). The slots in the MaterialX graph (the 19 finished skins declare `makeup`; every other article re-assembles byte-identically), the Blender Subsurface group (v13) and loader, and the Unreal Subsurface master (local masters build and package; job format 5). The reference merge (`tools/converters/fit/merge_makeup.py`, units `test_merge_makeup.py`), the pieces `Makeup_LipColour_Full_v01` and `Makeup_Tattoo_Arrow_v01` (`gen_makeup_pieces.py`), the first look `tools/parity/makeup/red_lips_hand_tattoo.json`, and `--makeup` / `--lips-skin` on `rig.py` and `look.py`. Measured at the pieces' pixels (rig, 512 px, Fitzpatrick II): lip colour within 6/255 per channel across the three tools; the tattoo's centre within 1 px, the same extent. | 26.2 |

- **Premise probe (alpha stays linear in a `color4` read as `srgb_texture`):** holds. Unreal by construction: the runtime decodes sRGB on RGB only (`MatterRuntimeGameMode.cpp` `LoadTexture`). Storm and Blender: the lips' covered-pixel counts and centres agree with Unreal's within 4 % and 1 px, which a gamma-curved coverage edge would not give.
- **F-P26-6 — a fact the Brief rested on was false:** *"no gate walks that tree except the release-time compressor … neither runs pre-release"*. The `compression` lane of `run_all.py` walks every texture and refused the piece pictures' unknown roles. `compress_textures.py` learns `coverage` (BC4) and `stamp` (BC7).
- **F-P26-7 — the build's environment:** `unreal/build.sh package` failed with *Permission denied* starting `~/.local/bin/env` (a non-executable file shadowing `/usr/bin/env` on the session's PATH). Run with a PATH without `~/.local/bin`, it packaged. A `/retro` item, not a code change.
- **The tattoo's point** was first taken 1.5 cm up the hand; the look view showed it on the wrist's edge, seen edge-on. Moved 2 cm toward the knuckles (`gen_makeup_pieces.back_of_left_hand`).
- At the hand view's ~5 px/mm the tattoo's edges step visibly: the 2048 atlas gives the back of the hand ~0.75 mm a texel (RD-P26-9; the 4K and 8K steps).

**26.1 sitting (2026-11-02), on labelled pictures from the look view:**
- **Click 1 (the red lipstick, Fitzpatrick II and VI):** the lead, verbatim: *"The lips are red"*. *Reading (the agent's): a pass, the dark skin's "lipstick, not a tint" included, since no fault was named; strike it in one line if not.*
- **Click 2 (the hand tattoo, both skins):** the lead, verbatim: *"yes"*.
- **Click 3 (the three tools agree, both skins, the rig's labelled grid):** the lead, verbatim: *"yes"*.
- **26.1 discharged:** the artifact was observed working in all three clicks.

**26.2 sitting (2026-11-02):**
- **Click 4 (the clear gloss, with and without, both skins):** the lead, verbatim: *"yes, serve"*. *Reading (the agent's): "yes" answers click 4; "serve" is the word to serve the pieces to Stage.*
- **Click 5 (the plum eyeshadow, both skins, front and three quarters):** the lead, verbatim: *"yes"*.
- **26.2 discharged:** both clicks observed working, and the pieces listed in the served catalog.
- **Served** (`serve_to_stage.py --no-restart`, Stage not running): the served catalog lists the four pieces under the `makeup` group, each one's record and picture resolving in the dev install.

**26.2 notes:**
- **F-P26-8 — the site file does not carry the pieces.** `groups.GROUPS` is shared by the site file and the dev catalog, so the `makeup` group sits in `groups.DEV_GROUPS`, the dev catalog's only. The site file listing pieces is *(planned, 2026-11-02)*.
- The eyeshadow's coverage falls on two atlas islands: the eyelids' own and the face's beside them. Both are the lids in 3D, as the render shows.
- The 26.2 sitting pictures, labelled: `library/parity/Look__Skin_FitzpatrickII_Clean_Base_s001_v01__makeup__lipsskin/CLICK{4_gloss,5_eyeshadow}.png`; the comparison without gloss in `library/parity/P26_2_without_gloss/` (git-ignored). Pictures: `library/parity/Look__Skin_FitzpatrickII_Clean_Base_s001_v01__makeup__lipsskin/CLICK{1,2,3}_*.png` (git-ignored).

## CLOSE — DONE (2026-11-02, on the lead's "Close Phase26")

- **The Outcome, re-read against the tree:** holds. Face makeup picked by area (the lip colour, the gloss, the eyeshadow, fitted) and a mark placed on the body (the tattoo) are merged by the reference merge into one layer on the skin, and the three tools agree at the pieces' pixels (26.1 click 3). Not an absolute claim, so the acceptance block does not arm.
- **Contract text:** LCDSchema §Makeup layer · `docs/specs/Authoring/MakeupPieces.md` (new) · JOB_FORMAT (format 5, the bindings, `MAKEUP_JOB_FORMAT`) · RuntimeCatalog §Groups (the `makeup` group, `pieces[]`) · SiteFile §Groups (not carried yet) · Identity §Makeup pieces · Glossary (*makeup layer*, *piece*, *fitted piece*, *placed piece*) · `_Architecture.md`'s Authoring row · CoreMechanisms row 2.
- **The ledger:** `PlatformDependencies.md` M14 (1) and (2) delivered, with the platform's next act (re-run its masters build from `build_masters.py`). That row is how the platform is told.
- **Loose ends:**

| Item | Disposition |
|---|---|
| F-P26-8 — the site file listing the pieces | deferred as an ADDITION: the Brief put the pieces in the dev catalog only; marked *(planned, 2026-11-02)* in SiteFile §Groups and MakeupPieces §Not yet |
| The tattoo's stepped edge at the hand view's ~5 px/mm | ruled out: 2048² first (RD-P26-9); 4K/8K are later steps |
| Thumbnails stale since the masters changed | ruled out (RD-P26-10, the lead) |
| F-P26-7 — `unreal/build.sh package` and a stray `~/.local/bin/env` | not the library's code; a `/retro` item |
| A published Unreal runtime with the slots | the lead's word: offered at the close; `unreal-runtime-v7` refuses a makeup job (format 5), so nothing draws wrong meanwhile |

- **Evidence:** `run_all.py` 18 lanes, 18 PASS (at 26.2, before the close's doc-only changes); `test_merge_makeup.py` PASS; `test_build_snapshot.py` PASS. No CI runs here (`LOCAL_DELTAS.md`, the CI row).
