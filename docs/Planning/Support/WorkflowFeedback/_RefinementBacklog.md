# Refinement Backlog — the Refiner's own ledger

**Not a `/retro`.** The inbox (`<YYMMDD>_*.md`) is the executor→refiner channel; this file
is the refiner's own. A refiner depositing into the queue it drains would invert that.

Four things live here, and nothing else:

1. **Absorbed** — items already folded in, so a later deposit doesn't re-file them
   (`retro.md` §Where it goes).
2. **Tallied, not landed** — grounded items that did not clear the bar, counted across runs.
   A second or third run of the same friction is what lands one.
3. **Cut-candidate tally and byte budget** — dead-weight flags, counted across runs.
   **Never tally a destructive-error-preventer.**
4. **Held, and Open** — accepted but not landed (with a condition that can be checked), and
   what needs a lead ruling.

Keep it as *state*, not a log: rewrite each section to what is true now. The history is in
the commits.

**The bar drain 2 used** (2026-10-11, 18 retros): an item changes a doc when it recurred in
three or more runs across two or more units, cost the lead directly, or is a contradiction with
both passages quoted. Everything else is one tally line.

---

## Absorbed

*Drain 2 (2026-10-11): the 18 retros of 2026-09-28 → 10-11. Portable items are upstream `996437d`.*

| Item | Landed in |
|---|---|
| A click's surface or fixture cannot show the thing judged: a primitive for a card, a sheet too coarse, flat light, a row clipped or equal to the start value, a tool that does not run on that machine, a click unpassable under Not-now, a fixture's state read from its name (10 items, P06 P08 P10 P12) | `discovery.md` First human test · `execute.md` §TRY (the surface sentence) · `LOCAL_DELTAS` artifact row and §Two machines |
| The lead used as an approver; a handback that leaves the state unclear; a `▶` asking for an act already done; a `<placeholder>` in a pasted command; a close that keeps testing | `execute.md` §BUILD (*for seeing, not approving*) · `execute_close.md` (*no long operation on its own*) · `AI_WorkingAgreement.md` (`Completed` opens with the state; the `▶` bullet) |
| A check that could not start, recorded as an inherited red by five phases | `execute.md` §Verify (baseline row) · `discovery.md` risk lane · `LOCAL_DELTAS` RUN row |
| A value that becomes a connection; a name sharing a prefix code selects on | `execute.md` §Verify (shape row) |
| A change whose target cannot run on the machine; what a stand-in proves; a runtime owed and unrecorded | `quick-fix.md` step 4 (fourth branch) · `LOCAL_DELTAS` second-producer row |
| Driving the lead's live GUI tool: their startup scene, framing the view, rendering it first, a viewer killed at the task limit | `execute.md` §TRY · Learnings `Blender/` B11, `ClaudeCode/` CC2 (B10 was already there) |
| Diverged trunk: the table's `reset --mixed` against *never reset past a commit you did not make* (3 runs) | `.claude/CLAUDE.md` §Git (the table: merge, and when a reset is safe) |
| A push that carries more than was approved; a foreign commit on top of yours, and under it (3 runs) | `.claude/CLAUDE.md` §Git (the `git push` row); `execute_close.md` row E points there |
| Unlabelled multi-file output paired by assumed order; the changed-on-disk notice on your own writes | `.claude/CLAUDE.md` §Git |
| `cd` in a `uv run`, a loop, a quick read (3 runs) | `.claude/CLAUDE.md` §Standalone reminders (the forms) · §Codebase search (the ban, synced from upstream) |
| No Grep tool and no Bash-less agent; saying so; which commands the shapes bind | `.claude/CLAUDE.md` §Codebase search |
| Stub textures read as a live session for three verbs | `.claude/CLAUDE.md` §Git (*measure before you assume liveness*) |
| Work pushed from the other machine invisible to `git status` | `discovery.md` Cold start 2 · `plan.md` (fetch first) |
| A Brief item under In-now with no step | `discovery.md` step list |
| A lead's proposal carried as a ruling; a ruling that closed its axis over an untested look | `discovery.md` *where rulings live* · fork test 1 |
| A quick fix graduating from research leaves its footer stale; several findings taken at once | `research.md` §Landing |
| A correction for a live run found only because the subject said so | `retro.md` (the *no channel* note) |
| A consumer's ask arriving as a research doc, sometimes unpushed; who owns a shared footer | `LOCAL_DELTAS` §Separation |
| Per-machine facts: which machine, the gate's lane set on each, hand-offs, the shared GPU | `LOCAL_DELTAS` §Two machines |
| The three-beat handback against the five; a background job's `result:` line; `SEED`/`SEEDED`; seed-then-continue in one response | upstream since drain 1 (`d005c68`, `3e3ee05`), now re-synced |
| The stale learnings-domains row; the planning-material section | `LOCAL_DELTAS` (row no longer lists; section retired, `research.md` §Landing owns it) |

*Drain 1 (2026-09-27): the 11 retros of 2026-09-23 → 27. Its portable half reached upstream only on 2026-10-11, as `691f3df`.*

| Item | Landed in |
|---|---|
| Finding ids collide across phases | upstream `NamingConventions` §Planning ids |
| `pkill -f` kills the tool's own shell | `.claude/CLAUDE.md` §Git; `execute.md` Rule 3 points there |
| Lead rulings missed because they live outside the spec (4 shapes) | `discovery.md` §Discovery discipline, *where rulings live* · fork test 1 · the numbering rule |
| An option that keeps a defect in the source of truth offered as a fork | `execute.md` §Divergence (locked-decision row) · `discovery.md` fork test 4 |
| A comparison or sensitivity from a blind instrument; probe vs harness | `execute.md` §Verify (ad-hoc-check row) · §BUILD (re-ask the loop) |
| A record taken as the event (a queued CI run) | `execute.md` §Verify (record row) |
| Changing a shape many tools parse | `execute.md` §Verify (visible-data row) |
| A Brief fact turns out false | `execute.md` §Divergence |
| The lead as the context gauge | `execute.md` §Keep the lead oriented · §STRENGTHEN item 4 |
| Tripwire under a status nudge | `execute.md` Rule 3 |
| TRY assumes a URL; the lead typing commands; a picture in chat | `execute.md` §TRY + §Handback · `discovery.md` first human test · `LOCAL_DELTAS` artifact row · `.claude/CLAUDE.md` §The deliverable surface |
| Account-level preconditions (CI) invisible to the tree; tool found via `PATH` | `discovery.md` capability claim |
| Adding files to a tree its gates enumerate; a new gate planned in the build map | `discovery.md` risk lane · build map |
| A0 arming list missed "alone / only / no need for"; an item surfaced while doing the lead's close instruction | `execute_close.md` A0 |
| An owed approval found mid-close; delegated writers authoring new rules | `execute_close.md` row A |
| No-CI close stamped provisional | `execute_close.md` row D · `LOCAL_DELTAS` CI row |
| "carry on" as the close go-ahead; replies that name no option; an item passed over repeatedly; ids and method words in lead messages; a pasted command broken by trailing prose | `AI_WorkingAgreement.md` §Working With the Lead · `execute_close.md` Prerequisite |
| Research landing too heavy for a one-sitting fix; coined unit words; stale claims about a consumer | `research.md` §Landing · §discipline |
| `/howdy` and a named tracker item | `howdy.md` |
| Private-sibling spec import; a producer's asks of other repos; vendoring from a stale clone | `ProjectFolders.md` §Setup 7 and 9 · `ADOPTING.md` §1 |
| The pre-release stance not where verbs read it | `AI_WorkingAgreement.md` §Settled practices · `.claude/CLAUDE.md` §Standalone reminders · `LOCAL_DELTAS` |
| A consumer's ruling arriving by a private id | `LOCAL_DELTAS` §Separation |
| MCP tools absent from a resumed session | Learnings `ClaudeCode/` CC1 |

---

## Tallied, not landed

One run each unless a count is given. The fix is ready to apply when the friction recurs.

| Friction | Run | Ready fix, and its home |
|---|---|---|
| The Brief never said which thing was under test and which were test inputs; the lead lost the thread | P06 | `discovery.md` Brief: name the unit under test; `execute.md` §Handback: report per unit under test |
| A fix verified on its target broke the case the lead last approved, and a calibration consumed it | P06 | `execute.md` §Verify: re-run the approved case before anything consumes the fix |
| A new tool disagreed with the reference, and the reference was the one that was wrong | P06 | `execute.md` §Verify: look at both pictures before moving the tool you own |
| A `⚠human` step the lead looked at, did not pass, and ruled to continue past | P12 | `execute.md` §TRY: a third mark, *closed by ruling, not passed* |
| The lead directs `/research` on the current step's premise | P08 | `execute.md` §Divergence row: suspend the step, name the lane switch, resume or hand off |
| A direct command refused by the classifier | P06 | `execute.md` Rule 3: hand the lead the exact `! <command>` line |
| An option that splits work out did not say where the split sits in the order | Library Coverage | `discovery.md` fork test 3 |
| Ids minted under a phase number that moved an hour later | Library Coverage | `NamingConventions` §Planning ids: a mnemonic scope until the number is stable. *(Practice has since moved there on its own: `F-GLC-`, `AT-F`.)* |
| `/howdy` named a Roadmap head entry the last close had emptied | Library Coverage | `howdy.md`: one grep of the last closed phase's ledger before naming what is next |
| No Roadmap status for discovery paused after a pass | Library Coverage | the Roadmap header: `ACTIVE (parked on <ref>)` covers a phase here too |
| A number composed while summarising the close | P08 | `execute_close.md` row A: every number in the close entry names its command |
| An Outcome only an act on the other machine can prove | P06 | `execute_close.md`: run A⁻–A, push, record *Close (in progress): held for <act>* |
| The owed lead act put in the close's one progress line, where it read as narration | P10 | `execute_close.md` row A: its own short message, as the `▶` |
| Harness nudges during the quiet close add up to row-by-row narration | P12 | `execute_close.md`: answer a nudge in a few words naming the row |
| The lead ordered the push before there was anything to look at | master adoption | `quick-fix.md` step 4: the look is owed, not waived; first line of `Next` |
| The lead reopened a session four times after `/retro`'s terminator | master adoption | `retro.md`: the terminator ends the agent's initiative; the next deposit is a `_2` |
| A research finding named a retired file as where a change lands, from a slice of it | asset tooling | `research.md`: read a file's first lines and find who imports it before naming it |
| Two edits to one table row are never separable hunks (twice in one run) | master adoption | `.claude/CLAUDE.md` §Git: the five-step rebuild recipe, in that run's retro (`git log -- docs/Planning/Support/WorkflowFeedback/261005_MasterAdoption_ResearchQuickFix_ColdStart.md`) |
| A `▶` whose next act is on the other machine | master adoption | `AI_WorkingAgreement.md` `▶` bullet |
| A Not-now item cited a tracker row that did not hold it | P12 | `discovery.md` Brief |
| A change under `tools/parity/` has no baseline rule, and rig scratch filled a quota on `/tmp` | master adoption | `LOCAL_DELTAS` RUN row. **Not landed because the quota is the other machine's and was not measurable from this one.** |

**Stack facts from single runs, not yet in `docs/Learnings/`** (check the domain file first; add on a second sighting): the rig's seam line flags any periodic texture whose boundary lands on the tile edge · fit a light factor on a probe with no material model in it (a white mirror), not on a material · `rig.py <path.mtlx> --out <scratch>` is the cross-tool one-variable probe · Storm barely renders `transmission_color` · after a `VK_ERROR_DEVICE_LOST`, read `journalctl -k` for a new Xid before relaunching · a `Monitor` on a build's progress counter floods the conversation.

---

## Cut-candidate tally

A rule is cut when the flags say it is dead weight *across runs* — not on one complaint.

| Candidate | Flags | Runs | Status |
|---|---|---|---|
| `execute.md`'s web-service framing (*up / current / reached the reader*, the browser and `curl` Verify rows) | 4 | P01, P03, P12 ×2 | Past its threshold. **It cannot be cut upstream** — web adopters need it in the build lane, and `execute_test.md` is read only in the high-rigor lane. Open 2 carries the proposal. |
| `execute_close.md` row D's provisional-stamp and CI-observed text | 1 | P12 | Tally. `LOCAL_DELTAS` already says no CI runs. |
| `research.md` orient step 2, the Documentation Map read | 2 | master adoption, asset tooling | Tally. Neither run read it; neither missed it. |
| `quick-fix.md` §from an Issue, *remove the `status:*` label* | 1 | master adoption | Tally. This repo's issues carry no labels. |

**Byte budget** (drain 1 → drain 2): `execute.md` 40,658 → 43,503 · `discovery.md` 25,336 → 28,123 · `execute_close.md` 24,983 → 26,069 · `plan.md` 33,922 → 34,137 · `research.md` 11,332 → 15,680 · `quick-fix.md` 11,987 → 14,000 · `retro.md` 11,204 → 11,397 · `LOCAL_DELTAS.md` 12,564 → 15,567 · `AI_WorkingAgreement.md` 21,825 → 22,809 · `.claude/CLAUDE.md` 13,887 → 17,417. About a third of the growth in `execute.md`, `discovery.md` and `research.md` is upstream's own since drain 1. **Every doc grew; no drain here has ended at or below where it started.**

---

## Held / deferred

| Item | Held until | Ready-to-apply fix |
|---|---|---|
| The rig baseline and scratch rule (tally, last row) | A run on the library machine confirms the `/tmp` quota and a home-disk scratch path | One clause in the `LOCAL_DELTAS` RUN row |

*(Drain 1's held `.claude/CLAUDE.md` patch landed 2026-10-11: the classifier that refused it accepted the edits in this session. Its *loop unit* item is closed: Phase11 took the shape, a phase whose deliverable is a running loop.)*

---

## Open — needs a lead ruling, not a refiner tweak

1. **Push the upstream clone.** `PeteSmalls/agentic-engineering` holds two unpushed commits in its local clone: `691f3df` (drain 1's portable half, re-landed) and `996437d` (drain 2). Drain 1's original commit was lost exactly this way: made, recorded here as the sync SHA, never pushed. **Recommendation:** push both before the next session on either repo.
2. **A streamlining pass is overdue** on `execute.md` (43.5 KB), `discovery.md` (28.1 KB) and `.claude/CLAUDE.md` (17.4 KB, loaded into every session). It needs the lead in the room (`workflow-refiner.md` §3). With it, the web-service framing: **recommendation** — upstream moves the stack-shaped paragraphs into a sibling that `execute.md` sends only a project with a web surface to, so a project with none never reads them.
3. **Should the refiner run the way the IMRSV refiner reports it does?** Its note upstream (`NOTE_FROM_IMRSV.md`, A and B): triage in batches of about twenty, default to decline, three bars, every wave ending at or below the bytes it started with, the lead picking from one screen. Drain 2 used the three bars and still grew every doc. **Recommendation:** adopt it into `workflow-refiner.md` upstream, with the byte rule as written — it is the only counter-force on record that held. Its C to F and H were not taken.
4. **This machine's gate is permanently red on two lanes** (`approval_binds_freeze`, `release_verify`; measured 2026-10-11). The cause is a git-ignored `library/staging/` from 2026-09-24. Three runs asked whether to rebuild or delete it; nobody has said. **Recommendation:** rebuild it (`stage_release.py build`) or delete it, so that a FAIL on this machine means something.
5. **Which machine regenerates the tracked `blender/asset_library/MatterLibrary.blend`, and when?** It is behind the tree, and a loader change of 2026-10-11 is not in it. One run held it back on this machine by its own inference. **Recommendation:** the library machine, at the end of every batch; then `LOCAL_DELTAS` §Two machines says so.
6. **Is asking before an Unreal launch still wanted when nothing else is using the GPU?** `LOCAL_DELTAS` §Two machines now says: check for a running engine, ask once for the batch only if one is running. That is the refiner's reading of a Phase06 instruction the lead later lifted for one session; confirm or correct it.
7. **`execute.md` says the context ceiling is about 400k; this box's context meter speaks at 450k, 600k and 750k.** Two numbers for one decision. **Recommendation:** the command doc names no number and points at the meter.
8. **The dormant `.github/workflows/gate.yml`**: keep it or remove it (carried from drain 1). **Recommendation:** keep. A data point since: a CI with both modules would have caught Phase12's break at the commit.
9. **Product and tool questions carried out of the disposed retros** (not methodology; as of each retro's date, not re-verified): what wrote 8×8 stub textures into `MatterLibrary/textures/` on 2026-09-23 and 09-27 · a committed tool to open the rig's character in the lead's Blender · the rig's seam measure against an interior boundary · a rig sweep row whose value is the article's own printing as a pass · the stand-in check for the masters builder as a gate lane · a `run_all.py` lane that warns when the masters have moved past the pinned runtime · the export add-on not enabled in the lead's Blender · the old author path in the library `.blend`'s history · `doubleSided` left free on a general go-ahead · eight articles whose new control has never been moved in a render · the lead's look at the rig's side view · the empty `docs/Planning/Phases/Complete/ignore/` folder · and from drain 1: does the publication scrub cover planning docs · a small test composition owned here · Blender's `colorSpace:name` in exports · real refraction in USDLiveView.
10. **Owed content fixes (each a `/quick-fix`, not the refiner's lane; all still present 2026-10-11):** the closed Phase03 doc's out-of-scope row names a private platform issue number in this public repo · the Roadmap's *Hair That Reads as Hair* entry still says *on cards now* after Phase09 finished cards · `docs/specs/Ontology/Taxonomy.md` still counts *4 Domains and 9 Classes* populated · `tools/conformance/codec_ab.py`'s comment *Hair = Masked's graph* · the docstrings of `tools/conformance/assert_profile.py` and `blender/addons/imrsv_lcd_export/lcd_usd_edit.py` cite the Creator Asset Profile at its old path in the platform's docs.

## Upstream queue

Portable fixes belong in [`PeteSmalls/agentic-engineering`](https://github.com/PeteSmalls/agentic-engineering),
not only here. Edit the local copy and upstream together so the re-sync is a no-op, then bump
the recorded SHA in `AGENTS.md` §Heritage — **and treat an unpushed upstream commit as not
landed: check `git merge-base --is-ancestor <sha> origin/main` in the upstream clone at the
start of each drain.**

- `691f3df` and `996437d` await the lead's push (Open 1).

## Recurring themes

- **A claim recorded as checked when the check could not see it.** A dead check, a stand-in, a clipped comparison, a fixture that cannot carry the property, a stale footer, an unrun build. Twenty-odd items across both drains; now a rule at discovery, at execute and in quick-fix. Watch whether the discovery-time check holds.
- **The lead asked to approve instead of shown.** Four rebukes in five phases. The counterweight is now in `execute.md` and the close; watch for over-correction (a run that stops asking a real product fork).
- **Two machines.** Stale checkouts, a tool that does not run where the step runs, a gate that reads differently, a runtime owed and unrecorded, a tracked file with no owner. `LOCAL_DELTAS` §Two machines is new; it restates measured state, which is the kind of row that goes stale.
- **The lead's rulings live outside the spec.** Still true (the GPU instruction lived in a closed phase doc), though this batch had fewer misses.
- **Rows that restate tree state go stale.** Two more this batch. The learnings row no longer lists anything.
- **Research into a batch of quick fixes is now the common unit here**, not the phase: four inbound-ask docs in a week. The verbs were written for one fix at a time.
