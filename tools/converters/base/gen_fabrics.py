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

Seamless (tileable.py; every count divides the tile, and the cell pattern wraps), fixed seeds,
no network. Writes MatterLibrary/textures/base/synthetic/textile/<Set>_<channel>_s001.png.

    gen_fabrics.py [--out DIR]

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


def jersey(seed: int = 7501) -> dict:
    """Knit loops: in each wale two legs lean in to a V, one course high."""
    wales, courses = 12, 16
    s = (X * wales) % 1.0                # across a wale
    t = (Y * courses) % 1.0              # up a course
    lean = 0.14 * (t - 0.5)
    leg = lambda c: np.exp(-((s - c) ** 2) / (2 * 0.09 ** 2))   # noqa: E731
    loops = np.maximum(leg(0.28 + lean), leg(0.72 - lean))
    loops *= 0.75 + 0.25 * np.sin(np.pi * t)                    # each loop rounds over the course
    fibre = tl.fbm((64, 128, 256), seed)                        # fuzz on the yarn
    height = loops + 0.15 * fibre
    rough = 0.82 + 0.06 * (fibre - 0.5) - 0.04 * loops
    return {"normal": tl.normal_map(height, strength=2.0), "roughness": tl.gray(rough)}


def twill(seed: int = 7502) -> dict:
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
    indigo = np.array([0.020, 0.040, 0.120])
    worn = np.array([0.050, 0.080, 0.180])
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


SETS = {"Cotton_Jersey": jersey, "Denim_Twill": twill, "Leather_Grain": grain}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the fabric base texture sets.")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args(argv)
    out = Path(args.out)
    made = {name: fn() for name, fn in SETS.items()}
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
