#!/usr/bin/env python3
"""Serve the working tree to a local Stage runtime, so USDLiveView can browse, apply and tune it.

    serve_to_stage.py [--runtime DIR] [--no-restart] [--view COMPOSITION] [--off]

Pre-release dev loop (lead, 2026-09-25: "Make a material, serve it to stage. no versioning").
Every article under ``MatterLibrary/materials/`` is served, as it is on disk right now. There
is no lockfile, no freeze, no approval and no version bump. Re-run it after adding an article.

What it does, in ``$IMRSV_STAGE_RUNTIME/MatterLibrary/`` (or ``--runtime``):
  * ``releases/matterlib-dev/materials`` and ``textures`` -> symlinks into this checkout, so a
    re-assembled article or a regenerated texture is live with no re-serve;
  * ``releases/matterlib-dev/hdris/`` -> a stamped copy of each HDRI in this checkout's
    ``MatterLibrary/hdris/``: its facts in its header, its pixels the checkout's bytes (Phase16,
    RD-P16-12; a symlink into the checkout until then), remade only when stale; and
    ``releases/matterlib-dev/thumbnails/hdris/`` -> a 1024 x 512 JPEG made from
    each HDRI, here in the runtime and never in the checkout (Q-P14-3);
  * ``releases/matterlib-dev/thumbnails/materials/`` -> each material's thumbnail, a 512 px JPEG
    of its first view, named by its entry's ``thumbnail_path`` (Phase17; the platform's ask A1 - A3):
    from this machine's master when it has a fresh one, else from the newest published dev
    snapshot, checked against its sha256 (``material_thumbnails.py``);
  * ``releases/matterlib-dev/matterlib-dev.catalog.json`` -> projected from the working tree
    (every ``.mtlx``; ``status`` from its recipe, else ``draft``; plus each article's own
    ``master`` token, so a consumer can route by it rather than by class: Phase07 7.2, L4), and,
    when the checkout holds HDRIs, their ``hdris`` list and ``default_hdri`` at schema 3 (Phase14:
    each file passes the HDRI check or the serve is refused; status from its record, else draft;
    the default from ``library/hdris.yaml``);
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
from project_runtime_catalog import (  # noqa: E402
    SCHEMA_VERSION, SCHEMA_VERSION_HDRIS, derive_entry, derive_hdri_entry)
import working_tree  # noqa: E402
import groups as G  # noqa: E402  (Phase15: the groups and each group's taxonomy)
sys.path.insert(0, str(HERE))
import hdris as H  # noqa: E402  (the HDRI list, default and thumbnail recipe: Phase14)
import material_thumbnails as MT  # noqa: E402  (Phase17: each material's thumbnail, served)

DEV = "matterlib-dev"
SERVED_RELEASE = "0.1.0"
SELECTOR = "active-release.json"
BACKUP = "active-release.before-dev.json"
PORT = 8081


def working_tree_catalog() -> dict:
    """Every article on disk, each with its recipe's status (else draft) and its own master
    token (Phase07 7.2, L4): the master lets a consumer route by the article rather than by a
    class table it has to be taught (PlatformDependencies P4)."""
    entries = []
    for art in working_tree.articles():
        row = {"id": art["id"], "version": art["version"], "status": art["status"],
               "creator_selectable": art["creator_selectable"]}
        entry = derive_entry(row)
        entry["master"] = art["master"]
        # Phase15 (RD-P15-3, RD-P15-5): the group and each group's taxonomy, read from the FILE.
        # derive_entry reads domain/class off the id's folders, which for a Character article are
        # character/<species>/<part>/, so the file's own values replace them; its domain and
        # class stay as what it is made of. Released catalogs are unchanged (RD-P15-6).
        entry.update(group=art["group"], domain=art["domain"], material_class=art["material_class"],
                     display_name=art["display_name"])
        if art["group"] == "character":
            entry.update(species=art["species"], part=art["part"])
        # Phase16 (RD-P16-11, RD-DS-2): who gave it and its licence, read from the FILE; a field
        # the file does not declare is left out (not known yet, RD-WS-1).
        entry.update({k: art[k] for k in ("contributor", "licence") if art[k]})
        if not (SOURCE / entry["payload_path"]).is_file():
            raise SystemExit(f"cannot serve {art['mtlx']}: expected payload {entry['payload_path']}")
        entries.append(entry)
    # Phase15 (RD-P15-5): the groups, in browse order, with each one's taxonomy and Character's
    # rows: the site file's list, so the engines and the website read one shape. Additive.
    catalog = {"schema_version": SCHEMA_VERSION, "release": SERVED_RELEASE, "materials": entries,
               "groups": G.GROUPS}
    hdris, default = working_tree_hdris()
    if hdris:  # Q-P14-2: schema 3 only when HDRIs are listed
        catalog.update(schema_version=SCHEMA_VERSION_HDRIS, hdris=hdris, default_hdri=default)
    return catalog


def working_tree_hdris() -> tuple[list[dict], str | None]:
    """Every HDRI on disk as a catalog entry, and the default (Phase14; tools/releases/hdris.py).
    A file that fails the HDRI check refuses the serve, as a missing payload does."""
    listed = H.on_disk()
    entries = []
    for h in listed:
        entry = derive_hdri_entry({"id": h["id"], "version": h["version"],
                                   "status": h["record"].get("status") or "draft"})
        # Phase15 (RD-P15-4): the group and its two axes; Phase16 (RD-P16-2, RD-P16-8): its
        # licence, contributor and full credit. All from H.facts, the same facts the served
        # copy's header is stamped with, so the two cannot disagree. Plus the record's whole
        # tagging (the platform's ask A10).
        f = H.facts(h)
        entry.update({k: f[k] for k in ("group", "when", "sky", "licence", "contributor", "credit")
                      if k in f})
        if h["record"].get("tagging"):
            entry["tagging"] = h["record"]["tagging"]
        entries.append(entry)
    return entries, H.default(listed)


def stamp_hdris(dev: Path) -> int:
    """Phase16 (RD-P16-12): the dev install serves a stamped copy of each HDRI, in place of
    Phase14's link into the checkout, so the repo keeps Poly Haven's bytes. Each copy is remade
    only when stale (H.stamp_stale); one the checkout no longer holds is removed. The first time,
    the copies are built beside the link and swapped in, so a reader never finds the folder empty.
    Returns how many were (re)stamped."""
    out = dev / "hdris"
    build = dev / "hdris.stamping" if out.is_symlink() else out
    build.mkdir(exist_ok=True)
    want, made = set(), 0
    for h in H.on_disk():
        f, dst = H.facts(h), build / h["path"].name
        want.add(dst.name)
        if H.stamp_stale(h["path"], dst, f):
            H.stamp(h["path"], dst, f)
            made += 1
    for p in build.iterdir():
        if p.is_file() and p.name not in want:
            p.unlink()
    if build != out:
        out.unlink()                  # the link only: never what it points at
        build.rename(out)
    return made


def make_thumbnails(dev: Path, entries: list[dict]) -> int:
    """A 2:1 JPEG per HDRI in the runtime (never in git: RD-MP-6), remade when stale."""
    made = 0
    for e in entries:
        src, dst = SOURCE / e["payload_path"], dev / e["thumbnail_path"]
        if H.stale(src, dst):
            H.thumbnail(src, dst)
            made += 1
    return made


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
        mt = MT.serve(dev, catalog["materials"], SOURCE)
        print(f"thumbnails  {mt['local'] + mt['published']} materials pictured ({mt['local']} from this "
              f"machine's masters, {mt['published']} from {mt['tag'] or 'no published snapshot'}), "
              f"{mt['none']} without; {mt['made']} made in {dev / MT.FOLDER}")
        if catalog.get("hdris"):
            stamped = stamp_hdris(dev)
            made = make_thumbnails(dev, catalog["hdris"])
            print(f"hdris  {len(catalog['hdris'])} served, default {catalog['default_hdri']}; "
                  f"{stamped} stamped in {dev / 'hdris'}; "
                  f"{made} thumbnail(s) made in {dev / 'thumbnails' / 'hdris'}")
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
