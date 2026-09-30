# Workflow Feedback — P06 / P09 / execute (close) → discovery → execute

| | |
|---|---|
| **Verb** | `execute` (P06 resume run 5 + `execute_close`) → `discovery` (P09 Pass 3) → `execute` (P09 run 1). One session, three verbs, all lead-invoked in turn; one file, because the grounding runs across them. **Not** a continuation of `260930_P06_Execute_Resume4Close.md` (that was run 4, on the other machine). |
| **Unit** | `P06` (close), `P09` (Pass 3, then 9.1–9.2) |
| **Mode** | P06: resume run 5 → close · P09: discovery resume · P09 execute cold start → suspend-handoff at ~400k |
| **Outcome** | P06 closed and pushed (`1f633df`); P09 Brief re-checked against Phase06 (pushed `a093d9e`); P09 9.1 ✅ (clicks 1–2), 9.2 ✅ (clicks 3–4), 5 commits unpushed at handoff (`dfd89d5`…`23f25ad`), 9.3 owed on the UE machine |
| **Shape** | behavior-touching (assembler, Blender loader, the rig's drivers, the fit-set tool, two articles) + docs |
| **Confidence** | Ran fully: the P06 close rows A⁻–E, a discovery pass, two execute steps with four lead sittings in Blender and on sheets. **Not exercised:** the UE machine, any Unreal build or publish, 9.3. |
| **Date** | 2026-09-30 |

Step 0: the handoff state (Execution Log, Resume block, every click verdict) was committed before this file (`23f25ad`); every finding raised in chat was written to the phase doc as it arose. Nothing from chat is un-routed.

---

## Items, ranked

### 1 — A viewer opened for a sitting as a harness background task is killed at the 2-hour limit, mid-sitting `[doc-gap]`

**Grounding.** The lead's Blender was not running with its MCP server, so each sitting was built headless as a `.blend` and opened with `blender /tmp/p09_eyes_sitting.blend` via `run_in_background` (max timeout, 7,200,000 ms). The eyes sitting sat unjudged across the lead's break; the harness killed it at 2 h ("stopped after reaching its background time limit"), and its own note says not to restart a task that already had the maximum. The lead had to type *"open it"* to get the viewer back. `execute.md` §TRY says to hand back *"the running tool opened on it"*, and `LOCAL_DELTAS.md`'s artifact row says to open the viewer, but neither says how to launch one that outlives the harness's task limit.

**Proposed fix.** In `LOCAL_DELTAS.md`'s *"artifact a person reaches"* row (or wherever the viewer launch is named): *"Launch the lead's viewer (Blender, USDLiveView) DETACHED from the session (`setsid blender <file> &` or the desktop's opener, `xdg-open`), never as a `run_in_background` task: a harness task is killed at its time limit, and a sitting can outlast it."*

**Where it'd live.** `LOCAL_DELTAS.md` (the viewer launch is project-specific); possibly `execute.md` §TRY if upstream wants the general form.

---

### 2 — I asked the lead to navigate a 3D viewport; he answered *"how do I do that?"* `[self-error-doc-could-prevent]`

**Grounding.** At click 1's second look (matte hair applied live), the handback's `▶` read *"Orbit the black and auburn heads in the Blender window"*. The lead: *"how do I do that?"*. I then framed the two heads myself through the MCP (`region_3d.view_location / view_rotation / view_distance`), and his next message was the verdict (*"OH! You did it!"*). `execute.md` §TRY already says the lead's part is to USE and JUDGE and that a machine-checkable click is the agent's, but framing a 3D view reads as "using" it, so the rule did not fire.

**Proposed fix.** In `execute.md` §TRY, beside *"A click that is machine-checkable, or is only typing a command, is yours"*: *"So is NAVIGATION: frame the view the judgement needs (camera, zoom, the part in question) before handing over. Never ask the lead to orbit, pan or zoom a viewer to reach the thing being judged."*

**Where it'd live.** `execute.md` §TRY.

---

### 3 — I carried a lead's side remark as an open `YOUR CALL` across two handbacks `[self-error-doc-could-prevent]`

**Grounding.** At P06 click 5 the lead said Unreal *"should make humans look WAY better"*. Run 4 filed it as a `YOUR CALL` (*"its home is the lead's call"*). I carried it into the P06 close handback, and again into its "still open" line. The lead: *"Stop asking about humans at thier besst... it was a side comment...."* A remark that did not ask for anything became an open decision by being written down once, then was re-asked because it was open.

**Proposed fix.** In `AI_WorkingAgreement.md` §Working With the Lead (the `YOUR CALL` entry gate): *"A lead's remark is not a decision request. If you are unsure whether it asks for something, ask ONCE; if the lead does not take it up, record it as a remark in the phase doc and drop it from `YOUR CALL`. Never carry an unanswered item into a second handback."*

**Where it'd live.** `AI_WorkingAgreement.md` §Working With the Lead.

---

### 4 — Verifying a sitting file by rendering it before opening it caught two defects the lead would otherwise have met `[doc-gap]`

**Grounding.** The first hair sitting, rendered headless before opening, came back **magenta**: importing a second USD (the `bob01` variant) into the scene writes that file's dome INTO the current scene's world, in place, so restoring the world pointer did not help; the nodes had to be stripped. The same check caught the camera too close. The eyes sitting's render caught a blown-out key light. None of this is in `execute.md`: the Verify row says *"Load it the way they will: a browser"*, which a run can read as satisfied by opening the file.

**Proposed fix.** In `execute.md` §Verify, the *"something a person sees"* row: *"For a viewer sitting, render the exact view you will hand over (headless) and LOOK at it before opening it for the lead."* Plus a learning: *Blender's USD importer, importing into a scene that already has a world, writes the imported dome into THAT world's node tree; strip it after the import, not by resetting `scene.world`.*

**Where it'd live.** `execute.md` §Verify; `docs/Learnings/Blender/` (the importer behaviour).

---

### 5 — A per-view file named `<id><suffix>` collided with the scene because one suffix is empty `[doc-gap]`

**Grounding.** Hiding the cornea in every view (9.2) made the Storm driver write the wide view's hide layer to `<id><suffix>.usda` = `defaults.usda`, **the setting scene itself**, as a layer sublayering itself. Blender then found no camera (*"camera '/World/Cam' not found after import"*), after a USD warning about a sublayer cycle. The scheme held since Phase05 only because the mouth view (suffix `__mouth`) ever hid anything. Fixed: `…__view.usda` (`ca7929f`).

**Proposed fix.** A learning, not a method rule: *"The parity rig's wide view has an EMPTY suffix. Any per-view artefact named `<id><suffix>` collides with the setting's own file for it; give per-view artefacts a name of their own."*

**Where it'd live.** `docs/Learnings/Storm/` (or a rig learning, if the domain list gains one).

---

### 6 — The `cd` ban was broken once, by reflex, in a throwaway read `[self-error-doc-could-prevent]`

**Grounding.** Reading the three eye recipes, I ran `cd …/recipes && python3 -c …`, which moved the session's working directory; the harness reported *"Primary working directory: …/recipes (was …)"*. `.claude/CLAUDE.md` and `execute.md` rule 2 both forbid `cd`. The rule was known and simply not applied to a "quick look". No doc change proposed: the rule is clear; recorded so the Refiner can see whether it recurs.

**Where it'd live.** n/a (a recurrence counter, if the Refiner keeps one).

---

## Keep these

- **Applying a proposed material change LIVE in the lead's Blender (MCP) before touching the recipe.** The hair specular (click 1) and the eye coat (click 3) were each judged in seconds on the real surface; only a verdict reached the article. Two sittings, two correct changes, no rework commits.
- **Adding sitting lights, and saying so** (P06 retro item 3, applied): a back light for hair and a small key light for the eyes' catchlight, each named in the handback as "added, not the rig's light". The lead judged the right thing both times.
- **Discovery reading the SELECTOR, not the assertion** (`execute.md` §Verify, gate row): Pass 3 read `article_material`'s refusal and `rig.run_unreal`, and found that 9.1 as planned would silently blank the character's whole Unreal column. The exact v1 bridge kept three columns on every sheet through 9.1–9.2.
- **Act by act with a present lead:** four clicks in one run, each fixed and re-judged before the next began.
- **Reading the Unreal job's own material JSON** to localise the white Unreal eye (the picture reached `base_color_tex`; the diffuse followed `subsurface_color`), rather than hypothesising.

## Dead weight

None.

## Open questions

1. **Lead:** the 5 P09 commits are unpushed at handoff; the UE machine cannot start 9.3 until they are pushed (asked in the handback).
2. **Refiner:** item 1's fix depends on how the lead wants viewers launched on this desktop (detached process vs `xdg-open`); unverified which survives the session ending.
