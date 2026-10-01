# Phase10 — Coloured Wear Layers

**Status:** SEEDED (2026-10-01; phase doc exists; discovery opens next). **Numbered Phase10 by the lead's ruling, 2026-10-01**, verbatim: *"If 2 then we need to do that phase now instead."* ("2" was Library Coverage's Pass 1 proposal to give colour on wear layers a phase of its own.) Library Coverage, which held Phase10 for part of that day, is un-numbered again (`PhaseTBD_LibraryCoverage.md`). That follows the lead's own precedent of 2026-09-28: *"make this Phase 8, mark the current Phase8 as TBD"*.
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

_(numbered passes accrue here: examined → finding → decision / hypothesis / open question)_

## Discovery Status

- **Passes captured:** —
- **Current working direction:** —
- **Open decisions:** —
- **Checks to carry forward:** —

## Execution Log

_(populated during execution)_
