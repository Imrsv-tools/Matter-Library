"""P25 Pass 3 probe 4a: hm08's own ear, drawn into the head island's frame from the mesh.
Per head texel (head_fields_8192.npz: position P, normal N, ear mask), averaged into the island frame
(paint_uv's uv_frame.json): a side-lit shade (N . L, L along the head's side axis, outward) and a depth
(how far the texel stands out from the skull at that height, so the bowl is deep and the rim proud).
usage: python probe4_earshape.py <head_fields.npz> <uv_frame.json> <out_dir>"""
import json, sys
import numpy as np
from PIL import Image

hf, of, out = sys.argv[1:4]
H = np.load(hf); F = json.load(open(of))
N8 = 8192
idx = H["idx"]; r, c = np.divmod(idx, N8)
y0, y1, x0, x1 = F["bbox"]; W, Hh = F["size"]
X = (y1 - r - 0.5) * W / (y1 - y0) - 0.5            # same to_frame as paint_uv / probe3_field
Y = (c - x0 + 0.5) * Hh / (x1 - x0) - 0.5
ok = (X >= 0) & (X < W - 0.5) & (Y >= 0) & (Y < Hh - 0.5)
P, Nn, ear = H["P"], H["N"], H["ears"]
xc = float(np.median(P[H["face"] > 0.9, 0]))          # head's mid-plane (x is left-right)
res = {}
for side, sgn in (("ear_r", -1.0), ("ear_l", 1.0)):
    sel = ok & (ear > 0.5) & (sgn * (P[:, 0] - xc) > 0)
    lat = sgn * (P[sel, 0] - xc)                       # distance out from the mid-plane
    shade = np.clip(sgn * Nn[sel, 0] * 0.6 + Nn[sel, 1] * 0.3 + 0.4, 0, 1)   # side light, a little from above
    jx, jy = np.round(X[sel]).astype(int), np.round(Y[sel]).astype(int)
    acc = np.zeros((Hh, W, 3)); cnt = np.zeros((Hh, W))
    np.add.at(acc, (jy, jx), np.stack([shade, lat, np.ones_like(lat)], 1)); np.add.at(cnt, (jy, jx), 1)
    m = cnt > 0
    sh = np.where(m, acc[..., 0] / np.maximum(cnt, 1), 0); la = np.where(m, acc[..., 1] / np.maximum(cnt, 1), 0)
    ys, xs = np.nonzero(m)
    bx = (xs.min(), xs.max() + 1, ys.min(), ys.max() + 1)
    lo, hi = np.percentile(la[m], 2), np.percentile(la[m], 98)
    dep = np.where(m, np.clip((la - lo) / (hi - lo), 0, 1), 0)
    np.savez_compressed(f"{out}/hm08_{side}_shape.npz", shade=sh.astype(np.float32), depth=dep.astype(np.float32), mask=m, box=np.array(bx))
    res[side] = {"box": [int(v) for v in bx], "texels": int(sel.sum()), "lateral_mm": [round(lo * 1000, 1), round(hi * 1000, 1)]}
    x_0, x_1, y_0, y_1 = bx
    crop = lambda a: Image.fromarray((a[y_0 - 20:y_1 + 20, x_0 - 20:x_1 + 20] * 255).astype(np.uint8)).resize(((x_1 - x_0 + 40) * 3, (y_1 - y_0 + 40) * 3), Image.NEAREST)
    crop(sh).save(f"{out}/hm08_{side}_shade.png"); crop(dep).save(f"{out}/hm08_{side}_depth.png")
print(json.dumps(res, indent=1))
