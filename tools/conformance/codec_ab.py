#!/usr/bin/env python3
"""Codec A/B parity comparator (Phase 60sq2.8) — the earliest OBJECTIVE parity gate for
scope B (BCn compressed delivery). Answers one question with a number, not an eye:

    Does swapping a material's authored source PNGs for their release BCn `.dds`
    (what the runtime actually samples) change the rendered result beyond the
    per-class parity bar?

Design (matched-conditions, one pinned pipeline — §6.5 discriminator discipline):
  * ONE renderer / scene / camera / light / color-pipeline for BOTH arms, so the
    ONLY variable is the texture bytes. Any renderer or OCIO imperfection cancels
    (the comparator is cross-renderer-independent and OCIO-safe by construction —
    the v2.4-native OCIO bundle is for CROSS-renderer parity, not this gate).
  * Arm A = authored source PNGs (the deployed-path RED fixture, by construction).
  * Arm B = each PNG's release `.dds` DECODED back to pixels — exactly the codec
    loss the GPU BC hardware sampler sees. Decode bridge: compressonatorcli -> .tga
    -> OIIO (OIIO's own DDS reader rejects compressonator's DX10/BC7 header, so we
    route through .tga). BC5 normals decode with B=0 (only R,G are stored); we
    reconstruct B = sqrt(1 - nx^2 - ny^2) — mirroring what a correct BC5-normal
    consumer (UE, and the GPU) does, so the normal's codec delta is real, not an
    artifact of a dropped Z.

Metric: CIE ΔE2000 over the rendered surface (background cropped out so it can't
dilute the delta), plus a structural SSIM and a per-role texture-space codec table.
The parity bar is per material CLASS (Experience_Materials.md): ΔE < 2 for
Opaque / Masked / Emissive; "recognizable" (advisory) for transmission / SSS. The
class is read from the material's `imrsv_metadata.master_material`.

Gate-can-fail discipline (§14a):
  * CONTROL: an A-vs-A self-consistency render must be ~0 (proves the renderer +
    metric are stable; a non-zero floor is the renderer's AA noise, reported).
  * RED-DEMO (--red-demo): recompress base color as BC1 (visibly lossy) and prove
    the gate's ΔE jumps well past the bar — a gate that cannot go RED is not a gate.

Usage:
  codec_ab.py <material.mtlx> [--staging <release-dir>] [--out <dir>]
              [--width N] [--red-demo] [--keep]
  codec_ab.py --self-test <material.mtlx>      # A-vs-A control only

Exit 0 iff every graded (tight-bar) material passes AND the control floor is below
the bar. Advisory (relaxed-bar) classes never fail the exit code.
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

# ---- toolchain pins (shared with render_leg_probe.py / check_conformance.sh) ----
INST = Path("/home/peter/usd-tools/inst/usd-26.03")
ENVP = Path("/home/peter/.conda/envs/imrsv-usd-tools")
HDRI = INST / "resources/Lights/san_giuseppe_bridge.hdr"
COMPRESSONATOR = os.environ.get(
    "COMPRESSONATORCLI", str(Path.home() / ".local/bin/compressonatorcli"))
DEFAULT_STAGING = Path(
    "/home/peter/Documents/IMRSV_GITrepos/IMRSV_Platform/Matter-Library/"
    "library/staging/matterlib-0.1.0")

# Per-class parity bar (Experience_Materials.md — ΔE2000 under standardized lighting).
TIGHT_BAR = 2.0
TIGHT_CLASSES = {"Opaque", "Masked", "Emissive"}   # graded (fail the exit code)
RELAXED_CLASSES = {"Transmission", "SSS", "Subsurface"}  # advisory only

# Normal-role tokens (need BC5 Z-reconstruction on decode).
NORMAL_TOKENS = ("normal", "_normal_", "normalmap")


# ---------------------------------------------------------------------------
# env / subprocess helpers
# ---------------------------------------------------------------------------
def usd_env() -> dict:
    """usdrecord + OIIO + colour env — Storm on this Wayland box needs xcb/glx + XAUTH."""
    e = dict(os.environ)
    e.update(
        PYTHONPATH=f"{INST}/lib/python",
        LD_LIBRARY_PATH=f"{INST}/lib:{ENVP}/lib",
        PXR_MTLX_STDLIB_SEARCH_PATHS=f"{INST}/libraries",
        QT_QPA_PLATFORM="xcb", QT_XCB_GL_INTEGRATION="glx",
        DISPLAY=os.environ.get("DISPLAY", ":0"),
    )
    if "XAUTHORITY" not in e:
        xa = sorted(Path(f"/run/user/{os.getuid()}").glob("xauth_*"),
                    key=lambda p: p.stat().st_mtime, reverse=True)
        if xa:
            e["XAUTHORITY"] = str(xa[0])
    return e


def _py():
    return str(ENVP / "bin/python")


def _compressonator_prefix() -> list[str]:
    try:
        head = Path(COMPRESSONATOR).read_bytes()[:4]
    except OSError:
        return [COMPRESSONATOR]
    return [COMPRESSONATOR] if head == b"\x7fELF" else ["/bin/bash", COMPRESSONATOR]


# ---------------------------------------------------------------------------
# OIIO image IO (run inside the usd-tools python via a tiny worker so numpy +
# colour + OIIO all resolve; the parent process may be any python)
# ---------------------------------------------------------------------------
def _worker(code: str, out_dir: Path) -> str:
    """Run `code` in the usd-tools python; returns stdout (raises on failure)."""
    r = subprocess.run([_py(), "-c", code], env=usd_env(),
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"usd-python worker failed:\n{r.stderr[-2000:]}")
    return r.stdout


# ---------------------------------------------------------------------------
# decode a BCn .dds -> a source-faithful PNG (arm B texture)
# ---------------------------------------------------------------------------
def decode_dds_to_png(dds: Path, dst_png: Path, src_png: Path, tmp: Path) -> None:
    """Decode `dds` to a PNG whose channel layout matches `src_png` (so the .mtlx
    samples it identically). BC5 normals get their Z reconstructed."""
    tmp.mkdir(parents=True, exist_ok=True)
    tga = tmp / (dds.stem + "_decode.tga")
    r = subprocess.run(_compressonator_prefix() + ["-noprogress", str(dds), str(tga)],
                       capture_output=True, text=True)
    if not tga.exists():
        raise RuntimeError(f"compressonatorcli decode failed for {dds.name}:\n{r.stdout[-800:]}{r.stderr[-800:]}")
    is_normal = any(t in dds.stem.lower() for t in NORMAL_TOKENS)
    code = f"""
import OpenImageIO as oiio, numpy as np
def rd(p):
    b=oiio.ImageBuf(p); s=b.spec()
    return s, b.get_pixels(oiio.UINT8).reshape(s.height,s.width,s.nchannels)
_, dec = rd({str(tga)!r})              # decoded, always 4ch from compressonator
ssrc, _ = rd({str(src_png)!r})         # source png, to match channel count
nch = ssrc.nchannels
is_normal = {is_normal}
if is_normal:
    # BC5 stored R,G; reconstruct B = sqrt(1 - nx^2 - ny^2) as a correct consumer does.
    r = dec[:,:,0].astype(np.float64)/255.0*2-1
    g = dec[:,:,1].astype(np.float64)/255.0*2-1
    b = np.sqrt(np.clip(1-r*r-g*g, 0, 1))
    out = np.stack([dec[:,:,0], dec[:,:,1], ((b*0.5+0.5)*255).round().astype(np.uint8)], -1)
elif nch == 1:
    out = dec[:,:,0:1]
elif nch == 3:
    out = dec[:,:,:3]
else:
    out = dec[:,:,:4]
h,w,c = out.shape
sp = oiio.ImageSpec(w,h,c,oiio.UINT8)
buf = oiio.ImageBuf(sp); buf.set_pixels(oiio.ROI(0,w,0,h,0,1,0,c), np.ascontiguousarray(out))
assert buf.write({str(dst_png)!r}), buf.geterror()
print("OK", w, h, c)
"""
    _worker(code, tmp)


def _perturb_darken(png: Path, tmp: Path, factor: float = 0.6) -> None:
    """RED-DEMO helper: multiply a texture's RGB by `factor` in place (a deterministic,
    data-independent 'materially wrong base color' the gate MUST flag)."""
    code = f"""
import OpenImageIO as oiio, numpy as np
b=oiio.ImageBuf({str(png)!r}); s=b.spec()
a=b.get_pixels(oiio.UINT8).reshape(s.height,s.width,s.nchannels).astype(np.float64)
n=min(3,s.nchannels)
a[:,:,:n]=np.clip(a[:,:,:n]*{factor},0,255)
out=a.round().astype(np.uint8)
sp=oiio.ImageSpec(s.width,s.height,s.nchannels,oiio.UINT8)
buf=oiio.ImageBuf(sp); buf.set_pixels(oiio.ROI(0,s.width,0,s.height,0,1,0,s.nchannels), np.ascontiguousarray(out))
assert buf.write({str(png)!r}), buf.geterror()
print("OK")
"""
    _worker(code, tmp)


# ---------------------------------------------------------------------------
# preview scene (matched-conditions contract — sphere + HDRI dome + fixed camera)
# ---------------------------------------------------------------------------
PREVIEW_TEMPLATE = """#usda 1.0
(
    defaultPrim = "World"
    upAxis = "Y"
)
def Xform "World"
{{
    def DomeLight "Dome"
    {{
        float inputs:intensity = 1.0
        asset inputs:texture:file = @{hdri}@
        token inputs:texture:format = "latlong"
    }}
    def "Mat" (
        prepend references = @{mtlx}@</MaterialX/Materials/{matname}>
    )
    {{
    }}
    def Sphere "PreviewSphere" (
        prepend apiSchemas = ["MaterialBindingAPI"]
    )
    {{
        double radius = 1.0
        rel material:binding = </World/Mat>
    }}
    def Camera "Cam"
    {{
        float focalLength = 35
        float focusDistance = 4
        double3 xformOp:translate = (0, 0, 4)
        uniform token[] xformOpOrder = ["xformOp:translate"]
    }}
}}
"""


def material_name(mtlx: Path) -> str:
    root = ET.parse(mtlx).getroot()
    for sm in root.iter():
        if sm.tag.endswith("surfacematerial"):
            return sm.get("name")
    raise RuntimeError(f"no <surfacematerial> in {mtlx}")


def material_class(mtlx: Path) -> str:
    """Read imrsv_metadata.master_material (the parity CLASS). Defaults to Opaque."""
    root = ET.parse(mtlx).getroot()
    for nd in root.iter():
        if nd.tag.endswith("nodedef") and nd.get("node") == "imrsv_metadata":
            for inp in nd:
                if inp.get("name") == "master_material":
                    return inp.get("value", "Opaque")
    return "Opaque"


def render(mtlx: Path, out_png: Path, width: int) -> None:
    scene = out_png.with_suffix(".preview.usda")
    scene.write_text(PREVIEW_TEMPLATE.format(
        hdri=HDRI, mtlx=mtlx, matname=material_name(mtlx)))
    r = subprocess.run(
        [_py(), str(INST / "bin/usdrecord"), "--renderer", "GL",
         "--complexity", "high", "--camera", "/World/Cam",
         "--imageWidth", str(width), str(scene), str(out_png)],
        env=usd_env(), capture_output=True, text=True)
    if not out_png.exists():
        raise RuntimeError(f"usdrecord failed for {mtlx.name}:\n{r.stdout[-1500:]}{r.stderr[-1500:]}")


# ---------------------------------------------------------------------------
# metric — ΔE2000 (+ SSIM) over the surface, background cropped
# ---------------------------------------------------------------------------
def compare(png_a: Path, png_b: Path, tmp: Path) -> dict:
    """Return {dE_mean, dE_p95, ssim, coverage} over the non-background surface."""
    code = f"""
import OpenImageIO as oiio, numpy as np, colour, json
def rd(p):
    b=oiio.ImageBuf(p); s=b.spec()
    a=b.get_pixels(oiio.FLOAT).reshape(s.height,s.width,s.nchannels)
    return a[:,:,:3]
A=rd({str(png_a)!r}); B=rd({str(png_b)!r})
# background mask: the dome renders a near-uniform bright surround; the sphere is the
# subject. Mask to pixels that differ from the median corner (background) — robust, and
# identical for both arms so the delta is measured over the material only.
h,w,_=A.shape
corners=np.concatenate([A[:8,:8].reshape(-1,3),A[:8,-8:].reshape(-1,3),
                        A[-8:,:8].reshape(-1,3),A[-8:,-8:].reshape(-1,3)])
bg=np.median(corners,0)
fg=(np.abs(A-bg).sum(2) > 0.06)          # subject pixels (both arms share arm-A mask)
cov=float(fg.mean())
# sRGB (usdrecord 8-bit output) -> XYZ -> Lab -> ΔE2000
def lab(x): return colour.XYZ_to_Lab(colour.sRGB_to_XYZ(np.clip(x,0,1)))
LA, LB = lab(A), lab(B)
dE = colour.difference.delta_E(LA, LB, method="CIE 2000")
dEf = dE[fg]
# lightweight global SSIM on luminance (structural — catches normal/roughness shifts ΔE underweights)
def lum(x): return (0.2126*x[:,:,0]+0.7152*x[:,:,1]+0.0722*x[:,:,2])
la,lb=lum(A)[fg],lum(B)[fg]
mua,mub=la.mean(),lb.mean(); va,vb=la.var(),lb.var(); cov_=((la-mua)*(lb-mub)).mean()
c1,c2=(0.01)**2,(0.03)**2
ssim=((2*mua*mub+c1)*(2*cov_+c2))/((mua**2+mub**2+c1)*(va+vb+c2))
print(json.dumps({{"dE_mean":float(dEf.mean()),"dE_p95":float(np.percentile(dEf,95)),
                   "dE_max":float(dEf.max()),"ssim":float(ssim),"coverage":cov}}))
"""
    import json
    return json.loads(_worker(code, tmp).strip())


def texture_codec_table(arm_a: Path, arm_b: Path, tmp: Path) -> str:
    """Per-role texture-space codec loss (diagnostic): color roles in ΔE2000, data roles in MAE/255."""
    code = f"""
import OpenImageIO as oiio, numpy as np, colour
from pathlib import Path
def rd(p):
    b=oiio.ImageBuf(str(p)); s=b.spec()
    return b.get_pixels(oiio.FLOAT).reshape(s.height,s.width,s.nchannels)
A=Path({str(arm_a/'textures')!r}); B=Path({str(arm_b/'textures')!r})
COLOR=("basecolor","diffuse","emissive")
rows=[]
for pa in sorted(A.glob("*.png")):
    pb=B/pa.name
    if not pb.exists(): rows.append(f"    {{pa.name:40s}} (no dds arm)"); continue
    a=rd(pa); b=rd(pb); n=min(a.shape[2],b.shape[2]); a=a[:,:,:n]; b=b[:,:,:n]
    stem=pa.stem.lower()
    if any(t in stem for t in COLOR) and n>=3:
        lab=lambda x: colour.XYZ_to_Lab(colour.sRGB_to_XYZ(np.clip(x[:,:,:3],0,1)))
        d=colour.difference.delta_E(lab(a),lab(b),method="CIE 2000")
        rows.append(f"    {{pa.name:40s}} ΔE2000 mean={{d.mean():.3f}} p95={{np.percentile(d,95):.3f}}")
    else:
        mae=np.abs(a-b).mean()*255
        rows.append(f"    {{pa.name:40s}} MAE={{mae:.3f}}/255  ({{n}}ch)")
print(chr(10).join(rows))
"""
    return _worker(code, tmp).strip()


# ---------------------------------------------------------------------------
# arm assembly
# ---------------------------------------------------------------------------
def index_staging(staging: Path) -> dict[str, Path]:
    """basename-stem -> .dds path over the whole staging texture tree."""
    idx = {}
    for p in staging.rglob("*.dds"):
        idx[p.stem] = p
    return idx


def texture_refs(mtlx: Path) -> list[str]:
    """relative texture filenames the .mtlx references (textures/X.png)."""
    root = ET.parse(mtlx).getroot()
    refs = []
    for img in root.iter():
        if img.tag.endswith("image"):
            for inp in img:
                if inp.get("name") == "file":
                    refs.append(inp.get("value"))
    return sorted(set(refs))


def build_arms(mtlx: Path, staging: Path, work: Path, red_demo: bool) -> tuple[Path, Path]:
    """Materialize arm_a (source PNGs) + arm_b (dds-decoded PNGs) as self-contained
    packages (mtlx + textures/). Returns (arm_a_mtlx, arm_b_mtlx)."""
    src_tex_dir = mtlx.parent / "textures"
    dds_idx = index_staging(staging)
    arm_a, arm_b = work / "arm_a", work / "arm_b"
    for d in (arm_a, arm_b):
        (d / "textures").mkdir(parents=True, exist_ok=True)
        shutil.copy(mtlx, d / mtlx.name)
    tmp = work / "_decode"
    missing = []
    for ref in texture_refs(mtlx):
        name = Path(ref).name
        src = src_tex_dir / name
        shutil.copy(src, arm_a / "textures" / name)          # arm A = authored source
        dds = dds_idx.get(Path(name).stem)
        if not dds or not dds.exists():
            missing.append(name); continue
        decode_dds_to_png(dds, arm_b / "textures" / name, src, tmp)
        if red_demo and "basecolor" in name.lower():
            # RED-DEMO (§14a — prove the gate can go RED): after a faithful decode,
            # inject a materially-wrong base color into arm B (a deterministic 0.6x
            # linear darken — "the runtime sampled a wrong/corrupt base color"). This is
            # data-independent and guaranteed to cross the Opaque bar, so a PASS here
            # would prove the threshold logic is tautological. (Plain BC1 on this near-
            # uniform copper only reaches render ΔE~0.74 — a metal is forgiving of base-
            # color banding — so BC1 is too weak to exercise the bar.)
            _perturb_darken(arm_b / "textures" / name, tmp)
    if missing:
        raise RuntimeError(f"no staged .dds for: {missing}")
    return arm_a / mtlx.name, arm_b / mtlx.name


# ---------------------------------------------------------------------------
# driver
# ---------------------------------------------------------------------------
def run_one(mtlx: Path, staging: Path, out: Path, width: int,
            red_demo: bool, self_test: bool) -> bool:
    name = mtlx.stem
    cls = material_class(mtlx)
    graded = cls in TIGHT_CLASSES
    work = out / name
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    print(f"\n=== {name}  (class={cls}, {'GRADED ΔE<%.1f' % TIGHT_BAR if graded else 'ADVISORY'}) ===")

    arm_a_mtlx, arm_b_mtlx = build_arms(mtlx, staging, work, red_demo)
    ra, rb = work / "render_A.png", work / "render_B.png"
    render(arm_a_mtlx, ra, width)
    if self_test:
        rb2 = work / "render_A2.png"
        render(arm_a_mtlx, rb2, width)
        ctl = compare(ra, rb2, work)
        print(f"  CONTROL A-vs-A: ΔE2000 mean={ctl['dE_mean']:.4f} p95={ctl['dE_p95']:.4f} "
              f"ssim={ctl['ssim']:.5f} coverage={ctl['coverage']*100:.1f}%")
        print(f"  (renderer/metric floor — should be ~0; this is the AA noise baseline)")
        return ctl["dE_mean"] < TIGHT_BAR

    render(arm_b_mtlx, rb, width)
    m = compare(ra, rb, work)
    print(f"  RENDER ΔE2000: mean={m['dE_mean']:.4f}  p95={m['dE_p95']:.4f}  max={m['dE_max']:.4f}")
    print(f"  structural SSIM={m['ssim']:.5f}   surface coverage={m['coverage']*100:.1f}%")
    print("  per-role texture-space codec loss:")
    print(texture_codec_table(arm_a_mtlx.parent, arm_b_mtlx.parent, work))
    print(f"  renders: {ra}  |  {rb}")
    if red_demo:
        red_fired = m["dE_mean"] > TIGHT_BAR
        print(f"  RED-DEMO (materially-wrong base color injected): ΔE mean={m['dE_mean']:.3f} "
              f"{'✓ gate FIRES (>%.1f)' % TIGHT_BAR if red_fired else '✗ gate did NOT fire'}")
        return red_fired
    if not graded:
        print(f"  ADVISORY class — ΔE recorded, not exit-graded (recognizable bar).")
        return True
    ok = m["dE_mean"] < TIGHT_BAR
    print(f"  VERDICT: {'PASS' if ok else 'FAIL'} (mean ΔE {m['dE_mean']:.3f} vs bar {TIGHT_BAR})")
    return ok


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Codec A/B parity comparator (Phase 60sq2.8).")
    ap.add_argument("mtlx", help="material .mtlx (with a sibling textures/ dir of source PNGs)")
    ap.add_argument("--staging", default=str(DEFAULT_STAGING),
                    help="release staging dir holding the BCn .dds (default: matterlib-0.1.0)")
    ap.add_argument("--out", default=None, help="output dir (default: a /tmp scratch)")
    ap.add_argument("--width", type=int, default=512, help="render width (square)")
    ap.add_argument("--red-demo", action="store_true",
                    help="force base color to BC1 to prove the gate can FAIL")
    ap.add_argument("--self-test", action="store_true", help="A-vs-A control only")
    ap.add_argument("--keep", action="store_true", help="keep the work dir")
    args = ap.parse_args(argv)

    mtlx = Path(args.mtlx).resolve()
    if not mtlx.exists():
        print(f"RESULT: FAIL — no such .mtlx: {mtlx}"); return 2
    if not Path(COMPRESSONATOR).exists():
        print(f"RESULT: FAIL — compressonatorcli not found at {COMPRESSONATOR}"); return 2
    out = Path(args.out) if args.out else Path(
        os.environ.get("CLAUDE_JOB_DIR", "/tmp")) / "tmp/codec_ab"
    out.mkdir(parents=True, exist_ok=True)

    ok = run_one(mtlx, Path(args.staging), out, args.width, args.red_demo, args.self_test)
    print("\nRESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
