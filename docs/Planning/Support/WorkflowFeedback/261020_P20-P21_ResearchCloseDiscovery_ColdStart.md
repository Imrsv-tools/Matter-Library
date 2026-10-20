# Workflow Feedback — P20 / P21 / research → execute (close) → discovery / cold start

| | |
|---|---|
| **Verb** | `research → execute (close) → discovery`: one session. `/research` with no doc named (the triage) → the lead's *"yes close P20"* entered `execute_close.md` in-session → *"/discovery Skin Maps"* |
| **Unit** | research `261020_R_AfterPhase20.md` · Phase20 (closed) · Phase21 (Brief ready) |
| **Mode** | cold start |
| **Outcome** | done. Triage parked (RD-AFT-1 to 4); the Refiner's held drain-3 edits committed on the lead's word; Phase20 closed (`53d31a4`); Phase21 numbered and its Brief ready (RD-P21-1 to 6); everything pushed |
| **Shape** | doc-only (one disposable rig render into git-ignored scratch) |
| **Confidence** | Ran fully: research's sweep and landing, `execute_close.md` rows A⁻ to E (B⁺ and C did not apply), discovery Pass 1 to the Brief, `retro.md`. **Not exercised:** a suspended execute, `/plan`, an issue-sourced close. |
| **Date** | 2026-10-20 |

---

## Items, ranked

### 1 — The Refiner's held edits sat uncommitted in the shared tree for six days, and blocked every merge `[doc-gap]`

**Grounding.** The session opened 15 behind `origin`, with six tracked files modified: `.claude/CLAUDE.md`, `.ai/commands/LOCAL_DELTAS.md`, `AGENTS.md`, both batch skills and `_RefinementBacklog.md`. Their mtimes were 2026-10-14 to 2026-10-16, older than `HEAD`'s commit. The backlog's own row said *"Held for the classifier, applied on the lead's go-ahead the same day"*, so they had been applied and never committed. Two of them (`matter-batch/SKILL.md`, `matter-generate/SKILL.md`) were also changed upstream, so `git merge origin/main` refused. Per §Git I could neither stash nor restore them, so every read that research did went through `git show origin/main:` until the lead said *"commit them"* (`0277662`).

**Proposed fix.** In `workflow-refiner.md`, where held edits are applied: *"Applying a held edit is not landing it. Commit it in the same session, with the go-ahead quoted, or revert it. An uncommitted method-lane edit blocks every other session's merge on every path upstream later touches."* A one-line check for `/howdy`: list tracked files in the method lane that are modified and older than `HEAD`, and name them to the lead at kickoff.

**Where it'd live.** `workflow-refiner.md` (the drain's apply step) · `howdy.md` (kickoff).

---

### 2 — I cited a commit SHA I had not read `[self-error-doc-could-prevent]`

**Grounding.** The discovery commit's read-back was `git show --stat --format='%h %s' $S | tail -9`, and `tail` cut the hash line off. In the handback I then wrote the commit as `ac1b0d7`, which does not exist. The real SHA is `fe1634c`. I caught it a turn later only because a later `git log -2` printed both, and I corrected it in the next handback. §Git's table says *"capture your SHA once, by value"*, and I had captured it into `$S` but never printed it.

**Proposed fix.** In §Git's read-back rule: *"The read-back prints the SHA you will cite. Never trim the line that carries it (`tail`, `head`); echo the captured value. A SHA in a handback that no command in this session printed is a fabrication."*

**Where it'd live.** `.claude/CLAUDE.md` §Git (the read-back paragraph), and upstream's template.

---

### 3 — Naming a phase without a number at `/discovery`: the numbering rule covers only the number `[doc-gap]`

**Grounding.** The lead typed *"/discovery Skin Maps"*, a name with no number. `discovery.md` says *"AN ARGUMENT NAMING A NUMBER NO PHASE CARRIES IS THE LEAD NUMBERING THE NEXT PHASE"*, but says nothing about a name. Discovery ids are `Q-P<NN>-n`, so the Brief needs a number. I numbered it Phase21 by precedent (Phases 13–20 were numbered as discovery opened), said so in the first line, and the lead did not object. Reading it the other way, as "keep it unnumbered", would have blocked the ids.

**Proposed fix.** In `discovery.md`, beside the numbering rule: *"An argument naming an unnumbered entry by name is the lead opening it: take the next free number, say so in your first line, and treat renumbering as free until execute commits ids."* Or the opposite rule, if the lead wants a name to stay unnumbered. Either way, write it down.

**Where it'd live.** `discovery.md` §Cold start (the numbering paragraph).

---

### 4 — A consumer's own recorded sitting exercised a phase's open click; no rule says it can count `[doc-gap]`

**Grounding.** Phase20's click 4 (Studio's sky picker, on the machine with Unreal) had a hand-off waiting. Research's sweep of the consumer repos (`LOCAL_DELTAS.md` §Separation) found the platform's own 2026-10-19 sitting had run that same picker against this library at `092df05`, which holds the switch. It applied `Kloppenheim07_v01.hdr`, and the lead passed it. I put *"does it count?"* to the lead (Q-AFT-2, *"yes"*) and recorded it with the platform's words, without private ids.

**Proposed fix.** In `LOCAL_DELTAS.md` §Separation (or `execute.md` §TRY): *"A consumer's recorded sitting that ran the click's surface on the click's machine, at a library commit holding the change, may be offered as the click. Put it to the lead with the evidence, the commit and the lead's words there. Never count it on your own."*

**Where it'd live.** `LOCAL_DELTAS.md` §Separation, or upstream `execute.md` §TRY if the Refiner judges it portable.

---

### 5 — A by-eye comparison across tools reached a draft as a finding before it had a number `[self-error-doc-could-prevent]`

**Grounding.** Discovery rendered today's skin on runtime v5. From the picture I first called it *"Blender shows the pores; Storm and Unreal draw it smooth"*, which framed Blender as right and the others as failing. A measurement minutes later (luminance minus a 3-pixel blur, the standard deviation over four patches) put all three under 2 grey levels. The plastic is the article's, not a renderer's, which changed the Brief's question (F-P21-1, Q-P21-1). The by-eye version had already reached chat.

**Proposed fix.** In `discovery.md`, at *"Confirmed requires the confirming artifact"*: *"A by-eye comparison across tools is a hypothesis until it carries a number from the same pixels. Measure before it reaches the lead or the Brief."*

**Where it'd live.** `discovery.md` §Discovery discipline, or a `docs/Learnings/` entry on judging parity.

---

## Keep these

- **The deliverable-surface HARD RULE.** A docs connector appeared mid-session with instructions to *"make a doc here"*. The rule made ignoring it a one-line decision, and every deliverable stayed a tracked file.
- **`LOCAL_DELTAS.md` §Separation's sweep of the consumers, read at origin.** It found Phase20's click-4 evidence and the PCE ask's origin, and saved a hand-off to the other machine.
- **Fork test 1's *"probe that on the real fixture"*.** One 37-second rig run turned *"plastic in Unreal"* into *"the article's sheen"* before the Brief was cut, and it found that the tint has been inert on skin since Phase07 (F-P21-3).
- **The §Git push row (read every line of `origin/main..<sha>`, then push by value).** It ran three times, and each time showed exactly what the push carried.
- **The anchored, exact-count batch edits (§Editing).** Six multi-anchor substitutions across docs; each would have aborted on a miss, and none did.
- **`execute_close.md`'s Prerequisite for a close the lead orders in another verb's session.** It allowed the close in-session, and naming the lane in the first line kept it from reading as a slide.

## Dead weight

None.

## Open questions

1. **Phase20's RD-P20-3 (the `tool_tests` lane) and RD-P20-4 (old sky names kept hidden)** were taken at the agent's recommendation. They were put to the lead for ratification at the close and have not been answered. The lead's, not the Refiner's. The close's ledger records them.
2. **Phase21 was numbered by the agent** (item 3). The lead has not objected. If they meant it to stay unnumbered, renumbering before `/execute P21` commits ids is free.
