"""P25 re-discovery probe: the island picture with hm08's lips and lid slits drawn strongly (uv_Ccue.png), after prep.py.

    uv run python -I <this> <out dir>          then:  UV_SRC=uv_Ccue.png python3 -I gen_uv.py <out dir> cue 0.6,0.75,0.9 7
"""
import json
import sys
from pathlib import Path
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
REPO = Path(__file__).resolve().parents[4]
OUT = Path(sys.argv[1]); N = 8192
prep = json.load(open(OUT / "uv_prep.json")); y0, y1, x0, x1 = prep["bbox"]; W, H = prep["size"]
z = np.load(REPO / "library/parity/P25_Views/head_fields_8192.npz")
r, c = np.divmod(z["idx"], N); k = (c >= 5100) & (r < 7150)


def frame(key):
    m = np.zeros((y1 - y0, x1 - x0), np.float32); m[r[k] - y0, c[k] - x0] = z[key][k]
    return np.asarray(Image.fromarray(m).transpose(Image.Transpose.ROTATE_270).resize((W, H), Image.BILINEAR))


lips, lids = frame("lips"), frame("lids")
np.save(OUT / "lipsmask.npy", lips); np.save(OUT / "lidsmask.npy", lids)
a = np.asarray(Image.open(OUT / "uv_C.png").convert("RGB"), np.float32)
lip = np.clip((lips - 0.3) / 0.4, 0, 1)[..., None]; a = a * (1 - 0.8 * lip) + np.array([150, 70, 80]) * 0.8 * lip
slit = np.clip((lids - 0.8) / 0.15, 0, 1)[..., None]; a = a * (1 - 0.9 * slit) + np.array([60, 40, 40]) * 0.9 * slit
Image.fromarray(a.clip(0, 255).astype(np.uint8)).save(OUT / "uv_Ccue.png")
