"""Linear PFM (the runtime's capture) -> 8-bit sRGB PNG, the plain encode Storm and Blender use.

    uv run python pfm_to_png.py in.pfm out.png [--exposure STOPS]
Prints the linear mean and the centre pixel, so a run can be compared by number.
"""
import sys

import numpy as np
from PIL import Image


def read_pfm(path):
    with open(path, "rb") as f:
        kind = f.readline().strip()
        w, h = map(int, f.readline().split())
        scale = float(f.readline())
        data = np.frombuffer(f.read(), dtype="<f4" if scale < 0 else ">f4")
    ch = 3 if kind == b"PF" else 1
    return np.flipud(data.reshape(h, w, ch))


def srgb(x):
    x = np.clip(x, 0.0, 1.0)
    return np.where(x <= 0.0031308, 12.92 * x, 1.055 * np.power(x, 1 / 2.4) - 0.055)


def main(argv):
    src, dst = argv[0], argv[1]
    stops = float(argv[argv.index("--exposure") + 1]) if "--exposure" in argv else 0.0
    lin = read_pfm(src) * (2.0 ** stops)
    Image.fromarray((srgb(lin) * 255.0 + 0.5).astype(np.uint8)).save(dst)
    h, w, _ = lin.shape
    print(f"{src}: {w}x{h} mean={lin.mean():.6f} max={lin.max():.4f} centre={lin[h // 2, w // 2]}")


if __name__ == "__main__":
    main(sys.argv[1:])
