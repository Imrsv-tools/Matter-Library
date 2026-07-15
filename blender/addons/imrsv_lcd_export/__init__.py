"""IMRSV LCD Export — a Blender USD-export add-on that carries Creator material
refinements (the frozen LCD scalar set) into a spec-clean USD Material.

WHY a wrapper and not a pure `USDHook`: Fedora's Blender ships USD as a C++-only
monolith (`libusd_ms.so`, no `pxr` Python module), so authoring `UsdShade` from
inside `bpy.types.USDHook` crashes Blender (`import pxr` -> `error_already_set`).
Per Phase 60 §11 the add-on instead does ONE export action with two internal steps:

  1. Bridge each material's LCD edits (node-group input sockets named as LCD ports,
     or explicit material custom properties) into ID custom properties, then run the
     stock `wm.usd_export` with custom-property export ON -> the values ride out as
     `userProperties:<port>` attrs on each Material prim.
  2. Call `lcd_usd_edit.transform_file` IN-PROCESS (Blender's own Python) to rewrite
     those into standard `inputs:<port>` UsdShade overrides and strip the
     `userProperties` bridge (Discovery 9: standard `inputs:` is the sole carrier).

Phase 60 §11 round-3: the USD-edit is a pxr-free, syntax-aware ASCII-`.usda` transform
(`lcd_usd_edit.py`), so it runs directly under Blender's Python with NO external
USD-capable interpreter and NO subprocess — closing the "harden-later" deployment gap.
Its semantic equivalence to the pxr path is proven by opening the result with `pxr` in
the tests.

LCD travel set (LCDSchema.md, Phase 53 D3): base_color_tint (color3), and the
floats overlay1_density, overlay2_density, maskset_blend, roughness_bias. UV
placement (uv_scale/uv_offset/uv_rotation) is Studio-side only (S3) and NOT exported.
"""
import bpy
from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

from . import lcd_usd_edit

bl_info = {
    "name": "IMRSV LCD Export",
    "author": "IMRSV",
    "version": (1, 0, 0),
    "blender": (5, 1, 1),
    "location": "File > Export > IMRSV LCD USD (.usda)",
    "description": "Export USD with Creator LCD material refinements as spec-clean inputs: overrides",
    "category": "Import-Export",
}

# Creator-adjustable LCD ports that TRAVEL (LCDSchema.md). UV placement excluded (S3).
LCD_TRAVEL_PORTS = (
    "base_color_tint",   # color3
    "overlay1_density",  # float
    "overlay2_density",  # float
    "maskset_blend",     # float
    "roughness_bias",    # float
)
_COLOR3_PORTS = {"base_color_tint"}


def _lcd_value_from_material(mat):
    """Collect this material's LCD edits. An explicit ID custom property wins;
    otherwise read the exposed input socket of a shader node-group (the flattened
    Creator control). Returns {port: value}. Only ports actually present are returned."""
    found = {}
    # 1) node-group input sockets (the Creator edit surface pre-flatten)
    if mat.use_nodes and mat.node_tree is not None:
        for node in mat.node_tree.nodes:
            if node.bl_idname != "ShaderNodeGroup" or node.node_tree is None:
                continue
            for sock in node.inputs:
                if sock.name in LCD_TRAVEL_PORTS and sock.name not in found:
                    try:
                        found[sock.name] = sock.default_value
                    except Exception:
                        pass
    # 2) explicit ID custom properties override the node-group value
    for port in LCD_TRAVEL_PORTS:
        if port in mat.keys():
            found[port] = mat[port]
    return found


def sync_lcd_custom_props(materials=None):
    """Stamp each material's collected LCD edits onto ID custom properties so the
    stock USD exporter carries them as userProperties. Returns the count stamped."""
    mats = materials if materials is not None else list(bpy.data.materials)
    n = 0
    for mat in mats:
        values = _lcd_value_from_material(mat)
        for port, val in values.items():
            if port in _COLOR3_PORTS:
                mat[port] = tuple(float(c) for c in val)[:3]
            else:
                mat[port] = float(val)
            n += 1
    return n


def export_lcd_usd(filepath):
    """Full one-action export: bridge LCD edits -> stock export -> in-process USD-edit.
    Returns (ok: bool, message: str)."""
    sync_lcd_custom_props()
    bpy.ops.wm.usd_export(
        filepath=filepath,
        export_materials=True,
        generate_preview_surface=True,
        export_custom_properties=True,
    )
    try:
        converted = lcd_usd_edit.transform_file(filepath)
    except lcd_usd_edit.LcdRejected as e:
        return False, "IMRSV LCD export REJECTED (out-of-range/malformed): %s" % e
    except lcd_usd_edit.LcdError as e:
        return False, "IMRSV LCD USD-edit failed: %s" % e
    return True, "converted %d LCD override(s)" % len(converted)


class WM_OT_imrsv_lcd_usd_export(Operator, ExportHelper):
    bl_idname = "wm.imrsv_lcd_usd_export"
    bl_label = "IMRSV LCD USD Export"
    bl_description = "Export USD with Creator LCD material refinements as spec-clean inputs: overrides"

    filename_ext = ".usda"
    filter_glob: StringProperty(default="*.usda;*.usd;*.usdc", options={'HIDDEN'})

    def execute(self, context):
        ok, msg = export_lcd_usd(self.filepath)
        if not ok:
            self.report({'ERROR'}, msg)
            return {'CANCELLED'}
        self.report({'INFO'}, "IMRSV LCD export ok: " + msg)
        return {'FINISHED'}


def _menu_func_export(self, context):
    self.layout.operator(WM_OT_imrsv_lcd_usd_export.bl_idname, text="IMRSV LCD USD (.usda)")


def register():
    bpy.utils.register_class(WM_OT_imrsv_lcd_usd_export)
    bpy.types.TOPBAR_MT_file_export.append(_menu_func_export)


def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(_menu_func_export)
    bpy.utils.unregister_class(WM_OT_imrsv_lcd_usd_export)


if __name__ == "__main__":
    register()
