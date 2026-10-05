# Workflow Feedback — P12 / Execute / Resume run 2

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P12` (Glass and Light Colour) |
| **Mode** | resume run 2, ended as a suspend-handoff at a step boundary |
| **Outcome** | suspended — steps 12.2 and 12.4 passed by the lead, 12.3 closed by a lead ruling; 12.5 and the close remain |
| **Shape** | behavior-touching |
| **Confidence** | Ran fully: `execute.md` §Before you touch anything, BUILD, TRY, STRENGTHEN, Handback, across three steps and three sittings, with a second session committing in the same tree. **Not exercised:** `execute_close.md`, `execute_repair.md`, `execute_highrigor.md`. Nothing below touches those. |
| **Date** | 2026-10-05 |

Not a continuation of another file. Step 0 was completed: the Resume block, the ledger rows, both findings and the lead's ruling are in the phase doc and committed.

---

## Items, ranked

### 1 — "Open the tool for the lead" has no stated shape, and the obvious one loads the lead's own work `[doc-gap]`

**Grounding.** Click 2 needed a scene in the lead's Blender. `execute.md` §TRY and `LOCAL_DELTAS.md` both say the agent opens the running tool on the thing. The run launched `blender --python <scene script>`. A bare launch loads the user's **startup scene**, which on this machine is a large personal project (590 objects), not Blender's default. The script looked up the object named `Cube`, found one that belonged to that project, moved it and replaced its material, in memory. Nothing was saved (the session had no file path), the window was closed by PID, and the startup, preferences and last-session files kept their size and timestamps. It cost a turn, a confession to the lead, and it was one keystroke of the lead's (*Save Startup File*) from being real damage. Two more facts found the same way: the Blender MCP answers from **whichever** Blender holds its port, so a second launch is silently not the one you are talking to; and a headless probe that used `--factory-startup` had been safe all along, which is why the hazard was invisible until the GUI launch.

**Proposed fix.** In `LOCAL_DELTAS.md`, beside "the artifact a person reaches": **A scene for the lead in a GUI tool is BUILT HEADLESS FROM THE FACTORY SCENE INTO ITS OWN FILE, and that file is opened (`blender <file> --python <view script>`). Never a bare `blender --python`. The build script refuses any scene whose object set is not the factory's; the view script and every MCP write assert the file path first. One GUI Blender at a time: the MCP talks to whichever holds the port.** The portable half, for `execute.md` §TRY next to *never break the lead's running environment*: **a GUI tool you launch for the lead starts in THEIR profile — their startup file, their recent session, their preferences. Build what you show in a file of its own; a lookup by a default name (`Cube`, `Scene`) is not evidence the object is yours.**

**Where it'd live.** `LOCAL_DELTAS.md` (the Blender shape) · `execute.md` §TRY (the portable sentence) · `docs/Learnings/Blender/` (the MCP-port fact).

---

### 2 — A click's pass condition can be unpassable under the Brief's own Not-now, and nothing checks it `[doc-gap]`

**Grounding.** Click 3 passed when *"the body of the stone takes the colour in Blender and Unreal"*. The same Brief put *"the solid master's absorption with depth"* and *"a new Unreal build"* under Not-now. On a solid, Unreal shows the colour faintly and does not deepen it with thickness, so the click could not pass without the excluded work. The lead looked, said it was hard to tell whether Unreal was colouring at all, and had to rule on scope mid-run. `execute.md` precondition 3 walks the **step list's targets**; it does not walk the **first human test** against Not-now. The Not-now line also pointed at a ledger row that did not hold the item (that row was about refraction bend only), so when the finding landed it had no home and the run appended it to the nearest row.

**Proposed fix.** `execute.md` §Before you touch anything, a fourth walk: **⛔ READ EACH CLICK'S "PASSES WHEN" AGAINST THE BRIEF'S NOT-NOW. A click that names a tool, a surface or a behaviour whose repair is Not-now is not passable as written: say so before the first step, and ask whether the click narrows or the Not-now moves.** And in `discovery.md`, where the Brief is written: **a Not-now item that cites a tracker row must be IN that row — open the row and read it, or add it.**

**Where it'd live.** `execute.md` §Before you touch anything · `discovery.md` (the Brief's Not-now).

---

### 3 — A test row named at discovery is a hypothesis about the instrument's range `[doc-gap]`

**Grounding.** Two of the Brief's planned rows could not show what they were for. *"The same row"* (a bottle green) on the solid article is fifteen absorption depths across the rig's cube: the path tracer draws it black, correctly, and two tools "agreed" at a difference of 1.0 because both were black. *"Brightness double"* on the dim view clips every tool to the same white, and the rig reported it **UNEVEN** (5.4 / 5.6 / 12.0): a false verdict that measured only how far each tool's default was from white. Both were caught by `execute.md`'s *"a comparison whose sides cannot differ agrees by construction"* row, which worked; but each cost a full re-render, and the lead had already been shown the first sheet.

**Proposed fix.** `discovery.md`, where the first human test is tabled: **each planned row carries the value it sets AND the reading it should land on in the instrument (below clip, above the noise floor, at the subject's real size). A row whose expected reading you cannot state is not yet a test.** One sentence; it moves a check the executor does at render time to where the row is invented.

**Where it'd live.** `discovery.md` (first human test) — unsure whether portable or this rig's.

---

### 4 — No mark exists for a `⚠human` step the lead looked at, did not pass, and ruled to continue past `[doc-gap]`

**Grounding.** `execute.md` §TRY gives two states: `✅` and `▶ SCAFFOLD COMPLETE — sitting owed`. After click 3 neither was true: the sitting was no longer owed, and it was not a pass. The run wrote *"Closed by the lead's ruling RD-P12-2, not by a pass of the Unreal column"* in the ledger row and in the Resume line. That is an invented state, written twice in slightly different words.

**Proposed fix.** Name the third state beside the other two: **`◐ CLOSED BY RULING <id> — not passed: <what did not>, followed up at <home>`.** The rule that a `✅` and an owed sitting are a contradiction stays as it is.

**Where it'd live.** `execute.md` §TRY.

---

### 5 — Opening a sheet for the lead cannot be confirmed `[doc-gap]`

**Grounding.** `LOCAL_DELTAS.md` says a picture pasted in chat is not the sitting, and the Brief says the agent *"opens the sheet"*. The run used `xdg-open <sheet.png>`, which returns nothing either way, and there is no desktop screenshot tool in the session, so both handbacks said *"I asked your image viewer to open it; if it did not, it is at …"*. The rule *"load it yourself first, the way they will"* cannot be met for a sheet.

**Proposed fix.** State the project's way in `LOCAL_DELTAS.md`: which command opens a rig sheet for the lead, and that the handback always carries the path as the fallback. If Blender is the viewer the lead already has open, an image editor area driven over the MCP is confirmable; `xdg-open` is not.

**Where it'd live.** `LOCAL_DELTAS.md`.

---

## Keep these

- **`.claude/CLAUDE.md` §Git, the post-commit read-back against a pre-measured count** — a second session landed five commits between this run's, one of them editing the same ledger line this run had an uncommitted addition on. `git diff --stat` before and `git show --stat` after matched to the line (24 files, 148 / 36), which is the only reason the 12.4 commit can be trusted. The sibling's filtered stage left this run's hunk intact, so that rule worked from the other side too.
- **`execute.md` "a comparison whose sides cannot differ agrees by construction"** — caught both clipped rows of item 3, and prompted the before/after control pair that proved two master rewrites moved nothing.
- **`LOCAL_DELTAS.md` "baseline `check_exporter.sh` BEFORE you edit", with `execute.md` "compare the SET, not the tally"** — the check was red before and after on the same five checks; without the baseline that reads as a regression of the step.
- **"No Claude co-author trailer" stated once in `.claude/CLAUDE.md`** — the harness injected an attribution reminder at the start of this session telling the agent to add one. The always-loaded line won.
- **`execute.md` "the lead's findings are the work" with the divergence table's "stop and surface"** — the lead's one-line remark on click 3 became a recorded finding, a two-option question and a ruling in one round trip.

## Dead weight

- `execute.md` §BUILD's *"is it up / is it current / has it reached what a reader loads"* paragraphs and the Verify rows on browser gates and `curl 200`: not consulted. `LOCAL_DELTAS.md` already says there is no web service; the text is still read in full on every `/execute`.

## Open questions

1. **[lead]** `check_exporter.sh` has carried the same red set since Phase10 (five carrier checks that stop at one import: the carrier check loads the assembler under a Python with no MaterialX). Each phase records it as inherited; no issue or ledger row owns it. Those are the checks that would prove a new Creator port is connected in an export, so this phase proved that by hand instead. Does it get an issue?
2. **[lead]** The export add-on is not enabled in the lead's Blender preferences, while the product spec lists *File → Export → IMRSV LCD USD* as shipped and `LOCAL_DELTAS.md` names *"the installed Blender add-on"* as a surface. Is installing it part of a close, or is the repo copy loaded by the agent the intended state before the first release?
3. **[refiner]** The handback-format contradiction (`execute.md`'s three beats against the Working Agreement's five) is already on `_RefinementBacklog.md`; met again this run, five beats used, not re-filed.
