#!/usr/bin/env python3
"""Units for the HDRI kind (Phase14 14.1): the HDRI check, the lockfile's `hdris` list and
`default_hdri`, the projector's schema rule (3 only when HDRIs are listed, Q-P14-2) and the
freeze guard. Every red case asserts its REASON, not only that it failed.

    uv run tools/validators/test_hdri.py        exit 0 = PASS
"""
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "converters"))
sys.path.insert(0, str(HERE.parent / "releases"))
import validate_manifest as vm  # noqa: E402
import project_runtime_catalog as prc  # noqa: E402
import freeze_release as fr  # noqa: E402

fails = []


def check(cond, what):
    print(f"  [{'PASS' if cond else 'FAIL'}] {what}")
    if not cond:
        fails.append(what)


def header(width=4096, height=2048, fmt="32-bit_rle_rgbe") -> bytes:
    return f"#?RADIANCE\nFORMAT={fmt}\nEXPOSURE=1.0\n\n-Y {height} +X {width}\n".encode() + b"\x02\x02" * 8


def has(errs, word):
    return any(word in e for e in errs)


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    lib = root / "MatterLibrary"
    hdris = lib / "hdris"
    hdris.mkdir(parents=True)
    good = hdris / "IndustrialSunset02_PureSky_v01.hdr"
    good.write_bytes(header())

    print("== check_hdri ==")
    check(vm.check_hdri(good) == [], "a 4096 x 2048 RGBE file with a conforming name passes")
    small = hdris / "Small_PureSky_v01.hdr"
    small.write_bytes(header(2048, 1024))
    check(has(vm.check_hdri(small), "size 2048 x 1024"), "a 2k file is refused for its size")
    xyze = hdris / "Xyze_PureSky_v01.hdr"
    xyze.write_bytes(header(fmt="32-bit_rle_xyze"))
    check(has(vm.check_hdri(xyze), "FORMAT="), "an XYZE file is refused for its format")
    badname = hdris / "industrial_sunset_02_puresky_4k.hdr"
    badname.write_bytes(header())
    check(has(vm.check_hdri(badname), "is not <Name>_<Variant>_vNN"), "a source's own name is refused")
    pointer = hdris / "Pointer_PureSky_v01.hdr"
    pointer.write_text("version https://git-lfs.github.com/spec/v1\noid sha256:00\nsize 16086915\n")
    check(has(vm.check_hdri(pointer), "not a Radiance"), "an un-fetched LFS pointer is refused, not passed")
    check(vm.hdri_id_version(good) == ("IndustrialSunset02_PureSky", "v01"), "id and version parse from the name")

    print("== lockfile + projection ==")
    (lib / "materials" / "natural" / "stone").mkdir(parents=True)
    (lib / "materials" / "natural" / "stone" / "Granite_Polished_Clean_Base_s1_v01.mtlx").write_text("<materialx/>")
    rel = root / "library" / "releases"
    rel.mkdir(parents=True)
    mats = ("materials:\n  - id: natural/stone/Granite_Polished_Clean_Base_s1\n"
            "    version: v01\n    status: draft\n")
    plain = rel / "matterlib-9.0.0.lock.yaml"
    plain.write_text("release: 9.0.0\n" + mats)
    cat = prc.build_catalog(plain, lib / "materials")
    check(cat["schema_version"] == 2 and "hdris" not in cat and "default_hdri" not in cat,
          "a lockfile without HDRIs projects at schema 2, with no hdris key (Q-P14-2)")

    with_h = rel / "matterlib-9.1.0.lock.yaml"
    with_h.write_text("release: 9.1.0\n" + mats + "hdris:\n  - id: IndustrialSunset02_PureSky\n"
                      "    version: v01\n    status: draft\ndefault_hdri: IndustrialSunset02_PureSky\n")
    cat = prc.build_catalog(with_h, lib / "materials")
    entry = (cat.get("hdris") or [{}])[0]
    check(cat["schema_version"] == 3, "a lockfile with HDRIs projects at schema 3")
    check(entry.get("payload_path") == "hdris/IndustrialSunset02_PureSky_v01.hdr"
          and entry.get("thumbnail_path") == "thumbnails/hdris/IndustrialSunset02_PureSky_v01.jpg"
          and entry.get("creator_selectable") is True and entry.get("display_name") == "IndustrialSunset02_PureSky",
          "the HDRI entry carries its payload, thumbnail, display name and creator_selectable")
    check(cat.get("default_hdri") == "IndustrialSunset02_PureSky", "the catalog names its default HDRI")
    check(not any(k in json.dumps(cat) for k in ("provenance", "license", "evidence")),
          "no provenance reaches the catalog (no_projection_guard's rule)")

    unlisted = rel / "matterlib-9.2.0.lock.yaml"
    unlisted.write_text(with_h.read_text().replace("default_hdri: IndustrialSunset02_PureSky",
                                                   "default_hdri: Nowhere_PureSky"))
    try:
        prc.build_catalog(unlisted, lib / "materials")
        check(False, "a default naming no listed HDRI is refused")
    except ValueError as exc:
        check("default_hdri 'Nowhere_PureSky' names no listed HDRI" in str(exc),
              "a default naming no listed HDRI is refused, for that reason")

    wrong = rel / "matterlib-9.3.0.lock.yaml"
    wrong.write_text(with_h.read_text().replace("IndustrialSunset02_PureSky", "Small_PureSky"))
    try:
        prc.build_catalog(wrong, lib / "materials")
        check(False, "a listed HDRI of the wrong size is refused")
    except ValueError as exc:
        check("size 2048 x 1024" in str(exc), "a listed HDRI of the wrong size is refused, for its size")

    print("== freeze guard ==")
    (rel / "matterlib-9.1.0.catalog.json").write_text(json.dumps(prc.build_catalog(with_h, lib / "materials")))
    try:
        fr._payload_files(root, "9.1.0", None)
        check(False, "freezing a release that lists HDRIs is refused")
    except ValueError as exc:
        check("lists HDRIs" in str(exc), "freezing a release that lists HDRIs is refused, for that reason")

print("RESULT:", "ALL PASS" if not fails else f"{len(fails)} FAIL")
sys.exit(1 if fails else 0)
