# Workflow Feedback — MasterAdoption / Research → Quick Fix / Cold start (second deposit)

| | |
|---|---|
| **Verb** | `research → quick-fix` (four more quick fixes and two research passes, all at the lead's direction) |
| **Unit** | research slugs `MasterAdoption` and `ThinGlass` (`261005_R_PlatformMasterAdoptionAsks.md` Passes 7 – 8; `261005_R_PlatformThinGlassAsks.md` Pass 3; ledger rows M6, M7, P23; issue #2) |
| **Mode** | cold start, continued after a first `/retro` |
| **Outcome** | done — a consumer's report of a broken conformance check reproduced, repaired and proven here (`c7b963e`, issue #2 closed); `build.sh` made to fail when the builder does (`7e33015`); two scripts marked executable (`c48fb98`); the rig's side view and the Blender driver's device test (`71d1233`). All pushed at the lead's word |
| **Shape** | behavior-touching |
| **Confidence** | Ran fully: `/research` (two passes), `/quick-fix` (four, one closing an issue), `/retro`. **Not run by this session:** anything in Unreal. Item 2 leans on what the library's other machine reported back in the shared research doc (its Pass 9), which this session read and did not reproduce |
| **Date** | deposited 2026-10-11; the work is of 2026-10-05 |

**This CONTINUES `261005_MasterAdoption_ResearchQuickFix_ColdStart.md`**, which was still in the inbox, undrained, when this was written. The lead reopened the session four times after that file's terminator. Nothing below restates it: item 2 adds evidence to its item 2 and says so. `_RefinementBacklog.md` was read first (last changed 2026-09-27).

---

## Items, ranked

### 1 — A check that cannot START was carried as "the same red before and after" by every phase since Phase05, and hid a break a consumer found `[doc-gap]`

**Grounding.** `tools/conformance/check_exporter.sh` runs the carrier check on four real exports and its self-test. All five lines died at one import from before Phase05 (issue #2: the check's Python has no MaterialX). Each phase since followed `LOCAL_DELTAS.md`'s *"baseline BEFORE you edit"* and `execute.md`'s *"compare the SET, not the tally"*, found the same five red lines before and after, and recorded them as inherited. Phase12's log: *"five carrier checks that all stop at one import"*. Phase12 then added three Creator ports named as OpenPBR's own inputs. USD puts those names on every Material, so the check, had it run, would have refused every asset. It could not run. The platform's gate, whose Python does have MaterialX, hit it within hours and worked around it. Repaired here in one sitting once looked at: 62 passes and FAIL became 66 and PASS.

Both rules were followed correctly, and that is the gap: *"the same red set"* treats a check that **ran and refused** and a check that **never started** as one thing. The second is missing coverage. And the missing coverage was exactly Phase12's subject: its Brief read the carrier rule and listed the check's file under controls.

**Proposed fix.**
- In the baseline rule: *"Sort the red set in two: checks that RAN and failed, and checks that could NOT START (an import error, a missing tool). A check that cannot start is absent coverage, not an inherited failure. Name what it would have covered."*
- In the Brief's risk lane: *"If a control you list cannot start on this machine, the phase either repairs it first or says, in the lane, which claim nobody is checking."*
- A tally in the handback while it lasts: *"N checks cannot start (since <phase>)"*, so the number is in front of the lead at every close instead of in a log.

**Where it'd live.** `execute.md` (the baseline and compare-the-set rules) and `discovery.md` (the risk lane): portable. `LOCAL_DELTAS.md` RUN row for the local wording.

---

### 2 — A stand-in encodes one report of how the absent system behaves; the real system behaved another way `[doc-gap]` *(adds to item 2 of the file this continues)*

**Grounding.** The platform reported that Unreal's commandlet exits 0 even when the builder's script raised. This session, with no Unreal, changed `unreal/build.sh` to read the builder's own result line, and tried it against a stand-in engine in three cases built from that report. On the library's machine with Unreal the same refusal made the commandlet exit **255**. So the script stopped at its `pipefail`, never reached the new check, printed no message and left its temporary log behind (the research doc's MA-R20). It still failed, which is why nobody was hurt; the other machine then rebuilt it to take both routes.

The first deposit's item 2 asks for a verify branch for *"this machine cannot run the thing"* and says a stand-in *"proves what your code asks for"*. This is the sharper half: the stand-in was faithful to **one machine's report**, and the code was written to that report alone.

**Proposed fix.** Add to that branch: *"A stand-in for an absent system is built from somebody's report of it. List the behaviours the report does NOT settle (the exit code, the output stream, what a failure looks like) and give the stand-in a case for each, including the opposite of what was reported. Code that handles only the reported behaviour is tested against an echo."*

**Where it'd live.** `quick-fix.md` step 4, with the first deposit's item 2.

---

### 3 — A research doc two sides write into has no owner for its Status footer `[doc-gap]`

**Grounding.** `261005_R_PlatformMasterAdoptionAsks.md` reached ten passes in a day from three writers: the platform's session, this session, and the library's session on its machine with Unreal. Each side kept the courtesy the platform stated when it first appended: *"the lines above are the library's and are not edited"*. So the footer became a log. It now carries ten *"Pass N"* bullets under prose bullets that still say *"Pushed … up to `a66377c`"* and list *"what was added"* as of Pass 4. `research.md` says a pass is not finished until the footer is reconciled, and calls a stale footer *"the worst place in the doc for a stale claim"*; it assumes one author. This session rewrote its own bullets twice and left the others, which is half a reconcile.

**Proposed fix.** For a doc more than one side writes: *"The passes belong to whoever wrote them and are not edited by the other side. The Status footer belongs to the doc: whoever closes a pass REWRITES its state lines (direction, asks, open questions, next) and keeps one line per pass below them, saying whose it was. Not editing the other side's lines is a rule for passes, never for the footer."*

**Where it'd live.** `research.md` §The research discipline (portable), and the inbound-ask paragraph the first deposit's item 5 proposes for `LOCAL_DELTAS.md`.

---

### 4 — `/retro` is terminal, and the lead reopened the session four times after it `[doc-gap]`

**Grounding.** The first deposit ended with the terminator. The lead's next message was *"Please pull to get more feedback and insight from the IMRSV project"*, and three more instructions followed, ending in this second `/retro`. `retro.md` says *"THEN STOP. NO FURTHER ACTIONS"* and that the terminator shows *"this agent is complete"*. It does not say what a new instruction after it means, or that the next `/retro` is a `_2`. This session carried on without a word about it, which was right and was a guess.

**Proposed fix.** One line under §`/retro` IS TERMINAL: *"The terminator ends the agent's own initiative, not the lead's. A new instruction after it reopens the session: say so in one line, do the work in its verb, and the next `/retro` is a `_2` that continues the first file."*

**Where it'd live.** `retro.md`.

---

### 5 — The rig has no baseline rule and no home for scratch, and its scratch is large `[doc-gap]`

**Grounding.** `LOCAL_DELTAS.md` tells a change under `tools/conformance/` to baseline `check_exporter.sh` first; that rule is what made item 1's repair provable. A change under `tools/parity/` has no such rule. This session baselined two articles' pictures by choice, before adding a view and changing the Blender driver, and the comparison was strong: Storm's and Unreal's pictures came out the same bytes, Blender's within one 8-bit code. It put that baseline under `/tmp`. One article's defaults are about 290 MB with two views and 430 MB with three, nearly all of it the Unreal driver's raw float captures, and the machine's `/tmp` has a user quota. The second run died with exit 120 and an unrelated-looking *"pwd: write error: Disk quota exceeded"* on every later command until scratch was cleared.

**Proposed fix.** In the RUN row: *"A change under `tools/parity/` baselines one article first (`rig.py <article> --out <scratch>`), and afterwards compares the pictures of every view that was not meant to change, by bytes for Storm and Unreal. Rig scratch goes on the home disk, never `/tmp`: one article is hundreds of megabytes."*

**Where it'd live.** `LOCAL_DELTAS.md`, the RUN row (local).

---

### 6 — A push the lead ordered up front lands a visible change before the lead has looked `[doc-gap]`

**Grounding.** `quick-fix.md` step 4, for a user-observable change: *"The lead's verdict that it's fixed … is the gate"*, and *"don't commit until it confirms the whole ask"*. The lead's instruction for the rig's new view was *"yes, do 1 and 2 and push"*. The view is something a person looks at. It was committed and pushed on the agent's own look, and the docs say so in those words (*"looked at by the agent, the lead's look not yet taken"*). The gate's fifth verdict (*"the lead already routed it here"*) covers entering the verb; nothing covers the lead ordering the push before there is anything to look at.

**Proposed fix.** In step 4: *"If the lead has already said to commit or push, the look is owed, not waived. Say whose eyes have been on it in the commit and in the doc, and carry the lead's look as the first line of `Next` until it is taken."*

**Where it'd live.** `quick-fix.md` step 4.

---

## Keep these

- **`LOCAL_DELTAS.md` "baseline `check_exporter.sh` BEFORE you edit"** — the repair of item 1 is provable only because the before-log existed: five lines changed, and no other.
- **`execute.md` "a comparison whose sides cannot differ agrees by construction"** — the repaired self-test was run against the old rule as a control, and 12 of its 23 checks failed. Without that, 23 passes would have shown nothing.
- **`quick-fix.md` §When the Quick Fix came from an Issue** — the `✅ Issue #2` subject with `Closes #2`, then a comment that stands alone. The push closed it; the comment carries the cause.
- **`research.md` "park, and lead with the one-sitting offer"** — asked *"should we do anything?"*, the run answered, reproduced the fault, parked a pass and offered one command. The lead's reply was one line. Building a contract-adjacent repair on a question would have been a slide.
- **The retro as the channel to a live run** (`retro.md` §TERMINAL, the *"no channel"* paragraph) — the two corrections the first deposit left for the Phase12 session were picked up and landed by it the same hour.
- **`.claude/CLAUDE.md` §Git, push by value** — every push in this session named its own last commit, on a trunk where another session and another machine were also pushing.

## Dead weight

- **`quick-fix.md` §from an Issue, step 4, "remove the workflow `status:*` label"** — this repo's issues carry no labels. One wasted look.

## Open questions

1. **[lead]** The look at the rig's side view is owed (`library/parity/Diamond_Brilliant_Clean_Base_s01_v01/sheet.png`, the last picture of each setting).
2. **[lead]** Does item 1's finding change how the still-dormant CI is weighed? A gate that ran on a machine with both modules would have caught Phase12's break at the commit. That is a product decision already on the backlog as a lead ruling; this is one more data point for it.
3. **[refiner]** Items 1 and 2 here and items 2 and 6 of the first deposit are one theme from four sides: **a claim was recorded as checked when the check could not see it** (a dead check, a stand-in, a stale footer, an unrun build). The backlog's recurring theme *"an instrument that cannot see the thing"* may be the home for all four.
