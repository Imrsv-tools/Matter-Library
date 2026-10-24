#!/usr/bin/env python3
"""Generate the shared overlay `Scratches01`: handling scratches, as a 10 cm tile.

A DAMAGE overlay for hard surfaces that get handled, knocked and wiped (painted and bare metal,
glazed ceramic, glass, stone, hard plastics): scattered single scratches running every which
way, coarser and far sparser than `HairlineScratches01`, a few long ones among many short,
each a shallow groove bending a little and tapering out at both ends. They cover the tile
evenly; any unevenness is left to a mask (worn patches inside a tile repeat with it and read
as a grid on highlights; Phase11 F-P11-14). Frozen overlay contract (MasterSet.md):

    R/G = normal XY (0.5 = flat)  ·  B = roughness bias (only roughens)  ·  A = density

B is filled everywhere (a renderer filters A and B separately, so a B masked to a thin line
would multiply down to almost nothing at a distance; Phase11 F-P11-7). Outside a scratch
A = 0, so the B there never applies.

Scale `s01` (10 cm tile, 2048 px, 0.05 mm per pixel; the lead, 2026-10-25): scratches 2-30 mm
long and 20-100 µm wide, so most are about a pixel wide and are drawn as anti-aliased lines
whose strength stands for their width. Was a 1 cm tile of value noise in
`gen_shared_textures.py` (`s001`), which repeated every 14 px of the parity rig's close-up and
read UNEVEN, strongest in Blender, as the 1 cm HairlineScratches01 did (F-P11-14). Matched to
it, filtered to 0.1 and 0.5 mm per pixel, so the articles that carry it keep their look: mean
density 0.068, density x roughness bias 0.022. Segments wrap toroidally, so the tile is
seamless. Fixed seed, no network: byte-stable.

    gen_scratches01.py [--out DIR]       # default: MatterLibrary/textures/shared/overlays/

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
NAME = "Scratches01_overlay_s01.png"
SEED = 1701
SIZE = 2048            # over 10 cm: 0.049 mm per pixel
PX_MM = 100 / SIZE
SCRATCHES = 1500       # per 10 cm tile
# Matched to the 1 cm version, filtered to 0.1 and 0.5 mm per pixel: mean density 0.068,
# mean density x roughness bias 0.022 (2026-10-25).
COVER_GAIN = 1.0       # density per pixel of width
ROUGH = 0.32           # mean roughness bias
STRENGTH = 2.0         # normal strength


def scratches() -> tuple:
    rng = np.random.RandomState(SEED)
    cells = rng.permutation(SCRATCHES)                           # one cell of a grid each:
    side = int(np.ceil(np.sqrt(SCRATCHES)))                      # even cover, no patches (F-P11-14)
    groove = np.zeros((SIZE, SIZE))
    cover = np.zeros((SIZE, SIZE))
    for k in range(SCRATCHES):
        cx = (cells[k] % side + rng.rand()) / side * SIZE
        cy = (cells[k] // side + rng.rand()) / side * SIZE
        th = rng.rand() * np.pi                                  # every which way
        length = (2 + 28 * rng.rand() ** 2.2) / PX_MM            # 2-30 mm, mostly short, in px
        hw = (0.01 + 0.04 * rng.rand() ** 1.5) / PX_MM           # half-width 10-50 µm, in px
        bend = rng.randn() * 0.035                               # sagitta / length: nearly straight
        depth = 0.35 + 0.65 * rng.rand()
        ux, uy = np.cos(th), np.sin(th)
        vx, vy = -uy, ux
        n = max(2, int(length))
        t = np.linspace(0, 1, n)
        off = bend * length * 4 * t * (1 - t)
        px_ = cx + (t - 0.5) * length * ux + off * vx            # the scratch's centre line
        py_ = cy + (t - 0.5) * length * uy + off * vy
        pad = int(np.ceil(hw + 3))
        x0, x1 = int(np.floor(px_.min())) - pad, int(np.ceil(px_.max())) + pad
        y0, y1 = int(np.floor(py_.min())) - pad, int(np.ceil(py_.max())) + pad
        xs, ys = np.arange(x0, x1 + 1), np.arange(y0, y1 + 1)
        gx, gy = np.meshgrid(xs, ys)
        # nearest centre-line sample per pixel (samples are a pixel apart, so this is sub-pixel close)
        step = max(1, n // 400)
        best = np.full(gx.shape, np.inf)
        bt = np.zeros(gx.shape)
        for i in range(0, n, step):
            d2 = (gx - px_[i]) ** 2 + (gy - py_[i]) ** 2
            m = d2 < best
            best[m], bt[m] = d2[m], t[i]
        dist = np.sqrt(best)
        taper = np.sin(np.pi * bt) ** 0.5
        w = hw * taper
        prof = np.clip(1 - dist / np.maximum(w + 0.5, 0.5), 0, 1)   # a V groove, at least a pixel wide
        line = prof * depth * np.minimum(1.0, 2 * w)             # depth: thinner = shallower
        wide = np.clip(1 - dist / (w + 1.0), 0, 1) * COVER_GAIN * np.minimum(1.0, 2 * w + 0.4) * (0.4 + 0.6 * depth)
        sub = np.ix_(ys % SIZE, xs % SIZE)
        groove[sub] = np.maximum(groove[sub], line)
        cover[sub] = np.maximum(cover[sub], wide)
    return groove, np.clip(cover, 0, 1)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Scratches01 shared overlay.")
    ap.add_argument("--out", default=str(ROOT / "MatterLibrary" / "textures" / "shared" / "overlays"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety)", file=sys.stderr)
        return 1
    groove, cover = scratches()
    img = tl.pack_overlay(-groove, strength=STRENGTH,
                          rough_bias=ROUGH + 0.12 * (tl.noise(240, SEED + 2, SIZE) - 0.5),
                          density=cover)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
