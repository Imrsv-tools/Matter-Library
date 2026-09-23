# Matter Library — Working Agreement

> **Job:** the **engineering agreements** — how we build here. Process agreements (workflow, phase numbering, commit cadence, learnings) live in `Methodology/AgenticEngineering_Workflow.md`. For *which doc owns what*, see `Methodology/AgenticEngineering_DocumentationMap.md`.
>
> The sections below are the **portable set** — they make agentic work sane in any project. Add stack-specific agreements (ownership boundaries, lifecycle rules, asset management) when the project commits to a stack; delete none of the portable ones without a recorded reason.

## Documentation Shapes Architecture (Conway's Variant)

A variant of Conway's Law guides this project: **the architecture and the built system are shaped by our *documentation* structure**, not (only) by our org chart. The names, boundaries, and concepts committed to `docs/Glossary.md` and the spec docs propagate into components, interfaces, and module boundaries — and **drift in the docs becomes drift in the system.**

Consequences:

- **Fix the term in the doc first; the implementation conforms.** The glossary is load-bearing, not decoration.
- **A naming decision is an architecture decision.** Treat terminology normalisation as real work, not cosmetics — cheap to get right early, expensive to unwind later.
- **Per-layer vocabulary is legitimate by design** — a user-facing word may differ from the internal one, *provided the translation boundary is explicit and documented*. What is illegitimate is two names for one thing at the **same** layer.
- **A boundary that is never named in the docs never grows in the system.** If a distinction matters, give it a term and a home; otherwise the implementation will quietly collapse it.

This applies from the second file onward: the moment a term is reused, it is load-bearing.

## No Workarounds (softened for spikes)

We build real things. Prefer the proper long-term solution.

- The **one sanctioned exception is an explicit spike**: a throwaway probe to answer a question fast. Mark it as such (in the phase doc / commit / a `SPIKE:` comment) so nobody mistakes it for foundation.
- Anything that outlives its spike gets rebuilt properly or is explicitly promoted with eyes open. Silent "temporary" code becoming permanent is the failure mode to avoid.

## No Mock Data Masquerading as Real

- Fabricated/placeholder data lives in `tests/` or is labelled a fixture — never presented as a real result.
- Fail loudly. Throw on the unhandled case rather than returning a plausible-looking default.

## What a Phase Is

**One phase = one thing added, configured, tested, and refined, with one user-facing outcome.** Not a period of time ("soak for two weeks" is not a phase). Not a bundle of related things — if two items get added and tested separately, they are two phases, however far off they are.

## Don't Delete Intent

If a planned idea isn't built yet, mark it **Todo** / **Reevaluate** — don't silently delete it from a plan or research doc. Deferred items keep their motivation; deleted ones lose the "why."

**Scope:** this protects work that was planned *and reasoned about in flight*. An unstarted registry seed that has been overtaken is just **deleted** — git keeps it, and a `RETIRED (superseded)` entry is clutter.

## Working With the Lead

**Proposals default to a list.** Rationale only when asked, and then one line per item. The lead reads the structure first and asks about whatever looks wrong.

**If the deliverable is not at the path the lead would open, that is the FIRST line of the report, not the last.** An unmerged branch means the work does not exist from their side, however finished it is from yours.

**⛔ THE HANDBACK IS FIVE LABELLED BEATS, IN THIS ORDER, AND NOTHING ELSE. EVERY VERB, EVERY STOP.** *(Lead-specified, 2026-08-25.)* **⛔ EXACTLY ONE CARVE-OUT, lead-specified 2026-08-26: a `/retro` handback ends with the terminator line `RETRO SUBMITTED — no other actions expected.` — alone, verbatim, AFTER the `▶` line.** `/retro` is the session's last act, and the terminator is how the lead sees at a glance that the agent is complete rather than still running (`retro.md` §`/retro` IS TERMINAL owns it). **No other verb adds a sixth line, and nothing else may follow `▶`.**

```
Completed:   what actually landed. Bullets, not prose.
Next:        the todo list, ordered. What a next session picks up.
Stopping:    ONE line — why this run ends here.
Blockers:    questions that BLOCK. Omit the section entirely if none.
▶            the call to action — one command, on its own line.
```

**The rules that make it work, each one written from a way it has already failed:**

- **Labels are load-bearing — the lead scans for a heading, not through a paragraph.** Do not rename, reorder, merge or "improve" them run to run. **A structure that changes every time cannot be scanned at all**, which is worse than a mediocre structure held constant.
- **⛔ `Blockers` means BLOCKED — "I cannot proceed without your answer."** A recommendation you are confident in is **not** a question: make the call, note it under `Completed`, move on. A decision that can wait goes to the **tracker or the backlog**, silently. **⛔ THE ONE THING THAT MUST RE-APPEAR IN `Blockers` AT EVERY STOP UNTIL IT IS RESOLVED: A HELD TWO-RULING FORK** — where new material collides with an earlier lead ruling and the agent correctly recorded both and resolved neither (`discovery.md` §Discovery discipline). **That rule says to hold; it does not say who picks the fork up, or what happens while it sits** — so a held fork silently becomes permanent. **Carry it in `Blockers` every stop, and NAME THE DEPENDENT STEPS** (*"steps 8 and 9 are behind this; the other twelve are not"*), so the lead can price resolving it against letting it sit. It is one of the few things that is genuinely blocked **and** genuinely theirs. *(Asked independently by two runs of one phase: "does anything say who is meant to pick it up, or how long a held item may sit before it blocks the phase?" Nothing did.)* *(The failure being fixed: eight "open questions" presented as if each needed an answer, when none blocked anything and every one already carried a recommendation. That teaches the lead the section is noise, so a real blocker gets skimmed past.)*
- **⛔ NO EDITORIAL BEATS.** No "what I was concerned about", no "what you should know", no "judgment calls I made", no reflection on the work's quality. **If it changes what the lead does next it belongs in one of the five; if it does not, it belongs in the commit message.**
- **Length is a hard cap, not a target: `Completed` ≤ 6 bullets, `Next` ≤ 6, `Stopping` one line, `Blockers` ≤ 3.** Over the cap means summarise, not continue. **The full record lives in the doc and the commit — the handback is an index to it, never a second copy.**
- **The `▶` line is the point of the whole message.** One command the lead can act on (`/execute Phase08` · `Keep going` · `Push, then bump the SHA`). Never bury it, never offer three.

*(Lead-specified. The trigger: "there are too many words at the end of each process, and the structure keeps changing — I have to read a HUGE block to find what the next step is." A four-beat version had existed in `execute.md` only, so every other verb had no format at all.)*

**⛔ PRECEDENT COUNTS AS AN ANSWER — ALWAYS, NOT ONLY WHEN THE LEAD IS AWAY.** If the repository shows the lead has already ruled **this shape** — `git log`, the sibling phase docs, an earlier ruling **in this same unit** — **follow it and record explicitly that you did.** Do not re-put a settled shape to them as a fresh question. It binds hardest on an unattended run, but an attended lead is *more* annoyed by it, not less: they answer a question they have already answered. *(One run found a universal rule it could not honestly satisfy, ran the fork tests, and asked. The precedent was **three passes back in the same phase doc** — the lead had met the identical shape and resolved it with a narrow, explicitly-stated carve-out; the question even offered that as the recommended option and the lead picked it. The round trip drew "Why forking... we had a plan... stop fucking around." The precedent rule existed, but sat inside the unattended-runs paragraph, so it read as not applying while the lead was present.)*

**⛔ A BLOCKING ITEM IS PRESENTED AS A QUESTION, NEVER AS A FINDING ID. The lead is not reading your document.** Any handback that crosses a gate carrying blockers — a `/discovery` stage gate, `/plan` Step 4 (present), an `/execute` checkpoint — must contain, **in the message itself**, for each blocker: **the question in one line · the sources that conflict · the options · your recommendation.** A finding id (`F-39`, `RD-06B`) is a **pointer into your own working file** — from inside the doc an id *feels* like the question, which is exactly why this fails silently. **If a stage produced ≥1 blocker, the question list IS the presentation**; naming the ids and saying "four items need rulings" is not presenting, it is deferring. *(Three consecutive handbacks in one run named blockers by id only. The lead had already said twice "if you have questions for me to answer, present them here with background", and the third drew: "How many times do I need to ask you to provide questions if needed... PUT THE QUESTIONS HERE! NOW... ALL OPEN GATING QUESTIONS!" The questions existed — they were written down, in the phase doc, which the lead was not reading.)*

**⛔ AND A REJECTED QUESTION-TOOL CALL IS NOT A REFUSAL TO ANSWER — THE ANSWERS MAY SIMPLY NOT HAVE REACHED YOU.** Where the harness offers a structured fork tool (`AskUserQuestion` or equivalent) and it returns *"the user doesn't want to proceed with this tool use"* **with no answers attached**, do **not** read that as *"stop asking and proceed"* — that is the opposite of what may have happened. **Restate the options in plain text and say the tool returned nothing**, rather than proceeding on an assumption or re-issuing the identical call. This is the rule above doing its job: the plain-text question in the message **is** the reliable channel, and the structured tool is a convenience that can fail silently. *(Two genuine forks were put to the lead through the tool; it came back rejected with no answers, and the lead's very next message was "I asnwerd them!" — they believed they had. Restating both in plain prose got both back in one line.)*

**⚠ UNATTENDED RUNS — decide the policy for THIS project and write it here.** Where sessions run as background jobs with the lead away for hours, a **blocking ask delivers nothing until answered**, and several carried gates say *present and wait* (`discovery.md` Kickoff 3, `execute.md` precondition 1). The shape that has worked: **do the read-only, mandated, precedented part; say in your first message which you are doing; reserve a genuine block for facts only the lead has.** (Precedent counts as an answer here too — see the rule above, which is general.) If your lead is reliably present, delete this paragraph and keep the gates literal.

## Spec-Driven, Lightly

Where work grows a durable spec (in `docs/`), the spec is the source of truth and the code conforms; a mismatch defaults to "fix the code" unless you deliberately change the spec. Don't *over*-spec a probe — write the spec when the idea has earned permanence, not before.

## A Derived Document Reflects Decisions — It Does Not Make Them

A roadmap, a diagram, a README, a milestone list: each is **derived** from the records that hold the actual decisions (the product contract, a research thread's `## Resolved`, a phase doc). Writing one puts constant pressure to settle open questions in passing — a milestone needs a renderer named, a diagram needs an arrow to point somewhere — and settling one there **records nothing**.

**Where a derived document needs a decision that has not been taken: record it upstream first, then follow it.** Take it to the lead, land it in the owning record, and only then write the derived line. If it isn't worth stopping for, the derived doc says the question is open — it does not quietly pick.

Two failures this prevents, both observed: a roadmap draft asserted a renderer while that question was formally open, and softened a committed launch requirement to "desirable". Both calls were *right*; neither was *recorded*. **Left alone, the derived document slowly becomes a second, contradictory specification** — and the contradiction surfaces long after anyone remembers which one was authoritative.

**So: after authoring or revising a derived document, review it against its upstream records** and reconcile every claim it makes. That review is part of writing it, not a later tidy-up.

**⛔ AND THE CONVERSE, WHICH IS WHERE RULINGS GET LOST: A RULING WHOSE SUBJECT EXTENDS BEYOND THE UNIT YOU ARE WORKING ON LANDS IN THE RESEARCH THREAD'S `## Resolved` IN THE SAME TURN IT IS MADE.** **A phase doc is archived at close — anything recorded only there leaves with it.** The test is **blast radius**, not who made the ruling or which verb was running: if it names entities, files, prefixes or contracts **another phase owns**, it is not this phase's to store. **A `## Resolved` entry is upstream, never a derived doc**, so the *capture-now-apply-at-close* discipline that governs derived specs does **not** apply to it — that would defer an upstream record behind execution. Derived-doc corrections still route to the tracker or the close as normal; the *decision* lands immediately. *(Two repros a day apart. A discovery pass ratified an identity model upstream exactly as this section requires — then **the very next pass** recorded two rulings binding every domain's records in the phase doc alone. The derived-doc corrections were correctly filed as a tracker issue, which is precisely why it read as handled; the rulings themselves would have been archived with the phase. It took a lead-instructed re-review to find. The plan verb then hit the same seam from the other side.)*

## Confirm the Precondition Before Building for It

**A "handle legacy X" decision is a claim that legacy X exists.** In a greenfield project — no deployed instances, no on-disk formats — don't build dual-read paths, on-open repair, or legacy fallbacks. Format changes are a hard cutover while pre-release. *(A missing/unknown-field → safe-default + warn guard is still right; that guards corruption, not legacy.)*

## Round-Trip Completeness

Write every field, read every field back, and treat **absence as a write bug** — never paper over it with a default on read. **A backup is not a restore until it has been drilled.**

## Documentation Navigation

`Methodology/AgenticEngineering_DocumentationMap.md` owns which doc owns what, the **1-hop rule**, and the link conventions. Read it rather than re-deriving where something belongs.

## Build Safety

Never blow these away casually:

- **The OpenUSD + MaterialX toolchain build** (`tools/usd-toolchain/`; installed at the path its recipe names, with the conda env `imrsv-usd-tools`). It is a from-source build of about 30–50 minutes. Do not delete, re-create or `conda env remove` it to "get a clean state".
- **Frozen release records** in `library/releases/` (`*.lock.yaml`, `*.catalog.json`, `*.freeze.json`, `*.approval.json`). The freeze hash-locks the manifest, the catalog and every payload file, so **editing any of them — even a comment — invalidates the freeze and the approval that binds to it.** A change is a new release, never an in-place edit (§Project practices → immutability).
- **Textures under `MatterLibrary/textures/`** are Git LFS objects and are the shipped pixels. Regenerating one changes its hash and its provenance evidence.
- **`library/staging/`** (gitignored) holds the staged/compressed release tree. It is rebuildable, but only with `compressonatorcli`.

## Project practices

**⛔ EMPTY AT ADOPTION, AND THAT IS CORRECT. This section GROWS as practices are established —
never populate it in advance.**

Everything above is a **principle** and is true before a single line of code exists. This section
is the opposite: **how THIS project does a specific thing, or when it does it** — a comment
convention, a rule about when a particular kind of change needs a migration, an ordering the team
has agreed on. Each entry earns its place by having been **decided**, not proposed.

**The test for whether something belongs here rather than in a stack doc:** this section holds
practices about **how we work**; `CodingStandards.md` holds rules about **how code looks**;
`docs/architecture/` holds **what the system is**. If it would still be true after a rewrite in a
different language, it probably belongs here.

⚠ **Add an entry the moment a practice is settled, not at some later tidy-up** — an agreement
that lives only in a conversation is an agreement the next agent will break, and neither the
transcript nor `git log` is somewhere anyone looks for it.

### Settled practices

- **Don't Delete Spec Functionality — stricter than §Don't Delete Intent** *(carried from
  `.ai/conventions.md`; re-affirmed by the lead 2026-09-23: "We are not in production... still
  building")*. Design intentionally runs ahead of disk. When aligning docs, **never delete a
  previously-specified capability**, including an unstarted one: the §Don't Delete Intent
  carve-out for overtaken seeds does **not** apply here. Mark it `(planned)`, `Todo`, `Drift` or
  `Reevaluate` **with a date** instead. Preserve intent; annotate reality.
- **Immutability after promotion** *(carried from `.ai/conventions.md`)*. Once `material@vNN` or
  `texture@vNN` ships in a released manifest, that file is frozen, and a change is always a new
  `vNN+1`. The design is in `docs/specs/_Architecture.md`.
- **Planning and docs commit before implementation** *(carried from `.ai/conventions.md`)*. That
  commit is the rollback baseline.
- **No AI attribution in commits** *(lead, 2026-09-23)*. The person committing is the author and the
  responsible party (`.claude/CLAUDE.md` §Git).
- **Public by default** *(lead rulings R9/R13, 2026-09-23)*. This is a community resource.
  Contributed materials and textures are CC0-1.0, and credit is asked for, never required. Private
  platform detail never enters a tracked file.

## Process Agreements → `AgenticEngineering_Workflow`

How we *run* the work — the Workflow Cycle, phase numbering, Phase/Step/Task terms, commit cadence, the rollback-snapshot tenet, the Learnings Policy — lives in `Methodology/AgenticEngineering_Workflow.md`. Local delta: **one repo, one commit — no submodule SHA cascade. This repo is a producer; consumers take published releases, and the IMRSV platform still pinning it as a submodule is not a step here** (`.ai/commands/LOCAL_DELTAS.md` §Separation), and durable **learnings** live in `docs/Learnings/` (create on first real lesson).
