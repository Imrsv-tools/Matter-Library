#!/usr/bin/env python3
"""Make the library's makeup PIECES for MakeHuman_Body_v01: their records and pictures.

    uv run tools/converters/fit/gen_makeup_pieces.py

Phase26 (RD-P26-5, RD-P26-7). A piece is one bit of makeup or one mark the reference merge
(``merge_makeup.py``) lays on the skin. Each has a record, ``MatterLibrary/makeup/<Name>.json``, and
its picture under ``MatterLibrary/textures/fit/makehuman/makeup/``:

* **fitted** — a coverage shape on the mesh's atlas (a greyscale PNG at the mesh's map size), made
  from the body in 3D and baked per layout;
* **placed** — a square stamp (RGBA: RGB a colour multiplier, white for a one-colour piece; A
  coverage) and its size in metres, laid on the body where a composition says.

Every record carries its controls' defaults (colour, linear rec709; strength; finish, a target
roughness), what it carries (colour, finish or both), and the channels the format keeps for later,
marked planned: relief (RD-P26-1) and pigment (Skin Layers). Procedural only, CC0: no photograph, no
scan, no AI (RD-SKM-2, RD-RO-2). It also writes the first look's composition (26.1's fixtures):
``tools/parity/makeup/red_lips_hand_tattoo.json``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gen_skin_maps as gsm  # noqa: E402
import gen_synth_skin as gss  # noqa: E402

REPO = HERE.parents[2]
RECORDS = REPO / "MatterLibrary" / "makeup"
PICTURES = REPO / "MatterLibrary" / "textures" / "fit" / "makehuman" / "makeup"
LOOKS = REPO / "tools" / "parity" / "makeup"
TAG = "sUKN"
PLANNED = {"relief": "planned (RD-P26-1, Skin Layers)", "pigment": "planned (Skin Layers)"}
STAMP = 512


def record(name: str, kind: str, carries: list, defaults: dict, summary: str, **extra) -> dict:
    return {"name": name, "kind": kind, "fits": "MakeHuman_Body_v01" if kind == "fitted" else None,
            "carries": carries, "defaults": defaults, "channels_planned": PLANNED, "summary": summary,
            "contributor": "MatterBot", "licence": "CC0-1.0", "origin": ["procedural", "agent-drafted"],
            "script": "tools/converters/fit/gen_makeup_pieces.py"} | extra


def save_record(rec: dict) -> Path:
    rec = {k: v for k, v in rec.items() if v is not None}
    p = RECORDS / f"{rec['name']}.json"
    p.write_text(json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    return p


def rel(p: Path) -> str:
    return Path("..", *p.relative_to(REPO / "MatterLibrary").parts).as_posix()


def save_grey(cov: np.ndarray, name: str) -> Path:
    p = PICTURES / f"{name}_coverage_{TAG}.png"
    Image.fromarray(np.round(np.clip(cov, 0, 1) * 255).astype(np.uint8), "L").save(p, optimize=True)
    return p


# ------------------------------------------------------------------ the pieces ---------------
def lip_colour(F: dict) -> dict:
    """The lips' vermilion, the body's own lip region, its border softened ~1 mm (2 texels at the
    face's ~0.47 mm a texel): full coverage on the lips, none past them. The region is a JPEG, whose
    faint ringing would print stray specks of colour across the atlas: below 0.1 is none."""
    m = gsm.blur(F["masks"]["lips"], 2)
    cov = np.clip((m - 0.1) / 0.6, 0, 1) * F["cover"]
    p = save_grey(cov, "Makeup_LipColour_Full_v01")
    return record("Makeup_LipColour_Full_v01", "fitted", ["colour", "finish"],
                  {"colour": [0.477, 0.007, 0.013], "strength": 1.0, "finish": 0.35},
                  "Lip colour over the whole lips: a red lipstick by default, satin.", coverage=rel(p))


def arrow_stamp() -> Image.Image:
    """An asymmetric arrow, white on clear, pointing up the stamp: its head has one barb, on the
    stamp's right, so a mirrored or turned stamp is seen at once. Drawn at 4x and box-filtered."""
    s = 4 * STAMP
    im = Image.new("L", (s, s), 0)
    d = ImageDraw.Draw(im)
    cx, w = s // 2, int(0.075 * s)
    top, bottom, head = int(0.03 * s), int(0.97 * s), int(0.33 * s)
    d.rectangle([cx - w // 2, head - 4, cx + w // 2, bottom], fill=255)                 # the shaft
    d.polygon([(cx - w // 2, top), (cx + int(0.30 * s), head), (cx - w // 2, head)], fill=255)  # one barb
    d.ellipse([cx - int(0.13 * s), bottom - int(0.10 * s), cx - w // 2, bottom], fill=255)  # a tail dot, left
    a = np.asarray(im, dtype=np.float64).reshape(STAMP, 4, STAMP, 4).mean(axis=(1, 3))
    rgba = np.zeros((STAMP, STAMP, 4), np.uint8)
    rgba[..., :3] = 255
    rgba[..., 3] = np.round(a).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def tattoo() -> dict:
    p = PICTURES / f"Makeup_Tattoo_Arrow_v01_stamp_{TAG}.png"
    arrow_stamp().save(p, optimize=True)
    return record("Makeup_Tattoo_Arrow_v01", "placed", ["colour"],
                  {"colour": [0.02, 0.02, 0.022], "strength": 1.0}, "A small black-ink arrow tattoo, "
                  "placed anywhere on the body; its head has one barb, so its turn reads.",
                  stamp=rel(p), size=0.042)


def back_of_left_hand(F: dict) -> list[float]:
    """The back of the left hand, between the wrist and the knuckles, on the rest pose: the look
    view's hand target (the hand's box centre, ``look.look_views``) moved 2 cm toward the knuckles, then
    the covered texel nearest that point on the side the hand view looks at."""
    P, Nr, cover = F["P"], F["N"], F["cover"]
    xmax = P[..., 0][cover].max()
    hand = cover & (P[..., 0] > xmax - 0.12)
    pts = P[hand]
    # 2 cm toward the knuckles: at 1.5 cm up, the first render put the arrow on the wrist's edge
    hc = (pts.min(0) + pts.max(0)) / 2 + np.array([0.0, -0.02, 0.0])
    d = np.array([0.15, 0.30, 1.0]) / np.linalg.norm([0.15, 0.30, 1.0])
    facing = hand & ((Nr @ d) > 0.5)
    q = P[facing] - hc
    perp = np.linalg.norm(q - np.outer(q @ d, d), axis=1)
    return [round(float(v), 4) for v in P[facing][int(np.argmin(perp))]]


def main() -> int:
    RECORDS.mkdir(parents=True, exist_ok=True)
    PICTURES.mkdir(parents=True, exist_ok=True)
    LOOKS.mkdir(parents=True, exist_ok=True)
    F = gss.fields(parts=False)
    for rec in (lip_colour(F), tattoo()):
        print(f"{rec['name']}: {save_record(rec)}")
    point = back_of_left_hand(F)
    look = {"mesh": "MakeHuman_Body_v01", "label": "Red lips and a hand tattoo (Phase26 26.1)",
            "pieces": [{"piece": "Makeup_LipColour_Full_v01"},
                       {"piece": "Makeup_Tattoo_Arrow_v01", "point": point, "size": 0.042, "turn": 0}]}
    p = LOOKS / "red_lips_hand_tattoo.json"
    p.write_text(json.dumps(look, indent=2) + "\n", encoding="utf-8")
    print(f"look {p}: the tattoo at {point}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
