#!/usr/bin/env python3
"""Generate the base texture set `PowderCoat_Textured` (lane L2).

Fine-texture powder coat: a polyester powder sprayed onto metal and baked into one
continuous pigmented film, the finish of architectural panels, railings, window frames and
enclosures. The "fine texture" grade cures with a dense, even field of small rounded bumps,
a few tenths of a millimetre across, like a very fine sandpaper under paint. It is matte to
satin and hides fingerprints and small dents, which is why it is used on large surfaces.

Authored WHITE, so a Creator's tint gives any colour. Physically Based has no powder coat
or white paint-film entry that fits, so the colour is a judgement: a neutral white of
linear albedo 0.82, an architectural white (light reflectance about 84 to 87) less the few
percent the surface reflects. The texture's mean albedo is that value exactly.

BUILT TO STAY EVEN ON LARGE PANELS. The tile is 1 cm and carries nothing slower than the
bumps themselves, so there is no mottle to repeat: from a metre away the bumps are below a
pixel and the panel reads as one even satin. The satin itself is in the roughness (a mean
of 0.55), not left to the bumps, so the finish holds at any distance.

Writes MatterLibrary/textures/base/synthetic/coating/PowderCoat_Textured_<channel>_s001.png:
basecolor (sRGB-encoded), roughness and normal (linear data, NormalGL). Seamless
(tileable.py), fixed seed, no network.

    gen_powdercoat_textured.py [--out DIR]

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
OUT = ROOT / "MatterLibrary" / "textures" / "base" / "synthetic" / "coating"
SET = "PowderCoat_Textured"
SCALE = "s001"
SEED = 9016
WHITE = np.array([0.82, 0.82, 0.82])   # judgement: an architectural white, linear sRGB
ROUGH_MEAN = 0.55                      # judgement: a fine-texture grade is matte to satin


def maps() -> dict:
    # On a 1 cm tile one pixel is about 10 micrometres.
    # The texture: a dense, even field of rounded bumps, 0.21, 0.15 and 0.10 mm across.
    bumps = (tl.noise(47, SEED) + 0.8 * tl.noise(67, SEED + 1) + 0.5 * tl.noise(97, SEED + 2)) / 2.3
    micro = tl.fbm((173, 347), SEED + 10)            # the film's own fine orange peel
    # Round the crowns and the hollows alike: a smooth S-curve about the middle.
    relief = np.clip((bumps - 0.5) * 2.2 + 0.5, 0, 1)
    relief = relief * relief * (3 - 2 * relief)

    shade = 1.0 + 0.015 * (relief - relief.mean()) + 0.01 * (micro - 0.5)
    albedo = WHITE[None, None, :] * shade[..., None]
    albedo *= WHITE / albedo.reshape(-1, 3).mean(0)             # the MEAN is the stated white exactly

    rough = 0.08 * (0.5 - relief) + 0.04 * (micro - 0.5)        # bump crowns cure a little smoother
    rough = np.clip(rough - rough.mean() + ROUGH_MEAN, 0, 1)

    height = 1.0 * relief + 0.08 * micro
    return {"basecolor": tl.rgb(tl.linear_to_srgb(albedo)),
            "roughness": tl.gray(rough),
            "normal": tl.normal_map(height, strength=4.0)}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate the PowderCoat_Textured base texture set.")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args(argv)
    out = Path(args.out)
    targets = {ch: out / f"{SET}_{ch}_{SCALE}.png" for ch in ("basecolor", "roughness", "normal")}
    if any(p.exists() for p in targets.values()):
        print(f"refusing to overwrite {SET} in {out} (Build Safety); use --out <dir>", file=sys.stderr)
        return 1
    out.mkdir(parents=True, exist_ok=True)
    for ch, img in maps().items():
        img.save(targets[ch], "PNG", optimize=True)
        print(f"wrote {targets[ch]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
