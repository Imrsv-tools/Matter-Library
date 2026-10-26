#!/usr/bin/env python3
"""Make SYNTHETIC EYE test pictures for MakeHuman_Eyes_v01: real-looking irises and whites, no person in them.

    uv run tools/converters/fit/gen_synth_eyes.py                    # every colour, both conditions
    uv run tools/converters/fit/gen_synth_eyes.py Hazel --out /tmp/eyes   # a trial

**What this is.** The lead's spike (2026-10-26; OMF research `261026_R_SyntheticSkinAndEyeSets`).
Each picture is a DRAFT test article's own ``base_color_map`` (``Eye_Synth<Colour>_…``), drawn on the
layout of the fit set's eyes (both eyeballs on one 1024 picture, measured from
``Brown_basecolor_sUKN.png``: centres ``CENTRES``, pupil edge ``R_PUPIL``, limbus ``R_IRIS``, the
white to ``R_BALL``). The nine MakeHuman eyes are not touched.

**How an iris is built — layers, as an ocularist paints one** (Lefohn et al. 2003, *An Ocularist's
Approach to Human Iris Synthesis*): a stroma base; radial fibres (fine and many on light irises,
smoothed on brown ones, as Bérard et al. 2016 observed); crypts (dark lacunae in the middle of the
iris); the collarette (a wavy ring about a third of the way out, often a different colour from the
outer iris); contraction furrows (broken rings near the edge); a soft dark limbal ring; and the
pupil's dark ruff. Each colourway (``PRESETS``) sets the colours of those layers. Blue and grey are
low-melanin irises, where the colour is scattering in a pale stroma (Lam & Baranoski 2006), so
their fibres are the lightest part; brown is melanin, so its fibres are barely lighter than its base.

**The white** has the measured sclera's warm colour (Physically Based, round 3), a little darker toward
the hidden edge, with vessels grown inward from the edge as
thinning branching walks that fade before the iris. ``Bloodshot`` has more, thicker, redder vessels
reaching nearer the iris, over a pink flush.

**Sources.** Procedural only: seeded noise and random walks. No photograph, no AI. The layer recipe
and colour logic are from the papers named above; every number here is judgement, tuned by eye.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "tools" / "parity" / "scene"))
sys.path.insert(0, str(HERE))
import gen_skin_maps as gsm  # noqa: E402  (the shared noise, blur and sRGB helpers)

N = 1024                                    # groups.PART_MESHES["MakeHuman_Eyes_v01"]["map_size"]
CENTRES = ((296.2, 725.3), (722.2, 303.3))  # the two eyeballs' front poles (measured)
R_PUPIL, R_IRIS, R_BALL = 30.0, 116.0, 268.0
CORNER = (957.0, 955.0, 60.0)               # the small island in the corner: kept dark
OUT = REPO / "MatterLibrary" / "textures" / "fit" / "makehuman" / "eyes"
PROVENANCE = REPO / "library" / "provenance" / "sources" / "fit" / "makehuman" / "synth_eyes.yaml"
TAG = "sUKN"
SEED = 20261026

# Each colourway: (inner/pupillary zone, outer/ciliary zone, fibres, crypts, collarette), sRGB 0-1,
# plus how strongly the fibres show (light irises are fibrous, brown ones smooth).
PRESETS = {
    "DarkBrown": dict(inner=(0.13, 0.07, 0.035), outer=(0.16, 0.085, 0.04), fibre=(0.24, 0.14, 0.07),
                      crypt=(0.06, 0.03, 0.02), collar=(0.20, 0.11, 0.05), fibrous=0.35),
    "Brown":     dict(inner=(0.24, 0.12, 0.05), outer=(0.30, 0.17, 0.08), fibre=(0.43, 0.27, 0.13),
                      crypt=(0.10, 0.05, 0.025), collar=(0.38, 0.22, 0.09), fibrous=0.45),
    "Amber":     dict(inner=(0.50, 0.30, 0.08), outer=(0.55, 0.36, 0.11), fibre=(0.72, 0.52, 0.22),
                      crypt=(0.25, 0.13, 0.04), collar=(0.62, 0.40, 0.12), fibrous=0.55),
    "Hazel":     dict(inner=(0.36, 0.24, 0.10), outer=(0.30, 0.34, 0.18), fibre=(0.52, 0.50, 0.30),
                      crypt=(0.14, 0.12, 0.06), collar=(0.50, 0.32, 0.10), fibrous=0.6),
    "Green":     dict(inner=(0.33, 0.30, 0.14), outer=(0.22, 0.36, 0.24), fibre=(0.45, 0.58, 0.42),
                      crypt=(0.08, 0.14, 0.10), collar=(0.44, 0.38, 0.14), fibrous=0.75),
    "Grey":      dict(inner=(0.36, 0.37, 0.36), outer=(0.36, 0.40, 0.42), fibre=(0.66, 0.69, 0.70),
                      crypt=(0.14, 0.16, 0.18), collar=(0.48, 0.47, 0.44), fibrous=0.95),
    "Blue":      dict(inner=(0.28, 0.36, 0.42), outer=(0.16, 0.30, 0.46), fibre=(0.55, 0.66, 0.75),
                      crypt=(0.06, 0.11, 0.20), collar=(0.40, 0.46, 0.50), fibrous=1.0),
    "LightBlue": dict(inner=(0.42, 0.52, 0.58), outer=(0.30, 0.47, 0.62), fibre=(0.74, 0.82, 0.87),
                      crypt=(0.12, 0.20, 0.30), collar=(0.56, 0.62, 0.64), fibrous=1.0),
}
CONDITIONS = ("Clean", "Bloodshot")
BLOODSHOT_OF = ("Brown", "Blue")            # the test's bloodshot pair: one dark iris, one light


def lin(c):
    return gsm._srgb_to_linear(np.asarray(c, dtype=np.float64))


# The white's colour. Round 3 (2026-10-26; the lead: "The eye all look quite bright to me"): round 1's
# near-neutral white (red/blue 1.18) read bright at a measured brightness. The white now takes the
# measured sclera's warm colour, Physically Based "Eye (Sclera)" (linear 0.652, 0.5, 0.394, the
# library's Sclera_Natural; red/blue 1.65), at round 1's brightness. The edge keeps round 1's darkening
# toward the hidden side but not its pink: on top of a measured warm white the pink counted the warmth
# twice and read peach on the character (tried and seen the same day).
SCLERA_PB = np.array((0.652, 0.5, 0.394))
ARTICLE_CONST = np.array((0.95, 0.93, 0.92))   # the eye articles' base_color_const, which the picture multiplies


def _lum(c):
    return float(np.dot(c, (0.2126, 0.7152, 0.0722)))


_ROUND1_CENTRE, _ROUND1_EDGE = lin((0.84, 0.81, 0.78)), lin((0.80, 0.70, 0.66))
WHITE_CENTRE = SCLERA_PB * (_lum(_ROUND1_CENTRE * ARTICLE_CONST) / _lum(SCLERA_PB)) / ARTICLE_CONST
WHITE_EDGE = WHITE_CENTRE * (_lum(_ROUND1_EDGE) / _lum(_ROUND1_CENTRE))


def polar(cx, cy):
    yy, xx = np.mgrid[:N, :N] + 0.5
    return np.hypot(xx - cx, yy - cy), np.arctan2(yy - cy, xx - cx)


def ring_noise(theta, rho, freq_t, freq_r, seed):
    """Seamless in theta: 3D value noise on (cos, sin) x radius."""
    rho = np.broadcast_to(rho, np.shape(theta))
    P = np.stack([np.cos(theta) * freq_t, np.sin(theta) * freq_t, rho * freq_r], -1)
    return gsm.vnoise(P, 1.0, seed)


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


def iris(preset, r, th, rng, seed):
    """One iris (linear colour) and its coverage (1 inside the limbus, soft at the edge)."""
    p = {k: lin(v) if isinstance(v, tuple) else v for k, v in preset.items()}
    rho = np.clip((r - R_PUPIL) / (R_IRIS - R_PUPIL), 0, 1)
    # the collarette: a wavy ring about a third of the way out, inner zone inside it
    rc = 0.33 + 0.045 * ring_noise(th, 0, 9, 0, seed + 1) + 0.02 * ring_noise(th, 0, 23, 0, seed + 2)
    inner = 1 - smoothstep(rc - 0.08, rc + 0.10, rho + 0.05 * ring_noise(th, rho, 25, 4.0, seed + 8))
    base = p["inner"] * inner[..., None] + p["outer"] * (1 - inner[..., None])
    # radial fibres: many fine streaks, wavy, stronger outside the collarette
    tw = th + 0.05 * ring_noise(th, rho, 5, 3.0, seed + 11) + 0.015 * ring_noise(th, rho, 18, 6.0, seed + 12)
    fib = (0.55 * ring_noise(tw, rho, 70, 3.0, seed + 3) + 0.3 * ring_noise(tw, rho, 140, 5.0, seed + 4)
           + 0.15 * ring_noise(tw, rho, 260, 9.0, seed + 5))
    clump = np.clip(0.55 + 0.7 * ring_noise(tw, rho, 22, 2.5, seed + 13), 0.15, 1.2)
    fib = (np.clip(0.5 + 0.9 * fib, 0, 1) ** 1.6) * clump
    fw = p["fibrous"] * (0.55 + 0.45 * (1 - inner)) * 0.85
    col = base * (1 - fw * fib)[..., None] + p["fibre"] * (fw * fib)[..., None]
    # crypts: dark radially-stretched lacunae across the middle
    crypt = np.zeros_like(r)
    for _ in range(int(rng.integers(22, 34))):
        t0, r0 = rng.uniform(-np.pi, np.pi), rng.uniform(0.22, 0.72)
        dt = np.angle(np.exp(1j * (th - t0)))
        a, b = rng.uniform(0.05, 0.12), rng.uniform(0.04, 0.09)
        crypt = np.maximum(crypt, np.exp(-((dt / a) ** 2 + ((rho - r0) / b) ** 2)) * rng.uniform(0.5, 1.0))
    crypt *= np.clip(0.6 + 0.8 * ring_noise(th, rho, 30, 2.0, seed + 6), 0, 1)
    col = col * (1 - 0.85 * crypt[..., None]) + p["crypt"] * (0.85 * crypt[..., None])
    # the collarette itself: a light, broken, zigzag ridge
    ridge = np.exp(-((rho - rc) / 0.025) ** 2) * np.clip(0.5 + 0.8 * ring_noise(th, 0, 40, 0, seed + 7), 0, 1)
    col = col * (1 - 0.55 * ridge[..., None]) + p["collar"] * (0.55 * ridge[..., None])
    # contraction furrows: broken concentric dark arcs near the edge
    furrow = 0
    for k, rf in enumerate((0.72, 0.8, 0.88)):
        furrow = furrow + np.exp(-((rho - rf - 0.01 * ring_noise(th, 0, 12, 0, seed + 10 + k)) / 0.008) ** 2) \
            * np.clip(ring_noise(th, 0, 7, 0, seed + 20 + k), 0, 1)
    col = col * (1 - 0.3 * np.clip(furrow, 0, 1))[..., None]
    # iris freckles, sometimes
    for _ in range(int(rng.integers(0, 3))):
        t0, r0 = rng.uniform(-np.pi, np.pi), rng.uniform(0.4, 0.85)
        d = np.hypot(np.angle(np.exp(1j * (th - t0))) * (R_PUPIL + r0 * (R_IRIS - R_PUPIL)), (rho - r0) * (R_IRIS - R_PUPIL))
        col = col * (1 - 0.6 * np.exp(-(d / rng.uniform(2.5, 5)) ** 2))[..., None]
    # the limbal ring: a soft dark band into the white
    limb = smoothstep(0.80, 1.0, rho) * (1 - smoothstep(1.0, 1.12, (r - R_PUPIL) / (R_IRIS - R_PUPIL)))
    col = col * (1 - 0.55 * limb)[..., None]
    # the pupil and its ruff
    ruff = np.exp(-(((r - R_PUPIL) / 3.0) ** 2)) * np.clip(0.6 + 0.6 * ring_noise(th, 0, 50, 0, seed + 30), 0, 1)
    col = col * (1 - 0.5 * ruff)[..., None]
    pupil = 1 - smoothstep(R_PUPIL - 2.0, R_PUPIL + 1.0, r)
    col = col * (1 - pupil[..., None]) + lin((0.02, 0.018, 0.018)) * pupil[..., None]
    cover = 1 - smoothstep(R_IRIS - 1.0, R_IRIS + 7.0, r)
    return col, cover


def vessels(rng, cx, cy, count, width, reach, seed):
    """Vessels grown inward from the edge of the white: thinning, wandering, branching walks."""
    from PIL import ImageDraw  # noqa: PLC0415
    big = 2
    im = Image.new("F", (N * big, N * big), 0.0)
    d = ImageDraw.Draw(im)
    stack = []
    for _ in range(count):
        a = rng.uniform(-np.pi, np.pi)
        r0 = R_BALL * rng.uniform(0.9, 1.0)
        stack.append((cx + r0 * np.cos(a), cy + r0 * np.sin(a), a + np.pi + rng.normal(0, 0.25),
                      width * rng.uniform(0.6, 1.0), rng.uniform(0.5, 1.0), 0))
    while stack:
        x, y, h, w, s, depth = stack.pop()
        while w > 0.25:
            nx, ny = x + 2.0 * np.cos(h), y + 2.0 * np.sin(h)
            if np.hypot(nx - cx, ny - cy) < R_IRIS + reach:
                break
            d.line([(x * big, y * big), (nx * big, ny * big)], fill=float(s), width=max(1, int(round(w * big))))
            x, y = nx, ny
            h += rng.normal(0, 0.22)
            w *= 0.985
            if depth < 3 and rng.random() < 0.05:
                stack.append((x, y, h + rng.choice([-1, 1]) * rng.uniform(0.4, 1.0), w * 0.7, s * 0.9, depth + 1))
    a = np.asarray(im.resize((N, N), Image.BILINEAR), dtype=np.float64)
    return np.clip(gsm.blur(a, 1), 0, 1)


def eye_picture(colour: str, condition: str):
    rng = np.random.default_rng(SEED + sum(map(ord, colour)) * 7 + (1 if condition == "Bloodshot" else 0))
    white_c, white_e = WHITE_CENTRE, WHITE_EDGE
    vessel_c = lin((0.55, 0.12, 0.10))
    out = np.zeros((N, N, 3)) + lin((0.70, 0.66, 0.64))      # beyond the islands: a neutral white
    for k, (cx, cy) in enumerate(CENTRES):
        r, th = polar(cx, cy)
        u = np.clip(r / R_BALL, 0, 1.2)
        white = white_c * (1 - smoothstep(0.35, 1.0, u)[..., None]) + white_e * smoothstep(0.35, 1.0, u)[..., None]
        white = white * (1 + 0.03 * gsm.vnoise(np.stack([r * np.cos(th), r * np.sin(th), np.zeros_like(r)], -1), 18.0, SEED + k)[..., None])
        if condition == "Bloodshot":
            flush = smoothstep(0.45, 1.0, u)
            white = white * (1 - 0.35 * flush[..., None]) + lin((0.80, 0.45, 0.42)) * (0.35 * flush[..., None])
            v = vessels(rng, cx, cy, 34, 2.6, 18, SEED + k)
            amt = 0.85
        else:
            v = vessels(rng, cx, cy, 11, 1.6, 60, SEED + k)
            amt = 0.5
        v = v * smoothstep(R_IRIS + 10, R_IRIS + 70, r)
        white = white * (1 - amt * v[..., None]) + vessel_c * (amt * v[..., None])
        col, cover = iris(PRESETS[colour], r, th, np.random.default_rng(SEED + k * 13 + sum(map(ord, colour))), SEED + 97 * k)
        eye = col * cover[..., None] + white * (1 - cover[..., None])
        inside = r < R_BALL + 6
        out[inside] = eye[inside]
    r, _ = polar(CORNER[0], CORNER[1])
    out[r < CORNER[2]] = lin((0.02, 0.018, 0.018))
    srgb = gsm._linear_to_srgb(np.clip(out, 0, 1))
    return np.round(srgb * 255).astype(np.uint8)


def names():
    for c in PRESETS:
        yield c, "Clean"
    for c in BLOODSHOT_OF:
        yield c, "Bloodshot"


def picture_name(colour, condition):
    return f"Synth{colour}{'' if condition == 'Clean' else condition}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("colours", nargs="*", help=f"some of {list(PRESETS)} (default: all)")
    ap.add_argument("--out", type=Path, help="write here instead (a trial: no provenance)")
    a = ap.parse_args(argv)
    out = a.out or OUT
    out.mkdir(parents=True, exist_ok=True)
    written = []
    for colour, cond in names():
        if a.colours and colour not in a.colours:
            continue
        px = eye_picture(colour, cond)
        p = out / f"{picture_name(colour, cond)}_basecolor_{TAG}.png"
        Image.fromarray(px, "RGB").save(p, optimize=True)
        written.append(p.name)
        print(p)
    if not a.out:
        files = sorted(f.name for f in OUT.glob(f"Synth*_basecolor_{TAG}.png"))
        PROVENANCE.write_text("\n".join([
            "# Provenance for the SYNTHETIC eye test pictures (the lead's spike, 2026-10-26): drafts beside",
            "# the fit set's nine MakeHuman eyes, on MakeHuman_Eyes_v01. Procedural only: no photograph, no",
            "# AI. Written by `evidence`.",
            "id: fit/makehuman/synth_eyes",
            "version: v01",
            "files:",
            *[f"  - MatterLibrary/textures/fit/makehuman/eyes/{f}" for f in files],
            "provenance:",
            "  source: procedural",
            "  license: CC0-1.0",
            "  evidence: tools/converters/fit/gen_synth_eyes.py",
            "  method: \"iris layers after Lefohn et al. 2003 (CG&A 23(6)); light irises fibrous, brown smooth (Berard et al. 2016); low-melanin colour as stromal scattering (Lam & Baranoski 2006); values judgement\"",
        ]) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
