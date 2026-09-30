#!/usr/bin/env python3
"""Write the parity rig's CHARACTER scene: ``character_scene.usda`` beside this file (Phase07 7.4).

    uv run tools/parity/scene/build_character.py

The MakeHuman body (CC0), split into one mesh per substance (Phase07 ruling L1), under the
rig's own lights (``build_scene.lights_block``) and three square cameras: the whole body, a
face close-up and a hand close-up. Generated from PINNED sources (URL + sha256, below), fetched
once into ``library/parity/_sources/`` (git-ignored) and verified; the output is committed, so
every tool reads the same bytes, and it is deterministic.

What is in it (Y up, metres, feet on y = 0, facing +Z):

* ``/World/Character/<Part>`` — one mesh per part (``PARTS``). MakeHuman's meshes are in
  decimetres; they are scaled to metres here.
* **st in METRES, like the test scene's subjects.** MakeHuman's UVs are one 0–1 atlas over the
  whole body (hm08): one UV unit spans ~1.7 m of body (Phase07 F13), so an article sized per UV
  tile (skin: 1 cm) would render ~170x too large. Each part's UVs are scaled by its own
  measured density (the median, over its faces, of sqrt(3D area / UV area)) so that 1 UV unit
  = 1 m on that part. A render job then divides by the article's ``meters_per_tile`` exactly as
  for the test scene. This is the rig's stand-in for a "fit" (research CM2): the article is
  unchanged, and the mesh is made to state real-world UVs. The atlas's islands are not all at
  the median density, so detail still varies in size across the body (recorded per part in the
  file's doc string).
* Unbound parts carry a mid-grey ``UsdPreviewSurface`` (``/World/Looks/Unbound``).
"""

from __future__ import annotations

import hashlib
import io
import math
import statistics
import sys
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
OUT = HERE / "character_scene.usda"
CACHE = REPO / "library" / "parity" / "_sources"
sys.path.insert(0, str(HERE))
import build_scene  # noqa: E402

DM = 0.1        # MakeHuman units are decimetres

# Pinned CC0 sources (research 260927_R_CharacterMaterials_MPFB2.md, Pass 3).
SOURCES = {
    "base.obj": {
        "url": "https://raw.githubusercontent.com/makehumancommunity/mpfb2/"
               "3edf9df0551765be43563d047888cf7877eb89b4/src/mpfb/data/3dobjs/base.obj",
        "sha256": "8e761e6624b8f54536409135d1636da63b32486a90d4897f84e121d144f6fb4c",
        "licence": "CC0 (MPFB2 LICENSE.ASSETS.md: the hm08 base mesh)",
    },
    "makehuman_system_assets_cc0.zip": {
        "url": "https://files.makehumancommunity.org/asset_packs/makehuman_system_assets/"
               "makehuman_system_assets_cc0.zip",
        "sha256": "b542127a8e25547c7c29c19f2d1d2adb9a664c80396ecd694095dbc8028a0107",
        "licence": "CC0 (each file's header: 'explicitly released as CC0 in september 2020')",
    },
}
PACK = "makehuman_system_assets_cc0.zip"
_MPFB = "https://raw.githubusercontent.com/makehumancommunity/mpfb2/3edf9df0551765be43563d047888cf7877eb89b4/src/mpfb/data/textures/"
for _mask, _sha in (("lips", "572630c2b4bb061dfd3b5bb75228615527442296b0db40feffffb0d439e8c203"),
                    ("fingernails", "0828222964a14c14a46e72445f549a2124de06f072daab71e5a6716324c37362"),
                    ("toenails", "029404d4efadbfd84cf7a9c9d9b1d93c6ba9b806a85897d52474a6f8edc803a4")):
    SOURCES[f"mpfb_{_mask}.jpg"] = {"url": _MPFB + f"mpfb_{_mask}.jpg", "sha256": _sha,
                                    "licence": "CC0 (MPFB2 LICENSE.ASSETS.md: region masks on hm08's UVs)"}

# One source mesh -> one or more parts (Phase07 ruling L1: one part per substance). A face goes
# to the first split whose rule selects it, else to the mesh's `rest` part. Rules read the face's
# UV centroid: `mask` (an MPFB2 region mask on hm08's UVs, > 50 %), `alpha` (the mesh's own
# MakeHuman texture is transparent there), `circles` (inside any (u, v, r) circle in UV) and
# `red` (the texture's red exceeds green and blue by > 30 levels). `grow` (Phase08 8.3) widens a
# rule's own UV selection by that many rings of neighbouring faces (sharing a vertex): on a
# loop-modelled mesh, whole edge loops.
MESHES = {
    "body": {"group": "body", "rest": "Body",
             "split": [("Lips", {"mask": ["mpfb_lips.jpg"]}),
                       ("Nails", {"mask": ["mpfb_fingernails.jpg", "mpfb_toenails.jpg"]})]},
    # The HIGH-poly eye has an outer shell (the cornea), mapped to a disc of its texture that is
    # fully transparent, so MakeHuman never shows it (Phase07 7.5: the research's "no cornea
    # shell" holds for the low-poly eye only). The iris circles are measured off the texture.
    # Phase09 9.2 (RD-P09-3, RD-P09-4): the sclera, iris and pupil share the eye's picture from the
    # fit set (`fit`, on `fit_parts`) and keep their atlas st; the cornea shell is left out of it
    # (Studio has none: the rig hides it in every view, job.CHARACTER_HIDE_ALWAYS).
    "eyes": {"proxy": "eyes/high-poly/high-poly", "texture": "eyes/materials/brown_eye.png",
             "rest": "Sclera", "fit": "eyes/Brown", "fit_parts": ["Sclera", "Iris", "Pupil"],
             "split": [("Cornea", {"alpha": True}),
                       ("Pupil", {"circles": [(0.705, 0.700, 0.034), (0.290, 0.288, 0.034)]}),
                       ("Iris", {"circles": [(0.705, 0.700, 0.118), (0.290, 0.288, 0.118)]})]},
    "teeth": {"proxy": "teeth/teeth_base/teeth_base", "texture": "teeth/teeth_base/teeth.png",
              "rest": "Teeth", "split": [("Gums", {"red": True})]},
    "tongue": {"proxy": "tongue/tongue01/tongue01", "rest": "Tongue"},
    # Clothing (7.5.2): a T-shirt and jeans on one atlas (the jeans are its lower-left island),
    # and leather shoes. `delete` drops the body faces a garment's .mhclo marks as covered, as
    # MakeHuman does, so the skin cannot show through the cloth.
    "suit": {"proxy": "clothes/female_casualsuit01/female_casualsuit01", "rest": "Shirt", "delete": True,
             # the jeans island, and its waistband corner past u 0.73 (the sleeves there stop at v 0.42)
             "split": [("Trousers", {"rect": [(0.0, 0.0, 0.73, 0.56), (0.73, 0.43, 0.78, 0.56)]})]},
    # Phase08 8.3: the sole is its own part (rubber, not the leather upper), so the rig can judge
    # rubber on a sole. The rig's own copy only; splitting the platform's garments is platform-side
    # (Phase08 §Not now). The underside is its own UV island (u < 0.835, v >= 0.69: 224 faces, all
    # within 2.75 cm of the ground); the sole slab's side is the next FOUR edge loops up from it
    # (44 faces a shoe each; the fifth is the upper), measured 2026-09-28, so its top edge is the
    # mesh's own seam. (A height band was tried first: it cut across the loops in stair-steps
    # and missed the heel.)
    "shoes": {"proxy": "clothes/shoes01/shoes01", "rest": "Shoes", "delete": True,
              "split": [("Soles", {"rect": [(0.0, 0.69, 0.835, 1.0)], "grow": 4})]},
    # Hair, brows and lashes (7.6, ruling L2): cards whose strands are the transparency of their
    # own texture. `cutout` keeps the part's st in the source atlas (the maps are drawn on it).
    # `fit` names the part's entry in the library's FIT SET (Phase09 RD-P09-2, RD-P09-6:
    # `MatterLibrary/textures/fit/makehuman/<fit>_{opacity,basecolor}_sUKN.png`, written by
    # tools/converters/fit/gen_fit_makehuman.py): its cut-out and its picture, which the rig
    # supplies when it binds the article (the article never carries them: D1). The hair is
    # `short02`, Studio's built-in hair (Phase09 RD-P09-4; `bob02` was the one blonde style).
    "hair": {"proxy": "hair/short02/short02", "fit": "hair/Short02", "rest": "Hair", "cutout": True},
    "brows": {"proxy": "eyebrows/eyebrow001/eyebrow001", "fit": "hair/Eyebrow001", "rest": "Brows",
              "cutout": True},
    "lashes": {"proxy": "eyelashes/eyelashes01/eyelashes01", "fit": "hair/Eyelashes01", "rest": "Lashes",
               "cutout": True},
}
FIT = REPO / "MatterLibrary" / "textures" / "fit" / "makehuman"
PARTS = [p for m in MESHES.values() for p in [s for s, _ in m.get("split", [])] + [m["rest"]]]

# Cameras (the rig's 50 mm lens on a 36 mm square), framed from the body's own measured bounds.
CAM_FOCAL, CAM_APERTURE = build_scene.CAM_FOCAL, build_scene.CAM_APERTURE


_VERIFIED: dict[str, bytes] = {}


def source(name: str, member: str | None = None) -> bytes:
    """A pinned source's bytes (or one member of a pinned zip), from the cache or fetched once;
    refused unless the whole file's sha256 matches the pin."""
    if name not in _VERIFIED:
        spec = SOURCES[name]
        path = CACHE / name
        if not path.exists():
            CACHE.mkdir(parents=True, exist_ok=True)
            req = urllib.request.Request(spec["url"], headers={"User-Agent": "matter-library-tools"})
            with urllib.request.urlopen(req, timeout=600) as r:
                path.write_bytes(r.read())
        data = path.read_bytes()
        got = hashlib.sha256(data).hexdigest()
        if got != spec["sha256"]:
            raise SystemExit(f"{name}: sha256 {got} != pinned {spec['sha256']} ({path})")
        _VERIFIED[name] = data
    if member is None:
        return _VERIFIED[name]
    with zipfile.ZipFile(io.BytesIO(_VERIFIED[name])) as z:
        return z.read(member)


def base_vertices(text: str) -> list[tuple[float, float, float]]:
    """Every base-mesh vertex, in MakeHuman units (a proxy's .mhclo indexes these)."""
    return [tuple(float(x) for x in line.split()[1:4]) for line in text.splitlines()
            if line.startswith("v ")]


def deleted_verts(mhclo: str) -> set[int]:
    """The base vertices a proxy's ``delete_verts`` section covers (indices and ``a - b`` ranges)."""
    out, on = set(), False
    for line in mhclo.splitlines():
        p = line.split()
        if not p or p[0].startswith("#"):
            continue
        if p[0] == "delete_verts":
            on = True
            continue
        if on and not p[0].isdigit():
            break
        if on:
            k = 0
            while k < len(p):
                if k + 2 < len(p) and p[k + 1] == "-":
                    out.update(range(int(p[k]), int(p[k + 2]) + 1))
                    k += 3
                else:
                    out.add(int(p[k]))
                    k += 1
    return out


def fit_proxy(mhclo: str, base: list) -> list[tuple[float, float, float]]:
    """A MakeHuman proxy's vertices, fitted to the base mesh (metres).

    Each ``verts`` line is ``v`` (exactly that base vertex) or ``v1 v2 v3 w1 w2 w3 dx dy dz``:
    the weighted sum of three base vertices plus an offset, the offset scaled per axis by the
    ``<axis>_scale a b ref`` lines (|base[a] - base[b]| along that axis / ref). MakeHuman's own
    proxy fitting; on the default body the scales are ~1.
    """
    scale, out, in_verts = [1.0, 1.0, 1.0], [], False
    for line in mhclo.splitlines():
        p = line.split()
        if not p or p[0].startswith("#"):
            continue
        if p[0] in ("x_scale", "y_scale", "z_scale"):
            ax = "xyz".index(p[0][0])
            a, b, ref = int(p[1]), int(p[2]), float(p[3])
            scale[ax] = abs(base[a][ax] - base[b][ax]) / ref
        elif p[0] == "verts":
            in_verts = True
        elif in_verts and len(p) == 1 and p[0].isdigit():
            out.append(base[int(p[0])])
        elif in_verts and len(p) == 9:
            v = [int(x) for x in p[:3]]
            w = [float(x) for x in p[3:6]]
            d = [float(x) for x in p[6:9]]
            out.append(tuple(sum(w[i] * base[v[i]][ax] for i in range(3)) + d[ax] * scale[ax]
                             for ax in range(3)))
        elif in_verts and out:
            in_verts = False        # the next section (e.g. delete_verts)
        # (a key line between `verts 0` and the first vertex, e.g. bob01's `material`, is skipped)
    return [(x * DM, y * DM, z * DM) for x, y, z in out]


def read_obj(text: str, group: str | None):
    """Points (metres), faces as [(vertex index, uv index)], uvs, and each point's index in the
    file — only the kept group's."""
    v, vt, faces, g = [], [], [], None
    for line in text.splitlines():
        p = line.split()
        if not p:
            continue
        if p[0] == "v":
            v.append(tuple(float(x) * DM for x in p[1:4]))
        elif p[0] == "vt":
            vt.append((float(p[1]), float(p[2])))
        elif p[0] == "g":
            g = p[1] if len(p) > 1 else None
        elif p[0] == "f" and (group is None or g == group):
            face = []
            for c in p[1:]:
                parts = c.split("/")
                face.append((int(parts[0]) - 1, int(parts[1]) - 1 if len(parts) > 1 and parts[1] else -1))
            faces.append(face)
    # keep only the vertices the kept faces use, in first-use order (deterministic)
    remap, pts, src = {}, [], []
    for f in faces:
        for vi, _ in f:
            if vi not in remap:
                remap[vi] = len(pts)
                pts.append(v[vi])
                src.append(vi)
    return pts, [[(remap[vi], ti) for vi, ti in f] for f in faces], vt, src


def _cross(u, w):
    return (u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0])


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def face_normal(pts, f):
    """Area-weighted (unnormalized) normal of a polygon (fan)."""
    n = [0.0, 0.0, 0.0]
    p0 = pts[f[0][0]]
    for i in range(1, len(f) - 1):
        c = _cross(_sub(pts[f[i][0]], p0), _sub(pts[f[i + 1][0]], p0))
        n = [n[k] + c[k] for k in range(3)]
    return n


def vertex_normals(pts, faces):
    acc = [[0.0, 0.0, 0.0] for _ in pts]
    for f in faces:
        n = face_normal(pts, f)
        for vi, _ in f:
            acc[vi] = [acc[vi][k] + n[k] for k in range(3)]
    out = []
    for a in acc:
        L = math.sqrt(sum(x * x for x in a)) or 1.0
        out.append((a[0] / L, a[1] / L, a[2] / L))
    return out


def uv_density(pts, faces, vt) -> tuple[float, float, float]:
    """Metres of surface per UV unit: (p5, median, p95) over the faces' sqrt(3D area / UV area)."""
    r = []
    for f in faces:
        a3 = 0.5 * math.sqrt(sum(x * x for x in face_normal(pts, f)))
        uv = [vt[ti] for _, ti in f]
        a2 = abs(sum(uv[i][0] * uv[(i + 1) % len(uv)][1] - uv[(i + 1) % len(uv)][0] * uv[i][1]
                     for i in range(len(uv)))) / 2
        if a2 > 1e-12 and a3 > 0:
            r.append(math.sqrt(a3 / a2))
    r.sort()
    return r[int(0.05 * (len(r) - 1))], statistics.median(r), r[int(0.95 * (len(r) - 1))]


def _image(data: bytes):
    from PIL import Image          # noqa: PLC0415 (only the build needs it)
    im = Image.open(io.BytesIO(data)).convert("RGBA")
    return im.size, im.load()


def _grown(faces, vt, rects, rings: int) -> set[int]:
    """The faces whose UV centroid is in `rects`, widened by `rings` rings of faces sharing a vertex."""
    sel = set()
    for i, f in enumerate(faces):
        u = statistics.mean(vt[t][0] for _, t in f)
        v = statistics.mean(vt[t][1] for _, t in f)
        if any(u0 <= u < u1 and v0 <= v < v1 for u0, v0, u1, v1 in rects):
            sel.add(i)
    by_v: dict[int, set[int]] = {}
    for i, f in enumerate(faces):
        for vi, _ in f:
            by_v.setdefault(vi, set()).add(i)
    front = set(sel)
    for _ in range(rings):
        front = {j for i in front for vi, _ in faces[i] for j in by_v[vi]} - sel
        sel |= front
    return sel


def split_faces(spec: dict, faces, vt) -> dict[str, list[int]]:
    """Face indices per part: the first split rule that selects a face wins, else `rest`."""
    rules = spec.get("split", [])
    grown = {name: _grown(faces, vt, rule["rect"], rule["grow"]) for name, rule in rules if "grow" in rule}
    imgs = {}
    for _, rule in rules:
        for m in rule.get("mask", []):
            imgs.setdefault(m, _image(source(m)))
    tex = _image(source(PACK, spec["texture"])) if "texture" in spec else None

    def at(img, u, v):
        (W, H), px = img
        return px[min(W - 1, int((u % 1.0) * W)), min(H - 1, int((1 - v % 1.0) * H))]

    out = {name: [] for name, _ in rules}
    out[spec["rest"]] = []
    for i, f in enumerate(faces):
        u = statistics.mean(vt[t][0] for _, t in f)
        v = statistics.mean(vt[t][1] for _, t in f)
        for name, rule in rules:
            if "mask" in rule and any(at(imgs[m], u, v)[0] > 127 for m in rule["mask"]):
                break
            if rule.get("alpha") and at(tex, u, v)[3] < 128:
                break
            if "circles" in rule and any(math.hypot(u - cu, v - cv) < r for cu, cv, r in rule["circles"]):
                break
            if "rect" in rule and any(u0 <= u < u1 and v0 <= v < v1 for u0, v0, u1, v1 in rule["rect"]):
                break
            if "grow" in rule and i in grown[name]:
                break
            if rule.get("red"):
                r, g, b, _ = at(tex, u, v)
                if r > g + 30 and r > b + 30:
                    break
        else:
            name = spec["rest"]
        out[name].append(i)
    return out


def subset(pts, normals, faces):
    """The points, normals and faces of a face subset, re-indexed in first-use order."""
    remap, p_pts, p_nrm = {}, [], []
    for f in faces:
        for vi, _ in f:
            if vi not in remap:
                remap[vi] = len(p_pts)
                p_pts.append(pts[vi])
                p_nrm.append(normals[vi])
    return p_pts, p_nrm, [[(remap[vi], ti) for vi, ti in f] for f in faces]


def load_parts() -> dict:
    """Every part: points, normals, faces, faceVarying st in metres, and its UV density."""
    base_text = source("base.obj").decode("utf-8", "replace")
    base = base_vertices(base_text)
    # the body faces the garments cover, as MakeHuman removes them (any deleted vertex)
    covered = set()
    for spec in MESHES.values():
        if spec.get("delete"):
            covered |= deleted_verts(source(PACK, spec["proxy"] + ".mhclo").decode("utf-8", "replace"))
    parts = {}
    for key, spec in MESHES.items():
        if "group" in spec:
            pts, faces, vt, src = read_obj(base_text, spec["group"])
            if covered:
                faces = [f for f in faces if not any(src[vi] in covered for vi, _ in f)]
                pts, _, faces = subset(pts, pts, faces)
        else:
            obj = source(PACK, spec["proxy"] + ".obj").decode("utf-8", "replace")
            fitted = fit_proxy(source(PACK, spec["proxy"] + ".mhclo").decode("utf-8", "replace"), base)
            _, faces, vt, src = read_obj(obj, None)
            n_obj = sum(1 for line in obj.splitlines() if line.startswith("v "))
            if n_obj != len(fitted):
                raise SystemExit(f"{key}: the .obj has {n_obj} vertices, the .mhclo fits {len(fitted)}")
            pts = [fitted[vi] for vi in src]
        normals = vertex_normals(pts, faces)        # over the whole mesh: no crease at a split
        for name, sel in split_faces(spec, faces, vt).items():
            if not sel:
                raise SystemExit(f"part {name!r}: its rule selected no faces")
            p_pts, p_nrm, p_faces = subset(pts, normals, [faces[i] for i in sel])
            d = uv_density(p_pts, p_faces, vt)
            k = 1.0 if name in _fit_parts(spec) else d[1]     # a fit part keeps its atlas
            st = [(vt[ti][0] * k, vt[ti][1] * k) for f in p_faces for _, ti in f]
            parts[name] = {"points": p_pts, "normals": p_nrm, "faces": p_faces, "st": st, "density": d,
                           "cutout": bool(spec.get("cutout"))}     # a card: doubleSided
    # feet on the ground: shift every part by the lowest point of all of them
    y0 = min(p[1] for part in parts.values() for p in part["points"])
    for part in parts.values():
        part["points"] = [(x, y - y0, z) for x, y, z in part["points"]]
    return parts


def _f3(vs):
    return ", ".join(f"({x:.5f}, {y:.5f}, {z:.5f})" for x, y, z in vs)


def _f2(vs):
    return ", ".join(f"({s:.5f}, {t:.5f})" for s, t in vs)


def mesh_block(name: str, part: dict) -> str:
    i = "        "
    counts = ", ".join(str(len(f)) for f in part["faces"])
    flat = ", ".join(str(vi) for f in part["faces"] for vi, _ in f)
    return (
        f'{i}def Mesh "{name}" (\n{i}    prepend apiSchemas = ["MaterialBindingAPI"]\n{i})\n{i}{{\n'
        f'{i}    uniform token subdivisionScheme = "none"\n'
        # cards are seen from both sides (MakeHuman's .mhmat: backfaceCull False)
        + (f'{i}    uniform bool doubleSided = 1\n' if part.get("cutout") else "") +
        f'{i}    point3f[] points = [{_f3(part["points"])}]\n'
        f'{i}    normal3f[] normals = [{_f3(part["normals"])}] (\n{i}        interpolation = "vertex"\n{i}    )\n'
        f'{i}    int[] faceVertexCounts = [{counts}]\n'
        f'{i}    int[] faceVertexIndices = [{flat}]\n'
        f'{i}    texCoord2f[] primvars:st = [{_f2(part["st"])}] (\n{i}        interpolation = "faceVarying"\n{i}    )\n'
        f'{i}    rel material:binding = </World/Looks/Unbound>\n'
        f'{i}}}\n')


def _look_at(pos, target):
    """(pitch, yaw) in degrees, rotateXYZ X then Y, for a camera looking down -Z at target."""
    dx, dy, dz = (target[k] - pos[k] for k in range(3))
    yaw = math.degrees(math.atan2(-dx, -dz))
    pitch = math.degrees(math.atan2(dy, math.hypot(dx, dz)))
    return pitch, yaw


def cameras(parts: dict) -> dict:
    """Framings from the parts' bounds: whole body, face, the character's left hand, the mouth
    (teeth, gums and tongue; the rig hides the face for that view)."""
    pts = parts["Body"]["points"]
    top = max(p[1] for p in pts)
    half = math.tan(math.atan(CAM_APERTURE / 2 / CAM_FOCAL))   # half-width per metre of distance
    cams = {}
    # whole body: frame the height + 10 %
    h = top * 1.1
    cams["Cam"] = ((0.0, top / 2, h / 2 / half), (0.0, top / 2, 0.0))
    # face: the front-most points in the top 12 % of the height, framed 0.30 m
    head = [p for p in pts if p[1] > top * 0.88]
    fz = max(p[2] for p in head)
    face = (0.0, statistics.median(p[1] for p in head) - 0.02, fz - 0.08)
    cams["CamFace"] = ((face[0] + 0.05, face[1] + 0.03, face[2] + 0.15 / half), face)
    # hand: the points within 12 cm of the extreme +x point (the character's left hand)
    xmax = max(p[0] for p in pts)
    hand = [p for p in pts if p[0] > xmax - 0.12]
    hc = tuple((min(p[k] for p in hand) + max(p[k] for p in hand)) / 2 for k in range(3))
    cams["CamHand"] = ((hc[0] + 0.02, hc[1] + 0.02, hc[2] + 0.17 / half), hc)
    mouth = [p for n in ("Teeth", "Gums", "Tongue") for p in parts[n]["points"]]
    mc = tuple((min(p[k] for p in mouth) + max(p[k] for p in mouth)) / 2 for k in range(3))
    cams["CamMouth"] = ((mc[0], mc[1] - 0.02, mc[2] + 0.06 / half), mc)
    # waist: where the shirt's hem meets the jeans' waistband, framed 0.36 m
    hem = max(p[1] for p in parts["Trousers"]["points"])
    band = [p for p in parts["Trousers"]["points"] if p[1] > hem - 0.08]
    wc = (0.0, hem - 0.04, max(p[2] for p in band) - 0.04)
    cams["CamWaist"] = ((wc[0] + 0.06, wc[1] + 0.05, wc[2] + 0.18 / half), wc)
    # feet: both shoes, framed 0.40 m, from the front and a little above
    sp = parts["Shoes"]["points"] + parts["Soles"]["points"]     # the whole shoe (8.3 split)
    fc =tuple((min(p[k] for p in sp) + max(p[k] for p in sp)) / 2 for k in range(3))
    cams["CamFeet"] = ((fc[0], fc[1] + 0.20, fc[2] + 0.20 / half), fc)
    return cams


def camera_block(name: str, pos, target) -> str:
    pitch, yaw = _look_at(pos, target)
    x, y, z = pos
    return (f'    def Camera "{name}"\n    {{\n'
            f'        float focalLength = {CAM_FOCAL}\n'
            f'        float horizontalAperture = {CAM_APERTURE}\n'
            f'        float verticalAperture = {CAM_APERTURE}\n'
            '        float2 clippingRange = (0.02, 100)\n'
            f'        double3 xformOp:translate = ({x:.4f}, {y:.4f}, {z:.4f})\n'
            f'        float3 xformOp:rotateXYZ = ({pitch:.3f}, {yaw:.3f}, 0)\n'
            '        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ"]\n    }\n')


def build(parts: dict) -> str:
    dens = "\n".join(f"    {n}: 1 UV unit = {p['density'][1]:.3f} m (p5 {p['density'][0]:.3f}, "
                     f"p95 {p['density'][2]:.3f})" for n, p in parts.items())
    srcs = "\n".join(f"    {k}: {s['url']} sha256 {s['sha256']}" for k, s in SOURCES.items())
    out = [
        '#usda 1.0\n(\n    """\n'
        "    The Matter parity rig's CHARACTER scene (generated by build_character.py; do not hand-edit).\n"
        "    The CC0 MakeHuman body, one mesh per substance. st is in METRES per part (source UVs x the\n"
        "    part's median density); a render job rescales st by the article's meters_per_tile.\n"
        "    Hair, Brows, Lashes, Sclera, Iris and Pupil keep their source atlas st: their fit-set\n"
        "    maps (MatterLibrary/textures/fit/makehuman/) are drawn on it.\n"
        f"{dens}\n    Sources (CC0):\n{srcs}\n"
        '    """\n'
        f'    defaultPrim = "World"\n    upAxis = "{build_scene.UP_AXIS}"\n'
        f'    metersPerUnit = {build_scene.METERS_PER_UNIT}\n)\n\n'
        'def Xform "World"\n{\n',
        build_scene.lights_block(f"./{build_scene.DOME_TEX}"),
        '    def Scope "Looks"\n    {\n',
        build_scene.preview_material("Unbound", color=0.18, roughness=0.6),
        '    }\n',
        '    def Xform "Character"\n    {\n',
    ]
    out += [mesh_block(n, p) for n, p in parts.items()]
    out.append('    }\n')
    out += [camera_block(n, pos, tgt) for n, (pos, tgt) in cameras(parts).items()]
    out.append('}\n')
    return "".join(out)


def part_uvs() -> dict[str, list[tuple[float, float]]]:
    """Each part's faceVarying st in metres, keyed by prim path (a job divides by meters_per_tile).
    A cut-out part's st is its source atlas instead (``cutout_maps``)."""
    return {f"/World/Character/{n}": p["st"] for n, p in load_parts().items()}


def _fit_parts(spec: dict) -> list[str]:
    """The parts of a mesh that carry its fit-set maps, on their source atlas st."""
    return (spec.get("fit_parts") or [spec["rest"]]) if spec.get("fit") else []


def atlas_parts() -> set[str]:
    """The prims whose st is their source atlas (the fit parts): a job neither rescales it by the
    article's ``meters_per_tile`` nor lets the article's UV placement move the maps drawn on it.
    The ONE copy of the rule (Phase09 F-P09-15): ``job.py`` and ``drivers/unreal.py`` read it."""
    return {f"/World/Character/{p}" for spec in MESHES.values() for p in _fit_parts(spec)}


def cutout_maps() -> dict[str, Path]:
    """Each cut-out part's map, keyed by prim path: the fit set's ``opacity`` (one channel; MaterialX
    reads a float image's FIRST channel), drawn on the part's atlas."""
    return {f"/World/Character/{spec['rest']}": FIT / f"{spec['fit']}_opacity_sUKN.png"
            for spec in MESHES.values() if spec.get("cutout")}


def base_color_maps() -> dict[str, Path]:
    """Each fit part's picture, keyed by prim path: the fit set's ``basecolor`` (Phase09
    ``base_color_map``): a card's strands, or the eye's picture on the sclera, iris and pupil."""
    return {f"/World/Character/{p}": FIT / f"{spec['fit']}_basecolor_sUKN.png"
            for spec in MESHES.values() for p in _fit_parts(spec)}


def mesh_maps() -> dict[str, dict[str, Path]]:
    """Every map the mesh supplies at binding, by prim path, then by the article's input name."""
    out: dict[str, dict[str, Path]] = {}
    for port, maps in (("cutout_map", cutout_maps()), ("base_color_map", base_color_maps())):
        for prim, path in maps.items():
            out.setdefault(prim, {})[port] = path
    return out



def main(argv=None) -> int:
    """``--hair <style> --out <path>``: the same character in another MakeHuman hairstyle (a lead's
    sitting, Phase09 click 1), written elsewhere; the rig's committed scene stays ``short02``."""
    import argparse  # noqa: PLC0415
    ap = argparse.ArgumentParser(description="Write the parity rig's character scene.")
    ap.add_argument("--hair", help="a MakeHuman hairstyle (e.g. bob01) instead of short02")
    ap.add_argument("--out", type=Path, default=OUT)
    args = ap.parse_args(argv)
    if args.hair:
        if args.out == OUT:
            raise SystemExit("--hair writes a variant: give it an --out other than the rig's scene")
        style = args.hair.lower()
        MESHES["hair"] = dict(MESHES["hair"], proxy=f"hair/{style}/{style}",
                              fit=f"hair/{style[:1].upper()}{style[1:]}")
    parts = load_parts()
    out = args.out
    out.write_text(build(parts), encoding="utf-8")
    if out != OUT:
        print(f"wrote {out}")
        return 0
    for n, p in parts.items():
        print(f"{n}: {len(p['points'])} points, {len(p['faces'])} faces, "
              f"1 UV unit = {p['density'][1]:.3f} m (p5 {p['density'][0]:.3f}, p95 {p['density'][2]:.3f})")
    print(f"wrote {OUT} ({OUT.stat().st_size / 1e6:.1f} MB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
