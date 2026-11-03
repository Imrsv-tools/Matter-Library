# Workflow Feedback — P27 / execute / resume 5 + close

| | |
|---|---|
| **Verb** | `execute` (resume from 27.2.14, then the close on the lead's "close") |
| **Unit** | `P27` (AI Body Skin) |
| **Mode** | resume run 5 → close |
| **Outcome** | done — 27.2.14–15 sat ("yes 3 is better"), 27.3 and 27.4 built, Tone34 served with the body, phase closed and pushed (`697446e`, then `c6d2a9e`) |
| **Shape** | behavior-touching (`project_body.py`, the maker's `gen_synth_skin.compose` / `gen_skin_maps`, the served Tone34 map and constant) |
| **Confidence** | Ran fully: execute (build → one sitting → strengthen), execute_close rows A⁻–E, retro step 0. **Not exercised:** a mid-run suspend; the issue-close coda (no source issue); the high-rigor lane. |
| **Date** | 2026-11-03 |

Not a continuation of `261102_P27_Execute_Resume4.md`: a distinct run (session `ML_P27_E5`).

---

## Items, ranked

### 1 — A scratch driver pinned to an old SHA rendered the OLD map as "the article", and I read it as what ships `[self-error-doc-could-prevent]`

**Grounding.** The look view cannot draw the tree's skin article on the pinned runtime (F-P27-6), so every Phase25/27 run uses a scratch driver that draws the article **as committed at `3d594fb`**. At 27.4 I served Tone34 and rendered "the served article" with that driver's default column against `D_kl3f`, measured a 5–7 grey-level, R/G +0.03–0.06 difference, and spent three build passes chasing it. Re-serving a corrected map gave **identical numbers to the decimal**. That is the tell: the default column draws the map at `3d594fb` too, not the served one. Rendering the served map × its constant as a `--candidate` gave 0.6–1.5 grey levels. The atlas round trip had been right all along. (The chased cast was real, 1.8 % in the atlas, so the work was not wasted, but the render was evidence about the wrong file.)

**Proposed fix.** Beside the pinned-runtime workaround, one line: *"the `3d594fb` driver's default column is the article AND its maps at that SHA; what ships is shown only as a candidate (the served map decoded × its `base_color_const`)."* This is `execute.md`'s "is it current?" in a form a scratch driver hides.

**Where it'd live.** `LOCAL_DELTAS.md`, the *artifact a person reaches* row (where the look view is named), or a `docs/Learnings/Unreal/` entry while the workaround lasts.

---

### 2 — A Brief fact moved under a live phase without any phase closing: the precondition's trigger missed it `[doc-gap]`

**Grounding.** Phase27's Brief (and 27.2.13's open call) assumed Tone34 is served at 8K. A lead-directed commit from a Studio session, `0e24d0c` (2026-11-02 19:37), moved Tone34 to 4K and changed the ear's grading. No phase closed in between, so `execute.md` precondition 1 (*"a Brief older than a phase that closed after it is stale"*) did not fire. I found it only when the maker crashed: `IndexError … size 16777216` while composing an 8K field at 4K. Cost: one failed run and a re-target of 27.3; logged as a DEVIATION.

**Proposed fix.** Widen precondition 1's trigger: *"…or when any commit since the Brief touches the files its remaining steps name: `git log <brief sha>..HEAD -- <those paths>`."* That command would have listed `0e24d0c` against `gen_synth_skin.py` at kickoff.

**Where it'd live.** `execute.md` §Before you touch anything, item 1.

---

### 3 — An outside field inverted against C, on texels outside the hold region, carries C's per-channel scale `[self-error-doc-could-prevent]`

**Grounding.** 27.3 followed Phase25's `pigments` recipe (target = C's table colour × D / C) for the body. The structure's body came out 1.8 % redder than D (R/G 1.763 vs 1.732). Three passes followed:
- **(a)** The maker's `EPS` in `(table + 0.01) / (base + 0.01)`: real, but small.
- **(b)** Estimating the scale from the head's colour: 12 % off, dropped.
- **(c)** The cause: C and the served head each hold *their own* face core to the subject's level, so D / C carries a scale per channel the structure does not. Phase25 never met it because its whole field *was* the face core.

The fix is a measured correcting pass (`pigments --correct-from <first structure>`), exact by construction because the face constant pins everything else: body 0.22 ΔE, R/G equal.

**Proposed fix.** A learning: *"a field inverted against C anywhere outside the hold region inherits C's calibration scale; measure the structure's result against D on that region and divide it out (one pass)."* The code carries it; the learning is so a third region (Phase28's hands and feet) doesn't rediscover it.

**Where it'd live.** A `docs/Learnings/` entry for the skin maker (no such domain yet; `unsure` which), and `CoreMechanisms.md` row 4 already points at `cmd_pigments`.

---

### 4 — The close's `▶` named `/execute` for a phase that was only SEEDED `[self-error-doc-could-prevent]`

**Grounding.** The close and the follow-up handback both ended `▶ /execute Phase28`. Phase28's Status is `SEEDED`, with no Brief, so `/execute` would stop at precondition 1. Caught only at retro step 0, when the namer was asked for the next session's name. The offer then went out as `/discovery Phase28` (`ML_P28_D1`); the lead said *Not yet*.

**Proposed fix.** In the close handback: *"the `▶` for the next phase is read from its Status line — SEEDED / IN DISCOVERY → `/discovery`, BRIEF READY → `/execute`."*

**Where it'd live.** `execute_close.md` (handback paragraph) or `AI_WorkingAgreement.md` §Working With the Lead, the `▶` bullet.

---

### 5 — A gate lane fails when a git-ignored symlink dangles, and nothing names that signature `[doc-gap]`

**Grounding.**
- **What failed.** Mid-close, `run_all.py` went 18 → 17. `tool_tests` → `test_gen_skin_shine.py` failed with `FileExistsError: … library/parity`.
- **Cause.** `library/parity` is a symlink to the WorkingDrive (F-P27-17), and the drive had been unmounted. The test's `build_character.source()` cache `mkdir(parents=True)` fails on a dangling link.
- **Diagnosis and cost.** Took a read of the log tail and an `ls` of `/run/media`. The `🎉` body had to explain the 17/18, and a second commit recorded the 18/18 once the lead remounted.

**Proposed fix.** In the RUN row: *"`tool_tests` red with `FileExistsError` on `library/parity` = the WorkingDrive is unmounted (the symlink dangles): a box input, not a regression."*

**Where it'd live.** `LOCAL_DELTAS.md`, the *way this project is RUN* row (or `docs/ToolingConventions.md` §Gates, which owns the lanes).

---

### 6 — I put a `cd` in front of the session namer at retro step 0 `[self-error-doc-could-prevent]`

**Grounding.** `retro.md` step 0 gives `python3 ~/.claude/hooks/session_name.py --next "<command>"`. The namer derives the project prefix (`ML_`) from the working directory. I reflexively prefixed `cd <repo>`, which `.claude/CLAUDE.md` bans in every command. The session's cwd was already the repo root, so the `cd` bought nothing.

**Proposed fix.** In step 0: *"run it from the session's own working directory (the repo root), with no `cd`."*

**Where it'd live.** `retro.md` step 0 (upstream: the namer belongs to `agentic-engineering`).

---

## Keep these

- **The regeneration proof before serving (Phase25 25.3.1's precedent).** All 19 body pictures remade pixel-identical, so RD-P27-3 (no picture of an unclothed person committed) held *and* the served map stays reproducible from the repo. It also caught nothing wrong, which is the point.
- **Exact-once anchored edit scripts** (`.claude/CLAUDE.md` §Editing). About a dozen multi-anchor edits across four files this run, every one aborting on a count other than 1. Zero silent no-ops.
- **"Decide, don't ask" (memory) with one picture per stop.** Light-blur, brightness-only levelling, the skin factor, the correction pass and the 4K re-target were all technical calls, made and recorded. The lead saw two things: one sitting (`breast_knees.png`) and one informational answer.
- **The context meter's plain readings every 50k.** They told me when 27.4 had to land in one cohesive push, rather than a self-estimate.
- **Remake-identical proof for a maker change** (`cmp` the served map, the 18 skins in place). It made a change to `compose` safe to land during a phase.

## Dead weight

- `execute_close.md` row D's CI-provisional and CI-observed text: read at the close, and N/A because CI is parked. +1 flag on the existing tally row (*"row D's provisional-stamp and CI-observed text"*).

## Open questions

1. **The uncommitted `.gitignore` line `library/parity`** (no slash, so it matches the symlink). It has sat uncommitted in this tree since 2026-11-02 16:34, across five sessions, each recording it as *"another session's, left alone"*. Whose is it to commit? **Lead question**, not a refiner tweak: until someone commits it, every session's `git status` carries it.
2. **Body fine skin at 4K.** Offered at the close (the close pictures are 0.39 mm a pixel and could carry pore-scale grain at 4K); the lead closed over it. Recorded in Phase27's CLOSE dispositions. If Studio shows the body softer than the face, it is a small `close put` change, no new pictures. Possibly Phase28's to fold in, since its hands and feet will meet the same question.
