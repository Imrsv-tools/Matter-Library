# Research — Which side of a face is drawn: what IMRSV's asset tooling found, and what it asks of the library

**Opened:** 2026-10-11 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `AT` (ids `AT-Qn`, `AT-Fn`). **Pass 1** is written from the asset tooling's side. The library's review of it against its own tree is a later pass, as in `261005_R_PlatformThinGlassAsks.md`.
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

## Status

- **Pass 1 only**, from the asset tooling's side. Nothing here is reviewed against the library's tree by the library, and nothing is ruled.
- **Asked:** A1 – A5. **Questions:** AT-Q1 – AT-Q3.
- **Measured:** AT-F2, AT-F3 (reproduction above), AT-F6, AT-F8. **Read, not measured:** how Studio treats `doubleSided` (AT-F1), Eevee and Cycles (AT-F4). **Measured once, captures not kept:** AT-F7.
- **▶ Next:** the library's review, as a Pass 2 here.
