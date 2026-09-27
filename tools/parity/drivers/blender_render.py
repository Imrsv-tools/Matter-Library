"""Blender driver: render every setting of a job with Cycles, headless.

    blender -b --factory-startup --python-exit-code 1 \
        --python tools/parity/drivers/blender_render.py -- <job.json>

Writes ``<out_dir>/blender/<setting id>.png``. Run by ``rig.py``; needs Blender 5.2 LTS.

The scene comes from the SAME USD file Storm renders (Blender's USD importer brings in the
meshes, their ``st``, the camera and the furniture's UsdPreviewSurface materials). The
article's material does not import (Blender converts only UsdPreviewSurface: probe P1, 0
nodes), so it is rebuilt on the Blender master by ``blender/masters/load_article.py`` and
assigned to the subjects, with the setting's sliders applied as a Creator would.

The lights are set here from the scene's own numbers (``build_scene.py``), not from the
importer's unit conversion, so the mapping is explicit and measured:

* dome: a constant world colour ``DOME_RADIANCE`` at strength ``DOME_INTENSITY x DOME_K`` —
  Storm's dome is its texture's linear value times its intensity, and so is this world;
* sun: a Sun of strength ``SUN_INTENSITY x SUN_K`` along the imported light's direction —
  a normalized UsdLux distant light's intensity is irradiance, as is a Sun's strength.

Matched lighting: no shadows, no bounce light, no reflections of other objects (Storm
has none of the three), so a difference between the columns is the material's.

Colour: the Standard view transform (a plain sRGB encode, no tone curve), like usdrecord's
``sRGB`` colour correction.
"""

from __future__ import annotations

import contextlib
import json
import math
import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / "scene"))
sys.path.insert(0, str(REPO / "blender" / "masters"))
import build_scene  # noqa: E402
import load_article  # noqa: E402

TOOL = "blender"
DOME_K = 1.0     # measured against Storm, Phase05 5.1 (see the phase doc's execution log)
SUN_K = 1.0


def _gpu() -> str:
    prefs = bpy.context.preferences.addons["cycles"].preferences
    for kind in ("OPTIX", "CUDA"):
        try:
            prefs.compute_device_type = kind
        except TypeError:
            continue
        prefs.get_devices()
        devs = [d for d in prefs.devices if d.type == kind]
        if devs:
            for d in prefs.devices:
                d.use = d.type == kind
            return kind
    return "CPU"


def setup_scene(job: dict) -> None:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.usd_import(filepath=job["settings"][0]["scene"])
    scn = bpy.context.scene
    wide = bpy.data.objects.get(job["camera"].rsplit("/", 1)[1])
    if wide is None or wide.type != "CAMERA":
        raise SystemExit(f"camera {job['camera']!r} not found after import")
    scn.camera = wide

    # lights: keep the imported sun's direction, set every value from the scene's numbers
    suns = [o for o in scn.objects if o.type == "LIGHT" and o.data.type == "SUN"]
    if len(suns) != 1:
        raise SystemExit(f"expected one sun, found {[s.name for s in suns]}")
    sun = suns[0]
    sun.data.energy = build_scene.SUN_INTENSITY * SUN_K
    sun.data.angle = math.radians(build_scene.SUN_ANGLE)
    sun.data.color = (1.0, 1.0, 1.0)
    for o in [o for o in scn.objects if o.type == "LIGHT" and o is not sun]:
        bpy.data.objects.remove(o)          # the dome arrives as a world; any extra is noise
    # Matched lighting: Storm shades each point from the unoccluded dome plus the sun, with
    # no shadows, no bounce light and no reflections of other objects. Cycles is held to the
    # same so that the only variable between the columns is the MATERIAL. Transmission rays
    # still see everything, so see-through materials show the wall behind them.
    sun.data.use_shadow = False
    for o in scn.objects:
        if o.type == "MESH":
            o.visible_shadow = False
            o.visible_diffuse = False
            o.visible_glossy = False
            o.visible_transmission = True
            o.visible_camera = True
    world = bpy.data.worlds.new("ML_ParityDome")
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    r = build_scene.DOME_RADIANCE          # the dome texture's linear value (Storm reads it)
    bg.inputs["Color"].default_value = (r, r, r, 1.0)
    bg.inputs["Strength"].default_value = build_scene.DOME_INTENSITY * DOME_K
    scn.world = world

    scn.render.engine = "CYCLES"
    scn.cycles.device = "GPU" if _gpu() != "CPU" else "CPU"
    scn.cycles.samples = int(job.get("samples", 128))
    scn.cycles.use_denoising = True
    scn.render.resolution_x = scn.render.resolution_y = int(job["width"])
    scn.render.resolution_percentage = 100
    scn.render.film_transparent = False
    scn.view_settings.view_transform = "Standard"
    scn.view_settings.look = "None"
    scn.view_settings.exposure = 0.0
    scn.view_settings.gamma = 1.0
    scn.display_settings.display_device = "sRGB"
    scn.render.image_settings.file_format = "PNG"
    scn.render.image_settings.color_mode = "RGB"
    scn.render.image_settings.color_depth = "8"


def subjects(job: dict) -> list:
    names = [p.rsplit("/", 1)[1] for p in job["subjects"]]
    objs = [bpy.data.objects.get(n) for n in names]
    missing = [n for n, o in zip(names, objs) if o is None]
    if missing:
        raise SystemExit(f"subjects not found after import: {missing} "
                         f"(have {[o.name for o in bpy.data.objects]})")
    for o in objs:
        if "st" not in o.data.uv_layers:
            raise SystemExit(f"{o.name} has no 'st' UV map (have {list(o.data.uv_layers.keys())})")
    return objs


@contextlib.contextmanager
def hide(job: dict, spec: dict):
    """Hide a view's `hide` prims from the render for the duration (a character's mouth view)."""
    objs = [bpy.data.objects.get(p.rsplit("/", 1)[1]) for p in spec.get("hide", [])]
    if None in objs:
        raise SystemExit(f"view hides a prim not found after import: {spec.get('hide')}")
    for o in objs:
        o.hide_render = True
    try:
        yield
    finally:
        for o in objs:
            o.hide_render = False


def mask_colours(job: dict, objs: list) -> list:
    """Each subject's flat mask colour: the job's ``mask_colours`` (a character job, one per part),
    else the test scene's sphere red, cube green, floor blue."""
    given = job.get("mask_colours")
    if given:
        return [tuple(given[p]) for p in job["subjects"]]
    return [(1, 0, 0), (0, 1, 0), (0, 0, 1)][:len(objs)]


def render_mask(objs: list, png: Path, colours: list) -> None:
    """One flat colour per subject, all else black."""
    scn = bpy.context.scene
    keep = {o.name: list(o.data.materials) for o in objs}
    world, samples, denoise = scn.world, scn.cycles.samples, scn.cycles.use_denoising
    view = scn.view_settings.view_transform
    black = bpy.data.worlds.new("ML_MaskBlack")
    black.use_nodes = True
    black.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.0
    hidden = [o for o in scn.objects if o.type == "MESH" and o not in objs]
    for o in hidden:
        o.hide_render = True
    for o, rgb in zip(objs, colours):
        m = bpy.data.materials.new(f"ML_Mask_{o.name}")
        nt = m.node_tree
        nt.nodes.clear()
        em = nt.nodes.new("ShaderNodeEmission")
        em.inputs["Color"].default_value = (*rgb, 1.0)
        out = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(em.outputs[0], out.inputs["Surface"])
        o.data.materials.clear()
        o.data.materials.append(m)
    scn.world, scn.cycles.samples, scn.cycles.use_denoising = black, 16, False
    scn.view_settings.view_transform = "Standard"
    scn.render.filepath = str(png)
    bpy.ops.render.render(write_still=True)
    scn.world, scn.cycles.samples, scn.cycles.use_denoising = world, samples, denoise
    scn.view_settings.view_transform = view
    for o in hidden:
        o.hide_render = False
    for o in objs:
        o.data.materials.clear()
        for m in keep[o.name]:
            o.data.materials.append(m)


def run(job_path: Path) -> None:
    job = json.loads(job_path.read_text(encoding="utf-8"))
    setup_scene(job)
    objs = subjects(job)
    out = Path(job["out_dir"]) / TOOL
    out.mkdir(parents=True, exist_ok=True)
    scn = bpy.context.scene
    views = job.get("views") or {"wide": {"camera": job["camera"], "suffix": ""}}
    cams = {}
    for v, spec in views.items():
        name = spec["camera"].rsplit("/", 1)[1]
        cams[v] = bpy.data.objects.get(name)
        if cams[v] is None or cams[v].type != "CAMERA":
            raise SystemExit(f"view {v!r}: camera {name!r} not found after import")
        scn.camera = cams[v]
        hidden = set(spec.get("hide", []))
        shown = [(p, o, c) for p, o, c in zip(job["subjects"], objs, mask_colours(job, objs)) if p not in hidden]
        with hide(job, spec):
            render_mask([o for _, o, _ in shown], Path(job["out_dir"]) / f"mask{spec['suffix']}.png",
                        [c for _, _, c in shown])
    # what goes on which subject: a character job binds one article per part (Phase07 7.4);
    # the test scene binds the one article to all three subjects
    bindings = job.get("bindings") or [{"subject": p, "article": job["article"]} for p in job["subjects"]]
    by_prim = {p: o for p, o in zip(job["subjects"], objs)}
    for s in job["settings"]:
        built = {}
        for b in bindings:
            a = b["article"]
            if a["name"] not in built:
                built[a["name"]] = load_article.build(Path(a["path"]), s.get("set", {}),
                                                      name=f"{a['name']}__{s['id']}")
            o = by_prim[b["subject"]]
            o.data.materials.clear()
            o.data.materials.append(built[a["name"]])
        for v, spec in views.items():
            scn.camera = cams[v]
            scn.view_settings.exposure = float(spec.get("exposure", 0.0))
            png = out / f"{s['id']}{spec['suffix']}.png"
            scn.render.filepath = str(png)
            with hide(job, spec):
                bpy.ops.render.render(write_still=True)
            print(f"blender: wrote {png}")
        scn.view_settings.exposure = 0.0


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if len(argv) != 1:
        raise SystemExit("usage: blender -b --python blender_render.py -- <job.json>")
    run(Path(argv[0]))
