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
from assemble_mtlx import MAX_OVERLAYS, RECIPE_METADATA_KEYS as METADATA_KEYS, MaterialSpec  # noqa: E402

SCHEMA_PATH = CONVERTERS / "recipe.schema.json"
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
}

# G6 — physical ranges. Colours are linear reflectances/transmittances; an IOR outside
# [1, 3] is no common solid or liquid (diamond is 2.42). Emission is not bounded.
UNIT_COLOURS = ("base_color_const", "layer2_base_color", "transmission_color", "subsurface_color")
UNIT_FLOATS = ("roughness_const", "metalness_const", "transmission", "subsurface_weight",
               "opacity_cutoff", "layer_blend_balance", "layer_blend_contrast",
               "layer2_roughness", "layer2_metalness")
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

    # G5 — path agreement
    want = f"{dom}/{cls}/{name}.mtlx"
    if d["path"] != want:
        errs.append(f"G5 path {d['path']!r} disagrees with domain/class/name: expected {want!r}")
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
        if "specular_ior" in d and not IOR_RANGE[0] <= d["specular_ior"] <= IOR_RANGE[1]:
            errs.append(f"G6 specular_ior = {d['specular_ior']}: outside {list(IOR_RANGE)}")

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
    if len(overlays) > MAX_OVERLAYS:
        errs.append(f"G7 {len(overlays)} overlays; the cap is {MAX_OVERLAYS} (MAX_OVERLAYS, MasterSet.md)")
    has_layer2 = any(k.startswith("layer2_") for k in d)
    if "maskset_tex" in d and not overlays and not has_layer2:
        errs.append("G7 a mask with no overlays and no second layer gates nothing (a dead control)")
    if "maskset_tex" in d and "maskset_blend" not in d["lcd_ports"]:
        errs.append("G7 a mask needs the maskset_blend port (its master strength)")
    if (dom, cls) == ("utility", "virtual") and (overlays or "maskset_tex" in d):
        errs.append("G7 a utility/virtual reference carries no wear layers (it stays pure; C1)")
    return errs


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
