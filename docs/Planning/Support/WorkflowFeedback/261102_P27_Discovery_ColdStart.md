# Workflow Feedback — P27 / discovery / cold start

| | |
|---|---|
| **Verb** | `discovery` |
| **Unit** | `P27` (AI Body Skin) |
| **Mode** | `cold start` (Pass 1, then Pass 2 in the same session after the lead mounted the model drive) |
| **Outcome** | `done` — BRIEF READY at `be80f8d`; `/execute Phase27` started as `ML_P27_E1` on the lead's yes |
| **Shape** | `doc-only` (plus throwaway probe scripts kept beside the phase doc) |
| **Confidence** | Ran fully: seed reading, Pass 1 product-docs review, premise probes (mesh islands/seams, Krea generations, projection), Brief, handback. **Not exercised:** the look view (nothing fitted to show), any cross-session message. |
| **Date** | `2026-11-02` |

---

## Items, ranked

### 1 — Pictures shown for a fork must be ONE file, named in the question, labelled by stage `[self-error-doc-could-prevent]`

**Grounding.** At the end of Pass 2 the run opened two pictures at once with `xdg-open`: Krea's raw four-view generation (`f4_s50_seed7.png`) and a five-column sheet of the backs on hm08 (`view_torso_b.png`), and asked *"Is four views painted in one picture acceptable?"*. The lead judged the sheet first (*"Nope... I see 5 of them.... 1 and MAYBE 3 are aligned"*), then the other picture (*"that one looks really good"*), then twice had to establish which picture was which: *"You keep opening images and assume I'm just sitting here ready for whatever random question you ask"* and *"now I give feedback and neither of us know what I'm giving feedback to... where did that skinmap come from.... did you align it?"*. The two pictures were different STAGES (the model's raw picture vs the result on the mesh), and nothing in the question said so. The project memory already said "one labelled picture at a time"; `discovery.md` and `LOCAL_DELTAS.md` say nothing about showing probe pictures during discovery (the rule lives in `execute.md` §TRY and memory).

**Proposed fix.** In `discovery.md` §Forking (where a fork is "shown as pictures, not asked in the abstract"): *"Open ONE picture per question, with the handback that asks it. The question names the file, says what STAGE it is (the model's raw picture · the result on the mesh · a reference), and names each column of a sheet. Two stages are two stops."*

**Where it'd live.** `discovery.md` §Forking to the lead (portable) — or `AI_WorkingAgreement.md` beside the five beats if it is meant for every verb.

---

### 2 — A GPU-busy check chained with `;` prints the busy process and runs the job anyway `[self-error-doc-could-prevent]`

**Grounding.** The four-view generation was launched as `ps -ef | grep "[U]nrealEditor" | head -1; …; <Krea run>`. A platform session had started Studio (`UnrealEditor -game`) at 16:46; the check printed it and the chain went on, so two Krea pictures (~30 s) ran beside it. `LOCAL_DELTAS.md` §Two machines says to check before a launch but gives the check only as a command to read, not one that gates.

**Proposed fix.** Give the check in a gating shape: `! ps -ef | grep -q "[U]nrealEditor" && <job>` (or `ps … | grep -q … && { echo "GPU busy"; exit 1; }`), and say *"a check that only prints does not stop a chain."*

**Where it'd live.** `LOCAL_DELTAS.md` §Two machines (local), or a `docs/Learnings/ClaudeCode/` entry if it recurs.

---

### 3 — `/retro` step 0's launch line says nothing about the working directory; the run reached for `cd` `[self-error-doc-could-prevent]`

**Grounding.** Launching the next session the run wrote `cd <repo> 2>/dev/null; claude --bg --name ML_P27_E1 "/execute Phase27"`. The session's cwd was already the repo root, so the `cd` did nothing, but it breaks `.claude/CLAUDE.md`'s *"No `cd` in ANY command"*. The step's command line gives no cwd, which invites making sure.

**Proposed fix.** In `retro.md` step 0: *"Run it as is: the session's working directory is the repo root, which is where the new session should start. No `cd`."*

**Where it'd live.** `retro.md` step 0 (portable).

---

### 4 — Probe output named per VIEW, not per run, made the doc's picture references go stale within the pass `[self-error-doc-could-prevent]`

**Grounding.** `body.py view` writes `view_<view>.png`; each later run overwrote the earlier sheets, so findings citing "`view_q.png`, the last column of the first run" pointed at pictures that no longer existed. Caught before the commit and fixed by re-rendering one sheet holding every column.

**Proposed fix.** None for the method beyond `discovery.md`'s existing *"the finding records its exact invocation"*: the reproduce line must re-create the cited picture as it is cited. A one-line addition there would do: *"…and the picture it cites, under a name no later run overwrites."*

**Where it'd live.** `discovery.md` (the premise-probe bullet), low priority.

---

## Keep these

- **Pass 1 top-down from the product docs** — `SkinMaps.md` §What the map must show gave RD-SKM-4 (genitals and groin plain skin), which the seed missed even though it approved unclothed generation.
- **Risk lane: "whatever fingerprints a file is a control"** — the grep found that `make_thumbnails.py` builds every thumbnail from the default character scene, so the unclothed cast became a separate option (RD-P27-4) rather than a change that stales every thumbnail.
- **"A pass/fail branch resting on a measurement that takes minutes is measured here"** — about 15 Krea pictures over three routes ruled out the flat-layout route and the two-view route before the Brief, with numbers (20 % of the body grazing vs 6.5 %), instead of an `OPEN` question.
- **Measure on the mesh** (Phase25's lesson) — the seams came from the mesh's own UV edges in one script, exact, and made the Annotated Skin download unnecessary (RD-P27-1).
- **Blockers only when blocked** — the unmounted drive was the one real blocker; the lead answered *"mounted"* and the pass continued.

## Dead weight

None.

## Open questions

1. **Lead decision, recorded as "unless the lead says otherwise":** 27.1 runs beside Phase25's 25.2 (no shared file), although the seed said this phase's execute waits for 25.2. `ML_P27_E1` started on that reading.
