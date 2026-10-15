"""The scale view's swap rule (Phase19 19.2, D-4) — pure, no ``bpy``, so a plain unit test covers it.

The scale view swaps every library material in a scene for the scale grid nearest its real size,
so a wrong UV scale shows at a glance: grid lines that do not match their neighbours' (the lead,
RD-P19-3: "I look at an object and see grid lines that match or don't mathc... we are trying to
verify that the mareails UV is MATCHING SCALE"). The rule, written once in LCDSchema.md §Scale view:

* **Which grid:** the scale tag nearest the article's ``meters_per_tile`` on a log scale; a tie
  goes to the larger grid.
* **Its size:** the binding's ``uv_scale`` becomes the old value x (grid tile / meters_per_tile).
  ``uv_scale`` DIVIDES the UV (``ML_Place2D``, the LCD place2d), and a mesh's UV unit is the
  article's tile, so the grid then draws at true size wherever the article would.
* **Kept:** ``uv_offset`` and ``uv_rotation``.
* **No size:** no ``meters_per_tile``, a ``meters_per_tile`` of 0, or the tag ``sUKN`` gets the
  hatch, ``uv_scale`` unchanged. That includes a fitted article that tiles nothing (RD-P18-8).
* **Matter and Character alike:** the rule reads the article, never its group.
* **Not a library article:** left alone, and listed.
* **Off its scale option:** an article whose size is not exactly its tag (RD-P19-2) is still
  swapped at its real size, and listed.
"""

from __future__ import annotations

import math

# Identity.md §Scale tags; the same table as assemble_mtlx.SCALE_TAG_METRES and G9's.
TAG_METRES = {"s0001": 0.001, "s001": 0.01, "s01": 0.1, "s1": 1.0, "s10": 10.0, "s100": 100.0}
UNKNOWN = "sUKN"


def grid_article(tag: str) -> str:
    """The scale grid article for a tag (RD-SP-3: the same name except the scale)."""
    return f"Diagnostic_ScaleGrid_Clean_Base_{tag}_v01"


def tag_of(article: str) -> str | None:
    """The scale tag token of an article identity (``…_<tag>_vNN``), or None."""
    parts = article.split("_")
    return parts[-2] if len(parts) >= 3 else None


def grid_for(meters_per_tile: float | None, tag: str | None = None) -> str:
    """The grid tag for an article: nearest on a log scale, a tie to the larger; else sUKN."""
    if tag == UNKNOWN or not meters_per_tile or meters_per_tile <= 0:
        return UNKNOWN
    lg = math.log10(meters_per_tile)
    best = min(TAG_METRES.items(),
               key=lambda kv: (round(abs(math.log10(kv[1]) - lg), 9), -kv[1]))
    return best[0]


def uv_scale_for(old_uv_scale: tuple[float, float], grid: str,
                 meters_per_tile: float | None) -> tuple[float, float]:
    """The grid binding's uv_scale: the old value x (grid tile / article tile); unchanged for sUKN."""
    if grid == UNKNOWN or not meters_per_tile:
        return (float(old_uv_scale[0]), float(old_uv_scale[1]))
    k = TAG_METRES[grid] / meters_per_tile
    return (old_uv_scale[0] * k, old_uv_scale[1] * k)


def off_scale(meters_per_tile: float | None, tag: str | None) -> bool:
    """True for an article whose size is not exactly its tag's length (RD-P19-2)."""
    if tag not in TAG_METRES or not meters_per_tile:
        return False
    want = TAG_METRES[tag]
    return abs(meters_per_tile - want) > 1e-9 * want
