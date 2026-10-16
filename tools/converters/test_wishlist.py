#!/usr/bin/env python3
"""Units for wishlist.py (Phase11): the file round-trips, the order, and what a keep writes.

    uv run tools/converters/test_wishlist.py        exit 0 = PASS
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wishlist as W  # noqa: E402

fails = []


def check(cond, what):
    print(("  [PASS] " if cond else "  [FAIL] ") + what)
    if not cond:
        fails.append(what)


rows = [
    W.Row(name="A_Natural_Clean_Base_s01_v01", slot="synthetic/plastic", master="Opaque", lane="L1",
          scale="s01", layers=["Scratches01", None, "Dust01", "Grime01"], note='quote "me": yes'),
    W.Row(name="B_Natural_Clean_Base_s01_v01", proving=2),
    W.Row(name="C_Natural_Clean_Base_s01_v01", proving=1),
    W.Row(name="D_Natural_Clean_Base_s01_v01", state="redo", redo="too shiny"),
    W.Row(name="E_Natural_Clean_Base_s01_v01", state="kept", proving=1),
    W.Row(name="F_Natural_Clean_Base_s01_v01", kind="rejudge"),
]
text = W.dumps(rows)
check(W.loads(text) == rows, "the list round-trips (a null layer, a quoted note)")
check(len([ln for ln in text.splitlines() if ln.startswith("  - {")]) == len(rows), "one line per row")
check([r.name[0] for r in W.next_rows(rows, 9)] == ["D", "C", "B", "A", "F"],
      "next: redo first, then proving batches in order, then list order; kept rows skipped "
      f"(got {[r.name[0] for r in W.next_rows(rows, 9)]})")
for bad in ("state: approved", "kind: other"):
    try:
        W.loads("rows:\n  - {name: X, " + bad + "}\n")
        check(False, f"refuses {bad}")
    except ValueError:
        check(True, f"refuses {bad}")
try:
    W.loads("rows:\n  - {name: X}\n  - {name: X}\n")
    check(False, "refuses a name listed twice")
except ValueError:
    check(True, "refuses a name listed twice")

# keep: the status follows the tools that moved alike (Glossary: Status lifecycle)
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    rec, par = tmp / "recipes", tmp / "parity"
    rec.mkdir()

    def fixture(name, tools, alike, status_line):
        (rec / f"{name}.json").write_text(
            '{\n  "_comment": "x",\n  "name": "%s",\n%s  "path": "a/b/%s.mtlx"\n}\n'
            % (name, status_line, name), encoding="utf-8")
        d = par / name
        d.mkdir(parents=True)
        mv = {t: 5.0 for t in tools}
        if not alike:
            mv[tools[-1]] = 0.1
        (d / "scorecard.json").write_text(json.dumps({"settings": {
            "defaults": {"views": {"wide": {}}},
            "wear_1_at_1": {"views": {"wide": {"moved": mv}, "close": {"moved": mv}}}}}))
        (d / "job.json").write_text(json.dumps({"settings": [{"id": "wear_1_at_1", "label": "wear 1 at 1"}]}))

    def judge(mv, md=True):          # the rig's rule, small: a tool under 0.25 of the most moved
        hi, lo = max(mv.values()), min(mv.values())
        return ("moved alike", True) if lo >= 0.25 * hi else ("ONE-SIDED", False)

    fixture("Three_A_B_C_s01_v01", ["storm", "blender", "unreal"], True, '  "status": "draft",\n')
    fixture("Two_A_B_C_s01_v01", ["storm", "blender"], True, "")
    fixture("Off_A_B_C_s01_v01", ["storm", "blender", "unreal"], False, "")
    ks = [W.Row(name=n) for n in ("Three_A_B_C_s01_v01", "Two_A_B_C_s01_v01", "Off_A_B_C_s01_v01")]
    got = {r.name: W.keep(ks, r.name, rec, par, judge) for r in ks}
    st = {n: json.loads((rec / f"{n}.json").read_text())["status"] for n in got}
    check(st["Three_A_B_C_s01_v01"] == "approved", f"all three tools alike -> approved (got {st['Three_A_B_C_s01_v01']})")
    check(st["Two_A_B_C_s01_v01"] == "candidate", f"Storm and Blender only -> candidate (got {st['Two_A_B_C_s01_v01']})")
    check(st["Off_A_B_C_s01_v01"] == "candidate", f"kept over a ONE-SIDED row -> candidate (got {st['Off_A_B_C_s01_v01']})")
    check(all(r.state == "kept" for r in ks), "the rows read kept")
    t = (rec / "Two_A_B_C_s01_v01.json").read_text()
    check(t.index('"name"') < t.index('"status"') < t.index('"path"'), "a missing status goes after the name line")

# brief: what a row starts from (token budget, 2026-10-16)
check(W.material_words("CarraraMarble_Honed_Clean_Base_s1_v01") == ["Carrara", "Marble"],
      "the Material token splits into its words")
with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)
    rec, mat, sh = tmp / "recipes", tmp / "materials", tmp / "shared"
    for d in (rec, mat / "natural" / "stone", sh / "overlays", sh / "masks"):
        d.mkdir(parents=True)
    (sh / "overlays" / "Dust01_overlay_s001.png").write_bytes(b"")
    (sh / "masks" / "Crevice01_s01.png").write_bytes(b"")

    def recipe(name, **kw):
        d = {"name": name, "master": "Opaque", "domain": "natural", "class": "stone"} | kw
        (rec / f"{name}.json").write_text(json.dumps(d), encoding="utf-8")

    recipe("Far_A_Clean_Base_s01_v01", domain="engineered", **{"class": "metal"}, status="approved")
    recipe("Near_A_Clean_Base_s1_v01", status="draft")
    recipe("Kept_A_Clean_Base_s1_v01", status="candidate")
    recipe("Other_A_Clean_Base_s1_v01", master="Subsurface", status="approved")
    recipe("Skin_A_Clean_Base_s1_v01", status="approved", group="character")
    recipe("Basalt_Natural_Clean_Base_s1_v01")
    (mat / "natural" / "stone" / "Basalt_Natural_Clean_Base_s1_v01.mtlx").write_text("")
    row = W.Row(name="Basalt_Natural_Clean_Base_s1_v01", slot="natural/stone", master="Opaque", lane="L3",
                layers=["Scratches01", "Dust01", None, "Crevice01"], state="redo", redo="too dark")
    got = W.layer_files(row.layers, sh)
    check(got == {"Scratches01": None, "Dust01": "overlays/Dust01_overlay_s001.png", "Crevice01": "masks/Crevice01_s01.png"},
          f"layers: found by name, a missing one is None, a null slot skipped (got {got})")
    near = W.nearest_recipe(row, rec)
    check(near is not None and near.stem == "Kept_A_Clean_Base_s1_v01",
          "nearest: same master and slot, kept over draft; never itself, another master or a Character "
          f"(got {near and near.stem})")
    lines = W.brief(row, rec, mat, sh, pb=False)
    text = "\n".join(lines)
    check("Basalt_Natural_Clean_Base_s1_v01.json" in text and "natural/stone/Basalt_Natural_Clean_Base_s1_v01.mtlx" in text,
          "brief: says what is on disk for the stem")
    check("Scratches01 MISSING" in text, "brief: names a layer not made yet")
    check(lines[-1] == "REDO     too dark", "brief: a redo row ends with the maintainer's note")
    check(not any(ln.startswith("pb") for ln in lines), "brief --no-pb: no network line")
    check(any(ln == "nearest  recipes/Kept_A_Clean_Base_s1_v01.json" for ln in lines), "brief: names the nearest recipe")
    check(any(ln.startswith("job      redo:") for ln in lines), "job: a redo on its tag follows the note")
    check(any(ln.startswith("gate     FAIL") for ln in lines), "gate: an incomplete recipe fails, with its errors")
    check("scale    s1 = 1 m" in lines, f"scale: the tag's length (got {[ln for ln in lines if ln.startswith('scale')]})")

    recipe("Basalt_Flamed_Clean_Base_s1_v01", scale_tag="s1", meters_per_tile=0.4)
    off = W.Row(name="Basalt_Flamed_Clean_Base_s1_v01", scale="s01", state="redo", redo="too small")
    lines = W.brief(off, rec, mat, sh, pb=False)
    check(any(ln.startswith("job      scale repair") for ln in lines), "job: a redo whose recipe is off its tag is a scale repair")
    check(any("the row says s01" in ln and "recipe 0.4 m: OFF its tag" in ln for ln in lines),
          "scale: the row's tag disagreeing with the name, and an off-tag recipe, are named")
    check(any(ln.startswith("same     Basalt_Natural_Clean_Base_s1_v01 ") for ln in lines),
          "same: the other articles of the Material token, never the row itself")
    check(W.job(W.Row(name="X", kind="rejudge"), None).startswith("review only"), "job: a queued rejudge is review only")
    check(W.job(W.Row(name="X"), None) == "new build", "job: a queued build with no recipe is a new build")
    check(W.job(W.Row(name="X", state="kept"), None) == "nothing: the row is kept", "job: a finished row needs nothing")

# rules: read from the validators and the schema, so it cannot drift from what the gate accepts
got = "\n".join(W.rules())
check("natural: mineral, soil, stone, wood" in got and "s01 = 10 cm" in got and "overlay cap  3" in got,
      "rules: the taxonomy, the scale tags and the cap come from the gate's own tables")

print(f"{'FAIL' if fails else 'PASS'}: {len(fails)} failed")
raise SystemExit(1 if fails else 0)
