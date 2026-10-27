# Phase23 — Synthetic Skin Sets

**Status:** SEEDED (2026-10-27) — numbered Phase23 by the lead's *"/discovery P23"*, which this doc reads as the numbering act: *Synthetic Skin Sets* was the head of the Roadmap's `## Future` (the lead's order of 2026-10-27, RD-CMT-3; F-CMT-9 had laid out *Phase23* for it). It had no phase doc, only a Roadmap line and a research item, so this invocation **seeds and stops** (`discovery.md` §Cold start, step 1). **The next `/discovery P23` opens Pass 1.**
**Written on:** the machine with Unreal, at `bda56b0`, while *Phase22 — Skin Maps Beyond Colour* is still in execution in a sibling session (its clicks 3–5 and the Studio click owed).
**Seeded from:** [`261026_R_SyntheticSkinAndEyes.md`](../Research/261026_R_SyntheticSkinAndEyes.md) (Pass 3, item 1; the test set, F-SYN-5 … 14) · [`261027_R_CharacterMaterials.md`](../Research/261027_R_CharacterMaterials.md) (Passes 4 and 6; RD-CMT-1 … 4) · [`Phase22_SkinMapsBeyondColour.md`](Phase22_SkinMapsBeyondColour.md) (its Deferred row; RD-P22-14, RD-P22-16) · [`Complete/Phase21_SkinMaps.md`](Complete/Phase21_SkinMaps.md) (F-P21-10) · [`../../specs/Authoring/SkinMaps.md`](../../specs/Authoring/SkinMaps.md).

## Outcome

**Every skin tone has several real-looking skins with no person in them, each tone with its own regional colour, made from one set of pigment maps.**

*(Verbatim from the Roadmap, as seeded 2026-10-26.)*

## Why this is a phase

- **It is the library's answer to the largest gain the platform's character research measured.** A scanned, research-only skin (Digital Emily) on the unchanged body was the biggest single improvement seen (the lead: *"WAY better"*). It can never ship (F-SYN-1). Its difference was colour detail at skin scale. Today's six skins are procedural region colour with nothing at that scale, and **the six maps are one picture** (F-P21-10), so every tone has the same regional hue.
- **It is where the plastic question comes back.** The lead, after Phase22's click 1: *"Don't ask mty why I think it look like plastic until we get to the pahses where we are actaully trying to implment the learning from emily (which clearly did not look like plastic)"* (RD-P22-14). This is that phase. Phase22's shine maps are the channels it rides on (RD-P22-16 already showed the synthetic draft wearing them).
- **The expensive-to-unwind choices sit here:** the maker that becomes the library's skin-map maker, how one tone gets several skins (names and articles), and the skin model at the ends of the tone range.

## Scope — as known at seeding (2026-10-27)

**In (candidate; discovery confirms each):**
- **The pigment-map maker becomes the library's skin-map maker.** `gen_synth_skin.py`'s approach (per-texel melanin and blood fields made in 3D, turned into colour by a skin model) replaces the colour recipe in `gen_skin_maps.py`, **keeping its calibration** (RD-P21-3: the average held to the measured tone). Research Pass 3, item 1.
- **One structure, six tone-correct maps:** each tone gets its own regional colour, where today's six are one picture (F-P21-10). The 15 drafts cover only II, IV and VI.
- **Several structures per tone** (structure seeds), so two characters of one tone do not share a face (CMT Pass 4).
- **The skins wear Phase22's shine maps:** the roughness, normal, cavity and scatter inputs. That is Phase22's Deferred row *"The 15 synthetic drafts wearing the maps → Synthetic Skin Sets"*, consuming *"the shared maps; the three inputs"* (four since RD-P22-18 added `scatter_map`).
- **The makers' six hm08-atlas inputs carried onto the body** (MPFB2's face, lips, ears, eyelids and areolae masks, and `sss.png`): `SkinMaps.md`'s Todo of 2026-10-26, which CMT Pass 6 and Phase22's *Decisions that bind* both place here. `gen_skin_shine.py` reads them too.
- **Tone VI's marks judged** (CMT Pass 6): on VI the layer drafts barely show (F-SYN-10).

**Not now:**
- **The AI detail layer** (RD-SKM-5, RD-SYN-1): later, and it needs a GPU machine with the AI tooling.
- **Marks as placed layers, not separate articles:** *Skin Layers* (F-SYN-3; RD-CMT-2).
- **Eyes:** *Eyes in the Shader*.
- **A denser render body, a face map of its own or a larger atlas:** the atlas stays 2048² (RD-P21-5). A new mesh version is a re-bake (`SkinMaps.md` §Authored on the body).
- **Studio's controls** (tone, redness, freckles, age, pores, oiliness, wetness): the platform's (RD-CMT-1).
- **A release:** *Release Bundle* (pre-release, no versioning).

**Rulings that bind, carried:** RD-SKM-1 (one approved mesh, `MakeHuman_Body_v01`) · RD-SKM-2, RD-RO-2 (no photograph or scan of a person; CC0) · RD-SKM-4 (plain groin) · RD-SKM-5, RD-SYN-1 (AI makes no whole skin map) · RD-P21-1 (one article carries the tone and its maps) · RD-P21-3 (the calibration) · *authored on the body, baked per layout* (2026-10-26) · RD-CMT-2 (a piece works on every character) · RD-CMT-4 and RD-P22-11 (where the look is judged) · RD-P22-2 (one shine set shared by the six tones).

## Open questions — seed against docs (settle in discovery)

*Each was run against the four tests as it was written (`discovery.md` §Forking to the lead). Unless marked **the lead's**, discovery answers it from the tree and the specs.*

- **Q-P23-1 — Do the six shipped `Skin_Fitzpatrick<tone>_Clean_Base` articles take the new colour in place, or do the synthetic skins ship beside them?** Research Pass 3 proposes *replace* (a proposal, not a ruling: RD-SYN-2 made only drafts). Pre-release, an in-place rebuild at `v01` is the standing practice. *Likely closable with a recommendation.*
- **Q-P23-2 — How are several skins of one tone named?** The drafts put `Synth` in the **Detail** token (`Skin_FitzpatrickIV_Clean_Synth_…`), which `NamingConventions.md` defines as *"the other layers"*. A second structure is not a layer. Discovery reads the grammar (Variant, Detail, or a new reading) before anything is named.
- **Q-P23-3 — Does each structure get its own shine maps, or share Phase22's one set?** RD-P22-2 decides *shared across tones*. It does not decide *across structures*, where a face's creases and its mottling might want to agree.
- **Q-P23-4 — The skin model at the ends of the range: is the gap visible?** The OMF two-chromophore table does not reach Fitzpatrick I/II or VI, and the calibration holds the average anyway (F-SYN-5). **Measure first.** Only if the ends look wrong does it become **the lead's** question: the research's candidate, Meta's BioSkin (MIT, a pretrained model from pigment to colour), has to be read against RD-SYN-1 (*"AI makes no whole skin map"*). It does not paint a map, but it is a learned model that colours every texel.
- **Q-P23-5 — What happens to the 15 layer drafts** (`Synth`, `SynthFreckles`, `SynthVeins`, `SynthMarks`, `SynthAll`)? They could be re-made here as whole skins, or held as drafts until *Skin Layers* turns them into placed layers (*"without a new skin per combination"*). Phase22 says this phase *"re-makes them"*. CMT Pass 6 has it *"judge tone VI's marks"*.
- **Q-P23-6 — Where is the plastic question asked, and against what bar?** The library's look view (RD-P22-11) is where Phase22 judges. The lead's bar is the Emily skin, which lives on the platform's side and cannot enter this public repo. The platform's look-dev scene (RD-CMT-4, ledger P33) may or may not exist by then. Phase22 also added a Studio click to its close (RD-P22-13).
- **Q-P23-7 — The lips.** Studio pairs each tone's own `Lips_Fitzpatrick*`, whose map is the shipped one, and the lip edge may show a step against a new body colour (F-SYN-8). Does the maker re-make the lip maps (`LIP_RULE`) in the same run?
- **Q-P23-8 — Sequencing against Phase22.** This phase consumes Phase22's shared maps and inputs, which are landed, and published as `unreal-runtime-v7` (its pin was still being committed by the Phase22 session at seeding). Phase22's close waits on a Studio click that waits on the platform (P34). Does this phase's execution wait for Phase22's close? *Test 2 first: does anything here read what that click could change?*

## Discovery Log

*(empty — `/discovery P23` fills it)*
