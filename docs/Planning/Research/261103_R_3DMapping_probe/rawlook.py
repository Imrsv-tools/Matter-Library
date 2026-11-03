"""Point-splat renders of Pixal3D's own painted mesh (no transfer): face front, feet from above-front."""
import sys, json, struct
from pathlib import Path
import numpy as np
from PIL import Image

def glb_attr(path, name):
    b = path.read_bytes(); n = struct.unpack("<I", b[12:16])[0]; j = json.loads(b[20:20 + n]); bin0 = 20 + n + 8
    acc = j["accessors"][j["meshes"][0]["primitives"][0]["attributes"][name]]; bv = j["bufferViews"][acc["bufferView"]]
    c = {"VEC3": 3, "VEC4": 4}[acc["type"]]
    return np.frombuffer(b, np.float32, acc["count"] * c, bin0 + bv.get("byteOffset", 0) + acc.get("byteOffset", 0)).reshape(-1, c).astype(np.float64)

glb, out = Path(sys.argv[1]), Path(sys.argv[2])
V = glb_attr(glb, "POSITION"); C = glb_attr(glb, "COLOR_0")[:, :3]; N = glb_attr(glb, "NORMAL")
lo, hi = V.min(0), V.max(0); H = hi[1] - lo[1]
print("extent", (hi - lo).round(3))
srgb = lambda x: np.where(x <= 0.0031308, x * 12.92, 1.055 * np.clip(x, 0, 1) ** (1 / 2.4) - 0.055)

def render(name, center, size, pitch, res=900):
    a = np.radians(pitch)
    R = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    P = (V - center) @ R.T; n = N @ R.T
    keep = (np.abs(P[:, 0]) < size / 2) & (np.abs(P[:, 1]) < size / 2) & (n[:, 2] > 0)
    P, c = P[keep], C[keep]
    px = ((P[:, 0] / size + 0.5) * res).astype(int); py = ((0.5 - P[:, 1] / size) * res).astype(int)
    img = np.full((res, res, 3), 0.3); zb = np.full((res, res), -1e9)
    order = np.argsort(P[:, 2])
    for dx in (0, 1):
        for dy in (0, 1):
            x = np.clip(px[order] + dx, 0, res - 1); y = np.clip(py[order] + dy, 0, res - 1)
            img[y, x] = c[order]; 
    Image.fromarray((srgb(img) * 255).astype(np.uint8)).save(out / f"raw_{name}.png")

top = hi[1]
render("face", np.array([0, top - 0.11 * H / 1.665, hi[2] - 0.05]), 0.32 * H / 1.665, 0)
render("feet", np.array([0, lo[1] + 0.05, 0.05]), 0.5 * H / 1.665, -45)
render("body", (lo + hi) / 2, H * 1.05, 0, 1200)
