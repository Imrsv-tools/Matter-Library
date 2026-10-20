# Skin Maps — what a contributed skin map is, and how to make one

> **⚠ DRAFT (planned, 2026-10-14).** No skin map ships yet, and nothing below is built except the probe. This draft exists so contributors can try their hand now (the lead, 2026-10-14: *"we need to start documenting a spec for this so other contributors can maybe also try thier hand at crafting these"*, RD-SKM-6). The *Skin Maps* phase hardens it ([`Phase21_SkinMaps.md`](../../Planning/Phases/Phase21_SkinMaps.md)). Until then, the authority is the research's `## Resolved` ([`261014_R_SkinMaps.md`](../../Planning/Research/261014_R_SkinMaps.md)).
>
> **Three marks are used here, and they mean different things:**
> - **Ruled:** the lead has decided it. It changes only by a new ruling.
> - **Proposed:** what the probe taught. The phase confirms or changes it.
> - **Open:** not decided. Ask before you rely on it.

## What a skin map is

A **skin map** is a painted picture of a body's skin, drawn on the approved human mesh's UV layout ([Glossary](../../Glossary.md) *Skin map*, *Approved human mesh*). It gives skin the variation a single tone cannot: lips that blend into the face, warmer cheeks, ears and fingertips, and darker creases.

- **It is a picture of the MESH, not part of the material.** The skin **article** (`Skin_FitzpatrickI` … `VI`) keeps the substance: its measured tone, scatter, coat, fuzz and the tiling pores (`Skin_Pores`). ~~The map is a **fit-set** picture, supplied when the article is bound, as the eye's and the hairstyle's pictures are (CM2). **Ruled** (F-SKM-10).~~ *(Corrected 2026-10-15, Phase18 F-P18-1: F-SKM-10 was a finding written within CM2's frame, never a ruling, and the lead has since ruled the other way.)* **The map lives in its own Character skin article**, as that article's `base_color_map` value, and the article declares the mesh it `fits` (`MakeHuman_Body_v01`); a binding that supplies a picture still wins ([LCDSchema §Base colour map](../Contract/LCDSchema.md#base-colour-map-the-meshs-picture-supplied-at-binding)). **Ruled** (RD-P18-9, the lead, 2026-10-15). Whether one article carries both the tone and its map, or the map is an article of its own beside the tone, is *Skin Maps*' to settle: **Open**.
- **It reaches every renderer through the existing input**, `base_color_map`: `base = base_color_const × base_color_map × base_color_tint`. There is no new input for colour. **Ruled** (RD-SKM-3).
- **It is colour only, for now.** Maps for normal, roughness, cavity or scatter would each need a new input. *(planned: the phase* Skin Maps Beyond Colour*, [`PhaseTBD_SkinMapsBeyondColour.md`](../../Planning/Phases/Future/PhaseTBD_SkinMapsBeyondColour.md), seeded 2026-10-14)*

## Which mesh it fits — **Ruled** (RD-SKM-1)

- **The approved human mesh is MakeHuman's hm08 body** (CC0), rigged to the Manny skeleton.
- **A map made for it fits every character built from it**, whatever its shape, skeleton or weights, because those leave the UV layout where it is.
- **A future mesh version gets its own skin maps.** A map can be moved to a new layout by baking, with some loss.
- **How a mesh version is named and recorded, so each map says which mesh it fits:** ~~**Open** (Q-SKM-4).~~ **Answered 2026-10-15 (Phase18, RD-P18-1):** a mesh version is a UV layout, named `<Family>_<Mesh>_vNN` and pinned by its layout hash in `tools/converters/groups.py` (`PART_MESHES`). hm08 is **`MakeHuman_Body_v01`**, at 2048 × 2048; a map declares it as `fits`, and the recipe gate (G8) checks the map against it. Its kit is `kit__MakeHuman_Body_v01.zip` ([Glossary](../../Glossary.md) *Part mesh*).

## One map per skin tone — **Ruled** (RD-SKM-3)

**Six maps per mesh version, one for each Fitzpatrick article (I to VI), each carrying its own hue.** One neutral map recoloured by tone cannot make cheeks and lips *redder*, because a brightness-only map carries no hue (F-SKM-14, F-SKM-24).

## What the map must and must not show

| Region | Rule | Mark |
|---|---|---|
| **Genitals and groin** | **Plain skin**: the tone, with no anatomical detail. | **Ruled** (RD-SKM-4) |
| **Areolae** | Natural colour variation, as on the rest of the body. | **Ruled** (RD-SKM-4) |
| **Lips** | The lip colour, with a **feathered** edge into the face, never a hard line. The character's Lips part wears the skin article and the map. | **Proposed** (F-SKM-9, F-SKM-22) |
| **Cheeks, ears, nose, fingertips** | Warmer, because blood shows through thin or flushed skin. | **Proposed** (F-SKM-14, F-SKM-25) |
| **Creases and eye sockets** | Slightly darker. | **Proposed** (F-SKM-25) |
| **Nails** | Not the map's job: the nails are their own part, bound to a nail article. | **Proposed** |
| **Anywhere** | **No lighting or shading baked in**, and no hair, make-up, tattoos or likeness of a real person. | **Proposed** (F-SKM-24: baked shading showed in the probe) |

**Anatomical detail, if it is ever wanted, is a separate opt-in package outside this repo, and none is planned** (RD-SKM-4).

## The picture's format — **Proposed** unless marked

- **Layout:** hm08's single 0–1 UV atlas, with at least **16 pixels of bleed** past each UV island's edge, as the probe baked.
- **Size:** **2048 × 2048** (MakeHuman's atlases and the probe). At that size the face gets about a 441-pixel square (F-SKM-26). Whether close-ups need a larger atlas, or a face map of its own: **Open**.
- **File:** an RGB **PNG**, read as **sRGB** (`srgb_texture`, as every `base_color_map` is: LCDSchema).
- **Where it lives:** the fit set, beside the eyes, e.g. `MatterLibrary/textures/fit/makehuman/skin/FitzpatrickIV_basecolor_sUKN.png`, scale tag `sUKN` (the fit set's tag). ~~The exact path waits on the mesh-version naming: **Open** (Q-SKM-4).~~ *(2026-10-15: the naming is answered, and the picture is named by its article as its `base_color_map` value (RD-P18-9); its folder stays `MatterLibrary/textures/fit/makehuman/skin/`, as the fitted teeth's is `…/teeth/`.)*

## Calibration: the measured tone stays the average — **Proposed** (F-SKM-20, F-SKM-25)

The probe's main lesson. Its first library-made map turned the whole body red, because its redness moved the skin's **average**, not only its regions.

1. **Paint, or generate, the absolute skin colour** for one tone, with its regions as above.
2. **Hold the average.** Over the skin, lips excluded, the picture's average colour must equal the article's measured tone, per channel. That is the article's `base_color_const` (from Physically Based), e.g. `0.436, 0.227, 0.131` for Fitzpatrick IV.
3. **Store it as a multiplier.** The stored map is the picture divided by the tone, scaled so its brightest value is 1. The article's own colour is raised by the same factor, so the product is unchanged. The library's fit converter (`tools/converters/fit/`) should do this step, so a contributor hands in the colour picture. *(planned)*

## Sources and licence

- **Licence:** CC0-1.0 by default; CC BY 4.0 is allowed, recorded per map. **Ruled** (RD-MP-8, RD-MP-1). *`CONTRIBUTING.md` still lists CC BY as not accepted; the* Two Licences *phase conforms it. Drift (2026-10-14).*
- **No photographs or scans of real people** unless their rights **and consent** are documented. **MakeHuman's photo atlases are excluded**, although they are CC0, because no consent is recorded for them. **Ruled** (RD-SKM-2; F-SKM-15).
  - Note that `CONTRIBUTING.md`'s *"your own photographs or scans ✅"* does not cover photographs of people for skin maps.
- **Made from parts you have the rights to: yes.** For example, the CC0 region masks and thickness map of MPFB2, measured tones, bakes from the mesh, procedural noise, or your own painting. **Ruled** (RD-SKM-2, RD-SKM-5).
- **AI: only as a fine-detail layer, and not yet.** A generator may later supply a **tone-free** detail layer (freckles, fine mottling), normalised to an average of 1, on top of a library-made map. It cannot change the tone, the lips or the groin. A **fully AI-made map is not accepted**. **Ruled** (RD-SKM-5). The detail layer's format is *(planned)*.
  - The model must allow CC0 output; the Apache-2.0 image models do (F-SKM-30).
  - The origin is recorded as *AI-assisted*, with the model named (F-MP-18).
- **Record the provenance of every input:** each mask, script and source, with its URL and hash, as for any texture ([AuthoringGoldenPath](AuthoringGoldenPath.md)).

## How to try one today

Until the phase builds the real path, the probe is the way to see a map on the character in Storm, Blender and Unreal side by side. It is `docs/Planning/Research/261014_R_SkinMaps_probe.py`; its header lists the four commands.

- **What it does:** it builds a library-made map for Fitzpatrick IV from the CC0 parts above, and renders the rig's clothed character at the face, hand and whole-body views. Everything it writes stays in the git-ignored `library/parity/SkinMapsProbe/`.
- **To try your own picture:**
  1. Store it as a multiplier (calibration step 3 above) in place of `made_basecolor.png` there.
  2. Set `made.base_color_const` in that folder's `maps.json` to the tone times your factor.
  3. Run the probe's `articles`, `render … made` and `sheet` steps.

**What "good" looks like (Proposed):**
- the lips blend into the face with no line;
- the skin's overall tone matches today's;
- no UV seams show at the face or hand views;
- Storm, Blender and Unreal move alike.

The probe's sheet is a diagnostic. Published pictures of skin show the face and hand on the clothed character only (`261014_R_MaterialPipeline.md` RD-MP-3, F-MP-17).

## What must be built before a map can ship *(planned)*

1. **Re-assemble the six skin articles to take a map.** Today they do not declare `base_color_map`, and their fixed scatter colour at full weight would hide one (F-SKM-19).
2. **Blender: render a tinted skin whose scatter follows its map.** `blender/masters/load_article.py` refuses it today (F-SKM-23).
3. **The calibration step** in the fit converter (above).
4. **The mesh-version naming** (Q-SKM-4).

## History

- 2026-10-14 — drafted from the research's Passes 1–6 and rulings RD-SKM-1 to RD-SKM-6 (lead-directed quick fix, RD-SKM-6).
