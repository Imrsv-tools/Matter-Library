# Phase04 — Wear Layers at Their Own Scale

**Status:** SEED (phase doc written 2026-09-25; discovery has not opened). Numbered by the lead, 2026-09-25, verbatim: *"i and then seed phase 5 and that will be building materials"*. That is, option (i): this entry is Phase04 and Library Coverage is Phase05. It carries out the Phase03 step 3.4 agreement that "the layer-scale fix goes on the Roadmap before *Library Coverage*".

## Outcome

**A wear layer (dust, scratches, scuffs) looks the right size on every material, whatever that material's tile size.**

*(Verbatim from the Roadmap entry.)* Concretely, at close:
- `Scuffs01` (authored at 0.1 m) reads at 0.1 m on the 1 m oak, not stretched 8x;
- `Dust01` (0.01 m) reads as fine dust on the 1 m concrete, not stretched 100x;
- the shipped wear layers tile without a seam;
- the producer side of the contract says how a layer's scale is honoured, so every consumer can match it.

## Why this is a phase

It is one visible result a person can check in USDLiveView, and it is a **contract change**: the assembler's graph, the spec, and every consumer master. **It goes before Library Coverage because Coverage multiplies it.** Coverage builds 17 new layers and about 162 articles that carry up to three of them each. Building those on the current contract means building them wrong, then re-assembling and re-reviewing all of them.

## What is on disk (measured 2026-09-25; re-verify at Pass 1)

- **Every layer samples through the article's placement.** `tools/converters/assemble_mtlx.py` builds one `texcoord` → `place2d "uv_place"` (driven by the Creator ports `uv_scale` / `uv_offset` / `uv_rotation`), and every image uses it, including `overlay{1,2,3}_tex` and `maskset_tex`. A layer's own scale tag (`Dust01_overlay_s001.png`, `Scuffs01_overlay_s01.png`) is carried in its filename and never reaches the graph.
- **The shipped layers:** overlays `Dust01` (s001), `Scratches01` (s001), `Fingerprints01`, `Scuffs01`, `EdgeWear01` (s01); masks `Grime01`, `RustBloom01`, `Verdigris01`, `Crevice01` (s01).
- **Tiling defect (Phase03 close, deferred here):** the shipped `Dust01` does not tile (wrap edge 66 vs 4), and probably neither do the other pre-Phase03 layers. The Phase03 layers are generated with `tileable.py`, and `Fingerprints01` / `Scuffs01` were re-measured seamless at close.
- **The contract:** the overlay/maskset model (`MasterSet.md`), the render-role texture nodes (`LCDSchema.md`), and `place2d` semantics for the UV ports (`LCDSchema.md`: `uv_scale` divides the coordinate).

## Scope

**In:**
- Each overlay honours its own real-world scale relative to the article's, with the Creator's UV placement still moving the whole material together.
- The spec change (`MasterSet.md` §Overlay/MaskSet model, `LCDSchema.md`) and the assembler change, re-assembling the articles that carry layers.
- Regenerating or fixing the shipped layers that don't tile (the Phase03 deferral).
- A gate that catches both defects, so they cannot come back silently.
- The consumer asks, recorded in `docs/Planning/PlatformDependencies.md` (the UE masters sample layers with the article's UV today).

**Not now:**
- Making the other 17 layers in the Coverage list: **Phase05 Library Coverage**, which consumes this phase's contract and generators.
- Localised colour or gloss through a mask (Coverage research L7).
- The shader-cost measurement of always-carried layers (`MasterSet.md` Reevaluate). Note it if this phase adds sampling cost, but don't run it here.
- Consumer-side implementation (Stage, UE masters): the platform's work.

## Seed-vs-docs questions (for discovery; the four fork tests were run as each was written)

1. **Where a layer's scale lives, and how the ratio is carried.** Is it the layer's filename scale tag, a recorded metres-per-tile (the ambientCG importer already records `meters_per_tile`), or both? Is the article-to-layer ratio baked into the nodegraph at assembly (a second `place2d` per layer) or exposed as data? *Discovery work: the spec has no ruling. Read the assembler and the importer first.*
2. **Do masks scale like overlays?** An overlay is a tiling surface effect. A mask says *where* wear goes, which may belong to the article's surface rather than to a physical size. *Read `MasterSet.md`'s channel contract and the shipped mask recipes before offering a choice.*
3. **Articles tagged `sUKN`,** and param-only (L1) articles with no base texture: what does "the article's tile size" mean for them?
4. **Re-assembled articles keep their `v01` in place.** *Answered (test 1)* by the lead's 2026-09-25 rulings: "no versioning ... we are VERY pre release" (`260925_R_DraftsInUSDLiveView.md` Pass 5) and "Fix forward only... we have no legacy projects yet" (Matter-Library#1). This is recorded so it isn't asked again. The frozen `matterlib-0.1.0` pilot is re-frozen, as in the #1 precedent, if its payload changes.
5. **The first human test:** serve the tree to Stage (`tools/releases/serve_to_stage.py`) → open the oak and the concrete in USDLiveView → dial each layer up. *USDLiveView had no LCD sliders at Phase03 3.4; the 2026-09-25 drafts research says it has them now. Confirm at Pass 1.*
6. **The risk lane.** The hypothesis is `build`: a producer graph and spec change, with no authorization, secrets or public edge. Discovery verifies it against the tree.

## Sources (pointers, not copies)

- `docs/Planning/Phases/Complete/Phase03_AgenticMaterialGeneration.md`: §Execution Log row 3.4 (the finding), and the Resume deferral ledger (`Dust01` tiling; layer scale ignored).
- `docs/specs/Ontology/MasterSet.md` §Overlay/MaskSet model · `docs/specs/Contract/LCDSchema.md` · `docs/NamingConventions.md` (scale tags).
- `tools/converters/{assemble_mtlx,gen_shared_textures,tileable,import_ambientcg}.py` · the Phase03 layer generators.

## Discovery Log

_(numbered passes accrue here)_

## Discovery Status

- **Passes captured:** — (seed only)

## Execution Log

_(populated during execution)_
