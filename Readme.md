# 🧱 Matter Library Project
### Unified Physically-Based Material Library and Toolset for Unreal Engine 5.7+ (Substrate) and Blender 4.x+ — others TBD

*Single-source MaterialX pipeline for consistent, real-world elemental / “Matter” materials across real-time and offline rendering.*

> **Status:** Research / aggregate / define phase. Much of what follows is **intended design**; sections are tagged **(exists)** or **(planned)** where the distinction matters. Nothing here is deleted just because it isn't built yet — see `.ai/conventions.md` §Don't Delete Spec Functionality.

---

## 🌍 Overview

The **Matter Library** is a shared, physically-accurate material ecosystem that behaves as closely as possible across Unreal Engine and Blender (others TBD with community support).
Materials are authored once in **MaterialX** — the single source of truth — and **transformed** into native Unreal (Substrate) and Blender (Principled BSDF) targets.

> **“Create a material once — render it anywhere — and it looks (close to) the same.”**

It is a component of the broader **IMRSV Platform** (see `IMRSV_Platform_Documentation/IMRSV_PlatformOverview.md`). The platform consumes a **stand-alone, “cooked”, versioned** material library so compositions stay lightweight (textures are huge; they ship once, pre-loaded, rather than per-composition).

---

## 🧭 Project Goals

- **MaterialX as the single source of truth** for all materials.
- **Physically correct scale** and tiling (meters-per-tile defined per material).
- **Visual parity across engines** — Unreal 5.7+ (Substrate + Lumen) and Blender 4.x (Principled BSDF). Others TBD.
- **Least Common Denominator (LCD)** parameter discipline — only expose what all targets can honor.
- **A volatile, community-friendly source collection** paired with a **controlled, curated, versioned library**.
- **Open and extensible** — a foundation others can build upon.
- **Flexible taxonomy** — tight structure (deep, not broad), with room for all matter and variations.
- **Filename clarity** — accounting for many variations and versions of a material.
- **Future-ready** — 8K physically-based textures, downsampled on export as needed.

---

## 🧩 Project components

- **MaterialX** — defines the canonical material structure and parameters.
- **Master Materials** — a versioned set of master materials for Unreal and Blender (others TBD).
- **Matter Library** — a taxonomy for organizing material and texture files.
- **Matter Filename** — a descriptive filename structure understandable outside the library.
- **Library Manifest / Releases** — curated lockfiles that pin which material/texture versions make up each released library version.
- **Blender Transformer** *(planned)* — converts `.mtlx` to Principled BSDF materials for Blender.
- **Unreal Transformer** *(planned)* — builds Substrate-friendly material instances.
- **UE Cook Project** *(planned)* — a standalone UE project (`bridges/unreal/`) that cooks Substrate materials for consumption by IMRSV Studio / Theater.
- **Matter Manager** *(planned)* — handles library file management, import, promotion, and subset creation / export.

---

## ⚙️ Master Materials *(planned)*

| Master Material | Description | Example Use |
|-----------------|--------------|--------------|
| `M_MasterMaterial_Opaque` | Standard PBR | Stone, metal, wood, fabric |
| `M_MasterMaterial_Masked` | Opaque + alpha cutout | Leaves, lace, perforated metal |
| `M_MasterMaterial_TranslucentThin` | Thin-surface transmission | Glass, resin, thin plastics |
| `M_MasterMaterial_TwoLayer` | Dual-blend opaque (mask-driven) | Paint-on-wood, rust-on-metal |
| `M_MasterMaterial_Emissive` | Unlit emissive | Plasma, atmospherics, UI/FX |

All share the same **Least Common Denominator (LCD)** parameter set — to be verified for parity across MaterialX, Blender, and Unreal. The master materials are also where we **bridge the gap** for the LCD approach (per-target tweaks that keep the visible result close).

---

## 🧱 Library Foundations

- Many **base materials** organized into **Classes**.
- Classes grouped into **5 Domains** (19 Classes defined today; the taxonomy is designed to grow):
  - 🪨 *Natural* — stone, wood, soil, mineral
  - ⚙️ *Engineered* — metal, glass, cementitious, composite
  - 🧪 *Synthetic* — plastic, polymer, textile, coating
  - 🌫️ *Environmental* — sand, vegetation, liquid, atmospheric
  - 💡 *Utility* — emissive, virtual, energy (placeholder / non-physical)

Top two levels are **Domain / Class** (folder structure only — see Filenaming).

If we ever connect this to an even larger library of “non-matter” compounds (brick wall, tile roof, cobblestone street, etc.), we can add a level **above** Domain — a **Realm** — where “Matter” is one Realm and e.g. “Buildings” is another with its own taxonomy. That gives lots of query vectors:

```
Realm  / Domain  / Class     / Material  / Variant / Condition  / Detail
Matter / Natural / Stone     / Limestone / Veined  / Distressed / Dusty
```

(More in Filenaming below.)

---

## 🧩 Overlays & MaskSets *(planned)*

| Type | Description | RGBA Layout |
|------|--------------|-------------|
| **Overlays** | Tiling surface effects (dust, scratches, fingerprints) | R/G = Normal XY, B = Roughness bias, A = Mask density |
| **MaskSets** | Multi-mask texture packs used for blending (paint, rust, dust, etc.) | R/G/B/A = 4 material masks |

Each material can reference one or more overlays and one MaskSet, enabling visual variety without redundant textures.

---

## ⚙️ Material composition

Each material specifies:
- Master Material
- The base texture set (normal, etc.) — where applicable
- Up to 1 mask layer (perforations, etc.)
- Up to 2 overlay layers (dust, etc.)
- The Lowest Common Denominator (LCD) parameter settings
- The non-LCD settings — where applicable

---

## 🗂️ Two-Tier Library Model: Source → Approved → Release

The library is deliberately split into a **volatile source collection** anyone can contribute to, and a **controlled versioned library** we curate. The connective tissue is a **manifest**, not file copies.

### Two version axes (don't conflate them)

| Axis | Versions what | Example | Driven by |
|---|---|---|---|
| **Material version** | one individual asset | `Limestone_Veined_Clean_Base_s01_`**`v02`** | contributor |
| **Library release version** | the curated *set* as a whole | **Matter Library 1.3** | maintainer |

### A library release is a manifest (lockfile), not a copy

A release pins the exact version of each included material and texture set:

```yaml
# library/releases/matterlib-1.3.lock.yaml
release: 1.3.0
materials:
  - id: engineered/glass/Glass_Clear_Clean_Base    version: v01  status: approved
  - id: natural/stone/Limestone_Veined_Clean_Base   version: v02  status: approved
  - id: natural/stone/Limestone_Veined_Clean_Base   version: v01  status: deprecated  # kept for back-compat
textures:
  - id: base/engineered/glass/CleanGlass01          version: v01
```

This gives us, for free:
- **Carry-forward** — release 1.4's manifest = 1.3's + new lines; unchanged materials keep their same `vNN` pin (no copying, no churn).
- **Back-compat** — list both an `approved` newer version and a `deprecated` older one; old release **tags** stay consumable forever.
- **Growth** — the manifest is append-mostly; we rarely remove, we mark `deprecated` / `retired`.

### Status lifecycle (per material/texture version)

```
draft        in source, not validated
  → candidate    passed CI (schema/naming/scale/parity checks)
  → approved     named in a release manifest
  → deprecated   superseded but kept for back-compat
  → retired      dropped from new manifests — never deleted from history
```

### Two rules that keep it safe

1. **Immutability after promotion** — once `material@vNN` ships in any released manifest, that file is frozen. A change is *always* a new `vNN+1`, never an in-place edit. This is what makes old releases reproducible.
2. **Library release semver** — **MAJOR**: breaking (LCD/master-material param change, scale-meaning change, a material retired). **MINOR**: additive (new materials/textures). **PATCH**: drop-in visual fix.

### Governance — volatile community, controlled library

- **Contribution is open but CI-gated.** Community PRs add materials to the source taxonomy; automated checks (MaterialX schema valid, naming/taxonomy valid, scale tag present, referenced textures exist, eventual automated parity render) move a material to `candidate`.
- **Promotion is controlled via CODEOWNERS.** Only maintainers can edit `library/releases/*.lock`. That single file set is the control point — anyone can flood the source; only maintainers define a release.
- Model stays in **one repo** today; the manifest approach upgrades cleanly to a separate library repo later (consuming source by pinned SHA) if access-control volume ever demands it — without re-architecting.

---

## 🧩 Library Folder Structure

Since many materials may share the same textures (e.g. Steel clean, Steel dusty, Steel brushed could all use base set “CleanSteel01”), textures are stored **separately** and referenced.

- Materials live in a **materials folder**, structured in the matter hierarchy.
- Base textures live in a **textures/base folder**, structured in the same hierarchy.
- Overlay and mask textures (used across materials in many domains) each have their own **shared** folders inside `textures/`.
- **Textures are tracked with Git LFS** (large, lower-churn than materials).

The Matter Manager will remap texture paths in materials on import / export. See `FolderStructure.txt` for the full tree with **(exists)** / **(planned)** markers.

---

### ⚖️ Texture Scale Reference

Every base texture uses a **real-world physical scale** — the number of **meters per UV tile**. This keeps detail consistent across Blender, Unreal, and future engines, and gives artists a sane starting point instead of guessing scale.

Each base texture set folder name includes a **scale tag** (`s###`); the material filename carries the scale tag it was authored against.

| **Scale Tag** | **Meters per Tile** | **Relative Detail** | **Typical Use Case** |
|:--------------:|:-------------------:|:--------------------|:----------------------|
| `s0001` | 0.001 m | Ultra-micro | Dust, pores, micro-scratches |
| `s001`  | 0.01 m  | Very fine | Fabric weave, paint texture, sand grains |
| `s01`   | 0.1 m   | Fine | Wood grain, brick clay, small tiles |
| `s1`    | 1 m     | Medium | Concrete, flooring, wall panels |
| `s10`   | 10 m    | Large | Terrain detail, large stone faces |
| `s100`  | 100 m   | Macro | Geological scale, landscapes, cliffs |
| `sUKN`  | Unknown | Unknown | Not defined, unknown, or not relevant |

---

## 🧮 Material Filenaming

Designed for both many **variations** of a material and many **versions** (updates) over time.

**Domain / Class** are defined **only in the folder structure** — so materials can be recategorized later without renaming files. The rest lives in the filename:

```
Material _ Variant _ Condition _ Detail _ Scale _ Version . mtlx
Limestone_Veined_Distressed_Dusty_s01_v01.mtlx
Glass_Clear_Clean_Base_s01_v01.mtlx
```

- **Condition** defaults to `Clean` and **Detail** defaults to `Base` when nothing special applies (see the seeded samples).
- Plenty of room for customization / variation while staying roughly readable:
  `Limestone26b_Veinish_VeryDistressed12_ScratchedButNotVeryDusty_s01_v32.mtlx`

---

## 🧰 Integration Considerations

### MaterialX (canonical)
- Metadata block for scale, domain/class, and master material (see seeded `.mtlx` samples — `imrsv_metadata` nodedef).
- Nodegraphs for base PBR + Overlays + MaskSets.
- Uses the open ASWF MaterialX 1.39+ standard.

### Blender Bridge *(planned)*
- MaterialX → Principled BSDF conversion.
- Node groups mirror Master Materials.
- Supports real-world scaling via `TextureScale_m`.

### Unreal Bridge *(planned)*
- MaterialX → Substrate material instance generator.
- Mirrors Blender masters for visual parity.
- Compatible with **Lumen** and **Nanite**.
- A standalone **UE cook project** (`bridges/unreal/`) cooks the materials so Studio / Theater can reference them.

---

## 🧪 Visual Parity Workflow *(planned)*

1. Author in **MaterialX Viewer**.
2. Validate in **Blender 4.x**.
3. Verify in **Unreal 5.7+ (Lumen)** — Linux dev currently pinned to UE 5.6.1 (see platform notes).
4. Compare output (target ΔE < 2) under standardized HDR lighting.

---

## 📘 References

- [MaterialX Documentation](https://materialx.org)
- [Unreal Engine Substrate Overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-substrate-materials-in-unreal-engine)
- [Blender Principled BSDF Manual](https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html)

---

## 🪪 Project

Part of the **IMRSV Platform** (`Imrsv-tools/Matter-Library`, submodule of `Imrsv-tools/IMRSV_Platform`).

Agent / contributor entry point: **`AGENTS.md`** → `.ai/context.md`.

**Contact:** *peter@imrsv.tools*

---

© 2025 The Matter Library
