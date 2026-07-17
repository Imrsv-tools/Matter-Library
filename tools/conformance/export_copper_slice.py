"""Phase 60sq1 Step 1 — the Creator producer conformance harness (Blender half).

Drives the REAL `imrsv_lcd_export` add-on (not a hand-authored fixture) end-to-end on a
2-mesh, same-identity Copper scene and writes the lightweight Open Matter Creator asset. The
`.usda` is then asserted against the Creator Asset Profile by the pxr half (`assert_profile.py`)
+ usdchecker/usdcat in `check_exporter.sh` — proving the SHIPPING exporter, through its new
selected-only / geometry+bindings-only output boundary, produces a conforming asset.

Modes (E8 corrections §1/§2 — `--mode` after `--`):
  * distinct (default): two meshes bound to SEPARATE datablocks of the ONE Copper identity, a
    Creator tint on ONLY the 2nd (sparse: 1st emits 0 LCD overrides) — the different-settings
    Creator path.
  * shared: two meshes bound to ONE shared datablock (identical settings) — the exporter must
    split it into a SEPARATE USD material-instance prim per mesh (§2). check_exporter.sh's
    binding-uniqueness assertion is the proof; RED without split_shared_materials.
  * renamed: the scaffold datablock is RENAMED away from its Matter identity but carries the
    durable `imrsv_matter_identity` custom property — the exporter must author identity from the
    property, NOT the display name (§1). Proves the property rides through the REAL Blender export.

All modes: DISTINCT per-mesh UV fits (1x and 3x) -> distinct primvars:st; the durable identity
property is stamped so §1's carrier is exercised end-to-end through the real export.

Run:
  blender --background <repo>/Matter-Library/blender/MatterMaterials.blend \
          --python tools/conformance/export_copper_slice.py -- <out.usda> [--mode MODE]
"""
import bpy, sys, os

argv = sys.argv
post = argv[argv.index("--") + 1:] if "--" in argv else []
out = post[0] if post else "/tmp/creator_copper_slice.usda"
mode = "distinct"
if "--mode" in post:
    mode = post[post.index("--mode") + 1]

addons = os.path.join(os.path.dirname(bpy.data.filepath), "addons")
sys.path.insert(0, addons)
import imrsv_lcd_export as A  # noqa: E402
from imrsv_lcd_export.lcd_usd_edit import IDENTITY_PROP  # noqa: E402

MID = "Copper_Verdigris_Aged_Base_s01_v01"
TINT = (0.2, 0.8, 0.4, 1.0)  # distinct-from-baseline Creator tint on instance B only

m1 = bpy.data.materials.get(MID)
assert m1 is not None, "scaffold Copper material %r not found in the .blend" % MID
# §1: the durable canonical-identity carrier the Asset-Browser generator authors (here stamped
# on the scaffold so the property path is exercised through the real Blender export).
m1[IDENTITY_PROP] = MID


def _grp(mat):
    for n in mat.node_tree.nodes:
        if n.bl_idname == "ShaderNodeGroup" and n.node_tree:
            return n
    return None


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


if mode == "shared":
    # §2: both meshes bind the SAME datablock -> the exporter splits per-mesh.
    mat_a = mat_b = m1
elif mode == "renamed":
    # §1: rename the datablock away from its identity; the property must win.
    m1.name = "MyRenamedCopper"
    mat_a = mat_b = m1
else:  # distinct
    m2 = m1.copy()  # 2nd datablock -> Blender auto-renames '<MID>.001' (property inherited)
    _grp(m2).inputs["base_color_tint"].default_value = TINT  # tint ONLY m2; m1 at baseline
    mat_a, mat_b = m1, m2

a = make_quad("Copper_Top", mat_a, [(0, 0), (1, 0), (1, 1), (0, 1)])   # UV fit A: 1x
b = make_quad("Copper_Leg", mat_b, [(0, 0), (3, 0), (3, 3), (0, 3)])   # UV fit B: 3x tiling

# selected-only export -> select exactly the two prop meshes
for o in bpy.context.scene.objects:
    o.select_set(False)
a.select_set(True)
b.select_set(True)
bpy.context.view_layer.objects.active = a

ok, msg = A.export_lcd_usd(out)
print("export_lcd_usd mode=%s ok=%s msg=%r out=%r" % (mode, ok, msg, out))
print("SLICE_EXPORT_OK" if ok else "SLICE_EXPORT_FAIL")
