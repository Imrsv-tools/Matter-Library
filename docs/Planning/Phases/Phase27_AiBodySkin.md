# Phase27 — AI Body Skin

**Status:** IN DISCOVERY (Pass 1, 2026-11-02, opened by the lead's *"/discovery Phase27"* at `9935a6e`). The Brief below is **provisional**: the body's route waits on a generation probe (§Open, item 1), and the model drive was not mounted. *Before:* SEEDED (2026-11-02, `9935a6e`), on the lead's *"Seed phase 27 as the body.."*. It runs **after Phase25**, whose chain it reuses; its execute waits for Phase25's 25.2.
**Lane:** `build` (§Risk lane; read against the tree this pass).
**Measured at:** `9935a6e`, on **the machine with Unreal**; Phase25's 25.2 was live in a sibling session (its doc and three `tools/converters/fit/` files uncommitted; none touched here).
**Seeded from:** [`Phase25_AiSkinStructure.md`](Phase25_AiSkinStructure.md): §Pass 3 hand-off (*"what about the rest of the body?"*, ruled 2026-11-02), RD-P25-15 (the face's front projection), F-P25-16 (one coordinate field), RD-P25-16 (the neck waits for the body), F-P25-18 (Annotated Skin), §Deferred (the body islands row). Pass 1's probe: [`Phase27_AiBodySkin_probe/`](Phase27_AiBodySkin_probe/) (the atlas's islands and seams, measured from the mesh; no picture of a person).

## Outcome

**An image model's picture of a real person's body becomes the body's skin in the body's own layout, joined to Phase25's head with no visible seam at the neck, the wrists, the ankles, or down the back and the limbs, and judged beside the maker's body on the same unclothed character. If it wins, the maker turns it into a calibrated skin structure, as Phase25 does for the head.**

*(Confirmed at Pass 1, one change: the seed's "neck, shoulders or arms" named seams that are not where the mesh has them. Measured, hm08's seams are the neck, the wrists, the ankles and the body island's own cut down the spine and along the legs and arms (F-P27-2); there is no shoulder seam.)*

---

## The Brief — provisional (Pass 1)

### What this phase builds, in one paragraph

**The body's skin comes from the model's picture of a person; every seam is decided on the mesh.** hm08's body is one island holding the trunk, arms and legs (58 % of the skin), laid out as a person seen from the front with the back split down the spine to the island's outer edges; the hands and feet are their own islands (F-P27-1, F-P27-3). Phase25's method carries over where a camera can see: a picture matched to hm08's render by landmarks and its silhouette, projected through that one camera, and one coordinate field carrying the rest, nothing blended (RD-P25-15, F-P25-16). **What does not carry over is the back:** no front camera sees it, so the route for the back is this phase's open question (§The routes), measured in Pass 2 before the Brief closes. The judge is the look view with an **unclothed** cast and body cameras, which do not exist yet (F-P27-5). Everything at 2K first (RD-P25-20), which a 2 MP full-body picture already matches on the body (F-P27-4). The genitals and groin stay the maker's plain skin (RD-SKM-4).

### The routes for the trunk, arms and legs (to measure in Pass 2)

| # | Route | State | What decides it |
|---|---|---|---|
| A | **The body island painted in UV space** (Phase25's route 5): the model repaints C's body island as one picture, no camera | Probe | At full strength Krea ignored the head island's layout and drew a front portrait from the words (F-P25-10, F-P25-14); at ≤ 0.6 it kept C (F-P25-7). But the body island already looks like a person seen from the front with arms out (F-P27-3), so the model may keep it. Measured: does the front stay on the front, and what does the model draw on the split back? |
| B | **Front and back of the same person in ONE generation** (a turnaround, side by side), each half projected through hm08's front or back render camera, matched by body landmarks and the silhouette; the two halves meet on the line down each side where both cameras see the skin edge-on, one coordinate field, nothing blended | Probe; then the lead rules on it (§Open, item 2) | One picture, one sampling, one person and one light, so the halves agree by construction; but it is two cameras, and the lead rejected *"many views cut, matched and blended"* for the head (25.1.8) while accepting one camera (RD-P25-15). |
| C | **The front picture only; the back the maker's** | Fallback | A seam down each side where the model's skin meets C's: the defect this phase exists to remove, so only if A and B both fail. |
| D | **The model repaints hm08's own render** (shaded with C) at a middle strength, then it is projected: the body lands on hm08's shape by construction (Phase25's Pass 3 direction 4) | Probe, as B's conditioner | The body has few features to drift (nipples, navel, the knees' and elbows' creases), so a strength that drifts the face may hold the body. |

**The hands** (2.3 % each) take the face's method, one camera each, hand landmarks (MediaPipe's hand landmarker, 21 points) and the silhouette; **the nails are not the map's** (the Nails part wears its own article, `SkinMaps.md` §What the map must show), so only the knuckles and the creases must land. **The feet** (2.7 % each): the same, with the silhouette only (no foot detector is known). Both are Pass 2 questions after the trunk.

### Rides on

| `CoreMechanisms.md` row | What in this phase rides it | The peer we follow |
|---|---|---|
| 1 — a body map larger than 2048 inside the machine's memory | the structure step only (the maker composing the body from the model's field at 8K), after the 2K work | `gen_synth_skin.compose_banded`, as Phase25's 25.2 uses it |
| NEW — the lead rules | **a picture projected onto the mesh through one camera, the rest carried by one coordinate field** | Phase25's chain is not a row yet (Phase25 has not closed): `tools/converters/fit/project_face.py` (`field`, `landmarks`, `ears`) is the peer, followed, not re-written |

Row 2 (makeup on the atlas) is not met.

### First human test (provisional)

**Where:** the machine with Unreal (every compared tool runs there).
- **The surface:** the library's look view (`tools/parity/look.py --judge`), with **an unclothed cast** (the rig's character without the suit and shoes, and without the faces they delete) and **body views**, both new (F-P27-5): the whole body front, back and profile at ~2.5 m; the trunk front and back at ~1 m; the neck and shoulder at 40 cm (the head seam); a wrist and an ankle at 40 cm; the back of the hand. Never Blender (RD-CMT-4). One labelled picture at a time, at native resolution.
- **The columns:** C (`Skin_Tone34_Clean_Base_s001_v01`, the maker's body) · D (the chain's body, with Phase25's D head, so the neck seam shows). C and D wear the working shine (Phase25's `--shine neutral`). **No scanned bar for the body** (OVS-7): judged by eye.
- **What the lead can say after:** *"D's body reads as a real person's skin, better than C, and I cannot find the seams"*, or which seam or region fails.
- **Can the surface show it?** At 2K the body's texel is ~0.8 mm (0.4–1.3 mm across the body, F-P27-4); through the rig's lens (50 mm on a 36 mm aperture) at 1536 wide, a view framing the whole body is ~1–2 mm a pixel (the distance set by the frame's height), the 40 cm seam views ~0.2 mm. The seams and the skin read at 1 m and 40 cm; the full views carry the overall look.
- **The pictures stay local.** An unclothed person drawn by a model is never committed to this public repo (RD-P27-3): they are written under the git-ignored `library/parity/P27_*` and opened for the lead with `xdg-open`, their paths in the handback.

### In now (provisional; steps named once the route is chosen)

- The unclothed judge: the bare cast and the body views (27.1).
- The body chain as a library tool under `tools/converters/fit/`, beside `project_face.py`: the body render through hm08's cameras (a generalisation of `project_views.render`'s head), landmarks, the projection and the field, the route Pass 2 picks.
- The seams: the neck (with Phase25's head), the wrists, the ankles and the body island's own cut, each read from the mesh (RD-P27-1).
- The groin held to the maker's plain skin (RD-P27-2).
- If D wins: the structure (the maker composing the body from D's field, as 25.2 does for the face), the lead's re-ruling, the set served.

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
- **RD-P27-2 — The genitals and groin are the maker's plain skin in every D** (RD-SKM-4), and the prompt asks for a hairless body. hm08 has no anatomy there; whatever the model draws in the region is replaced by the maker's colour, as Phase25's ear is the maker's. The region's mask is a Pass 2 item (the maker's own regions first).
- **RD-P27-3 — No picture of an unclothed person is committed.** The model's pictures, D's maps and the judge's renders stay under the git-ignored `library/parity/P27_*`; a sheet beside this doc shows only the mesh, the layout or numbers. Why: the repo is public, and RD-P25-8 already holds a person's picture back until a win and a re-ruling.
- **RD-P27-4 — The bare cast is an option beside the default, never a change to it.** `make_thumbnails.py` builds every published thumbnail from the default character, so changing it would stale them all.

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

### Step list (provisional)

- **27.1 — The bare judge, and the body's route shown.** The unclothed cast and the body views; C alone first (the agent checks the cameras), then the route Pass 2 chose, as D. **Click 1.**
- **27.2 — The seams, the hands and the feet.** The neck with Phase25's head, the wrists and ankles; the hands' and feet's islands. **Click 2.** *(May merge into 27.1 if the route's first picture already carries them; decided at Pass 2.)*
- **27.3 — D as a structure** (on Phase25's 25.2 inverse). Click only if the structure changes the look.
- **27.4 — If D won: the set with D, served.**

### Open — before the Brief can close

1. **The route (A, B, D), measured.** Needs the model drive: the WorkingDrive is attached but **not mounted** (as Phase25 found all day), so ComfyUI cannot load Krea. Each probe is minutes (one picture ~15 s, one projection, a look at it on the mesh through `project_views`' renderer, no look-view launch).
2. **Whether route B's two halves are admissible** under the 25.1.8 objection: one generation holding the front and the back, each half through its own camera, meeting on one line down each side, nothing blended. Shown to the lead as a picture once probed, not asked in the abstract.
3. **The neck:** one picture covering the body and the head's lower island, or the head's own picture meeting the body's on the seam line; measured once a body picture exists.

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
