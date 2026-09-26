"""Blender versions of the Matter masters, built by code (Phase05).

Run inside Blender (``import build_masters; build_masters.ensure_all()``). Every group is
get-or-create, so calling it twice is harmless.

The formulas are MaterialX's, copied, not approximated — each one names its source:

* ``ML_Place2D`` — MaterialX ``ND_place2d_vector2`` at its defaults (pivot 0, operation
  order 0): ``uv / scale``, then ``rotate2d`` (which turns the COORDINATE clockwise by
  ``uv_rotation`` degrees, so the texture appears counter-clockwise), then ``- offset``.
  Blender's Vector Rotate turns counter-clockwise, so it is given ``-uv_rotation``.
* ``ML_Opaque`` — the Opaque master's shading: ``base_color x base_color_tint`` (the
  article's ``base_color_tinted``), ``clamp(roughness + roughness_bias, 0, 1)`` (LCDSchema:
  added, then clamped), metalness, and the article's tangent-space normal map, into a
  Principled BSDF standing in for ``open_pbr_surface`` (both are the OpenPBR model).

Sockets that are Creator ports carry the frozen port name (LCDSchema §Creator subset), so
the Blender exporter reads them as it read the look-alike's.

Textures are sampled OUTSIDE the groups (a node group is shared, an image is per article):
the article loader (``load_article.py``) wires UV -> ML_Place2D -> Image nodes -> master.
"""

from __future__ import annotations

import math

import bpy

VERSION = 1     # bump when a group's contents change; ensure_*() rebuilds an older one


def _group(name: str, sockets_in, sockets_out):
    ng = bpy.data.node_groups.get(name)
    if ng is not None and ng.get("ml_version") == VERSION:
        return ng, False
    if ng is None:
        ng = bpy.data.node_groups.new(name, "ShaderNodeTree")
    ng.nodes.clear()
    ng.interface.clear()
    for sname, stype, default in sockets_in:
        s = ng.interface.new_socket(name=sname, in_out="INPUT", socket_type=stype)
        if default is not None:
            s.default_value = default
    for sname, stype in sockets_out:
        ng.interface.new_socket(name=sname, in_out="OUTPUT", socket_type=stype)
    ng["ml_version"] = VERSION
    return ng, True


def _node(ng, kind: str, x: float, y: float, **props):
    n = ng.nodes.new(kind)
    n.location = (x, y)
    for k, v in props.items():
        setattr(n, k, v)
    return n


def _vmath(ng, op: str, x, y):
    return _node(ng, "ShaderNodeVectorMath", x, y, operation=op)


def _math(ng, op: str, x, y, clamp: bool = False):
    return _node(ng, "ShaderNodeMath", x, y, operation=op, use_clamp=clamp)


def ensure_place2d():
    ng, fresh = _group(
        "ML_Place2D",
        [("UV", "NodeSocketVector", None),
         ("uv_scale", "NodeSocketVector", (1.0, 1.0, 1.0)),
         ("uv_offset", "NodeSocketVector", (0.0, 0.0, 0.0)),
         ("uv_rotation", "NodeSocketFloat", 0.0)],
        [("UV", "NodeSocketVector")])
    if not fresh:
        return ng
    L = ng.links.new
    gi = _node(ng, "NodeGroupInput", -800, 0)
    go = _node(ng, "NodeGroupOutput", 400, 0)
    div = _vmath(ng, "DIVIDE", -500, 100)
    L(gi.outputs["UV"], div.inputs[0])
    L(gi.outputs["uv_scale"], div.inputs[1])
    ang = _math(ng, "MULTIPLY", -500, -150)
    L(gi.outputs["uv_rotation"], ang.inputs[0])
    ang.inputs[1].default_value = -math.pi / 180.0
    rot = _node(ng, "ShaderNodeVectorRotate", -250, 100, rotation_type="Z_AXIS")
    rot.inputs["Center"].default_value = (0.0, 0.0, 0.0)
    L(div.outputs[0], rot.inputs["Vector"])
    L(ang.outputs[0], rot.inputs["Angle"])
    off = _vmath(ng, "SUBTRACT", 100, 0)
    L(rot.outputs[0], off.inputs[0])
    L(gi.outputs["uv_offset"], off.inputs[1])
    L(off.outputs[0], go.inputs["UV"])
    return ng


def ensure_opaque():
    ng, fresh = _group(
        "ML_Opaque",
        [("Base Color", "NodeSocketColor", (0.8, 0.8, 0.8, 1.0)),
         ("base_color_tint", "NodeSocketColor", (1.0, 1.0, 1.0, 1.0)),
         ("Roughness", "NodeSocketFloat", 0.5),
         ("roughness_bias", "NodeSocketFloat", 0.0),
         ("Metalness", "NodeSocketFloat", 0.0),
         ("Normal Map", "NodeSocketColor", (0.5, 0.5, 1.0, 1.0)),
         ("Use Normal Map", "NodeSocketFloat", 0.0),
         ("IOR", "NodeSocketFloat", 1.5),
         ("Specular Weight", "NodeSocketFloat", 1.0)],
        [("BSDF", "NodeSocketShader")])
    if not fresh:
        return ng
    L = ng.links.new
    gi = _node(ng, "NodeGroupInput", -1000, 0)
    go = _node(ng, "NodeGroupOutput", 600, 0)
    bsdf = _node(ng, "ShaderNodeBsdfPrincipled", 250, 0)
    L(bsdf.outputs["BSDF"], go.inputs["BSDF"])

    tint = _vmath(ng, "MULTIPLY", -600, 300)                  # base_color_tinted
    L(gi.outputs["Base Color"], tint.inputs[0])
    L(gi.outputs["base_color_tint"], tint.inputs[1])
    L(tint.outputs[0], bsdf.inputs["Base Color"])

    rough = _math(ng, "ADD", -600, 100, clamp=True)            # roughness_biased_clamped
    L(gi.outputs["Roughness"], rough.inputs[0])
    L(gi.outputs["roughness_bias"], rough.inputs[1])
    L(rough.outputs[0], bsdf.inputs["Roughness"])

    L(gi.outputs["Metalness"], bsdf.inputs["Metallic"])
    L(gi.outputs["IOR"], bsdf.inputs["IOR"])
    spec = _math(ng, "MULTIPLY", -600, -100)                   # 0.5 = "use the IOR as is"
    L(gi.outputs["Specular Weight"], spec.inputs[0])
    spec.inputs[1].default_value = 0.5
    L(spec.outputs[0], bsdf.inputs["Specular IOR Level"])

    # normal = the map's normal where the article has one, else the geometric normal
    nmap = _node(ng, "ShaderNodeNormalMap", -700, -300, space="TANGENT", uv_map="st")
    L(gi.outputs["Normal Map"], nmap.inputs["Color"])
    geo = _node(ng, "ShaderNodeNewGeometry", -700, -550)
    d = _vmath(ng, "SUBTRACT", -450, -350)
    L(nmap.outputs["Normal"], d.inputs[0])
    L(geo.outputs["Normal"], d.inputs[1])
    sc = _vmath(ng, "SCALE", -250, -350)
    L(d.outputs[0], sc.inputs[0])
    L(gi.outputs["Use Normal Map"], sc.inputs["Scale"])
    add = _vmath(ng, "ADD", -50, -350)
    L(geo.outputs["Normal"], add.inputs[0])
    L(sc.outputs[0], add.inputs[1])
    nrm = _vmath(ng, "NORMALIZE", 100, -350)
    L(add.outputs[0], nrm.inputs[0])
    L(nrm.outputs[0], bsdf.inputs["Normal"])
    return ng


MASTERS = {"Opaque": ensure_opaque}


def ensure_all():
    ensure_place2d()
    for fn in MASTERS.values():
        fn()
