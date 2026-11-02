# Research — Does an AI-made skin still fit every character?

**Status:** OPEN — parked 2026-11-02 at the lead's ask (*"I don't want to stop this flow right now.. but we do need to capture this"*), raised while Phase27's execute was live. Not yet a ruling. To be decided **before Phase28 starts**, and before Phase27's structure step (27.3) fixes what the body's map carries.

## The question

The lead: *"the idea of skinmaps is that we could apply them to any of our mesh... this is sounding like each character needs a bespoke skin"*.

## What is known (2026-11-02)

- **The fit carries over.** Every skin map is in hm08's UV layout (RD-SKM-1), shared by every character built on it; a different build moves the layout with the mesh, so a lip stays on the lip and a freckle on the shoulder. A map made on the rig's character fits any hm08 character.
- **The painted shading does not.** The image model's picture carries light and shadow painted for the body it was drawn on: the shoulder blades, the spine's groove, the fold under the breast, muscle contours. On a heavier or a male build those painted shadows sit in the wrong place, or where that body has no such shape. That is what would make a skin look bespoke.
- **What carries over cleanly:** tone, mottling, freckles, moles, flush, fine texture — the skin itself.
- **The spec already rules on it:** `docs/specs/Authoring/SkinMaps.md`, the *Anywhere* row — *"No lighting or shading baked in"* (in force, F-SKM-24).
- **The tension in Phase27:** its first body divided out the light the model painted (27.1.2), which kept the map portable but read less like the original. The lead's target since 27.2.4 is the original picture's look on the character (Phase27 §Execution Log), and 27.2.5 keeps more of the picture's colour (`put --keep-colour`). Some baked shading comes back with it.

## A proposed reading (the agent's, not ruled)

- **A skin is per person, not per mesh.** "A 20-year-old woman's skin" can be worn by any character; which skin suits which character is a choice, not a fit problem.
- **The map carries only the skin** (pigment, marks, texture, flush); **the shape's shading comes from the mesh and the light**, as in a real render. If that reads flat, the fix is in the character's surface detail (the relief map; the finer-mesh ask, Phase27 §Deferred), not in the colour.

## The test that settles it

Put the current AI body skin on a **differently built** hm08 character (a male or heavier shape, same mesh) in the library's Unreal look view, beside the rig's character, and look for shadows in the wrong places. One picture.

## Also open: veins and the body's relief (2026-11-02, the lead's ask)

**What exists (read from the maker, 2026-11-02):**
- **The relief map** (`gen_skin_shine`: the tangent-space normal every skin article wears) carries pores everywhere and the face's lines (forehead, frown, crow's feet, under the eyes, nose to mouth). **No veins, and nothing body-specific** (knuckle and palm creases, elbows, the navel, the soles' texture).
- **Vein colour exists** as a maker layer (`gen_synth_skin` `LAYERS`, the `SynthVeins` / `SynthAll` sets): blood drawn deeper under the skin so it reads blue-violet. Colour only, no relief.
- **The AI chain replaces only the colour** (Phase25, Phase27): an AI skin wears the maker's relief, roughness, cavity and scatter.

**The agent's thinking (not ruled):**
- **Vein colour, short term:** when Phase27's structure step turns the AI colour into pigment, the maker's vein layer still applies (the blood's depth stays the maker's in `compose`'s field join). Watch for doubles: the AI picture may paint veins of its own.
- **Vein colour, long term:** the Roadmap's *Skin Layers* already lists veins among the marks — a library piece placed on the body that works on every character. That matches the portability reading above: the skin carries the person, the marks are pieces.
- **Vein relief** (raised veins on the back of the hand, the forearm, the foot): **no plan anywhere.** Its natural home is the same *Skin Layers* mark, carrying relief as well as colour (Phase26's first pieces are colour only).
- **The body's other relief: also no plan.** Two candidate sources: (a) extend the maker's relief to the body, as it already draws the face's lines; (b) derive relief from the AI picture's fine skin (Phase27's close cameras) — untested.
- **When:** after Phase27's colour is settled, and alongside Phase28, since palm creases and knuckles are where relief matters most. The resolution steps already ordered (2K, a 4K test, then 8K; RD-P25-20) are the natural slot: relief needs the resolution to show.

## Where it binds

Phase27 27.2.5 onward (how much of the picture's colour is kept) · Phase27 27.3 (the structure turns colour into pigment — baked shading would become pigment) · Phase28 (hands and feet) · the person-from-a-brief phase (Phase28 Q-P28-4).
