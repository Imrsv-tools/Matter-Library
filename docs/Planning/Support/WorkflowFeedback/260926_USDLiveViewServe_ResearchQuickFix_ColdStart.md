# Workflow Feedback — USDLiveViewServe / research → quick-fix / cold start

| | |
|---|---|
| **Verb** | `research → quick-fix` (a **lead-directed graduation**, research.md §Landing: the lead rejected the parked options and directed the build) |
| **Unit** | `USDLiveViewServe` (pre-phase slug: testing drafts in USDLiveView) |
| **Mode** | cold start |
| **Outcome** | done: `0f4caac` research doc (4 passes) → `9dabea1` `tools/releases/serve_to_stage.py` + skill §6a + tool listings, proved live and pushed. `b5fb595` reconciled the research Status footer (step 0, this run's own staleness). |
| **Shape** | behavior-touching (a new tool; it writes into the local Stage runtime and restarts the daemon) |
| **Confidence** | Ran fully: `/research`, `/quick-fix`, the lead's push. The loop was proved against the running Stage (list op, apply op, slider op, a stock `usdrecord` of the saved file), and the lead confirmed it in USDLiveView ("Works great"). **Not exercised:** `/discovery`, `/plan`, `/execute`. |
| **Date** | 2026-09-26 (the run spanned 2026-09-25 → 26) |

---

## Items, ranked

### 1 — Research landed a phase-sized, ceremony-heavy answer for a one-sitting build, in a project that says "bias to the smallest unit" `[self-error-doc-could-prevent]`

**Grounding.** The ask: "build them and put them in the right place so we can use them in USDLiveView." The research found the whole gap in 3 passes: Stage serves only the installed release, and nothing puts a working-tree article there. The landing then offered **four options, four lead questions, an R1 ruling, a `/discovery` phase**, and a "draft install" constrained by the approval gate, release immutability and ReleaseConflict. The lead replied: *"Why so much overhead? Make a material, serve it to stage. no versioning, no faffing around. we are VERY pre release."* The actual fix was one ~200-line script, built, proved and pushed in the same sitting. The production release lifecycle (R1 no-deploy, approval, immutability) was treated as binding on a **maintainer-box dev loop**, which it never governed.

**Proposed fix.** In research.md §Landing, or as a local weighting line: *"When the finding reduces to a change buildable and provable in one sitting, lead the landing with that: 'I can build X now as a `/quick-fix`; here is what it does.' Put the heavier options second. Constraints written for a shipped product (release gates, consumer separation) are not constraints on a local dev/test loop unless a doc says so."* The research.md Hard rule ("never slide into …") pushes toward parking, and the project weighting ("bias to the smallest unit") pushes the other way. Nothing tells the agent which wins when a probe has already proved the small fix works.

**Where it'd live.** `LOCAL_DELTAS.md` §Weighting (the pre-release stance is local) and/or `research.md` §Landing (the "lead with the one-sitting build" framing may be portable). Refiner's call.

---

### 2 — The lead's pre-release stance ("no versioning, it's useless right now, just us") is not recorded where a verb reads it `[doc-gap]`

**Grounding.** Every spec the research read (ReleaseModel, Consumers, R1 in `260923_R_StandaloneSetup.md`) describes the release machinery as the authority, with Drift notes about *production*. LOCAL_DELTAS §Weighting says "still building, not a production system", but nothing says **the release lifecycle is irrelevant to day-to-day building and testing.** The agent had to be told, forcefully. The ruling now lives only in the research doc's Pass 5 and the tool's docstring.

**Proposed fix.** Record the lead ruling (2026-09-25, verbatim above) where every verb orients: a `LOCAL_DELTAS.md` row, or `AI_WorkingAgreement.md` §Project practices. Suggested wording: *"Until the first versionable library (~200 articles), the release lifecycle is not used for building or testing. Work is served straight from the working tree (`tools/releases/serve_to_stage.py`). Do not propose versioning, freezing or approval steps for dev work."*

**Where it'd live.** `LOCAL_DELTAS.md` or `AI_WorkingAgreement.md`. **A lead-ruling record**, so the Refiner lands it (§Lanes).

---

### 3 — A skill froze a consumer's capability as a timeless fact; it went false the same day `[doc-gap]`

**Grounding.** `matter-generate` §6a said "USDLiveView has no slider controls yet (its own Phase 04)", and Phase03's out-of-scope table says "parked". USDLiveView's roadmap shows Phase 04 **COMPLETE 2026-09-25**. The stale claim is why the skill made one temp `--set` scene per slider, which is the "playing games with locations" the lead objected to. It was found only because this research happened to read the consumer's roadmap.

**Proposed fix.** (a) research.md orient step 3: when the topic is **a consumer's behaviour**, prior art includes **that consumer's own roadmap/status**, not only this repo's docs. (b) Any skill or phase line stating a consumer's limitation carries a date and names the consumer milestone that would lift it (*"no sliders as of 2026-09-25; lifts at USDLiveView Phase 04"*), so a reader knows what to recheck.

**Where it'd live.** `research.md` step 3; a skill-authoring note (unsure where skills' conventions live; possibly `ToolingConventions.md`).

---

### 4 — `pkill -f <pattern>` killed the agent's own shell `[self-error-doc-could-prevent]`

**Grounding.** Stopping the viewer with `pkill -INT -f 'python -m app.main /home/…/MatterTestBench'; kill …; …` exited 1 with no output. The pattern also matched the bash process running that command line, so it killed its own shell, and the rest of the statement never ran. Both processes were still alive. Stopping them by PID worked.

**Proposed fix.** A learning: *"Never `pkill -f` / `pgrep -f` with a pattern that appears in your own command line: it matches the shell running it. Stop by PID (capture it at launch), or bracket one character of the pattern (`app[.]main`)."* Same silent-success class as the §Editing traps.

**Where it'd live.** `docs/Learnings/<Tooling>/` (the durable learnings home), or `.claude/CLAUDE.md`'s silent-success family if the Refiner judges it portable.

---

### 5 — "Put it in the right place" meant "the running system", the same reading as CLAUDE.md's URL rule `[doc-gap]`

**Grounding.** The preview tool's own README says "Nothing is written into the repo … `<tmp>/matter-preview/`". That design choice (Phase03 Pass 2) reached the lead as "inaccessible temp places". What the lead wanted was not a better file location but **the material live in the running Stage + USDLiveView**. That is the same shape as the recorded rule "a URL means a RUNNING SERVICE", generalised: *"where can I see it" = the running system the lead tests with.*

**Proposed fix.** Widen the CLAUDE.md deliverable-surface paragraph by one sentence: *"Likewise 'put it where I can see it' means the running tool (here: served to Stage, open in USDLiveView), never a scratch file for the lead to open."*

**Where it'd live.** `.claude/CLAUDE.md` §The deliverable surface (Refiner's lane).

---

## Keep these

- **research.md §Disposable probes, "prove the negative / inspect the bytes."** Reading the actual install root (`diff -rq`, counting `.mtlx`) is what found **12 served vs 17 authored**, the real root cause. Docs alone said the install and the checkout matched (true two days earlier).
- **Verify against the running thing, not the build (quick-fix step 4, infrastructure branch).** Asking Stage's list op, then applying + setting a slider + rendering the saved file, caught **my own probe error**: the first apply targeted a group prim and rendered nothing. A "served 17 articles" print would have passed.
- **Naming the lane on graduation (research.md §Landing).** "Switching to a `/quick-fix` on your direction" kept the research doc honest (parked, then Pass 5 records the ruling) instead of silently turning research into a build.
- **§Git explicit-path staging + `git show --stat` read-back.** A sibling session had live edits (`.gitignore`, `Phase05_TestRig.md`, `tools/parity/`) through every commit. None rode along.
- **The public-repo rule.** It shaped the research doc: consumer-side facts only, no private source file names, issue numbers or box paths. A grep for home paths ran before the push.

## Dead weight

None.

## Open questions

1. **Lead decision:** confirm item 2's wording as the standing pre-release rule, and where it lives.
2. **Lead decision:** should this repo own a small test composition, instead of each box pointing `$MATTER_TEST_COMPOSITION` at a copy of USDLiveView's smoke scene? (The lead's box uses such a copy, kept outside every repo.)
3. **Owed, not done (a completed phase doc, outside this run's lane):** Phase03's out-of-scope row "USDLiveView LCD sliders … parked" is stale since 2026-09-25. It needs a dated annotation, not a deletion.
4. A sibling session is live on `docs/Planning/Phases/Future/Phase05_TestRig.md` + `tools/parity/`. If that phase is a test rig for materials, it should know `serve_to_stage.py` exists (not verified; this run did not read it).
