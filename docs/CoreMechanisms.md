# Matter Library — Core Mechanisms

**Status:** Active. Empty until a phase solves a problem a later phase will meet — **correct while empty.**

**⛔ Read this WHOLE before designing anything that is shown, moved, edited or written** — every verb,
every run, up front. **Every row is a problem this project has already solved.**

- **A phase that meets a row RIDES it:** the phase doc's `## Rides on` table names the row, and the
  executor opens the reference code and follows it. **Building a second way is a knowing divergence
  that needs the lead's ruling** — never a plan pick.
- **Each row points at the doc that owns the rule and restates nothing beyond one line.** Detail lives
  with its owner (`Methodology/AgenticEngineering_DocumentationMap.md` §No-Duplication Rule).
- **A line number is a starting point — grep the symbol.** Code moves; the symbol is the address.
- **Rows are added when a phase solves a problem a later phase will meet — the close adds the row**
  (`execute_close.md` row A).

| # | The problem | Owning rule | Copy this |
|---|---|---|---|
| 1 | **Making a body map larger than 2048 inside the machine's memory** (an 8K map's per-texel fields and temporaries need ~45 GB made whole) | `docs/specs/Authoring/SkinMaps.md` §One subject's set at 8K (RD-P24-7) | `gen_synth_skin.compose_banded` / `band_pre` / `band_view` / `parts_banded` (bands of rows; what needs the whole atlas taken once); `gen_skin_shine.relief`'s `CHUNK`; `gen_skin_maps.bleed`'s ring-only path above 2048 |

| 2 | **Laying a mark or a bit of makeup on the body's atlas** (a shape made in 3D, or a stamp placed by a point, a size and a turn), merged with others into one picture a master reads | `docs/specs/Authoring/MakeupPieces.md` §The merge (RD-P26-5, RD-P26-6) | `merge_makeup.merge` / `stamp_coverage` / `tangent_frame` (placement); `gen_makeup_pieces.eyeshadow` (a fitted shape from landmarks); `_fill` (values pushed past an edge) |

| 3 | **Making a skin from an image model's picture** (the picture carried onto hm08 through a camera, then turned into the maker's melanin and blood so tone and marks stay changeable), served with its source | `docs/specs/Authoring/SkinMaps.md` §How to make one, *An AI-assisted map* (Phase25) | `project_face.cmd_field` (the front projection and coordinate field) · `gen_synth_skin.Lut.inverse` + `project_face.cmd_pigments` (colour → pigment) · `gen_skin_maps.subject(pigments_dir=…)` (served, the ear by `gen_synth_skin.ear_paint`) |

*Row 1 added at Phase24's close (2026-11-01); row 2 at Phase26's (2026-11-02); row 3 at Phase25's (2026-11-02).*
