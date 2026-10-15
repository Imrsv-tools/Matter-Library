"""Matter scale view (Phase19 19.2): swap every library material in the scene for its scale grid,
and back. A wrong UV scale then shows at a glance, as grid lines that do not match their
neighbours' (the lead, RD-P19-3). The rule is ``scale_view_rules`` (D-4); this module applies it.

* **On:** each material slot holding a library article (``imrsv_matter_identity`` or
  ``ml_article``) gets a copy of the grid nearest the article's ``ml_meters_per_tile`` (stamped by
  ``gen_asset_library.py``, D-5), with the binding's ``uv_scale`` scaled by grid tile / article tile
  and its ``uv_offset`` and ``uv_rotation`` kept. The slot's own material is recorded on whatever
  owns the slot (the mesh for a data-linked slot, the object for an object-linked one).
* **Off:** every recorded slot gets its own material back, and the grid copies are removed.
* **Never silently guessed:** a material with no stamp is looked up by its identity in the
  registered Matter asset library; one still without a size wears the hatch and is listed. The
  name's tag is never used as the size (it misreports the 15 off-tag articles).

The grids themselves are appended from the registered Matter asset library (``MatterLibrary.blend``),
the same place a person drags them from.
"""

from __future__ import annotations

import json
import os

import bpy
from bpy.props import EnumProperty
from bpy.types import Operator, Panel

from . import scale_view_rules as R

RESTORE = "ml_scale_view_restore"     # on the slot's owner: the slot's own material names
COPY = "ml_scale_view"                # on a grid copy made by the view
REPORT = "ml_scale_view_report"       # on the scene: the last swap's lists, for the panel
IDENTITY = ("imrsv_matter_identity", "ml_article")


def _identity(mat):
    for k in IDENTITY:
        if mat is not None and k in mat:
            return str(mat[k])
    return None


def _library_blend():
    for lib in bpy.context.preferences.filepaths.asset_libraries:
        path = os.path.join(bpy.path.abspath(lib.path), "MatterLibrary.blend")
        if os.path.isfile(path):
            return path
    return None


def _place2d(mat):
    """The ML_Place2D node inside a library material's own MatterLCD_ group, and that group node."""
    if mat is None or not mat.use_nodes:
        return None, None
    for n in mat.node_tree.nodes:
        if n.type == "GROUP" and n.node_tree and n.node_tree.name.startswith("MatterLCD_"):
            for m in n.node_tree.nodes:
                if m.type == "GROUP" and m.node_tree and m.node_tree.name.startswith("ML_Place2D"):
                    return m, n
    return None, None


def _sizes_from_library(identities, blend):
    """meters_per_tile for identities without a stamp, read from the library's own materials."""
    if not identities or not blend:
        return {}
    found = {}
    with bpy.data.libraries.load(blend, link=True) as (src, dst):
        dst.materials = [n for n in src.materials if n in identities]
    linked = [m for m in dst.materials if m is not None]
    for m in linked:
        if "ml_meters_per_tile" in m:
            found[m.name] = float(m["ml_meters_per_tile"])
    libs = {m.library for m in linked if m.library}
    bpy.data.batch_remove(linked + list(libs))
    return found


def _grid_template(tag, blend):
    name = R.grid_article(tag)
    mat = bpy.data.materials.get(name)
    if mat is not None and mat.library is None and COPY not in mat:
        return mat
    if blend is None:
        return None
    with bpy.data.libraries.load(blend, link=False) as (src, dst):
        dst.materials = [name] if name in src.materials else []
    return dst.materials[0] if dst.materials else None


def _owners(obj):
    """(owner ID, slot index, slot) for each material slot: the mesh for a data-linked slot."""
    for i, slot in enumerate(obj.material_slots):
        yield (obj.data if slot.link == "DATA" else obj), i, slot


def scale_view_on(scene, report):
    blend = _library_blend()
    objs = [o for o in scene.objects if o.type in {"MESH", "CURVE", "SURFACE", "META", "FONT"}]
    # Every library material in reach, and the sizes of those without a stamp.
    mats = {s.material for o in objs for s in o.material_slots if s.material is not None}
    missing = {_identity(m) for m in mats if _identity(m) and COPY not in m and "ml_meters_per_tile" not in m}
    looked_up = _sizes_from_library(missing, blend)
    copies, done_owners = {}, set()
    for obj in objs:
        for owner, i, slot in _owners(obj):
            mat = slot.material
            key = (owner.name, type(owner).__name__, i)
            if mat is None or key in done_owners or COPY in mat:
                continue
            ident = _identity(mat)
            if ident is None:
                report["left_alone"].add(mat.name)
                continue
            mpt = mat.get("ml_meters_per_tile", looked_up.get(ident))
            mpt = float(mpt) if mpt is not None else None
            tag = R.tag_of(ident)
            grid = R.grid_for(mpt, tag)
            if mpt is None and tag != R.UNKNOWN:
                report["no_size"].add(ident)
            if R.off_scale(mpt, tag):
                report["off_scale"].add(f"{ident} ({mpt:g} m)")
            place, _ = _place2d(mat)
            old = tuple(place.inputs["uv_scale"].default_value[:2]) if place else (1.0, 1.0)
            off = tuple(place.inputs["uv_offset"].default_value[:2]) if place else (0.0, 0.0)
            rot = float(place.inputs["uv_rotation"].default_value) if place else 0.0
            scale = R.uv_scale_for(old, grid, mpt)
            ckey = (grid, round(scale[0], 9), round(scale[1], 9), off, round(rot, 9))
            if ckey not in copies:
                tmpl = _grid_template(grid, blend)
                if tmpl is None:
                    raise RuntimeError("the Matter asset library is not registered (its MatterLibrary.blend "
                                       "holds the scale grids); add it under Preferences > File Paths")
                gmat = tmpl.copy()
                gmat.name = f"ScaleView_{grid}"
                gmat[COPY] = True
                gp, gnode = _place2d(gmat)
                if gnode is not None:
                    gnode.node_tree = gnode.node_tree.copy()          # its own placement
                    gp, _ = _place2d(gmat)
                    gp.inputs["uv_scale"].default_value = (scale[0], scale[1], 1.0)
                    gp.inputs["uv_offset"].default_value = (off[0], off[1], 0.0)
                    gp.inputs["uv_rotation"].default_value = rot
                copies[ckey] = gmat
            record = list(owner.get(RESTORE, [""] * len(obj.material_slots)))
            record += [""] * (len(obj.material_slots) - len(record))
            record[i] = mat.name
            owner[RESTORE] = record
            slot.material = copies[ckey]
            report["swapped"] += 1
            done_owners.add(key)
    return report


def scale_view_off(scene, report):
    owners = set()
    for obj in scene.objects:
        if obj.type in {"MESH", "CURVE", "SURFACE", "META", "FONT"}:
            for owner, _i, _s in _owners(obj):
                owners.add(owner)
            owners.add(obj)
    for owner in owners:
        if RESTORE not in owner:
            continue
        record = list(owner[RESTORE])
        slots = owner.material_slots if hasattr(owner, "material_slots") else None
        for i, name in enumerate(record):
            if not name:
                continue
            mat = bpy.data.materials.get(name)
            if isinstance(owner, bpy.types.Object):
                if i < len(owner.material_slots):
                    owner.material_slots[i].material = mat
            elif i < len(owner.materials):
                owner.materials[i] = mat
            report["restored"] += 1
        del owner[RESTORE]
    # the grid copies (and their own placement groups) now used by nothing
    for m in [m for m in bpy.data.materials if COPY in m and m.users == 0]:
        _p, gnode = _place2d(m)
        tree = gnode.node_tree if gnode is not None else None
        bpy.data.materials.remove(m)
        if tree is not None and tree.users == 0:
            bpy.data.node_groups.remove(tree)
    return report


def view_is_on(scene):
    return any(RESTORE in o or (o.data is not None and RESTORE in o.data)
               for o in scene.objects if o.type in {"MESH", "CURVE", "SURFACE", "META", "FONT"})


class MATTER_OT_scale_view(Operator):
    """Swap every library material for its scale grid, so a wrong UV scale shows; or swap back"""
    bl_idname = "matter.scale_view"
    bl_label = "Matter Scale View"
    bl_options = {"REGISTER", "UNDO"}

    mode: EnumProperty(items=[("TOGGLE", "Toggle", ""), ("ON", "On", ""), ("OFF", "Off", "")],
                       default="TOGGLE")

    def execute(self, context):
        scene = context.scene
        on = (self.mode == "ON") or (self.mode == "TOGGLE" and not view_is_on(scene))
        report = {"swapped": 0, "restored": 0, "left_alone": set(), "no_size": set(), "off_scale": set()}
        try:
            (scale_view_on if on else scale_view_off)(scene, report)
        except RuntimeError as e:
            self.report({"ERROR"}, str(e))
            return {"CANCELLED"}
        scene[REPORT] = json.dumps({k: sorted(v) if isinstance(v, set) else v for k, v in report.items()}
                                   | {"on": on})
        if on:
            self.report({"INFO"}, f"Scale view ON: {report['swapped']} slots wear their grid; "
                                  f"{len(report['left_alone'])} left alone; "
                                  f"{len(report['off_scale'])} off their scale option")
        else:
            self.report({"INFO"}, f"Scale view OFF: {report['restored']} slots restored")
        return {"FINISHED"}


class MATTER_PT_scale_view(Panel):
    bl_label = "Scale View"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Matter"

    def draw(self, context):
        lay = self.layout
        on = view_is_on(context.scene)
        lay.operator(MATTER_OT_scale_view.bl_idname,
                     text="Scale view: ON (click to restore)" if on else "Scale view: OFF (click to check)",
                     depress=on).mode = "TOGGLE"
        raw = context.scene.get(REPORT)
        if not raw:
            return
        rep = json.loads(raw)
        if not rep.get("on"):
            return
        for key, title in (("off_scale", "Off their scale option"), ("no_size", "No recorded size (hatch)"),
                           ("left_alone", "Not library materials (left alone)")):
            if rep.get(key):
                box = lay.box()
                box.label(text=f"{title}: {len(rep[key])}")
                for line in rep[key][:12]:
                    box.label(text=line)


CLASSES = (MATTER_OT_scale_view, MATTER_PT_scale_view)


def register():
    for c in CLASSES:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(CLASSES):
        bpy.utils.unregister_class(c)
