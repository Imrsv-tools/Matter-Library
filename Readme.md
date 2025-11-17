# 🧱 Matter Library Project
### Unified Physically-Based Material Library and Toolset for Blender 5.1+ and Unreal Engine 5.7+ (Substrate) - Others TBD

*Single-source MaterialX pipeline for consistent, real-world elemental / “Matter” materials across real-time and offline rendering.*

What 

the

fuck

---

## 🌍 Overview

The **Matter Library** is an open project to build a shared, physically-accurate material ecosystem that behaves identically across Blender and Unreal Engine (others TBD with community support).  
It is focused on **true-scale, physically based materials**, authored once in **MaterialX**, and converted (?) to native Blender and Unreal formats.

> **“Create a material once — render it anywhere — and it looks (close to) the same.”**

---

## 🧭 Project Goals

- **MaterialX as the single source of truth** for all materials  
- **Physically correct scale** and tiling (meters-per-tile defined per material)  
- **Visual parity across engines** — Blender 5.1 (Principled BSDF) and Unreal 5.7+ (Substrate + Lumen)  - others TBD
- **Open-source and extensible** — a foundation others can build upon
- **Flexible taxonomy** — tight structure (deep not broad), with room for all matter and variations
- **Filename clarity** — accounting for many variations and versions of a material  
- **Future-ready** — 8K physically-based textures, downsampled (on “export”) as needed.

---

## 🧩 Architecture Overview

```
┌───────────────────────────────────────────────┐
│   Matter Library (.mtlx) — Canonical Source   │
│   • Tons of unique base materials (Matter types)        │
│   • Hundreds of shared base texture sets         │
│   • Overlays / MaskSets as reusable nodegraphs│
└───────────────────────────────────────────────┘
               │
     ┌─────────┴──────────┐
     │                    │
┌───────────────┐    ┌───────────────┐
│  Blender 5.1  │    │ Unreal 5.6+   │
│ Principled BSDF│←→ │ Substrate Inst │
└───────────────┘    └───────────────┘
```

- **MaterialX** defines the canonical material structure and parameters.  
- **Blender Transformer** converts .mtlx to Principled BSDF materials.  
- **Unreal Transformer** builds Substrate friendly mtlx instances from the same source.  
- **Matter Manager** handles library file management and subset creation / export

---

## ⚙️ Master Materials

| Master Material | Description | Example Use |
|-----------------|--------------|--------------|
| `M_MasterMaterial_Opaque` | Standard PBR | Stone, metal, wood, fabric |
| `M_MasterMaterial_Masked` | Opaque + alpha cutout | Leaves, lace, perforated metal |
| `M_MasterMaterial_TranslucentThin` | Thin-surface transmission | Glass, resin, thin plastics |
| `M_MasterMaterial_TwoLayer` | Dual-blend opaque (mask-driven) | Paint-on-wood, rust-on-metal |
| `M_MasterMaterial_Emissive` | Unlit emissive | Plasma, atmospherics, UI/FX |

All share the same **Least Common Denominator (LCD)** parameter set — verified for parity across MaterialX, Blender, and Unreal.


---

## 🧱 Library Foundations

- Many **base materials** organized into **38 Classes**  
- Classes grouped by **5 Domains**:
  - 🪨 *Natural* — stone, wood, bark, sand  
  - ⚙️ *Engineered* — metal, glass, ceramics, composites  
  - 🧪 *Synthetic* — plastic, rubber, coatings, textiles  
  - 🌫️ *Environmental* — ice, water, atmosphere, powders  
  - 💡 *Utility* — virtual or placeholder materials  

These are the top level:
<Domain><Class>

If you want to connect the library to an even larger library of “Non-matter” (containing compound materials brick wall, tile roof, cobblestone street with gutters or whatever), we could add a level above (Group, Category, Sector, Realm or some such) where “Matter” could be one and another could be “Buildings” with its own taxonomy etc.

**Realm / Domain / Class /**

So a full categorization might be something like:
Realm_Domain_Class_Material_Variant_Condition_Detail 
Matter_Natural_Stone_Limestone_Veined_Distressed_Dusty

Gives room for lots of query vectors.
(More in filename below)

---

## 🧩 Overlays & MaskSets

| Type | Description | RGBA Layout |
|------|--------------|-------------|
| **Overlays** | Tiling surface effects (dust, scratches, fingerprints) | R/G = Normal XY, B = Roughness bias, A = Mask density |
| **MaskSets** | Multi-mask texture packs used for blending (paint, rust, dust, etc.) | R/G/B/A = 4 material masks |

Each material references one or more overlays and one MaskSet, enabling visual variety without redundant textures.

---

## ⚙️ Material composition
Pulling it together.
Each Material will use and specify:
- Master Material
- The base texture set (normal, …)  - where applicable
- Up to 1 mask layer (perforations, etc)
- Up to 2 overlay layers (dust, etc)
- The Lowest Common Denominator (LCD) parameter settings
- The non-LCD settings - where applicable

---

## 🧩 Library Folder Structure

Since many materials may share the same textures (e.g. Steel clean, Steel Dusty, Steel brushed, etc could all use the same base texture set “CleanSteel01”), these will be stored separately.

Materials will be in a **material folder** structured in matter hierarchy.
Base textures will be in a **textures folder** structured in the same matter hierarchy.
Overlay and mask textures (possibly used across materials in many domains) will each have their own folders **overlay folder** and **maskset folder** inside the textures.

The Material Manager will remap the texture paths in the materials when importing / exporting.

---

### ⚖️ Texture Scale Reference

Every base texture in the Matter Library uses a **real-world physical scale** — expressed as the number of **meters per UV tile**.  
This ensures that materials appear at consistent detail levels across Blender, Unreal, and any future engines, maintaining physical accuracy when scaled in scene units, and gives artists a starting point for material scale instead of just randomly sliding scale adjustments.

Each base texture set folder name includes a **scale tag** (`s###`) that defines its intended UV scale.  
Smaller values represent finer, more detailed surfaces; larger values represent broader, macro-scale textures.

| **Scale Tag** | **Meters per Tile** | **Relative Detail** | **Typical Use Case** |
|:--------------:|:-------------------:|:--------------------|:----------------------|
| `s0001` | 0.001 m | Ultra-micro | Dust, pores, micro-scratches |
| `s001`  | 0.01 m  | Very fine | Fabric weave, paint texture, sand grains |
| `s01`   | 0.1 m   | Fine | Wood grain, brick clay, small tiles |
| `s1`    | 1 m     | Medium | Concrete, flooring, wall panels |
| `s10`   | 10 m    | Large | Terrain detail, large stone faces |
| `s100`  | 100 m   | Macro | Geological scale, landscapes, cliffs |

---

## 🧮 Material Filenaming
Thinking of the future for both many variations of a material as well as versions of (updates to) the same material over time.
The **Domain / Class** are only defined in the folder structure (so the matter materials can be recategorized in the future if needed without file renaming).
The rest:
**Material / Variant / Condition / Detail / Scale / Version**
are in the filename:
Limestone_Veined_Distressed_Dusty_s01_v01.mtlx

This leaves plenty of room for customization / variation and mayhem, but keeps things roughly understandable.
Limestone26b_Veinish_VeryDistressed12_ScratchedButNotVeryDusty_s01_v32.mtlx


## 🧰 Integration Considerations

### **MaterialX (canonical)**
- Metadata block for scale, and master material
- Nodegraphs for base PBR + Overlays + MaskSets
- Uses open ASWF MaterialX 1.39+ standard

### **Blender Bridge**
- MaterialX → Principled BSDF conversion
- Node groups mirror Master Materials
- Supports real-world scaling via `TextureScale_m`

### **Unreal Bridge**
- MaterialX → Substrate Material Instance generator
- Mirrors Blender masters for visual parity
- Compatible with **Lumen** and **Nanite**

---

## 🧪 Visual Parity Workflow

1. Author in **MaterialX Viewer**  
2. Validate in **Blender 5.1**  
3. Verify in **Unreal 5.6 (Lumen)**  
4. Compare output (ΔE < 2) under standardized HDR lighting  

---

## 📘 References

- [MaterialX Documentation](https://materialx.org)  
- [Unreal Engine Substrate Overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-substrate-materials-in-unreal-engine)  
- [Blender Principled BSDF Manual](https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html)

---

## 🪪 Engaged

**Project Contributors:**  
GPT-5 (technical planning) obvy:) • Core Team (taxonomy & data) • Open Source Community  

**Contact:**  
For discussion, feedback, or collaboration proposals:  
📧 *peter@imrsv.tools*

---

© 2025 The Matter Library

