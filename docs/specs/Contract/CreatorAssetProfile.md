# Creator Asset Profile — the Open Matter Creator artifact contract

> **Brought home 2026-09-23** (Phase01 step 1.3) from the IMRSV platform docs. **This repo is now the authority** for this spec; consumers point here.

> **Status: golden pinned; a Matter Library contract.** This profile is the artifact contract for the **Open Matter Creator Pipeline**: the shape a Creator asset takes when it leaves the producer (Blender) and what an independent reference application must be able to open. It is proven by a hand-authored **[golden](../../Glossary.md)** and an executable conformance gate (below), not asserted on paper.

*Consumer-side (IMRSV): how IMRSV Studio's Add/Reimport consumes a conforming asset — see [Consumers](../Consumers.md).*

An **[Open Matter Creator asset](../../Glossary.md)** is a plain USD file that binds Matter materials to mesh geometry by **exact name**, with **no IMRSV-specific file format and no importer** — it opens in any standards-compliant USD/MaterialX application. There are **two forms of the same asset**; a conforming producer emits, and this profile pins, **both**.

## The two forms

| Form | Material reference | Payload | Opens with | Purpose |
|---|---|---|---|---|
| **Lightweight** (default) | **bare** `@Name.mtlx@` filename | none — the `.mtlx` + textures are library-resolved | a receiver configured with the Matter Library on its resolver search path | the everyday distribution form; keeps compositions small (materials are a *distribution strategy*, not copied per-asset) |
| **Complete-portable** (explicit option) | **local relative** `@./Name.mtlx@` | the required `.mtlx` + its texture set, materialized **once** into the package, references rewritten portable-relative | **any** USD app, with **no** Matter Library and **no** resolver configuration | hand-off / archival — the package is self-contained and opens standalone |

The complete-portable form materializes the `.mtlx` and textures **once** with portable references; it is **not** the incidental per-asset duplication the lightweight form forbids. (Boundary: a consumer's *composition-level* external Export — materializing a whole composition's dependency closure — is separate, consumer-owned work, **not** this profile.)

> **Shipped.** The complete-portable form is realized in the Blender exporter ([IMRSV LCD USD exporter](../../Glossary.md), `blender/addons/imrsv_lcd_export/`, historical name kept) as well as in the golden/reference `tools/conformance/build_portable.py`. **File → Export → IMRSV LCD USD** has an explicit **portable** option: off emits the lightweight form (default); on materializes each required `.mtlx` + its textures once into the package with portable-relative references. Portability is proven by **independent open** — `usdchecker`/`usdcat --flatten` compose the exported portable package with **no Matter-Library search path** configured. *(Updated 2026-09-23, measured: the add-on registers "IMRSV LCD USD (.usda)" under File > Export, and `export_lcd_usd(filepath, objects=None, portable=False)` drives `lcd_portable.py`.)*

## Conformance rules (both forms unless noted)

1. **One mesh per material-addressable region (v1).** Every independently material-addressable region is a **separate `Mesh` prim**. (GeomSubset multi-material binding is a USD mechanism but is **out of scope** for the v1 controlled producer path.)
2. **Geometry-authored UVs travel as `texCoord2f[] primvars:st`.** The Blender unwrap is the **primary** UV and travels as geometry. (A consumer's `place2d` nudge — `uv_scale/uv_offset/uv_rotation` — is authored downstream and does **not** travel from Blender — see [LCDSchema](LCDSchema.md).) Two meshes may share one Matter identity with **distinct UV fits** (distinct `primvars:st`).
3. **One Matter material per mesh, bound via `MaterialBindingAPI`.** `rel material:binding` targets a material prim.
4. **The material prim references the Matter article** — bare `@Name.mtlx@` (lightweight) or local `@./Name.mtlx@` (portable), targeting the `.mtlx`'s `</MaterialX/Materials/<Name>>` material.
5. **Exact identity is carried on `assetInfo:identifier`** — the exact [qualified Matter name](../Ontology/Identity.md), `≤63` chars `[A-Za-z0-9_]`. Identity is the `assetInfo:identifier`, **not** the prim's display name — so a producer never relies on Blender datablock display-name collision suffixes (`_001`) as semantic identity; any receiver recognises a Matter material by that identifier.
6. **Independent instances.** Two meshes sharing one Matter identity use **separate material prims** (e.g. `<id>_Instance_Top`, `<id>_Instance_Leg`) so per-mesh refinement downstream (an `inputs:` override) stays independent — editing one does not affect the other, and the `.mtlx`/textures are not duplicated to support the second instance.
7. **The composition records its ONE required Matter release** in root-layer `customLayerData` under `imrsv:matterlibRelease` (e.g. `"matterlib-0.1.0"`) — a standard USD metadata carrier, no proprietary interpretation. This is **package-dependency information**, not an alternate identity ([Manifest](Manifest.md) §Composition release pin). The historical IMRSV-branded key name is kept (R16).

   > **Reevaluate (2026-09-23):** an `imrsv:`-prefixed key sits in tension with the "no `imrsv:` USD attributes" principle ([MaterialXTemplate](MaterialXTemplate.md) hard rule 4) — owned by the contract phase.
8. **Each mesh declares `uniform token subdivisionScheme = "none"`.** These are polygon meshes, not subdivision cages. USD's Mesh default is `catmullClark`; leaving it unset tells every USD consumer the mesh is a subdivision cage, so a renderer that does not evaluate subdivision draws the raw cage with computed normals (and may warn), while one that does evaluate it smooths geometry the author meant to be faceted.
9. **Real-world scale.** Author `metersPerUnit` + coordinates so the object is its true physical size (a table ≈ 1 m, not sub-centimeter). A `metersPerUnit`/coordinate mismatch yields a speck the Creator cannot see in the scene.
10. **A face is wound counter-clockwise seen from outside, and the material's master decides whether its back is drawn** *(added 2026-10-11)*.
    - **The front of a face** is the side from which its vertices run counter-clockwise. That holds at USD's default `orientation`, right-handed, so a conforming mesh authors no `orientation`, or `rightHanded`; `leftHanded` turns every face round and is refused.
    - **Whether the back is drawn belongs to the master**, not to the mesh ([MasterSet](../Ontology/MasterSet.md) §Material-settings intent, the Two-sided column). Opaque, TwoLayer, Emissive and Subsurface draw a face's front only. Masked, Hair and the two see-through masters draw both sides. On a one-sided master a face wound the wrong way is missing from the front and shows from behind.
    - **A mesh's `doubleSided` does not make a face show**, and it is not a conformance rule: an asset conforms with `0`, with `1`, or with none. A consumer that draws with the masters takes two-sidedness from the master and does not read the flag. The library's own route writes the flag in agreement with the master (`0` on a one-sided master, `1` on a two-sided one: the Asset-Browser library's materials carry Blender's *Backface Culling* by master, and Blender's export writes the flag from that switch), so that no file the library makes says the opposite of its contract. A stock Blender export that says `1` on every mesh still conforms.
    - **What catches a backward face, and what does not.** Of the tools this repo runs, Blender's viewport and Eevee show it once *Backface Culling* is on, and Unreal shows it. Cycles does not read that switch, and Storm draws a face seen from behind whatever `doubleSided` says. **`check_facing.py` finds it from the file alone** *(added 2026-10-11, below)*.

    - **The check of the geometry: `tools/conformance/check_facing.py`** *(handed over 2026-10-11 by IMRSV's asset tooling, on the lead's word; research `261011_R_AssetToolingAsks.md`, Pass 4)*. For every closed piece of a mesh it asks which faces would have to turn round for the piece to hold a positive volume, and refuses an asset with any. It needs OpenUSD, so it sits beside `assert_profile.py`, which reads text only, and the gate runs both. **It cannot judge an open sheet**, which has no outside: it counts and names one, and does not refuse it. It reads a mirroring transform by USD's rule, as turning the winding round with it. **It is a dated copy.** The check is defined and tested in the asset tooling, which is private for now; when that project is public this file gives way to a pinned version of it. *(Was, earlier the same day, a Todo naming the check as on offer.)*

### Forbidden in a conforming asset

- **No `UsdPreviewSurface`** (no preview/proxy shading network) — the material is the referenced Matter `.mtlx`.
- **No lights** (`DomeLight`, any `*Light`), **no `Camera`**, **no generated world/environment texture** — an asset carries geometry + material bindings only. *(A render harness supplies a light + camera externally; it is never part of the asset.)*
- **No absolute author-machine paths** — every reference is a bare library name or a package-relative path.
- **Lightweight only:** **zero** localized Matter `.mtlx` or texture files of **any** kind beside the asset (the negative guard is "no material payload file of any extension," not "no Matter-named file").

## Golden + conformance gate

The pinned golden and the executable gate live in this repo:

```
tools/conformance/
  golden/creator_table_lightweight.usda      # hand-authored lightweight golden (2 Copper meshes, distinct UV fits)
  golden/creator_table_portable/             # complete-portable package (built by build_portable.py; not committed)
  build_portable.py                          # materializes the portable form from the lightweight golden + the Library
  assert_profile.py                          # pxr-free profile asserter (shape + spec-derived NEGATIVE guards)
  check_facing.py                            # rule 10's geometry: no face of a closed piece looks inward (needs pxr; a dated copy, see rule 10)
  test_check_facing.py                       # its self-test: it refuses a turned face before it is trusted to pass anything
  check_conformance.sh                       # the gate: usdchecker + usdcat --flatten + assert_profile + check_facing + usdrecord (both forms)
```

*(Updated 2026-09-23, measured: `golden/creator_table_lightweight.usda`, `build_portable.py`, `assert_profile.py` and `check_conformance.sh` exist; `golden/creator_table_portable/` is a build output listed in `tools/conformance/.gitignore`, so it appears only after `build_portable.py` runs. The lightweight golden sets `metersPerUnit = 1`, `imrsv:matterlibRelease = "matterlib-0.1.0"`, `subdivisionScheme = "none"` on both meshes, and bare `@Copper_Verdigris_Aged_Base_s01_v01.mtlx@` references.)*

**The gate proves — for BOTH forms:**
- `usdchecker` → `Success!` and `usdcat --flatten` composes the material network (96 shaders = 2 Copper instances × 48). The **lightweight** form resolves the bare `@Name.mtlx@` via a leaf-dir `PXR_AR_DEFAULT_SEARCH_PATH` (Matter Library on the search path); the **portable** form composes with **no search path at all** — proving independent open.
- `assert_profile.py` → every rule above holds, including the negative "no material payload beside a lightweight asset" guard (spec-derived, not a Matter-basename allowlist — so it cannot be fooled by a differently-named generated texture).
- `usdrecord` (Storm/GL) → an eyes-on render of both forms; the Copper material samples the mesh's authored `primvars:st` and renders as verdigris-copper metal.

`assert_profile.py` is **two-way**: run it against a whole-scene Blender export (which carries `UsdPreviewSurface` + a `DomeLight` + absolute paths) and it FAILs — so the gate can fail, and green means something.

> **Independent reference application** = **usdview / usdrecord** (OpenUSD Storm/Hydra), with the resolver configured as: `PXR_MTLX_STDLIB_SEARCH_PATHS=<usd>/libraries` + `PXR_AR_DEFAULT_SEARCH_PATH` = colon-joined list of each leaf directory holding a `.mtlx` (ArDefaultResolver is non-recursive, so leaf dirs are the search roots). See the [USD validation toolchain](../Tooling/USDValidationToolchain.md).

## History

- Pre-standalone (2026-06 → 2026-07): the profile was pinned by a hand-authored golden before any real exporter produced it, so the contract is defined by an asset that opens in plain OpenUSD rather than by one producer's output.
- Pre-standalone: rules 8 and 9 were found live in the first end-to-end smoke — an unset `subdivisionScheme` rendered as an unevaluated cage, and a `metersPerUnit = 0.01` fixture of ~0.6 units rendered as a ~1 cm speck.
- Pre-standalone: recognition moved from stripping Blender's `_001` suffixes off prim names to reading `assetInfo:identifier`.
- 2026-07-17: the complete-portable form shipped in the real Blender exporter, alongside the release pin.
- 2026-10-11: rule 10 added. IMRSV's asset tooling built a prop by script, saved it through the export add-on and passed all nine rules with 204 of its 3,764 triangles wound backwards; Studio drew it with parts missing from the front. The profile had said nothing about which way a face looks, and the golden itself carried `doubleSided = 1` on Copper, an Opaque article; it now carries `0`. The asserter refuses `leftHanded`. What `doubleSided` means was taken as *free* on the lead's go-ahead for the whole set of asks, with no other option named (research `261011_R_AssetToolingAsks.md`, §Resolved).
- 2026-10-11: `check_facing.py` handed over by IMRSV's asset tooling and added to the gate (step 3b), with its self-test. It is a dated copy of a check defined and tested there (rule 10; research `261011_R_AssetToolingAsks.md`, Pass 4).
