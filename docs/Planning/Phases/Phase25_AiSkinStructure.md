# Phase25 — AI Skin Structure

**Status:** IN EXECUTION (opened 2026-11-01 by the lead's "/execute Phase25" at `3df2ce1`). *Before:* BRIEF READY (discovery Pass 1, the same day), and SEEDED (2026-11-01), split out of Phase24 on the lead's *"Split and seed"* (RD-OVS-6). It runs after Phase24 (closed 2026-11-01), against Phase24's judge.
**Lane:** `build` (§Risk lane). **Next:** re-discovery of the route (25.1.8: the lead rejected project-and-bake; "generate a full map").
**Measured at:** `180e00b`, on **the machine with Unreal** (Unreal 5.8 at the path `unreal/build.sh` takes as `UE`; the official Blender 5.2.2 as `MATTER_BLENDER`; `unreal-runtime-v7` pinned).
**Seeded from:** [`../Research/261101_R_SkinMapsFromAnImageModel.md`](../Research/261101_R_SkinMapsFromAnImageModel.md) (RD-AIS-1, RD-AIS-2; Passes 3, 5 and 6) · [`../Research/261101_R_Spike_SkinMapFromImageModel.md`](../Research/261101_R_Spike_SkinMapFromImageModel.md) (the route proven on hm08's head; its scripts beside it) · [`../Research/261101_R_OneValidatedSkin.md`](../Research/261101_R_OneValidatedSkin.md) (OVS-3: AI enters as a structure; RD-OVS-1 … 6) · [`Complete/Phase24_OneValidatedSkin.md`](Complete/Phase24_OneValidatedSkin.md) (the judge, `Tone34`, its pigment fields).

## Outcome

**An image model's person becomes a skin structure in the library: projected onto the body, its light removed, turned into pigment and calibrated by the maker. It is judged beside the scanned skin and Phase24's skin on the same body.**

*(Confirmed at Pass 1 as seeded. The claim is the face, this subject, this tone (OVS-7), as Phase24's was.)*

---

## The Brief

### What this phase builds, in one paragraph

**The image model's skin as column D, against Phase24's judge.** A library tool renders hm08's head with `Tone34`, has an image model repaint the views as a real person (Krea 2 and FLUX.2 [klein], the same views, prompts and seeds), and bakes the pictures back onto the 8K atlas, with the brows, lid lines and lips masked out and the light divided off. Click 1 shows that projected colour (a comparison, RD-SYN-1) beside A and C, and picks the model. The winner is then inverted through the maker's skin model to melanin and blood, and the maker composes `Tone34` from that field in place of its own on the head, with C's own field on the body, calibrated like any structure. **Only the colour varies:** D wears `Tone34`'s shine set, lips, nails, body and every held-fixed piece. If D beats C, the lead gets the narrow re-ruling OVS-3 names and D becomes the set's colour. If not, the verdict is recorded and nothing ships.

### Rides on

| `CoreMechanisms.md` row | What in this phase rides it | The peer we follow |
|---|---|---|
| 1 — a body map larger than 2048 inside the machine's memory | D's colour composed at 8K from an outside field (25.2), and the 8K bake of the projected views (25.1) | `tools/converters/fit/gen_synth_skin.py` `compose_banded` (opened this pass): the atlas in bands of 512 rows, what needs the whole atlas taken once (`band_pre`) |

Nothing else here is shown, moved, edited or written by a mechanism the project has solved before: the projection and the inversion are new (F-P25-1).

### First human test

**Where:** the machine with Unreal, where every tool the clicks compare has run (`LOCAL_DELTAS.md` §Two machines).
- **The surface:** the library's look view (`tools/parity/look.py --judge`, the pinned runtime), Phase24's nine fixed views at ~1 m and ~40 cm (RD-P24-4, never changed), `--width 1536`. A is the scanned bar (`--bar`, made locally, never committed: RD-P23-10). C is `Skin_Tone34_Clean_Base_s001_v01` as served. D is a colour picture from outside the tree worn by `Tone34`'s article, with its shine set (RD-P25-3). The agent renders, measures, opens the sheet with `xdg-open` and puts its path in the handback. A character material's look is judged in the Unreal look view, never Blender (RD-CMT-4).
- **The ruler:** sat at Phase24's click 1 (*"A reads real, B reads fake"*) on these views and this light; nothing in them changes, so it is not re-sat. B is left off the sheet.
- **Can the surface show it?** At `--width 1536` the close-ups are 0.04 mm a pixel. The smallest thing judged is D's own detail: a model pixel is 0.16 mm on the face at 2048² views from the spike's camera, and 0.09 mm from a close camera (F-P25-2). So a model pixel is 2–4 screen pixels in the close-ups and the softness, if any, shows. An 8K texel is ~0.1 mm. The fixture is the subject itself: one tone and one person by ruling (RD-OVS-1), so there are no extremes to span.

1. **Click 1 — the model's person beside the bar (25.1).** A · C · **D-Krea** · **D-FLUX**, each D the projected colour held at the subject's tone (a comparison under RD-SYN-1, never shipped).
   - *Judge:* does either model's person read as real as A? Where does it beat C, or lose to it, part by part (the ring under the eye, the cheeks, the nose, the brows' edge, the hairline)?
   - *What the lead can say after:* *"D-FLUX reads real; it beats C at the cheeks and loses at the nose"*, or *"C beats both"*. That answers RD-AIS-2 (*"prove the concept"*) on the library's judge and picks the model.
   - **If neither D beats C in any view,** 25.2 does not start on the agent's own word: the result is recorded, and the lead says whether the structure is still built (RD-P25-6).
2. **Click 2 — the structure (25.2).** A · C · **D**, the winning model's field composed by the maker at 8K.
   - *Judge:* the same question, of the structure.
   - **Shown only if the structure changes the look:** the inversion is meant to give back the projected colour. The agent measures D against click 1's picture per face region; **if every region is within 1 ΔE (CIE76, on the rendered views), click 1's verdict stands for D**, the ledger records the measurement, and click 2 is not called. Where the model painted colour the skin model cannot make (painted-in hair, a grey shadow), the structure differs, and click 2 is shown.
3. **Click 3 — the set with D, served (25.3, only if D won).** The served set in the look view's four views (face, three quarters, the back of the hand with its nail, the ear) plus the 1 m front, where the head's field meets the body's at the neck.
   - *Judge:* does the set read as one person, with no join at the neck?

**Reconciled click by click:**
- Click 1 needs only 25.1: the views, the two models, the bake with its masks, the light divided off, D held at the tone, and `look.py` drawing a picture on `Tone34`. No inversion, no maker change.
- Click 2 needs 25.2: the inverse of the skin model, the maker taking a field, D composed at 8K. It is reached on the same fixture.
- Click 3 needs 25.3, which runs only on a D win and after the lead's re-ruling.
- **§In now, walked:** every row below names its step.

**Not a click: Studio and the headset.** The platform's (RD-OVS-4); its skin phase reads this one as *"nothing new for the platform beyond the judge"* (F-P25-6).

### In now

| Item | Step |
|---|---|
| **The projection as a library tool** under `tools/converters/fit/`: hm08's head rendered with `Tone34` from the spike's cameras plus close cameras for the face (RD-P25-4); the progressive sides (F-AIS-12); the bake onto the 8K atlas (z-buffer, silhouette and eye margins, cos⁴ weight, as the spike's); **masks at the brows, the lid lines and the lips** (F-AIS-13); the neck feather lengthened; the light divided off (the render's own light, as the spike's) | 25.1 |
| **The generation step** for both models, same views, prompts and seeds, recorded (model, revision, seed, prompt, steps, strength) (RD-P25-5, RD-P25-7) | 25.1 |
| **D held at the subject's tone** on the face core (`SUBJECTS["Tone34"]["held"]`, as C is) and feathered into C's colour below the neck (RD-P25-1) | 25.1 |
| **`look.py --reference` takes a subject skin** (today it refuses any non-Fitzpatrick skin) | 25.1 |
| **The inverse of the skin model:** a texel's colour over the tone → melanin and blood, at that texel's oxygenation and depth as the maker sets them (F-P25-1) | 25.2 |
| **The maker takes an outside field:** `gen_skin_maps.py --subject Tone34` with D's field on the head and C's on the body, joined in pigment at the neck; the lips the maker's (RD-P25-2); calibrated as C is | 25.2 |
| **`Tone34` and the 18 skins remake pixel-identical without the field** (Phase24's precedent) | 25.2 |
| **If D won:** the lead's re-ruling; `Tone34`'s colour made from D; its provenance (*AI-assisted*, the model named, `SkinMaps.md` §Sources); the views kept as its source (RD-P25-8); thumbnails; the dev install re-served | 25.3 |
| **Written down:** `SkinMaps.md` (an AI-made structure: how it is made, and whether one is accepted, in the lead's words); the AIS research's Q-AIS-1 row | at the close |

### Not now

- **The body from the model:** the head only (RD-P25-1). The body has no bar (OVS-7).
- **Other tones, people and ages:** *Variety*, after.
- **A raw painted AI map shipped as is:** never (RD-SYN-1); D0 is a comparison only.
- **A creator-run generator:** Q-AIS-1's framing, recorded, not ruled.
- **Training or fine-tuning a model,** and photos of people as training data (F-AIS-8, Q-AIS-2).
- **Krea 2's community edit LoRAs:** only if Krea's plain route fails its overlay check, and then the lead's call (RD-P25-5).
- **The shine set, lips and nails from the model:** a model draws colour only; they stay `Tone34`'s (RD-P25-3).
- **The skin-scale detail layer route** (F-AIS-5, the `Md`/`Bd` slot RD-SKM-5 already allows): kept open, not this phase. The whole-head structure is the claim under test.

### The reuse check

*What does the stack already provide, and which contracts are touched?*
- **The judge exists** (`look.py --judge`, `--bar`, Phase24). The reference column draws an outside picture on a skin with its own shine set (`look.py` `reference_casts`); it needs to accept a subject skin (F-P25-4).
- **The projection exists as the spike's scripts** (`261101_R_Spike_SkinMapFromImageModel_probe/`: `headrender.py` renders hm08 from the maker's fields, `bake.py` projects pictures back and holds the mean, `gen_flux.py` / `gen_krea.py` generate). It moves into `tools/converters/fit/`, at 8K, with the masks.
- **The generation runs in the lead's ComfyUI** (installed 2026-11-01, with a shared model folder on a local drive the lead set up for every project; its launcher `comfyui`, ComfyUI's default port). ComfyUI finds the models through its own model-path config, so the repo names a model by its file name and never writes the folder's path. It loads Krea 2 in the form it was supplied (F-P25-5) and FLUX.2 [klein] natively; the spike's diffusers scripts are the reference for the prompts and settings, not the runner.
- **The maker's face masks exist** for the masks D needs: `gen_synth_skin` `F["masks"]` (`eyelids`, `lips`, `face`) and `face_regions` (`upper_lid`, `under_eye`). A brow mask is placed from the same landmarks (`face_landmarks`).
- **C's pigment fields exist at 8K** (`gen_skin_maps.py --subject Tone34 --fields`, RD-P24-6): the body's field for D.
- **The skin model is tabulated** (`Lut`: melanin × blood × oxygenation → colour); its inverse is a lookup on the same table. Nothing borrows a new model.
- **The 8K maker in bands** (CoreMechanisms row 1).
- **Every map reaches every renderer through the inputs that exist** (`base_color_map`): no input added, no master changed, **no new Unreal runtime owed.**
- **Contracts touched:** none of the article's. `SkinMaps.md` §Sources (*"A fully AI-made map is not accepted"*) is touched only by the lead's re-ruling at 25.3, if D wins.

### Decisions that bind

*One authoritative copy. Rulings are quoted where they are the authority.*

**Carried rulings:**
- **RD-AIS-1** (the lead, 2026-11-01): Krea 2 first; the revenue limit is no obstacle (*"WELL under 1M … I would lean towards KREA2 … but I am open to whatever"*). FLUX.2 [klein] 4B beside it.
- **RD-AIS-2:** prove that whole maps can look really good (*"I want to prove the concept"*).
- **RD-OVS-1, -2, -5, -6:** the bar's tone (*"Tone, yes"*); 8K (*"start with 8k"*); the lead supplies the models (*"I will get us krea and also Flux klein to tryout"*); two phases (*"Split and seed"*).
- **OVS-3 (OMF's input, not a ruling):** an AI skin enters as a structure (projected, its light removed, pigment, calibrated), and a win is put to the lead as a narrow re-ruling.
- **RD-SKM-5, RD-SYN-1:** no whole AI map ships; a whole AI map is a judged comparison only. **RD-SKM-2:** no photograph of a person in what ships. **RD-P23-10:** the bar stays local, its path never in a tracked file. **RD-RO-2:** CC0.
- **RD-CMT-4:** a character material's look is judged in the Unreal look view until Studio draws it, never Blender.
- **Phase24's judge as it sat:** RD-P24-4 (the views, fixed), RD-P24-5 (A), RD-P24-3 (the lips on the skin), the subject `Tone34` (RD-P24-1, -8).
- **Pre-release, no versioning** (`AI_WorkingAgreement.md` §Settled practices).

**Decided here, unless the lead says otherwise:**
- **RD-P25-1 — The model draws the head; the body is C's.** The projection covers the head and neck (the spike's region, every triangle above the shoulders); below, D is C's own pigment field, joined in melanin and blood over the neck, where a join cannot change tone (both fields sit at the same operating melanin). Why: the claim is the face (OVS-7, no body bar), all nine judge views are of the head, and Krea's content-filter duty bites only on unclothed body views (F-AIS-3). *Answers the seed's "how far down the body".*
- **RD-P25-2 — The lips are the maker's.** `Tone34`'s solved lips (exact to the bar, 24.2.5) cover the lip zone, as the maker already feathers it (`compose`'s lips term); the model's lips are masked out of the bake. Why: OVS-8 holds the lips fixed, the spike's side views double the lip line (F-AIS-13), and a lip difference would decide the verdict, not the skin. *Answers the seed's "how the lip zone joins".*
- **RD-P25-3 — Only the colour varies.** D wears `Tone34`'s roughness, relief, cavity and scatter, its nails and every held-fixed piece. A model draws colour only.
- **RD-P25-4 — Views at the model's largest size, with close cameras for the face.** 2048² (FLUX.2 [klein]'s ceiling, 4 MP; Krea at the largest square it draws well, measured at 25.1, not assumed) from the spike's five cameras, plus close cameras at ~0.45 m on the eyes, the nose and cheeks, and the mouth, so the face gets about one model pixel per 8K texel (F-P25-2). The progressive order holds: each view rendered with the map baked so far. Execute records the measured millimetres per pixel per region.
- **RD-P25-5 — Two D rows at click 1, the same views, prompts and seeds.** The prompt is the subject: a woman about twenty (hm08's default age, RD-OVS-3), bald, eyes closed, no eyebrow hair, matte cross-polarised flat light, *"keep exactly the same head shape, pose, camera angle, framing"* (the spike's pass 2). **Krea 2 runs by the spike's route** (the render encoded to a latent and denoised at a strength below 1, ComfyUI's ordinary img2img), because it is not an edit model (F-P25-3), **with the stock text encoder** (`qwen3vl_4b_fp8_scaled`): the head route needs nothing a modified encoder unlocks, and the provenance then names only published files. The third-party encoder supplied beside it stays the lead's, for other work. **Its gate is F-AIS-11's overlay:** at a strength that repaints the skin, the eyes, nose, mouth and ears must land on hm08's. If no strength passes, Krea drops with the overlay as the evidence, FLUX carries click 1 alone, and Krea's edit LoRAs become the lead's question (their licences read first). *Answers the seed's Krea question as step 1's measurement.*
- **RD-P25-6 — Click 1 can stop the phase.** If neither D beats C in any view, the agent records it and asks the lead whether 25.2 is still built (the structure is what makes a later tone change and *Skin Layers*' marks possible, so it may be worth having even after a loss). It is not built on the agent's own word.
- **RD-P25-7 — The generation step drives the lead's ComfyUI; the project gains no dependency.** A library script sends a tracked workflow (one per model, JSON under `tools/converters/fit/`) to ComfyUI's HTTP API with the views, the prompt and the seed, and collects the pictures and a record of the model files, seed, prompt, steps and strength. It needs only the standard library, so the project's environment gains nothing (as RD-P24-5 kept EXR reading out); torch lives in ComfyUI's own environment. **ComfyUI is started by the agent only if it is not already running, and stopped by PID when the run is done** (`.claude/CLAUDE.md` §Git, *stop what you started*); its drive mounts at login, so a run checks it is there first. Everything after the pictures (the bake, the masks, the inversion, the field) is NumPy in the project's environment.
- **RD-P25-8 — If D wins, the views are its source.** The generated views (a handful of 2048² pictures, tens of MB) are tracked in LFS beside the skin's provenance, each with its model, revision, seed and prompt; the field and the map are remade from them by the NumPy half, with no model run. So D is reproducible from the tree, which the field alone (derived, ~hundreds of MB at 8K) is not worth tracking for (RD-P24-6's reasoning). They are synthetic pictures under licences that give the user the output (F-AIS-3, F-AIS-4), dedicated CC0 with the rest. **Where they live is execute's, after reading what enumerates that folder** (§Risk lane). If C wins, nothing is tracked.

### Risk lane — `build`

The controls this phase touches, each read on 2026-11-01:
- **The maker** (`gen_synth_skin.compose` / `compose_banded`, `gen_skin_maps.subject`): a new optional input. **Its fingerprint is every committed skin map:** without the field, `Tone34` and the 18 skins must remake pixel-identical (proved in-process, as Phase24 did at 2048, max difference 0). The provenance writer (`write_provenance`) gains a row only for a D win.
- **`look.py` `reference_casts`:** refuses a non-Fitzpatrick skin; widened to a subject skin. It writes only under its output folder (RD-P23-10).
- **What enumerates the trees D adds to:** the new tools under `tools/converters/fit/` are enumerated by no gate (they are scripts, not articles). A D win changes `SkinTone34_basecolor_sUKN.png`, which the recipe gate (G8 at 8K, RD-P24-2), thumbnails (stale, remade: 28 s) and `serve_to_stage.py` read; Learnings G2: compare pixels before committing a regenerated picture. The views' folder (RD-P25-8) is grepped against the release and provenance lanes before it is chosen.
- **The masters and the runtime:** untouched (§Reuse check).
- **The one irreversible risk is publication:** the repo is public. The bar is never committed nor its path written (`.gitignore`'s `library/parity/`, explicit-path staging). The generated views are committed only on a D win and the lead's re-ruling.
- **The box:** Krea 2 arrives in FP8 (its 12B transformer about half the GPU's memory, F-P25-5), so it runs on the GPU; other sessions compile on this machine, and the out-of-memory guard kills compilers first, then the largest process. **Before each model run:** `ps -ef | grep "[U]nrealEditor"` (the GPU is shared), a running ComfyUI checked for (another session's, then not stopped), and free memory read. The 8K compose peaks at about a fifth of the box's memory (row 1).
- **Disk:** the models live on the lead's shared model drive, not the home volume (F-P25-5).
- **Baseline:** `run_all.py` at `180e00b` (§Discovery Log). No change under `blender/addons/` or `tools/conformance/`, so `check_exporter.sh` is not owed.

Nothing here is authorization, secrets, a destructive migration or the public edge.

### Step list

- **25.1 — The model's person on the judge.** The projection tool at 8K with the masks and close cameras (RD-P25-4); both models through the generation script (RD-P25-5, -7); D held at the tone, the body C's (RD-P25-1); `look.py --reference` on `Tone34`. **Click 1** (A · C · D-Krea · D-FLUX).
- **25.2 — D as a structure.** The skin model's inverse; the maker composing `Tone34` from D's field on the head and C's on the body at 8K, the lips the maker's (RD-P25-2); the remake-identical proof; the round trip measured against click 1. **Click 2**, only if the structure changes the look.
- **25.3 — If D won: the set with D, served.** The lead's re-ruling put with the sheet; `Tone34`'s colour from D; provenance; the views tracked (RD-P25-8); thumbnails; the dev install re-served. **Click 3.**

Time to the first click: the spike's scripts moved and widened, two model runs (minutes each once the models are on disk), one 8K bake, one look-view launch. The models are on the shared drive (F-P25-5).

### Compact build map

- **25.1:**
  - `tools/converters/fit/project_views.py` (new, NumPy): render the head from the atlas (the spike's `headrender.py`, from `gen_synth_skin.fields()`), the cameras (`views.py`'s five + close cameras), `bake` (the spike's `bake.py` at 8K in bands, row 1; masks from `F["masks"]` and a brow mask from `face_landmarks`; a longer neck feather; held on `hold` = MPFB's face mask over 0.9, as `gen_skin_maps.subject` does). Writes under a git-ignored folder (`library/parity/P25_*`).
  - `tools/converters/fit/gen_views_model.py` (new, standard library, RD-P25-7) and its workflows (`comfy_krea2.json`, `comfy_flux2klein.json`): `--model krea|flux`, the views in through ComfyUI's API, the repainted views out, a JSON of the model files, seed, prompt, steps, strength. Prompts and settings from the spike's `gen_flux.py` and `gen_krea.py`.
  - `tools/parity/look.py` `reference_casts`: accept a subject skin; D's picture is already at the subject's tone, so it is drawn as made.
  - Evidence before click 1: F-AIS-11's overlay for each model; D per face region against A and C (Phase23's profiles, as Phase24 measured); millimetres per model pixel per region.
- **25.2:**
  - `gen_synth_skin.Lut.inverse(ratio, so2, depth)`: per texel, the (melanin, blood) whose colour over the base matches, by the table's own grid (a nearest lookup refined by one interpolation step); out-of-gamut texels reported, not clipped silently.
  - `compose` / `compose_banded`: an optional outside field (`field=`) replacing `mel` and `bld` where its weight is 1, C's own elsewhere, joined in log-pigment; the lips term unchanged.
  - `gen_skin_maps.py --subject Tone34 --pigments DIR`: D's field in; the map and its stats out to a scratch folder unless D won.
  - Proof: without `--pigments`, `Tone34` and the 18 skins pixel-identical (in-process). The round trip, D against click 1's picture per region (ΔE).
- **25.3 (only on a D win):** `SkinTone34_basecolor_sUKN.png` from D; the provenance row (`made: ai-assisted`, model, revision, seed, the views' hashes); the views tracked (RD-P25-8); `make_thumbnails.py`; `serve_to_stage.py --no-restart` (check for a running Stage daemon first; close what you start); `SkinMaps.md` §Sources in the lead's words.
- **Tests:** `run_all.py` per step; the remake-identical proof; one real-path smoke per click, which is the look view itself. No new gate.

### Open for the lead

*None.* RD-P25-1 … 8 are decided unless the lead says otherwise. *(FLUX.2 [klein], the one item open at the first commit, the lead closed during the pass: "You can grab flux and put it in the share models folder if you like" — fetched by this session, F-P25-5.)*


---

## Findings (discovery Pass 1, 2026-11-01)

- **F-P25-1 — The maker has no way in for an outside field, and its skin model runs one way.** `pigments=` on `compose`, `compose_banded` and `gen_skin_maps.py --fields` is an output (RD-P24-6). The colour is `tone × lut(melanin, blood, so2) × (1 − depth × reach) / lut(m0, blood0, 0.8)`, then held on the body (`compose`'s tail). So an inverse solves each texel's colour-over-tone for melanin and blood at that texel's oxygenation and depth, on the same table (`Lut`); it does not exist yet.
- **F-P25-2 — At 8K the views, not the layout, cap D's sharpness.** The spike's views are 1024² at 0.78 m with a 24° lens: 0.33 m across, **0.32 mm a pixel** on the face. FLUX.2 [klein] draws up to 4 MP (2048², its maker's specification), **0.16 mm**; a close camera at ~0.45 m gives **~0.09 mm**. `Tone34`'s 8K texel is ~0.1 mm, and the judge's close-ups show 0.04 mm a pixel. So the spike's views would make D ~3× softer than C, visibly, in the close-ups; F-AIS-15 (*"the layout limits sharpness"*) held at 2048 and reverses at 8K. RD-P25-4.
- **F-P25-3 — Krea 2 is not an edit model.** Its diffusers pipeline is text-to-image (the spike). Image-conditioned editing exists only as community ComfyUI LoRAs (a Krea 2 identity edit and a general edit LoRA; another node whose own page warns Krea 2 *"is not an edit model"* and *"alters the image sometimes"*); the official node takes a style reference only. Their licences are unread. So the spike's noised-latent start is the plain route, and Krea must re-prove that the features stay on hm08's (F-AIS-11). RD-P25-5.
- **F-P25-4 — Phase24 left D's footing in place.** C's 8K melanin and blood fields are local (`library/parity/P24_Fields/`, git-ignored, from `gen_skin_maps.py --subject Tone34 --fields`), and so is the solver that fitted `Tone34` to the bar (`library/parity/P24_Solver/`). `look.py --reference` draws an outside picture on a skin with its shine set, but `reference_casts` refuses any non-Fitzpatrick skin.
- **F-P25-5 — The models, as supplied (the lead's AIModels session, 2026-11-01, during this pass).** Krea 2 **Turbo** arrives as ComfyUI single-file FP8 from Comfy-Org's repack (the transformer `krea2_turbo_fp8_scaled`, 12.2 GiB, whole by the time this pass committed; the stock `qwen3vl_4b_fp8_scaled` text encoder and a third-party abliterated one beside it; the Qwen-Image VAE), each checked against its published hash, in **a shared model folder on a local drive** that ComfyUI reads (the lead: *"we are installing comfyui and various models in a share location"*). These are ComfyUI files, not diffusers, so the spike's `gen_krea.py` does not load them (RD-P25-7). The repack downloaded with no login, so no Hugging Face login is needed. **FLUX.2 [klein] was then fetched by this session on the lead's word** (*"You can grab flux and put it in the share models folder if you like"*): Comfy-Org's ComfyUI split of the Apache-2.0 4B at revision `5b3abca` (the distilled `flux-2-klein-4b`, the `qwen_3_4b` text encoder, `flux2-vae`), each renamed into place only after its sha256 matched the published one. In FP8 Krea's transformer is about half the GPU's memory, so it runs on the GPU (the spike's bf16 copy would not have fit).
- **F-P25-6 — The consumers since the seed (fetched 2026-11-01):** the platform's skin phase lists this phase as *"Nothing new for the platform beyond the judge"*, and its first sitting uses Phase24's judge; OMF's newest input (the character model) is addressed to the platform. **Nothing addressed to this library changes this phase.**

## Deferred

| What | To | What it consumes from this phase |
|---|---|---|
| Other tones, people and ages from the model | *Variety* | the projection tool, the generation script, the inverse, the maker taking a field; the passed prompt |
| Marks on a structure from the model | *Skin Layers* | D's pigment field (if D won) or C's, through the maker |
| The skin-scale detail layer from a model (RD-SKM-5's allowed slot) | a later phase, unnumbered | the inverse; the projection tool's bake |
| A creator-run generator | Q-AIS-1's framing, not ruled | the projection tool and the generation script |
| Studio's verdict | the platform (P33, P34) | the set as served |

## Depends on

- **The models (RD-OVS-5)** in the shared model folder, and the lead's ComfyUI, before 25.1's generation step: both supplied during this pass (F-P25-5). Execute checks each file is whole (no `.part` left) before the first run.
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
