#!/usr/bin/env python3
"""Self-test for check_lcd_carrier.py: it must go RED on today's unconnected override before it is
trusted to pass anything (Matter-Library#1 D).

Two layers, both against a REAL article (the Copper `.mtlx`, referenced by absolute path so no
search path is needed), so the `NG_<id>` nodegraph is the one usdMtlx actually composes:
  * the check: RED for the unconnected override (the pre-#1 carrier), an undeclared port and a
    `float3` tint; GREEN for connect + value and for connect only;
  * the premise, measured with plain UsdShade: `GetValueProducingAttributes()` on the nodegraph
    input reaches the Material value ONLY when connected, and the article default otherwise.

Run under the USD toolchain python (pxr + MaterialX):
    <pxr-python> tools/conformance/test_check_lcd_carrier.py
Exit 0 = all pass.
"""
import sys
import tempfile
from pathlib import Path

from pxr import Usd, UsdShade

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_lcd_carrier as C  # noqa: E402

_REPO = Path(__file__).resolve().parents[2]
ID = "Copper_Verdigris_Aged_Base_s01_v01"
MTLX = _REPO / "MatterLibrary" / "materials" / "engineered" / "metal" / f"{ID}.mtlx"
MAT = "/root/_materials/Copper_Inst"
UVGRID_ID = "Diagnostic_UVGrid_Clean_Base_s1_v01"
UVGRID = _REPO / "MatterLibrary" / "materials" / "utility" / "virtual" / f"{UVGRID_ID}.mtlx"

_fails = []


def check(cond, msg):
    print(("PASS" if cond else "FAIL") + ": " + msg)
    if not cond:
        _fails.append(msg)


def _stage(body, over="", ident=ID, mtlx=MTLX):
    """A Creator-asset-shaped stage: one Material instance referencing a real article (Copper by
    default), with `body` authored on the Material and `over` inside it (the NG_ connection)."""
    text = f'''#usda 1.0
(
    defaultPrim = "root"
)

def Xform "root"
{{
    def Scope "_materials"
    {{
        def "Copper_Inst" (
            prepend references = @{mtlx.as_posix()}@</MaterialX/Materials/{ident}>
        )
        {{
{body}
{over}
        }}
    }}
}}
'''
    f = tempfile.NamedTemporaryFile("w", suffix=".usda", delete=False)
    f.write(text)
    f.close()
    return Usd.Stage.Open(f.name)


def _connect(port, typ="color3f", ident=ID):
    return (f'            over "NG_{ident}"\n            {{\n'
            f'                {typ} inputs:{port}.connect = <{MAT}.inputs:{port}>\n'
            f'            }}')


TINT = "            color3f inputs:base_color_tint = (1, 0, 0)"


def test_check():
    _, p = C.check_stage(_stage(TINT))
    check(any("not connected" in m for m in p), "RED: an unconnected override (the pre-#1 carrier)")

    _, p = C.check_stage(_stage(TINT, _connect("base_color_tint")))
    check(p == [], "GREEN: connect + value (got %r)" % p)

    _, p = C.check_stage(_stage("            color3f inputs:base_color_tint", _connect("base_color_tint")))
    check(p == [], "GREEN: connect only, no value (safe to author up front) (got %r)" % p)

    _, p = C.check_stage(_stage("            float3 inputs:base_color_tint = (1, 0, 0)",
                                _connect("base_color_tint", "float3")))
    check(any("type" in m for m in p), "RED: a float3 tint (the nodegraph input is color3f)")

    # An article declares only the Creator ports it uses (UVGrid: 4 of the 8). The undeclared
    # port is discovered from the composed article, not assumed.
    st = _stage("", ident=UVGRID_ID, mtlx=UVGRID)
    ng = st.GetPrimAtPath(f"{MAT}/NG_{UVGRID_ID}")
    declared = {i.GetBaseName() for i in UsdShade.NodeGraph(ng).GetInputs()}
    missing = sorted(p for p in set(C.LCD_PORTS) - declared if C.LCD_PORTS[p][0] == "float")
    check(bool(missing), "UVGrid leaves a float Creator port undeclared (%r)" % missing)
    if missing:
        port = missing[0]
        _, p = C.check_stage(_stage(f"            float inputs:{port} = 0.3",
                                    _connect(port, "float", UVGRID_ID), UVGRID_ID, UVGRID))
        check(any("declares no" in m for m in p), "RED: an override on undeclared port %r" % port)


def test_premise():
    """The measured reason the rule exists, with plain UsdShade (no check code involved)."""
    def resolved(stage):
        ng = stage.GetPrimAtPath(f"{MAT}/NG_{ID}")
        attrs = UsdShade.NodeGraph(ng).GetInput("base_color_tint").GetValueProducingAttributes()
        return attrs[0].GetPath(), attrs[0].Get()

    path, _ = resolved(_stage(TINT))
    check(path.GetPrimPath() != MAT, "unconnected: the nodegraph resolves to the article, not the override")
    path, val = resolved(_stage(TINT, _connect("base_color_tint")))
    check(str(path) == f"{MAT}.inputs:base_color_tint" and tuple(val) == (1, 0, 0),
          "connected: the nodegraph resolves to the Material value (1,0,0)")
    path, _ = resolved(_stage("            color3f inputs:base_color_tint", _connect("base_color_tint")))
    check(path.GetPrimPath() != MAT, "connect only: the article default still flows through")


def main():
    print("=== check_lcd_carrier self-test (article: %s) ===" % MTLX.name)
    check(MTLX.exists(), "the Copper article exists")
    test_check()
    test_premise()
    print("=== %d checks failed ===" % len(_fails))
    return 1 if _fails else 0


if __name__ == "__main__":
    sys.exit(main())
