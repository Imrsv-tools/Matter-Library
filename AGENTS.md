# Matter Library — Agents Entry Point

Pointer-first onboarding for AI agents (Claude, Codex, others). The Matter Library is **a community, single-source MaterialX material library and its toolset: materials are authored once and published as versioned releases that Blender, Unreal-based apps (such as IMRSV), USD viewers and others consume.** **⛔ Root the session at the repo root before anything else.** `.claude/commands/` only loads from there, so a session started one level up sees a perfectly normal repo, reads these docs correctly, and **has no verbs at all**: `/research`, `/quick-fix`, `/discovery` and `/howdy` simply do not exist. The failure is silent. The likely outcome is an agent hand-emulating each command by reading its file as a document, never learning that the real thing was sitting right there. If you cannot invoke `/howdy`, check this first.

Read in this order:

1. `.ai/AI_Orientation.md` — identity, repo map, build/test entry points.
1b. `docs/specs/_Architecture.md` — **the canonical product contract** (what the library is, and the rules it keeps). Read before proposing architecture.
2. `.ai/AI_WorkingAgreement.md` — the engineering agreements.
3. `docs/Planning/Roadmap.md` — the phase registry.
4. `Methodology/AgenticEngineering_Workflow.md` §How we work — how work runs here.
5. `.ai/commands/howdy.md` — onboarding command behavior.

## Howdy Shortcut

When the user types `howdy` or `/howdy` in this repo, follow `.ai/commands/howdy.md`.

## Structural model (the one fact to internalize)

`.ai/` owns **agent operation** and stays **thin**. The full **`Planning/` surface** lives at **`docs/Planning/`**, alongside the durable **product** specs in `docs/specs/` (both in `docs/`, never in `.ai/`). The carried methodology blueprint lives in `Methodology/`.

**One repo, no submodules of its own.** Every commit is a single-repo commit. This repo is a **producer**: other projects consume its published releases, not its checkout. The IMRSV platform still registers it as a submodule during the transition; that is the platform's business, not a step here (`.ai/commands/LOCAL_DELTAS.md`). Full model: `Methodology/AgenticEngineering_DocumentationMap.md`.

## Codebase search (zero permission prompts)

Prefer the session's own **Grep / Glob / Read** tools; they never prompt. For big sweeps, fan out **in parallel** with Bash-less search agents (prompt them "use ONLY Read/Grep/Glob/LS"). **Never use a search agent that has the Bash tool**: it shells out and prompts on every call. The full rule is in `.claude/CLAUDE.md`.

## Heritage

Methodology carried from [`PeteSmalls/agentic-engineering`](https://github.com/PeteSmalls/agentic-engineering) on 2026-09-23 (upstream `9f52c7f`). Local divergences are recorded in `.ai/commands/LOCAL_DELTAS.md`. Frictions with the *portable methodology itself* are filed upstream; project-internal retros stay in `docs/Planning/Support/WorkflowFeedback/`.
