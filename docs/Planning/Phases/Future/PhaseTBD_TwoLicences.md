# PhaseTBD — Two Licences

**Status:** SEEDED (2026-10-14) — not numbered. **Withdrawn the same day** (the lead: *"YES... CC0 for materials... we decided that... material are CC0 but we will carry a handle if one is provided as courtesy and Forseti tracking"*, `../../Research/261014_R_RoadmapOrder.md` RD-RO-2): materials stay CC0 only, so nothing here is built. Kept so its intent survives (Don't Delete Spec Functionality); the handle lands in *Materials Described*. A pointer-shell written by `/research` on the lead's word (*"Seed all the TBD phases we discovered here"*). `/discovery` fills it. **Starting discovery is a deliberate gate, the lead's call, never a slide.**

## Outcome

**A material can be published under CC0 or CC BY 4.0, and every consumer shows each material's licence and the credit a CC BY material asks for.**

## Why this is a phase

The library was CC0-only (R13). The lead allowed CC BY 4.0 beside it on 2026-10-14 (RD-MP-1, *"inline with our asset library and composition sharing approach"*), with CC0 the default (RD-MP-8). That reaches the contract, a gate, every consumer, and the words the project describes itself with (F-MP-36). It is one thing a person can see: a CC BY material, credited where it is used.

## Scope — as ruled at research (2026-10-14)

The authority until this phase writes its specs: [`261014_R_MaterialPipeline.md`](../../Research/261014_R_MaterialPipeline.md) §Resolved (RD-MP-1, RD-MP-8) and F-MP-36.

- **One licence per article,** CC0-1.0 by default, CC BY 4.0 by the contributor's choice or forced by a CC BY input. Recorded in the recipe, the lockfile and the catalog.
- **An attribution list** in each release for its CC BY articles.
- **The provenance gate** (`validate_manifest.py`, CC0-only today) widens to the two licences. "Royalty-free" sources still do not qualify.
- **The words:** `CONTRIBUTING.md`, `LICENSE-CONTENT.md`, `_Architecture.md` §Governance, the Glossary's *Matter Library* line, `Experience_MatterLibrary.md`.
- **Consumers show the credit:** the website (RD-WS-1; the platform's), the Blender library, Studio (PlatformDependencies, a new ask).

## Open questions (settle during this phase)

- Where a CC BY article's attribution text comes from (the contributor's name as they give it, and the source's own credit line).
- Whether the runtime catalog carries the licence (it carries no provenance today, and `no_projection_guard` keeps it out) or only the site file and the attribution list do.

## Discovery Log

*(empty — `/discovery` fills it)*
