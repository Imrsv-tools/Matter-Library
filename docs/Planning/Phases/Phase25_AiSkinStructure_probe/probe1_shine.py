"""P25 Pass 3 probe 1: is the gap the colour or the shine set? Throwaway; reuses look.py's machinery.
usage: uv run --directory <repo> python <this> <out> <D-map picture>"""
import json, re, sys
from pathlib import Path
import numpy as np
from PIL import Image
REPO = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(REPO / "tools" / "parity"))
import look  # noqa
from look import jobmod, rig, bc, drv

out = Path(sys.argv[1]).resolve(); dmap = Path(sys.argv[2]).resolve()
maps = out / "maps"; maps.mkdir(parents=True, exist_ok=True)
FLAT = maps / "flat_normal.png"; Image.fromarray(np.full((8, 8, 3), (128, 128, 255), np.uint8)).save(FLAT)
ONE = maps / "cavity_one.png"; Image.fromarray(np.full((8, 8), 255, np.uint8)).save(ONE)

def variant(art, folder, *, picture=None, flat=False, rough_bias=None, cavity_one=False):
    a = look._with_map(art, picture, (1, 1, 1), folder / "_c") if picture else look._relocated(art, art.path.read_text(), folder / "_c" / f"{art.name}.mtlx")
    t = a.path.read_text(encoding="utf-8")
    def sub(pat, val):
        nonlocal t
        t, n = re.subn(pat, lambda m: m.group(1) + val + m.group(2), t)
        assert n == 1, (pat, n)
    if flat:
        sub(r'(<input name="normal_map" type="filename" value=")[^"]*(")', str(FLAT))
        sub(r'(<image name="normal_tex" type="vector3">\s*<input name="file" type="filename" value=")[^"]*(")', str(FLAT))
    if rough_bias is not None:
        sub(r'(<input name="roughness_bias" type="float" value=")[^"]*(")', str(rough_bias))
    if cavity_one:
        sub(r'(<input name="cavity_map" type="filename" value=")[^"]*(")', str(ONE))
    return look._relocated(a, t, folder / f"{art.name}.mtlx")

art = jobmod.Article.read(jobmod.find_article("Skin_Tone34_Clean_Base_s001_v01"))
cast = rig.character_cast(art)
swap = [p for p in ("Body", "Lips") if p in cast and cast[p].name == art.name]
COLS = [("C", "C: Tone34 as served", {}),
        ("C_neutral", "C: flat relief, matte", dict(flat=True, rough_bias=0.25)),
        ("D", "D-map: Tone34's shine set", dict(picture=dmap)),
        ("D_flat", "D-map: flat relief", dict(picture=dmap, flat=True)),
        ("D_neutral", "D-map: flat relief, matte", dict(picture=dmap, flat=True, rough_bias=0.25))]
work = out / "work"; settings = []; columns = []; meshes0 = None
for sid, head, kw in COLS:
    v = variant(art, work / sid, **kw) if kw else art
    m, meshes = look.materials(cast | {p: v for p in swap}, work / f"{sid}_cast")
    if meshes0 is None: meshes0 = meshes
    assert [Path(x["file"]).read_bytes() for x in meshes] == [Path(x["file"]).read_bytes() for x in meshes0]
    settings.append({"id": sid, "materials": m}); columns.append((sid, head))
parts = bc.load_parts(); views = look.judge_views(parts)
sun, sky = drv.lights(); width = 1536
ujob = {"format": drv.LOOK_JOB_FORMAT, "width": width * look.SUPERSAMPLE, "out_dir": str(work / "raw"),
        "settle_frames": drv.SETTLE_FRAMES, "sun": sun, "sky": sky, "meshes": meshes0,
        "settings": [drv.warmup(settings)] + settings, "views": views, "look": look.look_lights()}
up = work / "look_job.json"; up.write_text(json.dumps(ujob, indent=1))
wanted = [(s["id"], v["suffix"]) for s in settings for v in views if (v["suffix"] == "__ear") == s["id"].endswith("__backlit")]
drv.run_runtime(drv.find_runtime(), up, work / "unreal.log", [work / "raw" / f"{i}{x}.pfm" for i, x in wanted])
for i, x in wanted:
    Image.fromarray(drv.srgb8(look.linear(work / "raw" / f"{i}{x}.pfm"))).save(out / f"{i}{x}.png")
for p in (work / "raw").glob("*.pfm"): p.unlink()
print(look.sheet(out, columns, 640, look.JUDGE_VIEWS))
