#!/usr/bin/env python3
"""An image model's front portrait becomes the head island's skin, through hm08's front camera (Phase25).

    uv run tools/converters/fit/paint_uv.py cut <dir>                               # hm08's island frame
    uv run tools/converters/fit/project_face.py source <dir>                         # the model's source
    python3 -I tools/converters/fit/project_face.py paint <dir> [--seeds 7] [--strength 0.9]
    uv run --with mediapipe==1.2.0 tools/converters/fit/project_face.py landmarks <dir> --render
    uv run --with mediapipe==1.2.0 tools/converters/fit/project_face.py landmarks <dir> <picture>
    uv run --with scipy tools/converters/fit/project_face.py field <dir> <picture> [--min-nz 0.08]   # first pass
    uv run --with scipy tools/converters/fit/project_face.py ears  <dir> first_<stem>.png
    uv run --with scipy tools/converters/fit/project_face.py field <dir> <picture> --ears ears_<stem>.json
    uv run --with scipy tools/converters/fit/paint_uv.py put <dir> face_<stem>.png <tag>

Krea 2, asked for an unwrapped head, draws a FRONT PORTRAIT with only the scalp unrolled round it
(F-P25-14), so its face is never warped in UV space. ``source`` stands the subject's head island up at
the model's size (the island Pass 2 painted from, F-P25-7); ``paint`` has Krea repaint it at 0.9 with
the target's words through the lead's ComfyUI (standard library only, RD-P25-7), one record per picture.
``landmarks`` puts MediaPipe's 478 face points on the picture, or on hm08's front render with the eye
points snapped to the eye openings found from depth (F-P25-25: on the render the eye is an empty
opening and MediaPipe guesses its lids, unevenly). ``field`` maps the picture onto the island: each
visible face texel takes its colour through the front camera (landmark triangles, picture → render,
then the render pixel's texture coordinate, RD-P25-15); one coordinate field carries the rest of the
island from the picture's own layout, relaxed as a membrane, nothing blended (F-P25-16). The ear's
colour is the maker's (``put``, RD-P25-18), but ``ears`` first brings the picture's own ear onto hm08's
pad through the profile camera (RD-P25-17), so no ghost of it is left on the head round the ear. Everything is written under
``<dir>`` (git-ignored ``library/parity/P25_*``). MediaPipe (Apache-2.0) and SciPy ride ``--with``; the
project gains no dependency (§The reuse check).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))

N = 8192
VIEWS = REPO / "library" / "parity" / "P25_Views"          # project_views.py's front render and its geometry
RENDER, GEOM = VIEWS / "in_f000_base.png", VIEWS / "geom_f000.npz"
LANDMARKER = REPO / "library" / "parity" / "P25_Face" / "face_landmarker.task"
LANDMARKER_URL = ("https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/"
                  "face_landmarker.task")
LANDMARKER_SHA256 = "64184e229b263107bc2b804c6625db1341ff2bb731874b0bcc2fe6544e0bc9ff"
SUBJECT_MAP = REPO / "MatterLibrary/textures/fit/makehuman/skin/SkinTone34_basecolor_sUKN.png"
HELD = (0.6437, 0.3454, 0.2526)                             # gen_synth_skin.SUBJECTS["Tone34"]["held"]
SOURCE_ROWS, SOURCE_COL0 = 7150, 5100                       # the head island's part of the head region
# The target's words (F-P25-7; the lead on its picture: "so much LIFE, a glow, amazing detail, a softness").
PROMPT = ("A flat unwrapped UV texture map of a real human head's skin, from a photogrammetry scan of "
          "a real young woman about twenty, light warm skin between Fitzpatrick III and IV, shaved bald head, no eyebrow hair, no makeup. "
          "The face is laid out flat in the centre with the closed eyes, nose and lips, the scalp and the back of the head unrolled to each side, "
          "the ears as flat patches. Albedo only: even, shadowless, delit, no lighting, no highlights. "
          "Real unretouched skin: visible pores, fine vellus hair, small blemishes, tiny moles, faint freckles, uneven tone, "
          "slight redness around the nose and on the cheeks. Not a 3D render, not CGI, not painted.")
# hm08's eye contours in MediaPipe's numbering: upper lid, lower lid, the two corners
EYES = {"R": dict(up=[246, 161, 160, 159, 158, 157, 173], lo=[7, 163, 144, 145, 153, 154, 155], c=[33, 133]),
        "L": dict(up=[466, 388, 387, 386, 385, 384, 398], lo=[249, 390, 373, 374, 380, 381, 382], c=[263, 362])}


def _np():
    import numpy as np  # noqa: PLC0415  (``paint`` runs on the standard library alone)
    return np


def _img():
    from PIL import Image  # noqa: PLC0415
    Image.MAX_IMAGE_PIXELS = None
    return Image


def lin(s):
    np = _np()
    return np.where(s <= 0.04045, s / 12.92, ((s + 0.055) / 1.055) ** 2.4)


def srgb(x):
    np = _np()
    x = np.clip(x, 0, 1)
    return np.where(x <= 0.0031308, x * 12.92, 1.055 * x ** (1 / 2.4) - 0.055)


def to_frame(F: dict, rows, cols):
    """Atlas (row, col) → an upright frame's (x, y) (``ROTATE_270``: the head's top up)."""
    y0, y1, x0, x1 = F["bbox"]
    W, H = F["size"]
    return (y1 - rows - 0.5) * W / (y1 - y0) - 0.5, (cols - x0 + 0.5) * H / (x1 - x0) - 0.5


def from_frame(F: dict, x, y):
    y0, y1, x0, x1 = F["bbox"]
    W, H = F["size"]
    return y1 - 0.5 - (x + 0.5) * (y1 - y0) / W, x0 - 0.5 + (y + 0.5) * (x1 - x0) / H


# ------------------------------------------------------------------ source -----------------------
def cmd_source(d: Path, width: int) -> None:
    """The subject's head island, held at its face-core tone and stood upright at the model's size: the
    source the target picture was painted from (``src.png``, its frame ``src_frame.json``). At 0.9 Krea
    draws from the words alone (25.1.10), but the source sets the picture's size."""
    np, Image = _np(), _img()
    d.mkdir(parents=True, exist_ok=True)
    z = np.load(VIEWS / f"head_fields_{N}.npz")
    idx, face = z["idx"], z["face"]
    r, c = np.divmod(idx, N)
    keep = (c >= SOURCE_COL0) & (r < SOURCE_ROWS)
    idx, face = idx[keep], face[keep]
    C = np.asarray(Image.open(SUBJECT_MAP)).reshape(-1, 3) / 255.0
    Cl = lin(C[idx])
    k = np.array(HELD) / Cl[face > 0.9].mean(0)
    ys, xs = np.divmod(idx, N)
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    img = np.empty((y1 - y0, x1 - x0, 3))
    img[:] = (Cl * k).mean(0)
    img[ys - y0, xs - x0] = Cl * k
    pic = Image.fromarray((srgb(img) * 255 + 0.5).astype(np.uint8)).transpose(Image.Transpose.ROTATE_270)
    w, h = pic.size
    hgt = int(round(h * width / w / 16)) * 16
    pic.resize((width, hgt), Image.LANCZOS).save(d / "src.png")
    F = {"bbox": [int(y0), int(y1), int(x0), int(x1)], "rotate": "ROTATE_270", "size": [width, hgt], "scale": k.tolist()}
    (d / "src_frame.json").write_text(json.dumps(F, indent=1) + "\n")
    print(f"src.png: {width} x {hgt}, island rows {y0}-{y1}, cols {x0}-{x1}")


# ------------------------------------------------------------------ paint (standard library) ----
def cmd_paint(d: Path, seeds: list, strength: float, server: str) -> None:
    import gen_views_model as g  # noqa: PLC0415
    graph = json.loads(g.WORKFLOWS["krea"].read_text(encoding="utf-8"))
    version = json.loads(g._call(server, "/system_stats"))["system"]["comfyui_version"]
    models = {n["class_type"]: n["inputs"].get("unet_name") or n["inputs"].get("clip_name") or n["inputs"].get("vae_name")
              for n in graph.values() if n["class_type"] in ("UNETLoader", "CLIPLoader", "VAELoader")}
    src = g.upload(server, d / "src.png")
    for sd in seeds:
        t = time.time()
        vals = {"IMAGE": src, "PROMPT": PROMPT, "SEED": sd, "STEPS": 8, "STRENGTH": strength, "PREFIX": "matter_p25face"}
        png, pid = g.run(server, g.fill(graph, vals))
        name = f"face_s{round(strength * 100):02d}_seed{sd}"
        (d / f"{name}.png").write_bytes(png)
        rec = {"model": "krea", "workflow": g.WORKFLOWS["krea"].name, "files": models, "comfyui": version, "seed": sd,
               "steps": 8, "strength": strength, "source": "src.png",
               "source_sha256": hashlib.sha256((d / "src.png").read_bytes()).hexdigest(),
               "prompt": PROMPT, "prompt_id": pid, "seconds": round(time.time() - t, 1)}
        (d / f"{name}.json").write_text(json.dumps(rec, indent=1) + "\n")
        print(f"{name}: {rec['seconds']} s", flush=True)


# ------------------------------------------------------------------ landmarks --------------------
def landmarker(path: Path = LANDMARKER) -> Path:
    """MediaPipe's face-landmarker model, fetched once into the git-ignored parity folder, its sha256 checked."""
    if not path.is_file():
        path.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(LANDMARKER_URL, timeout=120) as r:
            data = r.read()
        if hashlib.sha256(data).hexdigest() != LANDMARKER_SHA256:
            raise SystemExit("the face-landmarker download does not match its pinned sha256; not kept")
        path.write_bytes(data)
    if hashlib.sha256(path.read_bytes()).hexdigest() != LANDMARKER_SHA256:
        raise SystemExit(f"{path}: sha256 is not the pinned one")
    return path


def detect(picture: Path):
    """The (478, 2) pixel landmarks of the largest face in ``picture``."""
    np, Image = _np(), _img()
    import mediapipe as mp  # noqa: PLC0415
    from mediapipe.tasks import python as mpt  # noqa: PLC0415
    from mediapipe.tasks.python import vision  # noqa: PLC0415
    opt = vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=str(landmarker())), num_faces=2,
                                       min_face_detection_confidence=0.2, min_face_presence_confidence=0.2)
    det = vision.FaceLandmarker.create_from_options(opt)
    im = Image.open(picture).convert("RGB")
    w, h = im.size
    r = det.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=np.asarray(im).copy()))
    if not r.face_landmarks:
        raise SystemExit(f"{picture.name}: no face found")
    fs = [np.array([[q.x * w, q.y * h] for q in f]) for f in r.face_landmarks]
    return max(fs, key=lambda f: np.ptp(f[:, 0]) * np.ptp(f[:, 1])), im


def _overlay(im, pts, out: Path, col=(0, 255, 0)) -> None:
    from PIL import ImageDraw  # noqa: PLC0415
    im = im.copy()
    dr = ImageDraw.Draw(im)
    for x, y in pts:
        dr.ellipse((x - 2, y - 2, x + 2, y + 2), fill=col)
    im.save(out, quality=90)


def snap_eyes(L):
    """hm08's eye-contour landmarks moved onto the eye opening's edge, found from the render's depth: the
    upper points to its top edge, the lower to its bottom, the corners to its ends, each keeping its
    relative place between the corners (F-P25-25). Returns the snapped array and the moves (px)."""
    np = _np()
    from scipy import ndimage as ndi  # noqa: PLC0415
    g = np.load(GEOM)
    Z, mask = g["z"], g["mask"]
    L0, L = L, L.copy()
    moves = {}
    for side, E in EYES.items():
        ids = E["up"] + E["lo"] + E["c"]
        p = L0[ids]
        x0, y0 = int(p[:, 0].min()) - 40, int(p[:, 1].min()) - 40
        x1, y1 = int(p[:, 0].max()) + 40, int(p[:, 1].max()) + 40
        z, mk = Z[y0:y1, x0:x1], mask[y0:y1, x0:x1]
        ring = np.percentile(z[mk], 50)                            # the lids' depth: the box is mostly lid
        lab, _ = ndi.label(~mk | (np.abs(z - ring) > 0.006))       # the opening: far behind the lids, or empty
        cy, cx = int(np.mean(p[:, 1]) - y0), int(np.mean(p[:, 0]) - x0)
        k = lab[cy, cx]
        if k == 0:
            near = ndi.distance_transform_edt(lab == 0, return_indices=True)[1]
            k = lab[near[0][cy, cx], near[1][cy, cx]]
        ys, xs = np.nonzero(ndi.binary_fill_holes(lab == k))
        cols = {xx: (ys[xs == xx].min() - 0.5, ys[xs == xx].max() + 0.5) for xx in np.unique(xs)}
        xmin, xmax = xs.min(), xs.max()
        co = L0[E["c"], 0] - x0
        lo_c, hi_c = co.min(), co.max()
        for which, group in ((0, E["up"]), (1, E["lo"])):
            for i in group:
                t = np.clip((L0[i, 0] - x0 - lo_c) / (hi_c - lo_c), 0.04, 0.96)
                x = xmin + t * (xmax - xmin)
                L[i] = [x + x0, cols[int(round(x))][which] + y0]
        for i in E["c"]:
            xe = xmin if abs(L[i, 0] - x0 - xmin) < abs(L[i, 0] - x0 - xmax) else xmax
            L[i] = [xe + x0 - (0.5 if xe == xmin else -0.5), ys[xs == xe].mean() + y0]
        moves[side] = np.abs(L[ids] - L0[ids]).max(0).round(1).tolist()
    return L, moves


AXIS = 1023.5      # hm08's front render is a mirror about this column (its eye openings sum to 2047, F-P25-25)


def mirror_pairs():
    """Each of MediaPipe's 478 landmarks paired with its mirror image, from the canonical face mesh inside the
    landmarker bundle (468 vertices, x y z u v each; symmetric by construction); the irises (468-472 and
    473-477) by their order. A midline point pairs with itself."""
    np = _np()
    import struct  # noqa: PLC0415
    import zipfile  # noqa: PLC0415
    b = zipfile.ZipFile(landmarker()).read("geometry_pipeline_metadata_landmarks.binarypb")

    def varint(i):
        v = s = 0
        while True:
            c = b[i]; i += 1; v |= (c & 127) << s; s += 7
            if c < 128:
                return v, i
    _, i = varint(0)                      # the canonical mesh: the first field
    n, i = varint(i)
    end, fl = i + n, []
    while i < end:
        k, i = varint(i)
        f, t = k >> 3, k & 7
        if t == 5:
            if f == 3:                    # the vertex buffer, one float a field
                fl.append(struct.unpack("<f", b[i:i + 4])[0])
            i += 4
        elif t == 0:
            _, i = varint(i)
        elif t == 2:
            ln, i = varint(i); i += ln
        else:
            i += 8
    V = np.array(fl).reshape(468, 5)[:, :3]
    if len(fl) != 2340:
        raise SystemExit("the canonical face mesh is not the expected 468 vertices")
    M = V * [-1, 1, 1]
    pair = np.argmin(((V[:, None] - M[None]) ** 2).sum(-1), axis=1)
    if not (pair[pair] == np.arange(468)).all():
        raise SystemExit("the canonical mesh's mirror pairing is not one-to-one")
    return np.r_[pair, [473, 474, 475, 476, 477, 468, 469, 470, 471, 472]]


def symmetric(L):
    """hm08's landmarks made mirror-symmetric about ``AXIS``. MediaPipe's fit on the render sits 10-17 px low
    on the image-right around the brow, above and below the eye and on the cheek (25.1.17; the lead at
    click 1: "left eyebrow (the one on the right) not in the correct position (map is too low) and that is
    the same for the eye area"). The fit is also shifted and rolled sideways (its midline at 1030-1036 in the upper face, 1022 at the
    chin; the render's silhouette is centred on ``AXIS`` on every row), so across, each pair is averaged about
    ``AXIS`` and the midline put on it; in height the image-left side is kept, the side the lead read right."""
    np = _np()
    pair = mirror_pairs()
    S = L.copy()
    iris = np.arange(len(L)) >= 468             # inside the empty eye opening, under closed lids: left as found
    mid = (pair == np.arange(len(L))) & ~iris
    S[mid, 0] = AXIS
    left = np.flatnonzero(~mid & ~iris & (L[:, 0] < L[pair, 0]))
    r = pair[left]
    x = (L[left, 0] + 2 * AXIS - L[r, 0]) / 2
    S[left, 0], S[r, 0], S[r, 1] = x, 2 * AXIS - x, L[left, 1]
    return S


def cmd_landmarks(d: Path, picture: Path | None) -> None:
    np = _np()
    if picture is None:                                            # hm08's front render, the eyes snapped
        raw, im = detect(RENDER)
        E, moves = snap_eyes(raw)
        L = symmetric(E)
        np.save(d / "lm_hm08_raw.npy", raw)
        np.save(d / "lm_hm08_eyes.npy", E)
        np.save(d / "lm_hm08.npy", L)
        _overlay(im, L, d / "lm_hm08_overlay.jpg")
        mv = np.abs(L - E)
        print(f"lm_hm08.npy: 478 points on hm08's front render; eye points snapped to the openings, moved up to {moves} px; "
              f"the image-right side mirrored from the left: moved up to {mv.max(0).round(1).tolist()} px, the snapped eye "
              f"contour by at most {mv[sum((e['up'] + e['lo'] + e['c'] for e in EYES.values()), [])].max():.1f} px")
        return
    L, im = detect(picture)
    np.save(d / f"lm_{picture.stem}.npy", L)
    _overlay(im, L, d / f"lm_{picture.stem}_overlay.jpg")
    print(f"lm_{picture.stem}.npy: 478 points, face span {L.min(0).round().tolist()} - {L.max(0).round().tolist()}")


# ------------------------------------------------------------------ field ------------------------
def _pushpull(img, kn):
    np = _np()
    if kn.all() or min(img.shape[:2]) < 2:
        return img
    h, w = img.shape[:2]
    H2, W2, c = (h + 1) // 2, (w + 1) // 2, img.shape[2]
    pi = np.zeros((H2 * 2, W2 * 2, c)); pk = np.zeros((H2 * 2, W2 * 2))
    pi[:h, :w] = img * kn[..., None]; pk[:h, :w] = kn
    si = pi.reshape(H2, 2, W2, 2, c).sum((1, 3)); sk = pk.reshape(H2, 2, W2, 2).sum((1, 3))
    low = _pushpull(np.where(sk[..., None] > 0, si / np.maximum(sk, 1e-9)[..., None], 0), sk > 0)
    up = np.repeat(np.repeat(low, 2, 0), 2, 1)[:h, :w]
    return np.where(kn[..., None], img, up)


def cmd_field(d: Path, picture: Path, min_nz: float, ears: Path | None = None, steps: int = 4000) -> None:
    """One mapping from the picture onto ``paint_uv``'s island frame (``uv_frame.json``). Inside the face
    the front projection; its displacement from the picture's own layout held there, and relaxed
    harmonically (``steps`` Jacobi steps on an 8× coarser grid) toward the island's border, held at zero.
    Without ``ears`` the ear pads are held at zero too: the first pass, ``first_<stem>.png``, which ``ears``
    reads. With ``ears`` (``ears_<stem>.json``) each ear's fit is held like the face: ``face_<stem>.png``,
    for ``paint_uv.py put``. Colour is sampled once."""
    np, Image = _np(), _img()
    from scipy.ndimage import binary_dilation, distance_transform_edt, map_coordinates, zoom  # noqa: PLC0415
    from scipy.spatial import Delaunay  # noqa: PLC0415
    PF = json.loads((d / "src_frame.json").read_text())
    OF = json.loads((d / "uv_frame.json").read_text())
    P = np.asarray(Image.open(picture).convert("RGB"), np.float64)
    if [P.shape[1], P.shape[0]] != PF["size"]:
        raise SystemExit(f"{picture.name} is {P.shape[1]} x {P.shape[0]}, the source frame {PF['size']}")
    W, H = OF["size"]
    gy, gx = np.mgrid[0:H, 0:W].astype(np.float64)
    ix, iy = to_frame(PF, *from_frame(OF, gx, gy))                # the picture's own layout at each out pixel
    Lp, Lr = np.load(d / f"lm_{picture.stem}.npy"), np.load(d / "lm_hm08.npy")
    g = np.load(GEOM)
    uv, mask, n = g["uv"], g["mask"], g["n"]
    tri = Delaunay(Lr)
    ys, xs = np.nonzero(mask)
    pts = np.stack([xs + 0.5, ys + 0.5], 1)
    s = tri.find_simplex(pts)
    ok = s >= 0
    T = tri.transform[s[ok]]
    b2 = np.einsum("nij,nj->ni", T[:, :2], pts[ok] - T[:, 2])
    bary = np.c_[b2, 1 - b2.sum(1)]
    src = np.einsum("ni,nij->nj", bary, Lp[tri.simplices[s[ok]]])  # render pixel → picture point
    yy, xx = ys[ok], xs[ok]
    w = np.clip((np.abs(n[yy, xx, 2]) - min_nz) / 0.15, 0, 1)     # how squarely the surface faces the camera
    ox, oy = to_frame(OF, uv[yy, xx, 1] * N, uv[yy, xx, 0] * N)
    jx, jy = np.round(ox).astype(int), np.round(oy).astype(int)
    k = (jx >= 0) & (jx < W) & (jy >= 0) & (jy < H) & (w > 0)
    acc = np.zeros((H, W, 2)); wt = np.zeros((H, W))
    np.add.at(acc, (jy[k], jx[k]), src[k] * w[k, None]); np.add.at(wt, (jy[k], jx[k]), w[k])
    known = wt > 0.05
    D = np.zeros((H, W, 2))
    D[known] = acc[known] / wt[known, None] - np.stack([ix[known], iy[known]], 1)
    zero = np.zeros((H, W), bool)
    zero[:4] = zero[-4:] = True
    zero[:, :4] = zero[:, -4:] = True
    EJ = json.loads(ears.read_text()) if ears else {}
    for e in ("ear_r", "ear_l"):
        if e in EJ:                                                 # the ear's fit, held like the face
            pj = np.load(d / EJ[e]["proj"])
            qx, qy = to_frame(PF, *from_frame(OF, pj["ox"], pj["oy"]))
            D[pj["py"], pj["px"]] = np.stack([qx - ix[pj["py"], pj["px"]], qy - iy[pj["py"], pj["px"]]], -1)
            known[pj["py"], pj["px"]] = True
            continue
        f = OF["features"][e]
        hw, hh = (f["x1"] - f["x0"]) * 0.75, (f["y1"] - f["y0"]) * 0.75
        zero[int(f["cy"] - hh):int(f["cy"] + hh), int(f["cx"] - hw):int(f["cx"] + hw)] = True
    zero &= ~binary_dilation(known, iterations=20)
    q = 8
    h8, w8 = (H + q - 1) // q, (W + q - 1) // q

    def coarse(a, m):
        pa = np.zeros((h8 * q, w8 * q, 2)); pm = np.zeros((h8 * q, w8 * q))
        pa[:H, :W] = a * m[..., None]; pm[:H, :W] = m
        sa = pa.reshape(h8, q, w8, q, 2).sum((1, 3)); sm = pm.reshape(h8, q, w8, q).sum((1, 3))
        return sa / np.maximum(sm, 1e-9)[..., None], sm > q * q * 0.3
    cD, cK = coarse(D, known)
    cZD, cZ = coarse(D, zero)
    fixed = cK | cZ
    val = np.where(cK[..., None], cD, np.where(cZ[..., None], cZD, 0.0))
    Dc = _pushpull(val, fixed)
    for _ in range(steps):
        av = (np.roll(Dc, 1, 0) + np.roll(Dc, -1, 0) + np.roll(Dc, 1, 1) + np.roll(Dc, -1, 1)) / 4
        Dc = np.where(fixed[..., None], val, av)
    Dup = zoom(Dc, (q, q, 1), order=1)[:H, :W]
    a = np.clip(1 - distance_transform_edt(~known) / 12.0, 0, 1)[..., None]   # a 12 px ramp off the face's edge
    Df = np.where(known[..., None], D, a * _pushpull(D, known) + (1 - a) * Dup)
    sx, sy = ix + Df[..., 0], iy + Df[..., 1]
    out = np.stack([map_coordinates(P[..., c], [sy, sx], order=1, mode="nearest") for c in range(3)], -1)
    name = f"{'face' if ears else 'first'}_{picture.stem}.png"
    Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(d / name)
    det = np.gradient(sx, axis=1) * np.gradient(sy, axis=0) - np.gradient(sx, axis=0) * np.gradient(sy, axis=1)
    mm = OF["mm_per_px"]
    rec = {"picture": picture.name, "min_nz": min_nz, "steps": steps, "ears": ears.name if ears else None, "landmarks": f"lm_{picture.stem}.npy",
           "render_landmarks": "lm_hm08.npy", "folded_pct": round(float((det <= 0).mean() * 100), 3),
           "folded_face_pct": round(float(((det <= 0) & known).sum() / known.sum() * 100), 2),
           "face_pct_of_island": round(float(known.mean() * 100), 1),
           "face_move_mm_median": round(float(np.median(np.hypot(*D[known].T)) * mm), 1)}
    (d / f"{name[:-4]}.json").write_text(json.dumps(rec, indent=1) + "\n")
    print(f"{name}: folded {rec['folded_pct']} % (face {rec['folded_face_pct']} %); the face {rec['face_pct_of_island']} % "
          f"of the island, moved {rec['face_move_mm_median']} mm (median) from where the model drew it")


# ------------------------------------------------------------------ ears -------------------------
# The ear's colour is the maker's (RD-P25-18), but the picture's own ear must still be brought onto hm08's
# pad: Krea draws it ~1.4x larger and 20-39 mm away (F-P25-16), so a pad held at zero move leaves a ghost
# ear on the head skin round it, and the ear's root level (what the maker's gradient is scaled to) is read
# off the drawn ear's shading (25.1.14). The fit is the profile camera's (RD-P25-17, F-P25-22, F-P25-23):
# hm08's rendered ear fitted onto the drawn ear's silhouette, each visible ear pixel carried to its texel,
# the whole pad and a rim held to that projection's best-fit affine, pushed out past the painted halo.
EAR_VIEWS = (("ear_r", "f-80"), ("ear_l", "f+80"))


def _hull_mask(m, shape):
    np = _np()
    from PIL import Image, ImageDraw  # noqa: PLC0415
    from scipy.spatial import ConvexHull  # noqa: PLC0415
    ys, xs = np.nonzero(m)
    h = ConvexHull(np.stack([xs, ys], 1))
    im = Image.new("L", (shape[1], shape[0]), 0)
    ImageDraw.Draw(im).polygon([(float(xs[i]), float(ys[i])) for i in h.vertices], fill=1)
    return np.asarray(im, bool)


def _drawn_ear(A, F, side):
    """The drawn ear's silhouette in the first pass: the strongest colour gradients after a 4 px blur (pores
    gone), closed and filled, the largest region's convex hull; no colour cue (F-P25-21)."""
    np = _np()
    from scipy.ndimage import binary_closing, binary_dilation, binary_fill_holes, gaussian_filter, label, sobel  # noqa: PLC0415
    W, H = F["size"]
    f = F["features"][side]
    cy, cx = int(f["cy"]), int(f["cx"])
    wy0, wy1 = max(cy - 280, 0), min(cy + 280, H)
    wx0, wx1 = (cx - 340, cx + 260) if side == "ear_r" else (cx - 260, cx + 340)
    wx0, wx1 = max(wx0, 0), min(wx1, W)
    Wn = A[wy0:wy1, wx0:wx1]
    G = sum(np.hypot(sobel(gaussian_filter(Wn[..., k], 4), 0), sobel(gaussian_filter(Wn[..., k], 4), 1)) for k in range(3))
    reg = binary_fill_holes(binary_closing(binary_dilation(G > np.percentile(G, 95), iterations=2), iterations=12))
    lab, _ = label(reg)
    sz = np.bincount(lab.ravel())
    sz[0] = 0
    return _hull_mask(lab == sz.argmax(), reg.shape), (wy0, wx0)


def cmd_ears(d: Path, first: Path, pad_rim: int = 12, min_nz: float = 0.05, ease: float = 6.0, back_out: float = 1.3) -> None:
    """``first`` is a ``field`` pass with the pads unmoved; writes ``ears_<stem>.json`` (+ one ``.npz`` per ear)
    for ``field --ears`` and ``ears_<stem>_check.png`` (hm08's ear outline, cyan, on the drawn ear, yellow)."""
    np, Image = _np(), _img()
    from PIL import ImageDraw  # noqa: PLC0415
    from scipy.ndimage import (binary_closing, binary_dilation, binary_erosion, binary_fill_holes,  # noqa: PLC0415
                               distance_transform_edt, gaussian_filter, label)
    from scipy.signal import correlate  # noqa: PLC0415
    F = json.loads((d / "uv_frame.json").read_text())
    y0, y1, x0, x1 = F["bbox"]
    W, H = F["size"]
    A = np.asarray(Image.open(first).convert("RGB"), np.float64) / 255
    Hd = np.load(VIEWS / f"head_fields_{N}.npz")
    earset = np.zeros(N * N, bool)
    earset[Hd["idx"][Hd["ears"] > 0.5]] = True
    _r, _c = np.divmod(Hd["idx"][Hd["ears"] > 0.5], N)
    PJX = np.clip(np.round((y1 - _r - 0.5) * W / (y1 - y0) - 0.5).astype(int), 0, W - 1)
    PJY = np.clip(np.round((_c - x0 + 0.5) * H / (x1 - x0) - 0.5).astype(int), 0, H - 1)
    stem = first.stem.removeprefix("first_")
    res, tiles = {}, []
    for side, view in EAR_VIEWS:
        g = np.load(VIEWS / f"geom_{view}.npz")
        m, uv, n = g["mask"], g["uv"], g["n"]
        rr = np.clip((uv[..., 1] * N).astype(int), 0, N - 1)
        cc = np.clip((uv[..., 0] * N).astype(int), 0, N - 1)
        e = m & earset[rr * N + cc]
        lab, _ = label(e)
        sz = np.bincount(lab.ravel())
        sz[0] = 0
        e = binary_fill_holes(lab == sz.argmax()) & m
        ey, ex = np.nonzero(e)
        c_r = np.array([ey.mean(), ex.mean()])
        eh = _hull_mask(e, e.shape)
        hy, hx = np.nonzero(eh)
        pts = np.stack([hy, hx], 1) - c_r
        drawn, (wy0, wx0) = _drawn_ear(A, F, side)
        s0, nA = np.sqrt(drawn.sum() / eh.sum()), drawn.sum()
        best = [-1.0, None]

        def tryit(s, deg, asp):
            th = np.deg2rad(deg)
            Mf = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]]) @ np.diag([s / np.sqrt(asp), s * np.sqrt(asp)])
            q = pts @ Mf.T
            q0 = np.floor(q.min(0)).astype(int)
            qi = np.round(q - q0).astype(int)
            hh, ww = qi.max(0) + 1
            if hh >= drawn.shape[0] or ww >= drawn.shape[1]:
                return
            K = np.zeros((hh, ww))
            K[qi[:, 0], qi[:, 1]] = 1
            K = binary_closing(K > 0, iterations=1).astype(float)
            ov = correlate(drawn.astype(float), K, mode="valid", method="fft")
            iou = ov / (nA + K.sum() - ov)
            k = np.unravel_index(np.argmax(iou), iou.shape)
            if iou[k] > best[0]:
                best[:] = [float(iou[k]), (s, deg, asp, np.array([wy0 + k[0], wx0 + k[1]]) - q0, Mf)]
        for s in s0 * np.arange(0.8, 1.21, 0.05):
            for deg in range(-24, 25, 4):
                for asp in (0.8, 0.9, 1.0, 1.1, 1.25):
                    tryit(s, deg, asp)
        a0 = best[1]
        for s in a0[0] * np.arange(0.96, 1.041, 0.01):
            for deg in np.arange(a0[1] - 3, a0[1] + 3.1, 1):
                for asp in a0[2] * np.array([0.95, 1.0, 1.05]):
                    tryit(s, deg, asp)
        iou, (s, deg, asp, centre, Mf) = best
        w = np.clip((np.abs(n[ey, ex, 2]) - min_nz) / 0.1, 0, 1)        # the bowl's grazing walls kept
        o = centre + (np.stack([ey, ex], 1) - c_r) @ Mf.T
        X = (y1 - rr[ey, ex] - 0.5) * W / (y1 - y0) - 0.5
        Y = (cc[ey, ex] - x0 + 0.5) * H / (x1 - x0) - 0.5
        acc = np.zeros((H, W, 2)); wt = np.zeros((H, W))
        bx0, by0 = np.floor(X).astype(int), np.floor(Y).astype(int)
        fx_, fy_ = X - bx0, Y - by0
        for ddx, ddy, ww in ((0, 0, (1 - fx_) * (1 - fy_)), (1, 0, fx_ * (1 - fy_)), (0, 1, (1 - fx_) * fy_), (1, 1, fx_ * fy_)):
            jx, jy = bx0 + ddx, by0 + ddy
            wv = w * ww
            k = (wv > 0) & (jx >= 0) & (jx < W) & (jy >= 0) & (jy < H)
            np.add.at(acc, (jy[k], jx[k]), o[k][:, ::-1] * wv[k, None]); np.add.at(wt, (jy[k], jx[k]), wv[k])
        good = wt > 0.05
        O = np.where(good[..., None], acc / np.maximum(wt, 1e-9)[..., None], 0)
        front = gaussian_filter(binary_fill_holes(binary_closing(good, iterations=3)).astype(float), 3.0) > 0.5
        good &= front
        O = _pushpull(O, good)
        for _ in range(300):
            av = (np.roll(O, 1, 0) + np.roll(O, -1, 0) + np.roll(O, 1, 1) + np.roll(O, -1, 1)) / 4
            O = np.where(good[..., None], O, av)
        py, px = np.nonzero(front)
        gy, gx = np.nonzero(good)
        coef, *_ = np.linalg.lstsq(np.c_[gx, gy, np.ones(len(gx))], np.c_[O[gy, gx, 0], O[gy, gx, 1]], rcond=None)
        padm = np.zeros((H, W), bool)
        padm[PJY, PJX] = True
        padm = binary_dilation(binary_closing(padm, iterations=2), iterations=pad_rim) & (np.abs(np.arange(W)[None, :] - F["features"][side]["cx"]) < 200)
        ay, ax = np.nonzero(padm & ~front)
        ec = centre[::-1]
        aff = ec + back_out * (np.c_[ax, ay, np.ones(len(ax))] @ coef - ec)
        if ease > 0:
            wv = np.clip(distance_transform_edt(front)[py, px] / ease, 0, 1)[:, None]
            O[py, px] = wv * O[py, px] + (1 - wv) * (ec + back_out * (np.c_[px, py, np.ones(len(px))] @ coef - ec))
        npz = d / f"ears_{stem}_{side}.npz"
        np.savez_compressed(npz, px=np.r_[px, ax], py=np.r_[py, ay], ox=np.r_[O[py, px, 0], aff[:, 0]], oy=np.r_[O[py, px, 1], aff[:, 1]])
        res[side] = {"proj": npz.name, "iou": round(iou, 3), "s": round(float(s), 3), "rot": float(deg), "aspect": round(float(asp), 3)}
        print(f"{side}: overlap (IoU) {iou:.3f}; render -> island x{s:.3f}, wider x{asp:.2f}, turn {deg:+.1f} deg")
        bnd = e & binary_dilation(~e, iterations=1)
        q = centre + (np.stack(np.nonzero(bnd), 1) - c_r) @ Mf.T
        dyy, dxx = np.nonzero(drawn & ~binary_erosion(drawn, iterations=1))
        cy, cx = centre.astype(int)
        im = Image.fromarray((A[cy - 160:cy + 160, cx - 160:cx + 160] * 255).astype(np.uint8)).resize((640, 640), Image.LANCZOS)
        dr = ImageDraw.Draw(im)
        for yy, xx in zip(dyy + wy0, dxx + wx0):
            dr.point(((xx - cx + 160) * 2, (yy - cy + 160) * 2), fill=(255, 220, 0))
        for yy, xx in q:
            dr.point(((xx - cx + 160) * 2, (yy - cy + 160) * 2), fill=(0, 255, 255))
        tiles.append(im)
    (d / f"ears_{stem}.json").write_text(json.dumps(res, indent=1) + "\n")
    chk = Image.new("RGB", (1290, 640), (40, 40, 40))
    chk.paste(tiles[0], (0, 0)); chk.paste(tiles[1], (650, 0))
    chk.save(d / f"ears_{stem}_check.png")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("source"); s.add_argument("dir", type=Path); s.add_argument("--width", type=int, default=2048)
    s = sub.add_parser("paint"); s.add_argument("dir", type=Path); s.add_argument("--seeds", default="7")
    s.add_argument("--strength", type=float, default=0.9); s.add_argument("--server", default="http://127.0.0.1:8188")
    s = sub.add_parser("landmarks"); s.add_argument("dir", type=Path); s.add_argument("picture", nargs="?")
    s.add_argument("--render", action="store_true", help="hm08's front render, the eye points snapped")
    s = sub.add_parser("field"); s.add_argument("dir", type=Path); s.add_argument("picture")
    s.add_argument("--min-nz", type=float, default=0.08,
                   help="the projection down to this normal z (0.3 for a seed whose cheek streaks, F-P25-17)")
    s.add_argument("--ears", help="ears_<stem>.json from `ears`: the second pass")
    s = sub.add_parser("ears"); s.add_argument("dir", type=Path); s.add_argument("first", help="first_<stem>.png")
    a = ap.parse_args(argv)
    if a.cmd == "source":
        cmd_source(a.dir, a.width)
    elif a.cmd == "paint":
        cmd_paint(a.dir, [int(x) for x in a.seeds.split(",")], a.strength, a.server)
    elif a.cmd == "landmarks":
        if a.render == bool(a.picture):
            raise SystemExit("give a picture, or --render (not both)")
        cmd_landmarks(a.dir, None if a.render else a.dir / a.picture)
    elif a.cmd == "ears":
        cmd_ears(a.dir, a.dir / a.first)
    else:
        cmd_field(a.dir, a.dir / a.picture, a.min_nz, a.dir / a.ears if a.ears else None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
