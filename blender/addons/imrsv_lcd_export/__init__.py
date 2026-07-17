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
from pathlib import Path

import bpy
from bpy.props import StringProperty, BoolProperty
from bpy.types import Operator
from bpy_extras.io_utils import ExportHelper

from . import lcd_usd_edit
from . import lcd_sparse
from . import lcd_portable
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


def _selected_meshes_from_context(context):
    """The Creator's selected mesh objects, read from the GIVEN context. Called from the export
    operator's `invoke()` — the VIEWPORT context, where the selection is intact.

    WHY capture at invoke() and thread it through (E9 §6 root cause): after File > Export opens the
    file dialog, the operator's `execute` runs in the FILE-BROWSER context, where BOTH
    `context.selected_objects` AND the view-layer select flags (`o.select_get()`) collapse to the
    active object — while `wm.usd_export(selected_objects_only=True)` still reads the scene's real
    selection and exports every mesh. That split starved the §2 per-mesh instance split: the GUI
    export emitted ONE shared material prim for two meshes and rule-6 independence was silently lost.
    Capturing the selection here (before the browser opens) and threading it into `export_lcd_usd`
    keeps the split, the v1-contract validate, and the actual export in agreement."""
    return [o for o in context.selected_objects if o.type == 'MESH']


def _selected_mesh_objects():
    """Fallback selection source for a programmatic/headless `export_lcd_usd()` with no explicit
    object list (no operator `invoke()` ran to capture one). Reads the view-layer SELECT FLAGS
    (`o.select_get()`) — the SAME source `wm.usd_export(selected_objects_only=True)` uses — which is
    correct in a `--python`/script context where no File-browser layer intervenes. The GUI path never
    relies on this: its selection is captured at `invoke()` (see `_selected_meshes_from_context`)."""
    vl = bpy.context.view_layer
    return [o for o in vl.objects if o.type == 'MESH' and o.select_get()]


def validate_v1_contract(objects):
    """Pre-write guard for the Creator Asset Profile v1 producer path (CreatorAssetProfile.md
    rules 1/2/3): the export is SELECTED-ONLY and each emitted mesh must carry exactly one Matter
    material and geometry-authored UVs. Two meshes MAY share one Blender material datablock (when
    the Creator wants identical Blender-side settings) — the exporter emits one USD material-
    instance prim PER MESH regardless (E8 correction §2 / `split_shared_materials`), so rule 6
    independence is a producer responsibility, NOT a Creator-facing rejection. Raises
    LcdContractError with a clear, spec-referenced message; never clamps or silently repairs."""
    if not objects:
        raise LcdContractError(
            "no mesh objects selected — the Creator export is selected-only (profile Step 1). "
            "Select the prop meshes to export.")
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


def split_shared_materials(objects):
    """E8 correction §2 — per-mesh material-instance split. Ensure each selected mesh has its OWN
    material datablock so the stock USD export emits a SEPARATE material-instance prim per mesh
    (CreatorAssetProfile.md rule 6), EVEN WHEN the Creator bound one shared Blender datablock to
    several meshes (identical Blender-side settings). Each copy PRESERVES the durable identity
    custom property (`imrsv_matter_identity`) + the node-group edit state, so every per-mesh
    instance carries the SAME Matter identity as an independent USD prim. Returns an undo record
    for `restore_shared_materials` (transactional — the source `.blend` is unchanged after export).
    Runs BEFORE `sync_lcd_custom_props` so a copy's LCD deltas still ride out."""
    claimed = {}   # material datablock -> the first selected object that used it
    undo = []      # (object, slot_index, original_material)
    for ob in objects:
        for si, slot in enumerate(ob.material_slots):
            mat = slot.material
            if mat is None:
                continue
            if mat in claimed and claimed[mat] is not ob:
                copy = mat.copy()          # ID.copy() preserves custom props + node tree
                undo.append((ob, si, mat))
                slot.material = copy
            elif mat not in claimed:
                claimed[mat] = ob
    return undo


def restore_shared_materials(undo):
    """Reverse `split_shared_materials`: reassign each slot's original datablock and purge the
    now-unused per-mesh copies, so an export never mutates the source `.blend` (transactional,
    mirrors `restore_lcd_custom_props`)."""
    copies = []
    for ob, si, original in reversed(undo):
        copy = ob.material_slots[si].material
        ob.material_slots[si].material = original
        if copy is not None and copy is not original:
            copies.append(copy)
    for c in copies:
        try:
            bpy.data.materials.remove(c)
        except Exception:
            pass


def _matterlib_paths():
    """Discover the installed Matter-Library root + the current-release catalog from the add-on's
    on-disk location (`.../Matter-Library/blender/addons/imrsv_lcd_export/` -> parents[3] = the
    Matter-Library repo). Used by the complete-portable materialize; the headless gate can bypass
    this and drive `lcd_portable.materialize_portable` with explicit paths."""
    repo = Path(__file__).resolve().parents[3]
    matterlib_root = repo / "MatterLibrary"
    catalog = repo / "library" / "releases" / (lcd_usd_edit.MATTERLIB_RELEASE + ".catalog.json")
    return matterlib_root, catalog


def export_lcd_usd(filepath, objects=None, portable=False):
    """Full one-action Creator export (Phase 60sq1 Step 1 output boundary): validate the v1
    contract -> per-mesh material-instance split (§2) -> bridge the sparse LCD deltas -> SELECTED-
    ONLY, geometry+bindings-only stock export (no preview surface / lights / camera / world, no
    texture duplication) -> in-process pxr-free USD reshape into the Open Matter Creator lightweight
    form (bare @Name.mtlx@ refs + assetInfo:identity + matterlibRelease stamp) -> restore the
    source material assignments. Returns (ok, message).

    `objects` = the mesh objects to export, captured at the operator's `invoke()` (viewport context)
    and threaded in so the §2 split and the v1 validate agree with `wm.usd_export` even in the
    File-browser execute context (E9 §6). When None (programmatic/headless caller), falls back to the
    current view-layer selection via `_selected_mesh_objects()`.

    `portable` (Step 5 / RD-4) = emit the COMPLETE-PORTABLE second producer mode: after the
    lightweight reshape, materialize each referenced Matter `.mtlx` + textures ONCE into the package
    and rewrite refs portable-relative, so it opens/renders independently with NO Matter Library.
    Default False = the lightweight, library-linked form."""
    if objects is None:
        objects = _selected_mesh_objects()
    try:
        validate_v1_contract(objects)
    except LcdContractError as e:
        return False, "IMRSV LCD export REJECTED (v1 contract): %s" % e
    split_undo = split_shared_materials(objects)  # §2: one USD instance per mesh
    try:
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
                export_custom_properties=True,   # carries the LCD + identity userProperties bridge
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
        if portable:
            matterlib_root, catalog = _matterlib_paths()
            try:
                lcd_portable.materialize_portable(filepath, matterlib_root, catalog)
            except lcd_portable.PortableError as e:
                return False, "IMRSV LCD complete-portable materialize failed: %s" % e
    finally:
        restore_shared_materials(split_undo)  # transactional: source .blend assignments unchanged
    return True, "converted %d LCD override(s)%s" % (
        len(converted), " + complete-portable package" if portable else "")


class WM_OT_imrsv_lcd_usd_export(Operator, ExportHelper):
    bl_idname = "wm.imrsv_lcd_usd_export"
    bl_label = "IMRSV LCD USD Export"
    bl_description = "Export USD with Creator LCD material refinements as spec-clean inputs: overrides"

    filename_ext = ".usda"
    filter_glob: StringProperty(default="*.usda;*.usd;*.usdc", options={'HIDDEN'})

    # Step 5 / RD-4 — the complete-portable second producer mode (default off = lightweight,
    # library-linked). The File > Export dialog exposes it as a checkbox; `⚠human-codev` UI, its
    # eyes-on (independent usdview open with no search path) is the human smoke half.
    portable: BoolProperty(
        name="Complete-portable package",
        description="Materialize each Matter .mtlx + textures into the package so it opens "
                    "independently with NO Matter Library (RD-4). Off = lightweight library-linked.",
        default=False,
    )

    # Selection captured at invoke() in the viewport context and threaded into the export at
    # execute() time. Class-level default so a direct EXEC_DEFAULT call (no invoke) falls back to
    # the current selection inside export_lcd_usd. (E9 §6: the File-browser execute context loses
    # the multi-object selection, which starved the §2 per-mesh split.)
    _invoke_meshes = None

    def invoke(self, context, event):
        # Capture the Creator's selection NOW — before File > Export opens the file browser and the
        # execute() context collapses it to the active object.
        self._invoke_meshes = _selected_meshes_from_context(context)
        # Call ExportHelper.invoke EXPLICITLY: with MRO (Operator, ExportHelper), super().invoke
        # would resolve to Operator (no file browser). ExportHelper.invoke opens the file dialog.
        return ExportHelper.invoke(self, context, event)

    def execute(self, context):
        ok, msg = export_lcd_usd(self.filepath, self._invoke_meshes, self.portable)
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
