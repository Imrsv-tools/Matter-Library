# Matter Taxonomy — 6 Domains / 23 Classes

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

The Matter Library organizes materials into a tight, deep taxonomy: **6 Domains**, each holding **Classes** (23 today; the taxonomy is designed to grow). **Domain and Class are expressed in the folder structure only** — never in the filename (see [Identity](Identity.md)) — so a material can be recategorized later without a rename.

## The 6 Domains and 23 Classes

| Domain | Classes | Count |
|--------|---------|-------|
| 🪨 **Natural** | stone · wood · soil · mineral | 4 |
| ⚙️ **Engineered** | metal · glass · ceramic · cementitious · composite | 5 |
| 🧪 **Synthetic** | plastic · polymer · textile · coating | 4 |
| 🌫️ **Environmental** | sand · vegetation · liquid · ~~atmospheric~~ | 4 |
| 💡 **Utility** | emissive · virtual · energy | 3 |
| 🧬 **Biological** *(added 2026-09-27)* | tissue · keratin · bone | 3 |
| | **Total** | **23** |

**`biological`** *(added 2026-09-27, lead ruling CM1, Phase07)* is **the matter of living bodies**, people and creatures alike:
- **`tissue`**: skin, mucosa (lips, gums, tongue), sclera, iris, cornea.
- **`keratin`**: hair fibre, nail, horn, feather.
- **`bone`**: bone, tooth enamel, dentin (ivory later).

The boundaries:
- **Plant matter** stays in `natural/wood` and `environmental/vegetation`.
- **Leather** is processed hide, so it stays in `synthetic/textile`.
- **A body is not matter**, just as a wall is not (§Growth model). Only the *substance* lives here. Anything bound to one mesh, such as a region mask, a painted skin atlas or a hair card's cut-out, stays outside the taxonomy (research `260927_R_CharacterMaterials_MPFB2.md`, CM2).

**`ceramic`** *(added 2026-09-23, lead)* is **fired-clay matter**: brick clay, terracotta, earthenware, stoneware and porcelain, glazed or unglazed. The boundaries:
- **Unfired clay** stays in `natural/soil`.
- **Cement, concrete and plaster**, which set rather than fire, stay in `cementitious`.
- **A brick wall or a tiled floor is not matter** (see §Growth model). The ceramic *substance* they are made of is what lives here.
- Its typical master is Opaque. A glaze wants a clear-coat, which the assembler does not carry yet *(planned)*.

### Coverage against the master set

The v1 [master set](MasterSet.md) covers **22 of 23 classes** *(was 19 of 20; the three `biological` classes added 2026-09-27)*. The one exception is **`atmospheric`** (volume materials — fog, mist, gas): it is **out of scope for prop-applied matter** and owned by a future Volumes/Effector domain *(planned)*, not the Matter master set. Every other class maps to a master (coverage table in [MasterSet.md](MasterSet.md)).

## Folder structure (Domain/Class only)

```
materials/
├── natural/        {stone, wood, soil, mineral}
├── engineered/     {metal, glass, ceramic, cementitious, composite}
├── synthetic/      {plastic, polymer, textile, coating}
├── environmental/  {sand, vegetation, liquid, atmospheric}
├── utility/        {emissive, virtual, energy}
└── biological/     {tissue, keratin, bone}
```

Base textures mirror the same hierarchy under `textures/base/`; cross-domain overlay and mask textures live in shared folders (`textures/shared/{overlays,masks}/`). Full tree: [Catalog](../Catalog/Catalog.md).

*(Updated 2026-09-23, measured: in this repo the tree is rooted at `MatterLibrary/` — `MatterLibrary/materials/<domain>/<class>/`, `MatterLibrary/textures/base/<domain>/…` and `MatterLibrary/textures/shared/{overlays,masks}/` all exist.)* Folders are created as articles land: today 4 Domains and 9 Classes are populated (engineered/{cementitious, glass, metal} · natural/{mineral, stone} · synthetic/{plastic, textile} · utility/{emissive, virtual}); the environmental Domain has no article yet. The taxonomy above is the full intended set regardless.

## Growth model

- **Classes** can be added under an existing Domain as the library grows (additive — a library semver-**minor**).
- **A Domain** can be added too, by lead ruling, when a whole family of matter has no home *(added 2026-09-27: `biological`, CM1)*. It is additive in the same way.
- **A Realm above Domain** *(planned)* is an escape hatch: if the library ever spans beyond elemental matter (e.g. composite "non-matter" like *brick wall*, *tile roof*, *cobblestone street*), a **Realm** level sits above Domain — "Matter" is one Realm; "Buildings" would be another with its own taxonomy. Not built; recorded so the query-vector design (`Realm / Domain / Class / Material / Variant / Condition / Detail`) is anticipated, not retrofitted.
- **Add a Class whenever the matter needs one** (lead, 2026-09-23: "we can add classes if we need to — we have a universe to rebuild matter for"). The class set is fixed *within* a release; adding one is additive (semver-minor). A Class is never added to reach a master: every article declares its own master ([MasterSet §Master resolution](MasterSet.md#master-resolution--the-article-declares-its-master)).

  > **Superseded (2026-09-23), kept for history:** "**Never add a Class to serve one article.** The 19-class ontology is closed per release; when a single article needs a different master than its Class routes to, the sanctioned mechanism is a name exception in MasterSet §Master resolution, not a new Class."

## Status

**Solid.** The original 5 Domains held from the library's original design until `biological` became the sixth (2026-09-27). The original 19 Classes are now 23: `ceramic` was added 2026-09-23, and `biological`'s three on 2026-09-27. It is the target-state ontology; the source collection populates it incrementally.

*(Updated 2026-09-23, measured: `MatterLibrary/materials/` in this repo is already laid out in the Domain/Class tree, and the `matterlib-0.1.0` runtime catalog carries `domain` and `material_class` per article.)* How a consumer lays out an installed release is consumer-side.

*Consumer-side (IMRSV): catalog folder cutover and live keep-set layout — see [Consumers](../Consumers.md).*

## History

- The 5-Domain / 19-Class taxonomy was first written in the library's original README and carried unchanged into the platform specs.
- 2026-06 — `atmospheric` was named explicitly out of master-set scope (volume materials are not prop-applied matter); this was the one change to the original ontology.
- 2026-09-23 — the "closed ontology, never add a Class" rule was relaxed (lead): Classes are added when the matter needs them, and masters no longer route by Class.
- 2026-09-23 — `engineered/ceramic` added (lead) for fired-clay matter. It is the first Class added since the original design (19 → 20).
- 2026-09-27 — the **`biological` Domain** added (lead ruling CM1, research `260927_R_CharacterMaterials_MPFB2.md`; built in Phase07) with `tissue`, `keratin` and `bone` (20 → 23 classes). It is the first Domain added since the original five. The growth model covered new Classes only, so a new Domain was a lead call. Like a Class, it is additive (semver-minor).
