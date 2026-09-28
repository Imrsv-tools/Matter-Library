"""Disposable probe (research 260928_R_HairAndNailRendering): the character's own hair cards,
backlit, three ways side by side. A = the library's Hair_Natural (opaque surface, hard cut-out);
B = A + thin-walled translucency (light through the fibre); C = B + soft coverage.

Run:  blender --python docs/Planning/Research/260928_R_HairAndNailRendering_probe.py
(Blender 5.2; it builds a scene of its own, "P08 hair probe", and touches nothing else.)"""
import sys
from pathlib import Path
import bpy

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "blender/masters"))
import load_article  # noqa: E402

SCENE_USD = REPO / "tools/parity/scene/character_scene.usda"
CUT = REPO / "tools/parity/scene/cutouts"
MATS = REPO / "MatterLibrary/materials"
TINT = (0.35, 0.22, 0.15)
BASE = (0.78, 0.68, 0.52)
COL = tuple(b * t for b, t in zip(BASE, TINT))
CAST = {"Body": "Skin_FitzpatrickIII", "Lips": "Lips_Natural", "Sclera": "Sclera_Natural",
        "Iris": "Iris_Brown", "Pupil": "Pupil_Dark", "Cornea": "Cornea_Clear"}
HAIR = ("Hair", "Brows", "Lashes")
KEEP = set(CAST) | set(HAIR)


def mtlx(stem):
    return next(MATS.rglob(f"{stem}_Clean_Base_s001_v01.mtlx"))


# a clean scene of its own, so nothing else in the file is touched
scene = bpy.data.scenes.new("P08 hair probe")
bpy.context.window.scene = scene
bpy.ops.wm.usd_import(filepath=str(SCENE_USD))
for ob in list(scene.objects):
    if ob.type == "MESH" and ob.name not in KEEP:
        bpy.data.objects.remove(ob, do_unlink=True)
    elif ob.type in ("CAMERA", "LIGHT"):
        bpy.data.objects.remove(ob, do_unlink=True)

for part, stem in CAST.items():
    ob = scene.objects.get(part)
    if ob:
        ob.data.materials.clear()
        ob.data.materials.append(load_article.build(mtlx(stem)))


def library_hair(part):
    m = load_article.build(REPO / "MatterLibrary/materials/biological/keratin/Hair_Natural_Clean_Base_s001_v01.mtlx",
                           {"base_color_tint": TINT}, name=f"A_{part}", cutout_map=CUT / f"{part}.png")
    return m


def probe_hair(part, soft):
    m = bpy.data.materials.new(f"{'C' if soft else 'B'}_{part}")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    N = nt.nodes.new
    L = nt.links.new
    uv = N("ShaderNodeUVMap")                       # blank name: the mesh's own map (B1)
    img = N("ShaderNodeTexImage")
    img.image = bpy.data.images.load(str(CUT / f"{part}.png"), check_existing=True)
    img.image.colorspace_settings.name = "Non-Color"
    L(uv.outputs["UV"], img.inputs["Vector"])
    tan = N("ShaderNodeTangent")
    tan.direction_type = "UV_MAP"
    p = N("ShaderNodeBsdfPrincipled")
    t = 0.6                                          # the share of the diffuse that passes through
    p.inputs["Base Color"].default_value = (*[c * (1 - t) for c in COL], 1)
    p.inputs["Roughness"].default_value = 0.4
    p.inputs["IOR"].default_value = 1.55
    p.inputs["Anisotropic"].default_value = 0.8
    L(tan.outputs["Tangent"], p.inputs["Tangent"])
    tr = N("ShaderNodeBsdfTranslucent")
    tr.inputs["Color"].default_value = (*[min(1.0, c * t * 1.6) for c in COL], 1)
    add = N("ShaderNodeAddShader")
    L(p.outputs["BSDF"], add.inputs[0])
    L(tr.outputs["BSDF"], add.inputs[1])
    clear = N("ShaderNodeBsdfTransparent")
    mix = N("ShaderNodeMixShader")
    if soft:
        L(img.outputs["Color"], mix.inputs["Fac"])
    else:
        gt = N("ShaderNodeMath")
        gt.operation = "GREATER_THAN"
        gt.inputs[1].default_value = 0.5
        L(img.outputs["Color"], gt.inputs[0])
        L(gt.outputs["Value"], mix.inputs["Fac"])
    L(clear.outputs["BSDF"], mix.inputs[1])
    L(add.outputs["Shader"], mix.inputs[2])
    out = N("ShaderNodeOutputMaterial")
    L(mix.outputs["Shader"], out.inputs["Surface"])
    return m


heads = [o for o in scene.objects if o.type == "MESH"]
variants = {"A": library_hair, "B": lambda p: probe_hair(p, False), "C": lambda p: probe_hair(p, True)}
for i, (key, make) in enumerate(variants.items()):
    dx = (i - 1) * 0.42
    for src in heads:
        ob = src if key == "B" else src.copy()
        if key != "B":
            ob.data = src.data.copy()
            scene.collection.objects.link(ob)
        ob.location.x += dx
        if src.name.split(".")[0] in HAIR:
            part = src.name.split(".")[0]
            ob.data.materials.clear()
            ob.data.materials.append(make(part))

hair = scene.objects["Hair"]
cz = hair.matrix_world.translation.z + sum((hair.matrix_world @ v.co).z for v in hair.data.vertices[:1]) * 0
top = max((hair.matrix_world @ v.co).z for v in hair.data.vertices)
head_z = top - 0.12
bpy.ops.object.camera_add(location=(0, -1.9, head_z), rotation=(1.5708, 0, 0))
scene.camera = bpy.context.object
scene.camera.data.lens = 55
bpy.ops.object.light_add(type="AREA", location=(0, 1.2, head_z + 0.5))
back = bpy.context.object
back.data.energy = 400
back.data.size = 1.5
back.data.color = (1.0, 0.92, 0.8)
back.rotation_euler = (-2.3, 0, 0)
bpy.ops.object.light_add(type="AREA", location=(-1.2, -1.5, head_z + 0.6))
key = bpy.context.object
key.data.energy = 120
key.data.size = 1.0
key.rotation_euler = (0.9, 0, -0.6)
world = bpy.data.worlds.new("probe world")
scene.world = world
world.color = (0.05, 0.05, 0.06)
scene.render.engine = "CYCLES"
scene.cycles.preview_samples = 64
for i, lab in enumerate(("A: library now", "B: + light through the fibre", "C: + soft edges")):
    bpy.ops.object.text_add(location=((i - 1) * 0.42 - 0.17, -0.3, head_z - 0.33), rotation=(1.5708, 0, 0))
    txt = bpy.context.object
    txt.data.body = lab
    txt.data.size = 0.035


def view():
    for win in bpy.context.window_manager.windows:
        for area in win.screen.areas:
            if area.type == "VIEW_3D":
                sp = area.spaces.active
                sp.shading.type = "RENDERED"
                sp.region_3d.view_perspective = "CAMERA"
                sp.overlay.show_overlays = False
    return None


bpy.app.timers.register(view, first_interval=0.5)
