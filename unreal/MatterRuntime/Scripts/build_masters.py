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

Built so far: the Opaque core in full (6.3: ``place2d``, the per-article textures, the mask set,
three overlays each at its own real-world size, the roughness bias and the tangent-space normal;
coat, fuzz and anisotropy pass straight to Epic's function) and the Sky (the rig's visible
dome, unlit, which the runtime's sky light captures).

Every texture slot samples as **LinearColor**: the runtime hands every texture over as linear
float, decoding a colour texture's sRGB itself, so no slot's colour flag can mismatch
(``MatterRuntimeGameMode::LoadTexture``). The slots' defaults are neutral: white, and an
overlay's alpha 0 (no wear).
"""

import unreal

MEL = unreal.MaterialEditingLibrary
EAL = unreal.EditorAssetLibrary
TOOLS = unreal.AssetToolsHelpers.get_asset_tools()
ROOT = "/Game/Masters"
FN_OPAQUE = "/Engine/Functions/Substrate/MF_Substrate_OpenPBR_Opaque"

# OpenPBR's defaults (MaterialX open_pbr_surface) for the lane-A inputs a master passes straight
# through to Epic's function, under their own names. The network's inputs (base colour,
# roughness, metalness, the normal) are wired by the network, not here. The tangent and the
# coat normal stay unwired: the mesh's tangent is dP/ds, OpenPBR's default Tworld, and the coat
# keeps the geometry's normal, as OpenPBR's geometry_coat_normal defaults to it.
PASS_THROUGH = {
    "base_weight": 1.0, "base_diffuse_roughness": 0.0,
    "specular_weight": 1.0, "specular_color": (1.0, 1.0, 1.0), "specular_ior": 1.5,
    "specular_roughness_anisotropy": 0.0,
    "coat_weight": 0.0, "coat_color": (1.0, 1.0, 1.0), "coat_roughness": 0.0, "coat_ior": 1.6,
    "fuzz_weight": 0.0, "fuzz_color": (1.0, 1.0, 1.0), "fuzz_roughness": 0.5,
}

# MasterSet §Material-settings intent (normative): coverage, shading model, two-sided.
SETTINGS = {
    "Opaque": ("opaque", False),
}

OVERLAYS = (1, 2, 3)
GATE_CHANNEL = {1: "G", 2: "B", 3: "A"}     # MasterSet §MaskSet channel contract

# The space Epic's function reads ``geometry_normal`` in. Substrate's slab takes the material's
# normal basis, which is tangent space (the material's default), so the combined tangent-space
# normal is wired straight in. "world" inserts a Tangent -> World transform instead. The check
# that tells them apart: the grey card, which carries a flat normal, must stay at its 6.1
# agreement with Storm (a world-space reading of (0, 0, 1) would light every face as the top).
NORMAL_SPACE = "tangent"


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

    def op_k(self, cls, a, k, col, a_out=""):
        """a <op> a constant (the node's own ConstB)."""
        n = self.node(cls, col, const_b=float(k))
        self.link(a, n, "A", a_out)
        return n

    def one(self, cls, src, col, src_out="", **props):
        """A one-input node (saturate, normalize, sine, a component mask …). The input is not
        called ``a``: a component mask's own properties are r, g, b and a."""
        n = self.node(cls, col, **props)
        self.link(src, n, "", src_out)
        return n

    def mask(self, a, channels, col, a_out=""):
        return self.one(unreal.MaterialExpressionComponentMask, a, col, a_out,
                        **{c: c in channels for c in "rgba"})

    def lerp_from_one(self, b, alpha, col, b_out=""):
        """mix(1, b, alpha): MaterialX's mix(bg=1, fg=b, mix=alpha)."""
        n = self.node(unreal.MaterialExpressionLinearInterpolate, col, const_a=1.0)
        self.link(b, n, "B", b_out)
        self.link(alpha, n, "Alpha")
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


def default_texture(name, rgba, srgb=False):
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


def place2d(g, col):
    """MaterialX ``ND_place2d_vector2`` at its defaults (pivot 0, operation order 0), on the
    mesh's st (t up): ``uv / scale``, then ``rotate2d`` (MaterialX's mx_rotate_vector2 turns the
    COORDINATE clockwise by ``uv_rotation`` degrees: (c x + s y, -s x + c y)), then ``- offset``.
    The same formula as Blender's ML_Place2D (build_masters.py)."""
    M = unreal
    st = g.node(M.MaterialExpressionTextureCoordinate, col)
    scale = g.mask(g.vector("uv_scale", (1.0, 1.0, 1.0), col=col), "rg", col - 1)
    q = g.op(M.MaterialExpressionDivide, st, scale, col - 1)
    x, y = g.mask(q, "r", col - 2), g.mask(q, "g", col - 2)
    deg = g.scalar("uv_rotation", 0.0, col=col - 1)
    s = g.one(M.MaterialExpressionSine, deg, col - 2, period=360.0)       # period 360: degrees
    c = g.one(M.MaterialExpressionCosine, deg, col - 2, period=360.0)
    u = g.op(M.MaterialExpressionAdd, g.op(M.MaterialExpressionMultiply, c, x, col - 3),
             g.op(M.MaterialExpressionMultiply, s, y, col - 3), col - 4)
    v = g.op(M.MaterialExpressionSubtract, g.op(M.MaterialExpressionMultiply, c, y, col - 3),
             g.op(M.MaterialExpressionMultiply, s, x, col - 3), col - 4)
    rot = g.op(M.MaterialExpressionAppendVector, u, v, col - 5)
    off = g.mask(g.vector("uv_offset", (0.0, 0.0, 0.0), col=col - 4), "rg", col - 5)
    return g.op(M.MaterialExpressionSubtract, rot, off, col - 6)


def image_uv(g, placed, col, layer=None):
    """The placed st -> Unreal's texture space (v down): (s, 1 - t). A tiled layer (MaterialX
    NG_tiledimage: st / realworldimagesize * realworldtilesize) first multiplies by its own
    ``<layer>_layer_scale`` (the article's tile / image size)."""
    M = unreal
    if layer:
        placed = g.op(M.MaterialExpressionMultiply, placed, g.scalar(f"{layer}_layer_scale", 1.0, col=col), col)
    flip = g.op(M.MaterialExpressionMultiply, placed,
                g.node(M.MaterialExpressionConstant2Vector, col, r=1.0, g=-1.0), col - 1)
    return g.op(M.MaterialExpressionAdd, flip,
                g.node(M.MaterialExpressionConstant2Vector, col - 1, r=0.0, g=1.0), col - 2)


def texture(g, name, default, uv, col):
    t = g.node(unreal.MaterialExpressionTextureSampleParameter2D, col, parameter_name=name, texture=default,
               sampler_type=unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
    g.link(uv, t, "UVs")
    return t


def build_opaque_core(token, white, no_wear, flat):
    """The Opaque core, MaterialX's formulas as in ``blender/masters/build_masters.py`` ``_build``:

    * base_color_tinted: base_color x base_color_tex x base_color_tint (the article sets one of
      the two to its value and leaves the other white);
    * roughness: specular_roughness x roughness_tex, + each overlay's B x effect, then
      roughness_biased_clamped = saturate(+ roughness_bias);
    * metalness: base_metalness x metalness_tex;
    * the normal, in TANGENT space: normal_tex x 2 - 1, + each overlay's (RG x 2 - 1, 0) x effect,
      normalised ONCE (MasterSet, since 5.3);
    * an overlay's effect = overlayN_density x overlay.A x gate, gate = mix(1, maskset[G|B|A],
      maskset_blend) (MasterSet §Overlay semantic, §MaskSet).
    """
    M = unreal
    mat = fresh(f"M_Matter_{token}")
    g = Graph(mat)
    fn = unreal.load_asset(FN_OPAQUE)
    call = g.node(M.MaterialExpressionMaterialFunctionCall, 1)
    call.set_material_function(fn)
    inputs = set(MEL.get_material_expression_input_names(call))
    placed = place2d(g, 22)
    uv = image_uv(g, placed, 15)

    base = g.op(M.MaterialExpressionMultiply, g.vector("base_color", (0.8, 0.8, 0.8)),
                texture(g, "base_color_tex", white, uv, 12), 11, b_out="RGB")
    base = g.op(M.MaterialExpressionMultiply, base, g.vector("base_color_tint", (1.0, 1.0, 1.0)), 10)
    g.link(base, call, "base_color")
    metal = g.op(M.MaterialExpressionMultiply, g.scalar("base_metalness", 0.0),
                 texture(g, "metalness_tex", white, uv, 12), 11, b_out="R")
    g.link(metal, call, "base_metalness")
    rough = g.op(M.MaterialExpressionMultiply, g.scalar("specular_roughness", 0.3),
                 texture(g, "roughness_tex", white, uv, 12), 11, b_out="R")
    # the article's normal map; where the article has none the rig's driver sets an exact flat
    # normal (this 8-bit default's 128 reads 0.502, a 0.2 degree tilt)
    n_ts = g.op_k(M.MaterialExpressionSubtract,
                  g.op_k(M.MaterialExpressionMultiply, texture(g, "normal_tex", flat, uv, 12), 2.0, 11, "RGB"),
                  1.0, 10)

    maskset = texture(g, "maskset_tex", white, image_uv(g, placed, 15, "maskset"), 12)
    blend = g.scalar("maskset_blend", 0.0, col=10)
    for n in OVERLAYS:
        ov = texture(g, f"overlay{n}_tex", no_wear, image_uv(g, placed, 15, f"overlay{n}"), 12)
        gate = g.lerp_from_one(maskset, blend, 9, b_out=GATE_CHANNEL[n])
        eff = g.op(M.MaterialExpressionMultiply, g.scalar(f"overlay{n}_density", 0.0, col=10), ov, 9, b_out="A")
        eff = g.op(M.MaterialExpressionMultiply, eff, gate, 8)
        rough = g.op(M.MaterialExpressionAdd, rough,
                     g.op(M.MaterialExpressionMultiply, ov, eff, 7, a_out="B"), 6)
        rg = g.op_k(M.MaterialExpressionSubtract,
                    g.op_k(M.MaterialExpressionMultiply, g.mask(ov, "rg", 10, "RGBA"), 2.0, 9), 1.0, 8)
        delta = g.op(M.MaterialExpressionAppendVector, rg, g.node(M.MaterialExpressionConstant, 8, r=0.0), 7)
        n_ts = g.op(M.MaterialExpressionAdd, n_ts, g.op(M.MaterialExpressionMultiply, delta, eff, 6), 5)

    # roughness_biased_clamped (LCDSchema): the bias is added, then clamped to 0..1
    rough = g.op(M.MaterialExpressionAdd, rough, g.scalar("roughness_bias", 0.0, col=4), 3)
    g.link(g.one(M.MaterialExpressionSaturate, rough, 2), call, "specular_roughness")
    normal = g.one(M.MaterialExpressionNormalize, n_ts, 3)
    if NORMAL_SPACE == "world":
        normal = g.one(M.MaterialExpressionTransform, normal, 2,
                       transform_source_type=M.MaterialVectorCoordTransformSource.TRANSFORMSOURCE_TANGENT,
                       transform_type=M.MaterialVectorCoordTransform.TRANSFORM_WORLD)
    g.link(normal, call, "geometry_normal")

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
    white = default_texture("T_Matter_White", (255, 255, 255, 255))
    no_wear = default_texture("T_Matter_NoWear", (128, 128, 0, 0))     # an overlay at alpha 0
    flat = default_texture("T_Matter_FlatNormal", (128, 128, 255, 255))
    for mat in (build_opaque_core("Opaque", white, no_wear, flat), build_sky()):
        save(mat)
    log("RESULT ok")


main()
