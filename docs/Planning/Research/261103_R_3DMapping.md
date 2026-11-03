# Research — Other ways to map a person onto the body: multi-view texturing, 3D reconstruction, multiview-to-UV

**Opened:** 2026-11-03 · **Mode:** research. It gathers and commits to nothing. **Mnemonic:** `TDM` (ids `F-TDM-n`, `Q-TDM-n`, `RD-TDM-n`). **Status:** parked, see the Status footer.
**Requested by:** the lead, 2026-11-03, verbatim: *"Looking at our skinmapping project... I am wondering if there are other ways to explore... might any of this be worth exploring?"*, with a pasted summary from another tool (*"AI Character Sheets → Humanoid Skinmaps"*): eight projects and four approaches, ranked.
**Altitude:** an **audit** of outside tools against the route the library has already built and served (Phase25, Phase27). Not a design pass: the design is settled and shipped as `Tone34`.
**Measured at:** `a2b70e0`, 2026-11-03. Every repo below was read at its origin on GitHub or Hugging Face the same day (licence files, code, model records), not from its README alone.

**Extends, does not replace:**
- [`261014_R_SkinMaps.md`](261014_R_SkinMaps.md) F-SKM-28 … 30: the mesh-texturing tools as of 2026-10-14;
- [`Phase25_AiSkinStructure.md`](../Phases/Complete/Phase25_AiSkinStructure.md) §The routes, compared (route 2, *"Texture the mesh inside ComfyUI"*), F-P25-9 and F-P25-12 (another agent's write-up, the same family as today's);
- [`Phase27_AiBodySkin.md`](../Phases/Complete/Phase27_AiBodySkin.md) §The routes for the trunk, arms and legs.

---

## Current picture (for the lead)

**Short answer: nothing on the list beats what is built for the library's skins, and two of the four approaches are what the library already does.** One method is worth watching; one tool might help Phase28 only if Krea fails there; the rest serve a different job, making a character's own body from a picture.

- **The pasted summary's main question, "rebuild the 3D character first, or texture the existing body?", was settled in October:** the body is fixed (RD-SKM-1, hm08), so the library textures hm08. **Its approach D is close to what Phase25 and Phase27 built** (pictures fitted to hm08 by landmarks and outline, projected, a hard cut between views). **Its approach A is Phase25's route 2,** not taken (RD-P25-11).
- **MV-Adapter** (approach A, its "recommended first experiment") keeps hm08's UVs, which the library's October record got wrong (F-TDM-2). But it paints with SDXL at 768 px a view, about 2.4 mm a pixel on the whole body. That is **coarser than the four-view picture you already judged "no effect at all" at 1.67 mm** (27.2.2). It also blends six views, which you ruled out at 25.1.8. **Not worth a probe for the body.**
- **Hunyuan3D-Paint 2.1** still re-unwraps the mesh (read in its code today), and its licence still does not apply in the EU, the UK or South Korea. **Out, as before** (F-TDM-3).
- **Pixal3D, ModelSheetTo3D, Chameleon Warp, AssetFurnace and PixelArtistry** (approach B) build **a new body** from a character sheet. That body's shape is not hm08's, so its skin would have to be wrapped back onto hm08 and baked: two more resamplings than today's route, through a model that repaints Krea's colours at its own resolution. **For the library's skins this is a longer road to the same place** (F-TDM-4). For a creator who wants *their* character's shape, it is the right family, but that is the asset tooling's or the platform's job, not the library's (Q-TDM-1).
- **MV2UV** (approach C) is the one idea that matches what you asked for at 25.1.8 (*"figure out how it can generate a full map"*): the views guide a model that paints straight into the UV layout, with no projection and no blending. **No code, no weights, trained on objects, 1024² output.** **Watch it, do not build it** (F-TDM-5). The library's own version of the idea is the layout LoRA it already keeps as a fallback (RD-P25-12).

**Nothing to build now and no Roadmap seed.** The one question for you is Q-TDM-1: was the pasted list about the library's skins, or about creators making their own characters?

---

## The rulings this touches (quoted)

- **RD-SKM-1:** hm08 is the body every skin map is made for. Its layout is fixed.
- **The lead at 25.1.8** (Phase25 §Decisions that bind), verbatim: *"figure out how to wrap a realistc skin on a 3D model … trying to figure out how it can generate a full map"*; not *"cuting pasting, patching, matching, blending"*.
- **RD-P25-15** (the lead: *"MUCH BETTER! YES"*): the face is one front picture fitted by landmarks and projected through one camera.
- **RD-P27-5** (the lead, on `f4_s50_seed7.png`: *"that one looks really good"*): the body is hm08's render shown four times in one picture, repainted by Krea; each view fitted, then each texel taken from the one view that faces it most squarely. Several views are allowed, **blending them is not**.
- **RD-P27-6** (the lead: *"3 looks more real, marks are right"*): the skin finer than ~3 mm comes from close cameras.
- **RD-P25-11** (decided at Phase25 Pass 2, *"unless the lead says otherwise"*, so an agent's call the lead let stand, not the lead's own words): route 2's tools are not taken. Its stated reasons: they blend views or re-unwrap hm08, and the best-known one's licence does not apply in the EU, the UK or South Korea.
- **RD-P25-12:** a layout LoRA trained on the maker's own maps is the fallback, on the lead's word only.
- **RD-AIS-3** and the lead's framing beside it (recorded, not ruled): the pipeline is *"something THEY [creators] could run to make their characters"*.
- **RD-RO-2:** the library ships CC0.

---

## Pass 1 — Each named project, read at its source (audit, 2026-11-03)

**Examined:** each project's repository tree and licence file on GitHub, the Hugging Face model record where there are weights, and the code path that handles UVs. All eight names exist; three were not found by a plain web search and were found on GitHub.

- **F-TDM-1 — The eight projects, as they are:**

| Project | What it is (read) | Licence (read) | Keeps hm08's UVs? | Fits the library's skin? |
|---|---|---|---|---|
| **MV-Adapter** (`huanngzh/MV-Adapter`) | An adapter that makes SDXL (or SD2.1) draw several consistent views, guided by the mesh's position and normal maps; a texture pipeline projects them into the UVs and fills gaps. Trained on Objaverse objects. Last code push 2025-06-26. | Apache-2.0 (repo). Its base model is SDXL. | **Yes by default** (`pipeline_texture.py`: `uv_unwarp: bool = False`). | No: 768 px views, six views blended (F-TDM-2). |
| **Hunyuan3D-Paint 2.1** (`Tencent-Hunyuan/Hunyuan3D-2.1`) | Tencent's multi-view PBR painter. | Tencent Hunyuan Community Licence: *"DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA"*; §5(b) no using outputs *"to improve any other AI model"*. | **No**: `textureGenPipeline.py` calls `mesh_uv_wrap` (xatlas) on every mesh. | No (F-TDM-3). |
| **Pixal3D** (`TencentARC/Pixal3D`, SIGGRAPH 2026) | Image(s) to a new textured mesh, built on TRELLIS.2. Multi-view inference released Sept 2026 (`inference_mv.py`); a low-memory mode exists. | **MIT for the code and the weights** (repo `LICENSE` and `NOTICE`; the Hugging Face record says `mit`, not gated). One ComfyUI wrapper calls it "academic-only"; the source does not. | n/a: it makes a new mesh. | Only through approach B (F-TDM-4). |
| **ModelSheetTo3D** (`hjyoon02/ModelSheetTo3D`, Eurographics 2026) | Research code: rebuilds a cartoon character from a **hand-drawn** model sheet (TRELLIS plus image-model steps). | **No licence file**, so no grant to use it. | n/a: new mesh. | No. |
| **Chameleon Warp** (`iss2g/chameleon-warp`) | A local browser app: wrap one mesh onto another keeping the source's topology, vertex order and UVs; deformation transfer; garment refit. Three stars, days old. | MIT. | It is the tool that would carry hm08's UVs onto a rebuilt shape. | Only inside approach B. |
| **AssetFurnace** (`Bingeljell/image-to-3dlab`) | A local studio for making game characters from a picture: Pixal3D, TRELLIS.2, Hunyuan3D, auto-rig, animations; records every asset's licences. | Apache-2.0 (the studio); each engine under its own. | n/a: new meshes. | No; a creator's tool. |
| **PixelArtistry Pixal3D Multiview** | A ComfyUI workflow: prompt → Qwen-Image 2.1 front view → Qwen-Image Edit draws a four-view turnaround in one row → Pixal3D builds a mesh. | MIT (workflow). | n/a. | Its first half is what Phase27 already does with Krea (four views in one picture). |
| **MV2UV** (arXiv 2603.15436, CVPR 2026) | Views from a multi-view model used as **prompts** to a model that generates in UV space, filling unseen parts there. SDXL backbone; ~80,000 Objaverse objects; 1024² maps; takes a mesh *"with known UV mapping"*. | **No code or weights found** (no repo on GitHub, no link in the paper). | Yes, by design. | Not available (F-TDM-5). |

- **F-TDM-2 — MV-Adapter keeps the mesh's UVs; F-P25-9 grouped it with tools that re-unwrap.** That part of the October record was wrong and is corrected here (the phase doc is closed and not edited). The verdict does not change, for two measured reasons:
  - **Resolution.** Six orthographic views at 768 px, framed at 1.1 × the mesh's size (`camera_ortho_scale` default, assuming the mesh is scaled to unit size, which the defaults imply; not run): on a 1.7 m body that is about **2.4 mm a pixel**. Phase27's four-view picture is 1.67 mm a pixel, and the lead read it as *"no effect at all"* on the skin (27.2.2), which is why the close cameras exist (RD-P27-6).
  - **Blending.** The views are merged into the UVs by a weighted blend (`uv_exp_blend_alpha=3`, all six views weighted equally), the step the lead ruled out at 25.1.8. The library takes each texel from one view only.
  - Also: the skin would be SDXL's, not Krea's (RD-AIS-1), and the model learned from objects, not people.
  - **One narrow use, not proposed:** its geometry-guided views hold a mesh's pose by construction. If Phase28's Q-P28-1 finds Krea will not keep hm08's fingers in place at a strength that repaints the skin, a geometry-guided view is one way to hold them, with Krea repainting on top. Phase28's discovery would weigh it beside a geometry control (Phase25 RD-P25-10 (b)).
- **F-TDM-3 — Hunyuan3D-Paint 2.1 is unchanged since October.** Its paint pipeline still re-unwraps every mesh (read in `textureGenPipeline.py` and `uvwrap_utils.py`, 2026-11-03), and its licence still excludes the EU, the UK and South Korea. §5(b) adds a further conflict: its outputs may not be used to improve another model, which would rule them out of the layout LoRA RD-P25-12 keeps as a fallback. The pasted summary's *"~21 GB VRAM"* was not checked: the tool is out before memory matters.
- **F-TDM-4 — Rebuilding the body (approach B) adds resampling steps and fixes nothing the library has left open.**
  - The chain would be: Krea's character sheet → Pixal3D builds a mesh and **paints its own texture** from the sheet → Chameleon Warp wraps hm08 onto that mesh → the texture is baked across into hm08's layout. Krea's skin is resampled at least twice, and the second model's texture is its own re-painting of the picture, at its own resolution.
  - Today's route fits each picture **directly to hm08's render** (landmarks and outline, 27.1: hm08's pixels on the background fell to 0.00–0.08 % per view) and projects once. The correspondence problem B solves in 3D is already solved in 2D, one step shorter.
  - What B would add is **the character's own shape**. The library has no use for it, since hm08 is fixed (RD-SKM-1). A creator's tool would (Q-TDM-1).
  - The light painted into the sheet comes along in every case. Phase27 had to divide it out (27.1.2) and the portability question is still open ([`261102_R_SkinPortability.md`](261102_R_SkinPortability.md)). Rebuilding the body does not help there.
- **F-TDM-5 — MV2UV is the method closest to the lead's stated aim, and none of it can be used.**
  - Its idea is the one the lead asked for at 25.1.8: the model generates the map in UV space, with views only as guidance, so nothing is projected, cut or blended.
  - Measured against the library: no code or weights (2026-11-03); trained on objects; 1024² maps, where the library makes maps at 4K and 8K; never shown on skin or a person.
  - **The library's own form of the idea already exists as a fallback:** a layout LoRA trained on the chain's maps (RD-P25-12), which teaches Krea hm08's layout directly. MV2UV's architecture (a UV-space model looking up the views through attention) is more than a LoRA, and needs training data the library does not have.
  - **Recheck when:** a code or weights release, or a human-texture result.

## Pass 2 — The four approaches, against what is built (2026-11-03)

- **F-TDM-6 — Where each approach stands:**

| Approach (pasted) | What the library has | Verdict |
|---|---|---|
| **A** — AI texturing of the existing body (MV-Adapter, Hunyuan3D-Paint) | Phase25's route 2, not taken (RD-P25-11). Phase27's four-view picture is the library's version: one Krea picture of four views of hm08's own render, fitted, one view per texel. | Not taken: coarser, blended, a different model (F-TDM-2, F-TDM-3). |
| **B** — Rebuild the body from views, then transfer | Not needed: hm08 is fixed, and the fit to its render already exists (27.1). | Not for the library (F-TDM-4). A creator's route (Q-TDM-1). |
| **C** — Generate the UV map directly from views | The aim of 25.1.8; Phase25's route 5 tried painting in UV space and found the model draws its own proportions (F-P25-11, F-P27-9). The layout LoRA is the fallback (RD-P25-12). | Watch MV2UV (F-TDM-5). |
| **D** — Segment, project, fix seams by inpainting | **Built**, in the library's own form: landmarks and outline instead of segmentation, the seams decided on the mesh (RD-P27-1), levelled rather than inpainted. | Done (Phase25, Phase27). |

- **F-TDM-7 — The summary's "important considerations" are already the library's rules:** *"Let AI generate appearance, not define the final atlas"* is RD-SKM-1 and the maker's structure (the picture becomes pigment, `Tone34`). *"Front, back and side images must describe the same person"* is why Phase27 draws the four views in one picture (F-P27-11). *"Seam correction"* is RD-P27-1 and 27.2.1's measured seams.

## Open questions

| Id | Question (as the lead would see it) | Recommendation |
|---|---|---|
| Q-TDM-1 | **Was the pasted list about the library's skins, or about creators making their own characters** (their own body shape, from a character sheet)? | **If the library's skins:** nothing here is worth a probe; Phase28 goes on as planned. **If creators' characters:** approach B is the right family (Pixal3D is MIT, code and weights), but it makes a new body, not a skin, so it belongs to the asset tooling or the platform, where characters are made (F-AIS-2). This repo would only supply the skin for it. |

## Resolved

*(none yet)*

## Status

- **Passes captured:** 2 (2026-11-03): Pass 1, the eight projects read at their source; Pass 2, the four approaches against what Phase25 and Phase27 built.
- **Current direction:** **park.** Nothing on the list improves the library's hm08 skins. Approach D is built; A is coarser and blends; B solves a problem the fit to hm08's render already solves; C (MV2UV) is the right idea with nothing released.
- **Found:** MV-Adapter keeps a mesh's UVs (F-TDM-2, correcting F-P25-9); Hunyuan3D-Paint 2.1 still re-unwraps and is still territory-limited (F-TDM-3); Pixal3D is MIT for code and weights (F-TDM-1).
- **Unverified:** MV2UV's release status beyond a GitHub search and the paper (2026-11-03); MV-Adapter's skin quality on hm08 (not run: ruled out by resolution and blending, not by a picture); Pixal3D's texture resolution (not needed for the verdict).
- **Watch:** MV2UV — recheck on a code or weights release. MV-Adapter's geometry-guided views — only if Phase28's Q-P28-1 fails (F-TDM-2).
- **Open with the lead:** Q-TDM-1.
- **▶ Next:** none in this repo. Phase28 (AI Hands and Feet) is next on the Roadmap; its discovery may read F-TDM-2's last point.

## Sources

Read 2026-11-03:
- `github.com/huanngzh/MV-Adapter`: licence (API), `mvadapter/pipelines/pipeline_texture.py`, README.
- `github.com/Tencent-Hunyuan/Hunyuan3D-2.1`: `LICENSE`, `hy3dpaint/textureGenPipeline.py`, `hy3dpaint/utils/uvwrap_utils.py`.
- `github.com/TencentARC/Pixal3D`: `LICENSE`, `NOTICE`, README; `huggingface.co/api/models/TencentARC/Pixal3D` (licence `mit`, not gated, created 2026-04-30); arXiv 2605.10922.
- `github.com/hjyoon02/ModelSheetTo3D`: tree and README (no licence file).
- `github.com/iss2g/chameleon-warp`: README, licence (API).
- `github.com/Bingeljell/image-to-3dlab` (AssetFurnace): README and backend licence table.
- `github.com/pixelartistry/PixelArtistry-Pixal3D-Multiview`: README.
- MV2UV, arXiv 2603.15436 (abstract and HTML), CVPR 2026 poster page; GitHub repository search (no result).
