# Phase06 — Unreal Test Runtime

**Status:** SEEDED (phase doc written 2026-09-26; discovery has not opened). Numbered by the lead, 2026-09-26 (verbatim in `Phase05_TestRig.md`). **This phase runs on the UE machine** (Linux, with its own agent and clone of this repo; rulings BP6, BP7). It starts after Phase05 is pushed. The thinking behind it is `docs/Planning/Research/260926_R_BigPicture_NimbleSetup.md` (Passes 7, 8).

## Outcome

**The test rig's picture sheet gains an Unreal column, rendered by a small Unreal app of our own that runs on any Linux machine with a GPU.**

Concretely, at close: a packaged Unreal 5.8 app (Substrate on) takes Phase05's render job (a material, its slider settings, the test scene) and writes one picture per setting, headless. It carries its own versions of the 7 master materials. The 7 test materials have an Unreal column in their sheets, and the package can be copied to the original machine so all three tools run there from Phase07 on.

## Why this is a phase

It is one thing, the Unreal leg of the rig. It needs a machine with Unreal on it, and nothing else in the plan does. Two choices are expensive to change later: **how the masters are built** (by a script that can rebuild them, or by hand in the editor) and **how the app reads a `.mtlx`**. Both carry forward into the public Unreal package the Roadmap already wants (*Unreal Reference Masters*).

## Scope

**In:**
- **Prove the risky part first:** one grey sphere rendered headless from a packaged Linux build, with Substrate on, giving the same picture every run (auto-exposure off, frames allowed to settle).
- **The 7 masters,** mirroring `docs/specs/Ontology/MasterSet.md`. Every input is a parameter, since a packaged app can't compile new shaders. Ideally they are built by an editor script, so they can be rebuilt rather than hand-clicked.
- **The loader:** it reads a `.mtlx` (which master, which textures, which values, the default slider values), loads the PNGs with the right colour settings (colour textures as sRGB, data textures as linear, the normal map's green channel the right way up), and sets them on the master.
- **The test scene** from Phase05's USD file, and **the render-job driver** exactly as Phase05 wrote it down.
- **The Unreal column** for the 7 test materials, compared in Phase05's picture sheets. *(Updated 2026-09-27 at the Phase05 close: the test set is **11 articles**, the grey card for calibration first. The render-job contract, the scene, the matched lighting an Unreal driver must reproduce, and the two open questions its column should settle (F12, F16) are in `tools/parity/JOB_FORMAT.md`. The Blender masters Phase05 built by code (`blender/masters/`) are a worked reference for the Unreal ones.)*
- **The package,** and how it gets to the other machine (it is too large for git).

**Out:**
- IMRSV Studio. Our runtime passing shows the materials can work in Unreal, not that Studio matches; Studio gets an occasional spot check.
- Publishing the masters as a public Unreal package (*Unreal Reference Masters*, later).
- Building new materials (Phase07 Character Materials, which runs here at the same time; Library Coverage, now unnumbered).

**Coupling with Phase07 (added 2026-09-27, lead re-sequencing CM4):** Phase07 runs while this phase builds the masters. It may add inputs to the Subsurface master (coat, fuzz, scatter anisotropy), a colour channel on layers, and possibly Hair or Eye masters. A packaged app can't compile new shaders, so **pull before building the masters, and read Phase07's rulings first.** A contract change that lands later means rebuilding the package, which the lead accepts.

**What Phase07 actually landed (closed 2026-09-27):**
- **No new master.** There is no Eye master (D-E), no `Skin` master (CM-Q10) and no Hair master (L2: Masked served). The layer colour channel was not built, and stays with Library Coverage (L3; it was Phase08 until 2026-09-28).
- **Subsurface** runs Blender's `RANDOM_WALK_SKIN` method, and its inputs gain `subsurface_scatter_anisotropy`.
- **Every master may carry** coat (`coat_{weight,color,roughness,ior}`), fuzz (`fuzz_{weight,color,roughness}`) and specular anisotropy (`specular_roughness_anisotropy`, along UV0's `U`). Each is authored only when set, and each is off at its default.
- **Masked** gains `cutout_map`: the mesh's cut-out texture, supplied per binding, sampled on UV0 without `place2d`, and thresholded by `opacity_cutoff` ([LCDSchema §Cut-out map](../../../specs/Contract/LCDSchema.md#cut-out-map-the-meshs-supplied-at-binding)).
- **The rig's character job** (`tools/parity/JOB_FORMAT.md` §The character job) is the Unreal driver's second job shape: one article per part, and `bindings[].cutout_map` on the hair, brows and lashes.
- The consumer side of all this is `PlatformDependencies.md` P15–P19.

**Since then (2026-09-28): Phase08 adds a `Hair` master** (in progress on this machine; the "no Hair master" line above predates it). Its graph is Masked's plus thin-walled translucency and soft coverage; Unreal's side is the **Hair shading model**. Pull and read `Phase08_CharacterAppearance.md` and `260928_R_HairAndNailRendering.md` before building it.

**Reevaluate under the lead's LCD ruling (2026-09-28)** (`_Architecture.md` §Design principles). The lead: *"we use the master materails to lean in on the egines BEST qaulities to make the material look as good as it can"*. The LCD is the shared parameter vocabulary, not a shared ceiling, so **each Unreal master should use Unreal's best feature for its matter**, even where Storm and Blender have no equivalent. Cross-tool agreement is judged on whether each parameter moves every tool the same way, not on matching pictures. Candidates, for this phase's discovery:
1. **Masked coverage: dithered, not hard-cut.** *Opacity Mask Dither* with temporal AA, two-sided, on Masked and Hair. This follows the lead's pick for hair, soft edges (Phase08, *"I do think c soft edges is the way"*), and applies to Lace too. Storm keeps a cutoff.
2. **Skin: Unreal's best skin scattering** (a Subsurface Profile, or Substrate's skin path) for skin, even if marble, jade and wax want another. CM-Q10 kept one Subsurface master because Blender's `RANDOM_WALK_SKIN` served both. That was a Blender measurement, so it does not decide Unreal. A `Skin` master (or an Unreal-side split) is now legitimate if Unreal needs it.
3. **Fabrics: Unreal's Cloth shading model** for Opaque articles that set fuzz (cotton, denim, felt, velvet). Fuzz is OpenPBR's sheen; the Cloth model is Unreal's best at it.
4. **Eyes: reconsider D-E** (no `Eye` master). D-E refused one because Unreal's eye model has inputs (iris depth, caustics) the others lack, which is the superseded wording. The open catch: Unreal's eye model expects one eye mesh with an iris mask, while the character's eye is split into sclera, iris, pupil and cornea (Phase07 L1).
5. **Strands later:** when the platform moves to grooms, the Hair master uses Unreal's strand hair model, driven by the same article parameters (colour, roughness). The article stays `open_pbr_surface` (Decision of record 1); the master picks the engine's fibre model.

## Open questions (settle during this phase)

- Is Unreal 5.8 available and working on the UE machine's Linux install?
- Real-time rendering or Unreal's path tracer for the comparison renders? The path tracer is steadier; real-time is what users see.
- Where does the package live between machines: a release download, or a copy?

## Notes

- Read Phase05's closed doc first. The render-job format and the test scene are the contract with the other machine.
- Keep the Unreal project in its own folder, and pull before every commit: two machines share this repo.

## Discovery Log

_(numbered passes accrue here: examined → finding → decision / hypothesis / open question)_

## Discovery Status

- **Passes captured:** —
- **Current working direction:** —
- **Open decisions:** —
- **Checks to carry forward:** —

## Execution Log

_(populated during execution)_
