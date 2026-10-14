# Phase18 — Thumbnails

**Status:** SEEDED (2026-10-14). **Numbered Phase18 by the lead the same day**, after The Library Service and ahead of Scale Grids: *"Actually lets pull the library service and thumbnails before Scale grids as well so we can get the entire chain establsihed recategorized, documented and working correctly before we add more materials"* (RD-DS-7). A pointer-shell written by `/research` on the lead's word (*"Seed all the TBD phases we discovered here"*). `/discovery` fills it. **Starting discovery is a deliberate gate, the lead's call, never a slide.**

## Outcome

**Every kept material has thumbnails that show it at its best,** on a subject that suits it (skin on a hand and a face, hair on a head, glass in front of a backdrop), ready for the website and the team's console.

## Why this is a phase

The rig's pictures are diagnostics, lit the same in every tool to compare them, and wrong for showing a material (F-MP-6). A thumbnail is a separate showcase render, with its own scene, lighting and subjects. Nothing like it exists yet. It is the library's half of *See the Library* (RD-WS-4).

## Scope — as ruled at research (2026-10-14)

The authority until this phase writes its specs: [`261014_R_MaterialPipeline.md`](../Research/261014_R_MaterialPipeline.md) Pass 2 and §Resolved.

- **The renderer** (RD-MP-2): Cycles today, labelled on every picture. An Unreal hero follows a showcase build of the runtime and the solid see-through master's repair (M6).
- **The subject per Class** (RD-MP-3): F-MP-9's table, starting set. Skin on the clothed character's hand and part of the face; hair on a head; ground matter on a slab at real size; glass and gems with a backdrop.
- **Non-intimate character views only** (F-MP-17): face, hand, mouth, eye; the character clothed.
- **Made before the review** (RD-MP-4), so the maintainer approves what the public sees.
- **The word** (RD-MP-5): "thumbnail". "Preview" stays the review render.
- **Never in git or LFS** (RD-MP-6): a folder that git ignores before a release; release assets at a release.
- **A few pictures each** (F-MP-11): a card, a close-up, a context view, a dark view for lights; optionally looks at a Creator setting.
- **Each records what made it** (F-MP-10): the article's hash, the masters version, the renderer, the scene version. A change to any of them makes it stale.

- **Carried in from Phase13 (RD-P13-2, the lead, 2026-10-14):** biological materials are not Matter, and need a human-context picture per kind: *"the skins need the sideface/hands image, eyes need an Eye image, Teeth need a teeth image, etc so that is a different experinence and we need to set taht up"*. Until this phase makes those, the site file publishes **no picture** for a `section: character` material (never the rig's cubes).

## Open questions (settle during this phase)

- GPU time per article at the chosen sample counts (F-MP-32), measured on the service.
- The showcase scene's lighting: which HDRI (from *HDRIs in the Library*?), which tone curve.
- Image formats and sizes for the site.

## Depends on

*The Library Service* (where the renders run; RD-MP-10: the thumbnail probe is one of its first tests).

## Discovery Log

*(empty — `/discovery` fills it)*
