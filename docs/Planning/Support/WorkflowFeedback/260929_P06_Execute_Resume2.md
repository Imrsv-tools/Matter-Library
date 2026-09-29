# Workflow Feedback — P06 / execute / resume run 2

| | |
|---|---|
| **Verb** | `execute` |
| **Unit** | `P06` |
| **Mode** | resume run 2 → suspend-handoff (~455k context, in 6.3's floor follow-up) |
| **Outcome** | suspended. 6.3 done (click 3 approved by the lead: *"yep looks the same, look into the floor"*). The floor was diagnosed to two causes, and the lead ruled *"c then b, and yes on the calibration"*. (c) done; (b)'s first form failed and was reverted; the calibration code landed but has not been run on a valid master. Resume block in the phase doc (`b0ba134`). |
| **Shape** | behavior-touching (the Unreal runtime's texture path and mesh format, the Opaque master, the driver, the calibration) |
| **Confidence** | Ran fully: BUILD, TRY (one sitting), STRENGTHEN (a diagnosis through probes), the commit discipline. **Not exercised:** `execute_close`, the push, the package build, the other machine. |
| **Date** | 2026-09-29 |

Not a continuation of `260929_P06_Execute_ColdStart.md` (that is run 1). Its items 4 (staging-tree reds) and 5 (the batched run table) met again this run and are not re-filed.

---

## Items, ranked

### 1 — A fix verified only on the case it targets can break the case the lead last approved; nothing says to re-run that anchor before anything consumes the fix `[self-error-doc-could-prevent]`

**Grounding.** The two-call Opaque master (the lead's ruling b) was checked on its target, the metalness-0.87 probe, where ×1.09 / ×1.24 came to ×1.02 / ×1.08. The next action was `--calibrate`, which consumed that master. The fit came back `SUN_K` 0.030 (was 1.033), which is absurd. Only then did an A/B show the master had broken the dielectric at Mix 0: the grey card read ×1.14 / 1.16 / 1.39 against Storm, where the single call reads ×1.006 / 1.002 / 0.996. The grey card was the case click 1 approved. One wasted calibration run, one A/B and a revert followed, and it was caught only because the number was absurd. A 20 % error would have been fitted into the constants silently.

**Proposed fix.** A verify-before-edit row: *"You verified a change on the case it targets → before anything CONSUMES it (a calibration, a re-baseline, a package), re-run the case the last sitting approved. A fix that holds on its target and breaks the anchor is the commonest regression, and a consumer turns it into a plausible-looking number."*

**Where it'd live.** `execute.md` §Verify before edit (portable).

---

### 2 — Calibrating a light factor on a material makes the renderers' material-model difference part of the light; a probe with no material model in it separates the two `[doc-gap]`

**Grounding.** D8 and 6.1 fitted `DOME_K` (1.068) and `SUN_K` on the grey card, a rough dielectric whose look is mostly the diffuse model. A white mirror, which reflects exactly the dome's radiance in any correct renderer, read 0.533 in Unreal against Storm's exact 0.503. The diffuse model's difference had been absorbed into the dome factor and then scaled every reflection 6 % too bright. The lead ruled to move `DOME_K` to the mirror. The same run's probe method (below) found it in two renders.

**Proposed fix.** A learning, plus the rig docs: *"Fit a light factor on a probe with no material model in it (a white mirror for a uniform dome; the visible dome for exposure). Fit a material-bearing reference only for what remains, with the light fixed."* D8's wording (*"calibrated on the grey card"*) is amended by the lead's ruling and needs conforming at the close.

**Where it'd live.** `docs/Learnings/` (the Unreal domain the close creates; or Storm/Blender, since it applies to any renderer the rig calibrates), `tools/parity/JOB_FORMAT.md`.

---

### 3 — The cross-tool bisect that worked was a PROBE ARTICLE: a copy of a known article with one value changed, run through the full rig into scratch; nothing records that the rig supports it `[doc-gap]`

**Grounding.** Unreal-only variants (one launch, one setting per suspect) found *which* input drove the difference: with metalness held constant, Unreal's floor correlated 0.95 with Storm's, up from 0.40. They could not say *which tool* was off, because Storm cannot take an Unreal job. The grey card's `.mtlx` rewritten by string replacement (base 1 or 0.1, metalness 1 or 0.87, roughness 0 / 0.45 / 0.95) and run as `rig.py <path.mtlx> --no-blender --out <scratch>` gave both tools the identical input. Six probes settled it: metal agrees at every roughness, and part-metal does not. `rig.py` already accepts a path and `--out`; it took a read of its argument parser to learn that.

**Proposed fix.** One line in `ToolingConventions.md` (the parity-rig row): *"`rig.py` takes a `.mtlx` path and `--out`: a copy of an article with one value changed, written outside the tree, is the cross-tool one-variable probe. Keep it out of `MatterLibrary/`."*

**Where it'd live.** `docs/ToolingConventions.md` (local), perhaps a line in `execute.md`'s bisect-by-construction guidance (portable: "vary one input in every tool at once").

---

### 4 — Unreal's Python commandlet: a script's `unreal.log` lines never reach `-stdout`, and a stub `unreal` module catches Python errors in seconds `[doc-gap]`

**Grounding.** The masters commandlet printed "Python script executed successfully" with no `MATTER …` lines at all. They were at Log verbosity, visible only in `unreal/MatterRuntime/Saved/Logs/MatterRuntime.log`, and that cost a round of doubt about whether the script ran. Two commandlet runs failed on plain Python errors: a `**{'a': …}` keyword colliding with a parameter named `a`, and a binding returning a string, not the `(bool, str)` the C++ signature suggests. A 60-line stub `unreal` module (`runpy` over the builder, fake nodes that record links) then caught such errors before each launch. It cannot validate pin or property names; the real commandlet still does that.

**Proposed fix.** In the LOCAL_DELTAS "RUN" row, or the coming Unreal learnings: *"Read a commandlet script's own output from `Saved/Logs/<Project>.log`, not stdout. Run a builder against a stub `unreal` first; commit the stub beside `build_masters.py` if it keeps earning its place."* Whether to commit the stub is the lead's call (it is a new tool, not a gate).

**Where it'd live.** `docs/Learnings/` (Unreal), `LOCAL_DELTAS.md` (the RUN row), or `unreal/` (the stub).

---

## Keep these

- **One ask for a batch of Unreal runs, then same-class repairs applied autonomously and SURFACED.** An `AskUserQuestion` with three options (all / CPU only / wait) got *"Go: all three"* once. The recompile and re-render after the filter fix, and the probe renders under *"look into the floor"*, ran without re-asking, each named in the handback as covered.
- **Drain to the click first.** Click 3 went to the lead with the floor named as an open diagnostic, not after chasing it. The lead approved the sweep and *then* directed the investigation.
- **"A parameter that should matter and barely moves indicts the instrument."** Anisotropic filtering, confirmed inside the runtime (`filter=4 aniso=16`), moved the floor 3.71 → 3.68. The run dropped the filtering hypothesis instead of claiming a fix. The change stayed, labelled "no measurable effect".
- **Bisect by construction in one launch.** Eight settings, one per suspect, in one Unreal launch found the metalness correlation (0.95) in about a minute of GPU time.
- **The context meter's 450k note.** It arrived as a first-time redesign (b's second form) was the next step. The run did one diagnostic A/B, reverted to a consistent tree, rebuilt the masters to match, and suspended with a resume block.

## Dead weight

None.

## Open questions

1. **Lead decision (owed next run):** if the Substrate-budget check does not explain the two-call break, the linear metal mix means leaving D6 (*"each master is Epic's function plus our network"*), e.g. our own Slab with `F0 = lerp(dielectric F0, base, m)`, or accepting Epic's behaviour. The resume block records both.
2. **Refiner:** item 1's row may overlap the existing *"a count you measured yourself goes stale at your next commit"* row. That row covers re-measuring after the last change. Item 1 is about *which case* to re-measure (the approved anchor) and *when* (before a consumer), so it may belong as a clause there, not a new row.
