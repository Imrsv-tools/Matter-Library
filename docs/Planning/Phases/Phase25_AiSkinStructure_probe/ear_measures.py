"""Per-texel ear measures from hm08's geometry, and the bar's colour on them (P25 Pass 3, RD-P25-18 probe).
usage: ear_measures.py <head_fields_8192.npz> <bar basecolor.png> <out.npz>"""
import sys, json
import numpy as np
from PIL import Image
from scipy.spatial import cKDTree
hf, barp, out = sys.argv[1:4]
z = np.load(hf); idx = z["idx"]; P = z["P"].astype(np.float64); Nn = z["N"].astype(np.float64)
ears = z["ears"] > 0.5; face = z["face"] > 0.9
Image.MAX_IMAGE_PIXELS = None
bar = np.asarray(Image.open(barp).convert("RGB"))
def lin(s): s = s / 255.0; return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)
col = lin(bar.reshape(-1, 3)[idx].astype(np.float64))
fc = col[face].mean(0); print("bar face core (linear):", fc.round(4))
res = {}
for side, sg in (("r", -1), ("l", 1)):
    e = ears & (np.sign(P[:, 0]) == sg)
    ei = np.flatnonzero(e)
    Pe, Ne = P[ei], Nn[ei]
    # the skull near the ear: head texels outside the ear mask within 6 cm of its centre
    c = Pe.mean(0)
    near = np.flatnonzero(~ears & (np.linalg.norm(P - c, axis=1) < 0.06))
    sk = cKDTree(P[near])
    stand = sk.query(Pe)[0]                                  # how far the texel stands off the skull (m)
    # front (faces away from the skull, laterally) vs back (faces the skull), from the normal
    front0 = (sg * Ne[:, 0]) > 0
    # thickness: distance to the nearest texel of the OTHER side (front <-> back)
    thick = np.empty(len(ei))
    for a in (True, False):
        src, dst = front0 == a, front0 != a
        thick[src] = cKDTree(Pe[dst]).query(Pe[src])[0]
    # front (faces away from the skull, laterally) vs back (faces the skull)
    front = front0
    r = col[ei] / fc
    res[side] = dict(ei=ei, stand=stand, thick=thick, front=front, ratio=r)
    print(f"ear {side}: {len(ei)} texels; stand mm p5/50/95 {np.percentile(stand,[5,50,95]).round(4)*1000}; "
          f"thick found {np.isfinite(thick).mean():.2f}, mm p5/50/95 {np.nanpercentile(thick,[5,50,95]).round(4)*1000}; front {front.mean():.2f}")
    for nm, sel in (("front", front), ("back", ~front)):
        print(f"   {nm}: bar/face ratio mean {r[sel].mean(0).round(3)}  (n {sel.sum()})")
    # gradient: the front by stand-off bins
    qs = np.percentile(stand[front], [0, 20, 40, 60, 80, 100])
    for a, b in zip(qs[:-1], qs[1:]):
        s = front & (stand >= a) & (stand <= b)
        print(f"   front stand {a*1000:5.1f}-{b*1000:5.1f} mm: ratio {r[s].mean(0).round(3)}  R/G {r[s,0].mean()/r[s,1].mean():.3f}")
np.savez(out, **{f"{s}_{k}": v for s in res for k, v in res[s].items()}, face_core=fc)
