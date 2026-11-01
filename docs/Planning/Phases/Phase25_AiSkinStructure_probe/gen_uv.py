"""P25 re-discovery probe: Krea 2 Turbo img2img directly on the upright head island (UV space), several strengths.

    python3 -I <this> <out dir> <tag> <strength>[,<strength>…] [seed] [prompt key]
Uses the tracked workflow and API helpers of tools/converters/fit/gen_views_model.py; writes only under <out dir>.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "tools/converters/fit"))
import gen_views_model as g  # noqa: E402

OUT = Path(sys.argv[1]); TAG = sys.argv[2]
STRS = [float(s) for s in sys.argv[3].split(",")]
SEED = int(sys.argv[4]) if len(sys.argv) > 4 else 7
KEY = sys.argv[5] if len(sys.argv) > 5 else "uv"
PROMPTS = {
    "uv": ("A flat unwrapped UV texture map of a real human head's skin, from a photogrammetry scan of "
           "a real young woman about twenty, light warm skin between Fitzpatrick III and IV, shaved bald head, no eyebrow hair, no makeup. "
           "The face is laid out flat in the centre with the closed eyes, nose and lips, the scalp and the back of the head unrolled to each side, "
           "the ears as flat patches. Albedo only: even, shadowless, delit, no lighting, no highlights. "
           "Real unretouched skin: visible pores, fine vellus hair, small blemishes, tiny moles, faint freckles, uneven tone, "
           "slight redness around the nose and on the cheeks. Not a 3D render, not CGI, not painted."),
}
graph = json.loads(g.WORKFLOWS["krea"].read_text())
img = g.upload("http://127.0.0.1:8188", OUT / "uv_C.png")
for s in STRS:
    t = time.time()
    vals = {"IMAGE": img, "PROMPT": PROMPTS[KEY], "SEED": SEED, "STEPS": 8, "STRENGTH": s, "PREFIX": f"matter_p25uv_{TAG}"}
    png, pid = g.run("http://127.0.0.1:8188", g.fill(graph, vals))
    name = f"uv_{TAG}_s{int(s*100):02d}_seed{SEED}"
    (OUT / f"{name}.png").write_bytes(png)
    (OUT / f"{name}.json").write_text(json.dumps({"model": "krea", "workflow": g.WORKFLOWS["krea"].name, "seed": SEED, "steps": 8,
                                                  "strength": s, "prompt": PROMPTS[KEY], "source": "uv_C.png"}, indent=1))
    print(name, round(time.time() - t, 1), "s", flush=True)
