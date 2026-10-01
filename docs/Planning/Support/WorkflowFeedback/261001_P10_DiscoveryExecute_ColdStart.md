# Workflow Feedback — P10 / discovery → execute / cold start

| | |
|---|---|
| **Verb** | `discovery → execute` (one session: discovery Pass 2 and the Brief, then `/execute` run 1) |
| **Unit** | `P10` (Coloured Wear Layers) |
| **Mode** | cold start (discovery resumed at Pass 2; execute run 1), ending in a suspend-handoff to the UE machine |
| **Outcome** | suspended: Brief written, Q-P10-1 ruled, 10.1–10.3 built and passed by the lead (clicks 1–5), pushed; 10.4 handed off to the UE machine |
| **Shape** | behavior-touching |
| **Confidence** | Ran fully: discovery Pass 2 (probe, Brief, fork), execute BUILD/TRY over three steps with five sittings, a push. **Not exercised:** the close, high-rigor, the Unreal build on the other machine. |
| **Date** | 2026-10-01 |

Not a continuation of any file. Read before writing: `_RefinementBacklog.md`, `261001_LC-P10_Discovery_Session.md`, `260930_P06-P09_CloseDiscoveryExecute_Session.md`.

---

## Items, ranked

### 1 — A value that becomes a CONNECTION is a shape change, and every reader of the old form drops it silently `[self-error-doc-could-prevent]`

**Grounding.** 10.1 made the assembler route `transmission_weight` (and subsurface, coat, fuzz) through the nodegraph whenever a deposit covers it, so on Glass_Clear the shader input changed from `value="0.95"` to `nodegraph=… output=…`. The one shared reader, `blender/masters/article.py`, collects shader inputs only `if i.get("value") is not None`. So Blender's loader would have left Transmission Weight at 0 (opaque glass), and the Unreal driver would have passed nothing. My headless Blender check printed the deposit flags and colours, not the weights that had changed form, so it passed. What surfaced it was a different reader: the rig's mask row did `startswith("overlay")` and set the new colour port to `1.0`, `usdrecord` refused the scene, and while fixing that I read the driver and found the dropped weight. Both were the same class: a new port sharing a prefix, and a value turned into a connection. `execute.md` §Verify already has the row (*"changing the SHAPE of data many tools parse … grep for … every parser of that shape"*). I did not fire it, because I filed the change in my head as *adding* a cover, not *changing* an input's form. Discovery's build map had enumerated every reader of `LCD_PORTS`, but not the readers of shader values.

**Proposed fix.** Give the existing row two examples a run will recognise: *"an input that was a VALUE becomes a CONNECTION"* and *"a new name shares a prefix that code selects on (`startswith`)"*. In discovery's build-map guidance: *"enumerate the readers of every value whose FORM changes, not only of the vocabulary that grows"*.

**Where it'd live.** `execute.md` §Verify before edit (the SHAPE row); `discovery.md` §The Brief (compact build map).

---

### 2 — A Brief asserted a fixture's state from its NAME `[self-error-doc-could-prevent]`

**Grounding.** The discovery Brief's click 5 said *"Concrete_Smooth_Worn_Dusty (its dusty defaults)"*. At execute its dust row at 0 equalled its defaults: the recipe sets no `lcd_defaults`, and "Dusty" is its texture. The click still worked (the lead judged the dust rows), but the Brief carried a false premise into a sitting description, and execute had to log a corrected fact. `discovery.md` already says to reconcile each click *"on the fixture the test will actually use"*. I reconciled reachability, not the fixture's state, and took that state from the name.

**Proposed fix.** One clause in the reconcile rule: *"a fixture's state (its start values, what it carries) is READ from its data, never inferred from its name."*

**Where it'd live.** `discovery.md` §The Brief (Step list, the reconcile sentence).

---

### 3 — The `cd` ban broken a third time, this time by a shell loop `[self-error-doc-could-prevent]`

**Grounding.** `cd …/tools/converters/recipes && for f in …; do python3 /tmp/p10_deposit.py $f.json …; done` to apply one edit to 11 recipes. The `cd` came in to keep the loop's filenames short, and it also moved the session's working directory (the harness reported the change). The two previous retros filed the same slip (`260930_…` item 6, `261001_LC-P10_…` item 7: there `uv run` pulled it in). Here no tool needed the directory; the loop did.

**Proposed fix.** Add the loop shape to the fallback shapes: *"a loop over files takes absolute paths (`for f in A B; do tool /abs/dir/$f.json; done`), or better, the script takes the list itself."* The structural fix that worked minutes later in this run: a `/tmp` Python script holding the list (`/tmp/p10_assemble11.py`).

**Where it'd live.** `.claude/CLAUDE.md` §Codebase search (fallback shapes), beside the uv form item 7 of `261001_LC-P10_…` proposes. This is a recurrence count, not a new rule.

---

### 4 — A handoff names commands for another machine: check every name exists `[doc-gap]`

**Grounding.** The 10.4 Resume block first said `build.sh package`, `publish.sh 3` and "the pin". A check found them at `unreal/build.sh`, `unreal/publish.sh` and `unreal/RUNTIME.json`, not under `unreal/MatterRuntime/`, the folder the same block named for `build_masters.py`. A run on the UE machine following the first wording would have looked in the wrong folder. Nothing in `execute.md` §Suspend asks that a handoff's commands be checked, and a cross-machine handoff is the case where the next run cannot ask.

**Proposed fix.** In the suspend/ledger guidance: *"every path, script and parameter name a handoff tells the next run to use is checked against the tree before the handoff is committed: `ls` it, `grep` it."*

**Where it'd live.** `execute.md` §STRENGTHEN (the suspend ledger).

---

## Keep these

- **A discovery probe before the Brief, kept as a tracked script.** Pass 1's direction (dust as OpenPBR fuzz) was measured in Storm in about 10 minutes and failed face-on (4.5 levels vs 4.2 today; a cover 16.9; glass needed transmission covered, 34.5). It overturned the direction before any code, and execute built on those numbers unchanged.
- **Baseline `check_exporter.sh` BEFORE editing `blender/addons/`** (LOCAL_DELTAS). It was already red on `main` for an environment reason. Because the baseline existed, 10.2's run compared as the same set with 64 PASS before and after, instead of a red to explain mid-step.
- **Compare the SET, not the tally** (§Verify). The gate went from {`approval_binds_freeze`} to {`approval_binds_freeze`, `release_verify`} at 10.1. The new member was attributed to Glass_Clear being in the pilot, then cleared by the 10.3 re-freeze, with no guessing.
- **Pre-push scan of the outgoing diff for private strings.** It caught a person's name inside a home path that I had quoted myself, in a finding about leaked paths (F-P10-17). It also measured that the already-published library `.blend` carries the same path, so the push added no exposure. Redacted, committed, then pushed.
- **Render the sitting before opening it.** Click 3's first framing was a dark, too-close shot of wood; reframed before the lead saw it.
- **Read back the lead's edit at the agent's half of a click.** At click 4's export the scene held the default colour, not the lead's. I said so, set soot on the same material in his session and exported that; the doc records it the same way. A step closes when the artifact works, not when the lead replies.
- **The act is the unit.** Five sittings, each passed on its own before the next step began; nothing drained ahead of a click.

## Dead weight

None.

## Open questions

1. **`check_exporter.sh` is red on `main` and nothing owns it.** Its carrier steps import `assemble_mtlx`, which imports `MaterialX`, under a `pxr` Python that has no MaterialX module (the same import at `HEAD`). It is recorded in Phase10's 10.1 ledger row as inherited. It needs a `/quick-fix` (or a `ToolingConventions.md` note on which Python the check needs), which is a lead call, not the Refiner's.
2. **F-P10-17** (an absolute author-machine path in exports and in the committed library `.blend`): the lead was asked quick-fix or issue; unanswered at this deposit. The recommendation is in Phase10's Resume block.
