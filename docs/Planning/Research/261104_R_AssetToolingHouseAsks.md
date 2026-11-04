# Research — A 1970s house, inside: what IMRSV's asset tooling asks of the library

**Opened:** 2026-11-04 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `RH` (ids `RH-Qn`, `RH-Fn`). **Pass 1** is written from the asset tooling's side; the library's review of it against its own tree is **Pass 2**, as in `261011_R_AssetToolingAsks.md`.
**Requested by:** IMRSV's work on the tools that make a model ready for Studio. The lead, 2026-11-04, verbatim: *"make any matter requests you need"*.

**Question:** what does a generated interior Set of a 1970s ranch house need from the library, now and for its kitchen and baths?

**Extends, does not replace:** `261101_R_AssetToolingBrickAsks.md` (its A3, a mortar, is asked again below with a second case) · `docs/specs/Ontology/Taxonomy.md` (*a brick wall is not matter*: the same holds for a stone wall and a tiled wall) · `260925_R_LibraryCoverage_FirstRelease.md`.

**Public-repo note.** The asset tooling is a sibling IMRSV project and is private for now. It is summarised here by what it built and what it needs: no paths, code or ruling ids of its own.

**Measured at:** `ebdf017` (2026-11-04) · Blender 5.2.2 (blender.org) · OpenUSD 26.03.

## The short version

- **The asset tooling built the inside of a one-storey 1970s house** (23.9 × 9.7 m, 130 sub-objects): oak strip floors throughout, painted walls and ceilings, oak trim and doors, brass knobs, and a family room with a **fieldstone wall** of ~250 modelled stones, a flagstone hearth and a firebrick firebox. Twelve articles; every one resolves in Studio's catalog.
- **Asks:** three articles into the library's Blender file (A1); a mortar, again (A2); a plastic laminate for counters (A3); a decision on tiled walls (RH-Q1); a buff stone the tints can reach (RH-Q2); a silvered mirror (A4, added with the kitchen and baths).

## Pass 1 — From the asset tooling's side

### What was built

- **RH-F1 — The articles the Set binds**, each by tint where a colour was wanted: `Paint_Satin_Clean_Base_s01_v01` (walls, ceilings, sashes, the outside doors), `Oak_Natural_Clean_Base_s1_v01` (floors; trim and doors stained by tint), `BlackWalnut_Natural_Clean_Base_s01_v01` (hewn beams, a mantel, a rail), `Granite_Weathered_Clean_Base_s1_v01` and `Sandstone_Weathered_Clean_Base_s1_v01` (the stones, two tints each), `Slate_Cleft_Clean_Base_s1_v01` (flagstones), `Concrete_Smooth_Worn_Dusty_s1_v01` (mortar), `Fireclay_Natural_Clean_Base_s01_v01` (firebrick), `Glass_Clear_Clean_Base_s01_v01`, `Brass_Polished_Clean_Base_s01_v01`, `Aluminium_Brushed_Clean_Base_s001_v01`, `PowderCoat_Textured_Clean_Base_s001_v01` (a steel lintel, soot).
- **RH-F2 — The library's Blender asset file lacks three of them**: `Granite_Weathered_Clean_Base_s1_v01`, `Sandstone_Weathered_Clean_Base_s1_v01`, `Brass_Polished_Clean_Base_s01_v01` (and, not used here, `Copper_Polished_Clean_Base_s01_v01`). Each has its `.mtlx` and maps; Studio's catalog lists all three. The design stills drew them from their own maps through a plain principled shader instead of the library's.
- **RH-F3 — A joint of `Concrete_Smooth_Worn_Dusty` reads near-white** in a fieldstone wall even tinted to 0.42: its dust layer lightens a recessed joint that should sit in shadow.
- **RH-F4 — Sandstone's base colour is warm and saturated** (linear mean 0.43, 0.31, 0.19). A tint multiplies, so it can darken and shift it but not grey it: buff took a tint of (0.72, 0.84, 1.02), brown (0.45, 0.47, 0.55).

- **RH-F5 — The kitchen, the baths and the laundry (the Set's third pass, same day)** bind five more articles, all in Studio's catalog: `Porcelain_Glazed_Clean_Base_s01_v01` (toilets, basins, tubs; the wall tile, tinted bone and aqua), `Paint_Gloss_Clean_Base_s01_v01` (baked-enamel appliances in harvest gold and white, an oven's black glass), `StainlessSteel_Brushed_Clean_Base_s001_v01` (a sink), `StainlessSteel_Polished_Clean_Base_s01_v01` (chrome fittings, and a mirror, below), `PowderCoat_Textured_Clean_Base_s001_v01` (the counters and vanity tops, standing in for A3's laminate, tinted to a wheat). The tile was modelled tile by tile over a grout of `Concrete_Smooth_Worn_Dusty` tinted near white: RH-Q1's assembly reading, applied until the library says otherwise. The library's Blender file has all five; the stills drew them through its own shader.
- **RH-F6 — Polished stainless steel does not stand in for a mirror.** Its roughness blurs the reflection to a frosted plate. A bathroom mirror over a vanity needs a silvered glass.

### Asks

- **A1 — Add the three articles to `blender/asset_library/MatterLibrary.blend`** (RH-F2), so a picture made from Blender shows the library's shader for them.
- **A2 — A cement mortar** (with `261101_R_AssetToolingBrickAsks.md` A3): grey-brown, sandy, no dust layer, at mortar scale (`s01`); one article serves brick, stone and tile joints.
- **A3 — A plastic laminate** for counters and a vanity top (high-pressure laminate, the 1970s *Formica*): a solid colour taken by tint, a faint texture, satin to gloss; `s01`. The kitchen and baths are now built with a powder coat standing in (RH-F5).
- **A4 — A silvered mirror** (RH-F6): glass over a silver backing, near-zero roughness, `s01`. One article serves a bathroom mirror, a medicine cabinet's door and a dressing mirror.

### Questions

- **RH-Q1 — A tiled bath wall: matter or assembly?** By `Taxonomy.md` a tiled wall is an assembly, so the tooling would model each tile in `Porcelain_Glazed_Clean_Base_s01_v01` over the A2 grout. Is that the library's reading, or is a glazed wall tile (with its slight pillowing and glaze pooling) an article of its own?
- **RH-Q2 — A buff or grey-brown fieldstone** (a weathered limestone or a quartzite) that sits where RH-F4's tints had to push sandstone. Is one on the coverage list?
