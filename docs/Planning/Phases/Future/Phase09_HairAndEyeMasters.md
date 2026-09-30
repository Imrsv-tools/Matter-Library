# Phase09 — Hair and Eye Masters

**Status:** IN EXECUTION (2026-09-30, `/execute 9`). Discovery complete (2026-09-29, Passes 1–2; re-checked against
Phase06's execution 2026-09-30, Pass 3). Lane: `build` (verified, §Risk lane). No `YOUR CALL` is open (§Discovery Status: 9.3 kept,
lead 2026-09-29). **Runs on two machines:** 9.1–9.2 on this one (the library machine), with Unreal's column rendered here
from the pinned package; 9.3's master building on the UE machine in Phase06's `unreal/` project (Phase06 D13; Phase06
closed 2026-09-30).
- **Seeded** 2026-09-29 from `docs/Planning/Research/260929_R_CharacterMaps.md` (rulings MAP-RD1–RD6), on the lead's word
  *"yes 1, seed the phase"*; **numbered Phase09** the same day (*"yes push it, make it Phase09"*); discovery opened by the
  lead's `/discovery P9` the same day.

## Outcome

**A Creator's character has hair that keeps its strands and takes any colour on any hairstyle, and eyes that look real —
a photographed iris in the colour they pick, wet, and in Studio shaded by Unreal's own eye model — the same in Blender, a
USD viewer and Studio.**

Concretely, at close:
- **one new input, `base_color_map`**: a picture the library holds in a mesh family's own layout, supplied when an article
  is bound, sampled on the mesh's `st` outside `place2d`, and **multiplied into the article's base colour** (RD-P09-1);
- **the library's fit set for MakeHuman**: each CC0 hairstyle's strand picture (normalised) and cut-out, the brows' and
  lashes', and the nine eye pictures, with provenance, prepared by one library tool (RD-P09-2, RD-P09-6);
- **`Hair_Natural` reads its hairstyle's picture**: any colour on every style, strands kept, brows and lashes following;
- **`Eye_Natural`**, one article for the whole eyeball, bound on the sclera, iris and pupil, with coat (RD-P09-3);
- **the `Eye` master** (the 9th token) with its settings row, and its Unreal side built on Substrate's eye BSDF in
  Phase06's project (RD-P09-7);
- every new or changed article a `candidate`, seen in the rig (Storm, Blender and Unreal: Phase06's column, rendered on
  this machine from the pinned package), in Blender's Asset Browser, and handed to Studio (`PlatformDependencies.md`).

---

## The Brief

### First human test

No running service. The lead judges in Blender, on the rig's sheets, and (9.3) on the Unreal column; Studio is the
platform's check. The agent runs every command and builds every scene.

1. **Blender, the character with Studio's built-in hair (`short02`)** at three tints — blonde, auburn, black — then
   `bob01`. **Expect:** each reads as that hair colour, with its strands and gaps; the brows and lashes take the tint
   too. *(9.1)*
2. **The rig's character sheet** (Storm | Blender | Unreal), wide and face views. **Expect:** the hair shows its strands in
   all three columns, not a flat colour; nothing magenta. *(9.1; Unreal's column from the pinned `unreal-runtime-v1`,
   F-P09-14)*
3. **Blender, face close-ups, a brown eye and a blue eye.** **Expect:** a photographed iris with its dark ring and the
   veins in the white, a wet highlight, and no stepped edge where the white meets the iris. *(9.2)*
4. **The rig's face view** (Storm | Blender | Unreal). **Expect:** the same eye in Storm and Blender; no cornea shell over
   it (Studio has none). Unreal's eye is advisory here: on its Subsurface master the picture shows at `1 − subsurface_weight`
   of its strength until 9.3 (F-P09-14). *(9.2)*
5. **The Unreal column, the face view on the `Eye` master** beside Storm and Blender, **rendered on this machine from
   `unreal-runtime-v2`** (built on the UE machine, F-P09-17). **Expect:** the eye reads as an eye, at least as well as the
   other two columns; the hair's picture shows in Unreal through the master's own input. *(9.3)*
6. **Studio** (the platform's check, handed over at the close): eye colour is chosen by picture; hair keeps its strands at
   any tint.

**Reconciled with the steps:** clicks 1–2 are 9.1's (click 2's Unreal column needs 9.1's driver bridge, F-P09-14); clicks
3–4 are 9.2's (the input exists from 9.1; the eye parts' atlas `st` in both copies of the rule, F-P09-15); click 5 is 9.3's
and needs its masters built and published as `v2`; click 6 is the close's hand-off. The tint is judged in Blender, because the rig's
character job takes defaults only (F-P08-4).

### In now

- **The input, `base_color_map`** (RD-P09-1): `LCDSchema.md` (a section beside §Cut-out map; §Author tier), the assembler,
  the recipe schema, the validator, the Blender masters and loader, the rig's job; `MasterSet.md` (the modulator rule says
  this input is not an overlay or maskset); the Glossary (`base_color_map`, **fit set**).
- **The fit set for MakeHuman** (RD-P09-2): one tool reads the pinned CC0 pack and writes the normalised strand pictures and
  cut-outs of the 10 hairstyles, the brows and lashes, and the nine eye pictures, with provenance.
- **Hair:** `Hair_Natural` re-authored in place to read the picture (`v01`, unreleased); MasterSet's Hair row corrected
  (RD-P09-5).
- **Eyes:** `Eye_Natural` (RD-P09-3), on Subsurface until 9.3, with coat; its subsurface colour follows the picture
  (F-P09-5).
- **The rig matches Studio** (RD-P09-4): hair `short02`; the eye parts on their atlas `st`; the cornea unbound.
- **Unreal's column kept alive on this machine through 9.1–9.2** (F-P09-14): the Unreal driver carries a binding's
  `base_color_map` onto the pinned `v1` masters, where that is exact, and refuses it otherwise.
- **The `Eye` master** (RD-P09-7): the token through every tool that lists tokens, the settings row, `Eye_Natural` moved
  onto it; its Unreal side in Phase06's `unreal/` project.
- **The Unreal masters take `base_color_map` as their own input** (F-P09-16): on every master whose author tier gains it
  (Opaque, Masked, Hair, Subsurface), sampled on the mesh's `st` outside `place2d`; the Subsurface master's colour follows
  the picture (F-P09-5, Unreal side). The driver's bridge retires. **Published as `unreal-runtime-v2`** and pinned (F-P09-17).
- **Hand-offs:** `PlatformDependencies.md` — Studio renames `strand_color_map` to `base_color_map` and **multiplies**
  instead of replacing; binds `Eye_Natural` on the eye parts and offers eye colour as a picture choice; takes the
  library's `Eye` master and the masters' new input from `build_masters.py` (P20), uploading the picture as **linear**
  (P20's LinearColor rule: the library decodes sRGB on the CPU). Matter-Library#3 answered. `Experience_MatterLibrary.md`
  §Shipped.

### Not now

- **Strands** (MAP-RD4): their own phase (Roadmap *Hair That Reads as Hair*).
- **New eye geometry** — a cornea shell, lid shadow, tear line (MAP-RD6: *"adding mesh is not the time"*).
- **Skin pictures** (MAP-RD2): skin stays general.
- **A Blender control for supplying a picture** by hand (as for the cut-out: Phase07's deferral, *planned*). Dropped from
  the Asset Browser onto any mesh, `Eye_Natural` is a plain eye colour and the hair its light colour, never magenta.
- **Retiring** `Iris_Brown`, `Sclera_Natural`, `Pupil_Dark`, `Cornea_Clear` or `Hair_DarkBrown`: they stay (Don't Delete).
- **A release** (L4, *"no versioning"* before the first release).

### Reuse check: what the stack already gives us

| Need | What exists | Evidence (2026-09-29) |
|---|---|---|
| A picture supplied at binding, sampled on the mesh's `st` | `cutout_map`: a lane-B `filename` input, the Carrier rule, `default = 1` when empty, sampled outside `place2d`, one Material instance per binding | `LCDSchema.md` §Cut-out map; Learnings S9; the eleven `cutout_map` sites (Pass 1) |
| The picture into the colour | the article's `base_color_tinted` multiply (`base_color_const × base_color_tint`): one more factor | the assembled articles |
| Subsurface detail surviving | the Hair graph connects `subsurface_color` to `base_color_out` | `LCDSchema.md` §Author tier, Hair row |
| A part keeping its atlas `st` in the rig | `build_character.py`'s `cutout: True` parts | read |
| The rig supplying a per-part map | `job.py` and `blender_render.py` supply `cutout_map` per part | read |
| Preparing CC0 textures with provenance | `gen_fabrics.py` + a provenance YAML per set; the pinned pack in `library/parity/_sources/` | read |
| A new master token | Phase08's `Hair` path through eight sites (F-P08-2) | `Phase08_CharacterAppearance.md` |
| Unreal's eye | Substrate's Eye BSDF: one surface with `IrisMask`, `IrisDistance`, cornea and iris normals, a subsurface profile | Phase06 F-P06-9 (read from the engine header, not rendered) |
| An Unreal project and column to build and judge on | Phase06's `unreal/` project and rig column; the column renders on this machine from the pinned package | Phase06 D13; closed 2026-09-30, clicks 2 + 6 passed here |
| A picture multiplied into the base on Unreal's side, before 9.3 | every Unreal master's `base_color × base_color_tex × base_color_tint` (`build_masters.py` `layer()`) | read 2026-09-30 (F-P09-14) |
| Shipping a master change to this machine | `unreal/build.sh package`, `unreal/publish.sh N`, the pin | Phase06 D2, D14; `ToolingConventions.md` |

**No custom layer is proposed:** the input is the cut-out's mechanism with a second role; the fit set is a folder of
textures; the Eye master is the master mechanism the spec already has.

### Decisions that bind

- **Standing:** MAP-RD1–RD6 (`260929_R_CharacterMaps.md` §Resolved) · D1 / CM2 (*"mesh-bound pictures are never in an
  article"*) · L1 (one part per substance) · L2 (the mesh's cut-out, supplied at binding) · RD-P08-5 (author light) · C4 /
  C5 (six tokens; `Natural` = the untinted look) · Decision of record 1 (articles are `open_pbr_surface`) · the LCD
  restatement (2026-09-28: each master leans on its engine's best features) · Phase06 D12 (Hair matte on cards) and D13
  (Phase09 builds the eye and the picture, their Unreal side included, in Phase06's project) · *"no versioning"* before
  the first release.
- **RD-P09-1 — The input is `base_color_map`**, and `base = base_color_const × base_color_map × base_color_tint`. Named by
  `LCDSchema.md` §Notes (*"Names use OpenPBR-aligned terms"*); the platform's `strand_color_map` was provisional until the
  library ruled (HS-Q6). An `image` with `default = 1`, `srgb_texture`, on texcoord 0, not through `place2d`, so the
  Creator's UV nudges never move it. It is not packed data, so the modulator rule does not apply to it (F-P09-4).
- **RD-P09-2 — The fit set lives at `MatterLibrary/textures/fit/<family>/`** — `fit/makehuman/hair/`, `…/eyes/` — a third
  root beside `base/` and `shared/`. Files follow the texture grammar with a role token the compression lane knows
  (`basecolor`, `opacity`) and scale tag `sUKN` (a picture drawn on a layout has no real-world size), each set with a
  provenance YAML. Answers CM-Q6 for pictures (MAP-RD1: *"the libery has all the assets anyone needs"*).
- **RD-P09-3 — One eye article, `Eye_Natural_Clean_Base_s001_v01`, bound on all three eye parts.** The picture draws the
  sclera, iris and pupil; the parts share the eye's layout (MAP-F11); Unreal's eye BSDF shades one eyeball surface with an
  iris mask (F-P06-9). The eye colour is the picture the binding supplies (F-P09-3), so there is no per-colour article. It
  sits on **Subsurface** until the `Eye` token exists (9.3). The three Phase07 eye articles stay.
- **RD-P09-4 — The rig's character matches Studio's:** hair `short02` (Studio's built-in; the rig's `bob02` is the one blonde
  style, F-P09-7); the eye parts keep their atlas `st`; the cornea part is left unbound (Studio dropped it, MAP-F12). The
  `Cornea_Clear` article and the cornea split stay.
- **RD-P09-5 — The Hair row, corrected:** the Unreal realisation is **matte, default lit**, coloured by the picture (Phase06
  D12; the lead at the platform's sitting); the hair shading model is kept for strands. The article's own graph keeps its
  soft coverage and thin-walled translucency. **Whether its specular stays** in Blender and Storm, now that the picture
  carries painted highlights, is judged at click 1 — the lead's *"too glossy"* is the standing verdict on the old hair.
- **RD-P09-6 — The library prepares the cut-outs too** (MAP-RD1): the fit set carries each hairstyle's cut-out beside its
  strand picture, so Studio can stop writing its own. The rig reads them from the fit set.
- **RD-P09-7 — The `Eye` master opens with a disposable spike** (9.3): does Substrate's eye BSDF, fed our picture and an
  iris mask from the fit set, shade MakeHuman's eyeball well, with no new geometry? Epic warns the model *"produces very
  strong dependencies between the shader code, the Material, the shape of the geometry, and its UV layout"* (F-P09-8).
  **If it does not, the token is not added and the finding goes to the lead** (the Unreal eye then stays on Subsurface).
  Settings row: coverage opaque, shading model **eye**, one-sided, the refraction offset built in the graph (F-P06-9).
  **The spike judges one real-time capture in the rig, not the editor viewport** (F-P09-18).
- **RD-P09-8 — One package publish, at 9.3's end** (`unreal-runtime-v2`, pinned), after its masters are built: Phase06
  D14's ruling applied to this phase's master change (lead: *"yes and 6.2 and close (not every master change)"*). Publishing
  is public and the lead's to call; the UE machine's traffic control holds (Phase06 D1: *"please check with me before running
  anything"*).
- **Bars:** as Phase08 — the Hair master judged like Lace (whole set advisory, close-up graded); the eye as Subsurface,
  "recognisable". Cross-tool agreement is read on the "Moved" nod (LCD restatement); picture ΔE is a diagnostic.

### Risk lane: `build` (verified)

The controls, read 2026-09-29:
- **The release lifecycle** (`library/releases/`, freeze, promote) is untouched; no release is cut. Release staging selects
  textures by a release's lock, not by folder (`source_provenance.py` `release_textures`), so new textures cannot break a
  frozen release.
- **`run_all.py` lanes that enumerate what this phase adds:** `compression` compresses **every PNG under
  `MatterLibrary/textures/`** and fails any it cannot classify by a role token (`compress_textures.py` `classify`) — so the
  fit files carry `basecolor` / `opacity`; `materials` validates every `.mtlx` by its master (it learns `base_color_map`,
  then `Eye`); `determinism` re-assembles every recipe (`Hair_Natural` changes by its recipe; every other article must stay
  byte-stable); `grammar` exercises the validator's fixtures.
- **`tools/conformance/codec_ab.py`** lists the graded classes: if 9.3 adds `Eye` there, **`check_exporter.sh` is baselined
  first** (LOCAL_DELTAS, the RUN row). `check_asset_library.sh` runs after each Blender library rebuild.
- **The contract edits are additive:** a new author-tier input (as `cutout_map` was) and a new token (semver-minor,
  `MasterSet.md` §Master tokens); `Hair_Natural` and the new articles are unreleased candidates.
- **Repository size is not a concern for the fit set** (lead, 2026-09-29, verbatim: *"not so worries about imagea in our
  library as that is pretty static... it was the 600 megs for each build of this standalone tool... that has no value once
  anew one is added"*). The fit set is Git LFS like every library texture; Phase06's concern was a package rebuilt per
  version.
- **One account-side act: 9.3 publishes `unreal-runtime-v2`**, a public GitHub pre-release on this repo, by Phase06's
  `publish.sh` (RD-P09-8). Release assets carry no storage or bandwidth charge (Phase06 §Risk lane). Creating it needs `gh`
  with write access on the UE machine.
- No authorization, secrets, destructive migration or public edge. **The push is the lead's, and it is irreversible.**

### Step list

- **9.1 — Any hair colour on any hairstyle, strands kept.**
  - The input through the contract and the tools (RD-P09-1); the Glossary.
  - The fit-set tool and the MakeHuman hair set: 10 styles' strand pictures and cut-outs, brows and lashes (RD-P09-2,
    RD-P09-6).
  - `Hair_Natural` reads the picture; the Hair row corrected (RD-P09-5).
  - The rig on `short02`, its hair parts fed from the fit set (RD-P09-4); Blender library rebuilt.
  - The Unreal driver's bridge: a binding's `base_color_map` onto `v1`'s `base_color_tex`, asserted exact, else refused
    (F-P09-14).
  - **First clickable result:** clicks 1–2.
- **9.2 — Eyes that look real, in Blender and a USD viewer.**
  - The nine eye pictures in the fit set.
  - `Eye_Natural` on Subsurface with coat, its subsurface colour following the picture (RD-P09-3, F-P09-5).
  - The rig's eye parts on their atlas `st`, bound to `Eye_Natural` with a picture, the cornea unbound (RD-P09-4), in both
    copies of the atlas rule, `job.py` and `drivers/unreal.py` (F-P09-15); Blender library rebuilt.
  - **First clickable result:** clicks 3–4.
- **9.3 — The `Eye` master, and both pictures in Unreal (masters built on the UE machine; judged here).**
  - The spike (RD-P09-7, F-P09-18). If it holds: the `Eye` token through every tool that lists tokens and its settings row;
    `Eye_Natural` onto it; its Unreal master in `unreal/` on Substrate's eye BSDF, with the iris mask from the fit set.
  - The Unreal masters take `base_color_map` as their own input (Opaque, Masked, Hair, Subsurface), the Subsurface colour
    following it; the driver's bridge retires (F-P09-16).
  - `build.sh package`, then `publish.sh 2` and the pin (RD-P09-8).
  - **First clickable result:** click 5, on this machine from the pinned `v2`.
- **Close.** `PlatformDependencies.md` (the asks in §In now), Matter-Library#3 answered, `Experience_MatterLibrary.md`
  §Shipped, the research thread's Status, Studio's check (click 6) handed over.

**Why this order:** 9.1 carries the one contract change and proves it on the part Studio already shows (hair); 9.2 reuses
it with no new contract; 9.3 changes Unreal masters, which only the UE machine can build, so it goes last, and one publish
carries all of them here.

**Split signal (raised, not cut):** hair (9.1–9.2's input) and the Unreal eye (9.3) are separately demonstrable, and 9.3
runs on another machine behind another phase. **They stay one phase** (lead, 2026-09-29: *"keep 9.3"*): 9.3's Eye master is
the Outcome's *"in Studio shaded by Unreal's own eye model"*.

### Compact build map

- **Contract:** `docs/specs/Contract/LCDSchema.md` (§Base colour map beside §Cut-out map; §Author tier rows for Masked,
  Hair, Subsurface, Opaque) · `docs/specs/Ontology/MasterSet.md` (the modulator note; the Hair row and settings row; 9.3: the
  `Eye` row, token, settings row, coverage line, History) · `docs/specs/_Architecture.md` §Textures (the `fit/` root) ·
  `docs/Glossary.md` · `docs/NamingConventions.md` (the fit-set filename form, if it needs a line).
- **Tools:** `tools/converters/assemble_mtlx.py` (`AUTHOR_TIER_PORTS`; the base multiply; Subsurface's colour; 9.3
  `KNOWN_MASTERS`) · `tools/converters/recipe.schema.json` · `tools/validators/validate_material.py` · `blender/masters/
  build_masters.py` (the per-object image, as for the cut-out; `VERSION` bump) and `load_article.py` · a new
  `tools/converters/fit/` tool writing `MatterLibrary/textures/fit/makehuman/…` and provenance under
  `library/provenance/sources/fit/…` · 9.3: `rig.py` (`GRADED`, `ADVISORY_VIEWS`), `codec_ab.py` (`TIGHT_CLASSES`,
  baseline first), `JOB_FORMAT.md`.
- **Rig:** `tools/parity/scene/build_character.py` (`MESHES`: hair `short02`; the eye parts keep atlas `st`; rebuild the
  scene) · `tools/parity/job.py` and `drivers/blender_render.py` (supply `base_color_map` per part, as `cutout_map`) ·
  `rig.py` `CHARACTER_CAST` (`Eye_Natural` on the three eye parts; no cornea binding).
- **Articles:** `tools/converters/recipes/Hair_Natural_…json` (re-authored), `Eye_Natural_Clean_Base_s001_v01.json` (new)
  → `MatterLibrary/materials/biological/{keratin,tissue}/`.
- **Unreal driver (9.1–9.2, this machine):** `tools/parity/drivers/unreal.py` — `article_material` (the `base_color_map`
  bridge onto `base_color_tex`, asserting no base texture and default placement; retired at 9.3) and the character's
  per-part `st` scale (~`CHARACTER + name in cutouts`: the eye parts keep their atlas too).
- **Unreal (9.3, UE machine):** Phase06's `unreal/` project: `Scripts/build_masters.py` (`MASTERS` gains `Eye`;
  `build_master`'s `layer()` gains `base_color_map_tex` on the mesh's own `st`, as `cutout_tex` is sampled; the Subsurface
  colour follows the modulated base); `drivers/unreal.py` `BUILT_MASTERS`; then `build.sh package` and `publish.sh 2`.
- **Tests:** existing only (`run_all.py`, `check_asset_library.sh`, `check_exporter.sh`) plus the rig's sheets and the
  lead's Blender scenes. No new gate.

---

## Discovery Log

### Pass 1 (2026-09-29): the product docs, top-down, read against the Outcome

**Examined:** `_Architecture.md` (the LCD restatement of 2026-09-28, Decisions of record) · `MasterSet.md` (tokens, the Hair
row, the settings table, the modulator rule) · `LCDSchema.md` (§Author tier, §Carrier rule, §Cut-out map, §Notes) ·
`NamingConventions.md` · the research thread (`260929_R_CharacterMaps.md` whole; HS; HairAndNail; CM) · Phase07 and Phase08
(decisions that bind, deferral ledgers) · `260929_R_UnrealTestRuntimeHere.md` and its spike. **Learnings:** Storm S9,
Blender B1, B5, MaterialX M4 apply. **Tree:** every `cutout_map` site (the precedent: `assemble_mtlx.py`,
`recipe.schema.json`, `validate_material.py`, `load_article.py`, `job.py`, `JOB_FORMAT.md`, `blender_render.py`,
`build_character.py`, the two hair recipes, three specs and the Glossary); the gates that enumerate `MatterLibrary/textures/`;
the rig's cast. **Tree grep for the phase's own names** (`base_color_map`, `strand_color_map`, `"Eye"`, `ML_Eye`): **nothing
built.** **External:** Epic, *Shading Models* (5.8). **This machine has no Unreal** (no engine, no probe folder); the UE
machine is the other one (UR-D1).

**Findings:**
- **F-P09-1 — The spec already expects this phase.** `_Architecture.md` lists Phase07's D-E (*"no `Eye` master"*) under
  **Reevaluate**, argued on the superseded LCD wording; the restated principle (*"we use the master materails to lean in on
  the egines BEST qaulities"*) is what MAP-RD6 applies. MasterSet's Hair row calls itself **interim** until *"mesh-supplied
  card maps"*.
- **F-P09-2 — MasterSet's Hair settings row is stale.** It says the shading model is *"hair (… Unreal's Scatter /
  Backlit)"*. The platform's sitting overturned that on the lead's eye (*"turn off anything specular, gloss, reflection,
  glow, highlight"*, then *"OK! That is HAIR!"*): matte, default lit, coloured by the picture. HS-Q3 is therefore answered;
  the row is corrected with the input, the hair shading model kept for strands.
- **F-P09-3 — Where the eye picture lives is answered: in the library, supplied at binding, never inside the article.**
  Phase08's binding list: *"CM2 / D1 (substance only; mesh-bound pictures are never in an article)"*; MAP-RD1: *"the libery
  has all the assets anyone needs"*. So the eye articles stay general (a sclera, an iris, a pupil) and **the eye colour is
  which picture the binding supplies** — the same as a hairstyle's picture. The lead's *"seperate pictures"* is nine pictures
  in the library, from two photographs (MAP-F9).
- **F-P09-4 — The one input, named by the spec's own rule.** `LCDSchema.md` §Notes: *"Names use OpenPBR-aligned terms"*.
  The input multiplies OpenPBR's `base_color`, so **`base_color_map`**: `base = base_color_const × base_color_map ×
  base_color_tint`, sampled on the mesh's `st` outside `place2d`, an empty map reading 1. The platform's
  `strand_color_map` was provisional until the library rules (HS-Q6), so the platform renames it. It is not an overlay or
  a maskset (packed data), so the modulator rule is untouched; the phase says so where the rule is stated.
- **F-P09-5 — On a Subsurface article the picture vanishes unless the subsurface colour follows it.** MaterialX M4: base
  detail keeps only `1 − subsurface_weight` of its strength; `Sclera_Natural` is at weight 1.0. So `subsurface_color` is
  connected to the modulated base, as the Hair graph already does.
- **F-P09-6 — The pictures need a home in the texture tree, and the gate reads every file there.** `_Architecture.md`
  §Textures names two roots, `base/` (by matter) and `shared/` (layers); a picture drawn on a mesh family's layout is
  neither. The **compression lane** classifies every PNG under `MatterLibrary/textures/` by a role token in its name
  (`basecolor`, `opacity`, …) or fails. Candidate: a third root `textures/fit/<family>/…` with role-token names and scale
  tag `sUKN` (the grammar allows it on a base texture, not on a layer). The Glossary uses *fit* under *Cut-out map*; a term
  for the set is fixed there first.
- **F-P09-7 — The rig cannot show the defect this phase fixes, as it stands.**
  - Its hair is **`bob02`, the one blonde style** (MAP-F2): the dark-picture tint problem does not appear on it. Studio's
    built-in hair is `short02`.
  - Its eye parts' `st` is rescaled to metres; they must keep the source atlas, as its cut-out parts do.
  - It binds a cornea shell that Studio does not have (MAP-F12).
  - Its character job takes defaults only (F-P08-4), so the tint is judged in Blender, as Phase08 did.
- **F-P09-8 — Unreal's eye model is tied to its own eye geometry.** Epic: *"This Shading Model is highly technical and has
  been developed in a way that produces very strong dependencies between the shader code, the Material, the shape of the
  geometry, and its UV layout"*; it recommends the Digital Humans eye geometry and material *"as-is"*. With no new eye mesh
  (MAP-RD6), an `Eye` master on MakeHuman's eyeball is **unproven**, and proving it needs Unreal, which is on the UE machine
  (Phase06's). → Q-P09-1 *(closed in Pass 2: a spike first, RD-P09-7)*.
- **F-P09-9 — Phase06 is being planned on the UE machine** (lead, 2026-09-29). The `Eye` master's Unreal side, and when
  Studio renders with the library's masters (P20), depend on it. The Brief is written after reading that plan.

**Forks tested and closed** (none reached the lead): *where the eye picture lives* → D1 / CM2 + MAP-RD1 (F-P09-3) · *the
input's name* → LCDSchema §Notes + HS-Q6 (F-P09-4) · *the Hair shading model* → the lead's ruling at the platform's sitting
(F-P09-2) · *whether the library holds the cut-outs too* → MAP-RD1 (yes).

### Pass 2 (2026-09-29): the Phase06 plan, read the moment it landed

**Examined:** `Phase06_UnrealTestRuntime.md` at its Brief (Passes 1–2, D12–D14), pulled from the UE machine the same day
(lead: *"the plan is pushed for you to pull"*).

- **F-P09-10 — Where the Unreal side is built is decided:** Phase06 D13, *"The eye and the hair picture belong to Phase09,
  including their Unreal side, built in this phase's `unreal/` project"*. Phase06 builds the eight masters and the column
  Phase09 judges on. So 9.3 runs on the UE machine after Phase06's 6.5. Answers MAP-Q13.
- **F-P09-11 — One eye article is what Unreal's eye wants.** Phase06 F-P06-9, read from the engine header: Substrate's Eye
  BSDF shades **one eyeball surface** with an `IrisMask` and `IrisDistance`; the iris is a masked region, not a material of
  its own. Answers MAP-Q12 (RD-P09-3). It does not settle F-P09-8 (the geometry dependency), which is why 9.3 opens with a
  spike (RD-P09-7).
- **F-P09-12 — The Hair master in Unreal is already matte** (Phase06 D12), and *"the master takes it when Phase09 lands"*:
  the picture input's Unreal side is 9.3's.

**Forks tested and closed:** Q-P09-1 (the Eye master: spike first) → answered by method, not a lead call: MAP-RD6 wants the
master and no new geometry, Phase06 D13 places its build, and an unproven core step gets a disposable spike before it is
built; the one lead call is if the spike fails (RD-P09-7).

### Pass 3 (2026-09-30): Phase06's execution, read against this Brief

**Examined:** `Phase06_UnrealTestRuntime.md` (closed 2026-09-30: its Execution Log and Close row) · `docs/Learnings/Unreal/`
(U1–U10, T1–T2) · `tools/parity/drivers/unreal.py` (`article_material`, the character's per-part `st`) · `tools/parity/rig.py`
`run_unreal` · `unreal/MatterRuntime/Scripts/build_masters.py` (`MASTERS`, `layer()`, the Hair fold) ·
`PlatformDependencies.md` P20. **Nothing in the contract, the fit set or 9.1–9.2's Storm and Blender work changes.** Phase06
changes where Unreal is seen, and what 9.1 would silently break there.

- **F-P09-13 — Unreal's column now renders on this machine.** Phase06's clicks 2 and 6 passed here: the rig downloads the
  pinned `unreal-runtime-v1` and fills the column with no Unreal installed. So every rig sheet in 9.1–9.2 can carry it; only
  **building** a master needs the UE machine. The rig's verdict is now the Moved agreement (Phase06 D9, built), which the
  Bars already assume.
- **F-P09-14 — As planned, 9.1 would blank the character's whole Unreal column.** The driver refuses an article declaring an
  input it does not carry (`article_material`: `unported` → `Unsupported`), and `rig.run_unreal` then skips the column for
  every part. `Hair_Natural` declares `base_color_map` from 9.1, `Eye_Natural` from 9.2. **The pinned `v1` can render it
  exactly, with no rebuild:** every Unreal master computes `base_color × base_color_tex × base_color_tint` (`layer()`), with
  `base_color_tex` on the placed `st`. On the character, placement stays at its defaults (the job takes defaults only,
  F-P08-4), and the hair and eye parts keep their raw atlas `st`, so a binding's map sent as `base_color_tex` is RD-P09-1's
  product, **provided the article has no base texture of its own** (`Hair_Natural` and `Eye_Natural` are constants). The
  driver asserts those conditions and refuses otherwise. **Its limit:** on Unreal's Subsurface master `subsurface_color` is
  its own parameter, so the eye's picture shows at `1 − subsurface_weight` of its strength until 9.3 (F-P09-5, Unreal side);
  click 4's Unreal eye is advisory.
- **F-P09-15 — The "atlas `st`" rule has two copies.** `job.write_character_scene` and `drivers/unreal.py` each keep a part's
  raw `st` only when it has a cut-out map (`build_character.cutout_maps()`). RD-P09-4 gives the eye parts their atlas without
  a cut-out, so both copies change in 9.2, or both read one flag.
- **F-P09-16 — Studio takes the masters from the builder, so the input must be a real slot on the Unreal masters.** P20
  (Phase06 close): Studio runs `build_masters.py` into its own project. F-P09-14's bridge is a rig device that Studio never
  sees, so 9.3 gives `base_color_map` its own input on every master whose author tier gains it (Opaque, Masked, Hair,
  Subsurface), sampled on the mesh's `st` outside `place2d` like `cutout_tex`, with the Subsurface colour following it. P20's
  LinearColor rule binds the picture too: the library decodes sRGB on the CPU, so Studio uploads it linear.
- **F-P09-17 — A master change reaches this machine only through a new package.** This machine renders whatever build the
  pin names (Phase06 D2), today `v1`. 9.3's masters are invisible here until `unreal-runtime-v2` is built, published and pinned. Hence
  RD-P09-8, and click 5 is judged here from `v2`, as Phase06's click 2 was.
- **F-P09-18 — Phase06's Unreal learnings bear on the Eye spike.**
  - **U1:** Epic's OpenPBR function is not the eye; the Eye master wires the article's OpenPBR names (Phase06 D5) onto
    Substrate's Eye BSDF itself.
  - **U3 / T1:** the eye BSDF, its coat and the subsurface profile must fit Substrate's 160-byte budget without flattening;
    read the compiled shader, since nothing warns.
  - **U6:** thin-surface subsurface is dark noise in a single real-time capture. The eye's subsurface profile is the same
    risk class, so the spike judges the rig's one-frame capture, not the editor viewport.
  - **U7:** the warm-up setting precedes every job; a first-setting checker is not a verdict on the master.
  - **Diamond (Phase06 6.4):** screen-space refraction bends nothing in the capture. That does not touch the eye, whose
    refraction is a UV offset built in the graph (F-P06-9).

**Forks tested and closed** (none reached the lead): *keep Unreal's column through 9.1–9.2, or accept "not yet" until 9.3* →
answered by Phase06's run-3 scope (*"after 6.5 and the published package, material-making moves to the other machine with
Unreal's column in its sheets"*): keep it, by the exact bridge (F-P09-14) · *publish once or per master* → Phase06 D14's class
ruling (RD-P09-8) · *the Hair input only, or every master whose tier gains it* → P20 (F-P09-16).

## Discovery Status

- **Passes captured:** 3 (2026-09-29, 2026-09-30). **The Brief is complete**, re-checked against Phase06's execution.
- **Current working direction:** the Brief above.
- **Open decisions:** none. ~~Keep 9.3 in this phase or cut it~~ **ruled (lead, 2026-09-29): *"keep 9.3"*.** The fit set's
  size is not a concern (§Risk lane). *(Q-P09-1 closed in Pass 2.)*
- **Checks to carry forward:** baseline `check_exporter.sh` before touching `tools/conformance/` · the compression lane on
  the fit set · regenerate the Blender library and run `check_asset_library.sh` ·
  rebuild the rig's character scene after `MESHES` changes · the character's Unreal column still renders after 9.1 and 9.2
  (F-P09-14) · on the UE machine, ask the lead before each build or GPU launch (Phase06 D1) · publish `v2` once (RD-P09-8).

## Execution Log

**Run 1 (2026-09-30, the library machine).** The lead drives each click; Blender sittings are built headless and opened in his Blender.

**▶ Resume (end of run 1, 2026-09-30; 9.1 ✅, 9.2 ✅; handed off at ~400k context):**
- **Next: 9.3, and its first job is Unreal's eye** — the lead at click 4: *"UE is TERRIBLE! but you say this is fixed in 9.3"*. The rig's Unreal column draws the eye white (the 9.2 row).
- **9.3 needs the UE machine** (Phase06 D1: ask the lead before each build or GPU launch there). In order: the Eye spike (RD-P09-7; judge the rig's one-frame capture, F-P09-18); the Unreal masters' own `base_color_map` input on Opaque, Masked, Hair and Subsurface, sampled on the mesh's `st` outside `place2d` like `cutout_tex`, **with the Subsurface master's subsurface colour following it** (the white Unreal eye, 9.2 row); retire the driver's `base_color_tex` bridge (`unreal.py` `article_material`); `build.sh package`, `publish.sh 2`, the pin (RD-P09-8). Then click 5 here, from `v2`.
- **Then the close's docs:** `PlatformDependencies.md` (Studio: rename `strand_color_map` → `base_color_map` and multiply; bind `Eye_Natural` on the three eye parts, eye colour as a picture choice; the picture uploaded linear, P20), Matter-Library#3, `Experience_MatterLibrary.md` §Shipped, the research thread's Status. The contract docs (LCDSchema, MasterSet, _Architecture, Glossary, JOB_FORMAT) landed at 9.1.
- **Watch items:** the eye's highlight (click 3); Storm's iris reads redder than Blender's (diagnostic).

| Step | Commit | Result | Next |
|---|---|---|---|
| 9.1 | `dfd89d5` + the matte commit | ✅ **Click 1, the lead (2026-09-30), on four heads in Blender (`short02` untinted blonde, auburn, black; `bob01` untinted):** *"this is looking quite good... in fact the eyelashes and brows also look good. the biggest giveaway right now is eh shine...maybe it is specular...it gives away these are flat sheets"*; then, shown the same heads with the hair's specular off: *"OH! You did it! yes! until we get proper hair... this will need to be the way"*. **RD-P09-5 settled: card hair is matte in every renderer** (`specular_weight = 0`; the field returns to the assembler, which had withdrawn it in Phase08 because no article needed it). **Fit set:** 26 cards; 9 are black paint (95th percentile under 0.004 linear: most brows and every lash card) and are written flat, so they take the article's colour and the tint. **Deviation (small):** the rig's `build_character.py` proxy parser ended a `verts` section at a key line before the first vertex, so `bob01` could not load; fixed. Blender library 56, CONFORMS. | click 2 (the character sheet), then 9.2 |
| 9.1 (click 2) | `e968242` | ✅ **Click 2, the lead (2026-09-30), on the character sheet (Storm / Blender / Unreal, the matte `short02` strands in all three):** *"pass, move on to the eyes"*. **9.1 ✅.** | 9.2 |
| 9.2 | `ca7929f` + the 9.2 commit | ✅ **Click 3, the lead (2026-09-30), in Blender (brown and blue pictures on one `Eye_Natural`, face close-ups, a small key light added for the catchlight):** *"similar to what we had with hair... there is an un natural about of "mirror" going on... Yes eyes are wet and shiney.. but these highlight aboultly reflect and blow out the eyes in an odd way.. thoughts?"* The coat (weight 1, roughness 0.02) was a mirror over the whole eyeball, which has no cornea bulge to confine it; softened to weight 0.5, roughness 0.1, and the sitting's key light shrunk. The lead: *"That helps... I think it will be something to kep an eye on (hahaha pun intended) it might still be too much but will not know until we work with it a bit..."* — **the eye's highlight is a watch item** (the `Eye` master may change it again, 9.3). **Built:** the nine eye pictures; `Eye_Natural`; F-P09-5 (the subsurface colour follows the picture: assembler, Blender loader; Unreal carries the constant until 9.3); F-P09-15 (one atlas rule, `build_character.atlas_parts()`); the cornea unbound and hidden in every view. **CAUGHT (not a gate):** the Storm driver named a view's hide layer `<id><suffix>.usda`, which for the wide view IS the setting scene: the first hide on a wide view overwrote the scene with a layer sublayering itself (now `…__view.usda`). **Unreal's column shows a white eye:** the picture reaches `base_color_tex`, but Unreal's Subsurface diffuse follows `subsurface_color` (cause not isolated); advisory until 9.3. Storm vs Blender, face view: iris 10.4 (Storm redder), pupil 4.7, sclera 3.8. ✅ **Click 4, the lead (2026-09-30), on the rig's face view enlarged (`eyes_3tools.png`):** *"INdeed... UE is TERRIBLE! but you say this is fixed in 9.3... handoff and we can carry on"* — Storm and Blender pass; **Unreal's white eye is carried to 9.3 as its first job.** **9.2 ✅.** | 9.3 on the UE machine |
