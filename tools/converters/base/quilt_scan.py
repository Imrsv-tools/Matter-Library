#!/usr/bin/env python3
"""Re-make a scanned texture set at a scale option's size, by image quilting (Phase19 D-9).

A scan whose tile is not a scale option (Granite at 0.4 m under `s1`) is never stretched to
fit (RD-P19-2). This tool builds a NEW seamless tile of the option's size out of patches of
the scan, each kept at the scan's own size: a crystal 5 mm across in the scan is 5 mm across
in the result. It is Efros and Freeman's image quilting (SIGGRAPH 2001) on a torus: patches
in a grid, each picked among random places in the scan for how well it matches what is
already laid down where they overlap, joined along the cheapest cut through that overlap;
the last row and column also match the first, so the result wraps.

It suits STOCHASTIC matter (granite speckle, sand, terrazzo, a concrete's aggregate). It
does not suit STRUCTURED matter (onyx bands, wood grain, lace): a band cut into patches
breaks at every cut. Those are re-made by a generator.

A scan's broad tone (a pale streak across the tile, uneven light at capture) is
flattened first (`--flatten`, on by default): each colour and roughness map is divided by
its own wrapped blur a few patches wide and scaled back to its mean, so only the grain is
quilted. Without it a broad streak, cut into patches, shows as pale blocks on the patch
grid. The relief (normal) keeps its own.

All maps of the set get the same patches and cuts, so colour, roughness and relief stay
in register. The patches are picked on the base colour's luminance. Normals are blended
as vectors and renormalised. The quilt is built at the scan's own pixel density, then
resized to `--size` with a wrapped border, so it stays seamless: that changes the
resolution, never the size in metres (RD-P19-1).

    quilt_scan.py <SET> --src DIR --src-m 0.4 --out-m 1.0 --scale s1 [--size 2048] [--patch 160 --overlap 32] [--resample PX] [--no-flatten] --out DIR

Reads DIR/<SET>_<channel>_*.png (basecolor, roughness, normal, metalness; those present) and writes
<SET>_<channel>_<scale>.png. Fixed seed, no network. It refuses to overwrite an existing
file (AI_WorkingAgreement §Build Safety).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent.parent.parent
CHANNELS = ("basecolor", "roughness", "normal", "metalness")
SEED = 1901
PATCH = 160            # patch side, in scan pixels
OVERLAP = 32           # the strip a patch shares with its neighbours
CANDIDATES = 400       # random places in the scan tried per patch
TOLERANCE = 1.1        # pick at random among the places within this factor of the best match
FLATTEN = 2 * PATCH    # the box the broad tone is measured over, in scan pixels


def load(path: Path) -> np.ndarray:
    a = np.asarray(Image.open(path)).astype(np.float32) / 255.0
    return a[..., None] if a.ndim == 2 else a[..., :3]


def wrap_take(img: np.ndarray, ys, xs) -> np.ndarray:
    """img[ys, xs] with wrap-around; ys, xs broadcastable index arrays."""
    return img[np.asarray(ys) % img.shape[0], np.asarray(xs) % img.shape[1]]


def box_wrapped(img: np.ndarray, side: int) -> np.ndarray:
    """A box blur of a seamless tile, wrapping at its edges."""
    r = side // 2
    k = 2 * r + 1
    p = np.pad(img, ((r, r), (r, r), (0, 0)), mode="wrap")
    c = np.cumsum(np.cumsum(np.pad(p, ((1, 0), (1, 0), (0, 0))), 0), 1)
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


def flatten(img: np.ndarray) -> np.ndarray:
    """The map with its broad tone taken out: divided by its blur, scaled back to its mean."""
    broad = box_wrapped(box_wrapped(img, FLATTEN), FLATTEN)    # two passes: a smooth blur
    return img / np.maximum(broad, 1e-3) * img.mean(axis=(0, 1))


def min_cut(err: np.ndarray) -> np.ndarray:
    """The cheapest top-to-bottom path through err (rows x cols): one column per row."""
    rows, cols = err.shape
    cost = err.copy()
    for r in range(1, rows):
        prev = cost[r - 1]
        left = np.r_[np.inf, prev[:-1]]
        right = np.r_[prev[1:], np.inf]
        cost[r] += np.minimum(np.minimum(left, prev), right)
    path = np.empty(rows, dtype=int)
    path[-1] = int(np.argmin(cost[-1]))
    for r in range(rows - 2, -1, -1):
        c = path[r + 1]
        lo, hi = max(c - 1, 0), min(c + 2, cols)
        path[r] = lo + int(np.argmin(cost[r, lo:hi]))
    return path


def soften(mask: np.ndarray, r: int = 2) -> np.ndarray:
    """A small box blur, so a cut is a few pixels' blend rather than a hard edge."""
    k = 2 * r + 1
    p = np.pad(mask, r, mode="edge")
    c = np.cumsum(np.cumsum(np.pad(p, ((1, 0), (1, 0))), 0), 1)
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


def patch_mask(err: np.ndarray, filled: np.ndarray, last_row: bool, last_col: bool) -> np.ndarray:
    """Where the new patch shows (1) and where what is laid down stays (0)."""
    b, ov = PATCH, OVERLAP
    new = np.ones((b, b), dtype=np.float32)
    if filled[:, :ov].any():                                   # left
        for r, c in enumerate(min_cut(err[:, :ov])):
            new[r, :c] = 0
    if filled[:ov, :].any():                                   # top
        for c, r in enumerate(min_cut(err[:ov, :].T)):
            new[:r, c] = 0
    if last_col and filled[:, b - ov:].any():                  # right, wrapping to column 0
        for r, c in enumerate(min_cut(err[:, b - ov:])):
            new[r, b - ov + c + 1:] = 0
    if last_row and filled[b - ov:, :].any():                  # bottom, wrapping to row 0
        for c, r in enumerate(min_cut(err[b - ov:, :].T)):
            new[b - ov + r + 1:, c] = 0
    new = soften(new)
    return np.where(filled, new, 1.0)


def plan(guide: np.ndarray, size: int, rng) -> list:
    """Lay the patches on the guide: [(rows, cols, y0, x0, mask)], rows and cols wrapped."""
    step = PATCH - OVERLAP
    n = size // step
    canvas = np.zeros((size, size), dtype=np.float32)
    done = np.zeros((size, size), dtype=bool)
    ar = np.arange(PATCH)
    sub = np.arange(0, PATCH, 2)                                # match on every other pixel
    ops = []
    for i in range(n):
        for j in range(n):
            rows, cols = (i * step + ar) % size, (j * step + ar) % size
            here, filled = canvas[np.ix_(rows, cols)], done[np.ix_(rows, cols)]
            ys = rng.randint(0, guide.shape[0], CANDIDATES)
            xs = rng.randint(0, guide.shape[1], CANDIDATES)
            if filled.any():
                cand = wrap_take(guide, ys[:, None, None] + sub[None, :, None], xs[:, None, None] + sub[None, None, :])
                f = filled[np.ix_(sub, sub)]
                e = (((cand - here[np.ix_(sub, sub)]) ** 2) * f).sum(axis=(1, 2))
                pick = rng.choice(np.flatnonzero(e <= e.min() * TOLERANCE + 1e-9))
            else:
                pick = 0
            y0, x0 = int(ys[pick]), int(xs[pick])
            patch = wrap_take(guide, y0 + ar[:, None], x0 + ar[None, :])
            err = np.where(filled, (patch - here) ** 2, 0.0)
            mask = patch_mask(err, filled, i == n - 1, j == n - 1)
            canvas[np.ix_(rows, cols)] = mask * patch + (1 - mask) * here
            done[np.ix_(rows, cols)] = True
            ops.append((rows, cols, y0, x0, mask))
    return ops


def apply(img: np.ndarray, ops: list, size: int) -> np.ndarray:
    out = np.zeros((size, size, img.shape[2]), dtype=np.float32)
    ar = np.arange(PATCH)
    for rows, cols, y0, x0, mask in ops:
        patch = wrap_take(img, y0 + ar[:, None], x0 + ar[None, :])
        cur = out[np.ix_(rows, cols)]
        out[np.ix_(rows, cols)] = mask[..., None] * patch + (1 - mask[..., None]) * cur
    return out


def renormalise(n: np.ndarray) -> np.ndarray:
    v = n * 2 - 1
    v /= np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-6)
    return v * 0.5 + 0.5


def resize_wrapped(img: np.ndarray, size: int) -> np.ndarray:
    """Resize a seamless tile to size x size, padding with its own wrap so the edges stay seamless."""
    src = img.shape[0]
    if src == size:
        return img
    pad = src // 16
    padded = np.pad(img, ((pad, pad), (pad, pad), (0, 0)), mode="wrap")
    k = size / src
    big = round(padded.shape[0] * k)
    chans = [np.asarray(Image.fromarray(padded[..., c]).resize((big, big), Image.LANCZOS)) for c in range(img.shape[2])]
    out = np.stack(chans, axis=-1)
    o = round(pad * k)
    return out[o:o + size, o:o + size]


def main(argv=None) -> int:
    global PATCH, OVERLAP, FLATTEN                             # one quilt per run: set once, below
    ap = argparse.ArgumentParser(description="Re-make a scanned texture set at a scale option's size.")
    ap.add_argument("set", help="the texture set's name, e.g. Granite_Polished")
    ap.add_argument("--src", required=True, help="the folder holding the scan's maps")
    ap.add_argument("--src-m", type=float, required=True, help="the scan's tile, in metres")
    ap.add_argument("--out-m", type=float, required=True, help="the scale option's length, in metres")
    ap.add_argument("--scale", required=True, help="the scale tag in the written names, e.g. s1")
    ap.add_argument("--size", type=int, default=2048, help="the written resolution, in pixels")
    ap.add_argument("--patch", type=int, default=PATCH, help="patch side, in scan pixels")
    ap.add_argument("--overlap", type=int, default=OVERLAP,
                    help="the strip a patch shares with its neighbours; patch - overlap must divide the quilt")
    ap.add_argument("--resample", type=int, default=0,
                    help="resize the scan's maps to N px first: a resolution change, never a size "
                         "change, for a quilt whose pixel count no patch step divides")
    ap.add_argument("--no-flatten", dest="flatten", action="store_false",
                    help="quilt the scan's broad tone too (a scan with none)")
    ap.add_argument("--out", required=True)
    args = ap.parse_args(argv)
    PATCH, OVERLAP, FLATTEN = args.patch, args.overlap, 2 * args.patch

    src, out = Path(args.src), Path(args.out)
    maps = {}
    for ch in CHANNELS:
        found = sorted(src.glob(f"{args.set}_{ch}_*.png"))
        if found:
            maps[ch] = load(found[0])
            if args.resample:
                maps[ch] = resize_wrapped(maps[ch], args.resample)
            if args.flatten and ch in ("basecolor", "roughness"):   # not relief, not a metal mask
                maps[ch] = flatten(maps[ch])
    if "basecolor" not in maps:
        print(f"no {args.set}_basecolor_*.png in {src}", file=sys.stderr)
        return 1
    side = maps["basecolor"].shape[0]
    work = round(side * args.out_m / args.src_m)               # the quilt at the scan's own density
    step = PATCH - OVERLAP
    if work % step:
        print(f"{work} px is not a whole number of {step} px steps; pick another --patch or --overlap", file=sys.stderr)
        return 1
    targets = {ch: out / f"{args.set}_{ch}_{args.scale}.png" for ch in maps}
    if any(p.exists() for p in targets.values()):
        print(f"refusing to overwrite {args.set} in {out} (Build Safety)", file=sys.stderr)
        return 1

    base = maps["basecolor"]
    guide = base @ np.array([0.2126, 0.7152, 0.0722], dtype=np.float32)
    ops = plan(guide, work, np.random.RandomState(SEED))
    out.mkdir(parents=True, exist_ok=True)
    for ch, img in maps.items():
        q = apply(img, ops, work)
        if ch == "normal":
            q = renormalise(q)
        q = resize_wrapped(q, args.size)
        if ch == "normal":
            q = renormalise(q)
        q = (np.clip(q, 0, 1) * 255).round().astype(np.uint8)
        Image.fromarray(q[..., 0] if q.shape[2] == 1 else q).save(targets[ch], "PNG", optimize=True)
        print(f"wrote {targets[ch]}  (mean {q.reshape(-1, q.shape[2]).mean(0).round(1)}, scan "
              f"{(img.reshape(-1, img.shape[2]).mean(0) * 255).round(1)})")
    print(f"{len(ops)} patches of {PATCH} px ({PATCH * args.src_m / side * 100:.1f} cm) on a {work} px quilt "
          f"({args.out_m} m), written at {args.size} px")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
