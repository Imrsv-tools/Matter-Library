# Phase30 — One Coat on the Opaque Master

**Status:** DISCOVERY — Brief written 2026-11-12, **parked on [The Rig on Windows](Future/PhaseTBD_RigOnWindows.md)** (RD-P30-2). Both blockers ruled the same day (RD-P30-1, RD-P30-2). Numbered by the lead the same day (*"Phase30, open discovery"*). Lane: **build**.

**Where the ask came from:** on 2026-11-12 the lead ruled, on the platform's ticket about what the Matter masters cost to draw, that the Opaque master is built from Substrate's own nodes ("O2"). The platform session relayed the ruling here the same day. Its research and measurements are private to the platform and are cited by content, never by id. *The ruling as relayed, not verbatim:* a dielectric slab and a metal slab, mixed by metalness (`SubstrateHorizontalMixing`, parameter blending off), under ONE coat slab weighted by `coat_weight` (`SubstrateVerticalLayering`, parameter blending off). It replaces two calls of Epic's `MF_Substrate_OpenPBR_Opaque`, each carrying its own coat. *"TwoLayer, Masked and Emissive keep the two calls until Opaque holds; then they follow."*

## Outcome

**An opaque article in Unreal (paint, porcelain, leather, metal) draws with a single clear coat over its base and matches the OpenPBR reference at least as well as it does today. It also costs less to draw, so Studio can run Substrate at its smaller per-pixel budget.**

*Who it is for:* the platform's Creators in Studio, who see the same articles drawn faster. The master's name and its Creator Inputs do not change. Blender and Storm are untouched; the Blender master is already one Principled BSDF, one coat over a linear mix, and is the layout reference.

**Why it is worth it (the platform's measurement on the prototype, stereo, median frame):** at the smaller budget, O2 drew the coated scene about 6 % faster and the matte scene about 13 % faster than today's master at the larger budget, with less video memory. On sky-lit pictures, the coat matched OpenPBR on a gloss paint and on Porcelain, Leather came closer to OpenPBR than today's master does, and matte, fuzz and metal articles stayed within 0.5 % of today's master (Copper Verdigris +2.6 %).

## First human test

**Where:** the rig's sheet on the machine with Unreal, opened by the agent; the handback carries its path. *(The Windows machine, once the rig runs there: RD-P30-2.)*

**⛔ The pictures are the rig's own float captures, so no tone curve applies.** The platform's Studio pictures are film-curve PNGs. Undo the default FilmToneMap before taking any brightness ratio from them, or dark articles read about 2× wrong.

1. **Click 1 — the Opaque master with one coat (30.1).**
   - **Picture:** the rig's sheet with four columns: Storm · Unreal with today's master at 160 B (the pinned runtime) · Unreal with O2 at 80 B · O2 at 160 B. Plus the Copper sweep (Phase06 6.3's sliders) on O2 at 80 B.
   - **Fixtures (all Opaque, all from the library; each one's values were read from its `.mtlx`):**
     - the grey card;
     - Copper_Polished, and the Copper sweep;
     - Copper_Verdigris (metalness from a map, so partly metal);
     - Silver_Polished (a near-white mirror);
     - CastIron_Raw (dark);
     - Porcelain_Glazed and Leather_Brown (coats; two of the four coated Opaque articles);
     - StainlessSteel_Brushed (anisotropy; one of three);
     - Felt_Natural (fuzz; one of seven textiles that set `fuzz_weight`);
     - Porcelain_Glazed with a coloured `coat_color`, set by the rig's sweep: a probe, because no library article tints its coat.
   - **What the lead judges:**
     - O2 at 80 B sits on Storm at least as closely as today's master does (ΔE per swatch beside the picture);
     - the coat reads as a coat, with no brightened base;
     - at 80 B and 160 B, O2 draws alike.
   - **The sentence afterwards:** *"the opaque master with one coat matches Storm as well as the old one, at the small budget."*
2. **Click 2 — the other masters at the small budget (30.2, RD-P30-1).**
   - **Picture:** the same four columns.
   - **Fixtures:** Rust_OnSteel_Flaking and Paint_OnMetal_Chipped (TwoLayer); Lace_Floral, OakLeaf_Natural and Hair_DarkBrown (Masked); Neon_Signage and LED_WarmWhite (Emissive); Marble_Veined_Polished and a skin (Subsurface); Hair_Natural (Hair).
   - **What the lead judges:** nothing gets brighter at 80 B.
   - **The sentence afterwards:** *"every master draws the same at 80 bytes as at 160."*

**Machine-checked, not a click (the agent's, T1):** the compiled `BasePassPixelShader.usf` at 80 B keeps a real `SubstrateTree.SubstrateVerticalLayering` and a linear horizontal mix, not `…ParameterBlending`. It is read for Opaque in 30.1 and for every master in 30.2.

## In now / not now

- **In:**
  - 30.1: O2 is the Opaque master. The `MATTER_MASTERS_OPAQUE` switch, its told-line suffix and the "PROTOTYPE / throwaway" wording are removed, and so is the function-call path for Opaque (no dangling nodes).
  - 30.1: the three uncommitted `o2_front` edits: fuzz on the dielectric slab only, F90 unwired where it is 1, and the base's index under the coat as OpenPBR's `eta_s`.
  - 30.1: each mapping gap, closed or dropped as §Decisions says.
  - 30.1: the 80-byte render (a launch override; see the build map) and the T1 read.
  - 30.2: TwoLayer, Masked and Emissive onto the same front, and the runtime's budget set to 80 (RD-P30-1).
  - At the close: the docs, a new Unreal test runtime (owed: this changes what Opaque draws at its defaults), and the `PlatformDependencies.md` row the platform reads.
- **Not now:**
  - the platform's side: pinning the release, cascading into Studio, Studio's budget setting, and re-measuring. This goes in the ledger row, not here.
  - the coated article's Lumen reflection cost and the first-appearance freeze (both the platform's);
  - Copper Verdigris drawing darker than OpenPBR in both masters, which predates O2 (the platform's ticket);
  - the translucent masters, which make one call and have no metal mix.

## Rides on

| Row | What in this phase rides it | The peer we follow (file:line, opened) |
|---|---|---|
| 5 — drawing an object part-present | O2's Opaque master keeps the dissolve's `fade_mask` clip, and its masked instance `MI_Matter_Opaque_Fading` takes the new graph | `build_masters.py:1029–1032` (the opaque clip, outside the front material: O2 does not touch it) · `build_fading` |
| — the coat darkening (no CoreMechanisms row; the master's own) | O2 is fed the base colour already darkened by MaterialX's factor | `build_masters.py:950–984` · Blender's `blender/masters/build_masters.py:491` (coat → Principled) |

## The reuse check

- **What Substrate provides:** the Slab BSDF, `SubstrateHorizontalMixing`, `SubstrateVerticalLayering`, `SubstrateWeight` and `SubstrateTransmittanceToMFP`. O2 is made of nothing else.
- **What it drops:** Epic's function, the custom layer that cost the second coat.
- **The slab's pins on 5.8**, read from the prototype's build log (2026-11-12): Diffuse Albedo, F0, F90, Roughness, Anisotropy, Normal, Tangent, SSS MFP, SSS MFP Scale, SSS Phase Anisotropy, Emissive Color, Second Roughness, Second Roughness Weight, the three Fuzz pins, and the two Glint pins. There is **no diffuse-roughness pin and no F82 pin**.
- **Standards touched:** OpenPBR's layering (`open_pbr_surface.mtlx`: the linear metal mix, `eta_s`, coat darkening) and nothing else.

## Decisions that bind

- **D-P30-1 — O2 supersedes Phase06 D6 for the Opaque master** ("each master is Epic's Substrate OpenPBR function plus our network"). The network (place2d, textures, overlays, TwoLayer blend, normals, the fade) is unchanged; only the BSDF front changes. Recorded in place in Phase06 D6, `Unreal.md` U1–U3, MasterSet §Where each target's masters are built, Consumers §Unreal material settings, LCDSchema §Coat (*"feeding Epic's own pin 0"*), `PlatformDependencies.md` P20 (*"need … 160"*), and the comment in `Config/DefaultEngine.ini`. All are marked, never deleted.
- **D-P30-2 — the mapping gaps** *(unless you say otherwise; the counts are of the library's 62 Opaque articles, 2026-11-12)*:
  - **`base_weight`: closed.** Multiply it into the base colour before both slabs, as OpenPBR does. It costs one node. Today's master passed it to Epic's function.
  - **`base_diffuse_roughness`: dropped**, marked `Drift (2026-11-12)`. The 5.8 slab has no pin for it, no Opaque article sets it, and it is no Creator port.
  - **The metal's edge tint: kept as `specular_color` → F90**, marked `Drift`. It equals OpenPBR's F82 at the default white, and no Opaque metal sets `specular_color`.
  - **Anisotropy: checked**, on StainlessSteel_Brushed in click 1. Three articles set it.
  - **The coat's colour through `TransmittanceToMFP`: checked**, on the probe in click 1. No article tints its coat.
  - **The coat darkening: kept as the master's own MaterialX factor**, checked on Porcelain and Leather.
  - **Fuzz on the dielectric slab only** (o2_front): a fuzzy metal loses its fuzz. No Opaque article sets fuzz with a constant metalness. Marked `Drift`.
- **D-P30-3 — the master's name, its parameters and the Creator Inputs do not change**, so Studio needs no change beyond the budget.

## Blockers — the lead's

1. **RULED 2026-11-12 → (a), RD-P30-1.** The lead: *"decision 1) a"*. *My reading:* TwoLayer, Masked and Emissive move to the one-coat front inside this phase (30.2), after Opaque holds, and the runtime and the ledger row go to 80 B only once every master reads clean there. **The platform agreed the same day** (its session, relayed): Studio stays at 160 B until the library's Phase30 ledger row says 80 B. *The fork as it was put:* **The small budget and the masters that still make two calls.** At 80 B, Substrate flattens the coat of every master built from two function calls, and the master gets brighter (`Unreal.md` U3: the grey card ×1.14–1.39). After O2 that is still TwoLayer, Masked and Emissive: **8 library articles**: Rust and Paint on metal (TwoLayer); Lace, Oak leaf and Hair_DarkBrown's cards (Masked); Neon and two LEDs (Emissive), plus whatever Studio's own scenes put on them. So the platform's planned budget move to 80 B would brighten them in Studio. The one-call masters (Subsurface, 66 articles; Hair; the two translucent ones) have never been read at 80 B.
   - **(a) Recommended.** This phase takes all three to the same front once Opaque holds (step 30.2), reads every master at 80 B (T1), and only then sets the runtime to 80 B and tells the platform it may. That keeps your ordering, *"until Opaque holds; then they follow"*, inside one phase. The code is shared: `o2_front` already takes the pins every master is fed.
   - **(b)** Opaque only. The runtime and Studio stay at 160 B until a later phase moves the rest, so the 80 B saving waits.
   - *(Studio going to 80 B with three masters still on two calls is not offered: it ships 8 known-bright articles.)*
2. **RULED 2026-11-12 → the rig on Windows first, RD-P30-2.** The lead: *"i only have this windows machine, not linux"*, then, offered (1) judge in Studio with Blender as the reference, (2) get the rig running on Windows first, (3) park: *"2"*. *My reading:* there is no machine with Unreal on Linux any more. The rig's three columns, the Unreal app's build and the runtime publish move to this Windows machine in a unit of their own ([The Rig on Windows](Future/PhaseTBD_RigOnWindows.md), seeded the same day, which holds what was measured). This Brief's clicks run there once it closes. Every "the machine with Unreal" in this doc now means the Windows machine. What that machine has and lacks today:
  - Storm is built by hand (its driver is still Linux-shaped);
  - Blender 5.x is missing (4.0 is installed);
  - the library's Unreal app has never been built (Visual Studio 2026 is present).

  *(Corrected the same day: this note first said there was no `usdrecord` and no C++ toolchain.)* *The fork as it was put:* **Which machine runs the clicks.** The rig's Unreal column runs the pinned Linux runtime, or editor mode through `$MATTER_UNREAL_EDITOR` (`tools/parity/drivers/unreal.py:617–643`). `unreal/build.sh` and `publish.sh` are Linux/Mac. This Windows machine has Unreal 5.8 and Studio, and the prototype was built here for Studio's plugin, but `LOCAL_DELTAS.md` §Two machines does not describe it.
   - **Recommended:** build, run the rig and publish on the Linux machine with Unreal, as every runtime so far. This machine keeps the platform's own look in Studio.
   - **Otherwise:** say this machine, and step 30.1 first proves the rig's editor-mode column runs here.

## Step list

- **30.1 — O2 is the Opaque master.**
  - Remove the switch and the function-call path; take in the three o2_front edits; close the gaps per D-P30-2.
  - Render the rig at 80 B and 160 B, and read the T1 shader dump.
  - First clickable result: **click 1**.
- **30.2 — TwoLayer, Masked and Emissive follow; the runtime goes to 80 B** *(RD-P30-1)*.
  - Masked: its coverage clip reads the coverage directly, since there is no `OpacityMask` output without the function.
  - Emissive: its light on the base slab's Emissive Color, keeping U4's length rule.
  - TwoLayer: the second layer is already mixed before the front.
  - Read the T1 dump for every master at 80 B, then set `r.Substrate.BytesPerPixel=80` in the runtime's config.
  - First clickable result: **click 2**.
- **At the close:** the doc sweep of D-P30-1; the new runtime (`unreal/publish.sh N`, on the lead's word, after the push); and the `PlatformDependencies.md` row update telling the platform it may pin, set 80 B and re-measure.

Every §In now bullet names a step above or *at the close*. Click 1 needs only 30.1. Click 2 needs 30.2.

## Compact build map

- **`unreal/MatterRuntime/Scripts/build_masters.py`:**
  - Opaque's `MASTERS` row stops making calls (and so do TwoLayer, Masked and Emissive at 30.2).
  - `feed` keeps recording `pins` with no call to link.
  - The checks against Epic's function's input names (`inputs`, `missing`, `coat_darkening`) and `outs`/`front` move behind "the master makes a call".
  - `o2_front` loses its prototype docstring and takes `base_weight`.
  - The head docstring and the `calls` comment are rewritten. `OPAQUE`, `_told("MATTER_MASTERS_OPAQUE"…)` and the told-line suffix are deleted.
- **`unreal/MatterRuntime/Config/DefaultEngine.ini`:** the budget comment now; the value at 30.2.
- **The 80 B render before 30.2:** a launch override, `-ini:Engine:[/Script/Engine.RendererSettings]:r.Substrate.BytesPerPixel=80`, the same `-ini:` route T1 uses. Whether the runtime's driver passes extra arguments is checked at 30.1; if it does not, the rig's editor mode takes it.
- **Docs:** the D-P30-1 list, plus `docs/ToolingConventions.md` §What a second project tells the builder (no `MATTER_MASTERS_OPAQUE`; it never landed there).
- **Tests:** the existing lanes (`run_all.py`) and the rig. There is no new gate.

## Risk lane — `build`

- **What it touches:** no authorisation, secrets, data or public edge; one generated-asset builder and the docs.
- **Controls read:**
  - `tools/parity/JOB_FORMAT.md:191–194`: a builder change reaches callers only through a new pinned runtime. That is owed, and it is the close's publish, on the lead's word.
  - `tools/parity/drivers/unreal.py:167,173`: build-date-gated features; O2 adds none.
  - No gate hashes `build_masters.py`.
- **What re-renders:** the Unreal column of every published rig picture, once the new runtime is pinned (the next dev snapshot).

## Open questions

- None beyond §Blockers.

## Discovery Log

- **Pass 1 (2026-11-12):** read the prototype (`b33aa2f`) and its three uncommitted edits, the builder's Opaque path (`build_masters.py:674–1060`), `Unreal.md` (U1–U3, T1), the runtime's config, Phase06 D6 and 6.3, `CoreMechanisms.md`, the specs that name the masters' build (MasterSet, Consumers, LCDSchema), `PlatformDependencies.md` P20/M7, the rig's runtime finder, the travel ports, and the library's Opaque articles (by script, a scratch count).
  - **Finding:** the small budget breaks the masters still on two calls → Blocker 1.
  - **Finding:** the slab has no diffuse-roughness or F82 pin → D-P30-2.
  - **Finding:** no prior research in this repo covers draw cost.
  - **Finding:** the phase name appears nowhere in the tree but the prototype.
  - **Learnings:** Unreal read; no other domain is touched.

## Discovery Status

- **Passes captured:** 1.
- **Current working direction:** 30.1 Opaque, then 30.2 the other two-call masters and the 80 B runtime.
- **Open decisions:** none. Both blockers ruled (RD-P30-1, RD-P30-2). The phase is parked until The Rig on Windows closes.
- **Checks to carry forward:** T1 at 80 B per master; ΔE per swatch against today's master; FilmToneMap undone before reading any Studio PNG.

## Execution Log

_(populated during execution)_
