#!/usr/bin/env python3
"""Check that the compressor's formats agree with the consumers' compressed-role table.

Stage and the Plugin load a role's ``.dds`` only in the BC format their shared role table names for the role's node
(``kCompressedRoles`` in Stage's ``include/shared/IoxMaterialTypes.h``), and refuse any other. The compressor picks a
picture's format from its filename (``compress_textures.classify``). This check walks every article, and for each
picture bound to a node the table names, compares the two. A disagreement means that picture's ``.dds`` would be
refused at load and the PNG used instead.

The library is a producer and its gate does not read a consumer's checkout, so this is not a ``run_all.py`` lane:
run it by hand, or from the consumer's side, with the header's path.

    check_role_formats.py --header <IoxMaterialTypes.h> [--library MatterLibrary]

Exit 0 when every bound picture agrees, or when the header is absent (skipped, said); 1 on any disagreement.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import compress_textures as CT  # noqa: E402

DEFAULT_LIBRARY = HERE.parent.parent / "MatterLibrary"

ROW = re.compile(r'\{\s*CompressedRole::\w+\s*,\s*"(?P<node>\w+)"\s*,\s*CompressedFormat::(?P<bc>BC\d)\s*,')


def read_role_table(header: Path) -> dict[str, str]:
    """Node name -> BC format, for every row of kCompressedRoles that names a node."""
    text = header.read_text()
    start = text.index("kCompressedRoles[]")
    body = text[start:text.index("};", start)]
    return {m["node"]: m["bc"] for m in ROW.finditer(body)}


def bound_pictures(mtlx: Path) -> list[tuple[str, Path]]:
    """(node, picture) for every image node with a non-empty file, its interface input followed."""
    pictures = []
    for graph in ET.parse(mtlx).getroot().iter("nodegraph"):
        interface = {i.get("name"): i.get("value", "") for i in graph.findall("input")}
        for node in graph:
            if node.tag not in ("image", "tiledimage"):
                continue
            file_input = node.find("input[@name='file']")
            if file_input is None:
                continue
            value = file_input.get("value") or interface.get(file_input.get("interfacename", ""), "")
            if value:
                pictures.append((node.get("name"), Path(os.path.normpath(mtlx.parent / value))))
    return pictures


def check_library(library: Path, table: dict[str, str]) -> tuple[int, list[str]]:
    """(pictures checked, problems), over every .mtlx under the library."""
    checked, problems = 0, []
    for mtlx in sorted(library.rglob("*.mtlx")):
        for node, picture in bound_pictures(mtlx):
            expected = table.get(node)
            if expected is None:
                continue
            checked += 1
            where = f"{mtlx.relative_to(library)}: {node} binds {picture.name}"
            try:
                _, got = CT.classify(picture, Path(picture.anchor))
            except CT.ClassifyError:
                problems.append(f"{where}, which the compressor cannot classify; the table wants {expected}")
                continue
            if got != expected:
                problems.append(f"{where}, compressed to {got}; the table wants {expected}")
    return checked, problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--header", type=Path, required=True, help="Stage's include/shared/IoxMaterialTypes.h")
    ap.add_argument("--library", type=Path, default=DEFAULT_LIBRARY, help="the MatterLibrary folder")
    args = ap.parse_args(argv)
    if not args.header.is_file():
        print(f"SKIP: no role table at {args.header}")
        return 0
    table = read_role_table(args.header)
    if not table:
        print(f"FAIL: no kCompressedRoles row read from {args.header}; has the table's layout changed?")
        return 1
    checked, problems = check_library(args.library, table)
    for problem in problems:
        print(f"  [DRIFT] {problem}")
    print(f"{'PASS' if not problems else 'FAIL'}: {checked} bound picture(s) against {len(table)} role(s), "
          f"{len(problems)} disagreement(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
