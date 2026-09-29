"""The Matter Library's Unreal masters, built by script (Phase06; no binary asset is committed).

Run as a commandlet (no GPU; unreal/build.sh does it):

  UnrealEditor-Cmd MatterRuntime.uproject -run=pythonscript -script=<this> \
      -EnablePlugins=PythonScriptPlugin,EditorScriptingUtilities -unattended -nullrhi

Each master is Epic's Substrate OpenPBR function (``MF_Substrate_OpenPBR_{Opaque,Translucent}``,
engine content, UR-F4) plus our network around it (Phase06 D6), a port of
``blender/masters/build_masters.py``'s ``_build``; the formulas are MaterialX's, and that file
names each one's source. Parameter names are the article's (D5): OpenPBR's for lane A, the frozen
Creator ports, and the author-tier names. Every master is deleted and rebuilt, so the output
depends only on this script and the engine.

Built so far (6.1): the Opaque core's first form (constants, the tint, and the base-colour
texture on the mesh's own UVs, which the rig's UV-grid wall needs; ``place2d`` comes at 6.3)
and the Sky (the rig's visible dome, unlit, which the runtime's sky light captures).
"""

import unreal

MEL = unreal.MaterialEditingLibrary
EAL = unreal.EditorAssetLibrary
TOOLS = unreal.AssetToolsHelpers.get_asset_tools()
ROOT = "/Game/Masters"
FN_OPAQUE = "/Engine/Functions/Substrate/MF_Substrate_OpenPBR_Opaque"

# OpenPBR's defaults (MaterialX open_pbr_surface) for the lane-A inputs a master passes straight
# through to Epic's function, under their own names. The network's inputs (base colour,
# roughness) are wired by the network, not here.
PASS_THROUGH = {
    "base_weight": 1.0, "base_metalness": 0.0, "base_diffuse_roughness": 0.0,
    "specular_weight": 1.0, "specular_color": (1.0, 1.0, 1.0), "specular_ior": 1.5,
    "specular_roughness_anisotropy": 0.0,
    "coat_weight": 0.0, "coat_color": (1.0, 1.0, 1.0), "coat_roughness": 0.0, "coat_ior": 1.6,
    "fuzz_weight": 0.0, "fuzz_color": (1.0, 1.0, 1.0), "fuzz_roughness": 0.5,
}

# MasterSet §Material-settings intent (normative): coverage, shading model, two-sided.
SETTINGS = {
    "Opaque": ("opaque", False),
}


def log(msg):
    unreal.log("MATTER " + msg)


class Graph:
    """A small builder over MaterialEditingLibrary: nodes laid out left to right."""

    def __init__(self, mat):
        self.mat = mat
        self.y = {}

    def node(self, cls, col, **props):
        y = self.y.get(col, 0)
        self.y[col] = y + 110
        n = MEL.create_material_expression(self.mat, cls, -300 * col, y)
        for k, v in props.items():
            n.set_editor_property(k, v)
        return n

    def scalar(self, name, default, col=6):
        return self.node(unreal.MaterialExpressionScalarParameter, col,
                         parameter_name=name, default_value=float(default))

    def vector(self, name, default, col=6):
        r, g, b = default
        return self.node(unreal.MaterialExpressionVectorParameter, col,
                         parameter_name=name, default_value=unreal.LinearColor(r, g, b, 1.0))

    def op(self, cls, a, b, col, a_out="", b_out=""):
        n = self.node(cls, col)
        self.link(a, n, "A", a_out)
        self.link(b, n, "B", b_out)
        return n

    def link(self, src, dst, dst_in, src_out=""):
        if not MEL.connect_material_expressions(src, src_out, dst, dst_in):
            raise RuntimeError(f"cannot connect {src.get_name()}:{src_out!r} -> {dst.get_name()}:{dst_in!r}")


def fresh(name):
    path = f"{ROOT}/{name}"
    if EAL.does_asset_exist(path):
        EAL.delete_asset(path)
    return TOOLS.create_asset(name, ROOT, unreal.Material, unreal.MaterialFactoryNew())


def _png(path, rgba, size=4):
    """A tiny flat PNG (8-bit RGBA), written without any imaging library."""
    import struct
    import zlib

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    row = b"\x00" + bytes(rgba) * size
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(row * size)) + chunk(b"IEND", b""))


def default_texture(name, rgba, srgb):
    """A flat default for a texture slot, generated and imported (no binary asset in git)."""
    import os
    folder = os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_saved_dir()), "MatterDefaults")
    os.makedirs(folder, exist_ok=True)
    src = os.path.join(folder, f"{name}.png")
    _png(src, rgba)
    if EAL.does_asset_exist(f"{ROOT}/{name}"):
        EAL.delete_asset(f"{ROOT}/{name}")
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", src)
    task.set_editor_property("destination_path", ROOT)
    task.set_editor_property("destination_name", name)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    TOOLS.import_asset_tasks([task])
    tex = unreal.load_asset(f"{ROOT}/{name}")
    if tex is None:
        raise RuntimeError(f"cannot import {src}")
    tex.set_editor_property("srgb", srgb)
    # uncompressed, so a flat value is exact: UserInterface2D (RGBA8) for colour, the vector
    # displacement format (BGRA8, never sRGB) for data
    tex.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_EDITOR_ICON if srgb
                            else unreal.TextureCompressionSettings.TC_VECTOR_DISPLACEMENTMAP)
    EAL.save_loaded_asset(tex)
    return tex


def texcoord_top_down(g, col):
    """MaterialX st (t up) -> Unreal's texture space (v down): (s, 1 - t)."""
    uv = g.node(unreal.MaterialExpressionTextureCoordinate, col)
    flip = g.op(unreal.MaterialExpressionMultiply, uv,
                g.node(unreal.MaterialExpressionConstant2Vector, col, r=1.0, g=-1.0), col - 1)
    return g.op(unreal.MaterialExpressionAdd, flip,
                g.node(unreal.MaterialExpressionConstant2Vector, col - 1, r=0.0, g=1.0), col - 2)


def texture(g, name, default, sampler, uv, col):
    t = g.node(unreal.MaterialExpressionTextureSampleParameter2D, col, parameter_name=name,
               texture=default, sampler_type=sampler)
    g.link(uv, t, "UVs")
    return t


def build_opaque_core(token, white_srgb):
    """The Opaque core: base_color x base_color_tex x base_color_tint;
    saturate(specular_roughness + roughness_bias)."""
    mat = fresh(f"M_Matter_{token}")
    g = Graph(mat)
    fn = unreal.load_asset(FN_OPAQUE)
    call = g.node(unreal.MaterialExpressionMaterialFunctionCall, 1)
    call.set_material_function(fn)
    inputs = set(MEL.get_material_expression_input_names(call))
    uv = texcoord_top_down(g, 9)

    # base_color_tinted (LCDSchema): the article's colour (a constant, or its texture: the
    # other is left at white) times the Creator tint
    tex = texture(g, "base_color_tex", white_srgb, unreal.MaterialSamplerType.SAMPLERTYPE_COLOR, uv, 5)
    base = g.op(unreal.MaterialExpressionMultiply, g.vector("base_color", (0.8, 0.8, 0.8)), tex, 4, b_out="RGB")
    base = g.op(unreal.MaterialExpressionMultiply, base, g.vector("base_color_tint", (1.0, 1.0, 1.0)), 3)
    g.link(base, call, "base_color")
    # roughness_biased_clamped (LCDSchema): the bias is added, then clamped to 0..1
    rough = g.op(unreal.MaterialExpressionAdd, g.scalar("specular_roughness", 0.3),
                 g.scalar("roughness_bias", 0.0), 3)
    sat = g.node(unreal.MaterialExpressionSaturate, 2)
    g.link(rough, sat, "")
    g.link(sat, call, "specular_roughness")

    missing = []
    for name, default in PASS_THROUGH.items():
        if name not in inputs:
            missing.append(name)
            continue
        p = g.vector(name, default) if isinstance(default, tuple) else g.scalar(name, default)
        g.link(p, call, name)
    if missing:
        raise RuntimeError(f"{token}: Epic's function has no input {missing}")

    outs = list(MEL.get_material_expression_output_names(call))
    front = next(o for o in outs if "front" in o.lower())
    if not MEL.connect_material_property(call, front, unreal.MaterialProperty.MP_FRONT_MATERIAL):
        raise RuntimeError(f"{token}: cannot connect {front!r} to the front material")
    blend, two_sided = SETTINGS[token]
    mat.set_editor_property("blend_mode", {"opaque": unreal.BlendMode.BLEND_OPAQUE}[blend])
    mat.set_editor_property("two_sided", two_sided)
    return mat


def build_sky():
    """The rig's dome as seen: unlit, two-sided (it is seen from inside), constant radiance."""
    mat = fresh("M_Matter_Sky")
    g = Graph(mat)
    mat.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    mat.set_editor_property("two_sided", True)
    rad = g.vector("radiance", (0.503, 0.503, 0.503), col=1)
    if not MEL.connect_material_property(rad, "", unreal.MaterialProperty.MP_EMISSIVE_COLOR):
        raise RuntimeError("Sky: cannot connect the radiance to emissive")
    return mat


def save(mat):
    MEL.recompile_material(mat)
    if not EAL.save_loaded_asset(mat):
        raise RuntimeError(f"cannot save {mat.get_name()}")
    log(f"built {mat.get_name()} scalars={sorted(str(n) for n in MEL.get_scalar_parameter_names(mat))} "
        f"vectors={sorted(str(n) for n in MEL.get_vector_parameter_names(mat))}")


def main():
    white_srgb = default_texture("T_Matter_White_sRGB", (255, 255, 255, 255), srgb=True)
    for mat in (build_opaque_core("Opaque", white_srgb), build_sky()):
        save(mat)
    log("RESULT ok")


main()
