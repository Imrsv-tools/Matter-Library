# Workflow Feedback — P05 / Execute / ColdStart (through the close)

| | |
|---|---|
| **Verb** | `execute` (stages 2–4 for all five steps, then `execute_close.md` in the same session on the lead's "close") |
| **Unit** | `P05` — Test Rig: Blender and USDLiveView Side by Side |
| **Mode** | cold start → close (one session, 2026-09-26 → 27) |
| **Outcome** | done — 🎉 `40e3087`, pushed (`5b367b2..40e3087`); one maintainer re-approval owed |
| **Shape** | behavior-touching (new tools, Blender masters, assembler fix, 9 articles re-assembled, pilot re-frozen) |
| **Confidence** | Ran fully: `execute.md` Build/Try/Strengthen with a present lead (5 sittings), `execute_close.md` rows A⁻, A0, A, B, D, E. **Not exercised:** `execute_highrigor.md`, `execute_repair.md`, B⁺ (not a Wave), C (not issue-sourced). |
| **Date** | 2026-09-27 |

---

## Items, ranked

### 1 — I asked the lead a question the project's own purpose answers; he had to restate the purpose `[self-error-doc-could-prevent]`

**Grounding.** At 5.2 I found the assembler builds every article's normal in the wrong space (F10). I put it as a `⛔ YOUR CALL`: "fix at the source, or copy the MaterialX maths into Blender faithfully and record the defect". The lead answered twice:

- first, "are we not on the current MaterialX path? Is there a version issue";
- then: *"I am not sure why this is a question then so maybe I need to restate the point of the entire IMRSV project … so we can make the correct test articles so we can create the correct materials … and they look right"*.

The Readme's first line settles it: the `.mtlx` is the single source of truth, "author once, render close to the same everywhere". A wrong article gets fixed; there was never a fork. I asked the same kind of question again (fix the preview lights?) and he had to answer it too. The Brief's own "Decisions that bind" line, *"a slider's math is MaterialX's"*, read literally, is what made copying look like a legitimate option.

**Proposed fix.** Add a test to the `YOUR CALL` entry gate: *"Before asking, re-read the project's one-line purpose. If one option leaves a defect in the single source of truth, it is not a product fork. Fix it and say so."* And a divergence-table row: **a binding decision read literally can protect a defect** ("copy the article's maths" vs "the article is wrong"); apply the purpose, and surface the tension in one line instead of asking.

**Where it'd live.** `AI_WorkingAgreement.md` §Working With the Lead (the `YOUR CALL` gate) + `execute.md` §Divergence. Portable.

---

### 2 — A comparison between two degenerate sides "agrees" by construction; four times this run a check passed on nothing `[doc-gap]`

**Grounding.** `execute.md` has *"Confirm it can fail"* for ad-hoc checks. That covers a check that matches nothing, but not a comparison where both sides are saturated or empty:

- **Neon** scored 0.09 ΔE, "under the bar", because both tools clipped it to pure white. Fixed with a −4-stop view.
- **Near-white plastic** clipped at the rig's first light level, so both tools "agreed" on flat white. Fixed by halving the lights.
- **A UV-name probe** found equal texture variation with the right and the wrong UV name, because a flat colour still varies with shading. Only rendering the UVs as emission showed the wrong name gives (0, 0).
- **An old-versus-fixed normal probe** on the cube's front face showed no difference, because on that face tangent space equals world space. I first read it as "the fix does nothing".

Each cost a turn or a wrong conclusion. The earliest one, the scene's lights contributing nothing, hid for months in the preview tool, because a headlight made every render look lit.

**Proposed fix.** A `Verify before edit` row: *"You are COMPARING two outputs (two renderers, before and after). Check each side has dynamic range first: not clipped, not flat, not a case where the two can't differ. Agreement between two saturated or degenerate sides is agreement by construction."*

**Where it'd live.** `execute.md` §Verify before edit. Portable. The stack-specific cases are already in `docs/Learnings/{Storm,Blender}/`.

---

### 3 — The first sitting's surface couldn't show what the click was about; the "what am I looking at" line was missing `[doc-gap]`

**Grounding.**
- **Click 1:** the lead replied *"I see a grey sheet and a colored background"*. My ▶ line gave numbers and paths, not what to compare. I had to follow up: "the first two panels are the same scene in two tools, do they look the same?"
- **Click 3:** *"the resolution is quite low for me to see bumps or dust"*. A 1 cm dust grain was about 1 px in the wide shot. The fix was a close-up camera, and it then exposed a real content finding (F11).

`execute.md`'s fixture-distribution row asks what the seed data makes impossible to see. It does not ask what the viewing distance or resolution makes impossible to see, and that is the axis that bit.

**Proposed fix.**
1. In §TRY: *"The ▶ line says in ONE sentence what to compare by eye, and what 'right' looks like."*
2. Extend the fixture row: *"…and whether the surface's SCALE (resolution, viewing distance, exposure) can show the thing the click is about."*

**Where it'd live.** `execute.md` §TRY. Portable.

---

### 4 — The lead copied a trailing comma out of the ▶ line, and the command failed `[self-error-doc-could-prevent]`

**Grounding.** The ▶ line read "Run `uv run tools/parity/rig.py GreyCard_…_v01`, then open …". The lead pasted `…_v01,` and got "no article named". I made the rig strip stray punctuation, which was a real fix, but the cause was the message format.

**Proposed fix.** *"A command in a handback goes on its own line, in a code block, with nothing after it."*

**Where it'd live.** `AI_WorkingAgreement.md` §Working With the Lead (format). Portable.

---

### 5 — Close row A0 has no disposition for an item found WHILE carrying out the lead's close instruction `[doc-gap]`

**Grounding.** The Outcome's *"Every disagreement is either fixed or written down with its cause"* armed A0. F12 was cleanly `ALREADY ROUTED`: it was stated in the handback the lead answered with "fix marble, then close". But fixing Marble, which the lead asked for as part of that same instruction, surfaced F16 (Marble's colour mix). F16 was never in front of the lead, so `ALREADY ROUTED` doesn't apply. It was written down with its cause, so it isn't an open deferral either. Strictly, "route it and block" would re-ask about work the lead had just told me to finish and close. I disclosed it in the 🎉 body and the handback, and inferred that this was allowed.

**Proposed fix.** In A0 §(3): *"An item surfaced while executing the lead's own close instruction (e.g. 'fix X, then close') is disposed like ALREADY ROUTED, provided it is written down with its cause, named in the close handback, and quoted in the 🎉 body."*

**Where it'd live.** `execute_close.md` row A0. Portable.

---

### 6 — `LOCAL_DELTAS.md`'s "the way this project is RUN" row is stale, and names no Blender instrument `[doc-gap]`

**Grounding.**
- The row says *"Measured 2026-09-23: `run_all.py` fails at import (no MaterialX Python module on the lead's box)"*. Phase02 fixed that, and `run_all.py` ran fine all run.
- It lists no way to *see* a material, which is now `tools/parity/rig.py`.
- At click 5 the lead's sliders were greyed out. One read-only call through the Blender MCP, set up at discovery but recorded only in the phase doc, found the cause at once: the library had imported "Pack", which links the material read-only. Without it this would have been a guessing round-trip.

**Proposed fix.** Refresh the row: *the gate runs; `uv run tools/parity/rig.py <article>` is the side-by-side picture; the Blender MCP (listens on localhost:9876 when Blender is started with `--online-mode`) can inspect the lead's live Blender during a sitting.*

**Where it'd live.** `LOCAL_DELTAS.md` (Refiner's lane; genuinely local).

---

### 7 — Time to first click was far over target: an inherited defect displaced the first step `[doc-gap]` (minor)

**Grounding.** 5.1 exceeded 60–90 minutes. The time went on diagnosing why Storm's scene lights did nothing (S1–S3 in `docs/Learnings/Storm/`), a defect inherited from the preview tool. `execute.md` says to name which scope alarm fires, and I did: "supporting work displaced the first step". It was the right call, because the rig couldn't claim "same light" without it, and it paid back all phase.

**Proposed fix.** None needed. Recorded so the Refiner has a data point that a Brief's reuse row ("reuse `make_preview.py`'s scene") can import a latent defect into the critical path. Discovery could have caught it by probing the reused tool with its headlight off.

**Where it'd live.** unsure (`discovery.md`'s reuse-check probes?).

---

## Keep these

- **"Ask whether the lead is available" plus act-by-act sittings.** The lead drove all five clicks. Two defects (the sheet's scale, greyed sliders) and one product ruling (faint wear → Phase08) came only from him using it.
- **"Whose defect is this?" is a measurement.** `git grep` at the phase-start commit proved both inherited reds (`approval_binds_freeze`, the `check_lcd_carrier` import crash) in seconds. Neither was misattributed in a commit.
- **Baseline before changing a generator.** Proving all 17 recipes reproduce their articles byte for byte *before* touching the assembler made the 8-article diff attributable to the fix alone.
- **Explicit-path staging + `git show --stat` read-back.** A sibling session committed and pushed four times during this run, including a re-sequence touching my phase doc. Nothing collided, and I noticed rather than reconciled.
- **Gates are frozen.** I wrote no new gate; the probes lived in the ignored `library/parity/_probe/`, and the rig is a tool. That kept the scope honest.
- **The close's "read the Goal verbatim" plus A0.** It caught that "every disagreement … written down with its cause" needed a real ledger, not a ✅ list.

## Dead weight

None.

## Open questions

1. **Should the rig's scorecard become a gate** (e.g. graded masters < 2 on every row)? `execute.md` freezes new gates, and I didn't ask. It's worth a lead ruling at Phase08, which owns the nightly/automatic run. *Lead decision.*
2. **F12 (bump strength) and F16 (Marble's colour mix)** are recorded for Phase06's Unreal column to arbitrate. If Unreal sides with Storm, the Blender master (for F12) or the OpenPBR colour-mix mapping (for F16) is what changes. *Tracked in the Phase05 doc; no Refiner action.*
