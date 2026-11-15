# Workflow Feedback — Velvet to main / lead-directed landing / cold

| | |
|---|---|
| **Verb** | None of the five. Lead-directed git work ("bring the whole branch over", then "we stop the sampler research here on a branch"), run in a session that was otherwise a side project. The lead asked for this retro directly. |
| **Unit** | Landing batches `261113-1`/`-2` (`Velvet_Natural_Clean_Base_s001_v01`) and the EmissiveGrainAsks research pass on `main`; the sampler work stays parked on `platform/compressed-texture-samplers` |
| **Mode** | cold. **Not a continuation** of `261113_Velvet_MatterBatch_Cold.md`, but its item 1 (the hour-long compression lane) is the same friction; this file adds only what that file missed. |
| **Outcome** | done: 10 commits cherry-picked onto `main` (one conflict in `gen_fabrics.py`, both fabrics kept), the Blender asset file rebuilt (`3ce1029`), pushed on the lead's word (`abf404e..3ce1029`) |
| **Shape** | behavior-touching (the asset file); the cherry-picks were already reviewed content |
| **Confidence** | Ran: `check_asset_library.sh` (PASS, 157 conform), `compress_textures.py --determinism --only Velvet_Pile` (ALL PASS). **Not run:** the full `run_all.py` gate, on purpose (item 2). |
| **Date** | 2026-11-15 |

---

## Items, ranked

### 1 — Adding a material does not update the Blender asset file, and nothing notices when it lags `[doc-gap]`

**Grounding.** Velvet was built and kept on 13 Nov. When I brought it to `main` today, `blender/asset_library/MatterLibrary.blend` still lacked it: `/matter-batch` and `/matter-generate` never rebuild that file, and `run_all.py` has no lane that compares the committed file against the articles on disk (`check_asset_library.sh` checks a freshly generated file's structure, not the committed one). This is the second time in two days. Batch `261114-1` needed its own follow-up commit (`ec2830f`): *"The asset file was rebuilt this morning, before the batch, so it lacked the ten articles kept today."* Both times the lag was found by someone looking, not by a check.

**Proposed fix.** (a) `/matter-batch` §6, before the batch's last commit: *"Rebuild the Blender asset file (`tools/conformance/check_asset_library.sh <scratch>`, copy `MatterLibrary.blend` in when it PASSES and the article count went up by the batch's rows)."* (b) The tool: a `run_all.py` lane, or a mode of `verify_asset_library.py`, that fails when an article on disk is missing from the committed `.blend`. That is a product change the lead calls.

**Where it'd live.** `.claude/skills/matter-batch/SKILL.md` §6 (a); `tools/validators/run_all.py` or `tools/conformance/verify_asset_library.py` (b).

---

### 2 — Second instance of the hour-long gate: landing a reviewed article on `main` had no named check, so I picked one by judgment `[doc-gap]`

**Grounding.** The 13 Nov retro's item 1 is still undrained. Today was its second instance in a different shape: no new article, only already-gated commits moving to `main`. The lead's framing was *"adding 1 material runs all"*. Nothing says which checks a landing (a cherry-pick or merge of reviewed content) owes. I chose `check_asset_library.sh` (item 1) plus `compress_textures.py --determinism --only Velvet_Pile`, about 2 minutes together. `run_all.py`'s argument parser has no way to skip lanes, so "the full gate minus the encoder lanes" is not something I could run.

**Proposed fix.** Same as the 13 Nov item 1 (a), extended: name a **one-article check set** once (the per-article lanes + `compress_textures.py --only` + the asset-library rebuild) and point both `/matter-batch` §6 and a branch landing at it. The tool half is unchanged: a `--skip`/`--only` lane option on `run_all.py`, or a changed-paths scope.

**Where it'd live.** `.claude/skills/matter-batch/SKILL.md` §6; `LOCAL_DELTAS.md` if a landing check is project-local.

---

### 3 — Which Blender writes the asset file is recorded nowhere `[doc-gap]`

**Grounding.** `check_asset_library.sh` runs `$MATTER_BLENDER` or else whatever `blender` is on `PATH`. `ec2830f` says it used *"official 5.2.2"*. This Mac has only 5.3.0, and `MATTER_BLENDER` was unset. I only found the mismatch by opening the committed file (`bpy.data.version` = 5.2), and asked the lead. They chose 5.3, so the file's version moved in a commit whose subject is about velvet. One more session without that check would have bumped it silently.

**Proposed fix.** Record the asset file's Blender version once (the add-on's minimum, or a pinned build), and have `check_asset_library.sh` print the version it ran, or warn when it differs from the committed file's.

**Where it'd live.** `tools/conformance/check_asset_library.sh`; the version itself in `LOCAL_DELTAS` §Two machines or `docs/ToolingConventions.md`.

---

## Keep these

- **The memory notes on LFS (fetch before merge, `-c http.sslCAInfo`, `lfs push` then push by SHA).** The fetch, fast-forward, LFS upload and push each worked first time.
- **Building the asset file in scratch first, then copying it in only after the gate PASSED and the catalog file came out byte-identical.** The committed file was never left half-written.
- **Push by SHA after a fresh fetch and `merge-base --is-ancestor` (§Git).** It confirmed the push was a fast-forward of only this run's 11 commits.

## Dead weight

None.

## Open questions

1. **Lead:** the rebuilt `.blend` is 3.28 MB against 3.42 MB before, with one more article. The gate passes. I assume the 5.3 save is the cause but did not check.
2. **Lead:** `platform/compressed-texture-samplers` was never pushed and is the only copy of the sampler work (5–6 Nov). It also still holds copies of the velvet commits, now duplicated on `main` under new SHAs. If the sampler work resumes, rebase it onto `main` and those copies drop out.
3. **Note:** the shared checkout was switched from that branch to `main` for this landing. A session expecting the branch would find `main`.
