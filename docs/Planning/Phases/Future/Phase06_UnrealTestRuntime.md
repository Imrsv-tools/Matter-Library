# Phase06 — Unreal Test Runtime

**Status:** SEEDED (phase doc written 2026-09-26; discovery has not opened). Numbered by the lead, 2026-09-26 (verbatim in `Phase05_TestRig.md`). **This phase runs on the UE machine** (Linux, with its own agent and clone of this repo; rulings BP6, BP7). It starts after Phase05 is pushed. The thinking behind it is `docs/Planning/Research/260926_R_BigPicture_NimbleSetup.md` (Passes 7, 8).

## Outcome

**The test rig's picture sheet gains an Unreal column, rendered by a small Unreal app of our own that runs on any Linux machine with a GPU.**

Concretely, at close: a packaged Unreal 5.8 app (Substrate on) takes Phase05's render job (a material, its slider settings, the test scene) and writes one picture per setting, headless. It carries its own versions of the 7 master materials. The 7 test materials have an Unreal column in their sheets, and the package can be copied to the original machine so all three tools run there from Phase07 on.

## Why this is a phase

It is one thing, the Unreal leg of the rig. It needs a machine with Unreal on it, and nothing else in the plan does. Two choices are expensive to change later: **how the masters are built** (by a script that can rebuild them, or by hand in the editor) and **how the app reads a `.mtlx`**. Both carry forward into the public Unreal package the Roadmap already wants (*Unreal Reference Masters*).

## Scope

**In:**
- **Prove the risky part first:** one grey sphere rendered headless from a packaged Linux build, with Substrate on, giving the same picture every run (auto-exposure off, frames allowed to settle).
- **The 7 masters,** mirroring `docs/specs/Ontology/MasterSet.md`. Every input is a parameter, since a packaged app can't compile new shaders. Ideally they are built by an editor script, so they can be rebuilt rather than hand-clicked.
- **The loader:** it reads a `.mtlx` (which master, which textures, which values, the default slider values), loads the PNGs with the right colour settings (colour textures as sRGB, data textures as linear, the normal map's green channel the right way up), and sets them on the master.
- **The test scene** from Phase05's USD file, and **the render-job driver** exactly as Phase05 wrote it down.
- **The Unreal column** for the 7 test materials, compared in Phase05's picture sheets.
- **The package,** and how it gets to the other machine (it is too large for git).

**Out:**
- IMRSV Studio. Our runtime passing shows the materials can work in Unreal, not that Studio matches; Studio gets an occasional spot check.
- Publishing the masters as a public Unreal package (*Unreal Reference Masters*, later).
- Building new materials (Phase07).

## Open questions (settle during this phase)

- Is Unreal 5.8 available and working on the UE machine's Linux install?
- Real-time rendering or Unreal's path tracer for the comparison renders? The path tracer is steadier; real-time is what users see.
- Where does the package live between machines: a release download, or a copy?

## Notes

- Read Phase05's closed doc first. The render-job format and the test scene are the contract with the other machine.
- Keep the Unreal project in its own folder, and pull before every commit: two machines share this repo.

## Discovery Log

_(numbered passes accrue here: examined → finding → decision / hypothesis / open question)_

## Discovery Status

- **Passes captured:** —
- **Current working direction:** —
- **Open decisions:** —
- **Checks to carry forward:** —

## Execution Log

_(populated during execution)_
