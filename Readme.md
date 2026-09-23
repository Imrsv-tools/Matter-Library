# Matter Library

**A community library of physically based materials, authored once in MaterialX and published as versioned releases that Blender, Unreal-based apps and USD tools can all use.**

> *"Author once, render close to the same everywhere."*

The Matter Library catalogues materials by **what things are made of** (stone, metal, glass, plastic, textile, …), not by the objects they appear on. Every material is:

- **One MaterialX file**, using OpenPBR (`open_pbr_surface`, MaterialX 1.39): the single source of truth. Blender and Unreal forms are derived from it, never hand-authored.
- **Physically scaled**, with a scale tag recording real-world meters per texture tile.
- **Built on a small, fixed set of masters**: Opaque, Masked, TranslucentThin, TranslucentThick, Subsurface, TwoLayer, Emissive. So it behaves predictably in every renderer.
- **Limited to parameters every target can honour** (the LCD discipline), so it looks close to the same in each one.
- **Free to use.** Materials and textures are **CC0**: no rights reserved, commercial use included.

## How it's organised

| Tier | What it is | Where |
|---|---|---|
| **Source collection** | every material and texture, open to community contribution, organised by Domain / Class | `MatterLibrary/` |
| **Versioned library** | curated releases: a manifest pins exact material and texture versions, and each release is frozen and reproducible | `library/releases/` |

Materials are named `Material_Variant_Condition_Detail_sNN_vNN` (for example `Copper_Verdigris_Aged_Base_s01_v01`). A material's own version (`vNN`) and the library's release version (`matterlib-X.Y.Z`) are separate.

## Using it

- **In Blender (5.1+):** the Asset-Browser library (`blender/asset_library/`) lets you assign Matter materials, and the Matter add-on (`blender/addons/imrsv_lcd_export/`) exports USD in one of two forms: a lightweight one that references the library, or a self-contained portable one.
- **In a USD tool:** reference an article by name (`@Name.mtlx@`) and put the library's material folders on the USD search path.
- **In Unreal-based apps** such as IMRSV: the app installs a release and builds its materials at runtime from a small set of master materials. Target: Unreal 5.8+ with Substrate.

How each part works is specified in **[`docs/specs/`](docs/specs/_Architecture.md)**. Start with the architecture.

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
