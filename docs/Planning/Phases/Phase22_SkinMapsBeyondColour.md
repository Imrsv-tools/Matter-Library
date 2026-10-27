# Phase22 — Skin Maps Beyond Colour

**Status:** ACTIVE (IN DISCOVERY) — **BRIEF READY, with one lead question open (Q-P22-2, raised by the lead at the session's `/retro`)** (Pass 2, 2026-10-27: the lead answered Q-P22-1 by rejecting Blender as the look surface and proposing the library's Unreal test runtime, RD-P22-11). Numbered Phase22 on 2026-10-27 as discovery opened (the lead: *"/discovery Phase22 Skin Maps Beyond Colour"*). It was the head of `## Future` after the 2026-10-27 re-sequence (RD-CMT-3), and F-CMT-9 laid out the numbering. Seeded 2026-10-14 by `/research` (the lead: *"Seed a phase TBD..."*, then *"Full skin map set"*). Parked the same day (RD-DS-8, *"skin detail stay parked TBD"*) and un-parked 2026-10-26 (RD-SYN-3, *"3) yes"*). Until 2026-10-27 the doc was `Phases/Future/PhaseTBD_SkinMapsBeyondColour.md`.
**Lane:** `build` (§Risk lane). **Next:** the lead answers Q-P22-2, then `/execute P22`.
**Measured at:** `49da20e`, on **the machine with Unreal**: Unreal 5.8 at the path `unreal/build.sh` takes as `UE`, and the official Blender 5.2.2 as `MATTER_BLENDER` (Learnings B22).
**Builds on:** *Skin Maps* ([`Phase21_SkinMaps.md`](Complete/Phase21_SkinMaps.md)), which shipped the colour map. **Research:** [`261014_R_SkinMaps.md`](../Research/261014_R_SkinMaps.md) (the survey, F-SKM-11 … 18) · [`261026_R_SyntheticSkinAndEyes.md`](../Research/261026_R_SyntheticSkinAndEyes.md) (RD-SYN-3) · [`261027_R_CharacterMaterials.md`](../Research/261027_R_CharacterMaterials.md) (the order, RD-CMT-1 … 4, F-CMT-9).

## Outcome

**Up close, a character's skin catches the light as real skin does:** fine wrinkles and creases, oilier and drier areas, and light glowing through ears and fingers. This works in Blender, a USD viewer and Unreal, for every character built from the approved human mesh.

*(Verbatim from the seed. The glow through ears and fingers sits behind a probe (RD-P22-7). If it cannot be carried, it is deferred with a dated `(planned)` mark, never cut from the Outcome.)*

---

## The Brief

### What this phase builds, in one paragraph

The six fitted Fitzpatrick skins, and their lips, get **shine maps** on `MakeHuman_Body_v01` (hm08's atlas). The library makes the maps **in 3D** (the 2026-10-26 rule), and one set is **shared by all six tones** (RD-P22-2). They arrive in order:
1. **roughness** (an oilier forehead, nose and chin; drier cheeks);
2. **relief** (a normal map for creases and wrinkles, and a cavity map that dims the shine in them);
3. **thickness**, if its probe finds a way to carry it (RD-P22-7).

Each map is a **new input in the material contract** (an author-tier input, lane B). It copies `base_color_map`'s shape: it is read on the mesh's own UVs, and a fitted Character article carries its own value. **Its neutral default draws today's skin**, so a consumer that does not read it loses nothing. The tiling `Skin_Pores` stays as the micro layer and is combined with the new maps.

Every tool runs on the machine with Unreal:
- Storm draws the article itself;
- Blender reads the maps through `load_article.py`;
- Unreal through `build_masters.py`, built and run here as a local package; `unreal-runtime-v7` is published at the lead's word.

The look is judged in **a shadowed look view added to the library's own Unreal test runtime** (RD-P22-11), the same Unreal, Substrate and masters Studio builds from. Tool agreement is judged on the rig. **Studio** sees the maps once the platform carries them (a ledger row filed at 22.1, F-P22-8).

### First human test

**Where:** the machine with Unreal; every tool the clicks compare runs there (F-P22-3).
- **The look: the library's Unreal test runtime, in a new shadowed look view** (RD-P22-11). It adds a side key light with shadows, a fill and a rim, a neutral dome, and fixed exposure, with the renderer set as close to Studio's as the runtime allows (read from the platform at execute). Its cameras are the face (front and three-quarter), the back of the hand, and a backlit ear, on the rig's hm08 character. **Today's skin and the new one are rendered side by side into a look sheet**, which the agent opens with `xdg-open`; the path goes in the handback. It is the same Unreal, Substrate and masters Studio builds from (F-P22-8).
- **Tool agreement:** the rig's sheet (`face`, `hand`) in Storm, Blender and Unreal, in the rig's matched light. Storm runs at 512 px on this machine (Storm S11).
- **The agent drives every tool; the lead looks and judges.**

1. **Roughness, one tone (22.1).** Fitzpatrick IV in the look view, today's beside it. *First, before any map: today's skin alone in the look view, as the baseline* (the lead: *"(or show me)"*).
   - *Judge:*
     - the forehead, nose and chin catch a brighter, tighter highlight than the cheeks;
     - the even sheen is broken;
     - the tone is unchanged;
     - **does it still read as plastic?**
   - **Can the surface show it?**
     - The key light puts a highlight across the forehead and one cheek. The rig's matched light has no shadows and cannot show it (RD-CMT-4's reason).
     - The face gets about a 441-pixel square of the atlas (F-SKM-26), and the oily zones span tens of those pixels. The look view renders above the rig's 512 px; Storm's 512 px limit (S11) does not apply to Unreal.
     - The fixture is the rig's own hm08 character, the mesh the platform builds from.
     - **The roughness map's average over the skin is neutral** (RD-P22-4), so the tone and the overall shine stay as they are, and only their spread changes.
2. **Relief (22.2).** The same tone, with the normal and cavity maps added.
   - *Judge:* the creases at the eyes, the fold from nose to mouth, the knuckles and the lip lines catch and lose the light, and the shine dims inside them. Nothing reads as painted-on shading. The relief runs across the lip edge with no seam (RD-P22-8).
   - **Can the surface show it?** The key light grazes the face and the back of the hand. The creases are drawn at the scale of millimetres to centimetres, which the 441-pixel face carries. The pores stay finer than a pixel at this framing, which is correct (F-P21-1).
3. **Light through ears and fingers (22.3), only if its probe passes** (RD-P22-7).
   - *Judge:* in the backlit-ear camera, the ear and the fingertips glow warm at their thin edges, more than today's.
   - **Can the surface show it?** The look view's backlit camera, today's beside the new. The probe also measures Blender's response for agreement.
4. **Six tones, three tools (22.4).** The rig's sheet: `face` and `hand` for Fitzpatrick I to VI, today's beside the new, in Storm, Blender and Unreal; and the look sheet for the six tones.
   - *Judge:* every tone takes the same shine, and the three tools move alike.
   - **The agent's evidence, in the 22.4 log:** the rig's Moved verdict per tone, the roughness map's average over the skin (neutral to within 1 %), and G8 on every map.
5. **Pictured (22.4).** The thumbnail sheet: the six skins' `face` and `hand` and the six lips' `lips`, beside today's.
   - *Judge:* skin you would pick from a card.

**Reconciled click by click:**
- Click 1 needs 22.1 only: the look view (and its baseline), the maker's roughness map, the input in the contract, the gates, IV's skin and Unreal's builder. Blender's and Storm's halves of 22.1 are the agent's evidence (the rig on IV), not a click.
- Click 2 needs 22.2.
- Click 3 needs 22.3, and only if its probe passes.
- Clicks 4 and 5 need 22.4.

**Not a click: Studio.** Studio sees the maps once the platform carries them (the ledger row filed at 22.1; F-P22-8) and judges them in its own look-dev scene when that exists (P33). That sitting is the platform's and does not hold this phase's close (RD-P22-12).

### In now

| Item | Step |
|---|---|
| **The shine-map maker:** a fit converter beside `gen_skin_maps.py`, computing in 3D on hm08 (the 2026-10-26 rule), writing each map and its provenance (RD-P22-10) | 22.1 (roughness), 22.2 (normal, cavity), 22.3 (thickness, if its probe passes) |
| **The inputs in the contract** (RD-P22-3): `roughness_map`, `normal_map` and `cavity_map` as author-tier lane-B inputs on Subsurface. Each in LCDSchema, the assembler (`AUTHOR_TIER_PORTS` and the Subsurface wiring), `lcd-as-input`, the recipe schema and G8's rule for a data map | 22.1 (roughness), 22.2 (normal, cavity) |
| **Fitzpatrick IV's skin and lips** wearing the maps (RD-P22-8), re-assembled in place at `v01` | 22.1, 22.2 |
| **Blender:** `load_article.py` reads each map on the mesh's UVs as non-colour data and combines it as the contract says | 22.1, 22.2 |
| **Unreal:** `build_masters.py` samples each map on the mesh's own UVs with a neutral default, and `drivers/unreal.py` wires it. Built and packaged here, and run by the rig as a local package | 22.1, 22.2 |
| **The runtime's shadowed look view** (RD-P22-11): the runtime's game mode lights a job asking for it with a key light that casts shadows, a fill and a rim, and turns on the shadows its matched light turns off. The rig asks for it and writes a look sheet, today's beside the new. Rebuilt and packaged here. **Its first picture is today's skin, the baseline** | 22.1 (first) |
| **The thickness probe** (RD-P22-7), then the map and its input if it passes | 22.3 |
| **All six tones and lips** wearing the shared maps; the rig's sheet over six tones | 22.4 |
| **Thumbnails re-made** (every kept one: the masters' hash moves with `load_article.py`, F-P22-6); the dev install re-served | 22.4 |
| **Written down:** LCDSchema (the new inputs, a section of their own), `SkinMaps.md` (*colour only, for now* becomes the shine maps, with how to make one), the Glossary (*shine map*), and Learnings where a trap is found | 22.4 |
| **Ledger:** a row asking Studio to carry the three maps (F-P22-8), filed as soon as `roughness_map` is in the contract, so a platform session can work alongside. Its id is claimed when it is written | 22.1 |
| **`unreal-runtime-v7`** and a dev snapshot, each at the lead's word, with `HEAD` pushed | 22.4 |

### Not now

- **The pores faded at grazing angles and masked by region** (the platform research's two-normal recipe): a master change of its own, beyond carrying the maps. → §Deferred.
- **A face map of its own, or a larger atlas** (F-SKM-26): the 2048² atlas stays (RD-P21-5).
- **Wrinkle maps driven by expressions:** the platform pushes face-shape weights to the material. A later phase that would consume this phase's `normal_map`.
- **The 15 synthetic drafts:** *Synthetic Skin Sets* re-makes them, and they pick up the shared maps there.
- **The marks' own relief** (a raised mole or a papule; the lead: *"lack any depth"*): this phase adds the inputs, and the per-mark relief is *Skin Layers*'.
- **A different skin scatter model** (CMT Pass 2: *"not a switch, master work with its own diagnosis"*).
- **The AI detail layer** (RD-SKM-5, RD-SYN-1).
- **The shine maps on the other masters** (Opaque, Masked, Hair): added when an article needs one (RD-P22-3).
- **Studio's side:** the platform's, through the ledger.
- **A release:** *Release Bundle*.

### The reuse check

*What does the stack already provide, and which contracts are touched?*
- **The shape of a mesh-supplied input already exists:** `base_color_map` (LCDSchema §Base colour map). It is a `filename` interface input, sampled on texcoord 0 directly (not through `place2d`), with a neutral image default. A fitted Character article names its own value (RD-P18-9), and a binding's value wins (the Carrier rule). It ships in all three tools. **Each new input copies it**, so no new mechanism is invented.
- **The way to combine two normals already exists:** the overlays add their XY to the article's normal in tangent space and normalise once, before the single `normalmap` (Learnings M1; MasterSet). The body normal joins the pores' normal the same way, in every master that already does it.
- **Cavity needs no new shader input:** `specular_weight` is an `open_pbr_surface` input that every master already carries (F-P22-4).
- **The 3D rasteriser exists:** `gen_synth_skin.py` gives every hm08 texel its 3D position, normal and concavity, in numpy. The pinned MPFB2 region masks and `sss.png` are already read by both makers (`gen_skin_maps.py`).
- **The fitted article, its part mesh, `fits` and G8:** Phase18 built them; Phase21 used them.
- **The rig passes an article's own maps on generically** (`job.Article.own_maps`). Storm needs no wiring, and data maps already stay raw, which is right (Storm S10).
- **Thumbnails** on the atlas, for fitted articles (Phase21 `50ed85b`).
- **The look view needs no new renderer:** the runtime already spawns a sun and a sky light and turns their shadows off on purpose, to match the rig (F-P22-11). The look view is those lights with shadows on, plus a fill and a rim, chosen by the job.
- **Contracts touched:** LCDSchema's author tier gains three inputs, added the way `cutout_map` and `base_color_map` were added. Every article that does not declare them assembles byte-identically. **No Creator port, name, type or range moves.**
- **New code:** the maker; one branch per map in the assembler, Blender's loader and Unreal's builder; the drivers' wiring; G8's rule for data maps; the runtime's look view and its sheet. **Nothing replaces a native behaviour.**

### Decisions that bind

*One authoritative copy. Rulings quoted where they are the authority.*

**Carried rulings:**
- **RD-SKM-1:** one approved mesh, hm08, as `MakeHuman_Body_v01` (RD-P18-1); maps are made per mesh version.
- **RD-SKM-2, RD-SKM-5, RD-SYN-1:** no photograph or scan of a person, and AI makes no whole map. **RD-RO-2:** *"material are CC0"*.
- **RD-SKM-4:** plain skin at the genitals and groin. It holds for every map: no relief there either.
- **Authored on the body, baked per layout** (the lead, 2026-10-26, `SkinMaps.md`): the shine maps are made in 3D. The maker may read the pinned MPFB2 masks the makers already read; moving those onto the body stays the spec's Todo, for *Synthetic Skin Sets*.
- **RD-P18-9:** a fitted Character article carries its own pictures. **RD-P21-1:** one article carries the tone and its maps.
- **RD-P21-3:** the colour calibration is unchanged; this phase does not touch `base_color_map`.
- **RD-P21-5:** the atlas stays 2048².
- **RD-P21-6** (the lead, *"a,"*, on an option that read *"un-park … next, with its roughness map first"*): roughness comes first.
- **RD-SYN-3** (*"3) yes"*): un-parked. **RD-CMT-3:** the order of the character phases.
- **RD-CMT-2** (*"usable on all the chars - not made for ONE character"*): maps on the approved mesh, placed by anatomy, pass the inclusion test by construction.
- **RD-CMT-4** (*"5) yes"*): the look verdict for a character material is made in the platform's shadowed look-dev scene; the rig stays the tool-agreement check. That scene does not exist yet and Studio cannot draw these maps yet (F-P22-8), so this phase judges in the library's own Unreal look view (RD-P22-11), and the Studio verdict follows (RD-P22-12).
- **The LCD principle** (the lead, 2026-09-28: *"we use the master materails to lean in on the egines BEST qaulities"*): a value one viewer ignores is still authored, and agreement is judged on the nod. It is the bar for the thickness probe.
- **Pre-release, no versioning** (`AI_WorkingAgreement.md` §Settled practices): the twelve articles are rebuilt in place at `v01`. None is in a frozen release (`library/releases/*.lock.yaml`, grepped 2026-10-27).

**Decided here, unless the lead says otherwise:**
- **RD-P22-1 — The order: roughness, then relief (normal and cavity), then thickness.**
  - **Why:** F-P21-1 measured the plastic as the even sheen, and RD-P21-6 adopted roughness first.
  - The industry adds the wrinkle normal before roughness (F-SKM-11). Here the micro normal already exists (`Skin_Pores`) and the sheen is the measured fault.
- **RD-P22-2 — One shared set for all six tones.**
  - These maps describe the surface, not the tone; even the six colour maps turned out to be one picture (F-P21-10).
  - Each is named by what it is, not by a tone. A contributor can still give one tone its own map, by pointing that article at another file.
  - RD-SKM-3 (one map per tone) is about colour's hue and does not bind a map without one.
- **RD-P22-3 — How each map is carried.**
  - **Names:** `roughness_map`, `normal_map`, `cavity_map` (and thickness's, named by its probe). `_map` is the mesh's picture and `_tex` the article's tiling one, as with `base_color_map` and `base_color_tex`.
  - **Shape:** each copies `base_color_map`. It is a lane-B author-tier `filename` input, sampled on texcoord 0 directly, as **linear data**. A fitted Character article names its own value; in any other article it is empty, and a binding's value wins.
  - **Defaults:** each image's default is neutral (grey 0.5, a flat normal, white), so a consumer that does not read the input draws today's skin.
  - **On the Subsurface master only** for now: the skins and lips are Subsurface. Other masters take a map when an article needs one.
- **RD-P22-4 — Roughness is an offset around 0.5.**
  - It is added to the pores' roughness before the Creator's `roughness_bias` and the clamp: `clamp(pores + (map − 0.5) + bias)`.
  - **Its average over the skin is held at 0.5**, so the article's measured roughness (Physically Based's 0.5, the pores' mean) stays its average. This is RD-P21-3's discipline, applied to shine.
  - **Why not a multiplier:** an 8-bit map cannot go above 1, so a multiplier could only make skin glossier.
- **RD-P22-5 — The body normal is combined in tangent space** (+Y up, MaterialX's convention).
  - Its XY is added to the pores', as the overlays' is, then normalised once before the single `normalmap` (M1).
  - The pores keep their 1 cm tile.
  - The tangent frame is the mesh's, from texcoord 0. A consumer needs MikkTSpace-compatible tangents (the ledger row).
- **RD-P22-6 — Cavity multiplies `specular_weight`** (1 on open skin, lower in creases and pores at body scale).
  - It adds no colour: the colour map's creases are already darker (Phase21's AO bake).
- **RD-P22-7 — Thickness sits behind a probe.**
  - OpenPBR has no thickness input (F-P22-4). The probe tries the candidate carriers on IV, backlit, in Blender and Unreal.
  - **It passes** if a carrier moves Blender and Unreal the same way at the ears and fingers. Storm's per-pixel subsurface may barely move (F-SKM-18); that is recorded, as scatter anisotropy is (Storm S8), under the LCD principle.
  - **It fails** if no carrier does that. Then the glow is deferred with a dated `(planned)` mark, and 22.4 proceeds.
- **RD-P22-8 — The lips carry the normal and cavity maps and keep their own roughness.**
  - The relief runs across the lip edge, and the lips keep their finish (RD-P21-2).
  - The nails wear no map (their own part).
- ~~**RD-P22-9 — The shadowed close-up's builder is a tracked script under `tools/parity/scene/`.**~~ *Superseded 2026-10-27 by RD-P22-11: the look surface is the Unreal runtime's look view, not a Blender scene.* What survives: the look surface is tracked code, not a `/tmp` script (F-P22-9), because the next four character phases judge in the same light until Studio's look-dev scene can show their pieces (P33).
- **RD-P22-10 — The maker is the library's, and in 3D.**
  - It reuses `gen_synth_skin.py`'s rasteriser and the makers' pinned MPFB2 masks, and adds no new picture drawn on the atlas.
  - It writes its provenance into `library/provenance/sources/fit/makehuman/skin.yaml`.
  - A contributor's own map painted on the atlas is accepted, bound to its layout, as for colour (`SkinMaps.md`).
- **RD-P22-11 — The look is judged in a shadowed look view in the library's Unreal test runtime** (Pass 2; answers Q-P22-1).
  - **The lead, verbatim (2026-10-27):** *"I think trying to judge if it look plastic in studio using Blender is not the way... Also... why not update our UE matter test tool to use the new maps first and shoe screensshots from that? (or show me)"*.
  - *The reading:* Blender is not the look surface, and option (a) is withdrawn. The look surface is the runtime the rig already drives, given a look view with shadows, which shows today's skin first, then each map.
  - **Why it stands in for Studio better than Blender:** it is Unreal with Substrate, running the masters Studio builds from the library's own builder (F-P22-8).
  - The rig's matched, shadowless light is unchanged and stays the tool-agreement check. The look view is a separate view a job asks for.
- **RD-P22-12 — The close does not wait for Studio** *(unless the lead says otherwise)*.
  - Studio needs platform work per map (F-P22-8) and a look-dev scene that does not exist yet (P33). The library files the ask at 22.1, so the work can run alongside.
  - The Studio sitting is the platform's, recorded in the ledger, as Studio's side did not hold Phase21's close.

### Risk lane — `build`

The controls this phase touches, each read on 2026-10-27:
- **The contract** (LCDSchema §Author tier): an additive lane-B input, the way `cutout_map` (Phase07) and `base_color_map` (Phase09) were added, both in the build lane. No authorisation, secret, destructive migration or public edge is involved.
- **`run_all.py`** (baseline at `49da20e`: see the Discovery Log):
  - **`lcd-as-input`** checks every interface input against `LCD_PORTS ∪ AUTHOR_TIER_PORTS`. The new names go into `assemble_mtlx.py`'s `AUTHOR_TIER_PORTS`, or the material lane refuses them.
  - **`determinism`** re-assembles every article byte-identically, so the articles are re-assembled by the tool, never by hand.
  - **`provenance_gate`** covers every texture under `MatterLibrary/textures/`. Each map's provenance is owed in `skin.yaml`.
  - **The recipe gate:**
    - **G1** refuses an unknown recipe key, so the schema learns each map.
    - **G8** is keyed on `base_color_map_tex`. It demands an RGB PNG "read as sRGB", and judges coverage by the background colour (F-P22-6). A data map needs its own rule there: the format it is, linear, and coverage that a neutral island does not fail. That is a rule in an existing gate, not a new gate.
  - **Release lanes:** none of the twelve articles is in a frozen lock.
- **`blender/masters/load_article.py`:** a master loader, not `blender/addons/`, so no `check_exporter.sh` baseline is owed (`LOCAL_DELTAS.md`, the RUN row). **But the masters' hash moves,** so the snapshot refuses every thumbnail made on the old masters, and they are all re-made at 22.4 (Phase21 re-made 57).
- **`unreal/MatterRuntime/Scripts/build_masters.py`:**
  - **At its defaults the master draws as before** (neutral images), so the build alone owes no runtime (the lead, 2026-10-05).
  - Showing the maps in Unreal outside this machine needs `unreal-runtime-v7`. `publish.sh 7` publishes a public asset: the lead's word, with `HEAD` pushed.
  - Unreal's Subsurface master samples 9 textures today; three or four more stay under 16 (F-P22-5).
  - Before any launch, check `ps -ef | grep "[U]nrealEditor"` (the lead's Studio shares this GPU).
- **The runtime's C++** (`unreal/MatterRuntime/Source/MatterRuntime/MatterRuntimeGameMode.cpp`): the look view is a lighting choice the job makes. **A job that does not ask for it lights exactly as today**, so the rig's matched light and every past verdict stand. This is a C++ change, so it needs `build.sh editor` (compiled with its capped job count) as well as `masters` and `package`. The defaults check is the rig on a Matter article and on IV before and after, compared to v6.
- **The tracked Asset-Browser library** (`blender/asset_library/MatterLibrary.blend`): it has only ever been regenerated on the library machine. If 22.4 needs it regenerated, ask first.
- **Publication:** a dev snapshot and a runtime, each at the lead's word. **Data:** nothing is deleted.
- **Content:** no map carries anatomy (RD-SKM-4). Thumbnails show only the face, hand and lips (RD-MP-3).
- **Shared box:** `serve_to_stage.py` restarts the Stage daemon. Close what is opened, by PID, and say so in the handback.

### Step list

- **22.1 — Roughness, one tone, end to end:** Fitzpatrick IV's skin, oily and dry by region.
  - **First, the runtime's look view, and today's skin in it** (the baseline picture).
  - The maker's roughness map, and `roughness_map` in the contract, the assembler and the gates.
  - Unreal's builder and Blender's loader, with Unreal built and packaged here.
  - The ledger row asking Studio to carry the three maps.
  - The rig on IV in all three tools, as the agent's evidence.
  - **Click 1.**
- **22.2 — Relief:** the normal and cavity maps and their inputs, on IV's skin and lips. **Click 2.**
- **22.3 — Light through thin parts:** the thickness probe, then its map and input if it passes; otherwise a dated deferral. **Click 3, if built.**
- **22.4 — Six tones, pictured, served, written down.**
  - The other five skins and six lips wear the shared maps; the rig's sheet over six tones.
  - Every kept thumbnail re-made; the dev install re-served.
  - The specs, the Glossary and the ledger row.
  - `unreal-runtime-v7` and a dev snapshot, at the lead's word.
  - **Clicks 4–5.**

### Compact build map

- **22.1:**
  - **The maker:** a new fit converter in `tools/converters/fit/` (named at execution). It uses `gen_synth_skin.py`'s per-texel 3D position, normal and concavity, and `gen_skin_maps.py`'s pinned masks. It writes `MatterLibrary/textures/fit/makehuman/skin/<map>_sUKN.png`, named by NamingConventions' fit-set grammar, and its provenance in `skin.yaml`.
  - **The contract:**
    - `docs/specs/Contract/LCDSchema.md`: the author-tier rows, and a section beside §Base colour map.
    - `tools/converters/assemble_mtlx.py`: `AUTHOR_TIER_PORTS`, and the Subsurface branch's roughness wiring (an `image` on texcoord 0, added before `roughness_biased`).
    - `tools/validators/validate_material.py` (it reads the union).
    - The recipe schema, and G8 in `validate_recipe.py`.
  - **Recipes:** `Skin_FitzpatrickIV_*.json`. Then `build_proof_subset.py`.
  - **Blender:** `blender/masters/load_article.py`, beside its `base_color_map` block. `blender/masters/article.py` skips the new render-role `*_map_tex` names, as it skips `base_color_map_tex`.
  - **Unreal:**
    - `build_masters.py`: `texture(g, "roughness_map_tex", <grey>, own_st, …)` added into the roughness before the bias.
    - `tools/parity/drivers/unreal.py` wires the port.
    - Build with `UE=~/Documents/Unreal/Linux_Unreal_Engine_5.8.0 bash unreal/build.sh masters`, then `package`.
    - Run the rig with `MATTER_UNREAL_RUNTIME=$PWD/unreal/MatterRuntime/Packaged/Linux/MatterRuntime.sh`.
    - Keep a copy of a `MATTER built …` log first, for the defaults check.
  - **The look view:**
    - `MatterRuntimeGameMode.cpp` / `.h` read a lighting choice from the job: the look view's key light with shadows, fill and rim, and shadows on. Without the choice, today's matched light.
    - `tools/parity/JOB_FORMAT.md` (the field), `tools/parity/job.py` (the look cameras: face front and three-quarter, the back of the hand, a backlit ear) and `tools/parity/drivers/unreal.py`.
    - A look sheet, today's beside the new, from the existing sheet tools (`pair_sheet.py`).
    - Today's articles re-assembled from `HEAD` into the git-ignored `library/parity/P22_today/`, as Phase21 did.
    - Build: `UE=… bash unreal/build.sh editor`, then `masters` and `package`.
  - **The ledger row:** `docs/Planning/PlatformDependencies.md`, written from F-P22-8's list, by content.
  - **Smoke:** `uv run tools/parity/rig.py --character Skin_FitzpatrickIV_Clean_Base_s001_v01`.
- **22.2:** the same for `normal_map` (added to the tangent-space XY before `normal_out_unit`) and `cavity_map` (× `specular_weight`). The recipes for `Lips_FitzpatrickIV_*.json` too.
- **22.3:** the probe, run on IV in scratch (never committed), backlit, in Blender and Unreal. Then the same wiring as above, or the deferral written into `SkinMaps.md` and §Deferred.
- **22.4:**
  - the other ten recipes;
  - `rig.py --character` per tone, and one sheet;
  - `tools/thumbnails/` for every kept thumbnail;
  - `serve_to_stage.py` (then close Stage);
  - `LCDSchema.md`, `SkinMaps.md`, `docs/Glossary.md`;
  - the ledger row brought up to date with what shipped;
  - at the lead's word: `unreal/publish.sh 7`, `unreal/RUNTIME.json`, `build_snapshot.py --publish`.
- **Test ceiling (build):** existing tests and units for the maker: the roughness map's average over the skin is neutral; the normal map decodes to unit vectors, flat where it should be; every island is covered. One real-path smoke: the rig on the character. G8's data-map rule is a rule in an existing gate. **No new gate or lane.**

### Open for the lead

1. **Q-P22-2 — Test the skins in Studio directly?** *(Raised by the lead with `/retro`, 2026-10-27, after Pass 2, verbatim: "And irt sounds like we just test the skins in studio directly?". Recorded at the run's end, not resolved: it may reverse RD-P22-11 and RD-P22-12.)*
   - **What "Studio directly" takes** (F-P22-8): per map, the platform re-runs its masters build from this repo's builder, has Stage carry the map as it carries `base_color_map`, binds it as linear data with a neutral default, and, for the normal map, builds MikkTSpace-compatible tangents. Then a shadowed look-dev scene to judge in (P33), which does not exist yet. All of it is platform work in its own repo.
   - **(a) Studio is the look surface, and this phase waits for it.** The library builds the maps and the inputs; each look click is sat in Studio once the platform has carried that map. The runtime's look view (RD-P22-11) is dropped, or kept only as the agent's own early check. The close waits on the platform (RD-P22-12 reversed). The ledger row at 22.1 becomes the critical path.
   - **(b) The runtime's look view first, Studio as the last click.** As Pass 2 has it, with one added click at the end: the six tones in Studio, once the platform has carried the maps. The close waits for that click.
   - **(c) As Pass 2 has it.** The runtime's look view is the phase's look surface, and the Studio sitting is the platform's, after the close.
   - *Not yet recommended by the agent:* the session ended at `/retro`. The next session puts it to the lead, with (b) as the likely middle: no step waits on another repo, and the product surface still has the last word.


- ~~**Q-P22-1 — Where is this phase's look verdict made?**~~ → **RD-P22-11.** The lead rejected (a), the shadowed close-up in Blender: *"trying to judge if it look plastic in studio using Blender is not the way"*. They proposed the library's Unreal test tool instead: *"why not update our UE matter test tool to use the new maps first and shoe screensshots from that? (or show me)"*. (b), waiting for Studio, is decided against by RD-P22-12, unless the lead says otherwise.

---

## Findings (discovery Pass 1, 2026-10-27)

- **F-P22-1 — The skin today, re-verified** (`Skin_FitzpatrickIV` recipe and article, read 2026-10-27).
  - Its roughness and normal come only from `Skin_Pores`, a 1 cm tile through `place2d`, with roughness 0.46–0.56 around 0.5.
  - Its coat is 0.1 at 0.3; no input at body scale exists.
  - F-P21-1's measurement stands: fine-scale contrast under 2 grey levels in all three tools, an even sheen.
- **F-P22-2 — Every map beyond colour is a new input (the seed's claim, re-verified).**
  - `assemble_mtlx.py`'s `AUTHOR_TIER_PORTS` holds `opacity_cutoff`, `cutout_map`, `base_color_map` and the layer-2 set, and nothing for shine.
  - LCDSchema's lane rule asks one question: *does OpenPBR have an input for it?* A picture on the mesh's UVs never is one, so each map is lane B.
  - The pattern to copy is `base_color_map` (RD-P22-3).
- **F-P22-3 — The machine with Unreal runs every tool this phase compares.**
  - Unreal 5.8 is installed at `build.sh`'s `UE` path. The masters build in about a minute, and a package in under a minute when only the masters change.
  - The rig takes a local package through `MATTER_UNREAL_RUNTIME`.
  - The official Blender 5.2.2 renders parity through `MATTER_BLENDER` (B22).
  - **Storm draws the character only at 512 px here** (S11), so a close look at a pore is not Storm's.
- **F-P22-4 — What OpenPBR offers each map.**
  - **Cavity:** `specular_weight` is an `open_pbr_surface` input in every target: Blender's master has a `Specular Weight` socket, fed to Principled's *Specular IOR Level*; Epic's OpenPBR function in Unreal takes it; Storm reads it natively.
  - **Thickness:** OpenPBR has no input for it. F-SKM-18 (2026-10-14) still stands: no thickness input was found on Unreal's Substrate slab, and Storm's subsurface moves no light between pixels.
- **F-P22-5 — Unreal's Subsurface master samples 9 textures today**, counted in `build_masters.py`: the mask set, base colour, roughness, metalness, normal, `base_color_map` and three overlays. Three or four more stay under Unreal's 16 per material.
- **F-P22-6 — The gates a new map passes through:**
  - the recipe schema (G1 refuses an unknown key);
  - G8 (keyed on `base_color_map_tex`; *"a fitted picture is an RGB PNG (read as sRGB; no alpha)"*; coverage judged against the background colour);
  - `lcd-as-input` (the `AUTHOR_TIER_PORTS` union);
  - `provenance_gate`;
  - `determinism`.
  - **The thumbnails' masters hash** moves with `load_article.py`, so every kept thumbnail is re-made before a snapshot (Phase21 21.3).
- **F-P22-7 — The rig already carries an article's own maps.**
  - `job.Article.own_maps` returns every `filename` input with a value, and `maps_for` puts them on the binding.
  - Each driver still wires each port.
  - `MAP_COLORSPACE` marks only `base_color_map` as sRGB, so data maps stay raw, which is right (Storm S10).
- **F-P22-8 — What Studio needs to see a new map** (read at the platform's origin, 2026-10-27, recorded by content; `LOCAL_DELTAS.md` §Separation). *Corrected in Pass 2: Pass 1 read the ledger's P20 `OPEN` as "Studio draws with masters of its own".*
  - **Studio already draws Matter with the library's masters.** The platform builds them into its own project by running this repo's `build_masters.py` (M7), and binds textures by the library's slot names (`base_color_map_tex`, `roughness_tex`, …). That was seen on Desktop in the platform's Matter-in-Studio work (2026-10-05). P20 stays `OPEN` for its close notes.
  - **So per new map, the platform:**
    1. re-runs its masters build from the library's updated builder, which gives Studio's masters the new slots;
    2. has Stage read the map from the article (the article's own value, or the binding's) and send it to Studio, through the same places `base_color_map` passes through today;
    3. binds the new slot as **linear data** in the plugin, with the neutral default when an article has none (as it already does for a missing normal);
    4. **for the normal map:** builds MikkTSpace-compatible tangents, or a baked normal map will not match the other tools.
  - **To judge the look in Studio:** a look-dev scene for characters (P33). None exists on the platform yet (searched 2026-10-27).
  - **The platform's character research** (2026-10-25 … 26) lists the shine maps as owed under every route, and describes skin that reads as skin as a roughness map, a specular or cavity map and a face normal, with the tiling pore normal faded at grazing angles.
- **F-P22-9 — Phase21's sitting scene is not on this machine.** It is in the library machine's git-ignored `library/parity/P21_Sitting/`, and its builder was a `/tmp` script that was not kept. → RD-P22-9, superseded by RD-P22-11.
- **F-P22-10 — The sweep for consumer rulings found nothing newer than the 2026-10-27 order.**
  - The platform's docs, fetched 2026-10-27, have no character commit after 2026-10-26, and CMT already read the character research through its last pass.
  - In this repo, the only later mention of this phase is the CharSkins retro's numbering question, which this invocation answers.
- **F-P22-11 — The library's Unreal runtime turns its shadows off on purpose** (read 2026-10-27).
  - `MatterRuntimeGameMode.cpp` spawns a sun and a sky light with shadows off, turns off dynamic and contact shadows, Lumen's light and its reflections, and casts no shadow from the mesh. `Config/DefaultEngine.ini` says why: matched lighting (`tools/parity/JOB_FORMAT.md`).
  - So its pictures cannot show plastic today, and a shadowed look view is a lighting choice added beside the matched one, not a new renderer.

## Deferred

| What | To | What it consumes from this phase |
|---|---|---|
| The pores faded at grazing angles and masked by region | a master change, `(planned)` | `normal_map`'s combination with the pores (RD-P22-5) |
| A face map of its own, or a larger atlas | a later question on the same mesh version (RD-P21-5) | the maker; G8's size rule |
| Wrinkle maps driven by expressions | a later phase, with the platform pushing face-shape weights | `normal_map` and its combination |
| The 15 synthetic drafts wearing the maps | *Synthetic Skin Sets* | the shared maps; the three inputs |
| A mark's own relief and shine | *Skin Layers* | the `normal_map` and `roughness_map` channels, and how they combine |
| Studio wearing the maps, and the verdict in its look-dev scene | the platform, through the ledger (the row filed at 22.1; P33); does not hold the close (RD-P22-12) | the three inputs as LCDSchema states them; the articles as served; `unreal-runtime-v7`'s Subsurface master |
| The glow through thin parts, **only if 22.3's probe fails** | a dated `(planned)` mark in `SkinMaps.md` | the probe's record |

## Depends on

- **Nothing outside this repo, for every click** (RD-P22-11, RD-P22-12). Studio's sitting follows the platform's work on the 22.1 row and P33.
- `unreal-runtime-v7` and the dev snapshot are the lead's word, with `HEAD` pushed.

## Discovery Log

- **2026-10-27 — Numbered and Pass 1** (the lead: *"/discovery Phase22 Skin Maps Beyond Colour"*).
  - **Numbered Phase22** in its own commit (`49da20e`). The doc moved from `Phases/Future/`, the Roadmap entry to Active, and two live links were re-pointed.
  - **Read:**
    - the seed;
    - `_Architecture.md` (the LCD principle and decisions of record);
    - LCDSchema §Author tier, §Carrier rule, §Cut-out map, §Base colour map and §Render-role textures;
    - `SkinMaps.md`;
    - Phase21's doc in full;
    - the research `261014_R_SkinMaps.md` (F-SKM-4, 11 … 18), `261026_R_SyntheticSkinAndEyes.md` and `261027_R_CharacterMaterials.md`;
    - the platform's character research, at its origin;
    - Learnings M1, M4, S8–S11, U3, U11, U14, B8, B10, B11 and B22.
  - **Read in the tree:**
    - `Skin_FitzpatrickIV`'s recipe and article;
    - `AUTHOR_TIER_PORTS`;
    - G8 (`validate_recipe.py`);
    - the rig's `own_maps` and `maps_for`;
    - the Unreal builder's samplers and the Blender loader's `specular_weight`;
    - `unreal/RUNTIME.json` (`unreal-runtime-v6`);
    - the release locks;
    - ledger rows P20, P28, P32, P33 and M7.
  - **Grepped the tree for the phase's name:** no code; only the planning docs above.
  - **Baseline:** `run_all.py` at `49da20e`, on the machine with Unreal: **18 lanes, 18 PASS, 0 SKIP, 0 FAIL** (every lane ran). `check_exporter.sh` is not baselined: no step touches `blender/addons/` or `tools/conformance/`.
  - **Decided by the agent unless the lead says otherwise:** RD-P22-1 to RD-P22-10. **Put to the lead:** Q-P22-1.
- **2026-10-27 — Pass 2** (the lead on Q-P22-1: *"1) What does it take to get Studio to see the new maps? I think trying to judge if it look plastic in studio using Blender is not the way... Also... why not update our UE matter test tool to use the new maps first and shoe screensshots from that? (or show me)"*).
  - **Read at the platform's origin:** how Studio builds its Matter masters and binds their textures, how Stage carries `base_color_map`, and whether a look-dev scene exists. → F-P22-8 corrected.
  - **Read in the tree:** the runtime's lighting (F-P22-11).
  - **Changed:** the look surface becomes the runtime's shadowed look view (RD-P22-11; RD-P22-9 superseded). The ledger row moves to 22.1. The close does not wait for Studio (RD-P22-12, unless the lead says otherwise). The First human test is rewritten: today's skin in the look view first.
