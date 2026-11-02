# Workflow Feedback — P26 / discovery / cold start

| | |
|---|---|
| **Verb** | `discovery` |
| **Unit** | `P26` (Makeup on the Skin) |
| **Mode** | `cold start` (Pass 1 on a seeded doc) |
| **Outcome** | `done`: BRIEF READY (`b5d22c1`), lane `build`. The lead's thumbnail ruling was recorded at handback as RD-P26-10 (`47c64aa`), and `ML_P26_E1` was started on `/execute Phase26` with the lead's yes. |
| **Shape** | `doc-only` |
| **Confidence** | Ran fully: discovery Pass 1, the two-way cross-session exchange with the platform's live skin-phase session, the Brief. **Not exercised:** any build or premise probe. The `color4` alpha probe was written into 26.1 rather than run here. |
| **Date** | 2026-11-02 |

Step 0 was done in full: the next session was offered and started, and the ruling landed in the phase doc before this file.

---

## Items, ranked

### 1 — Pricing a fingerprint re-make turned, pre-release, into scheduling it, and the lead called that waste `[doc-gap]`

**Grounding.** `discovery.md` §Risk lane says *"Whatever FINGERPRINTS a file the build map changes … is a control too … price what the change re-makes"*. I priced it correctly:
- `showcase.py` `masters_hash` covers `blender/masters/*.py`, so the slots stale all ~140 thumbnails, about 40 GPU-minutes.
- The Brief then wrote it as *"owed at the next snapshot"*, put *"the thumbnail re-render scheduled"* in the close, and listed it as a GPU job in the shared-surface table.

At handback the lead: *"Do NOT redo thumbnails until we get everything resolves, things in place, reduce the skin sets etc... total waiste of time"*.

The rule tells a run to find and price the re-make. It says nothing about whether the re-make is owed. Pre-release, with the skin sets still in flux, it is not. A thumbnail that is stale only because a master gained inputs that draw nothing at neutral is not a defect anyone is waiting on. This is the same family as the standing *"no release ceremony"* ruling (`.ai/AI_WorkingAgreement.md` §Settled practices): a snapshot check is release machinery, and it was allowed to schedule GPU work.

**Proposed fix.** After *"price what the change re-makes"*, add:

> **Pricing is not scheduling.** Name the re-make and its cost. Pre-release, a fingerprinted output left stale by a change that alters no picture is **left stale**: no step, no close item, no GPU slot. It becomes work only when the lead says so, or when a consumer reads that output now.

**Where it'd live.** The portable half in `discovery.md` §Risk lane. The local half (thumbnails stay stale until the skin work settles) in `LOCAL_DELTAS.md`'s publishing-producer rows or §Weighting. The refiner decides which half goes where.

---

### 2 — A live cross-session message answered a consumer-boundary question in minutes, and no doc names it as a channel `[doc-gap]`

**Grounding.** The invocation said *"raise it [relief] with the platform before the format is written"*. `LOCAL_DELTAS.md` §Separation names three routes, all of them written ones: the consumer's asks doc in `docs/Planning/Research/`, the consumer's phase doc, and `PlatformDependencies.md`. Not one of them is a way for the library to *ask* the platform something mid-discovery.

`ListAgents` showed the platform's skin phase live as `P119_E4`, so I messaged it twice: the question with a recommendation, then three refinements. Both were answered within minutes, with reasons ("one row on each side, a wire bump and a rebuild"). I then recorded the answers in the public phase doc by role, content and date, never by the platform's ids. That followed §Separation's ruling-recording rule by analogy.

`discovery.md` §Working in a shared tree sanctions messaging only for a split between **sibling phases** in this repo.

**Proposed fix.** One line in §Separation:

> A question for a consumer can go by message to its live session (`ListAgents` / `SendMessage`). Its answer is recorded here as a ruling is (by role, content and date, verbatim where it decides), and the consumer's own docs stay its record.

**Where it'd live.** `LOCAL_DELTAS.md` §Separation. Possibly portable, as part of the sibling-split sentence in `discovery.md`.

---

### 3 — A cross-unit claim went stale between writing and committing, and the pre-commit `git status` caught it `[self-error-doc-could-prevent]` (low; the rule worked)

**Grounding.** The shared-surface table said `look.py` held *"an uncommitted edit"* of Phase25's. At the pre-stage `git status`, `ahead 1` showed Phase25 had committed it (`9c11f4b`) minutes earlier. I fixed the row before committing. This is exactly the case `discovery.md`'s *"decays in minutes"* rule describes. Filed only as confirmation; no change proposed.

**Where it'd live.** No change; see Keep these.

---

## Keep these

- **"Open with the relief question and raise it before the format is written" (the invocation's own order).** Taking it to the live consumer before the slots were written avoided a third slot nothing would write. It also surfaced the finish-coverage gap and the placement rule while both sides could still change their plans.
- **Read the consumer's ask whole, against its own classifications.** The seed's first placed piece, a bruise, is a *pigment* piece by the ask's own Q-PSM-2. Reading that turned the fixture into a tattoo, which also tests turn.
- **First human test: work out the feature's size in pixels from the camera code.** `look.py`'s `at(target, frame_m, …)` showed the existing hand view frames 0.20 m, so a 4 cm tattoo spans about 200–300 px. That removed a camera I would otherwise have planned to add.
- **"Re-check any cross-unit claim immediately before the commit that carries it"**: item 3.
- **Reading the fingerprint control rather than guessing.** `masters_hash` covering every master file is what made the cost visible at all, even if item 1 says what to do with it next.

## Dead weight

None.

## Open questions

1. **When the thumbnails are re-rendered** is the lead's (RD-P26-10: after things resolve and the skin sets are reduced). *"Reduce the skin sets"* names work no phase owns yet. It sits with the skin phases, not with the refiner.
2. **I announced the Grep/Glob tools as my search mode at the start; this session had no Grep tool.** Searches ran as plain `grep` through Bash in a mode that does not prompt. The backlog already holds the *"no Grep tool … saying so"* row, so this is not re-filed. Noted only so the refiner can count the sighting.
