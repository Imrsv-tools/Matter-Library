#!/usr/bin/env python3
"""Units for the skin's shine maps (Phase22): the committed maps hold the rules their articles rely on.

    uv run tools/converters/fit/test_gen_skin_shine.py        exit 0 = PASS

* the roughness map is linear greyscale at hm08's map size;
* its average over the skin is the maker's SKIN_ROUGHNESS (0.62 since click 2, RD-P22-17; 0.5 at
  RD-P22-4) to within 1 %;
* outside every UV island it is exactly that average, so a mip blends no other offset in;
* the normal map (22.2) is RGB at the map size, decodes to unit vectors on the skin, and is exactly
  flat (128, 128, 255) beyond every island;
* the cavity map (22.2) is greyscale at the map size, never brightens (it only multiplies
  specular_weight down), and is exactly 255 beyond every island;
* the scatter map (22.3) is greyscale at the map size, exactly 0 (neutral) beyond every island,
  and raises only a small share of the skin (the thin parts), the ears most.
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
        if abs(avg - shine.SKIN_ROUGHNESS) > 0.005:
            fails.append(f"{p.name}: the skin's average is {avg:.4f}, not {shine.SKIN_ROUGHNESS} to within 1 %")
        grown = reg["islands"].copy()
        for _ in range(gsm.BLEED + 1):
            grown = grown | np.roll(grown, 1, 0) | np.roll(grown, -1, 0) | np.roll(grown, 1, 1) | np.roll(grown, -1, 1)
        off = m[~grown]
        if off.size and (off != shine.OUTSIDE).any():
            fails.append(f"{p.name}: {(off != shine.OUTSIDE).sum()} texels beyond every island are not "
                         f"the skin's average ({shine.OUTSIDE:.0f})")
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
    p = shine.OUT / shine.name("scatter")
    with Image.open(p) as im:
        ok = im.mode == "L" and im.size == (gsm.N, gsm.N)
        sc = np.asarray(im).astype(np.float64)
    if not ok:
        fails.append(f"{p.name}: want L {gsm.N} x {gsm.N}")
    else:
        off = sc[~grown]
        if off.size and (off != 0).any():
            fails.append(f"{p.name}: {(off != 0).sum()} texels beyond every island are not 0")
        raised = float((sc[reg["Body"]] > 12).mean())
        if raised > 0.15:
            fails.append(f"{p.name}: {raised:.0%} of the skin is raised; only the thin parts should be")
        ears = (gsm._grey("mpfb_ears.jpg") > 0.5) & reg["Body"]
        if (sc[ears] / 255.0).mean() < 0.4:
            fails.append(f"{p.name}: the ears average {(sc[ears] / 255.0).mean():.2f}; they are the thinnest part")
        print(f"scatter: {raised:.1%} of the skin raised, ears average {(sc[ears] / 255.0).mean():.2f}")
    for f in fails:
        print("FAIL", f)
    print("PASS" if not fails else f"{len(fails)} failed")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
