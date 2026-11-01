"""Snap hm08's MediaPipe eye-contour landmarks (front render) to the eye opening's real edge, found from depth.
usage: snap_eyes.py <geom_f000.npz> <lm_hm08.npy> <out.npy> <check.png> <render.png>"""
import sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
geom, lmi, out, chk, ren = sys.argv[1:6]
g = np.load(geom); Z = g["z"]; mask = g["mask"]
L = np.load(lmi).copy(); L0 = L.copy()
EYES = {"R": dict(up=[246, 161, 160, 159, 158, 157, 173], lo=[7, 163, 144, 145, 153, 154, 155], c=[33, 133]),
        "L": dict(up=[466, 388, 387, 386, 385, 384, 398], lo=[249, 390, 373, 374, 380, 381, 382], c=[263, 362])}
for side, E in EYES.items():
    ids = E["up"] + E["lo"] + E["c"]
    p = L[ids]
    x0, x1 = int(p[:, 0].min()) - 40, int(p[:, 0].max()) + 40
    y0, y1 = int(p[:, 1].min()) - 40, int(p[:, 1].max()) + 40
    z = Z[y0:y1, x0:x1]; mk = mask[y0:y1, x0:x1]
    ring = np.percentile(z[mk], 50)                       # the lids' depth (the box is mostly lid skin)
    sgn = np.sign(np.median(z[mk]) - np.median(Z[mask]))  # which way is "behind": compare to the whole head
    # the opening: pixels much further from the camera than the lids (or no surface at all)
    far = ~mk | (np.abs(z - ring) > 0.006)
    lab, nl = ndi.label(far)
    cy, cx = np.mean(p[:, 1]) - y0, np.mean(p[:, 0]) - x0
    k = lab[int(cy), int(cx)]
    if k == 0:  # landmarks' centre not inside: take the component nearest it
        d = ndi.distance_transform_edt(lab == 0, return_indices=True)[1]; k = lab[d[0][int(cy), int(cx)], d[1][int(cy), int(cx)]]
    op = ndi.binary_fill_holes(lab == k)
    ys, xs = np.nonzero(op)
    print(f"{side}: opening {op.sum()} px, x {xs.min()+x0}-{xs.max()+x0}, y {ys.min()+y0}-{ys.max()+y0}, centroid ({xs.mean()+x0:.1f}, {ys.mean()+y0:.1f})")
    cols = {}
    for xx in np.unique(xs):
        yy = ys[xs == xx]; cols[xx] = (yy.min() - 0.5, yy.max() + 0.5)
    xmin, xmax = xs.min(), xs.max()
    co = L0[E["c"], 0] - x0                               # the landmarks' own corners: each point keeps its relative place
    lo_c, hi_c = co.min(), co.max()
    def edge(i, which):
        t = np.clip((L0[i, 0] - x0 - lo_c) / (hi_c - lo_c), 0.04, 0.96)
        x = xmin + t * (xmax - xmin); xi = int(round(x))
        L[i] = [x + x0, cols[xi][which] + y0]
    for i in E["up"]: edge(i, 0)
    for i in E["lo"]: edge(i, 1)
    # corners: the opening's extreme columns, at their mid height
    for i in E["c"]:
        xe = xmin if abs(L[i, 0] - x0 - xmin) < abs(L[i, 0] - x0 - xmax) else xmax
        yy = ys[xs == xe]; L[i] = [xe + x0 + (0.5 if xe == xmin else -0.5) * -1, yy.mean() + y0]
    mv = np.abs(L[ids] - L0[ids]).max(0)
    print(f"   moved up to dx {mv[0]:.1f}, dy {mv[1]:.1f} px; upper mean y {L0[E['up'],1].mean():.1f} -> {L[E['up'],1].mean():.1f}, lower {L0[E['lo'],1].mean():.1f} -> {L[E['lo'],1].mean():.1f}")
np.save(out, L)
im = Image.open(ren).convert("RGB"); x0, y0, x1, y1 = 650, 920, 1400, 1100
c = im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * 2, (y1 - y0) * 2)); d = ImageDraw.Draw(c)
for E in EYES.values():
    for i in E["up"] + E["lo"] + E["c"]:
        for P, col in ((L0, (255, 0, 0)), (L, (0, 255, 0))):
            x, y = (P[i] - [x0, y0]) * 2; d.ellipse([x - 3, y - 3, x + 3, y + 3], fill=col)
c.save(chk)
