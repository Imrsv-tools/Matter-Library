# PhaseTBD — Glass and Light Colour

**Status:** SEED (2026-10-05). Not numbered; numbering is the lead's. Seeded by the lead's invocation, verbatim: *"/discovery Expose see-through colour, emission colour and emission brightness as Creator ports.. As normal, don;t hold everything else back just because of storm..."* The invocation is read as also opening discovery, so Pass 1 follows this seed.
**Mnemonic:** `GLC` (ids `Q-GLC-n`, `F-GLC-n`, `RD-GLC-n`; kept if the phase is numbered).
- **Seeded from:** the thin-glass thread of 2026-10-05 (`docs/Planning/Research/261005_R_PlatformThinGlassAsks.md`), and the lead's thought in that sitting, verbatim: *"I don't think we should bother with a 'colored' version of something unless it is adding a new texture that is truly needed to the equations... like clear glass and glass green... What is being added to glass to make it green?"*, then *"we could expose that as LCD I assume"*.
- **What it reverses:** the lead's ruling of 2026-09-25 in `docs/Planning/Research/260925_R_LibraryCoverage_FirstRelease.md` (E2: *"accept. A see-through colour is its own authored article, never a Creator tint, and no LCD change is made"*; E8, the same for emissive and utility colours). The lead was shown that ruling twice in the sitting before invoking this.

## Outcome

**A Creator sets the colour of glass and other see-through matter, and the colour and brightness of a light, with a control, in Blender and in Studio. The library then carries one clear glass and one light, not an article per colour.**

*(Seed wording, from the lead's invocation. Discovery's first act is to challenge it against the specs.)*

## Why this is a phase

One contract change carries it. The Creator vocabulary (`LCDSchema.md`) gains ports for values that today are fixed on the article: the colour seen through it, the colour it emits, and how bright it glows. Every implementation of the article moves with it: the assembler, the Blender masters and the exporter that makes the ports travel, the Unreal masters and the rig's driver, and Studio's controls (a hand-off). It is the shape of Phase10 (dust colour), which added three Creator colour ports the same way.

It is expensive to unwind for one reason: a Creator port is a public name every consumer binds to.

## Scope

**In (to settle at discovery):**
- The three values as Creator ports, declared only by the articles they mean something for.
- Every see-through and emissive article re-assembled with them.
- What becomes of the articles that differ from a sibling only by such a colour (`Glass_Green`; `LED_WarmWhite` and `LED_CoolWhite`), and of the wish-list rows of the same kind. Marked, never deleted.
- The naming rule that says a see-through colour is its own article (`260925_R_LibraryCoverage_FirstRelease.md` C5; `Identity.md` if it restates it).
- The hand-off row for Studio.

**Not now (to confirm at discovery):**
- Any change to how a renderer draws see-through matter (the thin-walled bend, the solid master's absorption): `PlatformDependencies.md` M6 and its research doc.
- Wear layers reaching the glow (dust dimming a light): Phase11's F-P11-9.
- Saved, named slider states (*personal saved variants*, the Roadmap's parking lot).

## Rulings carried in

- **RD-GLC-1 — Storm does not hold the rest back (the lead, 2026-10-05, in the invocation):** *"As normal, don;t hold everything else back just because of storm..."* Storm ignores the see-through colour today. A control that moves Blender and Unreal and not Storm is recorded as Storm's limit; it gates nothing.

## Seed questions (the seed against the docs)

*Each was put through discovery's four tests as it was written. None is a lead call yet; each is answerable by reading or measuring.*

1. **Q-GLC-1 [open] — The port names.** OpenPBR's own (`transmission_color`, `emission_color`, `emission_luminance`), as `LCDSchema.md` asks of every name? Those names are already shader inputs and Unreal master parameters.
2. **Q-GLC-2 [open] — The brightness port's meaning and range.** One meaning and one range, by the LCD rule. Today's value (12) is a relative number on the rig's scale.
3. **Q-GLC-3 [open] — Which articles declare which port,** and whether any article outside the see-through and Emissive masters authors emission.
4. **Q-GLC-4 [open] — What the Unreal side needs.** The masters already carry all three as parameters. Does the pinned runtime (`unreal-runtime-v3`) render a moved value as it stands, with only the rig's driver changed, or is a new build needed?
5. **Q-GLC-5 [open] — What a deposit does to these values.** Dust already takes transmission to none where it lies. Does it need to do anything to the see-through colour or the glow?
6. **Q-GLC-6 [open] — The pilot release.** Which re-assembled articles are in `matterlib-0.1.0`, so that it is re-frozen and the maintainer's promote is handed over.
7. **Q-GLC-7 [open] — The existing tint on these articles.** `base_color_tint` moves nothing on clear glass today. Does it stay declared?
8. **Q-GLC-8 [open] — The colour-only articles and rows.** How many, and what mark each takes.
9. **Q-GLC-9 [open] — The risk lane,** verified against the controls a new Creator port touches.

## Discovery Log

_(Pass 1 follows.)_

## Discovery Status

- **Passes captured:** none (seed only).
- **Current working direction:** —
- **Open decisions:** numbering (the lead's).
- **Checks to carry forward:** —

## Execution Log

_(populated during execution)_
