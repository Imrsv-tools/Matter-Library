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

# A camera: position, and either (pitch, yaw) in degrees (``rot``, USD rotateXYZ order) or a point it
# looks at (``aim``); focal length in mm, on a 36 mm square aperture. A view may be ``dark``: the
# HDRI, the key and the rim off, so an emitter is seen by its own light (an Emissive article).
SPHERE_CUBE_CARD = {"pos": (0.0, 0.46, 1.62), "rot": (-10.6, 0.0), "focal": 50.0}
SPHERE_CUBE_CLOSE = {"pos": (0.10, 0.34, 0.58), "rot": (-20.2, -12.5), "focal": 50.0}

# Each subject: the rig prims it keeps (``keep``), the geometry the Blender side builds for it
# (``build``, sizes in metres), and its views. ``lift`` raises the kept prims (the rig's slab has
# its top at y = 0, which is the backdrop's floor). The Brief's table (§The subjects), 17.2.
SUBJECTS = {
    # metal, plastic, polymer, composite, ceramic, coating, wood, stone not underfoot; TwoLayer;
    # Matter's Subsurface
    "sphere_cube": {"keep": ["/World/Subjects/Sphere", "/World/Subjects/Cube"], "build": None,
                    "views": {"card": SPHERE_CUBE_CARD, "close": SPHERE_CUBE_CLOSE}},
    # soil, sand, stone and floors seen underfoot: the rig's 1 m slab, 2 cm thick, low camera
    # Faces straight up into the sky and both lights: an 18 % grey lying flat read RGB 200-221 where
    # it reads 149 standing, so the slab is shot a stop down (17.2; ``exposure`` adds to the look's)
    "slab": {"keep": ["/World/Subjects/Floor"], "build": None, "lift": 0.02, "exposure": -1.0,
             "views": {"card": {"pos": (0.0, 0.36, 1.30), "aim": (0.0, 0.0, -0.08), "focal": 50.0},
                       "close": {"pos": (0.06, 0.17, 0.62), "aim": (0.0, 0.02, 0.18), "focal": 50.0}}},
    # cementitious: a wall section, 1.0 x 0.8 x 0.12 m, turned to show its end
    "wall": {"keep": [], "build": "wall",
             "views": {"card": {"pos": (0.05, 0.52, 2.15), "aim": (0.0, 0.40, -0.10), "focal": 50.0},
                       "close": {"pos": (0.50, 0.62, 0.78), "aim": (0.28, 0.50, 0.10), "focal": 50.0}}},
    # TranslucentThin: a 6 mm pane, 0.45 x 0.60 m, in front of a patterned card
    "pane": {"keep": [], "build": "pane",
             "views": {"card": {"pos": (0.22, 0.42, 1.45), "aim": (0.0, 0.30, -0.05), "focal": 50.0},
                       "close": {"pos": (0.30, 0.66, 0.50), "aim": (0.12, 0.52, 0.05), "focal": 50.0}}},
    # TranslucentThick: a round brilliant 25 mm across, and a 35 mm block
    "gem": {"keep": [], "build": "gem",
            "views": {"card": {"pos": (0.0, 0.065, 0.20), "aim": (0.004, 0.012, 0.0), "focal": 50.0},
                      "close": {"pos": (-0.035, 0.050, 0.085), "aim": (-0.022, 0.010, 0.0), "focal": 50.0}}},
    # textile (Opaque): a cloth draped over a ball
    "drape": {"keep": [], "build": "drape",
              "views": {"card": {"pos": (0.0, 0.55, 1.30), "aim": (0.0, 0.08, 0.0), "focal": 50.0},
                        "close": {"pos": (0.07, 0.25, 0.30), "aim": (0.02, 0.16, 0.06), "focal": 50.0}}},
    # Masked textile (lace): the same drape over a dark ball, so the holes read
    "lace": {"keep": [], "build": "lace",
             "views": {"card": {"pos": (0.0, 0.55, 1.30), "aim": (0.0, 0.08, 0.0), "focal": 50.0},
                       "close": {"pos": (0.07, 0.25, 0.30), "aim": (0.02, 0.16, 0.06), "focal": 50.0}}},
    # Emissive: a tube bent into a ring, lit and in the dark
    "tube": {"keep": [], "build": "tube",
             "views": {"card": {"pos": (0.0, 0.24, 1.00), "aim": (0.0, 0.17, 0.0), "focal": 50.0},
                       "dark": {"pos": (0.0, 0.24, 1.00), "aim": (0.0, 0.17, 0.0), "focal": 50.0,
                                "dark": True}}},
    # utility (virtual): a flat card, 0.3 m square, face on
    "card": {"keep": [], "build": "card",
             "views": {"card": {"pos": (0.0, 0.17, 0.95), "aim": (0.0, 0.16, 0.0), "focal": 50.0}}},
    # vegetation: leaf cards, one lying and one leaning
    "leaf": {"keep": [], "build": "leaf",
             "views": {"card": {"pos": (0.0, 0.20, 0.42), "aim": (0.005, 0.025, 0.0), "focal": 50.0},
                       "close": {"pos": (0.05, 0.12, 0.17), "aim": (0.02, 0.03, 0.0), "focal": 50.0}}},
}
VIEW_ORDER = ("card", "close", "dark")

# Stone and floors seen underfoot: the scale tag cannot say (Granite_Polished and Slate_Cleft are
# both s1), so it is settled here, article by article (17.2). Terrazzo is cementitious by class and
# a floor by use.
UNDERFOOT = {"Slate_Cleft", "Terrazzo_Polished"}


class NotYet(Exception):
    """An article whose subject a later step builds (Character: 17.3)."""


def subject_for(master: str, path: Path) -> str:
    """The subject an article is pictured on, from its master, its class and its name."""
    rel = path.resolve().relative_to(REPO / "MatterLibrary" / "materials").parts
    domain, klass = rel[0], rel[1]
    name = "_".join(path.stem.split("_")[:2])
    if domain == "character":
        raise NotYet(f"{path.stem}: a Character article is pictured on the character (17.3)")
    if master == "Emissive":
        return "tube"
    if master == "TranslucentThin":
        return "pane"
    if master == "TranslucentThick":
        return "gem"
    if klass == "vegetation":
        return "leaf"
    if klass == "textile":
        return "lace" if master == "Masked" else "drape"
    if klass == "virtual":
        return "card"
    if name in UNDERFOOT or klass in ("soil", "sand"):
        return "slab"
    if klass == "cementitious":
        return "wall"
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


def scene_hash(look: dict, subject: str) -> str:
    """The scene as it is drawn: the look the job carries, this subject (its geometry and cameras)
    and the Blender side. A number tuned without a ``SCENE_VERSION`` bump still makes the pictures
    it changes stale, and only those (a new tube leaves the oak alone)."""
    h = hashlib.sha256(json.dumps({"look": look, "subject": SUBJECTS.get(subject)},
                                  sort_keys=True).encode())
    for f in ("showcase_blender.py", "subjects_blender.py"):
        h.update((HERE / f).read_bytes())
    return h.hexdigest()


def record(mtlx: Path, textures, renderer: dict, views: list[str], subject: str, look: dict,
           seconds: dict | None = None) -> dict:
    """What a picture was made from. ``seconds`` (GPU time per view) is a measurement, not an
    input, so it is written and never compared."""
    r = {"article": mtlx.stem, "article_sha256": article_hash(mtlx, textures),
         "masters_sha256": masters_hash(), "renderer": renderer,
         "scene_version": SCENE_VERSION, "scene_sha256": scene_hash(look, subject),
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
