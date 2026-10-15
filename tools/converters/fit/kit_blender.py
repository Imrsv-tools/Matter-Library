"""The Blender side of a part-mesh kit (Phase18 18.1): the kit's mesh in a .blend of its own, with
articles bound on its parts, and a view that shows its UV layout. Run by Blender, never directly.

Build (headless, from the factory scene, into a file of its own: Learnings Blender B10):

    blender -b --factory-startup --python-exit-code 1 --python tools/converters/fit/kit_blender.py -- \\
        build library/kits/MakeHuman_Teeth_v01 library/kits/MakeHuman_Teeth_v01/MakeHuman_Teeth_v01.blend \\
        Teeth=MatterLibrary/materials/.../Enamel_Natural_Clean_Base_s001_v01.mtlx Gums=...

``Part=<article>`` binds an article on that part (built on its Blender master by
``blender/masters/load_article.py``); ``Part=<article>@<picture.png>`` also supplies the picture as
the binding's ``base_color_map``. Parts left out keep the importer's plain material.

View (a GUI Blender opened ON that file, for a person to look at):

    blender library/kits/MakeHuman_Teeth_v01/MakeHuman_Teeth_v01.blend --python tools/converters/fit/kit_blender.py -- view

It refuses any file that is not a kit's, then opens the UV Editing workspace with the kit's parts
in edit mode (so their UVs show) over the kit's layout picture, and frames the mesh.
"""

from __future__ import annotations

import sys
from pathlib import Path

import bpy

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "blender" / "masters"))


def _parts(root_name: str):
    root = bpy.data.objects.get(root_name)
    if root is None:
        raise SystemExit(f"no {root_name!r} in this file: not a kit's .blend")
    return [o for o in root.children_recursive if o.type == "MESH"]


def build(kit: Path, out: Path, bindings: list[str]) -> None:
    import load_article  # noqa: PLC0415 (needs blender/masters on the path)
    mesh_id = kit.name
    names = {o.name for o in bpy.data.objects}
    if names - {"Cube", "Light", "Camera"}:
        raise SystemExit(f"not the factory scene ({sorted(names)}): refusing to build into it (B10)")
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    bpy.ops.wm.usd_import(filepath=str(kit / f"{mesh_id}.usda"))
    parts = {o.name: o for o in _parts(mesh_id)}
    for b in bindings:
        part, _, art = b.partition("=")
        art, _, pic = art.partition("@")
        if part not in parts:
            raise SystemExit(f"{part!r} is not a part of {mesh_id} (have {sorted(parts)})")
        mat = load_article.build(Path(art), base_color_map=Path(pic) if pic else None)
        parts[part].data.materials.clear()
        parts[part].data.materials.append(mat)
    img = bpy.data.images.load(str(kit / f"{mesh_id}_layout.png"))
    img.name = f"{mesh_id}_layout"
    img.use_fake_user = True          # nothing uses it until the view shows it: kept on save
    bpy.context.scene["matter_kit"] = mesh_id
    out.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(out))
    print(f"wrote {out}: parts {sorted(parts)}")


def view() -> None:
    mesh_id = bpy.context.scene.get("matter_kit")
    if not mesh_id:
        raise SystemExit(f"{bpy.data.filepath!r} is not a kit's .blend (no matter_kit): refusing to act")
    parts = _parts(mesh_id)
    img = bpy.data.images.get(f"{mesh_id}_layout")

    def setup():
        win = bpy.context.window_manager.windows[0]
        win.workspace = bpy.data.workspaces["UV Editing"]
        return None

    def frame():
        win = bpy.context.window_manager.windows[0]
        screen = win.screen
        view3d = next(a for a in screen.areas if a.type == "VIEW_3D")
        image = next(a for a in screen.areas if a.type == "IMAGE_EDITOR")
        region = next(r for r in view3d.regions if r.type == "WINDOW")
        with bpy.context.temp_override(window=win, area=view3d, region=region):
            if bpy.context.object and bpy.context.object.mode != "OBJECT":
                bpy.ops.object.mode_set(mode="OBJECT")
            bpy.ops.object.select_all(action="DESELECT")
            for o in parts:
                o.select_set(True)
            bpy.context.view_layer.objects.active = parts[0]
            bpy.ops.object.mode_set(mode="EDIT")
            # every UV shows in the UV editor whatever is selected (sync), and with nothing selected
            # they draw as thin edges over the layout picture, not an orange sheet over the mesh
            bpy.context.scene.tool_settings.use_uv_select_sync = True
            bpy.context.scene.tool_settings.mesh_select_mode = (False, True, False)   # edges, no dots
            bpy.ops.mesh.select_all(action="SELECT")
            bpy.ops.view3d.view_axis(type="FRONT")         # the character faces the viewer
            bpy.ops.view3d.view_selected()
            bpy.ops.mesh.select_all(action="DESELECT")
            view3d.spaces[0].shading.type = "MATERIAL"
        image.spaces[0].image = img
        image.spaces[0].use_image_pin = True   # else the editor shows the active material's image
        iregion = next(r for r in image.regions if r.type == "WINDOW")
        with bpy.context.temp_override(window=win, area=image, region=iregion):
            bpy.ops.image.view_all(fit_view=True)
        return None

    bpy.app.timers.register(setup, first_interval=0.5)
    bpy.app.timers.register(frame, first_interval=1.5)


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if argv[:1] == ["build"] and len(argv) >= 3:
        build(Path(argv[1]).resolve(), Path(argv[2]).resolve(), argv[3:])
    elif argv == ["view"]:
        view()
    else:
        raise SystemExit("usage: -- build <kit dir> <out.blend> [Part=<article.mtlx>[@<picture>] ...] | -- view")
