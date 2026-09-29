# Phase09 — Hair and Eye Masters

**Status:** SEEDED (2026-09-29; phase doc exists; discovery has not opened). **Numbered Phase09 by the lead, 2026-09-29** (*"yes push it, make it Phase09"*); seeded unnumbered the same day.
- **Seeded** from `docs/Planning/Research/260929_R_CharacterMaps.md` (Passes 1–8, rulings MAP-RD1–RD6), on the lead's word:
  *"yes 1, seed the phase"*.
- **The deliberate gate:** this is a pointer-shell. It opens only by the lead's `/discovery`; nothing here is a plan.

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

_(numbered passes accrue here: examined → finding → decision / hypothesis / open question)_

## Discovery Status

- **Passes captured:** —
- **Current working direction:** —
- **Open decisions:** —
- **Checks to carry forward:** —

## Execution Log

_(populated during execution)_
