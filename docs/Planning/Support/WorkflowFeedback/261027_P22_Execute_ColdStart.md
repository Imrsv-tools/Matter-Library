# Workflow Feedback — P22 / execute / cold start

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P22` (*Skin Maps Beyond Colour*) |
| **Mode** | `cold start` |
| **Outcome** | `derailed`: 22.1 was built end to end (the Unreal look view, the roughness map, `roughness_map` in the contract and in all three tools, the Studio ask P34), and click 1 was rejected: *"very much looks like a silicon doll"*, then *"You are wasting my time with a viewing here"*. Recorded as RD-P22-14. |
| **Shape** | `behavior-touching` |
| **Confidence** | Ran fully: the kickoff (Q-P22-2 put to the lead), BUILD for 22.1, the TRY sitting, the commit discipline. **Not exercised:** STRENGTHEN after the verdict, the close. |
| **Date** | 2026-10-27 |

---

## Items, ranked

### 1 — A look click was asked on a change the run had already measured as near-invisible `[self-error-doc-could-prevent]`

**Grounding.** The first roughness map moved the look view by **0.33 of an 8-bit level on average**. The ad-hoc-check row ("move it 10×") worked: a scratch probe showed the renderer responds (a uniform −0.13 moved the highlights up to 23 %). So the map was made about twice as strong. The re-render still differed from today's by **0.37–0.43 levels on average** (p99 7–8), and it was handed to the lead as click 1 anyway. The lead: *"Looks basically exactly the same with the working tree slighly shinier.... if you are just showing me the same thing we have today with some color shifting... yea... loks like plastig today still looks like plastic"*. The number that predicted the verdict was in hand before the sitting.

**Proposed fix.** In §TRY's *"Can the surface show it?"* paragraph, add a second question: **can the CHANGE show it?** Before calling a sitting whose click compares today with new, measure the difference in the exact pictures the lead will see. If it is below what a person would notice at a glance (a mean of under one 8-bit level here), do not call the sitting: report the number and what would have to change for a click to be worth the lead's time.

**Where it'd live.** `execute.md` §TRY (beside *"Can the surface show it?"*).

---

### 2 — Discovery put "does it still read as plastic?" on a step the evidence on file said could not answer it `[doc-gap]`

**Grounding.** `261026_R_SyntheticSkinAndEyes.md` F-SYN-1 records that the largest gain the lead has seen came from CHQ's Digital Emily skin: colour detail at skin scale, from a real person (*"WAY better"*). This phase's First human test still asked the plastic question of a procedural roughness map on today's smooth skin (click 1), and planned the same question for procedural relief and thickness (clicks 2–3). Neither the Brief nor this run named the reference the lead had already judged as skin. The lead: *"Don't ask mty why I think it look like plastic until we get to the pahses where we are actaully trying to implment the learning from emily (which clearly did not look like plastic)"*.

**Proposed fix.** In discovery's First human test: **when a click asks for a judgement the lead has already made on a reference (the best look seen so far), name that reference in the Brief, and ask whether this step is expected to close the gap toward it. If it is not, the click is not a look click:** the step is plumbing, and its evidence is the agent's own.

**Where it'd live.** `discovery.md` §First human test (and `execute.md` §TRY should honour the same when a Brief's click fails this test).

---

### 3 — After a clear negative verdict, the run theorised and asked again instead of recording and stopping `[self-error-doc-could-prevent]`

**Grounding.** After *"very much looks like a silicon doll"*, the handback offered three paragraphs on why it reads as silicone and proposed a diagnosis sheet. To the lead's next question ("is this view supposed to be the new amazing skin from the learnings we had from emily?") it answered at length, then asked whether to set up an Emily comparison. The lead: *"Don't ask mty why I think it look like plastic"*. §TRY says to transcribe the verdict verbatim, and §BUILD says a present lead is *"for seeing, not for approving"*. Neither says what to do with a verdict that rejects the step's premise.

**Proposed fix.** *"A verdict that rejects the step's premise ends the act. Record it verbatim, say in one line what it reaches (the remaining clicks that ask the same question), and stop. A theory of the cause is the next unit's discovery, not this message."*

**Where it'd live.** `execute.md` §TRY (after *"Transcribe the lead's verdict"*).

---

### 4 — A consumer ask can be filed from decided rulings before the code exists `[doc-gap]`

**Grounding.** The Brief scheduled the Studio ledger row *"as soon as `roughness_map` is in the contract"* (22.1). The lead asked at kickoff, *"Have you documented what Studio needs to do to see the new maps? I can start it on that"*. RD-P22-3 … 6 already fixed the names, shapes and maths, so P34 was written from them before any code. It needed one later edit (the date the slot landed). Filing at the end of a step would have left the platform idle for the whole of 22.1.

**Proposed fix.** In `LOCAL_DELTAS.md` §Separation (or upstream): *"A consumer ask whose names and shapes are decided rulings is filed at kickoff, marked filed-before-built, and dated as each piece lands; the consumer can build alongside."*

**Where it'd live.** `LOCAL_DELTAS.md` §Separation, or upstream `execute.md` §BUILD if portable.

---

## Keep these

- **The ad-hoc-check row's "move it 10×" / indict the instrument first** (`execute.md` §Verify). It separated "the renderer can't show it" from "the map is too timid" in one scratch launch, instead of retuning the lights.
- **Putting the doc's open lead question at kickoff** (Q-P22-2). It was answered in one click, and it changed the close (RD-P22-13).
- **A format bump that keeps the old format readable.** Job format 4 for the look view, with format 3 still read, kept the pinned v6 and every other caller working. The defaults check (Marble on the new masters vs v6) came back pixel-identical.
- **`git show --stat` after every commit.** Five commits, each reconciled against the intended file list.

## Dead weight

None.

## Open questions

*(Suggestions made in chat and not routed elsewhere. The lead ended the run with "document and /retro", and RD-P22-14 put the look question on hold, so they are parked here rather than in the phase doc.)*

- **Emily as the bar in the look view.** Rendering CHQ's Digital Emily skin locally beside today's IV and the IV synthetic draft would show how far each is from the look the lead accepts. It must never be committed (public repo, a real person's scan). The run could not find the files under `_CHQ` by name. Unsettled: whether the lead wants it, and where it lives.
- **The run's reading of "silicone"** (not measured): no detail at the viewing scale (pores under a pixel at these framings, no creases), and an even subsurface glow with nothing darkening in folds. Relevant to whichever phase implements Emily's learnings, not to this one.
- **RD-P22-14's reach** (recorded in the phase doc as open): whether clicks 2–3 survive, and the order of this phase against *Synthetic Skin Sets*.
- **P34 needs a push** before the platform can rebuild its masters from `build_masters.py` with the roughness slot. Nothing is pushed.
- **Scope alarm:** click 1 came after about 400k of context. The look view, the maker, the contract and three-tool wiring all preceded it, with the lead away. The supporting work displaced the first look; a single Unreal-only roughness render on the existing look view would have answered the lead's question at a fraction of the cost.
