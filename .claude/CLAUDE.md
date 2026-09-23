# Matter Library — always-loaded project rules

See `../AGENTS.md` — canonical agent entry point. The Matter Library is **a community, single-source MaterialX material library and toolset, published as versioned releases for Blender, Unreal-based apps and USD tools to consume**, run with the Agentic-Engineering methodology (see `.ai/AI_Orientation.md` + `.ai/commands/LOCAL_DELTAS.md`).

## Standalone reminders (the carried commands assume nothing about your stack)

- **One repo, no submodules of its own.** Any command step about "bump the submodule SHA / cascade" is a no-op here — every commit is a single `git commit`. This repo is a **producer** consumed through its published releases; the IMRSV platform still registering it as a submodule is the platform's business, never a step here (`.ai/commands/LOCAL_DELTAS.md` §Separation).
- **Path resolution:** `docs/Planning/…` resolves literally. Durable product specs → `docs/specs/`.
- **Stack:** MaterialX 1.39 (OpenPBR `open_pbr_surface`) content · Python tooling under `tools/` · a Blender 5.1+ add-on under `blender/` · OpenUSD for validation. `docs/CodingStandards.md` is still a stub — it arrives when a phase first rules on how code is written here.
- **Bias to the smallest unit** — most work is a `/quick-fix` or a `/research`, not a full phase.
- **The repo is PUBLIC.** Anything committed and pushed is published. Never carry private platform detail (private issue numbers, internal paths, people's names, private-code citations) into a tracked file.

## Don't Delete Spec Functionality — HARD RULE (this project)

**The Matter Library is still being built: design intentionally runs ahead of disk. ADD or REFINE; never DELETE a previously-specified capability just because it isn't built yet.** When aligning docs, mark it `(planned)`, `Todo`, `Drift` or `Reevaluate` **with a date** instead — preserve intent, annotate reality. This is stricter than the method's §Don't Delete Intent carve-out; see `.ai/AI_WorkingAgreement.md` §Project practices.

## The deliverable surface — HARD RULE

**⛔ EVERY DELIVERABLE OF EVERY VERB IS A TRACKED FILE IN THIS REPO. Do not present work on an external surface.** The phase doc **is** the presentation surface — for a plan, a stage, a finding set, a status. Never an artifact, a published page, a hosted document or any other out-of-tree surface, however well it renders.

**If the lead asks for "a URL", they mean a RUNNING SERVICE — ask which.** They are asking to *reach the system*, not to read a prettier copy of your document.

*(A `/plan` run read "you need to provide URLs for me to use on this ipad" as a request for a reading copy, loaded a publish skill, authored a full themed HTML page and published it. The lead rejected it — "Not how this has ever worked... you write this back to the phase doc" — then invoked `/retro` with "you seem to have gotten lost with how plan works". **The cheaper reading was also the correct one, and the same message contained it**: "I could not test with tailscale only or local host". This is written down because the verbs said where a plan **lands** and nothing said where work is **presented**, while the harness offers a publish tool that looks purpose-built for it.)*

## Lanes — HARD RULE

**The methodology is the Workflow Refiner's lane. A working verb does not edit it.** If you are running `/discovery`, `/plan`, `/execute`, `/research` or `/quick-fix`, these are **read-only** to you:

`.ai/commands/**` (including `LOCAL_DELTAS.md`) · `Methodology/**` · `.ai/AI_Orientation.md` · `.ai/AI_WorkingAgreement.md` · `.claude/CLAUDE.md` · `AGENTS.md`

**Hit friction with a command? Adapt in the moment, keep going, and file it in a `/retro` at handback.** That is the entire channel — `/retro` deposits, `/workflow-refiner` triages and lands. Do not fix the command doc yourself, however obvious the fix looks.

**Why the detour is the point, not bureaucracy:** the refiner's job is deciding whether a fix is **portable** (belongs upstream in `PeteSmalls/agentic-engineering`, so every project gets it) or **genuinely local**. An agent that records its own fix has already skipped that decision — and a portable fix landed locally is exactly how one methodology becomes N divergent ones. *(Observed in a live project: a discovery run recorded a Wave-filename convention in its `LOCAL_DELTAS.md`. The rule was portable — it had to be promoted upstream and the local row deleted.)*

**The one exception is the lead asking directly** — then it is lead-directed work, and say so in your report so the next reader can tell it from drift.

**Stay in your verb.** `/discovery` gathers and structures the phase in front of it. A stale sentence three docs away is a `/retro` item, not your errand.

## Git — HARD RULE

**One repo, one branch, one set of docs.** Work in place on `main`. **Never** create a git worktree for agent work — it drops shadow copies of every doc inside the repo (which then poison every grep) and silently orphans commits. Set `"worktree": {"bgIsolation": "none"}` in `.claude/settings.json`; a process rule cannot change harness behaviour.

**⛔ Stage EXPLICIT PATHS. Never `git add -A`, never `git commit -a`, never a bare `git commit`.** The worktree ban is deliberate, which means **this tree is shared by concurrent sessions by design** — a wildcard stage commits someone else's half-finished work under your message. Run `git status -s` before you stage *and* again before you commit: any file you did not touch is another session, live, right now. **⛔ AND READ BACK WHAT YOU ACTUALLY COMMITTED — `git show --stat` — reconciling the file list AND the insertion count against the edit you intended.** Both `status` checks are **pre**-checks, and in a `git commit <paths>` the stage and the commit are **one statement**: there is no gap to re-check in, so a concurrent write to a path you named lands *inside* your commit. **The post-commit diff is the only check that can see this.** *(A one-line `sed` on a `Status:` line committed as **8 insertions / 4 deletions** — a parallel session had written the same file between the clean `git status` and the commit, and its edit rode the rollback baseline. Caught only because the count looked wrong and `git show` was run on a hunch.)* **And never `reset` past a commit you did not make** — resetting to amend an earlier commit orphans everything landed on top of it, and the orphan is on no branch.

**⛔ THE INDEX IS SHARED TOO** — a sibling's `git add` is in your index before you stage anything. **`git diff --cached --stat` immediately before every commit;** a path you did not touch → `git restore --staged <path>`, commit, then `git add` it back so the sibling's index is as they left it. The read-back above still binds: a sibling can stage into the one-call window after this check.

**⛔ SHARING A FILE WITH A SIBLING'S EDITS — the filtered stage, and the ONE sanctioned bare commit:** stage only your hunks (`git diff --output=<scratch>` → hand-remove the foreign hunk → `git apply --cached --check` → `git apply --cached`), then **commit from the index — `git commit -F <msgfile>` with NO pathspec** (a pathspec commits the working-tree version and silently discards the filter), **in the very next call** (a parked filtered stage lets a sibling commit your hunks under their message). **If the hunks are not separable** — equal `-`/`+` counts whose lines do not correspond, because both edited one section — do not filter: rebuild your change against `git show HEAD:<path>` and apply that.

**⛔ A GIT COMMAND THAT LOOKS LIKE A MEASUREMENT IS OFTEN ANSWERING A DIFFERENT QUESTION:**

| The command | What it actually answers | The right check |
|---|---|---|
| `git log -N` showing none of your commits | a window a busy sibling overflowed | `git merge-base --is-ancestor <your-sha> main` |
| `ahead N` dropping sharply | the remote — a sibling pushed | `merge-base --is-ancestor` |
| `git status` ` M` on a file | stale stat cache, possibly no content change | `git diff --stat <path>` |
| `HEAD` | the tree's tip, not your commit | capture your SHA **once, by value** |
| `origin/main..HEAD` | what is unpushed — it **excludes** what CI has seen | `git merge-base --is-ancestor <your-sha> origin/main` |
| `git show`, `git diff`, `git log -1` with no revision | `HEAD` — possibly a sibling's commit | always name your SHA |
| `git log --reverse -N` | the **newest** N, reversed | `git log --max-parents=0` for the first commit |
| `git commit --amend` | composes **from the index**; on a moved `HEAD` it makes a new commit on top | `git diff --cached --stat` **and** `git rev-parse HEAD` first |
| a SHA you read seconds ago | may have been rewritten by a sibling's amend | `git cat-file -e <sha>` before citing it |
| `git rebase` to converge a diverged trunk | may refuse; `--autostash` would stash a sibling's work | `git reset --mixed origin/main`, then re-stage your paths |

**⛔ A MULTI-LINE COMMIT MESSAGE GOES IN A FILE, PASSED WITH `-F`** — inside `-m "…"` a backtick is command substitution: the word silently vanishes and `git` reports success.

**⛔ No Claude co-author trailer — ever. Attribute to the lead only.** It is stated here, once, because it **overrides the harness default**, which appends one unless told otherwise. Stating it only inside individual verbs means an agent must already be running a verb to learn it — and an agent that instead matches what it sees in `git log` gets it wrong for a whole session. The repeats in `quick-fix.md`, `retro.md`, `execute.md` and `workflow-refiner.md` are references to this line, not independent rules.

## Editing — HARD RULE

**⛔ Never address an edit by line number — ANCHOR ON UNIQUE TEXT. A `sed -i` that hits the wrong line, and one that hits NOTHING, are both silent.** Two failure modes, one rule:

- **Stale numbers overwrite the wrong line.** Line numbers from an earlier `grep -n` are **stale the moment any edit lands**, and `sed -i` reports nothing when it overwrites the wrong line — it will silently destroy whatever now occupies it.
- **⛔ A substitution that matches nothing exits `0` and prints nothing — the no-op is indistinguishable from success.** This bites even with numbers you read *seconds ago*: an off-by-one from miscounting a blank line in a `sed -n` range silently changes nothing at all. **Success is not evidence the edit happened.**

Same class as a backtick inside `git commit -m`: **the tool reports success and the work silently did not happen.** Anchor on unique surrounding text, and **read the region back after any edit whose match you have not verified.**

**⚠ AND WHERE AN EDIT TOOL IS AVAILABLE, PREFER ONE ANCHORED `Edit` OVER A `sed` SHAPE** — atomic, anchored on unique text rather than a line range, and immune to both traps above. The `sed` forms in these docs exist because the shape rules were written when Bash was the only writer; keep them for the case where it is. *(A run had a sanctioned four-step `sed` sequence's first step — an unbounded `,$d` delete — refused outright by the auto-mode classifier as a single statement, and did the whole operation in one `Edit`.)*

**A pervasive but MECHANICAL edit — a rename, a renumber, stripping a marker — is a scripted substitution, not a rewrite.** Regenerating a whole file costs output proportional to **file size, not change size**, and silently risks dropping content a diff would have preserved. The two rules pull together: script the substitution, but anchor it on text, never on line numbers.

## Codebase search — HARD RULE (overrides default behavior)

Use the main session's **Grep / Glob / Read** tools directly — they never prompt.

**⛔ One way `grep` LIES: a NUL byte (`0x00`) anywhere in a file makes it treat the file as binary and skip it silently** — a search for a symbol that is demonstrably present returns nothing. **If `grep` and `git diff` disagree about whether a string is in a file, suspect a control character before you suspect the tree** (`grep -c '' <file>` or `cat -v` confirms it). This is the same silent-success class as §Editing's traps, and it cost one run a turn spent hunting for what had "reverted" its edits. **The design rule that makes it moot: a filter or sentinel that must match nothing should be STRUCTURAL, not a magic literal** — a condition that is false by construction cannot be corrupted by an invisible character. Record the stack-specific form in your durable learnings home. For big sweeps, fan out **in parallel** with **Bash-less** search agents; prompt them **"use ONLY the Read/Grep/Glob/LS tools."**

**NEVER use a search agent that carries the Bash tool.** It shells out (`find`/`wc`/`grep`/`cd`), those forms are un-analyzable, and a subagent's prompts surface on every call.

**Fallback when Grep/Glob are absent:** a **single statically-analyzable `grep -n` on literal absolute paths** — one statement, no `cd`, no pipes, no redirects, not a blind recursive `-r`. Quote any `--include` glob. Banned shapes: `find -exec`, piped greps, `cd && grep`, `grep … 2>/dev/null`.

**⛔ When the session's operating mode directs Bash-first file access, this rule does not silently lose.** Split it: the **tool-preference half** (prefer Grep/Glob/Read) yields to the mode — that half exists to avoid permission prompts, which a bypassing mode has already removed. The **other two halves bind regardless**: the *command-shape* rules above, and the absolute ban on **giving a search subagent the Bash tool**. Say in your first message which you are following, so the next reader can tell a considered choice from a violation.
