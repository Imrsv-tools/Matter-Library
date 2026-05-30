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

## Active

### Phase 01 — Foundations: Folder Structure, Taxonomy & Naming — PLANNING
**Goal:** Lay out the full folder structure and taxonomy, lock the filename grammar, and fix
the **portable `.mtlx` metadata contract** (identity + scale live in the file; version + status
live in the manifest later). The contract layer everything else builds on. No master
materials, textures, or manifest tooling this phase.
- `.ai/plan/Phase01_Foundations.md`

---

## Upcoming (not yet sequenced — rough working order)

### Material Catalog (gut-check)
**Goal:** A chart/listing of all the materials we want to start with — Domain/Class, filename,
assigned master material, scale tag, and whether it needs textures/overlays. The artifact that
gut-checks the taxonomy, naming, and scale model before we author anything.
- `PhaseTBD_MaterialCatalog` (doc created when it becomes active)

### Five Materials, No Textures + LCD Set
**Goal:** Author ~5 textureless materials spanning different master-material types; define the
**LCD parameter set** and a minimal master-material representation; validate
MaterialX → UE (Substrate) → Blender (Principled BSDF) **visual parity** (manual conversion is
fine at this stage). First real tracer bullet.
- `PhaseTBD_FiveMaterialsNoTextures`

### Five Materials, With Textures + Texture Pipeline (LFS)
**Goal:** Stand up `textures/{base,shared}` under Git LFS; texture-set naming/versioning, scale
tagging, material→texture reference + path-remap contract; author ~5 textured materials and
re-run the cross-engine parity test.
- `PhaseTBD_FiveMaterialsTextured`

### Overlays on the Ten (dust / scratch)
**Goal:** Add overlay/maskset layers (dust, scratches) to the ~10 materials and validate the
layered result across MaterialX / UE / Blender. Master materials gain overlay support.
- `PhaseTBD_Overlays`

### Cook the Unreal Library
**Goal:** The standalone UE cook project (`bridges/unreal/`, UE 5.7+ / Linux 5.6.1) packages
the ~10 materials into a cooked, referenceable Substrate library.
- `PhaseTBD_CookUnrealLibrary`

### Consume in IMRSV Studio
**Goal:** Make the cooked library usable inside IMRSV Studio. This is the cross-repo handoff —
it kicks off a series of **Studio-side** phases (platform-numbered, tracked in the platform
build plan: `Service_MaterialX`, `Service_MaterialManager`, the material panels/modals).
- `PhaseTBD_StudioConsumption` (Matter-Library side); Studio side lives in platform plan.

### Version Management
**Goal:** Build the source→approved→release machinery: the **manifest/release schema**
(`library/releases/matterlib-X.Y.lock.yaml`), semver rules, status lifecycle, immutability,
CODEOWNERS-gated promotion, and the first curated release (`matterlib-1.0`). Detailed design
already drafted at `.ai/phases/future/PhaseTBD_VersionManagement.md`.
- `.ai/phases/future/PhaseTBD_VersionManagement.md`

---

## Parking Lot

- **Matter Manager** tooling (`tools/matter_manager` — import, promotion, subset/export, path remap).
- **Automated transformer hardening** (`bridges/blender`, `bridges/unreal` converters — after manual parity is proven).
- **Parity-gate automation** (standardized HDR-lit ΔE comparison wired as a promotion CI check).
- **Validators / CI** (`tools/validators` — schema/naming/scale/reference checks).
- **Realm super-level** (Matter vs Buildings vs …) — only if a non-matter compound library lands.
- **Texture storage migration** to DAM / content-addressed pointers (manifest already allows it).
- **Additional engine targets** (others TBD).
