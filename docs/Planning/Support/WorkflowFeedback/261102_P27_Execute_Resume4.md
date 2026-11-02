# Workflow Feedback — P27 / execute / resume 4

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P27` |
| **Mode** | resume run 4 (`ML_P27_E4`, from `1d6d73a`; a distinct run, not a continuation of `261102_P27_Execute_Resume3.md`) |
| **Outcome** | suspended — 27.2.10 (the jaw line), 27.2.11 (the back's mottling measured, "keep 2"), 27.2.12–27.2.13 (the front beside the original; the nipples pinned) landed and seen; the lead ended the run with `/retro` at ~430k; `ML_P27_E5` started on the lead's yes |
| **Shape** | behavior-touching (`tools/converters/fit/project_body.py`: `put --jaw-free`, `--delight-keep`, `--mottle-gain`, `--fit-suffix`; `fit --front-pins`) |
| **Confidence** | Ran fully: the execute loop (build, Unreal renders, measure, show, verdict, commit) four times. **Not exercised:** the close; `serve_to_stage.py`; ComfyUI (no generation this run). |
| **Date** | 2026-11-02 |

---

## Items, ranked

### 1 — A phase seeded out of a live phase's scope left that phase's Brief stale, and the executor answered the lead from it `[self-error-doc-could-prevent]`

**Grounding.** Asked *"how much more until you think we have this completed?"*, I estimated 4–5 sessions, with **"hands and feet from the picture (the rest of 27.2)"** as the biggest item — straight from Phase27's Brief step list (`27.2 — The fine skin, the seams, the hands and the feet`). The lead: *"We did break out a hands and feet phase I believe..."*. Phase28 (`Phase28_AiHandsAndFeet.md`, seeded `9a81f9b` the same day) had taken that scope, and says so itself (*"written beside `ML_P27_E3`'s live execute, which this doc does not touch"*) — correctly not editing a live phase's doc, but nothing pointed back. `execute.md` §Before you touch anything, item 1, makes a resume re-read the Outcome of **each phase that closed** since the Brief; Phase28 had not closed, it had been **seeded**, so no rule sent me to it. My own kickoff read only Phase27, the core docs and `git log` (where `9a81f9b Phase28 seeded … right after Phase27` was in plain sight in the first `git log -8`).

**Proposed fix.** In `execute.md` §Before you touch anything, item 1: *"…and the Brief of any phase SEEDED since, whose Outcome takes scope from this one — a lead-directed seed beside a live run is written without touching the live doc, so the carve-out is visible only from the new phase's side."* And for the seeding side (`discovery.md` seeding, or wherever a lead-directed seed is written beside a live run): deposit the back-pointer the way `retro.md` step 5 does for corrections — a concrete line owed to the live run, named in the seed commit's subject.

**Where it'd live.** `execute.md` §Before you touch anything (resume) · the seeding guidance (unsure which file owns lead-directed seeds).

---

### 2 — A target the agent CHOOSES on the mesh was checked against the picture, not against the geometry it stands for; the lead caught it `[self-error-doc-could-prevent]`

**Grounding.** hm08 has no nipple (vertices ~12 mm apart at the chest). I chose "each breast's most forward point" (±0.075, 0.377 m) as the pin's target, then verified by drawing the target on the **picture warped by the new fit** (`nipfit.png`): the areola sat on the green circle, so it read as done. That check could only confirm the pin worked, not that the target was right — it shares the step's assumption. The lead, on the Unreal render: *"they don't seem to be lined up the outline I see below"*, a screenshot circling the areola inside and below the breast's curve. The mound's centre (±0.090, 0.388) fixed it (*"yes better"*). This is the same class as `261102_P27_Execute_Resume3.md`'s headline (*"draw a geometry-chosen mask before using it; an instrument sharing the step's assumption cannot catch it"*), a second instance the same day in the next session — filed for the tally, not as a new rule.

**Proposed fix.** If the refiner takes Resume3's item, extend its wording from a *mask* to any *target or landmark the agent picks on the mesh*: check it on hm08's own shading (a flat-colour render, the control 27.2.10 already used), not on the source mapped onto it.

**Where it'd live.** With Resume3's item (`execute.md` §Verify, the ad-hoc row) · a `docs/Learnings/` line: *hm08 has no nipple or navel geometry finer than ~12 mm; a "most forward point" on a curved chest sits toward the middle.*

---

### 3 — The look view's `3d594fb` driver, the side-by-side sheet and the gap instruments live only in other sessions' job folders `[doc-gap]` (recurrence: backlog drain 4B, *"the look sheet's measurement as part of look.py, not a scratch script"*)

**Grounding.** Every look-view launch this phase needs the skin article as at `3d594fb` (F-P27-6). The phase doc's reproduce lines say *"through the `3d594fb` driver"* / *"a scratch sheet"* / *"a scratch instrument … not kept"* with no path. I found the driver (`look_body_served.py`), the side-by-side (`sheet.py`), the band measure (`rg.py`) and the gap instrument (`gap.py`) only by grepping `~/.claude/jobs/*/tmp/` for `today_article` and `mottl|band`, and copied them into this job's folder. Those folders are deleted with their jobs, so the reproduce lines are one cleanup from dead. The 27.2.5 number I was asked to close (*"26 against the original's 37"*) was from `rg.py` on a render sheet, which I could only tell by reading the script.

**Proposed fix.** Not a methodology change: the tools belong in the tree (`look.py --rev <sha>` for the article; a `--reference-picture` side-by-side; the band measure as a `look.py` option), the product question already carried in the backlog. The methodology half: a reproduce line that names a scratch tool must name its path, and a scratch tool cited by two sessions is promoted or committed under the phase's `_probe/` folder.

**Where it'd live.** The product question → the phase or a tracker issue (lead's call) · the reproduce-line rule → `execute.md` §Keep the lead oriented (the write ceiling's ledger).

---

## Keep these

- **Bisect by construction: one launch with C, the candidate and a flat-colour control** (`execute.md` §Build, "make the probe load exactly the harness's inputs"). The jaw line went from "(a) or (b)?" to proven in the map, in the body's texels, and then to the exact band, in three launches; each diagnostic atlas (edge strip only · band evened) split the next hypothesis.
- **Look at native pixels before showing, and a number is not the verdict** (`execute.md` §TRY, §Verify ad-hoc row). Caught my own mottle gain drawing a pale line down the spine at 1.8, and the gain matching the original's number (33 vs 37) while reading grey and blotchy — neither reached the lead as a proposal.
- **Build every lever at strength, measure, then show** (memory `look-work-build-the-full-set`). The mottling fork reached the lead as one picture with the levers already built and measured; the ruling was three words (*"keep 2, do the front next"*).
- **One flag per fix in the maker** (`--jaw-free`, `--fit-suffix`, a separate `fit_<picture>_pins`): every earlier atlas in the ledger still reproduces, and the lead's "before" columns were free.

## Dead weight

None.

## Open questions

1. **Lead decision, recorded only in the phase doc:** *"4k is plenty right now - we should save wahtever time we can"* stops RD-P25-20's 2K → 4K → 8K at 4K for Phase27's body. Does it also bind Phase28's hands and feet, and the skin-map spec's 8K set (`SkinMaps.md` §One subject's set at 8K)? If yes, it belongs in a research thread's `## Resolved` (`AI_WorkingAgreement.md`, a ruling whose blast radius exceeds the unit), which this run did not write. Which is it?
2. **Refiner:** item 1's seeding half — which command owns a lead-directed seed written beside a live run? `discovery.md` covers seeding inside a pass; this seed came from another phase's discovery session on the lead's direct ask.
