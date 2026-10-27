#!/usr/bin/env python3
"""The library's PIGMENT skin maker for MakeHuman_Body_v01 (hm08), and its marks-layer test drafts.

    uv run tools/converters/fit/gen_skin_maps.py                                  # the library's six maps (this compose)
    uv run --with scipy tools/converters/fit/gen_synth_skin.py                    # the layer drafts (II, IV, VI)
    uv run --with scipy tools/converters/fit/gen_synth_skin.py IV --detail SynthVeins
    uv run --with scipy tools/converters/fit/gen_synth_skin.py --out /tmp/synth  # a trial, nothing in the library

**Phase23 (RD-P23-2): ``compose`` with no layers is the library's skin colour.** ``gen_skin_maps.py``
calls it for the six ``Skin_Fitzpatrick*`` maps and keeps the calibration, ``--picture`` and the
provenance. That path needs only the project's environment; ``--with scipy`` is for the marks
layers alone (their point processes use its k-d tree, RD-P23-7). The base's skin-scale detail is
raised to the bar's strength on the face and about 60 % of it on the body (``DETAIL``; click 1, the
lead: *"we need some sort of texture on the hands and rest of the body"*). The model holds only at
III and IV (23.2.1), so each tone takes the nearer one's response (``Lut``). The plain ``Synth``
drafts were retired at 23.2 (RD-P23-8); the twelve layer drafts were made before it, on the
spike's base, and are *Skin Layers*' references. Re-running this command remakes them on today's.

**What this is.** The lead's spike (2026-10-26; OMF research `261026_R_SyntheticSkinAndEyeSets`,
"1) yes 2) yes 3) yes - run the spike … add these tests directly to the Matter Library"). Each map is
a DRAFT test article's own ``base_color_map`` beside the six shipped ``Skin_Fitzpatrick*`` maps,
which it never touches. Colour only, because colour is all the contract carries today
(``docs/specs/Authoring/SkinMaps.md``; *Skin Maps Beyond Colour* is the next step).

**How the colour is made — chromophores, not paint.** Skin colour is two pigments: melanin
(epidermis) and blood (dermis). Every texel gets a melanin and a blood amount, and the colour comes
from a forward model of light in skin, so ONE structure gives each tone its own regional colour:
lips and cheeks redden on light skin and barely on dark, freckles show on fair skin and fade on dark
(today's six maps are one picture, F-P21-10). The model is the Open Morphology Foundation's
two-chromophore model, tabulated in ``synth/chromophore_lut.json`` (melanin x blood x oxygen
saturation -> linear albedo; its header names the model version and commit). Its gamut does not
reach the lightest and darkest tones, so it drives only the RELATIVE change around each tone; the
library's own calibration (``gen_skin_maps.calibrate``) still holds the average to the measured tone.
The lips keep the library's lip rule (``LIP_RULE``), since the model's lips run lilac.

**Where things go — 3D, not UV.** Every texel's 3D position and normal are rasterised from the mesh
(no Blender: ``rasterise``), so all noise is seamless across UV seams and every feature is placed on
the body: the sun-exposed face, neck, hands and forearms are darker than the covered trunk, palms
and soles are near-amelanotic, cheeks, nose, ears, fingertips and knuckles are redder, creases are
darker (mesh concavity, no light baked in).

**The layers** (``DETAILS``), each the base plus one kind of mark, so a viewer can switch them in
Studio's material window: ``Synth`` (the base), ``SynthFreckles`` (clustered freckles on the face,
shoulders, upper back and forearms: added melanin), ``SynthVeins`` (veins grown over the inner
forearms, the backs of the hands and feet, the temples, the chest: deoxygenated blood under the
skin), ``SynthMarks`` (moles, acne, post-acne marks and a flushed nose and cheeks), ``SynthAll``.

**Sources.** CC0 parts only and no photograph (RD-SKM-2): MPFB2's region masks and hm08 (pinned in
``build_character.SOURCES``), the tabulated model, seeded procedural noise and point processes. No AI.
Statistics the generators follow: freckles as a clustered point process with a density map and a
size distribution (Schneider, Egger & Vetter, FG 2018); nevi densest on the arms and back (body-site
nevus studies); veins visible where skin is thin over them. Their numbers here are judgement, not
fitted.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(REPO / "tools" / "parity" / "scene"))
sys.path.insert(0, str(HERE))
import build_character as bc  # noqa: E402
import gen_skin_maps as gsm  # noqa: E402
import make_kits  # noqa: E402

MESH = gsm.MESH
N = gsm.N
TONES = gsm.TONES                       # Phase23: the library's maker, all six tones
DRAFT_TONES = ("II", "IV", "VI")        # the layer drafts' spread (the 2026-10-26 spike)
DETAILS = ("SynthFreckles", "SynthVeins", "SynthMarks", "SynthAll")   # the plain "Synth" retired (RD-P23-8)
LAYERS = {"Synth": (), "SynthFreckles": ("freckles",), "SynthVeins": ("veins",),
          "SynthMarks": ("marks",), "SynthAll": ("freckles", "veins", "marks")}
OUT = gsm.OUT
TAG = gsm.TAG
PROVENANCE = REPO / "library" / "provenance" / "sources" / "fit" / "makehuman" / "synth_skin.yaml"
LUT_PATH = HERE / "synth" / "chromophore_lut.json"
BLOOD0 = 0.02            # the dermal blood prior: each tone's melanin is solved with blood held here
EPS = 0.01               # softens the ratio where a channel is near 0 (blue on dark skin)
SEED = 20261026
# The base detail, per fit (23.2.2; click 1, the bar). Gains over the spike's: ``fine`` on the 1-2.5 mm
# noise, ``coarse`` on the 7-25 mm noise (kept near the spike's: strong coarse noise reads blotchy),
# ``dots`` a sparse ~1 mm pigment fleck (the bar's fine detail is discrete flecks on a smooth base),
# each on the face and the body, and ``flush`` the cheeks' and nose's blood. The IV fit's operating
# melanin is 4x the III fit's, so a melanin modulation reads ~2.7x stronger there: its melanin gains
# are cut by that, and its flush is the spike's, so redness falls from the light tones to the dark.
DETAIL = {"III": {"fine": (3.0, 2.0), "coarse": (1.3, 1.0), "dots": (0.9, 0.5), "flush": 1.8},
          "IV": {"fine": (1.1, 0.75), "coarse": (0.5, 0.4), "dots": (0.33, 0.18), "flush": 1.0}}
# The face's PLACED regional colour (23.2.7; click 2, the lead: "We are certainly not at the "bar (c),
# III" level"). Each region is a smooth shape placed from the head's own landmarks (``face_regions``)
# and carries one pigment change: log melanin, log blood, oxygen saturation, and depth (blood seen
# through thin skin, which takes each channel by its own scatter reach: red most, so it reads
# violet). The numbers were solved once on III's fit so each region's colour over the trunk matches
# the bar's same region (the bar is a research reference, never shipped: RD-P23-10; a handful of
# region averages are taken from it, as a tone is, and no picture). The regions and their shapes are
# one structure for every tone; the numbers are per fit, as ``DETAIL``'s are. III's fit is solved to
# the bar's region colours over the trunk; IV's to the same colours at half their log contrast (no
# dark-skin reference exists: the agent's judgement, for the lead's eye at IV and V). Measured on the
# atlas, 2026-10-27: every region within 0.13 (III) and 0.02 (IV) in log of its target. The bar's face
# is lighter and cooler than its trunk (pink, where today's face was a darker tan from sun melanin).
# On III's fit that needs melanin out (its pheomelanin is the yellow); blood out alone reads cream.
FACE = {  # fit: {region: (dlog melanin, dlog blood, d so2, depth)}
    "III": {"face": (-1.106, -0.368, 0.150, -0.105), "forehead": (-0.108, -0.372, -0.130, -0.250),
            "cheek": (-3.000, -1.105, 0.150, -0.250), "nose": (-3.000, -1.200, 0.150, -0.250),
            "alae": (-1.262, 0.061, 0.150, -0.250), "under_eye": (-3.000, -0.135, 0.150, 0.053),
            "eyelid": (-0.588, 1.200, 0.150, 0.067), "chin": (-1.676, 0.203, 0.150, -0.025)},
    "IV": {"face": (-0.360, -0.040, 0.031, -0.055), "forehead": (-0.001, -0.089, -0.062, -0.121),
           "cheek": (-0.283, -0.185, -0.091, -0.171), "nose": (-0.328, -0.294, -0.148, -0.250),
           "alae": (-0.013, 0.035, 0.038, -0.091), "under_eye": (-0.182, 0.067, 0.082, 0.022),
           "eyelid": (-0.151, 0.607, 0.150, 0.036), "chin": (0.010, 0.133, 0.108, -0.001)},
}
# The lips over the tone, per fit: III's the bar's measured lips over its trunk (pink-mauve, where the
# library's rule, Phase08 8.2, reads brown-red on the new face); IV's keeps the rule.
LIPS = {"III": (0.93, 0.68, 0.93), "IV": gsm.LIP_RULE}


# ------------------------------------------------------------------ the model -------------------
class Lut:
    """The tabulated model, one table per FIT (Phase23 23.2.1, RD-P23-3 as the lead amended it,
    "Borrow the response"): OMF's model holds only at III and IV, so each tone uses the fit of the
    nearest of them (I, II from III; V, VI from IV) at that fit tone's own melanin, and so takes its
    RELATIVE response; the calibration still holds each tone's own average."""

    def __init__(self, path: Path = LUT_PATH):
        d = json.loads(path.read_text())
        self.meta = {k: d[k] for k in ("model", "omf_commit")}
        self.fits = d["fits"]                      # fit -> {eumelanin_ratio, epidermis_thickness_mm}
        self.tones = d["tones"]                    # tone -> {fit, melanin, matched_on, ...}
        self.mel = np.log(np.array(d["melanin"]))
        self.bld = np.log(np.array(d["blood"]))
        self.so2 = np.array(d["so2"])
        self.tables = {k: np.array(v) for k, v in d["albedo"].items()}   # fit -> [so2, mel, blood, rgb]
        self.a = None

    def use(self, roman: str) -> float:
        """Select the tone's fit; return its operating melanin."""
        t = self.tones[roman]
        self.a = self.tables[t["fit"]]
        return float(t["melanin"])

    def __call__(self, mel, bld, so2):
        fm = np.interp(np.log(np.maximum(mel, 1e-6)), self.mel, np.arange(len(self.mel)))
        fb = np.interp(np.log(np.maximum(bld, 1e-6)), self.bld, np.arange(len(self.bld)))
        fs = np.interp(so2, self.so2, np.arange(len(self.so2)))
        out = 0
        i0 = np.clip(np.floor(fm).astype(int), 0, len(self.mel) - 2)
        j0 = np.clip(np.floor(fb).astype(int), 0, len(self.bld) - 2)
        k0 = np.clip(np.floor(fs).astype(int), 0, len(self.so2) - 2)
        di, dj, dk = (fm - i0)[..., None], (fb - j0)[..., None], (fs - k0)[..., None]
        for a, wa in ((0, 1 - dk), (1, dk)):
            for b, wb in ((0, 1 - di), (1, di)):
                for c, wc in ((0, 1 - dj), (1, dj)):
                    out = out + wa * wb * wc * self.a[k0 + a, i0 + b, j0 + c]
        return out

    def check(self, roman: str, tone) -> dict:
        """RD-P23-3's printed check: the model's colour at the operating point over the tone (the
        borrowed tones' differ by design; the calibration takes it up)."""
        m0 = self.use(roman)
        c = self(np.array(m0), np.array(BLOOD0), np.array(0.8))
        r = c / np.asarray(tone)
        rb = (c[0] / c[2]) / (tone[0] / tone[2])
        return {"fit": self.tones[roman]["fit"], "melanin0": round(m0, 5), "model_over_tone": np.round(r, 3).tolist(),
                "red_blue_over_tone": round(float(rb), 3),
                "passes": bool(max(np.abs(r - 1).max(), abs(rb - 1)) <= 0.15)}


# ------------------------------------------------------------------ the mesh in 3D --------------
def joints() -> dict:
    """hm08's joint helpers (cubes in base.obj), their centres in metres."""
    V, G, grp = [], {}, None
    for line in bc.source("base.obj").decode("utf-8", "replace").splitlines():
        if line.startswith("v "):
            V.append([float(x) for x in line.split()[1:4]])
        elif line.startswith("g "):
            grp = line.split()[1]
        elif line.startswith("f ") and grp and grp.startswith("joint-"):
            G.setdefault(grp[6:], set()).update(int(t.split("/")[0]) - 1 for t in line.split()[1:])
    V = np.array(V) / 10.0
    return {k: V[sorted(v)].mean(0) for k, v in G.items()}


def rasterise(m: dict):
    """Each texel's 3D position, normal and mesh concavity, from the faces' UVs (barycentric)."""
    P = np.array(m["points"], dtype=np.float64)
    faces = m["faces"]
    vt = np.array(m["vt"], dtype=np.float64)
    vn = np.zeros_like(P)
    nb_sum, nb_cnt = np.zeros_like(P), np.zeros(len(P))
    for f in faces:
        idx = [v for v, _ in f]
        for a in range(len(idx)):
            b, c = idx[a], idx[(a + 1) % len(idx)]
            nb_sum[b] += P[c]; nb_cnt[b] += 1
            nb_sum[c] += P[b]; nb_cnt[c] += 1
        n = np.cross(P[idx[1]] - P[idx[0]], P[idx[2]] - P[idx[0]])
        if len(idx) == 4:
            n = n + np.cross(P[idx[2]] - P[idx[0]], P[idx[3]] - P[idx[0]])
        vn[idx] += n
    vn /= np.maximum(np.linalg.norm(vn, axis=1, keepdims=True), 1e-12)
    lap = nb_sum / np.maximum(nb_cnt, 1)[:, None] - P
    conc = np.einsum("ij,ij->i", lap, vn)               # > 0: the neighbours stand proud (a crease)
    conc = conc / max(np.percentile(np.abs(conc), 99), 1e-9)
    pos = np.zeros((N, N, 3)); nor = np.zeros((N, N, 3)); cv = np.zeros((N, N))
    cover = np.zeros((N, N), bool)
    for f in faces:
        for tri in ((0, 1, 2), (0, 2, 3)) if len(f) == 4 else ((0, 1, 2),):
            vi = [f[t][0] for t in tri]
            uv = np.array([[vt[f[t][1]][0] * N, (1 - vt[f[t][1]][1]) * N] for t in tri])
            x0, y0 = np.floor(uv.min(0)).astype(int)
            x1, y1 = np.ceil(uv.max(0)).astype(int)
            x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, N - 1), min(y1, N - 1)
            if x1 < x0 or y1 < y0:
                continue
            ys, xs = np.mgrid[y0:y1 + 1, x0:x1 + 1]
            px, py = xs + 0.5, ys + 0.5
            (ax, ay), (bx, by), (cx, cy) = uv
            den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
            if abs(den) < 1e-12:
                continue
            w0 = ((by - cy) * (px - cx) + (cx - bx) * (py - cy)) / den
            w1 = ((cy - ay) * (px - cx) + (ax - cx) * (py - cy)) / den
            w2 = 1 - w0 - w1
            ins = (w0 >= -1e-4) & (w1 >= -1e-4) & (w2 >= -1e-4)
            if not ins.any():
                continue
            W = np.stack([w0[ins], w1[ins], w2[ins]], -1)
            yy, xx = ys[ins], xs[ins]
            pos[yy, xx] = W @ P[vi]
            nor[yy, xx] = W @ vn[vi]
            cv[yy, xx] = W @ conc[vi]
            cover[yy, xx] = True
    nor /= np.maximum(np.linalg.norm(nor, axis=-1, keepdims=True), 1e-12)
    return pos, nor, cv, cover


# ------------------------------------------------------------------ fields ----------------------
def fbm(P, scales_m, amps, seed):
    return sum(a * gsm.vnoise(P, s, seed + 101 * i) for i, (s, a) in enumerate(zip(scales_m, amps)))


def seg_dist(P, a, b):
    ab = b - a
    t = np.clip(((P - a) @ ab) / max(ab @ ab, 1e-12), 0, 1)
    return np.linalg.norm(P - (a + t[..., None] * ab), axis=-1), t


def body_parts(P, J):
    """Soft membership of each texel in each body part, by distance to its bone (metres)."""
    S = {}
    def mid(*ks):
        return np.mean([J[k] for k in ks], axis=0)
    up = J["head"] - J["neck"]
    segs = {"head": (J["neck"] + up * 0.45, J["head"] + up * 0.6),
            "neck": (J["neck"] - np.array([0, 0.05, 0]), J["neck"] + up * 0.3),
            "trunk": (J["pelvis"], J["neck"] - (J["neck"] - J["pelvis"]) * 0.08)}
    for s in ("l", "r"):
        segs[f"upperarm_{s}"] = (J[f"{s}-shoulder"], J[f"{s}-elbow"])
        segs[f"forearm_{s}"] = (J[f"{s}-elbow"], J[f"{s}-hand"])
        segs[f"hand_{s}"] = (J[f"{s}-hand"], mid(f"{s}-finger-3-1", f"{s}-finger-3-4"))
        segs[f"thigh_{s}"] = (J[f"{s}-upper-leg"], J[f"{s}-knee"])
        segs[f"shin_{s}"] = (J[f"{s}-knee"], J[f"{s}-ankle"])
        segs[f"foot_{s}"] = (J[f"{s}-ankle"], mid(f"{s}-toe-3-1", f"{s}-toe-3-3"))
    D = {}
    T = {}
    for k, (a, b) in segs.items():
        D[k], T[k] = seg_dist(P, np.asarray(a), np.asarray(b))
    Dm = np.min(np.stack(list(D.values())), axis=0)
    W = {k: np.exp(-(d - Dm) / 0.02) for k, d in D.items()}
    tot = sum(W.values())
    for k in W:
        W[k] = W[k] / tot
    def pair(n):
        return W[f"{n}_l"] + W[f"{n}_r"]
    for n in ("upperarm", "forearm", "hand", "thigh", "shin", "foot"):
        S[n] = pair(n)
        S[n + "_t"] = np.where(W[f"{n}_l"] > W[f"{n}_r"], T[f"{n}_l"], T[f"{n}_r"])
    S["head"], S["neck"], S["trunk"] = W["head"], W["neck"], W["trunk"]
    return S


def gauss3(P, c, r):
    return np.exp(-(np.linalg.norm(P - np.asarray(c), axis=-1) / r) ** 2)


def ellipse3(P, c, r):
    """A soft ellipsoid: ``r`` is the (x, y, z) radius in metres."""
    return np.exp(-(((P - np.asarray(c)) / np.asarray(r)) ** 2).sum(-1))


def face_landmarks(P, masks, cover) -> dict:
    """The head's landmarks, from the mesh and MPFB's masks: the nose tip (the face's most forward
    texel), the face's midline, each eye (its eyelid mask's centre) and the mouth."""
    Fp = P[(masks["face"] > 0.5) & cover]
    nose = Fp[np.argmax(Fp[:, 2])]
    fx = Fp[:, 0].mean()
    lid = P[(masks["eyelids"] > 0.5) & cover]
    eyes = (lid[lid[:, 0] < fx].mean(0), lid[lid[:, 0] >= fx].mean(0))
    mouth = P[(masks["lips"] > 0.5) & cover].mean(0)

    def on_face(x, y):
        near = Fp[(np.abs(Fp[:, 0] - x) < 0.005) & (np.abs(Fp[:, 1] - y) < 0.005)]
        return np.array([x, y, near[:, 2].max() if len(near) else nose[2] - 0.03])
    return {"Fp": Fp, "nose": nose, "fx": fx, "eyes": eyes, "mouth": mouth, "on_face": on_face}


def face_regions(P, masks, cover, head=None) -> dict:
    """Each FACE region's soft weight (0..1), placed from the landmarks (23.2.7). The face's own level
    reaches over the whole head (``head``, the body part) and fades into the neck, so it does not stop
    at MPFB's face mask short of the hairline (a tan strip under the hair, seen at the look view)."""
    L = face_landmarks(P, masks, cover)
    n, fx, (el, er), mo, at = L["nose"], L["fx"], L["eyes"], L["mouth"], L["on_face"]
    face = np.clip(1.3 * gsm.blur(masks["face"], 30), 0, 1)
    lids = np.clip(gsm.blur(masks["eyelids"], 4) * 1.3, 0, 1)
    W = {"face": face if head is None else np.maximum(face, np.clip(head, 0, 1))}
    W["forehead"] = ellipse3(P, at(fx, (el[1] + er[1]) / 2 + 0.045), (0.045, 0.022, 0.03))
    W["cheek"] = sum(ellipse3(P, at(fx + s * 0.040, n[1] - 0.004), (0.020, 0.017, 0.02)) for s in (-1, 1))
    W["nose"] = gauss3(P, n, 0.010)
    W["alae"] = sum(gauss3(P, at(n[0] + s * 0.014, n[1] - 0.006), 0.007) for s in (-1, 1))
    W["under_eye"] = sum(ellipse3(P, at(e[0] + np.sign(e[0] - fx) * 0.002, e[1] - 0.015), (0.015, 0.007, 0.012))
                         for e in (el, er)) * (1 - lids)
    W["eyelid"] = lids
    W["chin"] = ellipse3(P, at(fx, mo[1] - 0.034), (0.018, 0.013, 0.02))
    for k in W:
        if k != "face":
            W[k] = np.clip(W[k], 0, 1) * face
    return W


# ------------------------------------------------------------------ point processes -------------
def sample_points(rng, weight, P, cover, n):
    """n texel positions drawn with probability ~ weight (already per unit skin area)."""
    w = np.where(cover, np.maximum(weight, 0), 0).ravel()
    if w.sum() <= 0 or n <= 0:
        return np.zeros((0, 3)), np.zeros((0,), int)
    idx = rng.choice(w.size, size=n, p=w / w.sum())
    return P.reshape(-1, 3)[idx], idx


def splat(P, cover, centres, radii, amps, rng, roughen=0.35, reach=3.0, sharp=2.0):
    """Sum of soft, irregular blobs (centres in 3D, radii in metres) over the covered texels."""
    from scipy.spatial import cKDTree  # noqa: PLC0415
    out = np.zeros(P.shape[:2])
    if len(centres) == 0:
        return out
    tree = cKDTree(centres)
    idx = np.flatnonzero(cover.ravel())
    Q = P.reshape(-1, 3)[idx]
    d, j = tree.query(Q, k=4, distance_upper_bound=float(radii.max() * reach))
    wob = 1 + roughen * gsm.vnoise(Q, 0.0012, int(rng.integers(1 << 30)))
    acc = np.zeros(len(Q))
    for c in range(d.shape[1]):
        ok = np.isfinite(d[:, c])
        jj = j[ok, c]
        acc[ok] += amps[jj] * np.exp(-(d[ok, c] / (radii[jj] * wob[ok])) ** sharp)
    out.ravel()[idx] = acc
    return out


def grow_veins(rng, P, N3, cover, starts, axis_dirs, lengths, radius, weight, step=0.002):
    """Veins as random walks over the surface: each starts at a point, heads along its limb with a
    wander, snaps back to the skin each step, branches now and then and thins as it goes."""
    from scipy.spatial import cKDTree  # noqa: PLC0415
    flat = np.flatnonzero(cover.ravel()[::1])
    pts, nrm = P.reshape(-1, 3)[flat], N3.reshape(-1, 3)[flat]
    sub = slice(None, None, 3)
    tree = cKDTree(pts[sub])
    pts_s, nrm_s = pts[sub], nrm[sub]
    out_p, out_r, out_w = [], [], []
    stack = [(np.asarray(s), np.asarray(d) / np.linalg.norm(d), L, radius, 0)
             for s, d, L in zip(starts, axis_dirs, lengths)]
    while stack:
        p, d, L, r, depth = stack.pop()
        travelled = 0.0
        while travelled < L and r > 0.0003:
            _, i = tree.query(p)
            p, n = pts_s[i], nrm_s[i]
            d = d - (d @ n) * n
            d = d / max(np.linalg.norm(d), 1e-9)
            t = np.cross(n, d)
            d = d + 0.07 * rng.normal() * t
            d = d / np.linalg.norm(d)
            out_p.append(p); out_r.append(r); out_w.append(weight)
            p = p + step * d
            travelled += step
            r *= 0.996
            if depth < 2 and rng.random() < 0.012:
                ang = rng.choice([-1, 1]) * rng.uniform(0.25, 0.5)
                bd = np.cos(ang) * d + np.sin(ang) * t
                stack.append((p.copy(), bd, (L - travelled) * rng.uniform(0.3, 0.7), r * 0.7, depth + 1))
    return np.array(out_p).reshape(-1, 3), np.array(out_r), np.array(out_w)


# ------------------------------------------------------------------ the picture -----------------
def compose(tone, roman, layers, F, lut, rng_seed, detail=None, face_tbl=None):
    """The absolute skin colour (linear) for one tone and one set of layers."""
    P, Nr, cv, cover, reg, masks, parts, J = (F[k] for k in ("P", "N", "cv", "cover", "reg", "masks", "parts", "J"))
    rng = np.random.default_rng(rng_seed)
    m0 = lut.use(roman)
    face = masks["face"]
    # Phase23 click 1 (the lead: "we need some sort of texture on the hands and rest of the body"):
    # the skin-scale detail on the face at the bar's measured strength, and on the body (23.2.2).
    # The face's weight is wide and follows the head, so no seam shows at the hairline.
    dg = DETAIL[lut.tones[roman]["fit"]] if detail is None else detail
    wf = np.clip(np.maximum(1.3 * gsm.blur(face, 40), 0.8 * F["parts"]["head"]), 0, 1)
    gf, gc, gd = ((dg[k][1] + (dg[k][0] - dg[k][1]) * wf) for k in ("fine", "coarse", "dots"))
    down = -Nr[..., 1]                                  # A-pose: the palms and the soles face down
    palm = parts["hand"] * np.clip((down - 0.2) / 0.5, 0, 1)
    sole = parts["foot"] * np.clip((down - 0.4) / 0.4, 0, 1)
    under_arm = (parts["forearm"] + parts["upperarm"]) * np.clip((down + 0.1) / 0.6, 0, 1)

    # sun exposure 0..1: face, neck, the backs of the hands and the forearms most; the trunk least
    sun = (0.95 * np.maximum(face, parts["head"] * 0.8) + 0.8 * parts["neck"] + 0.85 * parts["hand"]
           + 0.7 * parts["forearm"] + 0.5 * parts["upperarm"] + 0.3 * parts["trunk"]
           + 0.4 * parts["thigh"] + 0.55 * parts["shin"] + 0.5 * parts["foot"])
    sun = np.clip(sun - 0.3 * under_arm, 0, 1)
    upper_back = parts["trunk"] * np.clip((P[..., 1] - (J["pelvis"][1] + 0.6 * (J["neck"][1] - J["pelvis"][1]))) / 0.12, 0, 1)
    sun = sun + 0.15 * upper_back * np.clip(-Nr[..., 2], 0, 1)

    M = (0.82 + 0.36 * sun)
    M *= 1 - 0.45 * np.maximum(palm, sole)                       # palms and soles: little melanin
    M *= 1 + 0.18 * gsm.blur(masks["eyelids"], 6) + 0.5 * gsm.blur(masks["aureolae"], 4)
    M *= 1 + 0.22 * np.clip(cv, 0, 1.5)                          # creases: a little darker
    # The skin-scale detail is kept apart (``Md``) and added as an AMOUNT of pigment after the face's
    # regions (23.2.7): a fleck is the same melanin on a face whose melanin a region took out, so it
    # shows more on pale skin, not less (multiplied in, it vanished on III's pale face).
    Md = np.exp(gc * fbm(P, (0.025, 0.007), (0.09, 0.07), 11))
    Md *= np.exp(gf * fbm(P, (0.0025, 0.0012), (0.07, 0.05), 211))
    speck = np.abs(gsm.vnoise(P, 0.0009, 13)) + 0.5 * np.abs(gsm.vnoise(P, 0.0005, 17))
    Md *= np.exp(0.10 * gf * (0.6 - speck))                      # fine, uneven pigment (1-2 mm)
    Md *= 1 + gd * np.clip((gsm.vnoise(P, 0.0011, 41) - 0.5) / 0.3, 0, 1)  # sparse ~1 mm flecks

    # blood: cheeks, the nose, the ears, the fingertips and the palms, knuckles, elbows, knees
    Fp = P[(face > 0.5) & cover]
    nose = Fp[np.argmax(Fp[:, 2])]
    fx = Fp[:, 0].mean()
    cheek_y = nose[1] + 0.005
    cheek = np.zeros(P.shape[:2])
    for side in (-1, 1):
        c = np.array([fx + side * 0.042, cheek_y, 0.0])
        near = Fp[(np.abs(Fp[:, 0] - c[0]) < 0.01) & (np.abs(Fp[:, 1] - c[1]) < 0.01)]
        c[2] = near[:, 2].max() if len(near) else nose[2] - 0.02
        cheek = np.maximum(cheek, gauss3(P, c, 0.022))
    cheek *= gsm.blur(face, 10)
    tips = sum(gauss3(P, J[f"{s}-finger-{k}-4"], 0.012) for s in "lr" for k in range(1, 6))
    knuckles = sum(gauss3(P, J[f"{s}-finger-{k}-2"], 0.009) for s in "lr" for k in range(2, 6)) * np.clip(Nr[..., 1] + 0.3, 0, 1)
    joints_out = sum(gauss3(P, J[f"{s}-{j}"], 0.035) for s in "lr" for j in ("elbow", "knee"))
    sss = gsm._grey("sss.png")
    sss = np.clip(sss / max(np.percentile(sss[cover], 99), 1e-6), 0, 1)
    B = (1 + 0.9 * dg["flush"] * cheek + 0.8 * dg["flush"] * gauss3(P, nose, 0.012) + 0.9 * gsm.blur(masks["ears"], 6)
         + 0.7 * tips + 0.45 * palm + 0.5 * knuckles + 0.35 * joints_out + 0.25 * sss)
    Bd = np.exp(gc * fbm(P, (0.015, 0.004), (0.18, 0.12), 23) + gf * fbm(P, (0.0015, 0.0008), (0.08, 0.05), 223))
    so2 = np.full(P.shape[:2], 0.8)
    under_eye = gsm.blur(masks["eyelids"], 10)
    so2 = so2 - 0.25 * under_eye                                   # the bluish shadow under the eyes
    depth = np.zeros(P.shape[:2])
    fw = F.get("face_w") or face_regions(P, masks, cover, parts["head"])
    fit = lut.tones[roman]["fit"]
    Fm, Fb = np.ones(P.shape[:2]), np.ones(P.shape[:2])
    for k, (dm, db, ds, dd) in (FACE[fit] if face_tbl is None else face_tbl).items():
        Fm *= np.exp(dm * fw[k]); Fb *= np.exp(db * fw[k])
        so2 = so2 + ds * fw[k]; depth = depth + dd * fw[k]
    M *= np.maximum(Fm + Md - 1, 0.3 * Fm)                       # the regions, then the detail's amount
    B *= np.maximum(Fb + Bd - 1, 0.3 * Fb)
    dmel = np.zeros(P.shape[:2])

    # Each layer draws from its own generator, seeded alike, so SynthAll is exactly the single layers
    # together (round 2, 2026-10-26; before, SynthAll's veins and marks moved with the freckles' draws).
    if "freckles" in layers:
        rng = np.random.default_rng(rng_seed)
        # Round 2 (2026-10-26; the lead: "the freckles on the face read really large and oddly placed").
        # The face: a butterfly over the nose bridge and the upper cheeks, on the surface that faces
        # forward (the sun), symmetric by construction and not clustered; elsewhere on the face, sparse.
        # Round 1 put a +-5 cm band at nose-tip height from ear to ear and drew the face's freckles in
        # a few clumps of nine, which landed one-sided.
        def surface(x, y):
            near = Fp[(np.abs(Fp[:, 0] - x) < 0.006) & (np.abs(Fp[:, 1] - y) < 0.006)]
            return np.array([x, y, near[:, 2].max() if len(near) else nose[2] - 0.02])
        lid = P[(masks["eyelids"] > 0.5) & cover]
        eye_l, eye_r = lid[lid[:, 0] < fx].mean(0), lid[lid[:, 0] >= fx].mean(0)
        eye_y = (eye_l[1] + eye_r[1]) / 2
        facing = np.clip(Nr[..., 2] + 0.15, 0, 1)
        butterfly = gauss3(P, surface(fx, eye_y - 0.4 * (eye_y - nose[1])), 0.016)
        for e in (eye_l, eye_r):
            out_x = e[0] + np.sign(e[0] - fx) * 0.006
            butterfly = np.maximum(butterfly, gauss3(P, surface(out_x, e[1] - 0.024), 0.022))
        fdens = face * facing * (butterfly + 0.06)
        fc, _ = sample_points(rng, fdens, P, cover, 420)
        fr_r = np.exp(rng.normal(np.log(0.00055), 0.3, len(fc))).clip(0.0003, 0.0011)
        # The body: the shoulders, upper back, arms and hands, in small loose clusters.
        dens = (0.7 * upper_back + 0.35 * parts["upperarm"] * (1 - under_arm)
                + 0.55 * parts["forearm"] * (1 - under_arm) + 0.3 * parts["hand"] * (1 - palm)
                + 0.25 * parts["trunk"] * np.clip(Nr[..., 2], 0, 1) * np.clip((P[..., 1] - J["neck"][1] + 0.18) / 0.1, 0, 1))
        parents, _ = sample_points(rng, dens, P, cover, 240)
        kids = np.repeat(parents, 5, axis=0) + rng.normal(0, 0.008, (len(parents) * 5, 3))
        kids = np.concatenate([kids, sample_points(rng, dens, P, cover, 700)[0]])
        kr = np.exp(rng.normal(np.log(0.0008), 0.3, len(kids))).clip(0.0004, 0.0016)
        centres, radii = np.concatenate([fc, kids]), np.concatenate([fr_r, kr])
        amps = rng.uniform(0.5, 1.0, len(centres))
        fr = splat(P, cover, centres, radii, amps, rng, roughen=0.35, sharp=2.2)
        allw = fdens + dens
        dmel += 0.085 * np.clip(fr, 0, 1.2) * (0.6 + 0.4 * gsm.blur(allw, 20) / max(allw.max(), 1e-6))

    vein = np.zeros(P.shape[:2])
    if "veins" in layers:
        rng = np.random.default_rng(rng_seed)
        starts, dirs, lens, ws = [], [], [], []
        for s in "lr":
            elbow, wrist = J[f"{s}-elbow"], J[f"{s}-hand"]
            for k in range(3):                                     # the inner forearm
                a = wrist + (elbow - wrist) * 0.05 + np.array([rng.normal(0, 0.012), -0.02, rng.normal(0, 0.012)])
                starts.append(a); dirs.append(elbow - wrist); lens.append(rng.uniform(0.12, 0.2)); ws.append(1.0)
            for k in range(4):                                     # the back of the hand
                f = J[f"{s}-finger-{k + 2}-1"]
                starts.append(f + np.array([0, 0.012, 0])); dirs.append(wrist - f); lens.append(0.07); ws.append(1.0)
            ank = J[f"{s}-ankle"]
            for k in range(2):                                     # the top of the foot, the inner ankle
                t = J[f"{s}-toe-{1 + 2 * k}-1"]
                starts.append(t + np.array([0, 0.015, 0])); dirs.append(ank - t); lens.append(0.1); ws.append(0.8)
            side = 1 if s == "l" else -1
            temple = J["head"] + np.array([side * 0.062, 0.0, 0.03])
            starts.append(temple); dirs.append(np.array([0, 1.0, -0.3])); lens.append(0.05); ws.append(0.6)
            chest = J["neck"] + np.array([side * 0.07, -0.12, 0.09])
            starts.append(chest); dirs.append(np.array([side * 0.4, -1.0, 0])); lens.append(0.14); ws.append(0.45)
            knee_back = J[f"{s}-knee"] + np.array([0, 0.02, -0.06])
            starts.append(knee_back); dirs.append(J[f"{s}-upper-leg"] - J[f"{s}-knee"]); lens.append(0.16); ws.append(0.5)
        vp, vr, vw = [], [], []
        for a, d, L, w in zip(starts, dirs, lens, ws):
            p_, r_, w_ = grow_veins(rng, P, Nr, cover, [a], [d], [L], radius=rng.uniform(0.0022, 0.003), weight=w)
            vp.append(p_); vr.append(r_); vw.append(w_)
        vp, vr, vw = np.concatenate(vp), np.concatenate(vr), np.concatenate(vw)
        vein = np.clip(splat(P, cover, vp, vr * 1.6, vw * 0.5, rng, roughen=0.15, reach=3.0, sharp=1.4), 0, 1)
        vein = gsm.blur(vein, 2)

    if "marks" in layers:
        rng = np.random.default_rng(rng_seed)
        # moles: sparse, densest on the arms and the back
        mdens = 0.6 * parts["trunk"] * np.clip(-Nr[..., 2] + 0.4, 0, 1.4) + 0.5 * parts["upperarm"] + 0.5 * parts["forearm"] \
            + 0.35 * parts["thigh"] + 0.3 * face + 0.25 * parts["neck"] + 0.2 * parts["shin"]
        mc, _ = sample_points(rng, mdens, P, cover, 34)
        mr = np.exp(rng.normal(np.log(0.0016), 0.35, len(mc))).clip(0.0008, 0.0035)
        dmel += 0.28 * np.clip(splat(P, cover, mc, mr, rng.uniform(0.6, 1.0, len(mc)), rng, roughen=0.2, sharp=3.5), 0, 1.2)
        # acne on the T-zone, cheeks, chin and jaw, and the upper back: red papules; some healed to brown
        tzone = face * (np.clip(1 - np.abs(P[..., 0] - fx) / 0.02, 0, 1) + 0.7 * cheek + 0.5 * np.clip((nose[1] - 0.035 - P[..., 1]) / 0.03, 0, 1))
        adens = tzone + 0.5 * upper_back * np.clip(-Nr[..., 2], 0, 1)
        ac, _ = sample_points(rng, adens, P, cover, 70)
        ar = np.exp(rng.normal(np.log(0.0011), 0.3, len(ac))).clip(0.0006, 0.0025)
        red = rng.random(len(ac)) < 0.6
        papules = splat(P, cover, ac[red], ar[red], rng.uniform(0.6, 1.0, red.sum()), rng, roughen=0.25, sharp=2.0)
        pih = splat(P, cover, ac[~red], ar[~red] * 1.4, rng.uniform(0.5, 1.0, (~red).sum()), rng, roughen=0.3, sharp=2.0)
        B *= 1 + 2.6 * np.clip(papules, 0, 1)
        dmel += 0.02 * np.clip(pih, 0, 1) + 0.12 * m0 * np.clip(pih, 0, 1)
        # flushing of the nose and the cheeks
        B *= 1 + 0.55 * np.maximum(cheek, gauss3(P, nose, 0.018)) * (1 + 0.4 * gsm.vnoise(P, 0.004, 31))

    mel = m0 * M + dmel
    bld = BLOOD0 * B
    base = lut(np.full_like(mel, m0), np.full_like(bld, BLOOD0), np.full_like(mel, 0.8))
    col = lut(mel, bld, np.clip(so2, 0.45, 0.95))
    # Blood BELOW the dermis (a vein, the ring under the eye). The tabulated model is one semi-infinite
    # layer with no depth, where more blood only absorbs more blue (it reads orange, measured
    # 2026-10-26). What makes it read blue-violet is depth: red light reaches it and is absorbed, blue
    # scatters back before it gets there. So it darkens each channel by how deep that channel's light
    # goes, which is the article's own scatter depth per channel (subsurface_radius_scale).
    reach = np.asarray(F["scatter_scale"][roman])
    if "veins" in layers:
        depth = depth + 0.30 * vein
    col = col * np.clip(1 - depth[..., None] * reach, 0.2, 1.5)
    ratio = (col + EPS) / (base + EPS)
    out = tone * ratio

    # the lips: the library's rule, feathered (the Lips article carries its own lip colour)
    lm = np.clip(gsm.blur(masks["lips"], 5) * 1.15, 0, 1)[..., None]
    lips = tone * np.array(LIPS[fit]) * (0.92 + 0.08 * gsm.vnoise(P, 0.0025, 7)[..., None])
    out = out * (1 - lm) + lips * lm
    S = reg["Body"]
    s = (tone - (lips * lm)[S].mean(0)) / (out * (1 - lm))[S].mean(0)
    out = out * s * (1 - lm) + lips * lm
    return out, {"melanin0": round(m0, 4), "blood0": BLOOD0}


def fields() -> dict:
    m = make_kits.load_mesh(MESH)
    if m["uv_sha256"] != make_kits.G.PART_MESHES[MESH]["uv_sha256"]:
        raise SystemExit("the mesh's layout is not MakeHuman_Body_v01's")
    P, Nr, cv, rcover = rasterise(m)
    P = gsm.bleed(P, rcover, gsm.BLEED)
    Nr = gsm.bleed(Nr, rcover, gsm.BLEED)
    cv = gsm.bleed(cv[..., None], rcover, gsm.BLEED)[..., 0]
    reg = gsm.regions()
    cover = rcover | reg["islands"]
    masks = {k: gsm._grey(f"mpfb_{k}.jpg") for k in gsm.MASKS}
    J = joints()
    scale = {}
    for roman in ("I", "II", "III", "IV", "V", "VI"):
        r = json.loads((gsm.RECIPES / f"Skin_Fitzpatrick{roman}_Clean_Base_s001_v01.json").read_text())
        scale[roman] = [float(x) for x in r["subsurface_radius_scale"].split(",")]
    return {"scatter_scale": scale, "P": P, "N": Nr, "cv": cv, "cover": cover, "reg": reg, "masks": masks,
            "parts": body_parts(P, J), "J": J}


def write_provenance(rows: dict, lut: Lut) -> None:
    old = {}
    if PROVENANCE.is_file():
        for line in PROVENANCE.read_text().splitlines():
            if line.startswith("  Fitzpatrick") and ": {" in line:
                old[line.split(":", 1)[0].strip()] = line
    for name, r in rows.items():
        old[name] = f"  {name}: {json.dumps(r, separators=(', ', ': '))}"
    names = sorted(old)
    src = [bc.SOURCES[n] for n in ("base.obj", "mpfb_face.jpg", "mpfb_lips.jpg", "mpfb_ears.jpg",
                                   "mpfb_eyelids.jpg", "mpfb_aureolae.jpg", "sss.png")]
    lines = [
        "# Provenance for the SYNTHETIC skin test maps (the lead's spike, 2026-10-26): drafts beside the",
        "# six shipped skin maps, on MakeHuman_Body_v01 (hm08). CC0 parts only, no photograph, no AI",
        "# (RD-SKM-2); colour from a tabulated two-chromophore skin model. Written by `evidence`.",
        "id: fit/makehuman/synth_skin",
        "version: v01",
        "files:",
        *[f"  - MatterLibrary/textures/fit/makehuman/skin/{n}_basecolor_{TAG}.png" for n in names],
        "provenance:",
        "  source: procedural",
        "  license: CC0-1.0",
        "  upstream:",
        *[f"    - {{url: {s['url']}, sha256: {s['sha256']}}}" for s in src],
        "  upstream_licence: \"CC0 (MPFB2 LICENSE.ASSETS.md: the hm08 base mesh and its textures)\"",
        f"  model: \"{lut.meta['model']} (Open Morphology Foundation {lut.meta['omf_commit']}), tabulated in tools/converters/fit/synth/chromophore_lut.json\"",
        "  evidence: tools/converters/fit/gen_synth_skin.py",
        "members:",
        *[old[n] for n in names],
    ]
    PROVENANCE.parent.mkdir(parents=True, exist_ok=True)
    PROVENANCE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("tones", nargs="*", default=list(DRAFT_TONES))
    ap.add_argument("--detail", action="append", choices=DETAILS, help="one layer set (repeatable; default all)")
    ap.add_argument("--out", type=Path, help="write the pictures here instead (a trial: no provenance)")
    a = ap.parse_args(argv)
    lut = Lut()
    F = fields()
    rows = {}
    for roman in a.tones:
        tone = gsm.tone_of(roman)
        for i, det in enumerate(a.detail or DETAILS):
            col, info = compose(tone, roman, LAYERS[det], F, lut, SEED)
            srgb8, _c, st = gsm.calibrate(col, tone, F["reg"], F["cover"])
            name = f"Fitzpatrick{roman}{det}"
            out = (a.out or OUT)
            out.mkdir(parents=True, exist_ok=True)
            p = out / f"{name}_basecolor_{TAG}.png"
            Image.fromarray(srgb8, "RGB").save(p, optimize=True)
            rows[name] = {"made": "procedural", **info, "layers": list(LAYERS[det]), **st}
            print(f"{name}: {p}\n  " + json.dumps(st))
            if st["uncovered_islands"]:
                raise SystemExit(f"{name}: {st['uncovered_islands']} island texels left unpainted")
    if not a.out:
        write_provenance(rows, lut)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
