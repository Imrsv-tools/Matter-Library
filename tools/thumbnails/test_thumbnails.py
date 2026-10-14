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

print(f"\n{'PASS' if not fails else 'FAIL'}: {len(fails)} failed")
raise SystemExit(1 if fails else 0)
