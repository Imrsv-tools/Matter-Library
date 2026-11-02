"""P25 Pass 3 probe 5: the ear PROJECTED through the profile camera, as the face is through the front one.
hm08's ear in its profile render (geom_f-80 for the right ear, f+80 for the left; the ear pixels are those
whose texel is in head_fields' ear mask) is fitted onto the drawn ear's silhouette in the first-pass island
(probe4_earfit's segmentation; moved, sized, stretched, turned to the best overlap). Every visible ear pixel
then carries "where in the picture" to its own texel through its UV — the ear's front lands by
construction, however the UV squeezes it; its back (unseen) is left to the coordinate field.
Writes <out_dir>/proj_<ear>.npz (frame pixel -> island point) + ears json {ear: {proj: path}} for
probe3_field.py, and a check picture (hm08's rendered ear outline on the drawn ear).
usage: python probe5_earproj.py <first_pass_island.png> <uv_frame.json> <P25_Views dir> <out_dir> <tag> [pad_rim_px 12] [min_nz 0.05] [ease_px 6] [back_out 1.3]"""
import json, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import gaussian_filter, sobel, binary_closing, binary_fill_holes, label, binary_dilation, binary_erosion
from scipy.spatial import ConvexHull
from scipy.signal import correlate

pic, of, V, out, tag = sys.argv[1:6]
F = json.load(open(of)); y0, y1, x0, x1 = F["bbox"]; W, H = F["size"]
A = np.asarray(Image.open(pic).convert("RGB"), np.float64) / 255
Hd = np.load(f"{V}/head_fields_8192.npz")
earset = np.zeros(8192 * 8192, bool); earset[Hd["idx"][Hd["ears"] > 0.5]] = True

def hull_mask(m, shape):
    ys, xs = np.nonzero(m); h = ConvexHull(np.stack([xs, ys], 1))
    im = Image.new("L", (shape[1], shape[0]), 0)
    ImageDraw.Draw(im).polygon([(float(xs[i]), float(ys[i])) for i in h.vertices], fill=1)
    return np.asarray(im, bool)

def drawn_ear(side):
    f = F["features"][side]; cy, cx = int(f["cy"]), int(f["cx"])
    wy0, wy1 = max(cy - 280, 0), min(cy + 280, H)
    wx0, wx1 = (cx - 340, cx + 260) if side == "ear_r" else (cx - 260, cx + 340)
    wx0, wx1 = max(wx0, 0), min(wx1, W)
    Wn = A[wy0:wy1, wx0:wx1]
    G = sum(np.hypot(sobel(gaussian_filter(Wn[..., k], 4), 0), sobel(gaussian_filter(Wn[..., k], 4), 1)) for k in range(3))
    reg = binary_fill_holes(binary_closing(binary_dilation(G > np.percentile(G, 95), iterations=2), iterations=12))
    lab, _ = label(reg); sz = np.bincount(lab.ravel()); sz[0] = 0
    return hull_mask(lab == sz.argmax(), reg.shape), (wy0, wx0)

def pushpull(img, kn):
    if kn.all() or min(img.shape[:2]) < 2: return img
    h, w_ = img.shape[:2]; H2, W2 = (h + 1) // 2, (w_ + 1) // 2; c = img.shape[2]
    pi = np.zeros((H2 * 2, W2 * 2, c)); pk = np.zeros((H2 * 2, W2 * 2))
    pi[:h, :w_] = img * kn[..., None]; pk[:h, :w_] = kn
    si = pi.reshape(H2, 2, W2, 2, c).sum((1, 3)); sk = pk.reshape(H2, 2, W2, 2).sum((1, 3))
    low = pushpull(np.where(sk[..., None] > 0, si / np.maximum(sk, 1e-9)[..., None], 0), sk > 0)
    up = np.repeat(np.repeat(low, 2, 0), 2, 1)[:h, :w_]
    return np.where(kn[..., None], img, up)

PAD_RIM = int(sys.argv[6]) if len(sys.argv) > 6 else 12
MIN_NZ = float(sys.argv[7]) if len(sys.argv) > 7 else 0.05
EASE = float(sys.argv[8]) if len(sys.argv) > 8 else 6.0
BACK_OUT = float(sys.argv[9]) if len(sys.argv) > 9 else 1.3
SMOOTH = 3.0
EARM = Hd["ears"] > 0.5
_rr, _cc = np.divmod(Hd["idx"], 8192)
EX = (y1 - _rr - 0.5) * W / (y1 - y0) - 0.5; EY = (_cc - x0 + 0.5) * H / (x1 - x0) - 0.5
_r, _c = np.divmod(Hd["idx"][Hd["ears"] > 0.5], 8192)
PJX = np.clip(np.round((y1 - _r - 0.5) * W / (y1 - y0) - 0.5).astype(int), 0, W - 1)
PJY = np.clip(np.round((_c - x0 + 0.5) * H / (x1 - x0) - 0.5).astype(int), 0, H - 1)
res, tiles = {}, []
for side, view in (("ear_r", "f-80"), ("ear_l", "f+80")):
    g = np.load(f"{V}/geom_{view}.npz"); m, uv, n = g["mask"], g["uv"], g["n"]
    rr = np.clip((uv[..., 1] * 8192).astype(int), 0, 8191); cc = np.clip((uv[..., 0] * 8192).astype(int), 0, 8191)
    e = m & earset[rr * 8192 + cc]
    lab, _ = label(e); sz = np.bincount(lab.ravel()); sz[0] = 0; e = binary_fill_holes(lab == sz.argmax()) & m
    ey, ex = np.nonzero(e); c_r = np.array([ey.mean(), ex.mean()])
    eh = hull_mask(e, e.shape); hy, hx = np.nonzero(eh)
    pts = np.stack([hy, hx], 1) - c_r
    drawn, (wy0, wx0) = drawn_ear(side)
    s0 = np.sqrt(drawn.sum() / eh.sum()); nA = drawn.sum()
    best = (-1, None)
    def tryit(s, deg, asp):
        global best
        th = np.deg2rad(deg); Rm = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        Mf = Rm @ np.diag([s / np.sqrt(asp), s * np.sqrt(asp)])
        q = pts @ Mf.T; q0 = np.floor(q.min(0)).astype(int); qi = np.round(q - q0).astype(int)
        hh, ww = qi.max(0) + 1
        if hh >= drawn.shape[0] or ww >= drawn.shape[1]: return
        K = np.zeros((hh, ww)); K[qi[:, 0], qi[:, 1]] = 1; K = binary_closing(K > 0, iterations=1).astype(float)
        ov = correlate(drawn.astype(float), K, mode="valid", method="fft"); iou = ov / (nA + K.sum() - ov)
        k = np.unravel_index(np.argmax(iou), iou.shape)
        if iou[k] > best[0]:
            best = (float(iou[k]), (s, deg, asp, np.array([wy0 + k[0], wx0 + k[1]]) - q0, Mf))
    for s in s0 * np.arange(0.8, 1.21, 0.05):
        for deg in range(-24, 25, 4):
            for asp in (0.8, 0.9, 1.0, 1.1, 1.25): tryit(s, deg, asp)
    a0 = best[1]
    for s in a0[0] * np.arange(0.96, 1.041, 0.01):
        for deg in np.arange(a0[1] - 3, a0[1] + 3.1, 1):
            for asp in a0[2] * np.array([0.95, 1.0, 1.05]): tryit(s, deg, asp)
    iou, (s, deg, asp, centre, Mf) = best
    # every visible ear pixel: its texel's place in the frame <- the island point the fit puts it on
    w = np.clip((np.abs(n[ey, ex, 2]) - MIN_NZ) / 0.1, 0, 1)   # the bowl's walls are grazing from the side: keep them
    o = centre + (np.stack([ey, ex], 1) - c_r) @ Mf.T          # (row, col) in the island frame
    X = (y1 - rr[ey, ex] - 0.5) * W / (y1 - y0) - 0.5; Y = (cc[ey, ex] - x0 + 0.5) * H / (x1 - x0) - 0.5
    # each pixel spread over its four neighbouring texels (bilinear), not the nearest one: at grazing angles
    # a pixel spans a run of texels and nearest-rounding leaves stair-steps along the rim
    acc = np.zeros((H, W, 2)); wt = np.zeros((H, W))
    bx0, by0 = np.floor(X).astype(int), np.floor(Y).astype(int); fx_, fy_ = X - bx0, Y - by0
    for ddx, ddy, ww in ((0, 0, (1 - fx_) * (1 - fy_)), (1, 0, fx_ * (1 - fy_)), (0, 1, (1 - fx_) * fy_), (1, 1, fx_ * fy_)):
        jx, jy = bx0 + ddx, by0 + ddy; wv = w * ww
        k = (wv > 0) & (jx >= 0) & (jx < W) & (jy >= 0) & (jy < H)
        np.add.at(acc, (jy[k], jx[k]), o[k][:, ::-1] * wv[k, None]); np.add.at(wt, (jy[k], jx[k]), wv[k])
    good = wt > 0.05
    O = np.where(good[..., None], acc / np.maximum(wt, 1e-9)[..., None], 0)
    # holes inside the ear's front (folds the camera grazes): filled finely from their projected neighbours
    # the ear's front = what the profile camera sees (facing out from the head is NOT it: the ear's back
    # faces out too, the ear standing off the skull); its ragged grazing edge smoothed (blur, re-threshold)
    front = binary_fill_holes(binary_closing(good, iterations=3))
    front = gaussian_filter(front.astype(float), SMOOTH) > 0.5
    good &= front
    O = pushpull(O, good)
    for _ in range(300):   # then smooth the holes at full resolution (pull-push alone fills in squares)
        av = (np.roll(O, 1, 0) + np.roll(O, -1, 0) + np.roll(O, 1, 1) + np.roll(O, -1, 1)) / 4
        O = np.where(good[..., None], O, av)
    py, px = np.nonzero(front)
    # the whole pad (front and back) and a rim round it: held to the projection's best-fit affine, so the
    # ear's surround moves with it (no ghost of the picture's own ear); the projection exact on top
    gy, gx = np.nonzero(good)
    Xa = np.c_[gx, gy, np.ones(len(gx))]
    coef, *_ = np.linalg.lstsq(Xa, np.c_[O[gy, gx, 0], O[gy, gx, 1]], rcond=None)
    padm = np.zeros((H, W), bool); padm[PJY, PJX] = True
    padm = binary_dilation(binary_closing(padm, iterations=2), iterations=PAD_RIM) & (np.abs(np.arange(W)[None, :] - (F["features"][side]["cx"])) < 200)
    ay, ax = np.nonzero(padm & ~front)
    aff = np.c_[ax, ay, np.ones(len(ax))] @ coef
    # the ear's back and surround: the fitted move pushed out from the drawn ear's centre by BACK_OUT, so it
    # samples plain skin beyond the dark halo the model paints round an ear (still one coordinate, no blend)
    ec = centre[::-1]
    aff = ec + BACK_OUT * (aff - ec)
    # the front's edge: the projection eased into the fitted move over EASE px (a coordinate ramp, not a
    # colour blend), so the visible rim does not step against the ear's back (serrated helix, lobe step)
    if EASE > 0:
        from scipy.ndimage import distance_transform_edt
        dist = distance_transform_edt(front)
        wv = np.clip(dist[py, px] / EASE, 0, 1)[:, None]
        affF = ec + BACK_OUT * (np.c_[px, py, np.ones(len(px))] @ coef - ec)
        O[py, px] = wv * O[py, px] + (1 - wv) * affF
    np.savez_compressed(f"{out}/proj_{tag}_{side}.npz", px=np.r_[px, ax], py=np.r_[py, ay], ox=np.r_[O[py, px, 0], aff[:, 0]], oy=np.r_[O[py, px, 1], aff[:, 1]])
    res[side] = {"proj": f"{out}/proj_{tag}_{side}.npz", "iou": round(iou, 3), "s": round(float(s), 3), "rot": float(deg), "aspect": round(float(asp), 3)}
    print(f"{side}: overlap (IoU) {iou:.3f}; render->island x{s:.3f}, wider x{asp:.2f}, turn {deg:+.1f} deg; {good.sum()} texels of the island get the projection")
    # check: hm08's rendered ear outline (cyan) on the drawn ear, and the drawn hull (yellow)
    bnd = e & binary_dilation(~e, iterations=1); by, bx = np.nonzero(bnd)
    q = centre + (np.stack([by, bx], 1) - c_r) @ Mf.T
    dyy, dxx = np.nonzero(drawn & ~binary_erosion(drawn, iterations=1))
    cy, cx = centre.astype(int)
    im = Image.fromarray((A[cy - 160:cy + 160, cx - 160:cx + 160] * 255).astype(np.uint8)).resize((640, 640), Image.LANCZOS)
    dr = ImageDraw.Draw(im)
    for yy, xx in np.stack([dyy + wy0, dxx + wx0], 1): dr.point(((xx - cx + 160) * 2, (yy - cy + 160) * 2), fill=(255, 220, 0))
    for yy, xx in q: dr.point(((xx - cx + 160) * 2, (yy - cy + 160) * 2), fill=(0, 255, 255))
    tiles.append(im)
json.dump(res, open(f"{out}/earsP_{tag}.json", "w"), indent=1)
o_ = Image.new("RGB", (1290, 640), (40, 40, 40)); o_.paste(tiles[0], (0, 0)); o_.paste(tiles[1], (650, 0)); o_.save(f"{out}/chkP_{tag}.png")
