# Workflow Feedback — P19 / execute / resume → close

| | |
|---|---|
| **Verb** | `execute`: a resume run, then the close (stage 5) in the same session, on the lead's *"close"* and *"push"* |
| **Unit** | `P19` (Scale Grids) |
| **Mode** | resume run 2, then close. **A distinct run, not a continuation** of `261015_P19_DiscoveryExecute_Resume.md`, which covered the earlier session (clicks 1–3). This file does not repeat its four items. |
| **Outcome** | done. 19.2's tail, 19.3 and 19.4 landed; clicks 4 and 5 passed; the drag owed from click 1 led to the lead's RD-P19-4; 19.1's tail landed; the phase closed (`99a44f3`) and was pushed |
| **Shape** | behavior-touching |
| **Confidence** | Ran fully: execute BUILD / TRY (one sitting, clicks 4 and 5 plus the drag), STRENGTHEN, and the whole close (A⁻ to E). **Not exercised:** the high-rigor lane, the repair ladder, the issue-close coda (no source issue). |
| **Date** | 2026-10-15 |

---

## Items, ranked

### 1 — `LOCAL_DELTAS.md` says the library machine cannot run anything under `unreal/`, but the rig's Unreal column ran here all session `[doc-gap]`

**Grounding.**
- `LOCAL_DELTAS.md` §Two machines, on the library machine: *"cannot | run anything under `unreal/` — a change there is built, not run"*. Phase19's Brief inherited it: *"The Unreal column comes from the machine with Unreal when it next runs the rig"*.
- This run, on the library machine (no Unreal install at any path), `uv run tools/parity/rig.py …` wrote `unreal/defaults.png` for every view: the character scale view and all seven grids. Each run printed `unreal: wrote …`.
- `docs/ToolingConventions.md` already says why: *"The Unreal column comes from the pinned runtime, downloaded once (no Unreal install needed)"*.
- So the row conflates **building** under `unreal/` (needs Unreal 5.8) with **running** the published runtime (does not).
- It cost one corrected fact in the phase doc, and a wrong *"not run here"* expectation in the Brief.

**Proposed fix.** Split the cell. **cannot:** build or publish anything under `unreal/` (a change there is built, not run). **can:** run the rig's Unreal column from the pinned runtime (`unreal/RUNTIME.json`; measured 2026-10-15, Phase19).

**Where it'd live.** `LOCAL_DELTAS.md` §Two machines (port gap, local).

---

### 2 — A click's surface was checked for which TOOLS run there, not for whether the thing judged is big enough in pixels to see `[self-error-doc-could-prevent]`

**Grounding.**
- The Brief's *"Each click's surface can show what it judges"* gave click 1 a number (*"about 1,000 px across the cube's face, so the 10 cm and 1 cm lines resolve"*). Click 4 got only *"Storm and Blender run here"*.
- The first scale-view sheet was a grey haze on every skin and cloth part. A grid's lines are a fixed fraction of its tile (the edge is 12 of 4,096 px), and the 1 cm tile was about 3 px whole-body and 14 px on the face.
- `execute.md` §TRY (*"ask whether the surface … can SHOW the thing the click is about"*) caught it before the lead saw it. The fix was five 3 cm swatch cameras, two re-renders and a rebuilt scene: about 15 minutes that discovery could have priced.

**Proposed fix.** In discovery's *First human test*: *"For each click, answer 'can the surface show it' with a NUMBER: the size in pixels of the smallest feature judged, at that click's camera and resolution. 'The tool runs here' answers a different question."*

**Where it'd live.** `discovery.md` §The Brief, *First human test*. It is portable.

---

### 3 — An either/or question in a handback got a bare "ok", and the reading rode into the 🎉 commit unconfirmed `[self-error-doc-could-prevent]`

**Grounding.**
- The handback asked: *"Keep the rule as it is, or give the big grids a different view?"* The lead answered *"ok"*, which picks neither option.
- The run recorded it as a reading, *"to confirm at the close"*. The next message from the lead was *"close"*, so the reading was never confirmed. It went into the 🎉 body as `ALREADY ROUTED`, quoted beside the question.
- That is compliant (row A0's guard makes it overturnable), but it rests on an interpretation.

**Proposed fix.** In the handback beats: *"Put a question to the lead as ONE default and its alternative ('I'll keep the rule unless you say change it'), never as A-or-B. Then a bare 'ok' has one meaning."*

**Where it'd live.** `AI_WorkingAgreement.md` §Working With the Lead (the handback's question form). It is portable.

---

### 4 — A product fork put as four mechanisms confused the lead, who had to ask which option he was describing; the second ask, framed by what he'd see, landed at once `[self-error-doc-could-prevent]`

**Grounding.**
- The first `AskUserQuestion` on *"what should a dragged grid do?"* offered four mechanisms: keep, drop keeps the slot's size, drop measures the mesh, UVs in metres.
- The lead answered in prose: *"I am not sure which one would do what I would LOVE to see ... so I think "1" is wht you are saying? ... so I guess it needs to be manual?"*. His wish was in fact option 4.
- A short text explanation came next: what each convention means for a builder, with *"If you put a .1 material on a 1m object"* as the example. A second, two-option question followed, and he answered in one click: *"1 now, 4 as a next phase"*.

**Proposed fix.** In `execute.md` §Divergence, *"A genuine PRODUCT/UX choice … Batch them and ask"*: *"Frame each option by what the person will SEE or DO, in one sentence each, and state their goal in their words above the options. A list of mechanisms makes them reverse-engineer the outcome."*

**Where it'd live.** `execute.md` §Divergence. It is portable.

---

### 5 — `.claude/CLAUDE.md` §Codebase search assumes a Grep/Glob tool; this session had none `[doc-gap]`

**Grounding.** The run's first message named *"the session's Read/Grep/Glob tools"* as the search mode, per the rule. The first Grep call failed with *"No such tool available: Grep. Grep is not available in this session — search file contents with `grep` via the Bash tool instead"*. The run then said it was switching to the single-statement `grep -n` fallback. The rule's fallback covers the case, but the first-message declaration cannot know the tool set without trying.

**Proposed fix.** *"Name the search mode after checking the tool list (Grep/Glob present or not), not by assumption."* Or a one-line note that some harness builds ship without them.

**Where it'd live.** `.claude/CLAUDE.md` §Codebase search. Unsure whether portable: it depends on the harness.

---

## Keep these

- **`execute.md` §TRY, "ask whether the surface can SHOW it".** It caught the 1 cm haze before the sitting (item 2), and the lead judged swatches that worked.
- **`execute_close.md` row B's `git mv` warning.** The staged rename showed `0 insertions`, the pre-finalize blob. A pathspec commit naming both paths carried the finalize, and `git grep "COMPLETE (closed" <sha>` confirmed it in the commit.
- **Row B, "grep the tree for the old path".** It found five inbound links, including Phase15's `../Phase19_ScaleGrids.md`: the inverse case, correct before the move and wrong after.
- **The filtered stage (`.claude/CLAUDE.md` §Git).** One hunk of `/matter-generate`'s `SKILL.md` committed beside a sibling's two uncommitted hunks, which stayed in the tree.
- **"Read what selects a gate's subject".** `assert_profile.py`'s portable check took `ids[0]` only; the golden's second identity would have gone unchecked. Widened at 19.4.
- **"Confirm an ad-hoc check can fail".** The importer's size line was run on 0.8 m and 3 m (refused) as well as 1 m and 0.1 m.
- **Measure before diagnosing, on a lead observation.** The lead's *"UE looks much more warped"* became a table of `st` magnitudes per swatch that fits the hypothesis (the cheek is the only one over 128), and an issue with a test (Matter-Library#5), not a guess in a commit.

## Dead weight

None.

## Open questions

1. **The ruler check (F-P19-10)** cannot measure periodic or unresolved patterns, and a grid is both. Is that worth a line in the rig's scorecard (*"advisory for a diagnostic grid"*), or is the phase finding enough? This is the lead's or the next rig phase's call, not the Refiner's.
2. **The `s100` thumbnail.** The lead's *"ok"* (item 3) was read as keep the rule. If he meant "change it", it is a small follow-up on `showcase.subject_for` for `utility/virtual`.
