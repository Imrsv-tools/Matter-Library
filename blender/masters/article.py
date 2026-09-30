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
            if name in ("cutout_tex", "base_color_map_tex"):
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
    return art
