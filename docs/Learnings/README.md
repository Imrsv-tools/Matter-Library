# Learnings — what the technology did that surprised us

**This tree is EMPTY on a new project, and that is correct.** It is not a gap and it is not a
to-do. Every entry here is **paid for by a failed run**, never by reading — the first one arrives
the first time this project loses time to something it could not have predicted.

## Shape

**One folder per domain your project actually has** (`<Domain>/`), **one file per domain**, **one
entry per lesson**, each with a short stable id (`C1`, `L1`, `S1`…) so other docs can cite it.
Create a domain the first time it earns an entry — never in advance.

## Bar for adding — ALL FOUR, or it does not belong here

- **Non-obvious** — a competent developer reading the official docs would still get it wrong.
- **Poorly documented** — missing, wrong, or buried upstream.
- **Costly to rediscover** — it cost real debugging time, and would cost it again.
- **Specific** — a concrete pattern, not a general principle.

**A note that fails any one of the four belongs in the phase doc, not here.** If nothing
qualifies at the end of a piece of work, the honest answer is *"no new learnings"* — write that
and move on.

## ⛔ What does NOT go here

- **Why a METHODOLOGY RULE says what it says.** This tree is for what the *technology* does.
  Process rationale belongs with the rule it justifies — see
  `Methodology/AgenticEngineering_Workflow.md` §Where stack knowledge lives.
- **Anything the code or the commit already tells the next reader.** If it is greppable, it is
  not a learning.
- **A decision.** Decisions live in the research doc's `## Resolved` and in `docs/architecture/`.

## Reading them

Learnings are **force-read at discovery**, for the domains the phase touches — that is where a
costly invariant pays off, and reconstructing it from code is wasted passes. ⚠ **If the phase
touches no domain that has an entry, or this tree is still empty, say so in one line and move
on.** That is a **discharged** read, not a skipped one.
