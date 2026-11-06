#!/usr/bin/env python3
"""Units for codec_ab.py: what each arm is built from, and the scene both arms render in.

  * every picture an article binds is in its arms, the ones bound through the article's own inputs
    (a skin's maps) as well as the ones written on an image node;
  * the preview sphere has a UV set, so a UV-addressed picture covers it instead of showing one texel;
  * reading and writing a picture keeps its colour channels where its alpha is 0 (a maskset's or an
    overlay's channels are separate data, not a colour over a coverage);
  * the X11 settings for Qt are set on Linux only.

Run under the USD toolchain python (pxr, OpenImageIO, numpy):
    <pxr-python> tools/conformance/test_codec_ab.py
Exit 0 = all pass.
"""
import sys
import tempfile
from pathlib import Path

from pxr import Usd, UsdGeom

sys.path.insert(0, str(Path(__file__).resolve().parent))
import codec_ab as C  # noqa: E402

fails = []


def check(cond, what):
    print(("  [PASS] " if cond else "  [FAIL] ") + what)
    if not cond:
        fails.append(what)


ARTICLE = """<?xml version="1.0"?>
<materialx version="1.39">
  <nodegraph name="NG_Skin">
    <input name="normal_map" type="filename" value="../textures/Skin_normal_sUKN.png" />
    <input name="makeup_color_map" type="filename" value="" />
    <input name="roughness_bias" type="float" value="0.0" />
    <image name="base_color_tex" type="color3">
      <input name="file" type="filename" value="../textures/Skin_basecolor_sUKN.png" />
    </image>
    <image name="normal_map_tex" type="vector3">
      <input name="file" type="filename" interfacename="normal_map" />
    </image>
  </nodegraph>
</materialx>
"""

with tempfile.TemporaryDirectory() as tmp:
    tmp = Path(tmp)

    print("the pictures an article binds")
    mtlx = tmp / "Skin.mtlx"
    mtlx.write_text(ARTICLE)
    refs = C.texture_refs(mtlx)
    check(refs == ["../textures/Skin_basecolor_sUKN.png", "../textures/Skin_normal_sUKN.png"],
          f"one written on an image node and one bound through the article's input, no empty one: {refs}")

    print("the preview sphere")
    scene = tmp / "preview.usda"
    scene.write_text(C.preview_scene(hdri="sky.hdr", mtlx=mtlx, matname="Skin"))
    stage = Usd.Stage.Open(str(scene))
    sphere = stage.GetPrimAtPath("/World/PreviewSphere")
    check(sphere.IsA(UsdGeom.Mesh), f"is a mesh, got {sphere.GetTypeName()}")
    st = UsdGeom.PrimvarsAPI(sphere).GetPrimvar("st")
    values = st.Get() if st else None
    points = UsdGeom.Mesh(sphere).GetPointsAttr().Get()
    check(bool(values) and len(values) == len(points), "has one UV per point")
    if values:
        us, vs = [v[0] for v in values], [v[1] for v in values]
        check(min(us) == 0 and max(us) == 1 and min(vs) == 0 and max(vs) == 1, "its UVs cover 0..1 in both directions")
    extent = UsdGeom.Mesh(sphere).ComputeExtent(points) if points else None
    check(extent is not None and all(abs(abs(c) - 1) < 1e-4 for c in (*extent[0], *extent[1])),
          f"radius 1, as the camera is framed for: {extent}")

    print("a 4-channel picture with alpha 0 and alpha 128")
    png = tmp / "Mask_s1.png"
    C._worker(f"""
import OpenImageIO as oiio, numpy as np
px = np.zeros((4, 4, 4), np.uint8); px[:, :, 0] = 200; px[:, :, 1] = 100; px[:, :, 2] = 50; px[:, :2, 3] = 128
sp = oiio.ImageSpec(4, 4, 4, oiio.UINT8); sp.attribute("oiio:UnassociatedAlpha", 1)
b = oiio.ImageBuf(sp); b.set_pixels(oiio.ROI(0, 4, 0, 4, 0, 1, 0, 4), px)
assert b.write({str(png)!r}), b.geterror()
""", tmp)
    C._perturb_darken(png, tmp, factor=1.0)
    got = C._worker(f"""
b = read_buf({str(png)!r})
print([round(v * 255) for v in b.getpixel(1, 1)], [round(v * 255) for v in b.getpixel(3, 1)])
""", tmp).strip()
    check(got == "[200, 100, 50, 128] [200, 100, 50, 0]",
          f"a read and write leaves red, green and blue as they were, under partial and zero alpha: {got}")

print("the environment")
env = C.usd_env()
check(("QT_QPA_PLATFORM" in env) == sys.platform.startswith("linux"),
      f"Qt's X11 platform only on Linux ({sys.platform}): {env.get('QT_QPA_PLATFORM')}")

print(f"\n{'PASS' if not fails else 'FAIL'}: {len(fails)} failure(s)")
sys.exit(1 if fails else 0)
