# Phase07 — Character Materials

**Status:** IN EXECUTION (`/execute P7`, 2026-09-27). Discovery complete the same day: the Brief is complete and the four lead calls are ruled (§Lead rulings). Lane: `build` (verified, §Risk lane).
- **Seeded** 2026-09-27 from `docs/Planning/Research/260927_R_CharacterMaterials_MPFB2.md`, first as an unnumbered phase (CM3).
- **Numbered Phase07 by the lead, 2026-09-27** (CM4), verbatim:
  - *"I would like to get the character materials in as soon as possible after phase 5… Studio is going to be pulling from the matter library and there no character materials in the library at all so they will magenta… I would rather have everything in and 'uncalibrated' yet then a bunch of magenta"*;
  - on the plan: *"yes, We have time so let's just do them in Phase 7 as redefined and we will be good."*
- Library Coverage moved from Phase07 to **Phase08**.
- **This phase runs on this machine straight after Phase05, at the same time as Phase06 on the UE machine.** The platform's character work points Studio at the library once this phase lands (lead, 2026-09-27), and checks it in Studio straight away (L4).
- Discovery opened by the lead, 2026-09-27 (`/discovery P7`): Pass 1, then the lead's rulings L1–L4 the same day.

## Outcome

**A character wears real materials from the library (skin in six tones, eyes, mouth and teeth, lips, nails, hair and basic clothing fabrics) in Blender and in a USD viewer, and in Unreal once it is calibrated. None of them shows the missing-material magenta, and every one works on any character, not only the one it was made on.**

Concretely at close:
- the `biological` Domain exists (CM1), with its articles built from recipes like every other article;
- the MakeHuman body shows the full set side by side in the Phase05 rig;
- every article is marked **candidate**, meaning checked in USDLiveView and Blender and awaiting the Unreal column (Phase06). It becomes **approved** once Unreal agrees (research `260926_R_BigPicture_NimbleSetup.md` Pass 8, the momentum rule);
- **Studio can take the set at once** (L4). One command writes the install Studio reads, with every article's status and master in it.

## Why this is a phase

It is one user-facing result: characters get library materials. It carries the calls that are expensive to unwind:
- a new Domain;
- whether layers may carry colour;
- whether hair and eyes get masters of their own;
- where body-specific ("fit") data lives.

It runs before Unreal exists, so any new master or input it adds means rebuilding Phase06's Unreal package. The lead accepts that (*"we will need to adjust things once we have the actual UE test rig added"*; and L3: *"don't worry about what is happening in phase 7, everntually it all comes together"*).

---

## Lead rulings (2026-09-27)

Asked as four calls at the end of Pass 1; answered the same day. **Verbatim**, except that a platform phase number is replaced with a description (this repo is public).

| # | The call | The lead's words | Ruled |
|---|---|---|---|
| **L1** | Eyes, mouth and body regions: split the mesh, or paint masks on the hm08 body? | *"What sets us up for the best quality down the road, if the same - what is most aligned with the spirit of the IMRSV project?"* | **Split the mesh.** Both of the lead's criteria give the same answer (below). Answers CM-Q9, and CM-Q6 for regions. |
| **L2** | Hair, brows and lashes: where does a card's cut-out come from? | *"your recc"* | **(a): a cut-out map the mesh supplies when the material is bound**, with the hair fibre on the Masked master. A `Hair` master is probed only if Masked hair looks wrong. Answers CM-Q3. |
| **L3** | The colour channel on layers (CM-Q5): here, or back to Phase08? | *"Do what needs doing, don't worry about what is happening in phase 7, everntually it all comes together."* | **Build it here only if this phase needs it.** Holding it back so Phase06 has a stable contract is no longer a reason (read: "phase 7" as the other phases' timing). With L1, nothing in the Outcome needs it, so by default it stays with Phase08's dust. If the rig shows skin needs it (a lip border, tone variation), it is built here. |
| **L4** | How does Studio get these, given that a release cannot hold candidates? | *"When this phase is done, it need to be used in the Studio immediatly in [the platform's Studio phase] to verify everything looks close. Whatever you need to approve with your higher ups is what we need to do to build things and test things and stop working about non-existent version control on an unreleased product that only the two of us know anything about"* | **No release, and no release ceremony before the first release.** Studio takes the working tree the way USDLiveView already does (`serve_to_stage.py`, from the lead's 2026-09-25 *"Make a material, serve it to stage. no versioning"*). That install carries each article's status **and its master**, so Studio can route by master rather than by class (P4). Nothing needs approving: the only thing in the way was `ReleaseModel.md`'s own rule, which is for releases, and there is none. |

**Why L1 is the mesh split, on both of the lead's criteria:**
- **Quality down the road.** The white of the eye and the iris, teeth and gums, and nail and skin are physically separate surfaces with sharp edges. Split, each gets its own complete material (its own scatter, coat and roughness) at any resolution. A mask instead blends two materials inside one shader, is limited by the mask's resolution, and is limited to what one master can do: a two-layer blend is opaque and cannot mix a scattering skin with a glossy nail.
- **Reach.** Masks work on the hm08 body only. A split works on every character, creature or Creator-made mesh (the Outcome's "any character").
- **The IMRSV spirit.** The platform's own tenets are *"slot names are the contract; the pixels are not"* and *"characters do NOT travel with bespoke materials"* (research Pass 2): a character carries named slots and library references. A split is exactly that, with more slots. Masks put body-bound pixels back into the chain.
- **What masks are still for:** soft detail layered *on top* (a blush at the lip border, tone variation, freckles, makeup). That is an addition over the split, later, not an alternative to it. L1 does not close it off.

---

## The Brief

### First human test

No running service. The surfaces are the rig's picture sheet, Blender's Asset Browser, and USDLiveView (and then Studio) through the dev install.

1. `uv run tools/parity/rig.py Skin_FitzpatrickIII_Clean_Base_s001_v01` → open the sheet. **Expect:** the sphere and cube read as mid-tone skin in both columns, with a soft light bleed at the edges and pores on the close-up. The scorecard marks it "recognisable" (the Subsurface bar). *(The exact name is fixed at 7.1 by the Identity grammar; the command takes whatever lands.)*
2. **Blender 5.2** → Asset Browser → the Matter library → `biological / tissue` → drag the skin onto the default cube → Rendered view. **Expect:** skin, not magenta. The asset's tags include `candidate`.
3. `uv run tools/releases/serve_to_stage.py --view <a scratch composition>` → in USDLiveView, find the skin under `biological / tissue` and apply it. **Expect:** skin, not magenta. The served catalog lists it with `status: candidate` and `master: Subsurface`. *(Unverified: whether Stage accepts a class it has never seen. If it does not, that is M1/P4; see Pass 1 F9.)*
4. `rig.py` on each of the six skins, and `--sweep` on one. **Expect:** six tones from Fitzpatrick I to VI; a soft oily sheen (coat) and a faint grazing-angle fuzz; every slider moves both columns alike.
5. `uv run tools/parity/rig.py --character` → one sheet: **the MakeHuman body** (full length, a face close-up and a hand close-up), USDLiveView's renderer | Blender | Unreal (empty). **Expect:** skin, lips, finger- and toenails, the white of the eye, iris, teeth, gums, tongue and a garment each show their own material. Nothing is magenta and nothing is default grey.
6. The same sheet with **hair, brows and lashes** on the body: strands cut out, not solid cards, in both columns.
7. **Studio** (the platform's check, L4): the platform points its Studio install at this repo with `serve_to_stage.py --runtime <Studio's Matter install>` (a copy rather than links if that machine needs it) and applies the set to its character. **Expect:** it looks close to the rig. Magenta there means a routing gap on the platform side (M1/P4), not a missing material.

**Reconciled with the steps:** click 1 is 7.1's. Clicks 2–3 are 7.2's. Click 4 is 7.3's. Click 5 is 7.5's: **7.4 shows the body in skin only, which is click 5 with the other regions still grey.** Click 6 is 7.6's. Click 7 is the close's hand-off; the install it uses exists from 7.2.

### In now

- **The `biological` Domain** with classes `tissue` (skin, mucosa, sclera, iris, cornea), `keratin` (hair, nail) and `bone` (enamel, dentin, bone), in `Taxonomy.md` and in the one place the tools list the classes (`validate_recipe.py` `TAXONOMY`). Plant matter stays where it is (CM1).
- **The status field** (draft / candidate / approved) **in the recipe only**, not in the `.mtlx` (D-S). It reaches people through the dev install (`serve_to_stage.py`, which today stamps every article `draft`) and the Blender library (as an asset tag).
- **The dev install carries each article's master** beside its status (L4), so Studio can route by the article's own master (P4) and a new class is not magenta for want of a routing row.
- **The Blender library built from the working tree**, not from the frozen `matterlib-0.1.0` catalog, so a new article reaches Blender at all (F8). Candidates are included and tagged: *"I would rather have everything in and 'uncalibrated' yet then a bunch of magenta"*.
- **Skin ×6**, `Skin_FitzpatrickI…VI` on the Subsurface master: Physically Based albedo and scatter radius, MPFB2's CC0 roughness, and one tiling pore overlay. **This comes first: it needs no contract change.**
- **The three skin inputs**: subsurface scatter anisotropy, coat (planned carrier C2, pulled forward from Phase08's question 3) and fuzz. All three are OpenPBR inputs (lane A), so this is additive. **Each gets its Blender master input in the same step** (research Pass 8b). Blender 5.2 has all three (P1).
- **CM-Q10, measured**: Marble and a skin under Blender's `RANDOM_WALK` and `RANDOM_WALK_SKIN` subsurface methods. Add a `Skin` master token only if one setting cannot serve both.
- **The MakeHuman body in the rig**, split into one part per substance (L1): the CC0 hm08 body and its eye, teeth and tongue meshes. A rig mode binds one article per part.
- **The other substances**: lip mucosa, nail, sclera, iris, enamel, gum and tongue mucosa, and the fabrics pulled forward from Phase08 (cotton, denim, leather).
- **Hair, brows and lashes (L2)**: a hair-fibre article on Masked (melanin colour, roughness, and anisotropy, which is carrier C3), plus **one new input: a cut-out map the mesh supplies when the material is bound**. It is carried as a standard USD input on the material, connected into the article the way the Creator sliders are (`LCDSchema.md` §Carrier rule). With no map supplied, it is fully opaque (solid cards, never magenta). This is the first piece of a "fit"; its name and the Glossary term are ruled at 7.6.
- **The colour channel on layers, only if the rig shows this phase needs it** (L3).
- **The hand-off to the platform**: `PlatformDependencies.md` M1; a new row for the region slots (L1) and the cut-out input (L2); and Studio taking the dev install (L4).

### Not now

- Calibrating against Unreal: Phase06 builds the Unreal column, and these articles are re-judged when it arrives.
- **Cornea (planned).** MakeHuman's eye has no cornea shell (research Pass 3), so a cornea article has no surface to sit on. The wet highlight comes from coat on the sclera and iris instead. The cornea is built when an eye mesh with a shell exists.
- **Soft detail over the split** (a blush at the lip border, tone, freckles, makeup, photo detail from MPFB2's skin atlases): a later addition over L1, which it does not replace. The iris *pattern* could later use L2's input; in this phase the iris is a pigment with fine tiled detail.
- The platform's hair and garment meshes and their atlases (mesh assets, research Pass 6b). Its slot binding and character generator (platform side). The rig uses CC0 MakeHuman meshes of its own.
- CC-BY MakeHuman packs: local testing only, never committed (CM-Q8, answered by R13: contributions must be CC0-dedicable).
- **A release** (L4). No `library/releases/` record is written.
- The volume build and the nightly loop: Phase08.

### Reuse check: what the stack already gives us

| Need | What exists | Evidence (2026-09-27) |
|---|---|---|
| Skin's scattering | The Subsurface master: `subsurface_{weight,color,radius,radius_scale}` in the recipe schema, the assembler (lane A) and the Blender masters | read: `assemble_mtlx.py`, `build_masters.py`, `load_article.py` |
| Oil sheen, fuzz, forward scatter | OpenPBR `coat_*`, `fuzz_*` and `subsurface_scatter_anisotropy`. MasterSet already lists sheen and clearcoat as Opaque *params*. **The only gap is the assembler and the Blender masters**, not a new master | `MasterSet.md` row 1; P1 |
| The same inputs in Blender | Principled BSDF 5.2: `Coat Weight/Roughness/IOR/Tint`, `Sheen Weight/Roughness/Tint`, `Subsurface Anisotropy`, `Anisotropic`/`Tangent`, and `subsurface_method` ∈ {BURLEY, RANDOM_WALK, **RANDOM_WALK_SKIN**, RANDOM_WALK_LEGACY} (default RANDOM_WALK) | P1 |
| A per-binding input that any USD tool honours | The Carrier rule: a material-level input connected into the article's nodegraph resolves in every stock USD tool. Today it carries the Creator's numbers; **L2 uses it for a texture path** (unverified for a file-typed input: probed first in 7.6) | `LCDSchema.md` §Carrier rule |
| Measured values | Physically Based: Skin I–VI, Eye (Sclera), Eye (Cornea); `lookup_physically_based.py`. None for hair, nails, teeth, tongue or lips | research Pass 4 |
| Making the articles | `/matter-generate` (Phase03): recipe → assemble → gate → preview | `.claude/skills/matter-generate/` |
| A tiling pore layer | `tileable.py` and the layer generators (`tools/converters/layers/`); layers sampled at their own size (Phase04) | read |
| Side-by-side judging | The Phase05 rig: one article on a fixed scene of sphere, cube and plane | `tools/parity/job.py` (`SCENE` is one fixed file) |
| A status lifecycle | **Exists already, on release records**: `validate_manifest.py` `LIFECYCLE`, projected into the runtime catalog's `status`. Nothing carries status **before** a release | read; `ReleaseModel.md`: the runtime ignores status when it resolves |
| Getting the working tree to a Stage-based viewer | `serve_to_stage.py`: every `.mtlx` on disk, live, no release, `--runtime <dir>` for any install | read |
| The body | MPFB2's CC0 `base.obj` (hm08): its eye, teeth, tongue, hair and lash groups are **placeholders**; the real eye, teeth, tongue, hair, brow and lash meshes are separate CC0 meshes in the system-assets pack | P2; research Pass 3 |
| **Blender reaching new articles** | **Nothing.** `gen_asset_library.py` builds only from `matterlib-0.1.0`'s catalog | read (F8) |

### Decisions that bind

- **L1–L4** (§Lead rulings).
- **CM1** `biological` Domain. **CM2** substance in Matter, fit beside it: every article works on any mesh, and MPFB2 is *mined*, not ported. **CM4** everything in this phase, shipped as candidates. (Research §Resolved.)
- **D1 (2026-09-23): matter only, never assemblies.** An hm08 atlas is object-bound and never an article. L2's cut-out map belongs to the mesh and is supplied at binding; it is never part of the article.
- **The article's MaterialX is the reference, and Blender follows it** (Phase05). Each new input lands in the recipe, the assembler, `LCDSchema.md` and the Blender masters **in the same step**.
- **D-S — status lives in the recipe, not the `.mtlx`** (derived from two lead rules). BP4: *"Names never change on passing."* `_Architecture.md` §Immutability: once a `vNN` ships, *"that file is frozen"*. A status written into the `.mtlx` would change the file on promotion. This overrides research Q-G's recommendation ("both"), which was never ruled, and it leaves all 17 existing articles byte-identical. A missing key means `draft`.
- **D-E — no `Eye` master; the eye is composed from existing masters** (derived from the LCD principle, `_Architecture.md`: *"If one target can do something the others can't, don't rely on it"*). Unreal's eye model has inputs (iris depth, caustics) that neither OpenPBR nor Blender has. Sclera on Subsurface, iris on Subsurface or Opaque, both with coat for the wet look. Answers CM-Q4. The lead can overrule.
- **Subsurface colour (supersedes research Pass 8a's rule).** The Blender masters now mix subsurface colour exactly as OpenPBR does (Learnings B5, M4), so matching the base colour is no longer needed for parity. **"Unset" is wrong**: OpenPBR's default `subsurface_color` is a light grey, mixed in by `subsurface_weight`, which desaturates the skin. **Rule for skin:** set `subsurface_color` to the skin's own albedo. Base-colour texture detail keeps only `1 − subsurface_weight` of its strength (Marble's F16).
- **The Blender library includes candidates**, tagged (lead: *"everything in and 'uncalibrated'"*).
- **Bars:** Subsurface is "recognisable" (Decision of record 9). Opaque fabrics are ΔE < 2. Masked hair is judged like Lace (the whole set advisory, the close-up graded).

### Risk lane: `build` (verified)

The controls, read: the release lifecycle (`validate_manifest.py`, `freeze_release.py`, `promote_release.py`) guards `library/releases/`, and the determinism lane guards the assembled `.mtlx`. **This phase writes to neither.** No release is cut (L4). The status field lives in the recipe (D-S). The new assembler inputs are authored only when set, so every existing article stays byte-identical, and the determinism lane proves it. `gen_asset_library.py` *reads* the catalog today and will read the working tree instead; it writes only the committed Blender library. `serve_to_stage.py` writes into a runtime folder outside the repo. The contract changes (`Taxonomy.md`, `LCDSchema.md`, and L2's input in `MasterSet.md`) are additive. No authorization, secrets, destructive migration or public edge is involved. **The push is the lead's, and it is irreversible (a public repo).** It is also what Phase06 builds against: push after 7.3 (the skin inputs), and again after 7.6 (the cut-out input).

### Step list

- **7.1 — One skin in the rig.** The `biological` Domain (`Taxonomy.md` and `validate_recipe.py`), a tiling pore overlay, and `Skin_FitzpatrickIII` on Subsurface, from Physically Based and MPFB2's values, via `/matter-generate`. *(Click 1.)*
- **7.2 — A creator reaches it, marked candidate.** The recipe's `status` key (schema; missing = draft). `serve_to_stage.py` projects each article's status and master. `gen_asset_library.py` builds from the working tree's Creator-selectable articles and tags each one with its status; the asset-library checks follow. Probe whether Stage accepts the new class (F9). *(Clicks 2–3; the install click 7 uses.)*
- **7.3 — Skin that looks like skin.** Coat, fuzz and scatter anisotropy through the recipe, the assembler, `LCDSchema.md`, the Blender masters and the loader. CM-Q10 measured (Marble and skin under both Blender methods). The six skins. **Push:** Phase06 builds against these inputs. *(Click 4.)*
- **7.4 — The MakeHuman body in the rig.** Fetch the CC0 body and its eye, teeth and tongue meshes at the research's pinned sources, convert them to one USD, and split them into one part per substance (L1). Add the rig's `--character` mode (one article per part; `JOB_FORMAT.md` gains it for Phase06). The skins go on. *(Click 5, skin only.)*
- **7.5 — Every other substance.** Lip mucosa, nail, sclera, iris, enamel, gum and tongue mucosa, cotton, denim, leather, each through the rig and onto its part of the body. If a region shows it needs layer colour, L3 applies here. *(Click 5.)*
- **7.6 — Hair, brows and lashes (L2).** **Probe first:** does a file-typed input set on the material and connected into the article reach the image in USDLiveView's renderer and in Blender? Then add the cut-out input (`LCDSchema.md`, `MasterSet.md` Masked row, the assembler, the Blender masters, and the rig's binding of it) and the hair-fibre article (Masked + anisotropy, C3). CC0 MakeHuman hair, brow and lash meshes supply their own cut-outs in the rig. **Push:** Phase06's Masked master gains the input. *(Click 6.)*
- **Close.** `PlatformDependencies.md`: M1 updated; a new row for the region slots (L1) and the cut-out input (L2); Studio taking the dev install (L4, click 7). Phase06's coupling note (the inputs that landed). `Glossary.md` (the new terms). `Experience_MatterLibrary.md` §Shipped (the Blender library now includes candidates).

**Why this order:** 7.1 proves the whole path on one article with no contract change, and it is inside 90 minutes. 7.2 puts it in people's hands, Studio's included, which is the point of the phase. 7.3 lands the contract change Phase06 is waiting on, so it goes before the long tail. The body (7.4) and the other substances (7.5) need no new contract. Hair (7.6) carries the one new contract idea, so it goes last and alone.

**⚠ Split signal (raised, not cut):** hair, brows and lashes (7.6) are a second journey with a contract change of their own. Cut them into their own phase only if 7.6's probe shows the input needs more than one step's design.

### Compact build map

- **Ontology:** `docs/specs/Ontology/Taxonomy.md` (6 Domains; the classes; History) · `MasterSet.md` coverage line · `tools/validators/validate_recipe.py` `TAXONOMY` · `docs/Glossary.md`.
- **Status and master in the dev install:** `tools/converters/recipe.schema.json` (`status`) · `validate_recipe.py` (unknown keys are refused, per the `unknown_key` fixture, so the schema must gain it) · `tools/releases/serve_to_stage.py` (read the recipe's status instead of `"draft"`; add each article's master from its `.mtlx`; a copy option if Studio's machine needs one) · `tools/generators/gen_asset_library.py` (the working tree, not `CATALOG`; status tag) · `tools/conformance/{verify_asset_library.py,check_asset_library.sh}` · `blender/asset_library/MatterLibrary.blend` regenerated.
- **Skin inputs:** `recipe.schema.json` · `tools/converters/assemble_mtlx.py` (`MaterialSpec` + `_add_input`, authored only when set) · `docs/specs/Contract/LCDSchema.md` §Author tier · `blender/masters/build_masters.py` (`VERSION` bump; Coat, Sheen = fuzz, Subsurface Anisotropy; subsurface method per CM-Q10) · `blender/masters/load_article.py` (the input map).
- **Cut-out input (7.6):** `LCDSchema.md` (a new section beside §Carrier rule) · `MasterSet.md` (Masked row) · `assemble_mtlx.py` (the Masked branch) · `blender/masters/` (the per-object image) · `tools/parity/job.py` (supply it per part) · `validate_material.py` (the Masked conformance check accepts the input as a cut-out source).
- **Articles:** recipes in `tools/converters/recipes/`; `.mtlx` in `MatterLibrary/materials/biological/{tissue,keratin,bone}/` and fabrics in `synthetic/textile/`; textures in `MatterLibrary/textures/base/biological/…`; the pore overlay in `textures/shared/overlays/` with its provenance YAML.
- **Rig:** `tools/parity/job.py` (a character scene and one binding per part) · `rig.py` (`--character`) · `drivers/{storm,blender_render}.py` (several bindings) · `scene/` (the body USD, and the script that builds it from the pinned CC0 sources) · `JOB_FORMAT.md`.
- **Hand-offs:** `docs/Planning/PlatformDependencies.md` · `Phase06_UnrealTestRuntime.md` §Coupling.

## Discovery Log

### Pass 1 (2026-09-27): the product docs read against the Outcome, plus two probes

**Examined:** `_Architecture.md` · `Taxonomy.md` · `MasterSet.md` · `LCDSchema.md` · `Identity.md` · `Manifest.md`, `RuntimeCatalog.md` and `ReleaseModel.md` (status) · the research (whole) · `260926_R_BigPicture_NimbleSetup.md` (BP4, Pass 8, Q-G, Q-H) · `Phase05_TestRig.md` (closed) · the `Phase06` and `Phase08` seeds · `PlatformDependencies.md`. **Learnings:** `Blender.md` (B4, B5, B6), `MaterialX.md` (M4), `Storm.md` (S7): all three apply. **Tree grep for the phase's own terms** (`biological`, `makehuman`, `mpfb`, `hm08`, `fitzpatrick`, `skin`) over `tools/`, `blender/`, `MatterLibrary/` and the skills: **nothing**, so no prior phase built any of it. **Consumer docs:** not read (private); M1 and P4 name what the consumer needs.

**Probes (disposable; nothing in the repo):**
- **P1 — Blender 5.2.2 LTS Principled BSDF** (headless): it has `Subsurface Anisotropy`, `Coat Weight/Roughness/IOR/Tint/Normal`, `Sheen Weight/Roughness/Tint`, `Anisotropic`/`Tangent`, and `subsurface_method` ∈ {BURLEY, RANDOM_WALK, RANDOM_WALK_SKIN, RANDOM_WALK_LEGACY}, default RANDOM_WALK. It has no separate subsurface colour (B5 holds).
- **P2 — MPFB2's hm08 `base.obj`** (the research's clone in `/tmp/mpfb2` at `3edf9df`; not a reproduction): groups `body`, `helper-l-eye`, `helper-r-eye`, `helper-upper-teeth`, `helper-lower-teeth`, `helper-tongue`, `helper-hair`, `helper-{l,r}-eyelashes-{1,2}`, `helper-tights`, `helper-skirt`, `helper-genital`, and joint cubes. The eyes, teeth and tongue on the base mesh are **placeholders**; MakeHuman's real ones are separate meshes in the system-assets pack (research Pass 3). The CC0 region masks are in `data/textures/`.

**Findings:**
- **F1 — Skin needs no new master for its graph; it needs three lane-A inputs.** Confirmed against the tree and Blender 5.2 (P1). MasterSet already names sheen and clearcoat as Opaque params.
- **F2 — Research Pass 8a's Blender gap is stale.** It was written against `matter_proxy.py`, which Phase05 retired. The Blender masters now mix subsurface colour as OpenPBR does. Still missing: coat, fuzz, scatter anisotropy, and a subsurface method (none is set, so Blender's `RANDOM_WALK` applies).
- **F3 — "Leave `subsurface_color` unset" is wrong.** OpenPBR's default is a light grey, mixed in by weight. → Decisions, "Subsurface colour".
- **F4 — The status lifecycle already exists, on release records** (manifest → runtime catalog), and the runtime ignores it when resolving. What is missing is a status **before** a release. → D-S.
- **F5 — Research Q-G ("status in the recipe and the `.mtlx`") conflicts with immutability after promotion and with BP4.** Q-G was a research recommendation, never ruled, so this is not a fork. → D-S.
- **F6 — An Eye master fails the LCD principle.** → D-E.
- **F7 — Hair, brows, lashes and the iris pattern are the only Outcome items that cannot be pure substance.** A card's cut-out and an iris's radial pattern are pixels bound to a mesh. → L2.
- **F8 — A new article cannot reach Blender today.** `gen_asset_library.py` builds only from `matterlib-0.1.0`'s catalog (`CATALOG`). USDLiveView's dev loop serves the working tree but stamps everything `draft`. **This is the Outcome's entry path.** → 7.2.
- **F9 — A Stage-based viewer may route by class.** M1 says Studio routes by class, so a new class renders as the missing material. Whether Stage (which USDLiveView's dev loop uses) does the same is **unverified**. → A probe in 7.2. The dev install also carries each article's master (L4), which is what P4 needs to route without a class table.
- **F10 — Candidates cannot ride a release.** `ReleaseModel.md` requires `approved` before a freeze. → L4: no release is needed, and none is cut.
- **F11 — The rig has one fixed scene** (`job.py` `SCENE`) and one article per job. The body needs a scene of its own and one binding per part. → 7.4.

**The research's open questions, disposed:** CM-Q3 → L2 · CM-Q4 → D-E (the LCD principle) · CM-Q5 → L3 · CM-Q6 → L1 (regions: split) and L2 (cut-outs supplied by the mesh); soft detail later · CM-Q8 → answered (R13: never committed) · CM-Q9 → L1 · CM-Q10 → measured in 7.3.

## Discovery Status

- **Passes captured:** 1, plus the lead's rulings L1–L4. **The Brief is complete.**
- **Checks to carry forward:** the Stage class probe (F9, 7.2). The file-typed input probe (7.6, before building the cut-out input). The Chiang-hair probe, only if Masked hair looks wrong (L2). Re-download the system-assets pack at the research's recorded hash for the eye, teeth, tongue, hair, brow and lash meshes: of the `/tmp` copies, only the MPFB2 clone is left.

## Sources (pointers, not copies)

- `docs/Planning/Research/260927_R_CharacterMaterials_MPFB2.md`: the whole thread (pinned sources and hashes in Pass 3).
- `docs/Planning/Phases/Future/Phase08_LibraryCoverage.md`: questions 3 (carriers) and 10 (layer colour).
- `docs/Planning/Phases/Future/Phase06_UnrealTestRuntime.md`: the masters this phase's contract calls touch.
- `docs/Planning/Phases/Complete/Phase05_TestRig.md`: the rig; F13, F16.
- `docs/specs/Ontology/{Taxonomy,MasterSet}.md` · `docs/specs/Contract/LCDSchema.md` · `docs/specs/Distribution/ReleaseModel.md` · `docs/Planning/PlatformDependencies.md` (M1, P4).

## Execution Log

*Ledger: step · result · next. Findings live in the commit messages.*

### ▶ Resume here (2026-09-27, second execute run)

- **Where:** 7.1 ✅, 7.2 ✅ except click 3, 7.3 ✅, 7.4 ✅, **7.5.1 ▶ SCAFFOLD COMPLETE — sitting owed (head and hands)**. **Not pushed**; the push after 7.3 is the lead's (Phase06 builds against these inputs).
- **Owed by the lead:** click 3 (USDLiveView through Stage; Stage is still running on the working tree, `serve_to_stage.py --off` restores the release); the 7.5.1 sitting.
- **F13 RULED (lead, 2026-09-27): (b)**, *"I assume B but we eventually want the best looking option can get"*. The character mesh carries a real-scale detail UV set; Studio's stopgap until it does is (a). **At the close:** a `PlatformDependencies.md` row (the detail UV set on the platform's character mesh). **Kept as intent, not built (Don't Delete):** the best-looking option is still to be found; (c) (projection without UVs, with a rest-pose attribute so it holds when animated) or a mix stays open for when the Unreal column exists.
- **Next:** 7.5.2, clothing: a CC0 garment from the system-assets pack, and cotton, denim and leather with generated weave and grain detail. 7.5 is walked as two acts (head and hands, then clothing).
- **Deviation (small), 7.4 → 7.5:** the splits *inside* a mesh (lips and nails out of the body, cornea, pupil, iris and sclera, teeth and gums) moved to 7.5.1, beside their articles. **Deviation (small), 7.5.1: the cornea is built.** The Brief's Not now rested on "no cornea shell"; the high-poly eye has one, hidden by its texture, and rendered it covers the iris. A pupil part and article came with it.
- **F13 (measured 7.4; the lead's call) — a tiling article on MakeHuman's UVs.** A skin article's detail is sized per UV tile (`s001`: one tile = 1 cm, Identity §Scale tags). **One hm08 UV unit spans 1.69 m of body** (median; p5 0.81, p95 2.57), so on the raw atlas the pores render **~170x too large**. The rig stores each part's UVs in metres (the source UVs × the part's median density), which puts the pores at their size on average, but two things remain, both visible on the body sheet: detail varies ~3x in size between the atlas's islands, and **Blender shows the tiling normal map's seams** along the island borders on the neck and chest (Storm barely). The ways out, for the lead: **(a)** the platform sets `uv_scale` per slot (no change here; size only, seams stay); **(b)** the character mesh ships a real-scale second UV set (mesh work, platform side; seams stay wherever islands meet); **(c)** the article samples its tiling detail by a projection that does not use the UVs (triplanar; a contract change here, no seams, works on any mesh as CM2 promises).
- **Unchanged red:** `run_all.py`'s `approval_binds_freeze` (the pilot re-approval, inherited from Phase05).

**Tree at start (2026-09-27):** `main` @ `e35bf83`, clean, 3 ahead of origin, no other session visible. **Always-on gate at start:** `run_all.py` 14 PASS / 2 SKIP / 1 FAIL, `approval_binds_freeze` alone (inherited from Phase05's close: the pilot re-approval is still owed).

| Step | Result | Next |
|---|---|---|
| **7.1** | **✅ (sitting 2026-09-27).** Lead, on the Skin III sheet, verbatim: *"Yep...  looks the same"*. Built: the `biological` Domain (`Taxonomy.md`, `MasterSet.md` coverage, `validate_recipe.py`, the recipe schema); `Skin_FitzpatrickIII_Clean_Base_s001_v01` on Subsurface; the shared `Skin_Pores` micro-surface (1 cm tile, seamless, roughness mean 0.500); the Physically Based lookup now carries `subsurfaceRadius` (**centimetres**, established from the paper the entry cites: Skin IV–VI is exactly Jensen 2001's skin1 diffusion length). **Deviation (small):** the pores are the article's own normal and roughness, not a wear overlay, because an overlay ships at 0 (C1) and would leave skin plastic by default. **F12 — the rig imported every Blender scene at 1/100 scale.** Each setting scene sublayers the test scene but did not author `metersPerUnit`, which USD reads from the root layer only, so Blender took centimetres. Harmless on opaque matter; on subsurface, 4.8 mm of scatter crossed a 3.6 mm sphere and the skin rendered pale and waxy (ΔE 12.8). Fixed in `job.py` (the header now carries the test scene's `upAxis`/`metersPerUnit`, shared constants in `build_scene.py`; the test scene regenerates byte-identical). **Skin: ΔE 12.8 → 2.69 whole set / 2.44 close-up** (Subsurface bar: recognisable). Phase05's distance-bearing numbers were taken at the wrong scale. **Marble: 3.95 → 2.60** (whole set; close-up 2.56), so Phase05's F16 colour gap was mostly this bug. Its Blender ruler check now reads OFF (match 0.05): 8.5 mm of real scatter blurs the veins on the floor, and Storm's approximation does not blur. **Oak (opaque) is unchanged** (0.79 / 0.65, ruler 1.00 in both), so the fix does not touch sizing. Diamond (absorption depth) re-measured at 7.3. Gate: 14 PASS / 2 SKIP / 1 FAIL, the inherited `approval_binds_freeze` alone; the determinism lane shows every existing article byte-stable. | 7.2. |
| **7.2** | **Click 2 ✅ (sitting 2026-09-27); click 3 owed.** Lead, verbatim: *"I can't test stage right now but blender worked"*. Click 3 (USDLiveView through Stage) waits for the lead; the Stage probe (F9) already shows the skin listed as `biological/tissue`, `candidate`. Built: the recipe's `status` key (schema; a recipe metadata key, so it never reaches the `.mtlx`: the determinism lane shows all 18 articles byte-stable); `tools/converters/working_tree.py`, the one list both reach paths read (status = the recipe's, else the `matterlib-0.1.0` release's, else `draft`; master = the article's own token); `serve_to_stage.py` projects status and **master** (L4); `gen_asset_library.py` builds from the working tree and tags each asset with its status. **The Blender library has 17 articles (was 11)**, `Skin_FitzpatrickIII` under `biological/tissue` as `candidate`. The four Phase05 rig-passed, unreleased articles (GreyCard, ABS_Glossy, Oak, Glass_Green) are marked `candidate` by the same rule; Earthenware, never through the rig, stays `draft`. **F9 answered (Stage probe):** served, Stage lists 17 articles with the skin as `biological/tissue`, `status: candidate`; it accepts the new class and drops the `master` key it does not know (reading it is P4). Gates: `check_asset_library.sh` PASS (17 CONFORMS; its verifier's subject set moved to the working tree with a `matterlib-0.1.0` floor, and one **FALSE RED** recorded in its header: GreyCard has no sliders by design); `run_all.py` unchanged (14 / 2 / 1, the inherited `approval_binds_freeze`). **Stage is running on the working tree** (started by this step; `serve_to_stage.py --off` restores the release). | Lead: clicks 2–3. |
| **7.3** | **✅ (sitting 2026-09-27).** Lead, verbatim: *"skins look right in blender..of course I only see it on a sphere... I assume these map to humanoid meshs and ther is more detail for various body areas"*. The humanoid question is 7.4's: see F13 below. Landed at `7.3`: coat, fuzz and scatter anisotropy as optional lane-A carriers (every existing article byte-stable), Blender masters v5; the six skins, all `candidate`. **CM-Q10 answered: `RANDOM_WALK_SKIN`, no `Skin` token** (Marble 2.60 → 1.82, under the bar). **Storm ignores scatter anisotropy** (Learnings S8): kept at 0.8. Rig, whole set: 3.10–4.07 over the six (Subsurface: recognisable). Diamond at true scale: 16.7 / 21.4. Blender library: 22 articles. Gates: asset library PASS; `run_all.py` 14 / 2 / 1 unchanged. | Lead: click 4; then push. |
| **7.4** | **✅ (sitting 2026-09-27).** Lead, verbatim: *"I assume B but we eventually want the best looking option can get.Skins look close enough for now"*. **F13 ruled (b)**, below. Landed at `7.4`: `rig.py --character [<skin>]`, the CC0 MakeHuman body from pinned, hash-checked sources (body, eyes, teeth, tongue; MakeHuman's own proxy fit); per-part binding, masks and scoring; `JOB_FORMAT.md` §The character job. F13 measured (above). Skin on the body, Storm vs Blender (whole body / face / hand): **III 2.53 / 3.80 / 4.04 · VI 2.03 / 2.79 / 3.70**. GreyCard unchanged (0.35 / 0.26). `run_all.py` 14 / 2 / 1 unchanged. | Lead: click 5; F13. |
| **7.5.1** | **▶ SCAFFOLD COMPLETE — sitting owed (head and hands).** Landed at `7.5.1`: nine articles, all `candidate` (lips, nail, sclera, iris, pupil, cornea, enamel, gum, tongue), each on its own part (MPFB2's CC0 masks for lips and nails; the eye and teeth split by their own textures). The rig gains a `mouth` view (face hidden: the lips are closed). Storm vs Blender: lips 4.7, nails 2.5, the eye through its cornea 3.5 (face), enamel 0.6, gums 6.8, tongue 7.1 (Blender's mucosa brighter and redder: S8). Blender library 31. Gates unchanged. | Lead: the head-and-hands sitting; then 7.5.2. |
