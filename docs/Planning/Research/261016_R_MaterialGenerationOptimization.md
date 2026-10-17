# Proposal: Optimize wishlist material generation

Created: 2026-10-16  
Status: Proposal for discussion; no implementation or phase commitment.  
Scope: The standing material-making process, not a new material contract.

## Objective

Reduce elapsed time and agent effort per material the maintainer keeps, while preserving physical credibility, provenance, useful wear controls and final review in Storm, Blender and Unreal.

The recommendation is to start with preflight checks and a resumable batch runner. Measure the results before investing in render caching or a broad procedural generator framework.

## Existing workflow and evidence

The working queue is `library/wishlist.yaml`. `.claude/skills/matter-batch/SKILL.md` defines the batch loop and delegates authoring to `.claude/skills/matter-generate/SKILL.md` and its `reference.md`.

The current process already provides:

- `wishlist.py next`, `show` and `brief` for selecting and understanding rows. `brief` reports disk contents, missing layers, a nearby recipe and Physically Based matches.
- Recipe-based authoring, followed by MaterialX assembly; MaterialX is derived, never the editing surface.
- Defaults-only rig runs while fixing a material, followed by a final slider sweep. The skill caps the loop at three rig runs per row and requires a sweep before marking built or stuck.
- Local draft commits per row, a batch summary, and maintainer keep/redo review.
- Sequential writes and commits per row because the wishlist and credits are shared files; one rig at a time because it shares a GPU.

Read-only queue inspection on 2026-10-16 reported 209 rows: 172 queued, 19 redo and 18 kept. These are a snapshot, not a durable baseline. The next five were LED_WarmWhite, Rust_OnSteel, Granite_Polished, Slate_Cleft and Onyx_Polished. Their notes illustrate different jobs: colour-only re-review, visual repair, and physical-scale repair.

When this proposal was written, the authoring skills and wishlist tools had uncommitted changes. They were committed the same day (`99a7e11` skills, `brief` and `rules`; `f7f98b4` parity rig), so the versions described here are the committed ones.

No timings were collected. Sourcing, texture creation, rendering and revision are possible bottlenecks, not measured conclusions.

## Proposed improvements

### 1. Preflight before expensive work — first priority

Extend or compose the existing `brief` and validators rather than creating a second source of material rules. Produce a compact, actionable report for each selected row:

- Classify the work: new build, visual repair, scale repair, or review only. A redo note takes precedence over a row's original kind.
- Check existing identities and flag possible colour-only duplicates for judgement. Do not automatically delete, retire or merge articles.
- Verify scale-tag consistency, source size, available textures, required shared layers and recipe validity where a recipe exists.
- Identify unavailable sources and missing prerequisites before launching renders. Source lookups may need network access; distinguish unavailable from not yet checked.
- Carry the maintainer's redo note into the execution brief and eventual review summary.

Preflight is advisory where semantic judgement is required. It should not mistake an existing recipe for proof that the desired repair is complete.

### 2. Resumable batch runner — first priority

Automate deterministic orchestration: preflight → assemble → validate → defaults render → agent critique/fix checkpoint → final sweep → verdict collection → summary preparation.

The runner should resume after interruption without repeating completed work whose inputs remain valid. It should expose what succeeded, what failed and the next action. Agent judgement remains necessary for source selection, appearance and deciding which fixes to make; maintainer judgement remains necessary for keep/redo.

Use existing tools rather than duplicating their implementation. Persist execution progress separately from wishlist lifecycle states, whose meanings must remain intact. Record the relevant inputs and tool versions so a stale result cannot silently satisfy a checkpoint.

Keep the current one-row-through-commit discipline. Automating commits is a separate design choice; the first slice can prepare explicit file lists and leave the existing agent-driven commit step in place. Never push or change release records as part of this runner.

### 3. Group compatible work — after preflight

Preserve redo priority and explicit user selection. Within an agreed selection policy, group compatible jobs such as scale repairs, scanned materials, procedural materials and review-only rows. This can reuse source research, generator knowledge and diagnostic setup.

Do not silently replace the current stable wishlist ordering. Begin by suggesting a batch composition; make any automatic reordering an explicit, documented policy. Read-only planning may overlap rendering, but writes for the next row still wait until the current row is committed.

### 4. Progressive rendering and caching — measure first

The skill already avoids sweeping every fix. Retain that improvement and assess whether a cheaper preview catches enough errors to justify another stage.

Cache only results whose full inputs match: recipe or assembled material, all referenced textures, renderer/runtime, render settings, scene, camera and relevant rig code. Invalidate conservatively. A cached image must never be presented as evidence for changed inputs.

A cheap preview helps reject obvious colour, relief or scale mistakes; the final three-tool sweep remains required. Decide whether a preview counts toward the three-run budget before adding it. Also clarify how the runner reserves a final sweep when defaults fixes consume the budget; do not invent a new limit implicitly.

### 5. Reusable procedural generators — targeted investment

Identify families with repeated demand and no suitable scans, then parameterize a proven generator: physical size, grain or feature size, colour variation, roughness, relief and seed. Candidate families include clay, concrete and stone; which to implement should follow actual queue demand.

Each output still needs its own identity, recipe, provenance and visual judgement. Shared machinery must not flatten different substances into cosmetic variants. Verify tiling and generate at the intended physical size from the start.

### 6. Material-appropriate diagnostic views

Keep comparable rig views, but add targeted views where existing views conceal a fault: a plane for grain and repeating texture, grazing light for relief, suitable thickness for glass, or a character/close camera for fabric and body-worn materials.

First inspect the rig's current coverage. Add a view only for a demonstrated diagnostic gap; extra views also cost render and review time. Record which view supports a judgement.

## Constraints that remain binding

- MaterialX remains the single source consumed downstream; author edits happen through recipes and source textures.
- `meters_per_tile` must equal the scale tag's exact size. A scan at another size is remade at an allowed size or not used; changing metadata to stretch it is prohibited (`docs/specs/Ontology/Identity.md`, Phase19 scale rule).
- Report renderer limitations; never distort a material to force visual agreement.
- Preserve provenance, public-facing material words, relevant wear layers and final slider checks.
- Generated work remains draft until the existing review process records its disposition. Keep/redo and release approval are distinct acts.
- Respect shared-tree ownership, sequential row mutations and the single-GPU rig constraint.

## Suggested first implementation slice

Choose a small representative set of rows covering a scale repair, a new build and a review-only job. Capture a baseline while working them through the existing process. Add a preflight report and minimal execution journal using the existing tools, then demonstrate interruption and resume on a comparable run.

The useful result is a real row progressing through the existing authoring and review path with less repeated mechanical work. It is not a generic orchestration framework or a new wishlist state model.

Success evidence:

- Invalid scale or missing prerequisites are surfaced before an expensive render.
- Resume skips valid completed work and reruns work after a relevant input changes.
- The final summary links current evidence and preserves unresolved limitations.
- Explicit file ownership and per-row commits remain reviewable.
- Final review quality is preserved while elapsed time or agent effort falls.

Use focused checks for input invalidation and resume behavior, plus a real material run. Set numeric performance targets after the baseline rather than inventing them now.

## Measurement

Record per row: work category, sourcing time, authoring time, render time, agent intervention time where practical, rig-run count, repeated work after interruption, and final keep/redo outcome. Separate active work from waiting and separate new builds from repairs and re-reviews.

Use time per kept material as the eventual outcome measure, with time per review-ready draft as an earlier signal. Include failed and stuck attempts so throughput cannot look better merely by dropping difficult rows. Small samples are directional evidence, not proof of a general speedup.

## Questions for the reviewing agent

1. Which existing tool should own preflight, and what does `brief` already cover well enough to reuse unchanged?
2. What execution journal is sufficient for reliable resume without duplicating wishlist state or creating another planning surface?
3. Which measured stage is the largest avoidable cost, and should the first slice change if rendering is not dominant?
4. How should the three-rig-run limit reserve the required final sweep, and would an optional cheap preview count?
5. Does the existing rig already cover the proposed diagnostic views? Which concrete failures justify an addition?
6. Can conservative caching deliver enough benefit to justify its invalidation complexity?
7. Should grouped selection remain an agent recommendation or become an explicit queue option?

## Handoff status

This document is the only artifact created for this request. No material, wishlist state, skill, generator or release record was changed, and no implementation was started. The proposal is ready for discussion with another agent; its recommendations are not approved architecture or an assigned phase.

## Review (2026-10-16)

Reviewed against the committed tools and one measured row, `Titanium_Raw_Clean_Base_s01_v01` (batch 261016-1). Answers to the questions above:

1. **Preflight owner.** `wishlist.py brief` already covers about half: what is on disk for the stem, which of the row's layers exist, the nearest recipe for its master, Physically Based matches and the redo note. It does not classify the work (new build, visual repair, scale repair, review only), check scale against the source, flag possible colour-only duplicates, or run `validate_recipe.py` on an existing recipe. Added the same day as further `brief` lines, not a second tool: `job` (new build, scale repair when the recipe is off its tag, a redo that follows its note, review only), `gate` (`validate_recipe.check_recipe` on the row's recipe), `scale` (the tag's length, a row tag that disagrees with the name, an off-tag recipe) and `same` (the other articles of the Material token, for judging a colour-only variant). The source's own size is still checked at import (`import_ambientcg.py`), not in `brief`.
2. **Execution journal.** Open.
3. **Largest cost.** Rendering may not dominate. A full `--sweep` of the titanium row took 44 s wall time with the three renderers running at once (Storm 23 s, Blender 38 s, Unreal 44 s; 38 pictures each). The batch skill still says a sweep takes 4–10 minutes. Titanium is param-only, so re-measure on a textured row before choosing the first slice; sourcing and fix iterations may cost more than rendering.
4. **Final sweep within the run limit.** Answered in `99a7e11`: fix runs render the defaults only, and the third run is always the sweep, so a row can always be marked built or stuck. Whether a cheaper preview tier would count toward the limit stays open; no such tier exists.
5. **Diagnostic views.** Partly covered. Every job renders a wide view and a close-up; Emissive adds the set at -4 stops; Character jobs add face, mouth and swatch views (`tools/parity/job.py`, `views_for` and `CHARACTER_VIEWS`). There is no grazing-light view and no plane-only view for repetition; add one only for a demonstrated failure.
6. **Caching.** At under a minute per sweep for a param-only row, not justified yet; revisit once textured rows are measured.
7. **Grouped selection.** Open; a queue policy for the maintainer.

Follow-up from the review: re-measure a sweep on a textured row and correct the 4–10 minute figure in `.claude/skills/matter-batch/SKILL.md`. **Done (2026-10-17):** batch 261016-2's sweeps, three renderers at once, took 41–49 s on the textured rows (Slate_Cleft, Granite_Polished, Rust_OnSteel) and 76–77 s on LED_WarmWhite, whose Blender and Unreal columns render an extra dim view. The skill now says about 45 s to 1.5 min. Rendering is not the largest cost of a row.
