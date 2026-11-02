#!/usr/bin/env python3
"""Units for the reference merge (Phase26 RD-P26-4 … 6), on a small synthetic body.

    uv run tools/converters/fit/test_merge_makeup.py        exit 0 = PASS

The body is two plates 2 cm apart, each half of a 64² atlas: a FRONT plate facing +Z and, behind it,
a BACK plate facing -Z (the far side of a limb). A placed stamp on the front plate:

* covers the texel at its point, and nothing on the back plate, though the back lies inside the
  stamp's square;
* points the stamp's up along +Y at turn 0, and along +X at turn 90 (clockwise seen from the front,
  the viewer's right);
* spans its size: a full-coverage stamp 1 cm across covers 1 cm of the plate, not more.

A fitted piece's coverage equals its picture; a finish-only piece leaves the colour picture empty;
two pieces lay down in order, the second over the first.
"""
import json
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import merge_makeup as mm  # noqa: E402

N = 64
TEXEL = 0.001          # 1 mm a texel


def body():
    """Columns 0..31: the front plate (z = 0, facing +Z); 32..63: the back plate (z = -0.02, facing -Z).
    x = the column's metres within its plate, y = up the image (row 0 is the top)."""
    P, Nr = np.zeros((N, N, 3)), np.zeros((N, N, 3))
    rows, cols = np.mgrid[0:N, 0:N]
    half = cols % (N // 2)
    P[..., 0] = (half - 15.5) * TEXEL
    P[..., 1] = (N / 2 - 0.5 - rows) * TEXEL
    front = cols < N // 2
    P[..., 2] = np.where(front, 0.0, -0.02)
    Nr[..., 2] = np.where(front, 1.0, -1.0)
    return P, Nr, np.ones((N, N), bool), front


def write_pieces(root: Path):
    # a stamp whose top half is covered and bottom half clear: its "up" shows where it points
    st = np.zeros((32, 32, 4), np.uint8)
    st[..., :3] = 255
    st[:16, :, 3] = 255
    Image.fromarray(st, "RGBA").save(root / "half.png")
    full = st.copy()
    full[..., 3] = 255
    Image.fromarray(full, "RGBA").save(root / "full.png")
    fit = np.zeros((N, N), np.uint8)
    fit[10:20, 40:50] = 200
    Image.fromarray(fit, "L").save(root / "fit.png")
    recs = {"Half": {"kind": "placed", "stamp": "half.png", "carries": ["colour"],
                     "defaults": {"colour": [1.0, 0.0, 0.0], "strength": 1.0}},
            "Full": {"kind": "placed", "stamp": "full.png", "carries": ["colour"],
                     "defaults": {"colour": [0.0, 0.0, 1.0], "strength": 1.0}},
            "Fit": {"kind": "fitted", "coverage": "fit.png", "carries": ["colour", "finish"],
                    "defaults": {"colour": [0.0, 1.0, 0.0], "strength": 1.0, "finish": 0.2}},
            "Gloss": {"kind": "fitted", "coverage": "fit.png", "carries": ["finish"],
                      "defaults": {"strength": 1.0, "finish": 0.1}}}
    for name, r in recs.items():
        (root / f"{name}.json").write_text(json.dumps({"name": name} | r), encoding="utf-8")


def main() -> int:
    fails = []

    def check(ok, what):
        print(("PASS " if ok else "FAIL ") + what)
        if not ok:
            fails.append(what)

    P, Nr, cover, front = body()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        write_pieces(root)

        col, _ = mm.merge([{"piece": "Full", "point": [0.0, 0.0, 0.0], "size": 0.01}], P, Nr, cover, root)
        a = col[..., 3]
        r0, c0 = np.unravel_index(np.argmin(np.linalg.norm(P, axis=-1) + (~front) * 9), (N, N))
        check(a[r0, c0] > 0.99, "a placed stamp covers the texel at its point")
        check(a[~front].max() == 0.0, "nothing prints on the far side of the limb (normals facing away)")
        span = (a[r0] > 0.5).sum()
        check(9 <= span <= 11, f"a 1 cm stamp spans 1 cm of a 1 mm/texel plate ({span} texels)")
        check(np.allclose(col[a > 0.99][:, :3], [0, 0, 1]), "its colour is the piece's (linear, x white)")

        def centroid(turn):
            c, _ = mm.merge([{"piece": "Half", "point": [0.0, 0.0, 0.0], "size": 0.02, "turn": turn}],
                            P, Nr, cover, root)
            m = (c[..., 3] > 0.5) & front
            return P[m].mean(0)
        up0, up90 = centroid(0), centroid(90)
        check(up0[1] > 0.003 and abs(up0[0]) < 0.001, f"turn 0: the stamp's top is up the body (+Y) {up0[:2]}")
        check(up90[0] > 0.003 and abs(up90[1]) < 0.001,
              f"turn 90: clockwise seen from outside, its top points to the viewer's right, +X here {up90[:2]}")

        col, fin = mm.merge([{"piece": "Fit"}], P, Nr, cover, root)
        pic = np.asarray(Image.open(root / "fit.png"), dtype=np.float64) / 255.0
        check(np.allclose(col[..., 3], pic) and np.allclose(fin[..., 1], pic),
              "a fitted piece's colour and finish coverage equal its picture")
        check(np.allclose(fin[..., 0][pic > 0], 0.2), "the finish carries the piece's target roughness")

        col, fin = mm.merge([{"piece": "Gloss"}], P, Nr, cover, root)
        check(col[..., 3].max() == 0.0 and fin[..., 1].max() > 0.7, "a finish-only piece writes no colour")

        col, _ = mm.merge([{"piece": "Fit"}, {"piece": "Fit", "colour": [1.0, 0.0, 0.0], "strength": 0.5}],
                          P, Nr, cover, root)
        c = col[15, 45]
        a1 = 200 / 255
        a2 = a1 * 0.5
        want_a = a2 + a1 * (1 - a2)
        want_r = a2 / want_a
        check(abs(c[3] - want_a) < 1e-6 and abs(c[0] - want_r) < 1e-6,
              f"the second piece lays OVER the first (straight 'over': A {c[3]:.4f}, R {c[0]:.4f})")

        out = root / "out"
        mm.write(*mm.merge([{"piece": "Fit"}], P, Nr, cover, root), out)
        im = Image.open(out / "makeup_color.png")
        check(im.mode == "RGBA" and im.size == (N, N), "the colour picture is RGBA at the atlas size")
        px = np.asarray(im)[15, 45]
        check(px[3] == 200 and px[1] == 255, "its A is the coverage as stored, its RGB the sRGB-encoded colour")

    print("PASS" if not fails else f"FAIL ({len(fails)})")
    return 0 if not fails else 1


if __name__ == "__main__":
    raise SystemExit(main())
