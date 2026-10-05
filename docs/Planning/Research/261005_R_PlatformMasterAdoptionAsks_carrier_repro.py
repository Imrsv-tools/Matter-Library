"""The reproduction behind `261005_R_PlatformMasterAdoptionAsks.md` MA-F19: the carrier check
refuses a Material that carries no override at all.

Run with the USD toolchain's Python, as `tools/conformance/check_exporter.sh` runs the check:

    INST="${USD_TOOLS_ROOT:-$HOME/usd-tools}/inst/usd-26.03"
    PYTHONPATH="$INST/lib/python" LD_LIBRARY_PATH="$INST/lib" PXR_MTLX_STDLIB_SEARCH_PATHS="$INST/libraries" \
      "${USD_TOOLS_ENV:-$HOME/.conda/envs/imrsv-usd-tools}/bin/python" <this file>

That Python has no MaterialX module (issue #2), so the check cannot import the assembler's
`LCD_PORTS` there. A placeholder module stands in for MaterialX, for the import only: nothing in
the check or here calls it.
"""
import sys
import tempfile
import types
from pathlib import Path

from pxr import Usd, UsdShade

REPO = Path(__file__).resolve().parents[3]
try:
    import MaterialX  # noqa: F401
    print("MaterialX: importable in this Python")
except ImportError:
    print("MaterialX: NOT importable in this Python (issue #2); a placeholder stands in for the import")
    sys.modules["MaterialX"] = types.ModuleType("MaterialX")
sys.path.insert(0, str(REPO / "tools" / "conformance"))
import check_lcd_carrier as C  # noqa: E402

MAT = "/root/_materials/Inst"


def stage(mtlx, ident, body="", over=""):
    """A Creator-asset-shaped stage: one Material that references a real article."""
    text = f'''#usda 1.0
( defaultPrim = "root" )
def Xform "root"
{{
    def Scope "_materials"
    {{
        def "Inst" ( prepend references = @{mtlx.as_posix()}@</MaterialX/Materials/{ident}> )
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


def find(ident):
    hits = list((REPO / "MatterLibrary" / "materials").rglob(f"{ident}.mtlx"))
    assert len(hits) == 1, (ident, hits)
    return hits[0]


def report(st):
    n, problems = C.check_stage(st)
    print(f"  check: {n} counted as overrides, {len(problems)} refused")
    for p in problems:
        print("    " + p.replace(MAT + ".", "")[:140])


CASES = ["Copper_Verdigris_Aged_Base_s01_v01", "Glass_Clear_Clean_Base_s01_v01",
         "Neon_Signage_Clean_Base_s01_v01", "Diamond_Brilliant_Clean_Base_s01_v01"]
for ident in CASES:
    st = stage(find(ident), ident)
    mat = st.GetPrimAtPath(MAT)
    print(f"\n=== {ident}: referenced, NO override authored ===")
    for port in ("transmission_color", "emission_color", "emission_luminance", "base_color_tint"):
        inp = UsdShade.Material(mat).GetInput(port)
        if not inp:
            print(f"  Material inputs:{port}: absent")
            continue
        a = inp.GetAttr()
        layers = [Path(s.layer.identifier).suffix or s.layer.identifier for s in a.GetPropertyStack()]
        graphs = [c for c in mat.GetChildren() if c.GetName().startswith("NG_")]
        declared = any((gi := UsdShade.NodeGraph(g).GetInput(port)) and gi.GetAttr().HasAuthoredValue()
                       for g in graphs)
        print(f"  Material inputs:{port}: present, authored value={a.HasAuthoredValue()}, "
              f"specs from {layers}, the article declares it={declared}")
    report(st)

# the one override an asset does author, done right
ident = CASES[0]
print(f"\n=== {ident}: a correct base_color_tint override ===")
report(stage(find(ident), ident, "            color3f inputs:base_color_tint = (1, 0, 0)",
             f'            over "NG_{ident}"\n            {{\n                color3f inputs:base_color_tint.connect = '
             f'<{MAT}.inputs:base_color_tint>\n            }}'))
