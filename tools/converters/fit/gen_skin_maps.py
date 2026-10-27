#!/usr/bin/env python3
"""Make the library's SKIN MAPS for MakeHuman_Body_v01 (hm08), one per Fitzpatrick tone (Phase21).

    uv run tools/converters/fit/gen_skin_maps.py                  # every tone
    uv run tools/converters/fit/gen_skin_maps.py IV               # one tone
    uv run tools/converters/fit/gen_skin_maps.py IV --picture my_skin.png   # a contributor's picture

A **skin map** is a colour picture of the body drawn on hm08's atlas (``docs/specs/Authoring/
SkinMaps.md``). The six ``Skin_Fitzpatrick*`` articles carry it as their own ``base_color_map``
(RD-P18-9, RD-P21-1) and the six ``Lips_Fitzpatrick*`` carry the same one (RD-P21-2), so the
colour runs across the lip edge.

**What the picture is made of** (Phase23, RD-P23-2: pigment, not paint). The colour comes from
``gen_synth_skin.compose``: every texel gets a melanin and a blood amount placed on the body in 3D,
and a tabulated skin model (OMF's two-chromophore model, ``synth/chromophore_lut.json``) turns them
into colour, relative to the tone. The model holds only at III and IV (23.2.1), so I and II take
III's fitted response and V and VI take IV's (the lead, 2026-10-27, "Borrow the response"). CC0
parts only, never a photograph (RD-SKM-2, RD-SKM-5): MPFB2's CC0 region masks, hm08, seeded 3D
noise. The groin is plain skin by construction (RD-SKM-4). The lips take the lip colour, feathered
into the face. *(Until Phase23 it was the research probe's v2 recipe, F-SKM-25: an AO bake in
Blender, value noise and two cheek blobs; retired at 23.2.)*

**The calibration** (RD-P21-3, the spec's steps 2 and 3; ``calibrate``). The measured tone stays
the average: over the skin (the ``Body`` part, lips excluded) the picture's average is the
article's measured tone. The stored map is the picture divided by the tone and scaled so its
brightest is 1 (the 99.9th percentile per channel); the article's ``base_color_const`` is raised
by the same factor. The factor is worked out from the map AS STORED (8-bit sRGB, decoded), so the
average that renders is the tone to rounding. **The brightest texel stays a real albedo**
(``fit_albedo``, 23.2.11): where the constant would pass ``ALBEDO_MAX``, as a light tone with a
contrasty picture asks, the picture's light side (above the skin's mean) is compressed by one
exponent on every channel (the provenance row's ``contrast``) until it fits; the dark side (the
lips, the ring under the eye) is kept. ``--picture`` runs the same step on a contributor's
colour picture: they hand in a colour picture, the library stores the multiplier.

The tone is the skin recipe's Physically Based value (its ``sources[physicallybased].used``),
never its ``base_color_const``, which this tool's output raises. The lip colour is Phase08's rule
(the tone x ``LIP_RULE``; ``Lips_Fitzpatrick*``'s sources), drawn by the maker from the tone alone.

Writes ``MatterLibrary/textures/fit/makehuman/skin/Fitzpatrick<Tone>_basecolor_sUKN.png`` and
``library/provenance/sources/fit/makehuman/skin.yaml`` (with each tone's ``base_color_const``,
which the skin and lips recipes carry), and prints the numbers.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "tools" / "parity" / "scene"))
sys.path.insert(0, str(HERE))
import build_character as bc  # noqa: E402  (the pinned-source fetch: URL + sha256)

MESH = "MakeHuman_Body_v01"
N = 2048                                   # groups.PART_MESHES[MESH]["map_size"]
TONES = ("I", "II", "III", "IV", "V", "VI")
RECIPES = REPO / "tools" / "converters" / "recipes"
OUT = REPO / "MatterLibrary" / "textures" / "fit" / "makehuman" / "skin"
PROVENANCE = REPO / "library" / "provenance" / "sources" / "fit" / "makehuman" / "skin.yaml"
TAG = "sUKN"
BLEED = 16                                 # pixels past each island's edge (the kit's README)
LIP_RULE = (0.80, 0.55, 0.60)              # Phase08 8.2: lips = the skin's albedo x this
PEAK = 99.9                                # the stored map's brightest: this percentile -> 1
ALBEDO_MAX = 0.99                          # the constant's ceiling (G6: <= 1; headroom for 8-bit)

# MPFB2's CC0 region masks and thickness map on hm08's UVs (the probe pinned their git blob
# sha1s, 2026-10-14; these are the same files' sha256, measured 2026-10-20). The rig's own masks
# (lips, nails) are already in its table.
_MPFB = bc._MPFB
for _name, _sha in (("mpfb_face.jpg", "6f2d7abee30d63378b7b4214cf43a47d4cae65d967c12b34e365e058448b96df"),
                    ("mpfb_ears.jpg", "8c1becd3887b65df50720de87e91807667155107d23a6da9f5142d84142b724b"),
                    ("mpfb_eyelids.jpg", "2b6f41d6c51f1a991f715025f87a0c8626c889201c8fe9c12514fcc579710532"),
                    ("mpfb_aureolae.jpg", "bc69ca4c397a721c8e47fb854028649dd1c5aeb2d184b60c984f3eb6d53e2de7"),
                    ("sss.png", "d433f15c7240c5b0c91c6fafa482d9c380504efd6ad4d1504b4d7da32d1eec42")):
    bc.SOURCES.setdefault(_name, {"url": _MPFB + _name, "sha256": _sha,
                                  "licence": "CC0 (MPFB2 LICENSE.ASSETS.md: textures on hm08's UVs)"})
MASKS = ("face", "lips", "ears", "eyelids", "aureolae")


# ---------------------------------------------------------------- the picture (numpy) ------------
def _srgb_to_linear(c):
    import numpy as np  # noqa: PLC0415
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def _linear_to_srgb(c):
    import numpy as np  # noqa: PLC0415
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(np.maximum(c, 0), 1 / 2.4) - 0.055)


def _grey(name: str):
    """A pinned greyscale source on the atlas, 0..1 as stored (data, not colour), N x N."""
    import io  # noqa: PLC0415
    import numpy as np  # noqa: PLC0415
    from PIL import Image  # noqa: PLC0415
    im = Image.open(io.BytesIO(bc.source(name))).convert("RGB")
    a = np.asarray(im, dtype=np.float32)[..., 0] / 255.0
    if a.shape != (N, N):
        a = np.asarray(Image.fromarray(a, "F").resize((N, N), Image.BILINEAR), dtype=np.float32)
    return a


def blur(a, r: int):
    """Three box passes: about a Gaussian of sigma ~ r pixels (the probe's)."""
    import numpy as np  # noqa: PLC0415
    for _ in range(3):
        for ax in (0, 1):
            c = np.cumsum(np.pad(a, [(r + 1, r) if i == ax else (0, 0) for i in (0, 1)], mode="edge"), axis=ax)
            a = (np.take(c, range(2 * r + 1, c.shape[ax]), axis=ax)
                 - np.take(c, range(0, c.shape[ax] - 2 * r - 1), axis=ax)) / (2 * r + 1)
    return a


def vnoise(P, scale: float, seed: int):
    """3D value noise in -1..1 over the texels' positions: seamless across UV seams."""
    import numpy as np  # noqa: PLC0415
    q = P / scale
    i = np.floor(q).astype(np.int64)
    f = q - i
    f = f * f * (3 - 2 * f)

    def h(dx, dy, dz):
        n = ((i[..., 0] + dx) * 73856093) ^ ((i[..., 1] + dy) * 19349663) ^ ((i[..., 2] + dz) * 83492791) ^ seed
        return ((n * 2654435761) % 4294967296) / 4294967296.0
    acc = 0
    for dx in (0, 1):
        for dy in (0, 1):
            for dz in (0, 1):
                w = ((f[..., 0] if dx else 1 - f[..., 0]) * (f[..., 1] if dy else 1 - f[..., 1])
                     * (f[..., 2] if dz else 1 - f[..., 2]))
                acc = acc + w * h(dx, dy, dz)
    return acc * 2 - 1


def regions() -> dict:
    """The atlas's regions: ``islands`` (on the mesh, from the committed island picture G8 reads)
    and each rig part of the mesh (``Body`` is the skin: the lips and nails are parts of their own),
    rasterised FACE BY FACE as the rig splits them. Not by island, as the fitted teeth's are: the
    lips share the face's island, so an island vote gives the Body every lip texel (measured
    2026-10-20: the Lips mask came out empty)."""
    import numpy as np  # noqa: PLC0415
    from PIL import Image, ImageDraw  # noqa: PLC0415
    import make_kits  # noqa: PLC0415
    ids = np.asarray(Image.open(REPO / "library" / "meshes" / f"{MESH}_islands.png")).astype(np.int64)
    m = make_kits.load_mesh(MESH)
    out = {"islands": ids > 0}
    for part, faces in m["split"].items():
        im = Image.new("L", (N, N), 0)
        d = ImageDraw.Draw(im)
        for i in faces:
            d.polygon(make_kits._poly(m["faces"][i], m["vt"], N), fill=255)
        out[part] = np.asarray(im) >= 128
    out["Body"] = out["Body"] & ~out["Lips"] & ~out["Nails"]   # a shared edge pixel is not skin
    return out


def tone_of(roman: str):
    """The skin's measured tone: its recipe's Physically Based value (never base_color_const)."""
    import numpy as np  # noqa: PLC0415
    r = json.loads((RECIPES / f"Skin_Fitzpatrick{roman}_Clean_Base_s001_v01.json").read_text())
    used = [s["used"]["base_color_const"] for s in r["sources"]
            if s.get("kind") == "physicallybased" and "base_color_const" in s.get("used", {})]
    if len(used) != 1:
        raise SystemExit(f"Skin_Fitzpatrick{roman}: {len(used)} Physically Based base colours in its sources")
    return np.array([float(x) for x in used[0].split(",")])


def bleed(lin, covered, px: int):
    """Grow the covered colour ``px`` pixels outward (gen_fit_makehuman.bleed)."""
    import gen_fit_makehuman as fm  # noqa: PLC0415
    return fm.bleed(lin, covered, px)


def fit_albedo(ratio, tone, S, cover):
    """Keep the brightest texel a real albedo (G6: base_color_const in [0, 1]). The constant is the
    tone x the picture's peak over its skin mean, so a light tone with a contrasty picture asks for
    more than 1 (23.2.11: tone I on III's fit, its face 1.2-1.5x its trunk, asked for 1.21 in red).
    Then the picture's LIGHT side is compressed: above the skin's mean, ONE exponent on every channel
    (so the hue of each region holds); at or below it (the lips, the ring under the eye) the picture
    is kept as made. Just enough to fit. Returns (ratio, the exponent; 1 = as made)."""
    import numpy as np  # noqa: PLC0415
    m = ratio[S].mean(0)
    lr = np.log(np.maximum(ratio / m, 1e-6))

    def knee(g):
        return m * np.exp(np.where(lr > 0, g * lr, lr))

    def peak(r):           # the constant calibrate would write, per channel
        return tone * np.percentile(r[cover], PEAK, axis=0) / r[S].mean(0)

    if peak(ratio).max() <= ALBEDO_MAX:
        return ratio, 1.0
    lo, hi = 0.0, 1.0
    for _ in range(30):                        # bisect the exponent: the largest that fits
        g = (lo + hi) / 2
        lo, hi = (g, hi) if peak(knee(g)).max() <= ALBEDO_MAX else (lo, g)
    if peak(knee(lo)).max() > ALBEDO_MAX:
        raise SystemExit(f"tone {list(tone)}: no compression of the light side brings the constant under "
                         f"{ALBEDO_MAX} (the dark side alone asks too much)")
    return knee(lo), lo


def calibrate(col, tone, reg: dict, cover):
    """The colour picture -> (the stored map as 8-bit sRGB, the article's base_color_const, the
    numbers). The map is col / tone over its own 99.9th percentile per channel (brightest ~1); the
    constant is the tone over the STORED map's decoded average over the skin, so the article
    renders the tone on average (RD-P21-3)."""
    import numpy as np  # noqa: PLC0415
    S = reg["Body"]
    ratio = col / tone
    ratio, gamma = fit_albedo(ratio, tone, S, cover)
    k = np.maximum(np.percentile(ratio[cover], PEAK, axis=0), 1e-6)
    mp = np.clip(ratio / k, 0.0, 1.0)
    clipped = float((ratio[cover] / k > 1.0).any(axis=-1).mean())
    mp = bleed(np.where(cover[..., None], mp, 0.0), cover, BLEED)
    grown = cover.copy()
    for _ in range(BLEED):                     # where the bleed reached (any covered 4-neighbour)
        grown = grown | np.roll(grown, 1, 0) | np.roll(grown, -1, 0) | np.roll(grown, 1, 1) | np.roll(grown, -1, 1)
    mp[~grown] = mp[S].mean(0)                 # beyond: the skin's own mean, so a mip blends no black
    srgb8 = np.round(_linear_to_srgb(mp) * 255.0).astype(np.uint8)
    dec = _srgb_to_linear(srgb8 / 255.0)
    const = tone / dec[S].mean(0)
    stats = {"tone": [round(float(v), 4) for v in tone],
             "base_color_const": [round(float(v), 4) for v in const],
             "peak_factor": [round(float(v), 4) for v in k],
             "contrast": round(gamma, 3),
             "clipped_share": round(clipped, 5),
             "skin_average": [round(float(v), 4) for v in (const * dec[S].mean(0))],
             "lips_average": [round(float(v), 4) for v in (const * dec[reg["Lips"]].mean(0))],
             "uncovered_islands": int((reg["islands"] & ~grown).sum())}
    return srgb8, const, stats


def write(roman: str, srgb8) -> Path:
    from PIL import Image  # noqa: PLC0415
    OUT.mkdir(parents=True, exist_ok=True)
    p = OUT / f"Fitzpatrick{roman}_basecolor_{TAG}.png"
    Image.fromarray(srgb8, "RGB").save(p, optimize=True)
    return p


def write_provenance(rows: dict) -> None:
    """``skin.yaml``: every tone written so far (a run of one tone keeps the others' rows)."""
    old, shine_files, shine_rows = {}, [], []
    if PROVENANCE.is_file():
        for line in PROVENANCE.read_text().splitlines():
            if line.startswith("  Fitzpatrick") and ": {" in line:
                old[line.split(":", 1)[0].strip()] = line
            # Phase22: the shine maps' rows are gen_skin_shine.py's; carry them over unchanged
            elif line.startswith("  - MatterLibrary/textures/fit/makehuman/skin/Skin_"):
                shine_files.append(line)
            elif line.startswith("  Skin_") and ": {" in line:
                shine_rows.append(line)
    for roman, r in rows.items():
        old[f"Fitzpatrick{roman}"] = (
            f"  Fitzpatrick{roman}: {{made: {r['made']}, "
            + (f"fit: {r['fit']}, melanin0: {r['melanin0']}, " if "fit" in r else "")
            + (f"contrast: {r['contrast']}, " if r.get("contrast", 1.0) != 1.0 else "")
            + f"tone: {r['tone']}, base_color_const: "
            f"{r['base_color_const']}, peak_factor: {r['peak_factor']}, lips_average: {r['lips_average']}}}")
    names = sorted(old, key=lambda n: TONES.index(n.removeprefix("Fitzpatrick")))
    src = [bc.SOURCES[n] for n in ("base.obj", "mpfb_face.jpg", "mpfb_lips.jpg", "mpfb_ears.jpg",
                                   "mpfb_eyelids.jpg", "mpfb_aureolae.jpg", "sss.png")]
    lines = [
        "# Provenance for the skin maps (Phase21): one colour map per Fitzpatrick tone, drawn on",
        "# MakeHuman_Body_v01 (hm08), each a fitted Character article's own picture (RD-P18-9,",
        "# RD-P21-1). Made from CC0 parts only, no photograph (RD-SKM-2). Written by `evidence`.",
        "id: fit/makehuman/skin",
        "version: v01",
        "files:",
        *[f"  - MatterLibrary/textures/fit/makehuman/skin/{n}_basecolor_{TAG}.png" for n in names],
        *shine_files,
        "provenance:",
        "  source: derived",
        "  license: CC0-1.0",
        "  upstream:",
        *[f"    - {{url: {s['url']}, sha256: {s['sha256']}}}" for s in src],
        "  upstream_licence: \"CC0 (MPFB2 LICENSE.ASSETS.md: the hm08 base mesh and its textures)\"",
        "  model: \"open-morphology-foundation tools/material_generate/biophysical.py 0.1.0 (e079588), "
        "tabulated per fit in tools/converters/fit/synth/chromophore_lut.json\"",
        "  evidence: tools/converters/fit/gen_skin_maps.py, tools/converters/fit/gen_synth_skin.py"
        + (", tools/converters/fit/gen_skin_shine.py" if shine_rows else ""),
        "members:",
        *[old[n] for n in names],
        *shine_rows,
    ]
    PROVENANCE.parent.mkdir(parents=True, exist_ok=True)
    PROVENANCE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def from_picture(path: Path, reg: dict):
    """A contributor's colour picture (sRGB, N x N, on hm08's atlas) as linear colour."""
    import numpy as np  # noqa: PLC0415
    from PIL import Image  # noqa: PLC0415
    im = Image.open(path).convert("RGB")
    if im.size != (N, N):
        raise SystemExit(f"{path}: {im.size[0]} x {im.size[1]}; {MESH}'s pictures are {N} x {N}")
    return _srgb_to_linear(np.asarray(im, dtype=np.float64) / 255.0), reg["islands"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("tones", nargs="*", default=list(TONES), help="Roman numerals (default: all six)")
    ap.add_argument("--picture", type=Path, help="a contributor's colour picture for ONE tone")
    a = ap.parse_args(argv)
    bad = [t for t in a.tones if t not in TONES]
    if bad:
        raise SystemExit(f"unknown tone {bad} (have {list(TONES)})")
    if a.picture and len(a.tones) != 1:
        raise SystemExit("--picture is one tone's picture: name exactly one tone")
    reg = regions()
    F = lut = None
    rows = {}
    for roman in a.tones:
        tone = tone_of(roman)
        if a.picture:
            col, cover = from_picture(a.picture, reg)
            made = "contributed"
        else:
            import gen_synth_skin as gss  # noqa: PLC0415 (it imports this module)
            if F is None:
                F, lut = gss.fields(), gss.Lut()
            col, _info = gss.compose(tone, roman, (), F, lut, gss.SEED)
            cover = F["cover"]
            made = "pigment"
            model = lut.check(roman, tone)
            print(f"Fitzpatrick{roman} model check (RD-P23-3): " + json.dumps(model))
        srgb8, _const, st = calibrate(col, tone, reg, cover)
        p = write(roman, srgb8)
        rows[roman] = {"made": made, **st} | ({"fit": model["fit"], "melanin0": model["melanin0"]}
                                              if made == "pigment" else {})
        print(f"Fitzpatrick{roman}: {p.relative_to(REPO)}\n  " + json.dumps(st))
        if st["uncovered_islands"]:
            raise SystemExit(f"Fitzpatrick{roman}: {st['uncovered_islands']} island texels left unpainted")
    write_provenance(rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
