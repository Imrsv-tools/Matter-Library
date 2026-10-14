"""The showcase scene's numbers, the subjects, the views, and the record (Phase17).

No ``bpy`` here: the tool (``make_thumbnails.py``) and its units import this, and the Blender
side (``showcase_blender.py``) reads the same numbers from the job the tool writes.

A thumbnail is a SHOWCASE render, not a diagnostic: full lighting (an HDRI for fill and
reflections, a key light, shadows and bounce light), a seamless backdrop, a tone curve made for
showing materials (Khronos PBR Neutral) at a fixed exposure, fixed samples and seed. The rig's
matched lighting (``tools/parity/drivers/blender_render.py``) is the opposite of every one of
these, on purpose, and is left as it is (F-P17-9).

**``SCENE_VERSION`` is the look.** Bump it whenever a number below changes what a picture shows;
every picture made at another version is then stale (the record, below).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
MASTERS = REPO / "blender" / "masters"
OUT_ROOT = REPO / "library" / "thumbnails"

SCENE_VERSION = 1

# ------------------------------------------------------------------ the look (RD-P17-2)

HDRI = REPO / "MatterLibrary" / "hdris" / "KloofendalOvercast_PureSky_v01.hdr"
HDRI_STRENGTH = 0.22
HDRI_ROTATION = 0.0               # degrees about the up axis
# the key: a soft area light, front left and above, for shape and one highlight
KEY_POS = (-1.25, 1.55, 1.35)     # metres, Y up (the rig's space)
KEY_AIM = (0.0, 0.15, 0.0)
KEY_SIZE = 0.8                    # metres, square
KEY_POWER = 110.0                 # watts (Blender's area light)
# the rim: a soft light behind and above, for edges against the backdrop, and something bright for a
# mirror's top face to reflect (without it a polished cube's top reflects the grey wall behind it and
# vanishes into the backdrop, 17.1)
RIM_POS = (0.25, 0.95, -0.90)
RIM_AIM = (0.0, 0.25, 0.0)
RIM_SIZE = 1.0
RIM_POWER = 10.0
RIM_SPREAD = 40.0                 # degrees: a narrow beam, so it lights the subjects and not the wall
# the seamless backdrop: a floor that sweeps up into a back wall, mid-grey
BACKDROP_ALBEDO = 0.18            # linear
BACKDROP_ROUGHNESS = 0.7
BACKDROP_FLOOR_FRONT = 2.5        # z of the floor's front edge
BACKDROP_CURVE_Z = -0.55          # z where the floor starts to curve up
BACKDROP_RADIUS = 0.6
BACKDROP_TOP = 3.0
BACKDROP_WIDTH = 6.0
VIEW_TRANSFORM = "Khronos PBR Neutral"
EXPOSURE = 0.0
SAMPLES = 256
SEED = 17
SIZE = 1024                       # px, square: the master PNG (RD-P17-3)

# ------------------------------------------------------------------ views and subjects

# A camera: position, (pitch, yaw) in degrees, focal length in mm, on a 36 mm square aperture.
CAMERAS = {
    # both objects on the backdrop
    "card": {"pos": (0.0, 0.46, 1.62), "rot": (-10.6, 0.0), "focal": 50.0},
    # the cube's front face and top edge, where grain and wear read (the rig's close-up framing)
    "close": {"pos": (0.10, 0.34, 0.58), "rot": (-20.2, -12.5), "focal": 50.0},
}

# What each subject keeps of the rig's test scene, and which views it is pictured from.
# 17.1 builds the first; 17.2 adds the rest (Brief §The subjects).
SUBJECTS = {
    "sphere_cube": {"keep": ["/World/Subjects/Sphere", "/World/Subjects/Cube"],
                    "views": ["card", "close"]},
}


def subject_for(master: str, path: Path) -> str:
    """The subject an article is pictured on, from its master and class (17.2 widens this)."""
    return "sphere_cube"


# ------------------------------------------------------------------ the record (F-MP-10)

def _sha(paths) -> str:
    h = hashlib.sha256()
    for p in sorted(Path(p) for p in paths):
        h.update(p.name.encode())
        h.update(b"\0")
        h.update(p.read_bytes())
    return h.hexdigest()


def article_hash(mtlx: Path, textures) -> str:
    """The article: its .mtlx and every texture it names."""
    return _sha([mtlx, *textures])


def masters_hash() -> str:
    """The Blender masters the article is built on (``blender/masters/*.py``)."""
    return _sha(MASTERS.glob("*.py"))


def scene_hash(look: dict) -> str:
    """The scene as it is drawn: the look the job carries, the cameras, the subjects and the Blender
    side. A number tuned without a ``SCENE_VERSION`` bump still makes every picture stale."""
    h = hashlib.sha256(json.dumps({"look": look, "cameras": CAMERAS, "subjects": SUBJECTS},
                                  sort_keys=True).encode())
    h.update((HERE / "showcase_blender.py").read_bytes())
    return h.hexdigest()


def record(mtlx: Path, textures, renderer: dict, views: list[str], subject: str, look: dict,
           seconds: dict | None = None) -> dict:
    """What a picture was made from. ``seconds`` (GPU time per view) is a measurement, not an
    input, so it is written and never compared."""
    r = {"article": mtlx.stem, "article_sha256": article_hash(mtlx, textures),
         "masters_sha256": masters_hash(), "renderer": renderer,
         "scene_version": SCENE_VERSION, "scene_sha256": scene_hash(look),
         "samples": SAMPLES, "size": SIZE,
         "subject": subject, "views": sorted(views)}
    if seconds is not None:
        r["seconds"] = seconds
    return r


INPUTS = ("article_sha256", "masters_sha256", "renderer", "scene_version", "scene_sha256", "samples", "size",
          "subject", "views")


def stale(folder: Path, want: dict) -> list[str]:
    """Why ``folder``'s pictures must be re-made: each input that differs from ``want``, or that
    a picture or the record is missing. Empty: fresh, and nothing is made."""
    rec = folder / "record.json"
    if not rec.is_file():
        return ["no record"]
    have = json.loads(rec.read_text(encoding="utf-8"))
    why = [k for k in INPUTS if have.get(k) != want.get(k)]
    why += [f"no {v}.png" for v in want["views"] if not (folder / f"{v}.png").is_file()]
    return why
