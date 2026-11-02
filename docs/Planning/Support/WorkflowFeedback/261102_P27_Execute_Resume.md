# Workflow Feedback — P27 / execute / resume

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P27` |
| **Mode** | `resume run 2` (`ML_P27_E2`, from `8bb46f8`) |
| **Outcome** | `derailed` — 27.2's seams built and measured at the skin's own variation (`f412593`); click 2 ended on the premise: the lead saw "no effect at all... or an obvious [line]", and the source turned out to hold half the atlas's detail |
| **Shape** | `behavior-touching` |
| **Confidence** | Ran fully: build, the seam instrument, the judge render, one sitting, the verdict record. **Not exercised:** the close, a push, a runtime. |
| **Date** | `2026-11-02` |

Not a continuation of `261102_P27_Execute_ColdStart.md` (that was `ML_P27_E1`, 27.1); a distinct resume run.

---

## Items, ranked

### 1 — The click asked a narrow question (the seams) of a candidate nobody had checked was different from the control at all `[self-error-doc-could-prevent]`

**Grounding.** 27.2's click asked "can you find the seams?" at the neck, wrist and ankle, C beside D. Before the sitting I measured the seam steps against their control, the cut steps, and looked at every view for lines. I never measured whether D *differs from C* in those views. The lead: *"none look correct"*, then *"Either no effect at all... or an obvious [line]"*, then *"almost no deffernce at all on the hand"*. One measurement after the sitting (fine detail, D/C 0.85–0.99 in every view) showed D carried *less* detail than C. The cause was a dated Brief fact: F-P27-4's ~0.9 mm a pixel was for a ~2 MP full-body picture, but the route taken (four views in one 1968 × 1152 picture) is 1.67 mm. `execute.md` §TRY already says *"Then ask whether the CHANGE can show: measure ... against today"*. I read it as "can the seam change show" and measured the seam, not the candidate. The judge's whole purpose (D against C) went unmeasured.

**Proposed fix.** In §TRY's "can the CHANGE show" sentence: *"When the click's question is narrow (a seam, an edge, a single defect) and the views show a candidate beside its control, first measure that the candidate differs from the control at all in those views. A lead looking at two columns judges the difference before the question."*

**Where it'd live.** `execute.md` §TRY (portable).

---

### 2 — The always-on "typecheck, lint, format" gates have no local meaning here `[doc-gap]`

**Grounding.** `execute.md` §BUILD: *"BEFORE THE FIRST COMMIT OF A STEP, RUN THE REPO'S ALWAYS-ON GATES — typecheck, lint, format"*. This repo has no lint or format config. `ruff check` with its defaults flagged dozens of house-style lines the committed code already has (`noqa: PLC0415`, import order, a shebang). I had to decide on the spot that `run_all.py` is the only always-on gate.

**Proposed fix.** A row in the translation table: *"the repo's always-on gates" = `run_all.py`; there is no lint, format or typecheck config (dated); ruff at its defaults is not a gate here.*

**Where it'd live.** `LOCAL_DELTAS.md` (port gap).

---

### 3 — A one-off `cd` slipped into a scratch heredoc command `[self-error-doc-could-prevent]`

**Grounding.** One Bash call began `cd /dev/null 2>/dev/null; python3 - <<'EOF'`. It was a reflex, harmless only because `cd` into a file fails. `.claude/CLAUDE.md` bans `cd` in every mode. The rule is clear; this is noted only so the refiner can count recurrences.

**Proposed fix.** None beyond counting. If it recurs across runs, add the heredoc shape (`python3 - <<'EOF'` with no prefix) to the `cd`-free forms list.

**Where it'd live.** `.claude/CLAUDE.md` §Codebase search, the `cd`-free list (only if it recurs).

---

### 4 — A global levelling solve with a weak anchor moves everything toward one strongly held source `[doc-gap]` (a learning, not method)

**Grounding.** Holding Phase25's head fixed in the per-view seam levelling (weak anchor 1e-3 elsewhere) lifted the whole body 25 % and then 50–100 %. Every cell was past the cap, and the view steps came back. A local split ramp at the boundary (half each side, 6 cm, by distance on the body) fixed the neck without moving the body (body/C 1.00).

**Proposed fix.** A learning: *"to join a new source to a fixed one, don't add the fixed one to a weakly anchored global solve; measure the step on the boundary and ramp it locally on both sides."*

**Where it'd live.** `docs/Learnings/` (an image-processing or skin domain; none exists yet, so the refiner decides).

---

## Keep these

- **Instrument first, with a control that can fail** (`execute.md` Verify-before-edit, the ad-hoc check row). The seam measure read 1–2 % on the maker's map before I trusted it on D. Adding a same-side control turned "5 % on the back cut" from a defect into the skin's own variation. That saved a wrong fix.
- **"A reading that disagrees with the picture indicts the instrument"** — the 40 % neck p90 with a ±0.5 log spread made me look, and the picture showed Phase25's carried band.
- **Re-ask the loop when it changes character** — a CPU orthographic close-up render (seconds) carried every neck, wrist and ankle iteration. The Unreal judge ran only twice.
- **Ask once for the GPU while Studio runs** — one question, one "go ahead", no per-run asks.
- **A verdict that rejects the premise ends the act** — recorded verbatim with the reading beside it, measured once, and the run stopped instead of tuning.

## Dead weight

None.

## Open questions

1. Whether 27.2's seam work (`f412593`) survives a new body source is the next discovery's question (`ML_P27_D2`, started from this retro). It should: the joins are built for any picture projected through the four views. Not a refiner item.
