# Coverage of the body island by 2 views (front, back) vs 4 (front, both profiles, back), with occlusion.
import sys, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import body as B
out = Path(sys.argv[1])
A = np.load(out / "atlas.npz"); body = A["body"]
rr, cc = np.nonzero(body); X = A["P"][rr, cc].astype(float); Nn = A["N"][rr, cc].astype(float)
P, vt, T, vn = B.mesh()
face = {}
for yaw in (0, 90, 180, 270):
    g = B.raster(P, vt, T, vn, yaw, w=1200)
    px, py, z, _ = B.proj(X, yaw, w=1200)
    nz = (Nn @ B.rot(yaw).T)[:, 2]
    xi, yi = np.clip(px.astype(int), 0, 1199), np.clip(py.astype(int), 0, B.HH - 1)
    vis = (z <= g["z"][yi, xi] + 0.004) & (nz > 0)
    face[yaw] = np.where(vis, nz, 0)
for name, ys in (("2 views", (0, 180)), ("4 views", (0, 90, 180, 270))):
    best = np.max([face[y] for y in ys], 0)
    print(name, " ".join(f"<{t}: {(best < t).mean() * 100:.1f}%" for t in (0.05, 0.3, 0.5)))
