"""Disposable probe: render hm08's head with a skin map from known cameras, and project pictures
taken from those same cameras back into the 2048^2 UV map. Numpy only; reads the library's maker
code (never writes to the repo)."""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "tools/converters/fit"))
sys.path.insert(0, str(REPO / "tools/converters"))
import gen_synth_skin as gss  # noqa: E402
import make_kits  # noqa: E402

N = gss.N
SKIN = REPO / "MatterLibrary/textures/fit/makehuman/skin"
RECIPES = REPO / "tools/converters/recipes"
W = 1024
TARGET = np.array([0.0, 0.715, 0.03])


def srgb_to_lin(x):
    return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)


def lin_to_srgb(x):
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


def albedo(structure="", roman="III"):
    """The article's rendered albedo: decoded map x its raised base_color_const."""
    m = np.asarray(Image.open(SKIN / f"{structure}Fitzpatrick{roman}_basecolor_sUKN.png").convert("RGB"), np.float64) / 255
    name = f"{structure or 'Skin'}_Fitzpatrick{roman}_Clean_Base_s001_v01.json"
    c = np.array([float(v) for v in json.loads((RECIPES / name).read_text())["base_color_const"].split(",")])
    return srgb_to_lin(m) * c, c


def head_mesh():
    m = make_kits.load_mesh(gss.MESH)
    P = np.array(m["points"], np.float64)
    vt = np.array(m["vt"], np.float64)
    tris = []
    for f in m["faces"]:
        for t in ((0, 1, 2), (0, 2, 3)) if len(f) == 4 else ((0, 1, 2),):
            tris.append([(f[i][0], f[i][1]) for i in t])
    T = np.array(tris)  # (n,3,2)
    keep = (P[T[:, :, 0], 1] > 0.50).all(1)
    vn = np.zeros_like(P)
    for tri in T:
        vi = tri[:, 0]
        vn[vi] += np.cross(P[vi[1]] - P[vi[0]], P[vi[2]] - P[vi[0]])
    vn /= np.maximum(np.linalg.norm(vn, axis=1, keepdims=True), 1e-12)
    return P, vt, T[keep], vn


def camera(yaw_deg, pitch_deg=5.0, dist=0.78, fov_deg=24.0):
    y, p = np.radians(yaw_deg), np.radians(pitch_deg)
    C = TARGET + dist * np.array([np.sin(y) * np.cos(p), np.sin(p), np.cos(y) * np.cos(p)])
    f = TARGET - C
    f /= np.linalg.norm(f)
    r = np.cross(f, [0, 1, 0]); r /= np.linalg.norm(r)
    u = np.cross(r, f)
    return {"C": C, "R": np.stack([r, u, f]), "fpx": (W / 2) / np.tan(np.radians(fov_deg) / 2), "yaw": yaw_deg}


def project(cam, X):
    Xc = (X - cam["C"]) @ cam["R"].T          # x right, y up, z forward (depth)
    z = Xc[..., 2]
    px = W / 2 + cam["fpx"] * Xc[..., 0] / z
    py = W / 2 - cam["fpx"] * Xc[..., 1] / z
    return px, py, z


def render(cam, P, vt, T, vn):
    """z-buffer render: per pixel the UV (0..1, v down as the map's rows), depth and normal."""
    px, py, z = project(cam, P)
    zb = np.full((W, W), np.inf)
    uvb = np.zeros((W, W, 2))
    nb = np.zeros((W, W, 3))
    for tri in T:
        vi, ti = tri[:, 0], tri[:, 1]
        ax, bx, cx = px[vi]; ay, by, cy = py[vi]
        den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
        if den >= -1e-9:            # back-facing (or degenerate) in screen space: culled
            continue
        x0, x1 = int(max(np.floor(min(ax, bx, cx)), 0)), int(min(np.ceil(max(ax, bx, cx)), W - 1))
        y0, y1 = int(max(np.floor(min(ay, by, cy)), 0)), int(min(np.ceil(max(ay, by, cy)), W - 1))
        if x1 < x0 or y1 < y0:
            continue
        ys, xs = np.mgrid[y0:y1 + 1, x0:x1 + 1]
        qx, qy = xs + 0.5, ys + 0.5
        w0 = ((by - cy) * (qx - cx) + (cx - bx) * (qy - cy)) / den
        w1 = ((cy - ay) * (qx - cx) + (ax - cx) * (qy - cy)) / den
        w2 = 1 - w0 - w1
        ins = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        if not ins.any():
            continue
        Wb = np.stack([w0[ins], w1[ins], w2[ins]], -1)
        zz = Wb @ z[vi]
        yy, xx = ys[ins], xs[ins]
        closer = zz < zb[yy, xx]
        if not closer.any():
            continue
        yy, xx, Wb, zz = yy[closer], xx[closer], Wb[closer], zz[closer]
        zb[yy, xx] = zz
        uv = Wb @ vt[ti]
        uvb[yy, xx, 0] = uv[:, 0]
        uvb[yy, xx, 1] = 1 - uv[:, 1]
        n = Wb @ vn[vi]
        nb[yy, xx] = n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    return {"z": zb, "uv": uvb, "n": nb, "mask": np.isfinite(zb)}


def sample(img, uv):
    """Bilinear lookup of an (H,W,C) image at uv in 0..1 (x right, y down)."""
    H, Wd = img.shape[:2]
    x = np.clip(uv[..., 0] * Wd - 0.5, 0, Wd - 1.001)
    y = np.clip(uv[..., 1] * H - 0.5, 0, H - 1.001)
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    fx, fy = (x - x0)[..., None], (y - y0)[..., None]
    a, b = img[y0, x0], img[y0, x0 + 1]
    c, d = img[y0 + 1, x0], img[y0 + 1, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy


def shading(cam, rnd, key=(0.35, 0.45, 1.0), amb=0.45):
    """A soft key light from upper front-left in camera space, plus ambient."""
    l = np.array(key) / np.linalg.norm(key)
    nc = rnd["n"] @ cam["R"].T
    nc[..., 2] *= -1                         # camera z points away from the viewer; flip to face it
    return amb + (1 - amb) * np.clip(nc @ l, 0, 1)


def picture(cam, rnd, alb, bg=0.18, shade=True):
    col = sample(alb, rnd["uv"])
    if shade:
        col = col * shading(cam, rnd)[..., None]
    out = np.where(rnd["mask"][..., None], col, bg ** 2.2)
    return lin_to_srgb(out)


def save(path, srgb):
    Image.fromarray((np.clip(srgb, 0, 1) * 255 + 0.5).astype(np.uint8)).save(path)
