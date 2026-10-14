# PhaseTBD — HDRIs in the Library

**Status:** SEEDED (2026-10-14) — not numbered. A pointer-shell written by `/research` on the lead's word (*"seed the phase"*). `/discovery` fills it. **Starting discovery is a deliberate gate, the lead's call, never a slide.**

## Outcome

**A scene's lighting picture (an HDRI) is chosen from the library by name, in the IMRSV app and a USD viewer, and the library is the only place it comes from.** The dev install serves HDRIs before any release holds one.

## Why this is a phase

The library holds materials and nothing else: its specs, catalog, lockfile check, LFS rule, licence list and serve tool each assume a `.mtlx`. An HDRI is a second kind of entry, and a contract change (the catalog's `schema_version` moves). It is one thing a person can see: the platform's app shows a library HDRI, chosen by name, with no copy in the scene. The platform's own HDRI phase waits on it.

## Scope — as ruled at research (2026-10-14)

The authority until this phase writes the specs: [`261013_R_PlatformSkyAsks.md`](../../Research/261013_R_PlatformSkyAsks.md) §Resolved (RD-SKY-1 to 4) and Pass 2's priced table (asks A1 – A8).

- **The kind** (RD-SKY-1): one flat folder, `MatterLibrary/hdris/`, and a top-level `hdris` list beside `materials` in the catalog and the lockfile. [Taxonomy](../../../specs/Ontology/Taxonomy.md) says an HDRI is a kind beside the taxonomy. The Realm stays planned.
- **The name** (RD-SKY-2): `<Name>_<Variant>_vNN.hdr`, unique within `hdris/`, in [Identity](../../../specs/Ontology/Identity.md).
- **The file** (RD-SKY-3): Radiance `.hdr`, 4096 × 2048, refused otherwise by the lockfile check.
- **The catalog** (A2, A3): each entry's fields, one top-level key naming the default HDRI, and `schema_version` moving from 2 to 3 in [RuntimeCatalog](../../../specs/Contract/RuntimeCatalog.md) and [Manifest](../../../specs/Contract/Manifest.md).
- **The dev install** (RD-SKY-4): `tools/releases/serve_to_stage.py` links `hdris` and writes the list.
- **No compression** (RD-SKY-4): one line in [CompressedDistribution](../../../specs/Tooling/CompressedDistribution.md).
- **The small picture** (A4): a 2:1 JPEG per HDRI, named in its entry. *(2026-10-14: the published pictures are called **thumbnails** and are not stored in git, `261014_R_MaterialPipeline.md` RD-MP-5. Discovery reads A4 against that ruling.)*
- **Provenance and licence** (A5): a record per HDRI under `library/provenance/sources/`, made from the library's own download, and an `hdris/` row in `LICENSE-CONTENT.md`. *(2026-10-14: each article carries CC0-1.0 or CC BY 4.0, `261014_R_MaterialPipeline.md` RD-MP-1; withdrawn the same day, CC0 only, `261014_R_RoadmapOrder.md` RD-RO-2. Poly Haven publishes CC0.)*
- **Storage** (A7): `.gitattributes` puts `MatterLibrary/hdris/**` in LFS. About 16 MB per HDRI, with many to come.
- **The first HDRI** (A8): the one every scene uses today, Poly Haven's *industrial_sunset_02_puresky*. The rest are the lead's choice from Poly Haven.
- **The word:** the Glossary's *HDRI* headword, before any spec uses it.

## Open questions (settle during this phase)

- How many HDRIs fit before LFS storage needs the Roadmap's parked *Texture storage beyond Git LFS* (A7)?
- Where the HDRI wish list lives: `library/wishlist.yaml` or a list of its own (A8).
- Whether the rig or the preview tool lights with a library HDRI as well as its fixed dome. That is a later question, not this phase's.

## Consumers and the ledger

The platform's side (its runtime, plugin and app; its web publish check; USDLiveView's launcher) is [PlatformDependencies](../../PlatformDependencies.md) **M10**.

## Discovery Log

*(empty — `/discovery` fills it)*
