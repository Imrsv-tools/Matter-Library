#!/usr/bin/env python3
"""Generate the base texture set `Calcite_Egyptian` (Phase11 batch 261114-1; lane L2).

Egyptian alabaster: the banded calcite (travertine onyx) of ancient Egyptian vessels, lamps,
canopic jars, floors and shrine linings, cut across its layers and polished. It reads as THIS
stone, not as marble, because it is creamy and nearly even: a warm white-to-honey body crossed
by FAINT wavy bands, some a finger wide and some a hand wide, each only a shade paler, more
honey or more milky than the next, with a soft cloud inside the wider ones and an occasional
thin whiter seam. There are no dark veins.

Generated, not scanned: ambientCG's pale onyx scans (Onyx015, Onyx004, Onyx012) were looked at
and are cool grey, green-lined or brown, each strongly banded. The colour is a JUDGEMENT: the
mean linear albedo is (0.72, 0.63, 0.47), sRGB about 220, 208, 183, a creamy alabaster,
re-normalised so the mean is exact. Physically Based has no calcite or alabaster entry. The
mean roughness is 0.08 (polished); the relief is almost nil.

Writes MatterLibrary/textures/base/natural/stone/Calcite_Egyptian_<channel>_s1.png: basecolor
(sRGB-encoded), roughness and normal (linear data, NormalGL). Scale `s1`: a 1 m tile at 1024 px
(about 1 mm a texel): bands 1 to 10 cm wide, undulating over 20 to 50 cm. The band profile is a
periodic function of the height up the tile and every noise wraps: seamless. Fixed seed, no network.

    gen_calcite_egyptian.py [--out DIR]

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
SET = "Calcite_Egyptian"
SCALE = "s1"
SEED = 6607
CREAM = np.array([0.72, 0.63, 0.47])            # judgement: a creamy alabaster, linear sRGB
ROUGH_MEAN = 0.08
N = tl.SIZE
L = 8192                                        # samples in the periodic band profile


def profile(seed: int, cutoffs: tuple) -> np.ndarray:
    """A periodic 1-D profile in [0, 1]: random values smoothed at several widths (as a share of
    the tile), summed. It is the tone of the stone's layers, read off by height."""
    rng = np.random.RandomState(seed)
    f = np.fft.fftfreq(L) * L                                     # cycles per tile
    out = np.zeros(L)
    for k, c in enumerate(cutoffs):
        spec = np.fft.fft(rng.rand(L)) * np.exp(-(f / c) ** 2)
        a = np.real(np.fft.ifft(spec))
        out += (a - a.mean()) / a.std() * (0.6 ** k)
    return (out - out.min()) / (out.max() - out.min())


def lookup(p: np.ndarray, pos: np.ndarray) -> np.ndarray:
    """Read the periodic profile at `pos` (in tiles), linearly interpolated."""
    x = (pos % 1.0) * L
    i = np.floor(x).astype(int) % L
    t = x - np.floor(x)
    return p[i] * (1 - t) + p[(i + 1) % L] * t


def maps() -> dict:
    v = (np.arange(N)[:, None] + 0.5) / N * np.ones((1, N))
    swell = 0.45 * (tl.fbm((1, 2, 3), SEED) - 0.5) + 0.05 * (tl.fbm((5, 9, 17), SEED + 1) - 0.5)
    crinkle = 0.004 * (tl.fbm((40, 80, 160), SEED + 2) - 0.5)
    pos = v + swell + crinkle
    tone = lookup(profile(SEED + 10, (6, 18, 45, 110)), pos)      # bands 1 to 15 cm
    honey = lookup(profile(SEED + 11, (5, 14)), pos)              # which layers run honey
    milk = lookup(profile(SEED + 12, (9, 30)), pos)               # which run milky
    seamp = profile(SEED + 13, (70,))
    seam = np.clip((lookup(seamp, pos) - 0.86) / 0.10, 0, 1)      # a few thin whiter seams
    fade = tl.fbm((3, 6, 12), SEED + 3)                           # a band fades along its run
    cloud = tl.fbm((8, 16, 32), SEED + 4)                         # the cloud inside a band
    fine = tl.fbm((200, 400), SEED + 5)

    shade = (1.0 + 0.30 * (tone - 0.5) * (0.5 + fade) + 0.08 * (cloud - 0.5) + 0.02 * (fine - 0.5)
             + 0.10 * seam)
    albedo = CREAM[None, None, :] * shade[..., None]
    honey_col = np.array([1.03, 0.86, 0.60])                      # a honey layer: deeper, more amber
    milk_col = np.array([1.02, 1.06, 1.16])                       # a milky layer: whiter
    albedo = albedo * (1 + (honey_col - 1) * (np.clip(honey - 0.45, 0, 1) * 1.6 * (0.4 + fade))[..., None])
    albedo = albedo * (1 + (milk_col - 1) * (np.clip(milk - 0.5, 0, 1) * 1.8 + seam)[..., None])
    albedo *= CREAM / albedo.reshape(-1, 3).mean(0)               # re-anchor the MEAN exactly
    albedo = np.clip(albedo, 0, 1)

    rough = 0.02 * (fine - 0.5) + 0.02 * (cloud - 0.5) + 0.02 * seam
    rough = np.clip(rough - rough.mean() + ROUGH_MEAN, 0.02, 1)
    height = 0.3 * tone + 0.1 * fine                              # a polished face: almost flat
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=0.4)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Calcite_Egyptian base texture set.")
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
