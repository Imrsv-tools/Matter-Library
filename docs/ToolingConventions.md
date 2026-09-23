# Matter Library — Tooling Conventions

**Status: NOT YET.** This document arrives **with the first real build** — see
`Methodology/AgenticEngineering_Workflow.md` §Where stack knowledge lives.

⛔ **Do not invent a structure here to fill it in.** Creating an empty tree or a naming scheme for
artifacts that do not exist is **structure asserting a decision nobody made**, and the next agent
reads it as binding.

## What lands here, once there is a build

The **artifact taxonomy**: which roots are live and what each is for · where scripts, fixtures and
test assets live and how they are named · what the build / test / lint / deploy wrappers do · the
CI entry-point expectations · the authoritative surface for language and package-manager versions
· what the format check actually covers.

**If this project has a gate or check registry** — numbered checks a phase allocates ids from —
this doc owns it, including the allocation rule. ⚠ **A centrally-allocated id series is a
collision surface no file grep can see**, so say plainly whether ids are claimed at plan time or
at execute time (`Workflow.md` §Phase / Step / Task Terminology and the namespace rule in
`plan.md`).

**Where test documentation lives is this doc's call**, including ruling it N/A. Say so explicitly
rather than leaving it unstated — the first phase shipping a real suite decides it, here.

## What does NOT land here

- **What the system is** → `docs/architecture/`.
- **How code is written** → `CodingStandards.md`.
- **Naming rules and vocabularies** → `NamingConventions.md`.
