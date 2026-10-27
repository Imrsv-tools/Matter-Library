"""Read one Matter article's values from its ``.mtlx`` — plain XML, no Blender, no MaterialX.

    import article
    art = article.read(Path(".../Copper_Verdigris_Aged_Base_s01_v01.mtlx"))

The one reader every driver builds a master's material from: Blender's ``load_article.py``
and the parity rig's Unreal driver (``tools/parity/drivers/unreal.py``) both import it, so
the two cannot read an article differently (Phase06; it moved here out of ``load_article.py``,
which imports ``bpy``).

The article is read by the assembler's FIXED node names — the render-role contract (LCDSchema
§Render-role texture nodes; ``tools/converters/assemble_mtlx.py``): ``<role>_tex`` is an image,
``<role>_const`` a constant. Values authored directly on ``open_pbr_surface`` (lane A:
``specular_ior``, ``base_metalness`` …) are read from the shader node. The Creator sliders'
start values are the nodegraph's interface inputs.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path


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
    # Phase18 (RD-P18-9): a picture the ARTICLE names for an input the binding may supply
    # (`base_color_map`): a fitted Character article carries its own. input -> resolved file.
    maps: dict[str, Path] = field(default_factory=dict)


# The nodes that sample a MESH's map, whose file is the input's value (the binding's, or a fitted
# article's own: ArticleData.maps), not one of the article's texture roles. Phase22 adds the shine maps.
MESH_MAP_NODES = ("cutout_tex", "base_color_map_tex", "roughness_map_tex", "normal_map_tex", "cavity_map_tex",
                  "scatter_map_tex")


def read(path: Path) -> ArticleData:
    root = ET.parse(path).getroot()
    doc_cs = root.get("colorspace")
    master = next((i.get("value") for i in root.iter("input")
                   if i.get("name") == "master_material"), "Opaque")
    art = ArticleData(path, path.stem, master)
    ng = root.find("nodegraph")
    if ng is not None:
        for i in ng.findall("input"):
            if i.get("type") == "filename":       # a picture input: a path, never a number
                art.ports[i.get("name")] = []
                if i.get("value"):
                    art.maps[i.get("name")] = (path.parent / i.get("value")).resolve()
                continue
            art.ports[i.get("name")] = _floats(i.get("value"))
        for node in ng:
            name = node.get("name", "")
            if name in MESH_MAP_NODES:
                continue        # its file is the binding's map (build's `cutout_map` / `base_color_map`)
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
            elif ng is not None and i.get("output") == f"{i.get('name')}_out":
                # Phase10: a weight a deposit covers (transmission, subsurface, coat, fuzz) reaches
                # the shader through the graph, a chain of <name>_depositN mixes toward 0. Its OWN
                # value is the first mix's bg; each target's master applies the cover itself.
                chain = sorted((m for m in ng.findall("mix")
                                if m.get("name", "").startswith(f"{i.get('name')}_deposit")),
                               key=lambda m: m.get("name"))
                bg = chain[0].find("input[@name='bg']") if chain else None
                mapped = ng.find(f"multiply[@name='{i.get('name')}_mapped']/input[@name='in2']")
                if mapped is not None:
                    # Phase22: a mesh's map x the article's own value (in2): the cavity map x
                    # specular_weight (22.2), the scatter map's factor x subsurface_radius (22.3);
                    # each target's master applies the mesh's map itself
                    art.shader[i.get("name")] = _floats(mapped.get("value"))
                elif bg is not None and bg.get("value") is not None:
                    art.shader[i.get("name")] = _floats(bg.get("value"))
                elif not chain and i.get("name") in art.ports:
                    # Phase12: a value the Creator may SET (transmission_color) reaches the shader
                    # straight from its port; the article's own value is the port's start value
                    art.shader[i.get("name")] = list(art.ports[i.get("name")])
    return art
