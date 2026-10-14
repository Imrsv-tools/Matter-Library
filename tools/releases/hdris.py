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
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "validators"))
import validate_manifest as vm  # noqa: E402

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
