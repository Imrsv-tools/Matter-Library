"""Blender versions of the Matter masters, built by code (Phase05).

Run inside Blender (``import build_masters; build_masters.ensure_all()``). Every group is
get-or-create, so calling it twice is harmless.

The formulas are MaterialX's, copied, not approximated — each one names its source:

* ``ML_Place2D`` — MaterialX ``ND_place2d_vector2`` at its defaults (pivot 0, operation
  order 0): ``uv / scale``, then ``rotate2d`` (which turns the COORDINATE clockwise by
  ``uv_rotation`` degrees, so the texture appears counter-clockwise), then ``- offset``.
  Blender's Vector Rotate turns counter-clockwise, so it is given ``-uv_rotation``.
* ``ML_Opaque`` — the Opaque master: ``base_color x base_color_tint`` (the article's
  ``base_color_tinted``), roughness plus each wear layer's bias, then ``+ roughness_bias``
  clamped to 0..1 (LCDSchema), metalness, up to three wear layers gated by the maskset
  (MasterSet §Overlay semantic), and the normal combined in TANGENT space and converted
  once (see ``ensure_opaque``), into a Principled BSDF standing in for
  ``open_pbr_surface`` (both are the OpenPBR model).

Sockets that are Creator ports carry the frozen port name (LCDSchema §Creator subset), so
the Blender exporter reads them as it read the look-alike's.

Textures are sampled OUTSIDE the groups (a node group is shared, an image is per article):
the article loader (``load_article.py``) wires UV -> ML_Place2D -> Image nodes -> master.
"""

from __future__ import annotations

import math

import bpy

VERSION = 2     # bump when a group's contents change; ensure_*() rebuilds an older one


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


OVERLAYS = (1, 2, 3)
GATE_CHANNEL = {1: "G", 2: "B", 3: "A"}     # MasterSet §MaskSet channel contract


def _sep(ng, x, y):
    return _node(ng, "ShaderNodeSeparateColor", x, y)


def ensure_opaque():
    """The Opaque master: base PBR, Creator sliders, and up to three wear layers.

    Per overlay N (MasterSet §Overlay semantic):
        gate_N   = mix(1, maskset.<G|B|A>, maskset_blend)      # MaterialX mix(bg=1, fg, mix)
        effect_N = overlayN_density * overlayN.A * gate_N
        roughness += overlayN.B * effect_N                      # then + roughness_bias, clamp 0..1
        normal    += (overlayN.RG * 2 - 1, 0) * effect_N        # TANGENT space
    The normal is combined in TANGENT space (the article's normal map decoded, or flat
    (0, 0, 1) where it has none), renormalized, and converted to world space ONCE. That is
    the spec's intent; the articles built before Phase05 step 5.3 add the bumps to an
    already-world normal instead (Execution Log F10).
    """
    sockets = [("Base Color", "NodeSocketColor", (0.8, 0.8, 0.8, 1.0)),
               ("base_color_tint", "NodeSocketColor", (1.0, 1.0, 1.0, 1.0)),
               ("Roughness", "NodeSocketFloat", 0.5),
               ("roughness_bias", "NodeSocketFloat", 0.0),
               ("Metalness", "NodeSocketFloat", 0.0),
               ("Normal Map", "NodeSocketColor", (0.5, 0.5, 1.0, 1.0)),
               ("IOR", "NodeSocketFloat", 1.5),
               ("Specular Weight", "NodeSocketFloat", 1.0),
               ("Maskset", "NodeSocketColor", (1.0, 1.0, 1.0, 1.0)),
               ("Maskset Alpha", "NodeSocketFloat", 1.0),
               ("maskset_blend", "NodeSocketFloat", 0.0)]
    for n in OVERLAYS:
        sockets += [(f"Overlay {n}", "NodeSocketColor", (0.5, 0.5, 0.0, 1.0)),
                    (f"Overlay {n} Alpha", "NodeSocketFloat", 0.0),
                    (f"overlay{n}_density", "NodeSocketFloat", 0.0)]
    ng, fresh = _group("ML_Opaque", sockets, [("BSDF", "NodeSocketShader")])
    if not fresh:
        return ng
    L = ng.links.new
    gi = _node(ng, "NodeGroupInput", -1600, 0)
    go = _node(ng, "NodeGroupOutput", 900, 0)
    bsdf = _node(ng, "ShaderNodeBsdfPrincipled", 550, 0)
    L(bsdf.outputs["BSDF"], go.inputs["BSDF"])

    tint = _vmath(ng, "MULTIPLY", -300, 500)                  # base_color_tinted
    L(gi.outputs["Base Color"], tint.inputs[0])
    L(gi.outputs["base_color_tint"], tint.inputs[1])
    L(tint.outputs[0], bsdf.inputs["Base Color"])
    L(gi.outputs["Metalness"], bsdf.inputs["Metallic"])
    L(gi.outputs["IOR"], bsdf.inputs["IOR"])
    spec = _math(ng, "MULTIPLY", -300, 350)                    # 0.5 = "use the IOR as is"
    L(gi.outputs["Specular Weight"], spec.inputs[0])
    spec.inputs[1].default_value = 0.5
    L(spec.outputs[0], bsdf.inputs["Specular IOR Level"])

    mask = _sep(ng, -1300, -200)
    L(gi.outputs["Maskset"], mask.inputs["Color"])
    mask_ch = {"G": mask.outputs["Green"], "B": mask.outputs["Blue"], "A": gi.outputs["Maskset Alpha"]}

    # tangent-space normal: decode the map (2c - 1); flat maps decode to (0, 0, 1)
    dec = _vmath(ng, "MULTIPLY_ADD", -1000, -600)
    L(gi.outputs["Normal Map"], dec.inputs[0])
    dec.inputs[1].default_value = (2.0, 2.0, 2.0)
    dec.inputs[2].default_value = (-1.0, -1.0, -1.0)
    n_src = dec.outputs[0]
    rough_src = gi.outputs["Roughness"]

    for n in OVERLAYS:
        y = -200 - 350 * n
        # gate = 1 + (mask - 1) * blend  ==  mix(bg=1, fg=mask, mix=blend)
        gm = _math(ng, "SUBTRACT", -1000, y)
        L(mask_ch[GATE_CHANNEL[n]], gm.inputs[0])
        gm.inputs[1].default_value = 1.0
        gate = _math(ng, "MULTIPLY_ADD", -800, y)
        L(gm.outputs[0], gate.inputs[0])
        L(gi.outputs["maskset_blend"], gate.inputs[1])
        gate.inputs[2].default_value = 1.0
        e1 = _math(ng, "MULTIPLY", -600, y)
        L(gi.outputs[f"overlay{n}_density"], e1.inputs[0])
        L(gi.outputs[f"Overlay {n} Alpha"], e1.inputs[1])
        eff = _math(ng, "MULTIPLY", -400, y)
        L(e1.outputs[0], eff.inputs[0])
        L(gate.outputs[0], eff.inputs[1])

        ov = _sep(ng, -800, y - 150)
        L(gi.outputs[f"Overlay {n}"], ov.inputs["Color"])
        rd = _math(ng, "MULTIPLY_ADD", -200, y + 100)            # rough += B * effect
        L(ov.outputs["Blue"], rd.inputs[0])
        L(eff.outputs[0], rd.inputs[1])
        L(rough_src, rd.inputs[2])
        rough_src = rd.outputs[0]

        # (R*2-1, G*2-1, 0) * effect, added to the tangent-space normal
        comb = _node(ng, "ShaderNodeCombineXYZ", -600, y - 150)
        for axis, ch in (("X", "Red"), ("Y", "Green")):
            m = _math(ng, "MULTIPLY_ADD", -700, y - 150)
            L(ov.outputs[ch], m.inputs[0])
            m.inputs[1].default_value = 2.0
            m.inputs[2].default_value = -1.0
            L(m.outputs[0], comb.inputs[axis])
        sc = _vmath(ng, "SCALE", -400, y - 150)
        L(comb.outputs[0], sc.inputs[0])
        L(eff.outputs[0], sc.inputs["Scale"])
        add = _vmath(ng, "ADD", -200, y - 150)
        L(n_src, add.inputs[0])
        L(sc.outputs[0], add.inputs[1])
        n_src = add.outputs[0]

    rough = _math(ng, "ADD", 100, 200, clamp=True)             # roughness_biased_clamped
    L(rough_src, rough.inputs[0])
    L(gi.outputs["roughness_bias"], rough.inputs[1])
    L(rough.outputs[0], bsdf.inputs["Roughness"])

    # normalize in tangent space, re-encode, and convert to world space ONCE
    nrm = _vmath(ng, "NORMALIZE", 0, -600)
    L(n_src, nrm.inputs[0])
    enc = _vmath(ng, "MULTIPLY_ADD", 150, -600)
    L(nrm.outputs[0], enc.inputs[0])
    enc.inputs[1].default_value = (0.5, 0.5, 0.5)
    enc.inputs[2].default_value = (0.5, 0.5, 0.5)
    nmap = _node(ng, "ShaderNodeNormalMap", 300, -600, space="TANGENT", uv_map="st")
    L(enc.outputs[0], nmap.inputs["Color"])
    L(nmap.outputs["Normal"], bsdf.inputs["Normal"])
    return ng


MASTERS = {"Opaque": ensure_opaque}


def ensure_all():
    ensure_place2d()
    for fn in MASTERS.values():
        fn()
