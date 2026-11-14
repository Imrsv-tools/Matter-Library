# PhaseTBD — Renamed Articles Name Their Successor

**Status:** SEEDED (2026-11-14, by `/research` on the lead's *"seed"*, after ruling *"take (a) for retirement"*, RD-ATA-2 in [`../../Research/261114_R_AssetToolingAllAsks.md`](../../Research/261114_R_AssetToolingAllAsks.md)). Unnumbered: the lead numbers it. **Discovery is a deliberate gate the lead opens.** This doc is a pointer-shell; discovery fills it.

## Outcome

**An asset built against an article the library later renames or re-scales still finds its material: the catalog names the article that replaced it, so a builder or an app can rebind instead of refusing the whole asset.**

*Why:*
- Twice a re-scaled article left published assets naming a file that no longer exists: mild steel `_s01` → `_s1` (batch 261022-1) and terracotta `_s01` → `_s1` (batch 261101-1).
- A Set published against the old terracotta stopped opening in the platform's app.
- Source: [`../../Research/261113_R_AssetToolingArticleRetirementAsks.md`](../../Research/261113_R_AssetToolingArticleRetirementAsks.md) A1–A2 and AR-Q1; GitHub Issue #7.

## Scope (seed — discovery confirms or cuts)

- **The record:** for each retired article id, the id that replaced it, served with the catalog. This is the lead's choice (a): no stand-in `.mtlx` is kept under the old name.
- **The two known retirements recorded:** `MildSteel_Raw_Clean_Base_s01_v01` → `…_s1_v01` and `Terracotta_Unglazed_Clean_Base_s01_v01` → `…_s1_v01`.
- **Recorded where a retirement happens,** so the next one cannot be forgotten: the wish list's rename (`wishlist.py mark … --name`) and any rename by hand.
- **Said where a builder looks:** the dev catalog and a release's notes or catalog (the retirement doc's A2).
- **Written into the contract:** `docs/specs/Catalog/Catalog.md` and `docs/specs/Ontology/Identity.md` §Two version axes (a scale change is a new name and leaves a successor).

## In now / not now

- **In:** the record, the two retirements, the rename paths that write it, the spec text.
- **Not now:**
  - **the platform's side:** an app that rebinds by the record, or opens an asset with a missing article marked unmapped (the asset tooling asked the platform for that separately on 2026-11-13);
  - a stand-in file under the old name (ruled out, RD-ATA-2).

## Questions for discovery (seed vs docs)

1. Where does the record live: a field on the successor's catalog entry, an entry for the retired id, or a file of its own beside the catalog? Each consumer reads one of these (the dev catalog, the site file, a release).
2. Does it change the catalog's `schema_version`? `LOCAL_DELTAS.md` reserves that bump for a contract phase, which this is.
3. A chain (A → B → C): record each hop, or always the newest?
4. What a gate checks: every retired id named by a record resolves to an article on disk.
5. Does the wish list's rename already know the old name at the moment it renames (`--name`), or is the rename recorded somewhere else?
