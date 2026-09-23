# Phase03 — Agentic Material Generation

**Status:** ACTIVE: discovery. Pass 1 is done (2026-09-23), and **the Brief is complete except for one lead call (Q2).** Numbered by the lead ("yes, start discovery as Phase03"), naming the Roadmap's *Agentic Material Generation* entry. **Lane: `build`** (verified: §Risk lane).

## Outcome

**A maintainer can ask an agent for new materials and receive validated candidates, with recorded provenance, ready for human judgement.**

*(Verbatim from the Roadmap entry, written at Phase01 step 1.5.)*

---

## The Brief

### First human test

There is no running service. The surface is **Claude Code at the repo root**, plus the files a run leaves in the working tree.

1. `/matter-generate soda-lime window glass`
   - The skill states its plan: taxonomy slot `engineered/glass`, declared master `TranslucentThin` and why, a grammar-valid name, a scale tag, lane L1, and the Physically Based entries it will use (`Glass (Soda-lime)`, IOR 1.52).
   - It writes the recipe, assembles the `.mtlx`, and runs `uv run tools/validators/run_all.py`, which shows every lane PASS or SKIP, 0 FAIL.
   - It renders the article and shows the render with a short critique note. *(step 3.1)*
2. **The lead judges.**
   - Look at the render. For a closer look, run the command the skill prints to open the draft's preview scene in **USDLiveView** (`usdliveview <Stem>_preview.usda`) and fly or orbit around it. That is the same OpenUSD 26.03 + MaterialX 1.39.5 Storm stack, with no Stage and no release needed (Pass 2).
   - Keep it (`git add` the named paths and commit) or discard it (`git restore` / `git clean` on the named paths). The skill never commits.
   - **Time the review.** That is the phase's one measurement (research Pass 11 estimated 5–10 minutes per article, unmeasured).
3. Edit the new recipe so one key is misspelled (e.g. `roughnes_const`), and run the one command → the **recipe** lane FAILs and names the unknown key. Put a class that isn't in the taxonomy → FAIL. Put an albedo above 1 → FAIL. Undo the edits → green again. *(step 3.2)*
4. `/matter-generate worn oak planks` → the skill picks an ambientCG set and shows its id and page. It fetches the set and writes 1K textures (NormalGL) under `MatterLibrary/textures/base/natural/wood/`. It records provenance **(where: Q2)** with the sha256 evidence, adds a `CREDITS.md` row, then assembles, gates, renders and critiques. *(step 3.3)*
5. *(If step 3.4 lands)* `/matter-generate hand-made terracotta` → the skill writes a fixed-seed texture generator script, runs it, and records provenance as `procedural` with the script as evidence. The rest is as in click 1. *(step 3.4)*

**Reconciled click by click:** click 1 needs the skill, the Physically Based lookup, the assembler (existing), the gate (existing) and a working render, so the preview repair is **inside 3.1**, not after it. Click 2 needs nothing new. Click 3 is step 3.2's guards. Click 4 is step 3.3's importer. Click 5 is step 3.4.

### In now

- **The skill** `/matter-generate`. It follows the human path in `CONTRIBUTING.md` step for step (name → place → recipe → assemble → gate): plan → ground → recipe → assemble → gate → render → self-critique → a `draft` left in the tree.
- **Physically Based grounding** (CC0, licence verified in the repo's `LICENSE`). The recipe records which entries its constants came from (research O6).
- **A working preview render**: repair `tools/preview_generators/` so it renders a real article headless to a PNG (§Pass 1, P3).
- **Harness guards:**
  - G1: unknown recipe keys are rejected;
  - G2: a recipe schema the agent authors against;
  - G3: the class is in the taxonomy;
  - G5: the recipe's `path` agrees with its domain, class and name;
  - G6: physical plausibility.

  They run in a new **recipe** lane. G4 is dropped as a gate (§Decisions).
- **ambientCG import (L3)**: fetch, channel map, resize to 1K, provenance evidence, a `CREDITS.md` row.
- **Agent-written procedural generators (L2)** as step 3.4. This is the step to cut if time runs short (D4 says "next").

### Not now

- **Filling the library.** The ~170-article coverage push belongs to *Library Coverage*. It **consumes from this phase:** the `/matter-generate` skill, the recipe schema and the recipe lane, the ambientCG importer, and the preview render.
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
| Provenance evidence | `tools/validators/source_provenance.py compute <texture-id> <url>` prints the `{url, sha256_scope, sha256, files}` block | None for the evidence. **Where it is stored is Q2.** |
| Run a guided procedure | a Claude Code **project skill** (`.claude/skills/<name>/SKILL.md`) | The skill is thin: every deterministic step is a script in `tools/`, so a human, a later batch agent (D5) and the Matter Manager reuse the same tools. |

### Decisions that bind

- **Research D1–D7** (`docs/Planning/Research/260923_R_AgenticMaterialGeneration.md` §Resolved). This is the authoritative copy of them; they are not repeated here.
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
| **3.1** | Ask for a **param-only** material and get a validated, rendered draft (click 1–2) | The skill; the Physically Based lookup; recipe `sources`; the preview repaired to render a PNG headless; the critique note |
| **3.2** | See a bad recipe **refused** by the one command (click 3) | The `recipe` lane: G1 strict keys (also in `MaterialSpec.from_dict`), G2 schema, G3 taxonomy, G5 path agreement, G6 plausibility, with RED fixtures so the lane is shown both ways; the skill authors against the schema |
| **3.3** | Ask for a **textured** material and get it from a CC0 scan (click 4) | The ambientCG importer; provenance recorded (Q2); a `CREDITS.md` row |
| **3.4** | Ask for a material the scans don't cover and get **generated** textures (click 5) | Agent-written fixed-seed generator scripts (L2); `procedural` provenance. **The cut line** if the phase runs long |

Close acceptance: three real briefs (L1, L3, L2), each kept or discarded by the lead, with the **review minutes recorded** in §Execution Log.

### Compact build map

- `.claude/skills/matter-generate/SKILL.md`: **new root.** Add it to `ToolingConventions.md` (the `.claude/` row says "agent surface"; the lanes rule makes only `.claude/CLAUDE.md` read-only to working verbs, and the skill is this phase's *product*, not methodology).
- `tools/converters/`:
  - a Physically Based lookup script;
  - the ambientCG importer (3.3);
  - `recipes/<Stem>_vNN.json` (the existing home, per `ToolingConventions.md`, and globbed by `build_proof_subset.py` and the determinism lane);
  - the recipe JSON Schema (G2).
- `tools/converters/assemble_mtlx.py` `MaterialSpec.from_dict`: G1 rejects unknown keys, with an explicit allow-list for metadata keys (`_comment`, `path`, `sources`). **The 12 existing recipes must still assemble byte-identically** (determinism lane).
- `tools/validators/`: the new `recipe` lane in `run_all.py` (17 lanes) plus `fixtures/` RED recipes.
  - G3's class list mirrors `Taxonomy.md`, the same pattern as `LCD_PORTS` mirroring `LCDSchema.md`.
  - G6 exempts `utility/virtual` and the `system` master (the UV grid and magenta are deliberately unphysical).
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
  - `ToolingConventions.md` (skill root, texture layout drift, the 17th lane);
  - `tools/preview_generators/README.md`;
  - `CONTRIBUTING.md` (point at the skill as an option).

---

## Lead calls

| # | Call | Recommendation |
|---|---|---|
| **Q2** | **Where does a draft texture set's provenance live before a release pins it?** The release lock is where provenance is enforced, but it only exists at promotion. A working next-release lock would drag in the catalog, freeze and staging lanes, which run on the newest release (read in `run_all.py`): that is *Version Management*'s territory. Options: **A** a per-texture-set record `library/provenance/sources/<domain>/<class>/<Set>.yaml`, holding exactly the `provenance:` block the lock will later carry (from `source_provenance.py compute`, or `procedural` + script path); **B** a `provenance` block inside the recipe. | **A.** Provenance belongs to the *texture*, which is versioned and shared independently of any one article (the manifest has separate texture entries, and overlays and masks are shared by several articles). `library/provenance/` is already the home for provenance records. A cannot sit beside the PNGs, because `.gitattributes` puts everything under `MatterLibrary/textures/**` in LFS. |

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
| Q2 draft provenance | **Fork: lead call** (necessary per P5; deliverable; admissible). |
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

## Discovery Status

- **Passes captured:** 2 (2026-09-23).
- **Pass 2:** USDLiveView added as the lead's interactive review surface. It is already built and needs no Stage; it only needs the preview scene that step 3.1 writes anyway. The steps, lane and Q2 are unchanged.
- **Current working direction:** the Brief above, with 4 vertical steps, `build` lane, and first click at step 3.1.
- **Open decisions:** Q2 (lead call; affects step 3.3 only, so step 3.1 can start before it is answered).
- **Checks to carry forward:**
  - re-verify that the 12 existing recipes assemble byte-identically after G1;
  - confirm the skill loads from `.claude/skills/` (the first click proves it);
  - confirm the headless render opens no desktop window;
  - fix `ToolingConventions.md`'s texture-layout drift at doc sync.

## Execution Log

_(populated during execution)_
