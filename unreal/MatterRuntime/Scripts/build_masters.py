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

Built: the 8 masters (``MASTERS``), all on the Opaque core (6.3: ``place2d``, the per-article
textures, the mask set, three overlays each at its own real-world size, the roughness bias and the
tangent-space normal; coat, fuzz and anisotropy pass straight to Epic's function), each with its
own part (6.4; 6.5: Hair, and the mesh's ``cutout_tex`` on Masked and Hair; Phase09: the mesh's
picture ``base_color_map_tex`` on Opaque, Masked, Hair and Subsurface), and the Sky (the rig's
visible dome, unlit, which the runtime's sky light captures).

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
FN_TRANSLUCENT = "/Engine/Functions/Substrate/MF_Substrate_OpenPBR_Translucent"

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

# Lane-A inputs a master passes through beyond PASS_THROUGH, at OpenPBR's defaults.
EMISSION = {"emission_luminance": 0.0, "emission_color": (1.0, 1.0, 1.0)}
SUBSURFACE = {"subsurface_weight": 0.0, "subsurface_color": (0.8, 0.8, 0.8), "subsurface_radius": 1.0,
              "subsurface_radius_scale": (1.0, 1.0, 1.0), "subsurface_scatter_anisotropy": 0.0}
TRANSMISSION = {"transmission_weight": 0.0, "transmission_color": (1.0, 1.0, 1.0), "transmission_depth": 0.0}
# Inputs the master scales, keeping the article's name and value (D5):
# * an article's lengths are metres (the rig's scene, JOB_FORMAT §Units); Unreal's are cm;
# * emission: Epic's function renders emission_luminance x emission_color at 0.798 of the radiance
#   OpenPBR defines (Storm renders it exactly; the capture reads unlit emission exactly, EXPOSURE_K
#   0.999). Measured 2026-09-29 (6.4) on Neon's dim view, float captures: 0.798 on every region,
#   the same with one call or two and with specular_weight 1 or 0, so it is the function's own.
SCALED = {"subsurface_radius": 100.0, "transmission_depth": 100.0, "emission_luminance": 1.0 / 0.798}

# Each master (MasterSet §Material-settings intent, normative: coverage, two-sided, refraction):
#   calls    2 = Epic's function at metalness 0 and 1, mixed by the article's metalness
#            (OpenPBR's linear metal mix, 6.3), on the masters that carry metal; 1 on the ones
#            whose articles are dielectric by definition (Epic's single call is exact at metalness
#            0), which also keeps their Substrate bytes down
#   thin     geometry_thin_walled, a property of the master (its settings row), not a parameter
#   base_map the mesh's picture, base_color_map_tex (LCDSchema §Base colour map, Phase09 RD-P09-1),
#            on the masters whose author tier carries it
MASTERS = {
    "Opaque":           dict(fn=FN_OPAQUE, calls=2, blend="opaque", two_sided=False, base_map=True),
    "TwoLayer":         dict(fn=FN_OPAQUE, calls=2, blend="opaque", two_sided=False, layer2=True),
    "Masked":           dict(fn=FN_OPAQUE, calls=2, blend="masked", two_sided=True, opacity=True, base_map=True),
    # Hair (Phase06 D12, 6.5): matte on cards, default lit (not Unreal's hair shading model, which
    # reads a flat card as one glossy sheet); the cut-out as soft coverage, dithered; the light
    # through the card folded into its colour (build_master's hair part). Dielectric: one call.
    "Hair":             dict(fn=FN_OPAQUE, calls=1, blend="masked", two_sided=True, hair=True, base_map=True),
    "Emissive":         dict(fn=FN_OPAQUE, calls=2, blend="opaque", two_sided=False, extra=EMISSION),
    "Subsurface":       dict(fn=FN_OPAQUE, calls=1, blend="opaque", two_sided=False, extra=SUBSURFACE,
                             base_map=True),
    "TranslucentThin":  dict(fn=FN_TRANSLUCENT, calls=1, blend="translucent", two_sided=True,
                             extra=TRANSMISSION, thin=True),
    "TranslucentThick": dict(fn=FN_TRANSLUCENT, calls=1, blend="translucent", two_sided=True,
                             extra=TRANSMISSION, thin=False),
}

SUBSURFACE_FLOOR = 1e-4     # the scattered colour's floor (sRGB ~0.3/255: invisible)

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


def bayer4(g, col):
    """This pixel's 4x4 ordered-dither threshold, (k + 0.5) / 16, each k in 0..15 once per 4x4
    tile of pixels. The driver supersamples 4x and box-filters each 4x4 block (drivers/unreal.py
    SUPERSAMPLE), and the tiles align with the blocks, so a coverage c keeps round-ish(16 c) of a
    block's 16 samples: soft coverage to 1/16 in the rig's picture, with no noise.
    k = 4 M2(x mod 2, y mod 2) + M2(floor(x / 2) mod 2, floor(y / 2) mod 2), M2 = [[0, 2], [3, 1]]
    (M2(a, b) = 2 |a - b| + b), which is a bijection of the four bits onto 0..15."""
    M = unreal
    px = g.node(M.MaterialExpressionScreenPosition, col)
    two = g.node(M.MaterialExpressionConstant, col - 2, r=2.0)

    def bits(axis):
        p = g.one(M.MaterialExpressionFloor, g.mask(px, axis, col - 1, "PixelPosition"), col - 2)
        lo = g.op(M.MaterialExpressionFmod, p, two, col - 3)
        hi = g.op(M.MaterialExpressionFmod,
                  g.one(M.MaterialExpressionFloor, g.op_k(M.MaterialExpressionMultiply, p, 0.5, col - 3), col - 4),
                  two, col - 5)
        return lo, hi

    def m2(a, b):
        d = g.one(M.MaterialExpressionAbs, g.op(M.MaterialExpressionSubtract, a, b, col - 6), col - 7)
        return g.op(M.MaterialExpressionAdd, g.op_k(M.MaterialExpressionMultiply, d, 2.0, col - 8), b, col - 9)

    (x0, x1), (y0, y1) = bits("r"), bits("g")
    k = g.op(M.MaterialExpressionAdd, g.op_k(M.MaterialExpressionMultiply, m2(x0, y0), 4.0, col - 10),
             m2(x1, y1), col - 11)
    return g.op_k(M.MaterialExpressionMultiply, g.op_k(M.MaterialExpressionAdd, k, 0.5, col - 12), 1.0 / 16.0, col - 13)


def texture(g, name, default, uv, col):
    t = g.node(unreal.MaterialExpressionTextureSampleParameter2D, col, parameter_name=name, texture=default,
               sampler_type=unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
    g.link(uv, t, "UVs")
    return t


def build_master(token, white, no_wear, flat):
    """One master: Epic's function plus the core network (``MASTERS`` says what each adds —
    TwoLayer's second layer mixed in by the maskset's R before the tint, Masked's alpha test,
    the pass-through inputs, the coverage), MaterialX's formulas as in
    ``blender/masters/build_masters.py`` ``_build``:

    * base_color_tinted: base_color x base_color_tex x base_color_map_tex x base_color_tint (the
      article sets one of the first two to its value and leaves the other white; the third is the
      mesh's picture, on the mesh's own st, where the master has it: Phase09 RD-P09-1);
    * roughness: specular_roughness x roughness_tex, + each overlay's B x effect, then
      roughness_biased_clamped = saturate(+ roughness_bias);
    * metalness: base_metalness x metalness_tex, the Mix of the two calls (metalness 0 and 1);
    * the normal, in TANGENT space: normal_tex x 2 - 1, + each overlay's (RG x 2 - 1, 0) x effect,
      normalised ONCE (MasterSet, since 5.3);
    * an overlay's effect = overlayN_density x overlay.A x gate, gate = mix(1, maskset[G|B|A],
      maskset_blend) (MasterSet §Overlay semantic, §MaskSet).
    """
    M = unreal
    spec = MASTERS[token]
    layer2 = spec.get("layer2", False)
    mat = fresh(f"M_Matter_{token}")
    g = Graph(mat)
    fn = unreal.load_asset(spec["fn"])
    # OpenPBR's base is a LINEAR mix of the dielectric and metal lobes by metalness. Epic's
    # function mixes them by blending parameters (its "Is Metal?" mix), which reads 0 < metalness
    # < 1 wrong (Copper's floor x1.16 / x1.31). So: two calls, metalness 0 (dielectric) and 1
    # (metal), every other input the same, mixed per pixel by our own horizontal mix with
    # parameter blending off (Phase06 6.3, the lead's ruling "c then b"). It needs Substrate's
    # 160-byte budget (Config/DefaultEngine.ini), or the compiler flattens each coat to fit.
    calls = []
    for col in range(1, spec["calls"] + 1):
        c = g.node(M.MaterialExpressionMaterialFunctionCall, col)
        c.set_material_function(fn)
        calls.append(c)
    inputs = set(MEL.get_material_expression_input_names(calls[0]))

    def feed(src, name, src_out=""):
        for c in calls:
            g.link(src, c, name, src_out)

    placed = place2d(g, 22)
    uv = image_uv(g, placed, 15)
    maskset = texture(g, "maskset_tex", white, image_uv(g, placed, 15, "maskset"), 12)
    blend = g.scalar("maskset_blend", 0.0, col=10)

    def layer(names, defaults):
        """One layer's base colour, roughness, metalness and tangent-space normal: each the
        article's constant x its texture (the article sets one and leaves the other neutral).
        Where the article has no normal map the rig's driver sets an exact flat normal (this
        8-bit default's 128 reads 0.502, a 0.2 degree tilt)."""
        (b_name, r_name, m_name, prefix), (b_def, r_def, m_def) = names, defaults
        b = g.op(M.MaterialExpressionMultiply, g.vector(b_name, b_def),
                 texture(g, f"{prefix}base_color_tex", white, uv, 12), 11, b_out="RGB")
        r = g.op(M.MaterialExpressionMultiply, g.scalar(r_name, r_def),
                 texture(g, f"{prefix}roughness_tex", white, uv, 12), 11, b_out="R")
        m = g.op(M.MaterialExpressionMultiply, g.scalar(m_name, m_def),
                 texture(g, f"{prefix}metalness_tex", white, uv, 12), 11, b_out="R")
        n = g.op_k(M.MaterialExpressionSubtract,
                   g.op_k(M.MaterialExpressionMultiply, texture(g, f"{prefix}normal_tex", flat, uv, 12), 2.0, 11, "RGB"),
                   1.0, 10)
        return b, r, m, n

    base, rough, metal, n_ts = layer(("base_color", "specular_roughness", "base_metalness", ""),
                                     ((0.8, 0.8, 0.8), 0.3, 0.0))
    if layer2:
        # MasterSet §TwoLayer blend: t = saturate((maskset.R - balance) / max(1 - contrast, 1e-4)
        # + 0.5) x maskset_blend; each of layer 1's four values mixes to layer 2's by t, the
        # mixed normal normalised (then the overlays add to it, normalised once more below).
        # Layer 2's defaults are Blender's (ML_TwoLayer).
        b2, r2, m2, n2 = layer(("layer2_base_color", "layer2_roughness", "layer2_metalness", "layer2_"),
                               ((0.5, 0.5, 0.5), 0.5, 0.0))
        inv = g.node(M.MaterialExpressionSubtract, 10, const_a=1.0)
        g.link(g.scalar("layer_blend_contrast", 0.0, col=11), inv, "B")
        safe = g.op_k(M.MaterialExpressionMax, inv, 1e-4, 9)
        cen = g.op(M.MaterialExpressionSubtract, maskset, g.scalar("layer_blend_balance", 0.5, col=11), 9, a_out="R")
        k = g.one(M.MaterialExpressionSaturate,
                  g.op_k(M.MaterialExpressionAdd, g.op(M.MaterialExpressionDivide, cen, safe, 8), 0.5, 7), 6)
        t = g.op(M.MaterialExpressionMultiply, k, blend, 5)

        def mix(a, b):
            n = g.node(M.MaterialExpressionLinearInterpolate, 4)
            g.link(a, n, "A")
            g.link(b, n, "B")
            g.link(t, n, "Alpha")
            return n
        base, rough, metal = mix(base, b2), mix(rough, r2), mix(metal, m2)
        n_ts = g.one(M.MaterialExpressionNormalize, mix(n_ts, n2), 3)

    # The mesh's own st, NOT the article's placement: the atlas a mesh-supplied map is drawn on
    # (the cut-out, the picture), so a Creator's UV nudge never moves it.
    own_st = (image_uv(g, g.node(M.MaterialExpressionTextureCoordinate, 16), 15)
              if spec.get("base_map") or spec.get("opacity") or spec.get("hair") else None)
    base_map = None
    if spec.get("base_map"):
        # The mesh's picture (LCDSchema §Base colour map, Phase09 RD-P09-1), supplied per binding:
        # base = base_color_const x base_color_map x base_color_tint; white when none is bound.
        base_map = texture(g, "base_color_map_tex", white, own_st, 12)
        base = g.op(M.MaterialExpressionMultiply, base, base_map, 10, b_out="RGB")
    base = g.op(M.MaterialExpressionMultiply, base, g.vector("base_color_tint", (1.0, 1.0, 1.0)), 10)
    if spec.get("hair"):
        # The Hair row's light through the card, OpenPBR thin-walled subsurface with its colour c the
        # tinted base (MaterialX: a reflected lobe c.c(1 - a)/2 and a transmitted one c.c(1 + a)/2,
        # mixed in by the weight w). Under even light the two sum to mix(c, c.c, w), the anisotropy
        # cancelling, and that is the card's colour here, matte and default lit (D12). Substrate's
        # own thin-surface subsurface was tried first and rejected (6.5): in one real-time capture
        # it draws the card as dark, noisy pixels, solid card or cut. Measured on the character
        # against Storm, hair dE 4.3 (the plain base 7.4); ~20 % bright, because Storm's rear lobe
        # sees only the dome, not the sun.
        w = g.scalar("subsurface_weight", 0.0, col=11)
        base = g.op(M.MaterialExpressionLinearInterpolate, base,
                    g.op(M.MaterialExpressionMultiply, base, base, 10), 9)
        g.link(w, base, "Alpha")
    feed(base, "base_color")
    if len(calls) == 2:
        for c, m in zip(calls, (0.0, 1.0)):
            g.link(g.node(M.MaterialExpressionConstant, 2, r=m), c, "base_metalness")
    else:
        feed(metal, "base_metalness")

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
    feed(g.one(M.MaterialExpressionSaturate, rough, 2), "specular_roughness")
    normal = g.one(M.MaterialExpressionNormalize, n_ts, 3)
    if NORMAL_SPACE == "world":
        normal = g.one(M.MaterialExpressionTransform, normal, 2,
                       transform_source_type=M.MaterialVectorCoordTransformSource.TRANSFORMSOURCE_TANGENT,
                       transform_type=M.MaterialVectorCoordTransform.TRANSFORM_WORLD)
    feed(normal, "geometry_normal")

    missing = []
    for name, default in {**PASS_THROUGH, **spec.get("extra", {})}.items():
        if name not in inputs:
            missing.append(name)
            continue
        p = g.vector(name, default) if isinstance(default, tuple) else g.scalar(name, default)
        if name in SCALED:
            p = g.op_k(M.MaterialExpressionMultiply, p, SCALED[name], 5)
        if name == "subsurface_color" and base_map is not None:
            # Phase09 F-P09-5: an article taking the picture scatters the PICTURE's colour (its
            # subsurface_color is connected to base_color_out), or the picture keeps only
            # 1 - subsurface_weight of its strength (the white Unreal eye of 9.2). The driver sets
            # this parameter to the article's base constant then; with no picture bound it is x 1.
            p = g.op(M.MaterialExpressionMultiply, p, base_map, 5, b_out="RGB")
            # A black texel (the eye picture's pupil) would scatter a colour of exactly 0, which
            # HANGS THE GPU (learning U11: Xid 109 in SubsurfaceScattering, 9.3; the floor alone
            # cleared it, the job otherwise identical)
            p = g.op_k(M.MaterialExpressionMax, p, SUBSURFACE_FLOOR, 4)
        feed(p, name)
    if missing:
        raise RuntimeError(f"{token}: Epic's function has no input {missing}")
    if "thin" in spec:
        feed(g.node(M.MaterialExpressionConstant, 2, r=1.0 if spec["thin"] else 0.0), "geometry_thin_walled")

    outs = [str(o) for o in MEL.get_material_expression_output_names(calls[0])]
    front = next(o for o in outs if "front" in o.lower())
    if spec.get("opacity") or spec.get("hair"):
        # The mesh's cut-out map (LCDSchema §Cut-out map, supplied per binding), on the mesh's own
        # st; white, so a card, when none is bound.
        cov =g.op(M.MaterialExpressionMultiply, g.scalar("geometry_opacity", 1.0),
                   texture(g, "cutout_tex", white, own_st, 12), 11, b_out="R")
    if spec.get("opacity"):
        # Masked (MasterSet: alpha-tested at the cutoff): coverage = geometry_opacity x
        # opacity_tex x cutout_tex, through Epic's function; kept where coverage >=
        # opacity_cutoff, which a fixed clip of 0.5 does on (coverage - cutoff + 0.5).
        cov = g.op(M.MaterialExpressionMultiply, cov, texture(g, "opacity_tex", white, uv, 12), 10, b_out="R")
        feed(cov, "geometry_opacity")
        clip = g.op_k(M.MaterialExpressionAdd,
                      g.op(M.MaterialExpressionSubtract, calls[0], g.scalar("opacity_cutoff", 0.5, col=3), 2,
                           a_out="OpacityMask"), 0.5, 1)
    elif spec.get("hair"):
        # Hair (MasterSet: masked, DITHERED): the coverage is soft, never thresholded at a cutoff,
        # so each pixel keeps it against its own ordered-dither threshold. It is not fed to Epic's
        # function, whose weight would scale the kept pixels by it a second time.
        clip = g.op_k(M.MaterialExpressionAdd, g.op(M.MaterialExpressionSubtract, cov, bayer4(g, 10), 2), 0.5, 1)
    if spec.get("opacity") or spec.get("hair"):
        if not MEL.connect_material_property(clip, "", unreal.MaterialProperty.MP_OPACITY_MASK):
            raise RuntimeError(f"{token}: cannot connect the opacity mask")
        mat.set_editor_property("opacity_mask_clip_value", 0.5)
    if len(calls) == 2:
        top = g.node(M.MaterialExpressionSubstrateHorizontalMixing, 0)
        top.set_editor_property("use_parameter_blending", False)
        g.link(calls[0], top, "Background", front)
        g.link(calls[1], top, "Foreground", front)
        g.link(metal, top, "Mix")
        top_out = ""
    else:
        top, top_out = calls[0], front
    if not MEL.connect_material_property(top, top_out, unreal.MaterialProperty.MP_FRONT_MATERIAL):
        raise RuntimeError(f"{token}: cannot connect the front material")
    if spec["blend"] == "translucent":
        # refraction by the index of refraction (MasterSet: TranslucentThin / Thick)
        ior = next(o for o in outs if "refraction" in o.lower())
        if not MEL.connect_material_property(calls[0], ior, unreal.MaterialProperty.MP_REFRACTION):
            raise RuntimeError(f"{token}: cannot connect the refraction")
        mat.set_editor_property("refraction_method", unreal.RefractionMode.RM_INDEX_OF_REFRACTION)
        # lit per pixel, forward: the default translucency lighting is volumetric and carries no
        # specular, so glass only darkened what is behind it (6.4: no dome reflection, no glints)
        mat.set_editor_property("translucency_lighting_mode",
                                unreal.TranslucencyLightingMode.TLM_SURFACE_PER_PIXEL_LIGHTING)
    mat.set_editor_property("blend_mode", {
        "opaque": unreal.BlendMode.BLEND_OPAQUE, "masked": unreal.BlendMode.BLEND_MASKED,
        # Substrate's translucency with coloured transmittance: green glass filters what is behind
        "translucent": unreal.BlendMode.BLEND_TRANSLUCENT_COLORED_TRANSMITTANCE}[spec["blend"]])
    mat.set_editor_property("two_sided", spec["two_sided"])
    if spec.get("thin"):
        mat.set_editor_property("is_thin_surface", True)
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
    for mat in [build_master(t, white, no_wear, flat) for t in MASTERS] + [build_sky()]:
        save(mat)
    log("RESULT ok")


main()
