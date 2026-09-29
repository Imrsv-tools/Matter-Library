# Workflow Feedback — P06 / execute / resume run 4 + partial close

| | |
|---|---|
| **Verb** | `execute` (then `execute_close`, entered on the lead's *"THEN CONTINUE!"*) |
| **Unit** | `P06` |
| **Mode** | resume run 4 → close (partial: the 🎉 held for a sitting on another machine) |
| **Outcome** | suspended at the close's last human gate — 6.5 ✅ (click 5), 6.2's publish done (`unreal-runtime-v1`, pinned, verified by a pinned download), D9 built at the close, the docs list landed; the move and 🎉 wait on click 2 (+6) on the other machine |
| **Shape** | behavior-touching (driver, Unreal masters, the rig's verdict) + docs |
| **Confidence** | Ran fully: Build → Try → Strengthen for 6.5, one lead sitting, a package build + public publish, close rows A⁻–A (doc-conform, deferral ledger) and the pushes. **Not exercised:** close rows B–D (move, Roadmap, 🎉), Blender (this machine cannot render parity), the other machine. |
| **Date** | 2026-09-30 |

*A distinct run from `260929_P06_Execute_Resume3.md` (run 3), not a continuation.*

---

## Items, ranked

### 1 — My `▶` lines kept asking the lead to authorize acts that were already done, and the lead could no longer tell what state the world was in `[self-error-doc-could-prevent]`

**Grounding.** After *"THEN CONTINUE!"* I pushed, published `unreal-runtime-v1` and pushed the pin. The close handback then ended `▶ Push the three close commits`, as close row E prescribes (*"stop and ask before pushing"*). The lead answered *"commit and push and we need to get v1 published"* — v1 had been public for an hour — then sent *"publish"* on its own. I asked what they meant, and they replied: *"YOUR PROMOT keeps saying to tell me to tell you to publish.... so it's all published and pushed?"* Three round trips spent re-establishing state. The handbacks did say "published", but only in the middle of prose, while the `▶` — the one line the lead acts on — was an ask for another publish-shaped verb.

**Proposed fix.** In `execute.md` §Handback (and close row E): *"When the run has done outward acts (push, publish, a release), open `Done` with a STATE line — `pushed: <range> · published: <tag> · unpushed: <n commits, or none>` — and never phrase a `▶` so that it reads as asking for an act already done. **A lead's go-ahead that answered a list naming the push also covers that push:** do it and report it; do not re-ask at row E."*

**Where it'd live.** `execute.md` §Handback; `execute_close.md` row E.

---

### 2 — A Brief's "In now" item had no step, and four runs never built it; only the close's code read found it `[doc-gap]`

**Grounding.** The Brief's §In now reads *"The rig's verdict becomes the 'Moved' agreement, with picture ΔE demoted to a diagnostic"* (D9). The step list (6.1–6.5, Close) never mentions it, and its "Reconciled against the test" block reconciles the *clicks*, not the In-now bullets. Runs 1–4 drained the steps; `rig.py` still graded ΔE < 2. It surfaced only because I opened `rig.py` at the close to check the Brief against the code, and it had to be built there (`a3f31fc`). `execute.md` already says *"put the WORK in the step list"* — but that is aimed at owed rulings, and the Brief template has no check that every In-now bullet has a step.

**Proposed fix.** In the Brief template / `plan.md`: *"Reconcile §In now against the step list, not only the clicks: every In-now bullet names the step that builds it, or is marked 'at the close'."* In `execute.md` §Before you touch anything: *"Walk §In now bullet by bullet and name each one's step. An orphan is added to the list now, not found at the close."*

**Where it'd live.** `plan.md` / the phase template (Brief §Step list); `execute.md` §Before you touch anything.

---

### 3 — The "what can the surface show" check lists scale and exposure but not LIGHTING, and the lead met the gap at the sitting `[self-error-doc-could-prevent]`

**Grounding.** Click 5 passed, and the lead added: *"makes me sad because UE shoudl make humans look WAY better than the plastic lifeless ting sI'm seeing in storm."* The rig's matched lighting (Phase06 D8: no shadows, no bounce, an even dome) removes exactly what makes Unreal's skin look alive: the soft shadow edge subsurface scatter makes, light through thin parts, occlusion. I knew that before the sitting and never said it. `execute.md` §TRY asks *"whether the surface's SCALE — resolution, viewing distance, exposure — can show the thing the click is about"*; lighting is the missing axis, and here it was the one that mattered.

**Proposed fix.** In `execute.md` §TRY, extend that sentence: *"… resolution, viewing distance, exposure, **or its lighting** (a parity rig's flat light cannot show a renderer's best), and **say before the sitting what the surface cannot show**, so the lead judges the right thing."*

**Where it'd live.** `execute.md` §TRY.

---

### 4 — The handback did not say what was left to close the phase, so the lead had to ask *"Is this phase done?"* `[self-error-doc-could-prevent]`

**Grounding.** The 6.5 handback reported click 5 and one `YOUR CALL` (the steer), with nothing on what remained: 6.2's publish, click 2 and the close. The lead asked *"Is this phase done?"*, then *"THEN CONTINUE!"*. The owed publish was in the phase doc's Resume block, not in the message.

**Proposed fix.** In `execute.md` §Handback, `Done` beat: *"End it with one line: `To close: <remaining steps, owed sittings, publishes>`, or `nothing but the close`."*

**Where it'd live.** `execute.md` §Handback.

---

### 5 — The close has no shape for an Outcome that only an off-box human act can prove `[doc-gap]`

**Grounding.** The Outcome's *"runs on any Linux machine … with no Unreal installed"* arms row A0 (an absolute claim), and it can only be discharged on the other machine (clicks 2 and 6). `execute_close.md` runs rows A→E as one pass that ends at the push. I improvised: land row A (D9, the docs), hold rows B–D, and record a `Close (in progress)` ledger row. That worked, but I had to invent it, and the move/🎉 now needs a second close session.

**Proposed fix.** In `execute_close.md`, after row A0: *"If the acceptance needs a human act on another machine or surface, run A⁻–A, push, and record `Close (in progress): held for <act>` in the phase doc. B–E resume after the lead's verdict, and that resume reads only the Close row."*

**Where it'd live.** `execute_close.md`.

---

### 6 — LOCAL_DELTAS' learnings-domains row is now stale (`Unreal/` exists) `[doc-gap]`

**Grounding.** The close created `docs/Learnings/Unreal/` (U1–U10, T1–T2). The row lists *"Domains on 2026-09-27: Blender/, MaterialX/, Storm/, ClaudeCode/"*; it rightly says to `ls` rather than trust it, and it is the Refiner's lane, so I left it.

**Proposed fix.** Add `Unreal/` to that row, re-dated.

**Where it'd live.** `LOCAL_DELTAS.md`.

---

## Keep these

- **§BUILD's "bisect by construction: make the probe load EXACTLY the harness's inputs".** The default-material fallback looked like a broken master. One launch of the character's own Unreal job, with four settings that each swapped one thing, found it: only the FIRST setting failed, on any materials. A second launch, varying only the hair material, found the thin-surface subsurface noise. Two launches, no hypothesising.
- **"Look at the output before reading the number."** A ΔE of 25 on the skin read as a calibration problem until I looked at the picture: it was Unreal's world-grid checker.
- **Asking once for a batch of GPU launches (D1)** — one question cleared the commandlet and three renders; the lead answered in seconds.
- **Row A's code check at the close.** Checking the Brief against `rig.py`, not just against the ledger, is what caught item 2.
- **Verifying before publishing:** rendering the character from the unpacked archive before `publish.sh` proved the package carried this run's masters, and a pinned download with no Unreal settings proved the other machine's path.

## Dead weight

None.

## Open questions

1. **Lead decision (open):** where "Unreal humans at their best" goes. The executor's recommendation is in the phase doc's Resume block: its own phase, next, starting from a lit view.
2. **Refiner or lead:** D14 rules a second publish at the close. With no runtime change since v1, I read the close's publish as v1 itself. Should the doc say "a close publish only if the runtime changed"?
