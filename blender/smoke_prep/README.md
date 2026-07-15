# Phase 60 Lane-3 — 60.4 smoke-input prep (headless de-risk)

Reproducible headless dry-run that builds the **2-datablock same-identity Copper**
scene the `⚠human` 60.4 acceptance smoke depends on, and asserts the export-side
plumbing green — so the live Studio sitting is **purely eyes-on** (retarget +
render + tint-visibility + UV nudge/reopen), not gated on discovering a plumbing
bug at the rig.

Two-process split (Fedora's Blender has no `pxr`):

```
# 1. build + export the scene (Blender 5.1.1)
blender --background ../MatterMaterials.blend \
        --python build_two_object_copper.py -- /tmp/p60_copper_two_object.usda

# 2. assert the export with pxr (usd-toolchain / usdtools env)
<usdtools-python> assert_two_object_copper.py /tmp/p60_copper_two_object.usda
```

**What it proves (the 8-step 60.4 acceptance, export-side legs 1–4/6/7):**
- distinct per-object Blender UV fitting travels as **distinct `primvars:st`** (UV
  correctness — Discovery-14 PRIMARY);
- two Material prims of the same Copper identity, the duplicate carrying the Blender
  `..._v01_001` suffix that 60.3.1's Stage rewrite-on-import normalize strips;
- **sparse tint isolation** — the untouched instance emits 0 LCD overrides, the tinted
  one exactly `color3f inputs:base_color_tint`;
- **no heavy Matter-texture duplication** (`export_textures_mode='PRESERVE'`).

The Studio-side legs (identity retarget to canonical local Copper → two distinct
`/Composition/Materials/<id>_Instance_<N>`, render, save/reopen) are proven headless
by 60.3.1's committed Stage test and validated eyes-on at 60.4.

This export is also the **seed for the 60.7 multi-object round-trip regression test**
(`RoundTripGateTest` `MaterialRoundTripDriver`) — promoted there **after** the 60.4
smoke, per the phase's smoke-first discipline.
