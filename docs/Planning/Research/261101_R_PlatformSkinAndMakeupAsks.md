# Research — The platform's skin phase: what it draws from the library, and the makeup, polish and pigment it needs (2026-11-01)

**Mnemonic:** `PSM` — reports `R-PSM-n` (for the ledger), asks `Q-PSM-n` (for the library).
**Mode:** an asks doc, written from the platform's side. It commits the library to nothing.
**Asked by:** the platform's lead, through the platform's skin phase (*The First Skin Set*), 2026-11-01: *"send the asks"*.
**Public repo:** needs and uses only. No consumer paths, code or tracker numbers.

**Read against:** this repo at `e0f0ca2` (`SkinMaps.md`, `PlatformDependencies.md` P32–P35, `Phase24_OneValidatedSkin.md` and its RD-P24-3, RD-P24-6). OMF agreed the character model these asks describe on 2026-11-01.

---

## Reports — for the ledger

**R-PSM-1 — The platform's app will draw the four shine maps (P34).**
- Each map arrives on its own slot (`roughness_map_tex`, `normal_map_tex`, `cavity_map_tex`, `scatter_map_tex`), as linear data, sampled on the mesh's own layout.
- The masters are rebuilt from this repo's builder, unchanged.
- **The carrier rule is kept.** An article names its own file, and a picture a binding supplies wins.
- **A picture inside the installed library is named, never copied.**
- **An article without a map gets the exact neutral:** roughness 0.5, a flat normal, cavity white, scatter black.
- `coat_follows_normal` is set to 1 on a Subsurface article that declares `normal_map` and a coat.
- **The character's tangents become MikkTSpace-compatible**, from texcoord 0.
- Until this lands, every article that carries a shine map draws as "missing" in the app: the 18 skins and the six tone lips. The app refuses an input it does not carry rather than drawing a guess.

**R-PSM-2 — How big a picture costs in the app today.**
- The app loads a library picture uncompressed and keeps every mip: colour as 16-bit float, data as 8-bit.
- **One 8K skin set (a colour map and four shine maps) is about 2 GB of video memory in the app.** The same set at 2048² is about 128 MB.
- This is worked out from the formats, not yet measured. ~~The platform measures one 8K load before it plans.~~ *(2026-11-01, later: the app does not load an 8K picture at all today; the platform's skin phase makes it load whole, and its lead judges from that look whether to step down to 4K or 2K.)*
- It is an input to the library's later size tests (RD-OVS-2), not an ask.

**R-PSM-3 — The base character has five parts, and the lips are part of the body.**
- **The parts:** the body (lips included), the nails, the eyes, the mouth (teeth, gums, tongue), and hair, brows and lashes.
- **The app's base character stops having a separate lips part.**
- A skin on such a body colours the lips from its own colour map, as today. It glosses them from its own roughness map: the lip zone of RD-P24-3.
- **Older characters keep drawing correctly.** Where a character still has a lips part, the app goes on drawing the `Lips_*` articles there.

**R-PSM-4 — How a Creator picks a skin.**
- The Creator picks **a person** in the material window, then **changes the tone** from a row of the six tones beside it.
- **A tone change keeps the person.** It keeps the Material token and changes the Variant: `Skin2_FitzpatrickII` → `Skin2_FitzpatrickV` (P35 (1)).
- **The nails follow the tone.** One nail article per tone serves every person. *(2026-11-01, later: bare nails follow the tone; a polish the Creator picked stays through a tone or skin change. Polish is picked from a Nails row beside Skin and Eyes.)*

**R-PSM-5 — How the app stores and draws makeup.**
- **Makeup is a list of pieces on a character, merged into one layer on the skin**, so many pieces cost what one does. Each piece is on, off or changed mark by mark.
- **Two kinds of piece:**
  - **Fitted:** foundation, blush, eyeshadow, liner, lip colour and gloss. Each is painted for its zone of the face and picked, never placed.
  - **Placed:** a bruise, a scar, a tattoo, dirt. Each is put anywhere on the body or head by pointing at it, then moved, sized and turned.
- **What the composition stores:** the list, never pixels. Each piece is its library name, a point on the body's surface in its rest pose, size, turn, strength and marks.
- **What another app sees:** the list, but not the look. A future export will merge the makeup into the skin's own picture.
- **Nail polish is a nail material**, picked separately, so a face look never fixes the nails.
- **The person's own marks** (freckles, moles, veins, a birthmark) belong to the skin, not to makeup.

---

## Asks — for the library

**Q-PSM-1 — The lips' finish, in the finished skins.**
- RD-P24-3 glosses the lips from the skin's own roughness map, for Phase24's subject.
- **The need:**
  - the same lip zone in the roughness maps of the finished skins (or the shared shine set), when the library next remakes them;
  - **wet lips as a makeup piece** (lip gloss, Q-PSM-2), not as a coat on the skin. The skin has no coat (RD-P22-17).
- The `Lips_*` articles can stay as long as the library keeps them. The app draws them wherever a lips part remains.

**Q-PSM-2 — The makeup piece format.**
- **Fitted face pieces** (foundation, blush, eyeshadow, liner, lip colour and gloss):
  - authored in 3D and baked per layout, as the skin maps are;
  - each one **a shape with controls:** colour, strength, and finish from matte to wet;
  - a few shapes per zone, not a picture per colour.
- **Placed pieces** (bruise, scar, tattoo, dirt) as stamps. Each carries:
  - colour and coverage;
  - finish and, where it needs it, relief (a raised scar);
  - packed into two pictures per piece.
- **Two kinds of change, as OMF proposed:**
  - **pigment pieces** (flush, freckles, a bruise, a vein, a scar's colour) change melanin and blood, so they are right at every tone;
  - **paint pieces** (foundation, lipstick, eyeshadow, tattoo ink, dirt, surface blood) are colour, coverage and finish.
- **The need:**
  - the format, written as the library's contract;
  - a first handful of pieces;
  - the piece list's home (the library's catalog, with a group of its own).

**Q-PSM-3 — The skin's pigment fields, shipped.**
- A pigment piece needs the skin's own melanin and blood fields. The app's merge turns pigment into colour with the skin model's table.
- RD-P24-6 keeps the fields reproducible and unshipped for now, and *Skin Layers* is their owner.
- **The need:** the fields shipped beside a finished skin, with the model's table, in whatever form and size the library chooses.
- **The app's half:** its merge reads them.

**Q-PSM-4 — Nail polish as nail materials.**
- **The need:** a few polish articles (colours, matte to gloss), picked on the nails apart from the skin's tone.
- Chipped polish, if ever wanted, would be a placed piece.

**Q-PSM-5 — The person's own marks stay the skin's.**
- *Skin Layers*' freckles, moles and veins stay part of the skin, apart from makeup, so removing makeup never removes them.
- **The need:** confirmation that this split is the library's too.

**Q-PSM-6 — Telling a finished skin from a draft.**
- The app lists every skin article. The 12 `…Synth*` drafts show beside the 18 finished skins with nothing to tell them apart, and status alone cannot do it, since `Skin2`/`Skin3` are `candidate` too.
- The app will hide drafts from the skin list.
- **The need:** the field or rule that says which skins are finished, so the app filters on the library's word, not on names.

**Q-PSM-7 — Makeup slots on the skin's master** *(added 2026-11-01, later the same day; the platform's lead: "Ask library for slots")*.
- The app merges a character's makeup pieces into one layer (R-PSM-5). **The Subsurface master has nowhere to take it:** its overlays are tiled at their own real-world size, for wear and deposits; the only pictures on the mesh's own layout are the colour map and the four shine maps.
- The other road, painting the makeup into a per-character copy of the skin's colour and roughness maps, costs a full copy of each per character at the skin's size (about 1 GB at 8K), and more per mark with a different look. OMF's sketch is the opposite: merge once, and let a mark change a few live slots.
- **The need:** makeup slots on the Subsurface master, sampled on the mesh's own layout, built by this repo's builder:
  - a **colour + coverage** picture (the merged paint, premultiplied or with its coverage in alpha — the library's choice);
  - a **finish** picture (how far the makeup moves the skin's roughness, matte to wet), or its packing beside coverage;
  - **an amount** scalar, so a mark can fade the whole layer without a new merge;
  - the order against the skin's own maps written down (where the makeup sits relative to the colour map, the roughness map and the relief), so the look is the same in every renderer the library checks.
- Their neutral (no makeup) must leave every existing skin as it is today.
- A pigment piece (Q-PSM-3) reaches the colour + coverage picture after the app's merge turns it into colour, so it needs no slot of its own.

---

## A suggested ledger row (the library writes its own)

> | P36 | **Makeup, polish and the skin's pigment** (2026-11-01, [`261101_R_PlatformSkinAndMakeupAsks.md`](Research/261101_R_PlatformSkinAndMakeupAsks.md)). The makeup piece format and a first set of pieces (Q-PSM-2); the skin's pigment fields shipped (Q-PSM-3); nail polish articles (Q-PSM-4); the lips' gloss in the finished skins (Q-PSM-1); a finished-or-draft field (Q-PSM-6); makeup slots on the skin's master (Q-PSM-7). | The platform's characters wear makeup, marks and polish, merged into one layer per character. | the library | P34 · P35 · Skin Layers | OPEN |
