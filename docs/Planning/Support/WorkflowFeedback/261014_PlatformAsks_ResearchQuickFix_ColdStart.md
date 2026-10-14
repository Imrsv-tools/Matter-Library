# Workflow Feedback — PlatformAsks / research → quick-fix / cold start

| | |
|---|---|
| **Verb** | `research` → lead-directed `quick-fix` ×3, plus two Roadmap seeds (one session; the graduation was named, `research.md` §Landing) |
| **Unit** | `PlatformAsks`: the platform's asks tied to its issue-sweep phase, `261013_R_PlatformSkyAsks.md` and `261013_R_PlatformTrackedItemsAsks.md`, which spun out `261014_R_ScaleProbes.md` |
| **Mode** | cold start |
| **Outcome** | done. **The library's pass on two ask docs.** **Lead rulings:** RD-SKY-1–4, RD-TI-1–3, RD-SP-1–4. **Two seeds:** `PhaseTBD_HdrisInTheLibrary.md`, `PhaseTBD_ScaleGrids.md`. **Three quick fixes:** the ledger, the parity config marked Reevaluate, and a 1 m cube in the conformance golden. |
| **Shape** | behavior-touching (one contract golden), otherwise doc-only |
| **Confidence** | Ran fully: `research`, `quick-fix` (with gates baselined before and run after), Roadmap seeding. **Not exercised:** `/discovery`, and pushing. |
| **Date** | 2026-10-14 |

---

## Items, ranked

### 1 — A word the agent COINS is not checked against the Glossary; only a word it adopts is `[self-error-doc-could-prevent]`

**Grounding.** I named the lead's scale-reference idea *scale probes*. The word went into a new research doc, two commits, and three lead-facing handbacks. The lead then asked *"Is that what you are calling probes?"*, and only then did I grep the Glossary and find **Probe** = *"a local, disposable feasibility test"* (`docs/Glossary.md`, the method vocabulary). The fix cost a rename commit (34 hits) and a ruling note. The research doc's filename still says `ScaleProbes`, because dated research filenames are not renamed. `research.md`'s orient step says *"use the established term or fix it there first"*. I applied it to *HDRI*, a word I adopted, and not to *probe*, a word I invented. The rule reads as being about **existing concepts**, so a newly minted noun slipped past it.

**Proposed fix.** In `research.md` §Self-sufficient orient, item 2, add: *"**And any noun you mint for a new concept: grep the Glossary for it before it reaches a doc, a commit or the lead.** A coined word that collides with a headword, especially a method word (probe, candidate, stage), gives one word two meanings, and the lead will adopt your word in the next message."*

**Where it'd live.** `research.md` §Self-sufficient orient (portable: the method vocabulary ships with every project).

---

### 2 — A quick-fix offer was priced without reading the file's other readers; it ballooned mid-flight `[self-error-doc-could-prevent]`

**Grounding.** In the tracked-items pass, TI-F6 offered *"a one-metre cube in the conformance golden … a `/quick-fix`"*. I named the two gates that read the golden, but not the **builder** that copies it: `tools/conformance/build_portable.py` hard-codes the golden's one article (`MATERIAL_STEM = "Copper_…"`). When the lead said *"do the quick fixes"*, my first design was to dress the cube in the UV-grid diagnostic. That would have failed the portable form's self-contained check, and fixing it meant changing a conformance tool. The balloon valve in `quick-fix.md` caught it. I narrowed the change to a third Copper instance, and the limit is now a scope item of the Scale Grids seed. The offer turned out cheap, but by luck.

**Proposed fix.** In `research.md` §Landing, on the *"lead the landing with the one-sitting offer"* rule, add: *"**Price it by its readers, not its file:** before calling a change a quick fix, grep for everything that reads the file you would change (builders, gates, tests) and name them in the offer. A hard-coded assumption in a reader is what turns a one-file edit into a tool change."*

**Where it'd live.** `research.md` §Landing.

---

### 3 — A consumer's drafted ledger row carries an id that goes stale before the library writes it `[doc-gap]`

**Grounding.** The platform's HDRI ask doc drafts *"**M9** · Skies as a kind of library entry"*. The same day, before the library's pass, the library's own website research took **M9** in `PlatformDependencies.md`. I caught it only by listing the ledger's ids (SKY-F15), and wrote the row as M10. A consumer drafts in its own session and cannot see the producer's ledger moving under it. `LOCAL_DELTAS.md` §Separation describes the ask arriving with a suggested ledger row but says nothing about its id.

**Proposed fix.** In `LOCAL_DELTAS.md` §Separation, on the sentence about the consumer's ask and offering the ledger row as a quick fix, add: *"**A consumer's draft row carries no id, or one marked provisional:** the library assigns the next free `M` id when it writes the row, after listing the ledger."* This is genuinely local: the ledger is this project's.

**Where it'd live.** `LOCAL_DELTAS.md` §Separation (local; the Refiner may judge the producer/consumer ask shape portable).

---

### 4 — `git commit -- <new file>` refuses an untracked path, and a `;` chain then read back a sibling's commit `[self-error-doc-could-prevent]`

**Grounding.** My first commit named a new file, `261014_R_ScaleProbes.md`, in a `git commit -F msg -- <paths>` pathspec without `git add` first. Git refused with *"pathspec … did not match any file(s) known to git"* and committed nothing. Because the commands were chained with `;`, the next one, `git show --stat HEAD`, still ran. It printed a **sibling's** fresh commit (`ad838eb`, material-pipeline research), which could have read as mine. I caught it because the subject was wrong. `.claude/CLAUDE.md` §Git already warns that a bare `git show` answers *HEAD, possibly a sibling's commit*. It does not say that its sanctioned form, `git commit <paths>`, refuses a new file.

**Proposed fix.** In `.claude/CLAUDE.md` §Git, beside *"Stage EXPLICIT PATHS"*, add: *"**A new file must be `git add <path>` first** — `git commit -- <path>` refuses an untracked path and commits nothing. Chain the commit and its read-back with `&&`, never `;`, so a refused commit cannot be followed by a read-back of someone else's `HEAD`."*

**Where it'd live.** `.claude/CLAUDE.md` §Git (portable: the git table ships upstream).

---

### 5 — `/research <vague ask>`: nothing says how to find the asks still lacking the library's pass `[doc-gap]`

**Grounding.** The ask was *"The platform has some asks / questions … can you look into this"*, and the lead added *"It is related to its phase 96"* mid-run. The tree held three recent platform ask docs, one already ruled (the website). The only signal for which ones were still owed was each doc's Status footer: *"The library's review is owed"* / *"The library's review of it … is a later pass"*. I found them by reading all three in full. The lead's phase number named a **platform** phase. Resolving it meant reading the private platform docs, which `LOCAL_DELTAS.md` §Separation sanctions read-only, and writing the result back with no platform id. That worked, but it took about ten tool calls to triangulate.

**Proposed fix.** In `LOCAL_DELTAS.md` §Separation, after *"`/research <the ask>` then means…"*, add: *"**With no doc named, find the owed asks:** grep `docs/Planning/Research/` for footers saying the library's pass is owed, and list them for the lead with their dates. A platform phase number given by the lead is resolved read-only in the platform's docs and written back by subject, never by number."*

**Where it'd live.** `LOCAL_DELTAS.md` §Separation (local).

---

## Keep these

- **`LOCAL_DELTAS.md` §Separation's ask routine** (read the ask, add the library's pass and the footer, offer the ledger row as a quick fix). It gave the whole run its shape. Both docs' Status footers and the ledger stayed consistent across about ten commits.
- **"Several findings taken at once: baseline every gate you will disturb before the first edit, one commit per finding, then one record commit"** (`research.md` §Landing). The baseline is how I could say the cube changed the printed shader count from 110 to 165, and show that the spec's *"96"* was already stale *before* my edit, not caused by it.
- **The read-back after every commit** (`.claude/CLAUDE.md` §Git). It caught the refused commit (item 4) and confirmed each commit's insertion count while two sibling sessions committed and pushed around me.
- **`merge-base --is-ancestor` instead of `ahead N`.** *ahead 2* after eight commits looked alarming. The check showed a sibling had pushed six of mine, and named the two that were not pushed.
- **`quick-fix.md`'s "the lead already routed it" clause, with the balloon valve kept armed.** I proceeded on the lead's word and still narrowed the cube's design when the builder's limit showed up (item 2).
- **"A partial read is not a glance".** I read Phase 96's Status footer and the relevant sections before characterising it. That is how I saw it asks the library for nothing directly (*"Matter Library | its own repo | — | none"*) instead of inventing an ask.

## Dead weight

None.

## Open questions

1. **Item 3 (ledger ids): portable or local?** The ask-doc handshake between a producer and its consumers may be upstream material. The Refiner's call.
2. **For the lead, not the Refiner:** four of this run's commits (`e45e811`, `eede5f3`, `1d55ce2`, `c8a1991`) were unpushed when the retro was filed. Pushing is lead-gated; it was offered and not answered.
