# Workflow Feedback — P25 / Discovery / Pass 3

| | |
|---|---|
| **Verb** | `discovery` (Pass 3: the lead made the phase "research and testing until the result is great") |
| **Unit** | `P25` |
| **Mode** | `resume run 3 (session ML_P25_D3)` — a distinct run, not a continuation of `261101_P25_DiscoveryExecute_Pass2.md` |
| **Outcome** | `done` — five probes, the face's route settled by the lead (RD-P25-15: front-view face → dense landmarks → projected; one coordinate field for the island), findings F-P25-13 … 20, a hand-off section; the next session `ML_P25_D4` started on the lead's yes |
| **Shape** | `doc-only` (the phase doc, the Roadmap line, probe scripts beside the doc; no tool or source change) |
| **Confidence** | Ran fully: discovery's probe loop, the look view, the lead's sittings by picture, the peer-message correction channel, retro step 0. **Not exercised:** a Brief rewrite (see item 1), any gate or `run_all.py` (nothing under `tools/` changed). |
| **Date** | `2026-11-01` |

**One correction is owed to the live `ML_P25_D4`** (item 1): sent by message; recorded here as the channel of record.

---

## Items, ranked

### 1 — Five probes appended under the Brief; the Brief itself still describes the rejected route `[self-error-doc-could-prevent]`

**Grounding.** Pass 3 overturned the face's route twice in one session (the UV warp → front projection, RD-P25-15) and settled the neck (RD-P25-16). Every finding landed under `### Pass 3 results` and a `### Pass 3 hand-off`, but `## The Brief` at the top (§What this phase builds, §The routes compared, §In now, §Step list, §Compact build map, RD-P25-9/10's candidate (d)) was never rewritten. A reader starting at the top of the doc reads the route the lead rejected at 25.1.13. `discovery.md` says *"DISTIL, DO NOT APPEND"* and *"Reseed, don't patch, on a core-framing FLIP"*; this run did neither, because each probe was a short loop with the lead and the Brief felt like a step-list artifact that a research-and-testing pass had no use for. By the retro, `ML_P25_D4` was live on the doc, so the correction went to it by message instead of being landed.

**Proposed fix.** In `discovery.md` §Discovery discipline: *"A lead ruling that changes the route (a new RD that supersedes one in the Brief) is a Brief edit in the same commit — mark the superseded text in place and point at the new ruling. A pass that runs as an open probe loop still owns the Brief's first paragraph and the route table: they are what the next reader opens first."*

**Where it'd live.** `discovery.md` §Discovery discipline (supersession hygiene).

---

### 2 — The lead's target picture existed only in another session's job temp folder `[doc-gap]`

**Grounding.** The Pass 3 opening named the target as `uv_a_s90_seed7.png` with no path. It existed only under a finished session's `$CLAUDE_JOB_DIR/tmp`, which is deleted with that job; I found it with `find /`. This run then kept every probe input (the target, landmarks, frames, ear moves, maps) in its own job scratch until the hand-off, when I moved them to git-ignored `library/parity/P25_Pass3/`. A job deleted before the hand-off would have lost the lead's chosen reference (it turned out to be reproducible by seed, but nobody knew that until this run checked).

**Proposed fix.** One clause where scratch is defined (the premise-probe rule): *"A file the lead names, judges or is shown (a target, a winning picture) is copied into the phase's git-ignored parity folder when it is shown, and the doc names that path. Session scratch (`$CLAUDE_JOB_DIR/tmp`) is deleted with the job; it holds only what can be lost."*

**Where it'd live.** `discovery.md` HARD RULE (premise probe) · `LOCAL_DELTAS.md` (the parity folder is this project's home for it).

---

### 3 — A "clean" verdict given to the lead from a shrunk sheet, wrong at native pixels `[self-error-doc-could-prevent]`

**Grounding.** Seven seeds rendered, I judged them from half-size 4-up sheets and told the lead seeds 3, 42 and 2026 were "clean, front and profile". Building the native-resolution picture for the lead, 2026's profile showed horizontal streaks and a tone step on the cheek, which led to the 0.3 cut (F-P25-17). The rule that pictures are shown at native resolution (LOCAL_DELTAS, memory) is phrased for what the lead sees; nothing says the agent's own verdict needs the same pixels.

**Proposed fix.** Extend the native-resolution rule: *"…and the agent's own verdict on a look (clean / has a defect) is read from native pixels before it is said to the lead. A shrunk sheet is for picking which ones to open."*

**Where it'd live.** `LOCAL_DELTAS.md` (the artifact row's native-resolution clause) · memory `show-pictures-full-resolution`.

---

### 4 — The Unreal check sat in the same call as the launch, so it could not stop the launch `[self-error-doc-could-prevent]`

**Grounding.** Every look-view launch ran `ps -ef | grep "[U]nrealEditor"` and the launch in one Bash call. Once, a platform session's Studio (`UnrealEditor … -game`) had started; the output showed it, but the launch had already been issued. The launch only failed because of an unrelated bug (zsh passing six `label=picture` arguments as one, from an unquoted `$A`; `~/CLAUDE.md` already says use `${=VAR}`). I then asked the lead, who said run beside it.

**Proposed fix.** In §Two machines: *"The Unreal check is its own call, read before the launch is sent; never chained with it."*

**Where it'd live.** `LOCAL_DELTAS.md` §Two machines.

---

### 5 — `cd` again, in retro step 0's two commands `[self-error-doc-could-prevent]`

**Grounding.** I prefixed the namer call and `claude --bg` with `cd <repo>`, to be sure the namer picked the `ML_` prefix. The session's working directory was already the repo, so it was unneeded; `.claude/CLAUDE.md` bans `cd` in any command. `retro.md` step 0 gives the namer command without saying it reads the project from the current directory, which is what made me reach for `cd`.

**Proposed fix.** In `retro.md` step 0, after the namer command: *"(It reads the project from the session's working directory: run it as is, never behind a `cd`.)"*

**Where it'd live.** `retro.md` step 0 (upstream: the namer is upstream's).

---

## Keep these

- **One labelled picture at native pixels, opened for the lead, path in the handback** — the lead answered within minutes each time, and two of those answers changed the route (*"MUCH BETTER! YES"*, and the lead's own catch that Krea's map is a front view, which the picture made visible).
- **The lead's words verbatim in the doc, the reading apart** — six rulings and questions this pass; the hand-off could quote each instead of paraphrasing.
- **A premise probe's exact command beside its finding** — every probe here records its invocation and the scripts sit beside the doc; the hand-off is runnable.
- **"A comparison needs a number and a look"** (`discovery.md`) — caught that the ear finder's 3.0 mm passed a broken ear (seed 101), and the lip measure was calibrated on the lead's approved target before being quoted (−23 px on a fit the lead had accepted, so an offset, not a defect).
- **The peer-message channel for a correction to a live doc** — a sibling's correction arrived by message and landed in this run's first commit; this run's own correction went to `ML_P25_D4` the same way.
- **Asking once before launching beside another session's Studio** (§Two machines) — the lead said run, with the load and time in the question.

## Dead weight

None.

## Open questions

1. **Is an open-ended "research and testing until the result is great" pass a `/discovery` or a `/research`?** The lead opened it with `/discovery`; its output is a probe loop with the lead, not a Brief, and item 1 is the result. **Refiner question:** should discovery have a named probe-loop mode, with the Brief's first paragraph and route table as its only required sections, or should such a pass run as `/research` on the phase?
