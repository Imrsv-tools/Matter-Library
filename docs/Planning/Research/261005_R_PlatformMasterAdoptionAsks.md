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

---

## Pass 3 — The library's review: what each item is, how big, and where it can be proven (2026-10-05)

*Written from the library's side, at `65f87a4`. The lead's question, verbatim: "can you pull and see if this is a quick thing to add to 12 or something else". **This machine has no Unreal Engine** (checked 2026-10-05: no `UE` variable, no engine under the home folder or `/opt`; the three pinned packaged runtimes are here). Nothing below was built or run; the builder was read, not changed.*

**Examined:** `unreal/MatterRuntime/Scripts/build_masters.py` (whole) · `unreal/build.sh`, `unreal/RUNTIME.json`, `Config/DefaultEngine.ini`, `Config/DefaultGame.ini` · `MatterRuntimeGameMode.cpp` (`LoadMesh`, `LoadMaster`, `LoadTexture`) · `tools/parity/drivers/unreal.py` (`tangents`, `tangent_signs`, `write_mesh`) · `Phase12_GlassAndLightColour.md` (the Brief, F-GLC-4, the 12.3 row, the two lead calls) · `PlatformDependencies.md` (P11, P13, P16, P17, P20, M6) · `261005_R_PlatformThinGlassAsks.md` (whole) · `Phase06_UnrealTestRuntime.md` (D7, 6.4, 6.5, the close's deferral ledger) · `docs/Learnings/Unreal/Unreal.md` · `docs/specs/Tooling/CompressedDistribution.md` (the role table) · `LCDSchema.md` (the consumer-side line under §Author tier) · `Consumers.md` · the Roadmap.

### The answer to the lead's question

**It is not Phase12's, and it is not one thing.** It is five things of different sizes, and only the smallest can be finished on this machine.

| # | What | Size | Where it can be proven | Home |
|---|---|---|---|---|
| 1 | **The ledger and the two notes:** a row for these asks, M6's row brought up to date with what the platform saw, P11 and P17 marked as reported built, the schema's naming line dated | small, docs only | here, now | a quick fix |
| 2 | **The three switches in the builder** (A1 – A3), off by default, and the rig's Sky left out of a consumer's build | small: about 30 lines in one file (an estimate from MA-F5 – MA-F8, not a diff), and the platform has already run the same three edits | **not here.** Switches on: the platform re-runs its look from the library's builder in place of its copy. Switches off: `unreal/build.sh masters` on the machine with Unreal | a quick fix, on the machine with Unreal or handed to the platform to prove |
| 3 | **The solid see-through master in Unreal:** it bends nothing (MA-R3) and shows its colour faintly and flat (Phase12's F-P12-1). One master, two faults | not known until its cause is read; a repair is a new runtime build | the machine with Unreal | `PlatformDependencies.md` M6, which already holds both |
| 4 | **Skin reads as plastic** (MA-R5) | a look judgement, not a parity fault (MA-F9) | a lit view in Unreal | the lead's call; see MA-Q5 |
| 5 | **A compressed colour picture and a linear sampler** (MA-Q1) | a contract ruling, then a fourth switch of the same shape as A3 | the ruling here; the switch on the machine with Unreal | *Unreal Reference Masters* / the release bundle |

**Why not Phase12:**
- **Phase12 changes no master and builds no runtime.** Its Brief: *"A new Unreal build. None is needed"*, and *"Unreal (`tools/parity/drivers/unreal.py` only) … The masters and the pinned runtime are untouched."* Every ask here is in the builder.
- **Phase12 leans on the builder standing still.** F-GLC-4's evidence is that nothing under `unreal/MatterRuntime` has changed since the commit the pinned runtime was built from (`git log e1fc83e..HEAD`: empty). An edit to the builder makes that log non-empty, even one that changes nothing at its defaults.
- **Phase12 already ruled the nearest item out.** How a renderer draws see-through matter is in its Not-now, and the lead ruled Unreal's weak colour on a solid a follow-up and not that phase's work (2026-10-05, verbatim: *"A, keep going with 12.4"*; the phase doc's RD-P12-2, which the session working the phase had written and not yet committed when this was read).
- **Phase12 is being worked in another session now** (step 12.4, uncommitted work in the tree).

### Findings

- **MA-F5 — A1 is one constant.** `ROOT` is read at six places and written at one. Nothing else in the builder names the destination. The runtime names it twice on its own side (`LoadMaster`'s `/Game/Masters/M_Matter_<Token>` and `DefaultGame.ini`'s always-cook folder); both stay right while the default stays `/Game/Masters`.
- **MA-F6 — A2 is two properties on each of the eight, and off is right for the runtime.** The builder sets blend mode, two-sided and thin-surface, and no usage (MA-F2 holds). The runtime draws only procedural meshes built per job (`LoadMesh`), never a skinned one, so with the switch off its masters are as they are today. What the switch costs is more compiled shaders per master, at cook time and in size; MA-R1 says all eight compiled with it on.
- **MA-F7 — A3's placement half is one helper at two places.** The mesh's coordinate is read at exactly two nodes: the start of `place2d`, and `own_st` (the cut-out and the mesh's picture). Under the switch each first turns the mesh's `(u, v)` back into `st` (`(u, 1 − v)`); everything after is unchanged, so the picture is today's by construction. That covers A3's second sentence too (the maps sampled without placement).
- **MA-F8 — A3 has a second half the ask does not name, and it is not optional: the normal map's green.** The library's normal maps are +Y up (MaterialX). The rig's driver hands the runtime a tangent sign chosen so the binormal is dP/dt, *"the direction a MaterialX (+Y up) normal map's green channel follows"* (`tangent_signs`; `LoadMesh`'s comment). A mesh that carries Unreal's V, with a tangent basis built from those UVs, has its binormal along +v, which is −dP/dt. On such a mesh every bump leans the wrong way up and down unless the switch also negates the tangent-space normal's Y: once, on the sum, before it is normalised, which covers the article's map, the second layer's and the three overlays'. **Derived from the code, not seen:** it depends on how the consumer's meshes get their tangents (MA-Q4), and Pass 2 lists it as not looked at. A flat or softly lit bench would not show it.
- **MA-F9 — MA-R5 is not a fault the rig can see, and the lead has met it before.** In the rig, skin on the Subsurface master agrees with the other two tools (Phase06: the Skin III body 2.62 against Storm, 1.60 against Blender). At that sitting the lead said of all three alike that Unreal *"shoudl make humans look WAY better than the plastic lifeless ting sI'm seeing in storm"* (click 5, 2026-09-30), and then ruled the remark *"a side comment"*, with nothing to follow. Phase06's D7 names the trigger: a dedicated skin profile is added *"only if the column shows a gap"*, and the column, lit evenly with no shadows and no bounce, cannot show one. MA-R5 is the first time the master was seen under real light, by a consumer, with the article's coat and fuzz carried. So the master draws what the article says; what is missing is Unreal's own skin, which the LCD ruling (*"lean in on the egines BEST qaulities"*) allows and nothing has yet asked for. The cause is not looked into on either side.
- **MA-F10 — MA-Q1 is a gap between two of the library's own contracts.** `CompressedDistribution.md`'s role table ships the base colour, the second layer's base colour and the emissive picture as **BC7, sRGB**. P20 says every sampler in the masters is linear. The runtime never meets the two together: it reads the PNGs and decodes on the CPU. A consumer that takes the release's own compressed pictures does. Unreal ties a sampler's type to the texture's colour flag, so the answer is either a colour sampler on the colour slots (a build-time switch, the same shape as A3) or the pictures handed over decoded. Decoding in the shader after a linear fetch filters in the encoded space, which is slightly wrong at every edge. Not run here.
- **MA-F11 — A consumer's build should not write the rig's Sky.** Pass 2's copy carried *"no sky"*, a fourth difference the asks table does not list. `M_Matter_Sky` is the rig's visible dome, not a master (`MASTERS` has eight; `main()` builds nine). It belongs with whatever switch says *"this is not the library's runtime"*.
- **MA-F12 — MA-R3 answers the thin-glass doc's open question, and leaves one state standing.** That doc's TG-F15 had three states that fit the library's pictures. Two of them say the solid master bends in a live view. It does not (MA-R3), so what remains is the first: Epic's function hands the Refraction input something that bends nothing whatever the flag, the thin master is right, the solid master is wrong, and **the rig's Unreal column was truthful.** The platform's own solid master, which wires the article's index straight in, bends on the same cube, so the engine and the scene can bend. *What Epic's function puts on that output is still not read* (TG-Q5); the coloured-transmittance blend mode is the other thing the two solid masters may not share, and it is not ruled out.
- **MA-F13 — The same master carries Phase12's F-P12-1.** `M_Matter_TranslucentThick` shows a solid's see-through colour faintly and does not deepen it with thickness, and it bends nothing. Both are on M6, both need the machine with Unreal, and neither cause is measured. Whether they are one cause is a guess until the function is read (Learnings Unreal T2: `strings` on the engine's function asset gives its inputs and its author's notes).
- **MA-F14 — MA-R1 confirms P20's claim, and MA-R2 confirms P13's.** P20 says the builder writes the eight into *"any Unreal 5.8 project with Substrate on"*; a second project has now done it, with the three edits. The rust that the platform's own masters draw too coarse is the layer size of P13, which the library's masters carry.
- **MA-F15 — "80 bytes also looked good" does not move P20's 160.** What 80 costs was measured as a number, not seen: the dielectric of a two-call master reads 1.14 – 1.39 times too bright against Storm on the grey card (Learnings Unreal U3). A bench looked at once, with no side-by-side, would not show a brightness shift of that size. The platform is taking 160, so nothing follows.
- **MA-F16 — P11 and P17 cannot be closed from here.** Both are reported built by the platform's reading of its own code. The library cannot read that code, and the report itself says it is *"a reading, not a test"*. The check it offers, a composition saved by the app, is one the library can run: `GetValueProducingAttributes()` on each override (P11), and the card's `inputs:cutout_map` set and connected (P17).
- **MA-F17 — The schema line is as the platform says.** `LCDSchema.md`, the consumer-side line under §Author tier: *"the Unreal material-instance naming rule (snake_case reserved for the Creator ports, PascalCase for every author-tier parameter…)"*. The library's masters name every parameter as the article does (Phase06 D5), so the line stops being true for the platform at P20's close, and `Consumers.md`'s *"Parameter naming on the engine side"* row with it. Both want a dated note then, not a deletion.

### The asks, as the library finds them

| # | State after this pass |
|---|---|
| A1 | **Agreed. Small** (MA-F5). The default stays, so the library's own build and its pinned runtime are untouched. |
| A2 | **Agreed. Small, off by default** (MA-F6). |
| A3 | **Agreed, and it is two things** (MA-F7, MA-F8): the placement, which is exact by construction, and the normal's green, which needs a look on a mesh with a strong one-way bump. |
| — | **A fourth, unlisted:** no Sky in a consumer's build (MA-F11). |
| MA-Q1 | **A ruling, not an answer** (MA-F10). The library's leaning: a colour sampler on the colour slots behind a build-time switch, because it is exact and the release already ships the pictures that way. |
| MA-Q2 | **One builder, told what to build.** Each consumer runs it into its own project (P20), so there is one source and no second set to keep. Which build the packaged *Unreal Reference Masters* carries is that package's question, and it is not built yet. |
| The correction | **Agreed, at P20's close** (MA-F17). |
| P11, P17 | **Recorded as reported; the saved composition is the check** (MA-F16). |
| The ledger row | **Agreed.** It is not research's to write. |

### New questions

- **MA-Q3 [lead] — Does a builder edit that changes nothing at its defaults need a new runtime published?** `RUNTIME.json` pins the commit the runtime was built from, and Phase06's rule was *no second publish while nothing under `unreal/` has changed*. After the switches land, something has. The library's leaning: no publish, and the proof is the default build's parameter list unchanged on the machine with Unreal.
- **MA-Q4 [platform] — On the platform's meshes, which way does the binormal run?** Built by Unreal from the flipped UVs (then MA-F8 applies and the switch must negate the normal's Y), or carried in from USD's `st`?
- **MA-Q5 [lead] — Does MA-R5 change the ruling of 2026-09-30?** Then: Unreal's skin at its best was *"a side comment"*, nothing to follow. Now: a consumer, under real light, calls skin the one class that reads wrong on the masters it is to adopt. Both are recorded; neither is resolved here.
- **MA-Q6 — Do A1 – A3 stay three switches, or one** (*"this build is for a consumer"*: its destination, its meshes' usage, its V, no Sky)? The platform's copy carried all four together. Three is more honest about what each does; one is harder to half-set.

---

## Pass 4 — What was built from this, and what the system with Unreal does next (2026-10-05)

*The lead, after Pass 3, verbatim: "Build everything we can build here please so we can get it over to the other system". Done as two quick fixes outside this doc, the same day, and pushed. **Nothing below has been run in Unreal.***

- **The ledger** (`228bb2f`): `PlatformDependencies.md` **M7** is these asks; M6 says the solid master's missing bend is the master; P11 and P17 are marked as reported; P20 records what is owed at its close. The schema's naming line was **not** edited: the platform asked for that *"not before"* P20 closes, so it is recorded on P20 as owed.
- **The builder** (`a66377c`): `build_masters.py` is told what it is building for by environment variable. Its head lists them, and `docs/ToolingConventions.md` repeats the list.

  | Switch | Answers | State |
  |---|---|---|
  | `MATTER_MASTERS_ROOT=/Game/<path>` | A1 | built, not run |
  | `MATTER_MASTERS_SKINNED=1` | A2 | built, not run |
  | `MATTER_MASTERS_MESH_V=unreal` | A3, the placement (MA-F7) | built, not run |
  | `MATTER_MASTERS_MESH_BINORMAL=unreal` | A3's other half, the normal's green (MA-F8) | built, not run, **and worked out, not seen** |
  | `MATTER_MASTERS_SKY=0` | MA-F11 | built, not run |
  | `MATTER_MASTERS_COLOUR_SAMPLER=srgb` | a **candidate** for MA-Q1; the ruling is still the lead's | built, not run |
  | `MATTER_MASTERS_REFRACTION=index` | a **candidate** repair for M6 (MA-F12): the article's index on the solid master, 1.0 on the thin one | built, not run |

- **MA-Q6 is answered by the build: separate switches,** one thing each, so that a mesh with Unreal's V and a carried-in binormal can be told as it is (MA-Q4).
- **MA-F18 — What was checked here, and what that is worth.** `261005_R_PlatformMasterAdoptionAsks_check.py`, beside this doc, runs the builder against a stand-in for Unreal's Python that records every call. With no switch set the builder makes the same 4,436 calls as the builder before the switches, call for call, plus one log line saying what it was told. Each switch changes only its own thing. A value the builder does not know stops it before any asset is made. **That is what the script asks for. It says nothing about what the engine compiles or draws:** the property and enum names (`used_with_skeletal_mesh`, `used_with_morph_targets`, `SAMPLERTYPE_COLOR`, `MaterialExpressionConstant3Vector`'s `constant`) are Unreal's as read, not as run.

### What the system with Unreal does

1. **Build with the switches a consumer needs, and repeat the look of Pass 2** from the library's builder in place of the patched copy:
   `MATTER_MASTERS_ROOT=/Game/<its path> MATTER_MASTERS_SKINNED=1 MATTER_MASTERS_MESH_V=unreal MATTER_MASTERS_MESH_BINORMAL=unreal MATTER_MASTERS_SKY=0`
2. **Look at the normal map's green** on a mesh with a strong one-way bump, lit from the side. If bumps lean the wrong way up and down, build without `MATTER_MASTERS_MESH_BINORMAL`; that answers MA-Q4.
3. **Try the two candidates one at a time.** `MATTER_MASTERS_REFRACTION=index`: diamond on the cube, from the side, should bend, and clear glass should not. `MATTER_MASTERS_COLOUR_SAMPLER=srgb`: a block-compressed colour picture should bind and read the right brightness.
4. **On the machine that builds the library's runtime:** `unreal/build.sh masters` with no switch set, and the *"built …"* log lines' parameter lists unchanged. That is the half of the proof the stand-in cannot give.

---

## Pass 5 — The switches, run in a second project (2026-10-05)

*Written from the platform's side. The builder as it stands at `a66377c`, run unchanged against the platform's own Unreal 5.8.0 project, Substrate on, 160 bytes per pixel. **Built and compiled; not yet looked at.** The look from this build (Pass 4's steps 1 – 3) is still owed, and is the platform's next act. The patched copy is retired: the platform now builds from this builder.*

**What was built.** One run, told `MATTER_MASTERS_SKINNED=1`, `MATTER_MASTERS_MESH_V=unreal`, `MATTER_MASTERS_MESH_BINORMAL=unreal`, `MATTER_MASTERS_SKY=0`, `MATTER_MASTERS_REFRACTION=index`, and a `MATTER_MASTERS_ROOT` of its own (`MATTER_MASTERS_COLOUR_SAMPLER` left at `linear`).

- **MA-R6 — Every switch above builds.** The builder's own lines: *"told root=… skinned=1 mesh_v=unreal mesh_binormal=unreal sky=0 colour_sampler=linear refraction=index"*, then *"RESULT ok"*. Eight masters and the three default textures were written, and no Sky. This is the first run of any of the switches in Unreal.
- **MA-R7 — `MATTER_MASTERS_ROOT` takes a plugin's content path, not only `/Game/<path>`.** The platform keeps the masters in a plugin's own content, so its root is the plugin's mount point. The builder's check (a package path with no trailing slash) accepts it and the assets are written there. The head of the builder says `/Game/<path>`; the wording could say *a package path*.
- **MA-R8 — `MATTER_MASTERS_SKINNED=1` takes on Unreal 5.8, shown both ways.** Setting `used_with_skeletal_mesh` and `used_with_morph_targets` as editor properties works: read back in a second process through `MaterialEditingLibrary.has_material_usage`, both usages are true on all eight. The same build with the switch at `0` and every other switch unchanged: both false on all eight. So the usages come from the switch and from nothing else. That settles MA-F18's worry about those two property names.
- **MA-R9 — All eight compile on a real graphics device with these switches, for a static mesh.** One sphere per master, each an instance fed the way the platform feeds an article, drawn in the platform's app on Vulkan at 160 bytes: the engine compiled each master's shaders on its first draw, and none failed. That includes the two graphs nobody had run: the normal's green turned over (`MESH_BINORMAL=unreal`, all eight) and the index wired to the Refraction input (`REFRACTION=index`, the two see-through masters). **Not covered:** the skinned-mesh and morph-target shader permutations (first compiled when a character is drawn), a master with its textures bound, and anything about how they look.
- **MA-R10 — MA-Q4 is answered: the platform's binormal runs along Unreal's V.** Its meshes arrive with `v = 1 − t`, and the binormal is built from those UVs as they arrive, so it points along `+v`. `MATTER_MASTERS_MESH_BINORMAL=unreal` is the truthful switch for the platform and is set. Whether a bump then reads as a bump is Pass 4's step 2, owed with the look. The masters looked at in Pass 2 were built without it, on the same meshes, and a bump's direction was not looked at there (Pass 2's own list).
- **MA-R11 — A caller that reads the commandlet's output does not see the builder's lines.** The builder's *"told …"*, *"built …"* and *"RESULT ok"* lines are logged at a verbosity that `-stdout` alone does not print; they are in the project's own log file. With `-stdout` the output ends *"Python script executed successfully"* whatever the builder said, and that commandlet exits 0 even when the script raises. Adding `-FullStdOutLogOutput` puts the builder's lines on the output. `unreal/build.sh masters` passes `-stdout` alone and checks nothing. A suggestion, not an ask: the worked example could pass the flag and look for *"RESULT ok"*; the platform's own wrapper now does both, and compares the *"told …"* line with what it set, so a switch that did not reach the build cannot pass as the default.
- **MA-R12 — Phase12's articles, as a consumer met them.** With `emission_color` and `emission_luminance` moved from the shader to the nodegraph's interface, a consumer that reads a light's emission from the shader's input reads nothing and draws the light unlit. The platform's reader did exactly that after refreshing to `707200d`, with every one of its own checks passing, until it was changed to read the interface input; the same had happened one refresh earlier with `transmission_color`. P23's *"(3) Refresh the consumer's copy"* is not enough for a consumer whose reader looks on the shader: it must also read these three off the interface, as it reads every Creator port. Worth a sentence on P23. The three as Creator controls on the platform's side are planned, not built.

**Not done.** The look (Pass 4, steps 1 – 3): the bench beside its reference pictures, a bump under side light, diamond and clear glass on the cube from the side. `MATTER_MASTERS_COLOUR_SAMPLER=srgb` was not tried: the platform serves no block-compressed colour picture today, so it has nothing to bind there. Pass 4's step 4, the default build on the machine that builds the library's runtime, is the library's.

---

## Pass 6 — The look on the library's own builder, and a fault in the carrier check (2026-10-05)

*Written from the platform's side. The masters of Pass 5 (the library's builder, unchanged, with the switches listed there), fed by the platform's own reader from the library as it stands at `707200d`, in the platform's app on Unreal 5.8.0, Vulkan, Substrate at 160 bytes. Desktop only. One person looked, beside Storm pictures of the same bench made from the same library. **This is Pass 4's steps 1 – 3.***

**What was looked at.** A bench of 27 upright panels, one article each, across the opaque classes; a ball and a cube in polished stainless steel and in glossy plastic; a 2 m cube with a gridded cone behind it for the see-through articles; a character in skin, cloth, hair, brows and lashes; a small animated prop. 93 material instances, every one on one of the library's eight masters.

- **MA-R13 — Everything drew on the library's masters, and none failed to compile, the character included.** The engine reported no failed shader compile at the open or after it. That closes two of MA-R9's three gaps: the masters with their textures bound, and the skinned-mesh and morph-target permutations (the character is a skinned mesh with morph targets). The wall of 27, in the looker's words: *"looks good."* The panels were answered as a whole, not one by one.
- **MA-R14 — `MATTER_MASTERS_MESH_BINORMAL=unreal` is seen: a bump reads as a bump.** Slate, leather and rusted steel from a glancing angle, asked whether the bumps read as raised, like the picture, and not dented: *"Good."* So MA-F8 holds on a mesh whose binormal runs along Unreal's V, and the switch does what it says. It is no longer *worked out, not yet seen*.
- **MA-R15 — `MATTER_MASTERS_REFRACTION=index`: the thin master is right; the solid one was not called wrong, and was not called bent.** Frosted glass on the cube from the side, asked whether the cone's grid ran straight and soft: *"yes."* Clear glass: *"glass is great."* Diamond: *"Diamond is strange, but it is fine."* Whether the cone bent behind the diamond was asked and not answered in those words, so the candidate is neither confirmed nor refuted as a repair for the missing bend (MA-R3, MA-F12). It compiles, a thin wall fed 1.0 draws straight, and nothing was said against it. The platform keeps it built.
- **MA-R16 — Two more answers from the same look.** A neon article is lit (the emission pair read off the interface, MA-R12): *"yes."* Skin on the Subsurface master, a second time and in different words from MA-R5: *"there is a silicon doll look to it, it's not shiney but I think it is fine and good place to keep refning from (later)."* An input for MA-Q5, not a new ask. A textured panel from about ten metres does not shimmer.
- **MA-R17 — `tools/conformance/check_lcd_carrier.py` has refused every asset since Phase12, on inputs no asset authored.** Run on four generated assets that reference articles by bare name (stainless steel, glossy plastic, rust, concrete and others), one of which passed this same check at `d9f7eb9`: every Material is refused three times — *"the article declares no NG_\*.inputs:emission_color"*, and the same for `emission_luminance` and `transmission_color` — unless its article declares all three. Two of the four assets author no override of any kind.
  - **What was measured.** On each refused Material, the input has no authored value, its only opinion comes from the article's own `.mtlx`, and no nodegraph declares it. The one override the assets do author (`base_color_tint`, connected, with the `over` on the nodegraph) draws no refusal: it passes all four of the check's rules.
  - **Why, as far as the check's own header says.** The check takes *"every Material input named in the frozen Creator vocabulary"*, and the header notes that usdMtlx *"exposes only the surface shader's inputs on the Material"*. Phase12 added three names to `LCD_PORTS` that are also surface-shader inputs, so every Material now carries those three inputs whether or not anyone overrode them. The header's own definition of an override is *"a value on the bound Material's `inputs:<port>`"*; these carry no value.
  - **What it costs a consumer.** Any gate that runs this check on an asset stops, for most of the library's articles. The platform's own gate now counts a refusal only on a port the asset itself authors, and says how many it set aside; that is a workaround on the platform's side, not a repair.
  - **Not done here.** The check's self-test (`test_check_lcd_carrier.py`) was not run, so whether it sees this is not known. No repair is proposed beyond the observation above: rule 1 fires on an input that is not an override by the header's own words.

**Not the library's, said so that nobody chases it there.** In the platform's app a polished metal reflects the sky and no object in the scene. It is the same on every polished article and it is being looked for in the platform's own renderer. Nothing is asked of the library.

**Not done.** The headset. The solid master's bend, in words that settle it. `MATTER_MASTERS_COLOUR_SAMPLER=srgb`, for the reason Pass 5 gives.

---

## Pass 7 — The library's reply to Passes 5 and 6 (2026-10-05)

*Written from the library's side, at `c40a9bc`. The lead's question, verbatim: "should we do anything and push anything back to them?" This machine has no Unreal, so nothing in Passes 5 and 6 was re-run; it has the USD toolchain, so MA-R17 was. **Nothing was built or changed in this pass.***

**Examined:** Passes 5 and 6 · `tools/conformance/check_lcd_carrier.py` and its self-test · `tools/conformance/check_exporter.sh` · `tools/conformance/build_portable.py` · `tools/converters/assemble_mtlx.py` (its imports and `LCD_PORTS`) · the library's open issue #2 · `PlatformDependencies.md` P23, M6, M7 · `unreal/build.sh`.

### The answer to the lead's question

**Yes: one fault of the library's own to repair, four small things to tidy, and one question to send back.**

| # | What | Whose | Can it be proven here |
|---|---|---|---|
| 1 | **The carrier check refuses every asset** (MA-R17, MA-F19 – MA-F21) | the library's, from Phase12 | **yes**, with the USD toolchain |
| 2 | `unreal/build.sh masters` reports success when the builder raised (MA-R11) | the library's | no; the platform has run the flag |
| 3 | P23 says *refresh the copy*; a consumer whose reader looks on the shader must change the reader too (MA-R12) | the ledger | docs only |
| 4 | Three places still say no switch has been run: the builder's head, `ToolingConventions.md`, M7 (MA-F25) | the library's | docs only |
| 5 | `MATTER_MASTERS_ROOT`'s wording says `/Game/<path>`; a plugin's content path works (MA-R7) | the library's | docs only |
| 6 | **The diamond's bend, in words that settle it** (MA-Q7) | the platform's to answer | no |

### Findings

- **MA-F19 — MA-R17 holds here, and it is wider than reported.** With the pinned toolchain (OpenUSD 26.03), four articles referenced with **no override authored**: Copper, Glass_Clear, Neon_Signage, Diamond. On each, the Material carries `inputs:transmission_color`, `inputs:emission_color` and `inputs:emission_luminance`; each has no authored value, and its only spec is in the article's own `.mtlx`. The check counts three overrides on each and refuses all three.
  - **An article that declares a port does not escape.** Glass_Clear declares `transmission_color`, and is refused for it in different words: *"NG_Glass_Clear….inputs:transmission_color is not connected to it"*. Neon_Signage the same for its emission pair. So Pass 6's *"unless its article declares all three"* is not the limit: no article declares all three, and **every Material on every asset is refused three times.**
  - **A correct override does not help.** Copper with `base_color_tint` set and connected: four counted, three refused.
  - The script is `261005_R_PlatformMasterAdoptionAsks_carrier_repro.py`, beside this doc.
- **MA-F20 — The library did not see it because its own carrier check has not run since before Phase05.** The check imports `LCD_PORTS` from the assembler; the assembler imports MaterialX; the Python the gate runs the check with has `pxr` and no MaterialX. That is the library's issue #2, open since Phase05. Each phase since has recorded the red line as inherited (Phase12's log: *"five carrier checks that all stop at one import"*). Phase12 then gave three Creator ports OpenPBR's own names, which are the names usdMtlx puts on every Material, and the one check that would have gone red could not start. The reproduction above stands a placeholder in for the MaterialX import; nothing in the check calls it.
- **MA-F21 — The repair's shape is measured, not built.** What tells an asset's override from the article's own input is who wrote it: on all four articles the three inputs carry no authored value and no spec outside the `.mtlx`. Both forms of a Creator asset keep the article as a `.mtlx` file (the lightweight form references it; the portable form carries a copy, `build_portable.py`), so *"the asset has a spec on this input, outside the article's `.mtlx`"* separates the two in both. It agrees with the check's own header (*"a value on the bound Material's `inputs:<port>`"*) and with its self-test's *"connect only, no value"* case, which the asset authors. The same change wants issue #2's second option with it, the port list in a module that needs no MaterialX, or the repaired check still cannot run where the library gates. The self-test gains the cases MA-F19 lists. `tools/conformance/` is baselined with `check_exporter.sh` before it is edited.
- **MA-F22 — MA-R11 is taken as an ask, not a suggestion.** A build that prints success after the builder raised is the failure the builder's own refusals were written to prevent: a mistyped switch stops the script, and `build.sh` reports the commandlet's 0. The repair is the flag the platform names and a look for the builder's *"RESULT ok"* line. Not runnable here.
- **MA-F23 — MA-R12 is the reader fault the library met twice itself.** The library's shared reader dropped a graph-routed value at Phase10, and Phase12 repaired it again for these three (*"a shader input connected to a port's output takes the port's value"*). A consumer's reader has the same seam. P23's third clause should say so.
- **MA-F24 — MA-R8 and MA-R13 retire MA-F18's caution for five switches.** `used_with_skeletal_mesh` and `used_with_morph_targets` take, shown both ways; every master compiles with its textures bound and on a skinned mesh; `MaterialExpressionConstant3Vector`'s `constant` compiles and a bump reads as a bump (MA-R14). **Still on trust:** `SAMPLERTYPE_COLOR` and the sRGB default, which nobody has built.
- **MA-F25 — Where the switches stand after Passes 5 and 6.**

  | Switch | State |
  |---|---|
  | `MATTER_MASTERS_ROOT` | run; takes a plugin's content path (MA-R6, MA-R7) |
  | `MATTER_MASTERS_SKINNED=1` | run, shown both ways, drawn on a character (MA-R8, MA-R13) |
  | `MATTER_MASTERS_MESH_V=unreal` | run and looked at (MA-R13) |
  | `MATTER_MASTERS_MESH_BINORMAL=unreal` | run and **seen** (MA-R14). MA-F8 is no longer worked out only |
  | `MATTER_MASTERS_SKY=0` | run (MA-R6) |
  | `MATTER_MASTERS_REFRACTION=index` | compiles; the thin master is right under it; **the solid master's bend is not settled** (MA-R15) |
  | `MATTER_MASTERS_COLOUR_SAMPLER=srgb` | **never built.** The platform serves no block-compressed colour picture, so MA-Q1 has no one waiting on it |

  The builder's head, `ToolingConventions.md` and M7 still say none has been run.
- **MA-F26 — The skin has an answer for now.** The looker, on the Subsurface master under real light: *"it's not shiney but I think it is fine and good place to keep refning from (later)."* That agrees with the ruling of 2026-09-30. MA-Q5 is closed as *later*, with nothing to build.
- **MA-F27 — The default build is still unproven in Unreal.** Pass 4's fourth step, `unreal/build.sh masters` with no switch set, has not been run by anyone. Passes 5 and 6 ran the switches on; the stand-in (MA-F18) is still the only evidence that the unset build is unchanged.

### One question for the platform

- **MA-Q7 [platform] — Does the cone's grid sit in a different place behind the diamond under `MATTER_MASTERS_REFRACTION=index` than under `function`?** Two builds, one cube, one view from the side, the diamond only. *Yes* makes `index` the repair for M6 and the solid master's default, at a new runtime build. *No* means the cause is elsewhere (the blend mode is the other suspect, MA-F12), and the switch stays a candidate. *"Strange, but fine"* does not say which.

---

## Pass 8 — What the library repaired from Pass 7 (2026-10-05)

*The lead, after Pass 7, verbatim: "yes, fix it all and push". Done as quick fixes outside this doc, the same day.*

- **MA-R17 is repaired, and the library's own carrier check runs again** (`c7b963e`, which closes issue #2). The check counts a Material input only where the **asset** authored it: a spec in a layer that is not an article's own `.mtlx`. The port list moved to `tools/converters/lcd_ports.py`, plain data, so the gate's Python can import it.
  - **`check_exporter.sh`, baselined before the edit:** it was FAIL with five lines dead at the import, and is PASS. The four real exports report 1, 0, 0 and 1 overrides, each conforming, and no other line differs.
  - **The self-test** passes under the gate's own Python (23 checks), with new cases against Copper, Glass_Clear and Neon_Signage. Run against the old rule, 12 of them fail, the two original GREEN cases among them: so the test would have gone red at Phase12 had it been able to start.
  - **`run_all.py`:** the summary is the baseline's (15 PASS, 2 SKIP), `determinism` among them, so no article moved.
  - **The rule is in the contract:** `LCDSchema.md` §Carrier rule, *"a Material input is an override only where the asset authored it"*.
  - **One limit, stated in the check's header:** on a flattened copy every spec is in one layer, so the check cannot tell who wrote what. It is run on the asset as authored.
  - **The platform can drop its workaround** and take the check as it now stands. Its own rule (*"a refusal only on a port the asset itself authors"*) and the library's are the same rule.
- **MA-R11:** `unreal/build.sh masters` passes `-FullStdOutLogOutput` and fails unless the builder printed *"MATTER RESULT ok"*. **Not run in Unreal.** Tried against a stand-in engine in three cases: a good build passes; a build whose script raised while the commandlet exits 0 fails; a crashed engine fails.
- **MA-R12:** P23 says a reader that looks on the shader must change, and that a gate going by name finds three overrides on every Material.
- **MA-R7, MA-F25:** the builder's head, `ToolingConventions.md`, M7 and M6 say what has been run, by whom, and what has not. The builder's code is unchanged: the stand-in check beside this doc still passes.

---

## Pass 9 — The unset build, run on the machine that builds the library's runtime (2026-10-05)

*Written from the library's side, on its other machine: the one with Unreal 5.8.0, where the three published runtimes were built. At `7e33015`. The lead, verbatim: "run the default masters build and write it back". This is Pass 4's step 4, and the first run in Unreal of Pass 8's change to `unreal/build.sh`. **Nothing was drawn, and no code was changed:** the builder and `build.sh` are as Pass 8 left them.*

**What was run.** The masters step, four times, against the library's own project (`unreal/MatterRuntime`), with no graphics device (`-nullrhi`):

| Run | How | Told |
|---|---|---|
| 1 | `build.sh masters` | `MATTER_MASTERS_MESH_V=bogus`, a value the builder does not know |
| 2 | `build.sh masters` | nothing. **The run that was asked for** |
| 3 | the commandlet by hand, with `-stdout` and without `-FullStdOutLogOutput` | `MATTER_MASTERS_MESH_V=bogus` |
| 4 | the commandlet by hand, with `-stdout` and without `-FullStdOutLogOutput` | nothing |

**The baseline** is this project's own log of the masters build of 2026-10-01 18:26, made minutes before the commit the pinned runtime names as its source (`e1fc83e`), when the builder had no switch. Nothing under `unreal/` that the builder reads changed between that build and the two quick fixes of today.

- **MA-R18 — The unset build is unchanged in Unreal. MA-F27 is closed.** Run 2: the builder said *"told root=/Game/Masters skinned=0 mesh_v=st mesh_binormal=st sky=1 colour_sampler=linear refraction=function"*, then nine *"built …"* lines, then *"RESULT ok"*; exit 0; no error or warning from Python or from a material.
  - **The nine *"built …"* lines and the result line are those of 1 October, byte for byte:** the same nine assets in the same order, each with the same scalar and vector parameter names (6,269 bytes, one hash for both; see MA-R21 for the one thing that had to be stripped first).
  - **The twelve assets it wrote** (the eight masters, the Sky, three default textures) **are each the same size to the byte as on 1 October.** Their bytes differ. Whether a package Unreal saves again is ever byte-equal was not looked into, so the sizes are a second sign and not a proof.
  - **What this does not show.** It is the engine's own account of what was built, not a picture. Nothing was drawn, the runtime was not packaged, and the rig's Unreal column was not re-run.
- **MA-R19 — `build.sh masters` reports a good build from the builder's own line.** Run 2 ended *"masters: ok. MATTER told root=/Game/Masters skinned=0 mesh_v=st mesh_binormal=st sky=1 colour_sampler=linear refraction=function"*, so the script read both the result line and the line that says what the build was told.
- **MA-R20 — Here a refused switch fails the commandlet itself, so `build.sh` stops before its own check.** Runs 1 and 3: the builder refused (*"MATTER_MASTERS_MESH_V='bogus': want one of ['st', 'unreal']"*), the engine logged *"Python script executed with errors"* and *"Commandlet->Main return this error code: -1"*, and the process exited 255, with `-FullStdOutLogOutput` and without it. No asset was touched: the seventeen files in the masters folder kept their hashes after run 1, and their sizes and times after run 3.
  - **So `build.sh` did fail, which is what matters, and not by the route its comment describes.** It stopped at its `pipefail`, on the commandlet's own exit code. Its look for the result line was never reached: the *"masters: FAILED"* line was not printed, and the temporary log it makes was left behind.
  - **This differs from what the platform saw in its project** (MA-R11: exit 0 and *"executed successfully"* whatever the script did). Why the two differ is not known. Here the refusal is raised as the script is first read, before `main()`; whether a raise later in the build behaves the same was not tried.
  - **The result-line check is not shown wrong. It is shown unreached on this machine.** It stays the guard for the case the platform met.
  - **A tidy, not built:** take the pipeline's exit code into the same test as the result line, so one message and one clean-up cover both routes. Today a failure of the first kind leaves a temporary file per run. *(Built and run the same day: Pass 10, MA-R22.)*
- **MA-R21 — The flag is needed, as the platform said.** Run 4, a good build with `-stdout` alone: exit 0, *"Python script executed successfully"*, and **none** of the builder's eleven lines on the output; all eleven are in the project's log. Run 2, with the flag, printed all eleven. **A trap for whoever compares next:** the project's log file ends each line with a carriage return and the console output does not, so a plain `diff` of one against the other calls every line different.
- **A small thing met on the way.** The docs write the command as `unreal/build.sh masters`. Neither that script nor `unreal/publish.sh` is executable in the repo (both have been mode 644 since Phase06), so it is run as `bash unreal/build.sh masters`.

**What follows.**
- **MA-Q3 has the proof its leaning named** (*"the default build's parameter list unchanged on the machine with Unreal"*). The ruling, publish a new runtime or not, is still the lead's. *(Ruled the same day: no. MA-RD1.)*
- **Pass 4's four steps are all run.** Steps 1 – 3 by the platform (Passes 5 and 6), step 4 here.

**Not done.** A packaged runtime from today's sources. Anything drawn. The solid see-through master's two faults (M6), which also need this machine and wait on the lead. `MATTER_MASTERS_COLOUR_SAMPLER=srgb`, still never built.

---

## Pass 10 — A ruling on the runtime, and `build.sh` takes the exit code (2026-10-05)

*Written from the library's side, on its machine with Unreal, at `69db42d`. The lead, to Pass 9's handback, verbatim: "2) no 3)yes 4)ok 5)ok Push". Item 2 there was MA-Q3, put as: does a builder change that alters nothing at its defaults need a new runtime published? Item 3 was the tidy of MA-R20. The ruling is MA-RD1, under §Resolved. The tidy was built as a quick fix outside this doc and is run.*

- **MA-R22 — `build.sh masters` takes the commandlet's exit code into the same test as the result line. Built, and run in Unreal.** A good build is now both an exit code of 0 and the builder's *"RESULT ok"*; anything else ends in one *"masters: FAILED"* line that says what the commandlet exited with and whether the builder reported, and the script's temporary log is removed.
  - **Against a stand-in engine, four cases, the script before and after** (a test fixture, not Unreal: it prints and exits as each case says):

    | The engine | Before | After |
    |---|---|---|
    | prints *"RESULT ok"*, exits 0 | passes | passes |
    | no result line, exits 0 (what the platform saw) | fails with its message | fails with its message |
    | no result line, exits 255 (what this machine does) | exits 255, **no message, log left** | fails with its message, log removed |
    | prints *"RESULT ok"*, then exits 139 | exits 139, **no message, log left** | fails with its message, log removed |

  - **In Unreal 5.8.0, the library's own project.** `MATTER_MASTERS_MESH_V=bogus`: exit 1, *"masters: FAILED. The commandlet exited 255 and the builder did not report 'MATTER RESULT ok'"*, no log left, and the seventeen files in the masters folder kept their hashes. Nothing set: exit 0, *"masters: ok. MATTER told root=/Game/Masters …"*, the builder's ten lines once more those of 1 October byte for byte, and every asset the same size.
  - **The last row is a case nobody has met.** It is there because the old script would have let the exit code speak alone, and the new one must not let the result line speak alone.

---

## Resolved

- **MA-RD1 — A builder change that alters nothing at its defaults needs no new runtime published (the lead, 2026-10-05).** This is MA-Q3. It was put to the lead with Pass 9's result in hand, as *"does a builder change that alters nothing at its defaults need a new runtime published? The evidence the other machine asked for is now in, and its leaning was no"*; the lead, verbatim: *"no"*.
  - **What it settles.** The pinned runtime stays `unreal-runtime-v3`, built from `e1fc83e` (`unreal/RUNTIME.json`), although the builder and `build.sh` have changed since. Phase06's rule, *no second publish while nothing under `unreal/` has changed*, is read by what the default build makes, not by whether a file moved.
  - **What it rests on.** MA-R18: with nothing set, the builder's lines are those of the build the pinned runtime came from, byte for byte.
  - **What it does not settle.** A change that alters what the default build makes. Making `MATTER_MASTERS_REFRACTION=index` the solid master's default (M6, waiting on MA-Q7) would be one, and is a new runtime build.

---

## Status

- **Passes captured:** 10 (Passes 1, 2, 5 and 6 from the platform's side; Passes 3, 4, 7, 8, 9 and 10 from the library's, the last two on its machine with Unreal; all 2026-10-05).
- **Current direction.** The platform now builds from the library's builder and has retired its patched copy. The three asks and the two things the library added are **run in Unreal and looked at**, by the platform (Passes 5 and 6; MA-F25). Of the two candidates, the refraction one compiles and leaves the thin master right, with the solid master's bend unsettled (MA-Q7); the colour-sampler one has never been built. **What the look turned up is a fault of the library's own, not in the masters:** the carrier check has refused every asset since Phase12, and the library could not see it because that check has not run on its own machine since before Phase05 (MA-F19, MA-F20). *(Was, at Pass 4: "All of it is built and none of it is run … What is owed now is on the system that has it".)*
- **Asks:** A1, A2, A3 **built (`a66377c`) and run by the platform** (MA-R6 – MA-R14). The correction recorded on P20 as owed at its close. The ledger row written (M7, `228bb2f`). **New, from the platform, all done in Pass 8:** the carrier check (MA-R17; repaired and proven here), `build.sh`'s false success (MA-R11; built, not run in Unreal; *run the same day and widened to the exit code, Passes 9 and 10*), a sentence on P23 (MA-R12), the root's wording (MA-R7). *(Was, at Pass 4: "built, not run".)*
- **Questions:** MA-Q2 answered (one builder). MA-Q4 answered (along Unreal's V, MA-R10). MA-Q5 closed as *later* (MA-F26). MA-Q6 answered (separate switches). **Open:** MA-Q1 (a ruling; the candidate is unbuilt and nobody is waiting on it) · ~~MA-Q3~~ **ruled 2026-10-05: no new runtime publish** (MA-RD1; was open until Pass 10, with the proof its leaning named in from Pass 9) · **MA-Q7 (the platform's: the diamond's bend, in words that settle it).**
- **What was added, and what was not.** Passes 3 and 4, this footer, the check beside this doc, and a dated line in the thin-glass doc's Status. Outside this doc, at the lead's direction: the builder, `unreal/build.sh`'s header, `ToolingConventions.md`, and the ledger. **Not changed:** any article, any spec, the Roadmap, the pinned runtime (`unreal/RUNTIME.json`).
- **Not run.** Everything in Pass 3 is read from the tree. MA-F10's sampler rule is Unreal's known behaviour, not tried by anyone. Passes 2, 5 and 6 are the platform's, taken as written. **The unset build is run in Unreal** (Pass 9, MA-R18): its builder lines are those of 1 October, byte for byte. Nothing was drawn from it. *(Was, until Pass 9: "The unset build has met a stand-in only (MA-F18, MA-F27): nobody has run `unreal/build.sh masters` with no switch set".)* Pass 7 ran MA-R17 here and nothing else. *(MA-F8 was "derived, not seen" until Pass 6's MA-R14.)*
- **Pushed** to the public remote up to `a66377c` (the lead, 2026-10-05: *"push it"*).
- **Pass 5, added from the platform's side (2026-10-05; the lines above are the library's and are not edited):** the consumer switches and `MATTER_MASTERS_REFRACTION=index` are now **run** in a second project on Unreal 5.8 — built, the skinned usages shown both ways, all eight compiled for a static mesh (MA-R6 – MA-R9). **MA-Q4 is answered** (MA-R10: along Unreal's V, so the binormal switch is set). Two notes for the library: the builder's result lines do not reach a caller reading `-stdout` (MA-R11), and P23 needs a consumer's reader to change, not only its copy (MA-R12). **Still owed by the platform:** the look. **Still the library's:** Pass 4's step 4, and MA-Q1, MA-Q3, MA-Q5.
- **Pass 6, added from the platform's side (2026-10-05; the lines above are not edited):** **the look is run**, Desktop, on the library's own builder at `707200d` — Pass 4's steps 1 – 3. Everything drew and compiled, the character included (MA-R13); a bump reads as a bump with the binormal switch (MA-R14, so MA-F8 is seen); the thin master is right under `REFRACTION=index` and the solid one was called *"strange, but … fine"*, its bend not settled (MA-R15); skin is still not right and is left for later by the looker (MA-R16). **One thing for the library to act on: `check_lcd_carrier.py` refuses every asset since Phase12** (MA-R17). **Still owed by the platform:** the headset. **Still the library's:** Pass 4's step 4, MA-R17, and MA-Q1, MA-Q3, MA-Q5.

- **Pass 7, the library's (2026-10-05):** MA-R17 is reproduced here and is wider than reported: every Material on every asset, whatever its article declares (MA-F19). Its cause on the library's side is issue #2 (MA-F20), and the repair's shape is measured (MA-F21). Nothing built.

- **Pass 8, the library's (2026-10-05):** everything in Pass 7's table that is the library's is done (`c7b963e` and the commit that carries this line). The carrier check is repaired and proven on this machine; the exporter gate passes, having been red since at least Phase05's close, when issue #2 was filed; issue #2 is closed. `build.sh`'s change is not run in Unreal. *(Run the same day: Pass 9.)*

- **Pass 9, the library's, on its machine with Unreal (2026-10-05):** `unreal/build.sh masters` with no switch set is run, on Unreal 5.8.0, in the library's own project. **The unset build is unchanged** (MA-R18: the builder's nine *"built …"* lines and its result line are those of 1 October, byte for byte; the twelve assets are the same sizes), so MA-F27 is closed and MA-Q3 has the proof its leaning named. `build.sh` reports a good build from the builder's own line (MA-R19), and the flag it now passes is needed (MA-R21). **One thing differs from what the platform saw:** on this machine a refused switch makes the commandlet itself fail, so `build.sh` stops at its `pipefail` and never reaches its own check (MA-R20). It still fails. Nothing was drawn, and no code was changed.

- **Pass 10, the library's, on its machine with Unreal (2026-10-05):** **the lead ruled MA-Q3: no new runtime publish** for a builder change that alters nothing at its defaults (MA-RD1, §Resolved). `build.sh masters` now takes the commandlet's exit code into the same test as the result line, so every failure ends in one message and leaves no log behind (MA-R22): four cases against a stand-in, then a refused switch and a default build in Unreal 5.8.0.

▶ **Next:** nothing is owed by the machine with Unreal. **From the platform:** take the repaired carrier check and drop the workaround; answer MA-Q7 (the diamond, with the switch and without). **Waiting on the lead:** MA-Q1, and the solid master's two faults (M6, MA-F13), which need the machine with Unreal when they are taken up.

*(Superseded 2026-10-05 by Pass 10. Was: "nothing is owed by the machine with Unreal. From the platform: take the repaired carrier check and drop the workaround; answer MA-Q7 (the diamond, with the switch and without). Waiting on the lead: MA-Q3 (a new runtime publish or not; the proof is in, Pass 9), MA-Q1, and the solid master's two faults (M6, MA-F13), which need the machine with Unreal when they are taken up. Small and unbuilt: `build.sh` taking the commandlet's exit code into its own test (MA-R20).")*

*(Superseded 2026-10-05 by Pass 9. Was: "nothing here. From the platform: take the repaired carrier check and drop the workaround; answer MA-Q7 (the diamond, with the switch and without). On the machine that builds the library's runtime: `unreal/build.sh masters` with no switch set, which proves the unset build (MA-F27) and the script's new result check in one run. The solid master's faint, flat colour (MA-F13), and MA-Q1 and MA-Q3, wait on the lead.")*

*(Superseded 2026-10-05 by Pass 8. Was: "here, one quick fix: the carrier check counts only what an asset authored, the port list moves where the check can import it (closing issue #2), and the self-test gains the cases; with it the small things of Pass 7's table (rows 2 – 5). Then push, so the platform can drop its workaround. From the platform: MA-Q7. On the machine that builds the library's runtime: the unset build (MA-F27). The solid master's faint, flat colour (MA-F13) waits on the lead.")*

*(Superseded 2026-10-05 by Pass 7. Was: "on the system with Unreal, Pass 4's four steps. Here, nothing until that look comes back. The solid master's faint, flat colour (MA-F13) and the skin (MA-Q5) wait on the lead.")*

*(Superseded 2026-10-05 by Pass 4. Was: "two quick fixes, either order. (1) Here: the ledger row, M6 brought up to date, P11 and P17 as reported, the schema line dated. (2) On the machine with Unreal, or written here and proven by the platform's re-run: the switches in the builder. The solid master (M6) and the skin (MA-Q5) wait on the lead.")*
