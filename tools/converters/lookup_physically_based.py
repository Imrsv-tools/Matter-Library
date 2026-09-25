#!/usr/bin/env python3
"""Ground a recipe's constants in the Physically Based database (Phase03, step 3.1).

Physically Based (https://physicallybased.info) is a CC0 database of measured material
values. This tool reads one entry and prints (a) the recipe constants it implies and
(b) the ``sources`` block a recipe carries, so a reader can see where every grounded
number came from (research O6).

    lookup_physically_based.py search <text>          # list matching entry names
    lookup_physically_based.py show "<exact name>"    # constants + a recipe `sources` block

Colours are linear sRGB (``srgb-linear``), which is the library document colour space
(``lin_rec709``). A linear colour above 1.0 (e.g. Gold's red, 1.059) is CLAMPED to 1.0
here and the clamp is recorded in the output, never passed on silently: an albedo above 1
reflects more light than arrives, and the recipe lane refuses it.

Standard library only (one HTTPS GET, no key). ``--file <json>`` reads a saved copy of the
API response instead, for offline use.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request

API = "https://api.physicallybased.info/v2/materials"
COLOR_SPACE = "srgb-linear"


def _load(path: str | None) -> dict:
    if path:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    req = urllib.request.Request(API, headers={"User-Agent": "matter-library-tools"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)


def _linear(entries) -> list | None:
    """Pick the srgb-linear colour from a Physically Based colour list."""
    for e in entries or []:
        if e.get("colorSpace") == COLOR_SPACE:
            return e["color"]
    return None


def _fmt(rgb) -> str:
    return ", ".join(f"{c:g}" for c in rgb)


def ground(entry: dict, header: dict) -> dict:
    """Map one entry to recipe constants + a `sources` record."""
    used: dict = {}
    clamped: list = []

    col = _linear(entry.get("color"))
    if col is not None:
        safe = [min(max(c, 0.0), 1.0) for c in col]
        if safe != col:
            clamped.append({"field": "base_color_const", "from": _fmt(col), "to": _fmt(safe)})
        used["base_color_const"] = _fmt(safe)
    for src, dst in (("metalness", "metalness_const"), ("roughness", "roughness_const"),
                     ("ior", "specular_ior"), ("transmission", "transmission")):
        v = entry.get(src)
        if isinstance(v, (int, float)):
            used[dst] = v

    # Values Physically Based carries that the library has no carrier for yet: named, not used.
    unused = [k for k in ("specularColor", "complexIor", "transmissionDispersion",
                          "volumeCoefficients", "subsurfaceRadius", "thinFilmThickness")
              if k in entry]

    source = {
        "kind": "physicallybased",
        "entry": entry["name"],
        "api": API,
        "schema_version": header.get("schemaVersion"),
        "updated": header.get("updated"),
        "license": header.get("license"),
        "used": used,
    }
    if clamped:
        source["clamped"] = clamped
    if unused:
        source["not_carried"] = unused
    refs = [r["url"] for r in entry.get("references", []) if r.get("url")]
    return {"entry": entry["name"], "description": entry.get("description", ""),
            "category": entry.get("category", []), "references": refs, "source": source}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--file", help="read a saved API response instead of fetching")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="list entries whose name contains the text")
    s.add_argument("text")
    sh = sub.add_parser("show", help="print constants and a recipe `sources` block for one entry")
    sh.add_argument("name")
    args = ap.parse_args(argv)

    data = _load(args.file)
    header, items = data.get("header", {}), data.get("data", [])

    if args.cmd == "search":
        q = args.text.lower()
        hits = [m["name"] for m in items if q in m["name"].lower()
                or any(q in t.lower() for t in m.get("tags", []))]
        print("\n".join(hits) if hits else f"no entry matches {args.text!r}")
        return 0 if hits else 1

    match = [m for m in items if m["name"].lower() == args.name.lower()]
    if not match:
        print(f"no entry named {args.name!r}; try: search <text>", file=sys.stderr)
        return 1
    print(json.dumps(ground(match[0], header), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
