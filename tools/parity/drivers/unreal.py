#!/usr/bin/env python3
"""Unreal driver: render every setting of a job in the Matter Unreal runtime (Phase06).

    uv run tools/parity/drivers/unreal.py <job.json>              # what rig.py runs
    uv run tools/parity/drivers/unreal.py --calibrate <job.json>  # the grey card's light factors

Writes ``<out_dir>/unreal/<setting id><view suffix>.png`` (8-bit sRGB, ``width`` square).

The runtime is our own small Unreal app (``unreal/MatterRuntime``). It imports nothing at run
time: this driver hands it an **Unreal job** (``<out_dir>/unreal/job/unreal_job.json``) with the
scene already converted, so a packaged build renders any job without the editor:

* **the meshes** come from the same generators that write the rig's USD scene
  (``scene/build_scene.py``), converted here once: metres, Y up, right-handed ->
  centimetres, Z up, left-handed, by ``(x, y, z) -> 100 (-z, x, y)``. That map has determinant
  -1, which is exactly the handedness change, so USD's counter-clockwise front faces arrive as
  Unreal's front faces with their index order kept (checked against the engine's own
  ``UKismetProceduralMeshLibrary::GenerateBoxMesh``). The subjects' ``st`` is divided by the
  article's ``meters_per_tile``, as the setting scene does (``job.py``); tangents are ``dP/ds``
  from that ``st``. Metres are honoured by construction (JOB_FORMAT.md §Units). The character
  (6.5) comes from ``scene/build_character.py`` the same way, one mesh and one material slot per
  part, its faceVarying ``st`` split into one vertex per (point, uv) pair.
* **the material** of each setting: the article read by the one shared reader
  (``blender/masters/article.py``), its values set on its master under the article's names
  (Phase06 D5), with the setting's sliders applied as a Creator would.
* **the views** from the scene's cameras (translate, then rotateXYZ: X first), 50 mm on a
  36 mm square aperture; **the lights** from the scene's numbers, times the calibration below.

The runtime writes linear scene colour (before the tonemapper, exposure fixed); this driver
applies the view's ``exposure``, box-filters the supersampling and does the plain sRGB encode,
as Storm's and Blender's columns are encoded (Phase06 D8).

Where the runtime comes from, first found wins: ``$MATTER_UNREAL_RUNTIME`` (a packaged build's
launcher); editor mode on request, ``$MATTER_UNREAL_EDITOR`` (an Unreal 5.8 ``UnrealEditor``) on
``unreal/MatterRuntime``; else the build ``unreal/RUNTIME.json`` pins, a GitHub Release asset of
this repo, downloaded once into the git-ignored ``unreal/package/`` and checked by sha256
(Phase06 D2), so a machine with no Unreal renders the column. ``find_runtime()`` returns None
when there is none, and the rig then skips the column with a notice.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE.parent / "scene"))
sys.path.insert(0, str(REPO / "blender" / "masters"))
import article  # noqa: E402  (the shared reader: plain XML, no bpy)
import build_scene  # noqa: E402

TOOL = "unreal"
PROJECT = REPO / "unreal" / "MatterRuntime" / "MatterRuntime.uproject"
SUPERSAMPLE = 4          # Unreal renders with no anti-aliasing (the rig's AA is supersampling)
SETTLE_FRAMES = 120
TIMEOUT_S = 3600         # a first editor-mode launch compiles shaders for ~12 minutes (UR-F6)

# The calibration (Phase06 step 6.1, `--calibrate` on the grey card; the value and how it was
# measured are in the phase doc's execution log). Like Blender's DOME_K / SUN_K: the light a
# scene value asks for, times the factor that makes Unreal's picture of it agree.
# Measured 2026-09-29 against Storm (this machine's Blender cannot render parity), editor mode,
# the two-call Opaque master at 160 bytes/pixel (6.3, run 3): DOME_K from the white mirror (it reads
# 0.4975 of the dome's 0.5029 at factor 1), SUN_K on the grey card with the dome fixed; fitted
# per-pixel error over the subjects median 1.0 %, p95 3.3 %; sphere / cube / floor 1.002 / 1.000 /
# 0.995 of Storm. (6.1's two-factor grey-card fit, SUN_K 1.033 / DOME_K 1.068, lit specular 6 % hot.)
EXPOSURE_K = 0.999       # Unreal's scene colour for a radiance of 1 (read off the visible dome)
SUN_K = 1.130
DOME_K = 1.011

# The masters this runtime has, and what of an article each one can carry so far. An article
# needing more is refused by name, so the rig shows "not yet" instead of a wrong picture.
# The runtime refuses any other job format (2, 6.3: mesh buffers carry a tangent sign; 3, Phase09
# 9.3: the picture is the masters' own base_color_map_tex, which a v1-v2 master would silently drop).
JOB_FORMAT = 3
BUILT_MASTERS = {"Opaque", "TwoLayer", "Masked", "Emissive", "Subsurface", "TranslucentThin",
                 "TranslucentThick", "Hair"}
BASE_MAP_MASTERS = {"Opaque", "Masked", "Hair", "Subsurface"}   # build_masters.py MASTERS' base_map
CUTOUT_PORT = "cutout_map"   # not a slider: the mesh's map, supplied per binding (LCDSchema §Cut-out map)
BASE_MAP_PORT = "base_color_map"   # not a slider: the mesh's picture, per binding (Phase09 RD-P09-1)
# the article's texture roles -> the master's <role>_tex slots (6.3: the Opaque core in full;
# 6.4: TwoLayer's layer 2, Masked's opacity)
IMAGE_ROLES = ("base_color", "roughness", "metalness", "normal",
               "layer2_base_color", "layer2_roughness", "layer2_metalness", "layer2_normal", "opacity")
LAYER_ROLES = ("maskset", "overlay1", "overlay2", "overlay3")     # tiled, each at its own size
TEXTURE_ROLES = set(IMAGE_ROLES) | set(LAYER_ROLES)
COLOUR_ROLES = {"base_color", "layer2_base_color"}   # decoded from sRGB when the article says so
# each layer's constant: (texture role, the master's parameter); the constant goes neutral (1)
# where the article binds the texture instead
LAYER_CONSTANTS = (("base_color", "base_color"), ("roughness", "specular_roughness"),
                   ("metalness", "base_metalness"), ("layer2_base_color", "layer2_base_color"),
                   ("layer2_roughness", "layer2_roughness"), ("layer2_metalness", "layer2_metalness"),
                   ("opacity", "geometry_opacity"))
SLIDERS = {"base_color_tint", "roughness_bias", "uv_scale", "uv_offset", "uv_rotation", "maskset_blend",
           "overlay1_density", "overlay2_density", "overlay3_density",
           "layer_blend_balance", "layer_blend_contrast", "opacity_cutoff",
           # Phase10: a deposit's colour, with overlayN_deposit = 1 on its slot. unreal-runtime-v2's
           # masters have neither parameter and Unreal ignores a parameter a master lacks, so v2
           # draws today's colourless dust (F-P10-14); the masters take them at 10.4.
           "overlay1_color", "overlay2_color", "overlay3_color",
           # Phase12: a value the Creator may SET, under the article's (and OpenPBR's) own name.
           # Every runtime's see-through masters already carry it as a parameter (F-GLC-4).
           "transmission_color",
           # Phase12 12.4: a light's colour and brightness, the Emissive master's own parameters.
           # The master multiplies the brightness by 1/0.798 itself (Learnings Unreal U4), so a
           # Creator's value gets the same correction as the article's.
           "emission_color", "emission_luminance"}
COLOUR_SLIDERS = {"base_color_tint", "overlay1_color", "overlay2_color", "overlay3_color",
                  "transmission_color", "emission_color"}
FLAT_NORMAL = [0.5, 0.5, 1.0, 1.0]     # exact, for an article with no normal map
# lane-A values passed straight to Epic's OpenPBR function under their own names
PASS_THROUGH = {"base_weight", "base_diffuse_roughness", "specular_weight",
                "specular_color", "specular_ior", "specular_roughness_anisotropy", "coat_weight",
                "coat_color", "coat_roughness", "coat_ior", "coat_darkening", "fuzz_weight", "fuzz_color", "fuzz_roughness",
                "emission_luminance", "emission_color", "subsurface_weight", "subsurface_color",
                "subsurface_radius", "subsurface_radius_scale", "subsurface_scatter_anisotropy",
                "transmission_weight", "transmission_color", "transmission_depth"}
LINEAR_SPACES = {"lin_rec709", "raw", None}


class Unsupported(Exception):
    """The article needs a part of a master this runtime does not have yet."""


# ------------------------------------------------------------------ geometry

def to_ue(p: np.ndarray) -> np.ndarray:
    """Directions (or, times 100, points): USD Y-up right-handed -> Unreal Z-up left-handed."""
    p = np.asarray(p, dtype=np.float64)
    return np.stack([-p[..., 2], p[..., 0], p[..., 1]], axis=-1)


def rot_xyz(rx: float, ry: float, rz: float = 0.0) -> np.ndarray:
    """USD's xformOp:rotateXYZ (degrees) as a column-vector matrix: X first, then Y, then Z."""
    a, b, c = (math.radians(v) for v in (rx, ry, rz))
    Rx = np.array([[1, 0, 0], [0, math.cos(a), -math.sin(a)], [0, math.sin(a), math.cos(a)]])
    Ry = np.array([[math.cos(b), 0, math.sin(b)], [0, 1, 0], [-math.sin(b), 0, math.cos(b)]])
    Rz = np.array([[math.cos(c), -math.sin(c), 0], [math.sin(c), math.cos(c), 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def triangulate(faces) -> np.ndarray:
    """Fans, keeping each polygon's winding."""
    return np.array([(f[0], f[k], f[k + 1]) for f in faces for k in range(1, len(f) - 1)], dtype=np.int64)


def tangents(p: np.ndarray, n: np.ndarray, uv: np.ndarray, tris: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Per-vertex dP/ds, made perpendicular to the normal (the tangent a normal map's X
    follows), and dP/dt (the direction its Y follows: MaterialX normal maps are +Y up)."""
    i0, i1, i2 = tris[:, 0], tris[:, 1], tris[:, 2]
    e1, e2 = p[i1] - p[i0], p[i2] - p[i0]
    d1, d2 = uv[i1] - uv[i0], uv[i2] - uv[i0]
    det = d1[:, 0] * d2[:, 1] - d2[:, 0] * d1[:, 1]
    r = np.where(np.abs(det) > 1e-12, 1.0 / np.where(det == 0, 1, det), 0.0)
    t = (e1 * d2[:, 1:2] - e2 * d1[:, 1:2]) * r[:, None]
    b = (e2 * d1[:, 0:1] - e1 * d2[:, 0:1]) * r[:, None]
    acc, bacc = np.zeros_like(p), np.zeros_like(p)
    for k in (i0, i1, i2):
        np.add.at(acc, k, t)
        np.add.at(bacc, k, b)
    acc -= n * np.sum(acc * n, axis=1, keepdims=True)
    ln = np.linalg.norm(acc, axis=1, keepdims=True)
    fallback = np.cross(n, np.where(np.abs(n[:, 1:2]) < 0.9, [[0, 1, 0]], [[1, 0, 0]]))
    fallback /= np.linalg.norm(fallback, axis=1, keepdims=True)
    return np.where(ln > 1e-9, acc / np.maximum(ln, 1e-12), fallback), bacc


def tangent_signs(n_ue: np.ndarray, t_ue: np.ndarray, dpdt_ue: np.ndarray) -> np.ndarray:
    """Unreal builds the binormal as cross(N, T) x sign (LocalVertexFactory.ush; the sign is
    ProcMesh's bFlipTangentY). Choose the sign that makes it dP/dt, in Unreal's own space: the
    handedness change flips every cross product, so it is -1 on the plain scene (6.1 read)."""
    return np.where(np.sum(np.cross(n_ue, t_ue) * dpdt_ue, axis=1) < 0.0, -1.0, 1.0)


def write_mesh(folder: Path, name: str, pts, nrm, uvs, faces, material: str) -> dict:
    """One mesh buffer: float32 positions, normals, tangents (Unreal space), st, tangent signs;
    int32 triangles (the runtime's LoadMesh; job format 2)."""
    p, n = np.asarray(pts, float), np.asarray(nrm, float)
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    uv = np.asarray(uvs, float)
    tris = triangulate(faces)
    t, dpdt = tangents(p, n, uv, tris)
    n_ue, t_ue = to_ue(n), to_ue(t)
    sign = tangent_signs(n_ue, t_ue, to_ue(dpdt))
    buf = (np.concatenate([(to_ue(p) * 100.0).ravel(), n_ue.ravel(), t_ue.ravel(), uv.ravel(), sign])
           .astype("<f4").tobytes() + tris.astype("<i4").tobytes())
    f = folder / f"{name}.bin"
    f.write_bytes(buf)
    return {"name": name, "file": str(f), "verts": len(p), "indices": int(tris.size), "material": material}


def camera_view(pos, rot, suffix: str, hide=()) -> dict:
    R = rot_xyz(rot[0], rot[1])
    fov = math.degrees(2 * math.atan(build_scene.CAM_APERTURE / 2 / build_scene.CAM_FOCAL))
    return {"suffix": suffix, "location": list(to_ue(np.array(pos)) * 100.0),
            "forward": list(to_ue(R @ [0, 0, -1])), "up": list(to_ue(R @ [0, 1, 0])),
            "fov": fov, "near": 2.0, "hide": list(hide)}


TEST_CAMERAS = {"/World/Cam": (build_scene.CAM_POS, (build_scene.CAM_PITCH, 0.0)),
                "/World/CamClose": (build_scene.CLOSE_POS, build_scene.CLOSE_ROT),
                build_scene.SIDE_CAMERA: (build_scene.SIDE_POS, build_scene.SIDE_ROT)}


def lights(sun_k: float = SUN_K, dome_k: float = DOME_K) -> tuple[dict, dict]:
    d = rot_xyz(*build_scene.SUN_ROTATE) @ [0, 0, -1]          # a distant light shines along -Z
    sun = {"direction": list(to_ue(d)), "intensity": build_scene.SUN_INTENSITY * sun_k,
           "angle": build_scene.SUN_ANGLE}
    r = build_scene.DOME_RADIANCE                             # Storm draws the dome as its texture
    sky = {"radiance": [r, r, r], "intensity": build_scene.DOME_INTENSITY * dome_k}
    return sun, sky


# ------------------------------------------------------------------ materials

def _vec(v) -> list[float]:
    v = [float(x) for x in (v if isinstance(v, (list, tuple)) else [v])]
    return v * 3 if len(v) == 1 else v[:3]


def article_material(path: Path, sliders: dict | None = None, cutout_map: Path | None = None,
                     base_color_map: Path | None = None) -> dict:
    """The article on its master, by the article's names; raises Unsupported if not yet built.

    ``cutout_map`` is a binding's cut-out (a character's hair, brows, lashes: JOB_FORMAT.md
    ``bindings[].cutout_map``): the master samples it on the mesh's own st, unplaced, as the
    article's coverage (Masked thresholds it, Hair dithers it). Without one the card is solid.

    ``base_color_map`` is a binding's picture (Phase09 RD-P09-1): the master's own
    ``base_color_map_tex``, sampled on the mesh's st, unplaced (the caller checks the part's st is
    its atlas), multiplied into the base (9.3; it rode ``base_color_tex`` on the v1 masters). On
    Subsurface it scales ``subsurface_color`` too, which is exact where the article connects its
    subsurface colour to an untinted, untextured base (F-P09-5); anything else is refused.
    """
    art = article.read(Path(path))
    if art.master not in BUILT_MASTERS:
        raise Unsupported(f"{art.name}: the {art.master} master is not built in Unreal yet")
    extra = sorted(set(art.textures) - TEXTURE_ROLES)
    if extra:
        raise Unsupported(f"{art.name}: textures {extra} are not carried by Unreal's masters yet")
    unported = sorted(set(art.ports) - SLIDERS - {CUTOUT_PORT, BASE_MAP_PORT})
    if unported:
        raise Unsupported(f"{art.name}: sliders {unported} are not carried by Unreal's masters yet")
    if cutout_map is not None and CUTOUT_PORT not in art.ports:
        raise KeyError(f"{art.name} does not declare the cut-out input ({CUTOUT_PORT})")
    if base_color_map is not None:
        if BASE_MAP_PORT not in art.ports:
            raise KeyError(f"{art.name} does not declare the picture input ({BASE_MAP_PORT})")
        if art.master not in BASE_MAP_MASTERS:
            raise Unsupported(f"{art.name}: the {art.master} master has no base_color_map input")
        if art.master == "Subsurface" and "subsurface_weight" in art.shader:
            # the master scatters subsurface_color x the picture (F-P09-5): exact only for a
            # subsurface colour CONNECTED to a base that is the constant x the picture alone
            why = ("its subsurface colour is its own value" if "subsurface_color" in art.shader else
                   "its base has a texture" if "base_color" in art.textures else
                   "its base is tinted" if "base_color_tint" in art.ports else None)
            if why:
                raise Unsupported(f"{art.name}: a picture on Unreal's Subsurface master, but {why}")
    ports = {k: v for k, v in art.ports.items() if k not in (CUTOUT_PORT, BASE_MAP_PORT)}
    for k, v in (sliders or {}).items():
        if k not in ports:
            raise KeyError(f"{art.name} does not declare the slider {k!r}")
        ports[k] = list(v) if isinstance(v, (list, tuple)) else [float(v)]
    sh, scalars, vectors, textures = art.shader, {}, {}, {}
    for role, file_cs in art.textures.items():
        file, cs = file_cs
        textures[f"{role}_tex"] = {"file": str(file), "srgb": role in COLOUR_ROLES and cs not in LINEAR_SPACES}
        if role in LAYER_ROLES:
            scalars[f"{role}_layer_scale"] = float(art.layer_scale.get(role, 1.0))
    for n in ("normal", "layer2_normal"):
        if n not in art.textures:
            textures[f"{n}_tex"] = {"constant": FLAT_NORMAL}
    if cutout_map is not None:
        textures["cutout_tex"] = {"file": str(cutout_map), "srgb": False}
    if base_color_map is not None:
        textures["base_color_map_tex"] = {"file": str(base_color_map), "srgb": True}
    for role, param in LAYER_CONSTANTS:
        if role in art.textures:
            value = [1.0]                 # the texture carries it; the constant stays neutral
        else:
            value = art.consts.get(role) or sh.get(param)
        if value is None:
            continue
        if role.endswith("base_color"):
            vectors[param] = _vec(value)
        else:
            scalars[param] = float(value[0])
    for k in PASS_THROUGH & set(sh):
        if len(sh[k]) >= 3:
            vectors[k] = _vec(sh[k])
        else:
            scalars[k] = float(sh[k][0])
    # Phase09 (F-P09-5): a Subsurface article's subsurface_color CONNECTED to its base (no value on
    # the shader) scatters the base's colour: the article's constant here, which the master
    # multiplies by the binding's picture (base_color_map_tex, white when none is bound).
    if art.master == "Subsurface" and "subsurface_weight" in sh and "subsurface_color" not in sh:
        vectors["subsurface_color"] = list(vectors.get("base_color", [0.8, 0.8, 0.8]))
    # the Creator sliders, under the article's names (D5); a vector2 port is a vector's R, G
    for k, v in ports.items():
        if k in COLOUR_SLIDERS:
            vectors[k] = _vec(v)
            if k.startswith("overlay"):
                scalars[k.replace("_color", "_deposit")] = 1.0
        elif k in ("uv_scale", "uv_offset"):
            vectors[k] = [float(v[0]), float(v[-1]), 0.0]
        else:
            scalars[k] = float(v[0])
    return {"master": art.master, "scalars": scalars, "vectors": vectors, "textures": textures}


def preview_surface(colour: float | None = None, texture: Path | None = None, roughness: float = 0.9) -> dict:
    """The scene furniture's UsdPreviewSurface (build_scene.preview_material) on the Opaque master."""
    m = {"master": "Opaque", "scalars": {"specular_roughness": roughness, "base_metalness": 0.0,
                                         "specular_ior": 1.5},
         "vectors": {"base_color": [1.0] * 3 if texture else [colour] * 3},
         "textures": {"normal_tex": {"constant": FLAT_NORMAL}}}
    if texture:
        m["textures"]["base_color_tex"] = {"file": str(texture), "srgb": True}
    return m


# ------------------------------------------------------------------ the mask

MASK_ID = "__mask"
TEST_MASK = [(1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (0.0, 0.0, 1.0)]   # sphere, cube, floor (compare.REGIONS)


def mask_colours(job: dict, names: list[str]) -> dict[str, tuple]:
    given = job.get("mask_colours")
    if given:
        return {p.rsplit("/", 1)[1]: tuple(c) for p, c in given.items()}
    return dict(zip(names, TEST_MASK))


def mask_setting(job: dict, names: list[str], furniture: dict) -> dict:
    """The subjects in flat colours on the unlit Sky master, the furniture black: Unreal's own
    mask, for a machine where the Blender driver (which writes the rig's mask) is not run."""
    flat = lambda c: {"master": "Sky", "vectors": {"radiance": list(c)}}  # noqa: E731
    cols = mask_colours(job, names)
    return {"id": MASK_ID, "materials": {n: flat(cols[n]) for n in names}
            | {k: flat((0.0, 0.0, 0.0)) for k in furniture}}


def write_mask(raw: Path, png: Path, cols: dict) -> None:
    """Classify the flat-colour capture into a clean mask: a pixel within 0.1 of a subject's colour
    is that colour, everything else (the dome, edges) black. Written as the rig's masks are: the
    colour through a plain sRGB encode."""
    lin = linear(raw)
    out = np.zeros(lin.shape, dtype=np.uint8)
    for c in cols.values():
        hit = np.all(np.abs(lin - np.array(c)) < 0.1, axis=-1)
        out[hit] = srgb8(np.array(c, dtype=np.float64))
    Image.fromarray(out).save(png)


# ------------------------------------------------------------------ the Unreal job

def face_varying(points, normals, faces, st) -> tuple[list, list, list, list]:
    """A faceVarying-st mesh (build_character: faces of (point, uv) index pairs, st per corner)
    as a per-vertex one: one vertex per distinct (point, uv) pair, keeping the point's normal."""
    remap, pts, nrm, uvs, out = {}, [], [], [], []
    corner = 0
    for f in faces:
        poly = []
        for vi, ti in f:
            key = (vi, ti)
            if key not in remap:
                remap[key] = len(pts)
                pts.append(points[vi])
                nrm.append(normals[vi])
                uvs.append(st[corner])
            poly.append(remap[key])
            corner += 1
        out.append(poly)
    return pts, nrm, uvs, out


CHARACTER = "/World/Character/"


def character_scene(job: dict, meshes_dir: Path, settings: list) -> tuple[list, list, dict, dict]:
    """The character job (Phase07 7.4; JOB_FORMAT.md §The character job): every part of the scene
    as its own mesh and its own material slot; a bound part gets its article (one material per
    binding, its cut-out map with it), an unbound part the scene's grey. Its st is the scene's
    metres divided by the article's ``meters_per_tile``, except on a cut-out part, whose st stays
    the atlas its map is drawn on (``job.write_character_scene`` does the same).
    Returns the meshes, the bound part names, the unbound parts' materials and the cameras."""
    import build_character  # noqa: PLC0415  (heavy: parses the pinned sources)
    parts = build_character.load_parts()
    atlas = build_character.atlas_parts()      # the one copy of the rule (Phase09 F-P09-15)
    bound = {b["subject"].removeprefix(CHARACTER): b for b in job["bindings"]}
    unknown = sorted(set(bound) - set(parts))
    if unknown:
        raise SystemExit(f"the job binds parts the scene does not have: {unknown}")
    meshes, unbound = [], {}
    for name, part in parts.items():
        b = bound.get(name)
        k = 1.0 if (b is None or CHARACTER + name in atlas) else float(b["article"]["meters_per_tile"])
        pts, nrm, uvs, faces = face_varying(part["points"], part["normals"], part["faces"], part["st"])
        meshes.append(write_mesh(meshes_dir, name, pts, nrm, [(s / k, t / k) for s, t in uvs], faces, name))
        if b is None:
            unbound[name] = preview_surface(0.18, roughness=0.6)     # /World/Looks/Unbound
    for s in settings:
        for name, b in bound.items():
            cut, pic = b.get("cutout_map"), b.get("base_color_map")
            if pic and CHARACTER + name not in atlas:
                raise Unsupported(f"{name}: a base_color_map on a part whose st is not its atlas")
            s["materials"][name] = article_material(Path(b["article"]["path"]), s.get("set"),
                                                    Path(cut) if cut else None,
                                                    Path(pic) if pic else None)
    # the cameras as build_character writes them: translate to 4 places, rotateXYZ to 3
    cams = {}
    for cam, (pos, target) in build_character.cameras(parts).items():
        pitch, yaw = build_character._look_at(pos, target)
        cams[f"/World/{cam}"] = (tuple(round(v, 4) for v in pos), (round(pitch, 3), round(yaw, 3)))
    return meshes, list(bound), unbound, cams


def unreal_job(job: dict, folder: Path, sun_k: float = SUN_K, dome_k: float = DOME_K,
               extra_settings: list | None = None, extra_views: list | None = None) -> Path:
    """Convert a rig job (the test scene or the character) into the runtime's job; returns its path."""
    meshes_dir = folder / "meshes"
    meshes_dir.mkdir(parents=True, exist_ok=True)
    if job.get("mode") == "character":
        settings = [{"id": s["id"], "set": s.get("set"), "materials": {}} for s in job["settings"]]
        meshes, names, furniture, cameras = character_scene(job, meshes_dir, settings)
        for s in settings:
            s.pop("set")
            s["materials"] |= furniture
        return _write_ujob(job, folder, meshes, names, furniture, settings, cameras, sun_k, dome_k,
                           extra_settings, extra_views)
    mpt = float(job["article"]["meters_per_tile"])
    makers = {"Sphere": build_scene.sphere, "Cube": build_scene.rounded_cube, "Floor": build_scene.floor}
    meshes = []
    names = [prim.rsplit("/", 1)[1] for prim in job["subjects"]]
    for name in names:          # each subject its own slot: the mask colours them apart
        pts, nrm, uvs, idx = makers[name]()
        meshes.append(write_mesh(meshes_dir, name, pts, nrm, [(s / mpt, t / mpt) for s, t in uvs], idx, name))
    for name, mesh, mat in (("RulerBlack", build_scene.ruler(True), "ruler_black"),
                            ("RulerWhite", build_scene.ruler(False), "ruler_white"),
                            ("Wall", build_scene.wall(), "wall")):
        meshes.append(write_mesh(meshes_dir, name, *mesh, mat))
    furniture = {"ruler_black": preview_surface(0.02), "ruler_white": preview_surface(0.8),
                 "wall": preview_surface(texture=(build_scene.HERE / build_scene.UVGRID).resolve(), roughness=0.8)}
    settings = []
    for s in job["settings"]:
        mat = article_material(Path(job["article"]["path"]), s.get("set"))
        settings.append({"id": s["id"], "materials": {n: mat for n in names} | furniture})
    return _write_ujob(job, folder, meshes, names, furniture, settings, TEST_CAMERAS, sun_k, dome_k,
                       extra_settings, extra_views)


WARMUP_ID = "__warmup"


def warmup(settings: list) -> dict:
    """A throwaway first setting, a copy of the job's first: the launch's FIRST material assignment
    can draw a master as Unreal's default material with the runtime reporting ready (6.5: the
    character's Subsurface and Hair parts, setting 1 of a launch, every time; the same materials
    in any later setting rendered right; bisected on the character's own job). Its pictures are
    written and never read."""
    return {"id": WARMUP_ID, "materials": settings[0]["materials"]}


def _write_ujob(job: dict, folder: Path, meshes: list, names: list, furniture: dict, settings: list,
                cameras: dict, sun_k: float, dome_k: float, extra_settings, extra_views) -> Path:
    settings = ([warmup(settings)] + settings + list(extra_settings or [])
                + [mask_setting(job, names, furniture)])
    views = []
    for spec in job["views"].values():
        if spec["camera"] not in cameras:
            raise SystemExit(f"view camera {spec['camera']!r} is not in the scene (have {sorted(cameras)})")
        pos, rot = cameras[spec["camera"]]
        views.append(camera_view(pos, rot, spec["suffix"], [p.rsplit("/", 1)[1] for p in spec.get("hide", [])]))
    views += list(extra_views or [])
    sun, sky = lights(sun_k, dome_k)
    ujob = {"format": JOB_FORMAT, "width": int(job["width"]) * SUPERSAMPLE, "out_dir": str(folder / "raw"),
            "settle_frames": SETTLE_FRAMES, "sun": sun, "sky": sky, "meshes": meshes,
            "settings": settings, "views": views}
    p = folder / "unreal_job.json"
    p.write_text(json.dumps(ujob, indent=1) + "\n", encoding="utf-8")
    return p


# ------------------------------------------------------------------ running it

PIN = REPO / "unreal" / "RUNTIME.json"
PACKAGES = REPO / "unreal" / "package"          # git-ignored: downloaded builds, one folder per tag
RELEASES = "https://github.com/Imrsv-tools/Matter-Library/releases/download"


def find_runtime() -> list[str] | None:
    """The command that starts the runtime, or None (the rig skips the column with a notice).

    First found wins: ``$MATTER_UNREAL_RUNTIME`` (a launcher), editor mode when asked for by
    ``$MATTER_UNREAL_EDITOR``, else the build ``unreal/RUNTIME.json`` pins (Phase06 D2),
    downloaded and checked on first use.
    """
    exe = os.environ.get("MATTER_UNREAL_RUNTIME")
    if exe:
        return [exe]
    editor = os.environ.get("MATTER_UNREAL_EDITOR")
    if editor:
        return [editor, str(PROJECT), "-game"]
    if PIN.is_file():
        return [str(pinned_package())]
    return None


def pinned_package() -> Path:
    """The pinned build's launcher, downloading the release asset if this machine lacks it."""
    pin = json.loads(PIN.read_text(encoding="utf-8"))
    root = PACKAGES / pin["tag"]
    launcher, stamp = root / "Linux" / "MatterRuntime.sh", root / ".sha256"
    if launcher.is_file() and stamp.is_file() and stamp.read_text().strip() == pin["sha256"]:
        return launcher
    import hashlib  # noqa: PLC0415
    import shutil  # noqa: PLC0415
    import tarfile  # noqa: PLC0415
    import urllib.request  # noqa: PLC0415
    url = f"{RELEASES}/{pin['tag']}/{pin['asset']}"
    print(f"unreal: downloading {url} ({pin['size'] / 1e6:.0f} MB, once per machine)")
    PACKAGES.mkdir(parents=True, exist_ok=True)
    part = PACKAGES / f"{pin['asset']}.part"
    h = hashlib.sha256()
    with urllib.request.urlopen(url) as r, part.open("wb") as f:
        while chunk := r.read(1 << 20):
            h.update(chunk)
            f.write(chunk)
    if h.hexdigest() != pin["sha256"]:
        part.unlink()
        raise SystemExit(f"unreal: {url} has sha256 {h.hexdigest()}, the pin says {pin['sha256']}")
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir(parents=True)
    with tarfile.open(part) as t:
        t.extractall(root, filter="data")
    part.unlink()
    stamp.write_text(pin["sha256"] + "\n")
    if not launcher.is_file():
        raise SystemExit(f"unreal: {pin['asset']} has no Linux/MatterRuntime.sh")
    return launcher


def run_runtime(cmd: list[str], ujob: Path, log: Path) -> None:
    packaged = "-game" not in cmd
    env = dict(os.environ)
    if packaged:        # a package runs with no display at all, on SDL's dummy driver (UR-F8)
        env.pop("DISPLAY", None)
        env.pop("WAYLAND_DISPLAY", None)
    full = ["nice", "-n", "19", *cmd, f"-MatterJob={ujob}", "-RenderOffscreen", "-unattended",
            "-nosound", "-stdout", "-FullStdOutLogOutput"]
    record = ujob.parent / "raw" / "matter_runtime.log"     # the app's own record (Shipping has no log)
    record.unlink(missing_ok=True)
    with log.open("w", encoding="utf-8") as fh:
        rc = subprocess.run(full, stdout=fh, stderr=subprocess.STDOUT, env=env, timeout=TIMEOUT_S).returncode
    if rc != 0:
        raise SystemExit(f"Unreal runtime failed (exit {rc}); see {record} and {log}")


def read_pfm(path: Path) -> np.ndarray:
    with path.open("rb") as f:
        kind = f.readline().strip()
        w, h = map(int, f.readline().split())
        scale = float(f.readline())
        data = np.frombuffer(f.read(), dtype="<f4" if scale < 0 else ">f4")
    return np.flipud(data.reshape(h, w, 3 if kind == b"PF" else 1)).astype(np.float64)


def linear(path: Path, exposure: float = 0.0) -> np.ndarray:
    """A capture as the rig's linear picture: exposure applied, supersampling box-filtered."""
    img = read_pfm(path) / EXPOSURE_K * (2.0 ** exposure)
    h, w, c = img.shape
    return img.reshape(h // SUPERSAMPLE, SUPERSAMPLE, w // SUPERSAMPLE, SUPERSAMPLE, c).mean(axis=(1, 3))


def srgb8(lin: np.ndarray) -> np.ndarray:
    x = np.clip(lin, 0.0, 1.0)
    enc = np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055)
    return (enc * 255.0 + 0.5).astype(np.uint8)


def run(job_path: Path) -> None:
    job = json.loads(job_path.read_text(encoding="utf-8"))
    cmd = find_runtime()
    if cmd is None:
        raise SystemExit("no Unreal runtime (set MATTER_UNREAL_RUNTIME or MATTER_UNREAL_EDITOR)")
    out = Path(job["out_dir"]) / TOOL
    folder = out / "job"
    ujob = unreal_job(job, folder)
    run_runtime(cmd, ujob, out / "unreal.log")
    for s in job["settings"]:
        for spec in job["views"].values():
            lin = linear(folder / "raw" / f"{s['id']}{spec['suffix']}.pfm", float(spec.get("exposure", 0.0)))
            png = out / f"{s['id']}{spec['suffix']}.png"
            Image.fromarray(srgb8(lin)).save(png)
            print(f"unreal: wrote {png}")
    cols = mask_colours(job, [p.rsplit("/", 1)[1] for p in job["subjects"]])
    for spec in job["views"].values():
        write_mask(folder / "raw" / f"{MASK_ID}{spec['suffix']}.pfm", out / f"mask{spec['suffix']}.png", cols)


# ------------------------------------------------------------------ calibration

def calibrate(job_path: Path, ref_tool: str = "storm") -> None:
    """Fit SUN_K and DOME_K on the grey-card job, against a reference tool's picture of it.

    One launch renders the job's defaults three ways (sun and dome, sun only, dome only) at
    factors 1, the subjects as a white mirror under the dome alone, plus a view straight up into
    the dome and Unreal's own mask. The dome view gives EXPOSURE_K (an unlit sphere of radiance r
    reads EXPOSURE_K x r). **DOME_K comes from the mirror** (Phase06 6.3, the lead's ruling): a
    white mirror reflects exactly the dome's radiance, so it measures the light with no material
    model in it. **SUN_K is then fitted on the grey card with the dome fixed**:
    reference - DOME_K x dome-only = SUN_K x sun-only. (Fitting both on the grey card, as 6.1 did,
    let the two renderers' diffuse difference set DOME_K, which then scaled Unreal's specular
    6 % too bright.) The reference is Storm (USDLiveView's renderer) unless told otherwise: at
    the Phase05 close Storm and Blender agreed on the grey card to 0.35 dE2000.
    """
    global EXPOSURE_K
    import compare  # noqa: PLC0415  (tools/parity: the rig's own region reader)
    job = json.loads(job_path.read_text(encoding="utf-8"))
    out = Path(job["out_dir"])
    ref = out / ref_tool / "defaults.png"
    if not ref.is_file():
        raise SystemExit(f"run the rig on this job first ({ref} is missing)")
    cmd = find_runtime()
    if cmd is None:
        raise SystemExit("no Unreal runtime (set MATTER_UNREAL_RUNTIME or MATTER_UNREAL_EDITOR)")
    folder = out / TOOL / "calibrate"
    ujob = unreal_job(job, folder, sun_k=1.0, dome_k=1.0)
    spec = json.loads(ujob.read_text(encoding="utf-8"))
    mats, mask_s = spec["settings"][0]["materials"], spec["settings"][-1]
    names = [p.rsplit("/", 1)[1] for p in job["subjects"]]
    mirror = {"master": "Opaque", "scalars": {"specular_roughness": 0.0, "base_metalness": 1.0},
              "vectors": {"base_color": [1.0, 1.0, 1.0]}, "textures": {"normal_tex": {"constant": FLAT_NORMAL}}}
    spec["settings"] = [{"id": WARMUP_ID, "materials": mats}, {"id": "both", "materials": mats},
                        {"id": "sun", "materials": mats, "sky_scale": 0.0},
                        {"id": "dome", "materials": mats, "sun_scale": 0.0},
                        {"id": "mirror", "materials": mats | {n: mirror for n in names}, "sun_scale": 0.0}, mask_s]
    # the wide view, and one looking straight up from 3 m, where only the dome is in frame
    spec["views"] = [spec["views"][0], {"suffix": "__sky", "location": [0, 0, 300], "forward": [0, 0, 1],
                                        "up": [1, 0, 0], "fov": 30.0, "near": 2.0, "hide": []}]
    ujob.write_text(json.dumps(spec, indent=1) + "\n", encoding="utf-8")
    run_runtime(cmd, ujob, folder / "unreal.log")

    raw = folder / "raw"
    sky = read_pfm(raw / "both__sky.pfm")
    EXPOSURE_K = float(sky.mean() / build_scene.DOME_RADIANCE)
    mask = folder / "mask.png"
    write_mask(raw / f"{MASK_ID}.pfm", mask, mask_colours(job, names))
    both, sun, dome, mir = (linear(raw / f"{k}.pfm") for k in ("both", "sun", "dome", "mirror"))
    r8 = np.asarray(Image.open(ref).convert("RGB"), dtype=np.float64) / 255.0
    refl = np.where(r8 <= 0.04045, r8 / 12.92, ((r8 + 0.055) / 1.055) ** 2.4)
    regions = compare.masks(mask)
    on = regions["subjects"] & (refl.max(axis=2) < 0.98)
    # The dome from the white mirror, which reflects exactly the dome's radiance in any correct
    # renderer: the light alone, no material model in it (the lead, 6.3; it was fitted on the
    # grey card with the sun, which let the diffuse models' difference leak into the specular).
    dome_k = build_scene.DOME_RADIANCE / float(mir[regions["subjects"]].mean())
    # The sun on the grey card, the dome fixed: ref - DOME_K x dome = SUN_K x sun.
    s, r = sun[on].ravel(), (refl - dome_k * dome)[on].ravel()
    sun_k = float(s @ r / (s @ s))
    A = np.stack([sun[on].ravel(), dome[on].ravel()], axis=1)
    (old_sun, old_dome), *_ = np.linalg.lstsq(A, refl[on].ravel(), rcond=None)
    fit = sun_k * sun + dome_k * dome
    print(f"white mirror at factor 1 reads {mir[regions['subjects']].mean():.5f} "
          f"(dome radiance {build_scene.DOME_RADIANCE}); the two-factor grey-card fit would give "
          f"SUN_K {old_sun:.5f}, DOME_K {old_dome:.5f}")
    print(f"reference  = {ref_tool} ({ref})")
    print(f"EXPOSURE_K = {EXPOSURE_K:.5f}   (dome view mean {sky.mean():.5f}, spread "
          f"{sky.min():.5f}..{sky.max():.5f})")
    print(f"SUN_K      = {sun_k:.5f}")
    print(f"DOME_K     = {dome_k:.5f}")
    print(f"subject pixels: {int(on.sum())} of {on.size}")
    print(f"at factors 1: Unreal / {ref_tool} over the subjects = {both[on].mean() / refl[on].mean():.4f}")
    for name in ("sphere", "cube", "floor"):
        sel = regions[name] & on
        if sel.any():
            print(f"  {name:6s} {ref_tool} {refl[sel].mean():.4f}  Unreal fitted {fit[sel].mean():.4f}  "
                  f"ratio {fit[sel].mean() / refl[sel].mean():.4f}")
    rel = np.abs(fit[on] - refl[on]) / np.maximum(refl[on], 1e-3)
    print(f"fitted relative error over the subjects: median {np.median(rel):.4f}, p95 {np.percentile(rel, 95):.4f}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("job", type=Path)
    ap.add_argument("--calibrate", action="store_true", help="fit the light factors on this (grey card) job")
    ap.add_argument("--ref", default="storm", choices=("storm", "blender"),
                    help="the picture --calibrate fits to (default: storm)")
    a = ap.parse_args(argv)
    try:
        calibrate(a.job, a.ref) if a.calibrate else run(a.job)
    except Unsupported as e:
        raise SystemExit(f"unreal: {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
