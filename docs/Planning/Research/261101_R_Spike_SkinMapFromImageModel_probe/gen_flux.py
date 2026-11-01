"""Disposable probe: FLUX.2 [klein] 4B (Apache-2.0) repaints each head render as a photographed person.
The front first; the other views take the front's result as a second reference so the person holds."""
import sys
import time

import torch
from diffusers import Flux2KleinPipeline
from PIL import Image

OUT = __import__("os").environ.get("PROBE_OUT", "/tmp/skinprobe")
TAG = sys.argv[1] if len(sys.argv) > 1 else "flux_a"
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 7
STEPS = int(sys.argv[3]) if len(sys.argv) > 3 else 4
YAWS = [int(v) for v in sys.argv[4].split(",")] if len(sys.argv) > 4 else [0]
SRC = sys.argv[5] if len(sys.argv) > 5 else "skin"
ANGLE = {0: "seen straight from the front", -40: "seen in three-quarter view, turned to the right", 40: "seen in three-quarter view, turned to the left", -80: "seen in right profile", 80: "seen in left profile"}

PERSON = ("a woman in her thirties with fair, lightly sun-touched skin (Fitzpatrick type III), "
          "a fully shaved bald head, completely shaved-off eyebrows (no eyebrow hair at all), eyes gently closed, "
          "no makeup, matte skin with no shine and no specular highlights")
SKIN = ("photorealistic human skin: visible pores, fine texture, subtle natural redness on the cheeks and nose, "
        "slight darker tone under the eyes, faint freckles, natural uneven skin tone")
LIGHT = ("soft, even, shadowless diffuse lighting from all sides, like a cross-polarised flat scan; plain dark grey background")
KEEP = ("Keep the existing skin colour and any marks already on it. Keep exactly the same head shape, face shape, pose, camera angle, framing and silhouette as the image; "
        "only change the surface so it looks like a real photograph.")
FRONT = f"Turn this 3D render into a high-resolution photograph of a person: {PERSON}. {SKIN}. {LIGHT}. {KEEP}"
SIDE = (f"Turn the first image, a 3D render, into a high-resolution photograph of the same person shown in the second "
        f"image, seen from the first image's angle: {PERSON}. Match the second image's skin colour, texture and marks "
        f"exactly. {SKIN}. {LIGHT}. {KEEP}")

pipe = Flux2KleinPipeline.from_pretrained("black-forest-labs/FLUX.2-klein-4B", torch_dtype=torch.bfloat16).to("cuda")
for y in YAWS:
    t = time.time()
    ren = Image.open(f"{OUT}/view_{y:+04d}_{SRC}.png").convert("RGB")
    imgs, prompt = [ren], FRONT.replace("photograph of a", f"photograph, {ANGLE[y]}, of a")
    g = torch.Generator("cuda").manual_seed(SEED)
    im = pipe(image=imgs, prompt=prompt, height=1024, width=1024, num_inference_steps=STEPS,
              guidance_scale=1.0, generator=g).images[0]
    im.save(f"{OUT}/view_{y:+04d}_{TAG}.png")
    print(y, round(time.time() - t, 1), "s", flush=True)
print("peak GB", round(torch.cuda.max_memory_allocated() / 1e9, 1))
