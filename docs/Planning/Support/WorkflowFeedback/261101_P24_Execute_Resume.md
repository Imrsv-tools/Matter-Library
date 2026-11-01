# Workflow Feedback — P24 / execute → close / resume

| | |
|---|---|
| **Verb** | `execute` (resume at 24.2, through 24.3) **and its close** (`execute_close.md`, on the lead's *"close Phase24"*) |
| **Unit** | `P24` |
| **Mode** | resume run 2 (run 1 suspended at ~370k; its retro is `261101_P24_DiscoveryExecute_ColdStart.md`, already drained), then close |
| **Outcome** | `done`: the 8K maker built (in bands of rows), `Skin_Tone34` + `Nail_Tone34` made, clicks 2 and 3 sat (*"C is fine."*, *"seem to be the same person"*), served, closed and pushed (`b43cff1..4062d1c`) |
| **Shape** | `behavior-touching` |
| **Confidence** | Ran fully: execute stages 2–4 and the close, push included. **Not exercised:** the dev snapshot (not asked for), the high-rigor lane, `execute_repair.md`. |
| **Date** | `2026-11-01` |

Not a continuation of another file: run 1's retro covered discovery and the first execute session; this file covers only the resume and the close. Step 0's offer (`ML_P25_D1` on `/discovery Phase25`) was answered *"Not yet"*.

---

## Items, ranked

### 1 — The first look at C waited ~1 h 50 behind the 8K pipeline, though the tuning ran at 2048 and C could have been shown there in ~40 min `[self-error-doc-could-prevent]`

**Grounding.** The Brief's click 2 needed *"the makers at 8K"*, so I built the banded composer, made the colour (7:49) and the shine set (9:01) at 8K, built the articles, *then* rendered A · B · C. But the subject's colour was solved at 2048 (`library/parity/P24_Solver/solve_subject.py`, ~3 min) and the ledger itself said *"The tuning runs at 2048 … only the final set is made at 8K"*. A 2048 C (the subject's colour + the shared shine maps, ~1 min to make) could have reached the lead about an hour earlier, with the 8K remake running while they looked. The lead accepted the 8K C at once (*"C is fine."*), so nothing was lost this time. If they had named a region, every iteration would have paid ~17 min of 8K remake instead of ~1 min at 2048. `execute.md`'s *"drain the critical path to the first human test FIRST"* was in context; the Brief's step text (*"the makers at 8K … Click 2, iterated"*) read as making 8K a precondition of the click.

**Proposed fix.** In `execute.md` §BUILD, beside *"Restate the Outcome … drain the critical path"*: *"When the shipped form is expensive to make (a larger size, a full rebuild) and the judgement does not depend on that cost, show the cheap form first and make the expensive one while the lead looks. Ask: would the lead's verdict on the cheap form differ? If no, it goes first."* And in `discovery.md`'s Step list: a click's prerequisites name what the JUDGEMENT needs, not everything the step ships.

**Where it'd live.** `execute.md` §BUILD (portable); `discovery.md` First human test.

---

### 2 — A rule the Refiner landed mid-run contradicted the live phase's Brief, and the run found it only by grepping for something else `[doc-gap]`

**Grounding.** Drain 4B (`66d9017`, landed during this run) put *"a character material's LOOK is judged … in the library's Unreal look view — never Blender"* into `LOCAL_DELTAS.md`'s artifact row. Phase24's Brief (written that morning, before the row) put click 3 *"in the lead's Blender … built headless from the factory scene"*. I noticed only because a later commit subject said *"a character's look is judged in Unreal, never Blender"* and I grepped for it before building the Blender scene. Otherwise click 3 would have been a Blender scene the lead had ruled out twice. The Refiner did use the cross-session channel this run (the bar-marks relay, which worked well), but not for this rule.

**Proposed fix.** In `workflow-refiner.md`'s drain: *"Before committing a rule that changes where or how a click is judged, grep the ACTIVE phase docs' First human test and step list for the old form. Each hit is a correction owed to that live run: name it in the commit subject and send it through `SendMessage` where the harness offers it."*

**Where it'd live.** `workflow-refiner.md` (portable).

---

### 3 — Run 1's ledger recorded a solve as done whose numbers were saved nowhere `[self-error-doc-could-prevent]`

**Grounding.** Row 24.2.4 read *"The subject's `FACE` and `LIPS` rows are solved on IV's fit"*, marked `no commit`. The solver's outputs (`face_tbl_*.json`, `fields.pkl`) were not in `P23_Solver/`. I spent several calls searching the parity folders and the previous job's tmp before concluding the solve was owed, and re-ran it (8 iterations, ~3 min). The Resume block's item (b), *"the solve at 2048"*, disagreed with the row, and only the code settled which was true.

**Proposed fix.** In `execute.md` §Keep the lead oriented, under the write ceiling: *"A ledger row with no commit that claims a RESULT names the file the result lives in (a scratch path is fine). If the result exists only in the transcript, the row says 'designed, not run'."*

**Where it'd live.** `execute.md` §Keep the lead oriented (portable).

---

### 4 — Stack facts from this run, for the Learnings tally (single sighting each) `[doc-gap]`

**Grounding / the facts.**
- **The same relief design draws ~3.5× stronger normals at 8K than at 2048** (face RMS tilt 0.25 vs 0.07). 2048's 3×3 supersampling averaged away furrows narrower than a texel; at 8K they are drawn. Depths tuned by eye at one size do not carry to another. Visible on the back of the hand at click 3.
- **A whole-picture iterative bleed (64 px at 8K) costs minutes per map.** Working only the new ring each pass gives the same values per pixel in seconds (`gen_skin_maps.bleed` above 2048).
- **A scan's tone measured over its own coverage mask matches no region the maker can name.** Holding the maker's head to it left the face 0.25 log off (the scalp and ears differ). Hold on a region both sides define (here MPFB's face mask > 0.9) at the scan's mean *there*.
- **8K makers in bands:** colour 7:49 / 11.7 GB, shine 9:01 / 20.8 GB, against ~45 GB made whole (`CoreMechanisms.md` row 1 carries the mechanism).

**Proposed fix.** Tally; promote to `docs/Learnings/` (NumPy/imaging, or Skin) on a second sighting.

**Where it'd live.** `_RefinementBacklog.md`'s stack-facts tally.

---

## Keep these

- **Proving a new fast path equal to the old one before trusting it** (`band_check.py`: banded vs whole compose at 2048, 1.8e-7; the shared 2048 shine maps remade pixel-identical after the 8K edits). It made the 8K output trustworthy without an 8K reference.
- **Measuring the render before the showing** (`execute.md` §TRY: a look an instrument can read). The patch measurements at click 2 put numbers on what the lead might see, and they went into the ledger as the record behind *"C is fine."*
- **The Refiner's cross-session relay** of the bar's own marks (click 1) arrived before click 2 and stopped me reading them as gaps in C.
- **`.claude/CLAUDE.md` §Git's push row** (`log origin/main..HEAD`, read every line, push by value). The pre-close fetch found a sibling research commit, disjoint, merged cleanly.
- **The close's arming gate on row A0**: one question settled "not armed" without reading the long cell.

## Dead weight

None.

## Open questions

1. **A consumer's research doc links to itself at the wrong path:** `docs/Planning/Research/261101_R_PlatformSkinAndMakeupAsks.md` has a `](Research/261101_R_PlatformSkinAndMakeupAsks.md)` link that resolves to nothing. It was there before this run, and that doc's passes belong to its author, so I left it. A `/quick-fix`, or the consumer's next pass. *(Content, not methodology.)*
2. **The 8K relief's strength on the hands** (item 4): the lead passed click 3 without flagging it. Whether *Variety* re-runs of this recipe should halve the depths at 8K is a product call for that phase, not a refiner item.
3. **The dev snapshot carrying Tone34** (In now, *"at the lead's word"*) was not asked for at the close. It is offered in the close handback and recorded in the phase doc's CLOSE row.
