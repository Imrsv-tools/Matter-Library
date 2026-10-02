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

print(f"{'FAIL' if fails else 'PASS'}: {len(fails)} failed")
raise SystemExit(1 if fails else 0)
