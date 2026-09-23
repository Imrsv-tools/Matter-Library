# Phase02 — One-Command Check

**Status:** SEEDED (2026-09-23) — phase doc exists; discovery has not opened. Numbered by the lead (`/discovery Phase 2`, 2026-09-23): the entry at the head of the Roadmap's `## Future`.

## Outcome

**Anyone can clone the library on a fresh machine, run one command, and see every material and release validate, with the result also checked automatically on every pull request.**

*(Verbatim from the Roadmap entry, written at Phase01 step 1.5.)*

Concretely, at close: a pinned environment a newcomer creates in one documented step · the structural gate `tools/validators/run_all.py` running green from a fresh clone, and saying which lanes **ran** and which **skipped** · a CI job on GitHub running the same gate on every pull request.

## Why this is a phase

Every later phase — the release bundle, version management, the contribution path — needs a gate that runs somewhere other than one person's machine and says truthfully what it checked. Today it runs nowhere: `run_all.py` fails at import on the lead's box (measured 2026-09-23: `ModuleNotFoundError: No module named 'MaterialX'`). The expensive-to-unwind choice is the **environment form** (Q1 below). Contributors, CI and every later tool inherit it.

## Scope (seed — settle at discovery)

**In:**
- **A pinned core environment:** Python, MaterialX 1.39.5, pyyaml, numpy, Pillow, plus git-lfs for the textures. This is research Pass 7's "Core" tier.
- **`run_all.py` runs green from a fresh clone**, with no path that assumes the IMRSV platform's superrepo layout.
- **Truthful lane reporting:** a run names each lane `ran` / `skipped (why)`. Today a missing tool skips and still reports green (`docs/ToolingConventions.md` §Gates and CI, Drift 2026-09-23).
- **CI on GitHub** running the gate on every pull request.
- **The `fixture_sync` lane leaves this repo, with its intent recorded.** This is already ruled: `PlatformDependencies.md` P8 names "this repo (removes it)", under R1. It stays in scope as a task, not a question.
- **Routed hygiene** that Phase01 and the specs assigned here (each carries a dated Drift / Todo / Reevaluate marker to discharge):
  - retired old-layout paths in `tools/` comments and `.mtlx` files (Phase01 §Deferral ledger);
  - `library/provenance/matterlib-0.1.0-textures.md` still cites platform phase ids (Phase01 §Deferral ledger);
  - the USD toolchain recipe comments that still describe a consumer's build (`docs/specs/Tooling/USDValidationToolchain.md`, Drift);
  - the add-on's declared Blender `(5, 1, 1)` against the 5.1.0 installed (`docs/specs/Experience/Experience_MatterLibrary.md`, Reevaluate);
  - the `run_all.py` Todo in `docs/specs/Tooling/AuthoringHarness.md` and the CI Drift in `docs/specs/_Architecture.md`.

**Not now:**
- The contribution gate (source → `candidate`) and CODEOWNERS on `library/releases/` → Contribution Path.
- A parity gate in CI (render comparison) → Parity Baselines / Parking lot.
- Any contract or schema change → Release Bundle and Consumer Contract.
- Building OpenUSD, or any Blender or Unreal lane in CI. These tiers are heavy, and the one command is the structural gate. *(Hypothesis to test at discovery, not a ruling. See Q3.)*

## Open questions (seed vs docs — run through the four tests at authoring)

| # | Question | Why it is a question (tests 1–4) |
|---|---|---|
| Q1 | **Environment form:** a `pyproject` + venv for the core tier, extending the conda `environment.yml` that already hosts the USD build, or both? *(Research Q7, "seed 2's main fork".)* | Not answered by any spec. The premise is real: no `requirements.txt` or `pyproject` exists (checked 2026-09-23). Both options are deliverable. **Research lean:** the core tier is small enough for a `pyproject` and CI with no encoder or GPU. |
| Q2 | **What does "every release validates" require of the encoder-gated lanes** (compression, staging, and the `.dds` part of the freeze)? Options: install `compressonatorcli` locally and in CI, or run without it and have the run **name** those lanes as skipped. | The premise is real: `compressonatorcli` is absent and those lanes skip (research Pass 7). **Deliverability is under test:** whether a pinned Linux `compressonatorcli` V4.5.52 can be fetched in CI has not been checked. Confirm it before offering the choice. |
| Q3 | **How far does "fresh machine" reach?** Only the core tier the one command runs, or also the hardcoded home-directory paths in `tools/conformance/` and `tools/generators/` (USD and Blender tiers)? | Research seed 2 said "hardcoded paths gone" without naming a tier. A `grep` for the home path hits ten files, all in conformance and generators, none in `tools/validators/` (2026-09-23). The Outcome's "one command" suggests core only. **Test 1 at discovery:** does any `run_all` lane import those modules? |

## Checks to carry into discovery (not forks)

- **MaterialX wheel coverage:** does PyPI `MaterialX` 1.39.5 publish wheels for the pinned Python? The system Python is 3.14 and the conda env is 3.12 (Pass 7). This decides the Python pin.
- **Git LFS in CI:** the textures are LFS. CI checkout needs LFS, and that counts against the public repo's bandwidth quota. Measure the size.
- **The lane count:** docs say "16 lanes", but the `run_all.py` docstring lists 13 + 9b. Count the `results` keys of `main()`, which is `AuthoringHarness.md`'s own measurement rule.
- **Risk lane:** a CI workflow in a **public** repo, running on pull requests from forks. Name and read the control: the workflow trigger and token permissions (`pull_request`, not `pull_request_target`; read-only token). Default `build` until that read settles it.

## Sources

- `docs/Planning/Research/260923_R_StandaloneSetup.md` — Pass 7 (toolchain tiers and findings), Pass 8 seed 2, Q7.
- `docs/ToolingConventions.md` §Entry points, §Gates and CI.
- `docs/specs/Tooling/AuthoringHarness.md` (the lanes and the Todo).
- `docs/Planning/PlatformDependencies.md` P8.
- `docs/Planning/Phases/Complete/Phase01_StandaloneBootstrap.md` §Deferral ledger.

## Discovery Log

_(numbered passes accrue here)_

## Discovery Status

- **Passes captured:** — (seeded only)
- **Current working direction:** —
- **Open decisions:** Q1–Q3
- **Checks to carry forward:** the four above

## Execution Log

_(populated during execution)_
