#!/usr/bin/env python3
"""Two articles side by side: one with a slider set, the other as it is authored.

    uv run tools/parity/pair_sheet.py [--out sheet.png] [--cell 512] <pair> [<pair> ...]

A pair is ``<article>@<setting label>=<article>[@<view>,<view>]``: the first article at one of
its sweep rows (the row's label, or a part of it that names one row), the second at its own
values, in the views named (default: every view both were rendered in). It answers one question
(Phase12 12.5): does an article with a Creator control set stand in for the article that was
authored with that value?

It renders nothing. It reads the pictures ``rig.py`` stored under ``library/parity/<article>/``,
and refuses one that is older than its article (re-run the rig). Per pair, per view, per tool it
lays the set picture beside the authored one, with where they differ and the dE2000 between
them over the subjects; the same numbers are printed and written beside the sheet as
``<sheet>.md``. Both pictures of a row are the SAME tool, so the number is about the two
articles, not about the tools.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "drivers"))
import compare  # noqa: E402
import rig  # noqa: E402

# The difference picture's scale: black under half of it, yellow at it, red at 3x. Two ARTICLES
# differ by far more than two tools drawing one article (the rig's flag, 2), and at that flag
# the whole panel is red and shows nothing (seen on the first sheet, Phase12 12.5).
HEAT_BAR = 6.0
TOOLS = ("storm", "blender", "unreal")
SHORT = {"storm": "Storm", "blender": "Blender", "unreal": "Unreal"}


def parse_pair(text: str) -> tuple[str, str, str, list[str]]:
    left, sep, right = text.partition("=")
    a, at, label = left.partition("@")
    if not (sep and at and a and label and right):
        raise SystemExit(f"not a pair: {text!r} (want <article>@<setting label>=<article>[@views])")
    b, _, views = right.partition("@")
    return a, label, b, [v for v in views.split(",") if v]


def read_job(stem: str) -> dict:
    p = rig.OUT_ROOT / stem / "job.json"
    if not p.is_file():
        raise SystemExit(f"{stem} has no stored rig run ({p}); run rig.py on it first")
    return json.loads(p.read_text(encoding="utf-8"))


def find_setting(job: dict, label: str) -> dict:
    rows = [s for s in job["settings"] if s["label"] == label] or \
           [s for s in job["settings"] if label in s["label"]]
    if len(rows) != 1:
        raise SystemExit(f"{job['article']['name']}: {len(rows)} sweep rows match {label!r} "
                         f"(it has: {[s['label'] for s in job['settings']]}); run rig.py --sweep")
    return rows[0]


def picture(job: dict, tool: str, sid: str, suffix: str) -> Path | None:
    """A stored picture, or None where that tool was not rendered. Refuses a stale one."""
    p = Path(job["out_dir"]) / tool / f"{sid}{suffix}.png"
    if not p.is_file():
        return None
    if p.stat().st_mtime < Path(job["article"]["path"]).stat().st_mtime:
        raise SystemExit(f"{p} is older than its article; re-run rig.py on {job['article']['name']}")
    return p


def said(value) -> str:
    return ", ".join(f"{v:g}" for v in value) if isinstance(value, list) else f"{value:g}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="One article with a slider set, beside another as authored.")
    ap.add_argument("pairs", nargs="+", help="<article>@<setting label>=<article>[@view,view]")
    ap.add_argument("--out", default=str(rig.OUT_ROOT / "_pairs" / "sheet.png"))
    ap.add_argument("--cell", type=int, default=512, help="picture size on the sheet")
    args = ap.parse_args(argv)
    cell, label_w, head_h, line_h, gap = args.cell, 150, 96, 30, 36
    f, fs = rig._font(18), rig._font(15)

    blocks = []                                   # one per pair: (titles, rows)
    for text in args.pairs:
        a, label, b, views = parse_pair(text)
        ja, jb = read_job(a), read_job(b)
        s = find_setting(ja, label)
        views = views or [v for v in ja["views"] if v in jb["views"]]
        rows = []
        for v in views:
            if v not in ja["views"] or v not in jb["views"]:
                raise SystemExit(f"view {v!r} was not rendered for both {a} and {b}")
            sfx = ja["views"][v]["suffix"]
            mask = Path(ja["out_dir"]) / f"mask{sfx}.png"     # one scene, one camera: one mask
            for tool in TOOLS:
                pa, pb = picture(ja, tool, s["id"], sfx), picture(jb, tool, "defaults", sfx)
                sc = heat = None
                if pa and pb:
                    scores, dE = compare.compare(pa, pb, mask)
                    sc = scores
                    heat = compare.heatmap(dE, HEAT_BAR, compare.masks(mask)["subjects"])
                rows.append({"view": v, "tool": tool, "set": pa, "authored": pb, "scores": sc, "heat": heat})
        set_title = f"{a}  ·  SET: " + ", ".join(f"{p} = {said(val)}" for p, val in s["set"].items())
        blocks.append({"a": a, "b": b, "label": s["label"], "set_title": set_title,
                       "authored_title": f"{b}  ·  as authored", "rows": rows})

    W = label_w + 3 * cell
    H = sum(head_h + len(bk["rows"]) * (cell + line_h) + gap for bk in blocks)
    sheet = Image.new("RGB", (W, H), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    lines = ["# One article with a control set, beside the article authored with that value", "",
             "dE2000 between the two pictures of ONE tool, over the subjects (sphere, cube, floor). "
             f"The same scene, camera and light; the tools' own flag for a difference is {rig.BAR:g}."]
    y = 0
    for bk in blocks:
        d.text((10, y + 10), f"{bk['a']} with {bk['label']!r}   beside   {bk['b']}",
               fill=(235, 235, 235), font=f)
        differ = f"Where they differ (black = same, yellow = dE {HEAT_BAR:g}, red = {3 * HEAT_BAR:g} and over)"
        for i, t in enumerate((bk["set_title"], bk["authored_title"], differ)):
            d.text((label_w + i * cell + 10, y + 44), rig._wrap(t, max(20, cell // 9)),
                   fill=(200, 200, 200), font=fs)
        lines += ["", f"## {bk['set_title']} — beside — {bk['authored_title']}", "",
                  "| View | Tool | Mean | p95 | Sphere | Cube | Floor |", "|---|---|---|---|---|---|---|"]
        y += head_h
        for r in bk["rows"]:
            view = rig.VIEW_LABELS.get(r["view"], r["view"])
            d.text((10, y + 10), SHORT[r["tool"]], fill=(235, 235, 235), font=f)
            d.text((10, y + 40), rig._wrap(f"({view})", 16), fill=(150, 150, 150), font=fs)
            for i, key in enumerate(("set", "authored")):
                if r[key]:
                    sheet.paste(Image.open(r[key]).convert("RGB").resize((cell, cell)), (label_w + i * cell, y))
                else:
                    rig._placeholder(d, label_w + i * cell, y, cell, f"{SHORT[r['tool']]}: not rendered", fs)
            if r["scores"]:
                sheet.paste(r["heat"].resize((cell, cell)), (label_w + 2 * cell, y))
                m = r["scores"]["subjects"]
                part = {k: r["scores"][k]["dE_mean"] for k in ("sphere", "cube", "floor") if k in r["scores"]}
                d.text((label_w + 10, y + cell + 6),
                       f"{SHORT[r['tool']]}, {view}: set vs authored dE2000 mean {m['dE_mean']:.2f}, "
                       f"p95 {m['dE_p95']:.2f}   ·   " + ", ".join(f"{k} {x:.2f}" for k, x in part.items()),
                       fill=(200, 200, 150), font=fs)
                lines.append(f"| {view} | {SHORT[r['tool']]} | {m['dE_mean']:.2f} | {m['dE_p95']:.2f} | "
                             + " | ".join(f"{part[k]:.2f}" if k in part else "—"
                                          for k in ("sphere", "cube", "floor")) + " |")
            else:
                rig._placeholder(d, label_w + 2 * cell, y, cell, "nothing to compare", fs)
                lines.append(f"| {view} | {SHORT[r['tool']]} | not rendered | | | | |")
            y += cell + line_h
        y += gap
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    card = out.with_suffix(".md")
    card.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nsheet  {out}\nscores {card}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
