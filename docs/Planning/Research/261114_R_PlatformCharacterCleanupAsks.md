# Research — The platform's character cleanup: which skins and eyes it no longer wants (2026-11-14)

**Mnemonic:** `PCC` — reports `R-PCC-n` (for the ledger), asks `Q-PCC-n` (for the library).
**Mode:** an asks doc, written from the platform's side. It commits the library to nothing.
**Asked by:** the platform's lead, 2026-11-14, closing a cleanup of the platform's character work: *"there are too many skins, versions, as well as characters in the library … clean up the skins we know we will not use"* — and, on the three removals below, *"yes"*.
**Public repo:** needs and uses only. No consumer paths, code or tracker numbers.

**Read against:** this repo's working tree at `39c482b` (`SkinMaps.md`, `Manifest.md`, `Identity.md`, the recipes' `status`, `Phase23`'s RD-P23-4 and RD-P23-8, `261101_R_PlatformSkinAndMakeupAsks.md`).

**Passes:** the reports and asks below are the platform's (Pass 1, 2026-11-14). The library's reading, the open questions and `## Resolved` belong to the doc.

---

## Reports — for the ledger

**R-PCC-1 — The platform has one official character.**
- It is the generated MakeHuman hm08 body on the Manny-named rig, with the lips as part of the body.
- Every other character build the platform had made was removed from its shelves on 2026-11-14.

**R-PCC-2 — `Skin_Tone34` is the platform's go-to skin, for now.**
- The official character is shown on `Skin_Tone34` with `Nail_Tone34`. Its library picture was taken that way.
- The six `Skin_Fitzpatrick I–VI` skins stay in use: nearly every composition the platform has saved names one, and the app's tone row runs on them.

**R-PCC-3 — What the platform's saved work names.** Counted over every composition on the platform's working machine, current, test and archived, on 2026-11-14:

| Family | Compositions that name it |
|---|---|
| `Skin_Fitzpatrick I–VI` | several hundred |
| `Skin_Tone34` | 10 — the newest work |
| `Skin2_*` | **0** |
| `Skin3_*` | **0** |
| `Skin_*_Clean_Synth*` and `Eye_Synth*` | **1**, archived |

**R-PCC-4 — Makeup needs a skin's makeup inputs.**
- The app draws makeup pieces through the skin article's makeup inputs. `Skin` and `Skin_Tone34` carry them; `Skin2` and `Skin3` do not, so a character on either cannot wear makeup.

**R-PCC-5 — A person's marks are now pieces, not whole skins, on the platform's side.**
- Freckles, veins and marks as whole skins (the twelve `Synth` sets) are not offered to a Creator: the platform's skin list is to show finished skins only (Q-PSM-6).
- If the twelve are removed, that filter has nothing left to hide among the skins.

**R-PCC-6 — One picture stored three times.** Within each of `Skin`, `Skin2` and `Skin3`, the colour maps of tones IV, V and VI are byte-identical (one sha256 per family, three files each). Reported, not asked: the tone is in the article's numbers.

---

## Asks — for the library

**Q-PCC-1 — Retire `Skin2` and `Skin3`: the twelve articles, their recipes and their twelve colour maps.**
- Nothing the platform has saved names one (R-PCC-3), and neither can wear makeup (R-PCC-4).
- **This reverses RD-P23-4** (*"Three, not more"* people per tone). The platform asks for one person per tone, plus `Skin_Tone34`.
- The platform's tone row keeps working on one person: it changes the Variant and keeps the Material token, whatever the token is.

**Q-PCC-2 — Retire the twelve `Skin_Fitzpatrick{II,IV,VI}_Clean_Synth{All,Freckles,Marks,Veins}` drafts, their recipes and their twelve colour maps.**
- RD-P23-8 kept them as *Skin Layers*' references. The platform no longer shows them, and one archived composition names one.
- If *Skin Layers* still needs a reference, the generator (`gen_synth_skin.py`) remakes them: the ask is about what ships, not about the tool.

**Q-PCC-3 — Retire the ten `Eye_Synth*` drafts, their recipes and their ten colour maps.**
- They were made *"to be judged in Studio beside the MakeHuman eyes"*; that look has not happened, and the platform's eye work is parked on a drawing defect of its own.
- The weakest of the three asks: if the library would rather hold them until the eyes are judged, say so and the platform leaves them be.

**Q-PCC-4 — Say how a removal reaches the platform.**
- None of the 34 has been in a released catalog; all are `candidate` or `draft`. `Manifest.md`'s retire rule is marked "Reevaluate" before 1.0, and Phase 23.2 deleted three drafts outright.
- The platform's test suite holds an exact list of the library's Creator-selectable names and a copy of the catalog. It updates both in the same change as the snapshot that drops the 34 — so it needs to know **which snapshot**.

**What the platform keeps using:** `Skin_Fitzpatrick I–VI`, `Skin_Tone34`, `Lips_*`, `Nail_*` (the six tones, `Nail_Natural`, `Nail_Tone34`), `Eye_Natural`, `Eye_Green`, the four eye parts, `Teeth_Natural`, `Enamel_`, `Gum_`, `Tongue_`, `Hair_Natural`, `Hair_DarkBrown`, and the four makeup pieces.

---

## A suggested ledger row

| # | Need | State |
|---|---|---|
| P-next | The platform draws one person per tone plus `Skin_Tone34`; it asks that `Skin2`, `Skin3`, the twelve `Synth` skins and the ten `Eye_Synth` eyes leave the library (Q-PCC-1 … 3), and to be told the snapshot they leave in (Q-PCC-4). | asked 2026-11-14 |

---

## Status

- **Pass 1** (the platform, 2026-11-14): six reports, four asks.
- **Open:** Q-PCC-1 … 4, with the library.
- **Next:** the library's reading.
