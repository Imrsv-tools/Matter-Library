# Phase03 — Agentic Material Generation

**Status:** SEED (2026-09-23). Numbered by the lead ("yes, start discovery as Phase03"), naming the Roadmap's *Agentic Material Generation* entry. Discovery is opened; Pass 1 has not run. **Lane:** not yet assessed. The hypothesis is `build`, to be verified in Pass 1 against the provenance gate (Q7).

## Outcome

**A maintainer can ask an agent for new materials and receive validated candidates, with recorded provenance, ready for human judgement.**

*(Verbatim from the Roadmap entry, written at Phase01 step 1.5.)*

Concretely at close:
- a Claude Code skill in this repo that turns a brief into a draft article (recipe + `.mtlx` + any textures + provenance);
- the article passes the structural gate;
- the maintainer can look at a render of it before judging.

## Why this is a phase

It is one journey: *brief in → judgeable draft out*. The choices that are expensive to unwind are:
- what the agent is allowed to author (a recipe, never MaterialX);
- where its pixels may come from (the shipped-pixel rule);
- what the gate must refuse *before* volume authoring begins (the harness guards).

Getting these wrong means a batch of drafts to redo.

## Source — the research this phase stands on

`docs/Planning/Research/260923_R_AgenticMaterialGeneration.md`. **Its `## Resolved` table (D1–D7) binds this phase.** In short:
- matter only, never assemblies (D1);
- no new masters, and an article declares its master (D2, landed `0770f38`);
- classes grow as matter needs them (D3); `engineered/ceramic` added (D7, landed `f2cfa88`);
- lanes: param-only (L1) and ambientCG curation (L3) first, agent-written procedural generators (L2) next, generative imagery (L4) parked (D4);
- **a Claude Code skill first** (D5);
- **the harness guards G1–G6 are built here** (D6).

The prerequisite gap G8 is **met**: Phase02 is complete, and `uv run tools/validators/run_all.py` gave 14 PASS / 2 SKIP / 0 FAIL on the lead's box (2026-09-23).

## Scope (seed — to be audited by Pass 1)

**In:**
- **The skill** — brief → plan (taxonomy slot, declared master, grammar-valid name, scale tag, lane) → ground → recipe → assemble → gate → render → self-critique → a `draft` proposal the maintainer judges.
- **Lanes L1 and L3.** Parameter values are grounded in Physically Based (CC0, verified). Textures are ambientCG sets, fetched, pinned, and given sha256 evidence through `source_provenance.py`.
- **Lane L2 as the later step**, if the first steps land with room: agent-written deterministic texture generators, with the committed script as the evidence.
- **Harness guards (research Pass 5):**
  - G1: reject unknown recipe keys;
  - G2: a published recipe JSON Schema;
  - G3: the class is in the taxonomy;
  - G5: the recipe's `path` agrees with its domain/class/name;
  - G6: a physical-plausibility lane, which clamps or flags Physically Based colours above 1.0;
  - G4: the declared master is plausible for the material, a check and not a class lookup (after D2).
- **The render-and-critique step (G9):** `usdrecord` headless on the lead's box, with the result attached to the proposal.

**Not now:**
- **Filling the library.** The ~170-article coverage push is the *Library Coverage* phase. It *consumes* this phase's skill, its recipe schema and its guards. This phase proves the loop on a handful of briefs.
- **Lane L4** (generative imagery), parked by R13 and D4.
- **A batch agent and the Matter Manager.** They come after the skill (D5, and *Author a Material End to End*).
- **New OpenPBR carriers C1–C3** (metal F82, sheen/coat, anisotropy): they change the author-tier contract and need every consumer to honour them (Q6).
- **Moving drafts to `candidate` or into a release.** That stays the maintainer's call, via the existing lifecycle.
- **Assemblies** (D1). **Skin and hair** (research O9; PlatformDependencies M1).

## Questions to settle in discovery (seed vs docs)

*Each is a question under test. Pass 1 runs the four fork tests (answered? necessary? deliverable? admissible?) before any reaches the lead.*

| # | Question | First place to look |
|---|---|---|
| Q1 | **Where does a project skill live, and in what form?** `.claude/skills/<name>/SKILL.md` is the harness convention. The lanes rule makes `.claude/CLAUDE.md` read-only to working verbs; whether it also covers `.claude/skills/` is unstated. | `docs/ToolingConventions.md`, `.claude/CLAUDE.md` §Lanes, `AI_WorkingAgreement.md` |
| Q2 | **Where does a `draft` live?** An article in the source collection needs no lock entry; a texture's provenance is recorded in a release lock. Where does a draft texture's provenance evidence sit before any release pins it? | `Manifest.md` §Status lifecycle and §provenance, `_Architecture.md` (source collection vs versioned library) |
| Q3 | **Where do ambientCG downloads sit** before they are processed into `MatterLibrary/textures/`? Scratch, pin and re-fetch. The harness contract says "no network at assembly time"; fetching happens before assembly. | `AuthoringHarness.md` §contract, `ToolingConventions.md`, `.gitignore` |
| Q4 | **Channel mapping for ambientCG sets:** Color, Roughness, Normal (GL or DX?), Metalness, Opacity; Displacement and AO have no carrier. Which normal-map convention does the assembler and MaterialX `normalmap` expect? | `assemble_mtlx.py`, the MaterialX stdlib `normalmap` nodedef |
| Q5 | **Recipe home and naming** for agent-authored recipes: the same `tools/converters/recipes/` (which `build_proof_subset.py` globs), and a `vNN` per the grammar. | `NamingConventions.md`, `Identity.md` |
| Q6 | **Are carriers C1–C3 truly not-now?** Metals and coated or fabric matter then land as approximations. Does that meet the Outcome's "validated candidates", or does one carrier need to come in? | `LCDSchema.md` §Author tier, `MasterSet.md` |
| Q7 | **Risk lane.** The skill fetches third-party content and commits it to a **public** repo. The control is the provenance gate (`provenance_gate` lane plus `validate_manifest.py`). Read it: does a draft bypass it, and does that matter at `draft`? | `validate_manifest.py`, `Manifest.md`, the shipped-pixel rule |
| Q8 | **Carried from the research:** O5 (metal F82 carrier), O6 (cite where constants came from), O7 (credits for agent-authored articles), O12 (LFS, texture resolution and review-time budgets). Which of them does *this* phase actually need answered? | the research doc §Open questions |

## Notes

- **The first human test** (to write in the Brief): the lead invokes the skill in Claude Code with a brief such as "soda-lime window glass" (L1), and later "worn oak" (L3). The result is a draft article, a green gate and a render, reviewed and then kept or discarded. Measure review minutes per article (research Pass 11 estimated 5–10, unmeasured).
- **The repo is public:** a push publishes. Agent drafts land on `main` only by the lead's hand.

## Discovery Log

_(numbered passes accrue here: examined → finding → decision / hypothesis / open question)_

## Discovery Status

- **Passes captured:** 0 (seeded 2026-09-23).
- **Current working direction:** the research direction D1–D7. The Brief is not yet written.
- **Open decisions:** Q1–Q8 (under test).
- **Checks to carry forward:** re-verify every file claim above against the tree in Pass 1; the seed is context, not authority.

## Execution Log

_(populated during execution)_
