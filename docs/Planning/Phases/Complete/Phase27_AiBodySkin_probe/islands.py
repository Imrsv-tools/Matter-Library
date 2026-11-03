# Premise probe (ML_P27_D1): hm08's UV islands at 2048 — count, size, and which body part each holds.
import sys, numpy as np
from pathlib import Path
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')   # the scratch folder
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools" / "converters" / "fit"))
import gen_synth_skin as gss, make_kits
m = make_kits.load_mesh(gss.MESH)
P, Nr, cv, cover = gss.rasterise(m)
from scipy import ndimage
lab, n = ndimage.label(cover)
sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
order = np.argsort(-sizes)
tot = cover.sum()
print("atlas", cover.shape, "covered", tot, "islands", n)
top = P[..., 1][cover].max()
for i in order[:40]:
    k = i + 1
    sel = lab == k
    rr, cc = np.nonzero(sel)
    p = P[sel]
    print(f"#{k:3d} {sizes[i]/tot*100:6.2f}%  rows {rr.min()}-{rr.max()} cols {cc.min()}-{cc.max()}  "
          f"y {p[:,1].min():.2f}..{p[:,1].max():.2f}  x {p[:,0].min():+.2f}..{p[:,0].max():+.2f}  z {p[:,2].min():+.2f}..{p[:,2].max():+.2f}")
print("small islands (<0.05%):", int((sizes/tot < 0.0005).sum()), "holding", f"{sizes[sizes/tot<0.0005].sum()/tot*100:.2f}%")
np.save(str(OUT / "lab2048.npy"), lab)
