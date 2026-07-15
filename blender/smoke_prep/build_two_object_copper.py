"""Phase 60 — Lane-3 smoke-input prep (Blender build half).

Builds the 2-datablock same-identity Copper scene the 60.4 live smoke needs, so
that sitting is purely eyes-on and NOT gated on discovering plumbing bugs at the rig:
  * two mesh objects, both bound to the REAL scaffold Copper material identity
    (Obj2 gets a COPY of the datablock -> Blender auto-renames it '...v01.001'),
  * DISTINCT per-object UVs (Obj1 unit square, Obj2 scaled 2x) -> distinct primvars:st,
  * a tint on ONLY Obj2's instance (sparse: Obj1 untouched -> 0 overrides),
  * exported through the imrsv_lcd_export add-on (PRESERVE -> no heavy-texture duplication).

The pxr assertions live in the sibling `assert_two_object_copper.py` (a two-process split
because Fedora's Blender has no `pxr`). Together they de-risk the 8-step 60.4 acceptance
export-side (steps 1-4/6/7) and seed the 60.7 multi-object round-trip fixture.

Run:
  blender --background <repo>/Matter-Library/blender/MatterMaterials.blend \
          --python build_two_object_copper.py -- [<out.usda>]
Defaults <out.usda> to a temp path; writes a `<out>.meta.json` + `<out>.build.log` beside it.
"""
import bpy, sys, os, json, tempfile

argv = sys.argv
out = None
if "--" in argv:
    extra = argv[argv.index("--") + 1:]
    if extra:
        out = extra[0]
if out is None:
    out = os.path.join(tempfile.gettempdir(), "p60_copper_two_object.usda")

LOG = out + ".build.log"
log = []
def w(s): log.append(str(s))

MID = "Copper_Verdigris_Aged_Base_s01_v01"
TINT = (0.2, 0.8, 0.4, 1.0)  # distinct-from-baseline Creator tint on Obj2 only

addons = os.path.join(os.path.dirname(bpy.data.filepath), "addons")
sys.path.insert(0, addons)
import imrsv_lcd_export as A  # noqa: E402

m1 = bpy.data.materials.get(MID)
assert m1 is not None, "scaffold Copper material %r not found in the .blend" % MID
m2 = m1.copy()  # 2nd datablock -> Blender auto-renames '<MID>.001'
w("m1=%r  m2=%r" % (m1.name, m2.name))

def _grp(mat):
    for n in mat.node_tree.nodes:
        if n.bl_idname == "ShaderNodeGroup" and n.node_tree:
            return n
    return None

g2 = _grp(m2)
assert g2 is not None, "no Matter node-group on the copied material"
g2.inputs["base_color_tint"].default_value = TINT  # tint ONLY m2; m1 stays at article baseline
w("tinted m2 base_color_tint -> %r" % (tuple(g2.inputs['base_color_tint'].default_value),))

def make_quad(name, mat, uvs):
    me = bpy.data.meshes.new(name + "_mesh")
    me.from_pydata([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], [], [(0, 1, 2, 3)])
    me.update()
    uvl = me.uv_layers.new(name="UVMap")
    for i, co in enumerate(uvs):      # one quad face -> 4 loops in vertex order
        uvl.data[i].uv = co
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    bpy.context.collection.objects.link(ob)
    return ob

make_quad("Copper_ObjA", m1, [(0, 0), (1, 0), (1, 1), (0, 1)])        # unit square
make_quad("Copper_ObjB", m2, [(0, 0), (2, 0), (2, 2), (0, 2)])        # scaled 2x -> distinct st

tex_basenames = sorted({os.path.basename(img.filepath_raw) for img in bpy.data.images
                        if getattr(img, "filepath_raw", "")})
w("matter_tex_basenames=%r" % tex_basenames)

ok, msg = A.export_lcd_usd(out)
w("export_lcd_usd ok=%s msg=%r out=%r" % (ok, msg, out))
w("EXPORT_OK" if ok else "EXPORT_FAIL")

meta = {"out": out, "m1": m1.name, "m2": m2.name, "tint": list(TINT[:3]),
        "matter_tex_basenames": tex_basenames}
json.dump(meta, open(out + ".meta.json", "w"), indent=2)
open(LOG, "w").write("\n".join(log) + "\n")
print("BUILD DONE ->", out)
