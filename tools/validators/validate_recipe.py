#!/usr/bin/env python3
"""Recipe guards (Phase03 step 3.2) — the `recipe` lane of run_all.py.

A recipe is the only thing an author (human or agent) writes; the assembler generates the
.mtlx from it. The `materials` lane checks the generated article. This lane checks the
RECIPE, before its mistakes can hide inside a valid-looking article:

  G1  strict keys      — an unknown or misspelled key is an error, never silently dropped
  G2  schema           — tools/converters/recipe.schema.json (types, enums, required keys)
  G3  taxonomy         — the domain/class pair is a class in Taxonomy.md
  G5  path agreement   — `path` is <domain>/<class>/<name>.mtlx (and the file is <name>.json)
  G6  plausibility     — albedo, roughness, metalness … inside physical ranges
  G7  layer assignment — every layer texture exists; overlays within the assembler's cap;
                         a mask only where it has something to gate; utility/virtual pure
  G8  fitted picture   — (Phase18) a Character article's own picture fits the part mesh it
                         names: a known mesh of its species and part, a square sRGB RGB PNG at the
                         mesh's map size, covering every UV island (library/meshes/<mesh>_islands.png)
  G9  scale fit        — (Phase19, RD-P19-2) meters_per_tile is exactly its scale tag's length
                         (sUKN: 0.0); the articles off their tag when the rule was made are named

(G4, a class -> master lookup, was dropped in discovery: the article declares its master.)

What a gate cannot judge — whether a layer is RELEVANT to the matter, whether a master
FITS it — is the author's stated rationale plus the maintainer's review. Slider defaults
are not gated either: which default a `Clean_Base` name implies is open (research N8).

    validate_recipe.py [<recipe.json> ...]     # default: every tools/converters/recipes/*.json
"""

from __future__ import annotations

import json
import re
import sys
from dataclasses import fields as dc_fields
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
CONVERTERS = ROOT / "tools" / "converters"
sys.path.insert(0, str(CONVERTERS))
from assemble_mtlx import MAX_OVERLAYS, RECIPE_METADATA_KEYS as METADATA_KEYS, SCALE_TAG_METRES, MaterialSpec, SET_PORTS  # noqa: E402
import groups as G  # noqa: E402  (Phase15: the groups and Character's taxonomy)

SCHEMA_PATH = CONVERTERS / "recipe.schema.json"
ISLANDS = ROOT / "library" / "meshes"          # Phase18: each part mesh's UV islands (make_kits.py)
# G8: the share of any ONE island a picture may leave at its own background colour (the colour
# outside every island) before the island counts as unpainted. Measured 2026-10-15: MakeHuman's eye
# pictures paint their background a grey that is also 0.3 % of each eyeball; a bare island is 100 %.
# FALSE RED: 2026-10-15 — the first G8 counted bare pixels over the whole layout (limit 0.2 %) and
# refused every CC0 eye picture for that grey; it now counts per island (Phase18 18.3).
BARE_ISLAND = 0.5
MATERIALS = ROOT / "MatterLibrary" / "materials"
RECIPES = CONVERTERS / "recipes"

# G3 — mirrors docs/specs/Ontology/Taxonomy.md (the same pattern as LCD_PORTS mirroring
# LCDSchema.md). `atmospheric` is listed there but struck through: out of scope for
# prop-applied matter (Taxonomy.md §Coverage), so no article may use it.
TAXONOMY = {
    "natural": {"stone", "wood", "soil", "mineral"},
    "engineered": {"metal", "glass", "ceramic", "cementitious", "composite"},
    "synthetic": {"plastic", "polymer", "textile", "coating"},
    "environmental": {"sand", "vegetation", "liquid"},
    "utility": {"emissive", "virtual", "energy"},
    "biological": {"tissue", "keratin", "bone"},  # Phase07 (CM1, 2026-09-27)
}

# G6 — physical ranges. Colours are linear reflectances/transmittances; an IOR outside
# [1, 3] is no common solid or liquid (diamond is 2.42). Emission is not bounded.
UNIT_COLOURS = ("base_color_const", "layer2_base_color", "transmission_color", "subsurface_color",
                "coat_color", "fuzz_color")
UNIT_FLOATS = ("roughness_const", "metalness_const", "transmission", "subsurface_weight",
               "opacity_cutoff", "layer_blend_balance", "layer_blend_contrast",
               "layer2_roughness", "layer2_metalness",
               "coat_weight", "coat_roughness", "fuzz_weight", "fuzz_roughness")
SIGNED_UNIT_FLOATS = ("subsurface_scatter_anisotropy",)     # [-1, 1]
IOR_KEYS = ("specular_ior", "coat_ior")
IOR_RANGE = (1.0, 3.0)
# G6 is waived where unphysical is the point: the system fallback (magenta) and the
# utility/virtual references (the UV grid).
G6_EXEMPT_MASTERS = {"system"}
G6_EXEMPT_CLASSES = {("utility", "virtual")}

TEXTURE_KEYS = ("base_color_tex", "roughness_tex", "normal_tex", "metalness_tex", "opacity_tex",
                "layer2_base_color_tex", "layer2_roughness_tex", "layer2_metalness_tex",
                "layer2_normal_tex", "maskset_tex")


def load_schema() -> dict:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


# --- G2: a JSON Schema subset (the keywords recipe.schema.json uses) -------------------
# The schema file is standard JSON Schema, so any validator can read it. The gate checks the
# handful of keywords it uses rather than pull in `jsonschema` (+3 deps, one compiled) for them.
_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool}


def _is_type(v, t: str) -> bool:
    if t == "number":
        return isinstance(v, (int, float)) and not isinstance(v, bool)
    return isinstance(v, _TYPES[t])


def schema_errors(value, schema: dict, root: dict, where: str) -> list:
    if "$ref" in schema:
        schema = root["$defs"][schema["$ref"].rsplit("/", 1)[1]]
    errs = []
    t = schema.get("type")
    if t and not _is_type(value, t):
        return [f"{where}: expected {t}, got {type(value).__name__}"]
    if "enum" in schema and value not in schema["enum"]:
        errs.append(f"{where}: {value!r} is not one of {schema['enum']}")
    if "pattern" in schema and isinstance(value, str) and not re.search(schema["pattern"], value):
        errs.append(f"{where}: {value!r} does not match {schema['pattern']}")
    if "minimum" in schema and _is_type(value, "number") and value < schema["minimum"]:
        errs.append(f"{where}: {value} < minimum {schema['minimum']}")
    # lengths and counts (Phase13 13.2: the words' bounds)
    for key, kind, test in (("minLength", str, lambda n, b: n < b), ("maxLength", str, lambda n, b: n > b),
                            ("minItems", list, lambda n, b: n < b), ("maxItems", list, lambda n, b: n > b)):
        if key in schema and isinstance(value, kind) and test(len(value), schema[key]):
            errs.append(f"{where}: length {len(value)} breaks {key} {schema[key]}")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for k in schema.get("required", []):
            if k not in value:
                errs.append(f"{where}: missing required key {k!r}")
        for k, v in value.items():
            if k in props:
                errs += schema_errors(v, props[k], root, f"{where}.{k}")
            elif schema.get("additionalProperties") is False:
                errs.append(f"{where}: unknown key {k!r}")          # G1
    if isinstance(value, list) and "items" in schema:
        for i, v in enumerate(value):
            errs += schema_errors(v, schema["items"], root, f"{where}[{i}]")
    return errs


def schema_drift(schema: dict) -> list:
    """The schema and MaterialSpec must describe the same keys (else one of them is stale)."""
    spec = {f.name for f in dc_fields(MaterialSpec)} - {"klass"}
    allowed = set(schema["properties"])
    errs = [f"schema drift: MaterialSpec field {k!r} missing from recipe.schema.json"
            for k in sorted(spec - allowed)]
    errs += [f"schema drift: recipe.schema.json key {k!r} is neither a MaterialSpec field nor metadata"
             for k in sorted(allowed - spec - METADATA_KEYS)]
    fits = set(schema["properties"]["fits"]["enum"])          # Phase18: the one list is groups.py's
    if fits != set(G.PART_MESHES):
        errs.append(f"schema drift: fits enum {sorted(fits)} is not groups.PART_MESHES {sorted(G.PART_MESHES)}")
    return errs


# --- G8: a fitted picture against its part mesh's layout (Phase18, RD-P18-5) --------------
def picture_errors(picture: Path, mesh_id: str) -> list:
    """What is wrong with a picture drawn for a part mesh ([] when it fits): its format, its size,
    and whether it covers every UV island (``library/meshes/<mesh>_islands.png``)."""
    import numpy as np  # noqa: PLC0415 (only a fitted article needs them)
    from PIL import Image  # noqa: PLC0415
    mesh = G.PART_MESHES[mesh_id]
    n = mesh["map_size"]
    with Image.open(picture) as im:
        if im.format != "PNG" or im.mode != "RGB":
            return [f"G8 {picture.name} is {im.format} {im.mode}: a fitted picture is an RGB PNG "
                    "(read as sRGB; no alpha)"]
        if im.size != (n, n):
            return [f"G8 {picture.name} is {im.size[0]} x {im.size[1]}: {mesh_id}'s pictures are {n} x {n}"]
        px = np.asarray(im)
    ids = np.asarray(Image.open(ISLANDS / f"{mesh_id}_islands.png")).astype(np.int64)  # 16-bit numbers
    outside = ids == 0
    if not outside.any():
        return []
    colours, counts = np.unique(px[outside].reshape(-1, 3), axis=0, return_counts=True)
    bg = colours[counts.argmax()]
    bare = (px == bg).all(axis=2)
    size = np.bincount(ids.ravel())
    share = np.bincount(ids.ravel(), weights=bare.ravel(), minlength=len(size))[1:] / np.maximum(size[1:], 1)
    empty = [k + 1 for k in np.flatnonzero((share > BARE_ISLAND) & (size[1:] > 0))]
    if empty:
        return [f"G8 {picture.name} leaves {len(empty)} of {int((size[1:] > 0).sum())} UV islands of {mesh_id} "
                f"unpainted (over half at its background colour {tuple(int(c) for c in bg)}): paint every "
                "island of the layout (its kit's _islands.png)"]
    return []


def fitted_errors(d: dict) -> list:
    """G8 for one recipe: a fitted picture and the part mesh it names (Phase18, RD-P18-2)."""
    fits, pic = d.get("fits"), d.get("base_color_map_tex")
    if not fits and not pic:
        return []
    errs = []
    if (d.get("group") or G.DEFAULT_GROUP) != G.CHARACTER:
        errs.append("G8 a fitted picture belongs to a Character article (group character)")
    if bool(fits) != bool(pic):
        return errs + ["G8 base_color_map_tex and fits come together: the picture is drawn for the "
                       "part mesh fits names"]
    if not d.get("base_color_map"):
        errs.append("G8 base_color_map_tex is the base_color_map input's value: declare base_color_map")
    mesh = G.PART_MESHES.get(fits)
    if mesh is None:
        return errs + [f"G8 fits {fits!r} is not a part mesh (have {sorted(G.PART_MESHES)})"]
    if d.get("species") != mesh["species"] or d.get("part") not in mesh["parts"]:
        errs.append(f"G8 {fits} is drawn for {mesh['species']} {mesh['parts']}; this article is "
                    f"{d.get('species')} {d.get('part')}")
    f = ((MATERIALS / d["path"]).parent / pic).resolve()
    if not f.is_file():
        return errs + [f"G8 base_color_map_tex {pic!r} does not exist (resolved from the article's folder)"]
    return errs + picture_errors(f, fits)


# G8 for the shine maps (Phase22 22.1, RD-P22-3): a fitted article's own data map. LINEAR DATA, so
# not the picture's rule: greyscale ("L") for an offset map, at the mesh's map size. No coverage
# test: the map's neutral value (no change) is right on any island and is its background too, so
# an island left neutral is not an unpainted one (F-P22-6).
DATA_MAPS = {"roughness_map_tex": "L"}


def data_map_errors(d: dict) -> list:
    """G8 for one recipe's shine maps: each against the part mesh ``fits`` names."""
    from PIL import Image  # noqa: PLC0415 (only a fitted article needs it)
    errs = []
    for key, mode in DATA_MAPS.items():
        rel = d.get(key)
        if not rel:
            continue
        mesh = G.PART_MESHES.get(d.get("fits"))
        if mesh is None:
            errs.append(f"G8 {key} is drawn for a part mesh: declare fits")
            continue
        f = ((MATERIALS / d["path"]).parent / rel).resolve()
        if not f.is_file():
            errs.append(f"G8 {key} {rel!r} does not exist (resolved from the article's folder)")
            continue
        n = mesh["map_size"]
        with Image.open(f) as im:
            if im.format != "PNG" or im.mode != mode:
                errs.append(f"G8 {f.name} is {im.format} {im.mode}: {key} is a greyscale PNG "
                            "(linear data; no alpha)")
            elif im.size != (n, n):
                errs.append(f"G8 {f.name} is {im.size[0]} x {im.size[1]}: {d['fits']}'s maps are {n} x {n}")
    return errs


# --- G3 / G5 / G6 / G7 -------------------------------------------------------------------
def _colour(s: str) -> list:
    return [float(c) for c in s.split(",")]


def check_recipe(d: dict, schema: dict, file_stem: str | None = None) -> list:
    """Every guard's errors for one recipe dict, each prefixed with its guard id."""
    # G1 = a key the schema does not know; G2 = every other schema violation.
    errs = [f"{'G1' if 'unknown key' in e else 'G2'} {e}"
            for e in schema_errors(d, schema, schema, "recipe")]
    if errs:
        return errs          # later guards assume well-typed keys

    dom, cls, name = d["domain"], d["class"], d["name"]

    # G3 — taxonomy
    if dom not in TAXONOMY or cls not in TAXONOMY[dom]:
        errs.append(f"G3 class {dom}/{cls} is not in Taxonomy.md "
                    f"(the {dom} classes are {sorted(TAXONOMY.get(dom, []))})")

    # G3 — Character's own taxonomy (Phase15, RD-P15-1): a group, and for Character a species and
    # one of its parts. No group means Matter; the group is never read off the domain (F-DS-5).
    grp, species, part = d.get("group"), d.get("species"), d.get("part")
    errs += [f"G3 {e}" for e in G.character_errors(grp, species, part)]

    # G5 — path agreement: the folder says what the file declares (Phase15: a Character article
    # sits under character/<species>/<part>/, RD-P15-8; a Matter one under <domain>/<class>/)
    want = f"{G.folder_of(grp, species, part, dom, cls)}/{name}.mtlx"
    if d["path"] != want:
        errs.append(f"G5 path {d['path']!r} disagrees with its group/taxonomy and name: expected {want!r}")
    if file_stem is not None and file_stem != name:
        errs.append(f"G5 recipe file is {file_stem}.json but its name is {name!r}")

    # G6 — plausibility
    if d["master"] not in G6_EXEMPT_MASTERS and (dom, cls) not in G6_EXEMPT_CLASSES:
        for k in UNIT_COLOURS:
            if k in d and any(not 0.0 <= c <= 1.0 for c in _colour(d[k])):
                errs.append(f"G6 {k} = {d[k]!r}: each channel must be in [0, 1] "
                            "(a surface cannot reflect or transmit more light than arrives)")
        for k in UNIT_FLOATS:
            if k in d and not 0.0 <= d[k] <= 1.0:
                errs.append(f"G6 {k} = {d[k]}: must be in [0, 1]")
        for k in SIGNED_UNIT_FLOATS:
            if k in d and not -1.0 <= d[k] <= 1.0:
                errs.append(f"G6 {k} = {d[k]}: must be in [-1, 1]")
        for k in IOR_KEYS:
            if k in d and not IOR_RANGE[0] <= d[k] <= IOR_RANGE[1]:
                errs.append(f"G6 {k} = {d[k]}: outside {list(IOR_RANGE)}")

    # G7 — layer assignment (and every texture path resolves)
    art_dir = (MATERIALS / d["path"]).parent
    overlays = d.get("overlays", [])
    for k in TEXTURE_KEYS:
        if k in d and not (art_dir / d[k]).resolve().is_file():
            errs.append(f"G7 {k} {d[k]!r} does not exist (resolved from the article's folder)")
    for i, ov in enumerate(overlays, start=1):
        if not (art_dir / ov["texture"]).resolve().is_file():
            errs.append(f"G7 overlay {i} texture {ov['texture']!r} does not exist")
        if ov["density_port"] != f"overlay{i}_density":
            errs.append(f"G7 overlay {i} is driven by {ov['density_port']!r}; expected overlay{i}_density")
        if ov["density_port"] not in d["lcd_ports"]:
            errs.append(f"G7 overlay {i}: {ov['density_port']} is not in lcd_ports (no control, no effect)")
        # Phase10: a deposit's colour is its own slot's Creator port (MasterSet §Overlay semantic)
        if "color_port" in ov:
            if ov["color_port"] != f"overlay{i}_color":
                errs.append(f"G7 overlay {i}'s deposit colour is {ov['color_port']!r}; expected overlay{i}_color")
            if ov["color_port"] not in d["lcd_ports"]:
                errs.append(f"G7 overlay {i}: {ov['color_port']} is not in lcd_ports (the Creator could not change it)")
    deposit_ports = {ov.get("color_port") for ov in overlays}
    for port in d["lcd_ports"]:
        if port.endswith("_color") and port.startswith("overlay") and port not in deposit_ports:
            errs.append(f"G7 {port} is in lcd_ports but no overlay is a deposit with it (a dead control)")
    # Phase12: a port that SETS an author value is declared only on its masters, and starts at
    # the recipe's own field (LCDSchema §Creator-adjustable subset)
    for port in d["lcd_ports"]:
        if port in SET_PORTS:
            fld, masters = SET_PORTS[port]
            if d["master"] not in masters:
                errs.append(f"G7 {port} is in lcd_ports but is a port of {sorted(masters)}, "
                            f"not {d['master']} (a dead control)")
            elif fld not in d:
                errs.append(f"G7 {port} is in lcd_ports but the recipe authors no {fld} (no start value)")
    if len(overlays) > MAX_OVERLAYS:
        errs.append(f"G7 {len(overlays)} overlays; the cap is {MAX_OVERLAYS} (MAX_OVERLAYS, MasterSet.md)")
    has_layer2 = any(k.startswith("layer2_") for k in d)
    if "maskset_tex" in d and not overlays and not has_layer2:
        errs.append("G7 a mask with no overlays and no second layer gates nothing (a dead control)")
    if "maskset_tex" in d and "maskset_blend" not in d["lcd_ports"]:
        errs.append("G7 a mask needs the maskset_blend port (its master strength)")
    if (dom, cls) == ("utility", "virtual") and (overlays or "maskset_tex" in d):
        errs.append("G7 a utility/virtual reference carries no wear layers (it stays pure; C1)")
    errs += fitted_errors(d)
    errs += data_map_errors(d)
    errs += scale_fit_errors(d)
    return errs


# --- G9 ---------------------------------------------------------------------------------
# Phase19 (RD-P19-2), the lead: "We will want to be as firm as we can be that scale fits exactly
# into our scale options ... we should STRONGLY avoid fractions of that... worth noting for any of
# our generation toolsets." An article's tile is exactly its tag's length; an sUKN article tiles
# nothing and authors 0.0. Never stretch a source to fit: re-make it at a scale option's size.
TAG_METRES = SCALE_TAG_METRES          # the assembler's table (Identity.md §Scale tags)
# The articles already off their tag when the rule was made (Phase19 F-P15-1, 2026-10-15), each
# with its recorded size. Each is a redo row in library/wishlist.yaml; a redo that lands on its
# tag must leave this list, and nothing joins it.
OFF_SCALE_KNOWN = {
    "Concrete_BoardFormed_Clean_Base_s1_v01": 2.0,
    "Concrete_Polished_Clean_Base_s1_v01": 3.0,
    "Terrazzo_Polished_Clean_Base_s1_v01": 0.8,
    "Rust_OnSteel_Flaking_Base_s01_v01": 0.5,
    "BeachSand_Dry_Clean_Base_s1_v01": 1.5,
    "OakLeaf_Natural_Clean_Base_s01_v01": 0.12,
    "Marble_Veined_Polished_Base_s01_v01": 0.5,
    "Onyx_Polished_Clean_Base_s01_v01": 0.3,
    "Oak_Natural_Clean_Base_s1_v01": 0.8,
    "Paint_OnMetal_Chipped_Base_s01_v01": 0.3,
    "Lace_Floral_Clean_Base_s01_v01": 0.25,
}


def off_tag(d: dict) -> bool:
    """Whether a recipe's tile is not its scale tag's length (G9's test; sUKN and a missing size are not judged here)."""
    tag, mpt = d.get("scale_tag"), d.get("meters_per_tile")
    return tag in TAG_METRES and mpt is not None and abs(mpt - TAG_METRES[tag]) > 1e-9 * TAG_METRES[tag]


def scale_fit_errors(d: dict) -> list:
    """G9 for one recipe: its meters_per_tile is exactly its scale tag's length (RD-P19-2)."""
    tag, mpt, name = d.get("scale_tag"), d.get("meters_per_tile"), d["name"]
    if tag == "sUKN":
        return [] if not mpt else [f"G9 an sUKN article tiles nothing: meters_per_tile must be 0.0, not {mpt}"]
    if tag not in TAG_METRES or mpt is None:
        return []                       # the tag itself is the grammar's (G2 / the materials lane)
    want = TAG_METRES[tag]
    on_tag = not off_tag(d)
    if name in OFF_SCALE_KNOWN:
        if on_tag:
            return [f"G9 {name} is on its tag now: remove it from OFF_SCALE_KNOWN"]
        if mpt != OFF_SCALE_KNOWN[name]:
            return [f"G9 {name} is a known off-scale article at {OFF_SCALE_KNOWN[name]} m, now {mpt} m: "
                    f"a redo lands on its tag ({want} m), never on another fraction"]
        return []
    if not on_tag:
        return [f"G9 meters_per_tile {mpt} is not its tag's length: {tag} is exactly {want} m "
                "(RD-P19-2). Re-make the source at a scale option's size; never stretch it to fit"]
    return []


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    paths = [Path(a) for a in argv] if argv else sorted(RECIPES.glob("*.json"))
    schema = load_schema()
    ok = True
    for e in schema_drift(schema):
        print(f"  [FAIL] {e}")
        ok = False
    for p in paths:
        errs = check_recipe(json.loads(p.read_text(encoding="utf-8")), schema, p.stem)
        print(f"  [{'FAIL' if errs else 'PASS'}] {p.name}" + "".join(f"\n      {e}" for e in errs))
        ok = ok and not errs
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
