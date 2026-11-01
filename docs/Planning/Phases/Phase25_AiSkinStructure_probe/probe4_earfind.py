"""P25 Pass 3 probe 4b: find the model's drawn ear by its SHAPE, as hm08's own ear moved, sized and turned.
The template is hm08's ear drawn from the mesh into the island frame (probe4_earshape.py: side-lit shade,
the pad's mask). Template and picture are band-passed and the picture's contrast normalised locally, so a
pale ear and a pink ear score alike (paint_uv.find's pinkness cue failed on pale ears, F-P25-19). Masked
normalised cross-correlation over position (FFT), scale and rotation; coarse, then fine.
Writes the ears json probe3_field.py reads ({ear: dx, dy, s, rot}: the first pass at
c_hm - (dx,dy) + s * R(rot) * (p - c_hm) is what lands on hm08's pad point p) and a check picture.
usage: python probe4_earfind.py <first_pass_island.png> <uv_frame.json> <shape_dir> <out.json> [check.png] [cue: shade|depth] [pad_erosion_px 6]"""
import json, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, affine_transform, binary_erosion, sobel
from scipy.signal import correlate

pic, of, sd, outj = sys.argv[1:5]
chk = sys.argv[5] if len(sys.argv) > 5 else None
cue = sys.argv[6] if len(sys.argv) > 6 else "shade"
DEPTH_T = float(sys.argv[7]) if len(sys.argv) > 7 else 6     # pad erosion, px
F = json.load(open(of))
A = np.asarray(Image.open(pic).convert("RGB"), np.float64) / 255
L = A @ [0.299, 0.587, 0.114]

LO, HI = 2.5, 16.0      # coarser than pores, finer than the head's broad shading

def band(a, m=None, lo=LO, hi=HI):
    """band-pass; with a mask, by normalised convolution, so the mask's edge is not read as an edge"""
    if m is None:
        return gaussian_filter(a, lo) - gaussian_filter(a, hi)
    mf = m.astype(float)
    g = lambda s: gaussian_filter(a * mf, s) / np.maximum(gaussian_filter(mf, s), 1e-6)
    return g(lo) - g(hi)

Ib = band(L)    # no contrast boost: the masked NCC normalises each position, so a pale ear scores as a pink one

def ncc_map(I, t, m):
    n = m.sum()
    t = np.where(m, t - t[m].mean(), 0); t /= np.sqrt((t ** 2).sum()) + 1e-12
    cross = correlate(I, t, mode="valid", method="fft")
    s1 = correlate(I, m.astype(float), mode="valid", method="fft")
    s2 = correlate(I ** 2, m.astype(float), mode="valid", method="fft")
    return cross / np.sqrt(np.maximum(s2 - s1 ** 2 / n, 1e-9))

def warp_t(t, m, s, deg):
    """template scaled by s and turned by deg about its centre, on a canvas big enough to hold it"""
    h, w = t.shape; size = int(np.ceil(max(h, w) * s * 1.45)) | 1
    th = np.deg2rad(deg); Rm = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
    c_out = np.array([size / 2, size / 2]); c_in = np.array([h / 2, w / 2])
    Minv = np.linalg.inv(Rm * s)                               # (row, col) out -> in
    off = c_in - Minv @ c_out
    tt = affine_transform(t, Minv, off, order=1, output_shape=(size, size))
    mm = affine_transform(m.astype(float), Minv, off, order=1, output_shape=(size, size)) > 0.5
    return tt, mm, Minv, off

res, boxes = {}, {}
for side in ("ear_r", "ear_l"):
    S = np.load(f"{sd}/hm08_{side}_shape.npz")
    x0, x1, y0, y1 = [int(v) for v in S["box"]]
    pad = S["mask"][y0:y1, x0:x1]
    m = binary_erosion(pad, iterations=int(DEPTH_T))          # the pad, its outer few pixels dropped
    t = band(S[cue][y0:y1, x0:x1].astype(np.float64), pad) * m
    f = F["features"][side]
    chm = np.array([(y0 + y1) / 2, (x0 + x1) / 2])            # template centre (row, col) in the frame
    # search window: generous around the pad (seed 101's drawn ear sat 60 mm off), never into the face
    wy0, wy1 = int(f["cy"] - 260), int(f["cy"] + 260)
    if side == "ear_r": wx0, wx1 = int(f["cx"] - 330), int(f["cx"] + 260)
    else:               wx0, wx1 = int(f["cx"] - 260), int(f["cx"] + 330)
    wy0, wx0 = max(wy0, 0), max(wx0, 0); wy1, wx1 = min(wy1, L.shape[0]), min(wx1, L.shape[1])
    # the template stays fixed (same pixel count for every candidate: a shrinking template scores higher
    # on any local texture); the picture window is resampled instead: Iw(u) = Ib(c + s R (u - c))
    wc = np.array([(wy0 + wy1) / 2, (wx0 + wx1) / 2])
    best = (-9, None)
    def tryit(s, deg, asp=1.0):
        global best
        th = np.deg2rad(deg); Rm = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        Sd = np.diag([s / np.sqrt(asp), s * np.sqrt(asp)])          # (row, col): asp > 1 = the drawn ear wider
        hh, ww = int((wy1 - wy0) / Sd[0, 0]), int((wx1 - wx0) / Sd[1, 1])
        if hh <= t.shape[0] + 2 or ww <= t.shape[1] + 2: return
        uc = np.array([hh / 2, ww / 2])
        Mf = Rm @ Sd
        Iw = affine_transform(Ib, Mf, wc - Mf @ uc, order=1, output_shape=(hh, ww), mode="nearest")
        r = ncc_map(Iw, t, m); k = np.unravel_index(np.argmax(r), r.shape)
        if r[k] > best[0]:
            u = np.array(k) + np.array(t.shape) / 2                 # template centre in the resampled window
            best = (float(r[k]), (s, deg, asp, wc + Mf @ (u - uc), Mf))
    for s in np.arange(0.8, 2.41, 0.08):
        for deg in range(-24, 25, 8):
            for asp in (0.8, 1.0, 1.2, 1.45, 1.75): tryit(s, deg, asp)
    s0, d0, a0 = best[1][:3]
    for s in np.arange(s0 - 0.08, s0 + 0.081, 0.02):
        for deg in np.arange(d0 - 6, d0 + 6.1, 2):
            for asp in a0 * np.array([0.9, 0.95, 1.0, 1.05, 1.1]): tryit(s, deg, asp)
    sc, (s, deg, asp, found, Mf) = best[0], best[1]
    # map: hm08 pad point p -> picture point q = found + s R (p - chm); probe3_field form: c_hm=(cx,cy) of
    # the feature, so express with that centre
    c_hm = np.array([f["cy"], f["cx"]])
    q_of_chm = found + Mf @ (c_hm - chm)
    # M: the 2x2 (x, y) matrix taking (p - c_hm) on hm08's pad to the picture's offset from q_of_chm
    Mxy = np.array([[Mf[1, 1], Mf[1, 0]], [Mf[0, 1], Mf[0, 0]]])
    res[side] = {"dx": float(c_hm[1] - q_of_chm[1]), "dy": float(c_hm[0] - q_of_chm[0]), "s": float(s), "rot": float(deg),
                 "aspect": float(asp), "M": Mxy.tolist(), "score": round(sc, 3)}
    boxes[side] = (S, x0, x1, y0, y1, found, Mf, chm)
    print(f"{side}: score {sc:.3f}  move {np.hypot(res[side]['dx'], res[side]['dy']) * F['mm_per_px']:.1f} mm  size x{s:.2f}  wider x{asp:.2f}  turn {deg:+.1f} deg")
json.dump(res, open(outj, "w"), indent=1)
if chk:   # the window with hm08's ear (its ridges, from the shade) drawn where the finder put it
    tiles = []
    for side in ("ear_r", "ear_l"):
        S, x0, x1, y0, y1, found, Mf, chm = boxes[side]
        sh = S["shade"]; g = np.hypot(sobel(gaussian_filter(sh, 1.0), 0), sobel(gaussian_filter(sh, 1.0), 1))
        ys, xs = np.nonzero((g > np.percentile(g[S["mask"]], 70)) & binary_erosion(S["mask"], iterations=4))
        pts = np.stack([ys, xs], 1) - chm
        q = found + (Mf @ pts.T).T
        cy, cx = found.astype(int)
        crop = (A[max(cy - 150, 0):cy + 150, max(cx - 150, 0):cx + 150] * 255).astype(np.uint8)
        im = Image.fromarray(crop).resize((600, 600), Image.LANCZOS); dr = ImageDraw.Draw(im)
        for yy, xx in q:
            u, v = (xx - (cx - 150)) * 2, (yy - (cy - 150)) * 2
            dr.point((u, v), fill=(0, 255, 255))
        tiles.append(im)
    o = Image.new("RGB", (1210, 600), (40, 40, 40)); o.paste(tiles[0], (0, 0)); o.paste(tiles[1], (610, 0)); o.save(chk)
