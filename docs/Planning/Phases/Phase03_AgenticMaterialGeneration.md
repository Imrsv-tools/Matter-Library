# Phase03 — Agentic Material Generation

**Status:** IN EXECUTION (2026-09-25). Discovery closed at Pass 3: the Brief was re-cut for the lead's *smart, not lean* ruling (research D8 / C1), and Q2 was ruled A by the lead (2026-09-25). Numbered by the lead ("yes, start discovery as Phase03"), naming the Roadmap's *Agentic Material Generation* entry. **Lane: `build`** (verified: §Risk lane).

## Outcome

**A maintainer can ask an agent for new materials and receive validated candidates, with recorded provenance, ready for human judgement.**

*(Verbatim from the Roadmap entry, written at Phase01 step 1.5.)*

---

## The Brief

### First human test

There is no running service. The surface is **Claude Code at the repo root**, plus the files a run leaves in the working tree.

1. `/matter-generate an 18% grey card`
   - The skill states its plan: taxonomy slot `utility/virtual`, declared master `Opaque` and why, the name `GreyCard_Neutral18_Clean_Base_s01_v01` (six tokens, one per axis), lane L1, the Physically Based entry it will use (`Gray Card`), and **no wear layers, because a reference article stays pure** (the one exemption in C1).
   - It writes the recipe, assembles the `.mtlx`, and runs `uv run tools/validators/run_all.py`, which shows every lane PASS or SKIP, 0 FAIL.
   - It renders the article and shows the render with a short critique note. *(step 3.1)*
2. **The lead judges.**
   - Look at the render. For a closer look, run the command the skill prints to open the draft's preview scene in **USDLiveView** (`usdliveview <Stem>_preview.usda`) and fly or orbit around it. That is the same OpenUSD 26.03 + MaterialX 1.39.5 Storm stack, with no Stage and no release needed (Pass 2).
   - Keep it (`git add` the named paths and commit) or discard it (`git restore` / `git clean` on the named paths). The skill never commits.
   - **Time the review.** That is the phase's one measurement (research Pass 11 estimated 5–10 minutes per article, unmeasured).
3. Edit the new recipe so one key is misspelled (e.g. `roughnes_const`), and run the one command → the **recipe** lane FAILs and names the unknown key. Put a class that isn't in the taxonomy → FAIL. Put an albedo above 1 → FAIL. Point an overlay at a texture that doesn't exist → FAIL. Undo the edits → green again. *(step 3.2)*
4. `/matter-generate green bottle glass` → `Glass_Green_Clean_Base_s01_v01` (`TranslucentThin`, L1, `Glass (Soda-lime)`, IOR 1.52, with an authored green `transmission_color`, since a see-through colour is its own article, E2). The skill states the wear layers it will carry: overlays `Scratches01 · Dust01 · Fingerprints01`, mask `Grime01`, every slider at 0. It finds **`Fingerprints01` missing from the shared library**. So it writes a fixed-seed generator for that one packed-data overlay, runs it, and records provenance as `procedural` with the script as evidence **in its `library/provenance/sources/` record (Q2 = A)**. It then assembles the glass with all four layers, gates, renders and critiques. **Also look at the layer itself:** the critique shows the glass with the new overlay dialled up, so the lead judges the layer as well as the article. *(step 3.3)*
5. `/matter-generate white oak` → `WhiteOak_Natural_Clean_Base_s01_v01`. The skill picks an ambientCG set and shows its id and page. It fetches the set and writes 1K textures (NormalGL) under `MatterLibrary/textures/base/natural/wood/`. It records provenance with the sha256 evidence **in its `library/provenance/sources/` record (Q2 = A)** and adds a `CREDITS.md` row. Its overlay 1, `Scuffs01`, is missing, so step 3.3's layer path makes it first. Then it assembles, gates, renders and critiques. *(step 3.4)*
6. *(If step 3.5 lands)* `/matter-generate earthenware` → `Earthenware_Natural_Clean_Base_s01_v01`. The skill writes a fixed-seed generator for the **base** texture set (colour, roughness, normal), runs it, and records provenance as `procedural`. Any missing layers (`EdgeWear01`, `Crevice01`) come from 3.3's path. The rest is as in click 1. *(step 3.5)*

**Reconciled click by click:** click 1 needs the skill, the Physically Based lookup, the assembler (existing), the gate (existing) and a working render, so the preview repair is **inside 3.1**, not after it. Click 1 is deliberately a reference article: **every other article in the draft list needs at least one wear layer that isn't in the library yet** (measured below, Pass 3). A glass first click would make step 3.1 carry layer generation too, and C1 rules out leaving the layer off. So the test got smaller, not step 3.1 bigger. Click 2 needs nothing new. Click 3 is step 3.2's guards. Click 4 is step 3.3: layer generation, plus the third overlay slot that C2 already landed (§Decisions). Click 5 is step 3.4's importer, and it consumes 3.3's layer path. Click 6 is step 3.5.

### In now

- **The skill** `/matter-generate`. It follows the human path in `CONTRIBUTING.md` step for step (name → place → recipe → assemble → gate): plan → ground → **assign layers** → recipe → assemble → gate → render → self-critique → a `draft` left in the tree.
- **A layer assignment for every article (D8 / C1).** The skill carries every wear layer relevant to the matter, up to the cap: overlay 1 is the damage layer and overlays 2–3 are the rest (C5, E1). It adds one gating mask and sets every slider to 0. It states the choice and its reason in the plan. The draft list in `260925_R_LibraryCoverage_FirstRelease.md` is a **reference, not an authority**: it is research, and "nothing is committed".
- **Generating a missing wear layer (step 3.3).** When a relevant layer isn't in `MatterLibrary/textures/shared/`, the skill makes it: a fixed-seed packed-data generator, one script per layer, on the `gen_shared_textures.py` pattern. Only the layers this phase's briefs need are made (§Not now).
- **Physically Based grounding** (CC0, licence verified in the repo's `LICENSE`). The recipe records which entries its constants came from (research O6).
- **A working preview render**: repair `tools/preview_generators/` so it renders a real article headless to a PNG (§Pass 1, P3).
- **Harness guards:**
  - G1: unknown recipe keys are rejected;
  - G2: a recipe schema the agent authors against;
  - G3: the class is in the taxonomy;
  - G5: the recipe's `path` agrees with its domain, class and name;
  - G6: physical plausibility;
  - G7: the layer assignment is well-formed. Every overlay and mask path resolves to a file under `textures/shared/`, the overlay count is within the assembler's cap, a mask is present only where overlays or a second layer exist (otherwise it is a dead control), and a `utility/virtual` article carries none.

  They run in a new **recipe** lane. G4 is dropped as a gate (§Decisions). **Whether a layer is *relevant* is judgement, not a gate:** it is the skill's stated rationale plus the lead's review, the same split as for the declared master.
- **ambientCG import (L3)**: fetch, channel map, resize to 1K, provenance evidence, a `CREDITS.md` row.
- **Agent-written procedural base textures (L2)** as step 3.5. This is the step to cut if time runs short (D4 says "next"). The layer generators in 3.3 are the same technique applied to data textures, and they **can't** be cut, because C1 makes every non-reference article need them.

### Not now

- **Filling the library.** The ~170-article coverage push belongs to *Library Coverage*. It **consumes from this phase:** the `/matter-generate` skill, the recipe schema and the recipe lane (with G7), the layer-generation path, the ambientCG importer, and the preview render.
- **Producing the whole wear-layer library.** It grows from 5 to 22 layers in the research draft. That run is *Library Coverage*, which uses 3.3's layer path. This phase makes only the layers its own briefs need (`Fingerprints01`, `Scuffs01`, plus `EdgeWear01` and `Crevice01` if 3.5 lands).
- **Landing the third overlay (C2).** Done separately in `001a857` (§Decisions); this phase consumes the cap and never hard-codes it.
- **Re-versioning shipped articles that lack layers** (research L8, E3) and **what `Clean`/`Detail` mean for slider defaults on shipped articles** (research N8). Those belong to *Version Management* and *Library Coverage*. New drafts follow C1: `…_Clean_Base`, every slider at 0.
- **Localised colour or gloss** (moss only in crevices; research L7): a refinement, not a gap.
- **Generative imagery (L4)**: parked (R13, D4).
- **A batch agent and the Matter Manager** (D5).
- **OpenPBR carriers C1–C3** (metal F82, sheen/coat, anisotropy). The Outcome asks for *candidates ready for judgement*, not full fidelity for every class. The skill **says so** in its critique when a material wants a carrier it can't express (for example "brushed: no anisotropy").
- **Moving drafts to `candidate` or into a release**, and any change to `library/releases/`: that is the maintainer, then *Version Management*.
- **Assemblies** (D1). **Skin and hair** (research O9 / PlatformDependencies M1). **LFS budget and 2K textures** (research O12): a handful of briefs does not need them.

### Reuse check: what the stack already provides

| Need | Native answer | Custom layer? |
|---|---|---|
| Emit a valid Matter `.mtlx` | `tools/converters/assemble_mtlx.py` + `build_proof_subset.py` (deterministic) | **None.** The agent writes a recipe, never MaterialX. |
| Validate a draft | `run_all.py`: the `materials` lane covers every `.mtlx` and the `determinism` lane every recipe, so **drafts are gated automatically** (read 2026-09-23) | **One new lane, `recipe`** (G1/G2/G3/G5/G6). No lane checks recipes today. |
| Render for review | `usdrecord` (OpenUSD 26.03 on the lead's box) + `make_preview.py` | **A repair, not a new tool.** The wrapper has three defects (P3). |
| Judge the render | **The Claude Code session itself reads the PNG.** No model API, no keys. | None |
| The lead's close look | **USDLiveView** (a consumer viewer, working on the lead's box 2026-09-23) opens a `.usd`/`.usda` scene directly, with no Stage connection, on the same render stack | **None.** The skill writes the preview scene anyway (for the PNG) and prints the command to open it. It never launches a window itself. |
| Physical values | Physically Based API `api.physicallybased.info/v2/materials`: 116 records, CC0 | A small lookup script, so the grounding is repeatable and cited |
| Textures | ambientCG `…/get?file=<Id>_1K-PNG.zip`: maps named `_Color`, `_Roughness`, `_NormalGL`, `_Metalness`, `_Opacity` | An importer (fetch, map, place, evidence). ambientCG's own bundled `.mtlx` is **not** reusable: it is a flat OpenPBR graph with no LCD interface inputs (read in the zip, P2). |
| Wear layers | `tools/converters/gen_shared_textures.py`: fixed-seed value noise packed to the frozen channel contract (R/G normal XY · B roughness bias · A density). The shipped `Dust01`/`Scratches01` come from it and are recorded `source: procedural`, `evidence: <script>` in the lock | **The same pattern, one script per new layer.** Re-running the shared script would regenerate the shipped layers (§Build Safety). |
| Provenance evidence | `tools/validators/source_provenance.py compute <texture-id> <url>` prints the `{url, sha256_scope, sha256, files}` block | None for the evidence. **Where it is stored: Q2 = A, a per-texture-set record.** |
| Run a guided procedure | a Claude Code **project skill** (`.claude/skills/<name>/SKILL.md`) | The skill is thin: every deterministic step is a script in `tools/`, so a human, a later batch agent (D5) and the Matter Manager reuse the same tools. |

### Decisions that bind

- **Research D1–D8** (`docs/Planning/Research/260923_R_AgenticMaterialGeneration.md` §Resolved). This is the authoritative copy of them; they are not repeated here. **D8 in the lead's words:** "We are building and testing complex materials, not just a bunch of wood textures" (ruling C1, `260925_R_LibraryCoverage_FirstRelease.md`). Every article carries all its relevant layers, sliders at 0, and names don't change. "Leaving out a relevant layer is not an option."
- **Names are six fixed axes** (C4/C5, landed in `Identity.md`; the `materials` lane enforces exactly six tokens since quick fix `2b292be`): Material = the matter or species, Variant = the look (default `Natural`), Condition = damage (overlay 1), Detail = the rest (overlays 2–3). **Research L10 (enforce six tokens) is therefore done, and it is not a Phase03 guard.**
- **The third overlay (C2) is consumed, not built here. It landed in quick fix `001a857` (2026-09-25, lead-directed)**: `MAX_OVERLAYS = 3`, the Creator port `overlay3_density`, the `overlay3_tex` node, and the maskset's A channel as the overlay-3 gate. The maskset loads `color4` only on a 3-overlay article, so articles with ≤ 2 overlays assemble byte-identically. G7 reads the cap from the assembler and never hard-codes it. Click 4 uses the third slot (`Fingerprints01` on the glass). The consumer side is `PlatformDependencies.md` P12, not this phase.
- **The recipe is the only thing the agent authors** (research Pass 2). No hand-written `.mtlx`, as `CONTRIBUTING.md` step 3 says for humans too.
- **Normal maps come from ambientCG's `NormalGL`** (P1: the shipped Limestone normal is **byte-identical** to `Travertine009_1K-PNG_NormalGL.png`; the green channel correlates +1.0 with GL and −1.0 with DX).
- **Textures ship at 1K**, as all existing textures do (measured 1024²). They sit **flat in the class folder** as `<Set>_<channel>_<sNN>.png` (measured). `ToolingConventions.md`'s `…/<class>/<Set>/` is a doc drift; fix it at doc sync.
- **Declared master (D2) is checked structurally, not by lookup.** The `materials` lane's master-conformance check already fails a declared master whose defining carriers are missing (Masked without an opacity source, Thick without depth…). Whether a master *fits the material* is the skill's stated rationale plus the lead's judgement. **G4 as a class lookup is dropped**, because it would reintroduce class routing.
- **The skill never commits, never pushes, never touches `library/releases/`.** It never regenerates an existing texture (`AI_WorkingAgreement.md` §Build Safety).
- **Attribution (R8):** the committing maintainer is the author. `CREDITS.md` gets a texture-source row per ambientCG set, as the existing three have.

### Risk lane: `build` (verified)

The one control this phase goes near is the **shipped-pixel rule**, enforced by `_validate_provenance` in `tools/validators/validate_manifest.py`. **Read:** it fires only for `candidate`/`approved` textures in a release lock (`if status in PROMOTED`), so a draft does not reach it, by design. This phase writes no release record.
- The residual risk is **committing a non-CC0 pixel to a public repo**. It is controlled by the importer fetching from **one allowlisted source** (ambientCG, whose licence page was read: CC0 1.0, "copy, modify, distribute… without asking permission") and by **the lead's own commit and push**.
- No authorization, secrets, destructive migration, data loss or served edge is involved. So: **build**.

### Step list

| Step | What a person can do at the end | Intent |
|---|---|---|
| **3.1** | Ask for a **param-only reference** material and get a validated, rendered draft (clicks 1–2) | The skill, including its layer-assignment step (which rightly assigns none here); the Physically Based lookup; recipe `sources`; the preview repaired to render a PNG headless; the critique note |
| **3.2** | See a bad recipe **refused** by the one command (click 3) | The `recipe` lane: G1 strict keys (also in `MaterialSpec.from_dict`), G2 schema (layer fields included), G3 taxonomy, G5 path agreement, G6 plausibility, G7 layer assignment, with RED fixtures so the lane is shown both ways; the skill authors against the schema |
| **3.3** | Ask for a **layered** material whose wear layer doesn't exist yet, and get the layer **and** the article (click 4) | A fixed-seed packed-data generator per missing layer; `procedural` provenance (Q2); a render with the layer dialled up; the article with its full layer set, using the third overlay slot (C2, landed) |
| **3.4** | Ask for a **textured** material and get it from a CC0 scan (click 5) | The ambientCG importer; provenance recorded (Q2); a `CREDITS.md` row; its missing overlay 1 made through 3.3's path |
| **3.5** | Ask for a material the scans don't cover and get **generated** base textures (click 6) | Agent-written fixed-seed base-texture generators (L2); `procedural` provenance. **The cut line** if the phase runs long |

Close acceptance: four real briefs, the reference (3.1), the layered glass (3.3), the scanned oak (3.4) and, if it lands, the generated earthenware (3.5). Each is kept or discarded by the lead, with the **review minutes recorded** in §Execution Log. A generated layer is judged along with the first article that carries it.

### Compact build map

- `.claude/skills/matter-generate/SKILL.md`: **new root.** Add it to `ToolingConventions.md` (the `.claude/` row says "agent surface"; the lanes rule makes only `.claude/CLAUDE.md` read-only to working verbs, and the skill is this phase's *product*, not methodology).
- `tools/converters/`:
  - a Physically Based lookup script;
  - the ambientCG importer (3.4);
  - the layer generators (3.3): one fixed-seed script per new layer, writing only its own `MatterLibrary/textures/shared/{overlays,masks}/` file, so the provenance evidence names exactly one script. Its home is ruled at 3.3 against `ToolingConventions.md`. It must not be `tools/generators/`, which is the Blender asset-library generator;
  - `recipes/<Stem>_vNN.json` (the existing home, per `ToolingConventions.md`, and globbed by `build_proof_subset.py` and the determinism lane);
  - the recipe JSON Schema (G2).
- `tools/converters/assemble_mtlx.py` `MaterialSpec.from_dict`: G1 rejects unknown keys, with an explicit allow-list for metadata keys (`_comment`, `path`, `sources`). **The 12 existing recipes must still assemble byte-identically** (determinism lane).
- `tools/validators/`: the new `recipe` lane in `run_all.py` (17 lanes) plus `fixtures/` RED recipes.
  - G3's class list mirrors `Taxonomy.md`, the same pattern as `LCD_PORTS` mirroring `LCDSchema.md`.
  - G6 exempts `utility/virtual` and the `system` master (the UV grid and magenta are deliberately unphysical).
  - G7 must stay green on the 12 shipped recipes. **It does not gate slider defaults.** The shipped Glass ships with its wear dialled up (0.25 / 0.35 / 0.6) while Concrete ships at 0, and which is right is research N8, still open. The skill authors 0 (C1); the lane doesn't enforce it.
  - Physically Based linear colours above 1.0 (e.g. Gold `1.059`) are **clamped at lookup**, not accepted by the lane.
- `tools/preview_generators/`:
  - repair `preview_wrapper.usda` and `make_preview.py`: reference `</MaterialX>`, apply `MaterialBindingAPI`, use a UV-mapped mesh, add a camera;
  - add a render-to-PNG option via `usdrecord`, run inside the USD toolchain env (`USD_TOOLS_ROOT`, `USD_TOOLS_ENV`, `activate-usd-tools.sh`);
  - the working recipe is in §Pass 1, P3.
  - **Keep the preview `.usda` beside the PNG** (in a gitignored or temp location, not committed) so the lead can open it in USDLiveView. Its location is a per-box pointer with no default, the same pattern as `USD_TOOLS_ROOT`. The skill prints the command when the pointer is set, and prints just the scene path when it isn't.
  - Metals render dark under a textureless dome: a lighting rig with an environment is an execute-level improvement. A CC0 HDRI would itself be a third-party input under R13.
- **Doc sync at close:**
  - `AuthoringHarness.md` (tools, lanes, the preview repair; stages A→B partly in-repo);
  - `AuthoringGoldenPath.md` §Future-toolchain note;
  - `ToolingConventions.md` (skill root, the layer-generator home, texture layout drift, the 17th lane);
  - `tools/preview_generators/README.md`;
  - `CONTRIBUTING.md` (point at the skill as an option).

---

## Lead calls

| # | Call | Recommendation |
|---|---|---|
| **Q2** — ✅ **RULED A** (lead, 2026-09-25: "Great... lets do it", answering the recommendation below) | **Where does a draft texture set's provenance live before a release pins it?** The release lock is where provenance is enforced, but it only exists at promotion. A working next-release lock would drag in the catalog, freeze and staging lanes, which run on the newest release (read in `run_all.py`): that is *Version Management*'s territory. Options: **A** a per-texture-set record `library/provenance/sources/<domain>/<class>/<Set>.yaml`, holding exactly the `provenance:` block the lock will later carry (from `source_provenance.py compute`, or `procedural` + script path); **B** a `provenance` block inside the recipe. *(Pass 3: it now also covers a **generated wear layer**, e.g. `library/provenance/sources/shared/overlays/Fingerprints01.yaml`. A layer is shared by many articles, so it has no single recipe to live in under B. It is first needed at step 3.3; 3.1–3.2 can run without it.)* | **A.** Provenance belongs to the *texture*, which is versioned and shared independently of any one article (the manifest has separate texture entries, and overlays and masks are shared by several articles). `library/provenance/` is already the home for provenance records. A cannot sit beside the PNGs, because `.gitattributes` puts everything under `MatterLibrary/textures/**` in LFS. |

---

## Discovery Log

### Pass 1 (2026-09-23): specs top-down, anchored on the Outcome, plus three probes

**Examined:**
- `_Architecture.md` → `MasterSet.md`, `Taxonomy.md`, `Manifest.md` (in full), `AuthoringHarness.md`, `AuthoringGoldenPath.md`, `MaterialXTemplate.md`;
- `ToolingConventions.md`; `AI_WorkingAgreement.md` §No Workarounds, §Build Safety, §Project practices;
- `CONTRIBUTING.md`, `CREDITS.md`, `.gitignore`, `.gitattributes`, `.claude/`;
- code: `validate_manifest.py` (status and provenance paths), `run_all.py` (lane selection), `source_provenance.py`, `assemble_mtlx.py` (normal path), `make_preview.py` and its template;
- the research doc (D1–D7, Passes 1–12).

**Learnings:** `docs/Learnings/` holds no domain yet (only its README). This is a discharged read, not a skipped one. **Tree grep for the phase's name:** only the research doc, the Roadmap and this doc (nothing half-built).

**Findings:**
- **P1: normal convention, Confirmed.** Downloaded `Travertine009_1K-PNG.zip` (the recorded source of `Limestone_Veined`). The shipped normal is **byte-identical** to `_NormalGL.png` (`cmp`), and the green channel correlates +1.0 with GL and −1.0 with DX. MaterialX's `normalmap` spec states no convention; the library's evidence decides.
- **P2: ambientCG's zip ships an OpenPBR 1.39 `.mtlx`, `.usdc`, `.blend` and `.tres`.** Its `.mtlx` is a flat node graph (tiledimage → `open_pbr_surface`, plus displacement) with **no LCD interface inputs**, so it fails our template contract. It is reusable only as a cross-check of the channel mapping.
- **P3: the preview tool could not render a real article. Repaired in a probe; the render capability is Confirmed.**
  - `make_preview.py`'s wrapper rendered **solid white**, for three reasons:
    1. the article layer has **no `defaultPrim`**, so the bare file reference is unresolved; the reference needs `</MaterialX>`;
    2. USD 26.03 ignores `material:binding` without **`MaterialBindingAPI`**;
    3. the implicit `Sphere` has **no UVs**, so a textured article renders as one flat colour.
  - With all three fixed and a camera added, `usdrecord` rendered Limestone and Copper **headless and textured in about 1 s each**, and the session read the PNGs back.
  - The README's "degraded path (no pxr)" explains why this was never caught.
  - The preview tool is also the seed for *Parity Baselines*.
- **P4:** drafts are covered by the existing gate for free (`materials` and `determinism` glob the whole tree). No lane validates *recipes*, and `from_dict` silently drops unknown keys (research G1, re-read).
- **P5:** a draft is exempt from the provenance gate by design (`validate_manifest.py` checks only `PROMOTED` statuses). The Outcome still says "with recorded provenance", which makes Q2 necessary.

**Seed questions, four-tested:**

| Seed Q | Verdict |
|---|---|
| Q1 skill home | **Answered** (test 1): harness convention plus `ToolingConventions.md`'s `.claude/` agent-surface row. The lanes rule names only `.claude/CLAUDE.md`. Build map. |
| Q2 draft provenance | **Fork: lead call** (necessary per P5; deliverable; admissible). **Ruled A** (lead, 2026-09-25). |
| Q3 download scratch | **Answered** (test 1): `source_provenance.py` attests the *shipped* set, not the upstream download, so the raw zip is disposable (a temp dir). The pin is the asset id + URL + shipped-set sha256. |
| Q4 normal convention | **Answered** by probe P1: `NormalGL`. |
| Q5 recipe home | **Answered** (test 1): `ToolingConventions.md`, `tools/converters/recipes/<Stem>_vNN.json`. |
| Q6 carriers C1–C3 | **Fails test 2 (not necessary):** the Outcome is *candidates ready for judgement*. Not now; the skill states the limitation. |
| Q7 risk lane | **Answered:** `build` (§Risk lane, verified in `validate_manifest.py`). |
| Q8 research leftovers | O5 → Q6. O6 → in (recipe `sources`). O7 → **answered** by R8 and `CREDITS.md`. O12 → not now. |

<details><summary>Reproduction: the probes (disposable; the environment was torn down, the recipe is kept here)</summary>

Normal convention (P1), using the repo's `.venv`:

```sh
curl -sL -o t.zip "https://ambientcg.com/get?file=Travertine009_1K-PNG.zip" && unzip -q t.zip
cmp Travertine009_1K-PNG_NormalGL.png MatterLibrary/textures/base/natural/stone/Limestone_Veined_normal_s01.png && echo IDENTICAL
```

Headless render (P3), inside the USD env (`conda activate $USD_TOOLS_ENV; source tools/usd-toolchain/activate-usd-tools.sh`), then `usdrecord --camera /World/Cam --imageWidth 512 out.usda out.png`:

```python
# uvsphere.py <article.mtlx> <out.usda>: UV sphere + article + lights + camera
import math, sys
from pxr import Usd, UsdGeom, UsdShade, UsdLux, Sdf, Gf
mtlx, out = sys.argv[1], sys.argv[2]; name = mtlx.rsplit('/', 1)[1][:-5]
st = Usd.Stage.CreateNew(out); st.SetMetadata('upAxis', 'Y'); UsdGeom.Xform.Define(st, '/World')
st.DefinePrim('/World/Library').GetReferences().AddReference(mtlx, '/MaterialX')   # no defaultPrim
UsdLux.DomeLight.Define(st, '/World/Dome').CreateIntensityAttr(1.0)
k = UsdLux.DistantLight.Define(st, '/World/Key'); k.CreateIntensityAttr(3.0); UsdGeom.XformCommonAPI(k).SetRotate((-35, 30, 0))
U, V = 64, 32; pts, uvs, idx = [], [], []
for j in range(V + 1):
    for i in range(U + 1):
        u, v = i / U, j / V; th, ph = u * 2 * math.pi, v * math.pi
        pts.append(Gf.Vec3f(math.sin(ph) * math.cos(th), math.cos(ph), math.sin(ph) * math.sin(th))); uvs.append(Gf.Vec2f(u * 2, 1 - v))
for j in range(V):
    for i in range(U):
        a = j * (U + 1) + i; b = a + U + 1; idx += [a, a + 1, b + 1, b]
m = UsdGeom.Mesh.Define(st, '/World/Ball'); m.CreatePointsAttr(pts); m.CreateFaceVertexCountsAttr([4] * (U * V))
m.CreateFaceVertexIndicesAttr(idx); m.CreateSubdivisionSchemeAttr('none')
UsdGeom.PrimvarsAPI(m).CreatePrimvar('st', Sdf.ValueTypeNames.TexCoord2fArray, UsdGeom.Tokens.vertex).Set(uvs)
UsdShade.MaterialBindingAPI.Apply(m.GetPrim()).Bind(UsdShade.Material(st.GetPrimAtPath(f'/World/Library/Materials/{name}')))
c = UsdGeom.Camera.Define(st, '/World/Cam'); c.CreateFocalLengthAttr(50); UsdGeom.XformCommonAPI(c).SetTranslate((0, 0, 7.5))
st.Save()
```

The render opens no window that was observed. It uses Qt xcb on `DISPLAY` (the toolchain's documented GL fix), so **isolation from the lead's desktop is not verified**. Check at step 3.1.
</details>

### Pass 2 (2026-09-23): the review surface. The lead: "USDLiveView is working now."

**Examined:** USDLiveView's public-facing surfaces on the lead's box (its setup guide, orientation, launcher help text, its completed Apply-Materials phase). **Recorded here: only the consumer-side facts this phase needs.** USDLiveView is a private repo, and nothing of its internals is copied into this one.

**Findings:**
- **It opens a plain `.usd`/`.usda` file,** not only an IMRSV composition. Without a Stage connection it simply views the file. It renders on the same OpenUSD 26.03 + MaterialX 1.39.5 Storm stack as `usdrecord` (P3), so what the lead sees agrees with what the agent critiqued.
- **Its material *picker* lists a release catalog served by Stage.** A draft, which is in no release, never appears there. **So a draft is reviewed by opening its preview scene, not through the picker.** No platform dependency arises.
- **Its Matter root may be a Matter-Library checkout.** A composition that references a draft by name would also resolve. That is not needed for this phase's review, so it is not used.

**Decision (within the Brief, not a lead fork):** USDLiveView is the lead's **optional close-look surface** at click 2. The skill writes the preview scene it already needs for the PNG, keeps it, and prints the command to open it. It never launches the GUI itself: no surprise windows, and the agent never blocks on an interactive app. **Unverified until step 3.1:** opening a repaired preview scene in USDLiveView shows the draft textured. The first click proves it.

### Pass 3 (2026-09-25): what landed since, and "smart, not lean"

**Examined:** every commit since Pass 2 (`679cc72..2b292be`). That includes:
- the Library Coverage research in full where it touches this phase: rulings C1–C6, E1/E2/E5, Passes 4–7, L6–L10, and the per-class tables for glass, wood, ceramic and utility;
- the `Identity.md`, `NamingConventions.md`, `MaterialXTemplate.md` and `MasterSet.md` diffs;
- research D8;
- `assemble_mtlx.py` (the roughness clamp, `MAX_OVERLAYS`, maskset `color4`);
- `gen_shared_textures.py`, and the lock's provenance for `Dust01`;
- the Physically Based API (116 records; `Gray Card`, `Glass (Soda-lime)`, `Terracotta`, `Spectralon`, `Musou Black` present).

**Findings:**
- **P6: D8 / C1 widens the phase, as the research flagged ("`/discovery Phase03` should pick that up").** The skill must author a layer assignment; G2 must cover it, and a new G7 checks its structure.
- **P7: no ordinary brief can be built from today's layers.** Of 173 draft-list rows, the only ones whose relevant layers all exist are the shipped `Copper_Verdigris` and the 5 layer-free `utility/virtual` references (measured with a script over the tables). So layer generation can't stay behind the cut line. It moved from old step 3.4 to a new step 3.3, and click 1 became a reference article (§Reconciled).
- **P8: C2 (third overlay) was landed by a sibling unit during this pass** (quick fix `001a857`; it was seen live and uncommitted first, then re-checked at commit). No fork: this phase consumes the cap. Its verification recorded `run_all` at 14 PASS / 2 SKIP / 0 FAIL.
- **P9: the six-token guard (L10) landed in `2b292be`.** The first human test's names were rewritten to the C5 axes. "worn oak planks" became "white oak": "planks" is an assembly (D1), and "worn" would pre-dial a slider, which is N8's open question.
- **P10: the roughness clamp (Issue #1) changed the assembler's output for 10 articles**, which were regenerated in place. The "12 recipes assemble byte-identically after G1" check now means byte-identical to **today's** committed `.mtlx`, not to the Pass 1 bytes.

**Seed questions from this pass, four-tested:**

| Question | Verdict |
|---|---|
| Which unit lands C2? (research L6) | **Fails test 2 (not necessary):** a sibling landed it (P8). |
| Does Phase03 make all 17 new layers? | **Answered** (test 1) by the structurally identical Pass 1 ruling that filling the library is *Library Coverage*'s job. This phase makes only its briefs' layers. |
| Should G7 gate slider defaults at 0? | **Fails test 3 (not deliverable)** without breaking shipped Glass/Copper, and the rule itself is open research N8. The skill authors 0; nothing gates it. |
| Is the draft list the authority for layer choice? | **Answered** (test 1): the research says "nothing is committed". It is a reference, and the skill's rationale plus the lead decide. |

## Discovery Status

- **Passes captured:** 3 (2026-09-23 → 2026-09-25).
- **Pass 3:** the Brief was re-cut for D8 / C1. There are now 5 vertical steps: the reference article → guards (with G7) → layer generation plus the layered glass → the ambientCG oak → L2 base textures, the cut line. Lane unchanged (`build`: nothing new touches a control). Q2 now also covers generated layers.
- **Current working direction:** the Brief above, with its first click at step 3.1.
- **Open decisions:** none. Q2 was ruled **A** (lead, 2026-09-25: "Great... lets do it"): a per-texture-set record at `library/provenance/sources/<domain>/<class>/<Set>.yaml`, and for shared layers `library/provenance/sources/shared/{overlays,masks}/<Name>.yaml`.
- **Dependencies:** none open. C2 landed in `001a857`.
- **Checks to carry forward:**
  - re-verify that the 12 existing recipes assemble byte-identically **to today's committed `.mtlx`** after G1 and G7 (P10);
  - Pass 2's "USDLiveView shows the draft textured" is now proved at **click 4 or 5**, not click 1, because the grey card has no texture. Click 1 proves only that the scene opens;
  - confirm the skill loads from `.claude/skills/` (the first click proves it);
  - confirm the headless render opens no desktop window;
  - fix `ToolingConventions.md`'s texture-layout drift at doc sync.

## Execution Log

_(populated during execution)_
