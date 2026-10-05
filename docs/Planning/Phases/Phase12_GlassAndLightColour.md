# Phase12 — Glass and Light Colour

**Status:** IN EXECUTION (2026-10-05; lane `build`). Brief written at discovery Pass 1 the same day. **Numbered Phase12 by the lead, 2026-10-05:** the invocation *"/execute Phase12"* (RD-P12-1). Seeded and opened by the lead's invocation, verbatim: *"/discovery Expose see-through colour, emission colour and emission brightness as Creator ports.. As normal, don;t hold everything else back just because of storm..."*
**Mnemonic:** `GLC` (ids `Q-GLC-n`, `F-GLC-n`, `RD-GLC-n`, minted while the phase was un-numbered and kept; ids minted from execution on are `P12`).
- **Seeded from:** the thin-glass thread of 2026-10-05 (`docs/Planning/Research/261005_R_PlatformThinGlassAsks.md`), and the lead's thought in that sitting, verbatim: *"I don't think we should bother with a 'colored' version of something unless it is adding a new texture that is truly needed to the equations... like clear glass and glass green... What is being added to glass to make it green?"*, then *"we could expose that as LCD I assume"*.

## Outcome

**A Creator sets the colour of glass and other see-through matter, and the colour and brightness of a light, with a control, in Blender and in Studio. The library then carries one clear glass and one light, not an article per colour.**

*(Seed wording, kept. Challenged at Pass 1: it is user-facing, and its second sentence is what click 5 judges.)*

---

## The Brief

### What changes, in one paragraph

Three values that an author fixes on the article today become **Creator ports**: the colour seen through see-through matter (`transmission_color`), the colour a light emits (`emission_color`) and how bright it glows (`emission_luminance`). Each is a plain *set*: the Creator's value replaces the article's, and the article's own value is where the control starts. An article declares a port only where it means something: the see-through colour on the two see-through masters, the emission pair on Emissive. Nothing else about any article changes, and an article on any other master assembles byte-identically.

### First human test

Reached in the rig's sheets (`uv run tools/parity/rig.py <article> --sweep`; the agent runs it and opens the sheet) and in Blender with the **installed** Asset-Browser library, the scene framed by the agent. The lead looks and judges; the lead types nothing.

| # | Step | What the lead looks at | Passes when |
|---|---|---|---|
| 1 | 12.1 | **Glass_Clear's** sheet, a new row *"see-through green"*, in Storm, Blender and Unreal | the glass turns green in Blender and Unreal, the wall still seen through it. Storm darkens and does not turn green (F-GLC-6; it gates nothing, RD-GLC-1) |
| 2 | 12.2 | Blender: Glass_Clear from the Asset Browser on the default cube, the grid wall behind; the lead changes the **see-through colour** swatch to amber | the glass turns amber as a Creator would see it; the agent then shows the value in the exported USD |
| 3 | 12.3 | **Diamond's** sheet, the same row | the body of the stone takes the colour in Blender and Unreal |
| 4 | 12.4 | **LED_CoolWhite's** sheet, the dim view: rows *"emission warm"*, *"brightness half"*, *"brightness double"*; then in Blender the lead drags the brightness | every row moves all three tools alike; the light dims and brightens under the lead's hand |
| 5 | 12.5 | One sheet: **Glass_Clear set to Glass_Green's colour** beside **Glass_Green** itself; and **LED_CoolWhite set to the warm colour** beside **LED_WarmWhite** | the lead judges whether the set one stands in for the authored one. That judgement decides the mark the colour-only articles take |

**Reconciled click by click:** click 1 needs only 12.1 (the port in the assembler, the reader, Blender's thin master, the Unreal driver, the rig's row; Glass_Clear re-assembled). Click 2 needs 12.2 (the exporter and the rebuilt, installed library). Click 3 needs 12.3 (Blender's solid master). Click 4 needs 12.4 (the emission pair; the library rebuilt). Click 5 needs nothing beyond 12.1 and 12.4 in the tools, and runs in 12.5 because that is where its verdict is applied. No click reaches past its step.

### In now / not now

**In now:**
- **The contract:** `LCDSchema.md` (the three ports in the Creator table; the *"emissive colour … is not a Creator control"* paragraph marked superseded; the author-tier rows note which value is now a port) · `Identity.md` (the line *"A see-through colour is its own authored article"*, marked superseded) · `Glossary.md` *Creator tier* · `Experience_MatterLibrary.md` §Shipped.
- **The tools:** the recipe schema and its validator · the assembler · the article validator · the shared reader · the Blender masters, the loader and the exporter · the rig's Unreal driver · the rig's sweep · the Asset-Browser library rebuilt and installed.
- **Every see-through and emissive article (12)** re-assembled in place with its ports (`v01` kept, pre-release).
- **The pilot re-frozen:** `matterlib-0.1.0` carries three of the 12 (Glass_Clear, Diamond_Brilliant, Neon_Signage). The maintainer's promote command is handed over at the start of the close.
- **The colour-only articles and wish-list rows marked** after click 5 (never deleted): on disk `Glass_Green`, and `LED_WarmWhite` against `LED_CoolWhite`.
- **The hand-off:** one `PlatformDependencies.md` row (the three ports join Studio's and Stage's travel ports and Studio's and USDLiveView's Creator controls), and a note on M2, whose *"emissive colour not adjustable by Creators"* this answers on the library's side.
- **The matter-generate skill's** line that a see-through colour is its own article.

**Not now:**
- **A new Unreal build.** None is needed (F-GLC-4).
- **How a renderer draws see-through matter:** the thin-walled bend and the solid master's absorption with depth are `PlatformDependencies.md` M6 and its research doc.
- **Wear layers reaching the glow** (dust dimming a light): Phase11's F-P11-9.
- **The scattered colour** (`subsurface_color`: jade, wax, skin). The same shape, not asked for; a later, additive port.
- **Emission on a master other than Emissive.** No article authors it (F-GLC-3).
- **Saved, named slider states** (*personal saved variants*, the Roadmap's parking lot). Until they exist, a green glass is a clear glass with a colour set, not a named pick.
- **Retiring or renaming any article.** Marked only.
- **A gate** for any of this: a new gate is a lead ruling, and nothing asks for one.

### Reuse check

*What does the stack already provide, and which standards does this touch?*
- **USD already exposes these values on the Material** (F-GLC-1, measured): reading a `.mtlx`, usdMtlx puts every valued shader input on the Material prim and connects the shader to it. A value on the bound Material's `inputs:transmission_color` drives Glass_Clear in a stock USD tool **today, with no change to the article**. That native behaviour is **not** taken as the carrier, for two named gaps: the contract has one place a Creator port is declared and one way it is carried (the nodegraph's interface inputs and the Carrier rule, which every reader and writer already implements); and the native exposure **stops working without a sign** the day the value is routed through the graph, as `transmission_weight`'s did under dust (its Material input is left unconnected today).
- **The route through the graph is Phase10's:** a covered weight already reaches the shader through a nodegraph output. The three ports use the same route with nothing in between.
- **The Unreal masters already carry all three as parameters** under the article's names, and render them (F-GLC-4). **Blender's masters already have the three sockets,** under their author names.
- **OpenPBR's own inputs give the names, types and ranges** (`open_pbr_surface`: colours 0 – 1; `emission_luminance` from 0 with no hard maximum).
- **Standards touched:** the LCD vocabulary (additive, the third evolution; library semver-minor, the `overlay3_density` and `overlayN_color` precedents) · the Carrier rule (unchanged) · the `determinism` lane (every other article byte-identical).

### Decisions that bind

*One authoritative copy. "Taken" = decided by the spec, a measurement or precedent in this discovery, not a lead ruling.*

- **RD-GLC-1 — Storm does not hold the rest back (the lead, 2026-10-05, in the invocation):** *"As normal, don;t hold everything else back just because of storm..."* A control that moves Blender and Unreal and not Storm is recorded as Storm's limit; it gates nothing.
- **RD-GLC-2 — A see-through or emitted colour is a Creator setting, not its own article (the lead, 2026-10-05).** It reverses the lead's ruling of 2026-09-25 (E2 and the emissive half of E8, `260925_R_LibraryCoverage_FirstRelease.md`), which the lead was shown twice in the sitting before invoking this phase. The lead's words: the thought quoted in this doc's header, then the invocation. Recorded in that research doc's own rows the same day.
- **The three ports (taken; LCDSchema: *"Names use OpenPBR-aligned terms"*):**

  | Port | Type | Affects (OpenPBR) | Op | Range / schema default | Declared by |
  |---|---|---|---|---|---|
  | `transmission_color` | color3 | `transmission_color` | set | 0 – 1 per channel / `(1, 1, 1)` | TranslucentThin · TranslucentThick |
  | `emission_color` | color3 | `emission_color` | set | 0 – 1 per channel / `(1, 1, 1)` | Emissive |
  | `emission_luminance` | float | `emission_luminance` | set | 0 and up, no maximum / `0` | Emissive |

  `LCD_PORTS` then carries 15. No existing name, type, op or range moves.
- **Carried as every Creator port is (taken; LCDSchema §Carrier rule):** a nodegraph interface input, passed to the shader through a nodegraph output, and overridden on the bound Material with the connection. Not the native exposure of F-GLC-1.
- **One place holds the value (taken; Phase10's deviation is the precedent):** the recipe's existing `transmission_color`, `emission_color` and `emission_luminance` are the port's start value. The recipe lists the port in `lcd_ports`; it does not repeat the value in `lcd_defaults`.
- **Brightness means what OpenPBR's input means (taken; Learnings MaterialX M3):** `emission_luminance` is used as radiance directly, and is the same quantity as a Blender Emission Strength. The library's lights author 12; a Creator may set any value from 0 up. Zero is allowed from the Creator; an **article** on Emissive must still start above zero.
- **`base_color_tint` stays on these articles (taken; Don't Delete Spec Functionality).** It still tints the surface colour, which shows wherever an article is not fully see-through (Glass_Clear's transmission weight is 0.95).
- **A deposit needs nothing new (taken):** dust already takes `transmission_weight` to none where it lies, so the see-through colour under it does not show. Dust does not reach the glow, as today.
- **No article is deleted or retired.** `Glass_Green`, `LED_WarmWhite` and `LED_CoolWhite` are re-assembled with their ports like the rest. After click 5 the colour-only ones are marked `Reevaluate (date)` in their recipe's comment and their wish-list row's note, with what sets the same look.

### Risk lane — `build`, controls read

- **Contract:** the same shape as Phase04's `overlay3_density` and Phase10's `overlayN_color`, both of which ran in `build`. **Read:** `assemble_mtlx.py` (`LCD_PORTS`, the interface-input loop, the shader inputs, Phase10's graph outputs) · `recipe.schema.json` (`lcd_ports` is a closed enum, so the three names must be added) · `validate_recipe.py` (its G7 rules name the pattern a new rule follows) · `validate_material.py` (it requires `transmission_color` and `emission_color` **as values on the shader**, and reads `emission_luminance`'s value there, so it must follow a port-driven input) · `blender/masters/article.py` (it reads lane-A values from the shader only) · `lcd_usd_edit.LCD_PORTS` (it rejects a value over a port's maximum, so brightness takes an open maximum) · the four copies of the travel-port list (`lcd_sparse.py`, `load_article.py`, `verify_asset_library.py`, `matter_proxy.py`).
- **What enumerates the trees this phase changes:** the pilot's freeze hashes its payload, and **3 of the 12 re-assembled articles are in it**, so a re-freeze and the maintainer's promote are scheduled. The `determinism` lane re-assembles every article, which is the guard that nothing else moved. No gate globs `docs/`.
- **`check_exporter.sh`:** runs at 12.2 (a change under `blender/addons/`), **baselined before the edit** (`LOCAL_DELTAS.md`).
- **The public edge:** none. No runtime is published (F-GLC-4). Pushing is the lead's.
- No sign-in, secret, destructive migration or data loss.

### Step list

- **12.1 — Glass takes its colour from a control.** The contract text; `transmission_color` as a port in the schema, the validators, the assembler and the reader; Blender's thin see-through master and the loader; the Unreal driver; the rig's row; Glass_Clear re-assembled. *First clickable result: click 1.*
- **12.2 — The colour travels from Blender.** The exporter and the travel-port lists; the Blender library rebuilt and installed. *Click 2.*
- **12.3 — Solid see-through matter.** Blender's solid master works its absorption out from the port, inside the master; Diamond re-assembled. *Click 3.*
- **12.4 — A light's colour and brightness.** `emission_color` and `emission_luminance` through the same places; the rig's rows on the dim view; Neon_Signage and LED_CoolWhite re-assembled; the library rebuilt. *Click 4.*
- **12.5 — Every article, and the colour-only ones judged.** The other eight re-assembled; the pilot re-frozen; click 5's sheet; the marks; the skill's line; the hand-off row. *Click 5.* Then the close.

**A split signal, surfaced early and not cut:** glass (12.1 – 12.3) and lights (12.4) can each be shown on their own. They stay one phase because they are one contract change through the same files. If execution drags, 12.4 is the cut.

### Compact build map

- **The assembler** (`tools/converters/assemble_mtlx.py`): three entries in `LCD_PORTS`. For a declared port, the interface input takes the recipe's value, a pass-through node feeds a nodegraph output, and the shader input connects to that output where it carries a value today. **Refuse** a port whose value the recipe does not author, and `transmission_color` off the see-through masters or the emission pair off Emissive. Byte-identical for every article that declares none.
- **The recipe schema and validator:** the three names in the `lcd_ports` enum; a rule beside G7 for the refusals above.
- **The article validator** (`validate_material.py`): the see-through and Emissive checks accept a shader input driven by the article's own port, and read the start value from the port.
- **The shared reader** (`blender/masters/article.py`): a shader input connected to a port's output takes the port's value as its lane-A value, so the Blender loader and the Unreal driver keep reading one thing. *(Phase10 10.1 was caught by exactly this reader dropping a graph-routed value.)*
- **Blender** (`blender/masters/build_masters.py`, `VERSION` 9): the three sockets take the port names, as every Creator port's socket does. On the solid master the absorption (σ = −ln(colour) ÷ depth, Learnings Blender B5) moves from the loader's Python into the master's nodes, so it follows the socket. `load_article.py`: the three join `TRAVEL_PORTS`, the two colours `COLOR_TRAVEL_PORTS`.
- **The exporter** (`blender/addons/imrsv_lcd_export/`): `lcd_sparse.LCD_TRAVEL_PORTS` and `_COLOR3_PORTS`; `lcd_usd_edit.LCD_PORTS`, brightness with an open maximum. Its own tests sit beside it.
- **Unreal** (`tools/parity/drivers/unreal.py` only): the three join `SLIDERS`, and the two colours the vector branch. The masters and the pinned runtime are untouched.
- **The rig** (`tools/parity/rig.py`): `SWEEP` rows for the three ports. The emission rows are judged on the dim view, which Emissive articles already get.
- **Recipes:** the port names added to `lcd_ports` of the 12, found by `grep -l -e '"transmission_color"' -e '"emission_color"' tools/converters/recipes/*.json` less `IMRSV_MissingMaterial`.
- **Docs:** as listed under §In now, plus `MasterSet.md`'s History and `JOB_FORMAT.md` if the sweep's rows are named there.
- **Test surface (the `build` ceiling):** the existing `run_all.py` lanes (the `determinism` lane is the main guard), unit tests beside the assembler's and the exporter's for a declared and an undeclared port, and **one real-path smoke: the rig sheets of the first human test.** No new gate.

### Lead calls

**RD-P12-1 — answers Q-GLC-10: this is Phase12 (the lead, 2026-10-05).** The invocation *"/execute Phase12"*, against the recommendation below. Phase11 keeps its number and its pause.

**RD-P12-2 — answers Q-P12-1: Unreal's weak colour on a solid is a follow-up, not this phase's work (the lead, 2026-10-05).** Asked: carry on to 12.4 with it recorded (A), or bring the Unreal solid master into this phase (B). The lead: *"A, keep going with 12.4"*. Click 3 stands as looked at: Blender takes the colour, Unreal shows it faintly (F-P12-1, the 12.3 row). The follow-up is on `PlatformDependencies.md` M6, the row that already holds the library's Unreal see-through masters.

**Q-GLC-10 [lead] — The phase's number.** → RD-P12-1. Phase11 (Library Coverage) holds the Active slot, paused since 2026-10-02 with its refine pass owed. The next free number is 12. *Recommendation: number this Phase12 as work starts, the lead's usual practice; Phase11 keeps its number and its pause.*

---

## Why this is a phase

One contract change carries it. The Creator vocabulary gains ports for values that are fixed on the article today, and every implementation of the article moves with it: the assembler, the Blender masters and the exporter that makes the ports travel, the rig's Unreal driver, and Studio's controls (a hand-off). It is the shape of Phase10. It is expensive to unwind for one reason: a Creator port is a public name every consumer binds to.

## Findings

*Pass 1, distilled.*

- **F-GLC-1 — USD already exposes these values on the Material, and that is not the carrier.** `usdcat --flatten` of Glass_Clear's `.mtlx` (OpenUSD 26.03, the pinned toolchain): the Material prim carries `color3f inputs:transmission_color = (0.82, 0.95, 0.88)`, and the shader's input connects to it. A shader input the graph drives is different: the Material carries `float inputs:transmission_weight` with no value and nothing reading it, and the shader connects to the nodegraph's output. So the native exposure exists only while a value sits on the shader. → §Reuse check; §Decisions that bind.
- **F-GLC-2 — The spec answers where a Creator port lives.** LCDSchema: *"Every adjustable … is a standard `inputs:<port>` value on the bound material prim, connected from the article's nodegraph interface input"*, and *"An article declares the Creator ports it uses"*. Lane A (*"authored on the shader node"*) is the author tier. A value that becomes a Creator port moves to the interface. Answers Q-GLC-1.
- **F-GLC-3 — Twelve articles, three masters, nothing outside them.** Nine recipes author `transmission_color`: six on TranslucentThin, three on TranslucentThick. Three Creator-selectable recipes author emission, all on Emissive (Neon_Signage, LED_WarmWhite, LED_CoolWhite). The fourth is the system fallback `IMRSV_MissingMaterial`, which declares no port and is not touched. No article on another master authors either. Answers Q-GLC-3.
- **F-GLC-4 — The pinned Unreal runtime already renders all three, so no new build and no Unreal machine.** `unreal/MatterRuntime/Scripts/build_masters.py` gives the see-through masters the parameter `transmission_color` and the Emissive master `emission_color` and `emission_luminance`, under the article's names, and nothing under `unreal/MatterRuntime` has changed since the source `unreal-runtime-v3` was built from (`git log e1fc83e..HEAD`: empty). The parameters are live in the pictures: the same master draws Glass_Clear grey-white and Glass_Green green (F-GLC-6's table). What blocks a moved value today is the rig's driver alone: it refuses an article whose ports it does not know, and it would send a colour port as a single number. Answers Q-GLC-4. *Not yet seen:* a moved `emission_luminance`; the parameter is multiplied inside the master, so 12.4's row is its first proof.
- **F-GLC-5 — Blender's solid master takes its colour at load time, not from a socket.** `load_article.py` turns `transmission_color` and `transmission_depth` into absorption coefficients in Python, and sets the master's Transmission Color to white. A live port needs that sum inside the master. It is the one piece of new node work in the phase, which is why the solid master has a step of its own.
- **F-GLC-6 — Storm shows the see-through colour as darkness, not as hue.** Mean colour inside the cube, the rig's stored pictures at defaults:

  | Article | Tool | R | G | B | G ÷ R |
  |---|---|---|---|---|---|
  | Glass_Clear | Storm | 163 | 155 | 161 | 0.95 |
  | Glass_Clear | Unreal | 137 | 130 | 138 | 0.94 |
  | Glass_Clear | Blender | 154 | 164 | 160 | 1.06 |
  | Glass_Green | Storm | 91 | 85 | 90 | 0.93 |
  | Glass_Green | Unreal | 92 | 106 | 88 | 1.15 |
  | Glass_Green | Blender | 79 | 107 | 74 | 1.36 |

  Storm's green glass is darker than its clear glass and no greener. The two articles also differ in roughness, transmission weight and layers, so this is an indication, not a clean test; 12.1's row is the clean one. **It disagrees with Learnings Storm S7** (*"tinted per channel by `transmission_color`"*) and agrees with Phase06 6.4 (*"it renders Glass_Green grey"*). Whichever the row shows, RD-GLC-1 applies. A correction to S7, if the row confirms this, is the close's.
- **F-GLC-7 — The pilot carries three of the twelve** (`matterlib-0.1.0.lock.yaml`: Glass_Clear, Diamond_Brilliant, Neon_Signage). Re-assembling them invalidates the freeze. Answers Q-GLC-6.
- **F-GLC-8 — What is colour-only today is small, and the list ahead is where the saving is.** On disk: `Glass_Green` against `Glass_Clear` (it also differs in roughness, 0 against 0.02, transmission weight, 1 against 0.95, and a fingerprints layer), and `LED_WarmWhite` against `LED_CoolWhite` (the emission colour is the only difference). On the wish list, 34 rows sit on the three masters (9 thin, 16 solid, 9 emissive). Which of the queued ones are colour-only (`Glass_Amber` and `Phosphor_Green` look it; `Ruby`, `Honey`, `Lava_Molten` carry their own index, depth or textures) is judged row by row at 12.5, not here. Answers Q-GLC-8.
- **F-GLC-9 — Two durable docs restate the old rule and one says the opposite of this phase.** `Identity.md`: *"A see-through colour is its own authored article"*. The matter-generate skill repeats it. `LCDSchema.md`: *"emissive COLOUR is authored on the article, and is not a Creator control … it stays an open product question"*. All three are 12.1's and 12.5's to mark, dated, with the old text kept.
- **F-GLC-10 — Lane `build`,** verified against the tree (§Risk lane). Answers Q-GLC-9.

## Seed questions — where each stands

| # | Question | Where it stands |
|---|---|---|
| Q-GLC-1 | The port names | **OpenPBR's own, on the nodegraph interface** (F-GLC-2; §Decisions that bind). |
| Q-GLC-2 | Brightness: meaning and range | **OpenPBR's input, as radiance; 0 and up** (§Decisions that bind). |
| Q-GLC-3 | Which articles declare which port | **12 articles on 3 masters** (F-GLC-3). |
| Q-GLC-4 | What the Unreal side needs | **The rig's driver only; no new build** (F-GLC-4). |
| Q-GLC-5 | Deposits | **Nothing new** (§Decisions that bind). |
| Q-GLC-6 | The pilot | **Three articles; re-freeze and promote at the close** (F-GLC-7). |
| Q-GLC-7 | The tint on these articles | **Stays** (§Decisions that bind). |
| Q-GLC-8 | The colour-only articles and rows | **Two pairs on disk; the rows judged at 12.5; marked, never deleted** (F-GLC-8). |
| Q-GLC-9 | The risk lane | **`build`, verified** (F-GLC-10). |
| Q-GLC-10 | The phase's number **[lead]** | **Phase12** (RD-P12-1). |

## Sources (pointers, not copies)

- `docs/specs/_Architecture.md` §Design principles (the LCD ruling of 2026-09-28) · `docs/specs/Contract/LCDSchema.md` (the two tiers, lane A and B, the Creator table, §Carrier rule, the emissive-colour paragraph) · `docs/specs/Ontology/Identity.md` (the Variant axis) · `docs/specs/Ontology/MasterSet.md` (the see-through and Emissive rows).
- `docs/Planning/Research/260925_R_LibraryCoverage_FirstRelease.md` (C5, E2, E8) · `261005_R_PlatformThinGlassAsks.md` · `261004_R_PlatformSetMaterialAsks.md` (SM-F5, SM-Q3: the brighter strip).
- `docs/Planning/Phases/Complete/Phase10_ColouredWearLayers.md` (the precedent: its Brief, its deviations, the reader defect of 10.1) · `Phase06_UnrealTestRuntime.md` (6.4).
- `docs/Planning/PlatformDependencies.md` (M2, M6, P20, P22).
- Learnings read: MaterialX (M3) · Blender (B3: the exporter measures against the group's interface defaults; B5) · Storm (S6, S7) · Unreal (U1, U4: emission at 0.798, restored in the master). Claude Code: no bearing.
- The probe (F-GLC-1): `source tools/usd-toolchain/activate-usd-tools.sh`, then `usdcat --flatten MatterLibrary/materials/engineered/glass/Glass_Clear_Clean_Base_s01_v01.mtlx`, and read the Material prim's `inputs:` and the shader's connections.

## Discovery Log

- **Seed (2026-10-05)** — the lead's invocation; the Outcome, nine seed questions and RD-GLC-1 (`a8cc1b7`).
- **Pass 1 (2026-10-05)** — the specs read top-down against the Outcome, then the assembler, the validators, the reader, both sets of masters, the exporter, the rig and its Unreal driver, the pilot's lock and the wish list. One probe (F-GLC-1). All nine seed questions answered without a lead call; the reversal recorded upstream (RD-GLC-2); the Brief written.

## Discovery Status

- **Passes captured:** 1 (2026-10-05). **The Brief is complete**; lane `build`.
- **Current working direction:** three *set* ports under OpenPBR's names, carried as every Creator port is; five steps, glass first; no Unreal build.
- **Open decisions:** none. Q-GLC-10 was ruled at the start of execution (RD-P12-1).
- **Checks to carry forward:** Storm's row at 12.1 (hue or darkness: F-GLC-6, and Learnings Storm S7 if it needs correcting) · a moved `emission_luminance` in Unreal at 12.4 (F-GLC-4) · the U4 emission scale still applied when brightness is a port (12.4) · `check_exporter.sh` baselined before 12.2.

## Execution Log

**Resume (end of run 2, 2026-10-05; 12.1 ✅ · 12.2 ✅ · 12.3 closed by ruling · 12.4 ✅; stopped at the step boundary with the session at about 350k of context):**
- **Next: 12.5, the last step.** This machine; no Unreal machine is needed anywhere in the phase (F-GLC-4).
- **12.5:** the other eight articles re-assembled with their ports (four thin, two solid, LED_WarmWhite, and Glass_Green) and the library rebuilt · the pilot re-frozen (the promote command handed to the lead at the start of the close) · click 5's sheet · the marks on the colour-only articles and wish-list rows · the matter-generate skill's line · the hand-off row.
- **Another session is working in this tree** (seen 2026-10-05: a merge of the remote, a research pass and a ledger quick-fix landed between this run's commits, and it edited `PlatformDependencies.md` around this run's uncommitted M6 text without taking it). Check `git log` and the index before every commit. **It also changed the Unreal master builder** (`unreal/MatterRuntime/Scripts/build_masters.py`, `a66377c`, built and not run), so F-GLC-4's *"nothing under `unreal/MatterRuntime` has changed since the pinned runtime's source"* is now dated: the pinned runtime `unreal-runtime-v3` the rig renders with is unchanged, the source beside it is not.
- **A scene for the lead in Blender is built from Blender's FACTORY scene into its own file and that file opened; never `blender --python <script>` bare.** The lead's startup scene is a large personal project, and a bare launch loads it (run 2 did that once; nothing was saved, the window was closed, the files' times were unchanged). The two scripts of click 2 carry the guard: build headless with `--factory-startup` and refuse any scene that is not Cube, Light, Camera; the view script acts only in the file it was written for.
- **State:** every commit is on `main` and **unpushed** (the push is the lead's). Gate: `release_verify` red, predicted, until 12.5's re-freeze; everything else as the baseline.
- **Carried checks:** Unreal's lit level by colour (F-P12-2, the 12.4 row: a home for it at 12.5's hand-off, and Learnings Unreal U4 at the close) · Learnings Storm S7's correction on hue (the close) · Unreal's solid master tints a solid flat and does not deepen with depth, so the two green rows read differently from Blender's (12.3's row; Not-now, `PlatformDependencies.md` M6) · the rig turns a hyphen in a row's label into `m` in the picture's file name (cosmetic).

**Run 1 (2026-10-05, the library machine; the lead present).** Tree at the start: `main` at `3fac681`, clean, two commits ahead of the remote, no other session. **Gate baseline before any code change** (`run_all.py`): 17 lanes, 15 PASS, 2 SKIP (compression, staging), 0 FAIL.

**Corrected facts (the Brief):**
- **The article validator needed no change for the see-through colour.** Its check is that the shader *has* the input, which a port-driven input satisfies. The Emissive check reads `emission_luminance`'s *value* on the shader, so 12.4 still owes that edit.
- **F-GLC-6 is confirmed by the clean test** (click 1's row, one article, one value moved): Storm takes the see-through colour as darkness and shows no hue. Learnings Storm S7's *"tinted per channel"* is wrong on hue; its correction is the close's.

| Step | Commit | Result | Next |
|---|---|---|---|
| 12.1 | `fe1e16e` | ✅ **Click 1, the lead (2026-10-05), on Glass_Clear's defaults row above its *see-through green* row (Storm, Blender, Unreal; whole set and close-up):** *"pass on 1, write the handoff for 12.2"*. Built: the Creator port `transmission_color` (`LCD_PORTS`, 13; `SET_PORTS` names the field that holds its start value and the masters that may declare it); the assembler passes a declared port to the shader through a pass-through node and a nodegraph output; the recipe schema, a G7 rule and the RED fixture `set_port_wrong_master.json`; the shared reader; Blender masters v9 (the socket takes the port's name) and the loader's travel ports; the Unreal driver (`unreal-runtime-v3` untouched); the rig's row; LCDSchema, Identity, Glossary. Glass_Clear re-assembled in place: three lines differ (the interface input, the pass-through and its output, the shader's connection). **Rig, Glass_Clear, the row *see-through green*, moved Storm / Blender / Unreal:** whole set 11.4 / 18.3 / 20.0, close-up 14.8 / 20.3 / 20.3, *moved alike*. Looked at: green in Blender and Unreal, the wall still seen through; Storm darker and grey. Unreal against Blender on that row: 7.2 (9.8 close-up), nearer than at defaults (12.0). **Gate:** 14 PASS, 2 SKIP, 1 FAIL `release_verify`, the predicted one (Glass_Clear is in the pilot; the re-freeze is 12.5); the new fixture is rejected by G7; `determinism` PASS. | 12.2 |
| 12.2 | `ddba448` | ✅ **Click 2, the lead (2026-10-05), in Blender on Glass_Clear from the installed library on the factory default cube, the grid wall behind, the `transmission_color` swatch under the Material tab's Surface:** *"pass on 2, keep going with 12.3"*. *(Read from that window after the verdict, the swatch was back at the article's own colour, so the export taken from it carried 0 overrides, the sparse case. The amber value in the USD is the agent's own run, below.)* Run 2 (2026-10-05; tree `main` at `6c288e1`, clean, no other session). Built: `transmission_color` in the exporter's travel ports and its range table, and in the library verifier's copy; a case for it in each of the exporter's two test files; the Asset-Browser library rebuilt in place (88 articles, structure conforms; Glass_Clear's group exposes the swatch); Experience §Shipped. **Machine half of click 2, run by the agent on Glass_Clear appended from the installed library onto the default cube:** untouched, the export carries 0 overrides; set to amber, it carries `color3f inputs:transmission_color = (1, 0.6, 0.1)` on the Material, connected from `NG_Glass_Clear_Clean_Base_s01_v01`, and the flattened stage runs Material input → nodegraph input → pass-through → nodegraph output → the shader's `transmission_color`. **`check_exporter.sh`:** the red set is the same before and after the edit, five carrier checks that all stop at one import (`check_lcd_carrier.py` loads the assembler under a Python with no MaterialX); every export, profile, binding and selection check passes. **Gate:** 14 PASS, 2 SKIP, 1 FAIL `release_verify`, the predicted one. **Corrected facts:** `matter_proxy.py`'s port list is not live (retired, nothing imports it, and it never took Phase10's colour ports), so it is left as it is · the lead's Blender reads `blender/asset_library/` as an asset library with Append, so the rebuild in place is the install · the export add-on is **not enabled** in the lead's Blender preferences (measured from the preferences, 2026-10-05); the agent's exports load it from the repo. | 12.3 |
| 12.3 | `0258799` | **Closed by the lead's ruling RD-P12-2 (*"A, keep going with 12.4"*), not by a pass of the Unreal column: Blender takes the colour; Unreal's weak colour on a solid is followed up on `PlatformDependencies.md` M6.** **The lead (2026-10-05), on Diamond's two green rows:** *"Blender is much more noticable than UE... hard to tell if UE is coloring at all"*. **F-P12-1 — in Unreal a solid shows its see-through colour faintly and does not deepen it with thickness.** Unreal's close-up under the pale green is all but its defaults picture (moved 5.4, Blender 25.6); under the bottle green it is a muted green wash (16.8, Blender 19.4, near black). It is older than this phase: at its own values Diamond's blue fills the stone in Blender and does not show in Unreal (the same in the stored pictures of 2026-10-02). The library's Unreal master does pass `transmission_color` and `transmission_depth` to Epic's function (`unreal/MatterRuntime/Scripts/build_masters.py`); why the picture does not follow the depth is **not measured** (no engine source read, no depth probe run). A repair is in the Unreal master, so a new runtime build on the machine with Unreal, which the Brief put out of scope. **Q-P12-1 [lead]:** carry on to 12.4 with this recorded as a follow-up, or bring the Unreal solid master into this phase. Built: Blender masters v10, where `ML_TranslucentThick` works its absorption out inside the group from the `transmission_color` socket and a new `Transmission Depth` socket (σ = −ln(colour) ÷ depth; the surface stays untinted), and the loader no longer sums it; Diamond re-assembled in place with the port (the same three changes as Glass_Clear); a second sweep row for solid matter only, *see-through pale green*; MasterSet's History, LCDSchema's note, Experience §Shipped. **The master change moves nothing at the article's own values:** Diamond's Blender pictures before and after differ by at most 1 code value (whole set, close-up, roughness +0.5), and a control pair differs, so the comparison can fail. **Rig, Diamond, moved Storm / Blender / Unreal:** *see-through green* whole set 7.1 / 19.1 / 15.6, close-up 7.7 / 19.4 / 16.8 (UNEVEN, Storm the one behind: RD-GLC-1); *see-through pale green* 5.0 / 20.1 / 4.1, close-up 5.6 / 25.6 / 5.4 (ONE-SIDED). **Looked at:** under the bottle green Blender's stone goes near black and Unreal's goes green; under the pale green Blender's body goes green and deepens with thickness, and Unreal's barely moves. Both follow from one fact: the rig's 0.30 m cube is 15 of Diamond's 2 cm depths across, Blender absorbs with depth as OpenPBR says, and the library's Unreal solid master tints flat (Not-now: `PlatformDependencies.md` M6). **Gate:** 14 PASS, 2 SKIP, 1 FAIL `release_verify`, the predicted one; `determinism` PASS. The committed library `.blend` is stale again until 12.4 rebuilds it (masters v9, Diamond without the port). | 12.4 |
| 12.4 | `a77586a` | ✅ **Click 4, the lead (2026-10-05), asked for two looks: (1) LED_CoolWhite's sheet, the dim strip of the rows *emission warm*, *brightness half* and *brightness up a quarter*, all three columns moving together; (2) Blender, LED_CoolWhite from the installed library on the factory cube in a dim room, dragging `emission_luminance`:** *"1) Matches 2)yep"*. Built: the Creator ports `emission_color` and `emission_luminance` (`LCD_PORTS` 15; two `SET_PORTS` rows, Emissive only; the assembler refuses a declared set port whose shader input the article never authors); the recipe schema; the article validator reads an Emissive article's starting brightness from its port; Blender masters v11 (the two sockets take the port names) and the loader's travel ports; the exporter (brightness from 0 with no maximum, only a negative rejected) and the library verifier's list, a case in each exporter test file; the Unreal driver; the rig's rows; Neon_Signage and LED_CoolWhite re-assembled in place; the library rebuilt in place (88 articles, conforms); LCDSchema (the two rows, the *"not a Creator control"* paragraph superseded and kept), Glossary, MasterSet, Experience. **The change moves nothing at the article's own values:** LED_CoolWhite's lit level is the same in all three tools before and after, to the 8-bit digit. **Rig, LED_CoolWhite, the dim view, moved Storm / Blender / Unreal:** *emission warm* 25.3 / 25.5 / 23.0, *brightness half* 14.2 / 14.2 / 13.8, *brightness up a quarter* 4.7 / 4.8 / 4.6, each *moved alike*. **Deviation, the brighter row:** the Brief's *brightness double* cannot be read on the dim view, where 16 is display white: at 24 every tool clips to the same white (measured 5.4 / 5.6 / 12.0, a false "uneven"), so the row is 15, a quarter up. **Carried checks answered:** Unreal follows a moved brightness in proportion (lit cube, linear: 0.31 at 6, 0.58 at 12, 0.71 at 15), so the master's correction reaches a Creator's value as it does the article's. **F-P12-2 — Unreal's lit level depends on the light's colour, and is older than this phase:** against Storm and Blender (0.78 at 12) Unreal's white LED reads 0.58, about a quarter darker, and the warm colour reads about an eighth brighter (red 0.885 against 0.786); the pictures from before this step are identical. The correction of Learnings Unreal U4 (÷ 0.798) was measured on Neon's magenta alone; why the level follows the hue is not measured. **Machine half of click 4, run by the agent on LED_CoolWhite from the installed library:** untouched, 0 overrides; warm and doubled, `color3f inputs:emission_color` and `float inputs:emission_luminance = 24.0`, both connected from the article's nodegraph; a brightness of 0 exports. **`check_exporter.sh`:** the same red set as 12.2's. **Gate:** 14 PASS, 2 SKIP, 1 FAIL `release_verify`, the predicted one; `determinism` PASS. | 12.5 |
