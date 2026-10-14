# PhaseTBD — Skin Maps

**Status:** SEEDED (2026-10-14) — not numbered. A pointer-shell written by `/research` on the lead's word (*"Seed all the TBD phases we discovered here"*). **Its research is not finished:** the industry survey (`261014_R_SkinMaps.md` Pass 3) comes before `/discovery`. **Starting discovery is a deliberate gate, the lead's call, never a slide.**

## Outcome

**A character's skin varies across the body as real skin does,** with lips that blend into the face and redder cheeks and knuckles, in Blender, a USD viewer and Unreal. **Every character built from the approved human mesh wears it.**

## Why this is a phase

Today skin is a flat tone per part, which the lead judged *"pretty terrible in fact (the line between lips and face and no variation)"* (RD-MP-9). Skin maps are made per approved mesh version. Today's mesh is MakeHuman's hm08 on the Manny skeleton (RD-SKM-1), so one set of maps serves every character built from it.

## Scope — as ruled at research (2026-10-14)

The authority until this phase writes its specs: [`261014_R_SkinMaps.md`](../../Research/261014_R_SkinMaps.md) §Resolved and Passes 1–2.

- **A skin map is a fit-set picture for the approved mesh** (F-SKM-10). The skin article stays the substance (tone, scatter, coat, fuzz, pores), so CM2 holds.
- **The colour half needs no contract change:** `base_color_map` on Subsurface exists in every library target (F-SKM-3). Maps beyond colour (roughness, normal, scatter thickness) are Pass 3's question.
- **The lips can wear the skin article plus the map's lip colour**, which removes the hard line (F-SKM-9).
- **A mesh version is named and recorded,** so each map says which mesh it fits (Q-SKM-4).

## Open questions (settle in research, then here)

- Q-SKM-2: intimate anatomy in the map, or neutral regions; the hosts' content policies, starting with this public repo (F-SKM-6).
- Q-SKM-3: the probe (today's skin against one atlas multiplied in) before or after the survey; it runs on *The Library Service*.
- The survey's questions: `261014_R_SkinMaps.md` Pass 3.

## Discovery Log

*(empty — `/discovery` fills it, after the research's Pass 3)*
