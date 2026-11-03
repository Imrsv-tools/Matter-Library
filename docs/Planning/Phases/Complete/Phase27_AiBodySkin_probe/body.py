#!/usr/bin/env python3
"""Phase27 Pass 2 premise probe: routes for the body's skin (throwaway; ML_P27_D1).

    MATTER_SKIN_N=2048 uv run --with scipy python -I body.py prep  <out>
    python3 -I body.py paint <out> <source.png> <tag> <prompt key> <strength,...> <seed>
    MATTER_SKIN_N=2048 uv run --with scipy python -I body.py back  <out> <picture> <tag> (fb|uv)
    MATTER_SKIN_N=2048 uv run --with scipy python -I body.py view  <out> <tag,...>

Route B (+D): hm08's whole body rendered front and back (orthographic, Tone34's colour, a soft key)
side by side as ONE picture; Krea repaints it; each half goes back onto the body island through its
own camera, each texel from the camera it faces (a hard cut where the normal turns sideways).
Route A: the body island cut from Tone34 at 2048, upright, repainted flat; put back as is.
Only the body island changes; head, hands, feet stay C. Everything is written under <out>.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
FIT = REPO / "tools" / "converters" / "fit"
sys.path.insert(0, str(FIT))

S = 800.0                    # pixels per metre in the renders (1.25 mm a pixel)
HW, HH = 832, 1536           # one view's size; the picture is two side by side
CY = 0.015                   # the body's middle height (m)
PROMPTS = {
    "fb": ("A full-length photograph of the same real young woman about twenty shown twice side by side: on the left "
           "seen from the front, on the right seen from the back. She stands in an A-pose with her arms held out from "
           "her sides, nude, with a completely hairless body and a shaved bald head, light warm skin between "
           "Fitzpatrick III and IV. Real unretouched skin: visible pores, fine vellus hair, small blemishes, tiny moles, "
           "faint freckles, uneven tone, slight redness on the knees, elbows and knuckles. Even, soft, shadowless "
           "studio light on a plain grey background. Not a 3D render, not CGI, not painted."),
    "uv": ("A flat unwrapped UV texture map of a real human body's skin, from a photogrammetry scan of a real young "
           "woman about twenty, light warm skin between Fitzpatrick III and IV, completely hairless body. The front of "
           "the torso is laid flat in the centre with the arms out to the sides and the legs below, the back split down "
           "the spine to the left and right edges. Albedo only: even, shadowless, delit, no lighting, no highlights. "
           "Not a 3D render, not CGI, not painted. Real unretouched skin: visible pores, fine vellus hair, small "
           "blemishes, tiny moles, faint freckles, uneven tone."),
}


def lin(s):
    import numpy as np
    return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)


def srgb(x):
    import numpy as np
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


def mesh():
    import numpy as np
    import gen_synth_skin as gss, make_kits
    m = make_kits.load_mesh(gss.MESH)
    P = np.array(m["points"], np.float64)
    vt = np.array(m["vt"], np.float64)
    T = []
    for f in m["faces"]:
        for t in ((0, 1, 2), (0, 2, 3)) if len(f) == 4 else ((0, 1, 2),):
            T.append([(f[i][0], f[i][1]) for i in t])
    T = np.array(T)
    vn = np.zeros_like(P)
    for tri in T:
        vi = tri[:, 0]
        vn[vi] += np.cross(P[vi[1]] - P[vi[0]], P[vi[2]] - P[vi[0]])
    vn /= np.maximum(np.linalg.norm(vn, axis=1, keepdims=True), 1e-12)
    return P, vt, T, vn


def rot(yaw):
    """World → view: the camera looks along -z of the view frame after turning the body by ``yaw``."""
    import numpy as np
    a = np.radians(yaw)
    return np.array([[np.cos(a), 0, -np.sin(a)], [0, 1, 0], [np.sin(a), 0, np.cos(a)]])


def proj(X, yaw, s=S, w=HW, h=HH, cy=CY, cx0=0.0):
    """Orthographic: x right, y up in the view; depth = -z (smaller is closer)."""
    V = X @ rot(yaw).T
    return w / 2 + s * (V[..., 0] - cx0), h / 2 - s * (V[..., 1] - cy), -V[..., 2], V


def raster(P, vt, T, vn, yaw, s=S, w=HW, h=HH, cy=CY, cx0=0.0):
    import numpy as np
    px, py, z, _ = proj(P, yaw, s, w, h, cy, cx0)
    nv = vn @ rot(yaw).T
    zb = np.full((h, w), np.inf); uvb = np.zeros((h, w, 2)); nb = np.zeros((h, w, 3))
    for tri in T:
        vi, ti = tri[:, 0], tri[:, 1]
        ax, bx, cx = px[vi]; ay, by, cyy = py[vi]
        den = (by - cyy) * (ax - cx) + (cx - bx) * (ay - cyy)
        if abs(den) < 1e-9:
            continue
        x0, x1 = int(max(np.floor(min(ax, bx, cx)), 0)), int(min(np.ceil(max(ax, bx, cx)), w - 1))
        y0, y1 = int(max(np.floor(min(ay, by, cyy)), 0)), int(min(np.ceil(max(ay, by, cyy)), h - 1))
        if x1 < x0 or y1 < y0:
            continue
        ys, xs = np.mgrid[y0:y1 + 1, x0:x1 + 1]
        qx, qy = xs + 0.5, ys + 0.5
        w0 = ((by - cyy) * (qx - cx) + (cx - bx) * (qy - cyy)) / den
        w1 = ((cyy - ay) * (qx - cx) + (ax - cx) * (qy - cyy)) / den
        w2 = 1 - w0 - w1
        ins = (w0 >= 0) & (w1 >= 0) & (w2 >= 0)
        if not ins.any():
            continue
        Wb = np.stack([w0[ins], w1[ins], w2[ins]], -1)
        zz = Wb @ z[vi]
        yy, xx = ys[ins], xs[ins]
        c = zz < zb[yy, xx]
        yy, xx, Wb, zz = yy[c], xx[c], Wb[c], zz[c]
        zb[yy, xx] = zz
        uv = Wb @ vt[ti]
        uvb[yy, xx, 0], uvb[yy, xx, 1] = uv[:, 0], 1 - uv[:, 1]
        n = Wb @ nv[vi]
        nb[yy, xx] = n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)
    return {"z": zb, "uv": uvb, "n": nb, "mask": np.isfinite(zb)}


def shade(n, amb=0.5):
    import numpy as np
    l = np.array([-0.35, 0.45, 1.0]); l /= np.linalg.norm(l)
    return amb + (1 - amb) * np.clip(n @ l, 0, 1)


def sample(img, uv):
    import numpy as np
    H, W = img.shape[:2]
    x = np.clip(uv[..., 0] * W - 0.5, 0, W - 1.001); y = np.clip(uv[..., 1] * H - 0.5, 0, H - 1.001)
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    fx, fy = (x - x0)[..., None], (y - y0)[..., None]
    return ((img[y0, x0] * (1 - fx) + img[y0, x0 + 1] * fx) * (1 - fy) + (img[y0 + 1, x0] * (1 - fx) + img[y0 + 1, x0 + 1] * fx) * fy)


def pushpull(img, known):
    import numpy as np
    if known.all() or min(img.shape[:2]) < 2:
        return img
    h, w = img.shape[:2]
    H2, W2 = (h + 1) // 2, (w + 1) // 2
    pi = np.zeros((H2 * 2, W2 * 2, 3)); pk = np.zeros((H2 * 2, W2 * 2))
    pi[:h, :w] = img * known[..., None]; pk[:h, :w] = known
    si = pi.reshape(H2, 2, W2, 2, 3).sum((1, 3)); sk = pk.reshape(H2, 2, W2, 2).sum((1, 3))
    low = pushpull(np.where(sk[..., None] > 0, si / np.maximum(sk, 1e-9)[..., None], 0), sk > 0)
    up = np.repeat(np.repeat(low, 2, 0), 2, 1)[:h, :w]
    return np.where(known[..., None], img, up)


def save(path, linimg):
    import numpy as np
    from PIL import Image
    Image.fromarray((srgb(linimg) * 255 + 0.5).astype(np.uint8)).save(path)


def cmd_prep(out: Path):
    import numpy as np
    from PIL import Image
    from scipy import ndimage
    import gen_synth_skin as gss, make_kits
    import project_views as pv
    Image.MAX_IMAGE_PIXELS = None
    out.mkdir(parents=True, exist_ok=True)
    t = time.time()
    m = make_kits.load_mesh(gss.MESH)
    Pf, Nf, _, cover = gss.rasterise(m)
    lab, n = ndimage.label(cover)
    sizes = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
    body = lab == (int(np.argmax(sizes)) + 1)
    a8 = pv.subject_albedo()                                     # 8K linear
    k = a8.shape[0] // 2048
    C = a8.reshape(2048, k, 2048, k, 3).mean((1, 3))
    np.savez(out / "atlas.npz", C=C.astype(np.float32), P=Pf.astype(np.float32), N=Nf.astype(np.float32),
             cover=cover, body=body)
    print(f"atlas fields {time.time() - t:.0f}s; body texels {body.sum()}")
    P, vt, T, vn = mesh()
    pic = np.full((HH, 2 * HW, 3), 0.18)
    for i, yaw in enumerate((0, 180)):
        g = raster(P, vt, T, vn, yaw)
        np.savez(out / f"geom_{yaw}.npz", **g)
        col = sample(C, g["uv"]) * shade(g["n"])[..., None]
        half = pic[:, i * HW:(i + 1) * HW]
        half[g["mask"]] = col[g["mask"]]
    save(out / "in_fb.png", pic)
    rr, cc = np.nonzero(body)
    y0, y1, x0, x1 = rr.min(), rr.max() + 1, cc.min(), cc.max() + 1
    isl = pushpull(C[y0:y1, x0:x1].astype(np.float64), body[y0:y1, x0:x1])
    hgt = 1536; wid = int(round((x1 - x0) * hgt / (y1 - y0) / 16)) * 16
    Image.fromarray((srgb(isl) * 255 + 0.5).astype(np.uint8)).resize((wid, hgt), Image.LANCZOS).save(out / "in_uv.png")
    json.dump({"bbox": [int(y0), int(y1), int(x0), int(x1)], "uv_size": [wid, hgt]}, open(out / "frame.json", "w"))
    print(f"prep done {time.time() - t:.0f}s; uv source {wid}x{hgt}")


def cmd_paint(out: Path, src: Path, tag: str, key: str, strengths: str, seed: int):
    import hashlib
    import gen_views_model as g
    server = "http://127.0.0.1:8188"
    graph = json.loads(g.WORKFLOWS["krea"].read_text())
    raw = src.read_bytes()
    named = out / f"{src.stem}_{hashlib.sha256(raw).hexdigest()[:12]}.png"
    named.write_bytes(raw)
    up = g.upload(server, named)
    for st in strengths.split(","):
        t = time.time()
        png, pid = g.run(server, g.fill(graph, {"IMAGE": up, "PROMPT": PROMPTS[key], "SEED": seed, "STEPS": 8,
                                                "STRENGTH": float(st), "PREFIX": f"matter_p27_{tag}"}))
        name = f"{tag}_s{int(float(st) * 100)}_seed{seed}"
        (out / f"{name}.png").write_bytes(png)
        json.dump({"source": src.name, "prompt": PROMPTS[key], "strength": float(st), "seed": seed, "steps": 8,
                   "workflow": "krea2turbo_img2img.json", "prompt_id": pid}, open(out / f"{name}.json", "w"), indent=1)
        print(f"{name}: {time.time() - t:.1f}s", flush=True)


def cmd_back(out: Path, picture: Path, tag: str, how: str):
    import numpy as np
    from PIL import Image
    A = np.load(out / "atlas.npz")
    C, Pa, Na, body = A["C"].astype(np.float64), A["P"], A["N"], A["body"]
    pic = lin(np.asarray(Image.open(picture).convert("RGB"), np.float64) / 255)
    D = C.copy()
    if how == "uv":
        F = json.load(open(out / "frame.json"))
        y0, y1, x0, x1 = F["bbox"]
        p = np.asarray(Image.fromarray((srgb(pic) * 255 + .5).astype(np.uint8)).resize((x1 - x0, y1 - y0), Image.LANCZOS), np.float64) / 255
        sel = body[y0:y1, x0:x1]
        D[y0:y1, x0:x1][sel] = lin(p)[sel]
    else:
        pic = np.asarray(Image.fromarray((srgb(pic) * 255 + .5).astype(np.uint8)).resize((2 * HW, HH), Image.LANCZOS), np.float64) / 255
        pic = lin(pic)
        rr, cc = np.nonzero(body)
        X = Pa[rr, cc].astype(np.float64); Nn = Na[rr, cc].astype(np.float64)
        got = np.zeros((len(rr), 3)); have = np.zeros(len(rr), bool); face = np.zeros(len(rr))
        for i, yaw in enumerate((0, 180)):
            g = np.load(out / f"geom_{yaw}.npz")
            px, py, z, _ = proj(X, yaw)
            nz = (Nn @ rot(yaw).T)[:, 2]
            xi, yi = np.clip(px.astype(int), 0, HW - 1), np.clip(py.astype(int), 0, HH - 1)
            vis = (z <= g["z"][yi, xi] + 0.004) & (nz > 0)
            take = vis & (nz > face)
            half = pic[:, i * HW:(i + 1) * HW]
            uv = np.stack([px / HW, py / HH], -1)
            got[take] = sample(half, uv[take]); face[take] = nz[take]; have |= take
        sh = np.zeros_like(C); kn = np.zeros(C.shape[:2], bool)
        sh[rr[have], cc[have]] = got[have]; kn[rr[have], cc[have]] = True
        fill = pushpull(sh, kn)
        D[body] = fill[body]
        print(f"body texels seen {have.mean() * 100:.1f} %; holes filled by pull-push {100 - have.mean() * 100:.1f} %")
    k = C[body].mean(0) / D[body].mean(0)                      # the probe holds D's body mean to C's
    D[body] *= k
    np.save(out / f"D_{tag}.npy", D.astype(np.float32))
    save(out / f"D_{tag}_atlas.png", D)
    print(f"D_{tag}: gain {np.round(k, 3)}")


VIEWS = {"front": (0, 520, 0.015, 0.0, 1100, 1536), "back": (180, 520, 0.015, 0.0, 1100, 1536),
         "side": (90, 520, 0.015, 0.0, 700, 1536), "q": (35, 520, 0.015, 0.0, 900, 1536),
         "torso_f": (0, 1500, 0.35, 0.0, 1100, 900), "torso_b": (180, 1500, 0.35, 0.0, 1100, 900),
         "neck_q": (35, 2600, 0.62, 0.03, 900, 700), "arm_side": (60, 1400, 0.38, 0.30, 900, 700)}


def cmd_view(out: Path, tags: str):
    import numpy as np
    from PIL import Image, ImageDraw
    A = np.load(out / "atlas.npz")
    maps = [("C", A["C"].astype(np.float64))] + [(t, np.load(out / f"D_{t}.npy").astype(np.float64)) for t in tags.split(",")]
    P, vt, T, vn = mesh()
    for v, (yaw, s, cy, cx0, w, h) in VIEWS.items():
        g = raster(P, vt, T, vn, yaw, s, w, h, cy, cx0)
        sh = shade(g["n"])[..., None]
        row = []
        for name, M in maps:
            im = np.full((h, w, 3), 0.18)
            im[g["mask"]] = (sample(M, g["uv"]) * sh)[g["mask"]]
            pi = Image.fromarray((srgb(im) * 255 + .5).astype(np.uint8))
            ImageDraw.Draw(pi).text((10, 10), f"{name} · {v}", fill=(255, 255, 255))
            row.append(pi)
        sheet = Image.new("RGB", (w * len(row), h))
        for i, pi in enumerate(row):
            sheet.paste(pi, (i * w, 0))
        sheet.save(out / f"view_{v}.png")
        print("view", v, flush=True)


if __name__ == "__main__":
    c, out = sys.argv[1], Path(sys.argv[2])
    if c == "prep":
        cmd_prep(out)
    elif c == "paint":
        cmd_paint(out, Path(sys.argv[3]), sys.argv[4], sys.argv[5], sys.argv[6], int(sys.argv[7]))
    elif c == "back":
        cmd_back(out, Path(sys.argv[3]), sys.argv[4], sys.argv[5])
    elif c == "view":
        cmd_view(out, sys.argv[3])
