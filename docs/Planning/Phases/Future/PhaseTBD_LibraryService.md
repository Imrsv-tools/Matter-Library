# PhaseTBD — The Library Service

**Status:** SEEDED (2026-10-14) — not numbered. A pointer-shell written by `/research` on the lead's word (*"I like your reccomendation for the library home... I guess that is ALSO a new pahse to seed"*). `/discovery` fills it. **Starting discovery is a deliberate gate, the lead's call, never a slide.**

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

The authority until this phase writes its specs: [`261014_R_MaterialPipeline.md`](../../Research/261014_R_MaterialPipeline.md) §Resolved (RD-MP-11) and F-MP-40 to F-MP-42.

- **Independent, with its code in this repo, run by IMRSV** (RD-MP-11). Anyone who forks the library can stand one up, which keeps RD-WS-1's condition 3: *the library survives without IMRSV*. The platform's site and mirror consume what it publishes, and never reach into it.
- **What it runs** (F-MP-40):
  - **GPU work:** the rig in Storm, Blender and Unreal; Cycles thumbnails. This needs a GPU with Vulkan for the Unreal runtime.
  - **The toolchain:** Blender 5.1+, the OpenUSD and MaterialX toolchain (`tools/usd-toolchain/`, a 30–50 minute build), and the pinned Unreal runtime (`unreal/RUNTIME.json`).
  - **The agent's sessions** that run `/matter-batch`.
  - **The dev catalog** (`serve_to_stage.py`) and the thumbnail folder, not in git (RD-MP-6).
  - **Git:** commits to this public repo; pushes on the maintainer's word; approvals stay the maintainer's (`promote_release.py`).
  - **Storage** for renders, thumbnails and staged releases; the compressed-texture encoder (`PhaseTBD_ReleaseBundleConsumerContract.md` F4).
- **Its first tests** (RD-MP-10, the lead): the thumbnail probe (three articles in Cycles: Oak, Glass_Clear, and skin on the clothed character's hand and face), and the skin-map probe (`261014_R_SkinMaps.md`).

## Open questions (settle during this phase)

- **The host** (Q-MP-11's remainder). The candidates:
  - a cloud GPU instance, started only while work runs;
  - a dedicated machine, starting from the Linux GPU machine the Unreal work used, if it is free (`260926_R_BigPicture_NimbleSetup.md` BP6);
  - a GPU worker on the platform's infrastructure.

  The platform's web server records no GPU (F-MP-41).
- **How the team reaches it:** a private network, as the lead tests today, and sign-in.
- **What runs it unattended**, and what still waits for a person: a batch, a review, a push.
- **Packaging:** containers, or a provisioning script on one machine.
- **Cost:** GPU hours for the rig and thumbnails at about 200 articles (F-MP-32).

## What builds on it (not this phase)

- *Thumbnails* (RD-MP-2 to RD-MP-6).
- *The team's console* (RD-MP-7).
- The build loop at volume (`Phase11_LibraryCoverage.md`; Q-MP-12).
- *See the Library*'s staging feed (RD-WS-3).

## Discovery Log

*(empty — `/discovery` fills it)*
