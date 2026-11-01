"""P25 Pass 3 probe 4e: find the drawn ear by its SILHOUETTE and fit hm08's ear FRONT onto it.
Picture: edges = strongest colour gradients after a 4 px blur (pores gone), top 5 % of a generous window
round the pad; dilated, closed, holes filled; the largest region, its convex hull = the drawn ear. No colour
cue, so a pale ear is found like a pink one (paint_uv.find failed on pale ears and took a wrong blob on
seed 101). hm08: the ear's front as laid in the frame (probe4_earrender.py), its convex hull. Fit: the
hm08 hull moved, sized, stretched and turned to the largest overlap (IoU) with the drawn hull.
Writes the ears json probe3_field.py reads ({ear: dx, dy, M}: the first pass at c - (dx,dy) + M (p - c),
c the pad's feature centre, lands on hm08's point p) and a check picture (hm08's front outline, cyan, on
the drawn ear; the drawn hull, yellow).
usage: python probe4_earfit.py <first_pass_island.png> <uv_frame.json> <shape_dir> <out.json> <check.png> [max_turn_deg 30]"""
import json, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, sobel, binary_closing, binary_fill_holes, label, binary_dilation, binary_erosion
from scipy.spatial import ConvexHull
from scipy.signal import correlate

pic, of, sd, outj, chk = sys.argv[1:6]
MAXROT = float(sys.argv[6]) if len(sys.argv) > 6 else 30.0   # cap on the turn, degrees
F = json.load(open(of))
A = np.asarray(Image.open(pic).convert("RGB"), np.float64) / 255

def hull_mask(m, shape):
    ys, xs = np.nonzero(m); h = ConvexHull(np.stack([xs, ys], 1))
    im = Image.new("L", (shape[1], shape[0]), 0)
    ImageDraw.Draw(im).polygon([(float(xs[i]), float(ys[i])) for i in h.vertices], fill=1)
    return np.asarray(im, bool)

res, draw = {}, {}
for side in ("ear_r", "ear_l"):
    f = F["features"][side]; cy, cx = int(f["cy"]), int(f["cx"])
    wy0, wy1 = max(cy - 280, 0), min(cy + 280, A.shape[0])
    wx0, wx1 = (cx - 340, cx + 260) if side == "ear_r" else (cx - 260, cx + 340)
    wx0, wx1 = max(wx0, 0), min(wx1, A.shape[1])
    Wn = A[wy0:wy1, wx0:wx1]
    G = sum(np.hypot(sobel(gaussian_filter(Wn[..., k], 4), 0), sobel(gaussian_filter(Wn[..., k], 4), 1)) for k in range(3))
    e = G > np.percentile(G, 95)
    reg = binary_fill_holes(binary_closing(binary_dilation(e, iterations=2), iterations=12))
    lab, _ = label(reg); sz = np.bincount(lab.ravel()); sz[0] = 0
    drawn = hull_mask(lab == sz.argmax(), reg.shape)
    S = np.load(f"{sd}/hm08_{side}_shape.npz")
    front = S["front"]; fy, fx = np.nonzero(front)
    c_hm = np.array([fy.mean(), fx.mean()])
    fh = hull_mask(front, front.shape); hy, hx = np.nonzero(fh)
    pts = np.stack([hy, hx], 1) - c_hm                            # hm08's hull, filled, about its centre
    nA = drawn.sum()
    best = (-1, None)
    def tryit(s, deg, asp):
        global best
        th = np.deg2rad(deg); Rm = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        Mf = Rm @ np.diag([s / np.sqrt(asp), s * np.sqrt(asp)])
        q = pts @ Mf.T
        q0 = np.floor(q.min(0)).astype(int); qi = np.round(q - q0).astype(int)
        hh, ww = qi.max(0) + 1
        if hh >= drawn.shape[0] or ww >= drawn.shape[1]: return
        K = np.zeros((hh, ww)); K[qi[:, 0], qi[:, 1]] = 1
        K = binary_closing(K > 0, iterations=1).astype(float); nB = K.sum()
        ov = correlate(drawn.astype(float), K, mode="valid", method="fft")
        iou = ov / (nA + nB - ov)
        k = np.unravel_index(np.argmax(iou), iou.shape)
        if iou[k] > best[0]:
            best = (float(iou[k]), (s, deg, asp, np.array([wy0 + k[0], wx0 + k[1]]) - q0, Mf))
    for s in np.arange(0.9, 2.61, 0.08):
        for deg in np.arange(-MAXROT, MAXROT + 0.1, 6 if MAXROT >= 18 else 4):
            for asp in (0.9, 1.1, 1.35, 1.6, 1.9, 2.3): tryit(s, deg, asp)
    s0, d0, a0 = best[1][:3]
    for s in np.arange(s0 - 0.08, s0 + 0.081, 0.02):
        for deg in np.clip(np.arange(d0 - 6, d0 + 6.1, 1.5), -MAXROT, MAXROT):
            for asp in a0 * np.array([0.9, 0.95, 1.0, 1.05, 1.1]): tryit(s, deg, asp)
    iou, (s, deg, asp, centre, Mf) = best
    cf = np.array([f["cy"], f["cx"]])
    q_cf = centre + Mf @ (cf - c_hm)
    Mxy = np.array([[Mf[1, 1], Mf[1, 0]], [Mf[0, 1], Mf[0, 0]]])
    res[side] = {"dx": float(cf[1] - q_cf[1]), "dy": float(cf[0] - q_cf[0]), "s": float(s), "M": Mxy.tolist(),
                 "rot": float(deg), "aspect": float(asp), "iou": round(iou, 3)}
    print(f"{side}: overlap (IoU) {iou:.3f}; size x{s:.2f}, wider x{asp:.2f}, turn {deg:+.1f} deg; "
          f"ear front moved {np.hypot(*(centre - c_hm)) * F['mm_per_px']:.1f} mm")
    outline = front & ~binary_erosion(front, iterations=1)
    oy, ox = np.nonzero(outline)
    dy_, dx_ = np.nonzero(drawn & ~binary_erosion(drawn, iterations=1))
    draw[side] = (centre, Mf, np.stack([oy, ox], 1) - c_hm, np.stack([dy_ + wy0, dx_ + wx0], 1))
json.dump(res, open(outj, "w"), indent=1)
tiles = []
for side in ("ear_r", "ear_l"):
    centre, Mf, opts, dpts = draw[side]
    cy, cx = centre.astype(int)
    im = Image.fromarray((A[cy - 160:cy + 160, cx - 160:cx + 160] * 255).astype(np.uint8)).resize((640, 640), Image.LANCZOS)
    dr = ImageDraw.Draw(im)
    for P_, col in ((dpts - centre, (255, 220, 0)), (opts @ Mf.T, (0, 255, 255))):
        for yy, xx in P_:
            dr.point(((xx + 160) * 2, (yy + 160) * 2), fill=col)
    tiles.append(im)
o = Image.new("RGB", (1290, 640), (40, 40, 40)); o.paste(tiles[0], (0, 0)); o.paste(tiles[1], (650, 0)); o.save(chk)
