# Skin Maps — what a contributed skin map is, and how to make one

> **IN FORCE (2026-10-20, Phase21 *Skin Maps*, [`Phase21_SkinMaps.md`](../../Planning/Phases/Complete/Phase21_SkinMaps.md)).** Six skin maps ship, one per Fitzpatrick tone, on `MakeHuman_Body_v01`, carried by the six `Skin_Fitzpatrick*` articles and the six `Lips_Fitzpatrick*`. The lead judged them on the character in Blender, Storm and Unreal (*"lips blend, cheeks warmer"*; *"each tone reads as its own, tools move alike"*). *Was:* a draft (2026-10-14), written so contributors could try their hand early (the lead: *"we need to start documenting a spec for this so other contributors can maybe also try thier hand at crafting these"*, RD-SKM-6). The research's `## Resolved` ([`261014_R_SkinMaps.md`](../../Planning/Research/261014_R_SkinMaps.md)) is the history behind each rule.
>
> **The marks used here:**
> - **Ruled:** the lead has decided it. It changes only by a new ruling.
> - **In force:** built by Phase21 and seen by the lead at its sittings. *(These were* Proposed *in the draft: what the probe taught.)*
> - **Open:** not decided. Ask before you rely on it.

## What a skin map is

A **skin map** is a painted picture of a body's skin, drawn on the approved human mesh's UV layout ([Glossary](../../Glossary.md) *Skin map*, *Approved human mesh*). It gives skin the variation a single tone cannot: lips that blend into the face, warmer cheeks, ears and fingertips, and darker creases.

- **It is a picture of the MESH, not part of the material.** The skin **article** (`Skin_FitzpatrickI` … `VI`) keeps the substance: its measured tone, scatter, ~~coat,~~ fuzz and the tiling pores (`Skin_Pores`). *(2026-10-27, Phase22 RD-P22-17: a skin wearing the shine maps carries **no coat**: on the relief it laid a wet glint over the whole body, and the skin's oil is the roughness map's. Fitzpatrick IV first; all six since 22.4.)* ~~The map is a **fit-set** picture, supplied when the article is bound, as the eye's and the hairstyle's pictures are (CM2). **Ruled** (F-SKM-10).~~ *(Corrected 2026-10-15, Phase18 F-P18-1: F-SKM-10 was a finding written within CM2's frame, never a ruling, and the lead has since ruled the other way.)* **The map lives in its own Character skin article**, as that article's `base_color_map` value, and the article declares the mesh it `fits` (`MakeHuman_Body_v01`); a binding that supplies a picture still wins ([LCDSchema §Base colour map](../Contract/LCDSchema.md#base-colour-map-the-meshs-picture-supplied-at-binding)). **Ruled** (RD-P18-9, the lead, 2026-10-15). ~~Whether one article carries both the tone and its map, or the map is an article of its own beside the tone, is *Skin Maps*' to settle: **Open**.~~ **One article carries both the tone and its map** (RD-P21-1, Phase21, 2026-10-20): each `Skin_Fitzpatrick*` is a fitted article, so every body built from the approved mesh wears the map, and Studio and the website list six skins, not twelve. **Using the tone on another mesh is kept:** a binding that supplies a white picture wins over the article's own (the Carrier rule), so a consumer can still bind the tone alone.
- **It reaches every renderer through the existing input**, `base_color_map`: `base = base_color_const × base_color_map × base_color_tint`. There is no new input for colour. **Ruled** (RD-SKM-3).
- ~~**It is colour only, for now.** Maps for normal, roughness, cavity or scatter would each need a new input.~~ *(2026-10-27, Phase22: four **shine maps** now ride beside the colour map, each through a new input: [§Shine maps](#shine-maps-the-skins-surface-beyond-colour-phase22-2026-10-27) below.)* *(Was planned: the phase* Skin Maps Beyond Colour*, [`Phase22_SkinMapsBeyondColour.md`](../../Planning/Phases/Phase22_SkinMapsBeyondColour.md), seeded 2026-10-14, numbered Phase22 2026-10-27; kept parked by RD-P21-6; **un-parked by the lead 2026-10-26**, RD-SYN-3 in [`261026_R_SyntheticSkinAndEyes.md`](../../Planning/Research/261026_R_SyntheticSkinAndEyes.md). A colour map does not take away skin's plastic look: Phase21 measured the even sheen as the cause (F-P21-1), and the lead, on the mapped skin: "still reads plastic". The roughness map comes first there.)*

## Which mesh it fits — **Ruled** (RD-SKM-1)

- **The approved human mesh is MakeHuman's hm08 body** (CC0), rigged to the Manny skeleton.
- **A map made for it fits every character built from it**, whatever its shape, skeleton or weights, because those leave the UV layout where it is.
- **A future mesh version gets its own skin maps.** A map can be moved to a new layout by baking, with some loss. **The library's own maps are instead re-made from their source on the body,** one bake per layout ([below](#authored-on-the-body-baked-per-layout--ruled-2026-10-26)). *(2026-10-26: a next mesh version is now expected, a denser render body with its own UV layout, riding an hm08-class cage: [`261026_R_CharacterTestBenchInputs.md`](../../Planning/Research/261026_R_CharacterTestBenchInputs.md) CTB-7.)*
- **How a mesh version is named and recorded, so each map says which mesh it fits:** ~~**Open** (Q-SKM-4).~~ **Answered 2026-10-15 (Phase18, RD-P18-1):** a mesh version is a UV layout, named `<Family>_<Mesh>_vNN` and pinned by its layout hash in `tools/converters/groups.py` (`PART_MESHES`). hm08 is **`MakeHuman_Body_v01`**, at 2048 × 2048; a map declares it as `fits`, and the recipe gate (G8) checks the map against it. Its kit is `kit__MakeHuman_Body_v01.zip` ([Glossary](../../Glossary.md) *Part mesh*).

## Authored on the body, baked per layout — **Ruled** (2026-10-26)

**The library makes a skin map on the body, in 3D, and treats each UV-layout picture as a bake of it: a cache, one per mesh version.** Every texel's colour comes from where it sits on the body: its 3D position and normal, the body's anatomy, noise in 3D. **No map the library makes is painted directly in a UV layout.** *(The lead, 2026-10-26, "yes" to "make 'author skins in 3D or on the cage, bake per UV layout' a Matter Library rule now?"; recorded in [`261026_R_CharacterTestBenchInputs.md`](../../Planning/Research/261026_R_CharacterTestBenchInputs.md) §Resolved.)*

- **Why:** a new mesh version then costs a re-run of the maker, not a re-paint. Moving a finished picture from one layout to another loses detail.
- **Where the makers stand.** `gen_skin_maps.py` and the test set's `gen_synth_skin.py` both compute in 3D. **But both still read six pictures drawn on hm08's atlas:** MPFB2's face, lips, ears, eyelids and areolae masks, and its thickness map (`sss.png`). **Todo (2026-10-26):** carry those onto the body (for example as values per hm08 vertex) before the next mesh version's maps are made (CTB-5).
- **A contributor's picture painted on hm08's atlas is still accepted, bound to its layout.** It fits `MakeHuman_Body_v01` only and is not carried to the next mesh version (§How to make one). **Ruled** (the lead's go on this recommendation, 2026-10-26: the research doc's Q-CTB-5).

## One map per skin tone — **Ruled** (RD-SKM-3)

**Six maps per mesh version, one for each Fitzpatrick article (I to VI), each carrying its own hue.** One neutral map recoloured by tone cannot make cheeks and lips *redder*, because a brightness-only map carries no hue (F-SKM-14, F-SKM-24).

## Shine maps: the skin's surface, beyond colour (Phase22, 2026-10-27)

**The colour map does not take away skin's plastic look; the even sheen did that** (F-P21-1). Four more pictures on the same atlas describe the skin's **surface**: where it is oilier or drier, its relief, the shine lost in its creases, and where light passes through it. Built by Phase22 *Skin Maps Beyond Colour* ([`Phase22_SkinMapsBeyondColour.md`](../../Planning/Phases/Phase22_SkinMapsBeyondColour.md)); the lead's verdicts at its sittings are in that doc. The inputs and their formulas are the contract's: [LCDSchema §Shine maps](../Contract/LCDSchema.md#shine-maps-the-meshs-surface-a-fitted-article-carries).

- **One set for every tone** (RD-P22-2): they describe the surface, not the tone, so they carry no hue and are named by what they are (`Skin_roughness`, not `FitzpatrickIV_roughness`). A contributor can still give one tone its own map by pointing that article's recipe (`<name>_map_tex`) at another file.
- **Linear data, never colour:** each is read as raw numbers, and its neutral value draws the skin as it was before the map (so a consumer that does not read it loses nothing).
- **The skin wearing them carries no coat** (RD-P22-17): the oil is the roughness map's.

| Map (input) | What it carries | Neutral value |
|---|---|---|
| **Roughness** (`roughness_map`) | An offset on the pores' roughness: **oilier, so glossier, on the forehead, nose and chin; drier on the cheeks**, with a few-millimetre grain so the highlight breaks up, and drier grooves. **Its average over the skin is held at 0.62** (RD-P22-17), so the skin sits as rough as measured skin; that average sets the skin's overall shine. Neutral on the lips. | 0.5 (grey 128) |
| **Relief** (`normal_map`) | A tangent-space normal, **+Y up** (MaterialX's convention; MikkTSpace-compatible tangents from the mesh's UVs), at the scale the atlas carries: the furrow network between the skin's plateaus (larger cells on the hands and body than the face), the face's visible pores, and lines placed by anatomy (forehead, frown, crow's feet, under the eyes, nose to mouth, lips, neck, every finger joint). The tiling 1 cm `Skin_Pores` stays the finer layer, added to it. | flat (128, 128, 255) |
| **Cavity** (`cavity_map`) | Multiplies the shine (`specular_weight`): 1 on open skin, lower in the same furrows, pores and lines and in the mesh's own creases. It adds no colour: the colour map's creases are already darker. | white |
| **Scatter** (`scatter_map`) | Raises the scatter's reach where the body is thin, so **ears and fingertips glow when lit from behind**: the ears (thinnest at the rim, up to ×5), the last two finger joints (×2.2), the toes' tips; 0 elsewhere (RD-P22-18, RD-P22-19). *(The eyelids and the nose's wings are kept in the maker at 0: Blender drew them orange in front light on the darker tones, RD-P22-19.)* Unreal needs a light that casts shadows to show it; Storm barely moves with it. | black (×1) |

- **What they must not show:** the rules of [§What the map must and must not show](#what-the-map-must-and-must-not-show) hold for every shine map. **The groin is neutral in every one** (flat, no relief: RD-SKM-4). No lighting baked in.
- **The lips** wear the relief and cavity maps (so the relief runs across the lip edge) and keep their own roughness and coat (RD-P22-8). **The nails** wear none.
- **Format:** 2048 × 2048 PNG on hm08's atlas; **greyscale** for roughness, cavity and scatter, **RGB** for the normal; no alpha. G8 checks a shine map as data (its size, format, and the mesh it `fits`), with no coverage test: its neutral value is right on any island.
- **Where they live:** `MatterLibrary/textures/fit/makehuman/skin/Skin_{roughness,normal,cavity,scatter}_sUKN.png`.
- **Made in 3D** (the rule above): every texel's position and normal come from the mesh, the relief is a height field evaluated on the body, and the lines are placed from hm08's own joints, so nothing seams across a UV edge. CC0 parts only. One command makes all four and their provenance:

      uv run tools/converters/fit/gen_skin_shine.py                 # into the library
      uv run tools/converters/fit/gen_skin_shine.py --out /tmp/x    # a trial

  Then re-assemble the skins and lips (`uv run tools/converters/build_proof_subset.py <their recipe paths>`), see them in the look view (`uv run tools/parity/look.py <skin>`, a runtime that reads job format 4) and on the rig, and run the gate.
- **Not yet** *(planned)*: the pores faded at grazing angles and masked by region (a master change); wrinkles driven by expressions; a mark's own relief (*Skin Layers*). Each would ride these inputs.

## What the map must and must not show

| Region | Rule | Mark |
|---|---|---|
| **Genitals and groin** | **Plain skin**: the tone, with no anatomical detail. | **Ruled** (RD-SKM-4) |
| **Areolae** | Natural colour variation, as on the rest of the body. | **Ruled** (RD-SKM-4) |
| **Lips** | The lip colour, with a **feathered** edge into the face, never a hard line. ~~The character's Lips part wears the skin article and the map.~~ **The tone's `Lips_Fitzpatrick*` article carries the same map, with the lips' own finish** (roughness and coat), and the skin's calibrated colour, so the colour runs across the edge and the lips keep their shine (RD-P21-2; the lead: *"lips blend"*). | **In force** (F-SKM-9, F-SKM-22, RD-P21-2) |
| **Cheeks, ears, nose, fingertips** | Warmer, because blood shows through thin or flushed skin. | **In force** (F-SKM-14, F-SKM-25) |
| **Creases and eye sockets** | Slightly darker. | **In force** (F-SKM-25) |
| **Nails** | Not the map's job: the nails are their own part, bound to a nail article. | **In force** |
| **Anywhere** | **No lighting or shading baked in**, and no hair, make-up, tattoos or likeness of a real person. | **In force** (F-SKM-24: baked shading showed in the probe) |

**Anatomical detail, if it is ever wanted, is a separate opt-in package outside this repo, and none is planned** (RD-SKM-4).

## The picture's format — **In force** unless marked

- **Layout:** hm08's single 0–1 UV atlas, with at least **16 pixels of bleed** past each UV island's edge, as the probe baked. The recipe gate's G8 refuses a map that leaves any island of `MakeHuman_Body_v01` bare, the nails' and the inner mouth's included.
- **Size:** **2048 × 2048** (MakeHuman's atlases and the probe; RD-P21-5). At that size the face gets about a 441-pixel square (F-SKM-26). ~~Whether close-ups need a larger atlas, or a face map of its own: **Open**.~~ The atlas stays 2048² (RD-P21-5). A face map of its own, or a larger atlas, is a later question on the same mesh version *(planned)*.
- **File:** an RGB **PNG**, read as **sRGB** (`srgb_texture`, as every `base_color_map` is: LCDSchema). ⚠ **A USD writer that sets the picture on a bound Material authors `colorSpace = "srgb_texture"` on that asset value**, or Storm reads it raw and draws the skin washed out (F-P21-9; [Learnings Storm](../../Learnings/Storm/Storm.md) S10).
- **Where it lives:** the fit set, beside the eyes: `MatterLibrary/textures/fit/makehuman/skin/Fitzpatrick<Tone>_basecolor_sUKN.png`, scale tag `sUKN` (the fit set's tag). ~~The exact path waits on the mesh-version naming: **Open** (Q-SKM-4).~~ *(2026-10-15: the naming is answered, and the picture is named by its article as its `base_color_map` value (RD-P18-9); its folder stays `MatterLibrary/textures/fit/makehuman/skin/`, as the fitted teeth's is `…/teeth/`.)*
- **The pores still tile at 1 cm** on the fitted skin: the map samples the atlas directly, and the pores' layer rides it through `uv_scale = meters_per_tile ÷ the mesh's metres per UV unit` (0.006519 on hm08), which the binding sets (LCDSchema §Base colour map; the rig's `job.binding_set`).

## Calibration: the measured tone stays the average — **In force** (F-SKM-20, F-SKM-25, RD-P21-3)

The probe's main lesson. Its first library-made map turned the whole body red, because its redness moved the skin's **average**, not only its regions.

1. **Paint, or generate, the absolute skin colour** for one tone, with its regions as above.
2. **Hold the average.** Over the skin, lips excluded, the picture's average colour must equal the article's measured tone, per channel. That is the article's `base_color_const` (from Physically Based), e.g. `0.436, 0.227, 0.131` for Fitzpatrick IV.
3. **Store it as a multiplier.** The stored map is the picture divided by the tone, scaled so its brightest value is 1 (the 99.9th percentile per channel). The article's own colour is raised by the same factor, so the product is unchanged. ~~The library's fit converter (`tools/converters/fit/`) should do this step, so a contributor hands in the colour picture. *(planned)*~~ **The library's maker does this step** (`tools/converters/fit/gen_skin_maps.py`, below), so a contributor hands in the colour picture. It works the factor out from the map as stored (8-bit sRGB, decoded), so the average that renders is the tone to rounding. `fuzz_color` stays the tone, which is that average.

**Not a hidden map above 1** (RD-P21-3): a map normalised to its mean would need values above 1, which an 8-bit PNG cannot hold; raising the article's colour keeps the picture format unchanged.

**The library's six maps are one picture** (F-P21-10). Every term of the library's recipe multiplies the tone, so the map divided by the tone is identical for every tone: the six files are byte-identical, and Git LFS stores one. Each still carries hue (redder cheeks and lips), so one map per tone still holds (RD-SKM-3). **They are kept as six files, each named by its article, so a contributor can replace one tone's map on its own.**

## Sources and licence

- **Licence:** **CC0-1.0, and only CC0. Ruled** (RD-RO-2, the lead, 2026-10-14: *"material are CC0"*). A contributor's handle, when one is given, is carried as a courtesy. ~~CC0-1.0 by default; CC BY 4.0 is allowed, recorded per map. **Ruled** (RD-MP-8, RD-MP-1). *`CONTRIBUTING.md` still lists CC BY as not accepted; the* Two Licences *phase conforms it. Drift (2026-10-14).*~~ *(Corrected 2026-10-20, Phase21 F-P21-6: RD-RO-2 withdrew RD-MP-1 and the* Two Licences *phase the same day, so `CONTRIBUTING.md`, which refuses CC BY, was right.)*
- **No photographs or scans of real people** unless their rights **and consent** are documented. **MakeHuman's photo atlases are excluded**, although they are CC0, because no consent is recorded for them. **Ruled** (RD-SKM-2; F-SKM-15).
  - Note that `CONTRIBUTING.md`'s *"your own photographs or scans ✅"* does not cover photographs of people for skin maps.
- **Made from parts you have the rights to: yes.** For example, the CC0 region masks and thickness map of MPFB2, measured tones, bakes from the mesh, procedural noise, or your own painting. **Ruled** (RD-SKM-2, RD-SKM-5).
- **AI: only as a fine-detail layer, and not yet.** A generator may later supply a **tone-free** detail layer (freckles, fine mottling), normalised to an average of 1, on top of a library-made map. It cannot change the tone, the lips or the groin. A **fully AI-made map is not accepted**. **Ruled** (RD-SKM-5). The detail layer's format is *(planned)*.
  - The model must allow CC0 output; the Apache-2.0 image models do (F-SKM-30).
  - The origin is recorded as *AI-assisted*, with the model named (F-MP-18).
- **Record the provenance of every input:** each mask, script and source, with its URL and hash, as for any texture ([AuthoringGoldenPath](AuthoringGoldenPath.md)).

## How to make one

**The library's maps** are made by one command, which writes each map, its provenance (`library/provenance/sources/fit/makehuman/skin.yaml`) and each tone's raised `base_color_const`, and prints the measured averages:

    uv run tools/converters/fit/gen_skin_maps.py          # every tone
    uv run tools/converters/fit/gen_skin_maps.py IV       # one tone

**Your own picture**, painted (or made) as the absolute skin colour on hm08's atlas, under the rules above. It is bound to `MakeHuman_Body_v01` and is not carried to a later mesh version (§Authored on the body):

    uv run tools/converters/fit/gen_skin_maps.py IV --picture my_skin.png

It runs the calibration (steps 2 and 3) on your picture and writes it as that tone's map. Then:

1. Put the printed `base_color_const` into the tone's skin and lips recipes (`tools/converters/recipes/Skin_Fitzpatrick<Tone>_*.json`, `Lips_Fitzpatrick<Tone>_*.json`), and record your inputs' provenance.
2. Re-assemble them: `uv run tools/converters/build_proof_subset.py`.
3. See it on the character in Storm, Blender and Unreal side by side: `uv run tools/parity/rig.py --character Skin_Fitzpatrick<Tone>_Clean_Base_s001_v01`.
4. Run the gate: `uv run tools/validators/run_all.py` (G8 checks the map's size, format and every UV island).

### The probe *(superseded 2026-10-20 by the maker above; kept as the research record)*

Before Phase21 built the real path, the probe was the way to see a map on the character in Storm, Blender and Unreal side by side. It is `docs/Planning/Research/261014_R_SkinMaps_probe.py`; its header lists the four commands. The maker runs the probe's v2 recipe unchanged.

- **What it does:** it builds a library-made map for Fitzpatrick IV from the CC0 parts above, and renders the rig's clothed character at the face, hand and whole-body views. Everything it writes stays in the git-ignored `library/parity/SkinMapsProbe/`.
- **To try your own picture:**
  1. Store it as a multiplier (calibration step 3 above) in place of `made_basecolor.png` there.
  2. Set `made.base_color_const` in that folder's `maps.json` to the tone times your factor.
  3. Run the probe's `articles`, `render … made` and `sheet` steps.

**What "good" looks like (In force; the lead's Phase21 sittings judged these):**
- the lips blend into the face with no line;
- the skin's overall tone matches today's;
- no UV seams show at the face or hand views;
- Storm, Blender and Unreal move alike.

The probe's sheet is a diagnostic. Published pictures of skin show the face and hand on the clothed character only (`261014_R_MaterialPipeline.md` RD-MP-3, F-MP-17).

## What had to be built before a map could ship — **built** (Phase21, 2026-10-20)

1. ✅ **Re-assemble the six skin articles to take a map.** ~~Today they do not declare `base_color_map`, and their fixed scatter colour at full weight would hide one (F-SKM-19).~~ Each declares its map and `fits`, and its scatter colour follows the base (Phase21 21.1–21.2).
2. ✅ **Blender: render a tinted skin whose scatter follows its map.** ~~`blender/masters/load_article.py` refuses it today (F-SKM-23).~~ Lifted (21.1), so the Creator's tint works on skin. Unreal's master does the same (`subsurface_follows_base`), and it reaches a runtime once one is built on the machine with Unreal (`PlatformDependencies.md` M7).
3. ✅ **The calibration step:** `gen_skin_maps.py` (above).
4. ✅ **The mesh-version naming** (Q-SKM-4): answered by RD-P18-1 (2026-10-15).

## History

- 2026-10-14 — drafted from the research's Passes 1–6 and rulings RD-SKM-1 to RD-SKM-6 (lead-directed quick fix, RD-SKM-6).
- 2026-10-20 — in force (Phase21 21.3): the *Proposed* marks settled as built and seen; the article question answered (RD-P21-1), the lips (RD-P21-2), the calibration (RD-P21-3), the atlas size (RD-P21-5); the CC BY line corrected (F-P21-6); the six-maps-are-one finding (F-P21-10), Storm's colour space (F-P21-9), and how the maker is run.
- 2026-10-26 — *Authored on the body, baked per layout* (the lead's ruling on OMF's ask): the rule, the makers' six hm08-atlas inputs as a Todo, and a contributor's painted picture accepted as bound to its layout; *Beyond Colour* marked un-parked (lead-directed quick fix).
- 2026-10-27 — *Shine maps* (Phase22 22.4): the roughness, relief, cavity and scatter maps, one set for every tone, and the skin's coat dropped (RD-P22-17); *colour only, for now* struck.
