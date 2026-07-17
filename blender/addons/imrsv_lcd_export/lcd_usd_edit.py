#!/usr/bin/env python
"""IMRSV LCD USD-edit — pxr-free, syntax-aware ASCII-.usda transform (Phase 60 §11 round-3;
Phase 60sq1 Step 1 output-boundary rebuild).

The internal step of the Blender LCD export add-on. The stock `wm.usd_export` emits a
whole-scene USD with a UsdPreviewSurface (or a minimal placeholder `previewShader`) per
material, a `_materials` scope, and the Creator's LCD edits as `userProperties:<port>` attrs.
This module rewrites that raw export into the **Open Matter Creator asset** shape pinned by
`IMRSV_Platform_Documentation/MatterLibrary/Contract/CreatorAssetProfile.md`, in one pxr-free
pass over the ASCII `.usda`:

  1. Convert each Material-scoped LCD `userProperties:<port>` into a standard `inputs:<port>`
     UsdShade override and strip the off-spec `userProperties:` bridge (Discovery 9: standard
     `inputs:` is the sole carrier).
  2. Reshape each `_materials` Material into the lightweight profile form (Phase 60sq1 Step 1):
       * STRIP the exporter's shader network (`def Shader …` subtrees) and its
         `token outputs:surface[.connect]` — the material IS the referenced Matter `.mtlx`,
         not a preview/proxy network (profile "Forbidden: no UsdPreviewSurface").
       * STRIP the `userProperties:blender:*` bridge (data_name/etc.).
       * AUTHOR the bare library reference `@<id>.mtlx@</MaterialX/Materials/<id>>` and the
         exact-identity carrier `assetInfo:identifier = "<id>"` (profile rules 4/5). The
         material prim becomes a typeless `def "<name>"` whose type comes from the reference.
       * IDENTITY `<id>` = the durable `userProperties:imrsv_matter_identity` carrier on the
         Material prim (E8 correction §1 / profile rule 5) — a Blender ID custom property the
         Asset-Browser generator authors, PRESERVED across datablock duplication, so two meshes
         bound to copies of one Matter datablock both carry the SAME `assetInfo:identifier` as
         independent instances WITHOUT ever inferring identity from the datablock display name.
         Falls back to the `_NNN`-strip heuristic (`canonical_identity`) only for a transitional
         material that carries no such property. This retires reliance on the Stage consumer's
         `StripBlenderDuplicateSuffix` (profile rule 5).
  3. Stamp the composition's ONE required Matter release into root-layer `customLayerData`
     under `imrsv:matterlibRelease` (profile rule 7 / Phase 60sq1 RD-2).

WHY pxr-free: Fedora's Blender ships USD as a C++-only monolith (no `pxr` Python module), so
this must run *in Blender's own Python*. Rather than a naive `re.sub`, the transform is
SYNTAX-AWARE: it tracks the USD-ASCII prim/scope structure (a `def <Type> "<name>"` header +
its `{ }` body, ignoring braces inside strings, comments, and `( )` prim-metadata blocks where
USD dictionaries live) so it reshapes ONLY prims that are direct `Material` children. Multiple
materials and nested scopes are handled correctly. Acceptance is SEMANTIC equivalence to a
pxr-authored asset (verified by opening the result with `pxr` in the tests), not byte-equality.

Idempotent by construction: a reshaped material is a typeless `def "<name>"` (no longer a
`def Material`), so a 2nd pass does not re-match it; the release stamp is skipped when already
present. Running the transform on its own output is a no-op.

Bounded assumptions (true for Blender's USD export): dictionaries appear only inside `( )`
prim-metadata; a `def Material` header carries no inline `( )` metadata block (Blender writes
prim metadata on following lines, and materials get none); Matter identity names are
`[A-Za-z0-9_]` so the `_NNN` duplicate-suffix strip never truncates a real name (they end
`_v01`/`_s01`, never a bare `_NNN`).

Contract (LCDSchema.md, Phase 53 D3 — the 5 travel scalars; UV placement is Studio-side, S3):

    base_color_tint    color3   range [0,1]^3        -> color3f inputs:base_color_tint
    overlay1_density    float   range [0,1]          -> float   inputs:overlay1_density
    overlay2_density    float   range [0,1]          -> float   inputs:overlay2_density
    maskset_blend       float   range [0,1]          -> float   inputs:maskset_blend
    roughness_bias      float   range [-0.5,+0.5]    -> float   inputs:roughness_bias

Rules (Phase 60 §11):
  * REJECT — an out-of-range or malformed LCD value fails the whole export (never clamped).
  * An unknown `userProperties:` attr (not an LCD port, not the blender bridge) is left untouched.
  * `.usda` ASCII only — a `.usd`/`.usdc` crate path is rejected LOUDLY (never mangled).
  * Transactional (temp + atomic rename) and idempotent (a 2nd run is a no-op).

Exit codes (CLI, retained for tooling/back-compat): 0 = ok; 2 = REJECT (out-of-range /
malformed); 3 = not an ASCII .usda.
"""
import os
import re
import sys
import tempfile

# port -> (kind, low, high). kind: "color3" -> color3f; "float" -> float.
LCD_PORTS = {
    "base_color_tint": ("color3", 0.0, 1.0),
    "overlay1_density": ("float", 0.0, 1.0),
    "overlay2_density": ("float", 0.0, 1.0),
    "maskset_blend": ("float", 0.0, 1.0),
    "roughness_bias": ("float", -0.5, 0.5),
}

USERPROP_PREFIX = "userProperties:"
_DEF_KEYWORDS = ("def ", "over ", "class ")

# Profile rule 7 (Phase 60sq1 RD-2) — the ONE required Matter release, stamped on the root layer.
MATTERLIB_RELEASE = "matterlib-0.1.0"
RELEASE_KEY = "imrsv:matterlibRelease"

# Blender's duplicate-datablock suffix on the USD-sanitized prim name (`.001` -> `_001`).
_DUP_SUFFIX_RE = re.compile(r"_\d{3}$")

# Durable canonical-identity carrier (Phase 60sq1 E8 correction §1 / CreatorAssetProfile.md rule 5).
# The Asset-Browser generator authors this as a Blender ID custom property on the material; it is
# PRESERVED when the Creator duplicates the material, and rides out through the stock USD export
# (`export_custom_properties=True`) as `userProperties:imrsv_matter_identity` on the Material prim.
# The reshape reads it AUTHORITATIVELY — identity is NEVER inferred from the datablock display name
# when this carrier is present (rule 5: "a producer never relies on Blender datablock display-name
# collision suffixes (_001) as semantic identity"). The `_NNN`-strip below is interim scaffolding
# for the transitional case where the carrier is absent (a hand-authored material without it).
IDENTITY_PROP = "imrsv_matter_identity"
IDENTITY_USERPROP = USERPROP_PREFIX + IDENTITY_PROP


class LcdError(Exception):
    """Base for LCD transform failures; carries a CLI exit `code`."""
    code = 1


class LcdRejected(LcdError):
    """An out-of-range or malformed LCD value — the whole export is rejected."""
    code = 2


class LcdFormatError(LcdError):
    """The target is not an ASCII `.usda` (a crate `.usd`/`.usdc` is refused loudly)."""
    code = 3


def canonical_identity(prim_name):
    """INTERIM fallback identity for a material prim that carries NO durable `imrsv_matter_identity`
    carrier (E8 correction §1): the prim name with Blender's duplicate-datablock suffix (`_NNN`)
    removed. `Copper…_v01_001` -> `Copper…_v01`; a non-duplicate name is returned unchanged. The
    AUTHORITATIVE path reads the durable carrier (see `_scan_identities`); this heuristic exists
    only for a transitional material without it and retires when the generator authors the carrier
    on every article."""
    return _DUP_SUFFIX_RE.sub("", prim_name)


def _identity_userprop_value(stripped):
    """If `stripped` is a Material-scoped `[custom] string userProperties:imrsv_matter_identity =
    "<value>"` line, return the quoted `<value>` (the durable canonical-identity carrier). Return
    None otherwise. This is the durable property that survives datablock duplication — read in a
    pre-scan so the reshaped header can author `assetInfo:identifier` from it, never from the name."""
    if "=" not in stripped:
        return None
    lhs, _, rhs = stripped.partition("=")
    toks = lhs.split()
    if not toks or toks[-1] != IDENTITY_USERPROP:
        return None
    rhs = rhs.strip()
    if rhs.startswith('"'):
        q2 = rhs.find('"', 1)
        if q2 > 0:
            return rhs[1:q2]
    return None


def _scan_identities(text):
    """Pre-scan pass: walk the USD-ASCII structure once and record, per direct-child Material prim,
    the durable identity carried on `userProperties:imrsv_matter_identity`. Returns {prim_name:
    identity}. The reshape's header authoring reads this so identity comes from the durable carrier
    (rule 5), not the datablock display name — needed because the carrier is a Material BODY line
    (seen after the header in a single forward pass)."""
    identities = {}
    paren_depth = 0
    in_string = False
    scope_stack = []
    pending = None
    for raw_line in text.splitlines(keepends=True):
        cur = scope_stack[-1] if scope_stack else None
        if (cur is not None and cur[0] == "Material"
                and paren_depth == 0 and not in_string):
            val = _identity_userprop_value(raw_line.lstrip())
            if val is not None:
                identities[cur[1]] = val
        paren_depth, in_string, scope_stack, pending = _advance(
            raw_line, paren_depth, in_string, scope_stack, pending)
    return identities


def _fmt(v):
    """Compact, round-trippable float text (always carries a decimal point)."""
    return repr(float(v))


def _parse_floats(raw):
    s = raw.strip()
    if s.startswith("(") and s.endswith(")"):
        s = s[1:-1]
    out = []
    for tok in s.split(","):
        tok = tok.strip()
        if tok:
            out.append(float(tok))
    return out


def _validate(port, raw):
    """Return (kind, [floats]) for a known LCD port; raise LcdRejected on malformed/out-of-range."""
    kind, low, high = LCD_PORTS[port]
    try:
        vals = _parse_floats(raw)
    except (TypeError, ValueError):
        raise LcdRejected("%s malformed value: %r" % (port, raw.strip()))
    if kind == "color3" and len(vals) != 3:
        raise LcdRejected("%s expected 3 channels, got %d: %r" % (port, len(vals), raw.strip()))
    if kind == "float" and len(vals) != 1:
        raise LcdRejected("%s expected 1 value, got %d: %r" % (port, len(vals), raw.strip()))
    for v in vals:
        if v < low or v > high:
            raise LcdRejected("%s value %g out of range [%g, %g]" % (port, v, low, high))
    return kind, vals


def _detect_def(stripped):
    """If `stripped` is a def/over/class prim header, return (type, name) — type is "" for a
    typeless `def "Name"`. Otherwise None."""
    for kw in _DEF_KEYWORDS:
        if stripped.startswith(kw):
            rest = stripped[len(kw):].lstrip()
            if rest.startswith('"'):
                dtype = ""
            else:
                parts = rest.split(None, 1)
                dtype = parts[0] if parts else ""
                rest = parts[1] if len(parts) > 1 else ""
            q1 = rest.find('"')
            name = ""
            if q1 >= 0:
                q2 = rest.find('"', q1 + 1)
                name = rest[q1 + 1:q2] if q2 > q1 else ""
            return dtype, name
    return None


def _advance(line, paren_depth, in_string, scope_stack, pending):
    """Advance the structural state across one raw line. `scope_stack` holds (type, name)
    tuples per open prim body; `pending` is the (type, name) awaiting its `{`."""
    header = _detect_def(line.lstrip())
    if header is not None:
        pending = header
    i, n = 0, len(line)
    while i < n:
        c = line[i]
        if in_string:
            if c == "\\":
                i += 2
                continue
            if c == '"':
                in_string = False
            i += 1
            continue
        if c == '"':
            in_string = True
        elif c == "#":
            break  # comment to end of line
        elif c == "(":
            paren_depth += 1
        elif c == ")":
            if paren_depth > 0:
                paren_depth -= 1
        elif paren_depth == 0:
            if c == "{":
                scope_stack.append(pending if pending is not None else ("", ""))
                pending = None
            elif c == "}":
                if scope_stack:
                    scope_stack.pop()
        i += 1
    return paren_depth, in_string, scope_stack, pending


def _maybe_rewrite_userprop_line(line):
    """If `line` is a Material-scoped `[custom] <type> userProperties:<lcd-port> = <value>`
    assignment, return (new_line, (port, value)). Return None to leave the line untouched.
    Raise LcdRejected on an out-of-range/malformed LCD value."""
    eol = ""
    body = line
    if body.endswith("\n"):
        body, eol = body[:-1], "\n"
    if body.endswith("\r"):
        body, eol = body[:-1], "\r" + eol
    if "=" not in body:
        return None
    lhs, _, rhs = body.partition("=")
    lhs_tokens = lhs.split()
    if not lhs_tokens:
        return None
    name = lhs_tokens[-1]
    if not name.startswith(USERPROP_PREFIX):
        return None
    port = name[len(USERPROP_PREFIX):]
    if port not in LCD_PORTS:
        return None  # unknown userProperty (e.g. blender:data_name) — handled elsewhere
    kind, vals = _validate(port, rhs)
    indent = body[: len(body) - len(body.lstrip())]
    if kind == "color3":
        new_body = "%scolor3f inputs:%s = (%s, %s, %s)" % (
            indent, port, _fmt(vals[0]), _fmt(vals[1]), _fmt(vals[2]))
        value = tuple(round(v, 6) for v in vals)
    else:
        new_body = "%sfloat inputs:%s = %s" % (indent, port, _fmt(vals[0]))
        value = round(vals[0], 6)
    return new_body + eol, (port, value)


def _is_material_junk(stripped):
    """A Material-body line stripped by the reshape: the exporter's surface output plug, the
    `userProperties:blender:*` bridge (data_name/etc.), and the durable `imrsv_matter_identity`
    carrier (consumed into `assetInfo:identifier` by the pre-scan — it is a bridge, not spec)."""
    if stripped.startswith("token outputs:surface"):
        return True
    if "=" in stripped:
        lhs = stripped.partition("=")[0].split()
        if lhs and (lhs[-1].startswith("userProperties:blender:")
                    or lhs[-1] == IDENTITY_USERPROP):
            return True
    return False


def _material_metadata_block(indent, name, ident):
    """The reshaped material header: keep the ORIGINAL prim `name` (so `material:binding`
    targets still resolve and the two same-identity instances stay distinct prims), and author
    the bare library reference + exact-identity carrier from the canonical `ident` (rules 4/5)."""
    return (
        '%sdef "%s" (\n'
        '%s    prepend references = @%s.mtlx@</MaterialX/Materials/%s>\n'
        '%s    assetInfo = {\n'
        '%s        string identifier = "%s"\n'
        '%s    }\n'
        '%s)\n'
    ) % (indent, name, indent, ident, ident, indent, indent, ident, indent, indent)


def transform_text(text):
    """Reshape a raw Blender USD export into the Open Matter Creator lightweight asset form
    (Phase 60sq1 Step 1). Returns (new_text, [(prim_path, port, value)]) — the conversion list
    is the LCD `inputs:` authored. Raises LcdRejected on an out-of-range/malformed LCD value
    (caller writes nothing). Idempotent."""
    lines = text.splitlines(keepends=True)
    identities = _scan_identities(text)   # durable carrier per Material prim (rule 5); {} if none
    out_lines = []
    converted = []
    paren_depth = 0
    in_string = False
    scope_stack = []          # (type, name) per open prim body
    pending = None            # (type, name) awaiting its '{'
    seen_prim = False         # first top-level prim seen -> layer metadata is closed
    release_done = (RELEASE_KEY in text)   # idempotency: don't re-stamp
    strip_base = None         # material-body depth while dropping a shader subtree
    strip_armed = False       # waiting for the shader subtree's '{' to open

    for raw_line in lines:
        stripped = raw_line.lstrip()
        cur = scope_stack[-1] if scope_stack else None

        # --- dropping a shader subtree inside a Material ---
        if strip_base is not None:
            paren_depth, in_string, scope_stack, pending = _advance(
                raw_line, paren_depth, in_string, scope_stack, pending)
            if strip_armed:
                if len(scope_stack) > strip_base:
                    strip_armed = False
            elif len(scope_stack) <= strip_base:
                strip_base = None
            continue

        in_material_body = (cur is not None and cur[0] == "Material"
                            and paren_depth == 0 and not in_string)

        # --- inside a Material body: strip network / bridge, convert LCD ---
        if in_material_body:
            hdr = _detect_def(stripped)
            if hdr is not None:
                # a child def (the shader network) -> drop its whole subtree
                strip_base = len(scope_stack)
                strip_armed = True
                paren_depth, in_string, scope_stack, pending = _advance(
                    raw_line, paren_depth, in_string, scope_stack, pending)
                continue
            if _is_material_junk(stripped):
                paren_depth, in_string, scope_stack, pending = _advance(
                    raw_line, paren_depth, in_string, scope_stack, pending)
                continue
            rw = _maybe_rewrite_userprop_line(raw_line)
            if rw is not None:
                new_line, (port, value) = rw
                converted.append((cur[1], port, value))
                out_lines.append(new_line)
                paren_depth, in_string, scope_stack, pending = _advance(
                    raw_line, paren_depth, in_string, scope_stack, pending)
                continue
            out_lines.append(raw_line)
            paren_depth, in_string, scope_stack, pending = _advance(
                raw_line, paren_depth, in_string, scope_stack, pending)
            continue

        top_level_header = (paren_depth == 0 and not in_string
                            and _detect_def(stripped) is not None)

        # --- Material HEADER: retype typeless + inject reference/assetInfo ---
        if top_level_header:
            dtype, name = _detect_def(stripped)
            if dtype == "Material":
                indent = raw_line[: len(raw_line) - len(raw_line.lstrip())]
                # AUTHORITATIVE: the durable carrier (rule 5). Fall back to the `_NNN` strip only
                # for a transitional material that carries no carrier (E8 correction §1).
                ident = identities.get(name)
                if ident is None:
                    ident = canonical_identity(name)
                out_lines.append(_material_metadata_block(indent, name, ident))
                paren_depth, in_string, scope_stack, pending = _advance(
                    raw_line, paren_depth, in_string, scope_stack, pending)
                seen_prim = True
                continue
            seen_prim = True

        # --- layer-metadata release stamp (before the layer '( )' closes) ---
        if (not seen_prim and not release_done and paren_depth == 1
                and stripped.startswith(")")):
            out_lines.append('    customLayerData = {\n')
            out_lines.append('        string "%s" = "%s"\n' % (RELEASE_KEY, MATTERLIB_RELEASE))
            out_lines.append('    }\n')
            release_done = True

        out_lines.append(raw_line)
        paren_depth, in_string, scope_stack, pending = _advance(
            raw_line, paren_depth, in_string, scope_stack, pending)

    return "".join(out_lines), converted


def transform_file(path):
    """Transactionally reshape a `.usda` in place. Returns the LCD conversion list. Raises
    LcdFormatError on a non-.usda path and LcdRejected on an out-of-range/malformed value
    (leaving the original untouched). Idempotent."""
    if not path.endswith(".usda"):
        raise LcdFormatError("only ASCII .usda is supported; refusing " + path)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    new_text, converted = transform_text(text)
    if new_text != text:
        d = os.path.dirname(os.path.abspath(path))
        fd, tmp = tempfile.mkstemp(dir=d, prefix=".lcd_", suffix=".usda.tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(new_text)
            os.replace(tmp, path)  # atomic within the same directory
        except BaseException:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise
    return converted


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("usage: lcd_usd_edit.py <exported.usda>\n")
        return 2
    try:
        converted = transform_file(argv[1])
    except LcdError as e:
        sys.stderr.write("IMRSV_LCD_%s: %s\n" %
                         ("REJECT" if isinstance(e, LcdRejected) else "ERROR", e))
        return e.code
    for path, port, val in converted:
        print("IMRSV_LCD_CONVERTED %s %s = %s" % (path, port, val))
    print("IMRSV_LCD_CONVERTED_COUNT %d" % len(converted))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
