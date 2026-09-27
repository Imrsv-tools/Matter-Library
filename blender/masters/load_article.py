"""Build a Blender material for one Matter article, on its master (Phase05).

    import load_article
    mat = load_article.build(Path(".../Copper_Verdigris_Aged_Base_s01_v01.mtlx"),
                             sliders={"roughness_bias": 0.25})

The article is read with ``xml.etree`` (Blender's Python has no MaterialX module), by the
assembler's FIXED node names — the render-role contract (LCDSchema §Render-role texture
nodes; ``tools/converters/assemble_mtlx.py``): ``<role>_tex`` is an image, ``<role>_const``
a constant, for the roles base_color, roughness, metalness and normal. Values authored
directly on ``open_pbr_surface`` (lane A: ``specular_ior``, ``base_metalness`` …) are read
from the shader node. The Creator sliders' start values are the nodegraph's interface
inputs; ``sliders`` overrides them, as a Creator would.
"""

from __future__ import annotations

import math
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

import bpy

import build_masters

COLOR_SPACES = {"srgb_texture": "sRGB", "lin_rec709": "Non-Color", None: "Non-Color"}
# per-article texture roles (the assembler's <role>_tex / <role>_const) -> the master socket;
# a role is wired only where the article's master has the socket
ROLES = (("base_color", "Base Color"), ("roughness", "Roughness"), ("metalness", "Metalness"),
         ("normal", "Normal Map"), ("layer2_base_color", "Layer 2 Base Color"),
         ("layer2_roughness", "Layer 2 Roughness"), ("layer2_metalness", "Layer 2 Metalness"),
         ("layer2_normal", "Layer 2 Normal Map"), ("opacity", "Opacity"))
# The Creator ports that travel Blender -> USD as material inputs (the exporter's
# LCD_TRAVEL_PORTS); the UV ports travel as geometry and are fixed inside the group.
TRAVEL_PORTS = ("base_color_tint", "overlay1_density", "overlay2_density", "overlay3_density",
                "maskset_blend", "roughness_bias")
DATA_ROLES = ("roughness", "metalness", "normal", "layer2_roughness", "layer2_metalness",
              "layer2_normal", "opacity")


def _floats(text: str | None) -> list[float]:
    return [float(v) for v in (text or "").split(",") if v.strip()]


@dataclass
class ArticleData:
    path: Path
    name: str
    master: str
    ports: dict[str, list[float]] = field(default_factory=dict)       # Creator start values
    shader: dict[str, list[float]] = field(default_factory=dict)      # lane-A values
    textures: dict[str, tuple[Path, str]] = field(default_factory=dict)  # role -> (file, cs)
    layer_scale: dict[str, float] = field(default_factory=dict)  # role -> tilesize / imagesize
    consts: dict[str, list[float]] = field(default_factory=dict)      # role -> value


def read(path: Path) -> ArticleData:
    root = ET.parse(path).getroot()
    doc_cs = root.get("colorspace")
    master = next((i.get("value") for i in root.iter("input")
                   if i.get("name") == "master_material"), "Opaque")
    art = ArticleData(path, path.stem, master)
    ng = root.find("nodegraph")
    if ng is not None:
        for i in ng.findall("input"):
            art.ports[i.get("name")] = _floats(i.get("value"))
        for node in ng:
            name = node.get("name", "")
            if name == "cutout_tex":
                continue        # its file is the binding's cut-out map (build's `cutout_map`)
            if name.endswith("_tex") and node.tag in ("image", "tiledimage"):
                f = node.find("input[@name='file']")
                cs = node.get("colorspace", doc_cs if node.get("type", "").startswith("color") else None)
                art.textures[name[:-4]] = ((path.parent / f.get("value")).resolve(), cs)
                if node.tag == "tiledimage":
                    # MaterialX NG_tiledimage: uv / realworldimagesize * realworldtilesize
                    img = _floats(node.find("input[@name='realworldimagesize']").get("value"))
                    tile = _floats(node.find("input[@name='realworldtilesize']").get("value"))
                    if img[0] != img[-1] or tile[0] != tile[-1]:
                        raise NotImplementedError(f"{path.stem}/{name}: non-square layer size")
                    art.layer_scale[name[:-4]] = tile[0] / img[0]
            elif name.endswith("_const") and node.tag == "constant":
                art.consts[name[:-6]] = _floats(node.find("input[@name='value']").get("value"))
    sh = root.find("open_pbr_surface")
    if sh is not None:
        for i in sh.findall("input"):
            if i.get("value") is not None:
                art.shader[i.get("name")] = _floats(i.get("value")) if i.get("type") != "boolean" \
                    else [1.0 if i.get("value") == "true" else 0.0]
    return art


def _rgba(v: list[float]) -> tuple[float, float, float, float]:
    v = list(v) + [1.0] * (4 - len(v))
    return (v[0], v[1], v[2], 1.0)


def build(path: Path, sliders: dict | None = None, name: str | None = None,
          cutout_map: Path | None = None):
    """A new material for ``path`` with ``sliders`` applied; returns the material.

    ``cutout_map`` is the mesh's cut-out (LCDSchema §Cut-out map), supplied per binding the way
    a USD writer sets the Material's ``inputs:cutout_map``. It is sampled on the mesh's own UVs
    (not the article's placement); with none, the master's Opacity stays 1 (opaque).
    """
    build_masters.ensure_all()
    art = read(path)
    if art.master not in build_masters.MASTERS:
        raise NotImplementedError(f"{art.name}: master {art.master!r} has no Blender version yet")
    ports = dict(art.ports)
    for k, v in (sliders or {}).items():
        if k not in ports:
            raise KeyError(f"{art.name} does not declare the slider {k!r}")
        ports[k] = list(v) if isinstance(v, (list, tuple)) else [float(v)]

    mat = bpy.data.materials.new(name or art.name)
    mat["ml_article"] = str(path)
    mat["ml_master"] = art.master
    thick = "thick" in build_masters.MASTER_PARTS[art.master]

    # The whole article network lives in ONE per-article group, MatterLCD_<name>, whose inputs
    # are the article's Creator travel ports, defaulting to the ARTICLE'S values. The Blender
    # exporter measures a Creator's edits against exactly those interface defaults (sparse
    # deltas: an untouched material exports nothing), as it did on the look-alike's groups.
    wrap = bpy.data.node_groups.new(f"MatterLCD_{name or art.name}", "ShaderNodeTree")
    wrap.interface.new_socket(name="BSDF", in_out="OUTPUT", socket_type="NodeSocketShader")
    if thick:
        wrap.interface.new_socket(name="Volume", in_out="OUTPUT", socket_type="NodeSocketShader")
    nt = wrap
    L = nt.links.new
    gin = nt.nodes.new("NodeGroupInput")
    gin.location = (-1200, 600)
    out = nt.nodes.new("NodeGroupOutput")
    out.location = (900, 0)
    master = nt.nodes.new("ShaderNodeGroup")
    master.node_tree = bpy.data.node_groups[f"ML_{art.master}"]
    master.location = (500, 0)
    L(master.outputs["BSDF"], out.inputs["BSDF"])

    uv = nt.nodes.new("ShaderNodeUVMap")
    uv.uv_map = ""          # the ACTIVE UV map (a Blender mesh's "UVMap", a USD import's "st")
    uv.location = (-900, 0)
    place = nt.nodes.new("ShaderNodeGroup")
    place.node_tree = bpy.data.node_groups["ML_Place2D"]
    place.location = (-650, 0)
    L(uv.outputs["UV"], place.inputs["UV"])
    if "uv_scale" in ports:
        s = ports["uv_scale"]
        place.inputs["uv_scale"].default_value = (s[0], s[1], 1.0)
    if "uv_offset" in ports:
        o = ports["uv_offset"]
        place.inputs["uv_offset"].default_value = (o[0], o[1], 0.0)
    if "uv_rotation" in ports:
        place.inputs["uv_rotation"].default_value = ports["uv_rotation"][0]

    y = 400
    for role, socket in ROLES:
        if socket not in master.inputs:
            continue
        if role in art.textures:
            file, cs = art.textures[role]
            img = bpy.data.images.load(str(file), check_existing=True)
            img.colorspace_settings.name = "Non-Color" if role in DATA_ROLES else COLOR_SPACES.get(cs, "sRGB")
            tex = nt.nodes.new("ShaderNodeTexImage")
            tex.image = img
            tex.interpolation = "Linear"
            tex.extension = "REPEAT"
            tex.location = (-300, y)
            L(place.outputs["UV"], tex.inputs["Vector"])
            L(tex.outputs["Color"], master.inputs[socket])
        elif role in art.consts or (role.startswith("layer2_") and role in ports):
            v = art.consts.get(role) or ports[role]     # layer 2's consts are author-tier ports
            master.inputs[socket].default_value = _rgba(v) if role.endswith("base_color") else v[0]
        elif role == "base_color" and "base_color" in art.shader:
            master.inputs[socket].default_value = _rgba(art.shader["base_color"])
        elif role == "roughness" and "specular_roughness" in art.shader:
            master.inputs[socket].default_value = art.shader["specular_roughness"][0]
        elif role == "metalness" and "base_metalness" in art.shader:
            master.inputs[socket].default_value = art.shader["base_metalness"][0]
        y -= 300

    if cutout_map is not None:
        if "cutout_map" not in art.ports or "Opacity" not in master.inputs:
            raise KeyError(f"{art.name} does not declare the cut-out input (cutout_map)")
        img = bpy.data.images.load(str(cutout_map), check_existing=True)
        img.colorspace_settings.name = "Non-Color"
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = img
        tex.interpolation = "Linear"
        tex.extension = "REPEAT"
        tex.location = (-300, y)
        L(uv.outputs["UV"], tex.inputs["Vector"])     # the mesh's UVs, unplaced
        L(tex.outputs["Color"], master.inputs["Opacity"])
        y -= 300

    # shared layers: data textures (never colour), each at its own real-world size
    for role, socket in [("maskset", "Maskset")] + [(f"overlay{n}", f"Overlay {n}")
                                                   for n in build_masters.OVERLAYS]:
        if role not in art.textures:
            continue
        file, _cs = art.textures[role]
        img = bpy.data.images.load(str(file), check_existing=True)
        img.colorspace_settings.name = "Non-Color"
        img.alpha_mode = "CHANNEL_PACKED"       # alpha is data (density / gate), not coverage
        scale = nt.nodes.new("ShaderNodeVectorMath")
        scale.operation = "SCALE"
        scale.location = (-450, y)
        L(place.outputs["UV"], scale.inputs[0])
        scale.inputs["Scale"].default_value = art.layer_scale.get(role, 1.0)
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = img
        tex.interpolation = "Linear"
        tex.extension = "REPEAT"
        tex.location = (-300, y)
        L(scale.outputs[0], tex.inputs["Vector"])
        L(tex.outputs["Color"], master.inputs[socket])
        L(tex.outputs["Alpha"], master.inputs[f"{socket} Alpha"])
        y -= 300
    for port in ("maskset_blend",) + tuple(f"overlay{n}_density" for n in build_masters.OVERLAYS):
        if port in ports:
            master.inputs[port].default_value = ports[port][0]

    if "base_color_tint" in ports:
        master.inputs["base_color_tint"].default_value = _rgba(ports["base_color_tint"])
    if "roughness_bias" in ports:
        master.inputs["roughness_bias"].default_value = ports["roughness_bias"][0]
    if "specular_ior" in art.shader:
        master.inputs["IOR"].default_value = art.shader["specular_ior"][0]
    if "specular_weight" in art.shader:
        master.inputs["Specular Weight"].default_value = art.shader["specular_weight"][0]
    if "base_weight" in art.shader and art.shader["base_weight"][0] != 1.0:
        raise NotImplementedError(f"{art.name}: base_weight != 1 is not mapped yet")

    # author-tier ports (lane B) and lane-A shader values, wherever the master has the socket
    for port in ("layer_blend_balance", "layer_blend_contrast", "opacity_cutoff"):
        if port in ports and port in master.inputs:
            master.inputs[port].default_value = ports[port][0]
    sh = art.shader
    lane_a = {"emission_color": ("Emission Color", _rgba), "emission_luminance": ("Emission Luminance", None),
              "transmission_weight": ("Transmission Weight", None),
              "transmission_color": ("Transmission Color", _rgba),
              "subsurface_weight": ("Subsurface Weight", None), "subsurface_color": ("Subsurface Color", _rgba),
              "subsurface_radius": ("Subsurface Radius", None),
              "subsurface_radius_scale": ("Subsurface Radius Scale", tuple),
              "subsurface_scatter_anisotropy": ("Subsurface Anisotropy", None),
              "coat_weight": ("Coat Weight", None), "coat_color": ("Coat Color", _rgba),
              "coat_roughness": ("Coat Roughness", None), "coat_ior": ("Coat IOR", None),
              "fuzz_weight": ("Fuzz Weight", None), "fuzz_color": ("Fuzz Color", _rgba),
              "fuzz_roughness": ("Fuzz Roughness", None),
              "specular_roughness_anisotropy": ("Anisotropy", None)}
    for key, (socket, conv) in lane_a.items():
        if key in sh and socket in master.inputs:
            master.inputs[socket].default_value = conv(sh[key]) if conv else sh[key][0]
    if "Absorption" in master.inputs:
        # OpenPBR thick: transmission_color is what is left after transmission_depth of
        # travel (Beer-Lambert), so sigma = -ln(color) / depth, per channel; the SURFACE is
        # untinted (the colour lives in the volume)
        tc = sh.get("transmission_color", [1.0, 1.0, 1.0])
        depth = sh.get("transmission_depth", [0.0])[0]
        sigma = [(-math.log(max(c, 1e-4)) / depth) if depth > 0 else 0.0 for c in tc]
        master.inputs["Absorption"].default_value = tuple(sigma)
        master.inputs["Transmission Color"].default_value = (1.0, 1.0, 1.0, 1.0)
        L(master.outputs["Volume"], out.inputs["Volume"])
    if "geometry_thin_walled" in sh:
        thin = sh["geometry_thin_walled"][0] > 0.5
        want = art.master == "TranslucentThin"
        if art.master.startswith("Translucent") and thin != want:
            raise ValueError(f"{art.name}: geometry_thin_walled={thin} contradicts master {art.master}")

    # the Creator travel ports: exposed on the wrapper, defaulting to the ARTICLE's values
    travel = [p for p in TRAVEL_PORTS if p in art.ports and p in master.inputs]
    for p in travel:
        is_color = p == "base_color_tint"
        s = wrap.interface.new_socket(name=p, in_out="INPUT",
                                      socket_type="NodeSocketColor" if is_color else "NodeSocketFloat")
        s.default_value = _rgba(art.ports[p]) if is_color else art.ports[p][0]
        L(gin.outputs[p], master.inputs[p])

    # the material: the article's group, with the sliders on it as a Creator would set them
    mnt = mat.node_tree
    mnt.nodes.clear()
    node = mnt.nodes.new("ShaderNodeGroup")
    node.node_tree = wrap
    mout = mnt.nodes.new("ShaderNodeOutputMaterial")
    mout.location = (300, 0)
    mnt.links.new(node.outputs["BSDF"], mout.inputs["Surface"])
    if thick:
        mnt.links.new(node.outputs["Volume"], mout.inputs["Volume"])
    for p in travel:
        node.inputs[p].default_value = _rgba(ports[p]) if p == "base_color_tint" else ports[p][0]
    return mat
