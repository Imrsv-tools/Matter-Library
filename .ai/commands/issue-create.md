# issue-create — file a GitHub issue against the project tracker

The inline "capture an issue while doing other work" verb. You type `/issue-create`
(or say "file an issue for X"); this drafts a well-formed issue and files it on the
platform's GitHub tracker — **but only after you confirm the exact command.**

**⚙ Configured for this project (2026-09-23) — see `LOCAL_DELTAS.md`.** The default tracker
is `Imrsv-tools/Matter-Library` (recorded in `.ai/AI_Orientation.md`). Pre-existing Matter
issues that live in the IMRSV platform's tracker stay there; new Matter-Library work files
here.

Filing the issue creates the Issue lifecycle's **`captured`** state (Workflow §Issue lane);
pickup and the D→P→E flow happen later via `/discovery #<n>`.

## Pre-flight (the lane's standing prerequisite — like `/execute`'s "sandbox OFF")

The whole lane is GitHub-backed, so before drafting: **`gh` installed + authenticated
(`gh auth status`) + the repo has Issues enabled.** A fresh agent on a clean box otherwise
hits `gh: command not found` (exit 127) or an auth error and stalls. Fix is one-time host
setup: `sudo dnf install gh` then `gh auth login` (device flow). Say so plainly rather than
failing opaquely.

## The one hard rule — never auto-fire

`gh issue create` **writes to a public-ish external service**. So the flow is always:

> **gather → draft → SHOW the exact command → wait for explicit confirmation → run.**

**⛔ FILING A BATCH — a close's deferral ledger, a discovery's findings — IS ONE CONFIRMATION, NOT N.** This doc's worked example is a **single** issue, so the batch shape had no guidance and the per-invocation reading is the natural one. **Draft all of them, show TITLES + LABELS AS A TABLE plus the bodies' shape and one script path, and ask ONCE for the set.** Do **not** ask per issue: a close filing five issues would spend five round trips at exactly the point the lead is least interested in ceremony. *(`execute.md` already says the filing is lead-gated and should be confirmed "as a one-liner up front or at the checkpoint" — which is this shape — but it says so in the doc you are NOT reading at the moment you file.)*

Never run `gh issue create` without showing the lead the literal command first and getting
an explicit go-ahead. No "I'll just file it." A casual "sounds good" about the *content*
is not approval to *fire* — confirm the command itself.

**One case IS the confirmation: a lead directive naming already-drafted issues** ("file
them", "file both") **whose titles/labels/content were already shown** — fire, showing the
literal commands in the same firing turn, and report the URLs; re-asking there is the
banned process check-in. The extra round-trip is owed only when the content or labels
were never shown.

## Procedure

1. **Gather.** From the request (and the surrounding work, if this was triggered
   mid-task), establish:
   - a crisp **title** — the human-readable *"what,"* no type/area token (those are labels
     now) — per `ToolingConventions.md` §Issue tracker conventions title grammar. Found in a
     phase → a readable prose prefix (`P37 — AssetManager: second import drops textures`); not
     in a phase → plain title, no prefix. **⛔ Phase not yet NUMBERED?** Phases stay
     `PhaseTBD_<Name>` until the lead numbers them, so `P<NN>` has no value to take — use
     **`PTBD_<Name> — <area>: <what>`** and note the gap in the body. **If the phase is
     numbered later, do NOT retitle issues already filed** — the body's phase-doc pointer is
     the durable link, and retitling buys cosmetic consistency at the price of invalidating
     every citation of that title. *(Five issues were filed as `PTBD_IdentityAndAccess — …`
     and the lead numbered the phase two turns later.)* Imperative + specific ("Add-Prop relative-layer
     warning on reopen", not "bug");
   - a **body**: what's wrong / wanted, where (file·symbol·phase if known), repro or
     context, and — when it came up mid-work — a one-line "surfaced while doing X" note;
   - **labels — auto-suggest, show in the confirm step, fire with `--label`.** The platform
     tracker's label vocabulary is **`docs/ToolingConventions.md`
     §Issue tracker conventions** (the 4 axes `type:`/`area:`/`status:`/`source:` — NOT the
     Stage `…/agent-skills/triage-labels.md`, which is *Stage's* tracker + an uncustomized
     template). Default **`status:defined`** (a Claude-drafted ticket *is* defined) + infer
     **`type:`** (bug/feature/techdebt) and **`area:`** (the touched surface) from the
     request; add `source:deferred` if this came off the old backlog / a mid-run defer. Labels
     must **pre-exist** (`gh` errors on an absent `--label`), so **⛔ CHECK — `gh label list
     --repo Imrsv-tools/Matter-Library` — rather than assuming the taxonomy is seeded.** Where it is,
     don't invent new ones. **Where it ISN'T** (a young tracker carrying only its host's stock
     labels — the common case, and the doc that owns the taxonomy may itself still be an
     unbuilt deliverable): **file with the title grammar, apply the nearest stock label or
     none, and say so in the body.** Do **not** map the 4 axes onto stock labels — that
     invents a tracker-wide vocabulary, which is a lead decision, and it pre-empts whichever
     phase owns seeding it.
2. **Draft & show.** Present the title + body to the lead, then show the **exact** command
   you intend to run, e.g.:

   ```bash
   gh issue create --repo Imrsv-tools/Matter-Library \
     --title "Add-Prop relative-layer warning on composition reopen" \
     --label "type:bug,area:plugin,status:defined" \
     --body "$(cat <<'EOF'
   ## What
   Reopening a composition logs a relative-layer warning when a Prop was added…

   ## Where
   The composition reload path; see the Phase 26 known-issues write-up.

   ## Context
   Surfaced while running the platform chain smoke test.
   EOF
   )"
   ```
   Use a quoted heredoc (`<<'EOF'`) for multi-line bodies so backticks/`$` in the body
   are not expanded. Add `--label "..."` only when a real label applies.
3. **Confirm.** Wait for an explicit "yes, file it" (or edits). If the lead tweaks the
   title/body, re-show the updated command.
4. **Run** the confirmed command. `gh` must be authenticated (`gh auth status`); if not,
   say so rather than failing opaquely.
5. **Report** the issue URL `gh` prints back.

## Optional follow-ups (same confirm-before-fire discipline)

- Triage an existing issue: `gh issue edit <n> --add-label "..."`.
- Keep the full `gh` grammar (view/list/comment/close) wherever this project homes its
  tool reference; reuse it, just retarget `--repo`.

## Notes

- `gh` infers the repo from the clone's remote, but **pass `--repo Imrsv-tools/Matter-Library`
  explicitly** so a nested-checkout cwd or a detached checkout can't misfile the issue.
- This is a *verb* (you invoke it), distinct from a passive reference bundle
  (facts a verb reads).
