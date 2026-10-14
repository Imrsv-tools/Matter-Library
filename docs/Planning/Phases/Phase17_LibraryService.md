# Phase17 — The Library Service

**Status:** BRIEF READY (2026-10-14), lane **high-rigor**, next **`/plan Phase17`**. **One lead act is open: renting the server (Q-P17-1).** It blocks the first click, not the plan. Discovery opened by the lead: *"/discovery P17"*. **Numbered Phase17 by the lead the same day**, ahead of Scale Grids: *"Actually lets pull the library service and thumbnails before Scale grids as well so we can get the entire chain establsihed recategorized, documented and working correctly before we add more materials"* (RD-DS-7). Seeded by `/research` on the lead's word: *"I like your reccomendation for the library home... I guess that is ALSO a new pahse to seed"* (RD-MP-11). It runs after Phase15 and Phase16, and before Thumbnails (Phase18), which renders on it.

## Outcome

**A person on the team hands the library service one material package, from any machine on the team's private network, and it comes back gated and rigged in Storm, Blender and Unreal, waiting for review. All of this happens on a rented server, not on the lead's laptop.**

The lead's own line for it, from the order he checked and cut (RD-RO-3): *"a contributor uploads one material package, and it comes back tested in all three tools, waiting for review."* The seed's wider list (the rig, the batches, thumbnails, the dev catalog, all on a permanent machine) is kept. This phase delivers the machine, the rig on it and the door into it. What runs on it afterwards is listed under §Not now, with what each item takes from this phase.

## Why this is a phase

Everything the library does today runs on one laptop (the lead, 2026-10-14: *"that "library machine" is currently this little laptop... this is not setup on a system"*). The flow's second half needs a machine that is always there: thumbnails, the team's console, the batch loop at volume and the AI skin-detail probe (RD-SKM-5). Each is built on this one.

---

## The Brief

### First human test

**Where:** a browser on any of the lead's devices on his private network **other than the laptop** (the other machine, or a tablet), at the service's private address, which 17.1 writes into this doc. The agent does every upload from the laptop. The lead only opens pages and judges.

1. **The service's address → `Granite_Polished` → its sheet** *(after 17.1)*. *Judge: all three columns (Storm, Blender, Unreal) were rendered on the server, and the verdict reads* moved alike, *as the laptop's own sheet of the same article does.* The agent gives the laptop sheet's path beside it.
2. **The agent uploads one package of `Slate_Cleft` from the laptop. The service's address → its result** *(after 17.2)*. *Judge: one upload in; out comes the gate's PASS, the sheet and the scorecard, with the article waiting on its own branch for review.*
3. **The agent uploads a package with one texture missing. The service's address → its result** *(after 17.2)*. *Judge: it is refused, and the refusal names the rule it broke.*
4. **The agent runs a one-row batch (`/matter-batch`) on the laptop. The service's address → that batch's review page** *(after 17.3)*. *Judge: the batch was rigged on the server, and the laptop rendered nothing.*

**Can each surface show what is judged?**
- A browser shows a PNG sheet and a text result.
- Both fixtures are clean rows: all three tools *moved alike* on the laptop (F-MP-47). Both have sheets on disk with an `unreal/` column (measured 2026-10-14), so click 1's comparison has a real baseline.
- Every tool the clicks compare runs on the server. Running them there is what 17.1 builds.
- No click needs anything under §Not now.

**Reconciled click by click:**
- Click 1 needs only 17.1.
- Clicks 2 and 3 need 17.2, which uses 17.1's rig.
- Click 4 needs 17.3.
- **The doer for every click is the agent, from the laptop over SSH on the private network, once the lead has rented the box and given it access (Q-P17-1).** No such box exists today, so clicks 1 to 4 wait on that act. `/plan` does not.

### In now

- **17.1 — The rig runs on the server, reached over the private network.**
  - A provisioning recipe in this repo takes a stock Ubuntu install to a working rig:
    - the NVIDIA driver, and an X server on the GPU, so Storm can draw;
    - Blender, pinned to the laptop's 5.2.2;
    - the USD toolchain, through `tools/usd-toolchain/build-usd-tools.sh` as written;
    - `uv`, the clone and its LFS objects.
  - The Unreal runtime downloads itself on the first rig run, from the pin in `unreal/RUNTIME.json`.
  - The box takes no inbound traffic except over the private network.
  - The rig's output folder is shown read-only at the service's private address.
- **17.2 — One package in, a tested result out.**
  - One command makes a material package from an article on disk (F-RO-19). It holds:
    - the article in the complete-portable form `tools/conformance/build_portable.py` already makes;
    - its recipe;
    - its texture provenance records;
    - the contributor's handle, when one is given (RD-RO-2).
  - The package's shape is written as a draft contract spec under `docs/specs/Contract/`.
  - The door: an upload over the private network lands the package in the service's inbox. Each package is checked in a fresh scratch space:
    - its completeness;
    - `run_all.py`;
    - then the rig.
  - A refusal names its rule. A pass is committed to its own branch in the **service's own clone** and gets a review page.
- **17.3 — The batch loop goes through the same door** (F-RO-22). `/matter-batch` on the laptop packages each built row, uploads it, and reads the server's sheet and scorecard for its refine runs. The batch summary records the server's results.
- **At the close:** a ToolingConventions row for the new root; the Glossary's *Library service* entry loses `(planned)`; the Architecture component map gains the service.

### Not now — and what each takes from this phase

| Deferred | Where it goes | What it takes from this phase |
|---|---|---|
| **Thumbnails, made on upload before the review** (RD-MP-2 to RD-MP-6) | Phase18 | the box and its GPU; one more stage in the door's run, after the rig; a git-ignored thumbnail folder on the box, shown at the same address |
| **The team's console** (RD-MP-7) | *The Library Console* | the service's address; the per-upload branch; the review page; the inbox's results |
| **The dev snapshot built on the box** (`build_snapshot.py` reads the rig pictures, which will live there) | the first phase that needs the site fed from the service *(planned)*. Publishing stays the lead's word | the box's `library/parity/` layout, which 17.1 keeps identical to the laptop's |
| **Agent sessions running on the box** (F-MP-40's "agent work") | **Reevaluate (2026-10-14):** F-RO-22 moved the batch loop to the door, so the agent need not run on the box; an agent with credentials on an internet-facing box is its own question | nothing until then |
| **Outsiders uploading:** accounts, a public door, a sandbox for contributed scripts (F-MP-28, F-RO-21) | *Contribution Path* | the package spec and the door's checks, both 17.2 |
| **The AI skin-detail probe** (RD-SKM-5) | *Skin Maps* | the box's 24 GB GPU (F-P17-3) |
| **Re-running the whole library when a master, the runtime or a scene changes** (F-MP-4, F-RO-15) | *(planned)*, likely with the console's stale list | the door's rig stage, run over every article |
| **Containers** (F-MP-42's wording) | **Reevaluate (2026-10-14)**, Q-P17-2 | the provisioning recipe, which a container build can wrap later |

### The reuse check

**What the stack already provides:**
- **The rig, unchanged.** `rig.py` finds Blender by `$MATTER_BLENDER` or `PATH`, Storm by `$USD_TOOLS_ROOT`, and Unreal by the pin, downloaded and checked by sha256. Blender (Cycles) runs headless. The packaged Unreal runtime runs with no display at all (`drivers/unreal.py`: *"a package runs with no display at all, on SDL's dummy driver"*). **Storm does not run headless:** the toolchain's Garch is GLX-only, and `make_preview.py` sets `DISPLAY=:0` (F-P17-2).
- **The toolchain recipe:** `build-usd-tools.sh` and `environment.yml`, as written.
- **The package's core:** `build_portable.py`'s complete-portable form, already used by `build_snapshot.py` for the site's per-article zip.
- **The review page:** `review_pages.py`. **The verdicts:** `wishlist.py`.
- **Private reach:** the lead's private network (Tailscale), already how he reaches his machines (measured on the laptop). It serves a folder to the network's members with no web code of ours and no public listener.
- **The upload:** a copy over SSH on that same network into an inbox, which starts the check. No upload server is written in this phase, because the only uploaders are the team. A public door is *Contribution Path*'s.

**Custom layers this phase adds, each with its gap:**
- The provisioning recipe. Nothing stands up a rig on a fresh machine today.
- The package command and spec. No package exists (RD-RO-1).
- The inbox runner. Nothing runs the gate and the rig on an arrival.

**Standards touched:** `run_all.py`'s contract (the door calls it unchanged); `unreal/RUNTIME.json` (read only). There is no change to the `.mtlx`, catalog or site-file contracts.

### Decisions that bind

**Lead rulings carried in** (quoted where they are recorded):
- **RD-MP-11:** independent, with its code in this repo, run by IMRSV; the platform consumes what it publishes and never reaches into it.
- **RD-MP-12:** a new server rented from Hetzner. The two personal machines are not hosts, and stand in only for a contributor's side. The platform's web server is not a host for the GPU work.
- **RD-RO-1:** one package, one upload, tested on upload and taken apart on the library's side.
- **RD-RO-2:** CC0 only; a contributor's handle is carried as a courtesy.
- **RD-MP-6:** thumbnails never go in git.
- **Push is the maintainer's word** (`LOCAL_DELTAS.md`, *a publishing producer*). **`promote_release.py` is the maintainer's act.**

**Closed here, unless the lead says otherwise:**
- **Q-P17-2 → a provisioning script on one machine, not containers.**
  - Storm's GLX drawing needs a real X server on the GPU, which is plain on the host and fiddly inside a container.
  - A script on a stock Ubuntu install is as forkable as a container file, which keeps *"the library survives without IMRSV"*.
  - This departs from F-MP-42's word *"containers"*. RD-MP-11 adopted F-MP-42's shape: code here, IMRSV runs it, the platform consumes. It did not adopt that one word. Containers stay *Reevaluate*.
- **Q-P17-3 → private network only, no sign-in in this phase.**
  - Nothing on the box listens to the public internet.
  - Team sign-in, possibly with IMRSV accounts, is *The Library Console*'s open question.
- **Q-P17-4 → no push credential on the box.**
  - The service commits each passed upload to a branch in its own clone.
  - The agent fetches that branch over the private network, and pushes from the laptop on the lead's word, as today.
  - The box then holds no key that can publish to this public repo.
- **Q-P17-5 → what runs unattended:** the door's check and rig. **What waits for a person:** the review, the push, any publish and any approval (F-MP-22).
- **Q-P17-6 → cost.** The server is a flat monthly rental, so GPU hours are not billed (F-P17-1).
  - A full rig sweep of ~200 articles at the laptop's measured 3.4–9.6 minutes each is roughly 11 to 32 hours, against about 720 hours in a month.
  - One box is enough. Its real limits are disk and VRAM, both covered in F-P17-3.

### Open: the lead's act

- **Q-P17-1 — Rent the server: a Hetzner GEX45, €214 a month plus €209 setup, excluding VAT** (F-P17-1)?
  - **Recommendation: yes, the GEX45, now,** so it is ready when `/plan` ends.
  - It has three times the laptop's VRAM and four times its RAM.
  - A 96 GB model is for a later need the library does not have yet.
  - **What it blocks:** every click of the first human test (all of 17.1 onwards). `/plan` does not wait on it.
  - **What the agent needs once it is rented:** SSH access to the box from the laptop, and the box joined to the lead's private network. Joining needs an invite or key that only the lead can issue.

### Findings (Pass 1, measured 2026-10-14)

- **F-P17-1 — The server, read from Hetzner's own pages.**
  - **The seed's GEX44 is no longer listed** on Hetzner's GPU matrix (read 2026-10-14). The entry model is now the **GEX45**:
    - an NVIDIA RTX PRO 4000 Blackwell SFF, with 24 GB of VRAM;
    - an i5-13500 with 20 threads;
    - 64 GB of RAM;
    - 2 × 512 GB NVMe;
    - unlimited traffic;
    - Helsinki.
  - **Price:** €214.00 a month, plus a one-time setup fee of €209.00, both excluding VAT (Hetzner's press release of 2026-09-01).
  - The next models up (GEX63, GEX131) carry 96 GB of VRAM. Their prices were not shown on the page.
- **F-P17-2 — Storm needs a display; the other two do not.**
  - The USD toolchain's Garch is GLX-only (`make_preview.py`'s `usd_env`), so `usdrecord` needs an X server.
  - On the box that is an X server on the NVIDIA GPU, not a software one: software GL would make Storm slow and its pictures differ.
  - **Unverified until the box exists:** Storm under that X server; Vulkan for the Unreal runtime on a Blackwell card; Cycles on Blackwell with Blender 5.2.2. 17.1's first act runs all three.
- **F-P17-3 — The laptop's numbers, which size the box.**
  - **The laptop:** an RTX 2080 Max-Q with 8 GB; 12 threads; 15 GB of RAM.
  - **Rig time:** 3.4–9.6 minutes per article per run (batch summaries `261002-*`); Storm is the slowest column (184 s of 5.8 min in `261002-1`).
  - **Disk on the laptop:**
    - the rig's output: 83 GB for ~82 articles, about 1 GB each;
    - the toolchain: 2.2 GB;
    - the Unreal runtime: 1.5 GB;
    - LFS: 1.2 GB.
  - **At ~200 articles:** about 200 GB of rig output plus thumbnails. That fits the GEX45's disks mirrored (512 GB), and needs a pruning rule before the library grows much further.
  - **VRAM:** 24 GB covers the AI skin probe's 16–24 GB, at the top of its range (`261014_R_SkinMaps.md`).
- **F-P17-4 — Nothing is built.** A tree grep for the phase's name finds only the Glossary's *Library service* entry, marked `(planned)`. No prior phase built, deferred or half-built any part of it.
- **F-P17-5 — The site's staging reads a published GitHub pre-release, not a running server** (`build_snapshot.py`, Phase13). So "the dev catalog the site reads" needs no service endpoint. It needs the rig pictures to be where the snapshot is built (§Not now).
- **F-P17-6 — The consumer sweep** (the website's and platform's repos, read at origin; the sibling clones' unpushed commits listed, 2026-10-14).
  - The website's side agrees that the GPU half cannot run on its server.
  - It recommends the console sit beside the library, not in the platform's back office.
  - It offers IMRSV-account sign-in for the team later.
  - No section addressed to the library asks anything of this phase.

### Risk lane — **high-rigor**

**The reason, checked against the tree:** this phase creates a machine with a public IPv4 address, root access and a door that accepts files over a network. Those are the method's **public edge**, **secrets** and **authorization** triggers.

**No control for any of them exists in the tree to read** (F-P17-4). They are all written by this phase:
- the box's inbound rules;
- who may reach the private address;
- what credentials sit on the box;
- what the door does with an arriving zip (paths that escape the scratch space, size, file types).

**Q-P17-3 and Q-P17-4 make the surface small:** private network only, no publishing key. But they are still new controls on an internet-connected machine. `/plan` is where they are specified and tested.

**Lifecycle gates:** the release gates glob `library/releases/`, which this phase never writes. The box's `library/parity/` and inbox are git-ignored.

### Step list

1. **17.1 — The rig on the server.** The provisioning recipe; the private reach; `Granite_Polished` rigged there and opened from another device (click 1).
2. **17.2 — The door.** The package command and its draft spec; the inbox runner; pass and refusal results with review pages (clicks 2 and 3).
3. **17.3 — The batch loop through the door.** `/matter-batch` packages and uploads, and reads results back (click 4).

**Split signal, not cut:** 17.3 is a second journey that can be shown on its own (the loop, not the door). Keep it in unless `/plan` finds the door's result format still moving at the end of 17.2. Then it splits into its own phase, which takes the package command, the upload and the result layout from 17.2.

### Compact build map

- **The new root `service/`**, a peer of `unreal/` and `blender/`:
  - the provisioning recipe;
  - the inbox runner;
  - the box's network and service configuration.
- **The package command:** `tools/releases/`, beside `build_snapshot.py` (it reuses `build_portable.py`).
- **The package spec:** `docs/specs/Contract/`.
- **`/matter-batch`:** `.claude/skills/matter-batch/SKILL.md`, a product surface (ToolingConventions), not methodology. **A sibling session has it modified in the working tree as of 2026-10-14**, so `/plan` re-reads it.
- **Seams to read at `/plan`:**
  - `rig.py`'s tool lookup and its output root;
  - `drivers/unreal.py`'s download into `unreal/package/`;
  - `review_pages.py`'s input;
  - `run_all.py`'s two lanes that skip on the laptop (`LOCAL_DELTAS.md` §Two machines).
- **Test surface:** `/plan`'s, within the high-rigor lane.

---

## Carried in (2026-10-14)

- **From `261014_R_MaterialPipeline.md`:**
  - RD-MP-10: the thumbnail probe is one of the service's first tests. It is now Phase18's first act on this box.
  - F-MP-40: what the service runs.
  - F-MP-41: the web server cannot be the GPU host.
  - F-MP-42: the shape.
- **From `261014_R_RoadmapOrder.md`:**
  - F-RO-10: two jobs never run on a public website's machine: the agent's sessions and contributors' code.
  - F-RO-19 to F-RO-23: the package, the door, data not code, the loop through the door.
  - Q-RO-5: who makes the pictures, (a) the service. The lead: *"I lean toward server option "a""*, then RD-RO-1. **Taken as (a) here, unless the lead says otherwise.**

## Discovery Log

- **2026-10-14 — Pass 1** (`/discovery P17`, at `94a0566`).
  - **Read:** the product docs from `_Architecture.md` down; the two research docs that own the scope; the sibling phases 15, 16 and 18; the Console stub; the consumer repos at origin and their unpushed commits; Hetzner's own pages; the rig's drivers; and measurements of the laptop.
  - **Learnings read:**
    - Unreal U7–U10, headless capture. **U10 binds:** a Shipping package needs glibc 2.28 and runs on SDL's `dummy` driver with no display.
    - Storm S1–S9. **S3 binds the Storm check in 17.1:** one `usdrecord` run is not reliable, so judge the server's Storm column over the rig's repeats, not from one frame. Storm's *"headless `usdrecord`"* means no window. It still assumes an X server (F-P17-2).
    - Blender: not read beyond its index. The box never drives a live Blender (B10–B11).
  - **Distilled into the Brief above.** The seed's open questions are each closed or carried:
    - which server: F-P17-1, and Q-P17-1 for the lead;
    - reach: Q-P17-3;
    - unattended work: Q-P17-5;
    - packaging: Q-P17-2;
    - cost: Q-P17-6.
  - **A sibling session was live in the tree throughout** (Phase15 moving the character articles). This pass touched none of its files.
