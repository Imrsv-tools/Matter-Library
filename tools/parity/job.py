"""The render job: *this material, these slider settings, this scene, write pictures here*.

A job is a ``job.json`` in its output folder (``write_job`` below; the Phase06 hand-off,
``JOB_FORMAT.md``, is written at the Phase05 close), plus one
USD file per slider setting under ``scenes/``. Every driver — Storm (USDLiveView's
renderer), Blender, and later Unreal — reads the same ``job.json`` and the same scene
files, and writes ``<out>/<tool>/<setting id>.png``.

A setting's scene sublayers the rig's one test scene and adds only what the job decides:

* the article, referenced at ``/World/Library`` and bound to the three subjects;
* the subjects' ``st`` rescaled from metres to the article's tiles (÷ ``meters_per_tile``),
  so every article renders at its recorded real-world size;
* each moved slider, written by the carrier rule (LCDSchema §Carrier rule): a value on the
  bound Material's ``inputs:<port>``, and ``NG_<name>.inputs:<port>`` connected to it.
"""

from __future__ import annotations

import json
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SCENE = HERE / "scene" / "test_scene.usda"
MATERIALS = REPO / "MatterLibrary" / "materials"

sys.path.insert(0, str(HERE / "scene"))
import build_scene  # noqa: E402

STORM_SUPERSAMPLE = 4

USD_TYPES = {"float": "float", "vector2": "float2", "color3": "color3f", "color4": "color4f",
             "vector3": "float3", "integer": "int", "boolean": "bool", "filename": "asset"}


def find_article(name: str) -> Path:
    """An article by stem (or a path to its .mtlx).

    Stray punctuation or quotes around the name (copied along from prose) are ignored.
    """
    name = name.strip().strip(",.;:'\"`")
    p = Path(name)
    if p.suffix == ".mtlx" and p.is_file():
        return p.resolve()
    hits = sorted(MATERIALS.rglob(f"{p.stem}.mtlx"))
    if not hits:
        import difflib
        stems = sorted(m.stem for m in MATERIALS.rglob("*.mtlx"))
        near = difflib.get_close_matches(p.stem, stems, n=3, cutoff=0.5)
        hint = f"; did you mean {' or '.join(near)}?" if near else f"; articles: {', '.join(stems)}"
        raise SystemExit(f"no article named {name!r} under {MATERIALS}{hint}")
    return hits[0]


@dataclass
class Article:
    path: Path
    name: str
    master: str
    meters_per_tile: float
    ports: dict[str, tuple[str, str]] = field(default_factory=dict)  # port -> (mtlx type, value)
    textures: dict[str, Path] = field(default_factory=dict)          # node name -> file

    @classmethod
    def read(cls, path: Path) -> "Article":
        root = ET.parse(path).getroot()
        textures = {n.get("name"): (path.parent / f.get("value")).resolve()
                    for n in root.iter() if n.tag in ("image", "tiledimage")
                    for f in n.findall("input[@name='file']")
                    if f.get("value")}     # a cut-out's file is the binding's, not the article's
        meta = {i.get("name"): i.get("value") for i in root.iter("input")
                if i.get("name") in ("master_material", "meters_per_tile")}
        ng = root.find("nodegraph")
        ports = {i.get("name"): (i.get("type"), i.get("value")) for i in ng.findall("input")} if ng is not None else {}
        mpt = float(meta.get("meters_per_tile") or 0) or 1.0
        return cls(path, path.stem, meta.get("master_material", "Opaque"), mpt, ports, textures)


def _usd_value(mtype: str, value) -> str:
    if isinstance(value, (list, tuple)):
        return "(" + ", ".join(f"{float(v):g}" for v in value) + ")"
    if mtype in ("vector2", "color3", "vector3", "color4"):
        return "(" + ", ".join(f"{float(v):g}" for v in str(value).split(",")) + ")"
    return f"{float(value):g}"


def write_setting_scene(art: Article, setting: dict, out: Path) -> Path:
    """One setting's USD file. Refuses a slider the article does not declare."""
    mat = f"/World/Library/Materials/{art.name}"
    vals, cons = [], []
    for port, value in setting.get("set", {}).items():
        if port not in art.ports:
            raise SystemExit(f"{art.name} does not declare the slider {port!r} "
                             f"(it has: {sorted(art.ports)})")
        t = USD_TYPES[art.ports[port][0]]
        vals.append(f"                {t} inputs:{port} = {_usd_value(art.ports[port][0], value)}\n")
        cons.append(f"                    {t} inputs:{port}.connect = <{mat}.inputs:{port}>\n")
    mat_over = ""
    if vals:
        mat_over = ('        over "Materials"\n        {\n'
                    f'            over "{art.name}"\n            {{\n' + "".join(vals) +
                    f'                over "NG_{art.name}"\n                {{\n' + "".join(cons) +
                    '                }\n            }\n        }\n')
    subjects = []
    for prim, uvs in build_scene.subject_uvs().items():
        name = prim.rsplit("/", 1)[1]
        st = ", ".join(f"({s / art.meters_per_tile:.6f}, {t / art.meters_per_tile:.6f})" for s, t in uvs)
        subjects.append(
            f'        over "{name}" (\n            prepend apiSchemas = ["MaterialBindingAPI"]\n        )\n'
            f'        {{\n            texCoord2f[] primvars:st = [{st}] (\n'
            '                interpolation = "vertex"\n            )\n'
            f'            rel material:binding = <{mat}>\n        }}\n')
    # the root layer carries the stage metadata; a sublayer's is ignored (build_scene.py)
    text = ("#usda 1.0\n(\n    subLayers = [@" + SCENE.as_posix() + "@]\n"
            f'    upAxis = "{build_scene.UP_AXIS}"\n    metersPerUnit = {build_scene.METERS_PER_UNIT}\n)\n\n'
            'over "World"\n{\n'
            f'    def "Library" (\n        prepend references = @{art.path.as_posix()}@</MaterialX>\n    )\n    {{\n'
            + mat_over + "    }\n"
            '    over "Subjects"\n    {\n' + "".join(subjects) + "    }\n}\n")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return out


CHARACTER_SCENE = HERE / "scene" / "character_scene.usda"
# one flat mask colour per character part (the Blender driver renders them; compare.py scores
# each as its own region). Distinct, saturated, and far apart so an edge pixel is never mistaken.
CHARACTER_COLOURS = {"Body": (1, 0, 0), "Lips": (1, 0, 1), "Nails": (0, 1, 1),
                     "Cornea": (0.5, 0.5, 1), "Pupil": (0.5, 1, 0.5), "Iris": (1, 0.5, 0), "Sclera": (0, 1, 0),
                     "Teeth": (0, 0, 1), "Gums": (0.5, 0, 0.5), "Tongue": (1, 1, 0),
                     "Shirt": (1, 1, 1), "Trousers": (0, 0.5, 1), "Shoes": (1, 0, 0.5), "Soles": (0.5, 0.5, 0),
                     "Hair": (0.5, 1, 1), "Brows": (1, 0.5, 0.5), "Lashes": (0.5, 0, 1)}
CHARACTER_VIEWS = {"wide": ("/World/Cam", "whole body"), "face": ("/World/CamFace", "face"),
                   "hand": ("/World/CamHand", "hand"), "mouth": ("/World/CamMouth", "mouth, face hidden"),
                   "waist": ("/World/CamWaist", "waist"), "feet": ("/World/CamFeet", "feet")}
# prims a view hides (the teeth, gums and tongue sit behind closed lips on MakeHuman's body)
CHARACTER_HIDE = {"mouth": ["/World/Character/Body", "/World/Character/Lips"]}
# prims every view hides: the high-poly eye's cornea shell, which Studio's eye does not have
# (Phase09 RD-P09-4, MAP-F12). The split and `Cornea_Clear` stay; the rig's eye matches Studio's.
CHARACTER_HIDE_ALWAYS = ["/World/Character/Cornea"]


def write_character_scene(bindings: dict[str, "Article"], out: Path) -> Path:
    """The character's defaults scene (Phase07 7.4): one article bound per part.

    ``bindings`` maps a part name (``build_character.PARTS``) to its article. Each distinct
    article is referenced under its own ``/World/Library_<i>``; a bound part gets the binding
    and its st divided by that article's ``meters_per_tile`` (the scene's st is in metres, as the
    test scene's is). An unbound part keeps the scene's grey ``Unbound`` look.

    A fit part (hair, brows, lashes: ``build_character.mesh_maps``) bound to an article that
    declares ``cutout_map`` or ``base_color_map`` gets the mesh's maps on a Material instance of
    its own, by the carrier rule (LCDSchema §Cut-out map, §Base colour map: a value on the
    Material, connected into the article); its st is the atlas the maps are drawn on, so it is
    not rescaled.
    """
    import build_character  # noqa: PLC0415 (heavy: parses the pinned sources)
    uvs = build_character.part_uvs()
    atlas = build_character.atlas_parts()
    meshmaps = build_character.mesh_maps()
    libs, lib_of = [], {}           # one Library per (article, the mesh's maps)
    for part, art in bindings.items():
        key = (art.name, tuple(sorted(maps_for(part, art, meshmaps).items())))
        if key not in lib_of:
            lib_of[key] = len(libs)
            libs.append(key + (art,))
    text = ["#usda 1.0\n(\n    subLayers = [@" + CHARACTER_SCENE.as_posix() + "@]\n"
            f'    upAxis = "{build_scene.UP_AXIS}"\n    metersPerUnit = {build_scene.METERS_PER_UNIT}\n)\n\n'
            'over "World"\n{\n']
    for i, (name, maps, art) in enumerate(libs):
        body = ""
        if maps:
            mat = f"/World/Library_{i}/Materials/{name}"
            body = ('        over "Materials"\n        {\n'
                    f'            over "{name}"\n            {{\n'
                    + "".join(f'                asset inputs:{port} = @{path.as_posix()}@\n'
                              for port, path in maps)
                    + f'                over "NG_{name}"\n                {{\n'
                    + "".join(f'                    asset inputs:{port}.connect = <{mat}.inputs:{port}>\n'
                              for port, _ in maps)
                    + '                }\n            }\n        }\n')
        text.append(f'    def "Library_{i}" (\n        prepend references = @{art.path.as_posix()}@</MaterialX>\n'
                    '    )\n    {\n' + body + '    }\n')
    text.append('    over "Character"\n    {\n')
    for part, art in bindings.items():
        prim = f"/World/Character/{part}"
        if prim not in uvs:
            raise SystemExit(f"no character part {part!r} (have {sorted(p.rsplit('/', 1)[1] for p in uvs)})")
        k = 1.0 if prim in atlas else art.meters_per_tile
        st = ", ".join(f"({s / k:.5f}, {t / k:.5f})" for s, t in uvs[prim])
        key = (art.name, tuple(sorted(maps_for(part, art, meshmaps).items())))
        text.append(f'        over "{part}"\n        {{\n'
                    f'            texCoord2f[] primvars:st = [{st}] (\n'
                    '                interpolation = "faceVarying"\n            )\n'
                    f'            rel material:binding = </World/Library_{lib_of[key]}/Materials/{art.name}>\n'
                    '        }\n')
    text.append('    }\n}\n')
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("".join(text), encoding="utf-8")
    return out


def maps_for(part: str, art: "Article", meshmaps: dict[str, dict[str, Path]]) -> dict[str, Path]:
    """The mesh's maps for this binding (``cutout_map``, ``base_color_map``): each one the part
    has and the article declares as an input."""
    return {port: path for port, path in meshmaps.get(f"/World/Character/{part}", {}).items()
            if port in art.ports}


def write_character_job(bindings: dict[str, "Article"], out_dir: Path, width: int, samples: int) -> Path:
    """A character job: the defaults only (sliders are swept on the test scene), every view."""
    import build_character  # noqa: PLC0415
    out_dir.mkdir(parents=True, exist_ok=True)
    scene = write_character_scene(bindings, out_dir / "scenes" / "defaults.usda")
    meshmaps = build_character.mesh_maps()
    first = next(iter(bindings.values()))
    job = {
        "format": 1,
        "mode": "character",
        "article": {"name": first.name, "path": str(first.path), "master": first.master,
                    "meters_per_tile": first.meters_per_tile},
        # one entry per bound part: the driver builds the article on its master and assigns it;
        # `cutout_map` / `base_color_map` (a fit part) are the mesh's maps, supplied as the
        # binding's inputs
        "bindings": [{"subject": f"/World/Character/{p}", "article":
                      {"name": a.name, "path": str(a.path), "master": a.master,
                       "meters_per_tile": a.meters_per_tile}}
                     | {port: str(path) for port, path in maps_for(p, a, meshmaps).items()}
                     for p, a in bindings.items()],
        "scene": str(CHARACTER_SCENE),
        "camera": CHARACTER_VIEWS["wide"][0],
        "views": {v: {"camera": c, "suffix": view_suffix(v), "label": label}
                  | {"hide": CHARACTER_HIDE.get(v, []) + CHARACTER_HIDE_ALWAYS}
                  for v, (c, label) in CHARACTER_VIEWS.items()},
        "subjects": [f"/World/Character/{p}" for p in bindings],
        # the mask: one flat colour per subject; compare.py scores each colour as a region
        "mask_colours": {f"/World/Character/{p}": list(CHARACTER_COLOURS[p]) for p in bindings},
        "width": width,
        "samples": samples,
        "storm_supersample": STORM_SUPERSAMPLE,
        "settings": [{"id": "defaults", "label": "defaults", "set": {}, "scene": str(scene)}],
        "out_dir": str(out_dir),
    }
    p = out_dir / "job.json"
    p.write_text(json.dumps(job, indent=2) + "\n", encoding="utf-8")
    return p


def views_for(master: str) -> dict:
    """The views a job renders. An Emissive article adds the whole set at -4 stops.

    Emission is judged unclipped: Neon's luminance 12 x its pink is over display white in
    every channel, so at exposure 0 both tools draw it pure white and "agree" on nothing
    (5.4). Storm honours the USD camera's `exposure` (measured: the neon reads (225, 95,
    198) at -4); Blender's view exposure is the same multiply, before the display encode.
    """
    views = {v: {"camera": c, "suffix": view_suffix(v)} for v, c in build_scene.CAMERAS.items()}
    if master == "Emissive":
        views["dim"] = {"camera": build_scene.CAMERAS["wide"], "suffix": "__dim", "exposure": -4.0}
    return views


def view_suffix(view: str) -> str:
    """The wide view keeps the plain file name; any other view is ``<id>__<view>.png``."""
    return "" if view == "wide" else f"__{view}"


def write_job(art: Article, settings: list[dict], out_dir: Path, width: int, samples: int) -> Path:
    """Write every setting's scene and the job.json that names them."""
    out_dir.mkdir(parents=True, exist_ok=True)
    for s in settings:
        s["scene"] = str(write_setting_scene(art, s, out_dir / "scenes" / f"{s['id']}.usda"))
    job = {
        "format": 1,
        "article": {"name": art.name, "path": str(art.path), "master": art.master,
                    "meters_per_tile": art.meters_per_tile},
        "scene": str(SCENE),
        "camera": "/World/Cam",
        # every view is rendered for every setting: <tool>/<id><suffix>.png
        "views": views_for(art.master),
        "subjects": list(build_scene.SUBJECTS),
        "width": width,
        "samples": samples,
        # Storm renders at width x this and is box-filtered down (it has no anti-aliasing
        # of its own in usdrecord); Blender's own samples do the same job
        "storm_supersample": STORM_SUPERSAMPLE,
        "settings": settings,
        "out_dir": str(out_dir),
    }
    p = out_dir / "job.json"
    p.write_text(json.dumps(job, indent=2) + "\n", encoding="utf-8")
    return p
