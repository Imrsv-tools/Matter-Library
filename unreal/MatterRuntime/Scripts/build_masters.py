"""The Matter Library's Unreal masters, built by script (Phase06; no binary asset is committed).

Run as a commandlet (no GPU; unreal/build.sh does it):

  UnrealEditor-Cmd MatterRuntime.uproject -run=pythonscript -script=<this> \
      -EnablePlugins=PythonScriptPlugin,EditorScriptingUtilities -unattended -nullrhi

Each master is Epic's Substrate OpenPBR function (``MF_Substrate_OpenPBR_{Opaque,Translucent}``,
engine content, UR-F4) plus our network around it (Phase06 D6), but for Opaque, whose BSDF is built
from Substrate's own nodes with ONE coat (``one_coat_front``, Phase30 D-P30-1); a port of
``blender/masters/build_masters.py``'s ``_build``; the formulas are MaterialX's, and that file
names each one's source. Parameter names are the article's (D5): OpenPBR's for lane A, the frozen
Creator ports, and the author-tier names. Every master is deleted and rebuilt, so the output
depends only on this script and the engine.

Built: the 8 masters (``MASTERS``), all on the Opaque core (6.3: ``place2d``, the per-article
textures, the mask set, three overlays each at its own real-world size, the roughness bias and the
tangent-space normal; coat, fuzz and anisotropy pass straight to Epic's function, or to Opaque's
slabs, but for the coat's
darkening of the base, which is MaterialX's own), each with its
own part (6.4; 6.5: Hair, and the mesh's ``cutout_tex`` on Masked and Hair; Phase09: the mesh's
picture ``base_color_map_tex`` on Opaque, Masked, Hair and Subsurface), and the Sky (the rig's
visible dome, unlit, which the runtime's sky light captures). Phase29: every master dissolves an
object part-present by its ``object_fade`` (Custom Primitive Data slot 0; ``fade_terms``), and the
four solid masters each get a masked instance, ``MI_Matter_<Token>_Fading`` (``build_fading``).
29.3: the dissolve's threshold is a blue-noise tile the build generates, ``T_Matter_FadeNoise``
(``fade_threshold``), shifted every frame on a view that averages over time.

By default every texture slot samples as **LinearColor**: the runtime hands every texture over as
linear float, decoding a colour texture's sRGB itself, so no slot's colour flag can mismatch
(``MatterRuntimeGameMode::LoadTexture``). The colour and normal switches below change that for a
runtime that binds compressed textures. The slots' defaults are neutral: white, and an overlay's
alpha 0 (no wear).

A second project (PlatformDependencies M7, P20) tells the build what it is building for, by
environment variable. Unset, every one leaves the build exactly the library's own runtime's:

  MATTER_MASTERS_ROOT=<package path>    where the masters and the default textures are written:
                                        /Game/<path>, or a plugin's content mount point
                                        (default /Game/Masters)
  MATTER_MASTERS_SKINNED=1              the masters also draw on a skinned mesh with morph
                                        targets (a character). Without the usages a packaged run
                                        draws Unreal's default material there, reporting nothing
  MATTER_MASTERS_INSTANCED=1            the masters also draw on an instanced static mesh (one
                                        mesh drawn many times, as a USD prototype is). Without the
                                        usage a packaged run draws Unreal's default material there
  MATTER_MASTERS_MESH_V=unreal          the meshes' UVs are Unreal's (v = 1 - t, as its importers
                                        leave them), not USD's st (default st)
  MATTER_MASTERS_MESH_BINORMAL=unreal   the meshes' binormal runs along +v, as Unreal builds it
                                        from such UVs, not along +t (default st)
  MATTER_MASTERS_SKY=0                  leave out M_Matter_Sky, which is the rig's dome, not a master

Those five were run in a second project on Unreal 5.8 and looked at there (2026-10-05): all eight
masters compile with them, on a skinned mesh too, and a bump reads as a bump. With nothing set the
script was run in the library's own project the same day: its "built ..." lines are those of the
build before the switches, byte for byte. MATTER_MASTERS_INSTANCED came later (2026-10-10) and
sets one usage only, as the skinned switch does.

Two more are for a runtime that binds the release's block-compressed .dds (BC7 sRGB colour, BC5
normals) instead of decoding the PNGs itself (IMRSV_Platform #249):

  MATTER_MASTERS_COLOUR_SAMPLER=srgb    the colour slots sample an sRGB texture (a block-compressed
                                        colour picture carries its decode in its own flag, which a
                                        linear sampler refuses). Default linear
  MATTER_MASTERS_NORMAL_SAMPLER=normal  the normal slots (normal_tex, layer2_normal_tex,
                                        normal_map_tex) sample a normal map: the engine rebuilds Z
                                        from R and G (BC5 carries two channels; Y is not flipped),
                                        and the graph's own x 2 - 1 goes. Their default is a flat
                                        normal-map texture. Default linear

And one keeps the build that came before, to compare against:

  MATTER_MASTERS_REFRACTION=function    the Refraction input takes the output of Epic's function,
                                        which bends nothing on either see-through master (M6).
                                        Default index: the article's index on the solid master
                                        and 1.0 on the thin one. The default since 2026-10-16:
                                        in the rig's side view the solid master then bends the
                                        wall behind it, and the thin master's pictures are the
                                        same to the pixel (research 261016_R_UnrealMachineAsks)
"""

import os

import unreal


def _told(name, default, allowed=None):
    """What the build is told by one environment variable. A value it does not know stops the
    build: a mistyped switch must not build the default and report success."""
    value = os.environ.get(name, "").strip() or default
    if allowed is not None and value not in allowed:
        raise RuntimeError(f"{name}={value!r}: want one of {sorted(allowed)}")
    return value


MEL = unreal.MaterialEditingLibrary
EAL = unreal.EditorAssetLibrary
TOOLS = unreal.AssetToolsHelpers.get_asset_tools()
ROOT = _told("MATTER_MASTERS_ROOT", "/Game/Masters")
if not ROOT.startswith("/") or ROOT.endswith("/"):
    raise RuntimeError(f"MATTER_MASTERS_ROOT={ROOT!r}: want a package path such as /Game/Masters")
SKINNED = _told("MATTER_MASTERS_SKINNED", "0", {"0", "1"}) == "1"
INSTANCED = _told("MATTER_MASTERS_INSTANCED", "0", {"0", "1"}) == "1"
MESH_V = _told("MATTER_MASTERS_MESH_V", "st", {"st", "unreal"})
MESH_BINORMAL = _told("MATTER_MASTERS_MESH_BINORMAL", "st", {"st", "unreal"})
SKY = _told("MATTER_MASTERS_SKY", "1", {"0", "1"}) == "1"
COLOUR_SAMPLER = _told("MATTER_MASTERS_COLOUR_SAMPLER", "linear", {"linear", "srgb"})
NORMAL_SAMPLER = _told("MATTER_MASTERS_NORMAL_SAMPLER", "linear", {"linear", "normal"})
REFRACTION = _told("MATTER_MASTERS_REFRACTION", "index", {"function", "index"})
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
# * emission is not here: the master gives Epic's function emission_luminance x the LENGTH of
#   emission_color (build_master, "the light"). It was x 1 / 0.798 until 2026-10-11, a constant
#   measured 2026-09-29 (6.4) on Neon's dim view and read as the function's own scale; it is
#   1 / the length of Neon's magenta, and was wrong for every other colour.
SCALED = {"subsurface_radius": 100.0, "transmission_depth": 100.0}
SCATTER_GAIN = 4.0   # Phase22 RD-P22-18: radius x (1 + 4 x scatter_map), as the assembler's

# Each master (MasterSet §Material-settings intent, normative: coverage, two-sided, refraction):
#   calls    0 = no call of Epic's function: Substrate's own slabs, one coat over a linear mix of a
#            dielectric and a metal slab (one_coat_front, Phase30); 2 = Epic's function at
#            metalness 0 and 1, mixed by the article's metalness (OpenPBR's linear metal mix, 6.3),
#            on the other masters that carry metal: two coats a pixel, which needs the 160-byte
#            budget (Learnings Unreal U3); 1 on the ones whose articles are dielectric by
#            definition (Epic's single call is exact at metalness 0), which also keeps their
#            Substrate bytes down
#   thin     geometry_thin_walled, a property of the master (its settings row), not a parameter
#   base_map the mesh's picture, base_color_map_tex (LCDSchema §Base colour map, Phase09 RD-P09-1),
#            on the masters whose author tier carries it
#   shine    the mesh's shine maps (LCDSchema §Shine maps, Phase22): roughness_map_tex, an offset
#            around 0.5 added before the bias; a grey default (128) for a binding that has none.
#            22.2: normal_map_tex (tangent space, its XY added before the overlays; flat default)
#            and cavity_map_tex (x specular_weight; white default). 22.3: scatter_map_tex
#            (subsurface_radius x (1 + SCATTER_GAIN x map); black default)
#   makeup   the mesh's makeup (LCDSchema §Makeup layer, Phase26 RD-P26-2): makeup_color_map_tex
#            (RGB the colour, A its coverage; clear default) mixed over the tinted base, and the
#            scatter colour with it; makeup_finish_map_tex (R a target roughness, G its coverage;
#            black default) mixed in after the roughness clamp; both coverages x makeup_amount.
#            Coverage 0 at the defaults, so the master draws as before (no runtime owed)
MASTERS = {
    "Opaque":           dict(fn=FN_OPAQUE, calls=0, blend="opaque", two_sided=False, base_map=True),
    "TwoLayer":         dict(fn=FN_OPAQUE, calls=2, blend="opaque", two_sided=False, layer2=True),
    "Masked":           dict(fn=FN_OPAQUE, calls=2, blend="masked", two_sided=True, opacity=True, base_map=True),
    # Hair (Phase06 D12, 6.5): matte on cards, default lit (not Unreal's hair shading model, which
    # reads a flat card as one glossy sheet); the cut-out as soft coverage, dithered; the light
    # through the card folded into its colour (build_master's hair part). Dielectric: one call.
    "Hair":             dict(fn=FN_OPAQUE, calls=1, blend="masked", two_sided=True, hair=True, base_map=True),
    "Emissive":         dict(fn=FN_OPAQUE, calls=2, blend="opaque", two_sided=False, extra=EMISSION),
    "Subsurface":       dict(fn=FN_OPAQUE, calls=1, blend="opaque", two_sided=False, extra=SUBSURFACE,
                             base_map=True, shine=True, makeup=True),
    "TranslucentThin":  dict(fn=FN_TRANSLUCENT, calls=1, blend="translucent", two_sided=True,
                             extra=TRANSMISSION, thin=True),
    "TranslucentThick": dict(fn=FN_TRANSLUCENT, calls=1, blend="translucent", two_sided=True,
                             extra=TRANSMISSION, thin=False),
}

SUBSURFACE_FLOOR = 1e-4     # the scattered colour's floor (sRGB ~0.3/255: invisible)

OVERLAYS = (1, 2, 3)
GATE_CHANNEL = {1: "G", 2: "B", 3: "A"}     # MasterSet §MaskSet channel contract
# Phase10: a deposit's default colour (the Creator port overlayN_color, LCDSchema; Sand
# desaturated halfway, as the assembler's and Blender's) and the weights a deposit hides
DUST_COLOR = (0.413, 0.386, 0.308)
COVERED = {"transmission_weight", "subsurface_weight", "coat_weight", "fuzz_weight"}

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


def _png(path, rgba, size=4, pixels=None):
    """A tiny PNG (8-bit RGBA), written without any imaging library: flat ``rgba``, or ``pixels``,
    one RGBA tuple per pixel, rows top to bottom."""
    import struct
    import zlib

    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    if pixels is None:
        raw = (b"\x00" + bytes(rgba) * size) * size
    else:
        raw = b"".join(b"\x00" + b"".join(bytes(p) for p in pixels[y * size:(y + 1) * size]) for y in range(size))
    with open(path, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0))
                + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def default_texture(name, rgba, srgb=False, normal_map=False, pixels=None, size=4):
    """A flat default for a texture slot, generated and imported (no binary asset in git).
    ``normal_map`` makes it the default of a normal-map slot (MATTER_MASTERS_NORMAL_SAMPLER=normal):
    the engine checks a Normal sampler's default for the normal-map compression. ``pixels`` (with
    ``size``) gives a picture instead of a flat value (``fade_noise_texture``)."""
    import os
    folder = os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_saved_dir()), "MatterDefaults")
    os.makedirs(folder, exist_ok=True)
    src = os.path.join(folder, f"{name}.png")
    _png(src, rgba, size=size, pixels=pixels)
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
    # A normal-map default is BC5, which keeps a flat 128 exact.
    tex.set_editor_property("compression_settings",
                            unreal.TextureCompressionSettings.TC_NORMALMAP if normal_map
                            else unreal.TextureCompressionSettings.TC_EDITOR_ICON if srgb
                            else unreal.TextureCompressionSettings.TC_VECTOR_DISPLACEMENTMAP)
    EAL.save_loaded_asset(tex)
    return tex


FADE_NOISE = 64     # Phase29 29.3: the fade's blue-noise tile, FADE_NOISE x FADE_NOISE screen pixels


def blue_noise_ranks(n=FADE_NOISE, sigma=1.5, seed=1):
    """Phase29 29.3 (Q-OFL-1): every pixel of an n x n tile ranked 0 .. n*n - 1, each rank once, by
    void-and-cluster (Ulichney 1993) on the torus, so the tile repeats with no seam. Every prefix of
    the ranks (the pixels a presence keeps) is spread evenly with no grid. Pure Python from a fixed
    seed: every build makes the same map, and no binary asset is committed (~1 s)."""
    import math
    size, r = n * n, 7
    kern = [[math.exp(-(dx * dx + dy * dy) / (2 * sigma * sigma)) for dx in range(-r, r + 1)]
            for dy in range(-r, r + 1)]

    def splat(energy, i, sign):
        y0, x0 = divmod(i, n)
        for dy in range(-r, r + 1):
            row, krow = ((y0 + dy) % n) * n, kern[dy + r]
            for dx in range(-r, r + 1):
                energy[row + (x0 + dx) % n] += sign * krow[dx + r]

    def energy_of(bits):
        e = [0.0] * size
        for i in range(size):
            if bits[i]:
                splat(e, i, 1.0)
        return e

    def tightest(bits, e):          # the set pixel with the most energy around it
        return max((i for i in range(size) if bits[i]), key=e.__getitem__)

    def largest_void(bits, e):      # the empty pixel with the least
        return min((i for i in range(size) if not bits[i]), key=e.__getitem__)

    state, bits, ones = seed, [False] * size, 0      # a tenth of the pixels, from a fixed LCG
    while ones < size // 10:
        state = (state * 6364136223846793005 + 1442695040888963407) % (1 << 64)
        i = (state >> 33) % size
        if not bits[i]:
            bits[i], ones = True, ones + 1
    e = energy_of(bits)
    while True:                     # relax: the tightest cluster into the largest void, until stable
        a = tightest(bits, e)
        bits[a] = False
        splat(e, a, -1.0)
        b = largest_void(bits, e)
        bits[b] = True
        splat(e, b, 1.0)
        if b == a:
            break
    rank = [0] * size
    pb, pe = bits[:], e[:]
    for k in range(ones - 1, -1, -1):              # the prototype's own ranks, unwound
        a = tightest(pb, pe)
        pb[a] = False
        splat(pe, a, -1.0)
        rank[a] = k
    k = ones
    while k < size // 2:                           # the voids filled, to half
        b = largest_void(bits, e)
        bits[b] = True
        splat(e, b, 1.0)
        rank[b], k = k, k + 1
    e = energy_of([not v for v in bits])           # past half, the empty pixels are the minority
    while k < size:
        b = max((i for i in range(size) if not bits[i]), key=e.__getitem__)
        bits[b] = True
        splat(e, b, -1.0)
        rank[b], k = k, k + 1
    if sorted(rank) != list(range(size)):
        raise RuntimeError("blue_noise_ranks: the ranks are not a permutation")
    return rank


def fade_noise_texture():
    """Phase29 29.3: the fade's threshold tile, T_Matter_FadeNoise: each pixel's rank (0 .. 4095)
    split over R (rank // 16) and G (rank % 16), linear and uncompressed, sampled nearest with no
    mips, so the master reads the rank back exactly (``fade_threshold``)."""
    ranks = blue_noise_ranks()
    tex = default_texture("T_Matter_FadeNoise", None, size=FADE_NOISE,
                          pixels=[(k // 16, k % 16, 0, 255) for k in ranks])
    tex.set_editor_property("filter", unreal.TextureFilter.TF_NEAREST)
    tex.set_editor_property("mip_gen_settings", unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)
    tex.set_editor_property("never_stream", True)
    EAL.save_loaded_asset(tex)
    return tex


def mesh_st(g, col):
    """The mesh's st (t up), which everything downstream is written for. A mesh carrying USD's st
    hands it over as it is. A mesh carrying Unreal's V (MATTER_MASTERS_MESH_V=unreal: v = 1 - t)
    is turned back first, (u, 1 - v), so placement and sampling give the picture they give on st:
    without it ``image_uv``'s flip is a second one, and a rotation or an offset turns the wrong
    way."""
    M = unreal
    uv = g.node(M.MaterialExpressionTextureCoordinate, col)
    if MESH_V == "st":
        return uv
    flip = g.op(M.MaterialExpressionMultiply, uv,
                g.node(M.MaterialExpressionConstant2Vector, col, r=1.0, g=-1.0), col)
    return g.op(M.MaterialExpressionAdd, flip,
                g.node(M.MaterialExpressionConstant2Vector, col, r=0.0, g=1.0), col)


def place2d(g, col):
    """MaterialX ``ND_place2d_vector2`` at its defaults (pivot 0, operation order 0), on the
    mesh's st (t up): ``uv / scale``, then ``rotate2d`` (MaterialX's mx_rotate_vector2 turns the
    COORDINATE clockwise by ``uv_rotation`` degrees: (c x + s y, -s x + c y)), then ``- offset``.
    The same formula as Blender's ML_Place2D (build_masters.py)."""
    M = unreal
    st = mesh_st(g, col)
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


# Phase29 29.3 (Q-OFL-2): this frame's shift of the fade's threshold. On a view that averages over
# time (its temporal jitter sequence is longer than 1, which the engine allows only under TAA or TSR:
# SceneRendering.cpp, TemporalAAParams = (index, length, jitter x, y)) the shift walks the golden
# ratio's sequence frame by frame, so each pixel's average over frames is the presence itself: an
# even fade. On any other view (one sample per pixel, FXAA: the headset) it is 0, so the grain stays
# fixed. Read per view, so a desktop window and a headset drawn together each get their own.
FADE_FRAME_HLSL = ("return View.TemporalAAParams.y > 1.5 "
                   "? frac(float(View.StateFrameIndex % 1024u) * 0.61803398875) : 0.0;")


def fade_threshold(g, noise, col):
    """Phase29 29.3 (Q-OFL-1, Q-OFL-2): this pixel's fade threshold, t = frac((rank + 0.5) / 4096 +
    this frame's shift), rank the pixel's place in the blue-noise tile (``fade_noise_texture``,
    repeated across the screen). 4096 levels, so a slow fade flips one pixel in 4096 per level, and
    no grid. The shift is 0 on a view that does not average over time (``FADE_FRAME_HLSL``), where t
    is exactly (rank + 0.5) / 4096."""
    M = unreal
    px = g.one(M.MaterialExpressionFloor,
               g.mask(g.node(M.MaterialExpressionScreenPosition, col), "rg", col - 1, "PixelPosition"), col - 2)
    uv = g.op_k(M.MaterialExpressionMultiply, g.op_k(M.MaterialExpressionAdd, px, 0.5, col - 3),
                1.0 / FADE_NOISE, col - 4)
    s = g.node(M.MaterialExpressionTextureSample, col - 5, texture=noise,
               sampler_type=M.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
    g.link(uv, s, "UVs")

    def byte(channel):          # the 8-bit value back from unorm, exactly
        return g.one(M.MaterialExpressionFloor,
                     g.op_k(M.MaterialExpressionAdd, g.op_k(M.MaterialExpressionMultiply, s, 255.0, col - 6, channel),
                            0.5, col - 7), col - 8)
    rank = g.op(M.MaterialExpressionAdd, g.op_k(M.MaterialExpressionMultiply, byte("R"), 16.0, col - 9),
                byte("G"), col - 10)
    t = g.op_k(M.MaterialExpressionMultiply, g.op_k(M.MaterialExpressionAdd, rank, 0.5, col - 11),
               1.0 / (FADE_NOISE * FADE_NOISE), col - 12)
    shift = g.node(M.MaterialExpressionCustom, col - 12, code=FADE_FRAME_HLSL,
                   output_type=M.CustomMaterialOutputType.CMOT_FLOAT1, description="FadeFrameShift", inputs=[])
    return g.one(M.MaterialExpressionFrac, g.op(M.MaterialExpressionAdd, t, shift, col - 13), col - 14)


def fade_terms(g, col, noise):
    """Phase29 (MasterSet §Object fade, RD-P29-1, RD-P29-3): how present the object is, and this
    pixel's threshold.

    ``object_fade`` is Custom Primitive Data slot 0, written on the component, never on a material:
    0 = fully there (also what an unset slot reads), 1 = gone, negative = the copy fading in.
    Returns (presence, threshold): presence = 1 - |object_fade|; the threshold is
    ``fade_threshold``'s t (29.3: blue noise, shifted per frame on a view that averages; it was
    ``bayer4``'s 16 levels) for a copy fading out (and fully there) and 1 - t of the SAME t for one
    fading in, so two copies at f and -(1 - f) keep complementary pixels in every frame. A pixel is
    kept where threshold <= presence x the master's own coverage; a tie keeps it (Unreal keeps a
    pixel AT the clip), so a tie shows both copies, never neither. At 0 presence is exactly 1 and
    every threshold is below it: the master draws today's pixels."""
    M = unreal
    f = g.node(M.MaterialExpressionScalarParameter, col, parameter_name="object_fade", default_value=0.0,
               use_custom_primitive_data=True, primitive_data_index=0)
    presence = g.one(M.MaterialExpressionOneMinus, g.one(M.MaterialExpressionAbs, f, col - 1), col - 2)
    t = fade_threshold(g, noise, col)
    # 1 where the copy is fading in (f < 0), else exactly 0: sign(0) is 0
    fading_in = g.one(M.MaterialExpressionSaturate,
                      g.op_k(M.MaterialExpressionMultiply, g.one(M.MaterialExpressionSign, f, col - 1), -1.0, col - 2),
                      col - 3)
    threshold = lerp(g, t, g.one(M.MaterialExpressionOneMinus, t, col - 14), fading_in, col - 15)
    return presence, threshold


def fade_mask(g, presence, threshold, col, coverage=None):
    """The fade's own opacity mask, for a clip of 0.5: presence x coverage - threshold + 0.5 (kept
    at or above 0.5). ``coverage`` is the master's own soft coverage (Hair's), or none (1)."""
    M = unreal
    keep = presence if coverage is None else g.op(M.MaterialExpressionMultiply, presence, coverage, col)
    return g.op_k(M.MaterialExpressionAdd, g.op(M.MaterialExpressionSubtract, keep, threshold, col), 0.5, col - 1)


def texture(g, name, default, uv, col, colour=None, normal_map=None):
    """A texture slot: linear unless told otherwise. ``colour`` is given for a colour slot only, and only
    under MATTER_MASTERS_COLOUR_SAMPLER=srgb: the slot's sRGB default, which makes the slot sample
    an sRGB texture, decoded by the sampler. ``normal_map`` likewise for a normal slot under
    MATTER_MASTERS_NORMAL_SAMPLER=normal: the slot's normal-map default, which makes it a Normal
    sampler."""
    S = unreal.MaterialSamplerType
    if colour is not None:
        tex, kind = colour, S.SAMPLERTYPE_COLOR
    elif normal_map is not None:
        tex, kind = normal_map, S.SAMPLERTYPE_NORMAL
    else:
        tex, kind = default, S.SAMPLERTYPE_LINEAR_COLOR
    t = g.node(unreal.MaterialExpressionTextureSampleParameter2D, col, parameter_name=name,
               texture=tex, sampler_type=kind)
    g.link(uv, t, "UVs")
    return t


def tangent_normal(g, name, flat, uv, col, flat_map=None):
    """A normal slot's tangent-space normal, -1..1 (+Y up). On a linear sampler the graph decodes
    the three channels, x 2 - 1. On a Normal sampler (``flat_map`` given) the engine has already
    decoded R and G and rebuilt Z, so the graph takes its RGB as it is: no second decode."""
    if flat_map is not None:
        return g.mask(texture(g, name, flat, uv, col, normal_map=flat_map), "rgb", col - 1, "RGB")
    return g.op_k(unreal.MaterialExpressionSubtract,
                  g.op_k(unreal.MaterialExpressionMultiply, texture(g, name, flat, uv, col), 2.0, col - 1, "RGB"),
                  1.0, col - 2)


def lerp(g, a, b, alpha, col, a_out="", b_out=""):
    """mix(bg=a, fg=b, mix=alpha): MaterialX's mix, Unreal's Lerp."""
    n = g.node(unreal.MaterialExpressionLinearInterpolate, col)
    g.link(a, n, "A", a_out)
    g.link(b, n, "B", b_out)
    g.link(alpha, n, "Alpha")
    return n


def _pin(node, want, outputs=False):
    """A Substrate node's pin by its name with spaces and case ignored ("SSS MFP" = "sssmfp"):
    the Python names were not read from a running 5.8, so a miss stops the build naming them."""
    names = [str(n) for n in (MEL.get_material_expression_output_names(node) if outputs
                              else MEL.get_material_expression_input_names(node))]
    for n in names:
        if n.replace(" ", "").lower() == want:
            return n
    raise RuntimeError(f"front: {node.get_name()} has no {'output' if outputs else 'input'} {want!r}: {names}")


def one_coat_front(g, pins, metal):
    """Phase30 (D-P30-1): OpenPBR's layout in Substrate's own nodes, the Blender master's layout (one
    Principled BSDF, one coat over a linear mix). A dielectric slab and a metal slab, mixed by
    metalness with parameter blending off (the linear mix of Phase06 6.3), under ONE coat slab,
    weighted by coat_weight and layered with parameter blending off. Fed what Epic's function was fed
    (the base colour already darkened by the coat, MaterialX's own factor), and (D-P30-2):

    * base colour x base_weight, before both slabs, as OpenPBR does;
    * dielectric F0 = ((eta_s - 1) / (eta_s + 1))^2 x specular_color x min(specular_weight, 1 / eta_s),
      F90 1, eta_s the base's index relative to the coat's under it; the min is Epic's function's, not
      open_pbr_surface.mtlx's (which scales by specular_weight alone), kept because Storm agrees with it;
      metal F0 = base x specular_weight, F90 white:
      no edge tint (Drift 2026-11-12: the 5.8 slab has no F82 pin, and an F90 edge tint costs a uint
      80 B does not have; the library carries none, F-LC-6);
    * fuzz on the dielectric slab only, one fuzz a pixel (Drift 2026-11-12: a fuzzy metal loses it);
    * base_diffuse_roughness on the dielectric slab's Roughness, its specular roughness on Second
      Roughness at weight 1, as Epic's function does (the 5.8 slab has no diffuse-roughness pin);
    * the coat's colour, square-rooted, through TransmittanceToMFP; anisotropy passed as it is."""
    M = unreal

    def slab(col, **wires):
        s = g.node(M.MaterialExpressionSubstrateSlabBSDF, col)
        for want, (src, out) in wires.items():
            g.link(src, s, _pin(s, want), out)
        return s

    def f0(ior, col):
        r = g.op(M.MaterialExpressionDivide, g.op_k(M.MaterialExpressionSubtract, ior[0], 1.0, col + 1, ior[1]),
                 g.op_k(M.MaterialExpressionAdd, ior[0], 1.0, col + 1, ior[1]), col)
        return g.op(M.MaterialExpressionMultiply, r, r, col - 1)

    # F90 is left unwired where it is 1: an unwired F90 is white (MaterialExpressionSubstrate.cpp), and a wired one
    # costs an edge-colour uint a slab (SubstrateTranslatorCommon.cpp, EdgeColor). A byte test for 80 B.
    black = (g.node(M.MaterialExpressionConstant3Vector, -1, constant=unreal.LinearColor(0, 0, 0, 0)), "")
    bc, bw = pins["base_color"], pins["base_weight"]
    base_c = (g.op(M.MaterialExpressionMultiply, bc[0], bw[0], -2, a_out=bc[1], b_out=bw[1]), "")
    spec_w = pins["specular_weight"]
    common = dict(anisotropy=pins["specular_roughness_anisotropy"], normal=pins["geometry_normal"])
    # The dielectric's diffuse roughness, as Epic's function feeds it (read from its compiled shader,
    # 2026-11-12): a slab's Roughness pin also sets its diffuse (Chan) lobe, so the dielectric slab takes
    # base_diffuse_roughness there and its specular roughness as Second Roughness at weight 1. With the
    # specular roughness on Roughness the grey card drew x1.06 (sphere) to x1.12 (floor) of Storm.
    one = (g.node(M.MaterialExpressionConstant, -5, r=1.0), "")
    diffuse_rough = dict(roughness=pins["base_diffuse_roughness"], secondroughness=pins["specular_roughness"],
                         secondroughnessweight=one)
    # Fuzz on the dielectric slab only (one fuzz a pixel, not two): a byte test for 80 B. A fuzzy metal loses its fuzz.
    fuzz = dict(fuzzamount=pins["fuzz_weight"], fuzzcolor=pins["fuzz_color"], fuzzroughness=pins["fuzz_roughness"])
    # Under the coat the base's index is relative to the coat's (open_pbr_surface.mtlx eta_s, as Epic's
    # MF_OpenPBR_IOR does for the function): mix(s, max(s/c, c/s), coat_weight), the max being the TIR fix
    s, c, w = pins["specular_ior"], pins["coat_ior"], pins["coat_weight"]
    ratio = g.op(M.MaterialExpressionMax,
                 g.op(M.MaterialExpressionDivide, s[0], c[0], -1, a_out=s[1], b_out=c[1]),
                 g.op(M.MaterialExpressionDivide, c[0], s[0], -1, a_out=c[1], b_out=s[1]), 0)
    eta_s = g.node(M.MaterialExpressionLinearInterpolate, 1)
    g.link(s[0], eta_s, "A", s[1])
    g.link(ratio, eta_s, "B")
    g.link(w[0], eta_s, "Alpha", w[1])
    # specular_weight enters as min(specular_weight, 1 / eta_s), as Epic's function has it (read from its
    # compiled shader at 160 B, 2026-11-12), not as open_pbr_surface.mtlx's plain x specular_weight: at
    # index 1.5 that is F0 x 0.67. With the plain weight the slab drew every rough dielectric brighter
    # than Storm (grey card x1.03, Leather x1.05 to x1.07); with Epic's factor it draws as today's master
    # to three decimals (grey card, Leather, Felt, Porcelain). F0 is wired either way: no byte cost.
    d_f0 = g.op(M.MaterialExpressionMultiply,
                g.op(M.MaterialExpressionMultiply, f0((eta_s, ""), -3), pins["specular_color"][0], -4,
                     b_out=pins["specular_color"][1]),
                g.op(M.MaterialExpressionMin, spec_w[0],
                     g.op(M.MaterialExpressionDivide, one[0], eta_s, -5), -4, a_out=spec_w[1]), -5)
    dielectric = slab(-6, diffusealbedo=base_c, f0=(d_f0, ""), **diffuse_rough, **common, **fuzz)
    m_f0 = g.op(M.MaterialExpressionMultiply, base_c[0], spec_w[0], -5, b_out=spec_w[1])
    # The metal's F90 is left white (no edge tint): a wired F90 costs the slab a uint, and with the
    # dielectric's haziness uint the three slabs came to 21 of 80 B's 20, so the compiler blended the
    # metal mix's parameters (Verdigris drew 3.10 dE at 80 B, 0.98 at 160 B). The library carries no
    # edge tint (F-LC-6), so no article changes (Drift 2026-11-12).
    metal_slab = slab(-6, diffusealbedo=black, f0=(m_f0, ""), roughness=pins["specular_roughness"], **common)
    base = g.node(M.MaterialExpressionSubstrateHorizontalMixing, -7)
    base.set_editor_property("use_parameter_blending", False)
    g.link(dielectric, base, "Background")
    g.link(metal_slab, base, "Foreground")
    g.link(metal, base, "Mix")

    # The coat as Epic's function makes it: its colour is the transmittance of the light's whole way down
    # and back up, so each pass takes its square root (a coat tinted (0.55, 0.75, 1) drew the base x0.58 /
    # x0.77 of Storm without it), over a coat 5 thick in both the layering and the conversion.
    tint = g.node(M.MaterialExpressionSubstrateTransmittanceToMFP, -5)
    g.link(g.one(M.MaterialExpressionSquareRoot, pins["coat_color"][0], -4, pins["coat_color"][1]),
           tint, _pin(tint, "transmittancecolor"))
    thick = (g.node(M.MaterialExpressionConstant, -4, r=5.0), "")
    g.link(thick[0], tint, _pin(tint, "thickness"))
    coat = slab(-6, diffusealbedo=black, f0=(f0(pins["coat_ior"], -3), ""), roughness=pins["coat_roughness"],
                sssmfp=(tint, _pin(tint, "mfp", outputs=True)))
    # coat_weight on a Weight node over the coat, as Epic's function weights its coat. Tried 2026-11-12
    # and rejected: the coat's coverage (the Weight under a parameter-blended self-mix), which drew
    # alike to 3 decimals on every fixture but puts parameter blending in the shader; and the coat's
    # F0 scaled by the weight, which drew Leather (coat 0.3) x1.09 to x1.20 of Storm.
    weighted = g.node(M.MaterialExpressionSubstrateWeight, -7)
    g.link(coat, weighted, _pin(weighted, "a"))
    g.link(w[0], weighted, _pin(weighted, "weight"), w[1])
    top = g.node(M.MaterialExpressionSubstrateVerticalLayering, -8)
    top.set_editor_property("use_parameter_blending", False)
    g.link(weighted, top, _pin(top, "top"))
    g.link(base, top, _pin(top, "bottom"))
    g.link(thick[0], top, _pin(top, "topthickness"))    # the top layer's thickness is the layering's
    return top


def build_master(token, white, no_wear, flat, white_colour=None, grey=None, black=None, clear=None,
                 flat_map=None, noise=None):
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
      maskset_blend) (MasterSet §Overlay semantic, §MaskSet);
    * a deposit overlay (Phase10) covers: cover = effect x overlayN_deposit, the tinted base mixed
      to overlayN_color by it, and metalness, transmission, subsurface, coat and fuzz weights x
      (1 - cover), before the Hair part reads them.
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
    # Phase30: Opaque makes no call (calls 0): the same linear mix, of Substrate's own slabs, under
    # one coat (one_coat_front), fed what a call would be fed.
    calls = []
    for col in range(1, spec["calls"] + 1):
        c = g.node(M.MaterialExpressionMaterialFunctionCall, col)
        c.set_material_function(fn)
        calls.append(c)
    inputs = set(MEL.get_material_expression_input_names(calls[0])) if calls else None
    pins = {}   # what each of the function's pins is fed: the one-coat front's slabs read them

    def feed(src, name, src_out=""):
        pins[name] = (src, src_out)
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
                 texture(g, f"{prefix}base_color_tex", white, uv, 12, colour=white_colour), 11, b_out="RGB")
        r = g.op(M.MaterialExpressionMultiply, g.scalar(r_name, r_def),
                 texture(g, f"{prefix}roughness_tex", white, uv, 12), 11, b_out="R")
        m = g.op(M.MaterialExpressionMultiply, g.scalar(m_name, m_def),
                 texture(g, f"{prefix}metalness_tex", white, uv, 12), 11, b_out="R")
        n = tangent_normal(g, f"{prefix}normal_tex", flat, uv, 12, flat_map)
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
    own_st = (image_uv(g, mesh_st(g, 16), 15)
              if spec.get("base_map") or spec.get("opacity") or spec.get("hair") or spec.get("shine")
              else None)
    base_map = None
    if spec.get("base_map"):
        # The mesh's picture (LCDSchema §Base colour map, Phase09 RD-P09-1), supplied per binding:
        # base = base_color_const x base_color_map x base_color_tint; white when none is bound.
        base_map = texture(g, "base_color_map_tex", white, own_st, 12, colour=white_colour)
        base = g.op(M.MaterialExpressionMultiply, base, base_map, 10, b_out="RGB")
    base = g.op(M.MaterialExpressionMultiply, base, g.vector("base_color_tint", (1.0, 1.0, 1.0)), 10)
    makeup = None
    if spec.get("makeup"):
        # Phase26 (RD-P26-2, LCDSchema §Makeup layer): the merge's colour picture on the mesh's own
        # st, mixed over the tinted base by its A x makeup_amount, before any deposit (the assembler's
        # base_color_makeup). The clear default (0, 0, 0, 0) covers nothing.
        mk = texture(g, "makeup_color_map_tex", clear, own_st, 12)
        amount = g.scalar("makeup_amount", 1.0, col=11)
        mcov = g.op(M.MaterialExpressionMultiply, mk, amount, 10, a_out="A")
        base = lerp(g, base, mk, mcov, 9, b_out="RGB")
        makeup = (mk, mcov, amount)
    cavity = None
    scatter = None
    if spec.get("shine"):
        # Phase22 22.2 (LCDSchema §Shine maps, RD-P22-5): the mesh's relief, tangent space (+Y up) on
        # its own st: its XY added to the article's normal before the overlays, normalised once
        # below. The slot's default is the flat normal; the driver binds an exact flat constant.
        bn = tangent_normal(g, "normal_map_tex", flat, own_st, 12, flat_map)
        bxy = g.op(M.MaterialExpressionMultiply, bn,
                   g.node(M.MaterialExpressionConstant3Vector, 10,
                          constant=unreal.LinearColor(1.0, 1.0, 0.0, 0.0)), 9)
        n_ts = g.op(M.MaterialExpressionAdd, n_ts, bxy, 8)
        # RD-P22-6: the cavity map, x specular_weight (white when none is bound)
        cavity = texture(g, "cavity_map_tex", white, own_st, 7)
        # 22.3 (RD-P22-18): the scatter map raises the radius at thin parts: 1 + SCATTER_GAIN x map
        # (black when none is bound, so x 1)
        scatter = g.op_k(M.MaterialExpressionAdd,
                         g.op_k(M.MaterialExpressionMultiply, texture(g, "scatter_map_tex", black, own_st, 7),
                                SCATTER_GAIN, 6, "R"), 1.0, 5)

    keep = None     # Phase10: 1 - each deposit's cover, multiplied: what the deposits leave visible
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
        # Phase10 (MasterSet §Overlay semantic): a deposit COVERS: cover = effect x deposit; the
        # base colour goes to the deposit's colour (after the tint), and every layer under it is
        # hidden by (1 - cover). overlayN_deposit is 0 on a damage or gloss slot (the driver sets 1
        # on a deposit's), so with no deposit every master renders as v2 did.
        cover = g.op(M.MaterialExpressionMultiply, eff, g.scalar(f"overlay{n}_deposit", 0.0, col=8), 7)
        base = g.op(M.MaterialExpressionLinearInterpolate, base,
                    g.vector(f"overlay{n}_color", DUST_COLOR, col=7), 6)
        g.link(cover, base, "Alpha")
        left = g.one(M.MaterialExpressionOneMinus, cover, 6)
        keep = left if keep is None else g.op(M.MaterialExpressionMultiply, keep, left, 5)

    def hidden(src):
        """A weight under the deposits: weight x keep (= mix(weight, 0, cover), per deposit)."""
        return g.op(M.MaterialExpressionMultiply, src, keep, 4)

    metal = hidden(metal)
    if spec.get("hair"):
        # The Hair row's light through the card, OpenPBR thin-walled subsurface with its colour c the
        # tinted base (MaterialX: a reflected lobe c.c(1 - a)/2 and a transmitted one c.c(1 + a)/2,
        # mixed in by the weight w). Under even light the two sum to mix(c, c.c, w), the anisotropy
        # cancelling, and that is the card's colour here, matte and default lit (D12). Substrate's
        # own thin-surface subsurface was tried first and rejected (6.5): in one real-time capture
        # it draws the card as dark, noisy pixels, solid card or cut. Measured on the character
        # against Storm, hair dE 4.3 (the plain base 7.4); ~20 % bright, because Storm's rear lobe
        # sees only the dome, not the sun.
        # The light through is the covered colour's, and a deposit hides it as Blender's master does.
        w = hidden(g.scalar("subsurface_weight", 0.0, col=11))
        base = g.op(M.MaterialExpressionLinearInterpolate, base,
                    g.op(M.MaterialExpressionMultiply, base, base, 5), 4)
        g.link(w, base, "Alpha")
    if len(calls) == 2:
        for c, m in zip(calls, (0.0, 1.0)):
            g.link(g.node(M.MaterialExpressionConstant, 2, r=m), c, "base_metalness")
    else:
        feed(metal, "base_metalness")

    if spec.get("shine"):
        # Phase22 (LCDSchema §Shine maps, RD-P22-4): the mesh's roughness map, linear on its own st,
        # an offset around 0.5 added before the bias: clamp(r + (map - 0.5) + bias). The slot's
        # default is 128 (0.502); the library's driver binds an exact 0.5 where an article has none.
        rmap = texture(g, "roughness_map_tex", grey, own_st, 6)
        rough = g.op(M.MaterialExpressionAdd, rough,
                     g.op_k(M.MaterialExpressionSubtract, rmap, 0.5, 5, a_out="R"), 4)
    # roughness_biased_clamped (LCDSchema): the bias is added, then clamped to 0..1
    rough = g.op(M.MaterialExpressionAdd, rough, g.scalar("roughness_bias", 0.0, col=4), 3)
    rough = g.one(M.MaterialExpressionSaturate, rough, 2)
    if makeup is not None:
        # Phase26 (RD-P26-2): the finish after the bias and clamp (roughness_makeup): mix(that, R,
        # G x makeup_amount); the black default covers nothing
        fin = texture(g, "makeup_finish_map_tex", black, own_st, 4)
        fcov = g.op(M.MaterialExpressionMultiply, fin, makeup[2], 3, a_out="G")
        rough = lerp(g, rough, fin, fcov, 2, b_out="R")
    feed(rough, "specular_roughness")
    if MESH_BINORMAL == "unreal":
        # The library's normal maps are +Y up (MaterialX): green follows dP/dt, which is where the
        # runtime's meshes point their binormal (drivers/unreal.py tangent_signs). A mesh whose
        # binormal Unreal built from flipped UVs points it along +v = -dP/dt, so every bump would
        # lean the wrong way up and down. Negate Y once, on the sum (the article's map, the second
        # layer's and the three overlays'), before it is normalised. Seen in a second project
        # (2026-10-05): slate, leather and rusted steel at a glancing angle read as raised.
        n_ts = g.op(M.MaterialExpressionMultiply, n_ts,
                    g.node(M.MaterialExpressionConstant3Vector, 4,
                           constant=unreal.LinearColor(1.0, -1.0, 1.0, 0.0)), 4)
    normal = g.one(M.MaterialExpressionNormalize, n_ts, 3)
    if NORMAL_SPACE == "world":
        normal = g.one(M.MaterialExpressionTransform, normal, 2,
                       transform_source_type=M.MaterialVectorCoordTransformSource.TRANSFORMSOURCE_TANGENT,
                       transform_type=M.MaterialVectorCoordTransform.TRANSFORM_WORLD)
    feed(normal, "geometry_normal")
    if spec.get("shine"):
        # Phase22 22.2: skin's coat (its sebum) follows the skin's relief: the coat's normal is
        # mix(the geometry's, the article's, coat_follows_normal). 0 by default, so the master draws as
        # before; the driver sets 1 on an article that declares normal_map (the assembler's
        # geometry_coat_normal = normal_out).
        if "geometry_coat_normal" not in inputs:
            raise RuntimeError(f"{token}: Epic's function has no input geometry_coat_normal")
        coat_n = g.node(M.MaterialExpressionLinearInterpolate, 2)
        g.link(g.node(M.MaterialExpressionConstant3Vector, 3,
                      constant=unreal.LinearColor(0.0, 0.0, 1.0, 0.0)), coat_n, "A")
        g.link(normal, coat_n, "B")
        g.link(g.scalar("coat_follows_normal", 0.0, col=3), coat_n, "Alpha")
        feed(coat_n, "geometry_coat_normal")

    missing = []
    params = {}     # each pass-through parameter as the article sets it, before any scaling
    fed = {}        # ... and as Epic's function is given it
    for name, default in {**PASS_THROUGH, **spec.get("extra", {})}.items():
        if inputs is not None and name not in inputs:
            missing.append(name)
            continue
        p = g.vector(name, default) if isinstance(default, tuple) else g.scalar(name, default)
        params[name] = p
        if name in SCALED:
            p = g.op_k(M.MaterialExpressionMultiply, p, SCALED[name], 5)
        if name in COVERED:
            p = hidden(p)
        if name == "specular_weight" and cavity is not None:
            p = g.op(M.MaterialExpressionMultiply, p, cavity, 5, b_out="R")
        if name == "subsurface_radius" and scatter is not None:
            p = g.op(M.MaterialExpressionMultiply, p, scatter, 4)
        if name == "subsurface_color" and base_map is not None:
            # Phase09 F-P09-5: an article taking the picture scatters the PICTURE's colour (its
            # subsurface_color is connected to base_color_out), or the picture keeps only
            # 1 - subsurface_weight of its strength (the white Unreal eye of 9.2). The driver sets
            # this parameter to the article's base constant then; with no picture bound it is x 1.
            p = g.op(M.MaterialExpressionMultiply, p, base_map, 5, b_out="RGB")
            # ... and the Creator's tint, as the base takes it, where the scatter FOLLOWS the base
            # (Phase21 RD-P21-4, F-P21-3: Storm's follows base_color_out, after the tint; a value
            # the article pins stays untinted, as in Storm). `subsurface_follows_base` is 0 by
            # default and the tint white, so a master built with this draws nothing differently
            # at its defaults (no runtime owed, the lead 2026-10-05); the driver sets it to 1.
            follow = g.scalar("subsurface_follows_base", 0.0, col=6)
            p = g.op(M.MaterialExpressionMultiply, p,
                     g.lerp_from_one(g.vector("base_color_tint", (1.0, 1.0, 1.0)), follow, 5), 5)
            if makeup is not None:
                # Phase26: the scatter follows the made-up base (the makeup over it, as over the base)
                p = lerp(g, p, makeup[0], makeup[1], 4, b_out="RGB")
            # A black texel (the eye picture's pupil) would scatter a colour of exactly 0, which
            # HANGS THE GPU (learning U11: Xid 109 in SubsurfaceScattering, 9.3; the floor alone
            # cleared it, the job otherwise identical)
            p = g.op_k(M.MaterialExpressionMax, p, SUBSURFACE_FLOOR, 4)
        fed[name] = p
        # subsurface_color is fed below, darkened by the coat as the base is; emission_luminance
        # below too, times the length of its colour
        if name not in ("subsurface_color", "emission_luminance"):
            feed(p, name)
    if inputs is not None and "coat_darkening" not in inputs:
        missing.append("coat_darkening")
    if missing:
        raise RuntimeError(f"{token}: Epic's function has no input {missing}")

    # OpenPBR coat darkening, MaterialX's own (open_pbr_surface.mtlx, "Coat darkening
    # calculation"), as in Blender's _build: Kcoat = 1 - (1 - F0(coat_ior)) / coat_ior^2, Ebase =
    # mix(mix(base, subsurface_color, subsurface_weight), base x specular_weight, metalness), and
    # the base colour x mix(1, (1 - Kcoat) / (1 - Ebase Kcoat), coat_weight x coat_darkening).
    # Epic's function darkens about a third as much as MaterialX (porcelain, close up: L* -2.3
    # where Storm's is -7.3, 2026-10-10), so its own pin is given 0, not the article's value.
    ior = params["coat_ior"]
    f0 = g.op(M.MaterialExpressionDivide, g.op_k(M.MaterialExpressionSubtract, ior, 1.0, 5),
              g.op_k(M.MaterialExpressionAdd, ior, 1.0, 5), 4)
    omk = g.op(M.MaterialExpressionDivide, g.one(M.MaterialExpressionOneMinus,
                                                 g.op(M.MaterialExpressionMultiply, f0, f0, 3), 3),
               g.op(M.MaterialExpressionMultiply, ior, ior, 3), 2)        # 1 - Kcoat
    kc = g.one(M.MaterialExpressionOneMinus, omk, 2)
    e_base = base
    if "subsurface_weight" in fed:
        e_base = g.node(M.MaterialExpressionLinearInterpolate, 3)
        g.link(base, e_base, "A")
        g.link(fed["subsurface_color"], e_base, "B")
        g.link(fed["subsurface_weight"], e_base, "Alpha")
    e_metal = g.op(M.MaterialExpressionMultiply, base, fed["specular_weight"], 3)
    e_mix = g.node(M.MaterialExpressionLinearInterpolate, 2)
    g.link(e_base, e_mix, "A")
    g.link(e_metal, e_mix, "B")
    g.link(metal, e_mix, "Alpha")
    dark = g.op(M.MaterialExpressionDivide, omk,
                g.one(M.MaterialExpressionOneMinus, g.op(M.MaterialExpressionMultiply, e_mix, kc, 2), 2), 1)
    amount = g.op(M.MaterialExpressionMultiply, fed["coat_weight"],
                  g.scalar("coat_darkening", 1.0, col=3), 2)
    # MaterialX darkens the whole base substrate, so the scattered colour too: Epic's function
    # takes it on its own pin, where Blender's Principled folds it into Base Color
    factor = g.lerp_from_one(dark, amount, 1)
    feed(g.op(M.MaterialExpressionMultiply, base, factor, 1), "base_color")
    if "subsurface_color" in fed:
        feed(g.op(M.MaterialExpressionMultiply, fed["subsurface_color"], factor, 1), "subsurface_color")
    if calls:
        feed(g.node(M.MaterialExpressionConstant, 2, r=0.0), "coat_darkening")
    if "emission_luminance" in fed:
        # The light. OpenPBR's radiance is emission_luminance x emission_color. Epic's function
        # draws emission_luminance x the colour's DIRECTION, the colour over its own length:
        # white, a 0.5 grey and a 0.2 grey read alike, and over twelve colours the reading x the
        # colour's length is one number to 5 parts in 10,000 (2026-10-11: float captures, black
        # base, sun and sky scaled to zero, Storm renders the product exactly). So the luminance
        # is given the colour's length, and a black colour gives no light.
        colour = params["emission_color"]
        length = g.one(M.MaterialExpressionSquareRoot,
                       g.op(M.MaterialExpressionDotProduct, colour, colour, 4), 3)
        feed(g.op(M.MaterialExpressionMultiply, fed["emission_luminance"], length, 2), "emission_luminance")
    if "thin" in spec:
        feed(g.node(M.MaterialExpressionConstant, 2, r=1.0 if spec["thin"] else 0.0), "geometry_thin_walled")

    if calls:
        outs = [str(o) for o in MEL.get_material_expression_output_names(calls[0])]
        front = next(o for o in outs if "front" in o.lower())
    # Phase29 (MasterSet §Object fade, RD-P29-1): every master dissolves an object part-present, one
    # rule, each in its own blend mode; at object_fade 0 every master draws today's pixels.
    presence, threshold = fade_terms(g, 30, noise)
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
        # Phase29: the fade is a second test beside the alpha test; the pixel must pass both
        clip = g.op(M.MaterialExpressionMin, clip, fade_mask(g, presence, threshold, 2), 0)
    elif spec.get("hair"):
        # Hair (MasterSet: masked, DITHERED): the coverage is soft, never thresholded at a cutoff,
        # so each pixel keeps it against its own ordered-dither threshold. It is not fed to Epic's
        # function, whose weight would scale the kept pixels by it a second time. Phase29 29.3: the
        # fade is a second test beside it, on the fade's own threshold, which every part of the
        # object shares: a pixel the fade drops on the head is dropped on the hair over it too, and
        # at object_fade 0 the second test always passes, so the hair draws today's pixels.
        clip = g.op(M.MaterialExpressionMin, fade_mask(g, cov, bayer4(g, 12), 2),
                    fade_mask(g, presence, threshold, 2), 1)
    elif spec["blend"] == "opaque":
        # Phase29 (RD-P29-2): an opaque master ignores its mask; its masked instance
        # (MI_Matter_<Token>_Fading, build_fading) takes the same graph and keeps the test.
        clip = fade_mask(g, presence, threshold, 2)
    if spec["blend"] != "translucent":
        if not MEL.connect_material_property(clip, "", unreal.MaterialProperty.MP_OPACITY_MASK):
            raise RuntimeError(f"{token}: cannot connect the opacity mask")
        mat.set_editor_property("opacity_mask_clip_value", 0.5)
    else:
        # Phase29: translucency keeps no pixel back by a clip, so a dropped pixel is given no coverage
        # (no glass drawn) and, below, an index of 1 (it bends nothing). kept is exactly 1 or 0:
        # saturate(sign(presence - threshold) + 1), 1 at a tie.
        if "geometry_opacity" not in inputs:
            raise RuntimeError(f"{token}: Epic's function has no input geometry_opacity")
        kept = g.one(M.MaterialExpressionSaturate,
                     g.op_k(M.MaterialExpressionAdd,
                            g.one(M.MaterialExpressionSign,
                                  g.op(M.MaterialExpressionSubtract, presence, threshold, 4), 3), 1.0, 3), 2)
        feed(kept, "geometry_opacity")
    if not calls:
        top, top_out = one_coat_front(g, pins, metal), ""
    elif len(calls) == 2:
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
        if REFRACTION == "index":
            # M6. Seen live in a second project (2026-10-05): with the function's output here,
            # neither see-through master bends, so the solid one is wrong. MasterSet's rule, wired
            # directly: a solid bends by the article's index; a thin wall is not deflected, and an
            # index of 1.0 removes the bend while the distortion pass still blurs by roughness.
            # The default since 2026-10-16: the rig's side view shows the solid master bending,
            # and the four thin articles' pictures unchanged to the pixel.
            ior_src, ior = (g.node(M.MaterialExpressionConstant, 2, r=1.0) if spec.get("thin")
                            else params["specular_ior"]), ""
        else:
            ior_src, ior = calls[0], next(o for o in outs if "refraction" in o.lower())
        # Phase29 (RD-P29-1): a dropped pixel bends nothing, always: mix(index, 1, 1 - kept), exactly
        # the index where kept is 1
        bend = g.node(M.MaterialExpressionLinearInterpolate, 1, const_b=1.0)
        g.link(ior_src, bend, "A", ior)
        g.link(g.one(M.MaterialExpressionOneMinus, kept, 1), bend, "Alpha")
        ior_src, ior = bend, ""
        if not MEL.connect_material_property(ior_src, ior, unreal.MaterialProperty.MP_REFRACTION):
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
    if SKINNED:
        # A character is a skinned mesh with morph targets. The editor adds a missing usage by
        # itself; a packaged or -game run cannot, and draws Unreal's default material instead.
        mat.set_editor_property("used_with_skeletal_mesh", True)
        mat.set_editor_property("used_with_morph_targets", True)
    if INSTANCED:
        # The same holds for an instanced static mesh: the editor adds the usage at load and
        # recompiles it every launch; a packaged run draws Unreal's default material.
        mat.set_editor_property("used_with_instanced_static_meshes", True)
    return mat


FADING = ("Opaque", "TwoLayer", "Emissive", "Subsurface")     # Phase29 RD-P29-2: the solid masters


def build_fading(master):
    """Phase29 (RD-P29-2, MasterSet §Object fade): a solid master's MASKED INSTANCE,
    MI_Matter_<Token>_Fading: the master with its blend mode overridden to masked and its clip to
    0.5 (Unreal's default is 0.3333), and nothing else: no graph and no parameter of its own. A
    consumer re-parents a part to it while the object is part-present. Unreal 5.8 compiles an
    instance asset's overrides into the instance's own shaders (F-POA-2), so they must be ready
    before first use, as a master's are."""
    name = master.get_name().replace("M_Matter_", "MI_Matter_") + "_Fading"
    path = f"{ROOT}/{name}"
    if EAL.does_asset_exist(path):
        EAL.delete_asset(path)
    mic = TOOLS.create_asset(name, ROOT, unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    MEL.set_material_instance_parent(mic, master)
    ov = mic.get_editor_property("base_property_overrides")
    ov.set_editor_property("override_blend_mode", True)
    ov.set_editor_property("blend_mode", unreal.BlendMode.BLEND_MASKED)
    ov.set_editor_property("override_opacity_mask_clip_value", True)
    ov.set_editor_property("opacity_mask_clip_value", 0.5)
    mic.set_editor_property("base_property_overrides", ov)
    MEL.update_material_instance(mic)
    if not EAL.save_loaded_asset(mic):
        raise RuntimeError(f"cannot save {name}")
    got = mic.get_editor_property("base_property_overrides")
    log(f"built {name} parent={master.get_name()} blend={got.get_editor_property('blend_mode')} "
        f"clip={got.get_editor_property('opacity_mask_clip_value')} "
        f"override_blend={got.get_editor_property('override_blend_mode')}")


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
    log(f"told root={ROOT} skinned={int(SKINNED)} instanced={int(INSTANCED)} mesh_v={MESH_V} "
        f"mesh_binormal={MESH_BINORMAL} sky={int(SKY)} colour_sampler={COLOUR_SAMPLER} "
        f"normal_sampler={NORMAL_SAMPLER} refraction={REFRACTION}")
    white = default_texture("T_Matter_White", (255, 255, 255, 255))
    no_wear = default_texture("T_Matter_NoWear", (128, 128, 0, 0))     # an overlay at alpha 0
    flat = default_texture("T_Matter_FlatNormal", (128, 128, 255, 255))
    grey = default_texture("T_Matter_Grey", (128, 128, 128, 255))     # a shine map's neutral
    black = default_texture("T_Matter_Black", (0, 0, 0, 255))         # the scatter map's neutral
    clear = default_texture("T_Matter_Clear", (0, 0, 0, 0))           # Phase26: makeup, coverage 0
    white_colour = (default_texture("T_Matter_WhiteColour", (255, 255, 255, 255), srgb=True)
                    if COLOUR_SAMPLER == "srgb" else None)
    flat_map = (default_texture("T_Matter_FlatNormalMap", (128, 128, 255, 255), normal_map=True)
                if NORMAL_SAMPLER == "normal" else None)
    noise = fade_noise_texture()                                       # Phase29 29.3: the fade's threshold
    masters = {t: build_master(t, white, no_wear, flat, white_colour, grey, black, clear, flat_map, noise)
               for t in MASTERS}
    for mat in list(masters.values()) + ([build_sky()] if SKY else []):
        save(mat)
    for t in FADING:
        build_fading(masters[t])
    log("RESULT ok")


main()
