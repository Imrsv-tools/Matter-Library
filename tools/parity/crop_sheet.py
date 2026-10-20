#!/usr/bin/env python3
"""Crop a rig sheet's rows so a reader (an agent) can look at them: a whole sweep sheet is ~1790 x 17000 px.

    uv run tools/parity/crop_sheet.py [--full] <stem> <setting-label substring> [...]

Writes one half-size PNG per named setting (all its views) to /tmp/p11_<stem>__<label>[_full].png and
prints each path with the setting's label. The file is named for the setting, so crops from separate
calls never overwrite each other. ``--full`` keeps full size: a small sharp highlight (a coat, a
polish) can vanish at half size. Phase11 (the build loop reads its own sheets)."""
import argparse
import json
import re
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[2]
ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
ap.add_argument("--full", action="store_true", help="keep full size")
ap.add_argument("stem")
ap.add_argument("wants", nargs="+", metavar="label", help="a substring of a setting's label")
args = ap.parse_args()

out = REPO / "library" / "parity" / args.stem
job = json.loads((out / "job.json").read_text())
labels = [s["label"] for s in job["settings"]]
im = Image.open(out / "sheet.png")
w, h = im.size
block = h / len(labels)          # each setting is one block (all its views), stacked
for want in args.wants:
    i = next((i for i, l in enumerate(labels) if want in l), None)
    if i is None:
        raise SystemExit(f"no setting label contains {want!r}; the labels: {', '.join(labels)}")
    crop = im.crop((0, int(i * block), w, int((i + 1) * block)))
    if not args.full:
        crop = crop.resize((w // 2, int(block) // 2))
    p = Path(f"/tmp/p11_{args.stem}__{re.sub(r'[^A-Za-z0-9]+', '_', labels[i]).strip('_')}{'_full' if args.full else ''}.png")
    crop.save(p)
    print(p, labels[i])
