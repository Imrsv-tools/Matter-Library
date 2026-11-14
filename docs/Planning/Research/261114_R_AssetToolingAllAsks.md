# Research — Everything the asset tooling has asked of the library, in one place

**Opened:** 2026-11-14 · **Mode:** research — an **audit**: what is asked, by whom, and where each ask stands today. It gathers and commits to nothing.
**Mnemonic:** `ATA` (ids `F-ATA-n`, `Q-ATA-n`, `RD-ATA-n`).
**Asked by:** the lead, 2026-11-14: *"We have some more requests from the asset workshop, can you look into these and lets gather them all so we can address the requests"*.
**Public-repo note:** the asset tooling is a sibling IMRSV project and is private. It is described here by what it asks, with no paths, code or ruling ids of its own.

**Sources, each read whole on 2026-11-14:**

| Doc | Opened | Its asks | Library review |
|---|---|---|---|
| [`261011_R_AssetToolingAsks.md`](261011_R_AssetToolingAsks.md) | 2026-10-11 | A1–A5, AT-Q1–Q6 | done (Pass 2–3); two items still owed (below) |
| [`261101_R_AssetToolingBrickAsks.md`](261101_R_AssetToolingBrickAsks.md) | 2026-11-01 | A1–A4, BK-Q1 | **not written** |
| [`261104_R_AssetToolingHouseAsks.md`](261104_R_AssetToolingHouseAsks.md) | 2026-11-04, added to 11-10 | A1–A6, RH-Q1–Q2 | **not written** |
| [`261113_R_AssetToolingArticleRetirementAsks.md`](261113_R_AssetToolingArticleRetirementAsks.md) (also GitHub Issue #7) | 2026-11-13 | A1–A3, AR-Q1 | **not written** |
| **Not in this repo yet:** the asset tooling's research on historical Sets, read in place in its own clone (2 commits ahead of its origin, 2026-11-14 12:39 and 12:53) | 2026-11-14 | the finishes in Pass 1 below | — |

The asks in the first four docs stay where they were written. Each doc's own Pass 2 is still owed. This doc gathers them so they can be addressed together.

## The short version

- **One rebuild answers four asks.** The library's Blender asset file was last generated **2026-10-15**. It still names two retired articles and lacks the replacements, it lacks three articles the house binds, and it points at two overlay pictures that are gone (F-ATA-1).
- **Most of the materials asked for are already planned.** Of 17 finishes asked across the docs, **8 already have a wish-list row** and one more rides on the brick row, all `queued` since 2026-09-25. **8 have none** (F-ATA-2).
- **Five questions need a ruling, not a build:**
  - an article's retirement (keep its old name, or record its successor);
  - variation across thousands of pieces;
  - whether a tiled wall is matter or an assembly;
  - checking port ranges at conformance;
  - the sheets on a one-sided master (asked 2026-10-11, never ruled).
- **Most-asked:** a **mortar** (three times: bricks, the house, a stone church) and the **Blender file** (four times).
- **The asset tooling's newest word** (the lead, 2026-11-14): *"yes we can (and should) make material requests"*, ahead of two builds: a Shaker room and an Ancient Egyptian place. Of everything new it names, **a lime plaster opens the most of history**.

## Pass 1 — The gather (2026-11-14)

**Examined:**
- the four docs above, whole;
- the asset tooling's own research on historical Sets and on an office Set (2026-11-12, 2026-11-14), read in its clone;
- `library/wishlist.yaml`; the `.mtlx` on disk;
- the Blender asset file, decompressed (it is zstd) and searched for article names;
- `gh issue list` on this repo.

### F-ATA-1 — The Blender asset file is 30 days stale, and four asks are this one fact

`blender/asset_library/MatterLibrary.blend` was last committed 2026-10-15 (`037265c`). In its decompressed bytes on 2026-11-14:

| Name | In the file | On disk as `.mtlx` |
|---|---|---|
| `MildSteel_Raw_Clean_Base_s01_v01` | yes (3) | no: retired, now `…_s1_v01` |
| `MildSteel_Raw_Clean_Base_s1_v01` | **no** | yes |
| `Terracotta_Unglazed_Clean_Base_s01_v01` | yes (3) | no: retired in batch 261101-1 |
| `Terracotta_Unglazed_Clean_Base_s1_v01` | **no** | yes |
| `Granite_Weathered_…_s1`, `Sandstone_Weathered_…_s1`, `Brass_Polished_…_s01` | **no** | yes |
| `HairlineScratches01_overlay_s001`, `Scratches01_overlay_s001` | yes (1, 2) | no picture by that name |

These answer:
- the October doc's owed item 2 (*"regenerate `MatterLibrary.blend`"*);
- the bricks' A4 (the mild-steel name, the missing pictures);
- the house's A1 (three articles);
- the retirement doc's A3 (*"the Blender asset file follows the `.mtlx` names"*).

**It is one run of `tools/generators/gen_asset_library.py`** in `$MATTER_BLENDER`.
- **Its readers:** `tools/conformance/verify_asset_library.py`, `check_asset_library.sh` and `export_library_slice.py`, `tools/parity/scale_test_scene.py`, and the add-on's scale view. Each reads the file; none writes it.
- **What could stop it:** a reader that expects an article by its old name. Unchecked; the run itself shows it.

### F-ATA-2 — The finishes asked for, against the wish list

*"Row" = a line in `library/wishlist.yaml`. Every row found is `state: queued`, added by the coverage research of 2026-09-25. None is built.*

| Finish | Asked by (date) | Row | Note |
|---|---|---|---|
| **Brick clay**, with colour, roughness and normal maps, light enough to tint down | bricks A1 (11-01); historical Sets: an engine house (11-14) | `BrickClay_Natural_Clean_Base_s01_v01` | the row's *also wanted* is the efflorescence colour the bricks' A2 asks for |
| **Brick conditions:** soot and grime, efflorescence, a spalled face | bricks A2 (11-01) | (part of the brick row) | possibly overlay colours on one article, as the ask itself suggests |
| **Mortar** (cement or lime: sandy, gritty, no dust layer, `s01`) | bricks A3 (11-01); house A2 (11-04); historical Sets: an abbey (11-14) | **none** | asked three times. A dusty concrete stands in, and its dust lightens a joint that should sit in shadow |
| **Lime plaster or render** | historical Sets (11-14): *"the single ask that opens the most of history"* | `Plaster_Smooth_Clean_Base_s1_v01` | whether a smooth plaster is the lime plaster asked for is a question for the batch |
| **Earth plaster** | historical Sets: a Japanese room (11-14) | none | |
| **Plastic laminate**, a solid colour taken by tint, satin to gloss | house A3 (11-04); historical Sets: mid-century rooms | `Laminate_Matte_Clean_Base_s01_v01` | the row is **matte**; the ask runs satin to gloss |
| **Silvered mirror** (glass over silver, near-zero roughness) | house A4 (11-04) | `Chrome_Mirror_Clean_Base_s01_v01` | a chrome mirror is metal; whether it serves a bathroom mirror is a question for the batch |
| **A bright white**, about 0.9 linear, for vitreous china and white paint | house A6 (11-10) | none | today `Porcelain_Glazed` sits at 0.745 and the paints are cream, so a white needs a tint above 1, which Studio refuses |
| **Buff or grey-brown fieldstone** | house RH-Q2 (11-04) | `Quartzite_Natural_Clean_Base_s1_v01` | a weathered limestone would also serve |
| **Black marble** | an office Set (11-12); historical Sets: Art Deco (11-14) | none | a dark tint on `Marble_Veined_Polished` stands in |
| **Aged bronze** | an office Set (11-12); historical Sets: the Pantheon, Art Deco (11-14) | `Bronze_Aged_Clean_Base_s01_v01` | a dark tint on `Brass_Polished` stands in |
| **Porphyry** | historical Sets: the Pantheon (11-14) | none | |
| **Giallo antico** (a yellow marble) | historical Sets: the Pantheon, *"if a tint will not do"* | none | |
| **Travertine** | historical Sets, in its *"not there"* list (11-14) | `Travertine_Honed_Clean_Base_s1_v01` | |
| **Woven tape or rush** (chair seats) | historical Sets: the Shaker room (11-14) | `Straw_Natural_Clean_Base_s01_v01` (closest) | |
| **Tatami** | historical Sets: a Japanese room (11-14) | none | |
| **Linoleum** | historical Sets: mid-century rooms (11-14) | none | |

*Named in the historical Sets' "not there" list but not asked: wrought iron (cast iron stands in), rope and fur.*

### F-ATA-3 — The questions that need a ruling, not a build

| # | The question | Asked | What it decides |
|---|---|---|---|
| 1 | **When an article is replaced**, does its old name stay resolvable for a while, or does the catalog record *"replaced by"*? Is a scale change (`s01` → `s1`) meant to retire a name at all? (retirement A1–A2, AR-Q1; Issue #7) | 2026-11-13 | whether a published asset breaks when the library re-scales an article. **It has happened twice:** mild steel (batch 261022-1) and terracotta (batch 261101-1). A Set published against the old terracotta stopped opening |
| 2 | **Variation across thousands of pieces:** a per-piece random value the masters read, a variation mask, or a documented `uv_offset` practice? (BK-Q1) | 2026-11-01 | whether a brick wall is four material instances or one |
| 3 | **A tiled wall: matter or assembly?** By `Taxonomy.md` it is an assembly (tiles over grout). Is a glazed tile, with its pillowing and pooled glaze, an article of its own? (RH-Q1) | 2026-11-04 | whether the asset tooling keeps modelling tiles one by one |
| 4 | **Check every authored port against its range at conformance** (house A5). Tints above 1 passed every check and Studio refused them | 2026-11-10 | the asset tooling has since built this check on its own side (2026-11-10). The ask is that the library's own profile check does too |
| 5 | **Sheets on a one-sided master** (AT-Q4: twelve articles) | 2026-10-11 | never ruled. The October doc says *"whenever a sheet first looks wrong"* |

### F-ATA-4 — Related, not the library's

- On 2026-11-13 the asset tooling also asked the platform's app to open an asset that names a missing article, with that material marked unmapped instead of refusing the whole asset. That ask is the platform's.
- The library's half is F-ATA-3 row 1.

## A proposed order to address them (not ruled)

*Each is named by the verb that would land it. The lead cuts the order.*

1. **Rebuild the Blender asset file** (F-ATA-1): a `/quick-fix`, one sitting on either machine, one headless Blender run, then the asset-library conformance check. It answers four asks.
2. **Put the asked finishes at the top of the wish list, and add rows for the ones with none:** mortar, black marble, a bright white, porphyry, giallo antico if a tint will not do, earth plaster, linoleum, tatami, and a glossy laminate if the matte row will not stretch. Then `/matter-batch` works them.
   - **Lead order, by how many asks each answers:** mortar · brick clay (with its conditions) · lime plaster · aged bronze · black marble · laminate · a bright white · the mirror · the rest.
   - Adding the rows is a `/quick-fix` with `tools/converters/wishlist.py`.
3. **Rule the five questions** (F-ATA-3). Rows 1, 2 and 3 are contract questions:
   - row 1 is the biggest, since it decides what a release promises about names;
   - rows 4 and 5 are each a small change once ruled.
4. **Write the library's Pass 2 into each of the three unreviewed docs** at the end, pointing here, so each ask's own thread closes.
5. **A ledger row** in `PlatformDependencies.md` for the asset tooling's open asks, as M8 was for its first ones: **M16**, the next free id (M1–M15 listed 2026-11-14).

## Resolved

- **RD-ATA-1 — The order** (the lead, 2026-11-14: *"go"*, to the order put to them): the Blender file first, then the materials most asked: mortar → brick clay → lime plaster → aged bronze → black marble, then the rest. Answers Q-ATA-1.
- **RD-ATA-2 — A replaced article: the catalog records its successor** (the lead, 2026-11-14: *"take (a) for retirement"*). The old name is not kept as a stand-in file. The catalog says which article replaced a retired one, so a builder can rebind. Answers Q-ATA-2, and the retirement doc's A1 in its second form. *Reading, mine:* it also answers that doc's A2 (*"say when an article is retired"*), since a catalog entry is where a builder looks. AR-Q1 (is a scale change meant to retire a name?) is answered by practice: it does, and now it leaves a successor behind.

## Open questions

| # | Question | For |
|---|---|---|
| Q-ATA-1 | the order above | **ruled, RD-ATA-1** |
| Q-ATA-2 | F-ATA-3 row 1: keep an old name working, or record its successor? | **ruled, RD-ATA-2:** record the successor |
| Q-ATA-3 | F-ATA-3 rows 2, 3 and 5 | the lead, or a phase's discovery |

## Status

**Passes captured:** Pass 1, the gather (2026-11-14).

**Current direction:**
- one rebuild for the Blender file;
- the wish list for the materials: 8 rows exist (plus the brick conditions on the brick row), 8 finishes have none;
- five rulings;
- each source doc's Pass 2 at the end.

**Unverified:**
- whether any reader of the Blender file expects an old name (the rebuild will show it);
- whether `Plaster_Smooth`, `Chrome_Mirror` and `Laminate_Matte` as planned meet the asks (each batch's own judging);
- the historical-Sets asks are read from the asset tooling's unpushed commits and may still change there.

**Ruled (2026-11-14):** RD-ATA-1 (the order), RD-ATA-2 (a successor recorded in the catalog).

**Landed (2026-11-14):**
- `322685c` (`/quick-fix`): the Blender asset file rebuilt. 146 articles conform; current names; granite, sandstone, brass and copper in; no missing overlay pictures. It answers four asks (F-ATA-1).
- the next commit (`/quick-fix`): `library/wishlist.yaml`. The asked rows move to the top in RD-ATA-1's order (`wishlist.py next`: the two standing redo rows, then mortar → brick clay → plaster → aged bronze → black marble → laminate…). **Nine new rows:** `Mortar_Cement`, `Marble_Black`, `Laminate_Gloss`, `VitreousChina_White`, `Porphyry_Red`, `Marble_GialloAntico`, `EarthPlaster_Natural`, `Tatami_Natural`, `Linoleum_Plain`. Each asked row's note names who asked and what for.

**Not yet done:**
- **the materials themselves:** `/matter-batch` from the top of the list;
- **RD-ATA-2's build** (a retired article's successor in the catalog). It changes the catalog's contract, and `LOCAL_DELTAS.md` reserves a `schema_version` change to a contract phase, so it is a phase to seed;
- F-ATA-3 rows 2–5;
- each source doc's Pass 2;
- ledger row M16.

**▶ Next:** `/matter-batch` on the top rows (a fresh session), and the lead's word to seed the retirement phase.
