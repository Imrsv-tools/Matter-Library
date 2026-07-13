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
  * LCD-as-input    — every exposed control is a wired nodegraph interface input from the
                      TWO-TIER vocabulary (frozen Creator LCD ∪ author tier), not a buried
                      constant, and none is dead — the load-bearing §6 catch
  * master-conformance — the master's DEFINING author-tier carriers are present AND wired
                      (Phase 71). A master that cannot express the one property it exists
                      for is inert; this is the guard that makes that a build failure.
  * overlay/maskset-linear — the three render-role DATA textures load linear, never sRGB
  * identity grammar— <surfacematerial> name == filename stem, <=63 / [A-Za-z0-9_] / token shape
  * texture locality— every <image> file path is relative and resolves on disk

Exit code 0 iff every check passes on every file.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import MaterialX as mx

# One source of truth for both tiers of the vocabulary (LCDSchema.md D3 + §Author tier).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "converters"))
from assemble_mtlx import LCD_PORTS, AUTHOR_TIER_PORTS, DATA_COLORSPACE  # noqa: E402

# The two-tier vocabulary. RD-C: the Creator subset is frozen and untouched; the author
# tier sits BESIDE it. Before Phase 71 this validator knew only the frozen 8, which is
# literally why the Masked cutoff and the TwoLayer layer-2 set were unauthorable.
KNOWN_PORTS = {**LCD_PORTS, **AUTHOR_TIER_PORTS}

SCALE_TAGS = {"s0001", "s001", "s01", "s1", "s10", "s100", "sUKN"}
SYSTEM_EXEMPT = {"IMRSV_MissingMaterial"}   # off-grammar system material (MasterSet.md)
IDENT_RE = re.compile(r"^[A-Za-z0-9_]+$")
VERSION_RE = re.compile(r"^v\d+$")

# The render-role DATA textures (LCDSchema.md §Render-role texture nodes). Packed data —
# an sRGB transfer curve corrupts every channel they carry.
DATA_TEXTURE_NODES = ("overlay1_tex", "overlay2_tex", "maskset_tex")

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


def _master_token(doc) -> str:
    """The master identity token, off the internal imrsv_metadata nodedef ('' if absent)."""
    for nd in doc.getNodeDefs():
        inp = nd.getInput("master_material")
        if inp is not None:
            return inp.getValueString()
    return ""


def _shader_input(doc, name):
    """The named input on the single open_pbr_surface node (None if absent)."""
    for n in doc.getNodes():
        if n.getCategory() == "open_pbr_surface":
            return n.getInput(name)
    return None


def _is_graph_driven(inp) -> bool:
    """True when the input is fed by the nodegraph rather than carrying a literal value."""
    return inp is not None and bool(inp.getAttribute("nodegraph"))


def _iface_inputs(doc) -> dict:
    """Every nodegraph interface input, name -> value string."""
    out = {}
    for ng in doc.getNodeGraphs():
        for i in ng.getInputs():
            out[i.getName()] = i.getValueString()
    return out


def _as_float(s: str, default: float = 0.0) -> float:
    try:
        return float(s)
    except (TypeError, ValueError):
        return default


def check_master_conformance(doc) -> list:
    """The master's DEFINING author-tier carriers are present AND wired (Phase 71).

    Straight off the LCDSchema §Author tier carrier table. Six of the seven masters shipped
    unable to express the one property they exist for; this check is what makes that a
    failure instead of a silently-inert material.
    """
    master = _master_token(doc)
    if master in ("", "Opaque", "system"):
        # Opaque's defining behavior IS base PBR (RD-H) — already covered by the base checks.
        return []

    errs = []
    iface = _iface_inputs(doc)

    def need_shader(name, why):
        if _shader_input(doc, name) is None:
            errs.append(f"{master}: missing {name!r} on the shader — {why}")

    def need_iface(name, why):
        if name not in iface:
            errs.append(f"{master}: missing author-tier input {name!r} — {why}")

    def need_thin_walled(want: bool):
        inp = _shader_input(doc, "geometry_thin_walled")
        if inp is None:
            errs.append(f"{master}: geometry_thin_walled not authored — it is THE OpenPBR "
                        f"thin-vs-thick discriminator; without it Thick and Thin are the "
                        f"same material described twice")
        elif inp.getValueString() != ("true" if want else "false"):
            errs.append(f"{master}: geometry_thin_walled={inp.getValueString()!r}, "
                        f"expected {'true' if want else 'false'}")

    if master == "Masked":
        need_iface("opacity_cutoff", "the cutoff IS this master's defining property")
        op = _shader_input(doc, "geometry_opacity")
        if not _is_graph_driven(op):
            errs.append("Masked: geometry_opacity has no connected source — a cutoff with "
                        "nothing to threshold makes no holes")

    elif master in ("TranslucentThin", "TranslucentThick"):
        need_shader("specular_ior", "IOR is what refracts")
        need_shader("transmission_weight", "nothing transmits at weight 0")
        need_shader("transmission_color", "the absorption/tint colour")
        need_thin_walled(master == "TranslucentThin")
        if master == "TranslucentThick":
            need_shader("transmission_depth",
                        "absorption depth IS Thick's defining property (Beer-Lambert); "
                        "without it Thick is just Thin")

    elif master == "Subsurface":
        need_shader("subsurface_weight", "nothing scatters at weight 0")
        need_shader("subsurface_color", "the SSS colour")
        need_shader("subsurface_radius", "the scattering length scale")
        need_shader("subsurface_radius_scale", "the per-channel mean-free-path multiplier")

    elif master == "Emissive":
        need_shader("emission_color", "emission colour IS this master's defining property")
        lum = _shader_input(doc, "emission_luminance")
        if lum is None or _as_float(lum.getValueString()) <= 0:
            errs.append("Emissive: emission_luminance is absent or 0 — it would not glow")

    elif master == "TwoLayer":
        need_iface("layer_blend_balance", "the blend shaping controls")
        need_iface("layer_blend_contrast", "the blend shaping controls")
        graph_nodes = {n.getName() for ng in doc.getNodeGraphs() for n in ng.getNodes()}
        if "maskset_tex" not in graph_nodes:
            errs.append("TwoLayer: no maskset — maskset.R IS the layer-2 coverage; without "
                        "it nothing says WHERE layer 2 sits")
        layer2 = [p for p in ("layer2_base_color", "layer2_roughness", "layer2_metalness")
                  if p in iface]
        layer2 += [n for n in graph_nodes if n.startswith("layer2_") and n.endswith("_tex")]
        if not layer2:
            errs.append("TwoLayer: no second layer authored — two REAL layers is the whole "
                        "master (MasterSet.md); a clearcoat cannot render rust")
        # The blend is t = k * maskset_blend. At the schema default (0.0) layer 2 is
        # invisible no matter what else the article authors — an inert master.
        blend = iface.get("maskset_blend")
        if blend is None:
            errs.append("TwoLayer: maskset_blend not exposed — it is the maskset's master "
                        "strength; the layer-2 blend is scaled by it")
        elif _as_float(blend) <= 0:
            errs.append(f"TwoLayer: maskset_blend={blend!r} — t = k * maskset_blend, so at 0 "
                        f"layer 2 is invisible however it is authored. Author a nonzero start "
                        f"value.")

    return errs


def check_data_colorspaces(doc) -> list:
    """Overlays + masksets are DATA: they load lin_rec709, never through an sRGB curve.

    Loading a packed data texture (normal XY / roughness bias / mask density) through the
    sRGB transfer curve corrupts every channel it carries.
    """
    errs = []
    for ng in doc.getNodeGraphs():
        for node in ng.getNodes():
            if node.getName() not in DATA_TEXTURE_NODES:
                continue
            cs = node.getColorSpace()
            if cs and cs != DATA_COLORSPACE:
                errs.append(f"{node.getName()}: colorspace {cs!r} — a render-role data "
                            f"texture must load {DATA_COLORSPACE!r} (it is not colour)")
    return errs


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

    # --- LCD-as-interface-inputs (two-tier: frozen Creator vocabulary ∪ author tier) ---
    lcd_errs = []
    exposed = []
    referenced = set()
    for ng in doc.getNodeGraphs():
        iface = [i.getName() for i in ng.getInputs()]
        exposed.extend(iface)
        for name in iface:
            if name not in KNOWN_PORTS:
                lcd_errs.append(f"rogue interface input {name!r} "
                                f"(in neither the frozen LCD vocabulary nor the author tier)")
        for node in ng.getNodes():
            for inp in node.getInputs():
                ref = inp.getAttribute("interfacename")
                if ref:
                    referenced.add(ref)
            if node.getCategory() == "constant" and node.getName() in KNOWN_PORTS:
                lcd_errs.append(f"port {node.getName()!r} buried as a constant node")
    for name in exposed:
        if name not in referenced:
            lcd_errs.append(f"interface input {name!r} declared but not wired (dead)")
    results.append(("lcd-as-input", not lcd_errs,
                    f"exposed={exposed}" if not lcd_errs else "; ".join(lcd_errs)))

    # --- master-conformance: the master's defining author-tier carriers (Phase 71) ---
    mc_errs = check_master_conformance(doc)
    results.append(("master-conformance", not mc_errs,
                    f"{_master_token(doc) or '(none)'}: ok" if not mc_errs
                    else "; ".join(mc_errs)))

    # --- overlay/maskset colour space: data textures load linear (Phase 71) ---
    cs_errs = check_data_colorspaces(doc)
    results.append(("data-texture-linear", not cs_errs,
                    "ok" if not cs_errs else "; ".join(cs_errs)))

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
