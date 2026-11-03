# Research — Other ways to map a person onto the body: multi-view texturing, 3D reconstruction, multiview-to-UV

**Opened:** 2026-11-03 · **Mode:** research. It gathers and commits to nothing, and may run disposable probes on the lead's go. **Mnemonic:** `TDM` (ids `F-TDM-n`, `Q-TDM-n`, `RD-TDM-n`). **Status:** open, see the Status footer.
**Requested by:** the lead, 2026-11-03, verbatim: *"Looking at our skinmapping project... I am wondering if there are other ways to explore... might any of this be worth exploring?"*, with a pasted summary from another tool (*"AI Character Sheets → Humanoid Skinmaps"*): eight projects and four approaches, ranked.
**Altitude:** a **landscape of candidate routes to probe**, set beside the route Phase25 and Phase27 built. *(Pass 1–2 first read it as an audit that could close routes; the lead corrected that the same day: Pass 3, RD-TDM-1 … 4.)*
**Measured at:** `a2b70e0`, 2026-11-03. Every repo below was read at its origin on GitHub or Hugging Face the same day (licence files, code, model records), not from its README alone.

**Extends:**
- [`261014_R_SkinMaps.md`](261014_R_SkinMaps.md) F-SKM-28 … 30: the mesh-texturing tools as of 2026-10-14;
- [`Phase25_AiSkinStructure.md`](../Phases/Complete/Phase25_AiSkinStructure.md) §The routes, compared (route 2, *"Texture the mesh inside ComfyUI"*, not taken by RD-P25-11), F-P25-9;
- [`Phase27_AiBodySkin.md`](../Phases/Complete/Phase27_AiBodySkin.md) §The routes for the trunk, arms and legs.

---

## Current picture (for the lead)

**The proof of concept is not won yet, so every route on the list stays open and gets judged by pictures, not by the reasons this doc first gave** (RD-TDM-1 … 4). Today's `Tone34` is better than the original maps, but not good. The test that counts is **a complete map on hm08 with no seams and its details in the right places**, and that beats a sharper map that is badly placed.

**Pixal3D ran first, on the lead's choice (RD-TDM-5; Pass 4).** From the four-view picture the lead already liked, it built a textured body in **45 s** inside the lead's ComfyUI (built-in nodes, nothing compiled). That body sits on hm08 within 4.4 mm (median), and its colour copied onto hm08's layout gives **one continuous skin: no camera seams, the nipples, navel and groin crease in place, the tone held** (gains ~1). **Two defects:** the tops and soles of the feet came out purple-grey, and **the face is poor** (dark smears round the eyes and nostrils, soft doubled lips). The served face is far better. So the promising part is the body; a mixed map (Pixal3D's body, the served face) needs a neck join. Pictures: `library/parity/TDM_Pixal3D/show/` (local only, RD-P27-3).

**The other tools in the plan** (Pass 3), each giving a whole-body map to set beside `Tone34`:
1. **Hunyuan3D-Paint 2.1**: textures a given mesh from a reference picture. It makes its own UV layout, but on **hm08's own surface**, so its map copies across to hm08's layout in one bake.
2. **MV-Adapter**: textures a given mesh from a reference picture, guided by the mesh's shape, and **keeps hm08's UVs**.
3. **Pixal3D (multi-view)**: builds a textured body from the four-view picture Phase27 already has; hm08 is then wrapped onto it and the colour baked across.

**MV2UV** (painting straight into the UV layout) has no code or weights out; it is watched (F-TDM-5). **Waiting on:** the lead's look at Pass 4's pictures, and which way next (Q-TDM-3).

---

## The rulings this touches (quoted)

- **RD-SKM-1:** hm08 is the body every skin map is made for.
- **The lead at 25.1.8** (Phase25 §Decisions that bind), verbatim: *"you are cuting pasting, patching, matching, blending, when I think we should be trying to figure out how it can generate a full map"*. Said about one route's results (Phase25's first projection). **Not a ban on blending as a method** (RD-TDM-3).
- **RD-P25-11** (an agent's decision at Phase25 Pass 2, *"unless the lead says otherwise"*, not the lead's words): route 2's tools not taken. **Reopened by RD-TDM-1 and RD-TDM-2** for probing.
- **RD-P27-3:** no picture of an unclothed person is committed; probe pictures stay under git-ignored `library/parity/`.
- **RD-CMT-4:** a character's look is judged in the library's Unreal look view.

---

## Pass 1 — Each named project, read at its source (audit, 2026-11-03)

**Examined:** each project's repository tree and licence file on GitHub, the Hugging Face model record where there are weights, and the code path that handles UVs. All eight names exist; three were not found by a plain web search and were found on GitHub.

- **F-TDM-1 — The eight projects, as they are** *(facts only; the "can it run on hm08" column replaces the verdicts Pass 1 first wrote, Pass 3)*:

| Project | What it is (read) | Licence (read; a fact, not a filter — RD-TDM-1) | Works on hm08's UVs? | Can it run on hm08 now? |
|---|---|---|---|---|
| **MV-Adapter** (`huanngzh/MV-Adapter`) | An adapter that makes SDXL draw six consistent views of a given mesh, guided by its position and normal maps, from a text prompt or a **reference picture**; a texture pipeline projects them into the UVs and fills gaps. Trained on Objaverse objects. Last code push 2025-06-26. | Apache-2.0 (repo); base SDXL. | **Yes, kept by default** (`pipeline_texture.py`: `uv_unwarp: bool = False`). | **Yes** (probe 2). |
| **Hunyuan3D-Paint 2.1** (`Tencent-Hunyuan/Hunyuan3D-2.1`) | Tencent's multi-view PBR painter: a given mesh plus a reference picture → colour (and roughness and metal). | Tencent Hunyuan Community Licence (territory-limited; outputs not for training other models). | **It makes its own layout** (`textureGenPipeline.py` → `mesh_uv_wrap`, xatlas) **on the same surface**: xatlas splits vertices to cut seams but does not move them, so its map bakes across to hm08's layout exactly, surface to surface. | **Yes** (probe 1). |
| **Pixal3D** (`TencentARC/Pixal3D`, SIGGRAPH 2026) | Picture(s) → a new textured mesh, on TRELLIS.2. Multi-view inference since Sept 2026 (`inference_mv.py`), low-memory mode. | MIT, code and weights (repo `LICENSE`, `NOTICE`; Hugging Face record `mit`, not gated). | n/a: a new mesh; hm08 is wrapped onto it, then baked. | **Yes** (probe 3). |
| **ModelSheetTo3D** (`hjyoon02/ModelSheetTo3D`, Eurographics 2026) | Research code: rebuilds a cartoon character from a hand-drawn model sheet (TRELLIS plus image-model steps). | No licence file. | n/a: new mesh. | Possible; built for drawn cartoons, so after Pixal3D. |
| **Chameleon Warp** (`iss2g/chameleon-warp`) | Local browser app: wraps one mesh onto another **keeping the source's topology, vertex order and UVs**; landmarks clicked by hand. Days old. | MIT. | Carries hm08's UVs onto a rebuilt shape. | Yes, as probe 3's wrap step. |
| **AssetFurnace** (`Bingeljell/image-to-3dlab`) | A local studio around Pixal3D, TRELLIS.2 and Hunyuan3D, with install scripts and per-asset licence records. | Apache-2.0 (studio). | n/a. | A ready installer for probes 1 and 3, if it helps. |
| **PixelArtistry Pixal3D Multiview** | ComfyUI workflow: prompt → Qwen-Image front view → Qwen-Image Edit four-view turnaround → Pixal3D mesh. | MIT. | n/a. | Its turnaround is Phase27's four-view picture; its second half is probe 3. |
| **MV2UV** (arXiv 2603.15436, CVPR 2026) | Views used as **prompts** to a model that generates in UV space, filling unseen parts there. SDXL backbone; ~80,000 Objaverse objects; 1024² maps; takes a mesh *"with known UV mapping"*. | No code or weights found. | Yes, by design. | **No** — nothing released (F-TDM-5). |

- **F-TDM-2 — MV-Adapter keeps a mesh's UVs; F-P25-9 grouped it with tools that re-unwrap.** That part of the October record was wrong. Its views are 768 px (about 2.4 mm a pixel on the whole body at the default framing, inferred, not run) and are merged into the UVs by a weighted blend (`uv_exp_blend_alpha=3`). *(Pass 1 called both reasons to skip it; under RD-TDM-2 and RD-TDM-3 neither is.)* Its geometry guidance is what Phase25 and Phase27 lacked: the views are drawn **to hm08's shape**, so the details should land on hm08's features with no fit step.
- **F-TDM-3 — Hunyuan3D-Paint 2.1 re-unwraps, but on the given mesh's own surface** (read 2026-11-03). Pass 1 called the re-unwrap disqualifying; it is not, since a bake from its layout to hm08's on the same surface is one resample with no geometry to match. Memory: the pasted summary says ~21 GB for painting, near the GPU's whole memory, so ComfyUI's models must be freed first.
- **F-TDM-4 — Rebuilding the body (approach B) trades the fit for a wrap.** Pixal3D builds the body from the four views at once, so its texture is **one consistent person with no view seams by construction**; the open questions are how close its shape comes to hm08's and how well a wrap (Chameleon Warp, or a shrinkwrap in Blender) lines up the features. *(Pass 1 dismissed it for its extra steps; under RD-TDM-4 that is not a reason.)*
- **F-TDM-5 — MV2UV is the closest to generating a full map directly, and has nothing released.** Recheck on a code or weights release. The library's nearest form is the layout LoRA (RD-P25-12).

## Pass 2 — The four approaches, against what is built (2026-11-03)

| Approach (pasted) | What the library has | Next |
|---|---|---|
| **A** — AI texturing of the existing body (MV-Adapter, Hunyuan3D-Paint) | Not tried: Phase25's route 2 was set aside on reading (RD-P25-11), never run. | **Probe** (1, 2). |
| **B** — Rebuild the body from views, then transfer | Not tried. | **Probe** (3). |
| **C** — Generate the UV map directly from views | Phase25's route 5 (Krea painting the UV island) drew its own proportions (F-P25-11, F-P27-9). | Watch MV2UV; the layout LoRA stays the in-house form (RD-P25-12). |
| **D** — Segment, project, fix seams | Built in Phase25 and Phase27 (landmarks and outline, seams from the mesh). | The comparison column (`Tone34`). |

- **F-TDM-7 — The summary's "important considerations" match the library's own rules:** the final map in hm08's layout (RD-SKM-1); one consistent person in all views (why Phase27 draws four views in one picture); seams handled. Every probe below is judged on exactly those.

## Pass 3 — The lead's correction, and the probe plan (2026-11-03)

**The lead's response to Passes 1–2, as a note:** the doc closed promising routes for the wrong reasons. It treated a remark about one test as a standing ban (blending), attached *"no effect at all"* to a resolution argument the lead never made, counted an extra step as a reason to skip, and weighed licences although this is a proof of concept with no release in view (said many times). The lead is not happy with the results so far: `Tone34` beats the original maps, which were also poor, and the work has been slow. **What wins is a complete map with no seams and its details in place, even at lower resolution.**

**The agent's errors, checked:** the 25.1.8 words were said about one route's results; Pass 1 generalised them. *"No effect at all"* (27.2.2) was said about the seam panels of one click, not about resolution. RD-P25-11 was the agent's own decision, which the lead let stand, not a ruling.

**The probe plan** (one at a time; nothing in the repo; pictures under git-ignored `library/parity/TDM_*`; environments in scratch, torn down after, the scripts kept beside this doc):
- **Common input:** hm08's bare body (Phase27's bare cast), and the reference the lead already liked, Phase27's four-view picture `f4_s50_seed7.png` (its front view, or all four where a tool takes several).
- **Probe 1 — Hunyuan3D-Paint 2.1** on hm08 with that reference → its map baked across to hm08's layout.
- **Probe 2 — MV-Adapter** (image + geometry → views, SDXL) on hm08 with the same reference → a map in hm08's layout directly.
- **Probe 3 — Pixal3D multi-view** on the four views → a textured body → hm08 wrapped onto it → baked.
- **Shown:** each map on the bare character in the library's Unreal look view, beside `Tone34` and the reference picture, the same body views Phase27 used. Judged by the lead: complete? seams? details in place?
- **Cost:** about 40 GB of downloads in total (Hunyuan's ~20 GB, SDXL and the adapter ~10 GB, Pixal3D ~8 GB; a small share of the scratch disk's free space); two small CUDA builds for Hunyuan's rasteriser (minutes); each texturing run minutes on the GPU, which must be free of Unreal and ComfyUI's loaded models. Setup is the long part: roughly an hour per tool.

## Pass 4 — Probe 3 run first: Pixal3D multi-view on hm08 (2026-11-03)

**Run on the lead's choice (RD-TDM-5),** on the machine with Unreal. Scripts: [`261103_R_3DMapping_probe/`](261103_R_3DMapping_probe/). Pictures local only, under git-ignored `library/parity/TDM_Pixal3D/` (RD-P27-3).

- **F-TDM-8 — Pixal3D runs inside the lead's ComfyUI with no build.** ComfyUI v0.43.2 carries Pixal3D natively (`comfy_extras/nodes_trellis2.py`: `Pixal3DMultiViewConditioning`, the TRELLIS.2 stages) and ships the official template `3d_pixal3d_multi_views`. Five model files (Comfy-Org's repacks: the multi-view model int8, two VAEs, the DINOv3 encoder, BiRefNet) were added to the shared model folder. The template was run over ComfyUI's API with its sampler, remesh and bake settings unchanged (`run_pixal3d.py`); **45 s** for the whole chain.
- **F-TDM-9 — The input: Phase27's four-view picture `f4_s50_seed7.png`, as made** (no new generation). Its four orthographic views map one to one onto Pixal3D's rig (front, left = yaw 90, back, right = yaw 270; checked from `project_body.rot`). Each was framed **on the shared rotation axis**, the body's height 1/1.1 of a square frame, black background (`views.py`): **1.79 mm a pixel**. *(The template instead crops each view to its own outline, which would shift the views against each other.)* Field of view given as 20° (the rig's default) for orthographic views; not varied.
- **F-TDM-10 — Pixal3D's body fits hm08 closely.** Its mesh (painted, 350k vertices) was set upright by trying four turns (the right one 22 mm chamfer, the next 143 mm), then fitted by ICP with one scale (`transfer.py`): **hm08 → Pixal3D's surface 4.4 mm median, 12 mm at the 90th percentile, 31 mm at the 99th**; 14.8 % of texels sit more than 1 cm from it (the feet, the fingers' sides, the mouth's inside, the eyes' openings). Each hm08 texel took the colour of the nearest painted vertices. Pixal3D's colour (linear, as glTF stores it) needed only **×1.13 / 0.97 / 1.16** to hold the served body's mean: it kept the person's tone.
- **F-TDM-11 — What the look view shows** (`look.py --bare --body` and `--judge`, served shine, 1536 wide; columns: `Tone34` served · Pixal3D's whole map · Pixal3D's body with the served head; the default column is the `3d594fb` article, F-P27-6, not what ships):
  - **The body is one continuous skin:** no camera seam anywhere, down the sides, the spine or the limbs; the nipples, navel and groin crease where hm08's are; smoother and less blotchy than the served body.
  - **The feet are wrong:** the tops and soles are purple-grey (no view sees them squarely, the shapes differ by over 2 cm, and the views' dark ground shadow is near).
  - **The face is poor:** dark smears round the eyes and the nostrils, soft doubled lips. The views give the face ~1.8 mm a pixel and Pixal3D's head shape differs from hm08's there. **The served face is far better.**
  - **The mixed map** (Pixal3D's body, the served head) shows a tone step at the neck seam: it needs Phase27's neck join (`project_body.neck_join`).
- **Not tried:** another field of view; the textured GLB (4K bake) instead of the vertex colours; a second seed or picture; a fix for the feet.
- **Reproduce** (`<p>` = `library/parity`, the probe folder `<s>` = `docs/Planning/Research/261103_R_3DMapping_probe`; the lead's ComfyUI running, the five models in its model folders, `PIXAL3D_TEMPLATE` set to the template's path in ComfyUI's environment): `uv run --with scipy --with pillow python <s>/views.py <p>/P27_Probe/f4_s50_seed7.png <p>/TDM_Pixal3D/views` · `python3 -I <s>/run_pixal3d.py <p>/TDM_Pixal3D/views tdm_a 20` · `uv run --with scipy --with pillow --with trimesh python <s>/transfer.py <ComfyUI>/output/3d/tdm_a_painted_00001_.glb <p>/TDM_Pixal3D a` · `uv run python <s>/look_driver.py Skin_Tone34_Clean_Base_s001_v01 --bare --body --shine served --width 1536 --candidate "Tone34 served=<p>/TDM_Pixal3D/T_served.png" --candidate "Pixal3D whole map=<p>/TDM_Pixal3D/E_a_all.png" --candidate "Pixal3D body, served head=<p>/TDM_Pixal3D/E_a_body.png" --out <p>/TDM_Pixal3D/look_body` (and `--judge` for the face). `T_served.png` is the served map decoded × its `base_color_const`.

## Pass 5 — Where the face and feet defects come from (2026-11-03)

**The lead:** *"Pixal3d has no solve for the issues? Should we try other images that also have feet details?"*

- **F-TDM-12 — Both defects are in Pixal3D's own output, before the transfer.** A point render of its painted mesh (`rawlook.py`, local scratch) shows the black eye sockets, the doubled lips and the dark feet on Pixal3D's own body.
- **F-TDM-13 — The feet: the four eye-level views never see the soles, and see the tops only at a grazing angle; Pixal3D paints what it cannot see dark.** Run 1's cut-out also kept the ground shadow under the feet. Run 2 (`tdm_b`) cut each view along hm08's own outline + 2 cm (Phase27's `geom_*.npz`): the tops gained some skin, the undersides stayed black. **A better full-body picture alone will not fix it.**
- **F-TDM-14 — The face: the multi-view node scales every view to 1024 px** (`Pixal3DMultiViewConditioning`, `common_upscale` to 1024²), so in a full-body view the head gets ~130 px whatever the picture's resolution.
- **F-TDM-15 — Solves within Pixal3D (not yet run):**
  - **(a) A Pixal3D run per part, framed close:** four views of the head alone and of the feet alone, each filling the frame (~8× the pixels on the face). Each result is fitted and transferred onto hm08's head or feet as the body was. This is where *"other images with feet details"* applies: close four-views, all four at the same scale.
  - **(b) A view from above or below:** the ComfyUI node is a fixed eye-level rig (front, left, back, right); upstream's `inference_mv.py` takes any cameras (`transforms.json`), so a high view that sees the tops of the feet is possible there, or through the same internal call in a small custom node.
  - **(c) Mixed:** Pixal3D's body, the served face, and the feet from (a) or the maker, joined at the neck and ankles.

## Open questions

| Id | Question (as the lead would see it) | Recommendation |
|---|---|---|
| ~~Q-TDM-1~~ | ~~Library skins, or creators' own characters?~~ | *Withdrawn at Pass 3: the routes are probed for the library's hm08 map either way.* |
| ~~Q-TDM-2~~ → **RD-TDM-5** | ~~Run the three probes, Hunyuan first?~~ | *Answered: Pixal3D first.* |
| Q-TDM-3 | **After Pass 5: which way next?** (a) Pixal3D per part: close four-views of the head and of the feet from Krea, each run through Pixal3D and transferred (F-TDM-15 (a)); (b) Pixal3D's body + the served face, joined at the neck, feet from (a) or the maker; (c) go on to Hunyuan3D-Paint and MV-Adapter. | (a): it tests whether Pixal3D can carry the face and feet at all, and it answers the lead's feet question directly. |

## Resolved

The lead, 2026-11-03, on Passes 1–2 (recorded as meaning; see Pass 3):
- **RD-TDM-1 — Licences are not a filter while the concept is unproven.** No route is set aside for its licence until a proof of concept exists and release is on the table. Licence facts are still recorded.
- **RD-TDM-2 — A complete, seamless map with its details in place beats a sharper one that is badly placed.** Resolution is not a reason to skip a route.
- **RD-TDM-3 — One reaction of the lead's to one test is not a standing ruling.** A path is closed only when the lead is told plainly *"this closes X, because of your reaction to Y"* and agrees.
- **RD-TDM-4 — An extra step is not a reason to skip a route.** A library that claims to work is worth a probe.
- RD-TDM-1 … 4 reopen RD-P25-11 (route 2) for probing. The closed phase docs are not edited; this doc is where it stands.
- **RD-TDM-5 — Pixal3D first** (the lead, 2026-11-03: *"I am most intersted in Pixal3d .. .It is more current and if this works, it has potential for other uses with AIgen..."*). Answers Q-TDM-2. Run as Pass 4.

## Status

- **Passes captured:** 4 (2026-11-03): Pass 1, the eight projects read at their source; Pass 2, the approaches against what is built; Pass 3, the lead's correction (RD-TDM-1 … 4) and the probe plan; Pass 4, Pixal3D run on hm08 (RD-TDM-5).
- **Current direction:** Pixal3D's **body** is promising (one seamless skin, features in place, tone held); its face and feet are not. Hunyuan3D-Paint and MV-Adapter still to probe. Watch MV2UV.
- **Found:** Pixal3D runs in the lead's ComfyUI with no build, 45 s (F-TDM-8); its body fits hm08 to 4.4 mm median (F-TDM-10); what the look view shows (F-TDM-11). Earlier: MV-Adapter keeps a mesh's UVs (F-TDM-2); Hunyuan3D-Paint re-unwraps on the same surface (F-TDM-3); Pixal3D is MIT, code and weights (F-TDM-1).
- **Unverified:** Pixal3D on another seed, picture or field of view; Hunyuan3D-Paint and MV-Adapter on a body (not run); MV-Adapter's resolution figure (inferred); MV2UV's release status beyond a GitHub search and the paper.
- **Open with the lead:** the look at `library/parity/TDM_Pixal3D/show/` (16 pictures), and Q-TDM-3.
- **Left on the machine:** the five Pixal3D model files in the shared model folder (kept: the lead wants Pixal3D for other uses) and the probe's output under `library/parity/TDM_Pixal3D/` and ComfyUI's `output/3d/tdm_a_*`. ComfyUI, started by this run, stopped by its PID.
- **▶ Next:** the lead's look and Q-TDM-3.

## Sources

Read 2026-11-03:
- `github.com/huanngzh/MV-Adapter`: licence (API), `mvadapter/pipelines/pipeline_texture.py`, README.
- `github.com/Tencent-Hunyuan/Hunyuan3D-2.1`: `LICENSE`, `hy3dpaint/textureGenPipeline.py`, `hy3dpaint/utils/uvwrap_utils.py`.
- `github.com/TencentARC/Pixal3D`: `LICENSE`, `NOTICE`, README; `huggingface.co/api/models/TencentARC/Pixal3D` (licence `mit`, not gated, created 2026-04-30); arXiv 2605.10922.
- `github.com/hjyoon02/ModelSheetTo3D`: tree and README (no licence file).
- `github.com/iss2g/chameleon-warp`: README, licence (API).
- `github.com/Bingeljell/image-to-3dlab` (AssetFurnace): README and backend table.
- `github.com/pixelartistry/PixelArtistry-Pixal3D-Multiview`: README.
- MV2UV, arXiv 2603.15436 (abstract and HTML), CVPR 2026 poster page; GitHub repository search (no result).
