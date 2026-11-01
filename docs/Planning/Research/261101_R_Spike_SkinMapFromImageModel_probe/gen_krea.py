"""Disposable probe: Krea 2 Turbo repaints each head render (SDEdit img2img: the render's latent, noised
to STRENGTH, then the remaining Turbo steps). Krea2Pipeline is text-to-image only, so the start latent
and the sigma schedule are built here.
    gen_krea.py <tag> [strength=0.6] [seed=7]
The 26 GB bf16 transformer exceeds the 24 GB GPU: its blocks stream from CPU (group offload)."""
import sys
import time

import numpy as np
import torch
from diffusers import Krea2Pipeline
from PIL import Image

OUT = __import__("os").environ.get("PROBE_OUT", "/tmp/skinprobe")
TAG = sys.argv[1] if len(sys.argv) > 1 else "krea_a"
STRENGTH = float(sys.argv[2]) if len(sys.argv) > 2 else 0.6
SEED = int(sys.argv[3]) if len(sys.argv) > 3 else 7
STEPS = 8
YAWS = [0, -40, 40, -80, 80]
ANGLE = {0: "seen straight from the front", -40: "seen in three-quarter view, turned to the right",
         40: "seen in three-quarter view, turned to the left", -80: "seen in right profile", 80: "seen in left profile"}

PROMPT = ("A high-resolution studio photograph of a woman in her thirties, {angle}, with a fully shaved bald head, "
          "faint natural eyebrows, no makeup, neutral expression, eyes open. Fair, lightly sun-touched skin "
          "(Fitzpatrick type III) with visible pores, fine skin texture, subtle natural redness on the cheeks and "
          "nose, slightly darker skin under the eyes, faint freckles, natural uneven skin tone. Soft, even, "
          "shadowless light from the front; plain dark grey background. Sharp focus on the skin.")

pipe = Krea2Pipeline.from_pretrained("krea/Krea-2-Turbo", torch_dtype=torch.bfloat16)
pipe.transformer.enable_group_offload(onload_device=torch.device("cuda"), offload_device=torch.device("cpu"),
                                      offload_type="block_level", num_blocks_per_group=2, use_stream=True)
pipe.text_encoder.to("cuda")
pipe.vae.to("cuda")

vae = pipe.vae
mean = torch.tensor(vae.config.latents_mean).view(1, vae.config.z_dim, 1, 1, 1).to("cuda", torch.bfloat16)
std = torch.tensor(vae.config.latents_std).view(1, vae.config.z_dim, 1, 1, 1).to("cuda", torch.bfloat16)
sigmas = list(np.linspace(STRENGTH, 1 / STEPS, max(2, round(STEPS * STRENGTH))))

for y in YAWS:
    t = time.time()
    ren = Image.open(f"{OUT}/view_{y:+04d}_skin.png").convert("RGB")
    x = pipe.image_processor.preprocess(ren, height=1024, width=1024).to("cuda", torch.bfloat16)
    with torch.no_grad():
        z = vae.encode(x[:, :, None]).latent_dist.mode()          # (1, C, 1, h, w)
    z = ((z - mean) / std)[:, :, 0]                                 # (1, C, h, w)
    pipe.scheduler.set_timesteps(sigmas=sigmas, device="cuda", mu=1.15)   # Turbo's fixed shift, as the pipeline sets it
    s0 = float(pipe.scheduler.sigmas[0])
    g = torch.Generator("cuda").manual_seed(SEED)
    noise = torch.randn(z.shape, generator=g, device="cuda", dtype=z.dtype)
    lat = (1 - s0) * z + s0 * noise
    lat = pipe._pack_latents(lat, 1, z.shape[1], z.shape[2], z.shape[3])
    im = pipe(prompt=PROMPT.format(angle=ANGLE[y]), height=1024, width=1024, sigmas=sigmas, latents=lat,
              guidance_scale=0.0).images[0]
    im.save(f"{OUT}/view_{y:+04d}_{TAG}.png")
    print(y, "sigma0", round(s0, 3), round(time.time() - t, 1), "s", flush=True)
print("peak GB", round(torch.cuda.max_memory_allocated() / 1e9, 1))
