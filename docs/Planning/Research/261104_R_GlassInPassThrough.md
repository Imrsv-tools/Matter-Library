# Research — See-through glass shows the real room in the headset

**Opened:** 2026-11-04 · **Mode:** research. This is a **diagnosis** of a fault a consumer showed, not a design. It gathers and commits to nothing.
**Mnemonic:** `PTG` (ids `PTG-Qn`, `PTG-Fn`, `PTG-RDn`).
**Raised by:** the lead, 2026-11-04, from a headset sitting in IMRSV's Studio on the asset tooling's 1970s house (`261104_R_AssetToolingHouseAsks.md`). Their words: *"the material for the Windows was doing some strange passthought... I caould see my real screens fainly in the reflection of the windows"*.

**Question:** why does the window glass let the real room show through in the headset, and who fixes it?

**Extends, does not replace:** `261005_R_PlatformThinGlassAsks.md` (how the see-through masters refract in Unreal: TG-F7, the rough blur, and TG-F8, what turning refraction off costs) · `docs/specs/Ontology/MasterSet.md` (the TranslucentThin and TranslucentThick rows: *"roughness blurs the transmitted view in every consumer"*).

**Public-repo note.** Studio is private. Its behaviour is summarised by role, with no paths, ids or code of its own. Engine file names are Unreal Engine 5.8's own.

**Measured at:** `3e56ff7` (2026-11-04), on the machine with Unreal, by reading the Unreal Engine 5.8.0 source there. **Nothing was rendered or run.**

**Word used here:** **pass-through** is the consumer's word for a headset mode in which the runtime lays Studio's frame over its own cameras, so whatever Studio leaves see-through shows the real room. It is not a library term.

---

## The short version

- **The glass is not doing it. Unreal's rough-refraction pass is.** The glass is drawn twice: its translucent surface, which leaves the frame's alpha alone, and the refraction pass, which re-samples the scene behind the glass. In 5.8 that pass reads a copy of the scene made **without an alpha channel**, so it writes "see-through" into every pixel the glass covers.
- **In pass-through, see-through means the real room.** The headset adds the room on top of the frame by the frame's alpha. Behind a window is a bright scene, so the room arrives as a faint additive ghost, which reads as a reflection.
- **It is every see-through article, not windows only.** All nine articles on TranslucentThin and TranslucentThick draw in that pass: the house's toilet water too, and any gem.
- **One console line tests it in the headset:** `r.Refraction.Blur 0` while looking at a window. If the room goes, the cause is confirmed. That setting also turns off the rough blur the contract requires, so it is a test, not the fix.
- **The fix is the consumer's or the engine's, not the masters'.** A master can only avoid the pass by giving up the blur (TG-F8). The library's part is to record it.

---

## Pass 1 — What was seen, and what the engine source says

**Examined:** Studio's run log of the sitting (16:42 – 16:50 local) and its pass-through spec · `unreal/MatterRuntime/Scripts/build_masters.py` · in the 5.8.0 engine source: `BasePassPixelShader.usf`, `TranslucentRendering.cpp` (`GetTranslucentBlendState`), `ComposeSeparateTranslucency.usf`, `DistortionRendering.cpp`, `DistortApplyScreenPS.usf`, `DistortFiltering.usf`, `SceneRendering.cpp`, `Config/Linux/BaseLinuxEngine.ini`.

### What was seen

- **PTG-F1 — The sitting.** In the headset, pass-through on (the log: the runtime offered alpha blend, pass-through on, the desk window shown), the lead opened their composition 47. It holds the asset tooling's house. The windows bind `Glass_Clear_Clean_Base_s01_v01` with two wear layers (densities 0.25 and 0.35) and a green transmission tint (0.82, 0.95, 0.88). Through them the lead saw their real monitors, faintly, as if reflected.
- **PTG-F2 — How Studio's pass-through works** (its own spec, summarised). The frame's alpha is propagated to the headset project-wide. The headset shows *the frame's colour + the room × (1 − the frame's opacity)*. Unreal's alpha 1 means see-through, so Studio flips it for the headset. A black shell far behind everything keeps an empty sky solid. A hole is made on purpose in one place only: the window onto the desk. **Everything else is meant to be solid.** So the room showing in the glass means the glass pixels reach the headset partly see-through.
- **PTG-F3 — Studio draws the window with the library's own `M_Matter_TranslucentThin`**, built by `build_masters.py`. That master blends with Substrate's coloured transmittance (`BLEND_TRANSLUCENT_COLORED_TRANSMITTANCE`) and refracts by the index of refraction (`RM_INDEX_OF_REFRACTION`). TranslucentThick is the same in both settings.

### The glass's own surface leaves alpha alone

- **PTG-F4 — The translucent surface writes no see-through.** With dual-source blending, the glass outputs alpha 0 on the add target and 1 on the multiply target (`BasePassPixelShader.usf`, the `MATERIAL_WORKS_WITH_DUAL_SOURCE_COLOR_BLENDING` branch). Before depth of field, Substrate's blend makes the new alpha `src0.a + dst.a × src1.a`, which is `dst.a`, unchanged. After depth of field, its blend leaves alpha unchanged outright (`GetTranslucentBlendState`). The composite of the after-DOF layer multiplies alpha (`ComposeSeparateTranslucency.usf`, `SceneColor.a × translucency.a × grey(modulation)`). So wherever the scene behind is solid, it stays solid.

### The refraction pass writes see-through

- **PTG-F5 — Rough refraction reads a copy of the scene that has no alpha.** With Substrate on and `r.Refraction.Blur` above 0, the refraction pass blurs the background from a mip chain (`DistortionRendering.cpp`). That chain is created as `PF_FloatR11G11B10`, a format with no alpha channel, and the shader that fills it writes `float4(colour, 1.0)` (`DistortFiltering.usf`, `CopySceneColorDepthTexturePS`). The engine's own Linux platform ini sets `r.Refraction.Blur=1`, and Studio runs with Substrate on.
- **PTG-F6 — That alpha of 1 lands in the frame.** The apply pass samples the chain for every pixel the glass covers, both the refracted sample and the unrefracted one it blends toward (`DistortApplyScreenPS.usf`, the `USE_ROUGH_REFRACTION` branch), so its alpha is 1. The merge then writes the result back over the scene with alpha `1 × the before-DOF translucency's background visibility × its grey transmittance`. It keeps the scene's own alpha only when `r.Deferred.SupportPrimitiveAlphaHoldout` is on (`DistortionRendering.cpp`, the merge's blend state; `SceneRendering.cpp`). That setting is off by default and Studio's config does not set it.
- **PTG-F7 — So the glass turns see-through by roughly its transmittance.** An alpha near 1 is Unreal's "see-through". After Studio's flip the headset gets a low opacity at the window, and the room is added in at close to its full brightness. The exact amount is not predicted here, because the after-DOF composite multiplies in the glass's grey transmittance again.
- **PTG-F8 — Why it reads as a reflection.** The headset adds the room on top of the frame's colour (PTG-F2). Behind a window is a bright scene, so the room arrives as a faint ghost laid over it, and is plainest where the scene behind is dark. That is what a reflection looks like. The consumer recorded the same layer the same day for another see-through effect, a deliberate hole, where it found that the frame's colour behind a hole washes out the room.
- **PTG-F9 — Without rough refraction the alpha would be right.** The plain refraction path samples the real scene colour, which has alpha, at the shifted position (`DistortApplyScreenPS.usf`, the non-rough branch). So the alpha follows the solid scene behind. Turning the pass off entirely (`r.DisableDistortion 1`) also leaves alpha alone, and also loses the blur (TG-F8). Both settings are live console variables (`ECVF_Scalability` and `ECVF_Default`), so they need no relaunch.

### Scope

- **PTG-F10 — Every see-through article, both masters.** The fault is in a pass that every master with a refraction method draws in. That is TranslucentThin and TranslucentThick: all six thin articles and all three solid ones (TG-F1's list). In the house that includes the toilets' water, which binds `Glass_Clear`. The wear layers, the tint and thin versus solid play no part.
- **PTG-F11 — Only Unreal in pass-through.** Blender and Storm have no pass-through, and a flat screen ignores alpha. The library's Unreal rig cannot show it either: the runtime does not propagate alpha, and its captures are RGB-only PFMs. **The headset is the only surface that shows this today.**
- **PTG-F12 — Nothing in the articles or their `.mtlx` is wrong.** The masters do what the contract asks: a rough blur on the transmitted view. In 5.8 the engine's blur breaks alpha.

### Ways out

None is chosen here. The fix is not the library's to make.

| | What | Keeps the rough blur? | Whose |
|---|---|---|---|
| (a) | Studio sets `r.Refraction.Blur 0` while pass-through is on | **no:** frosted glass reads clear in the headset, against `MasterSet.md`'s *"in every consumer"* | Studio, one line |
| (b) | Patch the engine: the merge takes alpha from the unrefracted scene, or the mip chain keeps alpha | yes | whoever builds the engine; carried across upgrades; worth reporting to Epic |
| (c) | The library's masters stop refracting (method "none") | **no**, and in every mode, not only the headset (TG-F8) | the library — ruled out by its own contract |

### Questions

- **PTG-Q1 — Does `r.Refraction.Blur 0` remove the room from the windows?** The lead can answer this in the headset: look through a window, type it in Studio's console, then `r.Refraction.Blur 1` to bring it back. If the room goes, PTG-F5 – F7 are confirmed. If it stays, the cause is elsewhere, and the next test is `r.DisableDistortion 1`.
- **PTG-Q2 — In pass-through, may a consumer drop the rough blur?** (Way (a).) `MasterSet.md` says roughness blurs the transmitted view *"in every consumer"*, so (a) is a contract question for the lead, not a setting Studio can just flip. (b) keeps the contract and costs an engine patch.

---

## Status

- **Passes captured:** 1 (2026-11-04, the library's side, by reading the engine source).
- **Current direction:** the cause is Unreal 5.8's rough-refraction pass writing see-through alpha over every see-through article (PTG-F5 – F7), confirmed by reading and **not yet by eye**. The library's articles and masters are not at fault (PTG-F12). The fix is Studio's or the engine's (Ways out).
- **Open:** PTG-Q1 (the one-line headset test) · PTG-Q2 (whether pass-through may drop the blur).
- **Not run:** nothing was rendered, launched or built. The amount of room let through (PTG-F7) is not predicted.
- **What was added:** this doc only. No article, master, tool, spec or ledger row is changed.

▶ **Next:** the lead's one-line test (PTG-Q1). If it confirms, a quick fix can record the ask in `PlatformDependencies.md` (P36, the next free id as listed 2026-11-04) and the engine fact in `docs/Learnings/Unreal/`, and Studio chooses (a) or (b) after PTG-Q2.
