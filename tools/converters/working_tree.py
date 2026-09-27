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

REPO = Path(__file__).resolve().parents[2]
MATERIALS = REPO / "MatterLibrary" / "materials"
RECIPES = REPO / "tools" / "converters" / "recipes"
RELEASE_CATALOG = REPO / "library" / "releases" / "matterlib-0.1.0.catalog.json"   # read only
VERSION_RE = re.compile(r"^(?P<leaf>.+)_(?P<ver>v\d+)$")
SYSTEM = {"IMRSV_MissingMaterial"}
STATUSES = ("draft", "candidate", "approved", "deprecated", "retired")


def master_of(mtlx: Path) -> str:
    """The article's declared master token, from its imrsv_metadata."""
    root = ET.parse(mtlx).getroot()
    for nd in root.iter("nodedef"):
        if nd.get("node") == "imrsv_metadata":
            for i in nd.iter("input"):
                if i.get("name") == "master_material":
                    return i.get("value", "")
    return ""


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
        domain, klass = rel.split("/")[:2]
        rows.append({
            "id": mid, "version": ver, "status": status_of(mtlx.stem, (mid, ver), release),
            "master": master_of(mtlx),
            "creator_selectable": mtlx.stem not in SYSTEM,
            "domain": domain, "material_class": klass, "identity": mtlx.stem, "mtlx": mtlx,
        })
    return rows
