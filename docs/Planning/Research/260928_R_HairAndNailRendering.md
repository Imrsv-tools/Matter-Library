# Research — How to render hair (and nails) so they read as hair, in every renderer we target

**Opened:** 2026-09-28 · **Mode:** research, lead-directed from `/execute P8` step 8.1. It gathers and commits to nothing; Phase08 rules. **Mnemonic:** `HR` (ids `HR-Qn`, `HR-Fn`).

**Question (lead, 2026-09-28, verbatim, on `Hair_Natural` in Blender):** *"Hair still looks plastic, no transparency, no SSS... hair is not a thick solid"*, then *"YOu need to research how to render hair"* and *"Will be similar issue with nails"*.

**Extends, does not replace:** `260927_R_CharacterMaterials_MPFB2.md` (CM-Q3 hair, Pass 4's Chiang note) · `Phase08_CharacterAppearance.md` (RD-P08-1, now reopened) · `260928_R_PlatformAppearanceAsks.md` (A1: the lead's *"one hair material … really good"* that also serves strands later).

---

## Pass 1 — What makes hair read as hair (the physics, and what production does)

**Examined:** the fibre-scattering literature as production summarises it (Marschner; Kajiya-Kay; Scheuermann's card shader), and current real-time practice (Unreal hair cards, game card workflows). Sources at the end.

A hair fibre is a thin, **translucent** dielectric cylinder. Light does three things at it (Marschner's lobes):
- **R**: reflects off the cuticle. A white highlight, stretched **along** the fibre.
- **TT**: passes **through** the fibre. This is the backlit glow at the silhouette, coloured by the hair's pigment. It is the part the lead named: *"no transparency, no SSS"*.
- **TRT**: enters, reflects inside, and exits. A **second, tinted** highlight, broader, and shifted along the strand away from the first (the tilted cuticle scales shift the two lobes in opposite directions).

**Many fibres together** also scatter light between each other (multiple scattering), which makes a head of hair soft and saturated rather than a shiny shell.

**What real-time CARD hair does to fake this** (cards are what the platform ships, and what MakeHuman's bob is):
1. **Light through the card**: a translucency / backlit / scatter term (Unreal's Hair model *Scatter* and *Backlit*; *Two Sided Foliage* for leaves).
2. **Two anisotropic highlights**: primary white, secondary tinted, each along a tangent nudged towards or away from the normal (Kajiya-Kay shift).
3. **Soft coverage, not a hard cut-out**: masked plus **dithered opacity** with temporal AA, or alpha-to-coverage, and two-sided. A hard binary threshold gives the "helmet" edge.
4. **Mesh-supplied maps beside the cut-out**: a root-to-tip gradient (often the card's `V` coordinate), a per-strand random ID, and a depth/AO map. They darken the roots and the inner layers, and vary colour and roughness strand to strand.

⇒ **`Hair_Natural` as built has none of 1–3.** It is an opaque OpenPBR surface with one anisotropic highlight and a hard cut-out, which is exactly *"a thick solid"*. RD-P08-1 (settings-only) changes only how Unreal shades it.

## Pass 2 — What each target renderer can do (verified where marked)

| | MaterialX / OpenPBR → **Storm** (USD viewers) | **Blender 5.2** | **Unreal** (Hair shading model) |
|---|---|---|---|
| **Light through the card** | ✅ **Thin-walled subsurface**: with `geometry_thin_walled = true`, OpenPBR's subsurface becomes an Oren-Nayar reflection plus a **`translucent_bsdf`** transmission, split by `subsurface_scatter_anisotropy` (reflection × (1 − a), transmission × (1 + a)). *Verified in the local graph, `libraries/bxdf/open_pbr_surface.mtlx` (MaterialX 1.39.5, the "Subsurface (thin-walled)" block).* Storm's `mx_translucent_bsdf.glsl` **lights it from behind**: it flips the normal and takes both direct lights and environment irradiance from the far side (*read 2026-09-28*). | ✅ **Translucent BSDF** is Lambertian diffuse transmission (manual), the same lobe. Principled 5.2 also has a **`Thin Wall`** input (*probed live 2026-09-28*; the bundled manual does not list it yet). Whether Principled's Thin Wall turns its subsurface into translucency is **unverified**; the Blender master can add a Translucent lobe explicitly either way. | ✅ **Scatter** and **Backlit** inputs: *"approximating the way light passes through hair"* (Epic docs) |
| **Two highlights** | ✅ **specular** (`specular_roughness_anisotropy`, `geometry_tangent`) **+ coat** (`coat_color` tinted, `coat_roughness_anisotropy`, **its own `geometry_coat_tangent`**). *Verified: the inputs exist in the local graph.* So a white primary and a tinted, shifted secondary are expressible. | ⚠ Principled's coat has **no anisotropy and no tangent** (inputs listed live). A tinted coat approximates the second highlight, not its stretch or shift. | ✅ native: *"multiple specular highlights: one representing the color of light, and another representing a mix of hair and light color"* |
| **Soft coverage** | ⚠ continuous `geometry_opacity` (no cutoff) is alpha-**blended** in Storm: soft, with card-order sorting artefacts **unverified** | ✅ Cycles: stochastic, soft (the probe's variant C) | ✅ masked + **Opacity Mask Dither** + TAA (community docs) |
| **A real fibre model** | `chiang_hair_bsdf` exists with a GLSL implementation (inputs include `ior`, `cuticle_angle`, `absorption_coefficient`, `curve_direction`). It is a **fibre** model for curves, not cards. **Storm rendering it is unverified.** Decision of record 1 keeps articles on `open_pbr_surface`. | Principled Hair BSDF: **Cycles only**, a fibre model for **curves** (manual) | Hair model on **strands** (grooms) |

**The fibre models (Chiang, Principled Hair, Unreal strands) are for strands, not cards.** They are the answer to the lead's *"same material when we switch to groom"*, not to today's cards.

## Pass 3 — Probe: the character's own hair cards, backlit, three ways (2026-09-28, live Blender, Cycles)

A disposable probe in the lead's Blender: MakeHuman's CC0 bob, brows and lashes (the rig's character scene), a medium-brown tint, a warm backlight and a key light. Three heads side by side:
- **A**: the library's `Hair_Natural` as shipped (Masked graph: opaque surface, hard cut-out at 0.5).
- **B**: A + **light through the fibre**: a Translucent lobe carrying 60 % of the diffuse. This is the Blender equivalent of OpenPBR's thin-walled subsurface.
- **C**: B + **soft coverage** (the cut-out map's grey used as coverage, no threshold).

**Read by eye (agent):** A reads as flat, cardboard-like shells. B glows warm where the backlight passes through. C also loses the hard helmet silhouette. **The lead's judgement is owed** (it is the lead's eye that found the defect). **The limits of the fixture:** MakeHuman's `bob02` is a coarse card set with only albedo and alpha (Phase07 research Pass 3), so no material will make it photoreal. Root-to-tip, strand variation and depth need maps the cards do not carry (Pass 1, item 4).

**Reproduction:** `260928_R_HairAndNailRendering_probe.py` beside this doc. Run it in Blender 5.2, in a session with the repo checked out: it builds its own scene, **P08 hair probe**, and touches nothing else. Not yet probed: **the same three variants in Storm** (OpenPBR thin-walled subsurface through `usdrecord`), which is HR-Q1.

## Pass 4 — Nails: the same class of problem

A nail plate is **hard, flat, translucent keratin** over the **nail bed**: blood-perfused skin whose colour shows through, so the pink is the bed's, not the plate's (anatomy sources below). The lunula is whitish where the matrix meets the bed, and the free edge is whitish where there is no bed beneath. The surface is a smooth, glossy plate.

**`Nail_Natural` today:** Opaque, a constant pink `(0.80, 0.60, 0.55)`, and a coat. So it is a painted solid, which is the same *"thick solid"* defect.

**What reads as nail, in the contract we have:**
- the **Subsurface** master: the bed's colour scattering under the plate, with a short radius (the plate is ~0.5 mm), and `subsurface_color` from the **skin tone** of the hand (which matches M4, tone-matched nails);
- a **clear glossy coat** for the plate;
- the lunula and free-edge whitening as **mesh-bound maps** (a fit, like the cut-out), later.

MakeHuman's nail is part of the body mesh, split by MPFB2's CC0 mask (Phase07 7.5.1), so a thin-walled treatment does not apply: it sits on the finger. **Subsurface + coat is the probe to run** (HR-Q5).

## Pass 5 — What this means for the library (options, not decisions)

- **H1 — The Hair master gets a graph of its own: thin-walled translucency.** `geometry_thin_walled = true` with `subsurface_weight`, `subsurface_color` (the fibre's colour) and forward `subsurface_scatter_anisotropy`, so light passes through the card. All are lane-A OpenPBR inputs the assembler already carries (Phase07 7.3), except `geometry_thin_walled` on a non-translucent master. This **replaces RD-P08-1's "settings-only"**: the master earns its token with a real graph difference (translucency), plus its settings row (a hair model in Unreal). **Blender:** `ML_Hair` gains the Translucent lobe (probe B). **Unreal:** Scatter / Backlit. It stays `open_pbr_surface` (Decision of record 1).
- **H2 — Soft coverage for Hair.** Hair's coverage row becomes *"masked, dithered"*: Unreal's dithered mask, Cycles' stochastic alpha, and continuous opacity in the MaterialX graph instead of the 0.5 threshold. The Storm cost (blend sorting between cards) is **HR-Q2**, measured before it is ruled.
- **H3 — The second, tinted highlight via the coat** (`coat_color` = the fibre's colour, `coat_roughness_anisotropy`, `geometry_coat_tangent`). It is exact in MaterialX and Unreal and approximate in Blender (no coat anisotropy): **an LCD gap** to weigh (HR-Q3).
- **H4 — Mesh-supplied hair maps beyond the cut-out** (root-to-tip, strand ID, depth/AO): the same *"supplied at binding"* pattern as `cutout_map` (L2). They are platform assets. MakeHuman's cards carry none, but root-to-tip can come from the card's `V`. It is a contract addition, later (HR-Q4).
- **H5 — Strands later**: Chiang / Principled Hair / Unreal strands. This means a strand master whose article would not be `open_pbr_surface`, and **the lead's call when the platform switches to grooms**. Not now.
- **N1 — Nail on Subsurface + coat**, `subsurface_color` from the tone (with M4, Phase08 8.2).

**The cheap, visible order:** H1 (+ H2 if Storm allows it) re-authors `Hair_Natural` and `ML_Hair` in one step, and N1 folds into 8.2's per-tone nails. H3 is a refinement. H4 and H5 are later phases.

## Open questions

| # | Question | Why it matters |
|---|---|---|
| HR-Q1 | Does Storm render thin-walled OpenPBR subsurface on the character's cards the way Blender renders probe B? | Stock-viewer parity for H1 |
| HR-Q2 | Soft coverage in Storm: are the card-sorting artefacts acceptable, or does Hair keep a (lower) cutoff there? | H2 |
| HR-Q3 | Is a tinted, anisotropic coat worth an LCD gap in Blender? | H3 |
| HR-Q4 | Who supplies root-to-tip / strand-ID / depth maps, and when? | H4: the next realism step after H1–H2 |
| HR-Q5 | Does a Subsurface + coat nail read as nail on the character's hands, in both tools? | N1 |
| HR-Q6 | Does Principled's `Thin Wall` turn its subsurface into translucency (so `ML_Hair` needs no explicit Translucent lobe)? | A simpler Blender master |

## Status

- **Passes captured:** 1–5 (2026-09-28): the physics and production practice; the three renderers (thin-walled translucency verified in the local OpenPBR graph and Storm's GLSL; Blender's Thin Wall and coat inputs probed live); a live Blender probe (A / B / C); nails; options H1–H5 and N1.
- **Decided:** nothing. Phase08 rules H1/H2 (step 8.1 is suspended on this research) and N1 (step 8.2).
- **The lead on probe A / B / C (2026-09-28), verbatim:** *"I will follow your lead - they all look bad to me... too glossy, no "life" looks clearly extermly fake and really really bad... if that is the best we can do then it is what it is.. but eventuall this needs to be reseerached and fixed.. this is not usable..."*. On nails: *"Agreed nails are bad we need to fix them."*
- **Current direction:** H1 + H2 as the **interim** hair (translucency and soft edges), plus **less gloss** (the lead's *"too glossy"*). H4 (card maps) and H5 (strands) are the **real** fix: *"eventuall this needs to be reseerached and fixed"*. That needs a research thread of its own, and better card assets than MakeHuman's bob.
- **Unverified, recorded as such:** Storm on thin-walled subsurface for cards (HR-Q1) and on soft coverage (HR-Q2); Principled's Thin Wall semantics (HR-Q6); Storm on `chiang_hair_bsdf`; Unreal Substrate's hair path (only the legacy Hair shading model's inputs were read, from Epic's 5.8 docs).
- **Next step:** the lead judges probe A / B / C. Then, if B or C is right, a Storm probe of the same (HR-Q1, HR-Q2) and the 8.1 rework.

**Sources:**
[Epic — Shading Models (5.8)](https://dev.epicgames.com/documentation/en-us/unreal-engine/shading-models-in-unreal-engine) ·
[Epic — Hair Rendering (4.27)](https://dev.epicgames.com/documentation/en-us/unreal-engine/hair-rendering?application_version=4.27) ·
[80.lv — Unreal Engine hair shader tutorial](https://80.lv/articles/tutorial-unreal-engine-hair-shader) ·
[Scheuermann — Hair Rendering and Shading (ATI)](https://web.engr.oregonstate.edu/~mjb/cs557/Projects/Papers/HairRendering.pdf) ·
[fxguide — RenderMan & Marschner hair](https://www.fxguide.com/fxfeatured/pixars-renderman-marschner-hair/) ·
[Chalmers — Simulation and Visualization of Hair for Real-Time Games](https://www.cse.chalmers.se/~uffe/xjobb/Simulation%20and%20Visualization%20of%20hair%20for%20Real-Time%20Games.pdf) ·
[UE5 hair guide (cards: dither, two-sided, root-to-tip from V)](https://yelzkizi.org/unreal-engine-5-hair-guide-25-proven-tips/) ·
[OpenPBR specification](https://academysoftwarefoundation.github.io/OpenPBR/) ·
[Autodesk Arnold — OpenPBR (thin-walled)](https://help.autodesk.com/view/ARNOL/ENU/?guid=arnold_user_guide_ac_surface_shaders_ac_open_pbr_html) ·
[Maxon Redshift — OpenPBR material](https://help.maxon.net/r3d/maya/en-us/Content/html/Material+OpenPBR.html) ·
[ASWF — MaterialX 1.39.2 (Chiang hair BSDF)](https://www.aswf.io/blog/materialx-v1-39-2-now-publicly-available/) ·
[Blender manual — Principled Hair BSDF](https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/hair_principled.html) ·
[Wikipedia — Nail (anatomy)](https://en.wikipedia.org/wiki/Nail_(anatomy)) ·
[Wikipedia — Lunula](https://en.wikipedia.org/wiki/Lunula_(anatomy)) ·
[University of Leeds — Histology: nails](https://www.histology.leeds.ac.uk/skin/nails.php)
