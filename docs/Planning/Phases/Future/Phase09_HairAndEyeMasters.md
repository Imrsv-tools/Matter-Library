# Phase09 — Hair and Eye Masters

**Status:** DISCOVERY (opened 2026-09-29 by the lead's `/discovery P9`; Pass 1 captured; **the Brief waits on the Phase06 plan**, lead: *"phase 6 plan is about to be available to review"*). **Numbered Phase09 by the lead, 2026-09-29** (*"yes push it, make it Phase09"*); seeded unnumbered the same day.
- **Seeded** from `docs/Planning/Research/260929_R_CharacterMaps.md` (Passes 1–8, rulings MAP-RD1–RD6), on the lead's word:
  *"yes 1, seed the phase"*.
- **The deliberate gate:** passed — the lead opened discovery on 2026-09-29.

## Outcome

**A Creator's character has hair that keeps its strands and takes any colour on any hairstyle, and eyes that look real —
a photographed iris in the colour they pick, wet, and in Studio shaded by Unreal's own eye model — the same in Blender, a
USD viewer and Studio.**

Concretely (the research's reading; discovery confirms or changes it):
- **One new input kind on an article: a picture held by the library in a mesh family's own layout, sampled on the mesh's
  `st` outside `place2d`** — the mechanism the cut-out map already uses (`LCDSchema.md` §Cut-out map). One kind serves both
  parts (MAP-F11).
- **Hair:** the `Hair` article takes the hairstyle's picture, **prepared by the library** as a normalised light-and-dark
  structure, and uses it to **shade its own light colour** (MODULATE), so the tint reaches every colour on every style, and
  brows and lashes take it too (MAP-RD3, MAP-F2, MAP-F3). Answers Matter-Library#3 and the HS asks the library's way.
- **Eyes:** the whole eyeball picture from the CC0 MakeHuman pack (iris, limbal ring, sclera veins) in the library, on the
  sclera, iris and pupil parts; separate pictures per colour (the lead's lean; two real photographs behind nine colours,
  MAP-F9); coat for the wet look (MAP-RD5).
- **An `Eye` master token** (the 9th) whose MaterialX graph is the composed eye and whose settings row gives Unreal's eye
  shading, with no new eye geometry (MAP-RD6; reopens Phase07's D-E).

## Why this is a phase

One contract addition carries it (a new input kind, and a new master token), and every tool that knows the inputs and the
tokens moves with it: `LCDSchema.md`, `MasterSet.md`, the assembler, the recipe schema, the validator, the Blender masters,
the rig and its job format (Phase08 F-P08-2 counted the token in eight sites). Two consumers build against it: the
platform's Studio and this library's own Unreal masters (Phase06 / Unreal Reference Masters, P20). It started as an eye
`/quick-fix` and stopped at its balloon check for exactly this reason (research Pass 8).

## Scope

**In:**
- The picture input kind, its contract text and its tool support.
- The hair picture: the library's preparation tool, the prepared pictures for the CC0 hairstyles (and brows, lashes), the
  `Hair` graph reading it as MODULATE.
- The eye picture articles (sclera, iris per colour, pupil) with coat, on the rig's character with an eye matching
  Studio's (no cornea shell, MAP-F12).
- The `Eye` token and its settings row; its Unreal side where the library's Unreal masters are built.
- The hand-offs: `PlatformDependencies.md` (Studio's Hair master multiplies instead of replacing; the eye parts bound to
  the new articles; the `Eye` master until P20 lands).

**Out:**
- **Strands** (MAP-RD4): their own phase, on the Roadmap's *Hair That Reads as Hair* entry.
- **New eye geometry** (cornea shell, lid shadow, tear line): *"adding mesh is not the time"* (MAP-RD6).
- **Skin pictures** (MAP-RD2): skin stays general; its lift is P16 / P20 and the glow's calibration.

## Open questions (settle during this phase)

- MAP-Q5 — separate eye pictures per colour: which colours, from the two photographs (MAP-F9).
- MAP-Q12 — one `Eye` article on all three eye parts, or three articles on the `Eye` master (Unreal's eye model, from
  knowledge: one eyeball surface).
- MAP-Q13 — who builds the `Eye` master's Unreal side, and when Studio gets it.
- The input's name and where the prepared pictures live in the library, keyed to their mesh family (HS-Q6; MAP-RD1: the
  library holds every asset).
- How a binding names its picture (a path into the library, a setting like `cutout_map`), and what an exported character
  carries (MAP-RD1: names and settings only).

## Notes

- Sources: `docs/Planning/Research/260929_R_CharacterMaps.md` · `260928_R_HairStrandColourMap.md` (HS) ·
  `260928_R_HairAndNailRendering.md` · `Phase07_CharacterMaterials.md` (L2, D-E) · `Phase08_CharacterAppearance.md` ·
  `docs/specs/Contract/LCDSchema.md` §Cut-out map · `docs/Planning/PlatformDependencies.md` (P16–P18, P20, M3).

## Discovery Log

### Pass 1 (2026-09-29): the product docs, top-down, read against the Outcome

**Examined:** `_Architecture.md` (the LCD restatement of 2026-09-28, Decisions of record) · `MasterSet.md` (tokens, the Hair
row, the settings table, the modulator rule) · `LCDSchema.md` (§Author tier, §Carrier rule, §Cut-out map, §Notes) ·
`NamingConventions.md` · the research thread (`260929_R_CharacterMaps.md` whole; HS; HairAndNail; CM) · Phase07 and Phase08
(decisions that bind, deferral ledgers) · `260929_R_UnrealTestRuntimeHere.md` and its spike. **Learnings:** Storm S9,
Blender B1, B5, MaterialX M4 apply. **Tree:** every `cutout_map` site (the precedent: `assemble_mtlx.py`,
`recipe.schema.json`, `validate_material.py`, `load_article.py`, `job.py`, `JOB_FORMAT.md`, `blender_render.py`,
`build_character.py`, the two hair recipes, three specs and the Glossary); the gates that enumerate `MatterLibrary/textures/`;
the rig's cast. **Tree grep for the phase's own names** (`base_color_map`, `strand_color_map`, `"Eye"`, `ML_Eye`): **nothing
built.** **External:** Epic, *Shading Models* (5.8). **This machine has no Unreal** (no engine, no probe folder); the UE
machine is the other one (UR-D1).

**Findings:**
- **F-P09-1 — The spec already expects this phase.** `_Architecture.md` lists Phase07's D-E (*"no `Eye` master"*) under
  **Reevaluate**, argued on the superseded LCD wording; the restated principle (*"we use the master materails to lean in on
  the egines BEST qaulities"*) is what MAP-RD6 applies. MasterSet's Hair row calls itself **interim** until *"mesh-supplied
  card maps"*.
- **F-P09-2 — MasterSet's Hair settings row is stale.** It says the shading model is *"hair (… Unreal's Scatter /
  Backlit)"*. The platform's sitting overturned that on the lead's eye (*"turn off anything specular, gloss, reflection,
  glow, highlight"*, then *"OK! That is HAIR!"*): matte, default lit, coloured by the picture. HS-Q3 is therefore answered;
  the row is corrected with the input, the hair shading model kept for strands.
- **F-P09-3 — Where the eye picture lives is answered: in the library, supplied at binding, never inside the article.**
  Phase08's binding list: *"CM2 / D1 (substance only; mesh-bound pictures are never in an article)"*; MAP-RD1: *"the libery
  has all the assets anyone needs"*. So the eye articles stay general (a sclera, an iris, a pupil) and **the eye colour is
  which picture the binding supplies** — the same as a hairstyle's picture. The lead's *"seperate pictures"* is nine pictures
  in the library, from two photographs (MAP-F9).
- **F-P09-4 — The one input, named by the spec's own rule.** `LCDSchema.md` §Notes: *"Names use OpenPBR-aligned terms"*.
  The input multiplies OpenPBR's `base_color`, so **`base_color_map`**: `base = base_color_const × base_color_map ×
  base_color_tint`, sampled on the mesh's `st` outside `place2d`, an empty map reading 1. The platform's
  `strand_color_map` was provisional until the library rules (HS-Q6), so the platform renames it. It is not an overlay or
  a maskset (packed data), so the modulator rule is untouched; the phase says so where the rule is stated.
- **F-P09-5 — On a Subsurface article the picture vanishes unless the subsurface colour follows it.** MaterialX M4: base
  detail keeps only `1 − subsurface_weight` of its strength; `Sclera_Natural` is at weight 1.0. So `subsurface_color` is
  connected to the modulated base, as the Hair graph already does.
- **F-P09-6 — The pictures need a home in the texture tree, and the gate reads every file there.** `_Architecture.md`
  §Textures names two roots, `base/` (by matter) and `shared/` (layers); a picture drawn on a mesh family's layout is
  neither. The **compression lane** classifies every PNG under `MatterLibrary/textures/` by a role token in its name
  (`basecolor`, `opacity`, …) or fails. Candidate: a third root `textures/fit/<family>/…` with role-token names and scale
  tag `sUKN` (the grammar allows it on a base texture, not on a layer). The Glossary uses *fit* under *Cut-out map*; a term
  for the set is fixed there first.
- **F-P09-7 — The rig cannot show the defect this phase fixes, as it stands.**
  - Its hair is **`bob02`, the one blonde style** (MAP-F2): the dark-picture tint problem does not appear on it. Studio's
    built-in hair is `short02`.
  - Its eye parts' `st` is rescaled to metres; they must keep the source atlas, as its cut-out parts do.
  - It binds a cornea shell that Studio does not have (MAP-F12).
  - Its character job takes defaults only (F-P08-4), so the tint is judged in Blender, as Phase08 did.
- **F-P09-8 — Unreal's eye model is tied to its own eye geometry.** Epic: *"This Shading Model is highly technical and has
  been developed in a way that produces very strong dependencies between the shader code, the Material, the shape of the
  geometry, and its UV layout"*; it recommends the Digital Humans eye geometry and material *"as-is"*. With no new eye mesh
  (MAP-RD6), an `Eye` master on MakeHuman's eyeball is **unproven**, and proving it needs Unreal, which is on the UE machine
  (Phase06's). → Q-P09-1.
- **F-P09-9 — Phase06 is being planned on the UE machine** (lead, 2026-09-29). The `Eye` master's Unreal side, and when
  Studio renders with the library's masters (P20), depend on it. The Brief is written after reading that plan.

**Forks tested and closed** (none reached the lead): *where the eye picture lives* → D1 / CM2 + MAP-RD1 (F-P09-3) · *the
input's name* → LCDSchema §Notes + HS-Q6 (F-P09-4) · *the Hair shading model* → the lead's ruling at the platform's sitting
(F-P09-2) · *whether the library holds the cut-outs too* → MAP-RD1 (yes).

## Discovery Status

- **Passes captured:** 1 (2026-09-29).
- **Current working direction:** one input, `base_color_map`, sampled on the mesh's own UVs and multiplied into the base
  colour; the library prepares and holds the pictures (hair structure and cut-outs for the CC0 styles; nine eye pictures)
  under a `fit` root; hair re-authored to read it and corrected to matte; the eye articles take it (the sclera's subsurface
  colour following); the rig on `short02`, eyes on their atlas, no cornea; the `Eye` master per Q-P09-1.
- **Open decisions:** **Q-P09-1 — the `Eye` master, given F-P09-8:** (a) a disposable spike on the UE machine first —
  does Unreal's eye model work on MakeHuman's eyeball with our picture? — and the token only if it does; (b) defer the
  `Eye` master until eye geometry is in scope; (c) the token and settings row now, the Unreal side whenever it can be built.
  Recommendation: **(a)**, placed by the Phase06 plan.
- **Checks to carry forward:** read the Phase06 plan (F-P09-9) before the Brief · baseline `check_exporter.sh` before
  touching `tools/conformance/` · the compression lane on the new pictures · regenerate the Blender library and run
  `check_asset_library.sh`.

## Execution Log

_(populated during execution)_
