#!/usr/bin/env python3
"""The parity rig: one material, side by side in USDLiveView's renderer and Blender.

    uv run tools/parity/rig.py <article> [--sweep] [--width 512] [--samples 128]

``<article>`` is an article stem (``GreyCard_Neutral18_Clean_Base_s01_v01``) or a path to
its ``.mtlx``. The rig writes a render job (``job.py``), runs
the Storm driver and the Blender driver on it, and writes, into
``library/parity/<article>/`` (git-ignored):

* ``sheet.png`` — one row per slider setting: Storm | Blender | Unreal (empty until
  Phase06) | where they differ (black = same, yellow = at the bar, red = 3x the bar);
* ``scorecard.md`` (and ``scorecard.json``) — ΔE2000 per setting over the subjects, per
  subject, and the verdict against the master's bar.

It prints both paths. ``--sweep`` renders every slider the article declares through its
range (Phase05 step 5.2); without it, only the article's own settings.

Tools: Storm via ``$USD_TOOLS_ROOT`` (as make_preview.py), Blender as ``$MATTER_BLENDER``
or ``blender`` on PATH (5.2 LTS).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "drivers"))
import compare  # noqa: E402
import job as jobmod  # noqa: E402
import storm  # noqa: E402

OUT_ROOT = jobmod.REPO / "library" / "parity"
BLENDER_DRIVER = HERE / "drivers" / "blender_render.py"

# The bar per master (Decision of record 9): ΔE2000 < 2 is graded for these; the others are
# judged "recognisable" by eye and their numbers are advisory. The first numbers set each
# master's final bar (Phase05 Brief §Decisions that bind).
BAR = 2.0
GRADED = {"Opaque", "Masked", "Emissive", "TwoLayer"}


def settings_for(art: jobmod.Article, sweep: bool) -> list[dict]:
    s = [{"id": "defaults", "label": "defaults", "set": {}}]
    if not sweep:
        return s
    raise SystemExit("--sweep arrives in Phase05 step 5.2")


def run_blender(job_path: Path) -> None:
    exe = os.environ.get("MATTER_BLENDER") or shutil.which("blender")
    if not exe:
        raise SystemExit("Blender not found (set MATTER_BLENDER or put blender on PATH)")
    log = job_path.parent / "blender.log"
    with log.open("w", encoding="utf-8") as fh:
        rc = subprocess.run([exe, "-b", "--factory-startup", "--python-exit-code", "1",
                             "--python", str(BLENDER_DRIVER), "--", str(job_path)],
                            stdout=fh, stderr=subprocess.STDOUT).returncode
    if rc != 0:
        raise SystemExit(f"Blender driver failed (exit {rc}); see {log}")


def _font(size: int):
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def build_sheet(job: dict, scores: dict, heat: dict, cell: int) -> Path:
    out = Path(job["out_dir"])
    cols = ["USDLiveView (Storm)", "Blender (Cycles)", "Unreal", "Where they differ"]
    label_w, head_h, row_gap = 190, 72, 34
    rows = job["settings"]
    W = label_w + cell * len(cols)
    H = head_h + len(rows) * (cell + row_gap)
    sheet = Image.new("RGB", (W, H), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    f, fs = _font(18), _font(15)
    d.text((10, 10), f"{job['article']['name']}   ·   master {job['article']['master']}   ·   "
           f"bar dE2000 < {BAR:g}", fill=(235, 235, 235), font=f)
    for i, c in enumerate(cols):
        d.text((label_w + i * cell + 10, 42), c, fill=(200, 200, 200), font=f)
    for r, s in enumerate(rows):
        y = head_h + r * (cell + row_gap)
        d.text((10, y + 10), s["label"], fill=(235, 235, 235), font=f)
        for i, tool in enumerate(("storm", "blender")):
            img = Image.open(out / tool / f"{s['id']}.png").convert("RGB").resize((cell, cell))
            sheet.paste(img, (label_w + i * cell, y))
        d.rectangle([label_w + 2 * cell, y, label_w + 3 * cell - 1, y + cell - 1], fill=(40, 40, 40))
        d.text((label_w + 2 * cell + 20, y + cell // 2 - 10), "Unreal: no pictures yet",
               fill=(150, 150, 150), font=f)
        sheet.paste(heat[s["id"]].resize((cell, cell)), (label_w + 3 * cell, y))
        sc = scores[s["id"]]["subjects"]
        verdict = "under the bar" if sc["dE_mean"] < BAR else "OVER the bar"
        d.text((label_w + 10, y + cell + 8),
               f"dE2000 on the subjects: mean {sc['dE_mean']:.2f}, p95 {sc['dE_p95']:.2f}  "
               f"(bar {BAR:g}: {verdict})   SSIM {sc['ssim']:.3f}",
               fill=(120, 230, 120) if sc["dE_mean"] < BAR else (255, 140, 120), font=fs)
    p = out / "sheet.png"
    sheet.save(p)
    return p


def write_scorecard(job: dict, scores: dict) -> Path:
    out = Path(job["out_dir"])
    master = job["article"]["master"]
    graded = master in GRADED
    lines = [f"# Parity scorecard — {job['article']['name']}", "",
             f"Master **{master}** · bar ΔE2000 < {BAR:g} "
             f"({'graded' if graded else 'advisory: judged recognisable by eye'}) · "
             f"{job['width']} px · Cycles {job['samples']} samples · "
             f"written {time.strftime('%Y-%m-%d %H:%M')}", "",
             "ΔE2000 between USDLiveView's renderer (Storm) and Blender (Cycles), over the "
             "subjects' pixels (sphere, cube, floor).", "",
             "| Setting | Subjects mean | Subjects p95 | Sphere | Cube | Floor | SSIM | Verdict |",
             "|---|---|---|---|---|---|---|---|"]
    for s in job["settings"]:
        sc = scores[s["id"]]
        m = sc["subjects"]
        v = "under" if m["dE_mean"] < BAR else "**OVER**"
        lines.append(f"| {s['label']} | {m['dE_mean']:.2f} | {m['dE_p95']:.2f} | "
                     f"{sc['sphere']['dE_mean']:.2f} | {sc['cube']['dE_mean']:.2f} | "
                     f"{sc['floor']['dE_mean']:.2f} | {m['ssim']:.3f} | {v} |")
    p = out / "scorecard.md"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "scorecard.json").write_text(json.dumps(scores, indent=2) + "\n", encoding="utf-8")
    return p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Render one material side by side in Storm and Blender.")
    ap.add_argument("article")
    ap.add_argument("--sweep", action="store_true", help="every declared slider through its range")
    ap.add_argument("--width", type=int, default=512)
    ap.add_argument("--samples", type=int, default=128)
    ap.add_argument("--cell", type=int, default=320, help="picture size on the sheet")
    ap.add_argument("--out", default=None, help=f"default: {OUT_ROOT}/<article>")
    args = ap.parse_args(argv)

    art = jobmod.Article.read(jobmod.find_article(args.article))
    out = Path(args.out) if args.out else OUT_ROOT / art.name
    job_path = jobmod.write_job(art, settings_for(art, args.sweep), out, args.width, args.samples)
    job = json.loads(job_path.read_text(encoding="utf-8"))

    t0 = time.time()
    storm.run(job_path)
    t1 = time.time()
    run_blender(job_path)
    t2 = time.time()

    scores, heat = {}, {}
    for s in job["settings"]:
        sc, dE = compare.compare(out / "storm" / f"{s['id']}.png",
                                 out / "blender" / f"{s['id']}.png", out / "mask.png")
        scores[s["id"]] = sc
        heat[s["id"]] = compare.heatmap(dE, BAR)
    sheet = build_sheet(job, scores, heat, args.cell)
    card = write_scorecard(job, scores)
    print(f"storm {t1 - t0:.1f}s · blender {t2 - t1:.1f}s")
    print(f"sheet     {sheet}")
    print(f"scorecard {card}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
