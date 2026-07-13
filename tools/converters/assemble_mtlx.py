#!/usr/bin/env python3
"""Stage-C MaterialX assembler (Phase 53, deterministic).

Emits an OpenPBR 1.39 single-file ``.mtlx`` document from a structured spec,
mirroring ``Contract/examples/OpenPBR_Template_Reference.mtlx``:

  * single-file, self-contained, ``version="1.39"``, one ``open_pbr_surface``;
  * the Creator-adjustable LCD subset exposed as **nodegraph interface inputs**
    (frozen vocabulary, LCDSchema.md / Phase-53 D3);
  * the **author tier** (Phase 71) — the values that make each master *be* that
    master. Two carriage lanes, decided by one question (LCDSchema.md §Author tier):
    **Lane A** = OpenPBR has an input for it -> authored on the ``open_pbr_surface``
    node under its OpenPBR name; **Lane B** = it does not (only the Masked cutoff
    and the TwoLayer layer-2 set) -> a named author-tier nodegraph interface input;
  * UV placement on a ``place2d`` node (never a USD prim attr);
  * an optional internal ``imrsv_metadata`` nodedef (portability hint, no version).

**Overlays and masksets are MODULATORS, never albedo** (MasterSet.md, normative).
An overlay carries packed data (R/G = normal XY, B = roughness bias, A = mask density);
a maskset carries coverage (R = layer-2, G/B = overlay gates). Both load ``lin_rec709``.
Neither may contribute colour — mixing either over base colour is the defect this
structure exists to make impossible.

Determinism (CodingStandards / §6 "assembler determinism"): the document is built
in a fixed element order from ordered inputs — no ``datetime``, no RNG, no reliance
on set iteration — so identical inputs produce a byte-identical ``.mtlx``. Python 3.7+
dicts preserve insertion order, so dict iteration here is deterministic too. No network
is touched at assembly time.

Stage C of the A->B->C Authoring Golden Path; conforms to MaterialXTemplate.md.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from typing import Optional

import MaterialX as mx

MATERIALX_VERSION = "1.39"
DOC_COLORSPACE = "lin_rec709"

# Colour space for the three render-role DATA textures (overlays + maskset). They are
# packed data, not colour — an sRGB transfer curve corrupts every channel they carry.
# (LCDSchema.md §Render-role texture nodes; MasterSet.md §Overlay/MaskSet model.)
DATA_COLORSPACE = "lin_rec709"

# Frozen LCD interface-input vocabulary (LCDSchema.md, Phase 53 D3):
#   port name -> (type, default value string, uiname, extra-attrs dict)
LCD_PORTS = {
    "base_color_tint": ("color3", "1.0, 1.0, 1.0", "Base Color Tint", {}),
    "uv_scale": ("vector2", "1.0, 1.0", "UV Scale", {}),
    "uv_offset": ("vector2", "0.0, 0.0", "UV Offset", {}),
    "uv_rotation": ("float", "0.0", "UV Rotation (deg)",
                    {"unittype": "angle", "unit": "degree"}),
    "overlay1_density": ("float", "0.0", "Overlay 1 Density", {}),
    "overlay2_density": ("float", "0.0", "Overlay 2 Density", {}),
    "maskset_blend": ("float", "0.0", "Maskset Blend", {}),
    "roughness_bias": ("float", "0.0", "Roughness Bias", {}),
}

# Author-tier interface inputs — Lane B ONLY (LCDSchema.md §Author tier): the values
# OpenPBR has no input for. NOT Creator-adjustable and NOT part of the frozen Creator
# vocabulary (RD-C) — this dict sits BESIDE LCD_PORTS, never inside it. Authored once
# per article; never reaches the Creator UI. Emitted only when a spec authors them.
AUTHOR_TIER_PORTS = {
    "opacity_cutoff": ("float", "0.5", "Opacity Cutoff", {}),
    "layer_blend_balance": ("float", "0.5", "Layer Blend Balance", {}),
    "layer_blend_contrast": ("float", "0.0", "Layer Blend Contrast", {}),
    "layer2_base_color": ("color3", "0.8, 0.8, 0.8", "Layer 2 Base Color", {}),
    "layer2_roughness": ("float", "0.5", "Layer 2 Roughness", {}),
    "layer2_metalness": ("float", "0.0", "Layer 2 Metalness", {}),
}

# Master identity tokens (MasterSet.md). The bare token rides the contract; the UE
# asset name (M_MasterMaterial_<token>) is Plugin-owned and resolved Plugin-side.
KNOWN_MASTERS = {
    "Opaque", "Masked", "TranslucentThin", "TranslucentThick",
    "Subsurface", "TwoLayer", "Emissive", "system",
}

MAX_OVERLAYS = 2   # MasterSet.md: <=2 overlay layers, <=1 maskset


@dataclass
class Overlay:
    """A tiling packed-data overlay (dust, scratches), gated by an adjustable density port.

    Perturbs normal + roughness only — an overlay never tints (MasterSet.md).
    """
    texture: str            # relative path to the packed overlay data texture (RGBA)
    density_port: str       # which LCD port drives the effect (overlay1_density / overlay2_density)


@dataclass
class MaterialSpec:
    """Everything the assembler needs to emit one Matter material .mtlx."""
    name: str                                   # qualified Matter identity (= <surfacematerial> name)
    master: str                                 # master identity token (MasterSet.md)
    domain: str
    klass: str                                  # taxonomy class (``class`` is a Python keyword)
    scale_tag: str = "s01"
    meters_per_tile: float = 0.1
    # texture maps (relative paths; omit -> use the constant fallback value below)
    base_color_tex: Optional[str] = None
    roughness_tex: Optional[str] = None
    normal_tex: Optional[str] = None
    metalness_tex: Optional[str] = None
    # constant fallbacks (used when the matching *_tex is absent)
    base_color_const: str = "0.8, 0.8, 0.8"
    roughness_const: float = 0.5
    metalness_const: float = 0.0
    specular_ior: float = 1.5
    transmission: float = 0.0                   # >0 for TranslucentThin/Thick
    emission_color: Optional[str] = None        # set -> emissive contribution
    emission_luminance: float = 0.0

    # --- Author tier, Lane A: real OpenPBR inputs, authored on the shader node ---
    opacity_tex: Optional[str] = None             # -> geometry_opacity (what Masked thresholds)
    transmission_color: Optional[str] = None      # color3 — absorption colour (Beer-Lambert)
    transmission_depth: Optional[float] = None    # float — absorption depth; Thick's defining property
    thin_walled: Optional[bool] = None            # THE OpenPBR thin-vs-thick discriminator; None = don't author
    subsurface_weight: float = 0.0                # >0 -> authored
    subsurface_color: Optional[str] = None        # color3
    subsurface_radius: Optional[float] = None     # float — the length scale
    subsurface_radius_scale: Optional[str] = None  # color3 — per-channel MFP multiplier

    # --- Author tier, Lane B: no OpenPBR input exists -> named interface inputs ---
    opacity_cutoff: Optional[float] = None        # Masked; thresholds the geometry_opacity source
    layer_blend_balance: Optional[float] = None   # TwoLayer
    layer_blend_contrast: Optional[float] = None  # TwoLayer
    layer2_base_color_tex: Optional[str] = None
    layer2_roughness_tex: Optional[str] = None
    layer2_metalness_tex: Optional[str] = None
    layer2_normal_tex: Optional[str] = None
    layer2_base_color: Optional[str] = None       # color3 const (used when no layer2_base_color_tex)
    layer2_roughness: Optional[float] = None      # const (used when no layer2_roughness_tex)
    layer2_metalness: Optional[float] = None      # const (used when no layer2_metalness_tex)

    # layering
    overlays: list = field(default_factory=list)  # list[Overlay], <= 2
    maskset_tex: Optional[str] = None             # <=1 maskset (R = layer-2 coverage, G/B = overlay gates)
    # which LCD ports to expose as interface inputs (subset of LCD_PORTS keys, in order)
    lcd_ports: list = field(default_factory=list)
    # per-material authored starting values for exposed LCD ports (else the schema default)
    lcd_defaults: dict = field(default_factory=dict)
    include_metadata: bool = True

    @staticmethod
    def from_dict(d: dict) -> "MaterialSpec":
        # Keep only known spec fields, so a recipe may carry harness hints (e.g. "path")
        # and comment keys ("_comment") without breaking construction.
        fields = {f.name for f in MaterialSpec.__dataclass_fields__.values()}
        kwargs = {k: v for k, v in d.items()
                  if k in fields and k not in ("overlays", "klass")}
        if "class" in d:
            kwargs["klass"] = d["class"]
        kwargs["overlays"] = [Overlay(**o) for o in d.get("overlays", [])]
        return MaterialSpec(**kwargs)

    def has_layer2(self) -> bool:
        """True when the spec authors a second layer (any channel, texture or const)."""
        return any(v is not None for v in (
            self.layer2_base_color_tex, self.layer2_roughness_tex,
            self.layer2_metalness_tex, self.layer2_normal_tex,
            self.layer2_base_color, self.layer2_roughness, self.layer2_metalness,
        ))


def _mx_bool(b: bool) -> str:
    """MaterialX boolean literal — str(True) is 'True', which MaterialX will not parse."""
    return "true" if b else "false"


def _add_input(elem, name, typ, value=None, nodename=None, interfacename=None,
               output=None, nodegraph=None, attrs=None):
    """Add an <input> with a fixed attribute set (deterministic)."""
    inp = elem.addInput(name, typ)
    if value is not None:
        inp.setValueString(str(value))
    if nodename is not None:
        inp.setNodeName(nodename)
    if interfacename is not None:
        inp.setAttribute("interfacename", interfacename)
    if nodegraph is not None:
        inp.setAttribute("nodegraph", nodegraph)
    if output is not None:
        inp.setAttribute("output", output)
    if attrs:
        for k in attrs:                      # ordered (dict insertion order)
            inp.setAttribute(k, str(attrs[k]))
    return inp


def _check_spec(spec: MaterialSpec) -> None:
    """Structural guards — an incoherent spec fails here, not silently at render time."""
    if spec.master not in KNOWN_MASTERS:
        raise ValueError(f"unknown master token: {spec.master!r}")
    for port in spec.lcd_ports:
        if port not in LCD_PORTS:
            raise ValueError(f"unknown LCD port (not in frozen vocabulary): {port!r}")
    if len(spec.overlays) > MAX_OVERLAYS:
        raise ValueError(f"at most {MAX_OVERLAYS} overlays (MasterSet.md); got {len(spec.overlays)}")
    for ov in spec.overlays:
        if ov.density_port not in spec.lcd_ports:
            raise ValueError(
                f"overlay density port {ov.density_port!r} is not exposed in lcd_ports — "
                "the overlay would have no control and no effect")
    if spec.has_layer2() and not spec.maskset_tex:
        raise ValueError(
            "a layer-2 set requires a maskset: maskset.R IS the layer-2 coverage (MasterSet.md). "
            "Without it there is nothing to say WHERE layer 2 sits.")
    if spec.maskset_tex and "maskset_blend" not in spec.lcd_ports:
        raise ValueError(
            "a maskset requires the 'maskset_blend' LCD port — it is the master strength of the "
            "maskset's whole effect (MasterSet.md); without it the maskset is inert.")
    if spec.opacity_cutoff is not None and not spec.opacity_tex:
        raise ValueError(
            "opacity_cutoff needs an opacity source to threshold — a cutoff with nothing to "
            "threshold makes no holes.")


def assemble(spec: MaterialSpec) -> str:
    """Build the material document and return its serialized XML string."""
    _check_spec(spec)
    has_layer2 = spec.has_layer2()

    doc = mx.createDocument()
    doc.setVersionString(MATERIALX_VERSION)
    doc.setColorSpace(DOC_COLORSPACE)

    ng_name = f"NG_{spec.name}"
    sr_name = f"SR_{spec.name}"
    ng = doc.addNodeGraph(ng_name)

    # --- LCD interface inputs (fixed order = the order requested) ---
    for port in spec.lcd_ports:
        typ, default, uiname, extra = LCD_PORTS[port]
        value = spec.lcd_defaults.get(port, default)   # per-material authored start, else schema default
        attrs = {"uiname": uiname}
        attrs.update(extra)
        _add_input(ng, port, typ, value=value, attrs=attrs)

    # --- Author-tier interface inputs (Lane B) — beside the frozen vocabulary, never inside it.
    # Emitted only when this spec authors them, and only when nothing else already drives the
    # channel, so every author-tier input in the emitted graph has a consumer (no dangling inputs).
    author_values = {
        "opacity_cutoff": spec.opacity_cutoff,
        "layer_blend_balance": spec.layer_blend_balance,
        "layer_blend_contrast": spec.layer_blend_contrast,
        "layer2_base_color": spec.layer2_base_color,
        "layer2_roughness": spec.layer2_roughness,
        "layer2_metalness": spec.layer2_metalness,
    }
    author_ports = []
    if spec.opacity_cutoff is not None:
        author_ports.append("opacity_cutoff")
    if has_layer2:
        author_ports += ["layer_blend_balance", "layer_blend_contrast"]
        if not spec.layer2_base_color_tex:
            author_ports.append("layer2_base_color")
        if not spec.layer2_roughness_tex:
            author_ports.append("layer2_roughness")
        if not spec.layer2_metalness_tex:
            author_ports.append("layer2_metalness")

    for port in AUTHOR_TIER_PORTS:                      # declaration order -> deterministic
        if port not in author_ports:
            continue
        typ, default, uiname, extra = AUTHOR_TIER_PORTS[port]
        authored = author_values[port]
        value = default if authored is None else authored
        attrs = {"uiname": uiname}
        attrs.update(extra)
        _add_input(ng, port, typ, value=value, attrs=attrs)

    uses_uv = any([spec.base_color_tex, spec.roughness_tex, spec.normal_tex,
                   spec.metalness_tex, spec.opacity_tex,
                   spec.layer2_base_color_tex, spec.layer2_roughness_tex,
                   spec.layer2_metalness_tex, spec.layer2_normal_tex]
                  + [o.texture for o in spec.overlays]
                  + ([spec.maskset_tex] if spec.maskset_tex else []))

    # --- UV plumbing (only when something samples a texture) ---
    if uses_uv:
        texcoord = ng.addNode("texcoord", "geom_uv", "vector2")
        _add_input(texcoord, "index", "integer", value=0)
        place2d = ng.addNode("place2d", "uv_place", "vector2")
        _add_input(place2d, "texcoord", "vector2", nodename="geom_uv")
        if "uv_scale" in spec.lcd_ports:
            _add_input(place2d, "scale", "vector2", interfacename="uv_scale")
        if "uv_offset" in spec.lcd_ports:
            _add_input(place2d, "offset", "vector2", interfacename="uv_offset")
        if "uv_rotation" in spec.lcd_ports:
            _add_input(place2d, "rotate", "float", interfacename="uv_rotation")

    def _image(node_name, typ, path, colorspace=None):
        n = ng.addNode("image", node_name, typ)
        if colorspace:
            n.setColorSpace(colorspace)
        _add_input(n, "file", "filename", value=path)
        if uses_uv:
            _add_input(n, "texcoord", "vector2", nodename="uv_place")
        return n

    def _node(node_type, name, typ, **inputs):
        """Add a node whose inputs are (type, kind, value) triples — kind: value|nodename|interfacename."""
        n = ng.addNode(node_type, name, typ)
        for in_name, (in_type, kind, val) in inputs.items():
            _add_input(n, in_name, in_type, **{kind: val})
        return name

    # --- Render-role DATA textures: the maskset + the overlays. MODULATORS, never albedo.
    # Node names are the frozen render-role contract (LCDSchema.md) — the Stage extractor
    # reads each node's `file` into the matching wire field.
    if spec.maskset_tex:
        _image("maskset_tex", "color3", spec.maskset_tex, colorspace=DATA_COLORSPACE)
    for i, ov in enumerate(spec.overlays, start=1):
        # color4 — the alpha (mask density) is load-bearing.
        _image(f"overlay{i}_tex", "color4", ov.texture, colorspace=DATA_COLORSPACE)

    # --- TwoLayer blend factor `t` (MasterSet.md, frozen — the producer and the UE master
    # are two implementations of ONE formula):
    #     m = maskset.R ;  c = 1 / max(1e-4, 1 - contrast)
    #     k = saturate((m - balance) * c + 0.5) ;  t = k * maskset_blend
    # At the defaults (balance 0.5, contrast 0.0) this reduces to t = m * maskset_blend.
    t_src = None
    if has_layer2:
        _node("extract", "maskset_r", "float",
              **{"in": ("color3", "nodename", "maskset_tex"),
                 "index": ("integer", "value", 0)})
        _node("subtract", "layer_blend_contrast_inv", "float",
              in1=("float", "value", 1.0),
              in2=("float", "interfacename", "layer_blend_contrast"))
        _node("max", "layer_blend_contrast_safe", "float",
              in1=("float", "nodename", "layer_blend_contrast_inv"),
              in2=("float", "value", 0.0001))
        _node("divide", "layer_blend_gain", "float",
              in1=("float", "value", 1.0),
              in2=("float", "nodename", "layer_blend_contrast_safe"))
        _node("subtract", "layer_blend_centered", "float",
              in1=("float", "nodename", "maskset_r"),
              in2=("float", "interfacename", "layer_blend_balance"))
        _node("multiply", "layer_blend_scaled", "float",
              in1=("float", "nodename", "layer_blend_centered"),
              in2=("float", "nodename", "layer_blend_gain"))
        _node("add", "layer_blend_offset", "float",
              in1=("float", "nodename", "layer_blend_scaled"),
              in2=("float", "value", 0.5))
        _node("clamp", "layer_blend_k", "float",
              **{"in": ("float", "nodename", "layer_blend_offset"),
                 "low": ("float", "value", 0.0),
                 "high": ("float", "value", 1.0)})
        t_src = _node("multiply", "layer_blend_t", "float",
                      in1=("float", "nodename", "layer_blend_k"),
                      in2=("float", "interfacename", "maskset_blend"))

    # --- Overlay effect strength (MasterSet.md):
    #     effect_N = overlayN_density * overlayN.A * lerp(1, maskset.<G|B>, maskset_blend)
    # maskset G gates overlay 1, B gates overlay 2 (the channel contract).
    ov_effect = []
    for i, ov in enumerate(spec.overlays, start=1):
        gate_src = None
        if spec.maskset_tex:
            _node("extract", f"maskset_gate{i}", "float",
                  **{"in": ("color3", "nodename", "maskset_tex"),
                     "index": ("integer", "value", i)})     # overlay1 -> G(1), overlay2 -> B(2)
            gate_src = _node("mix", f"overlay{i}_gate", "float",
                             bg=("float", "value", 1.0),
                             fg=("float", "nodename", f"maskset_gate{i}"),
                             mix=("float", "interfacename", "maskset_blend"))
        _node("extract", f"overlay{i}_density_mask", "float",
              **{"in": ("color4", "nodename", f"overlay{i}_tex"),
                 "index": ("integer", "value", 3)})          # A = mask density
        eff = _node("multiply", f"overlay{i}_effect_raw", "float",
                    in1=("float", "interfacename", ov.density_port),
                    in2=("float", "nodename", f"overlay{i}_density_mask"))
        if gate_src:
            eff = _node("multiply", f"overlay{i}_effect", "float",
                        in1=("float", "nodename", eff),
                        in2=("float", "nodename", gate_src))
        ov_effect.append(eff)

    # --- Base color: source -> [layer-2 blend] -> tint -> out ---
    # The layer blend happens BEFORE base_color_tint, so the Creator tint stays a
    # whole-material control rather than tinting layer 1 only.
    if spec.base_color_tex:
        _image("base_color_tex", "color3", spec.base_color_tex, colorspace="srgb_texture")
        base_src = "base_color_tex"
    else:
        const = ng.addNode("constant", "base_color_const", "color3")
        _add_input(const, "value", "color3", value=spec.base_color_const)
        base_src = "base_color_const"

    if has_layer2:
        if spec.layer2_base_color_tex:
            _image("layer2_base_color_tex", "color3", spec.layer2_base_color_tex,
                   colorspace="srgb_texture")     # layer 2's own albedo IS colour
            l2_src = "layer2_base_color_tex"
        else:
            l2_src = _node("constant", "layer2_base_color_const", "color3",
                           value=("color3", "interfacename", "layer2_base_color"))
        base_src = _node("mix", "base_color_layered", "color3",
                         bg=("color3", "nodename", base_src),
                         fg=("color3", "nodename", l2_src),
                         mix=("float", "nodename", t_src))

    if "base_color_tint" in spec.lcd_ports:
        tint = ng.addNode("multiply", "base_color_tinted", "color3")
        _add_input(tint, "in1", "color3", nodename=base_src)
        _add_input(tint, "in2", "color3", interfacename="base_color_tint")
        base_src = "base_color_tinted"

    ng.addOutput("base_color_out", "color3").setNodeName(base_src)

    # --- Roughness: source -> [layer-2 blend] -> [overlay bias] -> Creator bias -> out ---
    if spec.roughness_tex:
        _image("roughness_tex", "float", spec.roughness_tex)
        rough_src = "roughness_tex"
    else:
        const = ng.addNode("constant", "roughness_const", "float")
        _add_input(const, "value", "float", value=spec.roughness_const)
        rough_src = "roughness_const"

    if has_layer2:
        if spec.layer2_roughness_tex:
            _image("layer2_roughness_tex", "float", spec.layer2_roughness_tex)
            r2_src = "layer2_roughness_tex"
        else:
            r2_src = _node("constant", "layer2_roughness_const", "float",
                           value=("float", "interfacename", "layer2_roughness"))
        rough_src = _node("mix", "roughness_layered", "float",
                          bg=("float", "nodename", rough_src),
                          fg=("float", "nodename", r2_src),
                          mix=("float", "nodename", t_src))

    for i, eff in enumerate(ov_effect, start=1):
        # B = roughness bias, in [0,1] -> an overlay can only ever ROUGHEN (MasterSet.md,
        # which deliberately does NOT *2-1 remap this channel, unlike the normal XY).
        _node("extract", f"overlay{i}_roughness_bias", "float",
              **{"in": ("color4", "nodename", f"overlay{i}_tex"),
                 "index": ("integer", "value", 2)})
        _node("multiply", f"overlay{i}_roughness_delta", "float",
              in1=("float", "nodename", f"overlay{i}_roughness_bias"),
              in2=("float", "nodename", eff))
        rough_src = _node("add", f"roughness_overlay{i}", "float",
                          in1=("float", "nodename", rough_src),
                          in2=("float", "nodename", f"overlay{i}_roughness_delta"))

    if "roughness_bias" in spec.lcd_ports:
        biased = ng.addNode("add", "roughness_biased", "float")
        _add_input(biased, "in1", "float", nodename=rough_src)
        _add_input(biased, "in2", "float", interfacename="roughness_bias")
        rough_src = "roughness_biased"
    ng.addOutput("roughness_out", "float").setNodeName(rough_src)

    # --- Metalness: a graph output whenever a texture OR a second layer exists ---
    has_metal_out = bool(spec.metalness_tex) or has_layer2
    if spec.metalness_tex:
        _image("metalness_tex", "float", spec.metalness_tex)
        metal_src = "metalness_tex"
    elif has_layer2:
        const = ng.addNode("constant", "metalness_const", "float")
        _add_input(const, "value", "float", value=spec.metalness_const)
        metal_src = "metalness_const"
    else:
        metal_src = None

    if has_layer2:
        if spec.layer2_metalness_tex:
            _image("layer2_metalness_tex", "float", spec.layer2_metalness_tex)
            m2_src = "layer2_metalness_tex"
        else:
            m2_src = _node("constant", "layer2_metalness_const", "float",
                           value=("float", "interfacename", "layer2_metalness"))
        metal_src = _node("mix", "metalness_layered", "float",
                          bg=("float", "nodename", metal_src),
                          fg=("float", "nodename", m2_src),
                          mix=("float", "nodename", t_src))

    if has_metal_out:
        ng.addOutput("metalness_out", "float").setNodeName(metal_src)

    # --- Normal: decode -> [layer-2 blend] -> [overlay perturbation] -> normalize -> out ---
    has_normal_out = bool(spec.normal_tex or spec.layer2_normal_tex or ov_effect)
    if has_normal_out:
        if spec.normal_tex:
            _image("normal_tex", "vector3", spec.normal_tex)
            nmap = ng.addNode("normalmap", "surface_normal", "vector3")
            _add_input(nmap, "in", "vector3", nodename="normal_tex")
            n_src = "surface_normal"
        else:
            # An overlay/layer-2 normal needs a base normal to perturb, or its contribution
            # is silently dropped. Flat tangent-space normal.
            n_src = _node("constant", "surface_normal_flat", "vector3",
                          value=("vector3", "value", "0.0, 0.0, 1.0"))

        if spec.layer2_normal_tex:
            _image("layer2_normal_tex", "vector3", spec.layer2_normal_tex)
            n2map = ng.addNode("normalmap", "layer2_normal", "vector3")
            _add_input(n2map, "in", "vector3", nodename="layer2_normal_tex")
            # Decode BOTH to tangent space FIRST, then blend, then renormalize.
            blended = _node("mix", "normal_layered", "vector3",
                            bg=("vector3", "nodename", n_src),
                            fg=("vector3", "nodename", "layer2_normal"),
                            mix=("float", "nodename", t_src))
            n_src = _node("normalize", "normal_layered_unit", "vector3",
                          **{"in": ("vector3", "nodename", blended)})

        for i, eff in enumerate(ov_effect, start=1):
            # R and G are remapped INDIVIDUALLY and only then combined: combining first and
            # remapping the vector would drive z to -1.
            for axis, idx in (("x", 0), ("y", 1)):
                _node("extract", f"overlay{i}_n{axis}_raw", "float",
                      **{"in": ("color4", "nodename", f"overlay{i}_tex"),
                         "index": ("integer", "value", idx)})
                _node("multiply", f"overlay{i}_n{axis}_scaled", "float",
                      in1=("float", "nodename", f"overlay{i}_n{axis}_raw"),
                      in2=("float", "value", 2.0))
                _node("subtract", f"overlay{i}_n{axis}", "float",
                      in1=("float", "nodename", f"overlay{i}_n{axis}_scaled"),
                      in2=("float", "value", 1.0))
            _node("combine3", f"overlay{i}_normal_delta", "vector3",
                  in1=("float", "nodename", f"overlay{i}_nx"),
                  in2=("float", "nodename", f"overlay{i}_ny"),
                  in3=("float", "value", 0.0))
            _node("multiply", f"overlay{i}_normal_scaled", "vector3",
                  in1=("vector3", "nodename", f"overlay{i}_normal_delta"),
                  in2=("float", "nodename", eff))
            n_src = _node("add", f"normal_overlay{i}", "vector3",
                          in1=("vector3", "nodename", n_src),
                          in2=("vector3", "nodename", f"overlay{i}_normal_scaled"))

        if ov_effect:
            n_src = _node("normalize", "normal_out_unit", "vector3",
                          **{"in": ("vector3", "nodename", n_src)})

        ng.addOutput("normal_out", "vector3").setNodeName(n_src)

    # --- Opacity: source -> [cutoff threshold] -> out.
    # The Masked cutoff is thresholded IN the graph (both here and in the UE master, P1) —
    # the alternative, UE's OpacityMaskClipValue, is a static base-property override a MID
    # cannot reach. Thresholding here also keeps opacity_cutoff a consumed input.
    has_opacity_out = bool(spec.opacity_tex)
    if has_opacity_out:
        _image("opacity_tex", "float", spec.opacity_tex)
        op_src = "opacity_tex"
        if spec.opacity_cutoff is not None:
            op_src = _node("ifgreatereq", "opacity_thresholded", "float",
                           value1=("float", "nodename", "opacity_tex"),
                           value2=("float", "interfacename", "opacity_cutoff"),
                           in1=("float", "value", 1.0),
                           in2=("float", "value", 0.0))
        ng.addOutput("opacity_out", "float").setNodeName(op_src)

    # --- OpenPBR surface shader ---
    shader = doc.addNode("open_pbr_surface", sr_name, "surfaceshader")
    _add_input(shader, "base_weight", "float", value=1.0)
    _add_input(shader, "base_color", "color3", nodegraph=ng_name, output="base_color_out")
    if has_metal_out:
        _add_input(shader, "base_metalness", "float", nodegraph=ng_name, output="metalness_out")
    else:
        _add_input(shader, "base_metalness", "float", value=spec.metalness_const)
    _add_input(shader, "specular_roughness", "float", nodegraph=ng_name, output="roughness_out")
    _add_input(shader, "specular_ior", "float", value=spec.specular_ior)
    if has_normal_out:
        _add_input(shader, "geometry_normal", "vector3", nodegraph=ng_name, output="normal_out")
    if has_opacity_out:
        _add_input(shader, "geometry_opacity", "float", nodegraph=ng_name, output="opacity_out")
    if spec.thin_walled is not None:
        # THE OpenPBR thin-vs-thick discriminator — what makes TranslucentThick not Thin
        # at the producer. Without it the two masters are the same material described twice.
        _add_input(shader, "geometry_thin_walled", "boolean", value=_mx_bool(spec.thin_walled))
    if spec.transmission > 0:
        _add_input(shader, "transmission_weight", "float", value=spec.transmission)
    if spec.transmission_color is not None:
        _add_input(shader, "transmission_color", "color3", value=spec.transmission_color)
    if spec.transmission_depth is not None:
        _add_input(shader, "transmission_depth", "float", value=spec.transmission_depth)
    if spec.subsurface_weight > 0:
        _add_input(shader, "subsurface_weight", "float", value=spec.subsurface_weight)
    if spec.subsurface_color is not None:
        _add_input(shader, "subsurface_color", "color3", value=spec.subsurface_color)
    if spec.subsurface_radius is not None:
        _add_input(shader, "subsurface_radius", "float", value=spec.subsurface_radius)
    if spec.subsurface_radius_scale is not None:
        _add_input(shader, "subsurface_radius_scale", "color3", value=spec.subsurface_radius_scale)
    if spec.emission_color is not None:
        _add_input(shader, "emission_luminance", "float", value=spec.emission_luminance)
        _add_input(shader, "emission_color", "color3", value=spec.emission_color)

    # --- Material: the name IS the qualified Matter identity ---
    surfmat = doc.addNode("surfacematerial", spec.name, "material")
    _add_input(surfmat, "surfaceshader", "surfaceshader", nodename=sr_name)

    # --- Optional internal metadata hint (NOT a USD imrsv: attr) ---
    if spec.include_metadata:
        nd = doc.addNodeDef("ND_imrsv_metadata", "string", "imrsv_metadata")
        nd.setNodeGroup("metadata")
        _add_input(nd, "master_material", "string", value=spec.master,
                   attrs={"uniform": "true"})
        _add_input(nd, "scale_tag", "string", value=spec.scale_tag,
                   attrs={"uniform": "true"})
        _add_input(nd, "meters_per_tile", "float", value=spec.meters_per_tile)
        _add_input(nd, "domain", "string", value=spec.domain, attrs={"uniform": "true"})
        _add_input(nd, "class", "string", value=spec.klass, attrs={"uniform": "true"})
        # addNodeDef(..., "string", ...) already declares the implicit "out" output.

    return mx.writeToXmlString(doc)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Assemble an OpenPBR 1.39 Matter .mtlx from a JSON spec.")
    ap.add_argument("spec", help="path to a JSON material spec")
    ap.add_argument("-o", "--out", help="output .mtlx path (default: stdout)")
    args = ap.parse_args(argv)

    with open(args.spec, "r", encoding="utf-8") as fh:
        spec = MaterialSpec.from_dict(json.load(fh))
    xml = assemble(spec)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(xml)
        print(f"wrote {args.out}")
    else:
        sys.stdout.write(xml)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
