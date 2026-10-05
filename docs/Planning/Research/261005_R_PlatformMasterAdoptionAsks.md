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

## Status

- **Passes captured:** 4 (Pass 1 the platform's asks; Pass 2 the platform's look, run; Pass 3 the library's review; Pass 4 what was built; all 2026-10-05).
- **Current direction.** Not Phase12's work. The three asks, the two things the library added, and two candidates are in the library's builder as switches, each off unless told; the ledger carries the ask as M7. **All of it is built and none of it is run:** this machine has no Unreal. What is owed now is on the system that has it (Pass 4's list). The two things the platform saw are older than this doc: the solid master's missing bend is M6's, now known to be the master and not the capture (MA-F12), with a candidate repair behind a switch; the skin is a look, not a parity fault (MA-F9).
- **Asks:** A1, A2, A3 **built, not run** (`a66377c`). The correction recorded on P20 as owed at its close. The ledger row written (M7, `228bb2f`). *(Was, at Pass 3: "A1, A2, A3 agreed, none built … The ledger row agreed, not written".)*
- **Questions:** MA-Q2 answered (one builder). MA-Q6 answered (separate switches). **Open:** MA-Q1 (a ruling; a candidate is built) · MA-Q3 (a new runtime publish or not, now that the builder has changed; `git log e1fc83e..HEAD -- unreal/MatterRuntime` is no longer empty) · MA-Q4 (the platform's binormal; Pass 4's second step answers it) · MA-Q5 (the skin, against the 2026-09-30 ruling).
- **What was added, and what was not.** Passes 3 and 4, this footer, the check beside this doc, and a dated line in the thin-glass doc's Status. Outside this doc, at the lead's direction: the builder, `unreal/build.sh`'s header, `ToolingConventions.md`, and the ledger. **Not changed:** any article, any spec, the Roadmap, the pinned runtime (`unreal/RUNTIME.json`).
- **Not run.** Everything in Pass 3 is read from the tree. MA-F8 is derived, not seen. MA-F10's sampler rule is Unreal's known behaviour, not tried here. Pass 2 is the platform's look, taken as written. Pass 4's switches have met a stand-in only (MA-F18).
- **Pushed** to the public remote up to `a66377c` (the lead, 2026-10-05: *"push it"*).
- **Pass 5, added from the platform's side (2026-10-05; the lines above are the library's and are not edited):** the consumer switches and `MATTER_MASTERS_REFRACTION=index` are now **run** in a second project on Unreal 5.8 — built, the skinned usages shown both ways, all eight compiled for a static mesh (MA-R6 – MA-R9). **MA-Q4 is answered** (MA-R10: along Unreal's V, so the binormal switch is set). Two notes for the library: the builder's result lines do not reach a caller reading `-stdout` (MA-R11), and P23 needs a consumer's reader to change, not only its copy (MA-R12). **Still owed by the platform:** the look. **Still the library's:** Pass 4's step 4, and MA-Q1, MA-Q3, MA-Q5.

▶ **Next:** on the system with Unreal, Pass 4's four steps. Here, nothing until that look comes back. The solid master's faint, flat colour (MA-F13) and the skin (MA-Q5) wait on the lead.

*(Superseded 2026-10-05 by Pass 4. Was: "two quick fixes, either order. (1) Here: the ledger row, M6 brought up to date, P11 and P17 as reported, the schema line dated. (2) On the machine with Unreal, or written here and proven by the platform's re-run: the switches in the builder. The solid master (M6) and the skin (MA-Q5) wait on the lead.")*
