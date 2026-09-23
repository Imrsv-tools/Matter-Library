# Refinement Backlog — the Refiner's own ledger

**Not a `/retro`.** The inbox (`<YYMMDD>_*.md`) is the executor→refiner channel; this file
is the refiner's own. A refiner depositing into the queue it drains would invert that.

Three things live here, and nothing else:

1. **Absorbed** — items already folded in, so a later deposit doesn't re-file them
   (`retro.md` §Where it goes).
2. **Cut-candidate tally** — dead-weight flags, counted across runs. A candidate that keeps
   getting flagged graduates to a cut. **Never tally a destructive-error-preventer.**
3. **Held / deferred** — accepted but not yet landed, with the reason and the ready-to-apply
   fix. **Written as a condition that can be checked, never as a justification** — a hold
   whose precondition has since been met is invisible to every sweep.

Keep it as *state*, not a log: rewrite each section to what is true now. The history is in
the commits.

---

## Absorbed

_Nothing drained yet._

| Item | Landed in |
|---|---|

---

## Cut-candidate tally

A rule is cut when the flags say it is dead weight *across runs* — not on one complaint.

| Candidate | Flags | Runs | Status |
|---|---|---|---|

---

## Held / deferred

| Item | Held until | Ready-to-apply fix |
|---|---|---|

---

## Open — needs a lead ruling, not a refiner tweak

_None._

## Upstream queue

Portable fixes belong in [`PeteSmalls/agentic-engineering`](https://github.com/PeteSmalls/agentic-engineering),
not only here. **A portable fix landed only locally is how N projects end up with N
divergent methodologies.** Edit the local copy and upstream together so the re-sync is a
no-op, then bump the recorded SHA in `AGENTS.md` §Heritage.

## Recurring themes

_None yet._
