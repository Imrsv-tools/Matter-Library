# Research — Which side of a face is drawn: what IMRSV's asset tooling found, and what it asks of the library

**Opened:** 2026-10-11 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `AT` (ids `AT-Qn`, `AT-Fn`). **Pass 1** is written from the asset tooling's side. The library's review of it against its own tree is **Pass 2** (the same day), as in `261005_R_PlatformThinGlassAsks.md`. **Pass 3** (the same day) is what the library then built.
**Requested by:** IMRSV's work on the tools that make a model ready for Studio: how an asset is built, checked and pictured before anyone opens Studio. The lead, 2026-10-11, verbatim: *"Go ahead and ask Matter library whatever you need"*.

**Questions:** (1) what should the library's Blender route and its Creator Asset Profile say about which side of a face is drawn? (2) may a second project call the rig's Unreal driver and app, to picture an asset?

**Extends, does not replace:** `docs/specs/Ontology/MasterSet.md` §Material-settings intent (the two-sided column) · `docs/specs/Contract/CreatorAssetProfile.md` · `blender/addons/imrsv_lcd_export` · `blender/asset_library/MatterLibrary.blend` · `tools/parity/JOB_FORMAT.md` and `tools/parity/drivers/unreal.py` · `PlatformDependencies.md` P23 (its note that an emissive's lit level follows the light's colour, not yet measured).

**Public-repo note.** The asset tooling is a sibling IMRSV project and is private for now. It is summarised here by what it found and what it needs: no paths, code or ruling ids of its own.

**Measured at:** `82a1f0d` (2026-10-11) · Blender 5.2.0 LTS · OpenUSD 26.03 · the pinned Unreal app, `unreal-runtime-v3`.

## The short version

- **A prop built for Studio passed every check and showed in Studio with parts missing from the front.** It was built by script, saved through the library's export add-on, and conformed to the profile 9 of 9. 204 of its 3,764 triangles were wound the wrong way round. **That fault was the builder's, and is fixed there.**
- **What hid it is the library's to look at.** MasterSet says four masters draw one side of a face. The library's Blender route says the opposite twice: Blender draws both sides of all 89 materials, and every mesh it exports is written `doubleSided = 1` (AT-F2, AT-F3). So the builder's own tool and the file both show a face that Studio will not.
- **Three asks about that** (A1 – A3), in the Blender asset file and in the profile's words.
- **The rig's Unreal app drew the faulty asset exactly as Studio had, from outside this repository, with nothing here changed** (AT-F6). That is worth keeping, so one ask is about which parts of the driver a second project may lean on (A4), and one about a download that happens when nobody asked for it (A5).
- **One measurement on the way, offered toward P23's open note:** on the Emissive master the picture's brightness follows the *length* of the emission colour (AT-F7).

## Pass 1 — What the asset tooling found

### What happened

- **AT-F1 — A one-sided master draws only a face's front, and an asset can pass the profile with faces wound backwards.**
  - The prop is 26 meshes in 14 library materials: 23 on Opaque, one each on TwoLayer, Emissive and TranslucentThin.
  - In Studio its back panel, the top of its bench and its drawer fronts were not drawn from the front, and were drawn from behind. Studio follows MasterSet here: whether both sides are drawn is the master's, and the mesh's own `doubleSided` is not used for a Matter material. *(The platform's reading of its own app, summarised.)*
  - The cause was 204 triangles wound clockwise seen from outside, all on parts the build script made as boxes.
  - `tools/conformance/assert_profile.py lightweight` answered CONFORMS. The profile's nine rules and its forbidden list do not mention which way a face looks, or `doubleSided`. Nor does `usdchecker`.

### What was measured

- **AT-F2 — Blender's USD exporter writes `doubleSided` from the material's *Backface Culling* switch.** On gives `doubleSided = 0`; off, which is Blender's default, gives `1`. Reproduction below.
- **AT-F3 — None of the 89 materials in `MatterLibrary.blend` has that switch on.** Counted by loading the file headless. So every mesh saved by the library's route says it has two sides, whichever master its article is on: the prop's 26 meshes all carry `doubleSided = 1`, 25 of them on a one-sided master.
- **AT-F4 — So three things disagree with the contract, and each one hides the fault.** Blender's viewport and its Eevee renderer draw both sides of a one-sided article. Storm believes the file's `doubleSided` and does the same. Only Unreal, drawing with the masters, shows it. *Not tried: whether Cycles would show it. Blender documents the switch as Eevee's.*
- **AT-F5 — A file check finds it with OpenUSD alone.** The asset tooling now has one: for every closed piece of every mesh, which faces would have to turn round for the piece to hold a positive volume. It refused the prop as first built (204 triangles) and passes it rebuilt. It can be offered here if the library wants it beside the asserter.
- **AT-F6 — The rig's Unreal app drew the asset from outside this repository, and showed what Studio showed.**
  - A reader on the asset tooling's side opened the asset with OpenUSD. A second script, in this repository's own Python, called `drivers/unreal.py` as it is: `write_mesh`, `article_material` (with the asset's own value for one mesh's `base_color_tint`), `camera_view`, `lights`, `warmup`, `find_runtime`, `run_runtime`, `read_pfm`, `linear`, `srgb8`, and the constants `JOB_FORMAT`, `SUPERSAMPLE`, `SETTLE_FRAMES`, `FLAT_NORMAL`. It wrote the app's job itself, with one material per mesh in each setting.
  - It also used two things of the app's that the job page does not describe for callers: a setting's `sun_scale` and `sky_scale`, and the `Sky` master as a flat two-sided colour.
  - All 26 meshes drew on their masters; the driver refused none of the 14 articles. A run of 26 meshes from six views, drawn four ways, took 35 seconds.
  - The picture of the prop as first built has the same parts missing as Studio's. The rebuilt prop is whole.
  - Drawing each mesh a second time in a flat colour on a one-sided master, and a third time on the two-sided `Sky` master, lets the missing faces be **counted**: a pixel that is a mesh's colour in the third picture and not in the second. It named the same 12 meshes the file check names.
- **AT-F7 — On the Emissive master, the brightness of the light follows the length of its colour.** Seen while making the flat colours above. With the sun and the sky scaled to zero, `base_color` black, `base_weight` 0 and `emission_luminance` 1, the float capture read:

  | `emission_color` asked | Read (R, G, B) |
  |---|---|
  | blue alone, at 1/3, at 2/3 and at 1 | (0, 0, 1.25), all three |
  | (0, 2/3, 1/3) | (0, 1.12, 0.56) |
  | (0, 2/3, 1) | (0, 0.69, 1.04) |
  | (1/3, 1/3, 2/3) | (0.51, 0.51, 1.02) |
  | (1/3, 2/3, 1) | (0.33, 0.67, 1.00) |

  Every row is 1.253 × the colour divided by its own length (the root of the sum of its squares), and 1.253 is the master's own 1 / 0.798. By that rule white would read 0.72 a channel, which is P23's *"a white light reads about a quarter darker"*. **These were read off captures that were not kept, so re-measure before building on them.**
- **AT-F8 — Asking the driver where the app is fetches the app.** `find_runtime()` with no environment variable set returns the pinned build, and downloads it (245 MB, 382 MB unpacked) if it is not there. A caller that only wants to know whether an app is present cannot ask without fetching. It happened to the asset tooling during a check that was meant to launch nothing.

### Reproduction (AT-F2, AT-F3)

```python
# blender -b --factory-startup --python this.py -- <out dir> <MatterLibrary.blend>
import bpy, sys
out, lib = sys.argv[sys.argv.index("--") + 1:][:2]
bpy.ops.wm.read_factory_settings(use_empty=True)
for name, cull in (("Culled", True), ("Plain", False)):
    bpy.ops.mesh.primitive_cube_add()
    ob = bpy.context.object; ob.name = name; ob.data.name = name
    m = bpy.data.materials.new(name); m.use_backface_culling = cull
    ob.data.materials.append(m)
bpy.ops.wm.usd_export(filepath=out + "/t.usda", export_materials=True)   # Culled: doubleSided = 0 · Plain: doubleSided = 1
with bpy.data.libraries.load(lib, link=False) as (src, dst):
    dst.materials = list(src.materials)
print(sum(1 for m in bpy.data.materials if m.use_backface_culling and m.name not in ("Culled", "Plain")))   # 0, of 89
```

The scripts behind AT-F5 and AT-F6 are the asset tooling's and are not public yet. They can be offered here on request.

### The asks

- **A1 — In the Blender asset file, an article on a one-sided master has *Backface Culling* on.** Opaque, TwoLayer, Emissive and Subsurface, by MasterSet's table; off for Masked, Hair and the two see-through masters. Then Blender stops drawing a face that Unreal will not, while the builder is still modelling. And by AT-F2 the export writes `doubleSided = 0` for those meshes with no change to the add-on, so a viewer that reads the flag can show it too. *If the library would sooner have the add-on write the flag from the article's master, that serves the file as well; it does not serve the builder's viewport.*
- **A2 — The Creator Asset Profile says which side of a face is drawn.** In a builder's words: faces are wound counter-clockwise seen from outside; whether both sides of a face are drawn belongs to the material's master; a mesh's `doubleSided` does not make a face show. Today that is in MasterSet, which a material's author reads, and not in the profile, which an asset's builder reads.
- **A3 — Say what `doubleSided` should be in a conforming asset.** Agreeing with the master, or free. Whether the asserter then checks it is the library's call.
- **A4 — Say what a second project may lean on in the rig's Unreal driver.** AT-F6 lists what was called. Either name the functions and the job fields that are meant to stay put (and write `sun_scale`, `sky_scale` and the `Sky` master into `JOB_FORMAT.md` if they are among them), or say that an asset job belongs inside the rig and the asset tooling should ask for that. **The lead has ruled (2026-10-11) that the asset tooling's own tools are defined and tested on its side; it asks only that what it calls here is not moved without a word.**
- **A5 — A way to ask whether an Unreal app is present without fetching one** (AT-F8).

### Questions for the library

- **AT-Q1 — How do answers come back?** The platform's asks are tracked in `PlatformDependencies.md`. The asset tooling is a new consumer and has no row there.
- **AT-Q2 — Is AT-F7 what the Emissive master means to do?** It is offered as a measurement toward P23's open note, not as an ask.
- **AT-Q3 — Does the library want the face-direction check** (AT-F5) beside its asserter, or is it the asset tooling's to keep?

### A suggested ledger row (the library authors it, or not)

*Which side of a face is drawn, said where a builder will see it: Backface Culling on for one-sided articles in the Blender asset file, and a line in the Creator Asset Profile. A second consumer, IMRSV's asset tooling, calls the rig's Unreal driver from outside to picture an asset.* Owner: Matter Library (the asset file, the profile, the driver's stated surface) · IMRSV's asset tooling (its own reader, its checks).

---

## Pass 2 — The library's review: what its own tree, tools and records show

*Written from the library's side, 2026-10-11, at `724c429`, on the machine with Unreal. Blender 5.2.0 LTS, OpenUSD 26.03. Pass 1 was measured at `82a1f0d`; the tree has since taken eight commits from the other machine (9 – 10 October), and two of them touch what Pass 1 leans on (AT-F18, AT-F19).*

**Examined:** `docs/specs/Ontology/MasterSet.md` §Material-settings intent · `docs/specs/Contract/CreatorAssetProfile.md` and `LCDSchema.md` · `tools/conformance/assert_profile.py`, its goldens and fixtures, `check_exporter.sh`, `check_asset_library.sh` · `blender/addons/imrsv_lcd_export` (the export and its edit step) · `tools/generators/matter_proxy.py` · `blender/asset_library/MatterLibrary.blend`, loaded headless · `tools/parity/drivers/unreal.py`, `rig.py`, `job.py`, `JOB_FORMAT.md`, the rig's scene builders · `unreal/MatterRuntime/Scripts/build_masters.py`, the app's job reader, `unreal/RUNTIME.json` and the unpacked build on this disk · the three emissive articles · `PlatformDependencies.md` P23, Learnings Unreal U4 and Phase12's step 12.4 · the master-adoption research's MA-RD1.

**Measured here, on throwaway scenes** (§Reproduction, Pass 2): Pass 1's own reproduction, again; the library's export add-on with *Backface Culling* on; a square seen from behind in Eevee, Cycles and Storm.

**Not run:** the Unreal runtime. Another Unreal application was using this machine's graphics card for the whole pass, so AT-F6 is not repeated and AT-F7 is not re-measured. **Not examined:** the asset tooling's scripts (private); how Studio, USDLiveView or usdview treat `doubleSided`; Epic's material function.

### Findings

**Which side of a face is drawn**

- **AT-F9 — AT-F2 and AT-F3 hold at the merged tree.** The stock exporter writes `doubleSided = 0` for a mesh whose material has *Backface Culling* on and `1` with it off. The asset file holds 89 materials, 88 of them articles (one stray `Material` is not marked as an asset), and none has the switch on. By master: 43 Opaque, 27 Subsurface, 3 Emissive and 2 TwoLayer, so **75 of the 88 articles are on a one-sided master**; the other 13 are on a two-sided one (6 TranslucentThin, 3 TranslucentThick, 3 Masked, 1 Hair).
- **AT-F10 — The same holds through the library's own add-on.** Pass 1 measured the stock exporter. Run through `export_lcd_usd` on two Copper squares, the second with the switch on, the file reads `doubleSided = 1` for the first mesh and `0` for the second. The add-on's edit step rewrites materials and the layer's metadata and never a mesh, so the flag leaves as Blender wrote it. `assert_profile.py lightweight` answers CONFORMS for that file, as it does for one with both at `1`: it does not read the flag.
- **AT-F11 — The contract's own golden says two sides on a one-sided master.** `tools/conformance/golden/creator_table_lightweight.usda` carries `doubleSided = 1` on both its Copper meshes, and Copper is on Opaque. The portable golden is built from it and carries the same. The profile's nine rules and its forbidden list name neither which way a face is wound, nor `doubleSided`, nor USD's `orientation` (which turns the rule round: counter-clockwise is the front only at its default, right-handed). Neither the golden nor the add-on's output authors `orientation`.
- **AT-F12 — The two-sided column is realised in exactly one place, the Unreal builder.** `build_masters.py` sets `two_sided` per master, and its table agrees with MasterSet row for row: false on Opaque, TwoLayer, Emissive and Subsurface; true on Masked, Hair and the two see-through masters. Nothing on the Blender side sets *Backface Culling*: not the asset file's generator, not the rig's Blender masters. `LCDSchema.md` says what MasterSet says: two-sidedness is baked into the master and is not driven per prim.
- **AT-F13 — Which of the library's renderers shows a face seen from behind** (one square, 64 × 64, 3,600 of its pixels covered by the square):

  | Renderer | Setting | Seen from behind |
  |---|---|---|
  | Eevee | *Backface Culling* off | drawn (3,600 pixels) |
  | Eevee | *Backface Culling* on | **not drawn** (0 pixels) |
  | Cycles | off, and on | drawn both times (3,610 and 3,610): **Cycles does not read the switch** |
  | Storm (`usdrecord` at its defaults) | `doubleSided = 1` | drawn, lit as the front is (255 of 255) |
  | Storm | `doubleSided = 0` | **still drawn**, shaded as a face turned away (13 of 255 under the camera light) |

  - **This answers what AT-F4 left untried:** Cycles would not show it. The rig's Blender column is Cycles, so A1 changes a builder's viewport and never the rig's sheet.
  - **It corrects AT-F4 on Storm.** Storm does not hide a backward face whatever the flag says; the flag changes how the face is lit. So the hope in A1, *"a viewer that reads the flag can show it too"*, is weaker than written: in Storm a backward face on a `doubleSided = 0` mesh turns dark under a light in front of it, and is not missing. *Not measured: the same under the rig's even dome, where a face turned away is lit from its other side and should hardly differ.*
  - **The rig's own scenes already agree with the masters.** The test scene authors no `doubleSided` (USD's default, one side), and the character's three cut-out cards, which are on two-sided masters, carry `1`.
- **AT-F14 — A1 has one home.** `load_article.build` in `blender/masters/load_article.py` creates each article's material, for the asset file and for the rig's Blender column alike. *(Corrected 2026-10-11, in Pass 3. Was: "`build_matter_proxy` in `tools/generators/matter_proxy.py` creates each article's material in the asset file and already reads the recipe's master to set the look". That file is the look-alike the generator used until Phase05 and is retired; Pass 2 read it and not the generator's own header, which says so.)* `check_asset_library.sh` generates a library into scratch and checks its structure with `verify_asset_library.py`, which is where a check of the switch would fit. The exporter's gate is separate: it exports from a scaffold file, `blender/MatterMaterials.blend`, whose Copper has the switch off, so it goes on writing `doubleSided = 1` until that scaffold and the golden are changed with A3.
- **AT-F15 — The tracked asset file is six articles behind the tree.** `Cardboard_Kraft`, `CastIron_Raw`, `Paint_Satin`, `Paper_Natural`, `Porcelain_Glazed` and `StainlessSteel_Brushed`, added on 9 and 10 October, have recipes and are not in `MatterLibrary.blend`. No lane of `run_all.py` names the file. A regeneration is owed with or without A1.
- **AT-F16 — A1 will be seen first on sheets.** With the switch on, a mesh that is one layer of faces disappears from behind in Blender's viewport, as it already does in Unreal. That is the truth A1 is for. Twelve of the 75 one-sided articles are sheet matter, all on Opaque: ten textiles (`Canvas_Natural`, `Cotton_Jersey`, `Denim_Indigo`, `Denim_LightWash`, `Felt_Natural`, `Leather_Brown`, `Leather_Natural`, `Satin_Natural`, `StretchKnit_Natural`, `WoolSuiting_Natural`), `Paper_Natural` and `Cardboard_Kraft`. A builder who hangs a curtain as one sheet will see it from one side only, in every scene that takes the next asset file.

**Calling the rig's Unreal driver from outside**

- **AT-F17 — Everything AT-F6 called is still there, and nothing says it is meant to stay.** The ten functions keep their names and arguments at `724c429`, and the four constants their values (`JOB_FORMAT` 3, `SUPERSAMPLE` 4, `SETTLE_FRAMES` 120, `FLAT_NORMAL`). `rig.py` is the only caller in this repository. The module marks two helpers private with an underscore and says nothing about the rest. `JOB_FORMAT.md` gives the rig's job a field table and describes the Unreal job (the file the app reads, format 3) in prose, with no table; the app's reader, `MatterRuntimeGameMode.cpp`, is the only full list of its fields. `sun_scale` and `sky_scale` are read per setting by the app and written only by the driver's own `calibrate`, since Phase06. The `Sky` master is what the driver's mask setting draws with; the builder calls it *"the rig's dome, not a master"* and leaves it out of a consumer's build (`MATTER_MASTERS_SKY=0`).
- **AT-F18 — What moved in the driver between Pass 1's measurement and this one.** Three things, none a changed name or argument: the list of values passed straight to Epic's function gained `coat_darkening`; `find_runtime()` on a Mac now runs the editor under `$UE_ROOT` or returns nothing, and no longer reaches the pinned build there; the job writers make `out_dir` absolute.
- **AT-F19 — The masters moved under the pinned runtime, and nothing says so.** This is the case A4 asks not to meet.
  - On 10 October the builder changed how the masters draw a coat: the base under it is darkened by MaterialX's factor, where Epic's own darkening had run before. `coat_darkening` defaults to 1, 27 articles set a coat and none sets `coat_darkening`, so **all 27 are drawn differently at their own values**. The commit's own measure: porcelain close up, Storm against Unreal, from about 6 to 1.18 (mean ΔE2000).
  - `unreal/RUNTIME.json` still pins `unreal-runtime-v3`, built from `e1fc83e` on 1 October. The masters are build output and are not tracked; this machine's were built on 5 October.
  - Since the pin's source the builder has changed in four commits. Three change nothing at the defaults: one added the switches, which the unset build of the master-adoption research's Pass 9 shows, and two edited its comments. This is the fourth. The app's own source has not changed.
  - **So a caller of the pinned runtime draws coated articles as before 10 October:** the asset tooling's pictures, and the rig's Unreal column on this machine. A Mac running the editor on freshly built masters draws them the new way. Two machines' Unreal columns now differ on 27 articles.
  - Nothing tells a caller. The job's format number did not change, rightly: the job did not. MA-RD1 (*"a builder change that alters nothing at its defaults needs no new runtime published"*) does not cover a change that does alter them.
  - **What a caller can check today, with no build:** `git log <the "source" in unreal/RUNTIME.json>..HEAD -- unreal/MatterRuntime/Scripts/build_masters.py` lists every builder change the pinned build does not have.
  - *Not run: no picture was made here to show the difference.*
- **AT-F20 — AT-F8 is as described, and this disk shows it.** On Linux with neither variable set, `find_runtime()` returns `pinned_package()`, which downloads and unpacks the build unless a launcher and a matching stamp are already there. `rig.py` calls it only to decide whether to run the column or skip it, which is the same *"only asking"* use. On this machine the pinned build's folder and its stamp are dated 2026-10-11 17:22, the hour of the asset tooling's check, around content dated 1 October (the archive's own dates). What was there before cannot be read from the disk. The machine also holds the same archive it built, under `unreal/dist/`, which the lookup never looks at.

**The Emissive master's brightness**

- **AT-F21 — AT-F7's rule fits the library's own records, and it explains the master's correction.** If Epic's function draws `emission_luminance` × the colour **divided by its own length**, then Unreal against the other two tools is 1.253 ÷ that length, 1.253 being the master's 1 ÷ 0.798:

  | Colour | Its length | Unreal ÷ the others, by the rule | What the library recorded |
  |---|---|---|---|
  | `Neon_Signage` (1, 0.15, 0.75) | 1.259 | 0.995 | the correction was fitted on this colour: 0.798 measured, and 1 ÷ 1.259 is 0.794 |
  | `LED_CoolWhite` (0.993, 0.992, 1) | 1.723 | 0.727 | *"about a quarter darker"*. Dim view, lit cube, at brightness 12: 0.58 against 0.78 |
  | the rig's *emission warm* row (1, 0.456, 0.147) | 1.109 | 1.130 | *"about an eighth brighter"*. Red: 0.885 against 0.786 |

  - **The two recorded pairs fit to the third digit.** The dim view shows a brightness of 12 as 12 ÷ 16 = 0.75; what Storm reads above that (0.03 on the white, 0.036 on the warm red) is the lit surface. White: 0.75 × 0.727 + 0.03 = 0.575, recorded 0.58. Warm red: 0.75 × 1.130 + 0.036 = 0.884, recorded 0.885. The white light at 6, 12 and 15 comes to 0.30, 0.575 and 0.71 by the rule, recorded 0.31, 0.58 and 0.71.
  - **So the 0.798 was never the function's own scale.** It is 1 ÷ the length of the one magenta it was measured on, to half a percent. Learnings Unreal U4 and P23 both say *"why is not measured"*; this is a why that fits five numbers the library took itself and the seven readings of AT-F7's table.
  - **If it holds, the repair is the master's:** multiply `emission_luminance` by the length of `emission_color` in place of the constant (with a guard for a black colour). It changes every emissive picture in Unreal except Neon's, so it needs a new runtime, as AT-F19 does.
  - *Worked out from recorded numbers, not measured in this pass. The function itself is not read.*

### The asks, as the library finds them

| # | State after this pass |
|---|---|
| A1 | **Built 2026-10-11 (Pass 3, AT-F23); the tracked asset file is still to be regenerated.** *Was, at Pass 2:* **Agreed in substance, not built.** It makes Blender's viewport and Eevee say what MasterSet says (AT-F12), through one function (AT-F14), and the export then writes the flag with no change to the add-on (AT-F10), so the alternative Pass 1 offers (the add-on writing the flag from the master) is not needed. Two things to know first: it does nothing for Cycles or the rig's sheet, and little for Storm (AT-F13); and it shows on 75 articles, sheets first (AT-F16). **One sitting.** |
| A2 | **Written 2026-10-11 (Pass 3, AT-F28): the profile's rule 10.** *Was, at Pass 2:* **Agreed, not written.** A contract edit is not research's to make (the precedent is the thin-glass rule, written on the lead's word). The sentence needs one thing Pass 1's wording leaves out: USD's `orientation` (AT-F11). |
| A3 | **Taken as *free* 2026-10-11 (§Resolved, AT-RD2; Pass 3, AT-F28).** *Was, at Pass 2:* **A ruling, the lead's.** What bears on it: the golden says `1` on a one-sided master (AT-F11); Blender's default writes `1`; MasterSet and LCDSchema give a per-mesh value nowhere to land; Storm reads the flag for shading only (AT-F13). **The library's leaning: free.** The profile says the flag never makes a face show and is not a conformance rule, and the library's own route and golden write it in agreement with the master, so that no file the library makes says the opposite of its contract. A rule that it *must* agree would fail every stock Blender export until its builder flips a viewport switch, and would not have caught the prop: its fault was the winding, which a check of the geometry finds (AT-Q3). |
| A4 | **The page is written 2026-10-11 (Pass 3, AT-F27), and a runtime with the moved masters is built and not published (AT-F26).** *Was, at Pass 2:* **Confirmed, and wider than asked.** Nothing names the surface (AT-F17). It held across the merge (AT-F18). The masters behind the pinned build did move (AT-F19). Three parts: a section in `JOB_FORMAT.md` naming the Unreal job's fields and the functions a second project may call (**one sitting**); `sun_scale`, `sky_scale` and `Sky` among them or not (they are the calibration's and the mask's, unchanged since Phase06, so cheap to promise); and a new runtime for the coat change (AT-Q5). |
| A5 | **Built 2026-10-11 (Pass 3, AT-F22).** *Was, at Pass 2:* **Confirmed** (AT-F20). **One sitting:** a way to ask that never fetches. The rig's own skip-or-run test wants the same answer. |

### The questions, as far as this pass takes them

- **AT-Q1 — How do answers come back?** By precedent, as passes in this doc and one row in `PlatformDependencies.md`, in the table of asks made of the library, where each earlier asks doc has its rows (M3 – M7); the next free number is M8. That row is written on the lead's word, as M6 was, and this pass does not write it. The table is headed *"From IMRSV to the Matter Library"* and the asset tooling is an IMRSV project, so it fits as it stands; a heading of its own is the lead's to ask for.
- **AT-Q2 — Is AT-F7 what the Emissive master means to do?** No. The master means to draw `emission_luminance × emission_color` and corrects with a constant that is right for one colour (AT-F21).
- **AT-Q3 — Does the library want the face-direction check?** Leaning yes; the lead's call. Every look the library has hides this fault (Cycles, Storm, and Eevee as the asset file ships), and its profile gate passes it, so a check of the file is the only thing shown to catch it without Unreal. Its limits: only a closed piece has an outside, so it cannot judge a sheet; and it needs OpenUSD, so it would sit beside `assert_profile.py`, which reads text only by design, as the other OpenUSD steps of the conformance gate do. The script is the asset tooling's and private; taking it means it is offered under this repository's licence.

### New questions

- **AT-Q4 — Is a sheet right on a one-sided master?** (AT-F16.) Twelve sheet articles are on Opaque. A1 makes visible in Blender what is already so in Unreal. MasterSet keeps a two-sided foliage variant as *planned*; cloth and paper are not mentioned there. Not this doc's to settle.
- **AT-Q5 — Does the coat change of 10 October get a new runtime build?** (AT-F19.) MA-RD1 does not cover it. Building it is this machine's work; publishing it is the lead's. Until then the pinned build and the builder disagree on 27 articles.
- **AT-Q6 — What does Epic's function do with `emission_color`?** (AT-F21.) Readable on the machine with Unreal. Or one launch of the runtime repeats AT-F7 with its captures kept: an Emissive article, black base, the sun and sky scaled to zero, a handful of colours.

### Reproduction (Pass 2)

All three ran from the repository root. Blender is started without the USD toolchain's variables, as `check_exporter.sh` starts it. Nothing they wrote is kept.

**AT-F9** is Pass 1's script with its last line replaced, so that each material's name is printed and can be joined to its recipe's `master`:

```python
for m in bpy.data.materials:
    if m.name not in ("Culled", "Plain"):
        print("MAT", m.name, int(m.use_backface_culling), int(bool(m.asset_data)))
```

**AT-F10**, the library's own add-on:

```python
# blender -b blender/MatterMaterials.blend --python this.py -- <out.usda>
import bpy, sys, os
out = sys.argv[sys.argv.index("--") + 1]
sys.path.insert(0, os.path.join(os.path.dirname(bpy.data.filepath), "addons"))
import imrsv_lcd_export as A
from imrsv_lcd_export.lcd_usd_edit import IDENTITY_PROP
MID = "Copper_Verdigris_Aged_Base_s01_v01"
m1 = bpy.data.materials[MID]; m1[IDENTITY_PROP] = MID
m2 = m1.copy(); m2.use_backface_culling = True
obs = []
for name, mat in (("Copper_Plain", m1), ("Copper_Culled", m2)):
    me = bpy.data.meshes.new(name + "_mesh")
    me.from_pydata([(0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0)], [], [(0, 1, 2, 3)]); me.update()
    uvl = me.uv_layers.new(name="UVMap")
    for i, co in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uvl.data[i].uv = co
    ob = bpy.data.objects.new(name, me); ob.data.materials.append(mat)
    bpy.context.collection.objects.link(ob); obs.append(ob)
for o in bpy.context.scene.objects:
    o.select_set(False)
for o in obs:
    o.select_set(True)
bpy.context.view_layer.objects.active = obs[0]
print(A.export_lcd_usd(out))     # then: grep doubleSided <out.usda>; assert_profile.py lightweight <out.usda>
```

**AT-F13**, Eevee and Cycles:

```python
# blender -b --factory-startup --python this.py -- <out dir>
import bpy, sys, addon_utils
out = sys.argv[sys.argv.index("--") + 1]
bpy.ops.wm.read_factory_settings(use_empty=True)
addon_utils.enable("cycles")
scn = bpy.context.scene
scn.world = bpy.data.worlds.new("W"); scn.world.use_nodes = True
scn.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
bpy.ops.mesh.primitive_plane_add(size=2)            # its normal is +Z
mat = bpy.data.materials.new("M"); mat.use_nodes = True
nt = mat.node_tree; nt.nodes.clear()
o = nt.nodes.new("ShaderNodeOutputMaterial"); e = nt.nodes.new("ShaderNodeEmission")
nt.links.new(e.outputs["Emission"], o.inputs["Surface"])
bpy.context.object.data.materials.append(mat)
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam")); scn.collection.objects.link(cam)
scn.camera = cam
scn.render.resolution_x = scn.render.resolution_y = 64
scn.view_settings.view_transform = "Standard"
for eng in ("CYCLES", "BLENDER_EEVEE"):
    scn.render.engine = eng
    if eng == "CYCLES":
        scn.cycles.device = "CPU"; scn.cycles.samples = 4; scn.cycles.use_denoising = False
    for side, z, rx in (("front", 3.0, 0.0), ("behind", -3.0, 3.141592653589793)):
        cam.location = (0, 0, z); cam.rotation_euler = (rx, 0, 0)
        for cull in (False, True):
            mat.use_backface_culling = cull
            scn.render.filepath = f"{out}/{eng}_{side}_{cull}.png"
            bpy.ops.render.render(write_still=True)
            img = bpy.data.images.load(scn.render.filepath); px = list(img.pixels)
            print(eng, side, "culling", cull, sum(1 for i in range(0, len(px), 4) if px[i] > 0.5), "pixels lit")
            bpy.data.images.remove(img)
```

**AT-F13**, Storm. Four files from this one: the camera in front (`translate` z 3, `rotateXYZ` y 0) or behind (z −3, y 180), and `doubleSided` 0 or 1. Each is recorded with `usdrecord --camera /Cam --imageWidth 64 <file> <png>` after `source tools/usd-toolchain/activate-usd-tools.sh`; the pixels drawn are those whose alpha is above 0.

```
#usda 1.0
(
    metersPerUnit = 1
    upAxis = "Y"
)

def Camera "Cam"
{
    float focalLength = 50
    float horizontalAperture = 36
    float verticalAperture = 36
    float2 clippingRange = (0.1, 100)
    double3 xformOp:translate = (0, 0, 3)
    float3 xformOp:rotateXYZ = (0, 0, 0)
    uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ"]
}

def Mesh "Square"
{
    uniform bool doubleSided = 0
    uniform token subdivisionScheme = "none"
    int[] faceVertexCounts = [4]
    int[] faceVertexIndices = [0, 1, 2, 3]
    point3f[] points = [(-1, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0)]
    color3f[] primvars:displayColor = [(1, 1, 1)]
}
```

---

## Pass 3 — What the library built (2026-10-11)

*Written from the library's side, on the machine with Unreal. The lead, to Pass 2's handback, verbatim: "yes, lets do it all... prep the work needed. or do it.. wither way" (§Resolved, AT-RD1). Built as six quick fixes outside this doc, each its own commit so that any one reverts alone. The other Unreal application had closed by then, so the runtime was launched.*

**Baseline first.** Before any edit: `run_all.py` 15 lanes pass and two fail (`approval_binds_freeze`, `release_verify`: red on this machine for a local reason, an old staging folder); `check_asset_library.sh`, `check_exporter.sh` and `check_conformance.sh` pass. After every edit: the same, lane for lane.

- **AT-F22 — A5 is built** (`b2d2ae6`). `find_runtime(fetch=False)` answers from the machine as it is and never downloads; the default is unchanged, so the rig behaves as before. With the download call replaced by one that raises: on this machine the answer is the unpacked build's launcher, the same as the default gives; on an empty package folder it is `None` and nothing is written, and the default still tries to download.
- **AT-F23 — A1 is built, in the loader** (`fc21616`). `blender/masters/build_masters.py` names the four two-sided masters, and `load_article.build` turns *Backface Culling* on for an article on any other. `verify_asset_library.py` asserts the switch per article, reading the master from the recipe.
  - **The check fails when it should:** run on a library generated before the change, it refuses exactly the 81 articles on a one-sided master and passes the 13 on a two-sided one. After the change `check_asset_library.sh` passes all 94.
  - **Through the add-on, from that generated library:** Copper (Opaque) writes `doubleSided = 0`; Lace (Masked) and Glass_Clear (thin) write `1`.
  - **The rig's Blender column does not move:** Cycles gives the same pixels with the switch on and off, on a cube and a square seen from behind.
  - **⚠ Not done: the tracked `blender/asset_library/MatterLibrary.blend` is not regenerated.** It has only ever been regenerated on the library machine. On this one Blender's colour configuration does not load, and the generator bakes each article's preview. So a Creator's installed library does not carry the switch yet. It is one command there, and it also brings in the six articles of AT-F15: `blender --background --factory-startup --python tools/generators/gen_asset_library.py`.
- **AT-F24 — AT-F7 is measured again, with the numbers kept. This answers AT-Q6.** The Emissive master alone, on `unreal-runtime-v3`: Neon_Signage with a black base and `base_weight` 0, `emission_luminance` 1, the sun and the sky scaled to zero, one setting per colour, the cube's 3,485 pixels read off the float capture (median, ÷ the driver's exposure constant).

  | `emission_color` asked | Its length | v3: read ÷ asked | v3: that × the length | The rebuilt runtime: read ÷ asked |
  |---|---|---|---|---|
  | (1, 0.15, 0.75) — Neon_Signage's own | 1.259 | 0.9961 | 1.2540 | 1.0008 |
  | (1, 1, 1) | 1.732 | 0.7239 | 1.2538 | 1.0005 |
  | (0.993, 0.992, 1) — LED_CoolWhite's own | 1.723 | 0.7277 | 1.2541 | 1.0008 |
  | (1, 0.456, 0.147) — LED_WarmWhite's own | 1.109 | 1.1308 | 1.2539 | 1.0008 |
  | (0, 0, 1) | 1.000 | 1.2542 | 1.2542 | 1.0010 |
  | (0, 0, 0.3333) | 0.333 | 3.7626 | 1.2542 | 1.0008 |
  | (0, 0.6667, 0.3333) | 0.745 | 1.6819 | 1.2536 | 1.0008 |
  | (0.3333, 0.3333, 0.6667) | 0.817 | 1.5352 | 1.2535 | 1.0008 |
  | (0.5, 0.5, 0.5) | 0.866 | 1.4477 | 1.2538 | 1.0005 |
  | (0.2, 0.2, 0.2) | 0.346 | 3.6193 | 1.2538 | 1.0008 |
  | (1, 0, 0) | 1.000 | 1.2542 | 1.2542 | 1.0010 |
  | (1, 1, 0) | 1.414 | 0.8866 | 1.2539 | 1.0005 |

  - **The fourth column is one number, 1.2535 to 1.2542.** So Epic's function draws the brightness × the colour's direction, the colour over its own length, and nothing of the colour's size: white, a 0.5 grey and a 0.2 grey all read 0.7239.
  - **1.2542 is 1.0008 ÷ 0.798.** The 0.08 % is the capture's own scale, not the master's.
- **AT-F25 — The Emissive master is repaired in the builder** (`51d2424`). `unreal/MatterRuntime/Scripts/build_masters.py` gives Epic's function `emission_luminance` × the length of `emission_color`, in place of × 1 ÷ 0.798. A black colour gives no light. On the rebuilt runtime every one of the twelve reads 1.0005 to 1.0010 of what was asked (the table's last column). Learnings Unreal U4 carries the cause.
- **AT-F26 — A runtime with both master changes is built, and is not published. It pictures AT-F19.** `unreal/build.sh masters`, then `package`, on Unreal 5.8.0. The rig run on three articles at 256 pixels, Storm and Unreal, once on the pinned v3 and once on the build:

  | Article | Storm against Unreal on v3 (mean ΔE76 over the subjects; L\*) | On the build | Float captures, v3 against the build |
  |---|---|---|---|
  | `Porcelain_Glazed` (a coat) | 6.7 wide, 7.2 close; L\* 78.8 against Storm's 72.1 | 1.3 wide, 1.3 close; L\* 73.2 | differ |
  | `GreyCard_Neutral18` | 0.72 | 0.72 | **the same bytes** |
  | `Copper_Verdigris` | 1.46 wide, 1.48 close | 1.46, 1.48 | **the same bytes** |

  - So the pinned v3 was drawing a coat the old way, as AT-F19 read from the tree; the build draws it as the coat change of 10 October meant; and an article with neither a coat nor a light is untouched.
  - **The archive is `unreal/dist/MatterRuntime-Linux.tar.gz` on this machine.** `unreal/RUNTIME.json` still pins v3. Publishing is the lead's: push, then `unreal/publish.sh 4`, then commit and push `RUNTIME.json`. **This is AT-Q5, half done.** *(Published the same day as `unreal-runtime-v4`: AT-RD3.)*
- **AT-F27 — A4's page is written** (`7c7ee66`): `tools/parity/JOB_FORMAT.md` §The Unreal job, and what a second project may call. The app's job file as a field table read off its reader, `sun_scale`, `sky_scale` and the `Sky` master among them; the ten functions and five names of AT-F6 as what a caller may lean on, each signature read back from the module; and how to tell which masters a pinned runtime carries. Two things the page says that nothing said before:
  - **A parameter name the master does not have is ignored, and nothing says so.** The app sets parameters by name and Unreal drops an unknown one silently. `article_material()` refuses what it knows the masters lack; a name written by hand is checked by nobody.
  - **The first setting of a launch may be drawn as Unreal's default material**, which is what `warmup()` is for.
- **AT-F28 — A2 and A3 are written** (`2b5d79e`). `CreatorAssetProfile.md` rule 10: faces are wound counter-clockwise seen from outside, at USD's default `orientation`; whether a face's back is drawn belongs to the material's master; a mesh's `doubleSided` is free and never makes a face show; and which tools show a backward face and which do not (AT-F13). The golden's two Copper meshes carry `doubleSided = 0`; both boxes hold a positive volume, so every face is wound outward, and Storm's pictures of both golden forms are the same pixel for pixel as before. `assert_profile.py` refuses `orientation = "leftHanded"`, the one part of the rule a text check can hold, and fails the golden with one mesh made left-handed.
  - **Known and left:** the exporter's gate exports from a scaffold file whose Copper has the switch off, so its output still says `doubleSided = 1`. It conforms.
- **AT-Q3, as it stands.** The profile carries a dated `Todo` for the face-direction check and names the asset tooling's as the one on offer. **The library wants it** (AT-RD1). It is the asset tooling's to hand over, under this repository's licence; nothing of it was copied here.

### Reproduction (AT-F24)

One launch, about eight seconds on this machine. `MATTER_UNREAL_RUNTIME=<a launcher>` points it at another build.

```python
# uv run python <this> <out dir> [label]      (from the repo root)
# The Emissive master alone: black base, sun and sky scaled to zero, emission_luminance 1,
# one setting per emission_color. Reads the cube's pixels off the float captures.
import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, "tools/parity/drivers"); sys.path.insert(0, "tools/parity")
import unreal as U

out = Path(sys.argv[1]).resolve()
ART = Path("MatterLibrary/materials/utility/emissive/Neon_Signage_Clean_Base_s01_v01.mtlx").resolve()
COLOURS = [(1, 0.15, 0.75), (1, 1, 1), (0.993, 0.992, 1), (1, 0.456, 0.147), (0, 0, 1), (0, 0, 1 / 3),
           (0, 2 / 3, 1 / 3), (1 / 3, 1 / 3, 2 / 3), (0.5, 0.5, 0.5), (0.2, 0.2, 0.2), (1, 0, 0), (1, 1, 0)]
job = {"article": {"path": str(ART), "meters_per_tile": 1.0}, "width": 64, "out_dir": str(out),
       "subjects": ["/World/Subjects/Sphere", "/World/Subjects/Cube", "/World/Subjects/Floor"],
       "settings": [{"id": "defaults", "set": {}}], "views": {"wide": {"camera": "/World/Cam", "suffix": ""}}}
folder = out / "unreal" / "job"
ujob = U.unreal_job(job, folder)
spec = json.loads(ujob.read_text())
first, mask_s = spec["settings"][1]["materials"], spec["settings"][-1]
names = ["Sphere", "Cube", "Floor"]
settings = [{"id": U.WARMUP_ID, "materials": first}]
for i, c in enumerate(COLOURS):
    m = U.article_material(ART, {"emission_color": list(c), "emission_luminance": 1.0})
    m["vectors"]["base_color"] = [0.0, 0.0, 0.0]
    m["scalars"]["base_weight"] = 0.0
    settings.append({"id": f"c{i}", "materials": first | {n: m for n in names}, "sun_scale": 0.0, "sky_scale": 0.0})
spec["settings"] = settings + [mask_s]
ujob.write_text(json.dumps(spec, indent=1) + "\n")
cmd = U.find_runtime()
print("runtime:", cmd)
U.run_runtime(cmd, ujob, out / "unreal.log")
raw = folder / "raw"
mask = U.read_pfm(raw / f"{U.MASK_ID}.pfm")
cube = (mask[..., 1] > 0.9) & (mask[..., 0] < 0.1) & (mask[..., 2] < 0.1)
print("cube pixels:", int(cube.sum()))
rows = []
for i, c in enumerate(COLOURS):
    px = U.read_pfm(raw / f"c{i}.pfm")[cube] / U.EXPOSURE_K
    read = np.median(px, axis=0)
    c = np.array(c, float); length = float(np.linalg.norm(c))
    k = [read[j] / c[j] for j in range(3) if c[j] > 0]
    rows.append({"colour": [round(float(x), 4) for x in c], "length": round(length, 4),
                 "read": [round(float(x), 4) for x in read], "read_over_colour": round(float(np.mean(k)), 4),
                 "times_length": round(float(np.mean(k)) * length, 4)})
    print(rows[-1])
(out / "emission.json").write_text(json.dumps(rows, indent=1) + "\n")
```

---

## Pass 4 — From the asset tooling's side: the check handed over, and the library's answer read (2026-10-11)

*Written from the asset tooling's side, at `4901203`. The lead, to the question of whether its face-direction check should be copied here now, held there or given over, verbatim: "I want the right checks in the right locations - feel free to put there where needed. a is fine", where (a) was a dated copy handed over now, marked as taken from the asset tooling, and replaced by a pin when that project is public (§Resolved, AT-RD3). Built as one quick fix outside this doc.*

- **AT-F29 — The face-direction check is here: `tools/conformance/check_facing.py`.** This answers AT-Q3 and closes the third thing owed.
  - **A dated copy**, its header says so: the check is defined and tested in the asset tooling. Change it there and bring a new copy; do not edit it here.
  - **Its self-test, `test_check_facing.py`, is new and is the library's own:** nine cases on small meshes it writes itself. A box wound outward passes; one face turned is refused; an inside-out box is refused; each is read rightly when the mesh is marked left-handed or mirrored by its transform; a sheet is counted and not refused; the golden passes.
  - **The conformance gate runs it** as step 3b: the self-test first, then both forms of the golden. `check_conformance.sh` passes on this machine with it, every step.
  - **The profile's rule 10** names the file where its Todo stood, and its history has a line.
  - **Not done, and the library's to decide:** no lane of `run_all.py` was added or changed. The ledger row M8 still says the check is to be handed over.
- **AT-F30 — Writing the self-test corrected the asker.** The first expectation written for a mirrored box was that it is refused. By USD's rule a mirroring transform turns the winding round with it, the check already allowed for that, and the test now holds it to it. **What is not known: whether a consumer honours it.** The rig's driver takes points that are already placed, and the asset tooling's reader turns a mirrored mesh's faces round before handing them over; how Studio draws a mirrored asset has not been looked at.
- **AT-F31 — The library's answer, read on the asset tooling's side.**
  - Its probe calls only what `JOB_FORMAT.md` now names, and asks for the app with `fetch=False` unless told to fetch. Two names it had borrowed outside that list are gone from it.
  - Rule 10 and the *free* reading of `doubleSided` are recorded there. Its prop conforms under the new asserter and needs no change.
  - AT-F13's two corrections are taken: Storm draws a face seen from behind whatever the flag says, and Cycles does not read the switch. The asset tooling had written that Storm drew it *because* of the flag.
  - **Not run: its picture of the prop on `unreal-runtime-v4`.** Another Unreal application had the graphics card. Its count of missing faces reads hue alone, so the light repair should not move it; that is reasoned, not measured.
- **Still open, and the library's:** the tracked Blender asset file is not regenerated, so a builder's export still says `doubleSided = 1` on every mesh today · AT-Q4, a sheet on a one-sided master.

---

## Resolved

- **AT-RD3 — The asset tooling's face-direction check is handed over as a dated copy (the lead, 2026-10-11).** Verbatim: *"I want the right checks in the right locations - feel free to put there where needed. a is fine"*. The check stays defined and tested in the asset tooling; the copy here gives way to a pinned version when that project is public (Pass 4, AT-F29).
- **AT-RD1 — Build all of it (the lead, 2026-10-11).** Pass 2's handback listed six next steps: A5, A1 with the asset file regenerated, A4's page, the ruling on `doubleSided`, one runtime build carrying the coat change and the emission repair, and a ledger row with the face-direction check. The lead, verbatim: *"yes, lets do it all... prep the work needed. or do it.. wither way"*. Done the same day, as quick fixes outside this doc (Pass 3), short of three things that are not this machine's or not an agent's: regenerating the tracked Blender asset file, publishing the runtime (done the same day, AT-RD3), and handing over the asset tooling's check.
- **AT-RD3 — The runtime is published as `unreal-runtime-v4` (the lead, 2026-10-11).** To Pass 3's handback, verbatim: *"push and publish runtime v4"*. Pushed at `47954ea`; `unreal/publish.sh 4` published the archive Pass 3 tested (sha256 `99c73f74…`, a pre-release tagged on that commit) and `unreal/RUNTIME.json` pins it. Fetched back through the pin by the driver, the published copy gives the same twelve emission readings as the build tested before publishing, 1.0005 to 1.0010 of what is asked. This answers AT-Q5: a master change that alters pictures at its defaults gets a new runtime.
- **AT-RD2 — A mesh's `doubleSided` is free in a conforming asset (taken 2026-10-11, on AT-RD1).** It is not a conformance rule and never makes a face show; the library's own route and golden write it in agreement with the master. This was the library's recommendation in Pass 2's handback, and the lead's go-ahead named no other option. **It was not ruled on by itself.** It is one commit (`2b5d79e`) and reverts as one, if the lead wants *"must agree with the master"* instead.

---

## Status

- **Passes captured:** 4, all 2026-10-11. Pass 1 is the asset tooling's side; Pass 2 is the library's review; Pass 3 is what the library built; Pass 4 is the asset tooling's side again: its check handed over. *(Was, at Pass 2: "2 … Nothing is ruled, and nothing is built".)*
- **Asks:** **A1 built** in the loader; the tracked Blender asset file is not regenerated, so an installed library does not carry it yet (AT-F23). **A2 and A3 written:** the profile's rule 10, with `doubleSided` taken as free (AT-RD2). **A4's page written**, and a runtime carrying the moved masters built (AT-F26, AT-F27) and **published as `unreal-runtime-v4`** (AT-RD3). **A5 built** (AT-F22).
- **Questions:** AT-Q1 answered: passes here and ledger row **M8**, written. AT-Q2 answered: no, and repaired (AT-F25). AT-Q3 answered: handed over as a dated copy and in the gate (Pass 4, AT-F29). *(Was: "the library wants the check; it is the asset tooling's to hand over".)* AT-Q6 answered: the colour's direction only (AT-F24). AT-Q5 answered: published (AT-RD3). **Open:** AT-Q4 (sheets on a one-sided master: twelve articles, and nobody has ruled).
- **Owed, in order.** (1) ~~The lead: push, `unreal/publish.sh 4`, commit and push `unreal/RUNTIME.json`.~~ **Done 2026-10-11 (AT-RD3).** (2) The library machine: regenerate `MatterLibrary.blend`. (3) The asset tooling: ~~pass `fetch=False` where it only asks; hand over its face-direction check~~ **both done (Pass 4)**; expect its pictures of coated and emissive assets to change at the new runtime, **not yet looked at on v4**. (4) A ruling on AT-Q4, whenever a sheet first looks wrong.
- **What changed outside this doc** (Pass 3, six commits): `tools/parity/drivers/unreal.py`, `tools/parity/JOB_FORMAT.md`, `blender/masters/build_masters.py` and `load_article.py`, `tools/conformance/verify_asset_library.py` and `assert_profile.py`, the lightweight golden, `unreal/MatterRuntime/Scripts/build_masters.py`, `docs/specs/Ontology/MasterSet.md`, `docs/specs/Contract/CreatorAssetProfile.md`, `docs/Learnings/Unreal/Unreal.md`, `docs/Planning/PlatformDependencies.md`. **Not changed:** any article, any texture, the add-on, the app's source, the tracked asset file. *(`unreal/RUNTIME.json` changed afterwards, at the publish: AT-RD3.)*
- **Measured in Pass 3:** AT-F22 – AT-F26 and AT-F28's checks. **Still not run:** AT-F6 is not repeated on the asset tooling's own prop (its scripts are private). **Still the asset tooling's reading:** how Studio treats `doubleSided` (AT-F1). **Pass 2's standing corrections:** AT-F14 named a retired file and is corrected in place; AT-F21's rule, worked out from records, is now measured (AT-F24).
- **▶ Next:** the library machine regenerates the Blender asset file (the second item owed); it also takes `unreal-runtime-v4` on its next rig run. *(Was: "the lead's push and publish", done.)*
