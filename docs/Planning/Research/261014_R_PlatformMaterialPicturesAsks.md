# Research — A material's picture in the dev install: what the platform asks

**Opened:** 2026-10-14 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `PIC` (ids `PIC-Fn`, `PIC-Qn`). **Pass 1** is written from the platform's side.
**Requested by:** the IMRSV platform's lead, 2026-10-14 (*"write the ask"*), for the platform phase that builds the app's material picker, now in discovery. The lead ruled the direction; this doc hands the library its half.

**Question:** can the dev install serve each material's thumbnail, named in the dev catalog, the way it already serves each HDRI's?

**Extends, does not replace:** [Phase17 — Thumbnails](../Phases/Phase17_Thumbnails.md) (its *Not now* row *"Thumbnails served in the dev install"*, and F-P17-24), [RuntimeCatalog](../../specs/Contract/RuntimeCatalog.md) §HDRIs (`hdris[].thumbnail_path`), [PlatformDependencies](../PlatformDependencies.md) M10, P19, P3.

**Public-repo note.** The platform's planning is private. It is summarised here by what it does with the library and what it needs — no platform paths, code or ruling ids.

**Measured at:** `fd48642` (`origin/main`, 2026-10-14) and the published pre-release `matterlib-0.2.0-dev.6`.

---

## The short version

- **The thumbnails are made and published** — 83 materials, WebP at 1024, in the site file and the `dev.6` release. The website can show them.
- **The platform's app cannot.** It reads the library only through the dev install (and, in a packaged build, the copy of it the build carries — P3). The dev install serves no material picture, and the app reads PNG and JPEG, not WebP.
- **This is the library's own *planned* row** — *"Thumbnails served in the dev install (a `thumbnail_path` per material in the dev catalog, under `thumbnails/materials/`, the way HDRIs are, M10)"* — held because *"No consumer has asked for it."* **The platform asks now.**
- **One ask that matters (A1)**, two that shape it (A2, A3), and one for later (A4).

---

## Pass 1 — What the platform does with a material's picture, and what it needs

*Written from the platform's side, 2026-10-14.*

### What was measured

- **PIC-F1 — What is published.** `matterlib-0.2.0-dev.6` (pre-release, 2026-10-14 21:09 UTC) carries 475 WebP pictures. By their file names, **83 materials have a thumbnail**: Matter by `card` (53) and `close` (49); Character in a human context by `hand` (13), `lips` (7), `face` (6), `eye` (5), `mouth` (3), `head` (2) and `dark` (2). The 59 plain `thumbnail` files are the HDRIs'. The site file lists each material's thumbnails first in its `pictures[]`, `role: thumbnail` ([SiteFile](../../specs/Contract/SiteFile.md)).
- **PIC-F2 — What the dev install serves.** On the consumer's machine, the served `thumbnails/` folder holds `hdris/` alone. The served catalog's material entries carry fifteen fields — `contributor`, `creator_selectable`, `display_name`, `domain`, `group`, `id`, `licence`, `master`, `material_class`, `part`, `payload_path`, `scale`, `species`, `status`, `version` — and no picture. `groups[]` shows Matter by `rig`. Both are as F-P17-24 rules: *"the dev install serves no thumbnails."*
- **PIC-F3 — What the consumer can draw.** The app's picture card takes PNG or JPEG and turns anything else away. Its engine, Unreal Engine 5.8, has no WebP reader at all (its image module lists PNG, JPEG, BMP, ICO, EXR and others; none is WebP). The HDRIs' 1024 × 512 JPEGs are the shape it is built for.
- **PIC-F4 — How the consumer shows a material.** A card per material in its picker, the picture drawn at about 180 × 120 on a 4K panel canvas, and up to every Creator-selectable material in one window (94 today). The material bound to an object is shown again, at about 200 square, on that object's material panel. At 1024 × 1024 each picture is about 4 MB once decoded — worked out, not measured.
- **PIC-F5 — Where the pictures are.** The 1024 × 1024 master PNGs are git-ignored in `library/thumbnails/<identity>/` on the machine that made them. The consumer's machine has a checkout of this repo and serves the dev install from it, and has no such folder (listed, 2026-10-14). The published WebP snapshot is the one copy every machine can reach.

### The asks

| # | Need | Why it matters to the consumer | What exists today |
|---|---|---|---|
| A1 | **Each material's thumbnail served in the dev install and named in the dev catalog** — one picture per material, the one the library shows first (Matter's `card`, Character's first human-context view), by a path field on its `materials[]` entry as `hdris[].thumbnail_path` names an HDRI's. A material with no thumbnail has no field. | A Creator finds a material by its picture. The app's picker and panel show grey placeholders until a picture is named where the app reads. | The library's own planned row (Phase17, *Not now*), the shape of `thumbnails/hdris/` (M10). |
| A2 | **A format the consumer reads: JPEG (or PNG).** The size is the library's to state; the consumer draws it at about 200 pixels at most, many at once (PIC-F4). | WebP cannot be drawn (PIC-F3). A smaller picture costs the window less memory. | The HDRIs' 1024 × 512 JPEG. |
| A3 | **The same on any machine that serves the dev install**, not only the one that made the masters. | The consumer's app runs on a machine that holds the checkout and not the git-ignored masters (PIC-F5). | The HDRI picture is made at serve time from a file every checkout holds. |
| A4 | **Later: the same in a release**, as a release asset, with the first release that ships pictures — as the HDRI's row already plans. | A packaged build carries what the library serves (P3). | Planned for HDRIs only. |

### Questions for the library

- **PIC-Q1 — Where does the serve tool take a material's picture from on a machine without the masters?** The published snapshot's WebP is there to convert; the masters could travel; or the tool could make them. The consumer needs only A1 – A3 to hold; the way is the library's.
- **PIC-Q2 — Does Matter's `shown` in the dev catalog become `thumbnail` once the pictures are served** (F-P17-24's reason gone)? The consumer does not read `shown` to find a picture; it reads the path field.
- **PIC-Q3 — One picture per material, or more?** The consumer asks for one. A second view (Matter's `close`) is not asked for.

### What the platform does next

- Its picker phase is in discovery now. It builds the card and the panel's picture against what A1 names, with a fixed placeholder where a material has no picture, and shows the library's pictures the day the dev install serves them.
- The first look in the app — and in a headset — is reported back here.

### A suggested ledger row

For `PlatformDependencies.md`, *From IMRSV to the Matter Library*. The library writes its own row; this is a draft.

> **M13** · **A material's thumbnail in the dev install** (2026-10-14): each material's first thumbnail served in the dev install and named on its dev-catalog entry, as an HDRI's is, in JPEG or PNG, on any machine that serves the dev install; in a release later. · *The platform's app finds a material by its picture; it reads only the dev install, and draws PNG and JPEG.* · Matter Library (the serve tool, the catalog field) · the platform's runtime and app (the consumer side) · `261014_R_PlatformMaterialPicturesAsks.md` A1 – A4 · OPEN
