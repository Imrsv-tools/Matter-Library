# Phase17 — Thumbnails

**Status:** IN EXECUTION (2026-10-14, *"/execute P17"*; Brief ready the same day, discovery Pass 1). Lane **build**. Runs on the library machine (the laptop) for now: the lead, *"We have to rethink and stay local for now"* (RD-MP-14), then *"Make this phase TBD, move the others forward, Thumbnails become Phase 17"* (RD-DS-8). **This phase's ids start at `Q-P17-8`, `F-P17-8` and `RD-P17-1`.** The Library Service minted `Q-P17-1…7` and `F-P17-1…7` while it was Phase17, and those stay its own. *(Numbered Phase18 earlier the same day, RD-DS-7. Seeded by `/research` on the lead's *"Seed all the TBD phases we discovered here"*.)*

## Outcome

**Every kept material has thumbnails that show it at its best,** on a subject that suits it (skin on a hand and a face, hair on a head, glass in front of a backdrop), ready for the website and the team's console.

## Why this is a phase

The rig's pictures are diagnostics: lit the same in every tool so the tools can be compared, with no shadows, no bounce light and no tone curve. That is wrong for showing a material (F-MP-6). A thumbnail is a separate showcase render, with its own scene, lighting and subjects. Nothing like it exists yet (F-P17-8). It is the library's half of *See the Library* (RD-WS-4), and Character Materials (Phase18) pictures each part on the rig this phase builds (RD-DS-7).

---

## The Brief

### First human test

**Where:** the library machine. The agent renders the pictures and opens each contact sheet with `xdg-open`, and the handback always carries the sheet's path (`LOCAL_DELTAS.md`, *the artifact a person reaches*). Click 5 is on the website's staging, which reads the published dev snapshots (SiteFile). The website is the platform's; its address is in the handback, not here.

1. **One material at its best (17.1).** The sheet shows `Oak_Natural` and `StainlessSteel_Polished` (both kept as candidates, read from their files), each as a **card** and a **close-up**. Beside each is the rig's Blender picture of the same article.
   - *Judge: does it look like oak and like polished steel, and better than the rig's flat picture? Do the light, shadow, backdrop and tone suit a showcase?*
   - **What the lead keeps here is the look:** the showcase scene's version 1. Every later picture inherits it.
   - The surface can show it: 1024 px pictures at full size. Oak's grain and wear read at close range. Polished steel is a mirror of the scene's lighting, which is where a wrong HDRI or tone curve would show first.
2. **Every Matter subject (17.2).** One sheet with one kept article per subject (§The subjects): `Loam_Natural` on a slab, a cementitious article on a wall section, `Glass_Clear` in front of a patterned backdrop, `Diamond_Brilliant` cut and side-lit, `Neon_Signage` lit and dark, `Lace_Floral` over a surface, `Canvas_Natural` draped, `GreyCard_Neutral18` as a flat card, and `OakLeaf_Natural` as a leaf card. OakLeaf is a draft: no leaf is kept yet, so it is the only fixture its subject has.
   - *Judge: does each subject suit its material?*
   - **What is judged is the subject, not the article.** The articles are a fixture.
3. **Character, in a human context (17.3).** One sheet on the clothed character:
   - `Skin_FitzpatrickIII` on the hand and half the face;
   - `Eye_Natural` in an eye close-up;
   - `Enamel_Natural`, `Gum_Natural` and `Tongue_Natural` in the open-mouth view;
   - `Lips_FitzpatrickIII` on the mouth with the face on;
   - `Nail_FitzpatrickIII` on the hand;
   - `Hair_Natural` and `Hair_DarkBrown` on the head.
   - *Judge: is each judged where people judge it, and is every picture non-intimate?*
   - These are today's tiling Character materials, which the lead called *"pretty terrible"* on a body. This click judges the **subject**. Whether a Character picture goes public is the review's keep (RD-MP-4).
4. **Every kept material (17.4).** The full sheet: 82 articles, each with its pictures, grouped by subject. The batch's review page now shows each row's thumbnail.
   - *Judge: which ones you would not publish.* Each is noted with what is wrong. It is fixed in the subject or the scene, or recorded as the article's own fault, which goes back into the loop as a redo row.
5. **On the website (17.5).** After the next dev snapshot is published at the lead's word, and the website has taken it: the website's staging, browsing Matter, then Character, then one material page.
   - The cards show thumbnails.
   - Character's rows show their parts in a human context, not the labelled swatch.
   - A material page shows the thumbnail labelled *Cycles*, with the rig's three columns still below it as evidence (F-MP-8).
   - *Judge: the library now shows what it is.* How the site lays it out is the platform's work. What is judged here is that the pictures arrived and are labelled.

**Reconciled click by click:**
- Click 1 needs only 17.1.
- Click 2 needs the subjects (17.2) on 17.1's scene.
- Click 3 needs the character views (17.3).
- Click 4 needs every subject and the record (17.4).
- Click 5 needs the snapshot (17.5). The website taking it is the platform's doing. If it has not taken it yet at the sitting, the published release page on GitHub shows the same files.
- Every tool any click uses is Blender (Cycles) on the library machine, and it has rendered there (the rig's Blender column).
- **The doers:** the agent renders, builds the sheets and the snapshot, and runs `gh`, all done before at Phase13–16. The lead looks, and says the word for the publish.

### In now

| What | Step |
|---|---|
| **A showcase scene, versioned** (`SCENE_VERSION`, starting at 1). Full lighting: one of the library's own HDRIs for fill and reflections, a key light, shadows and bounce light. A seamless backdrop. Khronos PBR Neutral tone and a fixed exposure. Fixed samples and seed. Built by code and headless, as the rig's scenes are. | 17.1 |
| **A thumbnail tool**: one article in, its pictures and its record out, into a git-ignored `library/thumbnails/<identity>/`. A master PNG at 1024 × 1024 per view. | 17.1 |
| **The record** (F-MP-10) beside each article's pictures: the article's hash (its `.mtlx` and every texture it names), the masters' hash (`blender/masters/`), the renderer (Blender version, Cycles, the device), the scene version and the samples. **A picture is stale when any of them differs**, and only stale pictures are re-made. | 17.1 |
| **The contact sheet** the lead judges, with the rig's picture beside each where it has one. | 17.1 |
| **The GPU time per picture, measured** (F-MP-32) and written in 17.1's log, then for the whole library in 17.4's. | 17.1, 17.4 |
| **The Matter subjects per Class** (RD-MP-3, §The subjects). Each article picks its subject from its class or master, and its tile from `meters_per_tile`, as the rig's scenes do. | 17.2 |
| **The pictures per article:** a **card** and a **close-up**, plus a **dark** view for an Emissive article. A Character article gets its part's views instead (§The subjects). | 17.1–17.3 |
| **The Character views, on the clothed character only** (F-MP-17): `face` (half the face), `hand`, `mouth` (open, face hidden), and three new cameras: `lips` (the mouth, face on), `eye` and `head`. **The tool refuses any other view by name.** The whole body, the waist and the feet are never a thumbnail, and the refusal has a unit. | 17.3 |
| **Every kept material made, and kept fresh.** 82 articles: the 52 kept Matter articles and the 30 Character candidates. `IMRSV_MissingMaterial` is the fallback, not a material, and gets none. A re-run makes only what is stale. | 17.4 |
| **Made before the review** (RD-MP-4): `review_pages.py` shows each row's thumbnail beside its rig sheet. | 17.4 |
| **The site file carries them** (SiteFile): `pictures[]` entries with `role: thumbnail`, their `view`, the renderer named, `file` and `sha256`, as WebP. Character materials now publish their human-context pictures, and still never a rig picture. Matter's group `shown` becomes `thumbnail` (§Decisions, RD-P17-4). The rig's pictures stay, as evidence. | 17.5 |
| **The next dev snapshot**, published at the lead's word, and the website told: PlatformDependencies M9 (3), *"a standard preview set"*, and M11 (2), *"a picture subject per row"*. | 17.5 |
| **Docs conformed:** Catalog §Thumbnails, SiteFile (`pictures`, §Groups, §Limits), the four "preview set" wordings RD-MP-5 left owed, `_Architecture.md` §LCD row 9 (F-P17-12), the Glossary's *Thumbnail* (no longer planned), ToolingConventions (`tools/thumbnails/`, `library/thumbnails/`), `.gitignore`, and the batch skill's step, re-read at the close against whatever the Workflow Refiner has landed in it. | at the close |

### Not now

| What | Why not now | What it will consume from this phase |
|---|---|---|
| **An Unreal hero thumbnail** (RD-MP-2) | Waits on a showcase build of the runtime (Lumen or ray tracing on) and the see-through master's repair (M6). Neither runs on the library machine. | The subject table, the record's `renderer` field, and the views as job cameras. |
| **A context view and Creator "looks"** (F-MP-11: the subject in its setting; the same article at a Creator setting) *(planned)* | For most Matter subjects the card already is the subject in its setting. Looks multiply the GPU time and the asset count. | The scene, the tool, and the record; a look adds its settings to the record. |
| **Thumbnails served in the dev install** (a `thumbnail_path` per material in the dev catalog, under `thumbnails/materials/`, the way HDRIs are, M10) *(planned)* | No consumer has asked for it. The website takes the site file. | The folder, the names and the record. The HDRI's `thumbnails/hdris/` is the shape. |
| **Release assets at a real release** (RD-MP-6) | No versionable release yet (pre-release ruling). The *Release Bundle* phase owns it. | The folder and the names. |
| **A completeness gate** refusing a release without thumbnails (F-MP-15) | It sits at the release. A new gate is a lead ruling. | The record. |
| **Per-part meshes, versioned, and map-authored character materials** | *Character Materials, Their Own Library* (Phase18). | **The Character views, the whitelist, the record and the tool's entry point.** It changes which mesh a part is, not how a part is pictured. |
| **The team's console's review queue and stale list** | *The Library Console* (TBD). | `library/thumbnails/<identity>/` and the record, which together are the stale list. |
| **Thumbnails made on upload, on a server** | *The Library Service* (TBD, on hold). | The tool, run as one more stage after the rig. |

### The reuse check

**What the stack already gives:**
- **Cycles in Blender 5.2.2**, which already renders the rig's Blender column on this machine. It has full lighting, and its default view transform is Khronos PBR Neutral, a tone curve made for showing materials (probed: F-P17-13).
- **`blender/masters/load_article.py`**: builds any article on its Blender master. The tool builds nothing of its own for materials.
- **The rig's scene generators** (`tools/parity/scene/build_scene.py`, `build_character.py`): the sphere, the rounded cube, the 2 cm slab, and the clothed MakeHuman character split into one part per substance, with its cameras and its `st` in metres. Subjects and views are taken from them, not remade.
- **The rig's job writer** (`tools/parity/job.py`): it binds the article and rescales `st` by `meters_per_tile`. **The Blender driver's** device choice (`pick_device`) and its character bindings (`cutout_map`, `base_color_map`).
- **The library's 59 HDRIs**, 7 of them overcast skies.
- **The snapshot builder** (`build_snapshot.py`): `pictures[]` already reserves `role: thumbnail` (SiteFile), and `write_webp`, the digests and the asset-limit check all exist.
- **Phase14's stale-or-make pattern** (`hdris.stale`, `serve_to_stage.make_thumbnails`).

**Each custom layer and its gap:**
- **The showcase scene.** The rig's lighting is matched by construction: every mesh is invisible to shadow, diffuse and glossy rays, and the view transform is `Standard` (`blender_render.setup_scene`). That is right for parity and is the whole problem here (F-MP-6). It stays untouched. The showcase sets its own lighting on the same geometry.
- **The record.** An HDRI's thumbnail is stale by file time, because it depends only on its HDRI and its recipe. A material's picture also depends on the masters, the renderer and the scene, which a file time cannot see (F-MP-4). The record is the smallest thing that can.
- **The subjects.** Most new subjects can be simple geometry made in code: the wall section, the pane, the cut stone, the draped cloth, the tube and the leaf card. Three new cameras are added to the character's.

**Contracts touched:** SiteFile (a DRAFT, told through M9). RuntimeCatalog is not touched. Nothing under `blender/addons/` or `tools/conformance/` is changed, so `check_exporter.sh` does not apply.

### Decisions that bind

**From research (the authority):** [`261014_R_MaterialPipeline.md`](../Research/261014_R_MaterialPipeline.md) §Resolved.
- **RD-MP-2:** Cycles renders the hero thumbnail today, and it is labelled with its renderer.
- **RD-MP-3:** F-MP-9's subject-per-Class table is the starting set: skin on the clothed character's hand and part of the face; hair on a head.
- **RD-MP-4:** thumbnails are made before the review.
- **RD-MP-5:** the published pictures are called "thumbnail"; "preview" stays the review render.
- **RD-MP-6:** thumbnails never go in git or LFS.
- **RD-MP-14 and RD-DS-8:** the work runs on the laptop.
- **RD-P13-2:** a Character material is pictured in a human context, never on the cubes.
- **RD-DS-4:** *"teeth need to not be dropped on a box for a thumbnail, they need to mapped to the teeth... same with Skin (showing half face nd hands as outlined in the doc) eyes need to be an eyeball"*.
- **RD-DS-7:** Character's per-part pictures are built on this phase's rig.
- **RD-RO-2:** CC0 only.
- Push and publication are the lead's word.

**Minted here, closed with a recommendation, unless you say otherwise:**
- **RD-P17-1 — This phase builds the Character views, on today's parts.** The seed carried RD-P13-2 in, and RD-DS-7 puts Character after Thumbnails *"because its per-part pictures are built on Thumbnails' rig"*. Phase18's seed line *"takes over the Character subjects from Thumbnails"* is read as taking over **the meshes the subjects sit on**, not the pictures. That line is agent-written, not a ruling. Today's Character materials get pictured, and whether they are published is the review's keep.
- **RD-P17-2 — The look starts as:** the library's `KloofendalOvercast_PureSky` for soft, neutral fill and reflections; one key light for shape and a highlight; shadows and bounce on; a mid-grey seamless backdrop; Khronos PBR Neutral; a fixed exposure. The lead's eye at click 1 decides it. Whatever is kept is scene version 1. *(The seed's open question: which HDRI and which tone curve.)*
- **RD-P17-3 — Sizes and formats:** a master PNG at 1024 × 1024 in the git-ignored folder, and WebP at 1024 in the snapshot. The rig's WebP stays at 512. *(The seed's open question: formats and sizes.)*
- **RD-P17-4 — Matter's group `shown` becomes `thumbnail`.** The site builds its cards from `shown` (SiteFile §Groups). `thumbnail` already means *"its own showcase picture"* for HDRIs, and it now means the same for Matter. Character keeps `human`, and its pictures arrive with `role: thumbnail`. The website is told in M9 and M11.
- **RD-P17-5 — Textiles are draped cloth, not a garment on the character.** The character's views stay on the whitelist, and the eleven textiles stay in Matter's own scene. *(F-MP-9 offered both.)*

### Risk lane — `build`

**The controls, each read:**
- **The gate.** No `run_all.py` lane enumerates `tools/thumbnails/`, `library/thumbnails/` or `library/snapshots/`. Its globs are `MatterLibrary/materials/**/*.mtlx`, `library/releases/*`, the recipes and the fixtures (read 2026-10-14).
- **The snapshot's asset limit** (`MAX_ASSETS = 1000`, `build_snapshot.py`). Thumbnails add about 170 assets to dev.5's 432, about 600 in all (F-P17-11).
- **Publication.** A dev snapshot is a GitHub pre-release on this public repo, made at the lead's word, as dev.1–dev.5 were in build-lane phases.
- **The non-intimate rule** (F-MP-17). It is a content rule enforced as a refusal in the tool, with a unit. It is not an authorization control.

No secrets, no destructive migration, no data loss, and no public edge of ours (the website's edge is the platform's).

**Baseline:** `run_all.py` gives 17 lanes, 14 PASS, 2 SKIP (compression, staging) and 1 FAIL (`approval_binds_freeze`), measured on the library machine on 2026-10-14. The red is the maintainer's promote of the pilot, owed since Phase16 re-froze it (Phase16's close records the same red). It is not this phase's work, and not a regression. **Test surface:** the existing `test_build_snapshot.py`, units for the record's staleness and the view whitelist, and one real-path smoke, click 1's render.

### Step list

| Step | Intent — the first clickable result |
|---|---|
| **17.1 — One material at its best** | The showcase scene v1, the tool, the record and the sheet. Oak and polished steel as a card and a close-up beside their rig pictures; the GPU time measured. **Click 1.** |
| **17.2 — Every Matter subject** | The subject table built: slab, wall, pane, cut stone, lit and dark tube, lace over a surface, draped cloth, flat card, leaf card. One article each. **Click 2.** |
| **17.3 — Character, in a human context** | The character on the showcase lighting, three new cameras, and the whitelist refusal. One article per part. **Click 3.** |
| **17.4 — Every kept material, kept fresh** | All 82 made. A re-run makes only what is stale. The review page shows the thumbnail. **Click 4.** |
| **17.5 — On the website** | The site file carries the thumbnails, the next dev snapshot is published at the lead's word, and M9 and M11 are told. **Click 5.** |

**Reconciled against §In now:** every row names its step, and the docs are *at the close*.

**Split signal, not cut:** Matter (17.1–17.2) and Character (17.3) could each be demonstrated alone. They share the scene, the tool, the record and the publish path, and 17.3 is one camera set and one refusal on top of 17.1. Cutting them apart would build the shared half twice.

### The subjects

The starting set is F-MP-9's table (RD-MP-3), mapped onto the classes and masters on disk (2026-10-14):

| Articles | Subject | Pictures |
|---|---|---|
| metal, plastic, polymer, composite, ceramic, coating, wood, and stone not seen underfoot; TwoLayer; Matter's Subsurface (marble, onyx, silicone) | the sphere and the rounded cube, on the backdrop | card, close |
| ground: soil, sand, and stone seen underfoot (a cleft slate) | a slab at real size, low camera | card, close |
| cementitious | a wall section | card, close |
| TranslucentThin (glass) | a pane in front of a patterned backdrop | card, close |
| TranslucentThick (gem, lead crystal) | a cut stone or a thick block, side-lit, with a backdrop | card, close |
| textile | a draped cloth (RD-P17-5) | card, close |
| Emissive | a tube, lit, and in the dark | card, dark |
| Masked (lace) | over a surface, with a backdrop | card, close |
| vegetation (leaf) | leaf cards | card, close |
| utility (`virtual`: grey card, UV grid) | a flat card | card |
| Character: skin | `hand`, `face` (half) | hand, face |
| Character: eyes (eye, iris, pupil, sclera, cornea) | `eye` | eye |
| Character: teeth, gums, tongue | `mouth` (open, face hidden) | mouth |
| Character: lips | `lips` (the mouth, face on) | lips |
| Character: nails | `hand` | hand |
| Character: hair | `head` | head |

Which stone counts as ground is settled at 17.2, article by article. **The scale tag alone cannot say:** `Granite_Polished` and `Slate_Cleft` are both `s1`, and only one is underfoot.

### Compact build map

- **New:** `tools/thumbnails/` (Apache-2.0). It holds:
  - the scene builder, with `SCENE_VERSION`;
  - the tool, `make_thumbnails.py <article>… [--all-kept] [--sheet]`;
  - a Blender-side script that sets the showcase lighting on the rig's geometry;
  - the record and stale logic;
  - units for the record and the whitelist.
- **New, git-ignored:** `library/thumbnails/<identity>/`, holding `<view>.png` and `record.json`.
- **Reused, not changed in behaviour:**
  - `tools/parity/job.py` (bind and rescale);
  - `scene/build_scene.py`;
  - `scene/build_character.py`, which gains the three cameras: an additive change, so its existing views and their pictures are unchanged;
  - `blender/masters/load_article.py`;
  - `blender_render.pick_device`.
  - **If 17.3's cameras change the character scene's file, the rig's own jobs must still render the same pictures.** Re-run one character job and compare.
- **Changed:**
  - `tools/parity/review_pages.py` (17.4);
  - `tools/releases/build_snapshot.py` (17.5): thumbnail pictures per article, Character pictures allowed when `role: thumbnail`, and the limit unchanged;
  - `.gitignore`.
- **Order:** 17.1 lays the scene and tool. 17.2 and 17.3 add subjects on top. 17.4 is the run. 17.5 is the publish.
- **Seams to watch:**
  - Subsurface on the character at 1024² on an 8 GB card (Blender B8: `RANDOM_WALK_SKIN`);
  - see-through subjects need closed meshes (B4);
  - a headless Blender must start from the factory scene (B10).

### Blockers

None. Every open question in the seed is closed above, unless you say otherwise.

---

## Findings (discovery Pass 1, 2026-10-14)

- **F-P17-8 — Nothing is built.**
  - A tree search for *thumbnail* finds two things.
    - **Phase14's HDRI thumbnails:** 1024 × 512, made from the HDRI itself.
    - **Reservations:** SiteFile's `role: thumbnail` *"once Catalog §Thumbnails exist"*; `build_snapshot.py`'s comment that a Character material's *"pictures wait for a human context (Thumbnails, RD-MP-3)"*; the Glossary's *Thumbnail (planned)*.
  - No prior phase built, deferred or half-built a material thumbnail.
- **F-P17-9 — The rig's Blender lighting cannot be borrowed, only its geometry.** `blender_render.setup_scene` turns off the sun's shadow and makes every mesh invisible to shadow, diffuse and glossy rays, keeping transmission. It uses the `Standard` view transform and a constant dome. Each choice is there so Storm can match it. The showcase needs the opposite of every one, so it sets its own lighting. The rig is left as it is.
- **F-P17-10 — The character has no eye or head view, and its mouth view hides the lips.**
  - The cameras are `wide`, `face`, `hand`, `mouth` (body and lips hidden, because MakeHuman's mouth is closed), `waist` and `feet` (`build_character.py`).
  - So `eye`, `head` and `lips` are new.
  - `wide`, `waist` and `feet` are off the whitelist (F-MP-17).
- **F-P17-11 — The asset count fits.**
  - `matterlib-0.2.0-dev.5` is 432 assets.
  - The thumbnails add 82 × 2, plus 3 dark views, about 167, for about 600 under GitHub's 1000.
  - SiteFile §Limits' *"at most seven per article"* changes with it.
- **F-P17-12 — Two specs say `usdrecord` makes thumbnails.** Both contradict RD-MP-2 (Cycles) and F-MP-6 (the rig's pictures are not thumbnails). Each is conformed in place at the close, not deleted.
  - Catalog §Thumbnails: *"`usdrecord` renders each article against a standardised sphere/dome scene. The same renders double as the per-class parity baselines"*.
  - `_Architecture.md` §LCD row 9: *"`usdrecord` suits the thumbnail pipeline"*.
- **F-P17-13 — The machine, measured.**
  - The library machine (no Unreal engine at the path `unreal/build.sh` takes as `UE`).
  - An RTX 2080 Max-Q with 8 GB.
  - Blender 5.2.2. It accepts the view transforms `Standard`, `AgX`, `Filmic` and `Khronos PBR Neutral` (the factory default), probed headless.
  - The library holds 7 overcast skies among its 59 HDRIs.
- **F-P17-14 — What "kept" is today** (read from the dev.5 site file, which is projected from each article's own file).
  - 95 articles: 23 approved and 30 candidate Matter, 12 draft Matter, and 30 Character candidates.
  - 82 get thumbnails. `IMRSV_MissingMaterial` (master `system`, not selectable) does not.
  - Drafts get theirs when they come to review (RD-MP-4).
- **F-P17-15 — The consumers' side** (swept read-only, 2026-10-14).
  - The website asks for thumbnails at web size with their renderer named, and a picture subject per Character row (M9 (3), M11 (2)).
  - It builds its browsing from the site file's groups (SiteFile §Groups) and shows a labelled swatch where a picture is missing (SiteFile; M11).
  - No other consumer has asked for material thumbnails.

## Execution Log

**Tree at start (2026-10-14):** `main` at `a903b51`, the library machine. Six Refiner-lane files modified by a sibling session (`.ai/`, `.claude/`, `AGENTS.md`, the refinement backlog); not touched. **Gate:** `run_all.py` 15 PASS, 2 SKIP (compression, staging), 0 FAIL. The Brief's red (`approval_binds_freeze`) went green with the maintainer's re-approval (`f113b3a`).

| Step | Commit | Result | Next |
|---|---|---|---|
| **17.1** | the 17.1 commit | `tools/thumbnails/`: the scene (`showcase.py`, `SCENE_VERSION = 1`), the Blender side (`showcase_blender.py`), the probe, the tool and the sheet (`make_thumbnails.py`), and 16 units for the record and staleness (`test_thumbnails.py`). Oak and polished steel made, card and close, at 1024² and 256 samples. A re-run makes nothing. **GPU time (F-MP-32): 12–14 s per picture** on the RTX 2080 Max-Q (OptiX), about 30 s of Blender per article. **▶ SCAFFOLD COMPLETE — sitting owed (click 1).** | the lead's eye on the look |

- **F-P17-16 — A polished mirror vanishes into a plain grey studio.** At the first look (HDRI, key, grey sweep) the steel cube's top face and bevel read as a translucent ghost around the cube. They were mirrors of a back wall the same grey as the wall beside them. The cube was bisected (hidden: gone; backdrop hidden: still there; diffuse: the cube's own outline). Fixed in the scene, not the article: **a rim light** behind and above, narrow (40° spread) and hidden from the camera, gives a mirror something bright to reflect and edges every subject against the backdrop.
- **F-P17-17 — `SCENE_VERSION` alone cannot keep a picture honest.** Tuning the look between renders left the version at 1, so the stale check called the old pictures fresh. **The record now also carries `scene_sha256`**: the look the job carries, the cameras, the subjects and the Blender-side script. `SCENE_VERSION` stays the name the lead keeps; the hash catches a number tuned without a bump (a unit).
- **Handed in by Phase16 (`08f5968`):** `tools/releases/hdris.py` `stale()` dates an HDRI thumbnail against the module's own mtime, so any edit to `hdris.py` re-makes all 59. It is not in this Brief's steps. It is a candidate for 17.4's stale pass, or a quick fix. Recorded, not yet changed.

## Discovery Log

- **2026-10-14 — Pass 1: the Brief.**
  - **Read:**
    - the seed;
    - `261014_R_MaterialPipeline.md`, `261014_R_DownstreamPicture.md` (RD-DS-1, -4, -7, -8, F-DS-13), `261014_R_RoadmapOrder.md`, `261014_R_TheLibrarysSite.md`;
    - the Library Service's Brief (Q-P17-7 → RD-DS-8) and the Character Library and Console seeds;
    - SiteFile, Catalog, RuntimeCatalog, `_Architecture.md` §LCD, the Glossary;
    - PlatformDependencies M9–M11;
    - `tools/parity/JOB_FORMAT.md`, the Blender driver, `build_character.py`, `build_snapshot.py`, `hdris.py`, `serve_to_stage.py`;
    - Learnings Blender B4, B8 and B10 (the rest of the learnings domains are not touched: no Storm, Unreal or MaterialX authoring);
    - the consumers' docs, at origin and read-only, for asks addressed to the library (`LOCAL_DELTAS.md` §Separation); nothing private is copied here.
  - **Measured:** the gate baseline, the GPU, Blender's tone curves, the article counts and the asset count.
  - **No lead question was needed:** every seed question closed against a ruling or with a recommendation (RD-P17-1 to -5).
  - **Phase16 closed (`eb4b70c`) during this pass**, with the same gate red recorded.
