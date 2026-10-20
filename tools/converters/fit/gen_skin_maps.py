#!/usr/bin/env python3
"""Make the library's SKIN MAPS for MakeHuman_Body_v01 (hm08), one per Fitzpatrick tone (Phase21).

    uv run tools/converters/fit/gen_skin_maps.py                  # every tone
    uv run tools/converters/fit/gen_skin_maps.py IV               # one tone
    uv run tools/converters/fit/gen_skin_maps.py IV --picture my_skin.png   # a contributor's picture

A **skin map** is a colour picture of the body drawn on hm08's atlas (``docs/specs/Authoring/
SkinMaps.md``). The six ``Skin_Fitzpatrick*`` articles carry it as their own ``base_color_map``
(RD-P18-9, RD-P21-1) and the six ``Lips_Fitzpatrick*`` carry the same one (RD-P21-2), so the
colour runs across the lip edge.

**What the picture is made of** (RD-SKM-2, RD-SKM-5: CC0 parts only, never a photograph). The
recipe is the research probe's v2 (``docs/Planning/Research/261014_R_SkinMaps_probe.py``,
F-SKM-25), unchanged:

* MPFB2's CC0 region masks (face, lips, ears, eyelids, areolae) and its thickness map
  (``sss.png``), pinned by sha256 in the rig's source table (``build_character.SOURCES``);
* an ambient-occlusion bake of the mesh, and each texel's 3D position, baked once in Blender
  headless (``bake``; cached in the git-ignored ``library/parity/_sources/skinmaps/``);
* 3D value noise (seamless across UV seams), and two cheek blobs placed from the face's own
  texel positions (no hand painting).

Blood (haemoglobin absorbs green and blue) reddens the thin and flushed regions; melanin and
occlusion darken the creases, the eye sockets and the areolae. The groin is plain skin by
construction (RD-SKM-4). The lips take the lip colour, feathered into the face.

**The calibration** (RD-P21-3, the spec's steps 2 and 3; ``calibrate``). The measured tone stays
the average: over the skin (the ``Body`` part, lips excluded) the picture's average is the
article's measured tone. The stored map is the picture divided by the tone and scaled so its
brightest is 1 (the 99.9th percentile per channel); the article's ``base_color_const`` is raised
by the same factor. The factor is worked out from the map AS STORED (8-bit sRGB, decoded), so the
average that renders is the tone to rounding. ``--picture`` runs the same step on a contributor's
colour picture: they hand in a colour picture, the library stores the multiplier.

The tone is the skin recipe's Physically Based value (its ``sources[physicallybased].used``),
never its ``base_color_const``, which this tool's output raises. The lip colour is Phase08's rule
(the tone x ``LIP_RULE``; ``Lips_Fitzpatrick*``'s sources).

Writes ``MatterLibrary/textures/fit/makehuman/skin/Fitzpatrick<Tone>_basecolor_sUKN.png`` and
``library/provenance/sources/fit/makehuman/skin.yaml`` (with each tone's ``base_color_const``,
which the skin and lips recipes carry), and prints the numbers.
"""

from __future__ import annotations

import argparse
import json
import subprocess
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
BAKE = bc.CACHE / "skinmaps"               # git-ignored: the mesh's AO and texel positions
TAG = "sUKN"
BLEED = 16                                 # pixels past each island's edge (the kit's README)
LIP_RULE = (0.80, 0.55, 0.60)              # Phase08 8.2: lips = the skin's albedo x this
PEAK = 99.9                                # the stored map's brightest: this percentile -> 1

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


# ---------------------------------------------------------------- bake (inside Blender) ----------
def bake(out: Path) -> None:
    """AO (4 cm of occlusion) and each texel's object-space position (MakeHuman units), baked on
    hm08's body at N x N with a 16-pixel margin; saved top row first, as an image file is read."""
    import bpy
    import numpy as np

    out.mkdir(parents=True, exist_ok=True)
    obj = out / "base.obj"
    obj.write_bytes(bc.source("base.obj"))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.obj_import(filepath=str(obj), use_split_groups=True)
    body = next(o for o in bpy.context.scene.objects if o.type == "MESH" and o.name.lower() == "body")
    for o in list(bpy.context.scene.objects):
        if o is not body:
            bpy.data.objects.remove(o)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.seed = 0
    sc.render.bake.margin = BLEED
    world = bpy.data.worlds.new("w")
    sc.world = world
    world.light_settings.distance = 0.4     # MakeHuman units (dm): 4 cm of occlusion

    def one(kind: str, samples: int, emit_coords: bool = False):
        img = bpy.data.images.new(kind, N, N, alpha=True, float_buffer=True)
        img.generated_color = (0, 0, 0, 0)
        mat = bpy.data.materials.new(kind)
        mat.use_nodes = True
        nt = mat.node_tree
        nt.nodes.clear()
        out_n = nt.nodes.new("ShaderNodeOutputMaterial")
        em = nt.nodes.new("ShaderNodeEmission")
        if emit_coords:
            tc = nt.nodes.new("ShaderNodeTexCoord")
            nt.links.new(tc.outputs["Object"], em.inputs["Color"])
        nt.links.new(em.outputs[0], out_n.inputs[0])
        tex = nt.nodes.new("ShaderNodeTexImage")
        tex.image = img
        nt.nodes.active = tex
        body.data.materials.clear()
        body.data.materials.append(mat)
        bpy.context.view_layer.objects.active = body
        body.select_set(True)
        sc.cycles.samples = samples
        bpy.ops.object.bake(type=kind)
        a = np.empty(N * N * 4, np.float32)
        img.pixels.foreach_get(a)
        return np.flipud(a.reshape(N, N, 4))        # Blender's rows run bottom-up

    np.save(out / "ao.npy", one("AO", 64)[..., 0])
    np.save(out / "pos.npy", one("EMIT", 1, emit_coords=True)[..., :3])
    (out / "bake.json").write_text(json.dumps({"N": N, "margin": BLEED, "ao_distance_mh": 0.4,
                                               "ao_samples": 64, "base_obj_sha256":
                                               bc.SOURCES["base.obj"]["sha256"]}) + "\n")


def ensure_bake():
    import numpy as np  # noqa: PLC0415
    meta = BAKE / "bake.json"
    if not (meta.is_file() and json.loads(meta.read_text()).get("N") == N
            and json.loads(meta.read_text()).get("base_obj_sha256") == bc.SOURCES["base.obj"]["sha256"]):
        exe = __import__("os").environ.get("MATTER_BLENDER") or __import__("shutil").which("blender")
        if not exe:
            raise SystemExit("Blender not found (set MATTER_BLENDER or put blender on PATH): the AO bake needs it")
        print(f"baking AO and positions on hm08 in Blender ({exe}) ...")
        subprocess.run([exe, "-b", "--factory-startup", "--python", str(Path(__file__).resolve()),
                        "--", "bake", str(BAKE)], check=True)
    return np.load(BAKE / "ao.npy"), np.load(BAKE / "pos.npy")


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


def compose(tone, reg: dict, ao, pos):
    """The absolute skin colour (linear) for one tone: the probe's v2 recipe (F-SKM-25), with the
    average held to the tone over the skin exactly, the lips' feathered edge included."""
    import numpy as np  # noqa: PLC0415
    cover = np.linalg.norm(pos, axis=-1) > 1e-5    # baked texels (the islands plus the margin)
    m = {k: _grey(f"mpfb_{k}.jpg") for k in MASKS}
    sss = _grey("sss.png")
    sss = np.clip(sss / max(np.percentile(sss[cover], 99), 1e-6), 0, 1)

    # cheeks: two blobs placed from the face texels' own 3D positions (X is lateral)
    F = pos[(m["face"] > 0.5) & cover]
    ext = F.max(0) - F.min(0)
    lat = 0
    up = int(np.argmax(np.where(np.arange(3) == lat, -1, ext)))
    front = 3 - lat - up
    sign = 1.0 if F[:, front].mean() > pos[cover][:, front].mean() else -1.0
    cx, w, h0, hh = F[:, lat].mean(), ext[lat], F[:, up].min(), ext[up]
    cheeks = np.zeros((N, N))
    for side in (-1, 1):
        c = np.zeros(3)
        c[lat] = cx + side * 0.27 * w
        c[up] = h0 + 0.42 * hh
        near = F[(np.abs(F[:, lat] - c[lat]) < 0.05 * w) & (np.abs(F[:, up] - c[up]) < 0.05 * hh)]
        c[front] = (near[:, front].max() if sign > 0 else near[:, front].min()) if len(near) else F[:, front].mean()
        cheeks = np.maximum(cheeks, np.exp(-((np.linalg.norm(pos - c, axis=-1) / (0.2 * w)) ** 2)))
    cheeks *= blur(m["face"], 12)

    n1, n2 = vnoise(pos, 0.25, 7), vnoise(pos, 1.0, 11)
    redness = np.clip(0.3 * sss + 0.4 * blur(m["ears"], 6) + 0.35 * cheeks + 0.25 * blur(m["aureolae"], 4)
                      + 0.05 * n1, 0, 1.2)
    HB = np.array([0.0, 0.42, 0.34])          # haemoglobin: absorbs green and blue
    MEL = np.array([0.88, 0.84, 0.80])        # the darker-skin side of the same tone
    col = tone * np.exp(-redness[..., None] * HB)
    dark = np.clip(1 - ao, 0, 1) * 0.9 + 0.35 * blur(m["eyelids"], 6) + 0.35 * blur(m["aureolae"], 4)
    col = col * (1 - np.clip(dark, 0, 1)[..., None] * (1 - MEL) * 2.2)
    col = col * (1 + 0.035 * n2)[..., None]
    lip = tone * np.array(LIP_RULE)
    lm = np.clip(blur(m["lips"], 5) * 1.15, 0, 1)[..., None]       # feathered: no line at the lips
    lips = lip * (0.92 + 0.08 * n1[..., None])
    # hold the average: over the skin, (s x col)(1 - lm) + lips lm averages to the tone, per channel
    S = reg["Body"]
    s = (tone - (lips * lm)[S].mean(0)) / (col * (1 - lm))[S].mean(0)
    col = col * s * (1 - lm) + lips * lm
    return col, cover


def bleed(lin, covered, px: int):
    """Grow the covered colour ``px`` pixels outward (gen_fit_makehuman.bleed)."""
    import gen_fit_makehuman as fm  # noqa: PLC0415
    return fm.bleed(lin, covered, px)


def calibrate(col, tone, reg: dict, cover):
    """The colour picture -> (the stored map as 8-bit sRGB, the article's base_color_const, the
    numbers). The map is col / tone over its own 99.9th percentile per channel (brightest ~1); the
    constant is the tone over the STORED map's decoded average over the skin, so the article
    renders the tone on average (RD-P21-3)."""
    import numpy as np  # noqa: PLC0415
    S = reg["Body"]
    ratio = col / tone
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
    old = {}
    if PROVENANCE.is_file():
        for line in PROVENANCE.read_text().splitlines():
            if line.startswith("  Fitzpatrick") and ": {" in line:
                old[line.split(":", 1)[0].strip()] = line
    for roman, r in rows.items():
        old[f"Fitzpatrick{roman}"] = (
            f"  Fitzpatrick{roman}: {{made: {r['made']}, tone: {r['tone']}, base_color_const: "
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
        "provenance:",
        "  source: derived",
        "  license: CC0-1.0",
        "  upstream:",
        *[f"    - {{url: {s['url']}, sha256: {s['sha256']}}}" for s in src],
        "  upstream_licence: \"CC0 (MPFB2 LICENSE.ASSETS.md: the hm08 base mesh and its textures)\"",
        "  evidence: tools/converters/fit/gen_skin_maps.py",
        "members:",
        *[old[n] for n in names],
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
    ao = pos = None
    rows = {}
    for roman in a.tones:
        tone = tone_of(roman)
        if a.picture:
            col, cover = from_picture(a.picture, reg)
            made = "contributed"
        else:
            if ao is None:
                ao, pos = ensure_bake()
            col, cover = compose(tone, reg, ao, pos)
            made = "procedural"
        srgb8, _const, st = calibrate(col, tone, reg, cover)
        p = write(roman, srgb8)
        rows[roman] = {"made": made, **st}
        print(f"Fitzpatrick{roman}: {p.relative_to(REPO)}\n  " + json.dumps(st))
        if st["uncovered_islands"]:
            raise SystemExit(f"Fitzpatrick{roman}: {st['uncovered_islands']} island texels left unpainted")
    write_provenance(rows)
    return 0


if __name__ == "__main__":
    if "--" in sys.argv and sys.argv[sys.argv.index("--") + 1] == "bake":
        bake(Path(sys.argv[sys.argv.index("--") + 2]))
    else:
        raise SystemExit(main())
