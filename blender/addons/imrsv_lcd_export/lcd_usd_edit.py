#!/usr/bin/env python
"""IMRSV LCD USD-edit — the internal-invocation step of the Blender export add-on.

Runs under a USD-capable Python (pxr / usd-core). Fedora's Blender ships USD as a
C++-only monolith (no `pxr` Python module), so the Blender add-on cannot author
UsdShade from inside the export hook; instead it runs the *normal* USD export
(which carries each Creator LCD edit as a `userProperties:<port>` attr on the
Material prim) and then invokes THIS script to rewrite those into spec-clean,
standard `inputs:<port>` UsdShade overrides — one export action, one producer.

Contract (LCDSchema.md, Phase 53 D3 — the 5 travel scalars; UV placement is
Studio-side only, S3):

    base_color_tint    color3   range [0,1]^3        (multiply on base_color)
    overlay1_density   float    range [0,1]          (overlay-1 mix)
    overlay2_density   float    range [0,1]          (overlay-2 mix)
    maskset_blend      float    range [0,1]          (maskset blend)
    roughness_bias     float    range [-0.5,+0.5]    (add on specular_roughness)

Rules (Phase 60 §11):
  * REJECT — an out-of-range or malformed LCD value fails the export (non-zero
    exit + a clear message); values are never silently clamped.
  * An unknown `userProperties:` attr (not an LCD port) is left untouched/ignored.
  * The off-spec `userProperties:<port>` bridge is stripped after conversion —
    standard `inputs:<port>` is the sole final carrier (Discovery 9; no imrsv:).

Exit: 0 = converted (or nothing to convert); 2 = malformed/out-of-range REJECT.
"""
import sys

from pxr import Usd, UsdShade, Sdf, Gf

# port -> (kind, low, high). kind: "color3" clamps each channel; "float" scalar.
LCD_PORTS = {
    "base_color_tint": ("color3", 0.0, 1.0),
    "overlay1_density": ("float", 0.0, 1.0),
    "overlay2_density": ("float", 0.0, 1.0),
    "maskset_blend": ("float", 0.0, 1.0),
    "roughness_bias": ("float", -0.5, 0.5),
}

USERPROP_PREFIX = "userProperties:"


def _reject(msg):
    sys.stderr.write("IMRSV_LCD_REJECT: " + msg + "\n")
    sys.exit(2)


def _validate_float(port, raw, low, high):
    try:
        v = float(raw)
    except (TypeError, ValueError):
        _reject("%s is not a number: %r" % (port, raw))
    if v < low or v > high:
        _reject("%s = %g out of range [%g, %g]" % (port, v, low, high))
    return v


def _validate_color3(port, raw, low, high):
    try:
        chans = [float(c) for c in raw]
    except (TypeError, ValueError):
        _reject("%s is not a color3: %r" % (port, raw))
    if len(chans) != 3:
        _reject("%s expected 3 channels, got %d: %r" % (port, len(chans), raw))
    for c in chans:
        if c < low or c > high:
            _reject("%s channel %g out of range [%g, %g]" % (port, c, low, high))
    return chans


def convert_stage(stage):
    """Convert every Material prim's LCD userProperties -> inputs. Returns a list of
    (prim-path, port, value) tuples that were converted."""
    converted = []
    for prim in stage.Traverse():
        if prim.GetTypeName() != "Material":
            continue
        mat = UsdShade.Material(prim)
        # snapshot names first — we mutate the prim inside the loop
        up_names = [a.GetName() for a in prim.GetAttributes()
                    if a.GetName().startswith(USERPROP_PREFIX)]
        for name in up_names:
            port = name[len(USERPROP_PREFIX):]
            spec = LCD_PORTS.get(port)
            if spec is None:
                continue  # unknown userProperty — leave it alone
            kind, low, high = spec
            raw = prim.GetAttribute(name).Get()
            if kind == "color3":
                chans = _validate_color3(port, raw, low, high)
                inp = mat.CreateInput(port, Sdf.ValueTypeNames.Color3f)
                inp.Set(Gf.Vec3f(chans[0], chans[1], chans[2]))
                val = tuple(round(c, 6) for c in chans)
            else:
                v = _validate_float(port, raw, low, high)
                inp = mat.CreateInput(port, Sdf.ValueTypeNames.Float)
                inp.Set(v)
                val = round(v, 6)
            prim.RemoveProperty(name)  # strip the off-spec bridge
            converted.append((str(prim.GetPath()), port, val))
    return converted


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("usage: lcd_usd_edit.py <exported.usda>\n")
        return 2
    usd_path = argv[1]
    stage = Usd.Stage.Open(usd_path)
    if stage is None:
        _reject("could not open USD stage: " + usd_path)
    converted = convert_stage(stage)
    if converted:
        stage.GetRootLayer().Save()
    for path, port, val in converted:
        print("IMRSV_LCD_CONVERTED %s %s = %s" % (path, port, val))
    print("IMRSV_LCD_CONVERTED_COUNT %d" % len(converted))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
