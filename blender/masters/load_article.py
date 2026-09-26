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

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

import bpy

import build_masters

COLOR_SPACES = {"srgb_texture": "sRGB", "lin_rec709": "Non-Color", None: "Non-Color"}
DATA_ROLES = ("roughness", "metalness", "normal")


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
            if name.endswith("_tex") and node.tag in ("image", "tiledimage"):
                f = node.find("input[@name='file']")
                cs = node.get("colorspace", doc_cs if node.get("type", "").startswith("color") else None)
                art.textures[name[:-4]] = ((path.parent / f.get("value")).resolve(), cs)
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


def build(path: Path, sliders: dict | None = None, name: str | None = None):
    """A new material for ``path`` with ``sliders`` applied; returns the material."""
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
    nt = mat.node_tree
    nt.nodes.clear()
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    out.location = (900, 0)
    master = nt.nodes.new("ShaderNodeGroup")
    master.node_tree = bpy.data.node_groups[f"ML_{art.master}"]
    master.location = (500, 0)
    L(master.outputs["BSDF"], out.inputs["Surface"])

    uv = nt.nodes.new("ShaderNodeUVMap")
    uv.uv_map = "st"
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
    for role, socket in (("base_color", "Base Color"), ("roughness", "Roughness"),
                         ("metalness", "Metalness"), ("normal", "Normal Map")):
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
            if role == "normal":
                master.inputs["Use Normal Map"].default_value = 1.0
        elif role in art.consts:
            v = art.consts[role]
            master.inputs[socket].default_value = _rgba(v) if role == "base_color" else v[0]
        elif role == "base_color" and "base_color" in art.shader:
            master.inputs[socket].default_value = _rgba(art.shader["base_color"])
        elif role == "roughness" and "specular_roughness" in art.shader:
            master.inputs[socket].default_value = art.shader["specular_roughness"][0]
        elif role == "metalness" and "base_metalness" in art.shader:
            master.inputs[socket].default_value = art.shader["base_metalness"][0]
        y -= 300

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
    return mat
