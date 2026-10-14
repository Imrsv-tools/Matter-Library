# Workflow Feedback — P17 (Thumbnails) / discovery / cold start

| | |
|---|---|
| **Verb** | `discovery` |
| **Unit** | `P17`: **Thumbnails**. Earlier the same day, `P17` meant *The Library Service* (RD-DS-8 renumbered it), so the filename carries the name. This is not a continuation of any Library Service deposit. |
| **Mode** | cold start |
| **Outcome** | done: Pass 1 wrote the Brief, BRIEF READY, lane build, committed `a903b51` (phase doc + Roadmap line); not pushed |
| **Shape** | doc-only |
| **Confidence** | Ran fully: discovery's reads, the gate baseline, headless Blender probes, the consumer sweep (read-only), the Brief, commit and read-back. **Not exercised:** forking to the lead (no question survived the four tests), `/execute`. Items that predict execute-time behaviour are inferential and marked. |
| **Date** | 2026-10-14 |

**Step 0:** nothing was left only in chat. The Brief, its five closed calls (RD-P17-1 to -5), the findings and the baseline are in the committed phase doc. The website's address went only into the handback, on purpose (item 1).

---

## Items, ranked

### 1 — A first human test on a CONSUMER's surface has no rule for where its address goes, and the consumer sweep reads private docs to find it `[doc-gap]`

**Grounding.**
- `discovery.md` §The Brief asks the first human test to name *"where the lead will reach it (the URL, or the running tool)"*.
- `LOCAL_DELTAS.md` §Separation has Pass 1 sweep the consumers' docs at origin, and those docs are private.
- Click 5 of this Brief is on the website's staging. The only place its address and its behaviour are written is the website's private phase doc: its menu naming, the mirror job that takes the library's pre-releases, and when that job runs.
- My first draft wrote three such facts into this public repo's phase doc:
  - *"Explore → Matter"*;
  - *"the website's mirror must also pick it up"*;
  - *"It picks up the library's published pre-releases by itself"*.
- They were caught only by `.claude/CLAUDE.md`'s *"re-read every sentence you wrote from a private source"*, done as a deliberate grep pass before staging. An id grep found nothing; every leak was a fact, not an id.
- I adapted by naming the surface **by role** in the doc ("the website's staging, which reads the published dev snapshots, SiteFile") and putting the address **in the handback only**.

**Proposed fix.** One sentence on `LOCAL_DELTAS.md`'s *"the lead's real surface"* row (or *the artifact a person reaches*): *"When a click is on a consumer's surface (the website's staging, Studio), the phase doc names it by role and cites only what this repo already publishes about it (SiteFile, PlatformDependencies); its address and its behaviour go in the handback, because they are read from the consumer's private docs."*

**Where it'd live.** `LOCAL_DELTAS.md` (a local fact: a public producer whose consumers' docs are private). The portable half, *"a first human test on someone else's surface is named by role"*, is the Refiner's call.

---

### 2 — The Brief's fixtures contradicted the Brief's OWN routing table; each was caught on a pre-commit data read `[self-error-doc-could-prevent]`

**Grounding.**
- I wrote the subject table (*"ground: … stone and terrain at `s1`/`s10` → a slab"*) and click 1's fixture (`Granite_Polished`, *"on the sphere and cube"*) in the same pass. `Granite_Polished` is `s1`, so my own table put it on a slab.
- Click 2 named `OakLeaf_Natural` as the leaf-card fixture inside a click about *kept* materials. It is a `draft`.
- Both surfaced only because I re-read each fixture's status and scale from the dev.5 site file before committing. That is `discovery.md`'s *"A fixture's state is READ from its data, never inferred from its name"*.
- That rule catches a fixture whose **state** is wrong. What I hit is a different defect: a fixture whose state is right, but which the Brief's own selection rule routes to a different subject than the one the click claims to show.
- The fix changed the table too. "Ground" cannot be decided by the scale tag alone (`Granite_Polished` and `Slate_Cleft` are both `s1`), which became a finding.

**Proposed fix.** Extend the first-human-test fixture sentence: *"…and where the Brief routes articles by a rule (a subject table, a class map, a tag), run each fixture through that rule and check that it lands where the click says it does. A fixture that contradicts its own Brief's rule is wrong in one of the two."*

**Where it'd live.** `discovery.md` §The Brief, First human test, beside the fixture sentence. It is near backlog row 48 (*"a click's surface or fixture cannot show the thing judged"*) but not the same: the surface could show it, and the Brief's rule disagreed with the click.

---

### 3 — The gate's failing reason sits about 1000 lines above its summary; I ran the whole gate twice to read it `[doc-gap]`

**Grounding.**
- `run_all.py` ended `17 lanes: 14 PASS, 2 SKIP, 1 FAIL … approval_binds_freeze`, and I had shown only its tail.
- `LOCAL_DELTAS.md` §Two machines attributes that exact red, on the machine with Unreal, to a stale git-ignored `library/staging/`. The library machine had **no** `library/staging/` at all, so that cause could not be the one.
- Finding the real reason (*"approval hashes != freeze record"*, Phase16's re-frozen pilot awaiting the maintainer's promote) took a **second full run** grepped for the lane. That is minutes of gate for one line.
- The dated row nearly made me record the wrong cause. The *"this file is dated, verify"* rule is what stopped it.

**Proposed fix.**
- **Method:** *"Capture the baseline run to a scratch log the first time (`… run_all.py > <scratch>/gate.log 2>&1`), then read the summary and every `[FAIL]` line from it. Never re-run the gate to read a reason."*
- **Tool (optional):** have `run_all.py`'s summary repeat each failing lane's first `[FAIL]` line. That is a build, so it is a quick-fix the lead can order, not a Refiner edit.
- **Data:** the Two machines row should say the red's cause varies by machine. On the library machine, 2026-10-14, the cause was the owed promote.

**Where it'd live.** `ToolingConventions.md` §Entry points (the scratch-log habit). `LOCAL_DELTAS.md` §Two machines (the row is stale for the library machine). Possibly `tools/validators/run_all.py`.

---

### 4 — A ruling decided the seed's dependency, but the seed still pointed at the open question it closed `[doc-gap]` *(minor)*

**Grounding.**
- The seed's §Depends on and `261014_R_MaterialPipeline.md` RD-MP-14 both say whether Thumbnails waits for a server *"is Phase17's Q-P17-7"*.
- Q-P17-7 lives in a different doc (`Future/PhaseTBD_LibraryService.md`), was closed by RD-DS-8 in a third (`261014_R_DownstreamPicture.md`), and its own heading carries the answer.
- Finding it took three reads. `discovery.md` §Where rulings live sent me looking, and that part worked.
- What made it slow: the research doc's RD-MP-14 still says *"Not decided by it … Both are Phase17's Q-P17-7"*, with no forward pointer, even though the same doc's §Status was updated that evening.

**Proposed fix.** In supersession hygiene: *"When a question closes, sweep for every sentence that DEFERS to it by id ('is Q-x's call', 'Q-x decides') and add the answer's id beside it. A deferral pointer is a restatement too."* (I did not fix RD-MP-14's line. It is another unit's doc and not my errand: §Lanes, *stay in your verb*.)

**Where it'd live.** `discovery.md` §Supersession hygiene, or `research.md`'s equivalent.

---

## Keep these

- **`.claude/CLAUDE.md`'s *"an id grep cannot see a fact — re-read every sentence you wrote from a private source"*.** It is the only thing that caught item 1's three leaks. A grep for private id patterns came back clean on text that was leaking.
- **`discovery.md`'s *"the seed is context, not authority"* and *"first — is this even YOUR fork?"*.** Phase18's seed said it *"takes over the Character subjects from Thumbnails"*, against RD-DS-7's *"Character follows Thumbnails because its per-part pictures are built on Thumbnails' rig"*. Asking which was a ruling (only RD-DS-7) closed it as RD-P17-1, with no round trip.
- **Reading the risk lane's controls instead of resembling a sibling.** Reading `run_all.py`'s globs and `build_snapshot.py`'s `MAX_ASSETS` turned the asset count into a finding (about 600 of 1000) that the build map needed anyway.
- **The capability probe on this project's own artifact.** A 5-second headless Blender call confirmed `Khronos PBR Neutral` exists and is 5.2's default. RD-P17-2 rests on it, rather than on memory of Blender versions.
- **`git show --stat` read-back.** 2 files, 236 / 21, exactly as intended, while a Refiner session held six dirty files in the same tree.

## Dead weight

None.

## Open questions

1. **For the Refiner:** item 1 is written as local. Its portable core may be *"a click on another system's surface is named by role in the phase doc; its address goes in the handback"*. Portable or local is your call.
2. **For the lead, not the Refiner:** the Brief's five calls (RD-P17-1 to -5) are closed *"unless you say otherwise"* and need nothing from this retro.
