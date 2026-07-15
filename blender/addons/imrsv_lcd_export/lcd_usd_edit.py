#!/usr/bin/env python
"""IMRSV LCD USD-edit — pxr-free, syntax-aware ASCII-.usda transform (Phase 60 §11 round-3).

The internal step of the Blender LCD export add-on. The stock `wm.usd_export` carries each
Creator LCD edit as a `userProperties:<port>` attribute on the exported Material prim; this
module rewrites those into spec-clean, standard `inputs:<port>` UsdShade overrides and strips
the off-spec `userProperties:` bridge (Discovery 9: standard `inputs:` is the sole carrier).

WHY pxr-free: Fedora's Blender ships USD as a C++-only monolith (no `pxr` Python module), so
this must run *in Blender's own Python* — a bundled `usd-core`/pxr is not viable there. Rather
than a naive `re.sub`, the transform is SYNTAX-AWARE: it tracks the USD-ASCII prim/scope
structure (a `def <Type> "<name>"` header + its `{ }` body, ignoring braces inside strings,
comments, and `( )` prim-metadata blocks where USD dictionaries live) so it converts ONLY the
`userProperties:<lcd-port>` attributes that sit directly inside a `Material` prim — multiple
materials and nested scopes are handled correctly. Acceptance is SEMANTIC equivalence to the
pxr path (verified by opening the result with `pxr` in the tests), not byte-equality.

Bounded assumption: dictionaries appear only inside `( )` prim-metadata (true for Blender's
USD export); attribute-level dictionary *defaults* are not supported.

Contract (LCDSchema.md, Phase 53 D3 — the 5 travel scalars; UV placement is Studio-side, S3):

    base_color_tint    color3   range [0,1]^3        -> color3f inputs:base_color_tint
    overlay1_density    float   range [0,1]          -> float   inputs:overlay1_density
    overlay2_density    float   range [0,1]          -> float   inputs:overlay2_density
    maskset_blend       float   range [0,1]          -> float   inputs:maskset_blend
    roughness_bias      float   range [-0.5,+0.5]    -> float   inputs:roughness_bias

Rules (Phase 60 §11):
  * REJECT — an out-of-range or malformed LCD value fails the whole export (never clamped).
  * An unknown `userProperties:` attr (not an LCD port) is left untouched.
  * `.usda` ASCII only — a `.usd`/`.usdc` crate path is rejected LOUDLY (never mangled).
  * Transactional (temp + atomic rename) and idempotent (a 2nd run is a no-op).

Exit codes (CLI, retained for tooling/back-compat): 0 = ok; 2 = REJECT (out-of-range /
malformed); 3 = not an ASCII .usda.
"""
import os
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


class LcdError(Exception):
    """Base for LCD transform failures; carries a CLI exit `code`."""
    code = 1


class LcdRejected(LcdError):
    """An out-of-range or malformed LCD value — the whole export is rejected."""
    code = 2


class LcdFormatError(LcdError):
    """The target is not an ASCII `.usda` (a crate `.usd`/`.usdc` is refused loudly)."""
    code = 3


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
        return None  # unknown userProperty (e.g. blender:data_name) — leave it alone
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


def transform_text(text):
    """Convert every Material-scoped LCD `userProperties:<port>` into a standard
    `inputs:<port>` and strip the bridge. Returns (new_text, [(prim_path, port, value)]).
    Raises LcdRejected on an out-of-range/malformed value (caller writes nothing)."""
    lines = text.splitlines(keepends=True)
    out_lines = []
    converted = []
    paren_depth = 0
    in_string = False
    scope_stack = []      # (type, name) per open prim body
    pending = None        # (type, name) awaiting its '{'

    for raw_line in lines:
        cur = scope_stack[-1] if scope_stack else None
        new_line = raw_line
        if cur is not None and cur[0] == "Material" and paren_depth == 0 and not in_string:
            rw = _maybe_rewrite_userprop_line(raw_line)
            if rw is not None:
                new_line, (port, value) = rw
                converted.append((cur[1], port, value))
        out_lines.append(new_line)
        paren_depth, in_string, scope_stack, pending = _advance(
            raw_line, paren_depth, in_string, scope_stack, pending)

    return "".join(out_lines), converted


def transform_file(path):
    """Transactionally convert a `.usda` in place. Returns the conversion list. Writes only
    when there is something to convert (idempotent). Raises LcdFormatError on a non-.usda path
    and LcdRejected on an out-of-range/malformed value (leaving the original untouched)."""
    if not path.endswith(".usda"):
        raise LcdFormatError("only ASCII .usda is supported; refusing " + path)
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    new_text, converted = transform_text(text)
    if converted and new_text != text:
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
