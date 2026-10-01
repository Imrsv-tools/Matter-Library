# Research — Character materials: bringing MPFB2 / MakeHuman into the Matter Library

**Opened:** 2026-09-27 · **Mode:** research. It gathers and commits to nothing. **Ruled so far:** CM1 (a `biological` Domain), CM2 (substance in Matter, fit beside it), CM3 (superseded), CM4 (Character Materials is Phase07, right after Phase05; Library Coverage is Phase08). **Parked** (§Status).

**Question (lead, 2026-09-27, condensed):** the IMRSV platform is starting on characters, using MPFB2 (the MakeHuman plugin for Blender) and its asset library to seed and test. "We need to convert those materials into our library concept, find a home for them in the ontology… these will be different than the other materials, as they will likely be more complex, especially with skins. That is OK… if you have a better solution for anything that fits with our matter philosophy and still ends up with great results, I'm up for it."

**Extends, does not replace:** `260925_R_LibraryCoverage_FirstRelease.md` (§Not in the list: biological matter, O9), `260923_R_AgenticMaterialGeneration.md` (D1 "matter only, never assemblies", D2 "no new masters", O9, carriers C1–C3), `260923_R_StandaloneSetup.md` (Q9), `PhaseTBD_LibraryCoverage.md` (seed questions 1 and 10; it was Phase07 until CM4, un-numbered 2026-09-28, briefly Phase10 on 2026-10-01; CM-Q5's colour on layers is now `Phase10_ColouredWearLayers.md`), `PlatformDependencies.md` (M1).

**Public-repo note.** The platform's own planning is private. It is summarised here by what it needs from the library, never by its paths, phase numbers or code.

---

## Resolved — lead decisions

| # | Decision |
|---|---|
| CM1 | **Character matter lives in a new `biological` Domain** (lead, 2026-09-27: *"biological domain and the split — go with both"*). It carries the classes recommended in Pass 7, `tissue` / `keratin` / `bone`; confirm the class list at discovery. Plant matter stays in `natural/wood` and `environmental/vegetation`. `Taxonomy.md` is not edited by this research: the Domain lands when a phase builds the first article in it. Answers CM-Q1. |
| CM2 | **The split: substance in Matter, fit beside it** (same ruling). Skin, lips, nails, eye tissues, enamel, mucosa and hair fibre are Matter articles that work on any mesh. The hm08-bound layer (region masks, photo detail, card and garment atlases) is a **fit set**, outside the taxonomy; where it lives is still CM-Q6. MPFB2's library is **mined** for values, masks and reference atlases, not ported file-for-file (Pass 8b). Answers CM-Q2. |
| CM3 | **The six skins go into Phase07; the rest is its own phase** (lead, 2026-09-27: *"fold the skins into Phase07, the rest its own phase"*). **Phase07** adds the `biological` Domain and builds `Skin_FitzpatrickI…VI` on the Subsurface master (Pass 6d, with Pass 8a's `subsurface_color` rule). Recorded under Phase07's seed question 1. **`PhaseTBD_CharacterMaterials.md`** (seeded, unnumbered, after Phase07) takes everything else: the other tissues, the new inputs, CM-Q3–Q6 and CM-Q8–Q10, and fit sets. Answers CM-Q7. **Superseded the same day by CM4.** |
| CM4 | **Character Materials is Phase07, straight after Phase05; Library Coverage becomes Phase08** (lead, 2026-09-27, verbatim):<br>• *"I would like to get the character materials in as soon as possible after phase 5… Studio is going to be pulling from the matter library and there no character materials in the library at all so they will magenta… I would rather have everything in and 'uncalibrated' yet then a bunch of magenta"*<br>• *"yes, We have time so let's just do them in Phase 7 as redefined and we will be good."*<br><br>Consequences:<br>• **All** character materials, the six skins included, are in `Phase07_CharacterMaterials.md`. It runs here while Phase06 runs on the UE machine, and its articles stay **candidates** until the Unreal column exists (the momentum rule, `260926_R_BigPicture_NimbleSetup.md` Pass 8).<br>• **Eyes and mouth are done properly in Phase07, with no interim stand-in textures** ("we have time"), so CM2 holds without an exception.<br>• The platform points Studio at the library once Phase07 lands; the platform's character work already knows this approach (lead). |

---

## Pass 1 — What this library already says about characters

**Examined:** `Phase07_LibraryCoverage.md`, `PlatformDependencies.md` M1, the coverage and generation research (O9, D1, D2), `Taxonomy.md`, `MasterSet.md`, `LCDSchema.md`, `Identity.md`.

- **The pull is known and still open.** M1 asks for masters for skin, cloth and hair for the platform's character Appearance work. Phase07's Outcome names skin, cloth and hair. Its seed question 1 notes that the taxonomy has **no class** for skin, hair, bone or nails, and that hair "is not a surface material in this model" (O9).
- **D1 (lead, 2026-09-23): matter only, never assemblies.** The library holds substances (fired clay, marble), never the wall or floor made of them. This is the ruling that decides most of this research (Pass 5).
- **D2: no new masters for coverage.** Masters exist because a renderer that partitions shader space (Unreal) forces a split (`MasterSet.md` §governing insight). D2 was argued for *coverage of the existing classes*. Whether it binds a genuinely new shading model (hair, eye) is a different question (Pass 6c).
- **The modulator rule** (`MasterSet.md`): an overlay or maskset may bend a normal, bias roughness or gate a layer, and **never contributes colour**. Phase07 seed question 10 already asks whether wear layers such as dust may carry a colour. Skin adds two more cases of the same need (Pass 6c).
- **What fits already:** skin is a textbook **Subsurface** article (`subsurface_weight` / `subsurface_color` / `subsurface_radius` / `subsurface_radius_scale`, lane A). Cloth fits `synthetic/textile` as it is. Leather (textile) and ivory (mineral) were already noted as boundary cases.
- **BP8 (lead, 2026-09-26):** licensing and provenance do not block the *seed* library ("we are trying to prove a concept"). The repo is still public and its content CC0 (R9/R13), so what gets **committed** still has to be CC0-dedicable.

## Pass 2 — What the platform's character work needs from the library

**Examined:** the platform's character planning and research (private; read 2026-09-27, summarised).

1. **One canonical body.** It is an MPFB2-generated MakeHuman body on the fixed **hm08** base-mesh topology. The body arrives *pre-conformed* to the platform's skeleton and expression names, and its **UV layout is hm08's default**. The face-expression packs (`faceunits01`, `visemes02`) are MPFB2 packs, verified CC0 in their own files.
2. **Named material slots are part of the character contract:** one for body skin, one per eye, one for the mouth. Earlier drafts also split face skin, teeth and tongue, with hair and wardrobe to follow. **Slot names are the contract; the pixels are not.**
3. **"Characters do NOT travel with bespoke materials"** (the platform lead's correction, 2026-06-20). A character package carries geometry, skeleton, UVs, named slots and **library references**, and zero bespoke pixels. Materials come from a library: the Matter Library, or a character collection built on the same catalog machinery. The platform tenet behind it: "Textures are HUGE — we force them into a pre-loaded (but robust) MaterialX library."
4. **Where the platform's research put things:** tileable fabrics go to Matter as-is. Garment seams and prints go to a garment overlay or mask over a tileable fabric. Skin, eyes and hair go to "a Character domain in the same catalog machinery", with skin on the existing Subsurface master.
5. **The fork it left open: UV-painted skin vs parameterised skin.** UV-painted skin (pores that follow the face) is photoreal, but it requires the canonical UV layout. Parameterised skin (tone plus tiled detail) binds to any UVs, with a lower close-up ceiling.
6. **The Appearance work** (skin, hair, clothing, makeup) binds its slots to **Matter masters**. Whether it integrates the library fully or binds masters directly "to prove the point" is still open on the platform side (= M1). Wardrobe per scene mark is desired.
7. **The skin wish-list it recorded:** albedo, normal, micro-displacement, roughness, specular or oiliness, subsurface masks, cavity and pores, region masks, freckles and moles, expression wrinkle masks, and makeup as a layer on top. It also wants a small Creator-facing tone control (base tone, melanin, redness).

## Pass 3 — The MPFB2 / MakeHuman library, inspected in the files

**Examined (2026-09-27):**
- `makehumancommunity/mpfb2` at `3edf9df` (shallow clone): licences, material entities, node-tree templates, settings, bundled textures.
- The `makehuman_system_assets` pack (`makehuman_system_assets_cc0.zip`, 280,737,770 B, sha256 `b542127a…0107`) and the `skins01` pack (`skins01_cc0.zip`, 104,227,958 B, sha256 `7495ab99…dba9`), both downloaded and unzipped.
- Every asset-pack page on the MakeHuman community site (64 packs).

Scratch copies were in `/tmp`, outside this repo, and are **not** a reproduction. The URLs and hashes above are.

**Licence: clean for the core, mixed for the community packs.**
- **MPFB2 code is GPLv3. Its assets are CC0** (`LICENSE.md` §C: "the base mesh and proxies, targets and modifiers, textures, clothes, rigs, poses, expressions… released under CC0 1.0"). §D states that MPFB2's output carries no trace of program logic, so exports and generated data are unencumbered.
- **The system assets pack is CC0 in the bytes.** The pack's metadata JSON lists 94 assets, every one `"license": "CC0"`. Each `.mhmat` / `.mhclo` header says "explicitly released as CC0 in September 2020". `skins01`'s metadata: 23 skins, all CC0.
- **The community packs split.** The site lists `skins01–03`, `eyebrows01`, `eyelashes01`, `hair01`, `shirts01`, `suits01–02`, `system_hair_materials01` and `system_clothes_materials01` as CC0. `hair02–03`, `shirts02–03`, `dress02–03`, `pants02–03`, `shoes02–03` and others are **CC-BY**. That is 26 of the 64 packs by listing.
- ⚠ **A listing is not the bytes.** `underwear02` is listed CC-BY but its file is named `underwear02_cc0.zip`. Only the system assets and `skins01` were verified in the files. Any other pack is **unverified** until its metadata JSON has been read.

**What the library actually contains** (measured on the system assets pack, plus `skins01`):

| Category | Count | What the material file carries | Texture |
|---|---|---|---|
| Skins | 23 (+23 in `skins01`) | **one albedo map**, plus a legacy `sssEnabled` flag and per-channel SSS scale; no normal, roughness or spec map | 2048² PNG, **a UV atlas on hm08** |
| Eyes | 9 materials, 2 meshes (high/low poly) | one albedo map with alpha (iris and sclera painted together); **one mesh, no separate cornea shell** | 1024² RGBA atlas |
| Hair | 10 | albedo + alpha, two-sided, transparent | 2048² RGBA **strand-card atlas** |
| Eyebrows / eyelashes | 12 / 4 | albedo + alpha cards | 512² RGBA |
| Teeth / tongue | 6 / 1 | one albedo map (teeth and gums on one atlas) | 2048² / 1024² |
| Clothes | 20 | albedo (+ normal on 15, AO on 11) | 512²–4096², **garment atlases** |

Looked at (a contact sheet of samples):
- The skin maps are **photo-derived UV atlases of the hm08 body**, with some shading baked in (creases, fingers). A small "© MakeHuman.org" / "CC0 MakeHuman.org" mark sits in unused UV space.
- One `skins01` entry (`blindsaypatten_uniform_skin_texture`) is a **tileable** skin texture rather than an atlas. It is the only one of its kind among the sampled skins.

**Where the realism actually lives: in MPFB2's shaders, not in its library files.** MPFB2 applies one of several node-tree shaders over those plain albedo maps:
- **"Enhanced skin"** (`enhanced_skin.json` + `enhanced_settings.default.json`):
  - albedo with brightness/contrast and a small red mix-in;
  - roughness 0.45, clearcoat 0.1 at roughness 0.3 (skin oil);
  - a procedural pore bump (noise at scale 2500, strength 0.2);
  - SSS at weight 0.2 with radius RGB `(1.0, 0.2, 0.1)` × a unit scale.
  - It repeats these settings **per body region**: body, ears, fingernails, lips, nipple, toenails, genitals. Lips have smaller pores and roughness 0.35; nails have no pores and roughness 0.25.
- **The v2 procedural skin** (`entities/nodemodel/v2/composites/*skin*`). It has **no photographed texture at all**:
  - a master skin colour (a palette of ten presets);
  - procedural colour variation, spots and freckles, veins, dermal micro-bump and large-scale unevenness;
  - an SSS control;
  - a region router over **seven CC0 greyscale region masks** in `data/textures/` (`mpfb_face`, `_lips`, `_ears`, `_eyelids`, `_fingernails`, `_toenails`, `_aureolae`, plus inside-mouth and crotch), each 2048², in a UV layout of their own.
- **Procedural eyes** (`procedural_eyes.json` + `eye_settings.default.json`): a fully parametric iris (major/minor colour, pupil size, section radii, radial and clockwise pattern) and an outer layer with IOR 1.33, full transmission and roughness 0.

⇒ **"Converting their library" cannot mean porting the `.mhmat` files.** Those are albedo bitmaps plus legacy flags. The valuable, CC0 and portable part is **MPFB2's material model**: which parameters make skin read as skin, per region, and at what values. Its v2 skin is structurally the Matter model already: a base substance, region masks, and tiling procedural detail.

## Pass 4 — External grounding: measured values and shader support

- **Physically Based** (CC0; the lookup tool `tools/converters/lookup_physically_based.py`, API read 2026-09-27):
  - **Skin I–VI** (Fitzpatrick types): linear albedo from `(0.847, 0.638, 0.552)` down to `(0.09, 0.05, 0.02)`, IOR 1.4, roughness 0.5, subsurface radius `(0.482, 0.169, 0.109)` for types I–III and `(0.367, 0.137, 0.068)` for IV–VI.
  - **Eye (Cornea)**: IOR 1.376, transmission 1. **Eye (Lens)**: IOR 1.386. **Eye (Sclera)**: albedo `(0.652, 0.5, 0.394)`, IOR 1.4, the same SSS radius as skin.
  - **Bone**, and **Blood** (oxygenated and deoxygenated, with volume coefficients).
  - **No entry** for hair, nails, teeth, tongue or lips.
- **MaterialX 1.39.5** (the local toolchain build and Blender's bundled copy):
  - `open_pbr_surface` carries everything skin needs: `subsurface_{weight,color,radius,radius_scale,scatter_anisotropy}`, `coat_*` (oil) and `fuzz_{weight,color,roughness}` (vellus hair, peach fuzz).
  - The pbrlib has **`chiang_hair_bsdf`** and **`deon_hair_absorption_from_melanin`**, and `mx_chiang_hair_bsdf.glsl` exists, so there is a GLSL implementation. **A melanin-driven hair colour is standard MaterialX.**
  - *Unverified:* whether Storm (Hydra) or USDLiveView renders a `chiang_hair_bsdf` article. It is a BSDF, not an OpenPBR surface, so it breaks Decision of record 1 ("the article shader is `open_pbr_surface`"). **Probe candidate.**
- **Blender and Unreal** *(from knowledge, not re-verified this pass)*:
  - Blender's Principled Hair BSDF uses the same Chiang model with melanin and melanin-redness inputs, so the melanin parameters would be LCD-true across MaterialX and Blender.
  - Unreal has dedicated hair and eye shading models, as Substrate slabs or legacy shading models, which is exactly the kind of shader-space partition that justifies a master.

## Pass 5 — The fit problem: what in the MPFB2 library is matter

Checked against **D1** (substances in, assemblies out):

| MPFB2 asset | Substance (matter) inside it | What is object-bound (not matter) |
|---|---|---|
| Skin atlas | **skin**: tone, SSS, pores, oil, fuzz | the hm08 UV painting (face features, region colouring, baked shading) |
| Eye material | **cornea** (clear tissue), **sclera** (SSS tissue), **iris** (pigmented tissue) | the eyeball layout painted on one atlas |
| Hair / brows / lashes | **hair fibre**: keratin with a melanin colour | the card atlas (strand silhouettes, alpha) |
| Teeth / tongue | **enamel**, **gum and tongue mucosa** | the teeth-and-gums atlas |
| Clothes | **fabric**: cotton, denim, wool, leather | the garment atlas (cut, seams, prints, AO) |
| Region masks | — | lips, nails, ears, eyelids, areolae **on hm08's UVs** |

⇒ **Each MPFB2 asset is an object-bound atlas with a substance inside it.** The Matter Library is for the substance. The atlas is bound to one topology (hm08) or one garment mesh, the same way a brick wall is bound to its bricks. D1 already answers where that goes: **not into the matter taxonomy.**

⇒ **This is not a reason to refuse the atlases.** It is a reason to give them **their own home**. The taxonomy already anticipates one: the **Realm** above Domain *(planned)*, for "non-matter" sets with their own taxonomy (`Taxonomy.md` §Growth model). Alternatively they ship with the character package (platform side). See CM-Q6.

## Pass 6 — A proposed shape (the "better solution"), for the lead to test

**The split: SUBSTANCE in Matter, FIT beside it.**

### 6a — Substance articles (matter, taxonomy-homed, any mesh)

These are ordinary Matter articles, generated by the Phase03 tools. They are **topology-free**: a skin that works on any mesh, including a Creator's own character, a creature, or a sculpt in Blender. They carry tiling micro-detail at real-world scale, like every other article. This is the "parameterised skin" branch of the platform's fork. It is also what MPFB2's own v2 skin shows can look good.

A starter set, named by the `Identity.md` grammar (all ≤63 characters):

| Article (sketch) | Master | Grounding | Notes |
|---|---|---|---|
| `Skin_FitzpatrickI…VI_Clean_Base_s001_v01` (6) | Subsurface | Physically Based Skin I–VI (albedo, radius); MPFB2 roughness, coat and pore values | pore/dermal detail as a tiling normal at `s001`; the Creator's `base_color_tint` does tone |
| `LipMucosa_Natural_Clean_Base_s001_v01` | Subsurface | MPFB2's lips region (roughness 0.35, finer pores) | lips are a different tissue, not "redder skin" |
| `Nail_Natural_Clean_Base_s001_v01` | Opaque (+ coat) | MPFB2's nails region (roughness 0.25, no pores) | keratin |
| `Sclera_Natural_Clean_Base_s01_v01` | Subsurface | Physically Based Eye (Sclera) | |
| `Cornea_Natural_Clean_Base_s01_v01` | TranslucentThin | Physically Based Eye (Cornea), IOR 1.376 | only usable if the eye mesh has a cornea shell (Pass 3: MakeHuman's does not) |
| `Iris_<Colour>_Clean_Base_s01_v01` | Opaque / Subsurface | MPFB2 procedural-eye parameters, baked to texture | an iris is a *pattern on a disc*, which is on the matter/object line (CM-Q4) |
| `Enamel_Natural_…`, `GumMucosa_…`, `TongueMucosa_…` | Subsurface | MPFB2 teeth/tongue albedo as a colour reference | |
| `Hair_<Melanin>_Clean_Base_…` | **Hair** (new) or Masked (v1) | melanin/redness (MaterialX `deon_hair_absorption_from_melanin`) | see 6c |
| `Cotton_…`, `Denim_…`, `Wool_…`, `Leather_…` | Opaque | Phase07's textile rows | the MPFB2 clothes are a *reference for which fabrics are wanted*, not a source |

### 6b — Fit sets (topology-bound, beside the taxonomy)

*Working name "fit set". It is not in the Glossary: it would need a term, fixed there first, before any spec uses it.*

A fit set is a small, versioned bundle keyed by a **topology id** (`hm08`) that tells a substance *where it goes on that body*:
- **Region masks.** MPFB2's CC0 region masks for lips, nails, ears, eyelids and areolae, packed as a maskset.
- **Optional detail maps**, which could be converted from MPFB2's CC0 skin atlases: a de-lit, **neutral-toned** albedo-variation map (freckles, moles, veins, face contrast), a cavity/AO map, an expression-wrinkle mask.
- **The card atlas for each hair asset**, and **the garment atlas for each piece of clothing.** These are mesh-bound, so they may belong with the mesh asset (the Asset-Library), not here.

This keeps D1 intact and keeps every substance portable. It still delivers the photoreal close-up, because the fit set is exactly the UV-painted layer. It also makes the MPFB2 photo skins **usable**: each one's *tone* becomes a substance choice, and its *features* become a fit-set detail map.

### 6c — The contract questions this raises (the "more complex" part, named)

1. **Colour from a layer.** Region tone (redder lips, cheeks, knuckles), freckles and **makeup** all need a layer that adds **colour**. The modulator rule forbids that. This is Phase07 question 10 again (dust and grime colour), now with two more cases. **One contract change should serve all three**: a colour channel on a layer, rather than dropping the rule. → CM-Q5
2. **More than one region per material.** The maskset has one layer-2 channel (R) and three overlay gates. A skin with lips, nails and eyelids is several regions at once. Two routes:
   - **(i) Geometry.** Split the body mesh into subsets (`UsdGeomSubset`) and bind a separate substance to each (skin / lips / nails). Every region stays pure matter, and it needs **no** contract change. Boundaries are hard, which suits the lip border and nail edges.
   - **(ii) A multi-region maskset.** Soft boundaries, but it is a master-contract change.
   - Route (i) is a **platform ask** (more slots than the current four). → CM-Q9
3. **Carriers the assembler lacks.** Skin wants **coat** (oil sheen) and **fuzz** (vellus hair). These are the planned carrier C2 (coat/sheen), which is already blocking ten Phase07 articles. Characters add weight to building it.
4. **Hair and eye are real shader-space partitions.** Unreal renders hair and eyes with their own shading models, which is the governing insight's own test for a master. D2 ("no new masters") was argued for coverage and does not obviously bind them. Options:
   - **Hair:** a new `Hair` master token (melanin, redness and roughness as lane-A-like carriers, over MaterialX `chiang_hair_bsdf`); or **Masked cards** for v1 (Masked + anisotropy, carrier C3), deferring a hair model.
   - **Eye:** compose it from existing masters (Subsurface sclera/iris + TranslucentThin cornea, which needs a cornea shell), or add an `Eye` master.
   - → CM-Q3, CM-Q4
5. **The article shader rule.** A `Hair` master over `chiang_hair_bsdf` would be the first article whose shader is not `open_pbr_surface` (Decision of record 1). A probe should show that Storm/USDLiveView and Blender render it before anything is decided.

### 6d — What "seed and test" can use soonest (no contract change)

In the order it could happen:
1. **Six skin articles, `Skin_FitzpatrickI…VI`, on the Subsurface master** from Physically Based, with MPFB2's roughness and pore values and one tiling pore overlay. These need only today's assembler plus one new overlay.
2. **Put one on the MakeHuman body in the Phase05 rig** (Blender + USDLiveView, then Unreal after Phase06). The platform's character is already that body.
3. For the side-by-side, **the same body with an MPFB2 CC0 photo atlas** as a local, uncommitted test. This shows the lead how far "substance only" is from "UV-painted" before anyone builds fit sets. It is a disposable probe (it builds nothing in the repo).
4. Cornea, sclera, lips, nails, enamel and mucosa follow the same path. Hair waits on CM-Q3.

### 6e — The literal port, compared

| | A. Port each MPFB2 skin as an article | **B. Substance only** | **C. Substance + fit sets (recommended)** |
|---|---|---|---|
| Fits D1 and the taxonomy | ✗ (object-bound atlases, `sUKN`) | ✓ | ✓ (fit sets outside the taxonomy) |
| Works on any mesh | ✗ hm08 only | ✓ | ✓ (substance); fit adds hm08 detail |
| Close-up realism | photo, but baked shading and no maps beyond albedo | parametric ceiling | photo detail where a fit set exists |
| Parity across renderers | poor (albedo-only; realism was MPFB2's Blender shader) | good (standard masters) | good |
| Contract change | none, but it breaks the ontology | none to start | a fit-set concept + CM-Q5 |
| Seed/test speed | fast to copy, slow to make good | **fastest to a real render** | B first, then C |

**Recommendation: B now, growing into C.** Build skin as matter first: it is quick, portable and parity-testable in the rig that exists. Then decide the fit-set home once the rig shows how far substance-only falls short on the MakeHuman body at close range. This keeps "matter" meaning matter, and it gives the platform a skin on day one.

## Pass 7 — Where it lives in the ontology (options for CM-Q1)

| Option | Shape | For | Against |
|---|---|---|---|
| **1. A new Domain `biological`** | classes `tissue` (skin, mucosa, sclera, cornea), `keratin` (hair, nail, horn, feather), `bone` (bone, enamel, dentin; ivory later) | one coherent home for people **and** creatures; room to grow; Physically Based's own categories are "Human" and "Organic" | the first new Domain since the original five; boundary with `natural/wood` and `environmental/vegetation` (plant matter stays there) |
| 2. Classes under `natural` | `natural/tissue`, `natural/keratin`, `natural/bone` | no new Domain; `natural` already holds wood, which is biological | "natural" becomes a catch-all |
| 3. A Character Realm | a separate taxonomy for characters | matches the platform's "Character domain" wording | puts *substances* outside Matter, which is backwards: the substance is matter, only the fit is not |

Domain and Class are **folder-only** (`Taxonomy.md`), so any of these can be changed later without renaming an article. Adding classes is semver-minor. **Adding a Domain is not covered by today's growth model**, so it is a lead call either way.

**Recommendation: option 1, `biological`**, with `tissue` / `keratin` / `bone`. The **fit sets** (6b) go to the Realm idea or to the character package, **never** into a Domain. **→ Ruled 2026-09-27: CM1.**

## Pass 8 — The lead's two follow-ups (2026-09-27)

**Asked, verbatim:** *"should we consider a new master material for skin or will we have the controls we need to make SubSurfaceScattering and other realism effect work? Is the approach that we would move MH materials into our library, refine them so they are good in MaterialX and then make NEW blender and UE versions that then Blender would consume OUR version?"*

### 8a — A Skin master? Not on the graph side. Possibly on the settings side, so measure it.

`MasterSet.md` defines a master as **a graph plus a settings block**. It justifies a new master only where a renderer that partitions shader space forces one. So the question splits in two.

**The graph: the Subsurface master can carry skin once three inputs are added.** Measured 2026-09-27: `subsurface_weight` / `_color` / `_radius` / `_radius_scale` are carried by the recipe schema, the assembler (`assemble_mtlx.py`, lane A) and the Blender proxy. What skin's realism needs, and where each piece lands:

| Effect | Where it lives | Today | Master needed? |
|---|---|---|---|
| Light bleeding through skin (colour + per-channel distance) | `subsurface_*` (OpenPBR) | ✅ carried | no |
| Forward scattering | `subsurface_scatter_anisotropy` | ✗ not carried | no, add a lane-A input |
| Skin-oil sheen (a second specular lobe) | `coat_weight` / `coat_roughness` / `coat_ior` | planned carrier **C2**, not built | no |
| Peach fuzz (vellus hair) at grazing angles | `fuzz_weight` / `fuzz_color` / `fuzz_roughness` | ✗ not carried, not planned | no, add a lane-A input |
| Skin's specular level (IOR ≈ 1.4) | `specular_ior` | ✅ carried | no |
| Pores and fine lines (micro-normal + roughness) | an **overlay** at `s0001`/`s001` | ✅ mechanism exists; the layer has to be generated | no |
| Region tone, freckles, makeup | a layer that adds colour | ✗ forbidden by the modulator rule (**CM-Q5**) | no; a contract change, not a master |
| Cavity / specular occlusion in creases | OpenPBR has no specular-occlusion input | open: fold into roughness/specular, or a fit-set map | no |
| Expression wrinkles | a wrinkle overlay whose `overlayN_density` the consumer drives from the face expression | the port exists; the drive is consumer-side | no |

⇒ **No new master for the graph.** Skin needs three more lane-A inputs (scatter anisotropy, coat, fuzz; coat was already planned as C2), plus the CM-Q5 colour-layer ruling. All of them are additive.

**The settings: this is where a Skin master could still be justified, and it should be decided on rendered evidence.**
- **Blender:** the Principled BSDF picks a subsurface **method** per material: Christensen-Burley, Random Walk, or Random Walk (Skin). *(From knowledge; not re-verified this pass.)* Our proxy sets none, so Blender's default applies.
- **Unreal:**
  - Its legacy model has a cheap wrap-style `Subsurface` shading model and a separate skin-grade `Subsurface Profile` model. That is a real shader-space partition.
  - Under Substrate (the R15 target), a slab takes its scatter distances per pixel, with an optional profile. Whether the scattering *type* is a static, per-material choice there is **unverified**.
- **USD viewers:** one model, approximated. Decision of record 9 already sets their bar for subsurface at "recognisable".

⇒ **Recommendation (CM-Q10):**
- Raise the Subsurface master's settings intent to **diffusion-grade** for every subsurface article (marble, jade, wax, milk, skin).
- Then render **Marble and one skin** in the Phase05 rig, and Phase06's once it exists, under each candidate setting.
- **If one settings block serves both, keep one master.** If skin needs a setting that makes marble wrong (for example Blender's skin-specific random walk, or a profile asset in Unreal), add a **`Skin` master token**. Adding a token is additive, so it is semver-minor.
- Either way, **eyes and hair**, not skin, are the likelier new masters (CM-Q3 / CM-Q4).

**A parity gap found while checking (Blender).**
- `tools/generators/matter_proxy.py`'s Subsurface branch sets only `Subsurface Weight` and `Subsurface Radius` (× scale). It sets no method, anisotropy, coat or fuzz.
- Blender's current Principled BSDF also has **no separate subsurface colour**: it scatters the base colour. *(From knowledge; check at the build.)* So an article whose `subsurface_color` differs from its base colour renders one way in MaterialX and another in Blender.
- ⇒ **Rule for skin articles, to stay LCD-true:** leave `subsurface_color` equal to the base colour, or unset, and express the skin's reddish scatter through `subsurface_radius_scale` (Physically Based's `(0.482, 0.169, 0.109)` does exactly that).

### 8b — The pipeline: yes, with three corrections

**The shape the lead describes is the library's architecture already** (`_Architecture.md` §Key characteristics): "MaterialX is the single source of truth… Blender and Unreal representations are **derived**, never hand-authored as the master." For characters it runs:

```
MPFB2 / MakeHuman (CC0)          values · shader settings · region masks · reference atlases
        │  mined, not copied
        ▼
recipe (per article) ──► assembler ──► .mtlx (the article; single source of truth)
        │                                   │
        │                                   ├─► judged in the rig: Storm · Blender · Unreal, side by side (BP3)
        │                                   └─► release (manifest · catalog · freeze)
        ▼
Blender:  generated MatterLCD_<id> proxy (matter_proxy.py) in the Asset-Browser library
Unreal:   no per-material asset; the Subsurface reference master + the article's data (Phase06)
```

1. **We don't move the MakeHuman materials in; we mine them.** The `.mhmat` files hold an albedo map and legacy flags (Pass 3). What we take is MPFB2's CC0 **settings** (roughness per region, pore scale, SSS radii), its **region masks**, and its photo atlases **as fit-set input** (CM2). Every article comes out of a recipe and the assembler, like every other article; none is hand-edited.
2. **"Good in MaterialX first, then port" becomes "good in all three at once".** BP3: no single renderer is the truth. A skin passes when Storm, Blender and Unreal agree within the Subsurface bar across the slider sweep, and it looks like skin. That is the rig's job.
3. **There are no hand-made Blender or Unreal versions, but the Blender one has to be *good enough*.**
   - Blender's version is **generated** from the same recipe (the `MatterLCD_<id>` proxy). Unreal's version is **data** on one reference master per token (Phase06 / *Unreal Reference Masters*); no per-material Unreal asset exists.
   - **Blender consuming our version** means: MPFB2 generates the body; our Asset-Browser library supplies the skin; it is bound to the body's slots; our exporter writes the character with **Matter identity references**, and the platform resolves them by name. That is the platform's "no bespoke pixels" rule.
   - **The catch:** MPFB2's own Blender skin shader is richer than our proxy today (8a gap). An artist who swaps MPFB2's skin for ours would see a step down until the proxy generator gains the same inputs. **Extend the proxy in the same unit as the three new carriers**, never after.
   - Who does the slot binding in the platform's character generator is **platform-side** (an M1 ask).

---

## Open questions

| # | Question | Why it matters | Recommendation |
|---|---|---|---|
| ~~CM-Q1~~ | ~~Ontology home~~ | — | ✅ **Ruled CM1 (2026-09-27): `biological`** |
| ~~CM-Q2~~ | ~~Literal port or split~~ | — | ✅ **Ruled CM2 (2026-09-27): the split** |
| CM-Q3 | **Hair:** a new `Hair` master (Chiang/melanin), or Masked cards for v1? | The first non-OpenPBR shader, or no hair model at all | Masked cards to seed; probe `chiang_hair_bsdf` in Storm and Blender before ruling |
| CM-Q4 | **Eyes:** composed from existing masters, or an `Eye` master? Is an iris matter? | MakeHuman's eye has no cornea shell | Compose for v1 (a sclera/iris atlas as a fit, cornea when a shell exists) |
| CM-Q5 | **A colour channel on layers** (region tone, freckles, makeup, and Phase07's dust colour) | The modulator rule forbids it today; four needs point at one change | Rule it once, together with Phase07 question 10 |
| CM-Q6 | **Where do fit sets live?** A Realm in this repo, the character package, or the Asset-Library? | hm08-bound data is not matter (D1) | Undecided. The rig comparison (6d step 3) should come first |
| ~~CM-Q7~~ | ~~Who owns the build~~ | — | ✅ **Ruled CM3, then CM4 (2026-09-27): all of it is `Phase07_CharacterMaterials.md`, right after Phase05** |
| CM-Q8 | **The CC-BY packs:** use them locally for testing only, or not at all? | BP8 frees the seed from provenance, but a public CC0 repo cannot carry CC-BY pixels | Local testing only; never committed |
| CM-Q9 | **Ask the platform for region slots** (skin / lips / nails as mesh subsets)? | Route 6c.2(i) needs no contract change here | Raise it under M1 when the platform opens its Appearance work |
| CM-Q10 | **A `Skin` master, or skin on the Subsurface master?** (Pass 8a) | The graph needs no new master, only three lane-A inputs; the per-material *settings* (Blender's subsurface method, Unreal's shading model) might differ between marble and skin | One Subsurface master with diffusion-grade settings; add a `Skin` token only if the rig shows marble and skin need different settings |

## Status

- **Passes captured:**
  1. Prior art in this library (O9, D1, D2, M1, Phase07 questions 1 and 10, the modulator rule).
  2. What the platform's character work needs (one hm08 body, named slots, "no bespoke pixels", the UV-painted-vs-parameterised fork, the skin wish-list).
  3. The MPFB2 / MakeHuman library in the files:
     - licences: code GPLv3, assets CC0, output unencumbered; the system pack and `skins01` verified CC0; 26 of 64 community packs CC-BY by listing, one listing contradicting its filename;
     - the skins are albedo-only 2048² hm08 atlases, and the realism lives in MPFB2's shaders;
     - the enhanced and v2 skin parameters, the region masks and the procedural eye were extracted.
  4. External grounding: Physically Based Skin I–VI, cornea, lens and sclera, with no hair, teeth or nails; OpenPBR covers skin; MaterialX 1.39.5 has a melanin-driven Chiang hair BSDF with GLSL.
  5. The fit problem: every MPFB2 asset is an object-bound atlas with a substance inside it (D1).
  6. The proposed shape: substance in Matter, fit sets beside it; contract questions named; a no-contract-change seed path.
  7. Ontology options.
  8. The lead's follow-ups (2026-09-27):
     - **8a:** skin needs no new master for its graph, only three lane-A inputs (scatter anisotropy, coat = C2, fuzz) plus CM-Q5. The per-material settings (Blender's subsurface method, Unreal's shading model) decide whether a `Skin` token is ever needed, measured on Marble vs skin in the rig (CM-Q10).
     - **8a, Blender:** the proxy's Subsurface branch is minimal. Blender scatters the base colour, so skin articles keep `subsurface_color` equal to the base colour.
     - **8b:** the pipeline is the architecture already: mine MPFB2 → recipe → `.mtlx` → judged in all three renderers → a generated Blender proxy and Unreal data on the reference master. There are no hand-made versions, but the proxy has to be extended alongside the new inputs.
- **Decided (2026-09-27):** **CM1**, a `biological` Domain; **CM2**, substance in Matter with fit sets beside it; **CM3**, six skins in Phase07 and the rest in a seeded phase, superseded the same day by **CM4**: Character Materials **is Phase07**, straight after Phase05 and alongside Phase06, with candidates until Unreal calibrates them and no eye/mouth stand-ins. Library Coverage is Phase08.
- **Current direction:**
  - build skin (then lips, nails, eye tissues, enamel, mucosa) as **Matter substances** in `biological/tissue` (etc.) on the Subsurface master, grounded in Physically Based and MPFB2's CC0 settings;
  - add the three lane-A inputs and the matching Blender proxy inputs;
  - judge Marble and a skin on the MakeHuman body in the Phase05 rig (CM-Q10);
  - then decide the home for hm08-bound **fit sets** (CM-Q6).
- **Unverified, recorded as such:**
  - that Storm/USDLiveView render `chiang_hair_bsdf`;
  - that Blender's Principled Hair and Unreal's hair and eye shading models match the MaterialX parametrisation (from knowledge);
  - the licence of any pack other than the system assets and `skins01` (listing only);
  - the region masks' UV layout relative to the skin atlases (they look like a separate layout; not traced).
- **Open questions:** CM-Q3 to CM-Q6 and CM-Q8 to CM-Q10 (CM-Q1, Q2 and Q7 are ruled). All of them now belong to `Phase07_CharacterMaterials.md`'s discovery. CM-Q10 is answered by rendering, not by ruling. None blocks the six skins.
- **Next step:** the research thread is **parked**. Phase07 opens by the lead's deliberate `/discovery` once Phase05 closes. That discovery rules the contract calls early, so Phase06's Unreal masters are built against them, and it checks the Blender-side Subsurface details marked "from knowledge" (the method enum, no separate subsurface colour).
