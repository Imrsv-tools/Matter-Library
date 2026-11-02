"""Phase27 Pass 3 probe: the fine detail of 8K atlases seen through a region camera (std of log-luminance minus\nits Gaussian blur at 2, 6, 20 px, x1000, on the body away from the outline)."""
import sys, numpy as np
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools/converters/fit"))
import project_body as pb
from PIL import Image
from scipy.ndimage import gaussian_filter, binary_erosion
Image.MAX_IMAGE_PIXELS = None
O = Path(sys.argv[1]); name = sys.argv[2]; atl = sys.argv[3:]
g = np.load(O / f"geom_{name}.npz"); m = binary_erosion(g["mask"], iterations=24)
sh = pb.shade(g["n"])[..., None]
print("atlas through the region camera (0.39 mm px): hp2  hp6  hp20  (x1000, log-lum high-pass std)")
for p in atl:
    A = pb.lin(np.asarray(Image.open(p).convert("RGB"), np.float32) / 255); n = A.shape[0]
    v = pb.sample(A, g["uv"][..., 0] * n - 0.5, g["uv"][..., 1] * n - 0.5) * sh
    L = np.log(np.maximum(v @ [0.2126, 0.7152, 0.0722], 1e-4))
    r = [np.std((L - gaussian_filter(L, s))[m]) * 1000 for s in (2, 6, 20)]
    print(f"{Path(p).name:22s} " + "  ".join(f"{x:6.1f}" for x in r))
