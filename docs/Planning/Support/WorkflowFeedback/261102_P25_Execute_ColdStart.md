# Workflow Feedback — P25 / execute / cold start

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P25` |
| **Mode** | `cold start` (25.1 of the head build; the next session `ML_P25_E2` was started at this retro, on the lead's yes) |
| **Outcome** | `suspended` — 25.1's chain built as a tool and proved byte-identical to the probes; click 1 sat and passed (*"D beats all"*); two fit fixes from the sitting landed (symmetric landmarks, brows snapped to the cards: *"brows look better"*); the inner-corner line is open |
| **Shape** | `behavior-touching` |
| **Confidence** | Ran fully: BUILD, TRY (one sitting and two fix showings), the divergence row for a false Brief premise, commit discipline on a tree shared with Phase26's live execute. **Not exercised:** the close, a push, high-rigor. |
| **Date** | `2026-11-02` |

Step 0: the next session was offered and started first; this run's chat-only handoff (the open item, the current files, the render workaround, what is owed) went to `ML_P25_E2` by message, because that session owns the phase doc now (§step 5's live-run rule). It is repeated in §Open questions 1 so it is not only in a message.

---

## Items, ranked

### 1 — A sibling's UNCOMMITTED edit to a shared article broke the click surface; nothing says to render against the last clean commit `[doc-gap]`

**Grounding.** At the launch of click 1, `look.py` raised `Unsupported: … sliders ['makeup_amount', 'makeup_color_map', 'makeup_finish_map'] are not carried by Unreal's masters yet`. Phase26's execute session had makeup inputs in every skin article, recipe and `blender/masters`, uncommitted, with the Unreal masters not yet rebuilt. `execute.md`'s blind spots cover a sibling's *files* (`git status`) and *runtime state*, but not a sibling's half-built edit that makes the shared surface unlaunchable for everyone else. I found `look.today_article(art, rev, folder)` (the `--today` mechanism) and drove `look.main` through a scratch script that monkeypatched `find_article` to the article at `3d594fb`. It worked, but it was a spike in a job folder that is deleted with the job, so the next session must rebuild it.

**Proposed fix.** One line in `execute.md` §Commit discipline's blind spots: *"A sibling's uncommitted edit can make a SHARED surface unlaunchable (an article the renderer cannot draw yet). Do not wait on it and do not touch it: render against the last commit that launches, by the tool's own at-revision path, and name the revision in the ledger."* Locally, `look.py` could take `--at REV` for the skin article itself, so this is a flag, not a monkeypatch. That is a tool change for a working verb, the lead's to schedule.

**Where it'd live.** `execute.md` (portable) · `LOCAL_DELTAS.md` "the way this project is RUN" row, if `--at` lands.

---

### 2 — I judged an alignment side by side and called it "level"; the lead's marked screenshot found the brow tail one round trip later `[self-error-doc-could-prevent]`

**Grounding.** After the symmetric-landmark fix I looked at a 2× before/after band, saw two level brows and handed it over: *"the two brows now level, each under its brow cards."* The lead returned a marked screenshot: the painted tail ran below the cards' tail, and a line ran down from the inner corner. An overlay of the cards' projected outline on the render, which I built only afterwards as `check/brow_mask.png`, shows the short brow points in one look. `execute.md`'s Verify table already says *"Alignment is judged by an overlay or a difference, never side by side"*. It sits as one clause inside the long "ad-hoc check" cell, and I did not connect it to "showing a fix".

**Proposed fix.** In `execute.md` §TRY, beside *"a click you saw come out wrong never reaches them"*: *"A FIT is shown only after you have overlaid the reference outline on the render yourself (the mesh's feature — the opening, the card, the mask — drawn on the picture); side by side you will see 'level' and miss the shape."*

**Where it'd live.** `execute.md` §TRY (portable).

---

### 3 — The Brief dropped a step from the probe chain the lead approved, by assertion; only the port's byte-compare caught it `[doc-gap]`

**Grounding.** The build map said the field holds the ear pads *"at zero move (the ear is the maker's)"*. The approved atlas (`D_grad_p2`) came from a chain that moved the drawn ear onto the pad first (`probe5_earproj.py`). Ported as written, the root level of the ear gradient read [0.60, 0.27, 0.18] against the probe's [0.69, 0.36, 0.24], and the island showed Krea's ear spilling off the pad. This was caught only because the first act of the build was to run the tool on the probe's exact input and compare it to the probe's output. That is §BUILD's *"make the probe load EXACTLY the harness's inputs"* used in reverse, which this run did by choice.

**Proposed fix.** `plan.md` / `discovery.md` Brief: *"A build map that drops or changes a step of a probe chain the lead approved names the measurement that justified it; otherwise the step is ported as the probe ran it."* `execute.md` §BUILD: *"Porting probes to a tool: the first check is the tool on the probe's own input, compared with the probe's own output (byte or near-byte) BEFORE any change the Brief asks for."*

**Where it'd live.** `discovery.md` / `plan.md` Brief rules · `execute.md` §BUILD (portable).

---

### 4 — My wait-until-ready loop on a server I launched matched log words, missed the launcher's own refusal, and would have run forever `[self-error-doc-could-prevent]`

**Grounding.** `until curl …/system_stats | grep -q comfyui_version || grep -q -E 'Traceback|Error|error:' comfyui.log; do sleep 1; done`. The launcher exited at once with *"WorkingDrive not mounted … open it in Dolphin first"*: no "Error", so no match. I found it only by checking by hand, then stopped the loop with `TaskStop`. Rule 3 says an until-loop must match *"the failure signatures"*. For a process I launched, the reliable failure signature is the process being gone, not a word in its log.

**Proposed fix.** Rule 3: *"Waiting on something you launched: the loop also ends when the process has exited (its PID gone), whatever its log says."*

**Where it'd live.** `execute.md` rule 3 (portable).

---

### 5 — Fitting landmarks on a render where the feature is not drawn: three lead round trips for one cause `[doc-gap]`

**Grounding.** hm08's front render has empty eye openings and no brows, so MediaPipe guesses them there. The low eye (Pass 3, F-P25-25), the 10–17 px tilt and the short brow tail (this run) are one cause, found piece by piece, each after the lead saw it. The eventual method, each landmark group snapped to a geometric reference (depth for the openings, the mesh's symmetry, the brow cards drawn through the camera), plus a symmetry measurement on a symmetric mesh, would have found all three in one pass.

**Proposed fix.** A learning (stack-specific): *"MediaPipe on a rendered mesh guesses any feature the render does not draw; before using its points, snap each group to the mesh's own reference and measure left/right symmetry."*

**Where it'd live.** `docs/Learnings/` (a domain for image-model fitting; none exists yet: the backlog's §stack facts says add on a second sighting, and this is the second).

---

## Keep these

- **Port, then byte-compare to the probe, before changing anything.** It caught item 3 and made "D is the probes' result" a measurement, not a hope.
- **Cross-session messages:** a closed session passed on a lead ruling, Phase26 announced its file split and GPU use, and I sent the GPU queue and this handoff. No file collisions despite Phase26 editing `look.py` and the masters beside this run.
- **Checking what each column drew from the written materials** (`flat_normal.png`, `roughness_bias 0.25`, D's map, no makeup) before trusting the render.
- **The divergence row for a false Brief premise** (*"build it, log a deviation, show it"*): one commit, no round trip.

## Dead weight

None.

## Open questions

1. **Handoff to `ML_P25_E2`, recorded here as well as sent by message (§step 0):** the first item is the line running down from the image-right inner eye corner (the same on both eyes, untouched by the landmark fixes; the picture's crease or hm08's corner point, undiagnosed). The current files are in git-ignored `library/parity/P25_Head/` (`D_brow.png`, `lm_hm08.npy` with eyes, symmetry and brows, `brow_cards.npz`); the picture is a copy of `P25_Pass3/uv_a_s90_seed7.png`. The look view needs the at-revision render (item 1) while Phase26's makeup is uncommitted. Owed: the regeneration proof (the WorkingDrive must be mounted for ComfyUI) and `run_all.py` after the last code change. *"Lips look better on A"* is answered by RD-P25-2's maker lips at 25.2.
2. **For the lead, not the Refiner:** should `look.py` take `--at REV` for the skin article (item 1), so a sibling's half-built article never blocks a sitting again?
