# Phase13 — Materials Described

**Status:** IN EXECUTION (2026-10-14, the lead: *"no need for plan? if not go ahead with /execute"*). Brief written at discovery Pass 1 the same day. Lane **`build`**, with the publication gated on the lead's word (§Risk lane). **Numbered Phase13 and opened by the lead, 2026-10-14:** the invocation, verbatim, *"/discovery materials definitions and numner the phase"* (RD-P13-1). Seeded the same day as a pointer-shell by `/research` on the lead's word (*"Seed all the TBD phases we discovered here"*).
**Ids:** `Q-P13-n` · `F-P13-n` · `RD-P13-n`. Ids cited from research (`F-MP-n`, `RD-WS-n`, `F-RO-n`) keep their own stems. The platform's site work is cited by date and content, never by its ids (`LOCAL_DELTAS.md` §Separation).

## Outcome

**Every kept material has a name a person reads, a one-line description and search words. The library publishes everything the website shows about each material in one file beside each release.**

*How it becomes true:* the file, with every field that is real today, is published first as a dev snapshot (13.1). The words that do not exist yet are written, confirmed by the lead and published in the same file next (13.2), and from then on the build loop writes them for every new material (13.3).

## Why this is a phase

An article's facts live in six records today (F-MP-3), and the words a person needs (a label, a summary, search words, where it came from) do not exist (F-MP-14). The website reads only what the library publishes (RD-WS-1), and the engines' catalog is kept lean by a gate (WS-F2). So the site needs a file of its own, projected from the same records (RD-WS-4). It is the library's other half of *See the Library*, beside *Thumbnails*. **The platform's site is built and is parked on this phase's first step**: its pictures, downloads and releases page wait for the snapshot (PlatformDependencies M9; F-RO-24 to F-RO-27).

---

## Brief

### First human test — 13.1, the dev snapshot

**Where:** the snapshot's GitHub release page, on the lead's desktop or iPad: `https://github.com/Imrsv-tools/Matter-Library/releases/tag/matterlib-0.2.0-dev.1`. It is a repository page, the closest thing this producer has to a page of its own (`LOCAL_DELTAS.md` has no browser surface). The site's own sitting comes after (act 6 below).

**Done by the agent first:** the snapshot is built on the library machine, where `library/parity/` lives; every digest is checked and one zip is rendered from a clean folder (§Tests). Then, **on the lead's word**, `main` is pushed and the pre-release is published (§Risk lane). The lead types nothing.

| # | The lead does | The lead sees, and judges | Fixture |
|---|---|---|---|
| 1 | opens the repository's Releases | `matterlib-0.2.0-dev.1`, marked **Pre-release**, beside the four `unreal-runtime-v*` builds; nothing is marked Latest | — |
| 2 | opens it | its notes say what it holds and what it does not hold yet (no thumbnails, no summaries, rig evidence for 56 of 95); its assets: the site file, `SHA256SUMS`, one zip per material, pictures | — |
| 3 | taps Copper Verdigris's three pictures | the same aged copper in Storm, Blender and Unreal | `Copper_Verdigris_Aged_Base_s01_v01`: approved, swept, all three tools (measured) |
| 4 | opens the site file, finds Copper, then Enamel | Copper: a plain name, its domain and class, its master, its scale and metres per tile, approved, its controls with start values and ranges, its sources, CC0, and **a verdict per control with the date it was measured**. Enamel: **no pictures and no verdict**, absent rather than invented. **No summary on either** | Copper as above; `Enamel_Natural_Clean_Base_s001_v01`: candidate, never rigged (measured) |
| 5 | downloads Copper's zip, with no sign-in | the `.mtlx` and a `textures/` folder holding its maps and its wear layers | Copper |

- **Act 6 is the platform's:** once the site's mirror has copied the snapshot, the lead reloads the site's staging and sees real pictures and a working Download. **That sitting is the site's, not a gate on this phase.**
- **Reconciled click by click:** acts 1 to 5 need only 13.1. Act 3 needs a swept article in all three tools, and Copper is one. Act 4's gap needs an article with no rig output, and Enamel is one. Act 5's "renders anywhere" property cannot be judged on an iPad; the agent's real-path smoke owns it (§Tests), and the lead judges only that the download works and holds what it should.
- **The doers:** the agent builds and verifies; publishing uses the lead's `gh` login on the library machine (`admin` on the repo, measured 2026-10-14). ✓ **The push and the publish are the lead's word, asked once, together** (§Risk lane).

### Later sittings

- **13.2:** the lead reads each material's label, summary and search words beside its picture on a words sheet (built like `tools/parity/review_pages.py`'s pages and opened for him on the library machine's desktop, with its path in the handback), and keeps or corrects them. The next snapshot (`…-dev.2`) carries them, and Copper's record in act 4 now has a summary.
- **13.3:** a `/matter-batch` row's review page shows the words the loop drafted, and the keep confirms them.

### In now / not now

| In now | Step |
|---|---|
| **The site file's contract**, `docs/specs/Contract/SiteFile.md`, **marked DRAFT** while only staging reads it (F-RO-26), written from the site's field list (F-P13-6) | 13.1 |
| **The dev snapshot as a GitHub pre-release:** the site file, pictures at web size, one MaterialX zip per material, `SHA256SUMS` (M9's ask, items 1 to 5) | 13.1 |
| **The parity verdict per Creator control**, carried with its measured date (WS-F6; Q-P13-4) | 13.1 |
| **The derived label** (split the PascalCase, drop the default tokens `Natural`, `Clean`, `Base`). It is a real field, derived the same way the site would derive it, but owned by the library (RD-WS-1 condition 4) | 13.1 |
| **The three layers** (F-MP-13): the runtime catalog stays technical and unchanged; the site file is the presentation layer; its compliance fields are those that exist (sources, licence) | 13.1 |
| **A contributor's handle**, as an optional field in the spec (RD-RO-2). Nothing records one today, so no article carries it | 13.1 (spec only) |
| **The words:** a label override, a one-line summary, search words, and the origin (procedural · scan · measured · agent-drafted; F-MP-18), written for the articles on disk and confirmed by the lead | 13.2 |
| **The loop writes the words** for every new row, and the review confirms them with the picture (F-MP-14; the seed's open question, Q-P13-6) | 13.3 |

| Not now → where | What it will consume from this phase |
|---|---|
| **Thumbnails** (the showcase pictures, RD-MP-2) → *Thumbnails* | the site file's picture list, which takes a `thumbnail` role beside the rig's `storm` / `blender` / `unreal` |
| **The approver** (F-MP-18), recorded per article → the first real release (*Release Bundle*): before it, the keep's status is the record, and an approver is a person's name in a public file | the spec's compliance block |
| **A completeness check before a release** (F-MP-15): a gate lane is a lead ruling, and pre-release nothing gates (`AI_WorkingAgreement.md` §Settled practices) → *Release Bundle* | the spec's list of required fields |
| **A picture of each moved control** (the site's Pass 3 list), **sweep pictures** and **character renders** → *Thumbnails* (F-MP-17's views) | the picture list's roles |
| **"Changed since the last release"** (the lockfile diff) → *Version Management* | the site file's `release` field |
| **Re-rigging the 39 un-rigged and the stale** (Q-P13-4) → the standing loop and *The Library Service*; each later snapshot carries what exists | the snapshot tool, unchanged |
| **The real release on GitHub with its digest** (RD-WS-2) → *Release Bundle*. The snapshot is a small slice of it and decides none of its contract (F-RO-27) | the publish command and the site file's spec |
| **Fit-set pictures in a zip** (hair cards, eyes: supplied when an article is bound, never referenced by it) → *Blender from a Release* / *Release Bundle* | the zip's layout (F-P13-9) |
| **Linking a handle to an account, Forseti** → the platform's (its ruling of 2026-10-14) | the handle field |

### The reuse check

**What the stack already provides, reused unchanged:**
- **The one list of articles:** `tools/converters/working_tree.py` `articles()`, which the dev catalog (`serve_to_stage.py`) and the Blender library already read. The snapshot lists the same 95, with the same statuses.
- **The identity fields:** `project_runtime_catalog.derive_entry` (`id`, `display_name`, `domain`, `material_class`, `scale`, `version`, `payload_path`).
- **The verdict word:** `tools/parity/rig.py` `moved_verdict` over each scorecard's `moved` values. It is not re-derived.
- **The portable rewrite:** `tools/conformance/build_portable.py`'s copy-and-rewrite to `./textures/<name>` (the exporter's complete-portable form, which the site's ask names).
- **The pre-release publish:** `unreal/publish.sh`'s `gh release create … --prerelease --target <pushed sha>`.
- **Pictures:** the rig's own `defaults.png` / `defaults__close.png` per tool (512 px, measured), re-encoded with Pillow (12.3, in the project env).

**Each new layer, and the gap that justifies it:**

| New | Beside | The gap |
|---|---|---|
| a snapshot builder in `tools/releases/` (working name `build_snapshot.py`) | `serve_to_stage.py` | the dev catalog is the engines' lean file (`no_projection_guard`); nothing projects the presentation fields, packs a zip per article or writes digests |
| the control **ranges** as data, beside `LCD_PORTS` in `lcd_ports.py` | `docs/specs/Contract/LCDSchema.md`'s frozen table | the ranges exist only as spec prose (F-P13-4), and the site needs them per control |
| `build_portable`'s rewrite as a function taking any article | its Copper-only `main()` | it is hard-coded to one article (F-P13-5) |
| recipe keys for the words (13.2) | the recipe's `status` and `sources` | there is no home for a summary, search words or an origin (F-MP-14) |

### Decisions that bind

- **RD-P13-1 — Materials Described is Phase13** (the lead, 2026-10-14: *"/discovery materials definitions and numner the phase"*). It was the head of `## Future` (RD-RO-3), and `261014_R_RoadmapOrder.md`'s next step names it.
- **RD-RO-2 — Materials are CC0-1.0 only; a contributor's handle is carried as a courtesy and for Forseti tracking.**
- **RD-WS-1 — the site invents no fact; the library owns every fact it shows.** **RD-WS-4 — a file for the site beside each release, its shape a contract spec here; the runtime catalog unchanged.**
- **RD-MP-5 / RD-MP-6 — "thumbnail" is the published picture's word; thumbnails never go in git or LFS.** The snapshot's pictures are release assets.
- **F-RO-26, as the lead took it (RD-RO-3) — real fields only:** a field that does not exist yet is left out, never filled with a made-up value (`AI_WorkingAgreement.md` *No Mock Data Masquerading as Real*).
- **Pre-release: no release ceremony** (`AI_WorkingAgreement.md` §Settled practices). The snapshot is **not** a lockfile release: no stage, freeze, approval or `library/releases/` record.

**Closed by discovery, unless the lead says otherwise:**
- **Q-P13-1 — The tag is `matterlib-0.2.0-dev.N`**, the site's own example. It begins `matterlib-` (the site takes only those, M9 item 1), sorts after the pilot `0.1.0` and before any `0.2.0`, and `N` counts snapshots. It is a GitHub **pre-release**, as the Unreal builds are, so it never shows as Latest. **A row goes in `NamingConventions.md`** beside *Library release* and *Unreal runtime build*. The site file's `release` is `0.2.0-dev.N`.
- **Q-P13-2 — The snapshot lists every article on disk (95), each with its status**, the same set the dev catalog serves, and the set the site's browsing already shows (the site's ruling of 2026-10-14: every material the library has pushed, each with its status). `IMRSV_MissingMaterial` is listed with `creator_selectable: false`, as the catalog does. Kept-only would hide the 12 drafts the site already shows by status.
- **Q-P13-3 — Pictures: the test scene's default renders only**, wide and close, in each tool that ran, re-encoded at web size. **Never** a character render (`Character__*`; F-MP-17) and never a sweep picture. This keeps each material at **seven assets or fewer** (six pictures and a zip), **at most 667 for 95 materials**, inside GitHub's 1000-asset limit (F-P13-7).
- **Q-P13-4 — Evidence is published as measured, each verdict and picture with its date; nothing is re-rigged first.** Every scorecard predates `unreal-runtime-v4` (F-P13-2), so a coated article's Unreal picture may be older than what Unreal draws now. The date is the true field, and later snapshots carry fresher evidence as the loop re-rigs. Re-rigging all 95 first is 11 to 35 GPU hours on the laptop (F-MP-44's 7–22 minutes each) for a staging-only snapshot.
- **Q-P13-5 — The file is `matterlib-<release>.site.json`**, beside the `.catalog.json` naming. Its spec is `docs/specs/Contract/SiteFile.md`, and its term, *site file*, goes in the Glossary. **The snapshot is built into a git-ignored folder, `library/snapshots/<tag>/`, never into `library/releases/`** (F-P13-8).
- **Q-P13-6 — Words for the articles on disk first (13.2), then the loop writes them (13.3).** This answers the seed's open question: the 95 already exist and the site shows them now. A change to `/matter-batch` alone would describe only new rows.
- **Q-P13-7 — Digests in one `SHA256SUMS` file** (`sha256sum -c` format) covering every asset, the site file included; a file cannot carry its own digest. The site file also lists each picture's and zip's sha256 beside its name, as the site asked (M9 item 5).

### Risk lane — `build`, verified against the tree

**Controls read (2026-10-14):**
- **The release lifecycle's gates enumerate `library/releases/`:** `run_all.py` globs `*.lock.yaml`, `matterlib-*.catalog.json`, `*.freeze.json` and `*.approval.json` there, and `check_fixture_sync.py` globs `*.catalog.json`. **The snapshot never writes there** (Q-P13-5), so no gate sees it. Nothing globs `library/snapshots/`, and it is added to `.gitignore`.
- **What reads GitHub releases:** only `tools/parity/drivers/unreal.py`, which downloads **by the tag `unreal/RUNTIME.json` pins**. A new tag cannot displace it, and a pre-release never becomes "Latest".
- **The publishing credential:** the lead's `gh` login (keyring, `repo` scope, `admin` on the repo; measured). The tool holds no secret and writes none.
- **What becomes public:** CC0 content already public in the repo, plus the rig's pictures of the test scene. **Never `job.json`, `*.log` or `scenes/`:** they carry absolute local paths (F-P13-3). The builder takes the pictures by name, never a folder.
- **Publication is irreversible in effect** (a mirror may copy it within the hour) and **the lead's word** (`.claude/CLAUDE.md`, the public repo). `--target` needs `HEAD` pushed (`unreal/publish.sh`'s precedent), so **13.1 asks once for both: push `main`, then publish**, listing every commit the push carries (`main` was ahead of `origin` with siblings' commits at the time of writing).

No authorization, secret, migration or data-loss surface is touched. **`build`.**

### Step list

- **13.1 — The dev snapshot.** Write `SiteFile.md` (DRAFT) and the builder. It projects the site file for all 95, picks and re-encodes the pictures, packs a portable zip per article and writes `SHA256SUMS` into `library/snapshots/matterlib-0.2.0-dev.1/`. Add the ranges to `lcd_ports.py`, the tag row to `NamingConventions.md`, and *site file* to the Glossary. Then, on the lead's word, push and publish the pre-release. *First clickable result:* **acts 1 to 5.**
- **13.2 — The words, for the articles on disk.** Add the recipe keys (label override, summary, search words, origin) to `recipe.schema.json` and `validate_recipe.py`, as optional. The agent drafts them for all 95, and the lead confirms on the words sheet. The builder carries them, and `…-dev.2` is published on the lead's word. *First clickable result:* the words sheet, then Copper's summary in the published file.
- **13.3 — The loop writes the words.** `/matter-batch` (`.claude/skills/matter-batch/SKILL.md`) drafts the words at build time, `review_pages.py` shows them beside the picture, and `wishlist.py keep` confirms them. *First clickable result:* the next batch's review page.

**Split check:** two journeys could be shown apart: publishing what exists (13.1) and writing the words (13.2, 13.3). **They are kept as one phase:** the Outcome is the lead's and names both, and 13.2 changes no shape, only fills fields 13.1's spec already defines. If the words wait on the lead's sitting for long, **13.2 and 13.3 are the steps to peel**, consuming the spec and the builder unchanged.

### Compact build map

- **`docs/specs/Contract/SiteFile.md`** (new, DRAFT): top level `schema_version`, `release`, `made` (the snapshot's date) and `materials[]`. Per material:
  - identity (`id`, `version`, `label`, `display_name`, `domain`, `material_class`, `master`, `scale`, `meters_per_tile`, `status`, `creator_selectable`);
  - `controls[]` (port, type, start value from the `.mtlx` interface, range from `lcd_ports.py`);
  - `wear_layers` (from the recipe's `overlays`);
  - `sources` (the recipe's; the lockfile's texture provenance for the pilot's twelve) and `licence: CC0-1.0`;
  - `parity` (per control: the verdict word and the tools that ran; one `measured` date per article);
  - `pictures[]` (role, tool, view, file, sha256) and `download` (file, bytes, sha256);
  - optional, absent until they exist: `summary`, `search_words`, `origin`, `contributor`.

  It names the rule that **an absent key means "not known yet"**, never a default. *Names are working names; the spec settles them.*
- **`tools/releases/build_snapshot.py`** (new): `--tag` and an `--out` default under `library/snapshots/`. It reads `working_tree.articles()`, the recipes, each `.mtlx` interface and `library/parity/<identity>/{scorecard.json,storm,blender,unreal}/defaults*.png`, then writes atomically. A separate `--publish` runs `gh release create <tag> --prerelease --target <sha> --notes-file …` with every asset. It **refuses unless the target sha is on `origin/main`**, and the agent runs it only on the lead's word.
- **`tools/converters/lcd_ports.py`:** a `LCD_RANGES` table copied from LCDSchema's frozen table, plus a unit asserting it covers every `LCD_PORTS` name.
- **The zip:** `build_portable`'s rewrite as a function. ⛔ **It lives under `tools/conformance/`, so `check_exporter.sh` is baselined before the edit** (`LOCAL_DELTAS.md`). The cheaper way is a sibling function in `tools/releases/` that follows the same rewrite, leaving `build_portable.py` untouched; execute chooses and says which.
- **13.2:** `recipe.schema.json`, `validate_recipe.py`, the 95 recipes' new keys, and a words sheet (one page per class, built like `review_pages.py`'s). **13.3:** `SKILL.md`, `review_pages.py`, `wishlist.py`.
- **Docs at close:** `RuntimeCatalog.md` (its *"planned; its name and spec are not written yet"* note points at `SiteFile.md`); `Consumers.md` §The library's website; `Catalog.md` §Thumbnails (the snapshot is not the thumbnail set); `PlatformDependencies.md` M9 (the snapshot published; what remains); `ToolingConventions.md` (the builder, `library/snapshots/`); `NamingConventions.md`; the Glossary.

**Tests, inside the `build` ceiling:**
- `run_all.py` green before and after;
- units for the pure parts: label derivation; the verdict per control from a scorecard (swept, defaults-only and missing); the ranges cover every port; picture selection excludes `Character__*`, `job.json` and logs; the asset count stays under 1000;
- **one real-path smoke:** unzip Copper's zip into an empty folder with no MaterialX or USD search path set, and render it there (usdrecord on a one-sphere stage referencing `./Copper_….mtlx`). The picture is not magenta, and every texture resolves inside the folder.

**Hazards:**
- **Upload size:** all textures total 162 MB (base 115, shared 18, fit 29; measured). Each zip repeats the shared wear layers it uses, so the release is a few hundred MB. Measure it at build, and name it in the publish ask.
- **The 1000-asset limit binds at about 140 materials** at seven assets each. Splitting belongs to *Release Bundle* (F-MP-30). The builder fails loudly past the limit rather than dropping assets.
- **A sibling may be committing on `main`** (one numbered Phase14 during this discovery). The push lists every commit it carries (`.claude/CLAUDE.md` §Git, the push row).

---

## Findings (Pass 1, 2026-10-14)

- **F-P13-1 — 95 articles on disk:** 60 candidate, 23 approved, 12 draft. Masters: Opaque 49, Subsurface 27, TranslucentThin 6, Masked 3, TranslucentThick 3, Emissive 3, TwoLayer 2, Hair 1, system 1 (`working_tree.articles()`, measured).
- **F-P13-2 — Rig evidence exists for 56 of the 95, not 72.** `library/parity/` holds 72 scorecards, but 16 are probes or character runs (`ProbeP07*`, `Character__*`). Of the 56:
  - 46 were swept, which gives a verdict per control;
  - 10 have defaults only;
  - 43 have an Unreal column.

  39 articles have no rig output at all, among them the nails, eye parts, gum and enamel. Every scorecard is dated 2026-09-27 to 2026-10-05, **before `unreal-runtime-v4` (2026-10-11)**, which changed the Unreal pictures of 27 coated articles (F-MP-4). *(F-RO-25's "72 of them with a scorecard" counted the probes; corrected here, not there.)*
- **F-P13-3 — The rig's working files carry absolute local paths:** `job.json` records the scene and the output folder by their full paths on the laptop, and the logs are similar. Only pictures are published.
- **F-P13-4 — The control ranges exist only as spec prose** (LCDSchema's frozen table). `LCD_PORTS` holds names, types and defaults, and the rig's `SWEEP` holds sample values, not ranges.
- **F-P13-5 — `build_portable.py` is hard-coded to Copper.** It is the proven rewrite, but it is not yet a tool for any article.
- **F-P13-6 — The site's "drafted shape" is a field list, not a file.** The site's research (its Pass 3) and its phase's ask are on its origin, read-only, 2026-10-14. The script it calls *the draft of the file's shape* is not. It says: *"If the library wants a different shape, it says so, and this side follows."* So the library writes the shape from the field list, and the site adopts it.
- **F-P13-7 — GitHub's limits** (GitHub's *About releases*, as relayed on the site's side, 2026-10-14): under 2 GiB a file, and up to 1000 assets a release. Seven assets per material fits 95 (Q-P13-3).
- **F-P13-8 — The release lifecycle's gates glob `library/releases/`** (§Risk lane). A snapshot written there would be read as a release.
- **F-P13-9 — Fit-set pictures are not referenced by any article** (`_Architecture.md` §Textures). The Hair and eye articles' zips therefore carry no card or iris picture, and the spec says so.
- **F-P13-10 — Learnings:** this phase changes no renderer, master, add-on or toolchain behaviour; it projects, packs and publishes. No `docs/Learnings/` entry applies (Blender, Storm, Unreal, MaterialX and ClaudeCode headings read).

## Depends on

Nothing to start. *Thumbnails* later adds the showcase pictures to the same file. ~~*Two Licences* supplies each article's licence.~~ Every article is CC0-1.0 (RD-RO-2, 2026-10-14).

## Sources

`261014_R_TheLibrarysSite.md` (RD-WS-1 to RD-WS-4, WS-F3 to WS-F6) · `261014_R_MaterialPipeline.md` Passes 1 and 3 (F-MP-3, F-MP-13 to F-MP-18) · `261014_R_RoadmapOrder.md` Pass 6 and RD-RO-2 (F-RO-24 to F-RO-29) · `PlatformDependencies.md` M9 · the platform's site phase, its *Needs the library* section and its research Pass 3 (read-only at its origin, 2026-10-14; no private detail copied).

## Discovery Log

- **Pass 1 (2026-10-14):** numbered by the lead (`ca8c60d`). The product docs were read from `_Architecture.md` down to RuntimeCatalog, Catalog, Consumers and LCDSchema, then the three research docs above, the site's ask and the tree. The seed agrees with the product docs; the one correction is F-P13-2's count. **The Brief was written in this pass; no question needs the lead before `/execute`.**
