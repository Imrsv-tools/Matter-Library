# Research — The hair card's strand colour map (what made the hair read as hair)

**Opened:** 2026-09-28 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `HS` (ids `HS-Qn`, `HS-Fn`).
**Requested by:** the IMRSV platform's **Phase 66 (Appearance)**, at its hair sitting (run E8). Lead: *"make a note somewhere
in the Matter Library repo (research maybe) once you know what the fix is"*.

**Extends, does not replace:** `260928_R_HairAndNailRendering.md` (H1–H5; HR-Q4 "card maps"), `260928_R_PlatformAppearanceAsks.md`
(A1, the Hair master), `Contract/LCDSchema.md` §Cut-out map, `Ontology/MasterSet.md` Hair row.

**Public-repo note.** The platform's planning is private; it is summarised here by what it found and what it needs. The
platform commits named are for traceability only.

---

## Pass 1 — What the lead saw, in order

The platform shaded card hair (the built-in MakeHuman `short02` and the wardrobe styles) on `Hair_Natural`, whose Unreal
realisation was the engine's **hair shading model** (per the Hair row: soft coverage, light through the card).

| Try | What the lead saw |
|---|---|
| Hair shading model, constant fibre tangent | blocky facets that mirror the sky, flicker when moving |
| + a per-polygon tangent bug fixed on the platform | the blocks' edges gone — but a **smooth glossy shell**: every lit patch one flat colour, washing to white in strong light |
| Specular 0 on the hair model | still a sheet — lead: *"turn off anything specular, gloss, reflection, glow, highlight"* |
| **Matte default-lit + MakeHuman's own hair texture** | lead: ***"OK! That is HAIR!"*** — and on a wardrobe card style with the tint: *"Tint works, Bob works .. Looks fine.. these cards are terrible but they read correct"* |

- **HS-F1 — What makes MakeHuman hair read as hair is its colour picture, not the shading model.** MakeHuman paints the
  strands — and the dark gaps between them — into the card's colour texture. The library's Hair article is one flat colour,
  and the cut-out map (the mesh's texture ALPHA) carries none of it, so every consumer drew a smooth tinted shell.
- **HS-F2 — A hair shading model on MakeHuman cards makes it worse, not better.** Unreal's hair BSDF needs a real per-strand
  tangent field (Epic's cards bake one into textures MakeHuman does not have); on a flat card it lights each card as one
  block. Its sheen is what the lead read as "a sheet". (Environment reflection is not the cause: under Substrate the engine
  gives hair no environment specular.) The platform's Unreal Hair master is now **matte default-lit** (Specular 0,
  Roughness 1, Metallic 0), soft-covered by the cut-out through a frame-stable dither.
- **HS-F3 — The colour cannot ride inside the cut-out.** The first proof put MakeHuman's RGBA picture in the cut-out file.
  It rendered right in Unreal, but §Cut-out map is one channel (*"MaterialX reads a float image's first channel"*): a USD
  viewer would take the hair's RED as coverage and draw it see-through. The platform's article validator refuses an RGBA
  cut-out by design, and a Masked-bound hair would break the same way.

## Pass 2 — What the platform built (IMRSV_Stage `78958782`, 2026-09-28)

A **second mesh-supplied map**, beside the cut-out, by the same carrier:

- **The file:** `cutouts/<mesh>_color.png` — the RGB of the same MakeHuman picture the cut-out's alpha comes from, drawn on
  the mesh's own `st` (8-bit RGB PNG, deterministic bytes, hash-pinned by the platform's generator).
- **The input:** `asset inputs:strand_color_map = @./cutouts/<mesh>_color.png@` on the card mesh's own bound Material, next to
  `inputs:cutout_map` (the article's value would be empty — the picture belongs to the mesh, D1).
- **The carry (platform import):** the resolved path on the instance's Material input; connected to
  `NG_<id>.inputs:strand_color_map` **when the article declares that port** — authored even while no article does, because
  Unreal consumes it today.
- **The consumer (Unreal):** it rides the platform's existing base-colour texture channel, so it **replaces the article's
  base colour, and the Creator's hair tint multiplies after**. An article with its own base-colour texture keeps it.
- **Today, therefore:** Unreal draws textured matte hair; a USD viewer (Storm) and Blender still draw the flat article colour
  — not broken, just untextured — until the library declares the port.

## Pass 3 — The asks

- **HS-Q1 — Declare `strand_color_map` on the Hair article (and on Masked, if a Masked hair should keep working).** A
  nodegraph interface input of type `filename`, author-tier lane-B, not a Creator port, value empty in the article — the
  exact shape of `cutout_map`. Proposed wording for §Cut-out map's sibling: *"A card mesh may also supply its strand
  colour: the RGB of the same picture, sampled on `st` directly (not through `place2d`). When supplied it replaces the
  article's base colour; the tint multiplies after."*
- **HS-Q2 — The graph:** `base = strand_color_map ? image(strand_color_map, texcoord 0) : base_color`, then `× base_color_tint`
  as today. With no map supplied the image default must leave the article colour (e.g. an `image` whose empty-file default
  is white multiplied into `base_color`, or a switch) — never magenta, like the cut-out's `default = 1`.
- **HS-Q3 — The Hair row's Unreal realisation.** The row reads "hair (… Unreal's Scatter / Backlit)". The platform found the
  hair model wrong for MakeHuman cards (HS-F2) and now renders matte. The row's shading intent may want restating as
  **matte, coloured by the mesh's picture**, with the hair model reserved for strands (H5) — the library's call.
- **HS-Q4 — Blender loader / rig:** read `inputs:strand_color_map` like `inputs:cutout_map`, so Blender draws the textured hair.
- **HS-Q5 — Validator:** `validate_material.py` / the rig's checks — accept the new author-tier input; an image `file` value
  in the article stays empty, like `cutout_tex`.

## Open

- **HS-Q6** — Does the strand colour belong in the card-maps family of HR-Q4 (root-to-tip, strand-ID, depth)? The platform
  treats it as the first of those maps; the naming is provisional (`strand_color_map`) until the library rules.

## Answered — by Phase09 (closed 2026-09-30)

The library answered every ask its own way (research `260929_R_CharacterMaps.md` MAP-RD3 as amended; `LCDSchema.md`
§Base colour map); Studio's side is `PlatformDependencies.md` P21.
- **HS-Q1 / HS-Q6:** the input is **`base_color_map`** (OpenPBR-aligned, LCDSchema §Notes), on Opaque, Masked, Hair and
  Subsurface; not a hair-only card map, since the eye takes it too.
- **HS-Q2:** it **multiplies** (`base_color_const × base_color_map × base_color_tint`), never replaces, so the tint
  reaches every colour on every style; unsupplied reads white.
- **HS-Q3:** card hair is **matte, default lit** in Unreal and matte everywhere (`specular_weight = 0`); the hair
  shading model is kept for strands.
- **HS-Q4 / HS-Q5:** the Blender loader, the rig and the validator read it as they read `cutout_map`. The library also
  prepares each hairstyle's picture and cut-out (the fit set).
