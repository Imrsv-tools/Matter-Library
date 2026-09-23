# Matter Library — Coding Standards

**Status: NOT YET.** This document arrives **when research commits to a stack** — see
`docs/architecture/` and `Methodology/AgenticEngineering_Workflow.md` §Where stack knowledge
lives.

⛔ **Do not populate this ahead of that decision.** A standards doc written before a stack is
chosen is a guess wearing the costume of a decision, and every later reader treats it as settled.
An empty one is correct; a speculative one is actively harmful.

## What lands here, once there is a stack

How code is **written** in this project: language level and idiom, error handling, module and
import shape, the typing bar, comment policy, test style, and the standards a review is actually
held to.

**Mark anything still open as `TBD →` with the phase or research that will close it** — an
explicit gap is honest and greppable; a silent omission reads as "no rule exists".

## What does NOT land here

- **What the system is** → `docs/architecture/`.
- **Where scripts, fixtures and CI entry points live, and what they are called** →
  `ToolingConventions.md`.
- **Casing matrices, identifier vocabularies, id registries** → `NamingConventions.md`.
- **What surprised us about the technology** → `docs/Learnings/<Domain>/`.
