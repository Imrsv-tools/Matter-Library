# Phase27 — AI Body Skin

**Status:** SEEDED (2026-11-02), on the lead's *"Seed phase 27 as the body.."*. It runs **after Phase25**, which builds the chain it reuses. **Its discovery may run now, beside Phase25's execute** (read-only, its probes in its own scratch); its execute waits for Phase25's 25.2. **`/discovery Phase27` opens Pass 1** and confirms or rewrites this doc.
**Written on:** the machine with Unreal, at `c315976`.
**Seeded from:** [`Phase25_AiSkinStructure.md`](Phase25_AiSkinStructure.md): §Pass 3 hand-off (*"The lead's question … what about the rest of the body?"*, ruled 2026-11-02), RD-P25-16 (the neck waits for the body), F-P25-18 (Annotated Skin), §Deferred (the body islands row).

## Outcome

**An image model's picture of a real person's body becomes the body's skin in the body's own layout, joined to Phase25's head with no visible seam at the neck, shoulders or arms, and judged beside the maker's body on the same character. If it wins, the maker turns it into a calibrated skin structure, as Phase25 does for the head.**

*(Drafted at seeding. Discovery confirms the words.)*

## Why this is a phase

- **The lead asked** (2026-11-02, during Phase25): *"what about the rest of the body?"*, and ruled on the answer's first question, *"(1) its own phase? and is asking the model for unclothed bodies in a public CC0 library OK?"*: *"1) yes"*. *(Read as: the body is its own phase, after Phase25, and generating unclothed body skin is approved.)*
- **Phase25 deferred the seams to it** (RD-P25-16): the neck join between the head island and the body island is solved once the model is on both sides, with the shoulders' and arms' seams, rather than patched on the head alone.
- **It needs things Phase25 does not:** body landmarks, a route for the large unrolled body island, the hands' and feet's islands, and a seam method across islands.

## The plan — as known at seeding

*The agent's outline from Phase25 (`ML_P25_D5`), not ruled beyond the lead's "1) yes".*

1. **The layout:** hm08's body is mostly one large unrolled island (the trunk, arms and legs, front and back together), with the hands and feet as their own islands. It has few features to line up (nipples, navel, knuckles, nails).
2. **A route per region, each a cheap probe first:**
   - **trunk, arms and legs:** (a) the model repaints the island in UV space at a low strength, over the maker's body; or (b) a front and a back picture projected through hm08's front and back renders, matched by body landmarks (Phase25's face method, RD-P25-15). Phase25's Pass 2 measured that at full strength the model ignores the layout (F-P25-7, F-P25-11);
   - **hands and feet:** the face's method, since knuckles and nails must land;
   - **every seam (neck, shoulders, arms):** solved there, with the model on both sides (RD-P25-16);
   - **what the mesh cannot carry:** the maker's gradient, as the ear (RD-P25-18).
3. **The seam map:** MakeHuman's *Annotated Skin* (CC0; labels the body regions and which island edge joins which, F-P25-18). *Unverified:* that its islands are packed as hm08's are; check against `Tone34`'s atlas before use.
4. **The judge:** the library's look view (`tools/parity/look.py`) with body views added, beside the maker's body (`Tone34`'s). **No scanned bar for the body** (OVS-7), so it is judged by eye.
5. **If it wins:** the maker composes the body from the model's field, as 25.2 does for the face.

## Scope — as known at seeding

**In (candidate):** the steps above; body landmarks and the body route as library tools under `tools/converters/fit/`, beside `project_face.py`; the seams.

**Not now:** other tones, people and ages (*Variety*); the 4K test and 8K (RD-P25-20: 2K until things are figured out, then a 4K test on the whole map, only then 8K); a layout LoRA (RD-P25-12, only on the lead's word); a raw AI map shipped as is (RD-SYN-1).

## Rulings carried

- **The lead, 2026-11-02:** the body is its own phase; asking the model for unclothed bodies in this public CC0 library is approved (*"1) yes"*, above).
- **RD-P25-16:** the neck join waits for the body; the seams are solved with the model on both sides.
- **RD-P25-20:** 2K, then a 4K test, then 8K.
- **RD-P25-7:** generation drives the lead's ComfyUI over its API; the project gains no dependency.
- **RD-P25-8:** a model's picture of a person is committed only on a win and the lead's re-ruling.
- **RD-SKM-1** (hm08 is the mesh) · **RD-SKM-5, RD-SYN-1** (no whole AI map ships) · **RD-SKM-2** (no photograph of a person in what ships) · **RD-RO-2** (CC0) · **RD-CMT-4** (a character material's look is judged in the Unreal look view, never Blender).

## Depends on

- **Phase25's chain** (`tools/converters/fit/project_face.py`, `paint_uv.py`, the maker's ear gradient) and its **25.2** (the maker taking an outside field). Phase25 is IN EXECUTION; this phase's execute waits for 25.2.
- **The lead's ComfyUI and models** on the shared model drive (the drive must be mounted, found unmounted 2026-11-02).
- **One GPU, shared** with Phase25's runs: one heavy job at a time.

## Questions for discovery

- Route (a) or (b) for the trunk, arms and legs: does a low-strength UV-space repaint keep the body's layout, or does it need the projection?
- Body landmarks: which detector, and what on hm08's renders it must be snapped to (Phase25 learned that a detector guesses any feature the render does not draw).
- How the head's island and the body's meet at the neck when both are the model's: one picture covering both, or two matched at the seam?
- The prompt for an unclothed body that reads as real skin, not a render, at the subject's tone.
