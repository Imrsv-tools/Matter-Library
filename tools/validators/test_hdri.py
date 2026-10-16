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

# ---------------------------------------------------------------- Phase16 16.2: the stamp
import hdris as H  # noqa: E402
import serve_to_stage as sts  # noqa: E402

print("== the facts (Phase16, RD-P16-2) ==")
record = {
    "status": "candidate",
    "provenance": {"license": "CC0-1.0"},
    "credit": {"source": "Poly Haven", "source_url": "https://polyhaven.com", "asset_id": "x",
               "asset_url": "https://polyhaven.com/a/x", "name": "Ünïcode Sky (Pure Sky)",
               "authors": [{"name": "A Person", "role": "Original"}, {"name": "B", "role": "Sky edits"}],
               "sponsors": [{"id": "1", "name": "S", "url": "https://s.example"}],
               "info": "Edited sky-only version of [Snow Field 2](https://polyhaven.com/a/snow_field_2)."},
    "tagging": {"categories": ["midday"], "attributes": {"weather": "clear"}},
}
row = {"id": "Test_PureSky", "version": "v01", "record": record}
f = H.facts(row)
check(f["contributor"] == "MatterBot" and f["licence"] == "CC0-1.0" and "name" not in f
      and f["credit"]["title"] == "Ünïcode Sky (Pure Sky)",
      "an HDRI's contributor is MatterBot, its licence comes from its record, and the source's title is credit, not a name (RD-LBL-1)")
check(f["credit"]["edited_from_name"] == "Snow Field 2"
      and f["credit"]["edited_from_url"] == "https://polyhaven.com/a/snow_field_2"
      and f["credit"]["edited_from"].startswith("Edited sky-only"),
      "edited_from is published as a name and an address beside the Markdown line (RD-P16-3)")
check("asset_id" not in f["credit"], "the credit keeps the site file's shape (A9): no asset_id")
check(f["group"] == "hdris" and f["when"] == "midday" and f["sky"] == "clear",
      "the facts carry Phase15's group, when and sky")
check(H.facts({**row, "record": {**record, "contributor": "someone"}})["contributor"] == "someone",
      "a record naming its own contributor wins over MatterBot")
check("licence" not in H.facts({**row, "record": {k: v for k, v in record.items() if k != "provenance"}}),
      "a record with no licence publishes none (an absent field means not known yet)")

print("== the stamp (Phase16, RD-P16-12) ==")
with tempfile.TemporaryDirectory() as tmp:
    src, dst = Path(tmp) / "Test_PureSky_v01.hdr", Path(tmp) / "served" / "Test_PureSky_v01.hdr"
    pixels = bytes(range(256)) * 64
    src.write_bytes(header() + pixels)
    before = src.read_bytes()
    H.stamp(src, dst, f)
    want = {**f, "credit": {k: v for k, v in f["credit"].items() if k != "edited_from"}}
    check(H.read_stamp(dst) == want, "a stamped header reads back as the facts")
    check(src.read_bytes() == before, "the source is untouched (the repo keeps its bytes)")
    out = dst.read_bytes()
    check(out.split(b"\n\n", 1)[1] == before.split(b"\n\n", 1)[1],
          "everything after the header is the source's own bytes")
    check(out.startswith(b"#?RADIANCE\nFORMAT=32-bit_rle_rgbe\nEXPOSURE=1.0\nMATTER_ID=Test_PureSky\n"),
          "the source's header lines come first, the MATTER_ lines after them")
    check(out.count(b"MATTER_CREDIT_AUTHOR=") == 2 and b"MATTER_CREDIT_SPONSOR=" in out,
          "a fact with several values repeats its key")
    check(vm.check_hdri(dst) == vm.check_hdri(src),
          "the stamped copy passes the HDRI check exactly as its source does")
    check(not H.stamp_stale(src, dst, f), "a fresh stamp is not stale")
    again = Path(tmp) / "again.hdr"
    H.stamp(dst, again, f)
    check(again.read_bytes() == out, "stamping a stamped file replaces its MATTER_ lines (idempotent)")
    renamed = {**f, "credit": {**f["credit"], "title": "Another Title"}}
    check(H.stamp_stale(src, dst, renamed), "a changed record makes the stamp stale, with no clock")
    try:
        H.stamp(src, dst, {**f, "contributor": "two\nlines"})
        check(False, "a value with a line break is refused")
    except ValueError as exc:
        check("line break" in str(exc), "a value with a line break is refused, for that reason")

print("== the catalog and the header agree, on the tree ==")
entries, _ = sts.working_tree_hdris()
facts = {h["id"]: H.facts(h) for h in H.on_disk()}
agree = [e["id"] for e in entries
         if all(e.get(k) == facts[e["id"]].get(k)
                for k in ("group", "when", "sky", "licence", "contributor", "credit"))]
check(entries and len(agree) == len(entries) == len(facts),
      f"every served HDRI entry carries its facts ({len(agree)} of {len(entries)})")
check(all(e.get("contributor") and e.get("licence") and e.get("credit") for e in entries),
      "every served HDRI entry has a contributor, a licence and a credit")

print("RESULT:", "ALL PASS" if not fails else f"{len(fails)} FAIL")
sys.exit(1 if fails else 0)
