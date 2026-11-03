#!/usr/bin/env python3
"""Phase27 Pass 3 probe: one body region through its own close camera, at ~0.4 mm a pixel.

    region.py prep  <out> <name> <yaw> <cx> <cy> <metres>       render hm08 there wearing D_seam9's colour
    region.py paint <out> <name> <strengths> <seed>              Krea img2img of in_<name>.png (close-up prompt)
    region.py put   <out> <name> <picture> <tag> <variant>       variant: detail (low from D, fine from the picture)
                                                                 or painted (the picture over the render's shade)
       (MATTER_SKIN_N = 2048 or 4096: the texel density the region is written at; the 8K atlas is the result)
    region.py calbedo <out>                                      C's rendered albedo (project_views.subject_albedo) as
                                                                 an sRGB 8K atlas, C_albedo.png
    region.py sheet <out> <name> <out.png> <column>...           one 768-px crop per column, side by side: C and D
                                                                 (D_seam9) through the region camera, or a picture
    region.py split <out> <name> <mm> <picture>                  D through the camera above <mm>, the picture below
                                                                 it (split_<mm>mm_<picture>): the marks stay D's
    region_detail.py <out> <name> <atlas>...                     the fine detail of each atlas through that camera

Throwaway, outside the repo; reuses tools/converters/fit/project_body.py and gen_views_model.py unchanged.
"""
import hashlib, json, os, sys, time
from pathlib import Path
R = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(R / "tools/converters/fit"))
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
import project_body as pb

SIZE = 1536
BODY = R / "library/parity/P27_Body"
D2K = BODY / "D_seam9_2048.png"
D8K = BODY / "D_seam9.png"
PROMPT = {
    "back": ("A close-up photograph of the bare upper back and shoulders of a real young woman about twenty, seen "
             "from directly behind, with a completely hairless body and a shaved bald head, light warm skin between "
             "Fitzpatrick III and IV. Real unretouched skin filling the frame: visible pores, fine vellus hair, small "
             "blemishes, tiny moles, faint freckles, uneven tone. Even, soft, shadowless studio light on a plain grey "
             "background. Not a 3D render, not CGI, not painted."),
    "calf": ("A close-up photograph of the bare lower legs and calves of a real young woman about twenty, seen from "
             "directly behind, completely hairless legs, light warm skin between Fitzpatrick III and IV. Real "
             "unretouched skin filling the frame: visible pores, fine vellus hair, small blemishes, tiny moles, faint "
             "freckles, uneven tone. Even, soft, shadowless studio light on a plain grey background. Not a 3D render, "
             "not CGI, not painted."),
}


def cam(out, name):
    return json.loads((out / f"cam_{name}.json").read_text())


def view(c):
    s = SIZE / c["metres"]
    return s


def prep(out, name, yaw, cx, cy, metres):
    out.mkdir(parents=True, exist_ok=True)
    c = {"yaw": yaw, "cx": cx, "cy": cy, "metres": metres}
    (out / f"cam_{name}.json").write_text(json.dumps(c))
    s = view(c)
    pb.proj.__defaults__ = (SIZE, s, cy)
    P, vt, T, vn = pb.mesh()
    g = pb.raster(P - np.array([cx, 0, 0]), vt, T, vn, yaw, SIZE, SIZE)
    np.savez(out / f"geom_{name}.npz", **g)
    D = pb.lin(np.asarray(Image.open(D2K).convert("RGB"), np.float64) / 255)
    n = D.shape[0]
    col = pb.sample(D, g["uv"][..., 0] * n - 0.5, g["uv"][..., 1] * n - 0.5)
    sh = pb.shade(g["n"])[..., None]
    img = np.where(g["mask"][..., None], col * sh, 0.18)
    pb.save(out / f"in_{name}.png", img)
    print(f"in_{name}.png at {1000 / s:.2f} mm a pixel; body pixels {g['mask'].mean() * 100:.0f} %")


def paint(out, name, strengths, seed, server="http://127.0.0.1:8188"):
    import gen_views_model as gv
    graph = json.loads(gv.WORKFLOWS["krea"].read_text())
    src = out / f"in_{name}.png"
    up = gv.upload(server, src)
    key = name.split("_")[0]
    for st in strengths:
        t = time.time()
        vals = {"IMAGE": up, "PROMPT": PROMPT[key], "SEED": seed, "STEPS": 8, "STRENGTH": st, "PREFIX": "matter_p27reg"}
        png, pid = gv.run(server, gv.fill(graph, vals))
        tag = f"{name}_s{round(st * 100):02d}_seed{seed}"
        (out / f"{tag}.png").write_bytes(png)
        (out / f"{tag}.json").write_text(json.dumps({"model": "krea", "seed": seed, "steps": 8, "strength": st,
            "source": src.name, "source_sha256": hashlib.sha256(src.read_bytes()).hexdigest(),
            "prompt": PROMPT[key], "prompt_id": pid, "seconds": round(time.time() - t, 1)}, indent=1))
        print(tag, round(time.time() - t, 1), "s", flush=True)


def gblur(img, m, sig):
    from scipy.ndimage import gaussian_filter
    mm = gaussian_filter(m.astype(np.float64), sig)
    if img.ndim == 2:
        return gaussian_filter(img * m, sig) / np.maximum(mm, 1e-6)
    return np.stack([gaussian_filter(img[..., k] * m, sig) for k in range(3)], -1) / np.maximum(mm, 1e-6)[..., None]


def put(out, name, picture, tag, variant):
    from scipy.ndimage import binary_erosion
    import gen_synth_skin as gss
    import make_kits
    t = time.time()
    c = cam(out, name); s = view(c)
    g = dict(np.load(out / f"geom_{name}.npz"))
    m = binary_erosion(g["mask"], iterations=6)                     # off the outline: no fit in this probe
    pic = pb.lin(np.asarray(Image.open(out / picture).convert("RGB").resize((SIZE, SIZE), Image.LANCZOS), np.float64) / 255)
    D = pb.lin(np.asarray(Image.open(D2K).convert("RGB"), np.float64) / 255)
    n2 = D.shape[0]
    Dimg = pb.sample(D, g["uv"][..., 0] * n2 - 0.5, g["uv"][..., 1] * n2 - 0.5)
    sig = 0.01 * s                                                   # 1 cm
    if variant == "detail":
        img = gblur(Dimg, m, sig) * pic / np.maximum(gblur(pic, m, sig), 1e-4)
    else:
        img = pic / pb.shade(g["n"])[..., None]
        img = img * (gblur(Dimg, m, 6 * sig).mean() / gblur(img, m, 6 * sig).mean())
    # texels at the working density
    N = gss.N
    mk = make_kits.load_mesh(gss.MESH)
    Pf, Nf, _, cover = gss.rasterise(mk)
    bid, ids = pb.body_island(N)
    body = (ids == bid) & cover
    yy, xx = np.nonzero(body)
    X = Pf[yy, xx].astype(np.float64) - np.array([c["cx"], 0, 0])
    pb.proj.__defaults__ = (SIZE, s, c["cy"])
    px, py, z = pb.proj(X, c["yaw"], SIZE, SIZE)
    fz = (Nf[yy, xx].astype(np.float64) @ pb.rot(c["yaw"]).T)[:, 2]
    ix, iy = np.floor(px).astype(int), np.floor(py).astype(int)
    inb = (ix >= 0) & (iy >= 0) & (ix < SIZE) & (iy < SIZE)
    ok = np.zeros(len(yy), bool)
    ok[inb] = m[iy[inb], ix[inb]] & (np.abs(z[inb] - g["z"][iy[inb], ix[inb]]) < 0.004) & (fz[inb] > 0.3)
    col = pb.sample(img, px[ok] - 0.5, py[ok] - 0.5)
    sel = np.zeros((N, N), bool); sel[yy[ok], xx[ok]] = True
    newN = np.zeros((N, N, 3)); newN[sel] = col
    # onto the 8K atlas: D_seam9 elsewhere; the region's texels replaced (bilinear from N, as put does)
    base = pb.lin(np.asarray(Image.open(D8K).convert("RGB"), np.float32) / 255).astype(np.float32)
    full = pb.pushpull(np.where(sel[..., None], newN, 0.0), sel)
    up = np.stack([np.asarray(Image.fromarray(full[..., k].astype(np.float32), "F").resize((8192, 8192), Image.BILINEAR))
                   for k in range(3)], -1)
    from scipy.ndimage import binary_dilation
    s8 = np.asarray(Image.fromarray(binary_erosion(sel, iterations=1).astype(np.uint8) * 255).resize((8192, 8192), Image.NEAREST)) > 0
    ids8, _, _ = pb.skin_islands(8192)
    s8 |= binary_dilation(s8, iterations=pb.GUTTER) & (ids8 == 0)   # the gutter too, as put does (27.2)
    base[s8] = up[s8]
    Image.fromarray((pb.srgb(base) * 255 + 0.5).astype(np.uint8)).save(out / f"D_{tag}.png")
    rec = {"picture": picture, "variant": variant, "N": N, "texels": int(sel.sum()), "seconds": round(time.time() - t)}
    (out / f"D_{tag}.json").write_text(json.dumps(rec))
    print(json.dumps(rec))


def calbedo(out):
    import project_views as pv
    a = pv.subject_albedo()
    Image.fromarray((pb.srgb(a) * 255 + 0.5).astype(np.uint8)).save(out / "C_albedo.png")


def ren(out, name, p):
    """An 8K atlas on hm08 through the region camera, the render's light, the raster's pixel cracks filled (linear)."""
    from scipy.ndimage import binary_closing
    g = np.load(out / f"geom_{name}.npz"); m = g["mask"]; mc = binary_closing(m, iterations=2)
    A = pb.lin(np.asarray(Image.open(p).convert("RGB"), np.float32) / 255); n = A.shape[0]
    col = pb.sample(A, g["uv"][..., 0] * n - 0.5, g["uv"][..., 1] * n - 0.5) * pb.shade(g["n"])[..., None]
    col = pb.pushpull(np.where(m[..., None], col, 0.0), m)
    return np.where(mc[..., None], col, 0.18)


def split(out, name, mm, picture):
    from scipy.ndimage import binary_erosion
    c = cam(out, name); s = view(c) * mm / 1000
    g = np.load(out / f"geom_{name}.npz"); m = binary_erosion(g["mask"], iterations=6)
    D = ren(out, name, D8K)
    P = pb.lin(np.asarray(Image.open(out / picture).convert("RGB").resize((SIZE, SIZE), Image.LANCZOS), np.float64) / 255)
    o = np.where(m[..., None], gblur(D, m, s) * P / np.maximum(gblur(P, m, s), 1e-4), D)
    pb.save(out / f"split_{mm:g}mm_{picture}", o)


def sheet(out, name, path, pics, box=(384, 200, 1152, 968)):
    from PIL import ImageDraw

    def im8(x):
        return Image.fromarray((pb.srgb(x) * 255 + 0.5).astype(np.uint8))
    named = {"C": ("C - the maker's skin on hm08 (probe renderer)", lambda: im8(ren(out, name, out / "C_albedo.png"))),
             "D": ("D as at click 2 - from the four-view picture (probe renderer)", lambda: im8(ren(out, name, D8K)))}
    cols = [(named[p][0], named[p][1]()) if p in named else (p, Image.open(out / p).convert("RGB")) for p in pics]
    W = box[2] - box[0]
    im = Image.new("RGB", (W * len(cols), W + 40), (30, 30, 30)); d = ImageDraw.Draw(im)
    for i, (t, c) in enumerate(cols):
        im.paste(c.crop(box), (W * i, 40)); d.text((W * i + 10, 12), f"{i + 1}. {t}", fill=(255, 255, 0))
    im.save(path)


if __name__ == "__main__":
    a = sys.argv[1:]
    out = Path(a[1])
    if a[0] == "prep":
        prep(out, a[2], int(a[3]), float(a[4]), float(a[5]), float(a[6]))
    elif a[0] == "paint":
        paint(out, a[2], [float(v) for v in a[3].split(",")], int(a[4]))
    elif a[0] == "put":
        put(out, a[2], a[3], a[4], a[5])
    elif a[0] == "calbedo":
        calbedo(out)
    elif a[0] == "sheet":
        sheet(out, a[2], Path(a[3]), a[4:])
    elif a[0] == "split":
        split(out, a[2], float(a[3]), a[4])
