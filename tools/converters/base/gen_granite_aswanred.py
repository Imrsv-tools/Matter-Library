#!/usr/bin/env python3
"""Generate the base texture set `Granite_AswanRed` (Phase11 batch 261114-1; lane L2).

The red granite of Aswan, polished: the stone of Egyptian obelisks, sarcophagi, columns and
statues. It reads as THIS granite because of its coarse, interlocking crystals: a rose-to-red
potassium FELDSPAR ground (crystals 1 to 3 cm, each its own shade, some large and blocky),
grey glassy QUARTZ between them, a little white-cream PLAGIOCLASE, and black BIOTITE and
hornblende in ragged flakes 2 to 8 mm that gather in clots. There is no bedding and no
veining: a granite is the same in every direction.

No scan fits: ambientCG's granites are countertop stones with no red or rose one among their
tags. The colours are a JUDGEMENT from the stone as quarried and polished; the mean linear
albedo comes out at (0.310, 0.163, 0.148), a deep rose with black and grey through it, and is
printed by the script. Physically Based has no granite entry. Roughness: a polished face,
mean 0.12, the mica a little glossier and the feldspar cleavage a little duller. The relief is
almost nil (a polished face), only the faint pluck of grain boundaries.

Writes MatterLibrary/textures/base/natural/stone/Granite_AswanRed_<channel>_s1.png: basecolor
(sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s1`: a 1 m tile at 1024 px
(about 1 mm a texel). Every cell field wraps: seamless. Fixed seed, no network.

    gen_granite_aswanred.py [--out DIR]

It refuses to overwrite an existing file (AI_WorkingAgreement §Build Safety).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import tileable as tl  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent.parent
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "natural" / "stone"
SET = "Granite_AswanRed"
SCALE = "s1"
SEED = 6503
N = tl.SIZE
FELDSPAR = np.array([0.37, 0.14, 0.125])         # rose-red potassium feldspar, linear sRGB
QUARTZ = np.array([0.19, 0.18, 0.175])           # grey, glassy
PLAGIO = np.array([0.58, 0.52, 0.47])           # white-cream plagioclase
MICA = np.array([0.02, 0.02, 0.022])            # biotite and hornblende
ROUGH_MEAN = 0.12


def soften(a: np.ndarray, sigma: float) -> np.ndarray:
    """A wrap-around Gaussian blur (sigma in texels), done in the frequency domain so it tiles."""
    f = np.fft.fftfreq(a.shape[0])
    k = np.exp(-2 * (np.pi * sigma) ** 2 * (f[:, None] ** 2 + f[None, :] ** 2))
    if a.ndim == 3:
        return np.stack([np.real(np.fft.ifft2(np.fft.fft2(a[..., c]) * k)) for c in range(a.shape[2])], -1)
    return np.real(np.fft.ifft2(np.fft.fft2(a) * k))


def crystals(n: int, seed: int, warp_amp: float) -> tuple:
    """A warped cell field: per texel the cell's own random value(s) and its edge closeness."""
    w = min(4 * n, N)
    warp = (warp_amp * (tl.noise(w, seed + 2) - 0.5), warp_amp * (tl.noise(w, seed + 3) - 0.5))
    d1, d2, cid = tl.cells(n, seed, warp=warp)
    rng = np.random.RandomState(seed + 1)
    return rng.rand(n * n)[cid], rng.rand(n * n)[cid], np.clip(1 - (d2 - d1) / 0.10, 0, 1)


def maps() -> dict:
    kind, tone, edge = crystals(75, SEED, 0.80)                   # the groundmass: crystals about 1 to 2 cm
    big_pick, big_tone, big_edge = crystals(30, SEED + 10, 0.30)  # blocky feldspars, 2 to 3 cm
    clot = tl.fbm((6, 11, 23), SEED + 20)                         # where the dark minerals gather
    mk, _, _ = crystals(170, SEED + 30, 0.7)                      # mica flakes, 3 to 8 mm
    mica = (mk < 0.10 + 0.75 * np.clip(clot - 0.50, 0, 1)).astype(float)
    body = tl.fbm((60, 120, 240), SEED + 41)                      # cloudiness inside a crystal
    cleave = tl.fbm((200, 400), SEED + 40)                        # cleavage glitter inside a crystal

    # groundmass: 58 % feldspar, 30 % quartz, 12 % plagioclase
    is_q = (kind > 0.58) & (kind <= 0.88)
    is_p = kind > 0.88
    col = np.where(is_q[..., None], QUARTZ, np.where(is_p[..., None], PLAGIO, FELDSPAR))
    shade = np.where(is_q, 0.80 + 0.40 * tone, np.where(is_p, 0.85 + 0.25 * tone, 0.70 + 0.65 * tone))
    big = big_pick < 0.22                                         # a blocky feldspar over the groundmass
    col = np.where(big[..., None], FELDSPAR * np.array([1.08, 1.0, 0.95]), col)
    shade = np.where(big, 0.85 + 0.50 * big_tone, shade)
    edge = np.where(big, big_edge, edge)
    albedo = col * (shade * (1 + 0.10 * (cleave - 0.5) + 0.45 * (body - 0.5)) * (1 - 0.18 * edge))[..., None]
    albedo = albedo * (1 - mica)[..., None] + MICA * mica[..., None]
    albedo = np.clip(soften(albedo, 0.6), 0, 1)                   # crystals meet cleanly, not in stairs

    rough = 0.03 * (cleave - 0.5) + 0.05 * edge - 0.04 * mica + 0.02 * is_q
    rough = np.clip(rough - rough.mean() + ROUGH_MEAN, 0.02, 1)
    height = -0.6 * edge - 0.3 * mica + 0.1 * cleave              # a polished face: almost flat
    print("mean linear albedo", albedo.reshape(-1, 3).mean(0).round(3), "mica share", round(float(mica.mean()), 3))
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(soften(height, 0.8), strength=0.5)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Granite_AswanRed base texture set.")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args(argv)
    out = Path(args.out)
    targets = {ch: out / f"{SET}_{ch}_{SCALE}.png" for ch in ("basecolor", "roughness", "normal")}
    if any(p.exists() for p in targets.values()):
        print(f"refusing to overwrite {SET} in {out} (Build Safety); use --out <dir>", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)
    for ch, img in maps().items():
        img.save(targets[ch], "PNG", optimize=True)
        print(f"wrote {targets[ch]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
