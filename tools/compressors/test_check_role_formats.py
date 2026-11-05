#!/usr/bin/env python3
"""Units for check_role_formats.py: each picture an article binds to a compressed role's node is compressed to the
format the consumers' role table names for that node.

    uv run tools/compressors/test_check_role_formats.py        exit 0 = PASS

Runs on a made-up role table and library in a temp folder, so no consumer checkout is needed.
"""
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import check_role_formats as C  # noqa: E402

fails = []


def check(cond, what):
    print(("  [PASS] " if cond else "  [FAIL] ") + what)
    if not cond:
        fails.append(what)


HEADER = """
inline constexpr CompressedRoleInfo kCompressedRoles[] = {
    {         CompressedRole::Diffuse,        "base_color_tex", CompressedFormat::BC7,  true},
    {        CompressedRole::Emissive,                      {}, CompressedFormat::BC7,  true},
    {       CompressedRole::NormalMap,        "normal_map_tex", CompressedFormat::BC5, false},
    {       CompressedRole::CavityMap,        "cavity_map_tex", CompressedFormat::BC4, false},
};
"""

ARTICLE = """<?xml version="1.0"?>
<materialx version="1.39">
  <nodegraph name="NG_Skin">
    <input name="normal_map" type="filename" value="../textures/Skin_normal_sUKN.png" />
    <input name="cavity_map" type="filename" value="../textures/Skin_{cavity_token}_sUKN.png" />
    <input name="makeup_color_map" type="filename" value="" />
    <image name="base_color_tex" type="color3">
      <input name="file" type="filename" value="../textures/Oak_basecolor_s001.png" />
    </image>
    <image name="normal_map_tex" type="vector3">
      <input name="file" type="filename" interfacename="normal_map" />
    </image>
    <image name="cavity_map_tex" type="float">
      <input name="file" type="filename" interfacename="cavity_map" />
    </image>
    <image name="makeup_color_map_tex" type="color4">
      <input name="file" type="filename" interfacename="makeup_color_map" />
    </image>
    <image name="unrelated_tex" type="float">
      <input name="file" type="filename" value="../textures/Grain_normal_s001.png" />
    </image>
  </nodegraph>
</materialx>
"""


def library(root, cavity_token):
    (root / "materials").mkdir(parents=True)
    (root / "materials" / "Skin.mtlx").write_text(ARTICLE.format(cavity_token=cavity_token))
    return root


with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    header = tmp / "IoxMaterialTypes.h"
    header.write_text(HEADER)

    print("the role table is read from the header")
    table = C.read_role_table(header)
    check(table == {"base_color_tex": "BC7", "normal_map_tex": "BC5", "cavity_map_tex": "BC4"}, f"node -> format, {table}")

    print("a library whose pictures agree with the table")
    good = library(tmp / "good", "cavity")
    checked, problems = C.check_library(good, table)
    check(problems == [], f"no problem, got {problems}")
    check(checked == 3, f"three bound pictures checked (an empty one and a node outside the table are not), got {checked}")

    print("a picture compressed to another format than its node's")
    bad = library(tmp / "bad", "basecolor")
    _, problems = C.check_library(bad, table)
    check(len(problems) == 1, f"one problem, got {problems}")
    check(problems and "cavity_map_tex" in problems[0] and "BC7" in problems[0] and "BC4" in problems[0],
          f"it names the node and both formats: {problems}")

    print("a picture the compressor cannot classify")
    odd = library(tmp / "odd", "pores")
    _, problems = C.check_library(odd, table)
    check(len(problems) == 1 and "cannot classify" in problems[0], f"said, got {problems}")

    print("the command")
    check(C.main(["--header", str(header), "--library", str(good)]) == 0, "agreeing library exits 0")
    check(C.main(["--header", str(header), "--library", str(bad)]) == 1, "drifting library exits 1")
    check(C.main(["--header", str(tmp / "absent.h"), "--library", str(good)]) == 0, "no header: skipped, exits 0")
    reshaped = tmp / "Reshaped.h"
    reshaped.write_text("inline constexpr CompressedRoleInfo kCompressedRoles[] = {\n    {Diffuse, base_color_tex},\n};\n")
    check(C.main(["--header", str(reshaped), "--library", str(good)]) == 1, "a header whose rows cannot be read exits 1")

print(f"\n{'PASS' if not fails else 'FAIL'}: {len(fails)} failure(s)")
sys.exit(1 if fails else 0)
