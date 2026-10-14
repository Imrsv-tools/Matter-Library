# Research — Where the library stands, and what each downstream tool must take in to use it correctly

**Opened:** 2026-10-14 · **Mode:** research. It gathers and commits to nothing.
**Mnemonic:** `DS` (ids `F-DS-n`, `Q-DS-n`, `RD-DS-n`).
**Asked by:** the lead, 2026-10-14: *"Somehow we are getting lost in a folder issue... so I am backing up and pasting a request here.... Can you make sense of where we are in the overall library and what you need the downstream tools to incorporate so they can use the library correctly?"*
**Altitude:** **audit and synthesis.** It says what exists and what each consumer reads, and it gathers in one place the asks that sessions in other repos addressed to the library today. It designs nothing beyond a logical sketch. The ledger is still [`PlatformDependencies.md`](../PlatformDependencies.md), and the contract is still [`Consumers.md`](../../specs/Consumers.md) and the specs it points to. This doc is a map over them.

**Read for it** (2026-10-14, all read and not run unless marked *measured*):
- **This repo** at `bbbb6ab` (the platform's HDRI Pass 3 merged in): the Roadmap, `PlatformDependencies.md`, `Consumers.md`, `ReleaseModel.md`, `RuntimeCatalog.md`, `SiteFile.md`, `Taxonomy.md`, the research footers, `serve_to_stage.py`, `stage_release.py`, `build_snapshot.py`.
- **The live dev install** on the library machine, `$IMRSV_STAGE_RUNTIME/MatterLibrary/` (*measured*).
- **USDLiveView**, fetched: its `origin/main`, and a research doc written in a USDLiveView session today, on what sits beside Matter, read in place and not pulled. That repo is private: what is used here is the lead's ruling and the library-facing asks, by content.
- **The website's repo** at its `origin/main`, fetched: the *Beside Matter* research and its two siblings, read with `git show`. The checkout was not pulled.
- **The platform's HDRI asks** came in as Pass 3 of [`261013_R_PlatformSkyAsks.md`](261013_R_PlatformSkyAsks.md), merged at `bbbb6ab`.

---

## The current picture

**Where the library is (2026-10-14, *measured*):**
- **95 articles** in the source collection: 23 approved, 60 candidate, 12 draft. **30 of them are biological** (skin, eyes, mouth, nails, hair), the materials the lead ruled *"not Matter"* (Phase13).
- **59 HDRIs** (all of Poly Haven's *Pure Skies*). The default is `IndustrialSunset02_PureSky`.
- **8 Unreal masters**, built by script. The pinned test runtime is `unreal-runtime-v4`.
- **One real release, the pilot `matterlib-0.1.0`, with 12 articles.** Nothing since. Pre-release, no release ceremony gates anything.
- **Two ways consumers get the library today:**
  - **The dev install**, for engines and viewers: `serve_to_stage.py` projects the working tree into an install root under the name `matterlib-dev`.
  - **The dev snapshots**, for the website: GitHub pre-releases `matterlib-0.2.0-dev.1` to `-dev.3`, each with the site file (schema 2 since dev.3).
- **Active:** Phase15, *Scale Grids* *(renumbered Phase18 the same evening, behind this doc's three phases, RD-DS-6)*. **Not started:** *Release Bundle and Consumer Contract*, the phase that makes a real, downloadable release.

**The folders, once, as a consumer must see them.** The library has **two trees**, and a consumer must only ever see the second:

```
the producer (this repo; never read by a consumer)
MatterLibrary/materials/<domain>/<class>/<Name>_vNN.mtlx
MatterLibrary/textures/{base,shared,fit}/…
MatterLibrary/hdris/<Name>_<Variant>_vNN.hdr

the install root (what every consumer reads)
<root>/active-release.json                       {"active_release": "<name>"}
<root>/releases/<name>/<name>.catalog.json       the runtime catalog: the ONLY entry point
<root>/releases/<name>/materials/…               payload_path is relative to the catalog
<root>/releases/<name>/textures/…                articles reach it as ../../../textures/…
<root>/releases/<name>/hdris/…                   (since Phase14)
<root>/releases/<name>/thumbnails/hdris/…        (since Phase14; made at serve time)
```

- **In the dev install** `<root>` is `$IMRSV_STAGE_RUNTIME/MatterLibrary/` and `<name>` is `matterlib-dev`. `materials/`, `textures/` and `hdris/` are **links into the checkout**. The catalog and the thumbnails are real files.
- **A release folder is self-contained** (*measured*). Every texture path in every article climbs to `textures/` inside the same release folder. Nothing points beside `releases/<name>/`. This is the rule the platform's packaged build relies on (F-DS-3).
- **The rule for every consumer:** find the release through the selector, read the catalog, and resolve everything relative to it. **Never a path into `MatterLibrary/`.** If a doc tells a consumer to read under `MatterLibrary/…`, the doc is wrong (F-DS-2).

---

## Pass 1 — what is loose, and why it reads as "a folder issue" (audit, 2026-10-14)

**F-DS-1 — The install layout in the spec is a Phase14 behind.** [ReleaseModel](../../specs/Distribution/ReleaseModel.md) §Install-root layout lists only `materials/` and `textures/` (incl. `.dds`). The dev install has also held `hdris/` and `thumbnails/hdris/` since 2026-10-14. [RuntimeCatalog](../../specs/Contract/RuntimeCatalog.md) §HDRIs is right about them. The layout block is the page a consumer reads first, so it is the one that misleads.

**F-DS-2 — Consumers are told to take the character's fit pictures from a checkout path, and a real release would not carry them.**
- Ledger row **P21** tells Studio to take each hairstyle's and eye colour's picture from `MatterLibrary/textures/fit/makehuman/…`. That is the producer tree.
- In the dev install the same files are at `releases/matterlib-dev/textures/fit/makehuman/…`, through the link. That is where a consumer should read them.
- **In a real release they would be absent.** `stage_release.py` copies *"exactly the textures this release's lock names"*. No article names a fit picture, because each one is supplied at binding. So a release built today would carry no hair or eye pictures.
- The *Release Bundle* phase owes them a place (Q-DS-5).

**F-DS-3 — The platform's packaged-build asks have had no library pass since 2026-10-11.** [`261011_R_PlatformBuildInstallAsks.md`](261011_R_PlatformBuildInstallAsks.md) has no Status footer and no library pass. Its suggested ledger notes on **P3** and **P19** are not written. What it asks:
- **A1:** say that a release folder is self-contained, as a rule. It holds by measurement (above).
- **A2:** give the dev install an identity of its own.
- **BI-Q1:** may a build for other people carry the dev install?
- **BI-Q2:** is a bundle installed into the same layout?
- **BI-Q3:** is the selector's one key stable?

**F-DS-4 — Today's lead ruling about the library was recorded in a consumer's repo, not here.** The lead's model of *three groups: Matter, Character and HDRI* was ruled in a USDLiveView session today, and recorded there. It is recorded here as **RD-DS-1** (§Resolved). That session's network map lists **four things only the library can do, none with a unit anywhere**:
- Character as a group of its own, with its own taxonomy;
- all three groups in the **runtime catalog**, not only the site file;
- the shared support info (creator, licence, name, taxonomy) in the runtime catalog;
- a picture rig per Character part.

**F-DS-5 — How `section` is decided today contradicts RD-DS-1.**
- The site file's `section` is worked out from the domain: `character` exactly when the domain is `biological` (`build_snapshot.py`, `section()`).
- RD-DS-1 keeps **generic** biological materials, *"a generic skin pattern … a generic hair material"*, in Matter.
- So the domain cannot decide it. Each article must declare its own group. The USDLiveView session reached the same rule: the group must not be guessed from the domain.
- **One consequence:** carrying today's `section` into the runtime catalog would spread the wrong rule to every engine. That is why this pass offers no quick fix for it.

**F-DS-6 — Two asks for "credit in the engines' data" are one decision.** The runtime catalog leaves out provenance, licence and credit on purpose (`no_projection_guard`; RuntimeCatalog §HDRIs). Two separate sessions ask today for that to change:
- **The platform's HDRI asks A9 and A10:** each HDRI's credit and its tagging, in what the dev install serves.
- **The third item in F-DS-4:** creator, licence and name for all three groups.

The **site file** already carries all of it, for every material and HDRI, in a shape the platform says *"would serve the consumer as it stands"*. That points to one answer: **serve the site file in the install too, beside the catalog** (Q-DS-1).

**F-DS-7 — The website's four asks are addressed to the library and not recorded here.** From its *Beside Matter* research, written for the library's public repo:
1. **The Character rows.** Publish, in the site file, which row each Character material sits in, with the rows' labels and order: **Eyes, Hair, Skin, Nails, Teeth, Mouth**. The lead ruled those six rows in the web's session today.
2. **A picture subject per row.** Until a picture exists, the site shows a labelled colour swatch. Nothing more is needed now. It is *Thumbnails*' work.
3. **The *"Free 16K HDRI"* sentence.** Poly Haven's own description reads as a claim about the library's 4096 × 2048 file. Keep it, trim it or annotate it.
4. **`credit.edited_from` is a Markdown link.** The platform's HDRI Pass 3 asks the same. Both would read the name and the address published as two fields.

**F-DS-8 — One platform fact is already out of date.** HDRI Pass 3 says USDLiveView's launcher change for the HDRI folder is not on that repo's origin. Fetched at 2026-10-14 evening, **it is on USDLiveView's `origin/main`**. M10's *"done in its repo"* stands.

---

## Pass 2 — what each downstream tool must take in (synthesis, 2026-10-14)

Each line points to the ledger row that owns it. The ledger's status is the authority. **"Reported"** means the platform says so, and it cannot be checked here.

### Every consumer, whatever it is

1. **Find the release through the selector.** Read `<root>/active-release.json`, then open `releases/<name>/<name>.catalog.json`. Never scan the folders, and never read `MatterLibrary/` (ReleaseModel; **P7** for USDLiveView).
2. **Read the catalog by field name, and ignore keys you don't know.** Today's catalog adds `master` on materials and, at schema 3, `hdris[]` and `default_hdri`. Later it may add support info (Q-DS-1) or a group field (Q-DS-2).
3. **Route each article by its own `master` token,** never by its class (**P4**, reported done).
4. **Resolve names bare through the USD search path:**
   - every folder under `materials/` that holds a `.mtlx`;
   - the `hdris/` folder, for a `DomeLight`'s `@<Name>_<Variant>_vNN.hdr@`;
   - plus the MaterialX standard-library path for your build ([Consumers](../../specs/Consumers.md) §USD viewers).
5. **Write and read Creator overrides with the connected carrier.** Every writer connects to the nodegraph input. Every reader uses `GetValueProducingAttributes()`. Add no rule of your own (**P11**). Read a port's start value from the nodegraph's interface input, never from the shader's input (**P23**'s warning).
6. **Carry every travel port the library lists,** at its declared type:
   - the original 9;
   - `overlay3_density` (**P12**);
   - `overlay{1,2,3}_color` (**P22**);
   - `transmission_color`, `emission_color`, `emission_luminance` (**P23**).
7. **Show each group as itself** (RD-DS-1): Matter, Character and HDRI browsed apart, from data the library publishes. **Never guess the group from the domain.** Until the library carries it in the install, a consumer cannot do this correctly (Q-DS-2).

### Stage runtime (the carrier for Studio, Theater, USDLiveView and export)

- Take a **release bundle** in place of the hand-synced mirror (**P1**). The bundle is not built yet. Until then, the **dev install** (**P19**).
- **The extractor:**
  - accepts `tiledimage` layer nodes with their two real-world sizes (**P13**);
  - carries the coat, fuzz and anisotropy values (**P16**);
  - skips `cutout_tex`'s empty `file` and reads the Material input (**P17**);
  - carries `base_color_map` (**P21**).
- **Read `hdris[]` and `default_hdri`** from the catalog, and carry them to its clients (**M10**). That is the platform's HDRI phase.
- **Pass through whatever the library adds for the groups and the support info,** when it adds them (Q-DS-1, Q-DS-2). Today Stage drops a catalog key it does not know ([RuntimeCatalog](../../specs/Contract/RuntimeCatalog.md) §Planned, measured for `master` 2026-09-27), so a new field reaches its clients only once Stage passes it on.

### UE plugin and Studio

- **Adopt the library's 8 masters** (**P20**). Build them with `build_masters.py` and the consumer switches (**M7**). Studio's side must match two things:
  - Substrate's budget at `r.Substrate.BytesPerPixel=160`;
  - every texture sampled as **LinearColor**, with linear defaults.
- **The picker:**
  - filters by the taxonomy's classes, not a hard-coded list (**P6**);
  - hides `creator_selectable: false`;
  - shows Matter and Character apart (RD-DS-1).
- **Characters:**
  - one mesh per substance; the body is done, the garments are still open (**P15**);
  - each card mesh's own cut-out map, supplied at binding (**P17**);
  - a real-scale detail UV set (**P18**);
  - hair and eye pictures from the library's fit set, read **from the install**, not the checkout (**P21**, F-DS-2);
  - the hair article on its own master (**M3**);
  - the lips and nails that match a skin tone found by the name's Variant (**M4**).
- **Packaged builds** carry the selector and the one release it names (**P3**: reported half done; F-DS-3).
- **The deploy installs one bundle per release** (**P2**).

### USDLiveView

- **Honour the selector** (**P7**). It still scans every installed release.
- **Keep the search path covering `hdris/`** (done today).
- **Offer the Creator controls the articles declare** (**P23**).
- **Then browse by group and show the support info.** That is the viewer's own phase, seeded today in its repo, and it waits on Q-DS-1 and Q-DS-2.

### The website (reads the dev snapshot or release on GitHub, not the install)

- **Read the site file, schema 2:**
  - `groups[]` gives the row above the browse: Matter, Character, HDRIs;
  - `hdris[]` gives each HDRI's credit and tags;
  - `section`.
- Its mirror refuses schema 2 today, so staging still shows dev.2.
- **Every download comes from the release, never this repo** (**P24**, **M9**).

### The platform's docs and umbrella repo

- **P9:** cut the platform's Matter spec tree down to pointers into this repo.
- **P10:** stop treating this repo as a submodule once P1 to P3 land.

---

## Pass 3 — what the library owes downstream, in order (2026-10-14)

Every consumer reads what the library publishes, so the library's items come first. **Unnumbered.** Order is position.

1. **Rule how the support info and HDRI credit reach the engines** (Q-DS-1). This one ruling answers HDRI asks A9 and A10 and half of RD-DS-1.
2. **Make Character a group each article declares, with its own taxonomy** (Q-DS-2). The taxonomy runs species, then part: humanoid today, then rows such as Eyes, Hair, Skin, Nails, Teeth and Mouth. **Then carry the group into the runtime catalog** (or the served site file, by Q-DS-1). This is design work at phase size, and no unit holds it today (F-DS-4).
3. **Answer the website's small asks:**
   - publish `edited_from` as a name and an address;
   - decide the *"16K"* sentence;
   - publish the Character rows once (2) sets them.
4. **The library's pass on the packaged-build asks:**
   - write A1 as a rule;
   - decide on A2, the install's identity;
   - answer BI-Q1 to BI-Q3;
   - write the P3 and P19 notes.
5. **Bring the specs and the ledger up to date** (F-DS-1, F-DS-2, F-DS-4, F-DS-7). This is doc-only.
6. **The *Release Bundle* phase** carries everything the dev install serves today:
   - HDRIs and their thumbnails;
   - the fit pictures;
   - the support-info file from (1).

---

## Pass 4 — the lead's model: materials work like assets, and Character is its own library (2026-10-14)

*Altitude: design, from the lead's rulings RD-DS-3 and RD-DS-4 (§Resolved). A logical sketch: it names no file to change.*

### What the lead asked for, in one line each

- **Same as assets.** Every entry (material, Character material, HDRI) says **who contributed it, its licence, its name and its place in the taxonomy**. Contributions are tracked for Forseti: who gave what, and how each thing does. None of this has to be shown all the time, but the library always knows it.
- **No sidecars.** The facts travel **inside the file**: in the `.mtlx` for a material, and in the `.hdr` for an HDRI, which is entirely the library's to write.
- **Character is its own library.** It has its own ontology that people can contribute to. Each piece fits a predefined part mesh, keeps its contributor's name, and is pictured on its own part.

### F-DS-9 — Half of the "inside the file" route already exists

- Every `.mtlx` already carries a metadata block, `imrsv_metadata`, with `master_material`, `scale_tag`, `meters_per_tile`, `domain` and `class`.
- The dev catalog already reads `master` **out of the file** and projects it (since Phase07). That is the same shape the lead is asking for.
- **So the sketch is short:** the block gains the contributor, the licence, the group (`matter` or `character`) and, for Character, its own taxonomy fields. The catalog projects them the way it already projects the master. An export of the `.mtlx` carries them with no extra step, because they are in the file.

### F-DS-10 — An `.hdr` can carry its own facts (probe, 2026-10-14)

- The Radiance format's header is text lines up to the first blank line. A reader looks for `FORMAT=` and skips any line it does not know.
- **Probe:** a copy of `AristeaWreck_PureSky_v01.hdr` with four lines added (`MATTER_ID`, `MATTER_VERSION`, `MATTER_LICENSE`, `MATTER_BUILDER`) after `FORMAT=`. **Blender 5.2.2 loads the copy at 4096 × 2048 with pixels identical to the original's** (a checksum over sampled pixels: 2166.3125 for both).
- **Not run:** USD's own image reader (`Hio` has no Python binding in the toolchain) and Unreal's importer. Both are checked in the build before anything ships.
- **The cost:** writing into the file changes its bytes. The record's `sha256` then describes Poly Haven's original, not the library's file. Phase14's claim that the default HDRI is *byte-identical* to the copy scenes use today would stop being true, and every place that relies on it needs to know.
- **Where the full credit goes:** a header line holds a short credit (contributor, role, licence). Poly Haven's long description and tags fit too, but whether that much should go into every file is a build choice.
- **Reproduction** (Python 3, standard library only; Blender's check: load both files with `bpy.data.images.load` and compare `pixels`):

  ```python
  import sys
  src, dst = sys.argv[1:]
  b = open(src, 'rb').read()
  i = b.index(b'\n\n')                       # end of the header
  extra = (b'MATTER_ID=AristeaWreck_PureSky\nMATTER_VERSION=v01\n'
           b'MATTER_LICENSE=CC0-1.0\n'
           b'MATTER_BUILDER=Poly Haven: Greg Zaal (Original), Jarod Guest (Sky edits)\n')
  open(dst, 'wb').write(b[:i + 1] + extra + b[i + 1:])
  ```

### F-DS-11 — What a sidecar is here, and what is not

- **A sidecar, to remove from what ships:** any per-entry file a consumer would have to read beside the entry to learn who made it or under what licence. **Nothing shipped is one today.** Credit has simply not reached the consumer at all (F-DS-6).
- **Not sidecars:**
  - **The catalog.** It is the library's index: one file for the whole release, so the app browses without opening 95 materials. It is projected **from** the files, as it already is for the master. The lead's *"a solution to share metadata and taxonomy so the Studio can consume it"* is this index plus the in-file facts.
  - **The site file.** It is the website's index, in the same way.
- **To decide in the build:** the per-HDRI records in `library/provenance/sources/hdris/` and the material recipes. These are producer-side sources: they never ship, and they are how an import is reproduced. The facts that matter get **written into the file from them**, so a consumer never needs them.

### F-DS-12 — Tracking *how it is doing* happens where the entry is used

- The library can write who contributed and a stable id plus version into every file. **It cannot see use.**
- A material applied in Studio or on a website download is counted where it happens, keyed by that id. The platform already does this for objects in a composition: each one carries its asset's id, version, maker and licence.
- **The ask, for the ledger:** a Matter material bound in a composition carries its id, version, contributor and licence the same way, read from the `.mtlx`. So does an HDRI set as a scene's sky, read from the `.hdr`.

### F-DS-13 — Character as its own library: what it means, against what exists

| The lead's requirement | What exists today | Gap |
|---|---|---|
| **Its own ontology, open to contributors** | 30 articles under the `biological` domain, in Matter's grammar (`Skin_FitzpatrickIV_…_s001_v01`) | A Character taxonomy: species (humanoid now; canine, equine later), then part (skin, eye, teeth, tongue, gums, lips, nails, hair, …). Its own name grammar, which **keeps the contributor's name visible**. |
| **Fits a predefined part mesh**, e.g. a set of teeth UV-mapped to the chosen teeth mesh | One approved human mesh (MakeHuman hm08, Glossary *Approved human mesh*). The rig already splits it into one mesh per substance (P15), and Skin Maps already plans *"skin maps per approved mesh version"*. Most of today's character articles are tiling Matter-style materials, which is why they read badly on a body. | Each part gets **its mesh named and versioned** as the target a contribution fits, and the maps are authored to that mesh's UVs. Skin Maps is the first instance of this rule, not a separate idea. |
| **Pictured on its own part, never on a cube** | Ruled at Phase13 and in *Thumbnails*' subjects (skin on half a face and hands; an eye on an eyeball; teeth on teeth). Nothing is built. | One picture rig per part, on that part's mesh. |
| **Generic biological stays in Matter** | — | A generic skin pattern or a generic hair, when one is made, is a Matter material that declares `group: matter`. |

**What this changes in Pass 3's order:** items 1 and 2 merge into *the facts inside the file*. Character becomes **its own phase sequence** (below). It is not a field added to Matter.

---

## Open questions

| Id | Question | Recommendation |
|---|---|---|
| ~~**Q-DS-1**~~ → **RD-DS-2** | ~~**How do creator, licence, credit and tags reach the engines?** (a) Widen the runtime catalog. This drops `no_projection_guard` for it. (b) **Serve the site file in the install, beside the catalog,** in the dev install now and in every release later. (c) A third, lean file just for credit. | **(b).** The site file already holds it all, for materials and HDRIs alike. The platform says its HDRI credit shape *"would serve the consumer as it stands"*. The catalog stays the engines' lean index. One projection, never two copies.~~ **Overruled by the lead: licence and credit go in the catalog entry, beside the name and the class it already carries (RD-DS-2).** |
| ~~**Q-DS-2**~~ withdrawn | ~~**Is Character a group each article declares,** with a species-then-part taxonomy? And which of today's 30 biological articles stay generic Matter? The candidates are `Hair_Natural`, the generic hair, and any generic skin. | **Yes, declared per article,** in its recipe beside `status`. Never derived from the domain (F-DS-5). Which articles move is the lead's call, article by article. Planning it is the work of a phase, proposed below.~~ **Withdrawn 2026-10-14: there was nothing to ask** (the lead: *"I have no idea what you are asking here... what is the use case?"*). The group is one more field on the catalog entry, like the class. All 30 biological materials today are character materials, so each is marked Character. A future generic material (a generic skin pattern) is marked Matter in its own record when it is made. |
| **Q-DS-3** | **May a build that goes to other people carry the dev install** (drafts and candidates)? (BI-Q1) | The lead's call. **Pre-release, building and serving a draft is ungated.** Shipping drafts *to people* is a different act. One line from the lead decides the platform's refusal. |
| **Q-DS-4** | **Does the dev install get an identity of its own** (BI-A2), such as a content hash or the source commit plus a dirty flag, written into the served catalog or beside it? | Yes, beside the catalog, so the catalog's fields don't change. It is small, and it goes with (b) above. |
| **Q-DS-5** | **Where do the fit pictures live in a real release?** | Under `textures/fit/`, as in the dev install, and staged even though no article names them. The *Release Bundle* phase owns it. |

**The sequence, ruled and seeded 2026-10-14 (RD-DS-5):** *Matter, Character and HDRI* (`Phases/Complete/Phase15_MatterCharacterHdri.md`), then *Every Entry Says What It Is* (`Phase16_EveryEntrySaysWhatItIs.md`), then *Character Materials, Their Own Library* (`Phase18_CharacterLibrary.md`). Numbered Phase15 – 17 by the lead the same day (RD-DS-6), ahead of Scale Grids; **then The Library Service (Phase17) and Thumbnails (Phase18) were pulled ahead too, Character became Phase19 and Scale Grids Phase20 (RD-DS-7).** The Pass 4 proposal it replaces is kept below.

~~**A sequence, proposed as phases** (unnumbered, for the lead to cut; redrawn at Pass 4):~~
- **Every Entry Says What It Is.** Outcome: every material and HDRI carries its contributor, licence, name and taxonomy inside its own file. Studio, USDLiveView and the website read it from the library, and Forseti can tell who gave what. *(Was "Library Groups in the Install".)*
- **Character Materials, Their Own Library.** Outcome: a contributor can craft a set of teeth, a skin or an eye that fits the character's own part mesh, keep their name on it, and see it pictured on that part. Skin Maps and Skin Maps Beyond Colour become its first instances.
- **Release Bundle and Consumer Contract** (already seeded). It also carries Q-DS-5 and the packaged-build layout answers.

## Resolved

- **RD-DS-8 — The Library Service goes back to TBD; the others move up one: Phase17 Thumbnails, Phase18 Character Materials, Phase19 Scale Grids; skin detail stays parked** (the lead, 2026-10-14, after Hetzner had no GPU server and *"We have to rethink and stay local for now"*, RD-MP-14: *"Make this phase TBD, move the others forward, Thumbnails become Phase 17, skin detail stay parked TBD"*). Refines RD-DS-7.
  - **Read as (mine):**
    - *"skin detail"* is *Skin Maps Beyond Colour*, the fine-detail half of the skin work (wrinkles, creases, oily and dry areas). It stays unnumbered and parked.
    - Thumbnails runs on the laptop until a server exists.
    - The Library Service sits at the head of the Roadmap's `## Future`, the place it held in the lead's cut.
  - **Ids:** The Library Service keeps the `Q-P17-1…7` and `F-P17-1…7` it minted (frozen once committed). Thumbnails' `P17` ids start at 8.
- **RD-DS-7 — The Library Service and Thumbnails come before Scale Grids too, and Character after Thumbnails** (the lead, 2026-10-14: *"Actually lets pull the library service and thumbnails before Scale grids as well so we can get the entire chain establsihed recategorized, documented and working correctly before we add more materials"*; asked where Character goes, *"Move Character after Thumbnails"*). The order: **Phase15** Matter, Character and HDRI · **Phase16** Every Entry Says What It Is · **Phase17** The Library Service · **Phase18** Thumbnails · **Phase19** Character Materials, Their Own Library · **Phase20** Scale Grids. Character follows Thumbnails because its per-part pictures are built on Thumbnails' rig, which runs on the service. Refines RD-DS-6.
- **RD-DS-6 — The three are the next phases, ahead of Scale Grids** (the lead, 2026-10-14: *"Lets make these the next phases (Before the scaled grid)"*). Numbered **Phase15** *Matter, Character and HDRI*, **Phase16** *Every Entry Says What It Is* and **Phase17** *Character Materials, Their Own Library*. Scale Grids, numbered Phase15 earlier the same day with its discovery Pass 1 done, becomes **Phase18** and keeps that work. This follows the precedent of 2026-10-01, when Coloured Wear Layers took Phase10 ahead of Library Coverage.
- **RD-DS-5 — Structure first: three phases, in order** (the lead, 2026-10-14: *"Should one of the phases be to provide everything needed for the concept of Matter | Character | HDRI to be propogated through the site and platfrom (insted of just chaacter work) then we know we have the structrue sorteed out... then Every entry says what it is?"*, then *"yes record it and seed all three"*). (1) *Matter, Character and HDRI*: the three groups as the library's structure (folders, a taxonomy each, carried in one shape inside the files, the catalog and the site file), with the consumers' halves asked through the ledger. (2) *Every Entry Says What It Is*. (3) *Character Materials, Their Own Library*. All three are seeded, unnumbered.
- **RD-DS-3 — Materials work like assets: tracked, licensed, browsable by a taxonomy, with the facts inside the file and no sidecars** (the lead, 2026-10-14, verbatim: *"I want Materials to work like Assets and Compositions.... same thing... people contribute they are tracked,, the is a license it is added,,, they can browse byt a taxolongy... same same same.... do it the same... Avoid sidecars, we can put things in MTLX, and in the case of HDRI... that is totally in our control. We are doing Materal tracking for FORSETI! we want to know who contributes, which things do well, Same as assets... We dont; need to show it all the time, but we shoudl know where it came from and how its doing."*; and on export: *"we have made them mtlx so I guess we could carry the metadata in those (so no sidecar on "export" which we have not implmented yet) I don't know how we share info about HDRI on export (or if we bother) but I assume when we are in our system (App pulling from OUR created and version library) there is a solution to share metadata and taxonomy so the Studio can consume it"*). **It refines RD-DS-2:** the fields' source is the file itself (`.mtlx`, `.hdr`), and the catalog projects them from there. How it reads: Pass 4.
- **RD-DS-4 — Character materials are their own library, with their own clear ontology that people can contribute to** (the lead, 2026-10-14, verbatim: *"I do think we will have a genereic skin pattern in the future, but the characters dots do not use "matter" level materials very well.. they look like totall shit to be frank... We need to think about character materials differnly so they need to officiallbe handled in a another very clear taxonomy/ontology that people can participate in. the need to be able to craft a set of teeth that will uvmap to the predefined teeth mesh we picked, and that should keep their name so people can realize how great a teeth a particular contributor is and teeth need to not be dropped on a box for a thumbnail, they need to mapped to the teeth... same with Skin (showing half face nd hands as outlined in the doc) eyes need to be an eyeball, etc, etc), HDRIs just need to be the image."*). It extends RD-DS-1, and it **supersedes Pass 3's treatment of Character as a group field on Matter**. How it reads: F-DS-13.
- **RD-DS-2 — Licence and name reach the engines the way the name and the class already do: as fields on each catalog entry** (the lead, 2026-10-14, on Q-DS-1: *"What do you mean how does the credit reach the engines? hwo does the name readh then egnies? how does the category reach the engine? use existing solutions to simple add licnese and name.. I thought we solves this with assets and compositions... same thing."*). This applies to materials and HDRIs alike, and the group goes the same way. **What it overrides:** the July rule that kept licence and provenance out of the runtime catalog (RuntimeCatalog §What the runtime catalog does NOT carry; the `no_projection_guard` gate lane), for these fields. The Site-file route this doc recommended is dropped. **Owed:** RuntimeCatalog gains the fields, the projector and the serve tool write them, and `no_projection_guard` is narrowed to what still stays out. That is a build, offered as a quick fix.
- **RD-DS-1 — Three groups, served with their context through the whole network** (the lead, 2026-10-14, in a USDLiveView session, recorded there as that repo's own ruling; recorded here by date and content. Verbatim: *"We have 3 conecpts in the Matter Library now and it needs to seerve each one and provide the context of each one through the entier networok... the other things consumes what this library creates... those material concepts are Matter | Character | HDRI . It starts here. these have different thumbnail requriments, taxonomy, in the case of character we hav humiod today and there will be others in the future such as cananine, equene etc. and character materials will need to have a special rig for thumbnails based on if it is a skin, an eye, teeth, tounge, whatever. That said, we can KEEP biological for things like a gernic skin pattern (matter) and a generic hair material, but the comples maps that are moving to for the characters need to be in chracters.... in the end they all have basially the smae support info, whoe created it, license, a name and a strict taxonomy.... THEN,,,, Studio/Theater, Web, USDLiveView all need it, plus output stuff"*).
  - **Vocabulary:** the lead's *concept* is the library's **group** ([SiteFile](../../specs/Contract/SiteFile.md) §Groups). This doc uses *group*, so the library does not gain a second word for one idea.
  - **What it refines:** it extends RD-P13-2 (*biological is not Matter*). Generic biological materials now stay in Matter, and only the character-specific ones move to Character.
- **Recorded from the website's session the same day** (the lead's rulings there, recorded here by content): the site's browse gains a row above it, Matter, Character and HDRIs, built from the library's `groups[]`. Character's rows are **Eyes, Hair, Skin, Nails, Teeth, Mouth**. Until the library publishes those rows, the site uses the library's classes.

## Status

- **Passes captured:** 4 (2026-10-14). Pass 1 audits what is loose (F-DS-1 to F-DS-8). Pass 2 lists what each downstream tool must take in. Pass 3 orders what the library owes. Pass 4 sketches the lead's model: facts inside the file, like assets (F-DS-9 to F-DS-12), and Character as its own library (F-DS-13).
- **Ruled:** RD-DS-1, recorded from a consumer's session, and the website's Character rows. Neither was in this repo before today.
- **Merged on the way:** the platform's HDRI Pass 3 (A9, A10), at `bbbb6ab`. Its footer now lists A9 and A10 as open, for this doc's Q-DS-1.
- **Ruled 2026-10-14:** RD-DS-2 (licence and name reach the engines like the class), refined by **RD-DS-3** (like assets; the facts inside the `.mtlx` and `.hdr`; no sidecars; tracked for Forseti). **RD-DS-4:** Character is its own library. **Withdrawn:** Q-DS-2.
- **Current direction:** three phases, seeded in order (RD-DS-5): *Matter, Character and HDRI*; *Every Entry Says What It Is*; *Character Materials, Their Own Library*. The probe shows an `.hdr` carries its own facts and Blender reads it unchanged (F-DS-10).
- **Open, for the lead:** Q-DS-3 to Q-DS-5, none urgent.
- **Offered as a quick fix (doc-only, one sitting):** bring the specs and the ledger up to date, with no ruling needed:
  - the ReleaseModel layout gains `hdris/` and `thumbnails/hdris/` (F-DS-1);
  - P21's read path becomes the install's (F-DS-2);
  - dated notes on P3 and P19 from the packaged-build asks (F-DS-3);
  - new ledger rows for RD-DS-1 and the website's four asks, under the next free `M` ids (M11 and M12 as of this pass, F-DS-4, F-DS-7).
- ~~**Offered as a second quick fix (a build, after RD-DS-2):** each catalog entry, for materials and HDRIs alike, gains its licence, its credit and its group, in the dev install. The gate lane is narrowed to match, and RuntimeCatalog is updated. *(Was: "not offered", because `section` comes from the domain. Today's 30 biological materials are all character materials, so the domain gives the right answer for every one of them. The per-record override waits until a generic one is made.)*~~ **Withdrawn at Pass 4:** RD-DS-3 puts the facts in the file first, and RD-DS-4 makes Character its own library. Both are bigger than a quick fix.
- **Owed elsewhere** (not this repo's to write): USDLiveView's record of RD-DS-1 names this file.
- **Seeded 2026-10-14 (RD-DS-5):** the three phases and their Roadmap entries.
- **Graduated 2026-10-14 (the lead: *"push it, then do the doc quick fix"*):** the doc-only quick fix landed (the commit marked `✅ Quick Fix`): ReleaseModel's layout (F-DS-1, F-DS-2), the Consumers drift note, and the ledger notes on P3, P7, P19, P21 and M10, with new rows P25, P26, M11 and M12.
- **Numbered 2026-10-14 (RD-DS-6):** Phase15 – 17, ahead of Scale Grids (Phase18).
- **Re-sequenced 2026-10-14 (RD-DS-7):** Phase15 – 20 as above, so the whole chain (structure, facts, service, pictures, Character) is in place before materials are added at volume again.
- **Taken up 2026-10-14 evening, in other sessions:** Phase15 and Phase16 each have discovery Pass 1 and a Brief, and Phase15 is executing (the lead chose Character's folder, `materials/character/humanoid/<part>/`). Their phase docs are now the authority; this doc's §Resolved stays the record of the rulings they rest on.
- **Still open here, none blocking:** Q-DS-3 (may a build for others carry the dev install), Q-DS-4 (the dev install's identity), Q-DS-5 (where the fit pictures live in a real release).
- **▶ Next:** nothing from this research. It parks. That quick fix now also adds ledger rows for F-DS-12's ask: a bound material and a scene's sky carry their id, contributor and licence.
