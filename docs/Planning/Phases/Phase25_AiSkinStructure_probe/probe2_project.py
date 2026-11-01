"""P25 Pass 3 probe 2: Krea's picture is a FRONT VIEW of a face (the scalp unrolled around it), so its face
is matched to hm08's FRONT RENDER by dense landmarks (MediaPipe, 478 points, a piecewise-affine warp per
triangle) and projected onto the mesh through that camera into the head island's frame. Outside what the
front camera sees well, the island keeps a base picture (feathered join: a probe, not the route).
usage: python probe2_project.py <picture> <lm_picture.npy> <lm_render.npy> <geom.npz> <uv_frame.json> <base> <out.png> [min_nz]"""
import json, sys
import numpy as np
from PIL import Image
from scipy.spatial import Delaunay
from scipy.ndimage import distance_transform_edt, map_coordinates, binary_closing, binary_fill_holes

pic, lmp, lmr, geom, frame, base, out = sys.argv[1:8]
min_nz = float(sys.argv[8]) if len(sys.argv) > 8 else 0.35
N = 8192
P = np.asarray(Image.open(pic).convert("RGB"), np.float64)
Lp, Lr = np.load(lmp), np.load(lmr)
g = np.load(geom); uv, mask, n = g["uv"], g["mask"], g["n"]
F = json.load(open(frame)); y0, y1, x0, x1 = F["bbox"]; W, Hh = F["size"]

tri = Delaunay(Lr)
ys, xs = np.nonzero(mask)
pts = np.stack([xs + 0.5, ys + 0.5], 1)
s = tri.find_simplex(pts)
ok = s >= 0
T = tri.transform[s[ok]]
b2 = np.einsum("nij,nj->ni", T[:, :2], pts[ok] - T[:, 2]); bary = np.c_[b2, 1 - b2.sum(1)]
src = np.einsum("ni,nij->nj", bary, Lp[tri.simplices[s[ok]]])          # where in the picture
col = np.stack([map_coordinates(P[..., k], [src[:, 1] - 0.5, src[:, 0] - 0.5], order=1, mode="nearest") for k in range(3)], 1)
yy, xx = ys[ok], xs[ok]
# facing the camera: the renderer's normal, camera looks along -z
nz = np.abs(n[yy, xx, 2]); w = np.clip((nz - min_nz) / 0.25, 0, 1)
u, v = uv[yy, xx, 0], uv[yy, xx, 1]
rows, cols = v * N, u * N
fx = (y1 - rows - 0.5) * (W / (y1 - y0)) - 0.5; fy = (cols - x0 + 0.5) * (Hh / (x1 - x0)) - 0.5
ix, iy = np.round(fx).astype(int), np.round(fy).astype(int)
k = (ix >= 0) & (ix < W) & (iy >= 0) & (iy < Hh) & (w > 0)
acc = np.zeros((Hh, W, 3)); wt = np.zeros((Hh, W))
np.add.at(acc, (iy[k], ix[k]), col[k] * w[k, None]); np.add.at(wt, (iy[k], ix[k]), w[k])
cov = wt > 0
proj = np.where(cov[..., None], acc / np.maximum(wt, 1e-9)[..., None], 0)
# close the splat's pinholes, then a feathered join to the base picture
region = binary_fill_holes(binary_closing(cov, iterations=3))
for _ in range(6):                                           # fill pinholes inside the region from neighbours
    hole = region & ~cov
    if not hole.any(): break
    sm = sum(np.roll(np.roll(proj * cov[..., None], dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1))
    sw = sum(np.roll(np.roll(cov.astype(float), dy, 0), dx, 1) for dy in (-1, 0, 1) for dx in (-1, 0, 1))
    fill = hole & (sw > 0); proj[fill] = sm[fill] / sw[fill, None]; cov = cov | fill
wfin = np.clip(distance_transform_edt(region & cov) / 24.0, 0, 1)     # 24 px (~8 mm) feather
B = np.asarray(Image.open(base).convert("RGB").resize((W, Hh)), np.float64)
outp = proj * wfin[..., None] + B * (1 - wfin[..., None])
Image.fromarray(np.clip(outp + 0.5, 0, 255).astype(np.uint8)).save(out)
Image.fromarray((wfin * 255).astype(np.uint8)).save(out.replace(".png", "_weight.png"))
print(f"render px mapped {ok.mean()*100:.1f}% of the head; island px covered {cov.mean()*100:.1f}%; triangles {len(tri.simplices)}")
