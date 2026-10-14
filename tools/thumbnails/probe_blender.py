"""Ask Blender what it will render thumbnails with: its version, the engine, the device.

    blender -b --factory-startup --python-exit-code 1 --python tools/thumbnails/probe_blender.py -- <out.json>

Run once per ``make_thumbnails.py`` invocation, so a picture's staleness can be judged before
anything is rendered (the renderer is part of the record). The device is the rig's choice
(``pick_device``), which renders to decide, so the probe sets up a camera and one cube.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import bpy

REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO / "tools" / "parity" / "drivers"))
sys.path.insert(0, str(REPO / "tools" / "parity" / "scene"))
sys.path.insert(0, str(REPO / "blender" / "masters"))
import blender_render  # noqa: E402

argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
if len(argv) != 1:
    raise SystemExit("usage: blender -b --python probe_blender.py -- <out.json>")
bpy.ops.wm.read_factory_settings(use_empty=True)
scn = bpy.context.scene
scn.render.engine = "CYCLES"
cam = bpy.data.objects.new("ProbeCam", bpy.data.cameras.new("ProbeCam"))
scn.collection.objects.link(cam)
cam.location = (0.0, -3.0, 0.0)
cam.rotation_euler = (1.5708, 0.0, 0.0)
scn.camera = cam
bpy.ops.mesh.primitive_cube_add()
device = blender_render.pick_device(scn)
Path(argv[0]).write_text(json.dumps({"blender": bpy.app.version_string, "engine": "Cycles",
                                     "device": device}) + "\n", encoding="utf-8")
