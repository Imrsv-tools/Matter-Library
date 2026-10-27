# Workflow Feedback — P23 / execute / resume

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P23` (Synthetic Skin Sets) |
| **Mode** | `resume run 2`, ending in a suspend-handoff (not a continuation of `261027_P23_Execute_ColdStart.md`: a separate session, resumed at 23.2.6) |
| **Outcome** | `suspended` — the face's placed regional colour (`84a2140`; the lead: *"III is closer, now fix the under-eye ring"*) and the under-eye ring (`9494870`; *"Yes... III new: the under eye ring is better..."*). The rest of 23.2 and all of 23.3 planned in the phase doc (`9c2d4f3`, `c8a727a`). |
| **Shape** | `behavior-touching` (the skin maker, six articles, their maps) |
| **Confidence** | Ran fully: BUILD, TRY (two sittings, both sat), the suspend ledger. **Not exercised:** the rig's three-tool sheet, 23.3, the close. |
| **Date** | 2026-10-27 |

---

## Items, ranked

### 1 — A multiplier zeroed the feature, and three solve-and-render rounds went into its shape before its final weight was read `[self-error-doc-could-prevent]`

**Grounding.** `face_regions` multiplied every face region by MPFB's face mask, which is near 0 around the eyes. The under-eye ring kept 0.04 of its shape. Signals I had and did not read as a fault in the instrument:
- the solver drove the ring to its clamps (blood ×e^1.2, depth 0.5);
- the region's own average went dark (0.76 / 0.83 / 1.00) while the profile across it stayed flat (ring ÷ below 0.96 / 1.01 / 0.99).

Before that I spent three rounds moving and resizing the shape: an ellipse, a band around the opening, then a tear trough and a crescent. That was about 40 minutes of solves and 8-minute look renders. A two-line check (the raw shape against the final weight, inside the band being measured) found it: 0.69 raw against 0.04 final.

**Proposed fix.** In `execute.md` §Verify, the row *"a parameter that should matter and barely moves the reading indicts the instrument before the subject"*, add: *"So does a solver whose parameters sit at their clamps. Before you change the shape or the target, read the FINAL weight of the thing you are tuning inside the band you are measuring. A multiplier upstream can zero it."*

**Where it'd live.** `execute.md` §Verify before edit (the ad-hoc check / sensitivity row).

---

### 2 — The previous run's item 1 recurred in a new form: region averages matched while the gradient that MAKES the feature did not `[self-error-doc-could-prevent]`

**Grounding.** `261027_P23_Execute_ColdStart.md` item 1 (a band-pass statistic matched, the look didn't) is still in the inbox. This run solved each face region's *average* colour to the bar's same region, and every average matched within 0.1 in log. The ring still did not show. The bar's ring is a **gradient** straight down from the eye: darkest 2–12 mm below the centre, 0.3 lighter (log) by 17–20 mm. Ours was flat across it, because a region average blends the dark band with the light skin below it. Solving the ring on that gradient (the 2–12 mm band against 16–23 mm) drew it in one solve.

**Proposed fix.** The same entry as that retro's item 1, with this form beside it: *"Match the contrast that makes the feature (the band against its surround, the profile across it), not the feature's average. An average can be right while the feature is absent."*

**Where it'd live.** With `261027_P23_Execute_ColdStart.md` item 1: memory `look-work-build-the-full-set`, or `execute.md` §Verify.

---

### 3 — Judge placement on the body, never in the atlas: the lead's placement grid settled in one render what two atlas views had confused `[doc-gap]`

**Grounding.**
- I checked the face regions on atlas (UV) crops. hm08's eye region is badly distorted there, and I misread the crop's orientation twice.
- Mid-run, the lead: *"We might want to consider a test body grid as well taht we can map on a body and apply to troubleshoot or so more accureat placement... (screenshot waht is actaully applied)"*.
- `look.py --reference <picture>` already draws any atlas picture on the body. So a 1 cm / 5 cm grid in 3D, with the regions tinted, rendered in the look view with no new tool. It showed every region where it was meant to be, which pointed at weight (item 1), not placement.
- A render-space difference against the bar, from the same camera, then showed exactly where ours was too light: the ring and the upper crease.

**Proposed fix.** A Learnings entry: *"To check where a map feature lands, paint a debug picture (a 3D grid, the shapes tinted) and render it through `look.py --reference`. To find where a look misses a reference, take the log-luminance difference of the two renders from the same camera. Never judge placement in the atlas."* The lead's library-level version (a character test surface) is in the phase's Deferred table, for the lead to order.

**Where it'd live.** `docs/Learnings/` (the parity / Unreal domain). Possibly `LOCAL_DELTAS.md`'s "artifact a person reaches" row as a debugging aid; the Refiner's call.

---

### 4 — The first click came at about 2 hours; the floor of the loop was an 8-minute look render, and the session spent nine `[self-error-doc-could-prevent]`

**Grounding.** The target is 60–90 minutes to the click. The fast loop I chose, the atlas crops plus a scratch solver at about 20 s an iteration, answered colour questions in seconds, but it could not show placement (item 3). So every placement question cost a full look launch: III, IV, V and the bar, about 8 minutes. The first handback said so as a scope alarm (loop too slow).

**Proposed fix.** None beyond item 3: the grid render would have been the right first loop for placement, ahead of the atlas. Recorded for the tally of *"the click surface used as the tuning loop"* (the previous retro's item 2): the look view is still the only true surface, so the loop question is how few launches it takes.

**Where it'd live.** With item 3, or the previous retro's item 2.

---

### 5 — A `cd` at the start of one command, against the standing ban `[self-error-doc-could-prevent]`

**Grounding.** One `python3 - <<'EOF'` edit of a scratch file began with `cd /home/peter/.claude/jobs/fa45dac8/tmp 2>/dev/null;` from habit. The harness moved the session's working directory. Nothing broke, because every other command used absolute paths and `git -C`. I said so in chat when it happened.

**Proposed fix.** None to the docs: the rule is clear and in `.claude/CLAUDE.md`. Recorded for the tally only.

**Where it'd live.** Nowhere new.

---

## Keep these

- **Measure the reference region by region before building** — it reversed the diagnosis in the first ten minutes: the bar's face is lighter and cooler than its trunk, ours was darker and warmer.
- **`execute.md`'s "a parameter that should matter and barely moves indicts the instrument"** — it is what finally sent me to read the weight (item 1). It fired late; it fired.
- **Per-fit tables, following `DETAIL`'s precedent** — they let IV's fit take the same regions at half the contrast without a new mechanism.
- **The private reference rule (RD-P23-10), grepped on the diff before every commit** — four commits, 0 hits each time.
- **Read the sibling's landed commit before your own** (`bec3056`, P32, one file, disjoint) — cheap, and it kept my explicit-path commit clean.
- **Verify a ledger claim before the commit that carries it** — I wrote "18/18 PASS" into a row while the gate was still running, and read the gate's result before committing.

## Dead weight

None.

## Open questions

1. **The character test surface** (the lead's grid idea, in Phase23's Deferred table): a phase or a `/quick-fix`, the lead's to order.
2. **`LIPS["III"]` and the darker tones' lips:** III's fit (I, II, III) now takes the bar's measured lips; IV's (IV, V, VI) keeps Phase08's rule. That split is the agent's judgement, not the lead's ruling, and the lead has not judged IV and V's lips. Worth one look at 23.2.12's sheet.
