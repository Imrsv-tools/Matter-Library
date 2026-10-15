# Research — A server without the GPU: the rig stays local, everything around it moves to a server; and what on the Roadmap is already done

**Opened:** 2026-10-15 · **Mode:** research. It gathers and commits to nothing. **Mnemonic:** `SV` (ids `F-SV-n`, `Q-SV-n`, `RD-SV-n`).
**Requested by:** the lead, 2026-10-15, verbatim: *"We are not going to setup a remote servier with a GPU right now... so that part needs to be local but we need to figure out how to pull that functinality out and get more things manages on a server, and I feel like some of the things on this list have been addressed.... So lets dig in... thoughts?"*
**Altitude:**
- **Pass 1 is an audit:** what the Roadmap's `## Future` entries already have, measured against what Phases 13–17 shipped.
- **Pass 2 is a design sketch:** which work needs the GPU, which does not, and how the two meet. It names no file or route to build.
- **Pass 3 is a draft order:** unnumbered, for the lead to cut.

**Measured at:** `0910615` (2026-10-15).
**Extends:**
- `PhaseTBD_LibraryService.md`: its Brief, kept for a rented GPU server; its §Not now; its findings F-P17-1 to F-P17-7.
- `261014_R_RoadmapOrder.md`: Passes 3–5, F-RO-10, F-RO-16 and F-RO-17, and RD-RO-1.
- `261014_R_MaterialPipeline.md`: RD-MP-12, RD-MP-14.

---

## The current picture

- **The GPU work stays on the laptop** (RD-MP-14, re-affirmed 2026-10-15): the rig in Storm, Blender and Unreal; the Cycles thumbnails; the AI skin probe.
- **Most of what was planned around the rig needs no GPU at all:**
  - the gate on every push;
  - the inbox for a material package;
  - the review queue and the console;
  - the release cut;
  - the stale list.
- **The shape that joins the two halves: the server keeps the queue, and the laptop *pulls* work from it when it is on.** The laptop serves nothing, so RD-MP-12's *"the personal machines are not hosts"* still holds. When a GPU server exists later, it runs the same worker.
- **Several Future entries are mostly done.** *See the Library*'s library half shipped in Phases 13–17 (seven dev snapshots). *Parity Baselines* is published in every snapshot. Part of *Release Bundle*'s publishing runs today.

---

## Pass 1 — What on the Roadmap is already addressed (audit, 2026-10-15)

**Examined:**
- the Roadmap's `## Future` and `## Complete`;
- `tools/releases/build_snapshot.py`, which says what a dev snapshot holds;
- the repo's GitHub releases (`gh release list`);
- PlatformDependencies M9 and P24–P27;
- the stubs.

**F-SV-1 — What a dev snapshot holds, from `build_snapshot.py`'s own header, published as `matterlib-0.2.0-dev.1` to `-dev.7` (2026-10-14):**
- the site file;
- the rig's default pictures per tool;
- one zip per material (its `.mtlx` and every texture it uses);
- the Cycles thumbnails;
- each HDRI's thumbnail;
- `SHA256SUMS` over every file.

The site file carries the parity verdict per Creator port, using the rig's own word (`moved_verdict`).

**F-SV-2 — Each Future entry, against that:**

| Entry | Already there | Left | Suggested Roadmap action |
|---|---|---|---|
| **See the Library** | **The library's half, all of it:** the site file (Phase13), the groups (Phase15), each entry's facts (Phase16), the thumbnails (Phase17), published with digests on GitHub (F-SV-1) | the public launch, with the first versionable release (RD-WS-3); the site itself is the platform's | **Library side complete.** Keep it as the platform's consumer outcome. |
| **Parity Baselines** (*"anyone can see how closely its MaterialX, Blender and Unreal renders match"*) | the rig's pictures in all three tools and the per-port verdict, in every snapshot (F-SV-1) | making the pictures **readable** for a person: *Comparison Pictures in Each Tool* (research, 2026-10-14) | **Fold into *Comparison Pictures*.** Mark it `Reevaluate (2026-10-15)` → superseded, kept. |
| **Release Bundle and Consumer Contract** | publishing on GitHub with a digest; one zip per material; the site file (the dev pre-releases) | the written consumer contract and the trust anchor (its Pass 1 F3); activation without the repo; the master token as data; the compressed textures (the encoder is missing, F-MP-29); **the first real release** | **Narrow it** to what is left; its Pass 1 is kept. |
| **Author a Material End to End** (*"from an idea to a validated material … in minutes, using one tool"*) | `/matter-generate` (Phase03) and `/matter-batch` (Phase11) take an idea to a rigged draft through the agent; a contributor is named in every entry (Phase16); Phase18 lets a contributor craft a fitted part | a **person's** single tool, the Matter Manager; its maintainer half is the console (F-RO-6) | **Fold** its maintainer half into the console and its outsider half into *Contribution Path*. Keep it marked `Reevaluate`. |
| **Contribution Path** | `contributor` in every `.mtlx` (Phase16); the package shape designed (RD-RO-1) | the door, the checks on upload, the outsiders' side | Keep. It builds on Pass 2's server. |
| **The Library Console** | — | everything | Keep. It runs on Pass 2's server, which needs no GPU. |
| **The Library Service** | its Brief, for a rented GPU server | the server | **Re-scope** (Pass 2, Q-SV-1). |
| **Version Management**, **Blender from a Release**, **Unreal Reference Masters**, **Hair That Reads as Hair** | — | everything | Keep. |
| **Skin Maps** | the survey and the probe (`261014_R_SkinMaps.md`); Phase18 builds its base, the body kit and the fitted picture | the six skins re-assembled, the scatter and the calibration (Phase18 §Not now) | Keep. It is next after Phase18 (F-SV-4). |
| **Two Licences** | — | withdrawn (RD-RO-2) | Unchanged: kept, withdrawn. |

**F-SV-3 — Ledger row M9 still reads `OPEN`, although its four items are delivered for the dev snapshots:**
1. the release published on GitHub with its digest;
2. the site file;
3. the thumbnails;
4. the per-port verdict.

What is left is the first real release, not M9's asks. Updating the row is a quick fix.

**F-SV-4 — Two rulings both claim the slot after Phase18.** Neither is resolved here:
- **RD-P18-10**, the lead's *"A on both"* (2026-10-15): *"Skin Maps is its own phase, straight after this one"*, recorded in `Phase18_CharacterLibrary.md`.
- **RD-DS-8** (2026-10-14): *"Phase18 Character Materials, Phase19 Scale Grids"*. The Roadmap's `## Active` lists Phase19 Scale Grids as *"BRIEF READY, after Phase16 – 18"*.

The lead decides which runs next (Q-SV-3).

---

## Pass 2 — Pull the GPU out: what stays local, what goes on a server (design sketch)

**F-SV-5 — Only four jobs need the GPU, and they all stay on the laptop:**
- the rig in Storm, Blender and Unreal;
- the Cycles thumbnails;
- re-running the library when a master, the runtime or a scene changes;
- the AI skin probe, which needs more VRAM than the laptop has, so it stays parked (F-P17-3).

**F-SV-6 — The work around them needs no GPU.** Each item below is in a stub or ruling already; none is new scope:
- **The gate on every push** (`run_all.py`). Automatic CI is parked: the organisation's Actions policy disables every repository (`ToolingConventions.md` §Gates and CI). A server can run the gate on each push and post its verdict. That is the parked CI, without Actions.
- **The inbox for a material package** (RD-RO-1). It checks completeness and runs the gate, then queues the package for a rig run. A refusal names its rule.
- **The review queue and the console** (RD-MP-7): sheet, thumbnails and words side by side; keep or redo, with a note; the wish list; the release composer; the stale list (F-MP-24).
- **Holding the results the laptop sends back,** at web size: sheets, scorecards, thumbnails. Not the ~1 GB of raw output per article (F-P17-3).
- **The release cut:** the lockfile, the freeze, the digests and the GitHub upload. All of it is CPU work. The approval stays the maintainer's act.
- **Knowing what is stale** (F-MP-23): which pictures were made with an older master or runtime.

The dev catalog for the site's staging needs no server: it is a GitHub pre-release (F-P17-5).

**F-SV-7 — The join: the laptop is a worker that pulls, not a host that serves.**
- The server keeps the queue of packages waiting for a rig run.
- When the laptop is on, a worker on it asks the server for work, runs the rig and the thumbnails, and sends the results back.
- **Nothing connects *to* the laptop.** It can be off, travelling or busy. Work waits in the queue and shows in the console as *"checked, waiting for a rig run"*.
- **RD-MP-12 holds as written:** the laptop hosts nothing.
- **A GPU server later is the same worker on another machine.** The Brief's 17.1 (the provisioning recipe) becomes that step. Nothing built now is thrown away (F-RO-17).
- The other Linux GPU machine, the one the Unreal work used, can run the worker too. It contributes work without hosting.

**F-SV-8 — Where the server runs: three options, none of them needing a GPU:**
- **(a) The platform's existing web server,** as the library's own service, deployed from this repo's code and reachable on the team's private network only.
  - It costs nothing new, and is run by the same people.
  - F-RO-10's exclusions hold: no agent session with push rights runs there, and no contributor's code.
  - It keeps the code in this repo, so RD-WS-1's *"the library survives without IMRSV"* holds.
- **(b) A small server of the library's own,** with no GPU, rented by the month. It is separate from the platform's box, at a cost not priced here.
- **(c) GitHub alone:** issues or pull requests as the inbox, releases as the store. It has no compute, because Actions are disabled by policy (F-SV-6), so the gate and the console would still need a machine.

**Recommendation: (a) to start, (b) if it pinches.** The service is a light web app and a queue, and (a) adds no new machine to run. The lead decides whether the library's service may sit on the platform's box (Q-SV-2).

**F-SV-9 — What changes for the phases that waited on a GPU server:**
- ***The Library Service*:** re-scoped to the library's server without a GPU: the gate on push, the inbox, the queue, and the laptop's worker. Its Brief for a rented GPU server is kept, as a later step.
- ***The Library Console*:** runs on it. It no longer waits for a GPU.
- ***Contribution Path*:** opens the same inbox to outsiders, adding accounts and the sandbox question (F-MP-28).
- **Re-running the library** becomes a queue of rig jobs the console can show as stale. The laptop works through it when it has time.

---

## Pass 3 — A draft order (unnumbered; one after the other; for the lead to cut)

*Active today, unchanged: Phase18, Character Materials, then whichever runs next (Q-SV-3).*

- **Skin Maps or Scale Grids, as Q-SV-3 settles:** skin that varies across the body like real skin / swap everything to its scale grid and see at once whether a metre is a metre.
- **The Library Service, re-scoped:** the library's server, with no GPU, checks every push and every material package and queues the rig work, and the laptop works through the queue when it is on.
- **The Library Console:** the team reviews, keeps or sends back, and picks what goes into each version, on one page.
- **Contribution Path:** an outsider submits one package and gets a verdict; only maintainers release.
- **Release Bundle, narrowed:** a consumer relies on a written contract and one verifiable release, without this repo.
- **Version Management:** the next release is cut from the last, and every old one stays reproducible.
- **Blender from a Release:** a Blender user installs the add-on and the library from a release.
- **Unreal Reference Masters:** Studio, or any Unreal user, renders with the masters from a release.
- **Comparison Pictures in Each Tool** (research first), absorbing *Parity Baselines*: a person can read each material's pictures in the three tools side by side.
- **Hair That Reads as Hair** (research): hair that looks like real hair.
- **Skin Maps Beyond Colour** (parked): up close, skin catches the light like real skin.

**The platform's, as consumer outcomes:** *IMRSV Consumes Releases* · *See the Library* (the library side is complete).
**Folded or withdrawn, kept:** *Parity Baselines* → *Comparison Pictures*; *Author a Material End to End* → the console and *Contribution Path*; *Two Licences* (withdrawn).

---

## Pass 4 — The service on the platform's web server: what it takes (2026-10-15)

**The lead, verbatim:** *"Scale grids have started, Skin maps then as you list. So we would run the library service on the same box as IMRSVWeb I presume?"*

- **F-SV-10 — The gate is light enough for a box without a GPU.**
  - `run_all.py` builds its own environment with `uv`, from `pyproject.toml` (Python 3.12, MaterialX 1.39.5 from pip; `ToolingConventions.md` §Entry points).
  - It does not reference the from-source USD toolchain: a grep of `tools/validators/run_all.py` for `USD_TOOLS` and `toolchain` finds nothing.
  - Its encoder lanes SKIP without `compressonatorcli` and say so (§Environment).

  So the server runs the gate with no toolchain build. **Unverified until discovery:** which of the 17 lanes skip there and why. Every skip is reported, never counted as a pass.
- **F-SV-11 — The server needs no git credentials.**
  - The repo is public, so the server reads it with no secret.
  - **The laptop's worker, which already commits, writes the accepted package into git** after the rig, and a push stays the lead's word.
  - The only things on the box are the inbox, the queue, the results at web size, and its place on the team's private network.

  This is stronger than F-RO-10's exclusion: nothing on the box can write to the repo.
- **F-SV-12 — What makes it safe to share the platform's box:**
  - **Its own service, from this repo's code.** It is not part of the platform's app. If it ever pinches, it moves to (b) as the same service.
  - **Private network only.** No public door until *Contribution Path* opens one.
  - **Low priority under the site.** It shares the box with the platform's website, so it runs below it.
  - **No agent sessions and no contributor code** (F-RO-10, F-MP-28).
- **F-SV-13 — It is the platform's box, so it is an ask across repos.** "Host the library's service on the web server" goes in PlatformDependencies as an ask from the library to IMRSV, when the service's discovery opens. The lead owns both repos, so his word settles it. The row records it for the platform's own sessions, which deploy to that box.

---

## Open questions

| Id | Question | Recommendation |
|---|---|---|
| ~~Q-SV-1~~ → RD-SV-2 | **Re-scope *The Library Service* to a server without a GPU** (the gate on push, the package inbox, the queue), with the laptop as a worker that pulls rig jobs (F-SV-7)? | **Yes.** It moves everything that needs no GPU off the laptop now, keeps RD-MP-12, and a GPU server later is one more worker. |
| ~~Q-SV-2~~ → RD-SV-2 | **Where that server runs:** (a) the platform's existing web server, as the library's own service on the private network; (b) a small server of the library's own; or (c) GitHub alone (F-SV-8)? | **(a) to start, (b) if it pinches.** |
| ~~Q-SV-3~~ → RD-SV-1 | **What runs after Phase18:** Skin Maps (RD-P18-10, *"straight after this one"*) or Phase19 Scale Grids (RD-DS-8)? | The lead's call. Scale Grids is small and has its Brief ready; Skin Maps follows on from Phase18's body kit. |
| ~~Q-SV-4~~ → RD-SV-3 | **Tidy the Roadmap to Pass 1** (F-SV-2): See the Library's library side marked complete; Parity Baselines and Author a Material End to End marked folded; Release Bundle narrowed; ledger M9 updated (F-SV-3)? | **Yes, as one quick fix** once Q-SV-1 to Q-SV-3 are cut. |

## Resolved

- **RD-SV-1 — After Phase19 Scale Grids (started), Skin Maps, then Pass 3's order as listed** (the lead, 2026-10-15: *"Scale grids have started, Skin maps then as you list"*). Closes Q-SV-3. It settles F-SV-4's two claims on the slot after Phase18: Scale Grids took it, and Skin Maps follows.
- **RD-SV-2 — *The Library Service* is re-scoped to a server without a GPU, run as the library's own service on the platform's web server, on the team's private network; the laptop pulls rig jobs from it** (read from the lead's question, 2026-10-15: *"So we would run the library service on the same box as IMRSVWeb I presume?"*; restated to him for correction). Closes Q-SV-1 and Q-SV-2 at (a). F-SV-12's conditions bind; (b) stays the exit if it pinches.
- **RD-SV-3 — The Roadmap is tidied to Pass 1 and Pass 3, as a quick fix, and pushed** (the lead, 2026-10-15: *"Tidy the Roadmap as a quick fix and push"*). Closes Q-SV-4.

## Status

- **Passes captured:** 4 (2026-10-15): the audit, the split, the draft order, and the service on the web server.
- **Ruled:**
  - **RD-SV-1:** Phase19 Scale Grids runs now, then Skin Maps, then Pass 3's order;
  - **RD-SV-2:** the service is re-scoped to a server without a GPU, on the platform's web server, on the private network, with the laptop pulling rig jobs. This one is read from the lead's question and restated for correction.
- **Current direction:**
  - the GPU work stays on the laptop;
  - the service, with no GPU, runs the gate on push, the package inbox and the queue;
  - the console follows on the same box;
  - the server holds no git credentials (F-SV-11).
- **Graduated, 2026-10-15 (RD-SV-3):** the lead's *"Tidy the Roadmap as a quick fix and push"*. The quick fix landed:
  - `## Future` reordered, Skin Maps first;
  - *The Library Service* re-scoped in the Roadmap and its stub, with the GPU-server Brief kept as a later step;
  - *See the Library*'s library side marked complete;
  - *Parity Baselines* and *Author a Material End to End* marked folded, and kept;
  - *Release Bundle* narrowed, in the Roadmap and its stub;
  - ledger M9 marked done for the dev snapshots.
- **Open:** nothing in this doc.
- **Next step:** `/discovery` on the re-scoped *Library Service* after Skin Maps. It adds the PlatformDependencies ask (F-SV-13) and measures the web server's headroom.
