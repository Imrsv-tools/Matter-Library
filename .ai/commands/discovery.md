Discovery for a phase — front-loads everything the session needs in one call. **Its deliverable is the Brief: stage 1 of the Phase Workflow.**

## ⛔ HARD RULE — read before anything else

**Discovery gathers, structures and COMPILES. It does not edit source and it does not build.**

Discovery is a **conversation that compiles**, not a transcript that accumulates. Its whole job is to make execution focused — so the executor never has to re-read the research corpus or replay the lead conversation. It is finished when the Brief below can be written, and **not when everything knowable has been written down.**

- **⛔ A lead instruction to "finish it / do it now / no more deferrals" changes the PACE and the SCOPE — it never changes the VERB.** The correct response is to hand to `/execute`, faster. It is not authorization to edit source. If the lead genuinely wants code now, **they must name the verb** — say so and let them choose.
- **⛔ Discovery does not edit the METHODOLOGY.** `.ai/commands/**`, `Methodology/**`, `AGENTS.md`, `.claude/CLAUDE.md`, `AI_Orientation.md` and `AI_WorkingAgreement.md` are the Workflow Refiner's lane and are read-only to you. Friction with a command is a `/retro` item — **adapt in the moment, keep going, file it at handback.** A stale sentence three docs away is not your errand. *(Unless the lead asks directly — then say it was lead-directed.)*

**Ordinary work goes `/discovery` → `/execute`.** There is no separate planning stage: the step list and the compact build map are part of the Brief. **[`plan.md`](plan.md) is the HIGH-RIGOR lane only** — authorization · secrets · destructive migrations · data loss · the public edge.

The argument is the phase doc — a path or an identifier resolved to `Planning/Phases/Phase<ARG>_*.md` — or an Issue (`#<n>`).

**⛔ AN ARGUMENT NAMING A NUMBER NO PHASE CARRIES IS THE LEAD NUMBERING THE NEXT PHASE.** Phases are not numbered until the lead numbers them, so the lead typing a number for an entry that has none **is the numbering act**. Resolve it to the entry at the head of the Roadmap's `## Future` — position in the list is the order — seed under that number, and **say which entry you took it to mean.** Ask only when two are genuinely equally next.

---

## Cold start — do this

1. **⛔ IS THERE NO PHASE DOC AT `Phases/Phase<N>_*.md` — WHATEVER THE ROADMAP ENTRY'S STATUS WORD SAYS? Then this invocation SEEDS and STOPS.** ⚠ **Key this on the ARTIFACT, never on the status word**, which is routinely wrong: a journey split out of another phase is seeded in **that phase's `## Deferred` table**, not in a doc of its own, and the Roadmap may already call it `SEEDED` — the vocabulary defines `SEEDED` as *"phase doc written"*, which is then false. **It is not seeded; write the doc.** *(One narrowing produced FIVE such entries in a day. Two consecutive discoveries hit the identical mis-keyed condition, both had to reason from the rule's spirit, and both reached the right answer via an exception written for a different status.)* The rule as originally written keyed on `RESEARCH`, and read literally it does not fire on the case that actually arrives. Seeding is not discovering. Write the phase doc — `Status: SEED`, its `Outcome`, scope in/not-now, and the seed-vs-docs question list — and **nothing else**. Touch no document outside the phase doc and its Roadmap entry. **⇒ The one exception is the lead opening it in the same breath:** an invocation that both names a phase to seed *and* asks for discovery to start is the deliberate opening this rule waits for. **The stop is a TURN boundary, not a session boundary.** Land the seed as its own commit, say you read the invocation as opening Pass 1, then run Pass 1 in the next turn without waiting to be asked again. **⛔ Seeding a phase that is NOT the active one is a legitimate invocation** — it writes one doc and one Roadmap line and starts nothing.
2. **Announce the tree.** Run `git status -sb`. Any file you did not touch means another session is live here; say so before doing anything else.
3. **Otherwise the doc is seeded:** assess it, flip `Status:`, and propose Pass 1's focus.

---

## Read — front-loaded, because this is where discovery earns its cost

1. **The phase doc itself** — the seed: the thinking captured so far, often a raw dump from prior sessions.
2. **⛔ PASS 1 = THE PLATFORM-DOCS REVIEW — an active survey, not a checklist read.** Start from *what the app IS* (the product-model / overview doc) and work **down** to the surfaces this phase touches. **Anchor it to the phase's `Outcome`** — you are reading to learn *how the app delivers THIS outcome*. **If the phase has no `Outcome` yet, writing it is discovery's first act.** Top-down is deliberate: it guarantees the foundational framing is hit even when the seed is narrow, and a surface-only read misses exactly the framing that matters. **The platform docs are TRUTH and the seed is context** — a disagreement becomes an explicit thread, never a silent override. Skipping this is a documented route into a day-long derail: a narrow phase whose seed contradicts the product model is the signature failure, and the conflict list is what surfaces it in pass 1 instead of at a day-six smoke.
3. **The project's own prior research and spike docs** — list `docs/Planning/Research/` and read every file whose subject touches this phase.
4. **Orientation baseline** — `.ai/AI_Orientation.md`, `.ai/AI_WorkingAgreement.md`, the Documentation Map.
5. **Domain learnings — AT DISCOVERY, not later.** Identify the domains the phase touches and force-read their `docs/Learnings/` entries. Discovery is exactly where a costly-to-rediscover invariant pays off; reconstructing it from code is wasted passes. **⚠ AND IF THE PHASE TOUCHES NONE OF THEM, SAY SO IN ONE LINE AND MOVE ON — that is a discharged read, not a skipped one.** The learnings domains reflect what has *hurt* so far, which skews toward infrastructure; a phase that touches no toolchain, no container and no framework collection legitimately has no entry to read. **Do not perform a listing you did not use** — a read recorded as done and not done is worse than an honest skip, and it teaches the next run that the whole block is ceremony. *(Two consecutive discoveries on the same user-facing surface listed every learnings file and read none, for the identical and correct reason.)*
6. **⛔ GREP THE TREE FOR THIS PHASE'S OWN NAME.** Committed code is a third source of routed work, and every other read in this block is a *document*. A prior phase may already have built, deferred or half-built what you are about to scope.
7. **Conditional** — `NamingConventions.md` + `CodingStandards.md` if the phase touches naming or vocabulary; the external system's own docs when the defect is in a framework's behaviour rather than ours.

---

## The Brief — the deliverable

One page in the phase doc. When this can be written honestly, discovery is done.

- **`Outcome`** — one sentence: what a **person can DO**. Plain, non-technical. Never tech for its own sake; always challenge *"is there a user-facing result?"*
- **First human test** — the **exact click path**, and the URL it will live at. Written before any code, because it is what `/execute` hands the lead.
- **In now / not now.**
- **⛔ The reuse check — one question, and it is the primary one:** *What does the selected stack already provide, and which standards are materially implicated by this change?* **Reuse is primary. Conformance is targeted to the contracts actually touched** — the full standards sweep belongs to the high-rigor lane or a final cross-system review, not here. Every custom layer the phase proposes must name the native behaviour it replaces and the gap that justified it; *"we may eventually need more control"* is not a gap.
- **Decisions that bind** — pulled from research and prior phases, **one authoritative copy**.
- **Risk lane** — `build` (default) or `high-rigor`, **with the reason named AND VERIFIED AGAINST THE TREE.** ⛔ **Name the specific control you believe you are or are not touching, and READ IT.** *"It resembles a phase that was high-rigor"* and *"it touches the same subsystem"* are hypotheses; the file implementing the control is the answer. **Both errors are expensive and neither is visible from the Brief** — wrongly `high-rigor` sends a static-file phase through `/plan`; wrongly `build` walks a real security amendment past the lane that exists to catch it. ⚠ **And the default is `build`, so an unverified reason fails toward the CHEAPER lane** — the wrong direction for the one decision that exists to catch expensive mistakes. *(A phase publishing four new URLs on the public edge looked like a sibling marked high-rigor for amending an edge control. Reading `edge.ts` settled it in minutes: the allowlist governs **proxied** paths and a publication host has no upstream at all — search needs one, a feed is a file. The same read also produced a build-map fact the Brief needed. **A lane check done properly pays twice.**)*
- **Step list** — the short sequence of **vertical** steps, first clickable path first, numbered `Phase.Step` (`19.1`, `19.2`, …). **This IS the phase's step sequence**; there is no separate skeleton stage. Ordering plus a one-line intent per step — no route-tracing. ⛔ **Vertical is the whole constraint: a step is something a person can USE, never a layer with no user path** (`AgenticEngineering_Workflow.md` §Phase / Step / Task Terminology, which also owns numbering — **numeric at every level, never `19.2a`**). **⛔ RECONCILE IT AGAINST THE FIRST HUMAN TEST, CLICK BY CLICK, BEFORE YOU SHIP THE BRIEF.** Every click that test names must be reachable by the step whose *"first clickable result"* claims it. If the test's third click needs step 2, then either the test is smaller or step 1 is bigger — **say which, in the Brief.** *(One Brief gave step 1 a test whose third click was "click through to page 2 and back" while making pagination step 2 — and its own §Native starting point said not to hand-roll a pager, so building step 1 alone was strictly MORE work than building both. The executor had to merge them mid-run and defend it, against a doc that had already made the call wrong in two directions.)*
- **Compact build map** — known seams, likely files, step ordering. Enough for a handoff. **Not an exhaustive implementation plan.**

**⛔ SPLIT TRIGGERS — and phase-doc length is NOT one of them.** Split when **more than one independently demonstrable journey** is in scope · the **active execution packet has become unscannable** · **time-to-first-click would exceed 60–90 minutes**. A provenance appendix may legitimately add length. **Surface a split signal early; cut LAST, on the full picture** — premature splitting on a partial picture forces a re-unification cycle when the coupling surfaces.

**⛔ A DEFERRAL ROW STATES WHAT THE DEFERRED JOURNEY WILL *CONSUME* FROM THIS PHASE** — the URLs it links to, the components it renders through, the types it reads. **"Independently demonstrable" is a test about the DEMO, not about the code:** two journeys can pass it and still share a URL shape and a template. ⛔ **A row claiming "no dependency" without naming what it consumes is a HYPOTHESIS, and the receiving discovery must seed it as a question under test rather than accept it.** *(One row read "one journey, no dependency on the rest." It was false twice over — the journey linked to a URL shape the parent phase owed and had **not ruled**, with that phase's own Brief warning "an executor may not invent it", and it rendered through a shared component the parent was mid-way through writing. The receiving discovery got the Brief right only by distrusting its source doc.)*

---

## Discovery discipline

**⛔ DISTIL, DO NOT APPEND — this is the rule that keeps the doc usable.** A pass ends by **rewriting the current synthesis**, never by appending another pass beneath a stale one. Superseded hypotheses compress to one sentence where the rejection matters; otherwise git owns them. Sources are pointers, not copied blocks of prose. Repeated statements become one authoritative section.

**Supersession hygiene — state each decision ONCE and mark superseded text in place.** ⛔ **A lead decision that resolves an open fork or drops a scope item IS a supersession event** — sweep the doc for every restatement of the old position in the same turn. **Make the sweep mechanical:** grep for the terms, do not do it from memory. Two runs missed sites doing it from memory. ⛔ **Anything that breaks a grep is a defect** — no soft hyphens, non-breaking spaces or smart quotes inside identifiers.

**⛔ Record a lead ruling in the LEAD'S OWN WORDS.** When a ruling arrives carrying its own reasoning, structure or refusals, quote it rather than paraphrasing — a paraphrase silently drops the half you did not think was load-bearing.

**Reseed, don't patch, on a core-framing FLIP.** Supersession hygiene is for decisions inside a stable frame. When the phase's central framing changes, rewrite the doc.

**The seed is context, not authority.** Audit it against the live tree; live reality wins. **Carry-forwards decay:** any seeded `file:line`, count, or "already named X" from a prior session is **dated — re-verify before citing it.** A negative result from a path-scoped search proves absence only within that scope.

**⛔ AND A FINDING ABOUT ANOTHER UNIT'S CODE DECAYS IN MINUTES, NOT SESSIONS, WHENEVER A SIBLING VERB IS LIVE ON IT** — which on this project is the normal operating mode, not an edge case. **Verifying it when you write it is not enough: the claim can be true when measured, soundly measured, and false by the time you commit.** Re-check any cross-unit claim **immediately before the commit that carries it**, and treat the pre-stage `git status` as that check rather than as bookkeeping. *(A hand-back's headline finding about a sibling's dirty-marker set was verified against committed code and staged; a routine `git status -s` showed the sibling editing those exact two files at that moment — they were fixing precisely it. Nothing about "verify before you assert" would have helped: the verification had been done.)*

⛔ **AND THE MOST PERISHABLE KIND IS THE ONE YOU HAVE NOT WRITTEN DOWN — the decay window opens when you FORM the claim, not when you stage it.** A cross-unit conclusion held only in the run's head has no diff to re-check and no reviewer. **Write it down or drop it; do not carry it.** *(A discovery held "the sitemap must not list `/` — the root is a `noindex` placeholder", correctly verified against the page's own source. By the time `/retro` step 0 forced it onto disk, a sibling phase had landed and the root read `index, follow`. The phase doc would have shipped the false claim; what caught it was being made to write it down.)*

**Read the durable SPECS — don't reverse-engineer the code.** Spec-driven development is nominal if every "what's the contract?" question is answered by reading code. Reconcile spec-vs-code and log staleness as a finding. ⛔ **But before logging a doc as owing a correction, ask which direction the error runs — N derived docs agreeing against one plain-language contract is usually one claim copied N times.**

**Enumerate the PEER SURFACES before recording any scope decision — the outlier is the defect, not the specification.** If the target is the only surface behaving that way, **that IS the defect**: a component exposing a channel nobody bound is an omission, never a scoping choice.

**⛔ A CAPABILITY claim ("feature X works") is a FOUR-POINT claim** — producer, consumer, the wire between them, and the entry path a person uses. Both-ends verification covers two of the four and **passes while the feature is unreachable**. ⛔ **And a capability probe runs against THIS PROJECT'S artifact, never only against the tool** — *"the tool exists and supports `--y`"* is not evidence our build does. ⛔ **AND WHERE THE PHASE ADDS URLs, THE FOURTH POINT INCLUDES THE ROUTE TABLE IT IS JOINING — enumerate the routes that already match the shape you are about to recommend, before you recommend it.** A framework resolving two candidates for one path is a build error, not a preference. *(A Brief probed its framework's content loader properly, against the installed artifact, and then recommended "one dynamic route over the collection, not five files" — at a path where an existing dynamic route already owned the same single-segment shape for every published article. The collision was recorded in that same Brief's own findings two sections away and never connected to the route-shape recommendation; execute had to overturn it in the first step and ship five static routes.)*

**"Confirmed" requires the confirming artifact in hand.** A finding is Confirmed only when its named artifact exists and you have read it. This governs architecture verdicts too, not just forensics.

**Don't rush to a plan.** Gather and structure; resist forming an approach until the picture is visible.

### Forking to the lead

**⛔ FIRST — is this even YOUR fork?** When lead-authored material contradicts an **earlier lead ruling**, you may not resolve it: both sides carry the lead's authority. Record both, resolve neither, hold every dependent correction behind a named condition, and hand it back.

**⛔ RUN THE FOUR TESTS WHEN YOU *WRITE* THE QUESTION, NOT WHEN YOU HAND IT OVER.** A seed's question list is where a fork is really authored — a question labelled `OPEN` there **is a fork you have already committed to**, and it gets carried forward and re-committed by every later pass. **Test 1 is cheapest at authoring**, when you are still holding the document that answers it. *(A seeded `OPEN` question — "what happens when the root stops being `noindex`?" — sat in a committed doc across two commits as a lead call. At Brief time the tests were run properly and it failed test 1 outright: removing `noindex` **is** the phase, said so in the `Outcome`. Had the lead answered it, that is a round trip spent on a decision already made.)*

**⛔ BEFORE YOU FORK — four tests, in order. A fork failing any of them is not a decision the lead gets to make.**

1. **ANSWERED?** — by the durable spec, a shipped peer, or a structurally identical ruling earlier in this same phase.
2. **NECESSARY?** — its triggering premise actually exists. A fork whose every option handles a condition that does not occur is noise.
3. **DELIVERABLE?** — every option's enabling capability exists. Confirm it before offering the choice, not after.
4. **⛔ ADMISSIBLE?** — are the options themselves things the lead may legitimately choose between? Tests 1–3 ask whether the *question* is real; this asks whether the *answers* are.

**When you do fork, separate independent decision axes up front** rather than presenting a tangle.

### Working in a shared tree

**Run `git status -sb` at kickoff.** Two sessions can legitimately hold write access to one phase doc, so a changed phase doc is a **real** collision to check — but ⛔ **`git status` can report ` M` on a file whose content matches `HEAD`** (the index caches stat data), so **run `git diff --stat <path>` before raising an alarm.** An empty diff means there is nothing to collide with.

**⛔ THE CHECK IS ABOUT CONTENT, NOT RULES — do not watch your own governing docs.** Your briefing is a **snapshot**: you read the command docs at start and that read is your contract for the whole run. A landed commit touching `.ai/**`, `.claude/**` or `Methodology/**` is the Refiner, is expected, and is **not** a collision. **Notice, do not reconcile.**

**⛔ A SHARED ID SERIES IS A COLLISION SURFACE NO FILE GREP CAN SEE.** Where a phase continues another's numbering — gate ids, id prefixes, migration ordinals — **do not pre-assign while a sibling is in flight.** Name the thing by what it asserts; the id is claimed at execution.

---

## Where discovery commits land

One repo, one commit, explicit paths. The phase doc and its Roadmap entry are the deliverable. **A new phase doc is untracked — `git add` it before its first explicit-path commit.** Read back with `git show --stat`.

## Hand-off

**Three beats: `Done` · `Notes` (omit unless it changes what the lead does) · `⛔ YOUR CALL` (last, closed by the `▶` line).** `AI_WorkingAgreement.md` §Working With the Lead owns the format.

Say plainly whether the Brief is complete and which lane the phase is in — that goes in `Done`. **The lane decides the `▶` line**: `build` → **`/execute`**, `high-rigor` → **`/plan`**. **Any question the Brief could not close is a numbered `YOUR CALL` item with your recommendation** — never a finding id, and never left for the lead to discover by reading the phase doc.

**⛔ The close ceremony is not a discovery concern** — no status audit, no `🎉 PHASE COMPLETE`. That is `execute_close.md`.
