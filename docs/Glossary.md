# Matter Library — Glossary

**Status:** Active. Created at bootstrap, not "when it settles" — the moment a second doc reuses a term, that term is load-bearing (`.ai/AI_WorkingAgreement.md` §Documentation Shapes Architecture). **Use the established term, or fix it here first.**

> **Shape.** Term + **one-line** definition + pointer — never the spec (`Methodology/AgenticEngineering_DocumentationMap.md` §Glossary entry shape). Detail lives with its owner; the moment an entry needs a paragraph, it is mis-homed.
>
> **Source of truth.** Where this file and an authoritative spec disagree, **the spec wins and this file is the bug.**

---

## Entities

| Term | Definition |
|---|---|
| **<Term>** | <one line> |

## <Domain grouping>

| Term | Definition |
|---|---|
| **<Term>** | <one line> |

## Method terms

*⚠ **These are OWNED by `Methodology/AgenticEngineering_Workflow.md` — the rows below are a one-line gloss plus a pointer, never a second copy of the definition.** They are seeded on day one because, unlike anything stack-shaped, **this vocabulary is fully understood at adoption** and you are about to meet it in every command doc. **Where a row and the owning section disagree, the owning section wins and this row is the bug.***

| Term | Definition |
|---|---|
| **Phase** | Complex interconnected functionality; the top-level unit of work. → `Workflow.md` §Phase / Step / Task Terminology |
| **Step** | A **vertical**, testable chunk inside a phase — something a person can USE, never a layer with no user path. Numbered `Phase.Step` (`12.3`). → *same* |
| **Task** | An atomic, validatable check inside a step (`12.3.5`). **Available when a step needs decomposing; not a level every step populates.** → *same* |
| **Side Quest** | Unplanned work surfaced mid-phase and needed *now*; completed inline, inherits the phase's anchor. → *same* |
| **Quick Fix** | Shallow, self-contained, finishable in one context; the commit is the record. → `Workflow.md` §Units of work |
| **Issue** | Deferred standalone work, tracked; promotes to a Phase when it needs an anchor of its own. → *same* |
| **Brief** | Discovery's deliverable — Outcome · first human test · in/not-now · reuse check · lane · step list · build map. → `.ai/commands/discovery.md` |
| **First human test** | The exact click path, written before any code, that `/execute` hands the lead. → *same* |

## Project-local method terms

*Only project-specific usages appear here — a status word this project adds, a tier it names differently.*

| Term | Definition |
|---|---|
| **RESEARCH** | Roadmap status: the thinking lives in a research doc — no phase doc yet; the entry's pointers are the raw material. |
| **SEEDED** | Roadmap status: a phase doc exists. That doc is what discovery → plan → execute run against. |
| **ACTIVE** | Roadmap status: being worked. The phase doc moves from `Phases/Future/` up to `Phases/`. |
| **COMPLETE** | Roadmap status: closed; the phase doc moves to `Phases/Complete/`. |
| **TBD** | Roadmap status: a phase the lead has not numbered. It may hold a perfectly settled position — order is position in the list, never an ordinal. |
| **Probe** *(a.k.a. spike)* | A local, disposable feasibility test answering what documentation cannot settle. → `.ai/commands/research.md` §Disposable probes. |
| **Candidate** vs **selection** | A candidate has been assessed or probe-verified; a selection has been decided by the lead. A passed probe yields a candidate, never a selection. |

---

## Retired identifiers

*When a term is replaced, record it here rather than deleting it — two names for one thing at the same layer is a bug, and a reader hitting the old word needs to land somewhere.*

| Retired name | Use instead | Why |
|---|---|---|
| | | |
