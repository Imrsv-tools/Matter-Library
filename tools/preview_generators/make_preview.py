#!/usr/bin/env python3
"""usdview parity-preview generator (Phase 53 fixture; seeds Phase-60 usdrecord baselines).

Given a Matter material .mtlx, emit a standalone preview .usda (sphere + dome light, the
material bound) per preview_wrapper.usda, then -- if usdview is available -- offer to view it.

    make_preview.py <material.mtlx> [-o <out.usda>] [--view]

Parity is mandatory-MANUAL (the author eyeballs the render vs the intent reference). If usdview
/ pxr is unavailable on this box (the Phase-53 gate-readiness reality), the gate DEGRADES to
SDK-validate + structural review and the artifact is an explicit `parity-not-evaluated` note --
an honest non-claim, not a silent pass (§6 degraded path). The .usda still gets written so a
USD-equipped box (or Phase 60) can render it.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

TEMPLATE = (Path(__file__).resolve().parent / "preview_wrapper.usda").read_text(encoding="utf-8")


def write_wrapper(mtlx: Path, out: Path) -> None:
    rel = os.path.relpath(mtlx.resolve(), out.resolve().parent)
    name = mtlx.stem
    text = TEMPLATE.replace("<REL_MTLX>", rel).replace("<NAME>", name)
    out.write_text(text, encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Generate a standalone usdview parity wrapper for a .mtlx.")
    ap.add_argument("mtlx")
    ap.add_argument("-o", "--out", default=None, help="default: <name>_preview.usda next to the .mtlx")
    ap.add_argument("--view", action="store_true", help="launch usdview if available")
    args = ap.parse_args(argv)

    mtlx = Path(args.mtlx)
    out = Path(args.out) if args.out else mtlx.with_name(f"{mtlx.stem}_preview.usda")
    write_wrapper(mtlx, out)
    print(f"wrote {out}")

    usdview = shutil.which("usdview")
    if not usdview:
        print(f"DEGRADED: usdview unavailable -- parity-not-evaluated for {mtlx.stem}. "
              f"Render {out.name} on a USD-equipped box (PXR_MTLX_STDLIB_SEARCH_PATHS set) "
              f"or defer to Phase 60.")
        return 0
    if args.view:
        os.execvp(usdview, [usdview, str(out)])
    print(f"usdview available at {usdview}; re-run with --view to render {out.name}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
