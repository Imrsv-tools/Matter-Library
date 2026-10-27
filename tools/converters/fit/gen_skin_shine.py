#!/usr/bin/env python3
"""Make the skin's SHINE MAPS for MakeHuman_Body_v01 (hm08): one shared set for all six tones.

    uv run tools/converters/fit/gen_skin_shine.py                 # every map, into the library
    uv run tools/converters/fit/gen_skin_shine.py --out /tmp/x    # a trial: nothing in the library

Phase22 *Skin Maps Beyond Colour* (RD-P22-1 … 10). Phase21's colour maps did not take away skin's
plastic look: the cause measured was the EVEN SHEEN (F-P21-1). These maps describe the surface, not
the tone, so one set serves every Fitzpatrick article (RD-P22-2). Each is LINEAR DATA on hm08's
atlas, read on the mesh's own UVs, and its neutral value draws today's skin (RD-P22-3):

* ``Skin_roughness_sUKN.png`` (22.1): an OFFSET around 0.5, added to the pores' roughness before
  the Creator's bias and the clamp, ``clamp(pores + (map - 0.5) + bias)`` (RD-P22-4). Oilier, so
  glossier, on the forehead, nose and chin; drier on the cheeks; a broad, gentle variation over the
  body; neutral on the lips (they keep their own finish, RD-P22-8). **Its average over the skin is
  held at 0.5**, so each article's measured roughness stays its average and only the spread moves.

**Made in 3D, not on the atlas** (the 2026-10-26 rule, ``SkinMaps.md``): every texel's position and
normal are rasterised from the mesh (``gen_synth_skin.rasterise``), the face's zones are placed from
hm08's own eye and jaw joints, and all noise is 3D, so nothing seams across a UV edge. The pinned
MPFB2 region masks the colour makers already read bound the face. CC0 parts only, no photograph and
no AI (RD-SKM-2); no relief at the genitals or groin (RD-SKM-4: this map is neutral there, as the
body's variation is a few hundredths). Provenance: ``library/provenance/sources/fit/makehuman/skin.yaml``.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gen_skin_maps as gsm  # noqa: E402
import gen_synth_skin as gss  # noqa: E402

OUT = gsm.OUT
TAG = gsm.TAG
PROVENANCE = gsm.PROVENANCE
SEED = 20261027
MAPS = ("roughness",)

# Roughness offsets (roughness units). The Physically Based skin value is 0.5 and the pores spread
# it 0.46 - 0.56; these move whole zones. Judgement, chosen to be seen in the look view, not fitted.
# First made at half these (T-zone -0.13, cheeks +0.07): the look view moved by a third of an 8-bit
# level on average, while a uniform -0.13 moved its highlights by up to 23 % (22.1.3's probe), so
# the renderer could show it and the map was too timid.
T_ZONE = -0.25         # forehead, nose, chin: the sebaceous zones, oilier
CHEEKS = +0.12         # drier
FACE_GRAIN = 0.06      # a 1.5 - 3 cm grain over the face, so the highlight breaks up
BODY_GRAIN = 0.025     # a 8 - 16 cm drift over the body
CHEST_BACK = -0.03     # the upper trunk's sebaceous zone


def name(kind: str) -> str:
    return f"Skin_{kind}_{TAG}.png"


def ellipse(P, cx: float, cy: float, rx: float, ry: float):
    """A soft zone on the face, seen from the front (x across, y up)."""
    return np.exp(-(((P[..., 0] - cx) / rx) ** 2 + ((P[..., 1] - cy) / ry) ** 2))


def roughness_offset(F: dict) -> tuple[np.ndarray, dict]:
    """The roughness offset over the atlas, before the average is held at 0."""
    P, Nr, J, masks, parts = F["P"], F["N"], F["J"], F["masks"], F["parts"]
    ye = float(J["l-eye"][1])                       # eye height (m); the eyes are 6.2 cm apart
    ex = float(J["l-eye"][0])
    chin_y = float(J["jaw"][1])
    front = np.clip((Nr[..., 2] - 0.1) / 0.4, 0.0, 1.0)      # facing forward
    face = np.clip(masks["face"] * 1.5, 0.0, 1.0) * front * (P[..., 1] > float(J["neck"][1]))
    forehead = ellipse(P, 0.0, ye + 0.050, 0.055, 0.028)
    nose = ellipse(P, 0.0, ye - 0.025, 0.014, 0.032)
    chin = ellipse(P, 0.0, chin_y - 0.004, 0.022, 0.016)
    tzone = np.maximum(np.maximum(forehead, nose), chin) * face
    cheeks = (ellipse(P, 1.55 * ex, ye - 0.032, 0.022, 0.022)
              + ellipse(P, -1.55 * ex, ye - 0.032, 0.022, 0.022)) * face
    grain = gss.fbm(P, (0.015, 0.03), (0.6, 0.4), SEED) * face
    drift = gss.fbm(P, (0.08, 0.16), (0.6, 0.4), SEED + 7)
    upper = np.clip((P[..., 1] - float(J["spine-2"][1])) / 0.15, 0.0, 1.0) * parts["trunk"]
    f = T_ZONE * tzone + CHEEKS * cheeks + FACE_GRAIN * grain + BODY_GRAIN * drift + CHEST_BACK * upper
    f = np.where(F["reg"]["Lips"], 0.0, f)          # the lips keep their own finish (RD-P22-8)
    zones = {"tzone": tzone > 0.5, "cheeks": cheeks > 0.5}
    return f, zones


def store(f: np.ndarray, F: dict) -> tuple[np.ndarray, dict]:
    """The offset -> an 8-bit linear map around 128, its average over the skin held at 0.5."""
    S, cover = F["reg"]["Body"], F["cover"]
    f = gsm.bleed(np.where(cover, f, 0.0)[..., None], cover, gsm.BLEED)[..., 0]
    grown = cover.copy()
    for _ in range(gsm.BLEED):
        grown = grown | np.roll(grown, 1, 0) | np.roll(grown, -1, 0) | np.roll(grown, 1, 1) | np.roll(grown, -1, 1)
    shift = -float(f[S].mean())
    for _ in range(4):                    # the clip and the 8 bits move the mean: settle it
        q = np.round(np.clip(0.5 + f + shift, 0.0, 1.0) * 255.0)
        q[~grown] = 128.0                  # beyond every island: neutral, so a mip blends nothing
        shift += 0.5 - float((q / 255.0)[S].mean())
    m = q.astype(np.uint8)
    dec = m / 255.0
    stats = {"skin_average": round(float(dec[S].mean()), 4),
             "skin_range": [round(float(np.percentile(dec[S], 1)), 3), round(float(np.percentile(dec[S], 99)), 3)],
             "uncovered_islands": int((F["reg"]["islands"] & ~grown).sum())}
    return m, stats


def write_provenance(rows: dict) -> None:
    """Add this maker's files and member rows to ``skin.yaml``, keeping every other row."""
    text = PROVENANCE.read_text(encoding="utf-8")
    lines = text.splitlines()
    files = [f"  - MatterLibrary/textures/fit/makehuman/skin/{name(k)}" for k in rows]
    members = [f"  Skin_{k}: {json.dumps(r, separators=(', ', ': '))}" for k, r in rows.items()]
    lines = [ln for ln in lines if ln not in files and not any(ln.startswith(f"  Skin_{k}:") for k in rows)]
    i = lines.index("provenance:")
    lines[i:i] = files
    lines += members
    out = "\n".join(lines) + "\n"
    out = re.sub(r"(  evidence: tools/converters/fit/gen_skin_maps\.py)(?:, tools/converters/fit/gen_skin_shine\.py)?",
                 r"\1, tools/converters/fit/gen_skin_shine.py", out)
    PROVENANCE.write_text(out, encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--out", type=Path, help="write the maps here instead (a trial: no provenance)")
    a = ap.parse_args(argv)
    F = gss.fields()
    rows = {}
    out = a.out or OUT
    out.mkdir(parents=True, exist_ok=True)
    f, zones = roughness_offset(F)
    m, st = store(f, F)
    dec = m / 255.0
    st |= {f"{z}_average": round(float(dec[sel & F['reg']['Body']].mean()), 4) for z, sel in zones.items()}
    p = out / name("roughness")
    Image.fromarray(m, "L").save(p, optimize=True)
    rows["roughness"] = {"made": "procedural", "space": "linear", "neutral": 0.5,
                         "rule": "roughness = clamp(pores + (map - 0.5) + roughness_bias)", **st}
    print(f"roughness: {p}\n  " + json.dumps(st))
    if st["uncovered_islands"]:
        raise SystemExit(f"roughness: {st['uncovered_islands']} island texels left unpainted")
    if abs(st["skin_average"] - 0.5) > 0.005:
        raise SystemExit(f"roughness: the skin's average is {st['skin_average']}, not 0.5")
    if not a.out:
        write_provenance(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
