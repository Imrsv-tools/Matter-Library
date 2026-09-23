# Matter Taxonomy — 5 Domains / 19 Classes

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

The Matter Library organizes materials into a tight, deep taxonomy: **5 Domains**, each holding **Classes** (19 today; the taxonomy is designed to grow). **Domain and Class are expressed in the folder structure only** — never in the filename (see [Identity](Identity.md)) — so a material can be recategorized later without a rename.

## The 5 Domains and 19 Classes

| Domain | Classes | Count |
|--------|---------|-------|
| 🪨 **Natural** | stone · wood · soil · mineral | 4 |
| ⚙️ **Engineered** | metal · glass · cementitious · composite | 4 |
| 🧪 **Synthetic** | plastic · polymer · textile · coating | 4 |
| 🌫️ **Environmental** | sand · vegetation · liquid · ~~atmospheric~~ | 4 |
| 💡 **Utility** | emissive · virtual · energy | 3 |
| | **Total** | **19** |

### Coverage against the master set

The v1 [master set](MasterSet.md) covers **18 of 19 classes**. The one exception is **`atmospheric`** (volume materials — fog, mist, gas): it is **out of scope for prop-applied matter** and owned by a future Volumes/Effector domain *(planned)*, not the Matter master set. Every other class maps to a master (coverage table in [MasterSet.md](MasterSet.md)).

## Folder structure (Domain/Class only)

```
materials/
├── natural/        {stone, wood, soil, mineral}
├── engineered/     {metal, glass, cementitious, composite}
├── synthetic/      {plastic, polymer, textile, coating}
├── environmental/  {sand, vegetation, liquid, atmospheric}
└── utility/        {emissive, virtual, energy}
```

Base textures mirror the same hierarchy under `textures/base/`; cross-domain overlay and mask textures live in shared folders (`textures/shared/{overlays,masks}/`). Full tree: [Catalog](../Catalog/Catalog.md).

*(Updated 2026-09-23, measured: in this repo the tree is rooted at `MatterLibrary/` — `MatterLibrary/materials/<domain>/<class>/`, `MatterLibrary/textures/base/<domain>/…` and `MatterLibrary/textures/shared/{overlays,masks}/` all exist.)* Folders are created as articles land: today 4 Domains and 9 Classes are populated (engineered/{cementitious, glass, metal} · natural/{mineral, stone} · synthetic/{plastic, textile} · utility/{emissive, virtual}); the environmental Domain has no article yet. The taxonomy above is the full intended set regardless.

## Growth model

- **Classes** can be added under an existing Domain as the library grows (additive — a library semver-**minor**).
- **A Realm above Domain** *(planned)* is an escape hatch: if the library ever spans beyond elemental matter (e.g. composite "non-matter" like *brick wall*, *tile roof*, *cobblestone street*), a **Realm** level sits above Domain — "Matter" is one Realm; "Buildings" would be another with its own taxonomy. Not built; recorded so the query-vector design (`Realm / Domain / Class / Material / Variant / Condition / Detail`) is anticipated, not retrofitted.
- **Never add a Class to serve one article.** The 19-class ontology is closed per release; when a single article needs a different master than its Class routes to, the sanctioned mechanism is a name exception in [MasterSet §Master resolution](MasterSet.md#master-resolution--class-routing-with-name-exceptions), not a new Class.

## Status

**Solid.** The 5-Domain / 19-Class structure has held since the library's original design. It is the target-state ontology; the source collection populates it incrementally.

*(Updated 2026-09-23, measured: `MatterLibrary/materials/` in this repo is already laid out in the Domain/Class tree, and the `matterlib-0.1.0` runtime catalog carries `domain` and `material_class` per article.)* How a consumer lays out an installed release is consumer-side.

*Consumer-side (IMRSV): catalog folder cutover and live keep-set layout — see [Consumers](../Consumers.md).*

## History

- The 5-Domain / 19-Class taxonomy was first written in the library's original README and carried unchanged into the platform specs.
- 2026-06 — `atmospheric` was named explicitly out of master-set scope (volume materials are not prop-applied matter); this was the one change to the original ontology.
