**⛔ THIS IS THE HIGH-RIGOR LANE. ORDINARY WORK DOES NOT COME HERE.**

Ordinary work runs `/discovery` → `/execute`; the Brief's step list and build map are all the planning it needs. **This verb is for work whose failure is expensive or irreversible** — authorization · secrets · destructive migrations · data loss · the public edge. **If the Brief's `Risk lane` does not say `high-rigor`, you are in the wrong verb: say so and hand back to `/execute`.** A `build`-lane phase moves here only when the lead names it. *(Lead ruling, 2026-08-29.)*

**What this verb adds:** an explicit written plan before building · negative tests · the full gate set · a rollback-snapshot commit before execution (taken by `/execute`, `execute_highrigor.md` §1). It authors the plan, **appends it to the phase doc, commits, and stops.**

## Before you start

- **Prerequisite:** a Brief exists in the phase doc and names this lane.
- **The argument** is a phase (`17`, `43`) resolved to `docs/Planning/Phases/Phase<ARG>_*.md`, or an Issue (`#<n>`). Missing, but this session's own Brief routed exactly one unit here? Take it and say so in your first line. Otherwise ask. **No phase doc for the arg? Do NOT create one** — confirm with the lead whether it is a phase at all: a merge, reconciliation or branch-integration task is a `Support/Troubleshooting/` runbook driven by lead-gated git, not a phase. **Never number a new phase yourself** — numbering is the lead's (Workflow §Phase Numbering).
- **Issue mode (`/plan #<n>`)** — same discipline, lighter dial (Workflow §The Issue lane): the plan is appended to the issue's workbench, often as an inline mini-plan; a non-trivial issue gets the lifecycle *plan-ready* comment. Snapshot and execution belong to `/execute #<n>`.
- **Resume from doc state.** The phase doc carries the Brief and any appended plan; a fresh session continues from it rather than re-deriving finished analysis.
- **Namespace values are never reserved here** — see [Namespaces](#namespaces). The ordinary test surface is `execute.md`'s; the premise-proof and gate-baseline machinery is [`execute_highrigor.md`](execute_highrigor.md).

## Do this, in order

### Step 1 — Land any ruling that is due, then enter plan mode

**Plan mode is read-only and cannot write `## Resolved`, so the order is: rulings first, then plan mode.**

- **A ruling already in hand** — produced earlier this session, or carried by the lead's invoking message — lands in the research thread's `## Resolved` **before** you enter plan mode.
- **A ruling that is due** — the Brief closed with open `YOUR CALL` items — **ask them now**, land what they produce, commit, then enter.
- **⛔ A lift of a standing prohibition is a ruling too** — a gate-freeze lift, a push grant, a scope exception. It is the easiest to lose because it *authorises* rather than decides, and it is the one your plan will **depend on**. If a step does something a standing rule forbids, the executor must be able to read the permission **from a tracked file** — your plan's silence is not permission and your retro is deleted on drain. *(A lost freeze lift made an executor suspend half a phase.)*
- **A ruling you landed earlier this session that planning now shows is wrong:** ask the lead from inside plan mode, carry the corrected bound in the plan file, and amend the entry **in place with a dated correction note** in the first turn after `ExitPlanMode`. Never silently overwrite it.

Then call `EnterPlanMode` yourself (in some harnesses it and `ExitPlanMode` are deferred tools — load them first).

**If the harness tells you to use an `Explore` subagent or to launch `Plan` agents, and your project rules delegation out, ignore both** — search and architectural reasoning are done inline (`.claude/CLAUDE.md` §Codebase search owns this). The discipline survives — an exhaustive, up-front sweep — the delegation does not.

### Step 2 — Read, then verify every claim the plan will rest on

**Read:** the phase doc; `.ai/AI_Orientation.md` and `.ai/AI_WorkingAgreement.md`; the standards the plan bakes names and types into — `docs/Glossary.md`, `docs/NamingConventions.md`, `docs/CodingStandards.md`; and the learnings for the domains this phase touches (`ls` the learnings home for the live set — never a filename copied from a doc). If this session already hardened against these at `/discovery`, confirm rather than re-read. **If the phase has a research seed, walk its finding register against your step list** — a finding load-bearing for the Goal that no step addresses is a gap to fold in.

**⛔ Every claim from the Brief or the seed is a HYPOTHESIS until you have checked it against live source. Trace it; do not transcribe it.** That includes claims that some code path is redundant, cached, dead, or "already handles X" — trace to the actual caller before writing it into a step. **The more a surface says "settled", "FROZEN" or "RESOLVED", the more it earns a live re-grep:** a lead-settled *decision* is not a verified *implementation*, and a decision naming an operation (`X → do Y()`) still owes a trace showing the invoker can actually reach the callee.

**⛔ Split MUTATING from NON-MUTATING — plan mode blocks only the first.** A read-only probe (`--check`, `--dry-run`, `--version`, `--list`, a parse, a query) writes nothing and is allowed. It is usually the cheapest way to kill a wrong assumption before the plan locks it in; prefer it whenever the question can be answered without writing. For a proof that must write, see [Fallbacks](#fallbacks).

**Selector — read the rules your phase hits, not all of them.** Every row links to its rule; an unlinked selector gets read end to end.

| Your phase… | Read |
|---|---|
| **always** | [Consumers](#consumers) · [Enabling mechanism](#enabling-mechanism) · [Spec-answered decision](#spec-answered-decision) · [Accepted degradation](#accepted-degradation) |
| **doc-only / no build** | [Doc-only phase](#doc-only-phase) — skip the rest |
| touches **any dependency you did not write — including the framework the application IS** | [Dependency reachability](#dependency-reachability) · [Declared, not hoisted](#declared-not-hoisted) · [Cache replacing an authoritative path](#cache-replacing-an-authoritative-path) |
| **renames / moves / sweeps**, or **changes which hooks, events or channels fire** | [Greppable is not rewritable](#greppable-is-not-rewritable) · [Sweep completeness](#sweep-completeness) · [Changed meaning or channel](#changed-meaning-or-channel) · [Moving code](#moving-code) |
| adds or changes a **stored, exported or wire field** | [Every hop, both directions](#every-hop-both-directions) · [Spike fidelity](#spike-fidelity) |
| adds a **new variant** to a registered family (a model, a block, a role, a handler, a codec) | [Registration](#registration) |
| adds **detection / classification / recovery** logic | [Design the logic](#design-the-logic) · [Failure injection](#failure-injection) |
| **fixes a bug** | [Sibling defect](#sibling-defect) · [Failure injection](#failure-injection) |
| claims something **does or doesn't exist in the world** | [Absence and presence](#absence-and-presence) · [Old data](#old-data) · [Doc pointers](#doc-pointers) |
| **widens a property an existing gate asserts over** — a closed set, enum, role list, allowlist, id registry | [Gates by symbol](#gates-by-symbol) · [Retiring a gate](#retiring-a-gate) |
| adds a **UI control** or a multi-instance case | [UI controls](#ui-controls) · [Multi-instance](#multi-instance) |

#### Doc-only phase
Skip the code battery. The verify surface is link and path-ref resolution · structural grep guards · offline format validation · contract versioning. `CodingStandards.md` is N/A; naming, no-duplication and versioning still bite.

#### Consumers
Every behavioural consumer the Brief's verification set names — a reader, a caller, a hook — gets a step, or an explicit "no edit, because…". A named consumer with no step is a plan hole.

#### Enabling mechanism
A plan that asserts a mechanism will *work* — a schema a validator must accept, "same shape as sibling X", a named fixture or tool, a test target's reachability — proves it against live reality before locking it: run the construct through the real validator, `ls` the named file, name the seam each planned test drives and confirm it is drivable without a live service. **Presence in a type, a comment or a sibling test file is not behavioural proof** — a sibling test proves the harness exists, not that your target is reachable. Prefer a project-owned fixture over vendor sample content. A seam that needs a source change to reach is a planned step with its own cost.

#### Spec-answered decision
Before forking a decision to the lead or carrying it as "open", read the durable spec and the cited issue body. A decision the spec already settles is not a fork.

#### Accepted degradation
A plan that prices a cost — *"we accept X; it is NOT a NO-GO trigger"* — names how X was **observed**, or marks it `UNOBSERVED`. An unmeasured accepted cost is lead-visible and authoritative in tone, so re-opening it later reads as re-litigating; it shields the defect for the whole phase. Cheapest discharge: observe it once, at the worst input the phase claims to support.

#### Dependency reachability
For anything whose source you do not own — **including the framework the application is built on, which feels neither external nor foreign and is exactly where this gets skipped** — the check is reachability through the surface you will actually call, not existence:
- **A symbol in a type declaration is not a public export** — grep the package's entry point, not only the type file.
- **"Already used in this codebase" is evidence about a consumer, not a mechanism.** Name what *kind* of thing consumes it there and in your step — component vs route handler, build-time vs request-time, server vs client. If the kinds differ, the citation proves nothing.
- **Measure the artifact you will run** — the pinned tag, not `main`; the image you ship, not a sibling's; the tool inside the container, not on the host. The tell is that the measurement was real, so it does not feel like an assumption. *(One phase hit all three: a config key renamed between `main` and the pinned tag, a `wget` healthcheck on an image shipping only `curl`, a reassuring `|| echo` from a `pgrep` that was not installed.)*
- **Check the axis that bites:** runtime-settable vs build-time only, reachable through this object type or only another.
- **Same check for in-tree wrappers and services the fix routes through** — a Brief's "N touch points" is a floor to verify, not a ceiling.

#### Declared, not hoisted
A package pulled in transitively imports cleanly and is invisible to any supply-chain gate that checks what the project **declares**. If you reach for a symbol, confirm the package is declared — otherwise write the few lines against the standard library.

#### Cache replacing an authoritative path
A cache or index that replaces an authoritative read pins (i) every write path that must invalidate it and (ii) its first consumer. With no live consumer it is scaffolding — co-locate it with the consumer's step, and tag deferred work `re-validate-need-at-<step>`; by then the authoritative path may already serve it.

#### Greppable is not rewritable
For any rename or move, say how each site is rewritten, and flag **generated or binary** sites a text sweep must not touch and a regeneration must — generated types, generated import maps, schema snapshots, serialized assets. Counting occurrences does not prove a change is mechanical.

#### Sweep completeness
A sweep, rename or drive-to-zero is only as good as its population. Grep the old token across **the test, fixture, seeder and gate trees, not just `src/`**, and make the exit audit cover the same file set.

#### Changed meaning or channel
A step that changes an existing function's *meaning*, or **which of N hooks, events or callbacks fire**, enumerates every caller **and every binder** — the shape is N channels × M consumers each binding a subset, so dropping one channel breaks whoever binds only that one. Routing a caller to a different existing function also confirms the return and parameter shapes match, or names the consumer refactor.

#### Moving code
Moving an operation out of a function: read **all** of it and name what stays — a line-range move silently drops an entangled concern. Moving between modules: state which may import which, and cut the move and its consumers over together; a shim that inverts the dependency arrow is impossible as written. Moving an operation to another layer: check the conventions already applied there (units, transforms, coordinate or value conventions), so nothing is applied twice.

#### Every hop, both directions
A stored, exported or wire field crosses **every** hop in **both** directions — producer → each serialization boundary → transport → decode → every consumer branch that reads it. The encode side is the one that silently drops a field. List the hops in the step. State whether the change is **internal** or **changes a versioned format or protocol** (its own version bump), and register a new persisted field in the round-trip gate if the project has one. Pin the contract's *semantics*, and let execute pick the minimal call.

#### Spike fidelity
If discovery proved a mechanism with a spike, the plan pins **that** mechanism as the contract, with the conditions it was measured under as step preconditions. A different form owes its own live validation, and a "precondition CONFIRMED" on a never-run path says whether it was traced or exercised.

#### Registration
A new variant of a registered family — a model in the framework config, an editor block, a role in the capability tables, a handler in a dispatch table — is incomplete until you trace **the table that selects it**, and confirm the identity you chose resolves to it. A complete per-variant chain that nothing routes to is still dead.

#### Design the logic
A step that detects, classifies or recovers state pseudo-codes the decision ladder, or names every discriminator and the negative-control cases. "Compose from existing readers X and Y" is a materials list, not a design.

#### Failure injection
For each planned failure test, confirm the cited function really **throws** on the injected input — a real `throw`, not a swallowed catch or a best-effort `return {}`. A non-throwing stage is not a testable strand point.

#### Sibling defect
A defect of the same class on the same code path as the fix comes into scope; fixing the first only moves the failure to the second. A separate defect on a different path defers.

#### Absence and presence
"Create / add, because absent": re-verify the absence live — a parallel stream may already have built it. A precondition naming a concrete existing fixture or record: `ls` it; if it has moved, name the restore source.

#### Old data
**⛔ Backward-compat, a migration, a dual-read or a fallback for OLD data is a data-existence claim — confirm with the lead that the old data exists before designing for it** (`AI_WorkingAgreement.md` §Confirm the Precondition Before Building for It). When two or more review blockers trace to one assumed precondition, ask a yes/no on the precondition rather than hardening the mechanism.

#### Doc pointers
Resolve each retargeted pointer to its own live target; never batch N pointers to one assumed target.

#### Gates by symbol
**Name the gates you will amend by the symbol they assert over, not by the files your steps edit** — grep the gate scripts for the property you are widening, then also grep **the route** it governs and **the rule's plain words**, because a gate asserting over HTTP imports none of your symbols. `execute_highrigor.md` §2 owns the rule; it is here because the plan is where the inventory is fixed and the lead approves it.

#### Retiring a gate
Retiring, folding or weakening a gate is a coverage claim: read that gate first and preserve its trigger and pass criteria, or justify the weaker coverage explicitly.

#### UI controls
A UI control that drives a rendered object traces both the persist path (write → reload) and the **live** re-apply path, and its proof shows the visible effect changing live — "persists" is not "works". If no gate renders that UI, name the browser probe or say the surface is owed to the sitting.

#### Multi-instance
Acceptance over two or more instances of one type is not covered by a single-instance proof. Trace what the real producer emits for the second (name collisions, shared vs copied state), and build the fixture from real output, not a hand-made clone.

### Step 3 — Author the plan

**Write it in the harness plan file, never the phase doc, headed `# Implementation Plan — <Phase>`** (step 5's append anchors on that heading). It contains:

- **Context** — the problem, why now, the intended outcome.
- **The recommended approach only** — a rejected option becomes a *why-not* note, never a live alternative.
- **Exact files and functions** — full paths, no ellipsis, existing utilities reused and cited. Trace the real routes and cite lines.
- **Deliberate behaviour changes.**
- **`## Acceptance invariants`** — every phrase in the Goal carrying an **absolute quantifier** (*"no deferrals" · "every" · "all" · "only" · "anyone" · "never"*) quoted **verbatim**. This is what makes `execute_close.md` row `A0` mechanical rather than self-scored.
- **A scope-coverage table** — see [Scope coverage](#scope-coverage).
- **An Execution access check** — see [Access check](#access-check).
- **Verification** — how each claim is tested end to end, and for **every gate, `runs-in:`** the workflow file and step, or the literal `local-only`. An invariant containing "in CI" or "on every push" names its workflow step.

#### Scope coverage
**Enumerate `## Scope` In line by line and name the step that discharges each** — including explicit scope-outs; silence is what fails. Then, the moment you author it:
- **Re-read each mapped step's text against its line's cardinality.** The table proves each line *has* a step, not that the step *delivers* it: "four axes", "both directions", "every entry path" must appear in the step **item for item**. The same holds for a step implementing a multi-clause `Resolved` decision — enumerate its sub-rules into the step, never its headline.
- **Map every fixture a verification clause names to a step that creates or modifies it.** A gate asserting against a fixture no step touches passes vacuously.
- **A ruling that changes `## Scope` mid-plan invalidates the table — re-run it, do not patch it.**

#### Namespaces
**⛔ Never pre-assign a value from a centrally-allocated namespace** — gate ids, entity id prefixes, migration ordinals, version constants, port assignments (`LOCAL_DELTAS.md` lists your project's). Two concurrent phases both compute "next free" and collide. **Enumerate which axes the phase touches; name each thing by what it asserts; the executor claims the value.** Where a registry is updated by a late step of its owning phase it lags by design: its high-water is a floor — grep the **active phase docs** for higher claims.

#### Access model
**If the plan adds or changes an access policy or capability set, re-read every later step as a caller subject to it.** A step whose gate creates, deletes, publishes or reads across scope may be forbidden by a decision earlier in the same plan — both halves read correctly in isolation, and the step turns out unwritable at execute.

#### Access check
**⛔ Mandatory whenever the phase's gates run in CI.** The lead is present now and may be absent at execute, and a scoped grant written here is what lets an unattended executor run at all. List:
- **Every outward-facing or out-of-tree action, with its scope and expected volume** — *"`git push`, scoped to the RED→GREEN demonstrations; expect several"*. **An action not listed is not granted.**
- **⛔ Vendor control-plane writes** — a network ACL, a DNS zone, a repository or account setting — can remove the access path the executor is standing on. Name each one's scope **and the fallback access path that stays open while it lands.**
- Environment invariants that hold for **every** step of a kind — stated once, not per step, or a resume that skips that step dies on them.
- Every named gate command, verified to exist (one `ls`).
- A pinned tool version, to be diffed at execute against what is installed and **in use** — a mismatch is a question, never an install.
- One-off tooling approvals (a novel binary, a network install), which are not `⚠human` steps.

A `⚠human` step that turns out to be automatable needs a capability this table cannot contain — that is a one-off ask at the moment of discovery, not a plan violation.

#### Ownership
**⛔ Every step must name only files this phase owns.** A durable spec this phase changes is yours. **An upstream decision record is not** — the research thread's `## Resolved`, the product overview, a sibling phase doc, a central registry — because the lanes that write them run concurrently with execution by design. **A step that needs one becomes a numbered `⛔ YOUR CALL` naming the rulings owed, with your recommendation.** This is what lets research on future phases proceed without stopping execution of planned ones.

#### Fallbacks
When a proof must *write*, plan mode cannot run it:
1. Confirm **presence** read-only.
2. Route the behavioural proof to a **named first sub-step** of the step that depends on it.
3. Pre-authorize a fallback **only if it ships the same product and UX** — one that changes the shipped design or the user's workflow halts and returns to review.

**Every named fallback states what it costs that the primary does not** — a new secret, a new authenticated consumer, a network hop. Also check the fork's shape: the real question is often a third thing neither branch names. *(A "local API or REST" fork was really "where does the build run", and the fallback silently needed a standing service credential.)* A prior phase having used a mechanism is presence evidence if its invocation was thrown away; **a committed, previously-run harness is behavioural evidence**, and can downgrade a `⚠human` step to autonomous.

#### Gates
- **One gate per hunk of human-testable outcome — one or two per phase.** If the Brief handed you more, cut them here; never invent a gate-authoring step. **Size a gate-authoring step as authoring plus a repair cycle** — its first run is the first instrument ever pointed at this phase's earlier work, and its reds are disproportionately yours.
- **A gate's observable must be producible by its method.** A visual sitting proves presence and visible effect, not an internal invariant. A parity gate compares semantically (type + value), not byte-for-byte, unless byte stability is the contract.
- **A named RED-demo mechanic is `mechanic unverified`** unless you measured it during planning; one that turns out not to exist is an ordinary ⭐ divergence at execute, not a plan violation.
- **A measurement whose outcome is really a lead call** is tagged `measurement-OR-lead-decision`: the close is satisfied by the number or a recorded ruling that waives it. Offer the lead the decision before building a heavy measurement.

#### Tags
Tag every step on each axis — they are independent:
- **Sequencing — `shippable` or `WIP-only`**: whether it lands in a state safe to suspend on. This is the executor's safe-pause map.
- **⛔ Blast radius — `[reversible]` or `[⛔ can take a public surface down]`.** **A step containing both kinds of edit is split**, because they have different suspend rules. Size a step whose deliverable is *proof* by its assertions, not its diff.
- **Gate class — two axes, and only the second is portable: (a) who validates** (CI / a local tool / doc-only — the tag *names* are per-project and recorded in `LOCAL_DELTAS.md`), **(b) `⚠human`** for any step needing a person at the machine. The human axis is the load-bearing one: it gives the phase its shape (*"ten steps, all autonomous"*) so the executor front-loads the autonomous batch and the lead schedules one sitting. **A `⚠human` inherited from a prior run or a Wave note is a hypothesis — verify it read-only**; over-tagging books sittings the phase does not need.
- **`[spec-edit: capture-at-close]`** on every step that edits a durable spec (`docs/` outside `Planning/`) — run this as its **own pass**, because spec edits look like ordinary documentation and get tagged doc-only instead. The edit is captured during execution and applied at close. **⛔ A `## Resolved` entry is upstream, never a derived doc, and this tag never applies to it** (`AI_WorkingAgreement.md` §A Derived Document Reflects Decisions).
- **`guards: <artifact>`** on a test that pins a config artifact (an allowlist, a proxy config, a flag file), so a later step changing the artifact inherits the guard.
- **`validated-at: <step>`** where a step's behaviour is validated by a test authored later, so a green gate here reads as regression guard, not validation. Give a gate with a hidden cost (a multi-hour rebuild) its own step.
- **Granularity:** an "all N surfaces" step with per-item work is sub-numbered (`24.1.1`) or tagged `[multi-item — decompose at execute]`; a cluster that cannot commit green midway is tagged `[no-mid-commit cluster]`. Pre-flag a change that ripples broadly through fixtures or snapshots, so the churn is budgeted rather than read as regression. A step that **settles a value a later step freezes** names the value.

#### Sittings
A `⚠human` step must pass both reachability tests:
1. **The verdict is reachable through the app UI** — never by the lead hand-typing console commands.
2. **⛔ The human can get there.** Name the URL and confirm it is open today, **resolving from the hostname down**: start at the edge config and follow it inward. A bind address, a port publish or a firewall rule is evidence about one hop and **can never establish that a path is closed** — a reverse proxy reaches a container by service name. A control a sibling phase shipped on purpose (an edge deny-rule, an ops boundary) is the specific hazard; where the closed path was a lead ruling, record and route the conflict, never resolve it.

Before booking a sitting:
- **Prefer a headless seam** for a *mechanism* question — a pre-fix RED demo is a cheaper, permanent premise proof — but keep a live marker of *delivery* if the sitting later becomes the gate of record.
- **Name a visual discriminator** where pass and fail would look alike, and a known-good control on the same fixture.
- **Confirm the sitting's preconditions are wired** — the instance it needs can be created, not a stub.
- **Tag `[verdict-by-headless]`** a step with no visible delta, so it is not booked as a wasted sitting.

#### Decisions
**⛔ A plan lands with every decision made.** A question only the lead can answer is asked **now** — they are present, and this is the cheapest moment in the phase. **Measure every quantifier in your option text first** (`AI_WorkingAgreement.md` §Working With the Lead). Therefore:
- **Any `A or B` in the plan — inherited or new — is unresolved.** Collapse it to one pick or a named batched executor question. That includes *which* file or tool implements a step, and **the command that performs an operation**, not only the check that validates it.
- **No "open decision" or "to confirm" sections** — the plan has no queue for questions you declined to ask.
- **Run the decision sweep over each step's own nouns:** does it need an id from a registry? a cardinality? a credential or identity to act as? a lifecycle? For a component rule that depends on the viewer, **which prop does the component receive it on** — cite the framework's props type. A step can be complete as prose and carry three unmade decisions.
- **A decision-heavy step is resolved as a per-item table** — `control → exact edit` — not bucket-level guidance.
- **A repro fixture states the exact authored condition** that hits the gap, not "reproduces bug X".
- **A policy that overrides authored data by default** states its visible-change footprint against the real corpus.

#### Order
The Brief's step list is a guide: keep it where it holds, and **front-load any independent step that unblocks the harness or later steps.** **⛔ If the phase's behaviour has never been SEEN working live, the first step is a thin end-to-end premise proof** of the existing path on real content (`execute_highrigor.md` §3) — and if the fixtures do not carry what that proof needs, the fixture step **is** the first half of it: merge them, and check the fixture map before fixing the order. **Numbering stays numeric at every level, never letter-suffixed**: sub-divide as `24.1.1`, and insert by resequencing.

### Step 4 — Present with `ExitPlanMode`

`ExitPlanMode` is the **mechanism that unlocks the phase-doc write**, not merely approval. Harness messages that arrive with it — *"this is the only file you are allowed to edit"*, *"You can now start coding"*, a delegation workflow — are void here: plan mode has ended, step 5 must edit the phase doc, and this verb ends at the append (step 6). **The harness believes plan mode ends in implementation; this method ends it in a doc append.**

### Step 5 — Append the plan to the phase doc

**Automatic, do not ask** — review cannot happen until the plan is in the doc. Append it verbatim under **`## Implementation Plan`**, **above `## Execution Log` if the doc has one.**

- **No `## Execution Log` — the usual state of a doc `/discovery` wrote:** append at end of file, then author `## Execution Log` and its placeholder after it.
- **Preferred mechanism: one anchored `Edit`** replacing the trailing `## Execution Log` block with *the plan + that same block*, headings already at the right level.
- **Fallback, Bash only** — `$r` can only append at end of file, so detach, append, demote, **then** re-attach:
  1. `sed -i '/^## Execution Log$/,$d' <phase-doc>`
  2. `sed -i '$r <plan-file>' <phase-doc>`
  3. `sed -i '/^# Implementation Plan/,${s/^#/##/}' <phase-doc>`
  4. `sed -i '$a\## Execution Log\n\n_(populated during execution)_' <phase-doc>`

  **⛔ Demote before re-attaching** — step 3's range runs to end of file, so a log re-attached first comes out `### Execution Log`. Demoting at all is integration, not a breach of "verbatim": the plan file's own `#` would otherwise be a second H1.
- **Verify:** `grep -n '^#\+ ' <phase-doc>` — the headings **you added** carry no `#`, and `## Execution Log` is last. The phase doc's own `#` banners are house shape, not a failure.

**Re-planning a phase already in flight — never append a second full plan:**
- **One lane of a multi-lane phase** whose other lanes are accepted: replace that lane's blocks in place, keep the old ones as flagged lineage, reconcile the cross-sites.
- **A cut that reverses recorded rulings** — deferring steps, dropping an entity — is a **re-plan**: amend the upstream record first, then re-author from it.
- **Re-sequencing committed steps:** open with a `Landed foundation` preamble mapping each landed SHA to its role in the new order.
- **Net-new work folded in:** a dated `## <Name> Plan` section, with a ⚠ pointer on each step it supersedes.

**Reconcile in the same pass — by grepping, never by re-reading what you wrote.** One `grep -n '<Q-id>'` per resolved decision finds every site still saying "open": the Status line · Scope · the Brief's verification set · any co-owning Wave doc named in the header. **Replace the Brief's step list and build map bodies with a one-line `⚠ Superseded — Implementation Plan governs`**, keeping the heading. A multi-line block that is hard to copy exactly is deleted with a range anchored on unique text at both ends: `sed -i '/^<first line>/,/^<last line>$/d' <file>`, or up to but excluding a line that must survive: `sed -i '/^<start>/,/^<keep>/{/^<keep>/!d}' <file>`.

**After any change to the plan — a step inserted, deleted or renumbered, a helper renamed, a design revised — run ONE whole-doc grep of the full supersede list:** old step numbers, old symbols, and **aggregate claims with no number in them** (*"all four"*, *"both gates"*, *"Nth of M"*). A helper with no remaining caller is dead code shipped into execute. A "leave / out of scope" disposition goes into the exit gate's keep-list in the same pass. The scratch plan file is **not** a reconcile target: once appended, the phase doc is the single source of truth.

**Then self-grep what you wrote for steering language** — `ready for`, `next verb`, `/execute`, `cleared to`, `gated for` (full list in `discovery.md`). The Status edit is where it creeps back in.

### Step 6 — Stop, commit, hand off

**Do not start coding.** The harness's "start coding" message does not apply. The plan's status is **`PLAN DRAFTED`**. **Commit the phase doc explicit-path** — a landed plan must not live only in a dirty tree — then say the command is complete. If the session is context-heavy, recommend a fresh session for `/execute`; the phase doc carries the state.

The rollback snapshot, the gate baseline and all execution belong to `/execute` (`execute_highrigor.md`). The close ceremony does not apply to a plan commit.

## Hard rule

Between invoking this command and the committed append, **edits to the plan file and the phase doc are allowed; edits to source, builds, deploys and execution scaffolding are not.** If unsure whether an action counts as execution, ask.
