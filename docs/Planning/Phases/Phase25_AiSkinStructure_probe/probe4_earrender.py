"""P25 Pass 3 probe 4c: hm08's ear AS SEEN FROM THE SIDE, laid into the head island's frame.
Each pixel of the head renderer's profile view (in_f±80_base.png + geom_f±80.npz: uv, mask) carries its
grey level to its texel's place in the frame. Inside hm08's ear pad only the ear's FRONT is seen (the pad
also holds the ear's back), so this is the shape a drawn ear must land on. Writes hm08_<ear>_shape.npz
(shade, mask, box) for probe4_earfind.py, and a view.
usage: python probe4_earrender.py <P25_Views dir> <uv_frame.json> <head_fields.npz> <out_dir>"""
import json, sys
import numpy as np
from PIL import Image
from scipy.ndimage import binary_dilation, binary_closing

V, of, hf, out = sys.argv[1:5]
F = json.load(open(of)); y0, y1, x0, x1 = F["bbox"]; W, H = F["size"]
Hd = np.load(hf); idx = Hd["idx"]; r, c = np.divmod(idx, 8192)
X = np.round((y1 - r - 0.5) * W / (y1 - y0) - 0.5).astype(int); Y = np.round((c - x0 + 0.5) * H / (x1 - x0) - 0.5).astype(int)
ok = (X >= 0) & (X < W) & (Y >= 0) & (Y < H) & (Hd["ears"] > 0.5)
pad = np.zeros((H, W), bool); pad[Y[ok], X[ok]] = True
pad = binary_closing(pad, iterations=2)
for view, side in (("f-80", "ear_r"), ("f+80", "ear_l")):
    g = np.load(f"{V}/geom_{view}.npz")
    im = np.asarray(Image.open(f"{V}/in_{view}_base.png").convert("L"), np.float64) / 255
    ys, xs = np.nonzero(g["mask"]); uv = g["uv"][ys, xs] * 8192
    fx = np.round((y1 - uv[:, 1] - 0.5) * W / (y1 - y0) - 0.5).astype(int)
    fy = np.round((uv[:, 0] - x0 + 0.5) * H / (x1 - x0) - 0.5).astype(int)
    k = (fx >= 0) & (fx < W) & (fy >= 0) & (fy < H)
    acc = np.zeros((H, W)); n = np.zeros((H, W))
    np.add.at(acc, (fy[k], fx[k]), im[ys[k], xs[k]]); np.add.at(n, (fy[k], fx[k]), 1)
    seen = binary_closing(n > 0, iterations=2)
    sh = np.where(n > 0, acc / np.maximum(n, 1), 0)
    f = F["features"][side]
    near = np.zeros((H, W), bool); near[int(f["y0"]) - 25:int(f["y1"]) + 25, int(f["x0"]) - 25:int(f["x1"]) + 25] = True
    front = seen & pad
    m = seen & binary_dilation(front, iterations=12) & near     # the ear's front and a rim of scalp round it
    yy, xx = np.nonzero(m)
    box = np.array([xx.min(), xx.max() + 1, yy.min(), yy.max() + 1])
    np.savez_compressed(f"{out}/hm08_{side}_shape.npz", shade=sh.astype(np.float32), mask=m, front=front, box=box)
    fy_, fx_ = np.nonzero(front)
    print(f"{side} (view {view}): front of the ear {np.ptp(fx_) + 1} x {np.ptp(fy_) + 1} px in the frame; pad {int(f['w'])} wide")
    bx0, bx1, by0, by1 = box
    Image.fromarray((np.where(m, sh, 0)[by0:by1, bx0:bx1] * 255).astype(np.uint8)).resize(((bx1 - bx0) * 3, (by1 - by0) * 3)).save(f"{out}/hm08_{side}_front.png")
