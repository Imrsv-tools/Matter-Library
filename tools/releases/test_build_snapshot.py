#!/usr/bin/env python3
"""Units for build_snapshot.py (Phase13 13.1): the label, the verdict per control, which pictures
are taken, the portable rewrite, and the ranges' coverage.

    uv run tools/releases/test_build_snapshot.py        exit 0 = PASS
"""
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build_snapshot as B  # noqa: E402
from lcd_ports import LCD_PORTS, LCD_RANGES  # noqa: E402  (on sys.path via build_snapshot)
from rig import moved_verdict  # noqa: E402

fails = []


def check(cond, what):
    print(("  [PASS] " if cond else "  [FAIL] ") + what)
    if not cond:
        fails.append(what)


print("== verdict per control ==")
job = {"settings": [{"id": "defaults"},
                    {"id": "roughness_m05", "label": "roughness -0.5", "port": "roughness_bias"},
                    {"id": "roughness_p05", "label": "roughness +0.5", "port": "roughness_bias"},
                    {"id": "tint_blue", "label": "tint blue", "port": "base_color_tint"}]}
card = {"settings": {"defaults": {},
                     "roughness_m05": {"moved": {"storm": 10.0, "blender": 9.5}},
                     "roughness_p05": {"moved": {"storm": 10.0, "blender": 0.5}},   # one-sided
                     "tint_blue": {"moved": {"storm": 8.0, "blender": 8.2, "unreal": 7.9}}}}
v = B.control_verdicts(card, job, moved_verdict)
check(v["roughness_bias"]["verdict"] == "ONE-SIDED", "a control takes its worst row's verdict")
check([r["verdict"] for r in v["roughness_bias"]["rows"]] == ["moved alike", "ONE-SIDED"], "each row keeps its own word")
check(v["base_color_tint"]["verdict"] == "moved alike", "a control that moved alike says so")
check(B.control_verdicts({"settings": {"defaults": {}}}, {"settings": [{"id": "defaults"}]}, moved_verdict) == {},
      "defaults only: no verdict per control (absent, not passed)")
check("uv_scale" not in v, "a control the sweep did not move has no entry")

print("== pictures ==")
with tempfile.TemporaryDirectory() as tmp:
    d = Path(tmp)
    for p in ["storm/defaults.png", "storm/defaults__close.png", "storm/tint_blue.png", "blender/defaults.png",
              "job.json", "blender.log", "unreal/unreal.log", "scenes/x.usda"]:
        (d / p).parent.mkdir(parents=True, exist_ok=True)
        (d / p).write_bytes(b"x")
    got = [(t, v_, s.relative_to(d).as_posix()) for t, v_, s in B.rig_pictures(d)]
    check(got == [("storm", "wide", "storm/defaults.png"), ("storm", "close", "storm/defaults__close.png"),
                  ("blender", "wide", "blender/defaults.png")],
          "only the default pictures of each tool that ran: never a sweep picture, a log, a job or a scene")

print("== portable rewrite ==")
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    (root / "mat").mkdir()
    (root / "tex/a").mkdir(parents=True)
    (root / "tex/b").mkdir(parents=True)
    (root / "tex/a/A_basecolor.png").write_bytes(b"a")
    (root / "tex/a/Same.png").write_bytes(b"1")
    (root / "tex/b/Same.png").write_bytes(b"2")
    text = '<input name="file" type="filename" value="../tex/a/A_basecolor.png" />'
    out, files = B.portable(text, root / "mat")
    check(out == '<input name="file" type="filename" value="textures/A_basecolor.png" />', "a reference becomes textures/<name>")
    check(list(files) == ["A_basecolor.png"], "the texture is packed once")
    clash = ('<input type="filename" value="../tex/a/Same.png" />'
             '<input type="filename" value="../tex/b/Same.png" />')
    try:
        B.portable(clash, root / "mat")
        check(False, "two different textures with one name are refused")
    except SystemExit:
        check(True, "two different textures with one name are refused")

print("== section (Phase15: from the file's group, never the domain) ==")
check(B.section({"group": "matter", "domain": "engineered"}) == "matter", "a Matter article is Matter")
check(B.section({"group": "character", "domain": "biological"}) == "character", "a Character article is Character")
check(B.section({"group": "matter", "domain": "biological"}) == "matter",
      "a generic biological material is Matter: the domain does not decide (RD-DS-1, F-DS-5)")
G = B.G
check(G.hdri_taxonomy({"tagging": {"categories": ["outdoor", "night"], "attributes": {"weather": "clear"}}})
      == {"when": "night", "sky": "clear"}, "an HDRI's when and sky are Poly Haven's own words")
check(G.hdri_taxonomy({"tagging": {"categories": ["outdoor"]}}) == {},
      "an HDRI with no time category or weather leaves both out, never guessed")
check(G.character_errors("character", "humanoid", "skin") == [] and G.character_errors(None, None, None) == [],
      "a declared Character part, and a Matter article with no group, are both right")
check(G.character_errors("character", "humanoid", "elbow") and G.character_errors("matter", "humanoid", None)
      and G.character_errors("hdris", None, None),
      "an unknown part, a Matter article with Character keys, and an HDRI group on a material are refused")
check(G.taxonomy_path({"group": "character", "species": "humanoid", "part": "mouth"}) == ["Character", "Humanoid", "Mouth"]
      and G.taxonomy_path({"group": "matter", "domain": "engineered", "material_class": "metal"})
      == ["Matter", "Engineered", "Metal"], "each group's place to browse, as a person reads it")

print("== groups (RD-P14-4) ==")
check([g["id"] for g in B.GROUPS] == ["matter", "character", "hdris"], "Matter, Character and HDRIs, in browse order")
check({g["id"]: g["shown"] for g in B.GROUPS} == {"matter": "thumbnail", "character": "human", "hdris": "thumbnail"},
      "each group says how it is shown: Matter by its thumbnails (RD-P17-4), Character never on the rig's cubes (RD-P13-2)")
check(B.GROUPS is G.GROUPS, "the site file and the dev catalog read one list (Phase17: the dev install serves thumbnails too)")

print("== thumbnails (Phase17 17.5) ==")
with tempfile.TemporaryDirectory() as t:
    t = Path(t)
    mtlx, tex = t / "A_Test_Clean_Base_s01_v01.mtlx", t / "a.png"
    mtlx.write_text("<materialx/>")
    tex.write_bytes(b"px")
    f = t / "thumbs"
    f.mkdir()
    check(B.thumbnail_pictures(f, mtlx, [tex]) == [], "no record: no thumbnail (left out, never stood in for)")
    rec = {"article_sha256": B.T.article_hash(mtlx, [tex]), "masters_sha256": B.T.masters_hash(),
           "views": ["card", "close"], "renderer": {"blender": "5.2.2 LTS", "engine": "Cycles", "device": "OPTIX"}}
    (f / "record.json").write_text(json.dumps(rec))
    for v in ("card", "close", "dark"):
        (f / f"{v}.png").write_bytes(b"png")
    got = B.thumbnail_pictures(f, mtlx, [tex])
    check([v for v, _, _ in got] == ["card", "close"], "the record's views, and only those (not a stray dark.png)")
    check(B.renderer_label(rec) == "Cycles (Blender 5.2.2 LTS)", "labelled with its renderer")
    tex.write_bytes(b"other")
    try:
        B.thumbnail_pictures(f, mtlx, [tex])
        check(False, "a thumbnail of another version of the article is refused")
    except B.Stale:
        check(True, "a thumbnail of another version of the article is refused")
    tex.write_bytes(b"px")
    (f / "close.png").unlink()
    try:
        B.thumbnail_pictures(f, mtlx, [tex])
        check(False, "a record whose picture is missing is refused")
    except B.Stale:
        check(True, "a record whose picture is missing is refused")
check({(g["list"], g.get("section")) for g in B.GROUPS} ==
      {("materials", "matter"), ("materials", "character"), ("hdris", None)},
      "Matter and Character are sections of materials; HDRIs are a list of their own")
check({g["id"]: g["taxonomy"] for g in B.GROUPS} == {"matter": ["domain", "material_class"],
      "character": ["species", "part"], "hdris": ["when", "sky"]}, "each group names the fields it is browsed by")
rows = next(g for g in B.GROUPS if g["id"] == "character")["rows"]
check([(r["species"], [p["label"] for p in r["parts"]]) for r in rows]
      == [("humanoid", ["Eyes", "Hair", "Skin", "Nails", "Teeth", "Mouth"])],
      "Character's rows, in the lead's order (M11 (1))")

print("== a material's thumbnail in the dev install (Phase17, the platform's A1 - A3) ==")
import material_thumbnails as MT  # noqa: E402
check(MT.first_view(["close", "card"]) == "card" and MT.first_view(["hand", "face"]) == "face"
      and MT.first_view(["dark", "card"]) == "card" and MT.first_view([]) is None,
      "one picture per material: Matter's card, a Character material's first human-context view")
with tempfile.TemporaryDirectory() as t:
    t = Path(t)
    MT.THUMBS = t
    mtlx, tex = t / "A_Test_Clean_Base_s01_v01.mtlx", t / "a.png"
    mtlx.write_text('<materialx><image name="b"><input name="file" type="filename" value="a.png"/></image></materialx>')
    tex.write_bytes(b"px")
    f = t / mtlx.stem
    f.mkdir()
    check(MT.local_source(mtlx.stem, mtlx) is None, "no record: no local picture (the published one is tried)")
    rec = {"article_sha256": MT.T.article_hash(mtlx, [tex.resolve()]), "masters_sha256": MT.T.masters_hash(),
           "views": ["card", "close"]}
    (f / "record.json").write_text(json.dumps(rec))
    (f / "card.png").write_bytes(b"png")
    check(MT.local_source(mtlx.stem, mtlx) == f / "card.png", "a fresh record's first view is the local picture")
    tex.write_bytes(b"changed")
    check(MT.local_source(mtlx.stem, mtlx) is None, "a record of another version of the article is not used")

print("== hdri entry (14.3) ==")
full = {"id": "IndustrialSunset02_PureSky", "version": "v01", "identity": "IndustrialSunset02_PureSky_v01",
        "record": {"status": "candidate", "description": "A calm industrial sunset.",
                   "credit": {"source": "Poly Haven", "asset_url": "https://polyhaven.com/a/x",
                              "name": "Industrial Sunset 02 (Pure Sky)",
                              "authors": [{"name": "A", "role": "Original"}], "sponsors": [],
                              "info": "Edited sky-only version of X."},
                   "tagging": {"tags": ["pure skies"], "categories": ["outdoor"]}}}
e = B.hdri_entry(full, "IndustrialSunset02_PureSky_v01__thumbnail.jpg", "ab" * 32)
check("label" not in e and e["credit"]["title"] == "Industrial Sunset 02 (Pure Sky)",
      "no label (RD-LBL-1): the name is the file name, and Poly Haven's title is the credit's title")
check(e["credit"]["authors"] == [{"name": "A", "role": "Original"}] and e["credit"]["edited_from"].startswith("Edited"),
      "the credit carries the contributors with their roles and what it was edited from")
check("sponsors" not in e["credit"], "an empty sponsor list is left out, not published empty")
check(e["pictures"] == [{"role": "thumbnail", "file": "IndustrialSunset02_PureSky_v01__thumbnail.jpg", "sha256": "ab" * 32}],
      "one thumbnail picture")
check("download" not in e, "no download: thumbnails and credit only (RD-P14-4)")
bare = B.hdri_entry({"id": "Bare_PureSky", "version": "v01", "identity": "Bare_PureSky_v01", "record": {}}, "t.jpg", "0" * 64)
check(bare["status"] == "draft" and "label" not in bare
      and not {"credit", "description", "tagging", "captured"} & set(bare),
      "with no record: status draft, no label, and nothing invented")

print("== Phase16: who gave it, its credit and its description ==")
import re  # noqa: E402
H, working_tree = B.H, B.working_tree
for src, want in [
    ("Free 16K HDRI, unclipped: midday partly cloudy sky.", "Midday partly cloudy sky."),
    ("Free 24K unclipped HDRI showing a low-contrast sunset.", "A low-contrast sunset."),
    ("Unclipped, free 20K HDRI: low-contrast sunrise.", "Low-contrast sunrise."),
    ("Free, unclipped 16K HDRI of a low-contrast industrial sunset: soft glow.", "A low-contrast industrial sunset: soft glow."),
    ("Free 24K HDRI (unclipped): midday pure sky.", "Midday pure sky."),
    ("Free 20K HDRI, unclipped, clear late-afternoon sky.", "Clear late-afternoon sky."),
    ("Free 16K, unclipped - bright morning/afternoon pure sky.", "Bright morning/afternoon pure sky."),
    ("Free 16K unclipped HDRI capturing a bright sunrise.", "A bright sunrise."),
    ("A calm industrial sunset.", "A calm industrial sunset."),
    ("Free and open sky with no resolution named.", "Free and open sky with no resolution named."),
]:
    check(B.description(src) == want, f"description {src[:40]!r} -> {B.description(src)!r}")
real = [B.description(h["record"].get("description", "")) for h in H.on_disk()]
check(len(real) == 59 and not [d for d in real if B.RESOLUTION_CLAIM.match(d) and re.search(r"\d+K", d[:30])],
      "all 59 real descriptions lose their opening resolution claim (RD-P16-4)")
md = {**full, "record": {**full["record"], "provenance": {"license": "CC0-1.0"},
                         "credit": {**full["record"]["credit"],
                                    "info": "Edited sky-only version of [Snow Field](https://polyhaven.com/a/snow_field)."}}}
e2 = B.hdri_entry(md, "t.jpg", "0" * 64)
check(e2["contributor"] == "MatterBot" and e2["licence"] == "CC0-1.0",
      "an HDRI entry says who gave it and its licence (RD-P16-11)")
check(e2["credit"]["edited_from_name"] == "Snow Field" and e2["credit"]["edited_from_url"] == "https://polyhaven.com/a/snow_field"
      and e2["credit"]["edited_from"].startswith("Edited"),
      "edited_from is published as a name and an address, beside the Markdown line (RD-P16-3)")
arts = working_tree.articles()
check(arts and all(a["contributor"] == "MatterBot" and a["licence"] == "CC0-1.0" for a in arts),
      f"every article's file says MatterBot and CC0-1.0 ({len(arts)})")

print("== Phase18: the mesh a fitted article fits, and the kits ==")
with tempfile.TemporaryDirectory() as t:
    f = Path(t) / "A_Teeth_Clean_Base_sUKN_v01.mtlx"
    f.write_text('<materialx><nodedef name="ND_m" node="imrsv_metadata">'
                 '<input name="contributor" type="string" value="AnotherHand" />'
                 '<input name="licence" type="string" value="CC0-1.0" />'
                 '<input name="fits" type="string" value="MakeHuman_Teeth_v01" /></nodedef></materialx>')
    md_ = working_tree.metadata_of(f)
    other = working_tree.declared({"contributor": md_.get("contributor", ""), "licence": md_.get("licence", ""),
                                   "fits": md_.get("fits", ""), "group": "character"})
check(other == {"contributor": "AnotherHand", "licence": "CC0-1.0", "fits": "MakeHuman_Teeth_v01"},
      "any contributor's handle and the mesh it fits reach the entry as the file declares them (not only MatterBot)")
check(working_tree.declared({"contributor": "MatterBot", "licence": "", "fits": ""}) == {"contributor": "MatterBot"},
      "a fact the file does not declare is left out, never published empty (RD-WS-1)")
fitted = {a["identity"]: a["fits"] for a in arts if a["fits"]}
check(fitted == {"Teeth_Natural_Clean_Base_sUKN_v01": "MakeHuman_Teeth_v01",
                 "Eye_Green_Clean_Base_sUKN_v01": "MakeHuman_Eyes_v01"},
      f"the two fitted articles, and only those, declare the mesh they fit ({sorted(fitted)})")
check(set(fitted.values()) <= set(G.PART_MESHES), "every fits names a known part mesh")
e3 = B.derive_entry({"id": "character/humanoid/teeth/Teeth_Natural_Clean_Base_sUKN", "version": "v01",
                     "status": "draft"})
check(e3["scale"] == "sUKN" and e3["display_name"] == "teeth/Teeth_Natural_Clean_Base"
      and e3["payload_path"] == "materials/character/humanoid/teeth/Teeth_Natural_Clean_Base_sUKN_v01.mtlx",
      f"an sUKN article is on the grammar: its scale, its name without the tag, its versioned file ({e3['payload_path']})")
check({a["identity"]: a["display_name"] for a in arts if a["fits"]}
      == {"Teeth_Natural_Clean_Base_sUKN_v01": "Teeth_Natural_Clean_Base", "Eye_Green_Clean_Base_sUKN_v01": "Eye_Green_Clean_Base"},
      "the working tree drops sUKN from the name as it drops sNN")
kits = [B.kit_entry(m, rec_, "0" * 64) for m, rec_ in G.PART_MESHES.items()]
check([k["id"] for k in kits] == ["MakeHuman_Body_v01", "MakeHuman_Eyes_v01", "MakeHuman_Teeth_v01",
                                  "MakeHuman_Tongue_v01"], "four kits, one per part mesh")
check(all(k["file"] == f"kit__{k['id']}.zip" and k["sha256"] == "0" * 64 and k["uv_sha256"] and k["map_size"]
          for k in kits), "each kit names its zip and its zip's sha256, with the layout hash and map size it is checked by")

print("== ranges ==")
check(set(LCD_RANGES) == set(LCD_PORTS), "every Creator port has a range, and no range names a non-port")

print(f"\n{'PASS' if not fails else 'FAIL'}: {len(fails)} failed")
sys.exit(1 if fails else 0)
