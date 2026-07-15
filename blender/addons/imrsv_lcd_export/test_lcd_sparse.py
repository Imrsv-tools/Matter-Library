#!/usr/bin/env python
"""Phase 60 (Lane 3, 60.3.3) — tests for the SPARSE LCD export producer.

Two layers (mirrors test_lcd_transform.py's split):

  * PURE-PYTHON delta core (`lcd_sparse`) — runs under ANY interpreter (Blender's Python,
    the usdtools pxr venv, or plain CPython): untouched -> {}, one tinted -> {that port},
    slider-to-baseline drops the override, explicit ID prop wins/drops, unknown ports ignored,
    float precision noise within tolerance is NOT a delta.

  * BPY INTEGRATION (needs Blender) — builds two thin-node-group-over-Principled-BSDF Copper
    materials (one untouched, one tinted) each with an on-disk image texture, runs the add-on's
    `export_lcd_usd`, then asserts against the exported `.usda`:
       - the UNTOUCHED material carries ZERO `inputs:` LCD overrides,
       - the TINTED material carries exactly `color3f inputs:base_color_tint`,
       - ZERO Matter-texture files are copied into the export dir (export_textures_mode='PRESERVE'),
       - the bridge ID custom-props are cleaned up (source materials byte-unchanged).

Run the FULL gate under Blender:
    blender --background --factory-startup --python blender/addons/imrsv_lcd_export/test_lcd_sparse.py
Run the pure layer only under any python (bpy layer is reported NOT RUN):
    <python> blender/addons/imrsv_lcd_export/test_lcd_sparse.py
Exit 0 = all pass; non-zero = a failure (or the bpy layer did not run, which is NOT a pass).
"""
import os
import sys
import glob
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lcd_sparse as S

try:
    import bpy  # noqa: F401
    HAVE_BPY = True
except Exception:
    HAVE_BPY = False

_fails = []

# 4-tuple RGBA baseline (as Blender interface color defaults arrive) + scalar float baselines.
_BASE = {
    "base_color_tint": (0.5, 0.5, 0.5, 1.0),
    "overlay1_density": 0.0,
    "overlay2_density": 0.0,
    "maskset_blend": 0.0,
    "roughness_bias": 0.0,
}


def check(cond, msg):
    print(("PASS" if cond else "FAIL") + ": " + msg)
    if not cond:
        _fails.append(msg)


# --------------------------------------------------------------------------- pure core
def test_pure_untouched_is_empty():
    inst = dict(_BASE)  # every instance socket == its interface default
    out = S.sparse_deltas(inst, _BASE)
    check(out == {}, "untouched material -> 0 overrides (got %r)" % out)


def test_pure_single_tint():
    inst = dict(_BASE)
    inst["base_color_tint"] = (0.2, 0.8, 0.4, 1.0)
    out = S.sparse_deltas(inst, _BASE)
    check(list(out) == ["base_color_tint"], "one tinted socket -> only that port (got %r)" % list(out))


def test_pure_slider_to_baseline_drops():
    inst = dict(_BASE)
    inst["roughness_bias"] = 0.0  # returned to baseline
    out = S.sparse_deltas(inst, _BASE)
    check("roughness_bias" not in out, "a socket returned to baseline carries no override")


def test_pure_precision_noise_not_delta():
    inst = dict(_BASE)
    inst["roughness_bias"] = 0.0 + 3e-8  # 32-bit round-trip noise, below _EPS
    out = S.sparse_deltas(inst, _BASE)
    check("roughness_bias" not in out, "float precision noise below tolerance is NOT a delta")


def test_pure_explicit_prop_wins_and_drops():
    inst = dict(_BASE)  # sockets all at baseline
    won = S.sparse_deltas(inst, _BASE, explicit_values={"maskset_blend": 0.7})
    check(won.get("maskset_blend") == 0.7, "an explicit ID prop overrides an at-baseline socket")
    dropped = S.sparse_deltas(inst, _BASE, explicit_values={"maskset_blend": 0.0})
    check("maskset_blend" not in dropped, "an explicit ID prop returned to baseline drops the override")


def test_pure_unknown_port_ignored():
    out = S.sparse_deltas({"not_an_lcd_port": 0.9}, _BASE, explicit_values={"blender:data_name": 1})
    check(out == {}, "a non-LCD port is never emitted (got %r)" % out)


def test_pure_no_baseline_is_delta():
    out = S.sparse_deltas({"maskset_blend": 0.3}, {})  # no interface default known
    check(out.get("maskset_blend") == 0.3, "a port with no known baseline counts as a delta")


# --------------------------------------------------------------------------- bpy integration
def _material_block(text, name):
    """Return the `def Material "name"` body text (brace-depth aware). '' if not found."""
    marker = 'def Material "%s"' % name
    i = text.find(marker)
    if i < 0:
        return ""
    j = text.find("{", i)
    if j < 0:
        return ""
    depth, k = 0, j
    while k < len(text):
        c = text[k]
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return text[j:k + 1]
        k += 1
    return text[j:]


def _lcd_inputs_in(block):
    return [p for p in S.LCD_TRAVEL_PORTS if ("inputs:%s" % p) in block]


def test_bpy_end_to_end():
    if not HAVE_BPY:
        _fails.append("bpy unavailable — the sparse end-to-end integration layer did NOT run")
        print("FAIL: bpy unavailable — run the full gate under Blender")
        return

    addons = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, addons)
    import imrsv_lcd_export as A

    workdir = tempfile.mkdtemp(prefix="p60_sparse_")

    # an on-disk image texture (PRESERVE must NOT copy it into the export dir)
    img = bpy.data.images.new("copper_albedo", width=4, height=4)
    tex_path = os.path.join(workdir, "copper_albedo.png")
    img.filepath_raw = tex_path
    img.file_format = "PNG"
    img.save()

    # thin Matter node-group: 5 LCD interface sockets with canonical (baseline) defaults
    ng = bpy.data.node_groups.new("MatterCtl", "ShaderNodeTree")
    ct = ng.interface.new_socket("base_color_tint", in_out="INPUT", socket_type="NodeSocketColor")
    ct.default_value = (0.5, 0.5, 0.5, 1.0)
    for fp in ("overlay1_density", "overlay2_density", "maskset_blend", "roughness_bias"):
        it = ng.interface.new_socket(fp, in_out="INPUT", socket_type="NodeSocketFloat")
        it.default_value = 0.0

    def _make_material(name):
        mat = bpy.data.materials.new(name)
        mat.use_nodes = True
        nt = mat.node_tree
        bsdf = nt.nodes.get("Principled BSDF") or nt.nodes.new("ShaderNodeBsdfPrincipled")
        timg = nt.nodes.new("ShaderNodeTexImage")
        timg.image = img
        nt.links.new(timg.outputs["Color"], bsdf.inputs["Base Color"])
        grp = nt.nodes.new("ShaderNodeGroup")
        grp.node_tree = ng
        return mat, grp

    def _mesh_with(mat, obj_name):
        me = bpy.data.meshes.new(obj_name + "_mesh")
        me.from_pydata([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], [], [(0, 1, 2, 3)])
        me.update()
        me.uv_layers.new(name="UVMap")
        ob = bpy.data.objects.new(obj_name, me)
        ob.data.materials.append(mat)
        bpy.context.collection.objects.link(ob)

    mat_u, _grp_u = _make_material("Copper_Untouched")            # sockets left at baseline
    mat_t, grp_t = _make_material("Copper_Tinted")
    grp_t.inputs["base_color_tint"].default_value = (0.2, 0.8, 0.4, 1.0)  # the only refinement
    _mesh_with(mat_u, "obj_untouched")
    _mesh_with(mat_t, "obj_tinted")

    out_usda = os.path.join(workdir, "export.usda")
    ok, msg = A.export_lcd_usd(out_usda)
    check(ok, "export_lcd_usd succeeded (%s)" % msg)

    text = open(out_usda, encoding="utf-8").read()
    block_u = _material_block(text, "Copper_Untouched")
    block_t = _material_block(text, "Copper_Tinted")
    check(block_u != "" and block_t != "", "both Material prims present in the export")
    check(_lcd_inputs_in(block_u) == [],
          "UNTOUCHED material -> 0 inputs: LCD overrides (got %r)" % _lcd_inputs_in(block_u))
    check(_lcd_inputs_in(block_t) == ["base_color_tint"],
          "TINTED material -> exactly inputs:base_color_tint (got %r)" % _lcd_inputs_in(block_t))
    check("color3f inputs:base_color_tint" in block_t, "the tint is authored as color3f inputs:")

    # no-texture-duplication (§9 piece 2a / §6): the heavy on-disk Matter texture must NOT be
    # copied beside the model. PRESERVE keeps the original path; NEW would duplicate it under a
    # textures/ folder. A Blender-generated CONSTANT texture for a BSDF input is an export
    # artifact (not a Matter texture) — reported, not failed on, and discarded by Stage's
    # identity-retarget regardless (Run-3 finding).
    tex_name = os.path.basename(tex_path)
    dupes = [p for p in glob.glob(os.path.join(workdir, "**", tex_name), recursive=True)
             if os.path.abspath(p) != os.path.abspath(tex_path)]
    generated = [os.path.basename(p) for p in glob.glob(os.path.join(workdir, "textures", "*"))
                 if os.path.isfile(p) and os.path.basename(p) != tex_name]
    if generated:
        print("NOTE: Blender wrote %d generated BSDF-constant texture(s), not Matter textures: %r"
              % (len(generated), generated))
    check(dupes == [], "the heavy Matter texture is NOT duplicated into the export dir (got %r)" % dupes)

    # transactional bridge cleanup: no LCD ID custom-prop survives on either source material
    leftover = {m.name: [p for p in S.LCD_TRAVEL_PORTS if p in m.keys()] for m in (mat_u, mat_t)}
    check(all(v == [] for v in leftover.values()),
          "bridge ID custom-props cleaned up after export (leftover %r)" % leftover)


def main():
    print("=== 60.3.3 sparse-export tests (bpy=%s) ===" % HAVE_BPY)
    test_pure_untouched_is_empty()
    test_pure_single_tint()
    test_pure_slider_to_baseline_drops()
    test_pure_precision_noise_not_delta()
    test_pure_explicit_prop_wins_and_drops()
    test_pure_unknown_port_ignored()
    test_pure_no_baseline_is_delta()
    test_bpy_end_to_end()
    print("=== %d checks failed ===" % len(_fails))
    return 1 if _fails else 0


if __name__ == "__main__":
    sys.exit(main())
