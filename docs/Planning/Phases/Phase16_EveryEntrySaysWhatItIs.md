# Phase16 — Every Entry Says What It Is

**Status:** IN EXECUTION (2026-10-14, `/execute P16`; baseline `run_all.py` 15 PASS / 2 SKIP / 0 FAIL at `830538d`), lane **build**. Brief ready at Pass 2. Phase15 closed the same evening, so nothing now stands ahead of this phase. Pass 2 re-cut the Brief on what Phase15 actually landed. Opened by the lead's `/discovery P16`, then *"Things shifted a bit and P15 just finished... do another discovery pass"*. Numbered Phase16 on *"Lets make these the next phases (Before the scaled grid)"* (RD-DS-6). Seeded by `/research` on *"yes record it and seed all three"*. It follows *Matter, Character and HDRI* ([`Phase15_MatterCharacterHdri.md`](Complete/Phase15_MatterCharacterHdri.md)), whose structure it fills, and comes before The Library Service ([`PhaseTBD_LibraryService.md`](Future/PhaseTBD_LibraryService.md); RD-DS-7).

## Outcome

**Every material and HDRI says who contributed it, its licence, its name and its place in the taxonomy, from inside its own file. Studio, USDLiveView and the website read it from the library, and Forseti can tell who gave what and how each one is doing.**

**The library's half, which this phase delivers:** the facts are in every file, and every file the library serves or publishes (the dev install's catalog, the site file) carries them. **Reading them in Studio, USDLiveView and the website is each consumer's own work**, asked in the ledger (P25, P26, M11), and told to their live sessions as Phase15 15.3 did. Seeing *how each one is doing* happens where an entry is used, so it is also the consumer's (F-DS-12).

**Where it stands after Phase15** (F-P16-11):
- *Its name* and *its place in the taxonomy* are already in every `.mtlx`:
  - the material's name is its identity;
  - `domain` and `class` are in the metadata block;
  - a Character article also has `group`, `species` and `part`;
  - a missing `group` means Matter.
- An HDRI's `group`, `when` and `sky` reach the dev catalog from its record, but are not yet in the file.
- **This phase adds:** *who contributed it* and *its licence* everywhere, and every fact inside the `.hdr`.

## Why this is a phase of its own

The lead: *"I want Materials to work like Assets and Compositions.... same thing... people contribute they are tracked,, the is a license it is added,,, they can browse byt a taxolongy... Avoid sidecars, we can put things in MTLX, and in the case of HDRI... that is totally in our control. We are doing Materal tracking for FORSETI!"* (RD-DS-3). It changes what every file carries, and it reverses a standing rule: licence and provenance were kept out of the engines' catalog on purpose (`no_projection_guard`; RD-DS-2).

---

## The Brief

### First human test

**Where:** the lead's Blender on the library machine. It reads the Matter Asset-Browser library **from the repo, as Append**, as at Phase15's sitting (Phase15 15.1). Execute regenerates that library and reads the lead's preferences without saving them (Blender **B2**, **B12**).

1. **Asset Browser → Matter Library → Matter › Engineered › Metal → Copper verdigris.**
   - The asset sidebar shows **Author** `MatterBot` and **License** `CC0-1.0`. The catalog path is its place in the taxonomy, as Phase15 left it.
   - *Judge: the material says who gave it and under what licence.*
   - Today the sidebar reads `IMRSV` for every article, hard-coded, and has no licence (F-P16-2).
2. **The same for Character › Humanoid › Skin → a skin, and for the UV grid**, a material the library made from a script.
   - *Judge: it holds across the library: Matter and Character, the pilot's twelve and the rest.*
   - Execute reads the three from their files after 16.1, never by their names.
3. **HDRIs: no click.** This waiver stands unless you say otherwise. No surface the lead uses shows an HDRI's credit yet: USDLiveView and Studio read it in their own phases (P25, P26), and the website in its own. Instead, the agent's evidence goes into the 16.2 log:
   - the default sky's header, read back from the served copy;
   - its dev-catalog entry;
   - its pixels, identical to the repo's file, in Storm and in Blender.

**Reconciled click by click:**
- Clicks 1 and 2 need only 16.1.
- Click 3's evidence needs 16.2.
- The only tool any click uses is Blender, and it runs on the library machine.
- The doers are the agent (regenerating, serving, building the snapshot, `gh`; all done before, at Phase15) and the lead (looking).

### In now

| What | Step |
|---|---|
| **Every recipe gains `contributor: "MatterBot"`** (RD-P16-11). The recipe schema adds the key, and the recipe gate refuses a recipe without one. The licence is not a recipe field: it is `CC0-1.0` library-wide (RD-RO-2). | 16.1 |
| **The assembler writes `contributor` and `licence` into `imrsv_metadata`**, beside Phase15's `group`, `species` and `part`. **All 95 are re-assembled** from their recipes. Each diff must be exactly the two new lines; any other count stops the run (RD-P16-10). | 16.1 |
| **Blender's asset library reads both from the file** into Blender's own `author` and `license` fields, replacing the hard-coded `IMRSV`. The library is regenerated. | 16.1 |
| **The pilot `matterlib-0.1.0` is re-frozen in place**, since 12 of its `.mtlx` files change. The lead's promote command is handed over at the start of the close. | 16.1 |
| **One function builds each HDRI's facts from its record:** id, version, name, licence, contributor, the full credit, and Phase15's `group`, `when` and `sky`. **The stamp** writes them into the `.hdr` header, and the dev catalog's entry takes the same facts, so the two cannot disagree (RD-P16-2). | 16.2 |
| **The dev install serves stamped copies** of the 59 HDRIs in place of its link into the repo, re-made only when stale, as the thumbnails are. The repo keeps Poly Haven's bytes (RD-P16-12). | 16.2 |
| **The dev catalog carries `contributor` and `licence`** on every material and HDRI entry. Each HDRI also carries its **`credit`** (A9), in the site file's shape. A material's fields are read from its file (`working_tree.metadata_of`); an HDRI's come from the same facts the stamp writes (RD-DS-2, RD-P16-8). | 16.2 |
| **The site file:** `contributor` stops being *(planned)*. The credit gains `edited_from_name` and `edited_from_url` beside the Markdown `edited_from` (M11 (4)). Each HDRI's `description` drops the source's resolution claim (M11 (3)). The dev snapshot `0.2.0-dev.5` is built, and published at the lead's word. | 16.3 |
| **The consumers are told** what is new, as Phase15 15.3 did: ledger notes on P26, M10 and M11, and a message to each live session of the website and USDLiveView. | 16.3 |
| **The rest of the close:** the specs (MaterialXTemplate for the block, RuntimeCatalog for the fields, SiteFile, Identity §HDRI names for the header); CREDITS.md's *"per-material credit … is planned"* line and its *"the first 12 articles"* credit (RD-P16-11); `260923_R_StandaloneSetup.md` Q12, answered. | at the close |

### Not now

| Not now → where | What it will consume from this phase |
|---|---|
| **Reading and showing the facts** in Stage, Studio's picker, USDLiveView and the website → the consumers (P25, P26, M11) | the dev catalog's `contributor`, `licence` and `credit`; the `.mtlx` and `.hdr` fields |
| **The material package carries the handle** → *The Library Service* (TBD since RD-DS-8; its drafted step 17.2: *"the contributor's handle, when one is given"*) | the recipe's `contributor`, and the `.mtlx` field the package's complete-portable article already carries |
| **`/matter-generate` and `/matter-batch` write `contributor`** into the recipes they make → a quick fix when material-making resumes, held until Phase19 (RD-DS-7; Phase18 since RD-DS-8). The skills are being edited in another session today. | the recipe key. Until then the recipe gate refuses a recipe without one, so the gap cannot pass silently. |
| **The release projector, and narrowing `no_projection_guard`** → the first release after this phase (*Release Bundle*), as `master` was handled and as Phase15's group is (RD-P15-6, RD-P16-8) | the dev catalog's field names; F-P16-3 (the guard must check keys) |
| **Stamped HDRIs in a real release** → *Release Bundle and Consumer Contract* | the stamp, and the facts function |
| **Linking a handle to an account; counting use for Forseti** → the platform (Phase13's deferral; F-DS-12) | the `contributor` field |
| **HDRIs as Blender World assets** → *Blender from a Release* | the header's fields |
| **The exporter writing the facts onto an exported material prim** (`assetInfo`) → P26's consumer half, or the export phase the lead calls *"not implemented yet"* (RD-DS-3) | the `.mtlx` fields. A complete-portable export already carries them, because it copies the `.mtlx`. |
| **Unreal's HDR importer on a stamped file** → a check on the machine with Unreal, handed off at 16.2 | the stamped file |

### The reuse check

**What the stack already provides, reused unchanged** (most of it landed by Phase15, F-P16-11):
- **The metadata block, and its one writer and one reader.**
  - The assembler writes optional keys only when the recipe has them (Phase15's `group`, `species`, `part` loop). `contributor` and `licence` join it.
  - `working_tree.metadata_of` reads every input of the block, so no new reader is written.
  - The dev catalog already projects `master` and the group out of the file (F-DS-9).
- **Blender's own asset metadata:** `AssetMetaData` has `author`, `license`, `copyright` and `description` (Blender 5.2.2, measured). The generator only fills two of them; no add-on panel.
- **The Radiance header.** Readers skip header lines they do not know. Blender reads a stamped file pixel for pixel (F-DS-10), and so does Storm (F-P16-1).
- **The HDRI's facts, already gathered:**
  - each record (`library/provenance/sources/hdris/<id>.yaml`) holds the full credit;
  - `groups.hdri_taxonomy(record)` gives `when` and `sky`;
  - `serve_to_stage.working_tree_hdris` already builds each dev-catalog entry from them.

  The facts function wraps those, and the record stays the producer's source (RD-P16-5).
- **The site file's HDRI `credit` shape**, which the platform said *"would serve the consumer as it stands"* (A9). The catalog takes the same shape rather than a second one.
- **The serve tool's stale-or-make pattern**: `hdris.stale` and `make_thumbnails`, for the stamped copies.

**Each new layer, and the gap that justifies it:**

| New | Beside | The gap |
|---|---|---|
| **The facts function and the stamp** (in `tools/releases/hdris.py`) | `thumbnail()`, the importer | nothing writes into an `.hdr` today, and the facts are spread over the record and `groups.py` |
| **Stamped copies in the dev install** | the `link(dev / "hdris", …)` it replaces | a link serves the repo's unstamped bytes (RD-P16-12) |

### Decisions that bind

*Carried from research and earlier phases:*
- **RD-DS-2:** licence and name reach the engines as fields on each catalog entry, as the name and class already do. This overrides `no_projection_guard` for these fields.
- **RD-DS-3:** the facts come from the file itself (`.mtlx`, `.hdr`), and the catalog projects them. No sidecars.
- **RD-DS-5, refined by RD-DS-7:** Phase15, then this phase, then The Library Service (Phase17), Thumbnails (Phase18), Character Materials (Phase19) and Scale Grids (Phase20). *(Since RD-DS-8, the same evening: The Library Service is TBD, Thumbnails is Phase17, Character Materials Phase18 and Scale Grids Phase19.)* The lead: *"so we can get the entire chain establsihed recategorized, documented and working correctly before we add more materials"*. Material-making is held until Phase19.
- **RD-RO-2:** materials are `CC0-1.0`, and only CC0. A contributor's handle is carried as a courtesy and for Forseti tracking; it is never a licence condition.
- **RD-WS-1 / F-RO-26:** the library publishes no invented fact, and an absent field means *not known yet*.
- **Phase15's shapes, as landed:**
  - **RD-P15-3:** `group`, `species` and `part` in the block, and a missing `group` means Matter.
  - **RD-P15-4:** HDRI `group` `hdris`, `when`, `sky`, and the record's whole `tagging` (A10) on each dev-catalog entry; the header write is this phase's.
  - **RD-P15-5 and RD-P15-7:** neither schema number moves.
  - **RD-P15-6:** the release projector is unchanged.
- **Pre-release, no release ceremony** (`AI_WorkingAgreement.md` §Settled practices). Files are fixed forward in place, and the pilot is re-frozen in place.

*The lead's rulings in this discovery:*
- **RD-P16-11 — The library's own entries carry the handle `MatterBot`** (the lead, 2026-10-14: *"MatterBot (I didn't make these, The system did)"*). That is all 154: 95 materials and 59 HDRIs. *The agent's reading:* it covers the pilot's 12 too, so CREDITS.md's *"the first 12 articles"* credit is corrected at the close. An HDRI's Poly Haven people stay in its `credit` (RD-P16-6).
- **RD-P16-12 — HDRIs are stamped in the served copy, never in the repo** (the lead, 2026-10-14: *"A, stamp in the served copy"*).
  - The dev install holds stamped copies of the 59 (about 1 GB on local disk) in place of its link. A release will do the same.
  - The repo keeps Poly Haven's bytes, LFS does not grow, and the record's `sha256` and the HDRI evidence check stay true (RD-P16-7).
  - *The agent's reading:* USDLiveView's checkout mode (`IMRSV_MATTER_LIBRARY`) sees unstamped files, while its default, the installed release, sees stamped ones. That goes in the M10 note.

*The agent's calls* (each holds unless you say otherwise):
- **RD-P16-1 — The key is spelled `licence`**, as the site file publishes it. The provenance blocks' `license` is producer-side and stays as it is.
- **RD-P16-2 — What an HDRI's header carries.**
  - **Lines:** one line per fact. The key prefix is `MATTER_`, after the probe, with key names that mirror the catalog's fields. A fact with several values, such as authors or sponsors, repeats its key.
  - **The facts:** id, version, name, licence, contributor, and the full credit A9 lists:
    - the source and its address;
    - the HDRI's page there;
    - each author, with their role;
    - each sponsor, with their link;
    - the HDRI it was edited from, as a name and an address;
    - plus Phase15's `group`, `when` and `sky`.
  - **Left out:** the source's description and raw tags. The description stays in the record and the site file; the tags are on the dev-catalog entry (RD-P15-4).
  - The exact list goes into Identity §HDRI names at the close. The probe carried a 400-character line and UTF-8 text with no effect on the pixels (F-P16-1).
- **RD-P16-3 — `edited_from` is published as a name and an address**: `edited_from_name` and `edited_from_url`, beside the Markdown line, which stays until the site has moved. It goes in the site file and in the catalog's `credit` (M11 (4)), and is additive.
- **RD-P16-4 — The *"Free 16K"* sentence:** the library's `description` of an HDRI drops the source's opening resolution claim. The source's words stay verbatim in the record. All 59 open with one (F-P16-6).
- **RD-P16-5 — What stays producer-side:** the recipes and the per-HDRI records. They are the source the files are written from, and they never ship (F-DS-11).
- **RD-P16-6 — The contributor's form is a handle**, one field on materials and HDRIs alike: *who brought this entry into the library*. An HDRI's source people sit in its `credit`.
- **RD-P16-7 — The byte change.** Because the stamp is made in the served copy, the repo's files and their checksums are untouched. What changes is Phase14's claim about the default sky: the served file is now *pixel-identical*, not *byte-identical*, to the sky scenes used before. The M10 note says so.
- **RD-P16-8 — Only the dev catalog and the site file carry the new fields, and neither schema number moves.** This matches RD-P15-5 to RD-P15-7. The release projector stays as it is, so the pilot's catalog re-projects unchanged. A frozen release gains the fields with the first release after this phase.
- **RD-P16-10 — All 95 are re-assembled through the assembler, the one writer**, as Phase15 did for its 30. *(Revised at Pass 2. It was a one-time insert script, written for fear that re-assembly changed more. The probe shows all 95 re-assemble byte-identical to disk today, F-P16-10.)* Each diff must be exactly the two new lines; any other count stops the run.

### Risk lane — `build`

The lane was checked against the controls themselves (read at Pass 1, re-read at Pass 2):
- **`no_projection_guard`** (`run_all.py`): not touched, because only the dev catalog gains fields (RD-P16-8).
- **The freeze** (`freeze_release.py`) hashes every referenced `.mtlx`, so stamping the pilot's 12 means a re-freeze in place. Approving it stays the maintainer's act (`LOCAL_DELTAS.md`, the publishing-producer row).
- **The `catalog_freshness` lane:** the release projector is unchanged, so the pilot's catalog re-projects byte-identically.
- **The `materials` lane** (`validate_material.py`) has no list of allowed metadata inputs (F-P16-8).
- **The `recipe` lane** gains one required key. That is a rule inside an existing validator, as Phase15's folder check was. It is not a new lane.
- **The HDRI evidence check** (`validate_manifest.py`) is untouched (RD-P16-12).
- **`tools/conformance/`:** `verify_asset_library.py` checks catalog paths, not authors, and nothing under `tools/conformance/` or `blender/addons/` changes, so `check_exporter.sh` is not owed.

**No master changes,** so no new Unreal runtime is owed. **Nothing touches** authorisation, secrets, a destructive migration or the public edge, beyond the push and the publish of `dev.5`, which wait on the lead's word as always.

**The test surface:** the existing units are extended (`test_hdri.py`, `test_build_snapshot.py`) with:
- a stamped header read back;
- the facts function and the catalog entry agreeing;
- the trimmed descriptions.

One real-path smoke: click 1. **Baseline:** `run_all.py` gave 15 PASS / 2 SKIP / 0 FAIL at Phase15's close (2026-10-14). Re-measure it before the first edit.

### Step list

| Step | Intent | First clickable result |
|---|---|---|
| **16.1** | **Every material says who gave it and its licence, and Blender shows it.** The recipe key and gate, the assembler, the 95 re-assembled (RD-P16-10), the asset-library generator, the library regenerated, the pilot re-frozen. | Clicks 1 and 2 |
| **16.2** | **The engines' catalog says it, and so does every HDRI the install serves.** The facts function, the stamp, the stamped copies in the dev install, and `contributor`, `licence` and `credit` on the dev catalog. The default sky is checked pixel for pixel in Storm and Blender. The Unreal check is handed to the machine with Unreal. | Click 3's evidence |
| **16.3** | **The website's file says it, and the consumers are told.** The site file's `contributor`, `edited_from` name and address, and the trimmed descriptions. `dev.5` is built, and published at the lead's word. The ledger notes are written and the live sessions messaged. | `dev.5`'s site file, fetched from its public address |

The steps run in order, because 16.2's material fields read what 16.1 wrote. **16.1 alone is a whole demonstrable result**, and it is the first thing to hand the lead.

### Compact build map

- **16.1:**
  - `tools/converters/recipe.schema.json`: add `contributor`.
  - `tools/validators/validate_recipe.py`: require it.
  - The 95 recipes: one key each, by an anchored script that stops on any other count.
  - `tools/converters/assemble_mtlx.py`: the optional-key loop beside `group` / `species` / `part`. `licence` is a constant there, so it is never a recipe field.
  - Re-assemble all 95, the same way the probe did (F-P16-10).
  - `tools/converters/working_tree.py` `articles()`: carry `contributor` and `licence` from `metadata_of`.
  - `tools/generators/gen_asset_library.py`: `ad.author` and `ad.license` from the row, in place of `"IMRSV"`.
  - `blender/asset_library/`: regenerate.
  - `tools/releases/freeze_release.py`: re-freeze the pilot.
- **16.2:**
  - `tools/releases/hdris.py`: the facts function and the stamp, beside `stale()` and `thumbnail()`.
  - `tools/releases/serve_to_stage.py`: replace `link(dev / "hdris", H.HDRIS)` with stamped copies. `working_tree_hdris` takes the facts function's output, and `working_tree_catalog` adds the two material fields.
- **16.3:**
  - `tools/releases/build_snapshot.py`: around `credit["edited_from"] = c["info"]`, and the description.
  - `test_build_snapshot.py`.
- **Learnings in play:** Blender **B2** and **B12** (the library), GitHub **G1** (an interrupted `gh release create`), and Storm **S2** to **S4** (read; F-P16-1).

### Blockers

None. Both of the lead's calls are answered: RD-P16-11 and RD-P16-12.

---

## Execution ledger

| Step | Landed | Result | Next |
|---|---|---|---|
| **16.1** | `7db3005` | ✅ **Clicks 1 and 2 passed** — the lead, 2026-10-14, on Copper verdigris, a skin and the UV grid showing Author `MatterBot` and License `CC0-1.0`: *"yep!"*. All 95 recipes say `contributor: "MatterBot"`; all 95 re-assembled, each diff exactly the two lines (`contributor`, `licence`). Library regenerated (94 assets); read back from the saved `.blend`, all 94 `author`/`license` equal their own file's, one value pair (`MatterBot`, `CC0-1.0`). `verify_asset_library`: CONFORMS. Pilot re-frozen (12 `.mtlx` hashes). The recipe lane's RED fixtures were keyed (a false red, recorded on the gate) and `missing_contributor.json` added. `run_all.py`: 14 PASS / 2 SKIP / 1 FAIL — `approval_binds_freeze`, red until the maintainer's promote, as at Phase12 | 16.2 |
| **16.2** | the 16.2 commit | ✅ (click 3 waived; the agent's evidence). `hdris.py`: `facts()`, `credit()`, `stamp()`, `read_stamp()`, `stamp_stale()` and `hdris.py stamp <id> <out>`. The dev install serves 59 stamped copies (1006 MB) in place of the link; a second serve restamps 0. The dev catalog: 95 of 95 materials carry `contributor` + `licence` from their file, 59 of 59 HDRIs carry `contributor`, `licence` and `credit` (with `edited_from_name`/`_url`). **The default sky** (`IndustrialSunset02_PureSky`): the served header reads back as its facts, 16 `MATTER_` lines; its catalog entry carries the same; the repo's file still matches its record's `sha256`; the bytes after the header are the repo's. **Storm:** repo and served copy, visible dome, twice each, all four PNGs byte-identical (`c5111264…`), a real sky. *(The first try drew no dome — `--enableDomeLightVisibility` missing, Storm S4 — and four white frames agreed by construction; caught by looking.)* **Blender 5.2.2:** all 33,554,432 decoded values equal. `test_hdri.py`: 18 new units pass | 16.3 |

**Handed to the machine with Unreal (16.2), owed, not blocking:** after the close's push, on that machine run `uv run tools/releases/hdris.py stamp IndustrialSunset02_PureSky /tmp/IndustrialSunset02_PureSky_v01.hdr`, then import that file and `MatterLibrary/hdris/IndustrialSunset02_PureSky_v01.hdr` into the Unreal 5.8 editor (drag into the Content Browser; each becomes a TextureCube). Right is: both import with no warning about the header, at 4096 × 2048, and look the same on a Sky Light. Record the result here.

---

## Findings (discovery, 2026-10-14)

- **F-P16-1 — Storm reads a stamped `.hdr` pixel for pixel** (probe, Pass 1).
  - **The probe:** `AristeaWreck_PureSky_v01.hdr` was given seven lines after `FORMAT=`, including UTF-8 text and a 400-character line. It was rendered as a visible dome with `usdrecord`, twice per file.
  - **The result:** all four PNGs are byte-identical (sha `671591c6…`), and they show a real sky (mean 209, standard deviation 53).
  - With F-DS-10 (Blender 5.2.2), two of the three readers are proven. **Unreal's importer is not run** (the machine with Unreal).
  - Storm's S2 (a hand-written flat `.hdr` misread) was about pixel data, not the header.
- **F-P16-2 — Blender's asset metadata already has the fields.** `AssetMetaData` has `author`, `description`, `copyright`, `license` and `tags` (5.2.2, measured). `gen_asset_library.py` sets `author = "IMRSV"` for every article and leaves `license` empty (re-read at Pass 2, after Phase15's catalog-path change).
- **F-P16-3 — The guard cannot see a `licence` field.** `run_no_projection_guard` refuses the substring `license` in the projected JSON, and `licence` does not contain it. When the release projector gains the fields (RD-P16-8), the guard must check keys, structurally.
- **F-P16-4 — The HDRIs are 1,006 MB in LFS** (measured), and the organisation's LFS is metered (Phase14 F-P14-13). That is why RD-P16-12 was offered.
- **F-P16-5 — Re-assembly changes 12 frozen pilot payloads.** The freeze hashes every referenced `.mtlx`. Re-freezing in place is settled practice.
- **F-P16-6 — All 59 HDRI descriptions open with a resolution claim**: 16K, 20K or 24K, in 23 phrasings (measured). One reads *"Free 16K, unclipped - bright morning/afternoon…"* without the word *HDRI*, so the trim is checked on all 59 by hand, not only by a pattern.
- **F-P16-8 — The `materials` lane has no list of allowed metadata inputs** (`validate_material.py` reads only `master_material`).
- **F-P16-9 — The website's mirror accepted exactly one site-file schema** (measured at Pass 1). Phase15 15.3 has since asked it to accept schema 2. Either way, the site shows these fields only in its own phase (P25, M11).
- **F-P16-10 — All 95 recipes re-assemble byte-identical to the files on disk** (probe, Pass 2): `assemble_mtlx.py <recipe> -o /tmp/…` for each, compared with `MatterLibrary/materials/<path>`, gave 95 same, 0 different, 0 failed. So re-assembly is safe, and it is the one writer (RD-P16-10).
- **F-P16-11 — What Phase15 landed that this phase builds on** (read at `7744f0b` and in its closing doc):
  - **The files:** the 30 character articles are in `materials/character/humanoid/<part>/`, and their dev-catalog ids changed. Each declares `group`, `species` and `part`. The assembler writes them through an optional-key loop.
  - **The code:** `tools/converters/groups.py` holds the groups and `hdri_taxonomy(record)`. `working_tree.metadata_of` reads the whole block.
  - **The dev catalog** carries `group`, and `species` and `part` on the 30. On each HDRI it carries `group`, `when`, `sky` and `tagging`. It also has `groups[]`, and is still at schema 3.
  - **The site file** is `dev.4`, still at schema 2.
  - **Blender's library** files by group, and the lead's Blender reads it from the repo.
  - **Its 15.3 messages** already told the website that the *16K* sentence and `edited_from` are this phase's, and told USDLiveView that its ask *L3* is this phase's. *L3* is that viewer's own id and is not defined in this repo, so 16.3 asks the viewer's session what it covers before answering it.
- **F-P16-12 — The Library Service (then Phase17; TBD since RD-DS-8) consumes the handle** (its Brief, `7ab55ce`). Its material package carries *"the contributor's handle, when one is given"*, so this phase's recipe key and `.mtlx` field are what it packs.

## Discovery Log

- **2026-10-14 — Pass 1** (`/discovery P16`). Read, top-down:
  - the specs: `_Architecture`, RuntimeCatalog, SiteFile, MaterialXTemplate, Identity §HDRI names;
  - the research: `261014_R_DownstreamPicture.md` in full, `261014_R_RoadmapOrder.md` (RD-RO-2), `261013_R_PlatformSkyAsks.md` (A9, A10), and `260923_R_StandaloneSetup.md` Q12 (*credits mechanics*, which this phase answers);
  - the ledger: P19, P25, P26, M9 to M12;
  - Phase13's and Phase14's docs;
  - the code that reads or writes the block, the catalog, the HDRIs and the site file.

  The Storm probe (F-P16-1) and Blender's asset fields were measured. Learnings: Storm S2 to S4. The tree was searched for this phase's name: no code names it.
  - **The same evening:**
    - RD-DS-7 landed (`4b0b67b`).
    - Phase15's Brief landed (`cc6905b`), and its session agreed the split: the header write is this phase's, and A10 is Phase15's.
    - The lead answered both calls (RD-P16-11, RD-P16-12).
- **2026-10-14 — Pass 2** (the lead: *"Things shifted a bit and P15 just finished... do another discovery pass"*).
  - **Read:** what landed since `71c3b85` (Phase15 15.1 to 15.3 and its closing doc, Phase17's Brief, the research footer, the Roadmap), and Phase15's code (`groups.py`, `working_tree.py`, the assembler's metadata block, `serve_to_stage.py`, `build_snapshot.py`, `gen_asset_library.py`).
  - **Changed in the Brief:**
    - the status: Phase15 is closed, and next is `/execute`;
    - the Outcome's *where it stands* (F-P16-11);
    - click 1's surface (from the repo, as Append);
    - RD-P16-10, from a one-time insert to re-assembly (F-P16-10);
    - the build map, now on real names;
    - the consumers told at 16.3;
    - two Not-now rows (Phase17's package, F-P16-12; the two skills);
    - §Shared with Phase15 folded into the reuse check, now that Phase15 has landed.
  - **Phase15's close was still uncommitted in the working tree** during this pass (the move of its doc into `Complete/`, the Glossary, `_Architecture`). It was left alone.
