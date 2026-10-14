# Research — The library's website: who builds it, and what the library publishes for it

**Opened:** 2026-10-14 · **Mode:** research, ruled the same day. **Mnemonic:** `WS` (ids `WS-Fn`, `RD-WS-n`).
**Requested by:** the lead, 2026-10-14: *"We should start considering what the web front end for Matter Library will be"*, and *"I think the Web repo should be responsible for build the web front end to this project"*.
**Measured at:** `0957cad` (2026-10-14).

**Public-repo note.** The site's build and design are IMRSV's, and its planning is private. They are summarised here by what was decided and what the library owes, with no platform paths, issue numbers or ruling ids.

**Extends, does not replace:** Roadmap *See the Library* (its Outcome stands) · `PhaseTBD_ReleaseBundleConsumerContract.md` (the host question, F6) · [Catalog](../../specs/Catalog/Catalog.md) §Thumbnails.

---

## The short version

- **IMRSV's web platform builds and runs the library's website.** The library publishes the facts, and the site shows them. The site is a **consumer** of published releases, exactly as Blender, Stage and USD viewers are (R1). It never reads this repo.
- **The library publishes every release itself**, on GitHub Releases, with its digest. IMRSV's web side **mirrors** it for speed and for its apps. The library never depends on IMRSV being up.
- **Until the first versionable library** (on the order of 200 articles, the pre-release ruling), the site runs on IMRSV's staging from the dev catalog, with each article's status shown. **It launches publicly with that first release.**
- **The library publishes a file for the site beside each release.** The runtime catalog stays the engines' lean file.

## Pass 1 — What the site needs that the library already has, and what it does not

- **WS-F1 — The site is a consumer, so it cannot read the repo.** R1 rules it out. So does Git LFS: an anonymous download of the textures is charged to the organisation, and past the quota a downloader receives pointer files instead of pictures. Every download comes from a published release or its mirror.
- **WS-F2 — The runtime catalog is the wrong file for a website.** It is lean by design. A gate (`no_projection_guard`) keeps provenance, licence and evidence out of it, and parameters are read from the `.mtlx` ([RuntimeCatalog](../../specs/Contract/RuntimeCatalog.md) §What the runtime catalog does NOT carry).
- **WS-F3 — Almost everything a material page needs already exists in the library**, spread across several records:
  - the identity, Domain/Class, master, scale and status: the lockfile, the recipe, the dev catalog;
  - the Creator ports an article declares, with their start values: the recipe and the `.mtlx`;
  - its wear layers: the recipe;
  - the Physically Based values used, and the ambientCG source: the recipe's `sources`;
  - texture provenance and its evidence: the lockfile;
  - the licence: CC0-1.0 throughout *(true when written; since RD-MP-1, 2026-10-14, an article may be CC BY 4.0, so the site shows each article's own licence and the attribution it asks for; **withdrawn the same day**, `261014_R_RoadmapOrder.md` RD-RO-2: CC0 throughout holds, with a contributor's handle shown as a courtesy)*;
  - the per-slider parity verdict across Storm, Blender and Unreal: `library/parity/<article>/scorecard.json`;
  - what changed between two releases: the lockfile diff.
- **WS-F4 — Two things would be new data:**
  1. **A plain one-line public summary per article.** The recipe's `_comment` is an authoring note, not public copy.
  2. **A human label.** `display_name` is the token string, e.g. `Glass_Clear_Clean_Base`. A label such as "Clear glass" can be derived (split the PascalCase, drop the default tokens `Natural`, `Clean` and `Base`), with an override where the result reads badly.
- **WS-F5 — Previews exist, but at the wrong grade.** The parity rig renders every article in three renderers, at its defaults and with each Creator port moved. Today these are working files: full-size PNGs and a sheet of about 24 MB. A **standard preview set** (one scene, fixed sizes, web formats) made at release time is [Catalog](../../specs/Catalog/Catalog.md) §Thumbnails *(planned)*. **The site is that set's first consumer.**
- **WS-F6 — The site's best material is the library's own evidence.** One article, side by side in a USD viewer, Blender and Unreal, with each Creator port moved. The site must word it as the LCD principle does ([_Architecture](../../specs/_Architecture.md) §Design principles): *a starting point in every engine*, never *looks the same everywhere*.
- **WS-F7 — A Creator setting is never a new material**, and the site shows it that way. Tint, wear, a glass's colour and a light's colour and brightness are controls on one article's page ([LCDSchema](../../specs/Contract/LCDSchema.md); Phase12's ruling that a green glass is a clear glass with its colour set).
- **WS-F8 — The release id has one spelling: `matterlib-X.Y.Z`** ([Manifest](../../specs/Contract/Manifest.md) §Composition release pin). The web side's early sample pages used date-like ids, which were placeholders. The site uses the library's spelling.

## Resolved

The lead, 2026-10-14, on all four recommendations together: *"Great... I agree. go ahead"*.

- **RD-WS-1 — IMRSV's web platform builds and runs the Matter Library's website, as a consumer of published releases.** Five conditions bind it:
  1. **The Matter Library keeps its own identity and its own domain.** It is a community resource (R9), not a product of the IMRSV family, and it carries no IMRSV product branding.
  2. **Browsing and downloading never need an account.**
  3. **The library survives without IMRSV** (RD-WS-2).
  4. **The library owns every fact the site shows** (identity, status, parity, provenance, licence). The site presents those facts and invents none of them.
  5. **The site is static, built from published files.**

  *The cost, accepted:* the site's code is not public, so the community contributes to the library and not to the site.
- **RD-WS-2 — The library publishes each release on GitHub Releases, with its digest. IMRSV's web side mirrors it**, verified against that digest, for speed and for its apps. This answers the host question the release-bundle phase held open (`PhaseTBD_ReleaseBundleConsumerContract.md` F6). **The size check it named still applies:** GitHub's documented per-file limit (under 2 GiB) shapes how the bundle is split. That is to be confirmed when that phase resumes.
- **RD-WS-3 — Before the first versionable library, the site runs on staging from the dev catalog, with each article's status shown. It launches publicly with the first versionable release.** This follows the pre-release ruling (`.ai/AI_WorkingAgreement.md` §Settled practices): the site adds no release step for dev work.
- **RD-WS-4 — The library publishes a file for the site beside each release**, projected from the same records as the runtime catalog (WS-F3), plus the standard preview set (WS-F5) *(called **thumbnails** since RD-MP-5, 2026-10-14; "preview" stays the review render, `261014_R_MaterialPipeline.md`)*. **The library owns its shape**, as a contract spec under `docs/specs/Contract/`, written by the phase that builds it. **Its name is not chosen.** The runtime catalog is unchanged.

## What the library owes, and where each item is tracked

| Item | Where it lives | Status |
|---|---|---|
| Publish each release on GitHub Releases with its digest (RD-WS-2) | the release-bundle phase (`PhaseTBD_ReleaseBundleConsumerContract.md`) | *(planned)* |
| The site file and its contract spec (RD-WS-4) | Roadmap *See the Library* | *(planned)* |
| The standard preview set (RD-WS-4, WS-F5) | [Catalog](../../specs/Catalog/Catalog.md) §Thumbnails · *See the Library* | *(planned)* |
| A public summary and a human label per article (WS-F4) | *See the Library* | *(planned)* |
| What the site and the mirror ask of the library, and the reverse | [PlatformDependencies](../PlatformDependencies.md) P24, M9 | OPEN |

## Status

**Ruled 2026-10-14** (RD-WS-1 to RD-WS-4). Nothing is built. The derived docs were brought into line in the same change: [Consumers](../../specs/Consumers.md), [PlatformDependencies](../PlatformDependencies.md), the Roadmap entry *See the Library*, [Catalog](../../specs/Catalog/Catalog.md) §Thumbnails, [RuntimeCatalog](../../specs/Contract/RuntimeCatalog.md), and the release-bundle phase doc.
