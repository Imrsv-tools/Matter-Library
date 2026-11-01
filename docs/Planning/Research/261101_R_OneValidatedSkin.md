# Research input — one validated skin: one subject, judged against the scanned bar, shown in Studio

**Opened:** 2026-11-01 · **Mnemonic:** `OVS` (ids `OVS-n`, `OVS-Qn`) · **Mode:** research input from the Open Morphology Foundation (OMF). It commits the library to nothing; this library's own `/discovery` seeds and rules the phase.
**Origin:** OMF research `261026_R_SyntheticSkinAndEyeSets.md` (OMF `.ai/planning/research/`), Passes 9–13 (2026-11-01). That doc reviewed the skin-and-makeup approach across OMF, this library and the platform, and it holds the sources.
**The lead's direction, 2026-11-01, verbatim** (in OMF's session):
- *"OMF is the keeper of taxonomy, ontology and the overall apprach to make things as realistic as possible … if you do the NEXT step is figure out how to vlisdate it... We need to STOP DOING 10 , 8, 26 versions of things... we need one 20 year old white female form and test with with (beause we have a real skin "Emily" test asset). Then we build all the tooling needed to make our own, and show it in studio...."*
- Asked whether that form is today's hm08 body or a new body, and where the phase lives: *"today's hm08, Matter Library hosts it - Share yousr insights with it and push.. it will seed the phase"*.

**Public-repo note.** Only what the library needs is here: no platform paths, no ruling ids from other projects, no private facts.
**Measured at:** this repo's `4f17d4d` (origin, 2026-10-30).

---

## The direction, as rulings (recorded by date and content)

- **2026-11-01 — OMF keeps the approach to realism.** OMF defines three things; this library builds its pieces to them, and the platform wears them:
  - the taxonomy of a character's look: its layers, the kinds of change, and what each mark is in measured terms;
  - the body's regions and landmarks;
  - how realism is judged.

  This sits beside RD-CMT-1 without conflict: that ruling is about who **makes** a piece, and this one is about who **defines** the approach.
- **2026-11-01 — Validate on one subject, not many versions.** The subject is a 20-year-old woman on **today's hm08** body, judged against the scanned skin the platform already fitted onto hm08 on 2026-10-25 (the bar this library's Phase23 measured against). Then build the tooling to make our own, and show it in Studio.
- **2026-11-01 — This library hosts the phase.**

## The proposed phase — *One Validated Skin*

**Outcome (proposed):** *in Studio, our own skin on one young woman's face stands beside the scanned skin in the look-dev scene, and the lead cannot tell them apart at set distances, or names, part by part, what still differs.*

**Why one subject is the right test** (OVS-1):
- **The mesh is held fixed and only the skin varies,** so a verdict is about the skin.
  - hm08's coarse ears and hands look the same in every column, so they do not bias the comparison.
  - The scanned skin already sits on hm08's own UVs, so no new mesh is needed.
- **It is the instinct of Phase23's click 2, made the rule:** *"this is taking too long, stop doing shades I. II. VI"*.
- **The later test comes free.** Re-baking the passed skin onto the next body tests *"made in 3D, baked per layout"* on a real change of body.

## The validation protocol (OMF's: the standard the phase opens with)

1. **The subject:**
   - **The body:** the female hm08 as the character builds it today, unchanged for the whole phase. Card hair, today's eyes, and one lighting rig.
   - **The tone:** the bar's tone. This library judged against the bar at III (Phase23).
2. **Three columns on the same body, in the same sitting and the same scene** (the platform's shadowed look-dev scene):
   - **A, known-good:** the scanned bar.
   - **B, known-bad:** today's shipped skin at that tone. The lead on Phase22's close: *"they look totally fake"*.
   - **C, the candidate:** our own skin for this subject. Several C rows are allowed (OVS-Q1).
3. **The ruler is checked first, in that sitting.** A must read as real and B as fake, in the lead's words. If not, the scene or the views are wrong and no verdict counts.
4. **Fixed views at set distances,** on the Desktop and in the headset:
   - the face from the front, three-quarter and profile;
   - close-ups of an eye, the lips, and the cheek with the nose;
   - the distances are fixed once (OVS-Q2) and never changed mid-phase.
5. **Two measures:**
   - **The screen:** the region-by-region profiles against the bar, built in Phase23 23.2.7–23.2.9. A screen can rule a failure out; it never accepts.
   - **The gate:** the lead's verdict per column and view, verbatim. It passes when C cannot be told from A, or the remaining gap is named by part.
6. **The claim is the face, this subject, this tone, nothing more.**
   - The bar is a head scan; its body was colour-matched at the neck (OVS-7). So the body has no measured bar here and makes no claim.
   - Other tones, ages, structures and makeup are later re-runs.
7. **After a pass, in order:**
   - re-bake onto the next body;
   - makeup and marks on this same subject (*Skin Layers*);
   - then other tones and ages.

## What OMF's review found that this phase needs

- **OVS-2 — The judge comes first, and it is the platform's.** RD-CMT-4 puts the verdict in the platform's look-dev scene. The asks are already filed: P33 (open a draft there), P34 (draw the shine maps) and P35 (keep a structure).
  - **None is answered:** as of 2026-11-01 the platform's docs mention no shine maps and no way to open a draft there.
  - Phase22 and Phase23 were judged in this library's look view, which is not what a Creator sees in Studio.
  - **The phase's first steps are therefore the judge** (with the platform), before any skin is tuned.
- **OVS-3 — AI enters as a C row, as a structure, never as a map.**
  - RD-SKM-5 stands as written: *"A fully AI-made map is not accepted"*. Its reasons are not licences, so a later "set licences aside" does not lift it:
    - baked light;
    - one picture is one tone;
    - likeness;
    - a map painted in one UV layout does not carry to the next.
  - **An AI-made structure fits the rules:** projected onto the body and stored in 3D, separated from its light, decomposed into pigment (melanin, blood), and calibrated like any structure, with a likeness check.
  - If an AI row beats the procedural one at the gate, the re-ruling is narrow: an AI-made **structure** is accepted under those conditions.
- **OVS-4 — The skin-colour model is not on this phase's path.** Phase23 23.2.1 found OMF's model holds at III and IV and fails at I, II, V and VI. The subject is at III, so the borrowed response is not used. Fixing the model is OMF's, before the other tones.
- **OVS-5 — Placement:** on hm08, the maker's own face regions (`gen_synth_skin.FACE`) are enough. The body's regions and landmarks OMF will define matter at the re-bake step, not before.
- **OVS-6 — For *Skin Layers*, not this phase: marks need pigment.**
  - A mark written as a pigment change (a bruise, a flush) can only become colour where the skin's pigment fields are.
  - But `SkinMaps.md` keeps them inside the maker and ships only the baked colour.
  - OMF's recommendation for that phase: a skin ships its pigment fields and the model's table, and the platform's bake turns pigment into colour. Cosmetics (foundation, lipstick, tattoo ink, dirt) stay paint over the skin.
- **OVS-7 — The bar is the face only.** The platform's fit of the scan to hm08 baked the head's maps into the face layout and the atlas, and colour-matched the body to the head's medians at the neck seam (2026-10-25).

- **OVS-8 — Hold the lips and the picture size fixed too** (added 2026-11-01, after OMF read the platform's own character model of the same day).
  - The bar wears its lips on the skin, so every column does.
  - The bar was baked at 8K on hm08's atlas, while today's skins are 2048². The columns are compared at one layout and one size: the bar resampled to the candidate's size, or the candidate made at the bar's. Otherwise resolution, not skin, decides the verdict.
  - The platform now draws one UV set on a skinned mesh, so the atlas is the layout.
  - The platform's model also puts the lips in the body, which touches P15 and RD-P21-2. It reaches this library as the platform's own map asks, not through this phase.

## Held fixed, and what varies

| Held fixed for the whole phase | Varies |
|---|---|
| the hm08 female body · its eyes · card hair · the look-dev scene and its light · the views and distances · the tone · **the lips worn on the skin**, as the bar's already are · **one layout (hm08's atlas) and one picture size for A, B and C** (OVS-8) | **only the skin:** its colour map and its shine set (roughness, relief, cavity, scatter) |

## Out of scope, each with its home

- other tones: re-runs after a pass (OMF fixes the model for I, II, V and VI first);
- ages and the next body: the re-bake step, then OMF's body work;
- makeup and marks: *Skin Layers*, on the same subject;
- a body bar: none exists yet (OVS-7);
- eyes: *Eyes in the Shader*. The eyes are held fixed here.

## Questions for the library's discovery (plain)

| Id | Question | OMF's recommendation |
|---|---|---|
| **OVS-Q1** | **Which C rows?** | The best procedural structure today, one structure made for this subject (a seed tuned to the bar), and the AI structure row if the library's AI research has one ready. Three at most. |
| **OVS-Q2** | **The set distances and views.** | Conversational (about 1 m) and close (about 40 cm), in the views of protocol step 4. Fix them at the first sitting. |
| **OVS-Q3** | **Is the subject's age set on hm08 once, at the start?** The character's body is MakeHuman's default proportions today. | Only if the lead wants it. Set once and never moved: a change of shape keeps hm08's UVs, so the bar's maps still fit. |

## Pass 2 — The library's side: one complete set, and the plan (2026-11-01)

*Written by this library's `/research` session, after reading this doc, the platform's same-day character model and its skin phase's seed (read in the platform's clone; recorded here by content only).*

**The lead, here, verbatim:** *"Studio provided insight and so did OMF... please read their updates adn lets come up with a plan for getting a full set of skins completed and testable for the full concept... Just ONE set please we need to stop genearting 5 shades... let's get one complete set build and tested,,, then we can add variety."*

- **F-OVS-L1 — The protocol fits the library's tools as they stand.**
  - The look view already draws a reference column from a picture outside the tree (Phase23 23.1, RD-P23-10).
  - The bar's fit to hm08 exists on the machine with Unreal at 8K, with colour, specular and scatter. So column A can wear the bar's own shine, not only its colour.
  - No platform work is needed to run the verdict in the library's look view. Studio's look waits on the platform's shine-map carry (P34) and a draft in its look-dev scene (P33). The platform's skin phase runs after its links work (its plan, 2026-11-01).
- **F-OVS-L2 — The platform's character model of 2026-11-01** (the lips part of the body, nails their own part, makeup one merged layer of pieces) **agrees with the protocol's lips row (OVS-8).** The one set wears its lips on the body's skin. The library's existing `Lips_*` articles stay as they are until a ruling retires them.
- **F-OVS-L3 — The AI row has a working start.** The library's spike of the same day (`261101_R_Spike_SkinMapFromImageModel.md`) projected an image model's person onto hm08's head and baked it into the map in under a minute, untrained. OVS-3's *structure* needs three steps the spike did not take:
  - masks at the brows, lids and lips;
  - inversion to melanin and blood through the maker's skin model;
  - the maker taking that field in place of its own.
- **The plan is seeded as [`Phase24_OneValidatedSkin.md`](../Phases/Phase24_OneValidatedSkin.md):**
  - **one set** = body skin (lips in) + its own shine set + nails, one tone, one person;
  - **four steps:** the judge and the ruler click → C1, the pigment maker tuned to the bar → C2, the image model's skin as a structure → the winner finished, served and seen on the character.
  - It answers OVS-Q1 (two C rows: C1, C2), OVS-Q2 (the views and distances as recommended) and OVS-Q3 (the default age, unless the lead sets it) **as recommendations for discovery.**
- **After it, as phases (unnumbered, the lead's to cut):**
  - *Skin Layers* on this same subject, from its pigment fields;
  - *Variety*: other tones, people and ages, as re-runs of the passed recipe;
  - then the order of 2026-10-27 resumes.

## Status

- **Passes:** 2.
  - Pass 1: OMF's input (2026-11-01; OVS-8 added the same day).
  - Pass 2: the library's side, and the plan (2026-11-01).
- **Ruled 2026-11-01** (recorded above by date and content): OMF keeps the approach; one subject on today's hm08; this library hosts the phase.
- **Seeded:** [`Phase24_OneValidatedSkin.md`](../Phases/Phase24_OneValidatedSkin.md). OVS-Q1 … Q3 are answered there as recommendations for its discovery.
- **▶ Next:** `/discovery Phase24` when the lead is ready.
