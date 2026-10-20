# Phase21 — Skin Maps

**Status:** IN EXECUTION (2026-10-20, `/execute P21`; at `a8d2787`, on the library machine). *Was:* BRIEF READY — the lead answered Q-P21-1 with *"a,"* (RD-P21-6): colour only. *Before that:* IN DISCOVERY, the Brief written with one lead question open. Opened by the lead's *"push, then /discovery Skin Maps"*. **Numbered Phase21 by the agent** as discovery opened, because it was the head of `## Future` (RD-SV-1), as Phases 13–20 were numbered. Renumbering is the lead's, and it is free until execute commits ids. Seeded 2026-10-14 by `/research` (*"Seed all the TBD phases we discovered here"*). Before this date, the stub was `Phases/Future/PhaseTBD_SkinMaps.md`.
**Lane:** `build` (§Risk lane). **Next:** `/execute P21`.
**Measured at:** `b2abdb5`, on the library machine (no engine at `unreal/build.sh`'s `UE`; Blender 5.2; an 8 GB GPU).

## Outcome

**A character's skin varies across the body as real skin does,** with lips that blend into the face and redder cheeks and knuckles, in Blender, a USD viewer and Unreal. **Every character built from the approved human mesh wears it.**

*(Verbatim from the seed. It does not promise that skin stops reading as plastic: F-P21-1 measures that a colour map alone does not reach the even sheen, and RD-P21-6 keeps the roughness map out of this phase. Click 1 asks the lead whether it still reads as plastic.)*

---

## The Brief

### What this phase builds, in one paragraph

The six Fitzpatrick skin articles become **fitted** Character articles. Each carries a colour map the library makes for its tone, on `MakeHuman_Body_v01` (hm08), and declares `fits`. The six lips articles carry the same tone's map, so the colour runs across the lip edge. The map is built from CC0 parts only (RD-SKM-2, RD-SKM-5). It is held so that its average is the measured tone, and stored as the multiplier the contract already reads (`base_color_map`, RD-SKM-3). The skin's scatter colour follows the map, and **the Creator's tint, inert on skin in every tool today (F-P21-3), starts working**. That needs two small master fixes: Blender's refusal (F-SKM-23) and Unreal's untinted scatter. **No contract changes:** every input exists, and Phase18 built the fitted-article rule, the part mesh, `fits` and G8 for this phase.

### First human test

**Where:** the library machine. The lead's Blender, on a scene built headless from the factory scene into its own file and opened detached (Blender B10–B11, ClaudeCode CC2), plus the rig's sheet and the thumbnail sheet, opened with `xdg-open`. Each path goes in the handback. **The agent drives every tool; the lead looks and judges.** Skin is judged on the character with a close camera, never on a colour sheet (`LOCAL_DELTAS.md`).

1. **One tone on the character (21.1).** In the lead's Blender: the clothed MakeHuman character in Fitzpatrick IV and its lips, a close camera on the face and a second on the back of the hand, beside the same character as it is today (a copy, side by side).
   - *Judge:*
     - the lips blend into the face, with no line of colour **and no line of shine** at the lip edge (RD-P21-2's premise);
     - the cheeks, ears, nose and knuckles are warmer, and the eye sockets slightly darker;
     - the skin's overall tone is today's tone;
     - **does it still read as plastic?** If it does, your words are the evidence to un-park *Skin Maps Beyond Colour* next, roughness first (RD-P21-6).
   - **Optional, on the lead's ask at the sitting: the scatter amount as a diagnostic.** The same skin at half and at double its scatter distance (`subsurface_radius`), beside it, in probe copies that are never committed. It shows whether the doll look is too much scatter, too little, or neither (F-P21-1 points at the shine). The lead, 2026-10-20: *"I thought maybe playing with the SSS might help see if the plastic / rubber / doll effet was too much or not enough SSS"*.
   - **The surface can show it:** Cycles at the probe's face framing gives the face about a 441-pixel square of map (F-SKM-26). The lips' edge fills a good part of the frame. The fixture is the rig's own character, the mesh the platform builds from (F-SKM-8).
2. **The tint works (21.1).** In the same scene, the agent sets the skin's tint to a strong colour and back.
   - *Judge:* the skin takes the tint. Today it does not, in any tool (F-P21-3).
3. **Six tones, three tools (21.2).** The rig's sheet, with `face` and `hand` for Fitzpatrick I to VI, each with today's beside it, in Storm (USDLiveView's renderer), Blender and Unreal.
   - *Judge:* every tone reads as its own tone, and the three tools move alike.
   - **The agent's evidence, in the 21.2 log:** each map's average against its measured tone (within 2 % per channel), G8 on every map, and the rig's verdict.
   - **Waived, said now (`discovery.md`): the USD viewer is judged on the rig's Storm column, not in USDLiveView.** No composition with the character exists in this repo, and the platform's are private. USDLiveView renders with Storm.
4. **Pictured (21.3).** The thumbnail sheet: the six skins' `face` and `hand` thumbnails and the six lips' `lips` thumbnails, beside today's.
   - *Judge:* skin you would pick from a card.

**Reconciled click by click:**
- Clicks 1 and 2 need 21.1 only: one tone's map, the skin and lips articles, Blender's fix, the rig's body on the atlas.
- Click 3 needs 21.2.
- Click 4 needs 21.3.

Every tool runs on the library machine: Blender, Storm, and Unreal from the pinned `unreal-runtime-v5`, fetched to this machine 2026-10-20.

**Not a click: the tint in Unreal.** 21.1 builds Unreal's fix, but it is not run here (`LOCAL_DELTAS.md` §Two machines). At its defaults (a white tint) the master draws as before, so **no runtime is owed** (the lead, 2026-10-05). The rig's `tint` row stays one-sided in Unreal until a runtime is built on the machine with Unreal (§Deferred).

**Not a click: Studio.** Studio draws a fitted article's own picture when its binding supplies none (P28; `Eye_Green` and `Teeth_Natural` today). It pairs lips and nails by name (R-PCE-2). So the skins reach Studio with **no Studio change** once its dev install is re-served. Seeing it there is the platform's sitting, recorded in a ledger row (21.3).

### In now

| Item | Step |
|---|---|
| The skin-map maker: the probe's recipe as a tool (MPFB2's CC0 region masks and `sss.png`, an AO bake, 3D noise, cheeks placed from the face), writing one map per tone with provenance | 21.1 (IV), 21.2 (all six) |
| The calibration (RD-P21-3): the map's average over the skin, lips excluded, is the article's measured tone; stored as a multiplier with brightest ≈ 1, and the article's `base_color_const` raised by the same factor. The fit converter does it, so a contributor hands in a colour picture (the spec's step 3) | 21.1 |
| The six skins re-assembled as fitted articles (RD-P21-1): `base_color_map` with the tone's picture, `fits: MakeHuman_Body_v01`, the scatter colour following the base (the constant dropped), the tint port kept, still `s001` (the pores), `v01` rebuilt in place | 21.1 (IV), 21.2 |
| The six lips (`Lips_FitzpatrickI`…`VI`) carry their tone's map with the lip finish (RD-P21-2) | 21.1 (IV), 21.2 |
| Blender: a tinted base's scatter colour follows the tint (`blender/masters/load_article.py`'s refusal lifted, F-SKM-23) | 21.1 |
| Unreal: the scatter colour carries the tint (`build_masters.py`), built and not run here (no runtime owed at defaults) | 21.1 |
| The rig's body, lips and nails on hm08's atlas UVs when the skin is fitted, with the pores' `uv_scale` from the measured density (the probe's patch, made real, F-SKM-27) | 21.1 |
| The skins' and lips' thumbnails re-made | 21.3 |
| The dev install re-served; a dev snapshot at the lead's word | 21.3 |
| The specs: `SkinMaps.md` from draft to in force (its *Proposed* and *Open* marks settled), the Glossary's *Skin map* row (still says "fit-set picture supplied when bound", F-P21-5), the spec's stale CC BY line (F-P21-6), and LCDSchema's note that a skin map is calibrated to its tone | 21.3 |
| Ledger: a row telling the platform what changed (skins and lips carry their own picture; the tint needs the masters rebuilt, M7). Q-PMU-1, Q-PMU-2 and Q-PMU-4 answered there | 21.3 |

### Not now

- **Maps beyond colour** (normal, roughness, cavity, scatter): *Skin Maps Beyond Colour*, parked (RD-DS-8; kept parked by RD-P21-6).
- **The AI fine-detail layer** (RD-SKM-5): later, on the library service's GPU.
- **A larger face map, or a face map of its own** (F-SKM-26): the 2048² atlas stays (decided below).
- **`Lips_Natural` and `Nail_Natural`:** no `Skin_Natural` exists to share a map with them. **The nails** wear no map (the spec: *"not the map's job"*).
- **Studio's side:** the platform's, through the ledger.
- **A release:** *Release Bundle*.
- **A Creator scatter control in Studio** (asked by the lead, 2026-10-20, *"could we or should we add a SSS slider to Studio and make part of the LCD controls?"*; *"nah... all good"* after the answer).
  - **Could:** an additive Creator port, as Phase12's were. That is a lead ruling on the frozen vocabulary, and a phase of its own.
  - **Not now, for three reasons:**
    - F-P21-1 puts the plastic in the shine, not the scatter;
    - Storm's subsurface is a per-pixel approximation (F-SKM-18) and ignores anisotropy (Storm S8), so the control might not move all three tools alike. That is unmeasured;
    - on skin, scatter is physical, not a style choice.
  - **Where it would earn its place:** jade, marble, wax and onyx (the `NephriteJade` redo asks for *"more translucency"*), as a multiplier on the scatter distance. A rig probe would test parity first.

### The reuse check

*What does the stack already provide, and which contracts are touched?*
- **The input:** `base_color_map` on Subsurface, in every target since Phase09. It samples texcoord 0 directly, not through `place2d` (LCDSchema §Base colour map), so the map rides the atlas while the pores keep their 1 cm tile through `uv_scale`. Proven in all three tools by the probe (F-SKM-22, F-SKM-27).
- **The fitted article:** Phase18 built it for this phase (RD-P18-10).
  - `fits` in the recipe and `imrsv_metadata`.
  - The assembler writes the picture as `base_color_map`'s value.
  - The part mesh `MakeHuman_Body_v01`, whose parts are `skin`, `mouth` and `nails`, so the Lips may carry it.
  - G8 refuses a wrong size, a wrong format or a bare UV island, and G9 lets the skins keep `s001` (`validate_recipe.py`, read 2026-10-20).
- **The scatter colour following the picture:** the assembler's F-P09-5 branch connects `subsurface_color` to `base_color_out`, which is after the tint, so Storm already follows a tint. Unreal's driver multiplies the scatter parameter by the picture, with the U11 floor (`build_masters.py`). **The gap** is the tint, in Blender and Unreal only (F-P21-3).
- **The map's recipe:** the probe (`261014_R_SkinMaps_probe.py`, 301 lines, committed). The sources are pinned and CC0: MPFB2's masks and `sss.png`, blob-pinned in the probe.
- **The rig's character** already keeps atlas UVs for a mesh marked `atlas` (the fitted teeth, `build_character.py`).
- **The thumbnails' `face`, `hand` and `lips` views** exist (Phase17, Phase18).
- **Consumers:** the platform draws an article's own picture (P28) and pairs by name (R-PCE-2).
- **Contracts touched:** none changed. LCDSchema gains a dated note: a skin map's average is its tone.
- **New code:** the map maker and its calibration; one branch each in Blender's and Unreal's masters; the rig's atlas switch for the body. **Nothing replaces a native behaviour.**

### Decisions that bind

*One authoritative copy. Research rulings quoted where they are the authority.*
- **RD-SKM-1:** skin maps are made per mesh version; today's is hm08 (`MakeHuman_Body_v01`, RD-P18-1). *"it is more about locking mesh then it is about materials"*.
- **RD-SKM-2 and RD-SKM-5:** the map is library-made, never MakeHuman's photo atlases. AI joins later, only as a tone-free detail layer.
- **RD-SKM-3:** one colour map per tone, carrying hue, through `base_color_map`, with no new input.
- **RD-SKM-4:** plain skin at the genitals and groin; the areolae keep their natural variation.
- **RD-SKM-6:** a spec contributors can work from. 21.3 takes `SkinMaps.md` out of draft.
- **RD-P18-9:** a fitted Character picture lives inside its article. **RD-P18-10:** this phase builds on Phase18's registry, kit, rule, check and picture binding.
- **RD-DS-8:** *"skin detail stay parked TBD"*. Maps beyond colour stay in their own parked phase (RD-P21-6).
- **RD-AFT-3** (the lead, 2026-10-20, *"3 yes"*): this discovery carries Q-PMU-4 (*"still plastic"*) as its own question. → F-P21-1, RD-P21-6.
- **RD-RO-2:** *"material are CC0"*. The maps are CC0.
- **Pre-release, no versioning** (`AI_WorkingAgreement.md` §Settled practices): the twelve articles are rebuilt in place at `v01`. **None is in a frozen release** (`library/releases/*.lock.yaml`, grepped 2026-10-20), so no release lane moves.
- **RD-P21-1 — One article carries both the tone and its map** *(closes the spec's Open, unless the lead says otherwise)*. The six `Skin_Fitzpatrick*` are re-assembled in place.
  - **Why:** RD-SKM-1 means every human body is the approved mesh, so a tone-only twin would offer the look the lead called *"pretty terrible in fact"*.
  - Twelve skins would double what Studio and the website list.
  - The platform's pairing by name (R-PCE-2) keeps working unchanged.
  - **Kept, not lost:** using the tone on another mesh. A binding that supplies a white picture wins (the Carrier rule), so a consumer can still bind the tone alone. The spec says so in 21.3.
- **RD-P21-2 — The lips carry their tone's map with the lip finish** *(the platform's second form, Q-PMU-2; unless the lead says otherwise)*.
  - `Lips_Fitzpatrick*` declare the same picture and `fits`, and take the skin's calibrated `base_color_const`, so the colour is continuous across the part edge. They keep their own roughness and coat.
  - **Why over the seed's "the lips wear the skin article" (F-SKM-9):** the lips keep their shine, and Studio's pairing, which puts `Lips_<Tone>` on the lips, needs no change.
  - **Its premise is click 1** (no line of shine at the edge). **The fallback, if it shows a line:** the lips wear the skin article. That makes the pairing rule a platform ask (R-PCE-2 changes), so it would be put to the lead, not taken.
- **RD-P21-3 — Calibrate by raising the article, not by a map above 1** (F-SKM-20's first way out).
  - The stored map is the colour picture divided by the tone and scaled so its brightest is 1, as LCDSchema already says. The article's `base_color_const` rises by that factor, so the average renders the measured tone.
  - **Why:** the second way (a map normalised to its mean) needs a picture format that holds values above 1, which is a contract change.
  - `fuzz_color` is pinned to the tone today, and is re-pinned to the calibrated average.
- **RD-P21-4 — The tint is fixed, not dropped.** Dropping the port would delete a shipped Creator control (the project's HARD RULE). Fixing it makes the control work for the first time (F-P21-3).
- **RD-P21-6 — Colour only; the roughness map waits for its own phase** (the lead, 2026-10-20: *"a,"*, answering Q-P21-1). RD-DS-8 holds. Click 1 asks whether skin still reads as plastic, and a yes is the evidence to un-park *Skin Maps Beyond Colour*, roughness first. The platform's *"still plastic"* (Q-PMU-4) is answered in part here, by the variation, and the ledger row says so (21.3).
- **RD-P21-5 — The atlas stays 2048²** (MakeHuman's, the probe's; G8 already checks the Body at 2048). A face map of its own is a later question on the same mesh version (F-SKM-26).

### Risk lane — `build`

The controls this phase touches, each read:
- **The recipe gate** (`validate_recipe.py`, read): G8 checks each map against `MakeHuman_Body_v01` (size, RGB PNG, every UV island covered); G9 keeps `s001`. **The maps must leave no Body island bare**, nails and inner-mouth islands included, which the probe's 16-pixel bleed met.
- **`run_all.py`:** `determinism` re-assembles every article byte-identically, so the twelve are re-assembled by the tool, never edited by hand. `provenance_gate` covers every texture under `MatterLibrary/textures/`, so a `library/provenance/sources/fit/makehuman/skin.yaml` beside `eyes.yaml`, `hair.yaml` and `teeth.yaml` is owed. **Release lanes:** none of the twelve is in a frozen lock. Baseline at the start of execute: 18 lanes, 16 PASS, 2 SKIP, 0 FAIL (2026-10-20, Phase20's close).
- **`blender/masters/load_article.py`:** a master loader, not `blender/addons/`, so no `check_exporter.sh` baseline is owed (`LOCAL_DELTAS.md`, the RUN row). The installed Asset-Browser library is regenerated for click 1's Blender.
- **`unreal/MatterRuntime/Scripts/build_masters.py`:** built and not run here. Defaults are unchanged (tint white), so no runtime is owed (the lead, 2026-10-05). Its commit adds no *runtime owed* line, and §Deferred names the one wanted.
- **The rig's character** (`tools/parity/scene/build_character.py`): the body's UVs become the atlas when its skin is fitted. Every Character job and the scale view (Phase19) read that mesh, so the scale view's body grid is re-checked at 21.1.
- **Publication:** a dev snapshot, practised ten times, at the lead's word. **Data:** nothing is deleted. The probe's scratch stays git-ignored.
- **Content:** the full-body map is neutral at the groin by construction (RD-SKM-4), and thumbnails show only the face, hand and lips (RD-MP-3).

### Step list

- **21.1 — One tone, end to end: Fitzpatrick IV's skin and lips on the character, with the tint working.** The map maker and its calibration, one map, two articles re-assembled, Blender's and Unreal's tint fixes, the rig's atlas switch. **Clicks 1–2.**
- **21.2 — All six tones:** the other five maps, skins and lips; the rig's sheet over six tones; the averages measured. **Click 3.**
- **21.3 — Pictured, served, written down:** the twelve thumbnails, the dev install re-served, the specs and Glossary, the ledger row; a dev snapshot at the lead's word. **Click 4.**

### Compact build map

- **21.1:**
  - **The maker:** a fit converter beside `tools/converters/fit/gen_fit_makehuman.py`, from the probe's `maps` step (Blender headless: the AO bake and 3D noise on hm08, the masks and `sss.png` from the pinned MPFB2 pack). It writes `MatterLibrary/textures/fit/makehuman/skin/Fitzpatrick<Tone>_basecolor_sUKN.png` (the spec's path) and the factor `k`. Its provenance goes in `library/provenance/sources/fit/makehuman/skin.yaml`.
  - **The calibration** lives in the maker, and takes a contributor's colour picture too.
  - **Recipes:** `tools/converters/recipes/Skin_FitzpatrickIV_*.json` and `Lips_FitzpatrickIV_*.json` (`base_color_map: true`, `base_color_map_tex`, `fits`; drop `subsurface_color`; `base_color_const` × `k`). Then assemble (`build_proof_subset.py`).
  - **Blender:** `blender/masters/load_article.py` (the refusal, around *"a subsurface colour following a TINTED base"*): feed Subsurface Color the tinted base.
  - **Unreal:** `build_masters.py`'s `subsurface_color` branch: × `base_color_tint`.
  - **The rig:** `build_character.py`, `atlas` for the Body mesh's parts when the skin is fitted, with `uv_scale` from the measured density (0.01 ÷ 1.534 in the probe).
  - **Smoke:** `uv run tools/parity/rig.py --character Skin_FitzpatrickIV_Clean_Base_s001_v01`.
- **21.2:** the same per tone, then `rig.py --character` per tone and one sheet.
- **21.3:** `tools/thumbnails/` for the twelve; `serve_to_stage.py`; `docs/specs/Authoring/SkinMaps.md`, `docs/specs/Contract/LCDSchema.md` (a dated note), `docs/Glossary.md`; `docs/Planning/PlatformDependencies.md`; `build_snapshot.py --publish` at the lead's word.
- **Test ceiling (build):** existing tests, units for the calibration (the average holds, brightest ≈ 1), and the one real-path smoke (the rig on the character). No new gate or lane.

### Open for the lead

*Nothing open (2026-10-20).*

- ~~**Q-P21-1**~~ → **RD-P21-6 (the lead, *"a,"*): (a), colour only.** *As asked:* **Q-P21-1 — Skin will very likely still read as plastic after this phase. Does this phase also take a roughness map, or does that wait for its own phase?** *(RD-AFT-3 asked where the plastic lies. Measured in F-P21-1: in the sheen, not the colour.)*
  - **(a) Colour only, as seeded (recommended).** RD-DS-8 holds. Click 1 asks you, on the character, whether it still reads as plastic. If it does, that is the evidence to un-park *Skin Maps Beyond Colour* next, with its roughness map first.
    - The cost: the platform's *"still plastic"* is likely answered only partly here, by the variation.
    - The gain: this phase stays on one machine with no contract change.
  - **(b) Pull the roughness map in** (Beyond Colour's item 2: an oilier forehead and nose, drier cheeks).
    - It needs a new mesh-supplied input on Subsurface, in LCDSchema, the assembler, Blender and Unreal.
    - **The Unreal master's defaults change, so a new runtime is owed from the machine with Unreal** (two machines), and the platform must carry a second picture (a ledger ask, as P21 was).
    - It roughly doubles the phase.

---

## Findings (discovery Pass 1, 2026-10-20)

- **F-P21-1 — Where the plastic lies (RD-AFT-3), measured.**
  - **What was run:** today's `Skin_FitzpatrickIV` on the rig's character on `unreal-runtime-v5` (scratch `library/parity/P21_Plastic_SkinIV_v5/`, 37 s, all three tools at once).
  - **What it shows:** **Storm and Unreal draw the face smooth and waxy under one even sheen, and Blender shows slightly more mid-scale bumps.**
  - **What it measures:** fine-scale contrast (luminance minus a 3-pixel blur, the standard deviation over forehead, cheek and neck patches) is under 2 grey levels in every tool: Storm 0.45–0.66, Blender 0.83–1.57, Unreal 0.41–1.06.
  - **So it is the article, not one renderer, and not the half-float UVs** (v5 fixed those, Issue #5).
  - **Three causes, read from the article:**
    - the colour is one tone, which the map fixes;
    - `Skin_Pores`' roughness picture spans only 0.46–0.56 around 0.5, under a uniform coat (0.1 at a fixed 0.3), so the sheen is even;
    - the pores' 1 cm tile at 1024 px is finer than a pixel at the face view, so their relief averages away. That is correct physics: pores read only up close.
  - **What reads at face distance** is regional variation in colour (this phase) and in shine (a roughness map: *Beyond Colour*). → RD-P21-6.
- **F-P21-2 — The platform's Roughness control "moves nothing visible" on skin, and the rig agrees it moves little.** The Skin III sweep (2026-10-01): roughness −0.5 moved 0.6–1.4 ΔE and +0.5 moved 0.4–0.9 ΔE, *moved alike* in all three, but small. Q-PMU-4's *"no change I can see"* is measured, not a consumer fault.
- **F-P21-3 — The Creator's tint on skin is inert in every tool today.** In the same sweep, *tint blue* scored **"no change in any tool"** (Storm 0.00, Blender 0.00, Unreal 0.13 ΔE).
  - **Why:** each skin pins `subsurface_color` to its tone at `subsurface_weight` 1.0, and OpenPBR mixes the (tinted) base fully toward that constant (Learnings M4).
  - Re-assembly with the scatter colour following the base makes it work in Storm (`base_color_out` is after the tint). Blender refuses it (F-SKM-23), and Unreal multiplies the untinted parameter by the picture (`build_masters.py`). → RD-P21-4.
- **F-P21-4 — The rig's body carries UVs in metres, not hm08's atlas** (`build_character.py`: *"st in METRES"*). A fitted skin needs the atlas there, as the probe patched at runtime. The `atlas` flag already exists per mesh (the fitted teeth). The platform keeps the atlas and scales the pores per mesh (P18's stopgap), so it needs nothing.
- **F-P21-5 — The Glossary's *Skin map* row is stale.** It says *"a fit-set picture supplied when the skin article is bound"*, which RD-P18-9 superseded, and `SkinMaps.md` was corrected at Phase18's close. Conformed at 21.3.
- **F-P21-6 — `SkinMaps.md` still allows CC BY 4.0** (*"CC0-1.0 by default; CC BY 4.0 is allowed … Ruled (RD-MP-8, RD-MP-1)"*). *Two Licences* was withdrawn the same day: *"material are CC0"* (RD-RO-2). Conformed at 21.3.
- **F-P21-7 — The seed's tree claims, re-verified 2026-10-20:**
  - F-SKM-19 holds: no skin declares `base_color_map`, and each pins `subsurface_color`.
  - F-SKM-23's refusal is live in `load_article.py`.
  - The probe's scratch survives in `library/parity/SkinMapsProbe/` (git-ignored).
  - Q-SKM-4 and Q-SKM-7 are answered: RD-P18-1 and RD-SKM-5.
- **F-P21-8 — The asks this phase answers** (from `261016_R_PlatformPhase99Asks.md` and `261019_R_PlatformCharacterEyeAsks.md`):
  - **Q-PMU-1** (where a fit-set picture is carried): by RD-P18-9, in the article's own `base_color_map`, as this phase does.
  - **Q-PMU-2** (the lips): RD-P21-2.
  - **Q-PMU-4** (plastic): F-P21-1 and RD-P21-6, in part.
  - **Q-PCE-2's layout gap** (how a consumer learns its mesh's layout) does not arise while every character is hm08. It stays the ask's.

## Deferred

| What | To | What it consumes from this phase |
|---|---|---|
| A runtime built with Unreal's tinted scatter (the rig's `tint` row in Unreal; Studio's masters through the platform's builder, M7) | the next work on the machine with Unreal; the platform | `build_masters.py`'s `subsurface_color` branch; the twelve articles as served |
| A roughness map (and the other maps beyond colour) | *Skin Maps Beyond Colour* (parked, RD-DS-8; RD-P21-6). Its trigger: click 1's verdict on plastic | `MakeHuman_Body_v01`, the map maker and its calibration, the fitted skins, the rig's atlas switch |
| A face map of its own, or a larger atlas | a later question on the same mesh version | the map maker; G8's size rule |
| Studio wearing the skins | the platform, ledger row (21.3) | the dev install's twelve articles and their pictures; P28; R-PCE-2's names |

## Depends on

- **Nothing outside this repo**, for every click.
- Studio's side is the platform's, through the ledger. It does not hold the close.

## Discovery Log

- **2026-10-20 — Opened and Pass 1** (the lead: *"push, then /discovery Skin Maps"*).
  - **Numbered Phase21** (the head of `## Future`). The stub moved from `Phases/Future/`.
  - **Read:**
    - the seed and `SkinMaps.md` (draft);
    - LCDSchema §Base colour map, Identity §scale tags, RuntimeCatalog `fits`;
    - the research `261014_R_SkinMaps.md` (Passes 1–2, 4–5, §Resolved) and its probe;
    - Phase18's Brief and close;
    - the platform's PMU and PCE asks;
    - Learnings M4, B5, B8, S8, U11 and U14.
  - **Measured:** today's skin on the character on v5 (F-P21-1), the pores' maps, the old sweep (F-P21-2, F-P21-3), the gate's G8 and G9, the release locks, the rig's UVs (F-P21-4).
  - **Decided by the agent unless the lead says otherwise:** RD-P21-1 to RD-P21-5. **Put to the lead:** Q-P21-1, answered the same day: *"a,"* (RD-P21-6).

## Execution Log

*A ledger: step · result · next. The commits carry the how.*

- **21.1 — ✅ (clicks 1–2 sat, 2026-10-20).**
  - **Click 1, the lead:** *"lips blend, cheeks warmer, still reads plastic...Left (the one you tinted) blends better than the right"* (left: the new skin; right: today's).
    - **"Still reads plastic"** is the evidence RD-P21-6 named for un-parking *Skin Maps Beyond Colour*, roughness first. Which phase runs next is the lead's call; it is recorded here, not taken.
  - **Click 2, the lead:** *"seen, put it back"*. The agent set the new skin's tint to (0.2, 0.4, 1.0) in the lead's Blender. The skin took it on the face, neck and hands; the lips and nails kept their own colour (their own articles, tint white). Set back to white.
  - **Built:** the map maker `tools/converters/fit/gen_skin_maps.py` (the probe's v2 recipe, its calibration, `--picture` for a contributor); `FitzpatrickIV_basecolor_sUKN.png` and `skin.yaml`; `Skin_FitzpatrickIV` and `Lips_FitzpatrickIV` fitted (`base_color_const` 0.4546, 0.2406, 0.1389, the scatter colour following the base); Blender's tinted scatter (`load_article.py`); Unreal's (`build_masters.py`, built and not run here); the rig's fitted binding (`build_character.fitted_st`, the atlas st and `uv_scale` 0.006519 on the job).
  - **Measured:** over the skin, the map × the constant averages to the tone (0.436, 0.227, 0.131) exactly; the lips average (0.327, 0.123, 0.076), against the lip rule's (0.349, 0.125, 0.079): the feathering pulls their red down about 6 %. 0.16 % of texels clip at the peak; no island texel is unpainted. The rig ran in all three tools in 29 s; Body ΔE (Storm vs Blender) at the face is 2.35, as today's. `run_all.py`: 18 lanes, 16 PASS, 2 SKIP, 0 FAIL, the baseline. Its first run was red on `test_build_snapshot.py`, whose two checks pinned the tree's fitted set to two articles; that is a FALSE RED, now held to the recipes.
  - **Deviations, each small:**
    - *The lips by face, not by island.* The maker rasterises the Body mesh's parts face by face. An island vote (the fitted teeth's way) put every lip texel in the skin, because the lips share the face's island: the first run measured an empty Lips mask.
    - *A fitted skin is cast as a skin.* Phase18's rule put a fitted article on every part of its mesh, which put the skin on the lips and nails. `rig.py` now casts a fitted `skin` with its tone's lips and nails (`Article.part`).
    - *Unreal tints only a scatter that follows its base.* The master gains `subsurface_follows_base` (0 by default; the driver sets 1), so a value an article pins stays untinted, as in Storm. On v5 a non-white tint on a Subsurface picture is refused by the driver (`RUNTIME_TINTS_SCATTER`), not drawn wrong.
  - **The sitting's surface:** `library/parity/P21_Sitting/P21_SkinIV.blend` (git-ignored; built headless from the factory scene), in four Cycles views: faces on top, the back of the hand below; new on the left, today on the right. Real light: a side sun with shadows, a grey dome, full bounce. **Not** the rig's matched light, which has no shadows and could not show plastic. Today's articles are re-assembled from `HEAD` into `library/parity/P21_today/`.
  - **Next:** the lead's clicks 1–2, then 21.2.
- **21.2 — ▶ SCAFFOLD COMPLETE, sitting owed (click 3), 2026-10-20.**
  - **Built:** the other five maps, and their skins and lips fitted, with `base_color_const`:
    - I: 0.8832, 0.6762, 0.5854
    - II: 0.8331, 0.514, 0.368
    - III: 0.6496, 0.4589, 0.3638
    - V: 0.2951, 0.1569, 0.0838
    - VI: 0.0938, 0.053, 0.0212
  - **Measured:** each map × its constant averages to its tone over the skin, exactly (to 4 places, inside the Brief's 2 %). G8 passes for all twelve recipes; no island is unpainted.
    - **The rig, twelve runs** (six tones, new and today's, after the F-P21-9 fix): Storm–Blender face ΔE for the skin holds at today's (2.1–3.9). For the lips it is within 0.2 of today's (3.1–4.4).
    - On the face, each tool's mean stays within about 3 % of today's and goes slightly redder, alike in all three tools.
    - The sheet is `library/parity/P21_SixTones_sheet.jpg`. `run_all.py`: 18 lanes, 16 PASS, 2 SKIP, 0 FAIL.
  - **F-P21-9 — Storm read every picture supplied through an article's interface input RAW, not sRGB.** Older than this phase; it is why the probe's Storm lips looked pale. Measured on IV's character:
    - A uniform sRGB-128 map against a 255 one rendered at 0.52–0.60 in Storm and 0.28–0.41 in Blender.
    - `colorSpace = "srgb_texture"` on the USD asset value brought Storm to 0.275, Blender's.
    - A `colorspace` on the `.mtlx` interface input, or on the image's `file` input, changed nothing: UsdMtlx does not carry it. Neither did leaving the article's own default in place (raw too).
    - **Fixed in the rig** (`job.MAP_COLORSPACE`). This also moves Storm's eye, hair and teeth pictures, which were raw before (the iris's 15.8 ΔE). **Owed to the platform** (21.3 ledger row): a writer that sets a fitted article's `base_color_map`, its own picture included, authors `colorSpace = "srgb_texture"`, or a Storm-based viewer draws it washed out.
  - **F-P21-10 — The six maps are one picture.** Every term of the recipe multiplies the tone, so the map ÷ the tone is identical for every tone (six byte-identical PNGs; Git LFS stores one). The map still carries hue (redder cheeks and lips), so RD-SKM-3's reason holds. **Kept as six files**, each named by its article, so a contributor can replace one tone's map alone (RD-SKM-3: one map per tone).
  - **Resolved:** the orange fingers in click 2's tinted live view were the viewport before it converged. A converged render shows the whole hand tinted, only the nails (their own article) untinted.
