"""Storm worker: many pictures from one process, exactly as ``usdrecord`` draws each.

    <the toolchain's python> storm_worker.py <usdrecord>     # started by storm.py, never by hand

Runs under the USD toolchain's own interpreter (usdrecord's), so it imports ``pxr`` and
nothing from the rig. One request per stdin line, a JSON object ``{"scene", "camera", "width",
"png"}``; one reply per request on stdout, a line starting ``STORM_WORKER `` and then
``{"ok": true}`` or ``{"error": "..."}`` (the libraries may print lines of their own there).

Each ``usdrecord`` launch paid for Python, the plugins, the GL context, the render delegate,
the MaterialX shader builds and the dome's lighting, every picture, twice (storm.py renders
each picture until two runs agree). Here they are paid once. The picture is made as usdrecord
makes it, by its own GL context function and the same FrameRecorder settings it sets from the
rig's flags (``--disableCameraLight --enableDomeLightVisibility --colorCorrectionMode sRGB``,
every other flag at usdrecord's default). One stage is kept open: its root layer is anonymous
and sublayers the file usdrecord would have opened, swapped per request, with that file's stage
metadata (upAxis, metersPerUnit) copied onto it. The imaging engine populates from its first
stage only (``UsdImagingGLEngine``), so a stage per request would need an engine per request,
and the shader builds again; a swapped sublayer is an ordinary scene edit the engine follows.
"""

from __future__ import annotations

import argparse
import json
import sys
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader

from pxr import Ar, Sdf, Tf, Usd, UsdAppUtils

REPLY = "STORM_WORKER "
SKIP_INFO = {"subLayers", "subLayerOffsets"}


def _usdrecord(path: str):
    """usdrecord itself, as a module: its GL context function is the one the pictures need."""
    loader = SourceFileLoader("usdrecord", path)
    mod = module_from_spec(spec_from_loader("usdrecord", loader))
    loader.exec_module(mod)
    return mod


def _defaults() -> argparse.Namespace:
    """usdrecord's own argument defaults, plus the rig's colour flag."""
    p = argparse.ArgumentParser()
    UsdAppUtils.complexityArgs.AddCmdlineArgs(p)
    UsdAppUtils.colorArgs.AddCmdlineArgs(p)
    UsdAppUtils.rendererArgs.AddCmdlineArgs(p)
    return p.parse_args(["--colorCorrectionMode", "sRGB"])


def _reply(**kw) -> None:
    sys.stdout.write(REPLY + json.dumps(kw) + "\n")
    sys.stdout.flush()


class Recorder:
    def __init__(self, usdrecord: str) -> None:
        args = _defaults()
        self._gl = _usdrecord(usdrecord)._SetupOpenGLContext()
        rec = UsdAppUtils.FrameRecorder(
            UsdAppUtils.rendererArgs.GetPluginIdFromArgument(args.rendererPlugin) or "", True, True)
        rec.SetComplexity(args.complexity.value)
        rec.SetCameraLightEnabled(False)
        rec.SetColorCorrectionMode(args.colorCorrectionMode)
        rec.SetIncludedPurposes(["proxy"])
        rec.SetDomeLightVisibility(True)
        self.rec = rec
        self.root = self.stage = self.scene = None

    def _open(self, scene: str):
        if scene == self.scene:     # the same picture again (storm.py's agreement check)
            return self.stage
        layer = Sdf.Layer.FindOrOpen(scene)
        if not layer:
            raise RuntimeError(f"could not open layer {scene}")
        layer.Reload()              # a view's layer is rewritten each run, after a first read
        if self.stage is None:      # the resolver context is the first scene's, as usdrecord's
            self.root = Sdf.Layer.CreateAnonymous("storm_worker.usda")
            ctx = Ar.GetResolver().CreateDefaultContextForAsset(scene)
            self.stage = Usd.Stage.Open(self.root, Sdf.Layer.CreateAnonymous(), ctx)
        with Sdf.ChangeBlock():
            pr, src = self.root.pseudoRoot, layer.pseudoRoot
            for k in (set(pr.ListInfoKeys()) | set(src.ListInfoKeys())) - SKIP_INFO:
                if src.HasInfo(k):
                    pr.SetInfo(k, src.GetInfo(k))
                else:
                    pr.ClearInfo(k)
            self.root.subLayerPaths = [layer.identifier]
        self.scene = scene
        return self.stage

    def record(self, scene: str, camera: str, width: int, png: str) -> None:
        stage = self._open(scene)
        cam = UsdAppUtils.GetCameraAtPath(stage, camera)
        if not cam:
            raise RuntimeError(f"no camera {camera} in {scene}")
        self.rec.SetImageWidth(max(int(width), 1))
        self.rec.SetPrimaryCameraPrimPath(cam.GetPath())
        self.rec.Record(stage, cam, Usd.TimeCode(stage.GetStartTimeCode()), png)


def main() -> int:
    rec = Recorder(sys.argv[1])
    _reply(ready=True)
    for line in sys.stdin:
        if not line.strip():
            continue
        req = json.loads(line)
        try:
            rec.record(req["scene"], req["camera"], req["width"], req["png"])
            _reply(ok=True)
        except (Tf.ErrorException, RuntimeError) as e:
            _reply(error=str(e))
    rec.rec = None          # the FrameRecorder goes before the GL context, as in usdrecord
    return 0


if __name__ == "__main__":
    sys.exit(main())
