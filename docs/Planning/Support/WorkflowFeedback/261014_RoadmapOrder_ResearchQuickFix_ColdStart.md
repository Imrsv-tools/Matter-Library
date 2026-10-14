# Workflow Feedback — RoadmapOrder / research → quick-fix / cold start

| | |
|---|---|
| **Verb** | `research → quick-fix` (a lead-directed graduation: *"yep! Good... quickix and push"*) |
| **Unit** | `RoadmapOrder` (`docs/Planning/Research/261014_R_RoadmapOrder.md`) |
| **Mode** | cold start |
| **Outcome** | done. Six research passes; the Roadmap was reordered in the lead's cut, unnumbered (`2739b6b`, pushed); CC0-only recorded and Two Licences withdrawn; the platform site's snapshot ask was routed to *Materials Described* and M9. |
| **Shape** | doc-only |
| **Confidence** | Ran fully: `/research` (orient, audit, passes, rulings, landing) and the `/quick-fix` landing with a push by value. **Not exercised:** `run_all.py` (a docs-only change), disposable probes. |
| **Date** | 2026-10-14 |

---

## Items, ranked

### 1 — The lead's own precedent in a SIBLING repo is an answer too, and I designed past it `[self-error-doc-could-prevent]`

**Grounding.** Asked whether the library service needs a GPU, I designed shape (d) (Pass 4): contributors render, and the article, the pictures and the evidence go to three places. The lead: *"No...I see.. that is jenky... they submit one entry per material, then we test on upload and parse as needed (like we do with compositions on web)"*. The web repo, which this checkout can read, already has the pattern: one upload, a fresh sandbox per upload, a refusal that names its rule. I had read that repo minutes earlier for the server's size, and never for its upload shape. That cost a whole pass and a round trip.

**Proposed fix.** In `AI_WorkingAgreement.md` §Working With the Lead, under *"PRECEDENT COUNTS AS AN ANSWER"*, add one line: *"That includes a shape the lead already ships in a sibling repo this checkout can read (an upload, a check, a release). Before designing a flow, grep the sibling repos for the same act and start from theirs."*

**Where it'd live.** `AI_WorkingAgreement.md` §Working With the Lead. It is portable: any multi-repo lead has this.

---

### 2 — A lead ruling made in a CONSUMER's session about THIS repo has no path here `[doc-gap]`

**Grounding.**
- On the web side, the lead answered *"Yes CC0 only"*. The web side recorded it as withdrawing this library's RD-MP-1, and noted *"the library records its own"*. Nothing carried it here.
- Meanwhile this repo still allowed CC BY, and had seeded a phase on it (*Two Licences*) that morning.
- I found the collision only because the lead asked about the web phase and I read its doc. The lead then confirmed: *"YES... CC0 for materials... we decided that"*.
- Backlog row 79 (*a consumer's ruling arriving by a private id*) covers how to **record** one. It does not cover one that never **arrives**.

**Proposed fix.** In `LOCAL_DELTAS.md` §Separation: *"A lead ruling about the library can be made in a consumer's session. Orient (`/howdy`, research Pass 1) reads the consumers' recent rulings that name the library — fetch, then read at origin — and lists any this repo has not recorded."* Upstream, the general form for any producer/consumer pair: *"a consumer that records a ruling about its producer leaves a ledger line on the producer's side, or says it did not."*

**Where it'd live.** `LOCAL_DELTAS.md` §Separation (local). The producer/consumer form may be portable: `Workflow` §Phase Numbering's neighbour on integration.

---

### 3 — A consumer's ask can arrive in the CONSUMER's repo, not ours `[doc-gap]`

**Grounding.** `LOCAL_DELTAS.md` §Separation says *"A consumer's ask arrives as a research doc the consumer writes into `docs/Planning/Research/`"*. The web side's site phase instead wrote a section titled *"Needs the library"* into its **own** phase doc, *"addressed to the Matter Library's session, which reads this repository"*, and parked a step on it. Nothing here pointed at it. The lead had to name the phase number.

**Proposed fix.** Add a second sentence to that row: *"…or as a section in the consumer's own phase doc, addressed to this repo's session. Orient greps the consumer repos' active phase docs for this library's name."* Item 2's orient step would cover both.

**Where it'd live.** `LOCAL_DELTAS.md` §Separation.

---

### 4 — `git commit -- <paths>` already excludes a sibling's staged file; the restore dance is only for a commit from the index `[doc-gap]`

**Grounding.** A sibling had `A docs/Planning/Support/WorkflowFeedback/261014_P11_Execute_Close.md` staged when I committed `2739b6b` with an explicit pathspec. My commit held exactly my 7 files, and the sibling's file stayed staged for them; they committed it as `a291319`. `.claude/CLAUDE.md` §Git says: *"a path you did not touch → `git restore --staged <path>`, commit, then `git add` it back"*. Read literally, that adds two index writes racing a live sibling, for no gain: a pathspec commit is `--only` by default.

**Proposed fix.** Scope the line: *"Before a commit FROM THE INDEX (`-F` with no pathspec, the filtered-stage case): restore it, commit, re-add it. A `git commit -- <paths>` commits only those paths, whatever else is staged; check `git diff --cached --stat`, and leave the sibling's index alone."*

**Where it'd live.** `.claude/CLAUDE.md` §Git, the index paragraph. Portable, upstream.

---

### 5 — A sequence for the lead to CUT reads best as a flat list with one-line outcomes; the dependency analysis stays in the doc `[self-error-doc-could-prevent]`

**Grounding.** My first landing gave a five-column dependency table, then grouped buckets with rationale per line. The lead: *"I can't really see the roadmap"*, and later *"I will want to see the proposed phase order again Not numbered just one after the other with SHORT outcome so I can verify this makes sense"*. When I gave him exactly that, he accepted it in one word: *"yep! Good"*. `research.md` §Landing says only *"unnumbered, with no ordinal column"*.

**Proposed fix.** In `research.md` §Landing, under *"An agent-drafted sequence is research output"*, add: *"Present it for the cut as one flat list, top to bottom: each line is the phase's name plus a short Outcome. Put waits and rationale in the doc, not in the list the lead verifies."*

**Where it'd live.** `research.md` §Landing. Portable.

---

### 6 — I did not say which search mode I was following `[self-error-doc-could-prevent]`

**Grounding.** This session had no Grep or Glob tool; one `Grep` call failed with *"No such tool available"*. Auto mode allowed compound Bash, so I searched with pipes. `.claude/CLAUDE.md` §Codebase search says *"Say in your first message which you are following"*. I never did. The rule sits in the fourth paragraph of the section.

**Proposed fix.** Make it the first line of §Codebase search: *"First message: name the search mode (Grep/Glob, single-statement fallback, or the mode's compound shapes)."*

**Where it'd live.** `.claude/CLAUDE.md` §Codebase search.

---

## Keep these

- **"An agent-drafted sequence is research output — unnumbered" and "numbers are the lead's"**: the lead asked for numbering at the start and, three turns later, asked for an unnumbered list to verify. Nothing had been numbered that needed undoing.
- **"Seeds decay — read a sibling's clone at origin, never pull it"**: the web clone was 9 commits behind, and its phase doc existed **only** at origin (`git show origin/main:…`).
- **"Record a consumer's ruling by date and content, never by its id"**, plus grepping the added lines for the consumer's id patterns: the snapshot ask and the CC0 ruling landed here with no web-side ids.
- **Push your own tip by value (`git push origin <sha>:refs/heads/main`)**: a sibling's retro commit had landed on top of mine and stayed behind. The one under mine (the Phase11 close) was named in the handback.
- **The exactly-once anchor guard for batch edits**: 7 withdrawal notes across 4 docs, then 8 Roadmap annotations, each refused unless it matched once. The Roadmap reorder was verified with a sorted-line diff showing only the annotated lines.
- **"Placeholder" read as absent-and-labelled, never made up** (Working Agreement §No Mock Data): it turned *"is it smart?"* into a yes with one condition, and the lead took it.

## Dead weight

None.

## Open questions

1. **Item 2 is half a lead question:** should rulings about the library that are made in a consumer's session be the consumer's job to carry over (a ledger line here), or this repo's job to sweep for at orient? The Refiner can propose; the split of work between the two repos is the lead's.
