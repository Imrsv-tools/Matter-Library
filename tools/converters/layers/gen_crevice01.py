#!/usr/bin/env python3
"""Generate the shared mask `Crevice01` (Phase03 step 3.5): wear gated to recesses and patches.

A mask only GATES layers (never colour). Frozen mask contract (MasterSet.md):

    R = layer-2 coverage (TwoLayer only)  ·  G/B/A = where overlays 1/2/3 may appear

Crevice01 is for porous, recessed matter (fired clay, stone): damage (overlay 1) in broken
patches, deposits (overlay 2, e.g. dust) settling into a network of fine recesses, overlay 3
in broad soft patches. Scale `s01`, seamless (tileable.py), fixed seed.

    gen_crevice01.py [--out DIR]       # default: MatterLibrary/textures/shared/masks/

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
NAME = "Crevice01_s01.png"
SEED = 503


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the Crevice01 shared mask.")
    ap.add_argument("--out", default=str(ROOT / "MatterLibrary" / "textures" / "shared" / "masks"))
    args = ap.parse_args(argv)
    out = Path(args.out) / NAME
    if out.exists():
        print(f"refusing to overwrite {out} (Build Safety)", file=sys.stderr)
        return 1
    ridged = 1 - np.abs(tl.fbm((16, 32, 64), SEED) * 2 - 1)   # thin valleys -> crevice network
    img = tl.pack_mask(
        r=tl.fbm((8, 16), SEED + 1),                            # layer-2 coverage (unused off TwoLayer)
        g=np.clip((tl.fbm((6, 12, 24), SEED + 2) - 0.35) * 2.2, 0, 1),   # overlay 1: broken patches
        b=np.clip((ridged - 0.72) * 4.5, 0, 1),                 # overlay 2: into the recesses
        a=np.clip((tl.fbm((4, 8), SEED + 3) - 0.3) * 1.8, 0, 1),         # overlay 3: broad patches
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
