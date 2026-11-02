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


# ------------------------------------------------------------------ the judge's views (Phase24) --
# RD-P24-4 (OVS-Q2): the face at a viewer's ~1 m and ~40 cm through the rig's one lens (50 mm on a
# 36 mm aperture), from the front, at three quarters and in profile (from the key's side); and the
# eye, the lips and the cheek with the nose, each the 40 cm view MAGNIFIED (the same camera
# position, a narrower view: what a crop of that view would show, at full resolution). Fixed at
# click 1 and never changed after.
JUDGE_VIEWS = {"front1m": "face, front, 1 m", "q1m": "face, three quarters, 1 m", "side1m": "face, profile, 1 m",
               "front40": "face, front, 40 cm", "q40": "face, three quarters, 40 cm",
               "side40": "face, profile, 40 cm", "eye": "left eye, 40 cm, magnified",
               "lips": "lips, 40 cm, magnified", "cheek": "left cheek and nose, 40 cm, magnified"}
CLOSE_FRAME = {"eye": 0.07, "lips": 0.07, "cheek": 0.09}       # metres across a magnified view


def judge_views(parts: dict) -> list[dict]:
    """The judge's nine cameras (``JUDGE_VIEWS``), placed from the rig's own parts."""
    pts = parts["Body"]["points"]
    top = max(p[1] for p in pts)
    head = [p for p in pts if p[1] > top * 0.88]
    face = (0.0, float(np.median([p[1] for p in head])) - 0.02, max(p[2] for p in head) - 0.08)
    mouth = tuple(np.mean(parts["Lips"]["points"], axis=0))
    iris = np.asarray(parts["Iris"]["points"])
    eye = tuple(iris[iris[:, 0] > 0].mean(0))                    # the character's left: +X, the key's side
    near = [p for p in head if abs(p[1] - (eye[1] + mouth[1]) / 2) < 0.01 and 0.015 < p[0] < 0.05]
    cheek = (0.03, (eye[1] + mouth[1]) / 2, max(p[2] for p in near) - 0.005)
    always = [p.rsplit("/", 1)[1] for p in jobmod.CHARACTER_HIDE_ALWAYS]
    fov = math.degrees(2 * math.atan(bc.CAM_APERTURE / 2 / bc.CAM_FOCAL))
    q, s = math.radians(35), math.radians(90)
    dirs = {"front": (0.0, 0.04, 1.0), "q": (math.sin(q), 0.04, math.cos(q)), "side": (math.sin(s), 0.04, math.cos(s))}
    cams = []
    for name, metres in (("1m", 1.0), ("40", 0.4)):
        for d, v in dirs.items():
            cams.append((f"{d}{name}", face, v, metres, fov))
    for v, target, d in (("eye", eye, (0.25, 0.05, 1.0)), ("lips", mouth, (0.0, 0.0, 1.0)),
                         ("cheek", cheek, (0.6, 0.05, 0.8))):
        cams.append((v, target, d, 0.4, math.degrees(2 * math.atan(CLOSE_FRAME[v] / 2 / 0.4))))
    out = []
    for v, target, d, metres, f in cams:
        d = np.asarray(d, float)
        pos = tuple(np.asarray(target) + d / np.linalg.norm(d) * metres)
        view = drv.camera_view(pos, bc._look_at(pos, target), f"__{v}", always)
        view["fov"] = f
        out.append(view)
    return out


# ------------------------------------------------------------------ the body's views (Phase27) ---
# F-P27-5: the judge for the body's skin, on the bare cast (``--bare``). The whole body from the front,
# the back and in profile (from the key's side) at ~2.5 m; the trunk front and back at ~1 m; and at
# 40 cm the neck and shoulder (the head's seam), the left wrist, the left ankle and the back of the
# left hand. Through the rig's one lens; placed from the rig's own parts, as ``judge_views`` is.
BODY_VIEWS = {"bfront": "whole body, front, 2.5 m", "bback": "whole body, back, 2.5 m",
              "bside": "whole body, profile, 2.5 m", "tfront": "trunk, front, 1 m", "tback": "trunk, back, 1 m",
              "neck": "neck and left shoulder, 40 cm", "wrist": "left wrist, 40 cm",
              "ankle": "left ankle, 40 cm", "bhand": "back of the left hand, 40 cm"}
GARMENT_PARTS = {n for m in bc.MESHES.values() if m.get("delete")
                 for n in [s for s, _ in m.get("split", [])] + [m["rest"]]}


def body_views(parts: dict) -> list[dict]:
    """The body's nine cameras (``BODY_VIEWS``), placed from the bare cast's parts."""
    pts = np.asarray(parts["Body"]["points"], float)
    top = pts[:, 1].max()
    zc = float(np.median(pts[:, 2]))
    xmax = pts[:, 0].max()
    hand = pts[pts[:, 0] > xmax - 0.12]
    hc = (hand.min(0) + hand.max(0)) / 2
    arm = pts[(pts[:, 0] > xmax - 0.16) & (pts[:, 0] < xmax - 0.12)]          # just inside the hand
    wrist = arm.mean(0)
    ank = pts[(pts[:, 1] > 0.07) & (pts[:, 1] < 0.11) & (pts[:, 0] > 0)]       # the left leg above the foot
    ankle = ank.mean(0)
    neck_y = top * 0.81
    sh = pts[(np.abs(pts[:, 1] - neck_y) < 0.02) & (pts[:, 0] > 0)]
    neck = (float(np.median(sh[:, 0])) * 0.6, neck_y - 0.02, zc)
    always = [p.rsplit("/", 1)[1] for p in jobmod.CHARACTER_HIDE_ALWAYS]
    fov = math.degrees(2 * math.atan(bc.CAM_APERTURE / 2 / bc.CAM_FOCAL))
    q = math.radians(35)
    cams = [("bfront", (0.0, top / 2, zc), (0.0, 0.0, 1.0), 2.5),
            ("bback", (0.0, top / 2, zc), (0.0, 0.0, -1.0), 2.5),
            ("bside", (0.0, top / 2, zc), (1.0, 0.0, 0.0), 2.5),
            ("tfront", (0.0, top * 0.64, zc), (0.0, 0.05, 1.0), 1.0),
            ("tback", (0.0, top * 0.64, zc), (0.0, 0.05, -1.0), 1.0),
            ("neck", neck, (math.sin(q), 0.15, math.cos(q)), 0.4),
            ("wrist", tuple(wrist), (0.3, 0.3, 1.0), 0.4),
            ("ankle", tuple(ankle), (0.5, 0.25, 1.0), 0.4),
            ("bhand", tuple(hc), (0.15, 0.30, 1.0), 0.4)]
    out = []
    for v, target, d, metres in cams:
        d = np.asarray(d, float)
        pos = tuple(np.asarray(target, float) + d / np.linalg.norm(d) * metres)
        view = drv.camera_view(pos, bc._look_at(pos, target), f"__{v}", always)
        view["fov"] = fov
        out.append(view)
    return out


def bar_article(art: jobmod.Article, bar: Path, out: Path) -> jobmod.Article:
    """``art`` wearing the bar's pictures (``bar_maps.py``): its colour and constant, its specular
    as the cavity map; the article's other shine maps as they are (RD-P24-5)."""
    rec = json.loads((bar / "bar.json").read_text(encoding="utf-8"))
    a = _with_map(art, bar / "basecolor.png", rec["base_color_const"], out / "_colour")
    text, n = re.subn(r'(<input name="cavity_map" type="filename" value=")[^"]*(")',
                      lambda m: m.group(1) + str((bar / "cavity.png").resolve()) + m.group(2),
                      a.path.read_text(encoding="utf-8"))
    if n != 1:
        raise SystemExit(f"{art.name}: no cavity_map to carry the bar's specular")
    return _relocated(a, text, out / f"{art.name}.mtlx")


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


BARE = False     # Phase27 ``--bare``: every cast in this launch is built unclothed (set by main)


def materials(cast: dict, folder: Path) -> tuple[dict, list[dict]]:
    """The cast's materials in the Unreal job, and its meshes (from a rig job with no views)."""
    if BARE:
        cast = {p: x for p, x in cast.items() if p not in GARMENT_PARTS}
    job = json.loads(jobmod.write_character_job(cast, folder, 512, 1).read_text(encoding="utf-8"))
    job["views"] = {}
    job["bare"] = BARE
    ujob = json.loads(drv.unreal_job(job, folder / "unreal").read_text(encoding="utf-8"))
    return next(s for s in ujob["settings"] if s["id"] == "defaults")["materials"], ujob["meshes"]


def linear(pfm: Path) -> np.ndarray:
    img = drv.read_pfm(pfm) / drv.EXPOSURE_K
    h, w, c = img.shape
    return img.reshape(h // SUPERSAMPLE, SUPERSAMPLE, w // SUPERSAMPLE, SUPERSAMPLE, c).mean(axis=(1, 3))


def sheet(out: Path, columns: list[tuple[str, str]], cell: int, views: dict = VIEWS) -> Path:
    """Rows: the views; columns: (setting prefix, heading). The ear row uses the backlit settings."""
    font, pad, head = rig._font(22), 8, 40
    w = len(columns) * (cell + pad) + pad + 220
    h = head + len(views) * (cell + pad) + pad
    img = Image.new("RGB", (w, h), (24, 24, 24))
    d = ImageDraw.Draw(img)
    for c, (_, title) in enumerate(columns):
        d.text((220 + pad + c * (cell + pad), 10), title, fill=(235, 235, 235), font=font)
    for r, (view, label) in enumerate(views.items()):
        y = head + pad + r * (cell + pad)
        d.text((pad, y + cell // 2 - 12), label, fill=(200, 200, 200), font=rig._font(18))
        for c, (prefix, _) in enumerate(columns):
            sid = f"{prefix}__backlit" if view == "ear" else prefix
            pic = Image.open(out / f"{sid}__{view}.png").resize((cell, cell), Image.LANCZOS)
            img.paste(pic, (220 + pad + c * (cell + pad), y))
    p = out / "look_sheet.png"
    img.save(p)
    return p


# ---------------------------------------------------------------- the working shine (Phase25) --
# F-P25-13 (the lead: "The skin looks better for this step (we can add texture and stuff later)"):
# flat relief (the article's normal map and its tiled pore normal both a flat normal) and matte
# (``roughness_bias`` 0.25); the cavity map kept. Applied alike to C and every candidate, so the
# click compares colour only; the bar keeps its own shine.
SHINES = ("served", "neutral")


def neutral_article(art: jobmod.Article, folder: Path) -> jobmod.Article:
    """``art`` with the working shine: flat relief and ``roughness_bias`` 0.25 (probe 1's settings)."""
    flat = folder / "flat_normal.png"
    if not flat.is_file():
        folder.mkdir(parents=True, exist_ok=True)
        Image.fromarray(np.full((8, 8, 3), (128, 128, 255), np.uint8)).save(flat)
    text = art.path.read_text(encoding="utf-8")
    for pat, val in ((r'(<input name="normal_map" type="filename" value=")[^"]*(")', str(flat)),
                     (r'(<image name="normal_tex" type="vector3">\s*<input name="file" type="filename" value=")[^"]*(")',
                      str(flat)),
                     (r'(<input name="roughness_bias" type="float" value=")[^"]*(")', "0.25")):
        text, n = re.subn(pat, lambda m: m.group(1) + val + m.group(2), text)
        if n != 1:
            raise SystemExit(f"{art.name}: --shine neutral expected one match of {pat!r}, found {n}")
    return _relocated(art, text, folder / art.name / f"{art.name}.mtlx")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("skin", nargs="?", default=rig.CHARACTER_SKIN)
    ap.add_argument("--today", metavar="REV", help="also render the cast as it stood at this git revision")
    ap.add_argument("--also", action="append", default=[], metavar="SKIN",
                    help="another skin from the working tree, a further column (repeatable)")
    ap.add_argument("--reference", type=Path, metavar="PICTURE",
                    help="a colour picture on the skin's atlas, from outside the tree (Phase23 RD-P23-10): "
                         "three more columns, the picture as made, held to the skin's tone, and that at 2048")
    ap.add_argument("--bar", type=Path, metavar="DIR",
                    help="Phase24 column A: the scanned bar's pictures made by bar_maps.py (git-ignored), "
                         "worn by the skin article on the body AND the lips (RD-P24-3, RD-P24-5)")
    ap.add_argument("--candidate", action="append", default=[], metavar="LABEL=PICTURE",
                    help="Phase25 column D: a colour picture from outside the tree (linear albedo, sRGB-encoded, "
                         "on the skin's atlas) drawn as made, constant 1, on the skin's body and lips, with the "
                         "skin's own shine maps; one column each (repeatable)")
    ap.add_argument("--judge", action="store_true",
                    help="Phase24's nine fixed views (RD-P24-4) in place of the four look views")
    ap.add_argument("--shine", choices=SHINES, default="served",
                    help="Phase25's working shine on the skin (C) and every candidate (D): 'neutral' is flat "
                         "relief and matte (F-P25-13); the bar keeps its own. Default: as served")
    ap.add_argument("--makeup", metavar="COMPOSITION",
                    help="Phase26: a makeup composition (a piece list, JSON) merged by the reference merge and "
                         "worn on the skin (and its lips with --lips-skin); needs a runtime reading job format 5")
    ap.add_argument("--lips-skin", action="store_true",
                    help="Phase26: the lips wear the skin, as the platform's base character's do")
    ap.add_argument("--bare", action="store_true",
                    help="Phase27: the character unclothed (the suit and shoes and the body faces they delete "
                         "left out), for judging the body's skin; never the default (RD-P27-4)")
    ap.add_argument("--body", action="store_true",
                    help="Phase27: the body's nine views (BODY_VIEWS) in place of the four look views; with --bare")
    ap.add_argument("--width", type=int, default=1024)
    ap.add_argument("--cell", type=int, default=640, help="picture size on the sheet")
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    if a.body and (a.judge or not a.bare):
        raise SystemExit("--body is the bare cast's views: give --bare, and not --judge")
    global BARE
    BARE = a.bare

    art = jobmod.Article.read(jobmod.find_article(a.skin))
    cast = rig.character_cast(art)
    out = (a.out or rig.OUT_ROOT / (f"Look__{art.name}" + (f"__vs_{a.today}" if a.today else "")
                                    + ("__vs_reference" if a.reference else "")
                                    + ("__makeup" if a.makeup else "") + ("__lipsskin" if a.lips_skin else ""))).resolve()
    cast = rig.makeup_cast(cast, a.makeup, a.lips_skin, out)
    shutil.rmtree(out / "work", ignore_errors=True)
    work = out / "work"

    swap = [p for p in ("Body", "Lips") if p in cast and cast[p].name == art.name]
    shine = (lambda x, f: neutral_article(x, f / "_neutral")) if a.shine == "neutral" else (lambda x, f: x)
    new_mats, meshes = materials(cast | {p: shine(cast[p], work / "new_shine") for p in swap}, work / "new")
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
        omats, omeshes = materials(rig.makeup_cast(rig.character_cast(oart), None, a.lips_skin, out),
                                   work / f"also{i}")      # the same makeup (job.MAKEUP) and lips
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
    for spec in a.candidate:
        label, sep, pic = spec.partition("=")
        if not sep or not Path(pic).is_file():
            raise SystemExit(f"--candidate {spec!r}: give LABEL=PICTURE, an existing picture")
        sid = "cand_" + re.sub(r"[^A-Za-z0-9]+", "_", label)
        ccast = cast | {p: shine(_with_map(cast[p], Path(pic), (1.0, 1.0, 1.0), work / sid), work / sid) for p in swap}
        cmats, cmeshes = materials(ccast, work / f"{sid}_cast")
        if [Path(m["file"]).read_bytes() for m in cmeshes] != [Path(m["file"]).read_bytes() for m in meshes]:
            raise SystemExit(f"{label}'s cast builds different meshes; it cannot share the launch")
        settings.append({"id": sid, "materials": cmats})
        columns.append((sid, f"D: {label}"))
    if a.bar:
        bart = bar_article(art, a.bar.resolve(), work / "bar")
        bmats, bmeshes = materials(cast | {"Body": bart, "Lips": bart}, work / "bar_cast")
        if [Path(m["file"]).read_bytes() for m in bmeshes] != [Path(m["file"]).read_bytes() for m in meshes]:
            raise SystemExit("the bar's cast builds different meshes; it cannot share the launch")
        settings.insert(0, {"id": "bar", "materials": bmats})
        columns.insert(0, ("bar", "A: the scanned bar"))
        columns[columns.index(("new", f"working tree: {art.name}"))] = ("new", f"{'C' if a.candidate else 'B'}: {art.name}")
    parts = bc.load_parts(bare=a.bare)
    views = judge_views(parts) if a.judge else body_views(parts) if a.body else look_views(parts)
    labels = JUDGE_VIEWS if a.judge else BODY_VIEWS if a.body else VIEWS
    if not (a.judge or a.body):
        settings += [s | {"id": f"{s['id']}__backlit"} | BACKLIT for s in list(settings)]
    sun, sky = drv.lights()
    fmt = drv.MAKEUP_JOB_FORMAT if a.makeup else drv.LOOK_JOB_FORMAT   # Phase26: an older runtime refuses it
    ujob = {"format": fmt, "width": a.width * SUPERSAMPLE, "out_dir": str(work / "raw"),
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
    p = sheet(out, columns, a.cell, labels)
    print(f"look sheet {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
