#!/usr/bin/env python3
"""Preview one Matter article: write a standalone scene, and render it headless to a PNG.

    make_preview.py <article.mtlx> [--out-dir DIR] [--render] [--width 512] [--view]
                    [--set PORT=VALUE ...]

Writes ``<Stem>_preview.usda`` (a UV sphere with the article bound, dome + key light and a
camera; shape in ``preview_wrapper.usda``). With ``--render`` it also runs ``usdrecord`` to
write ``<Stem>_preview.png``. Both go to ``--out-dir``, else ``$MATTER_PREVIEW_DIR``, else
``<tmp>/matter-preview/``. Nothing is written into the repo: previews are review material,
not library content.

The scene is plain USD, so the same file opens in usdview or USDLiveView for a closer look.
This script runs in the repo's core environment (no ``pxr`` needed to WRITE the scene). The
render runs ``usdrecord`` from the USD toolchain, found the way ``docs/ToolingConventions.md``
names it: ``$USD_TOOLS_ROOT`` (default ``~/usd-tools``) -> ``inst/usd-26.03``. The toolchain's
environment is set for the child process only, as ``tools/usd-toolchain/activate-usd-tools.sh``
sets it for a shell.

``--set overlay3_density=0.8`` previews the article with a Creator slider moved (float
ports: the densities, ``maskset_blend``, ``roughness_bias``). It writes a second scene,
``<Stem>_preview_<port>-<value>.usda``, that sublayers the first and applies the override
the way every writer must (LCDSchema.md §Carrier rule): a value on the bound Material's
``inputs:<port>``, with the article's ``NG_<Stem>.inputs:<port>`` connected to it.

A missing toolchain is reported, never passed silently: the scene is still written and the
script exits 2 with the reason.
"""

from __future__ import annotations

import argparse
import math
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TEMPLATE = (HERE / "preview_wrapper.usda").read_text(encoding="utf-8")
USD_VERSION_DIR = "usd-26.03"

# UV sphere resolution. The seam column is duplicated so U wraps 0 -> 1 cleanly.
SEG_U, SEG_V = 64, 32
UV_REPEAT = 2.0          # the texture tiles twice around the equator, once pole to pole


def _sphere() -> tuple[str, str, str, str]:
    """Deterministic UV-sphere arrays, formatted for the usda template."""
    pts, uvs, idx = [], [], []
    for j in range(SEG_V + 1):
        for i in range(SEG_U + 1):
            u, v = i / SEG_U, j / SEG_V
            th, ph = u * 2 * math.pi, v * math.pi
            pts.append((math.sin(ph) * math.cos(th), math.cos(ph), math.sin(ph) * math.sin(th)))
            uvs.append((u * UV_REPEAT, 1 - v))
    for j in range(SEG_V):
        for i in range(SEG_U):
            a = j * (SEG_U + 1) + i
            b = a + SEG_U + 1
            idx += [a, a + 1, b + 1, b]
    f3 = ", ".join(f"({x:.5f}, {y:.5f}, {z:.5f})" for x, y, z in pts)
    f2 = ", ".join(f"({s:.5f}, {t:.5f})" for s, t in uvs)
    counts = ", ".join(["4"] * (SEG_U * SEG_V))
    return f3, counts, ", ".join(map(str, idx)), f2


def write_scene(mtlx: Path, out: Path) -> None:
    points, counts, indices, uvs = _sphere()
    text = (TEMPLATE.replace("<MTLX>", mtlx.resolve().as_posix())
            .replace("<NAME>", mtlx.stem)
            .replace("<POINTS>", points).replace("<COUNTS>", counts)
            .replace("<INDICES>", indices).replace("<UVS>", uvs))
    out.write_text(text, encoding="utf-8")


FLOAT_PORTS = {"overlay1_density", "overlay2_density", "overlay3_density", "maskset_blend",
               "roughness_bias"}


def write_override(base: Path, name: str, sets: list[tuple[str, float]]) -> Path:
    """A scene that sublayers `base` and moves Creator sliders through the carrier rule."""
    tag = "_".join(f"{k}-{v:g}" for k, v in sets)
    out = base.with_name(f"{base.stem}_{tag}.usda")
    mat = f"/World/Library/Materials/{name}"
    vals = "".join(f"                float inputs:{k} = {v:g}\n" for k, v in sets)
    cons = "".join(f"                    float inputs:{k}.connect = <{mat}.inputs:{k}>\n" for k, _ in sets)
    out.write_text(
        "#usda 1.0\n(\n    subLayers = [@./" + base.name + "@]\n)\n\n"
        'over "World"\n{\n    over "Library"\n    {\n        over "Materials"\n        {\n'
        f'            over "{name}"\n            {{\n{vals}'
        f'                over "NG_{name}"\n                {{\n{cons}                }}\n'
        "            }\n        }\n    }\n}\n", encoding="utf-8")
    return out


def usd_install() -> Path:
    root = Path(os.environ.get("USD_TOOLS_ROOT", Path.home() / "usd-tools")).expanduser()
    return root / "inst" / USD_VERSION_DIR


def usd_env(inst: Path) -> dict:
    """The toolchain environment for a child process (mirrors activate-usd-tools.sh)."""
    env = dict(os.environ)
    env["PATH"] = f"{inst / 'bin'}{os.pathsep}{env.get('PATH', '')}"
    env["PYTHONPATH"] = f"{inst / 'lib' / 'python'}{os.pathsep}{env.get('PYTHONPATH', '')}"
    env["LD_LIBRARY_PATH"] = str(inst / "lib")
    env["PXR_MTLX_STDLIB_SEARCH_PATHS"] = str(inst / "libraries")
    if sys.platform.startswith("linux"):
        # The build's Garch is GLX-only: Qt must use xcb + GLX (see activate-usd-tools.sh).
        env.setdefault("QT_QPA_PLATFORM", "xcb")
        env.setdefault("QT_XCB_GL_INTEGRATION", "glx")
        env.setdefault("DISPLAY", ":0")
    return env


def render(scene: Path, png: Path, width: int) -> int:
    inst = usd_install()
    usdrecord = inst / "bin" / "usdrecord"
    if not usdrecord.exists():
        print(f"NOT RENDERED: usdrecord not found at {usdrecord} "
              "(set USD_TOOLS_ROOT, or build it: tools/usd-toolchain/run-all.sh)", file=sys.stderr)
        return 2
    cmd = [str(usdrecord), "--camera", "/World/Cam", "--imageWidth", str(width), str(scene), str(png)]
    proc = subprocess.run(cmd, env=usd_env(inst), capture_output=True, text=True)
    if proc.returncode != 0 or not png.exists():
        print(f"NOT RENDERED: usdrecord exited {proc.returncode}\n{proc.stdout}{proc.stderr}",
              file=sys.stderr)
        return 2
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Write (and optionally render) a preview scene for one article.")
    ap.add_argument("mtlx")
    ap.add_argument("--out-dir", default=None,
                    help="default: $MATTER_PREVIEW_DIR, else <tmp>/matter-preview")
    ap.add_argument("--render", action="store_true", help="render <Stem>_preview.png with usdrecord")
    ap.add_argument("--width", type=int, default=512)
    ap.add_argument("--view", action="store_true", help="open the scene in usdview")
    ap.add_argument("--set", action="append", default=[], metavar="PORT=VALUE",
                    help="preview with a Creator slider moved (float ports; repeatable)")
    args = ap.parse_args(argv)

    mtlx = Path(args.mtlx)
    if not mtlx.is_file():
        print(f"no such article: {mtlx}", file=sys.stderr)
        return 1
    out_dir = Path(args.out_dir or os.environ.get("MATTER_PREVIEW_DIR")
                   or Path(tempfile.gettempdir()) / "matter-preview").expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    scene = out_dir / f"{mtlx.stem}_preview.usda"
    write_scene(mtlx, scene)
    if args.set:
        sets = []
        for item in args.set:
            k, _, v = item.partition("=")
            if k not in FLOAT_PORTS:
                print(f"--set {item!r}: port must be one of {sorted(FLOAT_PORTS)}", file=sys.stderr)
                return 1
            sets.append((k, float(v)))
        scene = write_override(scene, mtlx.stem, sets)
    print(f"scene  {scene}")

    rc = 0
    if args.render:
        png = scene.with_suffix(".png")
        rc = render(scene, png, args.width)
        if rc == 0:
            print(f"render {png}")

    liveview = shutil.which("usdliveview")
    print(f"open   {'usdliveview ' + str(scene) if liveview else scene}  (USDLiveView or usdview)")

    if args.view:
        inst = usd_install()
        os.execvpe(str(inst / "bin" / "usdview"), ["usdview", str(scene)], usd_env(inst))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
