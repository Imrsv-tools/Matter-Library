"""Phase 60sq1 E9 §15d regression — the export must read the view-layer SELECT FLAGS, not
`bpy.context.selected_objects`, so §2's per-mesh split fires even in the File-browser execute
context (where `context.selected_objects` returns only the active object).

Reproduces the §6-slice bug headlessly: build 2 meshes sharing ONE datablock, select both, then
call `export_lcd_usd` under a `temp_override(selected_objects=[active])` that simulates the
File-browser context. The fixed exporter emits 2 material-instance prims (rule 6); the buggy one
emitted 1 shared prim. Run: blender --background --factory-startup --python <this> -- [out.usda]

Exit 0 = PASS (2 distinct instance prims); non-zero = the bug (1 shared prim) or an error.
"""
import bpy, sys, os
REPO = "/home/peter/Documents/IMRSV_GITrepos/IMRSV_Platform/Matter-Library"
sys.path.insert(0, os.path.join(REPO, "blender/addons"))
import imrsv_lcd_export as A  # noqa: E402

post = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
out = post[0] if post else "/tmp/creator_selection_regression.usda"

sc = bpy.context.scene
for o in list(bpy.data.objects):
    bpy.data.objects.remove(o, do_unlink=True)
mat = bpy.data.materials.new("Copper_Verdigris_Aged_Base_s01_v01")
mat["imrsv_matter_identity"] = "Copper_Verdigris_Aged_Base_s01_v01"


def quad(name):
    me = bpy.data.meshes.new(name + "_m")
    me.from_pydata([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], [], [(0, 1, 2, 3)])
    me.update(); me.uv_layers.new(name="UVMap")
    ob = bpy.data.objects.new(name, me); ob.data.materials.append(mat)
    sc.collection.objects.link(ob); return ob


a, b = quad("Cube"), quad("Cone")   # both bound to the ONE shared datablock (drag-assign)
a.select_set(True); b.select_set(True)
bpy.context.view_layer.objects.active = a

# Simulate the File-browser execute context: context.selected_objects sees ONLY the active object.
with bpy.context.temp_override(selected_objects=[a]):
    seen = len(A._selected_mesh_objects())
    ok, msg = A.export_lcd_usd(out)

prims = open(out).read().count('assetInfo = {') if os.path.exists(out) else 0
print("REG: _selected_mesh_objects under file-browser override saw %d meshes (want 2)" % seen)
print("REG: export ok=%s msg=%r material-instance prims=%d (want 2 — rule 6)" % (ok, msg, prims))
passed = (seen == 2 and ok and prims == 2)
print("REG: %s" % ("PASS" if passed else "FAIL — the §2 split did not fire in the file-browser context"))
sys.exit(0 if passed else 1)
