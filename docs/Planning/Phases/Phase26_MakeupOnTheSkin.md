# Phase26 — Makeup on the Skin

**Status:** SEEDED (2026-11-02). The first part of *Skin Layers*, numbered on the lead's *"b"* (RD-PSM-2). It runs **alongside Phase25** and **ahead of *Eyes in the Shader***. The rest of *Skin Layers* keeps its place after Eyes. **`/discovery Phase26` opens Pass 1** and confirms or rewrites this doc.
**Written on:** the machine with Unreal, at `9904aa3`.
**Seeded from:** [`../Research/261101_R_PlatformSkinAndMakeupAsks.md`](../Research/261101_R_PlatformSkinAndMakeupAsks.md) (Q-PSM-2, Q-PSM-7; F-PSM-1, F-PSM-4; RD-PSM-2) · [`../Research/261027_R_CharacterMaterials.md`](../Research/261027_R_CharacterMaterials.md) (Pass 4, Makeup and marks; RD-CMT-1, RD-CMT-2) · the platform's ask row `PlatformDependencies.md` **M14**.

## Outcome

**A character wears the library's first makeup: face makeup picked by area and a mark placed on the body, merged into one layer on its skin, and it looks the same in Storm, Blender and Unreal.**

*(Drafted at seeding. Discovery confirms the words.)*

## Why this is a phase

- **The platform's skin phase is held on it.** Its makeup step waits on the slots (Q-PSM-7) and on a format and a few pieces (Q-PSM-2), together (F-PSM-1).
- **The slots are a contract change in three tools** (F-PSM-4): the contract (`LCDSchema.md`), the MaterialX graph (`assemble_mtlx.py`), the Blender masters, the Unreal builder, the rig's drivers and the recipe check. That is a phase by `LOCAL_DELTAS.md` §Weighting.
- **Split out of *Skin Layers*** so the platform is unblocked first, with the least competition for the GPU and the lead's sittings beside Phase25 (RD-PSM-2).

## The plan — as known at seeding

1. **The slots on the Subsurface master** (Q-PSM-7): a colour + coverage picture, a finish picture (or its packing), an amount, all on the mesh's own layout. The order against the colour map, the roughness map and the relief written down. **Their neutral leaves every skin as it is today.**
2. **The piece format** (Q-PSM-2), written as the library's contract: fitted pieces (a shape per zone with colour, strength and finish) and placed pieces (stamps), and where the piece list lives in the catalog.
3. **A first handful of pieces**, made in 3D on the approved mesh and baked per layout; each works on every character (RD-CMT-2).
4. **Seen in all three tools** through the rig, and the look in the library's Unreal look view (RD-CMT-4). The platform rebuilds its masters from the builder's source (R-PSM-1), so it can start before a runtime is published.

## Scope — as known at seeding

**In (candidate):** the slots, the format, a first handful of pieces, the contract text, the rig showing them.

**Not now (the rest of *Skin Layers*, after Eyes):** pigment pieces and the shipped pigment fields (Q-PSM-3, F-PSM-6: a ruling to make there) · a wide piece set · the Blender kit for contributors (RD-CMT-2) · stubble and body hair.

## Rulings carried

- **RD-PSM-1** (the answers on marks and `status`) · **RD-PSM-2** (this phase, numbered now).
- **RD-CMT-1** (the library makes the pieces; how a character wears them is the platform's) · **RD-CMT-2** (a piece works on every character) · **RD-CMT-4** (the look verdict in the look-dev scene; the library's Unreal look view until Studio can draw it).
- **RD-P22-17** (the skin has no coat: wet lips are a piece, Q-PSM-1).
- **RD-RO-2:** CC0.

## Questions for discovery

- **Relief** (F-PSM-4): Q-PSM-2's placed pieces carry relief, Q-PSM-7 asks for no relief slot. A third picture, or no relief in the first pieces? Raise it with the platform before the format is written.
- Where the makeup colour sits against the colour map, and whether the scatter colour follows it.
- Whether finish replaces or moves the roughness map's value; premultiplied colour or coverage in alpha; the slots' size (RD-P25-20's 2K first).
- Which first pieces: enough to test both kinds (fitted: lip colour and gloss, eyeshadow; placed: a bruise).
