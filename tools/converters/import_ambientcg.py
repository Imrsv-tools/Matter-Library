#!/usr/bin/env python3
"""Import one ambientCG material as a Matter base texture set (Phase03, step 3.4).

ambientCG (https://ambientcg.com) publishes every asset under CC0 1.0. This is the ONLY
third-party texture source this tool fetches from: the host is fixed below, so a non-CC0
pixel cannot arrive through it (the phase's residual risk, Brief §Risk lane).

    import_ambientcg.py search <text>                          # candidate asset ids
    import_ambientcg.py info <AssetId>                         # tags, maps, physical size
    import_ambientcg.py import <AssetId> --set <SetName> --slot <domain>/<class>
                            --scale <sNN> --article <ArticleStem>

`import` does, for the asset's 1K-PNG zip:
  1. maps its channels onto the library's: Color -> basecolor, Roughness -> roughness,
     NormalGL -> normal (the library's convention: discovery P1), Metalness -> metalness,
     Opacity -> opacity. Displacement, AO and NormalDX are not carried, and are named.
  2. writes MatterLibrary/textures/base/<domain>/<class>/<SetName>_<channel>_<sNN>.png, flat
     in the class folder (the shipped layout). A map already 1024 px and in the right mode is
     copied VERBATIM, so it stays byte-identical to the download; anything else is resized
     to 1024 (Lanczos) and the fact is printed.
  3. records provenance (lead ruling Q2 = A) at
     library/provenance/sources/base/<domain>/<class>/<SetName>.yaml: the `provenance:` block a
     release lock will carry, with the shipped-source-set evidence (source_provenance.py).
  4. adds a row to CREDITS.md §Texture sources.
  5. prints `meters_per_tile` from the asset's physical size, for the recipe.

It refuses to overwrite any existing file. Standard library + Pillow + PyYAML only.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "tools" / "validators"))
import source_provenance as sp  # noqa: E402

HOST = "https://ambientcg.com"          # the one allowlisted source (CC0 1.0)
API = f"{HOST}/api/v2/full_json"
SIZE = 1024
CHANNELS = {  # ambientCG suffix -> (library channel, PIL mode)
    "Color": ("basecolor", "RGB"),
    "Roughness": ("roughness", "L"),
    "NormalGL": ("normal", "RGB"),
    "Metalness": ("metalness", "L"),
    "Opacity": ("opacity", "L"),
}
SCALE_TAGS = {"s0001", "s001", "s01", "s1", "s10", "s100", "sUKN"}


def _get(url: str) -> bytes:
    if not url.startswith(HOST + "/"):
        raise SystemExit(f"refusing to fetch outside {HOST}: {url}")
    req = urllib.request.Request(url, headers={"User-Agent": "matter-library-tools"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def _api(**params) -> list:
    q = urllib.parse.urlencode({"type": "Material", "include": "tagData,displayData,dimensionsData", **params})
    return json.loads(_get(f"{API}?{q}")).get("foundAssets", [])


def cmd_search(text: str) -> int:
    for a in _api(q=text, limit=30):
        dims = f"{a.get('dimensionX', '?')}x{a.get('dimensionY', '?')} cm"
        print(f"{a['assetId']:<14} {dims:<12} {', '.join(a.get('tags', [])[:10])}")
    return 0


def _asset(asset_id: str) -> dict:
    found = _api(id=asset_id)
    if not found:
        raise SystemExit(f"no ambientCG material {asset_id!r}")
    return found[0]


def cmd_info(asset_id: str) -> int:
    a = _asset(asset_id)
    print(f"{a['assetId']}  {HOST}/view?id={a['assetId']}")
    print(f"  tags:  {', '.join(a.get('tags', []))}")
    print(f"  maps:  {', '.join(a.get('maps', []))}")
    print(f"  size:  {a.get('dimensionX')} x {a.get('dimensionY')} cm "
          f"(meters_per_tile {(a.get('dimensionX') or 0) / 100:g})")
    return 0


def cmd_import(asset_id: str, set_name: str, slot: str, scale: str, article: str) -> int:
    if scale not in SCALE_TAGS:
        raise SystemExit(f"--scale must be one of {sorted(SCALE_TAGS)}")
    a = _asset(asset_id)
    tex_dir = ROOT / "MatterLibrary" / "textures" / "base" / slot
    prov = ROOT / "library" / "provenance" / "sources" / "base" / slot / f"{set_name}.yaml"
    if prov.exists() or list(tex_dir.glob(f"{set_name}_*.png")):
        raise SystemExit(f"refusing to overwrite: {set_name} already exists in {tex_dir} or {prov}")

    data = _get(f"{HOST}/get?file={asset_id}_1K-PNG.zip")
    written, skipped = [], []
    with tempfile.TemporaryDirectory() as tmp, zipfile.ZipFile(io.BytesIO(data)) as zf:
        zf.extractall(tmp)
        for src in sorted(Path(tmp).glob("*.png")):
            suffix = src.stem.split("_")[-1]
            if src.stem == asset_id:
                continue                                          # the zip's preview image
            if suffix not in CHANNELS:
                skipped.append(suffix)
                continue
            channel, mode = CHANNELS[suffix]
            dst = tex_dir / f"{set_name}_{channel}_{scale}.png"
            dst.parent.mkdir(parents=True, exist_ok=True)
            with Image.open(src) as im:
                if im.size == (SIZE, SIZE) and im.mode == mode:
                    shutil.copyfile(src, dst)                     # verbatim: byte-identical
                    how = "copied verbatim"
                else:
                    im.convert(mode).resize((SIZE, SIZE), Image.LANCZOS).save(dst, "PNG", optimize=True)
                    how = f"converted from {im.size[0]}x{im.size[1]} {im.mode}"
            written.append(dst)
            print(f"  {suffix:<10} -> {dst.relative_to(ROOT)}  ({how})")
    if not written:
        raise SystemExit(f"{asset_id}: no usable maps in the 1K-PNG zip")
    if skipped:
        print(f"  not carried: {', '.join(sorted(set(skipped)))}")

    tex_id = f"base/{slot}/{set_name}"
    ev = sp.compute_evidence(ROOT, tex_id, f"{HOST}/view?id={asset_id}")
    prov.parent.mkdir(parents=True, exist_ok=True)
    prov.write_text(
        "# Draft provenance for one texture set (Phase03, lead ruling Q2 = A).\n"
        "# Holds the `provenance:` block a release lock will carry when this texture is promoted.\n"
        + yaml.safe_dump({"id": tex_id, "version": "v01",
                          "provenance": {"source": "ambientCG", "license": "CC0-1.0", "evidence": ev}},
                         sort_keys=False, width=200), encoding="utf-8")
    print(f"  provenance -> {prov.relative_to(ROOT)}")

    credits = ROOT / "CREDITS.md"
    anchor = "\nEvery other texture is **procedural**"
    text = credits.read_text(encoding="utf-8")
    if text.count(anchor) != 1:
        raise SystemExit("CREDITS.md: texture-source table anchor not found; add the row by hand")
    used_for = re.sub(r"_v\d+$", "", article)                   # the table lists ids without _vNN
    row = f"| [ambientCG]({HOST}): [{asset_id}]({HOST}/view?id={asset_id}) | CC0-1.0 | `{used_for}` |\n"
    # the table's last row ends with "|\n", then a blank line, then the anchor sentence
    credits.write_text(text.replace("|\n" + anchor, "|\n" + row + anchor, 1), encoding="utf-8")
    print(f"  CREDITS.md row added for {asset_id}")
    print(f"  meters_per_tile {(a.get('dimensionX') or 0) / 100:g}  (asset is "
          f"{a.get('dimensionX')} x {a.get('dimensionY')} cm)")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Import an ambientCG material as a Matter base texture set.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("search").add_argument("text")
    sub.add_parser("info").add_argument("asset_id")
    im = sub.add_parser("import")
    im.add_argument("asset_id")
    im.add_argument("--set", required=True, dest="set_name", help="library set name, e.g. Oak_Natural")
    im.add_argument("--slot", required=True, help="<domain>/<class>, e.g. natural/wood")
    im.add_argument("--scale", required=True, help="scale tag, e.g. s1")
    im.add_argument("--article", required=True, help="the article stem it is for (CREDITS row)")
    args = ap.parse_args(argv)
    if args.cmd == "search":
        return cmd_search(args.text)
    if args.cmd == "info":
        return cmd_info(args.asset_id)
    return cmd_import(args.asset_id, args.set_name, args.slot, args.scale, args.article)


if __name__ == "__main__":
    raise SystemExit(main())
