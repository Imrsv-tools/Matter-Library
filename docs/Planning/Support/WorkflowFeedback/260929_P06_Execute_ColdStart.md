# Workflow Feedback — P06 / execute / cold start

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P06` |
| **Mode** | cold start → suspend-handoff (~450k context, at the 6.2/6.3 boundary) |
| **Outcome** | suspended. 6.1 done (click 1 approved by the lead: *"yep... looks the same"*); 6.2's package built and verified, publishing deferred by the lead; 6.3 investigated only. Resume block in the phase doc. |
| **Shape** | behavior-touching (a new Unreal app, a rig driver, rig changes, a Blender-side reader move) |
| **Confidence** | Ran fully: execute's BUILD and TRY for 6.1, BUILD for 6.2, the commit discipline, one push with a rebase. **Not exercised:** STRENGTHEN beyond the one caught bug, `execute_close`, `publish.sh` (never run), the other machine. |
| **Date** | 2026-09-29 |

Not a continuation of `260929_P06_ResearchDiscovery_ColdStart.md` (that file is the discovery run; this is the first execute run).

---

## Items, ranked

### 1 — A Brief's first human test can rest on a tool that does not run on the machine the step runs on; nothing checks `[doc-gap]`

**Grounding.** Click 1 read *"The grey reads as the same grey as Storm and Blender"* on this machine (the UE machine). The rig's Blender driver fails here: Fedora's `blender-5.2.0` cannot compile Cycles' CUDA kernels (CUDA 13), and its colour management is off (OCIO config v2.5, library 2.4.2). `library/parity/` did not exist on this box, so the rig had never run here. It surfaced only when the lead ran the rig mid-execute. Then the run had to build `rig.py --no-blender`, an Unreal-drawn mask and a Storm-referenced calibration, and log the false premise (about 25 minutes and one extra commit before click 1).

**Proposed fix.** In discovery's first-human-test check: *"For each tool the click compares against, name the machine the step runs on and show that the tool has run there: one existing output, or a one-line smoke. On a two-machine project, 'the rig works' is a per-machine fact."*

**Where it'd live.** `discovery.md` (the Brief's first-human-test gate), and `LOCAL_DELTAS.md` (the "RUN" row could name the tools each machine can run, measured and dated).

---

### 2 — Rebasing before a push rewrote every SHA the phase doc's ledger cited `[doc-gap]`

**Grounding.** Eight local commits were cited by SHA in the ledger (`6642cc7`, `0ebefb5` …). At push time the other machine had pushed 3 Phase09 commits, so `git rebase origin/main` rewrote all eight. The pushed ledger then pointed at orphaned objects and needed its own correction commit (`3240c21`). `execute.md`'s write ceiling covers only "a row cannot carry the SHA of the commit that contains it".

**Proposed fix.** In `execute.md` §Keep the lead oriented, beside the SHA rule: *"On a shared trunk, a SHA is not stable until pushed: a rebase onto someone else's push rewrites it. Cite steps in the ledger until the push, or re-map the SHAs in the same push."*

**Where it'd live.** `execute.md` (portable: any project with two writers to one trunk).

---

### 3 — When the permission classifier refuses a *direct* command, the working move is handing the lead a `! <cmd>` line; execute.md only covers refused wrappers `[doc-gap]`

**Grounding.** `uv run tools/parity/rig.py GreyCard…` (Storm + Blender, GPU) was refused as *"Interfere With Workloads"*. The Unreal build and launches were allowed. Rule 3's advice is for `bash script.sh` wrappers (re-issue as one direct statement), and this was already one. The lead ran it with `! …` and the output landed in the session, which unblocked the step.

**Proposed fix.** Rule 3, one sentence: *"A refused DIRECT statement is not yours to reshape: hand the lead the exact `! <command>` line, say what it produces and where, and carry on with work that does not depend on it."*

**Where it'd live.** `execute.md` §THREE RULES, rule 3.

---

### 4 — The gate of record is red on a box whose git-ignored staging tree predates the release records; LOCAL_DELTAS does not say so `[doc-gap]`

**Grounding.** `run_all.py` gave 14 PASS / 3 FAIL (`approval_binds_freeze`, `release_verify`, `activation`). The cause, measured and not assumed: this machine's `library/staging/matterlib-0.1.0` is dated 2026-09-24, and the records were re-frozen at the Phase05 close on 2026-09-27 on the other machine (*"freeze record carries no .dds entries"* against an on-disk `dds_set`). The run had to derive that before committing. The next run on this box will meet the same reds.

**Proposed fix.** In the `LOCAL_DELTAS.md` "RUN" row: *"The release lanes read the git-ignored `library/staging/`. A box whose tree predates the last re-freeze goes red on three lanes. That is box input, not a regression: refresh with `stage_release.py build` (the maintainer's call) or classify it as inherited."*

**Where it'd live.** `LOCAL_DELTAS.md` (local), or `docs/ToolingConventions.md` §Gates and CI (product).

---

### 5 — A shared GPU/UE machine with another project's agent: the batched run table was the shape that worked `[doc-gap]`

**Grounding.** The lead acted as traffic control (*"please check with me before running anything… I'll be traffic controll for now"*), on top of D1's "ask before each GPU launch". Asking per run would have been a dozen round trips. What worked was a table of runs with columns #, command, load (CPU / GPU / UE) and time. The lead answered in three words (*"go A–D, hold E and F"*, later *"go G1–G4"*), and later lifted the gate (*"you are the lead agent now… the IMRSV agent is paused"*). execute.md has *"Ask whether the lead is available"*, but no shape for *"the machine is shared with another project's heavy jobs"*.

**Proposed fix.** In execute.md's §Before you touch anything, a line: *"On a machine shared with other heavy work, present the next runs as one table (command · load · time) and ask once. Check for running engine and build processes before each launch."*

**Where it'd live.** `execute.md` (portable); the check itself is already D1 in this phase.

---

## Keep these

- **The verify row "a parameter that should matter … indicts the instrument before the subject."** The first calibration fitted `SUN_K` = 0.14 with a p95 error of 30%. Instead of accepting a factor, the run looked at the sun-only picture, then found the brightest sphere pixel (top-centre, 0.091 against Lambert's 0.086). That proved the strength right and the direction wrong: a spawn rotation that never reached a light made Movable after spawn. It was fixed and logged from inside the runtime; the fit then came out at 1.03 / 1.07 with a p95 error of 2.5%. It is also the likely cause of the research spike's "2.5× bright".
- **The divergence row "a fact the Brief rested on is false: build it, log a deviation".** It turned the broken Blender into a bounded detour (`--no-blender`, Unreal's own mask, calibration to Storm) instead of a stop.
- **"Split the work into what needs the full stack and what does not."** CPU smokes (mesh winding against the engine's own `GenerateBoxMesh`, the reader move on 57 articles, the no-Blender sheet on stand-in pictures) caught everything the first GPU launch would otherwise have spent.
- **The index check and read-back on every commit.** Clean all run. It also kept an editor-written `SecurityToken` out of a public repo (the engine rewrote `DefaultEngine.ini`).
- **The context meter's 450k note.** It arrived just as 6.3's first-time coding was about to start, and the run suspended with a resume block instead of starting it.

## Dead weight

None.

## Open questions

1. **Lead decision:** refresh this machine's `library/staging/` (`stage_release.py build`) so the gate is green here, or leave the three release-lane reds as known box input?
2. **Lead decision:** is Storm acceptable as the calibration reference of record, or must the close re-fit against Blender on the other machine? The resume block recommends the re-fit and recording both.
3. **Lead decision:** D1 (*"ask the lead before each GPU launch"*) was lifted for this session while the IMRSV agent was paused. Is that standing for later Phase06 runs, or per session? The phase doc still states D1 as written.
