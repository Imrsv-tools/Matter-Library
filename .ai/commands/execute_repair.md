# `/execute` — the Failure Routes: derail and verified repair

> **Sibling of [`execute.md`](execute.md). Read this ONLY when a gate, a build, or a smoke has FAILED** —
> i.e. you are on the derail or verified-repair route out of `execute.md` §STRENGTHEN.
> A healthy run (a success handback, or a suspend) never opens this file.
>
> Split out for that reason **and one more**: these rules fire at the moment of maximum pressure, and in the
> monolith they were read at run start — hundreds of thousands of tokens before they were needed, competing with
> reflex. Read them **here, now, before you write the fix.**

## Which route am I on? — pick the row, do NOT improvise

| The tell | Route |
|---|---|
| A **real, localized defect in an already-DONE-and-committed step** (often one whose parity test was green-but-premise-wrong), surfaced by the smoke or a closing gate | **Verified-repair loop**, below. Not a derail, not a deferral. |
| The work itself is **wrong / can't localize / fixes keep spawning fixes** | **Derailed — whack-a-mole**, below. |
| The **committed work PASSED ITS OWN GATES** and the failure sits in a layer the unit did not author | **Derailed — premise-invalid / scope-extends**, below. **KEEP THE COMMITS.** |
| The defect is **genuinely unrelated** to this phase | a **deferred GH issue** (the `DEFER:` note — `execute.md` §Doc-write routing). Not your defect. |
| The crash **matches a known pre-existing issue** (`source:preexisting`) | Neither a derail nor your defect. Find the OPEN ticket (`gh issue list --label source:preexisting`, or search the symptom) and post your fresh forensics (symbolicated callstack, repro) as a **comment on it**. Do **NOT** spin up a parallel `Troubleshooting/` doc, and do **NOT** roll back. |

---

# Derailed (the lead's judgment call)

**Rollback is the DEFAULT, not automatic.** Two sub-cases; pick by the tell.

| Sub-case | What you do |
|---|---|
| **Whack-a-mole derail** — the work itself is wrong / can't localize / fixes keep spawning fixes | Capture failure notes in a doc **outside the rollback scope** (durable `docs/Planning/Support/Troubleshooting/`), `git reset` cleanly to the `Snapshot_Phase<ARG>` baseline, hand back with the notes so planning can refine. |
| **Premise-invalid / scope-extends** — **⛔ KEEP ALL COMMITS, do NOT reset** | **The tell: the committed work PASSED ITS OWN GATES and the failure is in a layer the unit did not author** — the gate of record refutes the *premise*, not the code. Rolling back here destroys correct, live-proven, load-bearing work. Park the forensics in `Troubleshooting/`, **supersede the Resume block with the ruling**, hand to `/plan <unit>` to re-scope. |

**Keep-or-revert stays a LEAD call** — surface it, don't self-authorize either way.

**⛔ On EITHER sub-case, supersede the now-false discovery findings IN PLACE before handing off** — the §5/§6 rows and Resolved Decisions the refutation invalidated. `feedback_no_edit_phase_doc_mid_execution` bans editing the live *plan* mid-step; it does **not** bar marking a *refuted premise* at a deliberate derail stop — and if you don't, the next planner reads a false premise stated confidently.

---

# Verified-repair loop

**Fix in place — but ONLY if all three hold:**

1. root-caused to a **localized** change,
2. the fix carries its **own new parity test**,
3. the gate **re-greens** → re-deploy → re-smoke.

**⛔ AND *VERIFIED* IS THE WORD IN THIS ROUTE'S NAME, SO DEFINE IT BEFORE YOU USE IT: NAME THE OBSERVATION THAT WOULD DIFFER IF THE FIX WERE ABSENT. If the answer is "none" or "the same number", the measurement is NOT a verification.** The whole doc set is saturated with this question — *can this gate FAIL?*, *the proof must name its lane*, the entire RED-demo apparatus — **and every instance of it is written about a GATE**, so it correctly does not fire when you are verifying a one-line fix with an ad-hoc command. **A steady-state count is the weakest possible evidence for a cleanup**, because the absent-fix world produces the identical reading; **measure a quantity that must MOVE.** (`execute.md`'s verify-before-edit table carries the general rule and its tells — the discriminator is deliberately not gate-only.)

Then continue to the handback (`execute.md` §Handback). If it's broad / whack-a-mole / can't-localize → **Derailed**, above.

## ⛔ Root-cause EMPIRICALLY — don't spiral on static reads

**⛔ WHEN A NEIGHBOURING GATE REDS AFTER A FIX, ATTRIBUTE IT BY MEASUREMENT — REVERT THE ONE FILE, REBUILD, RE-RUN. RUN-ORDER ARGUMENTS AND *"IT MUST BE PRE-EXISTING"* ARE REASONING, AND REASONING LOSES.** *(A handback reasoned from run order that a red in an untouched subsystem was pre-existing-and-newly-visible, and flagged it unattributed — a careful, plausible, wrong conclusion. The lead said "run the rebuild-and-compare now"; a two-by-two revert table showed the fix DID cause it. A production hook had been reading a value that was correct only because of the bug being fixed.)* ⚠ Pairs with `execute.md`'s verify-before-edit row on fixing a bug other code depends on — that one fires **before** the edit, this one **after** the red.

**A NEGATIVE log grep is evidence only at the marker's VERBOSITY.** Before concluding a code path did NOT fire from log absence, check the log line's level — a line below the run's active verbosity never appears, so its absence proves nothing (a "never fired" claim once shipped while it had fired 345× at a suppressed level — and WAS the root cause). `execute_test.md` §Can this gate FAIL?'s Log-level rule covers markers you WRITE; this covers the pre-existing line you grep.

**The universal trigger: ≥2 static reads each concluding "should work" while live behavior contradicts = STOP READING, INSTRUMENT.** Go empirical — instrument the suspect function and write a test that drives the **REAL entry path end-to-end** (not the unit in isolation; a repro against the *real saved artifact* beats a synthetic reconstruction). Leave that live-path repro as the permanent regression test.

| The defect | The FIRST empirical move |
|---|---|
| **Segfault / heap corruption** | **`gdb -batch -ex run -ex bt`** for a backtrace. It localizes in one shot even when the crash surfaces far from its cause. Instrument only *after* the bt points you at the function. |
| **Live BEHAVIORAL bug, engine-level, no headless seam** | A **rate-limited per-frame `[DIAG]` log of the disputed state.** One confirming read, then instrument and drive **ONE** smoke before writing any fix. Static-reasoned fixes that build+smoke+fail burn a human-driven cycle each; the state probe finds it in one. |
| **Engine-level repair with no headless seam** (a a huge translation unit, no compile database, the defect in a code path the automation test cannot drive) | The **eyes-on re-smoke is the gate of record**, and a **regression-guarding code comment** substitutes for the headless parity test. Name this in the handback (`execute_test.md`'s eyes-on-gate provision). |
| **A banked defect FAILS to reproduce** against the exact live entry path | **A finding, not a dead end.** Keep the repro as a contract pin, re-attribute the live symptom explicitly (tag it `hypothesis` if unproven), add the instrument that will discriminate it at the next human gate, **headline the exoneration.** |

## ⛔ Escalation ladder — when a point-fix is the WRONG shape

Walk these in order. Each row exists because reactive per-control patching ran past it.

| Trigger | Action |
|---|---|
| **A 2nd distinct failure in the SAME subsystem that the 1st fix didn't predict** | **STOP per-control fixing. Do ONE systematic layer-trace** — enumerate the pipeline the data crosses (write → store → read → transport → render) and find which *layer* drops each attribute. Many controls failing "randomly" in one subsystem ⇒ a **completeness/contract break at a shared layer**, not N independent bugs. |
| **You have completed a layer-trace** | **⛔ It establishes WHICH LAYER is unowned/incomplete — it does NOT establish WHY any individual symptom occurs.** Two claims, two evidence bars: tag the **class** `confirmed` once the layer is shown unowned; tag **each per-symptom mechanism** `hypothesis` until **measured in the real artifact**. The trap is that a layer-trace *feels* like it has produced an explanation. |
| **A 2nd eyes-on failure survives a green verified-repair in the same subsystem** | **Invert to a bottom-up per-layer PROOF ladder** — drive each layer in isolation with hardcoded inputs, lead verdict per layer, fix at-layer with its own guard, **promote only on visual green**. |
| **≈3 consecutive eyes-on hypotheses fail to fix it** | **STOP-LOSS. Present derail-vs-spike-vs-continue as ONE numbered `YOUR CALL` item, with your recommendation** (`AI_WorkingAgreement.md` §Working With the Lead). Each hypothesis on a no-headless-seam defect costs a rebuild + a lead-driven smoke. **Never silently start hypothesis N+1** — a ~13-cycle ladder once ran until the *lead* called the derail. |
| **The layer-trace shows the defect sits in a subsystem the phase ASSUMED working** (a Discovery "never-exercised E2E" carry-forward) — especially a **SECOND** deep defect in that same subsystem | **Escalate to Derailed / spike: the phase premise is invalid.** Don't keep repairing on top of an unproven foundation. |

## Co-drive and suspend mechanics

- **When the lead is co-driving (`⚠human-codev` iteration):** **batch all root-caused fixes into a single rebuild per cycle** (each rebuild is 2–4 min of the lead waiting), keep the live defect state in the `Troubleshooting/` doc, and update the Resume block **ONCE at the actual suspend**, not per cycle.
- **A repair that crosses a suspend** (multi-iteration, context exhausted mid-repair): WIP-commit the validated-so-far slice as **`WIP [P<NN>.<step>] repair-partial`** (diagnostics still in is fine — note them) so the resume keys off a SHA. Leaving it on disk is sanctioned **only** with a `Troubleshooting/` doc + a Resume block naming **every** uncommitted file.
- **Context ceiling interaction:** the ~400k architecture-ceiling (`execute.md` §STRENGTHEN, the drive-to-done rule) does **NOT** gate executing a fix you have **already fully root-caused**. If the diagnosis is complete and the change is mechanical, **DO IT.** Citing the ceiling to defer a known one-liner is a misuse of the rule as cover. But the repair loop's stop-loss above **does** bind: a non-converging repair (≈3 failed attempts) or context ≥400k means an **unbounded repair IS the derail signal** — stop and hand the decision up, don't keep coding into it.

---

**Back to [`execute.md`](execute.md):** a re-greened repair continues to the **success handback** (`execute.md` §Handback); a derail hands back per the **three-beat handback format**.
