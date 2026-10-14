"""Blender side of the thumbnail tool: one article, its showcase pictures (Phase17).

    blender -b --factory-startup --python-exit-code 1 \
        --python tools/thumbnails/showcase_blender.py -- <thumb_job.json>

Run by ``make_thumbnails.py``, which writes the job. Writes ``<out_dir>/<view>.png`` for each view
and ``<out_dir>/render.json`` (the device, Blender's version, the seconds per view).

The geometry is the rig's: the job's ``scene`` is a rig setting scene (``tools/parity/job.py``), so
the subjects arrive with their ``st`` already rescaled by the article's ``meters_per_tile``. Every
imported prim the subject does not ``keep`` is removed (the rig's lights, wall, ruler, cameras).
The article is built on its Blender master (``blender/masters/load_article.py``), as the rig's
Blender column builds it. Everything else is set here, from the job's ``look``: the HDRI, the key
light, the backdrop, the cameras, the tone curve, the exposure, the samples and the seed.

Coordinates in the job are the rig's (USD: Y up, metres). The importer turns a Y-up stage into
Blender's Z up, so this script does the same to its own objects: (x, y, z) -> (x, -z, y).
"""

from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import bpy
from mathutils import Matrix, Vector

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "tools" / "parity" / "drivers"))
sys.path.insert(0, str(REPO / "tools" / "parity" / "scene"))
sys.path.insert(0, str(REPO / "blender" / "masters"))
import blender_render  # noqa: E402  (pick_device: the rig's device choice)
import load_article  # noqa: E402

Y_UP = Matrix.Rotation(math.radians(90.0), 4, "X")      # the rig's space -> Blender's


def v(p) -> Vector:
    """A point in the rig's space, in Blender's."""
    return Y_UP @ Vector(p)


def camera(name: str, spec: dict):
    cam = bpy.data.cameras.new(name)
    cam.lens = spec["focal"]
    cam.sensor_fit = "HORIZONTAL"
    cam.sensor_width = 36.0
    cam.clip_start, cam.clip_end = 0.02, 100.0
    obj = bpy.data.objects.new(name, cam)
    pitch, yaw = (math.radians(a) for a in spec["rot"])
    # USD rotateXYZ: X first, then Y; then the stage's Y-up turn
    obj.matrix_world = (Y_UP @ Matrix.Translation(Vector(spec["pos"]))
                        @ Matrix.Rotation(yaw, 4, "Y") @ Matrix.Rotation(pitch, 4, "X"))
    bpy.context.scene.collection.objects.link(obj)
    return obj


def backdrop(look: dict):
    """A floor that sweeps up into a back wall, extruded across x. Built in the rig's space."""
    zc, r = look["backdrop_curve_z"], look["backdrop_radius"]
    prof = [(0.0, look["backdrop_floor_front"]), (0.0, zc)]
    for k in range(1, 16):
        a = 0.5 * math.pi * k / 16
        prof.append((r - r * math.cos(a), zc - r * math.sin(a)))
    prof += [(r, zc - r), (look["backdrop_top"], zc - r)]
    w = look["backdrop_width"] / 2
    verts = [v((x, y, z)) for (y, z) in prof for x in (-w, w)]
    faces = [(2 * i, 2 * i + 1, 2 * i + 3, 2 * i + 2) for i in range(len(prof) - 1)]
    me = bpy.data.meshes.new("ML_Backdrop")
    me.from_pydata([tuple(p) for p in verts], [], faces)
    me.update()
    for p in me.polygons:
        p.use_smooth = True
    obj = bpy.data.objects.new("ML_Backdrop", me)
    mat = bpy.data.materials.new("ML_Backdrop")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF") or mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
    a = look["backdrop_albedo"]
    bsdf.inputs["Base Color"].default_value = (a, a, a, 1.0)
    bsdf.inputs["Roughness"].default_value = look["backdrop_roughness"]
    me.materials.append(mat)
    bpy.context.scene.collection.objects.link(obj)
    # face it towards the camera side: the normals must point up and forward
    up = sum((p.normal for p in me.polygons[:1]), Vector())
    if up.z < 0:
        me.flip_normals()
    return obj


def area_light(look: dict, which: str):
    """A square soft light (``key`` or ``rim``): lit and reflected, never seen by the camera."""
    lamp = bpy.data.lights.new(f"ML_{which}", "AREA")
    lamp.shape = "SQUARE"
    lamp.size = look[f"{which}_size"]
    lamp.energy = look[f"{which}_power"]
    if f"{which}_spread" in look:
        lamp.spread = math.radians(look[f"{which}_spread"])
    obj = bpy.data.objects.new(f"ML_{which}", lamp)
    pos, aim = v(look[f"{which}_pos"]), v(look[f"{which}_aim"])
    obj.matrix_world = Matrix.Translation(pos) @ (aim - pos).to_track_quat("-Z", "Y").to_matrix().to_4x4()
    obj.visible_camera = False
    bpy.context.scene.collection.objects.link(obj)
    return obj


def world(look: dict):
    w = bpy.data.worlds.new("ML_Showcase")
    w.use_nodes = True
    nt = w.node_tree
    nt.nodes.clear()
    env = nt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(look["hdri"], check_existing=True)
    coord = nt.nodes.new("ShaderNodeTexCoord")
    mapping = nt.nodes.new("ShaderNodeMapping")
    mapping.inputs["Rotation"].default_value = (0.0, 0.0, math.radians(look["hdri_rotation"]))
    bg = nt.nodes.new("ShaderNodeBackground")
    bg.inputs["Strength"].default_value = look["hdri_strength"]
    out = nt.nodes.new("ShaderNodeOutputWorld")
    nt.links.new(coord.outputs["Generated"], mapping.inputs["Vector"])
    nt.links.new(mapping.outputs["Vector"], env.inputs["Vector"])
    nt.links.new(env.outputs["Color"], bg.inputs["Color"])
    nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    bpy.context.scene.world = w


def setup(job: dict) -> list:
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.usd_import(filepath=job["scene"])
    scn = bpy.context.scene
    keep = {p.rsplit("/", 1)[1] for p in job["keep"]}
    for o in list(scn.objects):
        if o.type in ("MESH", "LIGHT", "CAMERA") and o.name not in keep:
            bpy.data.objects.remove(o)
    subjects = [bpy.data.objects.get(n) for n in sorted(keep)]
    if None in subjects:
        raise SystemExit(f"subjects not found after import: {sorted(keep)} "
                         f"(have {[o.name for o in bpy.data.objects]})")
    for o in subjects:
        if "st" not in o.data.uv_layers:
            raise SystemExit(f"{o.name} has no 'st' UV map")
        lo = min((o.matrix_world @ Vector(c)).z for c in o.bound_box)
        print(f"thumbnails: subject {o.name} rests at z = {lo:.4f}")
    a = job["article"]
    mat = load_article.build(Path(a["path"]), {}, name=f"{a['name']}__thumbnail")
    for o in subjects:
        o.data.materials.clear()
        o.data.materials.append(mat)

    look = job["look"]
    backdrop(look)
    area_light(look, "key")
    area_light(look, "rim")
    world(look)
    scn.render.engine = "CYCLES"
    scn.cycles.samples = int(job["samples"])
    scn.cycles.seed = int(job["seed"])
    scn.cycles.use_animated_seed = False
    scn.cycles.use_denoising = True
    scn.render.resolution_x = scn.render.resolution_y = int(job["size"])
    scn.render.resolution_percentage = 100
    scn.render.film_transparent = False
    scn.view_settings.view_transform = look["view_transform"]
    scn.view_settings.look = "None"
    scn.view_settings.exposure = float(look["exposure"])
    scn.view_settings.gamma = 1.0
    scn.display_settings.display_device = "sRGB"
    scn.render.image_settings.file_format = "PNG"
    scn.render.image_settings.color_mode = "RGB"
    scn.render.image_settings.color_depth = "8"
    cams = {name: camera(f"ML_Cam_{name}", spec) for name, spec in job["views"].items()}
    scn.camera = next(iter(cams.values()))
    return cams


def run(job_path: Path) -> None:
    job = json.loads(job_path.read_text(encoding="utf-8"))
    cams = setup(job)
    scn = bpy.context.scene
    device = blender_render.pick_device(scn)      # last: it renders, so the scene must be set
    out = Path(job["out_dir"])
    out.mkdir(parents=True, exist_ok=True)
    seconds = {}
    for name, cam in cams.items():
        scn.camera = cam
        scn.render.filepath = str(out / f"{name}.png")
        t = time.perf_counter()
        bpy.ops.render.render(write_still=True)
        seconds[name] = round(time.perf_counter() - t, 2)
        print(f"thumbnails: wrote {scn.render.filepath} in {seconds[name]} s")
    (out / "render.json").write_text(json.dumps(
        {"blender": bpy.app.version_string, "engine": "Cycles", "device": device,
         "seconds": seconds}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if len(argv) != 1:
        raise SystemExit("usage: blender -b --python showcase_blender.py -- <thumb_job.json>")
    run(Path(argv[0]))
