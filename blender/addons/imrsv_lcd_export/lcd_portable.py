"""Complete-portable materializer for the Open Matter Creator exporter (Phase 60sq1, Step 5 / RD-4).

The SECOND producer mode (the default is the lightweight, library-linked form). Given a reshaped
lightweight `.usda` (bare `@<id>.mtlx@` library references), materialize each referenced Matter
`.mtlx` + its texture set ONCE into the package directory, rewrite every texture reference to a
portable `textures/<base>` form, and rewrite the `.usda`'s bare library refs to local `@./<id>.mtlx@`.
The result opens and renders in a reference app with NO PXR_AR_DEFAULT_SEARCH_PATH and no access to
the installed Matter Library — the RD-4 self-contained independence guarantee.

pxr-free by design (file copy + MaterialX-text rewrite only) — GENERALIZES
`tools/conformance/build_portable.py` (which does this for the single golden Copper) to the N
materials a real export references, resolving each source `.mtlx` through the release catalog
(identity == the `.mtlx` basename stem == the `assetInfo:identifier` the lightweight form carries).
Deterministic: same inputs -> byte-identical package. Never silently skips — an unresolvable
identity, a missing texture, or a basename collision from distinct sources RAISES.
"""
import json
import re
import shutil
from pathlib import Path

# A bare library reference in the reshaped lightweight `.usda` (mirrors assert_profile.py's ref scan;
# the lightweight form is `references = @<id>.mtlx@</...>`, id == [A-Za-z0-9_]+).
_USDA_REF_RE = re.compile(r'references\s*=\s*@([A-Za-z0-9_]+)\.mtlx@')
# A texture file reference inside a MaterialX `.mtlx` (mirrors build_portable.py).
_MTLX_FILE_RE = re.compile(r'name="file" type="filename" value="([^"]+)"')


class PortableError(Exception):
    """The lightweight asset cannot be materialized into a self-contained portable package."""


def _load_catalog_index(catalog_path):
    """Map each catalog material's identity (== its `.mtlx` basename stem) -> its `payload_path`
    (a path relative to the Matter-Library MatterLibrary root)."""
    cat = json.loads(Path(catalog_path).read_text())
    index = {}
    for m in cat.get("materials", []):
        pp = m.get("payload_path")
        if pp:
            index[Path(pp).stem] = pp
    return index


def materialize_portable(usda_path, matterlib_root, catalog_path):
    """Convert the lightweight `.usda` at `usda_path` into its complete-portable form IN PLACE.

    * `matterlib_root` — the dir `payload_path` values are relative to (Matter-Library/MatterLibrary).
    * `catalog_path`   — the release catalog JSON (resolves identity -> payload_path).

    Writes each referenced `<id>.mtlx` (its textures flattened into `./textures/`) beside the `.usda`
    and rewrites every bare `@<id>.mtlx@` ref to a local `@./<id>.mtlx@`. A single shared `copied`
    dict dedups textures across ALL materials (shared overlays/masks are materialized once). Returns
    the sorted list of materialized identities. Raises `PortableError` on any unresolvable input.
    """
    usda_path = Path(usda_path)
    matterlib_root = Path(matterlib_root)
    index = _load_catalog_index(catalog_path)

    usda_text = usda_path.read_text()
    ids = sorted(set(_USDA_REF_RE.findall(usda_text)))
    if not ids:
        raise PortableError(
            "no bare @<id>.mtlx@ library references in %s — not a lightweight Creator asset" % usda_path)

    pkg = usda_path.parent
    tex_dir = pkg / "textures"
    tex_dir.mkdir(parents=True, exist_ok=True)

    copied = {}  # texture basename -> its absolute source path (shared across ALL materials)
    for ident in ids:
        pp = index.get(ident)
        if pp is None:
            raise PortableError(
                "identity %r is not in catalog %s — cannot resolve its .mtlx" % (ident, catalog_path))
        src_mtlx = (matterlib_root / pp).resolve()
        if not src_mtlx.is_file():
            raise PortableError("source .mtlx missing for %r: %s" % (ident, src_mtlx))

        mtlx_text = src_mtlx.read_text()
        for m in _MTLX_FILE_RE.finditer(mtlx_text):
            ref = m.group(1)
            base = Path(ref).name
            tex_src = (src_mtlx.parent / ref).resolve()
            if not tex_src.is_file():
                raise PortableError(
                    "texture %r referenced by %s not found: %s" % (ref, src_mtlx.name, tex_src))
            prev = copied.get(base)
            if prev is None:
                shutil.copy2(tex_src, tex_dir / base)
                copied[base] = tex_src
            elif prev != tex_src:
                raise PortableError(
                    "texture basename collision %r from distinct sources: %s vs %s"
                    % (base, prev, tex_src))
            mtlx_text = mtlx_text.replace('value="%s"' % ref, 'value="textures/%s"' % base)

        (pkg / ("%s.mtlx" % ident)).write_text(mtlx_text)
        usda_text = usda_text.replace("@%s.mtlx@" % ident, "@./%s.mtlx@" % ident)

    usda_path.write_text(usda_text)
    return ids
