"""Build a Blender material for one Matter article, on its master (Phase05).

    import load_article
    mat = load_article.build(Path(".../Copper_Verdigris_Aged_Base_s01_v01.mtlx"),
                             sliders={"roughness_bias": 0.25})

The article is read by ``article.read`` (plain XML, no ``bpy``; the parity rig's Unreal driver
reads it the same way, Phase06). The Creator sliders' start values are the nodegraph's
interface inputs; ``sliders`` overrides them, as a Creator would.
"""

from __future__ import annotations

from pathlib import Path

import bpy

import build_masters
from article import ArticleData, read  # noqa: F401  (ArticleData: kept importable from here)

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
                "maskset_blend", "roughness_bias",
                "overlay1_color", "overlay2_color", "overlay3_color",    # Phase10, RD-P10-1
                "transmission_color",                                    # Phase12, RD-GLC-2
                "emission_color", "emission_luminance")                  # Phase12 12.4
COLOR_TRAVEL_PORTS = {"base_color_tint", "overlay1_color", "overlay2_color", "overlay3_color",
                      "transmission_color", "emission_color"}
DATA_ROLES = ("roughness", "metalness", "normal", "layer2_roughness", "layer2_metalness",
              "layer2_normal", "opacity")


def _rgba(v: list[float]) -> tuple[float, float, float, float]:
    v = list(v) + [1.0] * (4 - len(v))
    return (v[0], v[1], v[2], 1.0)


def build(path: Path, sliders: dict | None = None, name: str | None = None,
          cutout_map: Path | None = None, base_color_map: Path | None = None,
          roughness_map: Path | None = None, normal_map: Path | None = None,
          cavity_map: Path | None = None):
    """A new material for ``path`` with ``sliders`` applied; returns the material.

    ``cutout_map`` is the mesh's cut-out (LCDSchema §Cut-out map), supplied per binding the way
    a USD writer sets the Material's ``inputs:cutout_map``. It is sampled on the mesh's own UVs
    (not the article's placement); with none, the master's Opacity stays 1 (opaque).
    ``base_color_map`` is the mesh's picture (LCDSchema §Base colour map, Phase09), supplied the
    same way and sampled the same way; it multiplies the article's base colour ahead of the
    master, whose own tint (and Hair's light through the card) then acts on the product.
    ``roughness_map`` (Phase22, LCDSchema §Shine maps) is the mesh's roughness offset, linear, on
    the mesh's own UVs: ``roughness + (map - 0.5)``, ahead of the master's bias and clamp.
    ``normal_map`` (22.2) is the mesh's tangent-space relief, its XY added to the article's normal;
    ``cavity_map`` multiplies the specular weight.
    """
    build_masters.ensure_all()
    art = read(path)
    # Phase18 (RD-P18-9): a fitted Character article names its own picture; a binding that
    # supplies one still wins (the Carrier rule), and with neither the article is its own colour
    if base_color_map is None:
        base_color_map = art.maps.get("base_color_map")
    if roughness_map is None:
        roughness_map = art.maps.get("roughness_map")
    if normal_map is None:
        normal_map = art.maps.get("normal_map")
    if cavity_map is None:
        cavity_map = art.maps.get("cavity_map")
    if art.master not in build_masters.MASTERS:
        raise NotImplementedError(f"{art.name}: master {art.master!r} has no Blender version yet")
    ports = dict(art.ports)
    for k, v in (sliders or {}).items():
        if k not in ports:
            raise KeyError(f"{art.name} does not declare the slider {k!r}")
        ports[k] = list(v) if isinstance(v, (list, tuple)) else [float(v)]

    mat = bpy.data.materials.new(name or art.name)
    # The article's id, never its path: a path is the author machine's, and these properties
    # ride into the committed library .blend (F-P10-17). The exporter strips `ml_*` too.
    mat["ml_article"] = art.name
    mat["ml_master"] = art.master
    mat.use_backface_culling = art.master not in build_masters.TWO_SIDED
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

    if base_color_map is not None:
        if "base_color_map" not in art.ports:
            raise KeyError(f"{art.name} does not declare the picture input (base_color_map)")
        img = bpy.data.images.load(str(base_color_map), check_existing=True)
        img.colorspace_settings.name = "sRGB"
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = img
        tex.interpolation = "Linear"
        tex.extension = "REPEAT"
        tex.location = (-300, y)
        L(uv.outputs["UV"], tex.inputs["Vector"])     # the mesh's UVs, unplaced
        sock = master.inputs["Base Color"]
        mul = nt.nodes.new("ShaderNodeMix")           # base_color_mapped: article base x picture
        mul.data_type = "RGBA"
        mul.blend_type = "MULTIPLY"
        mul.clamp_result = False
        mul.inputs["Factor"].default_value = 1.0
        mul.location = (100, y)
        if sock.is_linked:                            # the article's own base texture
            L(sock.links[0].from_socket, mul.inputs["A"])
        else:
            mul.inputs["A"].default_value = tuple(sock.default_value)
        L(tex.outputs["Color"], mul.inputs["B"])
        L(mul.outputs["Result"], sock)
        y -= 300

    if roughness_map is not None:
        if "roughness_map" not in art.ports:
            raise KeyError(f"{art.name} does not declare the shine input (roughness_map)")
        img = bpy.data.images.load(str(roughness_map), check_existing=True)
        img.colorspace_settings.name = "Non-Color"
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = img
        tex.interpolation = "Linear"
        tex.extension = "REPEAT"
        tex.location = (-300, y)
        L(uv.outputs["UV"], tex.inputs["Vector"])     # the mesh's UVs, unplaced
        off = nt.nodes.new("ShaderNodeMath")           # roughness_map_offset: map - 0.5
        off.operation = "SUBTRACT"
        off.inputs[1].default_value = 0.5
        off.location = (0, y)
        L(tex.outputs["Color"], off.inputs[0])
        add = nt.nodes.new("ShaderNodeMath")           # roughness_mapped (the master biases, clamps)
        add.operation = "ADD"
        add.location = (200, y)
        sock = master.inputs["Roughness"]
        if sock.is_linked:                             # the pores' roughness
            L(sock.links[0].from_socket, add.inputs[0])
        else:
            add.inputs[0].default_value = sock.default_value
        L(off.outputs["Value"], add.inputs[1])
        L(add.outputs["Value"], sock)
        y -= 300

    def _mesh_map(port: str, file: Path):
        """A shine map's image node, linear, on the mesh's UVs (unplaced)."""
        if port not in art.ports:
            raise KeyError(f"{art.name} does not declare the shine input ({port})")
        img = bpy.data.images.load(str(file), check_existing=True)
        img.colorspace_settings.name = "Non-Color"
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = img
        tex.interpolation = "Linear"
        tex.extension = "REPEAT"
        tex.location = (-300, y)
        L(uv.outputs["UV"], tex.inputs["Vector"])
        return tex

    def _vec(op: str, x: int, b=None):
        n = nt.nodes.new("ShaderNodeVectorMath")
        n.operation = op
        n.location = (x, y)
        if b is not None:
            n.inputs[1].default_value = b
        return n

    if normal_map is not None:
        # Phase22 22.2 (RD-P22-5): the mesh's relief, tangent space. The master decodes its Normal
        # Map colour (2c - 1), adds the overlays and normalises once; so the body's XY is added to
        # the article's own here and re-encoded, unclamped (c = n/2 + 1/2), as the graph does.
        tex = _mesh_map("normal_map", normal_map)
        sock = master.inputs["Normal Map"]
        own = _vec("MULTIPLY_ADD", 0)
        own.inputs[1].default_value = (2.0, 2.0, 2.0)
        own.inputs[2].default_value = (-1.0, -1.0, -1.0)
        if sock.is_linked:                             # the pores' normal
            L(sock.links[0].from_socket, own.inputs[0])
        else:
            own.inputs[0].default_value = tuple(sock.default_value)[:3]
        body = _vec("MULTIPLY_ADD", 0)
        body.inputs[1].default_value = (2.0, 2.0, 0.0)  # its XY only
        body.inputs[2].default_value = (-1.0, -1.0, 0.0)
        L(tex.outputs["Color"], body.inputs[0])
        add = _vec("ADD", 200)
        L(own.outputs[0], add.inputs[0])
        L(body.outputs[0], add.inputs[1])
        enc = _vec("MULTIPLY_ADD", 400)
        enc.inputs[1].default_value = (0.5, 0.5, 0.5)
        enc.inputs[2].default_value = (0.5, 0.5, 0.5)
        L(add.outputs[0], enc.inputs[0])
        L(enc.outputs[0], sock)
        y -= 300
        if "coat_weight" in art.shader and "Coat Follows Normal" in master.inputs:
            master.inputs["Coat Follows Normal"].default_value = 1.0   # the sebum follows the relief

    if cavity_map is not None:
        # RD-P22-6: specular_weight x the cavity map. The article's own specular_weight is set on
        # the socket below; this multiplies the map into whatever reaches it (1 when unset).
        tex = _mesh_map("cavity_map", cavity_map)
        mul = nt.nodes.new("ShaderNodeMath")
        mul.operation = "MULTIPLY"
        mul.location = (200, y)
        L(tex.outputs["Color"], mul.inputs[0])
        cavity_weight = mul
        L(mul.outputs["Value"], master.inputs["Specular Weight"])
        y -= 300
    else:
        cavity_weight = None

    # Phase09 (F-P09-5): a Subsurface article whose subsurface_color is CONNECTED to its base
    # (no value on the shader: the assembler wires it to base_color_out) scatters the base's own
    # colour, the picture included. ML_Subsurface tints its Base Color inside the master but takes
    # Subsurface Color as given, so a tinted article's scatter is tinted HERE, by the same port
    # (Phase21 RD-P21-4, F-P21-3: the assembler connects subsurface_color to base_color_out, which
    # is after the tint, so Storm's scatter follows the tint; this was refused until then, F-SKM-23).
    follow_tint = None
    if (art.master == "Subsurface" and "subsurface_weight" in art.shader
            and "subsurface_color" not in art.shader and "Subsurface Color" in master.inputs):
        bsock, ssock = master.inputs["Base Color"], master.inputs["Subsurface Color"]
        if "base_color_tint" in ports:
            follow_tint = nt.nodes.new("ShaderNodeMix")    # base x the tint (wired to the port below)
            follow_tint.data_type = "RGBA"
            follow_tint.blend_type = "MULTIPLY"
            follow_tint.clamp_result = False
            follow_tint.inputs["Factor"].default_value = 1.0
            follow_tint.location = (300, -400)
            if bsock.is_linked:
                L(bsock.links[0].from_socket, follow_tint.inputs["A"])
            else:
                follow_tint.inputs["A"].default_value = tuple(bsock.default_value)
            L(follow_tint.outputs["Result"], ssock)
        elif bsock.is_linked:
            L(bsock.links[0].from_socket, ssock)
        else:
            ssock.default_value = tuple(bsock.default_value)

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
    # Phase10: a slot is a DEPOSIT exactly when the article declares its colour port; its cover
    # is switched on and the Creator's colour set (MasterSet §Overlay semantic)
    for n in build_masters.OVERLAYS:
        if f"overlay{n}_color" in ports:
            master.inputs[f"overlay{n}_color"].default_value = _rgba(ports[f"overlay{n}_color"])
            master.inputs[f"Overlay {n} Deposit"].default_value = 1.0

    if "base_color_tint" in ports:
        master.inputs["base_color_tint"].default_value = _rgba(ports["base_color_tint"])
    if "roughness_bias" in ports:
        master.inputs["roughness_bias"].default_value = ports["roughness_bias"][0]
    if "specular_ior" in art.shader:
        master.inputs["IOR"].default_value = art.shader["specular_ior"][0]
    if cavity_weight is not None:
        cavity_weight.inputs[1].default_value = art.shader.get("specular_weight", [1.0])[0]
    elif "specular_weight" in art.shader:
        master.inputs["Specular Weight"].default_value = art.shader["specular_weight"][0]
    if "base_weight" in art.shader and art.shader["base_weight"][0] != 1.0:
        raise NotImplementedError(f"{art.name}: base_weight != 1 is not mapped yet")

    # author-tier ports (lane B) and lane-A shader values, wherever the master has the socket
    for port in ("layer_blend_balance", "layer_blend_contrast", "opacity_cutoff"):
        if port in ports and port in master.inputs:
            master.inputs[port].default_value = ports[port][0]
    sh = art.shader
    lane_a = {"emission_color": ("emission_color", _rgba), "emission_luminance": ("emission_luminance", None),
              "transmission_weight": ("Transmission Weight", None),
              "transmission_color": ("transmission_color", _rgba),
              "subsurface_weight": ("Subsurface Weight", None), "subsurface_color": ("Subsurface Color", _rgba),
              "subsurface_radius": ("Subsurface Radius", None),
              "subsurface_radius_scale": ("Subsurface Radius Scale", tuple),
              "subsurface_scatter_anisotropy": ("Subsurface Anisotropy", None),
              "coat_weight": ("Coat Weight", None), "coat_color": ("Coat Color", _rgba),
              "coat_roughness": ("Coat Roughness", None), "coat_ior": ("Coat IOR", None),
              "coat_darkening": ("Coat Darkening", None),
              "fuzz_weight": ("Fuzz Weight", None), "fuzz_color": ("Fuzz Color", _rgba),
              "fuzz_roughness": ("Fuzz Roughness", None),
              "specular_roughness_anisotropy": ("Anisotropy", None)}
    for key, (socket, conv) in lane_a.items():
        if key in sh and socket in master.inputs:
            master.inputs[socket].default_value = conv(sh[key]) if conv else sh[key][0]
    if "Transmission Depth" in master.inputs:
        # OpenPBR thick: transmission_color is what is left after transmission_depth of travel
        # (Beer-Lambert). ML_TranslucentThick works the absorption out itself from its
        # `transmission_color` socket (set above, and a Creator port where the article declares
        # it) and this depth (Phase12 12.3, masters v10; it was summed here until then, which
        # left the socket white and the colour fixed at load).
        master.inputs["Transmission Depth"].default_value = sh.get("transmission_depth", [0.0])[0]
        L(master.outputs["Volume"], out.inputs["Volume"])
    if "geometry_thin_walled" in sh:
        thin = sh["geometry_thin_walled"][0] > 0.5
        want = art.master == "TranslucentThin"
        if art.master.startswith("Translucent") and thin != want:
            raise ValueError(f"{art.name}: geometry_thin_walled={thin} contradicts master {art.master}")

    # the Creator travel ports: exposed on the wrapper, defaulting to the ARTICLE's values
    travel = [p for p in TRAVEL_PORTS if p in art.ports and p in master.inputs]
    for p in travel:
        is_color = p in COLOR_TRAVEL_PORTS
        s = wrap.interface.new_socket(name=p, in_out="INPUT",
                                      socket_type="NodeSocketColor" if is_color else "NodeSocketFloat")
        s.default_value = _rgba(art.ports[p]) if is_color else art.ports[p][0]
        L(gin.outputs[p], master.inputs[p])
        if p == "base_color_tint" and follow_tint is not None:
            L(gin.outputs[p], follow_tint.inputs["B"])     # the scatter takes the Creator's tint too

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
        node.inputs[p].default_value = _rgba(ports[p]) if p in COLOR_TRAVEL_PORTS else ports[p][0]
    return mat
