"""The rig's checks: colour difference (CIEDE2000) and structure (SSIM) between two renders.

Same method as ``tools/conformance/codec_ab.py`` (sRGB -> XYZ -> Lab, then ΔE2000, plus a
luminance SSIM), in plain numpy: the ``colour`` package codec_ab imports is not installed
in either Python environment (measured 2026-09-26), and one formula does not justify a new
dependency. The ΔE2000 here is checked against Sharma, Wu & Dalal's published test pairs
(``self_test``; run ``python compare.py``).

Scoring is over the SUBJECTS only: the Blender driver renders ``mask.png``, one flat colour
per subject (sphere red, cube green, floor blue), from the same camera.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

REGIONS = {"sphere": 0, "cube": 1, "floor": 2}     # mask channel per subject


def read_rgb(p: Path) -> np.ndarray:
    return np.asarray(Image.open(p).convert("RGB"), dtype=np.float64) / 255.0


def srgb_to_lab(rgb: np.ndarray) -> np.ndarray:
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = lin @ m.T / np.array([0.95047, 1.0, 1.08883])      # D65 white
    f = np.where(xyz > (6 / 29) ** 3, np.cbrt(xyz), xyz / (3 * (6 / 29) ** 2) + 4 / 29)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], axis=-1)


def delta_e2000(lab1: np.ndarray, lab2: np.ndarray) -> np.ndarray:
    """CIEDE2000 (kL = kC = kH = 1), after Sharma, Wu & Dalal (2005)."""
    L1, a1, b1 = lab1[..., 0], lab1[..., 1], lab1[..., 2]
    L2, a2, b2 = lab2[..., 0], lab2[..., 1], lab2[..., 2]
    C1, C2 = np.hypot(a1, b1), np.hypot(a2, b2)
    Cb7 = ((C1 + C2) / 2) ** 7
    G = 0.5 * (1 - np.sqrt(Cb7 / (Cb7 + 25.0 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360
    dLp, dCp = L2 - L1, C2p - C1p
    dh = h2p - h1p
    dh = np.where(dh > 180, dh - 360, np.where(dh < -180, dh + 360, dh))
    dh = np.where(C1p * C2p == 0, 0.0, dh)
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dh / 2))
    Lbp, Cbp = (L1 + L2) / 2, (C1p + C2p) / 2
    hs = h1p + h2p
    hbp = np.where(C1p * C2p == 0, hs,
                   np.where(np.abs(h1p - h2p) <= 180, hs / 2,
                            np.where(hs < 360, (hs + 360) / 2, (hs - 360) / 2)))
    T = (1 - 0.17 * np.cos(np.radians(hbp - 30)) + 0.24 * np.cos(np.radians(2 * hbp))
         + 0.32 * np.cos(np.radians(3 * hbp + 6)) - 0.20 * np.cos(np.radians(4 * hbp - 63)))
    dth = 30 * np.exp(-(((hbp - 275) / 25) ** 2))
    Cb7p = Cbp ** 7
    Rc = 2 * np.sqrt(Cb7p / (Cb7p + 25.0 ** 7))
    Sl = 1 + 0.015 * (Lbp - 50) ** 2 / np.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -np.sin(np.radians(2 * dth)) * Rc
    return np.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2
                   + Rt * (dCp / Sc) * (dHp / Sh))


def ssim(a: np.ndarray, b: np.ndarray) -> float:
    """Global luminance SSIM over the given pixels (codec_ab's form)."""
    w = np.array([0.2126, 0.7152, 0.0722])
    la, lb = a @ w, b @ w
    mua, mub = la.mean(), lb.mean()
    va, vb = la.var(), lb.var()
    cov = ((la - mua) * (lb - mub)).mean()
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    return float(((2 * mua * mub + c1) * (2 * cov + c2)) / ((mua ** 2 + mub ** 2 + c1) * (va + vb + c2)))


def masks(mask_png: Path) -> dict[str, np.ndarray]:
    m = read_rgb(mask_png)
    out = {name: m[..., ch] > 0.5 for name, ch in REGIONS.items()}
    out["subjects"] = out["sphere"] | out["cube"] | out["floor"]
    return out


def compare(png_a: Path, png_b: Path, mask_png: Path) -> tuple[dict, np.ndarray]:
    """Per-region ΔE2000 (mean, p95) and SSIM; returns (scores, the per-pixel ΔE map)."""
    A, B = read_rgb(png_a), read_rgb(png_b)
    dE = delta_e2000(srgb_to_lab(A), srgb_to_lab(B))
    scores = {}
    for name, m in masks(mask_png).items():
        if not m.any():
            continue
        d = dE[m]
        scores[name] = {"dE_mean": float(d.mean()), "dE_p95": float(np.percentile(d, 95)),
                        "ssim": ssim(A[m], B[m]), "pixels": int(m.sum())}
    scores["frame"] = {"dE_mean": float(dE.mean()), "dE_p95": float(np.percentile(dE, 95))}
    return scores, dE


def moved(png_setting: Path, png_defaults: Path, mask_png: Path) -> float:
    """How far a slider moved ONE tool's picture: mean dE2000 vs its own defaults, subjects."""
    a, b = read_rgb(png_setting), read_rgb(png_defaults)
    m = masks(mask_png)["subjects"]
    return float(delta_e2000(srgb_to_lab(a), srgb_to_lab(b))[m].mean())


def heatmap(dE: np.ndarray, bar: float, subjects: np.ndarray | None = None) -> Image.Image:
    """Black below half the bar, yellow at the bar, red at 3x the bar and above.

    (Black starts at half the bar so that Cycles' residual render noise, ~0.5-1 dE on flat
    areas, does not paint the whole panel: 5.1 sitting.)
    """
    t = dE / bar
    r = np.clip((t - 0.5) / 0.5, 0, 1)
    g = r * np.clip((3 - t) / 2, 0, 1)
    rgb = np.stack([r, g, np.zeros_like(t)], axis=-1)
    if subjects is not None:        # the furniture is not scored: show it at 30 %
        rgb = np.where(subjects[..., None], rgb, rgb * 0.3)
    return Image.fromarray((rgb * 255).astype(np.uint8))


# ------------------------------------------------------------------ scale (the ruler check)

def _camera():
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent / "scene"))
    import build_scene as bs
    return bs


def project(points: np.ndarray, width: int) -> np.ndarray:
    """World points (N, 3) -> pixel (x, y) through the scene's camera (square frame)."""
    bs = _camera()
    a = np.radians(bs.CAM_PITCH)
    rx = np.array([[1, 0, 0], [0, np.cos(a), -np.sin(a)], [0, np.sin(a), np.cos(a)]])
    local = (points - np.array(bs.CAM_POS)) @ rx          # R^T (p - c), row vectors
    half = bs.CAM_APERTURE / 2
    nx = bs.CAM_FOCAL * local[:, 0] / -local[:, 2] / half
    ny = bs.CAM_FOCAL * local[:, 1] / -local[:, 2] / half
    return np.stack([(nx + 1) / 2 * width, (1 - (ny + 1) / 2) * width], axis=1)


def _bilinear(img: np.ndarray, x: np.ndarray, y: np.ndarray, wrap: bool = False) -> np.ndarray:
    h, w = img.shape[:2]
    x, y = x - 0.5, y - 0.5
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    fx, fy = x - x0, y - y0
    if img.ndim == 3:
        fx, fy = fx[:, None], fy[:, None]

    def at(yy, xx):
        if wrap:
            return img[yy % h, xx % w]
        return img[np.clip(yy, 0, h - 1), np.clip(xx, 0, w - 1)]
    return ((at(y0, x0) * (1 - fx) + at(y0, x0 + 1) * fx) * (1 - fy)
            + (at(y0 + 1, x0) * (1 - fx) + at(y0 + 1, x0 + 1) * fx) * fy)


def _lum_linear(rgb: np.ndarray) -> np.ndarray:
    lin = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    return lin @ np.array([0.2126, 0.7152, 0.0722])


# The floor band sampled: in front of the objects, behind the ruler (z = 0.40).
BAND_X = np.linspace(-0.45, 0.45, 360)
BAND_Z = np.linspace(0.22, 0.36, 15)


def texture_scale(render_png: Path, texture_png: Path, meters_per_tile: float) -> dict:
    """At what size does the base texture appear on the floor?

    Samples the floor straight down (through the scene's camera) in a band in front of the
    objects, and correlates it with the article's base texture laid on the floor at
    ``k x`` its recorded size, for k from 0.25 to 4. ``size`` is the best k: 1.0 means the
    texture renders at exactly ``meters_per_tile``. The floor's st is (x + 0.5, 0.5 - z) in
    metres, divided by meters_per_tile by the render job.
    """
    img = read_rgb(render_png)
    X, Z = np.meshgrid(BAND_X, BAND_Z)
    pts = np.stack([X.ravel(), np.zeros(X.size), Z.ravel()], axis=1)
    px = project(pts, img.shape[1])
    r = _lum_linear(_bilinear(img, px[:, 0], px[:, 1]))
    tex = _lum_linear(read_rgb(texture_png))
    th, tw = tex.shape
    u0, v0 = (X.ravel() + 0.5) / meters_per_tile, (0.5 - Z.ravel()) / meters_per_tile
    best = (0.0, 0.0)
    for k in np.geomspace(0.25, 4.0, 241):
        t = _bilinear(tex, (u0 / k) * tw, (1 - v0 / k) * th, wrap=True)
        c = float(np.corrcoef(r, t)[0, 1])
        if c > best[1]:
            best = (float(k), c)
    return {"size": best[0], "ncc": best[1]}


# ------------------------------------------------------------------ seams (Phase04's measure)

def seam(texture_png: Path) -> dict:
    """Difference across the wrap edge vs between interior neighbours (0-255 scale).

    A SEAM is a wrap difference over ``SEAM_RATIO`` x the interior one. Phase04's real seams
    measured 2.1x to 26x (F3), while a seamless but noisy texture sits near 1x either side
    (Scratches01, regenerated seamless: 1.1x). A strict "wrap <= interior" is a coin flip on
    noisy textures (it flagged three seamless ones on its first run, Phase05 5.2).
    """
    a = np.asarray(Image.open(texture_png).convert("RGBA"), dtype=np.float64)
    wrap = (np.abs(a[:, 0] - a[:, -1]).mean() + np.abs(a[0] - a[-1]).mean()) / 2
    interior = (np.abs(np.diff(a, axis=1)).mean() + np.abs(np.diff(a, axis=0)).mean()) / 2
    return {"wrap": float(wrap), "interior": float(interior),
            "seamless": bool(wrap <= SEAM_RATIO * interior)}


SEAM_RATIO = 1.5


# Sharma, Wu & Dalal (2005), Table 1 — a sample of the published pairs.
SHARMA = [
    ((50.0, 2.6772, -79.7751), (50.0, 0.0, -82.7485), 2.0425),
    ((50.0, 3.1571, -77.2803), (50.0, 0.0, -82.7485), 2.8615),
    ((50.0, 0.0, 0.0), (50.0, -1.0, 2.0), 2.3669),
    ((50.0, 2.5, 0.0), (73.0, 25.0, -18.0), 27.1492),
    ((50.0, 2.5, 0.0), (50.0, 3.2592, 0.3350), 1.0000),
    ((60.2574, -34.0099, 36.2677), (60.4626, -34.1751, 39.4387), 1.2644),
    ((22.7233, 20.0904, -46.6940), (23.0331, 14.9730, -42.5619), 2.0373),
    ((90.8027, -2.0831, 1.4410), (91.1528, -1.6435, 0.0447), 1.4441),
    ((2.0776, 0.0795, -1.1350), (0.9033, -0.0636, -0.5514), 0.9082),
]


def self_test() -> int:
    bad = 0
    for l1, l2, want in SHARMA:
        got = float(delta_e2000(np.array(l1), np.array(l2)))
        ok = abs(got - want) < 1e-4
        bad += not ok
        print(f"{'ok ' if ok else 'BAD'} {l1} {l2} want {want:.4f} got {got:.4f}")
    print("PASS" if not bad else f"FAIL: {bad} pairs")
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(self_test())
