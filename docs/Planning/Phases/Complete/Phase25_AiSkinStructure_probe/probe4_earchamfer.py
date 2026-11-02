"""P25 Pass 3 probe 4d: find the drawn ear by its OUTLINE (chamfer match), as hm08's ear front moved,
sized, stretched and turned.
hm08's side: the front of the ear as laid in the frame (probe4_earrender.py's `front` mask); its RIM is
the front's boundary where it meets the ear's unseen back (the helix edge a profile shows). Picture side:
edges = the strongest colour gradients in the window (a per-window percentile, so a pale ear's faint
outline counts as a pink ear's strong one), their distance transform truncated. Score = the rim points'
mean distance to the nearest edge (lower is better), searched over position (FFT), size, stretch, turn.
Writes the ears json probe3_field.py reads ({ear: dx, dy, M}: the first pass at c_hm - (dx,dy) + M (p - c_hm)
lands on hm08's point p) and a check picture.
usage: python probe4_earchamfer.py <first_pass_island.png> <uv_frame.json> <shape_dir> <out.json> <check.png> [edge_pct 92] [outline: all|rim]"""
import json, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, sobel, distance_transform_edt, binary_erosion, binary_dilation
from scipy.signal import correlate

pic, of, sd, outj, chk = sys.argv[1:6]
PCT = float(sys.argv[6]) if len(sys.argv) > 6 else 92
OUTLINE = sys.argv[7] if len(sys.argv) > 7 else "all"     # all | rim
F = json.load(open(of))
A = np.asarray(Image.open(pic).convert("RGB"), np.float64) / 255
G = sum(np.hypot(sobel(gaussian_filter(A[..., k], 2.0), 0), sobel(gaussian_filter(A[..., k], 2.0), 1)) for k in range(3))
TRUNC = 12.0
res, draw = {}, {}
for side in ("ear_r", "ear_l"):
    S = np.load(f"{sd}/hm08_{side}_shape.npz")
    front = S["front"]; seen = S["shade"] > 0
    from scipy.ndimage import binary_opening
    unseen_near = binary_dilation(binary_opening(~seen, iterations=2), iterations=3)   # the back, specks dropped
    # the ear front's whole outline (only a short stretch of it borders the unseen back: alone it fits any edge)
    rim = front & ~binary_erosion(front, iterations=1) if OUTLINE == "all" else front & ~binary_erosion(front, iterations=1) & unseen_near
    ry, rx = np.nonzero(rim)
    fy, fx = np.nonzero(front)
    c_hm = np.array([fy.mean(), fx.mean()])
    pts = np.stack([ry, rx], 1) - c_hm                          # rim points about the ear front's centre
    f = F["features"][side]
    wy0, wy1 = max(int(f["cy"] - 280), 0), min(int(f["cy"] + 280), A.shape[0])
    wx0, wx1 = (int(f["cx"] - 340), int(f["cx"] + 260)) if side == "ear_r" else (int(f["cx"] - 260), int(f["cx"] + 340))
    wx0, wx1 = max(wx0, 0), min(wx1, A.shape[1])
    g = G[wy0:wy1, wx0:wx1]
    edges = g > np.percentile(g, PCT)
    DT = np.minimum(distance_transform_edt(~edges), TRUNC)
    best = (1e9, None)
    def tryit(s, deg, asp):
        global best
        th = np.deg2rad(deg); Rm = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        Mf = Rm @ np.diag([s / np.sqrt(asp), s * np.sqrt(asp)])   # (row, col)
        q = pts @ Mf.T
        q0 = np.floor(q.min(0)).astype(int); qi = np.round(q - q0).astype(int)
        hh, ww = qi.max(0) + 1
        if hh >= DT.shape[0] or ww >= DT.shape[1]: return
        K = np.zeros((hh, ww)); np.add.at(K, (qi[:, 0], qi[:, 1]), 1.0)
        sc = correlate(DT, K, mode="valid", method="fft") / len(pts)
        k = np.unravel_index(np.argmin(sc), sc.shape)
        if sc[k] < best[0]:
            centre = np.array([wy0 + k[0], wx0 + k[1]]) - q0      # where c_hm lands in the picture
            best = (float(sc[k]), (s, deg, asp, centre, Mf))
    for s in np.arange(0.9, 2.31, 0.07):
        for deg in range(-30, 31, 6):
            for asp in (1.0, 1.25, 1.5, 1.8, 2.2, 2.6): tryit(s, deg, asp)
    s0, d0, a0 = best[1][:3]
    for s in np.arange(s0 - 0.07, s0 + 0.071, 0.02):
        for deg in np.arange(d0 - 6, d0 + 6.1, 1.5):
            for asp in a0 * np.array([0.88, 0.94, 1.0, 1.06, 1.12]): tryit(s, deg, asp)
    sc, (s, deg, asp, centre, Mf) = best[0], best[1]
    # in probe3_field's terms, about the feature centre (cx, cy) of the pad
    cf = np.array([f["cy"], f["cx"]])
    q_cf = centre + Mf @ (cf - c_hm)
    Mxy = np.array([[Mf[1, 1], Mf[1, 0]], [Mf[0, 1], Mf[0, 0]]])
    res[side] = {"dx": float(cf[1] - q_cf[1]), "dy": float(cf[0] - q_cf[0]), "s": float(s), "M": Mxy.tolist(),
                 "rot": float(deg), "aspect": float(asp), "chamfer_px": round(sc, 2)}
    print(f"{side}: rim off the drawn outline by {sc:.2f} px on average (truncated at {TRUNC:.0f}); "
          f"size x{s:.2f}, wider x{asp:.2f}, turn {deg:+.1f} deg; ear front centre moved {np.hypot(*(centre - c_hm)) * F['mm_per_px']:.1f} mm")
    draw[side] = (centre, Mf, pts, np.stack([fy, fx], 1) - c_hm)
json.dump(res, open(outj, "w"), indent=1)
tiles = []
for side in ("ear_r", "ear_l"):
    centre, Mf, pts, fpts = draw[side]
    cy, cx = centre.astype(int)
    crop = (A[cy - 160:cy + 160, cx - 160:cx + 160] * 255).astype(np.uint8)
    im = Image.fromarray(crop).resize((640, 640), Image.LANCZOS); dr = ImageDraw.Draw(im)
    for P_, col in ((pts, (0, 255, 255)),):
        q = centre + P_ @ Mf.T
        for yy, xx in q:
            dr.point(((xx - (cx - 160)) * 2, (yy - (cy - 160)) * 2), fill=col)
    tiles.append(im)
o = Image.new("RGB", (1290, 640), (40, 40, 40)); o.paste(tiles[0], (0, 0)); o.paste(tiles[1], (650, 0)); o.save(chk)
