# Matter Library — Orientation

> **Job:** session-start orientation: what this is, where everything lives, how to work in it. This `.ai/` is the **agent-operational entrypoint** (thin); durable planning lives in `docs/Planning/`. For *which doc owns what*, see `Methodology/AgenticEngineering_DocumentationMap.md`.
>
> **⛔ Prerequisite: the session must be rooted at the repo root.** `.claude/commands/` only loads from there. Rooted one level up, none of the verbs exist and the failure is silent (see `AGENTS.md`).

## Identity

The Matter Library is **a community-driven, single-source material library and the toolset around it.**
- Materials are authored once in **MaterialX** (OpenPBR, `open_pbr_surface`, 1.39) under a physical-matter taxonomy.
- They are curated into **versioned releases** (a manifest that pins exact material and texture versions).
- They are published so that any renderer can consume them and look as close as possible to every other: Blender, Unreal-based apps such as IMRSV, USD viewers and more.
- Content is CC0; code is Apache-2.0.

**What the project is**, meaning its invariants, contract and boundaries, is in **`docs/specs/_Architecture.md`**. `Readme.md` is a front door that points there and deliberately does not restate it. **Where the project stands** is in neither: read `docs/Planning/Roadmap.md`. *(This file deliberately carries no summary of the active phase or of what exists vs what is planned. A copy here would go stale on its own schedule; the Roadmap is the registry.)*

- Local root: `/home/peter/Documents/_GIT_IMRSV/Matter-Library`.
- Remote: **`Imrsv-tools/Matter-Library` — public**, default branch `main`, Issues enabled (checked 2026-09-23 with `gh repo view`).

### Relationship to other projects
- **This repo is a producer.** Consumers take its **published release bundles**, never its working tree. They are the IMRSV platform (Stage runtime · UE plugin · Studio), Blender users, and USD viewers such as USDLiveView.
- The asks between this repo and its consumers are listed in `docs/Planning/PlatformDependencies.md`.
- Consumer-side behaviour (how IMRSV loads and renders a material) is specified in the consumer's own docs, not here.

## Working Mode

**Still building, not in production** (lead, 2026-09-23). Favour the smallest unit that fits:
- a **Quick Fix** for a self-contained change;
- a **phase** when the work grows a plan;
- `/research` when a question is worth keeping.

The Roadmap (`docs/Planning/Roadmap.md`) is the phase registry. Each phase gets a doc under `docs/Planning/Phases/`. The phase line is this repo's own, starting at Phase01; earlier work was done by IMRSV platform phases and is archived under `docs/Planning/Phases/Complete/PreStandalone/`.

## Repository Layout

```text
Matter-Library/
├── AGENTS.md, .claude/CLAUDE.md, Readme.md   # entry points
├── .ai/                                    # Working tier — agent-operational truth (THIN — no planning)
│   ├── AI_Orientation.md  (this file)
│   ├── AI_WorkingAgreement.md              # engineering agreements
│   ├── README.md                           # accepted-folder registry
│   └── commands/                           # the VERBS you invoke
│       ├── howdy.md
│       ├── LOCAL_DELTAS.md                  # where this project diverges from upstream — READ THIS
│       └── research·discovery·plan·execute(+_test,_repair,_close,_highrigor)·quick-fix·peer-review·retro·issue-create·workflow-refiner
├── Methodology/                            # Durable tier — the carried AgenticEngineering blueprint
├── docs/                                   # Durable tier — planning + product/spec home
│   ├── specs/                               #   the product contract (architecture, ontology, contract, distribution, tooling)
│   ├── Planning/
│   │   ├── Roadmap.md                       #   phase registry — ## Active / ## Future / ## Complete
│   │   ├── Phases/{Future,Complete}/
│   │   ├── Research/                        #   YYMMDD_R_*.md investigations + decisions
│   │   └── Support/{Troubleshooting,WorkflowFeedback}/
│   ├── Glossary.md                          # the project vocabulary (one line per term)
│   └── NamingConventions.md · ToolingConventions.md · CodingStandards.md · Learnings/
├── MatterLibrary/                          # the CONTENT (CC0): materials/ (.mtlx by Domain/Class) + textures/ (Git LFS)
├── library/                                # releases/ (lock.yaml · catalog.json · freeze · approval) + provenance/
├── tools/                                  # converters · validators · releases · compressors · conformance · generators · preview_generators · usd-toolchain
└── blender/                                # the Blender add-on (addons/imrsv_lcd_export) + the Asset-Browser library
```

## Build / Test / Deploy

- **The structural gate:** `python tools/validators/run_all.py` (16 lanes). **Measured 2026-09-23: it fails at import on the lead's box**, because the MaterialX Python module is installed neither in the system Python nor in the `imrsv-usd-tools` conda env. `compressonatorcli` is also absent, so the compression and staging lanes skip. Making this run on a fresh box is the one-command-check phase (Roadmap).
- **Toolchain recipe:** `tools/usd-toolchain/` (OpenUSD 26.03 + MaterialX 1.39.5 in the conda env `imrsv-usd-tools`). Blender 5.1+ runs the add-on and the Asset-Browser generator.
- **Releases:** the lifecycle scripts are in `tools/releases/`; the records are in `library/releases/`.
- `docs/CodingStandards.md` is still a stub. It gets written when a phase first rules on how code is written here.

## Documentation Pointers

- `docs/specs/_Architecture.md` — what this project is and the contract it keeps.
- `docs/Glossary.md` — the project vocabulary. It is load-bearing: use the established term, or fix it there first.
- `docs/Planning/Roadmap.md` — phase registry (Active / Future / Complete).

**The stack tier: this file names the ROLE, those docs hold the CONTENT.** Each states its own arrival trigger and is deliberately empty until then (`Methodology/AgenticEngineering_Workflow.md` §Where stack knowledge lives):

- `docs/specs/` — what the system IS (this project's `docs/architecture/`; see `LOCAL_DELTAS.md`).
- `docs/CodingStandards.md` — how code is written here. **A stub, deliberately empty.**
- `docs/ToolingConventions.md` — where scripts, fixtures and CI entry points live.
- `docs/NamingConventions.md` — the filename grammar, scale tags, casing and id series. **Active.**
- `docs/Learnings/<Domain>/` — what the technology did that surprised us. **Arrives on the first lesson actually paid for here.**
- `Methodology/AgenticEngineering_Workflow.md` — the canonical Workflow Cycle.
- `Methodology/AgenticEngineering_DocumentationMap.md` — which doc owns what.
- `Methodology/AgenticEngineering_ProjectFolders.md` — the blueprint this repo was built from.

## Heritage

Methodology carried from [`PeteSmalls/agentic-engineering`](https://github.com/PeteSmalls/agentic-engineering) on 2026-09-23 (upstream `9f52c7f`).
- This project keeps its **own** session-memory namespace. Durable facts belong in *these* docs, not in the originating repo's memory.
- Read the commands *for method*. Where an assumption doesn't fit, adapt, record it in `.ai/commands/LOCAL_DELTAS.md`, and file the friction via `/retro` → `/workflow-refiner`.
- The pre-adoption scaffold (`.ai/context.md`, `.ai/conventions.md`, `.ai/plan/`, `.ai/phases/`, `.ai/research/`) was folded into this shape with `git mv` on 2026-09-23 (Phase01 step 1.1).
