"""P25 re-discovery probe: a UV-space picture of the head island back into the subject's 8K atlas (linear albedo .npy).

    uv run --directory <repo> python -I <this> <out dir> <picture name> <tag>
Writes <out dir>/render/albedo_<tag>.npy for project_views.py render. Head island texels take the picture,
held to the subject's face-core tone; everything else stays C.
"""
import json
import sys
from pathlib import Path
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
REPO = Path(__file__).resolve().parents[4]
OUT = Path(sys.argv[1]); PIC = sys.argv[2]; TAG = sys.argv[3]
N = 8192
HELD = np.array([0.6437, 0.3454, 0.2526])
def lin(s): return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)

prep = json.load(open(OUT / "uv_prep.json"))
y0, y1, x0, x1 = prep["bbox"]
k = np.array(prep["scale"])
z = np.load(REPO / "library/parity/P25_Views/head_fields_8192.npz")
idx, face = z["idx"], z["face"]
r, c = np.divmod(idx, N); keep = (c >= 5100) & (r < 7150); idx, face, r, c = idx[keep], face[keep], r[keep], c[keep]
pic = Image.open(OUT / f"{PIC}.png").convert("RGB").transpose(Image.Transpose.ROTATE_90).resize((x1 - x0, y1 - y0), Image.LANCZOS)
p = lin(np.asarray(pic, np.float64) / 255)[r - y0, c - x0]
p *= HELD / p[face > 0.9].mean(0)
atlas = lin(np.asarray(Image.open(REPO / "MatterLibrary/textures/fit/makehuman/skin/SkinTone34_basecolor_sUKN.png"), np.float32) / 255)
atlas = (atlas * k).astype(np.float32)          # C at the held tone, as the renderer's base is
flat = atlas.reshape(-1, 3); flat[idx] = p
(OUT / "render").mkdir(exist_ok=True)
np.save(OUT / "render" / f"albedo_{TAG}.npy", atlas)
print(TAG, "face core", p[face > 0.9].mean(0).round(4))
