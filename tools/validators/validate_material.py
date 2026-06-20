#!/usr/bin/env python3
"""Per-material conformance validator (Phase 53).

Asserts the *contract*, not just MaterialX schema (§6 non-golden observable: a doc can
`validate()==True` while burying the LCD as constants or being multi-file). Each check is a
named pass/fail with an artifact line. Run per `.mtlx`:

    validate_material.py <file.mtlx> [<file.mtlx> ...]

Checks:
  * SDK validate    — mx.readFromXmlString + doc.validate() with the MaterialX stdlib loaded
  * single-file     — no <xi:include> / <include> / external .mtlx reference (S7)
  * OpenPBR-only    — exactly one open_pbr_surface; zero standard_surface
  * LCD-as-input    — every exposed LCD control is a wired nodegraph interface input from the
                      frozen vocabulary (not a buried constant) — the load-bearing §6 catch
  * identity grammar— <surfacematerial> name == filename stem, <=63 / [A-Za-z0-9_] / token shape
  * texture locality— every <image> file path is relative and resolves on disk

Exit code 0 iff every check passes on every file.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import MaterialX as mx

# One source of truth for the frozen LCD vocabulary (LCDSchema.md, D3).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "converters"))
from assemble_mtlx import LCD_PORTS  # noqa: E402

SCALE_TAGS = {"s0001", "s001", "s01", "s1", "s10", "s100", "sUKN"}
SYSTEM_EXEMPT = {"IMRSV_MissingMaterial"}   # off-grammar system material (MasterSet.md)
IDENT_RE = re.compile(r"^[A-Za-z0-9_]+$")
VERSION_RE = re.compile(r"^v\d+$")

_STDLIB = None


def _stdlib():
    """Load + cache the MaterialX stdlib (needed so OpenPBR/unit defs resolve in validate())."""
    global _STDLIB
    if _STDLIB is None:
        _STDLIB = mx.createDocument()
        mx.loadLibraries(mx.getDefaultDataLibraryFolders(),
                         mx.getDefaultDataSearchPath(), _STDLIB)
    return _STDLIB


def check_grammar(stem: str) -> list:
    """Return a list of grammar errors ([] == conformant). The per-work-item structural guard."""
    errors = []
    if len(stem) > 63:
        errors.append(f"length {len(stem)} > 63")
    if not IDENT_RE.match(stem):
        errors.append("charset: contains non-[A-Za-z0-9_]")
    if stem in SYSTEM_EXEMPT:
        return errors                       # system material: length + charset only
    toks = stem.split("_")
    if len(toks) < 4:
        errors.append(f"too few tokens ({len(toks)}); expected Material_Variant_..._sNN_vNN")
        return errors
    if toks[-2] not in SCALE_TAGS:
        errors.append(f"scale tag {toks[-2]!r} not in {sorted(SCALE_TAGS)}")
    if not VERSION_RE.match(toks[-1]):
        errors.append(f"version {toks[-1]!r} not 'vNN'")
    return errors


def _own_doc(xml: str):
    doc = mx.createDocument()
    mx.readFromXmlString(doc, xml)
    return doc


def validate_file(path: Path) -> list:
    """Run every check; return list of (check, ok, detail) tuples."""
    results = []
    xml = path.read_text(encoding="utf-8")
    doc = _own_doc(xml)

    # --- SDK validate (with stdlib) ---
    vdoc = _own_doc(xml)
    vdoc.importLibrary(_stdlib())
    valid, msg = vdoc.validate()
    results.append(("sdk-validate", valid, "ok" if valid else msg.strip().replace("\n", " | ")))

    # --- single-file ---
    bad_include = ("<xi:include" in xml) or ("<include" in xml)
    # an <image>/<tiledimage> 'file' is a texture, fine; a .mtlx reference is not
    ext_mtlx = bool(re.search(r'value="[^"]*\.mtlx"', xml))
    sf_ok = not bad_include and not ext_mtlx
    results.append(("single-file", sf_ok,
                    "ok" if sf_ok else "found include or external .mtlx reference"))

    # --- OpenPBR-only ---
    openpbr = [n for n in doc.getNodes() if n.getCategory() == "open_pbr_surface"]
    standard = [n for n in doc.getNodes() if n.getCategory() == "standard_surface"]
    op_ok = (len(openpbr) == 1 and len(standard) == 0)
    results.append(("openpbr-only", op_ok,
                    f"open_pbr_surface={len(openpbr)} standard_surface={len(standard)}"))

    # --- LCD-as-interface-inputs ---
    lcd_errs = []
    exposed = []
    referenced = set()
    for ng in doc.getNodeGraphs():
        iface = [i.getName() for i in ng.getInputs()]
        exposed.extend(iface)
        for name in iface:
            if name not in LCD_PORTS:
                lcd_errs.append(f"rogue interface input {name!r} (not in frozen LCD vocabulary)")
        for node in ng.getNodes():
            for inp in node.getInputs():
                ref = inp.getAttribute("interfacename")
                if ref:
                    referenced.add(ref)
            if node.getCategory() == "constant" and node.getName() in LCD_PORTS:
                lcd_errs.append(f"LCD port {node.getName()!r} buried as a constant node")
    for name in exposed:
        if name not in referenced:
            lcd_errs.append(f"interface input {name!r} declared but not wired (dead)")
    results.append(("lcd-as-input", not lcd_errs,
                    f"exposed={exposed}" if not lcd_errs else "; ".join(lcd_errs)))

    # --- identity grammar (name == stem, grammar) ---
    surfmats = [n for n in doc.getNodes() if n.getCategory() == "surfacematerial"]
    g_errs = []
    if len(surfmats) != 1:
        g_errs.append(f"expected 1 surfacematerial, found {len(surfmats)}")
    else:
        name = surfmats[0].getName()
        if name != path.stem:
            g_errs.append(f"surfacematerial name {name!r} != filename stem {path.stem!r}")
        g_errs.extend(check_grammar(name))
    results.append(("identity-grammar", not g_errs,
                    surfmats[0].getName() if (len(surfmats) == 1 and not g_errs)
                    else "; ".join(g_errs)))

    # --- texture-path locality ---
    t_errs = []
    images = [n for n in doc.getNodes() if n.getCategory() in ("image", "tiledimage")]
    for img in doc.getNodeGraphs():
        images.extend([n for n in img.getNodes() if n.getCategory() in ("image", "tiledimage")])
    for img in images:
        fin = img.getInput("file")
        if fin is None:
            continue
        fpath = fin.getValueString()
        if not fpath:
            continue
        if fpath.startswith("/") or "://" in fpath:
            t_errs.append(f"{fpath}: not relative")
            continue
        resolved = (path.parent / fpath).resolve()
        if not resolved.exists():
            t_errs.append(f"{fpath}: does not resolve on disk")
    results.append(("texture-locality", not t_errs,
                    "ok" if not t_errs else "; ".join(t_errs)))

    return results


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    if not argv:
        print("usage: validate_material.py <file.mtlx> [...]", file=sys.stderr)
        return 2
    all_ok = True
    for arg in argv:
        path = Path(arg)
        print(f"== {path.name} ==")
        try:
            results = validate_file(path)
        except Exception as exc:  # noqa: BLE001
            print(f"  ERROR: {exc}")
            all_ok = False
            continue
        for check, ok, detail in results:
            mark = "PASS" if ok else "FAIL"
            print(f"  [{mark}] {check}: {detail}")
            all_ok = all_ok and ok
    print("RESULT:", "ALL PASS" if all_ok else "FAILURES")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
