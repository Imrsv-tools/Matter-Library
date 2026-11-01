#!/usr/bin/env python3
"""The scanned bar's pictures for the look view's column A, made locally (Phase24 24.1, RD-P24-5).

    uv run --with OpenEXR tools/parity/bar_maps.py --colour <8K picture> --diffuse <exr>
        --specular <exr> [--scatter <exr>] [--out library/parity/P24_Bar]

The bar is a research reference made from a scanned person: it never enters the tree, and its
paths are never written in a tracked file (RD-SKM-2, RD-P23-10). Everything this writes goes under
``--out``, which must be inside the git-ignored ``library/parity/``. ``OpenEXR`` is not a project
dependency: it is needed only for a picture that never ships, so it rides ``--with``.

Inputs, all on hm08's atlas, square, a multiple of the library's 2048:
* ``--colour``: the full-body colour picture (sRGB): the scan's head, and the body colour-matched
  to it at the neck. Its absolute level is not trusted (it was composed against another skin).
* ``--diffuse``: the head's albedo as float, its values sRGB-ENCODED (decoded here). Zero where the
  scan has no data (the body). Its mean over the head's skin, lips excluded, is **the bar's tone**
  (RD-P24-1), and the colour picture is scaled to it.
* ``--specular``: the head's specular map (grey). Drawn as the article's **cavity map**, which
  multiplies the shine as a specular map does: the stored values over their 99.5th percentile on
  the head's skin, the body keeping the library's shared cavity map. Read as data, not decoded.
* ``--scatter``: measured and reported only; it maps onto no input this phase draws.

Writes ``basecolor.png`` (8-bit sRGB, the colour over its 99.9th percentile) and ``cavity.png``
(8-bit linear grey) at the inputs' size, and ``bar.json``: the article constant that renders the
colour exactly, the tone, and the measurements. ``look.py --bar <out>`` draws them.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path.insert(0, str(REPO / "tools" / "converters" / "fit"))
sys.path.insert(0, str(REPO / "tools" / "converters"))
import gen_skin_maps as gsm  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
PARITY = REPO / "library" / "parity"
SHARED_CAVITY = REPO / "MatterLibrary" / "textures" / "fit" / "makehuman" / "skin" / "Skin_cavity_sUKN.png"


def exr(path: Path) -> np.ndarray:
    import OpenEXR  # noqa: PLC0415 (only here: uv run --with OpenEXR)
    ch = OpenEXR.File(str(path)).channels()
    a = next(iter(ch.values())).pixels if len(ch) == 1 else np.stack([ch[c].pixels for c in "RGB"], -1)
    return np.asarray(a, dtype=np.float32)


def up(mask: np.ndarray, f: int) -> np.ndarray:
    return np.repeat(np.repeat(mask, f, 0), f, 1)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--colour", type=Path, required=True)
    ap.add_argument("--diffuse", type=Path, required=True)
    ap.add_argument("--specular", type=Path, required=True)
    ap.add_argument("--scatter", type=Path)
    ap.add_argument("--out", type=Path, default=PARITY / "P24_Bar")
    a = ap.parse_args(argv)
    out = a.out.resolve()
    if PARITY.resolve() not in out.parents and out != PARITY.resolve():
        raise SystemExit(f"--out must be inside {PARITY} (git-ignored): the bar never enters the tree")
    out.mkdir(parents=True, exist_ok=True)

    im = Image.open(a.colour).convert("RGB")
    n = im.size[0]
    if im.size[0] != im.size[1] or n % gsm.N:
        raise SystemExit(f"--colour is {im.size}: square, a multiple of {gsm.N}")
    f = n // gsm.N
    reg = gsm.regions()
    body, islands = up(reg["Body"], f), up(reg["islands"], f)

    diffuse = exr(a.diffuse)[..., :3]
    if diffuse.shape[:2] != (n, n):
        raise SystemExit(f"--diffuse is {diffuse.shape[:2]}, --colour {n}: one size")
    head = diffuse.max(-1) > 0
    face = head & body                                   # the head's skin, the lips excluded
    tone = gsm._srgb_to_linear(diffuse[face].astype(np.float64)).mean(0)
    del diffuse

    col = gsm._srgb_to_linear(np.asarray(im, dtype=np.float32) / np.float32(255.0)).astype(np.float32)
    del im
    s = tone / col[face].mean(0, dtype=np.float64)     # float64: a float32 sum over 16M texels drifts ~7 %
    col *= s.astype(np.float32)
    k = np.maximum(np.percentile(col[islands], 99.9, axis=0), 1e-6)
    srgb8 = np.round(gsm._linear_to_srgb(np.clip(col / k.astype(np.float32), 0.0, 1.0)) * 255.0).astype(np.uint8)
    Image.fromarray(srgb8, "RGB").save(out / "basecolor.png")
    dec = gsm._srgb_to_linear(srgb8[face].astype(np.float64) / 255.0) * k
    del srgb8, col

    spec = exr(a.specular)[..., 0]
    sk = float(np.percentile(spec[face], 99.5))
    cav = np.clip(spec / sk, 0.0, 1.0)
    shared = np.asarray(Image.open(SHARED_CAVITY).convert("L"), dtype=np.float32) / 255.0
    cav = np.where(head, cav, up(shared, f))
    Image.fromarray(np.round(cav * 255.0).astype(np.uint8), "L").save(out / "cavity.png")
    rec = {"size": n, "tone": tone.round(4).tolist(), "red_blue": round(float(tone[0] / tone[2]), 3),
           "base_color_const": k.round(4).tolist(), "colour_scale": s.round(4).tolist(),
           "rendered_face_mean": dec.mean(0).round(4).tolist(), "head_share": round(float(head.mean()), 4),
           "cavity": {"specular_p99_5": round(sk, 4), "face_mean": round(float(cav[face].mean(dtype=np.float64)), 4),
                      "body_mean": round(float(cav[body & ~head].mean(dtype=np.float64)), 4)}}
    del spec, cav
    if a.scatter:
        sc = exr(a.scatter)[..., 0][face]
        rec["scatter"] = {"face_p1_p50_p99": np.percentile(sc, [1, 50, 99]).round(4).tolist()}
    (out / "bar.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(rec))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
