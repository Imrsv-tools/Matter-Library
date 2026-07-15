"""Phase 60 — Lane-3 smoke-input prep (pxr assert half).

Opens the Blender-exported 2-datablock Copper USD (from build_two_object_copper.py) and
asserts the plumbing the 60.4 live smoke depends on, so the sitting is purely eyes-on:
  1. two Mesh prims each carry primvars:st, and the two st arrays are DISTINCT
     (per-object Blender UV fitting travels -> UV correctness, Discovery-14 PRIMARY);
  2. two Material prims of the SAME Copper identity: one 'Copper_..._v01', one the
     Blender-duplicate '..._v01_001' (the exact suffix 60.3.1's Stage normalize strips);
  3. sparse tint isolation: the untouched material -> 0 LCD inputs: overrides; the tinted
     one -> exactly color3f inputs:base_color_tint ~= the Creator tint (secondary);
  4. no heavy Matter-texture duplication beside the export (PRESERVE).

Run under a pxr-capable python (the usd-toolchain / usdtools env):
    <usdtools-python> assert_two_object_copper.py <out.usda>
Exit 0 = all pass. Reads `<out.usda>.meta.json` written by the build half.
"""
import sys, os, json, glob
from pxr import Usd, UsdGeom  # noqa

LCD_PORTS = ["base_color_tint", "overlay1_density", "overlay2_density", "maskset_blend", "roughness_bias"]

out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(__import__("tempfile").gettempdir(),
                                                         "p60_copper_two_object.usda")
meta_path = out + ".meta.json"
meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}

fails = []
def check(cond, msg):
    print(("PASS" if cond else "FAIL") + ": " + msg)
    if not cond:
        fails.append(msg)

stage = Usd.Stage.Open(out)
meshes = [p for p in stage.Traverse() if p.GetTypeName() == "Mesh"]
materials = [p for p in stage.Traverse() if p.GetTypeName() == "Material"]

# --- 1. distinct per-object UVs travel as distinct primvars:st ---
sts = []
for m in meshes:
    pv = UsdGeom.PrimvarsAPI(m).GetPrimvar("st")
    sts.append(pv.Get() if pv and pv.HasValue() else None)
check(len(meshes) == 2, "exactly 2 Mesh prims exported (got %d: %r)"
      % (len(meshes), [m.GetName() for m in meshes]))
have_st = [s for s in sts if s is not None]
check(len(have_st) == 2, "both meshes carry primvars:st (got %d)" % len(have_st))
if len(have_st) == 2:
    a = [tuple(round(c, 5) for c in uv) for uv in have_st[0]]
    b = [tuple(round(c, 5) for c in uv) for uv in have_st[1]]
    check(a != b, "the two meshes carry DISTINCT primvars:st (per-object UV fitting travels)")
    print("   st[0]=%r" % a)
    print("   st[1]=%r" % b)

# --- 2. two Material prims of the same identity, one Blender-duplicate-suffixed ---
mat_names = sorted(m.GetName() for m in materials)
print("   material prims: %r" % mat_names)
base = meta.get("m1", "Copper_Verdigris_Aged_Base_s01_v01")
check(base in mat_names, "canonical Copper material prim %r present" % base)
dupes = [n for n in mat_names if n != base and n.startswith("Copper_Verdigris_Aged_Base_s01_v01")]
check(len(dupes) == 1, "exactly one Blender-duplicate Copper prim present (got %r)" % dupes)
if dupes:
    check(dupes[0].endswith("_001"),
          "the duplicate carries the Blender suffix 60.3.1's Stage normalize strips (%r)" % dupes[0])

# --- 3. sparse tint isolation ---
def lcd_inputs(prim):
    found = {}
    for a in prim.GetAttributes():
        nm = a.GetName()
        if nm.startswith("inputs:") and nm[len("inputs:"):] in LCD_PORTS:
            found[nm[len("inputs:"):]] = a.Get()
    return found

by_name = {m.GetName(): lcd_inputs(m) for m in materials}
untouched = by_name.get(base, {})
tinted = by_name.get(dupes[0], {}) if dupes else {}
check(list(untouched) == [], "UNTOUCHED material -> 0 LCD inputs: overrides (got %r)" % list(untouched))
check(list(tinted) == ["base_color_tint"],
      "TINTED material -> exactly inputs:base_color_tint (got %r)" % list(tinted))
if tinted.get("base_color_tint") is not None:
    got = tuple(round(float(c), 3) for c in tinted["base_color_tint"])
    want = tuple(round(float(c), 3) for c in meta.get("tint", [0.2, 0.8, 0.4]))
    check(got == want, "the tint value travelled as color3f %r (== Creator tint %r)" % (got, want))

# --- 4. no heavy Matter-texture duplication beside the export (PRESERVE) ---
exp_dir = os.path.dirname(os.path.abspath(out))
matter_tex = set(meta.get("matter_tex_basenames", []))
copied = [os.path.relpath(p, exp_dir) for p in glob.glob(os.path.join(exp_dir, "**", "*"), recursive=True)
          if os.path.isfile(p) and os.path.basename(p) in matter_tex]
check(copied == [], "no heavy Matter texture duplicated beside the export (got %r)" % copied)
if matter_tex:
    print("   (Matter textures referenced, checked-not-copied: %r)" % sorted(matter_tex))

print("=== %d checks failed ===" % len(fails))
sys.exit(1 if fails else 0)
