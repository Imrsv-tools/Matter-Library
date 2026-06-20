#!/usr/bin/env python3
"""Assembler determinism check (Phase 53, §6 + CodingStandards reproducibility).

Same inputs must produce a byte-identical .mtlx. For each spec, assemble twice and assert
the two outputs are byte-identical; optionally assert re-assembly still matches the committed
on-disk .mtlx (regen stability).

    check_determinism.py <spec.json> [<spec.json> ...] [--against <materials-root>]

Exit 0 iff every spec re-assembles byte-stable (and matches disk when --against is given).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "converters"))
from assemble_mtlx import assemble, MaterialSpec  # noqa: E402


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Check the assembler is deterministic.")
    ap.add_argument("specs", nargs="+")
    ap.add_argument("--against", default=None,
                    help="materials root: also compare re-assembly to the on-disk .mtlx")
    args = ap.parse_args(argv)

    all_ok = True
    for spec_path in args.specs:
        d = json.loads(Path(spec_path).read_text(encoding="utf-8"))
        spec = MaterialSpec.from_dict(d)
        a = assemble(spec)
        b = assemble(spec)
        stable = (a == b)
        detail = "byte-stable" if stable else "NON-DETERMINISTIC re-assembly"
        if args.against and stable:
            # on-disk path derives from id-with-scale convention: <root>/<id>.mtlx where the
            # spec's name is the full stem; the recipe carries its own relative path.
            rel = d.get("path")
            if rel:
                disk = Path(args.against) / rel
                if disk.exists():
                    matches = (disk.read_text(encoding="utf-8") == a)
                    stable = stable and matches
                    detail += "; matches-disk" if matches else "; DIFFERS-FROM-DISK"
                else:
                    detail += f"; (no disk file at {disk})"
        print(f"  [{'PASS' if stable else 'FAIL'}] {spec.name}: {detail}")
        all_ok = all_ok and stable

    print("RESULT:", "ALL PASS" if all_ok else "FAILURES")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
