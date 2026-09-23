# Platform dependencies — asks between the Matter Library and its consumers

**What this is:** every piece of work that **a consumer** (the IMRSV platform: Stage runtime, UE plugin, Studio, its docs; USDLiveView) needs to do for the Matter Library to stand alone, and every ask a consumer has of us. It is recorded **here rather than in handback prose**, so none goes missing. This repo does not edit consumer repos (`.ai/commands/LOCAL_DELTAS.md` §Separation). Each ask names the consumer that owns it and the Matter phase it pairs with.

*Opened 2026-09-23 (Phase01 step 1.5). Status words: `OPEN` (not started) · `IN PROGRESS` · `DONE` · `DROPPED` (with a date and a reason).*

## From the Matter Library to IMRSV

| # | Ask | Why | Owner | Pairs with | Status |
|---|---|---|---|---|---|
| P1 | **Install and read a published release bundle** instead of the hand-synced mirror of the catalog and `.mtlx` files kept in Stage's test assets. The mirror stays a test fixture only. | R1: consumers take releases, never this repo's checkout. It also removes "a catalog promotion forces a Stage commit". | Stage | release bundle + consumer contract | OPEN |
| P2 | **Deploy from a bundle.** The dev deploy script currently assembles each installed release from three sources: the Stage mirror, this repo's current textures, and a staging folder. It copies the same `.mtlx` set into every release folder. It should install one bundle per release. | R1; per-release payloads must actually differ, and installed releases must be reproducible. | Studio deploy tooling | release bundle | OPEN |
| P3 | **Ship the library with packaged builds.** Packaged Studio builds stage the Stage runtime but not a Matter Library install, so a shipped build finds no catalog. | Without it, no end user gets Matter materials. | UE plugin build / Studio packaging | release bundle | OPEN |
| P4 | **Route articles to masters from release data**, using the per-article master token, instead of the class → master table compiled into the plugin. This needs a way to carry the token from Stage to the renderer. | R14: the master contract is data. A new class or a routing exception should be a library change, not a code change. | Stage + UE plugin | release bundle + consumer contract (the catalog schema bump) | OPEN |
| P5 | **Re-author the 7 masters natively on Substrate.** Today they are legacy-model graphs, converted automatically because Studio runs with Substrate on. | R15: Unreal 5.8+ with Substrate is the target; the conversion was never chosen or tested as the target. | UE plugin | parity baselines | OPEN |
| P6 | **Drive the picker's category filter from the taxonomy classes** instead of a hard-coded category list. | The picker should show the library's real classes (cementitious, textile, mineral, …). | Studio | — | OPEN |
| P7 | **Honour the active-release selector** instead of scanning every installed release. | Release activation must mean the same thing in every consumer. | USDLiveView | release bundle | OPEN |
| P8 | **Move the `fixture_sync` equality check to the consumer side.** It compares this repo's releases with the consumer's mirror, lives in this repo's validators, and passes silently when the mirror isn't found. | R1: a producer gate must not depend on a consumer's tree. | Stage (receives it) · this repo (removes it) | one-command check | **Half done (Phase02, 2026-09-23):** removed from this repo's gate; `check_fixture_sync.py` kept as the tool to hand over. Still open: Stage adopting it, and `promote_release.py`, which still runs it (release-bundle phase). |
| P9 | **Reduce the platform's `MatterLibrary/` spec tree to pointers into this repo**, keeping only consumer-side docs (see [`docs/specs/Consumers.md`](../specs/Consumers.md)). Repoint the platform glossary's Matter terms to [`docs/Glossary.md`](../Glossary.md). | R2: the specs came home on 2026-09-23. Two copies would drift. | Platform docs | — | OPEN |
| P10 | **Retire this repo as a platform submodule** once P1–P3 land, and reference it as an external track. | R1: separate projects, joined only by releases. | Platform umbrella repo | after the release bundle | OPEN |

## From IMRSV to the Matter Library

| # | Ask | Why | Owner | Pairs with | Status |
|---|---|---|---|---|---|
| M1 | **Master materials for skin, cloth and hair** for the platform's humanoid-character Appearance work. Whether it integrates the library or side-lines it is still open on the platform side. | The platform's one live pull on the library (2026-09-23). | Matter Library (masters / coverage) — pending the platform's decision | to be seeded | OPEN |
| M2 | **Open Matter issues in the platform tracker** (emissive colour not adjustable by Creators; cross-renderer view-transform match; the portable export's scale). They stay in the platform tracker for now because they may reach into the plugin and Studio (lead, 2026-09-23). | R4. | shared | contract / parity work | OPEN |

## How to use this file

- **Adding an ask:** one row, in the right table, with an owner and the Matter phase it pairs with. Scope, design and evidence live in that phase's doc, not here.
- **Closing an ask:** set `DONE` with the date. Do not delete the row.
- **Consumers read this file; they are not edited from here.**
