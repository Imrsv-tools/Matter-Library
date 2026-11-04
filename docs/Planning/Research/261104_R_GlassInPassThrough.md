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

## Pass 2 — The consumer's try: the engine's holdout switch cures it and costs the frame rate (2026-11-04)

*The lead asked what the consumer had just tried, after a headset take: the room left the windows, and the house ran at 10 fps.*

**Examined:** the consumer's record of the take (summarised by role) · its two run logs, before and with the switch · `DistortionRendering.cpp` (the merge) · `Engine/Build/InstalledBuild.txt` · `build_masters.py` (the thin master's refraction).

- **PTG-F13 — What was tried.** The consumer turned on `r.Deferred.SupportPrimitiveAlphaHoldout`, the one setting under which the merge keeps the scene's alpha (PTG-F6). It did this for a problem of its own with a deliberate hole, and the same take looked at the house.
- **PTG-F14 — The windows passed, which confirms the mechanism by eye.** The lead, in the headset: *"no more pass through in reflection"*. So the room in the glass was the merge's alpha (PTG-F5 – F7). **PTG-Q1 is answered by this, by a different test from the one asked.**
- **PTG-F15 — The cost is the switch, measured from the logs.** Each log line carries the engine's frame counter, so the frame rate can be read from line spacing (median over the spans). Same house, same session order:

  | | without the switch | with it |
  |---|---|---|
  | the house | 52 fps (164 spans) | 11 fps (two opens, 18 and 11 spans) |
  | a scene without glass | 60 fps | 60 fps |

  The switch makes the engine draw every translucent thing a second time into a holdout pass, with a copy of scene colour, per view. Which part costs this much in the house was not measured. **The consumer has reverted it.**
- **PTG-F16 — The switch is the wrong tool for this.** It turns on a whole feature (holdouts for every translucent primitive) to reach one side effect, the merge's blend state. The fault needs none of that feature.
- **PTG-F17 — The thin master refracts only for the blur.** It feeds an index of 1.0, so it bends nothing (`build_masters.py`, M6). The distortion pass draws it only to blur the view by roughness. A clear window (`Glass_Clear`, roughness near 0) gets almost nothing from the pass and still has its alpha broken by it.
- **PTG-F18 — A fix inside the engine is one line, but this engine cannot be rebuilt in place.** In rough mode the apply pass's alpha is always 1 (PTG-F6). So the merge's output alpha is exactly the factor the scene's alpha should be multiplied by. Blending alpha as `dst × src` (`BF_Zero, BF_SourceAlpha`) whenever rough refraction is on would be correct, at no cost. But the engine on the machine with Unreal is an installed build (`InstalledBuild.txt`), so the renderer module cannot be rebuilt in place. Patching it means a source build of the engine, kept across every upgrade. That is the fix to report to Epic.

### Ways out, revised

| | What | Frame cost | Keeps the rough blur? | State |
|---|---|---|---|---|
| (s) | the engine's holdout switch | **about a fifth of the frame rate** in the house | yes | tried, cured, **reverted** (PTG-F13 – F15) |
| (a) | Studio sets `r.Refraction.Blur 0` while pass-through is on (it already sets two settings when pass-through turns on) | none; it saves the mip chain | **no**, in the headset only: rough see-through articles read clear there | **not yet tried by eye**; by reading the plain path keeps alpha (PTG-F9) |
| (b) | engine patch (PTG-F18) | none | yes | needs a source-built engine; report to Epic |
| (d) | the thin master stops refracting and blurs in the material, from scene-colour taps | per glass pixel, only where rough | yes, every mode | a master redesign, re-judged on the rig: a phase, not a fix |
| (c) | the masters stop refracting, no blur | none | no, every mode | ruled out (contract) |

- **PTG-F19 — (a) is the cheap one, and its only loss is small.** The thin master bends nothing anyway (PTG-F17), so in the headset (a) changes only the rough articles' blur. The clear windows of this house would look the same. It still needs the lead's ruling, because `MasterSet.md` says the blur holds *"in every consumer"* (PTG-Q2).

### Questions, revised

- **PTG-Q1 — answered** (PTG-F14): the merge's alpha is the cause.
- **PTG-Q2 — still open:** may a consumer in pass-through drop the rough blur (way (a)), until (b) or (d) exists?
- **PTG-Q3 — new:** does `r.Refraction.Blur 0` clear the windows **at the house's normal frame rate**? It is one console line in the headset, and the last check before (a) is built.

---

## Pass 3 — Way (a) tried in the headset (2026-11-04)

- **PTG-F20 — `r.Refraction.Blur 0` clears the windows at the house's normal frame rate.** The lead typed it in Studio's console in the headset, in the house. Their words: *"r.Refraction.Blur 0 cleared it, still 52 fps"*. **PTG-Q3 is answered:** (a) works and costs no frame rate. It also confirms PTG-F9 by eye: without rough refraction the merge's alpha is right.
- **What (a) still costs:** the rough blur, in the headset only (PTG-F19). That is PTG-Q2, the lead's ruling, still open.

---

## Resolved

- **PTG-RD1 — In pass-through, a consumer may drop the rough blur (way (a)) until a fix keeps it; record it in the contract, the ledger and the engine notes (the lead, 2026-11-04).** Answers PTG-Q2. The question put to them: may Studio turn the glass blur off whenever pass-through is on, at the cost of rough see-through articles reading clear in the headset only, with a dated note on `MasterSet.md`'s *"every consumer"* rule? Their words: *"yes, do all three and push"*. The three were: a comment on the consumer's tracker, a library quick fix (the ask in `PlatformDependencies.md`, the note on the rule, the engine fact in `docs/Learnings/Unreal/`), and a push.

---

## Status

- **Passes captured:** 3 (2026-11-04; Pass 1 by reading the engine source, Pass 2 from the consumer's take and its logs, Pass 3 the lead's console test).
- **Current direction:** the cause is **confirmed by eye** (PTG-F14): Unreal 5.8's rough-refraction merge writes see-through alpha over every see-through article. **Way (a) is shown to work:** with the rough blur off, the windows are clear at the house's normal frame rate (PTG-F20). The engine switch also cures it, but at about a fifth of the frame rate, and is reverted (PTG-F15). (b), an engine patch, is the clean way and needs a source-built engine. The library's articles and masters are still not at fault (PTG-F12). *(Was, at Pass 2: "the cheap way is (a) … not yet tried by eye". At Pass 1: "confirmed by reading and not yet by eye".)*
- **Open:** none at research altitude. **PTG-Q2 is ruled** (PTG-RD1): in pass-through a consumer may drop the rough blur until a fix keeps it. *(Was: "PTG-Q2 … the one thing between Studio and building (a)".)*
- **Not run:** any source build of the engine · (a) built into Studio (it was a console line, for one session).
- **What was added:** this doc, and at the lead's direction a quick fix (the commit after the ruling) that made three edits. `MasterSet.md` gains the pass-through exception under the rough-transmission rule, plus a history line. `PlatformDependencies.md` gains **P36** (Studio turns the blur off while pass-through is on). `docs/Learnings/Unreal/Unreal.md` gains **U18** (the engine fact). No article, master or tool is changed. *(Was: "this doc only".)*

▶ **Next:** Studio builds P36 on its side. The exception lifts when a fix keeps the blur at no frame cost: way (b), an engine patch, or way (d), a blur drawn in the thin master, which would be a library phase.

*(Superseded 2026-11-04 by the ruling. Was: "the lead's ruling on PTG-Q2. If yes, Studio builds (a) … A quick fix records the ask …".)*

*(Superseded 2026-11-04 by Pass 3. Was: "the lead's one-line test of (a) (PTG-Q3) and their ruling on PTG-Q2. Then a quick fix can record the ask …".)*

*(Superseded 2026-11-04 by Pass 2. Was: "the lead's one-line test (PTG-Q1). If it confirms, a quick fix can record the ask … and Studio chooses (a) or (b) after PTG-Q2.")*
