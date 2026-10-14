# Research — Comparison pictures in each tool: a scene a person can read

**Opened:** 2026-10-14 · **Mode:** research. It gathers and commits to nothing; the phase it seeds rules.
**Mnemonic:** `CP` (ids `F-CP-n`, `Q-CP-n`, `RD-CP-n`).
**Opened by:** the lead, during Phase17's execution, after seeing the thumbnails and the material pages on the website: *"lets either seed a phase to do this or setup a research"*. **Seeded only.** Pass 1 is owed: `/research 261014_R_ComparisonPictures.md`.

**Question:** what scene should the rig's per-tool pictures (Storm, Blender, Unreal) be rendered in, so that a person can compare one material across the tools? The answer must keep what the rig measures.

---

## The lead's words (2026-10-14)

> *"So.. the hero images are really good... almost TOO good. but that is fine for now... the compair images (on the material pages for the matter library) we show the storm / Blender / UE image tests/// we have to revamp this test. the checkerboard background is SO overwhelming and you can barily see any detail in the objects. Isn't there some sort of standard object shape that is used for material tests... somethinglike this https://github.com/usd-wg/assets/tree/main/full_assets/StandardShaderBall and perhaps putting in a space with domelight so a reflectie pattern can be seen and not so many colors lime green and hot pink checkerboard is NOT helful... mayb reserach approprate backgrounds for shader ball tests. we don't need to do that this phase (obviously) but lets either seed a phase to do this or setup a research"*

## The website's ask (2026-10-14, addressed to the library; summarised)

The website shows the rig's pictures on each material page. Since Phase17 it shows them lower down, as *"How it was tested"*, with the day they were measured. It asks for a **comparison set** per material, *"not just to make it look good but for it to be a real comparison"* (its lead). The ask has seven points:
1. One scene, defined once, used by every tool: the same subjects, camera, lights, exposure, view transform and size. A plain, neutral backdrop, **not the UV grid**. The grid stays where it earns its place, the rig's see-through check.
2. Each tool as its users would see it, with its normal renderer, named per picture. The material is never tuned per tool. Lights are converted only by the rig's measured mappings, and the conversion is stated.
3. Differences are kept, not hidden. Where a tool cannot do something (a shadow, refraction, a wear layer), the picture shows it and a line per tool says so.
4. Current or not shipped: dated, and a stale one refused, as the thumbnails are.
5. Baseline JPEG (RD-P17-7), one size for all tools; 1024 would match the thumbnails.
6. In the site file, in a shape the library owns: per picture its tool, renderer, view, date, file and sha256, under a role of its own beside `thumbnail` and `rig`. Whether the rig's pictures stay published is the library's call.
7. A subset is fine. Unreal waits on a showcase build of the runtime.

It asks two questions. **Which renderer counts as each tool's own** (Cycles or EEVEE, Lumen or path tracing)? **Can Storm be lit to match a scene with real shadows**, or is the honest answer a flatter picture that says so?

## What is true today (measured in this repo, 2026-10-14)

- **F-CP-1 — The rig's scene is built for parity, by construction.** `tools/parity/scene/build_scene.py`: a 0.18 m sphere, a 0.30 m rounded cube and a 2 cm slab. A **UV-grid wall** stands behind them so see-through materials show something, with a 10 cm ruler. A constant dome (sRGB 188) and one sun. In Blender every mesh is invisible to shadow, diffuse and glossy rays, and the view transform is `Standard` (`drivers/blender_render.py`), **because Storm can do none of shadows, bounce or reflections of other objects** (`JOB_FORMAT.md` §Matched lighting). Unreal is held to the same. The parity verdict (*"Moved"*: does each slider move every tool alike) is measured on this scene.
- **F-CP-2 — The wall's grid is load-bearing in one view.** The `side` view (2026-10-05) tells a thin wall from a solid by whether the wall's lines move through the cube. The colourful UV grid is the pattern it reads (`build_scene.py` §SIDE).
- **F-CP-3 — The rig's published pictures are old and small.** 512 px, measured 2026-09-27 to 2026-10-05: before the current masters (the website's own reading).
- **F-CP-4 — The thumbnails solved a neighbouring problem, not this one.** Phase17's showcase is Cycles only, with its own lighting (HDRI, key, rim, shadows, Khronos PBR Neutral). It answers *"what does it look like at its best"*, not *"does each tool draw it alike"*. Its scene (`tools/thumbnails/`) and its record and stale logic are reusable.
- **F-CP-5 — The rig's drivers already render one job in three tools**, from one USD scene (`tools/parity/job.py`, `JOB_FORMAT.md`). A second scene is a second job shape, not a new rig.

## Questions for Pass 1

- **Q-CP-1 — The subject.** Is the USD working group's *StandardShaderBall* (`usd-wg/assets`, `full_assets/StandardShaderBall`) the right one, and what else is used (Mitsuba's material-preview ball, the MaterialX shader ball, Substance's, Disney's or Autodesk's)? **Its licence:** the library ships CC0 content only (RD-RO-2). Can a test asset under another licence sit in the tools, or must the subject be CC0 or made here? Does it carry an `st` in metres, so an article shows at its real size (`meters_per_tile`)?
- **Q-CP-2 — The background and the dome.** What do shader-ball tests use behind the ball: a neutral grey, a two-tone floor and sky, a studio HDRI, a soft checker at low contrast? Which dome makes a reflection pattern readable without taking over? Can Storm draw a textured dome, and its reflections, as Blender and Unreal do?
- **Q-CP-3 — Parity or appearance, or both.** Does the comparison set replace the rig's scene, sit beside it (the rig keeps its matched lighting for the verdicts, and a second job renders the comparison), or change the rig itself? Each changes what *"Moved alike"* is measured on.
- **Q-CP-4 — Each tool's own renderer** (the website's two questions): Cycles or EEVEE; Lumen, path tracing or the rig's matched lighting in Unreal; Storm as it is. And how is a difference that belongs to the tool shown?
- **Q-CP-5 — The see-through check** (F-CP-2): does it keep the colourful grid in the rig's `side` view only, or move to a neutral pattern everywhere?
- **Q-CP-6 — The shape in the site file:** a new role (`comparison`) beside `thumbnail` and `rig`, and whether the rig's own pictures stay published.

## Pointers

- Phase17 — Thumbnails (`docs/Planning/Phases/Complete/Phase17_Thumbnails.md`): F-P17-9, RD-P17-7, the record and stale logic.
- `tools/parity/JOB_FORMAT.md` (the job, the matched lighting, the Unreal driver), `tools/parity/scene/build_scene.py`.
- [SiteFile](../../specs/Contract/SiteFile.md) `pictures[]`. [PlatformDependencies](../PlatformDependencies.md) M9.
- [`261014_R_MaterialPipeline.md`](261014_R_MaterialPipeline.md) F-MP-6 (the rig's pictures are not thumbnails), RD-MP-2 (Unreal hero picture, waiting on a showcase runtime).

## Status

**Seeded 2026-10-14 (the lead, during Phase17's execution). Pass 1 owed:** the survey of shader-ball subjects and backgrounds (Q-CP-1, Q-CP-2) and the rig's options (Q-CP-3 to Q-CP-6), then the lead's rulings and a seeded phase. Roadmap: *Comparison Pictures in Each Tool*, RESEARCH.
