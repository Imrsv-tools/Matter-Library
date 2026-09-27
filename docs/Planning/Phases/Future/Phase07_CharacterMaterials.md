# Phase07 — Character Materials

**Status:** DISCOVERY — Pass 1 captured (2026-09-27). **The Brief is drafted; four lead calls are open (§Lead calls).** Lane: `build` (verified, §Risk lane).
- **Seeded** 2026-09-27 from `docs/Planning/Research/260927_R_CharacterMaterials_MPFB2.md`, first as an unnumbered phase (CM3).
- **Numbered Phase07 by the lead, 2026-09-27** (CM4), verbatim:
  - *"I would like to get the character materials in as soon as possible after phase 5… Studio is going to be pulling from the matter library and there no character materials in the library at all so they will magenta… I would rather have everything in and 'uncalibrated' yet then a bunch of magenta"*;
  - on the plan: *"yes, We have time so let's just do them in Phase 7 as redefined and we will be good."*
- Library Coverage moved from Phase07 to **Phase08**.
- **This phase runs on this machine straight after Phase05, at the same time as Phase06 on the UE machine.** The platform's character work points Studio at the library once this phase lands (lead, 2026-09-27).
- Discovery opened by the lead, 2026-09-27 (`/discovery P7`).

## Outcome

**A character wears real materials from the library (skin in six tones, eyes, mouth and teeth, lips, nails, hair and basic clothing fabrics) in Blender and in a USD viewer, and in Unreal once it is calibrated. None of them shows the missing-material magenta, and every one works on any character, not only the one it was made on.**

Concretely at close:
- the `biological` Domain exists (CM1), with its articles built from recipes like every other article;
- the MakeHuman body shows the full set side by side in the Phase05 rig;
- every article is marked **candidate**, meaning checked in USDLiveView and Blender and awaiting the Unreal column (Phase06). It becomes **approved** once Unreal agrees (research `260926_R_BigPicture_NimbleSetup.md` Pass 8, the momentum rule).

## Why this is a phase

It is one user-facing result: characters get library materials. It carries the calls that are expensive to unwind:
- a new Domain;
- whether layers may carry colour;
- whether hair and eyes get masters of their own;
- where body-specific ("fit") data lives.

It runs before Unreal exists, so any new master or input it adds means rebuilding Phase06's Unreal package. The lead accepts that ("we will need to adjust things once we have the actual UE test rig added"). The way to keep that cheap is to **rule the contract calls early in this phase** and push them, so the UE machine builds against them.

---

## The Brief

### First human test

No running service. The surfaces are the rig's picture sheet, Blender's Asset Browser, and USDLiveView through the dev loop.

1. `uv run tools/parity/rig.py Skin_FitzpatrickIII_Clean_Base_s001_v01` → open the sheet. **Expect:** the sphere and cube read as mid-tone skin in both columns, with a soft light bleed at the edges and pores on the close-up. The scorecard marks it "recognisable" (the Subsurface bar). *(The exact name is fixed at 7.1 by the Identity grammar; the command takes whatever lands.)*
2. **Blender 5.2** → Asset Browser → the Matter library → `biological / tissue` → drag the skin onto the default cube → Rendered view. **Expect:** skin, not magenta. The asset's tags include `candidate`.
3. `uv run tools/releases/serve_to_stage.py --view <a scratch composition>` → in USDLiveView, find the skin under `biological / tissue` and apply it. **Expect:** skin, not magenta; the served catalog lists it as `status: candidate`. *(Unverified: whether Stage accepts a class it has never seen. If it does not, that is M1/P4, a platform ask; see Pass 1 F9.)*
4. `rig.py` on each of the six skins, and `--sweep` on one. **Expect:** six tones from Fitzpatrick I to VI; a soft oily sheen (coat) and a faint grazing-angle fuzz; every slider moves both columns alike.
5. `uv run tools/parity/rig.py --character` → one sheet: **the MakeHuman body** (full length, a face close-up and a hand close-up), USDLiveView's renderer | Blender | Unreal (empty). **Expect:** skin, lips, finger- and toenails, sclera, iris, teeth, gums, tongue and a garment each show their own material. Nothing is magenta and nothing is default grey.
6. *(Depends on lead call 2.)* The same sheet with hair, brows and lashes on the body.

**Reconciled with the steps:** click 1 is 7.1's. Clicks 2–3 are 7.2's. Click 4 is 7.3's. Click 5 is 7.5's: **7.4 shows the body in skin only, which is click 5 with the other regions still grey.** Click 6 is 7.6's.

### In now

- **The `biological` Domain** with classes `tissue` (skin, mucosa, sclera, iris, cornea), `keratin` (hair, nail) and `bone` (enamel, dentin, bone), in `Taxonomy.md` and in the one place the tools list the classes (`validate_recipe.py` `TAXONOMY`). Plant matter stays where it is (CM1).
- **The status field** (draft / candidate / approved) **in the recipe only**, not in the `.mtlx` (Decisions, D-S). It reaches people through the dev catalog (`serve_to_stage.py`, which today stamps every article `draft`) and the Blender library (as an asset tag).
- **The Blender library built from the working tree**, not from the frozen `matterlib-0.1.0` catalog, so a new article reaches Blender at all (Pass 1 F8). Candidates are included and tagged: *"I would rather have everything in and 'uncalibrated' yet then a bunch of magenta"*.
- **Skin ×6**, `Skin_FitzpatrickI…VI` on the Subsurface master: Physically Based albedo and scatter radius, MPFB2's CC0 roughness, and one tiling pore overlay. **This comes first: it needs no contract change.**
- **The three skin inputs**: subsurface scatter anisotropy, coat (planned carrier C2, pulled forward from Phase08's question 3) and fuzz. All three are OpenPBR inputs (lane A), so this is additive. **Each gets its Blender master input in the same step** (research Pass 8b). Blender 5.2 has all three (Pass 1 P1).
- **CM-Q10, measured**: Marble and a skin under Blender's `RANDOM_WALK` and `RANDOM_WALK_SKIN` subsurface methods. Add a `Skin` master token only if one setting cannot serve both.
- **The MakeHuman body in the rig**: the CC0 hm08 body and its eye, teeth and tongue meshes, split into one part per substance (per lead call 1), and a rig mode that binds one article per part.
- **The other substances**: lip mucosa, nail, sclera, iris, enamel, gum and tongue mucosa, and the fabrics pulled forward from Phase08 (cotton, denim, leather).
- **Hair, brows and lashes**, in the form lead call 2 decides.
- **The hand-off to the platform**: `PlatformDependencies.md` M1, plus the region slots the geometry route needs (CM-Q9, lead call 1).

### Not now

- Calibrating against Unreal: Phase06 builds the Unreal column, and these articles are re-judged when it arrives.
- **Cornea (planned).** MakeHuman's eye has no cornea shell (research Pass 3), so a cornea article has no surface to sit on. The wet highlight comes from coat on the sclera and iris instead. The cornea is built when an eye mesh with a shell exists.
- **Soft region tone, freckles, makeup and photo detail from MPFB2's skin atlases** (fit sets, CM-Q6): these depend on lead calls 1–3.
- The platform's hair and garment meshes and their atlases (mesh assets, research Pass 6b). Its slot binding and character generator (platform side).
- CC-BY MakeHuman packs: local testing only, never committed (CM-Q8, answered by R13: contributions must be CC0-dedicable).
- A release. No `library/releases/` record is written (lead call 4).
- The volume build and the nightly loop: Phase08.

### Reuse check: what the stack already gives us

| Need | What exists | Evidence (2026-09-27) |
|---|---|---|
| Skin's scattering | The Subsurface master: `subsurface_{weight,color,radius,radius_scale}` in the recipe schema, the assembler (lane A) and the Blender masters | read: `assemble_mtlx.py`, `build_masters.py`, `load_article.py` |
| Oil sheen, fuzz, forward scatter | OpenPBR `coat_*`, `fuzz_*` and `subsurface_scatter_anisotropy`. MasterSet already lists sheen and clearcoat as Opaque *params*. **The only gap is the assembler and the Blender masters**, not a new master | `MasterSet.md` row 1; Blender probe P1 |
| The same inputs in Blender | Principled BSDF 5.2: `Coat Weight/Roughness/IOR/Tint`, `Sheen Weight/Roughness/Tint`, `Subsurface Anisotropy`, and `subsurface_method` ∈ {BURLEY, RANDOM_WALK, **RANDOM_WALK_SKIN**, RANDOM_WALK_LEGACY} (default RANDOM_WALK) | probe P1 |
| Measured values | Physically Based: Skin I–VI, Eye (Sclera), Eye (Cornea); `lookup_physically_based.py`. None for hair, nails, teeth, tongue or lips | research Pass 4 |
| Making the articles | `/matter-generate` (Phase03): recipe → assemble → gate → preview | `.claude/skills/matter-generate/` |
| A tiling pore layer | `tileable.py` and the layer generators (`tools/converters/layers/`); layers sampled at their own size (Phase04) | read |
| Side-by-side judging | The Phase05 rig: one article on a fixed scene of sphere, cube and plane | `tools/parity/job.py` (`SCENE` is one fixed file) |
| A status lifecycle | **Exists already, on release records**: `validate_manifest.py` `LIFECYCLE`, projected into the runtime catalog's `status`. Nothing carries status **before** a release | read; `ReleaseModel.md`: the runtime ignores status when it resolves |
| The body | MPFB2's CC0 `base.obj` (hm08): groups `body` and `helper-*` (eyes, upper and lower teeth, tongue, hair, lashes) are **placeholders**; the real eye, teeth and tongue are separate CC0 meshes in the system-assets pack | probe P2 |
| Region masks | MPFB2's CC0 greyscale masks (lips, fingernails, toenails, ears, eyelids, face, and others) | probe P2 |
| USDLiveView reaching new articles | `serve_to_stage.py` serves every `.mtlx` on disk, live, with no release | read |
| **Blender reaching new articles** | **Nothing.** `gen_asset_library.py` builds only from `matterlib-0.1.0`'s catalog | read (F8) |

### Decisions that bind

- **CM1** `biological` Domain. **CM2** substance in Matter, fit beside it: every article works on any mesh, and MPFB2 is *mined*, not ported. **CM4** everything in this phase, shipped as candidates. (Research §Resolved.)
- **D1 (2026-09-23): matter only, never assemblies.** An hm08 atlas is object-bound and never an article.
- **The article's MaterialX is the reference, and Blender follows it** (Phase05). Each new input lands in the recipe, the assembler, `LCDSchema.md` §Author tier and the Blender masters **in the same step**.
- **D-S — status lives in the recipe, not the `.mtlx`** (derived here, from two lead-owned rules). BP4: *"Names never change on passing."* `_Architecture.md` §Immutability: once a `vNN` ships, *"that file is frozen"*. A status written into the `.mtlx` would change the file on promotion, which forces either a new `vNN` or an edited frozen file. This overrides research Q-G's recommendation ("both"), which was never ruled. It also leaves all 17 existing articles byte-identical (Phase05 F4's cost disappears). A missing key means `draft`.
- **D-E — no `Eye` master; the eye is composed from existing masters** (derived from the LCD principle, `_Architecture.md`: *"If one target can do something the others can't, don't rely on it"*). Unreal's eye model has inputs (iris depth, caustics) that neither OpenPBR nor Blender has, so an article could not carry them. Sclera on Subsurface, iris on Subsurface or Opaque, both with coat for the wet look. Answers CM-Q4. The lead can overrule.
- **Subsurface colour, corrected (supersedes research Pass 8a's rule).** The Blender masters now mix subsurface colour exactly as OpenPBR does (Learnings B5, M4), so matching the base colour is no longer needed for parity. **"Unset" is wrong**: OpenPBR's default `subsurface_color` is a light grey, mixed in by `subsurface_weight`, which desaturates the skin. **Rule for skin:** set `subsurface_color` to the skin's own albedo, and remember that base-colour texture detail keeps only `1 − subsurface_weight` of its strength (Marble's F16).
- **The Blender library includes candidates**, tagged (lead: *"everything in and 'uncalibrated'"*).
- **Bars:** Subsurface is "recognisable" (Decision of record 9). Opaque fabrics are ΔE < 2.

### Risk lane: `build` (verified)

The controls, read: the release lifecycle (`validate_manifest.py`, `freeze_release.py`, `promote_release.py`) guards `library/releases/`, and the determinism lane guards the assembled `.mtlx`. **This phase writes to neither.** No release is cut (lead call 4). The status field lives in the recipe (D-S). The new assembler inputs are authored only when set, so every existing article stays byte-identical, and the determinism lane proves it. `gen_asset_library.py` *reads* the catalog today and will read the working tree instead; it writes only the committed Blender library. The contract changes (`Taxonomy.md`, `LCDSchema.md` §Author tier) are additive, semver-minor. No authorization, secrets, destructive migration or public edge is involved. **The push is the lead's, and it is irreversible (a public repo).** It is also what Phase06 builds against, so push after 7.3 lands the new inputs.

### Step list

- **7.1 — One skin in the rig.** The `biological` Domain (`Taxonomy.md` and `validate_recipe.py`), a tiling pore overlay, and `Skin_FitzpatrickIII` on Subsurface, from Physically Based and MPFB2's values, via `/matter-generate`. *(Click 1.)*
- **7.2 — A creator reaches it, marked candidate.** The recipe's `status` key (schema; missing = draft). `serve_to_stage.py` projects it. `gen_asset_library.py` builds from the working tree's Creator-selectable articles and tags each one with its status; the asset-library checks follow. Probe whether Stage accepts the new class. *(Clicks 2–3.)*
- **7.3 — Skin that looks like skin.** Coat, fuzz and scatter anisotropy through the recipe, the assembler, `LCDSchema.md`, the Blender masters and the loader. CM-Q10 measured (Marble and skin under both Blender methods). The six skins. **Push after this step:** Phase06 builds its masters against these inputs. *(Click 4.)*
- **7.4 — The MakeHuman body in the rig.** Fetch the CC0 body and its eye, teeth and tongue meshes at the research's pinned sources, convert them to one USD, and split them into one part per substance (lead call 1). Add the rig's `--character` mode (one article per part; `JOB_FORMAT.md` gains it for Phase06). The skins go on. *(Click 5, skin only.)*
- **7.5 — Every other substance.** Lip mucosa, nail, sclera, iris, enamel, gum and tongue mucosa, cotton, denim, leather, each through the rig and onto its part of the body. *(Click 5.)*
- **7.6 — Hair, brows and lashes**, in lead call 2's form. *(Click 6.)*
- **Close.** `PlatformDependencies.md` M1 and the region-slot ask. Phase06's coupling note (the inputs that landed). `Glossary.md` (the new terms). `Experience_MatterLibrary.md` §Shipped (the Blender library now includes candidates).

**Why this order:** 7.1 proves the whole path on one article with no contract change, and it is inside 90 minutes. 7.2 puts it in people's hands, which is the point of the phase ("rather… 'uncalibrated' than… magenta"). 7.3 lands the contract change that Phase06 is waiting on, so it goes before the long tail. The body (7.4) needs the region decision (call 1), and hair (7.6) the fit decision (call 2), so both come after the calls.

**⚠ Split signal (raised, not cut):** hair, brows and lashes (7.6) cannot be pure substance, because a hair card's cut-out is pixels bound to one mesh. They need a new contract idea (call 2), which makes them a second independently demonstrable journey. Keep them as the last step; cut them into their own phase if call 2's design grows past one step.

### Compact build map

- **Ontology:** `docs/specs/Ontology/Taxonomy.md` (6 Domains; the classes; History) · `MasterSet.md` coverage line · `tools/validators/validate_recipe.py` `TAXONOMY` · `docs/Glossary.md`.
- **Status:** `tools/converters/recipe.schema.json` (`status`) · `validate_recipe.py` (the `unknown_key` fixture shows unknown keys are refused, so the schema must gain it) · `tools/releases/serve_to_stage.py` (read the recipe's status instead of `"draft"`) · `tools/generators/gen_asset_library.py` (the working tree, not `CATALOG`; status tag) · `tools/conformance/{verify_asset_library.py,check_asset_library.sh}` · `blender/asset_library/MatterLibrary.blend` regenerated.
- **New inputs:** `recipe.schema.json` · `tools/converters/assemble_mtlx.py` (`MaterialSpec` + `_add_input`, authored only when set) · `docs/specs/Contract/LCDSchema.md` §Author tier · `blender/masters/build_masters.py` (`VERSION` bump; Coat, Sheen = fuzz, Subsurface Anisotropy; subsurface method per CM-Q10) · `blender/masters/load_article.py` (the input map).
- **Articles:** recipes in `tools/converters/recipes/`; `.mtlx` in `MatterLibrary/materials/biological/{tissue,keratin,bone}/` and fabrics in `synthetic/textile/`; textures in `MatterLibrary/textures/base/biological/…`; the pore overlay in `textures/shared/overlays/` with its provenance YAML.
- **Rig:** `tools/parity/job.py` (a character scene and one binding per part) · `rig.py` (`--character`) · `drivers/{storm,blender_render}.py` (several bindings) · `scene/` (the body USD and the script that builds it from the pinned CC0 sources) · `JOB_FORMAT.md`.
- **Hand-offs:** `docs/Planning/PlatformDependencies.md` (M1 update; a new row for the region slots) · `Phase06_UnrealTestRuntime.md` §Coupling.

## Lead calls (open)

1. **Regions: split the mesh, or paint masks?** The eye (sclera and iris), the teeth mesh (teeth and gums) and the body (skin, lips, nails) each carry more than one substance.
   - **(a) Split the mesh (recommended).** Each part gets its own article, using USD's standard geometry subsets and Blender's material slots. No contract change, every article stays usable on any mesh, and the boundaries are hard, which suits lip borders and nail edges. We split our own rig body. The platform is asked for the same slots (CM-Q9; its character contract already names slots, and "slot names are the contract").
   - **(b) Masks on the hm08 body** (a "fit set", CM-Q6). Soft boundaries, but a new contract concept, and the masks only work on that one body.
   *Recommend (a) now; (b) later for soft detail (tone, freckles, makeup) if the rig shows hard edges fall short.*
2. **Hair, brows and lashes: where does a card's cut-out come from?** A hair card's shape is pixels bound to one mesh, and the library holds no bound pixels (CM2, D1). This is the one piece of the Outcome that cannot be pure substance.
   - **(a) One new input: a cut-out map supplied when the material is bound (recommended).** The article carries the fibre (melanin colour, roughness, anisotropy, carrier C3) on the Masked master, and the mesh supplies its own alpha through a standard USD input on the material, as the Creator sliders do today. This is the first piece of a "fit". The same input later carries the iris pattern and region detail. It is a contract change (`LCDSchema.md`, `MasterSet.md`, and Phase06's Masked master).
   - **(b) A `Hair` master on MaterialX's Chiang hair model** (melanin-driven, and in Blender and Unreal too). It would be the first article that is not `open_pbr_surface` (Decision of record 1), whether USDLiveView's renderer draws it is **unverified**, and it still needs (a)'s cut-out.
   - **(c) Split hair, brows and lashes into their own phase** and ship the rest.
   *Recommend (a), with (b) probed only if Masked hair looks wrong in the rig.*
3. **The colour channel on layers (CM-Q5): keep it here, or send it back to Phase08?** If call 1 is (a), nothing in this Outcome needs it. Lips are their own substance, and freckles and makeup are not in the Outcome. Its real driver is Phase08's invisible dust (question 10). *Recommend sending it back to Phase08,* so Phase06 builds against a contract that is not about to move for it.
4. **How does Studio get these?** Today's release model cannot ship candidates: `ReleaseModel.md` requires every article in a release to be `approved` before the freeze. So Phase07 cuts no release. *Recommend:* Studio reads what the platform's deploy already copies from this repo (P2, as it does today), and a release with candidates in it is the Release Bundle phase's call. Say so if you expected a `matterlib-0.2.0`.

## Discovery Log

### Pass 1 (2026-09-27): the product docs read against the Outcome, plus two probes

**Examined:** `_Architecture.md` · `Taxonomy.md` · `MasterSet.md` · `LCDSchema.md` · `Identity.md` · `Manifest.md`, `RuntimeCatalog.md` and `ReleaseModel.md` (status) · the research (whole) · `260926_R_BigPicture_NimbleSetup.md` (BP4, Pass 8, Q-G, Q-H) · `Phase05_TestRig.md` (closed) · `Phase06` and `Phase08` seeds · `PlatformDependencies.md`. **Learnings:** `Blender.md` (B4, B5, B6), `MaterialX.md` (M4), `Storm.md` (S7): all three apply. **Tree grep for the phase's own terms** (`biological`, `makehuman`, `mpfb`, `hm08`, `fitzpatrick`, `skin`) over `tools/`, `blender/`, `MatterLibrary/` and the skills: **nothing**, so no prior phase built any of it. **Consumer docs:** not read (private); M1 and P4 name what the consumer needs.

**Probes (disposable; nothing in the repo):**
- **P1 — Blender 5.2.2 LTS Principled BSDF** (headless): it has `Subsurface Anisotropy`, `Coat Weight/Roughness/IOR/Tint/Normal`, `Sheen Weight/Roughness/Tint`, `Anisotropic`/`Tangent`, and `subsurface_method` ∈ {BURLEY, RANDOM_WALK, RANDOM_WALK_SKIN, RANDOM_WALK_LEGACY}, default RANDOM_WALK. It has no separate subsurface colour (B5 holds).
- **P2 — MPFB2's hm08 `base.obj`** (the research's clone in `/tmp/mpfb2` at `3edf9df`; not a reproduction): groups `body`, `helper-l-eye`, `helper-r-eye`, `helper-upper-teeth`, `helper-lower-teeth`, `helper-tongue`, `helper-hair`, `helper-{l,r}-eyelashes-{1,2}`, `helper-tights`, `helper-skirt`, `helper-genital`, and joint cubes. The eyes, teeth and tongue on the base mesh are **placeholders**; MakeHuman's real ones are separate meshes in the system-assets pack (research Pass 3). The CC0 region masks are in `data/textures/`.

**Findings:**
- **F1 — Skin needs no new master for its graph; it needs three lane-A inputs.** Confirmed against the tree and Blender 5.2 (P1). MasterSet already names sheen and clearcoat as Opaque params, so coat and fuzz on any master fit the spec as written.
- **F2 — Research Pass 8a's Blender gap is stale.** It was written against `matter_proxy.py`, which Phase05 retired. The Blender masters now mix subsurface colour as OpenPBR does. What is still missing: coat, fuzz, scatter anisotropy, and a subsurface method (none is set, so Blender's `RANDOM_WALK` applies).
- **F3 — "Leave `subsurface_color` unset" is wrong.** OpenPBR's default is a light grey, mixed in by weight. → Decisions, "Subsurface colour, corrected".
- **F4 — The status lifecycle already exists, on release records** (manifest → runtime catalog), and the runtime ignores it when resolving. What is missing is a status **before** a release. → D-S: recipe only.
- **F5 — Research Q-G ("status in the recipe and the `.mtlx`") conflicts with immutability after promotion and with BP4.** Q-G was a research recommendation, never ruled, so this is not a fork. → D-S.
- **F6 — An Eye master fails the LCD principle.** → D-E.
- **F7 — Hair, brows, lashes and the iris pattern are the only Outcome items that cannot be pure substance.** A card's cut-out and an iris's radial pattern are pixels bound to a mesh. → Lead call 2; split signal.
- **F8 — A new article cannot reach Blender today.** `gen_asset_library.py` builds only from `matterlib-0.1.0`'s catalog (`CATALOG`), so a candidate would never appear in the Asset Browser. USDLiveView's dev loop serves the working tree but stamps everything `draft`. **This is the Outcome's entry path, not a nicety.** → 7.2.
- **F9 — The Outcome's USD-viewer path through Stage may route by class.** M1 says Studio routes by class, so a new class renders as the missing material. Whether Stage (which USDLiveView's dev loop uses) does the same is **unverified**. → A probe in 7.2; if it does, it is M1/P4 (a platform ask), and the rig's direct renderer still satisfies "a USD viewer".
- **F10 — Candidates cannot ride a release.** `ReleaseModel.md` requires `approved` before a freeze. → Lead call 4.
- **F11 — The rig has one fixed scene** (`job.py` `SCENE`) and one article per job. The body needs a scene of its own and one binding per part. → 7.4.

**The research's open questions, disposed:** CM-Q3 → lead call 2 · CM-Q4 → D-E (answered by the LCD principle) · CM-Q5 → lead call 3 · CM-Q6 → lead calls 1–2 (the fit's home waits on whether one is needed) · CM-Q8 → answered (R13: never committed) · CM-Q9 → lead call 1 · CM-Q10 → measured in 7.3.

## Discovery Status

- **Passes captured:** 1. **The Brief is drafted; it completes when lead calls 1–4 are answered.** Calls 1 and 2 shape steps 7.4–7.6; 7.1–7.3 do not depend on any of them.
- **Checks to carry forward:** the Stage class probe (F9, in 7.2). The Chiang-hair probe, only if call 2 goes to (b). Re-download the system-assets pack at the research's recorded hash for the eye, teeth and tongue meshes: the `/tmp` copies are gone except the MPFB2 clone.

## Sources (pointers, not copies)

- `docs/Planning/Research/260927_R_CharacterMaterials_MPFB2.md`: the whole thread (pinned sources and hashes in Pass 3).
- `docs/Planning/Phases/Future/Phase08_LibraryCoverage.md`: questions 3 (carriers) and 10 (layer colour).
- `docs/Planning/Phases/Future/Phase06_UnrealTestRuntime.md`: the masters this phase's contract calls touch.
- `docs/Planning/Phases/Complete/Phase05_TestRig.md`: the rig; F13, F16.
- `docs/specs/Ontology/{Taxonomy,MasterSet}.md` · `docs/specs/Contract/LCDSchema.md` · `docs/specs/Distribution/ReleaseModel.md` · `docs/Planning/PlatformDependencies.md` (M1, P4).

## Execution Log

_(populated during execution)_
