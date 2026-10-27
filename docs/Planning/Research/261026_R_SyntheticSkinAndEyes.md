# Research — Synthetic skin and eyes: how the library should make real-looking skins, eyes and layers with no person in them

**Opened:** 2026-10-26 · **Mnemonic:** `SYN` (ids `F-SYN-n`, `RD-SYN-n`, `Q-SYN-n`) · **Mode:** research + a lead-directed test set (below). **Status:** see the Status footer.
**Requested by the lead,** on the Open Morphology Foundation's research `261026_R_SyntheticSkinAndEyeSets.md` (OMF `.ai/planning/research/`), verbatim: *"1) yes 2) yes 3) yes - run the spike... Could you add these tests directly to the Matter Library for us to test in the app?"*, then *"We can also infrom the matter library how it SHOULD be doing things moving forwrd.."*
**Builds on:** [`261014_R_SkinMaps.md`](261014_R_SkinMaps.md), [`../Phases/Complete/Phase21_SkinMaps.md`](../Phases/Complete/Phase21_SkinMaps.md), [`../../specs/Authoring/SkinMaps.md`](../../specs/Authoring/SkinMaps.md), [`../Phases/Complete/Phase22_SkinMapsBeyondColour.md`](../Phases/Complete/Phase22_SkinMapsBeyondColour.md), and the platform's character-quality research (`IMRSV_Platform_Documentation/Planning/Research/261025_Research_CharacterQuality.md`, *CHQ*). The OMF doc holds the survey (AI generation, procedural and biophysical synthesis, eyes, layer stacks) with its citations; this doc does not repeat it.

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

**Rendered 2026-10-26 (Pass 4).** All 25 render alike in Storm and Unreal. The comparison pictures are beside this doc (`…_skins.jpg`, `…_eyes.jpg`), and the verdict rows wait for the lead's words. **On tone VI the layers barely show.** On the machine with Unreal they are served (re-served 2026-10-26), with no thumbnails yet.

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

## Pass 4 — The first look, prepared on the machine with Unreal (2026-10-26)

**Asked by the lead,** verbatim: *"There was lots of reserach today about the look of characters, skins etc including feedback from OMF and som test skins... can you look into this and lets prepare to share the tests that will come int"*. The bench side of the same ask is [`261026_R_CharacterTestBenchInputs.md`](261026_R_CharacterTestBenchInputs.md) Pass 2.

**Done:** every draft, plus the shipped skins and eye it is judged against, rendered on the rig's character in Storm and Unreal (`rig.py --character --no-blender`; Blender cannot render parity on this machine). 29 runs, all clean, about 40 s each.

**Two pictures, committed beside this doc** so a session on the other machine (which renders nothing) can see them after a pull:
- [`261026_R_SyntheticSkinAndEyes_skins.jpg`](261026_R_SyntheticSkinAndEyes_skins.jpg): tones II, IV and VI × the shipped base and the five layer sets. Face, then the hand and forearm (where the veins are).
- [`261026_R_SyntheticSkinAndEyes_eyes.jpg`](261026_R_SyntheticSkinAndEyes_eyes.jpg): per eye, the iris as drawn (its fit-set picture), then the eye rendered (a crop of the 512 px face view, enlarged and soft).
- Re-made by [`261026_R_SyntheticSkinAndEyes_look.py`](261026_R_SyntheticSkinAndEyes_look.py), whose doc string holds the render loop. **Each tuning round re-runs it,** so a round is compared with the last.

- **F-SYN-9 — The renderers agree on every draft as closely as on the shipped article it sits beside.** This is Storm against Unreal, ΔE2000 median over the bound part:
  - skins: II 2.3 whole body / 2.9 face; IV 2.1 / 2.5; VI 1.4 / 1.4. Each is within 0.1 of its tone's shipped base.
  - eyes: iris 0.8–2.1, white 2.6. The shipped `Eye_Green` is 1.5 / 2.4.
  - **No draft draws differently in the two tools.**
- **F-SYN-10 — What the pictures show** (the agent's reading, **not a verdict**; the lead's look decides):
  - **Base → Synth:** the synthetic base adds mottling and uneven regional colour. On II it reads slightly more sallow than the shipped base, whose cheeks are pinker.
  - **Freckles:** strong on II, clear on IV, nearly gone on VI, as designed (F-SYN-6).
  - **Veins:** soft grey-green walks on the inner forearm and the back of the hand, on II and IV. At the hand camera they read as veins, not lines.
  - **Marks:** moles and acne show on II and IV. One mole sits on the right brow in every Marks and All set.
  - **⚠ Tone VI: the five layer sets look almost alike.** Measured on the maps, VI's marks darken about as much *relatively* as II's (up to 39 % against 54 %, over the same ~0.1 % of the skin). On skin that dark the same relative change all but vanishes in the render. **Hypothesis for tuning:** post-acne marks are commonly *more* visible on dark skin, so VI's marks may want a stronger melanin delta, not the same one.
  - **Eyes:**
    - the colour families read as irises, and Hazel's brown collarette over green works;
    - the light irises (grey, blue, light blue) carry visible fibres;
    - DarkBrown is nearly featureless, flat and in the render;
    - the shipped Green is more fibrous than any synthetic one;
    - bloodshot shows as a pink inner corner on the blue eye and is faint on the brown.
  - In the render the lids clip every iris top and bottom, the shipped one too: that is the rig's eye, not the drafts.
- **F-SYN-11 — Studio cannot show them yet on this machine.**
  - The dev install's served catalog (rebuilt 17:37 the same day, before this session merged `4438c1f`) lists 108 articles and **none of the 25**; the checkout holds 133.
  - **One re-serve fixes it:** `uv run tools/releases/serve_to_stage.py`. It **restarts the Stage daemon**, so it waits for the lead's word: when checked, Stage was running and Studio was not.
  - **They will have no thumbnail in Studio's material window.** Thumbnails come from Cycles (`make_thumbnails.py`), which this machine cannot render. They come from the library machine, or from a published dev snapshot.
- **F-SYN-12 — The rig's character fails in Storm above 512 px on this machine.** `--width 1024` and `2048` both stop with OpenUSD's *"HdStVBOSimpleMemoryManager can't reassign ranges"*, on every eye tried; 512 works. So eyes are judged soft here, and **a close look at an iris is the lead's, in Studio**.

### The verdict rows (the batch row's two lines, as columns)

**Verdict** is the tools' agreement (F-SYN-9). **Review** takes the lead's words verbatim, with the date. A row judged on a bench body names the body. Compare each skin with its tone's `Skin_Fitzpatrick<tone>_Clean_Base` and, for the bar, CHQ's Emily skin. Compare each eye with `Eye_Green`.

| Article | Verdict | Review |
|---|---|---|
| `Skin_FitzpatrickII_Clean_Synth_s001_v01` | Storm = Unreal | — |
| `Skin_FitzpatrickII_Clean_SynthFreckles_s001_v01` | Storm = Unreal | 2026-10-26, round 1: *"the freckles on the face read really large and oddly placed"* → re-made in round 2 (Pass 5). Round 2, 2026-10-26: *"Yep... better"* |
| `Skin_FitzpatrickII_Clean_SynthVeins_s001_v01` | Storm = Unreal | 2026-10-26, round 1: *"The viens look plausable"* |
| `Skin_FitzpatrickII_Clean_SynthMarks_s001_v01` | Storm = Unreal | 2026-10-26, round 1: *"the marks look plausable (but lack any depth which I think is expected"* |
| `Skin_FitzpatrickII_Clean_SynthAll_s001_v01` | Storm = Unreal | round 1 judged by layer (the rows above); round 2: its freckles re-made, its veins and marks now exactly the single layers' |
| `Skin_FitzpatrickIV_Clean_Synth_s001_v01` | Storm = Unreal | — |
| `Skin_FitzpatrickIV_Clean_SynthFreckles_s001_v01` | Storm = Unreal | 2026-10-26, round 1: *"the freckles on the face read really large and oddly placed"* → re-made in round 2 (Pass 5). Round 2, 2026-10-26: *"Yep... better"* |
| `Skin_FitzpatrickIV_Clean_SynthVeins_s001_v01` | Storm = Unreal | 2026-10-26, round 1: *"The viens look plausable"* |
| `Skin_FitzpatrickIV_Clean_SynthMarks_s001_v01` | Storm = Unreal | 2026-10-26, round 1: *"the marks look plausable (but lack any depth which I think is expected"* |
| `Skin_FitzpatrickIV_Clean_SynthAll_s001_v01` | Storm = Unreal | round 1 judged by layer (the rows above); round 2: its freckles re-made, its veins and marks now exactly the single layers' |
| `Skin_FitzpatrickVI_Clean_Synth_s001_v01` | Storm = Unreal | — |
| `Skin_FitzpatrickVI_Clean_SynthFreckles_s001_v01` | Storm = Unreal; freckles near-invisible by design | 2026-10-26, round 1: *"the freckles on the face read really large and oddly placed"* → re-made in round 2 (Pass 5). Round 2, 2026-10-26: *"Yep... better"* |
| `Skin_FitzpatrickVI_Clean_SynthVeins_s001_v01` | Storm = Unreal | 2026-10-26, round 1: *"The viens look plausable"* |
| `Skin_FitzpatrickVI_Clean_SynthMarks_s001_v01` | Storm = Unreal; marks barely show (F-SYN-10) | 2026-10-26, round 1: *"the marks look plausable (but lack any depth which I think is expected"* |
| `Skin_FitzpatrickVI_Clean_SynthAll_s001_v01` | Storm = Unreal | round 1 judged by layer (the rows above); round 2: its freckles re-made, its veins and marks now exactly the single layers' |
| `Eye_SynthDarkBrown_Clean_Base_sUKN_v01` | Storm = Unreal | 2026-10-26, round 1: *"The eye all look quite bright to me...but maybe that is OK? hard to tell"* → whites warmed in round 3 (Pass 6). Round 3, 2026-10-26: *"better"* |
| `Eye_SynthBrown_Clean_Base_sUKN_v01` | Storm = Unreal | 2026-10-26, round 1: *"The eye all look quite bright to me...but maybe that is OK? hard to tell"* → whites warmed in round 3 (Pass 6). Round 3, 2026-10-26: *"better"* |
| `Eye_SynthAmber_Clean_Base_sUKN_v01` | Storm = Unreal | 2026-10-26, round 1: *"The eye all look quite bright to me...but maybe that is OK? hard to tell"* → whites warmed in round 3 (Pass 6). Round 3, 2026-10-26: *"better"* |
| `Eye_SynthHazel_Clean_Base_sUKN_v01` | Storm = Unreal | 2026-10-26, round 1: *"The eye all look quite bright to me...but maybe that is OK? hard to tell"* → whites warmed in round 3 (Pass 6). Round 3, 2026-10-26: *"better"* |
| `Eye_SynthGreen_Clean_Base_sUKN_v01` | Storm = Unreal | 2026-10-26, round 1: *"The eye all look quite bright to me...but maybe that is OK? hard to tell"* → whites warmed in round 3 (Pass 6). Round 3, 2026-10-26: *"better"* |
| `Eye_SynthGrey_Clean_Base_sUKN_v01` | Storm = Unreal | 2026-10-26, round 1: *"The eye all look quite bright to me...but maybe that is OK? hard to tell"* → whites warmed in round 3 (Pass 6). Round 3, 2026-10-26: *"better"* |
| `Eye_SynthBlue_Clean_Base_sUKN_v01` | Storm = Unreal | 2026-10-26, round 1: *"The eye all look quite bright to me...but maybe that is OK? hard to tell"* → whites warmed in round 3 (Pass 6). Round 3, 2026-10-26: *"better"* |
| `Eye_SynthLightBlue_Clean_Base_sUKN_v01` | Storm = Unreal | 2026-10-26, round 1: *"The eye all look quite bright to me...but maybe that is OK? hard to tell"* → whites warmed in round 3 (Pass 6). Round 3, 2026-10-26: *"better"* |
| `Eye_SynthBrown_Bloodshot_Base_sUKN_v01` | Storm = Unreal | 2026-10-26, round 1: *"The eye all look quite bright to me...but maybe that is OK? hard to tell"* → whites warmed in round 3 (Pass 6). Round 3, 2026-10-26: *"better"* |
| `Eye_SynthBlue_Bloodshot_Base_sUKN_v01` | Storm = Unreal | 2026-10-26, round 1: *"The eye all look quite bright to me...but maybe that is OK? hard to tell"* → whites warmed in round 3 (Pass 6). Round 3, 2026-10-26: *"better"* |

**How a round comes in, and goes back out:**
1. A tuning round (the makers re-run on the library machine) or a bench body arrives with a pull, or, for a body, a copy into OMF's git-ignored folder (bench input doc, CTB-6).
2. On the machine with Unreal: the look file's render loop, then the pictures; then a re-serve, and the lead looks in Studio.
3. The lead's words go on the rows above, verbatim, and the pictures are re-committed.
4. OMF and the platform read the rows by content (bench input doc, CTB-4, CTB-8). A push is the lead's word, as always.

## Pass 5 — Round 2: the freckles re-made from the lead's first look (2026-10-26)

**The lead, verbatim:** *"the freckles on the face read really large and oddly placed, The viens look plausable, the marks look plausable (but lack any depth which I think is expected."* Recorded on Pass 4's rows. A lead-directed tuning round, as offered in the handback (*"tell me what you think and I'll run the first tuning round here as a quick fix"*).

- **F-SYN-13 — Why round 1's face freckles read large and oddly placed** (read in `gen_synth_skin.py`):
  - **Large:** radii drawn around 1.1 mm with a tail to 4 mm, each a soft blob two to three times its radius wide, in clumps of nine that merged into patches.
  - **Odd places:** the face's density was a ±5 cm band at nose-tip height running ear to ear, and the face's share came as a few clumps drawn for the whole body, so they landed one-sided.
- **Round 2, the freckles only:**
  - **The face:** a butterfly over the nose bridge and the upper cheeks under the eyes, on the forward-facing surface. It is symmetric by construction (centres from each eye and the nose), not clustered, with a sparse scatter elsewhere on the face. Radii around 0.55 mm (0.3–1.1 mm).
  - **The body:** the same regions, in smaller, looser clusters (5 per cluster, not 9; radii around 0.8 mm).
- **Each layer now draws from its own seeded generator.**
  - **`Synth`, `SynthVeins` and `SynthMarks` are pixel-identical to round 1 on every tone** (compared with `HEAD`).
  - **`SynthAll` is now exactly the three single layers together.** In round 1 its veins and marks sat elsewhere, moved by the freckles' draws.
- **What changed on disk:**
  - 6 maps (Freckles and All × II, IV, VI);
  - their recipes' `base_color_const`, re-calibrated by under 0.001;
  - their 6 articles, one line each;
  - the provenance record.
  - The 9 unchanged maps were re-encoded with identical pixels but different PNG bytes, so the committed bytes were kept.
- **Seen by the agent, not the lead** (`…_skins.jpg` re-made): a fine, even sprinkle over the nose and upper cheeks on II and IV. Storm = Unreal as before (II 2.3 / 2.9, IV 2.1 / 2.5, VI 1.4 / 1.4).
- **"Lack any depth" is expected, as the lead says.** The marks are colour only: no relief, no change in shine. A raised mole or papule needs the normal and roughness inputs of *Skin Maps Beyond Colour* (RD-SYN-3; F-SYN-8).

## Pass 6 — Round 3: the whites of the eyes take the measured sclera colour (2026-10-26)

**The lead, verbatim:** *"The eye all look quite bright to me...but maybe that is OK? hard to tell"*, then *"yes, run round 3"*. Recorded on Pass 4's eye rows.

- **F-SYN-14 — What reads bright is the white, and its colour, not its brightness.** Measured on the pictures, linear, times the articles' own constant:
  - **Irises:** in MakeHuman's range (DarkBrown 0.01 … LightBlue 0.22, against MakeHuman's 0.02 … 0.30).
  - **Whites:** 0.50, against MakeHuman's pictures at 0.34, and Physically Based's measured *Eye (Sclera)* (the library's `Sclera_Natural`, linear 0.652, 0.5, 0.394) at 0.52. **So the brightness is the measured one, and MakeHuman's are about a third darker.**
  - **Colour:** red/blue 1.18, near-neutral, against the measured sclera's 1.65, a warm ivory. A white with no warmth reads bright at a correct brightness.
- **Round 3** (`gen_synth_eyes.py`):
  - the white takes the measured sclera's colour at round 1's brightness;
  - the edge keeps its darkening toward the hidden side;
  - irises, vessels and the bloodshot flush are unchanged (iris pixels identical to round 1).
  - **Tried first and dropped the same day:** keeping round 1's pinker edge on top of the warm colour gave red/blue 1.88. It read peach on the character, close to the skin colour.
  - **Result:** whites at 0.51, red/blue 1.66; the bloodshot pair 0.44–0.45 and redder, as before. Storm = Unreal on the white as before (≈ 2.6).
- **Pictures:** [`261026_R_SyntheticSkinAndEyes_eyes_round3.jpg`](261026_R_SyntheticSkinAndEyes_eyes_round3.jpg) shows four eyes as round 1, the dropped try and round 3, side by side on the character. `…_eyes.jpg` is re-made.
- **What the material cannot fix:** a real white sits in the lids' and lashes' shadow and behind a wet dome. The rig has neither, and both are lighting and eye geometry (CHQ's wet-dome eye, F-SYN-8), not the picture.

## Resolved

- **RD-SYN-1 (the lead, 2026-10-26, "1) yes"):** AI makes **no whole skin map**. It may make the **tone-free detail layer** RD-SKM-5 describes, and content such as tattoo designs. A whole-face AI map is only ever a **judged comparison, never shipped**. *(The lead answered "yes" to the recommendation "not yet: AI for the detail layer and content, a whole-face AI map only as a comparison arm"; recorded as that reading.)*
- **RD-SYN-2 (2026-10-26, "2) yes … run the spike … add these tests directly to the Matter Library"):** the synthetic test set is built **into the library as drafts**, to be judged in Studio.
- **RD-SYN-3 (2026-10-26, "3) yes"):** ***Skin Maps Beyond Colour* is un-parked** (it was parked by RD-DS-8). Starting its discovery stays the lead's call.

## Status

- **Passes:** 5.
  - Pass 1: what is settled.
  - Pass 2: the test set and what tuning taught.
  - Pass 3: how the library should do it.
  - Pass 4: the first look, prepared (renders, pictures, the verdict rows).
  - Pass 5: round 2, the freckles re-made from the lead's first look.
  - Pass 6: round 3, the whites of the eyes warmed to the measured sclera.
- **The lead's first look (2026-10-26):** freckles too large and oddly placed (re-made in round 2; the lead on round 2: *"Yep... better"*); veins plausible; marks plausible, lacking depth as expected. Eyes: *"quite bright … hard to tell"*, whites warmed in round 3; the lead on round 3: *"better"*. The plain `Synth` bases have no words yet.
- **Built:**
  - the test set: 15 skins and 10 eyes, drafts;
  - two makers;
  - the pigment table and its provenance;
  - the look pictures and their script (Pass 4).
- **Rendered by the agent, 2026-10-26,** in Storm and Unreal on the rig's character: all 25 agree across the two tools (F-SYN-9). On tone VI the layers barely show (F-SYN-10). **Not yet seen by the lead.**
- **Owed:**
  - ~~a re-serve on the machine with Unreal, on the lead's word: it restarts Stage (F-SYN-11)~~ **done 2026-10-26** on the lead's *"go - re-serve"*: the served catalog lists 133 articles, the 25 synthetic ones among them, and Stage restarted cleanly;
  - the lead's look in Studio, with the words on Pass 4's rows. The skins are best judged beside `Skin_Fitzpatrick<tone>_Clean_Base` and, for the bar, beside CHQ's `CHQ_EmilySkin`. The eyes beside `Eye_Green`, ideally on CHQ's wet-dome eye;
  - thumbnails for the 25, from the library machine (F-SYN-11);
  - the AI detail layer and the whole-face comparison, which need a GPU machine with the AI tooling.
- **▶ Next, after the lead's look:**
  1. ~~the lead's look at round 2's freckles~~ seen, *"Yep... better"*; round 3's eyes seen, *"better"*; next, VI's marks, if the lead agrees with F-SYN-10;
  2. *Beyond Colour* discovery (RD-SYN-3);
  3. pick which of Pass 3's phases go next.
