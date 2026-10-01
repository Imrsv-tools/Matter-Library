# Phase10 — Coloured Wear Layers

**Status:** DISCOVERY (opened 2026-10-01; Pass 1 captured). **Numbered Phase10 by the lead's ruling, 2026-10-01**, verbatim: *"If 2 then we need to do that phase now instead."* ("2" was Library Coverage's Pass 1 proposal to give colour on wear layers a phase of its own.) Library Coverage, which held Phase10 for part of that day, is un-numbered again (`PhaseTBD_LibraryCoverage.md`). That follows the lead's own precedent of 2026-09-28: *"make this Phase 8, mark the current Phase8 as TBD"*.
- **Seeded from:** Library Coverage's seed question 10 and F-LC-7 · Phase07's ruling L3 (*"by L3's default the colour channel goes to Phase08 with dust"*, its close) · research `260927_R_CharacterMaterials_MPFB2.md` CM-Q5 · Phase05 step 5.2's finding F11 (the wear layers are too faint to see).

## Outcome

**A Creator who turns up a wear layer such as dust or grime sees it in its own colour, not only as a change in shine, and it looks that way in Blender, a USD viewer and Unreal.**

*(Seed wording; discovery tests it. Seed question 2 asks whether the character uses of the same idea, a blush, freckles, makeup or a garment's print, belong in it.)*

## Why this is a phase

One contract change carries it. `MasterSet.md` §Overlay/MaskSet model says, as a normative rule, *"an overlay never tints"* (`base_color: UNTOUCHED`). Letting a wear layer carry colour changes that rule, and every implementation of the overlay formula moves with it: the assembler, the Blender masters, the Unreal masters (and so the pinned Unreal runtime), the rig, and Studio's masters (a hand-off). Library Coverage depends on it, because every article it builds carries these layers (C1, *"smart, not lean"*).

## Scope

**In (seed):**
- The contract text: how a wear layer carries colour, in `MasterSet.md` and `LCDSchema.md`, keeping data textures data (seed question 5).
- The tool support: the assembler, the recipe schema and validator, the Blender masters, the Unreal masters (a new runtime build; publishing it is the lead's act, Phase06 D14), and the rig.
- Dust and grime that show their colour on the articles that carry them, judged on the rig in all three tools.
- The hand-off: `PlatformDependencies.md`, so Studio's masters take the same change.

**Not now (unless discovery pulls them in):**
- **Localised gloss or colour through a mask** (wet patches, moss in crevices: coverage research L7). A neighbour of this change, not this change.
- **Building the library at volume:** Library Coverage, after this phase.
- **Strands, card maps:** *Hair That Reads as Hair*.

## Seed-vs-docs questions (for discovery; the four fork tests were run as each was written)

1. **Where does a layer's colour come from, and who may change it?**
   - A colour per overlay slot that the article's author sets.
   - A colour picture shipped beside the shared layer.
   - A new Creator control, so the Creator picks the dust colour.

   Not ruled anywhere: CM-Q5 and Library Coverage's seed both say *"add a colour channel rather than dropping the rule"*, which is the research's proposal, not a ruling. **Run the reuse check first:** OpenPBR has a fuzz layer that its own specification describes as dust and fibres (`fuzz_weight`, `fuzz_color`, `fuzz_roughness`), and Phase07 built it in all three tools (coat, fuzz, anisotropy). Dust may need no new mechanism at all, only an overlay that drives fuzz. Grime (darkening) has no such twin. Pass 1 reads the OpenPBR fuzz definition and the masters' fuzz paths before anything is proposed.
2. **Do the character uses belong here?** CM-Q5 grouped region tone, freckles and makeup with dust colour (*"one contract change should serve all three"*), and the platform's research added garment prints and trims (AP-F9, A7). But those are drawn on one mesh's own layout. That is the fit-set path (`base_color_map`, Phase09), not a shared layer tiled at real size. **Hypothesis: out**, recorded as a later addition over `base_color_map`. Pass 1 tests that against the CM-Q5 text before it is put to the lead.
3. **Wear you can see.** Phase05 F11: `Scuffs01` is nearly empty (3 % coverage), and dust at full strength looked the same as at 0 on Oak's close-up. The Outcome says the Creator *sees* the layer, so regenerating `Scuffs01` (and checking the other 8 layers' strength) is a candidate for this phase rather than Library Coverage. Pass 1 decides.
4. **Which masters carry wear layers?** Every master whose articles declare overlays, in each of the three tools, plus Studio's. Pass 1 enumerates them from the tree (`assemble_mtlx.py`, `blender/masters/build_masters.py`, `unreal/MatterRuntime/Scripts/build_masters.py`) rather than from the docs.
5. **Keeping the modulator rule's reason.** The rule exists because packed data was once painted on as colour. *"A gate for this rule must check *what* changed, not *whether* something did"* (MasterSet). Whatever carries colour must leave the data channels data. Pass 1 reads how the rule is enforced today.
6. **Additive, and invisible until used.** The precedent is `overlay3_density`: an article that does not use the change assembles byte-identically (the `determinism` lane). A new Creator port is an evolution of the frozen vocabulary (library semver-minor).
7. **The risk lane.** Hypothesis `build`: a contract change of the same shape as Phase09's `base_color_map`, which ran in `build`. No sign-in, secret or public edge. Publishing a new Unreal runtime is public and the lead's call (Phase06 D14). Verified at the Brief.

## Sources (pointers, not copies)

- `docs/specs/Ontology/MasterSet.md` §Overlay/MaskSet model (the modulator rule, the overlay formula, the scale rule, linear colour space) · `docs/specs/Contract/LCDSchema.md` (the frozen Creator vocabulary; §Base colour map).
- `docs/Planning/Research/260927_R_CharacterMaterials_MPFB2.md` (CM-Q5) · `docs/Planning/Research/260928_R_PlatformAppearanceAsks.md` (AP-F9, A7) · `docs/Planning/Research/260925_R_LibraryCoverage_FirstRelease.md` (Pass 5, L7).
- `docs/Planning/Phases/Complete/Phase07_CharacterMaterials.md` (L3; its close) · `docs/Planning/Phases/Complete/Phase05_TestRig.md` (5.2, F11) · `docs/Planning/Phases/Future/PhaseTBD_LibraryCoverage.md` (seed question 10, F-LC-7).

## Discovery Log

### Pass 1 — 2026-10-01 — the contract and the three tools read against the Outcome

**Examined:**
- **Specs:** `MasterSet.md` §Overlay/MaskSet model (whole: the modulator rule, the formula, the scale and colour-space rules) · `LCDSchema.md` §Creator-adjustable subset · `Taxonomy.md` (CM2's boundary: *"Anything bound to one mesh … stays outside the taxonomy"*) · `PlatformDependencies.md` (P12, P20, P21, M1–M4).
- **Research:** `260927_R_CharacterMaterials_MPFB2.md` (CM-Q5 and its Pass text) · `260928_R_PlatformAppearanceAsks.md` (AP-F9, A7) · Phase07's close (L3, the unruled soft-detail item).
- **OpenPBR's own definition:** `~/usd-tools/inst/usd-26.03/libraries/bxdf/open_pbr_surface.mtlx`, the fuzz inputs.
- **Tree:** `assemble_mtlx.py` (the overlay formula, the fuzz carrier) · `blender/masters/build_masters.py` (overlays, fuzz → Sheen) · `unreal/MatterRuntime/Scripts/build_masters.py` (the master table, overlays, fuzz) · the validators (for any gate enforcing the modulator rule) · every recipe (which carry overlays, Dust01, fuzz) · the 9 shared layers, **measured**.
- **Learnings:** MaterialX (M1: normals are combined in tangent space; this phase does not touch normals) · Blender (B5, B9) · Unreal (U1: Epic's OpenPBR function takes fuzz; U3: the coat-flattening budget) · Storm (S8: coat and fuzz are honoured in Storm) · Claude Code: no bearing.
- **Machines:** this machine has no Unreal install (`MATTER_UNREAL_EDITOR` unset, no engine found). The Unreal masters are built on the UE machine, as in Phase09.

**Findings:**
- **F-P10-1 — OpenPBR already has a dust layer: fuzz.** Its definition, verbatim: *"The presence weight of a fuzz layer that can be used to approximate microfibers, for fabrics such as velvet and satin as well as dust grains."* It carries its own colour (`fuzz_color`) and roughness. **All three tools already render it**: the assembler carries `fuzz_*` per article (Phase07 7.3), Blender maps it to Principled's Sheen, Unreal passes it to Epic's OpenPBR function, and Storm honours it (Learnings S8). **This is the reuse check's answer.** A dust layer can drive `fuzz_weight` per pixel with a dust colour, with **no new BSDF and no change to the modulator rule** (fuzz is a layer over the surface, not paint on the base colour).
  - **Unproven:** whether fuzz alone *looks like* dust face-on. Fuzz shows mostly at grazing angles, while heavy dust also covers the base colour. Pass 2 runs a disposable probe on the rig: Oak with dust as fuzz only, against fuzz plus a base-colour cover.
  - **A collision to design for:** 13 articles already use fuzz for their own look (the 6 skins and 7 fabrics), and the 6 skins also carry Dust01. Dust and the article's own fuzz must combine (for example the larger weight, colour mixed by weight), not overwrite each other.
- **F-P10-2 — "Grime" is a mask, not a layer.** `Grime01` is a mask (it decides *where* wear may appear: low, protected areas), and there is no grime overlay. So "grime that shows its colour" is **dust or dirt placed by the Grime01 mask**, and the colour belongs to the overlay. The Outcome's wording stands (it reads right to a Creator); the mechanism is one coloured deposit layer, not two.
- **F-P10-3 — Only deposit layers want colour.** Of the 5 overlays, `Dust01` is a deposit. `Scratches01`, `Scuffs01` and `EdgeWear01` are damage (they reveal what is underneath, which is the localised-colour case L7, not now), and `Fingerprints01` is oily gloss (roughness). **Hypothesis:** colour is a property of a deposit layer. Dust now; dirt, soot or pollen later, as new deposit layers in the same shape.
- **F-P10-4 — The character uses are out, by the lead's ruling CM2.** CM-Q5 grouped region tone, freckles and makeup with dust colour, and the platform's research added garment prints (AP-F9). But CM2 (lead, 2026-09-27) puts anything drawn on one mesh's own layout *beside* the library as fit, never in an article (`Taxonomy.md`: *"Anything bound to one mesh, such as a region mask, a painted skin atlas or a hair card's cut-out, stays outside the taxonomy"*). A blush, freckles, makeup or a print is drawn on one mesh's layout, so it is fit, supplied at binding like `base_color_map` (Phase09). **That answers seed question 2**, and the soft-detail item Phase07 left unruled stays open for a later fit-set addition. Recorded here, and put to the lead only if the Outcome is read otherwise.
- **F-P10-5 — The layers' strength, measured** (mean alpha = how much of the tile the layer covers; B = its roughening):

  | Layer | Covers | Roughens (mean B) |
  |---|---|---|
  | `Dust01` | 39 % | 0.47 |
  | `EdgeWear01` | 9 % | 0.03 |
  | `Scratches01` | 7 % | 0.06 |
  | `Fingerprints01` | 4 % | 0.02 |
  | `Scuffs01` | 3 % | 0.01 |

  **Dust is not faint; it is colourless.** It covers 39 % and roughens strongly, but on a rough article such as Oak more roughness barely shows, which is exactly Phase05 F11's *"I don't really see any difference"*. Colour is the missing half, which is this phase. **`Scuffs01` (and probably `Fingerprints01`) are genuinely faint**, but they are damage and gloss layers with no colour. **They stay with Library Coverage**, as its seed already split it (*"Regenerating Scuffs01 stays here"*). That answers seed question 3.
- **F-P10-6 — Which masters, in each tool.** All three tools implement the one overlay formula on every master that carries overlays: the assembler for every article, Blender's `OVERLAYS = (1, 2, 3)` on each `ML_<Master>`, and Unreal's `build_master` for each of its 8 masters (Opaque, TwoLayer, Masked, Hair, Emissive, Subsurface, TranslucentThin, TranslucentThick). Fuzz is already an input of every Unreal master (its defaults table) and of every Blender master. The change is one edit per tool, not one per master. That answers seed question 4.
- **F-P10-7 — Nothing enforces the modulator rule.** No validator or conformance check looks for overlay data reaching the base colour (searched for the rule's words; only G6's albedo range exists). The rule lives only in the spec and in comments. A fuzz-based dust keeps it intact. If Pass 2's probe shows a base-colour cover is needed, then **the colour must come from the layer's declared colour, never from its packed channels**. Seed question 5's *"check what changed"* applies, and a gate for it would be a new lane (a lead ruling, not scheduled).
- **F-P10-8 — Who picks the dust colour is the lead's call** (the one open question, Q-P10-1 below). It changes the Creator's control set, which is the frozen vocabulary all three tools and Studio share (`LCDSchema.md`), and nothing in the docs decides it.
- **F-P10-9 — Two machines, as Phase09.** The MaterialX article, Blender and the rig's Storm column are built and judged here. The Unreal masters are rebuilt on the UE machine, and the runtime is republished (`unreal-runtime-v3`; publishing is public and the lead's act, Phase06 D14). Until then, the Unreal column renders from `v2`, which does not know the change. Phase09 kept that column honest with a small bridge in the Unreal driver (F-P09-14); the Brief decides whether this phase needs one.
- **F-P10-10 — Studio's cost is small.** Studio adopts the library's Unreal masters (P20). A master change reaches it through the next runtime and masters package, plus one row in `PlatformDependencies.md` naming the new input, as P12 did for the third overlay.
- **F-P10-11 — Risk lane: `build`, controls read.** A contract change of the same shape as Phase09's `base_color_map`, which ran in `build`. The guard that matters is the `determinism` lane: articles that do not use the change must assemble byte-identically, as `overlay3_density` did. No sign-in, secret or public edge in the repo. The runtime publish is public, and it is the lead's act at a named step.

**Q-P10-1 — Who picks the dust colour?** *(Four tests run: not answered by any ruling; necessary, because the Outcome says "in its own colour"; both options deliverable in all three tools; both admissible.)*
- **(a) The article sets it.** Each article carries its dust colour (an author value, like `fuzz_color` today). The Creator can turn the dust up but not recolour it. **No change to the Creator controls.**
- **(b) The Creator can change it.** A new Creator control (for example `overlay_deposit_color`, defaulting to the article's own) travels with the Creator's other settings from Blender to Studio, so desert dust or soot is one setting away. **It adds to the frozen Creator vocabulary** (additive, as `overlay3_density` did) and needs the row in `PlatformDependencies.md`.
- **Recommendation: (b).** It is the lead's own LCD intent: *"in blender a creator adds matter … and tweek a few params … then when they come into Studio with those params, they have a starting point"* (`_Architecture.md` §LCD). Dust colour depends on the scene the object sits in, not on the matter.

**Hypothesis for Pass 2 (the Brief):**
- **Steps:**
  - **10.1** dust shows its colour in the article and in Blender, on Oak, Phase05's specimen, after Pass 2's fuzz probe picks the drawing;
  - **10.2** the Unreal masters on the UE machine, and the runtime republished;
  - **10.3** every article that carries dust re-assembled (13 today), the Blender library rebuilt, and the hand-off row.
- **First human test:** Oak's rig sheet with dust swept 0 → 0.5 → 1 in Storm, Blender and Unreal, the dust visibly its own colour in each. Then, in Blender's Asset Browser, Oak dropped on the default cube with the dust slider (and, under Q-P10-1 (b), the dust colour) moved.

## Seed questions — where each stands (Pass 1)

| # | Question | Where it stands |
|---|---|---|
| 1 | Where the colour comes from | **Reuse found:** OpenPBR fuzz (F-P10-1). How it is drawn: Pass 2's probe. Who may change it: **Q-P10-1**. |
| 2 | The character uses | **Out, by CM2** (F-P10-4): mesh-bound pictures are fit. |
| 3 | Wear you can see | **Dust: colour is the missing half, this phase. `Scuffs01` / `Fingerprints01`: Library Coverage** (F-P10-5). |
| 4 | Which masters | **One edit per tool, every master** (F-P10-6). |
| 5 | The modulator rule | **Kept** with fuzz; colour from a declared value, never packed data, if a cover is needed (F-P10-7). |
| 6 | Additive | **The `determinism` lane is the guard** (F-P10-11). |
| 7 | Risk lane | **`build`** (F-P10-11). |

## Discovery Status

- **Passes captured:** 1 (2026-10-01).
- **Current working direction:** dust drawn with OpenPBR's own fuzz layer in a colour; the character uses out (CM2); faint damage layers stay with Library Coverage.
- **Open decisions:** **Q-P10-1** (who picks the dust colour; recommended: the Creator can).
- **Checks to carry forward:** Pass 2's fuzz probe on Oak (fuzz alone vs fuzz + a base-colour cover, in all three tools) · how dust combines with an article's own fuzz (skins, fabrics) · whether the Unreal column needs a bridge before `v3` (F-P10-9).

## Execution Log

_(populated during execution)_
