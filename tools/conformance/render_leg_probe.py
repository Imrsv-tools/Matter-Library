#!/usr/bin/env python3
"""Render-leg probe (Phase 60sq1, Step 2 sitting-prep) — does the Copper .mtlx sample each
of the 5 carried LCD appearance scalars in a STANDARDS renderer (Storm)?

P60's smoke proved recognized-Copper retarget + isolated `base_color_tint` only. The other 4
carried scalars (overlay1_density, overlay2_density, maskset_blend, roughness_bias) are
wire-present but render-unproven — the render-leg's unproven lane (§6.3). This probe isolates
the QUESTION: it renders single-scalar-isolated SATURATED variants of the golden — each a USD
`over` opinion authoring one `inputs:<port>` override on both Copper instances (exactly how
Studio op 305 set_material_inputs authors it) — and measures the per-scalar pixel delta vs a
neutral baseline. MAE > threshold ⇒ the scalar SAMPLES; MAE ~0 ⇒ SILENT FALLBACK to default.

Scope of what this proves: the .mtlx material network responds to each scalar in Storm/Hydra
(the reference renderer). It does NOT prove Studio's UE apply-site samples them — that stays
the Step-2 ⚠human premise-proof smoke. A Storm PASS isolates any Studio miss to the apply-site.

    render_leg_probe.py [OUT_DIR]
"""
import subprocess
import sys
from pathlib import Path

INST = "/home/peter/usd-tools/inst/usd-26.03"
ENVP = "/home/peter/.conda/envs/imrsv-usd-tools"
GOLDEN = "/home/peter/Documents/IMRSV_GITrepos/IMRSV_Platform/Matter-Library/tools/conformance/golden/creator_table_lightweight.usda"
MATROOT = "/home/peter/Documents/IMRSV_GITrepos/IMRSV_Platform/Matter-Library/MatterLibrary/materials"
INSTANCES = ("Copper_Instance_Top", "Copper_Instance_Leg")
# The LCD interface inputs live on the nodegraph prim (NG_<material-stem>) inside each
# instance — NOT on the material prim — so an override must target the nodegraph.
NODEGRAPH = "NG_Copper_Verdigris_Aged_Base_s01_v01"

# (label, override line) — baseline authors nothing; each variant isolates ONE scalar at a
# saturated value distinct from the article default (LCDSchema ranges).
VARIANTS = [
    ("baseline", None),
    ("base_color_tint", "color3f inputs:base_color_tint = (1, 0, 1)"),      # magenta (default 0.95,0.64,0.54) — control
    ("overlay1_density", "float inputs:overlay1_density = 1.0"),            # default 0.45
    ("overlay2_density", "float inputs:overlay2_density = 1.0"),            # default 0.30
    ("maskset_blend", "float inputs:maskset_blend = 1.0"),                  # default 0.35
    ("roughness_bias", "float inputs:roughness_bias = 0.5"),               # default 0.0 (range -0.5..+0.5)
]


def env():
    import os
    roots = subprocess.check_output(
        f"find {MATROOT} -name '*.mtlx' -printf '%h\\n' | sort -u | paste -sd: -",
        shell=True, text=True).strip()
    e = dict(os.environ)
    e.update(
        PYTHONPATH=f"{INST}/lib/python",
        LD_LIBRARY_PATH=f"{INST}/lib:{ENVP}/lib",
        PXR_MTLX_STDLIB_SEARCH_PATHS=f"{INST}/libraries",
        PXR_AR_DEFAULT_SEARCH_PATH=roots,
        QT_QPA_PLATFORM="xcb", QT_XCB_GL_INTEGRATION="glx",
        DISPLAY=os.environ.get("DISPLAY", ":0"),
    )
    if "XAUTHORITY" not in e:
        xa = sorted(Path(f"/run/user/{os.getuid()}").glob("xauth_*"),
                    key=lambda p: p.stat().st_mtime, reverse=True)
        if xa:
            e["XAUTHORITY"] = str(xa[0])
    return e


def variant_layer(override: str | None) -> str:
    dome = 'def DomeLight "Key"\n{\n    float inputs:intensity = 1500\n}\n'
    head = f'#usda 1.0\n(\n    subLayers = [@{GOLDEN}@]\n)\n{dome}'
    if override is None:
        return head
    overs = "\n".join(
        f'        over "{i}"\n        {{\n            over "{NODEGRAPH}"\n            {{\n                {override}\n            }}\n        }}'
        for i in INSTANCES)
    return head + f'over "Creator_Table"\n{{\n    over "Materials"\n    {{\n{overs}\n    }}\n}}\n'


def main() -> int:
    out = Path(sys.argv[1] if len(sys.argv) > 1 else
               "/home/peter/.claude/jobs/71b4820d/tmp/p60_conformance/renderleg")
    out.mkdir(parents=True, exist_ok=True)
    e = env()
    pngs: dict[str, Path] = {}
    for label, override in VARIANTS:
        layer = out / f"{label}.usda"
        layer.write_text(variant_layer(override))
        png = out / f"{label}.png"
        r = subprocess.run([f"{ENVP}/bin/python", f"{INST}/bin/usdrecord",
                            "--complexity", "high", "--renderer", "GL", str(layer), str(png)],
                           env=e, capture_output=True, text=True)
        ok = png.is_file()
        pngs[label] = png if ok else None
        print(f"  render {label:18s} {'OK' if ok else 'FAIL'}" + ("" if ok else f"  {r.stderr.strip()[-160:]}"))

    base = pngs.get("baseline")
    if not base:
        print("  baseline render missing — cannot diff"); return 1
    # The geometry fills only a fraction of the frame; a whole-image MAE is diluted by the
    # white background. Crop every image to the baseline's content bbox so the delta is
    # measured over the SURFACE only, then the per-scalar verdict is unconfounded.
    bbox = subprocess.check_output(["convert", str(base), "-trim", "-format", "%wx%h%O", "info:"],
                                   text=True).strip()
    print(f"\n  surface bbox (from baseline, -trim): {bbox}")

    def crop(src: Path) -> Path:
        dst = src.with_name(src.stem + "_crop.png")
        subprocess.run(["convert", str(src), "-crop", bbox, "+repage", str(dst)], check=True)
        return dst

    base_c = crop(base)
    # NOTE the metric's limit: the T-shaped table fills only a fraction of its bbox rectangle,
    # so absolute MAE is diluted (a visibly-magenta base_color_tint reads ~0.004, not ~0.5).
    # Use MAE as a RELATIVE sensitivity ranking; the eyes-on PNG is the gate (§14d). A per-scalar
    # Δ>0 proves the override reached the nodegraph and the .mtlx RESPONDS in Storm; it does NOT
    # replace Studio's UE apply-site render-leg (the Step-2 ⚠human smoke).
    print("  per-scalar Δ vs baseline, SURFACE-cropped (relative MAE; Δ>0 ⇒ .mtlx responds; eyes-on = gate):")
    fails = 0
    results = []
    for label, _ in VARIANTS[1:]:
        p = pngs.get(label)
        if not p:
            print(f"    {label:18s} —  (render failed)"); fails += 1; continue
        # ImageMagick MAE: `compare -metric MAE a b null:` prints "<abs> (<normalized>)" on stderr.
        cp = subprocess.run(["compare", "-metric", "MAE", str(base_c), str(crop(p)), "null:"],
                            capture_output=True, text=True)
        raw = cp.stderr.strip()
        norm = raw.split("(")[-1].rstrip(")") if "(" in raw else raw
        try:
            val = float(norm)
        except ValueError:
            print(f"    {label:18s} ?  ({raw})"); fails += 1; continue
        results.append((label, val))
        print(f"    {label:18s} Δ={val:.5f}  {'responds' if val > 0 else 'NO CHANGE (silent no-op)'}")
    silent = [l for l, v in results if v == 0.0]
    if silent:
        print(f"  ⚠ zero-Δ scalars (silent no-op in the .mtlx): {silent}")
        fails += 1
    print(f"\n  probe PNGs (eyes-on is the gate): {out}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
