#!/usr/bin/env python3
"""Check that every Creator LCD override is a CONNECTED Material input (Matter-Library#1 D).

    check_lcd_carrier.py <asset.usd> [<asset.usd> ...]

The contract (docs/specs/Contract/LCDSchema.md §Carrier rule): a Creator override is a value on the
bound Material's `inputs:<port>`, and the article's nodegraph input `NG_<id>.inputs:<port>`
CONNECTS to it. Without the connection the override is inert in every stock USD tool, because
usdMtlx exposes only the surface shader's inputs on the Material; and it is not INVALID, so none
of the stock `UsdValidation` validators sees it. This check has to be ours.

WHAT COUNTS AS AN OVERRIDE: a Material input, named in the frozen Creator vocabulary
(`LCD_PORTS`), that THE ASSET authored: it has a spec in a layer other than an article's own
`.mtlx`. The name alone is not enough. Three Creator ports carry OpenPBR's own input names
(`transmission_color`, `emission_color`, `emission_luminance`, Phase12), and usdMtlx puts every
surface-shader input on every Material, so each Material carries those three inputs whether or
not anyone set them: no value, and no spec outside the article. Those are the article's own, not
overrides, and are passed over. *(Until 2026-10-05 the check took the name alone, and so refused
every Material on every asset three times from the day Phase12 added the ports.)* Both forms of a
Creator asset keep the article as a `.mtlx` file, so this holds for both. It does NOT hold on a
FLATTENED copy, where every spec is in one layer and who wrote what is gone: run the check on the
asset as authored.

For every Material prim on the composed stage, every such override must:
  1. be DECLARED by the article: a child `NG_*` nodegraph carries `inputs:<port>` with a value
     (the article's start value). An override on an undeclared port is inert, so it is refused;
  2. be the connected source of that nodegraph input;
  3. carry the nodegraph input's type (`base_color_tint` is `color3f`, never `float3`);
  4. win resolution when it has a value: `GetValueProducingAttributes()` on the nodegraph input
     returns the Material attribute. That is the standard read every consumer uses.

Needs `pxr` (the USD validation toolchain, docs/specs/Tooling/USDValidationToolchain.md) and the
Matter articles on the asset search path, so the `.mtlx` references compose (check_exporter.sh sets
both). Exit 0 iff every override conforms; 1 on any violation; 2 on usage or a stage that fails to
open. Self-test: test_check_lcd_carrier.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

from pxr import Usd, UsdShade

_REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "tools" / "converters"))
# the frozen Creator vocabulary, one source. From lcd_ports, not assemble_mtlx: the assembler
# imports MaterialX, which the USD toolchain's Python does not have (Matter-Library#2).
from lcd_ports import LCD_PORTS  # noqa: E402


def asset_authored(inp: UsdShade.Input) -> bool:
    """True when the ASSET has an opinion on this Material input: a value or a bare declaration,
    in any layer that is not an article's own `.mtlx`. An input whose every spec comes from the
    article is the article's, exposed by usdMtlx, and is not an override (the module docstring)."""
    return any(spec.layer.GetFileFormat().formatId != "mtlx"
               for spec in inp.GetAttr().GetPropertyStack())


def check_stage(stage: Usd.Stage) -> tuple[int, list[str]]:
    """Return (overrides checked, [violation messages]) for every Material on `stage`."""
    checked, problems = 0, []
    for prim in stage.Traverse():
        if not prim.IsA(UsdShade.Material):
            continue
        mat_inputs = [i for i in UsdShade.Material(prim).GetInputs()
                      if i.GetBaseName() in LCD_PORTS and asset_authored(i)]
        if not mat_inputs:
            continue
        graphs = [c for c in prim.GetChildren() if c.GetName().startswith("NG_")]
        for inp in mat_inputs:
            checked += 1
            port = inp.GetBaseName()
            where = f"{prim.GetPath()}.inputs:{port}"
            declared = [g for g in graphs
                        if (gi := UsdShade.NodeGraph(g).GetInput(port))
                        and gi.GetAttr().HasAuthoredValue()]
            if not declared:
                problems.append(f"{where}: the article declares no NG_*.inputs:{port} "
                                f"(an undeclared port is inert; or the .mtlx did not compose)")
                continue
            for g in declared:
                gi = UsdShade.NodeGraph(g).GetInput(port)
                sources = gi.GetConnectedSources()[0]
                if not any(s.source.GetPath() == prim.GetPath() and s.sourceName == port
                           and s.sourceType == UsdShade.AttributeType.Input for s in sources):
                    problems.append(f"{where}: {g.GetName()}.inputs:{port} is not connected to it "
                                    f"(the override is inert in stock USD tools)")
                    continue
                # the ARTICLE's type: the weakest spec (a writer's own `over` can retype the input)
                declared_type = gi.GetAttr().GetPropertyStack()[-1].typeName
                if inp.GetTypeName() != declared_type:
                    problems.append(f"{where}: type {inp.GetTypeName()} != the article's "
                                    f"{declared_type}")
                    continue
                if inp.GetAttr().HasAuthoredValue():
                    producers = gi.GetValueProducingAttributes()
                    if not producers or producers[0].GetPath() != inp.GetAttr().GetPath():
                        problems.append(f"{where}: standard resolution of {g.GetName()}.inputs:"
                                        f"{port} does not reach the override "
                                        f"(got {[str(a.GetPath()) for a in producers]})")
    return checked, problems


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    rc = 0
    for path in argv[1:]:
        stage = Usd.Stage.Open(path)
        if not stage:
            print(f"  [FAIL] {path}: stage did not open")
            return 2
        checked, problems = check_stage(stage)
        for p in problems:
            print(f"  [FAIL] {p}")
        if problems:
            rc = 1
        else:
            print(f"  [PASS] {Path(path).name}: {checked} Creator override(s), every one a "
                  f"connected, declared, correctly typed Material input")
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
