# Phase28 — AI Hands and Feet

**Status:** SEEDED (2026-11-02, by `ML_P27_D2` on the lead's direct ask: *"add the hands, feet, palms and soles plan to a phase 28 doc and we will do it right after"* — lead-directed, written beside `ML_P27_E3`'s live execute, which this doc does not touch). Runs **right after Phase27**.

## Outcome

**The character's hands and feet — the backs of the hands, the palms, the tops of the feet and the soles — wear the same image-model person's skin as the body, so the whole skin map reads as one complete person from every side.**

*Why it is its own phase:* Phase27 makes the trunk, arms and legs the model's; its hands stayed the maker's (27.2.1: the four-view picture's fingers do not land at 1.7 mm a pixel), and no camera sees the palms or the soles. Once this lands, one AI-made person covers the whole map, head to toe.

**The line this serves (not this phase):** the lead, 2026-11-02 — come to the library with a brief (*"a 30-year-old Asian male"*) and get a complete skin map to add to the library. That needs this phase first, then a person-from-a-brief phase (*Variety*: Phase27 §Deferred) — see Q-P28-4.

## The plan (from the lead conversation, 2026-11-02)

Each part gets **its own close camera on hm08 itself**, the face's method (Phase25 RD-P25-15) and Phase27's close cameras:

| Part | Camera | Fitted by |
|---|---|---|
| Back of each hand | one camera, square to the back | MediaPipe's hand landmarker (21 points: knuckles, fingertips, wrist) + the outline |
| Each palm | one camera, square to the palm | the same 21 points (they work on a palm) + the outline |
| Top of each foot | one camera from above and in front | the outline (no foot detector is known) |
| Each sole | one camera from below | the outline (a sole is a simple shape) |

- **The source** is hm08 rendered from that camera, **wearing the body's finished colour**, so the tone carries over; Krea repaints it at a moderate strength, so it keeps hm08's pose and finger positions (a free prompt draws its own pose: Phase27 F-P27-9, 27.2.1).
- **The prompt** is the body's person (*"the same young woman…"*) plus what is true of the part: palms and soles paler and pinker (less melanin), palm creases, thicker sole skin, the knuckles' redness.
- **Fit, then project:** the picture is fitted to hm08's render (landmarks and outline), then each texel takes its colour from the camera that faces it most squarely — one camera per texel, nothing blended (Phase25, Phase27).
- **Where nothing sees** (the sides of the fingers, between the toes): the maker's skin at the colour round it, as the body's unseen spots.
- **The joins** at the wrists and ankles: Phase27's `neck_join` takes any pair of sources.
- **The fine skin:** Phase27's split (finer than ~2 mm from the close picture), if it helps.
- **The judge:** the original's hands and feet beside the character's, from the same angles, in the library's Unreal look view (Phase27's lesson: the reference beside the result is the test).
- **The nails are not this phase's:** the Nails part wears its own article (`SkinMaps.md` §What the map must show), so only the knuckles and creases must land.

## In now / not now

- **In:** the backs and palms of both hands; the tops and soles of both feet; their joins; the judge's hand and foot views (the palm and the sole are new views).
- **Not now:** a finer hand mesh for knuckle folds (Phase27 §Deferred, the OMF ask); a person from a brief, other tones, ages, a male body (*Variety*, Q-P28-4); 4K and 8K (RD-P25-20); a layout LoRA (RD-P25-12, the lead's word only).

## Questions for discovery (seed vs docs)

1. **Q-P28-1** — Does Krea keep hm08's finger positions at a strength that still repaints the skin? (Probe: a back-of-hand render at 0.4–0.65.)
2. **Q-P28-2** — Does the hand landmarker find 21 points on hm08's own render (a CG hand) as well as on Krea's picture? If not, the outline alone.
3. **Q-P28-3** — A sole from below: does Krea accept that view, or draw a different pose? (The soles are rarely seen; the maker's sole is the fallback.)
4. **Q-P28-4** — The lead's end goal (a skin map from a brief: age, ethnicity, sex): its own phase after this one? It needs at least a prompt built from a brief, a body render of that build (a male hm08 shape is not the rig's), and the maker taking a new subject — none of which this phase does.

## Depends on

- **Phase27 closed** (the body's finished colour is this phase's source tone, and its seams and close cameras are reused).
- The lead's ComfyUI and models on the WorkingDrive; one GPU, shared.
