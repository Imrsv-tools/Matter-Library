# Workflow Feedback — P19 / discovery → execute / resume

| | |
|---|---|
| **Verb** | `discovery → execute`, one session: discovery Pass 2 (a re-verify of a Brief written as Phase15), then `/execute P19` through clicks 1–3 |
| **Unit** | `P19` (Scale Grids) |
| **Mode** | resume (discovery Pass 2), then execute cold start; suspended at an act boundary (context) |
| **Outcome** | suspended. Clicks 1–3 passed: the grids (after two failed scenes and a lead ruling on the look), and the scale view on and off in the lead's Blender. 19.1 and 19.2 have tail work, and 19.3 and 19.4 are not started; the Resume block lists them |
| **Shape** | behavior-touching |
| **Confidence** | Ran fully: discovery Pass 2, execute BUILD, TRY (three sittings) and the Resume. **Not exercised:** STRENGTHEN beyond the sittings, and the close. |
| **Date** | 2026-10-15 |

---

## Items, ranked

### 1 — A Brief's design decision rested on the agent's reading of an ambiguous lead quote; it was never put to the lead as a reading, and click 1 failed twice on it `[self-error-doc-could-prevent]`

**Grounding.** RD-SP-4 quotes the lead: *"if each scale had that is its base then someting like 4 thicknessed of grid"*. Pass 1 read *"its base"* as **a background in the tile's colour**, recorded the choice as D-2/D-3 under *"Closed at this discovery (the agent's call)"*, and added a test of its own: *"from across the room each grid still reads as its own background colour"*. Pass 2 re-verified the Brief against the tree and never questioned the reading. A sketch shown to the lead mid-discovery carried the coloured backgrounds; the lead's *"gotcha ok"* was taken as agreement. At execute, the run spent a measured tuning pass making each grid's far colour stay within 11° of its own hue. At click 1 the lead: *"these are a bunch of different colored squares and I see not relation of grid size between them"*. After a checker variant: *"NO! NO NO... you are not understnding the assignment... Gridliines have colors... that is all... we are making a check grid validataion and I keep seeing colored squares"* (RD-P19-3). A whole rule, a palette rationale and a tuning pass were spent on a requirement the agent had invented.

**Proposed fix.** In discovery's Brief: *"A decision the agent closes by READING an ambiguous lead quote (not by a spec, a measurement or a peer) is a reading, not a decision. List it in the handback in plain words, the reading beside the quote ('I read "its base" as the background colour'), so the lead can strike it in one line. A picture that embodies the reading does not count as putting it: a lead approves the picture's gist, not each property in it."*

**Where it'd live.** `discovery.md` §Forking to the lead (test 1, *ANSWERED?*) or §The Brief's *Decisions that bind*.

---

### 2 — Click 1 tested the grids' look in isolation, never the phase's purpose; the lead could not tell what to judge `[self-error-doc-could-prevent]`

**Grounding.** The Brief's click 1 asked the lead to judge, among other things, *"the same length is the same colour in every grid; the four line levels read up close; from across the room each grid still reads as its own background colour"*. These are properties of the textures. The Outcome is about **objects whose UV scale is right or wrong**. The lead, at the sitting: *"I am not sure what I should be judging here... it does not solve what I am trying to achieve"*. Then he designed the click himself: *"there is a 10 meter square with a 10 meter material ... then a 1 meter square next to it ... the square exampel needs to change so we are seeing it scale down"*. Click 2 (planted errors on real objects) is what made it land: *"HA! COOL! This is amazing!"*.

**Proposed fix.** In discovery's *First human test*: *"For each click, write the one sentence the lead will be able to SAY afterwards about the Outcome ('the copper box's UVs are 10× too big'). A click whose answer is a judgement about a component's appearance, not about the Outcome, is preparation for a click, not a click: merge it into the first click that answers the Outcome, or show it as a sketch."*

**Where it'd live.** `discovery.md` §The Brief, *First human test*.

---

### 3 — Driving the lead's live Blender by script: three traps found only by screenshot, one of which crashed it `[doc-gap]`

**Grounding.** The run built a viewer `.blend` with workspace tabs, one per view, then fixed it live through the Blender MCP:
- the factory *Texture Paint* workspace opened in **paint mode**, with half the window an image editor, so a click could have painted on the scene;
- `bpy.ops.workspace.duplicate()` from a script, then a rename, **crashed the lead's Blender** (*"Couldn't find layout in this workspace"*). Only a scratch file was open;
- camera view would not frame from a script (`view_camera_zoom`, and `view_center_camera` failed its poll). A perspective view copied from the camera worked, with the viewport lens doubled.

Recorded in the phase's Resume block as *learnings owed at the close*.

**Proposed fix.** The five lines in the Resume block, as `B19`–`B23` in `docs/Learnings/Blender/Blender.md` at the close. Possibly one rule above them: *"Build a viewer from the factory **Layout** workspace only; never script workspace duplication in a GUI session."*

**Where it'd live.** a `docs/Learnings/Blender/` entry (the close's job here).

---

### 4 — A headless smoke render with no light looked like a defect; B11's "render it and look first" caught it before the lead saw anything `[self-error-doc-could-prevent]`

**Grounding.** The scale-test builder stripped the factory light, and its first `--smoke` render came out near-black. The lead's Material Preview uses a studio HDRI, so his view would have been fine. The agent's own check picture would have misled the agent, not the lead. The fix was to light the build with Material Preview's own default HDRI (`studiolights/world/forest.exr`), as click 1's builder already did. Two builders had to learn it separately.

**Proposed fix.** A learning: *"A scene built headless for a lead who uses Material Preview is lit with the same studio HDRI in its world, so the agent's look-first render matches the lead's view."*

**Where it'd live.** a `docs/Learnings/Blender/` entry, beside B11.

---

## Keep these

- **The discovery rule *"key on the artifact, re-verify a Brief written before the phases ahead of it ran"*.** Pass 2 found three real changes against the tree in under an hour:
  - D-5's stamp would have re-made every thumbnail (about 45 minutes of GPU);
  - the kept grids owed thumbnails;
  - *Matter* is now a group name.
- **Record the lead's ruling verbatim, the reading apart.** RD-P19-3 landed in his words, and its supersession sweep was done by grep: seven sites, marked in place.
- **Ask what the surface can show, before the sitting.** It made the run render each view and look first. That caught the occluded card, the half-buried body, the paint-mode tab and the black render, each before the lead saw it.
- **The lead names the wrong objects BEFORE reading the record.** It made click 2 a real test: he found all three planted errors, and his "maybe off" on the crate is itself a finding.
- **Act by act with a present lead.** Three sittings in one session. The two failed click-1 forms were repaired in minutes because he was there.

## Dead weight

None.

## Open questions

- **Click 1 scenes:** item 2's fix could make click 1 redundant in phases like this, since click 2 tested the grids better than click 1 did. Should the first click of a diagnostic-tool phase always be the tool in use?
- **The line hues (D-2):** the lead saw them through two scenes but never judged them as such. The executor carried them forward. Is that a ratification, or a reading of the same kind as item 1?
