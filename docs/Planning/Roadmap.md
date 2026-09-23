# Matter Library — Roadmap

Lightweight phase guide. Three sections: **`## Active`** (live work) → **`## Future`** (sequenced seeds + the backlog) → **`## Complete`** (closed phases, newest at the bottom).

> **Entry format — keep it scannable.** Each entry is just: the **heading** (name + status), a one-line **`Outcome`**, and **doc pointer(s)**. The **`Outcome` is what the USER can DO when the phase is done** — the *point* of the work, in plain non-technical language (no code symbols, no implementation detail, never tech-for-tech's-sake). **Always challenge it — "is there a user-facing result?"**: default to the user-facing outcome; a pure-infra / refactor phase MAY instead state a system-capability outcome, but the challenge is never skipped. If an `Outcome` already exists, don't rewrite it unless asked. The doc pointer is the phase doc if it exists, else the known relevant docs. **ALL technical content — scope, rename maps, root-cause, hazards — lives in the phase doc, never here.** This index exists so anyone can skim the phases in seconds.
>
> **Status vocabulary:** `RESEARCH` (no phase doc yet — the pointers are the raw material) → `SEEDED` (phase doc written) → `ACTIVE` (being worked) → `COMPLETE`. A `TBD` entry is simply one the lead has not numbered — it may hold a perfectly settled position, since **order is position in the list, never an ordinal**. Numbering is the lead's call: sometimes one as work starts, sometimes a whole span when committing to a Wave (Workflow §Phase Numbering).

> **Structural cut (Phase01 step 1.1, 2026-09-23).** This registry replaced the pre-adoption `.ai/plan/build_plan.md`, which is archived verbatim at `docs/Planning/Phases/Complete/PreStandalone/build_plan.md`. Its Upcoming and Parking Lot entries are carried below as-is, pending the **re-think in Phase01 step 1.5** (lead ruling R5/R11: the roadmap is rebuilt around the library and its tools; the first phases are standing alone, being versioned, and being consumed by IMRSV).

==================================================================================
## Active

### Phase01 — Standalone Bootstrap — ACTIVE
**Outcome:** anyone can understand, navigate and work on the Matter Library from this repository alone.
- `docs/Planning/Phases/Phase01_StandaloneBootstrap.md` · research: `docs/Planning/Research/260923_R_StandaloneSetup.md`

==================================================================================
## Future

*Carried from `build_plan.md` pending the step-1.5 re-think.*

### Version Management — TBD
**Outcome:** a maintainer can promote, deprecate and retire materials across library releases, with each release reproducible forever.
- `docs/Planning/Phases/Future/PhaseTBD_VersionManagement.md`

### Parity Baselines — RESEARCH
**Outcome:** anyone can see, per material class, how closely MaterialX, Blender and Unreal renders of a material match.
- `docs/Planning/Research/260923_R_StandaloneSetup.md` (Pass 8, seed 10)

### Parking lot — TBD
**Outcome:** unsequenced ideas, kept so their intent survives (Don't Delete Spec Functionality).
- `docs/Planning/Phases/Complete/PreStandalone/build_plan.md` §Parking Lot · `docs/Planning/Research/260923_R_StandaloneSetup.md` Pass 8

==================================================================================
## Complete

### Pre-standalone — delivered by IMRSV platform phases (2026-06 → 2026-07) — COMPLETE
**Outcome:** the foundations, the authoring harness, the first 12 materials, the release machinery and the Blender library, all built into this repo by the IMRSV platform's Materials wave.
- `docs/Planning/Phases/Complete/PreStandalone/build_plan.md` §Delivered · `docs/Planning/Phases/Complete/PreStandalone/Phase01_Foundations.md`
