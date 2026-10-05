# The parity rig's render job — the contract a renderer driver implements

*Written at the Phase05 close (2026-09-27) as the hand-off to Phase06 (the Unreal test runtime).*
*The code is the authority where this page and it disagree: `tools/parity/job.py` writes a job,
`drivers/storm.py` and `drivers/blender_render.py` are the two reference drivers, and
`drivers/unreal.py` (Phase06) is the third: §The Unreal driver below.*

A **render job** asks a renderer for pictures of **one material**, under **a list of slider
settings**, in **one test scene**, from **a few fixed views**. The rig (`rig.py`) writes the job,
runs every driver on it, then compares the pictures. A new renderer (Unreal) joins by adding a
driver that reads the same job and writes its pictures under its own folder, `<out_dir>/unreal/`.
The sheet already has an Unreal column; it fills once those files exist.

```
uv run tools/parity/rig.py <article> [--sweep]      # writes the job, runs the drivers, scores
<driver> <out_dir>/job.json                          # what each driver is given
```

## `job.json`

```json
{
  "format": 1,
  "article": {"name": "<stem>", "path": "<abs path to the .mtlx>",
              "master": "Opaque | TwoLayer | Masked | Hair | Emissive | TranslucentThin | TranslucentThick | Subsurface",
              "meters_per_tile": 0.1},
  "scene": "<abs path to tools/parity/scene/test_scene.usda>",
  "camera": "/World/Cam",
  "views": {
    "wide":  {"camera": "/World/Cam",      "suffix": ""},
    "close": {"camera": "/World/CamClose", "suffix": "__close"},
    "dim":   {"camera": "/World/Cam",      "suffix": "__dim", "exposure": -4.0},
    "side":  {"camera": "/World/CamSide",  "suffix": "__side", "hide": ["/World/Subjects/Sphere"]}
  },
  "subjects": ["/World/Subjects/Sphere", "/World/Subjects/Cube", "/World/Subjects/Floor"],
  "width": 512,
  "samples": 128,
  "storm_supersample": 4,
  "settings": [
    {"id": "defaults", "label": "defaults", "set": {}, "scene": "<abs>/scenes/defaults.usda"},
    {"id": "roughness_m05", "label": "roughness -0.5", "port": "roughness_bias",
     "set": {"roughness_bias": -0.5}, "scene": "<abs>/scenes/roughness_m05.usda"}
  ],
  "out_dir": "<abs path>"
}
```

| Field | Meaning for a driver |
|---|---|
| `article.path` | The article to render. A driver that cannot evaluate MaterialX directly (Blender, Unreal) builds the material on its own master for `article.master`, from the `.mtlx` (Blender: `blender/masters/load_article.py`). |
| `article.meters_per_tile` | Already applied: each setting's scene rescales the subjects' `st` by it. A driver does nothing with it. |
| `views` | Render **every setting from every view**. The `dim` view exists only for an **Emissive** article: the same camera at `exposure` stops (a multiply by 2^exposure in linear light, before the display encode). The `side` view *(added 2026-10-05)* exists only for a **see-through** article (TranslucentThin, TranslucentThick): the cube's flat front face from the side, the wall behind it, with the prims in its `hide` left out of the picture and of its mask, as a character view's are. It is the view that shows whether what is seen through the article is moved: a thin wall must leave the wall's lines straight, a solid must move them ([MasterSet](../../docs/specs/Ontology/MasterSet.md) §Material-settings intent). |
| `subjects` | The three meshes the article is bound to. Everything else (the ruler, the UV-grid wall) is scene furniture with UsdPreviewSurface materials. |
| `width` | Square output, `width` × `width`. |
| `samples` | A path tracer's samples per pixel (Blender: Cycles, denoised). The Blender driver renders on the first device that can actually render, OptiX, then CUDA, then the CPU, and names it in `blender.log`; a listed graphics device that cannot render is passed over *(2026-10-05; before it, the job failed)*. `MATTER_BLENDER_DEVICE=cpu` or `=gpu` forces the choice. The CPU's pictures differ from the card's by noise only (measured on Glass_Clear: under half an 8-bit code on average). |
| `storm_supersample` | Storm only: it renders at `width × n` and is box-filtered down, because `usdrecord` has no anti-aliasing. A real-time renderer with its own anti-aliasing can ignore it; one without should do the same. |
| `settings[].set` | The Creator sliders to move from the article's own values, by frozen port name (LCDSchema §Creator subset): floats, `[x, y]` for `uv_scale`/`uv_offset`, `[r, g, b]` for `base_color_tint`. |
| `settings[].scene` | A USD file per setting that sublayers the test scene and adds the article (referenced at `/World/Library`, bound to the subjects), the subjects' rescaled `st`, and each moved slider **by the carrier rule** (a value on the bound Material's `inputs:<port>`, connected from `NG_<stem>`). A driver that imports USD can load this file; one that cannot reads `set` instead. |

## The character job *(added 2026-09-27, Phase07 step 7.4)*

`rig.py --character [<skin>]` renders the **MakeHuman body** (`scene/character_scene.usda`, built by `scene/build_character.py` from pinned CC0 sources) with **one article per part**. The job carries three more fields, and a driver that reads them handles both kinds of job:

```json
{
  "mode": "character",
  "bindings": [{"subject": "/World/Character/Body", "article": {"name": "…", "path": "…", "master": "Subsurface", "meters_per_tile": 0.01}}],
  "subjects": ["/World/Character/Body"],
  "mask_colours": {"/World/Character/Body": [1, 0, 0]},
  "views": {"wide": {"camera": "/World/Cam", "suffix": "", "label": "whole body"},
            "face": {"camera": "/World/CamFace", "suffix": "__face", "label": "face"},
            "mouth": {"camera": "/World/CamMouth", "suffix": "__mouth", "label": "mouth, face hidden",
                      "hide": ["/World/Character/Body", "/World/Character/Lips"]},
            "…": "hand, waist, feet"}
}
```

| Field | Meaning for a driver |
|---|---|
| `bindings` | Build each distinct article on its master once, and assign it to its `subject`. A test-scene job has no `bindings`: `article` goes on every subject. `article` is still present (the first binding), for a driver that reads only it. |
| `mask_colours` | The mask's flat colour per subject (the test scene's default is sphere red, cube green, floor blue). The rig scores each colour as its own region. |
| `settings` | The defaults only. Sliders are swept on the test scene. |
| `bindings[].cutout_map` | *(Phase07 7.6)* The mesh's cut-out map (a one-channel PNG, white = strand), on a cut-out part (`Hair`, `Brows`, `Lashes`) bound to an article that declares `cutout_map` ([LCDSchema §Cut-out map](../../docs/specs/Contract/LCDSchema.md#cut-out-map-the-meshs-supplied-at-binding)). Build one material per (article, map): the setting scene does the same, one `Library_<i>` Material instance per map carrying `asset inputs:cutout_map` connected into the article. Sample it on the mesh's `st` **directly** (not through the article's placement), feed the master's opacity: **Masked** thresholds it at the article's `opacity_cutoff`; **Hair** *(Phase08 8.1)* takes it as soft coverage, unthresholded. Absent: no map, so the card is solid. *(Phase09: the map comes from the library's fit set, `MatterLibrary/textures/fit/makehuman/`.)* |
| `bindings[].base_color_map` | *(Phase09 9.1)* The mesh's picture (an sRGB PNG from the fit set), on a fit part bound to an article that declares `base_color_map` ([LCDSchema §Base colour map](../../docs/specs/Contract/LCDSchema.md#base-colour-map-the-meshs-picture-supplied-at-binding)). One material per (article, maps), as for `cutout_map`; sample it on the mesh's `st` directly and **multiply** it into the article's base colour ahead of the tint. Absent: the article's own colour. |
| `views[].hide` | Prims to hide for that view only *(Phase07 7.5)*. The `mouth` view hides the body and lips, because MakeHuman's mouth is closed. Storm: `token visibility = "invisible"` in the view's wrapper layer. Blender: `hide_render`. The mask for that view leaves them out too. |

- **The parts** (one per substance, Phase07 ruling L1): `Body`, `Lips`, `Nails`, `Cornea`, `Pupil`, `Iris`, `Sclera`, `Teeth`, `Gums`, `Tongue`, `Shirt`, `Trousers`, `Shoes`, *(Phase08 8.3)* `Soles` (the shoe's underside island plus the four edge loops above it, a `grow` rule: the sole slab up to the upper's seam), and (7.6) the cut-out cards `Hair`, `Brows`, `Lashes` (MakeHuman's CC0 `bob02`, `eyebrow001` and `eyelashes01`, two-sided). `build_character.py` splits MakeHuman's meshes into them by a per-face rule (MPFB2's CC0 region masks for lips and nails; the eye's and the teeth's own textures; a UV rectangle for the jeans), and drops the body faces a garment's `.mhclo` marks as covered, as MakeHuman does. An **unbound** part keeps the scene's grey `UsdPreviewSurface` (`/World/Looks/Unbound`).
- **The cast** (`rig.py` `CHARACTER_CAST`, `cast_for`): the skin is the positional argument, and *(Phase08 8.2)* its tone's lips and nails come with it by the shared Variant token (`Skin_FitzpatrickIV` → `Lips_FitzpatrickIV`, `Nail_FitzpatrickIV`); a skin with no such pair keeps `Lips_Natural` and `Nail_Natural`.
- **The views:** whole body, face, hand, mouth (face hidden), waist, feet.
- **Scoring:** each part is its mask colour, **and a pixel counts only when its eight neighbours are the same colour**, so an anti-aliased edge between two parts (whose blend can equal a third part's colour) is in no region. Parts behind the cornea (iris, pupil, sclera) are scored as the cornea: the eye as seen.
- **UVs:** the scene's `st` is in **metres per part**, like the test scene's subjects. MakeHuman's own UVs are one 0–1 atlas over the whole body (1 UV unit ≈ 1.69 m on the body), so the build scales each part's UVs by its measured median density; the setting scene then divides the bound parts' `st` by the article's `meters_per_tile`. The atlas's islands are not all at the median (body p5–p95: 0.8–2.6 m per UV unit), so detail still varies in size across the body. **An Unreal driver must import the setting scene's `st`, not the mesh's own UVs.** The exception is a cut-out part (7.6): its `st` stays the source atlas its map is drawn on, and it is not rescaled.
- **No floor and no wall:** the dome is the background. The lighting rules below (matched lighting, colour, units) are unchanged.

## What a driver writes

- `<out_dir>/<tool>/<setting id><view suffix>.png` — 8-bit sRGB, `width` × `width`, one per setting per view.
- The masks are written once, by the Blender driver: `<out_dir>/mask<view suffix>.png`, one flat colour per subject (sphere red, cube green, floor blue) on black. Another driver does not need to write them. *(Phase06: the Unreal driver also writes its own, `<out_dir>/unreal/mask<view suffix>.png`, which the rig scores on when Blender is not run, `--no-blender`.)*

## The scene, and why each number is what it is

`tools/parity/scene/test_scene.usda`, generated by `scene/build_scene.py`: Y up, metres. Keep a driver's scene **identical**; each item below was measured in Phase05.

- **Units: metres, in every file a driver loads** *(added 2026-09-27, Phase07 step 7.1)*. USD reads `metersPerUnit` and `upAxis` from the **root layer only**. Each setting's scene sublayers the test scene, so it must author both itself, and since Phase07 7.1 it does. Before then it authored neither, so Blender took USD's default of centimetres and imported every scene at **1/100 scale**. That was invisible on opaque matter, but every distance a material states (subsurface radius, absorption depth) acted 100x too long. **An Unreal driver that imports a setting scene must honour its `metersPerUnit`**, or it repeats the bug.

- **Subjects:** a 0.18 m sphere, a 0.30 m rounded cube, and a 1 m × 1 m floor that is a **2 cm slab**. A plane won't do: volumes and subsurface need a closed solid. The UVs are in metres.
- **Furniture:** a 10 cm ruler of 1 cm black and white cells on the floor, and a UV-grid wall behind the objects so see-through materials have something to show.
- **Lights:**
  - a dome whose texture is a constant 0.503 (sRGB code 188), at intensity 1;
  - a sun at `normalize = true`, intensity 1.5 (irradiance), angle 0.53°, rotated (−40°, 35°, 0).
  - Storm needs both details. It ignores an untextured dome, and an un-normalized distant light's intensity is the sun disk's radiance (×~6.7e-5).
  - The levels keep a white surface in full sun under display white.
- **Matched lighting:** each point is lit by the unoccluded dome and the sun, with **no shadows, no bounce light and no reflections of other objects**, because Storm can do none of the three. Blender holds itself to the same by making every mesh invisible to shadow, diffuse and glossy rays, and keeping transmission rays so glass still shows the wall. **An Unreal driver must match this, or its column measures the lighting, not the material.** For Unreal that means no shadows, no Lumen/GI bounce, and reflections of the dome only.
- **Colour:** no tone curve. A plain sRGB encode: Storm's `sRGB` colour correction, Blender's `Standard` view transform. In Unreal, turn off the filmic tonemapper and auto-exposure.
- **Cameras:** 50 mm focal length, 36 mm square aperture.
  - `/World/Cam` at (0, 0.48, 1.95), pitched −11°.
  - `/World/CamClose` at (0.10, 0.34, 0.58), pitched −20.2° and yawed −12.5° (rotateXYZ: X, then Y).
  - `/World/CamSide` *(2026-10-05)* at (0.96, 0.29, 0.74), pitched −8° and yawed 50°: 0.95 m from the cube's front face, 50° off that face's normal at its centre (43° to 55° across it). Every ray through the face meets the wall undeflected, inside the wall's width. Through 0.30 m of solid glass at this angle the wall should move about 12 cm sideways; through a thin wall, not at all. The other two views see this face too nearly head-on to show it (the close-up is 24° off).

## The test set (11 articles)

`GreyCard_Neutral18` (calibration) · `ABS_Glossy` · `Copper_Verdigris_Aged` (sweep) · `Oak_Natural` (sweep) · `Rust_OnSteel_Flaking` (TwoLayer) · `Lace_Floral` (Masked) · `Neon_Signage` (Emissive) · `Glass_Clear` and `Glass_Green` (TranslucentThin) · `Diamond_Brilliant` (TranslucentThick) · `Marble_Veined_Polished` (Subsurface).

**Start Unreal on the grey card:** it proves the lighting, colour and camera before any material is judged. At the Phase05 close Storm and Blender agreed on it at 0.35 ΔE2000, with linear radiance within 1–2 % everywhere.

## The Unreal driver *(Phase06, 2026-09-30)*

`drivers/unreal.py` renders a job in the library's own Unreal app (`unreal/MatterRuntime`, Unreal 5.8, Substrate on). What it does with each field, and the choices a reader of its column needs:

- **The runtime, first found wins:** `$MATTER_UNREAL_RUNTIME` (a packaged build's `MatterRuntime.sh`); `$MATTER_UNREAL_EDITOR` (an `UnrealEditor`, editor mode on the project: the development loop); else the build **`unreal/RUNTIME.json`** pins, a GitHub pre-release of this repo (`unreal-runtime-vN`), downloaded once into the git-ignored `unreal/package/` and checked by sha256. None: the rig skips the column and says why. No Unreal install is needed to render the column.
- **The scene is not imported from USD.** Epic's USD importer is editor-only, so a packaged runtime cannot use it, and each setting rescales `st`. The driver converts the rig's meshes and cameras from the same generators that write the USD (`scene/build_scene.py`, `scene/build_character.py`) into an **Unreal job** (`<out_dir>/unreal/job/unreal_job.json`, job format 2: float mesh buffers with a tangent sign per vertex). Metres → centimetres, Y up → Z up, right- → left-handed by `(x, y, z) → 100 (−z, x, y)`, whose determinant −1 keeps USD's front faces as Unreal's; §Units is honoured by construction. A character part's faceVarying `st` becomes one vertex per (point, uv) pair.
- **The material:** the article is read by the one shared reader (`blender/masters/article.py`), and set on its master (`unreal/MatterRuntime/Scripts/build_masters.py`) under the article's own names. A master or input Unreal does not carry is refused by name, and the sheet shows *"not yet"* instead of a wrong picture. A binding's `cutout_map` is sampled on the mesh's own `st`. A binding's `base_color_map` is the master's own `base_color_map_tex` (Opaque, Masked, Hair, Subsurface; Phase09 9.3), sampled on the mesh's own `st` on a part whose `st` is its atlas; on Subsurface it also scales the subsurface colour, which is exact for an article whose subsurface colour is connected to an untinted, untextured base (F-P09-5) and refused otherwise. *(Through 9.1–9.2 it rode the v1 masters' `base_color_tex`, F-P09-14; job format 3 makes an older runtime refuse the job rather than drop the picture.)*
- **Colour and light:** the app writes linear scene colour (exposure fixed, no tonemapper); the driver applies the view's `exposure`, box-filters the **4× supersampling** (Unreal renders with no anti-aliasing here) and does the plain sRGB encode. No shadows, no GI, no Lumen or screen-space reflections: §Matched lighting. The dome is an unlit sphere of constant radiance that a sky light captures. **The calibration** (`unreal.py --calibrate [--ref storm|blender] <grey card job.json>`): `EXPOSURE_K` from a view of the dome, **`DOME_K` from a white mirror** (which reflects exactly the dome, so no material model is in it), then **`SUN_K` on the grey card with the dome fixed**. The constants in the file were fitted against Storm on the UE machine; Blender is the path-traced reference, so re-fit with `--ref blender` where Blender renders parity.
- **Each launch opens with a throwaway `__warmup` setting** (a copy of the first). The launch's first material assignment can draw a master as Unreal's default material while the runtime reports ready (seen on the character, every launch); the warm-up absorbs it. Its pictures are written and never read.

## Open questions Unreal's column should settle

These are recorded in the Phase05 doc as F12 and F16.

- **F12:** Blender renders the wear layers' bump tilt more strongly than Storm (Oak close-up, dust at 1: 1.41 against 0.82). The cause is not established; the suspect is each renderer's tangent frame for normal maps.
- **F16:** Marble's colour. OpenPBR's graph mixes the base colour towards `subsurface_color` by `subsurface_weight`, and Blender follows that; Storm shows more of the base colour's veins. **Update (2026-09-27, Phase07 7.1): mostly the 1/100-scale bug above, not the colour mix.** At the right scale Marble measures **2.60** (was 3.95), so what is left is small. Unreal's column still settles the remainder. *(Phase06, 2026-09-30: Unreal against Storm reads 2.43, and 6.4 measured the difference as a uniform ×1.11 brightness; the three-way reading waits for Blender's column on the other machine.)* Diamond (absorption depth) was measured at the wrong scale too, and is re-measured in Phase07 7.3.
