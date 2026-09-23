# Matter Library — Architecture

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs, and merged with the design principles previously held in this repo's `.ai/conventions.md` and `.ai/context.md`. **This repo is now the authority** for the Matter Library's architecture and contract; consumers point here.

The **Matter Library** is a **community, CC0 library of physically based "matter" materials** (Limestone, Copper, Glass, …) **plus** the machinery to author, curate, version, validate and publish them. Materials are authored once in **MaterialX** (`open_pbr_surface`, 1.39: the single source of truth) and published as **versioned releases** that consumers use: Blender, Unreal-based apps such as IMRSV, and MaterialX-aware USD tools. The aim is *"author once, render close to the same everywhere."*

This doc is the **growth anchor**. It names every component and points at each component's spec. It is the product contract that `AGENTS.md` sends every agent to first.

---

## System overview

```
                     AUTHORING (the Authoring Golden Path — Authoring/)
   generate a tileable albedo → decompose to PBR maps → assemble the OpenPBR .mtlx (+ QC)
                                      |
                                      v
   +----------------------------------------------------------------+
   |                      SOURCE COLLECTION                          |
   |   one .mtlx per article (single-file open_pbr_surface 1.39)     |
   |   + base / overlay / mask textures, organised by Domain/Class   |
   +--------------------------------+-------------------------------+
                                    | curate (a manifest pins versions)
   +--------------------------------v-------------------------------+
   |                   CURATED, VERSIONED RELEASE                    |
   |   matterlib-X.Y.Z.lock.yaml → catalog · freeze · approval       |
   +--------------------------------+-------------------------------+
                                    | publish (release bundle — planned)
   +--------------------------------v-------------------------------+
   |            CONSUMERS (resolve by Matter identity)               |
   |   Blender (this repo's add-on + library) · IMRSV (Stage runtime, |
   |   UE plugin, Studio) · USD viewers (usdview, USDLiveView)        |
   +----------------------------------------------------------------+
```

**This repo is a producer** (lead ruling R1, 2026-09-23). Consumers install a **published release** and never read this repo's working tree. How each consumer resolves and renders a material is that consumer's own spec; see [Consumers](Consumers.md).

> **Drift (2026-09-23):** today the IMRSV consumer still assembles its install from this repo's checkout (a hand-synced mirror of the catalog and `.mtlx` files, plus textures copied from the tree). The **release bundle** that replaces this is *(planned)*, owned by the release-bundle / consumer-contract phase (R1/R14). The asks are listed in `docs/Planning/PlatformDependencies.md`.

### Key characteristics

- **MaterialX is the single source of truth.** Each article is `open_pbr_surface` 1.39, self-contained in one file. Blender and Unreal representations are **derived**, never hand-authored as the master.
- **Identity is the qualified Matter name.** A composition carries the name; consumers resolve it to the real library material ([Identity](Ontology/Identity.md)). Identity and adjustments ride standard USD carriers: names, bindings, shader `inputs:`.
  > **Reevaluate (2026-09-23):** the principle "no `imrsv:` custom USD attributes for materials" sits in tension with the release pin `imrsv:matterlibRelease` (a composition-level key). Owned by the release-bundle / consumer-contract phase.
- **A release is a manifest, not a copy.** The lockfile pins each material and texture version, so carry-forward and back-compat come for free ([Manifest](Contract/Manifest.md)).
- **Two version axes:** material `vNN` (in the name) vs library release semver, never conflated.
- **Curated, not just collected.** A volatile community source collection feeds a controlled, CI-gated, versioned library.
- **LCD parity.** Only parameters every target can honour are exposed, and masters bridge the per-target gaps ([LCD schema](Contract/LCDSchema.md)).

---

## Component map

The Matter Library is a **gathering of components, organised by concern**. Each row names the component, its spec, and where it lives in this repo.

| Component | Concern | Spec | In the repo |
|---|---|---|---|
| **Ontology** | taxonomy · identity grammar · master set | [Taxonomy](Ontology/Taxonomy.md) · [Identity](Ontology/Identity.md) · [MasterSet](Ontology/MasterSet.md) | the folder layout of `MatterLibrary/` |
| **Contract** | OpenPBR template · manifest schema · runtime-catalog schema · LCD schema · Creator asset profile | [MaterialXTemplate](Contract/MaterialXTemplate.md) · [Manifest](Contract/Manifest.md) · [RuntimeCatalog](Contract/RuntimeCatalog.md) · [LCDSchema](Contract/LCDSchema.md) · [CreatorAssetProfile](Contract/CreatorAssetProfile.md) · [examples](Contract/examples/) | `MatterLibrary/materials/`, `library/releases/` |
| **Catalog** | the curated set, human-readable | [Catalog](Catalog/Catalog.md) | `library/releases/*.catalog.json` |
| **Authoring** | the Authoring Golden Path (generate → decompose → assemble), provenance, future tooling | [AuthoringGoldenPath](Authoring/AuthoringGoldenPath.md) | `tools/converters/`, `library/provenance/` |
| **Distribution** | stage · freeze · approve · activate · rollback; the install layout and selector | [ReleaseModel](Distribution/ReleaseModel.md) | `tools/releases/`, `library/releases/` |
| **Tooling** | the authoring harness and validators · the USD validation toolchain · compression and parity | [AuthoringHarness](Tooling/AuthoringHarness.md) · [USDValidationToolchain](Tooling/USDValidationToolchain.md) · [CompressedDistribution](Tooling/CompressedDistribution.md) | `tools/` |
| **Blender bridge** | the Asset-Browser library and the Matter exporter | [Experience §Shipped](Experience/Experience_MatterLibrary.md) · [CreatorAssetProfile](Contract/CreatorAssetProfile.md) | `blender/`, `tools/generators/`, `tools/conformance/` |
| **Matter Manager** *(planned)* | import · promotion · subset/export · path remap | — | — |
| **Automated transformers** *(planned)* | MaterialX → Blender / Unreal, after manual parity is proven | — | — |
| **Unreal deliverable** *(planned, optional)* | a reference UE masters package for Unreal users outside IMRSV (R14 "B later") | — | — |

> **Experience** ([Experience_MatterLibrary](Experience/Experience_MatterLibrary.md)) is the **product/UX** view (the Creator Golden Path), distinct from this architecture/contract view. It links to the Contract and Ontology specs; it does not restate them.

---

## How the pieces fit (the spine: the identity contract)

Every link in the chain consumes or produces the **identity contract**: the qualified Matter name carried by the material name itself ([Identity](Ontology/Identity.md)).
1. Authoring produces a named `.mtlx`.
2. The manifest pins its version.
3. Distribution makes it resolvable.
4. Consumers bind by that name and resolve to the real material.

The [master set](Ontology/MasterSet.md) defines **what a Matter material can be**: a template instance ("master X + these textures + these LCD values"), not arbitrary node soup. So a material that doesn't fit is caught at authoring/CI time, never at runtime.

The **LCD discipline** is two-tier ([LCDSchema](Contract/LCDSchema.md)). The **author tier** is what a material author sets: maps, metallic, roughness, IOR, and each master's defining property. The **Creator tier** is the frozen 8-port subset an end user may adjust: tint, UV placement, overlay density, maskset blend, roughness bias. Both use the same OpenPBR-named inputs, for two audiences.

> **Drift (2026-09-23):** under R14 the **master contract** — the master set, parameter names, texture roles and the per-article master token — is published **as data** in each release, so a consumer never hard-codes class → master routing. Today the token lives only in each `.mtlx`'s `imrsv_metadata` hint and the IMRSV consumer routes in code. Owned by the release-bundle / consumer-contract phase.

---

## Design principles

*(Carried from this repo's `.ai/conventions.md`, 2026-09-23.)*

### Least Common Denominator (LCD)
- Expose only parameters every target (MaterialX / Unreal with Substrate / Blender Principled BSDF) can honour. If one target can do something the others can't, don't rely on it.
- Masters are where per-target gaps are bridged, so the visible result stays close (target ΔE < 2 under standardised lighting, where the master allows; see [CompressedDistribution](Tooling/CompressedDistribution.md) for the per-class bars).

### Two-tier library (source vs versioned)
- The **source collection** is volatile and community-contributable under the matter taxonomy.
- The **versioned library** is curated. A release = `library/releases/matterlib-X.Y.Z.lock.yaml` plus a git tag. *(Drift, 2026-09-23: no git tags exist yet; they are created as needed, per R8.)*
- **Promotion** edits the manifest; it does not copy files. Carry-forward: the next manifest keeps the same pins for unchanged articles.
- **Promotion model A:** manifest + tags in one repo, with the CODEOWNERS-gated manifest as the control point. It upgrades to a separate library repo later without re-architecting. *(Drift, 2026-09-23: no CODEOWNERS file exists yet.)*

### Versioning
- **Two axes:** per-material/texture `vNN` (contributor) vs library release semver (maintainer).
- **Library semver:** MAJOR = breaking (an LCD or master parameter change, a change in what a scale tag means, a material retired); MINOR = additive; PATCH = a drop-in visual fix.
- **Status lifecycle:** draft → candidate → approved → deprecated → retired.

### Immutability after promotion
- Once `material@vNN` (or `texture@vNN`) ships in any released manifest, that file is frozen. A change is **always** a new `vNN+1`, never an in-place edit, which keeps old releases reproducible and back-compat real.

### Textures
- Tracked with **Git LFS**. Stored once under `MatterLibrary/textures/base` (by the matter hierarchy) and `MatterLibrary/textures/shared` (overlays, masks), and referenced by many articles.

### Governance
- Source PRs are open but **CI-gated**: schema valid, naming/taxonomy valid, scale tag present, referenced textures exist, eventually an automated parity render. *(Phase02, 2026-09-23: `tools/validators/run_all.py` runs strict on every pull request via `.github/workflows/gate.yml`; the parity render is still (planned). Todo, 2026-09-23: GitHub Actions is disabled on the repository, so no run has happened yet. What makes a PR's material a `candidate` is the contribution-path phase's.)*
- The release manifests under `library/releases/` are **maintainer-gated**: only maintainers promote.
- **Contributions are CC0-1.0 and must be CC0-dedicable**; contributors are credited, and consumers are asked (not required) to credit the Matter Library (R13). Code is Apache-2.0 (R10).

### Targets
- **Blender 5.1+** (R6) · **Unreal 5.8+ with Substrate** (R15) · MaterialX 1.39 / OpenUSD for the USD path. Other engines are TBD, welcomed with community support.

---

## Decisions of record

The settled technical decisions this architecture rests on. They were first reached in the IMRSV platform's material-chain research (2026-06) and are **distilled here rather than migrated** (lead ruling, 2026-09-23). Each is stated as the decision plus its reason.

| # | Decision | Why |
|---|---|---|
| 1 | **The article shader is `open_pbr_surface`** (OpenPBR, MaterialX 1.39+). | OpenPBR is the ecosystem's uber-shader direction: bundled in USD, native in major DCCs, and the model Blender's Principled BSDF is based on. `standard_surface` ↔ OpenPBR translation graphs exist. |
| 2 | **Name budget: ≤63 characters of `[A-Za-z0-9_]`.** | Blender truncates material names at 63 bytes and sanitises other characters to `_` on USD export, and names that sanitise identically collide silently ([Blender #124263](https://projects.blender.org/blender/blender/issues/124263)). |
| 3 | **UV placement is geometry, not a Mapping node.** | Blender's USD exporter drops the Mapping node, so per-object placement is done with mesh UVs, and downstream adjustment uses the LCD UV inputs. |
| 4 | **Binding purposes:** the canonical MaterialX material on the all-purpose `material:binding`; a preview approximation on `material:binding:preview`. | USD viewers do not reliably honour `:full`; this pattern matches Blender's own dual export. |
| 5 | **Textures ship offline-precompressed (BCn), not compressed at runtime and not as engine-cooked packages.** | Runtime compression is unavailable in shipping engine builds, and cooked packages lock to one engine version. Precompressed mip chains load directly with zero engine cooking. |
| 6 | ~~Unreal masters target the legacy material model for v1; Substrate deferred.~~ **Superseded 2026-09-23 by R15: Unreal 5.8+ with Substrate.** | The original deferral was for Substrate's maturity and VR issues in 5.6/5.7. The surviving part: **the master contract (names, parameters, LCD mapping) is the stable artifact; the renderer implementation swaps.** |
| 7 | **One self-contained `.mtlx` file per article.** | Multi-file include chains fail to find node definitions in some USD viewers (OpenUSD issues #1636 / #1586). A consumer must also set the MaterialX standard-library search path for its USD build. |
| 8 | **Resolution uses the stock USD search path.** A bare `@Name.mtlx@` resolves through `ArDefaultResolver` and `PXR_AR_DEFAULT_SEARCH_PATH`, with no custom resolver. | Works everywhere USD does. Gotcha: the current directory is searched first and can shadow an install. |
| 9 | **Viewers approximate transmission and subsurface.** TranslucentThick and Subsurface get a "recognisable, not ΔE < 2" bar in real-time USD viewers; `usdrecord` suits the thumbnail pipeline. | Real-time rasterisation cannot path-trace these lobes. |

---

## Spec tree

```
docs/specs/
├── _Architecture.md      this doc — component map, how the pieces fit, decisions of record
├── _Docs_Index.md        navigation index
├── Consumers.md          the producer/consumer boundary: what stays in each consumer's own docs
├── Experience/           Experience_MatterLibrary.md (the product/UX view)
├── Ontology/             Taxonomy.md · Identity.md · MasterSet.md
├── Contract/             MaterialXTemplate.md · Manifest.md · RuntimeCatalog.md · LCDSchema.md · CreatorAssetProfile.md
│   └── examples/         a verbatim live article kept as the reference
├── Catalog/              Catalog.md (the pilot release, human-readable)
├── Authoring/            AuthoringGoldenPath.md
├── Distribution/         ReleaseModel.md
└── Tooling/              AuthoringHarness.md · USDValidationToolchain.md · CompressedDistribution.md
```

## Cross-references

- [Docs Index](_Docs_Index.md) · [Consumers](Consumers.md) · [Glossary](../Glossary.md) · [Naming Conventions](../NamingConventions.md)
- The decision record for the library model (manifest-not-copy, promotion model A, LFS, governance): `docs/Planning/Research/260530_R_LibraryArchitecture.md`
- The standalone rulings R1–R16: `docs/Planning/Research/260923_R_StandaloneSetup.md` §Resolved

## History

- 2025-11 → 2026-05 — the library model, taxonomy and filename grammar were designed in this repo's Readme and planning docs.
- 2026-06 — the IMRSV platform promoted and corrected that design into its own durable specs: 7 masters (not 5), `open_pbr_surface` (not `standard_surface`), the 63-character name budget. It then built the harness, the articles and the release machinery into this repo (2026-06 → 2026-07).
- 2026-09-23 — the specs came home. This repo became a standalone producer and the authority for its own contract.
