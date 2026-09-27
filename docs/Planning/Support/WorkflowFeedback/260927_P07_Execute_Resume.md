# Workflow Feedback — P07 / execute / resume run 2, suspend-handoff

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P07` (Character Materials) |
| **Mode** | resume run 2 → suspend-handoff (the lead: *"close enough, your context is high... we should hand off"*) |
| **Outcome** | suspended at the 7.5/7.6 boundary. Landed 7.3 (skin inputs, six skins, CM-Q10), 7.4 (the MakeHuman body in the rig), 7.5.1 and 7.5.2 (twelve more articles); five lead sittings, each passed and transcribed. Not pushed (the lead's call, unanswered). |
| **Shape** | behavior-touching (contract, assembler, Blender masters, the parity rig, 23 articles) |
| **Confidence** | Ran fully: `/execute` BUILD → TRY → STRENGTHEN, act by act with the lead present; the suspend. **Not exercised:** the close (`execute_close.md`), the high-rigor lane, `execute_repair.md`. |
| **Date** | 2026-09-27 |

A distinct run, **not** a continuation of `260927_P07_DiscoveryExecute_ColdStart.md` (the earlier session on this unit, still in the inbox). Its item 4 recurred here: see item 3.

---

## Items, ranked

### 1 — The lead had to call the handoff for context, two runs running; the executor never measured its own `[doc-gap]`

**Grounding.** `execute.md` §STRENGTHEN lists "Context is running out — wrap at the next cohesive boundary. ~400k is an attention ceiling" as a suspend trigger, but gives no moment to check it. This run crossed five act boundaries (each a natural wrap point) and never once reported or checked its context; the lead ended it: *"close enough, your context is high... we should hand off"*. The previous run on this same phase was suspended the same way: *"how is context... should we handoff?"* (its Resume block records it). Two consecutive runs, the lead acting as the context gauge.

**Proposed fix.** In §Keep the lead oriented, beside the one-line ledger: *"At each ACT boundary (a sitting handed back), state your context in the ledger line — roughly, in tokens — and if it is past the attention ceiling, say so and offer the handoff yourself in `YOUR CALL`. The lead should never be the one to notice."*

**Where it'd live.** `execute.md` §Keep the lead oriented (and the suspend list's context row should point to it).

---

### 2 — Unlabelled multi-file output, paired by assumed order, nearly produced a false finding `[self-error-doc-could-prevent]`

**Grounding.** Bisecting a parity gap (which of three new inputs moved Skin III), I ran `grep -h "^| defaults" <four scorecards>` and paired the output lines with the files in the order I had typed them. The pairing was wrong. It produced a contradiction (the variant with *no* new inputs scoring 5.60, where the unchanged article scored 2.69), which I started to reason about as a real effect before opening one sheet and seeing 2.69 on it. Re-run with `-H`, the answer was clean (anisotropy was the whole gap). A measurement that "looks like" per-file results but carries no file names is the same class as `.claude/CLAUDE.md`'s *"a git command that looks like a measurement"*.

**Proposed fix.** One row in `.claude/CLAUDE.md`'s measurement table (or the codebase-search rule): *"`grep`/`head`/`tail` over several files without `-H` (or `==> <==` headers): output you will PAIR with inputs by position → always label it (`grep -H`); never attribute a line to a file by its order."*

**Where it'd live.** `.claude/CLAUDE.md` §Git's measurement table, or §Codebase search (unsure which; portable either way).

---

### 3 — Recurrence: a probe built outside the harness's own inputs broke the harness, again `[self-error-doc-could-prevent]`

**Grounding.** The earlier P07 retro's item 4 ("when a probe passes and the harness fails, diff the harness's inputs before varying settings") is still in the inbox, undrained. This run repeated its class within hours: my bisect copied the article to new file names without renaming the material inside, the rig binds the material by the file stem, and Storm rendered every variant grey (ΔE 13 on all four). One wasted render round before I read the picture.

**Proposed fix.** No new wording; this is evidence for that item: two occurrences on one unit in one day. Suggested sharpening when it lands: *"A probe that COPIES a harness input must satisfy every key the harness looks it up by (names, stems, paths). Look at the picture before reading the number: a probe that broke the harness renders obviously wrong."*

**Where it'd live.** With the earlier retro's item 4 (`execute.md` §Verify before edit).

---

### 4 — The divergence table has no row for "a Not-now item's stated reason turns out to be false" `[doc-gap]`

**Grounding.** The Brief put the cornea under **Not now** *because* "MakeHuman's eye has no cornea shell" (research Pass 3). At 7.5.1 the high-poly eye turned out to have one (245 faces per eye, mapped to a fully transparent disc of its texture). Rendered, the shell covers the iris, so the in-scope eye articles could not be judged without a clear article on it. No row fit: it is not "invent a user-facing constraint", not "the lead asks for work outside the phase", and "small surprises: note and proceed" undersells building a Not-now article. I built it (and a pupil), logged a small deviation, and told the lead at the sitting; the lead passed it without comment.

**Proposed fix.** A divergence row: *"A Not-now item's STATED REASON is false (the fact it rested on does not hold) → if in-scope work cannot be judged or cannot work without it, build it, log a deviation naming the false premise, and surface it at the next sitting; otherwise leave it Not now and record the corrected fact so the next planner can reconsider."*

**Where it'd live.** `execute.md` §Divergence.

---

### 5 — A lead-gated `YOUR CALL` item the lead keeps passing over: re-ask how often? `[doc-gap]`

**Grounding.** The Brief scheduled a push after 7.3 (Phase06 builds against its inputs). I put "the push" in `YOUR CALL` at five consecutive handbacks; the lead answered every other item and never this one (`main` went from 11 to 20 ahead). I could not tell whether it was a deliberate "not yet", an oversight, or noise. Repeating it each time added a line the lead evidently reads past; dropping it risks Phase06 waiting silently.

**Proposed fix.** In `AI_WorkingAgreement.md` §Working With the Lead: *"A `YOUR CALL` item the lead has passed over twice: ask ONCE directly, as its own one-line question with the cost of waiting ('Phase06 is blocked on this'), then record the lead's answer (or 'unanswered, re-raise at <event>') in the Resume block and stop repeating it."*

**Where it'd live.** `AI_WorkingAgreement.md` §Working With the Lead (the `YOUR CALL` entry gate).

---

### 6 — I broke the tripwire once: a no-op `sleep 1` while a background render ran `[self-error-doc-could-prevent]`

**Grounding.** Waiting for the corrected bisect, I issued `sleep 1` "to wait". Rule 3 of the THREE RULES names that exact shape (*"A no-op call (`true`, `sleep 1`...) is the same violation"*). I recognised it on the result and ended the turn. The rule is right and prominent; I include it only as a data point that it still fires under a "the user hasn't heard from you" nudge, which is when it happened.

**Proposed fix.** None to the rule. If anything: *"A harness nudge to post a status update is a reason to WRITE a line, not to make a call."*

**Where it'd live.** `execute.md` §THREE RULES, rule 3 (optional).

---

## Keep these

- **The Outcome as ACTS, walked with a present lead (§BUILD, "the unit of work is an act").** Five sittings in one run, each short, each passed; 7.5 was split into two acts (head and hands, then clothing) so the lead saw the face before any fabric work began.
- **Look at the picture, not only the number.** Every material defect this run was found by viewing a sheet, none by the score: light skin going grey-green under `RANDOM_WALK`, tiling-normal seams on the neck, a 1 cm denim tile repeating its blotches, the cornea shell covering the iris, and the rig's own grey probe renders.
- **Re-run a known-good subject after editing shared rig code** (Verify before edit, "a count you measured goes stale at your next commit"): GreyCard (0.35 / 0.26) and Neon's −4-stop view (0.30) after each change to `compare.py` and the drivers. Nothing broke, and the handback could say so.
- **Post-commit read-back (`git show --stat`) and the churn check.** The churn check named two sibling commits (`2b11bf5`, `4b76e30`) in the run's range, both touching files I later edited, and confirmed no collision.
- **Anchor edits on unique text.** Two anchored `Edit`s missed (the text had changed) and *reported* the miss, so nothing was silently skipped; the one multi-block replacement was a script with count assertions on both anchors.
- **Transcribe the verdict verbatim, and never self-mark a `⚠human` step ✅.** Every step went `▶ SCAFFOLD COMPLETE` → `✅` only on the lead's words.

## Dead weight

None.

## Open questions

1. **Lead decision, routed:** when skin's soft detail (blush, freckles, makeup, tone variation) gets built. Offered three options in chat; the lead moved on without choosing. Now recorded in the P07 Resume block (committed `216a186`), not only in chat.
2. **Lead decision, unanswered:** the push (see item 5). Recorded in the Resume block as owed.
