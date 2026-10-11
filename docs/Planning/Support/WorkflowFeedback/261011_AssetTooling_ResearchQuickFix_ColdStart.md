# Workflow Feedback — AssetTooling / research → quick-fix / cold start

| | |
|---|---|
| **Verb** | `research → quick-fix` (one session: a `/research` pass, then a lead-directed graduation into six quick fixes, then a push and a runtime publish on the lead's word) |
| **Unit** | `AssetTooling` (`docs/Planning/Research/261011_R_AssetToolingAsks.md`, Passes 2 and 3; ledger row M8) |
| **Mode** | cold start |
| **Outcome** | done — the review written, all five asks built, the Emissive master repaired, `unreal-runtime-v4` published and pinned. Two things left to other hands: the tracked Blender asset file, and one open ruling (sheets on a one-sided master). |
| **Shape** | behavior-touching |
| **Confidence** | Ran fully: `research`, `quick-fix` (six, each its own commit), a push, `unreal/publish.sh`. **Not exercised:** `discovery`, `plan`, `execute`, `issue-create`. Item 3 touches every verb's handback and is grounded in this run's only. |
| **Date** | 2026-10-11 |

Step 0 was not cut short. Everything the run produced is in the research doc, the ledger or a commit; the two notes that lived only in chat are under §Open questions (3 and 4).

---

## Items, ranked

### 1 — A master change that alters pictures was pushed from a machine that cannot build the runtime, and nothing recorded that a new runtime was owed `[doc-gap]`

**Grounding.** On 10 October the other machine changed `unreal/MatterRuntime/Scripts/build_masters.py` so a coat darkens the base. That alters 27 articles at their own values. That machine runs the editor and cannot build the Linux package, so `unreal/RUNTIME.json` stayed on `unreal-runtime-v3`. The commit says nothing about a runtime, no ledger line was added, and no gate looks. From then on the two machines' Unreal columns differed on 27 articles in silence, and a second project calling the pinned build drew the old pictures. It was found a day later only because that project asked *"do not move what I call without a word"* and this run diffed the pin's `source` against `HEAD` (the research doc's AT-F19; pictured in AT-F26: Porcelain 6.7 against Storm on v3, 1.3 on a fresh build). The lead's ruling of 5 October covers the opposite case only (*"a builder change that alters nothing at its defaults needs no new runtime published"*).

`LOCAL_DELTAS.md`'s *"a publishing producer, if there is one"* row describes the library's release lifecycle and nothing else. The runtime is a second publishing producer with its own trigger (`unreal/publish.sh N`), its own lock (`unreal/RUNTIME.json`) and its own rule about who acts, and it is not in the table. This run treated the publish as lead-only by reading the script's header, then ran it when the lead said *"push and publish runtime v4"*.

**Proposed fix.** Two parts.
- In `LOCAL_DELTAS.md`, a second producer row: *"The Unreal test runtime. Trigger: `unreal/publish.sh N`, run on the machine with Unreal, on the lead's word (it publishes a public asset). Lock: `unreal/RUNTIME.json`. **A commit that changes what the masters draw at their defaults owes a new build. If the committing machine cannot build it, the commit adds a dated 'runtime owed' line to the ledger row it serves**, so the other machine finds it."*
- Optionally a lane in `run_all.py` that warns when `git log <RUNTIME.json source>..HEAD -- unreal/MatterRuntime/Scripts/build_masters.py` is not empty. This run wrote that command into `tools/parity/JOB_FORMAT.md` as something a person runs; a lane would run it for them. That is a tool change, so it is a quick fix for the lead to order, not the refiner's.

**Where it'd live.** `LOCAL_DELTAS.md` (local: the publishing-producer row). The lane: a `/quick-fix`.

---

### 2 — A research finding named a retired file as "the one home" of a change, from a slice of it `[self-error-doc-could-prevent]`

**Grounding.** Pass 2's AT-F14 said ask A1 *"has one home"*: `build_matter_proxy` in `tools/generators/matter_proxy.py`. A grep for `materials.new` had hit that file and `blender/masters/load_article.py`. I read lines 150 – 257 of the first, saw it create a material and read the recipe's master, and wrote the finding. Line 1 of that file is `"""RETIRED 2026-09-27 (Phase05 step 5.5) — kept as a file for history; nothing imports it.` and `docs/ToolingConventions.md` says the same in its `tools/generators/` row, which was on my screen in a grep result. The finding was committed and handed to the lead as a one-sitting offer. It was caught an hour later, at build time, only because the generator's own header happened to be the next file read. Without that, the quick fix would have edited dead code, its check would have passed nothing, and the commit would have said "built".

`research.md` already has the rule for docs: *"A partial read is not a glance — never summarise or rank a doc you have only sliced … map its structure first."* It is written about prior-art docs too large for one read. Nothing extends it to code.

**Proposed fix.** One sentence beside that rule: **"The same holds for code. Before a finding names a file as where a change lands, read that file's first lines and find who imports or runs it. A grep hit says the text is there, not that the code is live."**

**Where it'd live.** `research.md` §Self-sufficient orient or §The research discipline (portable).

---

### 3 — The five-beat handback says "nothing else", and a background session's harness requires a line the rule does not allow `[doc-gap]`

**Grounding.** `AI_WorkingAgreement.md` §Working With the Lead: *"THE HANDBACK IS FIVE LABELLED BEATS, IN THIS ORDER, AND NOTHING ELSE"*, with exactly one carve-out, `/retro`'s terminator. This session ran as a background job, whose harness reads the message text for a `result:` line on its own line, preceded by a sentence saying what was checked; without it the job never shows as complete. Both rules bind every stop. Three handbacks this run put the check sentence and the `result:` line **above** `Completed:` and kept `▶` last. Nothing sanctions that placement, and a later run could as easily put it after `▶`, where the rule says nothing may follow.

**Proposed fix.** A second carve-out, one line: **"Where the harness requires its own status line (a background job's `result:` / `needs input:` / `failed:`), it goes ABOVE `Completed:`, with the one sentence saying what was checked. Nothing is added below `▶`."**

**Where it'd live.** `AI_WorkingAgreement.md` §Working With the Lead (portable: any project run as background jobs meets it).

---

### 4 — A generated, tracked file has no stated owner machine, and nothing notices when it falls behind the tree `[doc-gap]`

**Grounding.** `blender/asset_library/MatterLibrary.blend` is generated by `gen_asset_library.py` and committed. This run changed the loader it is built from (ask A1), so the file had to be regenerated for a Creator to get the change. Nothing says which machine may do that. I held it back here on two inferences: every commit to that file is from the other machine, and on this one Blender's own colour configuration fails to load while the generator bakes each article's preview. That may be exactly right or needlessly cautious; no doc decides it, and the change now sits half-delivered until the other machine runs one command.

The same reading showed the file was already six articles behind the tree (AT-F15): the batch of 9 – 10 October added six recipes and did not regenerate it. `check_asset_library.sh` generates into scratch and checks that copy, so the tracked file is never compared with anything, and no lane of `run_all.py` names it.

**Proposed fix.**
- `docs/ToolingConventions.md`, the `blender/asset_library/` row: say who regenerates the file and when — *"regenerated on <machine> after any change to an article, a recipe or `blender/masters/`; another machine proves its change with `check_asset_library.sh <scratch>` and leaves the command for that one."*
- The `matter-batch` skill's close: regenerate it, or say in the batch summary that it is owed.

**Where it'd live.** `docs/ToolingConventions.md` and the `matter-batch` skill (both local). Which machine is the lead's to say (§Open questions 2).

---

### 5 — "Do it all" after a research landing is a batch of quick fixes, and `quick-fix.md` is written for one `[doc-gap]`

**Grounding.** Pass 2's handback listed six next steps and the lead answered *"yes, lets do it all... prep the work needed. or do it.. wither way"*. `quick-fix.md`'s gate covers *"the lead already routed it here"*, and `research.md` covers a lead-directed graduation, but both are about one change. For six, the run had to choose four things nothing states:
- one baseline of every gate **before the first edit**, not one per fix (`LOCAL_DELTAS.md` asks for a baseline only for the add-on and `tools/conformance/`);
- one commit per fix, so any one reverts alone;
- which fix to start first (the one whose build was longest, so it ran in the background);
- where the record goes: a `Pass` in the research doc with each fix's commit, a `## Resolved` entry holding the lead's words, and the ledger row. *"The commit is the record"* is true of one quick fix and loses the thread across six.

It worked, and the baseline is what let the last handback say *"lane for lane what it was before I started"*. The inbox already holds *"a quick fix that graduates from a research doc leaves that doc's footer stale"* (`261005_…_ColdStart.md` item 6); this is the batch shape of the same seam.

**Proposed fix.** In `research.md` §Landing, under *Lead-directed graduation*: **"When the lead takes several findings at once: baseline every gate you will disturb before the first edit; one commit per finding; then one record commit — a `Pass` naming each commit, the lead's words in `## Resolved`, the footer reconciled. Start the slowest build first."**

**Where it'd live.** `research.md` §Landing (portable), with a pointer from `quick-fix.md`'s gate.

---

### 6 — What this run adds to items still in the inbox

Not re-filed; one new fact each, for the drain.

- **The diverged trunk** (`261005_…_ColdStart.md` item 4). This time the local-only commit was **another session's commit**, not my uncommitted paths. `.claude/CLAUDE.md` §Git offers `git reset --mixed origin/main` for a diverged trunk and, two lines away, *"never `reset` past a commit you did not make"*. Followed together they leave no move. I merged `origin/main`, on the precedent of the merge commits already in history, and said so. A row for *"the commit ahead of the remote is a sibling's"* would have saved the reasoning.
- **A consumer's asks arriving as a research doc** (same file, item 5). Here it arrived **unpushed**, committed into this checkout by a session of another project ten minutes before the lead said *"pull the latest and … look into some feedback"*. The pull was refused as diverged, and the feedback was the divergence. It happened again at the end: two more of that session's commits were on local `main`, unpushed, when `/retro` was invoked.
- **The shared footer** (`261005_…_ColdStart_2.md` item 3). It held this time without a rule: each side reconciled the footer in its own pass, the same day, and marked what it replaced with *"Was:"*.

---

## Keep these

- **`research.md`: "Seeds decay — audit", and a claim about another system checked against that system's own status.** Diffing the Unreal driver across the merge and the pin's `source` against `HEAD` is what found the masters had moved under the pinned runtime (item 1).
- **`research.md` §Landing: lead with the one-sitting offer.** The handback put three one-sitting builds first, and the lead's whole reply was one line.
- **`quick-fix.md`'s infrastructure branch: assert the artifact and the effect, and that the path you did not mean to change is byte-for-byte unaffected.** It is why the new runtime was shown on a coated article **and** on two plain ones whose float captures matched to the byte, and why the published copy was fetched back through the pin before the pin was committed.
- **`.claude/CLAUDE.md` §Git: explicit paths, the index check, and reading back `git show --stat`.** Another session committed into this tree three times during the run. Nothing of its work rode a commit of mine.
- **`LOCAL_DELTAS.md`: baseline before you edit.** The two lanes that are red on this machine for a local reason were named once, up front, and never mistaken for a regression.
- **`AI_WorkingAgreement.md`'s reply-reading rule.** *"Do it all"* was read as covering the reversible ruling on `doubleSided`, taken as my recommendation and flagged everywhere it landed, and as **not** covering the push or the publish, which waited for *"push and publish runtime v4"*.
- **`research.md` §Disposable probes: inline the script.** Every measurement in Passes 2 and 3 can be run again from the doc.
- **`.claude/CLAUDE.md` §Lanes.** The run wrote a rule about runtimes into `tools/parity/JOB_FORMAT.md`, which is a tool's page, and touched no command doc.

## Dead weight

- **`research.md` orient step 2, `Methodology/AgenticEngineering_DocumentationMap.md`.** Not read this run, and not missed: `AI_Orientation.md` and the glossary's pointers were enough to find every owner. One flag, one run.

## Open questions

1. **For the lead: is it right to hold an Unreal launch while another Unreal application is using this machine's graphics card?** Pass 2 held the library's runtime back because Studio was running, and worked the emissive rule out from recorded numbers instead of measuring it. The measurement came an hour later and agreed. Nobody has said whether that caution is wanted.
2. **For the lead: which machine regenerates `blender/asset_library/MatterLibrary.blend`?** (Item 4.) It is owed now: an installed library does not carry ask A1 until it is done, and the file is six articles behind.
3. **An owed content fix, a `/quick-fix` and not the refiner's:** the docstrings of `tools/conformance/assert_profile.py` and `blender/addons/imrsv_lcd_export/lcd_usd_edit.py` still cite the Creator Asset Profile at its old path in the platform's docs. The spec came home on 2026-09-23 and lives at `docs/specs/Contract/CreatorAssetProfile.md`. Seen while editing the first file; left alone as outside the ask.
4. **For the lead: `doubleSided` is free in a conforming asset because I took my own recommendation on a general go-ahead** (the research doc's AT-RD2). It was not ruled on by itself. It reverts as one commit if *"must agree with the master"* is wanted.
5. **For the lead: two commits on local `main` are not pushed and are not mine** — the asset tooling's handed-over check and its Pass 4. The next push carries them, and this file's commit with them.
