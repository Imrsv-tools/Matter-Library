# The parity rig's render job — the contract a renderer driver implements

*Written at the Phase05 close (2026-09-27) as the hand-off to Phase06 (the Unreal test runtime).*
*The code is the authority where this page and it disagree: `tools/parity/job.py` writes a job,
`drivers/storm.py` and `drivers/blender_render.py` are the two reference drivers.*

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
              "master": "Opaque | TwoLayer | Masked | Emissive | TranslucentThin | TranslucentThick | Subsurface",
              "meters_per_tile": 0.1},
  "scene": "<abs path to tools/parity/scene/test_scene.usda>",
  "camera": "/World/Cam",
  "views": {
    "wide":  {"camera": "/World/Cam",      "suffix": ""},
    "close": {"camera": "/World/CamClose", "suffix": "__close"},
    "dim":   {"camera": "/World/Cam",      "suffix": "__dim", "exposure": -4.0}
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
| `views` | Render **every setting from every view**. The `dim` view exists only for an **Emissive** article: the same camera at `exposure` stops (a multiply by 2^exposure in linear light, before the display encode). |
| `subjects` | The three meshes the article is bound to. Everything else (the ruler, the UV-grid wall) is scene furniture with UsdPreviewSurface materials. |
| `width` | Square output, `width` × `width`. |
| `samples` | A path tracer's samples per pixel (Blender: Cycles, denoised). |
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
            "hand": {"camera": "/World/CamHand", "suffix": "__hand", "label": "hand"}}
}
```

| Field | Meaning for a driver |
|---|---|
| `bindings` | Build each distinct article on its master once, and assign it to its `subject`. A test-scene job has no `bindings`: `article` goes on every subject. `article` is still present (the first binding), for a driver that reads only it. |
| `mask_colours` | The mask's flat colour per subject (the test scene's default is sphere red, cube green, floor blue). The rig scores each colour as its own region. |
| `settings` | The defaults only. Sliders are swept on the test scene. |

- **The parts** are the body, the eyes, the teeth and the tongue (more come with Phase07 7.5). An **unbound** part keeps the scene's grey `UsdPreviewSurface` (`/World/Looks/Unbound`).
- **UVs:** the scene's `st` is in **metres per part**, like the test scene's subjects. MakeHuman's own UVs are one 0–1 atlas over the whole body (1 UV unit ≈ 1.69 m on the body), so the build scales each part's UVs by its measured median density; the setting scene then divides the bound parts' `st` by the article's `meters_per_tile`. The atlas's islands are not all at the median (body p5–p95: 0.8–2.6 m per UV unit), so detail still varies in size across the body. **An Unreal driver must import the setting scene's `st`, not the mesh's own UVs.**
- **No floor and no wall:** the dome is the background. The lighting rules below (matched lighting, colour, units) are unchanged.

## What a driver writes

- `<out_dir>/<tool>/<setting id><view suffix>.png` — 8-bit sRGB, `width` × `width`, one per setting per view.
- The masks are written once, by the Blender driver: `<out_dir>/mask<view suffix>.png`, one flat colour per subject (sphere red, cube green, floor blue) on black. Another driver does not need to write them.

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

## The test set (11 articles)

`GreyCard_Neutral18` (calibration) · `ABS_Glossy` · `Copper_Verdigris_Aged` (sweep) · `Oak_Natural` (sweep) · `Rust_OnSteel_Flaking` (TwoLayer) · `Lace_Floral` (Masked) · `Neon_Signage` (Emissive) · `Glass_Clear` and `Glass_Green` (TranslucentThin) · `Diamond_Brilliant` (TranslucentThick) · `Marble_Veined_Polished` (Subsurface).

**Start Unreal on the grey card:** it proves the lighting, colour and camera before any material is judged. At the Phase05 close Storm and Blender agreed on it at 0.35 ΔE2000, with linear radiance within 1–2 % everywhere.

## Open questions Unreal's column should settle

These are recorded in the Phase05 doc as F12 and F16.

- **F12:** Blender renders the wear layers' bump tilt more strongly than Storm (Oak close-up, dust at 1: 1.41 against 0.82). The cause is not established; the suspect is each renderer's tangent frame for normal maps.
- **F16:** Marble's colour. OpenPBR's graph mixes the base colour towards `subsurface_color` by `subsurface_weight`, and Blender follows that; Storm shows more of the base colour's veins. **Update (2026-09-27, Phase07 7.1): mostly the 1/100-scale bug above, not the colour mix.** At the right scale Marble measures **2.60** (was 3.95), so what is left is small. Unreal's column still settles the remainder. Diamond (absorption depth) was measured at the wrong scale too, and is re-measured in Phase07 7.3.
