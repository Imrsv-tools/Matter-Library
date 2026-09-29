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
  from that ``st``. Metres are honoured by construction (JOB_FORMAT.md §Units).
* **the material** of each setting: the article read by the one shared reader
  (``blender/masters/article.py``), its values set on its master under the article's names
  (Phase06 D5), with the setting's sliders applied as a Creator would.
* **the views** from the scene's cameras (translate, then rotateXYZ: X first), 50 mm on a
  36 mm square aperture; **the lights** from the scene's numbers, times the calibration below.

The runtime writes linear scene colour (before the tonemapper, exposure fixed); this driver
applies the view's ``exposure``, box-filters the supersampling and does the plain sRGB encode,
as Storm's and Blender's columns are encoded (Phase06 D8).

Where the runtime comes from, first found wins: ``$MATTER_UNREAL_RUNTIME`` (a packaged build's
launcher), then editor mode, ``$MATTER_UNREAL_EDITOR`` (an Unreal 5.8 ``UnrealEditor``) on
``unreal/MatterRuntime``. ``find_runtime()`` returns None when there is none, and the rig then
skips the column with a notice.
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
EXPOSURE_K = 1.0         # Unreal's scene colour for a radiance of 1 (read off the visible dome)
SUN_K = 1.0
DOME_K = 1.0

# The masters this runtime has, and what of an article each one can carry so far. An article
# needing more is refused by name, so the rig shows "not yet" instead of a wrong picture.
BUILT_MASTERS = {"Opaque"}
TEXTURE_ROLES = {"base_color"}
SLIDERS = {"base_color_tint", "roughness_bias"}
# lane-A values passed straight to Epic's OpenPBR function under their own names
PASS_THROUGH = {"base_weight", "base_metalness", "base_diffuse_roughness", "specular_weight",
                "specular_color", "specular_ior", "specular_roughness_anisotropy", "coat_weight",
                "coat_color", "coat_roughness", "coat_ior", "fuzz_weight", "fuzz_color", "fuzz_roughness"}
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


def tangents(p: np.ndarray, n: np.ndarray, uv: np.ndarray, tris: np.ndarray) -> np.ndarray:
    """Per-vertex dP/ds, made perpendicular to the normal (the tangent a normal map's X follows)."""
    i0, i1, i2 = tris[:, 0], tris[:, 1], tris[:, 2]
    e1, e2 = p[i1] - p[i0], p[i2] - p[i0]
    d1, d2 = uv[i1] - uv[i0], uv[i2] - uv[i0]
    det = d1[:, 0] * d2[:, 1] - d2[:, 0] * d1[:, 1]
    r = np.where(np.abs(det) > 1e-12, 1.0 / np.where(det == 0, 1, det), 0.0)
    t = (e1 * d2[:, 1:2] - e2 * d1[:, 1:2]) * r[:, None]
    acc = np.zeros_like(p)
    for k in (i0, i1, i2):
        np.add.at(acc, k, t)
    acc -= n * np.sum(acc * n, axis=1, keepdims=True)
    ln = np.linalg.norm(acc, axis=1, keepdims=True)
    fallback = np.cross(n, np.where(np.abs(n[:, 1:2]) < 0.9, [[0, 1, 0]], [[1, 0, 0]]))
    fallback /= np.linalg.norm(fallback, axis=1, keepdims=True)
    return np.where(ln > 1e-9, acc / np.maximum(ln, 1e-12), fallback)


def write_mesh(folder: Path, name: str, pts, nrm, uvs, faces, material: str) -> dict:
    """One mesh buffer: float32 positions, normals, tangents (Unreal space), st; int32 triangles."""
    p, n = np.asarray(pts, float), np.asarray(nrm, float)
    n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    uv = np.asarray(uvs, float)
    tris = triangulate(faces)
    t = tangents(p, n, uv, tris)
    buf = (np.concatenate([(to_ue(p) * 100.0).ravel(), to_ue(n).ravel(), to_ue(t).ravel(), uv.ravel()])
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
                "/World/CamClose": (build_scene.CLOSE_POS, build_scene.CLOSE_ROT)}


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


def article_material(path: Path, sliders: dict | None = None) -> dict:
    """The article on its master, by the article's names; raises Unsupported if not yet built."""
    art = article.read(Path(path))
    if art.master not in BUILT_MASTERS:
        raise Unsupported(f"{art.name}: the {art.master} master is not built in Unreal yet")
    extra = sorted(set(art.textures) - TEXTURE_ROLES)
    if extra:
        raise Unsupported(f"{art.name}: textures {extra} are not carried by Unreal's masters yet")
    unported = sorted(set(art.ports) - SLIDERS)
    if unported:
        raise Unsupported(f"{art.name}: sliders {unported} are not carried by Unreal's masters yet")
    ports = dict(art.ports)
    for k, v in (sliders or {}).items():
        if k not in ports:
            raise KeyError(f"{art.name} does not declare the slider {k!r}")
        ports[k] = list(v) if isinstance(v, (list, tuple)) else [float(v)]
    sh, scalars, vectors, textures = art.shader, {}, {}, {}
    for role, param in (("base_color", "base_color"), ("roughness", "specular_roughness"),
                        ("metalness", "base_metalness")):
        if role in art.textures:
            file, cs = art.textures[role]
            textures[f"{role}_tex"] = {"file": str(file), "srgb": cs not in LINEAR_SPACES}
            value = [1.0]                 # the texture carries it; the constant stays neutral
        else:
            value = art.consts.get(role) or sh.get(param)
        if value is None:
            continue
        if role == "base_color":
            vectors[param] = _vec(value)
        else:
            scalars[param] = float(value[0])
    for k in PASS_THROUGH & set(sh):
        if len(sh[k]) >= 3:
            vectors[k] = _vec(sh[k])
        else:
            scalars[k] = float(sh[k][0])
    if "base_color_tint" in ports:
        vectors["base_color_tint"] = _vec(ports["base_color_tint"])
    if "roughness_bias" in ports:
        scalars["roughness_bias"] = float(ports["roughness_bias"][0])
    return {"master": art.master, "scalars": scalars, "vectors": vectors, "textures": textures}


def preview_surface(colour: float | None = None, texture: Path | None = None, roughness: float = 0.9) -> dict:
    """The scene furniture's UsdPreviewSurface (build_scene.preview_material) on the Opaque master."""
    m = {"master": "Opaque", "scalars": {"specular_roughness": roughness, "base_metalness": 0.0,
                                         "specular_ior": 1.5},
         "vectors": {"base_color": [1.0] * 3 if texture else [colour] * 3}, "textures": {}}
    if texture:
        m["textures"]["base_color_tex"] = {"file": str(texture), "srgb": True}
    return m


# ------------------------------------------------------------------ the Unreal job

def unreal_job(job: dict, folder: Path, sun_k: float = SUN_K, dome_k: float = DOME_K,
               extra_settings: list | None = None, extra_views: list | None = None) -> Path:
    """Convert a rig job (test scene) into the runtime's job; returns its path."""
    if job.get("mode") == "character":
        raise Unsupported("the character job reaches Unreal at step 6.5")
    meshes_dir = folder / "meshes"
    meshes_dir.mkdir(parents=True, exist_ok=True)
    mpt = float(job["article"]["meters_per_tile"])
    makers = {"Sphere": build_scene.sphere, "Cube": build_scene.rounded_cube, "Floor": build_scene.floor}
    meshes = []
    for prim in job["subjects"]:
        name = prim.rsplit("/", 1)[1]
        pts, nrm, uvs, idx = makers[name]()
        meshes.append(write_mesh(meshes_dir, name, pts, nrm, [(s / mpt, t / mpt) for s, t in uvs], idx, "article"))
    for name, mesh, mat in (("RulerBlack", build_scene.ruler(True), "ruler_black"),
                            ("RulerWhite", build_scene.ruler(False), "ruler_white"),
                            ("Wall", build_scene.wall(), "wall")):
        meshes.append(write_mesh(meshes_dir, name, *mesh, mat))
    furniture = {"ruler_black": preview_surface(0.02), "ruler_white": preview_surface(0.8),
                 "wall": preview_surface(texture=(build_scene.HERE / build_scene.UVGRID).resolve(), roughness=0.8)}
    settings = [{"id": s["id"], "materials": {"article": article_material(Path(job["article"]["path"]), s.get("set")),
                                              **furniture}}
                for s in job["settings"]] + list(extra_settings or [])
    views = []
    for spec in job["views"].values():
        pos, rot = TEST_CAMERAS[spec["camera"]]
        views.append(camera_view(pos, rot, spec["suffix"], [p.rsplit("/", 1)[1] for p in spec.get("hide", [])]))
    views += list(extra_views or [])
    sun, sky = lights(sun_k, dome_k)
    ujob = {"format": 1, "width": int(job["width"]) * SUPERSAMPLE, "out_dir": str(folder / "raw"),
            "settle_frames": SETTLE_FRAMES, "sun": sun, "sky": sky, "meshes": meshes,
            "settings": settings, "views": views}
    p = folder / "unreal_job.json"
    p.write_text(json.dumps(ujob, indent=1) + "\n", encoding="utf-8")
    return p


# ------------------------------------------------------------------ running it

def find_runtime() -> list[str] | None:
    """The command that starts the runtime, or None (the rig skips the column with a notice)."""
    exe = os.environ.get("MATTER_UNREAL_RUNTIME")
    if exe:
        return [exe]
    editor = os.environ.get("MATTER_UNREAL_EDITOR")
    if editor:
        return [editor, str(PROJECT), "-game"]
    return None


def run_runtime(cmd: list[str], ujob: Path, log: Path) -> None:
    packaged = "-game" not in cmd
    env = dict(os.environ)
    if packaged:        # a package runs with no display at all, on SDL's dummy driver (UR-F8)
        env.pop("DISPLAY", None)
        env.pop("WAYLAND_DISPLAY", None)
    full = ["nice", "-n", "19", *cmd, f"-MatterJob={ujob}", "-RenderOffscreen", "-unattended",
            "-nosound", "-stdout", "-FullStdOutLogOutput"]
    with log.open("w", encoding="utf-8") as fh:
        rc = subprocess.run(full, stdout=fh, stderr=subprocess.STDOUT, env=env, timeout=TIMEOUT_S).returncode
    if rc != 0:
        raise SystemExit(f"Unreal runtime failed (exit {rc}); see {log}")


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


# ------------------------------------------------------------------ calibration

def calibrate(job_path: Path) -> None:
    """Fit SUN_K and DOME_K on the grey card, against Blender's picture of it.

    One launch renders the job's defaults three ways (sun and dome, sun only, dome only) at
    factors 1, plus a view straight up into the dome. The dome view gives EXPOSURE_K (an unlit
    sphere of radiance r reads EXPOSURE_K x r). Unreal's light is linear in each light, so
    Blender's linear picture over the subjects is fitted as SUN_K x sun-only + DOME_K x dome-only.
    """
    global EXPOSURE_K
    job = json.loads(job_path.read_text(encoding="utf-8"))
    out = Path(job["out_dir"])
    ref, mask = out / "blender" / "defaults.png", out / "mask.png"
    if not ref.is_file() or not mask.is_file():
        raise SystemExit(f"run the rig on this job first (Blender's {ref.name} and {mask.name})")
    cmd = find_runtime()
    if cmd is None:
        raise SystemExit("no Unreal runtime (set MATTER_UNREAL_RUNTIME or MATTER_UNREAL_EDITOR)")
    folder = out / TOOL / "calibrate"
    ujob = unreal_job(job, folder, sun_k=1.0, dome_k=1.0)
    spec = json.loads(ujob.read_text(encoding="utf-8"))
    mats = spec["settings"][0]["materials"]
    spec["settings"] = [{"id": "both", "materials": mats},
                        {"id": "sun", "materials": mats, "sky_scale": 0.0},
                        {"id": "dome", "materials": mats, "sun_scale": 0.0}]
    spec["views"] = [spec["views"][0], {"suffix": "__sky", "location": [0, 0, 0], "forward": [0, 0, 1],
                                        "up": [1, 0, 0], "fov": 30.0, "near": 2.0, "hide": []}]
    ujob.write_text(json.dumps(spec, indent=1) + "\n", encoding="utf-8")
    run_runtime(cmd, ujob, folder / "unreal.log")

    raw = folder / "raw"
    sky = read_pfm(raw / "both__sky.pfm")
    EXPOSURE_K = float(sky.mean() / build_scene.DOME_RADIANCE)
    both, sun, dome = (linear(raw / f"{k}.pfm") for k in ("both", "sun", "dome"))
    b8 = np.asarray(Image.open(ref).convert("RGB"), dtype=np.float64) / 255.0
    blender = np.where(b8 <= 0.04045, b8 / 12.92, ((b8 + 0.055) / 1.055) ** 2.4)
    m = np.asarray(Image.open(mask).convert("RGB"))
    on = (m.max(axis=2) > 200) & (blender.max(axis=2) < 0.98)
    A = np.stack([sun[on].ravel(), dome[on].ravel()], axis=1)
    (sun_k, dome_k), *_ = np.linalg.lstsq(A, blender[on].ravel(), rcond=None)
    fit = sun_k * sun + dome_k * dome
    print(f"EXPOSURE_K = {EXPOSURE_K:.5f}   (dome view mean {sky.mean():.5f}, sky spread "
          f"{sky.min():.5f}..{sky.max():.5f})")
    print(f"SUN_K      = {sun_k:.5f}")
    print(f"DOME_K     = {dome_k:.5f}")
    print(f"at factors 1: Unreal/Blender over the subjects = {both[on].mean() / blender[on].mean():.4f}")
    for i, name in enumerate(("sphere", "cube", "floor")):
        sel = m[..., i] > 200
        sel &= on
        if sel.any():
            print(f"  {name:6s} Blender {blender[sel].mean():.4f}  Unreal fitted {fit[sel].mean():.4f}  "
                  f"ratio {fit[sel].mean() / blender[sel].mean():.4f}")
    rel = np.abs(fit[on] - blender[on]) / np.maximum(blender[on], 1e-3)
    print(f"fitted relative error over the subjects: median {np.median(rel):.4f}, p95 {np.percentile(rel, 95):.4f}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("job", type=Path)
    ap.add_argument("--calibrate", action="store_true", help="fit the light factors on this (grey card) job")
    a = ap.parse_args(argv)
    try:
        calibrate(a.job) if a.calibrate else run(a.job)
    except Unsupported as e:
        raise SystemExit(f"unreal: {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
