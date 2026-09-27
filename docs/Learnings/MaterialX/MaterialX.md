# MaterialX (1.39)

*Phase05 (2026-09-26/27). Evidence: the Phase05 phase doc (F10) and the 5.3 commit.*

**M1 — `normalmap` outputs a WORLD-space normal.** The stdlib definition says it transforms "into 'world' space". Anything that combines normals must do so in **tangent** space, **before** the one `normalmap`: a second layer's normal blend, a bump added from a packed overlay's RG, or a "flat" fallback. So decode the map (`2c − 1`), combine, renormalize, re-encode (`n·0.5 + 0.5`), and pass that through `normalmap` once. Two symptoms of getting this wrong:

- A flat `(0, 0, 1)` fed straight into `geometry_normal` is a **fixed world +Z** normal, so the whole object shades as one flat colour.
- Bumps added after `normalmap` run along **world X/Y**, so their effect depends on which way the surface faces.

*(Our assembler did both for months: three articles rendered flat white in USDLiveView's renderer.)*

**M2 — `rotate2d` turns the COORDINATE clockwise.** `mx_rotate_vector2` is `(c·x + s·y, −s·x + c·y)`, so the texture appears to turn **counter-clockwise** by `amount` degrees. A renderer whose rotate node turns counter-clockwise (Blender's Vector Rotate) needs `−amount`. `place2d` (at defaults) is `uv / scale`, then `rotate2d`, then `− offset`.

**M3 — OpenPBR's `emission_luminance` is used as radiance directly** (`emission_color × emission_luminance` into a `uniform_edf`), with no unit conversion. It is the same quantity as a Blender Emission Strength.

**M4 — OpenPBR's `subsurface_radius` is in scene units.** In a metres scene, 1.5 means 1.5 m of scattering. OpenPBR's graph also mixes the diffuse colour from `base_color` towards `subsurface_color` by `subsurface_weight`, so base-colour detail (veins) keeps only `1 − weight` of its strength.
