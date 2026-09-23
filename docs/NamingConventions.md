# Matter Library — Naming Conventions

**Status: ACTIVE (arrived 2026-09-23, Phase01 step 1.1).** Its trigger was met long before adoption: the
Matter filename grammar, the scale tags and the release ids are id series in live use. Step 1.2
completes it (MaterialX casing, the identity grammar's full rules); this first cut carries the
naming rules from the retired `.ai/conventions.md` so none are lost. See
`Methodology/AgenticEngineering_Workflow.md` §Where stack knowledge lives.

## Matter naming (carried from `.ai/conventions.md`)

- **Domain / Class live in the folder path only**, so materials can be recategorised without renaming.
- **Filename:** `Material_Variant_Condition_Detail_sNN_vNN.mtlx`. `Condition` defaults to `Clean`,
  and `Detail` defaults to `Base` when nothing special applies.
- **Scale tags:** `s0001 … s100`, plus `sUKN` (the scale table is in `Readme.md` until step 1.3 brings
  the identity spec home under `docs/specs/Ontology/`).

⚠ **This one arrives EARLIER than the other stack docs**, and often before a stack is chosen: a
project starts naming things — phases, research docs, decisions — on day one, and those names are
load-bearing immediately.

## What lands here

- **The casing matrix** — what shape each kind of identifier takes, per layer.
- **The identifier vocabularies** — the prefixes and series this project uses (gate ids, finding
  ids, decision ids, phase and wave names) and **what each one means**.
- **The id registry**, if ids are centrally allocated: who assigns them and when. ⛔ **Record
  which artifact is AUTHORITATIVE** — a doc that lists ids is a record of the registry, not the
  registry itself, and the two drift.
- **Retired names** — when a term is replaced, record the old one and where it went. Two names
  for one thing at the same layer is a bug, and a reader hitting the old word needs to land
  somewhere.

## Relationship to the Glossary

**`docs/Glossary.md` says what a term MEANS. This doc says what a name may LOOK LIKE.** A term
that needs a definition goes there; a rule about form goes here. Where they overlap, the Glossary
carries the one-line definition and points here for the shape.

## What does NOT land here

- **How code is written** → `CodingStandards.md`.
- **Where artifacts live** → `ToolingConventions.md`.
