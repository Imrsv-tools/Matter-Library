# Phase29 — Object Opacity in the Masters

**Status:** SEEDED (2026-11-09, by `/research` on the lead's word: *"do both — quick-fix the ledger row, then seed the phase... We are paused on all the skin work right now... this will be the next phase we do"*, RD-POA-1). **Runs next**, ahead of the paused skin work (Phase28 included). Discovery is a deliberate gate the lead opens (`/discovery P29`). This doc is a pointer-shell; discovery fills it.

## Outcome

**A Character, Prop or Set drawn with the library's materials fades in and out in Unreal: part-faded, it dissolves into what is behind it and never turns to glass, so two versions of one character cross-fade cleanly. While it is fully there, it draws and costs exactly what it does today.**

*Who it is for:* the platform's Creators, who key an object's Opacity on the timeline (`PlatformDependencies.md` M15). Other USD apps see a clean swap. No article reads the value, so Blender and Storm are untouched.

## Source

[`../Research/261105_R_PlatformObjectOpacityAsks.md`](../Research/261105_R_PlatformObjectOpacityAsks.md):
- Pass 1 — the platform's reports and asks (R-POA-1 … 3, Q-POA-1 … 4);
- Pass 2 — the library's reading (F-POA-1 … 8). Its proposals are this seed's scope. **They are not ruled:** discovery confirms or cuts each one.

## Scope (seed — discovery confirms or cuts)

- **Every master dissolves** against the 4 × 4 screen threshold that Hair already uses. A pixel is kept when its threshold is below *(how present the object is) × (the master's own coverage)* (F-POA-4):
  - Hair: its soft coverage × presence;
  - Masked: a second test beside its alpha test;
  - the four solid masters: the same test on the opacity mask;
  - the two glass masters: the same dither, not a smooth scale.
- **One masked instance per solid master** (Opaque, TwoLayer, Emissive, Subsurface): blend mode overridden to masked, clip to 0.5 (Unreal's default is 0.3333), no graph of its own. The platform swaps a part to it while the object is part-present (F-POA-2, F-POA-6).
- **The value, fixed in `MasterSet.md`:** one Custom Primitive Data float, slot 0, `object_fade`:
  - how far the object has faded **out**; 0 = fully there, which is also what an unset slot reads;
  - **negative** for the copy fading in, which takes the mirror pattern, so a cross-fade shows every pixel exactly once (F-POA-5, F-POA-7).
- **The library's Unreal driver writes the value**, so the library can show the dissolve itself (F-POA-8).
- **The judge:** a cross-fade pair at half, and one object at several presences, seen in Unreal under FXAA, with the four masked instances in the picture.

## In now / not now

- **In:** the eight masters' dissolve; the four masked instances; the value's spec in `MasterSet.md`; the driver writing it; the look in Unreal.
- **Not now:**
  - the platform's side: writing the value, the material swap, the start-up precache, the bake to a clean swap, and the effect overlay (the platform's lead, 2026-11-09: the effect is the platform's own overlay material, with no library change);
  - any article, Creator port, Blender master or Storm change (F-POA-8).

## Dependencies

- **The machine with Unreal** builds and looks (`LOCAL_DELTAS.md` §Two machines).
- **No runtime is owed by the masters' change itself:** at `object_fade` = 0 every master draws exactly today's pixels (the lead's 2026-10-05 ruling). Whether the library's runtime is published so the driver can show the dissolve is a discovery question (Q-P29-4).
- **The platform runs the library's builder itself,** so it gets the masked instances with its next masters build. Its object-fade work waits on this phase for the swap (M15).

## Questions for discovery (seed vs docs)

1. **Q-P29-1** — On TranslucentThick, does a dropped pixel still bend what is behind it (refraction is a separate output)? If it does, zero the bend there too (F-POA-4 hypothesis).
2. **Q-P29-2** — A part-present object's shadow: does it thin with presence, as the hypothesis says? Is that acceptable?
3. **Q-P29-3** — The cost while fading: a masked part in the depth pass, and on Nanite. Measured on the machine with Unreal; the headset figure is the platform's.
4. **Q-P29-4** — Is the library's runtime published with the driver's new write, or only built locally?
5. **Q-P29-5** — Slot 0: confirm with the platform before it is written into the spec (F-POA-7: it reports no use of per-component data on its scene objects, 2026-11-09).
6. **Q-P29-6** — The strict and non-strict tests (F-POA-5): which copy owns a threshold equal to the value, given that Unreal's clip keeps a pixel when the mask is at or above the clip value.
