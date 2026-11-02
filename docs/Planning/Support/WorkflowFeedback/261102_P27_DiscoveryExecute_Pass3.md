# Workflow Feedback — P27 / discovery → execute / Pass 3 + resume

| | |
|---|---|
| **Verb** | `discovery → execute` (one session: discovery Pass 3, then the lead's `/execute Phase27` in the same session) |
| **Unit** | `P27` |
| **Mode** | discovery Pass 3 (reopened after 27.2.2 ended on the premise) · execute resume from 27.2 |
| **Outcome** | `done` for the act — the fine skin built (27.2.3), the original beside the character shown and sat (27.2.4: the lead, "that is looking good"); next session `ML_P27_E3` started on the lead's yes |
| **Shape** | behavior-touching (`tools/converters/fit/project_body.py close`) |
| **Confidence** | Ran fully: discovery (probes, two lead questions, Brief rewrite), execute (build, gate, look view, a sitting). **Not exercised:** the close, the structure step. |
| **Date** | 2026-11-02 |

*Not a continuation of `261102_P27_Execute_Resume.md` (that is `ML_P27_E2`'s); a distinct session, `ML_P27_D2`.*

---

## Items, ranked

### 1 — A measurable proxy replaced the lead's reference look, for two hours `[self-error-doc-could-prevent]`

**Grounding.** The lead had judged a reference as the goal at Pass 2 (`f4_s50_seed7.png`, "that one looks really good"). After 27.2.2 ("no effect at all") this session framed the problem as *fine detail*, measured high-pass numbers through discovery Pass 3 and execute 27.2.3, and handed back "×1.01–1.09, click not called" with an A/B question. The lead: the target is the original AI output's look on the character mesh; they did not know what they were being asked to look for. One picture — the original's back view · the character now · the character with the fine skin, same angles — got "Now we are talking.. that is looking good!" at once. That picture was never built before the lead asked for it.

**Proposed fix.** *"Where the lead has judged a reference as the goal, every look step's first evidence is that reference beside the result, at the same angles, in one picture. A number (detail, fit, a correlation) is supporting evidence for that picture, never the question put to the lead."* `discovery.md` §First human test already says "name the reference and say whether this step closes the gap toward it" — it was named, and then the run measured something else.

**Where it'd live.** `execute.md` §TRY (beside "measure, in the exact pictures the lead will see, the difference the click judges … against the reference the lead has accepted") · `discovery.md` First human test.

---

### 2 — "Below a glance, report the number instead of calling the sitting" stopped a sitting the lead wanted `[doc-gap]`

**Grounding.** 27.2.3 measured the fine skin at ×1.01–1.09 in the judge views and, per `execute.md` §TRY, did not call the sitting — it asked a fork instead. The lead's next message: "show me the fine skin if you want feedback… the main thing is that it reads as a complete character". Shown, it passed.

**Proposed fix.** The rule holds for a click whose *only* question is the change. When the click's question is the reference look (item 1), show the one picture anyway and say in a line "the change itself is small (×1.05); the question is whether it reads as the original". Never replace a sitting with a fork the lead cannot judge without the picture.

**Where it'd live.** `execute.md` §TRY.

---

### 3 — A heated lead message went verbatim into a public phase doc `[self-error-doc-could-prevent]`

**Grounding.** Following "record a ruling in the lead's own words", the run pasted the lead's frustrated message (with swearing) into `Phase27_AiBodySkin.md`. The lead: "DO NOT PUT STUFF LIKE THAT DIRECTLY IN THE PHASE... understand what I am saying and put in notes". Fixed by amending the run's own unpushed commit (`0f0c281` → `41fad21`) so the text is in no history; memory `notes-not-raw-quotes` written.

**Proposed fix.** In `AI_WorkingAgreement.md` §Record a ruling: *"Verbatim is for a ruling. A message that vents, or mixes direction with frustration, is recorded as a note of what it asks — never pasted. The repo is public."*

**Where it'd live.** `AI_WorkingAgreement.md` §Working With the Lead · `discovery.md` (which restates the verbatim rule).

---

### 4 — Lead-facing questions used the run's own labels `[self-error-doc-could-prevent]`

**Grounding.** Handbacks asked about "column 2/3/4", "split at 3 mm", "the close camera", "D_seam9", "18 cameras". The lead listed them back as noise ("skin d, skin a, four view skin… camera 6"). The plain-words rule exists (`AI_WorkingAgreement.md`, "any id or method word… say what it means"); it was not kept under pace.

**Proposed fix.** None new — a tally for the existing rule. Possibly: *"before a look question, write the one sentence of what to compare in the lead's terms first; if it needs a label you invented, the question is not ready."*

**Where it'd live.** tally only.

---

### 5 — `/retro` step 0's launch shape invites a `cd` `[doc-gap]`

**Grounding.** Step 0 says `claude --bg --name <name> "<command>"`. This run prefixed `cd <repo> &&`, which `.claude/CLAUDE.md` bans in every command. Harmless (the session's own root), but a violation the step's wording did not prevent.

**Proposed fix.** In `retro.md` step 0: *"it starts in this session's working directory, which is the repo root — no `cd`."*

**Where it'd live.** `retro.md` (portable).

---

### 6 — Discovery handed to execute in the same session at ~310k without the offer `[self-error-doc-could-prevent]`

**Grounding.** `discovery.md` §Hand-off: past ~250k at BRIEF READY, offer a fresh session. The lead typed `/execute Phase27` here and the run went on from ~310k; it ended at ~410k, with the build, two look-view runs and a sitting squeezed. The offer was not made.

**Proposed fix.** None new; when the lead's next verb arrives in a session already past 250k, say once: "I'm at ~Nk — start it fresh?" before step 1.

**Where it'd live.** tally (`discovery.md` §Hand-off).

---

## Keep these

- **One picture per stop, the question naming each column** — two Pass 3 questions answered in one line each ("2 is the closest to image…", "3 looks more real, marks are right").
- **Messaging the live sibling at kickoff** (`ListAgents` / `SendMessage`) — `ML_P27_E2` replied with its scratch tools, the seams' centres and the shoulder-dot state; nothing collided on the phase doc.
- **"Look at the output before reading the number"** — caught that `P27_Body/C_3d594fb.png` is not C's colour (it rendered pale grey) before any finding rested on it, and caught the render-crack line before it reached the lead.
- **Probe in scratch, scripts tracked repo-relative** — `region.py` re-ran to the same numbers from the repo.
- **Amend only an unpushed commit that is your own top** (`merge-base --is-ancestor`, `rev-parse HEAD`, `diff --cached` first) — made item 3's fix clean.

## Dead weight

None.

## Open questions

1. Whether the fine skin's settings (2 mm, a ±8 % cap) stay once the gap to the original is closed — `ML_P27_E3`'s to judge on the same side-by-side; not a Refiner item.
