"""IMRSV LCD Export — a Blender USD-export add-on that carries Creator material
refinements (the LCD scalar travel set) into a spec-clean USD Material.

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

Phase 60 §9 piece 2 (60.3.3) — the export is SPARSE and non-duplicating:
  * Delta-only — an `inputs:<port>` override is emitted ONLY for a port whose current
    value differs from its baseline (the thin Matter node-group's INTERFACE socket
    default). An untouched material carries ZERO overrides; returning a slider to
    baseline removes the override. Delta logic lives in the pxr-/bpy-free `lcd_sparse`.
  * No-texture-duplication — `wm.usd_export(export_textures_mode='PRESERVE')` keeps the
    installed Matter textures resolving by identity instead of copying them beside the
    model (the "required Matter export configuration").
  * Transactional bridge cleanup — the stamped ID custom-props are restored/removed in a
    `finally`, so the source `.blend` material is byte-unchanged after an export.

LCD travel set (LCDSchema.md, Phase 53 D3 — current/evolving, not frozen):
base_color_tint (color3), and the floats overlay1_density, overlay2_density,
maskset_blend, roughness_bias. UV placement (uv_scale/uv_offset/uv_rotation) is
Studio-side only (S3) and NOT exported.
"""
import bpy
from bpy.props import StringProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

from . import lcd_usd_edit
from . import lcd_sparse
from .lcd_sparse import LCD_TRAVEL_PORTS, _COLOR3_PORTS

bl_info = {
    "name": "IMRSV LCD Export",
    "author": "IMRSV",
    "version": (1, 0, 0),
    "blender": (5, 1, 1),
    "location": "File > Export > IMRSV LCD USD (.usda)",
    "description": "Export USD with Creator LCD material refinements as spec-clean inputs: overrides",
    "category": "Import-Export",
}


def _nodegroup_state(mat):
    """Read this material's thin Matter node-group: return (instance_values, baseline_values)
    dicts keyed by LCD port. `instance_values` = the node-group node's input-socket values (the
    Creator edit surface); `baseline_values` = the node-group's INTERFACE socket defaults (the
    article's canonical values). Ports the node-group does not expose are simply absent."""
    inst, base = {}, {}
    if not (getattr(mat, "use_nodes", False) and mat.node_tree is not None):
        return inst, base
    for node in mat.node_tree.nodes:
        if node.bl_idname != "ShaderNodeGroup" or node.node_tree is None:
            continue
        iface = {}
        for it in node.node_tree.interface.items_tree:
            if (getattr(it, "item_type", "") == "SOCKET"
                    and getattr(it, "in_out", "") == "INPUT"
                    and it.name in LCD_TRAVEL_PORTS):
                iface[it.name] = getattr(it, "default_value", None)
        for sock in node.inputs:
            if sock.name in LCD_TRAVEL_PORTS and sock.name not in inst:
                try:
                    inst[sock.name] = sock.default_value
                    base[sock.name] = iface.get(sock.name)
                except Exception:
                    pass
    return inst, base


def _explicit_props(mat):
    """LCD ports set as explicit ID custom properties on the material (an intentional override)."""
    return {port: mat[port] for port in LCD_TRAVEL_PORTS if port in mat.keys()}


def _lcd_value_from_material(mat):
    """Collect this material's SPARSE LCD deltas — only ports whose current value differs from
    the node-group interface-default baseline. An explicit ID custom property wins over the
    node-group value but is still delta-checked against the same baseline. An untouched material
    returns {} (zero overrides). Returns {port: value}."""
    inst, base = _nodegroup_state(mat)
    return lcd_sparse.sparse_deltas(inst, base, _explicit_props(mat))


def sync_lcd_custom_props(materials=None):
    """Stamp each material's SPARSE LCD deltas onto ID custom properties so the stock USD
    exporter carries them out as userProperties. Returns an UNDO record — a list of
    (material, port, had_prop, prev_value) — so `restore_lcd_custom_props` can leave the source
    `.blend` material exactly as it was (transactional bridge cleanup, §9 piece 2d)."""
    mats = materials if materials is not None else list(bpy.data.materials)
    undo = []
    for mat in mats:
        values = _lcd_value_from_material(mat)
        for port, val in values.items():
            had = port in mat.keys()
            prev = mat[port] if had else None
            undo.append((mat, port, had, prev))
            if port in _COLOR3_PORTS:
                mat[port] = tuple(float(c) for c in val)[:3]
            else:
                mat[port] = float(val)
    return undo


def restore_lcd_custom_props(undo):
    """Reverse a `sync_lcd_custom_props` stamping: restore a pre-existing prop's prior value,
    remove a prop we introduced. Applied in a `finally` so an export never mutates the source."""
    for mat, port, had, prev in reversed(undo):
        try:
            if had:
                mat[port] = prev
            elif port in mat.keys():
                del mat[port]
        except Exception:
            pass


class LcdContractError(Exception):
    """The selected content violates the Creator Asset Profile v1 producer contract
    (one material instance per mesh, geometry UVs). Raised BEFORE any file is written."""


def _selected_mesh_objects():
    """The mesh objects the selected-only export will emit (Phase 60sq1 Step 1 output boundary)."""
    return [o for o in bpy.context.selected_objects if o.type == 'MESH']


def validate_v1_contract(objects):
    """Pre-write guard for the Creator Asset Profile v1 producer path (CreatorAssetProfile.md
    rules 1/2/3/6): the export is SELECTED-ONLY and each emitted mesh must carry exactly one
    material instance and geometry-authored UVs, and no two meshes may share one material
    datablock (independent per-mesh refinement needs separate material prims). Raises
    LcdContractError with a clear, spec-referenced message; never clamps or silently repairs."""
    if not objects:
        raise LcdContractError(
            "no mesh objects selected — the Creator export is selected-only (profile Step 1). "
            "Select the prop meshes to export.")
    seen = {}
    for ob in objects:
        mats = [s.material for s in ob.material_slots if s.material is not None]
        if len(mats) != 1:
            raise LcdContractError(
                "mesh %r has %d materials — v1 requires exactly ONE Matter material per mesh "
                "(profile rule 3; GeomSubset multi-material is out of scope, Q-d)."
                % (ob.name, len(mats)))
        if not (ob.data.uv_layers and len(ob.data.uv_layers) >= 1):
            raise LcdContractError(
                "mesh %r has no UV map — Blender-authored UVs are the primary UV and must "
                "travel as texCoord2f primvars:st (profile rule 2)." % ob.name)
        mat = mats[0]
        if mat.name in seen:
            raise LcdContractError(
                "meshes %r and %r share material datablock %r — each Creator mesh needs its own "
                "material instance for independent per-mesh refinement (profile rule 6). "
                "Duplicate the material per mesh (the Asset-Browser assign does this)."
                % (seen[mat.name], ob.name, mat.name))
        seen[mat.name] = ob.name


def export_lcd_usd(filepath):
    """Full one-action Creator export (Phase 60sq1 Step 1 output boundary): validate the v1
    contract -> bridge the sparse LCD deltas -> SELECTED-ONLY, geometry+bindings-only stock
    export (no preview surface / lights / camera / world, no texture duplication) -> in-process
    pxr-free USD reshape into the Open Matter Creator lightweight form (bare @Name.mtlx@ refs +
    assetInfo:identity + matterlibRelease stamp) -> restore the source material. Returns
    (ok, message)."""
    try:
        validate_v1_contract(_selected_mesh_objects())
    except LcdContractError as e:
        return False, "IMRSV LCD export REJECTED (v1 contract): %s" % e
    undo = sync_lcd_custom_props()
    try:
        bpy.ops.wm.usd_export(
            filepath=filepath,
            selected_objects_only=True,      # Creator exports the selected props (Step 1)
            export_materials=True,
            generate_preview_surface=False,  # the material IS the referenced Matter .mtlx
            convert_world_material=False,    # no generated world/env EXR (Discovery-2 Ref. A)
            export_lights=False,
            export_cameras=False,
            export_uvmaps=True,              # geometry UVs travel as primvars:st (rule 2)
            export_custom_properties=True,   # carries the LCD userProperties bridge
            export_textures_mode='PRESERVE',  # no heavy-texture duplication (§9 piece 2a)
        )
    finally:
        restore_lcd_custom_props(undo)  # transactional: source .blend material unchanged
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
