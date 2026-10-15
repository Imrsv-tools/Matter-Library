"""Unit test for the scale view's swap rule (Phase19 19.2, D-4). Pure Python, no Blender.

    python3 blender/addons/imrsv_lcd_export/test_scale_view_rules.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import scale_view_rules as R  # noqa: E402

FAILS = []


def check(cond, what):
    print(f"  [{'PASS' if cond else 'FAIL'}] {what}")
    if not cond:
        FAILS.append(what)


def near(a, b):
    return all(abs(x - y) <= 1e-12 * max(1.0, abs(y)) for x, y in zip(a, b))


# Which grid: each tag's own length picks its own grid
for tag, m in R.TAG_METRES.items():
    check(R.grid_for(m, tag) == tag, f"{m} m picks {tag}")
# off-tag articles (F-P15-1): nearest on a log scale
check(R.grid_for(0.8, "s1") == "s1", "Oak at 0.8 m wears the 1 m grid")
check(R.grid_for(3.0, "s1") == "s1", "Concrete_Polished at 3 m wears the 1 m grid (3 is nearer 1 than 10 on a log scale)")
check(R.grid_for(0.3, "s01") == "s01", "MildSteel at 0.3 m wears the 10 cm grid (log 0.3 is 0.48 from 10 cm, 0.52 from 1 m)")
check(R.grid_for(0.12, "s01") == "s01", "OakLeaf at 0.12 m wears the 10 cm grid")
check(R.grid_for(10 ** -0.5, None) == "s1", "a tie (the geometric mean of 10 cm and 1 m) goes to the larger grid")
check(R.grid_for(250.0, None) == "s100", "beyond 100 m: the 100 m grid")
# No size
check(R.grid_for(0.0, "sUKN") == "sUKN", "a fitted article (sUKN, 0.0) wears the hatch")
check(R.grid_for(None, None) == "sUKN", "no recorded size wears the hatch")
check(R.grid_for(1.0, "sUKN") == "sUKN", "the tag sUKN wins over any number")

# Its size: old uv_scale x (grid tile / article tile)
check(near(R.uv_scale_for((1, 1), "s1", 1.0), (1, 1)), "an article on its tag: uv_scale unchanged")
check(near(R.uv_scale_for((1, 1), "s1", 0.8), (1.25, 1.25)), "Oak at 0.8 m: the 1 m grid at uv_scale 1.25")
check(near(R.uv_scale_for((1, 1), "s1", 3.0), (1 / 3, 1 / 3)), "Concrete at 3 m: uv_scale 1/3")
check(near(R.uv_scale_for((0.0059, 0.0059), "s001", 0.01), (0.0059, 0.0059)),
      "a binding's own correction (the skin on its atlas) is kept")
check(near(R.uv_scale_for((2, 0.5), "s01", 0.1), (2, 0.5)), "an anisotropic uv_scale keeps both axes")
check(near(R.uv_scale_for((1, 1), "sUKN", 0.0), (1, 1)), "the hatch: uv_scale unchanged")

# Off its scale option (RD-P19-2)
check(R.off_scale(0.8, "s1") and R.off_scale(3.0, "s1"), "0.8 m and 3 m tagged s1 are off their option")
check(not R.off_scale(1.0, "s1") and not R.off_scale(0.01, "s001"), "an article on its tag is not")
check(not R.off_scale(0.0, "sUKN"), "sUKN is never listed as off its option")

# Names
check(R.grid_article("s01") == "Diagnostic_ScaleGrid_Clean_Base_s01_v01", "the grid article is the same name except the scale (RD-SP-3)")
check(R.tag_of("Oak_Natural_Clean_Base_s1_v01") == "s1", "the tag is read off the identity")

print(f"{'FAIL' if FAILS else 'PASS'}: {len(FAILS)} failed")
sys.exit(1 if FAILS else 0)
