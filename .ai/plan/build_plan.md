# Matter Library — Build Plan

Lightweight phase guide for the Matter Library. This is a **standalone** project; its phase
line is independent of the IMRSV Platform's Studio/Plugin/Stage numbering and is referenced
from the platform plan as an external track.

Posture: **research / aggregate / learn / define.** Phases ADD and REFINE; they don't delete
intended design (see `.ai/conventions.md`).

Only the **Active** phase is numbered (numbers imply locked sequence). Everything under
**Upcoming** is `PhaseTBD_*` in rough working order — each gets a number when it becomes
active.

---

> **⚠ Re-based 2026-07-14.** This plan was written before the **platform** Materials wave
> (Phases 52–71) executed. That wave built most of what was listed below as "Upcoming" —
> **driving this repo directly, through platform phases rather than Matter-Library-numbered
> ones.** The delivered work is recorded under **## Delivered** so this plan stops describing
> a greenfield that no longer exists. Nothing intended has been deleted; what genuinely remains
> is still in **## Upcoming** / **## Parking Lot**.

## Active

**None — this repo has no independently-active phase line right now.** It is currently driven
by the **platform** wave: the live owner is **platform Phase 60** (production + full
experience — article **promotion**, texture **provenance**/licensing, **parity** baselines).
Track it at `IMRSV_Platform_Documentation/Planning/Phases/Phase52_60_Wave_Materials_Sequencer.md`.

---

## Delivered (by the platform Materials wave, 2026-06 → 2026-07)

Each of these was an "Upcoming" phase here; each shipped **into this repo** via a platform phase.

| Was planned as | State | Delivered by |
|---|---|---|
| **Phase 01 — Foundations** (folder structure, taxonomy, filename grammar ≤63, portable `.mtlx` metadata contract) | ✅ **DONE** | Platform **Phase 52** (`Complete/Phase52_MatterLibraryFoundation.md`) |
| **Material Catalog** (the gut-check listing) | ✅ **DONE** — and went further: the authored `matterlib-X.Y.lock.yaml` manifest is **projected** to `matterlib-X.Y.catalog.json`, the runtime catalog Stage reads | Platform **Phase 56** |
| **Five Materials, No Textures + LCD Set** | ✅ **DONE** — the deterministic MaterialX-SDK assembler (`assemble_mtlx.py`) + the **LCD parameter set**, frozen | Platform **Phase 53** |
| **Five Materials, With Textures + Texture Pipeline (LFS)** | ✅ **DONE** — `MatterLibrary/textures/{base,shared}` under Git LFS; procedural generators in `tools/converters/` | Platform **Phase 53** |
| **Overlays on the Ten** (dust / scratch) | ✅ **DONE** — overlay + maskset layers authored and consumed. ⚠ Both are **packed DATA textures, never albedo bitmaps** (a semantic defect Phase 71 found and fixed) | Platform **Phases 69 + 71** |
| **Cook the Unreal Library** | ✅ **DONE, but NOT via `bridges/unreal/`** — the 7 masters are cooked **in the Plugin repo** (`IMRSVStagePlugin`, baked by `bake_master_authortier.py`). The standalone cook project was not needed. *(If a standalone cooked library is ever wanted, that is still greenfield.)* | Platform **Phases 55 + 71** |
| **Consume in IMRSV Studio** | ✅ **DONE** — the full chain runs: article → producer → validators → Stage extractor → wire → Plugin DTO → MID → master, with save/reload and broken-material remap | Platform **Phases 54–58, 69** |
| **Validators / CI** *(was Parking Lot)* | ✅ **BUILT** — `tools/validators/run_all.py` over material / manifest / determinism / fixture-sync checks. **CI wiring** is still open | Platform **Phases 53 + 71** |
| **⭐ The two-tier LCD contract** *(never planned here — the wave discovered it was missing)* | ✅ **DONE** — the **Creator tier** (8 adjustable ports) was frozen at 53; the **author tier** (each master's *defining* property: cutoff · IOR · absorption · SSS · two-layer blend · emission) **had never been authored at all**, leaving 6 of 7 masters inert. Phase 71 built it end-to-end and gave **every one of the 7 masters a real example article** (library now at **12**) | Platform **Phase 71** |

---

## Upcoming (not yet sequenced — rough working order)

### Version Management — *partially delivered; the promotion machinery is what's left*
**Goal:** the source→approved→release machinery. **Already built:** the manifest/release schema
(`library/releases/matterlib-0.0.1.lock.yaml`), its projected runtime catalog, and the two
version axes (per-material `vNN` vs library semver). **Still open:** the **status lifecycle**
(all 12 articles are still `status: draft`), **immutability-after-promotion**, **CODEOWNERS-gated
promotion**, and the first curated release (`matterlib-1.0`). Promotion is now owned by
platform **Phase 60**.
- `.ai/phases/future/PhaseTBD_VersionManagement.md`

### Blender bridge — material library + export-preset extension
**Goal:** `bridges/blender` — the material-library `.blend` (Principled-BSDF node groups named
with exact qualified Matter names) + the **material-side** extension of the USD export preset
(the existing preset is mesh-side only). Greenfield. Owned by platform **Phase 60**, Lane 3.
- `PhaseTBD_BlenderBridge`

### Parity baselines
**Goal:** `usdrecord` previews + per-class ΔE parity bars across MaterialX / UE / Blender.
Spec text only today; no parity scene or ΔE tooling exists. Owned by platform **Phase 60**, Lane 4.
- `PhaseTBD_ParityBaselines`

---

## Parking Lot

- **Matter Manager** tooling (`tools/matter_manager` — import, promotion, subset/export, path remap).
- **Automated transformer hardening** (`bridges/blender`, `bridges/unreal` converters — after manual parity is proven).
- **Parity-gate automation** (standardized HDR-lit ΔE comparison wired as a promotion CI check).
- ~~**Validators / CI**~~ — ✅ **validators BUILT** (`tools/validators`, see ## Delivered). **CI wiring still open.**
- **Realm super-level** (Matter vs Buildings vs …) — only if a non-matter compound library lands.
- **Texture storage migration** to DAM / content-addressed pointers (manifest already allows it).
- **Additional engine targets** (others TBD).
