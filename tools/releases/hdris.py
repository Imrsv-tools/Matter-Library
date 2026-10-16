"""The library's HDRIs, as the dev install and the website's snapshot both read them (Phase14).

One list, one default and one thumbnail recipe, shared by ``serve_to_stage.py`` (the dev
install) and ``build_snapshot.py`` (the site file), so the two never disagree:

* ``on_disk()``: every HDRI file in ``MatterLibrary/hdris/``, each checked by the library's HDRI
  check (``validate_manifest.check_hdri``) and paired with its record in
  ``library/provenance/sources/hdris/`` (its status, credit and tagging). A file that fails the
  check refuses the caller, as a missing payload does.
* ``default()``: the HDRI a new scene starts with, named once in ``library/hdris.yaml`` (A3).
* ``thumbnail(src, dst)``: a 2:1 picture made from the HDRI, tone-mapped; never stored in git
  (RD-MP-6). JPEG or WebP by ``dst``'s extension.
* ``facts(hdri)``: what the HDRI says it is (Phase16, RD-P16-2): id, version, name, licence,
  contributor, its full ``credit`` in the site file's shape (A9), and Phase15's group, when and
  sky. The dev catalog's entry and the header ``stamp`` both take it, so the two cannot disagree.
* ``stamp(src, dst, facts)``: a copy of the HDRI with those facts in its Radiance header, one
  ``MATTER_`` line per fact; the pixels are the source's bytes. Made only in a served copy, never
  in the repo (RD-P16-12). ``read_stamp(path)`` reads them back.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "validators"))
import validate_manifest as vm  # noqa: E402
sys.path.insert(0, str(REPO / "tools" / "converters"))
import groups as G  # noqa: E402  (Phase15: the HDRI group, and when and sky from the record)

HDRIS = REPO / "MatterLibrary" / "hdris"
RECORDS = REPO / "library" / "provenance" / "sources" / "hdris"
SETTINGS = REPO / "library" / "hdris.yaml"
THUMBNAIL = "1024x512"                     # 2:1, the HDRI's own shape
# The tone curve, in linear light, before sRGB: exposure 0.6 into Reinhard (u / (1 + u)), then
# saturation +35 % and a gentle contrast. A plain conversion clips everything above 1.0 (a sun is
# thousands) into a white disc; this matches Poly Haven's own preview (Phase14 14.1), and holds
# across all 59 Pure Skies (14.2).
TONE = ["-fx", "(0.6*u)/(1+0.6*u)", "-colorspace", "sRGB", "-modulate", "100,135",
        "-sigmoidal-contrast", "2,50%"]
QUALITY = "88"

# Phase16 (RD-P16-11): who brought the library's own HDRIs into it. Poly Haven's people stay in
# each one's credit (RD-P16-6). A record naming its own contributor wins (an HDRI someone else
# gives, once the library takes contributions).
CONTRIBUTOR = "MatterBot"
# The credit fields the site file publishes (A9), in its shape.
CREDIT_KEYS = ("source", "source_url", "asset_url", "authors", "sponsors")
# Poly Haven's `info` names the HDRI an edit was made from as one Markdown link (all 59, measured).
EDITED_FROM = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
# The header (RD-P16-2): one line per fact, `MATTER_<FIELD>=<value>`, a field's name mirroring the
# catalog's. Credit fields are `MATTER_CREDIT_<FIELD>`; a field with several values (authors,
# sponsors) repeats its key, each value one JSON object. Readers skip header lines they do not know.
PREFIX = "MATTER_"
SCALARS = ("id", "version", "licence", "contributor", "group", "when", "sky")   # no "name": RD-LBL-1
CREDIT_SCALARS = ("title", "source", "source_url", "asset_url", "edited_from_name", "edited_from_url")
CREDIT_LISTS = {"authors": "AUTHOR", "sponsors": "SPONSOR"}


def on_disk() -> list[dict]:
    """Every HDRI on disk: id, version, identity (the file stem), path and record ({} if none)."""
    files = sorted(p for p in HDRIS.iterdir() if p.is_file()) if HDRIS.is_dir() else []
    out = []
    for hdr in files:
        errs = vm.check_hdri(hdr)
        if errs:
            raise SystemExit(f"{hdr.relative_to(REPO)}: {'; '.join(errs)}")
        hid, version = vm.hdri_id_version(hdr)
        rec_path = RECORDS / f"{hid}.yaml"
        record = (yaml.safe_load(rec_path.read_text(encoding="utf-8")) or {}) if rec_path.is_file() else {}
        out.append({"id": hid, "version": version, "identity": hdr.stem, "path": hdr, "record": record})
    return out


def default(listed: list[dict]) -> str | None:
    """The default HDRI's id; refuses one that names no listed HDRI."""
    name = (yaml.safe_load(SETTINGS.read_text(encoding="utf-8")) or {}).get("default") \
        if SETTINGS.is_file() else None
    if listed and name not in {h["id"] for h in listed}:
        raise SystemExit(f"{SETTINGS.relative_to(REPO)}: default {name!r} names no HDRI on disk")
    return name


def stale(src: Path, dst: Path) -> bool:
    """True when the thumbnail is missing, or older than its HDRI or than this recipe."""
    return not dst.is_file() or dst.stat().st_mtime < max(src.stat().st_mtime, Path(__file__).stat().st_mtime)


def thumbnail(src: Path, dst: Path) -> None:
    """Make dst (.jpg or .webp) from the HDRI src, tone-mapped, written atomically."""
    magick = shutil.which("magick")
    if not magick:
        raise SystemExit("ImageMagick's `magick` is needed to make HDRI thumbnails")
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.stem + ".tmp" + dst.suffix)
    subprocess.run([magick, str(src), "-resize", THUMBNAIL + "!", *TONE, "-quality", QUALITY, str(tmp)],
                   check=True)
    tmp.replace(dst)


# ------------------------------------------------------------------ Phase16: what it says it is

def credit(record: dict) -> dict:
    """The HDRI's credit in the site file's shape (A9): source, its address, the HDRI's page there,
    each author with their role, each sponsor with their link, and the HDRI it was edited from, as
    Poly Haven's Markdown line and (RD-P16-3) as a name and an address. A field the record does not
    hold is left out."""
    c = record.get("credit") or {}
    out = {k: c[k] for k in CREDIT_KEYS if c.get(k)}
    if c.get("name"):      # RD-LBL-1 (2026-10-16): the source's title is credit, never the HDRI's name
        out["title"] = c["name"]
    if c.get("info"):
        out["edited_from"] = c["info"]
        links = EDITED_FROM.findall(c["info"])
        if len(links) == 1:
            out["edited_from_name"], out["edited_from_url"] = links[0]
    return out


def facts(hdri: dict) -> dict:
    """What the HDRI says it is (RD-P16-2), from its record (``on_disk()``'s row): the dev
    catalog's entry and the header stamp both take this, so the two cannot disagree."""
    rec = hdri["record"]
    out = {"id": hdri["id"], "version": hdri["version"]}
    licence = (rec.get("provenance") or {}).get("license")
    if licence:
        out["licence"] = licence
    out["contributor"] = rec.get("contributor") or CONTRIBUTOR
    out["group"] = G.HDRIS
    out.update(G.hdri_taxonomy(rec))
    cr = credit(rec)
    if cr:
        out["credit"] = cr
    return out


def _line(key: str, value) -> str:
    text = value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)
    if "\n" in text or "\r" in text:
        raise ValueError(f"{key}: a header value cannot hold a line break")
    return f"{PREFIX}{key}={text}"


def header_lines(f: dict) -> list[str]:
    """The facts as header lines, in a fixed order. The Markdown `edited_from` line is the site's
    and the catalog's; the header carries its name and address."""
    lines = [_line(k.upper(), f[k]) for k in SCALARS if f.get(k)]
    c = f.get("credit") or {}
    lines += [_line("CREDIT_" + k.upper(), c[k]) for k in CREDIT_SCALARS if c.get(k)]
    for field, key in CREDIT_LISTS.items():
        lines += [_line("CREDIT_" + key, item) for item in c.get(field) or []]
    return lines


def _split(data: bytes) -> tuple[bytes, bytes]:
    """A Radiance file's header (through its last line) and the rest (the blank line, the
    resolution line and the pixels)."""
    end = data.find(b"\n\n")
    if not data.startswith(b"#?") or end < 0:
        raise ValueError("not a Radiance file: no #? signature or no end to the header")
    return data[:end + 1], data[end + 1:]


def stamp(src: Path, dst: Path, f: dict) -> None:
    """Write dst: src with the facts at the end of its header, any earlier MATTER_ lines dropped.
    Everything after the header is src's own bytes. Written atomically."""
    head, rest = _split(src.read_bytes())
    kept = [ln for ln in head.decode("latin-1").splitlines() if not ln.startswith(PREFIX)]
    new = ("\n".join(kept) + "\n").encode("latin-1") + \
        ("\n".join(header_lines(f)) + "\n").encode("utf-8")
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.name + ".tmp")
    tmp.write_bytes(new + rest)
    os.replace(tmp, dst)


def read_stamp(path: Path) -> dict:
    """The facts a stamped header carries, in ``facts()``'s shape ({} for an unstamped file).
    Reads only the header."""
    with open(path, "rb") as fh:
        head = b""
        while b"\n\n" not in head:
            chunk = fh.read(65536)
            if not chunk:
                break
            head += chunk
    head, _ = _split(head)
    out: dict = {}
    scalars = {k.upper(): k for k in SCALARS}
    credit_scalars = {"CREDIT_" + k.upper(): k for k in CREDIT_SCALARS}
    credit_lists = {"CREDIT_" + v: k for k, v in CREDIT_LISTS.items()}
    for raw in head.split(b"\n"):
        if not raw.startswith(PREFIX.encode()):
            continue
        key, _, value = raw.decode("utf-8")[len(PREFIX):].partition("=")
        if key in scalars:
            out[scalars[key]] = value
        elif key in credit_scalars:
            out.setdefault("credit", {})[credit_scalars[key]] = value
        elif key in credit_lists:
            out.setdefault("credit", {}).setdefault(credit_lists[key], []).append(json.loads(value))
    return out


def stamp_stale(src: Path, dst: Path, f: dict) -> bool:
    """True when the stamped copy is missing, older than its HDRI, or says other than the facts
    (the header is compared, so a changed record restamps without any clock)."""
    if not dst.is_file() or dst.stat().st_mtime < src.stat().st_mtime:
        return True
    want = dict(f)
    if "credit" in want:   # the Markdown line is not in the header (header_lines)
        want["credit"] = {k: v for k, v in want["credit"].items() if k != "edited_from"}
    return read_stamp(dst) != want


def main(argv=None) -> int:
    """`hdris.py stamp <id> <out.hdr>`: write one HDRI's stamped copy anywhere (the dev install
    makes all of them; this is for a check on another machine, such as Unreal's importer)."""
    import argparse
    ap = argparse.ArgumentParser(description="Stamp one HDRI's facts into a copy of it (Phase16).")
    sub = ap.add_subparsers(dest="cmd", required=True)
    st = sub.add_parser("stamp", help="write a stamped copy of one HDRI")
    st.add_argument("id", help="the HDRI's id, e.g. IndustrialSunset02_PureSky")
    st.add_argument("out", type=Path, help="where to write the stamped .hdr")
    args = ap.parse_args(argv)
    row = next((h for h in on_disk() if h["id"] == args.id), None)
    if row is None:
        raise SystemExit(f"no HDRI {args.id!r} in {HDRIS}")
    stamp(row["path"], args.out, facts(row))
    print(f"stamped {row['path'].name} -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
