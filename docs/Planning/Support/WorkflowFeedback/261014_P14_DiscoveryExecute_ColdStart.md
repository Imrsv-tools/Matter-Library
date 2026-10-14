# Workflow Feedback — P14 / discovery → execute (with the close) / cold start

| | |
|---|---|
| **Verb** | `discovery → execute`, one session: `/discovery P14` (three passes), then `/execute P14` through `execute_close`. |
| **Unit** | `P14` (*HDRIs in the Library*) |
| **Mode** | cold start → close |
| **Outcome** | `done`. Closed (`a16dfbb`) on the library's half of the Outcome: 59 Poly Haven HDRIs, credited, named by file, served by the dev install, judged in USDLiveView and on dev snapshot `matterlib-0.2.0-dev.3`. **The close's push is still owed:** the lead invoked `/retro` without saying push. |
| **Shape** | behavior-touching |
| **Confidence** | Ran fully: discovery (numbering, Pass 1 to 3), execute (three steps, four acts), the close (rows A⁻ to D). **Not exercised:** `/plan`, the high-rigor lane, `execute_repair.md`, row C (no issue source), row E (the push). |
| **Date** | 2026-10-14 |

Step 0: no handoff state or in-chat finding was left off disk. Every ruling, finding and sitting verdict is in the phase doc, M9/M10 or a spec. The one fact deliberately kept off disk is item 3's.

---

## Items, ranked

### 1 — A sitting verdict given in ANOTHER repo's session has no recording rule, and the obvious citation leaks private detail into this public repo `[doc-gap]`

**Grounding.** Act 1 (a library HDRI named bare, shown in USDLiveView) needed USDLiveView's launcher change. The lead ran that `/quick-fix` in the USDLiveView repo, and that session ran act 1 itself, on this phase's own scene pair in `/tmp/claude-p14/sitting/`. It recorded the lead's verdict, *"sky shows, they match"*, **in its own commit message** (in that private repo). Here the lead only said *"USDLiveView says it's working with the apprach"*. `execute.md` §TRY assumes the executor holds the sitting (*"Transcribe the lead's verdict into the phase doc, verbatim and attributed"*) and says nothing about a verdict given elsewhere. I transcribed it from that commit and first wrote that commit's SHA into the public phase doc. The public-repo rule caught that one pre-commit scan before it shipped.

**Proposed fix.** In `execute.md` §TRY, after the transcribe sentence: *"A verdict the lead gave in another session or repo (the consumer's fix session ran the act) discharges the act when you have read it there. Transcribe it verbatim, say where it was given, and, in a public repo, cite that place by content and date, never by a private SHA or issue number."*

**Where it'd live.** `execute.md` §TRY (portable). The public-repo half is already `.claude/CLAUDE.md`'s; this only points at it from the moment it bites.

---

### 2 — "Look at that exact view before you hand it over" has no means here for USDLiveView; the working proxy is a `usdrecord` render of the same file `[doc-gap]`

**Grounding.** Act 3's swap (QwantaniNoon) was opened in USDLiveView for the lead. `execute.md` §TRY: *"look at that exact view before you hand it over."* This session has no way to see the USDLiveView window: no screenshot tool for a Qt app, and the Blender MCP only sees Blender. What worked: render **the same composition file** with `usdrecord --enableDomeLightVisibility` and a search path built the way the launcher builds it, twice (Storm S3). Then check for the resolver warning, look at the frame, and check the launcher's log for its own warnings after launch. Without the flag the first probe showed no sky in any case (now Storm S6).

**Proposed fix.** A `LOCAL_DELTAS.md` line under *the artifact a person reaches*: *"Before handing over a USDLiveView view you cannot see, render the same file with `usdrecord` (Storm learnings S3, S4, S6: twice, dome visible) and read the launcher's stderr after launching it detached."*

**Where it'd live.** `LOCAL_DELTAS.md` (local: the viewer and the toolchain are this project's).

---

### 3 — A measurement discovery must put to the lead (a hosted service's cost) cannot be recorded in this public repo, so it lives only in chat `[doc-gap]`

**Grounding.** The lead widened 14.2 to 1.06 GB of HDRIs in LFS. `discovery.md` (*"put the clause to the lead with what keeping it running costs them"*) sent me to the account side. `gh api /organizations/…/settings/billing/usage` showed metered LFS with real spend. `.claude/CLAUDE.md` (*"never carry … a fact read from a private doc (hardware, cost, schedules)"*) forbids writing those figures into a tracked file. F-P14-13 records only *"metered; figures given in session"*. The numbers are now in the transcript alone, and the next run asking "what does LFS cost us?" re-measures.

**Proposed fix.** Name the home for private measurements a public producer needs: *"a cost or account fact goes to the lead in the handback and, if it must persist, into the platform's private docs, cited here by content only"*. Or rule explicitly that chat-only is the intended state, so the next run doesn't hunt for a home.

**Where it'd live.** `LOCAL_DELTAS.md` §Separation (local: it exists because this repo is public and its consumer's docs are private). `unsure` whether the lead wants a private home at all; that is the open question below.

---

### 4 — The lead adding work to THE PHASE ITSELF mid-execute has no row; what worked was: ruling verbatim, act and step into the Brief, a scope commit before the build `[doc-gap]`

**Grounding.** Mid-execute, the lead asked whether HDRIs would show on the website, then ruled *"add it as 14.3, thumbnails and credit only for now..."*. `execute.md` §Divergence has *"THE LEAD ASKS FOR WORK THAT BELONGS TO NO PHASE"*, but this belonged to this phase. With no row to follow, I:
- recorded RD-P14-4 verbatim, with my reading of *"relayed"* kept apart;
- added act 4, step 14.3 and an In-now row, striking the Not-now row in place;
- committed that scope (`88bc60f`) before writing code.

The lead judged act 4 against exactly that scope.

**Proposed fix.** A §Divergence row: *"The lead adds work to THIS phase → record the ruling verbatim, add its act and step to the Brief (a Not-now row it supersedes is struck, not deleted), and commit the scope before the build: the next sitting is judged against it."*

**Where it'd live.** `execute.md` §Divergence (portable).

---

### 5 — Inserting an item "before the next item's anchor" put act 4 before act 3 and step 14.3 before 14.2 `[self-error-doc-could-prevent]`

**Grounding.** Scoping 14.3, my anchored script inserted act 4 before act 3's row, and 14.3 before 14.2's line. I anchored on the line I wanted to follow, but inserted *before* it. Each anchor matched exactly once, so the exact-count guard passed. A read-back of the order caught it, and a second script moved both.

**Proposed fix.** One clause in `.claude/CLAUDE.md` §Editing, after the exact-once rule: *"an exact-once anchor proves WHERE, not WHICH SIDE. To append an item to a sequence, anchor on the predecessor's LAST line and insert after it, then read the sequence's order back."*

**Where it'd live.** `.claude/CLAUDE.md` §Editing (portable: the anchored-batch rule is upstream's).

---

## Keep these

- **Discovery's *"a number no phase carries IS the lead numbering the next phase"*, with its newer-ruling check:** *"/discovery P14"* resolved to the head of Future in one step, with no round trip.
- **The Risk lane's *"name the control and READ IT"*:** reading `freeze_release.py` and the freshness lane found that a global `schema_version` bump would rewrite the approved pilot's frozen catalog. That produced Q-P14-2 (schema 3 only where HDRIs are listed); both frozen catalogs stayed byte-current through the phase.
- **The First human test's *"can each surface show the thing judged"*, asked at discovery:** the Storm probe found the launcher gap (F-P14-1) and the hidden-dome trap before execute. That is why act 1's scene pair existed when USDLiveView's session wanted one.
- **TRY's *"look before you hand it over"*:** caught the blown-out first thumbnail (a white disc, the sun at 6,200 in linear) before act 2. Comparing with the source's own preview gave the tone curve.
- **`.claude/CLAUDE.md`'s push row (a foreign commit under your tip):** I named three foreign commits, then one more, before each push, with no surprise in the handback.
- **The public-repo rule, reread before each public write:** kept the billing figures, a private SHA and private issue and phase numbers out of the phase doc, M9 and M10.
- **Drain 3's *"a ruling's words kept apart from an agent's reading"*:** used for *"relayed"*; the lead judged act 4 against the reading and accepted it.

## Dead weight

- `execute.md` §Verify-before-edit's web rows (the browser gate's (iv), `allowedDevOrigins`, the edge route) and §BUILD's producer-watcher paragraph: read past at every step. This project has no web surface and no watcher. The *"click, not load"* point does generalise, but its examples are all browser.

## Open questions

1. **Lead decision:** where, if anywhere, a private measurement the library needs (LFS spend, item 3) should persist.
2. **Lead decision (product, not workflow):** every full clone now pulls about 1.1 GB of HDRIs through LFS, counted against the organisation's metered bandwidth. Should contributors be told to exclude `MatterLibrary/hdris/` from LFS fetches (`lfs.fetchexclude`) unless they work on HDRIs? Nothing records this yet.
