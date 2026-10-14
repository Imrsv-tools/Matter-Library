# Research — The Roadmap after 2026-10-14: what is on it, what waits on what, and a draft order for the lead to cut

**Opened:** 2026-10-14 · **Mode:** research. It gathers and commits to nothing. **Mnemonic:** `RO` (ids `F-RO-n`, `Q-RO-n`, `RD-RO-n`).
**Requested by:** the lead, 2026-10-14, verbatim: *"Matter Library just got exciting.. a bunch of new work to do... I can't really see the roadmap or what TBD phases the agents added... can you gather the current state and I would like to refine the orer and setup some phase numbering"*.
**Altitude:** Pass 1 is an **audit** of the Roadmap and the phase stubs as they stand. Pass 2 is a **draft order**: research output, unnumbered, until the lead cuts it. **Numbers are the lead's to assign** (`Methodology/AgenticEngineering_Workflow.md` §Phase Numbering). This doc proposes no number.
**Measured at:** `37cea68` (2026-10-14).
**Extends:** `260926_R_BigPicture_NimbleSetup.md`, whose sequence ends at Phase07, and `261014_R_MaterialPipeline.md` §Proposed phases, which left the order and the numbers to the lead.

---

## The current picture

- **Active:** Phase11 (Library Coverage). **It has been ruled to close** (RD-MP-13: review by verdict, the refine pass moved into the loop, the Blender library rebuilt). The close itself has not run, and Phase11's doc does not yet record the ruling.
- **Future:** 18 entries, all unnumbered. **8 were added today**, each placed last by the agent that added it, so the tail of the list is in the order the day found them, not an order anyone chose.
- **The next free number is Phase13** (Phase12 is complete).
- **The long pole is a server nobody has rented yet.** Thumbnails, the console and the skin-map probe all run on *The Library Service*, and RD-MP-12 puts that on a new Hetzner machine. Everything else can run on the laptop now.

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

---

## Open questions

| Id | Question | Recommendation |
|---|---|---|
| Q-RO-1 | **The cut:** does Pass 2's order stand, and which span gets numbers: (a) the next one, (b) the laptop span, Phase13–17, or (c) through the console, Phase13–20? | **(b).** It numbers what can start now, and leaves the server-bound half free to move once the server's shape is known. |
| Q-RO-2 | **When does the Release Bundle start?** Its L1 ruling (2026-09-25) is the lead's *"b"*, choosing the option that reads *"Re-sequence. Library Coverage becomes P4 (the ~200 materials) … The bundle waits for a library worth versioning."* The same day: *"we have 200 materials to build and test before we have our first versionable library"*. RD-MP-13 has since made material work a standing process with no end. So what marks *"worth versioning"* now: a count of kept materials, or the console existing to cut one? | **After the console, at a count the lead names when it reaches the head of the list.** Not blocking today. |
| Q-RO-3 | **The four overlapping older entries** (F-RO-6): keep them as they are, or annotate them? | **Annotate, never delete:** *See the Library* and *IMRSV Consumes Releases* marked as consumer outcomes; *Author a Material End to End* and *Parity Baselines* marked `Reevaluate (2026-10-14)`, with a pointer to what overlaps them. |
| Q-RO-4 | **One Roadmap line for the standing material-making process**, so the Roadmap does not read as if material work stopped when Phase11 closes (F-RO-7)? | **Yes:** one line under `## Active`, *"Material-making: a standing process, not a phase"*, pointing at `library/wishlist.yaml` and the batch summaries. |
| Q-RO-5 | **Where the library service runs** (F-RO-11): (a) one new GPU machine for everything, (b) the light half on the web server and a GPU machine for the rest, or (c) the light half on the web server and a GPU hired by the hour? | **(a)**, which keeps RD-MP-12. A GPU machine is rented by the month anyway, so moving the light half off it saves little and adds a copy step and a second machine to keep running. The web server stays the website's. The service's discovery confirms it with a measured spec and Hetzner's own price. |

## Resolved

*(none yet: the cut is the lead's)*

## Status

- **Passes captured:** 3 (2026-10-14). Pass 1 is the audit, Pass 2 the draft order, Pass 3 where the library service runs.
- **Current direction:**
  - close Phase11;
  - then the five laptop phases, HDRIs first because the platform is waiting;
  - **beside them, the service's discovery:** the server's spec, its price and its setup recipe. The lead proposed this (F-RO-12);
  - then the server-bound three;
  - then the first real release and its consumers.
- **The web server cannot host the service's GPU half** (F-RO-10). The recommendation stays RD-MP-12: one new GPU machine (Q-RO-5).
- **Open:**
  - Q-RO-1 (the cut and the numbers) is the one that changes what happens next.
  - Q-RO-5 (where the service runs) changes the service's scope, not the order.
  - Q-RO-2 to Q-RO-4 each carry a recommendation and block nothing.
- **Next step:** the lead cuts the order and names the numbers. The ruling lands in `## Resolved` first. Then, as a lead-directed `/quick-fix`, the change goes onto the Roadmap:
  - reorder `## Future`;
  - rename each numbered stub from `PhaseTBD_<Name>` to `Phase<NN>_<Name>` and fix its pointers (F-RO-8);
  - set its status line.
