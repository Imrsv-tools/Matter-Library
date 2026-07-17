"""Phase 60sq1 Step 4 (re-seq §9) — headless STRUCTURE verifier for the generated Blender
Asset-Browser library, ALL Creator-selectable articles (11 for matterlib-0.1.0).

Opens the generated MatterLibrary.blend and asserts, for every creator_selectable catalog
article (RD-5): the proxy material is present + asset-marked with a catalog, carries the durable
identity carrier, and keeps its `MatterLCD_<id>` node-group exposing the article's LCD travel-port
subset (from its recipe) as interface sockets. Also verifies IMRSV_MissingMaterial is ABSENT
(system material, not Creator-selectable) and the sibling blender_assets.cats.txt covers every
catalog path. Structure only — the browse/assign UX + colour are the §6 human sitting.

Run:
  blender --background <libdir>/MatterLibrary.blend --python verify_asset_library.py
"""
import bpy, os, sys, json

REPO = "/home/peter/Documents/IMRSV_GITrepos/IMRSV_Platform/Matter-Library"
CATALOG = os.path.join(REPO, "library/releases/matterlib-0.1.0.catalog.json")
RECIPES = os.path.join(REPO, "tools/converters/recipes")
IDENTITY_PROP = "imrsv_matter_identity"
LCD_TRAVEL_PORTS = {"base_color_tint", "overlay1_density", "overlay2_density",
                    "maskset_blend", "roughness_bias"}
fails = []


def check(ok, label, detail=""):
    print("  [%s] %s%s" % ("PASS" if ok else "FAIL", label, ("" if ok else " — %s" % detail)))
    if not ok:
        fails.append(label)


def load_catalog():
    with open(CATALOG) as f:
        return json.load(f)


def travel_ports_for(identity):
    """The article's LCD travel-port subset, from its recipe's lcd_ports."""
    rp = os.path.join(RECIPES, identity + ".json")
    if not os.path.isfile(rp):
        return set()
    with open(rp) as f:
        return set(json.load(f).get("lcd_ports", [])) & LCD_TRAVEL_PORTS


cat = load_catalog()
selectable = [m for m in cat.get("materials", []) if m.get("creator_selectable", True)]
system = [m for m in cat.get("materials", []) if not m.get("creator_selectable", True)]

libdir = os.path.dirname(bpy.data.filepath)
cats_path = os.path.join(libdir, "blender_assets.cats.txt")
cats_txt = open(cats_path).read() if os.path.isfile(cats_path) else ""
check(bool(cats_txt), "blender_assets.cats.txt exists beside the library", cats_path)
check("VERSION 1" in cats_txt, "cats file has VERSION 1 header")

check(len(selectable) == 11, "catalog has 11 creator-selectable articles", str(len(selectable)))

for m in selectable:
    identity = os.path.splitext(os.path.basename(m["payload_path"]))[0]
    cpath = "%s/%s" % (m["domain"], m["material_class"])
    mat = bpy.data.materials.get(identity)
    if mat is None:
        check(False, "%s: proxy material present" % identity)
        continue
    check(mat.get(IDENTITY_PROP) == identity,
          "%s: durable identity carrier == identity" % identity, str(mat.get(IDENTITY_PROP)))
    check(mat.asset_data is not None, "%s: asset-marked (browsable)" % identity)
    cid = mat.asset_data.catalog_id if mat.asset_data else ""
    check(bool(cid) and cid != "00000000-0000-0000-0000-000000000000",
          "%s: catalog assigned" % identity, cid)
    check(cid in cats_txt, "%s: catalog_id defined in cats file" % identity, cid)
    check(cpath in cats_txt, "%s: catalog path %s in cats file" % (identity, cpath))
    ng = [n for n in (mat.node_tree.nodes if mat.use_nodes and mat.node_tree else [])
          if n.bl_idname == "ShaderNodeGroup" and n.node_tree
          and n.node_tree.name.startswith("MatterLCD_")]
    check(len(ng) == 1, "%s: MatterLCD_ proxy node-group present" % identity, "found %d" % len(ng))
    if ng:
        socks = {it.name for it in ng[0].node_tree.interface.items_tree
                 if getattr(it, "in_out", "") == "INPUT"}
        want = travel_ports_for(identity)
        check(bool(want), "%s: recipe declares LCD travel ports" % identity, str(want))
        check(want <= socks, "%s: proxy exposes the article's LCD travel ports" % identity,
              "missing %s" % (want - socks))

# system material must NOT be browsable
for m in system:
    identity = os.path.splitext(os.path.basename(m["payload_path"]))[0]
    mat = bpy.data.materials.get(identity)
    check(mat is None or mat.asset_data is None,
          "%s: system material NOT asset-marked (RD-5 exclusion)" % identity)

print("  => asset-library structure (%d articles): %s"
      % (len(selectable), "CONFORMS" if not fails else "%d VIOLATION(S)" % len(fails)))
sys.exit(1 if fails else 0)
