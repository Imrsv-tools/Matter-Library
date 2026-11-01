# Phase25 — AI Skin Structure

**Status:** IN EXECUTION (Pass 2's Brief, opened 2026-11-01 by the lead's *"/execute Phase25"* at `c6b890d`). *Before:* BRIEF READY (re-discovery, Pass 2, 2026-11-01, opened by the lead's *"/discovery Phase25"* after 25.1.8). *Before:* IN EXECUTION from `3df2ce1` (25.1, the project-and-bake route, sat twice and rejected at 25.1.8); BRIEF READY (Pass 1); SEEDED (2026-11-01), split out of Phase24 on the lead's *"Split and seed"* (RD-OVS-6). It runs against Phase24's judge.
**Lane:** `build` (§Risk lane).
**Measured at:** `28b3c02` (Pass 2), on **the machine with Unreal** (Unreal 5.8 at the path `unreal/build.sh` takes as `UE`; the official Blender 5.2.2 as `MATTER_BLENDER`; `unreal-runtime-v7` pinned).
**Seeded from:** [`../Research/261101_R_SkinMapsFromAnImageModel.md`](../Research/261101_R_SkinMapsFromAnImageModel.md) (RD-AIS-1, RD-AIS-2) · [`../Research/261101_R_Spike_SkinMapFromImageModel.md`](../Research/261101_R_Spike_SkinMapFromImageModel.md) (the views route, now superseded) · [`../Research/261101_R_OneValidatedSkin.md`](../Research/261101_R_OneValidatedSkin.md) (OVS-3; RD-OVS-1 … 6) · [`Complete/Phase24_OneValidatedSkin.md`](Complete/Phase24_OneValidatedSkin.md) (the judge, `Tone34`, its pigment fields) · Pass 2's probe, [`Phase25_AiSkinStructure_probe/`](Phase25_AiSkinStructure_probe/) (F-P25-7).

## Outcome

**An image model paints the head's whole skin map in the body's own layout, as one picture with no views stitched together, and it is judged beside the scanned skin and Phase24's skin on the same body. If it wins, the maker turns it into a calibrated skin structure.**

*(Rewritten at Pass 2. Pass 1's Outcome said the model's person was "projected onto the body"; the lead rejected that route at 25.1.8: *"you are cuting pasting, patching, matching, blending, when I think we should be trying to figure out how it can generate a full map"*. The claim is still the face, this subject, this tone (OVS-7).)*

---

## The Brief

### What this phase builds, in one paragraph

**The model paints the map itself.** hm08's head is one island in the atlas: an unwrapped face with the scalp rolled out to each side and the ears as pads. Krea 2 already knows that picture: given the island at the subject's tone, it repaints it as one coherent unwrapped photograph of a real person, with the features where hm08's layout has them and no seams between views, because there are no views (F-P25-7, measured this pass). 25.1 makes that a library tool: cut the island, have the model repaint it fully while a constraint holds the fit: a geometry control (the lead's Krea edit LoRA route, F-P25-8), or one warp of the model's free face onto hm08's features (F-P25-11), because strength cannot hold it; put it back at the model's size (2K; 8K waits for the fit, RD-P25-13). Click 1 shows it beside A, C and 25.1's views-route D. The winner then goes through the maker as a structure (25.2) and, if it wins, into the set (25.3), as Pass 1 planned. **Only the colour varies:** D wears `Tone34`'s shine set, nails, body and every held-fixed piece.

### The routes, compared (Pass 2)

*The lead after 25.1.8 named routes 1–3 (*"a KreaImage Edit 2 Lora … rendering onto a 3D object in compfy … deconstruct from one if its finished products … or ???"*); the run that recorded them added 4; this pass added 5 and probed it.*

| # | Route | Verdict | Why |
|---|---|---|---|
| 5 | **Paint the head island in UV space** (the model repaints C's own island, at the subject's tone) | **Taken** (RD-P25-9) | Probed: one coherent person in hm08's layout, untrained, 13 s; no view seams (F-P25-7). Its defects are a conditioning and resolution problem, which 1 and the detail pass address. |
| 1 | **A Krea 2 edit LoRA** | **Taken as route 5's conditioner** (RD-P25-10) | Several exist under Krea's own licence (already accepted, RD-AIS-1), one is non-commercial (F-P25-8). An "aligned" source or a geometry control holds the features where strength cannot (F-P25-11: from 0.75 the model draws its own face, cued or not). |
| 2 | **Texture the mesh inside ComfyUI** (multi-view tools) | Not taken (RD-P25-11) | Every tool found either projects views and blends them (the rejected route, done jointly) or re-unwraps the mesh. The best known, Hunyuan3D Paint, is licensed with no grant in the EU, the UK or South Korea and bars using its outputs to improve other models (F-P25-9). |
| 3 | **Fit to the model's own finished face** | **Taken in UV space as conditioner (d)** (RD-P25-10); not taken as a photo projected onto the mesh (RD-P25-11) | Fitting hm08 to a photograph projects again, and the mesh is fixed (RD-SKM-1). But the model's free face at 0.9 is its best skin, one picture already in the layout, off only in where its features sit (F-P25-11): one smooth 2D warp in UV space moves them onto hm08's, with no view and no seam. |
| 4 | **Train a layout LoRA** (the AvatarTex method) | **Fallback** (RD-P25-12) | The published whole-map method; its weights are not released (F-P25-9). The probe shows the base model already knows an unwrapped face, so training is needed only if no conditioner holds the features. |

### Rides on

| `CoreMechanisms.md` row | What in this phase rides it | The peer we follow |
|---|---|---|
| 1 — a body map larger than 2048 inside the machine's memory | the island put back into the 8K atlas (25.1), D's colour composed at 8K from an outside field (25.2) | `tools/converters/fit/gen_synth_skin.py` `compose_banded` (opened at Pass 1): the atlas in bands of 512 rows |

The island cut and the UV-space generation are new; the inversion is new (F-P25-1).

### First human test

**Where:** the machine with Unreal, where every tool the clicks compare has run (`LOCAL_DELTAS.md` §Two machines).
- **The surface:** the library's look view (`tools/parity/look.py --judge`, the pinned runtime), Phase24's nine fixed views at ~1 m and ~40 cm (RD-P24-4), `--width 1536`. A is the scanned bar (`--bar`, made locally, never committed: RD-P23-10). C is `Skin_Tone34_Clean_Base_s001_v01` as served. D is an outside colour picture worn by `Tone34`'s article with its shine set (`look.py --candidate`, built at 25.1). The agent renders, measures, opens the sheet with `xdg-open` and puts its path in the handback. **Every picture shown to the lead is at its native resolution, one file per view, never a shrunk contact sheet** (the lead: *"the images you show me are too low res for the quaklity we are starting to look into"*). Never Blender (RD-CMT-4).
- **The ruler:** sat at Phase24's click 1 (*"A reads real, B reads fake"*); not re-sat.
- **The reference the lead has already judged:** 25.1's views-route D (`kr50`, second showing): *"It is better"* than C, rejected for its route and its seams. Click 1 is meant to close the gap from it to A **without** its seams.
- **Can the surface show it?** The close-ups are 0.04 mm a pixel; an 8K texel on the face is ~0.1 mm. The model paints the island at its largest size, about 2 MP (Krea's range is 1–2K, F-P25-10): **0.36 picture pixels per 8K texel, ~0.28 mm a pixel**, so the plain picture is ~3× softer than C's texels and ~7× the close-up's pixel. **Click 1 is judged at that size anyway** (RD-P25-13, the lead: work at 2K or 4K until the fit is solved): it answers the fit and the skin, and softness in the close-ups is expected, named in the handback, and not the question. The fixture is the subject itself (one tone, one person, RD-OVS-1).

1. **Click 1 — the model's whole map beside the bar (25.1).** A · C · **D-views** (25.1's `kr50`, already judged) · **D-map** (route 5, at the model's size, RD-P25-13).
   - *Judge:* does D-map read as real as A, and does it lose the seams D-views had (the neck and forehead gradient lines, the ears)? Part by part: the eyes, cheeks, nose, lips, hairline, ears, neck.
   - *What the lead can say after:* *"D-map reads real and has no lines; it beats D-views"*, or *"it is softer / it moved the lips / it painted shadows"*.
   - **If D-map loses to D-views or C in every view,** 25.2 does not start on the agent's word (RD-P25-6).
2. **Click 2 — the structure (25.2).** As Pass 1 wrote it: shown only if the inversion changes the look by more than 1 ΔE in a face region.
3. **Click 3 — the set with D, served (25.3, only if D won).** As Pass 1 wrote it.

**Reconciled click by click:**
- Click 1 needs only 25.1: the island cut and put back, the fit candidate chosen, `look.py --candidate` (already built). D-views is on disk (`library/parity/P25_Views/albedo_kr50.npy`, git-ignored); its picture is remade with `project_views.py bake … --picture` if `D_kr50.png` is stale.
- Clicks 2 and 3 are unchanged from Pass 1.
- **§In now, walked:** every row names its step.

**Not a click: Studio and the headset** (RD-OVS-4, F-P25-6).

### In now

| Item | Step |
|---|---|
| **The island tool** under `tools/converters/fit/`: cut `Tone34`'s head island from the 8K atlas at the subject's tone, upright, at the model's size, with its mask; put a picture back on the island, held to the subject's face core (`SUBJECTS["Tone34"]["held"]`), C elsewhere (the probe's `prep.py` / `back.py`, F-P25-7) | 25.1 |
| **The fit, held by a constraint chosen by measurement** (RD-P25-10): a geometry control (a Krea edit or control LoRA under Krea's licence, fed hm08's feature lines); FLUX.2 [klein]'s own edit; or the model's free face warped once onto hm08's in UV space. The gate: lips and lids land on hm08's, no brows painted, the skin fully repainted | 25.1 |
| **The detail pass to 8K in UV space** (RD-P25-13) | after the fit passes and click 1 is sat |
| **The prompt** that reads as a real person's unwrapped skin, with no shadows painted in (F-P25-7: the sockets came out dark) | 25.1 |
| **The record** of every picture: model files, LoRA, seed, prompt, steps, strength (RD-P25-7) | 25.1 |
| **The inverse of the skin model** and **the maker taking an outside field**, the remake-identical proof (unchanged from Pass 1; F-P25-1) | 25.2 |
| **If D won:** the lead's re-ruling; `Tone34`'s colour made from D; provenance (*AI-assisted*, the model and LoRA named); the picture kept as its source (RD-P25-8); thumbnails; the dev install re-served | 25.3 |
| **Written down:** `SkinMaps.md` (an AI-painted map: how it is made, and whether one is accepted, in the lead's words); the AIS research's Q-AIS-1 row and a pointer to Pass 2's routes | at the close |

### Not now

- **The body from the model:** the head island only (RD-P25-1). The body has no bar (OVS-7). The body islands painted the same way are the natural next unit.
- **Other tones, people and ages:** *Variety*, after.
- **A raw AI map shipped as is:** never (RD-SYN-1); D-map is a comparison until 25.2 makes it a structure.
- **Routes 2 and 3** (RD-P25-11); **training a layout LoRA** unless no conditioner passes (RD-P25-12).
- **The non-commercial identity-edit LoRA** (F-P25-8).
- **The shine set and nails from the model:** a model draws colour only (RD-P25-3).
- **The views route's bake** (25.1.1–25.1.8): kept in the tree, not the route (RD-P25-14).
- **A creator-run generator** (Q-AIS-1's framing); **training on photos of people** (Q-AIS-2).

### The reuse check

*What does the stack already provide, and which contracts are touched?*
- **The judge exists:** `look.py --judge`, `--bar`, and `--candidate` (25.1's commit `12343f5`).
- **The generation client exists:** `gen_views_model.py`'s ComfyUI client (`upload`, `fill`, `run`, standard library only) and its tracked Krea workflow; the probe drove it unchanged. Its view table and prompt are the views route's.
- **The head's texels and masks exist:** `project_views.head_fields` (the head's texel indices, positions, and the face, lips, lids, brow and ear masks at 8K), cached; the probe cut the island from them. Its renderer is the agent's quick check on the mesh (the probe's sheet).
- **ComfyUI's model folder** has Krea 2 Turbo and FLUX.2 [klein] 4B (F-P25-5). **A Krea edit LoRA needs its node pack** installed into the lead's ComfyUI (custom nodes) and the LoRA file in the shared model folder: a system change, logged in the workstation's change log.
- **The maker** (`gen_synth_skin`, `gen_skin_maps --fields`) and its 8K bands: as Pass 1 (25.2).
- **No input added, no master changed, no new Unreal runtime owed** (`base_color_map` carries D).
- **Contracts touched:** none of the article's. `SkinMaps.md` §Sources (*"A fully AI-made map is not accepted"*) only by the lead's re-ruling at 25.3.

### Decisions that bind

*One authoritative copy. Rulings are quoted where they are the authority.*

**Carried rulings:**
- **RD-AIS-1** (the lead, 2026-11-01): Krea 2 first; the revenue limit is no obstacle (*"WELL under 1M … I would lean towards KREA2 … but I am open to whatever"*). FLUX.2 [klein] 4B beside it.
- **RD-AIS-2:** prove that whole maps can look really good (*"I want to prove the concept"*).
- **The route (25.1.8, the lead):** *"figure out how to wrap a realistc skin on a 3D model … trying to figure out how it can generate a full map"*; not *"cuting pasting, patching, matching, blending"*.
- **RD-OVS-1, -2, -5, -6:** the bar's tone; 8K; the lead supplies the models; two phases.
- **OVS-3 (OMF's input, not a ruling):** an AI skin enters as a structure, and a win is put to the lead as a narrow re-ruling.
- **RD-SKM-1** (hm08 is the mesh) · **RD-SKM-5, RD-SYN-1:** no whole AI map ships; a whole AI map is a judged comparison only · **RD-SKM-2:** no photograph of a person in what ships · **RD-P23-10:** the bar stays local · **RD-RO-2:** CC0.
- **RD-CMT-4:** a character material's look is judged in the Unreal look view, never Blender.
- **Phase24's judge as it sat:** RD-P24-4, RD-P24-5, RD-P24-3, the subject `Tone34` (RD-P24-1, -8).
- **Pre-release, no versioning** (`AI_WorkingAgreement.md` §Settled practices).

**Decided at Pass 1 and still standing:** RD-P25-1 (the head; the body is C's, joined in pigment at the neck) · RD-P25-3 (only the colour varies) · RD-P25-6 (click 1 can stop the phase) · RD-P25-7 (generation drives the lead's ComfyUI over its API; the project gains no dependency; ComfyUI started by the agent only if not running, stopped by PID if started) · RD-P25-8 (if D wins, its picture is its source, in LFS with its record; now one picture, not views).
**Superseded at Pass 2:** RD-P25-4 (views at the model's size, close cameras) and RD-P25-5 (two D rows from the same views; Krea by img2img with the overlay gate): there are no views. **RD-P25-2 (the lips are the maker's)** now holds for 25.2's structure only: at click 1 D-map is shown as the model painted it, lips included, because masking them in is the patching the lead rejected; whether its lips stand is judged.

**Decided here, unless the lead says otherwise:**
- **RD-P25-9 — The route is the head island painted in UV space.** The model repaints C's head island, cut upright at the subject's tone, as one picture; the picture goes back on the island, held to the subject's face core. Why: it is the only route found that gives a whole map in hm08's own layout from the model with no views, no projection and no training, and the probe showed it works untrained (F-P25-7).
- **RD-P25-10 — The fit is held by a constraint, not by strength, and the constraint is chosen by measurement.** Plain img2img with cues is out (F-P25-11). Three candidates, the same island, prompt and seed: **(b)** a geometry control: a Krea 2 edit, control or inpaint LoRA under the Krea 2 Community License, given the island with hm08's feature lines (lips, lid slits, nostrils, ear rims, drawn from `head_fields`' masks) as an aligned source or edge map (NK2E and its canny LoRA, `krea2-inpaint-edit`, `krea2-anypaint`; licences read again at install); **(c)** FLUX.2 [klein] 4B's own edit (Apache-2.0); **(d)** the model paints freely at the strength where its skin is best (0.9 in the probe), then **one smooth 2D warp of that picture in UV space** moves its eyes, brows' line, nose, lips and ears onto hm08's (landmarks found on the picture, hm08's from its masks; a thin-plate warp, NumPy) and nothing is blended. **The gate:** in UV space, the painted lips' and lid lines' centroids within **1 mm** of hm08's masks, no brows painted, the skin repainted fully (strength ≥ 0.75, or (d)). (d) also needs: no feature stretched visibly by the warp (the agent's look at the warped picture, measured as the warp's largest local scale). The agent runs it; the winner goes to click 1. If none passes at a strength that repaints the skin, RD-P25-12 applies and the lead is asked.
- **RD-P25-11 — Routes 2 and 3 are not taken.** Route 2's tools are the rejected route done jointly, or re-unwrap hm08 (whose layout is fixed), and its best-known tool's licence does not apply in the EU, the UK or South Korea, which a public CC0 library's tool cannot have. Route 3 is projection again.
- **RD-P25-12 — A layout LoRA is the fallback, trained on the maker's own maps only.** Only if no conditioner passes RD-P25-10's gate: the method the literature uses (F-P25-9). Its data is the maker's hm08 maps (any number, one per seed), never photographs of people (Q-AIS-2 stays unopened). The lead is asked before training starts (it is new work, hours of GPU).
- **RD-P25-13 — 2K, at most 4K, until the fit is solved; the detail pass to 8K waits.** The lead, 2026-11-01: *"Until we solve this sizing stuff we can work in 4 or even 2k"*. *(Read as: the fit is the question; resolution comes after it.)* The island is painted at the model's size (~2 MP; 4K only where a candidate needs it) and put back as made; 25.1 does not build the detail pass. **Once the fit passes and the lead has looked at click 1,** the pass runs as follows, as its own step or the start of 25.2. The model's picture of the island is ~2 MP; 8K needs ~11× the pixels on the face. The pass is the model's own: the island upsampled to 8K and repainted in overlapping tiles at a low strength, the same prompt, the tiles joined by the sampler (a ComfyUI tiled upscale), not by our blend. Execute measures how far the tiles drift from the whole picture's colour (per face region, against the 2 MP picture upsampled) and shows the lead the plain picture too if the pass changes the look.
- **RD-P25-14 — 25.1's views-route code stays in the tree, unused by this route.** `look.py --candidate` and `gen_views_model.py`'s client are reused; `project_views.py`'s renderer and `head_fields` are reused; its bake is not the route. Whether the bake is retired is decided at the close, by whether anything still calls it.

### Risk lane — `build`

The controls this phase touches, each read on 2026-11-01:
- **The maker** (25.2): as Pass 1 — a new optional input; every committed skin map is its fingerprint; `Tone34` and the 18 skins must remake pixel-identical without the field.
- **`look.py`:** `--candidate` exists (`12343f5`); no change expected. Writes only under its output folder (RD-P23-10).
- **What enumerates the trees this phase adds to:** new tools under `tools/converters/fit/` are enumerated by no gate. **The probe folder** `docs/Planning/Phases/Phase25_AiSkinStructure_probe/` is read by nothing (only a docstring names `docs/Planning/Phases`; grepped `tools/` this pass), as Phase10's probe files are. A D win changes `SkinTone34_basecolor_sUKN.png` (the recipe gate G8, thumbnails, `serve_to_stage.py`; Learnings G2).
- **The lead's ComfyUI** is shared by the lead's other projects: a node pack is installed through its manager or its `custom_nodes` folder, the change logged in the workstation's change log with its revert, and the LoRA's licence quoted in the ledger before its first run. **Before each model run:** `ps -ef | grep "[U]nrealEditor"`; ComfyUI's queue empty (`/queue`); free memory read. **Before a look-view launch:** ComfyUI's cached models released with `POST /free` (`unload_models`), which does not stop the server (P25 retro item 4).
- **The masters and the runtime:** untouched.
- **The one irreversible risk is publication:** the repo is public. The bar is never committed nor its path written. D's picture is committed only on a D win and the lead's re-ruling.
- **Baseline:** `run_all.py` at `180e00b` (Pass 1: 18/18 PASS); 25.1.7 recorded 18/18 PASS after its tools. No change under `blender/addons/` or `tools/conformance/`.

Nothing here is authorization, secrets, a destructive migration or the public edge.

### Step list

- **25.1 — The model paints the map.** The island tool; the three fit candidates through RD-P25-10's gate; the prompt; D-map on the atlas at the model's size. **Click 1** (A · C · D-views · D-map).
- **25.2 — D as a structure.** As Pass 1: the skin model's inverse; the maker composing `Tone34` from D's field on the head and C's on the body at 8K, the lips the maker's (RD-P25-2); the remake-identical proof; the round trip. **Click 2**, only if the structure changes the look.
- **25.3 — If D won: the set with D, served.** As Pass 1. **Click 3.**

Time to the first click: the probe's four scripts become one tool, plus the warp (a few hours); a node pack and a LoRA installed (minutes); three candidates × a few strengths at ~13 s a picture; one look-view launch. The detail pass is not before click 1 (RD-P25-13).

### Compact build map

- **25.1:**
  - `tools/converters/fit/paint_uv.py` (new, NumPy): `cut` (the island from the subject's atlas at its held tone, upright, at a given size, plus its mask and C's lip/lid masks in the same frame; the probe's `prep.py`, with the island chosen from `head_fields` by its atlas columns, `_c >= 5100 & _r < 7150` in the probe: replace that literal with the island's own connected component) · `put` (a picture back on the island, held to the face core; the probe's `back.py`) · `lines` (hm08's feature lines in the island's frame, for a geometry control) · `warp` (conditioner (d): landmarks on the picture onto hm08's, one thin-plate warp, NumPy) · `gate` (the lip and lid centroids in mm, RD-P25-10). Writes under git-ignored `library/parity/P25_*`.
  - The generation: `gen_views_model.py`'s client, called on the island (a `--picture` mode, or a small sibling script); a tracked workflow per conditioner under `tools/converters/fit/comfy/` (the LoRA's file named, never the model folder's path).
  - *After the fit passes (RD-P25-13), not before click 1:* the detail pass: a tracked tiled-upscale workflow (ComfyUI's own tiled sampling, or a node pack's, licence read), on the cut island at 8K.
  - Evidence before click 1: the gate per conditioner and strength; the probe's mesh check (`project_views.py render … --albedo`) for the winner; D-map per face region against A and C (Phase23's profiles, as Phase24 measured); the detail pass's drift.
- **25.2** (unchanged from Pass 1):
  - `gen_synth_skin.Lut.inverse(ratio, so2, depth)`: per texel, the (melanin, blood) whose colour over the base matches, by the table's own grid (a nearest lookup refined by one interpolation step); out-of-gamut texels reported, not clipped silently.
  - `compose` / `compose_banded`: an optional outside field (`field=`) replacing `mel` and `bld` where its weight is 1, C's own elsewhere, joined in log-pigment; the lips term unchanged.
  - `gen_skin_maps.py --subject Tone34 --pigments DIR`: D's field in; the map and its stats out to a scratch folder unless D won.
  - Proof: without `--pigments`, `Tone34` and the 18 skins pixel-identical (in-process). The round trip, D against click 1's picture per region (ΔE).
- **25.3 (only on a D win):** `SkinTone34_basecolor_sUKN.png` from D; the provenance row (`made: ai-assisted`, model, LoRA, revision, seed, the picture's hash); the picture tracked (RD-P25-8); `make_thumbnails.py`; `serve_to_stage.py --no-restart` (check for a running Stage daemon first; close what you start); `SkinMaps.md` §Sources in the lead's words.
- **Tests:** `run_all.py` per step; the remake-identical proof; one real-path smoke per click, which is the look view. No new gate.

### Open for the lead

*None.* RD-P25-9 … 14 are decided unless the lead says otherwise.

---

## Findings (discovery Pass 1, 2026-11-01)

- **F-P25-1 — The maker has no way in for an outside field, and its skin model runs one way.** `pigments=` on `compose`, `compose_banded` and `gen_skin_maps.py --fields` is an output (RD-P24-6). The colour is `tone × lut(melanin, blood, so2) × (1 − depth × reach) / lut(m0, blood0, 0.8)`, then held on the body (`compose`'s tail). So an inverse solves each texel's colour-over-tone for melanin and blood at that texel's oxygenation and depth, on the same table (`Lut`); it does not exist yet.
- **F-P25-2 — At 8K the views, not the layout, cap D's sharpness.** The spike's views are 1024² at 0.78 m with a 24° lens: 0.33 m across, **0.32 mm a pixel** on the face. FLUX.2 [klein] draws up to 4 MP (2048², its maker's specification), **0.16 mm**; a close camera at ~0.45 m gives **~0.09 mm**. `Tone34`'s 8K texel is ~0.1 mm, and the judge's close-ups show 0.04 mm a pixel. So the spike's views would make D ~3× softer than C, visibly, in the close-ups; F-AIS-15 (*"the layout limits sharpness"*) held at 2048 and reverses at 8K. RD-P25-4.
- **F-P25-3 — Krea 2 is not an edit model.** Its diffusers pipeline is text-to-image (the spike). Image-conditioned editing exists only as community ComfyUI LoRAs (a Krea 2 identity edit and a general edit LoRA; another node whose own page warns Krea 2 *"is not an edit model"* and *"alters the image sometimes"*); the official node takes a style reference only. Their licences are unread. So the spike's noised-latent start is the plain route, and Krea must re-prove that the features stay on hm08's (F-AIS-11). RD-P25-5.
- **F-P25-4 — Phase24 left D's footing in place.** C's 8K melanin and blood fields are local (`library/parity/P24_Fields/`, git-ignored, from `gen_skin_maps.py --subject Tone34 --fields`), and so is the solver that fitted `Tone34` to the bar (`library/parity/P24_Solver/`). `look.py --reference` draws an outside picture on a skin with its shine set, but `reference_casts` refuses any non-Fitzpatrick skin.
- **F-P25-5 — The models, as supplied (the lead's AIModels session, 2026-11-01, during this pass).** Krea 2 **Turbo** arrives as ComfyUI single-file FP8 from Comfy-Org's repack (the transformer `krea2_turbo_fp8_scaled`, 12.2 GiB, whole by the time this pass committed; the stock `qwen3vl_4b_fp8_scaled` text encoder and a third-party abliterated one beside it; the Qwen-Image VAE), each checked against its published hash, in **a shared model folder on a local drive** that ComfyUI reads (the lead: *"we are installing comfyui and various models in a share location"*). These are ComfyUI files, not diffusers, so the spike's `gen_krea.py` does not load them (RD-P25-7). The repack downloaded with no login, so no Hugging Face login is needed. **FLUX.2 [klein] was then fetched by this session on the lead's word** (*"You can grab flux and put it in the share models folder if you like"*): Comfy-Org's ComfyUI split of the Apache-2.0 4B at revision `5b3abca` (the distilled `flux-2-klein-4b`, the `qwen_3_4b` text encoder, `flux2-vae`), each renamed into place only after its sha256 matched the published one. In FP8 Krea's transformer is about half the GPU's memory, so it runs on the GPU (the spike's bf16 copy would not have fit).
- **F-P25-6 — The consumers since the seed (fetched 2026-11-01):** the platform's skin phase lists this phase as *"Nothing new for the platform beyond the judge"*, and its first sitting uses Phase24's judge; OMF's newest input (the character model) is addressed to the platform. **Nothing addressed to this library changes this phase.**


## Findings (discovery Pass 2, 2026-11-01)

- **F-P25-7 — Krea 2 paints hm08's head island as one unwrapped person, untrained (probe, this pass).** C's head island (atlas rows 1492–7150, columns 5252–8140 at 8K), set to the subject's held tone and stood upright, went through Krea 2 Turbo's tracked img2img workflow (`comfy/krea2turbo_img2img.json`, 8 steps, seed 7) at 2048 × 1040 with a prompt naming *"a flat unwrapped UV texture map of a real human head's skin, from a photogrammetry scan"*; ~13 s a picture. Sheets: [`Phase25_AiSkinStructure_probe/uv_face.jpg`](Phase25_AiSkinStructure_probe/uv_face.jpg) (the face in UV space: C, then strength 0.45, 0.6, 0.75, 0.9) and [`…/heads.jpg`](Phase25_AiSkinStructure_probe/heads.jpg) (on the mesh, the probe's diffuse renderer, rows C · 25.1's D-views `kr50` · 0.45 · 0.6; front, ¾, profile, two close-ups).
  - **What held:** at 0.45 and 0.6 one coherent person, with pores, freckles, vellus texture and redness; the eyes on the lid openings, the nose on the nose; **real ears drawn on the ear pads**, which read as ears on the mesh; **no seams on the face**, because there are no views.
  - **What did not:** the features drift with strength: against hm08's lip and lid masks in UV space, the lips **~1 mm at 0.45, ~6 mm low at 0.6**; from 0.75 the model draws its own face (lips ~18 mm high, lash line ~7 mm off, brows painted; F-P25-11). *(First recorded as "+7 mm at 0.45": that measured against C's pale lips, whose redness sat 23 px above their mask; corrected the same pass.)* **Socket and nose shading painted in** (dark under the eyes), which real light would double. **A line where the head island meets the body's neck** (the island edge; C's body is untouched). **Softness:** 0.36 picture pixels per 8K texel.
  - **Not tested:** the look view; any conditioner but plain img2img; seeds other than 7; the island at more than 2 MP.
  - **Reproduce** (paths from the repo root; `<out>` any scratch folder; ComfyUI running on its default port):
    `uv run python -I docs/Planning/Phases/Phase25_AiSkinStructure_probe/prep.py <out> 2048` ·
    `python3 -I docs/Planning/Phases/Phase25_AiSkinStructure_probe/gen_uv.py <out> a 0.45,0.6,0.75,0.9 7` ·
    `uv run python -I docs/Planning/Phases/Phase25_AiSkinStructure_probe/back.py <out> uv_a_s45_seed7 uv45` ·
    link `library/parity/P25_Views/geom_*.npz` into `<out>/render/`, then `uv run tools/converters/fit/project_views.py render <out>/render f000,f-40,f-80,c000,c-35 --albedo uv45`.
- **F-P25-8 — Krea 2 edit LoRAs (web, 2026-11-01).** Krea has no open-weight edit model; editing is on its hosted platform only. The community ones:
  - **NK2E** (`nynxz/NK2E`, in-context edit, source + instruction; its card: *"weaker at recoloring large regions"*) · **`Cierpliwy/krea2-inpaint-edit`** (masked inpaint, the rest unchanged) · **`yijunwang2/krea2-anypaint`** (any-mask edit on Turbo; its reference encoded at 384 px at most): each under the **Krea 2 Community License**, the licence RD-AIS-1 already accepted (worldwide grant, §2.1).
  - **`conradlocke/krea2-identity-edit` V2** has the property route 5 wants most (an *"Aligned"* reference *"pinned to the output layout"*), but V2 is *"free for personal and non-commercial use … Commercial use needs a license from me"*: **not usable**. Its v1–v1.2 are under Krea's licence (unread).
  - **ostris's AI Toolkit** trains Krea 2 reference-image (edit) LoRAs (since 2026-07-04), with a ComfyUI node pack: the tool for RD-P25-12 if it comes to that.
  - **FLUX.2 [klein] 4B** edits from references natively (Apache-2.0). It reframed close-up views at 25.1; on a flat island it is untested.
  - VRAM is stated by none; each LoRA is under 1 GB beside the FP8 model. *Unverified:* every card's dates; the identity-edit page on Civitai (refused).
- **F-P25-9 — Texturing a mesh in ComfyUI, and generating in UV space (web, 2026-11-01).**
  - **Hunyuan3D Paint 2.0 / 2.1** (and kijai's ComfyUI wrapper): the licence's Territory is *"the worldwide territory, excluding the territory of the European Union, United Kingdom and South Korea"*, its preamble says it *"DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA"*, and §5(b) bars using outputs *"to improve any other AI model"* (`tencent/Hunyuan3D-2.1` LICENSE). Its own pipeline re-unwraps with xatlas. Later versions are hosted only.
  - **StableGen** (GPL-3.0, a Blender add-on driving ComfyUI) keeps the mesh's UVs and bakes to 8192, but projects views one after another and blends them: the rejected route, more consistent. No Krea support.
  - **MV-Adapter, Step1X-3D, TRELLIS.2, UniTEX, SeqTex**: re-unwrap, are unreleased, or are trained on objects; none shows skin.
  - **AvatarTex** (arXiv 2511.06721): the one published method for whole face maps in a fixed layout trains a FLUX LoRA on ~80 maps in that layout, plus a Canny ControlNet to lock the eyes, lips and nose. **Nothing released.**
  - **Img2img on an existing UV atlas** is established practice for detail (Paint3D's UV-position ControlNet, Apache-2.0, SD1.5-class); no published skin evidence was found. The known failure, a model not knowing what an island is, did not occur for the head island (F-P25-7): an unwrapped face is a picture the model knows.
- **F-P25-10 — Krea 2 draws 1–2K** (ComfyUI's Krea 2 page). An 8K head needs a detail pass (RD-P25-13).
- **F-P25-11 — Strength cannot hold the fit, and cues in the source do not help (probe, this pass, after the lead's reply).** hm08's lips drawn dark and its lid slits drawn black in the source (`Phase25_AiSkinStructure_probe/cue.py`), the same prompt and seed: at 0.6 the result matches the plain source's (lips ~6 mm low); at **0.75 and 0.9 the model draws the same face with or without cues**, lips ~18 mm high, lash line ~7 mm off, brows painted ([`uv_face_cue.jpg`](Phase25_AiSkinStructure_probe/uv_face_cue.jpg): cued source · plain 0.75 · cued 0.6, 0.75, 0.9). That free face is the best skin of the probe and stable across strengths. So the features need a constraint other than strength: a geometry control, or a warp of the free face (RD-P25-10). Reproduce: `cue.py <out>`, then `UV_SRC=uv_Ccue.png python3 -I …/gen_uv.py <out> cue 0.6,0.75,0.9 7`. Placement is measured as the lip-redness and darkest-line centroids inside windows around hm08's masks (crude: a check, not the gate).
- **F-P25-12 — Input forwarded by the lead (another agent's write-up, 2026-11-01).** The lead: *"the skin itself looks MUCH better... but I see the fit is an issue... here is soemthing another agent looked into"*. Its plan generates a person from references in front, back, side and close views, projects them onto the mesh and inpaints the seams (Paint3D or a custom projection), and names HumanRef and SiTH. *(Read as:)* its stages 3–4 are the views route the lead rejected at 25.1.8, so not taken; HumanRef and SiTH reconstruct a body rather than texture a fixed one. **Its closing point is taken:** *"stop using the strength setting to solve a texture problem. Use geometry constraints to preserve geometry, and let the AI concentrate on the texture"*, which F-P25-11 measured. Its claim about a "Krea 3" is unverified.

## Deferred

| What | To | What it consumes from this phase |
|---|---|---|
| Other tones, people and ages from the model | *Variety* | the projection tool, the generation script, the inverse, the maker taking a field; the passed prompt |
| Marks on a structure from the model | *Skin Layers* | D's pigment field (if D won) or C's, through the maker |
| The skin-scale detail layer from a model (RD-SKM-5's allowed slot) | a later phase, unnumbered | the inverse; the projection tool's bake |
| The body islands painted in UV space | a later unit, unnumbered | the island tool, the chosen conditioner, the detail pass, the prompt |
| A creator-run generator | Q-AIS-1's framing, not ruled | the projection tool and the generation script |
| Studio's verdict | the platform (P33, P34) | the set as served |

## Depends on

- **The models (RD-OVS-5)** in the shared model folder, and the lead's ComfyUI, before 25.1's generation step: both supplied during this pass (F-P25-5). Execute checks each file is whole (no `.part` left) before the first run.
- **A Krea edit LoRA and its node pack** in the lead's ComfyUI, installed by 25.1 (RD-P25-10); the change logged in the workstation's change log.
- **Nothing outside this repo for any click.** The bar is read locally (RD-P23-10).

## Discovery Log

- **Seeded 2026-11-01** (`a7bb775`) by `/research` on the lead's *"Split and seed"*.
- **Pass 1 — 2026-11-01,** opened by the lead's *"/discovery Phase25"*.
  - **Examined:** the seed; the AIS research and its spike in full (and the spike's scripts' cameras and bake); the OVS research in full; Phase24 in full, its ledger and close; `CoreMechanisms.md` (row 1); `SkinMaps.md`'s outline and §Sources; `gen_synth_skin` (`SUBJECTS`, `Lut`, `compose`'s detail, regions and colour tail, `compose_banded`); `gen_skin_maps` (`from_picture`, `main`, `subject`); `look.py`'s options and `reference_casts`; the P24 resume retro; the platform's skin phase and character-quality research, and OMF's commits since the seed (fetched, read in place); the web for Krea 2's image routes and FLUX.2 [klein]'s sizes.
  - **Learnings:** GitHub G2 (regenerated pictures and LFS) bears on 25.3. Blender: not a click surface here (RD-CMT-4). Unreal: the look view as Phase24 ran it, no master change. MaterialX and Storm: not touched.
  - **The seed's questions, closed:** Krea's image input → F-P25-3, RD-P25-5 (step 1's measurement) · how far down the body → RD-P25-1 · the lip zone → RD-P25-2.
  - **The models' state** came from the lead's AIModels session by message during the pass (F-P25-5), which moved generation to ComfyUI (RD-P25-7) and Krea's encoder to the stock one (RD-P25-5).
  - **Baseline:** `run_all.py` at `180e00b`: **18 lanes, 18 PASS, none skipped.**
  - **Tree:** clean; one unpushed commit at kickoff (`180e00b`, the P24 retro); nothing to pull.
- **Pass 2 — 2026-11-01 (re-discovery),** opened by the lead's *"/discovery Phase25"* after 25.1.8 rejected the views route.
  - **Examined:** this doc and its ledger; the AIS research and spike; the routes the lead named; 25.1's tools (`gen_views_model.py`, the Krea workflow, `project_views.head_fields` and its renderer); `Tone34`'s 8K atlas; the P25 retro that landed mid-pass (`aa08951`: its item 1, *a spike's method taken as the route*, is what the routes table answers; its item 4 is in §Risk lane).
  - **Probed:** route 5 on Krea 2 through the lead's ComfyUI (already running, not this run's; left running), scratch in the session's folder, the scripts and two sheets kept beside this doc (F-P25-7). **Web:** routes 1, 2 and 4, by a web-only agent (F-P25-8, F-P25-9).
  - **Learnings:** none touched beyond Pass 1's (the image-model facts are tallied in the retro, not yet a domain).
  - **Consumers:** not re-swept; Pass 1's sweep is the same day and nothing was addressed to this phase since.
  - **Tree:** `aa08951` (the retro) landed from a sibling session during the pass; eight commits unpushed, all the lead's sessions'.
  - **After `18c840f` (BRIEF READY), the lead replied** (*"VERY interesting test you did... the skin itself looks MUCH better... but I see the fit is an issue"*) with another agent's write-up (F-P25-12). Probed in minutes whether cues in the source hold the fit (F-P25-11: no); corrected F-P25-7's lip number; RD-P25-10 now names a geometry control or one warp of the free face, and route 3 is taken in UV space.

## Execution ledger

*`step · commit · result · next`. Opened 2026-11-01 at `3df2ce1`, on the machine with Unreal; no Unreal Editor running; the lead's ComfyUI already running (left running: not this run's); the tree clean, three commits ahead of origin (unpushed).*

- **25.1.1 — the tools** · the `25.1` commit · `tools/converters/fit/project_views.py` (render the head with the subject at 2048², eight cameras: five at 0.78 m, three close at 0.45 m; bake onto the subject's 8K atlas; brow, lid and lip masks; the overlay gate; masked brows and lids filled with C at D's level; held on the face core; feathered over the neck), `gen_views_model.py` + `comfy/flux2klein_edit.json`, `comfy/krea2turbo_img2img.json` (ComfyUI's API, standard library only), `look.py --candidate`. **No SciPy:** the project has none, so the image steps are NumPy (`_box`, `enclosed`) and the feather is the maker's `gsm.blur`.
- **25.1.2 — Krea 2's strength (RD-P25-5's gate)** · no commit (pictures under the git-ignored `library/parity/P25_Views/`, `check_f000_krea.jpg`) · front view at denoise 0.5, 0.65, 0.8, each overlaid on its render: **0.5 keeps the features on hm08's; 0.65 doubles the ears' edge; 0.8 moves the eyes and doubles the lips.** Krea runs at 0.5.
- **25.1.3 — both models through the progressive chain, baked at 8K** · no commit · 8 pictures per model, ~30 s each (Krea), ~16–28 s (FLUX); each bake ~1 min; the 8K head is 17.4 M texels, 10.3 M seen. **The overlay gate** (painted head over the render's silhouette, ≥ 0.95): **Krea passes all 8** (0.993–0.999). **FLUX fails 4** (`f+40` 0.904; its three close-ups 0.71–0.94: it reframed each close-up as a whole head) **and the 4 that pass place features off hm08's inside the outline** (an eye painted beside the eye, the nose doubled; `library/parity/P25_Views/check_flux_sides.jpg`). D held to the subject's face core within ~1 % (Krea 0.649, 0.350, 0.256 against 0.644, 0.345, 0.253); clipped texels ≤ 0.03 %.
- **25.1.4 — FLUX drops from click 1 (RD-P25-5's gate, applied to FLUX as written for Krea)** · the overlay is the gate for a model's pictures; FLUX fails it at half its views and misplaces features at the rest, so its column would show a defect of the pipeline, not the model's skin. Krea carries click 1. Its pictures and D stay in the scratch folder.
- **25.1.5 — click 1, first showing** · the `25.1` commit · sheet `library/parity/P25_Click1_Sheet/look_sheet.png` (git-ignored; A · C · D-Krea, the nine views) · **measured before the showing, 40 cm front, linear, D over A:** cheeks 0.83–0.94 (C 0.94–1.01), forehead 1.00 / 1.16 / 1.31 (C ~1.0: D less warm there), nose 0.95–1.03, chin 0.88–1.06, under the eye 1.00–1.05. **Seen:** D's skin reads photographic, smoother than C with a natural flush on the cheek and nose; a faint lighter ring around each eye where the lids are filled. `run_all.py` **18/18 PASS**. Sitting owed.
- **25.1.6 — click 1, SAT 2026-11-01 (first showing).** The lead, verbatim: *"No way.. i can't believe you promoted this correctly... ths looks like a 3d animation skin... did you say that? if you did... don't... We want a human skin... also the eyes have someting strange going on there is like a ring of idifferent skin around them. The ear pattern is clearly not lined up. There is a neck line skin color change. That said.. D is better than C in overall look"* · *(Read as: D wins over C overall; four defects named, each the pipeline's, so click 1 is re-shown after the fixes, not passed.)* · **Causes, measured from the record:** Krea's prompt said *"photorealistic"*, *"matte … no shine"* and *"like a cross-polarised flat scan"* (it did not say 3D; FLUX's instruction did), and denoise 0.5 keeps half the render; the ring is C's own colour in the 7 mm kept clear around each eye opening (unseen, so C showed raw); the ears are baked from profile pictures that do not sit on hm08's ear; the neck join blends D held to the face into C's body with no level match. · next: the fixes, re-shown.
- **25.1.7 — the four fixes, re-shown** · the `25.1.7` commit · **prompt** (`gen_views_model.py`): an unretouched documentary photograph of a real woman (pores, vellus hair, small blemishes, *"no retouching … not a 3D render, not CGI"*), no *"photorealistic"*, *"matte"* or *"flat scan"*; Krea at 0.5 again (0.6 tried: richer texture, but the eye line and lips drift off the openings). **Ring:** the lids are the model's (the 4 mm band around each opening keeps the lash line out), and every unseen head texel takes C at D's level. **Ears:** masked out of the model, filled the same way. **Neck:** D's broad level eased onto C's from 0.53 to 0.60 m (below the measured chin, 0.616 m), then faded in 0.50–0.56 m. All 8 pictures pass the overlay gate (0.992–0.999); D's face core 0.649, 0.350, 0.256. Sheet `library/parity/P25_Click1_Sheet2/look_sheet.png`. **Seen before the showing:** skin texture and uneven tone in D; no ring; the ear plain; no line at the neck at 40 cm or 1 m; **a faint lighter arc above each brow** where the brow fill meets the painted skin. Sitting owed.
- **25.1.8 — click 1, SAT again 2026-11-01: the act ends on the premise.** The lead, verbatim: *"It is better but the ears still do not align and there are noticable gradient lines on the neck, on the forehead... etc. I still feel like this is still comeing too much from "Let's make a 3D model have a realistic skin" and not "figure out how to wrap a realistc skin on a 3D model" so you are cuting pasting, patching, matching, blending, when I think we should be trying to figure out how it can generate a full map..."* · *(Read as: D still beats C, but project-and-bake (render the head, repaint each view, stitch the views back with masks and blends) is the wrong route; the phase should find how an image model produces the whole skin map. That rejects 25.1's premise, and 25.2 and 25.3 both build on its D, so neither starts.)* · **What 25.1 established, kept for the next unit:** Krea 2 Turbo through ComfyUI makes skin the lead reads as better than C's; the prompt that reads human (`gen_views_model.py`); Krea img2img keeps hm08's features only up to denoise ~0.5; FLUX.2 [klein] 4B reframes close-ups and drifts features; the overlay gate, the head renderer and `look.py --candidate` (the judge for any D). **Next:** a re-discovery of the route (how a model generates the whole map in hm08's layout), not more fixes to the bake.
- *Pass 2's 25.1 opened 2026-11-01 at `c6b890d`, on the machine with Unreal; the lead's ComfyUI already running (not this run's; left running); a platform session's Studio build compiling (CPU only).*
- **25.1.9 — the island tool** · the `25.1` map commit · `tools/converters/fit/paint_uv.py`: `cut` (the head island as its own connected region, at the subject's held tone, upright, 2048 × 1072, 0.32 mm a pixel on the face; hm08's lips, lid openings and ear pads in the same frame; outside the island C's skin pushed outward), `paint` (Krea or FLUX through ComfyUI, standard library; the source uploaded under its hash, because ComfyUI served a cached result for a re-used name), `gate` (lips and lash lines found over the whole face; a drawn positive control passes at 0.9 mm; ears reported, not ruled), `warp` (one thin-plate warp of the whole picture, held by two rings, two passes), `put` (back on the 8K atlas, C elsewhere).
- **25.1.10 — the fit candidates (RD-P25-10)** · no commit (pictures under git-ignored `library/parity/P25_Map/`) · **(c) FLUX.2 [klein] edit: out** — seed 7 painted a second, larger face over the island with lash slits squeezed into hm08's openings, which the gate scored at 3.4 mm (it cannot see an extra face; every picture is looked at); seeds 11, 23, 31 fail at 2–28 mm. **(d) Krea's free face, warped: seed 7 PASS** — before the warp its eyes sat 33 mm high and ~20 mm too far apart, its lips 16 mm high, its ears 22–39 mm off; after two passes lips −0.2, +0.3 mm, lash lines ≤ 0.3 mm, ears ≤ 3.1 mm; largest local stretch 1.66×. Seed 11: 2.2 mm (fail). **(b) the edit LoRA: not installed**, (d) having passed. **Krea at 0.9 ignores its input** (plain, cued and filled sources give byte-identical pictures; at 0.6 and 0.75 they differ): the free face is Krea drawing an unwrapped head from the words alone, and the warp fits it.
- **25.1.11 — the neck** · no commit · on the mesh (the head renderer) the warped map holds the mouth, lids and the model's ears on hm08's ears; **a streaky jaw crease under each ear** where Krea painted a jaw shadow along the island's lower edge. Neck words in the prompt made it worse (neck wrinkles, dark wedges) and were reverted. Shown as a known defect, not patched.
- **25.1.12 — click 1, shown** · the `25.1` map commit · look view (`look.py Skin_Tone34_Clean_Base_s001_v01 --judge --bar library/parity/P24_Bar --candidate D-views=…/P25_Views/D_kr50.png --candidate D-map=…/P25_Map/D_s7.png --width 1536 --out library/parity/P25_Click1_Map`, git-ignored); ComfyUI's models released first (`POST /free`); the GPU free, a platform build compiling. **Seen before the showing:** D-map's face is one continuous real skin, the features on hm08's, the ear reads as an ear; the jaw crease under each ear shows from the side at 40 cm; soft in the close-ups at 2K (RD-P25-13). One labelled 1:1 comparison for the lead: `P25_Click1_Map/click1_front40_compare.png` (A · C · D-views · D-map, 40 cm front). `run_all.py` **18/18 PASS**. Sitting owed.

## Routes to compare at the re-discovery (2026-11-01, after 25.1.8)

*Compared and decided at Pass 2: §The routes, compared.*
