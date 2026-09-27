# Refinement Backlog — the Refiner's own ledger

**Not a `/retro`.** The inbox (`<YYMMDD>_*.md`) is the executor→refiner channel; this file
is the refiner's own. A refiner depositing into the queue it drains would invert that.

Three things live here, and nothing else:

1. **Absorbed** — items already folded in, so a later deposit doesn't re-file them
   (`retro.md` §Where it goes).
2. **Cut-candidate tally** — dead-weight flags, counted across runs. A candidate that keeps
   getting flagged graduates to a cut. **Never tally a destructive-error-preventer.**
3. **Held / deferred** — accepted but not yet landed, with the reason and the ready-to-apply
   fix. **Written as a condition that can be checked, never as a justification** — a hold
   whose precondition has since been met is invisible to every sweep.

Keep it as *state*, not a log: rewrite each section to what is true now. The history is in
the commits.

---

## Absorbed

*Drain 1 (2026-09-27): the 11 retros of 2026-09-23 → 27. Per-item dispositions are in the drain's commit message.*

| Item | Landed in |
|---|---|
| Finding ids collide across phases | upstream `NamingConventions` §Planning ids (re-sync to `ebbfab3`) |
| `pkill -f` kills the tool's own shell | `execute.md` Rule 3 (upstream `45d9f39`); the move to `.claude/CLAUDE.md` is held below |
| Lead rulings missed because they live outside the spec (4 shapes) | `discovery.md` §Discovery discipline, *where rulings live* · fork test 1 · the numbering rule |
| An option that keeps a defect in the source of truth offered as a fork | `execute.md` §Divergence (locked-decision row) · `discovery.md` fork test 4 |
| A comparison or sensitivity from a blind instrument; probe vs harness | `execute.md` §Verify (ad-hoc-check row) · §BUILD (re-ask the loop) |
| A record taken as the event (a queued CI run) | `execute.md` §Verify (record row) |
| Changing a shape many tools parse | `execute.md` §Verify (visible-data row) |
| A Brief fact turns out false | `execute.md` §Divergence (new row) |
| The lead as the context gauge | `execute.md` §Keep the lead oriented · §STRENGTHEN item 4 |
| Tripwire under a status nudge | `execute.md` Rule 3 |
| TRY assumes a URL; the lead typing commands; a picture in chat | `execute.md` §TRY + §Handback · `discovery.md` first human test · `LOCAL_DELTAS` artifact row |
| Account-level preconditions (CI) invisible to the tree; tool found via `PATH` | `discovery.md` capability claim |
| Adding files to a tree its gates enumerate | `discovery.md` risk lane |
| A new gate planned in the build map | `discovery.md` build map |
| A0 arming list missed "alone / only / no need for" | `execute_close.md` A0 (now a class); `plan.md` points to it |
| An item surfaced while doing the lead's close instruction | `execute_close.md` A0 (3) |
| An owed approval found mid-close | `execute_close.md` row A · `LOCAL_DELTAS` producer row |
| No-CI close stamped provisional | `execute_close.md` row D · `LOCAL_DELTAS` CI row |
| A push publishing a sibling's commit | `execute_close.md` row E (the always-loaded home is held below) |
| "carry on" as the close go-ahead; replies that name no option; an item passed over repeatedly | `AI_WorkingAgreement.md` §Working With the Lead (reply-reading rule) · `execute_close.md` Prerequisite |
| Doc-internal ids and method words in lead messages | `AI_WorkingAgreement.md` §Working With the Lead |
| A pasted command broken by trailing prose | `AI_WorkingAgreement.md` `▶` bullet |
| Delegated writers authoring new rules | `execute_close.md` row A |
| Research landing too heavy for a one-sitting fix; coined unit words; stale claims about a consumer | `research.md` §Landing · §discipline |
| `/howdy` and a named tracker item | `howdy.md` |
| Private-sibling spec import; a producer's asks of other repos | `ProjectFolders.md` §Setup 7 and 9 |
| Vendoring from a stale clone; the bootstrap writing `LOCAL_DELTAS` | upstream `ADOPTING.md` §1 |
| Dangling `§The gate registry` pointer | `execute.md` §Verify (the CAUGHT row is self-contained) |
| The pre-release stance not where verbs read it | `AI_WorkingAgreement.md` §Settled practices · `LOCAL_DELTAS` §Weighting + producer row |
| Stale RUN row, learnings row, orientation gate line; no exporter baseline | `LOCAL_DELTAS` · `AI_Orientation.md` |
| A consumer's ruling arriving by a private id | `LOCAL_DELTAS` §Separation |
| MCP tools absent from a resumed session | `docs/Learnings/ClaudeCode/` CC1 |

---

## Cut-candidate tally

A rule is cut when the flags say it is dead weight *across runs* — not on one complaint.

| Candidate | Flags | Runs | Status |
|---|---|---|---|
| `execute.md`'s web-service framing (URLs, browser headers, `allowedDevOrigins`) | 2 | P01, P03 | **Generalised, not cut** (2026-09-27): §TRY now says *where the lead reaches it*, and `LOCAL_DELTAS` translates it. The browser rows stay (other projects need them). A third flag → propose moving them to `execute_test.md`. |

**Byte budget** (measured before → after drain 1): `discovery.md` 21,108 → 25,336 · `execute.md` 36,566 → 40,658 · `execute_close.md` 23,451 → 24,983 · `plan.md` 33,894 → 33,922 · `research.md` 10,108 → 11,332 · `LOCAL_DELTAS.md` 10,479 → 12,564 · `AI_WorkingAgreement.md` 19,081 → 21,825. **`execute.md` and `discovery.md` are due a streamlining pass** (`workflow-refiner.md` §3) — needs the lead in the room.

---

## Held / deferred

| Item | Held until | Ready-to-apply fix |
|---|---|---|
| **Seven edits to `.claude/CLAUDE.md`** (six portable, also for `templates/.claude/CLAUDE.md` upstream; one local) | The lead applies them, or allows the refiner to. The auto-mode classifier refuses agent edits to `.claude/CLAUDE.md` as self-modification (2026-09-27). | §*CLAUDE.md patch* below |
| **A "loop" unit for filling the library** (BigPicture item 5) | Phase08's discovery decides whether content volume runs as a standing loop | If it does: a phase whose deliverable is a running loop — no new unit word (`research.md` now forbids coining one). |

### CLAUDE.md patch (apply to both files; the last item is local only)

1. **§The deliverable surface**, after *"not to read a prettier copy of your document."* — add: **The same holds for *"where can I see it"* or *"put it where I can use it"*: the running system they test with (`LOCAL_DELTAS.md` names it). Open it for them; never leave a scratch file for them to find.**
2. **§Lanes**, replace *"The one exception is the lead asking directly — …drift."* with: **The exceptions are the lead asking directly** — then it is lead-directed work, and say so in your report so the next reader can tell it from drift — **and the adoption bootstrap**, which writes `LOCAL_DELTAS.md` and the entry docs until it closes (`ADOPTING.md`).
3. **§Git**, after *"a process rule cannot change harness behaviour."* — add: **If the harness demands a worktree anyway** (writes refused with *"call EnterWorktree first"*), **do not create one**: stop, say so, and offer a new session launched from the repo root, or writes through Bash on the lead's go-ahead.
4. **§Git**, before the `-F` commit-message rule — add: **⛔ IMMEDIATELY BEFORE `git push`, LIST WHAT IT CARRIES — `git log --format='%h %s' origin/main..HEAD` — AND READ EVERY LINE.** On a shared trunk a push publishes every session's commits; name any that are not yours to the lead before pushing. *(A sibling committed between a clean `git status` and a push, and its doc was published with the push.)* — then trim `execute_close.md` row E to a pointer.
5. **§Git**, same place — add: **The same measurement trap outside git:** a harness *"changed on disk since you last read it"* notice fires on your **own** Bash writes too — `git diff <path>` against what you wrote before you suspect a sibling; and output from several files without per-line names (`grep -h`, stacked `head`) pairs with its inputs only by the order you assumed — label it (`grep -H`).
6. **§Git**, after the backtick rule — move the `pkill -f` rule here from `execute.md` Rule 3 (it recurred in research, quick-fix and setup sessions, which never read `execute.md`), and leave Rule 3 a one-line pointer.
7. **Local only — §Standalone reminders**, after *Bias to the smallest unit*: **Pre-release: no release ceremony** (lead, 2026-09-25; re-affirmed 2026-09-27). Until the first versionable library, releases, freezes and approvals never gate building, testing or serving a draft — `.ai/AI_WorkingAgreement.md` §Settled practices owns it.

---

## Open — needs a lead ruling, not a refiner tweak

1. **The handback format contradicts itself upstream.** `AI_WorkingAgreement.md` specifies five beats (*Completed · Next · Stopping · Blockers · ▶*; lead-specified 2026-08-25). `execute.md` and `discovery.md` (from the 2026-08-29 rewrite) say *"Three beats: Done · Notes · ⛔ YOUR CALL"* and cite the Working Agreement for a *"YOUR CALL entry gate"* that has never existed there. Runs here use `YOUR CALL`. **Recommendation:** keep the five beats, map `YOUR CALL` to `Blockers` + `▶` in every verb's Handback section, and drop the dangling gate pointer. An upstream change touching every verb.
2. **`approval_binds_freeze` has been red on `main` since Phase04** (the pilot's re-approval is owed). A permanently red gate teaches every run that FAIL is normal. **Recommendation:** re-approve once now (the maintainer runs `promote_release.py 0.1.0 --approver <you> --force`); separately decide whether the release lanes SKIP with a pre-release reason until the first release (a gate change, so yours).
3. **The dormant `.github/workflows/gate.yml`**: keep it for the Contribution Path phase, or remove it. **Recommendation:** keep it (Don't Delete Spec Functionality); the `LOCAL_DELTAS` CI row now tells every close it never runs.
4. **Product questions carried out of the disposed retros** (not methodology; recorded so they are not lost): does the publication scrub cover planning docs? · should this repo own a small test composition instead of each box pointing at a copy? · strip Blender 5.2's `colorSpace:name` from exports? · raise real refraction in USDLiveView as a `PlatformDependencies` ask? · make the rig's scorecard a gate (Phase08)?
5. **An owed content fix (a `/quick-fix`, not the refiner's lane):** the closed Phase03 doc's out-of-scope row *"USDLiveView LCD sliders … parked"* has been stale since 2026-09-25, and it names a private platform issue number in this public repo.

## Upstream queue

Portable fixes belong in [`PeteSmalls/agentic-engineering`](https://github.com/PeteSmalls/agentic-engineering),
not only here. **A portable fix landed only locally is how N projects end up with N
divergent methodologies.** Edit the local copy and upstream together so the re-sync is a
no-op, then bump the recorded SHA in `AGENTS.md` §Heritage.

- **Drain 1's portable commit is made in the local upstream clone and awaits the lead's push** (its SHA is recorded in `AGENTS.md` §Heritage).
- The six portable `CLAUDE.md` edits above are held with the local ones.

## Recurring themes

- **The lead's rulings live outside the spec** — research passes, closed phase logs, docstrings, `git log` — and runs fork or sequence past them. Four shapes in four days.
- **Release ceremony applied to pre-release work.** Five retros, three lead rebukes. Watch whether the settled practice holds; the always-loaded pointer is held with the `CLAUDE.md` patch.
- **An instrument that cannot see the thing**: a saturated comparison, a harness at the wrong scale, a probe that is not the harness, a surface too coarse to show the defect. Six items, two phases.
- **Rows that restate tree state go stale.** The RUN row, the learnings row and the orientation gate line all went stale within days. Rows now point to the owning doc instead of restating counts.
- **The lead as the gauge**: of context, and of an unanswered question. Both now have a rule on the agent's side.
