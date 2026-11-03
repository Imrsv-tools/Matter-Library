# Premise probe (ML_P27_D1): every UV seam of hm08, from the mesh itself — 3D edges whose two faces
# carry different UVs — tallied by the pair of islands they join, with each seam's length in metres.
import sys, numpy as np
from pathlib import Path
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')   # the scratch folder
from collections import defaultdict
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools" / "converters" / "fit"))
import gen_synth_skin as gss, make_kits
m = make_kits.load_mesh(gss.MESH)
isl = make_kits.islands(m)
pts = np.asarray(m["points"], float)
faces = m["faces"]
edge = defaultdict(list)          # (v0,v1) -> [(face, uv0, uv1)]
for fi, f in enumerate(faces):
    n = len(f)
    for k in range(n):
        (a, ua), (b, ub) = f[k], f[(k + 1) % n]
        key = (a, b) if a < b else (b, a)
        uvs = (ua, ub) if a < b else (ub, ua)
        edge[key].append((fi, uvs))
names = {}
for fi, f in enumerate(faces):
    names.setdefault(isl[fi], []).append(fi)
def where(i):
    v = np.array([pts[a] for fi in names[i] for a, _ in faces[fi]])
    return f"y {v[:,1].min():+.2f}..{v[:,1].max():+.2f} x {v[:,0].min():+.2f}..{v[:,0].max():+.2f}"
print("islands:", {i: (len(names[i]), where(i)) for i in sorted(names)})
seam = defaultdict(float); open_ = defaultdict(float)
for (a, b), lst in edge.items():
    L = float(np.linalg.norm(pts[a] - pts[b]))
    if len(lst) == 1:
        open_[isl[lst[0][0]]] += L; continue
    (f0, u0), (f1, u1) = lst[0], lst[1]
    if u0 != u1:
        seam[tuple(sorted((isl[f0], isl[f1])))] += L
for k, L in sorted(seam.items(), key=lambda t: -t[1]):
    print("seam islands", k, f"{L:.2f} m")
for k, L in open_.items():
    print("open border island", k, f"{L:.2f} m")
# where the body island's own seam runs: midpoints, bucketed
mids = []
for (a, b), lst in edge.items():
    if len(lst) == 2 and isl[lst[0][0]] == 3 and isl[lst[1][0]] == 3 and lst[0][1] != lst[1][1]:
        mids.append(((pts[a] + pts[b]) / 2, float(np.linalg.norm(pts[a] - pts[b]))))
M = np.array([p for p, _ in mids]); Lm = np.array([l for _, l in mids])
def lab(p):
    x, y, z = p
    if y > 0.35 and abs(x) > 0.17: part = "arm"
    elif y < -0.05 and abs(x) > 0.02: part = "leg"
    elif y > 0.5: part = "neck/shoulder"
    else: part = "trunk"
    side = "midline-front" if abs(x) < 0.015 and z > 0 else "midline-back" if abs(x) < 0.015 else ("front" if z > 0.03 else "back" if z < -0.03 else "side")
    return part, side
tally = defaultdict(float)
for p, l in zip(M, Lm):
    tally[lab(p)] += l
for k, v in sorted(tally.items(), key=lambda t: -t[1]): print("body self-seam", k, f"{v:.2f} m")
print("x range", M[:,0].min(), M[:,0].max(), "z", M[:,2].min(), M[:,2].max())
