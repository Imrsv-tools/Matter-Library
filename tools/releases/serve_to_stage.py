#!/usr/bin/env python3
"""Serve the working tree to a local Stage runtime, so USDLiveView can browse, apply and tune it.

    serve_to_stage.py [--runtime DIR] [--no-restart] [--view COMPOSITION] [--off]

Pre-release dev loop (lead, 2026-09-25: "Make a material, serve it to stage. no versioning").
Every article under ``MatterLibrary/materials/`` is served, as it is on disk right now. There
is no lockfile, no freeze, no approval and no version bump. Re-run it after adding an article.

What it does, in ``$IMRSV_STAGE_RUNTIME/MatterLibrary/`` (or ``--runtime``):
  * ``releases/matterlib-dev/materials`` and ``textures`` -> symlinks into this checkout, so a
    re-assembled article or a regenerated texture is live with no re-serve;
  * ``releases/matterlib-dev/matterlib-dev.catalog.json`` -> projected from the working tree
    (every ``.mtlx``, ``status: draft``);
  * ``active-release.json`` -> ``matterlib-dev`` (the previous value is kept in
    ``active-release.before-dev.json``; ``--off`` puts it back);
  * then (re)starts the Stage daemon from that runtime, unless ``--no-restart``.

The served catalog reports ``release: 0.1.0``: Stage treats the installed release as
``matterlib-<release>`` and every existing composition is stamped ``matterlib-0.1.0``, so they
keep working. The release lifecycle (``stage/freeze/promote/activate_release.py``) is untouched.

``--view COMPOSITION`` then opens USDLiveView on it (``$USDLIVEVIEW``, else the sibling
``../USDLiveView/usdliveview``), resolving materials from this checkout only, which is what
Stage now serves. Edits save into the composition, so point it at a scene you can dirty.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
SOURCE = REPO / "MatterLibrary"
sys.path.insert(0, str(REPO / "tools" / "converters"))
from project_runtime_catalog import SCHEMA_VERSION, derive_entry  # noqa: E402

DEV = "matterlib-dev"
SERVED_RELEASE = "0.1.0"
SELECTOR = "active-release.json"
BACKUP = "active-release.before-dev.json"
PORT = 8081
VERSION_RE = re.compile(r"^(?P<leaf>.+)_(?P<ver>v\d+)$")
SYSTEM = {"IMRSV_MissingMaterial"}


def working_tree_catalog() -> dict:
    entries = []
    for mtlx in sorted((SOURCE / "materials").rglob("*.mtlx")):
        rel = mtlx.relative_to(SOURCE / "materials").with_suffix("").as_posix()
        m = VERSION_RE.match(rel)
        mid, ver = (m["leaf"], m["ver"]) if m else (rel, "v01")
        row = {"id": mid, "version": ver, "status": "draft"}
        if mtlx.stem in SYSTEM:
            row["creator_selectable"] = False
        entry = derive_entry(row)
        if not (SOURCE / entry["payload_path"]).is_file():
            raise SystemExit(f"cannot serve {mtlx}: expected payload {entry['payload_path']}")
        entries.append(entry)
    return {"schema_version": SCHEMA_VERSION, "release": SERVED_RELEASE, "materials": entries}


def write_atomic(path: Path, text: str) -> None:
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def link(path: Path, target: Path) -> None:
    if path.is_symlink() or path.exists():
        if path.is_symlink() and path.resolve() == target.resolve():
            return
        if not path.is_symlink():
            raise SystemExit(f"refusing to replace a real directory: {path}")
        path.unlink()
    path.symlink_to(target, target_is_directory=True)


def stage_pids(runtime: Path) -> list[int]:
    exe = (runtime / "IMRSV_Stage").resolve()
    pids = []
    for proc in Path("/proc").iterdir():
        if proc.name.isdigit():
            try:
                if Path(os.readlink(proc / "exe")) == exe:
                    pids.append(int(proc.name))
            except OSError:
                pass
    return pids


def port_open() -> bool:
    with socket.socket() as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", PORT)) == 0


def restart_stage(runtime: Path) -> int:
    for pid in stage_pids(runtime):
        os.kill(pid, signal.SIGINT)
        print(f"stage  stopping pid {pid}")
    for _ in range(50):
        if not stage_pids(runtime) and not port_open():
            break
        time.sleep(0.1)
    else:
        print(f"stage  port {PORT} is still taken (another Stage?) - not started", file=sys.stderr)
        return 1
    env = dict(os.environ)
    env["PXR_PLUGINPATH_NAME"] = f"{runtime / 'lib' / 'usd'}:{runtime / 'plugin' / 'usd'}"
    env["LD_LIBRARY_PATH"] = str(runtime)
    log = open(runtime / "stage.log", "ab")
    proc = subprocess.Popen([str(runtime / "IMRSV_Stage")], cwd=runtime, env=env,
                            stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    for _ in range(100):
        if port_open():
            print(f"stage  running, pid {proc.pid}, ws://127.0.0.1:{PORT} (log: {runtime / 'stage.log'})")
            return 0
        if proc.poll() is not None:
            break
        time.sleep(0.1)
    print(f"stage  did not come up - see {runtime / 'stage.log'}", file=sys.stderr)
    return 1


def view(composition: Path) -> None:
    viewer = Path(os.environ.get("USDLIVEVIEW", REPO.parent / "USDLiveView" / "usdliveview"))
    if not viewer.is_file():
        raise SystemExit(f"USDLiveView not found at {viewer} (set USDLIVEVIEW)")
    env = dict(os.environ, IMRSV_MATTER_LIBRARY=str(SOURCE))
    env.pop("IMRSV_MATTER_SOURCE", None)
    subprocess.Popen([str(viewer), str(composition)], env=env, start_new_session=True,
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"view   USDLiveView on {composition}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Serve the working tree to a local Stage runtime.")
    ap.add_argument("--runtime", default=os.environ.get("IMRSV_STAGE_RUNTIME"),
                    help="the Stage runtime dir (default: $IMRSV_STAGE_RUNTIME)")
    ap.add_argument("--no-restart", action="store_true", help="don't (re)start the Stage daemon")
    ap.add_argument("--view", metavar="COMPOSITION", help="then open USDLiveView on this composition")
    ap.add_argument("--off", action="store_true", help="put the previous active release back")
    args = ap.parse_args(argv)

    if not args.runtime:
        print("no Stage runtime: set IMRSV_STAGE_RUNTIME or pass --runtime", file=sys.stderr)
        return 1
    runtime = Path(args.runtime).expanduser().resolve()
    lib = runtime / "MatterLibrary"
    if not (runtime / "IMRSV_Stage").is_file():
        print(f"not a Stage runtime (no IMRSV_Stage): {runtime}", file=sys.stderr)
        return 1
    lib.mkdir(exist_ok=True)
    selector, backup = lib / SELECTOR, lib / BACKUP

    if args.off:
        if not backup.exists():
            print("nothing to undo: not serving the working tree", file=sys.stderr)
            return 1
        write_atomic(selector, backup.read_text(encoding="utf-8"))
        backup.unlink()
        print(f"served {json.loads(selector.read_text())['active_release']} again")
    else:
        dev = lib / "releases" / DEV
        dev.mkdir(parents=True, exist_ok=True)
        link(dev / "materials", SOURCE / "materials")
        link(dev / "textures", SOURCE / "textures")
        catalog = working_tree_catalog()
        write_atomic(dev / f"{DEV}.catalog.json",
                     json.dumps(catalog, indent=2, sort_keys=True) + "\n")
        current = json.loads(selector.read_text()).get("active_release") if selector.exists() else None
        if current != DEV:
            backup.write_text(selector.read_text() if selector.exists()
                              else json.dumps({"active_release": ""}) + "\n", encoding="utf-8")
            write_atomic(selector, json.dumps({"active_release": DEV}, indent=2) + "\n")
        print(f"served {len(catalog['materials'])} articles from {SOURCE} -> {dev}")

    rc = 0 if args.no_restart else restart_stage(runtime)
    if rc == 0 and args.view:
        view(Path(args.view).expanduser().resolve())
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
