#!/usr/bin/env python3
"""Units for the thumbnail tool (Phase17): the record, and what makes a picture stale.

    uv run tools/thumbnails/test_thumbnails.py        exit 0 = PASS
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import showcase as S  # noqa: E402

fails = []


def check(cond, what):
    print(("  [PASS] " if cond else "  [FAIL] ") + what)
    if not cond:
        fails.append(what)


tmp = Path(tempfile.mkdtemp(prefix="matter-thumb-test-"))
try:
    mtlx, tex = tmp / "A_Test_Clean_Base_s01_v01.mtlx", tmp / "a_basecolor.png"
    mtlx.write_text("<materialx/>")
    tex.write_bytes(b"pixels")
    masters = tmp / "masters"
    masters.mkdir()
    (masters / "m.py").write_text("x = 1\n")
    S.MASTERS = masters
    rend = {"blender": "5.2.2 LTS", "engine": "Cycles", "device": "OPTIX"}
    LOOK = {"hdri_strength": 0.22, "key_power": 110.0}

    def want(**over):
        r = S.record(mtlx, [tex], over.pop("renderer", rend), ["card", "close"], "sphere_cube",
                     over.pop("look", LOOK))
        return r | over

    def made(rec):
        """A folder as the tool leaves it: the record and a picture per view."""
        f = tmp / "out"
        shutil.rmtree(f, ignore_errors=True)
        f.mkdir()
        for v in rec["views"]:
            (f / f"{v}.png").write_bytes(b"png")
        (f / "record.json").write_text(json.dumps(rec | {"seconds": {"card": 8.0}}))
        return f

    print("== the record ==")
    r = want()
    check(set(S.INPUTS) <= set(r), "the record holds every input the stale check compares")
    check(r["scene_version"] == S.SCENE_VERSION and r["samples"] == S.SAMPLES and r["size"] == S.SIZE,
          "it carries the scene version, the samples and the size")
    check("seconds" not in S.INPUTS, "the measured time is written, never compared")

    print("== stale ==")
    f = made(r)
    check(S.stale(f, want()) == [], "fresh when nothing changed (seconds differ, and do not count)")
    check(S.stale(tmp / "nowhere", want()) == ["no record"], "stale with no record")
    tex.write_bytes(b"other pixels")
    check(S.stale(f, want()) == ["article_sha256"], "stale when a texture the article names changes")
    tex.write_bytes(b"pixels")
    mtlx.write_text("<materialx>changed</materialx>")
    check(S.stale(f, want()) == ["article_sha256"], "stale when the .mtlx changes")
    mtlx.write_text("<materialx/>")
    (masters / "m.py").write_text("x = 2\n")
    check(S.stale(f, want()) == ["masters_sha256"], "stale when a Blender master changes")
    (masters / "m.py").write_text("x = 1\n")
    check(S.stale(f, want()) == [], "fresh again once both are back")
    check(S.stale(f, want(renderer=rend | {"device": "CPU"})) == ["renderer"], "stale on another device")
    check(S.stale(f, want(renderer=rend | {"blender": "5.3.0"})) == ["renderer"], "stale on another Blender")
    check(S.stale(f, want(scene_version=S.SCENE_VERSION + 1)) == ["scene_version"], "stale at another scene version")
    check(S.stale(f, want(samples=S.SAMPLES * 2)) == ["samples"], "stale at other samples")
    check(S.stale(f, want(look=LOOK | {"key_power": 120.0})) == ["scene_sha256"],
          "stale when a look number is tuned without a version bump")
    (f / "close.png").unlink()
    check(S.stale(f, want()) == ["no close.png"], "stale when a view's picture is missing")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("== the subject an article is pictured on (17.2) ==")
M = S.REPO / "MatterLibrary" / "materials"
for rel, master, want_subject in [
        ("engineered/metal/StainlessSteel_Polished_Clean_Base_s01_v01.mtlx", "Opaque", "sphere_cube"),
        ("natural/stone/Granite_Polished_Clean_Base_s1_v01.mtlx", "Opaque", "sphere_cube"),
        ("natural/stone/Slate_Cleft_Clean_Base_s1_v01.mtlx", "Opaque", "slab"),
        ("engineered/cementitious/Terrazzo_Polished_Clean_Base_s1_v01.mtlx", "Opaque", "slab"),
        ("engineered/cementitious/Concrete_BoardFormed_Clean_Base_s1_v01.mtlx", "Opaque", "wall"),
        ("natural/soil/Loam_Natural_Clean_Base_s1_v01.mtlx", "Opaque", "slab"),
        ("engineered/glass/Glass_Clear_Clean_Base_s01_v01.mtlx", "TranslucentThin", "pane"),
        ("natural/mineral/Diamond_Brilliant_Clean_Base_s01_v01.mtlx", "TranslucentThick", "gem"),
        ("utility/emissive/Neon_Signage_Clean_Base_s01_v01.mtlx", "Emissive", "tube"),
        ("synthetic/textile/Lace_Floral_Clean_Base_s01_v01.mtlx", "Masked", "lace"),
        ("synthetic/textile/Canvas_Natural_Clean_Base_s001_v01.mtlx", "Opaque", "drape"),
        ("utility/virtual/GreyCard_Neutral18_Clean_Base_s01_v01.mtlx", "Opaque", "card"),
        ("environmental/vegetation/OakLeaf_Natural_Clean_Base_s01_v01.mtlx", "Masked", "leaf")]:
    got = S.subject_for(master, M / rel)
    check(got == want_subject, f"{Path(rel).stem.split('_Clean')[0]}: {got}")
try:
    S.subject_for("Subsurface", M / "character/humanoid/Skin_FitzpatrickIII_Clean_Base_s001_v01.mtlx")
    check(False, "a Character article is refused until 17.3 builds its views")
except S.NotYet:
    check(True, "a Character article is refused until 17.3 builds its views")
check(all(set(v) <= set(S.VIEW_ORDER) for v in (s["views"] for s in S.SUBJECTS.values())),
      "every subject's views are named in VIEW_ORDER (the sheet's order)")

print(f"\n{'PASS' if not fails else 'FAIL'}: {len(fails)} failed")
raise SystemExit(1 if fails else 0)
