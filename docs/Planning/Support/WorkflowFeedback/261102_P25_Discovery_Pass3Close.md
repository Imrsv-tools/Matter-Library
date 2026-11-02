# Workflow Feedback — P25 / Discovery / Pass 3 close

| | |
|---|---|
| **Verb** | `discovery` |
| **Unit** | `P25` |
| **Mode** | resume (Pass 3 continued from `ML_P25_D4`'s hand-off), then close: BRIEF READY |
| **Outcome** | done: the low eye fixed (F-P25-25), the ear as a gradient (F-P25-26, RD-P25-19), OMF's ear ask (F-P25-27), the resolution steps (RD-P25-20), the Brief rewritten; `ML_P25_E1` started on the lead's word |
| **Shape** | doc-only in the tree (probe scripts beside the phase doc); probes and renders under the git-ignored `library/parity/` |
| **Confidence** | Ran fully: discovery probes, the look view, the web-only agent, launching two sessions. **Not exercised:** a `run_all.py` baseline (left to execute). |
| **Date** | 2026-11-02 |

Not a continuation of `261101_P25_Discovery_Pass3Ears.md` (`ML_P25_D4`'s): this is the next session on the same pass.

---

## Items, ranked

### 1 — A continuation pass skips the consumer sweep, and the lead had to raise a consumer blocked on the library `[doc-gap]`

**Grounding.** Mid-run the lead wrote: *"Phase 119 is goign to be stuck waiting for you to draft makeup, bruises etc..."*. The platform's asks doc `261101_R_PlatformSkinAndMakeupAsks.md` had sat for a day with no library pass, no Status footer and no ledger row, while Phase25 ran three discovery sessions. `LOCAL_DELTAS.md` §Separation puts the sweep (*"footers here saying the library's pass is owed"*) in discovery's Pass 1. Pass 2 recorded *"Consumers: not re-swept"*, and Pass 3's sessions never ran it. None of the asks needed Phase25; only a roadmap ordering stood in the way.

**Proposed fix.** Any discovery session that opens on a new day, not only Pass 1, runs the owed-footer part of the sweep: a single grep of `docs/Planning/Research/` for asks docs without a library pass. Whatever it finds goes in the first message, with its date, as *"waiting on the library, independent of this phase?"*

**Where it'd live.** `LOCAL_DELTAS.md` §Separation (the sweep's trigger), or `discovery.md` Read §2 if portable.

### 2 — A three-column picture read as "pick the best-looking", when the question was one column `[self-error-doc-could-prevent]`

**Grounding.** `P3_ear_gradient.png` showed the projected picture, the gradient and a flat-colour render, labelled only by what each was. The lead asked: *"What is the intent here... for me to pick the best looking version and that will be the path?"* The route was already ruled (RD-P25-18). The picture repeated a rejected route as a column and never said which column was being judged or what the lead was asked. That cost a round trip.

**Proposed fix.** When a picture for the lead carries reference columns, its labels say which column is judged and which are reference ("REFERENCE: …", "JUDGE THIS: …"), and the handback states the question in one line. A ruled-out route appears only as "before".

**Where it'd live.** `discovery.md` First human test (*"what the lead can say after"*), or `AI_WorkingAgreement.md` §Working With the Lead.

### 3 — The session namer's `--next "/research …"` continues THIS session's name even for an unrelated topic `[doc-gap]`

**Grounding.** The lead asked for a research session on the platform's makeup asks. `session_name.py --next "/research PlatformSkinAndMakeupAsks"` printed `ML_P25_D6`, a Phase25 discovery name: by design, `/research` continues the calling session's thread (2026-10-26 change). The topic had nothing to do with P25. I named it `ML_R_PlatformMakeupAsks` by hand.

**Proposed fix.** `--next "/research <Topic>"` continues the caller's name only when the caller is itself a `/research` thread (an `R_`/topic name). From a phase verb's session, it gives `<prefix>R_<Topic>`.

**Where it'd live.** Upstream `agentic-engineering` `workstation/claude/hooks/session_name.py` (a workstation tool, not this repo); `retro.md` step 0 if the rule is stated there.

### 4 — An Unreal check chained in front of a launch does not gate it `[self-error-doc-could-prevent]`

**Grounding.** `ps -ef | grep "[U]nrealEditor" | wc -l; …; probe1_shine.py …` printed `1` and launched anyway. Another session's short run was up, and it was gone a minute later. The `;` chain made the check a printout. Later launches used `n=$(…); [ "$n" = 0 ] || exit 3` plus a background loop that waited for 3 quiet minutes.

**Proposed fix.** One sentence in §Two machines: *"the check gates the launch in the same command (`[ "$n" = 0 ] || exit`); a check chained with `;` only prints."*

**Where it'd live.** `LOCAL_DELTAS.md` §Two machines.

### 5 — A tracked doc said "answered in the handback", a pointer to chat `[self-error-doc-could-prevent]`

**Grounding.** Recording RD-P25-20, I wrote that the lead's body question *"is answered in the handback of `ML_P25_D5`"*. The answer (routes per region, its own phase, the unclothed-body question) lived only in chat until `/retro` step 1 caught it. It landed in commit "Phase25: the lead's body question - ML_P25_D5's answer written down", after `ML_P25_E1` had started on the same doc. `discovery.md` already says *"write it down or drop it"*. This is a sighting of the same failure in its "pointer to chat" form.

**Proposed fix.** Add to that rule: *"a tracked sentence that points at a handback, a chat or 'see above' is the same failure: write the answer itself."*

**Where it'd live.** `discovery.md` §Discovery discipline (the perishable-claim paragraph).

---

## Keep these

- **One labelled picture at native pixels per question.** The lead judged each in one reply (the eye, the ear, the whole ear).
- **The flat-colour render beside a map change.** It settled *"is this the map or the mesh?"* for the ear, and it shows the lead what the mesh can carry.
- **Re-running the old inputs through the same chain before trusting a new number.** The stored island reproduced byte-identical, so the fold-count difference (2.195 → 2.201 %) was the fix alone.
- **Checking a lead rule on the data before rendering.** "Don't touch the face" was verified on the atlas (0 changed texels with face weight ≥ 0.15) before the look-view launch.
- **Recording both of the lead's messages verbatim when the second corrects the first** (RD-P25-20), so the sweep could be undone cleanly.

## Dead weight

none

## Open questions

- Whether MediaPipe and SciPy should become project dependencies. The Brief keeps them on `uv run --with`, following `bar_maps.py`'s OpenEXR. A lead question if the tool is used outside Phase25.
- ComfyUI was found stopped mid-run (2026-11-02) by no act of this session. `ML_P25_E1` starts it if needed (RD-P25-7).
- An Unreal process ran briefly beside one look-view launch (`eargrad/look1`, a throwaway provisional render). Its numbers were not used.
