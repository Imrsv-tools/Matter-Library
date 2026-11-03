#!/usr/bin/env python3
"""Phase27 Pass 2 probe: N views of hm08's body in ONE picture (throwaway; ML_P27_D1).

    MATTER_SKIN_N=2048 uv run python -I body4.py prep  <out> <layout>
    python3 -I body.py paint <out> <out>/in_<layout>.png <layout> <prompt key> <strengths> <seed>
    MATTER_SKIN_N=2048 uv run --with scipy python -I body4.py back <out> <layout> <picture> <tag>

Each atlas texel of the body island takes its colour from the view that faces it most squarely
among those that see it AND where the model's picture shows the body (not its background).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import body as B  # noqa: E402

LAYOUTS = {   # pixels per metre, height, [(yaw, width)]
    "fb": (800.0, 1536, [(0, 832), (180, 832)]),
    "f4": (600.0, 1152, [(0, 624), (90, 360), (180, 624), (270, 360)]),
}
B.PROMPTS["f4"] = B.PROMPTS["fb"].replace(
    "shown twice side by side: on the left seen from the front, on the right seen from the back",
    "shown four times side by side: seen from the front, in profile from her side, from the back, and in "
    "profile from her other side")
assert B.PROMPTS["f4"] != B.PROMPTS["fb"]


def cmd_prep(out: Path, lay: str):
    import numpy as np
    s, h, views = LAYOUTS[lay]
    A = np.load(out / "atlas.npz")
    C = A["C"].astype(np.float64)
    P, vt, T, vn = B.mesh()
    W = sum(w for _, w in views)
    pic = np.full((h, W, 3), 0.18)
    x = 0
    for yaw, w in views:
        g = B.raster(P, vt, T, vn, yaw, s, w, h)
        np.savez(out / f"geom_{lay}_{yaw}.npz", **g)
        col = B.sample(C, g["uv"]) * B.shade(g["n"])[..., None]
        part = pic[:, x:x + w]
        part[g["mask"]] = col[g["mask"]]
        x += w
    B.save(out / f"in_{lay}.png", pic)
    print(f"in_{lay}.png {W}x{h}")


def cmd_back(out: Path, lay: str, picture: Path, tag: str, sigma: float = 0.0):
    import numpy as np
    from PIL import Image
    s, h, views = LAYOUTS[lay]
    W = sum(w for _, w in views)
    A = np.load(out / "atlas.npz")
    C, Pa, Na, body = A["C"].astype(np.float64), A["P"], A["N"], A["body"]
    raw = np.asarray(Image.open(picture).convert("RGB").resize((W, h), Image.LANCZOS), np.float64)
    bg = np.median(np.concatenate([raw[:40].reshape(-1, 3), raw[:, :20].reshape(-1, 3)]), 0)
    fg = np.abs(raw - bg).max(-1) > 18
    pic = B.lin(raw / 255)
    if sigma:   # the skin's detail only: the picture over its own blur (inside the body), times C below
        from scipy.ndimage import gaussian_filter
        m = fg.astype(float)
        low = np.stack([gaussian_filter(pic[..., k] * m, sigma) for k in range(3)], -1) / np.maximum(gaussian_filter(m, sigma), 1e-6)[..., None]
        pic = pic / np.maximum(low, 1e-4)
    rr, cc = np.nonzero(body)
    X, Nn = Pa[rr, cc].astype(np.float64), Na[rr, cc].astype(np.float64)
    got = np.zeros((len(rr), 3)); face = np.zeros(len(rr)); have = np.zeros(len(rr), bool)
    x = 0
    for yaw, w in views:
        g = np.load(out / f"geom_{lay}_{yaw}.npz")
        px, py, z, _ = B.proj(X, yaw, s, w, h)
        nz = (Nn @ B.rot(yaw).T)[:, 2]
        xi, yi = np.clip(px.astype(int), 0, w - 1), np.clip(py.astype(int), 0, h - 1)
        vis = (z <= g["z"][yi, xi] + 0.004) & (nz > 0) & fg[:, x:x + w][yi, xi]
        take = vis & (nz > face)
        uv = np.stack([px / w, py / h], -1)
        got[take] = B.sample(pic[:, x:x + w], uv[take]); face[take] = nz[take]; have |= take
        x += w
    sh = np.zeros_like(C); kn = np.zeros(C.shape[:2], bool)
    sh[rr[have], cc[have]] = got[have]; kn[rr[have], cc[have]] = True
    D = C.copy()
    D[body] = B.pushpull(sh, kn)[body] * (C[body] if sigma else 1)
    k = C[body].mean(0) / D[body].mean(0)
    D[body] *= k
    np.save(out / f"D_{tag}.npy", D.astype(np.float32))
    print(f"D_{tag}: seen {have.mean() * 100:.1f} %, under 0.3 {(have & (face < 0.3)).mean() * 100:.1f} %, gain {np.round(k, 3)}")


if __name__ == "__main__":
    c, out = sys.argv[1], Path(sys.argv[2])
    if c == "prep":
        cmd_prep(out, sys.argv[3])
    elif c == "back":
        cmd_back(out, sys.argv[3], Path(sys.argv[4]), sys.argv[5], float(sys.argv[6]) if len(sys.argv) > 6 else 0.0)
