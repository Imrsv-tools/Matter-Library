# Research — A room lined with glowing red panels: what IMRSV's asset tooling asks of the library

**Opened:** 2026-11-14 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `EG` (ids `EG-Qn`, `EG-Fn`). **Pass 1** is written from the asset tooling's side; the library's review of it against its own tree is **Pass 2**, as in `261011_R_AssetToolingAsks.md`.
**Requested by:** IMRSV's work on the tools that make a model ready for Studio. The lead, 2026-11-14, on whether to ask the library for a glowing material with grain: *"yes"*.

**Question:** what does a Set whose surfaces are large, dimly glowing panels need from the library, so those panels read as a real lit material and not as one flat colour?

**Extends, does not replace:** `261101_R_AssetToolingBrickAsks.md` (the same finding on a flat-colour article, there in terracotta) · `docs/specs/Ontology/MasterSet.md` (Emissive) · `docs/specs/Contract/LCDSchema.md` (`emission_color`, `emission_luminance`, `base_color_map`).

**Public-repo note.** The asset tooling is a sibling IMRSV project and is private for now. It is summarised here by what it built and what it needs: no paths, code or ruling ids of its own.

**Measured at:** `303b40f` (2026-11-14) · Blender 5.3.0 (blender.org) · OpenUSD 26.8.

## The short version

- **The asset tooling built a science-fiction memory room** (a square tube 3.6 × 7.2 × 3.6 m, 172 sub-objects): every wall, the floor and the ceiling are 1.2 m panels with a grid of fine slots cut through them, some lit from behind. The panel faces are meant to glow a deep red, dimly, as backlit plastic does.
- **The faces are `Neon_Signage_Clean_Base_s01_v01`**, set by its ports to a deep red at a low brightness (`emission_luminance` 0.25 × 0.65 / 1 / 1.4 across three variants). The lead's verdict on the result: *"too matte clean"*. `Neon_Signage` is one constant colour with no maps, and the Emissive master's emission is a constant no layer reaches, so a 1.2 m glowing face is perfectly even.
- **Asks:** a backlit-panel article whose glow carries a map (A1); a ruling on whether the Emissive master may take a map on its emission at all (EG-Q1); whether the wear layers `LED_CoolWhite` already carries read on a dim glow in Unreal (EG-Q2).

## Pass 1 — From the asset tooling's side

### What was built

- **EG-F1 — The articles the Set binds:** `Neon_Signage_Clean_Base_s01_v01` (the red faces, and the slot lights behind them at `emission_luminance` 20 and 6), `LED_CoolWhite_Clean_Base_s01_v01` (one bank's white modules, and a white-lit vestibule), `Acrylic_Clear_Clean_Base_s01_v01` (that bank's clear modules), `ABS_Glossy_Clean_Base_s01_v01`, `ABS_Matte_Clean_Base_s01_v01` (tinted near black for the recesses, red for a label plate), `Aluminium_Brushed_Clean_Base_s001_v01` (tinted dark for the joints). All six are in the library's Blender file; every override is inside `LCDSchema.md`'s ranges and the asset tooling's own rule set accepts the Set.
- **EG-F2 — A dim emissive face shows its own flatness.** At the brightness a backlit panel has in a room (here a quarter of `Neon_Signage`'s 12, under slot lights at 20), nothing hides that every point of a 1.2 m face is the same colour. Three panel variants at different brightnesses help across the room, and do nothing within a panel.
- **EG-F3 — The two emissive families differ in what they carry.** `Neon_Signage` is parameter-only with no layers. `LED_CoolWhite` and `LED_WarmWhite` carry scratches, dust and fingerprints at 0, gated by `Grime01`, but their recipe states that *the master's emission is a constant the layers do not reach, so wear shows only on the diffuser's reflection, not in the glow*.
- **EG-F4 — Tried earlier in the same Set and taken out:** a red acrylic sheet (`Acrylic_Clear` with `transmission_color` red) over white lights. It read as glass, with strong reflections the lead did not want; the film-style look is an opaque glowing face.

### Asks

- **A1 — A backlit plastic panel on Emissive whose glow varies across its face:** the lit face of an acrylic or polycarbonate panel with lamps behind it. The glow should vary a little across the face: a low-contrast, large-scale mottle (about ±10–15 % in luminance) for uneven backlighting, and a fine grain from the diffuser. It needs the same ports as the LEDs (`emission_color`, `emission_luminance`, and the wear layers) and should sit at `s01`. One article would serve light panels, lit walls and ceilings, and backlit signs of any colour.

### Questions

- **EG-Q1 — May the Emissive master take a map on its emission?** For example, an author-tier `emission_map` that multiplies the emission, as `base_color_map` does on the masters that take one (`LCDSchema.md`). Or should the master stay constant, with A1 reached some other way? If the master changes, it is the library's and the platform's call; the asset tooling needs only the article.
- **EG-Q2 — Do `LED_CoolWhite`'s wear layers read on a dim glow in Unreal?** If they do, an LED set red, dim, and with light dust and scratches is a stand-in for A1 until it exists. The asset tooling will try it in Blender; how it looks in Unreal is the library's to say.
