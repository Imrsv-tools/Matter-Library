"""Phase 60sq1 E8 correction §5 (re-seq §9 Step 1) — generate the installed Blender Asset-Browser
Matter library (v1: Copper-only).

Runs IN Blender on the scaffold `blender/MatterMaterials.blend` (which carries the frozen v1
Principled-BSDF proxy node-group `MatterLCD_<id>` — E8 §3), and produces an INSTALLED Asset-Browser
library the Creator browses + assigns from:

  * authors the DURABLE canonical-identity carrier `imrsv_matter_identity` (a Blender ID custom
    property = the exact qualified Matter name) on the material — PRESERVED across duplication, read
    authoritatively by the exporter (E8 §1 / CreatorAssetProfile.md rule 5);
  * writes a `blender_assets.cats.txt` whose catalog path is the article's `domain/material_class`
    (Copper -> `engineered/metal`), with a DETERMINISTIC uuid5 catalog id (stable across re-runs);
  * `.asset_mark()`s the material + assigns the catalog + author/description;
  * best-effort Blender-native preview (`asset_generate_preview`) — regenerated with correct color
    in the OCIO-fixed session (E8 §4); a fallback-color preview here is acceptable structure-prep;
  * saves the library `.blend` beside the cats file.

Copper-only for v1; the 11-article generalization (creator_selectable, all cats/previews) is
re-seq §9 Step 4. Identity/catalog come from `library/releases/matterlib-0.1.0.catalog.json` so the
generator generalizes without hardcoding.

Run:
  blender --background <repo>/Matter-Library/blender/MatterMaterials.blend \
          --python tools/generators/gen_asset_library.py -- [OUT_DIR]
Default OUT_DIR = <repo>/Matter-Library/blender/asset_library
"""
import bpy, sys, os, json, uuid

REPO = "/home/peter/Documents/IMRSV_GITrepos/IMRSV_Platform/Matter-Library"
CATALOG = os.path.join(REPO, "library/releases/matterlib-0.1.0.catalog.json")
IDENTITY_PROP = "imrsv_matter_identity"           # matches lcd_usd_edit.IDENTITY_PROP
CATALOG_NS = uuid.uuid5(uuid.NAMESPACE_URL, "imrsv:matterlib:asset-catalog")

# v1 Copper-only: the ONE article this library ships (its qualified Matter identity == the
# scaffold material name / the exporter's assetInfo:identifier).
V1_IDENTITY = "Copper_Verdigris_Aged_Base_s01_v01"

argv = sys.argv
post = argv[argv.index("--") + 1:] if "--" in argv else []
out_dir = post[0] if post else os.path.join(REPO, "blender/asset_library")
os.makedirs(out_dir, exist_ok=True)


def catalog_path_for(identity):
    """The Asset-Browser catalog path for an article = its `domain/material_class` (from the
    release catalog), e.g. Copper -> `engineered/metal`. Falls back to `matter` if not listed."""
    with open(CATALOG) as f:
        cat = json.load(f)
    for m in cat.get("materials", []):
        # catalog id tail is the versioned stem; match on the identity's base (drop the trailing
        # _v01 the .mtlx carries) against the material's payload/id.
        if identity.startswith(m.get("display_name", "\0")) or m.get("id", "").split("/")[-1] in identity:
            return "%s/%s" % (m["domain"], m["material_class"])
    return "matter"


def write_cats(path_map):
    """Write blender_assets.cats.txt (VERSION 1; `<uuid>:<catalog/path>:<simple_name>`) with a
    DETERMINISTIC uuid5 per catalog path so re-runs don't churn the file. Returns {path: uuid}."""
    ids = {}
    lines = ["# Anonymous file for the IMRSV Matter Asset-Browser library.",
             "# Catalog paths mirror each article's domain/material_class.", "", "VERSION 1", ""]
    for cp in sorted(path_map):
        cid = str(uuid.uuid5(CATALOG_NS, cp))
        ids[cp] = cid
        simple = cp.replace("/", "-")
        lines.append("%s:%s:%s" % (cid, cp, simple))
    with open(os.path.join(out_dir, "blender_assets.cats.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    return ids


def main():
    mat = bpy.data.materials.get(V1_IDENTITY)
    assert mat is not None, "scaffold material %r not found" % V1_IDENTITY

    # §1: durable canonical-identity carrier (survives duplication; exporter reads it).
    mat[IDENTITY_PROP] = V1_IDENTITY

    cp = catalog_path_for(V1_IDENTITY)
    cat_ids = write_cats({cp: True})

    # asset-mark + catalog assignment.
    if mat.asset_data is None:
        mat.asset_mark()
    ad = mat.asset_data
    ad.catalog_id = cat_ids[cp]
    ad.author = "IMRSV"
    ad.description = ("Matter material %s (matterlib-0.1.0). Assign to a mesh; export via IMRSV LCD "
                      "USD. Identity travels on imrsv_matter_identity." % V1_IDENTITY)
    try:
        ad.tags.new("matter")
        ad.tags.new(cp.split("/")[-1])
    except Exception:
        pass

    # best-effort Blender-native preview (correct color deferred to the OCIO-fixed session).
    try:
        with bpy.context.temp_override():
            mat.asset_generate_preview()
    except Exception as e:
        print("PREVIEW_SKIPPED: %r" % e)

    lib_blend = os.path.join(out_dir, "MatterLibrary.blend")
    bpy.ops.wm.save_as_mainfile(filepath=lib_blend)
    print("ASSET_LIB_OK identity=%s catalog=%s uuid=%s -> %s"
          % (V1_IDENTITY, cp, cat_ids[cp], lib_blend))


main()
