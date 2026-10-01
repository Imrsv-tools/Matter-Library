# Phase10 — Coloured Wear Layers

**Status:** IN EXECUTION (2026-10-01; lane `build`). Brief written at discovery Pass 2; Q-P10-1 ruled (b), RD-P10-1. **Numbered Phase10 by the lead's ruling, 2026-10-01**, verbatim: *"If 2 then we need to do that phase now instead."* ("2" was Library Coverage's Pass 1 proposal to give colour on wear layers a phase of its own.) Library Coverage, which held Phase10 for part of that day, is un-numbered again (`PhaseTBD_LibraryCoverage.md`). That follows the lead's own precedent of 2026-09-28: *"make this Phase 8, mark the current Phase8 as TBD"*.
- **Seeded from:** Library Coverage's seed question 10 and F-LC-7 · Phase07's ruling L3 (*"by L3's default the colour channel goes to Phase08 with dust"*, its close) · research `260927_R_CharacterMaterials_MPFB2.md` CM-Q5 · Phase05 step 5.2's finding F11 (the wear layers are too faint to see).

## Outcome

**A Creator who turns up a wear layer such as dust or grime sees it in its own colour, not only as a change in shine, and it looks that way in Blender, a USD viewer and Unreal.**

*(Seed wording, kept. "Grime" is dust placed by the `Grime01` mask (F-P10-2), so the wording reads right to a Creator and needs no change.)*

---

## The Brief

### What changes, in one paragraph

A wear layer that is a **deposit** (today only `Dust01`) gets a **declared colour**, and where it lies it **covers** the surface. The base colour moves to the dust colour, and metal, transmission, scattering, coat and fuzz all move to none, weighted by the overlay's existing effect (density × the layer's alpha × the mask gate). Damage and gloss layers (scratches, scuffs, edge wear, fingerprints) are untouched. The layer's packed channels still never become colour, because the colour is a declared value. That refines MasterSet's modulator rule rather than dropping it. An article with no deposit colour assembles byte-identically.

### First human test

Reached in the rig's sheets (`uv run tools/parity/rig.py <article> --sweep`, the agent runs it and opens the sheet) and in Blender with the **installed** Asset-Browser library, the scene framed by the agent. The lead looks and judges; the lead types nothing.

| # | Step | What the lead looks at | Passes when |
|---|---|---|---|
| 1 | 10.1 | **Oak's** sheet, the dust row at 0 → 0.5 → 1, Storm and Blender columns | the dust reads as dust, in its own colour, growing with the slider, alike in both. The Unreal column is still `v2` and shows colourless dust (F-P10-14) |
| 2 | 10.1 | **Glass_Clear's** sheet, its dust row | the dust is visible on the pane in both columns (a cover alone would not be: F-P10-13) |
| 3 | 10.1 | Blender: Oak on the default cube from the Asset Browser, framed close; the lead drags **Overlay 3 Density** 0 → 1 | the dust appears in its colour as a Creator would see it |
| 4 | 10.2 | the same scene; the lead sets the **dust colour** to a soot black | the dust turns dark; the agent then shows the value travelling in the exported USD |
| 5 | 10.3 | Sheets of **Concrete_Smooth_Worn_Dusty** (its dusty defaults), **Copper_Verdigris** (a metal), **Skin_FitzpatrickIII** (scattering and coat) | dust covers each the same way: no shiny metallic dust on copper, no glowing scattered dust on skin |
| 6 | 10.4 | Oak's and Glass_Clear's sheets **with the Unreal column from `unreal-runtime-v3`** | the dust matches in all three tools |

**Reconciled click by click:** clicks 1–3 need only 10.1 (the contract, the assembler, the Blender masters, Oak's and Glass_Clear's recipes, and the Blender library rebuilt and installed). Click 4 needs 10.2. Click 5 needs every dusty article re-assembled (10.3). Click 6 needs the runtime (10.4). No click reaches past its step.

### In now / not now

**In now:**
- **The contract:** `MasterSet.md` §Overlay/MaskSet model (the modulator rule refined, the deposit formula, a Change-log line) · `LCDSchema.md` (the input `overlayN_color`, a Creator port by RD-P10-1) · `AuthoringHarness.md` where it restates the overlay.
- **The tools:** the recipe schema (an optional `color` on an overlay entry) and its validator · the assembler · the Blender masters and `load_article.py` · the Unreal masters and the rig's Unreal driver · the Asset-Browser library rebuilt.
- **Every article that carries dust (13)** given its colour and re-assembled in place (`v01` kept, pre-release; the Phase05 5.3 precedent).
- **The pilot re-frozen:** `matterlib-0.1.0` carries three of the 13 (Concrete_Smooth_Worn_Dusty, Copper_Verdigris, Glass_Clear). The maintainer's promote command is handed over at the start of the close (`LOCAL_DELTAS.md`, the publishing row).
- **`unreal-runtime-v3`**, built on the UE machine; publishing it is the lead's act (Phase06 D14).
- **The hand-off:** one `PlatformDependencies.md` row (Studio's masters take the cover through the next runtime and masters package, as P12 did for overlay 3).

**Not now:**
- **Dust as fuzz.** It was tried and not taken (F-P10-12); a soft rim on top of the cover is a later refinement.
- **A grounded dust colour from a database.** Physically Based has no dust entry (searched `dust`, `soil`, `ash`; `Sand` is the nearest). 10.1 picks the value and records its source in the recipes.
- **Further deposit layers** (dirt, soot, pollen): later, in the same shape (F-P10-3).
- **Colour through damage layers**, and localised gloss or colour through a mask (L7).
- **The character uses** (blush, freckles, makeup, prints): fit-set work over `base_color_map`, by CM2 (F-P10-4).
- **The faint `Scuffs01` and `Fingerprints01`:** Library Coverage (F-P10-5).
- **A gate for "colour only from a declared value":** a new gate is a lead ruling, not scheduled (F-P10-7).

### Reuse check

*What does the stack already provide, and which standards does this touch?*
- **OpenPBR's fuzz** (its own definition: *"…microfibers … as well as dust grains"*) was the first candidate, and **it was measured and fails the Outcome face-on** (F-P10-12): fuzz alone moved Oak's close-up 4.5 levels at full dust, against 4.2 for today's colourless dust. The gap that justifies the cover is measured, not hypothetical.
- **The cover is no new BSDF.** It is a `mix` of existing inputs, by the overlay effect every tool already computes. MaterialX has `mix` natively, Blender has Mix nodes, and Unreal has Lerp. The Blender masters already lerp base colour by a weight (transmission, subsurface).
- **Standards touched:** MasterSet's modulator rule (refined, its reason kept: packed data never becomes colour) · the LCD vocabulary (RD-P10-1: additive, library semver-minor, the `overlay3_density` precedent) · the `determinism` lane (articles without a deposit colour must assemble byte-identically) · the linear colour-space rule (the declared colour is `lin_rec709`, like every library constant).

### Decisions that bind

*One authoritative copy. "Taken" = decided by measurement or precedent in this discovery, not a lead ruling.*
- **The deposit cover** (F-P10-12, F-P10-13, taken): for a deposit overlay N, with `c = effect_N`:
  ```
  base_color          = mix(base_color, overlayN_color, c)     # after the tint and base_color_map
  base_metalness      = mix(base_metalness, 0, c)
  transmission_weight = mix(transmission_weight, 0, c)
  subsurface_weight   = mix(subsurface_weight, 0, c)
  coat_weight         = mix(coat_weight, 0, c)
  fuzz_weight         = mix(fuzz_weight, 0, c)
  ```
  The normal and roughness parts of the overlay are unchanged. Deposits apply in slot order. The cover comes **after `base_color_tint`**, so a Creator who tints a car red does not tint its dust. **In Blender it comes before the master's own transmission and subsurface base-colour lerps**, because they read the covered weights.
- **Which layer is a deposit:** the recipe's overlay entry carries an optional `color` (linear `color3`). Its presence makes the slot a deposit. The colour is per slot, because Dust01 sits in slot 1, 2 or 3 depending on the article (measured: all three occur).
- **The input's name** follows the slot grammar: `overlay1_color` / `overlay2_color` / `overlay3_color`, declared on an article only for a deposit slot (as `overlayN_density` is only for a carried slot). An **author-tier** input (lane B, the `layer_blend_balance` path through `load_article.py` and the Unreal driver). It is also a Creator port (RD-P10-1), from 10.2.
- **The modulator rule, refined:** *"An overlay's packed channels never become colour. A deposit overlay covers the surface with its declared colour, weighted by its effect."* The 2026-07 history line stays; a Change-log line is added.
- **No bridge for the Unreal column before `v3`** (F-P10-14, taken).
- **The character uses stay out**, by CM2 (F-P10-4).

### Risk lane — `build`, controls read

- **Contract:** the same shape as Phase09's `base_color_map` and Phase04's `overlay3_density`, both of which ran in `build`. **Read:** `assemble_mtlx.py` (the `Overlay` dataclass, the effect, the base-colour chain), `recipe.schema.json` (overlay items are `additionalProperties: false`, so `color` must be added there), `LCD_PORTS` (defined in `assemble_mtlx.py` and `blender/addons/imrsv_lcd_export/lcd_usd_edit.py`, read by `validate_recipe.py`, `validate_material.py`, `check_lcd_carrier.py`, `verify_asset_library.py`, `matter_proxy.py`, `make_preview.py`, the rig and its Unreal driver). `LCD_PORTS` gains the port at 10.2 (RD-P10-1).
- **What enumerates the trees this phase changes:** the pilot's freeze hashes its payload, and **3 of the 13 re-assembled articles are in it**, so a re-freeze and the maintainer's promote are scheduled. The `determinism` lane re-assembles every article, which is the guard that nothing else moved. **No gate globs `docs/`** (read: `run_all.py`, `validate_recipe.py`, `check_fixture_sync.py` mention it only in comments), so the probe files beside this doc are inert.
- **`check_exporter.sh`:** runs only if 10.2 lands (a change under `blender/addons/`), **baselined before the edit** (`LOCAL_DELTAS.md`).
- **The public edge:** none in the repo. Publishing `unreal-runtime-v3` and pushing are public and the lead's, at named points.
- No sign-in, secret, destructive migration or data loss.

### Step list

- **10.1 — Dust covers in its colour, in the article and Blender.** The contract text; the recipe `color` and its validator; the assembler; the Blender masters and `load_article.py`; Oak and Glass_Clear given the colour and re-assembled; the Blender library rebuilt and installed. *First clickable result: clicks 1–3.*
- **10.2 — The Creator picks the dust colour.** *(RD-P10-1.)* `overlayN_color` joins `LCD_PORTS` and the exporter; the rig sweeps it. *Click 4.*
- **10.3 — Every dusty article.** The other 11 given the colour and re-assembled (Concrete_Smooth_Worn_Dusty, Copper_Verdigris, ABS_Glossy, Earthenware_Natural, Glass_Green and the 6 skins); the Blender library rebuilt; the pilot re-frozen. *Click 5.*
- **10.4 — Unreal.** On the UE machine: the masters take the cover, `unreal-runtime-v3` built and published by the lead, then pinned here. *Click 6.* Then the hand-off row and the close.

### Compact build map

- **The assembler** (`tools/converters/assemble_mtlx.py`): `Overlay` gains `color: Optional[str]`. For a deposit slot it emits the interface input `overlayN_color` and a `mix` after `base_color_tinted`. The covered weights go to the shader through new graph outputs, for whichever of metalness, transmission, subsurface, coat and fuzz the article authors. **A deposit with none of those authored touches only the base colour.** Byte-identical when no `color` is set.
- **Recipes:** `color` on the Dust01 entry of the 13 recipes listed by `grep -l Dust01 tools/converters/recipes/*.json`.
- **Blender** (`blender/masters/build_masters.py`): per slot in `OVERLAYS`, an `overlayN_color` socket (default white) and a **cover weight** that is 0 unless the article declares a deposit, so a master instance without one is unchanged. Lerps placed before the transmission and subsurface base-colour lerps. `load_article.py` sets the socket and turns the cover on.
- **Unreal** (`unreal/MatterRuntime/Scripts/build_masters.py`): the overlay loop runs **after** `feed(base, "base_color")` today, so the base colour, metalness and the pass-through weights (`TRANSMISSION`, `SUBSURFACE`, coat, fuzz) must be fed after the overlays. The rig's driver (`tools/parity/drivers/unreal.py`) passes `overlayN_color` and the cover. **Check at 10.4:** the translucent masters read a per-pixel transmission weight.
- **The rig:** under (b), a `SWEEP` row for the colour.
- **Docs:** `MasterSet.md` (§Overlay semantic, the rule, Change log) · `LCDSchema.md` · `AuthoringHarness.md` · `PlatformDependencies.md` (the row) · `Glossary.md` (*deposit layer*).
- **Test surface (the `build` ceiling):** the existing `run_all.py` lanes (the `determinism` lane is the main guard), unit tests beside the assembler's for the deposit and no-deposit cases, and **one real-path smoke: the rig sheets of the first human test.** No new gate.

### Lead calls

**RD-P10-1 — answers Q-P10-1: the Creator can change the dust colour, (b).** The lead, 2026-10-01, verbatim: *"b, go ahead with /execute Phase 10"*. Step 10.2 runs.

**Q-P10-1 [lead] — Who picks the dust colour?** → RD-P10-1 *(Four tests run at Pass 1: no ruling answers it; necessary, since the Outcome says "in its own colour"; both options deliverable in all three tools; both admissible. Pass 2 measured the cost.)*
- **(a) The article sets it.** An author value (`overlayN_color`, lane B), like `fuzz_color` today. A Creator turns the dust up but not recolours it, at least not in Studio: in Blender the value is a socket on the master and can be changed locally, but it **does not travel**, because only Creator ports are exported. **Cost:** none beyond 10.1.
- **(b) The Creator can change it.** The same input, also a Creator port, carried from Blender to Studio, so desert dust or soot is one setting away. **Cost: step 10.2.** `LCD_PORTS` in its two definitions and the 7 readers above; the exporter under `blender/addons/` (so `check_exporter.sh`); a frozen-vocabulary evolution (semver-minor, as `overlay3_density`); Studio's Creator controls in the hand-off row.
- **(a) is a strict subset of (b)**, so (b) can also come later, additively.
- **Recommendation: (b), now.** It is the lead's LCD intent: *"in blender a creator adds matter … and tweek a few params … then when they come into Studio with those params, they have a starting point"* (`_Architecture.md` §LCD). Dust's colour belongs to the scene the object sits in, not to the matter.

---

## Why this is a phase

One contract change carries it. `MasterSet.md` §Overlay/MaskSet model says, as a normative rule, *"an overlay never tints"* (`base_color: UNTOUCHED`). Letting a wear layer carry colour changes that rule, and every implementation of the overlay formula moves with it: the assembler, the Blender masters, the Unreal masters (and so the pinned Unreal runtime), the rig, and Studio's masters (a hand-off). Library Coverage depends on it, because every article it builds carries these layers (C1, *"smart, not lean"*).

## Findings

*Pass 1 and Pass 2, distilled. Pass 1's working direction, "dust drawn with OpenPBR's fuzz", is superseded by F-P10-12.*

- **F-P10-1 — OpenPBR's fuzz is the stack's own dust layer, and every tool renders it** (the assembler since Phase07 7.3, Blender's Sheen, Epic's OpenPBR function, Storm: learning S8). It was therefore the reuse check's first candidate. *Superseded as the mechanism by F-P10-12.*
- **F-P10-2 — "Grime" is a mask, not a layer.** `Grime01` decides *where* wear may appear; there is no grime overlay. "Grime that shows its colour" is dust placed by that mask.
- **F-P10-3 — Only deposit layers want colour.** Of the 5 overlays, `Dust01` is a deposit; `Scratches01`, `Scuffs01` and `EdgeWear01` are damage (they reveal what is underneath: L7, not now); `Fingerprints01` is gloss. Later deposits (dirt, soot, pollen) take the same shape.
- **F-P10-4 — The character uses are out, by the lead's ruling CM2.** A blush, freckles, makeup or a print is drawn on one mesh's layout, which is fit and supplied at binding like `base_color_map` (`Taxonomy.md`: *"Anything bound to one mesh … stays outside the taxonomy"*). Answers seed question 2.
- **F-P10-5 — The layers' strength, measured** (mean alpha = coverage; mean B = roughening): `Dust01` 39 % / 0.47 · `EdgeWear01` 9 % / 0.03 · `Scratches01` 7 % / 0.06 · `Fingerprints01` 4 % / 0.02 · `Scuffs01` 3 % / 0.01. **Dust is not faint; it is colourless.** The faint damage layers stay with Library Coverage. Answers seed question 3.
- **F-P10-6 — One edit per tool, not per master.** The assembler (every article), Blender (`OVERLAYS = (1, 2, 3)` on every `ML_<Master>`) and Unreal (`build_master` for all 8 masters) each implement the one overlay formula once. Answers seed question 4.
- **F-P10-7 — Nothing enforces the modulator rule** (no validator or conformance check looks for it; only G6's albedo range exists). The refined rule keeps its reason by construction: the colour is a declared value. A gate would be a new lane, so it is a lead ruling and not scheduled.
- **F-P10-8 — Who picks the dust colour is the lead's call:** it is Q-P10-1. It may change the Creator vocabulary all three tools and Studio share, and no doc decides it.
- **F-P10-9 — Two machines, as Phase09.** The article, Blender and Storm are built and judged here. The Unreal masters are built on the UE machine and published as `unreal-runtime-v3` (the lead's act).
- **F-P10-10 — Studio's cost is small.** Studio adopts the library's Unreal masters (P20), so the cover reaches it through the next runtime and masters package, plus one hand-off row.
- **F-P10-11 — Lane `build`.** See §Risk lane, now verified against the tree (Pass 2).
- **F-P10-12 — Fuzz alone does not show dust face-on; a colour cover does** (Pass 2 probe, Storm, Oak's close-up, dust 1 against 0; `Phase10_ColouredWearLayers_probe.py`, sheet `…_probe.jpg`):

  | Drawing | Picture moved | Mean change (8-bit levels) |
  |---|---|---|
  | today (roughness + bump) | 26 % | 4.2 |
  | fuzz in the dust colour | 81 % | 4.5 |
  | colour cover | 84 % | 16.9 |
  | fuzz + cover | 84 % | 19.3 |

  Fuzz spreads a faint sheen across the whole face but changes it no more than today's dust. The cover is about 4× stronger and reads as dust. Fuzz on top adds 14 % more. **Taken: the cover is the mechanism, and fuzz is not used.** This also removes the collision Pass 1 found with the 13 articles that use fuzz for their own look: the cover lowers their fuzz under dust instead of combining two fuzz sources.
- **F-P10-13 — On glass, the cover must also take away transmission** (the same probe, Glass_Clear):

  | Drawing | Picture moved | Mean change |
  |---|---|---|
  | today | 6 % | 7.8 |
  | colour cover only | 84 % | 4.3 |
  | cover + transmission → 0 | 83 % | 34.5 |

  Through a transmissive pane the base colour barely shows, so dust is a deposit that covers the whole surface, not a paint. By the same reasoning, metal, scattering, coat and fuzz under dust go to none (§Decisions that bind). Copper (metal) and the skins (scattering, coat) are the articles to check at click 5.
- **F-P10-14 — The Unreal column cannot be bridged before `v3`.** Phase09 bridged `v1` in the rig's driver (F-P09-14) because its change was a parameter the old masters already had. A per-pixel cover needs the master graph itself. Until 10.4, the Unreal column renders today's colourless dust, and the rig's Moved verdict reads the dust rows as one-sided. That is expected; it is no regression.
- **F-P10-15 — Dust occupies different slots.** Of the 13 recipes carrying `Dust01`, some put it in slot 1, some in 2, some in 3, so the colour is per slot (§Decisions that bind).
- **F-P10-16 — The pilot carries three dusty articles** (`matterlib-0.1.0.lock.yaml`: Concrete_Smooth_Worn_Dusty, Copper_Verdigris, Glass_Clear). Re-assembling them invalidates the freeze.

## Seed questions — where each stands

| # | Question | Where it stands |
|---|---|---|
| 1 | Where the colour comes from | **A declared colour on a deposit slot, drawn as a cover** (F-P10-12, F-P10-13). Who may change it: **the Creator** (RD-P10-1). |
| 2 | The character uses | **Out, by CM2** (F-P10-4). |
| 3 | Wear you can see | **Dust: the cover, this phase. `Scuffs01` / `Fingerprints01`: Library Coverage** (F-P10-5). |
| 4 | Which masters | **One edit per tool, every master** (F-P10-6). |
| 5 | The modulator rule | **Refined, reason kept:** packed data never becomes colour; the colour is declared (§Decisions that bind). |
| 6 | Additive | **The `determinism` lane is the guard**; no `color`, no change. |
| 7 | Risk lane | **`build`, verified** (§Risk lane). |

## Sources (pointers, not copies)

- `docs/specs/Ontology/MasterSet.md` §Overlay/MaskSet model · `docs/specs/Contract/LCDSchema.md` (§Creator-adjustable subset, the render-role table, §Base colour map) · `docs/specs/Ontology/Taxonomy.md` (CM2's boundary).
- `docs/Planning/Research/260927_R_CharacterMaterials_MPFB2.md` (CM-Q5) · `docs/Planning/Research/260928_R_PlatformAppearanceAsks.md` (AP-F9, A7) · `docs/Planning/Research/260925_R_LibraryCoverage_FirstRelease.md` (Pass 5, L7).
- `docs/Planning/Phases/Complete/Phase07_CharacterMaterials.md` (L3) · `Phase05_TestRig.md` (5.2 F11, 5.3) · `Phase09_HairAndEyeMasters.md` (F-P09-14, the `v1` bridge) · `docs/Planning/Phases/Future/PhaseTBD_LibraryCoverage.md` (F-LC-7).
- The probe: `Phase10_ColouredWearLayers_probe.py` (re-runnable; writes to `/tmp`) and its sheet `Phase10_ColouredWearLayers_probe.jpg`.
- Learnings read: MaterialX (M1, normals in tangent space, untouched here) · Blender (B5, B9) · Unreal (U1, U3, U11: a scatter colour of 0 hangs the GPU, relevant where `subsurface_color` reads the covered base colour) · Storm (S8) · Claude Code: no bearing.

## Discovery Log

- **Pass 1 (2026-10-01)** — the contract and the three tools read against the Outcome. It found fuzz as the reuse candidate, grime as a mask, the character uses out by CM2, and dust colourless rather than faint, and it put Q-P10-1 to the lead. Its findings are kept above with their ids unchanged.
- **Pass 2 (2026-10-01)** — the probe (fuzz fails face-on; the cover works, and on glass it must take transmission too), the slot spread, the pilot's three articles, the Unreal master's feed order, the Blender lerp order, the `LCD_PORTS` readers, and the Brief written. **No lead input arrived between the passes;** Q-P10-1 stays open.

## Discovery Status

- **Passes captured:** 2 (2026-10-01). **The Brief is complete**; Q-P10-1 was ruled at the start of execution (RD-P10-1).
- **Working direction:** a deposit layer covers the surface in its declared colour; fuzz is not used; the character uses are out (CM2); the faint damage layers stay with Library Coverage.
- **Open decisions:** none. Q-P10-1 was ruled (b) at the start of execution (RD-P10-1).
- **Checks carried to execute:** the dust colour's value and source (10.1) · the Unreal translucent masters with a per-pixel transmission weight (10.4) · the U11 floor still holding where `subsurface_color` reads the covered base colour (10.4).

## Execution Log

**Run 1 (2026-10-01, the library machine).** The lead drives each click; Blender sittings are built headless and opened in his Blender.

**Deviations from the Brief (2026-10-01):**
- **The recipe names the port, not a bare `color`:** an overlay entry carries `"color_port": "overlayN_color"` beside `density_port`, and the start value is the port's default (`DUST_COLOR`) or the recipe's `lcd_defaults`. Since RD-P10-1 makes the colour a Creator port, this is the grammar `density_port` already uses; a bare `color` would have been a second place to hold one value.
- **The ports joined `LCD_PORTS` at 10.1, not 10.2:** the assembler's vocabulary is where the article declares them. 10.2 keeps what makes them TRAVEL: the exporter, the Blender wrapper's travel ports, the rig's colour row.
- **Fixed in 10.1, a defect of 10.1's own (CAUGHT by the first rig run, not a gate):** a deposit routes a covered weight (`transmission_weight`, …) through the graph, so it is no longer a value on the shader, and the one shared reader (`blender/masters/article.py`) dropped it: Blender would have shaded Glass_Clear opaque. The reader now takes the weight's own value from the first deposit mix. The rig's mask row also turned every `overlay*` port to 1.0, the colour port included; it now selects `*_density`.
- **The Unreal driver passes the deposit now** (`overlayN_color`, `overlayN_deposit = 1`): Unreal ignores a parameter a master lacks, so `v2` draws today's colourless dust (F-P10-14) and 10.4's masters take the same names.

| Step | Commit | Result | Next |
|---|---|---|---|
| 10.1 | `ff70d52` | ✅ **Clicks 1–3, the lead (2026-10-01), on the dust rows (Oak, Glass_Clear; Storm and Blender) and Oak on the cube in Blender:** *"pass on 1-3, dust looks right, carry on with 10.2"*. Built: the Creator ports `overlay1_color`…`overlay3_color` (default Sand desaturated halfway: `0.413, 0.386, 0.308`); the deposit cover in the assembler; Blender masters v8 (`overlayN_color`, `Overlay N Deposit`); the loader; the recipe lane's G7 rules and the RED fixture `deposit_wrong_slot.json`; MasterSet, LCDSchema, Glossary, Experience. Oak and Glass_Clear re-assembled in place. **Rig (Storm vs Blender, dust at 1, close-up):** Oak moved 9.35 / 8.28, between the tools 1.14 (under the flag); Glass_Clear moved 8.54 / 6.81, between 7.61 (advisory: Glass_Clear sat at 10.9–11.1 before this phase, Phase05/06). Unreal (`v2`) ONE-SIDED on the dust rows, as F-P10-14 says. **Gate:** 13 PASS, 2 SKIP, 2 FAIL: `approval_binds_freeze` (inherited since Phase04) and `release_verify` (Glass_Clear is in the pilot; re-freeze at 10.3). Determinism byte-stable for every other article. **Blender library:** rebuilt, 57 articles, `check_asset_library.sh` PASS. **`check_exporter.sh` baseline before 10.2:** three carrier steps red, `check_lcd_carrier.py` imports the assembler under a `pxr` Python with no MaterialX (the same import at `HEAD`, so inherited); every other step PASS. | 10.2 |
| 10.2 | `758b204` | ✅ **Click 4, the lead (2026-10-01), in Blender, the dust colour swatch on Oak:** *"pass on 4, dust goes dark, carry on with 10.3"*. **Its export half (the agent's), from the lead's own session:** the scene read back with the default dust colour (the change had not stayed), so soot was set on the same material by the agent and exported: `color3f inputs:overlay3_color = (0.04, 0.035, 0.03)`, connected into `NG_*`. **F-P10-17 (not this phase's, found here):** that export also carries `userProperties:ml_article = "/home/peter/…"`, an absolute author-machine path, from `load_article.build`'s `mat["ml_article"]` (since Phase05, `b607a7b`); `assert_profile.py` 6b only matches `@…@` and `value="…"`, so `check_exporter.sh` passes it. The dust colour travels: `overlayN_color` in the exporter (`lcd_sparse.LCD_TRAVEL_PORTS`, `lcd_usd_edit.LCD_PORTS`, color3 0–1), the Blender wrapper's travel ports (`load_article.TRAVEL_PORTS`), `verify_asset_library`; the rig's row *"wear N at 1, soot"*. **Export, headless, from the sitting's own scene:** soot set → `color3f inputs:overlay3_color` on the Material, connected into `NG_*` (the Carrier rule); colour untouched → no `overlay3_color` (sparse). **Rig, Oak, dust at 1 in soot:** Storm moved 5.67, Blender 6.03, between the tools 0.92 (close-up 0.79), under the flag; Unreal `v2` unmoved. **`check_exporter.sh`:** the same set as the baseline (the inherited carrier-step reds), 64 PASS before and after. **Blender library** rebuilt, `check_asset_library.sh` PASS. | 10.3 |
