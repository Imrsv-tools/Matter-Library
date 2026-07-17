"""Phase 60sq1 E10 §15d regression — §2 split survives the File-browser selection collapse.

WHAT THIS PROVES (faithful, two-way): the export emits one USD material-instance prim PER MESH
(rule 6 / §2 split) as long as the export is handed the Creator's REAL selection — and it collapses
to ONE shared prim when handed the degraded selection the File-browser execute context produces.
The fix (E10) captures the selection in the export operator's `invoke()` (viewport context, before
File > Export opens the dialog) and threads it into `export_lcd_usd`, so the split, the v1 validate,
and `wm.usd_export` all agree on the real selection.

WHY the E9 version was a FALSE-GREEN: it faked only `context.selected_objects` via `temp_override`,
so the old view-layer read (`o.select_get()`) still returned 2 and the test passed with the bug
loaded. This version instead exercises the ACTUAL fix path — the explicit object list threaded into
`export_lcd_usd` — and reproduces the exact observed failure (1 shared prim) when the degraded
selection is used, so green here means the thread-through works.

RESIDUAL GAP (covered by the ⚠human gate of record): the real File > Export execute context — where
`context.selected_objects` AND `o.select_get()` BOTH collapse — cannot be reproduced under
`blender --background` (no file browser). The gate of record for the live bug remains the MANUAL
File > Export re-smoke showing 2 distinct instance prims. This headless test guards the mechanism the
fix relies on; the manual smoke proves it fires in the real dialog context.

Run: blender --background --factory-startup --python <this> -- [out_dir]
Exit 0 = PASS; non-zero = the split mechanism regressed.
"""
import bpy, sys, os
REPO = "/home/peter/Documents/IMRSV_GITrepos/IMRSV_Platform/Matter-Library"
sys.path.insert(0, os.path.join(REPO, "blender/addons"))
import imrsv_lcd_export as A  # noqa: E402

post = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
outdir = post[0] if post else "/tmp"
out_fixed = os.path.join(outdir, "creator_selection_fixed.usda")
out_degraded = os.path.join(outdir, "creator_selection_degraded.usda")

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


def prim_count(path):
    return open(path).read().count('assetInfo = {') if os.path.exists(path) else 0


# 1) What invoke() captures in the intact VIEWPORT context: the full selection.
captured = A._selected_meshes_from_context(bpy.context)

# 2) What the FILE-BROWSER execute context degrades context.selected_objects to (the bug source).
with bpy.context.temp_override(selected_objects=[a]):
    degraded = A._selected_meshes_from_context(bpy.context)

# 3) Threading the captured selection -> §2 split fires -> 2 distinct instance prims (rule 6).
ok_fixed, msg_fixed = A.export_lcd_usd(out_fixed, captured)
prims_fixed = prim_count(out_fixed)

# 4) Threading the degraded selection -> split misses the second mesh -> 1 shared prim (the bug).
ok_bug, msg_bug = A.export_lcd_usd(out_degraded, degraded)
prims_bug = prim_count(out_degraded)

print("REG: invoke() capture (viewport context) saw %d meshes (want 2)" % len(captured))
print("REG: File-browser-degraded selection saw %d meshes (want 1 — the bug source)" % len(degraded))
print("REG: export(captured) ok=%s msg=%r prims=%d (want 2 — §2 split fires)" % (ok_fixed, msg_fixed, prims_fixed))
print("REG: export(degraded) ok=%s msg=%r prims=%d (want 1 — split starved, reproduces E9 §6)" % (ok_bug, msg_bug, prims_bug))
passed = (len(captured) == 2 and len(degraded) == 1
          and ok_fixed and prims_fixed == 2
          and ok_bug and prims_bug == 1)
print("REG: %s" % ("PASS" if passed else "FAIL — the thread-through split mechanism regressed"))
sys.exit(0 if passed else 1)
