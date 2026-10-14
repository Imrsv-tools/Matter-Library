# Phase14 — HDRIs in the Library

**Status:** DISCOVERY, Pass 1 — **Brief written (2026-10-14), lane `build`.** One question for the lead (Q-P14-1) gates act 1 of 14.1's TRY, not its build. **Numbered Phase14 and opened by the lead, 2026-10-14:** the invocation, verbatim, *"/discovery P14"* (RD-P14-1). No phase carried 14, so the number goes to the entry heading `## Future` (RD-RO-3's order, after Materials Described took Phase13), and no ruling newer than that order undercuts it. Seeded the same day as a pointer-shell by `/research` on the lead's word (*"seed the phase"*).
**Ids:** `Q-P14-n` · `F-P14-n` · `RD-P14-n`. Ids cited from research (`SKY-Fn`, `RD-SKY-n`, `F-RO-n`, `RD-MP-n`) keep their own stems.

## Outcome

**A scene's lighting picture (an HDRI) is chosen from the library by name, in the IMRSV app and a USD viewer, and the library is the only place it comes from.** The dev install serves HDRIs before any release holds one.

*How it becomes true:* this phase is the library's half. It covers the kind, the name, the catalog list, the first HDRI and the lead's picks, the dev install serving them by name, and a USD viewer showing a scene lit by one. **The IMRSV app's half is the platform's own HDRI phase**, which waits on this one ([PlatformDependencies](../../PlatformDependencies.md) M10) and is judged there.

## Why this is a phase

The library holds materials and nothing else: its specs, catalog, lockfile check, LFS rule, licence list and serve tool each assume a `.mtlx`. An HDRI is a second kind of entry, and a contract change (a catalog's `schema_version` moves). It is one thing a person can see: a scene shows a library HDRI, chosen by name, with no copy in the scene. The platform's own HDRI phase waits on it.

---

## Brief

### First human test — 14.1 (acts 1–2), 14.2 (act 3)

**Where:** the lead's desktop on the library machine. **USDLiveView, opened by the agent** on a draft served to Stage (`LOCAL_DELTAS.md`, *the artifact a person reaches*). The thumbnail is opened with `xdg-open`, and its path is in the handback.

**The agent does first** (machine-checkable, not the lead's):
- serve the working tree (`uv run tools/releases/serve_to_stage.py`);
- confirm the dev catalog lists the HDRI, names it as `default_hdri`, and gives it a thumbnail that exists;
- build the scene: a copy of Asset-Library's `CubeAndCone_04` composition in a scratch folder, its `DomeLight` renamed to the bare `@IndustrialSunset_PureSky_v01.hdr@`, with **no `Assets/HDRIs/` folder beside it**;
- open that copy in USDLiveView, with the unchanged original in a second window.

| Act | The lead uses and judges | Step |
|---|---|---|
| 1 | The two windows show **the same sunset sky** behind the cubes and cones, lighting them the same way. The copy carries no sky file: its sky comes from the library, by name. | 14.1 |
| 2 | The HDRI's **thumbnail** reads as that sky: whole, 2:1, recognisable. | 14.1 |
| 3 | The lead names one or more Poly Haven HDRIs. The agent adds them and changes **only the dome's name** in the same scene, and the lead sees the other sky. | 14.2 |

**Can each surface show the thing judged?**
- **Act 1:**
  - **The fixture carries the property in use.** `CubeAndCone_04` is lit by the sky every scene shows today (SKY-F1, A8).
  - **The instrument separates the cases** (F-P14-3, measured in Storm on this machine). Named by its bare name, with its folder on the search path, the sky draws the same as the copied-in file (RMSE 1.5 %). Off the path, the dome draws no sky (RMSE 84 %), with Storm's *"could not be resolved"* warning.
  - **USDLiveView draws a dome as the background by default** (F-P14-5; read in code, not run).
  - **The act needs USDLiveView's launcher to put the HDRI folder on its search path (Q-P14-1).** Without that, it fails exactly as the unresolved probe did.
- **Act 2:** `magick` reads the Radiance file and writes a 2:1 JPEG that reads as the sky (F-P14-6).
- **Act 3:** Poly Haven serves the 4k `.hdr` to this machine (F-P14-8); the doer is the agent, on the lead's picks.
- **Nothing in Not-now is needed** by any act.

### In now / not now

| In now | Step |
|---|---|
| **The kind** (RD-SKY-1): one flat folder, `MatterLibrary/hdris/`. [Taxonomy](../../../specs/Ontology/Taxonomy.md) gains a line that an HDRI is a kind **beside** the taxonomy; the Realm stays planned. **The Glossary's *HDRI* headword lands first**, before any spec uses the word (SKY-F13). | 14.1 |
| **The name** (RD-SKY-2) in [Identity](../../../specs/Ontology/Identity.md): `<Name>_<Variant>_vNN.hdr`, PascalCase tokens, the 63-character `[A-Za-z0-9_]` budget, unique within `hdris/`. The id is `<Name>_<Variant>`; the payload is `hdris/<id>_<version>.hdr` (Q-P14-5). | 14.1 |
| **The HDRI check:** one function, used by the lockfile check and the serve tool. It checks the name grammar, a Radiance header, and 4096 × 2048 (RD-SKY-3). | 14.1 |
| **The catalog contract** ([RuntimeCatalog](../../../specs/Contract/RuntimeCatalog.md), [Manifest](../../../specs/Contract/Manifest.md)):<br>• a top-level `hdris[]` beside `materials`, each entry carrying `id`, `display_name`, `version`, `status`, `creator_selectable`, `payload_path` and `thumbnail_path`;<br>• one top-level `default_hdri` naming a listed id (A2, A3);<br>• **`schema_version` 3 for a catalog that lists HDRIs, and 2 for one that does not** (Q-P14-2). | 14.1 |
| **The lockfile check and the projector** take `hdris[]` and `default_hdri`. A default that names no listed HDRI fails. Each HDRI carries a provenance block in the texture's `{url, sha256}` form, which the projector never projects (`no_projection_guard`). | 14.1 |
| **Provenance and licence** (A5):<br>• a record per HDRI under `library/provenance/sources/hdris/<id>.yaml`, made from **the library's own Poly Haven download** (URL, `sha256`, `CC0-1.0`; RD-RO-2);<br>• a `MatterLibrary/hdris/` row in `LICENSE-CONTENT.md`, and a Poly Haven line under its third-party sources. | 14.1 |
| **Storage** (A7): `.gitattributes` puts `MatterLibrary/hdris/**` in LFS. | 14.1 |
| **The importer:** `tools/converters/import_polyhaven_hdri.py <polyhaven-id> <Name> <Variant>`. It downloads the 4k `.hdr`, runs the HDRI check, and writes the file and its record (the `import_ambientcg.py` pattern). | 14.1 |
| **The first HDRI** (A8): Poly Haven's `industrial_sunset_02_puresky` as `IndustrialSunset_PureSky_v01.hdr`. **Its hash is compared with the copy scenes use today** (SKY-F1's open point, F-P14-8), and a difference is reported before the lead's sitting. | 14.1 |
| **The default**, named once in `library/hdris.yaml` (`default: IndustrialSunset_PureSky`; Q-P14-5). | 14.1 |
| **The dev install** (RD-SKY-4), in `serve_to_stage.py`:<br>• `releases/matterlib-dev/hdris` linked into the checkout, beside `materials` and `textures`;<br>• the `hdris` list and `default_hdri` written into the dev catalog;<br>• each HDRI's thumbnail generated into the runtime's `releases/matterlib-dev/thumbnails/`, never into the checkout (Q-P14-3);<br>• an HDRI that fails the check is refused, as a missing payload is. | 14.1 |
| **No compression** (RD-SKY-4): one line in [CompressedDistribution](../../../specs/Tooling/CompressedDistribution.md). | 14.1 |
| **A guard:** `freeze_release.py` refuses a lockfile that lists HDRIs, so no release is frozen without hashing them, until staging carries them (Not now). | 14.1 |
| **The lead's picks** from Poly Haven, added by the importer (Q-P14-4). | 14.2 |
| **Docs at the close:**<br>• [Consumers](../../../specs/Consumers.md) §USD viewers: the HDRI folder on the search path;<br>• `ToolingConventions.md`: the importer and the `hdris/` root;<br>• `_Architecture.md`: one line in the component map;<br>• PlatformDependencies M10: what the dev install serves, and what the platform's phase now has. | at the close |

| Not now | Why, and who owns it |
|---|---|
| **Staging, freezing and activating a release that holds HDRIs.** A7's *"inside the release folder"* is written into the specs. | **(planned)**, built with the first release that holds one: *Release Bundle and Consumer Contract*. Pre-release, no release ceremony (`AI_WorkingAgreement.md` §Settled practices). The freeze guard above keeps the gap loud. |
| **The app's half:** Stage's search path, the picker and the switch away from per-scene copies. | The platform's HDRI phase (M10). |
| **USDLiveView's launcher change.** | USDLiveView's lane: its own ask doc already waits on this phase's folder (F-P14-1). Q-P14-1 says who does it and when. |
| **HDRIs on the library's website.** | Not asked. Phase13's site file lists materials. |
| **Storage beyond LFS** (the seed's open question on A7). | ~16 MB each, so LFS holds them until the count makes it a question. It joins the Parking lot's *Texture storage beyond Git LFS* and the LFS quota the site research flagged (`261014_R_TheLibrarysSite.md` WS-F1). |
| **The rig or the preview tool lit by a library HDRI** (the seed's third open question). | A later question, as the seed said. The rig's flat dome is deliberate (Storm learnings S2, S4). |

### The reuse check

**What the stack already provides:**
- **Resolution** is the stock USD search path: decision of record 8, SKY-F4, F-P14-3. There is no resolver of ours.
- **The dev install** already links folders and writes a catalog (`serve_to_stage.py`). This phase adds one link and one list.
- **The lockfile check and the projector** (`validate_manifest.py`, `project_runtime_catalog.py`) take a new list. Provenance reuses `_validate_provenance`'s `{url, sha256}` form.
- **The name budget** reuses `check_grammar`'s charset and 63-character rules. Its six-token material shape does not apply.
- **The thumbnail** is ImageMagick, already installed (F-P14-6). The preview tool is not used: it renders a material on a sphere.
- **The importer** follows `import_ambientcg.py`: download, then record the URL and a hash.

**Two custom pieces, each with its gap:**
- **The importer:** nothing in the tree downloads from Poly Haven or writes an HDRI's record.
- **The HDRI check:** nothing checks a `.hdr` at all.

**Contracts touched:** RuntimeCatalog and Manifest (additive, schema 3 only where HDRIs are listed), Identity, Taxonomy, and the CC0 shipped-pixel rule.

### Decisions that bind

**From research and earlier rulings (the authority until the specs land):**
- **RD-SKY-1 to RD-SKY-4** ([`261013_R_PlatformSkyAsks.md`](../../Research/261013_R_PlatformSkyAsks.md) §Resolved):
  - the flat `hdris/` kind beside the taxonomy;
  - the name `<Name>_<Variant>_vNN.hdr`;
  - Radiance `.hdr` at 4096 × 2048;
  - the dev install serves HDRIs, which skip compression.

  Pass 2's priced table (A1 – A8) is the starting point. This Brief confirms it, except where Q-P14-2 and Q-P14-3 refine it.
- **RD-RO-2:** content is CC0 only ([`261014_R_RoadmapOrder.md`](../../Research/261014_R_RoadmapOrder.md)). Poly Haven publishes CC0.
- **RD-MP-5 and RD-MP-6:** the published pictures are **thumbnails**, and **thumbnails never go in git or LFS** ([`261014_R_MaterialPipeline.md`](../../Research/261014_R_MaterialPipeline.md)).

**This phase:**
- **RD-P14-1 — Numbered Phase14 and opened by the lead**: *"/discovery P14"* (2026-10-14).
- **Q-P14-2 — `schema_version` 3 only for a catalog that lists HDRIs.** *Decided, unless the lead says otherwise.*
  - **Why:** the freeze hash-locks each release's catalog (F-P14-4), and the catalog-freshness lane re-projects **every** lockfile with the one projector constant.
  - **What a global bump would do:** turn the committed 0.0.1 and 0.1.0 catalogs red. Re-projecting them would rewrite the approved pilot's frozen payload and owe a re-freeze and the maintainer's re-approval, for a release that holds no HDRI.
  - **The rule:** a catalog's `schema_version` is the lowest that describes its content. Old releases stay byte-identical, and the consumer reads no `schema_version` anyway (SKY Pass 1, second addendum).
- **Q-P14-3 — A4's small picture is a thumbnail, generated and never committed.** *Decided, unless otherwise.*
  - It is a 1024 × 512 JPEG made from the HDRI by `magick`, written into the dev install at serve time. At a release it becomes a release asset, with the release.
  - The entry field is `thumbnail_path` (RD-MP-5's word), not A2's `preview path`.
  - It is a deterministic derivative, so nothing is lost by not storing it (RD-MP-6).
- **Q-P14-4 — No HDRI wish list.** *Decided, unless otherwise.* `library/wishlist.yaml` stays materials: its rows carry slot, master, lane and layers, and `/matter-batch` builds them. The lead names Poly Haven HDRIs (*"I will be getting many more open sky HDRIs from Polyhaven"*), and the importer adds each one. This closes the seed's A8 question.
- **Q-P14-5 — Identity and the default.** *Decided, unless otherwise.*
  - **The id** is `<Name>_<Variant>` and `version` is `vNN`, so `id` + `version` resolve to the file as a material's do. The display name is the id.
  - **The default** is authored once, in `library/hdris.yaml`, which the serve tool reads; a lockfile carries it as `default_hdri`.
  - **Status** comes from each HDRI's record: `candidate` once the HDRI check passes (Manifest's lifecycle).

### Risk lane — `build`

**The controls, read:**
- `freeze_release.py`: the catalog is in the hashed payload, and the guard refuses HDRIs until staging carries them.
- `run_all.py` `run_catalog_freshness`: it re-projects every lockfile, so the schema rule above.
- `validate_manifest.py`, `project_runtime_catalog.py` and `no_projection_guard`: extended, not replaced.
- `serve_to_stage.py`: it writes only into the runtime, and its links into the checkout.
- USDLiveView's launcher: another repo (Q-P14-1).

**Not touched:** authorisation, secrets, a destructive migration, the public edge. **The push publishes a 16 MB CC0 file through LFS:** irreversible and lead-gated, as every push here is.

**Baseline, the library machine, 2026-10-14:** `run_all.py` gives 17 lanes, **15 PASS and 2 SKIP** (compression and staging: the pinned encoder is absent), 0 FAIL. Every lane this phase touches starts and passes. The two SKIPs cover `stage_release.py`, which this phase does not change. `check_exporter.sh` is not owed, since nothing under `blender/addons/` or `tools/conformance/` changes.

**Test surface (within `build`'s ceiling):**
- the existing lanes, with new fixture rows in their existing lists: an HDRI lockfile that projects, a default naming no listed HDRI, and a wrong-size header;
- a unit test for the HDRI check;
- **one real-path smoke:** act 1.

### Step list

- **14.1 — The first HDRI, named from the library.**
  - The Glossary headword, then the specs.
  - The importer, the HDRI check, and the first HDRI with its record and LFS rule.
  - The lockfile and projector support, the freeze guard, and the serve tool.
  - *First clickable result:* **acts 1 and 2.** Act 1 also needs Q-P14-1's launcher change.
- **14.2 — The lead's picks.** The lead names HDRIs from Poly Haven, the importer adds each, and the agent re-serves and swaps only the dome's name in the act-1 scene. *First clickable result:* **act 3.**

**Reconciled, act by act:**
- Act 1 needs 14.1 and the launcher change.
- Act 2 needs 14.1's thumbnail.
- Act 3 needs 14.2.

**The doers:**
- **The agent:** downloads from Poly Haven (reachable, F-P14-8), serves, builds and opens the scene.
- **The lead:** judges, and picks HDRIs.
- **USDLiveView's lane:** the launcher (Q-P14-1).

### Compact build map

**Docs:**
- the Glossary (*HDRI*, first);
- `Taxonomy.md`, `Identity.md`, `RuntimeCatalog.md`, `Manifest.md`, `CompressedDistribution.md`;
- `LICENSE-CONTENT.md` and `.gitattributes`.

`RuntimeCatalog.md` and the Glossary are also touched by Phase13 at its close, in other sections (F-P14-9).

**Tools:**
- **`tools/converters/import_polyhaven_hdri.py` (new):**
  - Poly Haven's file URL shape is `https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/4k/<polyhaven-id>_4k.hdr` (measured for the first HDRI);
  - it writes `MatterLibrary/hdris/<id>_v01.hdr` and `library/provenance/sources/hdris/<id>.yaml`.
- **`tools/validators/validate_manifest.py`:**
  - `check_hdri(path)`: name, Radiance header, `-Y 2048 +X 4096`;
  - the `hdris[]` loop and the `default_hdri` check.
- **`tools/converters/project_runtime_catalog.py`:** an HDRI entry, `default_hdri`, and schema 3 only when `hdris` is listed. `serve_to_stage.py` imports the same constants.
- **`tools/releases/serve_to_stage.py`:** the link, the thumbnails, the list, and the refusal.
- **`tools/releases/freeze_release.py`:** the guard.
- **`library/hdris.yaml` (new):** the default.

**For USDLiveView's change** (the paths it needs):
- in a checkout, `MatterLibrary/hdris/`;
- in a Stage runtime, `MatterLibrary/releases/<active release>/hdris/` (the serve tool's link, in `matterlib-dev`).

**Learnings to carry** (`docs/Learnings/Storm/Storm.md`):
- **S1:** a headlight hides an unlit dome, so judge the visible sky and the resolver warning, not "it looks lit";
- **S3:** render twice;
- **S4:** the visible dome is the raw texture.

---

## Findings (Pass 1)

- **F-P14-1 — USDLiveView's launcher puts only folders holding a `.mtlx` on the search path.** That is its `find … -name '*.mtlx'` loop, in the USDLiveView checkout's `usdliveview`. A folder of `.hdr` files is not on it. USDLiveView's own repo holds the platform's ask for exactly this change (`docs/Planning/Research/261013_R_PlatformSkyAsk.md`): *"Nothing until the Matter Library says where skies sit. Then the launcher's one change, and one look."* RD-SKY-1 has now said where.
- **F-P14-2 — This repo cannot add the folder from outside.**
  - `serve_to_stage.py --view` hands the launcher `IMRSV_MATTER_LIBRARY=MatterLibrary/`.
  - The launcher then **sets** `PXR_AR_DEFAULT_SEARCH_PATH` itself, overwriting anything it was given.
- **F-P14-3 — Storm draws a bare-named HDRI once its folder is on the search path** (probe, 2026-10-14, OpenUSD 26.03, `usdrecord --enableDomeLightVisibility`). The probe used `CubeAndCone_04`, its dome renamed to `@IndustrialSunset_PureSky_v01.hdr@`, with the file in a separate `hdris/` folder:
  - **folder on the path:** the same picture as the copied-in original (RMSE 0.015);
  - **folder off the path:** no sky (RMSE 0.84 against "on"), and Storm warns *"Texture asset path 'IndustrialSunset_PureSky_v01.hdr' for dome light could not be resolved"*.

  Without `--enableDomeLightVisibility`, `usdrecord` draws no dome background at all, so the first run showed no sky in any case.
- **F-P14-4 — A global `schema_version` bump would break the approved pilot.**
  - **The freeze hashes the catalog:** `payload_sha256.catalog` in `freeze_release.py`.
  - **The freshness lane re-projects every lockfile** with the one `SCHEMA_VERSION` constant (`run_all.py` `run_catalog_freshness`).

  Hence Q-P14-2.
- **F-P14-5 — USDLiveView should draw the dome as the background** (read in code, not run). The Storm engine's dome-camera-visibility setting defaults to true (`usdImagingGL/engine.cpp`, `GetWithDefault<bool>(true)`), and USDLiveView's app sets nothing about domes.
- **F-P14-6 — `magick` reads the Radiance file** and writes a 512 × 256 JPEG that reads as the sky, with the sun clipped (probe). The tone-mapping is execute's to settle; a picker card shows it whole.
- **F-P14-7 — No HDRI code exists.**
  - The `.hdr` hits are the rig's own lighting probes (`library/parity/_probe/dome/`) and the exporter's package check, which lists `.hdr` as a texture extension (`tools/conformance/assert_profile.py`). Both are untouched.
  - Nothing enumerates `MatterLibrary/` wholesale: every walker is scoped to `materials/` or `textures/`, so a new `hdris/` joins no existing gate by accident.
- **F-P14-8 — Poly Haven serves the first HDRI to this machine**, at the same size as the copy scenes use.
  - The 4k URL above answers HTTP 200 with **16,086,915 bytes**, the same byte count as the copy in the Stage runtime.
  - That copy's header reads `-Y 2048 +X 4096`, Radiance RGBE.
  - The hashes are compared in 14.1.
- **F-P14-9 — Phase13 (in discovery beside this one) shares docs, not code.**
  - Its snapshot builder writes into `library/snapshots/`, and it changes neither the serve tool nor the projector.
  - Both phases touch the Glossary, `RuntimeCatalog.md`'s notes, `Consumers.md`, `ToolingConventions.md` and PlatformDependencies, in different sections.
  - **Phase13's site file lists materials only.**

## Questions for the lead

- **Q-P14-1 — Who makes USDLiveView's one launcher change, and when?** Act 1 cannot pass without it (F-P14-1, F-P14-2). The options:
  - **(a) Recommended:** a short session in the USDLiveView repo once 14.1 lands the folder: its own `/quick-fix` on its 2026-10-13 ask, with the paths in §Compact build map. Act 1 is judged after it lands; act 2 does not wait. The change belongs to that repo's lane, and its ask is already written and waiting on this phase.
  - **(b)** The lead directs this phase's `/execute` to make that one change in the USDLiveView checkout, committed there, and recorded as lead-directed cross-repo work.
  - **(c)** Act 1 is judged in stock `usdview`, launched by the agent with the search path set. USDLiveView follows in its own lane later. This is "a USD viewer", but not the surface the lead tests drafts on.

## Consumers and the ledger

The platform's side (its runtime, plugin and app; its web publish check; USDLiveView's launcher) is [PlatformDependencies](../../PlatformDependencies.md) **M10**. At the close it gains what the dev install now serves, and the platform's HDRI phase can start building against it.

## Discovery Log

- **Pass 1 (2026-10-14):**
  - **Numbered by the lead** (`de32333`).
  - **Read:** the product docs from `_Architecture.md` down to RuntimeCatalog, Manifest, ReleaseModel, Consumers, Taxonomy and the Glossary; then the three research docs (`261013_R_PlatformSkyAsks.md`, `261014_R_RoadmapOrder.md` §Resolved, `261014_R_MaterialPipeline.md` RD-MP-5 and RD-MP-6); then the tree's serve, projector, lockfile, freeze and gate code, the Storm learnings, and USDLiveView's launcher and its ask.
  - **Probed:** a bare-named dome in Storm, a thumbnail, and Poly Haven's file.
  - **The seed agrees with the product docs.** Pass 1 added two refinements (Q-P14-2: the schema rule, which the freeze forces; Q-P14-3: the thumbnail, which RD-MP-6 forces) and one finding that moves work into another repo (F-P14-1).
  - **The Brief was written in this pass.** Only Q-P14-1 needs the lead, and it gates act 1's sitting, not `/execute`.
