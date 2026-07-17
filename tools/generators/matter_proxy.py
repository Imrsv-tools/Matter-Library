"""Phase 60sq1 Step 4 — the ONE generic recipe->Principled proxy mapper.

Builds a Blender authoring proxy (a `MatterLCD_<id>` Principled-BSDF material) for a Matter
article from its canonical recipe + `.mtlx`. The proxy is the frozen v1 Blender representation
(E8 §3): it gives the Creator the LCD sliders + a RECOGNIZABLE Asset-Browser preview. It is NOT
a render-parity match for Studio's MaterialX — Studio's render is authoritative.

Lead directive (Phase 60sq1 E11, verbatim boundary):
    canonical recipe -> generic texture/scalar mapping -> small shading-mode mapping
    -> MatterLCD_<id> Principled proxy
NO per-article branches, NO pixel-matching, NO overlay-network recreation, NO texture baking,
NO export-behaviour changes. A feature that will not fit the small generic mapping gets the
closest reasonable proxy + a documented limitation (see LIMITATIONS below).

Generic mapping:
  * base color / roughness / metalness / normal <- the recipe's `*_tex` image when present,
    else its `*_const` scalar (else a neutral default);
  * LCD travel-port sockets (base_color_tint, overlay1_density, overlay2_density, maskset_blend,
    roughness_bias) — the article's `lcd_ports` subset — exposed as node-group interface INPUTS
    with their canonical `.mtlx` nodegraph defaults, so an untouched Creator export stays sparse
    (0 deltas). base_color_tint multiplies base colour; roughness_bias adds to roughness.
  * shading mode from `master`:
      Opaque            -> standard Principled
      Emissive          -> Emission Color + Emission Strength
      TranslucentThin   -> Transmission Weight + IOR (+ transmission_color tint)
      TranslucentThick  -> Transmission Weight + IOR (+ transmission_color tint)
      Subsurface        -> Subsurface Weight + Radius (+ scale)
      Masked            -> Alpha from the opacity texture, material alpha clip at opacity_cutoff
      TwoLayer          -> base (layer-1) textures only  [LIMITATION, see below]

LIMITATIONS (documented, by design — the proxy is recognizable, not faithful):
  * overlay1_density / overlay2_density / maskset_blend sockets are EXPOSED (so they travel on
    export) but NOT visually wired — the proxy does not recreate the MaterialX overlay/maskset
    modulator network.
  * TwoLayer (Rust) shows the base layer only; the layer-2 blend + maskset are not composited.
  * Masked (Lace) uses simple alpha clip, not the full cutout network.
"""
import bpy
import os
import xml.etree.ElementTree as ET

# The 5 appearance scalars that travel Blender->USD via `inputs:` (Stage kLcdTravelPorts).
# uv_scale/uv_offset/uv_rotation are NOT node-group sockets (they travel as primvars / place2d).
LCD_TRAVEL_PORTS = ("base_color_tint", "overlay1_density", "overlay2_density",
                    "maskset_blend", "roughness_bias")
_COLOR_PORTS = ("base_color_tint",)


def _floats(s):
    return [float(x) for x in str(s).replace(",", " ").split()]


def _rgba(s, fallback=(1.0, 1.0, 1.0)):
    v = _floats(s) if s is not None else list(fallback)
    v = (v + [0.0, 0.0, 0.0])[:3]
    return (v[0], v[1], v[2], 1.0)


def parse_mtlx_lcd_defaults(mtlx_path):
    """Read the canonical default of each LCD travel port from the article's `.mtlx` nodegraph
    interface inputs (the authoritative baseline the exporter's sparse-delta measures against)."""
    out = {}
    try:
        root = ET.parse(mtlx_path).getroot()
    except Exception:
        return out
    ng = root.find("nodegraph")
    if ng is None:
        return out
    for inp in ng.findall("input"):
        name = inp.get("name")
        if name in LCD_TRAVEL_PORTS and inp.get("value") is not None:
            out[name] = inp.get("value")
    return out


def _resolve_tex(recipe_rel, mtlx_path):
    """Recipe texture paths are relative to the article's `.mtlx` directory."""
    if not recipe_rel:
        return None
    p = os.path.normpath(os.path.join(os.path.dirname(mtlx_path), recipe_rel))
    return p if os.path.isfile(p) else None


def _build_lcd_group(identity, ports, defaults):
    """The MatterLCD_<id> node-group: passthrough Base Color/Roughness/Metalness/Normal +
    the article's LCD travel-port subset (canonical defaults). base_color_tint multiplies base
    colour; roughness_bias adds to roughness; overlay/maskset sockets are exposed but unwired."""
    ng = bpy.data.node_groups.new("MatterLCD_%s" % identity, "ShaderNodeTree")
    iface = ng.interface

    def add(name, io, stype, default=None):
        s = iface.new_socket(name, in_out=io, socket_type=stype)
        if default is not None:
            s.default_value = default
        return s

    # passthrough surface inputs
    add("Base Color", "INPUT", "NodeSocketColor", (0.8, 0.8, 0.8, 1.0))
    add("Roughness", "INPUT", "NodeSocketFloat", 0.5)
    add("Metalness", "INPUT", "NodeSocketFloat", 0.0)
    add("Normal", "INPUT", "NodeSocketVector", (0.0, 0.0, 1.0))
    # LCD travel-port sockets (article subset), canonical .mtlx defaults
    for p in LCD_TRAVEL_PORTS:
        if p not in ports:
            continue
        if p in _COLOR_PORTS:
            add(p, "INPUT", "NodeSocketColor", _rgba(defaults.get(p), (1.0, 1.0, 1.0)))
        else:
            dv = _floats(defaults[p])[0] if p in defaults else 0.0
            add(p, "INPUT", "NodeSocketFloat", dv)
    # outputs
    for nm in ("Base Color", "Roughness", "Metalness", "Normal"):
        add(nm, "OUTPUT", "NodeSocketColor" if nm == "Base Color"
            else "NodeSocketVector" if nm == "Normal" else "NodeSocketFloat")

    nodes, links = ng.nodes, ng.links
    gin = nodes.new("NodeGroupInput"); gin.location = (-400, 0)
    gout = nodes.new("NodeGroupOutput"); gout.location = (400, 0)

    def gi(name):
        return gin.outputs[name]

    # Base Color (× base_color_tint if present)
    if "base_color_tint" in ports:
        mix = nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"; mix.blend_type = "MULTIPLY"; mix.clamp_factor = True
        mix.inputs["Factor"].default_value = 1.0
        links.new(gi("Base Color"), mix.inputs[6])   # A (RGBA)
        links.new(gi("base_color_tint"), mix.inputs[7])  # B (RGBA)
        links.new(mix.outputs[2], gout.inputs["Base Color"])  # Result (RGBA)
    else:
        links.new(gi("Base Color"), gout.inputs["Base Color"])

    # Roughness (+ roughness_bias if present, clamped)
    if "roughness_bias" in ports:
        add_r = nodes.new("ShaderNodeMath"); add_r.operation = "ADD"; add_r.use_clamp = True
        links.new(gi("Roughness"), add_r.inputs[0])
        links.new(gi("roughness_bias"), add_r.inputs[1])
        links.new(add_r.outputs[0], gout.inputs["Roughness"])
    else:
        links.new(gi("Roughness"), gout.inputs["Roughness"])

    links.new(gi("Metalness"), gout.inputs["Metalness"])
    links.new(gi("Normal"), gout.inputs["Normal"])
    return ng


def build_matter_proxy(identity, recipe, mtlx_path):
    """Build (or rebuild) the `MatterLCD_<id>` proxy material for one article. Returns the material."""
    # clean any prior copy (idempotent regeneration)
    old = bpy.data.materials.get(identity)
    if old is not None:
        bpy.data.materials.remove(old)
    old_ng = bpy.data.node_groups.get("MatterLCD_%s" % identity)
    if old_ng is not None:
        bpy.data.node_groups.remove(old_ng)

    ports = set(recipe.get("lcd_ports", [])) & set(LCD_TRAVEL_PORTS)
    defaults = parse_mtlx_lcd_defaults(mtlx_path)
    group_tree = _build_lcd_group(identity, ports, defaults)

    mat = bpy.data.materials.new(identity)
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (600, 0)
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled"); bsdf.location = (300, 0)
    grp = nt.nodes.new("ShaderNodeGroup"); grp.node_tree = group_tree; grp.location = (0, 0)
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    nt.links.new(grp.outputs["Base Color"], bsdf.inputs["Base Color"])
    nt.links.new(grp.outputs["Roughness"], bsdf.inputs["Roughness"])
    nt.links.new(grp.outputs["Metalness"], bsdf.inputs["Metallic"])

    notes = []

    def image_node(rel, non_color, y):
        path = _resolve_tex(rel, mtlx_path)
        if path is None:
            if rel:
                notes.append("missing texture %s" % os.path.basename(rel))
            return None
        img = bpy.data.images.load(path, check_existing=True)
        if non_color:
            img.colorspace_settings.name = "Non-Color"
        n = nt.nodes.new("ShaderNodeTexImage"); n.image = img; n.location = (-300, y)
        return n

    # base color: texture else const else neutral
    bc = image_node(recipe.get("base_color_tex"), False, 200)
    if bc is not None:
        nt.links.new(bc.outputs["Color"], grp.inputs["Base Color"])
    elif recipe.get("base_color_const"):
        grp.inputs["Base Color"].default_value = _rgba(recipe["base_color_const"])

    rg = image_node(recipe.get("roughness_tex"), True, -50)
    if rg is not None:
        nt.links.new(rg.outputs["Color"], grp.inputs["Roughness"])
    elif recipe.get("roughness_const") is not None:
        grp.inputs["Roughness"].default_value = float(recipe["roughness_const"])

    mt = image_node(recipe.get("metalness_tex"), True, -300)
    if mt is not None:
        nt.links.new(mt.outputs["Color"], grp.inputs["Metalness"])
    elif recipe.get("metalness_const") is not None:
        grp.inputs["Metalness"].default_value = float(recipe["metalness_const"])

    nm = image_node(recipe.get("normal_tex"), True, -550)
    if nm is not None:
        nmap = nt.nodes.new("ShaderNodeNormalMap"); nmap.location = (-100, -550)
        nt.links.new(nm.outputs["Color"], nmap.inputs["Color"])
        nt.links.new(nmap.outputs["Normal"], grp.inputs["Normal"])
        nt.links.new(grp.outputs["Normal"], bsdf.inputs["Normal"])

    ior = recipe.get("specular_ior")
    if ior is not None and "IOR" in bsdf.inputs:
        bsdf.inputs["IOR"].default_value = float(ior)

    # --- small shading-mode mapping (defining trait only) ---
    master = recipe.get("master", "Opaque")
    if master == "Emissive":
        bsdf.inputs["Emission Color"].default_value = _rgba(recipe.get("emission_color"), (1, 1, 1))
        bsdf.inputs["Emission Strength"].default_value = float(recipe.get("emission_luminance", 1.0))
    elif master in ("TranslucentThin", "TranslucentThick"):
        bsdf.inputs["Transmission Weight"].default_value = float(recipe.get("transmission", 1.0))
        tc = recipe.get("transmission_color")
        if tc and bc is None:  # tint base colour toward the transmission colour when untextured
            grp.inputs["Base Color"].default_value = _rgba(tc)
    elif master == "Subsurface":
        bsdf.inputs["Subsurface Weight"].default_value = float(recipe.get("subsurface_weight", 0.0))
        if recipe.get("subsurface_radius") is not None:
            r = float(recipe["subsurface_radius"])
            sc = _floats(recipe.get("subsurface_radius_scale", "1 1 1"))
            sc = (sc + [1.0, 1.0, 1.0])[:3]
            bsdf.inputs["Subsurface Radius"].default_value = (r * sc[0], r * sc[1], r * sc[2])
    elif master == "Masked":
        op = image_node(recipe.get("opacity_tex"), True, 450)
        if op is not None:
            nt.links.new(op.outputs["Color"], bsdf.inputs["Alpha"])
            mat.blend_method = "CLIP" if hasattr(mat, "blend_method") else mat.blend_method
            if hasattr(mat, "alpha_threshold"):
                mat.alpha_threshold = float(recipe.get("opacity_cutoff", 0.5))
        notes.append("Masked: simple alpha clip, not the full cutout network")
    elif master == "TwoLayer":
        notes.append("TwoLayer: base (layer-1) only; layer-2 blend + maskset not composited")

    if ports & {"overlay1_density", "overlay2_density", "maskset_blend"}:
        notes.append("overlay/maskset sockets exposed for export travel but not visually wired")

    return mat, sorted(set(notes))
