#!/usr/bin/env python3
"""Units for the skin's shine maps (Phase22): the committed maps hold the rules their articles rely on.

    uv run tools/converters/fit/test_gen_skin_shine.py        exit 0 = PASS

* the roughness map is linear greyscale at hm08's map size;
* its average over the skin is 0.5 to within 1 %, so every article keeps its measured roughness on
  average (RD-P22-4);
* outside every UV island it is exactly neutral (128), so a mip blends no offset in;
* the normal map (22.2) is RGB at the map size, decodes to unit vectors on the skin, and is exactly
  flat (128, 128, 255) beyond every island;
* the cavity map (22.2) is greyscale at the map size, never brightens (it only multiplies
  specular_weight down), and is exactly 255 beyond every island.
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gen_skin_maps as gsm  # noqa: E402
import gen_skin_shine as shine  # noqa: E402


def main() -> int:
    fails = []
    reg = gsm.regions()
    p = shine.OUT / shine.name("roughness")
    with Image.open(p) as im:
        if im.mode != "L" or im.size != (gsm.N, gsm.N):
            fails.append(f"{p.name} is {im.mode} {im.size}: want L {gsm.N} x {gsm.N}")
        m = np.asarray(im).astype(np.float64)
    if not fails:
        avg = float((m / 255.0)[reg["Body"]].mean())
        if abs(avg - 0.5) > 0.005:
            fails.append(f"{p.name}: the skin's average is {avg:.4f}, not 0.5 to within 1 %")
        grown = reg["islands"].copy()
        for _ in range(gsm.BLEED + 1):
            grown = grown | np.roll(grown, 1, 0) | np.roll(grown, -1, 0) | np.roll(grown, 1, 1) | np.roll(grown, -1, 1)
        off = m[~grown]
        if off.size and (off != 128).any():
            fails.append(f"{p.name}: {(off != 128).sum()} texels beyond every island are not neutral (128)")
        print(f"roughness: skin average {avg:.4f}, range {m[reg['Body']].min():.0f}..{m[reg['Body']].max():.0f}")
    grown = reg["islands"].copy()
    for _ in range(gsm.BLEED + 1):
        grown = grown | np.roll(grown, 1, 0) | np.roll(grown, -1, 0) | np.roll(grown, 1, 1) | np.roll(grown, -1, 1)
    p = shine.OUT / shine.name("normal")
    with Image.open(p) as im:
        ok = im.mode == "RGB" and im.size == (gsm.N, gsm.N)
        n = np.asarray(im).astype(np.float64)
    if not ok:
        fails.append(f"{p.name}: want RGB {gsm.N} x {gsm.N}")
    else:
        dec = n / 255.0 * 2 - 1
        err = np.abs(np.linalg.norm(dec[reg["Body"]], axis=-1) - 1)
        if err.max() > 0.02:
            fails.append(f"{p.name}: a skin texel decodes {err.max():.3f} off unit length")
        off = n[~grown]
        if off.size and (off != (128, 128, 255)).any(axis=-1).any():
            fails.append(f"{p.name}: {(off != (128, 128, 255)).any(axis=-1).sum()} texels beyond every island are not flat")
        print(f"normal: unit error max {err.max():.4f}")
    p = shine.OUT / shine.name("cavity")
    with Image.open(p) as im:
        ok = im.mode == "L" and im.size == (gsm.N, gsm.N)
        c = np.asarray(im).astype(np.float64)
    if not ok:
        fails.append(f"{p.name}: want L {gsm.N} x {gsm.N}")
    else:
        off = c[~grown]
        if off.size and (off != 255).any():
            fails.append(f"{p.name}: {(off != 255).sum()} texels beyond every island are not 1")
        print(f"cavity: skin average {(c / 255.0)[reg['Body']].mean():.4f}")
    for f in fails:
        print("FAIL", f)
    print("PASS" if not fails else f"{len(fails)} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
