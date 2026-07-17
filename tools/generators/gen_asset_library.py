"""Phase 60sq1 Step 4 (re-seq §9) — generate the installed Blender Asset-Browser Matter library
for ALL Creator-selectable articles (11 for matterlib-0.1.0).

Generalizes the E9 Copper-only generator. Builds each article's proxy from scratch via the ONE
generic recipe->Principled mapper (`matter_proxy.build_matter_proxy`) — canonical recipe +
`.mtlx` in, `MatterLCD_<id>` Principled proxy out (lead directive, E11: recognizable authoring
proxy, not render parity; NO per-article branches). For each Creator-selectable catalog article
(honors the durable `creator_selectable` field, RD-5 — IMRSV_MissingMaterial excluded):

  * builds the proxy material with the durable `imrsv_matter_identity` carrier (survives
    duplication; the exporter reads it — E8 §1 / CreatorAssetProfile.md rule 5);
  * `.asset_mark()`s + assigns the catalog `domain/material_class` (deterministic uuid5 catalog id);
  * best-effort Blender-native preview (correct colour needs the OCIO-fixed session, E9 §4);
  * writes one `blender_assets.cats.txt` covering every article's catalog path;
  * saves the library `.blend`.

Run (no scaffold needed — built from the recipes):
  blender --background --factory-startup \
          --python tools/generators/gen_asset_library.py -- [OUT_DIR]
Default OUT_DIR = <repo>/Matter-Library/blender/asset_library
"""
import bpy, sys, os, json, uuid

REPO = "/home/peter/Documents/IMRSV_GITrepos/IMRSV_Platform/Matter-Library"
CATALOG = os.path.join(REPO, "library/releases/matterlib-0.1.0.catalog.json")
RECIPES = os.path.join(REPO, "tools/converters/recipes")
MTLX_ROOT = os.path.join(REPO, "MatterLibrary")   # payload_path is relative to this in source
IDENTITY_PROP = "imrsv_matter_identity"           # matches lcd_usd_edit.IDENTITY_PROP
CATALOG_NS = uuid.uuid5(uuid.NAMESPACE_URL, "imrsv:matterlib:asset-catalog")

sys.path.insert(0, os.path.join(REPO, "tools/generators"))
import matter_proxy  # noqa: E402

argv = sys.argv
post = argv[argv.index("--") + 1:] if "--" in argv else []
out_dir = post[0] if post else os.path.join(REPO, "blender/asset_library")
os.makedirs(out_dir, exist_ok=True)


def selectable_articles():
    """The Creator-selectable catalog rows (RD-5): creator_selectable == true."""
    with open(CATALOG) as f:
        cat = json.load(f)
    arts = []
    for m in cat.get("materials", []):
        if not m.get("creator_selectable", True):
            continue
        identity = os.path.splitext(os.path.basename(m["payload_path"]))[0]
        arts.append({
            "identity": identity,
            "catalog_path": "%s/%s" % (m["domain"], m["material_class"]),
            "mtlx": os.path.join(MTLX_ROOT, m["payload_path"]),
            "recipe": os.path.join(RECIPES, identity + ".json"),
        })
    return arts


def write_cats(paths):
    """Write blender_assets.cats.txt (VERSION 1) with a DETERMINISTIC uuid5 per catalog path.
    Returns {path: uuid}."""
    ids = {}
    lines = ["# Anonymous file for the IMRSV Matter Asset-Browser library.",
             "# Catalog paths mirror each article's domain/material_class.", "", "VERSION 1", ""]
    for cp in sorted(set(paths)):
        cid = str(uuid.uuid5(CATALOG_NS, cp))
        ids[cp] = cid
        lines.append("%s:%s:%s" % (cid, cp, cp.replace("/", "-")))
    with open(os.path.join(out_dir, "blender_assets.cats.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    return ids


def main():
    arts = selectable_articles()
    cat_ids = write_cats([a["catalog_path"] for a in arts])

    ok, skipped = 0, []
    for a in arts:
        if not os.path.isfile(a["recipe"]):
            skipped.append("%s (no recipe)" % a["identity"]); continue
        with open(a["recipe"]) as f:
            recipe = json.load(f)
        mat, notes = matter_proxy.build_matter_proxy(a["identity"], recipe, a["mtlx"])

        mat[IDENTITY_PROP] = a["identity"]          # §1 durable carrier
        if mat.asset_data is None:
            mat.asset_mark()
        ad = mat.asset_data
        ad.catalog_id = cat_ids[a["catalog_path"]]
        ad.author = "IMRSV"
        ad.description = ("Matter material %s (matterlib-0.1.0). Assign to a mesh; export via IMRSV "
                          "LCD USD. Identity travels on imrsv_matter_identity." % a["identity"])
        try:
            ad.tags.new("matter")
            ad.tags.new(a["catalog_path"].split("/")[-1])
        except Exception:
            pass
        try:
            with bpy.context.temp_override():
                mat.asset_generate_preview()
        except Exception as e:
            print("PREVIEW_SKIPPED %s: %r" % (a["identity"], e))
        ok += 1
        print("ARTICLE_OK %s catalog=%s%s"
              % (a["identity"], a["catalog_path"], (" notes=%r" % notes) if notes else ""))

    lib_blend = os.path.join(out_dir, "MatterLibrary.blend")
    bpy.ops.wm.save_as_mainfile(filepath=lib_blend)
    print("ASSET_LIB_OK articles=%d skipped=%r -> %s" % (ok, skipped, lib_blend))


main()
