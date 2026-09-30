#!/usr/bin/env python3
"""Write the library's FIT SET for MakeHuman: the pictures drawn on its meshes' own layouts (Phase09).

    uv run tools/converters/fit/gen_fit_makehuman.py            # every set
    uv run tools/converters/fit/gen_fit_makehuman.py hair       # one set

A **fit set** is the pictures a mesh family's own UV layout carries, held by the library and
supplied when an article is bound, never inside the article (Phase09 RD-P09-2; MAP-RD1: *"the
libery has all the assets anyone needs"*; D1 / CM2). They land in
``MatterLibrary/textures/fit/makehuman/<set>/`` with the texture grammar, ``<Name>_<role>_sUKN.png``:
a picture drawn on a layout has no real-world size, so its scale tag is ``sUKN``.

**hair** (9.1) — each of the pack's 10 hairstyles, 12 eyebrows and 4 eyelash cards:

* ``<Name>_basecolor_sUKN.png`` — the picture's STRUCTURE, not its colour (MAP-RD3 as amended:
  the picture shades the article's own light colour). Its linear luminance divided by its own
  95th percentile over the covered strands (the research's Pass 4 method), so the brightest
  strand is ~1 and roots and gaps fall below; clipped to 1 and written grey, sRGB-encoded (the
  input's colour space, ``srgb_texture``). A picture of black paint (95th percentile under
  ``FLAT_BELOW``) has no structure to keep and is written flat, 1. A fully transparent pixel takes the covered median,
  so filtering at a card's edge draws no dark halo. The article multiplies it into its base
  colour (``base_color_map``), so any tint reaches every style (MAP-F2) and the brows and lashes
  follow it (MAP-F3).
* ``<Name>_opacity_sUKN.png`` — the picture's alpha, one channel: the card's cut-out
  (``cutout_map``; RD-P09-6: the library prepares it too).

**eyes** (9.2) — the pack's nine eyeball pictures, ``<Colour>_basecolor_sUKN.png``, as they are:
the eye's colour IS the picture (``write_eyes``).

The source is MakeHuman's system-asset pack (CC0), pinned by URL and sha256 in the rig's character
builder (``tools/parity/scene/build_character.py`` ``SOURCES``) and fetched once into the
git-ignored ``library/parity/_sources/``. Deterministic: the same pack gives the same bytes.
Provenance: ``library/provenance/sources/fit/makehuman/<set>.yaml``.
"""

from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "tools" / "parity" / "scene"))
import build_character  # noqa: E402  (the pinned-source fetch: URL + sha256)

PACK = build_character.PACK
FIT = REPO / "MatterLibrary" / "textures" / "fit" / "makehuman"
PROVENANCE = REPO / "library" / "provenance" / "sources" / "fit" / "makehuman"
TAG = "sUKN"
COVERED = 0.5          # alpha at or above which a pixel is a strand (the percentile's sample)
PERCENTILE = 95        # Pass 4: luminance / its own 95th percentile -> brightest strand ~1
# Below this 95th percentile (linear; ~14 of 255 sRGB levels) a picture is black paint: dividing
# by it amplifies 8-bit quantisation, not strands, and a picture of pure black (four of the pack's
# brow and lash cards) would divide to 0 and hold the brows black at any tint (MAP-F3). Such a
# picture carries no structure, so it is written FLAT (1: the article's own colour, tinted).
FLAT_BELOW = 0.004


def _pack_members() -> list[str]:
    with zipfile.ZipFile(io.BytesIO(build_character.source(PACK))) as z:
        return z.namelist()


def hair_sources() -> dict[str, str]:
    """Name -> the pack member: every hairstyle's colour picture, every eyebrow and eyelash card."""
    out = {}
    for m in _pack_members():
        parts = m.split("/")
        if len(parts) != 3 or not m.endswith(".png") or m.endswith("_normal.png"):
            continue
        kind, style, file = parts
        if kind == "hair" and "diffuse" in file:
            out[style[:1].upper() + style[1:]] = m
        elif kind in ("eyebrows", "eyelashes") and file == f"{style}.png":
            out[style[:1].upper() + style[1:]] = m
    return dict(sorted(out.items()))


def _srgb_to_linear(c: np.ndarray) -> np.ndarray:
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _linear_to_srgb(c: np.ndarray) -> np.ndarray:
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1 / 2.4) - 0.055)


def structure(rgba: np.ndarray) -> tuple[np.ndarray, dict]:
    """The picture's normalised luminance (0..1, linear) and the numbers that made it."""
    rgb, a = rgba[..., :3] / 255.0, rgba[..., 3] / 255.0
    lin = _srgb_to_linear(rgb)
    lum = 0.2126 * lin[..., 0] + 0.7152 * lin[..., 1] + 0.0722 * lin[..., 2]
    covered = a >= COVERED
    if not covered.any():
        raise ValueError("no covered pixels: nothing to normalise")
    p = float(np.percentile(lum[covered], PERCENTILE))
    flat = p < FLAT_BELOW
    s = np.ones_like(lum) if flat else np.clip(lum / p, 0.0, 1.0)
    med = float(np.median(s[covered]))
    s[a <= 0.0] = med
    return s, {"p95_linear": p, "covered_median": med, "covered_fraction": float(covered.mean()),
               "flat": flat}


def write_hair() -> list[tuple[str, dict]]:
    out_dir = FIT / "hair"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, member in hair_sources().items():
        rgba = np.asarray(Image.open(io.BytesIO(build_character.source(PACK, member))).convert("RGBA"))
        s, stats = structure(rgba)
        grey = np.round(_linear_to_srgb(s) * 255.0).astype(np.uint8)
        Image.fromarray(np.dstack([grey, grey, grey]), "RGB").save(
            out_dir / f"{name}_basecolor_{TAG}.png", optimize=True)
        Image.fromarray(rgba[..., 3], "L").save(out_dir / f"{name}_opacity_{TAG}.png", optimize=True)
        rows.append((name, {"member": member, **stats}))
        print(f"fit/hair {name}: p95 {stats['p95_linear']:.4f}, covered {stats['covered_fraction']:.2f}, "
              f"median structure {stats['covered_median']:.2f}{'  FLAT (black paint)' if stats['flat'] else ''}")
    return rows


def write_provenance(set_name: str, rows: list[tuple[str, dict]]) -> None:
    PROVENANCE.mkdir(parents=True, exist_ok=True)
    rel = f"MatterLibrary/textures/fit/makehuman/{set_name}"
    src = build_character.SOURCES[PACK]
    lines = [
        "# Provenance for one fit set (Phase09 RD-P09-2): pictures on MakeHuman's own UV layouts,",
        "# supplied when an article is bound, never inside it. Written by the tool named in `evidence`.",
        f"id: fit/makehuman/{set_name}",
        "version: v01",
        "files:",
    ]
    for name, _ in rows:
        lines.append(f"  - {rel}/{name}_basecolor_{TAG}.png")
        if (FIT / set_name / f"{name}_opacity_{TAG}.png").exists():
            lines.append(f"  - {rel}/{name}_opacity_{TAG}.png")
    lines += [
        "provenance:",
        "  source: derived",
        "  license: CC0-1.0",
        f"  upstream: {src['url']}",
        f"  upstream_sha256: {src['sha256']}",
        f"  upstream_licence: \"{src['licence']}\"",
        "  evidence: tools/converters/fit/gen_fit_makehuman.py",
        "members:",
    ]
    for name, r in rows:
        extra = (f", p95_linear: {r['p95_linear']:.5f}, flat: {'true' if r['flat'] else 'false'}"
                 if "p95_linear" in r else "")
        lines.append(f"  {name}: {{member: {r['member']}{extra}}}")
    (PROVENANCE / f"{set_name}.yaml").write_text("\n".join(lines) + "\n", encoding="utf-8")


EYE_NAMES = {"brown": "Brown", "brownlight": "BrownLight", "blue": "Blue", "bluegreen": "BlueGreen",
             "deepblue": "DeepBlue", "green": "Green", "grey": "Grey", "ice": "Ice", "lightblue": "LightBlue"}


def write_eyes() -> list[tuple[str, dict]]:
    """The nine eyeball pictures, as they are (RGB, sRGB): the eye's COLOUR is which picture the
    binding supplies (Phase09 RD-P09-3, F-P09-3; the lead's lean to separate pictures, MAP-Q5).
    Each draws the sclera with its veins, the iris with its fibres and dark limbal ring, and the
    pupil, on MakeHuman's one eye layout (MAP-F11). Their alpha is all opaque, so no cut-out."""
    out_dir = FIT / "eyes"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for key, name in EYE_NAMES.items():
        member = f"eyes/materials/{key}_eye.png"
        im = Image.open(io.BytesIO(build_character.source(PACK, member))).convert("RGB")
        im.save(out_dir / f"{name}_basecolor_{TAG}.png", optimize=True)
        rows.append((name, {"member": member}))
        print(f"fit/eyes {name}: {im.size[0]}x{im.size[1]}")
    return rows


SETS = {"hair": write_hair, "eyes": write_eyes}


def main(argv=None) -> int:
    names = (argv if argv is not None else sys.argv[1:]) or list(SETS)
    for n in names:
        if n not in SETS:
            raise SystemExit(f"unknown fit set {n!r} (have {sorted(SETS)})")
        write_provenance(n, SETS[n]())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
