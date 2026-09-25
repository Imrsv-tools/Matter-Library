#!/usr/bin/env python3
"""Seamless (tileable) helpers for procedural textures (Phase03 step 3.5).

The older generators (gen_shared_textures.py, gen_article_textures.py) build noise by
resizing a random grid and take gradients with np.gradient; neither wraps, so their tiles
can show a seam. Everything here wraps: noise is interpolated periodically and gradients
use np.roll, so the right edge continues into the left and the top into the bottom.

Used by the per-set generators in tools/converters/base/ and tools/converters/layers/.
Fixed seeds, no network: byte-stable.
"""

from __future__ import annotations

import numpy as np
from PIL import Image

SIZE = 1024


def noise(scale: int, seed: int, size: int = SIZE) -> np.ndarray:
    """Periodic value noise in [0, 1]: a scale x scale random grid, smoothly interpolated
    with wrap-around, so the result tiles seamlessly."""
    rng = np.random.RandomState(seed)
    grid = rng.rand(scale, scale)
    t = np.arange(size) * scale / size
    i0 = np.floor(t).astype(int) % scale
    i1 = (i0 + 1) % scale
    f = t - np.floor(t)
    f = f * f * (3 - 2 * f)                                   # smoothstep
    rows = grid[i0][:, None, :] * (1 - f)[:, None, None] + grid[i1][:, None, :] * f[:, None, None]
    rows = rows[:, 0, :]                                      # (size, scale)
    out = rows[:, i0] * (1 - f)[None, :] + rows[:, i1] * f[None, :]
    return out


def fbm(scales: tuple, seed: int, size: int = SIZE) -> np.ndarray:
    """Sum of periodic noise octaves (coarse to fine), normalised to [0, 1]."""
    acc, amp, total = np.zeros((size, size)), 1.0, 0.0
    for k, s in enumerate(scales):
        acc += amp * noise(s, seed + k, size)
        total += amp
        amp *= 0.5
    return acc / total


def grad(height: np.ndarray) -> tuple:
    """Wrap-around central differences (d/dx, d/dy)."""
    dx = (np.roll(height, -1, axis=1) - np.roll(height, 1, axis=1)) * 0.5
    dy = (np.roll(height, -1, axis=0) - np.roll(height, 1, axis=0)) * 0.5
    return dx, dy


def normal_map(height: np.ndarray, strength: float) -> Image.Image:
    """A tangent-space normal map (OpenGL convention: +Y up, the library's NormalGL)."""
    dx, dy = grad(height)
    nx, ny, nz = -dx * strength, dy * strength, np.ones_like(dx)
    inv = 1.0 / np.sqrt(nx * nx + ny * ny + nz * nz)
    rgb = np.stack([nx * inv, ny * inv, nz * inv], axis=-1) * 0.5 + 0.5
    return Image.fromarray((np.clip(rgb, 0, 1) * 255).round().astype(np.uint8), "RGB")


def pack_overlay(height: np.ndarray, strength: float, rough_bias, density) -> Image.Image:
    """An overlay per the frozen contract: R/G normal XY (0.5 flat) · B roughness bias · A density."""
    dx, dy = grad(height)
    r = np.clip(-dx * strength * 0.5 + 0.5, 0, 1)
    g = np.clip(-dy * strength * 0.5 + 0.5, 0, 1)
    rgba = np.stack([r, g, np.clip(rough_bias, 0, 1), np.clip(density, 0, 1)], axis=-1)
    return Image.fromarray((rgba * 255).round().astype(np.uint8), "RGBA")


def pack_mask(r, g, b, a) -> Image.Image:
    """A mask per the frozen contract: R layer-2 coverage · G/B/A gates for overlays 1/2/3."""
    rgba = np.stack([np.clip(c, 0, 1) for c in (r, g, b, a)], axis=-1)
    return Image.fromarray((rgba * 255).round().astype(np.uint8), "RGBA")


def linear_to_srgb(c: np.ndarray) -> np.ndarray:
    """Encode linear values for an sRGB base-colour texture (srgb_texture on load)."""
    c = np.clip(c, 0, 1)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def gray(a: np.ndarray) -> Image.Image:
    return Image.fromarray((np.clip(a, 0, 1) * 255).round().astype(np.uint8), "L")


def rgb(a: np.ndarray) -> Image.Image:
    return Image.fromarray((np.clip(a, 0, 1) * 255).round().astype(np.uint8), "RGB")
