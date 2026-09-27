# Workflow Feedback — P07 / execute / resume run 3 + close

| | |
|---|---|
| **Verb** | `execute` (then the lead-directed close, `execute_close.md`) |
| **Unit** | `P07` |
| **Mode** | resume run 3 (7.6) + close. **Not a continuation** of `260927_P07_Execute_Resume.md` (run 2, a separate session); this is the next run on the same unit. |
| **Outcome** | done: 7.6 landed and was accepted (*"close enough, carry on"*); the phase closed (the lead overrode the owed 7.2 click 3) and was pushed (`40e3087..9f822ff`). |
| **Shape** | behavior-touching (assembler, Blender masters, rig, contract docs) |
| **Confidence** | Ran fully: `execute` (probe, build, one sitting), `execute_close` rows A⁻, A0, A, B, D, E. **Not exercised:** B⁺ (no Wave), C (no source issue), the high-rigor lane, `execute_repair.md`. |
| **Date** | 2026-09-27 |

---

## Items, ranked

### 1 — Close row D assumes a pushed phase gets a CI run; here CI is structurally absent, and that fact lives only in a closed phase's prose `[doc-gap]` (port gap)

**Grounding.** At the close I wrote "provisional until the push's CI run is read" into the status and the `🎉` commit, because `.github/workflows/gate.yml` says `on: push: branches: [main]`. After the push, `gh run list` showed no new run. `gh api …/actions/runs` gave `total_count: 1`: a `workflow_dispatch` run queued since 2026-09-23 with no runner, and the workflow `active`. The only statement that CI is parked is inside Phase05's `CLOSE — DONE` row ("automatic CI is parked (lead, 2026-09-23) … the local gate is the evidence"), which I found only by reading a sibling close for format. Row D's discharge act ("append `✅ CI OBSERVED <date> — <run URL>`") cannot happen here, so I invented a `CI NOT OBSERVABLE` status line in a follow-up commit and pushed it: a second commit and a second push.

**Proposed fix.** Add a `LOCAL_DELTAS.md` row: *"CI: `gate.yml` is active on push, but no runner picks it up; automatic CI has been parked since 2026-09-23 (lead). The close's evidence is the local `run_all.py`. Row D's stamp is not provisional here: write the local gate result into the `🎉` commit and the status line, and do not wait for a run."* If the lead un-parks CI, the row flips.

**Where it'd live.** `LOCAL_DELTAS.md` (port gap). Its "the way this project is RUN" row is the natural neighbour.

---

### 2 — Changing the shape of an artifact every tool parses: grep the readers BEFORE the first real run, not after it crashes `[self-error-doc-could-prevent]`

**Grounding.** 7.6 added an `image` node whose `file` has no value (the file comes from the binding). I fixed the Blender loader's reader while writing it, then launched the first character render, and the rig's own reader (`job.py` `Article.read`, `path.parent / f.get("value")`) crashed on `None`. Only then did I grep for every `name='file'` reader. That found a third that would have crashed later (`codec_ab.py`, `sorted()` over a set mixing `None` and `str`). Two regex readers were already safe. Cost: one failed background render and a relaunch.

**Proposed fix.** A Verify-before-edit row beside "making data VISIBLE that no surface previously read": *"You are changing the SHAPE of an artifact many tools parse (a node without an attribute every existing instance had, a new element type, an empty value): grep every reader of that shape BEFORE the first real run. A reader written when the shape was uniform assumes it."*

**Where it'd live.** `execute.md` §Verify before edit.

---

### 3 — "close enough, carry on" at the last step's sitting: is that the lead initiating the close? `[doc-gap]`

**Grounding.** My 7.6 handback's `Next` named the close. The lead answered the sitting with *"close enough, carry on"*. `execute_close.md` says the close is lead-initiated and never self-initiated, and its explicit-reading rule covers only the **push** authorization. I read "carry on" as initiating the close and said so in the handback; the lead's next message ruled on the close, which confirmed it. It was an inference, though, and the doc gives no test.

**Proposed fix.** In `execute_close.md` §Prerequisite: *"A 'carry on' that answers a handback whose `▶`/Next named the close counts as the lead initiating it. Say in your first close message that you read it so, as you would for the push."*

**Where it'd live.** `execute_close.md` (Prerequisite / Running it).

---

### 4 — Recurrence of run 2's item 6: I checked a backgrounded render twice before ending the turn `[self-error-doc-could-prevent]`

**Grounding.** During the character render I `tail`ed its output once (empty), then bundled a second `tail` into an unrelated `grep` call (empty again), and only then ended the turn. It was less blatant than run 2's `sleep 1`, but the same pattern: a peek that had no result I intended to act on. Filed only as a recurrence count; run 2 already proposed the fix.

**Proposed fix.** None new; count it toward run 2's item 6.

**Where it'd live.** `execute.md` §Three rules (the tripwire).

---

## Keep these

- **Row A0, applied mechanically.** The Outcome's "None … magenta" and "every one … on any character" armed it. The one item not in front of the lead (7.2's click 3, owed since 7.2) was routed rather than self-scored. It cost one short lead reply (*"close it without click 3, then push"*) and left the override on record, quoted in the `🎉` commit.
- **`ALREADY ROUTED`** kept the two items the lead had just seen in the 7.6 handback (the Blender cut-out control and the carrier-gate coverage) from re-blocking the close. Run 2's retro flagged re-asking an unanswered `YOUR CALL` five times; this path is what avoided a sixth.
- **"Re-measure a COUNT before restating it."** I wrote "24 candidate articles" into `PlatformDependencies.md` from memory, re-measured on the next action (it's 19; 23 including four older articles) and fixed it before commit.
- **"Read what SELECTS a gate's subject."** Reading `check_lcd_carrier.py`'s selector (`in LCD_PORTS`) showed the new `cutout_map` is invisible to it. Measuring why widening isn't a one-liner (usdMtlx leaves the empty default unauthored) turned it into a well-formed offer instead of a silent gap or a hasty gate edit.
- **"Probe first", with a discriminating variant folded in.** The Brief's probe question was one render. Adding a third render (`texcoord index 1` over an authored `st1`) cost ~30 s and found that Storm reads `st` for every index, which decided the contract's UV rule before any code (Learnings S9).
- **Read-back after every commit (`git show --stat`).** It confirmed the `git mv` rename committed the finalized blob, not the pre-finalize one.
- **A lead-available sitting per step.** 7.6 went build → one sheet → *"close enough"* in a single round.

## Dead weight

None.

## Open questions

1. **Is CI parked by choice, or is it a missing runner?** (Lead decision, not a Refiner tweak.) `gate.yml` is active on push, yet no run has been created since 2026-09-23. If CI is meant to run, a runner or setting is missing; if it is parked, item 1's `LOCAL_DELTAS` row is the fix.
