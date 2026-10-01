# Phase10 — Library Coverage

**Status:** SEEDED (phase doc written 2026-09-25; discovery has not opened). **Numbered Phase10 by the lead, 2026-10-01** (*"/discovery docs/Planning/Phases/Future/PhaseTBD_LibraryCoverage.md as Phase10"*), after Phase09 closed. **Un-numbered by the lead, 2026-09-28** (it was Phase08), verbatim: *"make this Phase 8, mark the current Phase8 as TBD - we have many other little things to get in here befoer we build out the full library."* Character Appearance for Studio took Phase08. *(Anything written before 2026-09-28 that says "Phase08", including closed phase docs and research, means this phase.)* **Earlier: renumbered Phase07 → Phase08 by the lead, 2026-09-27** (research `260927_R_CharacterMaterials_MPFB2.md` CM4): Character Materials takes Phase07 and runs straight after Phase05, so Studio's characters get library materials first. *(Quotes and pointers below that say "Phase07" were written when this phase held that number.)* **Earlier: renumbered Phase05 → Phase07 by the lead, 2026-09-26:** the test rig (Phase05) and the Unreal test runtime (Phase06) now come first, so every material this phase builds is checked in all three tools. **Reevaluate (2026-09-26):** this phase is expected to be re-cut as the nightly build loop over a wish list (`260926_R_BigPicture_NimbleSetup.md` Pass 9); the scope below predates that and is kept until discovery re-cuts it. Originally numbered by the lead, 2026-09-25, verbatim: *"i and then seed phase 5 and that will be building materials"*. It follows Phase04 (Wear Layers at Their Own Scale) and precedes the release bundle: *"we have 200 materials to build and test before we have our first versionable library"* (lead, 2026-09-25, `260925_R_DraftsInUSDLiveView.md` Pass 5).

## Outcome

**Creators find materials for every class of matter in the taxonomy, including the classes IMRSV's character work needs (skin, cloth, hair).**

*(Verbatim from the Roadmap entry; see question 1, which the seed's sources put under test.)* **Reevaluate (2026-09-27):** the character classes named here (skin, hair, and the character side of cloth) are now **Phase07 Character Materials** (CM4). This phase keeps the rest of the taxonomy, including the textile class; Phase07 pulls a few clothing fabrics forward. The Outcome text is kept as written until the lead restates it. Concretely, at close: the library is built out from the 17 `.mtlx` on disk (system and reference articles included) toward the ~173 of the draft list (`260925_R_LibraryCoverage_FirstRelease.md` Pass 2). Each article is generated with the Phase03 tools, carries its wear layers at strength 0 (ruling C1), and is kept by the lead in USDLiveView.

## Why this is a phase

It is **the** material-building phase: the lead's "building materials". It is the first real use of Phase03's agent at volume, and it is what makes a library worth versioning, which the release bundle then publishes. **Split signal, raised at seed:** it is certainly more than 60–90 minutes to the first click at full size, and the list is naturally cut by class. Expect discovery to propose tranches (by class or by lane) as steps, or to split. Cut last, on the full picture.

## What it consumes (measured 2026-09-25; re-verify at Pass 1)

- **From Phase03:** the `/matter-generate` skill (`.claude/skills/matter-generate/`), the recipe schema and lane, the layer-generation path (`tileable.py` and generators), the ambientCG importer, the Physically Based lookup, and the preview render.
- **From Phase04:** the layer-scale contract and the regenerated, tiling shared layers. Every article carries up to three layers, so this is a hard dependency.
- **The dev loop:** `tools/releases/serve_to_stage.py` → USDLiveView (no versioning, no release: lead 2026-09-25).
- **The draft list:** 173 articles (11 shipped then, 162 new), each with a stem, class, master, lane, scale, status and wear layers. The research's own status: "nothing is committed". The lead's mark-up is its next step. The research counts 140 as buildable with the Phase03 tools alone.

## Scope

**In:**
- Building the new articles, and the shared layers the list assigns: 22 in total (13 overlays, 9 masks). 9 are on disk (5 overlays, 4 masks, counted 2026-09-25), so 13 remain to make.
- Articles on disk updated to carry their relevant layers (C1). They keep their `v01` in place: the lead's "no versioning" ruling (2026-09-25); research L8, answered.
- The lead's rulings the list is waiting on (naming N1–N8, structure S1–S6), landed in `NamingConventions.md` / `Identity.md` / `Taxonomy.md` before the names they fix are built. *(Names are expensive once released; they are cheap now.)*

**Not now (unless discovery pulls them in):**
- **The author-tier carriers the assembler lacks:** C1 (F82 / `specular_color`, 8 metals), C2 (coat / sheen, 10 articles), C3 (anisotropy, 3), and a possible fourth, thin film (research L3). They are real OpenPBR inputs, a harness change rather than material work. See question 3.
- Localised colour or gloss through a mask (L7).
- Cutting, versioning or publishing a release: **Release Bundle and Consumer Contract** and **Version Management**.
- The catalog listing each article's layers and master (L9): the release bundle's catalog `schema_version` bump.

## Seed-vs-docs questions (for discovery; the four fork tests were run as each was written)

1. **Skin, cloth and hair in the Outcome vs the research.** The Roadmap Outcome names them. The coverage research (O9) says skin, hair, bone and nails have **no class**, that hair is **not a surface material** in this model, and that `PlatformDependencies.md` M1 is still pending the platform's decision ("whether it integrates the library or side-lines it is still open"). Cloth does exist (the textile class). **A genuine lead call, but not until Pass 1 has read `Taxonomy.md` and the textile rows:** is the Outcome narrowed to the taxonomy's classes, with the character classes a later phase, or does this phase add a biological class? *(The Outcome is not rewritten at seed.)*
   **→ Ruled 2026-09-27 (lead, research CM1–CM3, `260927_R_CharacterMaterials_MPFB2.md`):**
   - This phase adds the **`biological` Domain** and builds **six skin articles**, `Skin_FitzpatrickI…VI`, on the **Subsurface** master (Physically Based values + MPFB2's CC0 roughness/pore settings + one tiling pore overlay; research Pass 6d).
   - Keep `subsurface_color` equal to the base colour, or unset, so Blender matches (research Pass 8a).
   - The rest of the character matter (lips, nails, eyes, teeth, hair, fit sets and their contract calls) is **`PhaseTBD_CharacterMaterials.md`**.
   **→ Superseded the same day (lead, CM4):** the six skins **and** the `biological` Domain move to **Phase07 Character Materials** (`Phase07_CharacterMaterials.md`), which runs before this phase. Nothing character-specific remains here.
2. **Is this the whole ~173, or a first tranche?** Research L5 estimates 15–25 hours of review at 5–10 minutes per article (unmeasured). The lead's "200 materials before our first versionable library" suggests the whole set. Discovery should measure real review time on the first steps before cutting.
3. **Carriers C1–C3: in or out?** Building them unblocks 21 articles. That is an assembler plus contract change (lane A, no Creator change), and it may be its own small phase ahead of the blocked tranche. *Discovery reads the carriers section of `260923_R_AgenticMaterialGeneration.md` (Pass 11, O5) before offering the choice.* **Update (2026-09-27, CM4):** **C2 (coat) is pulled forward into Phase07 Character Materials** (skin oil sheen). Check Phase07's close for what landed before deciding C1 and C3 here. **Drift (2026-09-28, Phase08 F-P08-6): C2 and C3 are built.** Phase07 landed coat, fuzz (sheen) and specular anisotropy (lane A), and Phase08 used them on fabrics (`Satin_Natural`: anisotropy; felt, canvas, knit, suiting: fuzz). The draft list's `C2` / `C2 + C3` blockers on Suede, Velvet and Satin are stale; **only C1 (F82 / `specular_color`) and thin film remain.** **Already built by Phase08 (2026-09-28); the list's rows stay as written, and this phase skips them:** `Canvas_Natural`, `Felt_Natural`, `Satin_Natural` (textile rows 2, 7, 12, as L2 generated textures, not the L3 scans the list proposed) and `Rubber_Natural` (polymer), plus `Leather_Natural`, `Denim_LightWash`, `StretchKnit_Natural` and `WoolSuiting_Natural`, which the list did not have. They carry no wear layers, as every shipped textile; the list's layer sets for them are still intent.
4. **The gut-check the list is waiting on.** N1–N8 and S1–S6 (partly superseded by C5 and resolved rulings E1, E2, E5). Discovery compiles what is still open into one lead pass, rather than asking row by row.
5. **The layer library as a deliverable:** generate procedurally (L2) or convert ambientCG's imperfection sets (research Pass 9)? This is decided per layer by the skill today. Confirm that no policy is needed.
6. **The risk lane.** The hypothesis is `build`: content and generators, with no authorization, secrets or public edge. The push is irreversible, and the lead gates it.
7. **A seam guard lane over `MatterLibrary/textures/shared/**`?** Routed from Phase04's close: the old layers' seams went unnoticed through every earlier phase, and this phase adds 13 layers. A new gate needs the lead's ruling; Phase04 recommended yes. *The check Phase04 used: mean wrap-edge difference vs mean interior neighbour difference per axis.*
8. **Do the per-article base textures from the pre-Phase03 generators tile?** (Lace, Marble, Rust base sets; `tileable.py`'s docstring says those generators "can show a seam"; unmeasured.) A pre-existing defect routed from Phase04's close. Measure before building on them.
9. **Layers are now sampled at their own size** (Phase04, `MasterSet.md` §Scale): a new layer's scale tag is its rendered size, and a recipe's `meters_per_tile` must be the article's real tile size.
10. **The wear layers are too faint to see** (routed from Phase05 step 5.2, lead 2026-09-27: *"Phase07, carry on with 5.3"*). On Phase05's close-up (a 1 cm grain ≈ 15 px), Oak with dust at full strength looks the same as at defaults. Measured on the textures: **Scuffs01 is nearly empty** (alpha mean 0.03, so 3 % coverage; roughness bias 0.01; near-flat normals), and needs regenerating with real coverage. **Dust can only roughen and bump**: MasterSet's normative rule "an overlay never tints" leaves a dust or grime layer no way to show its colour, and on a rough material the roughening barely registers. Whether wear layers such as dust and grime may carry a colour is a **contract change** (MasterSet, LCDSchema, every consumer's master), so it is the lead's call at discovery. The rule exists because packed data was once painted on as colour, so a fix adds a colour channel rather than dropping the rule. Judge the result on the rig: `uv run tools/parity/rig.py <article> --sweep`, close-up rows. **Update (2026-09-27, CM4):** the **colour-channel half** of this question is ruled in **Phase07 Character Materials** (research CM-Q5: region tone, freckles and makeup need the same change). Regenerating Scuffs01 stays here. **Update (2026-09-27, Phase07 ruling L3):** Phase07 builds the colour channel only if its rig shows skin needs it. Phase07 splits character regions by mesh, so by default **the colour channel comes back here, with dust** (see `Phase07_CharacterMaterials.md` §Lead rulings). Check Phase07's close for whether it landed.

11. **Reevaluate under the lead's LCD ruling (added 2026-09-28)** (`_Architecture.md` §Design principles): the LCD is the shared parameter vocabulary, not a shared ceiling. *"we use the master materails to lean in on the egines BEST qaulities to make the material look as good as it can"*. For this phase:
    - **Every article states the real substance.** A value is never lowered or dropped because one viewer cannot show it: a check of the recipes on 2026-09-28 found none that had been (skin keeps its scatter anisotropy although Storm ignores it). Keep it that way at volume.
    - **Masked articles take soft coverage** once Phase08's Hair master proves it (the lead's pick for hair: *"I do think c soft edges is the way"*). `Lace_Floral`'s hard 0.5 cut-out is the first to revisit; perforated metal and leaf cards follow.
    - **The rig's bar.** `tools/parity/rig.py` passes or fails on ΔE < 2 between Storm's and Blender's pictures (`BAR`, `GRADED`). The ruling makes the criterion **"does each slider move every tool the same way"** (the rig's "Moved" column, and its ONE-SIDED flag), with picture ΔE kept as a bug-finding diagnostic. **Todo:** change the rig before reviewing ~170 articles against it, or the review will reward sameness over quality. A change to a gate's criterion is a lead ruling; this ruling is it.
    - **The earlier "subsurface colour equal to the base colour, so Blender matches"** (question 1, research Pass 8a) was already superseded by Phase07 (the Blender masters mix subsurface colour as OpenPBR does). It is superseded twice now.

## Sources (pointers, not copies)

- `docs/Planning/Research/260925_R_LibraryCoverage_FirstRelease.md`: rulings C1–C6; the list (Pass 2); Passes 3–7; Gut-check N/S; Open L1–L10.
- `docs/Planning/Research/260923_R_AgenticMaterialGeneration.md` (D1–D8; carriers C1–C3, Pass 11; O5).
- `docs/Planning/Phases/Complete/Phase03_AgenticMaterialGeneration.md` §Not now ("Filling the library ... consumes from this phase").
- `docs/specs/Ontology/{Taxonomy,Identity,MasterSet}.md` · `docs/NamingConventions.md` · `docs/Planning/PlatformDependencies.md` (M1, P12).

## Discovery Log

_(numbered passes accrue here)_

## Discovery Status

- **Passes captured:** — (seed only)

## Execution Log

_(populated during execution)_
