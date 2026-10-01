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
import re
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

DUST_COLOR = "0.413, 0.386, 0.308"   # linear; see overlayN_color below

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
    "overlay3_density": ("float", "0.0", "Overlay 3 Density", {}),   # added 2026-09-25 (cap 2 -> 3)
    "maskset_blend": ("float", "0.0", "Maskset Blend", {}),
    "roughness_bias": ("float", "0.0", "Roughness Bias", {}),
    # Phase10 (RD-P10-1): a DEPOSIT overlay's colour (dust), which the Creator may change. The
    # start value is Physically Based's Sand (CC0; 0.44, 0.386, 0.231) desaturated halfway to its
    # own luminance, since household dust is greyer than sand. MasterSet §Overlay semantic.
    "overlay1_color": ("color3", DUST_COLOR, "Overlay 1 Color", {}),
    "overlay2_color": ("color3", DUST_COLOR, "Overlay 2 Color", {}),
    "overlay3_color": ("color3", DUST_COLOR, "Overlay 3 Color", {}),
}

# Author-tier interface inputs — Lane B ONLY (LCDSchema.md §Author tier): the values
# OpenPBR has no input for. NOT Creator-adjustable and NOT part of the frozen Creator
# vocabulary (RD-C) — this dict sits BESIDE LCD_PORTS, never inside it. Authored once
# per article; never reaches the Creator UI. Emitted only when a spec authors them.
AUTHOR_TIER_PORTS = {
    "opacity_cutoff": ("float", "0.5", "Opacity Cutoff", {}),
    # Phase07 7.6 (L2): the MESH's cut-out, supplied when the article is bound (LCDSchema
    # §Cut-out map). Empty here: with no map supplied the image's default (1) is opaque.
    "cutout_map": ("filename", "", "Cut-out Map", {}),
    # Phase09 9.1 (RD-P09-1): the MESH's picture (a hairstyle's strands, an eye), supplied when
    # the article is bound (LCDSchema §Base colour map) and MULTIPLIED into the base colour.
    # Empty here: with no map supplied the image's default (1) leaves the article's own colour.
    "base_color_map": ("filename", "", "Base Color Map", {}),
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
    "Subsurface", "TwoLayer", "Emissive", "Hair", "system",
}

# Masters whose coverage is the mesh's cut-out (MasterSet.md). Masked THRESHOLDS it at
# `opacity_cutoff`; Hair (Phase08 8.1) takes it as SOFT coverage, unthresholded, and lets light
# through the card: thin-walled subsurface whose colour is the (tinted) base colour.
CUTOUT_MASTERS = {"Masked", "Hair"}

# Masters that take the mesh's picture, `base_color_map` (Phase09 RD-P09-1; LCDSchema §Author
# tier). The picture shades the article's base colour; the masters whose base is layered
# (TwoLayer), light (Emissive) or seen through (Translucent*) do not take it.
BASE_COLOR_MAP_MASTERS = {"Opaque", "Masked", "Hair", "Subsurface"}

MAX_OVERLAYS = 3   # MasterSet.md: <=3 overlay layers, <=1 maskset (raised from 2, 2026-09-25)

# Scale tag -> metres per UV tile (Identity.md §Scale tags). A SHARED layer (overlay or
# maskset) is sampled at its own size (Phase04): its tag IS its size, so `sUKN` is refused.
SCALE_TAG_METRES = {
    "s0001": 0.001, "s001": 0.01, "s01": 0.1, "s1": 1.0, "s10": 10.0, "s100": 100.0,
}
_LAYER_TAG_RE = re.compile(r"_(s\d+|sUKN)\.png$")


def layer_size_m(path: str) -> float:
    """A shared layer's real-world size, read off its filename scale tag (Identity.md)."""
    m = _LAYER_TAG_RE.search(path)
    if not m or m.group(1) not in SCALE_TAG_METRES:
        raise ValueError(
            f"shared layer {path!r} has no sized scale tag — a layer is sampled at its own "
            f"size, so its tag must be one of {sorted(SCALE_TAG_METRES)} (not sUKN)")
    return SCALE_TAG_METRES[m.group(1)]

# Recipe keys that are not spec fields: harness metadata, not material data (Phase03 G1).
# `status` (Phase07, D-S) is the article's lifecycle state BEFORE a release; it never reaches
# the .mtlx, which is frozen once released, so promoting an article never changes its file.
RECIPE_METADATA_KEYS = {"_comment", "path", "class", "sources", "status"}


@dataclass
class Overlay:
    """A tiling packed-data overlay (dust, scratches), gated by an adjustable density port.

    Perturbs normal + roughness. A DEPOSIT overlay (one with a ``color_port``, Phase10) also
    covers the surface with that port's colour, weighted by its effect; its packed channels
    never become colour (MasterSet.md §Overlay semantic).
    """
    texture: str            # relative path to the packed overlay data texture (RGBA)
    density_port: str       # which LCD port drives the effect (overlay1_density / overlay2_density / overlay3_density)
    color_port: Optional[str] = None   # a deposit's colour (overlayN_color, the same N); None = not a deposit


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
    subsurface_scatter_anisotropy: Optional[float] = None  # -1..1; >0 = forward (skin, Phase07)
    # coat and fuzz (Phase07 7.3): OpenPBR layers any master may carry (MasterSet: sheen and
    # clearcoat are Opaque params). Each is authored only when set, so an article that sets
    # none of them assembles byte-identically to before (the determinism lane).
    coat_weight: Optional[float] = None
    coat_color: Optional[str] = None              # color3 — the coat's tint of what lies under it
    coat_roughness: Optional[float] = None
    coat_ior: Optional[float] = None
    fuzz_weight: Optional[float] = None
    fuzz_color: Optional[str] = None              # color3
    fuzz_roughness: Optional[float] = None
    specular_roughness_anisotropy: Optional[float] = None  # 0..1 along the UV tangent (7.6, C3)
    # Phase09 9.1: OpenPBR's specular weight, authored only when set. Card hair is MATTE (the
    # lead at click 1: the shine "gives away these are flat sheets"), so Hair_Natural sets 0.
    specular_weight: Optional[float] = None

    # --- Author tier, Lane B: no OpenPBR input exists -> named interface inputs ---
    opacity_cutoff: Optional[float] = None        # Masked; thresholds the geometry_opacity source
    cutout_map: bool = False                      # Masked; declares the mesh-supplied cut-out input
    base_color_map: bool = False                  # declares the mesh-supplied picture (Phase09)
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
    overlays: list = field(default_factory=list)  # list[Overlay], <= 3
    maskset_tex: Optional[str] = None             # <=1 maskset (R = layer-2 coverage, G/B = overlay gates)
    # which LCD ports to expose as interface inputs (subset of LCD_PORTS keys, in order)
    lcd_ports: list = field(default_factory=list)
    # per-material authored starting values for exposed LCD ports (else the schema default)
    lcd_defaults: dict = field(default_factory=dict)
    include_metadata: bool = True

    @staticmethod
    def from_dict(d: dict) -> "MaterialSpec":
        # G1 (Phase03): an unknown key is an ERROR, never silently dropped. A misspelled key
        # (`roughnes_const`) used to vanish and leave the default in its place. The metadata
        # keys a recipe may carry are named; everything else must be a spec field.
        fields = {f.name for f in MaterialSpec.__dataclass_fields__.values()}
        unknown = sorted(set(d) - (fields - {"klass"}) - RECIPE_METADATA_KEYS)
        if unknown:
            raise ValueError(f"unknown recipe key(s) {unknown} (tools/converters/recipe.schema.json)")
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
        if ov.color_port is not None:
            slot = ov.density_port.removesuffix("_density")
            if ov.color_port != f"{slot}_color":
                raise ValueError(f"a deposit's colour port is its own slot's: {slot}_color, "
                                 f"not {ov.color_port!r}")
            if ov.color_port not in spec.lcd_ports:
                raise ValueError(f"deposit colour port {ov.color_port!r} is not exposed in "
                                 "lcd_ports — the Creator could not change it (RD-P10-1)")
    for port in spec.lcd_ports:
        if port.endswith("_color") and port.startswith("overlay") and not any(
                ov.color_port == port for ov in spec.overlays):
            raise ValueError(f"{port!r} is exposed but no overlay is a deposit with that "
                             "colour port: a dead port")
    if spec.has_layer2() and not spec.maskset_tex:
        raise ValueError(
            "a layer-2 set requires a maskset: maskset.R IS the layer-2 coverage (MasterSet.md). "
            "Without it there is nothing to say WHERE layer 2 sits.")
    if spec.maskset_tex and "maskset_blend" not in spec.lcd_ports:
        raise ValueError(
            "a maskset requires the 'maskset_blend' LCD port — it is the master strength of the "
            "maskset's whole effect (MasterSet.md); without it the maskset is inert.")
    if spec.opacity_cutoff is not None and not (spec.opacity_tex or spec.cutout_map):
        raise ValueError(
            "opacity_cutoff needs an opacity source to threshold — a cutoff with nothing to "
            "threshold makes no holes.")
    if spec.cutout_map:
        if spec.master not in CUTOUT_MASTERS:
            raise ValueError("cutout_map is an input of the cut-out masters "
                             f"{sorted(CUTOUT_MASTERS)} (MasterSet.md); this article is {spec.master}")
        if spec.opacity_tex:
            raise ValueError("an article has ONE opacity source: its own opacity_tex (a pattern "
                             "of the substance, like lace) or the mesh's cutout_map, not both")
        if spec.master == "Masked" and spec.opacity_cutoff is None:
            raise ValueError("cutout_map needs opacity_cutoff: Masked thresholds its source")
    if spec.base_color_map and spec.master not in BASE_COLOR_MAP_MASTERS:
        raise ValueError("base_color_map is an input of the masters "
                         f"{sorted(BASE_COLOR_MAP_MASTERS)} (LCDSchema.md); this article is {spec.master}")
    if spec.master == "Hair":
        # Phase08 8.1 (the lead's interim hair: light through the strands, soft edges)
        if not spec.cutout_map or spec.opacity_cutoff is not None:
            raise ValueError("Hair takes the mesh's cutout_map as soft coverage: cutout_map, "
                             "and no opacity_cutoff (that is Masked's hard cut-out)")
        if spec.thin_walled is not True or not spec.subsurface_weight > 0:
            raise ValueError("Hair lets light through the card: thin_walled true and "
                             "subsurface_weight > 0 (OpenPBR thin-walled subsurface)")
        if spec.subsurface_color is not None:
            raise ValueError("Hair's subsurface colour IS its tinted base colour (so the tint "
                             "reaches the light through the strands); do not author one")
    layers = [o.texture for o in spec.overlays] + ([spec.maskset_tex] if spec.maskset_tex else [])
    if layers and not spec.meters_per_tile > 0:
        raise ValueError(
            "an article carrying layers needs meters_per_tile > 0: each layer is sampled at "
            "its own size RELATIVE to the article's tile (Phase04)")
    for path in layers:
        layer_size_m(path)   # raises on an unsized (sUKN / untagged) layer


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
        "cutout_map": None,                  # the binding supplies it; the article's is empty
        "base_color_map": None,              # the binding supplies it; the article's is empty
        "layer_blend_balance": spec.layer_blend_balance,
        "layer_blend_contrast": spec.layer_blend_contrast,
        "layer2_base_color": spec.layer2_base_color,
        "layer2_roughness": spec.layer2_roughness,
        "layer2_metalness": spec.layer2_metalness,
    }
    author_ports = []
    if spec.opacity_cutoff is not None:
        author_ports.append("opacity_cutoff")
    if spec.cutout_map:
        author_ports.append("cutout_map")
    if spec.base_color_map:
        author_ports.append("base_color_map")
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
    # The maskset loads color3 (R/G/B) unless a third overlay needs its A channel as a gate:
    # only then color4, so an article with <= 2 overlays assembles byte-identically to before.
    # Phase04: a SHARED layer is sampled at its OWN real-world size. The render-role node is
    # a MaterialX `tiledimage` whose stdlib graph computes uv / realworldimagesize *
    # realworldtilesize, fed from `uv_place`, so the Creator's UV controls still move the
    # whole material together. Both sizes are fixed author data on the render-role node,
    # beside its `file` (LCDSchema.md §Render-role texture nodes).
    def _layer_image(node_name, typ, path):
        n = ng.addNode("tiledimage", node_name, typ)
        n.setColorSpace(DATA_COLORSPACE)
        _add_input(n, "file", "filename", value=path)
        _add_input(n, "texcoord", "vector2", nodename="uv_place")
        img_m, tile_m = layer_size_m(path), spec.meters_per_tile
        _add_input(n, "realworldimagesize", "vector2", value=f"{img_m:g}, {img_m:g}")
        _add_input(n, "realworldtilesize", "vector2", value=f"{tile_m:g}, {tile_m:g}")
        return n

    mask_type = "color4" if len(spec.overlays) >= 3 else "color3"
    if spec.maskset_tex:
        _layer_image("maskset_tex", mask_type, spec.maskset_tex)
    for i, ov in enumerate(spec.overlays, start=1):
        # color4 — the alpha (mask density) is load-bearing.
        _layer_image(f"overlay{i}_tex", "color4", ov.texture)

    # --- TwoLayer blend factor `t` (MasterSet.md, frozen — the producer and the UE master
    # are two implementations of ONE formula):
    #     m = maskset.R ;  c = 1 / max(1e-4, 1 - contrast)
    #     k = saturate((m - balance) * c + 0.5) ;  t = k * maskset_blend
    # At the defaults (balance 0.5, contrast 0.0) this reduces to t = m * maskset_blend.
    t_src = None
    if has_layer2:
        _node("extract", "maskset_r", "float",
              **{"in": (mask_type, "nodename", "maskset_tex"),
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
    # maskset G gates overlay 1, B gates overlay 2, A gates overlay 3 (the channel contract).
    ov_effect = []
    for i, ov in enumerate(spec.overlays, start=1):
        gate_src = None
        if spec.maskset_tex:
            _node("extract", f"maskset_gate{i}", "float",
                  **{"in": (mask_type, "nodename", "maskset_tex"),
                     "index": ("integer", "value", i)})     # overlay1 -> G(1), overlay2 -> B(2), overlay3 -> A(3)
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

    # --- Deposits (Phase10, MasterSet §Overlay semantic): a deposit overlay COVERS the surface
    # where it lies. Its declared colour (a Creator port, never its packed channels) replaces the
    # base colour, and every layer it hides (metal, transmission, subsurface, coat, fuzz) goes to
    # none, all by the overlay's effect. In slot order; an article with no deposit is unchanged.
    deposits = [(i, eff, ov.color_port) for i, (ov, eff)
                in enumerate(zip(spec.overlays, ov_effect), start=1) if ov.color_port]

    def _covered(name: str, typ: str, src_kind: str, src) -> str:
        """``src`` mixed toward 0 by every deposit's effect; returns the last node's name."""
        for i, eff, _ in deposits:
            src = _node("mix", f"{name}_deposit{i}", typ,
                        bg=(typ, src_kind, src), fg=(typ, "value", 0.0),
                        mix=("float", "nodename", eff))
            src_kind = "nodename"
        return src

    # --- Base color: source -> [layer-2 blend] -> tint -> [deposits] -> out ---
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

    # Phase09 (RD-P09-1): base = base_color_const x base_color_map x base_color_tint. The mesh's
    # picture is sampled on texcoord 0 directly, not `uv_place` (like `cutout_map`: drawn on the
    # mesh's own UVs, so the Creator's placement never moves it). With no map supplied the file
    # is empty and the image returns its `default`, white: the article's own colour, never magenta.
    if spec.base_color_map:
        _node("texcoord", "base_color_map_uv", "vector2", index=("integer", "value", 0))
        img = ng.addNode("image", "base_color_map_tex", "color3")
        img.setColorSpace("srgb_texture")
        _add_input(img, "file", "filename", interfacename="base_color_map")
        _add_input(img, "default", "color3", value="1.0, 1.0, 1.0")
        _add_input(img, "texcoord", "vector2", nodename="base_color_map_uv")
        base_src = _node("multiply", "base_color_mapped", "color3",
                         in1=("color3", "nodename", base_src),
                         in2=("color3", "nodename", "base_color_map_tex"))

    if "base_color_tint" in spec.lcd_ports:
        tint = ng.addNode("multiply", "base_color_tinted", "color3")
        _add_input(tint, "in1", "color3", nodename=base_src)
        _add_input(tint, "in2", "color3", interfacename="base_color_tint")
        base_src = "base_color_tinted"

    # After the tint (a Creator who tints a car red does not tint its dust) and the mesh's picture.
    for i, eff, port in deposits:
        base_src = _node("mix", f"base_color_deposit{i}", "color3",
                         bg=("color3", "nodename", base_src),
                         fg=("color3", "interfacename", port),
                         mix=("float", "nodename", eff))

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
        # Clamp the biased total to [0,1] (LCDSchema.md, `roughness_bias`): OpenPBR does not clamp
        # specular_roughness, so a negative total would render ROUGH in a stock viewer while the
        # Unreal masters (which clamp) render it glossy. The article owns the clamp.
        rough_src = _node("clamp", "roughness_biased_clamped", "float",
                          **{"in": ("float", "nodename", "roughness_biased"),
                             "low": ("float", "value", 0.0),
                             "high": ("float", "value", 1.0)})
    ng.addOutput("roughness_out", "float").setNodeName(rough_src)

    # --- Metalness: a graph output whenever a texture OR a second layer exists ---
    # A deposit hides metal (Phase10): a metal under dust is no longer seen as metal.
    cover_metal = bool(deposits) and bool(spec.metalness_tex or has_layer2 or spec.metalness_const > 0)
    has_metal_out = bool(spec.metalness_tex) or has_layer2 or cover_metal
    if spec.metalness_tex:
        _image("metalness_tex", "float", spec.metalness_tex)
        metal_src = "metalness_tex"
    elif has_layer2 or cover_metal:
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

    if cover_metal:
        metal_src = _covered("metalness", "float", "nodename", metal_src)
    if has_metal_out:
        ng.addOutput("metalness_out", "float").setNodeName(metal_src)

    # --- Normal ---
    # MaterialX's `normalmap` outputs a WORLD-space normal (stdlib: "into 'world' space"). So
    # everything that COMBINES normals — the layer-2 blend and the overlay bumps — happens in
    # TANGENT space, on decoded maps (2c - 1), and one `normalmap` converts the result to
    # world space at the end. Before Phase05 step 5.3 the combination was done on the
    # already-world output of `normalmap`: overlay bumps were added along world X/Y, and the
    # "flat" (0, 0, 1) fallback became a fixed world +Z normal (Execution Log F10).
    # An article with ONLY a normal map needs no combination and keeps the direct graph.
    has_normal_out = bool(spec.normal_tex or spec.layer2_normal_tex or ov_effect)
    combine = bool(spec.layer2_normal_tex or ov_effect)
    if has_normal_out and not combine:
        _image("normal_tex", "vector3", spec.normal_tex)
        nmap = ng.addNode("normalmap", "surface_normal", "vector3")
        _add_input(nmap, "in", "vector3", nodename="normal_tex")
        n_src = "surface_normal"
    elif has_normal_out:
        def _decode(tex: str, name: str) -> str:
            scaled = _node("multiply", f"{name}_x2", "vector3",
                           in1=("vector3", "nodename", tex), in2=("float", "value", 2.0))
            return _node("subtract", name, "vector3",
                         in1=("vector3", "nodename", scaled), in2=("float", "value", 1.0))

        if spec.normal_tex:
            _image("normal_tex", "vector3", spec.normal_tex)
            n_src = _decode("normal_tex", "surface_normal_ts")
        else:
            # An overlay/layer-2 normal needs a base normal to perturb, or its contribution
            # is silently dropped. Flat, in TANGENT space: it becomes the surface's own normal.
            n_src = _node("constant", "surface_normal_flat", "vector3",
                          value=("vector3", "value", "0.0, 0.0, 1.0"))

        if spec.layer2_normal_tex:
            _image("layer2_normal_tex", "vector3", spec.layer2_normal_tex)
            n2 = _decode("layer2_normal_tex", "layer2_normal_ts")
            # Decode BOTH to tangent space FIRST, then blend, then renormalize.
            blended = _node("mix", "normal_layered", "vector3",
                            bg=("vector3", "nodename", n_src),
                            fg=("vector3", "nodename", n2),
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
        # re-encode (n * 0.5 + 0.5) and convert the tangent-space result to world space ONCE
        half = _node("multiply", "normal_ts_half", "vector3",
                     in1=("vector3", "nodename", n_src), in2=("float", "value", 0.5))
        enc = _node("add", "normal_ts_encoded", "vector3",
                    in1=("vector3", "nodename", half), in2=("float", "value", 0.5))
        n_src = _node("normalmap", "surface_normal", "vector3",
                      **{"in": ("vector3", "nodename", enc)})

    if has_normal_out:
        ng.addOutput("normal_out", "vector3").setNodeName(n_src)

    # --- Opacity: source -> [cutoff threshold] -> out.
    # The Masked cutoff is thresholded IN the graph (both here and in the UE master, P1) —
    # the alternative, UE's OpacityMaskClipValue, is a static base-property override a MID
    # cannot reach. Thresholding here also keeps opacity_cutoff a consumed input.
    # Phase07 7.6: the source may instead be the MESH's cut-out (`cutout_map`, supplied when the
    # article is bound). It samples texcoord 0 directly, not `uv_place`: the map is drawn on the
    # mesh's own UVs, so the article's placement must not move it. (A second UV set is not an
    # option: Storm reads `st` for every texcoord index, measured 2026-09-27.) With no map
    # supplied the file is empty and the image returns its `default`, 1: opaque, never magenta.
    has_opacity_out = bool(spec.opacity_tex or spec.cutout_map)
    if has_opacity_out:
        if spec.cutout_map:
            _node("texcoord", "cutout_uv", "vector2", index=("integer", "value", 0))
            _node("image", "cutout_tex", "float",
                  file=("filename", "interfacename", "cutout_map"),
                  default=("float", "value", 1.0),
                  texcoord=("vector2", "nodename", "cutout_uv"))
            op_src = "cutout_tex"
        else:
            _image("opacity_tex", "float", spec.opacity_tex)
            op_src = "opacity_tex"
        if spec.opacity_cutoff is not None:
            op_src = _node("ifgreatereq", "opacity_thresholded", "float",
                           value1=("float", "nodename", op_src),
                           value2=("float", "interfacename", "opacity_cutoff"),
                           in1=("float", "value", 1.0),
                           in2=("float", "value", 0.0))
        ng.addOutput("opacity_out", "float").setNodeName(op_src)

    # --- The layers a deposit hides (Phase10): each authored weight above 0 reaches the shader
    # through the graph, mixed toward 0 by every deposit's effect (light no longer passes
    # through, scatters in, or reflects off a coat or fibres under dust).
    covered_out = {}
    if deposits:
        for name, val in (("transmission_weight", spec.transmission),
                          ("subsurface_weight", spec.subsurface_weight),
                          ("coat_weight", spec.coat_weight), ("fuzz_weight", spec.fuzz_weight)):
            if val:                                   # None or 0: nothing to hide
                src = _covered(name, "float", "value", val)
                ng.addOutput(f"{name}_out", "float").setNodeName(src)
                covered_out[name] = f"{name}_out"

    def _weight(name: str, value) -> None:
        if name in covered_out:
            _add_input(shader, name, "float", nodegraph=ng_name, output=covered_out[name])
        else:
            _add_input(shader, name, "float", value=value)

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
        _weight("transmission_weight", spec.transmission)
    if spec.transmission_color is not None:
        _add_input(shader, "transmission_color", "color3", value=spec.transmission_color)
    if spec.transmission_depth is not None:
        _add_input(shader, "transmission_depth", "float", value=spec.transmission_depth)
    if spec.subsurface_weight > 0:
        _weight("subsurface_weight", spec.subsurface_weight)
    if spec.subsurface_color is not None:
        _add_input(shader, "subsurface_color", "color3", value=spec.subsurface_color)
    elif spec.master == "Hair" or (spec.base_color_map and spec.subsurface_weight > 0):
        # Hair: the fibre's colour, tint included: what passes through a strand is coloured by it.
        # Phase09 (F-P09-5): a Subsurface article taking the mesh's picture scatters the PICTURE's
        # colour, or the picture keeps only (1 - subsurface_weight) of its strength (learning M4).
        _add_input(shader, "subsurface_color", "color3", nodegraph=ng_name, output="base_color_out")
    if spec.subsurface_radius is not None:
        _add_input(shader, "subsurface_radius", "float", value=spec.subsurface_radius)
    if spec.subsurface_radius_scale is not None:
        _add_input(shader, "subsurface_radius_scale", "color3", value=spec.subsurface_radius_scale)
    # Phase07 7.3 — lane A, OpenPBR's own names, each only when the spec sets it
    for key, typ in (("subsurface_scatter_anisotropy", "float"),
                     ("coat_weight", "float"), ("coat_color", "color3"),
                     ("coat_roughness", "float"), ("coat_ior", "float"),
                     ("fuzz_weight", "float"), ("fuzz_color", "color3"),
                     ("fuzz_roughness", "float"),
                     ("specular_roughness_anisotropy", "float"),
                     ("specular_weight", "float")):
        if getattr(spec, key) is not None:
            if key in covered_out:
                _weight(key, getattr(spec, key))
            else:
                _add_input(shader, key, typ, value=getattr(spec, key))
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
