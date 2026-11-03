# How much of the body only grazing cameras see, and how well the model's silhouette keeps hm08's.
import sys, numpy as np
from pathlib import Path
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
import body as B
out = Path(sys.argv[1])
A = np.load(out / "atlas.npz"); body = A["body"]; Nn = A["N"][body].astype(float)
best = np.maximum(np.abs(Nn[:, 2]), 0)
for t in (0.2, 0.3, 0.5):
    print(f"body texels whose best camera faces them under {t}: {(best < t).mean() * 100:.1f} %")
for s in sys.argv[2:]:
    pic = np.asarray(Image.open(out / f"fb_s{s}_seed7.png").convert("RGB").resize((2 * B.HW, B.HH)), float)
    bg = np.median(np.concatenate([pic[:40].reshape(-1, 3), pic[:, :20].reshape(-1, 3)]), 0)
    fg = np.abs(pic - bg).max(-1) > 18
    for i, yaw in enumerate((0, 180)):
        m = np.load(out / f"geom_{yaw}.npz")["mask"]
        f = fg[:, i * B.HW:(i + 1) * B.HW]
        rows = slice(int(B.HH * 0.25), int(B.HH * 0.85))              # neck to shin: the body island's span
        mm, ff = m[rows], f[rows]
        iou = (mm & ff).sum() / (mm | ff).sum()
        print(f"s{s} {'front' if yaw == 0 else 'back'}: silhouette IoU {iou:.3f}; hm08 pixels on the model's background {(mm & ~ff).sum() / mm.sum() * 100:.1f} %")
