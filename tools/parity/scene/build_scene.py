#!/usr/bin/env python3
"""Write the parity rig's ONE test scene: ``test_scene.usda`` beside this file.

    uv run tools/parity/scene/build_scene.py

The scene is generated (the meshes are arrays) but committed, so every tool reads the same
bytes. Re-run this only when the scene itself changes; the output is deterministic.

What is in it (Y up, metres, 1 unit = 1 m):

* ``/World/Subjects/{Sphere,Cube,Floor}`` — the three meshes the article under test is
  bound to: a 0.18 m-radius sphere, a 0.30 m rounded cube and a 1 m x 1 m floor. Their
  ``primvars:st`` are in METRES (1 UV unit = 1 m). A render job rescales them by the
  article's ``meters_per_tile`` (``subject_uvs``) so every article shows at its real size.
* ``/World/Ruler`` — a 10 cm ruler of ten 1 cm black and white cells on the floor.
* ``/World/Wall`` — a UV-grid wall behind the objects (1 m tiles), so see-through
  materials have something to show.
* ``/World/Lights/{Dome,Sun}`` — a white dome (no texture) and one distant light.
* ``/World/Cam`` — the fixed square camera on the whole set (the "wide" view), and
  ``/World/CamClose`` — a close-up on the cube's front face and the floor (the "close"
  view), where wear layers are big enough to see.

The furniture (ruler, wall) uses ``UsdPreviewSurface``, which every tool imports natively.
"""

from __future__ import annotations

import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "test_scene.usda"
UVGRID = "../../../MatterLibrary/textures/base/utility/virtual/UVGrid_basecolor_s1.png"

SPHERE_R, SPHERE_C = 0.18, (-0.24, 0.18, 0.02)
CUBE_H, CUBE_R, CUBE_C = 0.15, 0.025, (0.24, 0.15, -0.02)
FLOOR = 1.0
RULER_Z, RULER_W = 0.40, 0.01
WALL_Z, WALL_W, WALL_Y0, WALL_Y1 = -0.60, 2.4, -0.8, 1.6

# The camera: a square frame on the three subjects.
CAM_POS = (0.0, 0.48, 1.95)
CAM_PITCH = -11.0          # degrees about X (looking down)
CAM_FOCAL, CAM_APERTURE = 50.0, 36.0

# The close-up: ~0.5 m from the cube's front face, taking in its top edge and the floor in
# front, a frame ~0.35 m wide. At 512 px that is ~0.7 mm per pixel, so a 1 cm dust grain is
# ~15 px; in the wide shot it is ~1 px, which is why the wear could not be seen there
# (5.2 sitting). Rotation is (pitch about X, yaw about Y), applied X then Y.
CLOSE_POS = (0.10, 0.34, 0.58)
CLOSE_ROT = (-20.2, -12.5)
CAMERAS = {"wide": "/World/Cam", "close": "/World/CamClose"}

# Light values are the Storm (USD) values. The Blender driver maps them with measured
# factors (drivers/blender_render.py); the scene is the single source of the numbers.
#
# Two Storm facts make these lights work at all (measured, Phase05 5.1; before this, the
# preview scene's lights contributed NOTHING and every render was lit by usdrecord's
# camera headlight):
#   * a DistantLight's intensity is the sun DISK's radiance unless `normalize = true`
#     (hdSt/light.cpp multiplies it by the 0.53-degree disk's solid angle, ~6.7e-5 sr), so
#     the sun is normalized: its intensity is then the irradiance, like Blender's strength;
#   * Storm ignores a DomeLight with no texture ("Dome light has no texture asset path"),
#     so the dome carries DOME_TEX, a constant-white environment written by this script.
#     It is an 8-bit PNG (255 = radiance 1.0): a hand-written flat Radiance .hdr was
#     MISREAD by Storm (visible dome 0.36-0.52 and uneven, dome light ~56%), while the
#     white PNG reads exactly 1.0 (measured, Phase05 5.1).
DOME_INTENSITY = 1.0
DOME_TEX = "white_env.png"
SUN_INTENSITY = 3.0
SUN_ROTATE = (-40.0, 35.0, 0.0)
SUN_ANGLE = 0.53


# ---------------------------------------------------------------- mesh builders

def sphere(seg_u: int = 96, seg_v: int = 48):
    """UV sphere; st in metres along the surface (u around the equator, v pole to pole)."""
    r, (cx, cy, cz) = SPHERE_R, SPHERE_C
    pts, nrm, uvs, idx = [], [], [], []
    for j in range(seg_v + 1):
        for i in range(seg_u + 1):
            u, v = i / seg_u, j / seg_v
            th, ph = u * 2 * math.pi, v * math.pi
            n = (math.sin(ph) * math.cos(th), math.cos(ph), -math.sin(ph) * math.sin(th))
            nrm.append(n)
            pts.append((cx + r * n[0], cy + r * n[1], cz + r * n[2]))
            uvs.append((u * 2 * math.pi * r, (1 - v) * math.pi * r))
    for j in range(seg_v):
        for i in range(seg_u):
            a = j * (seg_u + 1) + i
            b = a + seg_u + 1
            idx.append((a, b, b + 1, a + 1))
    return pts, nrm, uvs, idx


def _bevel_coords(h: float, r: float, arc: int = 6, flat: int = 6) -> list[float]:
    """1-D grid for one cube face axis: dense across the bevels, sparse on the flat."""
    edge = h - r
    out = [-h + r * (1 - math.cos(0.5 * math.pi * k / arc)) for k in range(arc)]
    out += [-edge + 2 * edge * k / flat for k in range(flat + 1)]
    out += [h - r * (1 - math.cos(0.5 * math.pi * k / arc)) for k in range(arc - 1, -1, -1)]
    return out


def rounded_cube():
    """Six gridded faces pushed onto a rounded box; st is box-mapped in metres per face."""
    h, r, (cx, cy, cz) = CUBE_H, CUBE_R, CUBE_C
    g = _bevel_coords(h, r)
    n = len(g)
    faces = [  # (normal axis, sign, u axis, v axis)
        (2, 1, 0, 1), (2, -1, 0, 1), (0, 1, 2, 1), (0, -1, 2, 1), (1, 1, 0, 2), (1, -1, 0, 2)]
    pts, nrm, uvs, idx = [], [], [], []
    for ax, sg, ua, va in faces:
        base = len(pts)
        for j in range(n):
            for i in range(n):
                p = [0.0, 0.0, 0.0]
                p[ax], p[ua], p[va] = sg * h, g[i], g[j]
                q = [max(-(h - r), min(h - r, c)) for c in p]
                d = [p[k] - q[k] for k in range(3)]
                ln = math.sqrt(sum(c * c for c in d)) or 1.0
                d = [c / ln for c in d]
                pts.append((cx + q[0] + r * d[0], cy + q[1] + r * d[1], cz + q[2] + r * d[2]))
                nrm.append(tuple(d))
                # face-local st, so each face reads the right way round seen from outside
                su = g[i] * {2: sg, 0: -sg, 1: 1}[ax]
                sv = -g[j] if (ax == 1 and sg > 0) else g[j]
                uvs.append((su + h, sv + h))
        for j in range(n - 1):
            for i in range(n - 1):
                a, b = base + j * n + i, base + (j + 1) * n + i
                quad = (a, a + 1, b + 1, b)
                # u x v points along +Z for the Z faces and against the axis for X and Y;
                # flip where that disagrees with the face's outward sign (USD: CCW = front)
                idx.append(quad if (sg > 0) == (ax == 2) else quad[::-1])
    return pts, nrm, uvs, idx


def floor():
    s = FLOOR / 2
    pts = [(-s, 0.0, s), (s, 0.0, s), (s, 0.0, -s), (-s, 0.0, -s)]
    uvs = [(0.0, 0.0), (FLOOR, 0.0), (FLOOR, FLOOR), (0.0, FLOOR)]
    return pts, [(0.0, 1.0, 0.0)] * 4, uvs, [(0, 1, 2, 3)]


def wall():
    s = WALL_W / 2
    pts = [(-s, WALL_Y0, WALL_Z), (s, WALL_Y0, WALL_Z), (s, WALL_Y1, WALL_Z), (-s, WALL_Y1, WALL_Z)]
    uvs = [(0.0, 0.0), (WALL_W, 0.0), (WALL_W, WALL_Y1 - WALL_Y0), (0.0, WALL_Y1 - WALL_Y0)]
    return pts, [(0.0, 0.0, 1.0)] * 4, uvs, [(0, 1, 2, 3)]


def ruler(black: bool):
    """Ten 1 cm cells from x = -5 cm to +5 cm; even cells black, odd cells white."""
    pts, idx = [], []
    y, z0, z1 = 0.0008, RULER_Z - RULER_W / 2, RULER_Z + RULER_W / 2
    for k in range(10):
        if (k % 2 == 0) != black:
            continue
        x0, x1 = -0.05 + k * 0.01, -0.05 + (k + 1) * 0.01
        b = len(pts)
        pts += [(x0, y, z1), (x1, y, z1), (x1, y, z0), (x0, y, z0)]
        idx.append((b, b + 1, b + 2, b + 3))
    uvs = [(0.0, 0.0)] * len(pts)
    return pts, [(0.0, 1.0, 0.0)] * len(pts), uvs, idx


# ---------------------------------------------------------------- usda writer

def _f3(vs):
    return ", ".join(f"({x:.6f}, {y:.6f}, {z:.6f})" for x, y, z in vs)


def _f2(vs):
    return ", ".join(f"({s:.6f}, {t:.6f})" for s, t in vs)


def mesh_block(name: str, mesh, material: str | None, indent: str = "        ") -> str:
    pts, nrm, uvs, idx = mesh
    counts = ", ".join(str(len(f)) for f in idx)
    flat = ", ".join(str(i) for f in idx for i in f)
    bind = (f'{indent}    rel material:binding = <{material}>\n' if material else "")
    api = ' (\n' + f'{indent}    prepend apiSchemas = ["MaterialBindingAPI"]\n{indent})' if material else ""
    return (
        f'{indent}def Mesh "{name}"{api}\n{indent}{{\n'
        f'{indent}    uniform token subdivisionScheme = "none"\n'
        f'{indent}    point3f[] points = [{_f3(pts)}]\n'
        f'{indent}    normal3f[] normals = [{_f3(nrm)}] (\n{indent}        interpolation = "vertex"\n{indent}    )\n'
        f'{indent}    int[] faceVertexCounts = [{counts}]\n'
        f'{indent}    int[] faceVertexIndices = [{flat}]\n'
        f'{indent}    texCoord2f[] primvars:st = [{_f2(uvs)}] (\n{indent}        interpolation = "vertex"\n{indent}    )\n'
        f'{bind}{indent}}}\n')


def preview_material(name: str, color=None, texture: str | None = None,
                     roughness: float = 0.9) -> str:
    i = "            "
    if texture:
        diffuse = f'{i}    color3f inputs:diffuseColor.connect = </World/Looks/{name}/Tex.outputs:rgb>\n'
        tex = (f'{i}def Shader "Tex"\n{i}{{\n'
               f'{i}    uniform token info:id = "UsdUVTexture"\n'
               f'{i}    asset inputs:file = @{texture}@\n'
               f'{i}    token inputs:sourceColorSpace = "sRGB"\n'
               f'{i}    token inputs:wrapS = "repeat"\n{i}    token inputs:wrapT = "repeat"\n'
               f'{i}    float2 inputs:st.connect = </World/Looks/{name}/St.outputs:result>\n'
               f'{i}    float3 outputs:rgb\n{i}}}\n'
               f'{i}def Shader "St"\n{i}{{\n'
               f'{i}    uniform token info:id = "UsdPrimvarReader_float2"\n'
               f'{i}    string inputs:varname = "st"\n{i}    float2 outputs:result\n{i}}}\n')
    else:
        diffuse = f'{i}    color3f inputs:diffuseColor = ({color:.4f}, {color:.4f}, {color:.4f})\n'
        tex = ""
    return (
        f'        def Material "{name}"\n        {{\n'
        f'            token outputs:surface.connect = </World/Looks/{name}/Surface.outputs:surface>\n'
        f'{i}def Shader "Surface"\n{i}{{\n'
        f'{i}    uniform token info:id = "UsdPreviewSurface"\n'
        f'{diffuse}'
        f'{i}    float inputs:roughness = {roughness}\n'
        f'{i}    float inputs:metallic = 0\n'
        f'{i}    token outputs:surface\n{i}}}\n'
        f'{tex}        }}\n')


def build() -> str:
    parts = [
        '#usda 1.0\n(\n    """\n'
        '    The Matter parity rig\'s ONE test scene (generated by build_scene.py; do not hand-edit).\n'
        '    Subjects carry st in METRES; a render job rescales st by the article\'s meters_per_tile.\n'
        '    """\n'
        '    defaultPrim = "World"\n    upAxis = "Y"\n    metersPerUnit = 1.0\n)\n\n'
        'def Xform "World"\n{\n',
        '    def Scope "Lights"\n    {\n'
        f'        def DomeLight "Dome"\n        {{\n            float inputs:intensity = {DOME_INTENSITY}\n'
        f'            asset inputs:texture:file = @./{DOME_TEX}@\n'
        '            token inputs:texture:format = "latlong"\n        }\n'
        f'        def DistantLight "Sun"\n        {{\n'
        f'            float inputs:intensity = {SUN_INTENSITY}\n'
        '            bool inputs:normalize = true\n'
        f'            float inputs:angle = {SUN_ANGLE}\n'
        f'            float3 xformOp:rotateXYZ = ({SUN_ROTATE[0]}, {SUN_ROTATE[1]}, {SUN_ROTATE[2]})\n'
        '            uniform token[] xformOpOrder = ["xformOp:rotateXYZ"]\n        }\n    }\n',
        '    def Scope "Looks"\n    {\n',
        preview_material("UVGrid", texture=UVGRID, roughness=0.8),
        preview_material("RulerBlack", color=0.02),
        preview_material("RulerWhite", color=0.8),
        '    }\n',
        '    def Xform "Subjects"\n    {\n',
        mesh_block("Sphere", sphere(), None),
        mesh_block("Cube", rounded_cube(), None),
        mesh_block("Floor", floor(), None),
        '    }\n',
        '    def Xform "Ruler"\n    {\n',
        mesh_block("Black", ruler(True), "/World/Looks/RulerBlack"),
        mesh_block("White", ruler(False), "/World/Looks/RulerWhite"),
        '    }\n',
        mesh_block("Wall", wall(), "/World/Looks/UVGrid", indent="    "),
        camera_block("Cam", CAM_POS, (CAM_PITCH, 0.0)),
        camera_block("CamClose", CLOSE_POS, CLOSE_ROT),
        '}\n',
    ]
    return "".join(parts)


def camera_block(name: str, pos, rot) -> str:
    x, y, z = pos
    return (f'    def Camera "{name}"\n    {{\n'
            f'        float focalLength = {CAM_FOCAL}\n'
            f'        float horizontalAperture = {CAM_APERTURE}\n'
            f'        float verticalAperture = {CAM_APERTURE}\n'
            '        float2 clippingRange = (0.02, 100)\n'
            f'        double3 xformOp:translate = ({x}, {y}, {z})\n'
            f'        float3 xformOp:rotateXYZ = ({rot[0]}, {rot[1]}, 0)\n'
            '        uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ"]\n    }\n')


SUBJECTS = ("/World/Subjects/Sphere", "/World/Subjects/Cube", "/World/Subjects/Floor")


def subject_uvs() -> dict[str, list[tuple[float, float]]]:
    """The subjects' st in metres, keyed by prim path (a job divides by meters_per_tile)."""
    return {SUBJECTS[0]: sphere()[2], SUBJECTS[1]: rounded_cube()[2], SUBJECTS[2]: floor()[2]}


def main() -> int:
    from PIL import Image
    OUT.write_text(build(), encoding="utf-8")
    Image.new("RGB", (64, 32), (255, 255, 255)).save(HERE / DOME_TEX, optimize=True)
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
