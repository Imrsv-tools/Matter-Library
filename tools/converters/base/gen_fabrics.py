#!/usr/bin/env python3
"""Generate the fabric base texture sets (Phase07 step 7.5; lane L2): the structure of each
fabric at real size, on a 1 cm tile (scale `s001`, 1024 px, ~10 um per pixel).

- **Cotton_Jersey** — single-jersey knit (a T-shirt): columns of V-shaped loops, 12 wales and
  16 courses per centimetre. Normal and roughness; no colour (the article's constant is the
  yarn's colour, which a Creator tints).
- **Denim_Twill** — a 3/1 warp-faced twill, 32 ends and 32 picks per centimetre: the indigo
  warp floats over three picks and under one, stepping one thread per pick, so the diagonal
  wale runs up and to the right, and the white weft shows in one cell of four. Base colour
  (indigo warp, undyed weft, with thread-to-thread variation only: coarser variation would
  repeat every centimetre), normal, roughness.
- **Leather_Grain** — a pebbled full-grain hide: rounded cells about 0.8 mm across (12 per
  centimetre, jittered), with creases between them. Normal and roughness.
- **Denim_TwillLight** (Phase08 8.3) — Denim_Twill's weave, light-washed: base colour only (its
  normal and roughness are Denim_Twill's).
- **Canvas_Duck** (Phase08 8.4) — cotton duck, a heavy plain weave, 16 ends x 14 picks per
  centimetre, crowned floats and thread-to-thread slub. Normal and roughness.

Seamless (tileable.py; every count divides the tile, and the cell pattern wraps), fixed seeds,
no network. Writes MatterLibrary/textures/base/synthetic/textile/<Set>_<channel>_s001.png.

    gen_fabrics.py [--out DIR] [--sets NAME ...]

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
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "synthetic" / "textile"
SCALE = "s001"
N = tl.SIZE
Y, X = np.mgrid[0:N, 0:N] / N          # tile coordinates in [0, 1)


def jersey(seed: int = 7501, wales: int = 12, courses: int = 16, fuzz: float = 0.15,
           rough0: float = 0.82) -> dict:
    """Knit loops: in each wale two legs lean in to a V, one course high."""
    s = (X * wales) % 1.0                # across a wale
    t = (Y * courses) % 1.0              # up a course
    lean = 0.14 * (t - 0.5)
    leg = lambda c: np.exp(-((s - c) ** 2) / (2 * 0.09 ** 2))   # noqa: E731
    loops = np.maximum(leg(0.28 + lean), leg(0.72 - lean))
    loops *= 0.75 + 0.25 * np.sin(np.pi * t)                    # each loop rounds over the course
    fibre = tl.fbm((64, 128, 256), seed)                        # fuzz on the yarn
    height = loops + fuzz * fibre
    rough = rough0 + 0.06 * (fibre - 0.5) - 0.04 * loops
    return {"normal": tl.normal_map(height, strength=2.0), "roughness": tl.gray(rough)}


def stretch_knit(seed: int = 7507) -> dict:
    """Phase08 8.4: a synthetic stretch single jersey (polyester with elastane: leggings,
    sportswear, a fitted top). Cotton_Jersey's loop, knitted finer (20 wales x 28 courses per
    cm) from smooth continuous filament, so almost no fibre fuzz and a lower roughness: the
    soft sheen of a performance knit. Normal and roughness only."""
    return jersey(seed, wales=20, courses=28, fuzz=0.04, rough0=0.55)


def suiting(seed: int = 7508) -> dict:
    """Phase08 8.4: a worsted wool suiting, a fine 2/2 twill, 36 ends x 32 picks per cm, in
    smooth combed yarn. Two up, two down, stepping one per pick: a balanced twill, so its wale
    is quieter than denim's warp-faced 3/1. Colour is the article's constant (a suit is
    piece-dyed, warp and weft alike). Normal and roughness only."""
    ends, picks = 36, 32
    X, Y = half_thread(ends, picks)
    i = np.floor(X * ends).astype(int)
    j = np.floor(Y * picks).astype(int)
    warp_up = ((i + j) % 4) < 2
    u = (X * ends) % 1.0
    v = (Y * picks) % 1.0
    warp_h = np.sin(np.pi * u) ** 0.6
    weft_h = np.sin(np.pi * v) ** 0.6
    slub = tl.fbm((64, 128), seed)
    fibre = tl.fbm((128, 256), seed + 1)
    height = np.where(warp_up, warp_h, weft_h) * (0.92 + 0.16 * slub) + 0.08 * fibre
    rough = 0.72 + 0.05 * (fibre - 0.5) - 0.04 * height
    return {"normal": tl.normal_map(height, strength=2.5), "roughness": tl.gray(rough)}


def twill(seed: int = 7502, indigo=(0.020, 0.040, 0.120), worn=(0.050, 0.080, 0.180)) -> dict:
    """3/1 twill: warp (vertical) up in three cells of four, the step moving one per pick."""
    ends = picks = 32
    i = np.floor(X * ends).astype(int)   # warp thread (column)
    j = np.floor(Y * picks).astype(int)  # weft thread (row)
    warp_up = ((i + j) % 4) != 0
    u = (X * ends) % 1.0                 # across a warp thread
    v = (Y * picks) % 1.0                # across a weft thread
    warp_h = np.sin(np.pi * u) ** 0.6    # a round thread, seen across
    weft_h = np.sin(np.pi * v) ** 0.6
    # Only THREAD-scale variation lives in the tile. Anything coarser (slub runs, fading) would
    # repeat every centimetre and read as a regular blotch pattern across a garment (measured on
    # the body, 7.5.2); fading is wear, which is a wear layer's job at its own size.
    slub = tl.fbm((64, 128), seed)       # thread-to-thread thickness
    height = np.where(warp_up, warp_h, weft_h) * (0.9 + 0.2 * slub)
    # colour, linear: rope-dyed indigo warp, lighter where the ring-dyed yarn's core shows, and
    # an undyed, slightly warm weft
    fade = tl.fbm((64, 128, 256), seed + 1)
    indigo = np.array(indigo)
    worn = np.array(worn)
    warp_c = indigo + (worn - indigo) * fade[..., None]
    warp_c *= (0.92 + 0.16 * slub)[..., None]
    # the weft shows only in the gap between two warp floats, partly shadowed by them, so its
    # visible colour is dimmer than the yarn's own and blends into the warp at the cell's sides
    weft_c = np.array([0.42, 0.40, 0.36]) * (0.9 + 0.2 * tl.fbm((64, 128), seed + 2))[..., None]
    weft_c = weft_c * (0.35 + 0.65 * np.sin(np.pi * u) ** 2)[..., None] + indigo * (0.65 - 0.65 * np.sin(np.pi * u) ** 2)[..., None]
    colour = np.where(warp_up[..., None], warp_c, weft_c)
    colour *= (0.8 + 0.2 * np.where(warp_up, warp_h, weft_h))[..., None]   # thread shading
    rough = 0.78 + 0.05 * (slub - 0.5) - 0.05 * height
    return {"basecolor": tl.rgb(tl.linear_to_srgb(colour)), "normal": tl.normal_map(height, strength=2.5),
            "roughness": tl.gray(rough)}


def grain(seed: int = 7503) -> dict:
    """Pebble grain: jittered cells, raised in the middle, creased at the borders (toroidal)."""
    cells = 12
    rng = np.random.RandomState(seed)
    pts = (np.stack(np.meshgrid(np.arange(cells), np.arange(cells)), -1).reshape(-1, 2)
           + 0.15 + 0.7 * rng.rand(cells * cells, 2)) / cells
    d1 = np.full((N, N), 9.0)
    d2 = np.full((N, N), 9.0)
    for px, py in pts:                   # nearest and second-nearest seed, wrapped
        dx = np.abs(X - px)
        dy = np.abs(Y - py)
        d = np.hypot(np.minimum(dx, 1 - dx), np.minimum(dy, 1 - dy))
        d2 = np.where(d < d1, d1, np.minimum(d2, d))
        d1 = np.minimum(d1, d)
    edge = np.clip((d2 - d1) * cells * 3.0, 0, 1)   # 0 on a crease, 1 inside a cell
    fine = tl.fbm((48, 96, 192), seed + 1)
    height = np.sqrt(edge) + 0.12 * fine
    rough = 0.50 + 0.12 * (1 - edge) + 0.05 * (fine - 0.5)    # creases hold less finish
    return {"normal": tl.normal_map(height, strength=2.0), "roughness": tl.gray(rough)}


def twill_light(seed: int = 7502) -> dict:
    """Phase08 8.3: the same twill, light-washed (bleached indigo), authored light so a Creator's
    tint (a 0-1 multiply) reaches the darker washes and other colours (RD-P08-5). The weave, seed
    and so the normal and roughness are Denim_Twill's, so only the colour is written."""
    t = twill(seed, indigo=(0.22, 0.33, 0.55), worn=(0.32, 0.45, 0.66))
    return {"basecolor": t["basecolor"]}


def half_thread(ends: int, picks: int) -> tuple:
    """Tile coordinates shifted half a thread, so the tile's edge runs down the middle of a
    thread instead of along the crease between two. The weave is seamless either way; this keeps
    the rig's seam measure (wrap edge vs neighbouring pixels) from reading a thread border that
    happens to fall on the edge as a seam (Phase08 8.4)."""
    return (X + 0.5 / ends) % 1.0, (Y + 0.5 / picks) % 1.0


def canvas(seed: int = 7504) -> dict:
    """Phase08 8.4: cotton duck, a heavy plain weave, 16 ends x 14 picks per centimetre (plied
    yarn about 0.6 mm thick). Each thread passes over one and under the next, so every cell is a
    short float that crowns in its middle (the crimp). Yarn thickness varies thread to thread
    (the duck's irregular slub), and loose fibres fuzz the surface. Normal and roughness only:
    the colour is the article's constant, which a Creator tints."""
    ends, picks = 16, 14
    X, Y = half_thread(ends, picks)
    i = np.floor(X * ends).astype(int)
    j = np.floor(Y * picks).astype(int)
    u = (X * ends) % 1.0                 # across a warp thread
    v = (Y * picks) % 1.0                # across a weft thread
    rng = np.random.RandomState(seed)
    warp_thick = (0.85 + 0.3 * rng.rand(ends))[i]     # per-thread slub, constant along it
    weft_thick = (0.85 + 0.3 * rng.rand(picks))[j]
    # Two layers of continuous round threads; each one's centreline rises and falls (the crimp)
    # with a period of two crossings, in opposite phase to its neighbours. What shows is the
    # higher of the two at each point, so the warp is up where (i + j) is even.
    warp_r = np.sqrt(np.clip(1 - (2 * u - 1) ** 2, 0, 1)) * warp_thick
    weft_r = np.sqrt(np.clip(1 - (2 * v - 1) ** 2, 0, 1)) * weft_thick
    warp_z = 0.6 * warp_r + 0.4 * np.cos(np.pi * (Y * picks - 0.5 + i))
    weft_z = 0.6 * weft_r - 0.4 * np.cos(np.pi * (X * ends - 0.5 + j))
    warp_on = warp_z >= weft_z
    along = np.where(warp_on, Y * picks, X * ends)
    across = np.where(warp_on, u, v)
    ply = 0.05 * np.sin(2 * np.pi * (along * 3 + across))   # the plied yarn's twist
    fibre = tl.fbm((64, 128, 256), seed + 1)
    height = np.maximum(warp_z, weft_z) + ply + 0.08 * fibre
    rough = 0.86 + 0.05 * (fibre - 0.5) - 0.04 * height
    return {"normal": tl.normal_map(height, strength=6.0), "roughness": tl.gray(rough)}


def satin(seed: int = 7505) -> dict:
    """Phase08 8.4: a five-end warp satin in fine filament yarn, 100 ends x 40 picks per
    centimetre. Each warp floats over four picks and dips under the fifth; the dips step two
    ends per pick (the satin move), so they scatter instead of lining up into a twill wale. The
    face is almost all warp float, which is why satin is smooth and its highlight runs along the
    warp (the article's anisotropy). Normal and roughness only."""
    ends, picks = 100, 40
    X, Y = half_thread(ends, picks)
    i = np.floor(X * ends).astype(int)
    j = np.floor(Y * picks).astype(int)
    u = (X * ends) % 1.0
    v = (Y * picks) % 1.0
    down = (j % 5) == ((2 * i) % 5)      # this warp dips under this pick
    float_h = np.sin(np.pi * u) ** 0.3   # a flat filament bundle, barely rounded
    dip = np.exp(-((v - 0.5) ** 2) / (2 * 0.22 ** 2))
    height = 0.25 * float_h - np.where(down, 0.9 * dip, 0.0)
    sheen = tl.fbm((128, 256), seed)     # filament-to-filament lustre variation
    height = height + 0.04 * sheen
    rough = 0.24 + 0.04 * (sheen - 0.5) + np.where(down, 0.12 * dip, 0.0)
    return {"normal": tl.normal_map(height, strength=1.5), "roughness": tl.gray(rough)}


def felt(seed: int = 7506, fibres: int = 2400) -> dict:
    """Phase08 8.4: pressed wool felt, a non-woven: short fibres (1.5-4 mm, ~25 um thick)
    matted at random angles, over a cloudy density (thicker and thinner patches of the batt).
    No weave, so no regular structure at all. Normal and roughness only."""
    rng = np.random.RandomState(seed)
    batt = tl.fbm((8, 16, 32), seed)                       # the matted batt's density
    strands = np.zeros((N, N))
    for _ in range(fibres):                                 # each fibre a short soft line, wrapped
        x0, y0 = rng.rand(2) * N
        ang = rng.rand() * np.pi
        steps = int((1.5 + 2.5 * rng.rand()) * N / 10)      # 1.5-4 mm; the tile is 10 mm
        t = np.arange(steps)
        curl = 0.4 * np.sin(t / max(steps, 1) * np.pi * rng.rand() * 3)   # a crimped wool fibre
        xs = (x0 + t * np.cos(ang + curl)).astype(int) % N
        ys = (y0 + t * np.sin(ang + curl)).astype(int) % N
        strands[ys, xs] += 1.0
    # soften each fibre to ~3 px (about 25 um) with a wrapped box blur
    for _ in range(2):
        strands = (strands + np.roll(strands, 1, 0) + np.roll(strands, -1, 0)
                   + np.roll(strands, 1, 1) + np.roll(strands, -1, 1)) / 5
    strands = strands / strands.max()
    height = 0.6 * batt + 1.2 * np.sqrt(strands) + 0.1 * tl.fbm((128, 256), seed + 1)
    rough = 0.92 + 0.04 * (batt - 0.5) - 0.03 * np.sqrt(strands)
    return {"normal": tl.normal_map(height, strength=3.0), "roughness": tl.gray(rough)}


SETS = {"Cotton_Jersey": jersey, "Denim_Twill": twill, "Leather_Grain": grain,
        "Denim_TwillLight": twill_light, "Canvas_Duck": canvas, "Satin_Warp": satin,
        "Felt_Wool": felt, "Knit_Stretch": stretch_knit, "Wool_Suiting": suiting}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the fabric base texture sets.")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--sets", nargs="+", choices=sorted(SETS), default=sorted(SETS),
                    help="only these sets (default: all)")
    args = ap.parse_args(argv)
    out = Path(args.out)
    made = {name: SETS[name]() for name in args.sets}
    targets = {(name, ch): out / f"{name}_{ch}_{SCALE}.png" for name, maps in made.items() for ch in maps}
    if any(p.exists() for p in targets.values()):
        print(f"refusing to overwrite a fabric set in {out} (Build Safety); use --out <dir>", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)
    for (name, ch), p in targets.items():
        made[name][ch].save(p, "PNG", optimize=True)
        print(f"wrote {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
