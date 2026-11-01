"""Disposable probe: project generated views back into hm08's 2048^2 map and render a comparison.
    bake.py <tag> [--calibrate]"""
import pickle
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import headrender as hr  # noqa: E402
import gen_synth_skin as gss  # noqa: E402  (on the path headrender sets)

OUT = __import__("os").environ.get("PROBE_OUT", "/tmp/skinprobe")
TAG = sys.argv[1]
USE = [int(v) for v in sys.argv[2].split(",")] if len(sys.argv) > 2 and not sys.argv[2].startswith("--") else None
POW = 4.0
EYE = 22   # px kept clear around the eye openings (the model paints eyes larger than the holes)

views = pickle.load(open(f"{OUT}/views.pkl", "rb"))
F = gss.fields()
P, Nr, cover = F["P"], F["N"], F["cover"]
alb, const = hr.albedo("", "III")
region = cover & (P[..., 1] > 0.50)

acc = np.zeros(alb.shape)
wsum = np.zeros(alb.shape[:2])
for y, (cam, r) in views.items():
    if USE is not None and y not in USE:
        continue
    gen = hr.srgb_to_lin(np.asarray(Image.open(f"{OUT}/view_{y:+04d}_{TAG}.png").convert("RGB"), np.float64) / 255)
    # trust only pixels well inside the head's silhouette and away from the eye holes
    inside = ndimage.binary_erosion(r["mask"], iterations=6)
    holes = ndimage.binary_fill_holes(r["mask"]) & ~r["mask"]
    inside &= ~ndimage.binary_dilation(holes, iterations=EYE)
    px, py, z = hr.project(cam, P)
    xi, yi = np.clip(px.astype(int), 0, hr.W - 1), np.clip(py.astype(int), 0, hr.W - 1)
    vis = region & (np.abs(r["z"][yi, xi] - z) < 0.004) & inside[yi, xi]
    to_cam = cam["C"] - P
    to_cam /= np.linalg.norm(to_cam, axis=-1, keepdims=True)
    face = np.clip(np.einsum("ijk,ijk->ij", Nr, to_cam), 0, 1)
    w = np.where(vis, face ** POW, 0)
    # the picture's albedo: the generated colour over the render's own lighting
    uvpix = np.stack([px / hr.W, py / hr.W], -1)
    g = hr.sample(gen, uvpix)
    s = hr.shading(cam, r)[..., None]
    sh = hr.sample(s, uvpix)
    est = g / np.maximum(sh, 0.05)
    acc += w[..., None] * est
    wsum += w
    print(y, "texels", int((w > 0).sum()))

have = wsum > 1e-4
new = np.where(have[..., None], acc / np.maximum(wsum, 1e-9)[..., None], alb)
if "--calibrate" in sys.argv:
    k = alb[have].mean(0) / new[have].mean(0)
    new[have] *= k
    print("calibration x", k.round(3))
# feather the projected region into today's map
wt = np.clip(ndimage.gaussian_filter((wsum / np.percentile(wsum[have], 50)).clip(0, 1), 6), 0, 1)
wt = np.where(region, wt, 0)
out = alb * (1 - wt[..., None]) + new * wt[..., None]
np.save(f"{OUT}/albedo_{TAG}.npy", out.astype(np.float32))
if "--inputs" in sys.argv:   # the next views' inputs: rendered with the map baked so far
    for y, (cam, r) in views.items():
        if USE is None or y not in USE:
            hr.save(f"{OUT}/view_{y:+04d}_in_{TAG}.png", hr.picture(cam, r, out))
    print("inputs written"); sys.exit(0)
hr.save(f"{OUT}/map_{TAG}.png", hr.lin_to_srgb(np.clip(out / const, 0, 1)))

# comparison: today's skin and the probe's, from the baked views and two new ones
P3, vt, T, vn = hr.head_mesh()
rows = []
for yaw, pitch in ((0, 5), (-40, 5), (25, -12), (60, 15)):
    cam = hr.camera(yaw, pitch, dist=0.62)
    r = hr.render(cam, P3, vt, T, vn)
    rows.append(np.concatenate([hr.picture(cam, r, alb), hr.picture(cam, r, out)], 1))
sheet = np.concatenate(rows, 0)
Image.fromarray((sheet * 255).astype(np.uint8)).resize((1024, 2048)).save(f"{OUT}/sheet_{TAG}.png")
print("done")
