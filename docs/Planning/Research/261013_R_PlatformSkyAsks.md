# Research — Skies in the library: what the platform asks

**Opened:** 2026-10-13 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `SKY` (ids `SKY-Qn`, `SKY-Fn`). **Pass 1** is written from the platform's side. The library's review of it against its own tree is a later pass, as `260928_R_PlatformAppearanceAsks.md` Passes 5–6 were.
**Requested by:** the IMRSV platform's lead, 2026-10-13, as the first step of a platform phase that follows its current one. The lead ruled the direction; this doc hands the library its half.

**A sky, in this doc:** one high-dynamic-range picture of a whole surrounding, 2:1 latitude-longitude, that lights a scene and is seen behind it — a USD `DomeLight`'s `inputs:texture:file`. The platform's own word for it is *HDRI*.

**Question:** can the library hold skies as a kind of entry beside its materials, so that a consumer takes a scene's sky from the library by name and from nowhere else?

**Extends, does not replace:** [Taxonomy](../../specs/Ontology/Taxonomy.md) (the planned *Realm above Domain*), [RuntimeCatalog](../../specs/Contract/RuntimeCatalog.md), [Manifest](../../specs/Contract/Manifest.md), [ReleaseModel](../../specs/Distribution/ReleaseModel.md).

**Public-repo note.** The platform's planning is private. It is summarised here by what it does with the library and what it needs — no platform paths, code or ruling ids.

**Measured at:** `368a9d9` (2026-10-13), level with `origin/main`.

---

## The short version

- **The platform's rule is that heavy pictures ship once, in the library, and a scene names them.** Every texture already follows it. The sky is the one that does not: each scene carries its own sky file, copied in when the scene is made and uploaded again each time it is published.
- **The lead has ruled the sky follows the rule too** (2026-10-13): a scene **names** a sky from the library, by its bare file name, as it names a material by `<Name>.mtlx`. Nothing is copied into the scene. A Creator cannot bring a sky of their own; the library is the only source.
- **The library has no place for a sky today.** Every entry is a material, in its specs and in its checks. Its own Taxonomy names the way out and has not built it.
- **Eight things are asked** (A1 – A8). None is a material. The first three are what the platform needs before it can build anything; the rest can follow.
- **Nothing here is urgent this week.** The platform's phase starts when its current one closes. The dev install can serve skies long before a release holds one.

---

## Pass 1 — What the platform does with a sky, and what it needs

*Written from the platform's side, 2026-10-13.*

### The sky today, on the consumer's side

- **SKY-F1 — One sky is in use.** Every new scene starts with the same one: Poly Haven's *industrial_sunset_02_puresky*, 4096 × 2048, Radiance `.hdr`, 16 MB. The lead states its source as Poly Haven, CC0; the file's bytes have not been compared with Poly Haven's download, and its source is recorded in no file. Three more, each 8k OpenEXR at 265 – 279 MB, are used as test controls.
- **SKY-F2 — What the consumer's renderer takes.** A 2:1 latitude-longitude picture and nothing else: any other shape is refused. It reads Radiance `.hdr` and OpenEXR by content. It builds six cube faces, each as tall as the file, as 16-bit float, with no resize and one mip. **So a sky's size is its cost:** worked out from that, about 200 MB of graphics memory at 4k and about 800 MB at 8k. Not measured on a card.
- **SKY-F3 — A sky can differ at each point of a scene's story**, as a light's other values can. A scene may name several.
- **SKY-F4 — A bare name resolves in stock OpenUSD.** Measured, OpenUSD 26.05: a `DomeLight` whose `inputs:texture:file` is a bare file name resolves to the file on the default resolver's search path, in memory and from a saved file; with no search path it resolves to nothing. This is the mechanism a material's `<Name>.mtlx` already uses.
- **SKY-F5 — A file of the same name beside the scene's own file wins over the search path.** Same measurement. The platform will look a sky's name up in the library itself and not take the resolver's answer; it is noted here because it bears on how unique a sky's name needs to be.

### What was read in the library

- **SKY-F6 — Every entry is a material.** The runtime catalog's top-level key is `materials` and each entry's payload is a `.mtlx` ([RuntimeCatalog](../../specs/Contract/RuntimeCatalog.md) §Schema). The lockfile check fails an entry that does not resolve to a `.mtlx` (`tools/validators/validate_manifest.py`, the `materials[]` loop). The name grammar's `sNN` is metres per tile ([Identity](../../specs/Ontology/Identity.md)); a sky has no tile.
- **SKY-F7 — The way out is named and not built:** *"A Realm above Domain (planned) is an escape hatch: if the library ever spans beyond elemental matter …"* ([Taxonomy](../../specs/Ontology/Taxonomy.md)). Its example is Buildings.
- **SKY-F8 — A trap in the words.** The Domain **Environmental** is sand, vegetation and liquid. A sky is not one of them. And "category" here means a material's Class on the consumer's side ([Glossary](../../Glossary.md)), so "skies as their own category" has no meaning in the library as written.
- **SKY-F9 — Four mechanisms assume low-dynamic-range tiling textures:** Git LFS covers `MatterLibrary/textures/**` only (`.gitattributes`); the compression table is BC7 / BC5 / BC4 by texture role, with no float format ([CompressedDistribution](../../specs/Tooling/CompressedDistribution.md)); `LICENSE-CONTENT.md` lists content paths by name; and *Texture storage beyond Git LFS* is already in the Roadmap's parking lot.
- **SKY-F10 — The licence rule fits.** *"No pixel ships in a release unless its source is recorded and it is CC0-dedicable, with evidence"*; CC0 libraries are accepted with a URL and a hash (`CONTRIBUTING.md` §2). Poly Haven's skies are published CC0. `Phase03_AgenticMaterialGeneration.md` already notes that a CC0 sky *"would itself be a third-party input"* under that rule.
- **SKY-F11 — The library's own pictures are lit by a flat grey dome**, on purpose (`tools/preview_generators/`). No doc proposes skies as content. This is the first.

### The asks

| # | Need | Why it matters to the consumer | What exists today |
|---|---|---|---|
| A1 | **A sky is found by one bare file name**, unique across the library, the same in a published release and in the dev install. Where it sits and how it is named are the library's. | The scene stores that name and nothing else. Stock USD finds it on a search path, so the name must not collide with another sky's, or with a material's file. | Materials have this: `<Name>.mtlx` under `materials/<domain>/<class>/`. Skies have nowhere. |
| A2 | **The catalog lists skies apart from materials**: an identity, a display name, a version, a status, whether a Creator may pick it, and the payload's path — in a release's catalog and in the dev install's. | The consumer shows a Creator the skies to pick from, and must not offer them as materials or the reverse. | `materials[]` only. The consumer's reader takes that array and drops a key it does not know; an unknown *array* beside it was not tried. Please say whether `schema_version` moves. |
| A3 | **One sky is marked as the one a new scene starts with.** | Every new scene needs a sky before anyone has chosen one. A consumer that hardcodes a file name breaks when the library renames it. | Nothing. The consumer hardcodes one today. |
| A4 | **A small picture of each sky**, shipped with it and named in the catalog. | A sky is chosen by looking at it. The consumer's picker has no picture to show without one. | The library makes preview pictures of materials with its own tools; none is shipped to a consumer, and the consumer's material picker shows none either. |
| A5 | **Each sky's source, licence and hash are recorded** as a texture's are, and the skies' folder is on the licence file's list of content. | The sky in use today has no recorded source anywhere. The library's rule would close that by construction. | `textures[].provenance`, and `library/provenance/sources/`. |
| A6 | **One stated size and one file format for every sky**, 2:1 latitude-longitude. | The consumer's cost is set by the file (SKY-F2). One size makes that cost known and the same for every scene. | Nothing stated. The sky in use is 4096 × 2048 Radiance `.hdr`. |
| A7 | **Skies are inside the release folder**, so a release stays self-contained, and the checkout tracks them as it tracks textures. | A packaged build carries one release folder and nothing else. A sky kept beside it would be listed and not found. | The self-contained rule the packaged-build asks already put (`261011_R_PlatformBuildInstallAsks.md` A1). LFS covers the texture tree only. |
| A8 | **The first sky is the one in use today**, so a new scene looks as it does now. Which others, and how many, is the lead's choice from the library's own wish-list. | No scene's look changes on the day the consumer switches over. | The file is on the platform's side; its source is Poly Haven (SKY-F1). |

### Questions for the library

- **SKY-Q1 — Is a sky the first Realm, or something plainer?** A second top-level array and a folder beside `materials/` would serve the consumer as well. The Realm is the library's own recorded intent; which one is its ruling.
- **SKY-Q2 — What is a sky's name?** The material grammar does not fit. Two things the consumer leans on: the scene stores **the file's bare name with its extension**, because that is what a stock resolver finds — so a change of file format is a change of name; and a sky needs a version it can advance, as `vNN` does for a material.
- **SKY-Q3 — What size?** The consumer's hypothesis is 4096 × 2048, because it is what every scene has today. Whether that holds up as a backdrop in a headset is the consumer's to measure and report here.
- **SKY-Q4 — Can the dev install serve skies before any release holds one**, as it serves draft materials?
- **SKY-Q5 — Does a sky go through the compression step?** The consumer reads the float file as it is today. No compressed float format is asked for.

### What the platform does next

- Nothing waits on the library this week. The platform's phase follows its current one.
- With A1 – A3 in the dev install, the platform can build its side and be seen working.
- A6's size is reported back here once it has been looked at in a headset.
- The platform's two other consumers of this change are asked in their own repos: its web side (one rule of its publish check) and USDLiveView (its launcher's search path).

### A suggested ledger row

For `PlatformDependencies.md`, *From IMRSV to the Matter Library*. The library writes its own row; this is a draft.

> **M9** · **Skies as a kind of library entry** (2026-10-13): a sky found by a bare file name, listed in the catalog apart from materials, one marked as a new scene's default, each with a small picture, a recorded source and one stated size; inside the release folder. · *The platform's lead ruled that a scene names its sky from the library and carries no sky file; a Creator cannot bring their own.* · Matter Library (the kind, the first skies) · the platform's runtime, plugin and app (the consumer side) · `261013_R_PlatformSkyAsks.md` A1 – A8 · OPEN

---

## Pass 1, addendum — three rulings since (2026-10-13)

*From the platform's side, the same day. The platform's lead answered three things that bear on the asks above.*

- **The word.** The library's word for the thing is **HDRI**: the library holds and serves HDRIs. The platform's app shows a Creator a *Sky* on its own screens; that word is the app's and asks nothing of the library. **So read "sky" in this doc as "HDRI" wherever it names what the library holds.** The asks are unchanged. This doc's title and its ids (`SKY`) are left as written.
- **The size — SKY-Q3 is answered, and so is A6's half of it.** 4096 × 2048 for every HDRI. The lead: *"4k I think is fine"* — it is what every scene has shown in the headset. The file format is still the library's to state.
- **Which HDRIs — A8.** The first is the one in use today. More follow from Poly Haven, the lead's choice, when the kind is set up in the library: *"I will be getting many more open sky HDRIs from Polyhaven when we set it up in the Matter Library"*.

---

## Pass 1, second addendum — what the consumer's own code says of five of the asks (2026-10-14)

*From the platform's side. Read in the consumer's code; nothing was run. Nothing new is asked — these are facts the library may want in hand before it rules.*

- **A2 and SKY-Q1 — a second list beside `materials` is safe; a catalog without `materials` is not.** The consumer's reader takes `release` and the `materials` array by name, and nothing else. A new top-level list beside `materials` is not seen by a consumer built before it, and does it no harm. A catalog with no top-level `materials` array is refused whole. The consumer does not read `schema_version` at all. *(Pass 1 said an unknown array "was not tried". It is now read; it is still not run.)*
- **A1 — where an HDRI sits bears on how it is found.** The consumer hands stock USD the library's folders as a search path, one entry for each folder that holds payloads; a stock search path does not look into sub-folders. Materials give it one entry per `materials/<domain>/<class>/`. One flat folder of HDRIs would be one entry.
- **A6 — of the two formats, Radiance `.hdr` is the one every part of the consumer reads.** Its renderer reads `.hdr` and OpenEXR. Its texture service, which hands a picture's pixels to the app, reads `.hdr` and not OpenEXR. The consumer has not yet chosen which of the two carries an HDRI; `.hdr` keeps both open.
- **A4 — the small picture is a PNG or a JPEG.** The consumer's picture card draws those two and no other. It shows a picture whole, so a small picture in the HDRI's own 2:1 shape fills it.
- **SKY-Q4 — the dev install is made by the library's own serve tool.** `tools/releases/serve_to_stage.py` links `materials` and `textures` into the consumer's runtime and writes a catalog of `materials`. HDRIs in the dev install would be a third link there and the catalog's new list — the library's tool, and so the library's change.

---

## Pass 2 — the library's review (2026-10-14)

*From the library's side. Read against this tree at `42e26fa`; nothing was built or run. The lead tied the platform's asks to the platform's issue-sweep phase, 2026-10-14. That phase built the dome's tint and left the move of its sky to the library for the platform's next phase. That next phase is now in discovery. It names this review as the first thing it waits on: its own work can be seen running only once the dev install holds HDRIs (A1 – A3). This pass says what the library's tree confirms and what each ask costs. It recommends an answer to each question. **The rulings are the lead's.***

### The platform's reads of the library, checked

- **SKY-F12 — F6 to F11 hold against the tree**, with one narrowing:
  - **F6.** The lockfile check resolves each id to `<id>_<version>.mtlx`, falling back to a bare `<id>.mtlx` (`tools/validators/validate_manifest.py:120-121`). The dev catalog is `{schema_version, release, materials}` and nothing else (`tools/releases/serve_to_stage.py:68`).
  - **F7.** The Realm is planned, in [Taxonomy](../../specs/Ontology/Taxonomy.md) §Realm, and it is also in the Roadmap's parking lot.
  - **F9.** `.gitattributes` puts `MatterLibrary/textures/**` alone in LFS. `LICENSE-CONTENT.md` lists each content path by name.
  - **F10.** `CONTRIBUTING.md` accepts a CC0 library *"recorded with the source URL and a hash of what you shipped"*.
  - **F11, narrowed.** The preview tool lights with a dome picture of its own (`tools/preview_generators/make_preview.py`, `dome_env.png`). That it is a flat grey was not opened here.
- **SKY-F13 — the library's own Glossary has no *HDRI* headword.** The platform's lead ruled the word on 2026-10-13: the library holds and serves **HDRIs**, and the platform's app calls one a *Sky*. The library's working agreement says to fix the Glossary before using a new term. So the headword is owed before any spec says *HDRI*. It lands with the first durable doc that names one. This research doc does not count, and it says *HDRI* below.
- **SKY-F14 — the catalog has bumped its version once before, for a smaller change.** `schema_version` went from 1 to 2 for the additive `creator_selectable` field ([RuntimeCatalog](../../specs/Contract/RuntimeCatalog.md) §Schema). The consumer reads no `schema_version` (second addendum). The library's contract still owns that number, and it moves only in a contract phase. So an `hdris` list is a contract change: it is built by a phase, not a quick fix.

### The questions, as the library reads them — recommended answers, for the lead to rule

- **SKY-Q1 — a second kind beside materials, not the first Realm.** *Recommended.* The Realm is written for *composite matter*, for example Buildings. It brings that matter's own taxonomy below it, and the five-level query vector. An HDRI has no Domain, no Class, no master, no Creator ports and no tile. Putting it under a Realm would give it levels it never fills.
  - **The plainer shape:** one flat folder beside `materials/`, `MatterLibrary/hdris/`, and one top-level `hdris` list in the catalog and the lockfile.
  - **Why it suits the consumer:** a flat folder is one search-path entry (second addendum, A1). A second list is invisible to a consumer built before it.
  - **What the Realm keeps:** it stays planned, for composite matter. [Taxonomy](../../specs/Ontology/Taxonomy.md) gains a line that an HDRI is a kind **beside** the taxonomy, not in it. Nothing specified is removed.
- **SKY-Q2 — the name: the material grammar's shape, without its scale tag.** *Recommended:* `<Name>_<Variant>_vNN.hdr`, in PascalCase tokens. For example, `IndustrialSunset_PureSky_v01.hdr`. The tokens are the library's choice; the source's own id goes in the provenance record, not the name.
  - **Dropped:** `sNN`, because an HDRI has no tile. The size, because one size is ruled.
  - **Kept:** the character budget, because it costs nothing. The version follows the material's rule ([Identity](../../specs/Ontology/Identity.md) §Two version axes), so `_vNN` advances on a changed picture.
  - **The file format is part of the name** (Q2's first point), so it is fixed once, by A6.
  - **No clash with a material:** the extensions differ, and the two folders are separate search-path entries. **Unique within `hdris/`** is checked as material names are.
- **SKY-Q4 — yes, and it is the cheapest unblocker.** The dev install is the library's own tool (second addendum). `serve_to_stage.py` links `materials` and `textures` (`:175-176`). It would link `hdris` beside them and write the `hdris` list. That is a small change to the tool, but its list is the catalog shape of SKY-F14, so it follows Q1's and Q2's rulings. It is not built ahead of them.
- **SKY-Q5 — no.** The compression table is low-dynamic-range BCn by texture role ([CompressedDistribution](../../specs/Tooling/CompressedDistribution.md)). An HDRI ships as its file, and that spec gains a line that HDRIs skip the step.

### The asks, priced

| # | The library's answer | Size |
|---|---|---|
| A1 | `MatterLibrary/hdris/<Name>_<Variant>_vNN.hdr`, flat, unique there (Q1, Q2) | in the phase |
| A2 | A top-level `hdris` list beside `materials`, the same in a release's catalog and the dev catalog. Each entry carries id, display name, version, status, `creator_selectable`, payload path and preview path. `schema_version` moves from 2 to 3 (SKY-F14) | the phase's contract step |
| A3 | **One top-level key naming the default HDRI's id**, not a flag on each entry, so two defaults cannot be written. The lockfile check fails a default that names no listed HDRI | in the phase |
| A4 | A 2:1 JPEG made from each HDRI and shipped beside it, named in its entry (the consumer draws PNG or JPEG, second addendum). The library has no tool for it today: its preview tool renders a material on a sphere. The tool is new, and small | in the phase |
| A5 | As a texture's: a record under `library/provenance/sources/` with Poly Haven's URL, CC0 and a hash. `LICENSE-CONTENT.md` gains an `hdris/` row. **This also closes F1's open point:** the library records the file it downloads from Poly Haven itself, not the platform's copy | in the phase |
| A6 | **Radiance `.hdr`.** Every part of the consumer reads it; OpenEXR reaches its renderer only (second addendum). 4096 × 2048 is ruled. The lockfile check refuses any other size or shape | in the phase |
| A7 | Inside the release folder, as `materials/` and `textures/` are. `.gitattributes` gains `MatterLibrary/hdris/**` for LFS. **A cost to name:** one HDRI is about 16 MB (F1), and *"many more"* are coming (the lead, first addendum). That goes on the LFS quota the website research already flagged (`261014_R_TheLibrarysSite.md` WS-F1), and onto *Texture storage beyond Git LFS* in the Roadmap's parking lot | in the phase; the storage is a later question |
| A8 | The first HDRI is the one in use, downloaded again from Poly Haven by the library (A5). The rest are the lead's choice from Poly Haven. Whether they go on `library/wishlist.yaml` (materials today) or a list of their own is the phase's call | in the phase |

- **SKY-F15 — the ledger id the platform suggested is taken.** On 2026-10-14 M9 became *What the website needs from each release*. The HDRI row would be **M10**, with the platform's draft text otherwise unchanged.
- **SKY-F16 — what this comes to: one library phase, and nothing to build before the rulings.** A1 – A8 belong together. They share a folder, a name, a catalog list and a contract number. Each depends on Q1 and Q2. Nothing here is a one-sitting quick fix ahead of those rulings: even the serve tool's change writes the contract's shape. **Proposed, unnumbered:** *HDRIs in the library*. It covers the kind, its name, the catalog's `hdris` list, the lockfile check, provenance, LFS and the licence row, the serve tool, the preview, the Glossary's headword and the first HDRI. Its Outcome: *a consumer names a scene's HDRI from the library, and the dev install serves it.* It runs ahead of the platform's HDRI phase, which waits on it.

---

## Status

- **Passes:** 1 and its two addenda (the platform's side) · 2 (the library's review, 2026-10-14).
- **Answered:** SKY-Q3, 4096 × 2048. **Recommended, for the lead to rule:** SKY-Q1 (a second kind, `hdris/`, beside materials; the Realm stays planned) · SKY-Q2 (`<Name>_<Variant>_vNN.hdr`) · SKY-Q4 (yes, through the library's serve tool, after the rulings) · SKY-Q5 (no compression) · A6's format (Radiance `.hdr`).
- **Open:** A1 – A8, all for one library phase (SKY-F16). The Glossary's *HDRI* headword is owed (SKY-F13). The ledger row M10 is offered (SKY-F15).
- **▶ Next:** the lead rules Q1, Q2 and the format. On his word, a **Roadmap seed** for *HDRIs in the library* (a `PhaseTBD_` stub) and the ledger row M10, then `/discovery` on that phase. The platform's HDRI phase waits on it.
