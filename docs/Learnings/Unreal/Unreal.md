# Unreal Engine 5.8 (Substrate) and the Matter runtime

*As measured on Unreal 5.8.0 (Linux, Vulkan SM6, Substrate on), Phase06 (2026-09-29/30). Evidence: the Phase06 phase doc's Execution Log, its commits, and the probe `docs/Planning/Research/260929_R_Spike_UnrealRuntime.md` (UR-F4–F10).*

## What the engine does

**U1 — OpenPBR ships on Substrate in the core engine, and there is a look-alike that is NOT it.** `/Engine/Functions/Substrate/MF_Substrate_OpenPBR_{Opaque,Translucent}` take the whole OpenPBR surface under its own names and output `OpenPBR_FrontMaterial` + `OpacityMask` (Translucent adds `Refraction (IOR)`). The Interchange plugin's `MX_OpenPBR_*` takes the same inputs but outputs Unreal's *classic* pins; wired to Substrate's front material it fails with *"Material information is invalid"*. Two wrinkles: Translucent names `subsurface_anisotropy` where Opaque has `subsurface_scatter_anisotropy`, and the Opaque function's `geometry_thin_walled` input does nothing (its own note: thin-walled is *"enabled in the panel"*, the material's `is_thin_surface`). *(UR-F4.)*

**U2 — Epic's function mixes metal and dielectric by PARAMETER BLENDING, so 0 < metalness < 1 renders too bright.** Its *"Is Metal?"* mix blends the slab's parameters, not the two lobes' light as OpenPBR does. Measured against Storm: metalness 0.87 read +9 % face-on and +24 % at grazing; at metalness 0 or 1 it agrees within 3 %. **Build a metal-capable master as TWO calls, at metalness 0 and 1, mixed per pixel by a `SubstrateHorizontalMixing` with parameter blending off** — which needs U3. *(Phase06 6.3.)*

**U3 — At the default 80 bytes per pixel, Substrate FLATTENS a coat into its base to fit, and the material gets brighter.** Two calls of Epic's function (U2) each carry a coat layer; at 80 bytes the compiler rewrites each `SubstrateVerticalLayering` as `SubstrateVerticalLayeringParameterBlending`, which brightened the dielectric ×1.14–1.39. At **`r.Substrate.BytesPerPixel=160`** both coats stay real layers and the grey card is exact. Nothing warns; see T1 to read what the compiler did. *(Phase06 6.3.)*

**U4 — Epic's function renders emission at 0.798 of OpenPBR's radiance** (`emission_luminance × emission_color`), with one call or two, specular on or off: the function's own scale. Multiply `emission_luminance` by 1/0.798 in the master. Emission is also applied on the base slab, so fuzz and coat attenuate it (the function's author note). *(Phase06 6.4.)*

**U5 — Translucency lit the default (volumetric) way has NO specular:** glass only darkened what was behind it, with no dome reflection. Set **`TLM_SURFACE_PER_PIXEL_LIGHTING`** (Glass_Clear went from ΔE 25.3 to 7.2). *(Phase06 6.4.)*

**U6 — Substrate's thin-surface subsurface draws a card as dark, noisy pixels in a single real-time capture**, solid or cut; the same card with `subsurface_weight` 0 is smooth. With no temporal accumulation to resolve it, it is unusable for a one-frame picture. The library's Hair master folds the light through the card into its colour instead (MasterSet's Hair note). *(Phase06 6.5.)*

**U11 — A subsurface colour of exactly 0 HANGS THE GPU.** Epic's OpenPBR function fed `subsurface_color` = 0 (a picture's black pupil texel multiplied in) lost the device on the first frame: `VK_ERROR_DEVICE_LOST`, kernel Xid 109 (context-switch timeout) + Xid 31, breadcrumbs in `SubsurfaceScattering`. A black *base* colour is fine; a black *scatter* colour is not. **Floor the scattered colour** (`max(…, 1e-4)`, invisible at 8 bits): with only that changed the same job rendered clean. The driver recovered; a hang is still a risk to a shared desktop, so treat any master that can scatter a texture's colour as needing the floor. *(Phase09 9.3.)*

**U12 — Substrate's Eye BSDF does not shade a plain eyeball.** On MakeHuman's eye (one sphere, the iris painted in its atlas, no cornea shell) with the picture as `DiffuseColor`, a soft iris-disc `IrisMask`, default normals and either the default or a 1 mm subsurface profile, it drew the iris as a grey smear with a dark band, in the rig's one-frame capture. Epic's warning holds: the model depends on its own eye geometry and UV layout. The library's eye stays on the Subsurface master. *(Phase09 9.3 spike, RD-P09-7.)*

## Headless capture (`USceneCaptureComponent2D`)

**U7 — A capture can draw a material as Unreal's default (world-grid) material while everything reports ready.** `GShaderCompilingManager->GetNumRemainingJobs() == 0`, no PSO precaching and 120 settle frames all held, and **the launch's FIRST material assignment** still drew the character's Subsurface and Hair parts as the checker, every launch; any later assignment of the same materials was right. `FMaterialResource::IsGameThreadShaderMapComplete()` is no signal either (it read false for 200,000 frames on a master that rendered). **The runtime renders a throwaway first setting** (`drivers/unreal.py` `warmup`). **Look at the picture before reading its number:** the checker is unmistakable, and a ΔE of 25 is not. *(UR-F7; Phase06 6.5, bisected on the character's own job.)*

**U8 — A persisted capture view state changes the per-frame dither on every capture**, so two captures of identical values differ by zero-mean noise (a no-op slider "moved" ~0.25 ΔE). Set `bAlwaysPersistRenderingState = false`. `r.Test.FreezeTemporalSequences` would also do it, but it is **compiled out of Shipping**. *(Phase06 6.3.)*

**U9 — A directional light's SPAWN rotation did not reach the light:** it lit straight down at the right strength. Set the rotation again on the component once it is Movable, and log `GetDirection()`. This, not the light units, was the probe's "2.5× too bright" (UR-F10). *(Phase06 6.1.)*

**U10 — A Shipping build compiles `UE_LOG` out**, so a headless Shipping run leaves no log at all. The runtime writes its own record beside its pictures (`matter_runtime.log`). A Shipping package needs glibc 2.28, runs with no display on SDL's `dummy` driver, and strips to 380 MB (debug symbols and the Vulkan debug layers are ~520 MB of a Development build). *(UR-F8; Phase06 6.2.)*

## Techniques (Python cannot see these)

**T1 — Read what Substrate compiled a material to.** Launch once with `-ini:Engine:[ConsoleVariables]:r.DumpShaderDebugInfo=1`, then read `Saved/ShaderDebugInfo/<platform>/<material>/…/BasePassPixelShader.usf`: the defines `SUBSTRATE_CLAMPED_CLOSURE_COUNT` and `SUBSTRATE_MATERIAL_NUM_UINTS` give the budget, and the operator calls (`SubstrateVerticalLayeringParameterBlending(…)` against `SubstrateTree.SubstrateVerticalLayering(…)`) show what was flattened (U3). Python cannot read a material's Substrate report.

**T2 — Read an engine MaterialFunction's inputs and author notes with `strings` on its `.uasset`.** Python cannot list a MaterialFunction's expressions; `strings` gives every input name, the helper functions it calls and its comment text (U1's thin-walled note, U4's emission note).
