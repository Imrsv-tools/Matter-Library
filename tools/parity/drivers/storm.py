#!/usr/bin/env python3
"""Storm driver (USDLiveView's renderer): render every setting of a job as ``usdrecord`` does.

    storm.py <job.json>

Writes ``<out_dir>/storm/<setting id>.png``. The toolchain is found and its environment set
exactly as ``tools/preview_generators/make_preview.py`` does (``$USD_TOOLS_ROOT``).

Flags that make the picture comparable (each measured, Phase05 step 5.1):
``--disableCameraLight`` (otherwise usdrecord adds a headlight to the scene's lights),
``--enableDomeLightVisibility`` (the white dome is the background, as in Blender), and the
default ``--colorCorrectionMode sRGB`` (a plain sRGB encode, no tone curve).

The pictures come from ONE process per job, ``storm_worker.py`` (usdrecord's own code, with
those flags), not a usdrecord launch per picture: a launch paid for Python, the plugins, the
shader builds and the dome's lighting every time, about 2.6 s a picture and two pictures per
view (``render_setting``). The worker's pictures are the launches' to the pixel (2026-10-10, the
whole sweep of StainlessSteel_Polished, LED_WarmWhite's dim view, Acrylic_Clear's side view and
the character); a sweep takes a fifth of the time.
"""

from __future__ import annotations

import contextlib
import json
import shlex
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "preview_generators"))
from make_preview import usd_env, usd_install  # noqa: E402

TOOL = "storm"


AGREE = 0.5      # mean |difference| in 8-bit levels for two renders to count as the same
TRIES = 5


@contextlib.contextmanager
def storm_worker(log: Path):
    """One ``storm_worker.py`` process for a whole job: usdrecord's picture, without paying for
    its startup, the shader builds and the dome's lighting on every picture. Yields
    ``record(scene, png, width, camera)``."""
    inst = usd_install()
    usdrecord = inst / "bin" / "usdrecord"
    if not usdrecord.exists():
        raise SystemExit(f"usdrecord not found at {usdrecord} (set USD_TOOLS_ROOT)")
    # usdrecord's own interpreter (its #! line): the toolchain's Python, which has pxr; a build
    # may set the line to a command with arguments (PXR_PYTHON_SHEBANG="/usr/bin/env python3")
    python = shlex.split(usdrecord.read_text(encoding="utf-8").splitlines()[0].removeprefix("#!"))
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("w", encoding="utf-8") as err, subprocess.Popen(
            [*python, str(HERE / "storm_worker.py"), str(usdrecord)], env=usd_env(inst), text=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=err) as proc:

        def reply() -> dict:
            for line in proc.stdout:
                if line.startswith("STORM_WORKER "):
                    return json.loads(line.removeprefix("STORM_WORKER "))
            raise SystemExit(f"the Storm worker stopped (exit {proc.wait()}); see {log}")

        def record(scene: str, png: Path, width: int, camera: str) -> None:
            png.parent.mkdir(parents=True, exist_ok=True)
            proc.stdin.write(json.dumps({"scene": scene, "camera": camera, "width": width,
                                         "png": str(png)}) + "\n")
            proc.stdin.flush()
            if err_msg := reply().get("error"):
                raise SystemExit(f"Storm failed on {scene}: {err_msg}; see {log}")

        reply()                          # {"ready": true}
        yield record
        proc.stdin.close()


def _pixels(png: Path) -> np.ndarray:
    return np.asarray(Image.open(png).convert("RGB"))


def render_setting(record, scene: str, png: Path, width: int, camera: str) -> np.ndarray:
    """Render until two consecutive frames agree; returns the accepted picture's pixels.

    A single ``usdrecord`` run is NOT stable here: the same scene at the same size came back
    correct twice and once almost entirely white (measured, Phase05 5.1; most likely the
    first frame racing the dome texture's load). So a picture is accepted only when a second
    render reproduces it.
    """
    def frame() -> np.ndarray:
        record(scene, png, width, camera)
        return _pixels(png)

    prev = frame()
    for _ in range(TRIES):
        cur = frame()
        if float(np.abs(cur.astype(np.float32) - prev).mean()) < AGREE:
            return cur
        prev = cur
    raise SystemExit(f"Storm never produced two agreeing renders of {scene} in {TRIES + 1} tries")


def _overs(opinions: dict[str, list[str]]) -> str:
    """One `over` tree for every prim path (a layer may not name a prim twice)."""
    tree: dict = {}
    for path, lines in opinions.items():
        node = tree
        for name in path.strip("/").split("/"):
            node = node.setdefault(name, {})
        node.setdefault("", []).extend(lines)

    def emit(node: dict, depth: int) -> str:
        ind = "    " * depth
        out = "".join(f"{ind}{line}\n" for line in node.get("", []))
        for name, child in node.items():
            if name:
                out += f'{ind}over "{name}"\n{ind}{{\n{emit(child, depth + 1)}{ind}}}\n'
        return out

    return emit(tree, 0)


def run(job_path: Path) -> list[Path]:
    """Render every setting and view; supersampled by ``job["storm_supersample"]``.

    usdrecord renders one sample per pixel (no anti-aliasing), where USDLiveView on screen
    and Cycles' 128 samples both smooth edges. Unsupersampled, a cut-out (Lace) measured
    6.43 against Blender on the whole set and 2.55 close up, almost all of it hard, jagged
    hole edges; rendered at 4x and box-filtered down, 3.62 and 1.69 (Phase05 5.4).
    """
    job = json.loads(job_path.read_text(encoding="utf-8"))
    out = Path(job["out_dir"]) / TOOL
    ss = int(job.get("storm_supersample", 1))
    views = job.get("views") or {"wide": {"camera": job["camera"], "suffix": ""}}
    pngs = []
    with storm_worker(Path(job["out_dir"]) / "storm.log") as record:
        for s in job["settings"]:
            for v in views.values():
                png = out / f"{s['id']}{v['suffix']}.png"
                pixels = render_setting(record, view_scene(s, v), png, job["width"] * ss, v["camera"])
                if ss > 1:
                    Image.fromarray(pixels).resize(
                        (job["width"], job["width"]), Image.Resampling.BOX).save(png)
                pngs.append(png)
    return pngs


def view_scene(s: dict, v: dict) -> str:
    """The file Storm opens for one setting in one view: the setting's scene, or a layer over it
    with the view's exposure, on the USD camera (Storm honours `exposure`), and the prims it
    hides (a character's mouth view), as USD visibility."""
    scene = s["scene"]
    if not (v.get("exposure") or v.get("hide")):
        return scene
    opinions = {}          # prim path -> the attribute lines to author on it
    if v.get("exposure"):
        opinions[v["camera"]] = [f"float exposure = {v['exposure']}"]
    for prim in v.get("hide", []):
        opinions.setdefault(prim, []).append('token visibility = "invisible"')
    # its own name, never the setting scene's: the wide view's suffix is empty, so
    # `<id><suffix>.usda` WAS the scene, and a wide view that hides (Phase09: the
    # cornea, every view) overwrote it with a layer that sublayered itself
    wrap = Path(scene).with_name(f"{s['id']}{v['suffix']}__view.usda")
    wrap.write_text("#usda 1.0\n(\n    subLayers = [@./" + Path(scene).name + "@]\n)\n\n"
                    + _overs(opinions), encoding="utf-8")
    return str(wrap)


if __name__ == "__main__":
    for p in run(Path(sys.argv[1])):
        print(p)
