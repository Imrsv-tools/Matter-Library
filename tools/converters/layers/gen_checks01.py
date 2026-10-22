#!/usr/bin/env python3
"""Generate the shared overlay `Checks01` (batch 261022-1): weathering checks in wood.

The DAMAGE overlay (slot 1) for weathered and dried timber: the long, narrow splits that open
ALONG THE GRAIN as wood dries and weathers outdoors (a deck board, a fence rail, a barn
beam), not the cell network of `Cracks01` (crazing, right for glaze, plaster and dried mud;
the maintainer's redo of WhiteOak_Weathered: "Cracks01 is crazing, wrong for wood"). Each
check runs along U, the library's grain direction (the wood generators lay their grain along
U), wandering a little across it as the grain does, widest in its middle and closing to
nothing at both ends. A few long open checks, more short hairline ones. Each is a V-shaped
groove, so its two walls tilt opposite ways and it reads dark under any light, and its inside
is rough. Frozen overlay contract (MasterSet.md):

    R/G = normal XY (0.5 = flat)  ·  B = roughness bias (only roughens)  ·  A = density

B is filled everywhere (a renderer filters A and B separately, so a B masked to the thin
check would multiply down to almost nothing at a distance; Phase11 F-P11-7). Outside a check
A = 0, so the B there never applies.

Scale `s01` (0.1 m tile, 0.1 mm per pixel): open checks 2-9 cm long and 0.6-2 mm wide,
hairlines 0.5-3 cm and under 0.3 mm. Checks wrap toroidally, so the tile is seamless.
Fixed seed, no network: byte-stable.

    gen_checks01.py [--out DIR]        # default: MatterLibrary/textures/shared/overlays/

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
NAME = "Checks01_overlay_s01.png"
SEED = 2261
SIZE = tl.SIZE
OPEN = 20              # open checks per 0.1 m tile
HAIRLINE = 26          # hairline checks per tile


def checks() -> tuple:
    rng = np.random.RandomState(SEED)
    groove = np.zeros((SIZE, SIZE))
    cover = np.zeros((SIZE, SIZE))
    kinds = [(True, OPEN), (False, HAIRLINE)]
    for is_open, n in kinds:
        rows = rng.permutation(n)                              # spread across the grain
        for k in range(n):
            cx = rng.rand() * SIZE
            cy = (rows[k] + rng.rand()) / n * SIZE
            if is_open:
                length = 200 + 700 * rng.rand() ** 1.3             # px: 2-9 cm
                hw = 3.0 + 7.0 * rng.rand() ** 1.5                 # half-width px: 0.6-2 mm wide
            else:
                length = 50 + 250 * rng.rand()                     # 0.5-3 cm
                hw = 0.5 + 1.0 * rng.rand()                        # under 0.3 mm wide
            slope = rng.randn() * 0.012                            # the grain a little off U
            amp1, amp2 = rng.rand() * 3.0, rng.rand() * 0.5        # wander across the grain, px
            ph1, ph2 = rng.rand(2) * 2 * np.pi
            f1 = length / (250 + 250 * rng.rand())                 # a slow wave every 2.5-5 cm
            f2 = length / (60 + 60 * rng.rand())                   # a faint one every 6-12 mm
            x0 = cx - length / 2
            xs = np.arange(int(np.floor(x0)), int(np.ceil(x0 + length)) + 1)
            t = np.clip((xs - x0) / length, 0, 1)
            yc = (cy + slope * (xs - cx) + amp1 * np.sin(2 * np.pi * f1 * t + ph1)
                  + amp2 * np.sin(2 * np.pi * f2 * t + ph2))
            w = hw * np.sin(np.pi * t) ** 0.6                      # closes to nothing at both ends
            pad = int(np.ceil(hw + 4))
            ys = np.arange(int(np.floor(yc.min())) - pad, int(np.ceil(yc.max())) + pad + 1)
            d = np.abs(ys[:, None] - yc[None, :])
            g = np.clip(1.0 - d / np.maximum(w, 1e-3)[None, :], 0, 1) ** 0.8 * (w > 0.05)[None, :]
            a = np.clip(1.0 - d / (w + 2.0)[None, :], 0, 1) * (w > 0.05)[None, :]
            if not is_open:
                g = g * 0.7
            sub = np.ix_(ys % SIZE, xs % SIZE)
            groove[sub] = np.maximum(groove[sub], g)
            cover[sub] = np.maximum(cover[sub], a)
    return groove, np.clip(cover * 1.4, 0, 1)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Checks01 shared overlay.")
    ap.add_argument("--out", default=str(ROOT / "MatterLibrary" / "textures" / "shared" / "overlays"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety)", file=sys.stderr)
        return 1
    groove, density = checks()
    img = tl.pack_overlay(-groove, strength=9.0,                 # a split: steep walls, reads dark
                          rough_bias=0.55 + 0.15 * tl.noise(40, SEED + 7),
                          density=density)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
