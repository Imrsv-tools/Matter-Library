# Workflow Feedback — P20 hand-off + M7 runtime v6 / execute / machine hand-off

| | |
|---|---|
| **Verb** | `execute` (Phase20's click-4 hand-off, on the machine with Unreal), then lead-directed work in the same session: the M7 *runtime owed* line (Phase21 21.1, `unreal-runtime-v6`) |
| **Unit** | Phase20 (click 4) · `PlatformDependencies.md` M7 (Phase21 had closed by the time v6 was published) |
| **Mode** | hand-off from the other machine; one session across 2026-10-16 → 2026-10-25, with two lead waits (the re-serve go-ahead, the publish go-ahead) |
| **Outcome** | done — Phase20: dev install re-served into Studio's runtime, click 4 handed to the lead (later seen at the platform's sitting). M7: v6 built, smoked against v5, published, pinned and pushed (`dca758a`) |
| **Shape** | behavior-touching (a published runtime, the driver flag) |
| **Confidence** | Ran fully: pull/converge, `run_all.py`, `serve_to_stage.py` into Studio's runtime, `unreal/build.sh all`, the rig (`--character`, `--sweep`, `--no-blender`) on a local and a pinned runtime, `publish.sh 6`, commit and push by SHA. **Not exercised:** Studio itself (the lead's click), Blender parity (not runnable on this machine). |
| **Date** | 2026-10-25 |

Not a continuation of any other file. Step 0: nothing was left only in chat. The result is in M7 and `dca758a`, and Phase20's click 4 is recorded on the platform's side (`57d3498`).

---

## Items, ranked

### 1 — The *runtime owed* line's own smoke could not show the change it was asked for `[doc-gap]`

**Grounding.** M7's step (6) said: *"smoke: `rig.py --character Skin_FitzpatrickIV…`, where the Unreal column should match v5's at the defaults"*. That smoke is right for *"nothing moved at the defaults"*, but it cannot see the tint, which is why the runtime was asked for. The character job renders the defaults only, and `rig.py` refuses `--sweep` with `--character` (*"the character renders the defaults"*). The tint is visible only on the test scene's `--sweep` row `tint blue` (`rig.py:120`). I found that by reading `rig.py`, not from the request. Run on both runtimes, the sweep was the real proof: 26 of 28 Unreal pictures were byte-identical, and the two `tint blue` ones moved to Storm's (close-view mean 21.2 → 5.1). It is the same class as `execute.md` §TRY *"ask whether the surface can SHOW the thing the click is about"*, applied to a hand-off's smoke rather than a sitting.

**Proposed fix.** A *runtime owed* line names **two** smokes: one that the defaults did not move (old vs new runtime, byte compare), and one that **drives the changed path** (the slider, the row, the article the change is for), run on both runtimes, so the pair can differ. *"The writer of the line names the row that shows the change, and the hand-off says what right looks like there."*

**Where it'd live.** `LOCAL_DELTAS.md`, the Unreal test runtime producer row (where *runtime owed* is defined), or `quick-fix.md` step 4's *runtime owed* branch.

---

### 2 — Nothing says which runtime the rig actually ran, so an old-vs-new compare can agree by construction `[doc-gap]`

**Grounding.** Smoke A (the v5 baseline) wrote its pictures at 17:17:57, the same minute the new package landed in `unreal/MatterRuntime/Packaged/`. The rig's output says only *"unreal: wrote 6 pictures"*, and the Unreal log names no runtime. If the driver preferred a local package, A would have been v6 and the *byte-identical* result would have proved nothing. I had to read `drivers/unreal.py`'s resolution order: `$MATTER_UNREAL_RUNTIME`, then `$MATTER_UNREAL_EDITOR`, then the pin unpacked under `unreal/package/<tag>/`. I also had to check `env` for a stray `MATTER_*` and read `unreal/package/unreal-runtime-v5/.sha256` before the compare meant anything. The memory note gives the `MATTER_UNREAL_RUNTIME=…/Packaged/Linux/MatterRuntime.sh` form, but no tracked doc says how to tell afterwards which runtime ran.

**Proposed fix.** Either the rig prints the runtime it resolved (`unreal: runtime unreal-runtime-v5 (pinned)` / `unreal: runtime $MATTER_UNREAL_RUNTIME=<path>`), which is a tool change and a lead/phase call, or, at least, the producer row states the resolution order and the tell (`unreal/package/<tag>/.sha256`). A pre-publish test then knows which side of the compare is which.

**Where it'd live.** `tools/parity/JOB_FORMAT.md` or `docs/ToolingConventions.md` (the tell), and the backlog for the rig change. Unsure which.

---

### 3 — Testing a new runtime before publish needs a hand flag in a shared tree, which then sat uncommitted for five days `[doc-gap]`

**Grounding.** M7 step (5) says to set `RUNTIME_TINTS_SCATTER = True` *"in the commit that carries the new `RUNTIME.json`"*. The local v6 smoke needed it set first (with it `False`, the driver refuses a tinted Subsurface picture), and it has no environment override. So the edit sat uncommitted in this shared tree from 2026-10-20 to 2026-10-25, while the publish waited on the lead. In that window, any rig run here on the pinned v5 would have drawn a tinted skin's scatter untinted instead of refusing it, which is exactly what the flag exists to prevent. I flagged it to the lead on 10-25 and offered to revert.

**Proposed fix.** The driver should take the capability from the runtime it resolved rather than from a hand flag: a capability field in `RUNTIME.json` or the package, or an env override (`MATTER_RUNTIME_TINTS_SCATTER=1`) for a pre-publish test. A local test then leaves the tracked file alone. That is a tool change, so it is the lead's call. Until then, a *runtime owed* line should say: *"set the flag only for the smoke and revert it if the publish does not follow in the same sitting"*.

**Where it'd live.** The backlog (a driver change), plus the *runtime owed* step wording in `LOCAL_DELTAS.md`'s producer row.

---

### 4 — On the machine with Unreal, the dev install IS Studio's runtime; Phase20's hand-off assumed a separate deploy step `[doc-gap]`

**Grounding.** Phase20's hand-off step 3: *"The platform's deploy carries the dev catalog to Studio … Find the deploy step on that machine; it is not visible from here."* Measured here on 2026-10-16:
- `IMRSV_STAGE_RUNTIME` points at the Stage runtime inside Studio's own plugin.
- The platform's `deploy-to-studio.sh` itself runs `serve_to_stage.py --runtime <that dir> --no-restart` from this checkout.

So one `serve_to_stage.py --no-restart` *is* the route to Studio. Also, **any platform deploy re-serves whatever this checkout holds**: a platform session's 17:45 deploy had re-served the pre-pull tree (old *PureSky* names) four minutes before I looked. The re-serve was first refused by the auto-mode classifier (*"Modify Shared Resources"*): five platform sessions were live on that runtime. That refusal was correct, and so was the hand-off's *"ask the lead first"*. The lead's "yes" then cleared it.

**Proposed fix.** Record it in `LOCAL_DELTAS.md` §Two machines: *"On the machine with Unreal, the served dev install is Studio's own Stage runtime, and every platform deploy re-serves it from this checkout (`--no-restart`). Re-serve with `--no-restart`, and only on the lead's word while platform sessions are live."* A hand-off to that machine then names one command instead of *"find the deploy step"*.

**Where it'd live.** `LOCAL_DELTAS.md` §Two machines (the Refiner's lane, so filed here).

---

### 5 — Context use was not reported at act boundaries `[self-error-doc-could-prevent]`

**Grounding.** This session ran across five lead turns (pull and serve, build, publish) and never put a context reading in a ledger line, which `execute.md` §Keep the lead oriented asks for at each act boundary. The P18 retro (`f81c03b`) filed the same lapse.

**Proposed fix.** None new. This is a recurrence count for the item already in the backlog.

**Where it'd live.** Backlog (tally only).

---

## Keep these

- **Baseline the builder's `MATTER built …` lines before building** (memory note, and the M7 precedent). It turned *"unchanged at its defaults"* into a one-line diff: only `subsurface_follows_base` on the Subsurface master.
- **`execute.md` §Verify: "confirm the check can fail"**. The Storm-vs-Unreal control made the byte-identical v5/v6 result mean something, and the same discipline forced the runtime-resolution check in item 2.
- **Read the platform's deploy script before re-serving**. It showed the serve is the deploy's own step (item 4), so `--no-restart` matched what the platform already does.
- **`.claude/CLAUDE.md` §Git's push row**: `git log origin/main..HEAD` read line by line, then push the SHA by value. One commit was ahead, it was mine, and it went up clean.
- **Asking publish and push as one explicit question**. The lead's one-word "publish" answered both without a second round-trip.

## Dead weight

None.

## Open questions

1. **Lead decision:** the git-ignored `library/staging/matterlib-0.1.0/` from 2026-09-24 (30 `.dds` files no freeze lists) has kept `approval_binds_freeze` and `release_verify` red on this machine since at least 2026-10-05, and it survived the 2026-10-25 re-freeze. Delete it or rebuild it? It is not an agent's to remove.
2. **Refiner/lead:** `Phases/Complete/Phase21_SkinMaps.md` §Deferred still reads *"Requested 2026-10-20 … `unreal-runtime-v6`"*. M7 now records it done. Does a closed phase's Deferred row get a dated *done* note, or is M7 the only live record? I left the closed doc untouched.
