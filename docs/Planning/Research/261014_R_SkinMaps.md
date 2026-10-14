# Research — Skin maps: moving character skin from a tone per part to painted maps

**Opened:** 2026-10-14, seeded · **Mode:** research. It gathers and commits to nothing. **Mnemonic:** `SKM` (ids `F-SKM-n`, `Q-SKM-n`, `RD-SKM-n`).
**Requested by:** the lead, 2026-10-14, verbatim: *"I don't think this skintype per area of a mesh apprach is gong to yeild good results... Right now... it is pretty terrible in fact (the line between lips and face and no variation)... I think we need to plan to move to SkinMaps (if that is wht they are called)... feel free to seed a reseerach on this topic and we can dig in to what the industry is doing pros/cons"*.
**Altitude:** a **design** question: what character skin should be, and how the industry gets there. Pass 1 is what this repo already holds; Pass 2 is the lead's clarification of MAP-RD2; **Pass 3 is the industry survey** (run 2026-10-14, web only); Pass 4 is what the survey means for this repo, measured.
**Measured at:** `0474de4` (Passes 1–2), `867d5bd` (Passes 3–4), both 2026-10-14.

**Extends, does not replace:**
- `260927_R_CharacterMaterials_MPFB2.md` (CM2: substance in Matter, fit beside it; Pass 3's inventory of MakeHuman's skins);
- `260929_R_CharacterMaps.md` (MAP-RD1 to RD6; Passes 2–4: the atlases, what they carry, the replace-or-modulate probe);
- `261014_R_MaterialPipeline.md` (F-MP-35, Q-MP-6, now answered here).

**Words.** The industry's terms (checked in Pass 3):
- **skin map** or **skin texture** (the lead's word): the painted pictures of a character's skin. The vendors say *texture* or name the map (base colour, normal, cavity).
- **atlas**: those pictures laid out on one body's **UV layout**, the mesh's flattened map. A layout split into numbered tiles is a **UDIM** layout.
- **micro detail**: a small tiling pattern (pores, fine wrinkles) laid over the atlas. Epic says *micro skin detail*, Character Creator *micro normal*, Daz *detail normal*. The library's is `Skin_Pores`.

The library's word for a picture a mesh supplies at binding is a **fit-set** picture (Glossary).

---

## The lead's earlier rulings this reopens (quoted, not paraphrased)

> **Corrected 2026-10-14, the same day (Pass 2, RD-SKM-1): it reopens neither MAP-RD2 nor CM2.** The lead explained that MAP-RD2 is about **locking the mesh**, not about pictures: one approved human mesh, so any skin map made for it is allowed. The section below is kept as it was first written. What MAP-RD2 actually means is RD-SKM-1. Only MAP-RD5's *"skin stays general"* clause is superseded, by the move to skin maps (RD-MP-9).

- **MAP-RD2** (2026-09-29): *"No picture that fits only one mesh"* (*"no bespoke one image one mesh solutions"*). *"A library texture that fits any mesh following a known layout, placed by settings, is fine … a picture painted to one mesh's UV layout is not."* It retired every option that supplied a body's own skin picture (MAP S-a, S-b, S-c) and MAP-Q4 (*"which skin atlas, at what strength"*).
- **MAP-RD5** (2026-09-29): *"skin stays general and gains what already exists but does not reach Studio (coat, fuzz, glow)"*.
- **CM2** (2026-09-27): *"The split: substance in Matter, fit beside it … The hm08-bound layer (region masks, photo detail, card and garment atlases) is a fit set, outside the taxonomy."*

**A skin map does not have to break CM2:**
- the skin **article** stays the substance (tone, scatter, coat, fuzz, pores);
- the body's **map** is a fit-set picture beside it, supplied when the skin is bound, as the eye's and the hairstyle's pictures already are.

**It does reopen MAP-RD2 and MAP-RD5**, unless the map counts as *"a library texture that fits any mesh following a known layout"*. One map for the hm08 layout fits **every** MakeHuman body, as the eye's picture fits every MakeHuman eye. Whether it counts is the lead's call (Q-SKM-1).

## Pass 1 — What the library already holds (measured 2026-10-14)

- **F-SKM-1 — Skin today is a tone per part.**
  - Six skin articles (`Skin_FitzpatrickI` … `VI`), on **Subsurface**. Each is a Physically Based tone plus `Skin_Pores`, a 1 cm tiling normal and roughness, plus coat and fuzz.
  - Lips and nails are separate articles per tone (Phase08), each bound to its own mesh part (PlatformDependencies P15, *"one slot per substance"*).
- **F-SKM-2 — Why the lead sees a hard line and no variation.**
  - **The hard line:** the lips are their own part with their own flat tone, so the colour changes exactly at the part's edge.
  - **No variation:** the body is one tone everywhere. There are no redder cheeks, ears or knuckles, no darker eye sockets, no freckles or veins.

  A painted map carries exactly that. MAP Pass 3 measured it in MakeHuman's atlases: *"darker lips, nostrils, eye sockets, knuckles, nipples, redder ears and cheeks"*.
- **F-SKM-3 — The input a skin map needs already exists.**
  - Phase09 built `base_color_map`: a mesh's own picture, supplied at binding and **multiplied** into the article's base colour (`base_color_const × base_color_map × base_color_tint`).
  - It works on the **Subsurface** master (Glossary, *Base colour map*; LCDSchema §Base colour map), which the skin articles use.
  - It is in Blender, USD viewers and the library's Unreal masters (`base_color_map_tex`, P21).

  So a first skin map could reach every renderer with **no contract change**. What it would not carry is a map for anything but colour (roughness, normal, scatter thickness, Pass 3).

  *(Narrowed 2026-10-14, Pass 4, F-SKM-19: no contract change, but **the skin articles themselves must be re-assembled first**. They do not declare the input, and their fixed scatter colour at full weight would hide a map.)*
- **F-SKM-4 — The sources on hand** (MAP Pass 2, CM Pass 3; CC0, MakeHuman / MPFB2):
  - **22 photo-derived skin atlases** on the hm08 layout: 2048², colour only, young/middle/old × African/Asian/Caucasian × female/male. Some shading and stubble are baked in, and a small MakeHuman mark sits in unused space.
  - **`sss.png`:** a 2048² scatter-thickness map (bright at ears, nose, lips, fingers).
  - **10 region masks**, including face, lips, ears, eyelids, nails, areolae, inside the mouth, crotch and genitals.
  - **One tileable skin** in `skins01`.
- **F-SKM-5 — It was probed once.** MAP-F4: an atlas used as a **tone-free detail layer**, read by its brightness and multiplied into each Fitzpatrick tone (the multiply that `base_color_map` now does). The brightness ÷ mean ranges 0.46–1.48, and the atlas's baked shading comes along. *"Rejected"* there only by MAP-RD2.
- **F-SKM-6 — What it brings in that the library has kept out.** A full-body map carries intimate anatomy. That brings the skin-publishing guidance's whole track into play (`261014_R_MaterialPipeline.md` Pass 4):
  - adult-only classification;
  - honest disclosure on the download;
  - non-intimate thumbnails;
  - review of the actual picture at full resolution;
  - **every host's content policy**, starting with this public GitHub repo, where the fit set lives today, and the release host (RD-WS-2).

  Photo-derived sources also raise the guidance's *real-person* question: whose skin was photographed, and with what consent, even under CC0.

## Pass 2 — The lead's clarification: one approved mesh, skin maps per mesh version (2026-10-14)

**The lead, verbatim:** *"No it does not reverse my one image one mesh ruling....That has been mis understadd or perhaps I explained it wrong... Currently we are using ONE approved mesh for humans (people can shape and wieght it any way they want but a mesh on A rig we picked (Manny)) ... so ALL skinmaps should work with taht mesh.... that is what is meant by that rulling... it is more about locking mesh then it is about materials... So in the furure we may support a new mesh (more detailed or whatever) and then there wioudl need to be a new Material spec for a SkinMap..but then any mesh that stays to the count/shape shoudl be abel to use any of that versions skinmap... does that make sense? Am I getting the techincal part wrong? I assume that is doable"*.

- **F-SKM-7 — It is technically right.** A skin map is drawn on a mesh's **UV layout** (its flattened map), and the layout belongs to the mesh's topology: its vertices, faces and the seams that cut them. **Shape and skinning do not move it.**
  - Changing the body's shape (morph targets, sculpting a vertex's position), its skeleton or its weights leaves every vertex's UV coordinates where they were.
  - So **every character built from the approved mesh can wear any skin map made for that mesh**, as the lead says.
  - This is how the industry's character systems work. MetaHuman's, Character Creator's and Daz's skins each fit one base mesh and every body shaped from it (to confirm in Pass 3).
- **F-SKM-8 — The approved mesh, measured.** It is **MakeHuman's hm08 body**, rigged to the **Manny** skeleton. The body is the one this library's rig already renders (`tools/parity/scene/build_character.py`), and the platform builds its characters from it.
  - Read in the platform's own docs, read-only, 2026-10-14; nothing beyond this fact is carried here.
  - The skeleton is a separate thing from the UV layout, so a map is not tied to Manny; it is tied to hm08's layout.
- **F-SKM-9 — Three limits, none of which breaks the rule:**
  1. **A large reshape stretches the picture.** A much heavier or taller body spreads the same pixels over more skin, so painted detail grows with it. The library's tiled pores stay at real size only if the tile is set per body (the detail UV set, PlatformDependencies P18).
  2. **The parts must keep the original layout.** The body is split into one part per substance (P15: Body, Lips, Nails, …). The split moves no UV, so one map covers every part. **With a map, the lips can wear the skin article and the map's own lip colour, which removes the hard line** (F-SKM-2).
  3. **A new mesh needs its maps made again.** A map can be transferred from one layout to another by baking, but some detail is lost. That is what the lead's *"a new Material spec for a SkinMap"* per mesh version covers.
- **F-SKM-10 — The library already has the place for it.** The fit set is kept per mesh family: `MatterLibrary/textures/fit/makehuman/`, holding hair and eyes today. **A skin map is a fit-set picture for the approved mesh**, and a new mesh version becomes a new family (or a version of it). So the skin map changes no part of CM2: the substance stays in the article, and the mesh's picture stays beside it.

## Pass 3 — The industry survey (run 2026-10-14)

The questions, written before the survey so it answers them and not others:

1. **Which maps** make convincing skin, and which matter most: colour; roughness or specular; normal and cavity; displacement; scatter or thickness; micro detail.
2. **Layout:** one atlas per body (a single 0–1 layout) or tiles across several (UDIMs). Resolution for real-time (Studio) and for offline (Blender, Cycles).
3. **The common shape:** a body atlas for the large-scale variation **plus** a tiling micro-detail layer (the library's `Skin_Pores` already is one). Confirm how MetaHuman, Character Creator, Daz and scan vendors split the two.
4. **Skin tones:** one neutral map recoloured by tone (the library's multiply), or a map per tone? What do the tools do, and what breaks: baked shading, freckle colour.
5. **How the maps are made:** scans (licensing, consent); photo atlases with the light removed; painted; procedural; AI-generated (the guidance's uncertain copyright; RD-MP-1's licences).
6. **Intimate anatomy:** do public, open libraries ship it, and how? Options: neutral regions, separate maps, an adult-only package.
7. **Where the maps live:**
   - the library's fit set (public repo, CC0 or CC BY);
   - the platform's character package;
   - a separate adult-only package.

   Each against MAP-RD1 (*"the library prepares every material and every asset; consumers only consume"*).
8. **Unreal and Studio:** the cost of the maps in a real-time body material; what Substrate's subsurface does with a thickness map.

**Examined:** three web sweeps (2026-10-14). Each was given the lead's rulings verbatim (RD-SKM-1, MAP-RD1, RD-MP-1, RD-MP-8, the guidance's thumbnail line). They covered:
- the character systems' map sets (MetaHuman, Character Creator 4/5, Daz Genesis 9, MPFB2, Epic's skin guidance);
- how maps are made and licensed;
- intimate anatomy and the hosts' policies.

**Sourcing marks:**
- **read**: read on the vendor's or host's own page, docs, source or licence text;
- **second-hand**: a forum, store listing, search summary or secondary article, **not verified**.

Every claim about another system is as of 2026-10-14; recheck at that system's next major release. Nothing was run.

- **F-SKM-11 — Which maps, in the order the industry drops them** (question 1).
  - **MetaHuman** (read, Epic's MetaHuman docs). Each of the face and the body has:
    - a base colour (skin plus accents, make-up and freckles);
    - "SRMF" (specular, roughness, metallic and fuzz in one picture);
    - a normal;
    - a cavity (an override slot);
    - a scatter map (512²).

    The face adds animated wrinkle deltas. Its quality ladder drops the tiling micro detail first (LOD1), then the wrinkle maps (LOD2), then subsurface (medium/low quality). **Base colour and one baked normal survive to the last LOD.**
  - **Epic's skin guidance** (read):
    - base colour matters most at a distance;
    - roughness starts as a constant (~0.4), and specular is fixed at 0.35;
    - **the face's normal holds wrinkles only; pores come from a separate tiling micro normal.**
  - **Character Creator 4/5** (read). The usual colour, normal and roughness, plus transmission, scatter, a micro normal with its mask, and region masks. The head takes eleven pictures.
  - **Daz Genesis 9:** a dual-lobe specular and a detail normal (read); per-surface colour, normal, roughness and translucency (second-hand).
  - **So the order is:**
    1. colour;
    2. a normal for wrinkles and folds;
    3. the tiling micro normal;
    4. roughness or specular variation;
    5. cavity;
    6. scatter or thickness.

    **The library already has the third (`Skin_Pores`) and a constant for the fourth.** The first is the one the lead is missing.
- **F-SKM-12 — Layout** (question 2).
  - **Character Creator:** a tile (UDIM) per region (read), with the face, hands and nails given enlarged UV space (read). About 4K per region (second-hand).
  - **Daz Genesis 9:** several tiles by default, with a one-tile option (second-hand).
  - **MetaHuman:** separate face and body sets (read). Downloads are 2K, 4K or 8K, and the optimised build caps at 2K (read).
  - **MakeHuman (the approved mesh):** one 0–1 hm08 layout.
  - **Consequence:** one atlas for the whole body gives the face a small share of its pixels. The systems built for close-ups give the face its own map or tile. **How many pixels hm08's face gets on a 2048² atlas is not measured** (the probe, below).
- **F-SKM-13 — The common shape is confirmed: a body map plus a tiling micro layer, on the same UVs** (question 3).
  - **How each system tiles its micro detail:**
    - **Epic:** pores come from a tiling normal on the texture coordinate times a tiling factor (read).
    - **Character Creator:** the micro normal is tiled over the same UVs, 42× on the body and 20× on the head, and scaled per area by a mask (read).
    - **Daz:** a detail normal times a weight (read).
    - **None found uses a second UV set or a projection.**
  - **This is already the library's shape.** One UV set carries both layers, which is also all Storm can read (Learnings S9):
    - `base_color_map` is sampled on texcoord 0 directly, not through `place2d` (LCDSchema §Base colour map);
    - the article's `Skin_Pores` goes through `place2d`, which the binding sets to ≈ 0.006 on the raw hm08 atlas (LCDSchema §UV placement; P18's stopgap).
  - **An observation, not a reversal:** P18's real-scale detail UV set (Phase07 F13, ruled (b) by the lead 2026-09-27: *"A real-scale detail UV set on the character mesh"*) is not how the surveyed systems do it. What it buys is real-size pores on any body shape (F-SKM-9, limit 1). The phase weighs it.
- **F-SKM-14 — Skin tone: the leading systems do not tint one map** (question 4).
  - **MetaHuman** (read, its API docs):
    - a tone is a position in a two-dimensional skin-colour space;
    - the face's colour map is **synthesised** for that position from a model built on scans, and the body's takes a gain per tone;
    - normal and cavity maps are **chosen** from a set, not synthesised;
    - freckles and "accents" (redness, saturation, lightness) are separate controls.
  - **Character Creator SkinGen** (read): a layer stack from the base to body hair, with presets by age, gender and ethnicity, built from licensed Texturing.XYZ scans.
  - **MPFB2** (read): separate CC0 skins per look, plus a colour mix-in to shift them.
  - **Biophysical models** (read at abstract level): melanin and haemoglobin as two maps. Donner et al. 2008 is offline; Jimenez et al. 2010 is real-time, at *"negligible overhead"*.
  - **Against the library:**
    - What MAP-F4's multiply by luminance does: it gives each tone its darker lips, nostrils and sockets.
    - What it cannot do: it carries no hue, so it cannot make cheeks, ears or knuckles **redder**, which is half of what the lead found missing (F-SKM-2).
    - What MAP-F4 found when it tried to carry hue: a per-channel ratio cast the dark tones olive, because it brought the source photo's own colour.
    - Redness is the haemoglobin half of skin colour, and MetaHuman gives it a control of its own.
- **F-SKM-15 — How skin maps are made, and what an open library can use** (question 5).

  | Route | What the survey found | Usable here? |
  |---|---|---|
  | **Commercial scans** (Texturing.XYZ, 3D Scan Store / Ten24) | Both licences forbid releasing the material, or anything derived from it, under an open licence (read, verbatim: *"Release Materials or derivative products under an Open Source License"*). Neither states a model release. | **No** |
  | **Research scan sets** (Multiface, FaceScape) | Non-commercial licences (second-hand) | **No** |
  | **MakeHuman's photo atlases and skin packs** | CC0 (read: MakeHuman's `LICENSE.md` and its asset-pack page), on the hm08 layout. **No source says where the photos came from or records the consent of the people photographed** (searched; nothing found). | By licence, yes. **It collides with F-MP-19** (`261014_R_MaterialPipeline.md` Pass 4, verbatim: *"No photographs of people as a source unless rights and consent are documented, and excluded by default"*). F-MP-19 is a finding from the lead-supplied guidance, not yet a ruling. |
  | **Painted** | MakeHuman's own route is painting over its CC0 "Annotated Skin" (read) | Yes |
  | **Procedural** | MPFB2's layered skin is *"mostly procedural, but often use diffuse and normal maps"* (read). No system found is purely procedural; SkinGen layers scans. | Yes, but its quality is unproven |
  | **AI-generated** | Creative Commons recommends CC0 for works without significant human creativity (read). The US Copyright Office's Part 2 report (29 Jan 2025) says prompts alone are not authorship (date read; content second-hand). MetaHuman's synthesis is model output from scan data under Epic's licence (second-hand). | CC0 in form; **whose skin trained the model is the consent question again** |

  **Moving maps to a future mesh version:** Wrap and Mesh-to-MetaHuman match points and rebake, with hand fixes at the eyelids and nails (mostly second-hand). No measured loss was found. F-SKM-9's limit 3 stands, unquantified.
- **F-SKM-16 — Intimate anatomy: no surveyed system ships it in the base body** (question 6).
  - **MakeHuman** (read):
    - genitals are a proxy, *"removed from the official MakeHuman bundle"* to user-contributed assets;
    - the official asset-pack list (newest pack 2026-08-30) has underwear packs and no anatomy pack.
  - **Daz Genesis 9:** anatomical geometry comes in a separate expansion, with textures only in some character products (second-hand).
  - **Character Creator:** a nude default body without genitals, which come as third-party parts (second-hand).
  - **MetaHuman:** third-party 18+ add-ons, which implies none in the base (second-hand; no Epic statement found).
  - **The common pattern: a neutral base, with anatomy as a separate opt-in package hosted elsewhere.** No system was found that bakes underwear into the skin. How any system's default skin paints the areolae and groin was not found.
- **F-SKM-17 — The hosts** (questions 6 and 7).
  - **GitHub** (read):
    - it bans pornographic content, non-consensual intimate imagery and graphic sexual acts;
    - *"We recognize that not all nudity or content related to sexuality is obscene"*;
    - it *"may allow"* nudity *"in artistic, educational, historical or journalistic contexts"*, and *"a disclaimer can help communicate the context of the project"*;
    - no separate rule for LFS or Releases was found.
  - **Fab** (read): 18+ content is allowed only when flagged Mature; explicit content is never allowed.
  - **Sketchfab** (read, 2026-08-04): nudity must be flagged Restricted, and the flag shows on the thumbnail.
  - **Apple:** user content that is not safe for work is hidden by default (read).
  - **Blender Extensions** (read, 2026-08-10): no nudity clause, but the "no surprises" description rule applies, and online access needs the user's consent.
  - **So:**
    - **a neutral map is fine on every host;**
    - an anatomical map is allowed on GitHub only in context, and would need a flag on every store a consumer ships through.
- **F-SKM-18 — Unreal, Storm and Blender** (question 8).
  - **Unreal:**
    - Substrate is production-ready in Unreal 5.7 and the default for new projects (read).
    - Its slab takes a chromatic scatter distance, anisotropy and a second roughness, the dual lobe (read). A thickness-map input was not found.
  - **Storm:**
    - OpenPBR subsurface runs as MaterialX's `mx_subsurface_scattering_approx`: a curvature estimate per pixel over a Burley profile, and **no light moves between pixels** (read, MaterialX source).
    - So a scatter or thickness map would change Cycles and Unreal, and little in Storm.
  - **Blender:** Cycles has Random Walk (Skin), the library's B8. EEVEE's screen-space scatter takes only a scale per pixel (second-hand).
  - **Cost:** no per-map GPU cost is published. Epic's own ladder turns subsurface and the wrinkle maps off first at lower quality (read).

**Pros and cons** (the four options named at Pass 1, plus redness, which the survey adds):

| Option | For | Against |
|---|---|---|
| **A tone per part** (today) | No picture; works on any mesh; every tone is a measured value | The hard line at the lips and no variation (F-SKM-2) |
| **A colour map only, luminance × tone** (MAP-F4) | The industry's first map (F-SKM-11). No contract change (F-SKM-19). One map serves all six tones. Every renderer. | **No redness** (F-SKM-14). A photo source brings baked shading and the consent question (F-SKM-15). One atlas gives the face few pixels (F-SKM-12). |
| **A colour map with hue: one per tone, or colour plus a redness picture** | The half the lead found missing; MetaHuman's "accents"; the biophysical models | Per tone: six pictures per mesh version. A separate redness picture: a second mesh-supplied input, so a contract addition. |
| **The full set** (normal, roughness, cavity, scatter) | The industry's look at close range | Each is a new mesh-supplied input, so a contract addition. Scatter barely shows in Storm (F-SKM-18). The cost in Unreal. |
| **A scanned or bought set** | The best realism | No surveyed vendor's licence allows an open release; consent (F-SKM-15) |

## Pass 4 — Back in the repo: what a first map needs (measured 2026-10-14, at `867d5bd`)

- **F-SKM-19 — Today's skin articles cannot take a map yet.** This narrows F-SKM-3: there is still no contract change.
  - **The input is missing.** `Skin_FitzpatrickIV` does not declare `base_color_map`: its recipe has no `"base_color_map": true`, and the assembled `.mtlx` contains the input 0 times. Only `Eye_Natural` and `Hair_Natural` declare it today.
  - **The scatter colour would hide a map anyway.** The recipe pins `subsurface_color` to the tone at `subsurface_weight` 1.0. LCDSchema §Base colour map says that without a connected scatter colour *"the picture keeps only 1 − subsurface_weight of its strength"*, which is **none** at 1.0.
  - **The fix is the eye's.** Declare the map and drop the constant scatter colour. The assembler then connects the scatter colour to the base (`assemble_mtlx.py`, the F-P09-5 branch), so the skin scatters the picture's colour.
  - **Unreal's guard against a black scatter colour is already built** (`build_masters.py` `SUBSURFACE_FLOOR`, Learnings U11).
  - That is a re-assembly of the six skin articles: buildable, and not done here.
- **F-SKM-20 — The contract's "brightest ≈ 1" does not fit a skin map as it stands.**
  - **The two normalisations disagree.** LCDSchema normalises the picture so its brightest is ≈ 1 (written for hair strands). MAP-F4's skin layer is luminance ÷ its mean, which spans 0.46–1.48 (p5–p95).
  - **Normalised by its brightest, the average skin renders about a third darker** than the article's measured tone.
  - **Two ways out:**
    - scale the article's own colour up by the map's peak, so the average comes back to the measured tone;
    - or normalise the map to its mean, in a format that holds values above 1.

  A choice for the phase's discovery; neither is taken here.
- **F-SKM-21 — A map the library can make itself, with clean provenance** (a design sketch; no file targets).
  - **What it is built from:**
    - MPFB2's CC0 region masks (face, lips, ears, eyelids, nails, areolae; F-SKM-4);
    - the measured Fitzpatrick tones;
    - procedural variation, baked to an hm08 atlas.
  - **How it covers the gaps:**
    - redness and darkening by region give the cheeks, ears, knuckles, lips and sockets their colour **with hue** (F-SKM-14);
    - it can be made per tone at no cost in sources;
    - it is neutral at the groin by construction.
  - **Its precedent** is MPFB2's layered skin, which is mostly procedural.
  - **What it avoids:** no photograph, so no consent question (F-SKM-15) and no baked shading.
  - **Its quality is unproven**, which is what the probe below is for.

## A probe, when there is a machine for it

*(Widened 2026-10-14 by Passes 3–4. As first written, it compared today's Fitzpatrick IV skin with one MakeHuman atlas multiplied in by `base_color_map`, "through the existing input and no code change", at the face and hand views only. F-SKM-19 shows that the skin article needs re-assembling first.)*

**Render the rig's clothed character, at the face and hand views only:**
1. with today's Fitzpatrick IV skin;
2. with a probe copy of that article that takes a map (F-SKM-19), carrying one MakeHuman atlas by luminance (MAP-F4);
3. with the same copy carrying a quick library-made map (F-SKM-21).

**And measure** how many pixels hm08's face gets on a 2048² atlas (F-SKM-12).

**Run 2026-10-14 on the laptop, on the lead's word: Pass 5.**

It shows the lead, by eye, whether a colour map is worth it and whether a library-made map holds up against a photo. It was first offered at CM Pass 6 and never run. ~~**It waits for the library's permanent machine**~~ (`261014_R_MaterialPipeline.md` Pass 9: the lead, *"this is on my laptop right now"*). Running it on the laptop takes one sitting, if the lead would rather not wait.

## Pass 5 — The probe, run on the laptop (2026-10-14, at `f627ef3`)

**Run:** `261014_R_SkinMaps_probe.py`, committed beside this doc. Its four steps are in its header.
- **Scratch only:** everything it writes lands in the git-ignored `library/parity/SkinMapsProbe/`. The sheet is `SkinMapsProbe_sheet.jpg` there.
- **What it rendered:** Skin_FitzpatrickIV on the rig's clothed character, in three views (whole body, face, hand), in Storm, Blender (Cycles) and Unreal (`unreal-runtime-v4`).
- **The variants:**
  - **today:** the article as it is;
  - **photo:** a probe copy that takes a map, carrying MakeHuman's photo atlas by luminance. A comparison only (RD-SKM-2).
  - **made v1 and made v2:** the same copy carrying a colour map made from CC0 parts only (F-SKM-21):
    - MPFB2's region masks and its `sss.png` thickness map (blob-pinned, CC0 by MPFB2's `LICENSE.ASSETS.md`, read);
    - the measured tones;
    - an AO bake and 3D value noise from the mesh;
    - cheeks placed from the face's own 3D positions.
- **On the map variants:**
  - the Lips part wears the skin article and the map (F-SKM-9);
  - the body keeps hm08's atlas UVs, through a runtime patch of the rig, as the eye's picture does;
  - the pores are placed by `uv_scale` = 0.01 ÷ 1.534 = 0.0065.
- **Cost:** about 2.5 minutes per variant, all three tools at once. The photo run took 6 minutes in each tool, cause not looked into.

- **F-SKM-22 — A map removes the hard line at the lips, in all three tools.** With the Lips part on the skin article and the map, the lips' edge is the map's feathered edge, not the part's. Storm, Blender and Unreal move alike by eye on every view.
- **F-SKM-23 — Blender cannot yet render a tinted skin whose scatter follows its map.** `blender/masters/load_article.py` refuses it: *"a subsurface colour following a TINTED base is not mapped in Blender yet"* (F-P09-5; `Eye_Natural` has no tint port, so it never hit this).
  - Every skin article carries the Creator tint (`base_color_tint`), so **this is owed before any skin takes a map**. It joins F-SKM-19's re-assembly.
  - The probe dropped the tint port from its copies; the tint's default is white, so the look is unchanged.
- **F-SKM-24 — The photo atlas by luminance, rendered** (comparison only):
  - **the lips lose their colour** and go grey-beige: luminance carries no hue (F-SKM-14 confirmed by eye);
  - **the face reads lighter than today's tone:** the map is normalised to the whole body's mean, and the photo's face is brighter than its body;
  - **the photo's baked shading shows** in the eye sockets and around the mouth;
  - its fine detail (pores, blotches) is the richest of the variants;
  - detail p5/p50/p95 = 0.48 / 1.07 / 1.35; peak k = 1.70, so the article's colour was raised to (0.741, 0.386, 0.223) (F-SKM-20 in practice).
- **F-SKM-25 — The library-made map holds up once its average is held to the measured tone.**
  - **v1** (redness from thickness 0.55, ears 0.5, cheeks 0.6) **turned the whole body red**: the redness moved the skin's average, not only its regions.
  - **v2** halves the strengths and rescales the map so **the skin's average is the measured tone** per channel (lips excluded). The result:
    - the lips keep their colour and blend into the face with no line;
    - the cheeks, ears and fingertips are warmer;
    - the article's colour moves by under 7% (0.455, 0.241, 0.139 against the tone's 0.436, 0.227, 0.131).
  - **What it lacks next to the photo** is fine-scale detail: freckles, millimetre blotchiness, veins.
  - **The lesson for the phase:** a map's normalisation holds the measured tone as its average. This is F-SKM-20's rule, extended from brightness to colour.
- **F-SKM-26 — The face's share of a single hm08 atlas, measured.**
  - The face mask covers **194,717 texels at 2048²**, about a 441-pixel square. That is 6.7% of the UV area the body covers, and 4.6% of the atlas; 70% of the atlas is covered at all.
  - MetaHuman gives the face its own 2K–8K map (F-SKM-12), so close-ups will want a larger atlas, or a face map of its own **on the same mesh version**.
- **F-SKM-27 — The P18 stopgap works with a map on one UV set.** The map sat on hm08's atlas UVs and the pores at `uv_scale` 0.0065, in all three tools, as F-SKM-13 predicted.

## Pass 6 — The AI route, explored (web only, 2026-10-14; RD-SKM-2)

**Examined:** one web sweep, given RD-SKM-2 to RD-SKM-4, RD-MP-1, RD-MP-8, F-MP-18 and F-MP-19 verbatim. It covered:
- mesh-texturing generators;
- human-skin generators;
- image models guided in UV space;
- de-lighting;
- copyright and provenance.

The sourcing marks are Pass 3's.

- **F-SKM-28 — Few generators keep a mesh's own UVs, and each comes with a catch:**
  - **Meshy's retexture** keeps them on request (`enable_original_uv`, read) and returns colour (and a PBR set) at up to 8K. It is a cloud service.
    - On the free plan, Meshy **owns the output** and releases it CC BY 4.0 with credit to Meshy; that is not CC0.
    - Paid plans own their output *"to the extent possible under applicable law"* (read, terms of 2026-09-19).
    - It may train on non-Enterprise customers' inputs and outputs.
  - **Tripo** keeps them (second-hand).
  - **StableProjectorz** keeps them, runs locally, and its output licence follows the image model loaded (read).
  - **SyncMVD and Paint3D** keep them. Paint3D is guided by a position map in UV space and gives *"lighting-less"* output, but it is trained on Objaverse objects, not skin (read).
  - **Hunyuan3D-Paint 2.1 always re-unwraps** (its code calls `xatlas` unconditionally, read), which would lose hm08's layout. Its licence also **excludes the EU, the UK and South Korea** (read).
- **F-SKM-29 — No released human-skin generator draws onto an arbitrary layout such as hm08.**
  - **The human ones target templates the library cannot use:**
    - SMPL, whose licence is *"for the sole purpose of performing non-commercial scientific research"* (read): UVMap-ID, TexDreamer, SMPL-GPTexture;
    - face templates built from FFHQ's Flickr photos, with no consent statement (read).
  - **MetaHuman's synthesis** fits its own template and licence. Whether its textures may leave that licence as CC0 is not confirmed; its training data and consent are not published.
  - **A general method exists** (Paint3D's UV-position guidance; DirectUV, abstract only, 2026-09-28), but not for skin.
- **F-SKM-30 — The open route that fits the licences is a permissive image model guided in UV space.**
  - **The models:** FLUX.1 [schnell], Qwen-Image and Z-Image-Turbo are Apache-2.0 (read). They would be guided by hm08's own position and normal maps baked in UV space, which is Paint3D's mechanism and the same bake Pass 5 already makes.
  - **The known problems** (read, Paint3D):
    - seams where the UV islands are cut;
    - duplicated features;
    - lighting baked in by general models.
  - **None of these models documents its training data**, so F-MP-19's consent question applies to every general model: in a weaker form, since no one person's photo is used, but it is not answered.
  - **This laptop has an 8 GB RTX 2080** (measured). The mesh-texturing models need 16–24 GB, so **an AI probe belongs on the library service's GPU host** (RD-MP-12).
- **F-SKM-31 — Labelling AI output is now the norm.**
  - **Asset stores** (second-hand): Fab and Sketchfab require a *"CreatedWithAI"* tag.
  - **Poly Haven** (read, 2024-03-25): *"We won't make assets with AI"*, *"not some legal or moral stance"*.
  - **The EU AI Act's machine-readable marking** applies from 2026-08-02 (second-hand; its final timing is not confirmed).
  - **Copyright** (second-hand): the US position stands since *Thaler* (cert denied 2026-03-02), and prompts alone are not authorship. Creative Commons recommends CC0 for such output.
  - **For the library:** F-MP-14/18's origin field covers it, with *AI-assisted* as a value and the model named.
- **F-SKM-32 — The two routes combine where each is weak** (a design sketch).
  - **The library-made map holds the colour right but lacks fine detail** (F-SKM-25).
  - **AI output is rich in fine detail but uncertain in colour, lighting and provenance.**
  - **So:** keep the library-made map as the colour (the measured tone as its average, the regions by design), and take from a generator **only a tone-free fine-detail layer** (freckles, millimetre mottling) normalised to an average of 1, MAP-F4's way. The generator then cannot move the tone, the lips or the groin (RD-SKM-4).
  - **A procedural detail layer is the non-AI alternative for the same slot.**

## Resolved

- **RD-SKM-1 — MAP-RD2 means one approved human mesh, and skin maps are made per mesh version** (the lead, 2026-10-14, Pass 2: *"it is more about locking mesh then it is about materials"*).
  - The approved mesh is MakeHuman's hm08 body on the Manny skeleton (F-SKM-8).
  - Any skin map made for it serves every character built from it, whatever its shape, skeleton or weights.
  - A future mesh gets its own skin-map spec, and the meshes that keep its topology use that version's maps.
  - In-place note on MAP-RD2 in `260929_R_CharacterMaps.md`. It answers Q-SKM-1, and it reopens neither MAP-RD2 nor CM2.
- **RD-SKM-2 — The first skin map is made by the library (F-SKM-21) or AI-generated, never taken from MakeHuman's photo atlases; the AI route is to be explored** (the lead, 2026-10-14: *"1b or c I want to explore that option"*). The photo atlases stay a probe comparison only, never published. Which of the two ships is open until the AI route is explored (Q-SKM-7). It answers Q-SKM-5.
- **RD-SKM-3 — One colour map per skin tone, carrying hue** (the lead, 2026-10-14: *"2b"*): six pictures per mesh version, one per Fitzpatrick article, through the existing `base_color_map`, with no new input. It answers Q-SKM-6.
- **RD-SKM-4 — The library's map is neutral at the genitals and groin** (the lead, 2026-10-14: *"3 yes"*): plain skin there. The areolae keep their natural colour variation, with a one-line context note where the fit set says what it holds. Anatomy, if ever, is a separate opt-in package outside this repo, and none is planned. It answers Q-SKM-2.
- **The probe runs on the laptop now** (the lead, 2026-10-14: *"run the probe on the laptop"*). It answers Q-SKM-3.
- **RD-SKM-5 — The library-made map ships first; AI joins later, only as a fine-detail layer on top of it** (the lead, 2026-10-14: *"a"*, to F-SKM-32's option). The AI layer is tone-free and normalised to an average of 1, so it cannot move the tone, the lips or the groin. It is probed on the library service's GPU. A fully AI-made map and a paid cloud service are not taken. It answers Q-SKM-7.
- **RD-SKM-6 — Skin maps get a spec that contributors can work from** (the lead, 2026-10-14: *"we need to start documenting a spec for this so other contributors can maybe also try thier hand at crafting these"*). Written as a **draft** spec in `docs/specs/Authoring/SkinMaps.md` by a lead-directed `/quick-fix`. It records the rulings as ruled, the probe's lessons as proposed, and the open questions as open; the phase's discovery hardens it.

## Open questions

| Id | Question | Recommendation |
|---|---|---|
| ~~Q-SKM-1~~ | ~~Does one skin map for the hm08 layout count as allowed under MAP-RD2?~~ | → **RD-SKM-1:** yes; MAP-RD2 is about locking the mesh. |
| ~~Q-SKM-2~~ → **RD-SKM-4** (neutral) | Is intimate anatomy in the map in scope for the library at all, or does the library's map leave those regions neutral? | **Neutral at the genitals and groin** (plain skin there), as every surveyed system's base body is (F-SKM-16). That is fine on every host (F-SKM-17). Anatomy, if ever, is a separate opt-in package outside this repo, and none is planned. The areolae keep their natural colour variation, with a one-line context note where the fit set says what it holds (GitHub's own advice, F-SKM-17). *(Recommendation updated 2026-10-14, Pass 3.)* |
| ~~Q-SKM-3~~ → run now, on the laptop (the lead, 2026-10-14) | Run the probe before discovery, or after? *(Was "before the survey, or after"; the survey ran 2026-10-14.)* | **Before discovery.** It settles "is a colour map worth it" and "does a library-made map hold up" by eye. It waits for the permanent machine unless the lead runs it on the laptop. |
| Q-SKM-4 | **How a mesh version is named and recorded**, so each skin map says which mesh it fits (the fit set's family folder, plus a version)? | A small contract question for the phase that builds the first map: the family is `makehuman` today, and hm08 is its first version. |
| ~~Q-SKM-5~~ → **RD-SKM-2** (b or c; explore c) | **Where the first map comes from** (F-SKM-15): (a) MakeHuman's CC0 photo atlases, whose licence is fine but which record no consent from the people photographed (against F-MP-19) and carry baked shading; (b) a map the library makes from CC0 region masks and its measured tones (F-SKM-21); (c) AI-generated, which is CC0 in form but has unknown training sources. | **(b) for what ships.** (a) only as the probe's comparison, never published. |
| ~~Q-SKM-6~~ → **RD-SKM-3** (b) | **Redness** (F-SKM-14): (a) a luminance map only, accepting no redness; (b) one colour map per tone, carrying hue (six pictures per mesh version, no new input); (c) one map plus a separate redness picture (a second mesh-supplied input, so a contract addition). | **(b), if Q-SKM-5 is (b):** a library-made map costs nothing more to make per tone, and needs no contract change. Revisit (c) if the full map set ever opens new inputs. |
| ~~Q-SKM-7~~ → **RD-SKM-5** (a) | **Which ships: the library-made map or an AI-generated one** (RD-SKM-2)? *(Explored 2026-10-14, Passes 5–6.)* | **The library-made map ships first.** It holds up once calibrated (F-SKM-25), every tool renders it, and its provenance is clean. **AI then joins as a fine-detail layer on top** (F-SKM-32), from an Apache-2.0 model guided in UV space and labelled AI-assisted. It is probed on the library service's GPU, not the 8 GB laptop (F-SKM-30). |

## Status

- **Passes captured:** 6 (2026-10-14):
  - Pass 1: what the repo holds;
  - Pass 2: the lead's clarification;
  - Pass 3: the industry survey, web only;
  - Pass 4: what a first map needs in this repo, measured;
  - Pass 5: the probe, run on the laptop;
  - Pass 6: the AI route, web only.
- **Ruled:**
  - **RD-SKM-1:** MAP-RD2 locks the mesh, not the pictures. Skin maps are made per mesh version; today's mesh is MakeHuman's hm08 on Manny. Nothing earlier is reversed except MAP-RD5's *"skin stays general"* (by RD-MP-9).
  - **RD-SKM-2 to RD-SKM-6** (2026-10-14):
    - the first map is library-made or AI-generated, never MakeHuman's photos;
    - one colour map per tone;
    - neutral at the genitals and groin;
    - **the library-made map ships first, with AI later only as a fine-detail layer;**
    - **a draft spec for contributors.**
  - The probe ran on the laptop.
- **Direction:** plan to move character skin to skin maps. Today's tone per part gives a hard line at the lips and no variation (F-SKM-2); with a map, the lips can wear the skin and the map's own lip colour (F-SKM-9).
- **Found:**
  - **The industry's first map is colour**; the library already has the tiling micro layer (`Skin_Pores`), on the same UVs as the industry uses (F-SKM-11, F-SKM-13).
  - **The colour map needs no contract change, but the six skin articles must be re-assembled** to take it (F-SKM-19). Its "brightest ≈ 1" normalisation darkens skin as it stands (F-SKM-20).
  - **A luminance map gives no redness.** The leading systems make tone per position, not by tinting one map (F-SKM-14).
  - **The only open-licence source on the approved mesh is MakeHuman's CC0 photo atlases, and no consent is recorded for them** (F-SKM-15). A library-made map from CC0 region masks avoids that (F-SKM-21).
  - **No surveyed base body carries genitals; a neutral map is fine on every host** (F-SKM-16, F-SKM-17).
  - a skin map is a fit-set picture, so it changes no part of CM2 (F-SKM-10).
  - **The probe (Pass 5):**
    - a map removes the hard line at the lips in all three tools (F-SKM-22);
    - the photo map loses the lips' colour (F-SKM-24);
    - the library-made map holds up once its average is held to the measured tone (F-SKM-25);
    - Blender cannot yet render a tinted skin whose scatter follows its map (F-SKM-23);
    - the face gets about a 441-pixel square of a 2048² atlas (F-SKM-26).
  - **The AI route (Pass 6):**
    - no human-skin generator fits hm08; Apache-2.0 image models guided in UV space could, untested (F-SKM-28 to F-SKM-30);
    - the two routes combine as library colour plus an AI fine-detail layer (F-SKM-32).
- **Unverified (second-hand only):**
  - Daz's and Character Creator's anatomy handling, and their layouts' resolutions;
  - MetaHuman's lack of anatomy;
  - EEVEE's scatter inputs;
  - the content of the US Copyright Office report;
  - any measured loss when moving maps between layouts.
- **Open:** Q-SKM-4, naming a mesh version (for the phase).
- **Durable doc (RD-SKM-6): landed** 2026-10-14 as the draft `docs/specs/Authoring/SkinMaps.md`, by a lead-directed `/quick-fix` (the `✅ Quick Fix — skin-map contributor spec` commit).
  - It marks each statement *Ruled*, *Proposed* or *Open*. The phase's discovery hardens the *Proposed* and *Open* ones.
  - Pointers: `_Docs_Index`, `_Architecture`, the Glossary's *Skin map* and the phase stub.
- **Seeded as phases:**
  - `PhaseTBD_SkinMaps.md` (2026-10-14, the lead: *"Seed all the TBD phases we discovered here"*). The survey it waited for is done.
  - `PhaseTBD_SkinMapsBeyondColour.md` (2026-10-14, the lead: *"Seed a phase TBD..."*, then *"Full skin map set"*): normal, roughness, cavity and scatter maps, each a new input. It follows *Skin Maps*.
- **Owed by the phase, found by the probe:**
  - re-assemble the six skin articles to take a map (F-SKM-19);
  - map a tinted, map-following scatter colour in Blender (F-SKM-23);
  - write the normalisation rule: the measured tone stays the average (F-SKM-20, F-SKM-25).
- **Next step:**
  1. `/discovery` on *Skin Maps*, when the lead opens it: it hardens the draft spec.
  2. The AI detail-layer probe, on the library service's GPU.
