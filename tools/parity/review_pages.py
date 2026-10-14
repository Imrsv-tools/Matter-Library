#!/usr/bin/env python3
"""Review pages for a batch of the build loop (Phase11): per row of the batch, its close-up at the defaults
and with its dust at 1 (an emitter: the -4 stop view), Storm | Blender | Unreal, labelled. One page per
batch, so the maintainer reviews a batch without scrolling 17000-px sheets.

    uv run tools/parity/review_pages.py <batch> [<batch> ...]      # writes library/parity/_review/<batch>.png (git-ignored)
"""
import json
import sys
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[2]
PAR = REPO / "library" / "parity"
OUT = PAR / "_review"
OUT.mkdir(exist_ok=True)
rows = yaml.safe_load((REPO / "library" / "wishlist.yaml").read_text())["rows"]
CELL = 300
RECIPES = REPO / "tools" / "converters" / "recipes"
WORDS_H = 64      # the band under a row: the words the review confirms (Phase13 13.3)
try:
    FONT = ImageFont.truetype("DejaVuSans.ttf", 18)
    SMALL = ImageFont.truetype("DejaVuSans.ttf", 14)
except OSError:   # DejaVu is not on every Linux (Fedora ships Noto); Pillow's own lacks an em-dash
    try:
        FONT = ImageFont.truetype("/usr/share/fonts/google-noto/NotoSans-Regular.ttf", 18)
        SMALL = ImageFont.truetype("/usr/share/fonts/google-noto/NotoSans-Regular.ttf", 14)
    except OSError:
        FONT, SMALL = ImageFont.load_default(18), ImageFont.load_default(14)
sys.path.insert(0, str(REPO / "tools" / "releases"))
from build_snapshot import label as derived_label  # noqa: E402


def words(stem):
    """The words a keep confirms (Phase13 13.3): name, summary, search words, origin, from the recipe."""
    p = RECIPES / f"{stem}.json"
    rec = json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {}
    name = rec.get("label") or derived_label(stem.rsplit("_", 2)[0])
    if not rec.get("summary"):
        return f"{name} — NO WORDS YET: the row owes a summary, search words and origin", None
    return (f"{name} — {rec['summary']}",
            f"search: {', '.join(rec.get('search_words', []))}   ·   origin: {', '.join(rec.get('origin', []))}")


def pic(stem, tool, sid, sfx):
    p = PAR / stem / tool / f"{sid}{sfx}.png"
    return Image.open(p).convert("RGB").resize((CELL, CELL)) if p.is_file() else None


def deposit_setting(stem):
    """The deposit's slot is the one the sweep's soot row names; its plain 'wear N at 1' row is the dust."""
    job = json.loads((PAR / stem / "job.json").read_text())
    for s in job["settings"]:
        if "soot" in s["label"]:
            return s["id"].replace("_soot", ""), s["label"].replace(", soot", "")
    return None, None


for batch in sys.argv[1:]:
    mine = [r for r in rows if r.get("batch") == batch]
    lines = []
    for r in mine:
        stem = r["name"]
        job = json.loads((PAR / stem / "job.json").read_text())
        view = "dim" if r.get("master") == "Emissive" and "dim" in job["views"] else "close"
        sfx = job["views"].get(view, {}).get("suffix", "")
        dep_id, dep_label = deposit_setting(stem)
        cells = [pic(stem, t, "defaults", sfx) for t in ("storm", "blender", "unreal")]
        if dep_id:
            cells += [pic(stem, t, dep_id, sfx) for t in ("storm", "blender", "unreal")]
        lines.append((stem, r.get("kind"), r.get("master") + (" (-4 stops)" if view == "dim" else ""), dep_label, cells))
    W = 260 + 6 * CELL + 20
    H = 40 + len(lines) * (CELL + WORDS_H + 10)
    page = Image.new("RGB", (W, H), (24, 24, 24))
    d = ImageDraw.Draw(page)
    d.text((10, 10), f"Batch {batch} — close-up: defaults (Storm | Blender | Unreal), then the dust row at 1", fill="white", font=FONT)
    for i, (stem, kind, master, dep_label, cells) in enumerate(lines):
        y = 40 + i * (CELL + WORDS_H + 10)
        d.text((10, y + 10), "\n".join([stem[:28], stem[28:56], f"{master} · {kind}", dep_label or "no dust row"]), fill="white", font=SMALL)
        for j, c in enumerate(cells):
            x = 260 + j * CELL + (20 if j >= 3 else 0)
            if c is not None:
                page.paste(c, (x, y))
            else:
                d.text((x + 10, y + 10), "—", fill="grey", font=FONT)
        first, second = words(stem)
        d.text((10, y + CELL + 6), first, fill=(230, 230, 230) if second else (255, 140, 120), font=FONT)
        if second:
            d.text((10, y + CELL + 32), second, fill=(150, 200, 255), font=SMALL)
    p = OUT / f"{batch}.png"
    page.save(p)
    print(p, len(lines), "rows")
