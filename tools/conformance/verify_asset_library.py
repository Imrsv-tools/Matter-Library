"""Phase 60sq1 E8 §5 — headless STRUCTURE verifier for the generated Blender Asset-Browser library.

Opens the generated MatterLibrary.blend and asserts the Creator-browsable structure: the Matter
material is asset-marked with a catalog, carries the durable identity carrier, and keeps its
frozen Principled-proxy node-group. Also validates the sibling blender_assets.cats.txt referenced
by the material's catalog_id. Structure only — the browse/assign UX is the §6 human sitting.

Run:
  blender --background <libdir>/MatterLibrary.blend --python verify_asset_library.py
"""
import bpy, os, sys

IDENTITY_PROP = "imrsv_matter_identity"
V1_IDENTITY = "Copper_Verdigris_Aged_Base_s01_v01"
fails = []


def check(ok, label, detail=""):
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", label, ("" if ok else " — %s" % detail)))
    if not ok:
        fails.append(label)


libdir = os.path.dirname(bpy.data.filepath)
cats = os.path.join(libdir, "blender_assets.cats.txt")

mat = bpy.data.materials.get(V1_IDENTITY)
check(mat is not None, "library contains the Copper material %r" % V1_IDENTITY)
if mat is not None:
    check(mat.get(IDENTITY_PROP) == V1_IDENTITY,
          "durable imrsv_matter_identity carrier == identity (§1)", str(mat.get(IDENTITY_PROP)))
    check(mat.asset_data is not None, "material is asset-marked (browsable in the Asset Browser)")
    cid = mat.asset_data.catalog_id if mat.asset_data else ""
    check(bool(cid) and cid != "00000000-0000-0000-0000-000000000000",
          "material has a catalog assigned", cid)
    ng = [n for n in (mat.node_tree.nodes if mat.use_nodes and mat.node_tree else [])
          if n.bl_idname == "ShaderNodeGroup" and n.node_tree
          and n.node_tree.name.startswith("MatterLCD_")]
    check(len(ng) == 1, "the frozen v1 Principled-proxy node-group is present (§3)",
          "found %d" % len(ng))
    # every LCD travel port is a proxy socket (bounded adjustment surface)
    if ng:
        socks = {it.name for it in ng[0].node_tree.interface.items_tree
                 if getattr(it, "in_out", "") == "INPUT"}
        want = {"base_color_tint", "overlay1_density", "overlay2_density", "maskset_blend", "roughness_bias"}
        check(want <= socks, "proxy exposes all 5 LCD travel ports as sockets", str(want - socks))

    # cats file references the material's catalog_id
    check(os.path.isfile(cats), "blender_assets.cats.txt exists beside the library", cats)
    if os.path.isfile(cats) and mat.asset_data:
        txt = open(cats).read()
        check("VERSION 1" in txt, "cats file has VERSION 1 header")
        check(cid in txt, "the material's catalog_id is defined in the cats file", cid)
        check("engineered/metal" in txt, "Copper catalog path == engineered/metal (domain/class)")

print("  => asset-library structure: %s" % ("CONFORMS" if not fails else "%d VIOLATION(S)" % len(fails)))
sys.exit(1 if fails else 0)
