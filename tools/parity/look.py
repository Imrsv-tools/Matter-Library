#!/usr/bin/env python3
"""The look view: a character's skin in the library's Unreal runtime, lit to show its surface.

    uv run tools/parity/look.py <skin> [--today <git rev>] [--also <skin> ...] [--width 1024] [--out <dir>]

Phase22 (RD-P22-11). The rig's matched light has no shadows, so its sheet cannot show whether a
skin reads as plastic; it stays the tool-agreement check. This renders the rig's character, cast
as ``rig.py --character`` casts it, in the runtime's LOOK VIEW (JOB_FORMAT.md §The look view): a
key light from the character's left that casts shadows, a fill, a rim, a dimmed dome, contact
shadows and screen-space AO, at a fixed exposure. Four cameras:

* ``face``: the face from the front;
* ``face34``: the face at three quarters, from the key's side;
* ``hand``: the back of the left hand;
* ``ear``: the left ear, lit from behind by the rim alone (the key and the fill off; the hair hidden).

``--today <rev>`` also renders the same cast with each article as it stood at ``<rev>`` (from git),
and the sheet sets today's beside the new. Each of today's pictures is drawn as it stood at
``<rev>`` too: a picture changed since is taken from the local LFS store (Phase23 23.2; before, it
was drawn as it is now). Without it, one column: the baseline.

``--reference <picture>`` (Phase23 23.1, RD-P23-1) draws a colour picture from outside the tree
on a Fitzpatrick skin and its lips, in three more columns: as made (constant 1), held to the
skin's tone at the picture's own size, and held to it at the library's 2048 atlas (the
contributor's calibration, ``gen_skin_maps.calibrate``). It writes only under ``<out>``.

Writes ``<out>/<setting><view>.png`` and ``<out>/look_sheet.png``. Default ``<out>``:
``library/parity/Look__<skin>[__vs_<rev>]``. It needs a runtime that reads job format 4 (built at
Phase22 22.1 or later): ``MATTER_UNREAL_RUNTIME`` (a local package), ``MATTER_UNREAL_EDITOR``, or
the pinned build (``unreal/RUNTIME.json``, ``unreal-runtime-v7`` or later).
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE / "drivers"))
sys.path.insert(0, str(HERE / "scene"))
import build_character as bc  # noqa: E402
import build_scene  # noqa: E402
import job as jobmod  # noqa: E402
import rig  # noqa: E402
import unreal as drv  # noqa: E402

SUPERSAMPLE = 2          # the look view's own: 4x at 1024 px is 200 MB of float per picture

# The lights, as the way each light TRAVELS, in the rig's space (Y up; the character faces +Z and
# its left hand is at +X). Intensities are multiples of the rig's calibrated sun and dome.
KEY_FROM = (0.75, 0.50, 0.45)      # the character's left, in front, above: a highlight across the
                                   # forehead and the left cheek, the right side in shadow
FILL_FROM = (-0.60, 0.15, 0.80)    # the right, in front, low
RIM_FROM = (0.45, 0.30, -0.84)     # behind, on the left: the ear's back and the head's edge
FILL, RIM, DOME = 0.20, 0.90, 0.30
CONTACT_SHADOW = 0.02              # a fraction of the screen (Unreal's contact shadow length)
AMBIENT_OCCLUSION = 0.5

VIEWS = {"face": "face, front", "face34": "face, three quarters", "hand": "back of the left hand",
         "ear": "left ear, lit from behind"}
# the ear's setting; the rim casts shadows so Unreal can draw light through the ear (22.3)
BACKLIT = {"sun_scale": 0.0, "fill_scale": 0.0, "rim_scale": 1.6, "rim_shadows": True}


def _travel(source) -> list[float]:
    s = np.asarray(source, float)
    return list(drv.to_ue(-s / np.linalg.norm(s)))


def look_lights() -> dict:
    """The job's ``look`` field (JOB_FORMAT.md §The look view)."""
    sun, sky = drv.lights()
    key = sun["intensity"]
    return {"key": {"direction": _travel(KEY_FROM), "intensity": key, "angle": build_scene.SUN_ANGLE,
                    "contact_shadow": CONTACT_SHADOW},
            "fill": {"direction": _travel(FILL_FROM), "intensity": key * FILL, "angle": 5.0},
            "rim": {"direction": _travel(RIM_FROM), "intensity": key * RIM, "angle": 1.0},
            "sky_intensity": sky["intensity"] * DOME,
            "ambient_occlusion": AMBIENT_OCCLUSION, "virtual_shadows": True}


def look_views(parts: dict) -> list[dict]:
    """The four cameras, framed from the body's bounds as ``build_character.cameras`` frames its own."""
    half = bc.CAM_APERTURE / 2 / bc.CAM_FOCAL           # half the frame's width per metre away
    pts = parts["Body"]["points"]
    top = max(p[1] for p in pts)
    head = [p for p in pts if p[1] > top * 0.88]
    fz = max(p[2] for p in head)
    face = (0.0, float(np.median([p[1] for p in head])) - 0.02, fz - 0.08)
    xmax = max(p[0] for p in pts)
    hand = [p for p in pts if p[0] > xmax - 0.12]
    hc = tuple((min(p[k] for p in hand) + max(p[k] for p in hand)) / 2 for k in range(3))
    # the left ear: the head's +X edge in a band at the face's height (above it is the scalp)
    band = [p for p in head if abs(p[1] - face[1]) < 0.035]
    hx = max(p[0] for p in band)
    ear_pts = [p for p in band if p[0] > hx - 0.02]
    ear = tuple(float(np.mean([p[k] for p in ear_pts])) for k in range(3))

    def at(target, frame_m, direction):
        d = np.asarray(direction, float)
        pos = tuple(np.asarray(target) + d / np.linalg.norm(d) * (frame_m / 2 / half))
        return pos, bc._look_at(pos, target)

    always = [p.rsplit("/", 1)[1] for p in jobmod.CHARACTER_HIDE_ALWAYS]
    yaw = math.radians(35)
    cams = {"face": (at(face, 0.28, (0.0, 0.04, 1.0)), always),
            "face34": (at(face, 0.28, (math.sin(yaw), 0.04, math.cos(yaw))), always),
            "hand": (at(hc, 0.20, (0.15, 0.30, 1.0)), always),
            "ear": (at(ear, 0.10, (0.55, 0.05, 0.85)), always + ["Hair"])}
    return [drv.camera_view(pos, rot, f"__{v}", hide) for v, ((pos, rot), hide) in cams.items()]


def _relocated(art: jobmod.Article, text: str, out: Path) -> jobmod.Article:
    """``text`` (an article's .mtlx) written to ``out``, its pictures named by absolute path."""
    def absolute(m: re.Match) -> str:
        v = m.group(2)
        return m.group(1) + (str((art.path.parent / v).resolve()) if v else v) + m.group(3)
    text = re.sub(r'(type="filename" value=")([^"]*)(")', absolute, text)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return jobmod.Article.read(out)


def _picture_at(path: Path, rev: str, folder: Path) -> Path:
    """The picture at ``path`` as it stood at ``rev``: the working copy when it is unchanged, else
    the old one from the local LFS store, written under ``folder`` (Phase23 23.2: a re-made map would
    otherwise be drawn under the old article's constant)."""
    import hashlib  # noqa: PLC0415
    try:
        rel = path.resolve().relative_to(jobmod.REPO).as_posix()
    except ValueError:
        return path
    old = subprocess.run(["git", "-C", str(jobmod.REPO), "show", f"{rev}:{rel}"], capture_output=True)
    if old.returncode != 0:
        return path                                    # not in the tree at rev: as it is now
    blob = old.stdout
    if blob.startswith(b"version https://git-lfs"):
        oid = re.search(rb"oid sha256:([0-9a-f]{64})", blob).group(1).decode()
        if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == oid:
            return path
        blob = subprocess.run(["git", "-C", str(jobmod.REPO), "lfs", "smudge"], input=blob,
                              capture_output=True, check=True).stdout
    elif path.is_file() and path.read_bytes() == blob:
        return path
    out = folder / "_pictures" / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(blob)
    return out


def today_article(art: jobmod.Article, rev: str, folder: Path) -> jobmod.Article:
    """``art`` as it stood at ``rev``, each picture as it stood then (``_picture_at``)."""
    rel = art.path.resolve().relative_to(jobmod.REPO)
    text = subprocess.run(["git", "-C", str(jobmod.REPO), "show", f"{rev}:{rel.as_posix()}"],
                          capture_output=True, text=True, check=True).stdout

    def at_rev(m: re.Match) -> str:
        v = m.group(2)
        return m.group(1) + (str(_picture_at(art.path.parent / v, rev, folder)) if v else v) + m.group(3)
    text = re.sub(r'(type="filename" value=")([^"]*)(")', at_rev, text)
    return _relocated(art, text, folder / rel)


# ---------------------------------------------------------------- the reference column (Phase23) --
# RD-P23-1, RD-P23-10: a colour picture from OUTSIDE the tree (the platform's research reference)
# drawn on the skin article, so the bar is seen in this light on this shine. Everything it writes
# stays under the git-ignored ``library/parity/``; nothing here names the picture's path.

def _with_map(art: jobmod.Article, picture: Path, const, out: Path) -> jobmod.Article:
    """``art`` with its own ``base_color_map`` set to ``picture`` and ``base_color_const`` to ``const``."""
    text = art.path.read_text(encoding="utf-8")
    text, n_map = re.subn(r'(<input name="base_color_map" type="filename" value=")[^"]*(")',
                          lambda m: m.group(1) + str(picture.resolve()) + m.group(2), text)
    value = ", ".join(f"{float(v):.4f}" for v in const)
    text, n_const = re.subn(r'(<constant name="base_color_const" type="color3">\s*<input name="value" '
                            r'type="color3" value=")[^"]*(")',
                            lambda m: m.group(1) + value + m.group(2), text)
    if (n_map, n_const) != (1, 1):
        raise SystemExit(f"{art.name}: expected one base_color_map and one base_color_const "
                         f"(found {n_map} and {n_const}); it cannot carry a reference picture")
    return _relocated(art, text, out / f"{art.name}.mtlx")


def reference_casts(cast: dict, picture: Path, folder: Path) -> list[tuple[str, str, dict]]:
    """The reference columns for a Fitzpatrick skin's cast: (setting id, heading, cast).

    The skin and its lips share one map and one constant (RD-P21-2), so both take the picture.
    (b) the picture as made, constant 1; (c) held to the skin's tone, at the picture's own size,
    by ``gen_skin_maps.calibrate`` (the contributor's ``--picture`` step); (d) the picture box-
    filtered in linear light to the library's 2048 atlas, then the same step."""
    import numpy as np  # noqa: PLC0415
    sys.path.insert(0, str(jobmod.REPO / "tools" / "converters" / "fit"))
    import gen_skin_maps as gsm  # noqa: PLC0415

    skin = cast["Body"]
    variant = skin.name.split("_")[1]
    roman = variant.removeprefix("Fitzpatrick")
    if not variant.startswith("Fitzpatrick") or roman not in gsm.TONES:
        raise SystemExit(f"--reference needs a Fitzpatrick skin (got {skin.name})")
    swap = [p for p in ("Body", "Lips") if p in cast and "base_color_map" in cast[p].ports]

    im = Image.open(picture).convert("RGB")
    size = im.size[0]
    if im.size[0] != im.size[1] or size % gsm.N:
        raise SystemExit(f"the reference picture is {im.size[0]} x {im.size[1]}; it must be square, "
                         f"a multiple of {gsm.N}, on {gsm.MESH}'s atlas")
    f = size // gsm.N
    col = gsm._srgb_to_linear(np.asarray(im, dtype=np.float64) / 255.0)
    reg = gsm.regions()
    big = {k: np.repeat(np.repeat(v, f, 0), f, 1) for k, v in reg.items()}
    tone = gsm.tone_of(roman)
    avg = col[big["Body"]].mean(0)
    print(f"reference: {size}², skin average (linear) {np.round(avg, 3).tolist()}, "
          f"red/blue {avg[0] / avg[2]:.2f}; tone {roman} {np.round(tone, 4).tolist()}, "
          f"red/blue {tone[0] / tone[2]:.2f}")

    def column(sid, heading, pic, const):
        sub = folder / sid
        return sid, heading, cast | {p: _with_map(cast[p], pic, const, sub) for p in swap}

    out = [column("ref_asis", "(b) reference, as made", picture, (1.0, 1.0, 1.0))]
    for sid, heading, c, r in (("ref_held", f"(c) held to {roman}, {size} px", col, big),
                               ("ref_2048", f"(d) held to {roman}, {gsm.N} px",
                                col.reshape(gsm.N, f, gsm.N, f, 3).mean(axis=(1, 3)), reg)):
        srgb8, const, st = gsm.calibrate(c, tone, r, r["islands"])
        p = folder / sid / "basecolor.png"
        p.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(srgb8, "RGB").save(p)
        print(f"{sid}: " + json.dumps(st))
        out.append(column(sid, heading, p, const))
    return out


def materials(cast: dict, folder: Path) -> tuple[dict, list[dict]]:
    """The cast's materials in the Unreal job, and its meshes (from a rig job with no views)."""
    job = json.loads(jobmod.write_character_job(cast, folder, 512, 1).read_text(encoding="utf-8"))
    job["views"] = {}
    ujob = json.loads(drv.unreal_job(job, folder / "unreal").read_text(encoding="utf-8"))
    return next(s for s in ujob["settings"] if s["id"] == "defaults")["materials"], ujob["meshes"]


def linear(pfm: Path) -> np.ndarray:
    img = drv.read_pfm(pfm) / drv.EXPOSURE_K
    h, w, c = img.shape
    return img.reshape(h // SUPERSAMPLE, SUPERSAMPLE, w // SUPERSAMPLE, SUPERSAMPLE, c).mean(axis=(1, 3))


def sheet(out: Path, columns: list[tuple[str, str]], cell: int) -> Path:
    """Rows: the views; columns: (setting prefix, heading). The ear row uses the backlit settings."""
    font, pad, head = rig._font(22), 8, 40
    w = len(columns) * (cell + pad) + pad + 220
    h = head + len(VIEWS) * (cell + pad) + pad
    img = Image.new("RGB", (w, h), (24, 24, 24))
    d = ImageDraw.Draw(img)
    for c, (_, title) in enumerate(columns):
        d.text((220 + pad + c * (cell + pad), 10), title, fill=(235, 235, 235), font=font)
    for r, (view, label) in enumerate(VIEWS.items()):
        y = head + pad + r * (cell + pad)
        d.text((pad, y + cell // 2 - 12), label, fill=(200, 200, 200), font=rig._font(18))
        for c, (prefix, _) in enumerate(columns):
            sid = f"{prefix}__backlit" if view == "ear" else prefix
            pic = Image.open(out / f"{sid}__{view}.png").resize((cell, cell), Image.LANCZOS)
            img.paste(pic, (220 + pad + c * (cell + pad), y))
    p = out / "look_sheet.png"
    img.save(p)
    return p


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("skin", nargs="?", default=rig.CHARACTER_SKIN)
    ap.add_argument("--today", metavar="REV", help="also render the cast as it stood at this git revision")
    ap.add_argument("--also", action="append", default=[], metavar="SKIN",
                    help="another skin from the working tree, a further column (repeatable)")
    ap.add_argument("--reference", type=Path, metavar="PICTURE",
                    help="a colour picture on the skin's atlas, from outside the tree (Phase23 RD-P23-10): "
                         "three more columns, the picture as made, held to the skin's tone, and that at 2048")
    ap.add_argument("--width", type=int, default=1024)
    ap.add_argument("--cell", type=int, default=640, help="picture size on the sheet")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)

    art = jobmod.Article.read(jobmod.find_article(a.skin))
    cast = rig.character_cast(art)
    out = (a.out or rig.OUT_ROOT / (f"Look__{art.name}" + (f"__vs_{a.today}" if a.today else "")
                                    + ("__vs_reference" if a.reference else ""))).resolve()
    shutil.rmtree(out / "work", ignore_errors=True)
    work = out / "work"

    new_mats, meshes = materials(cast, work / "new")
    settings = [{"id": "new", "materials": new_mats}]
    columns = [("new", f"working tree: {art.name}")]
    if a.today:
        rev = subprocess.run(["git", "-C", str(jobmod.REPO), "rev-parse", "--short", a.today],
                             capture_output=True, text=True, check=True).stdout.strip()
        tcast = {p: today_article(x, rev, work / "today_articles") for p, x in cast.items()}
        today_mats, tmeshes = materials(tcast, work / "today")
        same = len(meshes) == len(tmeshes) and all(
            Path(m["file"]).read_bytes() == Path(t["file"]).read_bytes() for m, t in zip(meshes, tmeshes))
        if not same:
            raise SystemExit("today's cast builds different meshes from the new one (a part's st moved); "
                             "the two cannot share one launch")
        settings.insert(0, {"id": "today", "materials": today_mats})
        columns.insert(0, ("today", f"today ({rev})"))
    for i, other in enumerate(a.also, start=1):
        oart = jobmod.Article.read(jobmod.find_article(other))
        omats, omeshes = materials(rig.character_cast(oart), work / f"also{i}")
        if [Path(m["file"]).read_bytes() for m in omeshes] != [Path(m["file"]).read_bytes() for m in meshes]:
            raise SystemExit(f"{oart.name}'s cast builds different meshes; it cannot share the launch")
        settings.append({"id": f"also{i}", "materials": omats})
        columns.append((f"also{i}", f"working tree: {oart.name}"))
    if a.reference:
        columns[columns.index(("new", f"working tree: {art.name}"))] = ("new", f"(a) {art.name}")
        for sid, heading, rcast in reference_casts(cast, a.reference, work / "reference"):
            rmats, rmeshes = materials(rcast, work / sid)
            if [Path(m["file"]).read_bytes() for m in rmeshes] != [Path(m["file"]).read_bytes() for m in meshes]:
                raise SystemExit(f"{sid}'s cast builds different meshes; it cannot share the launch")
            settings.append({"id": sid, "materials": rmats})
            columns.append((sid, heading))
    settings +=[s | {"id": f"{s['id']}__backlit"} | BACKLIT for s in list(settings)]

    parts = bc.load_parts()
    views = look_views(parts)
    sun, sky = drv.lights()
    ujob = {"format": drv.LOOK_JOB_FORMAT, "width": a.width * SUPERSAMPLE, "out_dir": str(work / "raw"),
            "settle_frames": drv.SETTLE_FRAMES, "sun": sun, "sky": sky, "meshes": meshes,
            "settings": [drv.warmup(settings)] + settings, "views": views, "look": look_lights()}
    upath = work / "look_job.json"
    upath.write_text(json.dumps(ujob, indent=1) + "\n", encoding="utf-8")

    cmd = drv.find_runtime()          # the pinned unreal-runtime-v7 or later draws the look view
    if cmd is None:
        raise SystemExit("no Unreal runtime: set MATTER_UNREAL_RUNTIME to a package built at Phase22 22.1 "
                         "or later, or run on Linux, where the pinned build (v7) is downloaded")
    wanted = [(s["id"], v["suffix"]) for s in settings for v in views
              if (v["suffix"] == "__ear") == s["id"].endswith("__backlit")]
    drv.run_runtime(cmd, upath, work / "unreal.log", [work / "raw" / f"{i}{x}.pfm" for i, x in wanted])
    for i, x in wanted:
        Image.fromarray(drv.srgb8(linear(work / "raw" / f"{i}{x}.pfm"))).save(out / f"{i}{x}.png")
    for pfm in (work / "raw").glob("*.pfm"):
        pfm.unlink()                                  # ~50 MB each; the PNGs are the record
    p = sheet(out, columns, a.cell)
    print(f"look sheet {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
