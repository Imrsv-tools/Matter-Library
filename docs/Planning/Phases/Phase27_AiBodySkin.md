# Phase27 — AI Body Skin

**Status:** BRIEF READY (2026-11-02, the close of Pass 2): the route is the four-view picture (RD-P27-5, on the lead's verdict); `/execute` starts at 27.1, the fit. *Before:* IN DISCOVERY (Pass 2, after the lead's *"mounted"*: the routes probed, F-P27-9 … 13). *Pass 1:* 2026-11-02, opened by the lead's *"/discovery Phase27"* at `9935a6e`. *Before:* SEEDED (2026-11-02, `9935a6e`), on the lead's *"Seed phase 27 as the body.."*. It runs **after Phase25**, whose chain it reuses; its execute waits for Phase25's 25.2.
**Lane:** `build` (§Risk lane; read against the tree this pass).
**Measured at:** `9935a6e`, on **the machine with Unreal**; Phase25's 25.2 was live in a sibling session (its doc and three `tools/converters/fit/` files uncommitted; none touched here).
**Seeded from:** [`Phase25_AiSkinStructure.md`](Phase25_AiSkinStructure.md): §Pass 3 hand-off (*"what about the rest of the body?"*, ruled 2026-11-02), RD-P25-15 (the face's front projection), F-P25-16 (one coordinate field), RD-P25-16 (the neck waits for the body), F-P25-18 (Annotated Skin), §Deferred (the body islands row). Pass 1's probe: [`Phase27_AiBodySkin_probe/`](Phase27_AiBodySkin_probe/) (the atlas's islands and seams, measured from the mesh; no picture of a person).

## Outcome

**An image model's picture of a real person's body becomes the body's skin in the body's own layout, joined to Phase25's head with no visible seam at the neck, the wrists, the ankles, or down the back and the limbs, and judged beside the maker's body on the same unclothed character. If it wins, the maker turns it into a calibrated skin structure, as Phase25 does for the head.**

*(Confirmed at Pass 1, one change: the seed's "neck, shoulders or arms" named seams that are not where the mesh has them. Measured, hm08's seams are the neck, the wrists, the ankles and the body island's own cut down the spine and along the legs and arms (F-P27-2); there is no shoulder seam.)*

---

## The Brief

*Written at the close of Pass 2 (2026-11-02).*

### What this phase builds, in one paragraph

**The body's skin comes from the model's picture of a person; every seam is decided on the mesh.** hm08's body is one island holding the trunk, arms and legs (58 % of the skin), laid out as a person seen from the front with the back split down the spine to the island's outer edges; the hands and feet are their own islands (F-P27-1, F-P27-3). Phase25's method carries over where a camera can see: a picture matched to hm08's render by landmarks and its silhouette, projected through that one camera, and one coordinate field carrying the rest, nothing blended (RD-P25-15, F-P25-16). **What does not carry over is the back:** no front camera sees it. Pass 2 measured the routes (§The routes): the model keeps hm08's pose and build best when it repaints hm08's own render shown **four times in one picture** (front, profile, back, profile), and each body texel then takes its colour from the view that faces it most squarely (F-P27-11). The lead judged that picture *"really good"* and its projection onto hm08 misaligned (RD-P27-5): the model's outline differs from hm08's in each view, so **each view is fitted to hm08's render (landmarks and the outline) before it is projected** (F-P27-12). That fit is 27.1's work and its click. The judge is the look view with an **unclothed** cast and body cameras, which do not exist yet (F-P27-5). Everything at 2K first (RD-P25-20), which a 2 MP full-body picture already matches on the body (F-P27-4). The genitals and groin stay the maker's plain skin (RD-SKM-4).

### The routes for the trunk, arms and legs (measured at Pass 2)

| # | Route | Verdict | Why (measured) |
|---|---|---|---|
| B4 + D | **hm08's render, four views in ONE picture** (front, profile, back, profile), repainted by Krea at 0.5; each texel from the view facing it most squarely, a hard cut, nothing blended; **each view fitted to hm08's outline first** (to build) | **Taken** (RD-P27-5); the fit is 27.1 | Krea kept hm08's build and pose and obeyed *"bald"*; one person in all four views; 97.6 % of the body seen, **6.5 % at a grazing angle** (F-P27-11). Left: doubled contours where the model's outline differs from hm08's (F-P27-12). |
| B2 + D | The same with two views (front, back) | Not taken | **20 % of the body seen only at a grazing angle** (under 0.3, where Phase25's cheek streaked), the sides of the trunk, arms and legs; and Krea drew a larger bust than hm08's at 0.5–0.8 (F-P27-10). |
| A | **The body island painted in UV space** (Phase25's route 5) | **Out** | As on the head: from 0.6 Krea draws a front-view torso in its own proportions, not the unrolled layout; arms shortened, the split back not drawn as a back, underarm hair and anatomy painted (F-P27-9). |
| C | The front only; the back the maker's | Fallback only | A seam down each side: the defect the phase exists to remove. |

**The hands** (2.3 % each) take the face's method, one camera each, hand landmarks (MediaPipe's hand landmarker, 21 points) and the silhouette; **the nails are not the map's** (the Nails part wears its own article, `SkinMaps.md` §What the map must show), so only the knuckles and the creases must land. **The feet** (2.7 % each): the same, with the silhouette only (no foot detector is known). Both are 27.2.

### Rides on

| `CoreMechanisms.md` row | What in this phase rides it | The peer we follow |
|---|---|---|
| 1 — a body map larger than 2048 inside the machine's memory | the structure step only (the maker composing the body from the model's field at 8K), after the 2K work | `gen_synth_skin.compose_banded`, as Phase25's 25.2 uses it |
| NEW — the lead rules | **a picture projected onto the mesh through one camera, the rest carried by one coordinate field** | Phase25's chain is not a row yet (Phase25 has not closed): `tools/converters/fit/project_face.py` (`field`, `landmarks`, `ears`) is the peer, followed, not re-written |

Row 2 (makeup on the atlas) is not met.

### First human test

**Where:** the machine with Unreal (every compared tool runs there).
- **The surface:** the library's look view (`tools/parity/look.py --judge`), with **an unclothed cast** (the rig's character without the suit and shoes, and without the faces they delete) and **body views**, both new (F-P27-5): the whole body front, back and profile at ~2.5 m; the trunk front and back at ~1 m; the neck and shoulder at 40 cm (the head seam); a wrist and an ankle at 40 cm; the back of the hand. Never Blender (RD-CMT-4). One labelled picture at a time, at native resolution.
- **The columns:** C (`Skin_Tone34_Clean_Base_s001_v01`, the maker's body) · D (the four-view picture, fitted and projected, with Phase25's D head, so the neck seam shows). C and D wear the working shine (Phase25's `--shine neutral`). **No scanned bar for the body** (OVS-7): judged by eye.
- **Click 1 (27.1) — is the fitted body aligned?** *What the lead can say after:* *"D's body is the four-view picture's skin and it sits on hm08: no doubled contours, nothing off"*, or where it is off. **The reference already judged:** `f4_s50_seed7.png` (*"that one looks really good"*); the click asks whether the body on hm08 now looks like it. **Before the click the agent measures** the share of hm08's pixels on the model's background per view (1.2–6 % unfitted, F-P27-10) and looks at every view for doubled contours. **If the fit cannot align it,** 27.2 does not start on the agent's word: the next candidates are a geometry control holding the outline (Phase25's RD-P25-10 (b)) or a layout LoRA (RD-P25-12, the lead's word only).
- **Click 2 (27.2) — the seams:** *"I cannot find the seams"* at the neck, the wrists and the ankles, or which one shows.
- **One picture per stop**, opened with the handback that asks about it, the question naming the file and each column.
- **Can the surface show it?** At 2K the body's texel is ~0.8 mm (0.4–1.3 mm across the body, F-P27-4); through the rig's lens (50 mm on a 36 mm aperture) at 1536 wide, a view framing the whole body is ~1–2 mm a pixel (the distance set by the frame's height), the 40 cm seam views ~0.2 mm. The seams and the skin read at 1 m and 40 cm; the full views carry the overall look.
- **The pictures stay local.** An unclothed person drawn by a model is never committed to this public repo (RD-P27-3): they are written under the git-ignored `library/parity/P27_*` and opened for the lead with `xdg-open`, their paths in the handback.

### In now

- The unclothed judge: the bare cast and the body views (27.1).
- The body chain as a library tool, `tools/converters/fit/project_body.py` (new; Pass 2's `body.py` and `body4.py` ported): the four views of hm08 rendered as one picture, the generation, **the fit per view**, the projection (each texel from the view facing it most squarely) (27.1).
- The groin held to the maker's plain skin (RD-P27-2) (27.1).
- The seams: the neck (with Phase25's head), the wrists and the ankles, each read from the mesh (RD-P27-1); the hands and the feet (27.2).
- If D wins (27.3, 27.4): the structure (the maker composing the body from D's field, as 25.2 does for the face), the lead's re-ruling, the set served.

### Not now

- Other tones, people and ages (*Variety*). The 4K test and 8K (RD-P25-20). A layout LoRA (RD-P25-12, on the lead's word only). A raw AI map shipped as is (RD-SYN-1). Anatomical detail of any kind (RD-SKM-4: a separate opt-in package outside this repo, none planned). A body bar (OVS-7). Studio and the headset.
- **Annotated Skin** as the seam map: not needed, the mesh gives every seam exactly (RD-P27-1).

### The reuse check

- **The geometry exists for the whole body:** `gen_synth_skin.fields()` gives every texel's position, normal and region on the whole atlas (`project_views.head_fields` keeps only the head from it); `make_kits.islands` numbers the UV islands. The probe read nothing else (F-P27-1, F-P27-2).
- **The renderer exists for the head:** `project_views.render` (a NumPy rasteriser of hm08 through a camera, with texture coordinates) takes the head's faces; the body is the same call on the body's faces.
- **The projection and the field exist:** `project_face.py`. The body route reuses its field (displacement held at the island border, relaxed between) and its landmark-triangle warp.
- **The judge exists:** `look.py --judge --candidate --shine neutral`. New: a bare cast and body cameras. **The Unreal driver builds the character's meshes in Python** (`drivers/unreal.py` `character_scene` → `build_character.load_parts()`), so a bare cast is an option there, **no new Unreal runtime** (F-P27-5).
- **New outside packages:** MediaPipe's pose and hand landmarkers beside the face one, through `uv run --with` as Phase25 does; no project dependency.
- **Contracts touched:** none of the article's; `SkinMaps.md` §Sources (*"A fully AI-made map is not accepted"*) only by the lead's re-ruling on a win, as for the head.

### Decisions that bind

**Carried:**
- **The lead, 2026-11-02:** the body is its own phase; asking the model for unclothed bodies in this public CC0 library is approved (*"1) yes"*, to *"(1) its own phase? and is asking the model for unclothed bodies in a public CC0 library OK?"*).
- **RD-P25-15** (one camera, projected) · **F-P25-16's field** (nothing blended) · **the lead at 25.1.8**: not *"cuting pasting, patching, matching, blending"* · **RD-P25-16** (the seams solved with the model on both sides) · **RD-P25-20** (2K, then a 4K test, then 8K) · **RD-P25-7** (generation through the lead's ComfyUI over its API; started by the agent only if not running, stopped by PID) · **RD-P25-8** (a model's picture of a person committed only on a win and the lead's re-ruling).
- **RD-SKM-4** (the genitals and groin plain skin; areolae their natural variation) · **`SkinMaps.md` §Anywhere** (no lighting baked in, no hair) · **RD-SKM-1** (hm08) · **RD-SKM-5, RD-SYN-1** · **RD-SKM-2** · **RD-RO-2** (CC0) · **RD-CMT-4** (the Unreal look view, never Blender) · pre-release, no versioning.

**Decided at Pass 1, unless the lead says otherwise:**
- **RD-P27-1 — Every seam is read from the mesh, not from Annotated Skin.** An edge whose two faces carry different UVs is a seam, and the faces on each side name the islands it joins (F-P27-2). This is exact and is hm08 itself; Annotated Skin is another export whose packing is unverified (F-P25-18), and Phase25's lesson was to measure on the mesh.
- **RD-P27-2 — The genitals and groin are the maker's plain skin in every D** (RD-SKM-4), and the prompt asks for a hairless body. hm08 has no anatomy there; whatever the model draws in the region is replaced by the maker's colour, as Phase25's ear is the maker's. The region's mask is built at 27.1 (§Compact build map).
- **RD-P27-3 — No picture of an unclothed person is committed.** The model's pictures, D's maps and the judge's renders stay under the git-ignored `library/parity/P27_*`; a sheet beside this doc shows only the mesh, the layout or numbers. Why: the repo is public, and RD-P25-8 already holds a person's picture back until a win and a re-ruling.
- **RD-P27-4 — The bare cast is an option beside the default, never a change to it.** `make_thumbnails.py` builds every published thumbnail from the default character, so changing it would stale them all.

**Decided at Pass 2:**
- **RD-P27-5 — The body's source is hm08's render shown four times in one picture (front, profile, back, profile), repainted by Krea; each view is fitted to hm08's before it is projected.** The lead (2026-11-02), on the five-column back sheet (`view_torso_b.png`: C · flat layout · two views · four views as painted · four views detail only): *"Nope... I see 5 of them.... 1 and MAYBE 3 are aligned? all the rest clearly have issues"*; then on the four-view generation (`f4_s50_seed7.png`): *"now there is another with 4 positions ... that one looks really good"*. *(Read as: the four-view picture is the right source; projected unfitted it is misaligned, which F-P27-12 measured. So the fit is the work, not another route.)*
- **Unless the lead says otherwise:** Krea at 0.5, colour as painted (F-P27-13: detail only kept the contours and read blotchy, and the lead found it misaligned too); the head stays Phase25's picture, the body's own head region unused (~1.7 mm a pixel); **27.1 may run beside Phase25's 25.2** (it adds `project_body.py` and touches `look.py` and `build_character.py`, none of 25.2's files); 27.3 waits for 25.2's inverse.

### Risk lane — `build`

Read this pass:
- **The character build** (`tools/parity/scene/build_character.py`, `job.py`'s `CHARACTER_SCENE`, `drivers/unreal.py` `character_scene`): the bare cast is a new option, off by default; `make_thumbnails.py` reads the default (RD-P27-4). No gate under `tools/validators`, `tools/releases` or `tools/conformance` reads the scene (grep, 2026-11-02).
- **The maker:** untouched until the structure step; then the same remake-identical proof as Phase25's 25.2 (the 18 skins and `Tone34` without the new key).
- **`look.py`:** new views and a cast option, off by default; writes only under its output folder.
- **What enumerates the trees this phase adds to:** new tools under `tools/converters/fit/` are read by no gate; the probe folder beside this doc is read by nothing.
- **The pinned runtime refuses the tree's skin article** since Phase26's makeup inputs (`unreal-runtime-v7`; Phase26 §Deferred offered a new runtime at its close). Until one is published, the look view draws the skin article as committed at `3d594fb`, as Phase25's 25.1.15 does (F-P27-6).
- **The lead's ComfyUI and the GPU** are shared with Phase25 and the lead's other work: before a model run `ps -ef | grep "[U]nrealEditor"`, the queue empty; before a look-view launch, no Unreal process for ~3 minutes and ComfyUI's models freed (`POST /free`).
- **The one irreversible risk is publication:** RD-P27-3.

Nothing here is authorization, secrets, a destructive migration or the public edge.

### Step list

- **27.1 — The fitted body on the bare judge.** The unclothed cast and the body views (C alone first: the agent checks the cameras); `project_body.py` with the fit per view; the groin the maker's. **Click 1: is it aligned?**
- **27.2 — The seams, the hands and the feet.** The neck with Phase25's head, the wrists and ankles; the hands' and feet's islands. **Click 2.**
- **27.3 — D as a structure** (on Phase25's 25.2 inverse). Click only if the structure changes the look.
- **27.4 — If D won: the set with D, served.**

### Compact build map

- **27.1:**
  - `tools/parity/scene/build_character.py` `load_parts(bare=False)`: `bare` leaves out the suit and shoes and their deletes (RD-P27-4); `drivers/unreal.py` `character_scene` and `look.py` pass it through as `look.py --bare`.
  - `look.py`: body views beside `JUDGE_VIEWS` (whole body front, back, profile; trunk front and back at ~1 m; neck and shoulder, a wrist, an ankle at 40 cm; the back of the hand), placed from the rig's parts as `judge_views` places the face's.
  - `tools/converters/fit/project_body.py` (new): `render` (the four views of hm08 as one picture, Tone34's colour, `body4.py`'s layout `f4`), `paint` (Krea at 0.5 through `gen_views_model`'s client, the record per picture), `fit` (per view: MediaPipe's pose landmarker (33 points) on the picture and on the render, plus the outline matched contour to contour; one warp per view, the face's landmark-triangle warp), `put` (each texel from the view facing it most squarely and showing the body; holes by pull-push; the groin the maker's; on Tone34's 8K atlas, C elsewhere, for `look.py --candidate`). Writes under git-ignored `library/parity/P27_*`.
  - The groin's mask: the maker's own regions first (`gen_synth_skin`'s `reg` / `body_parts`), else from hm08's joints.
  - Evidence before click 1: hm08's pixels on the model's background per view, before and after the fit; each view looked at for doubled contours; `run_all.py`.
- **27.2:** the neck (Phase25's head island against the body's, the level across the 0.44 m seam measured), the hands (hand landmarks) and the feet (the outline).
- **27.3, 27.4:** as Phase25's 25.2 and 25.3, for the body.
- **Tests:** `run_all.py` per step; one real-path smoke per click, the look view. No new gate.

### Open for the lead

*None blocking.* The decisions above stand unless the lead says otherwise.

---

## Findings (discovery Pass 1, 2026-11-02)

- **F-P27-1 — hm08's atlas has nine islands; the body is one.** Measured at 2048 from the mesh (`Phase27_AiBodySkin_probe/islands.py`): the body (trunk, arms, legs; y −0.73…0.66 m) **57.7 %** of the covered texels; the head **28.6 %**; each foot **2.7 %**; each hand **2.3 %**; the inner mouth 2.5 %; two small islands at the eyes (0.7 % each). The seed's layout claim holds.
- **F-P27-2 — Every seam, from the mesh** (`seams.py`: an edge whose two faces carry different UVs, tallied by the islands it joins, in metres on the body): **the neck** (head ↔ body) **0.44 m**; **each ankle** 0.23 m; **each wrist** 0.13 m; **the body island's own cut 3.40 m**: down the back's midline (~0.8 m with the back of the neck), along the legs (~1.4 m) and arms (~0.3 m), and ~0.4 m on the front of the trunk. Inside the hands 0.79 m, the feet 0.68 m, the head 0.33 m (Phase25's). There is no shoulder seam. **Where one picture is projected across a seam, the seam cannot show** (both sides sample the same pixels); a seam shows only where two sources meet.
- **F-P27-3 — The body island is a person seen from the front, the back split down the spine** ([`layout_facing.jpg`](Phase27_AiBodySkin_probe/layout_facing.jpg): the atlas coloured by which way each texel faces, red front, blue back, green sideways, with 10 cm height bands). The front is one connected region in the island's middle, arms out and legs down; the back is two halves at the island's left and right edges. So **a front camera covers one connected region**, and every route for the back meets the front somewhere inside the island, down the sides, not on an island edge.
- **F-P27-4 — The model's size already matches 2K on the body.** hm08's atlas runs ~1.69 m to a UV unit at the median (0.8–2.6 m across the body, `JOB_FORMAT.md` §The character job), so a 2048 texel is ~0.8 mm (0.4–1.3 mm). A ~2 MP full-body picture (about 1024 × 2048, the body ~1.9 k pixels tall for ~1.67 m) is ~0.9 mm a pixel. The body at 2K needs no detail pass; the face did not either (RD-P25-20).
- **F-P27-5 — The judge has no unclothed body, and needs no new runtime for one.** The rig's character wears a T-shirt, jeans and shoes, and `build_character.py` deletes the body faces they cover (`"delete": True`), so no camera can show the trunk or legs. The look view's four views and the judge's nine are the face, a hand and an ear. The Unreal driver builds the meshes in Python from `build_character.load_parts()`, so a bare cast (garments and their deletes left out) is a host-side option; `make_thumbnails.py` writes its scene from the default cast (RD-P27-4).
- **F-P27-6 — The pinned runtime refuses the tree's skin article** (Phase26's makeup inputs; `unreal-runtime-v7`, `unreal/RUNTIME.json`): Phase25's look views draw the article as committed at `3d594fb` through a scratch driver (25.1.15). This phase does the same until a new runtime is published (Phase26's close offered it; the lead's word).
- **F-P27-7 — What the body's map may show** (`SkinMaps.md` §What the map must and must not show): the genitals and groin plain skin (RD-SKM-4); the areolae their natural variation; no hair, no lighting baked in, no likeness of a real person. The nails are their own part, not the map's. **So the prompt asks for a hairless body, and the groin is the maker's** (RD-P27-2); a model's body hair (underarm, pubic) would otherwise be painted into the skin.
- **F-P27-8 — The consumers:** nothing addressed to this phase. The platform's newest research on this side (`261101_R_PlatformSkinAndMakeupAsks.md`) is about the lips and makeup; the platform clone has one unpushed commit (a snapshot), unrelated (fetched 2026-11-02).

## Findings (discovery Pass 2, 2026-11-02)

*All pictures under the git-ignored `library/parity/P27_Probe/` (RD-P27-3); the scripts beside this doc. Krea 2 Turbo through the lead's ComfyUI (`comfy/krea2turbo_img2img.json`, 8 steps, seed 7), ~15 s a picture. Renders are orthographic, Tone34's colour under a soft key; "on the mesh" is the same renderer with the result as albedo, not the look view.*

- **F-P27-9 — Route A, the body island painted flat, fails as the head's did.** The island cut upright at 1360 × 1536 (C, the surround pushed outward): at **0.6** Krea already draws its own front-view torso over it (breasts and navel where it puts them, arms short, the back halves not drawn as a back, underarm hair); at **0.9** a frontal nude with anatomy, nothing of the layout. On the mesh (`view_q.png`, column `uv60`): smeared, low detail. Out.
- **F-P27-10 — Two views (front and back in one picture, B2) keep the pose but leave the sides grazing.** hm08's render at 1664 × 1536 (1.25 mm a pixel): Krea at **0.5** keeps the pose and the outline (silhouette IoU against hm08's 0.964 front, 0.970 back; 1.7 % and 1.2 % of hm08's pixels on the model's background), at 0.65 0.936 / 0.950, at 0.8 0.912 / 0.925; at every strength it draws a **larger bust than hm08's** and hair on the head despite *"bald"*. Front and back see 97 % of the body island, but **20.1 % of it faces its best camera under 0.3** (34 % under 0.5): the sides of the trunk, arms and legs. On the mesh (`view_side.png`, column `fb50`) the sides show the grey background in patches where the model's body is narrower than hm08's.
- **F-P27-11 — Four views in one picture (B4) fix the build and halve the grazing.** hm08 rendered front, profile, back, profile at 1968 × 1152 (1.67 mm a pixel): Krea at **0.5** draws one person four times **with hm08's small build and a shaved head**, matching across the views. With occlusion, **97.6 % of the body seen, 6.5 % under 0.3** (8.8 % before excluding the model's background; at 0.65, 95.4 % and 5.1 %). On the mesh: no background patches.
- **F-P27-12 — What is left is the outline: doubled contours.** Where the model's body edge in a view sits inside hm08's, its painted edge shading lands on hm08's skin: on the back a second waist and hip contour, and lines down the sides where the profile meets the back (`view_torso_b.png` and `view_side.png`, column `f4_50`). It is the body's version of the face's misfit, and the face's answer applies: fit each view to hm08's render before projecting (landmarks plus the outline), not more strength tuning.
- **F-P27-13 — Detail only removes the level steps but not the contours.** Each view taken as its own detail (the picture over its Gaussian blur, σ 12 px ≈ 2 cm, inside the body) on C's colour: the level steps between views go (gain ~1.03), but the painted edge creases stay as dark lines and the skin reads blotchy (`view_torso_b.png`, column `f4_50d`). As painted keeps the shoulder blades, the spine's shading and the flush that read as a real back. Colour as painted, unless the lead says otherwise (RD-P27-5).
- **Reproduce** (paths from the repo root; `<out>` = `library/parity/P27_Probe`; ComfyUI running on its default port): `MATTER_SKIN_N=2048 uv run --with scipy python -I docs/Planning/Phases/Phase27_AiBodySkin_probe/body.py prep <out>` · `python3 -I …/body.py paint <out> <out>/in_fb.png fb fb 0.5,0.65,0.8 7` · `python3 -I …/body.py paint <out> <out>/in_uv.png uv uv 0.45,0.6,0.75,0.9 7` · `MATTER_SKIN_N=2048 uv run --with scipy python -I …/body.py back <out> <out>/fb_s50_seed7.png fb50 fb` (and `uv`) · `… body4.py prep <out> f4`, then `paint` of `in_f4.png` with key `f4` (`body4` adds it) · `… body4.py back <out> f4 <out>/f4_s50_seed7.png f4_50 [12]` (12 = detail only) · `… body.py view <out> uv60,fb50,f4_50,f4_50d` (the sheets as they stand: each view, one column per map) · `measure.py <out> 50 65 80` · `cover4.py <out>`.

## Deferred

| What | To | What it consumes from this phase |
|---|---|---|
| Other tones, people and ages | *Variety* | the body chain, the prompt, the seam rules |
| Marks on the body from the model | *Skin Layers* | D's body field (if D won) or C's |
| A finer body mesh where folds matter (knuckles, the navel) | OMF, beside Phase25's ear ask (F-P25-27) | the body chain's per-region cameras; a re-meshed body re-runs them |

## Depends on

- **Phase25's chain** (`project_face.py`, `paint_uv.py`, the working shine) and its **25.2** (the maker taking an outside field). Phase25 is IN EXECUTION at 25.2; this phase's execute waits for it.
- **The lead's ComfyUI and models** on the WorkingDrive, **which must be mounted** (attached, not mounted, 2026-11-02).
- **A published runtime that takes the tree's skin article**, or the `3d594fb` workaround (F-P27-6).
- **One GPU, shared** with Phase25's runs and the lead's Unreal work: one heavy job at a time.

## Discovery Log

- **Seeded 2026-11-02** (`9935a6e`) by Phase25's session on the lead's *"Seed phase 27 as the body.."*.
- **Pass 1 — 2026-11-02,** opened by the lead's *"/discovery Phase27"*. Search mode: Bash reads on absolute paths (auto mode; this harness has no Grep/Glob tools).
  - **Examined:** the seed; Phase25 (the Brief, the ledger to 25.1.19, Pass 3's findings F-P25-14 … 18, §Deferred); `CoreMechanisms.md`; `SkinMaps.md` (§Authored on the body, §One subject's set, §What the map must show, §Sources); OVS-7; RD-SKM-4 and RD-MP-3 at their sources; `look.py`'s views; `build_character.py`'s garments; `job.py` and `drivers/unreal.py`'s character scene; `paint_uv.py`'s island cut; `project_views.head_fields` and `gen_synth_skin.fields`; the runtime pin and Phase26's runtime note; the platform's newest research and unpushed commits.
  - **Probed:** the atlas's islands, seams and layout from the mesh, in this session's scratch, the scripts and one picture (the layout, no person) kept beside this doc. Reproduce: `MATTER_SKIN_N=2048 uv run --with scipy python -I docs/Planning/Phases/Phase27_AiBodySkin_probe/islands.py <out>` · `MATTER_SKIN_N=2048 uv run python -I …/layout.py <out>` (after `islands.py`, same `<out>`) · `uv run python -I …/seams.py`.
  - **Not probed:** any generation (the WorkingDrive not mounted; ComfyUI not started); the look view (nothing new to draw yet).
  - **Learnings:** the domains this touches are Unreal (the look view as Phase24 and Phase25 ran it, nothing new) and the image-model facts, which live in Phase25's findings, not yet a domain. Blender, MaterialX, Storm, GitHub: not touched.
  - **Tree:** three commits ahead of origin at kickoff (all the lead's sessions'); Phase25's 25.2 live in a sibling session, its files left alone.
- **Pass 2 — 2026-11-02,** on the lead's *"mounted"* (the WorkingDrive).
  - **Probed:** routes A, B2 and B4, colour as painted and detail only (F-P27-9 … 13). ComfyUI was not running: started by this session and stopped by its PID after (RD-P25-7).
  - **House rule missed once:** a platform session started Studio (`UnrealEditor -game`) at 16:46; the check before the four-view run printed it but did not stop the chain, so two Krea pictures (~30 s) ran beside it. Nothing after that used the GPU.
  - **Not done:** the look view (nothing fitted to show yet); the hands, the feet, the neck.
  - **The lead's verdict and BRIEF READY:** RD-P27-5. Two pictures were opened at once with an unclear question; the lead judged the five-column sheet first (*"You keep opening images and assume I'm just sitting here ready for whatever random question you ask"*). One picture per stop from here (§First human test).
