#!/usr/bin/env python3
"""The wish list: every material the library wants, and where each one stands (Phase11).

    uv run tools/converters/wishlist.py next [N]           the next N rows to work (redo first, then proving order)
    uv run tools/converters/wishlist.py show <name>
    uv run tools/converters/wishlist.py mark <name> <state> [--why TEXT] [--batch ID] [--name NEW]
    uv run tools/converters/wishlist.py verdict <name>     the rig's Moved verdict per slider, from its scorecard
    uv run tools/converters/wishlist.py keep <name>        the lead keeps it: row kept, recipe status set (below)
    uv run tools/converters/wishlist.py redo <name> --note TEXT
    uv run tools/converters/wishlist.py counts

The list is ``library/wishlist.yaml``: one line per row, editable by hand (add a line to want a
material). A row is either ``build`` (make the material) or ``rejudge`` (an article already on disk:
rig it and review it, no build). States: ``queued`` · ``built`` (ready for review) · ``stuck`` (with
``why``) · ``kept`` · ``redo`` (with the lead's ``redo`` note; the loop rebuilds it in place).

**The list says ``kept``, never "approved".** ``keep`` sets the article's lifecycle status in its
recipe by the Glossary's definitions (Status lifecycle; Phase11 F-P11-1): ``approved`` when every
slider moved alike in USDLiveView's renderer (Storm), Blender AND Unreal, ``candidate`` when only
Storm and Blender agree. It never touches a release (``promote_release.py`` is the maintainer's).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, fields
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
LIST = REPO / "library" / "wishlist.yaml"
RECIPES = REPO / "tools" / "converters" / "recipes"
PARITY = REPO / "library" / "parity"
STATES = ("queued", "built", "stuck", "kept", "redo")
KINDS = ("build", "rejudge")
TOOLS3 = ("storm", "blender", "unreal")

HEADER = """\
# The wish list (Phase11 Library Coverage): every material the library wants, one line per row.
# Add a line to want a material; the batch (/matter-batch) works the list from the top.
# kind: build (make it) | rejudge (already on disk: rig and review only)
# state: queued | built (ready for review) | stuck (why) | kept | redo (the lead's note)
# proving: the proving batch a row belongs to (Phase11). note: free text, carried to the build.
# Tool: tools/converters/wishlist.py. Statuses on the article are set by its `keep`, never by hand here.
"""


@dataclass
class Row:
    name: str
    slot: str | None = None
    master: str | None = None
    lane: str | None = None
    scale: str | None = None
    layers: list | None = None
    kind: str = "build"
    state: str = "queued"
    proving: int | None = None
    batch: str | None = None
    note: str | None = None
    why: str | None = None
    redo: str | None = None
    extra: dict = field(default_factory=dict)

    def check(self) -> None:
        if self.kind not in KINDS:
            raise ValueError(f"{self.name}: kind {self.kind!r} is not one of {KINDS}")
        if self.state not in STATES:
            raise ValueError(f"{self.name}: state {self.state!r} is not one of {STATES}")


ORDER = [f.name for f in fields(Row) if f.name != "extra"]
_BARE = re.compile(r"^[A-Za-z][A-Za-z0-9_./-]*$")


def _scalar(v) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(_scalar(x) for x in v) + "]"
    s = str(v)
    if _BARE.match(s) and s.lower() not in {"null", "true", "false", "yes", "no", "on", "off", "y", "n"}:
        return s
    return json.dumps(s, ensure_ascii=False)        # a JSON string is a valid YAML double-quoted scalar


def dumps(rows: list[Row]) -> str:
    out = [HEADER, "rows:"]
    for r in rows:
        r.check()
        d = {k: getattr(r, k) for k in ORDER} | r.extra
        parts = [f"{k}: {_scalar(v)}" for k, v in d.items() if v is not None or k == "name"]
        out.append("  - {" + ", ".join(parts) + "}")
    return "\n".join(out) + "\n"


def loads(text: str) -> list[Row]:
    data = yaml.safe_load(text) or {}
    rows, seen = [], set()
    for d in data.get("rows") or []:
        known = {k: d[k] for k in ORDER if k in d}
        r = Row(**known, extra={k: v for k, v in d.items() if k not in ORDER})
        r.check()
        if r.name in seen:
            raise ValueError(f"{r.name}: listed twice")
        seen.add(r.name)
        rows.append(r)
    return rows


def load(path: Path = LIST) -> list[Row]:
    return loads(path.read_text(encoding="utf-8"))


def save(rows: list[Row], path: Path = LIST) -> None:
    text = dumps(rows)
    if loads(text) != rows:                           # round-trip: what we write is what we read
        raise ValueError("the list did not round-trip; not written")
    path.write_text(text, encoding="utf-8")


def find(rows: list[Row], name: str) -> Row:
    for r in rows:
        if r.name == name:
            return r
    raise SystemExit(f"no row {name!r} on the list")


def next_rows(rows: list[Row], n: int) -> list[Row]:
    """Redo rows first, then the proving batches in order, then the rest in list order."""
    work = [r for r in rows if r.state in ("queued", "redo")]
    key = lambda r: (r.state != "redo", r.proving is None, r.proving or 0)  # noqa: E731
    return sorted(work, key=key)[:n]                    # sorted() is stable: list order breaks ties


# --- the rig's verdict (reused: tools/parity/rig.py moved_verdict, Phase06 D9) -------------------

def _rig():
    sys.path.insert(0, str(REPO / "tools" / "parity"))
    import rig  # noqa: E402
    return rig


def verdict(name: str, parity: Path = PARITY, judge=None) -> dict:
    """Per setting and view, the Moved verdict; and whether all three tools moved alike throughout."""
    out = parity / name
    card = json.loads((out / "scorecard.json").read_text(encoding="utf-8"))
    job = json.loads((out / "job.json").read_text(encoding="utf-8"))
    labels = {s["id"]: s["label"] for s in job["settings"]}
    judge = judge or _rig().moved_verdict
    lines, tools, ok = [], set(), True
    for sid, sc in card["settings"].items():
        for view, v in sc.get("views", {}).items():
            mv = v.get("moved")
            if not mv:
                continue
            tools |= set(mv)
            word, passed = judge(mv, md=False)
            ok &= passed
            lines.append({"setting": labels.get(sid, sid), "view": view, "verdict": word,
                          "moved": {t: round(x, 2) for t, x in mv.items()}})
    seams = {n: s.get("seamless", True) for n, s in card.get("checks", {}).get("seams", {}).items()}
    scale = [r.get("ok", True) for r in card.get("checks", {}).get("scale", [])]
    three = set(TOOLS3) <= tools
    return {"rows": lines, "tools": sorted(tools), "all_alike": ok and bool(lines),
            "status": ("approved" if three else "candidate") if ok and lines else None,
            "seams_ok": all(seams.values()), "scale_ok": all(scale)}


_STATUS = re.compile(r'^(\s*)"status": "[a-z]+",\n', re.M)
_NAME = re.compile(r'^(\s*)"name": "[^"]*",\n', re.M)


def set_status(recipe: Path, status: str) -> None:
    """A minimal text edit: replace the recipe's status line, or add one after its name line."""
    text = recipe.read_text(encoding="utf-8")
    if _STATUS.search(text):
        new = _STATUS.sub(lambda m: f'{m[1]}"status": "{status}",\n', text, count=1)
    else:
        m = _NAME.search(text)
        if not m:
            raise SystemExit(f"{recipe}: no name line to put the status after")
        new = text[:m.end()] + f'{m[1]}"status": "{status}",\n' + text[m.end():]
    if json.loads(new).get("status") != status:
        raise SystemExit(f"{recipe}: status edit did not take")
    recipe.write_text(new, encoding="utf-8")


def keep(rows: list[Row], name: str, recipes: Path = RECIPES, parity: Path = PARITY, judge=None) -> str:
    r = find(rows, name)
    v = verdict(name, parity, judge)
    status = v["status"] or "candidate"      # the lead kept it over a disagreement: two-tool word at most
    set_status(recipes / f"{name}.json", status)
    r.state, r.why = "kept", None
    return status


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("next"); p.add_argument("n", nargs="?", type=int, default=5)
    p = sub.add_parser("show"); p.add_argument("name")
    p = sub.add_parser("mark"); p.add_argument("name"); p.add_argument("state", choices=STATES)
    p.add_argument("--why"); p.add_argument("--batch"); p.add_argument("--name", dest="new_name")
    p.add_argument("--lane", choices=("L1", "L2", "L3"), help="the way it was actually made, when it differs")
    p = sub.add_parser("verdict"); p.add_argument("name")
    p = sub.add_parser("keep"); p.add_argument("name")
    p = sub.add_parser("redo"); p.add_argument("name"); p.add_argument("--note", required=True)
    sub.add_parser("counts")
    a = ap.parse_args(argv)

    rows = load()
    if a.cmd == "next":
        for r in next_rows(rows, a.n):
            print(dumps([r]).splitlines()[-1].strip()[2:])
        return 0
    if a.cmd == "show":
        print(dumps([find(rows, a.name)]).splitlines()[-1].strip()[2:])
        return 0
    if a.cmd == "verdict":
        v = verdict(a.name)
        for x in v["rows"]:
            print(f"{x['setting']:<34} {x['view']:<6} {x['verdict']:<22} "
                  + " ".join(f"{t} {m:.2f}" for t, m in sorted(x["moved"].items())))
        ports = {}
        for x in v["rows"]:                       # per slider: did it move anything in any view?
            ports[x["setting"]] = ports.get(x["setting"], False) or x["verdict"] != "no change in any tool"
        silent = sorted(s for s, moved in ports.items() if not moved and not s.endswith(" at 0"))
        print(f"tools: {', '.join(v['tools'])} · all moved alike: {v['all_alike']} · seams ok: "
              f"{v['seams_ok']} · scale ok: {v['scale_ok']} · a keep would set: {v['status'] or 'candidate'}")
        print(f"moved nothing in any tool: {', '.join(silent) if silent else 'none'}")
        if not (v["seams_ok"] and v["scale_ok"]) or silent:
            print("REVIEW: say so on the summary's Verdict line. A seam, a failed ruler or a slider that moves "
                  "nothing does not change the status word (the Glossary's is about the tools agreeing); "
                  "whether to keep over it is the maintainer's call.")
        return 0
    if a.cmd == "counts":
        for k in KINDS:
            got = [r for r in rows if r.kind == k]
            print(f"{k}: {len(got)} — " + ", ".join(f"{s} {sum(r.state == s for r in got)}" for s in STATES))
        return 0
    r = find(rows, a.name)
    if a.cmd == "mark":
        if a.state == "stuck" and not a.why:
            raise SystemExit("a stuck row says why: --why TEXT")
        r.state, r.why = a.state, (a.why if a.state == "stuck" else None)
        if a.batch:
            r.batch = a.batch
        if a.new_name:
            r.name = a.new_name
        if a.lane:
            r.lane = a.lane
    elif a.cmd == "keep":
        print(f"{a.name}: kept, recipe status {keep(rows, a.name)}")
    elif a.cmd == "redo":
        r.state, r.redo = "redo", a.note
    save(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
