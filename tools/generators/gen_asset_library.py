"""Phase 60sq1 Step 4 (re-seq §9) — generate the installed Blender Asset-Browser Matter library
for ALL Creator-selectable articles in the working tree, each tagged with its status (since
Phase07 7.2, 2026-09-27; it read `matterlib-0.1.0`'s 11 until then).

Since Phase05 step 5.5 (2026-09-27) each article is built on the FAITHFUL Blender masters
(`blender/masters/load_article.py`: the article's `.mtlx` in, a `MatterLCD_<id>` group on
`ML_<Master>` out), the ones the parity rig measures against USDLiveView's renderer. Until then
it was `matter_proxy.build_matter_proxy`, a "recognizable, not faithful" look-alike (E11); that
file is kept, retired. For each Creator-selectable catalog article
(honors the durable `creator_selectable` field, RD-5 — IMRSV_MissingMaterial excluded):

  * builds the proxy material with the durable `imrsv_matter_identity` carrier (survives
    duplication; the exporter reads it — E8 §1 / CreatorAssetProfile.md rule 5);
  * `.asset_mark()`s + assigns the catalog `domain/material_class` (deterministic uuid5 catalog id);
  * best-effort Blender-native preview (correct colour needs the OCIO-fixed session, E9 §4);
  * writes one `blender_assets.cats.txt` covering every article's catalog path;
  * saves the library `.blend`.

Run (no scaffold needed — built from the articles' .mtlx):
  blender --background --factory-startup \
          --python tools/generators/gen_asset_library.py -- [OUT_DIR]
Default OUT_DIR = <repo>/Matter-Library/blender/asset_library
"""
import bpy, sys, os, json, uuid

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # this repo
IDENTITY_PROP = "imrsv_matter_identity"           # matches lcd_usd_edit.IDENTITY_PROP
CATALOG_NS = uuid.uuid5(uuid.NAMESPACE_URL, "imrsv:matterlib:asset-catalog")

sys.path.insert(0, os.path.join(REPO, "blender/masters"))
sys.path.insert(0, os.path.join(REPO, "tools/converters"))
from pathlib import Path  # noqa: E402
import load_article  # noqa: E402
import working_tree  # noqa: E402

STATUS_MEANS = {
    "draft": "not yet checked side by side",
    "candidate": "checked in USDLiveView and Blender; Unreal not yet",
    "approved": "checked in USDLiveView, Blender and Unreal",
    "deprecated": "kept for old scenes; prefer a newer material",
    "retired": "no longer offered",
}

argv = sys.argv
post = argv[argv.index("--") + 1:] if "--" in argv else []
out_dir = post[0] if post else os.path.join(REPO, "blender/asset_library")
os.makedirs(out_dir, exist_ok=True)


def selectable_articles():
    """Every Creator-selectable article in the WORKING TREE (RD-5: creator_selectable), with
    its status (Phase07 7.2). It read `matterlib-0.1.0`'s frozen catalog until then, so a new
    article could never reach Blender; the lead's ruling is to have everything in, marked,
    before the first release ("I would rather have everything in and 'uncalibrated' yet then
    a bunch of magenta", 2026-09-27)."""
    return [{
        "identity": a["identity"],
        "catalog_path": "%s/%s" % (a["domain"], a["material_class"]),
        "mtlx": str(a["mtlx"]),
        "status": a["status"],
    } for a in working_tree.articles() if a["creator_selectable"]]


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
        if not os.path.isfile(a["mtlx"]):
            skipped.append("%s (no .mtlx)" % a["identity"]); continue
        # Phase05 5.5: the faithful Blender master (blender/masters), built from the article's
        # .mtlx, replaces matter_proxy's "recognizable, not faithful" look-alike (lead,
        # 2026-09-26: "the goal indeed is to get things actaully working").
        mat = load_article.build(Path(a["mtlx"]), name=a["identity"])
        notes = None

        mat[IDENTITY_PROP] = a["identity"]          # §1 durable carrier
        if mat.asset_data is None:
            mat.asset_mark()
        ad = mat.asset_data
        ad.catalog_id = cat_ids[a["catalog_path"]]
        ad.author = "IMRSV"
        ad.description = ("Matter material %s (%s: %s). Assign to a mesh; export via IMRSV LCD "
                          "USD. Identity travels on imrsv_matter_identity."
                          % (a["identity"], a["status"], STATUS_MEANS[a["status"]]))
        try:
            ad.tags.new("matter")
            ad.tags.new(a["catalog_path"].split("/")[-1])
            ad.tags.new(a["status"])
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
