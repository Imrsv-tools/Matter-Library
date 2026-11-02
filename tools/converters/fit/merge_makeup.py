#!/usr/bin/env python3
"""The REFERENCE MERGE: a makeup composition (a list of pieces) -> the skin's two makeup pictures.

    uv run tools/converters/fit/merge_makeup.py <composition.json> --out <dir>

Phase26 26.1 (RD-P26-4, RD-P26-5, RD-P26-6). Writes, at the mesh's map size (2048², RD-P26-9):

* ``makeup_color.png`` — RGBA: RGB the makeup's colour (sRGB-encoded), A its coverage (straight, not
  premultiplied; linear). The article's ``makeup_color_map`` (LCDSchema §Makeup layer).
* ``makeup_finish.png`` — RGB: R the finish's target roughness, G the finish's coverage, B 0; linear.
  The article's ``makeup_finish_map``.

It is the KNOWN ANSWER: the rig, the look view and the platform's own merge all read it, and a live
merge must produce the same pictures for the same list (RD-P26-4).

**A composition** stores no pixels (R-PSM-5) — the pieces' names and their settings::

    {"mesh": "MakeHuman_Body_v01",
     "pieces": [{"piece": "Makeup_LipColour_Full_v01", "colour": [0.45, 0.01, 0.02], "finish": 0.35},
                {"piece": "Makeup_Tattoo_Arrow_v01", "point": [0.29, 0.83, 0.04], "size": 0.04, "turn": 0}]}

``colour`` is LINEAR rec709; ``strength`` (0..1) scales the piece's coverage; ``finish`` is a target
roughness; each defaults to the piece record's. Pieces lay down in list order, each OVER the ones
before (straight-alpha "over", per picture). A piece carries colour, finish or both (its record's
``carries``): a clear gloss writes the finish picture only.

**A fitted piece** is a coverage shape already on the mesh's atlas (a greyscale PNG). **A placed
piece** is a square stamp (RGBA: RGB a colour multiplier, A coverage) of ``size`` metres, laid on the
rest-pose surface (RD-P26-6): centred on ``point``; turn 0 points the stamp's up along the body's +Y
projected onto the tangent plane at the point; ``turn`` (degrees) is clockwise about the outward
normal; a texel takes the stamp only where its rest-pose normal faces the point's (dot > 0) and it lies
within half the stamp's size of the tangent plane, so a stamp never prints through a limb or onto a
thigh beside the hand. A texel's stamp coordinate is its rest-pose position projected into that frame.
Positions are the body's rest pose in metres (``gen_synth_skin.fields``: hm08's ``base.obj`` / 10; x
to the body's left, y up, z forward).
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PIECES = REPO / "MatterLibrary" / "makeup"            # the piece records (RD-P26-5)
FILL_RADII = (2, 8, 32, 128)                          # colour pushed past each piece's edge (pixels)


def srgb_encode(c: np.ndarray) -> np.ndarray:
    c = np.clip(c, 0.0, 1.0)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def srgb_decode(c: np.ndarray) -> np.ndarray:
    return np.where(c <= 0.04045, c / 12.92, np.power((c + 0.055) / 1.055, 2.4))


def read_piece(name: str, root: Path = PIECES) -> dict:
    """The piece record, its pictures resolved from the record's own folder."""
    p = root / f"{name}.json"
    if not p.is_file():
        raise SystemExit(f"no piece record {p}")
    rec = json.loads(p.read_text(encoding="utf-8"))
    for k in ("coverage", "stamp"):
        if k in rec:
            rec[k] = (p.parent / rec[k]).resolve()
    return rec


def tangent_frame(n: np.ndarray, turn_deg: float) -> tuple[np.ndarray, np.ndarray]:
    """(right, up) at a point with outward normal ``n``: up is the body's +Y projected onto the tangent
    plane, turned clockwise by ``turn_deg`` about ``n`` (seen from outside); right = up x n."""
    n = n / np.linalg.norm(n)
    y = np.array([0.0, 1.0, 0.0])
    up = y - n * float(n @ y)
    if np.linalg.norm(up) < 1e-6:                     # the normal is +-Y: fall back to the body's -Z
        z = np.array([0.0, 0.0, -1.0])
        up = z - n * float(n @ z)
    up /= np.linalg.norm(up)
    t = math.radians(-turn_deg)                       # clockwise about n = a negative right-hand turn
    up = up * math.cos(t) + np.cross(n, up) * math.sin(t)
    right = np.cross(up, n)
    return right, up


def nearest_surface(point, P: np.ndarray, Nrm: np.ndarray, cover: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """The covered texel nearest ``point``: its position and normal (the stamp's centre and frame)."""
    idx = np.flatnonzero(cover.ravel())
    d = np.linalg.norm(P.reshape(-1, 3)[idx] - np.asarray(point, float), axis=1)
    i = idx[int(np.argmin(d))]
    return P.reshape(-1, 3)[i], Nrm.reshape(-1, 3)[i]


def bilinear(img: np.ndarray, s: np.ndarray, t: np.ndarray) -> np.ndarray:
    """Sample ``img`` (H, W, C; row 0 the top, t = 1) at (s, t) in 0..1, clamped at the edges."""
    h, w = img.shape[:2]
    x = np.clip(s * w - 0.5, 0, w - 1)
    y = np.clip((1.0 - t) * h - 0.5, 0, h - 1)
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    x1, y1 = np.minimum(x0 + 1, w - 1), np.minimum(y0 + 1, h - 1)
    fx, fy = (x - x0)[..., None], (y - y0)[..., None]
    top = img[y0, x0] * (1 - fx) + img[y0, x1] * fx
    bot = img[y1, x0] * (1 - fx) + img[y1, x1] * fx
    return top * (1 - fy) + bot * fy


def stamp_coverage(rec: dict, piece: dict, P, Nrm, cover) -> tuple[np.ndarray, np.ndarray]:
    """A placed piece on the atlas: (coverage (N, N), colour multiplier (N, N, 3), linear)."""
    size = float(piece.get("size", rec.get("size")))
    centre, n = nearest_surface(piece["point"], P, Nrm, cover)
    n = n / np.linalg.norm(n)
    right, up = tangent_frame(n, float(piece.get("turn", 0.0)))
    d = P - centre
    s = d @ right / size + 0.5
    t = d @ up / size + 0.5
    h = d @ n
    inside = (cover & (s >= 0) & (s <= 1) & (t >= 0) & (t <= 1) & ((Nrm @ n) > 0) & (np.abs(h) < size / 2))
    rgba = np.asarray(Image.open(rec["stamp"]).convert("RGBA"), dtype=np.float64) / 255.0
    cov = np.zeros(P.shape[:2])
    mult = np.ones(P.shape[:2] + (3,))
    if inside.any():
        smp = bilinear(rgba, s[inside], t[inside])
        cov[inside] = smp[:, 3]
        mult[inside] = srgb_decode(smp[:, :3])
    return cov, mult


def fitted_coverage(rec: dict, shape: tuple) -> np.ndarray:
    img = Image.open(rec["coverage"]).convert("L")
    if img.size != (shape[1], shape[0]):
        raise SystemExit(f"{rec['name']}: its coverage is {img.size}, the atlas is {shape[1]} x {shape[0]}")
    return np.asarray(img, dtype=np.float64) / 255.0


def merge(pieces: list[dict], P: np.ndarray, Nrm: np.ndarray, cover: np.ndarray,
          root: Path = PIECES) -> tuple[np.ndarray, np.ndarray]:
    """The composition's two layers, straight alpha, linear: colour (N, N, 4) and finish (N, N, 2)."""
    shape = P.shape[:2]
    col, a_col = np.zeros(shape + (3,)), np.zeros(shape)
    rough, a_fin = np.zeros(shape), np.zeros(shape)
    for piece in pieces:
        rec = read_piece(piece["piece"], root)
        if rec["kind"] == "fitted":
            c, mult = fitted_coverage(rec, shape), np.ones(shape + (3,))
        elif rec["kind"] == "placed":
            c, mult = stamp_coverage(rec, piece, P, Nrm, cover)
        else:
            raise SystemExit(f"{rec['name']}: unknown kind {rec['kind']!r}")
        c = np.clip(c * float(piece.get("strength", rec["defaults"].get("strength", 1.0))), 0.0, 1.0)
        carries = rec["carries"]
        if "colour" in carries:
            rgb = np.asarray(piece.get("colour", rec["defaults"]["colour"]), float) * mult
            a_new = c + a_col * (1 - c)
            safe = np.maximum(a_new, 1e-12)[..., None]
            col = (rgb * c[..., None] + col * (a_col * (1 - c))[..., None]) / safe
            a_col = a_new
        if "finish" in carries:
            r = float(piece.get("finish", rec["defaults"]["finish"]))
            a_new = c + a_fin * (1 - c)
            rough = (r * c + rough * a_fin * (1 - c)) / np.maximum(a_new, 1e-12)
            a_fin = a_new
    col = _fill(col, a_col)
    rough = _fill(rough[..., None], a_fin)[..., 0]
    return np.concatenate([col, a_col[..., None]], -1), np.stack([rough, a_fin], -1)


def _box(x: np.ndarray, r: int) -> np.ndarray:
    """A box blur of radius r over the first two axes (summed-area table)."""
    pad = np.pad(x, ((r + 1, r), (r + 1, r)) + ((0, 0),) * (x.ndim - 2), mode="edge")
    s = pad.cumsum(0).cumsum(1)
    n = 2 * r + 1
    return (s[n:, n:] - s[:-n, n:] - s[n:, :-n] + s[:-n, :-n]) / (n * n)


def _fill(v: np.ndarray, a: np.ndarray) -> np.ndarray:
    """Push each layer's value past its edge where coverage is 0, so a filtered lookup at the edge
    blends the piece's own colour toward coverage 0 and never toward black (straight alpha)."""
    out, have = v.copy(), a > 1e-4
    for r in FILL_RADII:
        num, den = _box(v * a[..., None], r), _box(a, r)[..., None]
        reach = (~have) & (den[..., 0] > 1e-6)
        out[reach] = (num / np.maximum(den, 1e-12))[reach]
        have = have | reach
    return out


def write(colour: np.ndarray, finish: np.ndarray, out: Path) -> tuple[Path, Path]:
    out.mkdir(parents=True, exist_ok=True)
    rgba = np.concatenate([srgb_encode(colour[..., :3]), colour[..., 3:]], -1)
    pc, pf = out / "makeup_color.png", out / "makeup_finish.png"
    Image.fromarray(np.round(rgba * 255).astype(np.uint8), "RGBA").save(pc, optimize=True)
    fin = np.concatenate([finish, np.zeros(finish.shape[:2] + (1,))], -1)
    Image.fromarray(np.round(np.clip(fin, 0, 1) * 255).astype(np.uint8), "RGB").save(pf, optimize=True)
    return pc, pf


def body_fields():
    """The mesh's per-texel rest-pose position, normal and coverage (gen_synth_skin.fields' own)."""
    sys.path.insert(0, str(HERE))
    import gen_synth_skin as gss  # noqa: PLC0415 (heavy: rasterises the mesh)
    F = gss.fields(parts=False)
    return F["P"], F["N"], F["cover"]


def run(composition: Path, out: Path) -> tuple[Path, Path]:
    """Merge ``composition`` on the body and write its two pictures into ``out`` (the rig's and the
    look view's ``--makeup``)."""
    comp = json.loads(Path(composition).read_text(encoding="utf-8"))
    if comp.get("mesh", "MakeHuman_Body_v01") != "MakeHuman_Body_v01":
        raise SystemExit("the reference merge knows MakeHuman_Body_v01 only")
    P, Nrm, cover = body_fields()
    return write(*merge(comp["pieces"], P, Nrm, cover), Path(out))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("composition", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    a = ap.parse_args(argv)
    comp = json.loads(a.composition.read_text(encoding="utf-8"))
    if comp.get("mesh", "MakeHuman_Body_v01") != "MakeHuman_Body_v01":
        raise SystemExit("the reference merge knows MakeHuman_Body_v01 only")
    P, Nrm, cover = body_fields()
    colour, finish = merge(comp["pieces"], P, Nrm, cover)
    pc, pf = write(colour, finish, a.out)
    print(f"makeup colour {pc}  covered texels {int((colour[..., 3] > 0).sum())}\n"
          f"makeup finish {pf}  covered texels {int((finish[..., 1] > 0).sum())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
