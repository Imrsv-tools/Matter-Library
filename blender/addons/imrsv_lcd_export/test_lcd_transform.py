#!/usr/bin/env python
"""Phase 60sq1 Step 1 (was 60.3.2) — tests for the pxr-free, syntax-aware LCD USD-edit /
Creator-asset reshape transform.

Two layers:
  * pure-Python transform correctness (runs under ANY python, incl. Blender's) — multi-material,
    nested scopes, a customData dictionary, LCD conversion, shader-network + blender-bridge
    stripping, bare @Name.mtlx@ reference + assetInfo:identity authoring, `_NNN` duplicate-suffix
    identity collapse, the root matterlibRelease stamp, out-of-range REJECT, transactional (file
    untouched on reject), idempotency, `.usda`-only guard;
  * SEMANTIC-EQUIVALENCE acceptance — the result is opened with `pxr` and the authored `inputs:`
    are compared by TYPE and VALUE, and the exact-identity carrier is read from assetInfo
    (skipped, but reported, when pxr is absent).

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

# Mirrors the Blender 5.1.1 export syntax (Phase 60sq1 Step-1 probe): LCD edits ride out as
# `custom double3/double userProperties:<port>` at the Material's direct body level; the durable
# canonical-identity carrier rides as `custom string userProperties:imrsv_matter_identity`
# (E8 correction §1) — PRESERVED across datablock duplication; an unknown
# `userProperties:blender:data_name` (string) sits beside them; a customData dictionary lives in
# the root prim's `( )` metadata; a Shader network is nested inside each Material. The 2nd Copper
# is a datablock COPY (`..._v01_001`) that carries the SAME identity carrier -> the producer reads
# the carrier (NOT the datablock display name) so both collapse to one identity.
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
            custom string userProperties:imrsv_matter_identity = "Copper_Verdigris_Aged_Base_s01_v01"
            custom double userProperties:roughness_bias = 0.1
            token outputs:surface.connect = </root/_materials/Copper_Verdigris_Aged_Base_s01_v01/Principled_BSDF.outputs:surface>

            def Shader "Principled_BSDF"
            {
                uniform token info:id = "UsdPreviewSurface"
                float inputs:roughness = 0.5
            }
        }

        def Material "Copper_Verdigris_Aged_Base_s01_v01_001"
        {
            custom string userProperties:blender:data_name = "Copper_Verdigris_Aged_Base_s01_v01.001"
            custom string userProperties:imrsv_matter_identity = "Copper_Verdigris_Aged_Base_s01_v01"

            def Shader "Principled_BSDF"
            {
                uniform token info:id = "UsdPreviewSurface"
            }
        }

        def Material "Marble_Veined_Polished_Base_s01_v01"
        {
            custom double userProperties:overlay1_density = 0.5
            custom string userProperties:imrsv_matter_identity = "Marble_Veined_Polished_Base_s01_v01"

            def Shader "Principled_BSDF"
            {
                uniform token info:id = "UsdPreviewSurface"
            }
        }
    }
}
'''

# E8 correction §1 discriminator: a material whose Blender DISPLAY NAME does NOT match its Matter
# identity (a Creator renamed the datablock), carrying the durable identity carrier. The reshape
# MUST author the carrier's identity, NEVER the `_NNN`-stripped display name. Also covers the
# transitional FALLBACK material (no carrier -> name-strip heuristic).
FIXTURE_IDENTITY = '''#usda 1.0
(
    defaultPrim = "root"
)

def Xform "root"
{
    def Scope "_materials"
    {
        def Material "MyRenamedCopper_042"
        {
            custom string userProperties:imrsv_matter_identity = "Copper_Verdigris_Aged_Base_s01_v01"
            token outputs:surface.connect = </root/_materials/MyRenamedCopper_042/Principled_BSDF.outputs:surface>

            def Shader "Principled_BSDF"
            {
                uniform token info:id = "UsdPreviewSurface"
            }
        }

        def Material "Marble_Veined_Polished_Base_s01_v01_001"
        {
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

    # --- Creator-asset reshape (Phase 60sq1 Step 1) ---
    check("def Material" not in new_text,
          "every Material is retyped to a typeless `def` (referenced type wins)")
    check("userProperties:blender:data_name" not in new_text,
          "the blender:data_name bridge is consumed + stripped (was previously left untouched)")
    check("userProperties:imrsv_matter_identity" not in new_text,
          "the durable identity carrier is consumed into assetInfo + stripped from the body (§1)")
    check("Principled_BSDF" not in new_text and "UsdPreviewSurface" not in new_text
          and "outputs:surface" not in new_text,
          "the exporter's shader network + surface plug are stripped (material IS the .mtlx)")
    check('prepend references = @Copper_Verdigris_Aged_Base_s01_v01.mtlx@'
          '</MaterialX/Materials/Copper_Verdigris_Aged_Base_s01_v01>' in new_text,
          "authors the bare @Name.mtlx@ library reference")
    check('string identifier = "Copper_Verdigris_Aged_Base_s01_v01"' in new_text,
          "authors assetInfo:identifier with the exact qualified Matter name")
    check('string identifier = "Marble_Veined_Polished_Base_s01_v01"' in new_text,
          "authors the 2nd distinct identity (Marble)")
    # the duplicate datablock (`..._v01_001`) collapses to the SAME identity as the original,
    # but keeps a DISTINCT prim name so bindings resolve + instances stay independent.
    check(new_text.count('string identifier = "Copper_Verdigris_Aged_Base_s01_v01"') == 2,
          "the _001 duplicate collapses to the same identifier (independent instances, 1 identity)")
    check('def "Copper_Verdigris_Aged_Base_s01_v01_001"' in new_text,
          "the duplicate keeps its distinct prim name (bindings resolve)")

    # --- root matterlibRelease stamp (RD-2) ---
    check('string "imrsv:matterlibRelease" = "matterlib-0.1.0"' in new_text
          and "customLayerData" in new_text.split('def Xform "root"')[0],
          "stamps imrsv:matterlibRelease into root-layer customLayerData")

    # customData dict braces must not corrupt scope tracking (Marble still converts)
    check(any(p == "overlay1_density" for (_, p, _) in converted),
          "customData { } in ( ) metadata does not break scope tracking")


def test_idempotent():
    once, _ = L.transform_text(FIXTURE_MULTI)
    twice, conv2 = L.transform_text(once)
    check(conv2 == [] and twice == once, "a 2nd pass is a no-op (idempotent)")


def test_identity_from_property():
    """§1 core proof: identity comes from the durable `imrsv_matter_identity` carrier, NOT the
    datablock display name — even when the name would strip to something ELSE."""
    new_text, _ = L.transform_text(FIXTURE_IDENTITY)
    # the renamed material keeps its DISTINCT prim name, but its assetInfo identity + .mtlx ref
    # come from the carrier (name-strip would have (wrongly) yielded "MyRenamedCopper").
    check('def "MyRenamedCopper_042"' in new_text,
          "the renamed material keeps its distinct prim name (bindings resolve)")
    check('string identifier = "Copper_Verdigris_Aged_Base_s01_v01"' in new_text,
          "identity is read from the durable carrier, NOT the display name (§1)")
    check('prepend references = @Copper_Verdigris_Aged_Base_s01_v01.mtlx@'
          '</MaterialX/Materials/Copper_Verdigris_Aged_Base_s01_v01>' in new_text,
          "the .mtlx reference targets the carrier identity, not the display name (§1)")
    check('identifier = "MyRenamedCopper' not in new_text,
          "the datablock display name is NEVER used as identity when a carrier is present (§1)")
    # transitional FALLBACK: a material with NO carrier still normalizes via the `_NNN` strip.
    check('string identifier = "Marble_Veined_Polished_Base_s01_v01"' in new_text,
          "a carrier-less material falls back to the _NNN-strip heuristic (interim)")


def test_canonical_identity():
    check(L.canonical_identity("Copper_Verdigris_Aged_Base_s01_v01_001")
          == "Copper_Verdigris_Aged_Base_s01_v01", "_001 duplicate suffix stripped")
    check(L.canonical_identity("Copper_Verdigris_Aged_Base_s01_v01")
          == "Copper_Verdigris_Aged_Base_s01_v01", "a non-duplicate name is unchanged")
    check(L.canonical_identity("Foo_v01") == "Foo_v01",
          "a real name ending in letter+2 digits is NOT stripped")


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
    copper = stage.GetPrimAtPath("/root/_materials/Copper_Verdigris_Aged_Base_s01_v01")
    dup = stage.GetPrimAtPath("/root/_materials/Copper_Verdigris_Aged_Base_s01_v01_001")
    marble = stage.GetPrimAtPath("/root/_materials/Marble_Veined_Polished_Base_s01_v01")

    tint = UsdShade.Material(copper).GetInput("base_color_tint")
    check(bool(tint) and tint.GetTypeName() == Sdf.ValueTypeNames.Color3f,
          "pxr reads base_color_tint as color3f")
    v = tint.Get()
    check(v is not None and abs(v[0] - 0.2) < 1e-6 and abs(v[1] - 0.8) < 1e-6
          and abs(v[2] - 0.4) < 1e-6, "pxr reads base_color_tint value (0.2,0.8,0.4)")

    rb = UsdShade.Material(copper).GetInput("roughness_bias")
    check(bool(rb) and rb.GetTypeName() == Sdf.ValueTypeNames.Float and abs(rb.Get() - 0.1) < 1e-6,
          "pxr reads roughness_bias as float 0.1")

    od = UsdShade.Material(marble).GetInput("overlay1_density")
    check(bool(od) and od.GetTypeName() == Sdf.ValueTypeNames.Float and abs(od.Get() - 0.5) < 1e-6,
          "pxr reads overlay1_density as float 0.5 on the 2nd material")

    # exact-identity carrier readable via assetInfo (no resolver needed); dup collapses.
    check(copper.GetAssetInfoByKey("identifier") == "Copper_Verdigris_Aged_Base_s01_v01",
          "pxr reads assetInfo:identifier on the Copper instance")
    check(dup.GetAssetInfoByKey("identifier") == "Copper_Verdigris_Aged_Base_s01_v01",
          "the _001 duplicate carries the SAME identity (independent instance, one identity)")

    # the bridge is gone
    up = [a.GetName() for a in copper.GetAttributes()
          if a.GetName().startswith("userProperties:") and a.GetName().split(":")[-1] in L.LCD_PORTS]
    check(up == [], "no LCD userProperties remain on the Material after transform")
    idp = [a.GetName() for a in copper.GetAttributes() if a.GetName() == L.IDENTITY_USERPROP]
    check(idp == [], "no imrsv_matter_identity carrier remains on the Material after transform (§1)")

    # release stamp is on the root layer's customLayerData
    cld = stage.GetRootLayer().customLayerData
    check(cld.get("imrsv:matterlibRelease") == "matterlib-0.1.0",
          "pxr reads imrsv:matterlibRelease from root customLayerData")
    os.unlink(path)


def main():
    print("=== Phase 60sq1 Step-1 LCD transform / Creator-reshape tests (pxr=%s) ===" % HAVE_PXR)
    test_transform_text()
    test_idempotent()
    test_identity_from_property()
    test_canonical_identity()
    test_reject_transactional()
    test_usda_only_guard()
    test_semantic_equivalence()
    print("=== %d checks failed ===" % len(_fails))
    return 1 if _fails else 0


if __name__ == "__main__":
    sys.exit(main())
