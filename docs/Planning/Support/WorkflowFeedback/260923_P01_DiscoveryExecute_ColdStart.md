# Workflow Feedback — P01 / Discovery → Execute (+ close) / Cold start

| | |
|---|---|
| **Verb** | `discovery → execute` (compound, one session), including the lead-directed close. The session opened with an unfiled `/research` (landed as `docs/Planning/Research/260923_R_StandaloneSetup.md`). |
| **Unit** | `P01` (Standalone Bootstrap) |
| **Mode** | cold start → close |
| **Outcome** | `done`. Phase01 closed at `b30efc4` and pushed: the method was adopted into a pre-existing scaffold, 18 specs came home from a private parent repo scrubbed for a public repo, and licences, glossary and roadmap were written. |
| **Shape** | `doc-only` (no tool code changed) |
| **Confidence** | Ran fully: research (by hand, pre-adoption), discovery (Passes 1–3), execute (5 steps, 5 lead clicks), close (rows A⁻–E). **Not exercised:** `/plan`, `execute_highrigor`, `execute_test`, `execute_repair`, the issue coda, CI. Items touching those are inferential. |
| **Date** | 2026-09-23 |

*Step 0: all handoff state is on disk. Two items raised in chat had no home and are in §Open questions (the commit author name; the publication-check scope for planning docs).*

---

## Items, ranked

### 1 — Adopting into a repo whose specs live in a PRIVATE parent has no procedure; the "scrub + two-way publication check" had to be invented in discovery `[doc-gap]`

**Grounding.** Matter-Library is public; its canonical specs were in the private IMRSV platform docs. `ProjectFolders.md` §Setup Checklist item 9 ("absorb, don't duplicate") covers entry points, ADR registries and old plans, but not *durable specs arriving from a private sibling into a public repo*. Discovery had to invent three things:
- the publication-check regex;
- the "demonstrate it both ways" run: 22 hits on the raw platform text, 0 on the scrubbed tree;
- a shared scrub rulebook for three parallel writer agents (links into other trees, private issue numbers, names, local paths, private-code/ABI cites, phase/decision ids → one dated `## History`).

It worked, and the lead approved every click, but nothing in the method pointed at it.

**Proposed fix.** In `ProjectFolders.md` §Setup Checklist item 9, add a fourth arrival kind: *"**Durable specs from a private sibling into a public repo** → bring home, scrub, and prove it with a check run both ways (it must hit the raw source and print 0 on your tree). Condense load-bearing history into a dated section; drop ids. The push is the irreversible act, and it stays lead-gated."*

**Where it'd live.** `Methodology/AgenticEngineering_ProjectFolders.md` (portable, so upstream).

---

### 2 — The one-repo template has no home for a producer's asks of its consumers; `PlatformDependencies.md` and the `LOCAL_DELTAS` §Separation section were written from scratch `[doc-gap]`

**Grounding.** Upstream dropped the multi-repo apparatus ("do not pre-build it"). Matter-Library is one repo, but it is a *producer* with real consumers (IMRSV Stage/plugin/Studio, USDLiveView). The run needed:
- a `LOCAL_DELTAS` §Separation section (no SHA cascade here; integration phases numbered on the consumer's line; the consumer still pinning us is its business);
- `docs/Planning/PlatformDependencies.md` (10 outbound asks + 2 inbound).

The only precedent was PitchBoard's local LOCAL_DELTAS row. `Workflow.md` §Phase Numbering already says integration phases live on the main line; nothing says where the asks go.

**Proposed fix.** Add a one-paragraph *"Standalone with consumers"* note to `ProjectFolders.md` (or `DocumentationMap.md`): asks between a project and its siblings go in `docs/Planning/<Sibling>Dependencies.md` (one row per ask: owner · pairs-with phase · status), never in handback prose. Optionally ship it as a template stub.

**Where it'd live.** `Methodology/` + `templates/docs/Planning/` (portable, so upstream).

---

### 3 — `git add <old-path>` after `git mv` fails with "pathspec did not match", and it happened twice `[self-error-doc-could-prevent]`

**Grounding.**
- Discovery ruling commit: I staged `…/Future/PhaseTBD_StandaloneBootstrap.md` after `git mv` → `fatal: pathspec … did not match`. The `&&` chain meant **no commit happened**, and I only noticed from the output.
- Close: the identical failure with `…/Phases/Phase01_StandaloneBootstrap.md`.

`.claude/CLAUDE.md` §Git says to stage explicit paths and to `git add` a new file, but not that a `git mv`'d source path is already staged and must not be named again.

**Proposed fix.** Add one line to template `CLAUDE.md` §Git: *"After `git mv`, the removal is already staged — name only the NEW path in `git add`; naming the old one fails and, in an `&&` chain, silently skips the commit."*

**Where it'd live.** `templates/.claude/CLAUDE.md` §Git (portable).

---

### 4 — ADOPTING says "record the upstream SHA" but not "fetch upstream first"; the plan was built on a stale local clone `[doc-gap]`

**Grounding.**
- The research and Pass 1 read the local agentic-engineering clone at `a6e7e81`. The lead then found that clone was out of date.
- Pass 2 re-based on `b1f36c2`, and Pass 3 on `9f52c7f` after a sibling session pushed fixes mid-discovery.
- Two of the three fixes landed upstream **between discovery passes**, so the Brief's defect list would have carried already-fixed items.

**Proposed fix.** `ADOPTING.md` §1: *"`git fetch` the upstream and vendor from `origin/main` — never from a local clone's HEAD — and re-check the SHA at execution start; a sibling may be refining upstream the same day."*

**Where it'd live.** `ADOPTING.md` (portable).

---

### 5 — `execute_close` row A0's arming list misses "alone / only / no need for", so the run had to judge whether its Outcome was absolute `[doc-gap]`

**Grounding.** The Phase01 Outcome says *"…from this repository alone … with no need for the private IMRSV platform docs."* A0 arms on "no deferrals · no placeholders · every X · all Y · fully functioning". "Alone" and "no need for" are just as absolute but aren't listed, so I armed it by judgment, which is exactly the self-scoring A0 exists to remove.

**Proposed fix.** Extend the arming question: *"…or any exclusivity claim — **alone · only · without · no need for**."*

**Where it'd live.** `.ai/commands/execute_close.md` row A0 (portable).

---

### 6 — Parallel writer agents author new normative rules while "bringing docs home" unless the rulebook forbids it `[self-error-doc-could-prevent]`

**Grounding.** The Ontology writer added three rules to MasterSet that no one had ruled:
- "`system` is reserved";
- "removing a token is semver-major";
- "adding a token is additive".

It flagged them honestly in its report. The coordinator's consistency pass marked them `Reevaluate — proposed, not yet ruled`. Without that pass they would have shipped as contract.

**Proposed fix.** In `execute.md` §Native capability or `DocumentationMap` (delegated doc work), add: *"A delegated writer brief must say: carry, correct and annotate — never author a new normative rule; propose it as a flagged `Reevaluate`."* The `execute_close` row A doc-conform brief already carries a "refine, don't delete" constraint; this is its twin.

**Where it'd live.** `.ai/commands/execute.md` or `Methodology/AgenticEngineering_DocumentationMap.md` (portable).

---

### 7 — Discovery wrote a first-human-test click against a carried verb's output without reading that verb's Output section `[self-error-doc-could-prevent]`

**Grounding.** Click 1 said `/howdy` "answers with what the Matter Library is". Upstream `howdy.md` §Output prints ≤2 lines (branch · clean · last · active) and deliberately does not recite identity. Execute had to refine the test in the ledger.

**Proposed fix.** `discovery.md` §The Brief → *First human test*: *"If a click invokes a carried verb, read that verb's §Output before writing what the click shows."*

**Where it'd live.** `.ai/commands/discovery.md` (portable; minor).

---

### 8 — `LOCAL_DELTAS.md` is "the Refiner's lane" but adoption must write it; the bootstrap had to self-justify twice `[doc-gap]`

**Grounding.** `CLAUDE.md` §Lanes lists `LOCAL_DELTAS.md` as read-only to working verbs, and the bootstrap *was* an `/execute`. It wrote the file at 1.1 and updated a row at 1.5 (the file's own "update a not-yet-existing-artifact row" rule). Each time it had to add a note justifying itself.

**Proposed fix.** `ADOPTING.md` §6 or `CLAUDE.md` §Lanes: *"The adoption bootstrap (the phase that vendors the method) is a sanctioned writer of `LOCAL_DELTAS.md` and the entry docs until it closes; say so in its commits."*

**Where it'd live.** `templates/.claude/CLAUDE.md` §Lanes or `ADOPTING.md` (portable).

---

## Keep these

- **One lead click per step, verdict transcribed verbatim.** Five clicks, five one-line verdicts, zero rework; the lead drove the phase at his own pace.
- **The two-way publication check** (must hit the raw source, must be 0 on ours). It is what made pushing private-derived content to a public repo a checked act rather than a hope.
- **"Archive verbatim with a banner, then write fresh"** for `build_plan.md`, the old `Readme.md` and `FolderStructure.txt`. It honoured this repo's strict don't-delete rule and the Roadmap's "no technical content" rule at once.
- **Dated `Drift` / `Reevaluate` annotations instead of rewriting contract** (24 + 18). They let the specs come home honestly while the lead's rulings conflicted with them.
- **Spot-verifying agent claims before building on them** (e.g. `master_material` has no consumers; the catalog has no master field; the reference `.mtlx` defect; overlays are linear). It caught one stale platform-glossary claim (overlay = sRGB).
- **The `ALREADY ROUTED` disposition and the E-row push gate.** They made the close unambiguous: the lead approved the 9-commit push and then, separately, the close push.
- **The briefing-docs-point-don't-transcribe rule** (new at `b1f36c2`). `AI_Orientation` carries no Roadmap state, so nothing in it went stale during the phase.

## Dead weight

- **`execute.md` §TRY's URL/browser framing** ("hand back a URL", browser headers, `allowedDevOrigins`) did not map to a doc-only phase. The file path worked as the "URL" and nothing broke, but a reader had to translate it every step. One flag; not a cut on its own.

## Open questions

1. **Lead decision: does the publication scrub apply to planning docs too?** The check covered `docs/specs/`, the glossary/conventions and the entry docs. The research doc (`260923_R_StandaloneSetup.md`, pushed) and the phase doc still name private platform repos, doc paths and platform phase ids by design, as provenance. None are secrets, but the repo is public.
2. **Lead decision (raised in chat, unanswered): the commit author name.** This repo's local config makes commits `Pete <peter@imrsv.tools>`, while the 83 pre-standalone commits are `PeteSmalls`. The lead said which email; the name was never decided.
3. **Inferential:** whether item 2's `<Sibling>Dependencies.md` convention belongs upstream or stays local. It is the first multi-repo-adjacent adopter since upstream dropped that apparatus, so the Refiner's portable-vs-local call is genuinely open.
