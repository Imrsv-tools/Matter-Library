# Preview generators — usdview parity fixture (Phase 53)

Renders ONE Matter material `.mtlx` on a standard sphere under a dome light, standalone —
no live Stage→Plugin chain (which doesn't exist until Phases 54/55/57). The render is the
**mandatory-manual** parity artifact (informal visual parity, *not* the formal ΔE bar — that
is Phase 60). These wrappers also **seed Phase 60's `usdrecord` ΔE baselines**.

## Files
- `preview_wrapper.usda` — the documented wrapper shape (template, `<REL_MTLX>`/`<NAME>` slots).
- `make_preview.py` — given a `.mtlx`, writes `<name>_preview.usda` and (if `usdview` is on
  PATH) offers to view it.

## Path resolution (unambiguous — peer-review B3)
- The `.mtlx` is referenced by **relative filesystem path**, resolved by USD's
  **`ArDefaultResolver`** — *not* the `@MatterLib/...@` package search-path (that portable
  resolver is a Phase-54 Distribution concern).
- Texture `<image>` paths are **relative inside the `.mtlx`**, resolved by MaterialX relative
  to the `.mtlx` document — no env var owns texture lookup.
- **`PXR_MTLX_STDLIB_SEARCH_PATHS`** owns **only** the MaterialX stdlib nodedefs
  (`open_pbr_surface` etc.), the S7 deployment gotcha — not asset/texture resolution.

## Degraded path (this box, Phase 53)
`usdview` / the `pxr` Python module is **not installed here**, so the parity gate **degrades**
to SDK-validate + a structural review of the `.mtlx`. The artifact is then an explicit
**`parity-not-evaluated`** note (an honest non-claim that keeps the manifest `draft` status and
the deferred formal parity honest), plus the structural-review log — never a silent pass.
Render these wrappers on a USD-equipped box, or defer to Phase 60.
