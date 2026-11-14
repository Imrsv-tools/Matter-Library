# Research — Historical rooms: what IMRSV's asset tooling asks of the library

**Opened:** 2026-11-14 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `HR` (ids `HR-Qn`, `HR-Fn`). **Pass 1** is written from the asset tooling's side. The library's review is **Pass 2**, as in `261011_R_AssetToolingAsks.md`.
**Requested by:** IMRSV's work on the tools that make a model ready for Studio. The lead, 2026-11-14, verbatim: *"yes we can (and should) make material requests"*.

**Question:** what does the library need to hold so that a real historical interior, built at true size from its measured record, reads as real?

**Extends, does not replace:** `261101_R_AssetToolingBrickAsks.md` (its brick and its mortar stand, and are needed here too) · `261104_R_AssetToolingHouseAsks.md` (its A2, the mortar, again) · `docs/specs/Ontology/Taxonomy.md` (*a wall is not matter*: plaster on a wall is) · `260925_R_LibraryCoverage_FirstRelease.md`.

**Public-repo note.** The asset tooling is a sibling IMRSV project and is private for now. It is summarised here by what it is building and what it needs: no paths, code or ruling ids of its own.

**Measured at:** `0deb76d` (2026-11-14).

## The short version

- **The asset tooling is starting on historical rooms.** The first two are a 19th-century Shaker dwelling room and the Valley Temple of Khafre at Giza (about 2550 BC). Both were chosen because their finish is the material itself, kept clean, with no painted pattern: what the library's articles already do well.
- **One finish is missing from almost every room before 1950: a lime plaster.** The library has paint and no plaster (HR-F1).
- **Asks:** a lime plaster (A1) · the mortar, a third time (A2) · a red Aswan granite (A3) · an Egyptian calcite (A4) · a painted softwood, or word on how to get one (A5) · a woven cotton tape (A6) · a candle flame (A7) · tinplate (A8). Two questions on tinting stone and wood (HR-Q1, HR-Q2).

## Pass 1 — From the asset tooling's side

### What was found

- **HR-F1 — No plaster.** Searched at `0deb76d`: the materials tree, the coverage list and the specs name no plaster, limewash or render. A plastered wall can only be bound to `Paint_Satin_Clean_Base_s01_v01`, whose base colour is one constant. On a large flat wall that reads as a modern painted board: a real plastered wall shows slight trowel relief, soft unevenness in colour and a matte, chalky face.
- **HR-F2 — The granite and what a tint can do to it.** `Granite_Polished_Clean_Base_s1_v01`'s base map averages a warm buff (about 0.66, 0.59, 0.52 as stored). Aswan granite is red to rose with large black and white crystals. A tint multiplies the whole map, so it darkens the pale crystals with the ground: the result is a brown granite, not a red one with its own grain.
- **HR-F3 — No match for Egyptian calcite.** The floors of the temple are white calcite ("Egyptian alabaster"): creamy white, faintly banded, slightly translucent. `Onyx_Polished_Clean_Base_s01_v01` carries a fixed amber `subsurface_color` (0.573, 0.319, 0.147), so it glows honey whatever the tint. `Marble_Honed_Clean_Base_s1_v01` is the stand-in; its veining is marble's, not calcite's banding.
- **HR-F4 — Shaker woodwork is painted or stained softwood in strong, documented colours** (chrome yellow, red ochre, yellow-ochre floors, a blue-green), on pine, with the grain and board joints showing through a thin coat. `Paint_Satin` hides the wood entirely; `Oak_Natural` tinted is the wrong species and cannot reach a chrome yellow, since a tint only darkens.

### Asks

- **A1 — A lime plaster**, at wall scale (`s1`): matte, off-white, with fine trowel relief and soft tonal unevenness; colour by tint (whitewash white, cream, an earth tone). A smoother and a rougher condition if conditions are the library's way. One article serves most interiors from antiquity to about 1950, and it is the single most useful addition for this work.
- **A2 — The cement or lime mortar** (`261101_R_AssetToolingBrickAsks.md` A3, `261104_R_AssetToolingHouseAsks.md` A2): stone, brick and tile joints. A lime version, paler and softer, serves the older rooms.
- **A3 — A red Aswan granite**, polished (`s1`): rose to red ground, coarse black and white crystals. A honed or dressed condition would serve the unpolished faces.
- **A4 — An Egyptian calcite (alabaster)**, polished (`s1` or `s01`): creamy white, faint banding, a pale subsurface colour.
- **A5 — A painted softwood**, or the library's word on the right way to get one (HR-Q2): pine under a thin oil paint or stain, grain and joints still reading, colour by tint from a pale base.
- **A6 — A woven cotton tape** (`s001`): the checkerboard-woven seat of a Shaker chair, in one or two colours by tint. Also serves webbing and strapping.
- **A7 — A candle flame**: a warm emissive for a small flame (a candle, an oil lamp, a stove's open door). `LED_WarmWhite` is the stand-in; a flame is warmer and its brightness should sit well below a lamp's.
- **A8 — Tinplate**: tinned sheet iron, dull silver with a soft sheen, for sconces, lanterns and stove pipe. `Aluminium_Raw` is the stand-in.

### Questions

- **HR-Q1 — Recolouring a patterned stone.** Is there, or will there be, a way to shift the hue of an article's ground without multiplying its whole map (HR-F2)? If the answer is "a new article each time", A3 stands as asked.
- **HR-Q2 — Paint over a substrate.** Is "a thin paint over wood" one article (A5), or an overlay the masters could carry on any wood article, as dust and scratches are carried now?

## Pass 2 — The library's review

*(Not yet written.)*
