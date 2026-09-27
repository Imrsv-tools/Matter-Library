# Phase07 — Character Materials

**Status:** SEEDED (discovery has not opened).
- **Seeded** 2026-09-27 from `docs/Planning/Research/260927_R_CharacterMaterials_MPFB2.md`, first as an unnumbered phase (CM3).
- **Numbered Phase07 by the lead, 2026-09-27** (CM4), verbatim:
  - *"I would like to get the character materials in as soon as possible after phase 5… Studio is going to be pulling from the matter library and there no character materials in the library at all so they will magenta… I would rather have everything in and 'uncalibrated' yet then a bunch of magenta"*;
  - on the plan: *"yes, We have time so let's just do them in Phase 7 as redefined and we will be good."*
- Library Coverage moved from Phase07 to **Phase08**.
- **This phase runs on this machine straight after Phase05, at the same time as Phase06 on the UE machine.** The platform's character work points Studio at the library once this phase lands (lead, 2026-09-27).
- The handoff to `/discovery` is a deliberate gate the lead opens.

## Outcome

**A character wears real materials from the library (skin in six tones, eyes, mouth and teeth, lips, nails, hair and basic clothing fabrics) in Blender and in a USD viewer, and in Unreal once it is calibrated. None of them shows the missing-material magenta, and every one works on any character, not only the one it was made on.**

Concretely at close:
- the `biological` Domain exists (CM1), with its articles built from recipes like every other article;
- the MakeHuman body shows the full set side by side in the Phase05 rig;
- every article is marked **candidate**, meaning checked in USDLiveView and Blender and awaiting the Unreal column (Phase06). It becomes **approved** once Unreal agrees (research `260926_R_BigPicture_NimbleSetup.md` Pass 8, the momentum rule).

## Why this is a phase

It is one user-facing result: characters get library materials. It carries the calls that are expensive to unwind:
- a new Domain;
- whether layers may carry colour;
- whether hair and eyes get masters of their own;
- where body-specific ("fit") data lives.

It runs before Unreal exists, so any new master or input it adds means rebuilding Phase06's Unreal package. The lead accepts that ("we will need to adjust things once we have the actual UE test rig added"). The way to keep that cheap is to **rule the contract calls early in this phase** and push them, so the UE machine builds against them.

## Scope (to settle at discovery; the research's recommendations, not decisions)

**In:**
- **The `biological` Domain** (`tissue` / `keratin` / `bone`) in `Taxonomy.md`, and wherever the tools list the classes.
- **The status field** (draft / candidate / approved). Phase05 moved it to "Phase07" (Phase05 doc, F4). This is now the first phase that ships uncalibrated materials, so it needs the field.
- **Skin ×6:** `Skin_FitzpatrickI…VI` on the Subsurface master, from Physically Based values plus MPFB2's CC0 roughness and pore settings, with one tiling pore overlay (research Pass 6d). Keep `subsurface_color` equal to the base colour, or unset, so Blender matches (Pass 8a). **This comes first: it needs no contract change.**
- **Eyes and mouth, done properly, no stand-ins** (lead: "we have time").
  - The platform's eye and mouth are each one mesh painted with several materials: sclera plus iris; teeth plus gums plus tongue.
  - They need either the **fit set** (CM-Q6: region masks on the MakeHuman body, designed here) or the platform splitting those meshes (CM-Q9). Decide at discovery.
- **The other substances:** lip and gum/tongue mucosa, nail, sclera, cornea, iris, enamel, hair fibre with brows and lashes, and a few clothing fabrics (cotton, denim, leather) pulled forward from Phase08's list (research Pass 6a).
- **Skin realism inputs:** subsurface scatter anisotropy, fuzz, and coat (carrier C2, pulled forward from Phase08's question 3). Each gets its matching Blender proxy input **in the same step** (research Pass 8b).
- **The contract calls:**
  - a colour channel on layers (CM-Q5), which also answers the colour half of Phase08's question 10;
  - Hair master or Masked cards (CM-Q3);
  - Eye master or a composed eye (CM-Q4);
  - a Skin master only if the rig shows marble and skin need different renderer settings (CM-Q10).
- **The hand-off to the platform:** `PlatformDependencies.md` M1. Studio routes materials by class, so it needs either the new classes added to its routing table or the per-article master token (P4).

**Not now:**
- Calibrating against Unreal: Phase06 builds the Unreal column; these articles are re-judged when it arrives.
- The platform's hair and garment meshes, and their card and garment atlases: these are mesh assets (research Pass 6b).
- The platform's slot binding and character generator (platform side).
- CC-BY MakeHuman packs (CM-Q8: local testing only, never committed).
- The volume build and the nightly loop: Phase08.

## Open questions (carried from the research)

CM-Q3, CM-Q4, CM-Q5, CM-Q6, CM-Q8, CM-Q9, CM-Q10: see the research doc's §Open questions. **Discovery reads the research's §Resolved (CM1–CM4) and Pass 8 first.**

## Sources (pointers, not copies)

- `docs/Planning/Research/260927_R_CharacterMaterials_MPFB2.md`: the whole thread.
- `docs/Planning/Phases/Future/Phase08_LibraryCoverage.md`: questions 3 (carriers) and 10 (layer colour).
- `docs/Planning/Phases/Future/Phase06_UnrealTestRuntime.md`: the masters this phase's contract calls touch.
- `docs/specs/Ontology/{Taxonomy,MasterSet}.md` · `docs/specs/Contract/LCDSchema.md` · `docs/Planning/PlatformDependencies.md` (M1, P4).

## Discovery Log

_(numbered passes accrue here: examined → finding → decision / hypothesis / open question)_

## Discovery Status

- **Passes captured:** — (seed only)

## Execution Log

_(populated during execution)_
