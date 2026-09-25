# Consumers — the producer / consumer boundary

> **Written 2026-09-23** (Phase01 step 1.3). The Matter Library is a **producer** (lead ruling R1): consumers take its **published releases** and specify their own side in their own docs. This page says **what each consumer owns** and **which part of this repo's contract it binds to**, so a spec here never has to describe a consumer's internals. When a consumer needs something from this repo, or this repo needs something from a consumer, it is recorded in `docs/Planning/PlatformDependencies.md`.

## What every consumer binds to

Whatever the consumer, the contract it reads from this repo is the same:

| It reads | Spec |
|---|---|
| the **identity**: the qualified Matter name, Domain/Class, scale tag, `vNN` | [Identity](Ontology/Identity.md) · [Taxonomy](Ontology/Taxonomy.md) |
| the **master set** and each article's **master token** | [MasterSet](Ontology/MasterSet.md) |
| the **article format**: single-file `open_pbr_surface` `.mtlx`, render-role texture nodes | [MaterialXTemplate](Contract/MaterialXTemplate.md) · [LCDSchema](Contract/LCDSchema.md) |
| the **parameters**: the author tier and the frozen 8-port Creator tier | [LCDSchema](Contract/LCDSchema.md) |
| the **release**: runtime catalog, install-root layout, active-release selector | [RuntimeCatalog](Contract/RuntimeCatalog.md) · [ReleaseModel](Distribution/ReleaseModel.md) |
| **compressed textures**: role → BC format and colour space | [CompressedDistribution](Tooling/CompressedDistribution.md) |
| **Creator assets** exported from Blender | [CreatorAssetProfile](Contract/CreatorAssetProfile.md) |

> **Drift (2026-09-23):** consumers should receive all of the above as **one published release bundle** plus **the master contract as data** (R14). Both are *(planned)*, owned by the release-bundle / consumer-contract phase. Until then the IMRSV consumer assembles its install from this repo's checkout.

## Blender — owned by this repo

The Blender leg is produced here, so its behaviour is specified here, not deferred to a consumer:
- the Asset-Browser library and the `MatterLCD_<id>` proxies ([Experience §Shipped](Experience/Experience_MatterLibrary.md));
- the Matter exporter's lightweight and complete-portable forms ([CreatorAssetProfile](Contract/CreatorAssetProfile.md)).

Target: **Blender 5.1+** (R6).

## IMRSV — Stage runtime, UE plugin, Studio

IMRSV is the first and largest consumer. The following topics were **moved out of these specs** when they came home, because IMRSV owns them. They are specified in IMRSV's own documentation, which is private and not reproduced here.

| Topic | Owner inside IMRSV | Which Matter contract it implements |
|---|---|---|
| **Token → Unreal asset** (`M_MasterMaterial_<Token>`) and resolving an article to its master at render time | UE plugin | [MasterSet](Ontology/MasterSet.md) tokens; the article's own declared token, never its class (§Master resolution, 2026-09-23; [PlatformDependencies](../Planning/PlatformDependencies.md) P4) |
| **Unreal material settings per master** (blend mode, shading model, two-sided, refraction) and how the masters are built | UE plugin | MasterSet's renderer-neutral settings. Target **Unreal 5.8+ with Substrate** (R15). |
| **TwoLayer rendering**: rebuilding the layer blend in an engine that doesn't evaluate the MaterialX graph | UE plugin + Stage | MasterSet's TwoLayer blend formula |
| **Parameter naming on the engine side** (how LCD and author-tier names map to engine material parameters) | Stage + UE plugin | [LCDSchema](Contract/LCDSchema.md). Keeping Creator ports distinct from author-tier values is part of the consumer's contract. |
| **Extracting an article's values and textures** from the composed USD, and carrying them to the renderer | Stage | [LCDSchema](Contract/LCDSchema.md) render-role nodes; [MaterialXTemplate](Contract/MaterialXTemplate.md) |
| **Compressed-texture transport and loading** (which roles arrive compressed, how they are uploaded, the uncompressed fallback) | Stage + UE plugin | [CompressedDistribution](Tooling/CompressedDistribution.md) role table |
| **Installing a release and discovering it at runtime** (install root, reading the selector, the dev-fixture fallback) | Stage + the Studio deploy tooling | [ReleaseModel](Distribution/ReleaseModel.md) install layout + selector |
| **When a new release takes effect** (offline activation; a fresh process with an empty texture cache) | Studio | [ReleaseModel](Distribution/ReleaseModel.md) activation semantics |
| **Qualifying a release in the real app** before it is approved (an audience-path run) | Studio + UE plugin | [ReleaseModel](Distribution/ReleaseModel.md) qualify step |
| **The composition release pin in use**: set on first add, re-checked on every add; a mismatch surfaces **ReleaseConflict** | Stage + Studio | [Manifest](Contract/Manifest.md) / [CreatorAssetProfile](Contract/CreatorAssetProfile.md) define the pin `imrsv:matterlibRelease` |
| **Recognising Matter names on import** (rewrite-on-import) and resolving `@Name.mtlx@` through a search path | Stage | [Identity](Ontology/Identity.md); [CreatorAssetProfile](Contract/CreatorAssetProfile.md) (`assetInfo:identifier`) |
| **Picker filtering by `category`** (= the article's Class) and hiding non-`creator_selectable` articles | Stage + Studio | [RuntimeCatalog](Contract/RuntimeCatalog.md) |
| **The Studio and Theater steps of the Creator Golden Path**: panels, refinement, broken-material recovery | Studio | [Experience](Experience/Experience_MatterLibrary.md) |
| **Taxonomy layout of IMRSV's own fixture copy** of a release | Stage | [Taxonomy](Ontology/Taxonomy.md) |

## USD viewers (usdview, USDLiveView, others)

A USD viewer consumes the raw `.mtlx` articles:
- It resolves `@Name.mtlx@` through the stock USD search path ([_Architecture](_Architecture.md) §Decisions of record 8).
- It must set the MaterialX standard-library search path for its build (decision 7).
- It should honour the active-release selector rather than scanning every installed release (*Drift, 2026-09-23: USDLiveView scans all releases today; listed in `docs/Planning/PlatformDependencies.md`*).
- This repo's own validation baseline for USD rendering is [USDValidationToolchain](Tooling/USDValidationToolchain.md).
- **Creator overrides need nothing extra.** They are Material inputs that the article's nodegraph connects to ([LCDSchema §Carrier rule](Contract/LCDSchema.md#carrier-rule-no-imrsv-attrs)), so a stock viewer renders them through normal UsdShade resolution. A viewer must **not** add a resolution rule of its own: if an override does not render, the writer is at fault (`tools/conformance/check_lcd_carrier.py` says which).

## Adding a consumer

A new consumer (another engine, another DCC) needs nothing from this page except the table in §What every consumer binds to, plus the release it installs. If it needs a change to the contract, that is a contract change here, versioned by the library's semver (MAJOR for anything breaking).
