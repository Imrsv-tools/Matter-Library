# Phase05 — Library Coverage

**Status:** SEED (phase doc written 2026-09-25; discovery has not opened). Numbered by the lead, 2026-09-25, verbatim: *"i and then seed phase 5 and that will be building materials"*. It follows Phase04 (Wear Layers at Their Own Scale) and precedes the release bundle: *"we have 200 materials to build and test before we have our first versionable library"* (lead, 2026-09-25, `260925_R_DraftsInUSDLiveView.md` Pass 5).

## Outcome

**Creators find materials for every class of matter in the taxonomy, including the classes IMRSV's character work needs (skin, cloth, hair).**

*(Verbatim from the Roadmap entry; see question 1, which the seed's sources put under test.)* Concretely, at close: the library is built out from the 17 `.mtlx` on disk (system and reference articles included) toward the ~173 of the draft list (`260925_R_LibraryCoverage_FirstRelease.md` Pass 2). Each article is generated with the Phase03 tools, carries its wear layers at strength 0 (ruling C1), and is kept by the lead in USDLiveView.

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
2. **Is this the whole ~173, or a first tranche?** Research L5 estimates 15–25 hours of review at 5–10 minutes per article (unmeasured). The lead's "200 materials before our first versionable library" suggests the whole set. Discovery should measure real review time on the first steps before cutting.
3. **Carriers C1–C3: in or out?** Building them unblocks 21 articles. That is an assembler plus contract change (lane A, no Creator change), and it may be its own small phase ahead of the blocked tranche. *Discovery reads the carriers section of `260923_R_AgenticMaterialGeneration.md` (Pass 11, O5) before offering the choice.*
4. **The gut-check the list is waiting on.** N1–N8 and S1–S6 (partly superseded by C5 and resolved rulings E1, E2, E5). Discovery compiles what is still open into one lead pass, rather than asking row by row.
5. **The layer library as a deliverable:** generate procedurally (L2) or convert ambientCG's imperfection sets (research Pass 9)? This is decided per layer by the skill today. Confirm that no policy is needed.
6. **The risk lane.** The hypothesis is `build`: content and generators, with no authorization, secrets or public edge. The push is irreversible, and the lead gates it.

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
