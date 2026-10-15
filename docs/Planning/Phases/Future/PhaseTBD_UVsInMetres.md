# PhaseTBD — UVs in Metres

**Status:** SEEDED (2026-10-15) — not numbered. A pointer-shell written by Phase19's execution on the lead's ruling RD-P19-4 (`../Phase19_ScaleGrids.md`, *Decisions that bind*), when he chose *"1 now, 4 as a next phase"*. `/discovery` fills it. **Starting discovery is a deliberate gate, the lead's call, never a slide.**

## Outcome

**A builder lays out a mesh's UVs in metres once, and any library material picked for it draws at its real size; a scale grid dropped on it shows true-size cells, or visibly does not.**

## Why this is a phase

Today a mesh's UV unit is **the tile of the one material meant for it** ([LCDSchema](../../../specs/Contract/LCDSchema.md), *"The mesh's UV unit must be the article's tile"*). So a mesh UV'd for a 10 cm material draws a 1 m material ten times too small, and changing a material's size means new UVs or a `uv_scale` fix. Phase19's click 1 showed it from the person's side. The lead dragged scale grids from the Asset Browser onto a 1 m box with 0–1 UVs: *"they work... they do not change scale tho.. they all add to the 1meter cube as if they were each 1m materials"*.

His wish, at the ruling: *"Blender knows the scale (we work in metric for the mesh) so the the builder needs to define the uvs to scale (something actaully new becuase people don't seem to do that) so that when you pick a material it will map to the right scale.. If you put a .1 material on a 1m object, it will be wrong (the wrong grid colors align)... I am not sure any tools actaully undersatnd material scale to uv scale to object scale today"*.

The change reaches the contract, every article, the kits, the masters in three tools and every consumer, which is why it is a phase of its own.

## Scope — as known at seeding (2026-10-15)

- **The rule:** one UV unit is one metre on every mesh, and each article divides by its own `meters_per_tile`. (`uv_scale` divides, so an article's effective scale becomes its `meters_per_tile`.) This replaces LCDSchema's UV-unit rule. Probably a library semver-major change ([Identity](../../../specs/Ontology/Identity.md); [_Architecture](../../../specs/_Architecture.md) §Versioning).
- **Where the division lives:** in the masters (from `meters_per_tile`), in each article's `place2d`, or in the binding. Each must hold in MaterialX, Blender's `ML_Place2D` and the Unreal masters alike.
- **What already works this way:** the parity rig's scenes are already in metres and divide by `meters_per_tile` (`tools/parity/job.py`). The scale view's swap rule (LCDSchema §Scale view) gets simpler.
- **What does not tile:** fitted `sUKN` articles and maps on a mesh's atlas (`cutout_map`, `base_color_map`) keep their atlas UVs.
- **The kits and the character's detail UV set** (PlatformDependencies P18), and how a builder makes metric UVs in Blender.
- **Consumers:** Studio, the Unreal runtime, USDLiveView and the Blender add-on (PlatformDependencies, new asks).

## Open questions (settle during this phase)

- How existing meshes and scenes migrate, and whether the two conventions coexist for a while.
- Whether Unreal's mesh UVs need full precision. Small metre values may make Phase19's half-float finding (F-P19-9) moot.
- What existing tools do about real-world material size (the lead's question). A `/research` before discovery may answer it.

## Discovery Log

*(empty — `/discovery` fills it)*
