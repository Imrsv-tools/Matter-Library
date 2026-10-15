# Phase18 — Character Materials, Their Own Library

**Status:** IN EXECUTION (2026-10-15, the lead: *"/execute P18"*). Brief ready the same day — both lead calls answered: the lead, *"A on both, then /execute P18"* (Q-P18-1 → **RD-P18-9**, Q-P18-2 → **RD-P18-10**). Lane **build**. Opened by the lead 2026-10-15: *"/discovery p18"*. The Brief is written to the recommended answers. If you choose otherwise, only the steps that call says it reaches change. *(Seeded 2026-10-14 by `/research` on the lead's word: *"yes record it and seed all three"* (RD-DS-5). Numbered Phase17, then Phase19 (RD-DS-6, RD-DS-7), and Phase18 since RD-DS-8. It follows Thumbnails ([`Phase17_Thumbnails.md`](Complete/Phase17_Thumbnails.md)), whose character views it pictures each part with.)* **This phase's ids start at `Q-P18-1`, `F-P18-1` and `RD-P18-1`.** None existed before this pass (searched 2026-10-15).

## Outcome

**A contributor can craft a set of teeth, a skin or an eye that fits the character's own part mesh, keep their name on it, and see it pictured on that part: teeth on teeth, skin on half a face and hands, an eye on an eyeball.**

## Why this is a phase of its own

The lead: *"the characters dots do not use "matter" level materials very well.. they look like totall shit to be frank... We need to think about character materials differnly so they need to officiallbe handled in a another very clear taxonomy/ontology that people can participate in. the need to be able to craft a set of teeth that will uvmap to the predefined teeth mesh we picked, and that should keep their name so people can realize how great a teeth a particular contributor is"* (RD-DS-4). Character materials stop being tiling Matter materials put on a body. Each becomes a set of maps authored to one part mesh's UVs.

**Where it stands after Phase15–17** (F-P18-2, F-P18-3):
- **Character has its own place.** The folder is `materials/character/humanoid/<part>/`, and each file declares its group, species and part (Phase15).
- **Every file says who gave it and its licence** (Phase16). Blender shows them as Author and License.
- **Every part is pictured in a human context** on the whitelisted views (Phase17).
- **A picture drawn on a mesh's own UVs already reaches every target.** This is `base_color_map`, sampled on the mesh's `st` (Phase09). The eyes and the hairstyles use it today.
- **What is missing:**
  - **The part meshes have no name or version.** They exist only inside the rig, pinned by the CC0 pack's hash. A contributor cannot get one without running the rig.
  - **A fitted picture is not an entry.** It has no name, no contributor, no catalog row and no place in a release (F-DS-2).
  - **Nothing checks** that a picture fits its mesh.

---

## The Brief

### First human test

**Where:** the library machine, which has Blender 5.2.2 and no Unreal. **The agent plays the contributor and drives every tool. The lead looks and judges.**
- **The fixture is library-made**, so its contributor is `MatterBot` (RD-P16-11).
- **A unit proves that any other handle reaches the same places.**
- **A scene for the lead is built headless from the factory scene into its own file**, then opened detached (Blender B10, B11). Every sheet's path is in the handback.

1. **The teeth kit (18.1).** The agent opens the teeth part mesh's kit in the lead's Blender. It shows:
   - the mesh `MakeHuman_Teeth_v01`;
   - its UV layout in the UV editor, over the kit's layout picture;
   - today's `Enamel_Natural` and `Gum_Natural` on it.

   *Judge: could a contributor paint a set of teeth against this, and is it the teeth Studio's character wears?*
   - **The surface can show it.** Blender's UV editor draws the layout, and the mesh is the real pinned one.
   - **It is Studio's mesh too.** Studio's character is built from the same CC0 pack and the same teeth mesh (F-P18-5).
2. **A set of teeth, contributed and checked (18.2).** The lead's Asset Browser, under **Character › Humanoid › Teeth**, shows the new teeth set with **Author** and **License**. Dropped on the kit's teeth, it draws its own picture on the teeth and the gums.

   *Judge: it fits, and it says whose it is.*
   - **The agent's evidence goes in the 18.2 log:**
     - the gate passes the teeth set;
     - it refuses a misfit three ways: an unknown mesh, the wrong size, and a picture that leaves a UV island empty;
     - the rig's Storm and Blender columns agree on it.
   - Execute reads the article's `fits` and contributor from the file, never from its name.
3. **Pictured on its part (18.3).** The thumbnail sheet shows two things:
   - the teeth set in the `mouth` view (teeth and gums, face hidden), beside today's `Enamel_Natural` + `Gum_Natural` thumbnail;
   - a fitted eye in the `eye` view, beside today's `Eye_Natural`.

   *Judge: teeth on teeth and an eye on an eyeball, and the teeth read better than flat enamel.*
   - The surface is the 1024² showcase picture. The `mouth` view frames only the teeth, gums and tongue (F-P17-22), so the atlas's enamel and gum variation sits in the frame.
4. **Out to contributors (18.4).** The next dev snapshot's GitHub pre-release page, published at the lead's word, holds three things:
   - the kits, one per named part mesh;
   - the teeth set and the eye, with their contributor, part, the mesh they fit, and their thumbnails;
   - `CONTRIBUTING.md`, which now has a Character path.

   *Judge: an outside contributor could start from here.* How the website lays it out is the website's work.

**Reconciled click by click:**
- Click 1 needs only 18.1.
- Click 2 needs 18.2, on 18.1's kit.
- Click 3 needs 18.3.
- Click 4 needs 18.4.

Every tool any click uses is Blender, `gh` or the thumbnail tool, and all three have run on the library machine (Phase15–17).

**Not a click: the rig's Unreal column** for the teeth set. It runs on the machine with Unreal the next time work is there. No master changes, so no new runtime is owed (F-P18-7).

**The doers:** the agent makes the fixture, renders and publishes (`gh`, as for dev.1–dev.7). The lead looks, and gives the word to publish.

### In now

| What | Step |
|---|---|
| **The part meshes, named and versioned** (RD-P18-1): `MakeHuman_Body_v01` (hm08), `MakeHuman_Eyes_v01` (the high-poly eye), `MakeHuman_Teeth_v01` (`teeth_base` and its five shapes), `MakeHuman_Tongue_v01`. Each is recorded with its source in the pinned pack, its UV-layout hash, and the rig parts it yields. | 18.1 |
| **A kit per mesh version** (RD-P18-4): the mesh with its UVs, its layout picture, and the spec page. It is made from the pinned pack into a git-ignored folder. | 18.1 |
| **A Character article declares the mesh it fits:** `fits` in its recipe and its `imrsv_metadata` (RD-P18-2). | 18.2 |
| **A fitted article carries its own picture** (RD-P18-9). The assembler writes the recipe's picture as `base_color_map`'s value. Every other article assembles byte-identically. A binding can still supply its own (Carrier rule). | 18.2 |
| **The check against the UVs**, in the existing recipe lane (RD-P18-5): a known mesh version, the picture's size and format, and every UV island covered. | 18.2 |
| **The targets take the article's own picture** when the binding supplies none: Blender's loader, the rig's job, and so the Blender asset library. Storm reads it natively. | 18.2 |
| **The fixture: a set of teeth**, `Teeth_Natural_Clean_Base_sUKN_v01` (RD-P18-6, RD-P18-8). It is bound on the Teeth and Gums parts, as `Eye_Natural` is bound on three eye parts. | 18.2 |
| **Pictured on its part:** the thumbnail tool binds the article's own picture, and a `Teeth` family goes on `mouth`. | 18.3 |
| **A fitted eye**, one of the pack's CC0 eye pictures carried in its own article (RD-P18-6). It shows that the rule holds on a second mesh. | 18.3 |
| **`fits` in the dev catalog and the site file** (additive: schema numbers unchanged). | 18.4 |
| **The kits and the two articles in the next dev snapshot**, published at the lead's word. | 18.4 |
| **`CONTRIBUTING.md` gains the Character path** (F-P18-8). | 18.4 |
| **The consumers told**, through a new ledger row for Stage (read an article's own fitted picture when the binding supplies none) and a note on M11 for the website (`fits`). The ids are claimed at execute. | 18.4 |
| **Docs conformed:** LCDSchema §Base colour map; Taxonomy §Character (the mesh a part fits); Identity (a fitted article's scale tag; the contributor is not in the name); MaterialXTemplate and RuntimeCatalog / SiteFile (`fits`); the Glossary (*Part mesh*, *Mesh version*, *Approved human mesh*, *Fit set*); the SkinMaps draft (Q-SKM-4 answered, F-P18-1's label); ToolingConventions (the kit tool). | at the close |

### Not now

| What | Why not now | What it will consume from this phase |
|---|---|---|
| **Skin maps: a skin that fits the body** | RD-P18-10 (the lead chose A): *Skin Maps* is its own phase, straight after this one. It owes its own work: the six skins re-assembled (F-SKM-19), Blender's map-following scatter (F-SKM-23), and the calibration (F-SKM-20, F-SKM-25). | `MakeHuman_Body_v01` and its kit, `fits`, the article-carried picture, the coverage check, and the `face` and `hand` thumbnail binding. Its draft spec's Q-SKM-4 is answered here. |
| **Skin Maps Beyond Colour** | Parked (RD-DS-8). | The same, plus each new input it adds. |
| **Moving today's fit pictures into articles** (the nine eye colours and the hairstyles) | Studio reads them from the fit set today (P21). Moving them changes what a consumer binds. Nothing in the Outcome needs it. | The rule and the check. A move is one article per picture. |
| **Hair That Reads as Hair** (RD-P18-7) | A card is fitted per hairstyle and has its own research. Strands are the real path (MAP-RD4). | The mesh registry and the rule, for a hairstyle's cards. |
| **A tongue or gums contributed on their own** | The tongue's mesh is named and given a kit here, so anyone can start. The fixture is the teeth. | The tongue's kit. |
| **Other species** (canine, equine) | The taxonomy allows them (Phase15). None is made. | The registry's shape: family, mesh, version. |
| **Studio and Stage drawing a fitted article** | The platform's work, asked through the ledger. | The article's `base_color_map` value and `fits`. |
| **Contributions through an upload door, gated and rigged on a server** | The Library Service is on hold (RD-MP-14). | The check and the kit. |

### The reuse check

**What the stack already gives:**
- **`base_color_map`** (Phase09, LCDSchema §Base colour map). It is a picture sampled on the mesh's own `st`, outside `place2d`, on Opaque, Masked, Hair and Subsurface. It is shipped in the articles, the Blender masters and the library's Unreal masters.
  - **This phase adds no new input.** It only lets an article name the picture's value.
- **The Carrier rule.** A binding that supplies a picture still overrides the article's own.
- **`imrsv_metadata`** and its projection into the dev catalog and the site file, as `group`, `species`, `part`, `contributor` and `licence` already ride (Phase15–16). `fits` rides the same path.
- **The rig's part split** (`build_character.py`). The pinned pack's sources, the parts and the meshes' UVs are all already there, so the kit is a projection of what the rig builds.
- **The fit-set generator** (`tools/converters/fit/gen_fit_makehuman.py`) already prepares the pack's eye pictures. The teeth picture is prepared the same way.
- **`tools/converters/groups.py`**, the one table of species and parts. The mesh registry goes beside it.
- **The recipe gate's G5** (folder against group) shows where a Character check lives without a new lane.
- **The thumbnail tool's character views and whitelist** (Phase17). Its record already hashes every texture an article names, so the article's own picture makes it stale when changed.
- **The snapshot builder**, its digests and asset limit, and `gh` publish.

**Each custom layer and its gap:**
- **The mesh registry.** Today a mesh's identity is the pack's hash plus a path inside it. Nothing names a UV layout, so nothing can say *"this picture fits that mesh"* (Q-SKM-4).
- **The kit.** The meshes live inside a 280 MB pack, fetched by the rig into a git-ignored cache. A contributor needs the one mesh and its layout.
- **The coverage check.** No lane looks at a picture against a layout today (F-P18-10).

**Contracts touched:**
- LCDSchema §Base colour map: an article may now name the picture's value.
- MaterialXTemplate: `fits`.
- RuntimeCatalog and SiteFile: `fits`, additive, schema numbers unchanged.
- **RuntimeCatalog's frozen releases are untouched.** No lock names a Character article (Phase15, re-measured at 18.2).

### Decisions that bind

**The lead's rulings:**
- **RD-DS-1:** *"the comples maps that are moving to for the characters need to be in chracters"*; generic biological materials stay in Matter.
- **RD-DS-3:** the facts go inside the file, with no sidecars.
- **RD-DS-4:** craft a part to the predefined mesh, keep the contributor's name, and picture it on the part.
- **RD-SKM-1:** one approved mesh. A map is made per mesh version, and fits every body shaped from it.
- **RD-SKM-2:** no photographs of people for skin.
- **RD-P16-11:** library-made entries are `MatterBot`'s.
- **GPA-Q2:** the bare name is the stable key; the `id` is not.
- **RD-P13-2 and F-MP-17:** a Character material is pictured in a human context, on the whitelisted views only.
- **RD-P17-1:** Thumbnails built the views. This phase changes which mesh a part is, not how a part is pictured.
- **RD-RO-2:** CC0 only.
- **Pre-release:** no release ceremony gates anything. A push and a publication are the lead's word.
- **CM2** (substance in Matter, fit beside it) **and RD-DS-1 met at Q-P18-1. The lead resolved it: A (RD-P18-9).** For the Character group, a fitted picture lives in its article; CM2 stands for Matter.

**Minted here, closed with a recommendation, unless you say otherwise:**
- **RD-P18-1 — A mesh version is a UV layout, named `<Family>_<Mesh>_vNN`.**
  - A new layout is a new `vNN`. A new shape on the same layout is the same version: the six CC0 teeth meshes share one layout (F-P18-4).
  - Four are named: `MakeHuman_Body_v01` (hm08), `MakeHuman_Eyes_v01`, `MakeHuman_Teeth_v01` and `MakeHuman_Tongue_v01`.
  - They are recorded in `tools/converters/groups.py`, beside the species and parts.
  - This answers Q-SKM-4. *(The seed asked which parts come first and which mesh each fits.)*
- **RD-P18-2 — A Character article that carries a fitted picture declares `fits: <mesh version>`** in its recipe and its `imrsv_metadata`. The gate refuses an unknown mesh version, and a fitted picture without `fits`. An article with no fitted picture declares none.
- **RD-P18-3 — The contributor's name stays in the file, not in the material's name.**
  - It already shows wherever the entry is shown: Blender's Author, the dev catalog, the site file, and the thumbnail sheet's caption.
  - Why not the name:
    - the name is the stable key (GPA-Q2), and a handle in it would change the key when a handle changes;
    - it would use up the 63-character budget;
    - the Variant token is already free words, so a contributor names their look there.
  - *(The seed: "in the name grammar, or in the displayed name … Discovery settles which.")*
- **RD-P18-4 — A contributor gets a part mesh as a kit**, one per mesh version, made by a tool from the pinned pack. Each kit holds the mesh with its UVs (USD, metres, as the rig's), its layout picture at the map's size, and the spec page.
  - It is git-ignored, and published as dev snapshot assets at the lead's word.
  - It is not committed: the pack is the pinned source, and the build is deterministic.
  - *(The seed: "a download from a release?")*
- **RD-P18-5 — The check against the UVs lives in the existing recipe lane**, as G5 does. No new lane.
  - Each mesh version's **UV-island picture is committed beside its record**, small and one-channel, so the gate needs no download.
  - **The check:** a known `fits`; a square sRGB RGB PNG at the mesh's map size; and every island covered, with no empty fill inside it.
  - *(The seed: "how a contribution is checked against its UVs".)*
- **RD-P18-6 — The first instances are a set of teeth and an eye.**
  - **The teeth are the full journey.** The teeth are a flat colour today, and the CC0 pack has the teeth's own atlas.
  - **The eye shows the rule on a second mesh, at almost no cost.** Its CC0 picture already fits.
  - **Skin is its own phase, next (RD-P18-10).**
  - The teeth picture is prepared from the pack's teeth atlas as Phase09 prepared the eye pictures. RD-SKM-2's rule on photographs of people binds skin. Execute looks at the teeth atlas before using it.
- **RD-P18-7 — *Hair That Reads as Hair* is not folded in.** Cards fit per hairstyle, strands are the real path (MAP-RD4), and it has its own research. *(The seed's third question.)*
- **RD-P18-8 — A fitted article's scale tag is `sUKN` when it tiles nothing** (Identity: *"Not defined / not relevant"*, the fit set's tag). One that also tiles a detail, such as pores, keeps that tile's tag. *Scale Grids* (Phase19) re-verifies against this (F-P18-9).

### Risk lane — `build`

**The controls, each read (2026-10-15):**
- **The gates that enumerate the tree.** `run_all.py` walks `MatterLibrary/materials/**/*.mtlx`, the recipes, the fixtures and `library/releases/*`. The teeth set and the eye land under `materials/character/humanoid/`, so the `materials`, `determinism` and `recipe` lanes cover them unchanged. No lane globs `textures/fit/` (F-P18-10).
- **Frozen release records.** No lock names a Character article (Phase15 measured 0). This is re-measured at 18.2. If it still holds, nothing re-freezes.
- **`no_projection_guard`** bans only the tokens `provenance`, `evidence` and `license`. `fits` is none of them.
- **The snapshot's asset limit** (`MAX_ASSETS = 1000`). `dev.7` has 572 assets. This phase adds about ten: two articles' downloads and pictures, and four kits.
- **`tools/conformance/` and `blender/addons/`.** Neither is planned to change. If the asset-library verifier or the exporter is touched, `check_exporter.sh` is baselined before the edit (LOCAL_DELTAS).
- **The Unreal runtime.** No master changes: `base_color_map_tex` is already in the Opaque, Masked, Hair and Subsurface masters. No new runtime is owed.
- **Publication.** A dev snapshot is a GitHub pre-release on this public repo, at the lead's word, as `dev.1` to `dev.7` were in build-lane phases.

No authorization, no secrets, no destructive migration, no data loss, and no public edge of ours.

**Baseline (measured 2026-10-15, the library machine, `main` at `8ba44e9`):** `run_all.py` 17 lanes, **15 PASS, 2 SKIP** (`compression`, `staging`), **0 FAIL**.

**Test surface:**
- the existing units: `test_build_snapshot.py`, `test_thumbnails.py`, the recipe lane's RED fixtures;
- units for the `fits` check (three ways to misfit) and for a non-`MatterBot` contributor flowing through;
- **one real-path smoke**: click 3's render.

### Step list

| Step | Intent — the first clickable result |
|---|---|
| **18.1 — The part meshes, named, and the teeth kit** | The mesh registry (RD-P18-1). The kit tool. Four kits made. The teeth kit opened in the lead's Blender. **Click 1.** |
| **18.2 — A set of teeth, contributed and checked** | `fits` in the recipe, the assembler, the schema and the gate (the coverage check with its three RED fixtures). The article's own picture taken by Blender's loader and the rig's job. The teeth set made, the Blender library regenerated, and the rig run (Storm and Blender). **Click 2.** |
| **18.3 — Pictured on its part** | The thumbnail tool binds the article's picture, with a `Teeth` family on `mouth`. The fitted eye made. The sheet. **Click 3.** |
| **18.4 — Out to contributors** | `fits` in the dev catalog and the site file. The kits as snapshot assets. `CONTRIBUTING.md`'s Character path. The next dev snapshot built, and published at the lead's word. The ledger rows written and the live sessions told. **Click 4.** |

**Reconciled against §In now:** every row names its step, and the docs are *at the close*.

**Split signal, not cut:** none. One journey (contribute a fitted part) on one rule. The eye is one article on 18.2's machinery. Skin would be a second journey with its own owed work, hence Q-P18-2.

### Compact build map

- **The registry:** `tools/converters/groups.py` gains the part meshes (id, family, source path in the pack, UV-layout hash, the rig parts, the map size) and the species → part → mesh map.
- **The kit:** a new tool beside `tools/converters/fit/gen_fit_makehuman.py`, reusing `build_character`'s pinned fetch and part split. It writes `library/kits/<mesh version>/` (git-ignored) and the committed UV-island picture next to the mesh's record. *Where that picture lives is execute's call: next to the fit set, or under `library/provenance/`.*
- **Changed:**
  - `tools/converters/recipe.schema.json` and `tools/validators/validate_recipe.py`: `fits`, the article's picture, and the coverage check;
  - `tools/converters/assemble_mtlx.py`: `base_color_map`'s value from the recipe, and `fits` into `imrsv_metadata`;
  - `blender/masters/load_article.py`: it takes the article's own picture when none is supplied;
  - `tools/parity/job.py` `maps_for`: it falls back to the article's own picture, so the Storm, Blender and Unreal drivers stay unchanged;
  - `tools/thumbnails/showcase.py` `CHARACTER_FAMILIES`: `Teeth` → Teeth and Gums, on `mouth`;
  - `tools/converters/working_tree.py`, `tools/releases/serve_to_stage.py` and `tools/releases/build_snapshot.py`: `fits`, and the kits as snapshot assets;
  - `CONTRIBUTING.md`.
- **New content:**
  - the teeth set's recipe, picture and provenance;
  - the eye's recipe and provenance.
  - The pictures go under `MatterLibrary/textures/fit/makehuman/<mesh>/`, where pictures on a layout already live. The Glossary's *Fit set* wording follows RD-P18-9.
- **Seams to watch:**
  - **Blender B1:** a material naming a UV map the kit's mesh lacks draws one texel.
  - **B10 and B11:** the lead's Blender.
  - **B12:** the library `.blend` is compressed.
  - **Storm S9:** only `st` is read.
  - **MaterialX M4:** on Subsurface, the scatter follows the picture only if connected. Check the teeth's and the eye's masters.
  - **The teeth mesh's two parts** take one picture through two bindings.

---

## The two lead calls — answered 2026-10-15

**The lead, verbatim: *"A on both, then /execute P18"*.**
- **RD-P18-9 — Q-P18-1 → A: a contributed fitted picture lives inside its Character article** (its `base_color_map` value, with `fits`). This supersedes, for the Character group only, CM2's *"fit beside it"* and LCDSchema's *"empty in the article"*. The fit set and CM2 stand for everything else.
- **RD-P18-10 — Q-P18-2 → A: *Skin Maps* is its own phase, straight after this one**, built on this phase's registry, kit, rule, check and picture binding.

*The questions as they were put, kept for the record:*

### Q-P18-1 — Where does a contributed fitted picture live? **Two of your rulings meet here.**

**What each says:**
- **CM2 (you, 2026-09-27):** *"The split: substance in Matter, fit beside it."* The hm08-bound layer is a **fit set**, *"outside the taxonomy"*.
- **LCDSchema** builds on CM2: a fitted picture *"belongs to the mesh, never to the article"*, the article's value is *"empty"*, and the consumer supplies it at binding. The eyes and hair work this way today.
- **RD-DS-1 (you, 2026-10-14):** *"the comples maps that are moving to for the characters need to be in chracters"*.
- **RD-DS-4:** a contributed set of teeth *"should keep their name"*.
- **RD-DS-3:** the facts go *"in MTLX"*, with no sidecars.

| | Where the picture lives | What it gives | What it costs |
|---|---|---|---|
| **A (recommended)** | **Inside its Character article.** The article names the picture as its `base_color_map` value and declares `fits`. A binding can still supply its own (Carrier rule). | The picture is an entry. It has a name, its contributor and licence in the `.mtlx` (Phase16), a catalog row, a Blender asset, a thumbnail, and a place in a release, because staging copies what an article names. That also fixes F-DS-2 for every new picture. No new carrier is needed. | It reverses CM2's *"fit beside it"* for the Character group, and LCDSchema's *"empty in the article"* (an additive change). **Stage must read the article's own picture** when the binding supplies none: a new ledger ask. |
| **B** | **In the fit set, beside a generic article,** supplied at binding as today. The contributor is recorded with the picture. | CM2 and LCDSchema hold. Consumers bind as they do for the eyes. | The picture is not an entry: no catalog row, asset or thumbnail of its own. Its contributor needs a new carrier, which is either a record (a sidecar, against RD-DS-3) or a PNG text field that nothing reads today. A release still would not carry it (F-DS-2). 18.2–18.4 grow by that carrier. |

**Why A:** only A meets RD-DS-1, RD-DS-3 and RD-DS-4 together with machinery that already exists. CM2 was ruled inside Matter, before Character was its own library. Its reason, *"matter only, never assemblies"* (D1), is Matter's rule. A Character material is fitted by definition.

### Q-P18-2 — Does *Skin Maps* run inside this phase, or after it?

The seed made this your call: *"Whether they run inside this phase or ahead of it is the lead's call when it is opened."*

| | What it gives | What it costs |
|---|---|---|
| **A (recommended): its own phase, straight after this one** | This phase stays one journey with four clicks. *Skin Maps* starts on this phase's mesh registry, kit, rule, check and picture binding, and answers the Outcome's *"a skin"*. Its draft spec's Q-SKM-4 is answered here. | The Outcome's skin half closes in the next phase, not this one. |
| **B: folded in, as steps 18.5 onward** | One phase closes the whole Outcome. | It adds the six skins' re-assembly, Blender's map-following scatter (F-SKM-23), the calibration (F-SKM-20, F-SKM-25), and a library-made map per tone (RD-SKM-3). That is a second journey and many hours of work. It trips the split trigger (time to first click is fine, but the packet becomes two). |

*Skin Maps Beyond Colour* stays parked either way (RD-DS-8).

---

## Findings (discovery Pass 1, 2026-10-15)

- **F-P18-1 — Two lead rulings meet on where a fitted picture lives** (Q-P18-1).
  - **The SkinMaps draft spec marks *"a skin map is a fit-set picture … supplied when bound"* as *Ruled (F-SKM-10)*.** F-SKM-10 is a finding, written at 14:40 on 2026-10-14 within CM2's frame. It came about four hours before RD-DS-1 and RD-DS-4.
  - Its label is corrected at the close (RD-P18-9: the lead chose A).
- **F-P18-2 — The fitted-picture mechanism exists in every target; the entry does not.**
  - `base_color_map` (Phase09) is sampled on the mesh's `st` in the articles, the Blender masters and the Unreal masters. The eye's nine pictures and the hairstyles' ride it.
  - What a fitted picture lacks is a name, a contributor, a catalog row and a place in a release (F-DS-2).
- **F-P18-3 — The part meshes exist only inside the rig.**
  - `build_character.py` pins MakeHuman's CC0 pack (`b542127a…`) and `base.obj` by URL and sha256. It splits:
    - the high-poly eye into Sclera, Iris, Pupil and Cornea;
    - `teeth_base` into Teeth and Gums;
    - `tongue01`;
    - hm08 into Body, Lips and Nails.
  - Nothing names a layout or versions it, and no contributor can get a mesh without the rig.
- **F-P18-4 — A mesh version is a UV layout** (measured 2026-10-15). The pack's six teeth meshes (`teeth_base`, `teeth_shape01`–`05`) have 3868 vertices, 4712 UVs and 3560 faces each, an identical UV-and-face hash (`b7e92a3b…`), and the same `teeth.png` (2048², `d0afb578…`). So one teeth picture fits every teeth shape. This is RD-SKM-1's reading, measured on a second part.
- **F-P18-5 — Studio's character wears the same part meshes.** The platform builds it from the same pinned CC0 pack, with the same high-poly eye, `teeth_base` and `tongue01`. This was read read-only at the platform's `origin/main`, 2026-10-15; nothing private is copied here. So a set that fits the library's teeth mesh fits Studio's.
- **F-P18-6 — The teeth mesh holds two substances.** The rig and Studio split `teeth_base` into Teeth and Gums. A fitted teeth set covers both, as `Eye_Natural` is bound on three eye parts. Its row is Teeth.
- **F-P18-7 — An article naming its own picture is additive, and three readers need one change each** (code read 2026-10-15).
  - **The assembler** writes `base_color_map` with an empty value. A recipe-named value changes only that article.
  - **Storm** reads the value natively.
  - **Blender's loader** (`load_article.py`) and **the rig's job** (`job.py` `maps_for`) take a picture only from the binding.
  - **Stage** skips an empty file and reads the Material's input (P21). It is asked through the ledger.
  - **The Unreal runtime** takes each texture from the job's spec (`MatterRuntimeGameMode.cpp` reads each spec's `file`), so the rig's fallback should reach it unchanged. *Not run here: it is checked on the machine with Unreal.*
  - **The thumbnail record** already hashes every texture the article names.
- **F-P18-8 — `CONTRIBUTING.md` has no Character path.** Its *"Place it"* step puts every article under `materials/<domain>/<class>/`. This is drift since Phase15, conformed at 18.4.
- **F-P18-9 — Scale Grids (Phase19) waits on this phase.** Its re-verify note (2026-10-14) names the fitted skin, eyes and teeth, *"perhaps with no tile size"*. RD-P18-8 is the rule it re-verifies against.
- **F-P18-10 — Gates and machine, measured 2026-10-15.**
  - The library machine: an RTX 2080 Max-Q with 8 GB, Blender 5.2.2, and no Unreal at `UE`.
  - `run_all.py`: 15 PASS, 2 SKIP, 0 FAIL.
  - No lane globs `textures/fit/`. The lanes walk the materials, the recipes, the fixtures and the releases.
- **F-P18-11 — The consumers, swept read-only** (`LOCAL_DELTAS.md` §Separation; fetched 2026-10-15). There is nothing addressed to the library about part meshes or Character contributions:
  - the platform's docs and Stage at `origin/main`;
  - the website's repo, whose last library-facing pass is about Phase17's thumbnails;
  - USDLiveView, whose last pass is the sky ask, closed.

  The website already builds Character's rows from `groups[].rows`, so a new teeth set shows in its row with no change on its side.

## Discovery Log

- **2026-10-15 — Pass 1: the Brief.**
  - **Tree:** `main` at `8ba44e9`, one unpushed commit (a retro). Six Refiner-lane files are modified by a sibling session (`.ai/`, `.claude/`, `AGENTS.md`, the refinement backlog); not touched.
  - **Read:**
    - the seed;
    - `_Architecture`, Taxonomy, Identity, LCDSchema (§Cut-out map, §Base colour map), `Authoring/SkinMaps.md` (draft);
    - the Glossary (*Approved human mesh*, *Fit set*, *Group*, *Character material*);
    - `261014_R_DownstreamPicture.md` (RD-DS-1 to -8, F-DS-13);
    - `261014_R_SkinMaps.md` §Resolved and Status;
    - `260929_R_CharacterMaps.md` §Resolved and Passes 2–8;
    - `260927_R_CharacterMaterials_MPFB2.md` (CM2, D1);
    - Phase15, Phase16 and Phase17 (Brief, log, close);
    - the two skin seeds and the Roadmap's `## Future`;
    - PlatformDependencies P15, P17, P18, P21, P27, M11 and M12;
    - `CONTRIBUTING.md`;
    - the code: `build_character.py`, `gen_fit_makehuman.py`, `assemble_mtlx.py`, `load_article.py`, `job.py`, `showcase.py`, `groups.py`, `run_all.py`'s globs, and the Unreal runtime's texture spec.
  - **Learnings in play:** Blender B1, B2, B10, B11, B12; Storm S9; MaterialX M4. GitHub G1 applies at the publish. Unreal is not run here.
  - **Measured:** the gate baseline, the machine, and the teeth meshes' layouts (F-P18-4).
  - **Rulings newer than the Roadmap:** none about this phase since RD-DS-8. `git log` since the seed's last edit holds only Phase16–17's work and retros.

## Execution Log

**Tree at start (2026-10-15):** `main` at `48b5fad`, the library machine; two commits unpushed (a retro and this phase's discovery). Six Refiner-lane files are modified by a sibling session; not touched. **Gate:** `run_all.py` 15 PASS, 2 SKIP, 0 FAIL (measured at discovery, same tree).

| Step | Landed | Result | Next |
|---|---|---|---|
| **18.1** | the 18.1 commit | `groups.PART_MESHES`: four part meshes, each pinned by its layout hash (`make_kits.layout_sha256`). `teeth_shape03`'s hash equals `teeth_base`'s, and the low-poly eye's differs, so the hash tells layouts apart and ignores shape. `make_kits.py` writes the four kits to `library/kits/` (USD, OBJ, the layout picture, the island picture, README) and commits the island pictures to `library/meshes/` (9–75 KB). `kit_blender.py` builds a kit's `.blend` headless from the factory scene and opens the UV Editing view. Seen before the sitting: the first view drew an orange sheet over everything (all selected), then dropped the layout picture (no user at save); both fixed. **▶ SCAFFOLD COMPLETE — sitting owed (click 1).** | click 1 |
