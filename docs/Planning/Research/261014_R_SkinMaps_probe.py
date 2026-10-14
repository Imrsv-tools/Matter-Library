"""Disposable probe for 261014_R_SkinMaps.md (Pass 5): does a skin map beat a tone per part, and does
a map the library makes itself (F-SKM-21, RD-SKM-2) hold up against a photo atlas?

Nothing in the repo is written: every output lands in the git-ignored scratch folder <out>
(default library/parity/SkinMapsProbe). Three variants of Skin_FitzpatrickIV on the rig's character:
  today  - the article as it is: a tone per part (Lips_FitzpatrickIV on the lips).
  photo  - a probe copy that takes a map (F-SKM-19), carrying MakeHuman's CC0 photo atlas read by
           luminance (MAP-F4). A COMPARISON ONLY: never published (RD-SKM-2).
  made   - the same copy carrying a colour map made from CC0 parts only (RD-SKM-3: one map per tone,
           with hue): MPFB2's region masks and thickness map, the measured tones, an AO bake of the
           mesh, and 3D noise. No photograph. Neutral at the groin by construction (RD-SKM-4).
On both map variants the Lips part wears the skin article and the map (F-SKM-9), and the body keeps
hm08's atlas st, with the pores placed by uv_scale = meters_per_tile / metres-per-UV-unit (P18's stopgap).

Steps (run from anywhere; absolute paths):
  blender -b --factory-startup --python <this> -- maps <out>       # bake + compose the two maps
  uv run --directory <repo> python <this> articles <out>           # assemble the two probe articles
  uv run --directory <repo> python <this> render <out> today|photo|made
  uv run --directory <repo> --with pillow python <this> sheet <out>
"""
import json
import os
import subprocess
import sys
import urllib.request
import hashlib
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
PARITY = REPO / "tools" / "parity"
sys.path[:0] = [str(PARITY), str(PARITY / "scene"), str(PARITY / "drivers")]

SKIN = "Skin_FitzpatrickIV_Clean_Base_s001_v01"
RECIPES = REPO / "tools" / "converters" / "recipes"
MPFB = ("https://raw.githubusercontent.com/makehumancommunity/mpfb2/"
        "3edf9df0551765be43563d047888cf7877eb89b4/src/mpfb/data/textures/")
# git blob sha1 of each file at that commit (GitHub contents API, read 2026-10-14); CC0 (LICENSE.ASSETS.md)
MPFB_PINS = {"mpfb_face.jpg": "914b4b1e7e8bef3bd8a2d12821f70160eb294f17",
             "mpfb_lips.jpg": "2fe3cb395e7903f35f5b61dc2a922b218b231ad2",
             "mpfb_ears.jpg": "f136d23785f93ca54c150d475d7ee24cf08e8c43",
             "mpfb_eyelids.jpg": "d1c775515d81a1b3ad8114f87841186b8a2f215b",
             "mpfb_aureolae.jpg": "f7638a8c03d95bfefb8dde154ecb13ac286e0e0b",
             "sss.png": "f62a5b6581f51d3412b79a43e7ae0470e02466ea"}
PHOTO = "skins/young_caucasian_female/young_lightskinned_female_diffuse.png"   # as MAP-F4's probe
N = 2048


def fetch_mpfb(name: str, cache: Path) -> Path:
    p = cache / name
    if not p.is_file():
        req = urllib.request.Request(MPFB + name, headers={"User-Agent": "matter-library-probe"})
        p.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    data = p.read_bytes()
    got = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
    if got != MPFB_PINS[name]:
        raise SystemExit(f"{name}: blob sha {got} != pinned {MPFB_PINS[name]}")
    return p


# ---------------------------------------------------------------- maps (inside Blender) ----------
def maps(out: Path) -> None:
    import bpy
    import numpy as np
    import build_character as bc

    src = out / "_src"
    src.mkdir(parents=True, exist_ok=True)
    obj = src / "base.obj"
    obj.write_bytes(bc.source("base.obj"))                       # pinned + sha-checked by the rig
    (src / "photo.png").write_bytes(bc.source(bc.PACK, PHOTO))

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.obj_import(filepath=str(obj), use_split_groups=True)
    body = next(o for o in bpy.context.scene.objects if o.type == "MESH" and o.name.lower() == "body")
    for o in list(bpy.context.scene.objects):
        if o is not body:
            bpy.data.objects.remove(o)
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.render.bake.margin = 16
    world = bpy.data.worlds.new("w"); sc.world = world
    world.light_settings.distance = 0.4                          # MakeHuman units: 4 cm of occlusion

    def bake(kind: str, samples: int, emit_coords: bool = False):
        img = bpy.data.images.new(kind, N, N, alpha=True, float_buffer=True)
        img.generated_color = (0, 0, 0, 0)
        mat = bpy.data.materials.new(kind); mat.use_nodes = True
        nt = mat.node_tree; nt.nodes.clear()
        out_n = nt.nodes.new("ShaderNodeOutputMaterial")
        em = nt.nodes.new("ShaderNodeEmission")
        if emit_coords:
            tc = nt.nodes.new("ShaderNodeTexCoord")
            nt.links.new(tc.outputs["Object"], em.inputs["Color"])
        nt.links.new(em.outputs[0], out_n.inputs[0])
        tex = nt.nodes.new("ShaderNodeTexImage"); tex.image = img
        nt.nodes.active = tex
        body.data.materials.clear(); body.data.materials.append(mat)
        bpy.context.view_layer.objects.active = body; body.select_set(True)
        sc.cycles.samples = samples
        bpy.ops.object.bake(type=kind)
        a = np.empty(N * N * 4, np.float32); img.pixels.foreach_get(a)
        return a.reshape(N, N, 4)

    ao = bake("AO", 64)[..., 0]
    pos_px = bake("EMIT", 1, emit_coords=True)
    # the bake fills alpha everywhere (measured: "covered" read 1.0), so a texel is on the mesh where it
    # got a position; the background keeps the image's (0, 0, 0). Includes the 16 px bake margin.
    pos = pos_px[..., :3]
    cover = np.linalg.norm(pos, axis=-1) > 1e-5

    def load(path: Path, chan: int = 0):
        im = bpy.data.images.load(str(path))
        im.colorspace_settings.name = "Non-Color"
        if tuple(im.size) != (N, N):
            im.scale(N, N)
        a = np.empty(N * N * 4, np.float32); im.pixels.foreach_get(a)
        return a.reshape(N, N, 4)[..., chan] if chan is not None else a.reshape(N, N, 4)

    m = {k: load(fetch_mpfb(f"mpfb_{k}.jpg", src)) for k in ("face", "lips", "ears", "eyelids", "aureolae")}
    sss = load(fetch_mpfb("sss.png", src))
    sss = np.clip(sss / max(np.percentile(sss[cover], 99), 1e-6), 0, 1)

    def blur(a, r):                                   # three box passes ~ a Gaussian of sigma ~ r
        for _ in range(3):
            for ax in (0, 1):
                c = np.cumsum(np.pad(a, [(r + 1, r) if i == ax else (0, 0) for i in (0, 1)], mode="edge"), axis=ax)
                a = (np.take(c, range(2 * r + 1, c.shape[ax]), axis=ax) - np.take(c, range(0, c.shape[ax] - 2 * r - 1), axis=ax)) / (2 * r + 1)
        return a

    def vnoise(P, scale, seed):                       # 3D value noise: seamless across UV seams
        q = P / scale; i = np.floor(q).astype(np.int64); f = q - i; f = f * f * (3 - 2 * f)
        def h(dx, dy, dz):
            n = ((i[..., 0] + dx) * 73856093) ^ ((i[..., 1] + dy) * 19349663) ^ ((i[..., 2] + dz) * 83492791) ^ seed
            return ((n * 2654435761) % 4294967296) / 4294967296.0
        acc = 0
        for dx in (0, 1):
            for dy in (0, 1):
                for dz in (0, 1):
                    w = ((f[..., 0] if dx else 1 - f[..., 0]) * (f[..., 1] if dy else 1 - f[..., 1])
                         * (f[..., 2] if dz else 1 - f[..., 2]))
                    acc = acc + w * h(dx, dy, dz)
        return acc * 2 - 1

    recipe = lambda n: json.loads((RECIPES / f"{n}.json").read_text())
    tone = np.array([float(x) for x in recipe(SKIN)["base_color_const"].split(",")])
    lip = np.array([float(x) for x in recipe("Lips_FitzpatrickIV_Clean_Base_s001_v01")["base_color_const"].split(",")])

    # cheeks: two blobs placed from the face texels' own 3D positions (no hand-painting)
    F = pos[(m["face"] > 0.5) & cover]
    ext = F.max(0) - F.min(0); lat = 0                       # X is lateral (the body is symmetric in X)
    up = int(np.argmax(np.where(np.arange(3) == lat, -1, ext)))
    front = 3 - lat - up
    allp = pos[cover]
    sign = 1.0 if F[:, front].mean() > allp[:, front].mean() else -1.0
    cx, w, h0, hh = F[:, lat].mean(), ext[lat], F[:, up].min(), ext[up]
    cheeks = np.zeros((N, N))
    for side in (-1, 1):
        c = np.zeros(3); c[lat] = cx + side * 0.27 * w; c[up] = h0 + 0.42 * hh
        near = F[(np.abs(F[:, lat] - c[lat]) < 0.05 * w) & (np.abs(F[:, up] - c[up]) < 0.05 * hh)]
        c[front] = (near[:, front].max() if sign > 0 else near[:, front].min()) if len(near) else F[:, front].mean()
        cheeks = np.maximum(cheeks, np.exp(-((np.linalg.norm(pos - c, axis=-1) / (0.2 * w)) ** 2)))
    face_soft = blur(m["face"], 12)
    cheeks *= face_soft

    n1, n2 = vnoise(pos, 0.25, 7), vnoise(pos, 1.0, 11)
    # v1 (0.55 sss, 0.5 ears, 0.6 cheeks, 0.06 noise) rendered the whole body redder than its tone: the
    # redness moved the AVERAGE (Pass 5). v2: about half the strengths, and the average restored below.
    redness = np.clip(0.3 * sss + 0.4 * blur(m["ears"], 6) + 0.35 * cheeks + 0.25 * blur(m["aureolae"], 4)
                      + 0.05 * n1, 0, 1.2)
    HB = np.array([0.0, 0.42, 0.34])                    # haemoglobin: absorbs green and blue
    MEL = np.array([0.88, 0.84, 0.80])                  # the darker-skin side of the same tone
    col = tone * np.exp(-redness[..., None] * HB)
    dark = np.clip(1 - ao, 0, 1) * 0.9 + 0.35 * blur(m["eyelids"], 6) + 0.35 * blur(m["aureolae"], 4)
    col = col * (1 - np.clip(dark, 0, 1)[..., None] * (1 - MEL) * 2.2)
    col = col * (1 + 0.035 * n2)[..., None]
    skin = cover & (m["lips"] < 0.5)                    # v2: the measured tone stays the skin's average
    col = col * (tone / col[skin].mean(0))
    lm = np.clip(blur(m["lips"], 5) * 1.15, 0, 1)[..., None]   # feathered: no hard line at the lips
    col = col * (1 - lm) + lip * (0.92 + 0.08 * n1[..., None]) * lm

    def write(name: str, ratio, meta: dict):
        k = np.maximum(np.percentile(ratio[cover], 99.9, axis=0), 1e-6)   # F-SKM-20: peak -> 1, const x k
        mp = np.clip(ratio / k, 0, 1)
        enc = np.where(mp <= 0.0031308, mp * 12.92, 1.055 * mp ** (1 / 2.4) - 0.055)   # srgb_texture
        img = bpy.data.images.new(name, N, N, alpha=True)
        img.colorspace_settings.name = "Non-Color"
        rgba = np.concatenate([enc, np.ones((N, N, 1))], -1).astype(np.float32)
        img.pixels.foreach_set(rgba.ravel())
        img.filepath_raw = str(out / f"{name}_basecolor.png"); img.file_format = "PNG"; img.save()
        meta[name] = {"k": [float(x) for x in np.atleast_1d(k)] * (3 // np.atleast_1d(k).size),
                      "base_color_const": [float(x) for x in tone * k],
                      "map": str(out / f"{name}_basecolor.png")}

    meta = {}
    write("made", col / tone, meta)
    ph = load(src / "photo.png", None)[..., :3]
    ph = np.where(ph <= 0.04045, ph / 12.92, ((ph + 0.055) / 1.055) ** 2.4)
    L = ph @ np.array([0.2126, 0.7152, 0.0722])
    det = L / L[cover].mean()
    write("photo", np.repeat(det[..., None], 3, -1), meta)
    meta["luminance_detail_p5_p50_p95"] = [float(x) for x in np.percentile(det[cover], [5, 50, 95])]
    fm = (m["face"] > 0.5) & cover
    meta["face_texels"] = int(fm.sum())
    meta["face_share_of_covered"] = float(fm.sum() / cover.sum())
    meta["covered_share_of_atlas"] = float(cover.mean())
    (out / "maps.json").write_text(json.dumps(meta, indent=2) + "\n")
    print(json.dumps(meta, indent=2))


# ---------------------------------------------------------------- articles (uv python) -----------
def articles(out: Path) -> None:
    import build_character as bc
    meta = json.loads((out / "maps.json").read_text())
    dens = bc.load_parts()["Body"]["density"][1]                      # metres per UV unit on the body
    rec = json.loads((RECIPES / f"{SKIN}.json").read_text())
    mtlx_dir = (REPO / "MatterLibrary" / "materials" / rec["path"]).parent
    s = rec["meters_per_tile"] / dens
    for v in ("photo", "made"):
        r = dict(rec)
        r["base_color_map"] = True                                     # F-SKM-19: declare the input
        r.pop("subsurface_color", None)                                # ... and let the scatter follow it
        # PROBE ONLY: Blender's loader refuses a scatter colour following a TINTED base
        # (load_article.py, F-P09-5: "not mapped in Blender yet"; measured 2026-10-14, F-SKM-23), so the
        # probe copies drop the Creator tint port. It sits at white by default, so the look is unchanged.
        r["lcd_ports"] = [p for p in r["lcd_ports"] if p != "base_color_tint"]
        r["base_color_const"] = ", ".join(f"{x:.4f}" for x in meta[v]["base_color_const"])
        for key in ("roughness_tex", "normal_tex"):
            r[key] = str((mtlx_dir / r[key]).resolve())
        r["overlays"] = [dict(o, texture=str((mtlx_dir / o["texture"]).resolve())) for o in r["overlays"]]
        d = out / "articles" / v; d.mkdir(parents=True, exist_ok=True)
        spec = d / "recipe.json"; spec.write_text(json.dumps(r, indent=2))
        dst = d / f"{SKIN}.mtlx"
        subprocess.run([sys.executable, str(REPO / "tools/converters/assemble_mtlx.py"), str(spec), "-o", str(dst)],
                       check=True)
        t = dst.read_text()
        old = '<input name="uv_scale" type="vector2" value="1.0, 1.0"'
        if t.count(old) != 1:
            raise SystemExit(f"{dst}: uv_scale default found {t.count(old)} times")
        dst.write_text(t.replace(old, f'<input name="uv_scale" type="vector2" value="{s:.5f}, {s:.5f}"'))
        print(f"{v}: {dst}  base {r['base_color_const']}  uv_scale {s:.5f} (body {dens:.3f} m per UV unit)")


# ---------------------------------------------------------------- render (uv python) -------------
def render(out: Path, variant: str) -> int:
    os.environ.setdefault("USD_TOOLS_ROOT", str(Path.home() / "usd-tools"))
    import build_character as bc
    import job as jobmod
    import rig
    jobmod.CHARACTER_VIEWS = {v: jobmod.CHARACTER_VIEWS[v] for v in ("wide", "face", "hand")}
    if variant == "today":
        return rig.main(["--character", SKIN, "--out", str(out / "today")])
    art = out / "articles" / variant / f"{SKIN}.mtlx"
    pic = Path(json.loads((out / "maps.json").read_text())[variant]["map"])
    bc.MESHES["body"]["fit"] = "probe"                    # the body and lips keep hm08's atlas st
    bc.MESHES["body"]["fit_parts"] = ["Body", "Lips"]
    orig = bc.base_color_maps
    bc.base_color_maps = lambda: {k: p for k, p in orig().items() if "probe" not in str(p)} | {
        "/World/Character/Body": pic, "/World/Character/Lips": pic}
    cast = rig.cast_for(SKIN)
    rig.cast_for = lambda skin: cast | {"Lips": str(art)}
    return rig.main(["--character", str(art), "--out", str(out / variant)])


# ---------------------------------------------------------------- sheet (pillow) -----------------
def sheet(out: Path) -> None:
    from PIL import Image, ImageDraw
    cell, rows = 400, []
    for view, sfx in (("face", "__face"), ("hand", "__hand"), ("whole body", "")):
        for tool in ("blender", "storm", "unreal"):
            rows.append((f"{view} · {tool}", [out / v / tool / f"defaults{sfx}.png"
                                               for v in ("today", "photo", "made_v1", "made")]))
    heads = ["today: a tone per part", "photo atlas by luminance (comparison only)",
             "library-made v1 (average drifted red)", "library-made v2 (average = measured tone)"]
    S = Image.new("RGB", (4 * cell + 160, 30 + len(rows) * cell), "white"); d = ImageDraw.Draw(S)
    for j, hd in enumerate(heads):
        d.text((160 + j * cell + 6, 8), hd, fill="black")
    for i, (lab, files) in enumerate(rows):
        d.text((6, 30 + i * cell + cell // 2), lab, fill="black")
        for j, f in enumerate(files):
            if f.is_file():
                S.paste(Image.open(f).convert("RGB").resize((cell, cell)), (160 + j * cell, 30 + i * cell))
            else:
                d.text((160 + j * cell + 10, 30 + i * cell + cell // 2), "not rendered", fill="red")
    p = out / "SkinMapsProbe_sheet.jpg"; S.save(p, quality=88); print(p)


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else sys.argv[1:]
    mode, out = argv[0], Path(argv[1] if len(argv) > 1 else REPO / "library/parity/SkinMapsProbe").resolve()
    out.mkdir(parents=True, exist_ok=True)
    if mode == "maps":
        maps(out)
    elif mode == "articles":
        articles(out)
    elif mode == "render":
        sys.exit(render(out, argv[2]))
    elif mode == "sheet":
        sheet(out)
    else:
        raise SystemExit(__doc__)
