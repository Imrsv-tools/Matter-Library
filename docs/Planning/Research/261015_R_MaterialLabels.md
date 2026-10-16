# Research — The names a person reads: how a material's label is made, where it is kept, and who sees it

**Opened:** 2026-10-15 · **Mode:** research. It gathers and commits to nothing. **Mnemonic:** `LBL` (ids `F-LBL-n`, `Q-LBL-n`, `RD-LBL-n`).
**Requested by:** the lead, 2026-10-15, verbatim: *"It just came to my attention that we are adding names to materials taht are not the filenames of the materails... how is this generated, where is this kept and how is it shared?"*
**Altitude:** an audit of what exists (Pass 1), then the choices (Pass 2). It names no file to change.
**Measured at:** `b1eed80` (2026-10-15).

---

## The current picture

- **A material's identity is its file name** (`ABS_Glossy_Clean_Base_s01_v01`), and nothing changes that.
- **Beside it, the website shows a `label`,** a name a person reads (*"Glossy ABS plastic"*). The label was **written by the agent** in Phase13 and **confirmed by the lead** on the words sheet (RD-P13-3: *"Confirmed as drafted"*).
- **It is kept in the recipe** (`tools/converters/recipes/<identity>.json`), not in the `.mtlx`.
- **Only the website sees it,** through the site file in each dev snapshot. Studio, USDLiveView and Blender show the token name.
- **The spec says the label is derived from the file name, and written by hand only "where that reads badly".** In practice every one of the 85 materials with a recipe label has a hand-written one, and none matches the derived name.

---

## Pass 1 — How it works today (audit)

- **F-LBL-1 — How it is made.**
  - `tools/releases/build_snapshot.py` takes the recipe's `label` if there is one: `"label": recipe.get("label") or label(art["display_name"])`.
  - Otherwise it derives one with `label()`: it splits the PascalCase, drops the default tokens `Natural`, `Clean` and `Base`, and uses sentence case, keeping acronyms and roman numerals. `Copper_Verdigris_Aged_Base` becomes *"Copper verdigris aged"*.
- **F-LBL-2 — Who writes it.**
  - **Phase13 step 13.2:** the agent drafted the words (label, summary, search words, origin) for every material.
  - The lead confirmed them on a words sheet (`tools/releases/words_sheet.py`), RD-P13-3.
  - **New materials:** `/matter-batch` writes `"label"` *"**only** where the name derived from the tokens reads badly"* (its SKILL.md, the words step).
- **F-LBL-3 — Where it is kept.** In each material's recipe JSON, in git, beside `summary`, `search_words` and `origin`. Measured counts:
  - 86 recipes carry `"label"`, and 104 carry `"summary"` and `"search_words"`.
  - **The `.mtlx` does not carry it.** Its `imrsv_metadata` declares master, scale, metres per tile, domain, class, contributor and licence. `working_tree.DECLARED` is `("contributor", "licence", "fits")`.
- **F-LBL-4 — Who sees it.**
  - **The website only,** through the site file published in each dev snapshot (`matterlib-0.2.0-dev.N` on GitHub).
  - **The dev catalog** that Studio and USDLiveView read carries `display_name`, the token string `ABS_Glossy_Clean_Base` (`serve_to_stage.py`; [RuntimeCatalog](../../specs/Contract/RuntimeCatalog.md) `materials[].display_name`).
  - **Blender's asset library** names each asset by its article name.
  - **So one material shows two names,** depending on where a person meets it.
- **F-LBL-5 — The spec and the practice differ.** [SiteFile](../../specs/Contract/SiteFile.md) §`label`: *"Derived from the tokens … Where that reads badly, the recipe's `label` replaces it (Phase13 13.2)."* Measured:
  - **all 85** hand-written labels on articles with the full six-token name **differ from the derived one**;
  - so the override is the rule, not the exception.
- **F-LBL-6 — Most of the difference is word order.** The derivation reads in file order, Material then Variant (*"ABS glossy"*). People read the Variant first (*"Glossy ABS"*). Measured with a Variant-first rule:
  - **35 of 85** hand labels are matched exactly;
  - the other 50 add or change words, for example *"Glossy ABS **plastic**"*, *"**Cotton** canvas"*, *"Aged copper **with** verdigris"*, *"Board**-**formed concrete"* and *"Cornea"* (dropping `Clear`);
  - **the seven scale grids** use the label to carry their size (*"Scale grid 1 m (diagnostic)"*). The size is already in the file name's scale tag, so a rule could derive it.
- **F-LBL-7 — Phase16's own principle points the other way.** Its Outcome: *"every material … says who contributed it, its licence, its name and its place in the taxonomy, from inside its own file"*. The contributor and the licence moved into the `.mtlx`. The readable name stayed in the recipe.

---

## Pass 2 — The choices (design)

- **(a) Keep it as it is.** The hand label sits in the recipe, and the website alone shows it. It costs nothing now. **Two names per material remain,** and the website and Studio disagree about what a material is called. The spec's "only where it reads badly" stays untrue (F-LBL-5).
- **(b) One derived name, everywhere, from the file name.**
  - Improve `label()`: put the Variant first, and read the scale tag for diagnostics (F-LBL-6).
  - Carry the result into the dev catalog, the site file and Blender.
  - **It can never drift from the file name**, and renaming a material renames its label. It reads a little plainer (*"Glossy ABS"*, not *"Glossy ABS plastic"*).
  - The recipe's `label` stays as the rare override the spec describes, for the few names a rule cannot read. Each override is then a visible exception.
- **(c) The confirmed labels become part of each material's own file and are shown everywhere.**
  - Move `label` into the `.mtlx`'s `imrsv_metadata` beside `contributor` and `licence`, and add it to `DECLARED`.
  - Every projection carries it: the dev catalog, the site file and Blender.
  - The lead's confirmed wording is kept, and every consumer shows the same name. **It is still a second name to maintain:** a rename must update it, and a gate should check that it is present.
  - This is a contract change: the catalog gains a field, so Studio and USDLiveView are asked to show it.

**Recommendation: (b).**
- The lead's question is whether a material should carry a name that is not its file name.
- (b) answers that the readable name *is* the file name, read nicely. One rule fixes most of today's differences (F-LBL-6), and nothing can drift.
- (c) is right if the polished wording matters more than having one source.

Either way, (a)'s split, where the website and Studio name a material differently, should end.

## Pass 3 — The platform already asked for the same thing for HDRIs (2026-10-16)

**Found while checking the platform's requests at the lead's word** (*"can you pull everything and check.. I think platfrom has a request"*).

- **F-LBL-8 — Ask A12 is open and is this doc's question for HDRIs.** `261013_R_PlatformSkyAsks.md`, Pass 5 (2026-10-14) asks for *"a name a person reads on each HDRI (`hdris[].label`, Poly Haven's title without (Pure Sky))"*, in the dev catalog and the site file. Its footer: *"The library's to rule."* Measured at `cdacf44`:
  - the site file carries an HDRI `label`, the source's own name with *(Pure Sky)* ([SiteFile](../../specs/Contract/SiteFile.md) §HDRIs);
  - **the dev catalog carries none:** `serve_to_stage.py` writes `group`, `when`, `sky`, `licence`, `contributor` and `credit`.
- **F-LBL-9 — Studio's material list reads what the dev catalog carries, by presence:** the picture, the contributor, the licence, the group, species, part and master. A `label` added there would reach Studio's picker as soon as Studio reads it. That is (b)'s and (c)'s "shown everywhere", on the platform's side.
- **F-LBL-10 — Ask A11** (the HDRI rows' grouping in what the dev install serves) **looks answered in practice.** Since Phase15, the dev catalog gives every HDRI its `group` and the catalog its `groups[]`. The sky doc's footer still calls it open; its owed library pass can say so.

**So Q-LBL-1 decides one rule for both kinds of entry.** Materials and HDRIs get a readable name from the same place, in the dev catalog and the site file alike. The HDRI version of (b) is the source's name with *(Pure Sky)* dropped, which is what the platform asked for.

## Pass 4 — What the quick fix landed (2026-10-16, RD-LBL-4)

- **F-LBL-11 — No added names anywhere the library publishes:**
  - **The site file:** `label` is gone from every material and HDRI (`tools/releases/build_snapshot.py`; the `label()` derivation and its tests are removed). A scratch build of 104 materials and 59 HDRIs carries no `label`. Every HDRI carries `credit.title`. The groups keep their own `label` (Matter, Character, HDRIs).
  - **The recipes:** the hand labels are gone from all 86 (one line each, the `"label"` key).
  - **The HDRI header:** `MATTER_NAME` is no longer stamped; the source's title is `MATTER_CREDIT_TITLE` (`tools/releases/hdris.py`). The dev catalog's HDRI `credit` gains `title`.
  - **The words sheet** (`words_sheet.py`) shows the file name with spaces.
  - **The specs:** [SiteFile](../../specs/Contract/SiteFile.md) `label` withdrawn (dated, kept) and `credit.title` added; [Identity](../../specs/Ontology/Identity.md)'s header list; [RuntimeCatalog](../../specs/Contract/RuntimeCatalog.md)'s `credit`.
  - **The ledger:** M9 (the website) and M10 (HDRIs). The sky asks' A11 and A12 are answered (its Pass 6).
  - **`/matter-batch`** stops writing `"label"`, in its own commit, staged around a sibling session's uncommitted edit to the same file.
  - **The gate:** 15 PASS, 2 SKIP, 0 FAIL, the same as the baseline before the change. The snapshot's unit tests pass.
  - **Not yet visible:** the website shows the change from the next dev snapshot, whose publish is the lead's word. The dev install's served HDRI headers are re-stamped at the next `serve_to_stage.py` run.
- **F-LBL-12 — What dropping *PureSky* touches** (`git grep`, at origin where another repo, 2026-10-16):
  - **here:** the 59 HDRI files and 77 other files;
  - **the platform's repos:** Stage 42 files (its test goldens), USDLiveView 4, the Asset Library 4 (compositions that name the default sky), the website 6 (its mirror's test and a check fixture), the platform's docs 6.

  Every one names the sky by its file name, so the rename and their updates land together.

---

## Open questions

| Id | Question | Recommendation |
|---|---|---|
| ~~Q-LBL-2~~ → RD-LBL-2 | **HDRIs too?** Is an HDRI's name its file name (`AristeaWreck_PureSky_v01`, shown as *"AristeaWreck PureSky"*), with Poly Haven's title kept only as its credit? That answers the platform's ask A12 with no label. | **Yes.** It is the same rule, applied to both kinds of entry. |
| ~~Q-LBL-3~~ → RD-LBL-3 | **The one-line summary and the search words:** keep them? They describe a material without renaming it. | **Keep.** They are not names; the website and search use them. |
| ~~Q-LBL-4~~ → RD-LBL-5 | **Drop *PureSky* from the 59 HDRI file names** (RD-LBL-2's wish)? It renames the HDRI files, and every place that names one (F-LBL-12). | **Yes, as one coordinated change:** the library's rename and its own references, plus a ledger ask for the platform to update its scenes, fixtures and goldens in the same window. That is *"Fix forward only... we have no legacy projects yet"* (Version Management's precedent). |
| Q-LBL-5 | **The cutover for RD-LBL-5.** The library's half:
- the published name drops *PureSky* (`hdris.py`'s listing gives each HDRI a published id beside its source one);
- the name grammar check (`validate_manifest`) takes `<Name>_vNN` for a published HDRI;
- [Identity](../../specs/Ontology/Identity.md) §HDRI names;
- the default setting;
- the re-served dev install;
- a snapshot.

The moment the dev install is re-served, **every scene that names `…_PureSky_v01.hdr` loses its sky** until the platform renames its references (F-LBL-12: Stage 42 files, USDLiveView 4, the Asset Library 4, the website 6, the platform's docs 6). When does the library's half land? | **Build the library's half now, and hold the re-serve and the snapshot until the platform says its rename is ready.** Ledger M10 carries the ask with the exact old → new list. Then both land the same day. |
| ~~Q-LBL-1~~ → RD-LBL-1 | **One readable name per material:** (a) as today, the website only; (b) derived from the file name by a better rule, shown everywhere; or (c) the confirmed hand labels moved into each material's file, shown everywhere? | **(b)**. One source, no drift; an override only where a rule cannot read. |

## Resolved

- **RD-LBL-1 — The file name is the name. The library makes no other name for a material, and never rearranges the file name's words.** A consumer may show the underscores as spaces, or as the breaks between the name's sections (Material · Variant · Condition · Detail). The words and their order stay the file's. (The lead, 2026-10-16, verbatim: *"I dont think we should be having name added. the name is the file name that is the description, we can remove (in studio etc) the underscoreds to the sections that define categories .... but we should not be rearanging filename words to make new names of materials... that will be SUPER confusing."*)
  - **None of (a), (b) or (c):** it rules out the hand-written labels (a, c) and the reordered derived name (b, F-LBL-6).
  - **It reverses RD-P13-3 for the labels only.** RD-P13-3, *"Confirmed as drafted"*, covered the words; this ruling withdraws the label part.
  - Closes Q-LBL-1.
  - **What it owes** (not done here):
    - the site file's `label` is withdrawn, and consumers show `display_name`. [SiteFile](../../specs/Contract/SiteFile.md) §`label` gets a dated withdrawal note;
    - the 85 hand labels leave the recipes;
    - `/matter-batch` stops writing them;
    - the website is told, through ledger M9, since it shows `label` today;
    - a dev snapshot without labels, published at the lead's word.
  - Whether it also covers HDRIs and the one-line summaries is put to the lead (Q-LBL-2, Q-LBL-3).
- **RD-LBL-2 — HDRIs follow the same rule: an HDRI's name is its file name, and Poly Haven's title is kept only as its credit. The lead would also drop *PureSky* from the names, since every HDRI is one** (the lead, 2026-10-16: *"Yes but we can also drop "PureSky" since they are all puresky and we have no plans to change that for a while"*). Closes Q-LBL-2. Dropping *PureSky* renames files other repos name, so it is held as Q-LBL-4 (F-LBL-12).
- **RD-LBL-3 — The one-line summaries and the search words stay** (the lead, 2026-10-16: *"yes keep"*). Closes Q-LBL-3.
- **RD-LBL-5 — The HDRI source files keep their names; every name the library *publishes* drops *PureSky*** (the lead, 2026-10-16, to Q-LBL-4: *"We don't need to reanme the source files... but yes - we need to rename the others that are published"*). Closes Q-LBL-4.
  - `MatterLibrary/hdris/AristeaWreck_PureSky_v01.hdr` stays as it is, as do its record and its provenance.
  - **What is published becomes `AristeaWreck_v01`:** the catalog `id`, the served file name, the header's `MATTER_ID`, the thumbnail's file name, the site file's identity, and the default.
  - **It is a contract change for every consumer that names a sky by its file name** (F-LBL-12). Its cutover is Q-LBL-5.
- **RD-LBL-6 — The next dev snapshot is published** (the lead, 2026-10-16: *"1) Yes"*). `matterlib-0.2.0-dev.9` was published 2026-10-16 at `79a8a82`: 636 assets, no `label`, 59 HDRI `credit.title`. Its site file was fetched back byte-identical.
- **RD-LBL-4 — Carry RD-LBL-1 to RD-LBL-3 out as a quick fix, and push** (the lead, 2026-10-16: *"yes please"*). Landed: Pass 4.

## Status

- **Passes captured:** 3: how it works today and the choices (2026-10-15), and the platform's matching HDRI ask (2026-10-16).
- **Found:**
  - the label is the agent's draft, confirmed by the lead (RD-P13-3);
  - it is kept in the recipe, not the `.mtlx`;
  - only the website sees it;
  - every material has a hand label, though the spec says "only where it reads badly".
- **Ruled (2026-10-16):** RD-LBL-1 to RD-LBL-4. The file name is the name, for materials and HDRIs; the summaries and search words stay; carried out as a quick fix (Pass 4).
- **Published:** `matterlib-0.2.0-dev.9` (RD-LBL-6). The website shows the file names from its next mirror run.
- **Open:** Q-LBL-5, the cutover for dropping *PureSky* from the published HDRI names.
- **Next step:**
  - the lead answers Q-LBL-5;
  - then the library's half of RD-LBL-5 as a quick fix, and the ledger ask to the platform.
