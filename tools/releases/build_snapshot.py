#!/usr/bin/env python3
"""Build (and, on the lead's word, publish) a dev snapshot of the library for its website.

    build_snapshot.py --tag matterlib-0.2.0-dev.1            # build into library/snapshots/<tag>/
    build_snapshot.py --tag matterlib-0.2.0-dev.1 --publish  # then a GitHub pre-release of it

Phase13 13.1 (docs/Planning/Phases/Phase13_MaterialsDescribed.md). Pre-release, so this is NOT a
lockfile release: no stage, freeze or approval, and nothing is written to library/releases/ (the
release gates glob that folder). It lists every article on disk, as the dev catalog does
(working_tree.articles()), and writes, into a git-ignored folder:

  * ``matterlib-<release>.site.json``: the site file (docs/specs/Contract/SiteFile.md, DRAFT);
  * ``<identity>__<tool>[__close].webp``: the parity rig's default pictures of the test scene, per
    tool that ran (never a character render, a sweep picture, a log or a job file: those carry
    local paths, Phase13 F-P13-3);
  * ``<identity>.zip``: the article's .mtlx with every texture it uses, references rewritten to
    ``textures/<name>``, so it opens with no search path (the exporter's complete-portable form);
  * ``<identity>__thumbnail.webp``: each HDRI's 1024 x 512 thumbnail, tone-mapped (Phase14 14.3;
    the HDRI itself is not published: thumbnails and credit only, RD-P14-4);
  * ``<identity>__thumbnail__<view>.webp``: each material's thumbnails, 1024 x 1024, the showcase
    pictures ``tools/thumbnails/make_thumbnails.py`` makes in Cycles, labelled with their renderer
    (Phase17 17.5). A Character material publishes these, its human-context pictures, and still
    never a rig picture. A thumbnail older than its article or the masters is refused, not shipped;
  * ``SHA256SUMS``: every file above, in ``sha256sum -c`` form.

The site file also relays what the site shows side by side (``groups``: Matter, Character and
HDRIs, the list each reads and how each is shown, RD-P14-4) and lists the HDRIs with their full
credit and tagging (``hdris``, ``default_hdri``).

Real fields only: a field the library does not hold yet (a thumbnail, a summary) is left out,
never filled in (SiteFile.md §Absent means not known yet).

``--publish`` runs ``gh release create --prerelease --target <sha>``, the shape unreal/publish.sh
uses, and refuses unless the target commit is on origin/main. Publishing is public and
irreversible: the agent runs it only on the lead's word.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import yaml
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "tools" / "converters"))
sys.path.insert(0, str(REPO / "tools" / "parity"))
import working_tree  # noqa: E402
import groups as G  # noqa: E402  (Phase15: the groups and each group's taxonomy)
from lcd_ports import LCD_MIN_EXCLUSIVE, LCD_PORTS, LCD_RANGES  # noqa: E402
from project_runtime_catalog import derive_entry, derive_hdri_entry  # noqa: E402
sys.path.insert(0, str(HERE))
import hdris as H  # noqa: E402  (the HDRI list, default and thumbnail recipe: Phase14)
sys.path.insert(0, str(REPO / "tools" / "thumbnails"))
import showcase as T  # noqa: E402  (Phase17: the thumbnails' record and its hashes)
import job as jobmod  # noqa: E402  (the rig's article reader: the textures an article names)

PARITY = REPO / "library" / "parity"
THUMBS = REPO / "library" / "thumbnails"
SNAPSHOTS = REPO / "library" / "snapshots"
RECIPES = REPO / "tools" / "converters" / "recipes"
PILOT_LOCK = REPO / "library" / "releases" / "matterlib-0.1.0.lock.yaml"
REPO_SLUG = "Imrsv-tools/Matter-Library"
TAG_RE = re.compile(r"^matterlib-(\d+\.\d+\.\d+-dev\.\d+)$")
SITE_SCHEMA_VERSION = 2              # 1 -> 2 (Phase14 14.3): adds groups[], hdris[] and default_hdri
LICENCE = "CC0-1.0"                  # every article (RD-RO-2)
# Phase16 (RD-P16-4): the source's opening resolution claim (all 59 open with one, in 23 phrasings,
# F-P16-6): "free", the resolution, "unclipped" and "HDRI" in any order, then a separator or a
# joining word. The library's description starts after it; the record keeps the source's words.
RESOLUTION_CLAIM = re.compile(
    r"^(?:(?:free|unclipped|\(unclipped\)|\d+k|hdri)[ ,]*)+(?:[:.\-]\s*|(?:showing|of|with|capturing)\s+)?",
    re.I)
TOOLS = ("storm", "blender", "unreal")
VIEWS = (("wide", "defaults.png"), ("close", "defaults__close.png"))
MAX_ASSETS = 1000                    # GitHub: up to 1000 assets a release
WEBP_QUALITY = 90
DEFAULT_TOKENS = {"Natural", "Clean", "Base"}
# RD-P14-4 (the lead, 2026-10-14): the library relays what sits side by side on the site, and how
# each is shown, so the site builds its navigation from the library. In browse order:
#   rig       - on the parity rig's test scene (the cubes);
#   human     - in a human context (skin on a side face and hands, an eye on an eye), never on
#               the cubes (RD-P13-2); no picture is published until one exists (Thumbnails);
#   thumbnail - the HDRI's own 2:1 picture.
# Phase15 (RD-P15-5): the list lives in tools/converters/groups.py, which the dev catalog reads
# too, and each group names its taxonomy; Character's gains its rows (species, then parts).
# Phase17 (RD-P17-4): in the SITE FILE, Matter is shown by its own thumbnails, as an HDRI is; the
# rig's pictures stay, as evidence. Only here: the dev catalog keeps groups.py's word (`rig`),
# because the dev install does not serve thumbnails (Phase17 Not now, planned).
GROUPS = [g | {"shown": "thumbnail"} if g["id"] == G.MATTER else g for g in G.GROUPS]


class Stale(Exception):
    """A thumbnail made from another article or other masters than the ones on disk."""


def thumbnail_pictures(folder: Path, mtlx: Path, textures) -> list[tuple[str, Path, dict]]:
    """(view, source, record) for each thumbnail ``folder``'s record lists; [] when it has none (not
    made yet: left out, never stood in for). Raises Stale when the record was made from another
    article or other masters than the ones on disk, or a view's picture is missing: the site would
    label a picture of something else. The renderer and scene are the maker's to judge
    (``make_thumbnails.py``); these two are the facts a picture can be wrong about."""
    rec_path = folder / "record.json"
    if not rec_path.is_file():
        return []
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    if rec.get("article_sha256") != T.article_hash(mtlx, textures):
        raise Stale(f"{folder.name}: made from another version of the article")
    if rec.get("masters_sha256") != T.masters_hash():
        raise Stale(f"{folder.name}: made on other Blender masters")
    out = []
    for v in rec["views"]:
        src = folder / f"{v}.png"
        if not src.is_file():
            raise Stale(f"{folder.name}: its record lists {v}.png, which is not there")
        out.append((v, src, rec))
    return out


def renderer_label(rec: dict) -> str:
    r = rec.get("renderer", {})
    return f"{r.get('engine', 'Cycles')} (Blender {r.get('blender', '?')})"


def section(art: dict) -> str:
    """Where a material is browsed: its group, as its own file declares it (Phase15, RD-P15-3).
    Never worked out from the domain (F-DS-5); until Phase15 it was, `biological` -> character."""
    return art["group"]
ZIP_TIME = (2026, 1, 1, 0, 0, 0)     # fixed, so a zip of the same files is byte-identical


# ------------------------------------------------------------------ pure parts (unit-tested)

def label(display_name: str) -> str:
    """A name a person reads, derived from the article's tokens: split the PascalCase, drop the
    default tokens, sentence case. ``Copper_Verdigris_Aged_Base`` -> ``Copper verdigris aged``;
    an acronym or a roman numeral keeps its capitals (``ABS``, ``Fitzpatrick III``)."""
    words = []
    for token in display_name.split("_"):
        if token in DEFAULT_TOKENS:
            continue
        words += re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|\d+", token)
    out = [w if (w.isupper() and (len(w) > 1 or w in "IVX")) else w.lower() for w in words]
    if out and not out[0].isupper():
        out[0] = out[0][0].upper() + out[0][1:]
    return " ".join(out)


SEVERITY = {"ONE-SIDED": 3, "UNEVEN": 2, "moved alike": 1, "no change in any tool": 0}


def control_verdicts(scorecard: dict, job: dict, moved_verdict) -> dict:
    """Per Creator control: the worst of its sweep rows' Moved verdicts, and each row's. A control
    the sweep did not move has no entry (absent, not passed)."""
    port_of = {s["id"]: (s.get("port"), s.get("label", s["id"])) for s in job.get("settings", [])}
    out: dict[str, dict] = {}
    for sid, row in scorecard.get("settings", {}).items():
        port, lab = port_of.get(sid, (None, sid))
        if sid == "defaults" or not port:
            continue
        word, _ = moved_verdict(row.get("moved"), md=False)
        if word == "—":
            continue
        entry = out.setdefault(port, {"verdict": word, "rows": []})
        entry["rows"].append({"setting": lab, "verdict": word})
        if SEVERITY.get(word, 0) > SEVERITY.get(entry["verdict"], 0):
            entry["verdict"] = word
    return out


def rig_pictures(art_dir: Path) -> list[tuple[str, str, Path]]:
    """(tool, view, source) for each default picture of the test scene a tool rendered. Nothing
    else in the folder is ever taken: not the sweep's pictures, logs, job files or scenes."""
    found = []
    for tool in TOOLS:
        for view, name in VIEWS:
            src = art_dir / tool / name
            if src.is_file():
                found.append((tool, view, src))
    return found


def portable(mtlx_text: str, mtlx_dir: Path) -> tuple[str, dict[str, Path]]:
    """The .mtlx with every texture reference rewritten to ``textures/<name>``, and the files to
    pack. Two different files with one name would collide in ``textures/``: refused, not dropped."""
    files: dict[str, Path] = {}
    for ref in sorted(set(re.findall(r'type="filename" value="([^"]+)"', mtlx_text))):
        src = (mtlx_dir / ref).resolve()
        if not src.is_file():
            raise SystemExit(f"missing texture {ref} (from {mtlx_dir})")
        base = src.name
        if base in files and files[base] != src:
            raise SystemExit(f"two textures named {base}: {files[base]} and {src}")
        files[base] = src
        mtlx_text = mtlx_text.replace(f'value="{ref}"', f'value="textures/{base}"')
    return mtlx_text, files


def description(source: str) -> str:
    """The library's description of an HDRI: the source's, without its opening resolution claim
    (RD-P16-4). A description that does not open with one (no resolution in the opening) is kept
    as it is."""
    m = RESOLUTION_CLAIM.match(source)
    if not m or not re.search(r"\d+k", m.group(0), re.I):
        return source
    rest = source[m.end():]
    return rest[:1].upper() + rest[1:]


def hdri_entry(hdri: dict, thumb: str, thumb_sha: str) -> dict:
    """One HDRI's site entry: its identity as the runtime catalog has it, Poly Haven's name as its
    label, and every credit and tag its record holds; one thumbnail; no download (RD-P14-4). A
    field the record does not hold is left out."""
    rec = hdri["record"]
    cat = derive_hdri_entry({"id": hdri["id"], "version": hdri["version"], "status": rec.get("status") or "draft"})
    c = rec.get("credit") or {}
    f = H.facts(hdri)      # Phase16 (RD-P16-2): the same facts the served .hdr is stamped with
    out = {"id": cat["id"], "version": cat["version"], "identity": hdri["identity"],
           "label": c.get("name") or label(cat["display_name"]), "display_name": cat["display_name"],
           "status": cat["status"], "creator_selectable": cat["creator_selectable"],
           **{k: f[k] for k in ("licence", "contributor", "group", "when", "sky") if k in f},
           "pictures": [{"role": "thumbnail", "file": thumb, "sha256": thumb_sha}]}
    if rec.get("description"):
        out["description"] = description(rec["description"])     # RD-P16-4
    if f.get("credit"):    # A9's shape, with edited_from as a name and an address (RD-P16-3)
        out["credit"] = f["credit"]
    for key in ("tagging", "captured"):
        if rec.get(key):
            out[key] = rec[key]
    return out


# ------------------------------------------------------------------ reading the records

def _value(text: str, typ: str):
    nums = [float(v) for v in text.split(",")]
    return nums[0] if typ == "float" else nums


def controls(mtlx: Path) -> list[dict]:
    """The Creator controls the article declares: its nodegraph's interface inputs that are LCD
    ports, with the article's own start value and the port's frozen range."""
    root = ET.parse(mtlx).getroot()
    graph = root.find("nodegraph")
    out = []
    for i in (graph.findall("input") if graph is not None else []):
        name = i.get("name")
        if name not in LCD_PORTS:
            continue
        lo, hi = LCD_RANGES[name]
        rng = {"min": lo, "max": hi}
        if name in LCD_MIN_EXCLUSIVE:
            rng["min_exclusive"] = True
        out.append({"port": name, "name": LCD_PORTS[name][2], "type": i.get("type"),
                    "start": _value(i.get("value"), i.get("type")), "range": rng})
    return out


def metadata(mtlx: Path) -> dict:
    root = ET.parse(mtlx).getroot()
    for nd in root.iter("nodedef"):
        if nd.get("node") == "imrsv_metadata":
            return {i.get("name"): i.get("value") for i in nd.iter("input")}
    return {}


TEXTURES = REPO / "MatterLibrary" / "textures"


def pilot_provenance() -> dict[str, dict]:
    """Each pilot texture's lockfile id (``base/natural/stone/Marble_Veined``) -> its provenance.
    A texture file belongs to the id that prefixes its path under MatterLibrary/textures/."""
    if not PILOT_LOCK.is_file():
        return {}
    lock = yaml.safe_load(PILOT_LOCK.read_text(encoding="utf-8"))
    return {t["id"]: t["provenance"] for t in lock.get("textures", []) if t.get("provenance")}


def _provenance_of(src: Path, pilot: dict) -> dict | None:
    try:
        rel = src.relative_to(TEXTURES).as_posix()
    except ValueError:
        return None
    for tid, prov in pilot.items():
        if rel.startswith(tid + "_"):
            return prov
    return None


def sources(recipe: dict, texture_files: dict[str, Path], pilot: dict) -> list[dict]:
    """The recipe's sources (minus its repo-internal provenance path); for a pilot article with
    none, its textures' lockfile provenance, once per source."""
    if recipe.get("sources"):
        return [{k: v for k, v in s.items() if k != "provenance"} for s in recipe["sources"]]
    seen, out = set(), []
    for src in texture_files.values():
        if "shared/overlays" in src.as_posix():
            continue   # a wear layer is listed under wear_layers, as a recipe's sources never list it
        prov = _provenance_of(src, pilot)
        if not prov:
            continue
        ev = prov.get("evidence")
        url = ev.get("url") if isinstance(ev, dict) else None
        key = (prov.get("source"), url)
        if key in seen:
            continue
        seen.add(key)
        entry = {"kind": str(prov.get("source", "")).lower(), "license": prov.get("license")}
        if url:
            entry["url"] = url
        out.append(entry)
    return out


def wear_layers(recipe: dict) -> list[dict]:
    out = []
    for o in recipe.get("overlays", []):
        layer = {"layer": Path(o["texture"]).stem.split("_")[0], "density_port": o.get("density_port")}
        if o.get("color_port"):
            layer["color_port"] = o["color_port"]
        out.append(layer)
    return out


# ------------------------------------------------------------------ writing

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def write_zip(dest: Path, identity: str, mtlx_text: str, files: dict[str, Path]) -> None:
    tmp = dest.with_name(dest.name + ".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(zipfile.ZipInfo(f"{identity}.mtlx", ZIP_TIME), mtlx_text)
        for base in sorted(files):
            info = zipfile.ZipInfo(f"textures/{base}", ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, files[base].read_bytes())
    os.replace(tmp, dest)


def write_webp(src: Path, dest: Path) -> None:
    buf = io.BytesIO()
    Image.open(src).convert("RGB").save(buf, "WEBP", quality=WEBP_QUALITY, method=6)
    dest.write_bytes(buf.getvalue())


def build(tag: str, out: Path) -> dict:
    from rig import moved_verdict  # the rig's own verdict word; never re-derived here

    m = TAG_RE.match(tag)
    if not m:
        raise SystemExit(f"tag {tag!r} is not matterlib-X.Y.Z-dev.N (NamingConventions.md)")
    release = m[1]
    out.mkdir(parents=True, exist_ok=True)
    for old in out.iterdir():          # a rebuild starts clean; the folder is the snapshot's own
        if old.is_file():
            old.unlink()
    pilot = pilot_provenance()
    materials, assets, stale = [], [], []
    for art in working_tree.articles():
        identity, mtlx = art["identity"], art["mtlx"]
        recipe_path = RECIPES / f"{identity}.json"
        recipe = json.loads(recipe_path.read_text(encoding="utf-8")) if recipe_path.is_file() else {}
        meta = metadata(mtlx)
        entry = derive_entry({"id": art["id"], "version": art["version"], "status": art["status"],
                              "creator_selectable": art["creator_selectable"]})
        rec = {
            "id": entry["id"], "version": entry["version"], "identity": identity,
            "label": recipe.get("label") or label(art["display_name"]),
            "display_name": art["display_name"],
            "section": section(art), "group": art["group"],
            "domain": art["domain"], "material_class": art["material_class"],
            "master": art["master"], "scale": entry["scale"],
            "status": entry["status"], "creator_selectable": entry["creator_selectable"],
            "controls": controls(mtlx),
        }
        # Phase16 (RD-P16-11): who gave it and its licence, read from its own file; a field the
        # file does not declare is left out (not known yet, RD-WS-1).
        rec.update({k: art[k] for k in ("licence", "contributor") if art[k]})
        if art["group"] == G.CHARACTER:                      # Phase15: Character's own taxonomy
            rec.update(species=art["species"], part=art["part"])
        for key in ("summary", "search_words", "origin"):    # the words (13.2), when written
            if recipe.get(key):
                rec[key] = recipe[key]
        if meta.get("meters_per_tile"):
            rec["meters_per_tile"] = float(meta["meters_per_tile"])
        if wear := wear_layers(recipe):
            rec["wear_layers"] = wear
        text, files = portable(mtlx.read_text(encoding="utf-8"), mtlx.parent)
        if src := sources(recipe, files, pilot):
            rec["sources"] = src

        art_dir = PARITY / identity
        # a character material is never shown on the rig's cubes (RD-P13-2): its verdicts are
        # still evidence, but its pictures wait for a human context (Thumbnails, RD-MP-3)
        rendered = rig_pictures(art_dir)
        pics = rendered if rec["section"] == "matter" else []
        if rendered:
            card = art_dir / "scorecard.json"
            parity = {"tools": sorted({t for t, _, _ in rendered}, key=TOOLS.index),
                      "scene": "the rig's test scene"}
            if card.is_file():
                parity["measured"] = dt.date.fromtimestamp(card.stat().st_mtime).isoformat()
                verdicts = control_verdicts(json.loads(card.read_text(encoding="utf-8")),
                                            json.loads((art_dir / "job.json").read_text(encoding="utf-8")),
                                            moved_verdict)
                if verdicts:
                    parity["controls"] = verdicts
            rec["parity"] = parity
        try:
            thumbs = thumbnail_pictures(THUMBS / identity, mtlx, jobmod.Article.read(mtlx).textures.values())
        except Stale as e:
            stale.append(str(e))
            thumbs = []
        if thumbs:                     # Phase17 17.5: the showcase pictures, first
            rec["pictures"] = []
            for view, src, trec in thumbs:
                name = f"{identity}__thumbnail__{view}.webp"
                write_webp(src, out / name)
                rec["pictures"].append({"role": "thumbnail", "view": view, "renderer": renderer_label(trec),
                                        "file": name, "sha256": sha256(out / name)})
                assets.append(name)
        if pics:
            rec.setdefault("pictures", [])
            for tool, view, src in pics:
                name = f"{identity}__{tool}{'__close' if view == 'close' else ''}.webp"
                write_webp(src, out / name)
                rec["pictures"].append({"role": "rig", "tool": tool, "view": view, "file": name,
                                        "sha256": sha256(out / name)})
                assets.append(name)

        zname = f"{identity}.zip"
        write_zip(out / zname, identity, text, files)
        rec["download"] = {"file": zname, "bytes": (out / zname).stat().st_size,
                           "sha256": sha256(out / zname), "textures": len(files)}
        assets.append(zname)
        materials.append(rec)

    if stale:
        raise SystemExit(f"{len(stale)} thumbnail(s) stale, not shipped (re-run "
                         f"`uv run tools/thumbnails/make_thumbnails.py --all-kept`):\n  " + "\n  ".join(stale))
    hdris = []
    listed = H.on_disk()
    for h in listed:     # 14.3: thumbnails and credit only, never the .hdr (RD-P14-4)
        thumb = f"{h['identity']}__thumbnail.webp"
        H.thumbnail(h["path"], out / thumb)
        hdris.append(hdri_entry(h, thumb, sha256(out / thumb)))
        assets.append(thumb)

    site_name = f"matterlib-{release}.site.json"
    site = {"schema_version": SITE_SCHEMA_VERSION, "release": release,
            "made": dt.date.today().isoformat(), "draft": True,
            "groups": GROUPS,
            "materials": sorted(materials, key=lambda r: r["id"])}
    if hdris:
        site["hdris"] = sorted(hdris, key=lambda r: r["id"])
        site["default_hdri"] = H.default(listed)
    (out / site_name).write_text(json.dumps(site, indent=1, sort_keys=True, ensure_ascii=False) + "\n",
                                 encoding="utf-8")
    assets.append(site_name)
    sums = "".join(f"{sha256(out / a)}  {a}\n" for a in sorted(assets))
    (out / "SHA256SUMS").write_text(sums, encoding="utf-8")
    assets.append("SHA256SUMS")
    if len(assets) > MAX_ASSETS:
        raise SystemExit(f"{len(assets)} assets: over GitHub's {MAX_ASSETS} a release (Release Bundle splits)")

    rigged = sum(1 for r in materials if "parity" in r)
    swept = sum(1 for r in materials if "controls" in r.get("parity", {}))
    size = sum((out / a).stat().st_size for a in assets)
    described = sum(1 for r in materials if "summary" in r)
    pictured = sum(1 for r in materials if any(p["role"] == "rig" for p in r.get("pictures", [])))
    thumbed = sum(1 for r in materials if any(p["role"] == "thumbnail" for p in r.get("pictures", [])))
    characters = sum(1 for r in materials if r["section"] == "character")
    notes = (
        f"A **dev snapshot** of the Matter Library, for its website's staging. Not a release: "
        f"nothing here is versioned or approved, and every material shows its own status.\n\n"
        f"- `{site_name}`: every material on disk ({len(materials)}), with what the library knows "
        f"about each. A field it does not know yet is left out, never made up.\n"
        f"- Each material's `group` (and `section`): `matter`, or `character` ({characters}: eyes, hair, "
        f"skin, nails, teeth and mouth, each with its `species` and `part`), read from the material's "
        f"own file; Character is browsed apart and never shown on the rig's cubes.\n"
        f"- Thumbnails: {thumbed} materials, each shown at its best on a subject that suits it, in "
        f"Cycles (Blender), 1024 px, labelled with their renderer: Matter on its own subject (a slab, "
        f"a wall, a pane, a draped cloth, …), Character on the clothed character (half the face, the "
        f"hand, the eye, the lips, the open mouth, the head). Matter's group is now shown by them.\n"
        f"- Pictures: the parity rig's test scene in the tools that ran, for {pictured} Matter materials, "
        f"as evidence. "
        f"A verdict per control for {swept} materials, each with the date it was measured.\n"
        f"- `<material>.zip`: the MaterialX file and every texture it uses.\n"
        f"- `SHA256SUMS`: a digest for every file.\n"
        + (f"- HDRIs: {len(hdris)} lighting pictures from [Poly Haven](https://polyhaven.com), each with "
           f"its thumbnail and its full credit (contributors and their roles, sponsors, Poly Haven's "
           f"tags). The HDRI files themselves are not in this snapshot.\n" if hdris else "")
        + "- `groups`: what the site shows side by side (Matter, Character, HDRIs), how each is shown, "
          "the fields each is browsed by, and Character's rows (Eyes, Hair, Skin, Nails, Teeth, Mouth). "
          "Each HDRI carries its `when` and `sky`, Poly Haven's own words.\n"
        + (f"- Words: a plain name, a one-line summary and search words for {described} materials, "
           f"confirmed by the maintainer.\n\n" if described else "\n")
        + (f"Not yet in it: summaries and search words. " if not described else "")
        + f"Every material is CC0-1.0.\n")
    (out / "NOTES.md").write_text(notes, encoding="utf-8")   # the release body; not an asset
    return {"out": str(out), "materials": len(materials), "character": characters, "hdris": len(hdris),
            "rigged": rigged,
            "pictured": pictured, "thumbnails": thumbed, "swept": swept, "described": described, "assets": len(assets),
            "bytes": size}


# ------------------------------------------------------------------ publishing (lead's word)

def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(REPO), *args], check=True, capture_output=True,
                          text=True).stdout.strip()


def publish(tag: str, out: Path, target: str) -> None:
    sha = git("rev-parse", "--verify", f"{target}^{{commit}}")
    git("fetch", "-q", "origin")
    if subprocess.run(["git", "-C", str(REPO), "merge-base", "--is-ancestor", sha, "origin/main"]).returncode:
        raise SystemExit(f"{sha[:10]} is not on origin/main: push first (the lead's word), then publish")
    files = sorted(p for p in out.iterdir() if p.is_file() and p.name != "NOTES.md")
    if len(files) > MAX_ASSETS:
        raise SystemExit(f"{len(files)} assets: over {MAX_ASSETS}")
    draft = existing_draft(tag)
    if draft is None:
        # gh keeps the release a draft until every asset is up, then publishes it
        subprocess.run(["gh", "release", "create", tag, *map(str, files), "--repo", REPO_SLUG,
                        "--prerelease", "--target", sha, "--title", f"Matter Library dev snapshot {tag}",
                        "--notes-file", str(out / "NOTES.md")], check=True)
        return
    # An interrupted upload (Phase13 13.1: a slow network, a battery) left a draft: upload only
    # what it lacks, then publish it. A file whose upload never finished is not "uploaded" and
    # is sent again.
    have = {a["name"] for a in draft["assets"] if a["state"] == "uploaded"}
    for a in draft["assets"]:
        if a["state"] != "uploaded":
            subprocess.run(["gh", "api", "-X", "DELETE", f"repos/{REPO_SLUG}/releases/assets/{a['id']}"], check=True)
    missing = [str(p) for p in files if p.name not in have]
    print(f"resuming draft {draft['id']}: {len(have)} uploaded, {len(missing)} to send")
    for i in range(0, len(missing), 20):
        subprocess.run(["gh", "release", "upload", tag, *missing[i:i + 20], "--repo", REPO_SLUG], check=True)
    subprocess.run(["gh", "release", "edit", tag, "--repo", REPO_SLUG, "--draft=false", "--prerelease",
                    "--target", sha], check=True)


def existing_draft(tag: str) -> dict | None:
    """The draft release for this tag, if an earlier publish was interrupted."""
    rels = json.loads(subprocess.run(["gh", "api", "--paginate", f"repos/{REPO_SLUG}/releases?per_page=100"],
                                     check=True, capture_output=True, text=True).stdout or "[]")
    for r in rels:
        if r.get("tag_name") == tag:
            if not r.get("draft"):
                raise SystemExit(f"{tag} is already published")
            lines = subprocess.run(
                ["gh", "api", "--paginate", f"repos/{REPO_SLUG}/releases/{r['id']}/assets?per_page=100",
                 "--jq", ".[] | {id, name, state}"], check=True, capture_output=True, text=True).stdout
            r["assets"] = [json.loads(line) for line in lines.splitlines() if line.strip()]
            return r
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--tag", required=True, help="matterlib-X.Y.Z-dev.N")
    ap.add_argument("--out", type=Path, help="default: library/snapshots/<tag>/")
    ap.add_argument("--publish", action="store_true", help="publish the built folder (the lead's word)")
    ap.add_argument("--target", default="HEAD", help="the commit the tag points at (must be on origin/main)")
    args = ap.parse_args(argv)
    out = args.out or SNAPSHOTS / args.tag
    if args.publish:
        if not (out / "SHA256SUMS").is_file():
            raise SystemExit(f"nothing built at {out}: build first")
        publish(args.tag, out, args.target)
        return 0
    print(json.dumps(build(args.tag, out), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
