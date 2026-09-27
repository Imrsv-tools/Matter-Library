#!/usr/bin/env python3
"""Storm driver (USDLiveView's renderer): render every setting of a job with ``usdrecord``.

    storm.py <job.json>

Writes ``<out_dir>/storm/<setting id>.png``. The toolchain is found and its environment set
exactly as ``tools/preview_generators/make_preview.py`` does (``$USD_TOOLS_ROOT``).

Flags that make the picture comparable (each measured, Phase05 step 5.1):
``--disableCameraLight`` (otherwise usdrecord adds a headlight to the scene's lights),
``--enableDomeLightVisibility`` (the white dome is the background, as in Blender), and the
default ``--colorCorrectionMode sRGB`` (a plain sRGB encode, no tone curve).
"""

from __future__ import annotations

import json
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


def _record(scene: str, png: Path, width: int, camera: str) -> None:
    inst = usd_install()
    usdrecord = inst / "bin" / "usdrecord"
    if not usdrecord.exists():
        raise SystemExit(f"usdrecord not found at {usdrecord} (set USD_TOOLS_ROOT)")
    png.parent.mkdir(parents=True, exist_ok=True)
    cmd = [str(usdrecord), "--camera", camera, "--imageWidth", str(width),
           "--disableCameraLight", "--enableDomeLightVisibility",
           "--colorCorrectionMode", "sRGB", scene, str(png)]
    proc = subprocess.run(cmd, env=usd_env(inst), capture_output=True, text=True)
    if proc.returncode != 0 or not png.exists():
        raise SystemExit(f"usdrecord failed ({proc.returncode}) on {scene}\n{proc.stdout}{proc.stderr}")


def _pixels(png: Path) -> np.ndarray:
    return np.asarray(Image.open(png).convert("RGB"), dtype=np.float32)


def render_setting(scene: str, png: Path, width: int, camera: str) -> None:
    """Render until two consecutive frames agree.

    A single ``usdrecord`` run is NOT stable here: the same scene at the same size came back
    correct twice and once almost entirely white (measured, Phase05 5.1; most likely the
    first frame racing the dome texture's load). So a picture is accepted only when a second
    independent render reproduces it.
    """
    prev = png.with_suffix(".prev.png")
    _record(scene, prev, width, camera)
    for _ in range(TRIES):
        _record(scene, png, width, camera)
        if float(np.abs(_pixels(png) - _pixels(prev)).mean()) < AGREE:
            prev.unlink()
            return
        png.replace(prev)
    raise SystemExit(f"Storm never produced two agreeing renders of {scene} in {TRIES + 1} tries")


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
    pngs = []
    views = job.get("views") or {"wide": {"camera": job["camera"], "suffix": ""}}
    for s in job["settings"]:
        for v in views.values():
            png = out / f"{s['id']}{v['suffix']}.png"
            scene = s["scene"]
            if v.get("exposure"):
                # the view's exposure, on the USD camera (Storm honours `exposure`)
                cam = v["camera"].rsplit("/", 1)[1]
                wrap = Path(scene).with_name(f"{s['id']}{v['suffix']}.usda")
                wrap.write_text("#usda 1.0\n(\n    subLayers = [@./" + Path(scene).name + "@]\n)\n\n"
                                f'over "World"\n{{\n    over "{cam}"\n    {{\n'
                                f'        float exposure = {v["exposure"]}\n    }}\n}}\n',
                                encoding="utf-8")
                scene = str(wrap)
            render_setting(scene, png, job["width"] * ss, v["camera"])
            if ss > 1:
                Image.open(png).convert("RGB").resize(
                    (job["width"], job["width"]), Image.Resampling.BOX).save(png)
            pngs.append(png)
    return pngs


if __name__ == "__main__":
    for p in run(Path(sys.argv[1])):
        print(p)
