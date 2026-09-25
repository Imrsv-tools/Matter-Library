# Workflow Feedback — P03 / discovery → execute / cold start through a partial close

| | |
|---|---|
| **Verb** | `discovery → execute` (one session: discovery Pass 3, then `/execute P3` steps 3.1–3.5, then `/execute_close` rows A⁻–A partway) |
| **Unit** | `P03` (Agentic Material Generation) |
| **Mode** | cold start → close (the close was stopped by the lead's `/retro`; its state is in the phase doc's Resume block, `fdf727b`) |
| **Outcome** | done, bar the close. Five steps built and kept by the lead; the close is uncommitted, with a texture anomaly recorded |
| **Shape** | behavior-touching |
| **Confidence** | Ran fully: discovery (a re-pass on a seeded Brief), execute (five steps, lead sittings via USDLiveView), close rows A⁻/A0/part of A. **Not exercised:** close rows B–E, `plan`, CI (parked). |
| **Date** | 2026-09-25 |

This is a distinct run, not a continuation of any earlier file.

---

## Items, ranked

### 1 — On a project with no running service, the "first human test" is written as commands the LEAD types; the lead does not want to type them `[doc-gap]`

**Grounding.** The Brief's first human test (discovery, `discovery.md` §The Brief) listed clicks as commands for the lead: `/matter-generate …`, then "edit the recipe so a key is misspelled, run the one command, see FAIL". At 3.2 the lead said: "Why I am doing any of this... go ahead and do what you need to do... I can look at stuff if you need eyes on, but entering commants and testing failure I'm not intersted". From then on the agent ran every click, and the lead's part was judging a render, which is the only part a human is needed for.

**Proposed fix.** In the Brief: "The first human test names what the lead must JUDGE, not what they must type. Every click that is machine-checkable is the agent's; the lead's sitting is the judgement (look, keep or discard)." For this repo, a `LOCAL_DELTAS` row under "the way this project is RUN": *the agent drives the tools; the lead reviews results in USDLiveView*.

**Where it'd live.** `discovery.md` §The Brief (first human test) + `execute.md` §TRY; `LOCAL_DELTAS.md` for the local surface.

---

### 2 — The review surface was named in discovery (USDLiveView), then the executor showed PNGs in chat anyway `[self-error-doc-could-prevent]`

**Grounding.** Discovery Pass 2 recorded USDLiveView as the lead's close-look surface, but ruled "the skill never launches the GUI; it prints the command". In execution I pasted rendered PNGs into chat for 3.3 and 3.4. The lead: "You need to be clear were I can see things... just open LiveView (the reason we made it) and I can look and adjust LCDs". I then found the launcher at `USDLiveView/usdliveview` in a minute. The information existed; the rule pointed the wrong way.

**Proposed fix.** `LOCAL_DELTAS` row "the artifact a person reaches": add *for a draft article: its preview scene opened in USDLiveView by the agent (`USDLiveView/usdliveview <scene.usda>` with `IMRSV_MATTER_SOURCE` set); a dialled-up layer is its own `make_preview.py --set` scene*. And a line in `execute.md` §TRY: "If the project has a viewer the lead built for this, the agent opens it; a picture in chat is not the sitting."

**Where it'd live.** `LOCAL_DELTAS.md` (port gap: the carried TRY text assumes a URL), `execute.md` §TRY.

---

### 3 — The harness's background-session worktree guard refused Edit/Write despite `"worktree": {"bgIsolation": "none"}` `[doc-gap]`

**Grounding.** From step 3.2 on, every Edit/Write was refused: "This background session hasn't isolated its changes yet. Call EnterWorktree first…". `.claude/settings.json` already had `bgIsolation: none`, and `.claude/CLAUDE.md` §Git forbids worktrees. The session had been launched with its working directory at `tools/validators/` (a subfolder); that may be why the setting was not read, but this is unverified. Two lead round trips ("restarted", "how about now") did not clear it, because nothing restarted this session. The lead then said "write through Bash", and the rest of the phase was written through heredocs and anchored Python substitutions.

**Proposed fix.** `.claude/CLAUDE.md` §Git: "If the worktree guard fires anyway, do not create a worktree: stop, say so, and offer (a) a new session launched from the REPO ROOT, (b) Bash writes on the lead's explicit go-ahead." Also note the likely trigger (launching from a subfolder) as a thing to test.

**Where it'd live.** `.claude/CLAUDE.md` §Git (Refiner's lane) and possibly a `docs/Learnings/` entry once the cause is confirmed.

---

### 4 — Discovery's risk-lane check read the provenance control but not the FREEZE selector, and a draft texture broke release verification `[self-error-doc-could-prevent]`

**Grounding.** Discovery verified the lane by reading `_validate_provenance` (drafts are exempt). But `freeze_release.py` and `stage_release.py` took every PNG under `MatterLibrary/textures/` as a release's payload. The first draft texture (3.3, `Fingerprints01`) turned `release_verify` red on the frozen `matterlib-0.1.0`, and staging would have shipped the draft. Fixed with the lead's go-ahead (`87c9d61`), reproducing 0.1.0's recorded digest exactly. `execute.md` already says "READ WHAT SELECTS ITS SUBJECT"; discovery has no equivalent, and this was a discovery-time question ("will adding files here disturb any gate?").

**Proposed fix.** `discovery.md` §Risk lane: "If the phase ADDS files to a tree, grep for every gate or tool that enumerates that tree (`rglob`, `glob`, `os.walk`) and read its selector."

**Where it'd live.** `discovery.md` §Risk lane.

---

### 5 — The harness's "changed on disk since you last read it" notices fire on the agent's OWN Bash writes, and read like a sibling session `[doc-gap]`

**Grounding.** After the Bash-write switch, every file I edited through the shell produced "…changed on disk since you last read it" when next seen. At `/retro` time I first took `make_preview.py` and `SKILL.md` notices as evidence of a live sibling. They were my own edits. `git status` settled it.

**Proposed fix.** `.claude/CLAUDE.md` §Git (shared tree): "A harness 'changed on disk' notice is not evidence of another session. Your own Bash writes trigger it; `git status -s` against the paths you touched is the check."

**Where it'd live.** `.claude/CLAUDE.md` §Git.

---

### 6 — `execute.md` cites `docs/ToolingConventions.md` §The gate registry, which does not exist in this repo `[doc-gap]`

**Grounding.** When `release_verify` caught a genuine defect, `execute.md`'s verify table says append a `CAUGHT:` line in the format that section owns. `grep` found no such section and no existing `CAUGHT:` line. I used the command's own form (`# CAUGHT: <date> — <what>, (<step>)`) on `run_release_verify`.

**Proposed fix.** Either carry the gate-registry section into `ToolingConventions.md`, or add a `LOCAL_DELTAS` row saying where the `CAUGHT:` format lives here.

**Where it'd live.** `LOCAL_DELTAS.md` (port gap) or `docs/ToolingConventions.md`.

---

### 7 — The phase's one measurement (review minutes) was asked for inside `YOUR CALL` and mostly never given `[self-error-doc-could-prevent]`

**Grounding.** The Brief made "time the review" the phase's measurement. I asked for it in each keep/discard call; the lead answered the keep and not the time four times out of five ("keep all,", "Yep! They looked ok"). Only the grey card has a number (3 min). The agent could have measured it: the time between opening USDLiveView and the verdict.

**Proposed fix.** When a Brief names a measurement the lead would have to report, make the agent measure it where it can (timestamps around the sitting) and ask only as a fallback.

**Where it'd live.** `discovery.md` §The Brief (a measurement line) / `execute.md` §TRY.

---

## Keep these

- **The four fork tests at authoring time** — at Pass 3 they turned four would-be lead questions (who lands C2, all 17 layers, gate the slider defaults, list-as-authority) into answered/not-necessary, leaving one real call.
- **"A finding about another unit decays in minutes"** — the C2 claim went from "live, uncommitted" to "landed as `001a857`" between writing it and committing; the pre-commit `git status` re-check caught it.
- **`git show --stat` read-back after every commit** — cheap, and it kept the file counts honest across ~20 commits with LFS pointers in them.
- **RED fixtures rejected "by their own named guard"** — writing the lane that way exposed a real weakness at once (G1/G2 shared a prefix, so a fixture could pass for the wrong reason).
- **The CAUGHT rule** — the one time a gate went red on genuinely wrong code, the rule made me record it at the only cheap moment.

## Dead weight

- `execute.md`'s web-service material (browser gates must click, `allowedDevOrigins`, URLs a person loads, the edge/route half) was read and did not apply: this project has no service. A port-gap candidate, not a cut upstream.

## Open questions

1. **The texture anomaly at the stopped close** (lead or next run): `Fingerprints01_overlay_s01.png` shows as staged (`MM`), which this run never did, and `Scuffs01_overlay_s01.png` reappeared after a delete. Whether a second session was live in the tree is unknown. It is recorded in the phase doc's Resume block, and the close must resolve it before committing either texture.
2. **Whether launching a session from a repo subfolder is what defeats `bgIsolation: none`** (item 3) is unverified; worth one deliberate test.
