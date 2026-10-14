# Research — The Roadmap after 2026-10-14: what is on it, what waits on what, and a draft order for the lead to cut

**Opened:** 2026-10-14 · **Mode:** research. It gathers and commits to nothing. **Mnemonic:** `RO` (ids `F-RO-n`, `Q-RO-n`, `RD-RO-n`).
**Requested by:** the lead, 2026-10-14, verbatim: *"Matter Library just got exciting.. a bunch of new work to do... I can't really see the roadmap or what TBD phases the agents added... can you gather the current state and I would like to refine the orer and setup some phase numbering"*.
**Altitude:** Pass 1 is an **audit** of the Roadmap and the phase stubs as they stand. Pass 2 is a **draft order**: research output, unnumbered, until the lead cuts it. **Numbers are the lead's to assign** (`Methodology/AgenticEngineering_Workflow.md` §Phase Numbering). This doc proposes no number.
**Measured at:** `37cea68` (2026-10-14).
**Extends:** `260926_R_BigPicture_NimbleSetup.md`, whose sequence ends at Phase07, and `261014_R_MaterialPipeline.md` §Proposed phases, which left the order and the numbers to the lead.

---

## The current picture

*(Reconciled at the end of the run, 2026-10-14. Passes 1–2 below are the audit as measured at its start.)*

- **The Roadmap holds the lead's order** (RD-RO-3, landed `2739b6b`, pushed):
  - first: Materials Described, whose first step is the dev snapshot the platform's site is waiting on, then HDRIs and Scale Grids;
  - then the library service, which takes one package per material and tests it on upload (RD-RO-1), and what runs on it;
  - then the first real release and its consumers.
- **Nothing is numbered.** The next free number is Phase13; Phase11 closed the same day (`6b824f7`).
- **Materials are CC0 only** (RD-RO-2), and *Two Licences* is withdrawn.
- **Still open, blocking nothing:**
  - Q-RO-2: when the Release Bundle starts;
  - Q-RO-5's record of the service's shapes. The order's line has the service rendering on upload.

---

## Pass 1 — What the Roadmap holds (audit, 2026-10-14)

**Examined:** `Roadmap.md`; every stub in `Phases/Future/`; the Status footers of the research docs those stubs cite; `PlatformDependencies.md` (the rows the platform asks of the library, M1–M10).

**F-RO-1 — The Future list, in its current position on the Roadmap.** "Waits on" lists only real dependencies, each from its stub or its research doc.

| Entry | Status | Added | Waits on | What waits on it |
|---|---|---|---|---|
| Hair That Reads as Hair | RESEARCH | 2026-09-28 | a research thread of its own (H4 cards, H5 strands) | — |
| Skin Maps | SEEDED | 2026-10-14 | its research's industry survey (`261014_R_SkinMaps.md` Pass 3) before discovery; **the library service** for its probe | — |
| Release Bundle and Consumer Contract | SEEDED, discovery Pass 1 kept | 2026-09-25 | L1: *"the material work goes first"* (Q-RO-2); the texture encoder, missing on the laptop (F-MP-29) | Blender from a Release, Unreal Reference Masters, IMRSV Consumes Releases; the site's published feed (M9 (1)) |
| IMRSV Consumes Releases | RESEARCH | 2026-09-23 | Release Bundle | — *(the platform's phase, on the platform's line)* |
| Blender from a Release | RESEARCH | 2026-09-23 | Release Bundle | — |
| See the Library | RESEARCH | 2026-09-23, re-shaped 2026-10-14 | Thumbnails, Materials Described, Release Bundle *(the site itself is the platform's, RD-WS-1)* | — |
| Version Management | SEEDED | 2026-05-30, trimmed 2026-09-23 | nothing (the pilot `matterlib-0.1.0` exists to carry forward) | the console's release composer follows its rules |
| Author a Material End to End | RESEARCH | 2026-09-23 | — | — *(overlaps the console, F-RO-6)* |
| Contribution Path | RESEARCH | 2026-09-23 | the library service (a contributed script runs as code, F-MP-28); Two Licences (a contributor picks one) | — |
| Parity Baselines | RESEARCH | 2026-09-23 | — | — *(overlaps Materials Described, F-RO-6)* |
| Unreal Reference Masters | RESEARCH | 2026-09-23, re-scoped 2026-09-28 | Release Bundle (*"taken from a release"*); the see-through masters (M6, open) | the platform's Studio adopting the library masters (P20) |
| HDRIs in the Library | SEEDED | 2026-10-14 | nothing | **the platform's own HDRI phase** (M10) |
| Scale Grids | SEEDED | 2026-10-14 | nothing | — |
| The Library Service | SEEDED | 2026-10-14 | **a rented server** (RD-MP-12), outside the repo | Thumbnails, The Library Console, the skin-map probe, the loop at volume |
| Thumbnails | SEEDED | 2026-10-14 | the library service (RD-MP-10) | The Library Console; See the Library |
| Materials Described | SEEDED | 2026-10-14 | nothing to start (its stub) | The Library Console; See the Library |
| The Library Console | SEEDED | 2026-10-14 | the library service; Thumbnails; Materials Described | — |
| Two Licences | SEEDED | 2026-10-14 | nothing | any CC BY material reaching a release; Contribution Path |

**F-RO-2 — Phase11's close is owed and ruled.** RD-MP-13 (`261014_R_MaterialPipeline.md`): *"Phase11 closes now"*, with 11 of 35 rows kept by verdict and 24 for the lead's eye (F-MP-47). The Roadmap still shows it `ACTIVE`, correctly, because the close is `/execute Phase11`'s. `Phase11_LibraryCoverage.md` says *"paused by the lead after 11.3 (2026-10-02)"* and records no 2026-10-14 ruling (grep, 2026-10-14). The close records it.

**F-RO-3 — The server sets the pace for half the list.** Nothing in the repo can rent a Hetzner machine. Until one exists, Thumbnails, the console, the skin-map probe and the loop at volume cannot run. **Starting *The Library Service*'s discovery early is what shortens that wait**, because choosing the server is its first open question. Everything else on the list runs on the laptop: HDRIs, Scale Grids, Two Licences, Materials Described and Version Management, plus the Skin Maps survey (research).

**F-RO-4 — The pull from outside.** The platform's HDRI phase waits on *HDRIs in the Library* (M10, `OPEN`). The site's staging also waits on M9, but it runs on the dev catalog meanwhile (M9's own row), so that is not a hard wait. M6 (the see-through masters) is a ledger item, not a phase. It sits under two entries: Unreal Reference Masters, and an Unreal-rendered thumbnail (RD-MP-2).

**F-RO-5 — Two contract phases each move the catalog's `schema_version`.** HDRIs moves it 2 → 3 (its stub, A2–A3). Release Bundle bumps it for the master token (its stub, §Why). This is not a dependency: whichever lands second bumps again. Each bump is a consumer-visible change, so the cut may prefer to put them close together.

**F-RO-6 — Four older entries overlap today's seeds.** They are kept, and none is deleted (`.claude/CLAUDE.md` §Don't Delete Spec Functionality):
- **See the Library:** its library halves are now *Thumbnails* and *Materials Described*, plus the release publish. The site itself is the platform's (RD-WS-1). It now reads as a **consumer outcome**, like *IMRSV Consumes Releases*, more than a library phase.
- **Author a Material End to End (the Matter Manager):** *The Library Console* is its maintainer half (`PhaseTBD_LibraryConsole.md` §Open questions). The Creator's half lives in each consumer (F-MP-25).
- **Parity Baselines:** *Materials Described* carries the parity verdict per Creator port for the site (WS-F6). That is most of *"anyone can see how closely its renders match"*.
- **Hair That Reads as Hair** heads the list by position, but it has been research-only since 2026-09-28. *Skin Maps* is its sibling: character realism on the approved mesh.

**F-RO-7 — After Phase11 closes, nothing on the Roadmap says that material-making continues.** RD-MP-13 makes it *"a standing process outside the phase line"*. The Roadmap registers phases, so once Phase11 moves to `## Complete` a reader sees no material work at all (Q-RO-4).

**F-RO-8 — Renaming a stub when it is numbered is cheap.** Pointers by name, measured with `git grep` at `37cea68`:
- Version Management: 8 pointers in 7 files.
- Release Bundle: 6 pointers in 4 files.
- The Library Service: 4 pointers in 3 files.
- Every other stub: 1 to 3 pointers.

The finding and ruling ids keep their stems (`RD-MP-n`, `RD-SKY-n`). They have left the repo in commit messages and are frozen (Workflow §Phase Numbering).

---

## Pass 2 — A draft order (design; unnumbered, for the lead to cut)

**The method:** what is owed comes first, then what runs on the laptop, then what needs the server, then the first real release, then its consumers. Within a group the order is a recommendation, not a dependency. Where it is a dependency, it says so.

**Owed now**
- **Close Phase11** (RD-MP-13). This is already ruled; it is `/execute Phase11`.

**On the laptop: nothing it needs is missing**
- **HDRIs in the Library:** the platform's HDRI phase is waiting on it (M10). It is a contract change, so it goes before more contracts move.
- **The Library Service:** it goes early because the server must be rented first, and its discovery picks the server. Its build overlaps the phases after it.
- **Scale Grids:** small and independent. Every material check after it can use a scale view.
- **Two Licences:** before any CC BY material is built, and before *Materials Described* publishes a licence.
- **Materials Described:** needs nothing. It writes the words for Phase11's kept articles, and the batch loop writes them from then on.

**On the server**
- **Thumbnails** *(dependency: the service)*.
- **Skin Maps** *(dependency: its survey, a research session the lead opens, which can run any time before; the probe runs on the service)*.
- **The Library Console** *(dependency: the service, Thumbnails, Materials Described)*.

**The first real release**
- **Release Bundle and Consumer Contract:** the first publish, carrying the thumbnails, the site file and the attribution list (M9). Q-RO-2 asks when it starts.
- **Version Management:** the second release cut from the first. Until consumers hold a release, *"Fix forward only... we have no legacy projects yet"* (its stub's 2026-09-24 precedent) leaves it little to protect. The console's composer starts with today's lockfile rules and adopts these when they land.

**Consumers of a release, and the outside path**
- **Blender from a Release**, then **Unreal Reference Masters** *(also waits on M6)*.
- **IMRSV Consumes Releases** and **See the Library**: the platform's work, kept here as consumer outcomes (F-RO-6).
- **Contribution Path** *(dependency: the service's sandbox, Two Licences; the console is where a contribution is judged)*.

**Held, not ordered**
- **Hair That Reads as Hair:** research, best opened after the Skin Maps survey, because it uses the same mesh and the same kind of survey.
- **Author a Material End to End** and **Parity Baselines:** `Reevaluate (2026-10-14)` against the console and *Materials Described* (F-RO-6). Kept, not deleted.

**Where to number** (Q-RO-1). These are the method's own shapes; how many to number is the lead's call:
- **(a) The next one only:** HDRIs gets Phase13. Every later slot stays free to insert into or split.
- **(b) The laptop span:** Phase13–Phase17 (HDRIs, The Library Service, Scale Grids, Two Licences, Materials Described). Everything that needs the server stays `TBD` until the server exists, because that is where the shape is still likely to move.
- **(c) Through the console:** Phase13–Phase20. This gives up insertion for eight phases, three of them behind a server with no date.

A **Wave** (the method's word for coupled phases) was considered for the service, Thumbnails, Materials Described and the console, and is not recommended. They share two surfaces, the thumbnail record and the site file, and each has one owner already.

---

## Pass 3 — Where the library service runs: the web server, or a new machine (2026-10-14)

**The lead, verbatim:** *"Do I need a new Hetzner machine or should we/ could we run it on the Web system? I think the laptop work but concurently we can define and setup the server specs.... what do you think?"*

**It re-asks a ruling, quoted:** RD-MP-12, *"The library service needs a new server, rented from Hetzner … The platform's web server is the only server today, and it records no GPU."* This pass tests whether that still holds. It does not reverse it.

**Examined:** the platform's web repo, read-only. Its server facts are not copied here (this repo is public). Also, Hetzner's GPU offer as third parties report it.

- **F-RO-9 — The web server is a small, shared cloud server with no GPU.** Its own docs throttle the platform's builds on it because it is shared (read 2026-10-14). Hetzner's cloud servers do not offer a GPU; its GPU machines are dedicated servers rented by the month. **Unverified as of 2026-10-14** (third-party listings; Hetzner's own price page was not read): the entry model is the GEX44 (one RTX 4000 SFF Ada, 20 GB), quoted at €184 to €234 a month plus a setup fee. The service's discovery reads the price on hetzner.com.
- **F-RO-10 — The service is two halves, and only one of them could live on the web server:**
  - **The GPU half** cannot run there:
    - the rig in three tools (the Unreal runtime needs Vulkan on a GPU, and Storm and Cycles render on one);
    - thumbnails;
    - the 30–50 minute toolchain build.

    With no GPU, rendering on a few shared cores would take hours per batch and slow the site down.
  - **The light half** could run there: the console, the dev catalog, serving the thumbnail folder, git.
  - **Two jobs never run on the web server, whichever shape is chosen:**
    - the agent's sessions, which hold push rights to this public repo;
    - a contributor's generator script, which is outside code (F-MP-28).

    A public website's machine should hold neither.
- **F-RO-11 — Three shapes. Each keeps the code in this repo, so each keeps RD-MP-11 and RD-WS-1's *"the library survives without IMRSV"*:**
  - **(a) One new GPU machine runs everything** (RD-MP-12 as ruled). One box, one setup, always on. It costs one monthly rental.
  - **(b) The light half on the web server, the GPU half on a new GPU machine.** Two boxes, and the renders are copied from one to the other for the console to show. The saving is small, because the GPU box is rented by the month anyway.
  - **(c) The light half on the web server, with a GPU hired by the hour** from a cloud that rents GPUs that way (Hetzner does not). It is cheapest if batches are occasional. It has the most moving parts: the toolchain and the Unreal runtime are set up again on every start.
- **F-RO-12 — "The laptop work, and concurrently define and set up the server specs" is Pass 2's draft, with the service's discovery run beside the laptop phases.** That parallel track is the service's discovery, which delivers:
  - the spec (GPU, its memory, RAM, disk), measured from what the rig, the toolchain and the Unreal runtime use on today's two machines;
  - the price from Hetzner's own page;
  - the setup recipe, in this repo.

  **Renting the machine is the lead's act.** No laptop phase waits on it.

## Pass 4 — A fourth shape: the GPU work happens on the contributor's machine (2026-10-14)

**The lead, verbatim:** *"I lean toward server option "a"... I wonder - is there an option that all the creation and other work is done locally on the contributors system (the test, the thumbnails, etc) then all that is packed and sent to the git repo basically "ready to go" and we validate what we can of the content... so don't need a GPU?"*

- **F-RO-13 — This is how the work already runs.** The laptop builds each article, runs the rig in all three tools and writes the batch summary. The Unreal column comes from the packaged runtime, which the rig downloads, and which runs on *"any Linux machine with a GPU"* (Phase06's Outcome; Phase06 Click 2 proved it on a machine with no Unreal installed). The service was meant to move that work off the laptop. This shape instead makes the contributor's machine the place it belongs.
- **F-RO-14 — What a server with no GPU can still check.** A contributor's pictures are **evidence that the server cannot re-make**, so it checks that the evidence belongs to the content:
  - **The gate**, `run_all.py`, as today: the name, the schema, MaterialX validity, the lockfile, provenance and the licence.
  - **The binding.** Each rig result and thumbnail records what made it: the article's hash, the masters version, the renderer and its version, and the scene version (F-MP-10). The server checks every one of them against the repo. A picture of a different article, or one made with old masters or an unpinned tool, is refused.
  - **The picture as a file:** its size, its format, its colour space, and that it is not blank.
  - **Possibly, a small CPU render** (Cycles runs without a GPU) compared with the contributor's thumbnail, to catch a picture that does not match its article. It is unproven, and slow even at a small size. A probe would decide it.

  **What it cannot check:** the Unreal and Storm columns, without re-rendering them on a GPU. **The maintainer's review stays the real gate** (F-MP-22). The review judges the sheet and the thumbnails, so the server only has to show that they are the article's own.
- **F-RO-15 — What it costs:**
  - **A contributor needs a Linux machine with a GPU** for the Unreal column, plus Blender 5.1+ and the USD toolchain (a 30–50 minute build). That narrows who can contribute a full article. A contributor without one could send the build alone and leave the rig and thumbnails to the maintainer's machine.
  - **One look across the library needs a pinned kit:** the same showcase scene, tool versions and colour settings on every machine. Shape (a) needs the same recipe for its own server, so the work is the same either way. Here it is packaged for contributors.
  - **Re-running the whole library has no home.** When a master, the runtime or the showcase scene changes, every affected picture is stale (F-MP-4, F-MP-23). The masters' builder has changed in **15 commits since 2026-09-28** (`git log`, 2026-10-14). At 7–22 minutes of rig time per article (F-MP-44), a sweep of ~200 articles is roughly **23–73 GPU hours**, plus thumbnails. Nobody's contribution pays for that. It falls on the maintainer's machine, or on a GPU hired by the hour for the sweep.
  - **Thumbnails do not go in git** (RD-MP-6). So the package splits in two: the article goes to the repo as a pull request, and the pictures are uploaded to the server's folder. *"Sent to the git repo ready to go"* holds for the article, not the pictures.
- **F-RO-16 — The server shrinks to a small always-on machine with no GPU:** the checks above, the console, the dev catalog and the thumbnail folder. **It runs no agent session and no contributor code** (F-RO-10's two exclusions), which makes it a plain web app. That reopens the web server as a candidate host, or a small cloud server of its own beside it.
- **F-RO-17 — It grows into (a) without throwing anything away.** Shape (d) builds the pinned kit, the evidence records, the checks and the console. If library-wide sweeps outgrow personal machines and hourly hire, a GPU machine can join later and run the same kit. That decision then rests on measured hours, not on a guess.

## Pass 5 — One package per material, tested on upload (2026-10-14)

**The lead, verbatim:** *"No...I see.. that is jenky... I was hoping our repo could explain how to have everything packaged up, they submit one entry per material, then we test on upload and parse as needed (like we do with compositions on web) but if they need to upload the material, and then texctures, and then another for the thumbnail... this is too messy... Phase 11 close is underway."*

**The precedent he names:** the platform's web side takes a published composition as **one upload**. It checks the upload in a fresh sandbox per upload, and a refusal names the rule it broke. An accepted upload becomes an unchangeable version with a fingerprint. The web side's own docs were read, read-only, on 2026-10-14; no detail of theirs is copied here.

- **F-RO-18 — Pass 4's shape (d) split the submission across three places:**
  - the article into git;
  - the pictures to a folder;
  - the evidence checked against both.

  The lead rejects it for that (RD-RO-1). What remains of Pass 4 is the check on upload (F-RO-14), which carries over.
- **F-RO-19 — The shape the lead describes:**
  - **One file per material: the material package.** It holds everything:
    - the recipe, the `.mtlx` and its textures;
    - provenance and the licence;
    - the words (label, summary, search words).

    One command in this repo makes it, and `CONTRIBUTING.md` explains how.
  - **One upload,** to the library service.
  - **The check on upload,** in a fresh sandbox per upload, as the web side does:
    - the one-command gate;
    - the package's completeness;
    - a refusal names its rule.
  - **Parsed on our side.** The service puts the article into git (a branch the review reads), the pictures into the thumbnail folder, and the words into the site file's source. **The contributor never sees the split.**
- **F-RO-20 — Who makes the pictures is now the only open part, and "test on upload" points to the service:**
  - **Contributor's evidence in the package** (Pass 4). It needs no GPU on our side. It brings back every cost F-RO-15 named: the contributor needs a Linux GPU machine and the full kit; the library-wide re-runs have no home; and nothing re-checks a picture.
  - **The service renders on upload** (shape (a)): the rig in all three tools, then the thumbnails. The package carries the material only. **Anyone can contribute without a GPU or the toolchain.** One machine makes every picture, so the library looks consistent, and that same machine re-runs the library when a master changes.

  **Recommendation: the service renders** (shape (a) with the package door). It is what *"we test on upload"* means once the test includes the pictures, and the lead already leaned (a).
- **F-RO-21 — The package carries data, not code.** A contributor's generator *script* is code (F-MP-28). The package carries its output, the textures, and names the script as provenance. Running contributed code stays *Contribution Path*'s question.
- **F-RO-22 — The batch loop submits through the same door.** `/matter-batch` on the laptop becomes one more contributor: it makes a package and uploads it. **One path in, for the library's own work and for outsiders.** The laptop stops being where the pictures are made.
- **F-RO-23 — Where this sits on the Roadmap:**
  - **The door is the library service's first outcome:** a material package uploaded, tested and pictured, waiting for review.
  - ***Contribution Path* keeps what is specific to outsiders:** accounts, contributed scripts, and maintainers-only releases.
  - The stub *The Library Service* is updated by the quick fix that lands the lead's cut. Research does not edit a stub.

### The order, redrawn (unnumbered; one after the other, for the lead to check)

*Phase11's close is underway in another session, so it is not listed.*

- **HDRIs in the Library:** a scene's HDRI is chosen from the library by name.
- **Scale Grids:** swap every object to its scale grid and see at once whether a metre is a metre.
- **Two Licences:** a material is CC0 or CC BY, and is credited wherever it is used.
- **Materials Described:** every material has a readable name, a one-line description and search words.
- **The Library Service:** a contributor uploads one material package, and it comes back tested in all three tools, waiting for review. *Its spec is defined beside the four above; the build starts when the server is rented.*
- **Thumbnails:** every material is shown at its best, on a subject that suits it.
- **Skin Maps:** a character's skin varies across the body, as real skin does.
- **The Library Console:** the team reviews, keeps or sends back, and picks what goes into each version, on one page.
- **Release Bundle:** anyone downloads one verified release and uses it without this repo.
- **Version Management:** the next release is cut from the last, and every old one stays reproducible.
- **Blender from a Release:** a Blender user installs the add-on and the library from a release.
- **Unreal Reference Masters:** Studio, or any Unreal user, renders library materials with the masters from a release.
- **Contribution Path:** an outsider submits a package and gets a verdict; only maintainers release.

**The platform's, kept as consumer outcomes:** *IMRSV Consumes Releases* · *See the Library*.
**Held:**
- *Hair That Reads as Hair*: research, after the Skin Maps survey.
- *Author a Material End to End* and *Parity Baselines*: `Reevaluate (2026-10-14)` (F-RO-6).

## Pass 6 — What the platform's site phase needs now, and whether a placeholder is smart (2026-10-14)

**The lead, verbatim:** *"Can we do the things WEB needs for its phase 36 even if we just have palcehoder we fill out later... or is taht not really smart?"*

**Examined:** the platform's site phase, read-only at the web repo's origin, 2026-10-14. It is in execution. It wrote a section addressed to this library's session (*"Needs the library"*). Its ids are not copied here (`LOCAL_DELTAS.md` §Separation). Also measured: what the library already holds on disk.

- **F-RO-24 — What the site asks for: one dev snapshot, published as a GitHub pre-release**, which is the library half of PlatformDependencies **M9**:
  1. a tag starting `matterlib-` (for example `matterlib-0.2.0-dev.1`), marked as a pre-release;
  2. **the site file**: per article, its id and version, domain, class and master, scale tag and metres per tile, status and whether a Creator can pick it, the Creator controls with start values and ranges, sources and licence, the parity verdict per control, and the file names of its pictures and its zip. A summary and a plain name are optional;
  3. **pictures**, as release assets at web size: thumbnails, and the rig's pictures in the three tools. **"Whatever subset exists is fine."**
  4. **one MaterialX zip per material:** the `.mtlx` and every texture it uses, the shared wear layers included;
  5. **a sha256 digest for every file.**

  The site's browsing is already built on a fixture it drafted from this repo's public files. Only the step that shows pictures, downloads and releases is parked on this snapshot. The site stays on staging until the library's first versionable release.
- **F-RO-25 — Almost all of it is real data today, not placeholder** (measured 2026-10-14):
  - every field in item 2 already exists in the recipes, the lockfile, the masters' control table and the dev catalog, except the parity verdict. **Rig output exists for 82 articles, 72 of them with a scorecard**, under the git-ignored `library/parity/` on the laptop (81 GB at full size);
  - the zip follows the exporter's complete-portable form (`tools/conformance/build_portable.py`), which already gathers an article and its wear layers;
  - digests are trivial;
  - **only the thumbnails (RD-MP-2) and the summaries do not exist.**
- **F-RO-26 — So the smart form of "placeholder" is *absent and labelled*, never *made up*.**
  - The site already handles the absence. A missing picture shows a swatch of the material's colour, labelled *"texture, not a render"*. A missing plain name is derived from the article's name. A missing summary is simply not shown.
  - The snapshot therefore carries only true fields. It leaves the thumbnails and summaries out, and fills them in later in the same file shape. This keeps the Working Agreement's *No Mock Data Masquerading as Real*: a field present with a made-up value would be published on a public release.
  - **The real risk is the file's shape,** because the library owns it as a contract (RD-WS-4) and both repos pay for a change. The site drafted a shape and asked the library to adopt or change it. Adopting it as a **draft contract spec, marked as one, before the first versionable release** costs little to change while only staging reads it.
- **F-RO-27 — This is *Materials Described*'s first step, and it moves to the front.** That phase's Outcome already says *"the library publishes everything the website shows about each material in one file beside each release"*:
  - **its first step** is the dev snapshot above;
  - **its later step** writes and confirms the summaries and search words.

  The pictures it carries are the rig's for now. *Thumbnails* adds the showcase pictures to the same file later. The pre-release is a small slice of *Release Bundle*'s publishing (the GitHub Release and its digest), and decides none of that phase's contract.
- **F-RO-28 — A pre-release on this public repo is a publication: irreversible, and the lead's word** (`.claude/CLAUDE.md`). Its content is already public in the repo, all CC0. A pre-release also takes the downloads off Git LFS bandwidth, which the site's research warned about.
- **F-RO-29 — The site's licence ruling collides with this repo's.** On the web side, the lead answered *"Yes CC0 only"*, recorded there as *"Every Matter article is CC0-1.0; CC BY is not allowed"*. The web side notes *"the library records its own"*. This repo's **RD-MP-1** says: *"CC BY 4.0 is allowed beside CC0-1.0"* (the lead: *"CC by is indeed OK .. this is inline with our asset library and composition sharing approach in imrsv labs"*). **RD-MP-8** says: *"A new article is CC0-1.0 by default"* (*"CC0 is fine"*). Both rulings are recorded; neither is resolved here (Q-RO-6). *(Resolved the same day: CC0 only, RD-RO-2.)* Either way, the snapshot is unaffected: every article on disk is CC0. **If CC0-only holds for the library, *Two Licences* leaves the order**, marked `Withdrawn (2026-10-14)` and kept.

### The order, with this pass (unnumbered; one after the other)

- **Materials Described:** the website shows every material, with its rig pictures and a download, from a dev snapshot the library publishes; then a readable name, a one-line description and search words for each.
- **HDRIs in the Library:** a scene's HDRI is chosen from the library by name.
- **Scale Grids:** swap every object to its scale grid and see at once whether a metre is a metre.
- **The Library Service:** a contributor uploads one material package, and it comes back tested in all three tools, waiting for review.
- **Thumbnails:** every material is shown at its best, on a subject that suits it.
- **Skin Maps:** a character's skin varies across the body, as real skin does.
- **The Library Console:** the team reviews, keeps or sends back, and picks what goes into each version, on one page.
- **Release Bundle:** anyone downloads one verified release and uses it without this repo.
- **Version Management:** the next release is cut from the last, and every old one stays reproducible.
- **Blender from a Release:** a Blender user installs the add-on and the library from a release.
- **Unreal Reference Masters:** Studio, or any Unreal user, renders library materials with the masters from a release.
- **Contribution Path:** an outsider submits a package and gets a verdict; only maintainers release.

---

## Open questions

| Id | Question | Recommendation |
|---|---|---|
| Q-RO-1 | **The cut:** does Pass 2's order stand, and which span gets numbers: (a) the next one, (b) the laptop span, Phase13–17, or (c) through the console, Phase13–20? | **(b).** It numbers what can start now, and leaves the server-bound half free to move once the server's shape is known. |
| Q-RO-2 | **When does the Release Bundle start?** Its L1 ruling (2026-09-25) is the lead's *"b"*, choosing the option that reads *"Re-sequence. Library Coverage becomes P4 (the ~200 materials) … The bundle waits for a library worth versioning."* The same day: *"we have 200 materials to build and test before we have our first versionable library"*. RD-MP-13 has since made material work a standing process with no end. So what marks *"worth versioning"* now: a count of kept materials, or the console existing to cut one? | **After the console, at a count the lead names when it reaches the head of the list.** Not blocking today. |
| Q-RO-3 | **The four overlapping older entries** (F-RO-6): keep them as they are, or annotate them? | **Annotate, never delete:** *See the Library* and *IMRSV Consumes Releases* marked as consumer outcomes; *Author a Material End to End* and *Parity Baselines* marked `Reevaluate (2026-10-14)`, with a pointer to what overlaps them. |
| Q-RO-4 | **One Roadmap line for the standing material-making process**, so the Roadmap does not read as if material work stopped when Phase11 closes (F-RO-7)? | **Yes:** one line under `## Active`, *"Material-making: a standing process, not a phase"*, pointing at `library/wishlist.yaml` and the batch summaries. |
| ~~Q-RO-6~~ → RD-RO-2 | **CC0 only, or CC0 with CC BY allowed?** On the web side the lead said *"Yes CC0 only"*. This repo's RD-MP-1 allows CC BY beside CC0 (F-RO-29). | **CC0 only, library-wide**, as the lead's latest word. RD-MP-1 is then marked withdrawn in place, and *Two Licences* is marked `Withdrawn (2026-10-14)` and kept, not deleted. The lead decides. |
| Q-RO-5 | **Where the library service runs** (F-RO-11, F-RO-16): (a) one new GPU machine for everything, (b) the light half on the web server and a GPU machine for the rest, (c) the light half on the web server and a GPU hired by the hour, or **(d) the GPU work on each contributor's machine, sent as a ready package, with a small server that has no GPU and checks the evidence** (Pass 4, the lead's idea)? | **(a), with the one-package door (RD-RO-1, F-RO-20):** the service renders the rig and the thumbnails on upload. *(Pass 4 recommended (d); the lead rejected its split submission in Pass 5. A package carrying the contributor's own pictures is still possible, but it brings back Pass 4's costs.)* |

## Resolved

- **RD-RO-1 — A material is submitted as one package, in one upload, tested on upload and taken apart on the library's side. The contributor never uploads the material, its textures and its pictures separately.** (The lead, 2026-10-14: *"they submit one entry per material, then we test on upload and parse as needed (like we do with compositions on web)… this is too messy"*.) This rules out Pass 4's split submission. Who makes the pictures is Q-RO-5.
- **RD-RO-3 — Pass 6's order is the Roadmap's order, unnumbered** (the lead, 2026-10-14, to *"Order is good - put it on the Roadmap"*: *"yep! Good... quickix and push"*). It closes Q-RO-1's order half; numbers stay the lead's to assign.
- **RD-RO-2 — Materials are CC0-1.0, and only CC0. A contributor's handle, when one is given, is carried as a courtesy and for the platform's Forseti tracking.** (The lead, 2026-10-14: *"YES... CC0 for materials... we decided that... material are CC0 but we will carry a handle if one is provided as courtesy and Forseti tracking"*.) Its effects:
  - **It withdraws RD-MP-1** (CC BY beside CC0), with in-place notes there and on R13. RD-MP-8's default becomes the only licence.
  - ***Two Licences* leaves the order:** it is marked `Withdrawn (2026-10-14)` and kept, by the quick fix that lands the cut.
  - **The handle is new data** that nothing records today. The material package carries it when a contributor gives one (RD-RO-1). The site file publishes it (*Materials Described*). It is credit, never a licence condition. Closes Q-RO-6.

## Status

- **Passes captured:** 5 (2026-10-14):
  - Pass 1, the audit;
  - Pass 2, the draft order;
  - Pass 3, where the library service runs;
  - Pass 4, the contributor-side shape (d);
  - Pass 5, one package per material, with the order redrawn;
  - Pass 6, the site's dev snapshot. It is real data with gaps labelled, not placeholders, so *Materials Described* moves to the front and the order is redrawn again.
- **Ruled:**
  - **RD-RO-1:** a material is submitted as one package in one upload, tested on upload and taken apart on our side. Pass 4's split submission is out.
  - **RD-RO-2:** materials are CC0 only, and a contributor's handle is carried as a courtesy and for Forseti tracking. RD-MP-1 is withdrawn, and *Two Licences* leaves the order.
- **Phase11's close is underway** in another session (the lead, 2026-10-14).
- **Current direction:** Pass 6's order:
  - *Materials Described* first. Its first step is the dev snapshot the platform's site is parked on (F-RO-27);
  - then the laptop phases (HDRIs, Scale Grids). *Two Licences* is withdrawn (RD-RO-2);
  - beside them, the library service's spec (F-RO-12);
  - then the service, whose first outcome is the package door (F-RO-23);
  - then Thumbnails, Skin Maps and the console;
  - then the first real release and its consumers.
- **The recommendation is (a): the service renders on upload** (F-RO-20). The web server cannot host the GPU half (F-RO-10), and the lead leans (a). Pass 4's (d) and its loosened order are superseded by RD-RO-1, kept as the record.
- **Open:**
  - Q-RO-1: the lead checks Pass 5's order (*"Not numbered just one after the other with SHORT outcome so I can verify this makes sense"*), then cuts it and names any numbers.
  - Q-RO-5: who makes the pictures. The recommendation is (a), the service.
  - ~~Q-RO-6~~ → **RD-RO-2:** CC0 only, with a contributor's handle carried as a courtesy.
- **Owed beside the cut:** PlatformDependencies **M9** gains the site's dev-snapshot ask (F-RO-24), as a quick fix.
  - Q-RO-2 to Q-RO-4 each carry a recommendation and block nothing.
- **Graduated, 2026-10-14 (RD-RO-3):** the lead cut Pass 6's order and directed a `/quick-fix` and a push. The quick fix landed:
  - `## Future` reordered, with a dated re-sequencing note;
  - Two Licences marked withdrawn;
  - See the Library and the two overlapping entries annotated (Q-RO-3, taken as recommended);
  - the package door carried into *The Library Service*'s stub;
  - the dev snapshot carried into *Materials Described*'s stub;
  - the outsider-only scope added to *Contribution Path*'s pointer;
  - the site's snapshot ask added to M9.

  **No numbers were assigned.** Q-RO-1's numbering half stays the lead's, and F-RO-8 prices the renames for whenever he names them. Q-RO-2 (when the Release Bundle starts) stays open, and blocks nothing.
- **Next step:** `/discovery` on *Materials Described*, starting with the dev snapshot.
