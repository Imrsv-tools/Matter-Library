# Research — Character materials: what makes skins, eyes and makeup look great, and how anyone takes part

**Opened:** 2026-10-27 · **Mnemonic:** `CMT` (`F-CMT-n` · `Q-CMT-n` · `RD-CMT-n`) · **Status:** parked — see the Status footer.

> **The ask** (the lead, 2026-10-27): *"So... what can we do to make SkinMaps look great? Are there things we have learned from OMF and from the Character Quality reserach platform did that Matter Library can pick up and carry on with ? I assume skins, eyes, makeup (including scars, and other effects) live here now? If so... like asset workshop... we should define a plan for improvment and document so others know how they can particiapte. thoughts?"*
>
> **Altitude.** A **design** landscape: what the library has to be so that every kind of character material is made the same way, looks as good as it can, and can be made by someone outside the team. **Pass 1 is the audit** (what exists today). **Pass 2 carries what was learned elsewhere.** Passes 3 to 5 are design and name no file to build. **Pass 6 is an order of phases, unnumbered, for the lead to cut.** It commits to nothing. The shape follows the Asset Workshop's own research of the same day, *How the Asset Workshop works for every kind of asset*, on the lead's *"like asset workshop"*.
>
> **Read for it, 2026-10-27:** this repo's `SkinMaps.md`, `CONTRIBUTING.md`, the Roadmap's character seeds and research `261026_R_SyntheticSkinAndEyes.md` and `261026_R_CharacterTestBenchInputs.md`. **At their origins, fetched and never pulled:** the platform's research on character quality (2026-10-25 … 26, 16 passes; its summary, every rulings section, its Skin · Eyes · Makeup proposal, its lever results, its plan synthesis and its Status); the open morphology project's (OMF's) research on synthetic skin sets and on a character test bench (2026-10-26); the Asset Workshop's research on every kind of asset and its `CONTRIBUTING.md` (2026-10-27).
>
> **This repo is public.** Other projects are named by their role. Their files, ids, measurements of private hardware and schedules are left out; a source is named by what it is and its date. The lead's words are quoted where they rule.

---

## The current picture (for the lead)

- **Yes: skins, eyes and makeup live here** — makeup meaning everything from simple face makeup to film effects (scars, wounds, bruises, blemishes, tattoos, dirt, blood), on the whole body. The lead ruled it on 2026-10-25 in the platform's research: these are *made outside Studio*, *put in the Asset Library or Matter Library*, and *refined in Studio with simple controls* (§Resolved). That research placed **skin, eyes and makeup in this library**, and **hair's colour** here with its groom in the Asset Library. The Asset Workshop's research of 2026-10-27 adds that **cloth and hair colour are Matter's**. Until today none of this was written in this repo.
- **What makes them look great, largest gain first** (Pass 2, each seen by the lead in the platform's look tests unless marked):
  1. **A real-looking skin picture.** A scanned research-only skin on the same body was the largest single gain (*"WAY better"*). It can never ship, so the library's answer is the synthetic sets (judged 2026-10-26: freckles re-made *"better"*, veins and marks *"plausable"*).
  2. **The shine maps: roughness, cavity, a normal map.** "Plastic" is the even sheen, not the colour; raising shine strength alone did nothing visible. That is *Skin Maps Beyond Colour* — the library's, un-parked 2026-10-26, and the next phase.
  3. **The eyes' wet dome and a believable iris.** An iris on the cornea's curve carries a catch-light (*"YES much more alive"*). The dome is the platform's eye geometry; the iris pictures and the eye master are the library's.
  4. **Denser geometry where the eye looks** (ears, lips, eyelids, hands): OMF's render body, which the library meets with a re-bake (the 2026-10-26 rule: author in 3D, bake per layout).
  5. **A shadowed scene to judge in.** The library's rig has no shadows, so **its sheet cannot show plastic**. Character materials are judged in a shadowed look-dev scene in Studio, and the rig keeps its job: checking that the tools agree.
- **One shape for every kind** (Pass 3, borrowed from the Workshop): **the spec · what it is made on · the maker · the finish · the guide.** Only the first three change by kind. Skins have all five in a first form; eyes have three; makeup has none.
- **How others take part** (Pass 5): today, a **skin map** (painted, or made by a maker) and **maker settings**; after the phases, an **iris structure**, a **makeup piece painted on the body in Blender**, and **hair colours**. The rules are the same for every kind: CC0 only, no photograph or scan of a person, no whole AI-made map, provenance for every input, made in 3D.
- **Suggested order** (Pass 6, for the lead to cut): *Skin Maps Beyond Colour* → *Synthetic Skin Sets* → *Eyes in the Shader* → *Skin Layers* (makeup and marks, whole body) → *Hair Colour by Region*. Alongside the first: **a short participation page**, a lead-directed `/quick-fix`, not a phase.

---

## Pass 1 — What exists today, per kind (audit, 2026-10-27)

**Examined:** `MatterLibrary/materials/character/`, the fit set, the makers under `tools/converters/fit/`, `SkinMaps.md`, `CONTRIBUTING.md` §3.1, the Roadmap's character seeds.

- **F-CMT-1 — By kind:**

  | Kind | What ships or is drafted | Made by | A contributor's path today | Missing |
  |---|---|---|---|---|
  | **Skin** | six tones (`Skin_Fitzpatrick*`, Phase21); 15 synthetic drafts (three tones × five layer sets) | `gen_skin_maps.py`; `gen_synth_skin.py` (pigment maps, 3D) | **yes:** a picture on hm08's atlas, calibrated by `gen_skin_maps.py --picture` (`SkinMaps.md`) | shine maps (no contract input yet); several structures per tone; the six layout pictures carried onto the body (`SkinMaps.md` Todo) |
  | **Lips · nails** | six of each, paired to the tones | the skin maker; constants | through the skin | — |
  | **Eyes** | `Eye_Natural`, `Eye_Green` (MakeHuman's pictures); 10 synthetic drafts | `gen_synth_eyes.py` | **partly:** `CONTRIBUTING.md` §3.1 covers "an eye" as a painted picture; **no eye spec** | colour in the master (every colourway is a picture today); a bloodshot amount; an eye spec |
  | **Teeth · gums · tongue** | one each | constants on their part meshes | §3.1 | — |
  | **Hair colour** | `Hair_DarkBrown`, `Hair_Natural`, on the Hair master | judgement | as any material | colour per region (lashes darker than the scalp) |
  | **Makeup and marks** | none as articles. The synthetic test set carries freckles, veins and marks **as whole skins** (F-SYN-3) | `gen_synth_skin.py` layers | **none** | a placed layer: a mask on the body plus a few deltas, which the contract cannot carry (`LCDSchema.md` overlays tile at the article's scale) |

- **F-CMT-2 — The rules a contributor already meets are spread over four places.** They are `CONTRIBUTING.md` §2–3.1, `SkinMaps.md` (licence, photographs, AI, calibration, layout, 3D authoring), the Glossary (*Character material*, *Part mesh*, *Fit set*) and the research rulings. Nothing names the kinds in one place, or says which can be contributed yet.

## Pass 2 — What the platform's character research and OMF taught, carried by lever (2026-10-27)

**Examined:** as in the header. Each row names whose the lever is; "the library's" means it is carried here.

- **F-CMT-3 — The levers, and what each asks of this library:**

  | Lever | What was seen | Whose | What it asks here |
  |---|---|---|---|
  | **A real skin picture** | a scanned research-only skin on our body: the largest gain, *"WAY better"* | the library (the source) | **synthetic sets** with no person in them (`261026_R_SyntheticSkinAndEyes.md`); the scan stays a comparison bar, never shipped |
  | **Shine** | raising shine strength alone: invisible. The lever is **roughness + cavity**, plus a face normal for wrinkles | the library | *Skin Maps Beyond Colour* (un-parked, RD-SYN-3) |
  | **A face picture of its own (4K)** | more detail only in a close-up, and only with a normal or cavity map, not with colour alone | OMF (the render body's layout) + the library (the bake) | after *Beyond Colour*; met by a re-bake (the 3D-authoring rule) |
  | **A different skin scatter model** | redder skin and mirror-sharp highlights: **not a switch**, master work with its own diagnosis | the library (the Subsurface master) | a candidate question for *Beyond Colour*, not a lever to flip |
  | **An orange band under brow and fringe** | the scatter's colour, unconfirmed | the library (the master) | a check owed to the look-dev scene |
  | **The eyes' wet dome** | a crisp catch-light, *"YES much more alive"*; no master change | the platform (eye geometry) | nothing; the library's iris pictures must read well on it |
  | **A real iris** | today's MakeHuman pictures draw the iris **red, not brown** | the library | the synthetic irises (warm whites, round 3, *"better"*); colour in the master |
  | **Lash colour** | lashes drawn the scalp's colour read wrong; their own darker colour fixed it | the library (hair colour) | colour by region |
  | **Strand hair** | strands read as hair, cards as a drawing of hair (*"yes strands read better"*) | the Asset Library / Workshop (the groom) | its pigment only |
  | **The renderer's anti-aliasing** | a temporal method cleared the skin's speckle | the platform | nothing |
  | **The light to judge in** | no character had ever been judged in shadowed light; a fixed look-dev scene was built | the platform (the scene) | **judge character materials there**; the rig's sheet stays a tool-agreement check |
  | **Author in 3D, bake per layout** | ruled 2026-10-26 (`SkinMaps.md`) | the library | every maker works on the body, not the layout |
  | **A test bench of real body shapes** | one round, one scorecard row per character, the lead's verdict verbatim | OMF + the platform | `rig.py --character --body` (offered); verdict rows in batch form (done) |

- **F-CMT-4 — How every leading character system builds skin and makeup** (the platform's research, from public documentation of four systems): **an ordered stack of layers, each a mask plus a few parameters, baked into one texture set per character; only what changes over time stays live.** Cosmetic slots (foundation, cheeks, eyes, lips) plus a few FX slots (scars, wounds, blemishes, tattoos, dirt, blood) is the common pattern. **The closest precedent on our own mesh is MakeHuman's (MPFB's) ink layer:** a picture on a focus area of the body, painted in Blender.
- **F-CMT-5 — Where that leaves the work.** The **pieces** (a skin, an iris, a scar) are library articles. **The stack and its bake** (which pieces a character wears, at what amounts, per mark) is the consumer's. The lead ruled it a cache, never authored in Studio. So the library defines what a piece **is**, and the platform defines how a character **wears** pieces.

## Pass 3 — One shape for every kind (design, 2026-10-27)

**Borrowed from the Asset Workshop's research of the same day**, which found that every kind of asset needs the same five things and that only the first three change by kind.

- **F-CMT-6 — The five things, for a character material:**

  | # | Thing | What it is here | Skin today |
  |---|---|---|---|
  | 1 | **The spec** | what one piece is: its inputs, what it must and must not show, its rules | `SkinMaps.md` ✓ |
  | 2 | **What it is made on** | the part mesh and its layout (`MakeHuman_Body_v01`, `MakeHuman_Eyes_v01`); made **in 3D**, baked per layout | ✓ (the bake inputs still partly on the layout, `SkinMaps.md` Todo) |
  | 3 | **The maker** | a script under `tools/converters/fit/` for made pieces, or a Blender path for painted ones, with provenance for every input | ✓ two makers; no Blender path |
  | 4 | **The finish** | the recipe gate (G8 checks every UV island) → the rig on the character (the tools agree) → a look picture in the shadowed scene → **a verdict row in the lead's words** → draft until approved | ✓ except the shadowed scene |
  | 5 | **The guide** | a `CONTRIBUTING.md` section and the spec's *How to make one* | ✓ for a painted picture; nothing for a made one |

- **F-CMT-7 — What the library does not own** (each named so a contributor is not sent the wrong way):
  - the character's stack, its bake and the controls in Studio: the platform;
  - eye geometry (the wet dome, shells): the platform;
  - hair grooms: the Asset Library, through the Asset Workshop;
  - body shape and the render body: OMF.
  - **The Blender kit** for painting a piece on the body is unassigned (Q-CMT-2).

## Pass 4 — Each kind, sketched (design, 2026-10-27)

**These are proposals for discovery.** The controls are the platform research's starting list, which the lead ruled the starting list on 2026-10-25.

- **Skin, the person.**
  - **One piece is** a pigment-map set per tone, **several structures per tone** (two characters of one tone do not share a face), plus the shine set from *Beyond Colour*: roughness, normal, cavity and thickness.
  - **Controls in Studio:** tone · redness · freckles · age (wrinkle depth) · pores · oiliness · wetness. The first six are baked and wetness stays live.
  - **Contributors bring** maker settings or a new structure seed (reviewed as code), or a painted picture (layout-bound, `SkinMaps.md`).
- **Eyes.**
  - **One piece is** a greyscale iris structure (a handful: smooth "brown" types and fibrous "blue" types), a sclera with a vessel mask, and **colour set in the master**: two iris colours and a blend, the limbal ring, the pupil, a bloodshot amount, a sclera tint, wetness, each eye on its own.
  - **Contributors bring** an iris structure picture.
  - **Needs:** master inputs (a contract change, so a new Unreal runtime) and an eye spec.
- **Makeup and marks: one kind, two families.**
  - **One piece is** a **mask placed on the body**, made in 3D or on a focus area and baked per layout, plus **per-channel changes**: colour or pigment (melanin, blood), roughness (finish), normal (relief) and depth (a vein lies under the skin).
  - **Cosmetic pieces:** foundation, cheeks, eyes, lips. Their controls are colour · amount · finish (matte ↔ gloss).
  - **FX pieces:** scar, wound, bruise, blemish, mole, freckle field, vein field, tattoo, dirt, blood, sweat. Their controls add relief · fresh ↔ healed · wet.
  - **Anywhere on the body, and per mark** (both ruled 2026-10-25).
  - **Contributors bring** a mask painted on the body in Blender plus its settings, or a generator script.
  - **Needs:** a placed-layer mechanism in the library's contract (the contract has none, F-SYN-3), and the platform's stack bake.
  - The test set's freckles, veins and marks are the first examples, carried as whole skins until then.
  - **"Lack any depth"** (the lead on the test marks, 2026-10-26) is answered by the normal and roughness channels, which arrive with *Beyond Colour*.
- **Hair colour.**
  - **One piece is** a pigment: melanin · redness · dye · grey · shine, with **colour by region** (brows and lashes differ from the scalp).
  - **Stubble and body hair** are a skin layer (ruled 2026-10-25), so they are makeup-and-marks pieces.
  - The groom is the Asset Library's.
- **Lips, nails, teeth, mouth:** exist; they follow the skin's tone and its shine maps.

## Pass 5 — For someone who wants to take part (design, 2026-10-27)

- **F-CMT-8 — Three ways to take part:**
  - **an artist** paints a piece in Blender;
  - **a technical artist** writes or tunes a maker;
  - **a reviewer** judges a piece on a character and writes a verdict row.
- **The rules every piece keeps,** already ruled and today scattered (F-CMT-2):
  - **CC0 only** (RD-RO-2);
  - **no photograph or scan of a person** without documented rights and consent (RD-SKM-2);
  - **AI never makes a whole map**; it may make a tone-free detail layer and content such as tattoo designs (RD-SKM-5, RD-SYN-1);
  - **made in 3D, baked per layout**; a painted picture is accepted bound to its layout (2026-10-26);
  - provenance for every input;
  - every new piece is a **draft** until the maintainer keeps it.
- **What can be brought, and when:**

  | Kind | Today | After |
  |---|---|---|
  | Skin | a painted picture (layout-bound) · maker settings | *Beyond Colour*: shine maps · *Synthetic Skin Sets*: a structure seed |
  | Eyes | a painted eye picture | *Eyes in the Shader*: an iris structure |
  | Makeup and marks | — | *Skin Layers*: a piece painted on the body, or a generator |
  | Hair colour | a hair material | *Hair Colour by Region* |

- **Where it would be written** (a durable doc, owed only on the lead's word):
  - one entry page beside `SkinMaps.md`, `docs/specs/Authoring/CharacterMaterials.md`, listing the kinds, their status, the shared rules and the five-thing shape;
  - `CONTRIBUTING.md` §3.1 pointing at it;
  - each kind's own spec when its phase builds it (an eye spec with *Eyes in the Shader*, a makeup spec with *Skin Layers*).

## Pass 6 — A suggested order (2026-10-27)

**Research output, for the lead to cut. Unnumbered; each a phase with an Outcome, except the first line.**

- **Character Materials page** — a lead-directed `/quick-fix`, not a phase. *Outcome:* a contributor finds every kind of character material, what each needs, and which can be made today, on one page.
- **Skin Maps Beyond Colour** (seeded) — *Outcome:* up close, skin catches the light as real skin does (oilier and drier areas, creases, light through ears and fingers). Roughness first, then normal, cavity, thickness. **It also gives the marks their depth.**
- **Synthetic Skin Sets** (seeded) — *Outcome:* every tone has several real-looking skins with no person in them, from one maker. It carries the six layout pictures onto the body (the `SkinMaps.md` Todo) and judges tone VI's marks.
- **Eyes in the Shader** (seeded) — *Outcome:* a Creator sets an eye's colours, ring and redness with a few controls over a handful of iris structures.
- **Skin Layers** (seeded; **proposed widening**) — *Outcome:* a Creator puts makeup and marks, from blush to film scars, tattoos, dirt and blood, **anywhere on the body and per mark**, each a library piece, without a new skin per combination. It pairs with the platform's stack bake; the library's half is the placed-layer contract and the first pieces.
- **Hair Colour by Region** (new, small) — *Outcome:* brows and lashes take their own colour from the same hair pigment, and stubble and body hair arrive as skin layers.

**Waits outside the library:** the shadowed look-dev scene as a durable place to judge (the platform); OMF's render body (a re-bake here); the stack bake and controls (the platform).

## Open questions (plain)

| Id | Question | Recommendation |
|---|---|---|
| **Q-CMT-1** | **Is the ownership read right?** Skins, eyes, makeup and marks (film effects included) and hair colour are this library's pieces; the groom is the Asset Library's; how a character wears pieces (the stack, its bake, the Studio controls) is the platform's. | **Yes** — it is the 2026-10-25 ruling as the platform's research read it, and the Workshop's of 2026-10-27. |
| **Q-CMT-2** | **Who owns the Blender kit for painting a piece on the body** (a scar mask, a tattoo placement)? | **This library.** It already ships a Blender add-on (`blender/`), and the pieces are its articles; the Workshop's tools make assets for the Asset Library. |
| **Q-CMT-3** | **Cut the order** (Pass 6). | Beyond Colour first: it is the largest gain left, and it gives the marks their depth. |
| **Q-CMT-4** | **Write the participation page now** (Pass 5's *where it would be written*)? | **Yes, as a quick fix** once Q-CMT-1 is answered: it states only what is ruled, and marks the rest *(planned)*. |
| **Q-CMT-5** | **Is the shadowed look-dev scene the library's verdict surface for character materials** (asking the platform for a way to open a draft in it), with the rig kept for tool agreement? | **Yes.** The rig cannot show plastic; a verdict made where plastic cannot be seen is not a verdict on it. |

## Resolved

Rulings made in other projects' sessions that bind this library, **recorded here by date and content** (`LOCAL_DELTAS.md` §Separation), not by those projects' ids:

- **2026-10-25 — Character materials are made outside Studio and live in the libraries; Studio refines them.** The lead, verbatim: *"we want Studi to primarly be a consumer of assets, not a craetor of assets … Ideally people would make these things in blender, bring them in to studio and just refine it with simple controls … hair solutions that are crafted and put in the asset library or matter library ( like the skins, and the wardrobe etc) and then in studio, you pull it in a refine it for the situation"*. The platform's research read it as: skin, eyes and makeup in this library; hair's groom in the Asset Library and its colour here.
- **2026-10-25 — The human's layers are Skins · Eyes · Makeup;** makeup runs *"from … simple face makup to film makup like scars, blumishes"*; *"simple yet powerful"*; *"pipelines to allow others to continutbe"*. **Makeup changes from mark to mark,** and *"makeup should function the same accross the entrie body"*. **The proposed control lists are the starting list.**
- **2026-10-25 — One hair approach:** the groom (strands) is the authored thing, cards are made from it, and stubble and body hair are a layer of the skin.
- **2026-10-27 — Hair colour and cloth are Matter's** (the lead, in the Asset Workshop's research of that day).
- **Already here:** author in 3D, bake per layout (2026-10-26, `SkinMaps.md`); *Skin Maps Beyond Colour* un-parked (RD-SYN-3); AI makes no whole skin map (RD-SYN-1).

## Words this doc uses that the Glossary does not hold yet

- **piece** (one makeup-and-marks article);
- **placed layer** (a mask on the body's layout plus channel changes);
- **the stack** (the pieces a character wears, in order, with amounts);
- **look-dev scene** (the platform's shadowed scene for judging characters).

Each would be fixed in the Glossary by the phase that first builds it.

## Status

- **Passes:** 6 (2026-10-27).
  - Pass 1: the audit, per kind.
  - Pass 2: the levers learned elsewhere, and whose each is.
  - Pass 3: one shape for every kind.
  - Pass 4: each kind sketched.
  - Pass 5: how others take part.
  - Pass 6: a suggested order.
- **Current direction:**
  - The library makes the pieces (skin, eyes, makeup and marks, hair colour); the platform makes how a character wears them.
  - The largest gain left is the shine maps (*Beyond Colour*).
  - Participation needs one entry page now and a spec per kind as each is built.
- **Recorded:** four rulings made elsewhere (§Resolved).
- **Open with the lead:** Q-CMT-1 … 5.
- **▶ Next:** the lead's answers. Then, on the lead's word:
  - the participation page as a `/quick-fix` (Q-CMT-4);
  - `/discovery Skin Maps Beyond Colour`.

  Resume with `/research CharacterMaterials`.
