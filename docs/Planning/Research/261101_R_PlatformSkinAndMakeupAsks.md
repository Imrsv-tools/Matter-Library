# Research — The platform's skin phase: what it draws from the library, and the makeup, polish and pigment it needs (2026-11-01)

**Mnemonic:** `PSM` — reports `R-PSM-n` (for the ledger), asks `Q-PSM-n` (for the library).
**Mode:** an asks doc, written from the platform's side. It commits the library to nothing.
**Asked by:** the platform's lead, through the platform's skin phase (*The First Skin Set*), 2026-11-01: *"send the asks"*.
**Public repo:** needs and uses only. No consumer paths, code or tracker numbers.

**Read against:** this repo at `e0f0ca2` (`SkinMaps.md`, `PlatformDependencies.md` P32–P35, `Phase24_OneValidatedSkin.md` and its RD-P24-3, RD-P24-6). OMF agreed the character model these asks describe on 2026-11-01.

**Passes:** the reports and asks below are the platform's (Pass 1, 2026-11-01). **Pass 2 is the library's reading** (2026-11-02), then the open questions, `## Resolved` and the Status footer, which belong to the doc.

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

*The library files it as **M14**, not P36: the platform's asks of the library are the `M` table (the next free id, listed 2026-11-02); the `P` table is the library's asks of the platform.*

---

## Pass 2 — The library's reading (the library, 2026-11-02)

**Asked for by** the lead (2026-11-02): *"[the platform's skin phase] is goign to be stuck waiting for you to draft makeup, bruises etc... Seems like we are VERY far away from that since we haven't finished the head yet"*, then *"Please start a reserach session with that ask"*.

**Examined:** this repo after converging with `origin/main` (a merge; the incoming commits were material-batch work, none character or master); the ledger; every skin, lips and nail recipe; `serve_to_stage.py`; `build_masters.py`; `LCDSchema.md` §Base colour map and §Shine maps; `SkinMaps.md`; `gen_skin_shine.py`; `261027_R_CharacterMaterials.md` (CMT) and the Roadmap's character entries. **On the platform's side, read in place and never pulled:** its skin phase's doc at its newest commit (2026-11-02, not yet pushed). That phase is **executing**: the shine maps, the tangents, 8K, the lips in the body and the tone and Nails rows are built and wait for its first sitting.

**The altitude:** an audit of what the asks need from what exists, and which wait on what. The design of makeup is *Skin Layers*' discovery; this pass does not make it.

### F-PSM-1 — Two asks hold the platform's work; none waits on Phase25

- **The platform's plan holds two steps for the library:**
  - **"Finished skins only"** in the skin list waits on **Q-PSM-6**.
  - **"The merge"** (makeup draws at all) waits on **Q-PSM-2** (a format and some pieces) **and Q-PSM-7** (the slots).
  - The rest of its phase is built or buildable without the library, including its first sitting (the skin).
- **Q-PSM-1, -3, -4 and -5 hold no step.**
  - Q-PSM-1: the skin draws on its lips with neutral gloss until then.
  - Q-PSM-3: only a pigment piece needs it.
  - Q-PSM-4: the sitting uses an existing nail that is not a tone (`Nail_Natural`).
  - Q-PSM-5: a confirmation.
- **None of the seven reads Phase25.**
  - Phase25 paints a head's colour map in the body's layout; if it wins, the maker turns it into a structure.
  - Q-PSM-1 and Q-PSM-3 apply to *the finished skins*. A Phase25 skin would carry them the same way: RD-P24-6 already names Phase25 as a caller of the maker that writes the fields.
  - The coupling is **shared means, not data**: the machine with Unreal runs one heavy GPU job at a time (Phase25's generation, a master build, a look view), and the lead's sittings.
- **ML_P25_D5's reading holds, with one correction:** Q-PSM-7 is the critical path **together with Q-PSM-2**. Slots alone draw nothing until there is a piece to merge into them.

### F-PSM-2 — Q-PSM-6 is answered by a field that already ships: `status`

- **Measured 2026-11-02 (recipes):**
  - the 12 `Skin_Fitzpatrick{II,IV,VI}_Clean_Synth{All,Freckles,Marks,Veins}` are **`draft`**;
  - the 18 finished skins (`Skin`, `Skin2`, `Skin3` × six tones) and `Skin_Tone34` are **`candidate`**;
  - so are every `Lips_*` and `Nail_*`.
- **The dev install serves it per article.** `serve_to_stage.py` writes each recipe's `status` into the served catalog, `draft` when a recipe has none. The runtime catalog and the site file carry the same field (`RuntimeCatalog`, `SiteFile.md`).
- **Why the platform thought status could not do it:** its discovery counted `Skin_Tone34` and `Nail_Tone34` as drafts. Its own plan corrected that when it re-anchored after Phase24. With that fixed, status splits the 12 from the 19 exactly.
- **The answer:** list a skin when its `status` is not `draft`.
- **The library's side of the rule (proposed):** a skin that is not meant for a Creator stays `draft`.
  - The 12 Synth sets stay `draft`: they carry marks *as whole skins* only until *Skin Layers* ships marks as pieces (CMT Pass 4).
  - ⚠ `candidate` means the skin passed Storm and Blender in the parity rig (Glossary *Status lifecycle*). That checks the tools agree, not the lead's look verdict. For every skin today the two agree. The proposed rule is what keeps them agreeing.

### F-PSM-3 — Q-PSM-5 holds, with one addition

- **A skin carries its person's own marks today.** The structures and the Synth sets bake freckles, veins and moles into the colour map. P32's note of 2026-10-27 records the lead seeing a Synth skin's freckles and moles in Studio. Removing makeup removes nothing from a skin.
- **The library's design also makes marks into pieces.**
  - *Skin Layers*' Outcome (Roadmap; seeded on the lead's word 2026-10-26, widened 2026-10-27) says *a Creator adds … freckles, veins, moles …*.
  - CMT Pass 4 lists *mole, freckle field, vein field* among the effect pieces, and *freckles* among the skin's own controls.
- **So the split is:**
  - the person's own marks belong to the skin;
  - **a mark the Creator adds is a piece**, and goes with the makeup list.
  - This fits R-PSM-5 as long as the app treats an added mark as a piece.
- **Drafted reply:** *"Yes. A skin's own marks stay the skin's. Marks a Creator adds are pieces."* For the lead to confirm (Q-PSM-8).

### F-PSM-4 — Q-PSM-7 is a contract change in three tools, not a builder edit

- **The platform's description is right.**
  - The Subsurface master reads five pictures on the mesh's own layout: `base_color_map` and the four shine maps, all on texcoord 0 (LCDSchema §Base colour map, §Shine maps).
  - Its overlays are `tiledimage`s at their own real-world size (§Render-role texture nodes).
  - Nowhere takes a per-character layer.
- **What the slots touch: every reader and writer of a Subsurface picture input.** The shine maps took the same road. Grep of `roughness_map`, 2026-11-02:
  - the contract: `LCDSchema.md`, a section like §Shine maps;
  - the MaterialX graph Storm reads: `tools/converters/assemble_mtlx.py`;
  - the Blender masters: `blender/masters/article.py`, `load_article.py`;
  - the Unreal builder: `unreal/MatterRuntime/Scripts/build_masters.py`;
  - the rig's drivers: `tools/parity/drivers/unreal.py`, `blender_render.py`;
  - the recipe check: `tools/validators/validate_recipe.py`.
  - By `LOCAL_DELTAS.md` §Weighting that is a contract change and a consumer-facing format: a phase, not a `/quick-fix`.
- **No runtime publish is needed before the platform can start.**
  - At its neutral (no coverage, amount 0) every skin draws as today. A builder change that alters nothing at its defaults needs no new runtime (the lead, 2026-10-05).
  - The platform rebuilds its masters from the builder's source (R-PSM-1).
  - The library's **own** look and rig check of the slots still needs a runtime that has them, built on the machine with Unreal.
- **Choices the format must make (for *Skin Layers*' discovery, not here):**
  - where the makeup colour sits against the colour map, and whether the scatter colour follows it (it follows the colour map today, `subsurface_follows_base`);
  - whether finish replaces the roughness map's value or moves it, and against the wetness control;
  - premultiplied colour or coverage in alpha;
  - the slots' size;
  - the lips and nails are Subsurface too, so they get the slots at their neutral by construction.
- **⚠ A gap between Q-PSM-2 and Q-PSM-7: relief.**
  - Q-PSM-2's placed pieces carry relief (a raised scar), and CMT Pass 4 sketches relief and depth for marks.
  - Q-PSM-7 asks only for colour + coverage and finish.
  - A merged layer with no relief slot cannot draw a raised scar.
  - Either a third picture (a tangent-space relief, added like `normal_map`), or relief stays out of the first pieces. To raise with the platform before the format is written.

### F-PSM-5 — Q-PSM-1 is small: the shared roughness map leaves the lips neutral today

- **The 18 finished skins all wear one shared** `Skin_roughness_sUKN.png` (grep of the `.mtlx`, 2026-11-02).
- **Its lip region is neutral.** `gen_skin_shine.py` zeroes the lips' offset ("the lips keep their own finish", RD-P22-8), so on a body with no lips part the lips draw at the skin's average.
- **Only a Phase24 subject sets its lips' own value:** `Skin_Tone34` takes `lips_to` 0.30 (RD-P24-3). The shared set has no such option yet.
- **Who would see a change:**
  - Only a body with no lips part: the platform's new base.
  - The `Lips_*` articles do not wear the roughness map (RD-P22-8).
  - The rig casts `Lips_<Variant>` on the lips part whenever one exists (it casts the skin there only when none exists, RD-P24-3).
  - So the rig would show nothing new. **Judging the gloss needs the skin cast on the lips for a skin that has a `Lips_` article:** a small option on `rig.cast_for`.
- **Size of the job:** a `lips_to` for the shared set, regenerate the one map, look at it. The 18 articles name the same file, so no recipe changes. G8 checks only the map's shape.
  - 0.30 was solved against one reference for one subject; using it for all 18 is a judgement, made in the look view.
  - One sitting: a `/quick-fix` once the lead wants it.
- **Wet lips as a piece** is Q-PSM-2's.

### F-PSM-6 — Q-PSM-3 refines two rulings, so it is *Skin Layers*' to rule

- **RD-P24-6:** the fields are *"kept by being reproducible"*, not tracked, because at 8K they would add hundreds of MB to LFS.
- **RD-SKM-3** (the lead, 2026-10-14, *"2b"*): one colour map per tone through `base_color_map`, *"with no new input"*. The recorded consequence, and the Glossary's *Pigment map*, is *"the pigment maps stay inside the maker; what ships is their baked colour"*.
- **Shipping the fields for the app's merge needs no master input,** so it does not touch the *"no new input"* half.
- **It does reverse "stay inside the maker".** That is a ruling to make, with its size, when *Skin Layers* designs pigment pieces.
  - The platform does not need it before then: only a pigment piece reads the fields.
  - Paint pieces (foundation, lipstick, a tattoo, dirt) do not.

### F-PSM-7 — Q-PSM-4 can be built now, as ordinary articles

- **The nails are `Subsurface` articles** (`Nail_FitzpatrickII`'s recipe). A polish is a nail article with its own colour and finish, matte to gloss.
- **The platform's pairing already lets a polish stay:** a nail follows the tone only when its Variant is a skin's Variant. So a polish needs only a Variant that is not a tone; its name is chosen when it is built (`Identity.md`).
- **It waits on nothing:** a few wish-list rows built the `/matter-generate` way, judged on the character.
- **Chipped polish** would be a placed piece (Q-PSM-4), later.

### F-PSM-8 — What the reports change in the ledger

- **R-PSM-1 and R-PSM-4: the platform is building P34 and P35.**
  - Both are built in its skin phase and wait for its first sitting (2026-11-02).
  - Their status can move from `OPEN` to `IN PROGRESS`, dated.
- **R-PSM-3: the base character drops its lips part.**
  - P32 gains a dated note.
  - The `Lips_*` articles stay, drawn wherever a lips part remains.
- **R-PSM-2: the cost note** is an input to the size steps: RD-OVS-2, and Phase25's 2K → 4K → 8K (RD-P25-20).
- **R-PSM-5** matches *Skin Layers*' design: pieces placed on the body, the platform's stack bake (CMT Pass 4). Nothing to record beyond this pass.

### What this pass leaves for the lead

- **Answer now:** Q-PSM-6 (F-PSM-2); Q-PSM-5 drafted (F-PSM-3). Both await one word (Q-PSM-8).
- **Can be built now, each a sitting:**
  - the M14 row and the P32 / P34 / P35 notes (a `/quick-fix`);
  - the lips' gloss in the shared map (F-PSM-5);
  - a few polish articles (F-PSM-7).
- **A phase:** Q-PSM-7 + Q-PSM-2 (the slots, the format, the first pieces), with Q-PSM-3's ruling inside it. That is *Skin Layers*, or its first part. **When it runs** is Q-PSM-9.

---

## Open questions (for the lead)

| # | Question | The library's reading |
|---|---|---|
| **Q-PSM-8** | **Confirm the two answers to the platform.** Q-PSM-5: *a skin's own marks stay the skin's; marks a Creator adds are pieces.* Q-PSM-6: *list a skin whose `status` is not `draft`; the library keeps a skin not meant for Creators at `draft`.* | Both rest on what ships today (F-PSM-2, F-PSM-3). Neither changes a file. |
| **Q-PSM-9** | **Is *Skin Layers* numbered now, to run alongside Phase25 and ahead of *Eyes in the Shader*?** The 2026-10-27 order (RD-CMT-3) puts it after Eyes. The platform's makeup is held on it (F-PSM-1). **(a)** Number *Skin Layers* now: its discovery starts while Phase25 runs, and its first part is the slots, the format and a few pieces. Eyes follows it. **(b)** Number only that first part now, as its own phase. The rest of *Skin Layers* (more pieces, the Blender kit, pigment pieces) keeps its place after Eyes. **(c)** Keep the order. The platform can close its skin phase with the skin and polish and carry makeup to a later phase. | Not decided here. Whichever is chosen, the cost is **shared means**: one heavy GPU job at a time on the machine with Unreal, and the lead's sittings, beside Phase25. **(b)** asks least of those and unblocks the platform's held step. It needs a name; *Skin Layers* keeps its Outcome. |

## Resolved

*(None yet.)*

## Status

- **Passes captured:**
  - Pass 1, the platform's reports and asks (2026-11-01).
  - Pass 2, the library's reading (2026-11-02): F-PSM-1 … 8.
- **Current direction:**
  - None of Q-PSM-1 … 7 waits on Phase25 (F-PSM-1).
  - The platform's makeup is held on **Q-PSM-7 and Q-PSM-2 together**: a contract change in three tools plus a format and first pieces. That is a phase (F-PSM-4).
  - **Q-PSM-6 is answered** by the `status` field that ships today (F-PSM-2).
  - **Q-PSM-5 is answered as drafted** (F-PSM-3).
  - Both await the lead's confirmation before they go to the platform.
  - Q-PSM-1 and Q-PSM-4 are each a one-sitting build (F-PSM-5, F-PSM-7).
  - Q-PSM-3 is a ruling for *Skin Layers* (F-PSM-6).
  - ⚠ The platform should hear about the relief gap between Q-PSM-2 and Q-PSM-7 before the format is written (F-PSM-4).
- **Open questions:**
  - Q-PSM-8 (confirm the two answers);
  - Q-PSM-9 (when *Skin Layers*, or its first part, runs: alongside Phase25 and ahead of Eyes, or as ordered).
- **Ledger:** M14 not yet filed. It is offered as a `/quick-fix` (`PlatformDependencies.md`), with P34 and P35 moving to `IN PROGRESS` and a note on P32 (F-PSM-8).
- **Next step:**
  - The lead answers Q-PSM-8 and Q-PSM-9.
  - Then the M14 quick fix carries the confirmed answers to the platform.
  - If a phase is numbered, its seed and stub go on the Roadmap on the lead's word (`research.md` §Landing).
