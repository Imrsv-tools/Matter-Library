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

*Row 1 added at Phase24's close (2026-11-01).*
