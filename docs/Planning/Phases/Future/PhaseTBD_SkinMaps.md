# PhaseTBD — Skin Maps

**Status:** SEEDED (2026-10-14) — not numbered. A pointer-shell written by `/research` on the lead's word (*"Seed all the TBD phases we discovered here"*). **The industry survey is done** (`261014_R_SkinMaps.md` Passes 3–4, 2026-10-14). The lead ruled the same day (RD-SKM-2 to RD-SKM-4). The probe (on the laptop) and an exploration of the AI route (Q-SKM-7) come before `/discovery`. **Starting discovery is a deliberate gate, the lead's call, never a slide.**

## Outcome

**A character's skin varies across the body as real skin does,** with lips that blend into the face and redder cheeks and knuckles, in Blender, a USD viewer and Unreal. **Every character built from the approved human mesh wears it.**

## Why this is a phase

Today skin is a flat tone per part, which the lead judged *"pretty terrible in fact (the line between lips and face and no variation)"* (RD-MP-9). Skin maps are made per approved mesh version. Today's mesh is MakeHuman's hm08 on the Manny skeleton (RD-SKM-1), so one set of maps serves every character built from it.

## Scope — as ruled at research (2026-10-14)

The authority until this phase writes its specs: [`261014_R_SkinMaps.md`](../../Research/261014_R_SkinMaps.md) §Resolved and Passes 1–4.

- **A skin map is a fit-set picture for the approved mesh** (F-SKM-10). The skin article stays the substance (tone, scatter, coat, fuzz, pores), so CM2 holds.
- **The colour half needs no contract change:** `base_color_map` on Subsurface exists in every library target (F-SKM-3).
  - **But the six skin articles must be re-assembled to take it:** declare the map, and let the scatter colour follow it (F-SKM-19).
  - The map's normalisation must keep the measured tone as the average (F-SKM-20).
- **Colour is the industry's first map**, and the tiling micro layer is already here (F-SKM-11, F-SKM-13). The maps beyond colour (normal, roughness, cavity, scatter) each need a new input; that is a later question for the phase.
- **The lips can wear the skin article plus the map's lip colour**, which removes the hard line (F-SKM-9).
- **A mesh version is named and recorded,** so each map says which mesh it fits (Q-SKM-4).

## Open questions (settle in research, then here)

- ~~Q-SKM-2~~ → RD-SKM-4: neutral at the genitals and groin.
- ~~Q-SKM-3~~ → the probe runs on the laptop now: today's skin, a MakeHuman atlas (comparison only) and a library-made map.
- ~~Q-SKM-5~~ → RD-SKM-2: library-made or AI-generated, never the photo atlases; the AI route is to be explored.
- ~~Q-SKM-6~~ → RD-SKM-3: one colour map per tone.
- Q-SKM-7: which ships, library-made or AI.
- Q-SKM-4: naming a mesh version.

## Discovery Log

*(empty — `/discovery` fills it, after the research's Pass 3)*
