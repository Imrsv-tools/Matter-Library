# Research — Matter, Character and HDRI: what the website must change

**Opened:** 2026-10-14 · **Mode:** research, written by the library for the website's session. It commits the website to nothing; the website's own discovery rules each ask.
**Mnemonic:** `GWA` (ids `GWA-Fn`, `GWA-Qn`).
**Asked by:** the lead, 2026-10-14, after Phase15 closed: *"write these up in <> docs in research and push.. I will goto those systems and get them done"*.
**From:** [Phase15 — Matter, Character and HDRI](../Phases/Complete/Phase15_MatterCharacterHdri.md) (closed `c474572`). Ledger rows: [PlatformDependencies](../PlatformDependencies.md) **M11** (1) is answered and **P25** holds the website's half. It answers the website's *Beside Matter* ask 1: relay a structure for the Character group.
**The contract:** [SiteFile](../../specs/Contract/SiteFile.md), still **schema 2** (DRAFT).
**Where:** the dev snapshot [`matterlib-0.2.0-dev.4`](https://github.com/Imrsv-tools/Matter-Library/releases/tag/matterlib-0.2.0-dev.4), the asset `matterlib-0.2.0-dev.4.site.json` (95 materials, 59 HDRIs, 432 assets).

---

## What changed in the library (2026-10-14)

- **The library has three groups: Matter, Character and HDRIs**, each browsed by its own taxonomy (the lead, RD-DS-1).
- **Character's rows are the six the lead ruled** on the website's side: Eyes, Hair, Skin, Nails, Teeth, Mouth. Across the 30 Character materials they hold 5 · 2 · 6 · 7 · 1 · 9.
- **The 30 Character materials moved folder**, so their **`id`s changed**: `biological/tissue/Skin_FitzpatrickIV_Clean_Base_s001` is now `character/humanoid/skin/Skin_FitzpatrickIV_Clean_Base_s001`. Their names, `identity`, labels and zip names did not change.
- **Each material's group is now declared in its own file.** `section` is read from that, never from the domain.

---

## Ask 1 — accept site-file schema 2 (first, and required)

The mirror accepts only `schema_version` 1 and refuses anything else (the website's own finding, F-MSG-2). So staging still shows `dev.2`, and **nothing from `dev.3` or `dev.4` reaches the site** until it accepts 2.

Keep refusing an unknown schema (3 or later). **Every Phase15 change is additive inside schema 2**, so no further version step is needed for it.

---

## Ask 2 — build the browse from the groups

**What `dev.4` carries:**

| Field | Where | What it holds |
|---|---|---|
| `groups[]` | top level | `matter`, `character`, `hdris` in browse order, each with `label`, `list`, `section`, `shown` and (**new**) `taxonomy`: the fields it is browsed by |
| `groups[character].rows` | **new** | `[{species: "humanoid", label: "Humanoid", parts: [{id: "eyes", label: "Eyes"}, …hair, skin, nails, teeth, mouth]}]`, in order |
| `materials[].group` | **new** | `matter` or `character`; `section` holds the same value |
| `materials[].species`, `.part` | **new**, Character only | `humanoid`; `eyes` … `mouth` |
| `hdris[].group`, `.when`, `.sky` | **new** | `hdris` · `sunrise-sunset` 28, `morning-afternoon` 15, `midday` 11, `night` 5 · `clear` 24, `partly_cloudy` 26, `overcast` 7, `fog` 2 |

**The changes:**
1. **The row above the Dig** (Matter · Character · HDRIs) comes from `groups[]`, in its order and with its labels (the website's RD-MSG-1, unchanged).
2. **Character's rows** come from `groups[character].rows`, matched on each material's `part`. **This replaces the stand-in classes** (Tissue, Keratin, Bone; the website's RD-MSG-3).
3. **HDRI rows** read `when` and `sky`. They are Poly Haven's own words, one value each per HDRI. Merging them into *Day / Sunrise & sunset / Night* and *Clear / Cloudy* stays the website's presentation.
4. **Never decide the group from the domain.** A future generic biological material (a generic skin pattern) will be `matter`.

---

## Ask 3 — check nothing is keyed on the full `id` (GWA-Q1)

The 30 Character `id`s changed with their folder. A material's page address appears to come from its **name** (`copper-verdigris-aged-base-s01`), which did not change; that was read from the website's fixture filenames, not its code. **Please confirm** that no slug, cache, link or stored row uses the full `id`. If one does, it needs the new value.

---

## Not in `dev.4`

- **The *"Free 16K HDRI"* sentence and `edited_from` as a name plus an address** (the website's *Beside Matter* asks 3 and 4): the library's Phase16.
- **Creator and licence per entry:** Phase16.
- **Character pictures:** none yet. A Character material keeps its labelled swatch (the website's RD-MSG-2) until the library's Thumbnails phase.

**Done when.** On staging, the site shows Matter, Character and HDRIs as three things to browse: Character by Eyes, Hair, Skin, Nails, Teeth and Mouth, and HDRIs by when and sky, all read from `dev.4`'s site file.

---

## Status

- **2026-10-14:** written by the library at the lead's word. A summary was also sent to the website's live session. **The website's pass is owed**, taken up in a website session.
