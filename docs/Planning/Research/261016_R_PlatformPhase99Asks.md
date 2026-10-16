# Research — The platform's materials phase: reports and asks (2026-10-16)

**Mnemonic:** `PMU` — reports `R-PMU-n` (for the ledger), asks `Q-PMU-n` (for the library).
**Altitude:** ledger rows P11, P17, P21, P29, M6 (MA-Q7) and the consumer half of F-P19-9; three new asks.
**Asked by:** the platform's lead, through its materials phase (*Materials Understood*).

Each report names the row's own stated check and what was run. Nothing here asks the library to change a contract.

## Reports — for the ledger

**R-PMU-1 — P11 (write and read Creator overrides with the connected carrier).** The row's check, on a composition the
platform's app saved: the library's own `tools/conformance/check_lcd_carrier.py`, run on a test composition whose
overrides the lead set by hand in the app:

> `[PASS] … 77 Creator override(s), every one a connected, declared, correctly typed Material input`

The platform's import and reimport now carry all twelve Creator ports that travel (the fifteen less the three UV
placement ports), tested both ways. *Ask:* P11 to `DONE` on its own check.

**R-PMU-2 — P17 (supply each card mesh's cut-out map when binding).** The library names no tool for this row, so the
platform ran its own probe on an app-saved character composition: Hair, Eyebrows and Eyelashes each carry
`inputs:cutout_map`, set to the card's own picture inside the composition, and the NodeGraph's `cutout_map` input
resolves to it — *cards seen 3, failing 0*. *Ask:* P17 to `DONE` on its own check.

**R-PMU-3 — P29 (the scale view).** The platform builds **no** scene-wide scale-view switch. The lead: *"a
troubleshooting feature … I would hate for it to confuse or clutter the composition creation process."* The seven
scale grids are offered as ordinary materials instead — listed with the rest (`candidate` is shown; the platform's list
has no status filter) and assigned to any mesh like any other, so a mesh at the wrong UV scale shows. The swap-the-scene
view stays the Blender add-on's. *Ask:* P29's Studio half closed as *not built, by the lead's ruling*; its USDLiveView
half is not the platform's to answer here.

**R-PMU-4 — F-P19-9, the consumer's half.** The library's own runtime keeps full-precision UVs (`2d32a4c`). The
platform's skinned meshes now do too; they were half floats, and a character's material tiles ~150 times per UV unit,
so a half float's step near 1.0 (2⁻¹¹) is ~0.075 of a tile — the wander on the cheek. The platform's static meshes
already used full precision. The look is checked at the platform's exit sitting (a grid on a box and on the cheek);
the result is appended below.

**R-PMU-5 — P21 (take the character's pictures from the library).** Built:
- An *Eye colour* choice beside the skin tones lists the catalog's `Eye_<Colour>_…` articles by their colour word; a
  pick binds the article on Sclera, Iris and Pupil, both sides.
- A fitted article draws its own picture where the binding supplies none (P28) — `Eye_Green`, `Teeth_Natural`.
- A mesh's own picture (the hair's strands, the iris) is kept on every re-bind, so hair keeps its strands at any tint.
- A hairstyle put on arrives at the colour the character's brows carry: the article's light brown, or the Creator's.

The row's check — *eye colour chosen by picture; hair keeps its strands at any tint* — is seen at the exit sitting and
appended below.

## Asks — for the library

**Q-PMU-1 — which fit-set picture goes with an article and a mesh family, and where the catalog says so.** *(The
platform's Q-CSK-2; beside the library's own Q-SKM-4, naming a mesh version.)* The platform reads a picture the
article states. **Proposed answer:** a tone's article states its picture as its own `base_color_map` default, as
`Eye_Green` does — the platform already draws that.

**Q-PMU-2 — what the lips wear.** *(The platform's Q-CSK-4; an input for the library's Skin Maps discovery — the
articles are the library's.)* The draft's *Proposed* puts the skin article plus the map on the lips. A second form,
not yet weighed: the lips keep a lip article — wetter, finer pores — that also takes the map, as MPFB's lips share the
body's picture with their own finish. Either removes the line at the lip; the second keeps the shine.

**Q-PMU-3 — a coloured LED reads its colour.** *(The lead's ruling: the fix is the library's articles; the platform
does not change how it draws bright colour. Follows TI-F1 in `261013_R_PlatformTrackedItemsAsks.md`, which then named
nothing for the library.)* Measured in the platform's app with the LED articles as served:
- a red emission colour reads **orange at a luminance of 12** and **yellow at 25** — the renderer's tone curve, as
  expected of a bright light;
- on the article's **white body** it washes to **pale pink**;
- on a **black body** it reads **red at a luminance of about 1**.

*Ask:* the coloured LED articles get a darker body and a starting brightness at which the picked colour reads — red as
red, not orange or pale pink.

## Owed — appended after the platform's exit sitting

- **MA-Q7.** The library has recorded its answer (M6: `index` the default, `=function` the old build). The platform's
  exit sitting shows the gem under its `index` build and again under a `REFRACTION=function` rebuild on the same cube;
  what it shows is appended here.
- **R-PMU-4 and R-PMU-5's looks.** Appended.
- **Any master change** a look-tuning loop at the sitting shows is needed. The platform makes no master of its own; a
  change is an ask here.

## Status

- **Reports:** R-PMU-1 – 5 (P11, P17, P29, F-P19-9, P21).
- **Asks:** Q-PMU-1 – 3 (a fit-set picture's carrier, the lips, the LED body and brightness).
- **Owed to the library:** the exit sitting's looks (above).
