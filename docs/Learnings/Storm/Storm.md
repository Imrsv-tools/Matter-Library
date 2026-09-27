# Storm (USD's Hydra renderer) and `usdrecord`

*As measured on OpenUSD 26.03, headless `usdrecord`, Phase05 (2026-09-26/27). Evidence: the Phase05 phase doc's Execution Log and commits.*

**S1 — A scene's lights can light NOTHING while every render still looks lit.** `usdrecord` adds a camera headlight by default, and that headlight hides two traps:

- **An un-normalized `DistantLight` is almost dark.** Its `intensity` is the sun *disk's* radiance: `hdSt/light.cpp` multiplies it by the disk's solid angle (0.53° ≈ 6.7e-5 sr). So an intensity of 3 is effectively zero. **Author `inputs:normalize = true`**, and `intensity` becomes irradiance, as a Blender Sun's strength is. UsdLux's own default sun is 50 000 for this reason.
- **A `DomeLight` with no `texture:file` is ignored**, with only a warning ("Dome light has no texture asset path"). Give it a texture, even a constant one.

**Test your lights with `--disableCameraLight`.** If the picture goes black, only the headlight was lighting it. *(The library's preview tool had never been lit by its own lights, and a key light of 3 and of 30 gave identical pixels.)*

**S2 — A hand-written flat Radiance `.hdr` is misread** (the visible dome read 0.36–0.52 and uneven, and it lit at ~56 %). An 8-bit PNG reads exactly. A constant sRGB code 188 is linear 0.503.

**S3 — One `usdrecord` run is not reliable.** The same scene at the same size came back correct twice and once almost entirely white, most likely the first frame racing the dome texture's load. **Render twice and accept only when two consecutive frames agree.**

**S4 — The VISIBLE dome is drawn as the raw texture.** `--enableDomeLightVisibility` shows the dome at its texture value, ignoring the light's `intensity` and the camera's `exposure`, both of which do apply to lighting. **Put a dome's level in its texture**, not in its intensity, if the background must match another renderer.

**S5 — `usdrecord` has no anti-aliasing.** One sample per pixel draws a cut-out's hole edges hard and jagged, and at a distance the holes average differently from a path tracer's. Render at N× the width and box-filter down.

**S6 — The USD camera's `exposure` attribute IS honoured** (a multiply by 2^exposure before the display encode). That's the way to judge a bright emitter unclipped: at exposure 0, luminance 12 is display white in every channel.

**S7 — See-through is transparency, not refraction.** Storm uses MaterialX's opacity method for `transmission` (it says so, to keep pre-1.38.5 behaviour). What is behind shows through **unbent** but **tinted per channel** by `transmission_color`. At a high IOR (diamond), the Fresnel-reflected sky dominates and the object reads as smoky grey.

**S8 — `subsurface_scatter_anisotropy` is ignored.** *(Phase07 7.3, 2026-09-27.)* Skin at 0.8 and at 0 gives the same Storm picture (mean subject colour moves by 0.1 of 255), while Cycles' random walk honours it. On Skin I, anisotropy adds about 1.2 to the rig's ΔE between the tools (1.90 → 3.10 under Blender's `RANDOM_WALK_SKIN`; it was 2.0 → 7.0 under `RANDOM_WALK`, Blender B8). Coat and fuzz are honoured in both (2.7 with both on). **So a Subsurface article's ΔE is not a regression when it authors anisotropy:** the article is correct OpenPBR, and the viewer approximates, as with S7.
