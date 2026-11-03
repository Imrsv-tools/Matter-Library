# Premise probe (ML_P27_D1): hm08's atlas at 2048 coloured by which way each texel faces
# (front = red, back = blue, sideways = green) with island outlines, to read the body island's layout.
import sys, numpy as np
from pathlib import Path
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('.')   # the scratch folder
from PIL import Image
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools" / "converters" / "fit"))
import gen_synth_skin as gss, make_kits
m = make_kits.load_mesh(gss.MESH)
P, Nr, cv, cover = gss.rasterise(m)
lab = np.load(str(OUT / "lab2048.npy"))
n = Nr / np.maximum(np.linalg.norm(Nr, axis=-1, keepdims=True), 1e-9)
img = np.zeros(cover.shape + (3,))
img[..., 0] = np.clip(n[..., 2], 0, 1)
img[..., 2] = np.clip(-n[..., 2], 0, 1)
img[..., 1] = 1 - np.abs(n[..., 2])
img[~cover] = 0.12
edge = (lab != np.roll(lab, 1, 0)) | (lab != np.roll(lab, 1, 1))
img[edge & cover] = 1
# height bands every 0.1 m as thin grey lines
y = P[..., 1]
band = (np.abs((y * 10) - np.round(y * 10)) < 0.03) & cover
img[band] = img[band] * 0.4
Image.fromarray((img * 255).astype(np.uint8)).save(str(OUT / "layout_facing.png"))
print("ok")
