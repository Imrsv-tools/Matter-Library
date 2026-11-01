# Phase24 — One Validated Skin

**Status:** BRIEF READY (discovery Pass 1, 2026-11-01). *Before:* SEEDED the same day. The lead numbered it on OMF's input (*"today's hm08, Matter Library hosts it … it will seed the phase"*) and here: *"Just ONE set please we need to stop genearting 5 shades... let's get one complete set build and tested,,, then we can add variety."* Split the same day (*"Split and seed"*, RD-OVS-6). The image model's skin is [`Phase25_AiSkinStructure.md`](Phase25_AiSkinStructure.md), which runs against this phase's judge.

*Migration note (2026-11-01, the method re-sync to upstream `897f5f3`): this Brief was written under the earlier `/discovery`, so it has no `## Rides on` table. `docs/CoreMechanisms.md` holds no rows yet, so the table would be empty and `/execute` owes nothing for it beyond reading that file at its start.*
**Lane:** `build` (§Risk lane). **Next:** `/execute Phase24`.
**Measured at:** `08da67b`, on **the machine with Unreal** (Unreal 5.8 at the path `unreal/build.sh` takes as `UE`; the official Blender 5.2.2 as `MATTER_BLENDER`, Learnings B22; `unreal-runtime-v7` pinned).
**Builds on:** [`Complete/Phase23_SyntheticSkinSets.md`](Complete/Phase23_SyntheticSkinSets.md) (the pigment maker, the look view's reference column, the placed face regions and the scratch solver) · [`Complete/Phase22_SkinMapsBeyondColour.md`](Complete/Phase22_SkinMapsBeyondColour.md) (the four shine maps) · [`../../specs/Authoring/SkinMaps.md`](../../specs/Authoring/SkinMaps.md).
**Research:** [`../Research/261101_R_OneValidatedSkin.md`](../Research/261101_R_OneValidatedSkin.md) (OMF's protocol, OVS-1 … 8; the library's Pass 2; RD-OVS-1 … 6).

## Outcome

**One young woman's skin, complete (colour, shine, lips and nails), stands beside the scanned skin on the same body, and the lead cannot tell them apart at set distances, or names, part by part, what still differs. It is served as one finished set, ready for Studio when Studio can take it.**

*(Confirmed at Pass 1 as seeded: OMF's proposed Outcome, widened to the lead's "one complete set build and tested". The claim is the face, this subject, this tone (OVS-7).)*

---

## The Brief

### What this phase builds, in one paragraph

**One skin set for one subject, judged against the scanned skin at 8K.** The library's look view gets the judge: the scanned bar (A), today's III skin (B) and the candidate (C), on one body, in fixed views at two distances. The pigment maker and the shine maker then run at 8K for one subject, fitted to the bar region by region at the bar's own tone, with the lips drawn and glossed by the skin itself. The set (skin, lips in, its own shine maps, its nails) is served to the dev install and seen on the character in the lead's Blender. **Nothing else changes:** the 18 skins, six lips and shared shine maps stay as they are.

### The one set

| Piece | What it is | Today |
|---|---|---|
| **Body skin** | One article on hm08 at the bar's tone (RD-OVS-1), its colour map **at 8K** (RD-OVS-2). **The lips wear it** (RD-P24-3). | 2048², 18 skins, lips a separate article per tone |
| **Its shine set** | Its own roughness (a glossier lip zone and T-zone, fitted to the bar's specular), relief, cavity and scatter, at 8K | One 2048² set shared by every skin |
| **Nails** | One nail article for this subject, derived from its skin by the existing nail rule | One per Fitzpatrick tone |
| **Pigment fields** | Its melanin and blood, written beside the set on request, never shipped (RD-P24-6) | Inside the maker |
| **Held fixed** | the female hm08 at its default age (RD-OVS-3), its eyes, card hair and brows, the look view's light, the views and distances, the atlas | — |

### First human test

**Where:** the machine with Unreal; every tool the clicks compare runs there (`LOCAL_DELTAS.md` §Two machines).
- **The look:** the library's look view (`tools/parity/look.py`, the pinned runtime), with this phase's views. The agent renders, measures, opens the sheet with `xdg-open`, and puts its path in the handback.
- **The views, fixed at click 1 and never changed after** (OVS-Q2, RD-P24-4): the face from the front, at three quarters and in profile, each with a viewer's eye at **~1 m** and at **~40 cm**; and close-ups of an eye, the lips, and the cheek with the nose, at ~40 cm. One lens for all of them.
- **The agent drives every tool; the lead looks and judges.** A look click is called only when its change is measured visible (Phase22, RD-P22-14).

1. **The ruler (24.1).** Columns **A** (the scanned bar at 8K: its colour, its specular as the cavity map, on the shared relief and scatter; lips on the skin) and **B** (today's `Skin_FitzpatrickIII_Clean_Base_s001_v01` with its lips and nails, as shipped), in every view.
   - *Judge:* **A reads real and B fake**, in the lead's words. If not, the views or the light are wrong and no verdict after counts (OVS protocol step 3).
   - **Can the surface show it?** At `--width 1536` (the widest the look view captures, Phase23 23.1.1), the eye close-up spans ~6 cm, about 0.04 mm a pixel, finer than an 8K texel (~0.1 mm). The bar is the fixture the property lives on: it was fitted onto hm08's own atlas, so A is a picture of the body, not a stand-in.
2. **The candidate (24.2).** A · B · **C**, the same views, iterated until C passes or the gap is named by part.
   - *Judge:* can C be told from A, at each distance? If yes, where, part by part (the ring under the eye, the cheeks, the lips' edge, the nose, the pores' shine)?
   - **Can the surface show it?** The agent's evidence before each showing: C against A per face region (Phase23's profiles, 23.2.7–23.2.9, at 8K), the band-pass strengths, and the shine's spread over the T-zone and cheeks. **The screen can rule a failure out; it never accepts** (OVS protocol step 5).
3. **The set on the character (24.3).** The finished set (skin, lips, nails) on the character in the lead's Blender, built headless from the factory scene into its own file and opened detached (`LOCAL_DELTAS.md`; Learnings B10–B11, ClaudeCode CC2), with everything held fixed.
   - *Judge:* does the set read as one finished person, the nails and the lip edge included?
   - **Can the surface show it?** The scene's cameras are the look view's face and a hand, at the same two distances; Blender draws 8K pictures as stored.

**Reconciled click by click:**
- Click 1 needs only 24.1: the views, A's pictures made locally, the lips-on-skin cast, and B as shipped. No C, no maker change.
- Click 2 needs 24.2: the makers at 8K, the G8 size rule, the subject's skin article. The nails are not in a face view, so the cast's nails are held as at click 1 until 24.3.
- Click 3 needs 24.3: the nails, the provenance, the dev install, the Blender scene.
- **§In now, walked:** every row below names its step.

**Not a click: Studio, and the headset.** Studio's verdict in its look-dev scene (P33) and Studio drawing the shine maps (P34) are the platform's sittings; the lead asks the platform for them (RD-OVS-4), and the platform reads its own skin phase as its half of this one (its research, 2026-11-01). The protocol's headset view (OVS step 4) is Studio's too: the library's look view renders stills. **The close does not wait for either** (RD-P23-9's precedent).

### In now

| Item | Step |
|---|---|
| **The judge in the look view:** the fixed views and distances (RD-P24-4); columns A, B and C on one body; A's pictures made from the bar at 8K, locally, outside the tree (RD-P24-5); the Lips part wearing the skin where a set has its lips in (RD-P24-3) | 24.1 |
| **G8 takes a map at a power-of-two multiple of its mesh's size, on the same layout** (RD-P24-2); a test case for 8K accepted | 24.2 |
| **The colour and shine makers at 8K** within the box's memory (RD-P24-7) | 24.2 |
| **The subject's colour:** one structure, fitted to the bar by region at the bar's tone (Phase23's solver at 8K), the lips drawn in | 24.2 |
| **The subject's shine set:** its roughness fitted to the bar's specular by region, a glossier lip zone, at 8K; relief, cavity and scatter remade at 8K | 24.2 |
| **The subject's skin article**, wearing its five maps (`candidate`) | 24.2 |
| **The pigment fields** written on request (RD-P24-6) | 24.2 |
| **The subject's nail article**, from its skin by the nail rule | 24.3 |
| **Provenance, thumbnails, the dev install re-served** (`serve_to_stage.py`) | 24.3 |
| **Written down:** `SkinMaps.md` (one set at 8K beside the 2048 skins; the lips on the skin; a subject's own shine set), the Glossary if a term is new, the ledger's P33/P34 rows (the set to judge in Studio) | 24.3 |
| **A dev snapshot**, at the lead's word, with `HEAD` pushed | at the close |

### Not now

Each has a home:
- **the image model's skin:** [Phase25](Phase25_AiSkinStructure.md), against this judge (as column D);
- **picture size, loading and performance tests, and a size per layer:** later phases (RD-OVS-2). Here, one size: 8K;
- **other tones, people and ages:** re-runs of the passed recipe (*Variety*, after);
- **marks and makeup on this subject; shipping the pigment fields:** *Skin Layers*, from this set's fields (OVS-6);
- **the body's verdict:** the bar is a face scan (OVS-7);
- **a new body, and the re-bake onto it:** OMF's body work, then the re-bake test (OVS protocol step 7);
- **eyes:** *Eyes in the Shader*, held fixed here;
- **retiring the `Lips_*` articles or the 18 skins, or moving them to 8K:** they stay (§Don't Delete Spec Functionality);
- **the face's remaining gap on the 18 skins** (Phase23's parked ring and blotching): *Skin Layers*, unless the lead asks for this set's fix to be carried back;
- **Studio's side and the headset:** the platform's (RD-OVS-4).

### The reuse check

*What does the stack already provide, and which contracts are touched?*
- **The pigment maker, its placed face regions and the calibration exist** (`gen_synth_skin.py`, `gen_skin_maps.py`; Phase23). One subject is one row in `STRUCTURES` plus a tone. The scratch solver that fitted `FACE` to the bar's regions (Phase23 23.2.9, kept git-ignored on this machine) is the fitting tool; it moves from 4096 to the bar's 8K.
- **The shine maker exists** (`gen_skin_shine.py`, with `--out`). Its zones are placed from hm08's joints; this phase fits their strengths to the bar's specular and adds the lip zone.
- **The look view exists, with a reference column** (`look.py --reference`, Phase23 23.1). It already accepts a picture at any multiple of the atlas (`size % gsm.N`). New: views, and A's shine.
- **The Unreal runtime loads an 8K picture with no change** (F-P24-4): its texture group allows 16384, and it caches each file once.
- **Every map reaches every renderer through the inputs that exist:** `base_color_map` and the four shine inputs (LCDSchema). **No input is added, no master changes, so no new Unreal runtime is owed** (`LOCAL_DELTAS.md`).
- **A per-article shine set needs no new rule:** `SkinMaps.md` §Shine maps already lets an article's recipe name its own file.
- **The nail rule exists** (each `Nail_Fitzpatrick*` is derived from its skin by one rule). The rig pairs nails by the Variant token (`rig.cast_for`), unchanged.
- **Contracts touched:** G8's size check (RD-P24-2) and `SkinMaps.md`'s *Size: 2048* line for this set (RD-OVS-2). The kit stays 2048: a contributor still paints at 2048.

### Decisions that bind

*One authoritative copy. Rulings are quoted where they are the authority.*

**Carried rulings:**
- **2026-11-01, OMF's session (recorded by date and content in the OVS doc):** OMF keeps the approach to realism; validate on one subject on today's hm08; this library hosts the phase.
- **RD-OVS-1 … 6 (the lead, 2026-11-01; the OVS doc's `## Resolved`):** the bar's tone (*"Tone, yes"*); 8K now, sizes tested later (*"start with 8k and then evalaute all that in later phases"*); the default age (*"Age, keep"*); the lead asks the platform for Studio's side (*"Yes... I will … proceed with what we can now"*); the lead supplies Krea 2 and FLUX.2 [klein] (Phase25's); two phases (*"Split and seed"*).
- **RD-SKM-1:** hm08 as `MakeHuman_Body_v01`. **RD-SKM-2, RD-P23-10:** no photograph or scan of a person in anything shipped; the bar stays local, its path is never written in a tracked file, and no sheet showing it is committed, published, served or snapshotted. **RD-SKM-5, RD-SYN-1:** no whole AI map. **RD-RO-2:** CC0.
- **RD-SKM-3:** colour through `base_color_map`, no new input. **RD-P21-3:** the measured tone stays the average.
- **Authored on the body, baked per layout** (the lead, 2026-10-26): the 8K maps are made in 3D, as the 2048 ones are.
- **RD-P22-17:** a skin wearing the shine maps carries no coat.
- **RD-CMT-4** puts the look verdict for a character material in the platform's look-dev scene. **RD-P23-9 is the precedent for running the library's own judge meanwhile, and RD-OVS-4 (*"proceed with what we can now so we have the tings to test when the studio is ready"*) reaches this phase directly.**
- **Pre-release, no versioning** (`AI_WorkingAgreement.md` §Settled practices): the new articles are `v01`, `candidate`.

**Superseded for this set, by a newer ruling on the same axis:**
- **RD-P21-5** (*the atlas stays 2048²*) → **RD-OVS-2** (8K). It stays for the 18 skins, the six lips and the shared shine maps.
- **RD-P22-2 / RD-P23-6** (*one shine set for every tone and structure*) → this subject's own shine set, as the seed set out and RD-OVS-2's *"different resolutions for different layers"* anticipates. The shared set stays for the 18.
- **RD-P21-2 / RD-P23-5** (*the tone's `Lips_` article carries the skin's map with its own finish*) → RD-P24-3 for this set, per OVS-8 and the platform's character model of 2026-11-01 (lips in the body). The six `Lips_*` stay.

**Decided here, unless the lead says otherwise:**
- **RD-P24-1 — The tone is the bar's face average, measured on the bar's own albedo at execute (24.2), not on the composed picture Phase23 used.** F-P24-1: that picture is the bar's colour divided by the platform's then-skin, a multiplier. The platform's fit report gives the head's median albedo as 0.505, 0.275, 0.178, between III and IV. The model fit is the nearer passing one (III's or IV's, both pass RD-P23-3's check); the maker prints it. B stays today's III (RD-OVS-1).
- **RD-P24-2 — G8 takes a fitted map whose size is the mesh's `map_size` times a power of two, on the same layout.** A mesh version is a UV layout (RD-P18-1), not a size, so `MakeHuman_Body_v01` stays one version; the 18 skins keep passing at 2048. The island check reads the 2048 islands at the map's scale. `run_all.py`'s wrong-size fixture (1024 for a 2048 mesh) still fails. This widens a check on the lead's ruling RD-OVS-2; it adds no gate. The kit stays 2048.
- **RD-P24-3 — The set's lips wear the skin article itself.** The bar wears its lips on the skin (OVS-8), and the platform's model puts the lips in the body. So the Lips part is cast with the subject's skin; the lip colour is the map's (as today) and the lip gloss is the subject's roughness map (a glossier lip zone). There is no `Lips_` article for this subject, and no coat on the lips (RD-P22-17). **The rig's cast takes the skin on the Lips part when no `Lips_<Variant>` exists for a fitted skin that declares it** (today it falls back to the Natural lips; a small `rig.cast_for` change). A and C are cast this way; B as shipped.
- **RD-P24-4 — The views and distances (OVS-Q2, as OMF recommended):** front, three-quarter and profile at ~1 m and ~40 cm; eye, lips and cheek-with-nose close-ups at ~40 cm; one lens. **Fixed at click 1; never changed after.** The existing four (`face`, `face34`, `hand`, `ear`) stay for other uses.
- **RD-P24-5 — Column A, at 8K, made locally** under the git-ignored `library/parity/`:
  - **colour:** the bar's 8K albedo held to its own tone (no change of tone: it IS the tone, RD-P24-1);
  - **shine:** the bar's specular map as the cavity map (it multiplies the shine, as `cavity_map` does); the shared relief, roughness and scatter maps, as A wore them at Phase23's click 1 and read as skin;
  - **the bar's scatter map** is read for the comparison; it is drawn only if it maps onto an existing input faithfully (execute's call, recorded). It has no relief map on hm08.
  - **EXR reading** is scratch-only (`uv run --with OpenEXR`, or the official Blender): the project gains no dependency for a picture that never enters the tree.
- **RD-P24-6 — The pigment fields are kept by being reproducible.** The maker writes the subject's melanin and blood fields (linear, 16-bit) to a folder given on the command line, git-ignored by default, and the provenance names the command. They are not tracked: they are derived from the maker's table and seed, and at 8K they would add hundreds of MB to LFS. *Skin Layers* and Phase25 call the maker.
- **RD-P24-7 — The 8K makers must run inside the box's memory, with room for other sessions.** Measured at 2048 (F-P24-2): colour 34 s and 3.2 GB peak, shine 74 s and 3.1 GB, both on one core. At 8K that scales to ~50 GB each, close to all of the box's memory, where the out-of-memory guard kills a process first. **Execute makes them work in float32 and/or in bands of rows, to a peak of about a third of the box's memory**, and records the measured time and peak. The shine maker's supersampling drops as the texels shrink (3 per axis at 2048 is coarser than 1 at 8K).
- **RD-P24-8 — The subject's name** follows Identity's grammar (six tokens; the Variant is the tone): **a Variant naming the measured tone, never a person** (the bar's likeness and name stay out, RD-SKM-2). Execute picks the word, checks it against `validate_material.py`, and pairs the nail by it.

### Risk lane — `build`

The controls this phase touches, each read on 2026-11-01:
- **G8** (`tools/validators/validate_recipe.py` `picture_errors` and the shine-map check): both refuse any size but `map_size`; RD-P24-2 widens that, with a test case. **Run `run_all.py` after the change, before any 8K map lands.**
- **What enumerates the skin folder:** the recipe gate, the catalog, thumbnails (`showcase.character_family` reads the Material token; `Skin` is known), `serve_to_stage.py`, the release lanes. Adding one skin and one nail is the shape Phase23 added twelve of.
- **`rig.cast_for`:** the lips-on-skin cast (RD-P24-3) is new; the Variant pairing for every other skin is unchanged.
- **The kit and the snapshot's *"Paint at 2048"* line:** unchanged (`make_kits.py`, `build_snapshot.py` read `map_size`, which stays).
- **The masters and the runtime:** untouched (§Reuse). The runtime's texture loader was read (F-P24-4).
- **The one irreversible risk is publication:** the repo is public, and the bar must never be committed, nor its path written. Controls: `.gitignore`'s `library/parity/`, explicit-path staging, RD-P23-10.
- **The box:** 8K makers near the RAM ceiling (RD-P24-7); Unreal shares the GPU (`ps -ef | grep "[U]nrealEditor"` before each launch).
- **Baseline:** `run_all.py` at `08da67b` (§Discovery Log). No change under `blender/addons/` or `tools/conformance/`, so `check_exporter.sh` is not owed.

Nothing here is authorization, secrets, a destructive migration or the public edge.

### Step list

- **24.1 — The judge.** The fixed views (RD-P24-4); A made locally at 8K (RD-P24-5); the lips-on-skin cast (RD-P24-3); B as shipped. **Click 1: the ruler.**
- **24.2 — The candidate at 8K.** G8's size rule (RD-P24-2); the makers at 8K inside memory (RD-P24-7); the bar's tone measured (RD-P24-1); the subject's colour fitted to the bar by region; its shine set fitted to the bar's specular, the lips glossed; its skin article; its pigment fields (RD-P24-6). **Click 2**, iterated.
- **24.3 — The set finished and served.** The nail article; provenance; thumbnails; the dev install re-served; the docs; the Blender scene. **Click 3.**

Time to the first click: 24.1 is views in one tool, three local pictures and a cast rule.

### Compact build map

- **24.1:**
  - `tools/parity/look.py`: the views (camera positions from the head's bounds and a fixed lens; profile from the key's side), `--reference` taking the bar's pictures as A at 8K with no tone change and its specular as the cavity map. Everything A writes stays under the output folder (RD-P23-10).
  - `tools/parity/rig.py` `cast_for` / `character_cast`: Lips on the skin when no `Lips_<Variant>` exists (RD-P24-3).
  - GPU: ~0.7 GB per distinct 8K picture in the runtime (F-P24-4); A, B and C together take a large share of the GPU's memory. If one launch will not hold them, render A, B and C in separate launches at one setting.
  - Run with `--width 1536`. **Before launching:** `ps -ef | grep "[U]nrealEditor"`.
- **24.2:**
  - `validate_recipe.py` G8 (both checks) + a test case; `run_all.py`.
  - `gen_synth_skin.py` / `gen_skin_maps.py` / `gen_skin_shine.py`: an output size (8192 for the subject, 2048 the default), float32 and bands (RD-P24-7); a subject row (structure, tone, fit); the pigment-field output (RD-P24-6); the shine maker's lip zone and region strengths.
  - The scratch solver (Phase23 23.2.9, git-ignored) re-run on the bar at 8K for `FACE` and the shine strengths; the subject's `FACE` row lands in the maker.
  - The subject's recipe, copied from `Skin_FitzpatrickIII`'s, its five maps named by article (`<Material><Variant>_basecolor_sUKN.png` and `…_roughness_…` etc.), then `uv run tools/converters/build_proof_subset.py <recipe>`.
  - LFS: the five 8K maps are ~150 MB together (scaled from 2048's ~9.3 MB). Learnings G2: compare pixels before committing a regenerated picture.
- **24.3:**
  - The nail recipe from `Nail_FitzpatrickIII`'s by the nail rule; provenance rows; `make_thumbnails.py`; `serve_to_stage.py` (it restarts the Stage daemon; close it after, memory *close what you open*).
  - The Blender scene: headless from the factory scene, opened detached.
  - `SkinMaps.md`, the ledger's P33/P34 rows, the Glossary if needed.
- **Tests:** `run_all.py` per step; G8's new case; one real-path smoke per click, which is the look view itself. No new gate.

### Open for the lead

*None.* RD-P24-1 … 8 are decided unless the lead says otherwise.

---

## Findings (discovery Pass 1, 2026-11-01)

- **F-P24-1 — The bar's tone is between III and IV, not paler than every tone.**
  - Phase23's F-P23-2 measured the composed 4096 picture's skin average (0.600, 0.527, 0.482) and read it as *"paler and far less red than any library tone"*.
  - That picture is a multiplier: its compose record divides the bar's head median albedo (0.505, 0.275, 0.178) by the skin the platform's character wore then (about tone II).
  - The library's III is 0.623, 0.433, 0.343 and IV 0.436, 0.227, 0.131. The bar's red/blue is 2.84 (III 1.82, IV 3.33).
  - Phase23 held the picture to III before comparing, so its verdicts stand; only the tone claim was wrong. RD-P24-1 measures the face's own average at execute, on the albedo.
- **F-P24-2 — The makers at 8K would not fit the box as written.** Probed at 2048 from a scratch folder, nothing written to the tree (`/usr/bin/time -v`):
  - colour (`fields` + `compose` III + `calibrate`): 34 s, peak 3.2 GB;
  - shine (`gen_skin_shine.py --out`, supersample 3): 74 s, peak 3.1 GB;
  - both single-threaded (≈100 % of one core). 16× the texels gives ~50 GB each. RD-P24-7.
- **F-P24-3 — The bar exists at 8K on this machine with colour, specular and scatter, and no relief.** The platform's fit of the scan to hm08 (2026-10-25) wrote float EXRs of the diffuse albedo, the specular and the scatter, each on the atlas at 8192² (~800 MB each) and on the face at 4096², and composed 8-bit-per-channel 8K colour pictures. The project's environment reads no EXR (neither `OpenEXR` nor `imageio`). Paths stay off the tree (RD-P23-10).
- **F-P24-4 — The look view takes 8K with no runtime change, at a GPU cost.** `MatterRuntimeGameMode::LoadTexture` decodes any PNG to linear float on the CPU and uploads `PF_FloatRGBA` with a full mip chain, cached per file; `Config/DefaultDeviceProfiles.ini` allows 16384. One 8K picture is ~0.7 GB on the GPU and ~2 GB of transient CPU memory while it loads.
- **F-P24-5 — G8 refuses any size but the mesh's `map_size`** (`picture_errors` and the shine-map check, both `im.size != (n, n)`), and `map_size` also drives the kit and the snapshot's paint instruction. Changing `map_size` would fail all 18 skins, so the rule widens instead (RD-P24-2).
- **F-P24-6 — Today's rig cannot cast the lips on the skin.** `rig.cast_for` casts `Lips_<Variant>` or the Natural lips; a skin with no `Lips_` pair gets the Natural article on the Lips part (RD-P24-3).
- **F-P24-7 — The consumers since the seed (fetched 2026-11-01):** the platform's research recorded OMF's answers (the skin ships its pigment fields; density per region in px/cm, room reserved; regions as labels) and that the platform's own skin phase is its half of this one, *"the lead confirms"* (its research, 2026-11-01). OMF's newest input asks it about the platform's five-part character and a later render body's UV layout. **Nothing in either is addressed to this library or changes this phase**; the pigment fields' shipping is *Skin Layers*' (OVS-6).

## Deferred

| What | To | What it consumes from this phase |
|---|---|---|
| The image model's skin, as column D | [Phase25](Phase25_AiSkinStructure.md) | the judge (views, distances, A at 8K, the lips-on-skin cast); the subject's tone and fit; the maker at 8K taking an outside pigment field; the pigment-field output (RD-P24-6) |
| Marks and makeup on this subject; shipping the pigment fields | *Skin Layers* | the subject's pigment fields and maker row; the shine set's zones |
| Other tones, people, ages | *Variety* | the passed recipe: the subject row, the fitted `FACE`, the shine strengths |
| Picture size, loading and performance; a size per layer | later phases (RD-OVS-2) | the set at 8K; G8's size rule |
| Studio's verdict and shine; the headset | the platform (P33, P34; its own skin phase) | the set as served |
| The re-bake onto a new body | OMF's body work, then the re-bake test | the maker at 8K, made in 3D |

## Depends on

- **Nothing outside this repo, for every click.** The bar is read locally (RD-P23-10). The platform's half runs on its own line.
- A dev snapshot and the push are the lead's word, at the close.

## Discovery Log

- **Seeded 2026-11-01** (`de4f5d9`) by `/research` on the lead's word; split the same day (`a7bb775`).
- **Pass 1 — 2026-11-01,** opened by the lead's *"/discovery Phase24"*.
  - **Examined:** the OVS research in full; Phase25's seed; Phase23 in full; `SkinMaps.md` in full; Identity's tokens; the ledger's P33–P35; the Roadmap's head; the makers' size handling (`gen_skin_maps.N`, `gen_synth_skin`, `gen_skin_shine`), `look.py`'s options and views, `rig.cast_for`, G8 in `validate_recipe.py`, `groups.PART_MESHES`, the runtime's texture loader and device profile; the bar's files and fit records on this machine; the platform's and OMF's commits since the seed (fetched).
  - **Learnings:** GitHub G2 (regenerated pictures and LFS) bears on 24.2's commits; Unreal U11 (a black scatter colour hangs the GPU) on A's scatter, if drawn. Blender B10–B11, B22 and ClaudeCode CC2 are carried by `LOCAL_DELTAS.md` for click 3. MaterialX and Storm: not touched (no master change; Storm is not a click here).
  - **Probed:** the makers' cost at 2048 (F-P24-2), from a scratch folder outside the tree.
  - **Baseline:** `run_all.py` at `08da67b`: **18 lanes, 18 PASS, none skipped.**
  - **The seed's questions, closed:** the 8K maker's cost → F-P24-2, RD-P24-7 · the look view's columns at 8K → F-P24-4, RD-P24-5 · where the pigment fields are kept → RD-P24-6. OVS-Q1 → one C row here (Phase25 adds D) · OVS-Q2 → RD-P24-4 · OVS-Q3 → RD-OVS-3.
  - **Tree:** ahead of origin by three unpushed commits at kickoff (two retro and research commits, and a sibling session's retro item landing during the pass); nothing to pull.
