# Matter Library

**A community library of physically based materials, authored once in MaterialX and published as versioned releases that Blender, Unreal-based apps and USD tools can all use.**

> *"Author once, render close to the same everywhere."*

The library holds three kinds of thing, each browsed by its own taxonomy:

- **Matter**: materials catalogued by **what things are made of** (stone, metal, glass, plastic, textile, …), not by the objects they appear on.
- **Character**: what a character wears (skin, eyes, teeth, hair, nails, clothing fabrics), organised by species and then part, plus makeup and marks placed on the skin.
- **HDRIs**: a scene's lighting picture, chosen by name.

Every material is:

- **One MaterialX file**, using OpenPBR (`open_pbr_surface`, MaterialX 1.39): the single source of truth. Blender and Unreal forms are derived from it, never hand-authored.
- **Physically scaled**, with a scale tag recording real-world meters per texture tile.
- **Built on a small, fixed set of masters**: Opaque, Masked, TranslucentThin, TranslucentThick, Subsurface, TwoLayer, Emissive. So it behaves predictably in every renderer.
- **Driven by one shared set of controls that every renderer can take** (the LCD vocabulary), each with one meaning and one range, so a setting moves every renderer the same way. The controls are shared, not the quality: each renderer's master still makes the material look as good as that engine can.
- **Self-describing**: its file carries its readable name, a one-line description, search words, its contributor and its licence.
- **Free to use.** Materials and textures are **CC0**: no rights reserved, commercial use included.

## How it's organised

| Tier | What it is | Where |
|---|---|---|
| **Source collection** | every material, texture, makeup piece and HDRI, open to community contribution. Matter is organised by Domain / Class, Character by species / part | `MatterLibrary/` (`materials/`, `textures/`, `makeup/`, `hdris/`) |
| **Versioned library** | curated releases: a manifest pins exact material and texture versions, and each release is frozen and reproducible. Each release also publishes a catalog of everything apps and the website show about each entry | `library/releases/` |

Materials are named `Material_Variant_Condition_Detail_sNN_vNN` (for example `Copper_Verdigris_Aged_Base_s01_v01`). A material's own version (`vNN`) and the library's release version (`matterlib-X.Y.Z`) are separate.

## Using it

- **In Blender (5.1+):** the Asset-Browser library (`blender/asset_library/`) lets you assign Matter materials, and the Matter add-on (`blender/addons/imrsv_lcd_export/`) exports USD in one of two forms: a lightweight one that references the library, or a self-contained portable one. To set it up, add the `blender/asset_library/` folder under *Preferences → File Paths → Asset Libraries* and set that library's **Import Method** to **Append (Reuse Data)**: Blender's default for a new library links the material read-only, which greys out every slider.
- **In a USD tool:** reference an article by name (`@Name.mtlx@`) and put the library's material folders on the USD search path. An HDRI is named on a `DomeLight` in the same way.
- **In Unreal-based apps** such as IMRSV: the app installs a release and builds its materials at runtime from a small set of master materials. Target: Unreal 5.8+ with Substrate.

How each part works is specified in **[`docs/specs/`](docs/specs/_Architecture.md)**. Start with the architecture.

## Checking it

- **The gate:** `uv run tools/validators/run_all.py` checks every material and release in one command. [`CONTRIBUTING.md`](CONTRIBUTING.md) §Checks lists what it checks and how to set it up.
- **The parity rig:** `uv run tools/parity/rig.py <article> [--sweep]` renders a material side by side in USDLiveView's renderer (Storm), Blender and Unreal (when the machine has the Unreal runtime), moves each slider through its range, and scores where the renderers agree and where they drift.

## Contributing

New materials and textures are welcome. Read **[`CONTRIBUTING.md`](CONTRIBUTING.md)**: contributions are dedicated under CC0, and every texture must come from a source that can be (your own work, procedural, or CC0 libraries such as ambientCG).

## Licence and credit

- **Content** (materials, textures, recipes, release data): **[CC0-1.0](LICENSE-CONTENT.md)**.
- **Code** (tools, the Blender add-on, docs): **[Apache-2.0](LICENSE)**.

Credit isn't required, but it is appreciated:

> Materials from the **Matter Library** (https://github.com/Imrsv-tools/Matter-Library), CC0.

Contributors and sources are listed in [`CREDITS.md`](CREDITS.md).

## Where things are

| Looking for… | Go to |
|---|---|
| what the library is and how it's specified | [`docs/specs/`](docs/specs/_Docs_Index.md) |
| the vocabulary | [`docs/Glossary.md`](docs/Glossary.md) |
| what's being worked on, and what's next | [`docs/Planning/Roadmap.md`](docs/Planning/Roadmap.md) |
| working on this repo with an AI agent | [`AGENTS.md`](AGENTS.md) |
