"""Blender versions of the Matter masters, built by code (Phase05).

Run inside Blender (``import build_masters; build_masters.ensure_all()``). Every group is
get-or-create, so calling it twice is harmless.

The formulas are MaterialX's, copied, not approximated — each one names its source:

* ``ML_Place2D`` — MaterialX ``ND_place2d_vector2`` at its defaults (pivot 0, operation
  order 0): ``uv / scale``, then ``rotate2d`` (which turns the COORDINATE clockwise by
  ``uv_rotation`` degrees, so the texture appears counter-clockwise), then ``- offset``.
  Blender's Vector Rotate turns counter-clockwise, so it is given ``-uv_rotation``.
* ``ML_<Master>`` — one group per master (MasterSet §v1 baseline), all built on the same
  Opaque core (``_build``), with the master's own part switched on:

  ========================  ==========================================================
  Opaque                    the core: ``base_color`` (x ``base_color_tint``); roughness
                            + each wear layer's bias + ``roughness_bias``, clamped 0..1
                            (LCDSchema); metalness; up to three wear layers gated by the
                            maskset (MasterSet §Overlay semantic); the normal combined in
                            TANGENT space and converted once (MasterSet, since 5.3);
                            OpenPBR coat (-> Coat) and fuzz (-> Sheen), off at weight 0;
                            specular anisotropy along the UV tangent, off at 0
  TwoLayer                 + a second layer blended by the maskset's R (MasterSet
                            §TwoLayer blend): colour, roughness and metalness mixed, the
                            two normals mixed in tangent space; the tint applies after
  Masked                    + the cut-out: alpha = opacity >= ``opacity_cutoff`` (the
                            article's ``ifgreatereq``)
  Hair                      (Phase08 8.1) the mesh's cut-out as SOFT coverage (no cutoff),
                            and OpenPBR's thin-walled subsurface, copied from MaterialX's
                            graph: with c = the tinted base colour, w = subsurface weight,
                            a = scatter anisotropy, the diffuse becomes
                            lerp(base, c*c*(1-a)/2, w) and a Translucent BSDF of colour
                            w*c*c*(1+a)/2 is added (MaterialX applies c twice: as the
                            BSDF's colour and as its factor). The one approximation: the
                            Translucent lobe sits beside Principled, not under its
                            specular layer, so it is not dimmed by the specular's Fresnel
  Emissive                  + emission: colour x luminance (MaterialX's OpenPBR takes
                            luminance as radiance directly, as Blender's Strength is)
  TranslucentThin           + transmission, Thin Wall on; the tint of what shows through
                            is ``transmission_color``
  TranslucentThick          + transmission, Thin Wall off, and absorption inside the
                            volume: sigma = -ln(transmission_color) / transmission_depth
  Subsurface                + subsurface weight, radius, radius scale and scatter
                            anisotropy; the Cycles method is ``SUBSURFACE_METHOD``
  ========================  ==========================================================

  A Principled BSDF stands in for ``open_pbr_surface`` (both are the OpenPBR model). Two
  places where Principled has one colour where OpenPBR has two, and the mapping used:
  transmission is tinted by Base Color, so Base Color = lerp(base, transmission tint,
  transmission_weight); and subsurface uses Base Color, so Base Color = lerp(base,
  subsurface_color, subsurface_weight). Each is exact at weight 0 and at weight 1.

Sockets that are Creator ports carry the frozen port name (LCDSchema §Creator subset), so
the Blender exporter reads them as it read the look-alike's.

Textures are sampled OUTSIDE the groups (a node group is shared, an image is per article):
the article loader (``load_article.py``) wires UV -> ML_Place2D -> Image nodes -> master.
"""

from __future__ import annotations

import math

import bpy

VERSION = 8     # bump when a group's contents change; ensure_*() rebuilds an older one
#               (8: Phase10, a deposit overlay covers the surface in its colour)
                # 5 (Phase07 7.3): coat, fuzz, subsurface anisotropy and method
                # 6 (Phase07 7.6): specular anisotropy (carrier C3) on the UV tangent
                # 7 (Phase08 8.1): ML_Hair's own part (soft coverage, light through)

# The Subsurface master's Cycles method (Phase07 CM-Q10, measured 2026-09-27 in the rig, ΔE
# to Storm, whole set): RANDOM_WALK_SKIN serves marble AND skin better than RANDOM_WALK
# (Blender's default, implicit through Phase05): Marble 2.60 -> 1.82, Skin III 5.64 -> 3.46,
# Skin I 6.99 -> 3.10 (under RANDOM_WALK its forward scatter turned a light skin grey-green).
# One setting serves both, so no `Skin` master token (Learnings Blender B8).
SUBSURFACE_METHOD = "RANDOM_WALK_SKIN"

OVERLAYS = (1, 2, 3)
GATE_CHANNEL = {1: "G", 2: "B", 3: "A"}     # MasterSet §MaskSet channel contract
DUST_RGBA = (0.413, 0.386, 0.308, 1.0)       # the assembler's DUST_COLOR (linear), Phase10

# master -> the parts it switches on over the Opaque core
MASTER_PARTS = {
    "Opaque": set(),
    "TwoLayer": {"layer2"},
    "Masked": {"opacity"},
    "Hair": {"hair"},               # soft coverage + thin-walled translucency (Phase08 8.1)
    "Emissive": {"emission"},
    "TranslucentThin": {"transmission"},
    "TranslucentThick": {"transmission", "thick"},
    "Subsurface": {"subsurface"},
}


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


def _sep(ng, x, y):
    return _node(ng, "ShaderNodeSeparateColor", x, y)


def _lerp_color(ng, a, b, t, x, y):
    """a + (b - a) * t for colours (as vectors)."""
    d = _vmath(ng, "SUBTRACT", x, y)
    ng.links.new(b, d.inputs[0])
    ng.links.new(a, d.inputs[1])
    s = _vmath(ng, "SCALE", x + 150, y)
    ng.links.new(d.outputs[0], s.inputs[0])
    ng.links.new(t, s.inputs["Scale"])
    add = _vmath(ng, "ADD", x + 300, y)
    ng.links.new(a, add.inputs[0])
    ng.links.new(s.outputs[0], add.inputs[1])
    return add.outputs[0]


def _lerp_float(ng, a, b, t, x, y):
    m = _node(ng, "ShaderNodeMix", x, y, data_type="FLOAT")
    ng.links.new(t, m.inputs["Factor"])
    ng.links.new(a, m.inputs[2])      # A (float)
    ng.links.new(b, m.inputs[3])      # B (float)
    return m.outputs[0]               # Result (float)


def _decode(ng, color, x, y):
    """A normal-map colour -> a tangent-space vector (2c - 1)."""
    d = _vmath(ng, "MULTIPLY_ADD", x, y)
    ng.links.new(color, d.inputs[0])
    d.inputs[1].default_value = (2.0, 2.0, 2.0)
    d.inputs[2].default_value = (-1.0, -1.0, -1.0)
    return d.outputs[0]


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


def _sockets(parts: set) -> list:
    s = [("Base Color", "NodeSocketColor", (0.8, 0.8, 0.8, 1.0)),
         ("base_color_tint", "NodeSocketColor", (1.0, 1.0, 1.0, 1.0)),
         ("Roughness", "NodeSocketFloat", 0.5),
         ("roughness_bias", "NodeSocketFloat", 0.0),
         ("Metalness", "NodeSocketFloat", 0.0),
         ("Normal Map", "NodeSocketColor", (0.5, 0.5, 1.0, 1.0)),
         ("IOR", "NodeSocketFloat", 1.5),
         ("Specular Weight", "NodeSocketFloat", 1.0),
         ("Maskset", "NodeSocketColor", (1.0, 1.0, 1.0, 1.0)),
         ("Maskset Alpha", "NodeSocketFloat", 1.0),
         ("maskset_blend", "NodeSocketFloat", 0.0),
         # OpenPBR coat and fuzz (Phase07 7.3), at OpenPBR's defaults: off at weight 0
         ("Coat Weight", "NodeSocketFloat", 0.0),
         ("Coat Color", "NodeSocketColor", (1.0, 1.0, 1.0, 1.0)),
         ("Coat Roughness", "NodeSocketFloat", 0.0),
         ("Coat IOR", "NodeSocketFloat", 1.6),
         ("Fuzz Weight", "NodeSocketFloat", 0.0),
         ("Fuzz Color", "NodeSocketColor", (1.0, 1.0, 1.0, 1.0)),
         ("Fuzz Roughness", "NodeSocketFloat", 0.5),
         # OpenPBR specular_roughness_anisotropy (Phase07 7.6, carrier C3), off at 0
         ("Anisotropy", "NodeSocketFloat", 0.0)]
    for n in OVERLAYS:
        s += [(f"Overlay {n}", "NodeSocketColor", (0.5, 0.5, 0.0, 1.0)),
              (f"Overlay {n} Alpha", "NodeSocketFloat", 0.0),
              (f"overlay{n}_density", "NodeSocketFloat", 0.0),
              # Phase10: the Creator's deposit colour, and whether this slot IS a deposit (set by
              # the loader from the article; 0 = a damage or gloss layer, which never covers)
              (f"overlay{n}_color", "NodeSocketColor", DUST_RGBA),
              (f"Overlay {n} Deposit", "NodeSocketFloat", 0.0)]
    if "layer2" in parts:
        s += [("Layer 2 Base Color", "NodeSocketColor", (0.5, 0.5, 0.5, 1.0)),
              ("Layer 2 Roughness", "NodeSocketFloat", 0.5),
              ("Layer 2 Metalness", "NodeSocketFloat", 0.0),
              ("Layer 2 Normal Map", "NodeSocketColor", (0.5, 0.5, 1.0, 1.0)),
              ("layer_blend_balance", "NodeSocketFloat", 0.5),
              ("layer_blend_contrast", "NodeSocketFloat", 0.0)]
    if "opacity" in parts:
        s += [("Opacity", "NodeSocketFloat", 1.0),
              ("opacity_cutoff", "NodeSocketFloat", 0.5)]
    if "hair" in parts:
        s += [("Opacity", "NodeSocketFloat", 1.0),
              ("Subsurface Weight", "NodeSocketFloat", 0.0),
              ("Subsurface Anisotropy", "NodeSocketFloat", 0.0)]
    if "emission" in parts:
        s += [("Emission Color", "NodeSocketColor", (1.0, 1.0, 1.0, 1.0)),
              ("Emission Luminance", "NodeSocketFloat", 0.0)]
    if "transmission" in parts:
        s += [("Transmission Weight", "NodeSocketFloat", 0.0),
              ("Transmission Color", "NodeSocketColor", (1.0, 1.0, 1.0, 1.0))]
    if "thick" in parts:
        s += [("Absorption", "NodeSocketVector", (0.0, 0.0, 0.0))]
    if "subsurface" in parts:
        s += [("Subsurface Weight", "NodeSocketFloat", 0.0),
              ("Subsurface Color", "NodeSocketColor", (0.8, 0.8, 0.8, 1.0)),
              ("Subsurface Radius", "NodeSocketFloat", 1.0),
              ("Subsurface Radius Scale", "NodeSocketVector", (1.0, 1.0, 1.0)),
              ("Subsurface Anisotropy", "NodeSocketFloat", 0.0)]
    return s


def _build(name: str, parts: set):
    outs = [("BSDF", "NodeSocketShader")] + ([("Volume", "NodeSocketShader")] if "thick" in parts else [])
    ng, fresh = _group(name, _sockets(parts), outs)
    if not fresh:
        return ng
    L = ng.links.new
    gi = _node(ng, "NodeGroupInput", -2000, 0)
    go = _node(ng, "NodeGroupOutput", 1200, 0)
    bsdf = _node(ng, "ShaderNodeBsdfPrincipled", 850, 0)
    L(bsdf.outputs["BSDF"], go.inputs["BSDF"])
    L(gi.outputs["IOR"], bsdf.inputs["IOR"])
    spec = _math(ng, "MULTIPLY", 500, 350)                     # 0.5 = "use the IOR as is"
    L(gi.outputs["Specular Weight"], spec.inputs[0])
    spec.inputs[1].default_value = 0.5
    L(spec.outputs[0], bsdf.inputs["Specular IOR Level"])

    mask = _sep(ng, -1700, -200)
    L(gi.outputs["Maskset"], mask.inputs["Color"])
    mask_ch = {"R": mask.outputs["Red"], "G": mask.outputs["Green"], "B": mask.outputs["Blue"],
               "A": gi.outputs["Maskset Alpha"]}

    base = gi.outputs["Base Color"]
    rough = gi.outputs["Roughness"]
    metal = gi.outputs["Metalness"]
    n_ts = _decode(ng, gi.outputs["Normal Map"], -1400, -700)

    if "layer2" in parts:
        # MasterSet §TwoLayer blend: c = 1/max(1e-4, 1-contrast); k = saturate((R-bal)*c+.5)
        inv = _math(ng, "SUBTRACT", -1700, 700)
        inv.inputs[0].default_value = 1.0
        L(gi.outputs["layer_blend_contrast"], inv.inputs[1])
        safe = _math(ng, "MAXIMUM", -1550, 700)
        L(inv.outputs[0], safe.inputs[0])
        safe.inputs[1].default_value = 1e-4
        cen = _math(ng, "SUBTRACT", -1550, 850)
        L(mask_ch["R"], cen.inputs[0])
        L(gi.outputs["layer_blend_balance"], cen.inputs[1])
        scl = _math(ng, "DIVIDE", -1400, 800)
        L(cen.outputs[0], scl.inputs[0])
        L(safe.outputs[0], scl.inputs[1])
        k = _math(ng, "ADD", -1250, 800, clamp=True)
        L(scl.outputs[0], k.inputs[0])
        k.inputs[1].default_value = 0.5
        t = _math(ng, "MULTIPLY", -1100, 800)
        L(k.outputs[0], t.inputs[0])
        L(gi.outputs["maskset_blend"], t.inputs[1])
        tt = t.outputs[0]
        base = _lerp_color(ng, base, gi.outputs["Layer 2 Base Color"], tt, -900, 600)
        rough = _lerp_float(ng, rough, gi.outputs["Layer 2 Roughness"], tt, -900, 400)
        metal = _lerp_float(ng, metal, gi.outputs["Layer 2 Metalness"], tt, -900, 250)
        n2 = _decode(ng, gi.outputs["Layer 2 Normal Map"], -1400, -900)
        nb = _lerp_color(ng, n_ts, n2, tt, -1200, -800)
        nn = _vmath(ng, "NORMALIZE", -800, -800)
        L(nb, nn.inputs[0])
        n_ts = nn.outputs[0]

    tint = _vmath(ng, "MULTIPLY", -300, 600)                  # base_color_tinted (after layer 2)
    L(base, tint.inputs[0])
    L(gi.outputs["base_color_tint"], tint.inputs[1])
    base = tint.outputs[0]

    keep = None    # Phase10: 1 - each deposit's cover, multiplied: what a deposit leaves visible
    for n in OVERLAYS:
        y = -300 - 350 * n
        gm = _math(ng, "SUBTRACT", -1100, y)                   # gate = mix(1, mask, blend)
        L(mask_ch[GATE_CHANNEL[n]], gm.inputs[0])
        gm.inputs[1].default_value = 1.0
        gate = _math(ng, "MULTIPLY_ADD", -950, y)
        L(gm.outputs[0], gate.inputs[0])
        L(gi.outputs["maskset_blend"], gate.inputs[1])
        gate.inputs[2].default_value = 1.0
        e1 = _math(ng, "MULTIPLY", -800, y)
        L(gi.outputs[f"overlay{n}_density"], e1.inputs[0])
        L(gi.outputs[f"Overlay {n} Alpha"], e1.inputs[1])
        eff = _math(ng, "MULTIPLY", -650, y)
        L(e1.outputs[0], eff.inputs[0])
        L(gate.outputs[0], eff.inputs[1])
        ov = _sep(ng, -950, y - 150)
        L(gi.outputs[f"Overlay {n}"], ov.inputs["Color"])
        rd = _math(ng, "MULTIPLY_ADD", -450, y + 100)          # rough += B * effect
        L(ov.outputs["Blue"], rd.inputs[0])
        L(eff.outputs[0], rd.inputs[1])
        L(rough, rd.inputs[2])
        rough = rd.outputs[0]
        comb = _node(ng, "ShaderNodeCombineXYZ", -650, y - 150)
        for axis, ch in (("X", "Red"), ("Y", "Green")):
            m = _math(ng, "MULTIPLY_ADD", -800, y - 150)
            L(ov.outputs[ch], m.inputs[0])
            m.inputs[1].default_value = 2.0
            m.inputs[2].default_value = -1.0
            L(m.outputs[0], comb.inputs[axis])
        sc = _vmath(ng, "SCALE", -450, y - 150)
        L(comb.outputs[0], sc.inputs[0])
        L(eff.outputs[0], sc.inputs["Scale"])
        add = _vmath(ng, "ADD", -300, y - 150)
        L(n_ts, add.inputs[0])
        L(sc.outputs[0], add.inputs[1])
        n_ts = add.outputs[0]
        # Phase10 (MasterSet §Overlay semantic): a deposit COVERS: cover = effect x deposit;
        # the base colour goes to the deposit's colour (after the tint), and every layer under
        # it is hidden by (1 - cover). A slot that is not a deposit has cover 0: unchanged.
        cov = _math(ng, "MULTIPLY", -450, y + 220)
        L(eff.outputs[0], cov.inputs[0])
        L(gi.outputs[f"Overlay {n} Deposit"], cov.inputs[1])
        base = _lerp_color(ng, base, gi.outputs[f"overlay{n}_color"], cov.outputs[0], -300, y + 300)
        left = _math(ng, "SUBTRACT", -300, y + 220)
        left.inputs[0].default_value = 1.0
        L(cov.outputs[0], left.inputs[1])
        if keep is None:
            keep = left.outputs[0]
        else:
            k2 = _math(ng, "MULTIPLY", -150, y + 220)
            L(keep, k2.inputs[0])
            L(left.outputs[0], k2.inputs[1])
            keep = k2.outputs[0]

    def hidden(sock, x, y):
        """A weight under the deposits: weight x keep (= mix(weight, 0, cover), per deposit)."""
        m = _math(ng, "MULTIPLY", x, y)
        L(sock, m.inputs[0])
        L(keep, m.inputs[1])
        return m.outputs[0]

    L(hidden(metal, 0, 300), bsdf.inputs["Metallic"])

    rc = _math(ng, "ADD", 200, 200, clamp=True)                # roughness_biased_clamped
    L(rough, rc.inputs[0])
    L(gi.outputs["roughness_bias"], rc.inputs[1])

    # OpenPBR anisotropy -> Principled (Phase07 7.6). OpenPBR: at = r^2 sqrt(2 / (1 + (1-a)^2)),
    # ab = (1-a) at. Principled (Disney 2012): aspect = sqrt(1 - 0.9 a'), ax = r'^2 / aspect,
    # ay = r'^2 aspect. Same axis ratio: a' = a / 0.9 (exact up to a = 0.9, clamped past it).
    # Same lobe area (ax ay = at ab): r' = r (2 (1-a) / (1 + (1-a)^2))^(1/4), which is r at a = 0,
    # so an isotropic article is untouched. Both elongate along the tangent: OpenPBR's default
    # is Tworld (from texcoord 0), so the tangent is the UV map's, not Principled's default
    # (the object's radial "generated" tangent).
    an = gi.outputs["Anisotropy"]
    om = _math(ng, "SUBTRACT", 200, 60, clamp=True)           # 1 - a
    om.inputs[0].default_value = 1.0
    L(an, om.inputs[1])
    sq = _math(ng, "MULTIPLY", 330, 20)                        # (1-a)^2
    L(om.outputs[0], sq.inputs[0])
    L(om.outputs[0], sq.inputs[1])
    den = _math(ng, "ADD", 460, 20)                            # 1 + (1-a)^2
    den.inputs[0].default_value = 1.0
    L(sq.outputs[0], den.inputs[1])
    num = _math(ng, "MULTIPLY", 330, 100)                      # 2 (1-a)
    num.inputs[0].default_value = 2.0
    L(om.outputs[0], num.inputs[1])
    q = _math(ng, "DIVIDE", 590, 60)
    L(num.outputs[0], q.inputs[0])
    L(den.outputs[0], q.inputs[1])
    f = _math(ng, "POWER", 720, 60)
    L(q.outputs[0], f.inputs[0])
    f.inputs[1].default_value = 0.25
    rr = _math(ng, "MULTIPLY", 720, 200)
    L(rc.outputs[0], rr.inputs[0])
    L(f.outputs[0], rr.inputs[1])
    L(rr.outputs[0], bsdf.inputs["Roughness"])
    ap = _math(ng, "DIVIDE", 590, -60, clamp=True)
    L(an, ap.inputs[0])
    ap.inputs[1].default_value = 0.9
    L(ap.outputs[0], bsdf.inputs["Anisotropic"])
    tan = _node(ng, "ShaderNodeTangent", 590, -180, direction_type="UV_MAP", uv_map="")
    L(tan.outputs["Tangent"], bsdf.inputs["Tangent"])

    nrm = _vmath(ng, "NORMALIZE", 0, -700)                     # tangent -> world, ONCE
    L(n_ts, nrm.inputs[0])
    enc = _vmath(ng, "MULTIPLY_ADD", 150, -700)
    L(nrm.outputs[0], enc.inputs[0])
    enc.inputs[1].default_value = (0.5, 0.5, 0.5)
    enc.inputs[2].default_value = (0.5, 0.5, 0.5)
    # uv_map "" = the mesh's ACTIVE UV map: a Blender mesh names it "UVMap", a USD import "st",
    # and a named map the mesh lacks gives Cycles zero UVs (tangents), silently
    nmap = _node(ng, "ShaderNodeNormalMap", 300, -700, space="TANGENT", uv_map="")
    L(enc.outputs[0], nmap.inputs["Color"])
    L(nmap.outputs["Normal"], bsdf.inputs["Normal"])

    # OpenPBR coat -> Principled Coat (coat_color = Coat Tint: both tint what lies under the
    # coat). Coat Normal stays unlinked = the geometry normal, as OpenPBR's
    # geometry_coat_normal defaults to it. OpenPBR fuzz -> Principled Sheen (both a layer of
    # fine fibres over the rest, lit at grazing angles), on the base's normal as fuzz is.
    for sock, pin in (("Coat Weight", "Coat Weight"), ("Coat Color", "Coat Tint"),
                      ("Coat Roughness", "Coat Roughness"), ("Coat IOR", "Coat IOR"),
                      ("Fuzz Weight", "Sheen Weight"), ("Fuzz Color", "Sheen Tint"),
                      ("Fuzz Roughness", "Sheen Roughness")):
        src = gi.outputs[sock]
        if sock in ("Coat Weight", "Fuzz Weight"):             # a deposit hides coat and fibres
            src = hidden(src, 600, -350 if sock == "Coat Weight" else -450)
        L(src, bsdf.inputs[pin])

    if "opacity" in parts:
        # the article's ifgreatereq: opacity >= cutoff -> 1, else 0  (== 1 - (opacity < cutoff))
        lt = _math(ng, "LESS_THAN", 300, 450)
        L(gi.outputs["Opacity"], lt.inputs[0])
        L(gi.outputs["opacity_cutoff"], lt.inputs[1])
        a = _math(ng, "SUBTRACT", 450, 450)
        a.inputs[0].default_value = 1.0
        L(lt.outputs[0], a.inputs[1])
        L(a.outputs[0], bsdf.inputs["Alpha"])
    if "emission" in parts:
        L(gi.outputs["Emission Color"], bsdf.inputs["Emission Color"])
        L(gi.outputs["Emission Luminance"], bsdf.inputs["Emission Strength"])
    if "transmission" in parts:
        tw = hidden(gi.outputs["Transmission Weight"], -150, 900)   # dust lets no light through
        L(tw, bsdf.inputs["Transmission Weight"])
        bsdf.inputs["Thin Wall"].default_value = "thick" not in parts
        base = _lerp_color(ng, base, gi.outputs["Transmission Color"], tw, 0, 800)
    if "thick" in parts:
        vol = _node(ng, "ShaderNodeVolumeCoefficients", 850, -500)
        L(gi.outputs["Absorption"], vol.inputs["Absorption Coefficients"])
        vol.inputs["Scatter Coefficients"].default_value = (0.0, 0.0, 0.0)
        L(vol.outputs[0], go.inputs["Volume"])
    if "subsurface" in parts:
        sw = hidden(gi.outputs["Subsurface Weight"], -150, 900)    # dust does not scatter light in
        L(sw, bsdf.inputs["Subsurface Weight"])
        L(gi.outputs["Subsurface Radius Scale"], bsdf.inputs["Subsurface Radius"])
        L(gi.outputs["Subsurface Radius"], bsdf.inputs["Subsurface Scale"])
        L(gi.outputs["Subsurface Anisotropy"], bsdf.inputs["Subsurface Anisotropy"])
        bsdf.subsurface_method = SUBSURFACE_METHOD
        base = _lerp_color(ng, base, gi.outputs["Subsurface Color"], sw, 0, 800)
    if "hair" in parts:
        # OpenPBR thin-walled subsurface (MaterialX open_pbr_surface.mtlx, "Subsurface
        # (thin-walled)"): mix(reflection, transmission, 0.5), each lobe coloured c and
        # factored c(1 -/+ a); subsurface_color = the tinted base (the Hair graph's rule)
        c2 = _vmath(ng, "MULTIPLY", 0, 1000)
        L(base, c2.inputs[0])
        L(base, c2.inputs[1])
        w = gi.outputs["Subsurface Weight"]
        an_ss = gi.outputs["Subsurface Anisotropy"]
        rf = _math(ng, "SUBTRACT", 0, 1150)                    # (1 - a) / 2
        rf.inputs[0].default_value = 1.0
        L(an_ss, rf.inputs[1])
        rh = _math(ng, "MULTIPLY", 150, 1150)
        L(rf.outputs[0], rh.inputs[0])
        rh.inputs[1].default_value = 0.5
        refl = _vmath(ng, "SCALE", 300, 1100)
        L(c2.outputs[0], refl.inputs[0])
        L(rh.outputs[0], refl.inputs["Scale"])
        tf = _math(ng, "ADD", 0, 1300)                         # w (1 + a) / 2
        tf.inputs[0].default_value = 1.0
        L(an_ss, tf.inputs[1])
        th = _math(ng, "MULTIPLY", 150, 1300)
        L(tf.outputs[0], th.inputs[0])
        L(w, th.inputs[1])
        th2 = _math(ng, "MULTIPLY", 300, 1300)
        L(th.outputs[0], th2.inputs[0])
        th2.inputs[1].default_value = 0.5
        trans = _vmath(ng, "SCALE", 450, 1250)
        L(c2.outputs[0], trans.inputs[0])
        L(th2.outputs[0], trans.inputs["Scale"])
        base = _lerp_color(ng, base, refl.outputs[0], w, 450, 1050)
        tl = _node(ng, "ShaderNodeBsdfTranslucent", 850, 500)
        L(trans.outputs[0], tl.inputs["Color"])
        add = _node(ng, "ShaderNodeAddShader", 1000, 300)
        L(bsdf.outputs["BSDF"], add.inputs[0])
        L(tl.outputs["BSDF"], add.inputs[1])
        clear = _node(ng, "ShaderNodeBsdfTransparent", 1000, 450)
        cover = _node(ng, "ShaderNodeMixShader", 1100, 200)    # soft coverage: no cutoff
        L(gi.outputs["Opacity"], cover.inputs["Fac"])
        L(clear.outputs["BSDF"], cover.inputs[1])
        L(add.outputs["Shader"], cover.inputs[2])
        L(cover.outputs["Shader"], go.inputs["BSDF"])
    L(base, bsdf.inputs["Base Color"])
    return ng


MASTERS = {m: (lambda m=m: _build(f"ML_{m}", MASTER_PARTS[m])) for m in MASTER_PARTS}


def ensure_opaque():
    return MASTERS["Opaque"]()


def ensure_all():
    ensure_place2d()
    for fn in MASTERS.values():
        fn()
