#!/usr/bin/env python3
"""Make each article's thumbnails: showcase pictures in Cycles, and the record they were made from.

    uv run tools/thumbnails/make_thumbnails.py <article>... [--sheet NAME] [--force]
    uv run tools/thumbnails/make_thumbnails.py <article>... --draft      # small and fast: tuning the look

Writes ``library/thumbnails/<identity>/<view>.png`` (1024 x 1024) and ``record.json`` beside them
(git-ignored; RD-MP-6: thumbnails never go in git or LFS). A picture is made only when it is stale:
when its record is missing, or the article (its .mtlx and every texture it names), the Blender
masters, the renderer (Blender's version, Cycles, the device), the scene version, the samples, the
size, the subject or the views differ (``showcase.stale``). ``--force`` makes them anyway.

``--sheet NAME`` writes ``library/thumbnails/_sheets/NAME.png``: one row per article, the rig's
Blender pictures (wide over close, ``library/parity/<identity>/blender/``) beside the thumbnails at
full size. ``--draft`` renders at 384 px and 32 samples into ``library/thumbnails/_draft/`` with no
record, for tuning the scene; a draft is never a thumbnail.

Blender is ``$MATTER_BLENDER`` or ``blender`` on PATH, as for the rig. It renders on the first device
that can (the rig's ``pick_device``; ``MATTER_BLENDER_DEVICE`` forces it).
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "parity"))
sys.path.insert(0, str(HERE.parent / "parity" / "scene"))
import job as jobmod  # noqa: E402  (the rig's article reader and setting scene)
import showcase as S  # noqa: E402

BLENDER_SIDE = HERE / "showcase_blender.py"
PROBE = HERE / "probe_blender.py"
PARITY = S.REPO / "library" / "parity"


def blender_exe() -> str:
    exe = os.environ.get("MATTER_BLENDER") or shutil.which("blender")
    if not exe:
        raise SystemExit("Blender not found (set MATTER_BLENDER or put blender on PATH)")
    return exe


def run_blender(script: Path, arg: Path, log: Path) -> None:
    with log.open("w", encoding="utf-8") as fh:
        rc = subprocess.run([blender_exe(), "-b", "--factory-startup", "--python-exit-code", "1",
                             "--python", str(script), "--", str(arg)],
                            stdout=fh, stderr=subprocess.STDOUT).returncode
    if rc != 0:
        raise SystemExit(f"Blender failed (exit {rc}); see {log}")


def renderer() -> dict:
    """Blender's version, the engine, and the device it will render on: asked of Blender once."""
    tmp = Path(tempfile.mkdtemp(prefix="matter-thumb-probe-"))
    try:
        run_blender(PROBE, tmp / "probe.json", tmp / "probe.log")
        return json.loads((tmp / "probe.json").read_text(encoding="utf-8"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def look() -> dict:
    return {"hdri": str(S.HDRI), "hdri_strength": S.HDRI_STRENGTH, "hdri_rotation": S.HDRI_ROTATION,
            "key_pos": S.KEY_POS, "key_aim": S.KEY_AIM, "key_size": S.KEY_SIZE, "key_power": S.KEY_POWER,
            "rim_pos": S.RIM_POS, "rim_aim": S.RIM_AIM, "rim_size": S.RIM_SIZE, "rim_power": S.RIM_POWER,
            "rim_spread": S.RIM_SPREAD,
            "backdrop_albedo": S.BACKDROP_ALBEDO, "backdrop_roughness": S.BACKDROP_ROUGHNESS,
            "backdrop_floor_front": S.BACKDROP_FLOOR_FRONT, "backdrop_curve_z": S.BACKDROP_CURVE_Z,
            "backdrop_radius": S.BACKDROP_RADIUS, "backdrop_top": S.BACKDROP_TOP,
            "backdrop_width": S.BACKDROP_WIDTH, "view_transform": S.VIEW_TRANSFORM,
            "exposure": S.EXPOSURE}


def find(name: str) -> Path:
    """An article by its stem, a path, or its bare name (``Oak_Natural``) when only one stem has it."""
    hits = sorted(jobmod.MATERIALS.rglob(f"{name}_*.mtlx"))
    if "/" not in name and not name.endswith(".mtlx") and not list(jobmod.MATERIALS.rglob(f"{name}.mtlx")):
        bare = [h for h in hits if h.stem.split("_Clean_")[0].split("_Base_")[0] == name
                or h.stem.rsplit("_", 4)[0] == name]
        if len(bare) == 1:
            return bare[0]
    return jobmod.find_article(name)


def character_spec(art) -> tuple[dict, list[Path], dict]:
    """A Character article's subject: the clothed character wearing the rig's cast, on the skin of the
    article's own tone where there is one, with the article on its family's parts; its whitelisted
    views; and every file the picture is drawn from besides the article."""
    import build_character as B  # noqa: PLC0415  (heavy: parses the pinned CC0 sources)
    import rig  # noqa: PLC0415  (the rig's cast)
    parts_of, views = S.character_family(art.name)
    variant = art.name.split("_")[1]
    skin = f"Skin_{variant}_Clean_Base_s001_v01"
    if not list(jobmod.MATERIALS.rglob(f"{skin}.mtlx")):
        skin = rig.CHARACTER_SKIN
    cast = {"Body": skin} | rig.cast_for(skin) | {p: art.name for p in parts_of}
    arts = {p: jobmod.Article.read(jobmod.find_article(a)) for p, a in cast.items()}
    meshmaps = B.mesh_maps()
    parts = B.load_parts()
    cams = S.character_cameras(parts, B.cameras(parts))
    hide_always = [] if "Cornea" in parts_of else ["Cornea"]     # as the rig hides it (RD-P09-4)
    extra = S.CHARACTER_VIEW_EXTRA.get(art.name.split("_")[0], {})
    view_specs = {}
    for v in views:
        c = dict(cams[v])
        if extra.get("raise"):
            c["pos"] = (c["pos"][0], round(c["pos"][1] + extra["raise"], 4), c["pos"][2])
        c["hide"] = sorted(set(c.get("hide", []) + hide_always + extra.get("hide", [])))
        view_specs[v] = c
    bindings = [{"subject": f"/World/Character/{p}",
                 "article": {"name": a.name, "path": str(a.path), "master": a.master}}
                | {port: str(path) for port, path in jobmod.maps_for(p, a, meshmaps).items()}
                for p, a in arts.items()]
    spec = {"keep": [f"/World/Character/{p}" for p in B.PARTS], "build": None, "views": view_specs,
            "bindings": bindings, "on": parts_of}
    context = [jobmod.CHARACTER_SCENE]
    for p, a in arts.items():
        if a.name != art.name:
            context += [a.path, *a.textures.values()]
        context += list(jobmod.maps_for(p, a, meshmaps).values())
    return spec, context, arts


def make(name: str, rend: dict | None, force: bool, draft: bool) -> tuple[Path, str]:
    """One article's pictures. Returns its folder and what was done."""
    art = jobmod.Article.read(find(name))
    subject = S.subject_for(art.master, art.path)
    if subject == "character":
        spec, context, cast = character_spec(art)
    else:
        spec, context, cast = S.SUBJECTS[subject], [jobmod.SCENE], None
    folder = (S.OUT_ROOT / "_draft" if draft else S.OUT_ROOT) / art.name
    views = list(spec["views"])
    why = []
    if not draft:
        want = S.record(art.path, art.textures.values(), rend, views, subject, look(), spec, context)
        why = S.stale(folder, want)
        if not why and not force:
            return folder, "fresh"
    work = folder / "_job"
    work.mkdir(parents=True, exist_ok=True)
    (folder / "record.json").unlink(missing_ok=True)   # no record while the pictures are in doubt
    for old in folder.glob("*.png"):                     # a view the subject no longer has must not linger
        old.unlink()
    if cast:
        scene = jobmod.write_character_scene(cast, work / "scene.usda")
    else:
        scene = jobmod.write_setting_scene(art, {"id": "defaults", "set": {}}, work / "scene.usda")
    tj = {"article": {"name": art.name, "path": str(art.path), "master": art.master},
          "meters_per_tile": art.meters_per_tile, "subject": subject,
          "scene": str(scene), "keep": spec["keep"], "build": spec["build"], "lift": spec.get("lift", 0.0),
          "exposure": spec.get("exposure", 0.0), "bindings": spec.get("bindings"),
          "views": spec["views"], "look": look(),
          "samples": 32 if draft else S.SAMPLES, "seed": S.SEED, "size": 384 if draft else S.SIZE,
          "out_dir": str(folder)}
    jp = work / "thumb_job.json"
    jp.write_text(json.dumps(tj, indent=2) + "\n", encoding="utf-8")
    t = time.perf_counter()
    run_blender(BLENDER_SIDE, jp, work / "blender.log")
    took = time.perf_counter() - t
    got = json.loads((folder / "render.json").read_text(encoding="utf-8"))
    if draft:
        return folder, f"draft in {took:.0f} s ({got['device']})"
    if got["device"] != rend["device"] or got["blender"] != rend["blender"]:
        raise SystemExit(f"{art.name}: rendered on {got['device']} / {got['blender']}, but the probe "
                         f"said {rend['device']} / {rend['blender']}; no record written")
    rec = S.record(art.path, art.textures.values(), rend, views, subject, look(), spec, context, got["seconds"])
    (folder / "record.json").write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    per = ", ".join(f"{v} {s:.1f} s" for v, s in got["seconds"].items())
    return folder, f"made ({'forced' if force and not why else '; '.join(why)}): {per}; Blender {took:.0f} s in all"


# ------------------------------------------------------------------ the contact sheet

def _font(size: int):
    for f in ("/usr/share/fonts/google-noto/NotoSans-Regular.ttf", "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        if Path(f).is_file():
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def sheet(folders: list[Path], name: str) -> Path:
    """One row per article: its rig pictures (wide over close) at half size, then each view at full size."""
    rows = []
    for f in folders:
        views = [p for p in sorted(f.glob("*.png"))]
        rec = json.loads((f / "record.json").read_text()) if (f / "record.json").is_file() else {}
        order = rec.get("views") or [p.stem for p in views]
        order = [v for v in S.VIEW_ORDER if v in order] + [v for v in order if v not in S.VIEW_ORDER]
        rows.append((f, [f / f"{v}.png" for v in order], rec))
    big = max((Image.open(p).size[0] for _, ps, _ in rows for p in ps if p.is_file()), default=S.SIZE)
    half, head = big // 2, 70
    width = half + big * max(len(ps) for _, ps, _ in rows) + 20
    out = Image.new("RGB", (width, len(rows) * (big + head) + 20), (30, 30, 30))
    d = ImageDraw.Draw(out)
    f_big, f_small = _font(30), _font(20)
    for i, (f, ps, rec) in enumerate(rows):
        y = 10 + i * (big + head)
        d.text((10, y + 4), f.name, fill=(235, 235, 235), font=f_big)
        sec = rec.get("seconds", {})
        rend = rec.get("renderer", {})
        meta = (f"scene v{rec.get('scene_version', '?')} · Blender {rend.get('blender', '?')} Cycles "
                f"{rend.get('device', '?')} · {rec.get('samples', '?')} samples · "
                + " · ".join(f"{v} {s:.0f} s" for v, s in sec.items())) if rec else "draft"
        d.text((10, y + 40), meta, fill=(170, 170, 170), font=f_small)
        y += head
        rig = PARITY / f.name / "blender"
        for k, (pic, lab) in enumerate(((rig / "defaults.png", "rig: wide"), (rig / "defaults__close.png", "rig: close"))):
            if pic.is_file():
                out.paste(Image.open(pic).convert("RGB").resize((half, half), Image.LANCZOS), (10, y + k * half))
                d.text((16, y + k * half + 6), lab, fill=(255, 255, 0), font=f_small)
            else:
                d.text((16, y + k * half + 6), f"{lab}: none", fill=(200, 120, 120), font=f_small)
        for j, p in enumerate(ps):
            x = 10 + half + 10 + j * big
            if p.is_file():
                im = Image.open(p).convert("RGB")
                if im.size[0] != big:
                    im = im.resize((big, big), Image.LANCZOS)
                out.paste(im, (x, y))
            d.text((x + 8, y + 6), f"Cycles: {p.stem}", fill=(255, 255, 0), font=f_small)
    dst = S.OUT_ROOT / "_sheets" / f"{name}.png"
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst)
    return dst


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Make thumbnails: showcase pictures in Cycles, and their record.")
    ap.add_argument("articles", nargs="+", help="article stems (or paths to .mtlx)")
    ap.add_argument("--sheet", metavar="NAME", help="write library/thumbnails/_sheets/NAME.png")
    ap.add_argument("--force", action="store_true", help="make them even when fresh")
    ap.add_argument("--draft", action="store_true", help="384 px, 32 samples, no record: for tuning the look")
    args = ap.parse_args(argv)
    rend = None if args.draft else renderer()
    if rend:
        print(f"renderer: Blender {rend['blender']}, {rend['engine']}, {rend['device']}")
    folders = []
    for a in args.articles:
        folder, what = make(a, rend, args.force, args.draft)
        print(f"{folder.name}: {what}")
        folders.append(folder)
    if args.sheet:
        print(f"sheet: {sheet(folders, args.sheet)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
