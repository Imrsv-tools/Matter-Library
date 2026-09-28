# Workflow Feedback — P08 / execute / resume run 3 + close

| | |
|---|---|
| **Verb** | `execute` (then `execute_close`, in the same session, on the lead's *"close"*) |
| **Unit** | P08 |
| **Mode** | resume run 3 (8.4 from the second hand-off), then close, then push |
| **Outcome** | done — 8.4 (five fabrics, click 6 passed), the close (`b0fcbee`) and the push |
| **Shape** | behavior-touching (a texture generator, 5 articles, the Blender library) + doc-only close |
| **Confidence** | Ran fully: `execute` §BUILD/§TRY for one step with two sittings, `execute_close` rows A⁻ to E. **Not exercised:** `execute_repair.md`, high-rigor, the issue-close coda (no source issues), row B⁺ (not a Wave). |
| **Date** | 2026-09-28 |

*A distinct run, not a continuation.* `260928_P08_Execute_Resume.md` is the previous session's (run 2); I read it and `_RefinementBacklog.md` first, and file only what they do not already hold.

---

## Items, ranked

### 1 — At the close I wrote a count I had not measured into the CLOSE entry `[self-error-doc-could-prevent]`

**Grounding.** Drafting the CLOSE — DONE row I wrote *"37 new or changed articles across the phase"*. No command produced it. I caught it before committing and measured it (`git diff --name-status de08ccc HEAD -- MatterLibrary/materials`: **21 added, none changed**; 35 + 21 = the library's 56). `execute.md`'s verify-before-edit row covers restating a count that **a doc or a prior run** asserts. `execute_close.md` row A covers grepping the `🎉` body's **completion** claims. Neither covers a number the closer **composes** while summarising, which is exactly when summarising pressure is highest.

**Proposed fix.** In `execute_close.md` row A, beside *"Grep your own 🎉-body completion claim"*: **"and every NUMBER in the CLOSE entry and the `🎉` body (articles, files, steps, commits) names the command that produced it, or is measured now. A close summarises, and a summary is where counts get composed rather than read."**

**Where it'd live.** `execute_close.md` row A.

---

### 2 — The rig's seam check flags any periodic structure whose boundary lands on the tile edge; it fired falsely twice, and a shipped texture has the same flag latent `[doc-gap]`

**Grounding.** The canvas sheet said **`SEAM`** on its normal map (wrap edge 3.7 vs neighbours 0.9). I measured interior thread borders at 3.8–7.3: the tile edge simply fell on a thread border, and the check compares it to the average neighbour, which is mostly mid-thread. I shifted the weave half a thread (`half_thread()`, `c11693b`). The stretch knit then flagged `SEAM` too (7.56), for the same reason along the courses. The **shipped** `Cotton_Jersey` has the identical crease (4.61 at the edge and at every interior border). It has just never been swept, so it has never been flagged. This is the backlog's *"an instrument that cannot see the thing"* family, inverted: an instrument that **sees a thing that is not there**. It cost two diagnoses, and the second flag stays on a passed article's scorecard.

**Proposed fix.** Two, the lead's to pick. **(a) A learning** (the tool's quirk; no gate change): *"The rig's seam line compares the wrap edge to the average neighbour. On a periodic texture, compare it to an interior boundary at the same phase before reading it as a seam; generate woven sets so the tile edge runs mid-thread."* **(b) A tool change** to `rig.py`'s seam measure: compare against the interior column or row one period away, not the average neighbour. That touches a measuring tool, so it needs a ruling.

**Where it'd live.** A `docs/Learnings/` entry (no domain fits cleanly: MaterialX? a new `Rig/`?), and (b) is an open question below.

---

### 3 — Recurrence: the Brief named a sitting surface that could not show the property. The scale sentence in §TRY caught it in time `[doc-gap]`

**Grounding.** The Brief said click 6 is *"judged on the article sheet, not on outfits"* (RD-P08-4). The rig's close-up is ~15 px per cm and canvas has 16 threads per cm, so a thread is one pixel: the sheet showed a flat ecru cube. **`execute.md` §TRY's sentence ("ask whether the surface's SCALE … can show the thing … a 1 cm grain is one pixel in a wide shot") fired before the sitting**, and I built a close-camera scene in the lead's Blender instead. The lead then judged it there (*"The texture looks amazing"*). This is the third P08 instance of the fixture-can't-show family (the earlier two are in `260928_P08_ResearchDiscoveryExecute_ColdStart.md` item 2 and `260928_P08_Execute_Resume.md` items 2–3). What is new: **this time it was written into the Brief at discovery**, a plan-time error, and the executor's rule is what caught it.

**Proposed fix.** The same scale question at plan time. Where `discovery.md` / `plan.md` have the Brief name its first human test, add: **"For each click, name the surface and check that its resolution can show the feature (feature size ÷ the surface's size per pixel ≥ a few pixels). A sheet built for colour cannot judge a weave."** This is the upstream end of the existing §TRY sentence, not a new rule.

**Where it'd live.** `discovery.md` / `plan.md` (the Brief's First human test), pointing at `execute.md` §TRY.

---

## Keep these

- **`execute.md` §TRY "ask whether the surface's SCALE can show the thing"** — it caught item 3 before the lead saw a useless sheet.
- **`execute_close.md` row B's `git mv` warning** — `diff --cached --stat` showed the rename staged with **0 changes** (the pre-finalise blob); re-staging the moved path explicitly put the finalise into `b0fcbee`, and `git grep 'COMPLETE (closed' b0fcbee` confirmed it in the commit.
- **Walking one act before batching** — canvas alone first, then the four others together. The first verdict (*"the tint looks correct"*) settled the approach, so the batch passed in one reply (*"they all pass,"*).
- **`.claude/CLAUDE.md` stating the no-co-author rule once, always loaded** — the harness's attribution reminder said to add a trailer; the always-loaded override won, with no verb doc needed.
- **A0's arming question at the top of the cell** — answered in one line (armed: "any colour"), then the four dispositions (fix, rule, route, already routed) mapped the ledger without re-reading the ~900-word cell.
- **"Compare the SET, not the tally"** — the gate went 14 / 2 / 1 with `approval_binds_freeze` named each time, never a bare count.

## Dead weight

None.

## Open questions

1. **Item 2(b) — fix `rig.py`'s seam measure, or only record the learning?** A lead call: it changes a measuring tool, and the latent flag on the shipped `Cotton_Jersey` is untouched either way. My recommendation: the learning now; change the measure the next time a fabric is swept.
2. **Where do rig and tool quirks live in `docs/Learnings/`?** The domains are Blender, MaterialX, Storm and ClaudeCode, and none fits the rig's own measures. Refiner or lead.
