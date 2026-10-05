# Research — Adopting the library's Unreal masters: what the platform's app needs from the builder

**Opened:** 2026-10-05 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `MA` (ids `MA-Qn`, `MA-Fn`). **Pass 1** is written from the platform's side. The library's review of it against its own tree is a later pass, as in `261005_R_PlatformThinGlassAsks.md`.
**Requested by:** the IMRSV platform's work on how Matter materials look in its Unreal app. Before it re-writes its plugin for the library's masters (`PlatformDependencies.md` P20), it will build them into its own project and look at them in its own renderer, fed by the library's own mapping. Three things stand between the builder as it is and that look.

**Question:** what does a second Unreal project need from `build_masters.py` to draw with the library's masters, on its own meshes?

**Extends, does not replace:** `PlatformDependencies.md` P20 (*"What Studio finds comes back as an ask in this file"*), P11, P17 · `unreal/MatterRuntime/Scripts/build_masters.py` · `docs/specs/Contract/LCDSchema.md` (the consumer naming line under §Author tier) · `261005_R_PlatformThinGlassAsks.md`.

**Public-repo note.** The platform's planning is private. It is summarised here by what it found and what it needs — no platform paths, code or ruling ids.

**Measured at:** `d9f7eb9` (2026-10-05).

---

## The short version

- **The builder writes to one fixed place, for one kind of mesh, on one UV convention.** Each is right for the library's own runtime. A second project needs a say in all three.
- **Until then the platform builds from a patched copy** — three edits, kept beside its own notes, never in this repo. The look it takes with that copy also shows the asked-for variants working, or not.
- **One question, one correction and one note** ride along: how a compressed colour picture is meant to reach a linear sampler; a schema line that stops being true once P20 lands; and two ledger rows that are built on the platform's side.
- **A result owed from the earlier thin-glass asks:** the platform's own thin master, corrected to an index of 1.0 on the Refraction input, was looked at in a live view. Clear glass on a cube, from the side: the pattern behind runs straight, and is still softened by the article's roughness; diamond on the same cube still bends. So `TG-F7` of the thin-glass doc holds when run, on Unreal 5.8 with Substrate.

---

## Pass 1 — What the platform found

*Written from the platform's side, 2026-10-05. Read from the builder; nothing in this repo was run or changed.*

- **MA-F1 — The destination is a constant.** `build_masters.py` writes every master and default texture under `/Game/Masters` (`ROOT`). A project that already keeps masters of its own there, or that wants the library's under a path it can tell apart, has to edit the script.
- **MA-F2 — No usage is set.** The builder sets no material usage, which is right for the runtime's static meshes built in the editor. A character is a skinned mesh with morph targets. In a packaged or `-game` run, a material without those usages falls back to Unreal's default material on such a mesh — grey, with every bind reported as succeeding.
- **MA-F3 — The masters place on un-flipped UVs and flip at the sample.** `place2d` runs on the mesh's `st` with `t` up, and `image_uv` turns the placed coordinate into Unreal's texture space (`(s, 1 − t)`). That is exact for a mesh that still carries USD's `st`. The platform's meshes arrive already flipped once (`v = 1 − t`), as Unreal's own importers leave them. On those meshes the master's flip is a second one, and a rotation or an offset turns the wrong way.
- **MA-F4 — Every sampler is linear, and the runtime decodes colour on the CPU.** P20 already says so. What it leaves open is the compressed case: a colour picture shipped block-compressed carries its sRGB decode in the texture's own flag, which a linear sampler refuses.

## The asks

| # | Need | Why |
|---|---|---|
| A1 | **The builder can be told where to write** — an argument or an environment variable for the package root, defaulting to today's `/Game/Masters`. | MA-F1. One builder for every consumer, as P20 intends, without a fork per project. |
| A2 | **The builder can be told the masters must draw on a skinned mesh with morph targets** — a switch that sets those usages on all eight, off by default if the runtime's shader count matters. | MA-F2. The failure is silent, and it lands on the materials a Creator looks at first: skin, hair, eyes, cloth. |
| A3 | **The builder can be told the consumer's meshes already carry Unreal's V** — a switch under which placement and sampling are consistent for a mesh whose `v` is `1 − t`, giving the same picture as today's masters give on un-flipped `st`. The cut-out and base-colour maps, sampled on the mesh's own `st` without placement, need the same care. | MA-F3. The alternative is every consumer un-flipping its meshes for materials alone, and flipping them back for everything else. |

## Questions for the library

- **MA-Q1 —** How is a block-compressed colour picture meant to reach a master that samples everything as linear (MA-F4)? Decode in the shader behind a per-texture switch, ship colour pictures uncompressed, or something else? The platform's look uses uncompressed pictures, decoded on the CPU as the runtime does, so it does not depend on the answer.
- **MA-Q2 —** For A3, is one set of masters with a switch right, or two builds? The platform has no preference; it needs the pictures to match.

## A correction, and a note

- **The schema's consumer naming line stops being true at P20.** `LCDSchema.md`, under §Author tier, describes the platform's Unreal material instances as naming Creator ports in snake_case and author-tier parameters in PascalCase. Once the platform draws with the library's masters, the names are the masters' own. The line wants removing or re-pointing when P20 closes — not before.
- **P11 and P17 are built on the platform's side.** The ledger lists P11 as open and P17 as awaiting confirmation. By the platform's reading of its own code, both are in its app today: Creator overrides go through the connected carrier, and a card mesh's cut-out map is supplied at binding as the mesh's own. That is a reading, not a test against these rows' every clause; a composition saved by the app is the thing to check them on, and the platform can supply one.

## A suggested ledger row (the library authors it, or not)

> **The Unreal master builder serves a second project** (the platform's finding, 2026-10-05): a destination it is told, usage for skinned meshes with morph targets, and placement that is right for meshes already carrying Unreal's V. The platform looks at the masters in its own renderer from a patched copy first, and reports what it sees. Owner: Matter Library (the builder) · the platform's Unreal plugin (the look; then P20). Pairs with P20 · *Unreal Reference Masters*.

## Pass 2 — The look, run (2026-10-05)

*Written from the platform's side. The eight masters were built into the platform's own Unreal 5.8 project by a copy of `build_masters.py` at `d9f7eb9` carrying exactly the three asks above (A1 – A3) and no sky; each article's values came from this repo's own `article_material`, unchanged; textures were handed over as the runtime hands them (linear 16-bit float, colour decoded on the CPU). The platform's renderer has Lumen lighting and reflections and hardware ray tracing on. One person looked, on a desktop view, at a bench of 16 material panels, metal and plastic balls and cubes, a clothed character, a toy, and a 2 m cube with a patterned cone behind it. No number was taken from a picture.*

- **MA-R1 — The three asks are enough to build and draw.** With them the builder ran against a second project with no other change, every master took skinned-mesh and morph-target usage, and every master compiled with no error at both 80 and 160 Substrate bytes per pixel. Nothing drew as Unreal's default material.
- **MA-R2 — At 160 bytes the bench was judged better than on the platform's own masters.** In the looker's words: *"everything looks really good… Looks better."* A rust article whose mask is a tiled layer at its own real-world size is drawn too coarse by the platform's masters, which read no layer size; the library's masters carry it, but whether that pattern came right was not asked at this look.
- **MA-R3 — The solid see-through master did not bend in this renderer.** Diamond on the cube, from the side, with the cone behind it: *"looks the same as glass."* The platform's own solid master, which wires the article's index straight into Unreal's Refraction input, bends and magnifies on the same cube. So the missing bend the library saw in its own captures (the thin-glass doc's A3) is not the capture: it is there in a live view with reflections and ray tracing on. It points at what the OpenPBR function's refraction output carries.
- **MA-R4 — The thin see-through master read right.** Clear glass on the same cube: *"looks nice."* The looker was not asked to hold a ruler to the pattern behind it; nothing bent enough to be remarked on. That agrees with MA-R3 — if neither master bends, the thin one is right by the same cause that leaves the solid one wrong.
- **MA-R5 — Skin read as plastic.** On the Subsurface master, the character's skin and the skin panel: *"Skin looks like plastic."* The values set were the article's own (subsurface weight 1.0, radius 0.00482 m with the per-channel scale, coat weight 0.1, fuzz weight 0.1). Where it comes from was not looked into — the master, the renderer's settings, or the light. It is the one material class the looker called wrong.
- **80 bytes was looked at too, and *"also looked good"*** — one launch, the same bench; no side-by-side with 160 was made. The platform is taking 160, the library's own setting, since no cost of it showed (below).
- **Not looked at:** anything in a headset; whether a normal map's green reads the right way up on a mesh carrying Unreal's V (ask A3 as worded covers placement — the tangent basis may need the same care, and the platform has not checked).
- **A cost, for the record:** on that desktop view the graphics-card time per frame was about 7 – 8 ms at both budgets (median 7.2 ms at 160, 8.0 ms at 80, over different views) — no cost of the larger budget that this could see.
