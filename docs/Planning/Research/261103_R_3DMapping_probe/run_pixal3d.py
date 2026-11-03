"""Run ComfyUI's official Pixal3D multi-view template on four prepared views, through the API.

Usage: python run_pixal3d.py <views dir with front/left/back/right.png> <tag> [fov] [seed offset]
The template's sampler, remesh and bake settings are kept exactly; only the input changes: the template
loads a turnaround sheet, crops each view to its own outline (ImageCropToMask) and removes the background;
here the four views arrive already framed on one shared axis, black background, so those nodes are dropped.
Saves two GLBs under ComfyUI's output/3d/<tag>_*: the textured mesh and the vertex-painted mesh.
"""
import json
import sys
import time
import urllib.request
import uuid
from pathlib import Path
import os

SERVER = "http://127.0.0.1:8188"
TEMPLATE = Path(os.environ["PIXAL3D_TEMPLATE"])   # <ComfyUI venv>/site-packages/comfyui_workflow_templates_json/templates/3d_pixal3d_multi_views.json
DROP = {"Note", "MarkdownNote", "Preview3DAdvanced", "Save3DAdvanced", "MeshToFile3D", "SaveImageAdvanced", "ImageCropV2",
        "LoadImage", "RemoveBackground", "ImageCropToMask", "LoadBackgroundRemovalModel", "RenderUVAtlas"}
WIDGET_TYPES = {"INT", "FLOAT", "STRING", "BOOLEAN", "COMBO"}


def get(path):
    return json.load(urllib.request.urlopen(SERVER + path))


def post(path, data=None, files=None):
    req = urllib.request.Request(SERVER + path, data=json.dumps(data).encode(),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))


def upload(path: Path, name: str):
    boundary = uuid.uuid4().hex
    body = (f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{name}\"\r\n"
            f"Content-Type: image/png\r\n\r\n").encode() + path.read_bytes() + \
           f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(SERVER + "/upload/image", data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    return json.load(urllib.request.urlopen(req))["name"]


def main():
    views, tag = Path(sys.argv[1]), sys.argv[2]
    fov = float(sys.argv[3]) if len(sys.argv) > 3 else 20.0
    seed_off = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    w = json.loads(TEMPLATE.read_text())
    links = {l[0]: l for l in w["links"]}
    info = get("/object_info")
    prompt = {}
    for n in w["nodes"]:
        if n["type"] in DROP or n.get("mode", 0) != 0:
            continue
        spec = info[n["type"]]
        order = spec.get("input_order") or {k: list(v) for k, v in spec["input"].items()}
        linked = {i["name"]: links[i["link"]] for i in n.get("inputs", []) if i.get("link") is not None}
        vals = list(n.get("widgets_values") or [])
        inputs = {}
        for sect in ("required", "optional"):
            for name in order.get(sect, []):
                s = spec["input"][sect][name]
                t = s[0] if isinstance(s[0], str) else "COMBO"
                opts = s[1] if len(s) > 1 and isinstance(s[1], dict) else {}
                is_widget = t in WIDGET_TYPES or isinstance(s[0], list)
                if t == "COMFY_DYNAMICCOMBO_V3" and vals:
                    key = vals.pop(0)
                    inputs[name] = key
                    opt = next(o for o in opts["options"] if o["key"] == key)
                    for sub in opt["inputs"].get("required", {}):
                        inputs[f"{name}.{sub}"] = vals.pop(0)
                elif is_widget and vals:
                    v = vals.pop(0)
                    if opts.get("control_after_generate"):
                        vals.pop(0)
                    inputs[name] = v
                if name in linked:
                    l = linked[name]
                    inputs[name] = [str(l[1]), l[2]]
        if vals:
            print(f"warn: node {n['id']} {n['type']} has {len(vals)} unused widget values {vals}")
        prompt[str(n["id"])] = {"class_type": n["type"], "inputs": inputs}
    # the four views, as framed
    cond = prompt["324"]["inputs"]
    cond["fov"] = fov
    for i, side in enumerate(("front", "left", "back", "right")):
        name = upload(views / f"{side}.png", f"tdm_{tag}_{side}.png")
        prompt[f"9{i}00"] = {"class_type": "LoadImage", "inputs": {"image": name}}
        cond[side] = [f"9{i}00", 0]
    for k in ("3", "12", "18", "23"):
        prompt[k]["inputs"]["seed"] += seed_off
    prompt["9500"] = {"class_type": "SaveGLB", "inputs": {"mesh": ["260", 0], "filename_prefix": f"3d/{tag}_textured"}}
    prompt["9600"] = {"class_type": "SaveGLB", "inputs": {"mesh": ["252", 0], "filename_prefix": f"3d/{tag}_painted"}}
    for k in [k for k, v in prompt.items() if v["class_type"] == "PreviewImage"]:
        prompt[k]["class_type"] = "PreviewImage"
    (Path(os.environ.get("PROBE_OUT", ".")) / f"prompt_{tag}.json").write_text(json.dumps(prompt, indent=1))
    pid = post("/prompt", {"prompt": prompt, "client_id": "tdm"})["prompt_id"]
    print("queued", pid, flush=True)
    t = time.time()
    while True:
        h = get(f"/history/{pid}")
        if pid in h:
            st = h[pid]["status"]
            print("status", st.get("status_str"), f"{time.time() - t:.0f} s")
            for m in st.get("messages", []):
                if m[0] in ("execution_error",):
                    print(json.dumps(m[1])[:3000])
            for nid, out in h[pid]["outputs"].items():
                print(nid, json.dumps(out)[:400])
            break
        time.sleep(5)


if __name__ == "__main__":
    main()
