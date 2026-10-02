#!/usr/bin/env python3
"""Crop a rig sheet's rows so a reader (an agent) can look at them: a whole sweep sheet is ~1790 x 17000 px.

    uv run tools/parity/crop_sheet.py <stem> <setting-label substring> [...]

Writes one half-size PNG per named setting (all its views) to /tmp/p11_<stem[:20]>_<n>.png and prints
each path with the setting's label. Phase11 (the build loop reads its own sheets)."""
import json
import sys
from pathlib import Path

from PIL import Image

REPO = Path(__file__).resolve().parents[2]
stem, wants = sys.argv[1], sys.argv[2:]
out = REPO / "library" / "parity" / stem
job = json.loads((out / "job.json").read_text())
labels = [s["label"] for s in job["settings"]]
im = Image.open(out / "sheet.png")
w, h = im.size
block = h / len(labels)          # each setting is one block (all its views), stacked
for n, want in enumerate(wants):
    i = next(i for i, l in enumerate(labels) if want in l)
    crop = im.crop((0, int(i * block), w, int((i + 1) * block)))
    crop = crop.resize((w // 2, int(block) // 2))
    p = Path(f"/tmp/p11_{stem[:20]}_{n}.png")
    crop.save(p)
    print(p, labels[i])
