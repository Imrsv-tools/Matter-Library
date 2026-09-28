# Phase09 — Character Appearance for Studio

**Status:** SEEDED (phase doc written 2026-09-28; discovery has not opened). **Numbered by the lead, 2026-09-28**, verbatim: *"seed Phase09 with items 1–3.. I would like to address this issue now"*. It answers the needs of the IMRSV platform's Appearance phase (Phase 66), which is under way and focused on Studio. **Deliberate gate:** it opens by the lead's `/discovery P9`, never by a slide from research.
- **Seeded from** `docs/Planning/Research/260928_R_PlatformAppearanceAsks.md`: the platform's asks (Passes 1–4) and the library's review of them (Passes 5–6).
- **The consumer asks it answers:** `docs/Planning/PlatformDependencies.md` **M3** (a Hair master) and **M4** (tone-matched lips and nails), plus the wardrobe fabrics (research A5).

## Outcome

**In Studio, a Creator can give a character any hair colour from one good hair material, pick any of six skin tones and have the lips and nails match, and dress it in clothes whose fabrics, soles included, come from the library in any colour.**

Concretely, at close:
- a `Hair` master and a light, tintable hair article (research A1, AP-F1–F4);
- lips and nails for each of the six skin tones, with a pairing Studio reads without a table of its own (A2, AP-F6);
- the first wardrobe fabrics: rubber, a light leather and a lighter denim wash, then as many of canvas, felt, satin, stretch knit and wool suiting as the phase holds (A5, AP-F8);
- all of them served to Studio as `candidate` through the dev install (`serve_to_stage.py`, Phase07 L4), and seen on the MakeHuman body in the rig.

## Why this is a phase

One user-facing result: Studio's characters get the hair, skin and clothing choices its Appearance work is built around. It carries calls that are expensive to unwind:
- **a new master token** (the 8th), which every consumer must map, and which Studio fails loud on until its own Hair master exists;
- **how a tone pairing is expressed** (article names or a served-catalog field), which Studio's skin-tone control will read;
- **the names of new articles**, which never change once they ship (BP4).

## Scope

**In:**
1. **The `Hair` master and a tintable hair article** (research A1; `PlatformDependencies.md` M3).
   - The `Hair` token: `MasterSet.md` (token list, master table, settings row: masked coverage, a hair shading model, two-sided) and every tool that lists the tokens (AP-F4: `assemble_mtlx.py`, `validate_material.py`, `recipe.schema.json`, `blender/masters/build_masters.py`, `tools/parity/scene/build_scene.py`, `tools/parity/JOB_FORMAT.md`).
   - The review's reading, for discovery to test: **settings-only over the existing OpenPBR graph** (AP-F2), so stock USD viewers keep matching and the `chiang_hair_bsdf` probe does not gate this phase.
   - **A new hair article authored at a light base**, so `base_color_tint` (a multiply that only darkens) reaches every hair colour (AP-F1). `Hair_DarkBrown` stays on Masked, so nothing Studio uses today breaks while its Hair master does not exist yet (research Pass 4).
2. **Lips and nails for the six skin tones** (research A2; `PlatformDependencies.md` M4). Up to twelve articles, and a deterministic pairing to each `Skin_Fitzpatrick*`.
3. **Wardrobe fabrics** (research A5, AP-F8). Pulled forward from Phase08's draft list (`260925_R_LibraryCoverage_FirstRelease.md`, the `synthetic/textile` and polymer rows), as Phase07 pulled cotton, denim and leather. Every fabric Studio recolours is **authored light**. First: rubber (every shoe's sole), a light leather, a lighter denim wash. Then: canvas, felt, satin, and the two the draft list lacks, a synthetic stretch knit and a wool suiting.

**Not now:**
- **Who splits a garment into its fabrics** (research A6, AP-Q5). A CC0 outfit is one mesh with several fabrics. If discovery rules that the library owns the split, it may come in; if Studio owns it, nothing is built here.
- **Colour on layers** (CM-Q5): garment prints, trims and fades, and makeup (research A7). It is a contract change, and it stays out unless the lead pulls it in.
- **A real skin-tone control** (research A4): a change to the frozen Creator vocabulary.
- The small cleanups the review noticed (the Glossary's retired-proxy row, Phase08's stale C2 / C3 blockers, `check_lcd_carrier.py` not seeing `cutout_map`): `/retro` or `/quick-fix` material.
- A release (Phase07 L4: Studio takes the dev install).

## Open questions (settle during this phase)

- **Is the `Hair` master settings-only?** AP-F2's reading, argued against D-E (the refused `Eye` master). (AP-Q1)
- **Do brows and lashes stay on the same article as the hair?** They share one today. (AP-Q2, AP-F3)
- **How is the tone pairing expressed:** names (`Lips_FitzpatrickIII…`), or a tone-family field in the served catalog beside `status` and `master`? (AP-Q3, AP-F6)
- **The hair article's name and base colour**, and whether a melanin-style parameter is ever wanted. (AP-Q4)
- **Which fabrics make the cut, and in what order?** Rubber first. (AP-Q6)
- **The garment split:** in or out (see Not now). (AP-Q5)

## Notes

- **Sequencing with Studio** (research Pass 4). A2 and A3 are additive: Studio can take them whenever they land. A1's new article renders as the missing material in Studio until Studio's Hair master exists, so it ships as a `candidate` and Studio switches when it is ready.
- **The platform's unconfirmed row:** P17's cut-out map source (AP-Q8). It does not block this phase, but the hair work meets it.
- **Consumer claims are recorded as reported.** The platform's code is private; see the research's Pass 2.

## Discovery Log

_(numbered passes accrue here: examined → finding → decision / hypothesis / open question)_

## Discovery Status

- **Passes captured:** —
- **Current working direction:** —
- **Open decisions:** —
- **Checks to carry forward:** —

## Execution Log

_(populated during execution)_
