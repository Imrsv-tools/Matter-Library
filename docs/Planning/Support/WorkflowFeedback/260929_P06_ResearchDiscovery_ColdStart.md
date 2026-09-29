# Workflow Feedback — P06 / research → discovery / cold start

| | |
|---|---|
| **Verb** | `research → discovery` (one session: `/research` with lead-approved disposable probes, then `/discovery Phase06` on the lead's *"push it and start /discovery Phase06"*) |
| **Unit** | `P06` (research `260929_R_UnrealTestRuntimeHere.md`, spike `260929_R_Spike_UnrealRuntime.md`) |
| **Mode** | `cold start` |
| **Outcome** | `done`. The research answered "possible?" with yes. Probes 1–3 passed (an OpenPBR master by script, a headless capture, a standalone package). The Phase06 Brief is ready, with no open YOUR CALL, and pushed (`d48a009`). |
| **Shape** | `doc-only` in the repo. The probe code lived outside the repo; its sources are committed beside the spike doc. |
| **Confidence** | Ran fully: `/research` (with probes), `/discovery` Passes 1–2. **Not exercised:** `/execute`. Nothing here is about it. |
| **Date** | `2026-09-29` |

---

## Items, ranked

### 1 — On a two-machine project, discovery must `git fetch` before Pass 1 and again before the Brief ships `[doc-gap]`

**Grounding.** I wrote the Brief with **YOUR CALL 1** asking the lead to rule on the Hair master (HS-Q3). While I did, the other machine had already pushed five commits: the MAP research, with the rulings MAP-RD3 and RD6, and the Phase09 seed. They answered that call and moved the Eye master to Phase09. **I found out only because the lead said *"pull the latest MatterLibrary I think it might help us answer hair and eye questions"*.** `discovery.md`'s cold start runs `git status -sb`, which reports on the last fetch, not the remote. §*Where rulings live* says to read "`git log` since the doc you are reading was last edited", but only the local log. My local commit then had to be rebased onto theirs.

**Proposed fix.** In the discovery cold start (and in `/research`'s prior-art glance): *"Run `git fetch` and read `git log main..origin/main` before Pass 1, and again immediately before committing the Brief. A ruling pushed from another machine is invisible to `git status` and to the local `git log`."* The fetch before the commit is what would have caught this run's miss.

**Where it'd live.** `discovery.md` §Cold start (portable: any project whose collaborators push), or `LOCAL_DELTAS.md` if the Refiner judges it local, since this project runs on two machines by design (BP6).

---

### 2 — "This machine" in a doc is relative to its author; I mis-read which machine had Unreal `[self-error-doc-could-prevent]`

**Grounding.** BigPicture BP1 reads *"IMRSV Studio is not on the Linux box, where Blender 5.1 and the Stage runtime are"*. The Phase06 stub says *"runs on the UE machine"*. Those were written on the **other** machine. Reading them here, I took "this machine" to mean the machine I was on. The research doc's Pass 1 then told the lead that *"BP1 … were written because no Unreal was here"* and that Phase06 *"can run here instead"*. That was backwards: this box **is** the UE machine. The lead's *"the other one that build all the rest of this"* exposed it, and Pass 1 needed a correction commit.

**Proposed fix.** Planning docs name a machine by a **stable role name** (for example "the UE machine" and "the build machine", fixed once in `LOCAL_DELTAS.md`), never "this machine" or "here". A reader resolves the name from a check (is `UE_5.8` in `~/.config/Epic/UnrealEngine/Install.ini`? is Studio's checkout present?), not from the author's point of view.

**Where it'd live.** `LOCAL_DELTAS.md` (the two machines are this project's shape), plus a line in `research.md` §Seeds decay: *"deictic words in a seed ('this machine', 'here', 'now') resolve to the author's context, not yours."*

---

### 3 — A disposable probe that grows into real code should say that it is research, before it starts `[doc-gap]`

**Grounding.** After *"yes run it here … now is OK"*, I scaffolded a C++ Unreal project, a GameMode and a build pipeline for probes 1–3. It sat outside the repo and was disposable by design. But at no point did I tell the lead in advance that this was **research's probe lane and not Phase06**. The lead asked mid-build: *"Is this reserach for Phase 6 or have you started phase 6?"*. The answer was clean (research; offered the choice; the lead picked *"1, finish the probes"*), but the question shows the framing was not visible. `research.md` §Disposable probes covers tear-down and reproduction, not saying the lane out loud.

**Proposed fix.** In §Disposable probes: *"Before a probe that writes build code or spends GPU or compile time, say in one line: 'disposable probe under /research: outside the repo, nothing kept but the recipe; the build itself is Phase NN'. Probe code resembles the phase's step 1, and the lead cannot tell them apart from the diff."*

**Where it'd live.** `research.md` §Disposable probes.

---

### 4 — The Bash-less search rule had no tool to run on in this session `[doc-gap]`

**Grounding.** The `Grep` tool was absent (*"No such tool available: Grep"*). The agent types on offer were `Explore`, `general-purpose` and `Plan`, **all of which carry Bash**, so no Bash-less search agent existed. `.claude/CLAUDE.md` §Codebase search says to fall back to single-statement greps and to name the mode in the first message. I searched the Unreal install and the IMRSV docs with piped and recursive `grep`s under auto mode. I declared that only in the research handback, not in the first message.

**Proposed fix.** In §Codebase search: *"If neither the Grep tool nor a Bash-less agent type is listed in this session, say so in your first message and search in the main session only; command shape still binds."* The first-message declaration is easy to miss when the gap is found mid-run. Tie it to the moment the gap is discovered.

**Where it'd live.** `.claude/CLAUDE.md` §Codebase search (the Refiner's lane).

---

### 5 — The Monitor tool on a cook log floods the conversation `[doc-gap]`

**Grounding.** To watch `BuildCookRun`, I matched `Cooked packages` among the monitor's progress markers. The cook prints it every few seconds, so about 15 notifications arrived before I stopped the monitor. The stopped monitor also left its `tail -f` running until I killed it by pid. What was needed was a single notification when the background command finished, which that background job already gives.

**Proposed fix.** A `docs/Learnings/ClaudeCode/` entry: *"For a long build or cook, rely on the background command's completion notice. Watch with Monitor only for failure signatures, never for progress counters. After stopping a monitor, check that its `tail` is gone."*

**Where it'd live.** `docs/Learnings/ClaudeCode/ClaudeCode.md` (CC2).

---

## Keep these

- **Research §Disposable probes, "the reproduction must survive the box".** The probe's sources are committed beside the spike doc, so Phase06's executor starts from a working app, not from prose.
- **Asking before each GPU launch, and announcing a shader-heavy first launch** (the lead's UR-D2; the platform's rule on this machine). The 12-minute first compile was expected, not alarming, and the other agent's work was never at risk.
- **Research's "prove the negative" / "verify isolation empirically".** Running the package with `env -u DISPLAY -u WAYLAND_DISPLAY` is what proved "headless", not a log line.
- **Discovery's "probe an account-side entry path from the account side".** Reading the organisation's LFS billing gave the lead a number (August over allowance). That led straight to their question about fees and the switch to GitHub Releases, before anything was published.
- **Discovery's "distil, do not append".** Pass 2 folded the MAP rulings into the Brief (D12–D14) and retired a YOUR CALL in place, so the Brief the next session reads has one position per decision.
- **The discovery lane's four fork tests.** Test 1 turned "the Hair master" from a lead fork into a decision once MAP-RD3 was in hand, and D5's naming question was answered by LCDSchema's own sentence.

## Dead weight

None.

## Open questions

1. **Routing owed: F-P06-9 (Unreal 5.8's Substrate Eye BSDF shades one eyeball surface with `IrisMask` and `IrisDistance`) is evidence for Phase09's MAP-Q12.** It is recorded only in `Phase06_UnrealTestRuntime.md` Pass 2, because Phase09's doc was not this run's to edit. Phase09's discovery should read it there, or the lead routes it to `Phase09_HairAndEyeMasters.md` §Open questions. *(For the lead, not the Refiner.)*
2. **The probe folder `~/Documents/Unreal/Probes/MatterProbe` (4.2 GB) is still on disk**, kept deliberately for Phase06's first run (its compiled shaders are cached). It is recorded in the spike doc (UR-F11). The Phase06 close should delete it.
