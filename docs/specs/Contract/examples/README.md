# Contract examples

`Reference_Copper_Verdigris_Aged_Base_s01_v01.mtlx` is a verbatim copy (2026-09-23) of the live article `MatterLibrary/materials/engineered/metal/Copper_Verdigris_Aged_Base_s01_v01.mtlx`, chosen because it exercises the most of the [MaterialX template](../MaterialXTemplate.md): the 8 Creator ports, `place2d`, both overlays and the maskset as linear data modulating roughness and normal, full base PBR maps, and the `imrsv_metadata` hint. The live article is the authority; this copy is for reading only.

Its texture paths are relative to the article's own folder, not this one, so it does not resolve textures from here.

The platform's former hand-authored `OpenPBR_Template_Reference.mtlx` was retired: it taught the overlay defect (`overlay1_dust_tex` loaded as `srgb_texture` and `<mix>`ed over base colour), which the [modulator rule](../../Ontology/MasterSet.md) and the [render-role texture](../LCDSchema.md) contract forbid.
