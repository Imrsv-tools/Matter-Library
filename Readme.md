# 🧱 Matter Library Project
### Unified Physically-Based Material System for Blender 5.1+ and Unreal Engine (Substrate)

*Single-source MaterialX pipeline for consistent, real-world materials across real-time and offline rendering.*

---

## 🌍 Overview

The **Matter Library** is an open project to build a shared, physically-accurate material ecosystem that behaves identically across Blender and Unreal Engine (others TBD with communty support).  
It replaces traditional texture fakery with **true-scale, physically based materials**, authored once in **MaterialX**, and converted (?) to native Blender and Unreal formats.

> **“Write a material once — render it anywhere — and it looks the same.”**

---

## 🧭 Project Goals

- **MaterialX as the single source of truth** for all materials  
- **Physically correct scale** and tiling (meters-per-tile defined per material)  
- **Visual parity across engines** — Blender 5.1 (Principled BSDF) and Unreal 5.6+ (Substrate + Lumen)  - others TBD
- **Open-source and extensible** — a foundation others can build upon  
- **Future-ready** — 8K physically-based textures, downsampled dynamically (?) for performance

---

## 🧩 Architecture Overview

```
┌───────────────────────────────────────────────┐
│   Matter Library (.mtlx) — Canonical Source   │
│   • 145+ base materials (Matter types)        │
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
- **Blender Bridge** converts .mtlx to Principled BSDF materials.  
- **Unreal Bridge** builds Substrate Material Instances from the same source.  
- **Runtime editing** adjusts parameters like color, scale, and roughness — no recompilation required.

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

- **145 base materials** organized into **38 Families**  
- Families grouped by **MetaOrigin**:
  - 🪨 *Natural* — stone, wood, bark, sand  
  - ⚙️ *Engineered* — metal, glass, ceramics, composites  
  - 🧪 *Synthetic* — plastic, rubber, coatings, textiles  
  - 🌫️ *Environmental* — ice, water, atmosphere, powders  
  - 💡 *Utility* — virtual or placeholder materials  

Each material defines:
- `MetaOrigin`, `Family`, `Subtype`
- `MasterMaterial`
- `TextureScale_m` (meters per tile)
- Mask + Overlay slots for cross-family reuse

---

## 🧩 Overlays & MaskSets

| Type | Description | RGBA Layout |
|------|--------------|-------------|
| **Overlays** | Tiling surface effects (dust, scratches, fingerprints) | R/G = Normal XY, B = Roughness bias, A = Mask density |
| **MaskSets** | Multi-mask texture packs used for blending (paint, rust, dust, etc.) | R/G/B/A = 4 material masks |

Each material references one or more overlays and one MaskSet, enabling visual variety without redundant textures.

---

## 🧮 Naming Standard

**Format:**
```
<origin>_<family>_<subtype>-<finish>_<scale>_<resolution>_<version ###>
```

**Example:**
```
engineered_metal_steel-brushed_clean_01_8k_v001
natural_stone_granite-honed_clean_10_4k_v001
synthetic_plastic_abs-matte_clean_0001_8k_v001
```

This deterministic naming allows automatic lookup and runtime mapping across tools.

---

### ⚖️ Texture Scale Reference

Every base texture in the Matter Library uses a **real-world physical scale** — expressed as the number of **meters per UV tile**.  
This ensures that materials appear at consistent detail levels across Blender, Unreal, and any future engines, maintaining physical accuracy when scaled in scene units.

Each base texture set folder name includes a **scale tag** (`s###`) that defines its intended UV scale.  
Smaller values represent finer, more detailed surfaces; larger values represent broader, macro-scale textures.

| **Scale Tag** | **Meters per Tile** | **Relative Detail** | **Typical Use Case** |
|:--------------:|:-------------------:|:--------------------|:----------------------|
| `s0001` | 0.001 m | Ultra-micro | Dust, pores, micro-scratches |
| `s001`  | 0.01 m  | Very fine | Fabric weave, paint texture, sand grains |
| `s01`   | 0.1 m   | Fine | Wood grain, brick faces, small tiles |
| `s1`    | 1 m     | Medium | Concrete, flooring, wall panels |
| `s10`   | 10 m    | Large | Terrain detail, large stone faces |
| `s100`  | 100 m   | Macro | Geological scale, landscapes, cliffs |

**Example Folder Naming**




## 🧰 Integration Details

### **MaterialX (canonical)**
- Metadata block for origin, family, scale, and master material
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

## 📅 Project Roadmap

| Phase | Milestone | Status |
|-------|------------|--------|
| **1** | Taxonomy, naming, master materials | ✅ Done |
| **2** | MaterialX schema v2 (overlay + mask nodes) | 🧩 In progress |
| **3** | Engine master templates (Blender + UE) | ⚙️ In progress |
| **4** | Buildout of 145 base Matter materials (8K) | 🔜 Planned |
| **5** | Automated conversion pipelines | 🔜 Planned |
| **6** | Parity QA automation | 🔜 Planned |
| **7** | Open-source release (GitHub/ASWF) | 🌐 Planned |

---

## 🧭 Why It Matters

- Enables **consistent realism** across render engines  
- Creates a **shared visual language of materials**  
- Future-proofs physically-based rendering pipelines  
- Bridges **artists**, **developers**, and **technical directors** under one open framework  

---

## 💬 Get Involved

We welcome collaboration!

1. **Fork** this repository  
2. Explore the `/schemas` and `/materials` folders  
3. Check open tasks in `/docs/roadmap.md`  
4. Share feedback or issues via GitHub  

---

## 📘 References

- [MaterialX Documentation](https://materialx.org)  
- [Unreal Engine Substrate Overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-substrate-materials-in-unreal-engine)  
- [Blender Principled BSDF Manual](https://docs.blender.org/manual/en/latest/render/shader_nodes/shader/principled.html)

---

## 🪪 Credits

**Project Contributors:**  
GPT-5 (technical planning) obvy:) • Core Team (taxonomy & data) • Open Source Community  

**Contact:**  
For discussion, feedback, or collaboration proposals:  
📧 *peter@imrsv.tools*

---

© 2025 The Matter Library Project
