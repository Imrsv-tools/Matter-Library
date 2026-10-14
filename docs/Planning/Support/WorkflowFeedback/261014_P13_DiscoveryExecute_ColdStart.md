# Workflow Feedback — P13 / discovery → execute / cold start

| | |
|---|---|
| **Verb** | `discovery → execute` (one session: numbered and discovered the phase, executed 13.1–13.3, closed it) |
| **Unit** | `P13` (Materials Described) |
| **Mode** | `cold start` |
| **Outcome** | `done`: two dev snapshots published (`matterlib-0.2.0-dev.1`, `-dev.2`), the words for all 95 confirmed, the phase closed and pushed (`d59d745`) |
| **Shape** | `behavior-touching` (a new publishing tool, recipe metadata, the batch skill) |
| **Confidence** | Ran fully: `discovery`, `execute`, the close. **Not exercised:** `plan`, `research`, `quick-fix`. |
| **Date** | `2026-10-14` |

**Not a continuation** of `261014_P13_Execute_Close.md`: that file is this same session's earlier single-item deposit (the lead's "push as part of close" ruling), and is not restated here. The backlog was read first; none of the items below is in it.

---

## Items, ranked

### 1 — `LOCAL_DELTAS.md` says "No browser surface"; this phase's surface was a GitHub release page in the lead's browser `[doc-gap]`

**Grounding.** The row *"the lead's real surface (`discovery.md` First human test)"* ends *"No browser surface."* Phase13's first human test was the dev snapshot's GitHub release page, opened in the lead's browser (and named for his iPad). That was the right surface: the published thing itself, which the lead judged (*"looks right, go on with 13.2"*). The discovery had to argue its way past the row via `discovery.md`'s *"name the closest thing the lead can open there (a repository page)"*.

**Proposed fix.** Amend the row: *"…or, for a phase that publishes (a GitHub release or pre-release), **its release page in the lead's browser**: the published artifact is the surface (Phase13). No other browser surface."*

**Where it'd live.** `LOCAL_DELTAS.md` (port gap).

---

### 2 — A third publishing producer exists now and `LOCAL_DELTAS.md` names two `[doc-gap]`

**Grounding.** `LOCAL_DELTAS.md` lists *"a publishing producer"* (the release lifecycle) and *"a second publishing producer: the Unreal test runtime"*, each with its trigger, lock and marker (`execute.md` asks for all three). Phase13 added the dev snapshot. Its trigger is `uv run tools/releases/build_snapshot.py --tag matterlib-X.Y.Z-dev.N --publish --target <sha>`, run on the lead's word with `<sha>` on `origin/main`. Its lock is the tag (the next free `N`), and it has no watcher or marker. `--publish` resumes an interrupted draft (Learnings `GitHub/G1`). A future agent reading the producers table would not find it.

**Proposed fix.** A third row, *"a third publishing producer: the dev snapshot (Phase13)"*, with exactly those facts and a pointer to `docs/ToolingConventions.md` §Entry points, which already carries the commands.

**Where it'd live.** `LOCAL_DELTAS.md`.

---

### 3 — The publish ask named the size (468 MB) but not the time it would take on the lead's network, and the battery ran out mid-upload `[self-error-doc-could-prevent]`

**Grounding.** The Brief's hazard said *"measure it at build, and name it in the publish ask"*. The ask said *"407 files, 468 MB"*. The upload ran at about 6 MB a minute (31 assets in about 4 minutes), roughly 78 minutes in all, on a laptop on battery. The lead: *"this netwrok might be too slow…"*, then *"The battery will die... pause"*, then *"Welp... it died"*. It was recovered (the draft was resumed; `GitHub/G1`), but at the cost of a dead machine, a resume path written mid-flight, and two round trips.

**Proposed fix.** When a publish is over about 100 MB, the ask states an expected duration, not only a size: measure the uplink for a few seconds, or give the first minute's rate once the upload starts, and say plainly that the machine must stay awake and on its network for that long. Offer the split (small assets first, zips after) up front, not when the network proves slow.

**Where it'd live.** `LOCAL_DELTAS.md`'s new producer row (item 2), or `execute.md` §TRY if the Refiner judges it portable (any project publishing large artifacts from a laptop).

---

### 4 — The Brief picked a biological article (Enamel) as a fixture and the words sheet led with biological pages; the lead had to stop it `[self-error-doc-could-prevent]`

**Grounding.** The discovery chose `Enamel_Natural_Clean_Base_s001_v01` as the "never rigged" fixture for act 4, and `words_sheet.py` sorted domains alphabetically, so the lead's first page was `biological`. The lead: *"Please stop using biogical for any examples and in fact - we need to make that a second class category... it is not Matter, it really requires a human context (not cubes) stay focused on our Matter Materials for examples"*. The product half is now ruled and recorded (Phase13 RD-P13-2; `SiteFile.md` `section`; Taxonomy's dated note; `/matter-batch` §2). **The method half is not:** nothing an agent reads before choosing a fixture or an example says it.

**Proposed fix.** One line where fixtures and examples are chosen: *"Examples, fixtures and first pages use **Matter** materials; biological materials are not Matter and are never an example (the lead, 2026-10-14, Phase13 RD-P13-2)."*

**Where it'd live.** `LOCAL_DELTAS.md` (a project fact every verb's fixture choice should see), or `AI_Orientation.md`. Unsure which; the Refiner's call.

---

### 5 — I wrote a one-off "the words change no article" check when the harness already has one `[self-error-doc-could-prevent]`

**Grounding.** After adding the words to 95 recipes I needed to prove no `.mtlx` changed. `run_all.py`'s `determinism` lane prints `byte-stable` per recipe, which I first read as "matches disk". It only means "assembles the same twice" (`AuthoringHarness.md` says so accurately). So I wrote an ad-hoc script assembling each recipe from the working tree and from `HEAD` (95/95 identical). `check_determinism.py` already has *"optional regen-matches-committed"* (`AuthoringHarness.md` line 47), the reuse I missed.

**Proposed fix.** In `ToolingConventions.md` §Entry points, one row: *"prove a recipe change touches no article (metadata only): `check_determinism.py`'s regen-matches-committed mode"*. That keeps the reuse findable by its purpose, not by its lane name.

**Where it'd live.** `docs/ToolingConventions.md` (product doc, not methodology; flagged here because the miss was a reuse-check miss, `discovery.md` §The reuse check).

---

## Keep these

- **`LOCAL_DELTAS.md` §Separation's "grep your added lines for the consumer's id patterns before committing".** The Brief carried six of the platform's ids (its phase number, a step number, ruling ids) and its staging hostname. The grep caught all of them before the first commit of this public repo.
- **`discovery.md`'s "check each click's surface can show the thing judged" and the fixture-read rule.** Measuring found that Marble (the first fixture considered) had no sweep, so it could not carry act 4's verdicts. Copper replaced it before the Brief shipped.
- **`execute.md` "confirm a check can fail".** Copper's zip rendered as copper standalone and flat grey with its textures hidden. Without the second render the smoke proves nothing.
- **The filtered stage for a file shared with a sibling** (`.claude/CLAUDE.md` §Git): 13.3's lines in `SKILL.md` committed alone, and the Refiner's two held hunks stayed untouched.

## Dead weight

None.

## Open questions

1. Item 4 is a lead preference turned ruling: should it live as a project fact (`LOCAL_DELTAS.md`) or as a product rule only (`Taxonomy.md`, where it already is)? The Refiner's call; the lead may have a view.
2. Restructuring the `biological` domain (*"we need to set taht up"*) has no owning phase yet. It sits in Taxonomy's Reevaluate note and in *Thumbnails* for the pictures. Whether it needs a Roadmap seed is the lead's call.
