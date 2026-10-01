# Workflow Feedback — Library Coverage + Phase10 / discovery / session

| | |
|---|---|
| **Verb** | `discovery` (after a `/howdy`), across two units in one session |
| **Unit** | Library Coverage (numbered Phase10, then un-numbered again: `PhaseTBD_LibraryCoverage.md`, scope `LC`) and **Phase10 Coloured Wear Layers** (seeded mid-session) |
| **Mode** | cold start; a lead re-sequence mid-discovery |
| **Outcome** | done for the session: Library Coverage numbered (`5acd0bc`) and Pass 1 (`224db77`); re-sequenced on the lead's ruling, with Phase10 seeded and Library Coverage paused (`49b63e6`); Phase10 Pass 1 (`55ed6e2`). One question open (Q-P10-1). Nothing pushed (6 ahead). |
| **Shape** | doc-only |
| **Confidence** | Ran fully: `/howdy`, `/discovery` cold start on a seeded doc, the numbering rule, a reseed (framing flip), a re-sequence with id renaming, a seed + Pass 1 in one response. **Not exercised:** the Brief, any execute. |
| **Date** | 2026-10-01 |

Step 0: every in-chat finding is in a tracked file (the two phase docs, the Roadmap, BigPicture BP10), except the stale *Hair That Reads as Hair* Roadmap entry, which is a stale sentence outside this run's units; it is carried in §Open questions with its exact wording.

---

## Items, ranked

### 1 — A lead's proposal inside a research question was carried as a standing requirement `[self-error-doc-could-prevent]`

**Grounding.** `260926_R_BigPicture_NimbleSetup.md` opens with *"The lead proposed this sequence and asked for review"*, whose item 2 is *"an AI generation loop that runs at fixed times"*. BP5 says *"The proposed sequence (Pass 5) is accepted as the working plan."* I read that as adopting every clause. Under "precedent counts as an answer", I wrote "running at fixed times" into Library Coverage's scope as settled. I then priced it as a service (GPU, usage, headless permissions) using the CI precedent, and put it to the lead as a blocker. The lead: *"The fixed times was ONE session... remove taht thought."* A brainstorm clause had been promoted to a ruling, and it cost a blocker slot and a correction.

**Proposed fix.** In `discovery.md` §Discovery discipline, *where rulings live*: *"A proposal the lead makes INSIDE a research question ('the lead proposed … and asked for review') is input, not a ruling. 'Accepted as the working plan' adopts the ORDER it states, not every clause in it. A clause binds only if a `## Resolved` row names it. Before carrying one forward as settled, quote the row that adopts it."*

**Where it'd live.** `discovery.md` §Discovery discipline (*where rulings live*), next to fork test 1. Portable.

---

### 2 — Ids minted under a phase NUMBER broke when the number moved an hour later `[doc-gap]`

**Grounding.** The lead numbered Library Coverage Phase10. Pass 1 minted `F-P10-1…12` per `NamingConventions.md` §Planning ids. The lead then moved Phase10 to a new phase, so the old ids would have collided with the new phase's series. I renamed them to `F-LC-n` (a scripted `sed`, 23 hits) and declared scope `LC` in the doc header. **But commit `224db77`'s message still says `F-P10-1..12` about Library Coverage**, and commit messages cannot be edited, so `git log --grep F-P10-` now finds two phases. The §Planning ids grammar says *"the scope names the file"*, which assumes a number never moves. On this project it has moved six times in seven days (Library Coverage alone held 05, 07, 08, TBD, 10, TBD).

**Proposed fix.** In `NamingConventions.md` §Planning ids: *"A phase's number can move until it closes. When it does, rename that phase's minted ids to the new scope in the same commit, and say so in the commit message ('ids F-P10-n → F-LC-n'), so a `git log --grep` on the old id finds the rename. Commit messages before the rename keep the old scope."* Possibly also: *"mint ids under a mnemonic scope until the Brief, when the number is stable."* That would have avoided it outright, but it is the refiner's call.

**Where it'd live.** `NamingConventions.md` §Planning ids (marked as the method's, so upstream). Portable.

---

### 3 — An option that splits work into "its own phase" did not say where that phase SITS in the order `[self-error-doc-could-prevent]`

**Grounding.** Library Coverage Pass 1, F-LC-7: I recommended colour on wear layers become *"its own phase, seeded unnumbered"*, priced only by rework (*"adding colour later costs little re-work"*). The real consequence was ordering: every article the loop builds carries these layers, so the split phase must run first. The lead saw it at once: *"If 2 then we need to do that phase now instead."* I wrote *"Library Coverage depends on it"* only afterwards, in the seed. Fork test 3 (*DELIVERABLE: its doer*) asks who does an option's work, never **when it lands relative to this phase**.

**Proposed fix.** In `discovery.md` §Forking to the lead, under test 3: *"An option that splits work out of this phase states where the split sits in the order (before or after this one) and what this phase consumes from it. A split that this phase depends on is a re-sequence; say that in the option itself."*

**Where it'd live.** `discovery.md` §Forking (test 3) and the *Deferral row* rule beside it, which already makes this point for deferrals but not for splits. Portable.

---

### 4 — `/howdy`'s "what is next" named a Roadmap head the last close had already emptied `[doc-gap]`

**Grounding.** Asked *"what is next"*, `/howdy` named *Hair That Reads as Hair* (first under `## Future`, RESEARCH) and offered `/discovery` on it. The lead: *"Is that really a phase? If this is still about cards then we can skip it."* One grep of Phase09's close (*"card hair is matte in every renderer"*; strands *"ruled out (plan §Not now, MAP-RD4)"*) showed the card half was done and the strand half was waiting on the platform. "Glance only" is right for orientation, but a "what is next" answer is a sequencing claim, and position alone was stale.

**Proposed fix.** In `howdy.md` §Output: *"When the lead asks what is next, check the head entry against the most recent close's deferral ledger (one grep for the entry's name in the last closed phase doc) before naming it. Order is position, but a close can empty an entry without anyone moving it."*

**Where it'd live.** `howdy.md`. Portable.

---

### 5 — "Seeds and stops … run Pass 1 in the next turn without waiting" is ambiguous inside one response `[doc-gap]`

**Grounding.** The lead's *"we need to do that phase now instead"* opened a phase that had no doc. `discovery.md` Cold start 1: *"The stop is a TURN boundary, not a session boundary. Land the seed as its own commit, say you read the invocation as opening Pass 1, then run Pass 1 in the next turn without waiting to be asked again."* An agent cannot start a turn on its own. I read "next turn" as "after the seed's own commit, in the same response", and ran Pass 1 (`49b63e6` seed, `55ed6e2` Pass 1). The alternative reading, stopping and handing back for a "keep going", is the round trip the rule exists to avoid.

**Proposed fix.** Replace *"in the next turn"* with *"right after the seed's own commit, in the same response: the commit is the boundary"*.

**Where it'd live.** `discovery.md` Cold start 1. Portable.

---

### 6 — The Roadmap has no status word for "discovery paused after Pass N" `[doc-gap]`

**Grounding.** Re-sequenced mid-discovery, Library Coverage had a phase doc with Pass 1 captured and nothing in flight. The Roadmap vocabulary is `RESEARCH → SEEDED → ACTIVE (parked on <ref>) → COMPLETE`, where `parked on` means waiting on *another repo*. I wrote `SEEDED` with a parenthetical *"(discovery Pass 1 captured …, then paused for Phase10)"*, which bends `SEEDED`'s *"phase doc written"* meaning.

**Proposed fix.** Widen the vocabulary: `ACTIVE (parked on <ref>)` covers waiting on another *unit*, a phase here included (*"parked on Phase10"*), or add `SEEDED (paused after Pass N)`.

**Where it'd live.** The Roadmap header's status vocabulary (its template is upstream). Portable.

---

### 7 — Two `cd <root> && …` compounds again (the previous retro's "one cd slip" recurs) `[self-error-doc-could-prevent]`

**Grounding.** `cd /…/Matter-Library && git ls-files … | awk …` to count articles, and `cd /…/Matter-Library && uv run python - <<EOF` for the layer measurement. `uv run` needs the project root, which is what pulled in the `cd`. `git -C` served everywhere else.

**Proposed fix.** Name the `cd`-free form for uv where the shape rules live: `uv run --directory <repo root> …` (or `--project`), as `git -C` is named for git.

**Where it'd live.** `.claude/CLAUDE.md` §Codebase search (fallback shapes) or `ToolingConventions.md` §Entry points. Local, since `uv` is this stack's.

---

## Keep these

- **"Precedent counts as an answer"**: the lead's 2026-09-28 *"make this Phase 8, mark the current Phase8 as TBD"* settled the re-sequence's numbering with no round trip. I said I followed it, and offered to flip it.
- **The reuse check, run against the engine's own definition:** reading `open_pbr_surface.mtlx` found fuzz defined for *"dust grains"*, already built in all three tools. A contract change that looked like new shading collapsed into reuse.
- **Measure, don't carry forward:** a 10-line probe of the 9 layers turned the seed's "wear layers too faint" into "dust is colourless, scuffs are faint", which re-routed `Scuffs01` back to Library Coverage.
- **Where rulings live:** CM2's boundary in `Taxonomy.md` answered "do makeup and freckles belong here?" without asking the lead.
- **"Reseed, don't patch, on a core-framing flip"**: Library Coverage's doc was rewritten once, cleanly, with every seed item kept and marked.
- **Explicit-path stage + `diff --cached --stat` + `show --stat` read-back:** five commits, each count matching the edit.

## Dead weight

None.

## Open questions

1. **+1 on the backlog's Open 1 (handback format):** `discovery.md` §Hand-off says *"Three beats: Done · Notes · YOUR CALL"* while citing `AI_WorkingAgreement.md`, which owns five. Both handbacks this session used the five; nothing new beyond the repro.
2. **An owed content fix (a `/quick-fix`, outside this run's units):** the Roadmap entry *Hair That Reads as Hair* still says *"on cards now and on strands later"*, but card hair was finished and ruled matte in Phase09 9.1 (*"until we get proper hair... this will need to be the way"*), and strands wait on the platform's switch to grooms (`260928_R_HairAndNailRendering.md` H5: *"the lead's call when the platform switches to grooms. Not now."*). Suggested annotation, dated rather than deleted: *"Reevaluate (2026-10-01): the card half closed in Phase09 (matte cards, 9.1); what remains is strands, waiting on the platform's switch to grooms (H5), plus card maps (H4)."* I raised it in chat at `/howdy`, and it is recorded nowhere else.
3. **`docs/Planning/Phases/Complete/ignore`**, a folder seen in a listing whose purpose I don't know. I did not open it. A lead question, if anyone.
4. **Q-P10-1** (who picks the dust colour) is open in `Phase10_ColouredWearLayers.md`. It's not a method question; it is listed here only so it isn't lost.
