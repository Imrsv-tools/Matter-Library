# Phase16 — Every Entry Says What It Is

**Status:** BRIEF READY (2026-10-14), **one lead call open** (§Blockers), **executes after Phase15** (RD-DS-5). Opened by the lead's `/discovery P16` the evening it was numbered (*"Lets make these the next phases (Before the scaled grid)"*, RD-DS-6), while Phase15's own discovery ran in parallel. Seeded by `/research` on *"yes record it and seed all three"*. It comes after *Matter, Character and HDRI* ([`Phase15_MatterCharacterHdri.md`](Phase15_MatterCharacterHdri.md)), whose structure it fills, and before The Library Service ([`Phase17_LibraryService.md`](Phase17_LibraryService.md); RD-DS-7).

## Outcome

**Every material and HDRI says who contributed it, its licence, its name and its place in the taxonomy, from inside its own file. Studio, USDLiveView and the website read it from the library, and Forseti can tell who gave what and how each one is doing.**

**The library's half, which this phase delivers:** the facts are in every file, and every file the library serves or publishes (the dev install's catalog, the site file) carries them. **Reading them in Studio, USDLiveView and the website is each consumer's own work**, asked in the ledger (P25, P26, M11). Seeing *how each one is doing* happens where an entry is used, so it is also the consumer's (F-DS-12).

## Why this is a phase of its own

The lead: *"I want Materials to work like Assets and Compositions.... same thing... people contribute they are tracked,, the is a license it is added,,, they can browse byt a taxolongy... Avoid sidecars, we can put things in MTLX, and in the case of HDRI... that is totally in our control. We are doing Materal tracking for FORSETI!"* (RD-DS-3). It changes what every file carries, and it reverses a standing rule: licence and provenance were kept out of the engines' catalog on purpose (`no_projection_guard`; RD-DS-2).

---

## The Brief

### First human test

**Where:** the lead's Blender on the library machine, with the Matter Asset-Browser library the agent has regenerated **and installed** (the installed library, not the repo's copy).

1. **Asset Browser → Matter Library → Copper verdigris** (engineered / metal). The asset sidebar shows **Author** = `MatterBot` and **License** = `CC0-1.0`, and the catalog path shows its place in the taxonomy, as today. *Judge: the material says who gave it and under what licence.* Today the sidebar reads `IMRSV` for every article (hard-coded) and has no licence (F-P16-2).
2. **The same for a character material (a skin) and a material the library made from a script (the UV grid).** *Judge: it holds across the library, not only for the pilot's twelve.* The three are picked by their files' metadata, read after step 16.1, never by their names.
3. **HDRIs: no click. This is a waiver, to be confirmed by the lead** (unless you say otherwise). No surface the lead uses shows an HDRI's credit yet: USDLiveView and Studio read it in their own phases (P25, P26), and the website's mirror accepts only one site-file schema (F-P16-9). What the lead gets instead is the agent's evidence, written into the step's log:
   - the stamped header, read back;
   - the dev catalog's entry for the default sky;
   - the sky's pixels, identical before and after, in Storm and in Blender.

**Reconciled click by click:** clicks 1 and 2 are reachable at the end of 16.1. Click 3's evidence comes from 16.2. Every tool a click uses (Blender) runs on the library machine.

### In now

| What | Step |
|---|---|
| Every `.mtlx`'s `imrsv_metadata` gains **`contributor`** (a handle) and **`licence`** (`CC0-1.0`). The assembler writes both from the recipe. The 95 on disk are stamped in place. | 16.1 |
| **The recipe gains `contributor`.** The licence is not a recipe field: it is `CC0-1.0` library-wide (RD-RO-2). | 16.1 |
| **Blender's asset library reads both from the file** into Blender's own `author` and `license` fields. | 16.1 |
| **The pilot `matterlib-0.1.0` is re-frozen in place**, since 12 of its `.mtlx` files change. The lead's promote command is handed over at the start of the close. | 16.1 |
| **Every HDRI's `.hdr` header carries** its id, version, name, licence, contributor and full credit (RD-P16-2), and Phase15's `group`, `when` and `sky` (RD-P15-4). Where the stamp is made is Blocker 2. | 16.2 |
| **The catalog entries carry `contributor` and `licence`**, for materials and HDRIs alike, and each HDRI also carries its **`credit`** (A9). They are projected from the files into the dev catalog (RD-DS-2, RD-P16-8). | 16.2 |
| **The site file:** `contributor` stops being *(planned)*; `credit.edited_from` becomes a name and an address (M11 (4)); each HDRI's `description` drops the source's resolution claim (M11 (3)). A dev snapshot is built, and published at the lead's word. | 16.3 |
| Specs: MaterialXTemplate (the block), RuntimeCatalog (the fields), SiteFile, Identity §HDRI names (the header). CREDITS.md's *"per-material credit … is planned"* line, and its *"the first 12 articles"* credit (RD-P16-11). Ledger notes on P26, M10 and M11. | at the close |

### Not now

| Not now → where | What it will consume from this phase |
|---|---|
| **The group and each group's taxonomy** in the `.mtlx` files, the dev catalog and the site file (Character as a group; HDRIs by *when* and *sky*) → **Phase15**. *Writing an HDRI's `group`, `when` and `sky` into its header is this phase's: 16.2's stamp (RD-P15-4).* | the same metadata block and dev-catalog entry |
| **A10, each HDRI's tagging**, on the dev catalog's HDRI entries → **Phase15**, whose HDRI taxonomy is built from those tags (RD-P16-9; accepted there, RD-P15-4) | — |
| **The release projector, and narrowing `no_projection_guard`** → the first release after this phase (*Release Bundle*), as `master` was handled and as Phase15's group is (RD-P15-6, RD-P16-8) | the dev catalog's field names; F-P16-3 (the guard must check keys) |
| **Reading and showing the facts** in Stage, Studio's picker, USDLiveView and the website → the consumers (P25, P26, M11) | the catalog's `contributor`, `licence` and `credit` fields, and the `.mtlx` and `.hdr` fields |
| **Linking a handle to an account; counting use for Forseti** → the platform (Phase13's deferral; F-DS-12) | the `contributor` field |
| **Stamped HDRIs in a real release** → *Release Bundle and Consumer Contract* | the stamp tool built here |
| **HDRIs as Blender World assets** → *Blender from a Release* | the header's fields |
| **The exporter writing the facts onto an exported material prim** (`assetInfo`) → P26's consumer half, or the export phase the lead calls *"not implemented yet"* (RD-DS-3) | the `.mtlx` fields. A complete-portable export already carries them, because it copies the `.mtlx`. |
| **Unreal's HDR importer on a stamped file** → a check on the machine with Unreal, handed off at 16.2 | the stamped file |

### The reuse check

**What the stack already provides, reused unchanged:**
- **The metadata block** `imrsv_metadata`, which already carries the master, scale, domain and class (MaterialXTemplate). The dev catalog already projects `master` out of it (`working_tree.master_of`). The new fields follow the same path (F-DS-9).
- **Blender's own asset metadata.** `AssetMetaData` has `author`, `license`, `copyright` and `description` (Blender 5.2.2, measured). The generator only has to fill them. No add-on panel is needed.
- **The Radiance header.** Readers skip header lines they do not know. Blender reads a stamped file pixel for pixel (F-DS-10), and so does Storm (F-P16-1).
- **Each HDRI's record** (`library/provenance/sources/hdris/<id>.yaml`) already holds the full credit. The stamp is written from it, and the record stays the producer's source (RD-P16-5).
- **The catalog's derive path** (`project_runtime_catalog.derive_entry`, shared by `serve_to_stage.py`), and the site file's builder `build_snapshot.py`, which already writes `licence`.

**Each new layer, and the gap that justifies it:**

| New | Beside | The gap |
|---|---|---|
| A **stamp** for `.hdr` headers (a small function in `tools/releases/hdris.py`) | the importer, which keeps Poly Haven's bytes | nothing writes into an `.hdr` today |
| A **one-time stamp** of the 95 `.mtlx` files: an anchored insert of two inputs into the existing block | the assembler, which writes them from now on | re-assembling 95 articles from their recipes risks changing more than two lines. The insert does exactly two (RD-P16-10) |

### Decisions that bind

*Carried from research and earlier phases:*
- **RD-DS-2:** licence and name reach the engines as fields on each catalog entry, as the name and class already do. This overrides `no_projection_guard` for these fields.
- **RD-DS-3:** the source of the facts is the file itself (`.mtlx`, `.hdr`). The catalog projects from it. No sidecars.
- **RD-DS-5, refined by RD-DS-7:** Phase15, then this phase, then The Library Service (Phase17), Thumbnails (Phase18), Character Materials (Phase19) and Scale Grids (Phase20). The lead: *"so we can get the entire chain establsihed recategorized, documented and working correctly before we add more materials"*.
- **RD-RO-2:** materials are `CC0-1.0`, and only CC0. A contributor's handle, when one is given, is carried as a courtesy and for Forseti tracking; it is never a licence condition.
- **RD-WS-1 / F-RO-26:** the library publishes no invented fact, and an absent field means *not known yet*.
- **Pre-release, no release ceremony** (`AI_WorkingAgreement.md` §Settled practices). Files are fixed forward in place, and the pilot is re-frozen in place.

*Minted here.* These close the seed's four questions, and each holds unless you say otherwise:
- **RD-P16-1 — The key is spelled `licence`**, as the site file already publishes it. The provenance blocks' `license` stays as it is (producer-side).
- **RD-P16-2 — An HDRI's header carries its id, version, name, licence and contributor, plus the full credit** that A9 lists:
  - the source and its address;
  - the HDRI's page there;
  - each author, with their role;
  - each sponsor, with their link;
  - the HDRI it was edited from, as a name and an address;
  - Phase15's `group`, `when` and `sky`, under the spellings Phase15 lands (RD-P15-4).

  The source's description and raw tags stay out. The description stays in the record and the site file. The tags feed Phase15's taxonomy. *(Seed question 1: a short line, or the whole description.)* The probe carried a 400-character line and UTF-8 text with no effect on the pixels (F-P16-1).
- **RD-P16-3 — `edited_from` is published as two fields, a name and an address**, in the site file and in the catalog's `credit` (M11 (4)). They are **added beside** the existing Markdown line, which stays until the site has moved, so the change is additive (RD-P16-8).
- **RD-P16-4 — The *"Free 16K"* sentence:** the library's `description` of an HDRI drops the source's opening resolution claim. The source's own words stay verbatim in the record. *(All 59 open with a 16K, 20K or 24K claim, in 23 phrasings, measured; the library's file is 4096 × 2048, F-P16-6.)*
- **RD-P16-5 — What stays producer-side:** the recipes and the per-HDRI records. They are the source the files are written from, and they never ship (F-DS-11). *(Seed question 3.)*
- **RD-P16-6 — The contributor's form is a handle**, as RD-RO-2 says. It is one field on materials and HDRIs alike: *who brought this entry into the library*. An HDRI's source people sit in its `credit`, not in `contributor`. *(Seed question 4.)* Whose handle the library's own entries carry is Blocker 1.
- **RD-P16-7 — The byte change** *(seed question 2)* follows from Blocker 2. If the stamp is made in the served copy, the record's `sha256` still describes the file in the repo, and nothing changes. If the stamp is made in the repo, the HDRI evidence check (`validate_manifest.py`) compares the file **with the library's header lines removed** against the record's `sha256`. Under either answer, Phase14's *byte-identical default* becomes *pixel-identical*, and the M10 note says so.
- **RD-P16-8 — Only the dev catalog and the site file carry the new fields, and neither schema number moves** *(revised 2026-10-14 to match Phase15's RD-P15-5 to RD-P15-7)*. The release projector stays as it is, so the pilot's catalog re-projects unchanged. A frozen release gains the fields with the first release after this phase, as `master` did. With nothing projected into a release, `no_projection_guard` is not touched now; its blind spot (F-P16-3) is fixed when the projector gains the fields. Both changes are additive, and the website's mirror checks the version number, so neither `schema_version` nor the site file's schema is bumped. *(Was: both producers, the guard narrowed now, the schema steps claimed at execute.)*
- **RD-P16-9 — A10 (tagging) moves to Phase15**, whose HDRI taxonomy reads those tags. *(The seed's "it also answers A10", refined 2026-10-14. Phase15 accepted it the same evening: the whole `tagging` block on each dev-catalog HDRI entry, RD-P15-4.)*
- **RD-P16-10 — The 95 `.mtlx` files are stamped by inserting two inputs, not by re-assembling them.** Each diff must be exactly the two new lines; any other count aborts the run. The assembler writes both inputs for every article built from now on.
- **RD-P16-11 — The library's own entries carry the handle `MatterBot`** (the lead, 2026-10-14, on Blocker 1: *"MatterBot (I didn't make these, The system did)"*). That is all 154 today: 95 materials and 59 HDRIs. *The agent's reading:* it covers the pilot's 12 too, so CREDITS.md's *"the first 12 articles"* credit is corrected at the close. An HDRI's Poly Haven people stay in its `credit` (RD-P16-6).
- **RD-P16-8 and RD-P16-9 revised the same evening** to match Phase15's Brief (RD-P15-4 to RD-P15-7).

### Risk lane — `build`

The lane was checked against the controls themselves, read on 2026-10-14:
- **`no_projection_guard`** (`run_all.py`). Not touched now, because only the dev catalog gains fields (RD-P16-8).
- **The freeze** (`freeze_release.py`) hashes every referenced `.mtlx`, so stamping the pilot's 12 means a re-freeze in place. Approving it stays the maintainer's act (`LOCAL_DELTAS.md`, the publishing-producer row).
- **The `materials` lane** (`validate_material.py`) reads only `master_material` from the block, and has no list of allowed inputs (F-P16-8).
- **The HDRI evidence check** (`validate_manifest.py`) applies only to an HDRI listed in a lockfile, and none is listed yet.

**No master changes,** so no new Unreal runtime is owed. **Nothing touches** authorisation, secrets, a destructive migration or the public edge, beyond the push and the snapshot publish, which wait on the lead's word as always. **The test surface:** existing tests and units, plus one real-path smoke: click 1, in the installed library.

### Step list

| Step | Intent | First clickable result |
|---|---|---|
| **16.1** | **Every material says who gave it and its licence, and Blender shows it.** Recipe key, assembler, the 95 stamped (RD-P16-10), the asset-library generator reads the block, the library is regenerated and installed, the pilot is re-frozen. | Clicks 1 and 2 |
| **16.2** | **The engines' catalog says it, and so does every HDRI file.** The HDRI stamp (where: Blocker 2); `contributor`, `licence` and HDRI `credit` on every entry of the dev catalog; the stamp also writes Phase15's `group`, `when` and `sky` (RD-P15-4); the stamped default sky checked pixel for pixel in Storm and Blender; the Unreal check handed to the machine with Unreal. | Click 3's evidence |
| **16.3** | **The website's file says it.** In the site file: `contributor`, `edited_from` split into a name and an address, and the trimmed description. A dev snapshot is built, and published at the lead's word. | The snapshot's site file, fetched from its public address |

The steps run in order: 16.2's catalog fields read what 16.1 stamped. **16.1 alone is a whole demonstrable result**, and is the first thing to hand the lead.

### Compact build map

- **16.1:**
  - `tools/converters/recipe.schema.json`: add `contributor`.
  - `tools/converters/assemble_mtlx.py`: the metadata block, around `addNodeDef("ND_imrsv_metadata"…)`.
  - A one-time stamp script, kept with the step's evidence, not in `tools/`.
  - `tools/converters/working_tree.py`: a reader beside `master_of`.
  - `tools/generators/gen_asset_library.py`: the hard-coded `ad.author = "IMRSV"`, and `license`.
  - `blender/asset_library/`: regenerate, then install.
  - `tools/releases/freeze_release.py`: re-freeze the pilot.
- **16.2:**
  - `tools/releases/hdris.py`: the stamp, beside `thumbnail()`.
  - `tools/releases/serve_to_stage.py`: today it links `hdris/` into the checkout. Under Blocker 2's option A, it writes stamped copies, re-made only when stale, as the thumbnails are.
  - The dev catalog's entries, built in `serve_to_stage.py` on `derive_entry` / `derive_hdri_entry` (the projector's shared helpers; the release projection itself is unchanged).
  - `tools/validators/validate_manifest.py`'s evidence check, and `test_hdri.py`, under option B only.
- **16.3:** `tools/releases/build_snapshot.py` (`LICENCE`, the HDRI credit and description), and `test_build_snapshot.py`.
- **Gate:** `uv run tools/validators/run_all.py`, baselined before the first edit. It last read 15 PASS / 2 SKIP at Phase14 (dated: re-measure it). No file under `blender/addons/` or `tools/conformance/` changes, so `check_exporter.sh` is not owed.

### Shared with Phase15 — the collision surface

**Phase15 and this phase write the same places:**
- the `imrsv_metadata` block;
- the `.hdr` header;
- the dev catalog's entries, through `derive_entry`;
- the site file;
- `build_snapshot.py`.

**Execution follows RD-DS-5: Phase15 first.** This phase's first act at execute is to read Phase15's closed Brief and the code it landed. **Reuse its key spellings.** Phase15 builds no `.hdr` stamp and moves no schema number (its RD-P15-4, -5 and -7; agreed with Phase15's discovery session the same evening, `cc6905b`). **16.2's stamp is the only header write, and it carries Phase15's `group`, `when` and `sky` too**, so each file changes once. This phase owns `contributor`, `licence`, the HDRI `credit` and the stamp. The group and every taxonomy field are Phase15's.

### Blockers — the lead's calls

1. ~~**Whose handle do the library's own 154 entries carry?**~~ **Answered by the lead:** `MatterBot` (RD-P16-11).
2. **Where an HDRI is stamped:**
   - **(A) In the copy a consumer receives.** The repo keeps Poly Haven's bytes. The dev install writes stamped copies (about 1 GB on local disk, in place of links), and a release will do the same.
   - **(B) In the repo.** All 59 are re-written in place: about 1 GB more in the organisation's metered LFS (1,006 MB measured today), kept in history for good.

   **Recommended: (A).** Every file a consumer receives says what it is, which is what RD-DS-3 asks: consumers never read the checkout. LFS does not grow, and the import's check against Poly Haven's checksum stays true. A material is stamped in the repo either way, since the library writes the `.mtlx` itself. **One reader of the checkout exists:** USDLiveView's `IMRSV_MATTER_LIBRARY` mode searches a checkout whole (measured at its origin). Under (A) that mode would see unstamped HDRIs. Its default path, the active release in the install, would see stamped ones.

---

## Findings (discovery, 2026-10-14)

- **F-P16-1 — Storm reads a stamped `.hdr` pixel for pixel** (probe, 2026-10-14). `AristeaWreck_PureSky_v01.hdr` was given seven lines after `FORMAT=`, including UTF-8 text and a 400-character line. It was rendered as a visible dome with `usdrecord`, twice per file. All four PNGs are byte-identical (sha `671591c6…`), and they show a real sky (mean 209, standard deviation 53). The probe is under `/tmp/claude-p16/probe/` (stamp.py, two `.usda` files). Together with F-DS-10 (Blender 5.2.2), two of the three readers are proven. **Unreal's importer is not run** (the machine with Unreal). Storm's S2 lesson (a hand-written flat `.hdr` misread) does not apply: it was the pixel data, not the header.
- **F-P16-2 — Blender's asset metadata already has the fields.** `AssetMetaData` has `author`, `description`, `copyright`, `license` and `tags` (5.2.2, measured). `gen_asset_library.py` sets `author = "IMRSV"` for every article and leaves `license` empty.
- **F-P16-3 — The guard cannot see a `licence` field.** `run_no_projection_guard` refuses the **substring** `license` in the projected JSON. The site file's key is `licence`, which does not contain it, so a catalog `licence` field would pass the guard without the guard ever seeing it. When the release projector gains the fields (RD-P16-8), the guard must check keys, structurally (`.claude/CLAUDE.md` §Codebase search: a filter that must match nothing should be structural).
- **F-P16-4 — The HDRIs are 1,006 MB in LFS** (measured). The organisation's LFS is metered (Phase14 F-P14-13; the figures were given to the lead there, not here). Blocker 2.
- **F-P16-5 — Stamping changes 12 frozen pilot payloads.** The freeze hashes every referenced `.mtlx`. A re-freeze in place is settled practice.
- **F-P16-6 — All 59 HDRI descriptions open with a resolution claim**: 16K, 20K or 24K, in 23 phrasings (measured). One reads *"Free 16K, unclipped - bright morning/afternoon…"* without the word *HDRI*, so the trim is checked on all 59 by hand, not just by a pattern.
- **F-P16-7 — Phase15's discovery was running at the same time** (2026-10-14 evening; its doc was not yet changed at this commit). §Shared with Phase15 is the answer. Phase15's Brief landed as `cc6905b`, and the split is agreed.
- **F-P16-8 — The `materials` lane has no list of allowed metadata inputs**, so the two new inputs do not trip it (`validate_material.py` `_master_token` reads only `master_material`).
- **F-P16-9 — The website's mirror accepts exactly one site-file schema** (re-measured at its origin, 2026-10-14 evening, as in `261014_R_DownstreamPicture.md`). The site cannot show this phase's fields until it moves (P25, M11).

## Discovery Log

- **2026-10-14 — Pass 1** (`/discovery P16`). Read, top-down:
  - the specs: `_Architecture`, RuntimeCatalog, SiteFile, MaterialXTemplate, Identity §HDRI names;
  - the research: `261014_R_DownstreamPicture.md` in full, `261014_R_RoadmapOrder.md` (RD-RO-2), `261013_R_PlatformSkyAsks.md` (A9, A10), `261013_R_PlatformTrackedItemsAsks.md` (nothing for this phase), and `260923_R_StandaloneSetup.md` Q12 (*credits mechanics*: still open, and answered by this Brief);
  - the ledger: P19, P25, P26, M9 to M12;
  - Phase13's and Phase14's docs;
  - the code: the assembler, `working_tree`, the guard, the freeze, the HDRI check, the importer, the serve tool, the snapshot builder and the asset-library generator.

  The `.hdr` probe was extended to Storm (F-P16-1), and Blender's asset fields were measured. **Learnings:** Storm S2–S4 (read, and not a blocker, F-P16-1). No other domain applies: no master, colour or Unreal behaviour changes. **The tree was searched for this phase's name:** no code names it. The docs that do are the Roadmap, the research, Phase15's and Phase19's docs, and the ledger (P26, M11, M12). Hits on `P16` elsewhere are the ledger's row P16, which is a different id.
- **2026-10-14, the same pass:** RD-DS-7 landed mid-pass (`4b0b67b`): The Library Service and Thumbnails moved ahead of Character and Scale Grids. This phase keeps its number and its place after Phase15. The Brief cites the new order.
- **2026-10-14, the same evening:** the lead answered Blocker 1, *"MatterBot (I didn't make these, The system did)"* (RD-P16-11), and asked what *the consumer* means in Blocker 2. Phase15's Brief landed (`cc6905b`). Its session confirmed by message that Phase15 builds no `.hdr` stamp, moves no schema number and leaves the release projector alone. RD-P16-8 and RD-P16-9, the 16.2 stamp and §Shared with Phase15 were brought into line with it.
