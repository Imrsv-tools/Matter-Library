"""IMRSV LCD sparse-delta core — pure Python, NO `bpy` (Phase 60 §9 piece 2d).

The producer half of the add-on must export SPARSELY: an untouched material carries
ZERO `inputs:` overrides (byte-identical to the library default), and only a port whose
current value *differs* from its baseline is emitted. Returning a slider to baseline
removes the override.

This module holds ONLY the value-comparison logic, deliberately free of any `bpy`
dependency so it is unit-testable under any interpreter (Blender's own Python, the
`usdtools` pxr venv, or plain CPython). The `bpy` glue that reads a material's node-group
instance sockets and the node-group INTERFACE defaults (the baseline) lives in `__init__.py`
and hands plain dicts to `sparse_deltas` here.

Baseline representation (Discovery 14, §9 piece 2d): the thin Matter node-group's INTERFACE
socket defaults — the article's canonical values, declared once per node-group in the `.blend`.
A node INSTANCE socket value that differs from its interface default is a Creator refinement.
"""

# The Creator-adjustable LCD ports that TRAVEL (LCDSchema.md; 1:1 with Stage kLcdTravelPorts,
# MaterialXOps.cpp:75). UV placement (uv_scale/uv_offset/uv_rotation) is Studio-side only (S3).
LCD_TRAVEL_PORTS = (
    "base_color_tint",   # color3
    "overlay1_density",  # float
    "overlay2_density",  # float
    "maskset_blend",     # float
    "roughness_bias",    # float
)
_COLOR3_PORTS = frozenset({"base_color_tint"})

# Float tolerance for "differs from baseline". Blender stores socket values as 32-bit floats,
# so a value round-tripped through the UI carries precision noise (e.g. 0.2 -> 0.20000000298);
# a tolerance well above that noise floor but far below any meaningful refinement step.
_EPS = 1e-6


def color3(v):
    """Coerce a socket/interface color value (an RGBA tuple/array, or any 3+ sequence) to a
    3-tuple of plain floats — LCD `base_color_tint` is color3, so the alpha channel is dropped."""
    return tuple(float(c) for c in v)[:3]


def is_delta(port, value, baseline):
    """True if `value` differs from `baseline` beyond tolerance for this LCD port.
    A `None` baseline (no interface default available) counts as a delta — an explicit,
    intentional override with nothing to compare against."""
    if baseline is None:
        return True
    if port in _COLOR3_PORTS:
        return any(abs(a - b) > _EPS for a, b in zip(color3(value), color3(baseline)))
    return abs(float(value) - float(baseline)) > _EPS


def sparse_deltas(instance_values, baseline_values, explicit_values=None):
    """Return `{port: value}` for ONLY the LCD ports whose current value differs from its
    baseline — the sparse set the export must carry.

    * `instance_values`  — node-group INSTANCE socket values keyed by port (the Creator surface).
    * `baseline_values`  — the node-group INTERFACE defaults keyed by port (the canonical values).
    * `explicit_values`  — optional ID custom properties; an intentional override that WINS over
                           the instance value, but is still delta-checked against the same
                           baseline (an explicit value returned to baseline drops the override).

    An untouched material (every instance socket == its interface default) yields `{}`."""
    out = {}
    for port, val in instance_values.items():
        if port in LCD_TRAVEL_PORTS and is_delta(port, val, baseline_values.get(port)):
            out[port] = val
    if explicit_values:
        for port, val in explicit_values.items():
            if port not in LCD_TRAVEL_PORTS:
                continue
            if is_delta(port, val, baseline_values.get(port)):
                out[port] = val
            else:
                out.pop(port, None)  # explicit value returned to baseline -> no override
    return out
