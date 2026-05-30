# Matter Library — Agents Entry Point

Start here. This is a **standalone** IMRSV project: it owns its full planning surface in `.ai/` (it is also a git submodule of `Imrsv-tools/IMRSV_Platform`).

## Read First

1. `.ai/context.md` — identity, what's built vs planned, active phase.
2. `.ai/conventions.md` — rules & boundaries for this repo.
3. `.ai/plan/build_plan.md` — phase guide; find the Active phase.
4. `.ai/commands/howdy.md` — onboarding behavior.

## What This Repo Is

The **Matter Library**: a MaterialX single-source material library with a two-tier model —
a **volatile source collection** (community-contributable, under a matter taxonomy) and a
**controlled, curated, versioned library** (manifest + git tags). Materials are transformed
into Unreal (Substrate) and Blender (Principled BSDF) targets that look as close as possible
across engines (LCD approach).

## Golden Rules

- Read context before acting.
- **ADD or REFINE, don't DELETE** intended design just because it isn't built yet (see conventions §Don't Delete Spec Functionality). This repo is in research/define phase.
- MaterialX is the single source of truth; LCD parity across targets.
- Source = volatile/open; the versioned library (manifest) = controlled.
- Keep planning in `.ai/`; keep this repo's docs consistent.

## Platform Context

Cross-project platform planning lives at the **platform** repo (`IMRSV_Platform/.ai/`). This
repo is referenced there as an **external track**. Durable platform specs live in
`IMRSV_Platform_Documentation/`.
