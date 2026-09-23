# Folder Structure for a Project Repo

Purpose: standardize how a project repo is prepared for AI-assisted planning and implementation. This is the **blueprint you bootstrap a new project from** — pair it with `templates/`, which ships the starter files this doc describes.

Applies to any project that owns its full planning surface (roadmap, phases, research, support, conventions, commands) inside its own repo. **That is the default and recommended shape: one repo, one branch, one set of docs.**

## Where the planning surface lives

Planning is durable, human-discoverable project truth, so it lives in a top-level **`docs/`** home — at **`docs/Planning/`** — alongside the repo's product specs, **not** hidden in the agent-operational `.ai/`.

So: **planning is never a thinner, flat `plan/ + research/ + phases/` skeleton — it is the full `Planning/` tree.** If you find yourself making three loose sibling folders, that's the wrong shape. The unifying rule (`AgenticEngineering_DocumentationMap.md`): `.ai/` owns agent operation and never the work itself; planning truth lives in the durable `docs/Planning/` home.

### Command path-resolution

Every `docs/Planning/…` path in `commands/` **resolves literally**. There is no remapping step and no SHA cascade — one repo, one commit.

⚠ **IF THIS PROJECT EVER SPANS SEVERAL REPOSITORIES**, that is where the shape genuinely changes: the shared planning surface moves to one documentation repo consumed by the code repos, each code repo's `.ai/` stays a thin entrypoint, and commits acquire a cross-repo ordering the one-repo shape does not have. **The planning TREE is unchanged** — same subfolder names, only the parent home differs. **Write the mapping down in `LOCAL_DELTAS.md` when you get there, against the shape you actually have. Do not pre-build it.**

## Why This Structure Exists
- Keep agent onboarding fast and consistent.
- Separate stable project context from phase-by-phase execution.
- Use pointer docs so every agent reads the same core files first.
- Reduce duplicated or conflicting planning sources.

## Standard Layout

```text
<ProjectRoot>/
├── AGENTS.md
├── .claude/
│   └── CLAUDE.md                            # thin Claude pointers (+ .claude/commands/*.md → .ai/commands/*.md)
├── .ai/                                     # Working tier — agent-operational truth (thin)
│   ├── AI_Orientation.md                     # identity, repo map, the platform→standalone path mapping, build/test
│   ├── AI_WorkingAgreement.md
│   ├── README.md                             # the accepted-folder registry (mirror platform .ai/README.md)
│   ├── CodingStandards.md                    # OPTIONAL — framework/ABI deltas only; points up to platform CodingStandards.md
│   └── commands/                             # the VERBS you invoke — mirror the platform .ai/commands/ set
│       ├── howdy.md · research.md · discovery.md · plan.md · execute.md
│       ├── quick-fix.md · peer-review.md · retro.md · issue-create.md
│       └── workflow-refiner.md               # (+ whichever the project actually runs)
└── docs/                                    # Durable home — planning + product specs (the standalone difference)
    └── Planning/                            # the FULL Planning tree
        ├── Roadmap.md                        #   phase registry — ## Active / ## Future / ## Complete
        ├── Phases/                           #   phase docs
        │   ├── Future/                        #     unnumbered PhaseTBD_* docs
        │   └── Complete/                      #     closed
        ├── Research/                          #   investigations + decision records (YYMMDD_R_*.md)
        └── Support/                           #   diagnostics + the feedback inbox
            ├── Troubleshooting/
            └── WorkflowFeedback/              #     /retro inbox (the workflow-refiner drains it)
```

> **Planning and product specs both live in `docs/` — neither lives in `.ai/`.** `docs/Planning/` holds *how the work is run* (roadmap, phases, research, support); the standalone's durable **product** specs, charter, and architecture live alongside it in `docs/` (organise as suits the project — e.g. a `docs/specs/` subtree). `.ai/` helps agents work; it does not own the record.

This template prescribes the **current** doc names (`AI_Orientation`, `AI_WorkingAgreement`, `Roadmap.md`) for any standalone created going forward. A project adopted before these names settled keeps its old filenames until explicitly migrated.

The three tiers in brief: `.ai/` is the **Working tier** (orientation, agreement, commands); a standalone's **Durable tier** lives in `docs/` — the `docs/Planning/` surface plus durable methodology/standards material (Glossary · NamingConventions · CodingStandards); and a **Private memory tier** holds per-agent notes — never a home for team rules. Full model → `AgenticEngineering_DocumentationMap.md`.

## How It Works

1. `AGENTS.md` is the root entry point.
2. `.claude/CLAUDE.md` mirrors root pointers for Claude workflows.
3. `.ai/AI_Orientation.md` defines project purpose, boundaries, active phase, and the platform→standalone path mapping.
4. `.ai/AI_WorkingAgreement.md` defines non-negotiable rules and naming constraints.
5. `docs/Planning/Roadmap.md` is the phase registry (the `## Active` / `## Future` / `## Complete` sections).
6. `docs/Planning/Phases/{Future,Complete}/PhaseXX_*.md` hold scoped implementation plans.
7. `docs/Planning/Research/*.md` capture investigations and decisions; `docs/Planning/Support/` holds troubleshooting + the `/retro` feedback inbox.
8. `.ai/commands/*.md` define the verbs agents invoke — `howdy` (onboarding) plus the workflow set (`research, discovery, plan, execute, quick-fix, peer-review, retro, issue-create`), mirroring the platform `.ai/commands/` set.

## Operating Model (what runs inside these folders)

This doc fixes the **folder skeleton**; the **process that runs in it** is the same Agentic-Engineering machinery the platform uses — a standalone adopts it wholesale, not a thinner variant. Don't re-derive it here; conform to:

- **The Workflow Cycle** — `AgenticEngineering_Workflow.md`: the five-stage spine (Brief → Build → Try → Strengthen → Close), with `/discovery` → `/execute` as the ordinary path and `/plan` as the high-rigor lane, **unit triage on two axes — DEPTH first, then ANCHOR**, the separate **work-vs-ship** axes (units vs Build/Version), the **Quick Fix** and **Issue** lanes for sub-phase work, the **rollback-snapshot** tenet, phase numbering, and commit cadence.
- **The retro → Workflow-Refiner loop** — executors deposit `/retro` feedback into `docs/Planning/Support/WorkflowFeedback/`; the refiner verifies, triages, and folds the good parts back into these docs.
- **Doc ownership + tiers** — `AgenticEngineering_DocumentationMap.md` (the unifying rule: `.ai/` owns agent operation; durable product specs live in their own home).
- **The core concepts a new repo otherwise re-derives by being corrected** — `AgenticEngineering_Workflow.md` §What counts as ONE phase · §Roadmap status vocabulary · §Where decisions live. These were tacit platform practice for a long time (used in Roadmap entries, never defined), so **every new standalone paid to rediscover them.** They are written down now; carry them, don't re-derive them.

## Pointer-First Policy

`AGENTS.md` should point to:
- `.ai/AI_Orientation.md`
- `.ai/AI_WorkingAgreement.md`
- `docs/Planning/Roadmap.md`
- `.ai/commands/howdy.md`

`CLAUDE.md` should mirror the same pointers for tool compatibility.

## Document Roles

**Document roles** (which doc owns what, the three tiers, the two prefix genres, navigation/hop rules) → `AgenticEngineering_DocumentationMap.md`.

Avoid redundant planning files (for example a second roadmap doc) unless there is explicit reason.

## Setup Checklist

1. Create the folder tree — including the full `docs/Planning/{Roadmap.md, Phases/{Future,Complete}, Research, Support/{Troubleshooting,WorkflowFeedback}}` (mirror the reference layout in `docs/Planning/` exactly; do **not** make a flat `plan/ + research/ + phases/`).
2. Add `AGENTS.md` and `.claude/CLAUDE.md` with matching pointers.
3. Create starter `AI_Orientation.md` (include the platform→standalone path mapping) and `AI_WorkingAgreement.md` — the agreement **must carry §Documentation Shapes Architecture (Conway's Variant)** and the working-with-the-lead notes (proposals default to a **list**; if a deliverable is not at the path the lead would open, say so in the *first* line, not the last).
   - **`README.md` describes what the project IS** — concept, components, invariants. **Progress and status never go there**; the Planning tree owns those. A README doing status duty is the most common drift in a young repo.
3b. **Create `docs/Glossary.md` on day one, not "when it settles".** The moment a second doc reuses a term, that term is load-bearing (Conway's Variant), and a project that defers the glossary re-argues its own vocabulary instead. Shape: term + **one-line** definition + pointer, never the spec.
4. Optionally add a project-level `CodingStandards.md` / `CODING_STANDARD.md` with framework/ABI deltas only (points up to platform `CodingStandards.md`).
5. Create `docs/Planning/Roadmap.md` — **with the status legend in its header** (`RESEARCH → SEEDED → ACTIVE → COMPLETE`, plus `TBD`; see Workflow §Roadmap status vocabulary) — and an initial phase doc under `docs/Planning/Phases/Future/`. The platform used these statuses for a year without ever defining them, and every reader re-derived them.
5b. **Set the harness config, not just the docs** — a process rule cannot change harness behaviour. In `.claude/settings.json`: `"worktree": {"bgIsolation": "none"}`. **One repo, one branch, one set of docs**; worktrees drop shadow copies of every doc inside the repo (poisoning every grep) and silently orphan commits. If a background session's writes are being refused, this key is why — not the Working Agreement.
6. Add `.ai/README.md` (the accepted-folder registry) and the `commands/` set — `howdy` plus whichever workflow verbs the project runs (mirror the platform `.ai/commands/`). Mirror each as a thin `.claude/commands/<name>.md` pointer.
7. Decide the durable **product** spec home (e.g. `docs/`, `specs/`) — kept out of `.ai/`; a standalone that owns product specs splits `docs/` (durable spec tier) from `docs/Planning/Research/` (investigations) deliberately, not ad hoc.
8. **Licensing decision** (public/open standalones): LICENSE + CONTRIBUTING land at bootstrap, not later — verify any inherited engine/data licenses while choosing.
9. **Porting onto a PRE-EXISTING scaffold: absorb, don't duplicate** — reconcile what's there into the `.ai/` shape above and retire the superseded originals, rather than laying a second structure beside them. Three kinds arrive, and only the first is obvious:
   - **Entry points** (another tool's `AGENTS.md`, docs, context dumps) → fold into the read order.
   - **A decision registry — usually `docs/adr/`, and the single most common thing a pre-adoption repo already has.** ⛔ **Retire it and redistribute; do not keep it.** Workflow §Where decisions live is explicit that there is no single decision registry and that looking for one is the classic error. Decisions the lead actually took move to the owning record (a research thread's `## Resolved`, the phase doc); **anything the registry merely *asserted* was never a decision — demote it to an open question.** A pre-adoption ADR set routinely documents choices nobody made.
   - **A pre-existing plan or roadmap** → **audit it against Workflow §What counts as ONE phase BEFORE carrying anything into `Roadmap.md`.** Pre-adoption plans are almost always time-shaped (delivery windows, quarters, sprints) or theme-shaped (a bundle of related things) — both of which §What counts as ONE phase rejects outright. Checklist item 9's "entry point" test will not catch this: a delivery-estimate-led plan is a *plan*, not an entry point, and it reads perfectly reasonable right up until it is seeded as phases.
10. **Run a first adaptation pass on the inherited command docs** — the carried `.ai/commands/*` may still assume shapes this project does not have. Note each in `LOCAL_DELTAS.md`, add a heritage note ("read for method; tune via `/retro` → `/workflow-refiner`"), and run this as the new repo's inaugural `/workflow-refiner` session.
11. **Memory namespace:** a new standalone gets its own session-memory namespace — durable facts belong in the repo's `.ai/` docs, not the originating repo's memory (which keeps only a "this sibling exists" breadcrumb); its OWN `docs/Planning/Support/WorkflowFeedback/` inbox takes project-internal retros, while frictions about the *portable methodology itself* file to the platform inbox.

## Recommended Naming

- Match doc project names to canonical repo names.
- Use deterministic phase prefixes (`Phase01_`, `Phase02_`) only for phases **the lead has numbered** — everything else stays `PhaseTBD_<Name>` however settled its position (Workflow §Phase Numbering).
- Use concise, functional filenames.

## Operational Session Flow

1. Run `/howdy`, then read `AI_Orientation.md`, `AI_WorkingAgreement.md`, and `docs/Planning/Roadmap.md`.
2. Open active phase doc from `AI_Orientation.md` / `docs/Planning/Roadmap.md`. **A phase doc lives in `Phases/Future/` while UNNUMBERED (`PhaseTBD_*`), moves up to `Phases/` when the lead numbers it, and into `Phases/Complete/` when it closes** — the folder tracks commitment, not status (Workflow §Where a phase doc lives).
3. Execute only active-phase work, following the Workflow Cycle (Discovery → Plan → Execute) at the size the work warrants (Quick Fix / phase / Issue).
4. Update phase doc and `docs/Planning/Roadmap.md` as decisions land.
5. Add research notes only when they carry evidence or unresolved decisions; deposit a `/retro` into `docs/Planning/Support/WorkflowFeedback/` at handback.
