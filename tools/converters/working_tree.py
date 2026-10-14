"""The working tree's articles, as a person should see them before a release (Phase07 step 7.2).

One list, read by everything that shows unreleased articles to a person:
``tools/releases/serve_to_stage.py`` (USDLiveView and, through the platform's deploy, Studio)
and ``tools/generators/gen_asset_library.py`` (Blender's Asset Browser). Each row carries:

* ``status``: the recipe's ``status`` key (Phase07 D-S); else, for an article in the current
  release (``matterlib-0.1.0``), that release's status; else ``draft``. The lifecycle is
  ``draft → candidate → approved``: candidate = passed USDLiveView and Blender in the parity
  rig; approved = Unreal agrees too. It never lives in the ``.mtlx``, which is frozen once
  released, so promoting an article never changes its file.
* ``master``: the article's own master token (``imrsv_metadata.master_material``), so a
  consumer can route by the article rather than by its class (PlatformDependencies P4).

Standard library only: Blender's bundled Python runs this too.
"""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import groups as G  # Phase15: the groups and Character's taxonomy (same folder)

REPO =Path(__file__).resolve().parents[2]
MATERIALS = REPO / "MatterLibrary" / "materials"
RECIPES = REPO / "tools" / "converters" / "recipes"
RELEASE_CATALOG = REPO / "library" / "releases" / "matterlib-0.1.0.catalog.json"   # read only
VERSION_RE = re.compile(r"^(?P<leaf>.+)_(?P<ver>v\d+)$")
SCALE_RE = re.compile(r"_(s\d+)$")      # the same rule as project_runtime_catalog.SCALE_RE
SYSTEM = {"IMRSV_MissingMaterial"}
STATUSES = ("draft", "candidate", "approved", "deprecated", "retired")


def metadata_of(mtlx: Path) -> dict:
    """Every input of the article's imrsv_metadata block, by name ({} when it has none)."""
    root = ET.parse(mtlx).getroot()
    for nd in root.iter("nodedef"):
        if nd.get("node") == "imrsv_metadata":
            return {i.get("name"): i.get("value", "") for i in nd.iter("input")}
    return {}


def master_of(mtlx: Path) -> str:
    """The article's declared master token, from its imrsv_metadata."""
    return metadata_of(mtlx).get("master_material", "")


def taxonomy_of(mtlx: Path, rel: str) -> dict:
    """The article's group and its place in that group's taxonomy, read from the FILE (Phase15,
    RD-P15-3), never guessed from the domain (F-DS-5). No group means Matter. Its folder must
    agree with what it declares: a disagreement is an error, not a guess."""
    md = metadata_of(mtlx)
    folder = rel.rsplit("/", 1)[0]
    if not md:                                    # a system material with no metadata block
        domain, klass = folder.split("/")[:2]
        md = {"domain": domain, "class": klass}
    group = md.get("group") or G.DEFAULT_GROUP
    errs = G.character_errors(group, md.get("species"), md.get("part"))
    want = G.folder_of(group, md.get("species"), md.get("part"), md.get("domain", ""), md.get("class", ""))
    if not errs and folder != want:
        errs.append(f"it sits in {folder}/ but declares {want}/")
    if errs:
        raise ValueError(f"{mtlx}: " + "; ".join(errs))
    out = {"group": group, "domain": md.get("domain", ""), "material_class": md.get("class", "")}
    if group == G.CHARACTER:
        out.update(species=md["species"], part=md["part"])
    return out


def released() -> dict:
    """(id, version) -> status in the release consumers hold today, so an article already
    released is not shown as a draft just because its recipe predates the status key."""
    cat = json.loads(RELEASE_CATALOG.read_text(encoding="utf-8")) if RELEASE_CATALOG.is_file() else {}
    return {(m["id"], m["version"]): m["status"] for m in cat.get("materials", [])}


def status_of(stem: str, key: tuple, release: dict) -> str:
    """The recipe's status; else the release's, for an article in it; else draft."""
    recipe = RECIPES / f"{stem}.json"
    status = None
    if recipe.is_file():
        status = json.loads(recipe.read_text(encoding="utf-8")).get("status")
    status = status or release.get(key, "draft")
    if status not in STATUSES:
        raise ValueError(f"{recipe}: status {status!r} is not one of {STATUSES}")
    return status


def articles() -> list[dict]:
    """Every .mtlx on disk: id, version, status, master, creator_selectable, domain, class, mtlx."""
    rows, release = [], released()
    for mtlx in sorted(MATERIALS.rglob("*.mtlx")):
        rel = mtlx.relative_to(MATERIALS).with_suffix("").as_posix()
        m = VERSION_RE.match(rel)
        mid, ver = (m["leaf"], m["ver"]) if m else (rel, "v01")
        leaf = mid.rsplit("/", 1)[1]
        scale = SCALE_RE.search(leaf)
        rows.append({
            "display_name": leaf[: scale.start()] if scale else leaf,   # the name, sNN dropped
            "id": mid, "version": ver, "status": status_of(mtlx.stem, (mid, ver), release),
            "master": master_of(mtlx),
            "creator_selectable": mtlx.stem not in SYSTEM,
            **taxonomy_of(mtlx, rel), "identity": mtlx.stem, "mtlx": mtlx,
        })
    return rows
