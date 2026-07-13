#!/usr/bin/env python3
"""Deterministically generate the base textures for the Phase-71 example articles (71.11).

Five of the seven masters had no example article at all, so nothing in the library ever
exercised them. These are the maps those articles need:

    Lace     (Masked)     an OPACITY mask — the thing the cutoff thresholds. Without a
                          connected geometry_opacity source a cutoff has nothing to cut.
    Marble   (Subsurface) base colour / roughness / normal — veined, polished.
    Rust     (TwoLayer)   TWO complete layers (steel + rust: base colour, roughness,
                          metalness, normal each) + the maskset that says WHERE layer 2 sits.

    Diamond  (Thick)   and   Neon (Emissive)   are param-only — no maps.

Same discipline as gen_shared_textures.py: fixed-seed value noise, no network, byte-stable
for a given seed/size. Every article is authored to a DELIBERATELY UNMISTAKABLE look, because
71.12 is an eyes-on gate and a subtle article makes a weak gate (the #57 lesson: a
discriminator that cannot visibly fire is not a gate).

    gen_article_textures.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
BASE = ROOT / "MatterLibrary" / "textures" / "base"
MASKS = ROOT / "MatterLibrary" / "textures" / "shared" / "masks"

SIZE = 1024


def _value_noise(size: int, scale: int, seed: int) -> np.ndarray:
    rng = np.random.RandomState(seed)
    low = rng.rand(scale, scale).astype(np.float64)
    img = Image.fromarray((low * 255).astype(np.uint8)).resize((size, size), Image.BICUBIC)
    return np.asarray(img, dtype=np.float64) / 255.0


def _uv(size: int) -> tuple:
    a = (np.arange(size) + 0.5) / size
    return np.meshgrid(a, a)


def _normal_from_height(height: np.ndarray, strength: float) -> Image.Image:
    """A real tangent-space normal map (B = +Z), sRGB=OFF on import."""
    dy, dx = np.gradient(height)
    nx, ny = -dx * strength, -dy * strength
    nz = np.ones_like(nx)
    inv = 1.0 / np.sqrt(nx * nx + ny * ny + nz * nz)
    rgb = np.stack([nx * inv * 0.5 + 0.5, ny * inv * 0.5 + 0.5, nz * inv * 0.5 + 0.5], axis=-1)
    return Image.fromarray((np.clip(rgb, 0, 1) * 255).astype(np.uint8), "RGB")


def _gray(a: np.ndarray) -> Image.Image:
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "L")


def _rgb(r, g, b) -> Image.Image:
    return Image.fromarray(
        (np.clip(np.stack([r, g, b], axis=-1), 0, 1) * 255).astype(np.uint8), "RGB")


def _save(img: Image.Image, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)
    print("wrote", path.relative_to(ROOT))


# ── Lace (Masked) ─────────────────────────────────────────────────────────────
# The defining observable is HOLES — you see the background THROUGH it. So the opacity map is
# built with hard, unmistakable structure: a floral lattice of open cells. It is deliberately
# ~45% open, because a mask that is 95% solid proves nothing at the smoke.

def gen_lace() -> None:
    u, v = _uv(SIZE)
    # Two offset sine lattices -> a repeating floral cell; thresholded to a crisp alpha.
    cells = (np.sin(u * np.pi * 8) * np.sin(v * np.pi * 8)
             + 0.6 * np.sin((u + v) * np.pi * 12)
             + 0.4 * np.sin((u - v) * np.pi * 12))
    thread = np.abs(cells)
    grain = _value_noise(SIZE, 256, seed=101) * 0.10
    # thread present -> opaque(1); the open cells -> transparent(0). Hard edges by design:
    # the master thresholds this against opacity_cutoff, so a soft ramp would make the cutoff
    # control a blur rather than a hole size.
    opacity = np.clip((thread + grain - 0.42) * 6.0, 0, 1)
    _save(_gray(opacity), BASE / "synthetic" / "textile" / "Lace_Floral_opacity_s01.png")

    fibre = _value_noise(SIZE, 512, seed=103)
    _save(_rgb(0.93 - 0.06 * fibre, 0.91 - 0.06 * fibre, 0.86 - 0.06 * fibre),
          BASE / "synthetic" / "textile" / "Lace_Floral_basecolor_s01.png")
    _save(_gray(0.62 + 0.18 * fibre),
          BASE / "synthetic" / "textile" / "Lace_Floral_roughness_s01.png")


# ── Marble (Subsurface) ───────────────────────────────────────────────────────
# The defining observable is LIGHT BLEEDING THROUGH. The maps stay pale and low-contrast so
# the scatter is what you see, not the albedo.

def gen_marble() -> None:
    u, v = _uv(SIZE)
    warp = _value_noise(SIZE, 32, seed=201)
    # Turbulent veining: a banded field pushed around by low-frequency noise.
    veins = np.sin((u * 5.0 + v * 2.0 + warp * 3.2) * np.pi * 2.0)
    veins = np.abs(veins) ** 0.35                      # thin, dark, sharp-edged veins
    grain = _value_noise(SIZE, 384, seed=203)

    body = 0.90 - 0.30 * (1.0 - veins) + 0.03 * grain
    _save(_rgb(body, body * 0.985, body * 0.95),       # faintly warm white
          BASE / "natural" / "stone" / "Marble_Veined_basecolor_s01.png")
    # Polished: very smooth overall, veins slightly duller than the body.
    _save(_gray(0.10 + 0.16 * (1.0 - veins)),
          BASE / "natural" / "stone" / "Marble_Veined_roughness_s01.png")
    _save(_normal_from_height(veins * 0.35 + grain * 0.05, strength=1.5),
          BASE / "natural" / "stone" / "Marble_Veined_normal_s01.png")


# ── Rust on steel (TwoLayer) ──────────────────────────────────────────────────
# The defining observable is TWO LAYERS THAT ARE VISIBLY TWO. Layer 1 is clean, bright,
# polished steel (metal=1, smooth); layer 2 is dark orange flaking rust (metal=0, very rough).
# The two are about as far apart as a PBR surface can get — that separation IS the gate.

def gen_rust() -> None:
    metal_dir = BASE / "engineered" / "metal"

    # Layer 1 — steel: cool, bright, brushed, metallic.
    brush = _value_noise(SIZE, 8, seed=301) * 0.25 + _value_noise(SIZE, 512, seed=303) * 0.75
    _save(_rgb(0.55 + 0.06 * brush, 0.56 + 0.06 * brush, 0.60 + 0.06 * brush),
          metal_dir / "Rust_OnSteel_layer1_basecolor_s01.png")
    _save(_gray(0.18 + 0.10 * brush), metal_dir / "Rust_OnSteel_layer1_roughness_s01.png")
    _save(_gray(np.ones((SIZE, SIZE))), metal_dir / "Rust_OnSteel_layer1_metalness_s01.png")
    _save(_normal_from_height(brush * 0.12, strength=1.0),
          metal_dir / "Rust_OnSteel_layer1_normal_s01.png")

    # Layer 2 — rust: warm dark orange, crusty, NON-metallic (oxide is a dielectric).
    crust = _value_noise(SIZE, 128, seed=311)
    flake = _value_noise(SIZE, 320, seed=313)
    ox = np.clip(crust * 0.7 + flake * 0.3, 0, 1)
    _save(_rgb(0.42 + 0.22 * ox, 0.17 + 0.13 * ox, 0.06 + 0.05 * ox),
          metal_dir / "Rust_OnSteel_layer2_basecolor_s01.png")
    _save(_gray(0.78 + 0.20 * ox), metal_dir / "Rust_OnSteel_layer2_roughness_s01.png")
    _save(_gray(np.zeros((SIZE, SIZE))), metal_dir / "Rust_OnSteel_layer2_metalness_s01.png")
    _save(_normal_from_height(ox, strength=5.0),
          metal_dir / "Rust_OnSteel_layer2_normal_s01.png")

    # The maskset. R = layer-2 coverage — WHERE the rust sits. Built with a hard, blotchy,
    # high-contrast edge so the boundary between steel and rust is unmistakable at the smoke
    # (and so layer_blend_balance/contrast visibly MOVE that boundary, which is what the two
    # blend controls exist to prove).
    bloom = _value_noise(SIZE, 20, seed=321)
    creep = _value_noise(SIZE, 72, seed=323)
    coverage = np.clip((bloom * 0.75 + creep * 0.25 - 0.30) * 2.6, 0, 1)
    rgba = np.stack([
        coverage,                                 # R: layer-2 (rust) coverage
        _value_noise(SIZE, 40, seed=325),         # G: overlay-1 gate
        _value_noise(SIZE, 88, seed=327),         # B: overlay-2 gate
        np.ones((SIZE, SIZE)),                    # A: reserved (v1)
    ], axis=-1)
    _save(Image.fromarray((np.clip(rgba, 0, 1) * 255).astype(np.uint8), "RGBA"),
          MASKS / "RustBloom01_s01.png")


def main() -> int:
    gen_lace()
    gen_marble()
    gen_rust()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
