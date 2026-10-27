# Workflow Feedback — P22 / execute / resume

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P22` (*Skin Maps Beyond Colour*) |
| **Mode** | `resume` (the session the lead launched with *"LAUNCH A SESSION AND KEEP WORKING!"*). A distinct run from `261027_P22_Execute_ColdStart.md`, not a continuation of it. |
| **Outcome** | `done` for this run's act: 22.2 built (`e68e358`), click 2 sat: *"Better!... The shine is still just really over the top. buit we are getting there."* |
| **Shape** | `behavior-touching` |
| **Confidence** | Ran fully: BUILD (contract and three-tool wiring, the maker, a master change), the measured TRY, the commit discipline, the handoff. **Not exercised:** 22.3, the close. |
| **Date** | 2026-10-27 |

Step 0 was done in full: click 2's verdict (`c55f3b1`) and the Resume (`89eedca`) are in the phase doc.

---

## Items, ranked

### 1 — The largest cause of the plastic look was a master default, which no map could reach, and neither the Brief nor the research named it `[doc-gap]`

**Grounding.** With strong normal and cavity maps in, the look view still showed one smooth gloss over the relief. The coat (0.1 at roughness 0.3) sat on OpenPBR's default coat normal, the mesh's geometric one. By the numbers its peak was about as bright as the skin's own highlight and narrower, and it ignored every map. Wiring `geometry_coat_normal` to the article's normal (RD-P22-15) was the step that made the highlights break into texture. The phase was framed as "maps beyond colour", and the Brief's levers were all inputs. LCDSchema even states the coat sits on the geometry normal, as a fact rather than a lever.

**Proposed fix.** In discovery's First human test, or in the reuse check, for a look fault of the "sheen / plastic / glossy" kind: **list every specular lobe the master draws and which normal and roughness each one reads.** A lobe the phase's inputs cannot reach is either in scope or named as a Not-now with its reason. Separately, a learning: *a coat on the geometric normal glazes any relief underneath it.*

**Where it'd live.** `discovery.md` §The reuse check (portable). The learning goes in `docs/Learnings/MaterialX/` (local).

---

### 2 — The first relief was made at a strength that could not show, again, one step after the same lesson `[self-error-doc-could-prevent]`

**Grounding.** 22.1's map was too timid (a third of an 8-bit level). 22.2's first normal map then came out at XY RMS 0.016, about 1° of tilt, against 0.15 for the tiling pores layer it is added to. That number was in the maker's own output before any render. It took two more rounds (×2.5, then the coat) to reach a visible change. The comparison that predicts "too weak" is free: the new map against the layer it joins.

**Proposed fix.** In `execute.md` §Verify's ad-hoc-check row (*"move it 10×"*), add: **a map that is combined with an existing one is measured against it first**, by the same statistic (normal XY RMS against XY RMS, a roughness offset's spread against the base's spread). If it is an order of magnitude below, it cannot show; scale it before rendering.

**Where it'd live.** `execute.md` §Verify (portable). It could also be a maker convention in this repo.

---

### 3 — After answering the lead's informational question, the run ended on a question the Resume had already answered `[self-error-doc-could-prevent]`

**Grounding.** The lead interrupted a search: *"Hold on... what are the steps in this pahse ans what are we testing?"*. The answer laid out the steps, then asked *"Should I go ahead on that route, or do you want the phase's steps changed first?"*. The Resume said in so many words *"Decide the technical route yourself"*, and memory carries "decide, don't ask". The lead: *"Just carry on... we have to trust the process. … do the work and then we will test it."*

**Proposed fix.** In §BUILD's *"A PRESENT LEAD IS FOR SEEING, NOT FOR APPROVING"*: **an informational question from the lead is not a fork.** Answer it, state what you are doing next, and keep going. End with the plan, not with a question.

**Where it'd live.** `execute.md` §BUILD (portable).

---

### 4 — "Measure before the sitting" measured visibility, not direction, and the verdict was about direction `[doc-gap]`

**Grounding.** Per the ColdStart retro's item 1, the run measured the look sheet before calling click 2: mean change 1.1 and 3.2 levels against click 1's 0.4, plus a fine-detail contrast. That correctly predicted *"Better!"*. It said nothing about whether the shine was right, and the verdict was *"the shine is still just really over the top"*. The sheet has no column a person has already judged as skin (CHQ's Emily), so the agent could not measure distance to the bar, only distance from today.

**Proposed fix.** When the Brief names a reference the lead has accepted (the ColdStart retro's item 2), the measurement before a sitting reports the change against today **and** the remaining gap to that reference on the same statistic. Here that would be specular energy and highlight size on the face. When the reference cannot be shown (a private scan), say so and give the statistic anyway.

**Where it'd live.** `execute.md` §TRY, beside the ColdStart retro's proposed *"can the CHANGE show it?"* (portable).

---

## Keep these

- **The ColdStart retro's item 1, applied:** the look sheet was measured before the sitting (0.4 → 1.1 / 3.2 levels). The verdict moved from *"silicon doll"* to *"Better!"*.
- **A column per lever, instead of asking the lead why it looks wrong:** today | the shipped colour + maps | the synthetic colour + maps (`look.py --also`). It separated the shine maps' share from the colour's.
- **The fastest proving loop, found first:** the maker runs in ~30–90 s, a map change needs no Unreal rebuild, and a scratch relight of the atlas showed the pattern before any render.
- **`LOCAL_DELTAS.md`'s "ask once for the whole batch"** when Studio was on the GPU. One question, answered *"Carry on"*, covered every launch.
- **`git show --stat` read-back:** 27 files / 840 insertions, reconciled against the intended set.

## Dead weight

None.

## Open questions

- **The look sheet's measurement lives in a scratch script** (`$CLAUDE_JOB_DIR/tmp/measure.py`: mean change and fine-detail contrast on the skin, per view). If the next sittings rely on it, it belongs in `look.py` (a quick fix), so the numbers land beside the sheet.
- **Studio's side of RD-P22-15:** P34 now asks the plugin to set `coat_follows_normal = 1`. Whether the platform's Unreal master build carries the switch depends on it re-running `build_masters.py`, which needs a push.
- **Context:** the run reached ~400k at click 2, the attention ceiling. 22.3 and the shine pass are a fresh session's (Resume, `89eedca`).
