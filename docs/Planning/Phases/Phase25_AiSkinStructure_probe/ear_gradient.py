"""P25 Pass 3 (RD-P25-18) probe: the ear's colour as a gradient through the maker's skin model, no picture.
Per ear texel, weights from hm08's geometry (ear_measures.py): ear proper (stand-off from the skull), rim
(thin: near the ear's back surface, on the front), lobe (the lowest part), back (faces the skull). Each
weight carries a pigment change (dlog melanin, dlog blood, d so2); the colour is Lut(...) over Lut at the
operating point, times the skin round the ear (the atlas's own ring texels, per side).
usage: uv run python ear_gradient.py <in atlas.png> <measures.npz> <params.json> <out atlas.png>"""
import json, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "tools" / "converters" / "fit"))
import numpy as np
from PIL import Image
import gen_synth_skin as g
Image.MAX_IMAGE_PIXELS = None
src, meas, prm, out = sys.argv[1:5]
Pm = json.load(open(prm)); z = np.load(meas)
hf = np.load(REPO / "library" / "parity" / "P25_Views" / "head_fields_8192.npz")
idx, P, FACEW, EARS = hf["idx"], hf["P"], hf["face"], hf["ears"] > 0.5
from scipy.spatial import cKDTree
FEATHER = Pm.get("join_mm", 10.0) / 1000            # the join to the picture, on head skin outside the ear
def allowed(fw): t = np.clip((Pm.get("face_max", 0.15) - fw) / 0.10, 0, 1); return t * t * (3 - 2 * t)   # 0 on the face
L = g.Lut(); m0 = L.use("Tone34"); B0 = g.BLOOD0
import gen_skin_maps as gm
reach = np.array([float(x) for x in json.loads((gm.RECIPES / "Skin_Tone34_Clean_Base_s001_v01.json").read_text())["subsurface_radius_scale"].split(",")])
T = g.SUBJECTS["Tone34"]["face"]              # the subject's measured regions (Phase24 24.2): each ear part borrows one
def col(v): return L(m0 * np.exp(v[..., 0]), B0 * np.exp(v[..., 1]), 0.8 + v[..., 2]) * np.clip(1 - v[..., 3:4] * reach, 0.2, 1.5)
face = np.array(T["face"]); c0 = col(face[None])[0]
A = np.asarray(Image.open(src).convert("RGB")).copy()
flat = A.reshape(-1, 3)
def lin(s): s = s / 255.0; return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)
def enc(x): x = np.clip(x, 0, 1); return np.where(x <= 0.0031308, 12.92 * x, 1.055 * x ** (1 / 2.4) - 0.055) * 255 + 0.5
def ramp(x, a, b): t = np.clip((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t)
for s in ("r", "l"):
    ei, stand, thick, front = z[s + "_ei"], z[s + "_stand"], z[s + "_thick"], z[s + "_front"]
    y = P[ei, 1]
    w_ear = ramp(stand * 1000, *Pm["ear_stand_mm"])
    ear_y = y[w_ear > 0.5]; lo, hi = ear_y.min(), ear_y.max()
    w = {"front": w_ear * front,
         "rim": w_ear * front * (1 - ramp(thick * 1000, *Pm["rim_thick_mm"])),
         "lobe": w_ear * (1 - ramp((y - lo) / (hi - lo), *Pm["lobe_frac"])),
         "back": w_ear * (~front)}
    v = np.tile(face, (len(ei), 1))
    for k in w:
        for reg in Pm["parts"].get(k, []):
            v = v + w[k][:, None] * np.array(T[reg])
    ratio = col(v) / c0
    ring = (stand * 1000 < 1.0)
    base = np.median(lin(flat[idx[ei][ring]].astype(float)), 0)
    cur = lin(flat[idx[ei]].astype(float))
    new = base * ratio
    # RD-P25-19 (the lead): the gradient owns the whole ear, rim and root, at full strength; the skin
    # round it and the join to the picture lie on head skin behind the jaw, never on the face
    a = np.maximum(ramp(stand * 1000, 0.5, 1.5), allowed(FACEW[ei]))[:, None]
    flat[idx[ei]] = enc(cur * (1 - a) + new * a).astype(np.uint8)
    c = P[ei].mean(0)
    out_i = np.flatnonzero(~EARS & (np.linalg.norm(P - c, axis=1) < 0.08))
    d = cKDTree(P[ei]).query(P[out_i])[0]
    keep = d < FEATHER; oi = out_i[keep]
    wo = (allowed(FACEW[oi]) * (1 - ramp(d[keep], 0, FEATHER)))[:, None]
    flat[idx[oi]] = enc(lin(flat[idx[oi]].astype(float)) * (1 - wo) + base * wo).astype(np.uint8)
    print(f"   join: {(wo[:, 0] > 0.01).sum()} head texels outside the ear; front ring kept as the picture: {(a[:, 0] < 0.5).sum()} ear-mask texels")
    print(f"ear {s}: base {base.round(3)}, ratio at full ear p50 {np.median(ratio[w_ear>0.95],0).round(3)}, rim texels {(w['rim']>0.5).sum()}, lobe {(w['lobe']>0.5).sum()}, back {(w['back']>0.5).sum()}")
Image.fromarray(A).save(out)
