# Blender (5.2 LTS, Cycles)

*Phase05 (2026-09-26/27). Evidence: the Phase05 phase doc (F14, F15) and the 5.5 commits. B7: Phase07 (2026-09-27), its 7.1 commit.*

**B1 — A UV Map node (or a Normal Map node's tangent) that names a map the mesh lacks gives ZERO UVs, silently.** Every texture then draws one texel's colour. A USD import names its map `st`, and a Blender-made mesh names it `UVMap`. **Leave the name blank**, which means the mesh's active map, in any material meant for both. A shaded render can hide the failure (a flat colour still varies with lighting); render the UV itself as emission to check.

**B2 — A newly added Asset Library imports as "Pack" in 5.2**, which links the material read-only: every slider on it is greyed out. **Set the library's Import Method to Append (Reuse Data)** for editable materials.

**B3 — The exporter measures a material's edits against its node group's INTERFACE defaults.** This is our Blender add-on's rule (sparse deltas), and it forces one per-article group whose inputs default to that article's values. A master group shared across articles has only neutral defaults, so it would export an untouched article's own values as edits.

**B4 — Cycles volumes and random-walk subsurface need a CLOSED mesh.** On an open plane Cycles drew a thick-glass floor opaque white and a subsurface floor dark grey. Give a test floor thickness.

**B5 — Principled BSDF (5.2) has a `Thin Wall` input, but only ONE colour for transmission and for subsurface: Base Color.** OpenPBR has separate `transmission_color` and `subsurface_color`. Map each by lerping Base Color towards it by its weight, which is exact at weights 0 and 1. Thick-glass absorption goes on the volume: **Volume Coefficients** takes the absorption coefficient directly, σ = −ln(transmission_color) / transmission_depth.

**B7 — Blender's USD importer scales by the ROOT layer's `metersPerUnit`, and a sublayer's does not count.** *(Phase07 7.1.)* USD reads stage metadata from the root layer only. A file that sublayers a metres scene but authors no `metersPerUnit` of its own is a centimetre stage (USD's default), so Blender imports everything at 1/100. **Every picture still looks right:** the camera and lights shrink with it. Only a *distance a material states* gives it away. A subsurface radius or an absorption depth acts 100x too long, so skin renders pale and wax-like, and changing the radius "does nothing". **Author `upAxis` and `metersPerUnit` in every file you hand an importer**, and check an object's real size after import when a distance-based effect looks wrong.

**B6 — Blender's USD importer does not convert MaterialX.** A MaterialX-bound material imports with 0 nodes, and there is no option for it. Only UsdPreviewSurface converts. Build Blender materials by code instead.

**B8 — For an OpenPBR subsurface article, use Principled's `RANDOM_WALK_SKIN` method, not the default `RANDOM_WALK`.** *(Phase07 7.3, CM-Q10, measured in the parity rig against Storm.)* It is closer for marble as well as skin (Marble ΔE 2.60 → 1.82; Skin III 5.64 → 3.46; Skin I 6.99 → 3.10). Under `RANDOM_WALK`, a light skin with forward scatter (`Subsurface Anisotropy` 0.8) rendered **grey-green** while its albedo was pink; `RANDOM_WALK_SKIN` keeps the tone. One method serves every Subsurface article, so the master carries it and no per-material setting is needed.

**B9 — Principled's `Anisotropic` is not OpenPBR's `specular_roughness_anisotropy`, and its default tangent is not the UV's.** *(Phase07 7.6.)* Principled uses Disney 2012 (aspect = √(1 − 0.9a); αx = r²/aspect, αy = r²·aspect). OpenPBR uses αt = r²·√(2/(1+(1−a)²)), αb = (1−a)·αt. Matching both the ratio and the lobe area gives **a′ = a/0.9** and **r′ = r·(2(1−a)/(1+(1−a)²))^¼**, which is exact up to a = 0.9 and the identity at a = 0. An **unlinked** Principled `Tangent` is the object's radial "generated" tangent, while OpenPBR's default is `Tworld`, from texcoord 0. **Link a Tangent node in UV-map mode (blank name = the active map, B1).** Measured: the hair article's highlight stretches along `U` in both Storm and Cycles (test scene ΔE 1.80 / 1.05).
