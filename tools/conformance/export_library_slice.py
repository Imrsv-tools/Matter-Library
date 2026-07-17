"""Phase 60sq1 E8 §5→§1→§2 end-to-end — export a slice built from the GENERATED Asset-Browser
library material (not the scaffold), the way the §6 Creator slice will.

Factory-startup (no scaffold): APPENDS the Copper material from the generated
`blender/asset_library/MatterLibrary.blend` — exactly what Blender's Asset Browser does on
assign — so the material carries the §5-authored durable `imrsv_matter_identity` property + the
frozen Principled proxy from the library, NOT a script-stamped property. Binds it to TWO meshes
sharing that ONE datablock (§2 split path) with distinct UV fits, and exports via the real
`export_lcd_usd`. The conformance gate then proves the LIBRARY material produces a conforming
lightweight asset whose identity comes from the library's own carrier.

Run:
  blender --background --factory-startup --python tools/conformance/export_library_slice.py -- <out.usda>
"""
import bpy, sys, os

REPO = "/home/peter/Documents/IMRSV_GITrepos/IMRSV_Platform/Matter-Library"
LIB = os.path.join(REPO, "blender/asset_library/MatterLibrary.blend")
MID = "Copper_Verdigris_Aged_Base_s01_v01"

argv = sys.argv
post = argv[argv.index("--") + 1:] if "--" in argv else []
out = post[0] if post else "/tmp/creator_library_slice.usda"

sys.path.insert(0, os.path.join(REPO, "blender/addons"))
import imrsv_lcd_export as A  # noqa: E402

# APPEND the Copper material from the generated library (mimics Asset-Browser assign).
before = set(bpy.data.materials.keys())
with bpy.data.libraries.load(LIB, link=False) as (src, dst):
    assert MID in src.materials, "library %s missing material %r" % (LIB, MID)
    dst.materials = [MID]
mat = bpy.data.materials.get(MID)
assert mat is not None, "append failed"
print("APPENDED %r from library; imrsv_matter_identity=%r use_nodes=%s"
      % (mat.name, mat.get("imrsv_matter_identity"), mat.use_nodes))


def make_quad(name, mat, uvs):
    me = bpy.data.meshes.new(name + "_mesh")
    me.from_pydata([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], [], [(0, 1, 2, 3)])
    me.update()
    uvl = me.uv_layers.new(name="UVMap")
    for i, co in enumerate(uvs):
        uvl.data[i].uv = co
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    bpy.context.collection.objects.link(ob)
    return ob


# TWO meshes sharing the ONE appended library datablock -> §2 splits to per-mesh instances.
a = make_quad("Copper_Top", mat, [(0, 0), (1, 0), (1, 1), (0, 1)])
b = make_quad("Copper_Leg", mat, [(0, 0), (3, 0), (3, 3), (0, 3)])
for o in bpy.context.scene.objects:
    o.select_set(False)
a.select_set(True)
b.select_set(True)
bpy.context.view_layer.objects.active = a

ok, msg = A.export_lcd_usd(out)
print("export_lcd_usd ok=%s msg=%r out=%r" % (ok, msg, out))
print("SLICE_EXPORT_OK" if ok else "SLICE_EXPORT_FAIL")
