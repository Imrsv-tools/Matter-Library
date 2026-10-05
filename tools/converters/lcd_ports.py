"""The frozen Creator port vocabulary (LCDSchema.md §Creator-adjustable subset), as plain data.

It lives apart from the assembler so that a tool with no MaterialX module can read it: the
carrier check runs under the USD toolchain's Python, which has `pxr` and no `MaterialX`, and for
as long as it imported this from `assemble_mtlx` it could not start there (Matter-Library#2).
`assemble_mtlx` imports it from here and is still where the vocabulary is USED; this file imports
nothing.
"""

DUST_COLOR = "0.413, 0.386, 0.308"   # linear; see overlayN_color below

# Frozen LCD interface-input vocabulary (LCDSchema.md, Phase 53 D3):
#   port name -> (type, default value string, uiname, extra-attrs dict)
LCD_PORTS = {
    "base_color_tint": ("color3", "1.0, 1.0, 1.0", "Base Color Tint", {}),
    "uv_scale": ("vector2", "1.0, 1.0", "UV Scale", {}),
    "uv_offset": ("vector2", "0.0, 0.0", "UV Offset", {}),
    "uv_rotation": ("float", "0.0", "UV Rotation (deg)",
                    {"unittype": "angle", "unit": "degree"}),
    "overlay1_density": ("float", "0.0", "Overlay 1 Density", {}),
    "overlay2_density": ("float", "0.0", "Overlay 2 Density", {}),
    "overlay3_density": ("float", "0.0", "Overlay 3 Density", {}),   # added 2026-09-25 (cap 2 -> 3)
    "maskset_blend": ("float", "0.0", "Maskset Blend", {}),
    "roughness_bias": ("float", "0.0", "Roughness Bias", {}),
    # Phase10 (RD-P10-1): a DEPOSIT overlay's colour (dust), which the Creator may change. The
    # start value is Physically Based's Sand (CC0; 0.44, 0.386, 0.231) desaturated halfway to its
    # own luminance, since household dust is greyer than sand. MasterSet §Overlay semantic.
    "overlay1_color": ("color3", DUST_COLOR, "Overlay 1 Color", {}),
    "overlay2_color": ("color3", DUST_COLOR, "Overlay 2 Color", {}),
    "overlay3_color": ("color3", DUST_COLOR, "Overlay 3 Color", {}),
    # Phase12 (RD-GLC-2): the colour seen THROUGH see-through matter, which the Creator may set.
    # OpenPBR's own name, type and range; the default here is OpenPBR's, and an article's start
    # value is its own authored `transmission_color` (assemble_mtlx.SET_PORTS).
    "transmission_color": ("color3", "1.0, 1.0, 1.0", "Transmission Color", {}),
    # Phase12 12.4: the colour a light emits and how bright it glows, which the Creator may set.
    # OpenPBR's own names, types and defaults; `emission_luminance` is radiance, as OpenPBR's
    # input is (Learnings MaterialX M3), from 0 with no maximum. An article starts at its own.
    "emission_color": ("color3", "1.0, 1.0, 1.0", "Emission Color", {}),
    "emission_luminance": ("float", "0.0", "Emission Luminance", {}),
}
