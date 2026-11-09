#!/usr/bin/env python3
"""The fade sheet: the rig's 11 test-set articles in Unreal, fully there and part-faded (Phase29).

    uv run tools/parity/fade.py [--fade 0 --fade 0.5] [--supersample 1] [--width 512] [--out <dir>]
                                [--article grey ...] [--frames N]

Phase29 (RD-P29-1, RD-P29-3): every master draws an object part-present as a DISSOLVE, each pixel
kept or dropped against its threshold (29.3: a blue-noise tile, 4096 levels). The rig's averaging hides that (F-P29-1: it renders 4x
and box-filters each block, which turns a dissolve into a smooth see-through fade), so this renders
at ONE SAMPLE PER PIXEL by default, the way a headset draws it.

One launch of the library's Unreal runtime draws every article: each gets its own sphere, cube and
floor (its ``st`` divided by its own ``meters_per_tile``, as the rig's setting scene does), all in
the rig's places, and one view per article from the rig's wide camera hides the other articles'
subjects. A ``--fade`` is ``object_fade`` (MasterSet §Object fade) on every subject: 0 = fully
there, 0.5 = half gone; one column each. The ruler and the wall never fade.

Writes ``<out>/<setting>__<article>.png`` (``fade000``, ``fade050`` ...), ``<out>/fade_sheet.png``
at native resolution (no picture is resized), and ``<out>/captures.json``: each capture's sha256
over its linear float picture, so two runs compare exactly (a presence-1 baseline taken before a
builder change must match after it, pixel for pixel). Default ``<out>``: ``library/parity/Fade``.

A fade other than 0 needs a runtime that reads job format 6 (built at Phase29 or later); a run of
``--fade 0`` alone is a format-3 job any runtime draws.

``--article <short>`` (repeatable) draws only those articles (a slow fade on one article in many
small steps). ``--frames N`` (Phase29 29.3, job format 7) is a desktop's TSR on a still view: the
view runs TSR, so the masters shift the fade's threshold every frame, and each picture is TSR's own
output after N frames (post-processed colour, so not pixel-comparable with a one-sample picture),
which should read as an even fade.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "drivers"))
sys.path.insert(0, str(HERE / "scene"))
import build_scene  # noqa: E402
import job as jobmod  # noqa: E402
import rig  # noqa: E402
import unreal as drv  # noqa: E402

# JOB_FORMAT.md §The test set, in its order; the short name is the view's suffix
TEST_SET = {"grey": "GreyCard_Neutral18_Clean_Base_s01_v01", "abs": "ABS_Glossy_Clean_Base_s01_v01",
            "copper": "Copper_Verdigris_Aged_Base_s01_v01", "oak": "Oak_Natural_Clean_Base_s1_v01",
            "rust": "Rust_OnSteel_Flaking_Base_s01_v01", "lace": "Lace_Floral_Clean_Base_s01_v01",
            "neon": "Neon_Signage_Clean_Base_s01_v01", "glass": "Glass_Clear_Clean_Base_s01_v01",
            "glassgreen": "Glass_Green_Clean_Base_s01_v01", "diamond": "Diamond_Brilliant_Clean_Base_s01_v01",
            "marble": "Marble_Veined_Polished_Base_s01_v01"}
SUBJECTS = {"Sphere": build_scene.sphere, "Cube": build_scene.rounded_cube, "Floor": build_scene.floor}


def setting_id(fade: float) -> str:
    return f"fade{round(fade * 100):03d}" if fade >= 0 else f"fadein{round(-fade * 100):03d}"


def build_job(fades: list[float], width: int, supersample: int, work: Path, articles: dict,
              frames: int = 0) -> tuple[Path, list, list]:
    """The runtime's job; returns its path, the settings and the views."""
    meshes_dir = work / "meshes"
    meshes_dir.mkdir(parents=True, exist_ok=True)
    meshes, mats, subjects = [], {}, {}
    for short, stem in articles.items():
        art = jobmod.Article.read(jobmod.find_article(stem))
        slot = f"art_{short}"
        mats[slot] = drv.article_material(art.path)
        subjects[short] = []
        for name, make in SUBJECTS.items():
            pts, nrm, uvs, idx = make()
            mpt = art.meters_per_tile
            mesh = drv.write_mesh(meshes_dir, f"{name}_{short}", pts, nrm, [(s / mpt, t / mpt) for s, t in uvs],
                                  idx, slot)
            meshes.append(mesh)
            subjects[short].append(mesh["name"])
    for name, mesh, mat in (("RulerBlack", build_scene.ruler(True), "ruler_black"),
                            ("RulerWhite", build_scene.ruler(False), "ruler_white"),
                            ("Wall", build_scene.wall(), "wall")):
        meshes.append(drv.write_mesh(meshes_dir, name, *mesh, mat))
    mats |= {"ruler_black": drv.preview_surface(0.02), "ruler_white": drv.preview_surface(0.8),
             "wall": drv.preview_surface(texture=(build_scene.HERE / build_scene.UVGRID).resolve(), roughness=0.8)}
    views = [drv.camera_view(build_scene.CAM_POS, (build_scene.CAM_PITCH, 0.0), f"__{short}",
                             [m for other, names in subjects.items() if other != short for m in names])
             for short in articles]
    settings = []
    for f in fades:
        s = {"id": setting_id(f), "materials": mats}
        if f != 0.0:
            s["fade"] = {m: f for names in subjects.values() for m in names}
        settings.append(s)
    sun, sky = drv.lights()
    fmt = drv.FADE_JOB_FORMAT if any(f != 0.0 for f in fades) else drv.JOB_FORMAT
    ujob = {"format": fmt, "width": width * supersample, "out_dir": str(work / "raw"),
            "settle_frames": drv.SETTLE_FRAMES, "sun": sun, "sky": sky, "meshes": meshes,
            "settings": [drv.warmup(settings)] + settings, "views": views}
    if frames:
        ujob |= {"format": drv.TEMPORAL_JOB_FORMAT, "temporal_frames": frames}
    p = work / "fade_job.json"
    p.write_text(json.dumps(ujob, indent=1) + "\n", encoding="utf-8")
    return p, settings, views


def sheet(out: Path, fades: list[float], width: int, articles: dict, frames: int = 0) -> Path:
    """Rows: the articles; columns: the fades. Every picture at its own size, never resized."""
    font, small, pad, head, label = rig._font(22), rig._font(16), 8, 44, 250
    w = label + len(fades) * (width + pad) + pad
    h = head + len(articles) * (width + pad) + pad
    img = Image.new("RGB", (w, h), (24, 24, 24))
    d = ImageDraw.Draw(img)
    for c, f in enumerate(fades):
        title = "fully there" if f == 0 else f"object_fade {f:g}: {round((1 - abs(f)) * 100, 1):g} % present"
        if frames:
            title += f", TSR after {frames} frames"
        d.text((label + pad + c * (width + pad), 12), title, fill=(235, 235, 235), font=font)
    for r, (short, stem) in enumerate(articles.items()):
        y = head + pad + r * (width + pad)
        master = jobmod.Article.read(jobmod.find_article(stem)).master
        d.text((pad, y + width // 2 - 20), stem.split("_Base")[0].replace("_Clean", ""), fill=(220, 220, 220), font=small)
        d.text((pad, y + width // 2 + 4), master, fill=(150, 150, 150), font=small)
        for c, f in enumerate(fades):
            img.paste(Image.open(out / f"{setting_id(f)}__{short}.png").convert("RGB"),
                      (label + pad + c * (width + pad), y))
    p = out / "fade_sheet.png"
    img.save(p)
    return p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--fade", type=float, action="append",
                    help="object_fade on every subject, one column each (repeatable; default 0 and 0.5)")
    ap.add_argument("--supersample", type=int, default=1,
                    help="samples per pixel along each side, box-filtered (default 1: the dissolve as drawn; "
                         f"the rig's is {drv.SUPERSAMPLE})")
    ap.add_argument("--width", type=int, default=512)
    ap.add_argument("--out", type=Path)
    ap.add_argument("--article", action="append", choices=list(TEST_SET),
                    help="draw only this article (repeatable; default all 11)")
    ap.add_argument("--frames", type=int, default=0,
                    help="a still view under TSR: each picture TSR's output after N frames (job format 7)")
    a = ap.parse_args(argv)
    articles = {k: v for k, v in TEST_SET.items() if not a.article or k in a.article}
    if a.frames < 0:
        ap.error("--frames is 0 (one fixed frame) or more")
    fades = a.fade or [0.0, 0.5]
    if any(abs(f) > 1 for f in fades):
        ap.error("--fade is -1 .. 1")
    out = (a.out or rig.OUT_ROOT / "Fade").resolve()
    work = out / "work"
    shutil.rmtree(work, ignore_errors=True)
    upath, settings, views = build_job(fades, a.width, a.supersample, work, articles, a.frames)
    cmd = drv.find_runtime()
    if cmd is None:
        raise SystemExit("no Unreal runtime (set MATTER_UNREAL_RUNTIME or MATTER_UNREAL_EDITOR)")
    wanted = [(s["id"], v["suffix"]) for s in settings for v in views]
    raw = work / "raw"
    drv.run_runtime(cmd, upath, work / "unreal.log", [raw / f"{i}{x}.pfm" for i, x in wanted])
    shas = {}
    for i, x in wanted:
        pfm = raw / f"{i}{x}.pfm"
        shas[f"{i}{x}"] = hashlib.sha256(pfm.read_bytes()).hexdigest()
        Image.fromarray(drv.srgb8(drv.linear(pfm, supersample=a.supersample))).save(out / f"{i}{x}.png")
    for pfm in raw.glob("*.pfm"):
        pfm.unlink()                                  # ~50 MB each at 4x; the hashes and PNGs are the record
    (out / "captures.json").write_text(json.dumps({"supersample": a.supersample, "width": a.width,
                                                   "frames": a.frames, "sha256": shas}, indent=1) + "\n",
                                       encoding="utf-8")
    print(f"fade sheet {sheet(out, fades, a.width, articles, a.frames)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
