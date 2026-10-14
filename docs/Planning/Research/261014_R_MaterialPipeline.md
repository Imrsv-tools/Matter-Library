# Research — The material pipeline, end to end: from a wanted material to something consumers take, and the screens around it

**Opened:** 2026-10-14 · **Mode:** research. It gathers and commits to nothing. **Mnemonic:** `MP` (ids `F-MP-n`, `Q-MP-n`, `RD-MP-n`).
**Requested by:** the lead, 2026-10-14, verbatim: *"not only for human skin but for how we want to do thumbnails for all materials... we should use the best rendering view we have (maybe the UE one)... showing how "hair" materials look, or how "Skin" will look Should be mapped on mesh that makes more sence to judge it. Hand and part of face I had reccomended for skin but open to it... so when a new material is added it gets checked, vlaidated, all the metadata added, thumbnails generated and prepped so it cn be consumed. Then we need to sort out the selection and library managment front end so peeps can manage versions etc... So lets start thinking about the ful flow (even stuff I might have missed?"*
**Altitude:** a **design landscape** of the whole flow: what each stage must do, and what it should feel like for the maintainer and for consumers. **Pass 1 is the one audit pass** (what runs today, measured). Every other pass is design. It names no file or route to build.
**Measured at:** `42e26fa` (2026-10-14).

**Extends, does not replace:**
- `260926_R_BigPicture_NimbleSetup.md`: its Pass 5 and Pass 10 sketched this flow before the rig existed;
- `261014_R_TheLibrarysSite.md` (RD-WS-1 to RD-WS-4);
- `Phase11_LibraryCoverage.md` (the build loop);
- `PhaseTBD_VersionManagement.md`, `PhaseTBD_ReleaseBundleConsumerContract.md`;
- the Roadmap entries *See the Library*, *Author a Material End to End* (the Matter Manager), *Blender from a Release* and *Contribution Path*.

**An input from outside this repo:** a guidance document on publishing human skin materials, supplied by the lead (2026-10-14) and kept in the platform's private web planning. It is read as **context, not authority** (Pass 4), and is not copied here.

---

## The current picture

- **The first half of the flow runs and is proven:** want → build → check → rig → refine. The wish list holds 209 rows, and `/matter-batch` builds and rigs them.
- **The review is the bottleneck.** Thirty rows have been built since 2026-10-02 and **none has been kept**. Phase11 is paused before its end review.
- **Everything after the review is manual or missing:**
  - text for people (a label and a summary);
  - thumbnails;
  - rebuilding the Blender library;
  - picking what goes in a release;
  - publishing it;
  - telling consumers.
- **Thumbnails are a different product from the rig's pictures.** The rig is lit the same way in every tool, so it can compare them: no shadows, no bounce light, no tone curve. A thumbnail should show the material at its best, on a subject that suits it.
- **Today the best renderer for a thumbnail is Blender's Cycles, not Unreal** (Pass 2, Q-MP-1). The Unreal runtime is built with ray tracing and global illumination off, and its solid see-through master is known to be wrong (M6).

---

## Pass 1 — The flow as it runs today (audit, measured 2026-10-14)

**Examined:**
- `.claude/skills/matter-batch/SKILL.md` and the `/matter-generate` steps it reuses;
- `Phase11_LibraryCoverage.md` (Brief, §Resume);
- `library/wishlist.yaml` (209 rows: 35 built, 174 queued, none kept);
- all 95 recipes (statuses, source kinds);
- `tools/parity/JOB_FORMAT.md`; `tools/preview_generators/README.md`; `tools/releases/`; `tools/generators/gen_asset_library.py`;
- `unreal/RUNTIME.json` and `unreal/MatterRuntime/Config/DefaultEngine.ini`;
- `PlatformDependencies.md` M8;
- the Glossary.

| Stage | What does it today | Who acts | State |
|---|---|---|---|
| **Want** | a row in `library/wishlist.yaml` | anyone | runs |
| **Build** | `/matter-generate` §1–5: a recipe → `assemble_mtlx.py` → `.mtlx`, textures with their provenance | agent | runs |
| **Check** | `validate_recipe.py` per row; `run_all.py` (the structural gate) per batch | tool | runs |
| **Rig** | `rig.py --sweep`: Storm, Blender (Cycles) and Unreal, every Creator port, a scorecard and a verdict | tool, agent reads | runs |
| **Refine** | fix what is fixable, re-rig, at most 3 runs (RD-P11-4) | agent | runs; 11.4 still owed over the proving set |
| **Review** | `review_pages.py` builds one image per batch; the maintainer says keep or redo; `wishlist.py keep/redo` records it and writes the recipe's `status` | maintainer | built; **never run** (30 built, 0 kept) |
| **Reach the dev consumers** | `serve_to_stage.py` (USDLiveView, Studio); `gen_asset_library.py` (Blender) | agent, by hand | runs; **the tracked Blender library is six articles behind the tree** (M8) |
| **Release** | the lockfile by hand → `project_runtime_catalog.py` → stage → freeze → promote | maintainer | built; the 12-article pilot only |
| **Publish** | a release bundle on GitHub Releases, plus a file for the site and its pictures | — | *(planned)*: RD-WS-2, RD-WS-4 |
| **Consume** | the site, the Blender extension, the Unreal masters, IMRSV's mirror | consumers | *(planned)* |
| **Maintain** | carry forward, deprecate, retire, `vNN+1` | maintainer | *(planned)*: *Version Management* |

- **F-MP-1 — The build half is automated and proven, and it is not where the time goes.** The proving set built 30 rows in a day (Phase11, 2026-10-02).
- **F-MP-2 — The review is the bottleneck, and the flow downstream depends on it.** Nothing is kept, so nothing is ready to describe, show or release. Phase11's end review (RD-P11-3) is owed first. Without it, a thumbnail pipeline has no kept articles to run on.
- **F-MP-3 — An article's facts live in six places:**
  1. the recipe (status, sources, the authoring note);
  2. the `.mtlx`'s `imrsv_metadata` (master, scale, metres per tile, domain, class);
  3. the wish list (state, batch, the maintainer's note);
  4. the batch summary (critique, verdict, review words);
  5. the scorecard (per-port verdict);
  6. the lockfile (texture provenance and evidence).

  A consumable article needs them **projected**, not re-typed (RD-WS-4).
- **F-MP-4 — Nothing says when a downstream product has gone stale.** When a master, the Unreal runtime or the scene changes, every picture made with it is out of date. `unreal-runtime-v4` changed the pictures of every coated article (27) and every light (M8). So does the Blender library. Today a person notices, or does not.
- **F-MP-5 — The source kinds (recipes, measured):**

  | Source kind | Recipes using it |
  |---|---|
  | judgement | 76 |
  | Physically Based | 35 |
  | procedural | 27 |
  | ambientCG | 12 |

  **26 recipes have only a judgement**, and **12 have no `sources` at all** (the pilot's articles, whose provenance is in the lockfile). No recipe records an image-generation model, and none records that an agent drafted it, except in free-text notes.

## Pass 2 — Thumbnails: what "the best render" means here

- **F-MP-6 — The rig's pictures are diagnostics by design, not thumbnails.** JOB_FORMAT §Matched lighting: *"no shadows, no bounce light and no reflections of other objects, because Storm can do none of the three"*, with a plain sRGB encode and no tone curve. Blender and Unreal hold themselves to the same, so the columns compare the material and not the lighting. That is right for parity and wrong for a picture meant to sell a material. **A thumbnail is a separate render:**
  - full lighting: shadows, bounce light, an HDRI;
  - a fixed tone curve and exposure;
  - framing that suits the material.

  The rig's renders stay what they are: the evidence on the page (WS-F6).
- **F-MP-7 — "The best renderer" is, today, Blender's Cycles.** This collides with the lead's suggestion, *"maybe the UE one"*, which is not a ruling, so it is a question (Q-MP-1). The evidence:
  - **Unreal, as built:** `unreal-runtime-v4` is built with `r.RayTracing=False` and `r.DynamicGlobalIlluminationMethod=0` (its `DefaultEngine.ini`, for matched lighting). A showcase render needs a new runtime build on the Unreal machine, with Lumen or ray tracing on. Whether Unreal's path tracer works in a packaged Linux build is **unverified**.
  - **Unreal, by master:** the library's solid see-through master bends nothing, and a solid's see-through colour shows faintly (PlatformDependencies M6, open). Diamonds, sapphires and lead crystal would be its weakest pictures.
  - **Cycles:** a path tracer, with real refraction, subsurface and bounce light. It runs on this machine with a CPU fallback, and already renders the library's faithful Blender masters for the rig.
  - **Storm:** shows see-through matter as transparency, not refraction (Phase05).
- **F-MP-8 — A hero picture per article, labelled with its renderer, and the other engines on the page.** The LCD ruling makes an engine's own best picture legitimate (*"each master makes the article look as good as its engine can"*, `_Architecture.md` §Design principles). So:
  - **one hero thumbnail** per article, rendered by the best renderer for its master, which is Cycles today;
  - the label says which renderer made it;
  - the page also shows **the rig's three columns** as the evidence.

  An Unreal hero becomes a candidate once a showcase build exists. It also matters for another reason: it is what IMRSV's users will see.
- **F-MP-9 — The subject is chosen by Class (sometimes by master), sized by the scale tag.** The lead's rule: *"Skin will look should be mapped on mesh that makes more sense to judge it"*. A first table to argue with (Q-MP-2):

  | Class, or master | Subject | Why |
  |---|---|---|
  | most opaque matter: metal, plastic, polymer, coating, ceramic, wood, mineral | the rig's sphere and rounded cube, re-lit | the highlight reads roughness; the edges read wear and relief |
  | ground matter: soil, sand, terrain-scale stone (`s1`, `s10`) | a slab at real size, low camera | it is seen underfoot; one tile is 1 m or more |
  | cementitious; stone at `s01` | a block or a wall section | it is seen as a built surface |
  | glass (TranslucentThin) | a pane or a vessel, with a patterned backdrop | see-through matter needs something behind it |
  | gem, crystal (TranslucentThick) | a cut stone or a thick block, side-lit, with a backdrop | refraction is the point |
  | textile, leather | a draped cloth, or a garment on the character | how it folds and catches light |
  | **skin** (tissue) | **the character's hand, and part of the face** (the lead's suggestion; the rig's `hand` and `face` views) | judged where people judge skin |
  | lips · eyes · teeth, gums, tongue | the character's mouth or eye, close up (the rig's `mouth` view) | the substance in its place |
  | **hair** (keratin) | **a head with a hairstyle** (the character's `bob02` cards) | hair is judged as hair, not on a ball |
  | nails | the character's hand | — |
  | emissive | a tube or panel, in a dark view and a lit view (as the rig's `dim` view) | a light is judged by its glow |
  | vegetation (leaf) | leaf cards | a leaf is a cut-out |
  | Masked lace | over a surface, with a backdrop | the holes are the point |
  | utility (grey card, UV grid) | a flat card | it is a calibration tool, not a material to admire |

  **The character is the rig's own:** MakeHuman's CC0 adult body, **clothed** (shirt, trousers, shoes, JOB_FORMAT §The character job), already split into one part per substance. Its views today are whole body, face, hand, mouth, waist and feet.
- **F-MP-10 — The showcase scene is versioned and evolves.** The lead: *"something we could evolve over time"*. Every thumbnail records what made it:
  - the article's hash;
  - the masters version;
  - the renderer and its version;
  - the scene version.

  When any of the four changes, the thumbnail is stale (F-MP-4). Fixed seeds and sample counts keep a re-render byte-stable when nothing changed, so a re-run does not churn.
- **F-MP-11 — A few pictures per article, not one:**
  - a **card** (square, for grids);
  - a **close-up** at real scale, so the texture reads;
  - a **context** view (the subject in its setting);
  - a dark view for lights;
  - optionally **looks** (WS-F7): the same article at a Creator setting, such as glass set to amber or dust at full.

  Each is a master PNG plus web formats, with alt text taken from the label (Pass 3).
- **F-MP-12 — Where the pictures live.**
  - **Never in git.** Textures already strain LFS; pictures would be worse.
  - **Before a release:** a folder on this machine that is not tracked, served to the site's staging (RD-WS-3).
  - **At a release:** published as release assets beside the bundle (RD-WS-4).

  Q-MP-7.

## Pass 3 — Metadata: what a consumable article carries, in three layers

- **F-MP-13 — Three layers, and the library already has their homes.** The skin guidance (Pass 4) separates *technical*, *presentation* and *compliance* information. That matches RD-WS-4's split exactly:

  | Layer | Answers | Home |
  |---|---|---|
  | **technical** | what the article is | the runtime catalog |
  | **presentation** | what a person sees | the site file: label, summary, tags and aliases, Creator controls, wear layers, thumbnails, parity verdict |
  | **compliance** | where it came from and who said yes | provenance and evidence, licence, origin, approver, the review decision |

- **F-MP-14 — What is derivable, and what someone must write:**
  - **Derivable** from the six records (F-MP-3): identity, Class, master, scale, Creator controls, layers, parity, sources, licence.
  - **Must be written:** a **label** (derivable, with an override; WS-F4), a **summary**, **tags and aliases** (so "steel" finds `StainlessSteel_*`, and "brick" finds terracotta), and the **origin** (procedural · scan · measured · agent-drafted). The approver is recorded by the keep itself.
  - **Proposal:** the agent writes the words at build time, and **the review confirms them with the picture**. The maintainer judges what the public will read in the same sitting as what it will see.
- **F-MP-15 — A completeness check before a release, not before a draft.** A gate lane that refuses a release whose articles lack a label, summary, origin or thumbnail is a ruling (Phase11's Brief: *"A new gate or `run_all.py` lane … a lead ruling"*). It belongs at the release, so it never slows the build loop (the lesson of `260926_R_BigPicture_NimbleSetup.md` Pass 2: release checks held up a content fix).

## Pass 4 — The skin guidance, read against the library

**Examined:** the lead-supplied guidance (six pages, *"Working guidance v1.0, October 2026"*); `Ontology/Taxonomy.md` (biological); the fit set on disk; the skin recipes; the rig's character views and `.gitignore`.

**Its subject is mostly not ours.** It is written for a repository that publishes **anatomically complete, full-body adult skin atlases**. The library ruled the opposite at Phase07. Taxonomy.md, verbatim: *"A body is not matter, just as a wall is not … Anything bound to one mesh, such as a region mask, a painted skin atlas or a hair card's cut-out, stays outside the taxonomy (research `260927_R_CharacterMaterials_MPFB2.md`, CM2)."* The skin articles are a Physically Based tone plus a procedural pore pattern at a 1 cm tile (`Skin_FitzpatrickIII`: sources Physically Based *Skin III*, `gen_skin_pores.py` and judgements). They contain no atlas, no photograph and no likeness.

**Where it collides with a ruling, listed before anything is adopted:**
- **CC0 or CC BY:** the guidance offers both. The library is **CC0 only** (R13): *"Contributions are CC0-1.0 and must be CC0-dedicable"* (`_Architecture.md` §Governance). The library keeps CC0.
- **AI-generated work:** the guidance warns that *"entirely AI-generated outputs may have uncertain copyright status"*. BP8: *"Licensing and provenance do not block the seed library (lead, 2026-09-26: "we are trying to prove a concept")."* These do not conflict while the library is a seed. **They meet at the first release**, where the shipped-pixel rule (R13) applies. Hence F-MP-14's origin field: record it now, decide at the release.

**What it does give us:**
- **F-MP-16 — Where an atlas could get in: the fit set.** `MatterLibrary/textures/fit/makehuman/` holds hair and eyes only (measured). A body skin picture would be a fit picture. A one-line rule closes it (Q-MP-6): **the library holds no body skin atlas.** If that ever changes, it takes its own review track, with adult-only disclosure.
- **F-MP-17 — Pictures of people are limited to non-intimate views.** The guidance: *"Public thumbnails should demonstrate material quality using faces, hands, forearms, and neutral macro skin close-ups … Do not use nude full-body or sexualized renders"*. It agrees with the lead's hand-and-face suggestion. Proposal: the thumbnails take **only a whitelist of character views** (face, hand, mouth, eye); never the whole body, waist or feet; and always the clothed character. The rig's own renders are not published (`library/parity/` is ignored by git, measured).
- **F-MP-18 — Origin and the person who approved it** (F-MP-14). The guidance: *"Record whether assets were procedural, manually authored, or AI-assisted … and who approved release."*
- **F-MP-19 — No photographs of people as a source** unless rights and consent are documented, and excluded by default. True today; worth writing down.
- **F-MP-20 — A way to report and correct** a published article (rights, a wrong label, a fault). It belongs on the site, which is the platform's (RD-WS-1), and points back at this repo's issues.

## Pass 5 — The flow, end to end (a design sketch, not a plan)

Each stage says what it produces, and how it knows to run again.

| Stage | Produces | Who | Runs again when |
|---|---|---|---|
| 1. Want | a wish-list row | anyone | — |
| 2. Build | recipe, `.mtlx`, textures, provenance | agent | a redo note |
| 3. Check | the gate's verdict | tool | any file changes |
| 4. Rig | sheet, scorecard, per-port verdict | tool → agent | the article, a master, a runtime or the scene changes |
| 5. **Describe** *(new)* | label, summary, tags, origin | agent | the article changes; the maintainer edits |
| 6. **Show** *(new)* | hero thumbnail and views (Pass 2) | tool | the article, a master, the renderer or the showcase scene changes (F-MP-10) |
| 7. **Review** | keep or redo, with the words and the pictures confirmed | **maintainer** | a rebuilt row |
| 8. Reach the dev consumers | the dev catalog; the **Blender library rebuilt automatically after a keep** | tool | a keep |
| 9. **Cut a release** *(new as a tool)* | the lockfile from the kept articles; release notes from the diff; semver from the diff | **maintainer** | the maintainer decides |
| 10. Freeze and approve | freeze; approval | tool; **maintainer** | a cut |
| 11. Publish *(planned)* | the bundle on GitHub Releases, plus the site file and the pictures (RD-WS-2, -4) | tool | an approval |
| 12. Consume | the site (the platform's), the Blender extension, the Unreal masters, IMRSV's mirror | consumers | a publish |
| 13. Maintain | deprecate, retire, supersede (`vNN+1` after release) | **maintainer** | *Version Management* |

- **F-MP-21 — Thumbnails before the review, not after.** The maintainer then approves what the public will see, in the sitting where they judge the material (Q-MP-3). It costs renders for rows that get a redo; the rig already pays that cost.
- **F-MP-22 — The maintainer acts at three points only:** review, cut and approve. Everything else is a tool or the agent. That is BigPicture's *"the lead looks and judges"*, carried to the end of the flow.
- **F-MP-23 — Staleness is the flow's other trigger.** Stages 4, 6 and 8 re-run when what made them changes, not only when the article does (F-MP-4, F-MP-10). A short list of stale items is one of the things a management screen shows (Pass 6).

## Pass 6 — "The selection and library management front end": two audiences

The lead: *"so peeps can manage versions etc."* "Peeps" can be read two ways, and the two are different products (Q-MP-4).

- **F-MP-24 — (a) The maintainer's console, for curating the library:**
  - **the review queue:** sheet, thumbnail and words side by side, keep or redo, with a note;
  - **the release composer:** pick kept articles; see the difference from the last release; a suggested semver; deprecate and retire;
  - **the wish list:** add and reorder;
  - **what is stale** (F-MP-23).

  **Where it could live:**
  - **A local page served from this repo.** Git stays the source, and the page writes through the existing tools (`wishlist.py`, the lockfile). It is the natural next step after `review_pages.py`. **Recommended first.**
  - **GitHub itself:** pull requests as the interface.
  - **The platform's web back office**, writing to git.

  The first keeps RD-WS-1's condition that the library owns every fact.
- **F-MP-25 — (b) The Creator's side, for choosing and keeping materials up to date:**
  - pick a release and update to the next;
  - see what changed;
  - take a subset for a project;
  - know which compositions need which release;
  - favourites.

  **Where it lives:** in each consumer. The Blender extension's own updates (*Blender from a Release*), Studio (the platform's; `ReleaseConflict`), and the site (RD-WS). The *Matter Manager* seed (*"import · promotion · subset/export · path remap"*, `260923_R_StandaloneSetup.md` seed 7) spans both audiences, and is worth splitting along this line.

## Pass 7 — What might be missed

- **F-MP-26 — The review backlog comes first.** 30 rows have been built and none kept (F-MP-2). More pipeline will not move faster than the review does.
- **F-MP-27 — The pilot's 12 approved articles never went through the loop's review.** The first real release must re-judge them or carry them as they are.
- **F-MP-28 — Contributions from outside run code on our machine.** A contributed recipe is JSON. A contributed **generator script** is code, and the rig would run it on the GPU box (*Contribution Path*). This needs a sandbox or a maintainer's read before a run.
- **F-MP-29 — The compressed textures cannot be built here.** The pinned encoder is missing on this box (release-bundle F4). A release with `.dds` waits on it.
- **F-MP-30 — Bundle size against GitHub's per-file limit** (under 2 GiB, RD-WS-2). At 200 articles the bundle may need splitting, by domain or by role (PNG and DDS).
- **F-MP-31 — Retiring an article must not break old compositions.** The old release stays installable, and the composition's pin finds it. The consumer then needs to tell the Creator: the open experience questions in `Experience_MatterLibrary.md`.
- **F-MP-32 — Compute budget.** The rig takes 4–10 minutes per article. A Cycles showcase of about four views per article, across 200 articles, is hours of GPU time, and it competes with the rig. Measure it on a probe before choosing sample counts.
- **F-MP-33 — Accessibility:** alt text on every picture, and a text label beside every coloured status badge. The site draws them (RD-WS-1), but the alt text and labels are the library's words (Pass 3).
- **F-MP-34 — One word for the published picture.** The Catalog spec says *thumbnails*. RD-WS-4 says *a preview set*. `tools/preview_generators/` means the review render. Two names for one thing is a bug (Q-MP-5).

---

## Proposed phases (unnumbered; the order and the numbers are the lead's)

- **Library Coverage's end review** (Phase11, 11.4 and the review). It is not new; it unblocks everything after stage 7.
- **Thumbnails: every kept material shown at its best.**
  - Outcome: each kept material has a picture that shows it at its best, on a subject that suits it, ready for the site.
  - Content: Pass 2 and F-MP-17.
  - It is the library's half of *See the Library*, and could be that entry's first phase.
- **Describe at build, confirm at review:** Pass 3's words written by the agent and confirmed by the maintainer. Small; possibly a change to the batch skill rather than a phase.
- **The maintainer's console:** the review queue, the release composer and the stale list (F-MP-24). It overlaps *Version Management* and the Matter Manager.
- **Unchanged:** *Release Bundle*, *Version Management*, *Blender from a Release*, *Contribution Path*.

**One sitting, now, as a probe:** render a showcase thumbnail in Cycles for three articles: `Oak_Natural` on the sphere and cube, `Glass_Clear` with a backdrop, and `Skin_FitzpatrickIII` on the clothed character's hand and face. Lit fully, toned, one view each. **Cost, roughly:** a few minutes of GPU per picture, in a scratch folder, building nothing in the repo. It would answer Q-MP-1 and Q-MP-2 by eye rather than by argument.

## Pass 8 — The lead's first answers (2026-10-14)

The lead, verbatim: *"CC by is indeed OK .. this is inline with our asset library and composition sharing approach in imrsv labs. What do you mean by hold not body skin map? 1) After clarity on bodyskin map - I agree with your reccomdation 2) Ahh yeah.. I mean the IMRSV team managing what materials are going into what librarvy versions... I feel like this should be a front that we can use to view and evluate them, update versions, keep whatever provanence might exist etc"*.

**Read as:**
- The licence ruling (RD-MP-1) is taken as given.
- Item 1 agrees to the recommendations of Q-MP-1, -2, -3, -5 and -7. **Q-MP-6 is held** until the lead has the clarity he asked for.
- Item 2 answers Q-MP-4.
- Q-MP-8 was not answered and stays open.

- **F-MP-35 — What "the library holds no body skin map" means.** Put to the lead in chat, recorded here:
  - **What the library's skin is now:** a **tileable material**. A tone plus pores at a 1 cm tile, so it works on any mesh.
  - **What a body skin map is:** one painted picture laid over **one** body's UV layout. Face features, moles, nipples and genitals sit where that body has them, so it fits that body's mesh only.
  - **Where one could land:** the library already holds per-mesh pictures for MakeHuman's hair and eyes (the fit set). A full-body skin picture would be the next one there.
  - **The proposed rule:** never add one. Skin stays a material, and regional variety comes from separate substances (lips and nails as their own articles, PlatformDependencies P15) and from the Creator's tint.
  - **Why:**
    - Phase07's ruling (*"a painted skin atlas … stays outside the taxonomy"*, CM2);
    - a full-body map carries intimate anatomy, which brings in the guidance's whole adult-only review track and every host's content policy, including this public GitHub repo's;
    - it ties skin to one mesh.
  - **What it costs:** painted realism, such as freckles placed on a face, or blush. Where a consumer wants that, the body's own map is the character pipeline's, which is the platform's.
- **F-MP-36 — The licence change touches more than a word.** Each item is owed downstream and none is done here:
  - each article carries its own licence; the recipe, lockfile and catalog say which;
  - the release carries an **attribution list** for its CC BY articles;
  - consumers show credit (the site, the Blender library, Studio);
  - the manifest validator's CC0-only provenance gate widens;
  - `CONTRIBUTING.md` and `LICENSE-CONTENT.md` offer the choice;
  - `_Architecture.md` §Governance, the Glossary's *Matter Library* line (*"a community, CC0 … library"*) and `Experience_MatterLibrary.md` change their wording.

  The site research's *"the licence: CC0-1.0 throughout"* (WS-F3) is no longer true; it gets an in-place note.
- **F-MP-37 — The console is for the IMRSV team, and it is a front end the team can reach.** Its job, in the lead's words: *"view and evaluate them, update versions, keep whatever provenance might exist"*. That is F-MP-24's maintainer's console, used by more than one person. **Where it runs is now the open question (Q-MP-9).** "A local page" (the Q-MP-4 recommendation) assumed one maintainer at this machine.

## Pass 9 — The lead's second answers: skin maps, a permanent home, CC0 by default (2026-10-14)

**The lead, verbatim:**
1. *"BodySKinMaps - Sadly - I don't think this skintype per area of a mesh apprach is gong to yeild good results... Right now... it is pretty terrible in fact (the line between lips and face and no variation)... I think we need to plan to move to SkinMaps … feel free to seed a reseerach on this topic"*;
2. *"So... that "library machine" is currently this little laptop... this is not setup on a system... now - I am totalyl open to operationalizing MatterLibrary and getting it on a serviced instance that do everything... but we would need to build that and set that up.... Could be indpendent, or we could add that to imrsv web... thoughts?"*;
3. *"CC0 is fine"*;
4. *"What is needed from the review? I feel like it must have passed if we have moved on"*;
5. *"lets pause on that since again --- this is on my laptop right now so we might want to consdier if this moved to something more perminante with the this as one of the firsts tests"*.

- **F-MP-38 — Q-MP-6 is answered the other way.** The "no body skin map" rule is **not** taken. The lead's direction is to plan a move to skin maps, researched in **`261014_R_SkinMaps.md`** (seeded today). That doc quotes the rulings it reopens (MAP-RD2, MAP-RD5). It also finds that the colour half needs no contract change: `base_color_map` on Subsurface already exists (F-SKM-3).
- **F-MP-39 — The review has not happened. "Moved on" was a re-sequencing, not a pass.**
  - The lead paused Phase11 after 11.3 on 2026-10-02, and the work moved to other phases (Phase12, the platform's asks, the HDRIs).
  - Measured: every batch summary's **Review** line reads `—` (`library/batches/*.md`); the wish list holds 35 rows `built` and **0 `kept`**; the 30 proving rows are `draft`.
  - **What the review needs** (Phase11 §The end review): the lead opens each batch's review page (eight batches, one image each) and says keep or redo per row, about 35 rows. The agent records each verdict, and a keep writes the article's status (`approved` when all three tools moved alike, `candidate` otherwise). Phase11 also planned **11.4, a refine pass**, before it.
  - **Three ways to do it:**
    - **(a)** The end review as planned, in one sitting.
    - **(b)** Keep by verdict: every row whose three tools moved alike is kept at once, and the lead looks only at the flagged rows.
    - **(c)** Make the review the **first real job of the team's console** on the library's permanent machine (Q-MP-11).

    Q-MP-8, reframed.
- **F-MP-40 — The library's machine is a laptop, and the flow needs a permanent one.** What the service must run:

  | Job | What it needs |
  |---|---|
  | **GPU work:** the rig in Storm, Blender and Unreal; Cycles thumbnails | a GPU with Vulkan for the Unreal runtime; Blender 5.1+; the OpenUSD and MaterialX toolchain (a 30–50 minute from-source build); the pinned Unreal runtime |
  | **Agent work** | Claude Code sessions running `/matter-batch` and `/matter-generate` against a clone |
  | **The team's console** (RD-MP-7) | a light web app |
  | **The dev catalog** (`serve_to_stage.py`) and the thumbnail folder (RD-MP-6) | serving to staging (RD-WS-3) |
  | **Git** | commits to this public repo, and pushes on the maintainer's word; approvals stay the maintainer's (`promote_release.py`) |
  | **Storage** | renders, thumbnails and staged releases, none of them in git; the compressed-texture encoder (F-MP-29) |

- **F-MP-41 — The platform's web server cannot be that machine as it stands.** Its own docs describe a small, shared server with no GPU. "Adding it to the platform's web side" can mean only two things:
  - the **console** in the platform's back office;
  - a **GPU worker** elsewhere, which the platform's stack calls.

  The heavy half needs its own GPU host either way.
- **F-MP-42 — The shape that keeps both repos' rulings: an independent library service, run by IMRSV.**
  - **Its code lives in this repo:** containers for Blender, the USD toolchain, the Unreal runtime, the console and the agent's workspace. Anyone who forks the library can stand one up. That is RD-WS-1's condition 3, *"the library survives without IMRSV"*.
  - **IMRSV runs it:** its machine, its accounts. The team may later sign in with their IMRSV accounts, since one account crosses domains on the platform's side.
  - **The platform's site and mirror consume what it publishes:** the dev catalog and the thumbnails before a release, the bundle at a release. They never reach into it.
  - **Where it runs is a cost and ops question:** a cloud GPU instance started only while batches and thumbnails run; a dedicated machine (the Linux GPU machine the Unreal work used, BigPicture BP6, if it is free); or a GPU worker on the platform's infrastructure. Q-MP-11.
  - **Its first tests,** as the lead said: the thumbnail probe and the review (F-MP-39 (c)).
- **F-MP-43 — The thumbnail probe is paused** until the permanent machine exists, and becomes one of its first tests (RD-MP-10).

## Pass 10 — Phase11's remainder, and making material-making a process rather than a phase (2026-10-14)

**The lead, verbatim:** *"OHHHH... indeed phase 11 was taking a LONG time, how much more is left for it? we may want to break this up into phases differently or even have a material geneartion process different that the pahses for building the infra and tooling for the matter library... I like your reccomendation for the library home... I guess that is ALSO a new pahse to seed"*.

- **F-MP-44 — What is left of Phase11** (its Step list, measured against the wish list, 2026-10-14):

  | Step | State |
  |---|---|
  | 11.1, 11.2, 11.3 | **Done:** the list, the helper, the batch skill, 26 built rows and 4 re-judges, 7 new wear layers. |
  | **11.4, the refine pass** | Owed. All 30 proving rows re-read and fixed, up to 3 rig runs each. At the measured 7–22 minutes of rig time per row, that is **about 4 to 11 hours of the laptop's GPU**. |
  | **The end review** | Owed: about 35 rows, one picture per batch. |
  | **Close** | The Blender library rebuilt once, docs conformed. |

  **The 174 queued rows were never Phase11's steps.** Its Brief puts them under *"After the proof (the loop's work, not a step of this phase)"*. Phase11's Outcome already says the library fills *"without a phase per batch"*. So the remainder is small in steps but heavy in rig time, and the long tail was always meant to be a process.
- **F-MP-45 — The lead's split already matches the design; it only needs saying out loud:**
  - **Tooling phases:** the library service, thumbnails, the console, the release bundle, version management, skin maps. Each is built once.
  - **Material-making:** a **standing process**, the loop (`/matter-batch` over `library/wishlist.yaml`). It runs batches whenever there is a machine and time, and records itself in its batch summaries. **It is never a phase.**
- **F-MP-46 — The quickest honest close for Phase11:**
  1. Review by verdict (Q-MP-8 (b)): rows whose three tools moved alike are kept at once; the lead looks at the flagged ones.
  2. **Move 11.4's refine pass into the loop** as ordinary redo rows, each carrying its fault, so it runs as batches on the permanent machine rather than as a phase step on the laptop.
  3. Close: rebuild the Blender library, conform the docs.

  That closes the proof without spending a day of the laptop's GPU. It is the lead's call, and it is made in Phase11's doc, not here.

## Resolved

- **RD-MP-1 — CC BY 4.0 is allowed beside CC0-1.0** (the lead, 2026-10-14: *"CC by is indeed OK .. this is inline with our asset library and composition sharing approach in imrsv labs"*). **It amends R13** (`260923_R_StandaloneSetup.md`, in-place note there), which said *"Content licence: CC0-1.0 … every third-party input must itself be CC0 … CC-BY … sources do not"*. **Read as** the Asset Library's shape: **each article carries one licence, CC0-1.0 or CC BY 4.0**. A CC BY input makes its article CC BY. The default is Q-MP-10. Consequences: F-MP-36.
- **RD-MP-2 — The hero thumbnail is rendered by Cycles today, and labelled with its renderer.** An Unreal hero follows once a showcase build of the runtime exists and the solid see-through master is repaired (M6). (Q-MP-1.)
- **RD-MP-3 — F-MP-9's subject-per-Class table is the starting set**, evolved with the showcase scene's version: skin on the clothed character's hand and part of the face; hair on a head. (Q-MP-2.)
- **RD-MP-4 — Thumbnails are made before the review**, so the maintainer approves what the public will see. (Q-MP-3.)
- **RD-MP-5 — "Thumbnail" is the word for the published pictures; "preview" stays the review render.** RD-WS-4's *"a standard preview set"* means the thumbnails (in-place note there). The derived specs that say "preview set" (Catalog §Thumbnails's note, RuntimeCatalog's note, Consumers, PlatformDependencies M9) are conformed when a phase next touches them. (Q-MP-5.)
- **RD-MP-6 — Thumbnails never go in git or LFS.** Before a release they sit in a folder on this machine that git ignores, served to the site's staging; at a release they are release assets. (Q-MP-7.)
- **RD-MP-7 — The management front end is for the IMRSV team: to view and evaluate materials, decide what goes into which library version, and keep their provenance.** The Creator's side lives in each consumer. (Q-MP-4; where the console runs is Q-MP-9.)
- **RD-MP-8 — A new article is CC0-1.0 by default** (the lead, 2026-10-14: *"CC0 is fine"*). CC BY 4.0 is chosen by a contributor, or forced by a CC BY input, and recorded per article (RD-MP-1). (Q-MP-10.)
- **RD-MP-9 — The "no body skin map" rule is not taken. The direction is to plan a move to skin maps** (the lead, 2026-10-14: *"I think we need to plan to move to SkinMaps"*), researched in `261014_R_SkinMaps.md`. ~~The rulings it reopens are quoted there (MAP-RD2, MAP-RD5).~~ *(Corrected the same day: it reopens neither MAP-RD2 nor CM2. MAP-RD2 locks the mesh, not the pictures, so a skin map for the approved mesh is allowed, `261014_R_SkinMaps.md` RD-SKM-1. Only MAP-RD5's "skin stays general" is superseded.)* (Q-MP-6.)
- **RD-MP-11 — The library gets a permanent home of its own: an independent library service, with its code in this repo, run by IMRSV on a GPU host; the platform consumes what it publishes** (the lead, 2026-10-14: *"I like your reccomendation for the library home... I guess that is ALSO a new pahse to seed"*). F-MP-42 is its shape; the host is still open. Seeded as `PhaseTBD_LibraryService.md`. (Q-MP-11.)
- **RD-MP-10 — The thumbnail probe waits for the library's permanent machine, and is one of its first tests** (the lead, 2026-10-14: *"lets pause on that … we might want to consdier if this moved to something more perminante with the this as one of the firsts tests"*).

## Open questions

| Id | Question | Recommendation |
|---|---|---|
| ~~Q-MP-1~~ | ~~Which renderer makes the hero thumbnail?~~ | → RD-MP-2 |
| ~~Q-MP-2~~ | ~~The subject per Class?~~ | → RD-MP-3 |
| ~~Q-MP-3~~ | ~~Thumbnails before the review, or after?~~ | → RD-MP-4 |
| ~~Q-MP-4~~ | ~~Who is the management front end for?~~ | → RD-MP-7 |
| ~~Q-MP-5~~ | ~~One word for the published pictures?~~ | → RD-MP-5 |
| ~~Q-MP-6~~ | ~~A rule that the library holds no body skin map?~~ | → RD-MP-9 (not taken; skin maps instead) |
| ~~Q-MP-7~~ | ~~Where thumbnails live before a release?~~ | → RD-MP-6 |
| Q-MP-8 *(reframed 2026-10-14, F-MP-39)* | **How is the owed review done:** (a) the end review in one sitting, (b) keep by verdict and look only at the flagged rows, or (c) as the first job of the team's console on the permanent machine? | **(b) now:** it clears the backlog in minutes, and the console inherits a library with kept articles to curate. (c) if the lead would rather the console's first test be a real review. |
| Q-MP-12 *(new, F-MP-44 to F-MP-46)* | **Close Phase11 now** (review by verdict, 11.4's refine pass moved into the loop as redo rows, then the close), and run material-making as a standing process outside the phase line? | **Yes.** The proof is done in steps; what is left is rig time that belongs on the permanent machine. |
| ~~Q-MP-11~~ → RD-MP-11 *(the host is still open: in the Library Service's discovery)* | **Where the library service runs:** a cloud GPU instance on demand, a dedicated machine, or a GPU worker on the platform's infrastructure? And is it **independent** (code here, run by IMRSV) or **part of the platform's web side**? | **Independent, code in this repo, run by IMRSV**, on a GPU host; the platform consumes what it publishes. The host is a cost and ops call, starting from whether the Linux GPU machine used for the Unreal work is free. |
| ~~Q-MP-9~~ *(superseded by Q-MP-11, 2026-10-14: the "library machine" is a laptop, so where the console runs is part of where the service runs)* | **Where does the team's console run?** (a) A small web app **in this repo**, served from the library machine (where the rig, renders and thumbnails already are) and reachable by the team over its private network. It writes through the existing tools and commits to git. (b) **The platform's web back office**, which already has staff accounts and hosting, writing changes to this repo as pull requests. | **(a).** It keeps the library able to outlive IMRSV (RD-WS-1, condition 3), and anyone who forks the library can curate it. The heavy files it shows stay on the machine that makes them. Approvals stay the maintainer's act either way (`promote_release.py`). |
| ~~Q-MP-10~~ → RD-MP-8 | **The default licence for a new article** (RD-MP-1), and who chooses? | **CC0-1.0 by default.** All 95 on disk are CC0-dedicable, and their sources (ambientCG, Physically Based, our own generators) are CC0. CC BY 4.0 is chosen by a contributor, or forced by a CC BY input, and recorded per article. |

## Status

- **Passes captured:** 10 (2026-10-14). Pass 1 is the audit; Passes 2–7 are design; Passes 8–10 record the lead's answers.
- **Ruled:** RD-MP-1 to RD-MP-11.
  - **The library gets its own permanent service** (RD-MP-11), seeded as `PhaseTBD_LibraryService.md`.
  - **Skin maps reopen no earlier ruling** (RD-MP-9 as corrected; `261014_R_SkinMaps.md` RD-SKM-1).
  - **CC BY 4.0 is allowed beside CC0** (which amends R13), and **CC0 is the default**.
  - Cycles makes the hero thumbnail, on a subject chosen per Class, before the review; it is called a thumbnail; it is never stored in git.
  - The management front end is the IMRSV team's console for curating versions.
  - **Skin moves toward skin maps**, in its own research (`261014_R_SkinMaps.md`).
  - **The thumbnail probe waits for the library's permanent machine.**
- **Current direction:** the flow's first half runs, on a laptop. Its second half is a sketch (Pass 5).
  - The flow needs **a permanent library service** (F-MP-40). The recommended shape is independent, with its code in this repo, run by IMRSV on a GPU host, and the platform consuming what it publishes (F-MP-42).
  - The review is still owed (F-MP-39).
- **Open:**
  - Q-MP-8 (how the owed review is done);
  - Q-MP-12 (close Phase11 now, and make material-making a standing process).

  The service's host is open in its own seed.
- **Durable docs owed, and the verb that lands them:**
  - **RD-MP-1 and RD-MP-8's consequences (F-MP-36):** the licence field, the attribution list, the validator, `CONTRIBUTING.md`, `LICENSE-CONTENT.md`, `_Architecture.md` §Governance, the Glossary and `Experience_MatterLibrary.md`. A lead-directed `/quick-fix` for the words, or the phase that first ships a CC BY article for the field and the validator.
  - **RD-MP-5's wording in four specs:** conformed by the next phase that touches them.
- **Unverified:**
  - Unreal's path tracer or Lumen in a packaged Linux runtime;
  - the GPU time a showcase costs (F-MP-32);
  - the bundle's size at 200 articles;
  - the platform's web server having no GPU (its docs record none).
- **Next step:**
  - the lead's answers to Q-MP-8 and Q-MP-12;
  - `/discovery` on *the Library Service* when the lead opens it;
  - seeds for *Thumbnails* and *the team's console* after it, both of which run on the service.
