#!/usr/bin/env python3
"""Phase 60sq1 Step 5 (RD-4) — pxr-free unit tests for the complete-portable materializer.

Drives `lcd_portable.materialize_portable` directly on synthetic fixtures (no Blender, no pxr, no
Matter Library) so it runs under any python3. The two-way core: a lightweight `.usda` has BARE
`@<id>.mtlx@` refs and NO material payload beside it; after materialize it has LOCAL `@./<id>.mtlx@`
refs, each `<id>.mtlx` written beside it with textures flattened into `./textures/`. Plus the
self-containment guarantees (texture dedup across materials) and the never-silently-skip contracts
(unknown identity / missing texture / basename collision / no-refs all RAISE).

Run:  python3 test_lcd_portable.py     (mirrors test_lcd_sparse.py — pure-python layer)
"""
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lcd_portable as P  # noqa: E402

_fails = []


def check(ok, label):
    if not ok:
        _fails.append(label)
    print("  [%s] %s" % ("PASS" if ok else "FAIL", label))


def _mtlx(tex_refs):
    """A minimal MaterialX with one <image> per texture ref (matches lcd_portable's file scan)."""
    imgs = "\n".join(
        '    <image name="i%d" type="color3">\n'
        '      <input name="file" type="filename" value="%s"/>\n'
        '    </image>' % (i, r) for i, r in enumerate(tex_refs))
    return '<?xml version="1.0"?>\n<materialx version="1.39">\n%s\n</materialx>\n' % imgs


def _lightweight_usda(instances):
    """A lightweight `.usda`: one Material prim per (stem, instance-index); each a bare @stem.mtlx@."""
    body = "\n".join(
        '    def Material "%s_Instance_%d"\n    {\n'
        '        prepend references = @%s.mtlx@</MaterialX/Materials/%s>\n    }' % (stem, i, stem, stem)
        for stem, i in instances)
    return ('#usda 1.0\n(\n    customLayerData = {\n'
            '        string "imrsv:matterlibRelease" = "matterlib-0.1.0"\n    }\n)\n'
            'def Xform "root"\n{\n%s\n}\n' % body)


def _build_env(base, mats, instances):
    """Create a synthetic environment under `base`.

    * `mats`     — dict identity -> {mtlx_texture_ref: texture_on_disk_relpath}. The `.mtlx` is
                   written at matterlib_root/materials/<id>.mtlx referencing each key; the value is
                   the texture's path relative to matterlib_root/materials (the file is created).
    * `instances`— list of (identity, index) for the lightweight `.usda`'s material prims.

    Returns (usda_path, matterlib_root, catalog_path).
    """
    matterlib_root = base / "MatterLibrary"
    mat_dir = matterlib_root / "materials"
    mat_dir.mkdir(parents=True)
    catalog = {"release": "matterlib-0.1.0", "schema_version": 2, "materials": []}
    for ident, texmap in mats.items():
        for on_disk in set(texmap.values()):
            tex_path = mat_dir / on_disk
            tex_path.parent.mkdir(parents=True, exist_ok=True)
            tex_path.write_bytes(b"\x89PNG\r\n\x1a\n" + ident.encode() + on_disk.encode())
        (mat_dir / ("%s.mtlx" % ident)).write_text(_mtlx(list(texmap.keys())))
        catalog["materials"].append({"id": ident, "payload_path": "materials/%s.mtlx" % ident})
    catalog_path = base / "catalog.json"
    catalog_path.write_text(json.dumps(catalog))

    pkg = base / "export"
    pkg.mkdir()
    usda_path = pkg / "asset.usda"
    usda_path.write_text(_lightweight_usda(instances))
    return usda_path, matterlib_root, catalog_path


def test_two_way_lightweight_to_portable():
    print("=== two-way: lightweight (bare refs, no payload) -> portable (local refs, textures) ===")
    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        usda, mroot, cat = _build_env(
            base, {"Foo": {"base/foo_base.png": "base/foo_base.png"}}, [("Foo", 0), ("Foo", 1)])
        pkg = usda.parent

        pre = usda.read_text()
        check("@Foo.mtlx@" in pre and "@./Foo.mtlx@" not in pre, "PRE: lightweight has bare @Foo.mtlx@ refs")
        check(not (pkg / "Foo.mtlx").exists() and not (pkg / "textures").exists(),
              "PRE: no material payload beside the lightweight .usda")

        ids = P.materialize_portable(usda, mroot, cat)
        check(ids == ["Foo"], "returns the materialized identity list [Foo] (got %r)" % ids)

        post = usda.read_text()
        check("@./Foo.mtlx@" in post and "@Foo.mtlx@" not in post.replace("@./Foo.mtlx@", ""),
              "POST: EVERY bare ref rewritten to local @./Foo.mtlx@ (both instances)")
        check((pkg / "Foo.mtlx").is_file(), "POST: Foo.mtlx materialized beside the .usda")
        tex = list((pkg / "textures").glob("*")) if (pkg / "textures").is_dir() else []
        check([p.name for p in tex] == ["foo_base.png"], "POST: textures/ populated (foo_base.png)")
        mtlx_text = (pkg / "Foo.mtlx").read_text()
        check('value="textures/foo_base.png"' in mtlx_text and 'value="base/foo_base.png"' not in mtlx_text,
              "POST: .mtlx texture ref rewritten to portable textures/<base>")


def test_texture_dedup_across_materials():
    print("=== shared texture materialized ONCE across materials (shared overlays/masks) ===")
    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        # Foo and Bar both reference the SAME shared texture path + each its own base texture.
        usda, mroot, cat = _build_env(base, {
            "Foo": {"shared/dust.png": "shared/dust.png", "base/foo.png": "base/foo.png"},
            "Bar": {"shared/dust.png": "shared/dust.png", "base/bar.png": "base/bar.png"},
        }, [("Foo", 0), ("Bar", 0)])
        pkg = usda.parent
        ids = P.materialize_portable(usda, mroot, cat)
        check(ids == ["Bar", "Foo"], "both identities materialized (sorted) (got %r)" % ids)
        names = sorted(p.name for p in (pkg / "textures").glob("*"))
        check(names == ["bar.png", "dust.png", "foo.png"],
              "shared dust.png flattened ONCE; 3 textures total (got %r)" % names)


def test_unknown_identity_raises():
    print("=== unknown identity (not in catalog) RAISES, never silently skips ===")
    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        usda, mroot, cat = _build_env(base, {"Foo": {"base/foo.png": "base/foo.png"}}, [("Ghost", 0)])
        raised = False
        try:
            P.materialize_portable(usda, mroot, cat)
        except P.PortableError:
            raised = True
        check(raised, "materialize raises PortableError on an identity absent from the catalog")


def test_missing_texture_raises():
    print("=== a .mtlx referencing a nonexistent texture RAISES ===")
    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        usda, mroot, cat = _build_env(base, {"Foo": {"base/foo.png": "base/foo.png"}}, [("Foo", 0)])
        # Corrupt: point Foo.mtlx at a texture that isn't on disk.
        mtlx = mroot / "materials" / "Foo.mtlx"
        mtlx.write_text(mtlx.read_text().replace("base/foo.png", "base/GONE.png"))
        raised = False
        try:
            P.materialize_portable(usda, mroot, cat)
        except P.PortableError:
            raised = True
        check(raised, "materialize raises PortableError on a missing referenced texture")


def test_no_refs_raises():
    print("=== a .usda with no bare library refs RAISES (not a lightweight asset) ===")
    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        usda, mroot, cat = _build_env(base, {"Foo": {"base/foo.png": "base/foo.png"}}, [("Foo", 0)])
        usda.write_text("#usda 1.0\ndef Xform \"root\" {}\n")  # strip the refs
        raised = False
        try:
            P.materialize_portable(usda, mroot, cat)
        except P.PortableError:
            raised = True
        check(raised, "materialize raises PortableError when no @<id>.mtlx@ refs are present")


def test_basename_collision_raises():
    print("=== same texture basename from DISTINCT sources RAISES (no silent wrong-texture) ===")
    with tempfile.TemporaryDirectory() as d:
        base = Path(d)
        # Foo and Bar each reference a DIFFERENT-dir texture that flattens to the SAME basename.
        usda, mroot, cat = _build_env(base, {
            "Foo": {"a/tex.png": "a/tex.png"},
            "Bar": {"b/tex.png": "b/tex.png"},
        }, [("Foo", 0), ("Bar", 0)])
        raised = False
        try:
            P.materialize_portable(usda, mroot, cat)
        except P.PortableError:
            raised = True
        check(raised, "materialize raises PortableError on a basename collision from distinct sources")


def main():
    test_two_way_lightweight_to_portable()
    test_texture_dedup_across_materials()
    test_unknown_identity_raises()
    test_missing_texture_raises()
    test_no_refs_raises()
    test_basename_collision_raises()
    print("=== %d checks failed ===" % len(_fails))
    return 1 if _fails else 0


if __name__ == "__main__":
    sys.exit(main())
