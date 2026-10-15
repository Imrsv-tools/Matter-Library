"""The scale-test scene (Phase19 19.2, click 2): objects at real size wearing library materials,
with UV-scale errors planted in it, for the scale view to expose.

    blender --background --factory-startup --python tools/parity/scale_test_scene.py -- <out_dir> [--smoke]

Writes ``<out_dir>/scale_test.blend`` and, beside it, ``scale_test.record.json``: each object, its
material and what it plants (or that it is correct). The record is the click's answer key: the
lead names the wrong objects BEFORE reading it, and nothing is inferred from object names.

The materials are APPENDED from the committed Matter asset library (``blender/asset_library``), as
a person drags them in, so each carries the size stamp the scale view reads (D-5).

``--smoke`` (the phase's one real-path smoke): registers the add-on from the repo for this session,
turns the scale view on, checks every slot against the record (its grid and its uv_scale), turns it
off, checks every slot is its own material again, and renders both states to
``scale_test_on.png`` / ``scale_test_off.png``.
"""

import json
import math
import sys
from pathlib import Path

import bmesh
import bpy

REPO = Path(__file__).resolve().parent.parent.parent
LIB = REPO / "blender" / "asset_library" / "MatterLibrary.blend"
KIT = REPO / "library" / "kits" / "MakeHuman_Body_v01" / "MakeHuman_Body_v01.usda"
TEETH_KIT = REPO / "library" / "kits" / "MakeHuman_Teeth_v01" / "MakeHuman_Teeth_v01.usda"
ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = Path(ARGS[0])
SMOKE = "--smoke" in ARGS

OAK = "Oak_Natural_Clean_Base_s1_v01"                 # 0.8 m (off its tag)
CONCRETE = "Concrete_Polished_Clean_Base_s1_v01"      # 3 m (off its tag)
GRANITE = "Granite_Polished_Clean_Base_s1_v01"        # 0.4 m
COPPER = "Copper_Verdigris_Aged_Base_s01_v01"         # 0.1 m
STEEL = "MildSteel_Raw_Clean_Base_s01_v01"            # 0.3 m
SKIN = "Skin_FitzpatrickIII_Clean_Base_s001_v01"      # 1 cm
TEETH = "Teeth_Natural_Clean_Base_sUKN_v01"           # fitted, tiles nothing
GRID1 = "Diagnostic_ScaleGrid_Clean_Base_s1_v01"      # the 1 m reference


def factory_only():
    names = sorted(o.name for o in bpy.data.objects)
    if names != ["Camera", "Cube", "Light"]:
        raise SystemExit(f"not the factory scene: {names}")          # Learnings B10
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)


def append(names):
    with bpy.data.libraries.load(str(LIB), link=False) as (src, dst):
        missing = [n for n in names if n not in src.materials]
        if missing:
            raise SystemExit(f"not in the library: {missing}")
        dst.materials = list(names)
    return {m.name: m for m in dst.materials}


def box(name, size, loc, mat, uv_tile):
    """A box ``size`` metres, resting on the floor at ``loc``. ``uv_tile`` None: Blender's default
    0-1 per face (the error a fresh object carries); else each face's UVs are metres / uv_tile."""
    sx, sy, sz = size
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts:
        v.co.x *= sx; v.co.y *= sy; v.co.z = (v.co.z + 0.5) * sz
    uv = bm.loops.layers.uv.new("UVMap")
    for f in bm.faces:
        n = f.normal
        ax = max(range(3), key=lambda i: abs(n[i]))
        u_ax, v_ax = [(1, 2), (0, 2), (0, 1)][ax]
        for loop in f.loops:
            co = loop.vert.co
            if uv_tile is None:
                lo_u = min(l.vert.co[u_ax] for l in f.loops); hi_u = max(l.vert.co[u_ax] for l in f.loops)
                lo_v = min(l.vert.co[v_ax] for l in f.loops); hi_v = max(l.vert.co[v_ax] for l in f.loops)
                loop[uv].uv = ((co[u_ax] - lo_u) / (hi_u - lo_u), (co[v_ax] - lo_v) / (hi_v - lo_v))
            else:
                loop[uv].uv = (co[u_ax] / uv_tile, co[v_ax] / uv_tile)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    me.materials.append(mat)
    return ob


def plane(name, w, h, loc, rot, mat, uv_tile):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    vs = [bm.verts.new(v) for v in ((0, 0, 0), (w, 0, 0), (w, h, 0), (0, h, 0))]
    f = bm.faces.new(vs)
    uv = bm.loops.layers.uv.new("UVMap")
    for loop in f.loops:
        loop[uv].uv = (loop.vert.co.x / uv_tile, loop.vert.co.y / uv_tile)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location, ob.rotation_euler = loc, rot
    me.materials.append(mat)
    return ob


def import_kit(kit, keep=None):
    """A part-mesh kit's meshes (those named ``keep*``, or all), unparented with their world
    transform kept (the importer's Y-up rotation lives on the parent); everything else removed."""
    bpy.ops.object.select_all(action="DESELECT")
    bpy.ops.wm.usd_import(filepath=str(kit))
    imported = list(bpy.context.selected_objects)
    meshes = [o for o in imported if o.type == "MESH" and (keep is None or o.name.startswith(keep))]
    bpy.context.view_layer.update()
    for o in meshes:
        world = o.matrix_world.copy()
        o.parent = None
        o.matrix_world = world
    for o in imported:
        if o not in meshes:
            bpy.data.objects.remove(o, do_unlink=True)
    return meshes


def light():
    """Material Preview's own default studio HDRI, so a render matches the lead's view."""
    sc = bpy.context.scene
    wnt = sc.world.node_tree
    env = wnt.nodes.new("ShaderNodeTexEnvironment")
    env.image = bpy.data.images.load(
        str(Path(bpy.utils.system_resource("DATAFILES", path="studiolights/world")) / "forest.exr"))
    wnt.links.new(env.outputs["Color"], wnt.nodes["Background"].inputs["Color"])
    wnt.nodes["Background"].inputs["Strength"].default_value = 1.0


def build():
    factory_only()
    light()
    m = append([OAK, CONCRETE, GRANITE, COPPER, STEEL, SKIN, TEETH, GRID1])
    record = []

    def note(ob, mat, planted, expect):
        record.append({"object": ob.name, "material": mat, "planted": planted, "expect": expect})

    plane("Floor", 9.0, 5.0, (-4.5, -2.5, 0), (0, 0, 0), m[OAK], 0.8)
    note(bpy.data.objects["Floor"], OAK, None, "right: the 1 m grid at true size (Oak records 0.8 m)")
    plane("Wall", 9.0, 3.0, (-4.5, 2.5, 0), (math.radians(90), 0, 0), m[CONCRETE], 3.0)
    note(bpy.data.objects["Wall"], CONCRETE, None, "right: the 1 m grid at true size (Concrete records 3 m)")
    ob = box("Reference_cube_1m", (1, 1, 1), (-3.4, 0.3, 0), m[GRID1], 1.0)
    note(ob, GRID1, None, "right: the 1 m reference, one tile per face")
    ob = box("Granite_block", (0.8, 0.6, 0.5), (-1.9, 0.0, 0), m[GRANITE], 0.4)
    note(ob, GRANITE, None, "right: the 1 m grid at true size (Granite records 0.4 m)")
    ob = box("Copper_box", (1, 1, 1), (-0.4, 0.0, 0), m[COPPER], None)
    note(ob, COPPER, "Blender's default 0-1 UVs on a 1 m box: one 10 cm tile across each face",
         "WRONG: its 10 cm grid drawn 10x too large (one 10 cm cell per metre)")
    # the fitted teeth on their own part mesh (the lead, click 2: teeth on a plain box "is just
    # strange"); drawn enlarged so they can be seen across the set: the hatch has no size to judge
    teeth = import_kit(TEETH_KIT)
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ v.co for o in teeth for v in o.data.vertices]
    width = max(p.x for p in pts) - min(p.x for p in pts)
    grow = round(0.35 / width)
    cx = (max(p.x for p in pts) + min(p.x for p in pts)) / 2
    cy = (max(p.y for p in pts) + min(p.y for p in pts)) / 2
    for o in teeth:
        o.name = f"MakeHuman_{o.name.split('.')[0].lower()}"
        o.scale = [s * grow for s in o.scale]
        o.location = ((o.location.x - cx) * grow + 0.9, (o.location.y - cy) * grow - 0.8,
                      (o.location.z - min(p.z for p in pts)) * grow)
        o.data.materials.clear()
        o.data.materials.append(m[TEETH])
        note(o, TEETH, None, f"the hatch: a fitted picture tiles nothing (RD-P18-8), so it has no "
             f"grid size (the teeth part mesh, drawn {grow}x real size so it can be seen)")
    ob = box("Steel_crate", (0.6, 0.6, 0.6), (3.3, 0.2, 0), m[STEEL], 0.3)
    ob.scale = (2.5, 2.5, 2.5)
    note(ob, STEEL, "a 0.6 m crate with right UVs, brought in at 2.5x its size (1.5 m)",
         "WRONG: its 10 cm grid drawn 2.5x too large")

    body = import_kit(KIT, keep="Body")[0]     # the kit brings Body, Lips and Nails
    body.name = "MakeHuman_body"
    body.location = (1.9, 0.3, 0)
    body.data.materials.clear()
    body.data.materials.append(m[SKIN])
    note(body, SKIN, "the skin (1 cm tile) on the body's raw atlas, no uv_scale correction "
         "(one UV unit is about 1.7 m of body)", "WRONG: its 1 cm grid drawn about 170x too large")
    bpy.context.view_layer.update()
    zs = [(body.matrix_world @ v.co).z for v in body.data.vertices]   # the importer rotates Y-up
    h = max(zs) - min(zs)
    body.location.z -= min(zs)                 # feet on the floor (the kit's origin is not at them)
    if not 1.4 < h < 2.1:
        raise SystemExit(f"the body imported at {h:.2f} m tall, not real size (Learnings B7)")
    return record


def frame_view():
    """Every 3D view: Material Preview, the whole set in frame, the sidebar open (Matter tab)."""
    from mathutils import Euler, Vector
    rot = Euler((math.radians(78), 0, 0)).to_quaternion()
    target = Vector((0.0, 0.6, 1.0))
    for screen in bpy.data.screens:
        for a in screen.areas:
            if a.type == "VIEW_3D":
                sp = a.spaces.active
                sp.shading.type = "MATERIAL"
                sp.overlay.show_overlays = False
                sp.show_gizmo = False
                sp.show_region_ui = True
                sp.lens = 70
                r3 = sp.region_3d
                r3.view_perspective = "PERSP"
                r3.view_rotation = rot
                r3.view_location = target
                r3.view_distance = 11.0


def render(path):
    sc = bpy.context.scene
    cam = bpy.data.objects.get("SmokeCam")
    if cam is None:
        bpy.ops.object.camera_add(location=(0.0, -10.2, 3.2), rotation=(math.radians(78), 0, 0))
        cam = bpy.context.object
        cam.name = "SmokeCam"
        cam.data.lens = 35
    sc.camera = cam
    sc.render.engine = "BLENDER_EEVEE"
    sc.render.resolution_x, sc.render.resolution_y = 1600, 900
    sc.view_settings.view_transform = "Standard"
    sc.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def smoke(record):
    """Scale view on: every slot wears the grid D-4 names, at the uv_scale D-4 computes; off: back."""
    sys.path.insert(0, str(REPO / "blender" / "addons"))
    import imrsv_lcd_export
    from imrsv_lcd_export import scale_view as SV, scale_view_rules as R
    imrsv_lcd_export.register()
    lib = bpy.context.preferences.filepaths.asset_libraries.new(name="Matter (smoke)", directory=str(LIB.parent))
    own = {r["object"]: bpy.data.objects[r["object"]].material_slots[0].material.name for r in record}
    fails = []
    bpy.ops.matter.scale_view(mode="ON")
    for r in record:
        ob = bpy.data.objects[r["object"]]
        mat = ob.material_slots[0].material
        src = bpy.data.materials[own[r["object"]]]
        mpt = src.get("ml_meters_per_tile")
        grid = R.grid_for(mpt, R.tag_of(r["material"]))
        want = R.uv_scale_for((1.0, 1.0), grid, mpt)
        place, _ = SV._place2d(mat)
        got = tuple(place.inputs["uv_scale"].default_value[:2]) if place else None
        ok = (SV.COPY in mat and mat.get("ml_article") == R.grid_article(grid)
              and got is not None and all(abs(a - b) < 1e-6 for a, b in zip(got, want)))
        print(f"  [{'PASS' if ok else 'FAIL'}] ON  {r['object']}: {r['material']} -> {mat.get('ml_article')} "
              f"uv_scale {got} (want {grid} at {want})")
        fails += [] if ok else [r["object"]]
    report = json.loads(bpy.context.scene[SV.REPORT])
    off = sorted(report["off_scale"])
    print("  off their scale option:", off)
    if not any(OAK in s for s in off) or not any(CONCRETE in s for s in off):
        fails.append("the report lists Oak and Concrete as off their option")
    render(OUT / "scale_test_on.png")
    bpy.ops.matter.scale_view(mode="OFF")
    for r in record:
        mat = bpy.data.objects[r["object"]].material_slots[0].material
        ok = mat.name == own[r["object"]]
        print(f"  [{'PASS' if ok else 'FAIL'}] OFF {r['object']}: {mat.name}")
        fails += [] if ok else [r["object"] + " (off)"]
    left = [m.name for m in bpy.data.materials if SV.COPY in m]
    if left:
        fails.append(f"grid copies left after OFF: {left}")
    render(OUT / "scale_test_off.png")
    bpy.context.preferences.filepaths.asset_libraries.remove(lib)
    imrsv_lcd_export.unregister()
    print(f"SMOKE {'FAIL' if fails else 'PASS'}: {fails}")
    return not fails


record = build()
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "scale_test.record.json").write_text(json.dumps({"objects": record}, indent=2) + "\n", encoding="utf-8")
ok = smoke(record) if SMOKE else True
frame_view()
bpy.ops.wm.save_as_mainfile(filepath=str(OUT / "scale_test.blend"))
print("SCALE_TEST_OK", OUT)
sys.exit(0 if ok else 1)
