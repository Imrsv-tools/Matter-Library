# Workflow Feedback — P16 / execute / cold start through the close

| | |
|---|---|
| **Verb** | `execute` (BUILD → TRY → STRENGTHEN, then `execute_close`, in one session at the lead's word) |
| **Unit** | `P16` — *Every Entry Says What It Is* |
| **Mode** | cold start → close |
| **Outcome** | done — 16.1 to 16.3 landed, `dev.5` published, closed `eb4b70c`, pilot re-approved `f113b3a`, all pushed |
| **Shape** | behavior-touching (assembler, recipe gate, serve tool, snapshot builder, 95 `.mtlx`, Blender library) |
| **Confidence** | Ran fully: execute, the close, a publish, a pull/converge, cross-session messages. **Not exercised:** the high-rigor lane, `execute_repair.md`, Unreal (the machine with Unreal). |
| **Date** | 2026-10-14 |

Not a continuation of `261014_P16_Discovery_ColdStart.md` (the discovery session's deposit); a distinct run.

---

## Items, ranked

### 1 — A finding that cites a probe must carry the probe's exact command, or the executor re-derives it and can get it wrong silently `[doc-gap]`

**Grounding.** The Brief's F-P16-1 says Storm read a stamped `.hdr` "pixel for pixel… rendered as a visible dome with `usdrecord`". The scene file survived in `/tmp/claude-p16/probe/`, the command did not. At 16.2 I rebuilt the check from the scene and left out `--enableDomeLightVisibility` (Storm S4) and `--disableCameraLight` (S1): four renders, repo and stamped, came back byte-identical — and solid white, because no dome was drawn. The identical hashes were evidence of nothing. It was caught only because I looked at the PNG, and then because a 7× intensity change did not move the hash (`execute.md`'s "a parameter that should matter… indicts the instrument" — which worked exactly as written).

**Proposed fix.** In `discovery.md`'s findings discipline: *"A finding resting on a probe records the probe's exact invocation (binary, flags, inputs) in the finding or beside its scratch, because the executor re-runs it against the shipped thing; a scene file without its command is half a probe."*

**Where it'd live.** `discovery.md` (portable). The Storm half is already S1/S4 in `docs/Learnings/Storm/` — this run is a second sighting that the flags are needed *for a dome comparison*, which could be one clause on S4.

---

### 2 — The close's "promote before the 🎉 and the push" has no row for a lead who says push before he has promoted `[doc-gap]`

**Grounding.** `LOCAL_DELTAS.md` (publishing-producer row) and `execute_close.md` row A: hand the promote command at the start so it lands before the `🎉` and the push. I did; the lead's close instruction said *"…update the docs and push so the consumers can see"*, and the promote had not been run when the docs were done. I pushed anyway, reasoning that the re-freeze was **already on origin** (a sibling's push had carried 16.1's `7db3005`), so the push changed no approval state, and the promote landed afterwards as its own commit — the lead then said *"commit and push the approval"*. That reasoning was invented at the close; nothing says it.

**Proposed fix.** One clause in the publishing-producer row: *"If the re-freeze is already on origin (check `merge-base --is-ancestor`), the close may push before the promote — say so in the `🎉` body — and the promote lands as its own commit under the same push go."*

**Where it'd live.** `LOCAL_DELTAS.md` (local: the release lifecycle is this repo's).

---

### 3 — Making a schema key required turns every RED fixture into a false red, and can make one pass for the wrong reason `[self-error-doc-could-prevent]`

**Grounding.** 16.1 made `contributor` required in `recipe.schema.json`. The recipe lane's RED fixtures (`tools/validators/fixtures/recipes/`) lacked it, so ten failed on G2 before their own guard — and `wrong_type.json`, whose guard *is* G2, **passed on the missing key instead of its own defect** (the lane's selector is `any(e.startswith(guard + " "))`). Found by the first post-edit gate run; fixed by keying all twelve and adding `missing_contributor.json`, with a `FALSE RED:` line on the gate. `execute.md`'s "read what selects its subject" row covers this in spirit; what was missing was the trigger "you are adding a required key".

**Proposed fix.** In `execute.md` §Verify, the gate-subject row: *"(vi) Adding a REQUIRED field to a shape a RED fixture set exercises: key every fixture in the same commit, or each fails on your field before its own guard — and a fixture whose guard is the same check passes for the wrong reason."*

**Where it'd live.** `execute.md` (portable), or a `docs/Learnings/` line if the Refiner judges it stack-specific.

---

### 4 — Scratch under `/tmp/claude-p<NN>/` collides across verbs on the same phase `[doc-gap]`

**Grounding.** I created `/tmp/claude-p16/` for the sitting and found the discovery session's `msg*.txt`, `probe/` and `reasm/` already in it. Nothing was overwritten (new names only), but a same-named file would have been, and item 1's surviving scene file was only findable because of the shared folder — by luck.

**Proposed fix.** Name scratch by session, not phase (`/tmp/claude-<session-name>/`, e.g. `P16_E1`), and have discovery keep any probe it cites somewhere durable or name its scratch path in the finding.

**Where it'd live.** `LOCAL_DELTAS.md` or the ClaudeCode learnings (where B10–B11's scratch-scene rule lives).

---

## Keep these

- **"A parameter that should matter and barely moves the reading indicts the instrument before the subject"** (`execute.md` §Verify) — it turned four agreeing white frames into a found instrument fault in one probe.
- **The re-assembly's "each diff exactly the two lines, any other count stops"** (RD-P16-10, from discovery) — 95 files rewritten through the one writer with a mechanical stop; nothing to review by eye.
- **`LOCAL_DELTAS` §Separation's sweep of consumer repos for rulings about the library** — run for *"pull and review the feedback"*, it found the website's doc still allowing CC BY 4.0, written hours before RD-RO-2: the exact F-RO-29 pattern, caught this time.
- **Asking the consumer what its own id means** (the Brief's note on L3) — one cross-session message got a one-sentence definition, an independent check of the dev catalog, and the one real gap (the RuntimeCatalog text), which the close then fixed.
- **Hand the first clickable result early** — 16.1 reached the lead's Blender in under an hour; the verdict (*"yep!"*) took one message.

## Dead weight

None.

## Open questions

1. **For the lead, not the Refiner:** GPA-Q2's rename clause in Identity (*"a replacement gets its own name and the old one is marked `deprecated`"*) is the agent's reading of the existing lifecycle, marked `Reevaluate`. The platform is about to build on the bare-name key; whether a rename in place is ever allowed is a contract call worth ruling before it does.
