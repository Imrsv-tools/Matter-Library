#!/usr/bin/env python
"""Phase 60 (Lane 3, 60.3.2) — tests for the pxr-free, syntax-aware LCD USD-edit transform.

Two layers:
  * pure-Python transform correctness (runs under ANY python, incl. Blender's) — multi-material,
    nested scopes, a customData dictionary, unknown userProperties left untouched, out-of-range
    REJECT, transactional (file untouched on reject), idempotency, `.usda`-only guard;
  * SEMANTIC-EQUIVALENCE acceptance (§11 round-3 vi) — the result is opened with `pxr` and the
    authored `inputs:` are compared by TYPE and VALUE (skipped, but reported, when pxr is absent).

Run under a pxr-capable python for the full gate:
    <pxr-python> blender/addons/imrsv_lcd_export/test_lcd_transform.py
Exit 0 = all pass (pxr layer must have run); non-zero = a failure or pxr was unavailable.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lcd_usd_edit as L

try:
    from pxr import Usd, UsdShade, Sdf, Gf  # noqa: F401
    HAVE_PXR = True
except Exception:
    HAVE_PXR = False

# Mirrors the exact Blender 5.1.1 export syntax pinned by the 60.3.2 probe: LCD edits ride out
# as `custom double3/double userProperties:<port>` at the Material's direct body level; an
# unknown `userProperties:blender:data_name` (string) sits beside them; a customData dictionary
# lives in the root prim's `( )` metadata; a Shader network is nested inside each Material.
FIXTURE_MULTI = '''#usda 1.0
(
    defaultPrim = "root"
    doc = "Blender v5.1.1"
)

def Xform "root" (
    customData = {
        dictionary Blender = {
            bool generated = 1
        }
    }
)
{
    def Scope "_materials"
    {
        def Material "Copper_Verdigris_Aged_Base_s01_v01"
        {
            custom double3 userProperties:base_color_tint = (0.2, 0.8, 0.4)
            custom string userProperties:blender:data_name = "Copper_Verdigris_Aged_Base_s01_v01"
            custom double userProperties:roughness_bias = 0.1

            def Shader "Principled_BSDF"
            {
                uniform token info:id = "UsdPreviewSurface"
                float inputs:roughness = 0.5
            }
        }

        def Material "Marble_Veined_Polished_Base_s01_v01"
        {
            custom double userProperties:overlay1_density = 0.5

            def Shader "Principled_BSDF"
            {
                uniform token info:id = "UsdPreviewSurface"
            }
        }
    }
}
'''

_fails = []


def check(cond, msg):
    print(("PASS" if cond else "FAIL") + ": " + msg)
    if not cond:
        _fails.append(msg)


def _write_tmp(text, suffix=".usda"):
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(text)
    return path


def test_transform_text():
    new_text, converted = L.transform_text(FIXTURE_MULTI)
    ports = sorted(p for (_, p, _) in converted)
    check(ports == ["base_color_tint", "overlay1_density", "roughness_bias"],
          "converts exactly the 3 Material-scoped LCD ports (got %r)" % ports)
    check("color3f inputs:base_color_tint = (0.2, 0.8, 0.4)" in new_text,
          "base_color_tint -> color3f inputs:")
    check("float inputs:roughness_bias = 0.1" in new_text, "roughness_bias -> float inputs:")
    check("float inputs:overlay1_density = 0.5" in new_text, "overlay1_density -> float inputs:")
    check("userProperties:base_color_tint" not in new_text
          and "userProperties:roughness_bias" not in new_text
          and "userProperties:overlay1_density" not in new_text,
          "the userProperties: LCD bridge is stripped")
    check("custom string userProperties:blender:data_name" in new_text,
          "an unknown userProperty (blender:data_name) is left untouched")
    check("float inputs:roughness = 0.5" in new_text,
          "a nested Shader's own inputs: are not touched")
    # customData dict braces must not corrupt scope tracking (Marble still converts)
    check(any(p == "overlay1_density" for (_, p, _) in converted),
          "customData { } in ( ) metadata does not break scope tracking")


def test_idempotent():
    once, _ = L.transform_text(FIXTURE_MULTI)
    twice, conv2 = L.transform_text(once)
    check(conv2 == [] and twice == once, "a 2nd pass is a no-op (idempotent)")


def test_reject_transactional():
    bad = FIXTURE_MULTI.replace(
        "custom double userProperties:roughness_bias = 0.1",
        "custom double userProperties:roughness_bias = 0.9")  # 0.9 > 0.5 max
    path = _write_tmp(bad)
    before = open(path, encoding="utf-8").read()
    raised = False
    try:
        L.transform_file(path)
    except L.LcdRejected as e:
        raised = "roughness_bias" in str(e)
    after = open(path, encoding="utf-8").read()
    os.unlink(path)
    check(raised, "out-of-range roughness_bias=0.9 REJECTs with a port+range message")
    check(after == before, "a REJECT leaves the file byte-untouched (transactional)")


def test_usda_only_guard():
    path = _write_tmp("#usda 1.0\n", suffix=".usdc")
    raised = False
    try:
        L.transform_file(path)
    except L.LcdFormatError:
        raised = True
    os.unlink(path)
    check(raised, "a non-.usda (.usdc) path is refused loudly (LcdFormatError)")


def test_semantic_equivalence():
    if not HAVE_PXR:
        _fails.append("pxr unavailable — semantic-equivalence layer did NOT run")
        print("FAIL: pxr unavailable — run under a pxr-capable python")
        return
    path = _write_tmp(FIXTURE_MULTI)
    L.transform_file(path)
    stage = Usd.Stage.Open(path)
    copper = UsdShade.Material(stage.GetPrimAtPath(
        "/root/_materials/Copper_Verdigris_Aged_Base_s01_v01"))
    marble = UsdShade.Material(stage.GetPrimAtPath(
        "/root/_materials/Marble_Veined_Polished_Base_s01_v01"))

    tint = copper.GetInput("base_color_tint")
    check(bool(tint) and tint.GetTypeName() == Sdf.ValueTypeNames.Color3f,
          "pxr reads base_color_tint as color3f")
    v = tint.Get()
    check(v is not None and abs(v[0] - 0.2) < 1e-6 and abs(v[1] - 0.8) < 1e-6
          and abs(v[2] - 0.4) < 1e-6, "pxr reads base_color_tint value (0.2,0.8,0.4)")

    rb = copper.GetInput("roughness_bias")
    check(bool(rb) and rb.GetTypeName() == Sdf.ValueTypeNames.Float and abs(rb.Get() - 0.1) < 1e-6,
          "pxr reads roughness_bias as float 0.1")

    od = marble.GetInput("overlay1_density")
    check(bool(od) and od.GetTypeName() == Sdf.ValueTypeNames.Float and abs(od.Get() - 0.5) < 1e-6,
          "pxr reads overlay1_density as float 0.5 on the 2nd material")

    # the bridge is gone, and the composed shader network still resolves
    up = [a.GetName() for a in copper.GetPrim().GetAttributes()
          if a.GetName().startswith("userProperties:") and a.GetName().split(":")[-1] in L.LCD_PORTS]
    check(up == [], "no LCD userProperties remain on the Material after transform")
    os.unlink(path)


def main():
    print("=== 60.3.2 LCD transform tests (pxr=%s) ===" % HAVE_PXR)
    test_transform_text()
    test_idempotent()
    test_reject_transactional()
    test_usda_only_guard()
    test_semantic_equivalence()
    print("=== %d checks failed ===" % len(_fails))
    return 1 if _fails else 0


if __name__ == "__main__":
    sys.exit(main())
