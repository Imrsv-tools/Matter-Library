# Spike — a whole skin map from an image model, on hm08 (2026-11-01)

**Mode:** disposable probe (`/research`, §Disposable probes), run on the machine with Unreal on the lead's word (RD-AIS-2 in [`261101_R_SkinMapsFromAnImageModel.md`](261101_R_SkinMapsFromAnImageModel.md)). It commits to nothing and ships nothing. **Mnemonic:** the parent's `AIS`.
**The question:** can an image model, told what to draw, make a **whole** head skin map in the library's layout that looks like a real person? (The lead: *"I want to prove the concept that that these system can generate really good looking skinmaps"*.)
**Answer: yes, for the head, in under a minute, with no training.** FLUX.2 [klein] 4B turned renders of hm08 into a convincing person whose features land on the mesh. Baked back into the 2048² map, it reads as a real face from angles the model never painted. Krea 2, the lead's preferred model (RD-AIS-1), is scripted but **not run**: its download needs a Hugging Face login this machine does not have.

**Pictures** (beside this doc):
- `…_sheet.jpg` (pass 2), today's `Skin_FitzpatrickIII` on the left and the probe's map on the right. Rows: front · three-quarter · a low three-quarter and a high profile, **the last two from angles no view was painted from**.
- `…_sheet_pass1.jpg`: pass 1, before the fixes below.
- `…_views.jpg`: the five pictures the model painted in pass 2.

**Shown how:** a diffuse render by the probe's own rasteriser: colour times a soft light, **no subsurface scattering, no shine maps, no hair or eyes**. It judges the colour map only. **It is not the look** in Blender, Storm or Studio. That sitting is owed (see Next).

---

## Method

1. **Render** hm08's head (every triangle above y = 0.5 m) with today's III map from five cameras: front, ±40°, ±80°, 1024², 24° field of view (`views.py`, `headrender.py`).
2. **Repaint the front** with FLUX.2 [klein] 4B in image-edit mode: the render is the reference, and the prompt asks for a photograph of a bald woman in her thirties, Fitzpatrick III, with realistic skin, flat light, *"keep exactly the same head shape … pose, camera angle, framing"* (`gen_flux.py`, 4 steps).
3. **Bake** it into the map (`bake.py`). Each texel in the head region is projected into the picture. It is kept if the z-buffer shows it visible, it is not near the silhouette or within 22 px of an eye opening, and it is weighted by how squarely it faces the camera (cos⁴). Its albedo is the picture divided by the render's own light. The baked region's mean is held to today's map's mean per channel (the library's calibration rule, RD-P21-3). The region is feathered into today's map.
4. **Progressive sides:** re-render ±40° with the map baked so far, repaint, bake; then ±80° the same way.
5. **Compare:** today's map and the probe's, rendered from four cameras, two of them new.

**Round trip** (the check that the projection is right): baking today's own renders back reproduces today's map to 0.65 % at the 95th percentile.

## Findings

- **F-AIS-11 — An edit model keeps the mesh's features in place.** An overlay of the front picture on the render shows the eyes, nose, mouth and ears on hm08's own. So the picture projects onto the layout **with no landmark fitting**. Each view took ~3 s; the whole head took under a minute; peak GPU memory was 18.6 GB.
- **F-AIS-12 — The side views must be made progressively.** Given the front's result as a second reference, the model **copied the front** at every angle (pass 1's first try). Re-rendering each side with the map baked so far, and giving only that render, kept both the angle and the person (`…_views.jpg`).
- **F-AIS-13 — What the model got wrong, and the fix for each** (pass 1 → pass 2):
  - **eyes painted bigger than the openings** (irises on the lids) → *eyes closed* in the prompt, and 22 px kept clear: fixed;
  - **a shine highlight on the forehead** → *matte, cross-polarised flat light*: fixed;
  - **eyebrows painted in** → the prompt *"no eyebrow hair"* was ignored. Still open. The character's brows are separate cards, so these would double. A brow mask in the bake is the next fix;
  - **a closed-lid lash line** over each eye opening: still open (mask, as above);
  - **a slight double lip line** at three-quarter angles, where the side views' lips sit a few pixels off the front's: still open (lower the side views' weight near the lips, or align);
  - **a faint seam at the neck**, where the head region ends: the feather is too short. Still open.
- **F-AIS-14 — The model's picture is darker than the library's tone, and redder at the cheeks.** Holding the mean took ×1.50–1.54 per channel. The maker's calibration absorbs that by design. The **cheek flush is strong** (a model's idea of "subtle redness"): the prompt sets it.
- **F-AIS-15 — The layout limits sharpness, not the model.** The face uses only part of hm08's ~500 px head region in a 2048² atlas (as F-SKM-12 found). Each painted view had more pixels on the face than the map can hold.
- **F-AIS-16 — The stored map clips where the picture runs bright** (the shoulders), because the probe kept the article's colour value. The maker raises that value until the brightest texel fits (`SkinMaps.md` §Calibration); a real bake would do the same.

## Not tested

- **Krea 2** (RD-AIS-1). `gen_krea.py` is written: img2img through Krea 2 Turbo, starting from the render's latent noised to a strength, because its diffusers pipeline is text-to-image only. Its 26 GB transformer streams from system RAM. **Waits on a Hugging Face login** (the licence is accepted once, on the model's page).
- **The look in a real renderer**, on the character with eyes, brows, hair and the shine maps, beside today's skin.
- **The body below the neck, other tones, other people.**
- **Whether the result holds across seeds and prompts.** One seed (7) was run.

## Reproduction

The scripts are beside this doc (`261101_R_Spike_SkinMapFromImageModel_probe/`). They read the library's maker (`tools/converters/fit/`) and never write to the repo. Pictures go to `$PROBE_OUT` (default `/tmp/skinprobe`).

    uv venv -p 3.12 /tmp/skinprobe-venv
    VIRTUAL_ENV=/tmp/skinprobe-venv uv pip install torch "git+https://github.com/huggingface/diffusers.git" \
        transformers accelerate safetensors pillow numpy scipy huggingface_hub
    PY=/tmp/skinprobe-venv/bin/python; P=docs/Planning/Research/261101_R_Spike_SkinMapFromImageModel_probe
    $PY -I $P/views.py                                         # five renders with today's III map
    $PY -I $P/gen_flux.py b 7 4 0 skin                         # front (downloads FLUX.2 [klein] 4B, 16 GB)
    $PY -I $P/bake.py b 0 --calibrate --inputs                 # bake; render the sides with it
    $PY -I $P/gen_flux.py b 7 4 -40,40 in_b
    $PY -I $P/bake.py b 0,-40,40 --calibrate --inputs
    $PY -I $P/gen_flux.py b 7 4 -80,80 in_b
    $PY -I $P/bake.py b 0,-40,40,-80,80 --calibrate            # map_b.png, sheet_b.png
    # Krea 2 instead of FLUX (after `hf auth login`): gen_krea.py <tag> [strength] [seed], same views and bakes

The probe's environment (venv, the 15 GB model cache, its pictures) sat in the session's scratch and is deleted with it.

## Next

1. **Krea 2 on the same views** once a Hugging Face login exists. Compare its sheet with this one.
2. **The masks** for brows and lids, the lip weighting and a longer neck feather, then a second seed.
3. **The lead's look on the character** in the lead's Blender, beside today's skin. That is the judgement this sheet cannot give.
