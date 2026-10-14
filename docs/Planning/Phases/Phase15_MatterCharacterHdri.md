# Phase15 — Matter, Character and HDRI

**Status:** IN EXECUTION (2026-10-14), lane **build**. Q-P15-1 → **RD-P15-8: option A** (the lead, 2026-10-14: *"A, then /execute Phase15"*). Discovery opened by the lead: *"/discovery P15"*. **Numbered Phase15 by the lead the same day:** *"Lets make these the next phases (Before the scaled grid)"*. A pointer-shell written by `/research` on the lead's word: *"yes record it and seed all three"*. It is the first of the sequence (RD-DS-5, RD-DS-7): this one, then *Every Entry Says What It Is* ([`Phase16_EveryEntrySaysWhatItIs.md`](Phase16_EveryEntrySaysWhatItIs.md)), The Library Service (Phase17), Thumbnails (Phase18), then *Character Materials, Their Own Library* ([`Phase19_CharacterLibrary.md`](Phase19_CharacterLibrary.md)).

> **Ids.** `F-P15-1` to `F-P15-8` belong to *Scale Grids* (now [`Phase20_ScaleGrids.md`](Phase20_ScaleGrids.md)), minted while it held the number Phase15. **This doc's findings start at `F-P15-9`.** Its `Q-P15-n` and `RD-P15-n` series are its own (Scale Grids minted none).

## Outcome

**The website, Studio and USDLiveView each show Matter, Character and HDRI as three separate things to browse, each by its own taxonomy, from what the library publishes.**

**This phase builds the library's half: what it publishes.** Each consumer's browse is its own phase, asked through ledger row **P25**. **Done here when:**
- the library publishes the structure in the dev install and in a dev snapshot;
- the asks are in the ledger;
- the lead has judged clicks 1 to 3 below.

## Why this comes first

The structure is what every consumer builds its browsing on. The lead: *"then we know we have the structure sorted out"*, and, putting the service and pictures ahead too, *"get the entire chain establsihed recategorized, documented and working correctly before we add more materials"* (RD-DS-7).

Today only the website can tell Character from Matter, through a site-file field the library works out from the domain (F-DS-5). The engines' catalog carries nothing, so Studio, USDLiveView and export show the 30 character materials as an ordinary Matter domain.

---

## The Brief

### First human test

**Where:** the library machine. Blender, USDLiveView and `gh` all run there, and Phase14's sittings used all three. **The agent drives everything; the lead uses and judges.**

1. **Blender: the lead's Asset Browser, on the Matter Library** *(step 15.1).*
   - **What the lead sees:** the catalog tree reads **Matter** and **Character**. Matter holds its domains and classes as before, with nothing left under `biological`. **Character › Humanoid** holds **Eyes 5 · Hair 2 · Skin 6 · Nails 7 · Teeth 1 · Mouth 9**.
   - **Judge:** every material is in the row you would look for it in.
2. **USDLiveView, from the dev install: a scene wearing character materials by bare name, under the default sky** *(step 15.1, re-run after 15.2).*
   - **What the lead sees:** it draws as it did before the move. Every moved material still resolves.
   - **Judge:** nothing turns magenta and nothing changes.
   - Installed Materials still lists all 95. Grouping them there is the viewer's own phase (P25).
3. **The dev snapshot `matterlib-0.2.0-dev.4`, on its GitHub pre-release page**, as Phase14's act 4 was *(step 15.2)*. The site file names:
   - the three groups;
   - Character's six rows, in order;
   - each character material's species and part;
   - each HDRI's *when* and *sky*.

   **Judge:** it reads as the structure you ruled.

**Can each surface show what is judged?**
- **Click 1:** Blender's Asset Browser nests catalogs, so it can show Character › Humanoid › Skin. The fixture is the generated library itself. The lead's Blender must point at the regenerated library: execute reads the lead's preferences without saving them, and **B2** and **B12** apply.
- **Click 2:** resolution is binary: it draws, or it is magenta. Execute reads the scene's bindings **from the file** before the sitting, never from the scene's name. If the scene does not bind all 30, it is a grid of the 30 the agent builds.
- **Click 3:** a page of facts. There is no scale or lighting to get wrong.

**Not judged here, named now:**
- **Studio.** It reads the dev install through the platform. Whether it still binds the 30 after the move depends on Q-P15-1 (F-P15-10). Its browse by group is the platform's phase (P25).
- **The website's browse.** The web's phase (P25, M11).

### In now

| What | Step |
|---|---|
| The 30 character articles leave `biological/` for Character's folder (Q-P15-1). **No name changes** (RD-P15-2). | 15.1 |
| Each of the 30 declares `group`, `species` and `part` in its `imrsv_metadata`. Its recipe carries the same three keys (RD-P15-3). | 15.1 |
| The recipe schema and validator know Character's taxonomy. A gate refuses a folder that disagrees with the group the file declares. | 15.1 |
| The working-tree reader takes group, species and part **from the file**, never from the folder or the domain (F-DS-5). | 15.1 |
| Blender's Asset Browser files Matter by `Matter/<domain>/<class>` and Character by `Character/<species>/<part>`. Its verifier follows. | 15.1 |
| The dev catalog carries: `group` on every entry · `species` and `part` on Character entries · `group`, `when`, `sky` and the record's `tagging` (A10) on HDRIs · a top-level `groups[]` (RD-P15-4, RD-P15-5, RD-P15-6). | 15.2 |
| The site file reads `section` from the file's group, not the domain. It adds the same fields and Character's rows (M11 (1)). Publish `0.2.0-dev.4` on the lead's word. | 15.2 |
| **Specs, each in the step that changes its contract:** Taxonomy (Character's section), Identity (Character's folder grammar) and the Glossary (*Character*, *group*) in 15.1 · RuntimeCatalog, SiteFile and Consumers (the search path) in 15.2 · the Catalog tree at the close. | 15.1, 15.2, close |
| **The ledger:** a P25 note (Stage's search path; the 30 ids change, F-P15-11) · M11 (1) answered. | 15.2 |

### Not now

- **Moved to Phase16:** the HDRI facts written into the `.hdr` header (RD-P15-4), plus contributor and licence in any file.
- **Phase19 and Thumbnails (Phase18):** part meshes, a contributor's name in a material's name, and the picture rig per part.
- **Renaming any article** (RD-P15-2).
- **A frozen release carrying the group** (RD-P15-6). The first release after this phase carries it.
- **The consumers' builds** (P25): Stage passing the fields on, Studio's picker, USDLiveView's dialog, the website's group row.
- **HDRIs in Blender's Asset Browser.** Nothing of this phase needs them.
- **The website's asks 3 and 4** (the *"16K"* sentence, `edited_from`). M11 gives both to Phase16.

### Reuse check: what the stack already provides

- **The in-file route.** `imrsv_metadata` already carries `domain`, `class` and `master_material`. The dev catalog has projected `master` out of the file since Phase07 (F-DS-9). Group, species and part ride the same path: no new carrier, no sidecar (RD-DS-3).
- **The group list.** The site file has carried `groups[]` since Phase14 14.3. It is extended, and the catalog takes the same list rather than a second invented shape.
- **A default for an absent key.** The catalog already has one: `creator_selectable` is `true` when absent. `group` follows it (RD-P15-3).
- **Blender's native nested catalogs.** The generator only writes the paths; there is no custom UI.
- **The HDRI taxonomy.** It is Poly Haven's own words, already in every HDRI's record and in the site file's `tagging`. The library names two axes and passes the words through. Merging them into *Day* or *Cloudy* is the website's presentation, by its own ruling.
- **The contracts this touches:**
  - the runtime catalog: additive, `schema_version` unchanged;
  - the site-file draft: additive, schema stays 2;
  - Identity's folder rule: Character's folder grammar;
  - the immutability rule: no released file is edited. Neither lockfile holds a character article, measured below.

### Decisions that bind

**The lead's rulings** (verbatim in [`261014_R_DownstreamPicture.md`](../Research/261014_R_DownstreamPicture.md) §Resolved):
- **RD-DS-1:** three groups, Matter, Character and HDRI. Generic biological materials stay in Matter.
- **RD-DS-2:** licence and name reach the engines like the class. *"use existing solutions"*.
- **RD-DS-3:** the facts go inside the file, with no sidecar.
- **RD-DS-5 and RD-DS-7:** the order of the phases.
- **Q-DS-2, withdrawn.** The group is *"one more field on the catalog entry, like the class"*, and *"All 30 biological materials today are character materials, so each is marked Character."* So every one of the 30 moves.
- **Character's rows: Eyes, Hair, Skin, Nails, Teeth, Mouth.** Ruled in the website's session and recorded there by content.

**Closed in this discovery: the agent's call, standing unless the lead says otherwise.**

- **RD-P15-1** *(agent's call)*. **Character's parts for humanoid are the six rows.** Keys and folders are lower-case: `eyes`, `hair`, `skin`, `nails`, `teeth`, `mouth`. An article's part is set by its Material token (5 · 2 · 6 · 7 · 1 · 9 = 30, measured):

  | Part | Material tokens |
  |---|---|
  | eyes | Cornea, Eye, Iris, Pupil, Sclera |
  | hair | Hair |
  | skin | Skin |
  | nails | Nail |
  | teeth | Enamel |
  | mouth | Lips, Gum, Tongue |

  Which mesh a part fits is a field Phase19 adds; the parts do not have to change for it.
- **RD-P15-2** *(agent's call)*. **No article is renamed.**
  - The name is the identity ([Identity](../../specs/Ontology/Identity.md)), and a saved scene names the bare file. A move that keeps the name keeps every scene resolving wherever the search path covers the new folder.
  - A contributor's name in a material's name is Phase19's to decide.
- **RD-P15-3** *(agent's call)*. **In the file:** `imrsv_metadata` gains `group`, `species` and `part`.
  - **`group` absent means `matter`**, as `creator_selectable` absent means `true`. So no Matter file is edited, and no released file either.
  - A Character article must declare all three keys.
  - A Character article keeps its `domain` and `class` (`biological` / `tissue` and so on) as **what it is made of**. Two reasons: the substance is still true (Taxonomy: *"the matter of living bodies"*), and today's consumers keep browsing these materials exactly as now until they read `group`.
  - **Ruled out:** deriving the group from the domain (F-DS-5).
- **RD-P15-4** *(agent's call)*. **HDRIs in this phase:** `group` and two axes are projected from each HDRI's record, the same source the site file uses today:
  - **`when`:** Poly Haven's time category;
  - **`sky`:** its `weather` attribute.

  **It also takes the platform's ask A10** ([`261013_R_PlatformSkyAsks.md`](../Research/261013_R_PlatformSkyAsks.md)), handed here by Phase16's RD-P16-9: each HDRI entry in the dev catalog carries the record's whole `tagging` block, as the site file already does. The ask says the whole block *"costs little more"*.

  **Writing them into the `.hdr` header moves to Phase16**, for three reasons (F-P15-14):
  - Phase16's own Outcome already puts *"its place in the taxonomy, from inside its own file"*.
  - Phase16's Brief builds the header stamp (its 16.2 and Blocker 2), and its doc already holds the byte-change question (F-DS-10).
  - That makes one header write, not two, and one break of Phase14's *byte-identical default* claim, not two.

  **The hand-over:** Phase16's stamp writes `group`, `when` and `sky` alongside its own lines, under the key spellings this phase lands. RD-DS-3 is fully met at Phase16's close.
- **RD-P15-5** *(agent's call)*. **The catalog stays at `schema_version` 2/3.** The change is additive, and Stage reads each field with a default, ignoring keys it does not know (measured, F-P15-10). The top-level `groups[]` is the site file's list, with:
  - each group's `taxonomy`, the axes it is browsed by: Matter `domain`, `material_class` · Character `species`, `part` · HDRIs `when`, `sky`;
  - Character's `rows`, its parts' labels and order.

  An HDRI entry's `group` is `hdris`, the id the site file already uses.
- **RD-P15-6** *(agent's call)*. **Only the dev catalog and the site file carry these fields.** The release projector is unchanged, because the frozen pilot must re-project byte-identically (the `catalog_freshness` lane). A frozen release gains them with the first release after this phase. This is how `master` was handled.
- **RD-P15-7** *(agent's call)*. **The site file stays at schema 2.** The change is additive. The website's mirror checks the version number, so a bump would make it refuse `dev.4` the way it refuses `dev.3` today.

### Q-P15-1 — where Character's folder sits → RD-P15-8

> **RD-P15-8 — A: `materials/character/humanoid/<part>/`** (the lead, 2026-10-14, verbatim: *"A, then /execute Phase15"*). The Stage ask (walk every folder under `materials/`) goes into P25 at 15.2. Until Stage lands it, Studio cannot bind the 30 by bare name from the dev install.

**Measured 2026-10-14 (F-P15-10, F-P15-12):**
- **Stage** takes as search roots **exactly the folders two levels below `materials/`**.
- **USDLiveView's launcher** takes every folder holding a `.mtlx`, at any depth.
- **The library's gates** walk every `.mtlx` under `materials/`.
- **Texture references** are relative to the article's folder and are written from the recipes.

**The options:**

| | Folder | What it gives | What it costs |
|---|---|---|---|
| **A (recommended)** | `materials/character/humanoid/<part>/` | Species and part are in the path, as the seed has it. Every library gate keeps covering the 30 unchanged. Stage needs one change, making it match USDLiveView and the library's own rule (*"every folder under `materials/` that holds a `.mtlx`"*); after that, any future depth is free. | Texture references gain one `../` (a scripted substitution in 30 recipes, then re-assembled). **Studio cannot bind the 30 by bare name from the dev install until Stage walks every depth.** That ask is added to P25. |
| **B** | `materials/character/<part>/`, with species only in the file | **Nothing breaks anywhere.** The depth is unchanged, so Stage, textures and ids keep their shape. | The folder does not show species. A second species (canine) moves the humanoid materials down a level then, with the same Stage ask. |
| **C** | leave them in `biological/` | Group, species and part travel in the file and the catalog only. | Character has no folder of its own until Phase19, after Thumbnails. Meanwhile Taxonomy's *"folder = taxonomy"* holds for Matter only. |

**Not offered:** a root of its own beside `hdris/`, `MatterLibrary/characters/`.
- Every library tool and gate that walks `materials/` would need a second root, and one that missed it would silently stop checking the 30.
- It breaks Stage and the platform's deploy as A does, and more.

**Why A:** the lead put structure first so that consumers build once against the final shape (*"recategorized"*, RD-DS-7). Stage's two-level walk is the one consumer built to the old shape. Asking it once now is cheaper than moving the files twice.

**Pick B if a Studio gap is not acceptable:** with B, Studio cannot bind the 30 only until the platform lands that ask, never because of this phase.

### Risk lane: `build`

The controls, each read:
- **Frozen and approved records.** Neither `matterlib-0.0.1.lock.yaml` nor `matterlib-0.1.0.lock.yaml` names a biological article (0 matches). So the move and the edits inside the 30 files touch no frozen record, and no Matter file is edited (RD-P15-3).
- **The gates that enumerate the tree.** The `materials`, `determinism` and `recipe` lanes of `run_all.py` walk `materials/**`, so they still cover the 30 under A or B.
  - The release projector and the `catalog_freshness` lane are not touched (RD-P15-6).
  - `no_projection_guard` bans only the tokens `provenance`, `evidence` and `license`.
- **`tools/conformance/`.** `verify_asset_library.py` asserts each catalog path is `domain/class`, and 15.1 edits it. So **`check_exporter.sh` is baselined before that edit** (LOCAL_DELTAS).
- **The public edge.** `dev.4` is a GitHub pre-release, as `dev.1` to `dev.3` were in build-lane phases. Publishing it and the push are the lead's word.
- **The baseline, measured 2026-10-14 on the library machine:** `run_all.py` gives 17 lanes, 15 PASS, 2 SKIP (`compression`, `staging`), 0 FAIL.

### Steps

- **15.1 — Character has its own place, and Blender shows it.**
  - Move the 30 to the folder Q-P15-1 picks.
  - Declare group, species and part in each file and recipe.
  - Teach the recipe schema, the validator, the working-tree reader, and the asset-library generator and its verifier.
  - Regenerate the Blender library and re-serve the dev install.
  - Write Taxonomy, Identity and the Glossary.
  - **First clickable:** clicks 1 and 2.
- **15.2 — The engines' data and the site's say it.**
  - Add the dev catalog's fields and `groups[]`.
  - The site file reads the file's group, and gains the rows and the HDRI axes.
  - Write RuntimeCatalog, SiteFile and Consumers; add the ledger notes.
  - Publish `dev.4` on the lead's word.
  - **First clickable:** click 3, and click 2 re-run on the new catalog.
- **15.3 — Web and the platform are told what to change** *(added at execute, the lead, 2026-10-14, verbatim: "We will also need this pahse to message Web and/or platfrom what adjustments those need to make (if any)")*.
  - What each must change, written into the ledger rows they read (P25, M11) and sent as a message to each live session of theirs.
  - **The Stage ask goes out as soon as 15.1 lands**, because the move is what breaks Studio's binding of the 30 (RD-P15-8). The rest goes out after 15.2, once the fields are published.
- **At the close:** conform the Catalog tree.

**Reconciled click by click:**
- Click 1 needs only 15.1 (the regenerated library).
- Click 2 needs only 15.1: the dev install's serve tool already exists.
- Click 3 needs 15.2.
- Every row of §In now names its step.

**The doers:**
- **Publishing `dev.4`:** the agent, with `gh`. Its access is real: it published `dev.1` to `dev.3`.
- **The lead's Blender preferences:** read by the agent and never saved.

### Compact build map

- **The move.** `git mv` the 30 `.mtlx` files. Edit each recipe's `path`. Under A, change the texture references `../../../textures/` to `../../../../textures/`:
  - a scripted, anchored substitution over the 30 recipes, aborting on any other count;
  - then re-assemble with `tools/converters/assemble_mtlx.py`, which also writes the three keys into `imrsv_metadata`.
- **The files to change:**

  | File | Change |
  |---|---|
  | `tools/converters/recipe.schema.json` | `group`, `species`, `part` |
  | `tools/validators/validate_recipe.py` | its domain → class map, plus Character's species → part map |
  | `tools/converters/working_tree.py` | `articles()` today splits domain and class from the path; it reads the file instead |
  | `tools/releases/serve_to_stage.py` | the catalog fields and `groups[]` |
  | `tools/releases/build_snapshot.py` | `section()` and `CHARACTER_DOMAINS` give way to the file's group; `GROUPS` gains `taxonomy` and `rows`; the HDRI axes. Plus `test_build_snapshot.py` |
  | `tools/releases/hdris.py` | the reader for `when` and `sky` from the record |
  | `tools/generators/gen_asset_library.py` | the catalog paths |
  | `tools/conformance/verify_asset_library.py` | the catalog paths |

  `tools/parity/job.py` finds an article by its stem at any depth, so it is unaffected.
- **Tests:** extend the existing units (`test_build_snapshot.py`, `tools/validators/test_hdri.py`). **At most one real-path smoke:** click 2's served dev install, opened in USDLiveView. No new gate lane: the folder-against-group check lives inside the existing `recipe` or `materials` validator.
- **Learnings in play:** **B2** (an Asset Library added as *Pack* is read-only) · **B12** (the library `.blend` is compressed, so read it with Blender and not `grep`) · **G1** (an interrupted `gh release create` leaves a draft). Nothing in MaterialX, Storm or Unreal applies: no shading changes.

---

## Discovery Log

### Pass 1 — product docs, research, consumers, tree (2026-10-14)

**Read:**
- the specs top-down: `_Architecture`, Taxonomy, Identity, RuntimeCatalog, SiteFile, ReleaseModel;
- the research behind this phase: `261014_R_DownstreamPicture.md`, every pass;
- Phase16 and Phase19;
- `PlatformDependencies.md`: P25, P26, M9, M11 and M12;
- the learnings for Blender, GitHub and MaterialX;
- the tools that read the materials tree.

**The consumers, fetched and read read-only at their `origin/main`** (their private detail is not copied here): the platform's docs and Stage, the website's repo, USDLiveView (its `HEAD`, 5 local commits ahead) and the Asset Library.

**F-P15-9 — The seed's four questions, answered:**

| Seed question | Answer |
|---|---|
| Folder and name | Q-P15-1 and RD-P15-2 |
| Which articles move | All 30, by the lead's word (Q-DS-2 withdrawn) |
| Key names and the schema step | RD-P15-3, RD-P15-5, RD-P15-7 |
| What an earlier consumer does with moved files | F-P15-10 |

The seed's *"install layout in ReleaseModel"* item already landed in the quick fix `d27c2a9`.

**F-P15-10 — How each consumer meets a move** (measured 2026-10-14):

| Consumer | What it does | What a move does to it |
|---|---|---|
| **USDLiveView** | puts every folder holding a `.mtlx`, at any depth, on its search path | survives any layout |
| **Stage** | takes exactly the folders two levels below `materials/` as its search roots | **A breaks Studio's bare-name binding of the 30. B and C break nothing.** |
| | reads each catalog field with a default | ignores new keys; absent keys read as empty |
| **The website** | gives a material its address from its **name**, not its folder | its lasting URLs survive any move |
| **Stage's test fixtures** | hold their own frozen copy of the skins under `biological/` | untouched |

**F-P15-11 — A move changes the 30 catalog ids.**
- The `id` embeds the folder (`<domain>/<class>/<Name>`). Under A, `biological/tissue/Skin_FitzpatrickIV_Clean_Base_s001` becomes `character/humanoid/skin/Skin_FitzpatrickIV_Clean_Base_s001`.
- Anything a consumer stored by `id` rather than by name would break. The P25 note asks each consumer to say whether it stores ids.
- Bare names, which is what scenes store, are unchanged.

**F-P15-12 — Texture references depend on the folder's depth.**
- They are written verbatim from each recipe (`../../../textures/…`); the assembler does not compute them.
- A folder one level deeper means one more `../` in all 30 recipes.

**F-P15-13 — Nothing newer from the consumers changes the frame.**
- The website's *Beside Matter* Pass 4 and USDLiveView's *Library Concepts* seed are already recorded here (M11, M12, P25).
- **Newer, from this repo:** RD-DS-7, which renumbers Character to Phase19; it landed during this pass.
- The website browses HDRIs by Poly Haven's own words, merged into *Day / Sunrise & sunset / Night* and *Clear / Cloudy*. Its measurement: `categories` splits all 59 one each, and `weather` is single-valued. **Re-measure at 15.2.**

**F-P15-14 — Phase16 already owns the header.**
- Its Outcome reads *"… its place in the taxonomy, from inside its own file"*.
- Its doc already holds the `.hdr` byte-change question.
- Its Brief, committed during this pass (`191eaa8`), builds the stamp in `tools/releases/hdris.py` at its step 16.2. It shares five places with this phase: the `imrsv_metadata` block, the `.hdr` header, the catalog entry and its `schema_version`, the site file and its schema, and `build_snapshot.py`.
- **The split:** Phase16 claims only `contributor`, `licence` and the HDRI `credit`. It claims no schema number until this phase lands, and it hands A10 here (RD-P16-9).
- **One gap, closed here:** Phase16's split table gives *the taxonomy in the `.hdr` header* to this phase, while RD-P15-4 gives the header write to Phase16. RD-P15-4 resolves it: Phase16's stamp carries the taxonomy lines, and Phase16's session is told.
- Hence RD-P15-4.

**F-P15-15 — The library's own Blender Asset Browser is the outlier among the peer surfaces.**
- It files the 30 under `biological/tissue`, `keratin` and `bone`, because its catalog path is `domain/class`.
- The website already shows Character apart, and the other consumers are asked to (P25). So Blender is in scope (15.1). It is also the one surface where the library can show the whole structure itself.

**Learnings:**
- Blender **B2** and **B12** and GitHub **G1** apply.
- MaterialX has none that applies.
- Storm and Unreal are not touched.

---

## Execution Log

| Step | Landed | Result | Next |
|---|---|---|---|
| **15.1** ▶ **SCAFFOLD COMPLETE — sitting owed** (clicks 1, 2) | the 15.1 commit | **The 30 are in `materials/character/humanoid/<part>/`** (eyes 5 · hair 2 · skin 6 · nails 7 · teeth 1 · mouth 9), names unchanged. Each declares `group`, `species` and `part` in its `imrsv_metadata` and recipe. Re-assembly changed exactly 90 metadata lines and the skins' 24 texture paths (`../../../` → `../../../../`). **`tools/converters/groups.py`** holds the groups and Character's taxonomy. The recipe gate refuses a folder that disagrees with the file (G3/G5; probed failing three ways). The working-tree reader takes group and taxonomy from the file. Blender's library is regenerated under `Matter/<Domain>/<Class>` and `Character/Humanoid/<Part>`: 94 articles conform. The lead's Blender reads it from the repo, as Append. The dev catalog carries `group`, plus `species` and `part`, read from the file (served, 95 articles). The wish list's 30 slots are moved. **Gates:** `run_all.py` gives 15 PASS, 2 SKIP, 0 FAIL, the baseline set, and its materials, determinism and recipe lanes walked the moved files. `check_exporter.sh` passed before the edit; the re-run is recorded in the commit message. **Click 2, looked at first:** a headless Storm render of `Character30.imrsv` (30 spheres bound by bare name, with USDLiveView's search-path rule) resolves all 30, with no magenta. Its only warnings are the eye and hair fit maps, which are supplied at binding, as before. | sitting: clicks 1, 2 |
