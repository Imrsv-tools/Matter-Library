# Research — an AI tool that generates Matter materials

**Opened:** 2026-09-23 · **Mode:** research — gathers, commits to nothing · **Next:** lead reads the Status footer and answers the open questions

**Question:** from our existing docs and research, can we work out how to build an AI tool that generates MaterialX materials to start filling out the library, and what would it need?

**Extends, does not replace:** `260923_R_StandaloneSetup.md` Pass 8 seed 11 and its open question Q10 ("pipeline agent vs judging agent; paid vs open stack; near-term or parked?"), and `docs/specs/Authoring/AuthoringGoldenPath.md` §Future-toolchain note. The Roadmap entry is **Agentic Material Generation — RESEARCH**.

**Sources examined (2026-09-23):**
- specs: `AuthoringGoldenPath.md`, `Tooling/AuthoringHarness.md`, `Contract/MaterialXTemplate.md`, `Contract/LCDSchema.md` (grep), `Contract/Manifest.md` (grep), `Ontology/{Taxonomy,MasterSet,Identity}.md`, `docs/Glossary.md`;
- code: `tools/converters/{assemble_mtlx,build_proof_subset,gen_article_textures}.py`, `tools/converters/recipes/*.json` (3 read in full), `tools/validators/validate_material.py` (outline + master-conformance), `tools/generators/matter_proxy.py` (grep), `tools/preview_generators/README.md`, `library/releases/matterlib-0.1.0.lock.yaml` (provenance entries);
- web: physicallybased.info and its repo, ambientCG API and licence docs, and a search for recent vision-language material-generation research.

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
| G3 | **Taxonomy is not checked** | `domain`/`class` are free strings in the assembler; no validator greps them against the 19 classes | An agent could invent `natural/crystal`. `Taxonomy.md` says the 19 classes are closed per release. |
| G4 | **Class → master routing is not checked** | `_check_spec` checks only `master ∈ KNOWN_MASTERS`; routing (with the `marble`/`diamond`/`rust` name exceptions) is written in `MasterSet.md` and applied in consumer code (MasterSet *Drift 2026-09-23*) | An agent could declare `Subsurface` for a plastic and pass. The routing rule needs to exist as data or code before an agent can be held to it. This overlaps with R14 (master token as release data). |
| G5 | **`path` vs `domain`/`class`/`name` are not cross-checked** | `build_proof_subset.py` writes to `d["path"]` verbatim | A recipe can declare one class and land in another folder. |
| G6 | **No physical-plausibility lane** | `check_master_conformance` checks that the defining carriers are **present and wired**, not that values are sane; Opaque returns `[]` | Nothing flags an albedo of 1.0, a non-binary metalness on a clean metal, or an IOR of 4. This is exactly the "metallic correctness, roughness consistency" long pole of Pass 1. A cheap, automatic range check would take much of that load off the human. |
| G7 | **Adding to a manifest is manual** | no tool; the lock is hand-authored YAML | This is the Matter Manager's job (Roadmap: *Author a Material End to End*). |
| G8 | **The gate does not run on the lead's box** | `run_all.py` fails at import: no MaterialX Python module (AuthoringHarness *Todo 2026-09-23*) | **Hard prerequisite.** Phase02 (One-Command Check, ACTIVE) owns it. An agent loop cannot use a gate that cannot run. |
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

*Not verified:* which master each empty class routes to. That is MasterSet's coverage table, not re-read here. Also, `atmospheric` is out of master-set scope (Taxonomy.md).

---

## Open questions

| # | Question | Why it matters |
|---|---|---|
| O1 | **Which lanes are in scope first?** The hypothesis is L1 + L3 now, L2 next, L4 parked. | Sets the first slice; L4 alone reopens R13. |
| O2 | **Where does it run first:** a Claude Code skill (a), a batch agent (b), or wait for the Matter Manager (c)? | Option a needs no new infrastructure and could run as soon as Phase02 lands. |
| O3 | **Do G1–G6 belong to this seed, or to *Author a Material End to End*?** They help human authors equally. | Avoids two phases building the same guards. |
| O4 | **What status does agent output land in:** `draft`, or `candidate` once parity is automated? | Keeps the status lifecycle honest (Glossary: `candidate` = passed CI including parity). |
| O5 | **Metals:** does the assembler need an OpenPBR `specular_color`/F82 carrier to use measured metal data? | Metals are a large, common class; accurate metals need it. |
| O6 | **Grounding citations:** should a recipe (or provenance) record *where its constants came from* (e.g. a Physically Based entry), not only its pixels? | Auditable physics, same spirit as the shipped-pixel rule. |
| O7 | **Credits (StandaloneSetup Q12):** how is an agent-authored article credited? Per R8 the committing person is the author. | Touches the credits schema. |

## Status

**Passes captured:** 8 (2026-09-23).

**Current direction:** **yes, we can build this, and most of it already exists.**
- The AI authors a **recipe** (a small, typed JSON that the project already assembles, validates and projects to Blender). It never writes MaterialX (Pass 2).
- Its pixels come from three lanes that are **admissible under R13 today**: param-only, agent-written deterministic procedural generators (the script is the evidence), and CC0 ambientCG curation (Pass 3).
- Physical values are grounded in the **CC0 Physically Based database** (licence verified in the repo's `LICENSE` file; Pass 4).
- Generative imagery (L4) stays parked behind R13 and is **not needed to start**. This largely dissolves Q10's paid-vs-open fork.
- The agent drives the pipeline and self-critiques a `usdrecord` render. **A maintainer still judges** (Pass 6).

**Blocking prerequisite:** the structural gate must run: Phase02 (One-Command Check, ACTIVE), gap G8.

**Worth doing before or alongside:** harness guards G1–G6 (strict recipe parsing, a recipe schema, taxonomy and master-routing checks, a path cross-check, a plausibility range lane). They are small and they help human authors too.

**Open:** O1–O7.

**Next step:** the lead answers O1–O3. If the direction holds, the Roadmap entry *Agentic Material Generation* can be seeded as a phase stub via a later `/discovery`. A cheap first probe (after Phase02) is a disposable run of option a over 3 briefs, one per lane L1–L3, to see where the loop actually breaks. Nothing has been built; this doc is the only artifact.
