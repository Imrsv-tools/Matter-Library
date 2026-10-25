# Research — A measured fabric physics card on fabric materials (the platform's ask)

**Opened:** 2026-10-25 · **Mode:** research. It gathers and commits to nothing; the library's own discovery rules each ask.
**Mnemonic:** `FPC` (ids `FPC-Qn`, `FPC-Fn`). **Pass 1** is written from the platform's side. The library's review of it against its own tree is a later pass, as `260928_R_PlatformAppearanceAsks.md` Passes 5–6 were.
**Requested by:** the IMRSV platform's wardrobe research. The lead's direction (2026-10-25, condensed): garments should be made in **real garment-making tools** (Marvelous Designer, CLO 3D, Blender) with **physics-based fabrics defined by measured properties** — weight (GSM), stretch and elasticity, bending stiffness, shear resistance, thickness, surface friction, drape — so as *"not to recreate the wheel"*. Fabrics belong to this library, so the fabric half of that is asked here.

**Question:** what does a fabric article need to carry so that a cloth solver in the app drapes a garment the way the garment tool it was made in did?

**Extends, does not replace:** `260928_R_PlatformAppearanceAsks.md` (the wardrobe fabrics, AP-F7–F11, A5), `PlatformDependencies.md` (*From IMRSV to the Matter Library*: no row covers a fabric's physics; the next free id at writing is M14). Nothing in `docs/specs/` or `docs/Planning/` names fabric physics, a cloth solver's inputs or U3M (grep for *physics*, *simulation*, *drape*, *U3M*, *stiffness*, *friction*, *deformable*, 2026-10-25). The nearest existing work is the thumbnails' **headless cloth drape in Blender** (`docs/Learnings/Blender/Blender.md` B15; textiles are pictured as a draped cloth), which is where a drape check could start (A5).

**Public-repo note.** The platform's planning is private. It is summarised here by what it needs from the library and how it will use it — no platform paths, code or ruling ids.

**Measured at:** this repo's `af2f758` (origin/main, 2026-10-25).

---

## The short version

- **The app will drape garments, once per pose, with a cloth solver.** It is not live cloth: the app settles each garment around a character's pose and keeps the result. The solver needs each fabric's **mechanical numbers**, and today nothing supplies them.
- **Garments are made in real garment tools** on standard bodies, and arrive with their fabrics named from this library. **The same measured card should drive both the tool and the app's solver**, so a garment hangs in the app as it hung where it was made.
- **The ask is a fabric physics card on fabric articles:** areal density, thickness, stretch (warp / weft / bias), shear, bending (warp / weft), friction, damping marked as *tuned*, the drape coefficient as a **check target**, construction and composition — in SI units, each with how it was measured.
- **U3M in and out, not U3M as the schema:** read and write the open fabric package, and carry its raw test data and vendor blocks through untouched.
- **One converter per solver**, starting with the open solver the app uses today; and names that line up with the proposed OpenUSD deformable material, so warp / weft reduce to it.
- **Every design choice is the library's:** where the card lives, its names, its units' form, where its values come from under CC0.

---

## Pass 1 — What the app is doing, and what it needs

*Written from the platform's side, 2026-10-25.*

### How the app will use a fabric

- **FPC-F1 — A garment is made elsewhere and draped in the app.** A maker builds a garment in a garment tool (Marvelous Designer first, CLO second, Blender alongside, or an open pattern tool) on a **standard body** for its size, and exports it. The app puts it on a character, then — while the Creator holds a control — eases the character from rest into a scene's pose while a cloth solver settles the garment around it. On release the settled shape is kept for that pose, as plain USD. **No cloth runs during playback.**
- **FPC-F2 — The first draping test ran on guessed numbers.** The platform has run one garment through an open cloth solver this way (Newton's VBD solver, Apache-2.0). The storage half works exactly. The fabric's mass, stretch and bending were **set by hand**, because no fabric in the app carries them. Two lessons bear on the card:
  - what holds a garment *on* the body (a waistband, a collar) is the **garment's**, not the fabric's — it stays out of the card;
  - contact needs a **thickness** — a solver keeps cloth that far from the body and from itself.
- **FPC-F3 — The garment tools already work this way.** CLO and Marvelous Designer (one solver) expose stretch weft / warp, shear, bending weft / warp, buckling, internal damping, density and friction, as **unitless 0–99 sliders**, with weight and thickness shown in g/m² and mm [read, CLO's fabric guide]. A kit of strip, cantilever and force readings fills them from a real swatch [2nd]. Browzwear's analyser reports mass, thickness, bend, stretch, linearity and shear [read]. **No neutral parameter set is shared between tools** — each converts from its own instrument's readings.

### What a fabric's physics is, in the trade's own terms

- **FPC-F4 — Each property has a lab test,** and the two instrument systems (KES-F and FAST) measure most of them on one swatch [2nd]:

  | Property | Unit | Measured by |
  |---|---|---|
  | Weight (areal density) | g/m² (GSM); kg/m² = GSM / 1000 | ISO 3801 / ASTM D3776 |
  | Thickness | mm, at a stated pressure (~1 kPa) | ISO 5084 |
  | Stretch (tensile), **warp, weft and bias** | N/m at low strain; a force–strain curve | ISO 13934-1 (strip); FAST-3 (E5 · E20 · E100); KES-F |
  | Shear rigidity | N/m | KES-F *G*; FAST (from bias extension) |
  | Bending rigidity, warp and weft | N·m (per unit width) | ASTM D1388 (cantilever, Peirce); KES-F *B*; FAST-2 |
  | Friction | coefficient (static / dynamic) | KES-F *MIU* |
  | Drape coefficient | % | ISO 9073-9 (Cusick drape meter) |

- **FPC-F5 — Drape is an outcome, not an input.** The drape coefficient is what the other properties *produce* when a circle of fabric hangs over a disc. So it is the number a simulated swatch should match — a check on a card, not a value fed to a solver.
- **FPC-F6 — Damping is not measured.** Solvers need it to settle; no standard test gives it. A card that carries it should say so.

### The open formats nearby

- **FPC-F7 — U3M is the open fabric package, but its physics is per vendor.** U3M (Vizoo and Browzwear, **BSD-3-Clause**) carries PBR appearance and a physics part: `raw_data` (the instrument's own test curves) and **vendor blocks** (Browzwear's: mass, thickness, friction, stretch, shear, bend, hysteresis …) which other apps read *"only with their consent"* [read]. 25+ apps read U3M, Blender, Browzwear, Optitex and Style3D among them [read]; CLO's support is unconfirmed [2nd]. **So U3M is the exchange format garment tools and fabric vendors speak, but its vendor blocks are not a neutral schema to adopt.** AxF is appearance only [2nd].
- **FPC-F8 — OpenUSD's direction is isotropic.** The proposed surface-deformable material (`OmniPhysicsSurfaceDeformableMaterialAPI` at the time of reading: density, friction, stretch / shear / bend stiffness, thickness) has **no warp / weft**, and is marked *"subject to change"* [read]. A card with warp and weft reduces to it; the reverse loses the weave.
- **FPC-F9 — No openly licensed table of measured values per fabric type was found.** The few measured datasets the platform found carry no licence [read / 2nd]. Where a card's numbers come from is therefore the library's question under its CC0 rule (FPC-Q2).

### What the library holds today, as it touches this

- **FPC-F10 — Eleven `synthetic/textile` articles, five constructions.** Woven: `Canvas_Natural`, `Denim_Indigo`, `Denim_LightWash`, `Satin_Natural`, `WoolSuiting_Natural`. Knit: `Cotton_Jersey`, `StretchKnit_Natural`. Non-woven: `Felt_Natural`. Openwork: `Lace_Floral` (Masked). Hide: `Leather_Brown`, `Leather_Natural`. So *woven / knit* alone does not cover what the library already holds; `Rubber_Natural` (soles, `synthetic/polymer`) is a garment part with no cloth behaviour at all.
- **FPC-F11 — A tint does not change a fabric's mechanics.** `Denim_Indigo` and `Denim_LightWash` hang alike. That bears on whether a card is per article or shared (FPC-Q3).
- **FPC-F12 — Where article facts live today.** The `.mtlx`'s internal `imrsv_metadata` nodedef carries a few hints (master, scale, group, contributor, licence, `fits`); the runtime catalog stays lean and leaves parameters to the `.mtlx` (*What the runtime catalog does NOT carry*); provenance never reaches the catalog. MaterialX itself has no physics vocabulary. So the card has no obvious home yet (FPC-Q1).

### The asks

| # | Need | Why the app needs it | What matters for this use |
|---|---|---|---|
| **A1** | **A fabric physics card on fabric articles**: areal density (kg/m²), thickness (m, at a stated pressure), stretch warp / weft / bias (N/m at low strain, optionally a force–strain curve), shear rigidity (N/m), bending rigidity warp / weft (N·m), friction (static / dynamic), damping marked **tuned, not measured**, the drape coefficient (%) as a **check target**, construction and composition | The app's solver drapes each garment from its fabrics' numbers; today there are none (FPC-F2) | SI units with the test each value came from (FPC-F4), so a converter never guesses; an absent value means *not known*, not zero; a card states whether it was measured, derived or estimated |
| **A2** | **Read and write U3M** for fabric articles; a U3M's `raw_data` and vendor blocks **carried through untouched** | Garment tools and fabric vendors exchange fabrics as U3M (FPC-F7); a maker should bring a measured fabric in, and take the library's out, without loss | The card is the library's own neutral schema, filled from U3M where it can be; the vendor blocks are never re-interpreted or dropped, so a round trip gives the vendor back its own block |
| **A3** | **One converter per solver**, starting with the open solver the app uses today: Newton's VBD (its cloth takes `density`, mass per area; `tri_ke` / `tri_ka`, membrane stiffness; `edge_ke`, bending; damping terms) | The card is solver-neutral; each solver wants its own numbers, and the app should not hold that mapping privately | A converter is the only place warp / weft become an isotropic number for a solver that has none; later converters (a garment tool's sliders, Blender's cloth) are the library's choice |
| **A4** | **Names that line up with the proposed OpenUSD deformable material**, so warp / weft reduce to its isotropic terms | The app's garments are USD; when OpenUSD settles a deformable material, the card should map onto it without a rename (FPC-F8) | Alignment, not adoption: the proposal is *subject to change* and isotropic |
| **A5** | **A drape check**: a simulated circular swatch draped as in ISO 9073-9, its drape coefficient compared with the card's | It is the one number that proves a card's other numbers hang right (FPC-F5); without it a card is a guess with units | The library already drapes cloth headless in Blender for its textile thumbnails (Learnings B15), and its converter for the app's solver (A3) could run the same swatch |
| **A6** | **First cards on the fabrics the app's garments wear today**: the eleven textiles of FPC-F10 (leather and felt included); and a fabric for a **loose garment** (a coat or skirt), which is the platform's next draping test | Its first test was a skin-tight suit, where there is little to drape; a loose garment is where fabric numbers show | Even estimated values, marked as such, unblock the app; measured ones replace them later |

### What the platform needs back

- The card's shape, units and where it lives, so the app's solver reads it from the dev install the way it reads everything else from the library.
- For each carded article, which values are measured, derived or estimated.
- The Newton VBD converter's output for the first cards (A3), or its rule, so the app can check its own drape against the library's swatch (A5).

### Open questions for the library

- **FPC-Q1 — Where does the card live?** In the `.mtlx`'s internal nodedef (like the hints of FPC-F12), a file beside the `.mtlx`, the site file, the dev catalog, or a U3M beside the article? The app needs to read it from the dev install; the runtime catalog's lean rule may argue for a file beside the article.
- **FPC-Q2 — Where do the numbers come from, under CC0?** Library measurements (a lab, or a home cantilever and strip test), values stated as facts in published papers with a grounding citation (as Physically Based grounds colour today), or a vendor's U3M with its consent? FPC-F9 found no open table.
- **FPC-Q3 — One card per article, or one per fabric shared by its variants?** A tint does not change mechanics (FPC-F11), so `Denim_Indigo` and `Denim_LightWash` could share one.
- **FPC-Q4 — The construction vocabulary.** Woven / knit is not enough for what the library holds (FPC-F10): non-woven, openwork and hide at least. And composition: by fibre and percentage?
- **FPC-Q5 — Stretch: a low-strain value, a curve, or both?** Most solvers take one stiffness; knits and stretch fabrics are strongly non-linear. Is bias measured or derived from warp, weft and shear?
- **FPC-Q6 — Is damping in the card at all, or in each converter?** It is tuned per solver (FPC-F6).
- **FPC-Q7 — Here, or in the Open Morphology Foundation's apparel reference?** That project plans an open apparel reference that reads its body measurements, and lists *fabric behaviour* among its inputs. The platform leans here, since this library owns materials, with that project citing it.
- **FPC-Q8 — Does adding a card change an approved article's version?** A card adds no pixel and no Creator port, but the library's articles are immutable after promotion.

### A suggested ledger row

For `PlatformDependencies.md`, *From IMRSV to the Matter Library*, when the library takes this up (the id is provisional; the library assigns the next free one):

> **M14 — A measured fabric physics card on fabric articles** (2026-10-25): areal density, thickness, stretch warp / weft / bias, shear, bending warp / weft, friction, damping marked tuned, the drape coefficient as a check target, construction and composition, in SI units with the test each came from; U3M read and written, its raw data and vendor blocks carried through untouched; one converter per solver, the first for Newton's VBD; names aligned with the proposed OpenUSD deformable material; a drape check on a simulated swatch; first cards on the eleven textiles and a loose-garment fabric. · *Why:* the app drapes each garment once per pose with a cloth solver, and garments are made in real garment tools; one measured card should drive both, so a garment hangs in the app as it did where it was made. · *Owner:* Matter Library (the card, the converters, the check) · the platform's runtime (its solver reads the card). · *Pairs with:* `261025_R_PlatformFabricPhysicsAsks.md`.

---

## Sources

**[read]** = primary page or file fetched by the platform's research; **[2nd]** = snippet, mirror or secondary page. Licences are as stated by their sources.

- **U3M:** [github.com/vizoogmbh/u3m](https://github.com/vizoogmbh/u3m) (BSD-3-Clause) · its physics examples and raw-physics documentation, [u3m1.1/physics/](https://github.com/vizoogmbh/u3m/tree/master/u3m1.1/physics) · [u3m.info](http://www.u3m.info)
- **The open solver:** [github.com/newton-physics/newton](https://github.com/newton-physics/newton) (Apache-2.0) and its [documentation](https://newton-physics.github.io/newton/) (`ModelBuilder.add_cloth_mesh`: `density` is mass per unit area) · [github.com/NVIDIA/warp](https://github.com/NVIDIA/warp)
- **OpenUSD:** [OpenUSD proposals](https://github.com/PixarAnimationStudios/OpenUSD-proposals) (deformable bodies) · [UsdPhysics](https://openusd.org/release/api/usd_physics_page_front.html)
- **Garment tools:** [CLO fabric guide](https://support.clo3d.com) · [Browzwear](https://browzwear.com) (FAB analyser, U3M) · [Hohenstein](https://www.hohenstein.com) (one lab method feeding several tools) [2nd]
- **Test standards:** [ISO](https://www.iso.org) 3801 (mass per area), 5084 (thickness), 13934-1 (tensile strip), 9073-9 (drape coefficient) · [ASTM](https://www.astm.org) D3776 (mass per area), D1388 (stiffness, cantilever) · KES-F ([Kato Tech](https://english.keskato.co.jp)) · FAST (CSIRO) [2nd]

---

## Status

- **Passes captured:** 1 (2026-10-25, the platform's side): how the app will use a fabric (FPC-F1–F3), the trade's properties and their tests (FPC-F4–F6), the open formats nearby (FPC-F7–F9), what the library holds (FPC-F10–F12), asks **A1–A6**, questions **FPC-Q1–Q8**, a suggested ledger row.
- **Decided:** nothing; the library's discovery rules the asks.
- **Unverified, recorded as such:** CLO's U3M support; the exact form of the OpenUSD deformable-material proposal (*subject to change*); how Newton's `tri_ke` / `tri_ka` / `edge_ke` map onto N/m and N·m (the converter's to work out); every [2nd] item above.
- **▶ Next:** the library reviews Pass 1 against its tree, records the ledger row under its next free `M` id, and rules where the card lives (FPC-Q1) and where its numbers come from (FPC-Q2) before any card is written.
