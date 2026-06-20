#!/usr/bin/env python3
"""Author the proof-subset .mtlx from recipes (Phase 53.6 driver).

Reads each JSON recipe in ``tools/converters/recipes/`` (or the paths given on argv) and
writes the assembled OpenPBR 1.39 .mtlx to its ``path`` (relative to MatterLibrary/materials/).
Deterministic: identical recipes -> identical .mtlx.

    build_proof_subset.py [<recipe.json> ...]
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from assemble_mtlx import assemble, MaterialSpec  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent.parent          # Matter-Library/
MATERIALS = ROOT / "MatterLibrary" / "materials"
RECIPES = Path(__file__).resolve().parent / "recipes"


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    recipes = [Path(a) for a in argv] if argv else sorted(RECIPES.glob("*.json"))
    if not recipes:
        print("no recipes found", file=sys.stderr)
        return 2
    for r in recipes:
        d = json.loads(r.read_text(encoding="utf-8"))
        spec = MaterialSpec.from_dict(d)
        out = MATERIALS / d["path"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(assemble(spec), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
