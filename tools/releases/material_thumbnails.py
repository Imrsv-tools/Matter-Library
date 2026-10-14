"""Each material's thumbnail in the dev install (Phase17; the platform's ask, research
``261014_R_PlatformMaterialPicturesAsks.md`` A1 - A3).

One picture per material, its first view (Matter's ``card``; a Character material's first
human-context view, in ``showcase.CHARACTER_VIEWS`` order), served as a baseline JPEG of
``SERVED`` px at ``thumbnails/materials/<identity>.jpg`` and named by the dev catalog's
``thumbnail_path``, the way an HDRI's is (``thumbnails/hdris/``). A material with no thumbnail
has no field.

**Where the picture comes from, on any machine** (A3):

1. this machine's master, ``library/thumbnails/<identity>/<view>.png``, when its record was made
   from the article and the Blender masters now on disk; else
2. the newest published dev snapshot's picture (``matterlib-*-dev.*`` on GitHub), downloaded once
   into ``library/thumbnails/_published/<tag>/`` and checked against the site file's ``sha256``.

Offline with no master, a material simply has no picture yet; the serve goes on.
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import sys
import urllib.request
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "tools" / "thumbnails"))
sys.path.insert(0, str(REPO / "tools" / "parity"))
import showcase as T  # noqa: E402  (the record and its hashes)
import job as jobmod  # noqa: E402  (the textures an article names)

SERVED = 512                  # px square: the consumer draws it at ~200 px, many at once (PIC-F4)
JPEG_QUALITY = 90
FOLDER = "thumbnails/materials"
THUMBS = REPO / "library" / "thumbnails"
PUBLISHED = THUMBS / "_published"
REPO_SLUG = "Imrsv-tools/Matter-Library"
DEV_TAG = re.compile(r"^matterlib-\d+\.\d+\.\d+-dev\.\d+$")
VIEW_ORDER = tuple(T.VIEW_ORDER) + tuple(T.CHARACTER_VIEWS)


def first_view(views) -> str | None:
    """The view a material is shown by: the first in ``VIEW_ORDER`` it has."""
    return next((v for v in VIEW_ORDER if v in views), None)


def local_source(identity: str, mtlx: Path) -> Path | None:
    """This machine's master of the first view, when its record matches the article and masters."""
    folder = THUMBS / identity
    rec_path = folder / "record.json"
    if not rec_path.is_file():
        return None
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    textures = jobmod.Article.read(mtlx).textures.values()
    if rec.get("article_sha256") != T.article_hash(mtlx, textures) or rec.get("masters_sha256") != T.masters_hash():
        return None
    v = first_view(rec.get("views", []))
    src = folder / f"{v}.png" if v else None
    return src if src and src.is_file() else None


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "matter-library-serve"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def published_sources() -> tuple[str | None, dict[str, Path]]:
    """(tag, identity -> cached picture) from the newest published dev snapshot. Each picture is
    downloaded once and refused unless it matches the site file's sha256. (None, {}) offline."""
    try:
        rels = json.loads(_get(f"https://api.github.com/repos/{REPO_SLUG}/releases?per_page=30"))
    except OSError as e:
        print(f"thumbnails: no published snapshot reachable ({e}); this machine's masters only")
        return None, {}
    rels = [r for r in rels if DEV_TAG.match(r["tag_name"]) and not r["draft"]]
    if not rels:
        return None, {}
    rel = max(rels, key=lambda r: r["created_at"])
    tag, assets = rel["tag_name"], {a["name"]: a["browser_download_url"] for a in rel["assets"]}
    cache = PUBLISHED / tag
    cache.mkdir(parents=True, exist_ok=True)
    site_name = f"{tag}.site.json"
    site_path = cache / site_name
    if not site_path.is_file():
        site_path.write_bytes(_get(assets[site_name]))
    site = json.loads(site_path.read_text(encoding="utf-8"))
    out = {}
    for m in site["materials"]:
        pics = {p["view"]: p for p in m.get("pictures", []) if p["role"] == "thumbnail"}
        v = first_view(pics)
        if not v:
            continue
        p = pics[v]
        dst = cache / p["file"]
        if not dst.is_file() or hashlib.sha256(dst.read_bytes()).hexdigest() != p["sha256"]:
            if p["file"] not in assets:
                continue
            data = _get(assets[p["file"]])
            if hashlib.sha256(data).hexdigest() != p["sha256"]:
                print(f"thumbnails: {p['file']} does not match its sha256 in {site_name}; skipped")
                continue
            dst.write_bytes(data)
        out[m["identity"]] = dst
    return tag, out


def write_jpeg(src: Path, dst: Path) -> None:
    im = Image.open(src).convert("RGB")
    if im.size != (SERVED, SERVED):
        im = im.resize((SERVED, SERVED), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=False)
    tmp = dst.with_name(dst.name + ".tmp")
    tmp.write_bytes(buf.getvalue())
    tmp.replace(dst)


def serve(dev: Path, entries: list[dict], source_root: Path) -> dict:
    """Put each material's thumbnail in ``dev/thumbnails/materials/`` and name it on its entry
    (``thumbnail_path``), remade only when its source is newer. Removes a served picture no material
    has any more. Returns counts for the log."""
    out = dev / FOLDER
    out.mkdir(parents=True, exist_ok=True)
    local, tag, published = {}, None, None
    for e in entries:
        identity = Path(e["payload_path"]).stem
        src = local_source(identity, source_root / e["payload_path"])
        if src:
            local[identity] = src
    want, made, counts = set(), 0, {"local": 0, "published": 0, "none": 0}
    for e in entries:
        identity = Path(e["payload_path"]).stem
        src = local.get(identity)
        if src:
            counts["local"] += 1
        else:
            if published is None:
                tag, published = published_sources()
            src = published.get(identity)
            counts["published" if src else "none"] += 1
        if not src:
            continue
        dst = out / f"{identity}.jpg"
        want.add(dst.name)
        if not dst.is_file() or dst.stat().st_mtime < src.stat().st_mtime:
            write_jpeg(src, dst)
            made += 1
        e["thumbnail_path"] = f"{FOLDER}/{identity}.jpg"
    for p in out.iterdir():
        if p.is_file() and p.name not in want:
            p.unlink()
    return counts | {"made": made, "tag": tag}
