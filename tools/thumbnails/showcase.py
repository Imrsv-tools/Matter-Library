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
EXPOSURE = 0.0     # planned: -0.5 with SCENE_VERSION = 2, so whites keep their detail (the lead,
                   # 2026-10-14, Phase17 RD-P17-6); this phase ships version 1 as kept
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


def subject_for(master: str, path: Path) -> str:
    """The subject an article is pictured on, from its master, its class and its name."""
    rel = path.resolve().relative_to(REPO / "MatterLibrary" / "materials").parts
    domain, klass = rel[0], rel[1]
    name = "_".join(path.stem.split("_")[:2])
    if domain == "character":
        return "character"          # on the clothed character, in a human context (17.3)
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


# ------------------------------------------------------------------ Character (17.3)

# A Character article is pictured on the clothed character only (F-MP-17, RD-P13-2, RD-DS-4), from
# these views and NO OTHER: the whole body, the waist and the feet are never a thumbnail.
CHARACTER_VIEWS = ("face", "hand", "mouth", "lips", "eye", "head")


class Refused(ValueError):
    """A view a Character article is never pictured from."""


def character_views(names) -> list[str]:
    """``names``, refused unless every one is on the whitelist (``CHARACTER_VIEWS``)."""
    names = list(names)
    bad = [n for n in names if n not in CHARACTER_VIEWS]
    if bad:
        raise Refused(f"view {', '.join(map(repr, bad))} is never a thumbnail: a Character article is "
                      f"pictured only from {', '.join(CHARACTER_VIEWS)} (F-MP-17)")
    return names


# Each family: the parts its article goes on, and the views it is pictured from (the Brief's
# §The subjects). The rest of the character wears the rig's cast (``rig.cast_for``), on the skin
# of the article's own tone where it has one.
CHARACTER_FAMILIES = {
    "Skin": (["Body"], ["face", "hand"]),
    "Lips": (["Lips"], ["lips"]),
    "Nail": (["Nails"], ["hand"]),
    "Eye": (["Pupil", "Iris", "Sclera"], ["eye"]),
    "Iris": (["Iris"], ["eye"]),
    "Pupil": (["Pupil"], ["eye"]),
    "Sclera": (["Sclera"], ["eye"]),
    "Cornea": (["Cornea"], ["eye"]),
    "Enamel": (["Teeth"], ["mouth"]),
    "Gum": (["Gums"], ["mouth"]),
    "Tongue": (["Tongue"], ["mouth"]),
    "Hair": (["Hair", "Brows", "Lashes"], ["head"]),
}
CHARACTER_FOCAL = 50.0
# A family whose part the view's own framing cannot show: MakeHuman's jaw is closed, so the tongue
# sits behind the teeth in the mouth view. For a Tongue article the view also hides the teeth and
# looks down from ``raise`` metres higher (17.3).
CHARACTER_VIEW_EXTRA = {"Tongue": {"hide": ["Teeth"], "raise": 0.05}}


def character_family(stem: str) -> tuple[list[str], list[str]]:
    fam = stem.split("_")[0]
    if fam not in CHARACTER_FAMILIES:
        raise SystemExit(f"{stem}: no Character family {fam!r} (have {', '.join(CHARACTER_FAMILIES)})")
    parts, views = CHARACTER_FAMILIES[fam]
    return parts, character_views(views)


def _centre(pts):
    return tuple((min(p[k] for p in pts) + max(p[k] for p in pts)) / 2 for k in range(3))


def character_cameras(parts: dict, rig_cams: dict) -> dict:
    """Every whitelisted view's camera, framed from the parts' bounds (rig space: metres, Y up,
    the character facing +Z, its left hand at +X). ``hand`` and ``mouth`` are the rig's own framings
    (``build_character.cameras``); ``face`` is half the face (the character's left eye, cheek and
    the side of the nose); ``lips``, ``eye`` and ``head`` are new."""
    def cam(pos, aim, **kw):
        return {"pos": tuple(round(c, 4) for c in pos), "aim": tuple(round(c, 4) for c in aim),
                "focal": CHARACTER_FOCAL, "relight": True} | kw
    eye = _centre([p for p in parts["Iris"]["points"] if p[0] > 0])
    lips = _centre(parts["Lips"]["points"])
    hair = _centre(parts["Hair"]["points"])
    cheek = (eye[0] * 1.5, eye[1] - 0.03, eye[2] - 0.03)
    hand, mouth = rig_cams["CamHand"], rig_cams["CamMouth"]
    return {
        "face": cam((cheek[0] + 0.13, cheek[1] + 0.02, cheek[2] + 0.13), cheek),
        "hand": cam(*hand),
        # MakeHuman's mouth is closed, so the rig's view hides the face; a thumbnail hides every part
        # but the mouth's, or the hair behind the head shows through it
        "mouth": cam(*mouth, hide=sorted(p for p in parts if p not in ("Teeth", "Gums", "Tongue"))),
        "lips": cam((lips[0], lips[1] + 0.005, lips[2] + 0.11), lips),
        "eye": cam((eye[0] + 0.005, eye[1] + 0.004, eye[2] + 0.075), eye),
        "head": cam((hair[0] + 0.32, hair[1] + 0.12, hair[2] + 0.42), (hair[0], hair[1] - 0.01, hair[2])),
    }


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


def scene_hash(look: dict, spec: dict) -> str:
    """The scene as it is drawn: the look the job carries, this subject as sent (its geometry,
    cameras and, for Character, its cast) and the Blender side. A number tuned without a
    ``SCENE_VERSION`` bump still makes the pictures it changes stale, and only those (a new tube
    leaves the oak alone)."""
    h = hashlib.sha256(json.dumps({"look": look, "subject": spec}, sort_keys=True, default=str).encode())
    for f in ("showcase_blender.py", "subjects_blender.py"):
        h.update((HERE / f).read_bytes())
    return h.hexdigest()


def record(mtlx: Path, textures, renderer: dict, views: list[str], subject: str, look: dict,
           spec: dict, context=(), seconds: dict | None = None) -> dict:
    """What a picture was made from. ``seconds`` (GPU time per view) is a measurement, not an
    input, so it is written and never compared. ``context`` is every other file the picture is
    drawn from: the rig scene file and, on the character, the cast's articles, their textures and
    the fit maps; a changed skin makes the lips picture stale."""
    r = {"article": mtlx.stem, "article_sha256": article_hash(mtlx, textures),
         "masters_sha256": masters_hash(), "renderer": renderer,
         "scene_version": SCENE_VERSION, "scene_sha256": scene_hash(look, spec),
         "context_sha256": _sha(sorted(set(map(Path, context)))),
         "samples": SAMPLES, "size": SIZE,
         "subject": subject, "views": sorted(views)}
    if seconds is not None:
        r["seconds"] = seconds
    return r


INPUTS = ("article_sha256", "masters_sha256", "renderer", "scene_version", "scene_sha256", "context_sha256",
          "samples", "size",
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
