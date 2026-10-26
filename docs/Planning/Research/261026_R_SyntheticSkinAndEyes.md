# Research — Synthetic skin and eyes: how the library should make real-looking skins, eyes and layers with no person in them

**Opened:** 2026-10-26 · **Mnemonic:** `SYN` (ids `F-SYN-n`, `RD-SYN-n`, `Q-SYN-n`) · **Mode:** research + a lead-directed test set (below). **Status:** see the Status footer.
**Requested by the lead,** on the Open Morphology Foundation's research `261026_R_SyntheticSkinAndEyeSets.md` (OMF `.ai/planning/research/`), verbatim: *"1) yes 2) yes 3) yes - run the spike... Could you add these tests directly to the Matter Library for us to test in the app?"*, then *"We can also infrom the matter library how it SHOULD be doing things moving forwrd.."*
**Builds on:** [`261014_R_SkinMaps.md`](261014_R_SkinMaps.md), [`../Phases/Complete/Phase21_SkinMaps.md`](../Phases/Complete/Phase21_SkinMaps.md), [`../../specs/Authoring/SkinMaps.md`](../../specs/Authoring/SkinMaps.md), [`../Phases/Future/PhaseTBD_SkinMapsBeyondColour.md`](../Phases/Future/PhaseTBD_SkinMapsBeyondColour.md), and the platform's character-quality research (`IMRSV_Platform_Documentation/Planning/Research/261025_Research_CharacterQuality.md`, *CHQ*). The OMF doc holds the survey (AI generation, procedural and biophysical synthesis, eyes, layer stacks) with its citations; this doc does not repeat it.

---

## Current picture (for the lead)

**The test set is in the library as drafts, to judge in Studio:**
- **15 synthetic skins.** Tones II, IV and VI, each in five layer sets:
  - `…_Clean_Synth_…` — the base, no marks;
  - `SynthFreckles`;
  - `SynthVeins`;
  - `SynthMarks` — moles, acne, post-acne marks, flushing;
  - `SynthAll`.
- **10 synthetic eyes.** Eight colourways (`Eye_Synth<Colour>_Clean_Base_…`) and two bloodshot ones (`Eye_SynthBrown_Bloodshot_…`, `Eye_SynthBlue_Bloodshot_…`).

None has a photograph or AI in it, and none touches a shipped article. To see them: pull, run `uv run tools/releases/serve_to_stage.py` (a new article needs one re-serve), and pick them in Studio's material window under Character › Skin and Character › Eyes.

**How the library should make skins from here on (proposed, Pass 3):**
- **Skin colour comes from pigment amounts, not paint.** Each texel gets melanin and blood amounts, and a skin model turns them into colour. One structure then gives each tone its own regional colour, which today's six identical maps can't (F-P21-10).
- **Maps are authored in 3D,** so there are no seams and features land on anatomy.
- **Marks are separate layers.**
- **The plastic look is fixed by roughness, normal and cavity maps.** That is *Skin Maps Beyond Colour*, which the lead un-parked today (RD-SYN-3).
- **Eyes get their colour in the shader,** from a few owned greyscale iris structures.

---

## Pass 1 — What the platform's spike and the library's rules settle (2026-10-26)

**Examined:** CHQ Passes 1–11; `SkinMaps.md`; `PhaseTBD_SkinMapsBeyondColour.md`; `LCDSchema.md` §overlays; the six skin recipes; the eye fit set.

- **F-SYN-1 — Colour alone moved the look most, and its source was a real person.**
  - CHQ's Digital Emily skin on the unchanged hm08 was the largest gain seen (the lead: *"WAY better"*).
  - It is research-only and can never ship, which is the reason for this work.
  - Today's maps are procedural region colour with nothing at skin scale. The six are byte-identical (F-P21-10), so the regional hue is the same at every tone.
- **F-SYN-2 — "Plastic" is the even shine, not the colour** (F-P21-1; CHQ F-CHQ-36: shine *strength* invisible). Its levers are roughness, cavity and a normal map. Each one is a new contract input.
- **F-SYN-3 — The library's overlays cannot carry a skin layer.** They are tiling data modulators at the article's scale (`LCDSchema.md` §render-role textures). A freckle field, a vein map or a scar sits on the body's layout. **Until a placed-layer mechanism exists, a layer is a separate article** (the test set does exactly this, through the six-token name's **Detail** token).
- **F-SYN-4 — The rulings the test set keeps:**
  - no photograph of a person (RD-SKM-2);
  - colour through `base_color_map` only (RD-SKM-3);
  - plain groin (RD-SKM-4);
  - the average held to the measured tone (RD-P21-3);
  - CC0 (RD-RO-2);
  - no AI in these maps (RD-SKM-5 and RD-SYN-1).

## Pass 2 — The test set: how it is made, and what it showed while being made (2026-10-26)

**Built:** `tools/converters/fit/gen_synth_skin.py`, `tools/converters/fit/gen_synth_eyes.py`, `tools/converters/fit/synth/chromophore_lut.json`, 25 draft recipes, their pictures and two provenance records (`fit/makehuman/synth_skin`, `fit/makehuman/synth_eyes`). Every picture was looked at during tuning (trial sheets in the git-ignored `library/parity/_synth_trial/`).

- **F-SYN-5 — The skin maker** (`gen_synth_skin.py`):
  1. **3D first.** It rasterises hm08's faces to give every texel its 3D position, normal and mesh concavity. This is numpy only: no Blender bake was available on the machine that built it. All noise is in 3D, so it has no UV seams. Body parts come from hm08's own joint helpers.
  2. **Two pigment fields:**
     - **Melanin:** sun exposure (face, neck, the backs of the hands and the forearms most; the trunk least), palms and soles low, creases slightly darker, multi-scale mottling down to ~1 mm.
     - **Blood:** cheeks, the nose, ears, fingertips, palms, knuckles, elbows and knees, blotchy at 1–15 mm.
     - Under the eyes the oxygen saturation is lower, which gives the bluish shadow.
  3. **The skin model.** A table from the Open Morphology Foundation's two-chromophore model (melanin × blood × oxygen → linear albedo; its header names the model version and commit). The model's gamut does not reach Fitzpatrick I/II or VI, so **it drives the change around each tone, and the library's own `calibrate` still holds the average to the measured tone.**
  4. **Lips** keep `LIP_RULE`. The model's lips run lilac on light skin, the same grey-lilac CHQ saw (F-CHQ-28).
- **F-SYN-6 — The layers, and what tuning taught:**
  - **Freckles** are *added* melanin in a clustered point process: denser on the nose and cheeks, shoulders, upper back and forearms; ~1 mm median. A *multiplied* freckle disappears on fair skin, which is where freckles show most.
  - **Veins** are grown as smooth walks over the surface along each limb: inner forearms, the backs of the hands and feet, temples, chest, behind the knee.
    - **The pigment model alone draws them orange.** It is one layer with no depth, so more blood only absorbs more blue.
    - A vein reads blue-green because red light reaches it and blue doesn't. So the vein darkens each channel by that channel's scatter depth, taken from the article's own `subsurface_radius_scale`.
    - The first walks were wormy and hard-edged. Real superficial veins are long, gently curving and soft.
  - **Marks:**
    - moles (sparse, densest on the back and arms);
    - acne on the T-zone, cheeks, chin and upper back (60 % red papules, the rest healed brown marks);
    - flushed nose and cheeks.
- **F-SYN-7 — The eye maker** (`gen_synth_eyes.py`):
  - It draws on the fit set's layout, measured from `Brown_basecolor_sUKN.png`: pupil edge 30 px, limbus 116 px, the white to 268 px at 1024.
  - The iris is built in layers, as an ocularist paints one (Lefohn et al. 2003): stroma, wavy clumped radial fibres, crypts, a wavy collarette with its own inner colour, broken contraction furrows, a soft limbal ring, the pupil ruff.
  - Light irises are fibrous and brown ones smooth (Bérard et al. 2016). The light irises' colour is a pale scattering stroma (Lam & Baranoski 2006), so their fibres are the lightest part.
  - The white is warm, pinker toward the hidden edge, with vessels grown inward that fade before the iris. *Bloodshot* has more, thicker, redder vessels near the iris over a pink flush.
- **F-SYN-8 — What the set cannot show, by construction:**
  - **No shine, relief or pores beyond the tiled `Skin_Pores`.** The plastic look stays until *Beyond Colour* (F-SYN-2).
  - **2048² atlas only.** The face still gets ~441 px. CHQ measured a 4K face layout reachable with a face mesh of its own (F-CHQ-37).
  - **Lips:** Studio pairs the tone's own `Lips_Fitzpatrick*`, whose map is the shipped one. The lip edge may show a small step.
  - **Eyes:** no catch-light without CHQ's wet-dome eye geometry (a Stage generator change). The vessels' angles around the white are uniform, because the layout's orientation was not traced.
  - **Not rendered in any tool by the session that built them.** That machine has no Blender, USD toolchain or Unreal. **The first look is the lead's, in Studio.**

## Pass 3 — How the library should do it from here (proposed)

Each item is a candidate phase, unnumbered (seeded in `Roadmap.md`, Future).

1. **Synthetic Skin Sets — the pigment-map maker as the library's skin-map maker.**
   - `gen_synth_skin.py`'s approach replaces the colour recipe in `gen_skin_maps.py`, keeping its calibration.
   - **One structure, six tone-correct maps,** where today's six are one picture.
   - Add a **better skin model at the extremes.** Meta's BioSkin (MIT, pretrained RGB ↔ biophysical) is the candidate; the OMF model doesn't reach I/II/VI.
   - Add **several structure seeds**, so two characters of one tone don't share a face.
   - Later, **an AI detail layer:** close-up skin patches with no face, split into melanin and blood variation and kept only as a mean-1 multiplier. That is exactly RD-SKM-5's detail layer (RD-SYN-1).
2. ***Skin Maps Beyond Colour* — un-parked by the lead (RD-SYN-3).**
   - Roughness first (oily T-zone, drier cheeks), then a normal map for creases and wrinkles, then cavity, then thickness for ears and fingers.
   - The same 3D fields make them: the concavity is already computed, and the Open Morphology Foundation's statistics-anchored meso-detail generator gives pores and furrows by region.
   - This is the step that answers "still reads plastic".
3. **Skin Layers — marks as placed layers, not separate articles.**
   - A layer is **a mask on the body's layout + a pigment delta (melanin, blood, depth) + an amount**, made outside the app and kept as its own article.
   - A character names its stack, and the stack is baked into one texture set as a cache (CHQ Pass 5; the industry's model: MetaHuman, Character Creator SkinGen, Daz).
   - **Veins sit in the subsurface (depth) and freckles and makeup in the base colour,** as OpenPBR's own description of skin puts them.
   - **Wetness and sweat stay live,** on the coat, never baked.
4. **Eyes in the Shader.**
   - An iris article becomes **a greyscale structure picture** (4–6 owned ones: smooth "brown" and fibrous "blue" types).
   - **The colour is set in the master,** with MetaHuman-style controls: two colours and a blend, the limbal ring's size, softness and colour, saturation.
   - The white gets **a vein mask with a *Bloodshot* amount.**
   - Eight colourways then cost one picture each, not one per colour. The test set's pictures are the structures' first form.

**What stays the same:**
- the approved mesh and its layout (RD-SKM-1);
- one article carrying tone and map (RD-P21-1);
- the calibration (RD-P21-3);
- CC0, with no photograph of a person (RD-SKM-2, RD-RO-2).

## Resolved

- **RD-SYN-1 (the lead, 2026-10-26, "1) yes"):** AI makes **no whole skin map**. It may make the **tone-free detail layer** RD-SKM-5 describes, and content such as tattoo designs. A whole-face AI map is only ever a **judged comparison, never shipped**. *(The lead answered "yes" to the recommendation "not yet: AI for the detail layer and content, a whole-face AI map only as a comparison arm"; recorded as that reading.)*
- **RD-SYN-2 (2026-10-26, "2) yes … run the spike … add these tests directly to the Matter Library"):** the synthetic test set is built **into the library as drafts**, to be judged in Studio.
- **RD-SYN-3 (2026-10-26, "3) yes"):** ***Skin Maps Beyond Colour* is un-parked** (it was parked by RD-DS-8). Starting its discovery stays the lead's call.

## Status

- **Passes:** 3.
  - Pass 1: what is settled.
  - Pass 2: the test set and what tuning taught.
  - Pass 3: how the library should do it.
- **Built:**
  - the test set: 15 skins and 10 eyes, drafts;
  - two makers;
  - the pigment table and its provenance.
- **Not yet seen by anyone in a renderer.**
- **Owed:**
  - the lead's look in Studio. The skins are best judged beside `Skin_Fitzpatrick<tone>_Clean_Base` and, for the bar, beside CHQ's `CHQ_EmilySkin`. The eyes beside `Eye_Green`, ideally on CHQ's wet-dome eye.
  - The AI detail layer and the whole-face comparison need a GPU machine (not this one).
- **▶ Next, after the lead's look:**
  1. *Beyond Colour* discovery (RD-SYN-3);
  2. tune the set from the lead's notes;
  3. pick which of Pass 3's phases go next.
