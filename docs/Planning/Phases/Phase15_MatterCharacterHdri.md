# Phase15 — Matter, Character and HDRI

**Status:** SEEDED (2026-10-14). **Numbered Phase15 by the lead the same day:** *"Lets make these the next phases (Before the scaled grid)"*; Scale Grids, which held the number, is Phase18 and follows these three. A pointer-shell written by `/research` on the lead's word: *"yes record it and seed all three"*. **Starting discovery is a deliberate gate, the lead's call, never a slide.** It is the first of three phases in that order (RD-DS-5): this one, then *Every Entry Says What It Is* ([`Phase16_EveryEntrySaysWhatItIs.md`](Phase16_EveryEntrySaysWhatItIs.md)), then *Character Materials, Their Own Library* ([`Phase17_CharacterLibrary.md`](Phase17_CharacterLibrary.md)).

## Outcome

**The website, Studio and USDLiveView each show Matter, Character and HDRI as three separate things to browse, each by its own taxonomy, from what the library publishes.**

## Why this comes first

The structure is what every consumer builds its browsing on (the lead: *"then we know we have the structure sorted out"*). Today only the website can tell Character from Matter, through a site-file field the library works out from the domain. The engines' catalog carries nothing, so Studio, USDLiveView and export show the 30 character materials as an ordinary Matter domain. Adding contributor and licence first would have consumers build against a shape that is about to change.

## Scope — as known at research (2026-10-14)

The authority until this phase writes its specs: [`261014_R_DownstreamPicture.md`](../Research/261014_R_DownstreamPicture.md) §Resolved (RD-DS-1, RD-DS-4, RD-DS-5), Pass 1 and Pass 4.

**The library's half (this repo):**
- **The three groups as the library's own structure.** The lead's word is *concept*; the library's is **group** ([SiteFile](../../specs/Contract/SiteFile.md) §Groups).
- **Folders.** Character leaves `MatterLibrary/materials/biological/` for a tree of its own, by species and then part. HDRIs already have their own (`MatterLibrary/hdris/`). Generic biological materials (a generic skin pattern, a generic hair) stay in Matter (RD-DS-1).
- **One taxonomy per group:**
  - Matter keeps Domain and Class ([Taxonomy](../../specs/Ontology/Taxonomy.md)).
  - Character runs species, then part. Humanoid today, with parts Eyes, Hair, Skin, Nails, Teeth and Mouth: the six rows the website asked for (Pass 1 F-DS-7).
  - HDRIs run *when* and *sky*, from Poly Haven's own tags.
- **Carried in one shape everywhere:** the group and its taxonomy go **inside each file** (the `.mtlx`'s `imrsv_metadata` block; the `.hdr`'s header, F-DS-10). The catalog Studio reads and the site file project them from there. No sidecar (RD-DS-3).
- **The install layout** in [ReleaseModel](../../specs/Distribution/ReleaseModel.md) shows every folder a release holds (F-DS-1).
- **The Glossary gains *Character* and *group*** as headwords.

**The consumers' half, asked through [`PlatformDependencies.md`](../PlatformDependencies.md)** (their phases, not this one):
- Stage passes the new fields on to its clients.
- Studio's picker and USDLiveView's material dialog browse by group, then by each group's taxonomy.
- The website reads site-file schema 2 (its mirror accepts only 1, measured 2026-10-14) and builds the group row and the HDRI pages.

**Done here when:** the library publishes the structure (dev install and a dev snapshot), the asks are in the ledger, and the lead has seen that each consumer can read it.

## Open questions (settle in discovery)

- The Character folder and name grammar: where the species and part sit in the path and the name, and how a part names the mesh it fits (that last half is *Character Materials, Their Own Library*'s; this phase leaves room for it).
- Which of today's 30 biological articles move. The lead's words point to all of them (*"the complex maps … need to be in characters"*). Any that is generic stays in Matter.
- The key names inside the `.mtlx` and the `.hdr`, and the catalog's `schema_version` step.
- What a consumer built before this phase does with the moved files (the dev install's paths change).

## Discovery Log

*(empty: `/discovery` fills it)*
