# Workflow Feedback — Velvet / matter-batch / cold

| | |
|---|---|
| **Verb** | `/matter-batch` (one row, run through `/matter-generate` §1–5). Not one of the five verbs; the lead asked for this retro directly. |
| **Unit** | Batch `261113-1`: `Velvet_Natural_Clean_Base_s001_v01` |
| **Mode** | cold start, one row named by the lead ("make velvet next"), out of `next`'s order |
| **Outcome** | done: the row built as a draft and committed with two new shared overlays (Pilling01, Creases01) and a new base set; the full gate stopped part-way on the lead's word, scoped check run instead; the batch summary committed. The review page (§7) is not built yet. |
| **Shape** | behavior-touching (new generators, textures, a recipe) |
| **Confidence** | Ran fully: `/matter-batch` §1–6, `/matter-generate` §1–5 and §3a. **Not exercised:** §7 (the review), `run_all.py`'s staging, release and tool-test lanes. Items 1 and 2 are measured; item 3 is one row's evidence. |
| **Date** | 2026-11-13 |

---

## Items, ranked

### 1 — The full gate's `compression` lane takes about an hour on a one-row batch, and `/matter-batch` §6 requires it `[doc-gap]`

**Grounding.** §6: *"Run `uv run tools/validators/run_all.py` (0 FAIL …)"*, once before the batch's last commit. The row added 4 textures. The `compression` lane (`run_all.py` `run_compression`) compresses **every** texture under `MatterLibrary/textures/` (275) **twice** for its determinism check, each in its own `docker run --platform linux/amd64 compressonatorcli` container, emulated on an Apple Silicon box. After an hour it was 162/275 into the second pass, with `staging` (encoder-gated, a third encode) and the tool tests still to come. Its docstring still says *"On the dev box … the full sweep (~12 s over 30 textures) runs."* The lead asked *"why do we compress all textures just to add velvet?"* and had it stopped. Every lane that judges an article (grammar, per-material, determinism, recipe, catalog, provenance) had already passed in the first ~25 minutes. The batch's own textures were then checked in about a minute with `tools/compressors/compress_textures.py --determinism --only <substring>` and `--validate --only <substring>`; all PASS, byte-identical. A SIGTERM'd gate also skips its `finally`, leaving ~1.5 GB of `mtc_run_a_*`/`mtc_run_b_*` in the temp dir.

**Proposed fix.** Two halves, and the refiner decides which is method. (a) **The skill:** §6 names the scoped form for a batch: *"The full gate re-encodes every texture twice (about an hour). For a batch, run `run_all.py` with the encoder lanes skipped, plus `compress_textures.py --determinism` and `--validate` with `--only` per new texture; the full gate runs before a release, not per batch."* This needs a way to skip lanes, which `run_all.py` lacks. (b) **The tool (a product question for the lead, not the refiner):** the lane caches by source content hash, or takes a changed-paths scope; its docstring is corrected; it cleans its temp folders on a signal.

**Where it'd live.** `.claude/skills/matter-batch/SKILL.md` §6 (a); `tools/validators/run_all.py` (b, a tool change: a phase or quick-fix the lead calls).

---

### 2 — I quoted the gate's result from a memory written before the encoder existed here `[self-error-doc-could-prevent]`

**Grounding.** Asked what the gate does, I told the lead my notes said *"16 PASS · 2 SKIP · 0 FAIL"*. That was October, when `compression` and `staging` SKIPped for want of an encoder. On this branch the encoder is present, those lanes run, and the timing is a different world. I launched the gate in the background without measuring or estimating its length, then reported "still running" twice before measuring anything.

**Proposed fix.** Already done for my own memory (a dated correction, plus a note on the hour and the scoped form). For the method: before starting a long background gate, state its expected length from a measurement (the last run's output, the lane's texture count), not from a remembered count.

**Where it'd live.** memory (done); possibly `/matter-batch` §6 beside item 1.

---

### 3 — The rig never judges a tintable article TINTED, and the row's worst fault only showed in a close Blender view `[doc-gap]`

**Grounding.** Velvet is authored as an undyed ivory so the Creator tint reaches dyed colours, as Canvas and Felt are. The rig's sweep has a "tint blue" row, which moved alike in all three tools and passed. But §3 has the agent judge *"does it read as the matter"* only at defaults. The fault only showed when the lead asked to see it up close and I built a scene in their Blender with a deep red tint: the fuzz colour is a constant the tint does not reach, so every dyed velvet gets a pale pink frosting. That is the finding the review most needs, and the rig's agreement verdict is blind to it by design (all three tools frost alike). A three.js OpenPBR velvet the lead found was rendered beside it for reference; it showed the haze is the fuzz model's, which the sheet could not have shown either.

**Proposed fix.** §3: *"An article authored pale for the tint (`base_color_tint`, a fabric, a paint) is also judged tinted: read the sweep's tint row as the matter, not only for agreement, and say on the Critique whether the tinted version still reads as the matter."* And `LOCAL_DELTAS.md` already says *"a sheet built for colour cannot judge a weave … show a weave … a close camera in the lead's Blender"*: §3 could point at that for a pile or a weave.

**Where it'd live.** `.claude/skills/matter-batch/SKILL.md` §3.

---

## Keep these

- **Defaults-only rig runs while fixing, the sweep once (§3).** Three runs took 1.6 min of rig time; run 1 caught "reads as plaster" in 26 s.
- **The tile-repeat memory ([maintainer rejects visible tile repeat]).** I tiled each new layer 3 × 3 in scratch before writing it. That caught two grids before any rig run: Pilling01's islands, and Creases01 at 10 cm, which moved to 1 m.
- **`wishlist.py mark --lane`** recorded L3 → L2 in one call, with the reason in the recipe and the summary.
- **`git show --stat` after every commit (§Git).** All three commits read back at the expected file and line counts.
- **B10/B11 (a headless factory scene into its own file, render and look before opening).** The first test render was blown out and too close; the lead never saw it.

## Dead weight

None.

## Open questions

1. **Lead:** should the Creator tint reach `fuzz_color`? That's the library fix for every tinted pile fabric (velvet, felt, canvas). It touches the assembler and all three renderers' masters, so it's phase-sized. Recorded on the batch summary's redo line.
2. **Lead:** this batch was committed on `platform/compressed-texture-samplers`, on the lead's word, not on `main`. It reaches `main` with that branch.
3. **Owed:** `/matter-batch` §7, the review page (`review_pages.py 261113-1`) and opening it for the maintainer, was not done; the lead ended the run with this retro.
4. **Recurrence:** the close Blender view and the five-sphere comparison were scratch scripts again (`velvet_close.py`, `velvet_compare.py`, not committed). This is the backlog's existing product item (a committed sitting or view builder; drain 4A, P21), and this run is one more instance.
