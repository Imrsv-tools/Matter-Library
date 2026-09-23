# quick-fix — do a shallow, self-contained change now, in one context

The **informal front door.** You come in cold and say `/quick-fix <describe the request>`
("make the popup blue", "rename `frobnicate` to `transform` in the slice writer", "the
README link is dead") — and an agent runs the whole D→P→E flow *itself*, lightly, in **one
sitting**: understand the project + conventions, go in, effect the change, commit. No phase
doc, no tracker, no ceremony.

Canonical model: `Methodology/AgenticEngineering_Workflow.md`
§Units of work (the Quick Fix row + the depth-then-anchor triage).

## Where it sits — the three classes of command

- **Cold entries** (the lead supplies the intent): `/howdy` · `/research` · `/discovery` ·
 **`/quick-fix`** · `/issue-create`. Quick Fix is the **do-it-now** sibling of
 `/issue-create`'s **file-it-for-later** — same cold trigger, opposite verdict.
- **Continuations** (the AI rehydrates a persisted phase doc): `/plan` · `/execute`. You
 *can't* reach these cold — they need a phase doc to already exist. Quick Fix is the
 opposite: it carries its own context start to finish, so there is **nothing to rehydrate
 and nothing to hand off.**
- **Machinery** (the system maintaining itself): `/retro` · `/workflow-refiner`.

## What makes it a Quick Fix — the **DEPTH** bound (not size, not urgency)

A Quick Fix is bounded by **depth**: it needs *no real dive*. The agent already knows enough
(project + conventions) to just do it. That is the whole test. It is distinct from a **Side
Quest** (bounded by *anchor* — needed-now, rides a running phase, **can be any size**) and from
an **Issue/Phase** (needs a dive — architecture, decisions, multi-step thought, its own anchor).

The argument is the request itself, in plain language. If it's ambiguous in a way that blocks
starting, ask **one** simple clarifying question ("which shade of purple?") — **never an
architecture / data-model / contract call.** A **bounded presentation/UX fork** (even a 3-way
"inline error vs disabled button vs both") is fine to resolve with a single `AskUserQuestion` and
continue ([[feedback_decision_questions_content_not_process]]) — that's content, not architecture.
But **more than one real question, or an architecture/data-model/contract decision**, is a signal
this isn't a Quick Fix (see the gate).

## The do-or-route gate (the load-bearing step)

Before changing anything, assess: **is this actually shallow and self-contained?** The signals
that it is *not* — any one is enough to stop:

- it touches **many files / multiple subsystems**,
- it raises a **real architecture / data-model / contract decision** — a *bounded presentation/UX
 fork* ("inline error vs disabled button vs both") is **not** this: resolve it with one
 `AskUserQuestion` and continue,
- it hits an **unknown** that needs investigating before you can act,
- it's **interconnected** enough to want its own rollback anchor.

**⛔ A FIFTH VERDICT THE TABLE NEVER HAD — THE LEAD ALREADY ROUTED IT HERE.** Every signal above assumes the lead has **not yet spoken**; the framing *"stop and surface a recommendation; the lead calls it"* is meaningless when they just called it by naming the verb. **When the lead has explicitly said "do the X quick-fix": proceed. State the signal you would otherwise have stopped on and why you judge it cheap, and keep the mid-flight balloon valve armed.** **The gate exists to protect the lead's decision, not to override it.**

**Route on the verdict — and when it's not a Quick Fix, STOP and surface a recommendation; the
lead calls it** (consistent with Workflow's "the agent surfaces the signal, the lead calls it" —
never silently promote):

| Verdict | Action |
|---|---|
| **shallow & clear** | **do it** — inline mini-plan → change → light verify → commit |
| **bigger-but-clear** | stop, recommend **`/issue-create`** (file it, do it properly later) |
| **needs digging** | stop, recommend **`/research`** (investigate first, may seed a phase) |
| **needs its own anchor** | stop, recommend a **Phase** via **`/discovery`** |

**The safety valve runs mid-flight too.** A change that *looked* shallow but balloons once
you're in it — a third file, a decision you didn't expect — **stops and promotes** the same way.
Shallow is the default for small; ballooning kicks it up a tier. There's no threshold to
memorize — surface the signal ("this is reading bigger than a quick fix — promote to an Issue?")
and let the lead decide with the picture in front of them.

## Procedure (light by design)

1. **Orient — Fundamentals (carried) + a thin slice of Focus.** You already carry the
 **Fundamentals** (the distilled handbook is always loaded); pull only the **thin slice of
 Focus** this change touches — the project map to navigate (`.ai/AI_Orientation.md`), the one
 convention the edit hits (`NamingConventions`/`CodingStandards` *only if* it's naming/code-shape),
 **Don't** front-load
 the full discovery read set (Roadmap, phase docs, a domain-Learnings sweep) — that weight is
 exactly what Quick Fix exists to avoid. (See SystemOverview §What-the-machine-reads — a Quick
 Fix is the minimal corner of that chart.)
2. **One-pass read** — locate what's being asked and where it lives (Grep/Glob/Read or a
 Bash-less search agent — **never `Explore`**). At most one simple clarifying question.
 **If Grep/Glob are absent from the session, don't improvise** — take the documented
 fallback in `.claude/CLAUDE.md` §Codebase search (a single statically-analysable
 `grep -n` on literal absolute paths; no `cd`, no pipes, no redirects). The named tools
 are the primary path, not the only sanctioned one.
3. **Gate** — run the do-or-route assessment above. If it's not a Quick Fix, stop and recommend
 the right door. **Skip §7 repo-sync** — Quick Fix rides clean-trunk HEAD, it doesn't
 sync-and-re-plan.
4. **Do it, then VERIFY — proportional to what a user can OBSERVE, and BEFORE the commit**
 (the commit is the record; don't record an unverified behavior claim). Inline mini-plan in
 your head (no plan doc), make the change, then:
 - **⛔ INFRASTRUCTURE / BUILD-PATH CHANGE — a third branch, and neither of the two below fits it.** Nothing is visible in a UI, and **a green compile proves nothing whatsoever, because the pipeline IS the subject**: the build succeeding is the thing under test, not evidence about it. **Assert the ARTIFACT AND THE EFFECT** — what the built artifact *contains*, what the running thing *answers*, and that **the path you did NOT intend to change is byte-for-byte unaffected.** Then **name the command that would have caught it.** ⚠ Read literally without this branch, such a change routes to *"non-observable ⇒ the compile IS sufficient"* — **which is exactly the state in which a silently repointed production image is live and invisible.**
 - **User-observable change** (visible / clickable / runtime — and **most Quick Fixes are
 visual in-app issues**): a green build is necessary but **NOT sufficient.** Build, then
 **open the page yourself and click the thing**, and **hand the lead the exact steps** ("open
 a new article → the title field should accept text") so they can confirm at a glance.
 **The lead's verdict that it's fixed — and fixed COMPLETELY, not half — is the gate.**
 (The #26 lesson: a green build "declared done" had fixed only *half*; only the click
 caught it. Don't commit until it confirms the *whole* ask.)
 - **Non-observable change** (doc link, comment, a pure-logic path fully covered by a passing
 unit test): the build / test IS sufficient.
 Honor the §⚠️ gate rules from `execute.md` if you shell out (no capture-tails; literal paths /
 `git -C`; long ops → a `/tmp` script) — but most Quick Fixes are a single edit and never hit them.
5. **Sync touched docs (spec-driven — docs are source of truth).** If the change touched a
 surface that has a spec doc (a modal, component, system, service — anything under
 `docs/`), **update that doc in the same commit** so code and spec
 don't drift. Match the doc to what you actually shipped — fix stale/aspirational text (e.g. an
 "Error State" that describes behavior you just made real), and add a short dated note where the
 doc tracks history. Most trivial fixes (a popup color, a dead link) touch no spec doc and skip
 this. Don't *duplicate* — link to canonical docs and record only the delta ([[feedback_no_doc_duplication]]).
6. **Commit — the git commit IS the record.** Stage **your paths explicitly — never `git add
 -A`** (this tree carries parallel-session churn you didn't create — leave it). The
 **top commit subject carries the loud, greppable marker `✅ Quick Fix
 — <what changed>`** so quick fixes are findable in `git log --grep "✅ Quick Fix"` (the sibling
 of `🎉 PHASE COMPLETE` / `✅ Issue #<n>`, and distinct from both so each greps cleanly).
 **No Claude co-author trailer** (your authorship only — the project states this once, centrally;
 see `.claude/CLAUDE.md` §Git). **No Roadmap entry, no `Snapshot_*`, no stage-5 close ceremony.**
 (When the fix came from a GH issue, the close uses `✅ Issue #<n>` instead — see the next section.)

## When the Quick Fix came from an Issue (close it out)

A Quick Fix is usually a cold entry, but one can also be **drawn from an existing GH Issue** —
the lead points at a filed ticket and the fix turns out to be shallow enough to just do now
(this is the crossover the original "do-it-now vs file-it-for-later" framing didn't cover). When
that happens, the Issue is a real obligation — don't leave it dangling. After the change is built
and **verified**:

1. **Did the fix actually resolve the Issue's ask?** Be honest. If it only *partially* addresses
 it (e.g. you fixed a root-cause trigger but the Issue's stated ask is a separate UI change),
 **comment with what you did and leave the Issue open** — re-scope it in the comment. Only run
 the full close-out below when the Issue's actual ask is satisfied.
2. **Commit first** (steps 5–6 above), so you have a SHA to cite. The platform-repo commit that
 closes an Issue uses the loud, greppable Issue-close format — **`✅ Issue #<n> — <Title>`**
 subject with **`Closes #<n>`** in the body (
 referencing `#<n>`). This is the same convention as a full Issue close ([[feedback_issue_complete_commit]]),
 minus the workbench delete (a Quick Fix never had one).
3. **Comment on the Issue** with what the fix was — the root cause, what changed, and the
 commit SHA(s) — so the ticket stands alone in its history (`gh issue comment <n>`).
4. **Remove the workflow `status:*` label and close** (`gh issue edit <n> --remove-label
 status:<x>` then `gh issue close <n>`). Closing explicitly (don't rely solely on `Closes #<n>`
 auto-closing on push — a Quick Fix may not push right away).

**No** Roadmap entry and **no** version event — an Issue bumps neither MINOR nor BUILD; it rides
the next Build, exactly as in the normal Issue lane.

## Rollback is free — no snapshot to manage

Quick Fix takes **no named snapshot** (that's a Phase/Issue concern). Before you commit, your
edits discard cleanly (`git restore <paths>`); after, it's a single `git revert`. That's the
whole rollback story — which is *why* the depth bound matters: if the change is big enough to
want a real snapshot, it was never a Quick Fix.

## Notes

- **No handoff, ever.** Quick Fix is one-context by definition. If a change can't finish in one
 sitting, that's the balloon signal — promote it, don't hand it off.
- **The commit message is the only durable trace** — make it descriptive enough to stand alone
 in `git log` (the request + what changed), since there's no phase doc or issue carrying context.
- This is a *verb* (you invoke it); the lead can also just describe the change in prose and an
 agent should recognize the Quick-Fix shape and apply this procedure.
