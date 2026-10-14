# Phase17 — The Library Service

**Status:** SEEDED (2026-10-14). **Numbered Phase17 by the lead the same day**, ahead of Scale Grids: *"Actually lets pull the library service and thumbnails before Scale grids as well so we can get the entire chain establsihed recategorized, documented and working correctly before we add more materials"* (RD-DS-7). A pointer-shell written by `/research` on the lead's word (*"I like your reccomendation for the library home... I guess that is ALSO a new pahse to seed"*). `/discovery` fills it. **Starting discovery is a deliberate gate, the lead's call, never a slide.**

## Outcome

**The library's work runs on a permanent machine instead of the lead's laptop:**
- the test rig in all three tools;
- the build loop's batches;
- thumbnails;
- the dev catalog the site's staging reads.

The IMRSV team reaches it from wherever they are.

## Why this is a phase

Everything the library does today runs on one laptop (the lead, 2026-10-14: *"that "library machine" is currently this little laptop... this is not setup on a system"*). The flow's second half needs a machine that is always there:
- thumbnails (RD-MP-2 to RD-MP-6);
- the team's console (RD-MP-7);
- the site's staging feed (RD-WS-3);
- the batch loop at volume.

It is one thing a person can see: a batch, a rig run and a thumbnail produced by the service, reached from somewhere other than the laptop.

## Scope — as ruled at research (2026-10-14)

The authority until this phase writes its specs: [`261014_R_MaterialPipeline.md`](../Research/261014_R_MaterialPipeline.md) §Resolved (RD-MP-11) and F-MP-40 to F-MP-42.

- **Independent, with its code in this repo, run by IMRSV** (RD-MP-11). Anyone who forks the library can stand one up, which keeps RD-WS-1's condition 3: *the library survives without IMRSV*. The platform's site and mirror consume what it publishes, and never reach into it.
- **What it runs** (F-MP-40):
  - **GPU work:** the rig in Storm, Blender and Unreal; Cycles thumbnails. This needs a GPU with Vulkan for the Unreal runtime.
  - **The toolchain:** Blender 5.1+, the OpenUSD and MaterialX toolchain (`tools/usd-toolchain/`, a 30–50 minute build), and the pinned Unreal runtime (`unreal/RUNTIME.json`).
  - **The agent's sessions** that run `/matter-batch`.
  - **The dev catalog** (`serve_to_stage.py`) and the thumbnail folder, not in git (RD-MP-6).
  - **Git:** commits to this public repo; pushes on the maintainer's word; approvals stay the maintainer's (`promote_release.py`).
  - **Storage** for renders, thumbnails and staged releases; the compressed-texture encoder (`PhaseTBD_ReleaseBundleConsumerContract.md` F4).
- **Its first tests** (RD-MP-10, the lead): the thumbnail probe (three articles in Cycles: Oak, Glass_Clear, and skin on the clothed character's hand and face), and the skin-map probe (`261014_R_SkinMaps.md`).

## What the lead has said about hosts (2026-10-14)

*"the Other machine is also just a personal machine not a server,,, the only server we currently have is the IMRSV Web server... so we would need to get another serier from Hetzner for this. Now - if it is just to simulate contributors side then this or that can be used"* (`261014_R_MaterialPipeline.md` RD-MP-12).
- **The service needs a new server,** rented from Hetzner, the provider the platform's web server already uses. Hetzner rents dedicated GPU servers. Which model, and its price, is this phase's to check (unverified here).
- **The two personal machines** (the lead's laptop, and the Linux GPU machine the Unreal work used) are **not** hosts. They can stand in for a contributor's machine: running the loop or the rig as an outside contributor would, against the service.
- **The platform's web server is not a host** for the GPU work: it records no GPU (F-MP-41).

## Open questions (settle during this phase)

- **Which Hetzner server:** a GPU model that runs the Unreal runtime (Vulkan) and Cycles; memory and disk for the toolchain, renders and staged releases; and the monthly cost against GPU hours at about 200 articles (F-MP-32).
- **How the team reaches it:** a private network, as the lead tests today, and sign-in.
- **What runs it unattended**, and what still waits for a person: a batch, a review, a push.
- **Packaging:** containers, or a provisioning script on one machine.
- **Cost:** GPU hours for the rig and thumbnails at about 200 articles (F-MP-32).

## What builds on it (not this phase)

- *Thumbnails* (RD-MP-2 to RD-MP-6).
- *The team's console* (RD-MP-7).
- The build loop at volume (`Phase11_LibraryCoverage.md`; Q-MP-12).
- *See the Library*'s staging feed (RD-WS-3).

## Carried in (2026-10-14)

From [`261014_R_RoadmapOrder.md`](../Research/261014_R_RoadmapOrder.md) Passes 3–5, and the order the lead cut the same day:
- **A material arrives as one package, in one upload, tested on upload and taken apart here** (RD-RO-1; the lead: *"they submit one entry per material, then we test on upload and parse as needed (like we do with compositions on web)"*). The package holds the recipe, the `.mtlx` and its textures, provenance, and the words. One command in this repo makes it (F-RO-19).
- **This service makes the pictures on upload,** the rig in all three tools and then the thumbnails, so a contributor needs no GPU (F-RO-20). The order's line for this phase says so; Q-RO-5 keeps the record of the shapes weighed.
- **The web server cannot hold the GPU half** (F-RO-10). Hetzner's GPU machines are dedicated and monthly: the GEX44 is quoted at €184–234 a month plus setup by third parties (unverified, 2026-10-14). Read the real price on hetzner.com.
- **The batch loop submits through the same door** (F-RO-22). **A package carries data, not code** (F-RO-21).
- **Its spec is defined beside the phases above it in the order** (F-RO-12): GPU, its memory, RAM and disk, measured from today's two machines; the price; the setup recipe. Renting is the lead's act.

## Discovery Log

*(empty — `/discovery` fills it)*
