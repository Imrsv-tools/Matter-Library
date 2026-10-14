# Research — Matter, Character and HDRI: what the platform (Stage and Studio) must change

**Opened:** 2026-10-14 · **Mode:** research, written by the library for the platform's session. It commits the platform to nothing; the platform's own discovery rules each ask.
**Mnemonic:** `GPA` (ids `GPA-Fn`, `GPA-Qn`).
**Asked by:** the lead, 2026-10-14, after Phase15 closed: *"write these up in <> docs in research and push.. I will goto those systems and get them done"*.
**From:** [Phase15 — Matter, Character and HDRI](../Phases/Complete/Phase15_MatterCharacterHdri.md) (closed `c474572`). The ledger rows are [PlatformDependencies](../PlatformDependencies.md) **P27** and **P25**.
**The contract:** [RuntimeCatalog](../../specs/Contract/RuntimeCatalog.md) §Groups · [Taxonomy](../../specs/Ontology/Taxonomy.md) §Character · [Consumers](../../specs/Consumers.md) §USD viewers.

---

## What changed in the library (2026-10-14)

- **The library has three groups: Matter, Character and HDRIs**, each browsed by its own taxonomy (the lead, RD-DS-1):
  - **Matter:** by Domain, then Class (unchanged);
  - **Character:** by species, then part; humanoid today, with the parts Eyes, Hair, Skin, Nails, Teeth and Mouth;
  - **HDRIs:** by *when*, then *sky*, in Poly Haven's own words.
- **The 30 character materials moved** from `materials/biological/<class>/` to **`materials/character/humanoid/<part>/`**. **Their names did not change.** Each file now declares `group`, `species` and `part` in its `imrsv_metadata`. A file with no `group` is Matter.
- **The dev catalog** (`releases/matterlib-dev/matterlib-dev.catalog.json` in the dev install) carries the groups. The change is additive, so **`schema_version` is unchanged** (3 with HDRIs).

---

## Ask 1 — URGENT: resolve bare names from every folder under `materials/`, at any depth (P27)

**Why it is urgent.** Today Stage takes as its search roots **exactly the folders two levels below `materials/`** (`<domain>/<class>/`). The 30 character materials now sit **three** levels down. **Studio cannot bind them by bare name from the dev install until Stage walks every depth.** That covers skin, eyes, hair, nails, teeth and mouth: the character.

**The change.** Put on the search path every folder under the release's `materials/` that holds a `.mtlx`, at any depth. This is the library's stated rule ([Consumers](../../specs/Consumers.md) §USD viewers). USDLiveView's launcher already works this way, and draws all 30 (judged 2026-10-14).

**What does not need changing.**
- Saved compositions: they name materials bare (`@Skin_FitzpatrickIV_Clean_Base_s001_v01.mtlx@`), and the names are unchanged.
- The selector, the catalog's location, `payload_path` resolution, textures: a release folder is still self-contained.

**One thing to check on the platform's side (GPA-Q1).** **The 30 catalog `id`s changed**: `biological/tissue/Skin_FitzpatrickIV_Clean_Base_s001` is now `character/humanoid/skin/Skin_FitzpatrickIV_Clean_Base_s001`. Anything Stage or Studio stored **by `id`** rather than by name (a wardrobe or character table, a cache, a test fixture) needs the new value. The platform's own frozen fixture copy of the skins is its own business and is unaffected.

**Done when.** In Studio, from the dev install, the character wears the library's skin, eyes, hair, nails, teeth and mouth with nothing magenta.

---

## Ask 2 — pass the groups through, and browse by them (P25)

**Why.** Stage drops a catalog key it does not know (measured for `master`, 2026-09-27). The groups therefore reach Studio only once Stage passes them on.

**What the dev catalog carries now** ([RuntimeCatalog](../../specs/Contract/RuntimeCatalog.md) §Groups):

| Field | On | Values |
|---|---|---|
| `groups[]` | the catalog (top level) | the three groups in browse order: `id` (`matter`, `character`, `hdris`), `label`, `list` (`materials` or `hdris`), `section`, `shown` (`rig`, `human`, `thumbnail`), `taxonomy` (the fields it is browsed by), and for Character `rows` (per species, its parts' `id`s and `label`s in order) |
| `group` | every material | `matter` or `character` |
| `species`, `part` | Character materials | `humanoid`; `eyes`, `hair`, `skin`, `nails`, `teeth`, `mouth` |
| `domain`, `material_class` | every material | unchanged for Matter. On Character they say **what it is made of** (`biological` / `tissue`), **not** where it is browsed |
| `group`, `when`, `sky`, `tagging` | every HDRI | `hdris` · `sunrise-sunset`, `morning-afternoon`, `midday`, `night` · `clear`, `partly_cloudy`, `overcast`, `fog` · Poly Haven's full `tagging` (the platform's ask A10) |

**The changes, in order:**
1. **Stage** carries these fields to its clients: in the catalog read, in the material and HDRI lists it sends, and on the wire.
2. **Studio's material picker** shows Matter and Character apart, built from `groups[]`:
   - Matter by Domain, then Class (this also covers P6: classes from the catalog, not a hard-coded list);
   - Character by species, then part, in `rows` order.
   - **It never decides the group from the domain.** A future generic biological material will be Matter.
3. **Studio's HDRI window** may filter by `when` and `sky`. Grouping Poly Haven's words into fewer rows (Day, Cloudy) is Studio's presentation.

**Not part of this ask.**
- Creator and licence on each entry: the library's Phase16, ledger P26.
- A released catalog carrying these fields: the first release after Phase15. **The dev install is where they are today.**

**Done when.** Studio's picker shows Matter, Character and HDRIs as three things to browse, each by its own taxonomy, read from the catalog.

---

## Pass 2 — the platform's pass (2026-10-14)

*Written from the platform's side, at the lead's word: "is there anything you need to / want to relay back to the Matter library... just update and push the doc". Read against the platform's own code; what is stated here about it is not verifiable from this repo (private code).*

- **Ask 1 (P27) — confirmed, and taken now.** Stage takes as search roots exactly the folders two levels below `materials/`, so the 30 Character materials are not found by bare name. Nothing else on the platform's side depends on the depth: a material's textures are reached by its own relative path, and a pick from Studio's picker finds its file through `payload_path`. The lead ruled the change be made at once: Stage will search every folder under `materials/` that holds a `.mtlx`, at any depth, as [Consumers](../../specs/Consumers.md) says. **Done when** is the library's own: the character wears the dev install's skin, eyes, hair, nails, teeth and mouth with nothing magenta.
- **GPA-Q1 — yes, the platform kept the `id`, in every saved scene.** When a library material is bound, the platform names the material instance in the scene after the material's catalog `id`, and later recognises the instance by that `id`. So every scene saved before this regroup that holds a Character material names it `biological/tissue/…` (flattened) and **no longer recognises it**, even once Ask 1 is built. The bare `.mtlx` name inside it is unchanged and would resolve.
  - **The platform takes the loss.** It is pre-release; the lead: *"we do not need to be reverse compatible with previous compositions... we are still building and this is a part of growth... more will be coming soon"*.
  - **The platform will recognise a bound material by its bare name, not by its `id`** (the lead's ruling), so the next regroup costs scenes nothing. Not built yet.
  - **Asked of the library (GPA-Q2): say in the contract that the bare name is the stable key and the `id` is not.** Today [Identity](../../specs/Ontology/Identity.md) and [Consumers](../../specs/Consumers.md) say a material resolves by its bare name, but nowhere that the name survives a regroup while the `id` (where it is browsed) may move. The platform is about to lean on exactly that, and so does every saved scene in any consumer. A sentence in Identity, and a line in Consumers' *what a consumer may rely on*, would do. If the library can't promise it (a name that must change, say, for a rename), say what happens then, and the platform plans for it.
- **P6 — already true on the platform's side.** Studio's picker builds its class list from the catalog's classes; no class is hard-coded. Only its scale list is fixed. The row can close on this report.
- **Ask 2 (P25) — taken in the platform's work on HDRIs, now in discovery.** Stage reads nine keys per material today and drops the rest, and reads no `hdris` at all yet. The platform's HDRI work adds the HDRI list and is where Studio's library windows learn to narrow by rows, as the website does. The groups, their taxonomies and Character's rows come in with it, read from `groups[]`, and the group is never inferred from the domain.
  - **A10 is received:** `hdris[].tagging`, `when` and `sky` in the dev catalog are what the platform's Sky window narrows by. **A9 (the credit) waits on the library's Phase16** (P26), as this doc says.
- **One word note, no change asked.** In the platform, *group* already names an area of a Set or Prop, and *part* a shape added under an object. The platform's app will label the library's groups and Character's parts in words of its own; the catalog's field names are fine as they are.

## Status

- **2026-10-14:** written by the library at the lead's word. Both asks are in the ledger: P27 (urgent) and P25. ~~**The platform's pass is owed**, taken up in a platform session.~~
- **2026-10-14:** the platform's pass is Pass 2. P27 is being built now; P25 rides the platform's HDRI work; GPA-Q1 is answered (yes, and the platform moves to the name). **Owed by the library:** GPA-Q2 (the bare name as the stable key, in the contract), and the ledger rows P6 (closes on the platform's report) and P27/P25 (the platform's status).
