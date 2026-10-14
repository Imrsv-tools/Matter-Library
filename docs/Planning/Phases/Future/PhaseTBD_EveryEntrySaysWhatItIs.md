# PhaseTBD — Every Entry Says What It Is

**Status:** SEEDED (2026-10-14), not numbered. A pointer-shell written by `/research` on the lead's word: *"yes record it and seed all three"*. **Starting discovery is a deliberate gate, the lead's call, never a slide.** It is second of three, after *Matter, Character and HDRI* ([`PhaseTBD_MatterCharacterHdri.md`](PhaseTBD_MatterCharacterHdri.md)), whose structure it fills (RD-DS-5).

## Outcome

**Every material and HDRI says who contributed it, its licence, its name and its place in the taxonomy, from inside its own file. Studio, USDLiveView and the website read it from the library, and Forseti can tell who gave what and how each one is doing.**

## Why this is a phase of its own

The lead: *"I want Materials to work like Assets and Compositions.... same thing... people contribute they are tracked,, the is a license it is added,,, they can browse byt a taxolongy... Avoid sidecars, we can put things in MTLX, and in the case of HDRI... that is totally in our control. We are doing Materal tracking for FORSETI!"* (RD-DS-3). It changes what every file carries, and it reverses a standing rule: licence and provenance were kept out of the engines' catalog on purpose (`no_projection_guard`; RD-DS-2).

## Scope — as known at research (2026-10-14)

The authority until this phase writes its specs: [`261014_R_DownstreamPicture.md`](../../Research/261014_R_DownstreamPicture.md) §Resolved (RD-DS-2, RD-DS-3) and Pass 4 (F-DS-9 to F-DS-12).

- **In the `.mtlx`:** the existing `imrsv_metadata` block gains the contributor and the licence. It already carries the master, scale, domain and class (F-DS-9). An export carries them with no extra step.
- **In the `.hdr`:** the header carries the id, version, licence and contributors. Blender reads a header stamped this way with identical pixels (F-DS-10, probe 2026-10-14). USD's own reader and Unreal's importer are not yet run.
- **The catalog and the site file project them from the file,** as the dev catalog already does for the master. `no_projection_guard` narrows to what still stays out.
- **Tracking use is the consumer's** (F-DS-12). The library writes a stable id and the contributor into every file. A material bound in a composition, and a scene's sky, carry that id, contributor and licence, the way the platform's assets already do. The ask goes in the ledger.
- **It also answers** the platform's HDRI asks A9 (credit) and A10 (tagging) ([`261013_R_PlatformSkyAsks.md`](../../Research/261013_R_PlatformSkyAsks.md) Pass 3), and the website's `edited_from` ask (F-DS-7).

## Open questions (settle in discovery)

- How much of an HDRI's credit goes in its header: a short line, or Poly Haven's whole description and tags.
- The byte change: the record's checksum then describes Poly Haven's original, and Phase14's *byte-identical default* no longer holds (F-DS-10).
- What stays producer-side (recipes, the per-HDRI records), as the source the files are written from (F-DS-11).
- The contributor's form: a handle, as RD-RO-2 already carries for Forseti.

## Discovery Log

*(empty: `/discovery` fills it)*
