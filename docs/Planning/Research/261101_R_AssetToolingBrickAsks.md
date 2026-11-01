# Research — A brick that reads as brick: what IMRSV's asset tooling asks of the library

**Opened:** 2026-11-01 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `BK` (ids `BK-Qn`, `BK-Fn`). **Pass 1** is written from the asset tooling's side. The library's review of it against its own tree is **Pass 2**, as in `261011_R_AssetToolingAsks.md`.
**Requested by:** IMRSV's work on the tools that make a model ready for Studio. The lead, 2026-11-01, verbatim: *"can you make a request to the matter library for a proper brick material"* — after seeing the Set below roughened in geometry: *"that suddenly made everything look very unrealistic and 'stylized' like pixar brick wall"*.

**Question:** what does a Set built of modelled bricks need from the library, so that a red brick wall reads as real brick at arm's length?

**Extends, does not replace:** `260925_R_LibraryCoverage_FirstRelease.md` §engineered/ceramic (its row 3, `BrickClay_Natural_Clean_Base_s01_v01`, status *Now*, is the article asked for) · `docs/specs/Ontology/Taxonomy.md` (`ceramic`; *a brick wall is not matter*) · `docs/specs/Ontology/MasterSet.md` (tint and overlays) · `docs/specs/Ontology/Identity.md` (names) · `261004_R_PlatformSetMaterialAsks.md` (the last time a generated Set asked for materials).

**Public-repo note.** The asset tooling is a sibling IMRSV project and is private for now. It is summarised here by what it built and what it needs: no paths, code or ruling ids of its own.

**Measured at:** `b2abe6b` (2026-11-01) · Blender 5.2.2 (blender.org) · OpenUSD 26.03.

## The short version

- **The asset tooling built a photo-studio Set in a brick loft: 4,130 bricks, each one modelled** (English common bond, soldier courses over the openings, recessed mortar). The wall is the assembly, so it stays on the builder's side, exactly as `Taxonomy.md` says. What it lacks is the *substance* the bricks are made of.
- **Today every brick is `Terracotta_Unglazed_Clean_Base_s01_v01`, tinted** four ways to reach old red brick in four firings, plus light edge wear and dust. It passes every check. Up close it reads clean and synthetic, because terracotta's base colour is one constant: no colour map, no surface relief (BK-F2).
- **Adding damage in geometry made it worse, not better** (BK-F3). Real brick reads as brick through the variation *inside* each face: mottled firing colour, sand and grit, small voids, soot. That is the library's lane, not the mesh's.
- **Asks:** the brick-clay article the coverage list already plans, with maps (A1); conditions for an old wall: soot, efflorescence, a pitted face (A2); a mortar (A3). One question about variation across thousands of pieces (BK-Q1). Two housekeeping finds on the way (A4).

## Pass 1 — From the asset tooling's side

### What was built

- **BK-F1 — A generated interior Set, 6 × 12 m and 4.5 m high, with two walls of modelled brick.**
  - 4,130 bricks, 215 × 65 mm faces on 10 mm joints; a header course every sixth; jamb bricks returning into each window reveal; soldier courses on steel lintels. Each brick is jittered a few millimetres, worn at its edges, and a few are chipped or eroded.
  - The bricks are four sub-objects by firing colour (*Bricks*, *Dark*, *Light*, *Burnt*), each one mesh bound to one Matter material instance; a fifth holds bricks under an old coat of whitewash (`Paint_Satin_Clean_Base_s01_v01`). Each brick is assigned to a colour at random, so the wall's variety comes from mixing four materials.
  - UVs are real size (one UV unit is one tile, 0.1 m), with each brick's UVs offset at random so no two bricks show the same part of the tile.
  - The asset conforms to the Creator Asset Profile (lightweight; every sub-object file), and its faces all look outward.
  - What it looks like today: `261101_R_AssetToolingBrickAsks_today.jpg` beside this doc.

### What was measured

- **BK-F2 — Terracotta is one flat colour, so the tint is the only colour a brick has.**
  - `Terracotta_Unglazed_Clean_Base_s01_v01` has `base_color_const` = (0.555, 0.212, 0.11) and no colour, roughness or normal map; its only images are the shared EdgeWear01 / Dust01 overlays and the Crevice01 mask.
  - To reach old red brick the instances carry `base_color_tint` (linear): (0.55, 0.30, 0.36) common · (0.36, 0.22, 0.30) dark · (0.68, 0.50, 0.62) light · (0.20, 0.16, 0.30) burnt. Common red lands near (0.31, 0.064, 0.040).
  - Every brick of one colour is therefore the same uniform colour from edge to edge. The random UV offset does nothing on a constant.
- **BK-F3 — Damage in geometry reads as stylised, not as weathering.** A second build gave about 1,900 bricks (every jamb, corner and opening edge) a broken arris: points along each edge, each nicked in by up to 10 mm. With a flat-colour face the nicks read as carved facets; the lead's word was *"stylized"*. It was turned off again. **Edge relief at that scale belongs in a normal map.**
- **BK-F4 — The overlays help only when faint.** EdgeWear01 at 0.55–0.75 (`overlay1_density`) on the flat terracotta read as paint spatter; at about 0.2 it reads as wear. Dust01 (`overlay2_density`) at about 0.1 is kept. The Set now carries both, faint, per firing colour.

### The asks

- **A1 — Build `BrickClay_Natural_Clean_Base_s01_v01`** (coverage row 3, already *Now*, Opaque, L1, s01): the fired face of a common red brick as a substance, with maps.
  - **Base colour map:** mottling within one face (firing flash, darker toward one end), sand and grit specks, the odd dark inclusion. Not a picture of a wall: no joints, no brick outlines. Tileable at 0.1 m like terracotta, so a 215 × 65 mm face shows two tiles.
  - **Roughness and normal maps:** a sand-faced or lightly textured face, small voids and pits; the relief BK-F3 tried to model.
  - **A base light enough to be tinted down.** `base_color_tint` runs 0 – 1, so a consumer can darken a firing but not brighten one. If the article's average sits at the light end of red brick, tints can reach dark and burnt firings while keeping the map's variation.
  - **Its overlays as the coverage row lists:** EdgeWear01 · Dust01 · Crevice01, with the efflorescence colour it names as *also wanted*.
- **A2 — The conditions an old wall needs** (`Identity.md`: Condition is damage, driven by overlay 1 and the maskset): `Worn` and `Distressed` states of A1, or the overlays to reach them. The look the Set needs: **soot and grime** settled on the upper faces and in pits, **efflorescence** (white salt bloom, often low on a wall and near the mortar), and a **spalled, pitted face** on a few bricks. If these are overlay colours a Creator can set (`overlayN_color`), one article with its condition sliders may be enough.
- **A3 — A mortar.** The Set's joints are `Concrete_Smooth_Worn_Dusty_s1_v01` tinted (0.62, 0.58, 0.52). An aged lime or cement mortar (sandy, gritty, slightly recessed and stained) would sit behind every brick wall. Naming and whether it is `cementitious` are the library's call.
- **A4 — Housekeeping, found on the way** (offered, not blocking):
  - `blender/asset_library/MatterLibrary.blend` still names `MildSteel_Raw_Clean_Base_s01_v01`, while its `.mtlx` is `MildSteel_Raw_Clean_Base_s1_v01` since batch 261022-1. A builder who looks the article up by its `.mtlx` name cannot find it in the Blender file, so the Set left mild steel out.
  - The same file still refers to `HairlineScratches01_overlay_s001.png` and `Scratches01_overlay_s001.png`, which are not on disk (`Scratches01` is now 0.1 m tile). Cycles reports *"Failed to load 2 image files"* when a metal or powder-coat article is rendered from it.

### A question

- **BK-Q1 — Variation across thousands of pieces.** A wall is thousands of bricks on a handful of material instances. The builder breaks the repeat with a random UV offset per brick, which works once the article has a map (A1). Is there a better way the library would rather a consumer use: a per-piece random value the masters read, a variation mask, or a documented `uv_offset` practice? The answer decides whether the builder keeps four firing instances or moves to one.

### What the asset tooling will do with it

- Point the four firing sub-objects at A1 and pull their tints back to small shifts around the article's own colour; keep the whitewash on paint; move the joints to A3; picture it before and after with the same views.
- Ask its checks again (the Creator Asset Profile, real-size UVs against the article's tile) and report back in a later pass here.

## Pass 2 — The library's review

*(Not yet written.)*
