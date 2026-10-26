#!/usr/bin/env python3
"""The synthetic test set's look pictures (research 261026_R_SyntheticSkinAndEyes, Pass 4).

Re-makes the two JPGs beside the research doc from the parity rig's character renders, so each
tuning round can be compared with the last by re-running the same three steps:

    # 1. the skins and their shipped bases, at the rig's default size (about 40 s each)
    for a in Skin_Fitzpatrick{II,IV,VI}_Clean_{Base,Synth,SynthFreckles,SynthVeins,SynthMarks,SynthAll}_s001_v01; do
        uv run tools/parity/rig.py --character "$a" --no-blender      # --no-blender on the machine with Unreal
    done
    # 2. the eyes and the shipped one beside them (the rig's default 512 px: on the machine with
    #    Unreal, Storm fails on the character at --width 1024 and 2048, 2026-10-26)
    for a in Eye_Green_Clean_Base_sUKN_v01 Eye_Synth*; do
        uv run tools/parity/rig.py --character "$a" --no-blender
    done
    # 3. the pictures
    uv run docs/Planning/Research/261026_R_SyntheticSkinAndEyes_look.py

Storm's pictures are used (the rig scores Storm against Unreal; their agreement is on each sheet).
Reads only the git-ignored ``library/parity/`` and the fit set's eye pictures; writes the two JPGs.
"""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PAR = REPO / "library" / "parity"
EYES_FIT = REPO / "MatterLibrary" / "textures" / "fit" / "makehuman" / "eyes"
STEM = "261026_R_SyntheticSkinAndEyes"

TONES = ("II", "IV", "VI")
SETS = ("Base", "Synth", "SynthFreckles", "SynthVeins", "SynthMarks", "SynthAll")
EYES = [("Eye_Green_Clean_Base_sUKN_v01", "Green", "Green (shipped)")] + [
    (f"Eye_Synth{c}_{k}_Base_sUKN_v01", f"Synth{c}{'Bloodshot' if k == 'Bloodshot' else ''}",
     f"{c}{' bloodshot' if k == 'Bloodshot' else ''}")
    for c, k in (("DarkBrown", "Clean"), ("Brown", "Clean"), ("Amber", "Clean"), ("Hazel", "Clean"),
                 ("Green", "Clean"), ("Grey", "Clean"), ("Blue", "Clean"), ("LightBlue", "Clean"),
                 ("Brown", "Bloodshot"), ("Blue", "Bloodshot"))]

CELL = 256
LABEL = 26


def font(size: int):
    for f in ("DejaVuSans.ttf", "/usr/share/fonts/google-noto/NotoSans-Regular.ttf"):
        try:
            return ImageFont.truetype(f, size)
        except OSError:
            continue
    return ImageFont.load_default(size)


F, FS = font(16), font(13)


def render(article: str, view: str) -> Image.Image:
    name = "defaults.png" if view == "wide" else f"defaults__{view}.png"
    path = PAR / f"Character__{article}" / "storm" / name
    if not path.is_file():
        sys.exit(f"missing {path}: run step 1/2 of this file's doc string first")
    return Image.open(path).convert("RGB")


def crop_rel(im: Image.Image, box: tuple[float, float, float, float]) -> Image.Image:
    w, h = im.size
    return im.crop((int(box[0] * w), int(box[1] * h), int(box[2] * w), int(box[3] * h)))


def skins() -> Path:
    """Rows: tone x view (face, then the hand and forearm, where the veins are); columns: the layer sets."""
    views = (("face", (0.18, 0.14, 0.82, 0.78)), ("hand", (0.0, 0.0, 1.0, 1.0)))
    rows = [(t, v, box) for v, box in views for t in TONES]
    W, H = LABEL * 3 + CELL * len(SETS), LABEL + CELL * len(rows)
    sheet = Image.new("RGB", (W, H), (236, 236, 236))
    d = ImageDraw.Draw(sheet)
    for c, s in enumerate(SETS):
        d.text((LABEL * 3 + c * CELL + 6, 5), s if s != "Base" else "Base (shipped)", fill=(0, 0, 0), font=F)
    for r, (tone, view, box) in enumerate(rows):
        y = LABEL + r * CELL
        d.text((4, y + CELL // 2 - 20), tone, fill=(0, 0, 0), font=F)
        d.text((4, y + CELL // 2 + 2), view, fill=(80, 80, 80), font=FS)
        for c, s in enumerate(SETS):
            art = f"Skin_Fitzpatrick{tone}_Clean_{s}_s001_v01"
            sheet.paste(crop_rel(render(art, view), box).resize((CELL, CELL), Image.LANCZOS),
                        (LABEL * 3 + c * CELL, y))
    out = HERE / f"{STEM}_skins.jpg"
    sheet.save(out, quality=82, optimize=True)
    return out


def eyes() -> Path:
    """Per eye: the iris as drawn (its fit-set picture, centred on the right eye's pupil) and the same
    eye rendered, cropped from the 512 px face view and enlarged about 4x (soft by construction)."""
    n_col = 4
    pic = CELL
    tile_w, tile_h = pic * 2, pic + LABEL
    n_row = -(-len(EYES) // n_col)
    sheet = Image.new("RGB", (tile_w * n_col, tile_h * n_row), (236, 236, 236))
    d = ImageDraw.Draw(sheet)
    for i, (art, fit, label) in enumerate(EYES):
        x, y = (i % n_col) * tile_w, (i // n_col) * tile_h
        tex = Image.open(EYES_FIT / f"{fit}_basecolor_sUKN.png").convert("RGB")
        w, h = tex.size
        # the iris disc of the fit-set layout (build_character MESHES['eyes'] circles: centre, radius)
        cx, cy, rad = 0.705, 1 - 0.700, 0.118 * 1.15
        flat = tex.crop((int((cx - rad) * w), int((cy - rad) * h), int((cx + rad) * w), int((cy + rad) * h)))
        sheet.paste(flat.resize((pic, pic), Image.LANCZOS), (x, y + LABEL))
        face = render(art, "face")
        # the character's right eye in the rig's face view (centre ~ (0.36, 0.40) of the frame)
        sheet.paste(crop_rel(face, (0.30, 0.34, 0.42, 0.46)).resize((pic, pic), Image.LANCZOS),
                    (x + pic, y + LABEL))
        d.text((x + 6, y + 5), label, fill=(0, 0, 0), font=F)
    out = HERE / f"{STEM}_eyes.jpg"
    sheet.save(out, quality=85, optimize=True)
    return out


if __name__ == "__main__":
    which = sys.argv[1:] or ["skins", "eyes"]
    for w in which:
        print(f"wrote {(skins if w == 'skins' else eyes)()}")
