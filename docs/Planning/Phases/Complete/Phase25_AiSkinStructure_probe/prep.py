"""P25 re-discovery probe: the head island of C's 8K atlas, at the subject's tone, upright, for a UV-space img2img.

    uv run --directory <repo> python <this> <out dir> [width]
"""
import sys
import json
from pathlib import Path
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
REPO = Path(__file__).resolve().parents[4]
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
WIDTH = int(sys.argv[2]) if len(sys.argv) > 2 else 2048
N = 8192
HELD = np.array([0.6437, 0.3454, 0.2526])

def lin(s): return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)
def srgb(l):
    l = np.clip(l, 0, 1); return np.where(l <= 0.0031308, l * 12.92, 1.055 * l ** (1 / 2.4) - 0.055)

z = np.load(REPO / "library/parity/P25_Views/head_fields_8192.npz")
idx, face = z["idx"], z["face"]
_r, _c = np.divmod(idx, N); _keep = (_c >= 5100) & (_r < 7150)   # the head island only
idx, face = idx[_keep], face[_keep]
C = np.asarray(Image.open(REPO / "MatterLibrary/textures/fit/makehuman/skin/SkinTone34_basecolor_sUKN.png")).reshape(-1, 3) / 255.0
Cl = lin(C[idx])
k = HELD / Cl[face > 0.9].mean(0)
print("scale to the held tone", k.round(3))
ys, xs = np.divmod(idx, N)
y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
print("head island bbox (rows, cols)", y0, y1, x0, x1)
img = np.empty((y1 - y0, x1 - x0, 3)); img[:] = (Cl * k).mean(0)       # outside: the island's mean
img[ys - y0, xs - x0] = Cl * k
mask = np.zeros(img.shape[:2], bool); mask[ys - y0, xs - x0] = True
pic = Image.fromarray((srgb(img) * 255 + 0.5).astype(np.uint8))
m = Image.fromarray(mask.astype(np.uint8) * 255)
rot = Image.Transpose.ROTATE_270                                    # top of the head (atlas left) to the top
pic, m = pic.transpose(rot), m.transpose(rot)
w, h = pic.size
H = int(round(h * WIDTH / w / 16)) * 16
pic.resize((WIDTH, H), Image.LANCZOS).save(OUT / "uv_C.png")
m.resize((WIDTH, H), Image.NEAREST).save(OUT / "uv_mask.png")
json.dump({"bbox": [int(y0), int(y1), int(x0), int(x1)], "rotate": "ROTATE_270", "size": [WIDTH, H], "scale": k.tolist()},
          open(OUT / "uv_prep.json", "w"), indent=1)
print("wrote", WIDTH, "x", H)
