"""Phase 60sq1 Step 1 — the Creator producer conformance harness (Blender half).

Drives the REAL `imrsv_lcd_export` add-on (not a hand-authored fixture) end-to-end on a
2-mesh, same-identity Copper scene and writes the lightweight Open Matter Creator asset. The
`.usda` is then asserted against the Creator Asset Profile by the pxr half (`assert_profile.py`)
+ usdchecker/usdcat in `check_exporter.sh` — proving the SHIPPING exporter, through its new
selected-only / geometry+bindings-only output boundary, produces a conforming asset.

Scene (mirrors the pinned golden's two-instance shape):
  * two mesh objects bound to SEPARATE datablocks of the ONE scaffold Copper identity
    (Blender auto-renames the copy `..._v01.001` -> the producer's `_001` normalization
    collapses both to the same `assetInfo:identifier`),
  * DISTINCT per-mesh UV fits (1x and 3x) -> distinct primvars:st,
  * a Creator tint on ONLY the 2nd instance (sparse: the 1st emits 0 LCD overrides),
  * exported selected-only through `export_lcd_usd` (validates the v1 contract, strips the
    preview network, authors the bare @Name.mtlx@ refs + identity + release stamp).

Run:
  blender --background <repo>/Matter-Library/blender/MatterMaterials.blend \
          --python tools/conformance/export_copper_slice.py -- <out.usda>
"""
import bpy, sys, os

argv = sys.argv
out = argv[argv.index("--") + 1] if "--" in argv else "/tmp/creator_copper_slice.usda"

addons = os.path.join(os.path.dirname(bpy.data.filepath), "addons")
sys.path.insert(0, addons)
import imrsv_lcd_export as A  # noqa: E402

MID = "Copper_Verdigris_Aged_Base_s01_v01"
TINT = (0.2, 0.8, 0.4, 1.0)  # distinct-from-baseline Creator tint on instance B only

m1 = bpy.data.materials.get(MID)
assert m1 is not None, "scaffold Copper material %r not found in the .blend" % MID
m2 = m1.copy()  # 2nd datablock -> Blender auto-renames '<MID>.001'


def _grp(mat):
    for n in mat.node_tree.nodes:
        if n.bl_idname == "ShaderNodeGroup" and n.node_tree:
            return n
    return None


_grp(m2).inputs["base_color_tint"].default_value = TINT  # tint ONLY m2; m1 at article baseline


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


a = make_quad("Copper_Top", m1, [(0, 0), (1, 0), (1, 1), (0, 1)])   # UV fit A: 1x
b = make_quad("Copper_Leg", m2, [(0, 0), (3, 0), (3, 3), (0, 3)])   # UV fit B: 3x tiling

# selected-only export -> select exactly the two prop meshes
for o in bpy.context.scene.objects:
    o.select_set(False)
a.select_set(True)
b.select_set(True)
bpy.context.view_layer.objects.active = a

ok, msg = A.export_lcd_usd(out)
print("export_lcd_usd ok=%s msg=%r out=%r" % (ok, msg, out))
print("SLICE_EXPORT_OK" if ok else "SLICE_EXPORT_FAIL")
