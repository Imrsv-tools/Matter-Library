"""Disposable probe for 260929_R_CharacterMaps.md (Pass 4).

Reads the pinned CC0 MakeHuman system-assets zip (sha256 b542127a…0107; the rig caches it at
library/parity/_sources/) and compares two ways a consumer can use a mesh's own colour picture:
  REPLACE  - the picture replaces the article's base colour; base_color_tint multiplies after
             (what Studio does for hair today, IMRSV P66 E8).
  MODULATE - the picture's STRUCTURE only (its luminance divided by its own bright level, so the
             brightest strand ~1.0), times the article's own light base, times the tint.
Flat 2D swatches, no lighting. Writes <out>.jpg and prints the numbers. Nothing in the repo is written.
Run:  uv run --with pillow --with numpy python 260929_R_CharacterMaps_probe.py <zip> <out.jpg>
"""
import io, sys, zipfile
import numpy as np
from PIL import Image, ImageDraw

Z = zipfile.ZipFile(sys.argv[1]); OUT = sys.argv[2]
def load(n): return Image.open(io.BytesIO(Z.read(n)))
def lin(a): a = a / 255.0; return np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
def srgb(a): a = np.clip(a, 0, 1); return np.where(a <= 0.0031308, a * 12.92, 1.055 * a ** (1 / 2.4) - 0.055)
LUM = np.array([0.2126, 0.7152, 0.0722])

HAIR_BASE = np.array([0.60, 0.45, 0.30])       # a pale fibre, as Hair_Natural is authored light (RD-P08-5)
TINTS = {"blonde": (1.0, 0.85, 0.55), "auburn": (0.55, 0.20, 0.08), "black": (0.05, 0.04, 0.035)}
SKIN = {"I": (0.847, 0.638, 0.552), "IV": (0.35, 0.19, 0.12), "VI": (0.09, 0.05, 0.02)}   # Physically Based
T = 256

def structure(rgb, mask):
    """Luminance / its 95th percentile inside the mask -> ~1 on the bright strands, <1 in gaps and roots."""
    L = rgb @ LUM
    ref = np.percentile(L[mask], 95)
    return np.clip(L / max(ref, 1e-6), 0, 1)[..., None], ref

tiles, notes = [], []
for name in ("hair/bob01/bob01_diffuse.png", "hair/long01/long01_diffuse.png", "hair/afro01/afro_diffuse.png"):
    im = np.asarray(load(name).convert("RGBA").resize((T, T))).astype(float)
    rgb, a = lin(im[..., :3]), im[..., 3] > 127
    s, ref = structure(rgb, a)
    bg = np.full_like(rgb, 0.18)
    for t, tint in TINTS.items():
        tint = np.array(tint)
        rep = np.where(a[..., None], rgb * tint, bg)
        mod = np.where(a[..., None], s * HAIR_BASE * tint, bg)
        tiles.append((f"{name.split('/')[1]} {t} REPLACE", rep)); tiles.append((f"{name.split('/')[1]} {t} MODULATE", mod))
        notes.append(f"{name.split('/')[1]:8s} {t:6s} median L  replace {np.median((rgb*tint)[a]@LUM):.4f}   modulate {np.median((s*HAIR_BASE*tint)[a]@LUM):.4f}")

# skin: the face island of one MakeHuman atlas; its LUMINANCE detail (divided by its own mean) over three library tones.
# (A per-channel ratio carries the source skin's chroma and casts dark tones olive: tried first, rejected.)
sk = np.asarray(load("skins/young_caucasian_female/young_lightskinned_female_diffuse.png").convert("RGB")
                .crop((1400, 700, 2040, 1640)).resize((T, T))).astype(float)
face = lin(sk); Lf = face @ LUM
detail = (Lf / Lf.mean())[..., None]
notes.append(f"skin luminance detail p5/p50/p95: {np.percentile(detail, [5, 50, 95]).round(2).tolist()}")
for k, tone in SKIN.items():
    tiles.append((f"skin {k} flat (today)", np.broadcast_to(np.array(tone), face.shape).copy()))
    tiles.append((f"skin {k} x atlas detail", np.clip(detail * np.array(tone), 0, 1)))

# eye: the brown eye picture as is, and its iris STRUCTURE over a blue and a green base. The iris is found by
# geometry (the pupil centres the platform measured off this picture, UV (0.705, 0.700) and (0.290, 0.288); iris
# radius ~0.105 UV, read off the picture), as Studio's Iris mesh is: a tint then reaches iris faces only.
E = 1024
ey = lin(np.asarray(load("eyes/materials/brown_eye.png").convert("RGB")).astype(float))
yy, xx = np.mgrid[0:E, 0:E]
iris = np.zeros((E, E), bool)
for u, v in ((0.705, 0.700), (0.290, 0.288)):
    iris |= (xx - u * E) ** 2 + (yy - (1 - v) * E) ** 2 < (0.105 * E) ** 2
L = ey @ LUM
s_e = np.clip(L / np.percentile(L[iris], 95), 0, 1)[..., None]
def small(a): return lin(np.asarray(Image.fromarray((srgb(a) * 255).astype(np.uint8)).resize((T, T))).astype(float))
tiles.append(("eye picture (brown, CC0)", small(ey)))
for k, base in {"blue base": (0.10, 0.22, 0.35), "green base": (0.12, 0.20, 0.06)}.items():
    tiles.append((f"eye iris {k} x structure", small(np.where(iris[..., None], s_e * np.array(base), ey))))

cols = 6; rows = (len(tiles) + cols - 1) // cols
sheet = Image.new("RGB", (cols * T, rows * (T + 18)), "white"); d = ImageDraw.Draw(sheet)
for i, (lab, arr) in enumerate(tiles):
    x, y = (i % cols) * T, (i // cols) * (T + 18)
    sheet.paste(Image.fromarray((srgb(arr) * 255).astype(np.uint8)), (x, y + 18)); d.text((x + 3, y + 3), lab, fill="black")
sheet.save(OUT, quality=80)
print("\n".join(notes))
