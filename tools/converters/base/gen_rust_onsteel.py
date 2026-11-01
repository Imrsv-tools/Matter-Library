#!/usr/bin/env python3
"""Generate the base texture sets of `Rust_OnSteel` (batch 261016-2; lane L2): its two layers.

Rust_OnSteel is TwoLayer: layer 1 the bare steel, layer 2 the rust, and the shared mask
RustFlake01 (sampled at its own 1 m) says where the rust has grown. These are the layers
themselves, each a full set (base colour, roughness, metalness, normal). They replace the
Phase71 example maps (gen_article_textures.py), a deliberately loud test pattern whose
noise did not wrap (7 of 9 maps seamed).

- Layer 1, steel: bare mild steel where the rust has flaked away: grey, metallic, dulled
  and faintly tarnished, with fine pitting; its mean colour is Physically Based's Iron.
- Layer 2, rust: iron oxide grown into a blistered crust that has cracked into flakes (about
  2-6 mm, irregular), each its own shade from dark brown to orange; only some borders have
  opened, their edges lifted and the cracks dark; some flakes have fallen away to the older,
  darker scale beneath; a fine granular crust over all. Non-metallic (oxide is a dielectric),
  rough; its mean colour is Physically Based's Rust.

The colours are anchored, not invented: each layer's mean linear albedo is scaled to its
Physically Based entry exactly; everything here only varies around it.

Writes MatterLibrary/textures/base/engineered/metal/Rust_OnSteel_layer<N>_<channel>_s01.png
(basecolor sRGB-encoded; roughness, metalness and normal linear data, NormalGL). Scale `s01`:
exactly a 0.1 m tile (Phase19 D-9), 1024 px, about 0.1 mm a pixel. Seamless (periodic noise
and cells), fixed seed, no network.

    gen_rust_onsteel.py [--out DIR]

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
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "engineered" / "metal"
SET = "Rust_OnSteel"
SCALE = "s01"
SEED = 1610
SIZE = tl.SIZE
IRON = np.array([0.53, 0.513, 0.494])    # Physically Based "Iron", linear sRGB
RUST = np.array([0.181, 0.057, 0.017])   # Physically Based "Rust", linear sRGB


def anchored(albedo: np.ndarray, mean: np.ndarray) -> np.ndarray:
    """Scale the albedo so its mean is exactly `mean` (the varying is ours, the mean is not)."""
    return albedo * (mean / albedo.reshape(-1, 3).mean(0))


def steel() -> dict:
    tarnish = tl.fbm((4, 8, 16), SEED)                        # dull, uneven oxide film
    grain = tl.fbm((128, 256), SEED + 1)                      # fine surface grain
    d1, _, pid = tl.cells(90, SEED + 2)                       # pits, ~1 mm apart
    rng = np.random.RandomState(SEED + 3)
    deep = rng.rand(90 * 90)[pid] > 0.7                       # three in ten points are a pit
    pit = np.where(deep, np.clip(1 - d1 / 0.25, 0, 1) ** 2, 0)
    shade = 1.0 - 0.10 * (tarnish - 0.5) + 0.05 * (grain - 0.5) - 0.25 * pit
    albedo = anchored(IRON[None, None, :] * shade[..., None], IRON)
    rough = np.clip(0.55 + 0.10 * (tarnish - 0.5) + 0.05 * (grain - 0.5) + 0.20 * pit, 0, 1)
    height = 0.6 * grain - 2.0 * pit
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "metalness": tl.gray(np.ones((SIZE, SIZE))),
            "normal": tl.normal_map(height, strength=1.5)}


def rust() -> dict:
    rng = np.random.RandomState(SEED + 10)
    # Flakes of ~2-6 mm, bent out of the cell grid's regularity by a periodic warp.
    wx = (tl.fbm((6, 12, 24), SEED + 15) - 0.5) * 1.6
    wy = (tl.fbm((6, 12, 24), SEED + 16) - 0.5) * 1.6
    d1, d2, flake = tl.cells(30, SEED + 11, warp=(wx, wy))
    gap = d2 - d1                                             # 0 on a border between flakes
    tone = rng.rand(30 * 30)[flake]                           # a shade per flake
    lift = rng.rand(30 * 30)[flake]                           # each flake at its own height
    # Flakes that have fallen away: a soft-edged step (anti-aliased across the border).
    gone = (rng.rand(30 * 30)[flake] < 0.18) * np.clip(gap / 0.06, 0, 1)
    # Only some borders have opened into cracks: the crust is broken, not tiled.
    opened = np.clip((tl.fbm((24, 48), SEED + 17) - 0.45) * 4, 0, 1)
    crack = np.clip(1 - gap / 0.07, 0, 1) * opened
    curl = np.clip(1 - gap / 0.35, 0, 1) * opened * (1 - crack)   # a lifting flake's edge
    crust = tl.fbm((128, 256, 512), SEED + 13)                # the fine granular crust
    g1, _, gid = tl.cells(160, SEED + 19)                     # loose grains, ~0.6 mm
    grains = np.clip(1 - g1 / 0.35, 0, 1) * (rng.rand(160 * 160)[gid] < 0.35)
    blister = tl.fbm((40, 80), SEED + 18)                     # bubbled, uneven growth
    patch = tl.fbm((3, 6, 12), SEED + 14)                     # broad shifts, orange to brown

    # Colour: dark brown to orange; under a fallen flake the older, darker scale; the cracks dark.
    orange = np.array([1.60, 1.30, 1.05])                     # relative to the mean: warmer, lighter
    brown = np.array([0.72, 0.62, 0.62])
    t = np.clip(0.45 * tone + 0.35 * patch + 0.30 * blister - 0.05, 0, 1)[..., None] ** 1.3
    albedo = RUST[None, None, :] * (brown + (orange - brown) * t)
    albedo *= (1 - 0.45 * gone * (1 - 0.6 * (blister - 0.5)))[..., None]
    albedo *= (1 - 0.55 * crack)[..., None]
    albedo *= (1 + 0.70 * (crust - 0.5) - 0.45 * grains)[..., None]
    albedo = anchored(albedo, RUST)

    rough = np.clip(0.90 + 0.08 * (crust - 0.5) - 0.08 * curl + 0.05 * gone, 0, 1)
    height = (0.5 * lift * (1 - gone) - 0.8 * gone + 0.7 * curl - 1.2 * crack
              + 0.9 * blister + 0.8 * crust + 0.6 * grains)
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "metalness": tl.gray(np.zeros((SIZE, SIZE))),
            "normal": tl.normal_map(height, strength=3.0)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Rust_OnSteel layer texture sets.")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args(argv)
    out = Path(args.out)
    layers = {"layer1": steel, "layer2": rust}
    targets = {(ly, ch): out / f"{SET}_{ly}_{ch}_{SCALE}.png"
               for ly in layers for ch in ("basecolor", "roughness", "metalness", "normal")}
    if any(p.exists() for p in targets.values()):
        print(f"refusing to overwrite {SET} in {out} (Build Safety); use --out <dir>", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)
    for ly, make in layers.items():
        for ch, img in make().items():
            img.save(targets[(ly, ch)], "PNG", optimize=True)
            print(f"wrote {targets[(ly, ch)]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
