# Research — The platform's character phase: skin and eyes from the library (2026-10-19)

**Mnemonic:** `PCE` — reports `R-PCE-n` (for the ledger), asks `Q-PCE-n` (for the library).
**Altitude:** the Character group's `skin` and `eyes` parts as one consumer now uses them; two asks.
**Asked by:** the platform's lead, through its character phase (*Characters and Wardrobe*).

Nothing here asks the library to change a contract.

## Reports — for the ledger

**R-PCE-1 — skin and eyes are picked from the library's own shelf.** The platform's app no longer lists skin tones or
eye colours as buttons of its own. A Creator presses **Change** on the character's Skin or Eyes and the material window
opens on the Character group at that part (`character` › `skin`, `character` › `eyes`); a card clicked is tried on the
character at once, and Save keeps it as one Undo step.

**R-PCE-2 — what the app reads from an article's name.** Two naming rules now carry weight for this consumer:
- **A skin pick pairs the lips and nails by name.** A pick named `Skin_Fitzpatrick<Tone>_…` puts the same tone's
  `Lips_Fitzpatrick<Tone>_…` on the lips and `Nail_Fitzpatrick<Tone>_…` on the nails, in the same step. A tone with no
  lips or nails article leaves that part as it is; a skin article that is not a Fitzpatrick tone pairs nothing.
- **The eyes' window shows whole-eye looks only** — articles named `Eye_…`. A whole-eye look is put on the sclera, iris
  and pupil of both eyes.

Renaming either family would quietly change what the app offers, so the rules are written down here.

## Asks — for the library

**Q-PCE-1 — do the single-part eye articles stay for a Creator to pick?** The eyes part also serves `Cornea_…`,
`Iris_…`, `Pupil_…` and `Sclera_…` articles, each `creator_selectable`. The platform's app offers a whole-eye look only,
so it does not show them. **The need:** to know whether they are building blocks of the whole-eye looks (then not
`creator_selectable`) or looks a Creator is meant to mix (then the app needs a way to offer them, which is not designed).

**Q-PCE-2 — `fits` is read by no consumer today.** Whole-eye articles carry `fits` (e.g. `MakeHuman_Eyes_v01`). The
platform reads no `fits` field; it puts a whole-eye look on any character's six eye meshes by their names. **The need:**
to know whether `fits` is meant to narrow which characters an article is offered for — if so, which mesh family names a
consumer should expect, and whether an article without `fits` fits every family.
