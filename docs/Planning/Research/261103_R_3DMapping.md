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

**Three tools can be run on hm08 now, each giving a whole-body map to set beside `Tone34`** (Pass 3, the probe plan):
1. **Hunyuan3D-Paint 2.1**: textures a given mesh from a reference picture. It makes its own UV layout, but on **hm08's own surface**, so its map copies across to hm08's layout in one bake.
2. **MV-Adapter**: textures a given mesh from a reference picture, guided by the mesh's shape, and **keeps hm08's UVs**.
3. **Pixal3D (multi-view)**: builds a textured body from the four-view picture Phase27 already has; hm08 is then wrapped onto it and the colour baked across.

**MV2UV** (painting straight into the UV layout) has no code or weights out; it is watched (F-TDM-5). **Waiting on:** the lead's go for the probes (Q-TDM-2).

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

## Open questions

| Id | Question (as the lead would see it) | Recommendation |
|---|---|---|
| ~~Q-TDM-1~~ | ~~Library skins, or creators' own characters?~~ | *Withdrawn at Pass 3: the routes are probed for the library's hm08 map either way.* |
| Q-TDM-2 | **Run the three probes**, in the order 1 (Hunyuan) → 2 (MV-Adapter) → 3 (Pixal3D), each shown as soon as it has a map? | Yes. Hunyuan first: the most complete texturer of the three, and the quickest test of the core question (does a tool that paints *on the mesh* place details right with no fit step). |

## Resolved

The lead, 2026-11-03, on Passes 1–2 (recorded as meaning; see Pass 3):
- **RD-TDM-1 — Licences are not a filter while the concept is unproven.** No route is set aside for its licence until a proof of concept exists and release is on the table. Licence facts are still recorded.
- **RD-TDM-2 — A complete, seamless map with its details in place beats a sharper one that is badly placed.** Resolution is not a reason to skip a route.
- **RD-TDM-3 — One reaction of the lead's to one test is not a standing ruling.** A path is closed only when the lead is told plainly *"this closes X, because of your reaction to Y"* and agrees.
- **RD-TDM-4 — An extra step is not a reason to skip a route.** A library that claims to work is worth a probe.
- RD-TDM-1 … 4 reopen RD-P25-11 (route 2) for probing. The closed phase docs are not edited; this doc is where it stands.

## Status

- **Passes captured:** 3 (2026-11-03): Pass 1, the eight projects read at their source; Pass 2, the approaches against what is built; Pass 3, the lead's correction (RD-TDM-1 … 4) and the probe plan.
- **Current direction:** **probe** Hunyuan3D-Paint 2.1, MV-Adapter and Pixal3D on hm08, each map judged beside `Tone34` in the look view. Watch MV2UV.
- **Found:** MV-Adapter keeps a mesh's UVs (F-TDM-2, correcting F-P25-9); Hunyuan3D-Paint re-unwraps on the same surface, so its map bakes across exactly (F-TDM-3); Pixal3D is MIT, code and weights (F-TDM-1).
- **Unverified:** every tool's look on a human body (none run); MV-Adapter's resolution figure (inferred from defaults); Hunyuan's memory need (from the pasted summary); MV2UV's release status beyond a GitHub search and the paper.
- **Open with the lead:** Q-TDM-2 (the go for the probes).
- **▶ Next:** on the go, probe 1.

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
