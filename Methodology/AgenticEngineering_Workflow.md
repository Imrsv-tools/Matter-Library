# Agentic Engineering Workflow

> Genre: **portable methodology** (`AgenticEngineering_*`) — how an Agentic Engineering project runs the work. *(Formerly `AgenticEngineering_PlanningProcess.md`.)* For *which doc owns what*, see `AgenticEngineering_DocumentationMap.md`.

Purpose: define a repeatable workflow for platform research, phase planning, execution prep, and recovery when runs go off track — plus the process agreements (phase numbering, terminology, commit cadence, archive location) that govern it.

# How we work

*The onboarding overview — read this first. Everything below it is detail: the **Phase Workflow** is this same flow in five steps, in the **BUILD** lane by default; the **Issue lane** is it dialed lighter still; **HIGH-RIGOR** is opted into by name for work whose failure is expensive or irreversible; the Process Agreements govern all three.*

## One elastic flow

Work **enters as Research, commits at Discovery, and lands through Execute** — one flow, every size:

```
"look into X" ──► RESEARCH (intake: explores, commits to nothing; may dead-end,
                            may seed the Roadmap)   output: Planning/Research/ doc
                      │
                      ▼   deliberate go/no-go gate — kicked off when ready
      ══ COMMITMENT LINE ══
                      │
                      ▼
      DISCOVERY ────────────────► EXECUTE     (ordinary work: the Brief, then build)
           └──► PLAN ──►┘                     (HIGH-RIGOR only)
```

- **Research is intake, not a delivery stage.** It explores a topic (`/research`), writes a `Planning/Research/` doc, and either **dead-ends — a valid finish** — or seeds the Roadmap. The handoff to Discovery is a parked, deliberate gate, not a slide.
- **Discovery is the commitment line.** Reaching `/discovery` means the work is on a path to deliver (as a Phase or an Issue). Discovery → Execute never dead-ends; they're already committed.
- **One flow, sized by context — never by command.** Ordinary work runs **`/discovery` → `/execute`**: the Brief carries the step list and a compact build map, so there is no separate planning stage. **`/plan` is the HIGH-RIGOR lane only** — an explicit written plan for work whose failure is expensive or irreversible. The same commands serve every unit (`/discovery 41` works a Phase, `/discovery #145` an Issue). Trivial and big take the exact same steps — trivial just goes faster. Context budget is the natural regulator of agent handoff: trivial work flies through in one agent; big work spans agents, and **the doc is the resume state** at every handoff.

Each stage splits into **physics** — what reality forces at any size (a clean rollback point, build order, whatever cross-repo bookkeeping your shape imposes, standards conformance, the known-issues triage list) — and **ceremony** — coordination scaffolding that pays off at scale (multi-pass discovery logs, step skeletons, review cycles, Roadmap registration). **Physics never bends; ceremony dials with size — and size is discovered, not declared.**

## Units of work (the work axis)

| Unit | What it is | Anchor (snapshot · close) |
|---|---|---|
| **Wave** | several Phases that must stay **consistent with each other** — a shared contract, an order, a common exit condition — held together by one Wave doc. **Coupling is what makes a Wave, not size.** | — (batches Phases; each member keeps its own) |
| **Phase** | **ONE independently demonstrable increment — one thing a person can DO.** Runs the five-step Phase Workflow in the **BUILD** lane. *Not* "everything belonging to Media"; if the Outcome needs a list to explain what it really means, split it | snapshot only in the HIGH-RIGOR lane · close per §5 |
| **Issue** | standalone small-to-medium work, GitHub-tracked, picked off independently; elastic | own `Snapshot_Issue<n>` · light close (§Issue lane) |
| **Quick Fix** (`/quick-fix`) | a **shallow, self-contained** change that needs *no deep dive* — understand the project + conventions, go in, effect the change, done. Runs the full D→P→E flow **lightly and autonomously, in ONE context** (one agent, no cross-session handoff) | clean-trunk HEAD = free rollback (no named snapshot) · the **git commit is the record** — marked `✅ Quick Fix —` so it's greppable (no tracker, no Roadmap, no close ceremony) |
| **Side Quest** | something that pops out of active work and is needed *now* — **any size** (can grow phase-sized) | inherits the running Phase's anchor (WIP-HEAD, phase close) |
| **Step / Task** | sub-units inside a Phase or Issue (`12.3`, `12.3.5`) | — |

**Units are triaged on two axes — DEPTH first, then ANCHOR.** *Depth:* does this need a real dive — architecture, decisions, multi-step thought — or can an agent just **go in knowing the conventions and effect the change**? Shallow + do-it-now + finishable-in-one-context → **Quick Fix** (**`/quick-fix`** — it runs the whole D→P→E flow itself, lightly: a one-pass discovery, maybe one *simple* clarifying question — "which shade of purple?" — never an architecture call; it **skips §7 repo-sync**; the git commit is the record). **A Quick Fix can also be *drawn from* an existing Issue** — the lead points at a filed ticket whose fix proves shallow enough to just do now; it runs the same way but **closes the Issue out** (comment what changed + `Closes #<n>` + drop the `status:` label, no Roadmap/version — `quick-fix.md` §From-an-Issue). So Quick Fix is the **do-it-now sibling of `/issue-create`** *and* the **express lane for an already-filed Issue**. *Anchor* (for everything that needs a dive): *do I need this now, here?* Yes → **Side Quest** (rides the current phase's anchor — **any size**, can grow phase-sized). No → **Issue** (deferred, standalone, tracked). A big Issue **promotes to a Phase** — promotion isn't bureaucracy, it's "this finally needs an anchor of its own." **The safety valve runs both ways:** a Quick Fix that turns out to need a dive (touches many files, raises a real decision) **stops and promotes** to an Issue or Phase — *shallow is the default for small, ballooning kicks it up a tier.* There is no threshold to memorize: the agent **surfaces the signal** ("this is reading bigger than a quick fix / phase-sized — promote it?") and the lead calls it with the picture in front of them.

### What counts as ONE Wave

**A Wave is a coordination unit, not a big phase and not a theme.** It exists when several Phases share something that has to stay true across all of them — a contract they all speak, an order they must run in, a gate none of them closes alone — and that shared thing needs **one authoritative home** so N phase docs don't each carry a copy that drifts apart. That home is the Wave doc. **The coupling is the whole justification.** Ask it directly: *if these phases each went their own way, what would break?* A real answer means a Wave. No answer means you have several independent phases, and independent phases need no Wave doc at all — the Roadmap already sequences them.

Three tests, in order, and only the last one reaches "Wave":

1. **Is this actually more than one Phase?** Each member must independently earn a Phase — its own outcome, its own snapshot, its own close. If the parts only make sense delivered together, they are **Steps inside one Phase** (`Phase.Step`), and calling them a Wave is the common category error. Size alone never promotes: a large phase with fifteen steps is a large phase.
2. **Are they coupled?** If they merely share a subject, that is a theme. Sequence them and move on.
3. **Then it is a Wave** — and the coupling you just named is exactly what the Wave doc is for.

**Waves arrive from more than one direction, and none is more correct.** Sometimes the shape is visible in **research**, before a single phase doc exists — you can already see the shared contract, so the Wave is authored first and the members are seeded under it. Sometimes it is **carved out of a Phase whose discovery outgrew it** — the phase was the right container until the picture filled in, and now the work plainly needs several anchors. Occasionally a phase **already in flight** turns out to be several, which is the same call made later and more expensively. What differs is only what you already hold in hand; what a Wave *is* does not change, and neither does the discipline: **surface the possibility early, cut LAST, on the full picture.** Premature splitting on a partial picture forces a re-unification cycle when the coupling surfaces — a phase split in two, then folded back under a Wave doc once the shared contract became visible.

**When a Wave is carved out of an existing phase doc, that doc's discovery is the asset — place it, don't strand it.** Its cross-cutting findings are usually the Wave doc's shared-contract material, and its scoped findings belong to whichever member now owns them. Whether the origin doc is *promoted* into the Wave doc or archived and drawn from is a judgement call for the run. The invariant is the only part that matters: **every finding ends up somewhere with an owner, and nothing is left in a doc whose scope no longer matches it.**

**A Wave doc** lives at **`Planning/Phases/Phase<first>_<last>_Wave_<Name>.md`** — the **range** of phase numbers it spans (first + last, not every number; a wave of 17–22 is `Phase17_22_Wave_<Name>.md`), the `Wave` token, then **just the wave's subject name** (e.g. `Phase52_60_Wave_Materials.md`). **The `Wave` token already implies the coordinating / sequencer role — do NOT append "Sequencer" (or any role word) to the name** (forward-only; existing `*_Sequencer` names are not renamed). It sits in `Planning/Phases/` **next to the phase docs it coordinates** (not in `Support/`). **That range needs numbers the Wave often does not have yet** — one recognised in research, or carved before the lead numbers its members, has no `<last>`. Name it **`Phase<first>_TBD_Wave_<Name>.md`** (or `PhaseTBD_Wave_<Name>.md` when nothing is numbered) and **rename once the numbers land**: the interim name is a real state, not a mistake, and the cost is one `git mv` plus a link sweep. In practice the interim is short, because committing to a Wave is itself one of the normal moments a lead numbers a whole span (§Phase Numbering). Shape it around what it is authoritative for — **its status, its members, the contracts they share, their order, and the gate that closes the Wave** (`PhaseNN_MM_Wave_Template.md`); beyond those, keep it thin. **Anything a single member owns belongs in that member's phase doc, not here** — a Wave doc that restates member detail becomes a second contradicting source, which is the failure it exists to prevent. And a Wave is registered in **both** the Roadmap and the Wave doc: a Roadmap-only insertion leaves two authoritative, contradicting stories (`discovery.md` §Discovery discipline).

**What counts as ONE phase** — the two errors this definition exists to stop, both seen on a real cold-start:

- **Not a period of time.** "Soak — live on it for a few weeks" is not a phase; it has no deliverable and nothing to close.
- **Not a bundle of related things.** If two items get added and tested separately, they are two phases however adjacent they look — Mastodon and PeerTube are not "the public edge phase". Bundle by *deliverable*, never by theme.

## Roadmap status vocabulary

An entry's status names **which artifact exists**, which is why it is unambiguous:

| Status | Means |
|---|---|
| `RESEARCH` | The thinking lives in a research doc. **No phase doc** — the entry's pointers are the raw material. |
| `SEEDED` | **A phase doc exists.** It is what discovery → plan → execute run against; seeding it is the handoff off RESEARCH. |
| `ACTIVE` | Being worked. (The doc has already moved up to `Phases/` — see §Where a phase doc lives.) |
| `COMPLETE` | Closed; the phase doc moves to `Phases/Complete/`. |
| `TBD` | Not yet started. **Unnumbered** — see §Phase Numbering. A `TBD` entry may hold a perfectly settled position in the sequence; position in the list *is* the order, and it carries no number until work starts on it. |

**Which verb performs each transition** — the states above name the *what*; without the *who*, the seam gets improvised. `RESEARCH → SEEDED` is **`/discovery`, seeding and stopping** (`discovery.md` §Cold start step 1): it writes the phase doc and nothing else, and Pass 1 is a separate, lead-opened invocation. `SEEDED → ACTIVE` is `/discovery` opening Pass 1. *(**Numbering and the move out of `Phases/Future/` are governed SEPARATELY** — see §Phase Numbering and §Where a phase doc lives. **A phase may be numbered, and sitting in `Phases/`, while still `SEEDED`**: numbering is the lead's commitment, not a side effect of work starting. This sentence used to assert both couplings; it no longer owns either.)* `ACTIVE → COMPLETE` is the `/execute` close (stage 5, `execute_close.md`). **`/research` performs no transition at all** — it parks findings and commits to nothing, which is exactly why the seeding step needed a named owner rather than falling between the two verbs.

**⛔ THE ROADMAP *SECTION* FOLLOWS STATUS; THE *FOLDER* FOLLOWS NUMBERING. They move independently, and that is not a contradiction.** An entry sits in `## Active` because its status is `ACTIVE`, regardless of whether its doc is still under `Phases/Future/` (which tracks *numbering*, per §Where a phase doc lives). **A numbered-but-unclosed phase, and an unnumbered-but-live one, are both normal states** — do not "reconcile" them by moving the entry to match the folder, or the doc to match the section. This is the same two-register discipline the Roadmap↔phase-doc rule above states for status *words*, applied to *location*. *(A phase ran its whole discovery reading `### PhaseTBD_… — ACTIVE` while sitting under `## Future`, because §Phase Numbering says position in `## Future` **is** the order while `## Active` is defined as "live work" — both readings defensible from the text. The run correctly declined to restructure and raised it; it then dissolved by accident rather than by rule.)*

**A Wave carries its OWN status, distinct from its members'.** The Wave is `ACTIVE` from the moment it is the live work, while its members hold their individual statuses — so **`ACTIVE` Wave / `SEEDED` members is a correct and expected state**, not a bookkeeping error. The Wave's status answers *"is this the work in flight?"*; each member's answers *"has anyone opened it?"*. And a **numbered, `SEEDED`, out-of-`Future/`** member is likewise correct: `SEEDED` means *a phase doc exists*, and it stays the right word until Pass 1 opens — the vocabulary needs no fourth state for it.

**⛔ TWO REGISTERS, NOT A CONTRADICTION — the vocabulary above is the ROADMAP's.** The Roadmap entry carries the coarse lifecycle (`RESEARCH → SEEDED → ACTIVE → COMPLETE`); the **phase doc's own `Status:` line carries a finer working state** — `DISCOVERY (<date>)`, `PLAN DRAFTED`, `IN EXECUTION`. **A phase whose Roadmap entry says `ACTIVE` and whose doc says `DISCOVERY` is correctly recorded, not inconsistent.** Stated here because `discovery.md` §Cold start step 2 mandates the `DISCOVERY` stamp while this list does not contain the word, and a run that hits the gap writes two different words for one state and reconciles it silently — leaving the next agent to hit the same fork and possibly resolve it the other way.

**⛔ AND THE FINER LIST IS ILLUSTRATIVE, NOT CLOSED — it reads as exhaustive because it is a bare three-item enumeration, and it is not.** The Roadmap's coarse lifecycle **is** closed (`RESEARCH → SEEDED → ACTIVE → COMPLETE`); **the phase doc's working register is not, because it tracks the verbs, and the verbs have more states than three.** ⇒ **If no listed word describes the doc's real state, COIN THE OBVIOUS ONE — `<VERB-PAST-PARTICIPLE>` or `<VERB> (<date>)` — and use it.** Do not stretch a listed word to cover a state it does not name, and do not stall on the vocabulary: a `Status:` line contradicting the doc's own footer is worse than a word this list has not seen. *(Two runs hit this within a day. One ended a plan round on the lead's *"andf mark approved"* and wrote `PLAN APPROVED (<date>)` — correct, and outside the list. The other finished discovery and handed to `/plan`, and **could find no term for "discovery done, plan not started"**; it left `DISCOVERY (<date>)` standing against a footer saying discovery was complete, and declined to fix it because `/retro` is terminal. Both were reasoning about whether the list was closed. It is not.)*

## Where decisions live

**At the altitude they were made, accreting as the funnel narrows** — research doc → phase doc → discovery → plan. Each tier records what it decided; none pre-empts the next. There is **no single decision registry**, and looking for one is the classic error:

- A research-tier decision lives in the deciding doc's Status footer, consolidated into the thread authority's `## Resolved` section.
- **Not** in the `Roadmap.md` — it registers *units of work*, and all detail lives in the phase doc.
- **Not** in the `README.md` — that describes what the project *is*; the Planning tree owns where it stands.

## The two axes — work vs ship

The units above organize the **doing** (the work axis). **Shipped state is marked on a separate ship axis.** *Done* and *released* are different questions, and conflating them is how "closed" comes to mean two things at once.

**If the project ships a versioned artifact** — a packaged runtime, a tagged release, a pinned image digest — name the axis explicitly and keep three answers distinct: **what marks a release · what records its contents · where an issue is stamped as shipped.** **"Closed by" ≠ "shipped in":** an issue is fixed *in code* at its commit, and *available to a user* only once a release carries it. Both events get recorded; neither substitutes for the other.

**If the project deploys continuously**, the ship axis *is* the deploy and there is no version line to reserve or confirm. **Any carried instruction to reserve a version line is then a no-op** — but see §Phase Workflow stage 2: a project with no version line usually still has *other* centrally-allocated counters (gate ids, id prefixes, migration ordinals) that a phase must claim at execution rather than bank from a plan.

## Tenets

### Snapshot before execution

> **Always have a clean rollback snapshot before execution — at every scale — unless the lead explicitly says don't bother** (very unusual; echo it back before skipping).

The snapshot's value *is* the free "whoa, back up, let's replan" move — and that move must be free at every scale, because the fix that *looked* small is exactly the one that explodes. It is doubly load-bearing in this repo: an explosion doesn't mess up one tree, it strands half-done state across four repos along the deepest-first cascade; hard-resetting everything to one named `Snapshot_` is a single move. One principle, three renderings: **Phase / Issue** → a named marker commit (`Snapshot_Phase<N>` / `Snapshot_Issue<n>`), kept permanently; **Side Quest** → its clean point is the running phase's current WIP-HEAD. (`execute.md` §Before you touch anything and the Issue lane point up here rather than restating it.)

### Branching — trunk by default

A **guideline, not a rule**, in the same rollback-safety family as the snapshot tenet:

- **Default = trunk-based.** Work on the shared trunk, **commit often** (local commits are the rollback granularity), **push when stable**. This is the norm for all Issues and ordinary Phases — the `Snapshot_*` tenet provides rollback; a branch is not needed for safety.
- **Rollback economics is the trigger.** While work is unpushed, rollback to a snapshot is a cheap local reset; once pushed past the snapshot to a shared trunk, it becomes a public revert. "Push only when stable" is what keeps rollback cheap. **Branch when you'll need to push intermediate states that aren't trunk-stable** — big/long/risky multi-session work that wants remote backup or cross-machine sharing before it's stable, and/or where half-done would break the trunk for a parallel collaborator. A long-running restructure branch is the shape this exception exists for.
- **The branch unit is the big effort** (a Wave or a big restructure Phase) — **never an Issue.** Keep the bar high: branching costs whatever coordination your repo shape imposes, and on a multi-repo project that cost is large.

### A claim carries its measurement

> **Write what you MEASURED and WHEN — never a settled property.** A dated claim goes visibly stale; a present-tense one goes silently stale and reads authoritative the whole time.

The characteristic failure of this method is not a wrong action — it is a **settled-sounding sentence, written by a competent agent, that nobody re-measured.** It has appeared in every carrier the method has: a plan's risk pricing, a code comment, a transcribed handoff command, a gate's expected value, an orientation doc's statement of project state. In most cases the correction was **one command**.

- **The countermeasure is not "verify more" — it is the dated form.** `LIVE (reconciled at step 4)`, `UNOBSERVED`, *"re-run this check at execution start"*. A claim that carries its own expiry cannot silently become false.
- **An inherited claim is a hypothesis, including one you wrote yourself last session.** Name the subject it was measured against: *the tool or the tree* · *the plan's belief or this run's output* · *the doc's date or now*.
- **⛔ A THROWAWAY COMMAND IS EVIDENCE TOO.** An ad-hoc search, count or status check written mid-step is trusted **more** than a test — it feels like direct observation rather than a test — and it is the least scrutinised output in the process. Before acting on one, ask what it would print if the thing you are checking were absent.

### Reading a green result

> **A pass is evidence only if a fail was possible.** Of any green you are about to rely on: *can it fail?* and *can it pass?*

⚠ **This is not a licence to build proof apparatus** — §Testing Policy governs what you *write*, and its answer is usually "nothing". This tenet governs how you **read** a result you already have.

- **A check can pass for a reason unrelated to its subject** — satisfied by its own input echoed back, or asserting a value the fixture itself wrote.
- **A check can fail for the wrong reason and slander the thing under test.** Predict what should go red *before* you run it, then account for every difference.
- **⛔ AND THE LAYER PER-CHECK REVIEW CANNOT SEE: EVERY CHECK SOUND, THE SET BLIND.** Individually correct checks share one unexamined entry path. The question is cheap and set-level — **what do ALL of these never touch?** *(On one project: 154 assertions across six gates, each defensible; not one ever loaded the screen the work existed to deliver.)*

### The human's waiting time is a budget

> **Every other resource here is instrumented — context, test counts, commit cadence. Time spent with a person sitting waiting is not, and it is the most frequent cause of intervention.**

- **The measure is §Phase Workflow's: how long until the lead can click the thing.** Missing it is a scope or loop alarm.
- **⛔ THE WRONG CONCLUSION IS "VERIFY LESS".** The same evidence that indicts waiting also shows cheap checks earning their cost. **Make the loop cheaper, not the proof weaker.**
- **The number that settles the priority:** a person clicking through the product for ~90 minutes found **nine defects that had survived roughly 120 passing assertions.** That is why stage 3 hands over a URL and stops.

## Scope and Document Locations

**⛔ THIS METHOD ASSUMES ONE REPO, ONE BRANCH, ONE SET OF DOCS.** That is the shape it is written for and the only shape it is tested against. **If a project later grows into several repositories, the method grows with it** — the cross-repo bookkeeping (build order, a SHA cascade, a shared numbering line) is real physics and will need writing down at that point. **Do not carry apparatus for a shape you do not have.**

This process operates against the `.ai/` **agent entrypoint** and the **durable `Planning/` surface**. Planning is durable project truth — it lives in `docs/Planning/`, not under `.ai/` (see `AgenticEngineering_DocumentationMap.md` §load-bearing rule). Unless otherwise stated, the references below mean:

- `Roadmap.md` → durable `docs/Planning/Roadmap.md` (the phase registry; formerly `.ai/plan/build_plan.md`).
- `AI_Orientation.md` → platform `.ai/AI_Orientation.md` (formerly `context.md`).
- `AI_WorkingAgreement.md` → platform `.ai/AI_WorkingAgreement.md` (formerly `conventions.md`).
- `PhaseXX_*.md` → durable `Planning/Phases/PhaseXX_*.md` (active phases live **directly** in `Phases/`; no `Active/` subfolder).
- Cross-project `research/*.md` → durable `Planning/Research/`.
- Project-scoped research for a **separate satellite project** → that project's own repo (see `AgenticEngineering_ProjectFolders.md`). *(On the ordinary one-repo project there is no such split; everything lands in the one `Planning/Research/`.)*

**Phase numbering is a single shared line** — one sequence for the project. *(A satellite project in its own repo keeps its own numbering and is referenced as an external track.)*

## Where stack knowledge lives

**⛔ THE METHODOLOGY AND ITS TERMS ARE STACK-BLIND, AND STAY THAT WAY.** No command doc names a language, framework, engine, package or file of yours. **A project's stack knowledge accumulates in project-owned docs, and the methodology references them BY ROLE, never by content.**

The order is always the same and nothing skips ahead of it:

**research settles the tech → `docs/architecture/` records what the system IS → `CodingStandards` · `ToolingConventions` · `NamingConventions` record how it is built → `Learnings/<Domain>/` records what has hurt, one entry per failure actually paid for.**

⛔ **NOTHING IN THAT CHAIN IS POPULATED BEFORE IT IS UNDERSTOOD.** An empty `Learnings/` on a new project is **correct**, not a gap. A `CodingStandards.md` written before a spike commits to a stack is a guess wearing the costume of a decision, and every later reader treats it as settled.

⛔ **AND THE METHODOLOGY NEVER CARRIES THE FACT — ONLY THE POINTER.** *"Your durable learnings home"*, *"your project's tooling-conventions doc"*, *"the namespaces THIS project allocates from"*. **The moment a command doc names one of your files, every other project reading that sentence has a dead path and a mandate it cannot execute** — and a mandated read of a file that cannot exist teaches an adopter to ignore the whole block it sits in.

**`LOCAL_DELTAS.md` is the seam, and its length is the diagnostic:** a long one means portable fixes are being landed locally.

⚠ **THE ONE CATEGORY THAT *IS* SAFE TO SEED ON DAY ONE IS THIS METHOD'S OWN VOCABULARY** — Phase, Step, Task, Side Quest, Quick Fix, Issue, Brief. Those are fully understood at adoption, which is exactly why `docs/Glossary.md` ships with them (as a one-line gloss **plus a pointer to the owning section** — never a second copy of the definition).

## Learnings Policy

Read learnings at planning time, not at implementation time, to keep working context tight. **Exception — domain learnings at discovery:** when a phase is **lock / threading / concurrency / lifecycle-sensitive**, or touches a domain that has a `Learnings/<Domain>/` doc, **force-read that domain's learnings at discovery kickoff (§2), not at §5/§9.** Discovery is exactly where the costly-to-rediscover invariant (a caller-held-lock rule, a lifecycle ordering) pays off — reconstructing it from code is wasted passes. The "learnings at planning time" rule keeps *implementation* context tight; it shouldn't starve discovery of the one doc that resolves its hardest question. (`/discovery` front-loads this.)

- Code-domain learnings live in the durable `docs/Learnings/<Domain>/` home — **one folder per domain your project actually has.** Create a domain the first time it earns an entry, never in advance.
- Cross-cutting build / deploy / infra learnings live in a **cross-cutting domain folder** alongside the code domains.
- A learning lives in exactly one place — link, don't duplicate.
- ⚠ **AND IF THE PHASE TOUCHES NO DOMAIN THAT HAS AN ENTRY — OR THE TREE IS STILL EMPTY, WHICH IS THE CORRECT STATE FOR A YOUNG PROJECT — SAY SO IN ONE LINE AND MOVE ON. That is a DISCHARGED read, not a skipped one.** **Do not perform a listing you did not use:** a read recorded as done-and-not-done is worse than an honest skip, and it teaches the next run that this whole block is ceremony. *(The domains reflect what has hurt so far, which skews toward infrastructure — a phase touching none of them legitimately has nothing to read.)*
- ⛔ **`Learnings/` IS FOR WHAT THE TECHNOLOGY DID, NEVER FOR WHY THE METHOD SAYS SOMETHING.** Process rationale belongs with the rule it justifies (§Where stack knowledge lives); putting it here puts process history into the one tree whose entire value is being about the stack.

### Learnings Criteria

Add to learnings docs ONLY if it meets ALL of the following:
- **Non-obvious** — a competent dev reading the docs would still get it wrong.
- **Poorly documented** — missing or buried in official docs.
- **Costly to rediscover** — significant debugging or subtle bugs.
- **Specific** — a concrete pattern, not a general principle.

If nothing qualifies: "No new learnings this step."

## Agent Roles

Two assistants, used at different passes (interchangeable for general review cycles; this is the default rhythm):

- **Codex** — first-pass research baseline (steps 2–3) and plan / sequencing-risk review (step 11).
- **Claude** — second-pass reviewer + edge-case / implementation pressure-testing (steps 3, 5), test-strategy + step-sequence proposal (steps 6, 8), and PlanMode implementation-plan authoring (step 9). In PlanMode, Claude writes to the harness plan file (under `~/.claude/plans/`, outside the repo), never the Phase doc.

## Phase Workflow — five stages

**⛔ THE MEASURE IS: HOW LONG UNTIL THE LEAD CAN CLICK THE THING?** Target **60–90 minutes** from opening a phase. Missing it is a **SCOPE alarm** — the phase is too big, or the loop is too slow — **never** a cue to certify harder before showing him.

**⛔ FIVE STAGES IS THE WHOLE FLOW. THE USEFUL MECHANISMS BELOW ARE FOLDED IN AS QUESTIONS, NOT PROMOTED BACK INTO STAGES OF THEIR OWN.** *(Lead ruling, 2026-08-29: "keeping ten useful mechanisms must not mean retaining ten mandatory stages. **Preserve the function, not the section number.** Otherwise we recreate the same workflow with shorter prose.")* This replaced a sixteen-stage spine in which nothing was built until §13 and no person touched the result until §14, with the test surface designed at §6 before a line of code existed. That spine was implemented faithfully and shipped two phases that closed COMPLETE and green **while a writer could not create an article at all.**

**Two lanes. BUILD is the default. HIGH-RIGOR is opted into by name** — authorization · secrets · destructive migrations · data loss · the public edge · anything whose failure is expensive or irreversible. **A phase does not start in HIGH-RIGOR because high-rigor rules exist somewhere in the methodology.** It moves there when evidence during the work warrants it; say so when it happens.

### 1) Brief

One page in the phase doc. Discovery still happens and still earns its cost — it is **a conversation that compiles**, not a transcript that accumulates. It is finished when this can be written:

- **`Outcome`** — one sentence: what a **person can DO**. Plain, non-technical.
- **First human test** — the **exact click path** and the URL, written **before any code**. It is what stage 3 hands the lead.
- **Relevant-doc review** — a top-down read of the product docs *anchored to the Outcome*, producing the seed-vs-docs conflict list. **This is where discovery earns its cost**; skipping it is how a phase builds the wrong kind of thing.
- **⛔ Reuse check — the primary question, and it is one question:** *What does the selected stack already provide, and which standards are materially implicated by this change?* **Reuse is primary; conformance is targeted to the contracts actually touched.** The full standards sweep belongs to HIGH-RIGOR or a final cross-system review, not to ordinary work.
- **Risk lane** — `build` or `high-rigor`, with the reason named.
- **Split decision** — see below.
- **Step list** — the short sequence of **vertical** steps (§Phase / Step / Task Terminology). **This IS the phase's step sequence**; there is no separate skeleton stage and no second planning artifact.
- **Compact build map** — known seams, likely files, step ordering. Enough for a handoff. **Not a separate exhaustive implementation plan.**

**⛔ SPLIT TRIGGERS — and total phase-doc length is NOT one of them.** Split when: **more than one independently demonstrable journey** is in scope · the **active execution packet has become unscannable** · **time-to-first-click exceeds the budget**. *(A provenance appendix may legitimately add length without triggering anything.)*

**⛔ DISTIL, DO NOT APPEND.** A discovery pass ends by **rewriting the current synthesis**, never by appending another pass beneath a stale one. Superseded hypotheses compress to one sentence where the rejection matters; otherwise git owns them. Sources are pointers, not copied prose. **Keeping the phase doc current is part of authoring the Brief — it is not a separate integration stage.**

**Before you start: record `branch`, `HEAD`, `git status` and who else is working here.** ⛔ **This tree is shared and dirty by design — "just pull" is not the lightweight action.** Pull only when it is safe to.

### 2) Build

- **Native capability first.** Configure before you write. Every custom layer must name the native behaviour it replaces and the gap that justified it — *"we may eventually need more control"* is not a gap.
- **Smallest vertical step**, on the dev loop with hot reload. **Do not rebuild the production image to see a change.** A command that takes minutes is not an inner-loop tool.
- **⛔ Claim live namespace values AT EXECUTION — never bank one from a plan or a doc.** Version constants, gate ids, entity-id prefixes and migration ordinals are centrally allocated and a sibling phase moves them under you. Read the live value at the moment you use it.
- **Rollback is your own frequent scoped commits.** Every run records its starting SHA; ordinary work needs nothing more. **A dedicated snapshot commit is EARNED** — by a destructive migration, a security-sensitive change, or a risky multi-step sequence.

### 3) Try

**A cheap agent smoke that the path is alive — then the lead clicks it, within 60–90 minutes.** Hand back **a URL and the exact click path**, and **STOP**.

**⛔ NEVER BREAK THE LEAD'S ENVIRONMENT TO GET HERE.** Do not stop, tear down, rebuild or re-point the running stack without telling him first — never as a convenience, never silently. If a restart is genuinely needed: say so, do it fast, then **open the surface and confirm it loads and is usable.** A green gate, a healthy container and a passing build have each certified an unusable admin on this project; **only loading it proves it.**

*(This is not a ceremonial sign-off. Working through a phase feature-by-feature — build, the lead tries it, fix, try again — has repeatedly found that a great deal was broken which the headless suite reported as fine.)*

### 4) Strengthen

**Repair what the lead's use exposed**, then add **proportionate** robustness and regression tests — see §Testing Policy. Loop 2→4 per step; each step stays something a person can use, never a layer with no user path.

**If a run must stop mid-flight: suspend with a ledger** — where you are, what is next, what is unresolved. **If the same defect survives repeated verified repairs, switch to the per-layer repair ladder** (`execute_repair.md`). ⛔ **Do not read the ladder unless you are in that trouble** — knowing it exists is the whole requirement.

### 5) Close

- **Compact handoff ledger** — `step · commit · result · next`.
- **Targeted doc-conform** — update the documentation for **the contracts this phase actually changed**. ⛔ **Not another whole-corpus standards sweep.**
- **Explicit loose-end disposition** — every open thread gets one: **fixed · ruled out · deferred as an ADDITION**. A **correction to a surface this phase authored is not deferrable**: fix it, rule it out, or demote the headline. You may not ship `COMPLETE` alongside a list of gaps in the thing you just completed.
- Commit with **explicit paths**; move the doc to `Planning/Phases/Complete/`; update the Roadmap entry (status and pointer only — never the `Outcome` text). **Push stays lead-gated.**

---

## Testing Policy

**⛔ THREE QUESTIONS. THAT IS THE ORDINARY TEST SURFACE.**

1. **What existing test already covers this?**
2. **What is the cheapest observable the agent needs while building?**
3. **Did the human test expose a regression that now deserves a test?**

**Question 1 comes first on purpose** — it is the check that stops the suite growing, and it is the one that was never asked.

**⛔ ONE REAL-PATH SMOKE IS THE ORDINARY MAXIMUM, BY DEFAULT — and it is a ceiling, not a requirement to author a new gate.** RED demonstrations, discriminator design, gate-readiness matrices and premise-proof gates are **HIGH-RIGOR only.** Anticipated edge cases, coverage, symmetry and *"proving the assertion is capable of failing"* are **not** reasons to write anything.

**⛔ GATES ARE FROZEN** *(lead ruling, 2026-08-29)* — author **no** new `scripts/check-*.ts`. Thirty already exist, and measured on 2026-08-29 they carry **13,751 lines of real gate code against 11,048 lines of real application code — 1.24 : 1, more test than product.** Not one of them asks the only question that has ever caught a user-facing defect here: *can a person load the page and use it?* The existing suite keeps running; **pruning it is the lead's call on a reviewed proposal.** If you believe question 3 genuinely requires a new gate, **say so in the handback and let the lead rule. Do not write it.**

**Tests accumulate from observed failures.** That is the only way a suite stays proportional to the product it protects.

---

## The phase doc — compiled context, not a transcript

The phase doc owns **intent and compiled context**. The tree owns **current mechanics**. Git owns **the narrative**. The same finding is not copied into all three.

The execution record is a **ledger**, not an essay:

```text
step · commit · result · next
```

**⛔ Findings go in the commit message. Unresolved decisions go in the handback.** Neither gets restated in a growing chronological log. **An abrupt stop must leave resume state in the ledger — never defer it.** *(Measured: one phase's execution log ran **1,990 lines — 53% of the doc and 7× the plan it was executing**, at ~87 lines per entry, against a spec that already said "a one-line entry".)*

---

## Do not refine the workflow inside a feature

Workflow observations **park** during execution and drain in a separate refiner session — `/retro` deposits, `/workflow-refiner` triages. **The product and the operating system for building it must not change in the same loop.** The one exception is a method problem actively blocking safe progress.

---

# The Issue lane (the same flow, dialed light)

An **Issue** (§How we work) is standalone small-to-medium work tracked as a **GitHub issue** — the durable home and record. The working medium during the work is a **transient local workbench**, because GH comments are a poor iterative-edit surface for an agent (append-only, network round-trips, comment sprawl). The lane is the same D→P→E flow with three knobs dialed light:

| Knob | Phase | Issue |
|---|---|---|
| Working artifact | durable `Planning/Phases/Phase<N>_*.md` | transient `Planning/Support/Workbench/Issue<n>_Name.md` (contents gitignored; published to the ticket at close) |
| Snapshot label | `Snapshot_Phase<N>` | `Snapshot_Issue<n>` |
| Close | Phase Workflow §5 (move to `Complete/` · Roadmap · `🎉 PHASE COMPLETE`) | light: publish → delete workbench · `✅ Issue #<n> — <Title>` + `Closes #<n>` · no Roadmap entry |

**Pre-flight (the lane's standing prerequisite — the Issue analog of `/execute`'s "sandbox OFF").** The whole lane is GitHub-backed, so before capture or any lifecycle comment verify **`gh` is installed + authenticated (`gh auth status`) and the repo has Issues enabled**. A fresh agent on a clean box otherwise hits `gh: command not found` (exit 127) or an auth error and stalls mid-`/issue-create` (the dogfood-#1 trap — `gh` wasn't installed at all). Install (`sudo dnf install gh`) + `gh auth login` (device flow) is a one-time host setup, not per-issue.

**The flow:**

1. **Capture** — `/issue-create` files GH issue `#n` (the lifecycle's `captured` state). Issues live in GitHub only — no `Planning/Issues/` tier, and **never on the Roadmap** (an Issue reaches the Roadmap only by being bundled into a planned Phase).
2. **Pickup** — on "work on #n": create the transient workbench `Planning/Support/Workbench/Issue<n>_Name.md` (mirrors `Phase<N>_Name.md`; contents gitignored via that folder's `.gitignore`). Because it's gitignored, a rollback to the snapshot never touches it — it doubles as the derail route's "failure notes outside rollback scope" surface for free.
3. **D→P→E** — `/discovery #n` → `/plan #n` → `/execute #n`, all editing the workbench; the same stages and discipline as a Phase, dialed lighter (often one discovery pass, an inline mini-plan, no full review cycle). `/execute #n` snapshots **`Snapshot_Issue<n>`** (the snapshot tenet, §How we work); code WIP-commits land wherever that code lives. The Issue's one real-path check is a first-class deliverable.
4. **Close (light)** — **publish first**: post the distilled summary (optionally the full workbench as one collapsed comment) to GH#n, **then** delete the workbench, then commit **`✅ Issue #<n> — <Title>`** with **`Closes #<n>`** in the body at the repo where the tracker lives; push auto-closes the ticket. **No** move-to-`Complete/`, **no** Roadmap entry, **no** version event — the work rides the project's next release, whatever marks one. **Two close-discipline catches:** (a) **drop the `status:` label** as part of closing — `status:` is an *open-lifecycle* axis (`requested→defined→approved→in-progress`); Complete = closed-with-no-status-label, so a closed issue still wearing `status:in-progress` is stale (`gh issue edit <n> --remove-label "status:<x>"`). (b) **On a multi-repo project, verify any recorded cross-repo pointer names the issue's OWN last content commit** — a late doc refresh after the last bump leaves it stale, and a parallel commit stacked above yours must not be folded in. **Single-repo projects skip this entirely.**

**Four-comment lifecycle (comments mark the progress narrative; a label taxonomy carries the axes; no boards/project fields until a real gap shows).** Five conceptual states — `captured → active → planned → landed → fixed-in-build`. Two are intrinsic to GitHub (captured = open; landed = closed via `Closes #n`); the rest are marked by comments on the ticket. *(The orthogonal `type:`/`area:`/`status:`/`source:` **labels** — `ToolingConventions` §Issue tracker conventions — are now live alongside these comments; a GitHub **Project board** stays the future upgrade path if a single-select enforced Status is ever wanted.)*

- **pickup** → "Started discovery; local workbench `Issue<n>_Name.md`." (makes active work visible off-machine — the workbench itself doesn't travel)
- **plan-ready** *(non-trivial issues only)* → a short distilled plan.
- **close** → the distilled summary, posted **before** the workbench is deleted.
- **release** → a "shipped in" stamp on the issue, applied when the release that carries it goes out (§The two axes). Projects that deploy continuously have no separate event here.

All four comments are **agent-owned** — a rule with no owner doesn't execute. Authorization: on the **first** lifecycle comment for issue #n in a session, the agent asks once — *"posting lifecycle comments to #n as we go — ok?"* — and a yes covers that issue for the session. (`/issue-create`'s show-then-fire convention stays as-is for issue *creation*.) **Trivial path:** pickup → close → fixed-in-build; trivial issues fly through with no plan-ready comment.

**Promotion (Issue → Phase).** Pure judgment — no threshold exists; Issue discovery is responsible for **surfacing the signal** ("this is reading phase-sized — promote it?") and the lead calls it with the picture in front of them. Mechanics: the GH issue **stays open as the tracker** and links to the new Phase doc; the discovery done so far carries straight into the phase doc (zero waste); `Snapshot_Issue<n>` is superseded by the Phase's own `/execute` snapshot.

**Three dispositions when an issue grows mid-discovery — promote / stay / defer-to-phase.** Promotion isn't the only escape valve when an issue turns out bigger than it looked. The three:
- **Promote** — the *whole* issue is phase-sized → it becomes a Phase (above).
- **Stay** — it's still issue-sized → run it as an Issue.
- **Defer-to-phase** — the issue has a **small shippable slice plus a big part that belongs to a future phase**. Ship the slice as the issue; **deposit the architectural/big-part findings into the owning future-phase doc** (`PhaseTBD_<Name>.md`), keeping the issue scoped to the slice; **close the issue when its slice lands** (the big part now lives in the phase doc, not as an open tracker). *(Reference the future phase by doc path/name, never a bare "Phase N" — §Phase Numbering.)*

**Bundling several issues into a planned Phase (the §6.5 path — multi-issue sibling of defer-to-phase).** When a cluster of related open issues is best worked together as one planned unit (a "Light Panel" phase absorbing #5/#8/#12), bundle them — reusing existing primitives, no new machinery:
- **Form** — create `Planning/Phases/Phase<NN>_Name.md` whose scope **lists + seeds from** the constituent issues, and add the **Roadmap entry** (the only way Issues reach the Roadmap). The issues are *scope inputs*, not 1:1 steps — `/plan` gives the phase its own `Phase.Step` map.
- **Mark it (git + GH):** a **GitHub Milestone `Phase <NN> — Name`** (the purpose-built grouping — progress bar, filter, closes with the phase; milestone description → phase-doc path; **no per-phase labels** — that's cruft); a **per-issue comment** `Bundled into Phase <NN> (<doc path>)`; and **`Refs: #5 #8 #12`** in the phase's step / `🎉 PHASE COMPLETE` commits (the git→issue link — **`Refs:` not `Closes:`**, so a *partially*-delivered issue isn't auto-closed on push; the deliberate close is the close's issue-close coda). *(Milestone over a tracking/parent issue: a parent issue would make the phase itself a GH issue — we keep phases as docs, so the milestone is the cleaner bridge.)*
- **Lifecycle** — issues **stay open** through bundling (not done yet); worked **as the phase** (full D→P→E ceremony); **closed in the close's issue-close coda** (`execute_close.md` row C) (comment → drop `status:` → close; `Refs:` not auto-`Closes:`, so partial delivery is stated honestly); close the milestone at phase complete.
- **Version** — the **phase owns the version** (MINOR++ at close); bundled issues ride the phase's MINOR (not a loose Build), each still getting `Fixed in 0.M.B` at the next Cut-a-Build.
- **One line:** *Milestone + per-issue "bundled" comment + phase-doc list + `Closes #n` commits + Roadmap entry; issues stay open → close via the phase.*

**Deferred-work capture — direct to GitHub (the `Planning/DeferredBacklog/` folder is retired).** Found something to defer (an unrelated bug, tech-debt, a small improvement)? It's a **GH issue**, not a backlog `.md` file. The old "backlog file → graduate when picked up" pipeline collapsed to the predicted endgame: capture *is* filing. **The one preserved nicety** — the backlog gave a frictionless *no-network / no-confirm* mid-`/execute` capture (an AFK executor can't fire `/issue-create`'s confirm gate). Preserve it: a mid-run defer lands as a **line in the execution log / workbench**, promoted to a GH issue at the **next checkpoint** (confirmed, batched). *(The existing ~22 backlog items were bulk-migrated to GH issues in creation order, 2026-06-13, and the folder retired.)*

# Process Agreements

> These govern *how the work runs* (Bucket B). They live here, with the workflow they support; engineering agreements about *how the software is built* (Bucket A — the project's own architectural principles) live in `.ai/AI_WorkingAgreement.md`.

## Phase Numbering

- **Every code domain the main project owns shares a single numbering line.** Where a project spans several, each phase carries a primary-domain tag and a touches list; a single-repo project needs neither.
- **Standalone projects keep their own numbering inside their own repos.** The main `Planning/Roadmap.md` references them as external tracks.
- **Integration phases between a standalone and the main project are numbered on the main line**, and live wherever the integrating code lives.
- **Reference future / unstarted phases by doc path or name — never a bare "Phase N".** Numbers are assigned late, and an unstarted phase's *internal* renumbering collides with **completed** roadmap phases (dogfood-#1 wrote "Phase 22/24" — both already done). Future phases are in fact all unnumbered `PhaseTBD_*` docs; cite the doc path (`PhaseTBD_StageCompositionLifecycle.md`) or its name.
- **A number attaches when the LEAD assigns it — not when a phase is sequenced.** Being listed in the Roadmap, even in a fully settled order, is *not* what earns a number; everything unassigned stays `PhaseTBD_<Name>`, and **order is position in the list, never an ordinal** — so never add ordinals, letters, or "first/second" to an unnumbered entry. **How many get numbered, and when, is the lead's call.** Often it is one, as work starts on it. But committing to a **Wave**, or to a run of phases whose order is settled by real dependencies, may reasonably number several at once — that is a normal use of the rule, not a deviation from it, and a doc should not have to defend it. What is never right: **an agent assigning a number**, or numbering drifting into a bookkeeping habit that runs ahead of the lead's commitment.
  - **The reason matters more than the count, because it names what the lead is trading.** While a phase is unnumbered, two things are free: **inserting a phase between two existing ones**, and **splitting one listed phase into several** once it is properly understood. Both get expensive the moment numbers exist — a written-down number becomes a phase number, renumbering is then treated as costly, and the sequence calcifies. **Numbering a span is a deliberate decision to give that freedom up for that span**, which is exactly why it belongs to the lead and not to a default. Numbers assigned this way are **planning IDs, not promises**: if the shape moves again, rename rather than contort.
  - **⛔ AN ID THAT HAS LEFT THE REPOSITORY IS FROZEN — and on an unnumbered phase, ids leave constantly.** Once a finding or ruling id (`F-12`, `RD-IA-7`) appears in a **commit message, an issue, or a PR**, it is permanent: those artifacts are immutable from inside the repo, and renumbering to match a number the lead assigns later invalidates every one of those citations for cosmetic consistency. **So never promise a renumber.** On an unnumbered phase, **pick an id form you are willing to KEEP** — a name-derived stem (`RD-IA-n`) survives numbering; a placeholder that presumes one (`F-n → F<NN>-n`) does not. **The phase-doc pointer, not the id's shape, is the durable link.** *(A discovery wrote a convention note promising to renumber `F-n` → `F<NN>-n` when the phase was numbered. By the time it was, those ids were cited in five filed issues and eight commit messages; the promise had to be withdrawn in-doc.)*

## Phase / Step / Task Terminology

- **Phase** — complex interconnected functionality. Top-level unit of work. Numbered (Phase 11, 12, …).
- **Step** — manageable / testable chunk inside a phase. Numbered `Phase.Step` (e.g. `12.3`). **⛔ AND IT IS VERTICAL: something a person can USE, never a layer with no user path.** A schema, an endpoint or a component with nothing reaching it is not a step, however much work it was — that is the horizontal build the five-stage flow exists to prevent, and it is what produces a finished phase nobody has ever used.
- **Task** — atomic, validatable check inside a step. Numbered `Phase.Step.Task` (e.g. `12.3.5`). **Available when a step genuinely needs decomposing; not a level every step must populate.** ⚠ **This is the ANSWER to the letter-suffix urge** — see the numbering rule below.
- **Side Quest** — unplanned work surfaced mid-phase and needed *now*. Complete it inline and return to the phase (it inherits the phase's anchor — §How we work); document it in the phase doc as a Side Quest.

**Numbering is numeric at EVERY level — NEVER letter-suffix.** `24.1a` / `24.1b` is wrong. The scheme already gives you the next level down: *sub-dividing* step `24.1` yields **Tasks `24.1.1`, `24.1.2`, …** (not `24.1a/b`), and *inserting* between two existing items means the new one takes the integer/`.N` slot and **everything after it resequences** (a step between `1` and `2` becomes the new `2`; old `2`→`3`, …). Letters are never the answer — if you reach for `a`/`b`, you actually want either a deeper `.Task` number (decomposing) or a resequence (inserting).

## Inner Loop During Execute

**Stages 2→4 of the Phase Workflow, looped per step** — build the smallest real path, take one cheap observable, let the lead use it, repair. Stated once, there; not restated here. **Never mark a step complete until the lead confirms it — a green gate is not a confirmation.**

## Commit Cadence & Where Commits Land

**One repo, one commit.** Stage **explicit paths** — never `git add -A`, never a bare `git commit`. Read back with `git show --stat` and reconcile the file list against the edit you intended; the tree is shared with concurrent sessions by design. **Push stays lead-gated.** Full mechanics: `.claude/CLAUDE.md` §Git.

Code, planning, phase docs, research and learnings all commit here in the one repo. **There is no submodule cascade and no SHA bump** — any carried instruction about one is a no-op.

## Where a phase doc lives

**The folder tracks COMMITMENT, not status** — status lives in the doc's `Status:` line and in the Roadmap, and duplicating it in the folder tree is what makes the two disagree.

- **`Planning/Phases/Future/`** — phases the lead has **not numbered**: `PhaseTBD_<Name>.md`, however settled their position in the sequence.
- **`Planning/Phases/`** — phases the lead **has numbered**. Numbering *is* the commitment (§Phase Numbering), so the doc moves up when the number is assigned, **not** when work starts on it. A `SEEDED` numbered phase and an `ACTIVE` one therefore sit side by side, which is correct: the Roadmap says which is which.
- **`Planning/Phases/Complete/`** — closed phases, flat at the top since they may touch multiple components. Abandoned or stale plans go to `Planning/Phases/Complete/ignore/`.

*(This was two contradicting rules until a Wave exposed it: one said a doc lives in `Future/` "while seeded" and moves up at `ACTIVE`, another said `Future/` holds "not yet sequenced" plans under `PhaseTBD_*` names. Six numbered-but-seeded members satisfied neither. Tying the move to numbering resolves it and matches what numbering already means.)*

## Archive Location

Completed phase docs move to durable `Planning/Phases/Complete/`. Abandoned or stale plans live in `Planning/Phases/Complete/ignore/`. Phases land flat at the top of `Phases/Complete/` since they may touch multiple components. *(A project migrating from an older numbering scheme can keep the superseded docs in a clearly-named `Complete/` subfolder rather than renumbering them.)*

## Research Document Naming

Research docs (durable `docs/Planning/Research/`) are named **`YYMMDD_R_ConceptName.md`** — date-prefixed with the doc's **creation date** so the folder sorts chronologically (the order concepts entered the pipeline; phase docs already carry their own numeric order, research docs don't, so the date is what gives them one). A disposable-probe **result** doc adds a `_Spike_` marker: `YYMMDD_R_Spike_<Subject>.md`. The support dirs (`docs/Planning/Support/**`) are exempt. *(The short `_R_` form is the current convention; an older `YYMMDD_Research_*` form appears in some carried examples.)*
