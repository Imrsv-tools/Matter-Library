# Phase22 — Skin Maps Beyond Colour

**Status:** ACTIVE (IN DISCOVERY) — **numbered Phase22 2026-10-27 as discovery opened** (the lead: *"/discovery Phase22 Skin Maps Beyond Colour"*; the head of `## Future` since the 2026-10-27 re-sequence, RD-CMT-3; the numbering F-CMT-9 laid out). Seeded 2026-10-14, **un-parked 2026-10-26** (the lead, *"3) yes"*, RD-SYN-3, [`261026_R_SyntheticSkinAndEyes.md`](../../Research/261026_R_SyntheticSkinAndEyes.md); it was parked 2026-10-14, *"skin detail stay parked TBD"*, RD-DS-8). The test set there shows what colour alone can reach; this phase is what answers "still reads plastic". A pointer-shell written by `/research` on the lead's word: *"Seed a phase TBD..."*, then *"Full skin map set"* when asked which. **Starting discovery is a deliberate gate, the lead's call, never a slide.** It builds on *Skin Maps* ([`Phase21_SkinMaps.md`](../Phase21_SkinMaps.md)), which ships the colour map first.

## Outcome

**Up close, a character's skin catches the light as real skin does:** fine wrinkles and creases, oilier and drier areas, and light glowing through ears and fingers. This works in Blender, a USD viewer and Unreal, for every character built from the approved human mesh.

## Why this is a phase of its own

*Skin Maps* gives skin its colour through the existing `base_color_map`, with no new input (RD-SKM-3). **Every map beyond colour needs a new mesh-supplied input**, so each one is an addition to the material contract (F-SKM-11, F-SKM-18). That work is added and tested apart from the colour map, which makes it its own phase (Working Agreement §What a Phase Is).

## Scope — as known at research (2026-10-14)

The authority until this phase writes its specs: [`261014_R_SkinMaps.md`](../../Research/261014_R_SkinMaps.md) §Resolved and Passes 3–6. The draft contributor spec: [`docs/specs/Authoring/SkinMaps.md`](../../../specs/Authoring/SkinMaps.md).

- **The maps, in the order the industry adds them after colour** (F-SKM-11):
  1. a normal map for wrinkles and folds; pores stay the article's tiling `Skin_Pores`, as everyone does it;
  2. roughness or specular variation: oilier forehead and nose, drier elsewhere;
  3. cavity;
  4. scatter or thickness: thin parts glow.
- **What the library already has:**
  - the tiling micro layer (`Skin_Pores`) and a roughness constant (F-SKM-11);
  - MPFB2's CC0 thickness map `sss.png` (F-SKM-4; MAP S-b);
  - one UV set carrying both the atlas and the tiled pores (F-SKM-13, F-SKM-27).
- **What each renderer does with them** (F-SKM-18):
  - Storm's subsurface is a per-pixel approximation, so a thickness map changes Cycles and Unreal and little in Storm;
  - no thickness-map input was found on Unreal's Substrate slab.

  *(Each is "as of 2026-10-14"; recheck at the next major release.)*
- **The rulings carry over:** one approved mesh (RD-SKM-1); sources without photographs of people (RD-SKM-2); neutral at the genitals and groin (RD-SKM-4); AI only as a detail layer (RD-SKM-5).

## Open questions (settle in research or discovery)

- Which map comes first, and is it worth it in all three tools? A probe, as *Skin Maps* had (Pass 5).
- One map per skin tone (as colour), or one shared by all six? Most of these maps describe the surface, not the tone.
- How each new input is named and carried in the contract (LCDSchema, Carrier rule), and what a renderer without it does.

## Discovery Log

*(empty: `/discovery` fills it, after Skin Maps)*
