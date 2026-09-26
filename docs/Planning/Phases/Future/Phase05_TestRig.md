# Phase05 — Test Rig: Blender and USDLiveView Side by Side

**Status:** SEEDED (phase doc written 2026-09-26; discovery has not opened). Numbered by the lead, 2026-09-26, verbatim: *"seed Phase05 and Phase06 … we can do all of Phase 5 here, commit and push, then I can move to the other system for Phase 6 … and once we have the UE runtime we can move back here for phase 7 and on."* It takes over the Roadmap's *Parity Baselines* entry. The thinking behind it is `docs/Planning/Research/260926_R_BigPicture_NimbleSetup.md` (Passes 3, 4, 8; rulings BP1–BP9).

## Outcome

**The maintainer can put any material side by side in Blender and USDLiveView, with every slider moved through its range, and see where the two agree and where they drift.**

Concretely, at close: one command renders a material in both tools in the same test scene, across its slider settings, and produces a picture sheet plus a short scorecard. The 7 test materials (below) have been through it. Where they disagree, the cause is either fixed or written down. **The Unreal column exists but is empty,** and the format it will be filled with is written down for Phase06.

## Why this is a phase

The library's whole promise is that a material behaves the same in every tool as its sliders move. That has never been measured (research Pass 1). This phase builds the measuring tool and points it at a small set first, so that design flaws show up on 7 materials rather than 170. Two choices here are expensive to change later: **the render-job format** (Phase06 builds against it on another machine) and **the test scene** (every future result is judged in it).

## Scope

**In:**
- **Check first (about an hour):** does Blender 5.1's USD import bring our MaterialX materials in faithfully, wear layers included? If not, build **Blender versions of the 7 master materials**, one node group each, wear-layer network included. Today's Blender material is a look-alike whose wear sliders do nothing (`tools/generators/matter_proxy.py`), so this is expected to be the biggest piece.
- **The test scene,** made once as a USD file: sphere, rounded cube, a 1 m plane with a ruler, fixed camera. Start with the simplest lighting that can match across tools: one sun, flat ambient light, no tone curve.
- **Matching the lighting first:** the grey card and UV grid must agree between the tools before any material is judged.
- **The render job, written down:** *this material, these slider settings, this scene, write pictures here*. There is one small driver per tool: USDLiveView's renderer (Storm, via `usdrecord`) and Blender (headless). Unreal's slot is defined but empty.
- **The picture sheet and four checks:** colour, size against the ruler, whether each slider does the same thing in each tool, and seams. Add more checks only when a real problem needs one.
- **The status field** (draft, candidate, approved) on each material, so the later build loop can track progress (ruling BP4: names stay `v01`).
- **The 7 test materials:** `GreyCard_Neutral18`, `Copper_Verdigris_Aged`, `Oak_Natural`, `Rust_OnSteel_Flaking`, `Glass_Clear`, `Lace_Floral`, `Neon_Signage`. Between them they cover every master, the wear layers and a two-layer material.

**Out:**
- The Unreal column: **Phase06**, on the UE machine.
- Building new materials and the nightly build loop: **Phase07**.
- Releases of any kind (research Pass 3 item 4).
- Automatic checks on pull requests (Contribution Path, later).

## Open questions (settle during this phase)

- What range counts as "agrees" for each master? Let the first numbers set it, rather than assuming a colour difference under 2 up front. Glossy highlights, glass and subsurface will never match exactly between a path tracer and a real-time renderer.
- Blender: Cycles, EEVEE, or both? Cycles is the more faithful render; EEVEE is what creators see while they work.
- Where rig pictures live: an ignored scratch folder, with a small scorecard kept beside each material (research Q-F)?

## Notes

- **Close = committed and pushed,** so the agent on the UE machine can start Phase06 from a clean clone.
- **The render-job format and the test scene must be documented well enough for Phase06 to build against them without asking.** That is the hand-off between the two machines.
- Keep it small: the rig serves the library, not the other way round.

## Discovery Log

_(numbered passes accrue here: examined → finding → decision / hypothesis / open question)_

## Discovery Status

- **Passes captured:** —
- **Current working direction:** —
- **Open decisions:** —
- **Checks to carry forward:** —

## Execution Log

_(populated during execution)_
