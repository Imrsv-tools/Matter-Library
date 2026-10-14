# Phase13 — Materials Described

**Status:** DISCOVERY, Pass 1 (2026-10-14). **Numbered Phase13 and opened by the lead, 2026-10-14:** the invocation, verbatim, *"/discovery materials definitions and numner the phase"* (RD-P13-1). Seeded the same day as a pointer-shell by `/research` on the lead's word (*"Seed all the TBD phases we discovered here"*).
**Ids:** `Q-P13-n` · `F-P13-n` · `RD-P13-n`. Ids cited from research (`F-MP-n`, `RD-WS-n`, `F-RO-n`) keep their own stems.

## Outcome

**Every kept material has a name a person reads, a one-line description and search words. The library publishes everything the website shows about each material in one file beside each release.**

## Why this is a phase

An article's facts live in six records today (F-MP-3), and the words a person needs (a label, a summary, search words, where it came from) do not exist (F-MP-14). The website reads only what the library publishes (RD-WS-1), and the engines' catalog is kept lean by a gate (WS-F2). So the site needs a file of its own, projected from the same records (RD-WS-4). It is the library's other half of *See the Library*, beside *Thumbnails*.

## Scope — as ruled at research (2026-10-14)

The authority until this phase writes its specs: [`261014_R_TheLibrarysSite.md`](../../Research/261014_R_TheLibrarysSite.md) (RD-WS-4, WS-F3, WS-F4) and [`261014_R_MaterialPipeline.md`](../../Research/261014_R_MaterialPipeline.md) Pass 3.

- **The site file:** projected per release from the lockfile, recipes, `.mtlx`, scorecards and provenance. Its shape is a contract spec under `docs/specs/Contract/`. **Its name is not chosen.**
- **The three layers** (F-MP-13): technical (the runtime catalog, unchanged), presentation (the site file), compliance (provenance, licence, origin, approver).
- **The words:**
  - the **label** is derived (split the PascalCase, drop `Natural`, `Clean` and `Base`), with an override;
  - the **summary** and **search words** are written by the agent at build time and confirmed at the review (F-MP-14);
  - the **origin** (procedural · scan · measured · agent-drafted) and the **approver** are recorded (F-MP-18).
- **The parity verdict per Creator port**, carried for the site to show as evidence (WS-F6).

## Open questions (settle during this phase)

- A completeness check before a release (F-MP-15): a gate lane is a lead ruling.
- Whether the batch skill writes the words (a change to `/matter-batch`), or this phase writes them for the articles on disk first.

## Depends on

Nothing to start. *Thumbnails* supplies the pictures it lists. ~~*Two Licences* supplies each article's licence.~~ Every article is CC0-1.0 (RD-RO-2, 2026-10-14).

## Carried in (2026-10-14)

From [`261014_R_RoadmapOrder.md`](../../Research/261014_R_RoadmapOrder.md) Pass 6 and RD-RO-2:
- **First in the order. Its first step is the dev snapshot the platform's site is waiting on** (PlatformDependencies M9): a GitHub pre-release with a `matterlib-` tag, carrying the site file, the rig's pictures at web size, one MaterialX zip per material, and a sha256 for every file (F-RO-24 to F-RO-27).
  - **Real fields only.** A field that does not exist yet (a thumbnail, a summary) is left out, never made up; the site labels the gap.
  - The site drafted a file shape and asked the library to adopt or change it. **Adopt it as a draft contract spec, marked as one**, while only staging reads it.
  - Publishing the pre-release is public and irreversible: the lead's word.
- **The words follow** as its later step: the summaries and search words.
- **A contributor's handle,** when one is given, is carried as a courtesy and for the platform's Forseti tracking (RD-RO-2). Nothing records one today.

## Discovery Log

*(empty — `/discovery` fills it)*
