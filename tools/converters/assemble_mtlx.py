#!/usr/bin/env python3
"""Stage-C MaterialX assembler (Phase 53, deterministic).

Emits an OpenPBR 1.39 single-file ``.mtlx`` document from a structured spec,
mirroring ``Contract/examples/OpenPBR_Template_Reference.mtlx``:

  * single-file, self-contained, ``version="1.39"``, one ``open_pbr_surface``;
  * the Creator-adjustable LCD subset exposed as **nodegraph interface inputs**
    (frozen vocabulary, LCDSchema.md / Phase-53 D3);
  * UV placement on a ``place2d`` node (never a USD prim attr);
  * an optional internal ``imrsv_metadata`` nodedef (portability hint, no version).

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

# Master identity tokens (MasterSet.md). The bare token rides the contract; the UE
# asset name (M_MasterMaterial_<token>) is Plugin-owned and resolved Plugin-side.
KNOWN_MASTERS = {
    "Opaque", "Masked", "TranslucentThin", "TranslucentThick",
    "Subsurface", "TwoLayer", "Emissive", "system",
}


@dataclass
class Overlay:
    """A tiling overlay layer mixed over base color by an adjustable density port."""
    texture: str            # relative path to the overlay color texture
    density_port: str       # which LCD port drives the mix (overlay1_density / overlay2_density)


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
    # layering
    overlays: list = field(default_factory=list)  # list[Overlay], <= 2
    maskset_tex: Optional[str] = None             # <=1 maskset (drives maskset_blend)
    # which LCD ports to expose as interface inputs (subset of LCD_PORTS keys, in order)
    lcd_ports: list = field(default_factory=list)
    include_metadata: bool = True

    @staticmethod
    def from_dict(d: dict) -> "MaterialSpec":
        overlays = [Overlay(**o) for o in d.get("overlays", [])]
        kwargs = {k: v for k, v in d.items() if k not in ("overlays", "class")}
        if "class" in d:
            kwargs["klass"] = d["class"]
        kwargs["overlays"] = overlays
        return MaterialSpec(**kwargs)


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


def assemble(spec: MaterialSpec) -> str:
    """Build the material document and return its serialized XML string."""
    if spec.master not in KNOWN_MASTERS:
        raise ValueError(f"unknown master token: {spec.master!r}")
    for port in spec.lcd_ports:
        if port not in LCD_PORTS:
            raise ValueError(f"unknown LCD port (not in frozen vocabulary): {port!r}")

    doc = mx.createDocument()
    doc.setVersionString(MATERIALX_VERSION)
    doc.setColorSpace(DOC_COLORSPACE)

    ng_name = f"NG_{spec.name}"
    sr_name = f"SR_{spec.name}"
    ng = doc.addNodeGraph(ng_name)

    # --- LCD interface inputs (fixed order = the order requested) ---
    for port in spec.lcd_ports:
        typ, default, uiname, extra = LCD_PORTS[port]
        attrs = {"uiname": uiname}
        attrs.update(extra)
        _add_input(ng, port, typ, value=default, attrs=attrs)

    uses_uv = any([spec.base_color_tex, spec.roughness_tex, spec.normal_tex,
                   spec.metalness_tex] + [o.texture for o in spec.overlays]
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

    # --- Base color: source (image|constant) -> tint -> overlays -> mask -> out ---
    if spec.base_color_tex:
        _image("base_color_tex", "color3", spec.base_color_tex, colorspace="srgb_texture")
        base_src = "base_color_tex"
    else:
        const = ng.addNode("constant", "base_color_const", "color3")
        _add_input(const, "value", "color3", value=spec.base_color_const)
        base_src = "base_color_const"

    if "base_color_tint" in spec.lcd_ports:
        tint = ng.addNode("multiply", "base_color_tinted", "color3")
        _add_input(tint, "in1", "color3", nodename=base_src)
        _add_input(tint, "in2", "color3", interfacename="base_color_tint")
        base_src = "base_color_tinted"

    # Overlays mixed over base color, each by its density port.
    for i, ov in enumerate(spec.overlays, start=1):
        ov_tex = f"overlay{i}_tex"
        _image(ov_tex, "color3", ov.texture, colorspace="srgb_texture")
        mixn = ng.addNode("mix", f"base_color_overlay{i}", "color3")
        _add_input(mixn, "bg", "color3", nodename=base_src)
        _add_input(mixn, "fg", "color3", nodename=ov_tex)
        _add_input(mixn, "mix", "float", interfacename=ov.density_port)
        base_src = f"base_color_overlay{i}"

    # Maskset blend over base color.
    if spec.maskset_tex and "maskset_blend" in spec.lcd_ports:
        _image("maskset_tex", "color3", spec.maskset_tex, colorspace="srgb_texture")
        maskn = ng.addNode("mix", "base_color_masked", "color3")
        _add_input(maskn, "bg", "color3", nodename=base_src)
        _add_input(maskn, "fg", "color3", nodename="maskset_tex")
        _add_input(maskn, "mix", "float", interfacename="maskset_blend")
        base_src = "base_color_masked"

    ng.addOutput("base_color_out", "color3").setNodeName(base_src)

    # --- Roughness: source -> bias -> out ---
    if spec.roughness_tex:
        _image("roughness_tex", "float", spec.roughness_tex)
        rough_src = "roughness_tex"
    else:
        const = ng.addNode("constant", "roughness_const", "float")
        _add_input(const, "value", "float", value=spec.roughness_const)
        rough_src = "roughness_const"
    if "roughness_bias" in spec.lcd_ports:
        biased = ng.addNode("add", "roughness_biased", "float")
        _add_input(biased, "in1", "float", nodename=rough_src)
        _add_input(biased, "in2", "float", interfacename="roughness_bias")
        rough_src = "roughness_biased"
    ng.addOutput("roughness_out", "float").setNodeName(rough_src)

    # --- Metalness (texture or constant) ---
    if spec.metalness_tex:
        _image("metalness_tex", "float", spec.metalness_tex)
        ng.addOutput("metalness_out", "float").setNodeName("metalness_tex")
        has_metal_out = True
    else:
        has_metal_out = False

    # --- Normal (texture only) ---
    if spec.normal_tex:
        _image("normal_tex", "vector3", spec.normal_tex)
        nmap = ng.addNode("normalmap", "surface_normal", "vector3")
        _add_input(nmap, "in", "vector3", nodename="normal_tex")
        ng.addOutput("normal_out", "vector3").setNodeName("surface_normal")
        has_normal_out = True
    else:
        has_normal_out = False

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
    if spec.transmission > 0:
        _add_input(shader, "transmission_weight", "float", value=spec.transmission)
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
