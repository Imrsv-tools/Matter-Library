# Workflow Feedback — P27 / execute / cold start

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P27` |
| **Mode** | `cold start` (session `ML_P27_E1`) |
| **Outcome** | `done` for 27.1: the bare judge and the fitted body built, click 1 sat (*"it is aliggned"*), its two creases fixed; 27.2 handed to `ML_P27_E2` (running) |
| **Shape** | `behavior-touching` (`look.py`, `build_character.py`, `drivers/unreal.py`, new `project_body.py`) |
| **Confidence** | Ran fully: BUILD, TRY (one sitting, two lead turns), STRENGTHEN (one repair), the look view in Unreal, `run_all.py`. **Not exercised:** the close, a push, any publish, the high-rigor lane. |
| **Date** | 2026-11-02 |

---

## Items, ranked

### 1 — The click's picture left out the reference the Brief's click named; the lead had to ask for it `[self-error-doc-could-prevent]`

**Grounding.** The Brief's click 1 reads: *"The reference already judged: `f4_s50_seed7.png` (… "that one looks really good"); the click asks whether the body on hm08 now looks like it."* I built the sitting picture as C | D (`click1_tback.png`) and asked "is D aligned?". The lead's first words: *"Maybe... can you show me what the source looked like?"*. Once it was open, they answered: *"Yes... ok.. it is also splochy.. that is what I needed to see... it is aliggned"*. A whole round trip, and the question the click poses (does it look like the reference?) cannot be answered from a picture without the reference in it.

**Proposed fix.** In `execute.md` §TRY, beside *"Say in one sentence what to compare and what right looks like"*: *"When the click compares against a reference the lead already judged, that reference is IN the picture (a column, the same framing where it has one, else beside it at native size). A column of 'today' (C) is not the reference."* The sentence *"measure … against the reference the lead has accepted"* exists, but only for measuring, not for showing.

**Where it'd live.** `execute.md` §TRY (and `discovery.md` First human test, where a click names its reference).

---

### 2 — Measuring before the sitting caught five defects; each fix was found only by looking at the next picture `[doc-gap]` (a keep, with one refinement)

**Grounding.** Between the first fitted D and the picture shown, in order, each caught by me in the look view or the quick renderer, never by the lead: (a) a 35 % level step where back and profile cameras meet, drawing a second waist and hip; (b) an atlas-smooth levelling that drew lines down the spine and across the shoulders (the back's two halves are separate atlas pieces); (c) pale streaks where every camera grazes, brightened by dividing out the light; (d) a pale patch at the waist and a line on the lower back, from the model's arm edge inside the silhouette; (e) a dark hip patch that turned out to be the arm's cast shadow, in C too. The lead then found (f), two waist creases: the same cause as (d), at the elbow. **The refinement:** (e) cost a diagnosis before I opened C's same view. Comparing D to C in the same view is the cheapest test of whether a mark belongs to D at all, and it settled (f) at once.

**Proposed fix.** In `execute.md` §Verify, the ad-hoc-check row (*"A reading that disagrees with the picture indicts the instrument"*): add *"A mark on the candidate is first looked for in the control's same view (today's / C's) — the light, the mesh and the shadows are shared, so a mark in both is not the candidate's."*

**Where it'd live.** `execute.md` §Verify (ad-hoc-check row) or §TRY's effect-off control sentence.

---

### 3 — A Brief default ("colour as painted, unless the lead says otherwise") overturned on a measurement: handled by the false-fact row, and it worked `[doc-gap]` (small)

**Grounding.** RD-P27-5's default kept the colour as painted. The look view showed it fails the click's own question (doubled contours from the views' different painted light), so I built delighting and levelling, logged a DEVIATION with the numbers (35 % → 0.9 %), and named it in the handback as a call the lead could strike. The nearest row, §Divergence *"A FACT THE BRIEF RESTED ON IS FALSE"*, fits only loosely: here a *default* failed its own click, not a premise.

**Proposed fix.** Widen that row's trigger: *"…or a Brief DEFAULT ('unless the lead says otherwise') fails the click it serves, measured."* The same action follows.

**Where it'd live.** `execute.md` §Divergence.

---

### 4 — Stack lesson: a correction smooth in the ATLAS is not smooth on the BODY `[doc-gap]` (a learning)

**Grounding.** Seam levelling solved on atlas cells drew a hard line down the spine and across the shoulders: hm08's body island is cut down the back, so neighbours on the body are far apart in the atlas, and each half drifted on its own. Linking the cells by 3D distance (1.2 cm) fixed it. The same trap waits for any blur, fill or field on this atlas (pull-push fills are atlas-local too: the faint spine line, handed to 27.2).

**Proposed fix.** A Learnings entry: *"On hm08's atlas, anything smooth (a blur, a fill, a correction field) is built on the body (3D neighbours), not in UV: the island's own cuts join pieces the atlas holds apart."*

**Where it'd live.** `docs/Learnings/` (a texture or projection domain; first sighting).

---

### 5 — `library/parity/` is a symlink out of the repo; "git-ignored" is the wrong word for it `[doc-gap]`

**Grounding.** The Brief (RD-P27-3) and the reproduce lines say the pictures go under the *"git-ignored `library/parity/P27_*`"*. `git check-ignore` on such a path fails: *"pathspec … is beyond a symbolic link"*. The folder resolves to the WorkingDrive (`look.py` printed `/run/media/…/MatterLibrary/parity/…`). The outcome is the same (nothing there can be committed), but "git-ignored" is a property that can change with one `.gitignore` edit; "outside the repo" cannot. It also means the pictures vanish when the drive is unmounted.

**Proposed fix.** Where `LOCAL_DELTAS.md` or `ToolingConventions.md` name `library/parity/`, say it is a link to the machine's working drive (outside the repo) on the machine with Unreal, and that the parity pictures need that drive mounted.

**Where it'd live.** `LOCAL_DELTAS.md` (Two machines) or `docs/ToolingConventions.md`.

---

### 6 — One no-op tool call while waiting on a background job `[self-error-doc-could-prevent]` (doc already right)

**Grounding.** After launching the look view in the background I ran `echo waiting`, which is exactly the tripwire's *"a no-op call is the same violation"*. No harm, but it is the rule's exact shape. The doc is clear; no change proposed beyond counting the sighting.

**Where it'd live.** `execute.md` Rule 3 (tally only).

---

## Keep these

- **"Measure before the lead sits; a click you saw come out wrong never reaches them"** (§TRY): it caught five defects (item 2) before the first showing. The lead's sitting found one, with the same cause as one already fixed.
- **One picture per stop, opened, the question naming the file and each column** (this phase's Brief, from Pass 2's retro): one turn to the verdict once the reference was shown.
- **A fast loop beside the judge** (§BUILD *find the fastest loop*): an orthographic renderer (seconds) for texture defects, Unreal (~3 min) only to confirm. Each defect was found in the fast loop and confirmed in the slow one, except (e), the shadow, which only the judge's light could show.
- **The ledger-row rule** (no row may carry its own commit's SHA): steps cited as "the `27.1` commit", no follow-up commits for hashes.
- **The read-back after every commit** (`git show --stat`): four commits, each matched its intended file list while a sibling's files sat modified in the same tree.

## Dead weight

None.

## Open questions

1. **For the lead, not the Refiner:** the delit and levelled colour (RD-P27-5's default overturned) is recorded as a deviation the lead may strike. Their verdict (*"it is aliggned"*) was on that D, so it reads as accepted, but they ruled on alignment, not explicitly on delighting.
