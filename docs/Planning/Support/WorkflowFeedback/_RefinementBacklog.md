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

*Drain 3 (2026-10-14): the 6 retros of 2026-10-14 (MatterSitePipeline, P09, P11 close, PlatformAsks, RoadmapOrder, SetAsks). Portable half upstream `8108e84` + `9de2459`, pushed 2026-10-14.*

| Item | Landed in |
|---|---|
| An agent's gloss beside a ruling quoted as the ruling two weeks later; a ruling given by reference (*"yes 1"*) recorded with consequences the lead never saw (2 runs, cost the lead twice) | `AI_WorkingAgreement.md` §Working With the Lead (the rule moved there from `discovery.md`, which now points; every verb records rulings) · `research.md` tension row |
| A one-sitting offer or recommendation made before its premise was taken: a count not measured, a second writer of the value, a builder that reads the file (3 runs) | `research.md` §Landing, the ⛔ one-sitting rule |
| A coined noun that collided with a Glossary headword (*probe*; a 34-hit rename) | `research.md` orient item 2 |
| The lead's own shape, already shipped in a sibling repo, designed past | `AI_WorkingAgreement.md` *PRECEDENT COUNTS* |
| Contract vocabulary instead of the lead's model; rulings amended within the hour (corroborated by IMRSV's note 3, six runs) | `AI_WorkingAgreement.md`, the plain-words sentence |
| A sequence for the lead to cut, given as a dependency table | `research.md` §Landing |
| A close ordered by a ruling that names its own steps (a sitting, a rebuild), against *"by the close the lead has seen everything"* | `execute_close.md` Prerequisite |
| Row B's *"one level deeper"* false here: Phases 09, 10, 11, 13 and 14 were numbered and left in `Phases/Future/` (14 while this drain ran). Source: upstream's own `research.md` seeded numbered stubs into `Future/`, the template Roadmap modelled it, and the Workflow's `ACTIVE` row coupled the move to status | `research.md` seed path · `discovery.md` numbering act · Workflow `ACTIVE` row · Glossary `ACTIVE` row (here and the template) · template Roadmap. Row B was right; no `LOCAL_DELTAS` row |
| The consumer handshake: a ruling made in a consumer's session never arriving (CC0), an ask filed in the consumer's own phase doc, owed asks found by reading everything, a drafted ledger id gone stale, a ruling binding both repos, a private fact past the id grep (6 items, 3 runs) | `LOCAL_DELTAS` §Separation |
| A pathspec commit and the shared index (the restore dance only before a commit from the index; a new file is `git add`ed first; read-back chained with `&&`) · backticks in any double-quoted argument, as an Editing rule · the search-mode line first · a private fact past the id grep · the skills' unconditional never-push · the preview cannot judge scale · a batch's owed lines. Held for the classifier, applied on the lead's go-ahead the same day | `.claude/CLAUDE.md` §Git, §Editing, §Codebase search, *The repo is PUBLIC* · `/matter-generate` hard rules and §6 · `/matter-batch` hard rules and hand back |
| Support docs (lead-directed, this drain): no Glossary rows for the rig, the Moved verdict, `rejudge` rows, scale grids, HDRIs; `CodingStandards.md` still the template's banner pointing at `docs/architecture/` | `docs/Glossary.md` · `docs/CodingStandards.md` |

*Drain 2 (2026-10-11): the 18 retros of 2026-09-28 → 10-11. Portable items are upstream `996437d`; `d271d0c` restores a sibling drain's commit that the re-landing overwrote.*

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
| A new tool disagreed with the reference, and the reference was the one that was wrong; a probe's printed numbers hid two artefacts its picture showed | P06, P09 | `execute.md` §Verify and `research.md` §Disposable probes: a finding from a visual tool is read off its picture, not its numbers |
| A close's own workaround (a hand edit, a `/tmp` script standing in for a tool) was the missed correction | P11 | `execute_close.md` row A: list every workaround the close used; each is a candidate CORRECTION |
| A wish-list row built by `/matter-generate` outside a batch has no honest state; `kind: rejudge, state: queued` was improvised and worked | SetAsks | `/matter-generate` §1, one sentence; or a `drafted` state in `wishlist.py` |
| How a draft reaches a consumer on the other machine (rebuild the `.blend`, re-serve Stage, push, `git lfs pull`) | SetAsks | `/matter-generate` §7, a short *usable elsewhere* section; waits on Open 5 |
| A `⚠human` step the lead looked at, did not pass, and ruled to continue past | P12 | `execute.md` §TRY: a third mark, *closed by ruling, not passed* |
| The lead directs `/research` on the current step's premise | P08 | `execute.md` §Divergence row: suspend the step, name the lane switch, resume or hand off |
| A direct command refused by the classifier | P06 | `execute.md` Rule 3: hand the lead the exact `! <command>` line |
| An option that splits work out did not say where the split sits in the order | Library Coverage | `discovery.md` fork test 3 |
| Ids minted under a phase number that moved an hour later | Library Coverage | `NamingConventions` §Planning ids: a mnemonic scope until the number is stable. *(Practice has since moved there on its own: `F-GLC-`, `AT-F`.)* |
| `/howdy` named a Roadmap head entry the last close had emptied | Library Coverage | `howdy.md`: one grep of the last closed phase's ledger before naming what is next |
| No Roadmap status for discovery paused after a pass | Library Coverage | the Roadmap header: `ACTIVE (parked on <ref>)` covers a phase here too |
| A number composed while summarising the close; a rig-scene size written from memory into a batch summary (*2 m*; the floor is 1 m) | P08, SetAsks | `execute_close.md` row A and `/matter-batch` §6: every number written names its source (a command, a file's constant) |
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
| `execute.md` read in full (43.5 KB) for a run whose argument names the close | 1 | P11 | Tally. Fix when it lands: the `/execute` pointer routes a close straight to `execute_close.md`, which cites `execute.md` by section ten times, so those are read on demand. |

**Byte budget, drain 3** (before → after): `research.md` 15,953 → 16,739 · `discovery.md` 28,291 → 28,344 · `execute_close.md` 26,170 → 26,410 · `LOCAL_DELTAS.md` 15,913 → 16,796 · `AI_WorkingAgreement.md` 22,809 → 24,020 · Workflow +5 · `.claude/CLAUDE.md` 17,417 → 18,192 · `/matter-generate` 16,769 → 17,160 · `/matter-batch` 11,973 → 12,234. **Grew again, by about 4.6 KB:** every item that landed passed the bar, and the cuts that would pay for them are the streamlining pass (Open 2), which needs the lead.

**Byte budget** (drain 1 → drain 2): `execute.md` 40,658 → 43,503 · `discovery.md` 25,336 → 28,123 · `execute_close.md` 24,983 → 26,069 · `plan.md` 33,922 → 34,137 · `research.md` 11,332 → 15,680 · `quick-fix.md` 11,987 → 14,000 · `retro.md` 11,204 → 11,397 · `LOCAL_DELTAS.md` 12,564 → 15,567 · `AI_WorkingAgreement.md` 21,825 → 22,809 · `.claude/CLAUDE.md` 13,887 → 17,417. About a third of the growth in `execute.md`, `discovery.md` and `research.md` is upstream's own since drain 1. **Every doc grew; no drain here has ended at or below where it started.**

---

## Held / deferred

| Item | Held until | Ready-to-apply fix |
|---|---|---|
| The rig baseline and scratch rule (tally, last row) | A run on the library machine confirms the `/tmp` quota and a home-disk scratch path | One clause in the `LOCAL_DELTAS` RUN row |

*(Drain 1's held `.claude/CLAUDE.md` patch landed 2026-10-11: the classifier that refused it accepted the edits in this session. Its *loop unit* item is closed: Phase11 took the shape, a phase whose deliverable is a running loop.)*

---

## Open — needs a lead ruling, not a refiner tweak

1. *(Closed 2026-10-11: both repos were pushed on the lead's word. Upstream is at `d271d0c`.)*
2. **A streamlining pass is overdue** on `execute.md` (43.5 KB), `discovery.md` (28.1 KB) and `.claude/CLAUDE.md` (17.4 KB, loaded into every session). It needs the lead in the room (`workflow-refiner.md` §3). With it, the web-service framing: **recommendation** — upstream moves the stack-shaped paragraphs into a sibling that `execute.md` sends only a project with a web surface to, so a project with none never reads them.
3. **Should the refiner run the way the IMRSV refiner reports it does?** Its note upstream (`NOTE_FROM_IMRSV.md`, A and B): triage in batches of about twenty, default to decline, three bars, every wave ending at or below the bytes it started with, the lead picking from one screen. Drain 2 used the three bars and still grew every doc. **Recommendation:** adopt it into `workflow-refiner.md` upstream, with the byte rule as written — it is the only counter-force on record that held. Its C to F and H were not taken.
4. **This machine's gate is permanently red on two lanes** (`approval_binds_freeze`, `release_verify`; measured 2026-10-11). The cause is a git-ignored `library/staging/` from 2026-09-24. Three runs asked whether to rebuild or delete it; nobody has said. **Recommendation:** rebuild it (`stage_release.py build`) or delete it, so that a FAIL on this machine means something.
5. **Which machine regenerates the tracked `blender/asset_library/MatterLibrary.blend`, and when?** It is behind the tree, and a loader change of 2026-10-11 is not in it. One run held it back on this machine by its own inference. Since: SetAsks found it 27 articles behind and rebuilt it twice on the lead's ask; the Phase11 close rebuilt it by ruling; Stage's dev catalog was 7 days stale the same way. **Recommendation:** the library machine, at the end of every batch, with a Stage re-serve (`serve_to_stage.py --no-restart`); then `LOCAL_DELTAS` §Two machines and `/matter-batch`'s hand back say so, and the tallied *usable elsewhere* section lands with it.
6. **Is asking before an Unreal launch still wanted when nothing else is using the GPU?** `LOCAL_DELTAS` §Two machines now says: check for a running engine, ask once for the batch only if one is running. That is the refiner's reading of a Phase06 instruction the lead later lifted for one session; confirm or correct it.
7. **`execute.md` says the context ceiling is about 400k; this box's context meter speaks at 450k, 600k and 750k.** Two numbers for one decision. **Recommendation:** the command doc names no number and points at the meter.
8. **The dormant `.github/workflows/gate.yml`**: keep it or remove it (carried from drain 1). **Recommendation:** keep. A data point since: a CI with both modules would have caught Phase12's break at the commit.
9. **Product and tool questions carried out of the disposed retros** (not methodology; as of each retro's date, not re-verified): what wrote 8×8 stub textures into `MatterLibrary/textures/` on 2026-09-23 and 09-27 · a committed tool to open the rig's character in the lead's Blender · the rig's seam measure against an interior boundary · a rig sweep row whose value is the article's own printing as a pass · the stand-in check for the masters builder as a gate lane · a `run_all.py` lane that warns when the masters have moved past the pinned runtime · the export add-on not enabled in the lead's Blender · the old author path in the library `.blend`'s history · `doubleSided` left free on a general go-ahead · eight articles whose new control has never been moved in a render · the lead's look at the rig's side view · the empty `docs/Planning/Phases/Complete/ignore/` folder · and from drain 1: does the publication scrub cover planning docs · a small test composition owned here · Blender's `colorSpace:name` in exports · real refraction in USDLiveView. And from drain 3: `wishlist.py review` (classify every `built` row) and `keep --clean`, the by-verdict review rebuilt ad hoc twice (P11 close) · why Unreal draws a white emitter at 0.75 of Storm and Blender, a warm one at 1.12 (batch `261004-1`; unchecked since Phase12's emission ports) · a Set's recorded release while it uses drafts (SM-Q5) · a gate form for a Set root that assembles part files (the platform's A8) · keep or redo on batch `261004-1`'s five rows (the maintainer's).
10. **Owed content fixes (each a `/quick-fix`, not the refiner's lane; all still present 2026-10-11):** the closed Phase03 doc's out-of-scope row names a private platform issue number in this public repo · the Roadmap's *Hair That Reads as Hair* entry still says *on cards now* after Phase09 finished cards · `docs/specs/Ontology/Taxonomy.md` still counts *4 Domains and 9 Classes* populated · `tools/conformance/codec_ab.py`'s comment *Hair = Masked's graph* · the docstrings of `tools/conformance/assert_profile.py` and `blender/addons/imrsv_lcd_export/lcd_usd_edit.py` cite the Creator Asset Profile at its old path in the platform's docs.
11. **Whose job is a ruling about the library made in a consumer's session?** Drain 3 landed this repo's half (orient sweeps the consumers, `LOCAL_DELTAS` §Separation). **Recommendation:** the consumer also leaves a ledger line on this side when it records one; that is the platform refiner's to adopt, and upstream's once a second producer has the shape.
12. **The deferred additions Phase11 left with no owning phase** (Edges01's curvature input; the library limits F-P11-9, -16, -17; soft coverage on Masked; the rig's surround and gem size): seed a *masters refinement* phase, or leave them in Phase11's ledger until a phase claims them? *(From the P11 close retro.)*
13. **Phase13 and Phase14 are numbered and still in `Phases/Future/`** (Phase13 being edited by a live session at drain time). Under the rule drain 3 sharpened, each moves to `Phases/` with its Roadmap pointer, by whichever session holds it. **Recommendation:** the next `/discovery` on each does it in its first commit.

## Upstream queue

Portable fixes belong in [`PeteSmalls/agentic-engineering`](https://github.com/PeteSmalls/agentic-engineering),
not only here. Edit the local copy and upstream together so the re-sync is a no-op, then bump
the recorded SHA in `AGENTS.md` §Heritage — **and treat an unpushed upstream commit as not
landed: check `git merge-base --is-ancestor <sha> origin/main` in the upstream clone at the
start of each drain.**

- Nothing awaits a push (2026-10-14: drain 3 pushed as `8108e84` + `9de2459`, built in a private clone so the shared clone's checkout was never touched; `AGENTS.md` §Heritage bumped).
- **The shared clone's `main` sits on `c723ba4`, ahead 1 and behind 10** — drain 1's commit that never reached upstream, re-landed there as `691f3df`. Not reset: it was not this drain's to discard. A drain that needs the clone's `main` asks the lead first.
- **IMRSV's note 3 (`ef1a8b8`) landed a three-line question form in its own repo, unproven:** what a user does and what happens today · the choices as the lead would see them · `Checked:`. Drain 3's plain-words sentence is the same fault seen from here; when IMRSV's form proves out upstream, it replaces that sentence rather than sitting beside it.
- **A cross-repo session's retro** (MatterSitePipeline's question): friction with this repo's machinery is filed here; friction met in a sibling repo goes to that repo's inbox.
- **The upstream clone is a shared tree too.** Another project's refiner committed into it mid-drain on 2026-10-11, and files prepared from the earlier tip were written over three of its changes and pushed; `d271d0c` restored them. **`git rev-parse HEAD` in the clone immediately before writing any file prepared from an earlier read of it** — `git status` cannot show a commit that has already landed.

## Recurring themes

- **A claim recorded as checked when the check could not see it.** A dead check, a stand-in, a clipped comparison, a fixture that cannot carry the property, a stale footer, an unrun build. Twenty-odd items across both drains; now a rule at discovery, at execute and in quick-fix. Watch whether the discovery-time check holds.
- **The lead asked to approve instead of shown.** Four rebukes in five phases. The counterweight is now in `execute.md` and the close; watch for over-correction (a run that stops asking a real product fork).
- **Two machines.** Stale checkouts, a tool that does not run where the step runs, a gate that reads differently, a runtime owed and unrecorded, a tracked file with no owner. `LOCAL_DELTAS` §Two machines is new; it restates measured state, which is the kind of row that goes stale.
- **The lead's rulings live outside the spec.** Still true (the GPU instruction lived in a closed phase doc), though this batch had fewer misses.
- **Rows that restate tree state go stale.** Two more this batch. The learnings row no longer lists anything.
- **Research into a batch of quick fixes is now the common unit here**, not the phase: four inbound-ask docs in a week, and five of drain 3's six retros. The verbs were written for one fix at a time.
- **An agent's reading stored as the lead's ruling.** A gloss quoted as the ruling, a by-reference yes carrying unstated consequences, contract words standing in for the lead's model. The rule now sits in the Working Agreement, where every verb reads it; watch whether a gloss still gets quoted.
- **The library and its consumers drift apart between sessions.** Rulings, asks and ledger ids made on one side and not seen on the other. `LOCAL_DELTAS` §Separation now has orient sweep for them; Open 11 holds the consumer's half.
