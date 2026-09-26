# Workflow Feedback — BigPicture + P05 / research → discovery / cold start

| | |
|---|---|
| **Verb** | `research → discovery` (one session: `/research` on the project's direction, a lead-directed seed of Phase05/Phase06, then `/discovery Phase05`, then lead-directed machine setup: Blender 5.2.2 LTS and the official Blender MCP) |
| **Unit** | `BigPicture` research (`260926_R_BigPicture_NimbleSetup.md`) + `P05` discovery |
| **Mode** | `cold start` |
| **Outcome** | `done`. Research parked with 12 passes and rulings BP1–BP9. Phase05/06 seeded, Library Coverage renumbered to Phase07. The Phase05 Brief is complete (build lane). Blender 5.2.2 and the Blender MCP are set up on the maintainer's box. |
| **Shape** | `doc-only` in the repo (plus machine setup outside it) |
| **Confidence** | Ran fully: research, the seed, discovery Pass 1–2 with probes, and the machine setup. **Not exercised:** execute. A fresh session is executing Phase05 as this is written (`tools/parity/` is untracked, and `.gitignore` and the Phase05 doc are modified by it). |
| **Date** | 2026-09-26 |

**Step 0 was completed.** The chat-only considerations went to research Pass 12 (`d38a21b`), and the footer was reconciled (`d6f04ff`). **One correction is owed to a doc a live verb owns**; see Item 1. It is deposited here because this session can't reach that run.

---

## Items, ranked

### 1 — OWED CORRECTION to the live Phase05 doc (hand to the executor) `[self-error-doc-could-prevent]`

**Grounding.** Commit `a4b234b` wrote into `docs/Planning/Phases/Future/Phase05_TestRig.md` §Discovery Status → *Checks to carry forward*: *"Clash to avoid: Blender 5.1's config still enables an older community MCP add-on on the same port, so don't run 5.1 and 5.2 at once."* The lead then said "turn off the old MCP add-on in 5.1", and it was disabled in 5.1's saved preferences (verified: a fresh 5.1 launch no longer loads `blender_mcp_addon`; backup at `~/.config/blender/5.1/config/userpref.blend.bak-260926-mcp`). The sentence is now false. A fresh session is executing Phase05 and has uncommitted edits to that doc, so this session did not touch it.

**Proposed fix (for the executor, anchored).** Replace the sentence beginning *"*Clash to avoid:* Blender 5.1's config still enables"* with: *"The older community MCP add-on in Blender 5.1's config was switched off (lead, 2026-09-26), so 5.1 and 5.2 no longer compete for port 9876."*

**Where it'd live.** The Phase05 doc (a content correction, not the method).

---

### 2 — The lead cannot follow the method's vocabulary, and inventing a new term made it worse `[doc-gap]`

**Grounding.** The lead said *"I don't know the magic words you are using here with lanes and tricky terms… how many times do I need to say stop with the bureaucracy"* and, later, *"Milestone is not really a thing I know… I am really confused what you plan is."* The second was caused by this run. To avoid a glossary collision ("Stage" is the IMRSV runtime), I invented **"milestones M0–M6"** for proposed phases in a research doc. The lead read them as a new process layer and asked whether I was "trying to oneshot this". The method's own word, "phase", was right all along. A proposed-but-unnumbered phase is exactly what the Roadmap's `TBD` entries are. Separately, the lead-facing messages used project-internal ids ("lane L4", "C1", "R14", "BP3") that mean nothing to someone not reading the docs.

**Proposed fix.** In `research.md` (and `AI_WorkingAgreement.md` §Working With the Lead): *"A research doc that proposes a sequence of work proposes **phases** — named, unnumbered, the Roadmap's `TBD` shape. Never introduce a new unit word (milestone, stage, track, wave) for it; the lead reads a new word as a new process layer."* And: *"In a lead-facing message, say what an id means in plain words; never lean on a doc-internal id (`L4`, `BP3`, `C1`) as if the lead knew it."*

**Where it'd live.** `research.md` + `AI_WorkingAgreement.md`. Probably portable → upstream.

---

### 3 — MCP servers added mid-session never reach a RESUMED conversation, and nothing says so `[doc-gap]`

**Grounding.** The Blender MCP was registered with `claude mcp add -s local` during this session. The lead restarted Claude Code, which **resumed this conversation**. Claude Code's log (`~/.cache/claude-cli-nodejs/<project>/mcp-logs-blender/`) shows the server connecting and listing its tools at 12:05:43Z, yet a `ToolSearch` for its tools in the resumed conversation found nothing, twice. I first told the lead the setup was fine and to "restart", then misdiagnosed it as "you are talking to the old session" before correcting myself from the log. Only a **fresh** (non-resumed) session exposes newly added MCP tools.

**Proposed fix.** A learning, plus a line wherever the method sets up tooling: *"After adding an MCP server, the tools appear only in a FRESH session: not this one, not a `--continue`/`--resume` of it. Say so in the same message, and verify from the new session with one live call. `claude mcp list` saying 'Connected' proves the server starts, not that this conversation can call it."*

**Where it'd live.** A `docs/Learnings/ClaudeCode/` entry (the first; the folder is still empty), and the setup guidance if one exists. Unsure whether it is portable; probably yes.

---

### 4 — `pkill -f <path>` killed the agent's own shell again (second occurrence, same day) `[self-error-doc-could-prevent]`

**Grounding.** `pkill -f 'opt/blender-5.2.2-linux-x64/blender'` matched the bash command line that contained it. Exit 144, and nothing after it in the same call ran: no config backup, no migration. This is **already filed** as item 4 of `260926_USDLiveViewServe_ResearchQuickFix_ColdStart.md`. It is recorded here only as **recurrence evidence** from a different session the same day, which argues for a rule in `.claude/CLAUDE.md`-level guidance rather than a learning. What worked: `pgrep` with an end-anchored regex (`'blender-5\.2\.2-linux-x64/blender$'`), or killing by the captured PID.

**Proposed fix.** As in the earlier file; this is a second count.

**Where it'd live.** Wherever the Refiner lands the earlier item.

---

### 5 — Filling a library is a loop, not a sequence of phases, and the method has only phases `[doc-gap]`

**Grounding.** The lead's frustration was the trigger for this whole research (*"Phase 4 got too lost… we need to be way more nimble"*). Measured: 81 commits and about 48,000 words of planning since 2026-09-23, while the library grew from 12 to 17 materials. Phase04, a 90-minute content fix, was held up by re-freezing a pilot release nobody consumes. The plan agreed with the lead makes material-building a **scheduled loop** (Phase07: generate → test in the rig → fix → keep), with phases reserved for building tools. The method has no shape for "a recurring loop that produces content without opening a phase per batch". The earlier file's item 2 (the pre-release stance isn't recorded where verbs read it) is the same root seen from the release side.

**Proposed fix.** Decide whether the method gets a "loop" unit (a standing, scheduled job with its own log and a stop condition), or whether Phase07 simply defines it as a phase whose deliverable is a running loop. The Refiner should look at Phase07's discovery before deciding.

**Where it'd live.** `Workflow` (portable) or `LOCAL_DELTAS.md`. Unsure; it needs Phase07's evidence.

---

### 6 — Discovery built a rival picture of a two-ruling "fork" before checking whether the lead had already moved on `[self-error-doc-could-prevent]`

**Grounding.** Discovery Pass 1 found a 2026-07 lead directive in code docstrings (`matter_proxy.py`: Blender materials are *"recognizable, not faithful … NO overlay-network recreation"*), which collides with Phase05's purpose. I resolved it as "no fork: build a separate faithful material, leave the look-alike" and put Lead call 1 to the lead. The lead answered *"Yes - the goal indeed is to get things actually working"*, which retires the old directive outright. The directive lives **only in code docstrings**, not in any spec's decision record or a research `## Resolved`, so no doc search would have found it. It surfaced because I read the file.

**Proposed fix.** In `discovery.md` §Read: *"Lead directives quoted in code docstrings (`Lead directive … verbatim`) are rulings too. Grep the code for them in the areas the phase touches, since they are not in any `## Resolved`."*

**Where it'd live.** `discovery.md` (portable).

---

## Keep these

- **Front-loaded probes in discovery** — the Blender import probe (0 nodes) turned "maybe hand-build Blender masters" into a fact in a minute, and re-running it on 5.2.2 settled the version question the same way.
- **Asking the lead when only the lead knows** — four questions (where UE runs, the UE target, the reference, v00 vs a status field) changed the plan materially and cost one round trip.
- **Research commits to nothing; seeding is lead-directed** — the Roadmap changed only after "seed Phase05 and Phase06". That kept the lead in control while they were already confused.
- **Reading the local USD source** to answer "can USDLiveView show glass?" — it found the transparency path, and the backdrop probe overturned a stale "renders black" claim in the skill.
- **Explicit-path staging + `git diff --cached` + `git show --stat`** — a sibling session was live in the tree (untracked `tools/parity/`, modified `.gitignore`), and none of its work entered my commits.

## Dead weight

None.

## Open questions

1. **Lead decision:** should real refraction in USDLiveView be raised as an ask in `PlatformDependencies.md`? (It is research Pass 12, parked.)
2. **Refiner:** is Item 2's "no new unit words" portable? I believe so, but it came from one lead's reaction.
