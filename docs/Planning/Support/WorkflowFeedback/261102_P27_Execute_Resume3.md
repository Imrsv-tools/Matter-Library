# Workflow Feedback — P27 / execute / resume 3

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P27` |
| **Mode** | `resume run 3` (`ML_P27_E3`, from `7131ef3`); a distinct run, **not** a continuation of `261102_P27_Execute_Resume.md` |
| **Outcome** | `suspended` — four look fixes landed and each was seen and passed by the lead (colour kept `53b68f3`, one skin at the neck `94f684b`, shoulder dots `e8ce3cd`, the patch under the jaw `6cc2c0b`); the jaw line measured, not fixed (`1d6d73a`); handed to `ML_P27_E4` at ~410k |
| **Shape** | `behavior-touching` (`tools/converters/fit/project_body.py`, four new `put` options, defaults unchanged) |
| **Confidence** | Ran fully: execute's BUILD → TRY loop four times with the lead present, the look view, `run_all.py`. **Not exercised:** the close, a push, the structure step. |
| **Date** | `2026-11-02` |

---

## Items, ranked

### 1 — A region chosen by geometry was used before it was looked at; it took the lips instead of the chin `[self-error-doc-could-prevent]`

**Grounding.** For the jaw patch (27.2.8) I selected "the chin's underside" as head texels with height under 0.70 m and a down-facing normal, from where I *assumed* the face sat. The face is lower (nose tip 0.69 m, chin 0.616 m), so the mask took the lower face and both lips. Worse, the "dark-red rim" I had measured as the defect was the lower lip seen from below: a walk down the throat had been ordered by height, mixed the lips in, and I read their red as a defect. Two builds, three Unreal renders and a render-order test went into it before an overlay of the changed texels **on the atlas's own layout** showed it in one picture.

**Proposed fix.** Before a step uses a mask chosen by position or normal, draw it: the mask over the atlas (or the mesh), plus one printed landmark (the nose tip, the chin's lowest point) that pins its frame. "A region you have not looked at is a hypothesis about where things are."

**Where it'd live.** `execute.md` §Verify before edit, beside the ad-hoc-check row (a mask is an instrument too), or a `docs/Learnings/` entry on hm08's layout.

---

### 2 — My check that the lips were untouched was built on the same wrong assumption, so it agreed with the mistake `[self-error-doc-could-prevent]`

**Grounding.** After the lips came out orange in the render, I checked "no head texel above 0.69 m changed", which is the same mis-assumed height. It read 0, I trusted the number over the picture, and I spent a render testing whether Unreal was drawing later candidates from coarser mips. The ad-hoc row already says a reading that disagrees with the picture indicts the instrument. What it does not say is that an instrument sharing the step's own assumption cannot catch that assumption being wrong.

**Proposed fix.** One clause in that row: *"…and an instrument that selects its subject with the same assumption as the step under test cannot catch that assumption — check it in the asset's own frame (an overlay on the texture or the mesh), not through the step's coordinates."*

**Where it'd live.** `execute.md` §Verify before edit, the ad-hoc-check row.

---

### 3 — The GPU-sharing check reads a compile as "Unreal busy" `[doc-gap]`

**Grounding.** `ps -ef | grep "[U]nrealEditor"` matched another session's clang processes (their command lines carry the engine path), so a look-view launch aborted and waited. `LOCAL_DELTAS.md` §Two machines says what to do about an interactive editor or Studio (ask) and about a `-nullrhi` run (wait), but says nothing about a build. I waited, because a render on top of a large compile risks the box's memory (earlyoom history), but the rule had nothing on it.

**Proposed fix.** Add a line: a compile of the engine or editor is not GPU work but is memory pressure — wait for it like a `-nullrhi` run, and tell it apart from the editor by the process name (`clang`/`ld`), not by the path.

**Where it'd live.** `LOCAL_DELTAS.md` §Two machines (port-local; this box's facts).

---

### 4 — The look view has no close camera on the face's lower half `[doc-gap]`

**Grounding.** The chin patch and the jaw line were diagnosed from ~100-pixel crops of the whole-body front view, enlarged; the body views (27.1) have a neck from behind, a wrist and an ankle at 40 cm, but nothing under the chin or along the jaw, where the head meets the body at the front. The jaw line is left open partly because no view can separate a texture line from the mesh's shading there.

**Proposed fix.** A `look.py --body` view of the throat and jaw from the front-below at 40 cm, next to the neck view. This is the phase's own tooling, so it may be `ML_P27_E4`'s first step rather than a method change.

**Where it'd live.** Phase27 (the Brief's judge views); unsure that it is method at all.

---

## Keep these

- **One labelled picture per stop, with the comparison and what "right" looks like said in one sentence.** The lead answered each of the four in one line (*"yes one skin now, fix the shoulder dots next"*) and named the next target; there were no wrong-picture round trips this run.
- **Measure where the gap enters before changing anything.** Putting the atlas back through the original picture's own camera split the "too orange" gap into chain steps vs Unreal in one run and pointed at the two culprits.
- **Every look fix built as an option, defaults unchanged.** Every earlier atlas still reproduces from its ledger line, and the dropped tries (`--chin`, the 3 mm join) were removed or reverted cleanly.

## Dead weight

- None.

## Open questions

- The jaw line (27.2.9): a pale strip of Phase25's head where it meets the body, which the neck fill copies onto the body, or the mesh's shading at that seam? Recorded in the phase doc for `ML_P27_E4`.
