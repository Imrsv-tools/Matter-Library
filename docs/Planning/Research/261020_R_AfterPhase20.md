# Research — After Phase20: the requests waiting, and what comes next (2026-10-20)

**Mnemonic:** `AFT` — findings `F-AFT-n`, questions `Q-AFT-n`.
**Altitude:** a **triage** of what is waiting on the library (asks, holds, an open phase), then the next phase in the lead's order. Audit, not design. It commits to nothing; each answer it drafts is a recommendation until the lead rules.
**Asked by:** the lead, 2026-10-20: *"Grab the latest from git... evaluate if there are any reqeusts we should address and if not, let's think about the next phase"*.

## Pass 1 — The sweep (2026-10-20)

**Examined.**
- This repo at `origin/main` `92df0ca`. The checkout was **15 behind** and is not converged (F-AFT-1), so everything here was read at origin.
- The ledger (`PlatformDependencies.md`), the asks docs written since 2026-10-16, the Phase20 doc, the batch records, open issues.
- The consumers' repos, fetched and read at origin, for anything addressed to this repo since 2026-10-16. They are private, so only what this repo needs is recorded here.

**F-AFT-1 — the checkout cannot converge without the lead.** Six tracked files carry uncommitted edits dated 2026-10-14 to 2026-10-16. Five are method files (the Refiner's lane), and two of them are also changed upstream: `.claude/skills/matter-batch/SKILL.md` and `matter-generate/SKILL.md`, so `git merge origin/main` refuses. Measured: the edits are older than the checkout's last commit, so this is not a live session. They are small hunks (*"never push unasked"*, a batch's *owed lines*), and they do not overlap upstream's lines. **Not restored or stashed:** they are another session's.

**F-AFT-2 — two asks docs have no library pass and no ledger row.**
- `261016_R_PlatformPhase99Asks.md` (PMU, 2026-10-16): 5 reports, 7 asks.
- `261019_R_PlatformCharacterEyeAsks.md` (PCE, 2026-10-19): 2 reports, 2 asks.

The ledger has not changed since 2026-10-16, and the next free id is **M14**.

**F-AFT-3 — Phase20's click 4 was in effect seen on the platform's side.**
- **The sitting:** the platform's library-window phase, at its Desktop sitting on 2026-10-19, on the machine with Unreal, Studio serving this library at `092df05`, which holds Phase20's switch.
- **What it showed:** the Sky picker applied `Kloppenheim07_v01.hdr` and `Kloppenheim02_v01.hdr`, published names with no *PureSky*. The lead passed the sitting.
- **The other half of click 4:** a scene saved with an old name keeping its sky is covered by the platform's own fixture and test of the hidden old names. No one has clicked it in Studio.
- **Click 5** (the website) is the platform's P30.
- **Also stale:** Phase20's own `Next:` line still says *"/execute once the lead answers Q-P20-1 and Q-P20-2"*.

**F-AFT-4 — the platform's PMU reports move four ledger rows** (each against the row's own stated check):

| Row | What the report asks |
|---|---|
| P11 | to `DONE`: `check_lcd_carrier.py` passed on an app-saved composition (77 overrides) |
| P17 | to `DONE`: the platform's own probe found cards seen 3, failing 0 |
| P29 | its Studio half closed *not built, by the lead's ruling*. The scale grids are offered as ordinary materials, and the swap-the-scene view stays Blender's |
| P21 | built; its check was seen at the platform's exit sitting |

**F-AFT-5 — the nine asks, sorted by what answers them.**

**(a) Answered by specs already on disk.** A ledger row records the answer and nothing else is built.
- **Q-PMU-1, the fit-set picture's carrier:** the article names its picture as its own `base_color_map` value and declares `fits`. This has been the rule since Phase18 (RD-P18-9, LCDSchema §Base colour map), and it is the platform's proposed answer.
- **Q-PCE-2, `fits`:** RuntimeCatalog `materials[].fits` and Taxonomy §Character already say what it means.
  - It names the UV layout the article's own picture is painted for, `<Family>_<Mesh>_vNN`. Today the layouts are `MakeHuman_Body_v01`, `_Eyes_v01`, `_Teeth_v01` and `_Tongue_v01`.
  - An article without `fits` has no picture of its own, so it fits any mesh.
  - Every character today is on the MakeHuman layout, so a consumer that ignores `fits` binds correctly today.
  - **One gap the spec does not close:** how a consumer learns its own mesh's layout. The library pins each layout by a hash in `tools/converters/groups.py`, and no consumer reads that. This only matters when a second layout exists.

**(b) Need a lead ruling.**
- **Q-PCE-1, whether the single-part eye articles stay `creator_selectable`.** The spec says that flag is `false` only on `IMRSV_MissingMaterial`, and it filters every consumer's browse at once, Blender's Asset Browser included.
  - **Recommendation: keep them selectable.** Hiding them is the platform app's own choice (it offers whole-eye looks only), and a Blender user mixing an eye still wants the parts.
  - **The alternative:** mark them building blocks (`false`), which refines the spec.

**(c) Material work: the standing `/matter-batch` process, not a phase.**
- **Q-PMU-3:** the coloured LED articles get a darker body, and a starting brightness at which red reads red.
- **Q-PMU-5:** Felt's Roughness control has no room under its fuzz. Either give it room or state that it is inert.
- **Q-PMU-6:** Felt reads out of scale on a 2 m cube; check its `s001` tile against its picture.
- **Q-PMU-7:** more eye colours, and an `Eye_Natural` that reads calm.

`Felt_Natural` and `Eye_Natural` already sit on the wish list as queued re-judge rows. They would become `redo` rows carrying the platform's words, and the LED and eye colours would be new rows.

**(d) Inputs to the next phase, Skin Maps.**
- **Q-PMU-2, what the lips wear:**
  - the seed's form is the skin article plus the map (F-SKM-9);
  - the platform adds a second form: a lip article (wetter, finer) that also takes the map, which keeps the shine.
- **Q-PMU-4, skin still reads as plastic in Unreal, at every control's range.** See F-AFT-7.

**F-AFT-6 — the maintainer's holds from batch 261016-2** (`library/batches/261016-2.md`):
- **Rust_OnSteel's rebuild is withdrawn.** It is in released `0.1.0`, and its new textures are not in that lock. The ruling it waits on: how a released article's rebuild lands.
- **Onyx is not started.** It waits on a ruling on the scale-repair method for banded matter.
- **LED_WarmWhite is colour-only.** Retire it or not?
- **Three built rows await keep or redo:** LED_WarmWhite, Slate_Cleft and Granite_Polished. Titanium_Raw from 261016-1 waits too.
- **Issue #4** (the pilot's freeze on a machine with a staged folder) is open since 2026-10-05: box input, not a regression.

**F-AFT-7 — Skin Maps is ready for discovery, but its scope may not reach the platform's complaint.**
- **Ready:** the survey and the probe are done, RD-SKM-1 to RD-SKM-6 are ruled, Q-SKM-4 was answered by Phase18 (RD-P18-1), and a draft spec exists.
- **Stale:** the seed's open-questions list still shows Q-SKM-4 and Q-SKM-7 as open.
- **The scope gap:** Skin Maps is **colour only**, which removes the lip line and adds variation (F-SKM-22, F-SKM-25). *"Plastic"* is a highlight and scatter judgement, and those maps are *Skin Maps Beyond Colour*, which the lead parked (RD-DS-8). It may also lie in the articles' values or in the Unreal Subsurface master, which no map fixes. Q-PMU-4 names all three places.
- **So discovery should take Q-PMU-4 as a question of its own** (Q-AFT-3), not assume the colour map answers it.

**Decision / next.** Nothing here forces work ahead of the lead's order. The requests sort into: one ledger quick fix (F-AFT-4, F-AFT-5 (a)), one ruling (Q-PCE-1), wish-list rows (F-AFT-5 (c)), and inputs to Skin Maps (F-AFT-5 (d)).

## Resolved

*The lead, 2026-10-20, in one line: "1 commit them, 2 yes close P20, 3 yes, 4 what does this mean? how many parts to an eye?"*

- **RD-AFT-1 — the stale method edits are committed as the Refiner's** (*"1 commit them"*; Q-AFT-1). They are drain 3's held edits (`.claude/CLAUDE.md`, the two skills, the heritage re-sync, the backlog). Committed as `0277662` by this session, which did not author them. The checkout then merged `origin/main`.
- **RD-AFT-2 — the platform's 2026-10-19 sitting counts as Phase20's click 4, and Phase20 closes** (*"2 yes close P20"*; Q-AFT-2). Closed as `53d31a4`, on the library's half.
- **RD-AFT-3 — Skin Maps' discovery carries Q-PMU-4 (*"still plastic"*) as its own question** (*"3 yes"*; Q-AFT-3). That includes a first look at where the plastic lies: the articles' values, the pictures, or the Unreal Subsurface master's highlight. It is not assumed that the colour map answers it. Cross-referenced in `Phases/Future/PhaseTBD_SkinMaps.md`.
- **RD-AFT-4 — the single-part eye articles stay `creator_selectable`** (the lead, 2026-10-20: *"keep them selectable"*; Q-PCE-1). `Cornea_`, `Iris_`, `Pupil_` and `Sclera_` stay in every browse (Blender's Asset Browser included). Offering whole-eye looks only is the platform app's own choice, and the spec (`RuntimeCatalog` `creator_selectable`: `false` only on `IMRSV_MissingMaterial`) is unchanged. The ledger row that tells the platform is the offered quick fix (M15).

## Open questions

| Id | Question | Recommendation |
|---|---|---|
| ~~Q-AFT-1~~ → **RD-AFT-1** | ~~The six stale uncommitted method edits: commit, discard or leave?~~ | committed |
| ~~Q-AFT-2~~ → **RD-AFT-2** | ~~Does the platform's sitting count as Phase20's click 4?~~ | yes; Phase20 closed |
| ~~Q-AFT-3~~ → **RD-AFT-3** | ~~Does Skin Maps' discovery carry Q-PMU-4 as its own question?~~ | yes |
| ~~Q-PCE-1~~ → **RD-AFT-4** | ~~Do the single-part eye articles stay `creator_selectable`?~~ | kept selectable |

## Status

- **Passes captured:** 1 (the sweep, 2026-10-20, read at `origin/main` `92df0ca`). The checkout has since converged.
- **Ruled:** RD-AFT-1 to RD-AFT-4 (2026-10-20). The Refiner's edits are committed, Phase20 is closed, Skin Maps carries *"plastic"*, and the single-part eye articles stay selectable.
- **Current direction:** `/discovery` on **Skin Maps**, which is next in the lead's order (RD-SV-1) and is the lead's gate. Carry into it:
  - Q-PMU-2, the lips;
  - Q-PMU-4, plastic (RD-AFT-3);
  - Q-PCE-2's layout gap.
- **Offered as `/quick-fix`es, none taken:**
  - the ledger: P11 and P17 to `DONE`, P29's Studio half closed, P21 seen, and M14 (PMU) and M15 (PCE) recording the asks and their answers;
  - the wish-list rows for the LED, Felt and eye asks.
- **Open:** nothing of the lead's from this doc. The batch holds (F-AFT-6) are the maintainer's.
- **Next step:** `/discovery` on Skin Maps (the lead, 2026-10-20: *"push, then /discovery Skin Maps"*). The quick fixes wait for the lead's word. Nothing is numbered or seeded by this doc.
