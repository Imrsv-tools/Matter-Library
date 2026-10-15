"""The library's three groups and each group's own taxonomy (Phase15, RD-DS-1, RD-P15-1).

One place, read by everything that files, checks or publishes an entry: the recipe validator,
the working-tree reader, the dev catalog (``serve_to_stage.py``), the site file
(``build_snapshot.py``) and Blender's Asset Browser (``gen_asset_library.py``).

* **Matter** is browsed by Domain, then Class (``docs/specs/Ontology/Taxonomy.md``).
* **Character** is browsed by species, then part. Humanoid today; its parts are the six rows the
  lead ruled for the website (Eyes, Hair, Skin, Nails, Teeth, Mouth). A Character article lives at
  ``materials/character/<species>/<part>/`` (RD-P15-8) and says so in its own ``imrsv_metadata``.
* **HDRIs** are browsed by *when* and *sky*: Poly Haven's own words, read from each HDRI's record.

**A file never has its group guessed from its domain** (F-DS-5). An ``.mtlx`` with no ``group``
in its metadata is Matter, as an entry with no ``creator_selectable`` is selectable (RD-P15-3).

Standard library only: Blender's bundled Python imports this too.
"""

from __future__ import annotations

MATTER, CHARACTER, HDRIS = "matter", "character", "hdris"
DEFAULT_GROUP = MATTER

# The folder every Character article sits under, below MatterLibrary/materials/ (RD-P15-8).
CHARACTER_FOLDER = "character"

# species -> its parts, in browse order, each with the label a person reads (RD-P15-1).
CHARACTER_TAXONOMY = {
    "humanoid": [
        ("eyes", "Eyes"), ("hair", "Hair"), ("skin", "Skin"),
        ("nails", "Nails"), ("teeth", "Teeth"), ("mouth", "Mouth"),
    ],
}
SPECIES_LABELS = {"humanoid": "Humanoid"}

# The PART MESHES (Phase18, RD-P18-1): the mesh a Character article's picture is drawn for, named
# `<Family>_<Mesh>_vNN` and versioned. **A version is a UV layout**: a new layout is a new vNN, and
# a new shape on the same layout is the same version (F-P18-4: MakeHuman's six teeth share one).
# A fitted article declares the one it fits (`fits`, RD-P18-2), and its picture is checked against
# that layout's islands (`library/meshes/<id>_islands.png`, RD-P18-5).
#   source     the rig's mesh (tools/parity/scene/build_character.py MESHES), pinned there by sha256
#   rig_parts  the parts the rig and Studio split it into, each bound to an article
#   parts      the Character rows its parts are browsed under
#   map_size   the picture's size, in pixels (square)
#   uv_sha256  the layout's hash (tools/converters/fit/make_kits.py layout_sha256); a kit refuses
#              any other, since another layout is another mesh version
PART_MESHES = {
    "MakeHuman_Body_v01": {
        "family": "makehuman", "species": "humanoid", "source": "body",
        "what": "the whole body's skin (hm08), with the lips and the nails",
        "rig_parts": ["Lips", "Nails", "Body"], "parts": ["skin", "mouth", "nails"], "map_size": 2048,
        "uv_sha256": "f2ec4e33d9371e1dfb0f3d857c2377b4be5d0de0554d8cdf8f29837224591b2f"},
    "MakeHuman_Eyes_v01": {
        "family": "makehuman", "species": "humanoid", "source": "eyes",
        "what": "both eyeballs (MakeHuman's high-poly eye): the white, the iris and the pupil",
        "rig_parts": ["Cornea", "Pupil", "Iris", "Sclera"], "parts": ["eyes"], "map_size": 1024,
        "uv_sha256": "3b7f8d157b7c5baf6b5dd71428d5e68f17d4e572ad2912f33231bd4ba7043d65"},
    "MakeHuman_Teeth_v01": {
        "family": "makehuman", "species": "humanoid", "source": "teeth",
        "what": "a set of teeth with its gums (MakeHuman's teeth_base and its five shapes)",
        "rig_parts": ["Gums", "Teeth"], "parts": ["teeth", "mouth"], "map_size": 2048,
        "uv_sha256": "51edbff6914b869d16a3e53628ae20222b07bf5687b890d558cd734f8021e206"},
    "MakeHuman_Tongue_v01": {
        "family": "makehuman", "species": "humanoid", "source": "tongue",
        "what": "the tongue (MakeHuman's tongue01)",
        "rig_parts": ["Tongue"], "parts": ["mouth"], "map_size": 1024,
        "uv_sha256": "7b717e2ef4de7ada6967d5345e268555eb847e590fe636e773d6392b38548755"},
}

# What the groups are, in browse order: the site file's list (SiteFile.md §Groups), which the dev
# catalog carries too (RD-P15-5). `taxonomy` names the fields a group is browsed by, in order;
# Character's `rows` are its parts' labels and order, per species.
GROUPS = [
    # Phase17 (RD-P17-4, PIC-Q2): Matter is shown by its own thumbnails, in the site file and the
    # dev catalog alike (until then `rig`, the parity rig's cubes, whose pictures stay as evidence)
    {"id": MATTER, "label": "Matter", "list": "materials", "section": MATTER, "shown": "thumbnail",
     "taxonomy": ["domain", "material_class"]},
    {"id": CHARACTER, "label": "Character", "list": "materials", "section": CHARACTER, "shown": "human",
     "taxonomy": ["species", "part"],
     "rows": [{"species": sp, "label": SPECIES_LABELS[sp],
               "parts": [{"id": p, "label": lab} for p, lab in parts]}
              for sp, parts in CHARACTER_TAXONOMY.items()]},
    {"id": HDRIS, "label": "HDRIs", "list": "hdris", "shown": "thumbnail",
     "taxonomy": ["when", "sky"]},
]


# HDRIs: *when* is Poly Haven's time category (exactly one per HDRI, measured on all 59,
# 2026-10-14); *sky* is its `weather` attribute. The words stay Poly Haven's; merging them into
# fewer rows (Day, Cloudy) is a consumer's presentation (RD-P15-4).
HDRI_WHEN = ("sunrise-sunset", "morning-afternoon", "midday", "night")


def hdri_taxonomy(record: dict) -> dict:
    """An HDRI's `when` and `sky`, read from its record's tagging. A value the record does not
    hold is left out, never guessed (SiteFile.md §The rule)."""
    tagging = record.get("tagging") or {}
    when = [c for c in HDRI_WHEN if c in (tagging.get("categories") or [])]
    sky = (tagging.get("attributes") or {}).get("weather")
    out = {}
    if len(when) == 1:
        out["when"] = when[0]
    if sky:
        out["sky"] = sky
    return out


def parts_of(species: str) -> list[str]:
    """The part ids of a species, in browse order ([] for an unknown species)."""
    return [p for p, _ in CHARACTER_TAXONOMY.get(species, [])]


def character_errors(group: str | None, species: str | None, part: str | None) -> list[str]:
    """What is wrong with an article's declared group and Character taxonomy ([] when right)."""
    g = group or DEFAULT_GROUP
    if g not in (MATTER, CHARACTER):
        return [f"group {g!r} is not one of {[MATTER, CHARACTER]} (an HDRI is not a material)"]
    if g == MATTER:
        return ([f"species/part are Character's taxonomy; a Matter article declares neither"]
                if species or part else [])
    errs = []
    if species not in CHARACTER_TAXONOMY:
        errs.append(f"species {species!r} is not one of {sorted(CHARACTER_TAXONOMY)}")
    elif part not in parts_of(species):
        errs.append(f"part {part!r} is not one of {species}'s parts {parts_of(species)}")
    return errs


def taxonomy_path(entry: dict) -> list[str]:
    """An article's place to browse, as the labels a person reads: its group, then that group's
    own taxonomy (["Matter", "Engineered", "Metal"], ["Character", "Humanoid", "Skin"])."""
    if entry.get("group", DEFAULT_GROUP) == CHARACTER:
        sp = entry["species"]
        return ["Character", SPECIES_LABELS[sp], dict(CHARACTER_TAXONOMY[sp])[entry["part"]]]
    return ["Matter", entry["domain"].capitalize(), entry["material_class"].capitalize()]


def folder_of(group: str | None, species: str | None, part: str | None,
              domain: str, klass: str) -> str:
    """The folder an article belongs in, below MatterLibrary/materials/."""
    if (group or DEFAULT_GROUP) == CHARACTER:
        return f"{CHARACTER_FOLDER}/{species}/{part}"
    return f"{domain}/{klass}"
