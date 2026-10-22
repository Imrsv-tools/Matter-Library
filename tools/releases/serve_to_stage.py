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
``../USDLiveView/usdliveview``), resolving from the dev install just served: materials from this
checkout (through its links), skies by their published names (Phase20). Edits save into the
composition, so point it at a scene you can dirty.

Phase20 (Q-P20-2 (b)): when ``library/hdris.yaml`` sets ``published_drop_variant``, each name an
HDRI was published by before is kept for the scenes saved with it: a ``deprecated``,
non-selectable catalog row and a link in ``hdris/`` to the published copy. HDRI thumbnails no
entry names are removed.
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
STAGE_EXE = "IMRSV_Stage.exe" if os.name == "nt" else "IMRSV_Stage"


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
        # Phase16 (RD-P16-11, RD-DS-2) and Phase18 (RD-P18-2): who gave it, its licence and the
        # part mesh its own picture fits, read from the FILE (working_tree.declared)
        entry.update(working_tree.declared(art))
        # CAUGHT: 2026-10-15 — the first sUKN articles (Phase18's fitted teeth and eye) projected
        # to a version-less payload path: SCALE_RE read only sNN (fixed in project_runtime_catalog)
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
    # Phase20 (Q-P20-2 (b)): each name an HDRI was published by before the switch stays
    # resolvable for the scenes saved with it, hidden and deprecated (Identity.md: "kept for old
    # scenes"). Its file is a link to the published copy (stamp_hdris) and its picture is that one's.
    current = {e["id"]: e for e in entries}
    for h in H.former(listed):
        old = derive_hdri_entry({"id": h["source_id"], "version": h["version"],
                                 "status": "deprecated", "creator_selectable": False})
        now = current[h["id"]]
        old.update({k: now[k] for k in ("thumbnail_path", "group", "when", "sky", "licence",
                                        "contributor", "credit", "tagging") if k in now})
        entries.append(old)
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
    listed = H.on_disk()
    for h in listed:
        f, dst = H.facts(h), build / f"{h['identity']}.hdr"    # the published name (RD-LBL-5)
        want.add(dst.name)
        if H.stamp_stale(h["path"], dst, f):
            H.stamp(h["path"], dst, f)
            made += 1
    # Phase20 (Q-P20-2 (b)): the name each was published by before the switch, a relative link to
    # the published copy, so a scene saved with it still finds its sky (the catalog's hidden row
    # for Stage; the folder itself for a viewer that searches it, such as USDLiveView).
    for h in H.former(listed):
        old = build / f"{h['source_id']}_{h['version']}.hdr"
        want.add(old.name)
        if not (old.is_symlink() and os.readlink(old) == f"{h['identity']}.hdr"):
            if old.is_symlink() or old.exists():
                old.unlink()          # the stamped copy served under that name before the switch
            old.symlink_to(f"{h['identity']}.hdr")
    for p in build.iterdir():
        if (p.is_file() or p.is_symlink()) and p.name not in want:
            p.unlink()
    if build != out:
        out.unlink()                  # the link only: never what it points at
        build.rename(out)
    return made


def make_thumbnails(dev: Path, entries: list[dict]) -> int:
    """A 2:1 JPEG per HDRI in the runtime (never in git: RD-MP-6), remade when stale. A picture no
    entry names any more (one under a name the switch retired, Phase20) is removed."""
    made, want = 0, set()
    source = {}
    for h in H.on_disk():   # published id, and the source id a hidden row keeps -> source file
        source[h["id"]] = source[h["source_id"]] = h["path"]
    for e in entries:
        src, dst = source[e["id"]], dev / e["thumbnail_path"]
        want.add(dst.name)
        if H.stale(src, dst):
            H.thumbnail(src, dst)
            made += 1
    folder = dev / "thumbnails" / "hdris"
    for p in folder.iterdir() if folder.is_dir() else []:
        if p.is_file() and p.name not in want:
            p.unlink()
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
    exe = (runtime / STAGE_EXE).resolve()
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
    proc = subprocess.Popen([str(runtime / STAGE_EXE)], cwd=runtime, env=env,
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


def view(composition: Path, lib: Path) -> None:
    viewer = Path(os.environ.get("USDLIVEVIEW", REPO.parent / "USDLiveView" / "usdliveview"))
    if not viewer.is_file():
        raise SystemExit(f"USDLiveView not found at {viewer} (set USDLIVEVIEW)")
    # Phase20: the dev install, not the checkout. Its materials and textures are links into this
    # checkout, and its HDRIs carry the PUBLISHED names (RD-LBL-5) a scene names, plus the old
    # ones kept for scenes saved before the switch; the checkout holds only the source names.
    env = dict(os.environ, IMRSV_MATTER_LIBRARY=str(lib))
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
    if os.name == "nt" and not args.no_restart:
        # stage_pids / restart_stage read /proc and set LD_LIBRARY_PATH: POSIX only.
        ap.error("on Windows pass --no-restart: the daemon restart is POSIX-only (Studio starts Stage)")

    if not args.runtime:
        print("no Stage runtime: set IMRSV_STAGE_RUNTIME or pass --runtime", file=sys.stderr)
        return 1
    runtime = Path(args.runtime).expanduser().resolve()
    lib = runtime / "MatterLibrary"
    if not (runtime / STAGE_EXE).is_file():
        print(f"not a Stage runtime (no {STAGE_EXE}): {runtime}", file=sys.stderr)
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
            kept = sum(1 for e in catalog["hdris"] if not e["creator_selectable"])
            print(f"hdris  {len(catalog['hdris']) - kept} served"
                  + (f" (+{kept} old names kept for old scenes, hidden)" if kept else "")
                  + f", default {catalog['default_hdri']}; "
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
        view(Path(args.view).expanduser().resolve(), lib)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
