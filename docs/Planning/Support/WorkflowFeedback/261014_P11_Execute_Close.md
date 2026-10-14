# Workflow Feedback — P11 / execute / close

| | |
|---|---|
| **Verb** | `execute` (the close, `execute_close.md`) |
| **Unit** | `P11` (Library Coverage) |
| **Mode** | `close`: a close by ruling. The phase was paused after 11.3 on 2026-10-02, and a research ruling (RD-MP-13 in `261014_R_MaterialPipeline.md`) replaced its remaining step and its end review |
| **Outcome** | `done`: 29 of 35 rows kept, 6 redo, the Blender library rebuilt, the docs conformed, closed and pushed (`3caf294..6b824f7`) |
| **Shape** | `behavior-touching` (recipe statuses, the wish list, the generated library `.blend`) |
| **Confidence** | Ran fully: `execute_close.md` rows A⁻ to E, with one lead sitting inside the close. **Not exercised:** BUILD/TRY/STRENGTHEN from `execute.md`, rows B⁺ (no Wave) and C (no issue). |
| **Date** | `2026-10-14` |

---

## Items, ranked

### 1 — The close assumes "by the close the lead has seen everything", and a close by ruling breaks that `[doc-gap]`

**Grounding.** The argument was `/execute Phase 11 close (as noted)`. "As noted" was RD-MP-13: keep by verdict, put 24 rows to the lead's eye, move 11.4 into the loop as redo rows, rebuild the Blender library, close. So the close itself held a lead sitting (24 rows, review pages opened, a keep or redo per row) and a minutes-long Blender rebuild. `execute_close.md` assumes otherwise in two places: *"The close does not start a long operation on its own. By the close the lead has seen everything"*, and *"Prerequisite: you arrived here from `execute.md` §Handback"*. Neither was true, and I had to decide on my own that a research ruling naming the close as `/execute Phase11`'s counts as the lead initiating it, and that the sitting and the rebuild were the ruling's steps, not "an evidence gap".

**Proposed fix.** In `execute_close.md` §Prerequisite: *"A close can also be ordered by a ruling that replaces the phase's remaining steps (a close by verdict). The ruling's steps are then the close's first rows: run them, including a lead sitting, before row A. The no-long-operation rule is about re-checking what the lead has already seen; it does not cover steps the ruling names."*

**Where it'd live.** `execute_close.md` (likely portable).

---

### 2 — Row A's ledger walks the doc's threads, not the tools the close itself ran, so a defect in this phase's own tool slipped through `[self-error-doc-could-prevent]`

**Grounding.** At the close the lead said *"redo Terracotta too"*, for a row I had already kept by verdict. `wishlist.py redo` set the state but left the recipe at `approved`, against the phase's own Decision 4 (*"A redo leaves it `draft`"*). I worked around it by calling `set_status(…, "draft")` from a `/tmp` script, and closed. Only at `/retro` step 0 did I see that the workaround *was* the finding: a correction to a surface this phase authored, which row A says is in scope and never deferrable. It is now a ledger row in the phase doc, owed as a quick fix (`36b3c0a`), not a fix.

**Proposed fix.** In row A's ledger bullet: *"Also list every workaround the close itself used (a hand edit, a /tmp script standing in for a tool). Each one is a candidate CORRECTION to the tool it worked around."*

**Where it'd live.** `execute_close.md` row A (portable).

---

### 3 — Row B's link rule says the move puts the doc "one level deeper"; here it doesn't `[doc-gap]`

**Grounding.** This project keeps seeded phases in `Phases/Future/` and closed ones in `Phases/Complete/`, so the move is a sibling-to-sibling move at the same depth. Every `../../Research/…` link stayed right. The one that broke was `../Complete/Phase10_….md`, which became a same-folder link. The "inverse case" sentence covers it, but only after a paragraph built on a premise that is false here.

**Proposed fix.** One line in `LOCAL_DELTAS.md`: *"Phase docs move `Phases/Future/` → `Phases/Complete/`, the same depth: only links naming `../Complete/` change (to a bare filename)."*

**Where it'd live.** `LOCAL_DELTAS.md` (a port gap).

---

### 4 — "Keep by verdict over every built row" was rebuilt ad hoc, a second time `[doc-gap]` (a product gap, raised for routing)

**Grounding.** F-MP-47 was measured by a research run with a classification over `wishlist.verdict`. At the close I re-measured it with a new `/tmp/p11_verdicts.py` (clean / flag / disagree / no run), then ran `wishlist.py keep` 11 times, then 25 more changes through a second `/tmp` script. The helper has `verdict <name>` and `keep <name>`, but nothing for "all built rows". That operation is now the loop's standing review step (RD-MP-13).

**Proposed fix.** A product quick fix, not a method change: `wishlist.py review` (classify every `built` row) and `keep --clean`. Listed here so the refiner can route it, since it is not workflow.

**Where it'd live.** Unsure: product backlog (`/matter-batch` or `wishlist.py`), not a command doc.

---

## Keep these

- **Row D's "I have not pushed is not CI has not run": `merge-base --is-ancestor` before writing the `🎉` body.** My draft said *"the whole phase since 2026-10-02 is local"*. The check showed `aa23deb` already on origin, and the line was corrected before the commit.
- **Re-measure a count after your own last change.** I wrote "30 kept, 15 approved" into the Experience spec before Terracotta's redo. `wishlist.py counts` gave 29 and 14, and it was fixed before the commit.
- **`git status -s` plus `git diff --cached --stat` before every commit.** Siblings were live in the SkinMaps, RoadmapOrder, Roadmap and four seed docs throughout. Every commit was explicit-path and none carried their work.
- **Push your tip by value, naming the foreign commits under it.** The lead was told about 18 sibling commits under `6b824f7` before saying push. A sibling commit that landed after the push stayed behind and was reported.
- **The deliverable-surface rule.** The sitting went into the phase doc and the review pages were opened locally. A publish tool was on offer and was not used.
- **"A present lead is for seeing": a recommendation on every row.** It let the lead judge 24 rows in one line (*"go with your recommendations, redo Terracotta too"*).

## Dead weight

- **`execute.md` read in full (58 KB) for a run whose argument said "close".** The `/execute` skill loads it, and its first paragraph sends a close to `execute_close.md`. None of BUILD, TRY or STRENGTHEN applied. A one-line router at the top of the skill ("argument names the close → read `execute_close.md` only") would have saved it.

## Open questions

1. **Lead decision:** the deferred additions have no owning phase (Edges01's curvature input; the library limits F-P11-9, -16, -17; soft coverage on Masked; the rig's surround and gem size). Seed a "masters refinement" phase, or leave them in the Phase11 ledger until a phase claims them?
2. **Owed, not done:** the `wishlist.py redo` correction (item 2), as a `/quick-fix`.
