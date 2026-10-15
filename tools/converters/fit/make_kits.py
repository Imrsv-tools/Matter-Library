#!/usr/bin/env python3
"""Make a contributor's KIT for each named part mesh (Phase18 18.1, RD-P18-1, RD-P18-4).

    uv run tools/converters/fit/make_kits.py                       # every part mesh
    uv run tools/converters/fit/make_kits.py MakeHuman_Teeth_v01   # one
    uv run tools/converters/fit/make_kits.py --measure             # print each layout's hash

A **part mesh** is the mesh a Character article's picture is drawn for, named and versioned in
``tools/converters/groups.py`` ``PART_MESHES``. **Its version is a UV layout**: a new layout is a new
``vNN``, a new shape on the same layout is the same version (F-P18-4). A kit is what a contributor
paints against, written into the git-ignored ``library/kits/<mesh>/``:

* ``<mesh>.usda`` and ``<mesh>.obj`` — the mesh in metres (Y up), one piece per part the rig and
  Studio split it into (``rig_parts``), each carrying the SOURCE UVs the picture is drawn on;
* ``<mesh>_layout.png`` — the UV layout at the picture's size: each part's islands filled in its
  own light colour, every edge drawn, to paint over;
* ``<mesh>_islands.png`` — one channel, white inside the islands: what a picture must cover;
* the gate's copy, committed as ``library/meshes/<mesh>_islands.png``, is the same picture with
  each UV island numbered (16-bit, 0 outside), so the gate (G8, RD-P18-5) can tell a whole island
  left bare from a background colour that also appears inside one;
* ``README.md`` — what the picture must be, and how it gets into the library.

The meshes come from MakeHuman's CC0 pack, pinned by URL and sha256 in the rig's character builder
(``tools/parity/scene/build_character.py``), fitted and split exactly as the rig does. A layout
whose hash is not the pinned ``uv_sha256`` is refused: it is a different mesh version.
Deterministic: the same pack gives the same bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "tools" / "parity" / "scene"))
sys.path.insert(0, str(REPO / "tools" / "converters"))
import build_character as BC  # noqa: E402  (the pinned sources, the proxy fit and the part split)
import groups as G  # noqa: E402  (PART_MESHES: the registry)

KITS = REPO / "library" / "kits"
ISLANDS = REPO / "library" / "meshes"           # the committed island pictures (the gate reads)
SUPERSAMPLE = 4                                 # the island mask is drawn 4x and reduced: smooth edges

# One light fill per rig part (layout picture only); the edge colour is dark grey.
FILLS = [(222, 214, 196), (196, 214, 226), (214, 226, 196), (226, 200, 214), (204, 204, 204)]
EDGE = (60, 60, 60)


def layout_sha256(faces, vt) -> str:
    """The UV layout's hash: every face's corner UVs, in file order (6 decimals). Two meshes with
    the same faces on the same UVs hash the same whatever their shape (F-P18-4)."""
    h = hashlib.sha256()
    for f in faces:
        h.update((" ".join(f"{vt[t][0]:.6f},{vt[t][1]:.6f}" for _, t in f) + "\n").encode())
    return h.hexdigest()


def load_mesh(mesh_id: str) -> dict:
    """A part mesh as the rig builds it: points (metres), faces [(vertex, uv)], the source UVs,
    and the faces of each rig part. No garment deletes a body face here: a kit is the whole body."""
    spec = G.PART_MESHES[mesh_id]
    src = BC.MESHES[spec["source"]]
    base_text = BC.source("base.obj").decode("utf-8", "replace")
    if "group" in src:
        pts, faces, vt, _ = BC.read_obj(base_text, src["group"])
    else:
        obj = BC.source(BC.PACK, src["proxy"] + ".obj").decode("utf-8", "replace")
        fitted = BC.fit_proxy(BC.source(BC.PACK, src["proxy"] + ".mhclo").decode("utf-8", "replace"),
                              BC.base_vertices(base_text))
        _, faces, vt, srcv = BC.read_obj(obj, None)
        pts = [fitted[vi] for vi in srcv]
    split = BC.split_faces(src, faces, vt)
    if sorted(split) != sorted(spec["rig_parts"]):
        raise SystemExit(f"{mesh_id}: the rig splits it into {sorted(split)}, the registry says "
                         f"{sorted(spec['rig_parts'])}")
    return {"points": pts, "faces": faces, "vt": vt, "split": split,
            "uv_sha256": layout_sha256(faces, vt)}


def islands(m: dict) -> list[int]:
    """Each face's UV island (1, 2, ...): faces sharing a UV corner are one island, numbered in
    the order their first face appears (deterministic)."""
    parent: dict[int, int] = {}

    def find(a):
        while parent.setdefault(a, a) != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    for f in m["faces"]:
        for _, t in f[1:]:
            parent[find(f[0][1])] = find(t)
    number: dict[int, int] = {}
    return [number.setdefault(find(f[0][1]), len(number) + 1) for f in m["faces"]]


def island_ids_png(m: dict, size: int):
    """The gate's islands: each island's pixels hold its number (16-bit PNG), 0 outside."""
    from PIL import Image, ImageDraw  # noqa: PLC0415
    ids = islands(m)
    if max(ids) > 65535:
        raise SystemExit("more islands than a 16-bit picture holds")
    im = Image.new("I", (size, size), 0)
    d = ImageDraw.Draw(im)
    for f, k in zip(m["faces"], ids):
        d.polygon(_poly(f, m["vt"], size), fill=k)
    return im.convert("I;16")


def _poly(f, vt, size):
    return [(vt[t][0] * size, (1.0 - vt[t][1]) * size) for _, t in f]


def islands_png(m: dict, size: int):
    """White inside every UV island, black outside (one channel), antialiased by supersampling."""
    from PIL import Image, ImageDraw  # noqa: PLC0415
    big = size * SUPERSAMPLE
    im = Image.new("L", (big, big), 0)
    d = ImageDraw.Draw(im)
    for f in m["faces"]:
        d.polygon(_poly(f, m["vt"], big), fill=255)
    return im.resize((size, size), Image.BOX)


def layout_png(m: dict, size: int, parts: list[str]):
    """The layout to paint over: each part's islands in its own light fill, every edge drawn."""
    from PIL import Image, ImageDraw  # noqa: PLC0415
    im = Image.new("RGB", (size, size), (255, 255, 255))
    d = ImageDraw.Draw(im)
    for k, name in enumerate(parts):
        for i in m["split"][name]:
            d.polygon(_poly(m["faces"][i], m["vt"], size), fill=FILLS[k % len(FILLS)])
    for f in m["faces"]:
        p = _poly(f, m["vt"], size)
        d.line(p + p[:1], fill=EDGE, width=1)
    return im


def usda(mesh_id: str, m: dict, parts: list[str]) -> str:
    """The mesh as USD: one Mesh per rig part, faceVarying ``st`` = the source UVs."""
    out = ['#usda 1.0\n(\n    """\n'
           f"    {mesh_id}: a Matter Library part mesh (made by tools/converters/fit/make_kits.py;\n"
           "    MakeHuman's CC0 pack, fitted and split as the parity rig does). st is the UV layout a\n"
           f"    picture for it is drawn on; layout sha256 {m['uv_sha256']}.\n"
           '    """\n'
           f'    defaultPrim = "{mesh_id}"\n    upAxis = "Y"\n    metersPerUnit = 1\n)\n\n'
           f'def Xform "{mesh_id}"\n{{\n']
    for name in parts:
        fs = [m["faces"][i] for i in m["split"][name]]
        remap, pts = {}, []
        for f in fs:
            for vi, _ in f:
                if vi not in remap:
                    remap[vi] = len(pts)
                    pts.append(m["points"][vi])
        out.append(
            f'    def Mesh "{name}"\n    {{\n'
            '        uniform token subdivisionScheme = "none"\n'
            f'        point3f[] points = [{BC._f3(pts)}]\n'
            f'        int[] faceVertexCounts = [{", ".join(str(len(f)) for f in fs)}]\n'
            f'        int[] faceVertexIndices = [{", ".join(str(remap[vi]) for f in fs for vi, _ in f)}]\n'
            f'        texCoord2f[] primvars:st = [{BC._f2([m["vt"][t] for f in fs for _, t in f])}] (\n'
            '            interpolation = "faceVarying"\n        )\n    }\n')
    out.append("}\n")
    return "".join(out)


def obj(mesh_id: str, m: dict, parts: list[str]) -> str:
    """The same mesh as Wavefront OBJ (one group per part), for painting tools that take OBJ."""
    lines = [f"# {mesh_id}: a Matter Library part mesh (CC0; layout sha256 {m['uv_sha256']})"]
    lines += [f"v {x:.6f} {y:.6f} {z:.6f}" for x, y, z in m["points"]]
    lines += [f"vt {u:.6f} {v:.6f}" for u, v in m["vt"]]
    for name in parts:
        lines.append(f"g {name}")
        lines += ["f " + " ".join(f"{vi + 1}/{t + 1}" for vi, t in m["faces"][i]) for i in m["split"][name]]
    return "\n".join(lines) + "\n"


README = """# {mesh_id} — a part-mesh kit

**What this is.** The mesh a Matter Library Character material is painted for: {what}. It is
MakeHuman's CC0 mesh, fitted and split exactly as the library's rig and Studio's character use it.
A picture painted on this UV layout fits every character built from it, whatever its shape
(**mesh version = UV layout**; layout sha256 `{sha}`).

**In this kit:**
- `{mesh_id}.usda`, `{mesh_id}.obj`: the mesh in metres, Y up, one piece per part ({parts}),
  carrying the UVs your picture is drawn on.
- `{mesh_id}_layout.png`: the UV layout at {size} × {size}, each part's islands in its own fill,
  to paint over.
- `{mesh_id}_islands.png`: white inside the islands. Your picture must cover every white pixel.

**Your picture must be:**
- a **{size} × {size} RGB PNG**, read as **sRGB**, painted on this layout;
- **the colour of the thing itself**: no lighting or shading baked in;
- **covering every island**, with a few pixels of bleed past each island's edge;
- your own work, or made from sources you have the rights to, dedicated **CC0-1.0**.

**How it gets into the library:** a recipe that names the picture and declares
`"fits": "{mesh_id}"`, with your handle as `contributor`. The gate checks the picture against this
layout. See `CONTRIBUTING.md` (§Character materials) and `docs/specs/Contract/LCDSchema.md`
(§Base colour map).
"""


def make(mesh_id: str) -> Path:
    spec = G.PART_MESHES[mesh_id]
    m = load_mesh(mesh_id)
    if m["uv_sha256"] != spec["uv_sha256"]:
        raise SystemExit(f"{mesh_id}: layout sha256 {m['uv_sha256']} is not the pinned "
                         f"{spec['uv_sha256']}: a different UV layout is a new mesh version")
    parts, size = spec["rig_parts"], spec["map_size"]
    out = KITS / mesh_id
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / f"{mesh_id}.usda").write_text(usda(mesh_id, m, parts), encoding="utf-8")
    (out / f"{mesh_id}.obj").write_text(obj(mesh_id, m, parts), encoding="utf-8")
    layout_png(m, size, parts).save(out / f"{mesh_id}_layout.png", optimize=True)
    islands_png(m, size).save(out / f"{mesh_id}_islands.png", optimize=True)
    ISLANDS.mkdir(parents=True, exist_ok=True)
    island_ids_png(m, size).save(ISLANDS / f"{mesh_id}_islands.png", optimize=True)
    (out / "README.md").write_text(README.format(
        mesh_id=mesh_id, what=spec["what"], sha=m["uv_sha256"], parts=", ".join(parts), size=size),
        encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Make the part-mesh kits.")
    ap.add_argument("mesh", nargs="*", help="part mesh ids (default: every one in PART_MESHES)")
    ap.add_argument("--measure", action="store_true", help="print each layout's sha256 and stop")
    args = ap.parse_args(argv)
    ids = args.mesh or list(G.PART_MESHES)
    for mid in ids:
        if mid not in G.PART_MESHES:
            raise SystemExit(f"{mid}: not a part mesh (have {', '.join(G.PART_MESHES)})")
        if args.measure:
            m = load_mesh(mid)
            print(f"{mid}: {len(m['faces'])} faces, layout sha256 {m['uv_sha256']}, "
                  + ", ".join(f"{p} {len(m['split'][p])}" for p in G.PART_MESHES[mid]["rig_parts"]))
            continue
        print(f"wrote {make(mid).relative_to(REPO)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
