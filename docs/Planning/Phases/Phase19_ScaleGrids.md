# Phase19 — Scale Grids

**Status:** IN EXECUTION (2026-10-15, the lead: *"/execute P19"*, after Phase18 closed; it runs ahead of *Skin Maps*, which RD-P18-10 had put next). Brief ready and **re-verified 2026-10-15** by discovery Pass 2, which the lead opened: *"/discovery P19"*. Lane **build**. Pass 1 (2026-10-14) was written when this phase was Phase15, before Phase15 – 18 ran. Pass 2 re-measured it against them, and the Brief below is the result (F-P19-1 to F-P19-8). In the same session the lead ruled that a higher resolution is an option of one material (RD-P19-1), and that a size fits the scale options exactly (RD-P19-2, D-9).
- **Ids:** `F-P15-1` to `F-P15-8` were minted while this phase was Phase15 and are kept (Phase15's own start at `F-P15-9`). Pass 2 mints `F-P19-n`.
- **Steps are `19.n` since Pass 2.** They were `15.n`, which Phase15's own commits now use.
- *Numbering:* Phase15 by the lead's *"/discovery P15"*, then Phase18, Phase20 and Phase19, all on 2026-10-14 (RD-DS-6 to RD-DS-8; the lead's words are in the Roadmap's §Future note).
- *Seeded* 2026-10-14 by `/research` on the lead's word: *"a Material for every UV scale that "aligns" with eachtoehr … we can use for testing when apllying UVs to ensure they are to scale … can be it's own phase"*.

> **Re-verified 2026-10-15 (Pass 2).** Pass 1's retro feared that *Character Materials* (now Phase18) would take skin, eyes and teeth off a tile size, and so break clicks 2 and 4. **It does not take the skin off its tile.** A fitted article is `sUKN` only when it tiles nothing (RD-P18-8). *Skin Maps*, ruled to run straight after Phase18 (RD-P18-10), keeps the skin's tiling micro layer. So clicks 2 and 4 hold whichever of the two phases runs first (F-P19-1). Three things in the tree did change the Brief:
> - D-5's stamp moves out of `blender/masters/`, whose hash every thumbnail keys on (F-P19-2);
> - the kept grids owe thumbnails (F-P19-4);
> - *Matter* now names a group, so the scale view is said to cover every library material, Matter and Character (F-P19-7).

## Outcome

**Anyone applying UVs can swap every object in a scene to the scale grid of its own material and see at once whether a metre is a metre: a wrong scale is obvious.**

*Why it is a phase:* today a material's size is checked in one place, the rig's ruler check: a number, for one article, in one test scene. Errors happen in UVs and bindings on real meshes, and nothing shows them by eye: UVs in the wrong unit, a binding that forgot its UV scale, an object imported at the wrong size, an article with no recorded size. The skin detail once drawn about 170 times too large on a character's own atlas was one of these ([LCDSchema](../../specs/Contract/LCDSchema.md) §Creator-adjustable subset).

---

## The Brief

### First human test

**Where:** the library machine, in the lead's own Blender 5.2 (Material Preview), plus two pictures the agent opens for him. Every scene is built headless from the factory scene into its own file, rendered and looked at by the agent first, then opened detached (Learnings Blender B10, B11). The lead judges by eye; every machine-checkable click is the agent's.

1. **(19.1) The grids, scaling down** *(as it passed, 2026-10-15: six squares side by side, each exactly its grid's tile, 100 m to 1 mm, one view per step; the form first written here, below, was superseded at the sitting)*. ~~A scene with the 1 m reference cube in the 1 m grid and one object per grid, each at its grid's own size, plus the `sUKN` hatch.~~ The lead judges: the same length is the same colour in every grid; the four line levels read up close; **from across the room each grid still reads as its own background colour** (F-P15-8); the hatch reads *"size unknown"*. He then finds the seven grids in his Asset Browser under *utility / virtual* and drags one onto an object.
2. **(19.2) Scale view on.** A *scale test* scene of objects at real size, each wearing a library material (Matter or Character), with errors planted in it. One action turns on scale view: every object wearing a library material wears the grid nearest that material's size. **The lead names the wrong objects before reading the fixture's record.** Two off-tag articles read *right* in size (Oak at 0.8 m, Concrete_Polished at 3 m), and the view lists them as off their scale option (RD-P19-2). The fitted teeth set (`Teeth_Natural`, `sUKN`) reads the hatch, which is also right: it tiles nothing (RD-P18-8).
3. **(19.2) Scale view off.** Every object wears its own material again, exactly as before.
4. **(19.3) The character in the rig.** The rig's sheet of the MakeHuman body in scale view, in Storm and Blender: each part in its grid. The lead judges that both tools draw the same grid at the same size, and sees where the skin's size varies across the body (F-P15-2). A part on its own mesh's atlas draws one grid tile per atlas unit, which is the truth about a tiled article on an atlas. A part wearing a fitted `sUKN` article draws the hatch (F-P19-5). The cast is the rig's own (`rig.py` `cast_for`), read at execute, since Phase18 may change it.
5. **(19.4) The golden cube.** The conformance gate's own Storm render: the 1 m cube in the 1 m grid beside the Copper table.

**Each click's surface can show what it judges:**
- Clicks 1–3 compare one tool, Blender, which renders here (5.2.2).
- Click 1's camera puts about 1,000 px across the cube's face, so the 10 cm and 1 cm lines resolve. ~~A second, far view tests the background tint.~~ *(Superseded by RD-P19-3: the background is neutral.)*
- Click 2's errors are **read from the fixture's own record** (a JSON written beside the `.blend` by the builder), never inferred from object names. The planted errors are:
  - Copper on Blender's default 0–1 UVs (its grid 10× too large beside the cube);
  - MakeHuman's skin on the raw body atlas (the 170× case: the 1 cm grid drawn at about 1.7 m);
  - one object brought in at the wrong size.
- Click 4: Storm and Blender run here. The Unreal column comes from the machine with Unreal when it next runs the rig. The click does not need it.
- Click 5: the gate's `usdrecord` render runs here; the gate was green on 2026-10-15.
- No click needs anything under *Not now*.

### In now
- **The scale grids** (19.1):
  - a generator and seven grids (`s0001` to `s100`, plus `sUKN`), as library content in `utility/virtual/`, each with its words (label, summary, search words);
  - each grid through the rig in Storm and Blender;
  - the Blender library regenerated, so they appear in the Asset Browser;
  - a thumbnail for each grid. They are `candidate`, so they are kept, and every kept article is pictured (Phase17). Each is drawn on the `card` subject at true size, as every article is (F-P19-4);
  - the Glossary's *Scale grid* loses *(planned)*, and the grids join the [Catalog](../../specs/Catalog/Catalog.md) and [MasterSet](../../specs/Ontology/MasterSet.md) tables.
- **Scale view in Blender** (19.2): turns on and off in the lead's Blender; the swap rule is written once in a spec.
- **Scale view in the rig** (19.3), on the character.
- **The golden's 1 m cube wears the 1 m grid** (19.4), with `build_portable.py` carrying more than one article.
- **The scale options held firm** (RD-P19-2, D-9):
  - the rule in Identity, the `recipe` lane's check, the generation tools' wording and the 15 redo rows (19.1);
  - the scale view's list of off-option articles (19.2).

### Not now
- **A scale view in Studio, USDLiveView or any other consumer.** It is the consumer's to build from the shipped grids and the written swap rule. At the close, offer it as a ledger row in `PlatformDependencies.md`, naming what it consumes: the seven article names, the swap rule's spec section, and `meters_per_tile` in `imrsv_metadata`.
- **Installing the Matter add-on permanently in the lead's Blender.** The sitting registers it for the session (D-6); a permanent install is offered at the close, and *Blender from a Release* owns installing.
- **One procedural grid instead of seven textures** (SP-Q2, answered by RD-SP-1). Also out: world-aligned grids.
- **Articles at `s0001`, `s10` or `s100`.** None exist yet (F-P15-1); those three grids stand ready for them.
- **Any change to the UV grid.** It is kept beside the new grids (SP-F3).
- **Any change to what a scale tag means.**
- **Any release.** Pre-release, no ceremony. The next dev snapshot carries the grids on its own (F-P15-6).
- **Re-making the 15 off-option articles.** They become redo rows for the material-making process (D-9).
- **How a resolution option ships** (RD-P19-1). That is *Version Management*'s.
- **The Unreal column on the library machine.**

### Reuse check — what the stack already gives, and the gap that justifies each new piece

| New piece | What it reuses | Native alternative, and why it is not enough |
|---|---|---|
| `gen_scalegrid.py` | the `gen_uvgrid.py` pattern: PIL, deterministic, no network, LFS under `textures/**` | Blender's *UV Grid* / *Color Grid* images, Unreal's world-grid default material (U7): neither measures in metres or encodes length as colour, and neither ships to every consumer |
| seven articles | recipe → `assemble_mtlx.py` → the gate's lanes, exactly as the UV grid | — |
| Asset Browser entries | `gen_asset_library.py` builds every Creator-selectable article in the working tree; the lead's library is already registered, set to Append | nothing new |
| the grids' thumbnails | `make_thumbnails.py` and the `card` subject (`showcase.subject_for`: class `virtual`), at true size | nothing new |
| Blender scale view | `load_article` / `ML_Place2D`'s `uv_scale` input, the `ml_article` property, the existing add-on package | Blender has no "swap every material for its scale reference" action |
| rig scale view | the character job already divides each part's `st` by the bound article's `meters_per_tile` (F-P15-2) | — |
| the cube in the golden | `build_portable.py`, taught a list of articles instead of one | — |

**Standards touched:**
- [Identity](../../specs/Ontology/Identity.md): six tokens, ≤63 characters.
- [Taxonomy](../../specs/Ontology/Taxonomy.md): `utility/virtual`.
- MaterialX 1.39 / OpenPBR through the assembler.
- The LCD `place2d` semantics: `uv_scale` **divides**.
- [CreatorAssetProfile](../../specs/Contract/CreatorAssetProfile.md), for the golden (19.4).
- The Blender 5.1+ API.

### Decisions that bind

**The lead's, from research** ([`261014_R_ScaleProbes.md`](../Research/261014_R_ScaleProbes.md) §Resolved, quoted there in full):
- **RD-SP-1** — *"a Material for every UV scale that "aligns" with eachtoehr … can be it's own phase"*: one grid per scale tag, `s0001` to `s100`, plus the `sUKN` hatch.
- **RD-SP-2** — *"Yes ship in releases... very useful in all locations when trouble shooting"*: library content.
- **RD-SP-3** — *"exact name execpt scale"*: `Diagnostic_ScaleGrid_Clean_Base_<sNN>_v01`. It is 38–41 characters and has six tokens, so it passes [Identity](../../specs/Ontology/Identity.md) as written. The `sUKN` grid is `Diagnostic_ScaleGrid_Clean_Base_sUKN_v01`.
- **RD-SP-4** — *"consistant scale colors in the grid … if each scale had that is its base then someting like 4 thicknessed of grid … like Blue is 1 meter in all of them (for example)"*:
  - a line's colour is its length, in every grid;
  - ~~a grid's background is a dark shade of its own tile length's colour;~~ *(this was the agent's reading of "if each scale had that is its base"; superseded by RD-P19-3: the background is neutral, only the lines carry colour)*
  - four line levels: the tile's edge, then each tenth below it, three times.

**The lead's, at Pass 2** (2026-10-15, in this session; the lead's words, then the reading):
- **RD-P19-1** — asked whether a higher-resolution copy of the same texture (8k beside 2k) is a new material: *"New resoution option of one material."*
  - *Reading:* a resolution is an option of one article. It never changes the article's size (`meters_per_tile`) or its identity.
  - How an option ships is not ruled here. That is *Version Management*'s, and this ruling is carried there at the close.
- **RD-P19-2** — *"We will want to be as firm as we can be that scale fits exactly into our scale options. I think we are providing an excellent structrue of metric scale - we should STRONGLY avoid fractions of that... worth noting for any of our generation toolsets."*
  - *Reading:* an article's `meters_per_tile` is exactly its tag's length (1 mm, 1 cm, 10 cm, 1 m, 10 m or 100 m), and the generation tools hold to it (D-9).

**The lead's, at execute** (2026-10-15, click 1):
- **RD-P19-3** — *"NO! NO NO... you are not understnding the assignment... Gridliines have colors... that is all... I look at an object and see grid lines that match or don't mathc... coloring things does NOT help... we are not making a pantone series... wer are making a check grid validataion and I keep seeing colored squares... This set could be helpful to ID why KIND of scale is added to an object.. .that is NOT the mission.. we are trying to verify that the mareails UV is MATCHING SCALE"*. Asked just before it: *"are you putting a background color or something on this materials?"*
  - *Reading:* only the lines carry colour (a line's colour is its length, RD-SP-4). The background is neutral, the same in every grid. A grid is a check grid: it tells whether an object's UV matches its scale, never which scale it is.
  - **This supersedes** this doc's reading of RD-SP-4's *"if each scale had that is its base"* as a background in the tile's colour: D-2's *"they are also the backgrounds"*, D-3's *"blends into the grid's own colour"*, and the far-colour tuning recorded at 19.1. A finer level too small to resolve should fade into the neutral background, not tint it.

**Closed at this discovery** (each the agent's call, recorded so the executor need not re-derive it; the lead may overrule any):
- **D-1 — Where and how:**
  - **Place:** `MatterLibrary/materials/utility/virtual/` and `textures/base/utility/virtual/ScaleGrid_basecolor_<sNN>.png`, beside the UV grid (its peer).
  - **Master:** `Opaque`, as the UV grid's. A grid on an unlit master would be a new kind of diagnostic with no peer.
  - **Size:** `meters_per_tile` equals the tag exactly. The `sUKN` grid has no metric size. It authors `0.0`, as every `sUKN` article does (the missing material and Phase18's fitted teeth and eye). The rig and the thumbnail tool draw a `0.0` as one tile per metre (`job.py` reads it as `1.0`, F-P19-3).
  - **Texture:** 4,096 px square. Flat colours compress to almost nothing.
- **D-2 — The palette:**
  - It covers **nine lengths**, 1 µm to 100 m, the finest line of the `s0001` grid to the `s100` tile.
  - Blue is 1 m, the lead's example.
  - The six tile lengths take the most distinct hues. ~~since they are also the backgrounds~~ *(RD-P19-3)*
  - Weight and brightness step with the level too, so a colour-blind eye still reads which level a line is.
  - The executor proposes it; the lead judges it at click 1.
- **D-3 — The finest level is drawn dim.** Its line is about 1 px and low in contrast against the background, so that at a distance it fades into the neutral grey instead of tinting it (F-P15-8; *"the grid's own colour"* superseded by RD-P19-3). The four levels are kept.
- **D-4 — The swap rule** (written once, in [LCDSchema](../../specs/Contract/LCDSchema.md) beside *"the mesh's UV unit must be the article's tile"*, the rule a grid tests, SP-F1):
  - **Which grid:** each article's grid is the tag nearest its `meters_per_tile` on a log scale; a tie goes to the larger grid.
  - **Its size:** the binding's `uv_scale` becomes the old value × (grid tile ÷ article `meters_per_tile`).
  - **Kept:** `uv_offset` and `uv_rotation`.
  - **No size:** an article with no `meters_per_tile`, a `meters_per_tile` of `0.0`, or the tag `sUKN` gets the hatch, with `uv_scale` unchanged. This covers a fitted article that tiles nothing (RD-P18-8).
  - **Matter and Character alike:** the rule reads the article, never its group.
  - **Not a library article:** a material that is not a library article is left alone, and the swap lists it.
  - **On an atlas:** an article sampled on the mesh's own atlas (`cutout_map`, `base_color_map`) is swapped like any other. Its card then shows solid, which is correct for a size check.
- **D-5 — Blender's swap needs each material's real size.**
  - **`gen_asset_library.py` stamps `ml_meters_per_tile`**, beside the identity it already stamps (`imrsv_matter_identity`). This is additive, and the library is regenerated. The scale-test fixture builder stamps its own materials the same way.
  - **The stamp is not put in `load_article.build`** *(revised at Pass 2, 2026-10-15)*. Every thumbnail's record keys on the hash of `blender/masters/*.py` (`showcase.masters_hash`), so any edit there stales all the kept thumbnails, and re-making them took 2475 s of GPU at Phase18 18.3 (F-P19-2).
  - A material without the stamp is looked up by `ml_article` in the registered Matter asset library.
  - The swap **never falls back to the name's tag silently**: that would misreport the 15 off-tag articles.
- **D-6 — Where the scale view lives in Blender:** a module of its own inside the existing add-on package `blender/addons/imrsv_lcd_export/` (one Matter add-on to install later), with an on/off action.
  - At the sitting, the view script registers it for that session from the repo copy, which changes nothing in the lead's preferences.
  - Turning the view off restores each slot's own material, recorded on the object when the view went on.
- **D-7 — The rig's scale view:**
  - a flag on `rig.py --character`, which binds each part's grid, chosen by D-4 from that part's article;
  - the job divides `st` by the **grid's** tile, so no `uv_scale` correction is needed there (F-P15-2);
  - a part on its mesh's atlas keeps its source `st`, as today (`build_character.atlas_parts`, the one copy of that rule), so its grid draws one tile per atlas unit (F-P19-5);
  - the test scene gains nothing: a grid on it is right by construction.
- **D-8 — The golden cube:**
  - its UVs become one tile per face (`[0,1]`, the 1 m grid's real scale), not `[0,10]` with a `uv_scale` override, because Blender exports no UV ports;
  - the table keeps its two Copper instances;
  - [CreatorAssetProfile](../../specs/Contract/CreatorAssetProfile.md) §History records the change.
- **D-9 — Holding the scale options firm (RD-P19-2)** *(added at Pass 2, 2026-10-15)*:
  - **The rule, written once,** in [Identity](../../specs/Ontology/Identity.md) §Scale tags:
    - `meters_per_tile` is exactly the tag's length;
    - an `sUKN` article authors `0.0`;
    - a resolution option keeps its article's size (RD-P19-1).
  - **The gate:** the existing `recipe` lane refuses a recipe whose `meters_per_tile` is not exactly its tag. No new lane is added.
    - The 15 articles already off their tag (F-P15-1) are named in the check as known, each to be redone.
    - So the gate stays green, and a 16th cannot join them.
  - **Never stretch a source to fit.** Stretching Oak's 0.8 m picture over 1 m makes its grain 25 % too large, which is the very error this phase exists to show.
    - A source whose real size is not a scale option is re-made at an option's size, or not used.
    - A generated texture (`/matter-generate`'s lane L2) is made at the option's size from the start.
  - **The generation tools:**
    - `import_ambientcg.py` says whether a scan's size is a scale option;
    - `/matter-generate`'s *"Use that value, and the nearest scale tag"* becomes: use a scan only at a scale option's size.
    - On 2026-10-15 a sibling session had uncommitted edits in `.claude/skills/`, so re-check `git status -s` before touching them.
  - **The 15 become redo rows** in `library/wishlist.yaml`. The material-making process (`/matter-batch`) works them, not this phase.
  - **The scale view names them:** turning it on also lists every article whose recorded size is not exactly its tag, beside the materials it left alone.

### Risk lane — **build**

Read against the tree on 2026-10-14, and again on 2026-10-15 (Pass 2, with Phase18's 18.4 commits in). No authorization, secrets, destructive migration, data loss or public edge. The controls the phase meets:

- **`run_all.py` enumerates the tree.** `materials` globs every `.mtlx`; `recipe` and `determinism` glob every recipe. The new articles must pass them; `recipe`'s G7 keeps a `utility/virtual` article free of wear layers.
- **The `recipe` lane gains a check (D-9)**, inside the lane, as Phase18's G8 did. It names the 15 known articles, so the baseline stays 15 PASS, 2 SKIP, 0 FAIL.
- **The release lanes key on `*.lock.yaml` / `*.catalog.json`, not on the tree**, so an unpinned article touches none of them.
- **The thumbnails' freshness keys on `blender/masters/*.py`** (`showcase.masters_hash`): a control that enumerates a folder. The phase leaves that folder alone (D-5). Its only thumbnail work is the seven new grids.
- **The site file and the dev catalog read `sUKN` as on the grammar** since Phase18's `1a0ddc4` (`SCALE_RE`). Before that commit, the `sUKN` grid would have been served at a version-less path (F-P19-3).
- **Baseline, measured on 2026-10-14 and again on 2026-10-15, the same on both days:**
  - `run_all.py`: 17 lanes, 15 PASS, 2 SKIP (compression and staging: no encoder), 0 FAIL;
  - `check_exporter.sh`: PASS, the baseline 19.2 needs before editing the add-on (`LOCAL_DELTAS.md`);
  - `check_conformance.sh`: PASS. It resolves the golden against the **working tree's** `MatterLibrary/materials`, so the cube can wear a grid no release carries yet.
- **`verify_asset_library.py`** reads `matterlib-0.1.0`'s catalog, which the grids are not in, so regenerating the library only adds to it.
- **No Unreal runtime is owed:** the `Opaque` master's defaults do not change.

### Steps

| Step | What a person can use when it lands | First clickable result |
|---|---|---|
| **19.1** | The seven scale grids, in the library and the Asset Browser | click 1 |
| **19.2** | Scale view on and off in Blender, on any scene | clicks 2–3 |
| **19.3** | Scale view in the rig, on the character | click 4 |
| **19.4** | The golden's 1 m cube in the 1 m grid | click 5 |

*Reconciled click by click:* each click needs only its own step and the ones before it. Click 1's drag from the Asset Browser needs only 19.1's regenerated library. Click 2's fixture is built by 19.2. In-now bullets map one to one; the spec and Glossary updates land with the step that makes them true, and the ledger offer lands *at the close*. **The doer is the agent throughout:**
- the fixtures are built headless;
- the lead's Blender is opened, not reconfigured;
- the lead's asset library is already registered, as `asset_library`, set to Append (read from his preferences on 2026-10-14 and 2026-10-15, nothing saved).

### Compact build map

- **19.1:**
  - `tools/converters/gen_scalegrid.py` writes the seven PNGs (deterministic; the `determinism` lane is the check).
  - Seven recipes in `tools/converters/recipes/`, with `lcd_ports` as the UV grid's: `base_color_tint`, `uv_scale`, `uv_offset`, `uv_rotation`.
  - Assemble the articles; provenance follows the UV grid's (procedural, the script as source).
  - `uv run tools/parity/rig.py <grid>` for each grid (Storm and Blender), then status `candidate`.
  - Regenerate the library: `blender --background --factory-startup --python tools/generators/gen_asset_library.py`.
  - The seven thumbnails: `uv run tools/thumbnails/make_thumbnails.py <grid>…`. Each took 13–41 s at Phase18.
  - Click 1's scene builder lives in a scratch folder, not the repo.
  - Docs: Glossary, Catalog, MasterSet.
  - D-9:
    - the Identity line;
    - the `recipe` lane's check, with the 15 named;
    - `import_ambientcg.py`'s size line, and `/matter-generate`'s wording;
    - the 15 redo rows in `library/wishlist.yaml`.
- **19.2:**
  - `check_exporter.sh` baseline first.
  - `tools/generators/gen_asset_library.py`: the `ml_meters_per_tile` stamp, then regenerate the library. **Not `blender/masters/`** (D-5).
  - The new module in `blender/addons/imrsv_lcd_export/`, with a pure-Python unit test for D-4's choice and arithmetic beside the add-on's existing tests.
  - The scale-test fixture builder writes its error record beside the `.blend`.
  - The D-4 section in LCDSchema.
  - Close the step with `check_exporter.sh`.
- **19.3:**
  - `tools/parity/rig.py` (the flag; `cast_for`) and `tools/parity/job.py`. `write_character_scene` binds each part's grid and divides `st` by the grid's tile; atlas parts keep `k = 1.0`.
  - `JOB_FORMAT.md` §The character job.
- **19.4:**
  - `tools/conformance/build_portable.py`: a list of articles.
  - `golden/creator_table_lightweight.usda`: the cube's binding and UVs.
  - Rebuild the portable form, run `check_conformance.sh`, look at its render.
  - `CreatorAssetProfile.md` §History.
- **Tests (build ceiling):** the existing gates, the 19.2 unit test, and one real-path smoke, the click-2 scene, rendered headless before the sitting. No new gate or lane.
- **Shared tree:** on 2026-10-15, Phase18 was executing 18.4 in the same tree (`tools/converters/`, `tools/releases/`), and its close conforms the Glossary, LCDSchema and the Catalog. Re-check `git status -s` before each commit to those files.

---

## Findings (Pass 1, 2026-10-14; re-measured and extended by Pass 2, 2026-10-15)

- **F-P15-1 — The library today** (re-measured 2026-10-15; a throwaway script read every `.mtlx`'s `imrsv_metadata`):
  - **Count:** 97 articles: Pass 1's 95, plus Phase18's fitted teeth set and green eye.
    - 79 tile at their tag's size.
    - **15 tile at another size**, the same 15 the research found: e.g. Oak `s1` at 0.8 m, Concrete_Polished `s1` at 3 m, MildSteel_Raw `s01` at 0.3 m.
    - **3 are `sUKN`, each with `meters_per_tile` `0.0`:** the system `IMRSV_MissingMaterial`, `Teeth_Natural` and `Eye_Green`.
  - **Tags in use:** `s001` 46 (30 of them Character, the six skins among them), `s01` 38, `s1` 10, `sUKN` 3. **None** are at `s0001`, `s10` or `s100`.
  - **Others:** no article authors a `uv_scale` other than 1. Two articles carry their own fitted picture (`base_color_map`, with `fits`): the teeth set and the green eye. The other atlas-sampled cases get their picture from the binding, as before.
- **F-P19-1 — The skin keeps its tile, so clicks 2 and 4 hold whichever phase runs first.**
  - Under Phase18, a fitted article is `sUKN` only when it tiles nothing. *"One that also tiles a detail, such as pores, keeps that tile's tag"* (RD-P18-8).
  - *Skin Maps* (RD-P18-10: *"its own phase, straight after this one"*) keeps the skin article as the substance, its tiling micro layer included (its seed's §Scope, F-SKM-11, F-SKM-13).
  - So a skin on the raw body atlas is still the 170× case. The six skins are `s001` today, and they stay tiled either way.
- **F-P19-2 — An edit under `blender/masters/` re-makes every thumbnail.**
  - `showcase.masters_hash()` hashes `blender/masters/*.py`, and every kept thumbnail's record holds it.
  - Phase18 moved the hash at 18.3 and re-made 79 thumbnails (2475 s of GPU), though nothing they draw had changed.
  - D-5 as Pass 1 wrote it (a stamp in `load_article.build`) would have done the same. `gen_asset_library.py`, which already stamps each asset's identity, author and licence, is outside that folder: hence D-5's revision.
- **F-P19-3 — `sUKN` is on the grammar in the projections since 2026-10-15.**
  - Phase18's `1a0ddc4` widened `SCALE_RE` to `_(s\d+|sUKN)$` in `project_runtime_catalog.py` and `working_tree.py`. Before that, an `sUKN` article was served at a version-less path with no scale.
  - The other tag readers already take `sUKN`: `validate_material.SCALE_TAGS`, `import_ambientcg.SCALE_TAGS`, and the assembler's layer check, which refuses `sUKN` only on a shared wear layer.
  - `assemble_mtlx.SCALE_TAG_METRES` is the library's tag-to-metres table, and D-4's choice of grid matches it.
  - `job.py` reads a `meters_per_tile` of `0.0` as `1.0`, so the rig and the thumbnail tool draw the hatch without dividing by zero.
- **F-P19-4 — The grids owe thumbnails, drawn at true size.**
  - `make_thumbnails.kept()` takes every `approved` or `candidate` article that is Creator-selectable. Since the grids are `candidate`, all seven are kept.
  - `showcase.subject_for` gives class `virtual` the `card` subject, a 0.3 m card face on. The subjects divide `st` by `meters_per_tile`, so every article is pictured at true size.
  - On a 0.3 m card, the `s10` and `s100` grids show only their finer lines on grey, and the `s0001` grid near-neutral grey (RD-P19-3). That is what the grid is designed to show from a distance (D-2, D-3). It is kept as every article's rule, with no per-grid exception.
- **F-P19-5 — Atlas parts in the rig keep their source UVs.** Since Phase18, `build_character.atlas_parts()` is the one copy of the rule. The character scene neither rescales such a part's `st` by the article's tile nor lets the article's UV placement move it (`job.py`, `k = 1.0`). In the rig's scale view, then, a tiled article on an atlas part shows its grid one tile per atlas unit, and an `sUKN` article shows the hatch.
- **F-P19-6 — The consumers were swept read-only** (`LOCAL_DELTAS.md` §Separation; each fetched 2026-10-15): the platform's docs, Stage, the website, USDLiveView and the asset library. Nothing in them is about the library's scale grids or a scale view.
- **F-P19-7 — *Matter* names a group now** (Glossary *Group*, Phase15): Matter, Character and HDRIs. Pass 1 wrote *"Matter objects"* to mean any library material. The scale view covers Matter and Character alike, as click 2's skin and click 4's character already assumed, and the Brief now says so.
- **F-P19-8 — The generation tools write fractions on purpose today, and nothing checks for them** (read 2026-10-15; the reason for D-9).
  - `import_ambientcg.py` prints `meters_per_tile` from the scan's own physical size (`dimensionX`).
  - `/matter-generate` says *"Use that value, and the nearest scale tag"*.
  - `validate_material.py` checks only that the tag is in the closed set. No lane compares an article's size with its tag.
  - That is how the 15 off-tag articles came in, among them the scans at 0.8 m, 2 m and 3 m.
- **F-P15-2 — The rig is right by construction, so it shows only the mesh's own metres.**
  - The rig never sets `uv_scale`. Each job divides the subjects' `st` (in metres) by the bound article's `meters_per_tile`, so a grid bound in the rig always draws at true size.
  - What it can show is where the mesh's metres are wrong. On the character, the atlas's islands run 0.8–2.6 m per UV unit around the median the build scales by (`JOB_FORMAT.md` §The character job).
  - The `uv_scale` correction (D-4) matters in a real scene: Blender, or a USD binding.
- **F-P15-3 — In Blender, an article's size reaches the material only through the mesh's UVs.**
  - One UV unit is one tile. The UV ports are fixed inside the per-article `MatterLCD_` group (`ML_Place2D`) and are never exported ("Studio-side only", the add-on's header).
  - A material carries `ml_article` but not its `meters_per_tile`: hence D-5.
- **F-P15-4 — The Matter add-on is not enabled in the lead's Blender 5.2; the library is registered, set to Append.** Read from his preferences on 2026-10-14, and again on 2026-10-15: still true, with the library named `asset_library`. Nothing was saved either time. Hence D-6's session registration.
- **F-P15-5 — Unreal's default material is itself a world grid** (Learnings Unreal U7). A scale grid must never read as it. ~~The dark background in the grid's own colour is the tell,~~ *(RD-P19-3: the background is neutral; the coloured lines are the tell)* and click 4 shows it once the Unreal column exists.
- **F-P15-6 — The grids reach the website without further work.** `tools/releases/build_snapshot.py` takes every article on disk, and puts `utility` in the `matter` section, as it does the UV grid. The next dev snapshot carries the grids and their words; nothing in this phase publishes.
- **F-P15-7 — The golden pins `matterlib-0.1.0`, which has no grid, and the conformance check does not care.** It resolves against the working tree (`check_conformance.sh`, `PXR_AR_DEFAULT_SEARCH_PATH` over `MatterLibrary/materials`). So 19.4 needs no release.
- **F-P15-8 — Drawn at full strength, the finest level takes the grid's colour over** (probe, 2026-10-14; a throwaway PIL script, nothing kept in the repo).
  - **The probe:** an `s1` grid at 4,096 px with four levels (1 m blue edge, 10 cm, 1 cm, 1 mm). At full size every level reads.
  - **Reduced to screen size** (a 1 m face across 1,024, 512 and 256 px), the 1 mm lines, one every 4 px, turn the dark-blue background into the 1 mm colour; at 256 px the whole grid is one haze.
  - **So** RD-SP-4's two halves, four levels and *"its base"* colour, hold together only when the finest level is drawn dim: D-3. Click 1's far view checks it.

## Discovery Log

- **Pass 1 (2026-10-14):**
  - **Read:** the product docs from `_Architecture.md` down to Identity (the grammar and scale tags), MasterSet §Scale and LCDSchema (`uv_scale` divides; the UV-unit rule); the research `261014_R_ScaleProbes.md` and `261013_R_PlatformTrackedItemsAsks.md` A1; the Blender, MaterialX, Storm and Unreal learnings (B1, B2, B10, B11, M2, S5, U7 apply).
  - **Walked in code:** the UV grid's generator, recipe and article; `run_all.py`'s lanes; the rig's character job; `load_article` and the add-on; the asset-library generator and verifier; `build_portable.py`, the golden and `check_conformance.sh`; `build_snapshot.py`.
  - **Measured:** the 95 articles; the lead's Blender preferences; the gate, exporter and conformance baselines; and one probe (F-P15-8).
  - **Rulings:** no lead ruling newer than the Roadmap's order of 2026-10-14 bears on this phase.
  - **Questions:** the seed's open questions are closed as D-1 (where), D-2 (palette), D-3 (the finest level) and the first test's clicks 2 and 4 (a character first, then the conformance table). None is with the lead.
- **Pass 2 (2026-10-15), the re-verify Pass 1's retro asked for, opened by the lead's *"/discovery P19"*:**
  - **Read:** what Phase15 – 18 changed: the Glossary's groups; Phase16's contributor and licence; Phase17's thumbnail tool (`kept`, `subject_for`, `masters_hash`); Phase18's Brief, its rulings RD-P18-8 to RD-P18-10, and its 18.1 – 18.4 commits; and the *Skin Maps* seed. A message from Phase18's live execute session pointed at `1a0ddc4`, which this pass had already read.
  - **Measured:** the 97 articles (F-P15-1). The gate (15 PASS, 2 SKIP, 0 FAIL), `check_exporter.sh` (PASS) and `check_conformance.sh` (PASS), with Phase18's 18.4 commits in. The lead's Blender preferences (F-P15-4). The consumers (F-P19-6).
  - **Changed in the Brief:** the Status line; click 2 (library materials, and the fitted teeth reading the hatch) and click 4 (atlas parts); D-1's `0.0`; D-4 (no size, both groups); D-5 (the stamp's home); D-7 (atlas parts); the thumbnails in 19.1; the risk lane's controls; and the steps renumbered `19.n`.
  - **Rulings newer than Pass 1:** RD-P18-8 and RD-P18-10 (F-P19-1). Neither reverses a decision here. **Sequencing:** RD-P18-10 puts *Skin Maps* straight after Phase18, while this phase holds the number 19. The Brief holds under either order, so which runs first is the lead's call and blocks nothing here.
  - **The lead's rulings in this session**, after a sketch of the grids was shown (a throwaway picture, nothing kept): RD-P19-1 (a resolution is an option of one material) and RD-P19-2 (sizes fit the scale options exactly). From RD-P19-2: D-9, F-P19-8, click 2's list, and the in-now and not-now bullets.
  - **Questions:** none is with the lead.

## Execution Log

**Tree at start (2026-10-15):** `main` at `1e1e3d9`, the library machine, 5 commits unpushed. Six Refiner-lane files (`.ai/commands/LOCAL_DELTAS.md`, `.claude/**`, `AGENTS.md`, `_RefinementBacklog.md`) are modified by a sibling session from 2026-10-14 15:34; not touched. Gate 15 PASS, 2 SKIP, 0 FAIL.

| Step | Landed | Result | Next |
|---|---|---|---|
| **19.1** (in progress) | `9cb062e` (WIP) | The seven grids, G9 and its RED fixture, the library regenerated (gate 15/2/0). **❌ Click 1, the lead (2026-10-15):** *"I am not sure what I should be judging here... I can tell if this is everything we have an issue because it does not solve what I am trying to achieve... these are a bunch of different colored squares and I see not relation of grid size between them"*. Read against the scene: each grid on its own 1 m card, seen from across the room. The finer grids' lines are a fixed fraction of their tile, so they vanish and those cards read as flat colour. The tile edge is drawn in the tile's colour on a dark shade of that colour, so it hides. The same 10 cm line is also 4× thinner in the 10 cm grid than in the 1 m grid. Second form, the lead's: *"there is a 10 meter square with a 10 meter material ... then a 1 meter square next to it ... the square exampel needs to change so we are seeing it scale down"*: six squares, each its grid's tile, side by side. Then RD-P19-3: the background goes neutral, and only the lines carry colour. **✅ Click 1, the lead (2026-10-15):** *"YES! NOW we can see the colos of the grid clearly..."* | finish 19.1 (rig, thumbnails, docs, D-9's tool wording and redo rows) |
| **19.2** (in progress) | the 19.2 WIP commit | The scale view (the Matter tab), the swap rule and its unit test, the size stamp in the library (D-5), and the scale-test scene builder, whose `--smoke` passes ON and OFF (8 of 8 slots). Exporter check PASS before and after. **✅ Click 2, the lead (2026-10-15):** *"HA! COOL! This is amazing!"*. Seen in his window: the view on, the steel crate selected with its 2.5× scale showing, and the panel listing the four off-option materials. **Named before reading the record**, the lead: *"copper box, the body for SURE was really bad, and the big crate looks maybe off but I don't really know it's material, I guess the unknow scale is the teeth and that is just strange"*: all three planted errors (the Copper box's default UVs, the skin on the raw atlas, the crate at 2.5×), and the hatch read as size unknown. The teeth on a plain box read as strange: a fixture defect, so the hatch case moves to a fitted article on its own part mesh. **✅ Click 3, the lead (2026-10-15):** *"yes, all back to normal (but the wrong scale_ :)"*. Read inside his Blender: all 8 slots hold their own material, with no grid copies and no restore records left. | finish 19.2 (LCDSchema §Scale view, the hatch fixture on a part mesh); 19.3 |
| **19.2** tail | `6b01dc1` | LCDSchema §Scale view (D-4, written once). The teeth hatch is now on the teeth part mesh; `--smoke` PASS, 9 of 9. | — |
| **19.3** | `af4b982` | `rig.py --character --scale-view`. **Deviation (the surface):** the first sheet could not show click 4. A grid's lines are a fixed fraction of its tile, so a 1 cm grid is grey haze at whole-body and face distance. Five swatch views, 3 cm across, were added to the character scene; the other jobs are unchanged. **Corrected fact:** an Unreal runtime ran on the library machine, so the sheet has all three columns (the Brief: *"The Unreal column comes from the machine with Unreal"*). Seen, not fixed: in Unreal's mouth view the hair cards disappear, because an Opaque grid on a card is one-sided there. | click 4 |
| **19.4** | `73cff74` | The golden cube wears the 1 m grid. `check_conformance.sh` PASS, `check_exporter.sh` PASS, gate 15/2/0. | click 5 |
| **19.1** docs (in progress) | — | **Deviation (a false premise):** the Brief's *"the grids join the Catalog"*. [Catalog](../../specs/Catalog/Catalog.md) is a view of a **release** (its one table is `matterlib-0.1.0`), and no working-tree article is listed there. The grids join it with the first release that carries them. MasterSet, Glossary and Identity (D-9) are edited and not yet committed: Identity's line names the redo rows, which are not written yet. | 19.1's tail |

### Resume (2026-10-15, after 19.3 and 19.4 landed; clicks 4 and 5 owed)

- **Where:** clicks 1–3 passed. 19.2 is complete. 19.3 and 19.4 have landed, and their sittings (clicks 4 and 5) are owed. 19.1's tail is not done.
- **Next:** the lead's verdict on clicks 4 and 5 (the sheet `library/parity/Character__Teeth_Natural_Clean_Base_sUKN_v01__scale_view/sheet.png`; the golden's render from `check_conformance.sh /tmp/claude-p19/conf`). Then 19.1's tail, as listed below: rig each grid, mark them `candidate`, the seven thumbnails, D-9's tool wording, and the 15 redo rows. Commit the docs (Glossary, MasterSet, Identity) with the redo rows.
- **Still owed:** the click-1 Asset Browser drag and the five Blender learnings, both in the block below. The drag was asked for at the clicks 4–5 sitting.

### Resume (2026-10-15, at the act boundary after clicks 1–3; kept for its 19.1 list)

- **Where:** clicks 1, 2 and 3 passed. Steps 19.1 and 19.2 have their sittings done; each has owed tail work that needs no sitting.
- **Next, in order:**
  1. **19.1's tail.**
     - Each grid through the rig: `uv run tools/parity/rig.py <grid>` (Storm and Blender). Then `"status": "candidate"` in the seven recipes, and re-assemble.
     - The seven thumbnails: `uv run tools/thumbnails/make_thumbnails.py <grid>…`. Each is drawn on the `card` subject. The sUKN grid draws at 1 m, since `job.py` reads 0.0 as 1.0.
     - Docs: Glossary *Scale grid* loses *(planned)* and says neutral background, coloured lines (RD-P19-3); the grids join the Catalog and MasterSet tables; Identity §Scale tags gets D-9's line.
     - D-9's tools: `import_ambientcg.py` prints whether a scan's size is a scale option. `/matter-generate`'s *"Use that value, and the nearest scale tag"* changes; `.claude/skills/` holds a sibling's uncommitted edits, so use a filtered stage. The 15 redo rows go in `library/wishlist.yaml`.
  2. **19.2's tail.**
     - LCDSchema §Scale view: the D-4 rule, written once, beside *"the mesh's UV unit must be the article's tile"*.
     - `scale_test_scene.py`: the fitted-teeth hatch case moves from a plain box to the teeth part mesh (`library/kits/MakeHuman_Teeth_v01`), after the lead's *"that is just strange"*. Re-run `--smoke`.
  3. **19.3:** the rig's scale view on the character (D-7, F-P19-5), then click 4.
  4. **19.4:** the golden cube in the 1 m grid (D-8), then click 5.
- **Sitting files** (scratch, not committed): `/tmp/claude-p19/click1/build_powers.py` (click 1 as it passed); `/tmp/claude-p19/click2/` (`scale_test.blend`, its record, and `view_scale_test.py`, which registers the add-on for a session). Rebuild them from the builders; do not trust them to survive a reboot.
- **Unresolved:** none with the lead. Click 1's first scene (each grid on a 1 m card), then a checker, were rejected; the powers-of-ten form and a neutral background passed.
- **Owed from click 1, not exercised:** the Asset Browser drag (find the grids under *Matter / Utility / Virtual*, drag one onto an object). The scene changed form at the sitting, and the drag was never done. Ask for it at the next sitting. The line hues (D-2, blue 1 m) were seen, never judged on their own: *"NOW we can see the colos of the grid clearly"*.
- **Learnings owed at the close** (`docs/Learnings/Blender/`, found driving the lead's Blender 5.2.2 at click 1):
  - Each factory workspace carries a mode: *Texture Paint* opens in paint mode with half the window an image editor, and *Sculpting* opens in sculpt mode. Set `workspace.object_mode = "OBJECT"` on any workspace built for a viewer.
  - `bpy.ops.workspace.duplicate()` from a script, then a rename in the same call, crashed the GUI (*"Couldn't find layout in this workspace"*).
  - `bpy.ops.screen.area_close()` with an area override works from a script, and its neighbours expand into the space.
  - In camera view, `view_camera_zoom` did not frame the camera from a script. A perspective view copied from the camera does, with the viewport `lens` at twice the camera's to match its field (measured here).
  - A bpy struct's Python wrapper is new on each access, so compare with `!=`, never `is`.
