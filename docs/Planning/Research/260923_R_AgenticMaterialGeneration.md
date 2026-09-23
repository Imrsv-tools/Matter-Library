# Research — an AI tool that generates Matter materials

**Opened:** 2026-09-23 · **Mode:** research — gathers, commits to nothing · **Next:** lead reads the Status footer and answers the open questions

**Question:** from our existing docs and research, can we work out how to build an AI tool that generates MaterialX materials to start filling out the library, and what would it need?

**Extends, does not replace:** `260923_R_StandaloneSetup.md` Pass 8 seed 11 and its open question Q10 ("pipeline agent vs judging agent; paid vs open stack; near-term or parked?"), and `docs/specs/Authoring/AuthoringGoldenPath.md` §Future-toolchain note. The Roadmap entry is **Agentic Material Generation — RESEARCH**.

**Sources examined (2026-09-23):**
- specs: `AuthoringGoldenPath.md`, `Tooling/AuthoringHarness.md`, `Contract/MaterialXTemplate.md`, `Contract/LCDSchema.md` (grep), `Contract/Manifest.md` (grep), `Ontology/{Taxonomy,MasterSet,Identity}.md`, `docs/Glossary.md`;
- code: `tools/converters/{assemble_mtlx,build_proof_subset,gen_article_textures}.py`, `tools/converters/recipes/*.json` (3 read in full), `tools/validators/validate_material.py` (outline + master-conformance), `tools/generators/matter_proxy.py` (grep), `tools/preview_generators/README.md`, `library/releases/matterlib-0.1.0.lock.yaml` (provenance entries);
- web: physicallybased.info and its repo, ambientCG API and licence docs, and a search for recent vision-language material-generation research.

---

## Resolved — lead decisions (2026-09-23)

| # | Decision |
|---|---|
| D1 | **Matter only, never assemblies.** The library holds *substances*: fired clay (brick material), marble (tile material), wood species (floor material). It does **not** hold brick walls, tiled floors or plank floors. This closes O10. It matches `_Architecture.md` ("physically based 'matter' materials") and `Taxonomy.md` (brick wall, tile roof and cobblestone street are "non-matter"; the Realm stays *(planned)* and is untouched). Pass 9 was wrong to frame assemblies as a coverage candidate. |
| D2 | **No new masters.** A master *is* the LCD and texture structure for a type of material. The 7 masters stand; coverage needs none added. This closes O8 as it was framed. The one real issue underneath it (Pass 10) is that `MasterSet.md` §Master resolution chooses the master **by taxonomy class**, and that is a doc conflict to discuss with the lead, not a design question. See Pass 12. **Doc fix landed** (the lead agreed): an article declares the master that fits the material, and its class gives only a typical default (`MasterSet.md` §Master resolution, quick fix `0770f38`). This closes O13. |
| D3 | **Classes are added when the matter needs them:** "we have a universe to rebuild matter for". The 19 classes are a starting set, not a ceiling. Landed in `Taxonomy.md` §Growth model (quick fix `0770f38`). This unblocks O11: fired clay can get its own class. |
| D4 | **Lanes (O1): yes.** Param-only (L1) and ambientCG curation (L3) first, agent-written procedural generators (L2) next, generative imagery (L4) parked behind R13. |
| D5 | **Where it runs (O2): a Claude Code skill first.** The lead stays in the loop and the existing scripts are driven as they are. A batch agent and the Matter Manager come later. |
| D6 | **The harness guards belong to this work (O3).** G1–G6 are built as part of agentic generation, not as part of *Author a Material End to End*. Human authors benefit anyway. |
| D7 | **Add `ceramic` (O11).** Landed as `engineered/ceramic` (quick fix `f2cfa88`): fired-clay matter, meaning brick clay, terracotta, earthenware, stoneware and porcelain. The domain placement was the agent's; the lead named the class. |

---

## Pass 1 — What is already decided (prior art, re-read)

**Examined:** StandaloneSetup Pass 8 seed 11 and Q10, AuthoringGoldenPath in full, the R13 shipped-pixel rule.

**Finding:** the design frame already exists. Four positions are settled, and this research builds on them rather than reopening them:
1. **No tool emits valid MaterialX from a prompt, so stage C stays a deterministic, scripted assembler.** It exists: `tools/converters/assemble_mtlx.py`.
2. **The long pole is human judgement:** metallic correctness, roughness consistency, parity.
3. **Output is a proposal, never an approval.** Seed 11 says "candidate materials, never approved ones … a human judgement gate".
4. **The shipped-pixel rule (R13, HARD):** no pixel ships unless its provenance is recorded and it is CC0-dedicable, with evidence. Generative-model output is "case by case", and **no generative tool is approved today** (AuthoringGoldenPath, *Reevaluate 2026-09-23*).

**What was still open:** how an agent should actually author a material, where its pixels come from under R13, and what the harness lacks for an agent to use it safely. Passes 2–6 cover these.

## Pass 2 — The generation target is the recipe, not MaterialX

**Examined:** the `MaterialSpec` dataclass and `from_dict` in `assemble_mtlx.py`; `build_proof_subset.py`; three recipes (ABS, Copper, Rust); `matter_proxy.py`.

**Finding (verified in code):** a Matter article is fully determined by **one small JSON recipe plus its textures**.
- The recipe is a flat, typed spec of about 45 fields: identity (`name`, `path`), taxonomy (`domain`, `class`), `master`, `scale_tag`/`meters_per_tile`, the base PBR maps or constants, per-master author-tier values (IOR, transmission and absorption, subsurface, emission, cutoff, the layer-2 set), up to 2 overlays and 1 maskset, and the Creator-tier `lcd_ports` and `lcd_defaults`.
- A param-only article is about 10 fields. `ABS_Matte_Clean_Base_s01_v01.json` is the whole of one.
- `build_proof_subset.py <recipe>` writes the `.mtlx` to `MatterLibrary/materials/<path>`, deterministically.
- **The same recipe also drives the Blender side:** `matter_proxy.py` builds the `MatterLCD_<id>` Principled proxy from the recipe's `*_tex` and `*_const` fields. **One recipe → the `.mtlx` and the Blender proxy.**
- `_check_spec` already refuses incoherent specs: unknown master; a port outside the frozen LCD vocabulary; more than 2 overlays; an overlay with no density port; layer 2 without a maskset; a maskset without `maskset_blend`; a cutoff with no opacity source.

**Decision / hypothesis:** **the AI's output is a recipe (plus, where needed, a texture source); it never writes MaterialX.** This is the key simplification. The model works in a small, closed, typed space that the project already has guards for, and everything downstream (assembly, validation, determinism, catalog, Blender proxy) is existing tooling. It also answers the golden path's "no tool closes text → MaterialX" directly: nothing has to.

## Pass 3 — Where the pixels come from under R13: four lanes

**Examined:** the R13 test table (AuthoringGoldenPath), the 0.1.0 lock's provenance entries, `gen_article_textures.py`.

**Finding:** the lock already records two admissible pixel classes, and both are agent-reachable:
- `source: procedural, license: CC0-1.0, evidence: tools/converters/gen_article_textures.py` (verified in the lock: Lace, Marble, Rust, the shared overlays and masks);
- ambientCG, with `evidence: {url, sha256_scope, sha256, files[]}` computed by `tools/validators/source_provenance.py`.

The generators are plain fixed-seed numpy value-noise scripts (about 175 lines for three articles). **A script like that is exactly what a language model writes well, and the committed script *is* the CC0 evidence.**

| Lane | What the agent produces | Pixel provenance under R13 | Quality ceiling | Admissible today? |
|---|---|---|---|---|
| **L1 — param-only** | a recipe with constants only (no textures) | none — no pixels | good for uniform matter: plastics, glass, gems, liquids, clean metals, emissive | **yes** |
| **L2 — agent-written procedural** | a recipe **+ a deterministic, fixed-seed texture generator script**, committed | `procedural` / CC0-1.0 / evidence = the script, as today | stylised to semi-real; weak for photoreal wood, soil and vegetation | **yes**, the same class as the existing generators |
| **L3 — CC0 curation** | picks an ambientCG set, fetches it, records the evidence, writes the recipe | ambientCG CC0-1.0 with sha256 evidence, as today | photoreal, scanned | **yes**. ambientCG's licence: all assets CC0 1.0, "copy, modify, distribute … even for commercial purposes, all without asking permission" (docs.ambientcg.com/license, 2026-09-23) |
| **L4 — generative imagery** | stage A/B of the golden path (a diffusion albedo, then a decomposer) | case by case; **no tool approved** | photoreal, unbounded variety | **no — parked behind R13** |

**Decision / hypothesis:** **an agent can start filling the library today through L1–L3 without reopening R13.** L4 is the only lane with a provenance question, and it is the least needed for a first push. The "paid clean-provenance vs open stack" fork in Q10 is therefore **not on the critical path**. Both halves are L4.

⚠ **L3 is curation, not generation.** It is honest to call it "an agent that finds, fits and packages CC0 scans". It will likely fill the textured classes faster and better than L2 or L4.

## Pass 4 — Grounding data an agent can cite (CC0, verified)

**Examined:** physicallybased.info, its GitHub repo, the ambientCG API docs.

**Finding:**
- **Physically Based** (`AntonPalmqvist/physically-based-api`) is a database of measured values for CG materials: colour (several colour spaces), IOR, specular, F0/F82 and density. It has a JSON API at `api.physicallybased.info/v2`, with `data/materials` and `data/lightsources` in the repo.
  - **Licence verified by reading the repo's `LICENSE` file: CC0 1.0 Universal** (2026-09-23). The website itself states no licence; the file is the evidence.
- **ambientCG** has a JSON API (v3: `/assets`, `/categories`, `/collections`; v1/v2 `/full_json`, `/downloads_csv`). Its own docs warn it is run by one person and "potentially not as reliable or stable as needed for an 'enterprise-level' application". So cache and pin; don't depend on it live.

**Hypothesis:** this is what makes L1 **physically honest rather than plausible-sounding**. The agent looks up the measured base colour and IOR (or F82 for metals) and cites the source in the recipe's comment or provenance. It does not invent them. It also gives a checkable reference for the plausibility lane (Pass 5).
- *Unverified:* how Physically Based's metal F82 values map onto OpenPBR's `specular_color`/F82 carriers. The assembler authors no such input today (the `MaterialSpec` has no `specular_color` field). **Metals may need an assembler addition** before measured metal values can be carried.

## Pass 5 — What the harness lacks for an agent author (verified gaps)

**Examined:** `from_dict`, `_check_spec`, `validate_material.py` (its checks list and `check_master_conformance`), `build_proof_subset.py`.

The harness was built for a careful human author. An agent authoring at volume would hit these gaps, each verified against the live code on 2026-09-23:

| # | Gap | Evidence | Why it bites an agent |
|---|---|---|---|
| G1 | **Unknown recipe keys are dropped silently** | `from_dict` "keep[s] only known spec fields" so `_comment`/`path` survive | A typo such as `roughnes_const` silently becomes the default 0.5 and still passes every gate. **The same silent-success class as `.claude/CLAUDE.md` §Editing.** An agent needs unknown-key rejection, or a published JSON Schema to author against. |
| G2 | **No machine-readable recipe schema** | the dataclass is the only definition | Structured-output and tool-use authoring want a JSON Schema (types, enums for master, domain, class, LCD ports). |
| G3 | **Taxonomy is not checked** | `domain`/`class` are free strings in the assembler; no validator greps them against the 19 classes | An agent could invent `natural/crystal`. `Taxonomy.md` says the 19 classes are closed per release. *(2026-09-23: now 20 classes, and classes grow by lead decision (D3); the guard checks against the current list, so a new class is a deliberate, reviewed addition.)* |
| G4 | **Class → master routing is not checked** | `_check_spec` checks only `master ∈ KNOWN_MASTERS`; routing (with the `marble`/`diamond`/`rust` name exceptions) is written in `MasterSet.md` and applied in consumer code (MasterSet *Drift 2026-09-23*) | An agent could declare `Subsurface` for a plastic and pass. The routing rule needs to exist as data or code before an agent can be held to it. This overlaps with R14 (master token as release data). *Refined by Pass 10 (2026-09-23): enforcing **today's** one-master-per-class table would block most of textile. What to check instead waits on the doc conflict in Pass 12.* |
| G5 | **`path` vs `domain`/`class`/`name` are not cross-checked** | `build_proof_subset.py` writes to `d["path"]` verbatim | A recipe can declare one class and land in another folder. |
| G6 | **No physical-plausibility lane** | `check_master_conformance` checks that the defining carriers are **present and wired**, not that values are sane; Opaque returns `[]` | Nothing flags an albedo of 1.0, a non-binary metalness on a clean metal, or an IOR of 4. This is exactly the "metallic correctness, roughness consistency" long pole of Pass 1. A cheap, automatic range check would take much of that load off the human. |
| G7 | **Adding to a manifest is manual** | no tool; the lock is hand-authored YAML | This is the Matter Manager's job (Roadmap: *Author a Material End to End*). |
| G8 | **The gate does not run on the lead's box** | `run_all.py` fails at import: no MaterialX Python module (AuthoringHarness *Todo 2026-09-23*) | **Hard prerequisite.** Phase02 (One-Command Check, ACTIVE) owns it. An agent loop cannot use a gate that cannot run. **Met 2026-09-23** (Phase02 COMPLETE; measured: `uv run tools/validators/run_all.py` → 16 lanes, 14 PASS / 2 SKIP (`compression`, `staging`: encoder absent), 0 FAIL on the lead's box). |
| G9 | **Visual check needs the USD toolchain** | `make_preview.py` + usdview/usdrecord; it degrades to `parity-not-evaluated` without `pxr` | An agent that critiques its own render (Pass 6) needs `usdrecord` headless. It is built on the lead's box (StandaloneSetup Pass 7), but not in CI. |

**Finding:** G1–G6 are small and mostly additive (a schema, a routing table, a range table, strict parsing). They also **benefit human authors**, which is why they belong in *Author a Material End to End* as much as here.

## Pass 6 — Shape of the tool (hypothesis, not a design)

**The loop.** The existing A → B → C pipeline, with the agent at the front and a render-and-critique step at the back:

```
brief ("weathered oak planks", or a coverage gap: "environmental/sand has 0 articles")
  → plan    : taxonomy slot, master via routing (G4), grammar-valid name (Identity.md), scale tag, lane L1/L2/L3
  → ground  : Physically Based values (L1) · ambientCG set (L3) · write the generator (L2)
  → author  : recipe JSON (+ generator script or fetched set + provenance evidence)
  → assemble: build_proof_subset.py <recipe>            ← existing, deterministic
  → gate    : validate_material + plausibility (G6)    ← existing + new
  → render  : make_preview + usdrecord → PNG            ← existing toolchain
  → critique: a vision model compares the render with the brief; iterate (bounded, e.g. ≤3 rounds)
  → propose : a branch/PR with the recipe, textures, provenance, render and a critique note; status `draft`
  → HUMAN   : a maintainer judges; only a maintainer moves it toward a release
```

**Where it runs.** Three options, in rising cost:

| Option | What | For | Against |
|---|---|---|---|
| **a — a Claude Code skill in this repo** | a skill/prompt that drives the existing scripts, with the lead in the loop | no new infrastructure; uses the tools as they are; the lead watches every step; fits "bias to the smallest unit" | tied to one maintainer's session; not a community tool |
| **b — a scripted batch agent** | a Python driver calling an LLM API with tools (author the recipe, assemble, validate, render, critique) over a list of briefs | runs unattended over a coverage list; reproducible | needs API keys, a cost budget and a model choice; more code to own |
| **c — inside the Matter Manager** | generation as one feature of the planned authoring tool | the long-term home (AuthoringGoldenPath §Future-toolchain note) | the Manager doesn't exist yet |

**Hypothesis:** **a first, then b once a handful of articles show the loop works; c absorbs it later.** Option a costs almost nothing to try and would surface the real gaps before any code is written for b.

**Q10's "pipeline agent vs judging agent" narrows to this:** the agent **drives the pipeline and self-critiques against its brief**, which is cheap and catches gross failures. It does **not** judge for release. The maintainer judgement gate stays (seed 11; Manifest §Governance). The vision critique is advisory evidence attached to the proposal, not a gate.

**Manifest status.** The Glossary defines `candidate` as "passed CI (schema / naming / scale / parity checks)". Parity is not automated (G9), so agent output lands as **`draft`**. It reaches `candidate` only when that lane exists. *(Open question O4.)*

## Pass 7 — External research leads (checked only at abstract level)

**Examined:** one web search, 2026-09-23. **Unverified beyond the abstracts and listing pages. Treat these as leads, not findings.**
- **VLMaterial** (ICLR 2025, MIT/ETH; code at `github.com/mit-gfx/VLMaterial`): fine-tunes a vision-language model to emit **Blender procedural material programs (Python)** from an image, with an open procedural-material dataset.
- **MultiMat** (arXiv 2509.22151): multimodal program synthesis for procedural materials.
- **"Reflecting Process Expertise in Procedural Material Generation"** (arXiv 2607.13318).

**Relevance:** these target **open-ended node graphs**. Our target space is far smaller: a closed recipe over 7 masters and 8 frozen ports. So a general-purpose model with the schema and grounding data (Passes 2 and 4) is likely enough for L1 and L3, without fine-tuning. The research line matters most for **L2** (procedural textures from an image reference). A later pass could test whether any of their generators emit CC0-dedicable output under R13. Their *code* licences are not checked here.

## Pass 8 — What it could fill, roughly

Today: 12 articles; 9 of 19 classes populated; the environmental domain is empty (Taxonomy.md, measured 2026-09-23).
- **L1 (param-only)** plausibly reaches plastic, polymer, glass, mineral (gems), liquid, emissive and energy, plus clean metals once the F82 carrier question (Pass 4) is settled.
- **L3 (ambientCG)** plausibly reaches wood, stone, soil, sand, cementitious, metal (worn), textile and vegetation. That is most of the photoreal gap.
- **L2** covers what L3 lacks and supplies variants (Condition/Detail tokens), overlays and masksets.

*Not verified:* which master each empty class routes to. That is MasterSet's coverage table, not re-read here. Also, `atmospheric` is out of master-set scope (Taxonomy.md). *(Superseded by Passes 9–11, 2026-09-23: the supply is measured, the routing is read, and it turns out to be a blocker for several classes.)*

## Pass 9 — Supply, measured: what the two CC0 sources actually hold

**Examined (2026-09-23):**
- the ambientCG catalogue via `https://ambientcg.com/api/v2/full_json?type=Material&limit=2000&include=tagData`: 2,000 of 2,011 reported materials, grouped by `displayCategory`, `creationMethod` and `dimensionX`;
- the Physically Based dataset via `https://api.physicallybased.info/v2/materials`: all 116 records and their fields.

**ambientCG, mapped by hand onto the 19 classes.** The category → class mapping is this pass's judgement, not ambientCG's:

| Matter class | ambientCG categories mapped | Count |
|---|---|---|
| natural/stone | Rock, Rocks, Marble, Onyx, Travertine, Granite, Lava | 167 |
| natural/wood | Wood, Planks, Bark, Bamboo, Tree End, Wood Chips, Logs, Cork | 193 |
| natural/soil | Ground, Clay | 131 |
| natural/mineral | Ivory, Shells | 5 |
| engineered/metal | Metal, Metal Plates, Diamond Plate, Corrugated Steel, Rust, Sheet Metal, Foil, Chainmail, Grate, Painted Metal | 198 |
| engineered/glass | — | **0** |
| engineered/cementitious | Concrete, Asphalt, Plaster, Painted Plaster, Terrazzo | 153 |
| engineered/composite | Chipboard, Cardboard, Paper, Styrofoam, Porcelain, Glazed Terracotta, Solar Panel | 33 |
| synthetic/plastic | Plastic | 25 |
| synthetic/polymer | Rubber, Foam, Acoustic Foam, Sponge | 13 |
| synthetic/textile | Fabric, Leather, Carpet, Wicker, Rope, Net, Tatami | 189 |
| synthetic/coating | Paint, Painted Wood, Wallpaper | 29 |
| environmental/sand | Gravel | 44 |
| environmental/vegetation | Grass, Moss, Scattered Leaves, Leaf, Thatched Roof, Flower Set | 28 |
| environmental/liquid | Snow, Ice | 27 |
| utility/* | — | **0** |
| **Assemblies — not matter** | Tiles, Paving Stones, Bricks, Wood Floor, Road, Roofing Tiles, Facade, Wood Siding, Fence, Metal Walkway, Tactile Paving, Painted Bricks, Office Ceiling, Pathway, Pipe, Rails | **659** |
| **Imperfection sources** | Surface Imperfections, Fingerprints, Scratches, Smear, Footsteps, Chip | 52 |
| **Out of scope** | Sign, Christmas Tree Ornament, Pizza, Candy, Stick Set, Painting | 54 |

**Findings:**
- **About 1,235 ambientCG materials land in a matter class. That is far more than an initial library needs, so photoreal supply is not the limit.** Supply is thin in exactly the classes where ambientCG is structurally weak: glass (0), mineral (5), polymer (13), plastic (25), liquid (27, and those are snow and ice), and all of utility (0).
- **A third of ambientCG (659) is assemblies** such as bricks, tiles, paving and floors. `Taxonomy.md` names exactly these ("*brick wall*, *tile roof*, *cobblestone street*") as the future **Realm** above Domain *(planned)*. They are among the most-downloaded assets and what users will ask for first, but they are **not matter** under today's ontology. *(Open question O10.)* **Correction (lead, D1, 2026-09-23): out of scope, and not a question.** The library is substances. The substance behind an assembly (fired clay, marble, a wood species) is in scope; it comes from the matter categories above or from Physically Based (`Brick`, `Terracotta`, `Clay`, `Porcelain`, `Marble`), not from a patterned wall or floor texture.
- **The 52 imperfection sources map onto our overlays and masksets**, but not directly: an overlay is **packed data** (R/G normal XY · B roughness bias · A density; `LCDSchema.md`), so each needs converting. The library has 2 overlays and 3 masksets today.
- **Creation method:** 1,408 `PBRProcedural`, 355 photogrammetry, 201 approximated, 36 multi-angle. All are CC0 under the licence read in Pass 3.
- **Scale tags:** only **512 of 2,000** records carry physical dimensions (`dimensionX`/`dimensionY`; e.g. `Bricks105` 240 × 120). For the rest, the scale tag has to be estimated by the agent, which is human-checkable, or recorded as `sUKN`.

**Physically Based (116 records):** Metal 32 · Manmade 22 · Liquid 19 · Organic 15 · Human 11 · Crystal 10 · Plastic 7.
- The fields go well beyond Pass 4's list: `color`, `metalness`, `roughness`, `ior`, `complexIor`, `specularColor` (both **F82** and Gulbrandsen forms), `transmission`, `transmissionDepth`, `volumeCoefficients`, `subsurfaceRadius`, `thinFilmIor`/`thinFilmThickness`, `density`.
- So **it supplies the defining author-tier value for most masters directly:** IOR and absorption for Thick (Diamond 2.4168, soda-lime glass 1.52, water 1.3325), subsurface radius for Subsurface (Marble, 6 Fitzpatrick skin types), and F82 for metals. It **answers the data half of O5.** Whether the assembler can carry F82 is still open.
- ⚠ **Some linear colours exceed 1.0** (Gold `[1.059, 0.773, 0.307]` srgb-linear). A plausibility lane (G6) must **clamp or flag** these rather than reject the source.
- **Calibration references:** Gray Card, Spectralon, Musou Black and MIT Black exist in the dataset. They would make ideal `utility/virtual` reference articles for the **Parity Baselines** roadmap entry.

## Pass 10 — Class → master routing does not scale to real coverage (verified)

**Examined:** `MasterSet.md` §v1 baseline (the "Covers" column) and §Master resolution; `validate_material.py` `check_master_conformance` (read in full).

**What the conformance check requires, per master (verified in code):**
- **Masked:** an `opacity_cutoff` interface input **and** a graph-driven `geometry_opacity` source.
- **Translucent:** IOR, transmission weight, colour and thin-walled flag, plus depth for Thick.
- **Subsurface:** all four SSS carriers.
- **TwoLayer:** a maskset, a second layer and a nonzero `maskset_blend`.

**The collision.** Routing is one master per class plus leaf-stem name exceptions (`marble`, `diamond`, `rust`). Real coverage breaks it in many classes, not one:

| Class (routes to) | Articles the route gets wrong | What they need |
|---|---|---|
| synthetic/textile (**Masked**) | cotton, denim, wool, leather, carpet — nearly all of ambientCG's 189 | Opaque (plus sheen, Pass 11). Held to Masked, every fabric would need an opacity map to pass. |
| environmental/vegetation (**Masked**) | grass or moss ground cover | Opaque. Leaves and fronds are Masked plus the *(planned)* foliage variant. |
| natural/mineral (**Opaque**) | sapphire, quartz, amber, salt crystal | TranslucentThick. Only `diamond` has an exception. |
| engineered/glass (TranslucentThin) | thick or solid glass, glass blocks | TranslucentThick |
| synthetic/plastic (**Opaque**) | acrylic, polycarbonate, clear PET | TranslucentThin |
| natural/stone (**Opaque**) | jade, onyx, alabaster | Subsurface. Only `marble` has an exception. |
| synthetic/coating (**Opaque**) | car paint, varnish, glazes | Opaque plus clearcoat (Pass 11), or TwoLayer |
| engineered/metal (**Opaque**) | perforated metal | Masked. There is no route, already known (MasterSet ¹). |

**Finding:** the name-exception mechanism would need **dozens** of exceptions to reach real coverage. Its own spec's precedent ("one material justifies one master") does not hold at this scale.
- Today nothing *enforces* routing: the recipe's `master` is free, so an agent can declare Opaque for cotton and pass. That is also why **G4 as written ("check routing") would, if implemented against the current table, block most of textile.**

**Hypothesis (for the contract phase, not decided here):** route by **class → a set of allowed masters, with a default**. The article declares its master, the validator checks membership, and the master token rides in release data per article (already the direction of R14). The existing name exceptions become the evidence for which masters each class allows.
- This is a `MasterSet.md` contract change, so it belongs to the release-bundle / consumer-contract phase that owns R14.
- It is recorded here because **it gates coverage in 8 of 18 in-scope classes.** *(Open question O8.)*

**Correction (lead, D2, 2026-09-23):** the framing above treated this as a master-design question. It is not one: no masters are added, and the table above does not ask for any. Every "needs" entry is one of the existing 7. What the table actually shows is that **the docs choose the master by class**, while a master is the structure for a *type of material*. Pass 12 locates exactly where the docs say this.

## Pass 11 — What "excellent initial coverage" would take

**A target, not a plan.** The library's design argues for **depth per matter, not volume**: one article plus the Creator-tier tint, UV and roughness controls and its overlays and maskset already spans many conditions (Copper's patina, dust and scratches are all one article). So the target is **distinct matters**, roughly 5–15 per class weighted by how often a scene needs them, not ambientCG's 1,235.

| Class | Target | Main lane | Blocked by / needs |
|---|---|---|---|
| natural/stone | 15 | L3 (167) | jade/onyx → Subsurface routing (O8) |
| natural/wood | 15 | L3 (193) | varnished wood → clearcoat (C2) |
| natural/soil | 10 | L3 (131) | — |
| natural/mineral | 8 | L1 (PB crystals) | gems → Thick routing (O8) |
| engineered/metal | 20 | L1 (PB 32 metals) + L3 (198) | F82 (C1); brushed → anisotropy (C3); perforated → Masked (O8) |
| engineered/glass | 6 | L1 only | thick glass routing (O8) |
| engineered/cementitious | 10 | L3 (153) | — |
| engineered/ceramic *(added 2026-09-23, D7)* | 8 | L1 (PB `Brick`, `Terracotta`, `Porcelain`) + L3 (Porcelain, Glazed Terracotta) | glaze → clearcoat (C2) |
| engineered/composite | 8 | L3 (33) | the class's boundary is undefined (O11); porcelain and terracotta have moved to ceramic |
| synthetic/plastic | 10 | L1 (PB 7) + L3 (25) | clear plastics → Thin routing (O8) |
| synthetic/polymer | 6 | L1 + L3 (13) | plastic vs polymer boundary (O11) |
| synthetic/textile | 12 | L3 (189) | textile routing (O8); sheen (C2) |
| synthetic/coating | 8 | L1 + L3 (29) | clearcoat (C2) |
| environmental/sand | 6 | L3 (44) | — |
| environmental/vegetation | 6 | L3 (28) | routing (O8); foliage variant *(planned)* |
| environmental/liquid | 8 | L1 (PB 19 liquids) | snow and ice are not liquids (O11) |
| utility/emissive | 6 | L1 | — |
| utility/virtual | 5 | L1 (PB references) | — |
| utility/energy | 3 | L1/L2 | animated "plasma" is out of scope (MasterSet) |
| **Total** | **~160** (~170 with ceramic) | | plus **~8 overlays and ~8 masksets** (L2, or ambientCG imperfections converted) |

**Scale of the ask:**
- **~110 of ~160 are reachable with no contract change.** These are the rows marked "—", plus the unblocked majority of stone, wood, metal, plastic and coating. The remaining ~50 wait on routing (O8) or on the three OpenPBR carriers below. *Correction (D2): the "routing" blockers are a doc fix, not design work (Pass 12). Once the docs say the master follows the material, the real blockers are only carriers C1–C3 and the class boundaries (O11).*
- **Texture storage:** today's textured articles take 4.3 MB (Limestone) to 7.7 MB (Copper) of 1K PNG in Git LFS (measured). ~110 textured articles is roughly **0.5–1 GB of LFS** before any 2K option. *Unverified:* the GitHub LFS storage and bandwidth quota for this org. Every clone and CI run pulls it.
- **Review is the throughput limit, not generation.** Authoring a recipe is minutes of agent time. The human gate is the cost. At an *estimated, unmeasured* 5–10 minutes per article with a render and critique note attached, ~160 articles is **roughly 15–25 maintainer hours**. The first probe (Status → Next) should measure this.

**What it would take, in dependency order:**
1. **The gate runs:** Phase02 (G8).
2. **Harness guards:** G1–G3, G5, G6 (G6 with clamping for PB values above 1.0). Also G4, but only after O8.
3. ~~**Routing reform (O8):** class → allowed masters. This is a contract change owned by the R14 phase.~~ *Superseded by D2: fix the docs so the master follows the material (Pass 12).*
4. **Three author-tier carriers the assembler lacks**, all real OpenPBR inputs (carriage lane A), so no Creator-tier change:
   - **C1** `specular_color` / F82 for metals (data from PB);
   - **C2** `fuzz_*` (sheen) for cloth and `coat_*` for varnish, paint and glaze;
   - **C3** `specular_roughness_anisotropy` for brushed metal.

   `MasterSet.md` already lists "anisotropy, sheen, clearcoat as optional Substrate slab features" on Opaque; `MaterialSpec` has none of them (verified). Each also needs the Blender proxy and UE master side to honour it, so **the LCD parity question comes with it.** *Unverified:* the exact OpenPBR 1.39 input names above. Check them against the stdlib `open_pbr_surface` nodedef before relying on them.
5. **An ambientCG importer:**
   - fetch and pin a set; downscale to 1K;
   - map the channels (Color, Roughness, Normal, Metalness, Opacity; Displacement and AO have no carrier today);
   - compute the evidence with `source_provenance.py`;
   - propose a scale tag from `dimensionX` where present.

   *Unverified:* which normal-map convention (GL or DX) the assembler expects. ambientCG ships both.
6. **An overlay packer:** convert imperfection sources into the packed overlay/maskset format.
7. **Headless render plus a contact sheet for review (G9).** This is the same work as the *See the Library* Roadmap entry.
8. **Batch manifest entry (G7)**, which the Matter Manager owns.
9. **Taxonomy rulings (O9–O11).**

## Pass 12 — Reread after the lead's correction: where the docs stand

**Examined (2026-09-23):** `_Architecture.md` (matter definition, master section); `MasterSet.md` (intro, v1 table, §Master resolution); `Taxonomy.md` §Growth model; `Identity.md` scale table; `docs/Glossary.md`. I also grepped `docs/specs`, `Readme.md` and the Glossary for brick / wall / floor / tile / Realm / assembly.

**Matter vs assemblies: the docs agree with D1.** No spec describes a wall or floor as in scope.
- `_Architecture.md`: "a community, CC0 library of physically based 'matter' materials (Limestone, Copper, Glass, …)".
- `Taxonomy.md`: brick wall, tile roof and cobblestone street are "non-matter", reachable only through a *(planned)* Realm.

The conflation was this research's alone: it took ambientCG's catalogue as the frame.
- *Minor, lead's call:* `Identity.md`'s scale-tag table gives "small tiles", "flooring" and "wall panels" as scale examples. Read quickly, these name assemblies. A wording touch-up could name the substance at that scale instead.

**How a master is chosen: the docs conflict with D2.**
- `MasterSet.md` intro and `_Architecture.md` agree with the lead. A master is "a template instance: master X + these textures + these LCD parameter values", and it defines "what a Matter material can BE".
- But `MasterSet.md` **§Master resolution** says "a material identity resolves to a master **by its taxonomy class**, with leaf-stem name exceptions". Its v1 table's "Covers" column assigns classes to masters, which puts all of textile and vegetation under **Masked**.
- **Taken literally, that makes a cotton or denim article Masked.** The Masked conformance check would then demand a cut-out opacity map (Pass 10).
- **Where the class rule came from** (StandaloneSetup Pass 9, verified there): IMRSV's plugin routes by class in C++, because the per-article token in each `.mtlx` "is read by nobody". R14 already moves the per-article master token into release data. After that, **no consumer needs class routing**, and the article's own declared master, chosen for what the material is, is the only rule needed.
- The class rule also appears in the Glossary ("Name-keyed master resolution", consumer-side) and in `_Architecture.md`'s R14 Drift note ("a consumer never hard-codes class → master routing").

**Not decided here (a spec edit is outside `/research`):** whether §Master resolution is rewritten as "an article declares the master that fits the material; class gives a typical default", and whether the "Covers" column becomes typical examples rather than a routing rule. **The lead asked for a conversation before fixing the docs.** This pass is the input to it. *(Open question O13.)*

---

## Open questions

| # | Question | Why it matters |
|---|---|---|
| ~~O1~~ | **Resolved: D4.** ~~Which lanes are in scope first?~~ The hypothesis is L1 + L3 now, L2 next, L4 parked. | Sets the first slice; L4 alone reopens R13. |
| ~~O2~~ | **Resolved: D5 (skill first).** ~~Where does it run first:~~ a Claude Code skill (a), a batch agent (b), or wait for the Matter Manager (c)? | Option a needs no new infrastructure and could run as soon as Phase02 lands. |
| ~~O3~~ | **Resolved: D6 (here).** ~~Do G1–G6 belong to this seed,~~ or to *Author a Material End to End*?** They help human authors equally. | Avoids two phases building the same guards. |
| O4 | **What status does agent output land in:** `draft`, or `candidate` once parity is automated? | Keeps the status lifecycle honest (Glossary: `candidate` = passed CI including parity). |
| O5 | **Metals:** does the assembler need an OpenPBR `specular_color`/F82 carrier to use measured metal data? *Narrowed by Pass 9: the data exists (PB carries F82 for 32 metals); what remains is carrier C1 in Pass 11.* | Metals are a large, common class; accurate metals need it. |
| O6 | **Grounding citations:** should a recipe (or provenance) record *where its constants came from* (e.g. a Physically Based entry), not only its pixels? | Auditable physics, same spirit as the shipped-pixel rule. |
| O7 | **Credits (StandaloneSetup Q12):** how is an agent-authored article credited? Per R8 the committing person is the author. | Touches the credits schema. |
| ~~O8~~ | ~~Master routing: one master per class, or an allowed set?~~ **Closed by D2: no new masters; the underlying doc conflict is O13.** | — |
| O9 | **Skin, hair and cloth for characters (PlatformDependencies M1):** the taxonomy has no biological class. Physically Based has 6 skin types with subsurface data, but skin has nowhere to live. Hair is not a surface material in this model at all. | The platform's one live pull on the library. |
| ~~O10~~ | ~~Assemblies in scope?~~ **Closed by D1: matter only; the substance (fired clay, marble, wood species) is in, the wall or floor is out.** | — |
| O11 | *Partly resolved by D7: `engineered/ceramic` added for fired clay.* **Remaining class boundaries:** composite vs cementitious; plastic vs polymer; where snow and ice live (liquid is wrong); **where fired clay, terracotta and porcelain live** (there is no ceramic class; Pass 9 filed porcelain under composite by judgement). | An agent sorting ~160 articles needs written boundaries, or it will sort inconsistently. D1 makes fired clay a first-class substance. |
| ~~O13~~ | ~~The `MasterSet.md` routing conflict?~~ **Resolved: the doc fix landed (D2, `0770f38`).** G4 becomes "the declared master fits the material", which is a plausibility check, not a class lookup. | — |
| O12 | **Budgets:** the LFS quota, the texture resolution (1K only, or a 2K option), and how much maintainer review time per batch. | Sets how many can realistically ship per release. |

## Status

**Passes captured:** 12 (2026-09-23).

**Update, 2026-09-23 (the direction is set: D4–D7):**
- **Lanes:** L1 + L3 first, L2 next, L4 parked (D4).
- **Where it runs:** a Claude Code skill first (D5).
- **Guards G1–G6 are built here** (D6).
- **`engineered/ceramic` added** (D7, quick fix `f2cfa88`; that commit also brought the Glossary's *Class routing* entry in line with `0770f38`).
- **Remaining open:** O4–O7, O9, O11's leftover boundaries, O12. None blocks starting.
- **The research has crossed the commitment line.** The next unit is `/discovery` for the *Agentic Material Generation* Roadmap entry. Its prerequisite, Phase02 (G8), is **met**: Phase02 is COMPLETE, and the gate runs via `uv run tools/validators/run_all.py` (14 PASS / 2 SKIP / 0 FAIL, measured 2026-09-23).

**Update, 2026-09-23 (lead rulings landed):**
- The master-resolution doc fix landed as a lead-directed `/quick-fix` (`0770f38`): articles declare their master, and the class is only a default (D2). O13 is closed.
- **D3:** classes are added when the matter needs them.
- Pass 11's routing-blocked rows are now **unblocked in the docs**. What remains for full coverage is carriers C1–C3, the harness guards and the class boundaries (O11). D3 turns O11 into "which classes to add" rather than "where to squeeze things in".

**Update, 2026-09-23 (Pass 12, after the lead's correction):**
- **D1:** matter only; walls and floors are out, and their substances are in.
- **D2:** no new masters.
- O8 and O10 are closed.
- A reread found **no doc** putting assemblies in scope; that conflation was this research's own.
- It found **one real doc conflict**: `MasterSet.md` §Master resolution picks the master by taxonomy class, which would make ordinary fabrics Masked. It is recorded as **O13**, for discussion with the lead before any spec edit.
- With that fixed, the ~50 "blocked" articles of Pass 11 wait only on carriers C1–C3 and the class boundaries (O11, which now includes where fired clay lives).

**Update, 2026-09-23 (Passes 9–11, the lead asked "how many, and what for excellent coverage?"):**
- **Supply is not the limit.** ambientCG maps about 1,235 materials onto matter classes, and Physically Based adds 116 measured records that carry most masters' defining values (F82, IOR, absorption, subsurface).
- **A proposed target is ~160 distinct articles plus ~8 overlays and ~8 masksets**, weighted per class. About **110** are reachable without any contract change.
- **The limits are:**
  - **master routing** (one master per class breaks coverage in 8 classes; *superseded: a doc conflict, O13*);
  - **three missing OpenPBR carriers** (F82, sheen/coat, anisotropy);
  - **taxonomy rulings** (O9–O11);
  - **maintainer review time**, estimated at 15–25 hours for ~160 articles (unmeasured).
- Open questions **O8–O12 are new**; O5 is narrowed.

**Earlier direction (Passes 1–8), still holding:** **yes, we can build this, and most of it already exists.**
- The AI authors a **recipe** (a small, typed JSON that the project already assembles, validates and projects to Blender). It never writes MaterialX (Pass 2).
- Its pixels come from three lanes that are **admissible under R13 today**: param-only, agent-written deterministic procedural generators (the script is the evidence), and CC0 ambientCG curation (Pass 3).
- Physical values are grounded in the **CC0 Physically Based database** (licence verified in the repo's `LICENSE` file; Pass 4).
- Generative imagery (L4) stays parked behind R13 and is **not needed to start**. This largely dissolves Q10's paid-vs-open fork.
- The agent drives the pipeline and self-critiques a `usdrecord` render. **A maintainer still judges** (Pass 6).

**Blocking prerequisite:** the structural gate must run: Phase02 (One-Command Check, ACTIVE), gap G8.

**Worth doing before or alongside:** harness guards G1–G6 (strict recipe parsing, a recipe schema, taxonomy and master-routing checks (routing only after O8), a path cross-check, a plausibility range lane). They are small and they help human authors too.

**Open:** O4–O7, O9, O11 (remaining boundaries), O12. O1–O3, O8, O10 and O13 are closed by D1–D7.

**Next step:** when the lead chooses, `/discovery` for *Agentic Material Generation*, seeded from D1–D7 and Passes 2–12. It should sequence after Phase02, whose working gate is the prerequisite. Its first stage is likely the skill plus guards G1–G3, G5 and G6, then a three-brief probe (one each for L1, L3 and L2) that also measures review time. If the direction holds, the Roadmap entry *Agentic Material Generation* can be seeded as a phase stub via a later `/discovery`. A cheap first probe (after Phase02) is a disposable run of option a over 3 briefs, one per lane L1–L3, to see where the loop actually breaks **and to measure the maintainer review time per article** (Pass 11's estimate). Nothing has been built; this doc is the only artifact.
