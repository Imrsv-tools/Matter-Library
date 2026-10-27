# Phase23 — Synthetic Skin Sets

**Status:** IN EXECUTION (2026-10-27, the lead's *"/execute P23"*; at `749fb60`). *Before:* BRIEF READY (discovery Pass 1, 2026-10-27), and before that SEEDED the same day. The lead numbered it Phase23 with *"/discovery P23"*, then *"yes. synth skin"*, which opened Pass 1. It was the head of `## Future` in the lead's order of 2026-10-27 (RD-CMT-3), and F-CMT-9 had laid out *Phase23* for it.
**Lane:** `build` (§Risk lane). **Next:** `/execute P23`.
**Measured at:** `4398f05`, on **the machine with Unreal**. Unreal 5.8 is at the path `unreal/build.sh` takes as `UE`, and the official Blender 5.2.2 is set as `MATTER_BLENDER` (Learnings B22). `unreal-runtime-v7` is pinned.
**Builds on:** *Skin Maps* ([`Complete/Phase21_SkinMaps.md`](Complete/Phase21_SkinMaps.md)), which shipped the colour map, and *Skin Maps Beyond Colour* ([`Complete/Phase22_SkinMapsBeyondColour.md`](Complete/Phase22_SkinMapsBeyondColour.md)), which shipped the four shine maps. It closed 2026-10-27, the lead: *"they look totally fake but better then the previous totally fake looking ones so we continue building and learning"*. Its deferral table routes *"the skin still reads as fake"* here.
**Research:** [`261026_R_SyntheticSkinAndEyes.md`](../Research/261026_R_SyntheticSkinAndEyes.md) (the test set and the makers, F-SYN-1 … 14; Pass 3, item 1) · [`261027_R_CharacterMaterials.md`](../Research/261027_R_CharacterMaterials.md) (Passes 4 and 6; RD-CMT-1 … 4) · [`261014_R_SkinMaps.md`](../Research/261014_R_SkinMaps.md) (RD-SKM-1 … 6).

## Outcome

**Every skin tone has several real-looking skins with no person in them, each tone with its own regional colour, made from one set of pigment maps.**

*(Verbatim from the Roadmap, as seeded 2026-10-26. The reading used here: one set of pigment fields per skin drives all six tones, so "the same person" exists at every tone.)*

---

## The Brief

### What this phase builds, in one paragraph

The library's skin colour stops being paint and becomes pigment. `gen_synth_skin.py`'s approach takes over as **the library's skin-map maker**, replacing `gen_skin_maps.py`'s colour recipe:
- every texel gets a melanin and a blood amount, placed on the body in 3D;
- a skin model turns those amounts into colour;
- the library's calibration still holds each tone's average to its measured value.

**One set of pigment fields then gives each of the six tones its own regional colour.** Today's six maps are one picture (F-P21-10). The skin model is **refitted per tone first**, because today it only works at III and IV (F-P23-1). The six shipped skins take the result in place. **Two more structures per tone** follow, so two characters of one tone need not share a face:
- named `Skin2_…` and `Skin3_…`, with the tone kept in the Variant token, so lips, nails and the platform's tone control still pair by it;
- each structure is the same person at every tone.

**Before any of that, click 1 tests the phase's premise.** The lead's bar, the Emily skin, is put on the library's own body in the library's look view, next to today's skin, as a local reference that never enters the tree. Then we see whether colour is still the lever in our light and on our shine.

### First human test

**Where:** the machine with Unreal. Every tool the clicks compare runs there.
- **The look:** the library's Unreal test runtime, in its shadowed **look view** (`tools/parity/look.py`, Phase22 RD-P22-11; the pinned `unreal-runtime-v7`). The cameras are the face from the front, the face at three quarters, the back of the hand, and the backlit ear. The agent opens the sheet with `xdg-open` and puts its path in the handback.
- **Tool agreement:** the rig's sheet (`face`, `hand`) in Storm, Blender and Unreal. Storm runs at 512 px on this machine (Storm S11).
- **The agent drives every tool; the lead looks and judges.**
- **Before each click, the change is measured as visible.** A look click is called only then (Phase22, RD-P22-14's reach as the lead settled it).

1. **The bar, in our light (23.1).** One look sheet, all four columns on the same substance, Fitzpatrick III's, wearing Phase22's four shine maps:
   - (a) today's `Skin_FitzpatrickIII_Clean_Base`;
   - (b) the Emily colour picture as the platform's spike made it;
   - (c) the same picture held to tone III, calibrated as any contributor's picture is (`SkinMaps.md` §Calibration);
   - (d) (c) resampled to the library's 2048² atlas.
   - *Judge:* does (b) or (c) read as skin where (a) reads fake? Does (d) keep what (c) has?
   - **Can the surface show it?**
     - The face is rendered at **2048 px** (`--width 2048`), so it spans more pixels than the 4096 picture gives the face (~880 texels across), and (c) against (d) can differ.
     - The fixture is the rig's hm08 character, the body the Emily picture was laid on.
     - The tone is held in (c) and (d). (b) is paler and far less red than any library tone (F-P23-2), so (b) against (c) separates "her tone" from "her detail".
   - **What the answer decides** (RD-P23-1):
     - If (c) reads as skin, colour is the lever, and 23.2 proceeds.
     - If neither (b) nor (c) does, colour is not the lever in our light. The phase stops, and the next lever goes to the lead.
     - If (c) does and (d) does not, the atlas size is the limit, which reopens RD-P21-5 with the lead.
2. **Six tones, one pigment structure (23.2).** The look sheet: the six tones' face and hand, today's beside new, with (c) from click 1 beside tone III as the bar. Plus the rig's six-tone sheet.
   - *Judge:*
     - each tone has its own regional colour (cheeks and lips redden on light skin and barely on dark; freckle-scale mottling shows on light skin and fades on dark);
     - each tone's average is unchanged;
     - no seams;
     - the three tools move alike;
     - does it come closer to the bar?
   - **Can the surface show it?**
     - The regional colour spans centimetres, at the face and hand cameras.
     - **The agent's evidence, in the 23.2 log:** each tone's map ÷ tone at the cheeks, the lips and the trunk (the redness must fall from I to VI, where today it is equal); the calibration's average per tone (exact to rounding); the model-fit check (RD-P23-3); G8 on every map.
3. **Several skins per tone (23.3).** The look view's face, as a grid: three structures down, six tones across. Plus the hand, and the thumbnail sheet of the 18 skins.
   - *Judge:*
     - the three in a column read as three different people of that tone;
     - each row reads as one person at six tones;
     - the lips' edge is clean on `Skin2` and `Skin3`, which wear the tone's one `Lips_` article (RD-P23-5).
   - **Can the surface show it?**
     - A structure differs in its mottling, sun pattern and regional redness at centimetre scale (RD-P23-4), at the face camera.
     - The lips' edge is checked by measurement first: the three structures' maps are identical inside the lips' zone (RD-P23-5).

**Reconciled click by click:**
- Click 1 needs only 23.1: the reference column in `look.py`, today's III skin, and Phase22's shine maps. The picture is on this machine (F-P23-8).
- Click 2 needs 23.2. Its bar column is click 1's (c), re-run.
- Click 3 needs 23.3. Its lips need 23.2's maker, which draws the lips' zone from the tone alone.
- **§In now, walked:** every row below names its step.

**Not a click: Studio.** The verdict in the platform's look-dev scene (RD-CMT-4; P33), and Studio drawing these skins with their shine (P34), are the platform's sittings, recorded in the ledger. **The close does not wait for them** (RD-P23-9).

### In now

| Item | Step |
|---|---|
| **A reference column in the look view:** `look.py` draws a skin article with a picture supplied from outside the tree, as-is or held to the article's tone. It is local only (RD-P23-10) and uses no runtime change. | 23.1 |
| **The skin model refitted per tone** (RD-P23-3): the pigment table re-made from OMF's pinned model with the eumelanin share and the epidermis thickness per tone (and the melanin range below 0.003), so each tone's own colour sits inside the model | 23.2 |
| **The library's skin-map maker:** `gen_synth_skin.py`'s pigment approach, at all six tones, replaces `gen_skin_maps.py`'s colour recipe (RD-P23-2). It keeps `calibrate`, the contributor's `--picture` path and the provenance record. It draws the lips' zone from the tone alone (RD-P23-5). | 23.2 |
| **The six `Skin_Fitzpatrick*_Clean_Base` and six `Lips_Fitzpatrick*`** re-made in place at `v01`, with their `base_color_const` from the calibration | 23.2 |
| **The three plain `…_Clean_Synth` drafts retired:** the shipped bases are their successors (RD-P23-8) | 23.2 |
| **Two more structures per tone:** `Skin2_Fitzpatrick<Tone>_Clean_Base_s001_v01` and `Skin3_…`, twelve new `candidate` articles with their maps and provenance, wearing the shared shine maps (RD-P23-4, RD-P23-6) | 23.3 |
| **Thumbnails** for the 18 skins and six lips; the dev install re-served | 23.3 |
| **Ledger:** a row asking Studio's skin-tone control to keep the skin's Material token (its structure) when it changes the Variant (its tone), and to offer the structures. Its id is claimed when it is written. | 23.3 |
| **Written down:** `SkinMaps.md` (the pigment maker, the refit, structures, how to make one); `Identity.md` (a skin structure is a base-set id on the Material token: an example); the Glossary (*skin structure*, *pigment map*); Learnings where a trap is found | 23.3 |
| **A dev snapshot**, at the lead's word, with `HEAD` pushed | at the close |

### Not now

- **Marks as placed layers, and the 12 layer drafts** (`SynthFreckles`, `SynthVeins`, `SynthMarks`, `SynthAll` × II, IV, VI), tone VI's marks included: *Skin Layers* (F-SYN-3; RD-CMT-2). The drafts stay as they are, as its references (§Deferred).
- **The AI detail layer** (RD-SKM-5, RD-SYN-1): it needs a GPU machine with the AI tooling.
- **Meta's BioSkin, or any learned skin model:** only if the physical refit fails (RD-P23-3). That would be the lead's question against RD-SYN-1.
- **The makers' six hm08-atlas inputs carried onto the body** (`SkinMaps.md`'s Todo): re-routed to the first `Body_v02` maps (CTB-7), which is the condition the spec's own Todo names. Phase22 had routed it here. Nothing in this Outcome reads it.
- **A face map of its own, or a larger atlas:** RD-P21-5 stands, unless click 1's branch reopens it.
- **Eyes:** *Eyes in the Shader*.
- **Studio's controls** (tone, redness, freckles, age, pores, oiliness, wetness): the platform's (RD-CMT-1).
- **A release:** *Release Bundle*. Pre-release, no versioning.

### The reuse check

*What does the stack already provide, and which contracts are touched?*
- **The pigment maker exists.** `gen_synth_skin.py` (2026-10-26) rasterises hm08 in 3D, builds the melanin and blood fields and the freckles, veins and marks, and calibrates through `gen_skin_maps.calibrate`. It runs three tones and one seed today (`TONES`, `SEED`). This phase widens it; it is not new.
- **The calibration, the provenance writer, the lip rule and the region masks exist** in `gen_skin_maps.py` and are kept.
- **The skin model exists:** OMF's `biophysical.py` at the pinned `e079588` (Apache-2.0, on this machine). Its `SkinPhysiology` already carries `eumelanin_ratio` and `epidermis_thickness_mm` (F-P23-9). The refit uses parameters the model has; nothing is invented.
- **Colour reaches every renderer through `base_color_map`** (RD-SKM-3). **No contract input is added**, no master changes, and so **no new Unreal runtime is owed** (`LOCAL_DELTAS.md`: only a change to what the masters draw owes one).
- **The shine maps exist and are shared** (RD-P22-2). Every new skin names the same four files.
- **The pairing exists twice:** the platform pairs lips and nails by the Variant token (ledger M4), and so does the rig (`rig.py`, `skin.split("_")[1]`). A structure on the Material token leaves both untouched (F-P23-3).
- **The look view, the rig, `--today` and `--also`, the thumbnails and `serve_to_stage.py` exist.** Only the reference column is new, and it is a tool option, not a gate.
- **Contracts touched:** none in LCDSchema. `Identity.md` gains an example of a reading it already allows (*"Material … optionally with a base-set id, as in `Limestone26b`"*).

### Decisions that bind

*One authoritative copy. Rulings are quoted where they are the authority.*

**Carried rulings:**
- **RD-SKM-1:** one approved mesh, hm08, as `MakeHuman_Body_v01`.
- **RD-SKM-2, RD-SKM-5, RD-SYN-1:** no photograph or scan of a person in anything shipped, and AI makes no whole map. **RD-RO-2:** *"material are CC0"*.
- **RD-SKM-3:** one colour map per tone, through `base_color_map`, with no new input. The pigment maps stay inside the maker; what ships is their baked colour.
- **RD-SKM-4:** plain skin at the genitals and groin, in every structure.
- **Authored on the body, baked per layout** (the lead, 2026-10-26, `SkinMaps.md`).
- **RD-P21-1:** one article carries the tone and its map. **RD-P21-3:** the measured tone stays the average. **RD-P21-5:** the atlas stays 2048².
- **RD-P22-2:** one shine set for every tone.
- **RD-CMT-2** (*"usable on all the chars - not made for ONE character"*): a skin made in 3D on the approved mesh passes by construction.
- **RD-CMT-3:** the order of the character phases. **RD-CMT-4:** the look verdict for a character material belongs in the platform's look-dev scene; the rig stays the tool-agreement check.
- **Phase22, RD-P22-14** (the lead: *"Don't ask mty why I think it look like plastic until we get to the pahses where we are actaully trying to implment the learning from emily"*): **this is that phase.** The plastic question is asked here, against the bar. The click is called only when its change is measured visible.
- **Pre-release, no versioning** (`AI_WorkingAgreement.md` §Settled practices): articles are rebuilt in place at `v01`. None is in a frozen release.

**Decided here, unless the lead says otherwise:**
- **RD-P23-1 — Click 1 tests the premise before the maker is rebuilt.**
  - F-SYN-1 says colour at skin scale moved the look most. That was seen in Studio's light, on a skin with no shine maps. Phase22 then changed the shine, and the lead still reads the skin as fake.
  - So the bar goes into our light and onto our shine first. The three branches in click 1 are decided now, so the answer routes the phase without a meeting.
- **RD-P23-2 — The six shipped skins take the new colour in place. The pigment maker becomes the library's one maker.**
  - Research Pass 3 proposed this. The lead's *"so we continue building and learning"* at Phase22's close keeps the shipped six as the line being improved.
  - `gen_skin_maps.py`'s procedural colour recipe is retired. **Its capabilities stay:** one command makes the library's six maps; a contributor's own picture is calibrated with `--picture`; the provenance record is written.
- **RD-P23-3 — The skin model is refitted per tone, physically, before any learned model.**
  - Measured (F-P23-1): tone I sits on the table's melanin floor. VI's model colour is 2.8× the tone in red and 0.6× in blue (red/blue 20.5 against 4.5). Only III and IV are close.
  - **The refit:** per tone, the eumelanin share and the epidermis thickness (and a melanin range below 0.003), from OMF's pinned model. The table is re-made the way `chromophore_lut.json` was, its header naming the model and the commit. CC0 derived numbers, Apache-2.0 code, not copied into the tree.
  - **It passes** when, at all six tones, the model colour at the tone's pigment is within ±15 % of the tone per channel and its red/blue within 15 %. The maker prints this check; it is not a new gate.
  - **If it fails** at a tone: that tone keeps today's procedural colour, and BioSkin goes to the lead as a question against RD-SYN-1. It is a learned model that colours every texel, though it paints no map.
- **RD-P23-4 — Three structures per tone, named on the Material token: `Skin`, `Skin2`, `Skin3`.**
  - **What a structure is:** a seed plus a small set of named maker parameters (sun-exposure pattern, mottling strength and scale, regional redness), kept in the maker's table as RD-P22-19's scatter table is. It is the same person at every tone, because the fields are computed once and only the tone's pigment is applied to them.
  - **Why the Material token:** `Identity.md` gives the Material token *"optionally … a base-set id, as in `Limestone26b`"*, and a structure is a base set. The Variant stays the tone, so ledger M4's pairing and `rig.py`'s pairing are untouched. Changing tone swaps the Variant only, so a character keeps its face. Detail is *"the other layers"*: the drafts' `Synth…` is a layer set, not a structure.
  - **`Skin` keeps its bare name:** the bare name is the stable key (`Identity.md`), so saved scenes holding today's skins keep resolving.
  - **Three, not more:** enough to show a tone has several people. More is a maker parameter later, not a phase.
- **RD-P23-5 — One `Lips_<Tone>` serves every structure of its tone.**
  - The maker draws the lips and their feathered ring into the face from the tone alone, the same in every structure. So the lips' map (structure 1's) meets every structure's skin with no step.
  - **Checked by measurement, not by eye:** the three structures' maps are identical inside the lips' island, its 16 px bleed and the feather.
- **RD-P23-6 — The shine maps stay one shared set across structures too.** They describe anatomy, not pigment (RD-P22-2's reason). The colour's creases come from the same mesh concavity, so they agree.
- **RD-P23-7 — The maker's dependency on `scipy` becomes the project's.** `gen_synth_skin.py` runs today with `uv run --with scipy` (its point processes use a k-d tree). As the library's maker it runs on the project's own environment: add `scipy` to the project, or drop the k-d tree. Execute picks the smaller change.
- **RD-P23-8 — The 15 drafts:** the three plain `…_Clean_Synth` are retired at 23.2, because the shipped bases succeed them (they carry no lead words). The twelve layer drafts stay unchanged, as *Skin Layers*' references.
- **RD-P23-9 — The close does not wait for Studio.** The look view is the verdict here. Studio's look-dev scene (P33) and its shine (P34) are the platform's sittings. This follows the lead's Phase22 close, where *"close"* lifted the Studio wait (RD-P22-13 lifted).
- **RD-P23-10 — The Emily reference never enters the tree.**
  - It is the platform's research spike made from a scanned person: research-only, never shipped (F-SYN-1, RD-SKM-2).
  - It is supplied by path at run time. Its renders stay in the git-ignored `library/parity/` (`.gitignore`, checked 2026-10-27).
  - **No sheet showing it is committed beside a doc** (as the test set's pictures were, Pass 4), published, served or put in a snapshot. Its path is never written in a tracked file; on the machine, `locate -i emily` finds it.

### Risk lane — `build`

The controls this phase touches, each read on 2026-10-27:
- **The name grammar** (`tools/validators/validate_material.py`): six tokens, a scale tag and a version. No rule on the Material token's shape, so `Skin2` passes.
- **What enumerates `materials/character/humanoid/skin/`:** the recipe gate (G5 folder, G8 maps), the catalog, the thumbnails, `serve_to_stage.py` and the release lanes. **Evidence:** the 25 synthetic drafts were added there on 2026-10-26, and `run_all.py` read **18/18 PASS** at Phase22's close (2026-10-27).
- **Code keyed on skin names:** only on the shipped `Skin_Fitzpatrick<Tone>_Clean_Base_s001_v01` (`gen_skin_maps.py`, `gen_synth_skin.py`, `rig.py`, `scale_test_scene.py`, `test_thumbnails.py`), and those names are kept. **On the Material token alone:** the thumbnails' `character_family`, which stops on `Skin2` until 23.3 fixes it (F-P23-3).
- **The masters and the runtime:** untouched. No input is added (§Reuse).
- **The one irreversible risk is publication:** the repo is public, and the Emily reference must never be committed. The controls are `.gitignore`'s `library/parity/` and explicit-path staging (`.claude/CLAUDE.md` §Git). RD-P23-10 names the rule. Nothing here is authorization, secrets, a destructive migration or the public edge.
- **Baseline:** `run_all.py` 18/18 PASS (Phase22's close). No change under `blender/addons/` or `tools/conformance/`, so `check_exporter.sh` is not owed.

### Step list

- **23.1 — The bar, in our light.** `look.py`'s reference column; the sheet of today's III, the Emily picture as-is, held to III, and at 2048. **Click 1**, and its branch (RD-P23-1).
- **23.2 — Six tones from one pigment structure.** The refit (RD-P23-3), the maker at six tones with the lips' zone from the tone alone, the six skins and six lips re-made, the three plain `Synth` drafts retired. The rig over six tones. **Click 2.**
- **23.3 — Several skins per tone.** `Skin2` and `Skin3` at six tones, the lips' check, thumbnails, the dev install, the ledger row, the docs. **Click 3.**

Time to the first click is short: 23.1 is one tool option and four renders.

### Compact build map

- **23.1:** `tools/parity/look.py` gains a reference column. One supplied picture (the Emily colour picture, read from outside the tree) is drawn on the skin article as a binding-supplied picture would be (the Carrier rule), as-is (`base_color_const` = 1) or held to the article's tone (`gen_skin_maps.calibrate`), with an optional resample to 2048. If the job format cannot carry it without a runtime change, a scratch article in the git-ignored `library/parity/` carries it instead. **No runtime is built for it.** Run with `--width 2048`. **Before launching:** `ps -ef | grep "[U]nrealEditor"` (`LOCAL_DELTAS.md` §Two machines).
- **23.2:**
  - The table is re-made from `git -C <OMF> show e079588:tools/material_generate/biophysical.py`, run from a scratch folder (Apache-2.0; not copied in), into `tools/converters/fit/synth/chromophore_lut.json` with the new dimensions.
  - `gen_synth_skin.py` takes all six tones and the per-tone fit, and draws the lips' zone from the tone alone. It writes `MatterLibrary/textures/fit/makehuman/skin/Fitzpatrick<Tone>_basecolor_sUKN.png` (the shipped names) and its provenance.
  - `gen_skin_maps.py` keeps `calibrate`, `--picture` and the masks; its colour recipe goes. Whether the two files merge is execute's call.
  - Recipes `Skin_Fitzpatrick*` and `Lips_Fitzpatrick*` take the printed `base_color_const`. Then `uv run tools/converters/build_proof_subset.py <recipe paths>`.
  - The three plain `Synth` drafts: their recipe, `.mtlx` and map go.
  - Look: `uv run tools/parity/look.py Skin_Fitzpatrick<Tone>_Clean_Base_s001_v01 --today 4398f05`. Rig: `uv run tools/parity/rig.py --character …`.
- **23.3:**
  - The maker's structure table and its `Skin2`/`Skin3` output (maps named by article, e.g. `Skin2FitzpatrickIV_basecolor_sUKN.png`; execute checks the fit-set filename grammar).
  - Twelve recipes copied from each tone's `Skin_` recipe, then `build_proof_subset.py`.
  - `tools/thumbnails/showcase.py` `character_family` reads the article's part (or strips a structure number) so `Skin2`/`Skin3` get the skin's views (F-P23-3); `test_thumbnails.py` gains the case.
  - The lips' measurement; `make_thumbnails.py`; `serve_to_stage.py` (restarts the Stage daemon, `LOCAL_DELTAS.md`).
  - The ledger row; `SkinMaps.md`, `Identity.md`, the Glossary.
- **Tests:** `run_all.py` per step. One real-path smoke per click is the look view itself. The refit check and the lips' check are printed by the maker, not new gates.

### Open for the lead

*None.* Click 1's branches (RD-P23-1) may put one to the lead after it is seen. RD-P23-3's fallback (BioSkin) reaches the lead only if the refit fails.

---

## Findings (discovery Pass 1, 2026-10-27)

- **F-P23-1 — The skin model reaches only the middle tones.** Probed on the table as committed (`Lut.melanin_for`, melanin with blood at 0.02, oxygen 0.8). The model colour ÷ the tone, r / g / b, and the red/blue of the model against the tone:

  | Tone | Melanin | Model ÷ tone | Red/blue, model vs tone |
  |---|---|---|---|
  | I | 0.0030 (**the table's floor**) | 0.72 / 0.78 / 0.77 | 1.45 vs 1.53 |
  | II | 0.0119 | 0.75 / 0.97 / 1.09 | 1.57 vs 2.30 |
  | III | 0.0200 | 0.93 / 1.03 / 1.00 | 1.69 vs 1.82 |
  | IV | 0.1035 | 1.03 / 1.12 / 0.94 | 3.65 vs 3.33 |
  | V | 0.1528 | 1.35 / 1.24 / 0.84 | 5.77 vs 3.58 |
  | VI | 0.2723 | **2.78 / 1.66 / 0.61** | **20.5 vs 4.5** |

  The calibration hides the average error, but each tone's regional changes come from the model's slope at a wrong operating point. At I, every region lighter than average (palms, soles, trunk) is clamped at the floor. At VI the changes run orange. This fits the test set's *"on tone VI the layers barely show"* (F-SYN-10). It also matches Learnings B23 (Cycles carries red through dark skin), a separate effect in the renderer.
- **F-P23-2 — The Emily picture is paler and far less red than any library tone.** Its average over hm08's skin, lips excluded, linear: 0.600, 0.527, 0.482 (red/blue 1.24). Tones II and III are 2.30 and 1.82, and it is about equally far from I, II and III (log distance 0.39–0.44). Comparing it with a library skin mixes her tone with her detail. Click 1 shows it as-is and held to III to separate them.
- **F-P23-3 — The structure is free on the Material token, with one tool to fix.**
  - Ledger M4: *"The pairing is the name's Variant token"*. `rig.py` pairs by `skin.split("_")[1]` (`cast_for`) and casts a fitted skin onto the body by the file's `part` (`character_cast`), so `look.py` and the rig take a `Skin2_…` unchanged.
  - **The thumbnails do key on the Material token:** `tools/thumbnails/showcase.py` `character_family` looks up `stem.split("_")[0]` in `CHARACTER_FAMILIES` and **stops** on an unknown one (*"no Character family 'Skin2'"*). 23.3 makes it read the part from the file, or strip a structure number. That is the cheaper cost of the three tokens: the Variant would break M4's pairing, and Detail means layers.
  - A consumer's own code keyed on `Skin` cannot be read from here. The ledger row at 23.3 names the new names.
- **F-P23-4 — Only `Skin_FitzpatrickIV_Clean_Synth` wears the shine maps; the other 14 drafts do not** (grepped `roughness_map_tex`). Phase22's Deferred row (*"the 15 synthetic drafts wearing the maps"*) is answered by RD-P23-8: three retired, twelve left for *Skin Layers*.
- **F-P23-5 — A draft differs from a shipped skin only in its map, its `base_color_const`, its status and its provenance** (the IV recipes diffed). Taking the new colour in place is a recipe-level change.
- **F-P23-6 — Nothing on the consumers' side since this morning's sweep.** The platform's docs and repo have no commit about skins since 2026-10-27 00:00 (fetched). The character-materials research's sweep of the same day stands. Of this repo's research footers, only the sky asks owe the library a pass, and that is unrelated.
- **F-P23-7 — `gen_synth_skin.py` needs `scipy`, which the project does not carry** (`uv run --with scipy`; neither `gen_skin_maps.py` nor `gen_skin_shine.py` uses it). See RD-P23-7.
- **F-P23-8 — The bar is on this machine.** The platform's Emily colour picture on hm08's atlas, 4096², is on the machine with Unreal. `library/parity/` is git-ignored.
- **F-P23-9 — OMF's model at the pinned `e079588` is on this machine** (Apache-2.0). `SkinPhysiology` exposes `eumelanin_ratio` (0–1), `epidermis_thickness_mm` (0.03–1.5) and `melanin_fraction` (0–0.45). The table used the defaults (0.85, 0.10 mm).

## Deferred

| What | To | What it consumes from this phase |
|---|---|---|
| The 12 layer drafts as placed layers; tone VI's marks | *Skin Layers* | the pigment maker's freckle, vein and mark generators; the structure's fields, so a layer lands on a skin's own pigment |
| The makers' atlas inputs on the body | the first `Body_v02` maps (CTB-7) | the maker as this phase leaves it |
| The AI detail layer | later, a GPU machine (RD-SKM-5) | the calibrated base it multiplies |
| Studio keeping a character's structure when its tone changes | the platform, through the row filed at 23.3 | the `Skin` / `Skin2` / `Skin3` Material tokens; the Variant pairing (M4) |
| The verdict in the look-dev scene | the platform (P33) | the 18 skins as served |
| A learned skin model (BioSkin) | the lead, only if RD-P23-3's refit fails at a tone | the refit's printed check |

## Depends on

- **Nothing outside this repo, for every click.** The Emily picture is read locally (RD-P23-10). OMF's model is read at its pinned commit from the local clone.
- A dev snapshot and the push are the lead's word, at the close.

## Discovery Log

- **Seeded 2026-10-27** (`4398f05`) on the lead's *"/discovery P23"*. It had no phase doc, so that invocation seeded and stopped.
- **Pass 1 — 2026-10-27,** opened by the lead's *"yes. synth skin"*.
  - **Examined:** `_Architecture.md`; Taxonomy §Character; Identity's grammar; `SkinMaps.md` in full; LCDSchema's shine maps (through `SkinMaps.md`); ledger M4, P28, P32, P33, P34; the research `261014_R_SkinMaps.md` §Resolved, `261026_R_SyntheticSkinAndEyes.md` in full, `261027_R_CharacterMaterials.md` Passes 4, 6 and 7 and §Resolved, and `261026_R_CharacterTestBenchInputs.md` §Resolved; Phase22 in full, including its close, landing in a sibling session during this pass; the three makers, the IV recipes, `rig.py`'s pairing, `look.py`'s options and `validate_material.py`'s grammar; OMF's model at `e079588`.
  - **Learnings:** B8, B22, B23, S10 and S11 bear on the clicks and are carried by the specs and Phase22, not restated. The MaterialX and Unreal entries are not touched: no master changes.
  - **Probed:** the skin model at six tones (F-P23-1) and the Emily picture's average (F-P23-2), as scratch scripts outside the tree.
  - **The seed's questions, closed:** Q-P23-1 → RD-P23-2 · Q-P23-2 → RD-P23-4 · Q-P23-3 → RD-P23-6 · Q-P23-4 → RD-P23-3 · Q-P23-5 → RD-P23-8 · Q-P23-6 → RD-P23-1, RD-P23-9 · Q-P23-7 → RD-P23-5 · Q-P23-8 → **moot:** Phase22 closed during the pass.

## Execution ledger

*`step · commit · result · next`. Opened 2026-10-27 at `749fb60`, tree clean, on the machine with Unreal; no Unreal Editor running.*

- **23.1.1 — the reference column** · the `23.1.1` commit · `look.py --reference <picture>` adds three columns, the skin and its lips together (they share one map and one constant): (b) as made, constant 1; (c) held to the skin's tone at the picture's own size, by `gen_skin_maps.calibrate`; (d) the picture box-filtered in linear light to 2048, then the same step. Everything it writes stays under the git-ignored output folder (RD-P23-10). The picture's skin average reproduces F-P23-2 (0.600, 0.527, 0.482). Held to III: constant (1.028, 0.725, 0.675) at 4096 and (1.026, 0.717, 0.670) at 2048, 0.14 % and 0.15 % of the skin clipped, the skin's average the tone exactly. **The Brief's `--width 2048` cannot run:** at a 4096 capture Unreal asks Vulkan for one 4 GiB block and dies (`VulkanMemory.cpp`, out of memory). Rendered at `--width 1536` (a 3072 capture), where the face still spans more pixels than the picture gives it texels. **Measured visible** (8-bit levels over the frame; mean, then p99 for c vs d): (a) vs (c): face 5.7, three-quarter 6.2, ear 5.3, hand 0.7. (c) vs (d): mean 0.6–1.6, p99 9–17. **The hand row shows tone only:** the picture carries its detail on the face, and the hand is near plain. `run_all.py` 18/18 PASS.
- **23.1.2 — click 1** · **SAT 2026-10-27. The lead, verbatim: *"b,c,d read as skin (but they had a rough night)... b is a very pale., c and d read better... we need some sort of texture on the hands and rest of the body...."*** · the sheet `library/parity/Look__Skin_FitzpatrickIII_Clean_Base_s001_v01__vs_reference/look_sheet.png` · **RD-P23-1's branch: colour is the lever, and 23.2 proceeds.** (d) reads as (c), so the 2048 atlas is not the limit (RD-P21-5 stands). Taken into 23.2: **the hands and body need skin-scale texture too**, not only the face (judged at click 2 on the hand camera, measured first). *"A rough night"* is the bar's own under-eye darkness and blotching; the maker does not copy it.
- **23.2.1 — the refit (RD-P23-3): FAILS at I, II, V and VI** · this commit · OMF's model at `e079588` vectorised in a scratch folder (Apache-2.0, not copied in); its projection matches the committed table to 0.002. Each tone searched over the eumelanin share (0–1), the epidermis (0.03–0.4 mm) and melanin down to 0.0003; worst error of the per-channel ratio and the red/blue ratio, the pass is ≤ 0.15:

  | Tone | As decided (share, epidermis) | With blood and oxygen also free |
  |---|---|---|
  | I | **0.27**: melanin at the floor, the model still ~25 % too dark | 0.12, at the blood floor, pheomelanin only |
  | II | **0.28**: too little red | 0.14, melanin 0.21 (10× IV's) |
  | III | 0.04 | 0.04 |
  | IV | 0.10 | 0.00, epidermis 0.4 mm and melanin 0.02 |
  | V | **0.38**: melanin at the model's ceiling (0.45) | 0.12, blood at the ceiling |
  | VI | **2.0**: red 3× the tone at the ceiling | **1.46** |

  The freed fits pass by contradiction (II darker in melanin than IV; both light tones on the blood floor), so a regional change driven from them is arbitrary, and VI fails under every setting. **The model is the limit, not its parameters.** RD-P23-3's fallback (today's colour at the failing tones; BioSkin to the lead) applies, and it breaks the Outcome's *"one set of pigment maps"* at four tones · next: the lead's call.
