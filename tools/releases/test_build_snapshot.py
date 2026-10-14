#!/usr/bin/env python3
"""Units for build_snapshot.py (Phase13 13.1): the label, the verdict per control, which pictures
are taken, the portable rewrite, and the ranges' coverage.

    uv run tools/releases/test_build_snapshot.py        exit 0 = PASS
"""
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


print("== label ==")
for raw, want in [("Copper_Verdigris_Aged_Base", "Copper verdigris aged"),
                  ("Oak_Natural_Clean_Base", "Oak"),
                  ("ABS_Matte_Clean_Base", "ABS matte"),
                  ("Paint_GradeI_Clean_Base", "Paint grade I"),          # a roman numeral keeps its capital
                  ("Paint_GradeIV_Clean_Base", "Paint grade IV"),
                  ("Diagnostic_UVGrid_Clean_Base", "Diagnostic UV grid"),
                  ("Rust_OnSteel_Flaking_Base", "Rust on steel flaking"),
                  ("GreyCard_Neutral18_Clean_Base", "Grey card neutral 18")]:
    check(B.label(raw) == want, f"{raw} -> {B.label(raw)!r} (want {want!r})")

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

print("== section ==")
check(B.section("engineered") == "matter" and B.section("environmental") == "matter", "a Matter domain is Matter")
check(B.section("biological") == "character", "biological is a character material, browsed apart (RD-P13-2)")

print("== groups (RD-P14-4) ==")
check([g["id"] for g in B.GROUPS] == ["matter", "character", "hdris"], "Matter, Character and HDRIs, in browse order")
check({g["id"]: g["shown"] for g in B.GROUPS} == {"matter": "rig", "character": "human", "hdris": "thumbnail"},
      "each group says how it is shown: Character never on the rig's cubes (RD-P13-2)")
check({(g["list"], g.get("section")) for g in B.GROUPS} ==
      {("materials", "matter"), ("materials", "character"), ("hdris", None)},
      "Matter and Character are sections of materials; HDRIs are a list of their own")

print("== hdri entry (14.3) ==")
full = {"id": "IndustrialSunset02_PureSky", "version": "v01", "identity": "IndustrialSunset02_PureSky_v01",
        "record": {"status": "candidate", "description": "A calm industrial sunset.",
                   "credit": {"source": "Poly Haven", "asset_url": "https://polyhaven.com/a/x",
                              "name": "Industrial Sunset 02 (Pure Sky)",
                              "authors": [{"name": "A", "role": "Original"}], "sponsors": [],
                              "info": "Edited sky-only version of X."},
                   "tagging": {"tags": ["pure skies"], "categories": ["outdoor"]}}}
e = B.hdri_entry(full, "IndustrialSunset02_PureSky_v01__thumbnail.webp", "ab" * 32)
check(e["label"] == "Industrial Sunset 02 (Pure Sky)", "the label is Poly Haven's own name")
check(e["credit"]["authors"] == [{"name": "A", "role": "Original"}] and e["credit"]["edited_from"].startswith("Edited"),
      "the credit carries the contributors with their roles and what it was edited from")
check("sponsors" not in e["credit"], "an empty sponsor list is left out, not published empty")
check(e["pictures"] == [{"role": "thumbnail", "file": "IndustrialSunset02_PureSky_v01__thumbnail.webp", "sha256": "ab" * 32}],
      "one thumbnail picture")
check("download" not in e, "no download: thumbnails and credit only (RD-P14-4)")
bare = B.hdri_entry({"id": "Bare_PureSky", "version": "v01", "identity": "Bare_PureSky_v01", "record": {}}, "t.webp", "0" * 64)
check(bare["status"] == "draft" and bare["label"] == "Bare pure sky"
      and not {"credit", "description", "tagging", "captured"} & set(bare),
      "with no record: status draft, a derived label, and nothing invented")

print("== ranges ==")
check(set(LCD_RANGES) == set(LCD_PORTS), "every Creator port has a range, and no range names a non-port")

print(f"\n{'PASS' if not fails else 'FAIL'}: {len(fails)} failed")
sys.exit(1 if fails else 0)
