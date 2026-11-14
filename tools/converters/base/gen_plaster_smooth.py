#!/usr/bin/env python3
"""Generate the base texture set `Plaster_Smooth` (Phase11 batch 261114-1; lane L2).

A lime plaster finish coat, trowelled smooth and left bare or limewashed: the wall of most
rooms from antiquity to the mid twentieth century. It reads as HAND-TROWELLED PLASTER, not as
a painted board, because of what this draws: the TROWEL (passes 25 to 40 cm across, each a run of very
shallow curved ridges swept its own way and lapping the last, the surface gently uneven at hand scale), a faint cloudy
tone where the lime cured unevenly, the fine sand of the mix as a tooth, and a few pinholes.
All of it is slight: at arm's length the wall is one matte off-white.

Generated, not scanned: ambientCG's plasters are rough modern renders or painted and broken
walls, and none states a physical size (they were not tried; a redo may). The colour is a JUDGEMENT: the mean linear albedo is (0.76, 0.72, 0.64), sRGB
about 225, 220, 208, a warm off-white lime, re-normalised so the mean is exact; a colour wash
is the article's tint. The mean roughness is 0.88 (matte, with a trace of burnish where the
trowel closed the face).

Writes MatterLibrary/textures/base/engineered/cementitious/Plaster_Smooth_<channel>_s1.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s1`: a 1 m
tile at 1024 px (about 1 mm a texel). Seamless (tileable.py), fixed seed, no network.

    gen_plaster_smooth.py [--out DIR]

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
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "engineered" / "cementitious"
SET = "Plaster_Smooth"
SCALE = "s1"
SEED = 6307
LIME = np.array([0.76, 0.72, 0.64])             # judgement: a warm off-white lime, linear sRGB
ROUGH_MEAN = 0.88
N = tl.SIZE


def soften(a: np.ndarray, sigma: float) -> np.ndarray:
    """A wrap-around Gaussian blur (sigma in texels), done in the frequency domain so it tiles."""
    f = np.fft.fftfreq(a.shape[0])
    g = np.exp(-2 * (np.pi * sigma) ** 2 * (f[:, None] ** 2 + f[None, :] ** 2))
    return np.real(np.fft.ifft2(np.fft.fft2(a) * g))


def trowel() -> np.ndarray:
    """Trowel passes: each pass is a patch of shallow parallel ridges swept in its own direction
    and gently curved, lapping its neighbours. A pass's ridges are a wave with a whole number of
    cycles across the tile each way, so every pass wraps. Two sets of passes at different
    sizes, so no single layout reads."""
    out = np.zeros((N, N))
    u = (np.arange(N)[None, :] + 0.5) / N
    v = (np.arange(N)[:, None] + 0.5) / N
    for k, (n, amp) in enumerate(((3, 1.0), (4, 0.6))):
        s = SEED + 20 + 10 * k
        warp = (0.5 * (tl.fbm((3, 7), s + 1) - 0.5), 0.5 * (tl.fbm((3, 7), s + 2) - 0.5))
        d1, d2, cid = tl.cells(n, s, warp=warp)
        rng = np.random.RandomState(s + 3)
        kx = (rng.randint(5, 15, n * n) * rng.choice([-1, 1], n * n))[cid]
        ky = (rng.randint(5, 15, n * n) * rng.choice([-1, 1], n * n))[cid]
        phase = rng.rand(n * n)[cid]
        bend = 1.6 * tl.fbm((2, 3, 5), s + 5)                    # the sweep of the arm: a curve
        ridges = 0.5 + 0.5 * np.sin(2 * np.pi * (kx * u + ky * v + phase + bend))
        lap = np.clip((d2 - d1) / 0.25, 0, 1) ** 0.5             # a pass fades out toward its edge
        level = rng.rand(n * n)[cid]                             # each pass leaves its own level
        out += amp * (ridges * (0.3 + 0.7 * tl.fbm((5, 9), s + 4)) * lap + 0.35 * level)
    return soften(out, 3.0)


def maps() -> dict:
    tr = trowel()
    tr = (tr - tr.min()) / (tr.max() - tr.min())
    wave = tl.fbm((3, 5, 9), SEED + 1)                            # the wall's hand-scale unevenness
    cloud = soften(tl.fbm((4, 7, 13), SEED + 2), 4.0)             # uneven curing: a faint cloud
    fine = tl.fbm((256, 512), SEED + 3)                           # the sand's tooth
    rng = np.random.RandomState(SEED + 5)
    speck = rng.rand(N, N)
    pin = soften((rng.rand(N, N) > 0.9975).astype(float), 0.6)    # pinholes, about 1 mm
    pin = pin / pin.max()

    shade = (1.0 + 0.07 * (cloud - 0.5) + 0.03 * (tr - 0.5) + 0.03 * (fine - 0.5)
             + 0.02 * (speck - 0.5) - 0.25 * pin)
    albedo = LIME[None, None, :] * shade[..., None]
    warm = np.array([1.0, 0.985, 0.95])                           # thinner, cooler-cured areas are whiter
    albedo = albedo * (1 + (warm - 1) * (2 * (0.5 - cloud))[..., None])
    albedo *= LIME / albedo.reshape(-1, 3).mean(0)                # re-anchor the MEAN exactly
    albedo = np.clip(albedo, 0, 1)

    rough = -0.06 * (tr - 0.5) + 0.04 * (fine - 0.5) + 0.04 * pin
    rough = np.clip(rough - rough.mean() + ROUGH_MEAN, 0, 1)
    height = 5.0 * wave + 1.6 * tr + 0.25 * fine + 0.10 * speck - 0.8 * pin
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=1.5)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Plaster_Smooth base texture set.")
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
