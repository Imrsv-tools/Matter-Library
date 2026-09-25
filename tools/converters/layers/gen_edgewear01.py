#!/usr/bin/env python3
"""Generate the shared overlay `EdgeWear01` (Phase03 step 3.5): chipped, rounded wear.

The DAMAGE overlay (slot 1) for fired clay, stone and painted edges: small chips where the
surface has knocked off, each a shallow dent with a rounded rim, the exposed body a little
rougher. Frozen overlay contract: R/G normal XY (0.5 flat) · B roughness bias · A density.

Scale `s01`: a 0.1 m tile, so chips are ~2-8 mm. Seamless (tileable.py), fixed seed.

    gen_edgewear01.py [--out DIR]      # default: MatterLibrary/textures/shared/overlays/

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
NAME = "EdgeWear01_overlay_s01.png"
SEED = 401


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the EdgeWear01 shared overlay.")
    ap.add_argument("--out", default=str(ROOT / "MatterLibrary" / "textures" / "shared" / "overlays"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety)", file=sys.stderr)
        return 1
    field = tl.fbm((24, 48, 96), SEED)                         # where chips cluster
    chips = np.clip((field - 0.66) * 8, 0, 1)                  # sparse chip bodies
    edge = np.clip((field - 0.62) * 8, 0, 1) - chips           # a rounded rim around each
    height = -chips + 0.35 * np.clip(edge, 0, 1)               # a dent with a lip
    img = tl.pack_overlay(height, strength=10.0,
                          rough_bias=0.35 * chips + 0.15 * np.clip(edge, 0, 1),
                          density=np.clip(chips + 0.6 * np.clip(edge, 0, 1), 0, 1))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
