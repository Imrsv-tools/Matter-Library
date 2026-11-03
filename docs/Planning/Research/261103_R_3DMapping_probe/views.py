"""Cut Phase27's four-view picture into Pixal3D's four square views (RGBA), on one shared rotation axis.

Usage: python views.py <f4 picture> <out dir>
The picture is orthographic, 600 px a metre; each panel's rotation axis is its middle column (project_body.proj).
Every view gets the same square frame: the body's height spans 1/1.1 of it, the axis in the middle column.
"""
import sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[4]   # docs/Planning/Research/<probe>/ -> the repo
import numpy as np
from PIL import Image
sys.path.insert(0, str(REPO / "tools/converters/fit"))
import project_body as pb

pic_path, out = Path(sys.argv[1]), Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
img, fg = pb.picture(pic_path)                      # linear colour, body mask, at the render's size
rgb = pb.srgb(img) if hasattr(pb, "srgb") else img
rows = np.nonzero(fg.any(1))[0]
top, bot = rows.min(), rows.max() + 1
H = bot - top
L = int(round(1.1 * H))
cy = (top + bot) / 2
names = {0: "front", 90: "left", 180: "back", 270: "right"}
for yaw, x0, w in pb.frames():
    canvas = np.zeros((L, L, 4))
    ys = np.arange(L) - L / 2 + cy                  # picture rows for each canvas row
    xs = np.arange(L) - L / 2 + x0 + w / 2          # picture columns, axis in the middle
    yi, xi = np.meshgrid(np.round(ys).astype(int), np.round(xs).astype(int), indexing="ij")
    ok = (yi >= 0) & (yi < img.shape[0]) & (xi >= x0) & (xi < x0 + w)
    m = np.zeros((L, L), bool)
    m[ok] = fg[yi[ok], xi[ok]]
    c = np.zeros((L, L, 3))
    c[ok] = np.clip(rgb[yi[ok], xi[ok]], 0, 1)
    canvas[..., :3] = c * m[..., None]
    canvas[..., 3] = m
    im = Image.fromarray((canvas * 255 + 0.5).astype(np.uint8), "RGBA").resize((1024, 1024), Image.LANCZOS)
    im.save(out / f"{names[yaw]}.png")
    print(names[yaw], "body px", int(m.sum()))
print(f"frame {L} px square for a body {H} px tall ({H / pb.S:.3f} m); 1024 px = {L / pb.S / 1024 * 1000:.2f} mm a pixel")
