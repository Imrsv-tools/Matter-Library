# Phase30 — One Coat on the Opaque Master

**Status:** SEEDED 2026-11-12. The lead numbered it, *"Phase30, open discovery"*, so discovery opens straight after this seed commit.

**Where the ask came from:** the lead ruled on 2026-11-12, on the platform's ticket about what the Matter masters cost to draw, that the Opaque master is built from Substrate's own nodes ("O2"). The platform session handed it to this repo the same day. Its research is private to the platform and is cited here by content, never by id.

## Outcome

**An opaque article in Unreal (paint, porcelain, leather, metal) draws with a single clear coat over its base and matches the OpenPBR reference at least as well as it does today. It also costs less to draw, so Studio can run Substrate at its smaller per-pixel budget.**

Concretely, at close:
- the Opaque master in `build_masters.py` is one dielectric slab and one metal slab, mixed by metalness, under one coat slab;
- the master keeps its name and its Creator Inputs;
- the rig shows it beside Storm;
- a new Unreal test runtime is published.

## Why this is a phase

It reverses a standing choice: Phase06 D6 wrapped Epic's OpenPBR function for every master, and this replaces that for Opaque. It changes what the masters draw at their defaults, so it owes a new runtime. It also carries five mapping questions that each need a ruling or a measured parity check.

## Scope

**In (from the platform's handoff, to be audited in Pass 1):**
- **The new master.** O2 becomes the Opaque master. The prototype switch (`MATTER_MASTERS_OPAQUE`), its told-line suffix and its "prototype / throwaway" wording are removed. The two-function-call Opaque path is removed too, with no dangling function nodes. The master's name and Creator Inputs stay.
- **The prototype's three uncommitted edits (`o2_front`), carried into the phase:**
  - fuzz on the dielectric slab only;
  - F90 left unwired where it is 1;
  - the base's specular IOR under the coat is OpenPBR's `eta_s`.
- **The mapping gaps, each closed or dropped with a recorded reason:**
  - `base_weight` and `base_diffuse_roughness`;
  - the metal's edge tint (`specular_color` as F90, against OpenPBR's F82 tint);
  - anisotropy against Storm;
  - the coat colour through the simple-volume mean free path, against Storm;
  - the coat darkening, which the master computes itself.
- **Parity against Storm** on the grey card and a Copper sweep, at both Substrate budgets (80 B and 160 B). The generated shader keeps a real vertical layer and a linear horizontal mix at 80 B.
- **The docs that change with it:**
  - Phase06 D6 (superseded for Opaque, recorded where);
  - `docs/Learnings/Unreal/Unreal.md` U1–U3;
  - any spec in `docs/specs/` that says the masters wrap Epic's function.

**Not now:**
- TwoLayer, Masked and Emissive keep the two function calls until Opaque holds, then follow (a deferral row in Pass 1).
- The platform's side: pinning the release, cascading into Studio, setting Studio's Substrate budget to 80 B, and re-measuring.
- The coated article's Lumen reflection cost and the first-appearance freeze, both tracked on the platform.
- Copper Verdigris drawing darker than OpenPBR in both masters, which predates O2.

## Rides on

_(discovery pass 1)_

| Row | What in this phase rides it | The peer we follow (file:line, opened) |
|---|---|---|

## Open questions (the seed's, to test against the docs in Pass 1)

1. Does any spec in `docs/specs/` make wrapping Epic's function part of the contract rather than an implementation choice? If so, the reversal is a contract change.
2. Can the rig's Unreal column render at 80 B as well as 160 B, or does the budget need a rig parameter?
3. Which machine runs each step? The build and the runtime publish need the machine with Unreal (`LOCAL_DELTAS.md` §Two machines).
4. Does any gate or cache fingerprint `build_masters.py`, so that this change re-renders published pictures?
5. For each of the five mapping gaps: is it answered by the Blender master (one Principled BSDF, the layout reference), by MaterialX's `open_pbr_surface.mtlx`, or only by a parity measurement?

## Discovery Log

_(numbered passes accrue here)_

## Discovery Status

- **Passes captured:** —
- **Current working direction:** —
- **Open decisions:** —
- **Checks to carry forward:** —

## Execution Log

_(populated during execution)_
