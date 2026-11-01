#!/usr/bin/env python3
"""Have an image model repaint the head's renders as a photographed person, through ComfyUI (Phase25).

    python3 tools/converters/fit/gen_views_model.py <dir> --model flux|krea --views f000[,…] \\
        --src <render tag> --tag <out tag> [--seed 7] [--steps N] [--strength 0.6] [--server URL]

Reads ``<dir>/in_<view>_<src>.png`` (``project_views.py render``), sends each through a tracked
workflow (``comfy/flux2klein_edit.json``: FLUX.2 [klein] 4B, the render as its reference; or
``comfy/krea2turbo_img2img.json``: Krea 2 Turbo from the render's latent, denoised at ``--strength``,
F-P25-3) to a running ComfyUI, and writes ``<dir>/view_<view>_<tag>.png`` and
``<dir>/view_<view>_<tag>.json`` (the model files, seed, steps, strength, prompt). The standard library
only: torch lives in ComfyUI's own environment, and ComfyUI finds the models through its own model
paths, so no path to them is written here (RD-P25-7). Start ComfyUI first (``comfyui``); this script
does not start or stop it.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
WORKFLOWS = {"flux": HERE / "comfy" / "flux2klein_edit.json", "krea": HERE / "comfy" / "krea2turbo_img2img.json"}
STEPS = {"flux": 4, "krea": 8}

# The subject (RD-P25-5): hm08's default age (RD-OVS-3), the measured tone between III and IV (RD-P24-1).
# The lead at click 1: "ths looks like a 3d animation skin ... We want a human skin". The first prompt said
# "photorealistic", "matte ... no shine" and "a cross-polarised flat scan", which pull toward a render and a
# retouched face; this one asks for an unretouched photograph of a real person.
PERSON = ("a real young woman about twenty years old with light, warm skin between Fitzpatrick types III and IV, "
          "a fully shaved bald head, completely shaved-off eyebrows (no eyebrow hair at all), eyes gently closed, "
          "no makeup")
SKIN = ("real human skin, unretouched: visible pores, fine vellus hair, a few small blemishes and tiny moles, "
        "uneven tone, slight redness around the nose and on the cheeks, faint freckles, faint veins at the temples; "
        "no retouching, no airbrushing, no beauty filter, not a 3D render, not CGI")
LIGHT = ("raw documentary photograph on a DSLR with a 100 mm macro lens, soft overcast daylight from the front, "
         "even and gentle; plain dark grey background")
KEEP = ("Keep exactly the same head shape, face shape, pose, camera angle, framing and silhouette as the image; "
        "only change the surface so it looks like a real photograph.")


def prompt(model: str, words: str) -> str:
    if model == "flux":       # an edit model takes an instruction
        return f"Turn this 3D render into a high-resolution photograph, {words}, of {PERSON}. {SKIN}. {LIGHT}. {KEEP}"
    return f"A high-resolution photograph, {words}, of {PERSON}. {SKIN}. {LIGHT}."   # Krea draws a description


def _call(server: str, path: str, data: bytes | None = None, headers: dict | None = None):
    req = urllib.request.Request(server + path, data=data, headers=headers or {})
    with urllib.request.urlopen(req, timeout=600) as r:
        return r.read()


def upload(server: str, picture: Path) -> str:
    boundary = uuid.uuid4().hex
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{picture.name}\"\r\n"
            f"Content-Type: image/png\r\n\r\n").encode() + picture.read_bytes() + \
        f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n--{boundary}--\r\n".encode()
    r = json.loads(_call(server, "/upload/image", body, {"Content-Type": f"multipart/form-data; boundary={boundary}"}))
    return r["name"] if not r.get("subfolder") else f"{r['subfolder']}/{r['name']}"


def fill(graph: dict, values: dict) -> dict:
    out = {}
    for nid, node in graph.items():
        ins = {}
        for k, v in node["inputs"].items():
            if isinstance(v, str) and v.startswith("{{") and v.endswith("}}"):
                v = values[v[2:-2]]
            ins[k] = v
        out[nid] = {"class_type": node["class_type"], "inputs": ins}
    return out


def run(server: str, graph: dict) -> tuple[bytes, str]:
    cid = uuid.uuid4().hex
    pid = json.loads(_call(server, "/prompt", json.dumps({"prompt": graph, "client_id": cid}).encode(),
                           {"Content-Type": "application/json"}))["prompt_id"]
    while True:
        h = json.loads(_call(server, f"/history/{pid}"))
        if pid in h:
            st = h[pid].get("status", {})
            if st.get("status_str") == "error":
                raise SystemExit(f"ComfyUI failed: {json.dumps(st)[:2000]}")
            if st.get("completed"):
                for o in h[pid]["outputs"].values():
                    for im in o.get("images", []):
                        q = urllib.parse.urlencode({"filename": im["filename"], "subfolder": im["subfolder"], "type": im["type"]})
                        return _call(server, f"/view?{q}"), pid
                raise SystemExit("ComfyUI finished with no picture")
        time.sleep(1)


def main(argv=None) -> int:
    import project_views as pv  # noqa: PLC0415  (its view table; it re-execs only when run as a script)
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("dir", type=Path)
    ap.add_argument("--model", choices=WORKFLOWS, required=True)
    ap.add_argument("--views", required=True)
    ap.add_argument("--src", required=True, help="the render tag (in_<view>_<src>.png)")
    ap.add_argument("--tag", required=True)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--steps", type=int)
    ap.add_argument("--strength", type=float, default=0.6, help="Krea only: how far from the render it repaints")
    ap.add_argument("--server", default="http://127.0.0.1:8188")
    a = ap.parse_args(argv)
    graph = json.loads(WORKFLOWS[a.model].read_text(encoding="utf-8"))
    version = json.loads(_call(a.server, "/system_stats"))["system"]["comfyui_version"]
    steps = a.steps or STEPS[a.model]
    for k in a.views.split(","):
        t = time.time()
        src = a.dir / f"in_{k}_{a.src}.png"
        text = prompt(a.model, pv.VIEWS[k]["words"])
        values = {"IMAGE": upload(a.server, src), "PROMPT": text, "SEED": a.seed, "STEPS": steps,
                  "STRENGTH": a.strength, "PREFIX": f"matter_p25_{a.tag}_{k}"}
        png, pid = run(a.server, fill(graph, values))
        (a.dir / f"view_{k}_{a.tag}.png").write_bytes(png)
        models = {n["class_type"]: n["inputs"].get("unet_name") or n["inputs"].get("clip_name") or n["inputs"].get("vae_name")
                  for n in graph.values() if n["class_type"] in ("UNETLoader", "CLIPLoader", "VAELoader")}
        rec = {"model": a.model, "workflow": WORKFLOWS[a.model].name, "files": models, "comfyui": version,
               "seed": a.seed, "steps": steps, "strength": a.strength if a.model == "krea" else None,
               "source": src.name, "prompt": text, "prompt_id": pid, "seconds": round(time.time() - t, 1)}
        (a.dir / f"view_{k}_{a.tag}.json").write_text(json.dumps(rec, indent=1) + "\n", encoding="utf-8")
        print(f"{k}: {rec['seconds']}s", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
