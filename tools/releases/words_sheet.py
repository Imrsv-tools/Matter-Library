#!/usr/bin/env python3
"""The words sheet (Phase13 13.2): each material's name, one-line summary, search words and origin
beside its picture, drawn FROM a built snapshot's site file and its own pictures, so the maintainer
confirms exactly what would be published.

    uv run tools/releases/words_sheet.py --tag matterlib-0.2.0-dev.2
        -> library/snapshots/<tag>/_words/<NN>_<domain>.png  (git-ignored; not an asset)

One page per domain, split every ROWS materials. A material with no rig picture shows a grey cell
saying so, as the site shows a swatch.
"""
import argparse
import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

REPO = Path(__file__).resolve().parents[2]
SNAPSHOTS = REPO / "library" / "snapshots"
PIC, ROWS, W = 170, 12, 1500
def _font(names: tuple[str, ...], size: int):
    """The first of these fonts the machine has (DejaVu is not on every Linux; Fedora ships
    Noto), else Pillow's own scalable default at the same size."""
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


BOLD = ("DejaVuSans-Bold.ttf", "/usr/share/fonts/google-noto/NotoSans-Bold.ttf")
REGULAR = ("DejaVuSans.ttf", "/usr/share/fonts/google-noto/NotoSans-Regular.ttf")
BIG, FONT, SMALL = _font(BOLD, 24), _font(REGULAR, 19), _font(REGULAR, 16)


def picture(snap: Path, mat: dict) -> Image.Image:
    pics = {(p["tool"], p["view"]): p["file"] for p in mat.get("pictures", [])}
    for key in (("blender", "close"), ("storm", "close"), ("unreal", "close"), ("blender", "wide"), ("storm", "wide")):
        if key in pics:
            return Image.open(snap / pics[key]).convert("RGB").resize((PIC, PIC))
    cell = Image.new("RGB", (PIC, PIC), (70, 70, 70))
    ImageDraw.Draw(cell).text((12, PIC // 2 - 20), "no rig picture\nyet", fill=(200, 200, 200), font=SMALL)
    return cell


def page(snap: Path, title: str, mats: list[dict]) -> Image.Image:
    h = 60 + len(mats) * (PIC + 14)
    im = Image.new("RGB", (W, h), (24, 24, 24))
    d = ImageDraw.Draw(im)
    d.text((14, 16), title, fill="white", font=BIG)
    y = 60
    for m in mats:
        im.paste(picture(snap, m), (14, y))
        x = PIC + 34
        d.text((x, y), m["label"], fill="white", font=BIG)
        d.text((x + 8 + d.textlength(m["label"], font=BIG), y + 5), f"   {m['identity']}", fill=(140, 140, 140), font=SMALL)
        ty = y + 32
        for line in textwrap.wrap(m.get("summary", "(no summary)"), 105):
            d.text((x, ty), line, fill=(230, 230, 230), font=FONT)
            ty += 24
        d.text((x, ty + 4), "search: " + ", ".join(m.get("search_words", [])), fill=(150, 200, 255), font=SMALL)
        d.text((x, ty + 26), f"origin: {', '.join(m.get('origin', []))}   ·   {m['domain']}/{m['material_class']} · "
                             f"{m['master']} · {m['status']}", fill=(170, 170, 170), font=SMALL)
        y += PIC + 14
    return im


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    args = ap.parse_args(argv)
    snap = SNAPSHOTS / args.tag
    site = json.loads((snap / f"{args.tag}.site.json").read_text(encoding="utf-8"))
    out = snap / "_words"
    out.mkdir(exist_ok=True)
    for old in out.glob("*.png"):
        old.unlink()
    by_domain: dict[str, list] = {}
    for m in site["materials"]:
        by_domain.setdefault(m["domain"], []).append(m)
    n = 0
    for domain in sorted(by_domain):
        mats = sorted(by_domain[domain], key=lambda m: (m["material_class"], m["label"]))
        parts = [mats[i:i + ROWS] for i in range(0, len(mats), ROWS)]
        for k, part in enumerate(parts, 1):
            n += 1
            title = f"Words for {args.tag} — {domain} ({k} of {len(parts)}): name · summary · search words · origin"
            page(snap, title, part).save(out / f"{n:02d}_{domain}_{k}.png")
    print(f"{n} pages: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
