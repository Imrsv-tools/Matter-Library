"""P25 Pass 3 probe 3: ONE mapping from the model's picture onto the head island, nothing blended.
Inside the face: the front projection (probe 2: dense landmarks, picture -> hm08's front render -> each
visible pixel's texture coordinate). Its displacement from the picture's own unrolled layout is then
continued smoothly outward and fades to zero (the picture's sides, scalp and ears as drawn), so colour is
only ever SAMPLED, at one place per texel.
usage: python probe3_field.py <picture> <picture_frame.json> <lm_picture.npy> <lm_render.npy> <geom.npz>
                               <out_frame.json> <out.png> [min_nz 0.08] [fade_px 60]"""
import json, sys
import numpy as np
from PIL import Image
from scipy.spatial import Delaunay
from scipy.ndimage import distance_transform_edt, map_coordinates

pic, pf, lmp, lmr, geom, of, out = sys.argv[1:8]
min_nz = float(sys.argv[8]) if len(sys.argv) > 8 else 0.08
fade = float(sys.argv[9]) if len(sys.argv) > 9 else 60.0
N = 8192
P = np.asarray(Image.open(pic).convert("RGB"), np.float64)
PF, OF = json.load(open(pf)), json.load(open(of))

def to_frame(F, rows, cols):
    y0, y1, x0, x1 = F["bbox"]; W, H = F["size"]
    return (y1 - rows - 0.5) * W / (y1 - y0) - 0.5, (cols - x0 + 0.5) * H / (x1 - x0) - 0.5

def from_frame(F, x, y):
    y0, y1, x0, x1 = F["bbox"]; W, H = F["size"]
    return y1 - 0.5 - (x + 0.5) * (y1 - y0) / W, x0 - 0.5 + (y + 0.5) * (x1 - x0) / H

W, H = OF["size"]
gy, gx = np.mgrid[0:H, 0:W].astype(np.float64)
ix, iy = to_frame(PF, *from_frame(OF, gx, gy))          # identity: the picture's own layout at each out pixel

Lp, Lr = np.load(lmp), np.load(lmr)
g = np.load(geom); uv, mask, n = g["uv"], g["mask"], g["n"]
tri = Delaunay(Lr)
ys, xs = np.nonzero(mask)
pts = np.stack([xs + 0.5, ys + 0.5], 1)
s = tri.find_simplex(pts); ok = s >= 0
T = tri.transform[s[ok]]
b2 = np.einsum("nij,nj->ni", T[:, :2], pts[ok] - T[:, 2]); bary = np.c_[b2, 1 - b2.sum(1)]
src = np.einsum("ni,nij->nj", bary, Lp[tri.simplices[s[ok]]])
yy, xx = ys[ok], xs[ok]
w = np.clip((np.abs(n[yy, xx, 2]) - min_nz) / 0.15, 0, 1)
ox, oy = to_frame(OF, uv[yy, xx, 1] * N, uv[yy, xx, 0] * N)
jx, jy = np.round(ox).astype(int), np.round(oy).astype(int)
k = (jx >= 0) & (jx < W) & (jy >= 0) & (jy < H) & (w > 0)
acc = np.zeros((H, W, 2)); wt = np.zeros((H, W))
np.add.at(acc, (jy[k], jx[k]), src[k] * w[k, None]); np.add.at(wt, (jy[k], jx[k]), w[k])
known = wt > 0.05
D = np.zeros((H, W, 2))
D[known] = acc[known] / wt[known, None] - np.stack([ix[known], iy[known]], 1)

def pushpull(img, kn):
    if kn.all() or min(img.shape[:2]) < 2: return img
    h, w_ = img.shape[:2]; H2, W2 = (h + 1) // 2, (w_ + 1) // 2; c = img.shape[2]
    pi = np.zeros((H2 * 2, W2 * 2, c)); pk = np.zeros((H2 * 2, W2 * 2))
    pi[:h, :w_] = img * kn[..., None]; pk[:h, :w_] = kn
    si = pi.reshape(H2, 2, W2, 2, c).sum((1, 3)); sk = pk.reshape(H2, 2, W2, 2).sum((1, 3))
    low = pushpull(np.where(sk[..., None] > 0, si / np.maximum(sk, 1e-9)[..., None], 0), sk > 0)
    up = np.repeat(np.repeat(low, 2, 0), 2, 1)[:h, :w_]
    return np.where(kn[..., None], img, up)

# a membrane: the face's displacement held in the face, zero held on the ear pads (the picture's own ears,
# drawn there) and on the island's border; harmonic in between, solved on a coarse grid, then upsampled
from scipy.ndimage import zoom, binary_dilation
zero = np.zeros((H, W), bool); zero[:4] = zero[-4:] = True; zero[:, :4] = zero[:, -4:] = True
for e in ("ear_r", "ear_l"):
    f = OF["features"][e]; cx, cy, hw, hh = f["cx"], f["cy"], (f["x1"] - f["x0"]) * 0.75, (f["y1"] - f["y0"]) * 0.75
    zero[int(cy - hh):int(cy + hh), int(cx - hw):int(cx + hw)] = True
zero &= ~binary_dilation(known, iterations=20)
q = 8; h8, w8 = (H + q - 1) // q, (W + q - 1) // q
def coarse(a, m):
    pa = np.zeros((h8 * q, w8 * q) + a.shape[2:]); pm = np.zeros((h8 * q, w8 * q))
    pa[:H, :W] = a * (m[..., None] if a.ndim == 3 else m); pm[:H, :W] = m
    sa = pa.reshape(h8, q, w8, q, -1).sum((1, 3)); sm = pm.reshape(h8, q, w8, q).sum((1, 3))
    return sa / np.maximum(sm, 1e-9)[..., None], sm > q * q * 0.3
cD, cK = coarse(D, known); cZ = coarse(zero.astype(float)[..., None], zero)[1]
fixed = cK | cZ; val = np.where(cK[..., None], cD, 0.0)
Dc = pushpull(val, fixed)
for _ in range(4000):
    av = (np.roll(Dc, 1, 0) + np.roll(Dc, -1, 0) + np.roll(Dc, 1, 1) + np.roll(Dc, -1, 1)) / 4
    Dc = np.where(fixed[..., None], val, av)
Dup = zoom(Dc, (q, q, 1), order=1)[:H, :W]
Df = np.where(known[..., None], D, Dup)
# soften the step at the face's edge: a narrow ramp between the exact face and the membrane
dist = distance_transform_edt(~known); a = np.clip(1 - dist / 12.0, 0, 1)[..., None]
Df = np.where(known[..., None], D, a * pushpull(D, known) + (1 - a) * Dup)
sx, sy = ix + Df[..., 0], iy + Df[..., 1]
outp = np.stack([map_coordinates(P[..., c], [sy, sx], order=1, mode="nearest") for c in range(3)], -1)
Image.fromarray(np.clip(outp + 0.5, 0, 255).astype(np.uint8)).save(out)
mm = 0.32
jxx = np.gradient(sx, axis=1); jyy = np.gradient(sy, axis=0); jxy = np.gradient(sx, axis=0); jyx = np.gradient(sy, axis=1)
det = jxx * jyy - jxy * jyx
print(f"fold check: texels folded {(det <= 0).mean()*100:.3f}% (in the face {((det <= 0) & known).sum() / known.sum()*100:.2f}%, outside {((det <= 0) & ~known).mean()*100:.3f}%), largest local stretch {np.sqrt(np.abs(det)).max():.2f}")
print(f"known {known.mean()*100:.1f}% of the island; displacement in the face: median {np.median(np.hypot(*D[known].T))*mm:.1f} mm, max {np.hypot(*D[known].T).max()*mm:.0f} mm")
