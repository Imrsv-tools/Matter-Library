# Agentic Engineering — Documentation Map

> Genre: **portable methodology** (`AgenticEngineering_*`, lives under `Methodology/`) — the map of *which doc owns what*. This is the one place that answers "where does this rule/fact live?" so the doc system stays legible and drift-free. Consolidates what used to be scattered across `conventions §Documentation Navigation Policy`, `context §Documentation Pointers`, `*ProjectFolders §Document Roles`, and `AGENTS.md §Operating Model`.

**The load-bearing rule this whole map turns on:**

> `.ai/` owns **agent operation**. `docs/Planning/` owns **durable planning truth**.

`.ai/` is the **thin agent-operational entrypoint** — orientation, working agreement, commands. It *helps agents work; it does not own the work.* Roadmap, phase docs, research, the deferred backlog, execution support, and durable learnings are team-visible project truth and live in the Durable tier (`Planning/`, `Learnings/`), not under `.ai/`.

A new agent or dev should be able to answer all of these from **this doc alone, in ≤1 hop**:

1. **Where do I start?** → `AGENTS.md` → `.ai/AI_Orientation.md` (or run `/howdy`).
2. **Where does planning live?** → durable `Planning/` (`Roadmap.md`, `Phases/`, `Research/`, `Support/`). *(Deferred work is GitHub issues now — the `DeferredBacklog/` folder was retired.)*
3. **Which doc owns *workflow* (how we run the work)?** → `AgenticEngineering_Workflow.md` (this folder).
4. **Which doc owns *naming*?** → `../NamingConventions.md` (words + grammar).
5. **Which doc owns *coding style*?** → `../CodingStandards.md` (enforced style); project deltas point up to it.
6. **Which doc owns *developer tooling + artifact placement*?** → `../ToolingConventions.md` (the artifact taxonomy — where build/script/test/asset/output artifacts live — plus build/test/deploy/lint/CI entry-point rules).
7. **Where do learnings live?** → durable `docs/Learnings/<Domain>/`, one folder per domain the project has; `.ai/AI_Orientation.md` points at the domain home.
8. **Where does each kind of doc live?** → see §One repo — where each kind of doc lives, below.
9. **What must not be duplicated?** → see §No-Duplication Rule (a rule lives in exactly one home; others link to it).

---

## The three tiers

| Tier | Home | Audience | Holds |
|---|---|---|---|
| **Working** | `.ai/` (truth) + `.claude/` (bindings) | AI + devs, frequently read, howdy-routed | tool-agnostic truth in `.ai/` (`AI_Orientation`, `AI_WorkingAgreement`, `README` registry, `commands/`, opt-in/reserved `agent-skills/`·`reference/`·`agents/`); thin per-tool bindings in `.claude/` (commands·agents·hooks·settings) — **agent-operational only; not a planning archive** |
| **Durable** | `docs/` | team, authoritative | `Planning/` (roadmap · phases · research · backlog · support) + `Learnings/` + `Methodology/` (`AgenticEngineering_*`) + the standards trio (Glossary · NamingConventions · CodingStandards) + `ToolingConventions` + product specs |
| **Private** | memory (`~/.claude/.../memory/`) | Claude, on one machine only | how-the-user-wants-me-to-behave. **Never a home for a team rule** — teammates can't see it |

> **Working `.ai/` no longer holds `build_plan`, phase docs, or learnings** (Phase 33, 2026-06-10). Those moved to the Durable tier: roadmap+phases+research+backlog → `Planning/`, learnings → `Learnings/`. The `AgenticEngineering_*` methodology docs moved from the Durable-tier *root* into `Durable/Methodology/`.

## Two prefix genres (folder = tier; prefix = genre)

The `.ai/` `AI_*` prefix and the `Methodology/` `AgenticEngineering_*` prefix mark two different doc *genres* — they are not redundant:

- **`AI_*` = operational docs of action** — "what to do, now, in *this* project" (`AI_Orientation`, `AI_WorkingAgreement`).
- **`AgenticEngineering_*` = portable methodology blueprint** — "how an Agentic Engineering project is set up and run" (`Workflow`, `ProjectFolders`, `DocumentationMap`), now homed under `Methodology/`. Carry these over when starting a new Agentic Engineering project.

## The disambiguation test (this is what stops future drift)

> **A rule lives where its enforcement mechanism lives.**
> - Linter / compiler can check it → **CodingStandards**
> - It's a vocabulary / name-grammar choice → **NamingConventions**
> - It's a developer tool entry-point / script / runner / CI-wrapper convention → **ToolingConventions**
> - It's an engineering judgment call about how we build → **AI_WorkingAgreement**
> - It's a process / workflow agreement about how we run the work → **AgenticEngineering_Workflow**
> - It's a planning record (roadmap, phase, research, backlog) → **Planning/**
> - It's reusable engineering memory (costly-to-rediscover, specific) → **Learnings/**
> - It's orientation (what is this, where's everything, how do I build) → **AI_Orientation**
> - It's my-behavior-with-the-user → **memory**

The one shared edge — **casing** (snake_case et al.) — is *about naming* but *enforced by lint*: **NamingConventions** owns the words + name-grammar; **CodingStandards** owns casing/formatting enforcement and points to NamingConventions for the words. One-way reference, no copy.

### Detail-altitude (which doc owns a topic ≠ how much detail it carries)

The disambiguation test picks the *owning doc*. This picks the *depth* each doc holds:

> Each doc carries content at **its own altitude** and points down for depth.
> A **Glossary** entry is *the term + a one-line definition + an optional pointer* — never the spec. The moment an entry needs a paragraph, a phase number, a file path, a protocol/version, an algorithm, or a casing rule, that detail is mis-homed: keep the one-liner, move the detail to the owner (**NamingConventions** for name-grammar/casing, a **product spec** for behavior, **Workflow** for process, **git history** for provenance).

This is the upstream-doesn't-restate-downstream rule applied to definitions: the Glossary names words, NamingConventions rules their grammar, specs own behavior.

---

## Doc → owns → references (the lookup)

### Working tier — `.ai/` truth + `.claude/` bindings

`.ai/` holds the **tool-agnostic truth**, authored once; each tool's `.claude/` (and future `.codex/`, `.gemini/`) holds **thin pointers + tool-only mechanics**. The accepted `.ai/` set is registered in `.ai/README.md` (the folder registry); the layout is in `AgenticEngineering_ProjectFolders.md`.

| Doc / folder | Owns canonically | References |
|---|---|---|
| `AI_Orientation.md` | session-start orientation; the live **project/repo map**; build/test entry points; doc pointers (into durable `Planning/` + `Learnings/`) | down into each project; up to Durable docs |
| `AI_WorkingAgreement.md` | **engineering agreements** (Bucket A): the project's hard engineering agreements — ownership boundaries, lifecycle awareness, asset management, No Workarounds, No Mock Data, Build Safety, Don't-Delete-Spec, Documentation-Shapes-Architecture | → `Methodology/AgenticEngineering_Workflow` for process; → this Map for navigation |
| `.ai/README.md` | the **accepted-folder registry** — what may live in `.ai/`, each folder's role, and the "verify a better home first" checklist before adding anything | → this Map; → `ProjectFolders` |
| `.ai/commands/` | **verbs** you invoke — session command behavior (`howdy`, `research`, `discovery`, `plan`, `execute`, `peer-review`, `retro`, `workflow-refiner`, `issue-create`); resolve durable `Planning/` paths; deliberately restate the Workflow rules they execute (see §No-Duplication → operational rendering) | → durable Planning |
| `.ai/reference/` · `.ai/agents/` · `.ai/agent-skills/` | reserved/opt-in: **nouns** the verbs look up (`reference/`, on first real doc), tool-agnostic **roles** (`agents/`, deferred until a 2nd tool needs them), external-skills-framework config (`agent-skills/`, present only where that workflow runs — Stage) | → `.ai/README.md` for the rule |
| `.claude/` (binding) | Claude's **thin pointers + tool-only mechanics**: `commands/*.md` (5-line `/slash` → `.ai/commands/X.md`), `agents/*.md` (subagent specs — frontmatter + role body), `hooks/`, `settings*.json`. Carries **no project facts** — only pointers + Claude-specific config | → `.ai/` for all truth |

### Durable tier (`docs/`)

| Doc / home | Genre | Owns canonically | References |
|---|---|---|---|
| `Planning/Roadmap.md` | planning | the phase registry / sequencing board (active + upcoming + landed). *(Formerly `.ai/plan/build_plan.md`.)* Phase-only — Issues live in GitHub and reach the Roadmap only by bundling into a Phase | → phase docs |
| `Planning/Builds.md` | planning | the **Build ledger** — version ↔ contents, one line per cut Build (ship-axis record) | → `Workflow` §Cut a Build |
| `Planning/Phases/` | planning | phase execution-unit docs; **the folder tracks COMMITMENT, not status** (Workflow §Where a phase doc lives) — unnumbered `PhaseTBD_*` in `Future/`, numbered in `Phases/` whether SEEDED or ACTIVE, closed in `Complete/`; **Wave docs** as `Phase<first>_<last>_Wave_<Name>.md`, or `Phase<first>_TBD_Wave_<Name>.md` until the members are numbered (range-named; `<Name>` = the wave subject only — "Wave" implies the sequencer role, no "Sequencer" suffix; sit beside the phases they coordinate) | → research |
| `docs/Planning/Research/` | planning | investigations + decision records (`YYMMDD_R_*.md`); disposable-probe results carry `_Spike_` | — |
| `Planning/Support/` | planning | execution diagnostics (`Troubleshooting/`) + upstream diff notes (`UpstreamDiffs/`) + transient Issue **`Workbench/`** (gitignored contents) + workflow-feedback inbox (`WorkflowFeedback/`) | — |
| `Learnings/<Domain>/` | engineering memory | reusable costly-to-rediscover lessons by code-domain | one home each |
| `<Project>Overview.md` | product vision | vision, tenets, ecosystem members + responsibilities, the **entity Naming Matrix** (display / slug / repo token) | → `AI_Orientation` for the live repo map; → `NamingConventions` for code/contract grammar |
| `Methodology/AgenticEngineering_Workflow.md` | methodology | the "How we work" overview (units, two axes, tenets) + the Workflow Cycle + the Issue lane & Cut-a-Build + **process agreements** (Bucket B): phase numbering, Phase/Step/Task terminology, commit cadence & where commits land, archive location, Learnings Policy, Agent Roles | — |
| `Methodology/AgenticEngineering_ProjectFolders.md` | methodology | the folder layout + the Setup Checklist for a new project | → this Map |
| `Methodology/AgenticEngineering_DocumentationMap.md` | methodology | **this doc** — which doc owns what; tiers; genres; nav rules | — |
| `Methodology/Shareable/` | explainer (outward, non-governing) | audience-facing explainers of the methodology for readers *outside* the project (evaluate / learn / adapt) — the genericized `IdeasWorthStealing` cut + the `SystemOverview`/`LeadPlaybook` narratives. **Not loaded by agents to make decisions; the governing docs above win on any disagreement.** | → `AgenticEngineering_Workflow` for authority; see `Shareable/README.md` |
| `Glossary.md` | standard | platform terms — **one-line definitions only** (Detail-altitude rule); detail lives in the owning doc | → `NamingConventions` for grammar; → product specs for behavior |
| `NamingConventions.md` | standard | **naming grammar** — words, verbs, the cross-layer casing matrix, the per-class call template | → `CodingStandards` for impl rendering |
| `CodingStandards.md` | standard | **enforced C++ style** — casing/formatting/headers/ownership/errors; indexes project deltas | → `NamingConventions` for the words |
| `ToolingConventions.md` | standard | **tooling + artifact conventions** — the artifact taxonomy (build/script/test-source/fixture/golden/shared-article/output homes + the two-genre test-asset rule + structural guards), script location/naming, build/test/deploy/lint wrapper behavior, test-runner result handling, CI entry-point expectations | → `AI_Orientation` for current commands; → project docs for local tool details; |
| `architecture/` | product | **what the system IS** — components, boundaries, the invariants it keeps. **Empty until research commits to a stack**; every other stack-shaped doc points back at it | → the research doc's `## Resolved` for the decision behind each |
| product specs (`<Area>/`) | product | system / service / interface behavior, **one folder per product area** — created when the area exists, never in advance | per that area's index |

---

## One repo — where each kind of doc lives

**⛔ THIS METHOD ASSUMES ONE REPO, ONE BRANCH, ONE SET OF DOCS** (`AgenticEngineering_Workflow.md` §Scope and Document Locations). There is one `.ai/`, one `docs/Planning/`, one `docs/Learnings/`, and nothing travels separately.

- **`.ai/`** owns the **agent entrypoint**: orientation, the working agreement, and the commands. It is **thin** — no planning lives here.
- **`docs/Planning/`** owns durable planning: the Roadmap, phase docs, research, and the workflow-feedback surface. **Never keep a parallel roadmap anywhere else** — two registries is the failure this split exists to prevent.
- **`docs/Learnings/<Domain>/`** owns what the technology did that surprised you, one folder per domain the project actually has.
- **`docs/`** owns the durable product and stack surface: the product definition, `docs/architecture/`, and the standards docs.

⚠ **IF A PROJECT LATER SPANS SEVERAL REPOSITORIES**, a real question appears that this map does not answer: which docs travel with the code and which stay central. **Answer it then, in `LOCAL_DELTAS.md`, against the shape you actually have** — the general principle is that anything a person needs while working in an isolated checkout has to travel with it, and everything else centralises. **Do not pre-build that structure.**

## No-Duplication Rule

A rule/fact lives in **exactly one home**; everything else **links** to it (per `AI_WorkingAgreement` §Documentation-Shapes-Architecture and `AgenticEngineering_Workflow` §Learnings Policy). When two docs seem to want the same content, apply the disambiguation test above to pick the single owner, and replace the other copy with a one-line pointer + (if useful) the *reason*. Examples currently enforced: Learnings Policy → `Workflow` only; language-level rules → `CodingStandards.md` only; the project/repo map → `AI_Orientation` only.

**⛔ THE HIGHEST-COST INSTANCE, AND IT LANDS IN THE DOCS READ FIRST: A BRIEFING DOC THAT SUMMARISES WHAT A REGISTRY CURRENTLY SAYS.** An orientation file, an agent-rules file, a project entry point — each is tempted to transcribe the current state of the roadmap, the gate set, the live phase. **Every copy then goes stale on its own schedule, and they are precisely the documents a session reads before it has any way to know they are wrong.** *(Measured on one project: five hand-written summaries of the phase registry, all naming as live a phase that had closed six phases earlier; a sixth site listed fifteen checks when thirty existed.)*

- **A briefing doc names WHERE the registry is. It never restates what the registry currently holds.** A pointer cannot go stale.
- **When you replace a transcription with a pointer, leave one line saying the summary is deliberately absent** — without it the next writer reads the gap as an omission and helpfully fills it back in.
- **⛔ AND THE MOVE THAT FINDS THESE: a rule of the form "X does not belong in Y" is worth testing as "Y does not belong in X."** The duplication mechanism is symmetric and the reasoning usually transfers verbatim. *(The rule forbidding findings from leaking **into** the registry already existed, for this exact stated reason. Nobody had run it backwards.)*

**The one named exception — operational rendering.** `AgenticEngineering_Workflow.md` owns a process rule **canonically**; `.ai/commands/` deliberately **restate** the rules a command executes (the Build / Try / Strengthen stages in `/execute`, the plan it authors in `/plan`, …) so a fresh session is self-sufficient without re-reading the Workflow. That restatement is the rule's **operational rendering**, not a duplication violation — do not "deduplicate" it away; the Workflow Refiner keeps the two surfaces synced.

---

## Navigation / Hop Rules

Keep doc-reading scoped to the task. Spec subdirs in `docs/` are **maps, not reading lists**.

### Tiers (read in order; stop when the answer is in hand)

- **Tier 0** — `.ai/AI_Orientation.md` + the active phase doc (`Planning/Phases/`) + the relevant project's `_Docs_Index.md` (overview only).
- **Tier 1** — System / Service spec docs for the active task.
- **Tier 2** — Interface / module specs (panels, components, modals, IPC contracts) only if directly relevant.
- **Tier 3** — Code (only after the docs indicate it is necessary).

### Hop Rule

Follow at most **1 hop** from the entry doc unless the task explicitly requires deeper research.

### Link Conventions

- Use **repo-relative** paths inside a single repo.
- Use **platform-relative** paths (no leading slash, no `~`, no absolute) when crossing repos within the platform.
- Avoid absolute paths — they break on rename and aren't portable.
- Example: `docs/<Area>/<Subsystem>/<Component>_<Topic>.md`.

### Cross-reference format (doc → doc, doc → code)

- **Referencing another doc:** use a relative markdown link (`[Architecture](../architecture/README.md)`), or refer by prefix-and-name in prose ("see `System_Timeline` for timeline details").
- **Referencing code:** use backticks for symbols (`ColorPicker`, `CompositionService`), and include the file path when it helps (`src/systems/undo-redo.ts`).

### Doc status marking (`**Status:**`)

A durable doc declares its relation to current reality with a **`**Status:**` line** (front-matter / doc lead). The value taxonomy — one vocabulary, platform-wide:

- `Current` — describes the code as it stands.
- `Partial — <what's TBD>` — partly realized; the gap is named.
- `Placeholder — <scope>` — seed doc for unbuilt functionality; scope is named.
- `Aspirational — <owning future phase>` — intended forward-spec, deliberately ahead of the code; the parked phase that owns it is named.
- `Archived` — superseded/abandoned approach kept for history (lives under an `Archive/` folder).

Two granularities, one vocabulary: the doc-level `**Status:**` line classifies the **whole doc**; a **section/row-level** mark inside an otherwise-current doc uses an inline audit stamp — `*(P<NN>-audit: Aspirational — <phase>)*` — so partially-forward-spec docs (e.g. schema tables) stay honest row by row. Absence of a `Status:` line means `Current` by default. A project's front-matter *shape* (DocID / Primary Code / Related Code / Status) is defined in the project’s own doc-template file, which points here for the values. *(P38-audit: standardized from the pre-existing ad-hoc Status lines, 2026-06-12.)*
