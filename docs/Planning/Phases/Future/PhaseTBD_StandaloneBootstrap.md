# PhaseTBD — Standalone Bootstrap

**Status:** SEED (phase doc written 2026-09-23; discovery opening in the same session, by lead invocation).

## Outcome

**Anyone, whether a contributor, a consumer or a fresh agent session, can understand, navigate and work on the Matter Library from this repository alone.** That covers what it is, its vocabulary, its contract, its licence terms and its plan, with no need for the private IMRSV platform docs.

Concretely, at close this repo has:
- the Agentic Engineering method vendored in;
- the old `.ai/` scaffold folded into the standard shape;
- the Matter-owned specs brought home and scrubbed for a public repo;
- a Glossary on day one;
- Apache-2.0 (code) and CC0-1.0 (content) licences plus a CONTRIBUTING guide;
- an identity-only README;
- a Roadmap seeded for what comes next;
- a list of the asks this repo has of its consumers.

## Why this is a phase

It is one user-facing result: *the repo stands on its own*. Nothing in it builds or changes the library's tools or payload. It is also the first phase of this repo's own phase line, so every later phase depends on the vocabulary, spec layout and roadmap it sets.

The expensive-to-unwind choices are:
- **where the specs live** (every consumer's pointers will target it);
- **glossary terms** (Conway's Variant: names propagate into the system);
- **what goes public** (a public commit cannot be taken back).

## Scope

**In:**
- Vendor the method from `PeteSmalls/agentic-engineering`: `.ai/`, `.claude/`, commands, Methodology, templates, the provenance stamp, `LOCAL_DELTAS.md`, and `.claude/settings.json`.
- Fold in the existing `AGENTS.md`, `.claude/CLAUDE.md`, `.ai/{context,conventions}.md`, `.ai/commands/{howdy,housekeeping}.md`, `.ai/plan/*`, `.ai/phases/*`, `.ai/research/*`, `Readme.md` and `FolderStructure.txt`, moving them with history and without dropping intent.
- Bring home the Matter-owned specs from the platform's `MatterLibrary/` tree, rewritten for a public repo (no private links, issue numbers, names, paths or ABI internals).
- `docs/Glossary.md` + `docs/NamingConventions.md`, reusing IMRSV wording where it applies (R16).
- LICENSE (Apache-2.0, code), a CC0-1.0 content dedication, CONTRIBUTING (CC0 affirmation + credit norm), and a credits record.
- `docs/Planning/Roadmap.md` seeded from the research's candidate list (audited against §What counts as ONE phase).
- `docs/Planning/PlatformDependencies.md`: the asks of Stage/Plugin/Studio/USDLiveView and the platform docs.
- Small hygiene: the tracked `stage.log`, the `.gitignore` gaps.

**Not now:**
- Fixing tool code: hardcoded paths, the pinned environment, CI (the one-command-check phase).
- The release bundle and consumer contract build (a later phase).
- Any edit in another repo. The platform-side pointer changes are *listed* in `PlatformDependencies.md`, not made.
- Tagging or re-versioning releases (research Q5).

## Seed questions (tested at authoring)

1. **Spec layout:** `docs/specs/{Ontology,Contract,Catalog,Authoring,Distribution,Tooling,Experience}` mirroring the platform tree, or flatter? (research Q1)
2. **Platform research docs** (MaterialChain, MaterialsBuildGrounding, OpenMatterCreatorPipeline): migrate them, or distil their settled decisions into the specs and cite them as platform history?
3. **Phase numbering:** does this phase get a number, and does this repo's line restart at `Phase01`? (research Q6; the lead's call)

## Sources

- Research + lead rulings R1–R16: `docs/Planning/Research/260923_R_StandaloneSetup.md`, the one authoritative copy.
- Method upstream: `PeteSmalls/agentic-engineering` @ `a6e7e81` (`ADOPTING.md`, `Methodology/AgenticEngineering_ProjectFolders.md` §Setup Checklist).

## Discovery Log

_(passes accrue here)_

## Discovery Status

- **Passes captured:** —
- **Current working direction:** —
- **Open decisions:** seed questions 1–3
- **Checks to carry forward:** —

## Execution Log

_(populated during execution)_
