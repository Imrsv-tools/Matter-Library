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

USD_TYPES = {"float": "float", "vector2": "float2", "color3": "color3f", "color4": "color4f",
             "vector3": "float3", "integer": "int", "boolean": "bool"}


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
                    for f in n.findall("input[@name='file']")}
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
    text = ("#usda 1.0\n(\n    subLayers = [@" + SCENE.as_posix() + "@]\n)\n\n"
            'over "World"\n{\n'
            f'    def "Library" (\n        prepend references = @{art.path.as_posix()}@</MaterialX>\n    )\n    {{\n'
            + mat_over + "    }\n"
            '    over "Subjects"\n    {\n' + "".join(subjects) + "    }\n}\n")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return out


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
        "subjects": list(build_scene.SUBJECTS),
        "width": width,
        "samples": samples,
        "settings": settings,
        "out_dir": str(out_dir),
    }
    p = out_dir / "job.json"
    p.write_text(json.dumps(job, indent=2) + "\n", encoding="utf-8")
    return p
