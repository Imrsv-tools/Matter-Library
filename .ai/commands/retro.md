Capture structured **workflow feedback** from a finishing (or mid-run) agent, so the Workflow Refiner can sharpen the process docs / commands from **real friction** — instead of the lead hand-asking "any feedback?" each time.

You invoke this on **the agent that just ran (or is partway through) a `/research`, `/discovery`, `/plan`, `/execute`, or `/quick-fix`** — you have the run context, so you self-author one feedback file. It is **deposit-only:** it does NOT edit `Workflow.md` / the command docs (that's the Refiner's separate session, which triages and may decline) — it only drops grounded feedback in the inbox.

> **Note:** one-repo cut — `docs/Planning/`, single-repo commit (no submodule, no SHA cascade). On a solo project "concurrent sessions never collide" matters less, but one-file-per-run is still the shape.

The optional argument is freeform focus (e.g. `/retro focus on the resume friction`); absent that, cover whatever had the most friction this run.

## ⛔ `/retro` IS TERMINAL — the lead is saying "that's it, you are done"

*(Lead-specified, 2026-08-26. Read this before the steps; it changes what the steps are FOR.)*

**`/retro` is not "also write a retro". It is the LAST act of the session.** When the lead types it they are ending the run, so three things follow, in this order and no other:

1. **⛔ DOCUMENT FIRST — the retro is written AFTER the handoff state is on disk, never instead of it.** Everything this run produced that lives only in chat must land in a tracked file before you write a word of feedback: the Execution-Log entry you owe, the Resume block, a status line you left contradictory, **and — the one that actually gets missed — the SUGGESTIONS AND FINDINGS YOU SCATTERED THROUGH THE CONVERSATION.** A recommendation made in chat and never written down did not happen; the next session cannot see it, and the lead should not have to scroll a transcript to recover it. **Route each one to its home** (phase doc · a `DEFER:` line · a tracker issue · this retro's own items) **before depositing.** *(The failure this is written from: runs that "tossed a bunch of suggestions" at the lead and then filed a retro, leaving it genuinely ambiguous whether any of it was recorded anywhere.)*
   ⚠ **IF THE LEAD CUTS STEP 0 SHORT** — *"no more editing, we have moved on, just /retro"* — **do NOT keep routing.** Record the un-routed findings in **this retro's own §Open questions**, and say **at the top of the file** that step 0 was truncated by the lead. **One place, flagged, beats a half-finished sweep**, and the lead ending the run outranks this step. *(It happened on the first day this rule existed: a run was mid-route, moving a `/howdy` assessment's recommendations to a research doc, when the lead stopped it. The deposit is compliant read this way and non-compliant read literally.)*

   ⚠ **AND "HAND THE CORRECTION TO THE LIVE RUN" (step 5) HAS NO CHANNEL — so depositing it HERE is what discharges it.** If a verb is live on the unit and you are holding a correction to its doc, **write the correction into this retro as a concrete item — the file, the anchor, the exact wording** — and say in the handback that it is owed. **You cannot message another session**, and the correction must not be left only in chat. *(Asked by a run that withheld corrections correctly while an execute session committed to the same phase doc every few minutes, then noticed they now lived only in its retro and the transcript.)*

2. **Then deposit the retro** — steps 1–5 below, one file, one commit.
3. **⛔ THEN STOP. NO FURTHER ACTIONS.** Do not start the next thing, do not "while I'm here" a fix, do not open another verb. If something still needs doing, it goes in the retro or in `Next` — not in this session's hands.

**⛔ AND THE LAST LINE OF YOUR FINAL MESSAGE IS THE TERMINATOR, ALONE, VERBATIM:**

```
RETRO SUBMITTED — no other actions expected.
```

**It goes AFTER the five handback beats, after the `▶` line, after any commentary** — and it is the one thing permitted to follow `▶` (`AI_WorkingAgreement.md` §Working With the Lead, whose "five beats and nothing else" rule carves this out by name). **Anything you want to say about what else needs doing is fine — say it BEFORE the terminator.** The line exists so the lead can tell **at a glance, from the bottom of the message, that this agent is complete** and nothing is still in flight. **A message that ends any other way reads as a session still running.**

## Where it goes — ONE file per run (never append to a shared file)

`docs/Planning/Support/WorkflowFeedback/<YYMMDD>_<Unit>_<Verb>_<Mode>.md` — copy `_Template.md`. **One file per run.** `<Unit>` = the phase (`P01`), the Issue #, or a short slug for pre-phase research (`Characters`). Filename examples: `260719_P01_Execute_ColdStart.md`, `260719_Sandbox_Research_ColdStart.md`, `260719_QF-icons_QuickFix_Cold.md`.

**`<Mode>` is what distinguishes two runs on the same unit — use it.** Every worked example above says `ColdStart`, which makes the field read as decorative; it isn't. A resume run of the same verb on the same unit and day is `260824_P01_Discovery_Resume.md`, not a `_3` on someone else's `ColdStart` stem.

**A long run may deposit more than once** — the refiner drains and deletes the first file while the run continues. Use a `_2` / `_3` suffix on the same stem, say in the header which file it continues, and **read `_RefinementBacklog.md` first so you don't re-file items already absorbed.** **`_2`/`_3` also disambiguates two DISTINCT runs that genuinely collide on every field** (same unit, verb, mode and date — common when one verb runs twice on a unit in a day). **The header must say which case it is:** a continuation names the file it continues; a distinct run says plainly that it is *not* a continuation. Otherwise the refiner has to infer it, and the two cases drain differently.

**⛔ RE-INVOKED WITH NO WORK IN BETWEEN? Deposit ONLY WHAT THE EARLIER FILE MISSED.** Re-read that file *and* `_RefinementBacklog.md` before writing a word. **If genuinely nothing is left, say so in one line and deposit nothing** — an empty `_2` costs the refiner a drain and teaches the inbox to lie. **The failure mode is restating the first deposit in fresh wording**: two overlapping files are strictly worse than one, and reconciling them is pure waste. *(The anti-fabrication rule — "'none' is a fine and common answer, don't fabricate" — is stated under **Dead weight** but governs the WHOLE file, this case included. Declining outright is wrong too: the lead asked.)*

**One session spanning two verbs — a sanctioned `discovery` → `plan` arc — is ONE file with a COMPOUND `<Verb>`** (`260824_P05_DiscoveryPlan_ColdStart.md`), because the grounding genuinely spans both and splitting it duplicates context. Say both verbs in the header's **Verb** row. *(Blessed by the refiner after two runs independently chose the compound form over the doc's single-value field and both flagged the mismatch. `discovery.md` §Hand-off explicitly sanctions the arc, so the filename grammar had to admit it.)*

## Do this, in order

0. **Land the handoff state and every in-chat suggestion in a tracked file — §`/retro` IS TERMINAL step 1.** This precedes the header, not follows the deposit.
1. **Fill the header** from your own run context: **Verb** (research/discovery/plan/execute/quick-fix — **or a compound, for one session spanning a sanctioned arc: `discovery → plan`**), **Unit** (phase / Issue # / research slug), **Mode** (cold-start / resume run N / suspend-handoff / close / *quick-fix:* cold / from-issue), **Outcome** (done / derailed / suspended / repaired / promoted / n/a), **Shape** (behavior-touching / doc-only), **Confidence** (ran it fully vs inferential on `<X>` — flag the parts you *didn't* exercise), **Date**.
2. **Write ranked, GROUNDED items — highest-value first.** Each carries: the one-line claim, **flagged `[doc-gap]` or `[self-error-doc-could-prevent]`**, the **Grounding** (what actually happened this run — the repro, not an abstraction), a concrete **Proposed fix**, and **Where it'd live** (`execute.md` / `Workflow` / a learning / memory / `LOCAL_DELTAS.md` for a port gap / unsure). **Ground every item in this run's friction — no generic best-practice advice** (the Refiner declines ungrounded items). In a freshly-adopted project a very common item is a **port gap** — a carried command still assuming the upstream's shape; flag those `[doc-gap]` and point at `LOCAL_DELTAS.md`.
3. **List "Keep these" — and flag "Dead weight."** *Keep these:* what worked and must NOT be "fixed." *Dead weight (optional, default "none"):* rules you ignored, didn't need, or had to re-read because they were buried this run — the inverse signal that tells the Refiner what to *cut*. One line each; **"none" is a fine and common answer — don't fabricate.**
4. **Open questions** — anything you couldn't resolve or are unsure about.
5. **Commit the single file**, **explicit path**, no Claude co-author trailer: `git add docs/Planning/Support/WorkflowFeedback/<file>` then commit. **Don't** touch anything else — the Refiner processes and deletes the file on disposition (no forever archive). **⚠ "Anything else" means THE METHODOLOGY LANE and other people's work** (`.ai/commands/**`, `Methodology/**`, the entry-point docs — `.claude/CLAUDE.md` §Lanes) — **it does NOT forbid correcting your own run's uncommitted state error in a planning doc.** If the retro surfaces a live inconsistency *your run created* — a Roadmap transition you owed and skipped, a status line you left contradictory — **fix it, in its own commit, and say in the retro that you did.** Filing a report about a one-line error you are standing in front of is worse than fixing it. **The line you may not cross is authoring the methodology fix**, which is the Refiner's call precisely because it decides portable-vs-local. **⛔ AND BEFORE CORRECTING A PHASE DOC, CHECK WHETHER A VERB IS LIVE ON THAT UNIT** — `git log` for commits on it in the last hour, or just ask. **If one is, HAND THE CORRECTION TO THAT RUN INSTEAD OF LANDING IT.** The executor owns that doc; your correction will race an anchored edit it is holding, and **a `sed` that loses to a concurrent write reports success.** *(Both rules were followed and they collided anyway: a finishing run corrected its own stale Resume block under this very step, citing it by name — while the session `/execute`-ing that phase was mid-edit on the same header. Two sessions fixed one block in the same ten minutes, and the executor's two anchored edits silently no-opped. Benign only because both edits happened to be the same correction.)*

6. **Hand back, then STOP** — the five beats, then the terminator line as the last line of the message. Nothing after it, and no further tool calls in the session.

## Hard rule

Deposit grounded feedback; do **not** edit the Workflow doc / command files yourself — that's the Refiner's lane. Ground every item in what happened **this run**, rank by value, flag doc-gap vs self-error, and name the keep-these.
