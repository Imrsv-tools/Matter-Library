# Research — Skin maps: moving character skin from a tone per part to painted maps

**Opened:** 2026-10-14, seeded · **Mode:** research. It gathers and commits to nothing. **Mnemonic:** `SKM` (ids `F-SKM-n`, `Q-SKM-n`, `RD-SKM-n`).
**Requested by:** the lead, 2026-10-14, verbatim: *"I don't think this skintype per area of a mesh apprach is gong to yeild good results... Right now... it is pretty terrible in fact (the line between lips and face and no variation)... I think we need to plan to move to SkinMaps (if that is wht they are called)... feel free to seed a reseerach on this topic and we can dig in to what the industry is doing pros/cons"*.
**Altitude:** a **design** question: what character skin should be, and how the industry gets there. Pass 1 is what this repo already holds. **Pass 3, the industry survey, is not run yet** (Pass 2 is the lead's clarification of MAP-RD2); it is the next step, with the lead.
**Measured at:** `0474de4` (2026-10-14).

**Extends, does not replace:**
- `260927_R_CharacterMaterials_MPFB2.md` (CM2: substance in Matter, fit beside it; Pass 3's inventory of MakeHuman's skins);
- `260929_R_CharacterMaps.md` (MAP-RD1 to RD6; Passes 2–4: the atlases, what they carry, the replace-or-modulate probe);
- `261014_R_MaterialPipeline.md` (F-MP-35, Q-MP-6, now answered here).

**Words.** The industry's terms (to confirm in Pass 3):
- **skin map** or **skin texture** (the lead's word): the painted pictures of a character's skin;
- **atlas**: those pictures laid out on one body's **UV layout**, the mesh's flattened map;
- **micro detail**: a small tiling pattern (pores, fine wrinkles) laid over the atlas.

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

## Pass 3 — The industry survey (to run with the lead)

The questions, so the survey answers them and not others:

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

**Pros and cons to fill in at Pass 3:** the tone per part (today) · a colour map only (F-SKM-3: fastest, no contract change) · the full map set · a scanned or bought set.

## A probe, when there is a machine for it

**Render the rig's clothed character:**
- with today's Fitzpatrick IV skin;
- with one MakeHuman atlas multiplied in by `base_color_map`, through the existing input and no code change, at the face and hand views only.

It shows the lead the difference by eye. It was offered at CM Pass 6 and never run. **It waits for the library's permanent machine** (`261014_R_MaterialPipeline.md` Pass 9: the lead, *"this is on my laptop right now"*).

## Resolved

- **RD-SKM-1 — MAP-RD2 means one approved human mesh, and skin maps are made per mesh version** (the lead, 2026-10-14, Pass 2: *"it is more about locking mesh then it is about materials"*).
  - The approved mesh is MakeHuman's hm08 body on the Manny skeleton (F-SKM-8).
  - Any skin map made for it serves every character built from it, whatever its shape, skeleton or weights.
  - A future mesh gets its own skin-map spec, and the meshes that keep its topology use that version's maps.
  - In-place note on MAP-RD2 in `260929_R_CharacterMaps.md`. It answers Q-SKM-1, and it reopens neither MAP-RD2 nor CM2.

## Open questions

| Id | Question | Recommendation |
|---|---|---|
| ~~Q-SKM-1~~ | ~~Does one skin map for the hm08 layout count as allowed under MAP-RD2?~~ | → **RD-SKM-1:** yes; MAP-RD2 is about locking the mesh. |
| Q-SKM-2 | Is intimate anatomy in the map in scope for the library at all, or does the library's map leave those regions neutral? | After Pass 3 (survey question 6) and a check of the hosts' policies. |
| Q-SKM-3 | Run the probe above before the survey, or after? | Before, once a machine is ready: a picture settles "is it worth it" faster than a survey. |
| Q-SKM-4 | **How a mesh version is named and recorded**, so each skin map says which mesh it fits (the fit set's family folder, plus a version)? | A small contract question for the phase that builds the first map: the family is `makehuman` today, and hm08 is its first version. |

## Status

- **Passes captured:** 2 (2026-10-14): what the repo holds, then the lead's clarification. **Pass 3, the industry survey, is next, with the lead.**
- **Ruled:** RD-SKM-1. MAP-RD2 locks the mesh, not the pictures. Skin maps are made per mesh version; today's mesh is MakeHuman's hm08 on Manny. Nothing earlier is reversed except MAP-RD5's *"skin stays general"* (by RD-MP-9).
- **Direction:** plan to move character skin to skin maps. Today's tone per part gives a hard line at the lips and no variation (F-SKM-2); with a map, the lips can wear the skin and the map's own lip colour (F-SKM-9).
- **Found:**
  - the colour half needs no contract change: `base_color_map` on Subsurface exists (F-SKM-3);
  - the sources are on hand (F-SKM-4);
  - a skin map is a fit-set picture, so it changes no part of CM2 (F-SKM-10);
  - it brings in the publishing guidance and host policies (F-SKM-6, Q-SKM-2).
- **Open:** Q-SKM-2 to Q-SKM-4.
- **Next step:** Pass 3, the survey; the probe when the library's machine exists.
