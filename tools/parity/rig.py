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
# Views whose numbers are advisory for a graded master (set from the first numbers, 5.4):
# on the whole set a cut-out's holes are smaller than a pixel, and a real-time renderer
# (Storm, Unreal) filters the opacity texture BEFORE the cut-out test while a path tracer
# cuts per sample, so the two draw different coverage there by construction. The close-up,
# where the holes are resolved, is graded.
ADVISORY_VIEWS = {"Masked": {"wide"}}


VIEW_LABELS = {"wide": "whole set", "close": "close-up", "dim": "whole set, -4 stops"}
VIEW_NOTES = {
    "close": "The cube's front face and the floor in front: wear layers are big enough to "
             "see here (a 1 cm grain is ~15 px).",
    "dim": "The whole set at exposure -4 (1/16): emission is judged here, unclipped (at "
           "exposure 0 a bright emitter is display white in both tools).",
}


def graded(master: str, view: str) -> bool:
    return master in GRADED and view not in ADVISORY_VIEWS.get(master, set())


def verdict(master: str, view: str, de: float, md: bool = True) -> str:
    """'under' / 'OVER' the bar, marked advisory where this master's view is not graded."""
    word = "under" if de < BAR else ("**OVER**" if md else "OVER")
    return word if graded(master, view) else f"{word} (advisory)"


# The sweep (Phase05 Brief, first human test click 2): each slider the article declares,
# moved on its own from the article's start values.
SWEEP = [
    ("base_color_tint", [("tint blue", (0.5, 0.75, 1.0))]),
    ("roughness_bias", [("roughness -0.5", -0.5), ("roughness +0.5", 0.5)]),
    ("overlay1_density", [("wear 1 at 0", 0.0), ("wear 1 at 0.5", 0.5), ("wear 1 at 1", 1.0)]),
    ("overlay2_density", [("wear 2 at 0", 0.0), ("wear 2 at 0.5", 0.5), ("wear 2 at 1", 1.0)]),
    ("overlay3_density", [("wear 3 at 0", 0.0), ("wear 3 at 0.5", 0.5), ("wear 3 at 1", 1.0)]),
    # the mask only GATES wear, so its rows turn every declared wear layer up to 1 (on an
    # article whose wear starts at 0, a bare mask row moves nothing: Oak, 5.2)
    ("maskset_blend", [("mask blend 0, wear at 1", 0.0), ("mask blend 1, wear at 1", 1.0)]),
    ("uv_scale", [("UV scale 0.5", (0.5, 0.5)), ("UV scale 2", (2.0, 2.0))]),
    ("uv_rotation", [("UV rotation 90", 90.0)]),
]


def settings_for(art: jobmod.Article, sweep: bool) -> list[dict]:
    s = [{"id": "defaults", "label": "defaults", "set": {}}]
    if not sweep:
        return s
    for port, rows in SWEEP:
        if port not in art.ports:
            continue
        for label, value in rows:
            sid = (label.replace(",", "").replace(" ", "_").replace("+", "p")
                   .replace("-", "m").replace(".", ""))
            setting = {port: list(value) if isinstance(value, tuple) else value}
            if port == "maskset_blend":
                setting.update({p: 1.0 for p in art.ports if p.startswith("overlay")})
            s.append({"id": sid, "label": label, "port": port, "set": setting})
    return s


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
    label_w, head_h, line_h, row_gap = 190, 72, 30, 30
    rows, views = job["settings"], list(job["views"])
    block = len(views) * (cell + line_h) + row_gap          # one setting: every view, stacked
    W = label_w + cell * len(cols)
    H = head_h + len(rows) * block
    sheet = Image.new("RGB", (W, H), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    f, fs = _font(18), _font(15)
    d.text((10, 10), f"{job['article']['name']}   ·   master {job['article']['master']}   ·   "
           f"bar dE2000 < {BAR:g}", fill=(235, 235, 235), font=f)
    for i, c in enumerate(cols):
        d.text((label_w + i * cell + 10, 42), c, fill=(200, 200, 200), font=f)
    for r, s in enumerate(rows):
        y0 = head_h + r * block
        d.text((10, y0 + 10), s["label"], fill=(235, 235, 235), font=f)
        for k, v in enumerate(views):
            y = y0 + k * (cell + line_h)
            sfx = job["views"][v]["suffix"]
            d.text((10, y + 40), f"({job['views'][v].get('label') or VIEW_LABELS.get(v, v)})",
                   fill=(150, 150, 150), font=fs)
            for i, tool in enumerate(("storm", "blender")):
                img = Image.open(out / tool / f"{s['id']}{sfx}.png").convert("RGB").resize((cell, cell))
                sheet.paste(img, (label_w + i * cell, y))
            d.rectangle([label_w + 2 * cell, y, label_w + 3 * cell - 1, y + cell - 1], fill=(40, 40, 40))
            d.text((label_w + 2 * cell + 20, y + cell // 2 - 10), "Unreal: no pictures yet",
                   fill=(150, 150, 150), font=f)
            sheet.paste(heat[s["id"]][v].resize((cell, cell)), (label_w + 3 * cell, y))
            sc = scores[s["id"]]["views"][v]
            m = sc["subjects"]
            ok = m["dE_mean"] < BAR or not graded(job["article"]["master"], v)
            said = verdict(job["article"]["master"], v, m["dE_mean"], md=False)
            mv = sc.get("moved")
            moved = (f"   ·   the slider moved Storm {mv['storm']:.1f}, Blender {mv['blender']:.1f}"
                     if mv else "")
            d.text((label_w + 10, y + cell + 6),
                   f"dE2000 between the tools: mean {m['dE_mean']:.2f}, p95 {m['dE_p95']:.2f}  "
                   f"(bar {BAR:g}: {said}){moved}",
                   fill=(120, 230, 120) if ok else (255, 140, 120), font=fs)
    p = out / "sheet.png"
    sheet.save(p)
    return p


SCALE_TOLERANCE = 0.03     # found size within 3 % of the expected one


def scale_checks(art: jobmod.Article, job: dict) -> list[dict]:
    """The ruler check: does the base texture render at its recorded size, in each tool?

    Run on the defaults and on each UV-scale row, where the expected size is the slider's
    value (uv_scale divides the coordinate, so 2 renders the texture twice as large). A
    rotated row is skipped (the check correlates the unrotated texture).
    """
    tex = art.textures.get("base_color_tex")
    if tex is None:
        return []
    out = Path(job["out_dir"])
    rows = []
    for s in job["settings"]:
        port = s.get("port")
        if s["id"] == "defaults":
            want = float(art.ports.get("uv_scale", ("", "1, 1"))[1].split(",")[0])
        elif port == "uv_scale":
            want = float(s["set"]["uv_scale"][0])
        else:
            continue
        row = {"setting": s["label"], "expected": want}
        for tool in ("storm", "blender"):
            r = compare.texture_scale(out / tool / f"{s['id']}.png", tex, art.meters_per_tile)
            row[tool] = r
        row["ok"] = all(abs(row[t]["size"] / want - 1) <= SCALE_TOLERANCE for t in ("storm", "blender"))
        rows.append(row)
    return rows


def write_scorecard(job: dict, scores: dict, checks: dict) -> Path:
    out = Path(job["out_dir"])
    master = job["article"]["master"]
    is_graded = master in GRADED
    lines = [f"# Parity scorecard — {job['article']['name']}", "",
             f"Master **{master}** · bar ΔE2000 < {BAR:g} "
             f"({'graded' + (', except the ' + ' and '.join(sorted(ADVISORY_VIEWS[master])) + ' view (advisory)' if master in ADVISORY_VIEWS else '') if is_graded else 'advisory: judged recognisable by eye'}) · "
             f"{job['width']} px · Cycles {job['samples']} samples · "
             f"written {time.strftime('%Y-%m-%d %H:%M')}", "",
             "ΔE2000 between USDLiveView's renderer (Storm) and Blender (Cycles), over the "
             "subjects' pixels (sphere, cube, floor).", "",
             "**Moved** is how far the slider changed each tool's own picture from its defaults "
             "(mean dE2000 on the subjects). A slider that moves one tool and not the other is "
             "**ONE-SIDED**.", "",
             "| Setting | Between tools: mean | p95 | Sphere | Cube | Floor | SSIM | Moved: Storm | Moved: Blender | Verdict |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for s in job["settings"]:
        sc = scores[s["id"]]
        m = sc["subjects"]
        v = verdict(master, "wide", m["dE_mean"])
        mv = sc.get("moved")
        if mv and (max(mv.values()) > 1.0 and min(mv.values()) < 0.25 * max(mv.values())):
            v += " · **ONE-SIDED**"
        ms = f"{mv['storm']:.2f} | {mv['blender']:.2f}" if mv else "— | —"
        lines.append(f"| {s['label']} | {m['dE_mean']:.2f} | {m['dE_p95']:.2f} | "
                     f"{sc['sphere']['dE_mean']:.2f} | {sc['cube']['dE_mean']:.2f} | "
                     f"{sc['floor']['dE_mean']:.2f} | {m['ssim']:.3f} | {ms} | {v} |")
    for view in [v for v in job["views"] if v != "wide"]:
        lines += ["", f"## The {VIEW_LABELS.get(view, view)} view", "", VIEW_NOTES.get(view, ""), "",
                  "| Setting | Between tools: mean | p95 | SSIM | Moved: Storm | Moved: Blender | Verdict |",
                  "|---|---|---|---|---|---|---|"]
        for s in job["settings"]:
            sc = scores[s["id"]]["views"][view]
            m = sc["subjects"]
            v = verdict(master, view, m["dE_mean"])
            mv = sc.get("moved")
            if mv and (max(mv.values()) > 1.0 and min(mv.values()) < 0.25 * max(mv.values())):
                v += " · **ONE-SIDED**"
            ms = f"{mv['storm']:.2f} | {mv['blender']:.2f}" if mv else "— | —"
            lines.append(f"| {s['label']} | {m['dE_mean']:.2f} | {m['dE_p95']:.2f} | "
                         f"{m['ssim']:.3f} | {ms} | {v} |")
    worst = {}
    for s in job["settings"]:
        if s.get("port"):
            for view, sc in scores[s["id"]]["views"].items():
                d = sc["subjects"]["dE_mean"]
                if d > worst.get(s["port"], (0, "", ""))[0]:
                    worst[s["port"]] = (d, s["label"], view)
    if worst:
        lines += ["", "**Per slider, the worst difference between the tools (either view):**", ""]
        lines += [f"- `{p}`: {d:.2f} at *{lab}*, {view} view "
                  f"({'under' if d < BAR else 'OVER'} the bar)"
                  for p, (d, lab, view) in worst.items()]
    mpt = job["article"]["meters_per_tile"]
    lines += ["", f"## Scale (the ruler check) — recorded size {mpt:g} m per tile", ""]
    if checks["scale"]:
        lines += ["The floor is sampled straight down and matched against the article's base "
                  "texture laid at k x its recorded size. **Size found** is the best k "
                  "(1.00 = exactly the recorded size); *match* is the correlation there.", "",
                  "| Setting | Expected | Storm: size found (match) | Blender: size found (match) | |",
                  "|---|---|---|---|---|"]
        for r in checks["scale"]:
            lines.append(f"| {r['setting']} | {r['expected']:.2f} | {r['storm']['size']:.2f} "
                         f"({r['storm']['ncc']:.2f}) | {r['blender']['size']:.2f} "
                         f"({r['blender']['ncc']:.2f}) | {'ok' if r['ok'] else '**OFF**'} |")
    else:
        lines.append("No base texture: nothing to measure.")
    lines += ["", "## Seams (Phase04's measure, on each texture the article uses)", "",
              "| Texture node | Across the wrap edge | Between interior neighbours | |", "|---|---|---|---|"]
    for n, s in checks["seams"].items():
        lines.append(f"| `{n}` | {s['wrap']:.1f} | {s['interior']:.1f} | "
                     f"{'seamless' if s['seamless'] else '**SEAM**'} |")
    if not checks["seams"]:
        lines.append("| (no textures) | | | |")
    p = out / "scorecard.md"
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "scorecard.json").write_text(json.dumps({"settings": scores, "checks": checks},
                                                   indent=2, default=str) + "\n", encoding="utf-8")
    return p


CHARACTER_SKIN = "Skin_FitzpatrickIII_Clean_Base_s001_v01"
# The character's cast: one article per part (Phase07 7.5). "Body" is the skin, the positional
# argument; every other part is fixed here.
CHARACTER_CAST = {
    "Lips": "Lips_Natural_Clean_Base_s001_v01",
    "Nails": "Nail_Natural_Clean_Base_s001_v01",
    "Cornea": "Cornea_Clear_Clean_Base_s001_v01",
    "Pupil": "Pupil_Dark_Clean_Base_s001_v01",
    "Iris": "Iris_Brown_Clean_Base_s001_v01",
    "Sclera": "Sclera_Natural_Clean_Base_s001_v01",
    "Teeth": "Enamel_Natural_Clean_Base_s001_v01",
    "Gums": "Gum_Natural_Clean_Base_s001_v01",
    "Tongue": "Tongue_Natural_Clean_Base_s001_v01",
    "Shirt": "Cotton_Jersey_Clean_Base_s001_v01",
    "Trousers": "Denim_Indigo_Clean_Base_s001_v01",
    "Shoes": "Leather_Brown_Clean_Base_s001_v01",
}


def region_colours(job: dict) -> dict | None:
    """A character job's regions: part name -> mask colour (None for the test scene)."""
    mc = job.get("mask_colours")
    return {p.rsplit("/", 1)[1]: c for p, c in mc.items()} if mc else None


def write_character_scorecard(job: dict, scores: dict) -> Path:
    out = Path(job["out_dir"])
    sc = scores["defaults"]["views"]
    parts = {b["subject"].rsplit("/", 1)[1]: b["article"] for b in job["bindings"]}
    lines = [f"# Parity scorecard — the character ({', '.join(f'{p}: {a['name']}' for p, a in parts.items())})",
             "", f"{job['width']} px · Cycles {job['samples']} samples · "
             f"written {time.strftime('%Y-%m-%d %H:%M')}", "",
             "ΔE2000 between USDLiveView's renderer (Storm) and Blender (Cycles), per bound part, "
             "per view. Unbound parts are the scene's grey and are not scored.", "",
             "| Part | Article (master) | " + " | ".join(
                 job["views"][v].get("label", v) for v in job["views"]) + " |",
             "|---|---|" + "---|" * len(job["views"])]
    for p, a in parts.items():
        cells = []
        for v in job["views"]:
            r = sc[v].get(p)
            cells.append(f"{r['dE_mean']:.2f} (p95 {r['dE_p95']:.2f})" if r else "not in view")
        lines.append(f"| {p} | {a['name']} ({a['master']}) | " + " | ".join(cells) + " |")
    card = out / "scorecard.md"
    card.write_text("\n".join(lines) + "\n", encoding="utf-8")
    (out / "scorecard.json").write_text(json.dumps({"settings": scores}, indent=2, default=str) + "\n",
                                        encoding="utf-8")
    return card


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Render one material side by side in Storm and Blender.")
    ap.add_argument("article", nargs="?",
                    help=f"the article (with --character: the skin; default {CHARACTER_SKIN})")
    ap.add_argument("--character", action="store_true",
                    help="the MakeHuman body instead of the test scene: whole body, face, hand")
    ap.add_argument("--sweep", action="store_true", help="every declared slider through its range")
    ap.add_argument("--width", type=int, default=512)
    ap.add_argument("--samples", type=int, default=128)
    ap.add_argument("--cell", type=int, default=400, help="picture size on the sheet")
    ap.add_argument("--out", default=None, help=f"default: {OUT_ROOT}/<article>")
    ap.add_argument("--score-only", action="store_true",
                    help="re-score the pictures already rendered (no Storm, no Blender)")
    args = ap.parse_args(argv)

    if args.character:
        if args.sweep:
            raise SystemExit("--sweep runs on the test scene; the character renders the defaults")
        art = jobmod.Article.read(jobmod.find_article(args.article or CHARACTER_SKIN))
        out = Path(args.out) if args.out else OUT_ROOT / f"Character__{art.name}"
        cast = {"Body": art} | {p: jobmod.Article.read(jobmod.find_article(a))
                                for p, a in CHARACTER_CAST.items()}
        job_path = jobmod.write_character_job(cast, out, args.width, args.samples)
    else:
        if not args.article:
            ap.error("an article is required (or --character)")
        art = jobmod.Article.read(jobmod.find_article(args.article))
        out = Path(args.out) if args.out else OUT_ROOT / art.name
        job_path = jobmod.write_job(art, settings_for(art, args.sweep), out, args.width, args.samples)
    job = json.loads(job_path.read_text(encoding="utf-8"))
    colours = region_colours(job)

    t0 = time.time()
    if not args.score_only:
        storm.run(job_path)
    t1 = time.time()
    if not args.score_only:
        run_blender(job_path)
    t2 = time.time()

    scores, heat = {}, {}
    views = job["views"]
    for s in job["settings"]:
        per_view, heat[s["id"]] = {}, {}
        for v, spec in views.items():
            sfx = spec["suffix"]
            mask = out / f"mask{sfx}.png"
            sc, dE = compare.compare(out / "storm" / f"{s['id']}{sfx}.png",
                                     out / "blender" / f"{s['id']}{sfx}.png", mask, colours)
            if s["id"] != "defaults":
                sc["moved"] = {t: compare.moved(out / t / f"{s['id']}{sfx}.png",
                                                out / t / f"defaults{sfx}.png", mask, colours)
                               for t in ("storm", "blender")}
            per_view[v] = sc
            heat[s["id"]][v] = compare.heatmap(dE, BAR, compare.masks(mask, colours)["subjects"])
        scores[s["id"]] = per_view["wide"] | {"views": per_view}
    sheet = build_sheet(job, scores, heat, args.cell)
    if args.character:
        card = write_character_scorecard(job, scores)
    else:
        checks = {"scale": scale_checks(art, job),
                  "seams": {n: compare.seam(p) for n, p in art.textures.items()}}
        card = write_scorecard(job, scores, checks)
    print(f"storm {t1 - t0:.1f}s · blender {t2 - t1:.1f}s")
    print(f"sheet     {sheet}")
    print(f"scorecard {card}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
