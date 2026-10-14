# PhaseTBD — The Library Console

**Status:** SEEDED (2026-10-14) — not numbered. A pointer-shell written by `/research` on the lead's word (*"Seed all the TBD phases we discovered here"*). `/discovery` fills it. **Starting discovery is a deliberate gate, the lead's call, never a slide.**

## Outcome

**The IMRSV team opens one page to:**
- review new materials (the rig's sheet, the thumbnails and the words), and keep each one or send it back with a note;
- choose which materials go into each library version;
- see each material's provenance.

## Why this is a phase

Today a review is the agent opening a picture and the lead answering in chat (Phase11), and a release is a hand-edited lockfile. The lead: *"a front that we can use to view and evluate them, update versions, keep whatever provanence might exist etc"* (RD-MP-7). It is the screen the flow's three human acts happen on: review, cut, approve (F-MP-22).

## Scope — as ruled at research (2026-10-14)

The authority until this phase writes its specs: [`261014_R_MaterialPipeline.md`](../../Research/261014_R_MaterialPipeline.md) Pass 6, F-MP-24 and §Resolved.

- **For the IMRSV team**, not for Creators (RD-MP-7). The Creator's side (choosing and updating a release) lives in each consumer.
- **Runs on the library service** (RD-MP-11), with its code in this repo. **Git stays the source:** the console writes through the existing tools (`wishlist.py`, the lockfile, the projector) and commits.
- **What it shows** (F-MP-24):
  - **the review queue:** sheet, thumbnails and words side by side; keep, or redo with a note;
  - **the release composer:** pick kept articles; the difference from the last release; a suggested semver; deprecate and retire;
  - **the wish list:** add and reorder;
  - **what is stale** (F-MP-23).
- **Approvals stay the maintainer's act** (`promote_release.py`). The console may prepare one; it never makes one.

## Open questions (settle during this phase)

- Sign-in for the team (its own, or IMRSV accounts, which already cross domains on the platform's side).
- How it overlaps *Version Management* (the rules) and the *Matter Manager* seed (`260923_R_StandaloneSetup.md` seed 7). This console is the Manager's maintainer half.

## Depends on

*The Library Service*; *Thumbnails* (for what it shows); *Materials Described* (for the words).

## Discovery Log

*(empty — `/discovery` fills it)*
