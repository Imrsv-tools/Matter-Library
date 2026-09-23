Internal project research — the **intake feeder**, upstream of the commitment line (Workflow §How we work). `/research <topic>` explores a topic across code / docs / behavior and **parks** the findings; it commits to nothing.

Canonical model: `Methodology/AgenticEngineering_Workflow.md` §How we work — Research is intake, not a delivery stage; its handoff to `/discovery` is a parked, **deliberate** gate, never a slide.

## Self-sufficient orient (howdy optional)

Read on invocation (same precedent as `/execute` — running `/howdy` first is fine but not required):

1. `.ai/AI_Orientation.md` (project map, entry points) + `.ai/AI_WorkingAgreement.md` (engineering principles, so the exploration stays inside them).
2. `docs/Glossary.md` (the project vocabulary — **use the established term or fix it there first**, per Working Agreement §Documentation Shapes Architecture; inventing a second name for an existing concept is a bug, not a style choice) + `Methodology/AgenticEngineering_DocumentationMap.md` (≤1-hop navigation — which doc owns what).
3. **Glance** `docs/Planning/Roadmap.md` and the existing `docs/Planning/Research/` folder for prior or adjacent research on the topic — **and `grep -ril <topic>` across `docs/`** — extend an existing doc rather than duplicating it. Prior art for a **named artifact** (a system, a library, a tool) tends to live in its own spec/design folder, not the research inbox.
   - **A partial read is not a glance — never summarise or rank a doc you have only sliced.** If a prior-art doc is too large for one `Read` (doc A is ~30k tokens and `Read` refuses it outright), map its structure first — `grep -n '^#'` — then read its **Status footer and any Decisions / Resolved section** *before* writing anything that characterises it. Skimming doc A's first 40 lines produced a review doc asserting the adversary boundary was the #1 open question, when Pass 15 had recorded the lead's decision settling it; two committed docs needed correction.

## The research discipline

- **Gather, commit to nothing.** Write ONLY to `docs/Planning/Research/` — never durable specs, never code, never a phase doc. If the work starts committing to an approach with route-level file targets, the topic has crossed the **commitment line** — stop and say so; the lead kicks off `/discovery` deliberately, later.
- **Naming:** `docs/Planning/Research/YYMMDD_R_ConceptName.md` — date-prefixed with the creation date so the folder sorts chronologically (phase docs carry their own numeric order; research docs don't, so the date is what gives them one). A disposable-probe **result** doc takes a `_Spike_` marker — `YYMMDD_R_Spike_<Subject>.md` — so probes are distinguishable from investigations at a glance.
- **Shape:** Discovery-Log style **numbered passes** (*what was examined → finding → decision / hypothesis / open question*) + a running **Status footer** (passes captured / current direction / open questions / next step). The command structures the *discipline and the landing*, not the thinking — exploration stays freeform.
- **Closing a pass means RECONCILING the Status footer, not just appending the pass.** `## Resolved` and the open-questions table are *lists*, so a pass revisits them naturally; the footer is *prose*, so it silently keeps asserting what was true three passes ago — and it is the first thing `/howdy` and every resuming session reads, which makes it the worst place in the doc for a stale claim. A pass that answers a question the footer still calls open is not finished until the footer says so.
- **Extend, don't duplicate.** When prior art already answers a question exhaustively, *narrow* it with newly-known facts instead of re-running it. That is usually the highest-value-per-token pass available.
- **Seeds decay — audit, don't assume.** Anything carried from prior docs/sessions is *context, not authority*; spot-verify `file:line` claims against the live tree before building on them. Where a claim can't be verified, record the unverified status explicitly in the landing so unverified never reads as verified.
- **Bash-less search (hard rule):** Grep/Glob/Read directly, or the Bash-less search agents (`codebase-locator` / `codebase-analyzer` / `codebase-pattern-finder`) — **never the `Explore` agent** (see `.claude/CLAUDE.md` §Codebase search).
- **Distinct from `deep-research`:** that is the web/multi-source harness; `/research` is *internal project* investigation. It MAY use `deep-research` or web tools as sub-tools. Two grounding rules when it does:
  - **A claim about what a repo/artifact CONTAINS — source availability, license coverage, file presence — is confirmed only by tree/artifact inspection, never by text sources.** READMEs and listing pages *say* source-available things and will survive adversarial text-verification while being false. Inspect the bytes; prefer a local artifact as the tiebreaker.
  - **`deep-research`'s verified findings are a budgeted SUBSET of what it extracted.** Before trusting an **absence / coverage-gap** conclusion, sweep the raw extraction for load-bearing leads the budget dropped and verify the critical ones yourself.

## Disposable probes

Research may stand up a **local, disposable probe** to test a claim that documentation cannot settle — the standing example is "does this app actually hold the property we need?". A probe is still research: it commits to nothing, selects nothing, and its result doc parks like any other.

- **Disposable means the environment, not the recipe.** Tear down containers, volumes, images, and venvs on completion — but **park the working setup script inside the probe's result doc**. Follow-up probes on the same stack are the norm, not the exception: the Ente environment was destroyed and rebuilt from zero the same day when the next question arrived.
- **The reproduction must survive the box — a path into gitignored scratch is not a reproduction.** `vendor/` (or whatever the project's scratch is) is torn down and untracked, so a `## Reproduction` section citing files that live there claims a reproducibility the doc cannot deliver to anyone else. Either **inline the scripts in the result doc** or **commit them beside it**; never cite a path the next reader cannot open. Scratch keeps clones and build output — never the only copy of the recipe.
- **Verify isolation empirically — a virtual display is not isolation.** `xvfb-run` does not contain a Wayland-aware app: Electron honours `WAYLAND_DISPLAY` and will open a window on the lead's real desktop. Unset it, and isolate **state** separately (`--user-data-dir`). Confirm the isolation held rather than assuming it.
- **Budget a human-in-the-loop for GUI apps.** Modal dialogs no config file can bypass will block an unattended run, and the failure is often **silent** — LiveSync logged "Replicator initialised and activated" while replicating nothing, because a compatibility-review modal had it paused. Plan for a lead interaction instead of assuming headless.
- **Prove the negative.** A probe that claims an encryption boundary holds must inspect the stored bytes (the Ente probe read ciphertext straight out of Postgres). A log line saying it worked is not evidence.

## Landing — park, don't push

- The research doc itself (**always**), and
- *if* something firmed up: an optional **Roadmap seed** — either an unnumbered `PhaseTBD_` `## Future` entry, or (when the lead says "seed Phase `<NN>`") a numbered entry plus a `SEED`-status stub at `docs/Planning/Phases/Future/Phase<NN>_<Name>.md` opening with a **`## Outcome`** (the user-facing north star — see the `Roadmap.md` entry-format rule). The Roadmap entry points at the **stub**, not the research doc. Research authors the pointer-shell; `/discovery` fills it. Both shapes carry the deliberate-gate note.
- **Parking with no seed is the default and the common case** — findings park in `docs/Planning/Research/`, no seed, no apology. Dead-ending is a valid finish.
- **A lead DECISION stays at the altitude it was made — research-tier decisions live in the research docs.** Record it in the deciding doc's Status footer *and* consolidate it into the thread's authority doc (its `## Resolved …` section), so it is findable without re-reading the thread — a decision buried mid-doc costs a full re-read to rediscover, which is exactly how doc A's Pass-15 boundary decision got missed. **Do not push it up or out:** the `Roadmap.md` registers *units of work*, not decisions ("all detail lives in the phase doc, never here"), and `README.md` describes what the project *is*. Detail and decisions **accrete downstream** as the funnel narrows — research → phase doc (§5 hardening) → `/discovery` → `/plan` — each tier capturing the decisions made at its own altitude. Research does not pre-empt any of them.
- **Lead-directed graduation (a named hand-off, NOT a slide).** Research parks by DEFAULT; but **if the lead directs immediate action off a finding, hand to the fitting lane EXPLICITLY and say which one you're entering** — `/quick-fix` for a small self-contained build, `/discovery` for a phase. Naming the lane is exactly what distinguishes a lead-directed graduation from the undisciplined slide the Hard rule forbids (that ban still governs an *un-directed* one).

**Commits:** one `git commit` in this repo — the one-repo default has no submodules and no SHA cascade. Commit explicit paths.

## Resumable — the doc is the state

Long research spans context windows. A fresh session re-invokes `/research <topic>` (or names the doc directly), reads the Status footer, and continues — don't re-run completed passes.

## Hard rule

Explore freely; structure the landing. Never touch durable specs, never *slide* into `/discovery` / `/plan` / `/execute`, never edit repo code. Output = a parked research doc (+ optional Roadmap seed) or a clean dead-end. *(Two sanctioned exceptions: a **disposable probe** — §Disposable probes, which builds nothing in-repo — and a **lead-directed graduation** — §Landing.)*
