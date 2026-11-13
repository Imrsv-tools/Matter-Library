# Research — When an article is replaced: what IMRSV's asset tooling asks of the library

**Opened:** 2026-11-13 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `AR` (ids `AR-Qn`, `AR-Fn`). **Pass 1** is written from the asset tooling's side. The library's review is **Pass 2**, as in `261011_R_AssetToolingAsks.md`.
**Requested by:** IMRSV's work on the tools that make a model ready for Studio. The lead, 2026-11-13, verbatim: *"yes write both and file as issues"* — this doc and a sibling ask to the app, both after a published asset stopped opening.

**Question:** when the library replaces an article, how does an asset that already names the old one keep working, or learn what to name instead?

**Extends, does not replace:** `docs/specs/Ontology/Identity.md` §Two version axes · `docs/specs/Catalog/Catalog.md` · `261101_R_AssetToolingBrickAsks.md` (the same Set; its brick ask stands).

**Public-repo note.** The asset tooling is a sibling IMRSV project and is private for now. It is summarised here by what happened: no paths, code or ruling ids of its own.

**Measured at:** `c1d2a74` (batch 261101-1) and the tree of 2026-11-13.

## The short version

- **A Set that was correct when built stopped opening twelve days later.** Its bricks named `Terracotta_Unglazed_Clean_Base_s01_v01`. Batch 261101-1 built `Terracotta_Unglazed_Clean_Base_s1_v01` and removed the `_s01` file. A consumer that resolves the bare name now finds nothing, and the app refused the whole asset (AR-F1).
- **The asset tooling has rebuilt it; the copy already published still names the old article.** Every published asset that bound `_s01` is in the same place, and nothing tells its owner.
- **Asks:** keep a retired name resolvable for a while, or record what replaced it (A1); say so in the release notes or the catalog (A2). One question about which axis changed (AR-Q1).

## Pass 1 — From the asset tooling's side

- **AR-F1 — What the app did.** Adding the Set from the shelf, or from its build folder: *"it names a file that is not there: Terracotta_Unglazed_Clean_Base_s01_v01"*. The app's own copy of the library holds only `…_s1_v01`. The other ten articles the Set binds were all still there under their names.
- **AR-F2 — The replacement is a good one, and was drop-in in practice.** `…_s1_v01` carries colour, roughness and normal maps at 1 m, and its colour map averages (0.555, 0.212, 0.11) linear: the old article's constant. The Set's four tints held unchanged; only the bound name and the UV density (one unit a metre, read from `meters_per_tile`) changed. That is what makes a recorded successor (A1) cheap to act on.
- **AR-F3 — It has happened before.** `MildSteel_Raw_Clean_Base_s01_v01` → `…_s1_v01` (batch 261022-1), and the Blender asset file still names the old one (`261101_R_AssetToolingBrickAsks.md` A4). The asset tooling avoided mild steel for that reason.

### The asks

- **A1 — Keep a retired article resolvable, or name its successor.** Either keep the old `.mtlx` for a stated time (a stub that references the new one would do), or record in the catalog *"replaced by"* for each retired id, so a consumer or a builder can rebind automatically. The second is enough for the asset tooling.
- **A2 — Say when an article is retired or renamed**, in the release notes or the catalog, so a builder can find every asset it binds before a Creator meets the failure.
- **A3 — The Blender asset file follows the `.mtlx` names** (repeats `261101_R_AssetToolingBrickAsks.md` A4; still open).

### A question

- **AR-Q1 — Which axis was this?** `Identity.md` keeps two version axes. A change of scale tag (`s01` → `s1`) is a new name, not a `v02`. Is a scale change meant to retire the old name, or should both live until assets move?

## Pass 2 — The library's review

*(Not yet written.)*
