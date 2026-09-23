**⛔ READ THIS ONLY IF THE PHASE'S BRIEF NAMED THE HIGH-RIGOR LANE.** Ordinary work runs [`execute.md`](execute.md) and nothing else.

**The lane exists for work whose failure is expensive or irreversible:** authorization · secrets · destructive migrations · data loss · the public edge. *(Lead ruling, 2026-08-29: a phase does not start here because high-rigor rules exist somewhere in the methodology. It starts here because the work warrants it, or it moves here when evidence during the work says so.)*

This file adds four things to `execute.md`. It replaces nothing in it.

---

## 1) A dedicated rollback snapshot

Ordinary runs use frequent scoped commits as rollback points and record their starting SHA. **Here, take a real snapshot commit before the first edit** — `Snapshot_Phase<N> — <Title> (rollback baseline)` — and keep it permanently. It is the reset target.

---

## 2) The gate baseline

**Run the phase's planned gates once against the snapshot tree; record PASS/RED plus counts, before the first source edit.** A red measured *after* your change cannot be attributed, which destroys the only thing the baseline was for.

**⛔ SELECT THE LANES BY THE SYMBOL EACH GATE ASSERTS OVER, NOT BY THE FILES YOUR STEPS EDIT.** "Touches" reads as *files*, and that is wrong for the commonest expensive case: **for every CLOSED SET your phase WIDENS — a role list, a capability vocabulary, an enum, a provider allowlist, an id registry — find the gate whose subject IS that set and baseline it, even though no step of yours edits its file.** One command gets you the list: grep the gate scripts for the symbol you are about to widen. **The cost is asymmetric** — an un-baselined lane that goes red late is not merely unmeasured, it is actively misleading.

**⛔ RECORD THE SET, NOT ONLY THE COUNT, WHENEVER ONE ASSERTION ENUMERATES ITS SUBJECTS.** A gate whose single assertion names *N* failing subjects **reds identically whether N is five or six**, so a count-to-count comparison is structurally blind to a new member joining — which is the exact shape of a regression you introduced. Where a red's message lists names, **bank the names**. It cuts both ways: an equal count cannot show a set changed *and cannot show it did not*. A count is fine when each failure is its own assertion; **a set is required when one assertion enumerates.**

**⛔ AND THIS FIRES HARDEST ON A BASELINE *YOU* RECORDED, AGAINST A CHANGE *YOU* MADE.** The obvious case is inheriting a red whose set grew. The dangerous one is the inverse: **a conditional field, a newly-guarded control or a narrowed fixture removes a subject from an enumerating assertion without moving its tally** — and the number you are comparing against is one you wrote an hour earlier, which feels authoritative in a way an inherited figure does not. *(A run made a field conditional — correctly, at the lead's request — and its gate held at exactly the inherited `11 of 52` while the absent set went from five members to six. A tally comparison would have shipped it.)*

**⛔ RECORD BOTH SIDES — an un-run lane is `✗ NOT RUN`, never omitted.** You cannot see the lane nobody mentioned. Write `lanes: typecheck ✓ · browser ✗ NOT RUN`. **A step with any `✗` lane is not a bare `✅`.**

**A deferred lane's baseline is taken at the top of the step that owes it — before that step's first edit.** Deferring the *lane* is fine; deferring the *measurement* past your own change is not.

---

## 3) The premise proof

**⛔ A PREMISE PROOF IS NOT A GATE BASELINE.** They answer different questions — *has the target behaviour ever worked?* versus *what was already red before I touched anything?* **If the first step is a premise proof, the baseline is STILL OWED: take it in the same turn, before the first source edit.**

**When the phase's goal is an end-to-end behaviour** — including a *"a prior phase already built X, this just finishes it"* premise — establish **when that behaviour was last SEEN working, live**, and record it. *Never* / *unknown* / *"the gates were green"* means the first scheduled act is a live premise-proof smoke. **No run may claim "done, only the smoke remains" while `behavior proven live? = N`.** Green builds anchor nothing here.

**⛔ THE PROOF MUST NAME ITS LANE.** Record three fields: `proof exercised: <file:line / predicate>` · `feature traverses: <file:line / predicate>` · `same? Y/N`. **An `N`, or an unfilled field, does not satisfy the gate.** *"The chain works"* is not a claim a branching system can support — only *"this branch works"* is, and a proof that cannot name its branch is not a premise proof.

**⛔ SET-LEVEL, AND NO PER-GATE RULE CAN SEE IT: enumerate the entry paths your whole baseline actually traverses** — HTTP API · stored rows · the CLI · the rendered UI · the build artifact — **and name the ones with ZERO coverage. A phase whose Outcome is a user-facing surface, and whose every assertion is server-side, has not planned to test its deliverable.**

**A `⚠human` premise proof splits, and this is settled once rather than re-litigated per turn:** the agent drives the deploy / launch / log-observable half autonomously; the eyes-on verdict is the lead's and may be async.

---

## 4) The RED-demo playbook

**When this phase adds, re-points or must demonstrate a gate, read [`execute_test.md`](execute_test.md).** You are in its territory whether or not a step is labelled "test".

**⛔ BIND THAT READ TO YOUR FIRST GATE INVOCATION, NOT TO THE PHASE'S GATE INVENTORY.** On a phase whose gates land *last*, "read the gate playbook now" competes with starting step 2 and loses to a reasonable belief — *"I will read it when I get there."* Three runs failed this trigger, and the third read it, evaluated it correctly, and deferred it anyway.

The load-bearing rule, promoted here so it is never missed: **a RED-demo script exits NON-ZERO BY DESIGN. Never infer the outcome from the exit code — read each arm's log and confirm it is red for the intended reason.**
