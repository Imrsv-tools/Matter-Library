# Workflow Feedback — MasterAdoption / Research → Quick Fix / Cold start

| | |
|---|---|
| **Verb** | `research → quick-fix → quick-fix` (one session: a `/research`, then two quick fixes at the lead's direction, then a push) |
| **Unit** | research slug `MasterAdoption` (`docs/Planning/Research/261005_R_PlatformMasterAdoptionAsks.md`; ledger row M7) |
| **Mode** | cold start |
| **Outcome** | done — a consumer's request reviewed (Pass 3), recorded on the ledger (`228bb2f`), built as switches in the Unreal master builder (`a66377c`), pushed, and the research doc reconciled with a committed check (`2e9e7a1`). **Built, not run:** this machine has no Unreal |
| **Shape** | behavior-touching (one script under `unreal/`), with docs |
| **Confidence** | Ran fully: `/research`, `/quick-fix` twice, `/retro`. **Not exercised:** disposable probes, a Roadmap seed, the from-issue close. **Not read:** `Methodology/AgenticEngineering_DocumentationMap.md`, which `research.md` lists in its orient. Item 6 is inferential on what a `/quick-fix` on a machine with Unreal would have done |
| **Date** | 2026-10-05 |

**A second session was live on the tree throughout** (`/execute Phase12`, steps 12.4 and 12.5). Items 1, 3 and 4 come from sharing the tree with it. **Two corrections to its phase doc are owed and are deposited here, not landed** (§Corrections owed to the live run).

---

## Items, ranked

### 1 — "Rebuild your change against `git show HEAD:<path>`" is one sentence for a recipe this repo needs every time two sessions touch the ledger `[doc-gap]`

**Grounding.** `PlatformDependencies.md` holds each ask as one table row, which is one line of 1,000 – 3,000 characters. The Phase12 session had an uncommitted addition at the end of M6's line. This run had to change the middle of that same line and add M7 on the next line, which lands in the same hunk. So the filtered stage (`git diff` → hand-remove the foreign hunk) could not apply, twice in one session. `.claude/CLAUDE.md` §Git covers this case in one clause: *"do not filter: rebuild your change against `git show HEAD:<path>` and apply that."* What worked, both times:
1. `git show HEAD:<path> > /tmp/head_copy`.
2. One small script applies the **same** anchored substitutions to the working-tree file and to the copy, and refuses to write either unless every anchor occurs exactly once in both.
3. `diff -u --label a/<path> --label b/<path> <pristine HEAD copy> <edited copy> > patch`, then `git apply --cached --check` and `git apply --cached`.
4. `git commit -F <msg>` with no pathspec, in the same call.
5. Read back: `git show --stat <sha>`, **and `git diff --stat -- <path>` must now show exactly the sibling's change and nothing else.**

Step 5's second half is the check that the sibling's work survived; nothing in §Git names it. The Phase12 session's own retro confirms from the other side that its hunk was intact.

**Proposed fix.** Under the filtered-stage rule, write the five steps above as the inseparable case's recipe, and add: *"a Markdown table row is one line, so any two edits to one row are inseparable and an added row shares a hunk with its neighbour: on a ledger, expect this case, not the filter."*

**Where it'd live.** `.claude/CLAUDE.md` §Git (portable: any project with one-line-per-record docs and a shared tree).

---

### 2 — `/quick-fix` has no VERIFY branch for "this machine cannot run the thing I am changing" `[doc-gap]`

**Grounding.** The lead: *"Build everything we can build here please so we can get it over to the other system"*. The change was to `unreal/MatterRuntime/Scripts/build_masters.py`, which runs only inside Unreal's editor, and this machine has no Unreal. `quick-fix.md` step 4 has three branches (infrastructure, user-observable, non-observable) and each ends in something run here. Read literally, the change was either unverifiable or *"non-observable ⇒ the compile is sufficient"*, and `py_compile` proves nothing about a script whose every call is into an absent module. The run built a recording stand-in for the `unreal` module and compared the builder's calls before and after: identical with no switch set (4,436 calls), and each switch changing only its own thing. It then said **"built, not run"** in the commit subject, the ledger row, the tooling doc and the handback, and named the two runs that would prove it.

**Proposed fix.** A fourth branch in step 4: *"The target cannot run on this machine (an engine, a device, a consumer's app). Then: (a) prove the path you did NOT mean to change is unchanged, structurally (a recorded call trace, a generated artifact diffed); (b) put **built, not run** in the commit subject and in every doc line that describes the change; (c) name the exact run, and the machine, that proves the rest. A stand-in proves what your code asks for and nothing about what the absent system does: say so in those words."*

**Where it'd live.** `quick-fix.md` step 4 (portable). A local pointer in `LOCAL_DELTAS.md`'s RUN row: a change under `unreal/` cannot be run where there is no engine.

---

### 3 — A push approved for N commits can carry N + 1 `[doc-gap]`

**Grounding.** The handback said `main` was 12 commits ahead and named whose they were; the lead replied *"push it"*. Before pushing, `git log origin/main..HEAD` showed 13: the Phase12 session had committed step 12.4 in between. A plain `git push` would have published a commit the lead had not been shown. The run pushed `git push origin <sha>:refs/heads/main` up to its own last commit and reported the held-back one.

`_RefinementBacklog.md` already holds *"immediately before `git push`, list what it carries"* (Held, item 4). This is the other half: what to do when the list has grown since the approval.

**Proposed fix.** Add to that held rule: *"If the list is longer than what the lead approved, push the approved tip by value — `git push origin <sha>:refs/heads/main` — and report what stayed behind."* And a row in the measurement table: `git push` | the tree's tip, including commits that landed after the approval | `git push origin <approved-sha>:refs/heads/main`.

**Where it'd live.** `.claude/CLAUDE.md` §Git, with the held item.

---

### 4 — The table's cure for a diverged trunk would have un-committed eight of another session's commits `[doc-gap]`

**Grounding.** *"can you pull"* met a tree 8 ahead, 1 behind, with nine dirty files, none of the eight commits this run's. The §Git table's last row reads: `git rebase` to converge a diverged trunk → `git reset --mixed origin/main`, then re-stage your paths. Here that would have moved `main` back past eight Phase12 commits and left their content as loose changes in a tree a live session was writing. The run instead checked that the index was empty and that the one incoming path overlapped no dirty path, then ran `git merge --no-edit origin/main`, following three earlier merge commits in `git log --merges`. The same section's *"never `reset` past a commit you did not make"* forbids the row's own advice in this state, and nothing joins the two.

**Proposed fix.** Scope the row: *"…`git reset --mixed origin/main` **only when every local commit ahead of the remote is yours**. Otherwise merge: `git diff --cached --stat` empty, `git diff --name-only HEAD...origin/main` disjoint from `git status -s`, then `git merge --no-edit origin/main`."*

**Where it'd live.** `.claude/CLAUDE.md` §Git.

---

### 5 — A consumer's request arrives as a research doc pushed into this repo, and no doc says so `[doc-gap]`

**Grounding.** The lead's whole brief was *"another system has made a materials request... can you pull and see"*. Finding the request took a fetch, a look at the open issues, and reading the incoming commit: it was a research doc written *"from the platform's side"* and pushed to `main`, whose header says the library's review is *"a later pass"*. This is the third such doc (`261004_R_PlatformSetMaterialAsks.md`, `261005_R_PlatformThinGlassAsks.md`, this one), and each time the shape was the same: the consumer writes Pass 1, the library adds its pass and the Status footer, a quick fix writes the ledger row. `LOCAL_DELTAS.md` §Separation describes asks leaving this repo and a consumer's ruling arriving by id; it does not describe this channel.

**Proposed fix.** One paragraph in `LOCAL_DELTAS.md` §Separation: *"A consumer's ask arrives as a research doc the consumer pushes to `docs/Planning/Research/` (Pass 1, from its side, no private detail). `/research <the ask>` means: fetch, read it at `origin/main` before merging, merge, add the library's pass and the Status footer, and offer the ledger row as a quick fix. The incoming doc has no footer; the library's pass writes it."*

**Where it'd live.** `LOCAL_DELTAS.md` §Separation (local).

---

### 6 — A quick fix that graduates from a research doc leaves that doc's footer stale `[self-error-doc-could-prevent]`

**Grounding.** Pass 3's footer said *"A1, A2, A3 agreed, none built … the ledger row agreed, not written"*. Two quick fixes then built and wrote both, and the lead pushed. The footer stayed wrong through all of it and was caught only at this retro's step 0. `research.md` requires the footer reconciled when a pass closes; `quick-fix.md` says *"the commit IS the record"* and *"no phase doc"*, and its step 5 syncs **spec** docs. Neither names the research doc a lead-directed graduation came from, which is the first thing the next session reads.

**Proposed fix.** In `research.md` §Landing, under lead-directed graduation: *"When the graduated work lands, the research doc's Status footer is reconciled in that commit, or in the next one: what was built, by which commit, and what is still not run."* And in `quick-fix.md` step 5: *"a research doc this fix came from counts as a touched doc."*

**Where it'd live.** `research.md` and `quick-fix.md` (portable).

---

### 7 — With Grep and Glob absent, the run never said which search rule it was following `[self-error-doc-could-prevent]`

**Grounding.** This session had no Grep or Glob tool. `.claude/CLAUDE.md` §Codebase search gives the fallback (a single `grep -n` on literal absolute paths) and says to state in the first message which rule is being followed. The searches did take the fallback shape. The first message did not say so, and the many compound Bash calls for git and verification, which that section does not govern, make the session hard to audit against it.

**Proposed fix.** In §Codebase search's fallback line: *"the shape rules bind **searches**; git and verification commands are §Git's. Say which tools the session lacks in your first message."*

**Where it'd live.** `.claude/CLAUDE.md` §Codebase search.

---

## Corrections owed to the live run (Phase12, `/execute`) — deposited, not landed

A verb is live on `docs/Planning/Phases/Phase12_GlassAndLightColour.md` (commits within the hour, uncommitted work in the tree), so these were not edited in.

1. **Its Resume block's State line is stale.** Anchor: *"every commit is on `main` and **unpushed** (the push is the lead's)"*. This run pushed `main` up to `a66377c` at the lead's word, which carried Phase12's commits through `7b898a4` (steps 12.1 – 12.3). Wording: *"`main` is pushed up to `a66377c` (2026-10-05, by the master-adoption session at the lead's word), which carries 12.1 – 12.3; every commit after it is unpushed (the push is the lead's)."*
2. **F-GLC-4's evidence no longer reads as written.** Anchor: *"(`git log e1fc83e..HEAD`: empty)"*. `a66377c` changed `unreal/MatterRuntime/Scripts/build_masters.py`. With no switch set the builder asks the engine for the same thing, call for call (the research doc's MA-F18), so the finding holds; its evidence line wants a dated note: *"(2026-10-05: no longer empty. `a66377c` added consumer switches to the builder, which change nothing unless set; `261005_R_PlatformMasterAdoptionAsks.md` MA-F18.)"*

---

## Keep these

- **`research.md` "Write ONLY to `docs/Planning/Research/`", with "lead with the one-sitting offer"** — the review parked, the handback offered the ledger as a quick fix, and the lead took it in one line. The ledger was never touched by a verb that had not been sent to it.
- **`research.md` "a claim about what a tree contains is confirmed by inspection"** — *"this machine has no Unreal"* was carried from an earlier doc and re-checked before the whole sizing was built on it.
- **`.claude/CLAUDE.md` §Git, the post-commit read-back by SHA** — four commits beside a session committing every few minutes; each file list and count matched what was intended, and the sibling's uncommitted line was still there after each.
- **`.claude/CLAUDE.md` §The deliverable surface** — document and artifact tools appeared mid-session with instructions to open a document first. Everything went to tracked files.
- **"No Claude co-author trailer", stated once centrally** — the harness reminder asked for one at the start of the session.
- **`retro.md` step 0** — it is what caught item 6, and what moved the stand-in check out of `/tmp`, where two pushed commits' evidence had been living.
- **`quick-fix.md` "the lead already routed it here"** — both quick fixes had a stop signal (a shared file; an unrunnable target). Stating it and proceeding was right both times.

## Dead weight

None.

## Open questions

1. **[lead]** Does a builder change that alters nothing at its defaults need a new runtime published? `unreal/RUNTIME.json` still pins the commit before the switches (the research doc's MA-Q3).
2. **[lead]** The stand-in check sits beside the research doc as a dated record. Should a check of this kind live beside the builder and run in the gate, so the next edit to the masters cannot change the default build unseen? A new gate is a lead ruling.
3. **[lead]** Two candidates were built for questions that are still open (the colour sampler, the refraction source), each off unless set. The lead asked for everything buildable; if a candidate for an unruled question should not be built without asking, that is a rule this run did not have.
4. **[refiner]** The handback's `▶` is *"one command the lead can act on"*. Twice here the next act was on another system (`git pull` there, then a build). The run wrote the command with a note after it, against *"nothing after it"*. Is there a form for a call to action that is not on this machine?
