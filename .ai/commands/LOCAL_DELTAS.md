# Local Deltas — read this once, then read the other commands *for method*

The other files in `.ai/commands/` were **carried from [`PeteSmalls/agentic-engineering`](https://github.com/PeteSmalls/agentic-engineering)** on `2026-09-23` (upstream `9f52c7f`). They encode a mature Agentic-Engineering workflow, which is exactly why they're here. But upstream cannot know your stack, your repo shape or your tracker. Read them for the *method*, and translate the assumptions listed below as you go.

**This file is the override seam.** Upstream ships the method; this file records where *this* project diverges. Keep it short: a long deltas file means the divergence belongs upstream.

**⛔ A ROW DESCRIBING A NOT-YET-EXISTING ARTIFACT MUST BE UPDATED WHEN IT COMES TO EXIST — and until then, do not read one as a statement of current state.** A parenthetical like *"(create on the first real lesson)"* is a standing **instruction**; it ages into a false **fact** the moment the thing exists, and it reads as *"it isn't there"* to every subsequent agent. **This file is dated, not live — verify any row that asserts tree state before repeating it.** *(An executor asserted "the learnings folder does not exist yet" in a phase doc, a commit message and a lead-facing handback, straight from such a row. The folder had held two files for a day. Nobody ran `ls`; the close's doc-conform gate caught it by luck.)*

## The translation table

*Rows written 2026-09-23 at adoption (Phase01 step 1.1). State claims carry their measurement date.*

| The command says… | In the Matter Library it means… |
|---|---|
| `docs/Planning/…` | Resolves literally. |
| `--repo <owner>/<repo>` in `issue-create` | `Imrsv-tools/Matter-Library` (public; Issues enabled, checked 2026-09-23). **Pre-existing Matter issues filed in the IMRSV platform's tracker stay there** (lead, 2026-09-23): they may reach into the platform's plugin or Studio. New Matter-Library-only work files here. |
| the glossary | `docs/Glossary.md`. It ships seeded with the method vocabulary; the Matter terms land in Phase01 step 1.2. |
| the durable learnings home | `docs/Learnings/<Domain>/`. **It ships empty, which is correct.** No domain exists yet (2026-09-23). |
| `docs/architecture/` | **`docs/specs/`** — this project's product contract, keeping the subfolder names it had in the IMRSV platform docs (`Ontology/`, `Contract/`, `Catalog/`, `Authoring/`, `Distribution/`, `Tooling/`, `Experience/`) so that consumer pointers rewrite mechanically. The entry is `docs/specs/_Architecture.md`. Lead ruling, 2026-09-23. |
| `CodingStandards.md` · `ToolingConventions.md` · `NamingConventions.md` | `NamingConventions.md` is **active** (the filename grammar, scale tags and release ids were live before adoption). `ToolingConventions.md` is filled in Phase01 step 1.5 from the retired `FolderStructure.txt` and the `tools/` taxonomy. `CodingStandards.md` **stays a stub** until a phase first rules on how code is written. |
| discovery Pass 1, "the platform-docs review" | **This project's own product docs: `docs/specs/` (from `_Architecture.md` down) and `docs/Glossary.md`.** The IMRSV platform docs apply only where a phase touches a consumer boundary (how Stage, the UE plugin or Studio read a release). Those docs are private; name the consumer-side fact you need, and never copy private detail into this repo. |
| this project's centrally-allocated namespaces | **Library release ids** `matterlib-X.Y.Z` (semver; assigned by the maintainer at promotion) · **material/texture versions** `vNN` (per asset; the next free integer for that asset at authoring) · **scale tags** `s0001…s100`, `sUKN` (a closed set, in `NamingConventions.md`) · **catalog `schema_version`** (an integer, bumped only by a contract phase). No gate-id series exists (2026-09-23). |
| the way this project is RUN | **There is no running service.** "Run" means the **structural gate** `python tools/validators/run_all.py` (16 lanes) plus the Blender side (Blender 5.1+ running the add-on in `blender/addons/imrsv_lcd_export/` and the Asset-Browser library in `blender/asset_library/`). **Measured 2026-09-23: `run_all.py` fails at import (no MaterialX Python module on the lead's box)**; the one-command-check phase owns fixing that. |
| "the artifact a person reaches" (`execute_test`: the thing that RUNS is not the source) | For this project: **a release bundle** (`library/releases/` + the staged tree), **the installed Blender add-on and Asset-Browser library** (installed into Blender, not the repo copy), or **a usdview preview** of a `.mtlx`. A green `run_all.py` is evidence about the source tree, not that an installed add-on carries your edit. |
| a publishing producer, if there is one | **The release lifecycle.** Its trigger is the maintainer running `tools/releases/{stage,freeze,promote,activate}_release.py`; the lock is the frozen, hash-locked records in `library/releases/` (editing one invalidates its freeze and approval); the marker is `active-release.json`, the selector `activate_release.py` writes into a consumer's install root. There is no watcher and no automatic publish (2026-09-23). |

## Separation — this repo and the IMRSV platform

**This repo is a standalone producer** (lead ruling R1, 2026-09-23; `docs/Planning/Research/260923_R_StandaloneSetup.md`).

- **Consumers take published releases, never the checkout.** IMRSV (Stage runtime, UE plugin, Studio), Blender and USDLiveView are consumers.
- **No SHA cascade.** Any carried instruction to "bump the submodule SHA at close" is a **no-op here**. The IMRSV platform still registers this repo as a submodule during the transition; retiring that is the platform's work, listed in `docs/Planning/PlatformDependencies.md`.
- **Integration phases are numbered on the platform's line** (`Methodology/AgenticEngineering_Workflow.md` §Phase Numbering). This repo keeps its own line, starting at Phase01 (lead, 2026-09-23).
- **Work this repo needs a consumer to do** goes in `docs/Planning/PlatformDependencies.md`, not in handback prose.

## Retired local verb — `housekeeping`

The pre-adoption `.ai/commands/housekeeping.md` (retired 2026-09-23) has no upstream twin. Its checks still apply at phase close and after doc/plan updates, expressed against the new shape:

1. The Roadmap names the correct active phase, or "no active phase" between phases.
2. `Readme.md`, `docs/specs/` and the on-disk content agree on the taxonomy and filename grammar. Drift is **tagged** (`(planned)`, `Todo`, `Drift`, `Reevaluate` with a date), never silently deleted.
3. Every `.mtlx` validates against the filename grammar and metadata schema (`run_all.py` grammar and material lanes).
4. Aspirational design is preserved, and nothing is pruned just to match disk (`AI_WorkingAgreement.md` §Project practices).
5. ~~At close, have the platform bump this submodule's SHA.~~ Retired by R1: this repo is a producer.

## The rule for divergences

When an upstream assumption doesn't fit:

1. **Adapt in the moment** — do the sensible local equivalent (usually: drop the cascade step, remap the path). Then keep going; the adaptation is not the deliverable.
2. **File the friction** via `/retro` into `docs/Planning/Support/WorkflowFeedback/`. **⛔ Do NOT record it in this file yourself** — this file is the Refiner's lane (`.claude/CLAUDE.md` §Lanes), and writing the row yourself skips the only decision that matters: **is this divergence portable or genuinely local?** *(That skip has already cost once: a Wave-filename convention was recorded here by a working run, turned out to be portable, and had to be promoted upstream and the row deleted.)*
3. The **`/workflow-refiner`** session drains that inbox and records the outcome. **Fixes to the *portable* method go upstream and are re-synced; fixes that are genuinely project-specific land here.** That split is what stops the methodology forking, and it only works if one role makes the call.

**The steps below are the Refiner's, not a working verb's:**

4. **When you record a substitution as DONE, rewrite the carried command's `⚙ Configure before first use` banner too** — to *"configured for this project; see `LOCAL_DELTAS`"*. Leaving it standing makes the file call a live, working value "a placeholder", every reader re-checks it, and the contradiction outlives the substitution. *(`issue-create.md` warned "never leave the placeholder unresolved" about the very value three of its own `gh` invocations were already using — and that value was stale.)*

Don't rewrite a whole command doc on first contact — let the retro→refiner loop do it deliberately.

*(This file's rows were written at adoption by the Phase01 bootstrap, which is the method's own adoption step (`ADOPTING.md` §2–§6), not a working verb recording its own fix.)*

## Lead-authored durable planning material — a known verb gap

**No verb owns this.** The method assumes a project past the commitment line, where `/plan` owns durable planning output. Before that, a lead may hand over a finished planning document — a build sequence, a milestone set — that fits nothing: it is not `/research` (it *commits* to things), not `/quick-fix` (it spans tiers), and `/discovery` seeds one phase at a time. Until it recurs often enough to earn a verb, record the local answer here. The shape that worked:

- **It lands in `docs/Planning/`** as a durable planning doc — **not** in `Planning/Research/`, which is for investigations.
- **`Roadmap.md` stays structurally distinct from it.** The Roadmap is the phase *registry* — heading, one-line `Outcome`, doc pointer. All scope and technical content lives in the planning doc it points at.
- **Upstream records are updated FIRST** — the product contract, the research thread's `## Resolved` — and only then the derived doc (`AI_WorkingAgreement.md` §A Derived Document Reflects Decisions, which owns the rule; this is the seam where it gets missed).

## Weighting

**Still building, not a production system** (lead, 2026-09-23). Bias to the smallest unit that fits. The full `/execute` ceremony is available and worth it for a real build: a contract change, a release, a consumer-facing format. But a lot of work here is a `/quick-fix` (a doc correction, a single material) or a `/research`. **The one lane-raising fact to keep in mind:** the repo is public, so publication (a push) is irreversible and lead-gated.
